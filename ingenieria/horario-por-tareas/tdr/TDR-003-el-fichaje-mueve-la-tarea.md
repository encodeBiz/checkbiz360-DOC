# TDR-003 — Fase 2: el fichaje mueve la tarea

**Fecha:** 2026-10-16
**Estado:** En implementación (API y app)
**Componente:** `encodebiz-api` — `services/checkinbiz` (fichaje), `services/tasks` (actividad), `services/reports` (descanso); app `checkbiz360`
**Decisiones de referencia:** [README](../README.md) D5 y D6; [TDR-001](./TDR-001-modo-dias-generados-y-escritor.md)

---

## 1. Qué entrega

Para una persona en «Horario por tareas», el gesto es el fichaje de siempre y la tarea va
detrás: **Entrar inicia la tarea del turno, Salir la completa, Descanso la pausa y Fin de
descanso la reanuda.** La app esconde los botones de iniciar y completar de la tarea y pone el
nombre de la tarea en los de fichar. El supervisor no cambia: validar, rechazar, puntuar,
cancelar y completar desde el panel siguen igual.

Fuera de esta fase: las alarmas por tarea (fase 3), las dos líneas del informe (fase 4) y el
cuadrante en el modo (fase 5).

## 2. Quién mueve la tarea: la puerta delegada de `tasks`

`checkinbiz` no reimplementa ninguna transición. Llama al servicio de tareas por su **puerta
delegada**, `/api/v1/tasks/delegated/...`, con la clave S2S y `x-actor-uid` = el `uid` de la
persona (conector-asistente ADR-005). Desde ahí la petición es de esa persona, con sus reglas
de siempre: asignación, jornada abierta, geocerca de la tarea, evidencia al completar,
política de «todos completan», actividad, eventos, avisos y espejo a Postgres. Lo que el
servicio de tareas rechaza, el fichaje lo devuelve tal cual.

| Fichaje | Llamada delegada | Orden |
|---|---|---|
| `checkin` | `PATCH /:taskId/status` `{status: "in_progress", geo}` | fichaje primero, tarea después: iniciar exige jornada abierta |
| `checkout` | `PATCH /:taskId/status` `{status: "completed", geo}` | **tarea primero**: completar exige jornada abierta, y si falta la evidencia la salida no se escribe |
| `restin` | `POST /:taskId/pause` `{reason: "break"}` | fichaje primero |
| `restout` | `POST /:taskId/resume` `{geo}` | fichaje primero |

Cada llamada lleva `viaChecklogId` en el cuerpo; el servicio de tareas lo anota en la
actividad (`metadata.viaChecklog`), que es el «iniciada por fichaje» del README.

`TASKS_INTERNAL_URL` (por defecto `http://tasks:3006`) y `ENCODEBIZ_API_KEY` en `checkinbiz`.

## 3. Qué tarea

- **Entrar:** la del turno que elige el fichaje (`scheduleApplied.taskId`, TDR-001 §5).
- **Salir, Descanso, Fin de descanso:** la de la entrada abierta, leída de su
  `metadata.scheduleApplied.taskId`. No se vuelve a calcular: si la tarea se movió entretanto,
  la jornada sigue siendo de la que se empezó.

Solo cuando el fichaje lo hace la propia persona. Un fichaje de administrador
(`isAdmin`) no mueve tareas: es una corrección de jornada, no un gesto de trabajo.

## 4. La geocerca

En el modo, el trabajo puede no estar en la sucursal (ayuda a domicilio, limpieza en
clientes). Así que **Entrar valida contra el lugar de la tarea si lo tiene, y si no contra la
sucursal**; el resto de fichajes, igual que hoy. El fichaje guarda la distancia como siempre y
la tarea vuelve a medir su valla al iniciar, que es lo que ya hace.

## 5. Antes de escribir nada

En Entrar se comprueba, antes de escribir el fichaje, que la tarea existe, que la persona está
asignada y que su estado admite empezar (`assigned` o `in_progress`). Así el caso normal no deja
una jornada abierta con la tarea sin empezar. Si aun así la tarea falla después (caída del
servicio), el fichaje ya está escrito y la respuesta lo dice: `task.ok = false` con el código, y
la app ofrece reintentar el inicio de la tarea, que sí es posible porque la jornada está abierta.

En Salir, si la tarea ya está completada, validada, rechazada o cancelada (el supervisor la
cerró), no se toca y la salida se escribe sin más.

## 6. La respuesta

La de siempre, con un campo más cuando el modo actuó:

```jsonc
201 {
  "code": "checklog/created",
  "checkLog": { … },
  "task": {"taskId": "…", "action": "start" | "complete" | "pause" | "resume", "ok": true, "status": "in_progress"}
  // o {"taskId": "…", "action": "start", "ok": false, "code": "task/out_of_worksite", "error": "…"}
}
```

En Salir, un rechazo de la tarea **es** el rechazo del fichaje: `400` con el código del servicio
de tareas (`task/evidence_required`, por ejemplo) y sin salida escrita.

## 7. El descanso fijo

En el modo no aplica (README D6): con un turno por tarea restaría el fijo en cada tarea. El
fichaje congela `scheduleDay.breakMinutes = 0` cuando `source = "tasks"`, y el informe diario
(`BuildEmployeeDailyReports`) usa el descanso real en los ciclos cuya entrada tiene
`schedule_applied.source = "tasks"`, aunque la sucursal tenga el descanso fijo puesto.

## 8. La app

- Detecta el modo con la lectura con la que arranca: `GET /calendar` →
  `data.scheduleMode`, y los turnos de `effectiveDay.day.shifts` con `taskId` y `title`.
- En el modo, esconde iniciar y completar de la pantalla de la tarea (notas y evidencias
  siguen), y los botones de fichar dicen la tarea: «Entrar · <título>, 10:05» con el turno
  que toca ahora, «Salir · <título>» con la de la jornada abierta.
- Manda posición siempre.
- Antes de Salir, si la tarea exige evidencia y no tiene, la pide; si el servidor responde
  `task/evidence_required`, lleva a la pantalla de la tarea para subirla.
- Lee `task` de la respuesta: si `ok` es `false` en Entrar, lo dice y ofrece reintentar el
  inicio de la tarea con su endpoint de siempre.
- Sin turno ahora, el error `checklog/out_of_schedule` se lee como «No tienes ninguna tarea
  ahora».

## 9. Pruebas

Unitarias donde haya lógica pura; QA `54-horario-por-tareas` amplía con HPT-11 a HPT-15:
entrar inicia, salir completa, salir sin evidencia exigida se rechaza y no escribe salida,
descanso pausa y reanuda, y el fichaje de administrador no mueve la tarea.

## 10. El horario no se reconstruye al fichar

Pregunta de Jose al implementar: si el fichaje cambia el estado de la tarea, ¿se reconstruye el
horario? Sí: `onTaskDay` regeneraba el día —y copiaba la semana a la plantilla (D11)— en cada
escritura de la tarea. El resultado era el mismo, porque una tarea en curso o completada sigue
siendo el mismo turno, pero eran varias escrituras por persona y día para nada.

Ahora el trigger sale sin hacer nada si la escritura no cambia lo que forma el día:
`affectsGeneratedDay` (shared, con prueba) mira inicio, vencimiento, personas, título,
sucursal y si la tarea entra o sale de borrador o cancelada. Estado de trabajo, pausas, notas
y validación no cuentan. Crear y borrar, siempre.

## 11. Hecho el 2026-10-16

API en `feat/horario-por-tareas-fase2` de `encodebiz-api`, sin fusionar: `checkinbiz`
(`tasksModeAttendance.ts` y `createChecklog`), `tasks` (`withViaChecklog` en iniciar,
completar, pausar y reanudar), `reports` (descanso real), `shared` (`affectsGeneratedDay`) y
`firebase_sdk` (salida temprana de `onTaskDay`). Typecheck en verde en los servicios tocados y
27 pruebas unitarias. QA HPT-11..14 escrita, sin ejecutar: necesita los contenedores con este
código.

App en `feat/horario-por-tareas-fase2` de `checkbiz360` (d9fa7d0), sin fusionar, desde `develop`:
modelo del horario con el modo y la tarea de cada turno, la tarea que toca bajo los botones de
fichar, la ficha de la tarea sin iniciar/completar/pausar/reanudar para quien la tiene
asignada, y los avisos de «no tienes ninguna tarea ahora», evidencia al salir y tarea que no
se movió. `flutter analyze` sin nada nuevo y 157 pruebas de asistencia y tareas en verde, 4
nuevas. Diseño visual pendiente de retoque. Las dos ramas están empujadas a origin.

Para probarla de punta a punta hacen falta los contenedores de staging con la rama de la API:
hoy staging no la tiene.

## 12. En develop y en staging, 2026-10-16

- **API:** `feat/horario-por-tareas-fase2` → `develop` (f3cb851) → `staging` (5094c14). Por
  indicación de Jose, **sin el workflow**: el merge a `staging` lleva `[skip ci]`, y en el
  servidor de desarrollo se hizo `git pull --ff-only origin staging` con la clave
  `~/.ssh/github_deploy`, `up --build -d checkinbiz tasks reports` y
  `up -d --force-recreate nginx`. Los tres sanos; rutas 401/400 sin 502; `checkinbiz` con el
  código nuevo, `ENCODEBIZ_API_KEY` y `TASKS_INTERNAL_URL` por defecto. `onTaskDay` redesplegada
  en `dev-encodebiz` con `--solo`.
- **QA contra staging:** `54-horario-por-tareas` entera, 15 de 15, con HPT-11..14. HPT-07
  fallaba en el último CI de otra sesión porque D11 cambió lo que pasa al salir del modo (manda
  la plantilla propia, que era el espejo, no la de la sucursal); ajustado (4935cad).
- **App:** `feat/horario-por-tareas-fase2` → `develop` (28cf76e), fusionada en un worktree
  sobre `origin/develop` para no tocar el checkout de otra sesión. 157 pruebas en verde y sin
  errores de análisis.
- **Pendiente:** retoque visual de la app; devolver `plantillaAnterior` al quitar el modo (D11
  dice que es manual hasta que el selector lo haga solo); el pase.

## 13. Hotfix del 2026-10-17: el fichaje en el lugar de la tarea

**Lo que pasó en producción.** Jose probó el modo con una tarea creada desde el asistente con
«Calle de la Alondra, Carabanchel, 28025 Madrid», sin número. Google devolvió el centro
geométrico de la calle (`precision: center`) y la API lo aceptó como geocerca de 150 m. Jose
fichó desde la calle de la Alondra 3 —la propia oficina, a ~10 m del punto de la sucursal—, a
232 m de ese centro, y las tres entradas (17:35, 17:36, 17:40) se rechazaron con
`checklog/out_of_radius`. El GPS y el fichaje hicieron lo que debían; el fallo era aceptar una
calle sin número como lugar.

**Al revisarlo apareció otro:** §4 decía que solo Entrar se medía contra el lugar de la tarea, y
Descanso, Fin de descanso y Salir contra la sucursal. Quien entraba en un domicilio no habría
podido salir desde él.

**Arreglos (PR #162, en producción desde el 2026-10-17, f55c9f3):**
- Todo el fichaje de una tarea con lugar propio se mide en ese lugar (§4 queda así).
- El geocodificador marca `wholeStreet` (`route` sin `street_number`) y una tarea con ese lugar
  responde 400 `task/worksite_imprecise`. Comprobado en staging contra Google: sin número, 400;
  «Calle de la Alondra 3», 201 con `rooftop` a ~10 m de donde fichó Jose.
- 500 m por defecto en todas las geocercas (Jose, 2026-10-17): lugar de la tarea (o el de la
  sucursal si es mayor), sucursal, asistente, cuadrantes, puesta en marcha y Rentman.

QA HPT-15-01 (entrar, descansar y salir desde el lugar de la tarea, a 500 km de la sucursal):
16/16 en staging. Las funciones `onChecklogWrite` y `onActivateCheckbiz` también llevan el
cambio a 500 en el código, pero en producción siguen con código desplegado antes del porte a
`firebase_sdk` (29-jul y 4-sep): se despliegan aparte, con las demás.

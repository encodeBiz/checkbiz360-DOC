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
código. La app, en su rama propia (§8).

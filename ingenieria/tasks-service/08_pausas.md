# 08 — Pausas en las tareas

**Estado:** En implementación (2026-09-11). D1 decidida; D2–D9 se aplican tal como están escritas mientras no se diga otra cosa
**Origen:** petición de clientes reales

Lo que se pide: poder **pausar** una tarea en curso, **varias veces**, que ese tiempo
**salga en los informes** y que **se descuente** del tiempo de la tarea.

Todo lo que sigue es propuesta, no decisión tomada. Lo marcado como *estimación* no está
medido.

---

## 1. Lo que hay que decidir antes de escribir código

### D1 — ¿La pausa es de la tarea o de cada trabajador? — **DECIDIDA: de la tarea**

> Decidido por Jose el 2026-09-11.

Es la única que va al cliente: tiene dos respuestas cerradas, sin ella el modelo no se puede
escribir, y decide qué número aparece en un informe con el que se factura o se paga.

- **De la tarea**: una sola pausa abierta a la vez. La pulsa cualquiera de los asignados y
  queda anotado quién. El informe cuenta la duración del trabajo.
- **De cada trabajador**: cada asignado pausa lo suyo. El informe tendría que elegir entre
  horas-persona y duración, y la tarea solo estaría "en pausa" cuando lo estuvieran todos.

**Propuesta: de la tarea.** Con un solo asignado, que es el caso habitual, las dos opciones
dan el mismo número, y esta no obliga a abrir la discusión horas-persona / duración.

### D2 — La pausa no es un estado nuevo

La tarea sigue en `in_progress` y se le añade `pausedAt` (presente = pausada). Hacer `paused`
un octavo `TaskStatus` rompe tres cosas que existen hoy:

- La pantalla de inicio de la app consulta `status == in_progress`
  (`task_today_provider.dart`): la tarea pausada **desaparecería justo de donde se reanuda**.
- En las apps ya instaladas, `TaskStatus.fromString` convierte un estado desconocido en
  `draft`: la tarea saldría como "Borrador" y **no se podría ni iniciar ni completar**.
- La huella de cambios de Rentman (`huella()` en `pushTasksToRentman.ts`) incluye `status`:
  **cada pausa reenviaría la tarea a Rentman**.

Con `pausedAt` aparte, una app vieja ve la tarea "En curso" y la puede completar; no se
rompe nada.

### D3 — El plazo no se estira

`dueAt` es un compromiso con alguien, no un presupuesto de horas. `timeComplianceStatus` se
sigue calculando contra `dueAt`, haya pausas o no.

### D4 — Completar o cancelar con una pausa abierta la cierra

Se cierra en ese instante y se anota por qué (`endedReason: "completed" | "cancelled"`).
Prohibirlo obligaría a reanudar para acto seguido terminar, y es exactamente lo que haría una
app vieja que no conoce el botón. Lo observado —que nadie reanudó— queda registrado.

### D5 — Pausar es libre; reanudar pide lo mismo que iniciar

- **Pausar** no exige jornada abierta ni geocerca: se pausa precisamente cuando uno se va.
- **Reanudar** exige jornada abierta y, si la tarea tiene `workSite`, estar dentro de la
  valla, igual que iniciar: quien reanuda está volviendo al trabajo.

### D6 — Quién

Los asignados, y supervisor en adelante desde el panel. Son las mismas reglas que iniciar y
completar (`canOperateAssignedTask`).

### D7 — Motivo y avisos

- Motivo **opcional, texto libre**. Si más adelante se quieren analizar las pausas, se pasa
  a una lista cerrada.
- **Sin notificación** en esta versión. Una pausa es rutina, y avisar de cada una enseña a
  ignorar los avisos.

### D8 — Reabrir pone los contadores a cero

Volver a `assigned` o `draft` ya borra `startedAt`/`completedAt`. Las pausas eran de esa
ejecución: los contadores del documento vuelven a cero y el historial se conserva.

### D9 — Cómo se llaman las columnas del informe

Hoy "Tiempo invertido (h)" es `Fin − Inicio`: **tiempo transcurrido**, no tiempo trabajado.
Una tarea que se abre el viernes y se cierra el lunes cuenta el fin de semana. Descontar las
pausas no lo convierte en tiempo trabajado: lo convierte en tiempo transcurrido **menos las
pausas que alguien pulsó**. Por eso la propuesta es que el nombre diga lo que se mide:

| Columna | Qué es |
|---|---|
| Duración (h) | `Fin − Inicio`, como hoy |
| En pausa (h) | Suma de las pausas |
| Nº pausas | Cuántas |
| Duración sin pausas (h) | Duración − En pausa. **Es el número que pide el cliente** |

Renombrar "Tiempo invertido" cambia un documento que el cliente ya lee: se decide con él.

---

## 2. El modelo (propuesta)

**En el documento de la tarea** —para que el informe no tenga que leer nada más—:

| Campo | Tipo | |
|---|---|---|
| `pausedAt` | `Date?` | Inicio de la pausa abierta. Ausente = no está pausada |
| `pausedBy` | `string?` | Quién la abrió |
| `pauseId` | `string?` | Documento de `pauses` abierto, para cerrarlo sin buscarlo |
| `pausedMs` | `number` | Suma de las pausas **cerradas**. Por defecto `0` |
| `pauseCount` | `number` | Número de pausas, abierta incluida. Por defecto `0` |

El informe ya hace dos lecturas de subcolección por tarea y admite 1.000 tareas; sin los
contadores en el documento serían 3.000 lecturas por informe.

**Subcolección `pauses/{pauseId}`**, el historial: `startedAt`, `startedBy`, `reason?`,
`endedAt?`, `endedBy?`, `endedReason` (`resumed | completed | cancelled | reset`),
`durationMs?`.

**Rutas propias**, no `PATCH /:taskId/status`, porque la pausa no es un estado (D2):

- `POST /:taskId/pause` — `{entityId, reason?, geo?}`
- `POST /:taskId/resume` — `{entityId, geo?}`

Errores nuevos: `task/not_in_progress`, `task/already_paused`, `task/not_paused`. Reanudar
reutiliza los de iniciar (`task/no_open_session`, `task/geo_required`,
`task/out_of_worksite`).

**Transacción** sobre el documento en pausar y reanudar: dos asignados que pulsan a la vez
no pueden dejar dos pausas abiertas ni descuadrar `pausedMs`.

**Actividad** `paused`, `resumed` y `resume_rejected` (reanudar fuera de la valla, con el
mismo rastro que `start_rejected`). **Eventos** `task.paused` y `task.resumed`, y
`paused_at`, `paused_ms` y `pause_count` en el modelo público de la tarea: todo aditivo, sin
cambiar la versión `2025-08-01` (ver `eventos-webhooks/04_contrato-publico.md` §7). El motivo
de la pausa no viaja en el evento, por lo mismo que el texto de una nota.

### Qué pasa con cada combinación de versiones

| Servidor | Cliente | Resultado |
|---|---|---|
| Nuevo | App vieja | Ve "En curso", puede completar y eso cierra la pausa (D4). Bien |
| Nuevo | Panel viejo | Igual: "En curso", sin indicador de pausa. Bien |
| Viejo | App nueva | El botón de pausa da 404. **Por eso el servidor va a producción antes que la app a tiendas** |

---

## 3. Lo que no cambia, y por qué

- **Analítica.** `onWriteTaskForPattern` solo actúa en la transición a
  `validated`/`rejected`: una escritura de pausa no le mueve nada. Si se quiere la pausa en
  analítica, hay que ir a buscarla (F6).
- **Rentman.** Su huella no incluye los campos nuevos, y las horas que se le mandan salen del
  fichaje, no de las tareas (migración 009, D2).
- **`tasksHandler` de Firebase** (la copia de rollback). Ignora los campos nuevos. Si se
  volviera a él no se podría pausar, pero nada se rompe.

---

## 4. Fases, por uso

**Frecuencia: estimación, no medida.** Las tareas viven en el Firestore de producción, y el
snapshot diario del backoffice solo cuenta valoraciones, no actividad. Lo estimado:

1. **App** — donde se pausa y se reanuda. Es la acción más frecuente: varias por tarea y por
   día.
2. **Panel** — donde se mira. Varias veces al día por administrador.
3. **Informe** — unas pocas veces al mes por cliente.
4. **Webhooks** — solo los clientes con endpoints dados de alta.

**El orden se rompe en un punto:** el servicio `tasks` va primero porque las tres
superficies lo llaman, y sin él ninguna funciona.

Se puede medir: contando por día las actividades `started`/`completed` de producción.

### F1 — Servicio `tasks`

**Estado:** hecho y en `staging` (2026-09-11). Probado contra dev lo que se prueba sin
token: las rutas existen y responden 400/404 desde su controlador. Falta el ciclo completo.

**Objetivo:** pausar y reanudar existen y dejan rastro.

- Campos y subcolección de §2, rutas `pause`/`resume` con las reglas D5 y D6, en transacción.
- `updateTaskStatus`: completar o cancelar cierra la pausa abierta (D4); reabrir pone los
  contadores a cero (D8).
- Actividad `paused`/`resumed`, eventos y catálogo en `shared`.
- `03_contratos-api.md` actualizado.

**Criterio de éxito:** contra dev, pausar → reanudar → pausar → completar deja
`pauseCount = 2` y `pausedMs` igual a la suma de las dos; dos pausas a la vez dejan una sola
abierta; reanudar fuera de la valla da `task/out_of_worksite`; completar con la pausa abierta
—lo que hace una app vieja— la cierra con `endedReason: completed`.

**Necesita:** un token de dev para las pruebas (`npm run get-token`).

**Rollback:** nadie llama todavía a las rutas; revertir el merge.

### F2 — App

**Estado:** en `develop` y `staging` de la app (2026-09-11), con `flutter analyze` limpio y los
tests en verde. Sin probar todavía en un teléfono.

**Objetivo:** el trabajador pausa y reanuda desde el teléfono.

- `TaskModel`: `pausedAt`, `pausedBy`, `pausedMs`, `pauseCount` (+ `build_runner`). El
  conversor de fechas ya acepta `Timestamp` de Firestore e ISO.
- Entidad: `isPaused`, `canPause`, `canResume`. `canComplete` no cambia (D4).
- Botones Pausar/Reanudar en la ficha, aviso "En pausa desde las HH:mm" y distintivo en la
  tarjeta y en la de hoy.
- Textos en los cuatro idiomas (es, en, de, pt).
- Rama desde `develop`, **no desde `master`**.

**Criterio de éxito:** `flutter analyze` limpio; con el flavor de desarrollo contra
`api-staging.checkbiz360.com`, pausar, reanudar y completar.

**Rollback:** no está publicada.

**Tiendas:** subida manual, y solo **después** del pase a producción de F1.

### F3 — Panel

**Estado:** en `develop` y `staging` del panel (2026-09-11), con typecheck en verde.

**Objetivo:** el administrador ve qué está en pausa y desde cuándo.

- "En pausa" sobre el chip de estado, en el listado y en la ficha.
- Pausar/Reanudar en la ficha para supervisor en adelante.
- Tiempo en pausa y nº de pausas en la ficha; etiquetas `paused`/`resumed` en la actividad.

**Criterio de éxito:** desde el panel contra staging, el ciclo completo.

**Rollback:** revertir el merge.

### F4 — Informe

**Estado:** hecho y en `staging` (2026-09-11). "Tiempo invertido (h)" conserva su nombre
hasta que decida el cliente; la columna nueva se llama "Tiempo invertido sin pausas (h)".

**Objetivo:** el tiempo en pausa sale en el Excel y se descuenta.

- Columnas de D9, leídas de los contadores del documento: ninguna lectura más.
- Una tarea pausada que no ha terminado enseña las pausas hasta el momento y la duración
  vacía, como hoy.
- `07_integracion-informe-tareas.md` y `TDR-004` actualizados.

**Criterio de éxito:** en dev, una tarea con dos pausas da en el Excel los mismos números
que su actividad.

**Rollback:** revertir; los datos no se tocan.

### Después, no hoy

**F5 — Pausa automática desde el fichaje.** Si el trabajador ficha un descanso o la salida
con una tarea en curso, la tarea se pausa sola (`startedBy: "checklog"`). Es la fase que
hace verdadero el número de D9: sin ella, la duración sin pausas mide quién se acuerda de
pulsar, y una tarea que se queda abierta por la noche sigue contando la noche. El fichaje ya
lo sirve el contenedor `checkinbiz`, que llamaría a `tasks` por la ruta de sistema, como hace
Rentman con `HttpTasksClient`. *Estimación: 2–3 jornadas.*

**F6 — Analítica.** El tiempo en pausa como señal del patrón. No tiene sentido hasta que
haya semanas de datos, y conviene que F5 exista antes para que la señal no mida disciplina.

---

## 5. Hoy

*Estimación*, en el orden de §4:

| Paso | Quién | Tiempo |
|---|---|---|
| Validar D1–D9 | Jose (D1, con el cliente) | ~15 min |
| F1 servicio `tasks` + pruebas en dev | Claude | ~2 h |
| F2 app, hasta la build de desarrollo | Claude; prueba en teléfono, Jose | ~3 h |
| F3 panel | Claude | ~1 h |
| F4 informe | Claude | ~45 min |

Hoy todo llega a `staging` (dev). A producción, en este orden y en el pase de Jose:
**`tasks` + `reports` → panel → app a tiendas**.

# TDR-001 — Fase 1: el modo, los días generados y quién los escribe

**Fecha:** 2026-10-15
**Estado:** Diseño, pendiente de implementación
**Componente:** `encodebiz-api` — `packages/shared` (calendar), `services/checkinbiz` (calendar, checklog), `services/tasks` (validaciones), `services/firebase_sdk` (trigger), `services/analytics` (espejo y resolutor), `firestore.rules`, `firestore.indexes.json`
**Decisiones de referencia:** [README](../README.md), D1 a D4 y D10

---

## 1. Qué entrega esta fase

Al acabar, una persona con «Horario por tareas» activo ficha contra los turnos que forman
sus tareas, con el gesto doble de hoy (fichar y, aparte, iniciar la tarea); el fichaje
congela ese día como congela cualquier otro; el panel la ve esperada con sus turnos; y los
informes y las horas planificadas salen del día generado. No se toca la app: todo lo de
esta fase se prueba desde la API y el panel, y es lo que permite validar el modelo antes de
dar el paso del gesto único (fase 2).

Lo que la fase deja hecho, en orden de uso:

1. El campo `scheduleMode` en el calendario, heredado, con su validación y su comprobación
   al activarlo.
2. Los días generados por fecha en el calendario del empleado, y la función pura que los
   construye a partir de las tareas.
3. El trigger sobre `tasks` que los regenera, y la generación inicial al activar el modo.
4. El resolutor del día efectivo que, en el modo, lee el día generado antes que la plantilla,
   en Firestore y en Postgres.
5. Las reglas que hacen a una tarea incompatible con el modo, en todos los caminos que
   escriben tareas.
6. El espejo de los días generados a Postgres y lo que la disponibilidad hace con ellos.
7. Reglas de Firestore e índices.

## 2. El modo en el calendario

### 2.1 Campo

`BaseCalendar` (`packages/shared/src/calendar/Calendar.ts`) gana un campo opcional:

```ts
scheduleMode?: "weekly" | "tasks";
```

Está en los tres niveles. Se resuelve como la zona horaria, no como el horario: **gana el
nivel más cercano que lo tenga definido**, empleado, luego sucursal, luego entidad, y sin
ninguno es `weekly`. No depende de `overridesDisabled`, que apaga el horario de un nivel y
no su modo. `ResolveEffectiveCalendarUseCase` lo devuelve en `data.scheduleMode` y anota de
dónde vino en `sources.scheduleMode`.

Por qué el más cercano y no «el de la sucursal manda»: una sucursal entera de auxiliares va
por tareas y su administrativa, que ficha en la misma sucursal, sigue con horario semanal.
Con herencia por nivel más cercano, a ella se le pone `weekly` en su ficha y ya está.

### 2.2 Escritura

Los tres `upsert*CalendarController` de `services/checkinbiz/src/interfaces/http/calendar/`
aceptan `scheduleMode` en el cuerpo, lo validan (`weekly` o `tasks`, nada más; si no,
`calendar/bad_request`) y lo pasan al `upsert*Calendar` del repositorio como un campo más.
`null` lo borra, para volver a heredar.

**Al poner `tasks`** el controlador comprueba, antes de escribir, las tareas que lo harían
incompatible (D4) de cada persona afectada: en el ámbito empleado, esa persona; en sucursal
o entidad, todas las personas activas que heredarían el modo, o sea las que no tienen
`scheduleMode` propio. Se miran las tareas no canceladas de hoy en adelante en la zona de
cada persona. Si hay alguna sin hora de inicio, de más de un día o solapada con otra de la
misma persona, se responde:

```jsonc
400 {
  "code": "calendar/tasks_mode_conflict",
  "error": "Some tasks are incompatible with schedule by tasks",
  "details": {
    "conflicts": [
      {"employeeId": "…", "taskId": "…", "reason": "no_start" | "multi_day" | "overlap", "withTaskId": "…"}
    ]
  }
}
```

La lista enseña qué arreglar; nada se escribe. En sucursal o entidad la comprobación puede
ser larga, y se hace igual: activar un modo es una vez, y vale más esperar un segundo que
dejar a alguien con un día que no se puede generar.

**Al quitar `tasks`** no se borra nada: los días generados se quedan y simplemente dejan de
leerse, porque el resolutor solo los mira en el modo (§5). Si el modo vuelve, se regeneran
al activar. Los pasados son constancia (D3) y no se tocan nunca.

### 2.3 Lectura

`GET /calendar` devuelve `data.scheduleMode` y `data.sources.scheduleMode`. En el modo,
`effectiveDay` es el día generado (§5), y `data.weeklySchedule` sigue siendo la plantilla
por si el panel la quiere enseñar apagada. La app, en la lectura con la que arranca, ya
tiene ahí todo lo que necesita para la fase 2.

## 3. Los días generados

### 3.1 Dónde

Subcolección del empleado, hermana de `calendar`:

```
entities/{entityId}/employees/{employeeId}/calendar_days/{YYYY-MM-DD}
```

La fecha es la **local** de la persona, en su zona efectiva. Un documento por día. **Sin
documento, o con `shifts` vacío, el día está cerrado**: sin tareas no hay jornada. Un día que
se queda sin tareas se escribe vacío, no se borra: el espejo (§7) solo ve lo que existe, y un
borrado sería invisible para él. Nada en esta subcolección se borra nunca.

### 3.2 Forma

```ts
interface GeneratedDay {
  entityId: string;
  employeeId: string;
  date: string;                 // YYYY-MM-DD local
  timezone: string;             // la zona con la que se calculó la fecha
  shifts: Array<{
    start: {hour: number; minute: number};
    end: {hour: number; minute: number};
    taskId: string;
    title: string;              // para que el panel y la app etiqueten el turno sin otra lectura
    branchId: string;
  }>;
  taskIds: string[];            // los de shifts, para consultas
  generatedAt: Date;
  generatedBy: "tasks_trigger" | "mode_activation";
  frozen?: true;                // lo pone el trigger cuando la fecha ya pasó; no se regenera
}
```

`start` y `end` son hora y minuto del día, la misma forma que `Shift` en el calendario, para
que el fichaje, el planificador y el informe lo consuman sin convertir nada. Los turnos van
ordenados por inicio.

### 3.3 Cómo se construye

Una función pura en shared, `buildGeneratedDay(tasks, {employeeId, date, timezone})`, que
recibe las tareas de la persona que **empiezan** en esa fecha local y devuelve el documento,
con `shifts` vacío si no queda ningún turno. Reglas:

- Cuentan todas las tareas **menos `draft` y `cancelled`**. Una tarea rechazada o validada
  se hizo: su turno existió.
- Un turno por tarea, de `scheduledStartAt` a `dueAt`, en la zona dada.
- Una tarea sin `scheduledStartAt`, o cuyo inicio y vencimiento caen en fechas locales
  distintas, **no entra y se registra en el log**. D4 impide que exista; si llega, no se
  convierte en un turno roto.
- Dos tareas solapadas, si se cuelan por una carrera, se dejan las dos tal cual: el fichaje
  escoge el turno en el que cae la hora. No se funden (D2).

Es pura para que las pruebas unitarias la cubran sin Firestore y para que los dos escritores
(§4) no puedan divergir.

### 3.4 Lo que no se regenera

Un día cuya fecha local ya pasó **no se toca**: ni al mover una tarea pasada ni al cancelarla.
El documento queda como estaba y el trigger lo marca `frozen` la primera vez que lo encuentra
pasado. Hoy sí se regenera: las tareas se mueven durante el día.

## 4. Un solo escritor: el trigger, y la activación

### 4.1 El trigger

Un trigger de Firestore en `services/firebase_sdk`, `onDocumentWritten` sobre
`entities/{entityId}/tasks/{taskId}`. En cada escritura:

1. Calcula los pares (persona, fecha) afectados: las personas de `assignedEmployeeIds` antes
   y después, y las fechas locales de `scheduledStartAt` antes y después. Un cambio de fecha
   o de persona toca el día viejo y el nuevo.
2. Para cada persona resuelve su modo (cascada, cacheada en la ejecución). Si no está en el
   modo, nada.
3. Para cada par en el modo y con fecha hoy o futura: consulta las tareas de esa persona que
   empiezan en esa fecha local, llama a `buildGeneratedDay` y escribe el documento, vacío si
   no quedan turnos. Última escritura gana; cada ejecución parte de una consulta fresca, así
   que dos triggers seguidos sobre la misma persona convergen.

Cubre el panel, la app, el cuadrante, el sync de Rentman, las tareas de sistema y lo que
venga, sin que ninguno sepa que existe. Es lo que el README llama «nadie tiene que
acordarse».

**Dónde y cómo se despliega.** `firebase_sdk` ya tiene un trigger sobre ese mismo documento,
`onTaskPattern` (`src/patrones/onWriteTaskForPattern.ts`), que solo actúa al validar o
rechazar. Este es **otra función**, no una rama dentro de aquella: un fallo en los patrones no
puede dejar sin día a nadie, ni al revés. Se exporta en `src/index.ts` bajo la jerarquía
`apiV100.firebaseFirestoreTriggersCheckinBiz`, como las demás, y se despliega **solo ella**:

```bash
node services/firebase_sdk/scripts/desplegar.mjs --project dev-encodebiz --solo onTaskDay
```

El servicio comparte el codebase `default` con lo que sigue desplegado desde `encodeBiz-SAAS`,
y por eso nunca se despliega entero: se despliega por lista de nombres y lo que no está en la
lista no se toca (README del servicio, «Despliegue — reemplazar, no añadir»). Al ser una
función nueva, con nombre nuevo, no pisa nada del SaaS ni depende de que el resto del porte
esté vivo.

**Precondición, comprobada antes de escribir código:** el estado real de despliegue de
`firebase_sdk` no está anotado en ningún sitio; la última verificación escrita
(`eventos-webhooks/07_estado-verificado.md`, 2026-09-04) es anterior al porte. El primer paso
de la fase es `firebase functions:list --project dev-encodebiz` y dejar escrito qué corre.

**Alternativa considerada, para que conste.** `services/tasks` ya tiene un decorador que
espeja cada escritura a Postgres en la misma petición, `MirroredTaskRepository`, a mejor
esfuerzo y con un job de reparación por `updatedAt` (ADR-003 del dashboard operativo). El
mismo decorador podría regenerar el día: síncrono, sin depender de Firebase, y la prueba de QA
no tendría que esperar. Lo que no ve es una escritura que no pase por `tasks`, y hoy no se
conoce ninguna: Rentman, el cuadrante, el panel y la app entran todas por su API. El README
decidió el trigger (D3) con la premisa «venga de donde venga»; si esa premisa se da por
cubierta con «todo pasa por `tasks`», el decorador es menos pieza. Queda como pregunta
abierta en §11 hasta que se decida; el resto del TDR vale igual con cualquiera de los dos.

### 4.2 La activación

Al activar el modo (§2.2) hay que generar los días de las tareas que la persona ya tiene de
hoy en adelante. Lo hace el propio controlador de calendario en `checkinbiz`, con la misma
`buildGeneratedDay` y el mismo repositorio de días que el trigger (`GeneratedDaysRepository`
en shared, implementación Firestore). Son dos puntos de entrada con una sola función y un
solo repositorio; la regla del README, un solo escritor, está en que **ningún camino que
escribe tareas regenera nada**.

## 5. El resolutor del día efectivo

`ResolveEffectiveDayUseCase.execute` (`packages/shared/src/calendar/resolveEffectiveDay.usecase.ts`),
después de resolver la cascada y antes de elegir el día de la semana:

- Si `scheduleMode` efectivo es `tasks` **y** hay `employeeId`, pide al repositorio
  `getGeneratedDay(entityId, employeeId, dateLocal)`, método nuevo en `CalendarRepository`.
  - Con documento: `day = {shifts}` del documento, `isWorkingDay` según tenga turnos y no
    sea festivo, y `sources.schedule = "tasks"`.
  - Sin documento: `day = {disabled: true, shifts: []}`. El fichaje responde el
    `checklog/day_disabled` de siempre, y el texto de la app, en la fase 2, dirá «no tienes
    ninguna tarea hoy».
- Además devuelve `weeklySchedule` **sintetizada de la semana de esa fecha**: siete días
  generados, lunes a domingo, cada uno con sus turnos o apagado. Es lo que hace que
  `createChecklog` no cambie en nada para `weekPlan` y `plannedMinutes`: sigue sumando los
  turnos de `weeklySchedule`, solo que ahora son los de esa semana concreta. Una consulta
  por rango de siete fechas sobre la subcolección.
- Sin `employeeId` (ámbitos entidad y sucursal) el modo no aplica: sin persona no hay tareas,
  y la plantilla se devuelve como hoy.

Los festivos y las ausencias siguen mandando por encima: una tarea puesta en un festivo
genera turno, y el fichaje lo rechaza igual que rechaza un turno de plantilla en festivo.
En la fase 1 no se avisa al crear la tarea; queda anotado en §11.

En el fichaje (`createChecklog.controller.ts`):

- `ScheduleApplied.source` admite `"tasks"` (tipo en `CheckLog.ts`); el valor sale de
  `data.sources.schedule` como hoy.
- El turno elegido lleva `taskId` y `title`: `scheduleApplied.taskId` y
  `scheduleApplied.shifts[].taskId`, aditivos. Es el enlace que la fase 2 necesita para que
  Entrar sepa qué tarea arranca, y ya desde esta fase deja escrito en el registro a qué tarea
  correspondió cada fichaje.
- `buildOpenDefaultDay` no entra en juego en el modo: hay calendario, lo que no hay es
  turno, y eso es un día cerrado.

En Postgres, `PostgresCalendarRepository.getGeneratedDay` lee `dim_calendar_days` (§7). Es el
mismo caso de uso con otro repositorio, como todo el calendario; `BuildPlannedHours` y lo
que resuelva días desde analytics quedan en el modo sin tocarlos.

### 5.1 La disponibilidad

`ResolveAvailabilityUseCase` (`resolveAvailability.usecase.ts`) construye quién debía venir
con la plantilla semanal de cada par (persona, sucursal). `AvailabilityRepository` gana
`getGeneratedDays(entityId, employeeIds, from, to)` que devuelve un mapa persona → fecha →
turnos, en **una** consulta de grupo sobre `calendar_days` por `entityId` y rango de fechas
(índice en §8). Para las personas en el modo, `evaluate` y `executeDay` usan esos turnos en
vez de `shiftsOf(weekly[weekday])`; sin turnos ese día, `noShift`, que es lo que ya
significa «no tenía turno». Implementación Firestore en `checkinbiz` y Postgres en
`analytics`, las dos sobre el mismo caso de uso.

Limitación aceptada en esta fase: los turnos se enseñan en el par (persona, sucursal) de la
responsabilidad, aunque la tarea sea de otra sucursal. Lo que importa al dashboard, que la
persona estaba esperada y a qué hora, sale bien; qué sucursal la cuenta se afina cuando el
dashboard agrupe por tarea.

## 6. Las reglas de D4 en `tasks`

Una función en `services/tasks/src/interfaces/http/task/task.helpers.ts`:

```ts
validateTasksModeCompatibility(entityId, employeeIds, {scheduledStartAt, dueAt, excludeTaskId?})
  → Array<{employeeId, reason: "no_start" | "multi_day" | "overlap", withTaskId?}>
```

Para cada persona resuelve el modo (cascada, con caché por petición). Si está en el modo:

- sin `scheduledStartAt` → `no_start`;
- inicio y vencimiento en fechas locales distintas, en la zona efectiva de la persona →
  `multi_day`;
- cualquier otra tarea suya, no cancelada, que empiece ese día y cuyo intervalo se cruce con
  este → `overlap`, con `withTaskId`.

Y la respuesta, en todos los caminos:

```jsonc
400 {"code": "task/incompatible_with_tasks_mode", "error": "…", "details": {"conflicts": [...]}}
```

Dónde se llama, que son **todos** los sitios que escriben una tarea con personas:

| Camino | Cuándo |
|---|---|
| `createTask.controller.ts` | si hay `assignedEmployeeIds` |
| `updateTask.controller.ts` | si cambian `scheduledStartAt` o `dueAt`, contra los asignados actuales |
| `assignTaskWorkers.controller.ts` | contra las personas nuevas |
| `duplicateTask.controller.ts` | como crear |
| `createSystemTask.controller.ts` | como crear; es por donde entran Rentman y las tareas de sistema |

Rentman: `importCatalogue.ts` crea tareas de `plannedStart` a `plannedEnd` de la función del
proyecto, que normalmente son de varios días. Con una persona en el modo, esa creación
responde 400 y el import lo registra como error de esa tarea; el adaptador **no las parte**
(README, D4). Una persona con proyectos de Rentman no entra en el modo, y punto.

La comprobación de solape es contra una consulta, no contra un bloqueo: dos creaciones
simultáneas pueden colarse. Por eso el generador (§3.3) tolera el solape y no lo esconde.

## 7. El espejo a Postgres

No hay espejo en vivo del calendario: lo copia el job `dimensiones` de `analytics`
(`src/jobs/scheduler.ts`), cada hora al minuto 20 UTC, para cada entidad con actividad en los
últimos 30 días. `syncCalendars` (`src/application/SyncDimensions.ts`) lee
`calendar/config` de la entidad, de cada sucursal y de cada empleado, y hace `upsert` en
`dim_calendars`, clave `(scope, scope_id)`, con el horario en `weekly_schedule`. Se puede
lanzar a mano con `POST /api/analytics/dimensions/sync?entityId=…` (S2S), que es lo que usará
QA.

Lo que se añade, en ese mismo job:

- `dim_calendars` gana `schedule_mode` (`weekly`, `tasks` o nulo), que `upsertCalendar`
  copia del documento. Con eso `PostgresCalendarRepository` resuelve el modo con la misma
  cascada.
- Tabla nueva `dim_calendar_days`: `entity_id`, `employee_id`, `date`, `timezone`, `shifts`
  (jsonb), `task_ids` (text[]), `generated_at`, `frozen`, `synced_at`; clave `(employee_id,
  date)`, índice `(entity_id, date)`. En el bucle de empleados de `syncCalendars`, además de
  `calendar/config`, se lee `calendar_days` con `date >= hoy − 7` y se hace `upsert` de cada
  documento. Una ventana de siete días basta: un día pasado no se regenera (§3.4), así que lo
  que quedó espejado no cambia; y como nada se borra (§3.1), el espejo no necesita ver
  ausencias.
- `dim_sync_log` registra la dimensión `calendar_days` como registra las demás.

Migración: `migrations/037_horario_por_tareas.sql`, en la raíz del repositorio como todas, con
la columna y la tabla. **Se aplica a mano por SSH**, nunca el despliegue, y en producción
mirando el resultado.

El retraso del espejo es de hasta una hora. Vale para el dashboard, que ya vive con él para
el resto del calendario; lo que tiene que ser inmediato, el fichaje y la disponibilidad desde
`checkinbiz`, lee Firestore.

## 8. Reglas de Firestore e índices

**Reglas.** `calendar_days` entra en `soloServidor` de `firestore.rules`: lo escribe el
servidor y lo lee el servidor; la app y el panel lo reciben por `GET /calendar` y por la
disponibilidad. Desde el cliente, nada, ni leer: es el plan de una persona y, en parte,
registro.

**Índices.** Este repositorio no tiene `firestore.indexes.json` ni lo declara en
`firebase.json`; el fichero vive en `encodeBiz-SAAS/firestore.indexes.json` (114 índices) y
es el que poda en cada despliegue del SaaS. Lo que ya existe sobre `tasks` y sirve: nada para
la consulta del generador, que es «tareas de una persona que empiezan ese día» sin sucursal;
el índice de grupo `assignedEmployeeIds` + `branchId` + `scheduledStartAt` no la cubre. Hacen
falta dos:

| Colección | Ámbito | Campos | Para |
|---|---|---|---|
| `tasks` | colección | `assignedEmployeeIds` CONTAINS, `scheduledStartAt` ASC | generador, D4, activación |
| `calendar_days` | grupo de colecciones | `entityId` ASC, `date` ASC | disponibilidad por rango |

La lectura del espejo y la del resolutor van por la subcolección de una persona con un solo
campo (`date`), que no necesita índice compuesto.

Se crean con `gcloud firestore indexes composite create --project dev-encodebiz …`, que no
poda, **y** se añaden al fichero del SaaS en el mismo cambio, porque el siguiente
`firebase deploy` desde allí borraría lo que no esté en él (ya pasó: ver
«Índices Firestore: deriva»). En producción, lo mismo en el pase.

## 9. Inventario de cambios

| Sitio | Qué |
|---|---|
| `packages/shared/src/calendar/Calendar.ts` | `scheduleMode` en `BaseCalendar`; tipo `GeneratedDay` |
| `packages/shared/src/calendar/generatedDay.ts` (nuevo) | `buildGeneratedDay`, pura |
| `packages/shared/src/calendar/CalendarRepository.ts` | `getGeneratedDay`, `getGeneratedDaysInRange` |
| `packages/shared/src/calendar/GeneratedDaysRepository.ts` (nuevo) | escritura: `upsert`, `delete`, `deleteFrom(date)` |
| `packages/shared/src/calendar/FirestoreCalendarRepository.ts` | las lecturas nuevas y la implementación de escritura |
| `packages/shared/src/calendar/resolveEffectiveCalendar.usecase.ts` | resolver `scheduleMode` y su fuente |
| `packages/shared/src/calendar/resolveEffectiveDay.usecase.ts` | §5 |
| `packages/shared/src/calendar/resolveAvailability.usecase.ts` y `AvailabilityRepository.ts` | §5.1 |
| `packages/shared/src/checkbiz/entities/CheckLog.ts` | `source: "tasks"`, `taskId` en `ScheduleApplied` y en sus turnos |
| `services/checkinbiz/.../calendar/upsert{Entity,Branch,Employee}Calendar.controller.ts` | §2.2, con la comprobación y la generación inicial |
| `services/checkinbiz/.../calendar/getEffectiveCalendar.controller.ts` | §2.3 |
| `services/checkinbiz/.../checklog/createChecklog.controller.ts` | `taskId` en lo congelado |
| `services/checkinbiz/src/infrastructure/...AvailabilityRepository` | `getGeneratedDays` |
| `services/tasks/.../task.helpers.ts` y los cinco controladores de §6 | D4 |
| `services/firebase_sdk/src/calendario/onWriteTaskForDay.ts` (nuevo), exportado como `onTaskDay` | el trigger de §4.1 |
| `services/analytics/src/infrastructure/PostgresCalendarRepository.ts` y `PostgresAvailabilityRepository.ts` | lecturas desde `dim_calendar_days` |
| `services/analytics/src/application/SyncDimensions.ts`, `PostgresCalendarRepository.ts`, `migrations/037_horario_por_tareas.sql` | §7 |
| `firestore.rules`, `firestore.indexes.json` | §8 |

Nada de lo anterior cambia la forma de lo que ya existe: campos nuevos, valores nuevos en
uniones, métodos nuevos. Una persona sin el modo no nota el despliegue.

## 10. Pruebas

**Unitarias, en shared:** `buildGeneratedDay` (orden, estados que cuentan, zona horaria,
sin inicio y multi-día fuera, solape conservado, `null` sin turnos); el resolutor del día en
el modo (con documento, sin documento, semana sintetizada, sin `employeeId`); la
disponibilidad con días generados.

**QA, Playwright, `qa/tests/con-datos/54-horario-por-tareas.spec.ts`**, con la técnica de
`42-fichaje-jornada-partida`: se mueve la zona de la sucursal para que «ahora» sean las 12.
El trigger es eventual: las pruebas esperan al día generado con reintentos cortos, nunca lo
dan por escrito al volver la petición.

| Caso | Qué comprueba |
|---|---|
| HPT-01 | Activar el modo a una persona sin tareas: `GET /calendar` da día cerrado y la entrada responde `checklog/day_disabled` |
| HPT-02 | Crear una tarea hoy de 12:00 a 14:00: aparece como turno con `taskId` y `title`; la entrada entra y congela `source: "tasks"` y el `taskId` |
| HPT-03 | Mover la tarea a 15:00: el turno se mueve; una entrada a las 12 ya no entra |
| HPT-04 | Cancelar la tarea: el día desaparece |
| HPT-05 | Crear sin inicio, de dos días y solapada: los tres 400 con su `reason` |
| HPT-06 | Activar el modo con una tarea incompatible ya creada: 400 con la lista; nada escrito |
| HPT-07 | Quitar el modo: los días futuros se borran y la plantilla semanal vuelve a mandar |
| HPT-08 | Disponibilidad del día: la persona sale esperada con el turno de la tarea |
| HPT-09 | Una persona de la misma sucursal con `weekly` en su ficha sigue con la plantilla |

HPT-08 se comprueba por la ruta de disponibilidad de `checkinbiz`, que lee Firestore. El
espejo se prueba aparte, en el patrón de `45-espejo-y-programadas`: lanzar
`POST /api/analytics/dimensions/sync?entityId=…` y leer `dim_calendar_days`.

## 11. Fuera de esta fase, y lo abierto

Fuera: el gesto único (fase 2), las alarmas por tarea (fase 3), las dos líneas del informe
(fase 4), el cuadrante en el modo (fase 5), la app entera, y avisar al crear una tarea en
festivo o en ausencia de la persona, que hoy tampoco se avisa.

Abierto antes del código: **quién escribe el día**, el trigger de Firestore (D3, como está
decidido) o el decorador en `tasks` (§4.1, alternativa). Cambia dónde vive un fichero y si la
prueba espera o no; no cambia nada más de este TDR.

## 12. Criterio de éxito

Los nueve casos de QA en verde en staging; una persona en el modo que ficha deja en su
checklog `scheduleApplied.source = "tasks"` con el `taskId` del turno y un `scheduleDay` cuyos
minutos planificados son la suma de sus tareas; su día aparece en `dim_calendar_days` en
menos de un ciclo del espejo; y ninguna prueba de las que ya existen cambia de resultado.

# Catálogo de casos de uso — «Horario por tareas» (prefijo HPT)

> **Fase 1** (2026-10-15): el modo, los días generados y quién los escribe. Diseño en
> `DOCS/ingenieria/horario-por-tareas` (README y `tdr/TDR-001`). Lo que hay que esperar es lo
> que dice el TDR; se escribió antes que el código, así que aquí no hay «lo que hace hoy».
> Prueba: `qa/tests/con-datos/54-horario-por-tareas.spec.ts`.

Para quien está en el modo cada tarea es un turno de su día, y el día no sale de la
plantilla semanal sino de sus tareas, en un documento por fecha local que escribe un trigger
de Firebase. Es eventual: las pruebas lo esperan con reintentos, nunca lo dan por escrito al
volver la petición. Se mueve la sucursal, no el reloj: una zona en la que ahora son las 12.

## Convenciones

- El modo se pone con `PATCH /api/v1/checkinbiz/calendar` y `{scope: "employee", scheduleMode}`.
  `null` lo borra para volver a heredar. También en `branch` y `entity`.
- El día se lee con `GET /api/v1/checkinbiz/calendar?scope=employee&…`: `data.scheduleMode`,
  `data.sources.scheduleMode` y `effectiveDay` con `sources.schedule = "tasks"` y
  `day.shifts[].taskId`.
- El fichaje congela `metadata.scheduleApplied.source = "tasks"` y `taskId`.

## Casos

| Id | Actor | Qué | Esperado |
|---|---|---|---|
| HPT-01-01 | PROP, OP | Activar el modo a una persona sin tareas; leer su día; entrar | 200; `scheduleMode: "tasks"`, `sources.scheduleMode: "employee"`, `isWorkingDay: false`; entrada 400 `checklog/day_disabled` aunque la plantilla de la sucursal tenga el día abierto |
| HPT-02-01 | PROP, OP | Crear una tarea de hoy (de hace 10 min a dentro de 2 h) asignada; esperar el día; entrar | 201; el día trae el turno con `taskId` y `title`; entrada 201 con `scheduleApplied.source = "tasks"`, `taskId` de la tarea y `scheduleDay.plannedMinutes = 120` |
| HPT-08-01 | PROP | Disponibilidad del día de la sucursal | 200; la persona entre `available`, con `shifts[].taskId` de la tarea |
| HPT-03-01 | PROP, OP | Salir; mover la tarea a dentro de 3 h; esperar; entrar | 200; el turno se mueve; entrada 400 `checklog/out_of_schedule` |
| HPT-04-01 | PROP | Cancelar la tarea; esperar | 200; `isWorkingDay: false`, `day.shifts: []` (el día se escribe vacío, no se borra) |
| HPT-05-01 | PROP | Crear para la persona en el modo: sin inicio; de dos días; solapada con otra suya; contigua | 400 `task/incompatible_with_tasks_mode` con `details.conflicts[].reason` `no_start`, `multi_day`, `overlap` (+`withTaskId`); la contigua, que empieza cuando acaba la otra, 201 |
| HPT-09-01 | PROP | Leer el día de su compañera de sucursal con plantilla semanal | `scheduleMode: "weekly"`, `sources.schedule: "branch"`, `isWorkingDay: true`, turnos sin `taskId` |
| HPT-07-01 | PROP | Quitar el modo (`scheduleMode: null`); leer | 200; `scheduleMode: "weekly"`, `sources.schedule: "branch"`, el día de la plantilla |
| HPT-06-01 | PROP | Activar el modo a alguien con una tarea sin hora de inicio | 400 `calendar/tasks_mode_conflict` con `details.conflicts[]` `{employeeId, taskId, reason: "no_start"}`; el modo no se escribe |

## Fuera de la prueba automática, por ahora

- El espejo a Postgres (`dim_calendar_days`): se comprueba en el patrón de
  `45-espejo-y-programadas`, lanzando `POST /api/analytics/dimensions/sync?entityId=…`.
- Activar el modo en sucursal o entidad (misma comprobación, más gente).
- Las tareas que crea el sync de Rentman (`createSystemTask`): mismo 400 que HPT-05.

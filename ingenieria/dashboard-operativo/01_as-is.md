# 01 — Estado actual (As-Is)

Todo lo de abajo está verificado contra el código el 2026-10-10, y las cifras contra la base
de **desarrollo** (`encodebiz_staging`) ese mismo día. Producción no se ha medido: el hook la
bloquea y se mide en la fase 0-bis con un token real.

---

## 1. La portada del panel no dice nada de operativa

`encodebiz-front-saas/src/app/main/[entityId]/dashboard/page.tsx` pinta, en este orden:

1. `OnboardingCard` — la bienvenida.
2. `EmployeeTrendChart` — evolución mensual del número de empleados, sólo si la entidad tiene
   CheckBiz contratado (`entitySuscription`).
3. `ServiceList` — los servicios.
4. `DescriptionCard`.

El controlador (`page.controller.tsx`) sólo gestiona si abrir el onboarding. No hay ninguna
llamada a datos de jornada, tareas o coste.

## 2. Lo que sí habla de operativa está repartido, y ninguno responde «ahora»

### El Panel de CheckBiz es mensual y corta en ayer

`GET /api/analytics/panel/overview?period=YYYY-MM` (`services/analytics/src/application/BuildPanelOverview.ts`).
Pide un **mes**, no un rango, y si el mes está en curso lo corta en **ayer**, con comentario
explícito: «el día de hoy está a medias y arrastraría las medias hacia abajo, que es justo la
falsa alarma que queremos evitar». Es correcto para lo que es, y por eso **no se toca**: el hoy
es otra superficie.

Sí tiene series semanales (`evolution`, dos meses) de fiabilidad, efecto centro y carga. No son
los números operativos del día: son índices. El histórico que falta en la portada es el de los
mismos números del hoy, no éstos.

### Asistencia construye jornadas a partir de fichajes

`encodebiz-front-saas/src/app/main/[entityId]/checkinbiz/attendance/attendanceSummary.ts`,
`buildWorkSessionSummaries`. Convierte los fichajes de un rango en jornadas con estado
`pending | incident | on_break | working | completed`, pausas, minutos trabajados e
incidencias (`failed_log`, `missing_checkin`, `open_break`, `invalid_sequence`,
`multiple_checkouts`, `cross_branch_session`, `incomplete_workday`, `pending_validation`).
Ancla cada jornada en su checkin, resuelve el día en la zona del fichaje (`metadata.tz`) y
trata un `failed` como un intento que no ocurrió.

- **Vive sólo en el front.** No existe en `@encodebiz/shared` (comprobado: ningún
  `WorkSessionSummary` ni `buildWorkSessionSummaries` en `packages/shared/src`).
- **Quien no fichó no genera fila.** No puede decir «sin fichaje».
- Resuelve nombres con una lectura por fichaje (`enrichLogs`), el N+1 que disponibilidad retiró.

### Disponibilidad dice quién debería estar, sin mirar si vino

`GET /api/v1/checkinbiz/calendar/availability` y `/availability/day`, en el contenedor
`checkinbiz`, caso de uso `ResolveAvailabilityDayUseCase` en `shared`. Contrato en
[disponibilidad/03](../disponibilidad/03_contratos-api.md). Verificado en dev y en pantalla
en septiembre. Lee Firestore en cinco idas y vueltas fijas.

### Presencia cruza las dos cosas, para la app

[presencia/README](../presencia/README.md), estudio del 2026-10-09, sin planificar. Cruza el
desglose del día con los fichajes de la sucursal, en el servidor, sobre Firestore, para el
supervisor en el móvil. Su contrato define el vocabulario de presencia
(`no_log | working | on_break | finished | pending_validation | incomplete | other_branch`) que
este dashboard **reutiliza tal cual**. Su «Después» —«vista de gerente: cifras por centro para
toda la entidad»— es este trabajo. Su ADR-002 descartó `analytics` «porque es histórico sobre
Postgres»; con la restricción de este proyecto ese argumento se invierte
([ADR-002](./adr/ADR-002-el-dashboard-vive-en-analytics.md)).

## 3. Qué llega a Postgres y con qué frescura

Medido en dev el 2026-10-10 por SSH, sobre `encodebiz_staging`.

### Fichajes: en vivo, sin reintento

- **Cómo llegan:** trigger `onChecklogSync` (`encodeBiz-SAAS/functions/src/services-saas/checkinbiz/firebase-firestore-trigger/onChecklogSync.ts`),
  `onDocumentWritten` sobre `/entities/{eid}/checklogs/{chid}`, que llama a
  `POST /api/sync/checklogs` del contenedor con timeout de 7 s. Ignora borrados. **Si falla,
  escribe un `console.error` y nada más**: no hay cola, no hay reintento.
- **Dónde caen:** `checklogs_raw` (`migrations/001_init.sql`), upsert por `id`. Columnas que
  importan aquí: `type`, `status`, `closed`, `checkin_ref`, `timestamp`, `real_date_market`,
  `adjusted_timestamp`, `employee_price`, `schedule_applied` (JSONB con `start`, `end`,
  `toleranceMinutes`, `shifts`, `scheduleDay` con `plannedMinutes` y `breakMinutes`), `etz`,
  `employee_responsibility`, `metadata_raw` (con `tz`). Índice `idx_checklogs_entity_branch_ts
  (entity_id, branch_id, timestamp DESC)`.
- **Frescura en dev:**

| Medida | Valor |
|---|---|
| Filas con `timestamp` en los últimos 7 días | 2.416 |
| Último `timestamp` | 2026-10-10 17:41 UTC |
| Último `updated_at` | 2026-10-10 18:00 UTC |
| `sync_log` últimos 7 días | 4.597 `success`, 0 `failed` |

El cero de fallos en dev no dice nada de producción: el fallo que preocupa es el de red entre
GCP y OVH bajo carga, que dev no tiene.

### Dimensiones: existen, nadie las refresca

- `dim_branches` (nombre, estado, `tz`, horario, geo), `dim_employees` (nombre, puesto,
  estado, `branch_ids`), `dim_calendars` (los tres niveles con horario semanal, festivos,
  ausencias y `overrides_disabled`). Migraciones `006`, `007`, `008`.
- Las puebla `SyncDimensions` (`services/analytics/src/application/SyncDimensions.ts`) desde
  `POST /api/analytics/dimensions/sync` (S2S). El comentario del código dice «corre por cron
  o bajo demanda». **No hay cron**: `analytics` no tiene planificador (`server.ts` sólo
  escucha), y en `docker-compose.staging.yml` no hay ningún servicio que lo llame. La QA lo
  deja escrito (`qa/tests/con-datos/45-espejo-y-programadas.spec.ts`, caso ANA-05-01).
- **Frescura en dev:** las seis dimensiones se refrescaron el 2026-10-10 a las 10:01 UTC,
  todas en el mismo segundo. Es la QA, no un programador. `dim_employees` tiene 2.643 filas,
  `dim_branches` 235, `dim_calendars` 59 de entidad, 58 de sucursal y 58 de empleado.
- `PostgresCalendarRepository` (`services/analytics/src/infrastructure/`) implementa el
  **mismo** contrato que usa `checkinbiz` contra Firestore, así que `ResolveEffectiveDayUseCase`
  resuelve la cascada sobre Postgres sin reimplementar nada. `BuildPlannedHours` ya lo usa.
  Verificado en producción en julio: el plan coincide exactamente con el `scheduleApplied` de
  los fichajes.
- Inventario ya pagó este problema: hasta el 2026-10-08 sus informes salían sin nombres y con
  coste 0 porque `dim_items` sólo se rellenaba a mano. Lo resolvió escribiendo la dimensión en
  la propia petición (`services/inventory/src/infrastructure/MirroredMasters.ts`).

### Tareas: no están

- Sólo `task_ratings_raw` (valoraciones), empujadas desde Firebase como los fichajes.
- El servicio `tasks` no toca Postgres (ningún `pool` en `services/tasks/src`).
- Sí **emite un evento por cada escritura** (`services/tasks/src/events/task.ts`:
  `task.created`, `task.updated`, `task.status_changed`, `task.deleted`) hacia los webhooks
  de clientes. Eso deja `webhook_delivery`, no una tabla de tareas.
- El cruce de ejes del Panel lo dice en su respuesta: «Tareas va como `sin_evidencia` para
  todo el mundo».
- **Quién escribe tareas hoy:** todo pasa por el servicio `tasks` por HTTP. El panel y la app
  por `/api/v1/tasks`; Rentman (`services/rentman/src/infrastructure/HttpTasksClient.ts`) y
  los cuadrantes de Merlin (`services/merlin/src/soporte/cuadrantes/application/aplicar.ts`)
  por `/api/v1/tasks/system`. El único repositorio de tareas del contenedor fuera de `tasks`
  es el de `inventory`, que escribe **actividad** (`item_consumed`), no la tarea. El
  `taskStartNotificationWorker` (Firebase, y su porte en `firebase_sdk`) sólo sella
  `scheduledStartNotifiedAt`. **Queda por confirmar en producción** que la Cloud Function
  `tasksHandler`, que sigue exportada en el SaaS, no recibe tráfico (fase 0-bis).
- El estado de cumplimiento `timeComplianceStatus` se escribe **sólo** en
  `updateTaskStatus.controller.ts`: al iniciar (`on_time` u `overdue` según `dueAt`) y al
  completar (`computeCompletionStatus`). Ningún planificador lo revisa. Una tarea asignada cuya
  fecha ya pasó sigue en `not_started` hasta que alguien la toque.

### Inventario: en vivo, con coste

- `item_movements_raw` (`migrations/023_inventario.sql`) lo escribe `inventory` en la
  petición, tras confirmar Firestore, a mejor esfuerzo y con job `remirror`
  ([inventario TDR-004](../inventario/tdr/TDR-004-espejo-postgres-e-informes.md)). Trae
  `type`, `item_id`, `task_id`, `branch_id`, `quantity`, `employee_id`, `occurred_at`.
- `dim_items.unit_cost` da el coste unitario. Lo escribe `inventory` al crear o cambiar el
  artículo, además del sync general.
- **Frescura en dev:** 97 movimientos, el último a las 18:23 UTC del 2026-10-10.

### Tarifa por hora: en cada fichaje

`employee_price` en `checklogs_raw` es la tarifa por hora de la responsabilidad en el momento
del fichaje. Verificado en producción en julio por `BuildOperatingCost`: cobertura de 1.023
sobre 1.036 fichajes; los puestos españoles la llevan derivada del salario mensual y los
americanos directa. **La tarifa de quien aún no ha fichado no está en Postgres**: vive en
`employee_responsibilities`, que `dim_employees` no espeja (sólo `job_title`).

### Partes diarios: existen, y son otra cosa

`employee_daily_reports` lo escribe `reports` (`BuildEmployeeDailyReports.ts`) con un cron
horario que construye cada centro a las 02:xx de **su** zona para el día anterior
(`DailyReportCron.ts`). Es el registro de jornada legal por persona (ciclos, minutos netos,
descansos). No tiene «previstos», ni tareas, ni coste. **Su mecanismo de cron por zona es el
que se copia** para el cierre diario de este dashboard; su tabla no se reutiliza.

## 4. La puerta del panel

`services/analytics/src/app.ts` monta `/api/analytics/panel` con `cors()`,
`requireFirebaseAuth` y `requireEntityAccess` (`core/entityAccess.ts`): `user_entity_roles/{uid}_{entityId}`
con rol `owner` o `admin`. Sólo lectura por contrato: «aquí solo pueden colgar rutas de LECTURA».
El front llega por el proxy `checkinbiz_panel_overview` (`serverBackendProxy.ts`), variable
`NEXT_BACKEND_URI_CHECKINBIZ_PANEL_OVERVIEW`, con la query reenviada tal cual.

## 5. Lo que condiciona el diseño

- **Sin planificador en `analytics` ni en `sync`.** El cron de dimensiones, la conciliación y
  el cierre diario necesitan uno. `reports` usa `node-cron`; al implementar se optó por `setInterval`, como `tasks` e `inventory`.
- **El espejo de fichajes puede tener huecos** y nadie lo sabe. Un dashboard que dice «4 de
  10» sobre un espejo con huecos es el peor fallo posible: no avisa, miente.
- **`dim_calendars` no tiene historia.** Cada sync la pisa. Aplicarla a días pasados reescribe
  el pasado (limitación ya escrita en `BuildPlannedHours`). Es la razón del cierre diario.
- **`incomplete_workday` sin semántica cerrada.** El 31 % de los fichajes de julio en
  producción. Se enseña, no se juzga.
- **Zona horaria por centro.** `dim_branches.tz` existe; los fichajes llevan `metadata_raw.tz`
  y `etz`. El día es el del centro; la jornada es la del día de su checkin.
- **Sin turno por día y sucursal.** Sobreconteo heredado.

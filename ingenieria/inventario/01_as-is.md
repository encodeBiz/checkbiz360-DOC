# 01 — Estado actual (As-Is)

## No hay inventario

No existe ninguna colección, tabla, servicio ni endpoint de inventario en la plataforma.
Comprobado el 2026-09-28 sobre `encodebiz-api` y `DOCS/ingenieria`: la única aparición del
concepto «almacén» es `rentman_warehouse_tasks` en la migración `011`, que es del conector de
Rentman y no tiene nada que ver con esto.

Este documento no describe un sistema que haya que migrar. Describe **lo que ya existe y el
módulo va a reutilizar de verdad** — y, en dos sitios, lo que parecía reutilizable y no lo es.
La primera versión de este documento afirmó tres reutilizaciones sin comprobarlas; la revisión
del mismo día las tumbó, y aquí quedan corregidas.

## Lo que se reutiliza

### La tarea, que ya es casi todo

`packages/shared/src/checkbiz/entities/Task.ts` ya trae, sin tocar nada:

- `entityId`, `branchId` y `assignedEmployeeIds` — a quién y a qué centro se imputa el gasto.
- `workSite` (`TaskWorkSite extends Geofence`) — **dónde** se hizo el trabajo. De aquí sale la
  posición de un operable sin que nadie la mantenga a mano.
- `TaskActivity` con `actorId`, `actorRole` y `employeeId` **separados** — el precedente exacto
  de «quien lo registra no es siempre quien lo gastó» (ver [ADR-004](./adr/ADR-004-asignar-no-es-consumir.md)).
- `TaskResource` con `uploadedBy` y `employeeId`, por la misma razón.
- `TaskValidation` — el momento en que una persona cierra la tarea. Es donde encaja la
  conciliación del material sobrante sin inventar un flujo nuevo.
- Contadores en el documento y detalle en subcolección (`pausedMs`/`pauseCount` + `pauses`) —
  el idioma que sigue el saldo respecto del libro de movimientos.

### El control de estado de la tarea

Está en un solo controlador, `updateTaskStatus.controller.ts`, con una máquina de estados
explícita (`ALLOWED_FROM`) y estados sellados —`validated`, `rejected`, `cancelled`— de los que
solo se sale reabriendo. Validar y rechazar van por endpoints propios. Nada automático toca
`status` en este repo.

Las señales que existen, y las únicas que este módulo puede escuchar:

- `task.status_changed` con `status`, `previous_status` y `changed_by` — **solo si el estado
  cambió de verdad**. El completado parcial (`completionPolicy: all_assigned_workers`) deja la
  tarea `in_progress` y no emite nada.
- `task.validated` y `task.rejected`, con evento propio.

No existen `task.completed` ni `task.cancelled`: son `status_changed` con ese `status`.

### La sucursal y el empleado

`Branch` y `Employee` dan el eje multisucursal. `EmployeeResponsibility`, con su
`scope: {entityId, branchId?, teamId?}`, es el precedente de relación N:M que el almacén imita.
El empleado además denormaliza `branchId: string[]` para poder consultarse — es lo que hace el
almacén con sus `branchIds`.

### La disponibilidad — lo que sí y lo que no

`packages/shared/src/calendar/` resuelve la disponibilidad con cascada entidad → sucursal →
empleado. **Eso sí se reutiliza**, para los huecos de no disponibilidad de un operable: avería,
revisión, veterinario, descanso son la misma cascada de festivos y ausencias que ya tienen las
personas.

Lo que **no** se reutiliza es el `AvailabilityBoard`. Es un mapa de calor: una fila por grupo
(`kind: "branch" | "unassigned"`, unión cerrada) y una celda que es un contador
(`{date, available, closed}`). El tablero de operables necesita una fila por ejemplar y una
celda con la tarea y el sitio: es una **agenda**, otro contrato y otro componente en el panel.
Ver [TDR-003 §4](./tdr/TDR-003-operables-agenda-y-choque.md).

### La monetización

`entities/{entityId}/subscriptions/{serviceId}` + `service/{serviceId}/plan/{planId}`, con el
patrón de lectura en `packages/shared/src/checkbiz/plan/subscriptionLimits.ts`.

La suscripción **la escribe `billing`** por entidad y servicio, en este repo. Lo que hay que
tocar para que exista `inventory` es corto: el tipo `SERVICES` en
`packages/shared/src/platform/Service.ts` (hoy `"passinbiz" | "checkinbiz"`), la lista
`OUR_SERVICES` de `StripeWebhookHandler.ts` en `billing`, los planes en Firestore y el precio en
Stripe. `onActivateCheckbiz` ya está portado a `services/firebase_sdk/src/altas/` y lo único que
hace es crear la sucursal inicial: **no hay ningún trigger que portar** para inventario.

### Los eventos — lo que son y lo que no

`packages/shared/src/events/publish.ts` es un **sistema de webhooks salientes**, no un bus
entre servicios: resuelve los endpoints suscritos del cliente (`endpoints.findSubscribed`) y,
si no hay ninguno, **vuelve sin encolar nada**. Un servicio interno no puede «escuchar» un
evento por el mero hecho de que se emita.

Lo que sí ofrece, y este módulo aprovecha, es la cola `webhook_delivery` con firma, reintentos
y rescate. La forma de engancharse es un **suscriptor interno** en la resolución de
suscriptores ([TDR-002 §6](./tdr/TDR-002-saldos-movimientos-y-conciliacion.md)).

### El espejo a Postgres — cómo funciona de verdad

`services/sync` es un **receptor pasivo**: recibe por HTTP lo que los triggers de
`firebase_sdk` le empujan (`AnalyticsServerClient` → `/api/sync/checklogs`,
`/api/sync/task-ratings`), con un timeout corto y un `catch` que solo escribe en el log. Las
`dim_*` ni siquiera van por ahí: las puebla `SyncDimensions` en `analytics`, por cron o bajo
demanda, con registro en `dim_sync_log`.

Por eso el espejo de este módulo **no usa `sync`**: `inventory` escribe en Postgres en la misma
petición y reintenta con un job propio ([TDR-004](./tdr/TDR-004-espejo-postgres-e-informes.md)).
Las tres dimensiones nuevas entran en `SyncDimensions` como una más.

### La app

Verificado en el repo de la app el 2026-09-28: tiene `cloud_firestore` y `firebase_auth`, pero
**solo lee cuatro colecciones y no tiene ni una escritura directa a Firestore**. Todo lo que
escribe —tareas, fichaje, documentos, el `criticalHandler`— va por HTTP con Dio. Su caché local
es un `SharedPreferences` con treinta minutos de caducidad, no una cola de escritura. Y las
tareas, de las que cuelga la pantalla de material, se leen por HTTP.

Esto fija el camino: **todo por API, como el resto**. El trabajo sin conexión es fase posterior
([06 §D3](./06_decisiones-abiertas.md)).

## Lo que no existe y hay que crear

- Catálogo de artículos, almacenes y ejemplares.
- Existencias y libro de movimientos.
- Reserva de operables, detección de choque y el tablero (contrato y componente nuevos).
- El servicio `inventory`, su bloque en compose y nginx, y su endpoint interno para las
  entregas de eventos de tarea.
- `inventory` en `SERVICES` y en `OUR_SERVICES` de `billing`, sus planes y su precio.

## Limitaciones del entorno que condicionan el diseño

1. **La app no escribe en Firestore ni tiene cola sin conexión.** Todo va por API. El offline
   se aplaza y se boceta en 06 §D3 para no discutirlo desde cero.
2. **`sync` no tiene reintentos.** Si una pasada falla, esos registros no vuelven a intentarse
   y el espejo queda incompleto en silencio. **No afecta a este módulo** porque su espejo no
   pasa por ahí, pero se deja constancia: afecta a checklogs y valoraciones.
3. **Un solo servidor.** Los contenedores se hablan por la red de Docker y Postgres no está
   expuesto fuera de ella (sin `ports:` en el compose).
4. **No hay respaldo programado de Postgres en el repo.** Lo único que consta es un `pg_dump`
   comentado en `docker-compose.yml`. Hay que confirmarlo antes de producción
   ([06 §D4](./06_decisiones-abiertas.md)).

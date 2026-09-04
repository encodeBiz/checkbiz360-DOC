# 03 — Catálogo de eventos y mapa de lanzadores

Este documento tiene dos mitades. La primera dice **qué eventos existen**. La segunda, que es
la que cuesta trabajo, dice **desde qué línea de código sale cada uno**.

---

## 1. Convención

`<dominio>.<acción_en_pasado>` — dos segmentos, minúsculas, `snake_case` en la acción.
Continúa la forma de los dos eventos que ya existen (`attendance.clock_in`).

Dominios: `attendance`, `workday`, `issue`, `task`, `document`, `employee`, `branch`,
`schedule`, `calendar`, `report`, `alert`, `service`, `invoice`, `endpoint`.

Reglas:

- La acción se nombra por **lo que pasó**, no por la operación HTTP. `document.acknowledged`,
  no `document.ack_posted`.
- Un evento por hecho de negocio, no por escritura. Cambiar tres campos de una tarea es
  `task.updated`, una vez.
- Los estados que importan tienen evento propio aunque sean un `PATCH` más:
  `task.status_changed` no se disuelve dentro de `task.updated`.
- Nada de eventos `.failed` de infraestructura. Un fallo interno es un log, no un webhook. Las
  excepciones son las que el cliente necesita accionar: `attendance.clock_rejected`.

## 2. Catálogo

### attendance — fichaje

| Evento | Cuándo |
|---|---|
| `attendance.clock_in` | Entrada válida registrada |
| `attendance.clock_out` | Salida válida registrada |
| `attendance.break_start` | Inicio de descanso (`restin`) |
| `attendance.break_end` | Fin de descanso (`restout`) |
| `attendance.clock_rejected` | El fichaje se rechaza en el acto. `reason`: fuera de geocerca, tipo duplicado, sin turno |
| `attendance.clock_flagged` | El fichaje se acepta pero se marca sospechoso (`isSuspect`) |
| `attendance.manual_requested` | Se solicita una jornada manual desde el back office |
| `attendance.correction_requested` | Se propone una corrección; el fichaje queda en `pending-employee-validation` |
| `attendance.correction_accepted` | El empleado confirma la corrección desde la app |
| `attendance.correction_rejected` | El empleado la rechaza. Lleva `rejectionReason` |

`clock_rejected` y `clock_flagged` son distintos a propósito: el primero es un fichaje que no
llega a existir; el segundo existe y cuenta, pero queda señalado. Los dos se deciden en el alta
(`CreateChecklog.ts` decide `isSuspect` ahí mismo), no después.

### workday — jornada

| Evento | Cuándo |
|---|---|
| `workday.closed` | Jornada cerrada, con horas netas ya calculadas y el descanso del centro descontado |
| `workday.incomplete` | La jornada terminó sin salida y hubo que cerrarla |

Son los que un integrador quiere de verdad: `workday.closed` es literalmente lo que el add-on
de Rentman consume hoy por sondeo cada 15 minutos.

### issue — incidencias

| Evento | Cuándo |
|---|---|
| `issue.opened` | Se abre una incidencia. Lleva `type` y `toRole` |
| `issue.responded` | Alguien responde (incrementa `responseCount`) |
| `issue.resolved` | Pasa a `resolved` |
| `issue.rejected` | Pasa a `rejected` |

### task — tareas

`task.created`, `task.updated`, `task.status_changed`, `task.assigned`, `task.unassigned`,
`task.validated`, `task.rejected`, `task.note_added`, `task.resource_uploaded`,
`task.worker_rated`.

### document — documentos

`document.created`, `document.updated`, `document.archived`, `document.acknowledged`.

`document.acknowledged` es el que tiene valor legal: es la constancia de que el trabajador
recibió y aceptó el documento.

### employee — empleados

`employee.created`, `employee.updated`, `employee.deleted`, `employee.device_added`,
`employee.responsibility_changed`.

### branch — centros de trabajo

`branch.created`, `branch.updated`, `branch.deleted`, `branch.geofence_changed`.

La geocerca va aparte porque cambiarla cambia qué fichajes se aceptarán mañana: es un hecho de
negocio, no un campo más.

### schedule / calendar — horarios

`schedule.published`, `schedule.assigned`, `schedule.changed`, `calendar.preset_saved`,
`calendar.holiday_changed`.

### Transversales

| Evento | Cuándo |
|---|---|
| `report.generated` | Informe legal generado y disponible |
| `alert.raised` | Merlin o la heurística levantan un aviso operativo |
| `service.activated` / `service.deactivated` | Alta o baja de un servicio contratado |
| `addon.connected` / `addon.disconnected` | Un add-on se conecta o se retira (Rentman el primero) |
| `invoice.issued` / `invoice.payment_failed` | Facturación |
| `endpoint.test` | Evento de prueba disparado a mano desde el panel |

`endpoint.test` no es de negocio: existe para que quien integra valide firma y conectividad sin
esperar a que alguien fiche. Es lo primero que se echa de menos al integrar.

`alert.raised` es el único que publica conocimiento en vez de datos, y probablemente el que más
valor tenga para el cliente.

---

## 3. Mapa de lanzadores

Esta es la parte trabajosa. La regla que la ordena: **emite donde vive la escritura, no donde
vive el dato**.

**Revisado el 2026-09-04 contra el código y contra el tráfico real de desarrollo**, no deducido
del diseño. Entre agosto y septiembre se portaron al contenedor los fichajes, el calendario, las
tareas y los documentos, así que buena parte de la segunda tabla que llevaba este mapa ya no
era cierta: lo que estaba «todavía en Firebase» hoy entra por nginx al contenedor.

Cómo se comprobó, para poder repetirlo: `firebase functions:list --project dev-encodebiz` dice
qué sigue vivo del lado de Firebase; las rutas de escritura de cada servicio dicen qué existe en
el contenedor; y el log de nginx de desarrollo de las últimas 72 h dice por dónde entra el
tráfico de verdad — que es lo único que distingue una ruta escrita de una ruta usada.

### 3.1 La escritura ya está en el contenedor — 32 eventos, **lanzador cableado**

| Eventos | Dónde va la llamada | Tráfico en 72 h |
|---|---|---|
| `attendance.clock_in`, `clock_out`, `break_start`, `break_end`, `clock_rejected`, `clock_flagged` | `services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts`. El rechazo ya existe como registro: la valla escribe el fichaje con `status: "failed"` y `failedCode: "checklog/out_of_radius"` antes de devolver el 400. `isSuspect` se decide en `CreateChecklog.ts` | 20 fichajes |
| `attendance.correction_requested`, `correction_accepted`, `correction_rejected` | `updateChecklog.controller.ts` — los tres caminos ya están separados ahí | — |
| `attendance.manual_requested` | `requestManualChecklog.controller.ts` | — |
| `workday.closed` | El mismo `createChecklog.controller.ts`: el checkout marca `closed: true` sobre la entrada asociada | 20 fichajes |
| `task.*` — los diez | `services/tasks/src/interfaces/http/task/taskRouter.ts`, un controlador por acción, correspondencia uno a uno | 7 PATCH |
| `document.created`, `updated`, `archived`, `acknowledged` | `services/documents/src/interfaces/http/document/documentRouter.ts` (`POST /`, `PATCH /:id`, `DELETE /:id`, `POST /:id/ack`) | 1 POST |
| `calendar.preset_saved`, `calendar.holiday_changed` | `services/checkinbiz/src/interfaces/http/calendar/calendar.router.ts` | 36 escrituras |
| `report.generated` | `services/reports/src/interfaces/report.router.ts` (`POST /generate`) | — |
| `invoice.issued`, `invoice.payment_failed` | `services/billing/src/application/StripeWebhookHandler.ts` | 21 llamadas |
| `addon.connected`, `addon.disconnected` | `services/rentman/src/interfaces/http/rentman.router.ts` (`/connect`, `/disconnect`) | — |

Un guion en la última columna no significa que la ruta no se use: significa que en esas 72 h
nadie generó un informe ni conectó un add-on en desarrollo. La ruta existe y es la única.

**Los 32 están cableados** desde `feat/eventos-oleada-2` (2026-09-04). Cada servicio trae su
mapeador en `src/events/`, y ninguna llamada se espera: `emit()` de `@encodebiz/shared`
devuelve `void` justamente para que no se pueda poner un `await` delante. Falta desplegarlos y
borrar `onChecklogWebhook` — ver [07 §3.1](./07_estado-verificado.md).

### 3.2 Camino duplicado — 7 eventos, hay que decidir antes de cablear

Existen las dos implementaciones a la vez: la ruta del contenedor y la función de Firebase, que
sigue desplegada. Poner el lanzador en el lado que el panel no usa emite para la mitad del
tráfico, o para nada — y es un fallo que no se ve, porque no rompe nada.

| Eventos | Contenedor | Firebase, aún desplegado |
|---|---|---|
| `employee.created`, `updated`, `deleted`, `device_added` | `checkinbiz/.../employee/employee.router.ts` (`POST /`, `PATCH /:employeeId`, `DELETE /:employeeId`, `POST /:employeeId/email`) | `createEmployee`, `updateEmployee`, `deleteEmployee`, `addDeviceEmployee` |
| `schedule.published`, `schedule.assigned`, `schedule.changed` | El horario semanal se edita por `calendar.router.ts` | `employeePlanifierWorker`, `planifierNotificationWorker` — `schedule.published` es suyo |

En 72 h de desarrollo no pasó ni una escritura de empleado, así que el tráfico no desempata.
Se resuelve mirando qué URL llama el panel, no eligiendo.

### 3.3 La escritura sigue en Firebase — 12 eventos

Van por `services/firebase_sdk` con la ruta S2S (`POST /api/v1/events/s2s/publish`, API key), o
esperan a que se porte su CRUD. Ver [ADR-006](./adr/ADR-006-firebase-sdk-residuo-transitorio.md).

| Eventos | Dónde |
|---|---|
| `workday.incomplete`, `issue.opened` | `scheduleCheckbiz-sanitizerChecklog`. Cuando un check-in vence sin checkout, fabrica el checkout `incomplete_workday` y crea la incidencia acto seguido |
| `issue.responded`, `issue.resolved`, `issue.rejected` | `onIssuesResponse` y escrituras directas sobre `/issues/{id}` desde el back office y la app |
| `employee.responsibility_changed` | `responsibilitiesHandler` |
| `service.activated`, `service.deactivated` | `onActivateCheckbiz` y el flujo de suscripciones |
| `branch.created`, `updated`, `deleted`, `geofence_changed` | `createBranch`, `updateBranch`, `deleteBranch` — el CRUD de centros sigue entero en Firebase; el contenedor solo lee |

### 3.4 Sin sitio donde emitir — 1 evento

`alert.raised`. Merlin interpreta y cachea análisis; no tiene hoy ningún concepto de alerta en
el código. No es un lanzador pendiente de cablear: es un evento declarado sin hecho de negocio
detrás todavía. Mientras siga así, el panel lo ofrece como suscribible y nadie lo recibirá
nunca — decidir si se implementa o se retira del catálogo.

### 3.5 El recuento, para no perderlo de vista

53 eventos diseñados: 32 cableados, 7 esperando a que se aclare el camino duplicado, 12
esperando a su CRUD, 1 sin emisor posible, y `endpoint.test`, que ya funcionaba.

**El catálogo solo declara los 33 que emiten.** Los otros veinte están comentados en su sitio
dentro de `packages/shared/src/events/catalogue.ts`, cada uno con lo que hay que portar antes
de descomentarlo. La razón es la del panel: un evento ofrecido que nunca llega no se distingue,
desde fuera, de una integración rota — y `isValidSubscription` rechaza además suscribirse a una
familia que no emite (`issue.*` da error, `attendance.*` no). Se descomenta cuando su lanzador
exista, no antes.

### 3.6 `Issue.type` — resuelto el 2026-08-26

El sanitizador escribía `type: "journey_registration"` en snake_case, mientras que el
contenedor y el front lo declaran y lo esperan en camelCase. Era el único sitio que lo
escribía así, con la consecuencia de que las únicas incidencias que la plataforma genera sola
eran también las únicas que el front no sabía etiquetar.

**Queda `journeyRegistration`.** Corregido en el SaaS y desplegado en desarrollo.

Lo que ese cambio no toca: las incidencias **ya creadas** conservan el valor viejo. Antes de
publicar `issue.opened` hacia fuera hay que convertirlas, o el consumidor verá dos tipos para
el mismo hecho.

### 3.7 Por qué el trigger encoge

Cada fila de §3.3 es temporal, y la revisión del 2026-09-04 lo demuestra mejor que cualquier
argumento: los fichajes, el calendario, las tareas y los documentos estaban ahí en agosto y hoy
están en §3.1. Conforme el CRUD de centros, horarios y jornada se
porte al contenedor, su lanzador se mueve al caso de uso y el trigger correspondiente se borra.
`services/firebase_sdk` es el sitio donde esperan mientras tanto — ver
[ADR-006](./adr/ADR-006-firebase-sdk-residuo-transitorio.md).

---

## 4. Retirada de passinbiz

Todo el catálogo `pass.*` / `credential.*` / `validation.*` desaparece. Cuatro sitios:

1. Borrar `services-saas/passinbiz/webhook-events.ts`.
2. Quitar su import de `functions/src/index.ts` (el registro es por efecto de import).
3. Quitar las llamadas de `ValidatePass.ts` y `createPassOnDemand.controller.ts`.
4. **El que no se ve:** `core/firebase-entry-schedule/mailer/email-worker.ts` llama a
   `publishEvent` directamente con `pass.sent` / `credential.sent` / `.failed`. Si se borra el
   catálogo sin tocar esto, `publishEvent` lanza en cada email enviado.

passinbiz está descontinuado, así que no hay que comprobar suscriptores vivos.

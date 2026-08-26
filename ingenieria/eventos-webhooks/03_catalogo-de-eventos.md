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

### Ya escriben en el contenedor — el lanzador va en el caso de uso

| Eventos | Dónde va la llamada |
|---|---|
| `attendance.clock_in/out`, `break_start/end`, `clock_rejected`, `clock_flagged` | `services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts` y su caso de uso `CreateChecklog.ts` — `isSuspect` se decide en `CreateChecklog.ts:74` |
| `workday.closed` | El mismo controlador: un `checkout` cierra el ciclo marcando `closed: true` sobre el check-in (`createChecklog.controller.ts:419`) |
| `attendance.correction_requested/accepted/rejected` | `services/checkinbiz/src/interfaces/http/checklog/updateChecklog.controller.ts` — los tres caminos ya están separados ahí: la transición a `pending-employee-validation`, la confirmación del empleado y el rechazo con `rejectionReason` |
| `attendance.manual_requested` | `services/checkinbiz/src/interfaces/http/checklog/requestManualChecklog.controller.ts` |
| `task.*` (los diez) | `services/tasks/src/interfaces/http/task/*.controller.ts` — hay un controlador por acción, la correspondencia es uno a uno |
| `document.*` (los cuatro) | `services/documents/src/interfaces/http/document/*.controller.ts` — ídem |
| `employee.created/updated/deleted/device_added` | `services/checkinbiz/src/interfaces/http/employee/employee.router.ts` (`POST /`, `PATCH /:employeeId`, `DELETE /:employeeId`, `POST /:employeeId/email`) |
| `report.generated` | `services/reports` |
| `invoice.*` | `services/billing` |
| `addon.connected/disconnected` | `services/rentman/src/interfaces/http/rentman.router.ts` (`/connect`, `/disconnect`) |
| `alert.raised` | `services/merlin` |

### Todavía escriben en Firebase — el lanzador va, de momento, en un trigger

| Eventos | Dónde |
|---|---|
| `branch.created/updated/deleted`, `branch.geofence_changed` | El CRUD sigue en `firebase-checkinbiz-http/create-branch.ts`, `update-branch.ts`, `delete-branch.ts`. El contenedor solo lee (`services/backoffice/.../branches.router.ts`) |
| `schedule.*`, `calendar.*` | `firebase-checkinbiz-http/calendar.ts` (`savePreset`, borrado) y los workers del planificador. El contenedor solo sirve `getEffectiveCalendar` |
| `workday.incomplete` e `issue.opened` | Los emite el **mismo sitio**: `interfaces/triggers/sanitizerChecklogs.controller.ts` (job horario `sanitizerChecklog`). Cuando un check-in vence sin checkout, fabrica un checkout con `status: "incomplete_workday"` y crea acto seguido la incidencia (`issueRepo.create`, línea 139) |
| `issue.responded`, `issue.resolved`, `issue.rejected` | Escrituras sobre `/issues/{id}` desde el back office y la app. El trigger `onCreateIssues` solo cubre el alta |
| `employee.responsibility_changed` | `responsibilitiesHandler` |
| `service.activated/deactivated` | `onActivateCheckbiz` y el flujo de suscripciones |

### `Issue.type` — resuelto el 2026-08-26

El sanitizador escribía `type: "journey_registration"` en snake_case, mientras que el
contenedor y el front lo declaran y lo esperan en camelCase. Era el único sitio que lo
escribía así, con la consecuencia de que las únicas incidencias que la plataforma genera sola
eran también las únicas que el front no sabía etiquetar.

**Queda `journeyRegistration`.** Corregido en el SaaS y desplegado en desarrollo.

Lo que ese cambio no toca: las incidencias **ya creadas** conservan el valor viejo. Antes de
publicar `issue.opened` hacia fuera hay que convertirlas, o el consumidor verá dos tipos para
el mismo hecho.

### Por qué el trigger encoge

Cada fila de la segunda tabla es temporal. Conforme el CRUD de centros, horarios y jornada se
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

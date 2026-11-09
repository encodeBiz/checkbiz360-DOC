# 01 — Estado actual (As-Is)

## No hay cliente

No existe ninguna colección, tabla, servicio ni campo que represente al cliente de una empresa
en el dominio de checkbiz. Comprobado el 2026-10-29 sobre `encodebiz-api`: lo único que se
llama `customer` en `packages/shared` es `findByCustomerId` de `FirestoreEntityRepository`,
que es el **customer de Stripe** de la propia empresa, y las entradas de `webhook_endpoint`.
`services/tasks` no contiene la palabra. Las entidades de `shared/checkbiz/entities` son
`Branch`, `CheckLog`, `Employee`, `Issue`, `Task` y `Team`.

Este documento no describe un sistema que haya que migrar. Describe **lo que ya existe y el
módulo va a reutilizar de verdad**, y lo que hoy hace de cliente sin serlo.

## Lo que hoy hace de cliente sin serlo

**La sucursal.** En Neteges (producción, leído el 2026-10-29): 142 sucursales para 28
empleados, 34 con alguien asignado, 11 personas sin ninguna, y en 30 días 8 personas fichan y
32 de sus 97 fichajes se rechazan por `out_of_radius`. No tienen ninguna tarea y su calendario
es la plantilla por defecto de 9 a 17. Cada «sucursal» es un centro de un cliente. El propio
código lo admite: `Employee.branchId` se comenta como `assigned branches/projects`.

En construcción esa misma identificación es correcta y no un caos: la obra **es** el sitio
donde la gente ficha con su geocerca, así que la sucursal por obra está bien puesta. La
diferencia entre los dos casos no es el modelo de sucursal, es que en Neteges la gente no
ficha en el centro del cliente sino que va a tres o cuatro al día.

**El título de la tarea.** En la empresa de ayuda a domicilio, la tarea se llama como la
clienta y el expediente va de adjunto (TDR-007 de tasks, 2026-10-29). Con cien clientas, cien
PDFs distinguibles por nombre de fichero. El TDR lo acepta y lo deja escrito: «el día que
exista ese add-on, estos adjuntos se reasignan al cliente (un dato más, no una migración)».

## Lo que se reutiliza

### La tarea, que ya tiene el sitio

`packages/shared/src/checkbiz/entities/Task.ts` trae, sin tocar nada:

- `entityId`, `branchId`, `assignedEmployeeIds`: a qué sucursal y a quién se imputa.
- `workSite?: TaskWorkSite`, que **extiende `Geofence`** y lleva `street`, `postalCode`,
  `country`, `timeZone`, `placeId` y `precision` ([tasks TDR-005](../tasks-service/tdr/TDR-005-worksite-y-geocerca-de-tarea.md)).
  Es exactamente la forma que tiene que tener el lugar de un cliente: la cartera lo guarda
  con dueño y la tarea lo recibe tal cual. **La app ya lo conoce** y ya ficha contra él al
  iniciar la tarea; no hace falta que la app sepa de clientes para que la trabajadora llegue
  al sitio correcto.
- `TaskResource` con `isEvidence?: boolean` (TDR-007): la marca que separa adjunto de
  evidencia. Lo que hoy es un adjunto en la tarea mañana es un documento del cliente.
- Estados sellados y eventos `task.status_changed`, `task.validated`, `task.rejected`: las
  únicas señales que un módulo externo puede escuchar, igual que hace inventario.

Lo que la tarea **no** tiene: ningún campo que diga para quién es. `tasks_raw` en Postgres
(migración `026`) tampoco: `branch_id`, `title`, `work_site_tz`, pero ningún cliente.

### La sucursal y el empleado

`Branch` lleva `address.street`, `address.geo`, `postalCode`, `country`, `timeZone`: la misma
dirección geocodificada que el lugar del cliente, así que **una sucursal puede ser el lugar
de un cliente** sin copiar nada (construcción). `Employee.branchId: string[]` da el eje
multisucursal, y `EmployeeResponsibility` quién tiene mando en cada centro.

### Los tres modos de horario

`ScheduleMode = "weekly" | "tasks" | "calendar"` en `shared/calendar/Calendar.ts`, en
pantalla **Semana tipo**, **Por tareas** y **Por turnos** ([horario-por-tareas TDR-009](../horario-por-tareas/tdr/TDR-009-tres-modos-cada-uno-lo-suyo.md),
en producción desde el 2026-10-22). Dos cosas importan aquí:

- **El modo es de cada persona**, no de la sucursal ni de la empresa; «Por tareas» solo se
  pone en la ficha del empleado (decidido el 2026-10-16). La cartera, por tanto, **no puede
  apoyarse en el modo para decidir nada**: una misma sucursal tiene gente en los tres.
- El modo explica la **forma** de cada sector, no el modelo. Con Semana tipo o Por turnos la
  gente ficha en la sucursal (construcción, SAD); con Por tareas va donde dice la tarea
  (Neteges). En los tres casos el cliente se cuelga de la tarea; lo que cambia es de dónde
  salen las horas, y eso se resuelve con un dato explícito en la asignación cliente-sucursal,
  no mirando el modo ([ADR-003](./adr/ADR-003-la-tarea-lleva-el-cliente-y-las-horas-se-imputan-por-tarea-o-por-sucursal-dedicada.md)).

### El documental

`ManagedDocument` (`services/documents/src/domain/entities/Document.ts`) ya es multi-ámbito:
`scope: "entity" | "branch" | "employee" | "item" | "unit"`, con `visibleToRoles`
(`worker | supervisor | manager`), `expiresAt`, `requiresAcknowledgement`, `version`,
`contentSha256` y firma por dentro. Los tipos incluyen `contract`, `project_document`,
`risk_prevention`. Inventario le añadió `item` y `unit` el 2026-10-08 sin tocar el resto.
**Añadir `customer` es el mismo gesto.** El documental cuenta ya con `DocumentActivity`, que
es donde queda quién abrió qué: lo que hace falta para un expediente de SAD.

### El inventario, como precedente entero

Todo lo que este módulo necesita de infraestructura lo estrenó inventario hace un mes. La
puerta de suscripción y el alta en billing valen aquí **solo para el portal** (fase dos): la
cartera básica es gratuita y no las usa (ADR-001, revisado el 2026-11-03). El resto se copia
entero:

- Servicio propio con puerta delante de todo (`requireInventorySubscription` en `app.ts`,
  orden credencial → suscripción → actor → routers) y `GET /access` para que el panel
  pregunte si la empresa lo tiene ([inventario ADR-001](../inventario/adr/ADR-001-servicio-inventory-add-on-de-pago.md)).
- Alta como servicio: valor en `SERVICES` de `shared/platform/Service.ts`, entrada en
  `PLATFORM_SERVICES` de `billing` (`domain/PlatformServices.ts`: «un add-on nuevo entra en
  las tres añadiéndolo aquí»), plan único `standard`, precio en Stripe con tramos graduados
  sobre la plantilla, plantilla de correo de alta (`emailTemplates/inventory.ts`).
- La relación «entidad propia que sirve a varias sucursales», con `scope: "entity" | "branches"`
  y `branchIds[]` explícito ([inventario ADR-002](../inventario/adr/ADR-002-almacen-entidad-propia-multisucursal.md)).
- Instante en Firestore, histórico en Postgres escrito por el propio servicio en la misma
  petición, con job de reintento ([inventario ADR-005](../inventario/adr/ADR-005-instante-firestore-historico-postgres.md)).
- El informe que **cambia de forma con el add-on** y sin él es el de siempre
  ([inventario TDR-005](../inventario/tdr/TDR-005-material-en-el-informe-de-tareas.md)).

### El índice de búsqueda y la paginación

`shared/checkbiz/search/searchIndex.ts` es lo que usa el buscador del panel; lo escriben hoy
el repositorio de sucursales, `manageEmployee` y el de artículos de inventario. Toda lista
nueva del panel entra por ahí y pagina en servidor; borrar un cliente retira su entrada.

### Postgres y los informes

`tasks_raw`, `checklogs_raw`, `dim_branches`, `dim_employees`, `item_movements_raw`,
`unit_assignments_raw`: las horas, el material y quién fue ya están en Postgres. Al informe
por cliente solo le falta la etiqueta. `reports` genera XLSX y ya sabe pedirle a inventario
si la empresa tiene el add-on. La última migración es la `048`.

### Storage

El trigger cuenta contra los 2 GB lo que lleve `entities/{entityId}` en la ruta
([almacenamiento ADR-002](../almacenamiento/)). Los documentos del cliente van bajo la
empresa y se cuentan solos; ningún código suma por su cuenta.

## Lo que no existe y hay que crear

- El cliente, sus contactos y sus lugares.
- La relación cliente-sucursal.
- La tarifa, el presupuesto y el contrato **como objetos de negocio**. Hoy `contract` es
  solo un tipo de documento sin fechas de vigencia propias (tiene `expiresAt`, que vale).
- La imputación de horas a algo que no sea la sucursal o la persona.
- Un informe «por cliente».
- Qué ve la persona de campo del cliente al que va: hoy ve el título y el `workSite` de la
  tarea, nada más.

## Limitaciones del entorno que condicionan el diseño

- **La app lee las tareas directamente de Firestore**, no por la API (TDR-007 §1). Lo que la
  app tenga que enseñar del cliente sin esperar a una versión nueva tiene que estar **dentro
  del documento de la tarea** (un snapshot con nombre y contacto), no en otra colección que
  requeriría reglas y versión.
- **El modo de horario es de la persona.** Nada en la cartera puede depender de él.
- **`sync` no reintenta** (detectado el 2026-09-28). El espejo de este módulo lo escribe
  `customers` como hace `inventory`, y no pasa por `sync`.
- **GitHub Actions parado por facturación desde el 2026-10-23**: los despliegues van a mano
  con su orden. No cambia el diseño; cambia el ritual de cada fase.

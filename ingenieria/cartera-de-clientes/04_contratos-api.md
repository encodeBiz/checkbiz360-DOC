# 04 — Contratos de API

Base: `/api/v1/customers`. Auth y actor como en `tasks`: credencial de panel o de app y
`resolveActor`; **sin puerta de suscripción**, porque la cartera básica es de checkinbiz
(ADR-001). La única puerta del servicio es la del portal, sobre `/portal/*` y sobre las rutas
del panel que lo gestionan ([07](./07_portal-del-cliente.md)). Respuestas de error con
`{code, error, …detalles}`; los códigos empiezan por `customers/`.

Permisos: `canManageCustomers` (owner, admin; gestor con mando en alguna sucursal del
cliente), `canViewCustomers` (lo anterior más supervisor de sus sucursales),
`canViewCustomerFromTask` (el trabajador, solo con tarea asignada de ese cliente).

## Acceso

No hay `GET /access` para el básico: «Clientes» se enseña a toda empresa con checkinbiz. El
selector de cliente en la tarea aparece cuando `GET /?branchId=…` devuelve algo. El portal
tendrá el suyo (`GET /portal/access`, [07](./07_portal-del-cliente.md)).

## Clientes

```
GET    /                 ?entityId&branchId?&status?&q?&limit&cursor   → {items, nextCursor, total}
POST   /                 Customer sin id                               → 201 Customer
GET    /:customerId                                                    → Customer + {sitesCount, openTasksCount, contractsExpiring}
PATCH  /:customerId      campos editables                              → Customer
DELETE /:customerId      ?hard=true                                    → 204 | 409 customers/has_history {tasks, documents}
```

- `branchId` filtra por asignación: devuelve los `scope: "entity"` más los que lleven esa
  sucursal en `branchIds`. Es la consulta del selector de la tarea.
- `q` va contra `searchIndex`; sin `q`, orden por nombre, paginado en servidor.
- `DELETE` sin `hard` es blando. Con `hard`, solo si no hay historia.

### Sucursales

```
PUT    /:customerId/branches     {scope, branchIds, dedicatedBranchIds}  → Customer
```

Una sola ruta que sustituye la asignación entera; es como se edita en el panel. Reglas que
impone el servidor: `dedicatedBranchIds ⊆ branchIds`; una sucursal no puede estar dedicada
a dos clientes (`409 customers/branch_already_dedicated {customerId, customerName}`); una
sucursal que deja de estar en `branchIds` deja de ser `dedicated` y, si tiene lugares `branch`
de este cliente, se avisa en la respuesta (`warnings`) y se desactivan.

## Lugares

```
GET    /:customerId/sites                                  → CustomerSite[]
POST   /:customerId/sites        CustomerSite sin id       → 201
PATCH  /:customerId/sites/:siteId                          → CustomerSite + {updatedFutureTasks: n}
DELETE /:customerId/sites/:siteId                          → 204 + {futureTasksUsingIt: n}
```

- `kind: "address"` exige `workSite` completo (dirección geocodificada y radio); `kind:
  "branch"` exige `branchId ∈ branchIds` del cliente.
- Cambiar el `workSite` de un lugar actualiza las tareas futuras (`draft`/`assigned` con
  `scheduledStartAt` posterior a ahora) que lo referencian por `customerSiteId`, y devuelve
  cuántas. Las pasadas no se tocan.

## Contratos

Construido el 2026-11-05 ([TDR-004](./tdr/TDR-004-rentabilidad-del-montaje.md)). El contrato cuelga
del cliente y puede haber varios a la vez; la tarea dice de cuál es (`Task.contractId`, en
`tasks`: se pone solo si el cliente tiene un único contrato vigente; `null` lo quita). Colección
plana `entities/{e}/customerContracts`; dinero en **céntimos**.

```
GET    /:customerId/contracts                → {items: Profitability[], totals?}   (totals solo owner/admin)
GET    /:customerId/contracts/options?at=    → {items: [{id, title, startsAt, endsAt, inForce}], inForce}
POST   /:customerId/contracts                {title, documentId?, startsAt, endsAt?, amount?, currency?, estimatedHours?, complexity?, notes?, extraction?}
GET    /contracts/:id                        → Profitability + {events}
PATCH  /contracts/:id                        términos, fechas, título, notas (null quita)
POST   /contracts/:id/close                  {closedAt?}
POST   /contracts/:id/reopen
DELETE /contracts/:id                        (409 customers/contract_has_tasks si hay tareas)
```

`Profitability = {contract, period: {from, to, asOf, days}, labour: {minutes, costCents|null,
coverage|null, untrackedSessions, people, source, tasks, tasksByClock}, materials: {movements,
costCents|null, unpricedMovements}, costCents, marginCents, marginPct, warnings, forecast?}`.
Quien no es owner ni admin la recibe sin importe, coste, margen ni extracción.

La **lectura del PDF** es `POST /api/v1/gpt/contratos/leer {entityId, documentId}` en `merlin`
(token de Firebase + owner/admin): devuelve `{extraction, isContract, avisos, inventario}` sin
guardar nada; con PDF escaneado sin texto, 422 `unreadable`.

## Lo que ve la persona de campo

```
GET /for-task/:taskId
→ {customer: {id, name, fieldNotes, contacts: [solo visibleToWorkers]},
   site: {name, workSite},
   documents: [{id, title, type, url} solo visibleToRoles ∋ worker]}
```

Solo si el actor está en `assignedEmployeeIds` de esa tarea (o la gestiona). Es la ruta que
la app llamará en la versión que enseñe documentos del cliente; hasta entonces le basta el
snapshot `task.customer`.

## Actividad e informe

```
GET /:customerId/activity   ?from&to&siteId?   → {days: [{day, employeeId, minutes, source, taskId?}], tasks: [...], totals}
GET /:customerId/report     ?from&to&siteId?   → 302 a reports (XLSX «Por cliente»)
```

El informe lo genera `reports`, que ya hace los XLSX y ya pregunta a inventario por el add-on:
hoja «Resumen» (horas por lugar y por persona, importe si hay tarifa), hoja «Tareas» (con
evidencias contadas), hoja «Material» si hay inventario, hoja «Jornadas» con la fuente de
cada línea (tarea o sucursal dedicada). Lo nombra el servidor
(`cliente-{nombre}-{periodo}.xlsx`), como el resto de informes.

## Interno

```
POST /internal/mirror/retry           job de reintento del espejo (S2S)
POST /internal/hours/recompute        {entityId, from, to}  recalcula customer_hours_daily
```

Fuera de la puerta, antes del json, solo S2S firmado, como `inventory/internal`.

## Lo que cambia en otros servicios

**`tasks`.** `POST /` y `PATCH /:taskId` aceptan `customerId`, `customerSiteId` y `customer`
(snapshot) y los guardan **tal cual**, como `workSite`. El duplicado (`POST /:taskId/duplicate`)
los copia. La carga de cuadrante por tareas (`/tasks/system`, plantilla Excel) acepta una
columna «Cliente» que el panel resuelve a `customerId` **antes** de enviar, por nombre o por
`reference`, y señala en la propuesta las filas que no casan: una tarea sin cliente no es un
error, es una tarea sin cliente.

**`documents`.** `scope: "customer"` con `customerId` en alta, listado y filtros. La URL de
Storage bajo `customers/{customerId}/documents/`. Nada más.

**`reports`.** Informe «Por cliente» (nuevo) y columna «Cliente» en el de tareas, los dos
**solo si la empresa tiene algún cliente dado de alta**: sin clientes, los informes de
siempre, byte a byte. Es la misma mecánica con la que inventario añade el material, con otra
condición.

## Códigos de error

| Código | HTTP | Cuándo |
|---|---|---|
| `customers/not_found` | 404 | Cliente, lugar, contrato o presupuesto inexistente en esa empresa |
| `customers/branch_not_assigned` | 400 | Un lugar `branch` o una tarea apunta a una sucursal que no está en `branchIds` |
| `customers/branch_already_dedicated` | 409 | La sucursal ya es dedicada de otro cliente |
| `customers/has_history` | 409 | Borrado duro con tareas o documentos |
| `customers/forbidden_for_task` | 403 | `for-task` sin estar asignado a la tarea |
| `customers/contract_not_found` | 404 | Contrato inexistente en esa empresa |
| `customers/document_not_found` | 404 | `documentId` que no es un documento activo de ese cliente |
| `customers/contract_has_tasks` | 409 | Borrar un contrato al que apuntan tareas |
| `customers/contract_closed` | 409 | Editar, vincular o cerrar un contrato ya cerrado: antes `reopen` |
| `customers/contract_not_closed` | 409 | `reopen` sobre un contrato activo |
| `customers/portal_subscription_required` | 403 | Lo devuelve la puerta del portal, solo en `/portal/*` y en su gestión |

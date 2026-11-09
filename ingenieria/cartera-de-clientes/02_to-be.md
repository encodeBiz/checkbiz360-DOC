# 02 — Arquitectura objetivo (To-Be)

## Un servicio, sin puerta

`services/customers/` en el puerto **3018** (3016 es `inventory`, 3017 `assistant`), ruta
`/api/v1/customers/`, upstream y location en nginx, bloque en los dos compose. Copia del
esqueleto de `inventory`: `app.ts`, `server.ts`, capas `domain / application / infrastructure /
interfaces`, `jobs/` para el reintento del espejo, `scripts/` para la conversión de Neteges.

**Sin puerta de suscripción** (decidido el 2026-11-03): la cartera básica es parte de
checkinbiz y gratuita, así que las rutas exigen la credencial de checkinbiz como las de
`tasks` y nada más. Orden: credencial → actor → routers. El panel enseña «Clientes» a toda
empresa con checkinbiz, sin preguntar a nadie.

Por qué servicio propio aunque sea gratis, y no un módulo dentro de `tasks` o `checkinbiz`:
porque el **portal del cliente** (fase dos, [07](./07_portal-del-cliente.md)) se engancha a
él y ese sí lleva puerta, autenticación propia y ritmo propio; porque `tasks` ya es grande y
el acoplamiento iría en la dirección equivocada; y porque la imputación de horas y el espejo
son jobs. Y si un día hay que cobrar el básico, la puerta se pone delante en una tarde, como
la tiene inventario ([inventario ADR-001](../inventario/adr/ADR-001-servicio-inventory-add-on-de-pago.md)).
Ver [ADR-001](./adr/ADR-001-servicio-customers-en-el-core-gratuito.md).

La única puerta del servicio es la del portal: `requirePortalSubscription` delante de
`/api/v1/customers/portal/*` y de las rutas del panel que lo gestionan
([ADR-005](./adr/ADR-005-el-portal-del-cliente-es-el-add-on-como-el-quiosco.md)).

## Lo que toca fuera de su casa

Poco, y todo aditivo:

| Dónde | Qué | Por qué |
|---|---|---|
| `shared/checkbiz/entities/Task.ts` | `customerId?`, `customerSiteId?`, `customer?: {id, name, contact?}` | El cliente de la tarea y un snapshot para la app, que lee Firestore |
| `shared/platform/Service.ts`, `billing` | **Nada en v1.** El portal (fase dos) entra como `customer_portal`, calcado del quiosco | El básico no se cobra |
| `documents` `Document.ts` | `scope: "customer"`, `customerId?` | El expediente y el contrato viven en el cliente |
| `migrations/049_*.sql` | `customer_id`, `customer_site_id` en `tasks_raw`; tablas del módulo | Informe por cliente |
| `reports` | Informe «Por cliente»; columna «Cliente» en el de tareas **solo si la empresa tiene algún cliente** | Sin clientes, los informes de siempre, byte a byte |
| `tasks` | Acepta y guarda los tres campos como guarda `workSite`: **opacos** | `tasks` no conoce el módulo |

`tasks` **no valida** que el cliente exista ni que pertenezca a la sucursal. Lo garantiza el
selector del panel, que solo enseña los clientes de esa sucursal, y lo vigila el espejo: una
tarea con `customerId` que no está en `dim_customers` aparece en el panel como «cliente
desconocido», un filtro, no un error. Es el precio de que el núcleo no dependa de un módulo
opcional, y es el mismo trato que recibe `workSite` hoy.

## Cómo fluye el dato

**Hacia abajo, un campo.** El panel, al crear o editar una tarea en una sucursal, pide a
`customers` los clientes de esa sucursal y los ofrece en un desplegable **opcional y sin
preseleccionar**, también cuando hay uno solo: hay tareas que no son de ningún cliente
(administración, una validación), y un cliente puesto solo se colaba en ellas (Jose,
2026-11-05). Es además la regla del almacén: un valor por defecto se acepta por inercia y
acaba firmando contra el cliente equivocado. Sin cliente, la tarea se crea como hoy. Elegido el cliente, sus lugares: uno, entra solo como `workSite`; varios,
se elige. El panel escribe en `tasks` `customerId`, `customerSiteId`, el snapshot y el
`workSite` copiado del lugar. **La app no cambia**: recibe un `workSite` como siempre.

**Hacia arriba, lo del cliente.** Contactos, lugares, documentos (por `documents` con
`scope: "customer"`), contratos, tarifa y presupuestos viven en `customers` y se gestionan
desde la ficha del cliente en el panel.

**Hacia el cliente, lo que ya existe.** Las horas, las evidencias y el material **no se
escriben dos veces**. El espejo de `customers` añade la etiqueta a `tasks_raw` y calcula la
imputación diaria (`customer_hours_daily`) desde `tasks_raw` y `checklogs_raw` según la regla
del [ADR-003](./adr/ADR-003-la-tarea-lleva-el-cliente-y-las-horas-se-imputan-por-tarea-o-por-sucursal-dedicada.md):
las horas de una tarea con cliente son de ese cliente; las jornadas fichadas en una sucursal
**dedicada** a un cliente son de ese cliente. `reports` lee de ahí.

## Dónde vive cada cosa

| | Firestore (instante) | Postgres (histórico) |
|---|---|---|
| Cliente, contactos, lugares, asignación a sucursales | `customers`, subcolecciones `sites`, `contracts`, `budgets` | `dim_customers`, `dim_customer_sites`, `customer_branch_links`, `customer_contracts`, `customer_budgets` |
| El cliente de la tarea | en `tasks` (campos nuevos) | `tasks_raw.customer_id`, `customer_site_id` |
| Horas por cliente y día | — | `customer_hours_daily`, materializada por un job |
| Importe facturable, desvío | — | se calculan al leer, con la tarifa y el presupuesto vigentes |
| Documentos del cliente | `documents` (del documental) | — |
| Búsqueda del panel | `searchIndex`, `kind: "customer"` | — |

El espejo lo escribe `customers` en la misma petición que el instante, con un job de
reintento, como inventario. No pasa por `sync`.

## Permisos

| Quién | Clientes | Documentos del cliente |
|---|---|---|
| Owner, admin | Todo, en toda la empresa | Todo |
| Gestor con mando en una sucursal | Ve y edita los clientes asignados a sus sucursales; no borra | Según `visibleToRoles` |
| Supervisor | Ve los de sus sucursales | Según `visibleToRoles` |
| Trabajador | **Solo a través de la tarea asignada**: nombre, lugar, contacto, notas de campo | Solo los marcados `visibleToRoles: ["worker"]`, y solo mientras tenga tarea de ese cliente |

La asimetría del trabajador es deliberada y es lo delicado del SAD: el expediente de Juana lo
ve la auxiliar que va a casa de Juana hoy, no toda la plantilla. Cada apertura queda en
`DocumentActivity`, que ya existe.

## Lo que pasa al darse de baja

Del básico no hay baja: es checkinbiz. Del **portal** sí: deja de pasar su puerta, los
enlaces de los contactos dejan de abrir, el panel esconde la pestaña Portal. Las solicitudes,
los mensajes y las firmas que el cliente dejó **se quedan en el cliente**, que es del core, y
se siguen viendo desde el panel. Volver a contratar reactiva los accesos sin tocar nada:
**apagar no borra**, como inventario.

## Lo que este módulo no hace

- No valida la tarea, no la bloquea, no la retrasa: si `customers` está caído, la tarea se
  crea sin cliente y el panel lo dice en rojo.
- No escucha el bus para nada en v1. Inventario necesitaba reaccionar a la validación de la
  tarea para cuadrar el sobrante; la cartera no tiene nada que hacer en ese instante. Si lo
  necesita (contador de visitas por contrato, por ejemplo), se engancha como suscriptor
  interno igual que inventario.
- No emite facturas ni habla con Stripe por cuenta de la empresa. Ver [ADR-004](./adr/ADR-004-la-tarifa-valora-no-factura.md).

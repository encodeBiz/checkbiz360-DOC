# TDR-001 — Colecciones, maestros y puerta de suscripción

**Fecha:** 2026-09-28
**Estado:** Diseño aprobado
**Componente:** `encodebiz-api` — `inventory:3016` + `@encodebiz/shared`
**Decisiones de referencia:** [ADR-001](../adr/ADR-001-servicio-inventory-add-on-de-pago.md),
[ADR-002](../adr/ADR-002-almacen-entidad-propia-multisucursal.md),
[ADR-003](../adr/ADR-003-un-catalogo-consumible-y-operable.md)

---

## 1. Dónde vive el dominio

`packages/shared/src/checkbiz/inventory/`:

```
entities/Warehouse.ts      Warehouse
entities/Item.ts           Item, ItemType, UsageUnit
entities/ItemUnit.ts       ItemUnit, UnitStatus
entities/Stock.ts          Stock
entities/Movement.ts       ItemMovement, MovementType
entities/TaskMaterial.ts   TaskMaterial
entities/Reservation.ts    UnitReservation, ReservationStatus
repositories/Firestore*Repository.ts
plan/inventoryAccess.ts    getInventoryAccess(entityId)
```

El dominio de checkbiz vive en `shared` y no se copia a los servicios. `inventory` importa de
ahí, igual que `tasks`, `employees` y `branches`.

## 2. Rutas de Firestore

```
entities/{entityId}/warehouses/{warehouseId}
entities/{entityId}/items/{itemId}
entities/{entityId}/item_units/{unitId}
entities/{entityId}/stock/{itemId}_{warehouseId}
entities/{entityId}/item_movements/{movementId}
entities/{entityId}/task_materials/{taskId}_{itemId}
entities/{entityId}/unit_reservations/{reservationId}
```

Los ids compuestos de `stock` y `task_materials` son deliberados: permiten escribir sin buscar
primero y garantizan unicidad sin índice.

## 3. Índices compuestos necesarios

Las colecciones cuelgan de `entities/{entityId}/…`, así que con `queryScope: COLLECTION` el
`entityId` **no va en el índice**: ya lo da la ruta.

**En la implementación (Fases 1–2) no hace falta ninguno**: las consultas del módulo usan
solo igualdades —que Firestore resuelve con los índices de campo único— y ordenan en memoria,
porque son pocos documentos por entidad y cada `where` + `orderBy` habría exigido su propio
índice compuesto (se comprobó el 2026-09-29: la primera versión pedía tres). La tabla de
abajo queda como referencia de lo que haría falta si alguna consulta volviera a ordenar en
Firestore. Y recordar la deriva ya documentada: el fichero de índices no refleja lo
desplegado, y el deploy de Firebase poda mientras `gcloud` no.

| Colección | Campos |
|---|---|
| `warehouses` | `branchIds` (array-contains) + `status` · `scope` + `status` |
| `items` | `type` + `active` |
| `item_units` | `itemId` + `status` · `warehouseId` + `status` |
| `stock` | `warehouseId` · `itemId` · `hasDiscrepancy` |
| `item_movements` | `occurredAt` · `taskId` + `occurredAt` · `mirrored` + `createdAt` |
| `task_materials` | `taskId` |
| `unit_reservations` | `unitId` + `status` + `startAt` · `taskId` + `status` |

`mirrored` se consulta como booleano escrito siempre: Firestore no encuentra campos ausentes,
así que `mirroredAt == null` no valdría.

## 4. La puerta de suscripción

Middleware montado antes de todos los routers menos `/health`:

```
entities/{entityId}/subscriptions/inventory   → {plan, status}
```

Una comprobación: suscripción presente y `status` en `active` o `trialing` → si no, **403**
`inventory/not_subscribed`. Es 403 y no 402 a propósito: la plataforma no usa 402, y un
código nuevo obliga a tocar el proxy del panel y el cliente Dio; el código en el cuerpo basta
para que el panel ofrezca el alta.

No hay un «módulo activado» aparte de la suscripción: contratar es activar. Y no hay límites
de plan que comprobar: **un límite nunca para el servicio; si se pasa, se cobra.** El módulo
lee la suscripción y nunca el plan. Las rutas exentas son `/health` y la interna de eventos.

### Alta del servicio

```
service/inventory                      → {id, name, active, activatedAt}
service/inventory/plan/{planId}        → {name, stripePrice, minItemsPay}
```

La suscripción la escribe `billing` por entidad y servicio. Para que `inventory` exista como
servicio: añadirlo al tipo `SERVICES` de `packages/shared/src/platform/Service.ts`, a
`OUR_SERVICES` en `StripeWebhookHandler.ts`, y crear el precio en Stripe. **No hay trigger que
portar**: `onActivateCheckbiz` ya está en `firebase_sdk/altas/` y solo crea la sucursal inicial.

## 5. Búsqueda

Si artículos y almacenes se buscan desde el panel, entran en `searchIndex` — y **el borrado
tiene que retirar la entrada**. Es la trampa que el repo ya documenta para empleados y centros,
y cualquier borrado nuevo tiene que acordarse. Ver [06 §D7](../06_decisiones-abiertas.md).

## 6. Borrado

- **Almacén** con existencias distintas de cero o ejemplares con base ahí: `409`
  `inventory/warehouse_not_empty`, con el detalle de qué queda dentro.
- **Artículo** con movimientos: no se borra, se archiva (`active: false`). La historia no se
  puede quedar apuntando a un artículo que no existe.
- **Ejemplar** con reservas futuras: se avisa y se devuelven las reservas afectadas; no se
  cancelan solas.

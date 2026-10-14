# 04 — Contratos de API

**Base:** `https://<host>/api/v1/inventory`
**Auth:** `Authorization: Bearer <token>` — Firebase ID token (panel) o staff JWT (app), igual
que en `tasks`.
**Puerta:** toda ruta distinta de `/health` y de la interna pasa por el middleware de
suscripción. Sin suscripción activa de `inventory` → **403** `inventory/not_subscribed`. No hay
límites de plan que devuelvan nada: un límite nunca para el servicio.

## Permisos

Misma escala de responsabilidad que tareas (`worker < supervisor < manager < admin/owner`), con
`isEntityWriter` como atajo de entidad, igual que en `task.helpers.ts`:

| Acción | Quién |
|---|---|
| Ver almacenes, artículos y existencias | `worker` (solo los almacenes de sus sucursales) o superior |
| Crear/editar artículos, almacenes y ejemplares | `manager`, `admin`, `owner`, entityWriter |
| Entradas, ajustes y traspasos | `manager` o superior |
| Reservar material y operables a una tarea | `supervisor` o superior |
| Sacar material y declarar consumo | `worker` asignado a la tarea, o `supervisor` o superior |
| Cuadrar el pendiente al validar | quien puede validar la tarea (`canValidateOrRejectTask`) |

---

## Almacenes

### `GET /warehouses`
Query: `entityId` (obligatorio), `branchId?`, `status?`.
Con `branchId` devuelve los que tienen esa sucursal en `branchIds` (y, mientras existan, los
anteriores con `scope: "entity"`, que sirven a todas hasta que se editen).
`200` → `Warehouse[]`.

### `POST /warehouses`
Body: `entityId`, `name`, `branchIds` (**obligatorio, al menos una**), `address?`. `scope` no se lee:
todo almacén cuelga de sucursales (decisión del 2026-09-29: el almacén general vive en la
sucursal principal, no «en toda la empresa»).
`400 inventory/branches_required` si `branchIds` vacío.
`201` → `Warehouse`.

### `PATCH /warehouses/:warehouseId`
Body: campos editables. Quitar una sucursal de `branchIds` **no** borra existencias ni
movimientos: solo deja de ofrecerse a esa sucursal. Dejar `branchIds` vacío con
es `400`, no «pasa a global».
`200` → `Warehouse`.

### `DELETE /warehouses/:warehouseId`
Solo si no tiene existencias con `onHand != 0` ni ejemplares con base ahí.
`409 inventory/warehouse_not_empty` en otro caso, con el detalle de qué queda dentro.

---

## Artículos

### `GET /items`
Query: `entityId`, `type?`, `category?`, `q?` (nombre o referencia), `active?`.
`200` → `Item[]`.

### `POST /items`
Body: `entityId`, `type`, `name`, `reference?`, `unit?`, `unitCost?`, `usageUnit?`, `category?`.
`400 inventory/usage_unit_required` si `type: "operable"` y falta `usageUnit`.
`201` → `Item`.

### `PATCH /items/:itemId`
El `type` **no es editable**: un consumible no se convierte en operable, porque su historia de
movimientos no se puede reinterpretar. Para eso se crea otro artículo.
`200` → `Item`.

### `DELETE /items/:itemId`
Si tiene movimientos, no se borra: se archiva (`active: false`). `200` → `{archived: true}`.

---

## Ejemplares de operable

### `GET /items/:itemId/units`
Query: `entityId`, `warehouseId?`, `status?`.
`200` → `ItemUnit[]`, cada uno con su reserva activa si la hay (`currentReservation?`), que es
de donde sale «en uso» y «dónde está».

### `POST /items/:itemId/units`
Body: `entityId`, `warehouseId`, `identifier?`, `label?`, `usageCounter?`.
`400 inventory/not_operable` si el artículo es consumible; `404 inventory/warehouse_not_found`
si el almacén no existe o está inactivo.
`201` → `ItemUnit`.

### `PATCH /units/:unitId`
Body: `warehouseId?` (cambio de base), `status?`, `unavailableReason?`, `unavailableUntil?`.
Pasar a `unavailable` con reservas futuras devuelve `200` **y la lista de reservas afectadas**,
para que el panel las enseñe. No se cancelan solas.

### `GET /units/:unitId/schedule`
Query: `from`, `to`.
`200` → `{reservations: UnitReservation[], unavailable: {from, to, reason}[]}`.

---

## Existencias

### `GET /stock`
Query: `entityId`, `warehouseId?`, `itemId?`, `belowMinimum?`, `withDiscrepancy?`.
`200` → `Stock[]` con `available = onHand - committed` calculado.

### `POST /stock/receipts` — entrada
Body: `entityId`, `movementId`, `warehouseId`, `itemId`, `quantity`, `unitCost?`, `note?`.
Efectos: movimiento `receipt`, sube `onHand`.
`201` → `{movement, stock}`.

### `POST /stock/adjustments` — ajuste de recuento
Body: `entityId`, `movementId`, `warehouseId`, `itemId`, `countedQuantity`, `reason`.
Efectos: movimiento `adjustment` con `previousOnHand`, deja `onHand = countedQuantity`, limpia
`hasDiscrepancy`. `reason` es **obligatorio** (`400 inventory/adjustment_reason_required`).

### `POST /stock/transfers` — traspaso
Body: `entityId`, `movementId`, `itemId`, `fromWarehouseId`, `toWarehouseId`, `quantity`, `note?`.
Efectos: dos movimientos (`transfer_out` + `transfer_in`) con el mismo `transferId`, en una
transacción.

---

## Material de una tarea

### `GET /tasks/:taskId/materials`
`200` → `{materials: TaskMaterial[], reservations: UnitReservation[]}`.
Es lo que la app pinta en la pantalla de material de la tarea.

### `POST /tasks/:taskId/materials/reserve` — asignar
Permiso: `supervisor` o superior.
Body: `entityId`, `movementId`, `items: [{itemId, warehouseId, quantity}]`.
Efectos: movimiento `reservation`, sube `committed`. **No toca `onHand`**.
Si `available < quantity`, **no se bloquea**: se reserva igual y se devuelve `201` con
`warnings: [{itemId, available, requested}]`. Avisar, no impedir.
`409 inventory/material_warehouse_mismatch` si el artículo ya tiene otro almacén en esta tarea.

### `POST /tasks/:taskId/materials/issue` — salida
Permiso: `worker` asignado a la tarea, o `supervisor` o superior.
Body: `entityId`, `movementId`, `items: [{itemId, warehouseId?, quantity}]`, `employeeId?`,
`occurredAt?`.
`warehouseId` es obligatorio **solo si la sucursal de la tarea tiene más de un almacén**; con
uno solo, el servidor lo resuelve. Con varios y sin él: `400 inventory/warehouse_required` con
la lista de candidatos. Sin preseleccionar.
`occurredAt` es opcional y hoy no lo manda nadie: está para el offline. Si viene, se respeta;
si no, hora del servidor.
Efectos: movimiento `issue`, baja `onHand`, baja `committed` en lo que estuviera reservado.
`409 inventory/material_warehouse_mismatch` si el artículo ya salió de otro almacén en esta
tarea.

### `POST /tasks/:taskId/materials/consume` — declarar gasto
Permiso: como `issue`.
Body: `entityId`, `movementId`, `items: [{itemId, quantity}]`, `employeeId?`, `occurredAt?`.
La app pregunta **cuánto se usó**, nunca cuánto se devuelve, y llega precargada con lo que
salió: si se gastó todo, es un clic.
Efectos: movimiento `consumption`, actualiza `consumed` y `pending`, actividad `item_consumed`
en la tarea.

### `POST /tasks/:taskId/materials/settle` — cuadrar el pendiente
Permiso: quien valida la tarea.
Body: `entityId`, `movementId`, `items: [{itemId, resolution: "returned" | "consumed", quantity}]`.
Efectos: movimiento `return` o `consumption` según la resolución; `pending` a cero.
Es el paso que aparece en la pantalla de validación cuando quedan cantidades sin declarar.

---

## Material por destino — persona o sucursal (2026-10-14)

Las mismas cuatro operaciones que la tarea, contra una **persona** o una **sucursal**
([ADR-009](./adr/ADR-009-el-material-sale-hacia-una-tarea-una-persona-o-una-sucursal.md)). Cuelgan
de `/materials` y llevan el destino en el cuerpo (`kind`, `id`); `kind: "task"` también vale y
delega en lo de arriba. Contratos completos en [TDR-008](./tdr/TDR-008-cuentas-de-material-por-destino.md) §4.

```
GET  /materials?kind&id                 → { accounts }            ficha del empleado o de la sucursal
GET  /me/materials                      → { accounts }            «Mi material» en la app (kind=employee)
GET  /materials/outstanding?warehouseId → { accounts + nombres }  lo que está fuera del almacén, por destino
POST /materials/reserve                 { kind, id, movementId, items }                       dotación
POST /materials/issue                   { kind, id, movementId, items, branchId?, employeeId? } salida
POST /materials/consume                 { kind, id, movementId, items, branchId?, employeeId? } gasto (apunta la salida si no la hubo)
POST /materials/return                  { kind, id, movementId, items }                       devolución
POST /materials/settle                  { kind, id, movementId, items: [{resolution}] }        cuadre; lo no resuelto se queda
```

---

## Operables en una tarea

### `POST /tasks/:taskId/units` — reservar
Body: `entityId`, `unitId`, `startAt`, `endAt`.
`409 inventory/unit_conflict` si el intervalo solapa con otra reserva, **con la reserva que
choca en el cuerpo** (`{taskId, taskTitle, startAt, endAt, branchId}`).
`409 inventory/unit_unavailable` si el ejemplar está no disponible en ese tramo.
`201` → `UnitReservation`.

### `DELETE /tasks/:taskId/units/:unitId` — liberar a mano
`200` → `UnitReservation` con `status: "released"`, `releasedReason: "manual"`.

### `GET /board` — tablero de ocupación
Query: `entityId`, `from`, `to`, `warehouseId?`, `itemId?`.
`200` → `UnitBoard` — **contrato propio**, no el `AvailabilityBoard`:

```ts
interface UnitBoard {
  range: {from: string; to: string; timezone: string};
  rows: {
    unitId: string; itemId: string; itemName: string; label?: string; warehouseId: string;
    days: {
      date: string;
      slots: {kind: "reservation" | "unavailable"; from: string; to: string;
              taskId?: string; taskTitle?: string; site?: string; reason?: string}[];
    }[];
  }[];
}
```

Es una agenda por ejemplar, no un mapa de calor. Detalle en
[TDR-003 §4](./tdr/TDR-003-operables-agenda-y-choque.md).

---

## Libro

### `GET /movements`
Query: `entityId`, `from`, `to`, `itemId?`, `warehouseId?`, `taskId?`, `employeeId?`, `type?`,
`limit?`, `cursor?`.
Se sirve **desde Postgres**. `200` → `{movements: ItemMovement[], cursor?, staleness?}`.
`staleness` aparece si hay movimientos sin espejar más viejos que el umbral: un informe
incompleto que se presenta como completo es peor que no tenerlo.

Los informes agregados viven en `reports`, como el informe de tareas.

---

## Interno

### `POST /internal/task-events`
Auth: S2S (la misma que campañas). Recibe entregas de `task.status_changed`, `task.validated`
y `task.rejected` desde el motor de eventos. Idempotente por `delivery_id`. `204` siempre que
la entrega sea válida, tenga o no la entidad suscripción.

---

## Errores

| Código | Cuándo |
|---|---|
| `403 inventory/not_subscribed` | La entidad no tiene el add-on |
| `400 inventory/warehouse_required` | La sucursal tiene varios almacenes y no se dijo cuál |
| `409 inventory/material_warehouse_mismatch` | Mismo artículo desde dos almacenes en una tarea |
| `409 inventory/unit_conflict` | Solapamiento de reservas |
| `409 inventory/unit_unavailable` | El ejemplar está no disponible en ese tramo |
| `409 inventory/warehouse_not_empty` | Borrado de almacén con existencias o ejemplares |
| `400 inventory/branches_required` | Almacén sin sucursales |
| `400 inventory/adjustment_reason_required` | Ajuste sin motivo |
| `400 inventory/account_required` | Un movimiento de cuenta sin destino (`accountKind` y su id) |

**No hay error por falta de existencias.** Reservar de más avisa; consumir de más deja el saldo
en negativo y lo marca. Ver [ADR-005](./adr/ADR-005-instante-firestore-historico-postgres.md),
«El saldo puede quedar negativo».

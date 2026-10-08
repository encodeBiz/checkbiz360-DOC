# TDR-002 — Saldos, libro de movimientos y conciliación del sobrante

**Fecha:** 2026-09-28 (revisado el mismo día)
**Estado:** Diseño aprobado
**Componente:** `encodebiz-api` — `inventory:3016` + `shared/events`
**Decisiones de referencia:** [ADR-004](../adr/ADR-004-asignar-no-es-consumir.md),
[ADR-005](../adr/ADR-005-instante-firestore-historico-postgres.md)

---

## 1. El invariante

Cantidades **siempre positivas**; el signo lo pone el tipo:

```
onHand    = Σ receipt − Σ issue + Σ return + Σ transfer_in − Σ transfer_out   (adjustment fija el valor)
committed = Σ reservation − Σ reservation_released − Σ issue_sobre_reserva
available = onHand − committed
```

`issue_sobre_reserva` es `min(quantity, reserved − reservedIssued − released)` de la tarea: una
salida descuenta compromiso solo hasta lo que quedaba reservado; el resto sale sin plan y no
toca `committed`. La cuenta guarda esa parte en `reservedIssued`. **No** se calcula con
`issued`: una salida grande sin plan «gastaría» las reservas posteriores y el compromiso se
quedaría vivo para siempre en el saldo — encontrado en la prueba del 2026-09-29.

**El movimiento es la verdad; el saldo es una proyección.**

## 2. Un solo camino de escritura

Toda escritura entra por HTTP a `inventory` con un `movementId` generado por la app. El caso de
uso:

1. Resuelve actor, permisos, tarea y almacén (§7).
2. Abre **una transacción de Firestore**:
   - Lee `item_movements/{movementId}`. **Si existe, devuelve lo que hay y termina**: es un
     reintento de red, no un apunte nuevo. Este es el único mecanismo de idempotencia; la
     «ventana de ids aplicados» de la primera versión era insegura y sobra.
   - Lee `stock/{itemId_warehouseId}` (y `task_materials/{taskId_itemId}` si aplica).
   - Escribe el movimiento con `mirrored: false`, aplica el delta al saldo y a la cuenta de la
     tarea.
3. Tras confirmar, inserta en Postgres a mejor esfuerzo ([TDR-004 §2](./TDR-004-espejo-postgres-e-informes.md)).

No hay observador de `item_movements`, ni `appliedAt`, ni camino offline: la app no escribe en
Firestore.

## 3. `occurredAt`

Lo pone el servidor. Las rutas de salida y consumo aceptan uno opcional desde la app; si viene,
se respeta. Hoy no lo manda nadie: es el gancho para que el offline, cuando se retome, no toque
el contrato ([06 §D3](../06_decisiones-abiertas.md)).

## 4. Recálculo periódico

Un job en `inventory` recorre las existencias con actividad reciente, **recalcula desde los
movimientos** y reescribe el saldo si difiere, dejando registro de la corrección. Es lo que
convierte una deriva en una condición que se cura sola.

## 5. Saldo negativo

`onHand < 0` es **un resultado válido**, no un error. Se marca `hasDiscrepancy: true` y se lista
para que un responsable haga un ajuste. No se impide, no se redondea a cero y no se rechaza el
movimiento.

## 6. Cómo se entera `inventory` de la tarea

`publish()` **no es un bus**: resuelve los endpoints suscritos del cliente y, si no hay
ninguno, vuelve sin encolar. Para que `inventory` reciba algo, la resolución de suscriptores
devuelve, además de los del cliente, **un endpoint interno** hacia
`POST /api/v1/inventory/internal/task-events` para los tipos `task.*`. Con eso hereda firma,
`webhook_delivery`, backoff y rescate — más garantía de la que tiene `sync`.

- Autenticación S2S, la misma que campañas.
- **Idempotente por `delivery_id`**: las entregas se reintentan.
- Responde `204` rápido a las entidades sin suscripción. No se filtra en el resolutor: acoplar
  el motor de eventos a la suscripción de un módulo es peor que unas filas de más.

### Los eventos y lo que hace con cada uno

| Evento | Condición | Efecto en `inventory` |
|---|---|---|
| `task.status_changed` | `status: "in_progress"` | Reservas de la tarea a `in_use`. **Idempotente**: llega también por el «deshacer» `completed → in_progress`. |
| `task.status_changed` | `status: "completed"` | Reservas a `released` (`completed`). El material queda `pending` hasta validar. |
| `task.status_changed` | `status: "cancelled"` | `reservation_released` por `reserved − issued`; reservas a `released` (`cancelled`); el material ya salido sigue `pending` — cancelar no devuelve toallas que están en una furgoneta. |
| `task.status_changed` | `status: "assigned"` o `"draft"` (reabrir) | Nada. Una reserva liberada no resucita; el `pending` sigue ahí. |
| `task.validated` | — | `reservation_released` por `reserved − issued`; reservas a `released` si aún no lo estaban. Es el momento del cuadre (§8). |
| `task.rejected` | desde `in_progress` o `completed` | Como `validated` en cuanto a compromiso y reservas (`rejected`). |
| `task.rejected` | desde `validated` | **Nada**: el material ya se cuadró y el compromiso ya bajó. |

Las tres trampas del control de estado, comprobadas en `updateTaskStatus.controller.ts`:
`status_changed` solo se emite si el estado cambió de verdad, así que el **completado parcial no
emite nada**; el «deshacer» sí emite `in_progress` otra vez; y reabrir llega **después** de
haber liberado.

## 7. Resolución del almacén

Al registrar una salida, el servidor mira cuántos almacenes sirven a la sucursal de la tarea
(`scope: "entity"` ∪ `branchIds` contiene la sucursal):

- **Uno** → lo resuelve y no pregunta. El movimiento guarda el `warehouseId` igualmente.
- **Varios** → `warehouseId` es obligatorio en el cuerpo. Sin él, `400`
  `inventory/warehouse_required` **con la lista de candidatos**. Sin preseleccionar
  ([ADR-002](../adr/ADR-002-almacen-entidad-propia-multisucursal.md), «Sin almacén principal»).
- Si `task_materials/{taskId_itemId}` ya tiene otro `warehouseId` → `409`
  `inventory/material_warehouse_mismatch`. Un almacén por artículo y tarea.

## 8. La conciliación del sobrante

`task_materials` mantiene, por tarea y artículo:

```
pending = issued − consumed − returned
```

Mientras la tarea está abierta, `pending > 0` es normal: el material está en la furgoneta.

Al **validar**, si queda `pending > 0`, la pantalla de validación muestra *«salieron 30, se
declararon 20, faltan 10»* y ofrece resolverlo con `POST /tasks/:id/materials/settle`:
**devueltas** (movimiento `return`, sube `onHand`) o **consumidas** (movimiento `consumption`,
se imputa al empleado). Un botón. Y en la misma validación, lo reservado que nunca salió se
libera (§6).

Es **Fase 2**, no un extra: es el cierre del ciclo del consumible.

## 9. Rastro en la tarea

Cada `consumption` deja una entrada de `TaskActivity` con `type: "item_consumed"` y el detalle
en `metadata`. Es un valor nuevo en el enum de `Task.ts`, en `shared` — aditivo. Se escribe **a
través del repositorio de `shared`**, no tocando la colección a mano.

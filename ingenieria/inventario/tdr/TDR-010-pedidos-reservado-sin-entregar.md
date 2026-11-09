# TDR-010 — Pedidos: lo reservado sin entregar, agrupado por destino

**Fecha:** 2026-11-09
**Estado:** implementado en `feat/inventario-pendiente-producto` (API y panel), sin desplegar
**Servicio:** `encodebiz-api/services/inventory` + `encodebiz-front-saas` (Inventario → Pedidos)
**Relacionado:** [ADR-004](../adr/ADR-004-asignar-no-es-consumir.md), [ADR-009](../adr/ADR-009-el-material-sale-hacia-una-tarea-una-persona-o-una-sucursal.md), [TDR-004](./TDR-004-espejo-postgres-e-informes.md), [TDR-008](./TDR-008-cuentas-de-material-por-destino.md)

---

## Por qué

Jose, 2026-11-09: una tarea con cinco o más artículos reservados obliga al almacén a dar salida
artículo a artículo, buscando cada uno. Lo que el almacén necesita es una lista de **pedidos**:
cada destino con todo lo que tiene reservado y aún no ha salido, y una acción para entregarlo
entero de una vez.

Decisiones de Jose en la misma conversación:

- Pedidos de **tareas, personas y sucursales** (las tres cuentas de ADR-009).
- **Paginado de 5 en 5**, del más reciente al más antiguo.
- **Buscador** por el nombre del destino (la tarea, la persona o la sucursal).
- El **albarán / acta de entrega** (documento y firma) queda para otra fase.

## Qué es un pedido

Un destino (`account_kind` + su id) con al menos una línea donde lo reservado no ha salido:

```
por entregar = reservado − la parte de las salidas que descontó reserva − liberado
```

Es exactamente `outstandingReservation()` de `shared` (`reserved − reservedIssued − released`),
calculado por línea (destino, artículo, almacén).

## Dónde se lee: Postgres, no Firestore

En Firestore ese número no está guardado: se calcula al leer cada cuenta. Listar «las cuentas
con algo por entregar» exigiría guardarlo como campo nuevo en `task_materials` y
`material_accounts`, un script que lo rellene en lo existente, leer todas las cuentas abiertas
en cada página y agrupar y paginar en memoria. Y el buscador no tiene dónde mirar: las tareas
no están en `searchIndex`.

Postgres ya tiene todo:

- `item_movements_raw` guarda cada apunte con su `account_kind`, `task_id` / `employee_id` /
  `branch_id` y su `committed_delta` (la parte que descontó reserva, en `issue` y
  `reservation_released`). El espejo se escribe en la misma petición, tras Firestore
  (`MirroredLedger`); lo que falla lo recoge `remirror`.
- Los nombres están en `tasks_raw` (título, estado, inicio previsto), `dim_employees`,
  `dim_branches`, `dim_items` y `dim_warehouses`.

Una sola consulta agrupa, filtra por nombre, ordena y pagina. Sin migración: la consulta va
por `idx_movements_account_kind (entity_id, account_kind, occurred_at DESC)`. Recorre los
apuntes de reserva, salida y liberación de la empresa; si algún día pesa, el siguiente paso es
un índice parcial `WHERE type IN ('reservation','issue','reservation_released')`.

```sql
WITH lines AS (
  SELECT account_kind AS kind,
         CASE account_kind WHEN 'task' THEN task_id WHEN 'employee' THEN employee_id ELSE branch_id END AS target_id,
         item_id, warehouse_id,
         SUM(CASE WHEN type = 'reservation' THEN quantity ELSE 0 END)
           - SUM(CASE WHEN type IN ('issue','reservation_released') THEN COALESCE(committed_delta, 0) ELSE 0 END) AS to_issue,
         MAX(occurred_at) FILTER (WHERE type = 'reservation') AS reserved_at
    FROM item_movements_raw
   WHERE entity_id = $1 AND account_kind IS NOT NULL
     AND type IN ('reservation', 'issue', 'reservation_released')
   GROUP BY 1, 2, 3, 4
)
-- por destino: líneas con to_issue > 0, nombre del destino, último reservado;
-- ORDER BY último reservado DESC, LIMIT 6 OFFSET page*5 (el sexto dice si hay más)
```

El orden es **la última reserva del pedido**, descendente: lo último que se pidió, arriba.

## Contrato

```
GET /orders?entityId&q?&kind?&warehouseId?&page?   (supervisor o superior: canReserve)
→ { orders: [{ kind, targetId, targetName, taskStatus?, scheduledStartAt?, reservedAt,
               lines: [{ itemId, itemName, itemUnit, warehouseId, warehouseName, toIssue }] }],
    hasMore }
```

- `q`: filtra por el nombre del destino (título de la tarea, nombre de la persona o de la
  sucursal), sin distinguir mayúsculas ni tildes.
- `kind`, `warehouseId`: filtros opcionales. Con `warehouseId`, solo las líneas de ese almacén.
- Página de 5.

**Entregar todo** no es una ruta nueva: es `POST /materials/issue` con todas las líneas del
pedido (`items[]`), que ya existía para los tres destinos, con sus permisos de siempre
(`canOperateTask` en una tarea, `canOperateAccount` en persona o sucursal). En persona o
sucursal cada línea lleva su almacén, para que la salida descuente la reserva de ese almacén.
Las cantidades se pueden corregir o quitar líneas antes de entregar.

## Panel

Pestaña **Pedidos** en Inventario (lazy, como el resto del módulo): buscador, filtro de
destino, de 5 en 5. Cada pedido es una tarjeta con el destino (enlace a su ficha), la fecha de
la tarea si la tiene y sus líneas; **«Entregar todo»** abre el diálogo con las cantidades
editables y entrega en una sola petición.

## Fuera de esta fase

- Albarán en PDF y acta firmada por quien recibe (módulo de firma).
- Recoger: cuadrar un pedido entero de una tarea terminada desde la misma pantalla.

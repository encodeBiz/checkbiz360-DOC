# TDR-004 — Espejo a Postgres desde `inventory`, migración 023 e informes

**Fecha:** 2026-09-28 (revisado el mismo día)
**Estado:** Diseño aprobado
**Componente:** `encodebiz-api` — `inventory`, `analytics` (SyncDimensions), `reports`
**Decisión de referencia:** [ADR-005](../adr/ADR-005-instante-firestore-historico-postgres.md)

---

## 1. Qué se espeja y quién lo escribe

| Origen (Firestore) | Destino (Postgres) | Quién | Cadencia |
|---|---|---|---|
| `items` | `dim_items` | `SyncDimensions` (`analytics`) | Con las demás dimensiones |
| `warehouses` | `dim_warehouses` | ídem | ídem |
| `item_units` | `dim_item_units` | ídem | ídem |
| `item_movements` | `item_movements_raw` | **`inventory`**, en la petición | Inmediata + job |
| `unit_reservations` | `unit_reservations_raw` | **`inventory`**, en cada cambio | Inmediata + job |

**No pasa por `sync`.** `sync` es un receptor pasivo que recibe lo que `firebase_sdk` le empuja,
con timeout corto y un `catch` que solo escribe en el log; y las `dim_*` ni siquiera van por
ahí. Como todas las escrituras de este módulo pasan por `inventory`, es `inventory` quien
inserta. El riesgo de `sync` sin reintentos no toca a este módulo.

## 2. Inserción en la petición

Tras confirmar la transacción de Firestore:

```
INSERT INTO item_movements_raw (...) VALUES (...) ON CONFLICT (movement_id) DO NOTHING;
UPDATE item_movements/{id} SET mirrored = true, mirroredAt = now   -- Firestore
```

**A mejor esfuerzo.** Si Postgres no responde, la petición **no falla**: el movimiento ya está
en Firestore con `mirrored: false`, y el job lo recoge. Nunca dentro de la transacción, nunca
antes del commit: el usuario no espera a Postgres para saber que su apunte existe.

`movement_id` como clave primaria es lo que hace el espejo idempotente.

## 3. Job `remirror`

En `inventory`, cada pocos minutos: consulta `item_movements` con `mirrored == false` ordenado
por `createdAt`, inserta con `ON CONFLICT DO NOTHING` y marca `mirrored: true`. Deja registro de
cuántos recogió y cuántos siguen fallando.

`mirrored` es un **booleano escrito siempre**: Firestore no encuentra campos ausentes, así que
`mirroredAt == null` no serviría como filtro.

## 4. Migración `023`

```sql
-- 023_inventario.sql
CREATE TABLE IF NOT EXISTS dim_warehouses (
  warehouse_id   TEXT PRIMARY KEY,
  entity_id      TEXT NOT NULL,
  name           TEXT NOT NULL,
  scope          TEXT NOT NULL,             -- entity | branches
  branch_ids     TEXT[] NOT NULL DEFAULT '{}',
  status         TEXT NOT NULL,
  synced_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dim_items (
  item_id     TEXT PRIMARY KEY,
  entity_id   TEXT NOT NULL,
  type        TEXT NOT NULL,                -- consumable | operable
  name        TEXT NOT NULL,
  reference   TEXT,
  unit        TEXT,
  unit_cost   NUMERIC(12,4),
  usage_unit  TEXT,                         -- hours | kilometers | days
  active      BOOLEAN NOT NULL DEFAULT true,
  synced_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dim_item_units (
  unit_id       TEXT PRIMARY KEY,
  entity_id     TEXT NOT NULL,
  item_id       TEXT NOT NULL,
  identifier    TEXT,
  warehouse_id  TEXT,
  status        TEXT NOT NULL,              -- available | unavailable | retired
  usage_counter NUMERIC(14,2),
  synced_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS item_movements_raw (
  movement_id      TEXT PRIMARY KEY,        -- el id que generó la app
  entity_id        TEXT NOT NULL,
  type             TEXT NOT NULL,
  item_id          TEXT NOT NULL,
  warehouse_id     TEXT NOT NULL,
  unit_id          TEXT,
  task_id          TEXT,
  branch_id        TEXT,
  quantity         NUMERIC(14,3),           -- siempre positiva; el signo lo da type
  transfer_id      TEXT,
  previous_on_hand NUMERIC(14,3),
  start_at         TIMESTAMPTZ,
  end_at           TIMESTAMPTZ,
  usage_counter    NUMERIC(14,2),
  registered_by    TEXT NOT NULL,
  employee_id      TEXT,
  note             TEXT,
  occurred_at      TIMESTAMPTZ NOT NULL,
  created_at       TIMESTAMPTZ NOT NULL,
  synced_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_movements_entity_occurred ON item_movements_raw (entity_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS ix_movements_task            ON item_movements_raw (task_id);
CREATE INDEX IF NOT EXISTS ix_movements_employee        ON item_movements_raw (entity_id, employee_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS ix_movements_transfer        ON item_movements_raw (transfer_id) WHERE transfer_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS unit_reservations_raw (
  reservation_id  TEXT PRIMARY KEY,
  entity_id       TEXT NOT NULL,
  unit_id         TEXT NOT NULL,
  item_id         TEXT NOT NULL,
  task_id         TEXT NOT NULL,
  branch_id       TEXT,
  start_at        TIMESTAMPTZ NOT NULL,
  end_at          TIMESTAMPTZ NOT NULL,
  status          TEXT NOT NULL,
  released_reason TEXT,
  usage_start     NUMERIC(14,2),
  usage_end       NUMERIC(14,2),
  synced_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Las reservas se **upsertan** (`ON CONFLICT DO UPDATE`): cambian de estado. Los movimientos no.

**La migración se aplica a mano por SSH**, nunca desde el despliegue. En producción, una a una y
mirando el resultado de cada una.

## 4b. Lo que la implementación añadió (2026-09-29)

- `dim_sync_log.dimension` nació con un `CHECK` cerrado a `branches | employees | calendars`; la
  `023` lo reescribe (`DROP` + `ADD`) para admitir `warehouses | items | item_units`.
- `listEntitiesWithData` de `analytics` también mira `item_movements_raw`: una entidad con
  inventario y sin fichajes entra igual en la pasada de dimensiones.
- El espejo va como decorador del repositorio (`MirroredLedger`, `MirroredReservations`) en
  `services/inventory/src/infrastructure/`: la verdad se escribe igual y Postgres no entra en
  `shared`. La reserva se upserta en cada cambio de estado y lleva `updatedAt` para reespejar
  solo lo que cambió.
- `GET /api/reports/inventory/consumption` (JSON) en `reports`, agrupable por artículo, tarea,
  empleado, sucursal o almacén; exige asiento en la empresa como el informe de tareas.

## 5. Frescura declarada

`GET /movements` y el informe de consumo devuelven `staleness` cuando hay movimientos con
`mirrored: false` más viejos que un umbral (p. ej. 15 minutos): cuántos y desde cuándo. Un
informe incompleto que se presenta como completo es peor que no tenerlo.

## 6. Poda

**No se poda nada de Firestore en v1.** Cuando se plantee, la condición es `mirrored: true` y la
tarea cerrada. Podar sin espejo confirmado no es archivar, es borrar.

## 7. Informes

Viven en `reports`, como el informe de tareas:

- **Consumo por periodo**, desglosable por sucursal, empleado, artículo y tarea.
- **Coste de material**: cantidad × `unit_cost` de la ficha. **Sin valoración** —ni FIFO ni
  precio medio ponderado.
- **Ocupación de operables** por periodo, base del futuro mantenimiento por contador de uso.

`GET /api/v1/inventory/movements` sirve el libro paginado desde estas tablas.

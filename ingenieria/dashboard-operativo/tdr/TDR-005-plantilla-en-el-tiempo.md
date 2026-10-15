# TDR-005 — Plantilla en el tiempo: eventos de estado, foto diaria y GET /panel/headcount

**Fecha:** 2026-10-12
**Estado:** Diseño
**Componente:** `services/analytics` — `SyncDimensions` (detección), `application/headcount/*`, `jobs/scheduler.ts`, `scripts/reconstruir-plantilla.ts`; migración `028_plantilla_en_el_tiempo.sql`
**Decisión de referencia:** [ADR-006](../adr/ADR-006-la-plantilla-se-sigue-por-eventos-de-estado.md)

---

## 1. Qué estados se pintan

| Línea | Estados de la ficha |
|---|---|
| Activos | `active`, `vacation`, `sick_leave`, `leave_of_absence`, `paternity_leave`, `maternity_leave` |
| Inactivos | `inactive` |
| Despedidos | `fired` |
| Fuera de la serie | `pending`: ficha a medio hacer, todavía no es plantilla |

Los cinco estados de ausencia cuentan como activos: siguen siendo plantilla, igual que en
disponibilidad (TDR-001 §2.1).

## 2. Migración `028_plantilla_en_el_tiempo.sql`

- `dim_employees` gana `created_at` y `source_updated_at` (el `updatedAt` de la ficha).
- `employee_status_events`: `event_id` (serial), `entity_id`, `employee_id`, `from_status`
  (nulo en el alta), `to_status`, `at`, `source` ∈ `sync_diff | created_at |
  estimated_updated_at | tracking_start`, `recorded_at`. Índices por `(entity_id, at)` y
  `(employee_id, at)`. Único por `(employee_id, to_status, at)` para que repetir sea inocuo.
- `headcount_daily`: `(entity_id, branch_id, day)` como clave, con `'__entity__'` en
  `branch_id` para el total sin duplicar. Columnas `active`, `inactive`, `fired`, `pending`,
  `taken_at`.

## 3. Detección en la sincronización

En `syncEmployees`, antes del upsert se leen de una vez los estados actuales de la entidad en
`dim_employees`. Por cada ficha:

- Si no existía: evento de alta `from_status = NULL`, `to_status = status`, `at = createdAt`,
  `source = created_at`.
- Si existía y el estado cambió: evento `from → to`, `at = NOW()`, `source = sync_diff`.

El upsert guarda además `created_at` y `source_updated_at`.

## 4. Foto diaria

Tarea del planificador a las 00:40 UTC: por cada entidad activa, recuentos por estado desde
`dim_employees`, total de empresa y por centro (`branch_ids`, con el sobreconteo conocido de
quien está en varios). Upsert por clave: repetir el mismo día pisa.

## 5. Reconstrucción del pasado (una vez)

`scripts/reconstruir-plantilla.ts --entity <id> | --all [--apply]`, simula por defecto. Para cada
empleado de `dim_employees` sin ningún evento:

- Alta: `created_at` → evento `NULL → active`, `source = created_at`.
- Si `status = fired`: evento `active → fired` en `source_updated_at` (`estimated_updated_at`).
  Sin `source_updated_at`, en `tracking_start`.
- Si `status = inactive` u otro distinto de activo: evento `active → status` en la fecha de
  arranque (`tracking_start`).

Exige dimensiones frescas: antes, `dimensions/sync`.

## 6. `GET /api/analytics/panel/headcount`

Query: `entityId`, `branchId` opcional, `from` opcional (`YYYY-MM`, por defecto el mes del primer
alta). Misma puerta que `/today`.

Reproduce los eventos de la entidad en orden y cierra cada mes:

```jsonc
{
  "ok": true,
  "months": [
    { "month": "2026-06", "active": 31, "inactive": 0, "fired": 2, "hires": 5, "exits": 1, "estimated": true }
  ],
  "trackingSince": "2026-10-12",
  "dataHealth": {
    "estimatedExits": 9,
    "undatedInactive": 15,
    "note": "Los inactivos sin fecha cuentan como activos hasta trackingSince"
  }
}
```

- `active`/`inactive`/`fired` son personas en ese estado al cierre del mes.
- `hires` = altas del mes; `exits` = pasos a `fired` o `inactive` del mes.
- `estimated` = el mes contiene algún evento de `source` estimada o de arranque.
- Con `branchId`, solo los empleados cuyo `branch_ids` actual lo contiene.

## 7. Verificación

- Tras reconstruir, el último mes de la serie coincide con los recuentos actuales de
  `dim_employees` (activos, inactivos y despedidos).
- Cambiar el estado de una ficha en dev y sincronizar deja un evento `sync_diff`.
- La foto diaria del día cuadra con el último mes de la serie.

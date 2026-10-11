# TDR-003 — Cierre diario y semanas: `operational_daily`, cron por zona, backfill y agregación

**Fecha:** 2026-10-10
**Estado:** Diseño
**Componente:** `services/analytics` — `src/application/CloseOperationalDay.ts`, `src/application/BuildOperationalWeeks.ts`, `src/jobs/closeDayCron.ts`, `src/scripts/cerrar-dias.ts`; migración `027_dashboard_operativo.sql`
**Decisión de referencia:** [ADR-004](../adr/ADR-004-el-historico-se-congela-al-cerrar-el-dia.md)
**Patrón copiado:** `services/reports/src/application/DailyReportCron.ts` (cron horario, cada centro a su hora local)

---

> **Implementado el 2026-10-11 (`1eb7049`).** Cambios respecto a lo de abajo: no se guardan
> `tasks_validated` ni `tasks_rejected` (el cálculo del día no los produce) y se añade
> `untracked_sessions`. La migración real es `encodebiz-api/migrations/027_dashboard_operativo.sql`.

## 1. Qué se congela

Por centro y día, el resultado de `buildOperationalDay(entity, branch, day, asOf = cierre)`:
los totales de los tres bloques y un detalle compacto por persona y por tarea.

```sql
-- 027_dashboard_operativo.sql
-- encodeBiz Analytics — cierre diario del dashboard operativo (ADR-004).
-- Una fila por centro y día. La escribe el cron a las 04:xx locales para el día anterior,
-- el script de backfill para los días anteriores al arranque y `POST /close-day` para
-- rehacer. Se upserta por clave primaria y sube `version`: el pasado sólo cambia a propósito.

CREATE TABLE IF NOT EXISTS operational_daily (
  entity_id               VARCHAR(128)  NOT NULL,
  branch_id               VARCHAR(128)  NOT NULL,
  day                     DATE          NOT NULL,     -- en la zona del centro
  tz                      VARCHAR(80)   NOT NULL,
  closed_day              BOOLEAN       NOT NULL DEFAULT FALSE,  -- nadie debía trabajar

  -- Jornada
  expected                INTEGER,                    -- NULL si no había calendario espejado
  with_log                INTEGER       NOT NULL DEFAULT 0,  -- previstos con jornada aquí
  no_log                  INTEGER       NOT NULL DEFAULT 0,
  late                    INTEGER       NOT NULL DEFAULT 0,
  late_minutes            INTEGER       NOT NULL DEFAULT 0,
  finished                INTEGER       NOT NULL DEFAULT 0,
  incomplete              INTEGER       NOT NULL DEFAULT 0,
  other_branch            INTEGER       NOT NULL DEFAULT 0,
  pending_validation      INTEGER       NOT NULL DEFAULT 0,
  unexpected              INTEGER       NOT NULL DEFAULT 0,
  rejected_attempts       INTEGER       NOT NULL DEFAULT 0,

  -- Coste
  worked_minutes          INTEGER       NOT NULL DEFAULT 0,
  break_minutes           INTEGER       NOT NULL DEFAULT 0,
  labor_cost              NUMERIC(14,2),
  rate_coverage           NUMERIC(5,4),
  material_cost           NUMERIC(14,2),
  material_movements      INTEGER       NOT NULL DEFAULT 0,

  -- Tareas (al cierre)
  tasks_due               INTEGER       NOT NULL DEFAULT 0,
  tasks_completed         INTEGER       NOT NULL DEFAULT 0,
  tasks_completed_on_time INTEGER       NOT NULL DEFAULT 0,
  tasks_completed_late    INTEGER       NOT NULL DEFAULT 0,
  tasks_overdue_open      INTEGER       NOT NULL DEFAULT 0,
  tasks_start_late        INTEGER       NOT NULL DEFAULT 0,
  tasks_validated         INTEGER       NOT NULL DEFAULT 0,
  tasks_rejected          INTEGER       NOT NULL DEFAULT 0,

  -- Detalle compacto para el «ver más» del histórico sin releer el crudo:
  -- { people: [{ employeeId, presence, late, minutesFromShiftStart, workedMinutes, laborCost }],
  --   tasks:  [{ taskId, signals, status }] }
  detail                  JSONB,

  source                  VARCHAR(10)   NOT NULL CHECK (source IN ('close','backfill','manual')),
  as_of                   TIMESTAMPTZ   NOT NULL,     -- el `asOf` con el que se calculó
  version                 INTEGER       NOT NULL DEFAULT 1,
  closed_at               TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  PRIMARY KEY (entity_id, branch_id, day)
);

CREATE INDEX IF NOT EXISTS idx_operational_daily_entity_day
  ON operational_daily (entity_id, day DESC);
```

`with_log` cuenta previstos con jornada **en este centro**: `with_log + no_log + other_branch
= expected` cuando `expected` no es nulo. Las tasas no se guardan: se calculan sobre sumas.

## 2. Cuándo se cierra: 04:xx de la zona del centro

Tarea del planificador de `analytics` (`jobs/scheduler.ts`, `setInterval` sin dependencia
nueva) al minuto :10 de cada hora UTC. En cada tic (`application/operational/CloseDue.ts`):

1. Centros con actividad reciente: `SELECT DISTINCT entity_id, branch_id FROM checklogs_raw
   WHERE synced_at >= NOW() - INTERVAL '30 days'` unido con `dim_branches` activas de esas
   entidades (un centro sin fichajes pero con previstos también se cierra: su `no_log` es el
   dato).
2. Para cada uno, su zona: `dim_branches.tz`, con los mismos fallbacks del TDR-001.
3. Si la hora local es **04**, se cierra **ayer** en esa zona con
   `asOf = ayer 24:00 local + 4 h`. La cola de 4 h recoge jornadas que cruzan la medianoche y
   da margen al saneador horario para marcar `incomplete_workday`.
4. Upsert con `source = 'close'`, `version = version + 1` si ya existía.

¿Por qué 04 y no 02 como `reports`? Para ir **detrás** del saneador y detrás del registro de
jornada: un cierre que acusa «jornada sin cerrar» a alguien a quien el saneador todavía no ha
mirado es una acusación con prisa.

Un tick que falla para un centro escribe en el log y sigue con el resto; el siguiente tick no
lo repite (ya no son las 04). Por eso existe `close-day` y por eso el cron de las 05:xx
reintenta los centros de ayer **sin fila**: un segundo barrido, sólo para los huecos.

## 3. Rehacer un día

`POST /api/analytics/close-day?entityId=&date=&branchId?` (S2S) llama a la misma función con
`source = 'manual'`. Se usa después de corregir un fichaje de un día cerrado o de un backfill
de tareas. Idempotente: pisa y sube `version`.

## 4. Backfill de las ocho semanas

`services/analytics/src/scripts/cerrar-dias.ts --entity <id> | --all --from YYYY-MM-DD --to YYYY-MM-DD [--apply]`.

- Simula por defecto: lista los pares (centro, día) que cerraría y cuántos ya tienen fila.
- Con `--apply`, cierra con `source = 'backfill'` **sin pisar** los días que ya tengan
  `source = 'close'` o `'manual'`.
- `expected` sale del calendario **actual** (`dim_calendars` no tiene historia). Es la
  limitación declarada en [ADR-004](../adr/ADR-004-el-historico-se-congela-al-cerrar-el-dia.md),
  y por eso el día se marca. Para las personas que ficharon, el turno aplicado del propio
  fichaje (`schedule_applied`) es exacto y se usa; sólo el `no_log` depende del calendario actual.
- Orden recomendado en el arranque: backfill de tareas ([TDR-002 §5](./TDR-002-espejo-de-tareas.md))
  **antes** que éste; si no, las semanas reconstruidas salen sin tareas.

## 5. Semanas: `BuildOperationalWeeks`

`GET /panel/weeks` lee `operational_daily` para la entidad (o el centro) desde el lunes de
hace `weeks` semanas hasta ayer, y agrupa:

- **Semana ISO en la zona del centro**: `date_trunc('week', day)` sobre `day`, que ya es
  local. A nivel entidad, cada centro aporta sus días; la semana de entidad es la suma.
- Sumas de todos los contadores; `expected` suma sólo donde no es nulo y `closed_day = false`;
  `workingDays` = días con `closed_day = false`.
- Tasas sobre sumas: `coverage = with_log / expected`, `lateRate = late / with_log`,
  `onTimeRate = tasks_completed_on_time / tasks_completed`. Con denominador 0, `null`.
- `source` de la semana: `close` si todos sus días lo son, `backfill` si todos, `mixed` si
  conviven. `closedDays` = filas presentes; `days` = 7 o los transcurridos para la actual.
- `branches[]` a nivel entidad: la fila compacta por centro y semana (cobertura, retraso, a
  tiempo, coste), que es lo que pinta el ranking.
- `dataHealth.history`: `have` = días con fila en el rango, `need` = días del rango ×
  centros; `warming` mientras `have < need` o mientras todo sea `backfill`.

Una consulta, por clave primaria y rango de fechas. Milisegundos.

## 6. Verificación (fase 3)

- Para la entidad de pruebas, la QA guarda la respuesta de `/today` de ayer a las 23:50 locales;
  tras el cierre, la fila de `operational_daily` tiene los mismos totales (salvo lo que el
  saneador cambió entre medias, que se lista).
- Siete días cerrados suman la semana; `coverage` sale de las sumas.
- `close-day` tras corregir un fichaje: `version = 2`, `source = manual`.
- Backfill: no pisa días `close`; marca `backfill`.
- Casos QA **DAS-06** y **DAS-07**.

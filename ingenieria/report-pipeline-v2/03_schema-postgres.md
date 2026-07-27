# 03 — Schema PostgreSQL

Base de datos: `encodebiz_analytics`  
Motor: PostgreSQL 15+  
Servidor: privado (propiedad de encodeBiz)

---

## Tabla: `checklogs_raw`

Réplica 1:1 de los checklogs de Firestore. Fuente analítica para construir daily reports.

```sql
CREATE TABLE checklogs_raw (
  -- Identificación
  id                    VARCHAR(128)  PRIMARY KEY,   -- Firestore document ID
  entity_id             VARCHAR(128)  NOT NULL,
  branch_id             VARCHAR(128)  NOT NULL,
  employee_id           VARCHAR(128)  NOT NULL,

  -- Tiempo
  timestamp             TIMESTAMPTZ   NOT NULL,       -- timestamp operacional (ajustado)
  real_date_market      TIMESTAMPTZ,                  -- marca horaria real del dispositivo

  -- Tipo y estado
  type                  VARCHAR(20)   NOT NULL        -- 'checkin' | 'checkout' | 'restin' | 'restout'
                          CHECK (type IN ('checkin','checkout','restin','restout')),
  status                VARCHAR(60)   NOT NULL,       -- 'valid' | 'failed' | 'pending-employee-validation' | 'incomplete_workday'
  is_suspect            BOOLEAN       DEFAULT FALSE,
  failed_code           VARCHAR(100),
  checkin_ref           VARCHAR(128),                 -- ID del checkin al que pertenece este log (vincula el ciclo)
  closed                BOOLEAN       DEFAULT FALSE,

  -- Geo
  geo_lat               DOUBLE PRECISION,
  geo_lng               DOUBLE PRECISION,

  -- Dispositivo
  user_agent            TEXT,
  device_trusted        BOOLEAN,

  -- Subcampos analíticos de metadata (únicos campos sincronizados — ver TDR-002 y 05_contratos-api.md)
  schedule_applied      JSONB,                        -- copia de metadata.scheduleApplied
  etz                   VARCHAR(80),                  -- timezone del empleado
  employee_responsibility JSONB,                      -- copia de metadata.employeeResponsibility
  -- metadata JSONB completo excluido: objeto variable, sin queries analíticas directas.
  -- Si se necesita backfill de auditoría completa, añadir la columna en una migración posterior.

  -- Control de sync
  synced_at             TIMESTAMPTZ   DEFAULT NOW(),
  updated_at            TIMESTAMPTZ   DEFAULT NOW()
);

-- Índices operacionales
CREATE INDEX idx_checklogs_entity_branch_ts
  ON checklogs_raw (entity_id, branch_id, timestamp DESC);

CREATE INDEX idx_checklogs_employee_ts
  ON checklogs_raw (employee_id, timestamp DESC);

CREATE INDEX idx_checklogs_real_date
  ON checklogs_raw (entity_id, branch_id, real_date_market DESC)
  WHERE real_date_market IS NOT NULL;

CREATE INDEX idx_checklogs_checkin_ref
  ON checklogs_raw (checkin_ref)
  WHERE checkin_ref IS NOT NULL;
```

---

## Tabla: `task_ratings_raw`

Valoraciones de tareas por empleado. Se sincroniza desde `onWriteTaskRating`.

```sql
CREATE TABLE task_ratings_raw (
  -- Identificación
  id                    VARCHAR(128)  PRIMARY KEY,   -- Firestore task_id + worker_id compuesto
  entity_id             VARCHAR(128)  NOT NULL,
  branch_id             VARCHAR(128),                -- puede ser null si la tarea no tiene branch
  employee_id           VARCHAR(128)  NOT NULL,      -- el trabajador valorado
  task_id               VARCHAR(128)  NOT NULL,

  -- Valoración
  rating                NUMERIC(3,1)  CHECK (rating >= 0 AND rating <= 5),
  rated_by              VARCHAR(128),                -- uid del manager que valoró
  rated_at              TIMESTAMPTZ   NOT NULL,

  -- Contexto de la tarea
  task_name             VARCHAR(500),
  task_status           VARCHAR(80),                 -- 'completed' | 'validated' | etc.
  task_completed_at     TIMESTAMPTZ,

  -- Control de sync
  synced_at             TIMESTAMPTZ   DEFAULT NOW()
);

CREATE INDEX idx_ratings_entity_employee_date
  ON task_ratings_raw (entity_id, employee_id, rated_at DESC);

CREATE INDEX idx_ratings_entity_branch_date
  ON task_ratings_raw (entity_id, branch_id, rated_at DESC)
  WHERE branch_id IS NOT NULL;

CREATE INDEX idx_ratings_task
  ON task_ratings_raw (task_id);
```

---

## Tabla: `daily_reports`

Reportes diarios pre-computados, enriquecidos con task ratings. Fuente para el frontend y la IA.

```sql
CREATE TABLE daily_reports (
  -- Identificación determinista
  id                    VARCHAR(200)  PRIMARY KEY,   -- {entityId}_{branchId}_{yyyyMMdd}
  entity_id             VARCHAR(128)  NOT NULL,
  branch_id             VARCHAR(128)  NOT NULL,
  date                  DATE          NOT NULL,

  -- Métricas de horas y costos
  worked_hours          NUMERIC(10,4) DEFAULT 0,
  effective_hours       NUMERIC(10,4) DEFAULT 0,
  total_cost            NUMERIC(12,2) DEFAULT 0,

  -- Métricas operacionales
  employees_count       INTEGER       DEFAULT 0,
  avg_distance          NUMERIC(10,2) DEFAULT 0,
  irregular_events      INTEGER       DEFAULT 0,
  failed_checklogs      INTEGER       DEFAULT 0,
  valid_checklogs       INTEGER       DEFAULT 0,
  suspect_rate          NUMERIC(5,4)  DEFAULT 0,    -- 0.0000 – 1.0000
  count_suspects        INTEGER       DEFAULT 0,

  -- Horario promedio
  avg_start_checklogs   NUMERIC(5,2),               -- ej: 8.50 = 08:30
  avg_end_checklogs     NUMERIC(5,2),

  -- Puntualidad (branch)
  on_time_checkins      INTEGER       DEFAULT 0,
  total_checkins        INTEGER       DEFAULT 0,
  late_minutes_sum_in   NUMERIC(10,2) DEFAULT 0,
  first_checkin_utc     TIMESTAMPTZ,

  on_time_checkouts     INTEGER       DEFAULT 0,
  total_checkouts       INTEGER       DEFAULT 0,
  late_minutes_sum_out  NUMERIC(10,2) DEFAULT 0,
  last_checkout_utc     TIMESTAMPTZ,

  start_hour_applied    NUMERIC(5,2),
  end_hour_applied      NUMERIC(5,2),
  tz                    VARCHAR(80),

  -- Task ratings integrados (NUEVO)
  avg_task_rating       NUMERIC(3,2),               -- NULL si no hay ratings ese día
  tasks_completed       INTEGER       DEFAULT 0,
  tasks_rated           INTEGER       DEFAULT 0,

  -- Breakdown por empleado (JSON array de DailyEmployeeReportV2)
  employees             JSONB,

  -- Control
  computed_at           TIMESTAMPTZ   DEFAULT NOW(),
  updated_at            TIMESTAMPTZ   DEFAULT NOW(),

  CONSTRAINT unique_daily_report UNIQUE (entity_id, branch_id, date)
);

CREATE INDEX idx_daily_reports_entity_branch_date
  ON daily_reports (entity_id, branch_id, date DESC);

CREATE INDEX idx_daily_reports_entity_date
  ON daily_reports (entity_id, date DESC);
```

---

## Tabla: `pattern_snapshots`

Fotografía del patrón (BranchPattern) capturada una vez al día por branch. Deduplicada por fecha.

```sql
CREATE TABLE pattern_snapshots (
  -- Identificación
  id                    BIGSERIAL     PRIMARY KEY,
  entity_id             VARCHAR(128)  NOT NULL,
  branch_id             VARCHAR(128)  NOT NULL,
  snapshot_date         DATE          NOT NULL,

  -- Indicadores temporales (del BranchPattern actual)
  avg_start_hour        NUMERIC(5,2),               -- ej: 8.50 = 08:30
  avg_end_hour          NUMERIC(5,2),
  std_start_hour        NUMERIC(5,4),               -- desviación típica
  std_end_hour          NUMERIC(5,4),

  -- Fiabilidad y masa de datos
  reliability           NUMERIC(5,4),               -- 0.0000 – 1.0000
  data_points           INTEGER,

  -- Economía
  avg_cost_efficiency   NUMERIC(5,4),
  cost_variance         NUMERIC(10,4),
  avg_cycle_cost        NUMERIC(12,2),
  avg_effective_cost    NUMERIC(12,2),
  effective_real_cost   NUMERIC(12,2),
  cost_trend            VARCHAR(10),                -- 'up' | 'down' | '-'

  -- Task rating integrado en el patrón (NUEVO)
  avg_task_rating_30d   NUMERIC(3,2),               -- media móvil de los últimos 30 días en el momento del snapshot
  tasks_rated_30d       INTEGER,

  -- Patrones semanales (JSON arrays de 7 elementos, Dom=0, Sáb=6)
  weekly_start_avg      JSONB,
  weekly_end_avg        JSONB,
  weekly_work_avg       JSONB,

  -- Indicadores heurísticos calculados ese día
  heuristic_scores      JSONB,                      -- { WTB: 8.5, OSD: 0.5, HCI: 0.72, ... }

  -- Snapshot completo del patrón para auditoria
  raw_pattern           JSONB,

  -- Control
  created_at            TIMESTAMPTZ   DEFAULT NOW(),

  CONSTRAINT unique_pattern_snapshot UNIQUE (entity_id, branch_id, snapshot_date)
);

CREATE INDEX idx_pattern_snapshots_entity_branch_date
  ON pattern_snapshots (entity_id, branch_id, snapshot_date DESC);

CREATE INDEX idx_pattern_snapshots_entity_date
  ON pattern_snapshots (entity_id, snapshot_date DESC);
```

---

## Tabla: `sync_log`

Auditoría de syncs Firebase → PostgreSQL para detectar fallos y reintento.

```sql
CREATE TABLE sync_log (
  id                    BIGSERIAL     PRIMARY KEY,
  source                VARCHAR(50)   NOT NULL,     -- 'checklog' | 'task_rating' | 'daily_report'
  source_id             VARCHAR(200)  NOT NULL,     -- ID del documento sincronizado
  entity_id             VARCHAR(128),
  status                VARCHAR(20)   NOT NULL,     -- 'success' | 'failed' | 'retrying'
  error_message         TEXT,
  synced_at             TIMESTAMPTZ   DEFAULT NOW()
);

CREATE INDEX idx_sync_log_status ON sync_log (status, synced_at DESC);
CREATE INDEX idx_sync_log_source ON sync_log (source, source_id);
```

---

## Vistas analíticas (para uso futuro en dashboards internos)

```sql
-- Tendencia de puntualidad por branch, últimos 30 días
CREATE VIEW v_branch_punctuality_trend AS
SELECT
  entity_id,
  branch_id,
  date,
  CASE WHEN total_checkins > 0
    THEN ROUND(on_time_checkins::NUMERIC / total_checkins, 4)
    ELSE NULL
  END AS punctuality_rate,
  late_minutes_sum_in,
  avg_task_rating
FROM daily_reports
WHERE date >= CURRENT_DATE - INTERVAL '30 days';

-- Evolución de reliability por branch
CREATE VIEW v_branch_reliability_trend AS
SELECT
  entity_id,
  branch_id,
  snapshot_date,
  reliability,
  data_points,
  avg_task_rating_30d,
  cost_trend
FROM pattern_snapshots
ORDER BY entity_id, branch_id, snapshot_date ASC;  -- ASC requerido por TrendAnalyzer (TDR-005)
```

---

## Notas de operación

- **Backup:** Daily pg_dump a S3/storage externo. Los datos en Firebase son el respaldo secundario.
- **Retención:** `checklogs_raw` y `daily_reports`: 5 años. `sync_log`: 90 días (purge automático).
- **Conexión desde Firebase:** La Cloud Function usa la URL del servidor privado via variable de entorno `ANALYTICS_SERVER_URL`. La comunicación usa HTTPS con API key compartida en header `X-Encodebiz-Key`.

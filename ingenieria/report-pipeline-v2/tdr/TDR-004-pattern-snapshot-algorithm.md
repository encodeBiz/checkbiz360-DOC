# TDR-004 — Algoritmo de captura de Pattern Snapshots

**Fecha:** 2026-06-02  
**Estado:** Diseño aprobado, pendiente implementación (Fase 3)  
**Componente:** Servidor privado — parte del flujo `POST /api/build/daily-report`

---

## Problema

El `BranchPattern` en Firestore es un documento mutable. Cada checkout válido actualiza el patrón via EMA. Para preservar la historia necesitamos capturar el estado del patrón una vez al día. La pregunta es qué capturar exactamente, cómo integrarlo con el daily report, y cómo garantizar que sea reproducible.

---

## Qué es un PatternSnapshot

Un snapshot es una **fotografía del BranchPattern en el momento de las 02:00 locales**, enriquecida con:
1. Los indicadores heurísticos calculados sobre ese patrón ese día
2. Las métricas del DailyReport del mismo día (puntualidad, task ratings)
3. La media móvil de task ratings de los últimos 30 días (no solo el día)

No es el BranchPattern raw de Firestore simplemente copiado. Es una composición de tres fuentes: patrón actual, daily report del día, e historial de ratings.

---

## Fuentes de datos para el snapshot

### Fuente 1: BranchPattern (recibido del Cloud Function)

El Cloud Function incluye el `currentPattern` en el body del request a `/api/build/daily-report`. Este es el patrón más actualizado disponible en el momento de la llamada (puede tener ciclos del día en curso que llegaron tarde, pero en esencia es el patrón "de cierre del día").

Campos extraídos:
```
avgStartHour, avgEndHour, stdStartHour, stdEndHour
reliability, dataPoints
avgCostEfficiency, costVariance, avgCycleCost, avgEffectiveCost, effectiveRealCost
costTrend
weeklyStartAvg[7], weeklyEndAvg[7], weeklyWorkAvg[7]
```

### Fuente 2: DailyReport del mismo día (recién construido)

Calculado en el paso anterior (TDR-003). Extraemos:
```
onTimeCheckins, totalCheckins → puntualidad rate del día
lateMinutesSumIn              → minutos medios de retraso
avgTaskRating                 → media de ratings del día
```

### Fuente 3: Media móvil de ratings de los últimos 30 días (PostgreSQL)

```sql
SELECT
  AVG(avg_task_rating) FILTER (WHERE avg_task_rating IS NOT NULL) AS avg_rating_30d,
  SUM(tasks_rated) AS tasks_rated_30d
FROM daily_reports
WHERE entity_id = $entityId
  AND branch_id = $branchId
  AND date >= CURRENT_DATE - INTERVAL '30 days'
  AND date < $targetDate;
```

Esto da el contexto de largo plazo para el campo `avg_task_rating_30d` del snapshot.

---

## Cálculo de heuristic_scores en el snapshot

Los indicadores heurísticos (WTB, OSD, HCI, OSI, PSS, etc.) se calculan sobre el `BranchPattern` usando la misma lógica que `HeuristicCalculator`. En Fase 3 se replica esta lógica en el servidor privado (o se llama a un endpoint de Firebase que los calcula, pero esto añade latencia y dependencia innecesaria).

La lógica de `HeuristicCalculator.computeBranch()` es matemática pura sin efectos laterales. Se puede portar directamente al servidor privado en TypeScript/Node.

Los scores se guardan como JSONB en `pattern_snapshots.heuristic_scores`:
```json
{
  "WTB": 8.91,
  "OSD": 0.40,
  "HCI": 0.78,
  "OSI": 0.74,
  "PSS": 0.76,
  "RCV": 0.12,
  "CVH": 0.08,
  "CPD": -2.3,
  "CRI": 0.03,
  "OER": 0.88,
  "ECR": 0.45,
  "ERP": 0.71,
  "ROIh": 0.09,
  "CEE": -0.06,
  "WLB": 7.32,
  "SSR": 0.75,
  "GHI": 0.58,
  "QHI": 0.64
}
```

Guardar los scores junto con el snapshot permite ver cómo evolucionó cada indicador a lo largo del tiempo sin necesidad de re-calcularlos.

---

## Algoritmo completo de construcción del snapshot

```typescript
async function buildPatternSnapshot(
  entityId: string,
  branchId: string,
  targetDate: string,        // "2026-06-01"
  currentPattern: BranchPattern,
  dailyReport: DailyReportEnriched,
  db: PostgresClient
): Promise<PatternSnapshotInsert> {

  // 1. Media móvil de ratings 30 días
  const { avg_rating_30d, tasks_rated_30d } = await db.queryOne(`
    SELECT
      AVG(avg_task_rating) FILTER (WHERE avg_task_rating IS NOT NULL) AS avg_rating_30d,
      COALESCE(SUM(tasks_rated), 0) AS tasks_rated_30d
    FROM daily_reports
    WHERE entity_id = $1 AND branch_id = $2
      AND date >= $3::date - INTERVAL '30 days'
      AND date < $3::date
  `, [entityId, branchId, targetDate]);

  // 2. Calcular heuristic scores
  const calculator = new HeuristicCalculator(currentPattern);
  const INDICATORS = ["WTB","OSD","HCI","OSI","PSS","RCV","CVH","CPD","CRI","OER","ECR","ERP","ROIh","CEE","WLB","SSR","GHI","QHI"];
  const heuristicScores: Record<string, number> = {};
  for (const id of INDICATORS) {
    const val = calculator.computeBranch(id);
    if (val !== null) heuristicScores[id] = val;
  }

  // 3. Construir el snapshot
  return {
    entity_id: entityId,
    branch_id: branchId,
    snapshot_date: targetDate,

    avg_start_hour: currentPattern.avgStartHour,
    avg_end_hour: currentPattern.avgEndHour,
    std_start_hour: currentPattern.stdStartHour,
    std_end_hour: currentPattern.stdEndHour,
    reliability: currentPattern.reliability,
    data_points: currentPattern.dataPoints,
    avg_cost_efficiency: currentPattern.avgCostEfficiency ?? null,
    cost_variance: currentPattern.costVariance ?? null,
    avg_cycle_cost: currentPattern.avgCycleCost ?? null,
    avg_effective_cost: currentPattern.avgEffectiveCost ?? null,
    effective_real_cost: currentPattern.effectiveRealCost ?? null,
    cost_trend: currentPattern.costTrend ?? null,

    avg_task_rating_30d: avg_rating_30d ?? null,
    tasks_rated_30d: tasks_rated_30d ?? 0,

    weekly_start_avg: JSON.stringify(currentPattern.weeklyStartAvg),
    weekly_end_avg: JSON.stringify(currentPattern.weeklyEndAvg),
    weekly_work_avg: JSON.stringify(currentPattern.weeklyWorkAvg),

    heuristic_scores: JSON.stringify(heuristicScores),
    raw_pattern: JSON.stringify(currentPattern),
  };
}
```

---

## Idempotencia

```sql
INSERT INTO pattern_snapshots (entity_id, branch_id, snapshot_date, ...)
VALUES ($1, $2, $3, ...)
ON CONFLICT (entity_id, branch_id, snapshot_date)
DO UPDATE SET
  reliability = EXCLUDED.reliability,
  avg_task_rating_30d = EXCLUDED.avg_task_rating_30d,
  heuristic_scores = EXCLUDED.heuristic_scores,
  raw_pattern = EXCLUDED.raw_pattern,
  -- Campos estáticos del patrón también se actualizan
  avg_start_hour = EXCLUDED.avg_start_hour,
  avg_end_hour = EXCLUDED.avg_end_hour;
```

Si el batch de 02:00 se re-ejecuta por error el mismo día, el UPSERT actualiza el snapshot existente con los datos más recientes. No crea duplicados.

---

## Cuándo NO se crea snapshot

- Si no hay checklogs para la branch ese día → no hay daily report → no hay snapshot
- Si el BranchPattern no existe en Firestore para esa branch → el request body no trae `currentPattern` → se loguea y se omite el snapshot (no bloquea el daily report)

Este segundo caso es raro (una branch sin patrón es una branch muy nueva), pero es importante no fallar el daily report por ausencia de patrón.

---

## Recuperación de snapshots faltantes

Si la Fase 3 falla un día concreto para una branch, el snapshot queda vacío para esa fecha. Para recuperarlo manualmente:

1. Llamar a `branchRepo.findPatternByBranch(branchId)` en Firestore para obtener el patrón actual
2. Llamar a `/api/patterns/history/backfill` (endpoint de utilidad en el servidor privado) con la fecha y el patrón
3. El endpoint crea el snapshot para esa fecha usando el patrón actual como aproximación (no es el patrón exacto de ese día, pero es mejor que un hueco)

Este endpoint de backfill es utilitario y no tiene contrato formal; se implementa en la herramienta de operaciones interna.

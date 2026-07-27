# TDR-005 — Algoritmo TrendAnalysis: cálculo de tendencias con datos escasos

**Fecha:** 2026-06-02
**Estado:** ⚠️ **Núcleo de cálculo sustituido por [TDR-007](./TDR-007-drift-based-trend-engine.md)**
(2026-07-24) — la comparación de medias por mitades no detectaba derivas lentas y sostenidas
(caso real documentado en TDR-007). Se mantienen de este documento: el concepto de `confidence` por
métrica, las bandas de `dataQuality`, la lógica de `recoverySignal` y el principio de umbral relativo
por métrica — todos heredados en TDR-007. Este documento queda como referencia histórica de la
decisión original.
**Componente:** `functions/src/services-saas/checkinbiz/application/heuristic/TrendAnalyzer.ts`
(nota: la implementación real vive en `encodebiz-api/packages/shared`, no en Firebase Functions — ver
TDR-007 para el porqué)

---

## Problema

El historial de pattern snapshots puede tener entre 7 y 90+ días de datos. El algoritmo de tendencias debe:

1. Funcionar correctamente con tan solo 7 días de datos (mínimo de Fase 4)
2. Dar señales fiables con 30+ días (el escenario habitual)
3. No generar falsos positivos (decir "mejora" cuando hay ruido aleatorio)
4. Ser determinista: mismos datos → mismo resultado

Los algoritmos estadísticos sofisticados (regresión lineal, series temporales ARIMA) son excesivos para este volumen. Necesitamos algo robusto pero simple.

---

## Decisión: comparación de medias por mitades con umbral relativo

### Algoritmo base

Para cada métrica con N snapshots ordenados cronológicamente (más antiguo primero):

```typescript
function computeTrend(
  snapshots: PatternSnapshot[],
  accessor: (s: PatternSnapshot) => number | null,
  options: { higherIsBetter: boolean; threshold?: number }
): TrendResult {
  const { higherIsBetter, threshold = 0.05 } = options;

  const values = snapshots
    .map(accessor)
    .filter((v): v is number => v !== null && isFinite(v));

  if (values.length < 6) {
    return { direction: "stable", confidence: "insufficient", delta: 0, deltaPercent: 0 };
  }

  const mid = Math.floor(values.length / 2);
  const olderHalf = values.slice(0, mid);   // primera mitad = más antiguo
  const newerHalf = values.slice(mid);       // segunda mitad = más reciente

  const avgOlder = mean(olderHalf);
  const avgNewer = mean(newerHalf);

  if (avgOlder === 0) {
    return { direction: "stable", confidence: "low", delta: 0, deltaPercent: 0 };
  }

  const delta = avgNewer - avgOlder;
  const deltaPercent = Math.abs(delta / avgOlder);
  const isImproving = higherIsBetter ? delta > 0 : delta < 0;

  let direction: "improving" | "declining" | "stable";
  if (deltaPercent < threshold) {
    direction = "stable";
  } else if (isImproving) {
    direction = "improving";
  } else {
    direction = "declining";
  }

  const confidence: "high" | "medium" | "low" | "insufficient" =
    values.length >= 21 ? "high" :
    values.length >= 14 ? "medium" : "low";

  return { direction, confidence, delta, deltaPercent };
}
```

### Por qué comparación de mitades y no regresión lineal

La regresión lineal ajusta una recta a todos los puntos y usa la pendiente como indicador de tendencia. Es perfecta cuando los datos son continuos y lineales.

El problema con los patrones de asistencia es que son **ruidosos por naturaleza**. Un lunes con 5 empleados enfermos distorsiona la semana. La media de mitades es más resistente a outliers que la pendiente de regresión, porque el impacto de un outlier queda diluido en la media de su mitad.

---

## Métricas que se analizan y su dirección "buena"

| Métrica | Fuente | Higher is better | Threshold |
|---------|--------|-----------------|-----------|
| `reliability` | pattern | Sí | 5% |
| `punctualityRateIn` | daily_reports | Sí | 5% |
| `lateMinutesSumIn` | daily_reports | No (menos es mejor) | 10% |
| `punctualityRateOut` | daily_reports | Sí | 5% |
| `lateMinutesSumOut` | daily_reports | No | 10% |
| `avgTaskRating30d` | pattern_snapshots | Sí | 3% (escala 1-5, más sensible) |
| `avgCostEfficiency` | pattern | Sí | 5% |
| `costVariance` | pattern | No (menos es mejor) | 8% |
| `hci` (HCI score) | heuristic_scores | Sí | 5% |

`lateMinutesSumIn` usa un threshold mayor (10%) porque la varianza diaria es alta (puede haber 0 retrasos un día y 30 minutos otro). Un 5% de threshold generaría falsos positivos constantes.

---

## Métricas derivadas

### punctualityRateIn por día

No está directamente en `pattern_snapshots` pero se puede calcular desde `daily_reports`:

```sql
SELECT
  date,
  CASE WHEN total_checkins > 0
    THEN on_time_checkins::FLOAT / total_checkins
    ELSE NULL
  END AS punctuality_rate_in
FROM daily_reports
WHERE entity_id = $1 AND branch_id = $2
ORDER BY date ASC;
```

### consistencyScore del patrón a lo largo del tiempo

Mide qué tan estable es `reliability` en el período analizado:

```typescript
function computeVolatility(values: number[]): "high" | "medium" | "low" {
  const std = standardDeviation(values);
  if (std > 0.15) return "high";
  if (std > 0.07) return "medium";
  return "low";
}
```

Alta volatilidad de `reliability` significa que el patrón salta entre estados: unos días bien, otros mal. Esto es una señal de gestión deficiente o alta rotación de empleados.

---

## Señal de recuperación (recoverySignal)

Se activa cuando en los últimos 7 días la tendencia invierte después de una tendencia negativa:

```typescript
function detectRecovery(
  snapshots: PatternSnapshot[],
  accessor: (s: PatternSnapshot) => number | null,
  higherIsBetter: boolean
): boolean {
  if (snapshots.length < 14) return false;

  const last7 = snapshots.slice(-7);
  const previous7 = snapshots.slice(-14, -7);

  const avgLast7 = mean(last7.map(accessor).filter(notNull));
  const avgPrev7 = mean(previous7.map(accessor).filter(notNull));

  const globalTrend = computeTrend(snapshots, accessor, { higherIsBetter });

  // Hay recuperación si la tendencia global es negativa PERO los últimos 7 días mejoran
  const recentImproves = higherIsBetter ? avgLast7 > avgPrev7 : avgLast7 < avgPrev7;
  return globalTrend.direction === "declining" && recentImproves;
}
```

---

## Estructura completa del TrendAnalysis

```typescript
interface TrendAnalysis {
  daysAvailable: number;
  dataQuality: "rich" | "moderate" | "insufficient";  // rich: >=21, moderate: 7-20, insufficient: <7

  reliability: TrendResult;
  punctualityIn: TrendResult;
  punctualityOut: TrendResult;
  lateMinutesIn: TrendResult;
  lateMinutesOut: TrendResult;
  taskRating: TrendResult | null;     // null si no hay ratings en el período
  costEfficiency: TrendResult;
  costVariance: TrendResult;

  volatility: "high" | "medium" | "low";
  consistencyScore: number;           // 0-1: 1-std(reliability)/max_std
  recoverySignal: boolean;

  // Valores absolutos de referencia (para el prompt de IA)
  currentReliability: number;
  currentPunctualityRateIn: number | null;
  currentAvgTaskRating: number | null;
  currentCostEfficiency: number | null;
}

interface TrendResult {
  direction: "improving" | "declining" | "stable";
  confidence: "high" | "medium" | "low" | "insufficient";
  delta: number;          // cambio absoluto (newerAvg - olderAvg)
  deltaPercent: number;   // cambio relativo (0-1)
}
```

---

## Mínimos de datos para cada análisis

| Análisis | Mínimo de snapshots | Comportamiento si < mínimo |
|----------|--------------------|-----------------------------|
| Tendencia básica | 6 | `direction: "stable"`, `confidence: "insufficient"` |
| Media de mitades | 6 | Igual que arriba |
| Volatilidad | 7 | Se omite (null en el resultado) |
| recoverySignal | 14 | `false` siempre |
| Alta confianza | 21 | `confidence: "high"` |

Con < 6 snapshots, `TrendAnalysis` retorna `dataQuality: "insufficient"` y el caller (`analyzeHeuristic`) devuelve solo los indicadores actuales sin contexto temporal. El frontend puede mostrar "insuficiente historia para análisis de tendencias" si `dataQuality === "insufficient"`.

---

## Notas sobre datos faltantes (huecos)

Si hay un hueco en el historial (branch sin actividad un día → sin snapshot), los arrays de valores tendrán null. La función `accessor` retorna null, y el filtro `filter(notNull)` los excluye del cálculo. Los huecos ocasionales (1-2 días por mes) no afectan materialmente las tendencias.

Si hay huecos sistemáticos (la branch opera solo lunes-viernes), la ventana de 30 días tendrá solo ~22 snapshots. Esto es normal y el algoritmo lo maneja correctamente. `daysAvailable` refleja el número real de snapshots, no los días de calendario.

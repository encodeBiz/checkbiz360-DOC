# 06 — Upgrade del Motor de IA

## El problema actual

`HeuristicCore` analiza un BranchPattern que es un **snapshot plano** de estadísticas acumuladas. No sabe nada sobre la evolución temporal.

Cuando dice "la puntualidad es baja", no puede añadir:
- ¿Es nueva o lleva semanas así?
- ¿Empeoró después de un cambio de horario?
- ¿El task rating ha subido mientras la puntualidad baja? (un empleado puede llegar tarde pero trabajar muy bien)
- ¿Hay una tendencia de recuperación?

Sin ese contexto, el análisis es descriptivo, no predictivo ni accionable. Un cliente con acceso a la IA debería recibir **insights que no podría calcular mirando los datos él mismo**.

---

## Nuevo flujo del análisis IA

```
analyzeHeuristic(request)
  │
  ├─► [1] Fetch current BranchPattern (Firestore, igual que ahora)
  │
  ├─► [2] Fetch patternHistory (PostgreSQL via servidor privado)
  │        GET /api/patterns/history?days=30
  │        → array de PatternSnapshot ordenados por fecha
  │
  ├─► [3] ComputeTrend(patternHistory) → TrendAnalysis
  │        Calcula tendencias de cada indicador clave
  │
  ├─► [4] HeuristicCore V2.analyzeBranchV2(pattern, trends)
  │        → indicadores actuales (igual que V1)
  │        → resultados enriquecidos con contexto de tendencia
  │
  └─► [5] Response con results + trend + narrative context
```

---

## TrendAnalysis: qué se computa

```typescript
interface TrendAnalysis {
  daysAvailable: number;           // cuántos días de historia hay
  dataQuality: "rich" | "moderate" | "insufficient";
                                   // rich: >= 21 días, moderate: 7-20, insufficient: < 7

  // Tendencias (últimos N días vs N anteriores)
  reliability: TrendDirection;     // "improving" | "declining" | "stable"
  punctualityIn: TrendDirection;   // basado en on_time_checkins/total_checkins
  punctualityOut: TrendDirection;
  lateMinutesIn: TrendDirection;   // tendencia de minutos de retraso
  taskRating: TrendDirection | "no_data";
  costEfficiency: TrendDirection;
  costVariance: TrendDirection;    // si sube = más volátil (malo)

  // Cuantificaciones
  reliabilityDelta: number;        // cambio en reliability (hoy vs hace 14 días)
  punctualityRateDelta: number;    // cambio en tasa de puntualidad (0-1)
  taskRatingDelta: number | null;  // cambio en rating medio
  lateMinutesDelta: number;        // cambio en minutos medios de retraso

  // Señales especiales
  volatilityAlert: boolean;        // true si std de reliability > 0.15 en 30d
  consistencyScore: number;        // 0-1: cuán estable es el patrón en el tiempo
  recoverySignal: boolean;         // true si declining → improving en últimos 7d
}

type TrendDirection = "improving" | "declining" | "stable";
```

### Algoritmo de tendencia

Divide el historial en dos mitades (primera mitad vs segunda mitad) y compara las medias:

```typescript
function computeTrendForMetric(
  history: PatternSnapshot[],
  accessor: (s: PatternSnapshot) => number | null
): TrendDirection {
  const values = history
    .map(accessor)
    .filter((v): v is number => v !== null);
  
  if (values.length < 6) return "stable"; // datos insuficientes para tendencia

  const mid = Math.floor(values.length / 2);
  const older = values.slice(mid);          // primera mitad = más antiguo
  const newer = values.slice(0, mid);       // segunda mitad = más reciente

  const avgOlder = avg(older);
  const avgNewer = avg(newer);
  const delta = avgNewer - avgOlder;
  const threshold = Math.abs(avgOlder) * 0.05; // 5% de cambio = señal

  if (delta > threshold) return "improving";
  if (delta < -threshold) return "declining";
  return "stable";
}
```

---

## Rediseño del prompt de IA

El motor actual no usa un LLM — usa un motor de reglas heurísticas con thresholds definidos en Firestore (`HeuristicEvaluator`). El "prompt de IA" es en realidad la forma en que se construye el contexto que se le pasa al evaluador y, si hay un LLM en el futuro, el texto que se genera.

### V1 (actual) — lo que el evaluador recibe

```
Indicador WTB: 8.91  → threshold: >8 = "success"
Indicador HCI: 0.72  → threshold: between 0.6-0.8 = "warning"
...
```

Cada indicador se evalúa de forma aislada. El evaluador no sabe que HCI mejoró desde 0.55 hace dos semanas.

### V2 — contexto enriquecido para el evaluador

**Nuevo campo en `HeuristicIndicator` (Firestore):**
```typescript
interface HeuristicIndicatorV2 extends HeuristicIndicator {
  trendModifiers?: {
    improving: { severityAdjust: -1 | 0 | 1; noteKey: string };
    declining:  { severityAdjust: -1 | 0 | 1; noteKey: string };
  };
}
```

Cuando se evalúa un indicador en zona "warning", pero la tendencia es "improving", se puede bajar la severidad y agregar una nota contextual.

**Estructura de resultado V2:**
```typescript
interface HeuristicResultV2 {
  id: string;
  value: number;
  severity: "success" | "warning" | "error" | "info";
  label: { es: string; en: string };
  consequence: { es: string; en: string };
  action: { es: string; en: string };

  // NUEVO: contexto temporal
  trend?: TrendDirection;
  trendNote?: { es: string; en: string };
  historicalContext?: {
    daysAnalyzed: number;
    valueNDaysAgo: number;
    delta: number;
    deltaPercent: number;
  };
}
```

**Ejemplo de resultado enriquecido:**
```json
{
  "id": "HCI",
  "value": 0.72,
  "severity": "warning",
  "label": { "es": "Índice de Confianza Heurística" },
  "consequence": { "es": "El patrón no está completamente consolidado" },
  "action": { "es": "Continuar acumulando ciclos de trabajo" },
  "trend": "improving",
  "trendNote": {
    "es": "En mejora: era 0.55 hace 14 días (+31%). La confianza se está consolidando progresivamente."
  },
  "historicalContext": {
    "daysAnalyzed": 14,
    "valueNDaysAgo": 0.55,
    "delta": 0.17,
    "deltaPercent": 31
  }
}
```

---

## Narrativa de tendencias (nivel branch)

Además de los resultados por indicador, el response incluye una sección de narrativa general:

```typescript
interface BranchNarrative {
  summary: { es: string; en: string };    // 2-3 frases resumiendo el estado + evolución
  highlights: Array<{ es: string; en: string }>;  // 2-4 puntos destacados
  alerts: Array<{ es: string; en: string }>;      // señales preocupantes si las hay
  positives: Array<{ es: string; en: string }>;   // tendencias positivas
}
```

La narrativa se genera con reglas deterministas (no LLM) combinando:
- Severidad de los indicadores actuales
- Tendencias de los últimos 14-30 días
- Presencia de señales especiales (volatilityAlert, recoverySignal)
- Task rating trend (si hay datos)

**Ejemplo de narrativa generada:**
```json
{
  "summary": {
    "es": "La sucursal muestra un patrón operacional en consolidación. La fiabilidad mejora consistentemente (+31% en 14 días), aunque la puntualidad de entrada mantiene un retraso medio de 12 minutos. Las valoraciones de tareas (4.2/5) son el punto más sólido del período."
  },
  "highlights": [
    { "es": "Confianza del patrón en crecimiento sostenido desde hace 2 semanas" },
    { "es": "Valoración de tareas por encima de la media del sector (4.2/5)" }
  ],
  "alerts": [
    { "es": "Retraso medio de entrada aumentó 3 minutos en los últimos 7 días" }
  ],
  "positives": [
    { "es": "Tasa de checkouts puntualidad: 100% en los últimos 5 días" }
  ]
}
```

---

## Preparación para LLM futuro

Si en el futuro se integra un LLM (Claude API), el contexto ya estará estructurado para pasarlo directamente. El prompt sería:

```
Eres un analista operacional de encodeBiz. 
Analiza los siguientes datos de la sucursal y genera un informe ejecutivo en {lang}.

ESTADO ACTUAL:
{JSON.stringify(heuristicResults)}

TENDENCIAS (últimos {daysAvailable} días):
- Fiabilidad del patrón: {reliability} ({reliabilityDelta > 0 ? "↑" : "↓"} {abs(reliabilityDelta*100)}%)
- Puntualidad entrada: {punctualityIn} ({punctualityRateDelta > 0 ? "↑" : "↓"} {abs(punctualityRateDelta*100)}%)
- Valoración de tareas: {taskRatingTrend} (media: {avgTaskRating}/5)
- Variabilidad de costos: {costVariance}

SEÑALES ESPECIALES:
{volatilityAlert ? "⚠️ Alta volatilidad detectada en el patrón" : ""}
{recoverySignal ? "✅ Señal de recuperación activa (mejora en últimos 7 días)" : ""}

Genera:
1. Un resumen ejecutivo (3-4 frases)
2. Los 3 puntos de acción más importantes con justificación histórica
3. Una proyección a 14 días si las tendencias actuales continúan
```

---

## Métricas de éxito del upgrade de IA

| Métrica | V1 (actual) | V2 (objetivo) |
|---------|-------------|---------------|
| Contexto temporal | Ninguno | 7-30 días |
| Task ratings en análisis | No | Sí |
| Severidad ajustada por tendencia | No | Sí |
| Narrativa generada | No | Sí (reglas) |
| Preparado para LLM | No | Sí |
| Datos mínimos para activar tendencias | — | 7 días de snapshots |

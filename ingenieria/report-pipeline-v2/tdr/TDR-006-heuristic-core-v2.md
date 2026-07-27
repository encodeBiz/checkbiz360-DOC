# TDR-006 — HeuristicCore V2: integración del contexto histórico sin romper V1

**Fecha:** 2026-06-02  
**Estado:** Diseño aprobado, pendiente implementación (Fase 4)  
**Componente:** `functions/src/services-saas/checkinbiz/application/heuristic/HeuristicCore.ts`

---

## Problema

`HeuristicCore.analyzeBranch()` recibe un `BranchPattern` y evalúa indicadores matemáticos contra thresholds de Firestore. Retorna resultados puntuales: "este indicador está en zona warning". No tiene concepto de tiempo.

Para la Fase 4, el método debe poder recibir un historial de snapshots y enriquecer cada resultado con contexto temporal, sin romper el flujo V1 (que puede seguir operando sin historial).

---

## Principio: retrocompatibilidad total con V1

El método `analyzeBranch` existente NO se modifica. Se añade un nuevo método `analyzeBranchV2` que llama a `analyzeBranch` internamente y enriquece su resultado:

```typescript
// V1 — NO CAMBIA
async analyzeBranch(pattern, level): Promise<HeuristicReport>

// V2 — NUEVO
async analyzeBranchV2(
  pattern: BranchPattern,
  history: PatternSnapshot[],
  level: "branch" | "employee_entity" | "employee_branch_entity"
): Promise<HeuristicReportV2>
```

`analyzeHeuristic.ts` usa V2 si tiene historial, V1 si no. El caller decide, no el core.

---

## Flujo de analyzeBranchV2

```typescript
async analyzeBranchV2(
  pattern: BranchPattern,
  history: PatternSnapshot[],
  level: "branch"
): Promise<HeuristicReportV2> {

  // 1. Ejecutar análisis V1 (igual que antes)
  const baseReport = await this.analyzeBranch(pattern, level);

  if (baseReport.error) return { ...baseReport, trend: null };

  // 2. Calcular tendencias sobre el historial
  const trendAnalyzer = new TrendAnalyzer(history);
  const trend = trendAnalyzer.compute();

  // 3. Enriquecer cada resultado con contexto temporal
  const enrichedResults = baseReport.results.map(result =>
    this.enrichResult(result, trend, history)
  );

  // 4. Generar narrativa
  const narrative = NarrativeBuilder.build(enrichedResults, trend, this.lang);

  return {
    branchId: baseReport.branchId,
    reliability: baseReport.reliability,
    dataPoints: baseReport.dataPoints,
    results: enrichedResults,
    trend,
    narrative,
  };
}
```

---

## enrichResult: cómo se enriquece cada indicador

Cada indicador tiene un ID (WTB, HCI, OSI, etc.). En `pattern_snapshots.heuristic_scores` tenemos el valor histórico de ese mismo indicador por día. Se puede ver la evolución de HCI a lo largo del tiempo.

```typescript
private enrichResult(
  result: HeuristicResult,
  trend: TrendAnalysis,
  history: PatternSnapshot[]
): HeuristicResultV2 {

  // Extraer historial de este indicador específico
  const historicalValues = history
    .map(s => (s.heuristic_scores as Record<string, number>)?.[result.id])
    .filter((v): v is number => v !== null && v !== undefined);

  if (historicalValues.length < 6) {
    return { ...result, trend: null, trendNote: null, historicalContext: null };
  }

  // Tendencia del indicador específico (¿HCI mejora? ¿OSI empeora?)
  const indicatorTrend = computeTrendForValues(historicalValues, {
    higherIsBetter: this.isHigherBetter(result.id),
    threshold: 0.05
  });

  // Ajuste de severidad: si está en "warning" pero mejorando → puede quedarse en warning
  // pero se añade nota positiva. No se sube a "success" automáticamente.
  const adjustedStatus = result.status; // por ahora sin ajuste de severidad (puede añadirse después)

  // Nota contextual de tendencia
  const trendNote = this.buildTrendNote(result.id, indicatorTrend, historicalValues, result.value);

  // Contexto histórico numérico
  const midIdx = Math.floor(historicalValues.length / 2);
  const avgOlder = mean(historicalValues.slice(0, midIdx));
  const delta = result.value - avgOlder;

  return {
    ...result,
    status: adjustedStatus,
    trend: indicatorTrend,
    trendNote: trendNote ? { es: trendNote.es, en: trendNote.en } : null,
    historicalContext: {
      daysAnalyzed: historicalValues.length,
      referenceValue: Number(avgOlder.toFixed(4)),
      delta: Number(delta.toFixed(4)),
      deltaPercent: avgOlder !== 0 ? Number((delta / Math.abs(avgOlder) * 100).toFixed(1)) : 0,
    },
  };
}
```

### isHigherBetter por indicador

```typescript
private isHigherBetter(id: string): boolean {
  const lowerIsBetter = new Set(["OSD", "RCV", "CVH", "CRI", "CPD"]);
  return !lowerIsBetter.has(id);
}
```

`OSD` es dispersión horaria → menor es mejor (más puntual).  
`RCV` es varianza de costo → menor es mejor (más estable).  
`CPD` es delta de costo → puede ser positivo o negativo, pero se interpreta como "cuánto supera el costo real al esperado", menor es mejor.

---

## NarrativeBuilder: generación de narrativa determinista

La narrativa no usa LLM. Se genera por reglas combinando el estado actual y las tendencias:

```typescript
class NarrativeBuilder {
  static build(results: HeuristicResultV2[], trend: TrendAnalysis, lang: "es" | "en"): BranchNarrative {

    const errors = results.filter(r => r.status === "error");
    const warnings = results.filter(r => r.status === "warning");
    const successes = results.filter(r => r.status === "success");

    const alerts: string[] = [];
    const positives: string[] = [];
    const highlights: string[] = [];

    // --- Alertas críticas ---
    if (errors.length > 0) {
      alerts.push(lang === "es"
        ? `${errors.length} indicador(es) en estado crítico: ${errors.map(r => r.id).join(", ")}`
        : `${errors.length} indicator(s) in critical state: ${errors.map(r => r.id).join(", ")}`
      );
    }

    if (trend.volatility === "high") {
      alerts.push(lang === "es"
        ? "Alta volatilidad detectada en el patrón. El comportamiento es inconsistente."
        : "High volatility detected. Behavior is inconsistent."
      );
    }

    // --- Tendencias negativas en indicadores clave ---
    if (trend.reliability.direction === "declining" && trend.reliability.confidence !== "insufficient") {
      const pct = (trend.reliability.deltaPercent * 100).toFixed(1);
      alerts.push(lang === "es"
        ? `La fiabilidad del patrón cayó un ${pct}% en el período analizado.`
        : `Pattern reliability dropped ${pct}% in the analyzed period.`
      );
    }

    // --- Señal de recuperación ---
    if (trend.recoverySignal) {
      highlights.push(lang === "es"
        ? "Señal de recuperación activa: los últimos 7 días muestran mejora sostenida."
        : "Recovery signal detected: last 7 days show sustained improvement."
      );
    }

    // --- Task rating ---
    if (trend.taskRating && trend.taskRating.direction !== "stable" && trend.taskRating.confidence !== "insufficient") {
      if (trend.taskRating.direction === "improving") {
        positives.push(lang === "es"
          ? `Valoración de tareas en mejora (${trend.currentAvgTaskRating?.toFixed(1)}/5 actual)`
          : `Task rating improving (${trend.currentAvgTaskRating?.toFixed(1)}/5 current)`
        );
      } else {
        alerts.push(lang === "es"
          ? `Valoración de tareas en descenso (${trend.currentAvgTaskRating?.toFixed(1)}/5 actual)`
          : `Task rating declining (${trend.currentAvgTaskRating?.toFixed(1)}/5 current)`
        );
      }
    }

    // --- Positivos ---
    if (successes.length >= Math.ceil(results.length * 0.7)) {
      positives.push(lang === "es"
        ? `${successes.length} de ${results.length} indicadores en estado óptimo.`
        : `${successes.length} of ${results.length} indicators in optimal state.`
      );
    }

    // --- Summary ---
    const overallState = errors.length > 0 ? "crítico" : warnings.length > results.length / 2 ? "en atención" : "saludable";
    const trendDesc = trend.reliability.direction === "improving" ? "con tendencia positiva" :
                      trend.reliability.direction === "declining" ? "con tendencia negativa" : "estable";

    const summary = lang === "es"
      ? `El patrón de la sucursal se encuentra en estado ${overallState}, ${trendDesc}. ` +
        `Fiabilidad actual: ${(trend.currentReliability * 100).toFixed(0)}%. ` +
        `${trend.daysAvailable} días de historia analizados.`
      : `Branch pattern is ${overallState === "saludable" ? "healthy" : overallState === "crítico" ? "critical" : "under attention"}, ${trendDesc === "con tendencia positiva" ? "with positive trend" : trendDesc === "con tendencia negativa" ? "with negative trend" : "stable"}. ` +
        `Current reliability: ${(trend.currentReliability * 100).toFixed(0)}%. ` +
        `${trend.daysAvailable} days of history analyzed.`;

    return { summary, highlights, alerts, positives };
  }
}
```

---

## Estructura del response V2

```typescript
interface HeuristicReportV2 {
  branchId: string;
  reliability: number;           // del patrón actual
  dataPoints: number;
  results: HeuristicResultV2[];  // indicadores enriquecidos
  trend: TrendAnalysis | null;   // null si historial insuficiente
  narrative: BranchNarrative | null;
}

interface HeuristicResultV2 extends HeuristicResult {
  trend: TrendResult | null;
  trendNote: { es: string; en: string } | null;
  historicalContext: {
    daysAnalyzed: number;
    referenceValue: number;
    delta: number;
    deltaPercent: number;
  } | null;
}
```

---

## Integración en analyzePattern.ts

```typescript
const analyzePattern = async (entityId, branchId, lang, employeeId) => {
  // ... (validaciones existentes sin cambio)

  const pattern = await patternsRepo.findPatternByBranch(branchId);
  if (!pattern) return { error: "pattern/not_found" };

  // Fetch historial (nuevo en Fase 4)
  let history: PatternSnapshot[] = [];
  try {
    const historyResult = await AnalyticsServerClient.getPatternHistory(entityId, branchId, 30);
    history = historyResult.history ?? [];
  } catch (err) {
    console.warn("[analyzePattern] Could not fetch pattern history, proceeding without trends", err);
    // No bloquear: si el servidor privado falla, el análisis V1 sigue funcionando
  }

  const core = new HeuristicCore(repository, lang);

  // Usar V2 si hay historial suficiente, V1 si no
  const report = history.length >= 6
    ? await core.analyzeBranchV2(pattern, history, "branch")
    : await core.analyzeBranch(pattern, "branch");

  return { report };
};
```

**Degradación elegante:** Si el servidor privado está caído o no hay suficiente historia, el análisis funciona exactamente como hoy (V1). El cliente solo recibe un reporte sin `trend` ni `narrative`, no un error.

---

## Archivos a crear/modificar en Fase 4

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `application/heuristic/TrendAnalyzer.ts` | Crear | Clase con el algoritmo de TDR-005 |
| `application/heuristic/NarrativeBuilder.ts` | Crear | Generador de narrativa por reglas |
| `application/heuristic/HeuristicCore.ts` | Modificar | Añadir `analyzeBranchV2` |
| `firebase-checkinbiz-http/analyzePattern.ts` | Modificar | Fetch de historial + llamada a V2 |
| `domain/report/PatternSnapshot.ts` | Crear | Interfaz TypeScript del snapshot |

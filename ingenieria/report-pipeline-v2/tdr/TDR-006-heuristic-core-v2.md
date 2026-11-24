# TDR-006 — HeuristicCore V2: integración del contexto histórico sin romper V1

**Fecha:** 2026-06-02 · **Revisión:** 2026-11-09 (reglas, indicadores y madurez: §A–§F al final)  
**Estado:** La parte V2 (tendencia enriquecida) sigue pendiente. La revisión de coherencia de las reglas está implementada en `fix/heuristica-coherente` (encodebiz-api), sin desplegar.  
**Componente:** `services/analytics/src/application/heuristic/*`, `services/analytics/src/interfaces/heuristic.router.ts` (portado desde la Cloud Function `analyzeHeuristic`)

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

---

# Revisión 2026-11-09 — coherencia de reglas, indicadores y madurez

Rama `fix/heuristica-coherente` (encodebiz-api). Con TDR-008 la variabilidad ya se medía contra el
plan, pero el resto de la capa seguía con tres fallos de fondo: (1) reglas de persona decididas
por `skillLevel` (40 % horas en la plataforma, 20 % estabilidad del reloj) con textos que
nombraban causas; (2) indicadores de centro que devolvían 0 cuando faltaba el dato
(`criticalTaskOnTimeRate`, `branchAvgRating`) o medían un ciclo como si fuera una jornada (WTB,
WLB, ROIh); (3) sin umbrales en Firestore no había resultado alguno, y el porte leía
`checkbiz_heuristic_indicators` cuando la función original y el panel leen
`checkbiz_heuristic_indicators_v2`.

## A. Qué pasa cuando no hay indicadores

Antes: `results: []` siempre (la colección está vacía en dev; en el porte además con el nombre
equivocado). El panel pintaba «No se puede mostrar el análisis heurístico» con un patrón de 914
ciclos. No había umbrales por defecto en ningún sitio: ni en código, ni en el SAAS, ni en el front.

Ahora: `FirestoreHeuristicRepository.getAll()` lee `checkbiz_heuristic_indicators_v2`; si no hay
documentos con `thresholds`, manda el catálogo `defaultIndicators.ts` (§C). La respuesta dice de
dónde salieron (`indicatorsSource: "firestore" | "default"`). Las reglas de persona ya **no se
leen de Firestore** (`engine_rules`): viven en `engineRules.ts` con el texto construido sobre las
cifras observadas. La colección queda sin lector.

## B. Reglas de persona (`engineRules.ts`, versión `2026-11-09`)

Todas leen la **vista** (`applyPlanTiming`): con plan, `stdStartHour`/`stdEndHour` son la
dispersión robusta del desvío frente al plan; sin plan, el reloj. Cada resultado lleva `basis`
(`plan`/`clock`) y `evidence` con las cifras. Una señal que falta es `null` y la regla no aplica.

| id | Qué mide | Dato | Umbral | Por qué | Por tareas |
|---|---|---|---|---|---|
| `correct_high_variability` | Dispersión de entrada o salida | `stdStartHour`/`stdEndHour` de la vista | > 0,8 h (48 min) | Corte de v1 y `OSD_MAVERICK`; una σ de 48 min = una de cada tres marcas más lejos | Sí (contra el plan) |
| `late_arrivals` *(nueva)* | Entradas después del plan + tolerancia | `timing.punctuality` (solo plan) | < 70 % con ≥ 10 ciclos con plan | Banda «problema» de la doc. (> 85 alto, 70-85 aceptable, < 70) | Sí |
| `plan_coverage_low` *(sustituye a `coaching_low_efficiency`)* | Σ trabajado / Σ planificado por ciclo | `timing.planCoverage` (solo plan) | < 75 % | `efficiencyIndex` era calidad de datos × madurez; el 75 % está muy por encima del ruido (±5 %) y del déficit claro (10 %) del eje de horas del panel: la regla solo repite el hecho cuando es grande | Sí |
| `tasks_late` *(nueva)* | Tareas con plazo terminadas tarde | `tasks.onTimeRate` (`tasks_raw`) | en plazo < 70 % con ≥ 10 terminadas | Misma banda que la puntualidad | Sí |
| `tasks_rejected` *(nueva)* | Tareas revisadas rechazadas | `tasks.rejectionRate` | > 25 % con ≥ 5 terminadas | `REJECTION_COMPLIANCE` (perfil `compliance-risk`) | Sí |
| `data_quality_low` *(sustituye a `monitor_low_reliability`)* | Calidad de registro de los fichajes | `dataQuality` | < 35 %, informativa | `DATA_QUALITY_WEAK`; por encima del ~0,5 del bug del descanso fijo | Sí |
| `high_stability_reward` | Entrada y salida estables (y puntuales con plan) | `std*` de la vista; `timing.punctuality` | ambas < 0,3 h y, con plan, puntualidad ≥ 85 % | 18 min es el corte de v1; cae `skillLevel ≥ 0,45` | Sí |
| `tasks_on_time_high` *(nueva)* | Volumen y plazo de tareas | `tasks.done`, `tasks.onTimeRate` | ≥ 20 terminadas y ≥ 90 % en plazo | 20 = `MIN_DATA_POINTS`; 90 % por encima de «alto» para que el elogio no sea ambiguo | Sí |

Eliminadas, con el motivo: `onboarding_followup` (exigía `dataPoints < 20`, que el núcleo rechaza
antes: nunca saltó); `maintain_average_performer`, `potential_rising_star`,
`promote_high_performer`, `role_reassignment_candidate`, `critical_rrhh_review` (decidían por
`skillLevel`/`efficiencyIndex`, es decir, por antigüedad en la plataforma y hora del reloj, y
sus textos eran inferencias: «talento emergente», «desalineación», «candidato a promoción»).

Textos: nombran el hecho con sus cifras y la ventana («La hora de entrada se separa de la
planificada con una dispersión de 52 min…», «Trabajó el 73 % del tiempo planificado en 23
ciclos…»). La acción es «Revisar» con «La causa no está establecida» cuando no lo está. Salen en
`es` y `en`; las `actions` también siguen el idioma pedido (antes solo español).

## C. Indicadores de centro (`HeuristicCalculator.computeBranch`)

| id | Qué mide | Dato | Null cuando | Umbral por defecto | Por tareas |
|---|---|---|---|---|---|
| OSD | Dispersión entrada + salida (h) | vista (`std*`) | sin dispersión | < 0,5 ✓ · 0,5-1,0 ⚠ · > 1,0 ✗ (`OSD_DISCIPLINED`/`OSD_MULTI_SHIFT`) | Sí |
| WLB | Cobertura del plan | `timing.planCoverage`; sin plan `workHours/avgScheduledHours` | sin plan y sin `avgScheduledHours`, o ciclo = tarea sin plan | ≥ 0,9 ✓ · 0,75-0,9 ⚠ · < 0,75 ✗ (10 % = `CLEAR_SHORTFALL_PCT`; 75 % = regla de persona) | Sí |
| TAC | onTime × (1 − rechazo) | espejo `tasks_raw`; si no, `taskSignals` con `taskCount > 0` | sin veredicto de plazo | ≥ 0,85 ✓ · 0,7-0,85 ⚠ · < 0,7 ✗ | Sí |
| TRI | Rechazadas / revisadas | espejo; si no, `taskSignals` | sin revisadas | < 0,1 ✓ · 0,1-0,25 ⚠ · > 0,25 ✗ | Sí |
| PTC | Críticas en plazo | **solo espejo** (`criticalWithVerdict > 0`) | sin críticas con veredicto (el patrón guarda 0 en los dos casos) | ≥ 0,9 ✓ · 0,7-0,9 ⚠ · < 0,7 ✗ | Sí |
| TQI | Nota media × (1 − rechazo) | **solo espejo** (`task_ratings_raw`, ≥ 3 valoraciones) | sin valoraciones (`branchAvgRating` del patrón es siempre 0) | sin defecto | Sí |
| QHI | (TAC + 1−TRI [+ TQI]) / n | los anteriores | sin TAC o TRI (antes caía a madurez + calidad + OER con el mismo nombre) | sin defecto | Sí |
| WTB | Duración media del ciclo (h) | `avgEnd − avgStart` | **ciclo = tarea** (`dominantSource: tasks`) | sin defecto | **No** (ciclo ≠ jornada) |
| ROIh | `avgCostEfficiency / workHours` | ídem | ciclo = tarea, o sin coste | sin defecto | No |
| CPD | `effectiveRealCost − avgCycleCost` | patrón | **con base plan** (`effectiveRealCost` suma penalizaciones del reloj: dispersión × tarifa × 0,5) | sin defecto | No |
| CRI | `min(CV,2) × coste / 100` | con plan, coste de referencia = `avgCycleCost` | sin CV o sin coste | sin defecto | Parcial |
| HCI, PSS | Confianza/madurez del patrón | `reliability`, `dataMaturity`, `dataQuality` | — | sin defecto (lo cubre `maturity`) | Describe el dato, no la operación |
| OSI, RCV, CVH, OER, ECR, ERP, CEE, SSR, GHI | Costes y «eficiencia» | `costCV`, `avgCostEfficiency` (= consistencyScore × fiabilidad: **calidad de datos, no eficiencia**) | sin el dato (antes 0) | sin defecto: solo si Firestore define umbral | Dudosa: `costCV` en Por tareas mide el reparto de duraciones de tarea |

Ningún indicador devuelve `NaN`/`Infinity`; el evaluador recibe el indicador cargado (antes una
lectura de Firestore por indicador) y cae a `es` si falta el idioma.

## D. Madurez única (ADR-005)

`HeuristicSelector.maturity(pattern, observedDays)` usa `normalizeReliability` de shared: `ready`
con ≥ 20 ciclos **y** ≥ 14 días distintos con fichaje (90 días del espejo). La misma vara que el
`archetype` de `BuildPanelOverview`. Sin `ready`: `profileType: null` y `results: []`, con
`maturity: {status, progress, observedDays, dataPoints}` en la respuesta. El 404
`analyze/insufficient_data` con < 20 ciclos se mantiene (contrato con panel y conector). Si
Postgres no responde, `observedDays: null` y decide solo el recuento (como antes). Lo que había
en el selector (`status` con 3 ciclos y fiabilidad 0,4) no lo leía nadie: eliminado.

`BuildPanelOverview` deja de publicar el `profileType` guardado cuando lo clasificó el reloj y
el plan de la persona se mueve (`dominantSource: tasks` o ≥ 3 inicios planificados distintos);
si el patrón ya trae `timingBasis: "plan"` (clasificador único de shared, 09-nov), vale.

## E. Contexto (`loadContext.ts`)

`timing` (TDR-008), `tasks` (persona **o centro**: `fetchTaskEvidence` acepta `branchId`),
`branchTasks` (críticas y valoraciones) y `observedDays`. El clasificador de sucursal recibe las
tareas del espejo, no solo las EMA del trigger.

## F. SaludStart (staging, 29 personas «Por tareas», 09-nov)

| | 08-nov (reloj) | develop (TDR-008) | ahora |
|---|---|---|---|
| `correct_high_variability` | 25 (falsos) | 0 | 0 |
| `coaching_low_efficiency` | 2 (falsos) | 0 | — (sustituida) |
| `high_stability_reward` | 0 | 0 (`skillLevel` 0,22-0,38 por el reloj y la antigüedad) | 27 |
| `tasks_on_time_high` | — | — | 13 |
| Perfil | 26 maverick (falsos) | 19 anchor, 10 neutral | 19 anchor, 9 neutral, 1 sin madurez (11 días) |
| Badalona / Barcelona | 404 / — | elite, `results: []` | elite; OSD ✓, WLB ⚠ 0,90 / ✓ 0,905, TAC ✓, TRI ✓; PTC y TQI no aplican |

Lo que sigue abierto: `trabaja_de_menos` para 28/29 en el eje de horas del panel
(`BuildOperatingCost`, −10 % de la siembra): en Por tareas acabar antes la tarea no es trabajar
de menos; el eje debería leer tareas. WLB ⚠ en Badalona (0,8976) repite ese mismo hecho con otro
corte. El front solo pinta `results` (ni `profileType`, ni `maturity`, ni `basis`), filtra los de
centro por los ids de coste (`defaultItems2`) y lee `explanation[locale]` solo para `es`/`en`.

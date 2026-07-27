# TDR-007 — Motor de tendencia basado en deriva (sustituye el núcleo de cálculo de TDR-005)

**Fecha:** 2026-07-24
**Estado:** Diseño aprobado, implementación en curso (branch primero, empleado después)
**Componente:** `encodebiz-api/packages/shared/src/analysis/patternHistory.ts` — compartido por el
servidor `analytics` (branch) y por `merlin` (empleado). **Nota de arquitectura:** vive en el servidor
privado, no en Firebase Functions como asumía TDR-005 originalmente — decisión consciente: el servidor
ya tiene acceso directo a `pattern_snapshots` en PostgreSQL y evita duplicar lógica de cálculo entre
Firebase y el servidor (ver Fase 5 de [04_fases.md](../04_fases.md), que ya movía HeuristicCore al
servidor por el mismo motivo).

Relación con TDR-005: **este documento sustituye el algoritmo base** (comparación de medias por
mitades) por un motor de deriva/pendiente. Mantiene de TDR-005: el concepto de `confidence` por
métrica, las bandas de `dataQuality`, la lógica de `recoverySignal` (adaptada) y el principio de
umbral relativo por métrica. TDR-005 queda como referencia histórica de esas piezas; no se elimina.

---

## Problema con el método de TDR-005 (medias por mitades)

Comparar la media de la primera mitad de la ventana contra la media de la segunda mitad detecta
saltos de nivel, pero es ciego a una **deriva lenta y sostenida**: una señal que cambia poco por
día pero en la misma dirección durante toda la ventana.

Caso real encontrado en producción (ACB2 Spain, sucursal `Gj8AsdQW…`, 16 días): la dispersión de
hora de entrada bajó de 53 a 50 minutos, **monótonamente, los 16 días**. El método de medias por
mitades lo clasificó como `stable` (el cambio relativo entre mitades no llegaba al umbral). Es
exactamente la señal que un manager querría ver — "el equipo lleva dos semanas ganando puntualidad
de forma sostenida" — y el método anterior la descartaba como ruido.

---

## Decisión: pendiente (mínimos cuadrados) + monotonicidad, con umbral relativo heredado

### Algoritmo base — por métrica

```typescript
interface TrendResult {
  direction: "improving" | "declining" | "stable";
  confidence: "high" | "medium" | "low" | "insufficient";
  delta: number;          // valor de llegada (suavizado) - valor de partida (suavizado)
  deltaPercent: number;   // |delta / anchorFrom| — umbral relativo, evita comparar escalas distintas
  slopePerStep: number;   // pendiente por mínimos cuadrados sobre TODA la ventana
  monotonicity: number;   // 0..1 — fracción de pasos día-a-día en la dirección dominante
}

function computeMetricTrend(
  series: Array<number | null>,
  options: { higherIsBetter: boolean; relativeThreshold: number; monoFloor: number }
): TrendResult {
  const ys = series.filter((v): v is number => v !== null && isFinite(v));

  if (ys.length < 6) {
    return { direction: "stable", confidence: "insufficient", delta: 0, deltaPercent: 0, slopePerStep: 0, monotonicity: 0 };
  }

  // Anclas suavizadas: media de los primeros/últimos min(3, n/2) puntos, no un único día
  // (un solo día de ruido no debe decidir el delta reportado).
  const edge = Math.min(3, Math.floor(ys.length / 2));
  const anchorFrom = mean(ys.slice(0, edge));
  const anchorTo = mean(ys.slice(-edge));
  const delta = anchorTo - anchorFrom;
  const deltaPercent = anchorFrom === 0 ? 0 : Math.abs(delta / anchorFrom);

  const slopePerStep = leastSquaresSlope(ys);      // ver patternHistory.ts
  const monotonicity = monotonicityFrac(ys);        // ver patternHistory.ts

  const magnitudeSignal = deltaPercent >= options.relativeThreshold;
  const driftSignal = monotonicity >= 0.8 && Math.abs(delta) >= options.monoFloor;

  const sign = delta > 0 ? 1 : delta < 0 ? -1 : 0;
  const isImproving = options.higherIsBetter ? sign > 0 : sign < 0;

  let direction: TrendResult["direction"] = "stable";
  if (magnitudeSignal || driftSignal) {
    direction = isImproving ? "improving" : "declining";
  }

  const confidence: TrendResult["confidence"] =
    ys.length >= 21 ? "high" : ys.length >= 14 ? "medium" : "low";

  return { direction, confidence, delta, deltaPercent, slopePerStep, monotonicity };
}
```

**Por qué se mantiene un umbral relativo (heredado de TDR-005) además de la pendiente:** la pendiente
sola detectaría como "deriva" un cambio minúsculo pero perfectamente monótono (p.ej. 0.001 de
fiabilidad subiendo 7 días seguidos por redondeo). `magnitudeSignal` exige que el cambio relativo
total sea significativo; `driftSignal` exige que, aunque el cambio sea pequeño, sea consistente y
supere un piso absoluto (`monoFloor`) para no disparar con ruido de precisión numérica. Basta con
que se cumpla **uno** de los dos.

### Suavizado previo para métricas de alto ruido (`costCV`)

```typescript
function rollingMean(series: Array<number | null>, window = 7): Array<number | null> {
  return series.map((_, i) => {
    const slice = series.slice(Math.max(0, i - window + 1), i + 1).filter((v): v is number => v !== null);
    return slice.length ? mean(slice) : null;
  });
}
```

`costCV` se pasa por `rollingMean(series, 7)` **antes** de entrar en `computeMetricTrend`. El resto
de métricas usan la serie cruda — solo `costCV` mostró ruido día-a-día (4–16%, picos de 114%) que
haría inútil cualquier umbral directo (ver tabla de validación empírica más abajo).

### `confidence` y `dataQuality` — se mantienen de TDR-005 sin cambios

| Nivel | Umbral (nº de valores no nulos de esa métrica) |
|---|---|
| `high` | ≥ 21 |
| `medium` | ≥ 14 |
| `low` | ≥ 6 |
| `insufficient` | < 6 → `direction` forzado a `stable` |

`dataQuality` del paquete completo (no por métrica): `rich` ≥21 snapshots totales, `moderate` 7-20,
`insufficient` <7 — igual que TDR-005.

### `recoverySignal` — mismo criterio de TDR-005, misma implementación, solo cambia la fuente de "declining"

Requiere ≥14 snapshots. Se calcula **solo sobre `reliability`**:

```typescript
function detectRecovery(reliabilitySeries: Array<number | null>): boolean {
  if (nonNullCount(reliabilitySeries) < 14) return false;
  const last7 = reliabilitySeries.slice(-7);
  const prev7 = reliabilitySeries.slice(-14, -7);
  const globalTrend = computeMetricTrend(reliabilitySeries, RELIABILITY_OPTIONS); // motor de deriva, no medias
  const recentImproves = mean(nonNull(last7)) > mean(nonNull(prev7));
  return globalTrend.direction === "declining" && recentImproves;
}
```

Idéntico a TDR-005 en semántica (últimos 7 vs 7 anteriores, solo si la tendencia global venía mal);
cambia únicamente de dónde sale `globalTrend.direction` — antes de la comparación de mitades, ahora
del motor de deriva de arriba.

### `volatility` / `consistencyScore` — sobre `reliability`, completando el hueco de TDR-005

TDR-005 dejaba `max_std` sin definir en `consistencyScore = 1 - std(reliability)/max_std`. Se fija
`max_std = 0.2` (el punto en que la volatilidad ya es "alta" según la propia tabla de TDR-005, con
margen):

```typescript
function computeVolatility(std: number): "high" | "medium" | "low" {
  if (std > 0.15) return "high";
  if (std > 0.07) return "medium";
  return "low";
}
const consistencyScore = 1 - Math.min(std(reliabilitySeries) / 0.2, 1); // 0..1
```

---

## Extensión sobre TDR-005: hechos fechados (`drifts` ya no es un algoritmo aparte — es el mismo motor, expuesto por métrica)

Además del resumen `TrendResult` por métrica, el paquete expone hechos concretos que ya usan el
mismo cálculo de pendiente/monotonicidad, pensados para que la IA los cite, no los infiera:

- **`keyChanges`** — saltos día-a-día que superan un umbral absoluto por métrica, con fecha exacta.
- **`streaks`** — rachas de `reliability` en la misma dirección (≥3 movimientos consecutivos).
- **`archetypeShifts`** — cambios de `profileType` (categórico) entre un día y el siguiente. Más
  elocuente que cualquier delta numérico: es el propio motor de heurísticas cambiando de opinión.
- **`extremes`** — mejor y peor día de `reliability` en la ventana, con fecha.

---

## Métricas — set validado contra datos reales (2026-07-24, corregido tras revisión)

**Validación empírica de umbrales** (no se fijaron a ojo): se midió el ruido día-a-día real de
`promotionScore`, `efficiencyIndex`, `costCV` y `totalExperienceYears` sobre 5 empleados reales
(Arendel/ACB2/Encodebiz, 12-30 días cada uno) antes de fijar los umbrales de abajo. Resultado:

| Métrica | Ruido día-a-día real | Consecuencia |
|---|---|---|
| `reliability` | 0.2–0.9% | umbral 5% aguanta sin cambios |
| `promotionScore` | 0.3–0.9% | umbral 3% aguanta sin cambios |
| `efficiencyIndex` | 0.3–2.5% (un caso rozó el umbral) | sube de 3% a **5%** por margen |
| `costCV` | **4–16%, picos de hasta 114% en un solo día** | umbral directo de 8% es inviable — dispararía "cambio notable" casi cada día. Se **suaviza con media móvil de 7 días antes** de clasificar tendencia (igual tratamiento que ya recibe `avgTaskRating30d`, que es una media de 30 días por diseño) |
| `totalExperienceYears` | 1–3%/día, hasta 38% en 2 semanas | el % de cambio depende mecánicamente de la antigüedad (un mes de tenure = salto grande relativo; años de tenure = casi plano). Un único umbral relativo no sirve para ambos casos. **Se saca del clasificador de tendencia** y se reporta como hecho de contexto directo ("lleva X meses/años"), no como dirección mejora/empeora |

### Branch (fuente: `pattern_snapshots`, `employee_id IS NULL`)

| Métrica | Campo fuente | higherIsBetter | relativeThreshold | Estado |
|---|---|:---:|:---:|---|
| `reliability` | `reliability` | sí | 5% | ✅ datos reales |
| `startTime` | `avg_start_hour` | informativo | 5% | ✅ — añadida aquí: es la señal que motivó todo TDR-007 (ver "Problema" arriba); TDR-005 no la incluía porque asumía `daily_reports`, que está vacía |
| `endTime` | `avg_end_hour` | informativo | 5% | ✅ datos reales |
| `startDispersion` | `std_start_hour` | no | 5% | ✅ datos reales — caso real ACB2 `Gj8AsdQW…`: 53→50min, delta relativo 6%, monotonía 100% |
| `costEfficiency` | `heuristic_scores.avgCostEfficiency` | sí | 5% | ✅ datos reales |
| `costVariance` | `heuristic_scores.costCV`, **suavizado media móvil 7d** | no | 15% (sobre serie ya suavizada; sujeto a revisar con más histórico) | ✅ datos reales, con suavizado |
| `taskRating` | `avg_task_rating_30d` | sí | 3% | ⚠️ schema listo, sin datos (ver nota) |
| `hci` | `heuristic_scores.HCI` | sí | 5% | ✅ datos reales |
| `punctualityRateIn` | `daily_reports.on_time_checkins/total_checkins` | sí | 5% | 🚫 **bloqueada** — `daily_reports` tiene 0 filas en prod (Fase 2 del pipeline nunca se activó) |
| `punctualityRateOut` | `daily_reports.on_time_checkouts/total_checkouts` | sí | 5% | 🚫 bloqueada, mismo motivo |
| `lateMinutesIn` | `daily_reports.late_minutes_sum_in` | no | 10% | 🚫 bloqueada, mismo motivo |

Las métricas bloqueadas devuelven `confidence: "insufficient"` siempre, de forma honesta, en vez de
simularse. Se desbloquean si se retoma la Fase 2 documentada en
[04_fases.md](../04_fases.md#fase-2-daily-report-enriquecido-desde-postgresql).

### Empleado (fuente: `pattern_snapshots`, `employee_id IS NOT NULL`) — sin spec previa, definida aquí

| Métrica | Campo fuente | higherIsBetter | relativeThreshold |
|---|---|:---:|:---:|
| `reliability` | `reliability` | sí | 5% |
| `startTime` / `endTime` | `avg_start_hour` / `avg_end_hour` | informativo | 5% |
| `startDispersion` | `std_start_hour` | no | 5% |
| `promotionScore` | `heuristic_scores.promotionScore` | sí | 3% |
| `efficiencyIndex` | `heuristic_scores.efficiencyIndex` | sí | 5% |
| `costCV` | `heuristic_scores.costCV`, **suavizado media móvil 7d** | no | 15% |
| `taskRating` | `avg_task_rating_30d` | sí | 3% — ⚠️ schema listo, sin datos reales aún: feature de valoración de tareas de baja adopción por clientes, no es un bug ni está bloqueada técnicamente |

**Fuera del clasificador de tendencia, como contexto directo (no dirección mejora/empeora):**
`totalExperienceYears` (antigüedad actual + fecha), `profileType` actual (el cambio de arquetipo ya
se reporta aparte vía `archetypeShifts`).

**Importante:** branch y empleado usan el mismo motor de cálculo (`computeMetricTrend`), pero son
**modelos separados** con sets de métricas propios — un branch es un agregado operativo, un empleado
es una persona; sus señales y sus soluciones no son intercambiables (ver `contrato-perfil.md` para
un ejemplo de módulo que sí distingue explícitamente niveles entidad/sucursal/empleado en su
resolución).

---

## Colisión de nomenclatura con `contrato-perfil.md`

`DOCS/modulos/contrato-perfil.md` ya usa "Perfil laboral" para plantillas contractuales (jornada,
horas extra, nocturnidad, ET/RDL España) — un concepto no relacionado con el perfil de comportamiento
descrito aquí. Se recomienda no nombrar el trabajo de este documento simplemente "perfil" en código o
UI para evitar confusión con el módulo ya especificado; nombre de trabajo sugerido:
**"perfil de comportamiento"** o **"perfil operativo"**, pendiente de confirmación de producto.

---

## Mínimos de datos (sin cambios respecto a TDR-005)

| Análisis | Mínimo de snapshots | Comportamiento si no se alcanza |
|---|---|---|
| Tendencia por métrica | 6 valores no nulos | `direction: "stable"`, `confidence: "insufficient"` |
| `recoverySignal` | 14 | `false` siempre |
| `confidence: "high"` | 21 | — |

---

## Rollout

1. Branch primero (ya tiene 74 snapshots reales en prod, Arendel/ACB2/Encodebiz) — sustituye el
   algoritmo desplegado en `analytics.router.ts` / `packages/shared`.
2. Validar contra las series reales ya usadas para detectar el problema original (ACB2 `Gj8AsdQW…`
   debe pasar a mostrar `startDispersion: declining` con alta monotonicidad).
3. Empleado después, sobre el mismo motor, con su propio set de métricas de la tabla de arriba.

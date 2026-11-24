# TDR-007 — Motor de tendencia basado en deriva (sustituye el núcleo de cálculo de TDR-005)

**Fecha:** 2026-07-24 · **Revisado:** 2026-11-09 (§«Base de cada medida», al final)
**Estado:** Implementado (branch y empleado). La revisión del 09-nov está en `fix/tendencia-e-historial`, sin desplegar
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

---

## Base de cada medida (revisión 2026-11-09)

Medido en staging con SaludStart («Por tareas», 28 personas, 2.159 fotos reconstruidas con su fecha
real del 1-oct al 9-nov) el paquete de evidencia contaba cosas que no eran: a Youssef
(`7CdglWOrwMDSelf2fdaz`) «fiabilidad mejora, entra más temprano, progreso mejora, eficiencia mejora,
dos cambios de perfil»; a Badalona, seis «cambios de perfil» en diez días (neutral↔understaffed en
días alternos). Nada de eso describía a la persona ni al centro. Las causas, y lo que cambia:

### 1. Una serie, una granularidad

`fetchPatternSeries` (shared) y la consulta de `GET /patterns/history` (analytics) piden ahora
exactamente un nivel: sucursal (`employee_id IS NULL AND branch_id = $`), entidad (`branch_id IS NULL
AND employee_id IS NULL`), persona global (`employee_id = $ AND branch_id IS NULL`) y persona en
sucursal. El índice único es `(entity_id, COALESCE(branch_id,''), COALESCE(employee_id,''), fecha)`:
sin el `IS NULL` explícito, la serie de un nivel se mezclaba con la de sus hijos (una persona de dos
sucursales daba 83 «días» en 30). El commit `19fd412` lo arregló para la persona global; esto lo cierra
para los cuatro niveles. Hoy no se escriben fotos de entidad (ningún trigger las produce), así que la
consulta de entidad devuelve vacío en vez de la suma de sucursales.

### 2. Solo cuentan los días con registro

Una foto cuyo `dataPoints` no cambió respecto a la anterior es el patrón copiado un día sin ciclos
(domingos, festivos), no una observación nueva. `activePoints` las quita antes de calcular; el paquete
trae `daysAvailable` (fotos) y `activeDays` (con registro), y la confianza y la cobertura (`dataQuality`
del paquete: rich/moderate/insufficient) se cuentan sobre los días con registro. Sin `dataPoints` la
foto se conserva.

### 3. La fiabilidad se compara por su parte comparable

`reliability` del patrón = `dataMaturity × dataQuality`, y la madurez es `0,2 + 0,8·log1p(n)/log1p(100)`:
crece sola con cada ciclo hasta los 100. Sergi pasaba de 0,78 a 0,85 en dos semanas con la calidad
clavada en 1: la «mejora» era la curva de madurez. Ahora la métrica `reliability` del paquete se mide
sobre `dataQuality` cuando las fotos la traen (`reliabilityBasis: "dataQuality"`), y las rachas, los
extremos, la volatilidad, la consistencia y la señal de recuperación salen de esa misma serie. Sin
`dataQuality` en las fotos (anteriores a V2) se usa la compuesta, pero solo si el patrón ya estaba
maduro al EMPEZAR la ventana (`dataMaturity ≥ 0,95`, ≈ 75 ciclos; si no hay madurez, `dataPoints ≥ 75`);
si no, `confidence: "insufficient", reason: "maturing"`. Regla heredada de TDR-003 del panel
(`analysis/reliability.ts`): la calidad compara, la madurez decide el estado.

### 4. Las medidas que llevan la fiabilidad dentro esperan a que el patrón madure

| Medida | Qué es de verdad (`fichaje/helper.ts`, `fichaje/employee.ts`) | Decisión |
|---|---|---|
| `avgCostEfficiency` (branch `costEfficiency`) | EMA(consistencia del ciclo × reliability): «calidad de datos del ciclo, no eficiencia operativa real» | `maturityBound`: no se compara mientras el patrón se forma. Etiqueta: «coste efectivo frente al coste bruto del ciclo (limpieza del registro)» |
| `efficiencyIndex` (empleado) | EMA(avgCostEfficiency × reliability) desde 0: doble producto con la madurez; con plan, TDR-008 lo sustituye por la cobertura del plan, que no está en las fotos | **Sale del set.** No mide aprovechamiento de nada |
| `promotionScore` | skillLevel(reliability, efficiencyIndex, variabilidad del reloj) × reliability × min(1, antigüedad/10) | `maturityBound`. Además lleva la tenure dentro (crece mecánicamente, como `totalExperienceYears`) y la variabilidad del reloj: pendiente de rehacer cuando el clasificador mida contra el plan |
| `costCV` (`costVariance`) | σ/μ (Welford) del coste de cada ciclo = horas × tarifa | Se mantiene, suavizado 7 d. Etiqueta: «dispersión del coste por ciclo de fichaje». En «Por tareas» mide cuánto varía la duración de las tareas de la persona, no a la persona |
| `costTrend` | «up/down» comparando la EMA del coste efectivo con la del ciclo anterior | No entra ni entrará: es el signo del último paso de una EMA |
| `dataMaturity` | cuánto patrón hay | Contexto: `context.dataMaturityLatest`, `context.maturing`. Nunca tendencia |
| `avgStartHour`, `avgEndHour`, `stdStartHour`, `weeklyWorkAvg` | medias POR CICLO con la hora del reloj. En «Por tareas» un ciclo es una tarea de 90-150 min a otra hora del día | `clock`: con base `plan` no se comparan (`reason: "clock_basis"`) ni se fechan sus saltos. `weeklyWorkAvg` no entra en el paquete |
| `HCI` | nunca lo escribe ningún trigger (`heuristic_scores` no trae la clave) | Se deja declarado y sale siempre `too_few_points`, que es la verdad |

El paquete lleva `basis: "plan" | "clock"` y `basisSource`: lo dijo quien llama (`caller`: merlin tras
`withPlanTiming`; `GET /patterns/history` tras `fetchPlanTiming` del espejo), lo traen las fotos
(`snapshots`, cuando el clasificador escriba `timingBasis`) o no se sabe y se asume reloj (`assumed`),
que es lo que había. `trendWithBase` de merlin sigue filtrando después: las dos capas dicen lo mismo.

### 5. Un cambio de perfil es un hecho solo si dura

`detectArchetypeShifts` toma los días con registro cuyo perfil se clasificó con la misma base que la
lectura (con base `plan`, solo las fotos con `timingBasis: "plan"`: el perfil anterior a ese cambio se
calculó con el reloj y no vale), quita los estados de madurez (`ghost`, `data-weak`: entrar o salir
de ellos es que hay más datos, no que alguien cambió), comprime en rachas y solo las de
`SHIFT_MIN_DAYS = 5` días con registro cuentan. El cambio es el paso entre dos rachas confirmadas con
perfil distinto, fechado el primer día de la nueva, con `persistedDays`. Lo que no llega se cuenta en
`context.profileFlaps` y no se narra. Consecuencia aceptada: un cambio real se afirma cinco días con
registro después de empezar. En SaludStart, con base plan, los cinco sujetos quedan sin cambio (los
perfiles son del reloj); con base reloj quedan Youssef `neutral→maverick` el 29-oct (9 días) y Sergi el
23-oct (13 días) —que serían cambios de verdad si el reloj fuera la base— y desaparecen el `at-risk` de
dos días de `E93z…`, los seis parpadeos de Badalona y los cuatro de Barcelona.

### 6. Antes y después (staging, ventana de 30 días al 09-nov, base `plan`)

| Sujeto | Antes | Después | Qué era ruido |
|---|---|---|---|
| Youssef `7CdglWOrwMDSelf2fdaz` (28 fotos) | fiabilidad mejora · entra/sale más temprano · dispersión empeora · progreso mejora · eficiencia mejora · coste/ciclo más disperso · 2 cambios de perfil (22-oct ghost→neutral, 29-oct neutral→maverick) · volatilidad media | 23 días con registro · calidad del registro sin cambio · coste/ciclo más disperso · sin cambios de perfil · patrón formándose (0,84, 39 ciclos) · volatilidad baja | la fiabilidad y el progreso eran la curva de madurez; la hora y la dispersión, el reloj en «Por tareas»; ghost→neutral, llegar a 20 ciclos; neutral→maverick, la dispersión del reloj |
| `E93zJ7bFORo8FVU9J3Qa` (28) | fiabilidad mejora · hora más temprano · progreso y eficiencia mejoran · 3 cambios (14-oct →maverick, 30-oct →at-risk, 2-nov →maverick) | 23 días · calidad sin cambio · coste/ciclo sin cambio · sin cambios · maduro (0,98, 89 ciclos) | el `at-risk` duró dos días (uno sin registro) |
| Sergi `KEErhkSKomD2xwy5zpT3` (28) | fiabilidad mejora · racha de 4 días mejorando · sale más temprano · dispersión empeora · progreso y eficiencia mejoran · 2 cambios | 23 días · calidad sin cambio · sin racha · sin cambios · formándose (0,89, 52 ciclos) | la racha era la madurez; lo demás, igual que Youssef |
| Badalona `xRwDBVrJ8BM34uWkgoNV` (28) | sale más tarde · dispersión mejora · limpieza del ciclo empeora · coste/ciclo más disperso · **6 cambios de perfil** en 10 días | 25 días · calidad sin cambio · limpieza del ciclo empeora · coste/ciclo más disperso · sin cambios (5 parpadeos) | neutral↔understaffed por una EMA de puntualidad de tareas rozando 0,6; `wtb < 7 h` siempre, porque un ciclo es una tarea |
| Barcelona `FzXKjZW8odGbnw7AVjFX` (27) | entra/sale más temprano · dispersión empeora · limpieza mejora · 4 cambios (27→30-oct, en días alternos) | 22 días · calidad sin cambio · limpieza mejora · sin cambios (3 parpadeos) | igual que Badalona |

Las dos «limpieza del ciclo» de las sucursales son medidas con base (patrón maduro) y se quedan; lo que
antes se llamaba «eficiencia de coste» ahora se nombra por lo que es.

### 7. La fecha de la foto (ADR-006 revisado)

`onBranchPatternSync` / `onEmployeePatternSync` fechaban con el día UTC de la escritura. Ahora
`snapshotDateFor` (shared `analysis/snapshotDate.ts`): el día local, en `pattern.timeZone`, de
`pattern.lastCycleAt` si el patrón lo trae, y si no, de ahora; nunca futuro. Compatible con lo
guardado (mismo `YYYY-MM-DD`; solo cambian de día los ciclos cerrados entre las 00:00 locales y las
00:00 UTC). `lastCycleAt` lo tiene que escribir el trigger del fichaje (petición al agente de
`fichaje/*`); mientras no esté, un reproceso sigue fechando en hoy.

### 8. Inventario para la fase dos y esquema mínimo

Lo que hay hoy en Postgres por día y sujeto (staging, SaludStart):

| Tabla | Grano | Qué guarda | Falta |
|---|---|---|---|
| `pattern_snapshots` (2.216 filas: 69 sucursal, 964 persona global, 1.183 persona-sucursal; 0 de entidad) | (entidad, sucursal?, persona?, día) | el ESTADO acumulado del patrón ese día: medias EMA del reloj, `reliability`, `dataPoints`, `heuristic_scores` (profileType, dataQuality, dataMaturity, costes, taskSignals acumuladas por EMA, promotionScore…), `raw_pattern` completo, valoraciones 30 d | la base de la medida y la etiqueta con su base (→ `timing_basis`, migración 063); la fiabilidad descompuesta en columna (→ `data_quality`, `data_maturity`); cuándo se pisó (→ `updated_at`); el último ciclo (`lastCycleAt`, pendiente del trigger) |
| `employee_daily_reports` (970 filas, 29 días) | (entidad, persona, sucursal, día) | la JORNADA REAL del día: minutos netos y de descanso, `cycles[]` con entrada/salida de cada ciclo, `worker_meta` | lo planificado del día (está en `checklogs_raw.schedule_applied` de cada entrada; no agregado) |
| `operational_daily` (117 filas) | (entidad, sucursal, día) | el cierre del centro: esperados, con registro, tarde, terminados, minutos, tareas vencidas/terminadas/a tiempo/tarde, coste | nada por persona |
| `checklogs_raw` (3.088) | fichaje | cada marca con `schedule_applied` (el plan del ciclo: tarea o turno), geo, sospecha, `task_id` | — |
| `tasks_raw` (2.265), `task_events_raw` (11.663), `task_ratings_raw` | tarea / evento | estado, plazo (`time_compliance_status`), prioridad, planificado/empezado/terminado/validado, pausas, asignados; cada evento con fecha | — |
| `daily_reports` | (entidad, sucursal, día) | **0 filas**: la Fase 2 nunca se activó | — |

No hay tabla `task_signals`: las señales de tareas viven en `heuristic_scores.taskSignals` (EMA
acumulada, sin fecha) y los hechos con fecha están en `tasks_raw`/`task_events_raw`.

**Conclusión:** la observación diaria (jornada real, plan del ciclo, tareas del día) YA existe en el
espejo; lo que faltaba en la foto era saber con qué base se midió y poder separar madurez de calidad
sin abrir el JSON. Eso es la migración **063** (`migrations/063_pattern_snapshots_base_de_medida.sql`,
se aplica a mano ANTES de desplegar `analytics`): `timing_basis TEXT`, `data_quality NUMERIC(5,4)`,
`data_maturity NUMERIC(5,4)`, `updated_at TIMESTAMPTZ`, rellenadas desde el JSON guardado, e índice
`(entity_id, timing_basis, snapshot_date)`.

Esquema de entrenamiento propuesto (sin tabla nueva: una vista o una consulta, cuando toque):

```sql
-- una fila por persona y día con registro: estado del patrón al cierre + observación del día + etiqueta
SELECT s.entity_id, s.employee_id, s.branch_id, s.snapshot_date,
       s.timing_basis, s.data_quality, s.data_maturity, s.data_points,
       s.heuristic_scores->>'profileType' AS label, s.heuristic_scores->'taskSignals' AS task_signals_ema,
       d.total_net_minutes, d.total_break_minutes, jsonb_array_length(d.cycles) AS cycles
       -- plan del día: ventanas distintas de schedule_applied de las entradas de ese día (shared/planTiming.plannedWindowFor)
       -- tareas del día: COUNT/FILTER sobre tasks_raw por assigned_employee_ids y completed_at::date
  FROM pattern_snapshots s
  JOIN employee_daily_reports d ON d.entity_id = s.entity_id AND d.employee_id = s.employee_id
                               AND d.branch_id IS NOT DISTINCT FROM s.branch_id AND d.date = s.snapshot_date
 WHERE s.employee_id IS NOT NULL;
```

Lo que todavía no está y haría falta para entrenar con criterio: `timing_basis` poblado (lo escribe el
clasificador), `lastCycleAt` (el trigger del fichaje), y una etiqueta de perfil calculada contra el plan
cuando lo hay. Sin esas tres, la etiqueta guardada hasta hoy es la del reloj.

### 9. Lo que se pide al clasificador unificado (`packages/shared`, otro agente)

El motor espera en el documento del patrón, y por tanto en `raw_pattern` y `heuristic_scores`:

- `timingBasis: "plan" | "clock"` — con qué base se calcularon `stdStartHour`/`stdEndHour` y el
  `profileType` guardados. `BuildPatternSnapshot` ya lo copia a `heuristic_scores` y a la columna
  `timing_basis`; `fetchPatternSeries` ya lo lee. Un perfil con `timingBasis: "plan"` vuelve a contar en
  `archetypeShifts` con lectura contra el plan.
- `lastCycleAt` (ISO o Timestamp) — el último ciclo que entró en el patrón, para fechar la foto
  (`snapshotDateFor`). Lo escribe el trigger del fichaje, no el clasificador.
- Opcional, útil: `planCoverage` (Σ trabajado / Σ planificado) en el patrón cuando la base es plan, para
  que la trayectoria tenga una medida de aprovechamiento con base en vez de `efficiencyIndex`.

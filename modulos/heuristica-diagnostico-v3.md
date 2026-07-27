# Diagnóstico de la Capa Heurística V3

> **Documento histórico — para referencia de diseño.**
> Los 5 errores matemáticos descritos aquí están **resueltos en V2** (rama `qa/heuristic-v2-task-integration`).
> Para el estado actual del sistema ver [heuristica.md](./heuristica.md).
> Para el detalle de cada corrección ver [heuristica-changelog.md](./heuristica-changelog.md).
>
> Fecha del análisis original: 2026-06-05

---

## Por qué existe este documento

El motor heurístico genera 18 indicadores que el intérprete IA (Merlin) usa para producir análisis operativos. El output de Merlin era sistemáticamente genérico ("revisar turnos y fichajes") independientemente de los datos reales. Tras auditar el código se identificaron **5 errores matemáticos** y **5 deficiencias de diseño** que explican el problema.

**Regla de oro para este módulo:** no tocar el prompt de Merlin (Fase 5) hasta que los errores matemáticos (Fase 1) estén corregidos. Mejorar la presentación de datos rotos tiene techo muy bajo.

---

## Errores matemáticos confirmados

### E1 — QHI es algebraicamente idéntico a GHI

```
GHI = (ECR + OSI + HCI) / 3
QHI = (GHI + ECR + OSI + HCI) / 4
    = ((ECR+OSI+HCI)/3 + ECR+OSI+HCI) / 4
    = (ECR+OSI+HCI) · (4/3) / 4
    = (ECR+OSI+HCI) / 3
    = GHI  ← idéntico
```

Cualquier diferencia observable entre los dos valores es ruido de punto flotante. El AI recibe dos señales que parecen independientes y son la misma.

**Corrección:** Redefinir QHI como índice de calidad de tareas `(TAC + TQI + (1-TRI)) / 3` (ver [heuristica-v2-roadmap.md](./heuristica-v2-roadmap.md) §4).

---

### E2 — `costVariance` no es varianza estadística

**Archivo afectado:** `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/helper.ts`

```typescript
// ACTUAL — desviación absoluta de un único punto
const costVariance = Math.abs(costCycle - (pattern.avgCycleCost ?? costCycle));
```

Esto es `|x - μ|` (desviación absoluta de la observación actual), no `σ²` ni `σ`. El valor fluctúa punto a punto y no refleja la dispersión histórica del coste.

**Corrección:** Welford incremental, exactamente igual a como ya se calcula `stdStartHour`:

```typescript
// Añadir al patrón: costM2 (acumulador Welford)
const costStats = updateStd(costCycle, pattern.avgCycleCost, pattern.costM2 ?? 0, pattern.dataPoints ?? 0);
// costStats.std → desviación estándar real de costes por ciclo
// CV = costStats.std / avgCycleCost → coeficiente de variación interpretable
```

El CV tiene escala operativa: `< 0.2` = costes estables; `0.2–0.5` = variabilidad normal; `> 0.5` = alta dispersión.

---

### E3 — `HeuristicNormalizer` crea una cadena de cálculos sin dimensión

**Archivo afectado:** `api-express/src/checkinbiz/application/heuristic/HeuristicCore.ts`

```typescript
// ACTUAL en HeuristicNormalizer
const costVarNormalized = 1 - (1 / (1 + rawVar)); // rawVar = desviación absoluta → 0..1

// Luego en HeuristicCalculator
const relativeCostVar = this.safeDiv(costVarianceAbs, avgCycleCost, 0);
// costVarianceAbs ya está en [0..1] por el normalizer
// dividir [0..1] / 150€ = 0.006 → sin interpretación posible
```

El normalizer convierte la desviación absoluta a 0..1, y luego el calculator divide ese número adimensional entre `avgCycleCost` (en euros). El resultado alimenta OSI, CVH, CRI, WLB, PSS, SSR, GHI.

**Corrección:** Eliminar `HeuristicNormalizer` tras implementar E2. Con el CV de Welford, `boundedCostVar = min(CV, 2)` es directamente operativo y no necesita normalización previa.

---

### E4 — WLB no mide balance de carga de trabajo

**Archivo afectado:** `api-express/src/checkinbiz/application/heuristic/HeuristicCalculator.ts`

```typescript
// ACTUAL
case "WLB":
  return (workHours * avgCostEfficiency) / (1 + boundedCostVar);
```

Esto es eficiencia ponderada ajustada por varianza de coste. No tiene relación con "workload balance". Un empleado con jornada de 8h perfecta puede aparecer como "Underload" porque `avgCostEfficiency` es bajo (ver E5).

**Corrección:** Comparar horas reales vs planificadas del `WorkSchedule`:
```typescript
WLB = netWorkedHours / scheduledHours  // donde scheduledHours viene de Branch.advance.workSchedule
// null si no hay workSchedule configurado
// 0.95–1.05 = óptimo; < 0.85 = infrautilización; > 1.10 = horas extra sistemáticas
```

---

### E5 — `avgCostEfficiency` es calidad de datos, no eficiencia operativa

**Archivo afectado:** `helper.ts`

```typescript
// ACTUAL
const costEfficiency = costCycle > 0 ? effectiveCostCycle / costCycle : 0;
// donde effectiveCostCycle = costCycle * consistencyScore * newReliability
// → costEfficiency = consistencyScore * reliability
//                  = min(1, events/4) * reliability
```

Esto no mide si la operación es eficiente. Mide si el fichaje del ciclo fue completo y el patrón es fiable. Los indicadores ECR, ERP, ROIh, CEE y WLB que usan `avgCostEfficiency` como proxy de eficiencia están midiendo en realidad "¿qué tan bien fichó el empleado?", no "¿qué tan eficientemente trabajó?".

**Corrección a largo plazo:** La eficiencia real requiere datos de output (tareas completadas, tiempo de tarea vs tiempo planificado). Ver integración de `taskSignals` en el roadmap §3.

---

## Deficiencias de diseño

### D1 — 6 de 18 indicadores miden lo mismo

OSI, HCI, PSS, SSR, GHI y QHI dependen todos de `reliability` y `boundedCostVar`. Cuando ambos son bajos (reliability < 0.6), los seis disparan simultáneamente en estado `error`. El AI recibe 6 señales de "inestabilidad" que vienen del mismo par de valores subyacentes.

Con el set actual: ante un patrón con baja calidad de datos, el output del AI siempre dirá "inestabilidad" aunque la sucursal opere perfectamente.

---

### D2 — OSD dispara falsos positivos en operaciones multi-turno

```typescript
OSD = stdStartHour + stdEndHour  // std calculada sobre TODOS los ciclos globalmente
```

Una empresa con turno de mañana (08:00-16:00) y turno de tarde (14:00-22:00) tendrá `stdStartHour` alto por estructura, no por desorden. OSD marcará "High dispersion / Redesign shifts" aunque ambos turnos sean perfectamente consistentes internamente.

**Corrección:** Calcular OSD por grupo de turno usando `stdStartByDay[day]` ya existente. El OSD global solo aplica cuando no hay `workSchedule` configurado, con aviso explícito al AI.

---

### D3 — `reliability` mezcla dos problemas distintos

```typescript
reliability = dataMaturity × dataQuality
           = f(dataPoints) × f(consistencyScore, distanceFactor)
```

Una sucursal nueva con fichajes impecables tiene `reliability` baja por volumen. Una sucursal con 3 años de datos pero 50% de fichajes fallidos también tiene `reliability` baja por calidad. Son síntomas distintos que requieren acciones distintas y el indicador no los distingue.

**Corrección:** Almacenar `dataMaturity` y `dataQuality` por separado en el patrón.

---

### D4 — Sin benchmarking cross-branch

Todos los indicadores son auto-referenciales. CPD = `effectiveRealCost - avgCycleCost`: ambas son medias del mismo dataset, por lo que CPD converge a ~0 con suficientes datos. No hay referencia de qué es "normal" para una entidad o sector.

Esto impide responder: "¿Esta sucursal es cara o barata comparada con las otras sucursales de la misma empresa?"

---

### D5 — Datos de tareas no están en los patrones

El trigger `onWriteTaskRating` ya agrega ratings a `employee.ratingTask`. Sin embargo, `EmployeePattern` y `BranchPattern` no tienen ningún campo de tareas. El motor heurístico ignora completamente:

- Tasas de cumplimiento de plazos (`timeComplianceStatus`)
- Calificaciones por supervisor (`TaskRating`)
- Tasas de rechazo (`validated` vs `rejected`)
- Manejo de prioridades (`critical` vs `low`)

---

## Estado actual de los indicadores

| ID | Nombre | Estado |
|----|--------|--------|
| WTB | Working Time Balance | ✅ Correcto |
| OSD | Operational Shift Deviation | ⚠️ Falsos positivos en multi-turno (D2) |
| HCI | Heuristic Confidence Index | ⚠️ Depende de reliability no separada (D3) |
| OSI | Operational Stability Index | ❌ Usa costVar rota (E2+E3) |
| PSS | Pattern Stability Score | ⚠️ Promedio de dos indicadores con problemas |
| RCV | Relative Cost Variance | ❌ Usa costVar rota (E2+E3) |
| CVH | Cost Variability Heuristic | ❌ Usa costVar rota (E2+E3) |
| CPD | Cost Performance Delta | ⚠️ Auto-referencial, converge a 0 (D4) |
| CRI | Cost Risk Index | ❌ Usa costVar rota (E2+E3) |
| OER | Operational Efficiency Ratio | ✅ Correcto (avgEffectiveCost / avgCycleCost) |
| ECR | Efficiency-to-Cost Ratio | ❌ avgCostEfficiency no es eficiencia (E5) |
| ERP | Efficiency Recovery Potential | ❌ avgCostEfficiency no es eficiencia (E5) |
| ROIh | Return on Hour | ❌ avgCostEfficiency no es eficiencia (E5) |
| CEE | Cost Efficiency Evolution | ❌ avgCostEfficiency no es eficiencia (E5) |
| WLB | Workload Balance | ❌ Fórmula incorrecta (E4) |
| SSR | Smart Stability Ratio | ❌ Hereda E2+E3 via PSS y OER |
| GHI | Global Heuristic Index | ❌ Hereda E2+E3+E5 |
| QHI | Quality Heuristic Index | ❌ Idéntico a GHI (E1) |

**Indicadores sin errores conocidos: WTB, OER** (2 de 18).

---

## Archivos clave y su problema

| Archivo | Problema |
|---------|----------|
| `api-express/src/checkinbiz/application/heuristic/HeuristicCalculator.ts` | E1, E4 — fórmulas WLB y QHI |
| `api-express/src/checkinbiz/application/heuristic/HeuristicCore.ts` | E3 — `HeuristicNormalizer` a eliminar |
| `functions/.../dataProcessing/helper.ts` | E2 — `costVariance`, E5 — `avgCostEfficiency`; D3 — `reliability` sin separar |
| `functions/.../dataProcessing/writeController.ts` | D5 — no integra señales de tareas al patrón |
| `functions/.../onWriteTaskRating.ts` | Trigger existente — base para extender a `taskSignals` |
| `api-express/src/customGPT/infraestructure/promptBuilders/branchInterpret.builder.ts` | No tocar hasta F1 completo |

---

## Hoja de ruta de corrección

El orden de implementación importa. Ver [heuristica-v2-roadmap.md](./heuristica-v2-roadmap.md) para el detalle completo.

```
F1 (correcciones math)  →  F2a (separar reliability)  →  F2b (WLB real)
     ↓
F3a (task signals en patterns)  →  F3b (nuevos indicadores TAC/TQI/TRI/PTC)
     ↓
F4 (arquetipos de perfil)  →  F2c (OSD multi-turno)  →  F5 (Merlin prompt)
```

**No saltarse F1.** Todo lo demás construye sobre estos cimientos.

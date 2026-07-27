# Heurística — Changelog de implementación

Registro de lo que se hizo, qué se resolvió y qué archivos tocó cada fase.
Para el diseño completo ver [heuristica-v2-roadmap.md](./heuristica-v2-roadmap.md).
Para el diagnóstico del estado anterior ver [heuristica-diagnostico-v3.md](./heuristica-diagnostico-v3.md).

---

## Fase F1 — Correcciones matemáticas

> **Branch:** `feat/heuristic-v2-task-integration`
> **Fecha:** 2026-06-05
> **Build:** ✅ `functions/` y `api-express/` compilan sin errores tras los cambios

### Qué se hizo

#### F1.1 — costVariance reemplazado por Welford

**Problema:** `costVariance = |costCycle - avgCycleCost|` era la desviación absoluta de un único punto, no una varianza estadística. Fluctuaba punto a punto y su valor dependía de cuánto difería el último ciclo del promedio EMA, lo que lo hacía inestable.

**Solución:** Se usa el mismo algoritmo Welford incremental que ya existía para `stdStartHour`. Ahora el patrón acumula `costM2` (acumulador interno) y calcula:
- `costStd` = desviación estándar real de los costes por ciclo (σ, en la misma unidad que `avgCycleCost`)
- `costCV` = coeficiente de variación = `costStd / avgCycleCost` — escala operativa interpretable (0.2 = 20% de variación, > 0.5 = alta dispersión)

El campo `costVariance` se conserva por retrocompatibilidad pero ahora almacena el CV (mismo valor que `costCV`). Todos los indicadores V2 usan `costCV` directamente.

**Archivo:** `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/helper.ts`

---

#### F1.2 — HeuristicNormalizer eliminado

**Problema:** El `HeuristicNormalizer` convertía `costVariance` a rango 0..1 antes de enviarlo al `HeuristicCalculator`. Luego el Calculator dividía ese número 0..1 entre `avgCycleCost` (en €), produciendo un `relativeCostVar` sin dimensión operativa que hacía que OSI, CVH, CRI, WLB, PSS, SSR, GHI usaran un input incorrecto.

**Solución:** Se elimina la clase `HeuristicNormalizer` completa. El patrón llega directamente al `HeuristicCalculator` sin transformación previa. Los indicadores ahora usan `costCV` (ya en escala operativa por construcción) via `boundedCostVar = min(costCV, 2)`.

**Archivos:**
- `functions/src/services-saas/checkinbiz/application/heuristic/HeuristicCore.ts`
- `api-express/src/checkinbiz/application/heuristic/HeuristicCore.ts`

---

#### F1.3 — reliability separada en dataMaturity + dataQuality

**Problema:** `reliability` mezclaba dos métricas distintas: cuántos datos tiene el patrón (madurez por volumen) y qué tan buenos son esos datos (calidad de fichaje). Imposible distinguir "sucursal nueva con fichajes perfectos" de "sucursal antigua con fichajes malos".

**Solución:** Se calculan y almacenan por separado:
- `dataMaturity` = `BASE + (1-BASE) * min(1, log1p(dataPoints) / log1p(100))` — crece logarítmicamente con el número de ciclos, independiente de la calidad. Llega a ~1.0 con ~100 ciclos.
- `dataQuality` = EMA de `consistencyScore × distanceFactor` — calidad de cada ciclo individual (completitud de eventos × precisión GPS). Se actualiza en cada checkout.
- `reliability` = EMA de `dataMaturity × cycleQuality` — se mantiene como campo compuesto para retrocompatibilidad con código existente.

**Archivo:** `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/helper.ts`

---

#### F1.4 — WLB redefinido como adherencia de jornada real

**Problema:** `WLB = (workHours × avgCostEfficiency) / (1 + boundedCostVar)` era eficiencia ponderada por varianza de coste. El label "Underload/Overload" era ficticio porque la fórmula no comparaba horas reales vs horas planificadas.

**Solución:** `WLB = workHours / avgScheduledHours`
- `avgScheduledHours` es la EMA de las horas planificadas para cada día, derivadas del `WorkSchedule` configurado en la sucursal. Se calcula en `writeController.ts` en cada checkout.
- WLB = null si la sucursal no tiene `WorkSchedule` configurado (el indicador no aparece en los resultados).
- Escala: 0.95-1.05 = óptimo, < 0.85 = infrautilización, > 1.10 = horas extra sistemáticas, máx. clamped a 2.0.

**Archivos:**
- `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/writeController.ts` (calcula `scheduledHoursToday` y lo pasa a `calculatePatternStats`)
- `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/helper.ts` (recibe `scheduledHours` y calcula `newAvgScheduledHours`)
- `functions/src/services-saas/checkinbiz/application/heuristic/HeuristicCalculator.ts`
- `api-express/src/checkinbiz/application/heuristic/HeuristicCalculator.ts`

---

#### F1.5 — QHI redefinido (ya no es idéntico a GHI)

**Problema:** `QHI = (GHI + ECR + OSI + HCI) / 4` es algebraicamente idéntico a `GHI = (ECR + OSI + HCI) / 3`. Los dos indicadores producían el mismo número.

**Solución (placeholder hasta F3):** `QHI = (dataMaturity + dataQuality + OER) / 3`

QHI ahora mide "¿qué tan confiable es este patrón para tomar decisiones?": madurez del patrón por volumen + calidad de datos + eficiencia operativa básica. Es genuinamente distinto de GHI que mide eficiencia + estabilidad operativa + confianza.

En F3 (task signals), QHI será reemplazado por el índice de calidad de tareas `(TAC + TQI + (1-TRI)) / 3`.

**Archivos:**
- `functions/src/services-saas/checkinbiz/application/heuristic/HeuristicCalculator.ts`
- `api-express/src/checkinbiz/application/heuristic/HeuristicCalculator.ts`

---

#### F1.6 — PSS redefinido (separación real de estabilidad de patrón)

**Problema:** `PSS = (OSI + HCI) / 2` promediaba dos indicadores que dependen los dos de `reliability` y `boundedCostVar`. No añadía información independiente.

**Solución:** `PSS = (dataMaturity + dataQuality) / 2` — mide directamente la estabilidad del patrón de datos: qué tan maduro es (volumen) y qué tan limpio es (calidad). Esto le da a PSS un significado operativo propio.

**Archivos:** mismos que F1.5.

---

#### F1.7 — Interfaces extendidas

Se añaden los nuevos campos a `BranchPattern` y `EmployeePattern` en ambas copias (functions y api-express):

```typescript
// V2 — Reliability decomposed
dataMaturity?: number;   // 0..1
dataQuality?: number;    // 0..1

// V2 — Cost statistics (Welford)
costM2?: number;         // acumulador interno Welford
costStd?: number;        // σ del coste por ciclo
costCV?: number;         // coeficiente de variación

// V2 — Scheduling (solo BranchPattern)
avgScheduledHours?: number;

// V2 — Archetype
profileType?: BranchProfileType | EmployeeProfileType;
```

Se añaden los tipos `BranchProfileType` y `EmployeeProfileType` con todos los valores de arquetipos definidos en el roadmap.

Los campos legacy (`costVariance`) se mantienen con comentario `// legacy: use costCV for new logic`.

**Archivos:**
- `functions/src/services-saas/checkinbiz/domain/entities/Branch.ts`
- `functions/src/services-saas/checkinbiz/domain/entities/Employee.ts`
- `api-express/src/checkinbiz/domain/entities/Branch.ts`
- `api-express/src/checkinbiz/domain/entities/Employee.ts`

---

### Estado de los indicadores tras F1

| ID | Estado antes | Estado tras F1 |
|----|-------------|----------------|
| WTB | ✅ | ✅ sin cambios |
| OSD | ⚠️ multi-turno | ⚠️ pendiente F2c |
| HCI | ⚠️ | ✅ usa reliability correcta |
| OSI | ❌ costVar rota | ✅ usa costCV (Welford) |
| PSS | ⚠️ redundante | ✅ dataMaturity + dataQuality |
| RCV | ❌ costVar rota | ✅ = costCV directamente |
| CVH | ❌ costVar rota | ✅ usa costCV |
| CPD | ⚠️ auto-ref | ⚠️ pendiente benchmarking (F4+) |
| CRI | ❌ costVar rota | ✅ usa costCV |
| OER | ✅ | ✅ sin cambios |
| ECR | ❌ costEfficiency≠eficiencia | ⚠️ usa avgCostEfficiency (limitación conocida hasta F3) |
| ERP | ❌ costEfficiency | ⚠️ igual |
| ROIh | ❌ costEfficiency | ⚠️ igual |
| CEE | ❌ costEfficiency | ⚠️ igual |
| WLB | ❌ fórmula falsa | ✅ horas reales / planificadas (null si sin WorkSchedule) |
| SSR | ❌ heredaba | ✅ usa PSS corregido + OER |
| GHI | ❌ heredaba | ✅ usa OSI corregido |
| QHI | ❌ = GHI | ✅ dataMaturity + dataQuality + OER (≠ GHI) |

**Indicadores corregidos: 12/18. Pendientes de mejora profunda (requieren task signals F3): ECR, ERP, ROIh, CEE.**

---

### Qué NO cambia (retrocompatibilidad)

- `reliability` sigue existiendo y calculándose (código que lo lee fuera del motor heurístico no se rompe).
- `costVariance` se conserva en el patrón (ahora almacena el CV, que es un valor más pequeño que antes — los patrones existentes en Firestore tendrán un valor nuevo en el próximo checkout, no requiere migración).
- El output del endpoint `analyzeHeuristic` mantiene la misma forma JSON.
- Los umbrales de los indicadores en la colección Firestore `checkbiz_heuristic_indicators` **deben revisarse** para OSI, CVH, CRI, RCV, PSS, WLB, QHI — sus escalas han cambiado (ver sección siguiente).

---

### Umbrales de Firestore a revisar

Los umbrales de los indicadores se almacenan en `checkbiz_heuristic_indicators`. Con los cambios de F1, los siguientes indicadores tienen escalas diferentes:

| Indicador | Escala anterior | Escala V2 | Acción recomendada |
|-----------|----------------|-----------|-------------------|
| OSI | 0..1 (basado en costVar rota) | 0..1 (costCV: misma escala, valores más correctos) | Revisar si el threshold `< 0.5 = error` sigue siendo apropiado |
| RCV | 0..∞ (relativo roto) | CV real 0..∞ (CV < 0.2 = estable, > 0.5 = disperso) | Actualizar: success < 0.2, warning 0.2-0.5, error > 0.5 |
| CVH | 0..2 (inestable) | 0..2 (costCV × (1-reliability), más estable) | Revisar umbrales |
| PSS | 0..1 (OSI+HCI) | 0..1 (dataMaturity+dataQuality) | Mantener umbrales (misma escala) |
| WLB | 0..∞ (sin sentido) | 0..2 (ratio real, 1.0 = perfecto) | Actualizar: success 0.9-1.1, warning 0.8-0.9 o 1.1-1.2, error fuera |
| QHI | 0..1 (= GHI) | 0..1 (dataMaturity+dataQuality+OER) | Mantener umbrales (misma escala, diferente significado) |

---

---

## Fase F2 — Integración de señales de tareas en patrones

> **Branch:** `feat/heuristic-v2-task-integration`
> **Fecha:** 2026-06-05
> **Build:** ✅ `functions/` y `api-express/` compilan sin errores

### Qué se hizo

#### F2.1 — Interfaces TaskSignalsBranch y TaskSignalsEmployee

Se añaden dos nuevas interfaces al dominio para encapsular todas las señales derivadas del módulo de tareas:

**`TaskSignalsBranch`** (en `Branch.ts`):
```typescript
{ branchOnTimeRate, branchRejectionRate, branchCompletionRate,
  branchAvgRating, criticalTaskOnTimeRate, taskCount, updatedAt }
```

**`TaskSignalsEmployee`** (en `Employee.ts`):
```typescript
{ avgRating, ratingCount, ratingTrend, taskOnTimeRate, taskStartDelayAvg,
  taskValidationRate, taskRejectionRate, taskCompletionRate,
  priorityWeightedScore, taskCount, updatedAt }
```

Ambas interfaces se incorporan como campos opcionales `taskSignals?` en `BranchPattern` y `EmployeePattern` respectivamente (ambas copias: `functions/` y `api-express/`).

---

#### F2.2 — Trigger `onWriteTaskForPattern`

**Archivo:** `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/onWriteTaskForPattern.ts`

**Path escuchado:** `entities/{entityId}/tasks/{taskId}`

**Condición de disparo:** Solo procesa la transición hacia `validated` o `rejected`. Si `before.status` ya era terminal, no re-procesa (idempotente).

**Lógica de actualización:**

1. **BranchPattern.taskSignals** — EMA de onTimeRate, rejectionRate, completionRate, criticalTaskOnTimeRate (solo si priority = "critical").

2. **EmployeePattern.taskSignals** (branch-scoped + global entity) — EMA de onTimeRate, startDelayAvg (scheduledStartAt → startedAt en minutos), validationRate, rejectionRate, completionRate, priorityWeightedScore.

**priorityWeightedScore:** Score 0-1 que combina prioridad × resultado:
```
critical=1.0 | high=0.75 | medium=0.50 | low=0.25
× outcome: on_time=1.0, late=0.5, rejected=0.0
```

**EMA alpha = 0.15** (convergencia más lenta que checklog porque las tareas son menos frecuentes).

---

#### F2.3 — `onWriteTaskRating` extendido para sincronizar `avgRating` al patrón

**Archivo:** `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/onWriteTaskRating.ts`

Nueva función `syncRatingToPatterns()` que:
1. Tras actualizar `employee.ratingTask` (comportamiento existente), lee el nuevo `ratingTask.average`.
2. Normaliza el rating: `(average - 1) / 4` → escala 0-1.
3. Actualiza `EmployeePattern.taskSignals.avgRating` con EMA (alpha = 0.15) para todos los patrones del empleado en esa entidad.
4. Actualiza `ratingTrend` comparando valor anterior vs nuevo (`+0.01` = up, `-0.01` = down).

---

#### F2.4 — Indicadores TAC, TQI, TRI, PTC en `HeuristicCalculator`

Cuatro nuevos indicadores de tareas para sucursales (ambas copias del calculador):

| ID | Fórmula | Escala | Interpreta |
|----|---------|--------|-----------|
| **TAC** | `branchOnTimeRate × branchCompletionRate` | 0–1 | Adherencia total: en plazo Y validada |
| **TQI** | `branchAvgRating × branchCompletionRate` | 0–1 | Calidad percibida por supervisores |
| **TRI** | `branchRejectionRate` | 0–1 (bajo=mejor) | Tasa de rechazo — riesgo de calidad |
| **PTC** | `criticalTaskOnTimeRate` | 0–1 | Cumplimiento en tareas críticas |

Si `taskSignals` es null o `taskCount = 0`, los cuatro indicadores devuelven 0 (sin datos suficientes, no aparecen en error).

---

#### F2.5 — QHI actualizado con task signals

QHI evoluciona automáticamente según disponibilidad de datos:

- **Con taskSignals** (`taskCount > 0`): `(TAC + TQI + (1-TRI)) / 3` — índice de calidad operativa real
- **Sin taskSignals**: `(dataMaturity + dataQuality + OER) / 3` — fallback de calidad del patrón de datos

Esto hace que QHI mejore gradualmente a medida que se acumula historial de tareas, sin romper sucursales que aún no tienen tareas.

---

### Resumen de señales disponibles tras F2

Los patrones ahora incluyen dos fuentes de verdad independientes:

| Fuente | Frecuencia | Señales |
|--------|-----------|---------|
| Checklog (F1) | Por jornada | timing, costs, reliability, efficiency |
| Tasks (F2) | Por tarea | ratings, compliance, rejection, priority handling |

El motor heurístico combina ambas fuentes en los 22 indicadores resultantes (18 originales + TAC, TQI, TRI, PTC).

---

### Archivos modificados en F2

| Archivo | Cambio |
|---------|--------|
| `functions/.../domain/entities/Branch.ts` | TaskSignalsBranch + BranchPattern.taskSignals |
| `functions/.../domain/entities/Employee.ts` | TaskSignalsEmployee + EmployeePattern.taskSignals |
| `api-express/.../domain/entities/Branch.ts` | igual |
| `api-express/.../domain/entities/Employee.ts` | igual |
| `functions/.../onWriteTaskForPattern.ts` | nuevo trigger |
| `functions/.../onWriteTaskRating.ts` | +syncRatingToPatterns |
| `functions/.../firebase-firestore-trigger/index.ts` | export onWriteTaskForPattern |
| `functions/.../heuristic/HeuristicCalculator.ts` | TAC, TQI, TRI, PTC, QHI actualizado |
| `api-express/.../heuristic/HeuristicCalculator.ts` | igual |

---

---

## Fase F3 — Arquetipos de perfil (profileType)

> **Branch:** `feat/heuristic-v2-task-integration`
> **Fecha:** 2026-06-06
> **Build:** ✅ `functions/` y `api-express/` compilan sin errores

### Qué se hizo

#### F3.1 — ProfileClassifier.ts (módulo puro, sin dependencias Firestore)

Creado en ambas copias (`functions/` y `api-express/`) como clase estática con dos métodos:

**`classifyBranch(pattern: BranchPattern): BranchProfileType`**

| Perfil | Condición |
|--------|-----------|
| `data-weak` | `dataMaturity < 0.4` O `dataQuality < 0.35` — primera en chequearse |
| `multi-shift-stable` | OSD > 1.0h global PERO ≥ 2 días con std < 0.4h cada uno (multi-turno bien definido) |
| `elite` | OSD < 0.5h AND TAC > 0.85 AND reliability > 0.85 AND ≥ 5 tareas |
| `discipline-gap` | reliability > 0.75 AND branchRejectionRate > 0.2 AND ≥ 5 tareas |
| `understaffed` | WTB < 7h AND branchOnTimeRate < 0.6 AND ≥ 5 tareas |
| `seasonal-volatile` | rango de weeklyWorkAvg entre días > 2h |
| `neutral` | resto |

**`classifyEmployee(pattern: EmployeePattern): EmployeeProfileType`**

| Perfil | Condición (en orden de prioridad) |
|--------|----------------------------------|
| `ghost` | dataPoints < 20 O reliability < 0.3 |
| `at-risk` | taskCount ≥ 5 AND (onTimeRate < 0.6 O avgRating < 0.375) |
| `compliance-risk` | reliability ≥ 0.7 AND taskRejectionRate > 0.25 AND ≥ 5 tareas |
| `anchor` | reliability ≥ 0.8 AND onTimeRate ≥ 0.85 AND avgRating ≥ 0.75 AND ≥ 5 tareas |
| `high-potential` | experienceYears < 1 AND avgRating ≥ 0.75 AND onTimeRate ≥ 0.80 AND ≥ 3 tareas |
| `specialist` | 1-2 tipos de trabajo AND avgRating ≥ 0.75 AND ≥ 5 tareas |
| `maverick` | OSD > 0.8h AND avgRating ≥ 0.75 AND ≥ 5 tareas |
| `neutral` | resto |

Los umbrales están centralizados en el objeto `THRESHOLDS` del archivo para facilitar ajuste sin tocar la lógica.

**Nota sobre `avgRating`:** Está normalizado 0-1 (`(stars-1)/4`). Por tanto:
- 0.75 = 4.0 estrellas
- 0.375 = 2.5 estrellas

---

#### F3.2 — HeuristicCore incluye profileType en el resultado

`HeuristicCore.analyzeBranch()` ahora retorna:
```typescript
{ branchId, reliability, dataPoints, dataMaturity, dataQuality, profileType, results }
```

El `profileType` se calcula al vuelo sobre el patrón completo, ya con los resultados de los indicadores disponibles.

---

#### F3.3 + F3.4 — profileType persistido en Firestore

El clasificador se llama tras consolidar cada patrón para guardar el perfil actualizado:
- `writeController.ts` → persiste `profileType` en los 3 patrones (branch, employee-branch, employee-global) en cada checkout
- `onWriteTaskForPattern.ts` → reclasifica y persiste `profileType` en la misma transacción que actualiza `taskSignals`

Esto asegura que `profileType` en Firestore siempre refleja el estado más reciente sin necesidad de llamadas adicionales.

---

#### F3.5 — profileType en el contexto de Merlin

`interpretBranches.ts` pasa `profileType`, `dataMaturity` y `dataQuality` al `interpretUseCase.execute()`.

`branchInterpret.builder.ts` usa `profileType` para:

1. **Contexto numérico:** añade `profileType=elite`, `dataMaturity=90%`, `dataQuality=49%` a la línea de Context del user prompt.

2. **Guía de tono por perfil:**

| profileType | Tono que recibe el AI |
|-------------|----------------------|
| `elite` | Consolidación. Resaltar lo que funciona y cómo replicarlo |
| `data-weak` | Cauteloso. No diagnosticar operaciones. Centrarse en mejorar datos |
| `discipline-gap` | Directo. Raíz del rechazo de tareas |
| `understaffed` | Operacional. Revisar headcount / reasignación de turnos |
| `multi-shift-stable` | Informativo. NO señalar OSD como problema (es estructural) |
| `seasonal-volatile` | Planificación. Revisar scheduling semanal |
| `neutral` | Balanceado estándar |

El AI recibe exactamente esto: `Profile guidance: Branch profile: discipline-gap. Attendance is reliable but task quality is low. Tone: direct. Focus on execution quality and task rejection root causes.`

---

### Impacto en el output de Merlin

Antes de F3, Merlin siempre producía el mismo párrafo de "revisar turnos y fichajes" porque no tenía contexto de qué tipo de sucursal estaba analizando.

Con F3:
- Una sucursal `data-weak` recibe respuesta sobre cómo mejorar la calidad de datos, no análisis operativo
- Una sucursal `elite` recibe respuesta de consolidación, no alarmas
- Una sucursal `multi-shift-stable` no recibe "redesign shifts" aunque su OSD sea > 1.0h

---

### Archivos creados/modificados en F3

| Archivo | Cambio |
|---------|--------|
| `functions/.../heuristic/ProfileClassifier.ts` | nuevo — lógica pura de clasificación |
| `api-express/.../heuristic/ProfileClassifier.ts` | nuevo — copia para el servicio |
| `functions/.../heuristic/HeuristicCore.ts` | retorna profileType + dataMaturity + dataQuality |
| `api-express/.../heuristic/HeuristicCore.ts` | igual |
| `functions/.../dataProcessing/writeController.ts` | persiste profileType en 3 patrones por checkout |
| `functions/.../onWriteTaskForPattern.ts` | reclasifica profileType en cada task terminal |
| `api-express/.../gpt/application/interpretBranches.ts` | pasa profileType/dataMaturity/dataQuality al interpret |
| `api-express/.../promptBuilders/branchInterpret.builder.ts` | profileGuidance + contexto numérico de perfil |

---

## Estado del branch tras F1+F2+F3

| Fase | Estado | Commits |
|------|--------|---------|
| F1 — Correcciones matemáticas | ✅ | `b9131db` |
| F2 — Task signals en patrones | ✅ | `f79d4fc` |
| F3 — Arquetipos de perfil | ✅ | `e3cd7b7` |
| F4 — OSD multi-turno (pendiente) | ⏳ | — |
| F5 — Merlin prompt upgrade (pendiente) | ⏳ | — |

## Próximas fases

- **F4 (OSD multi-turno):** ya no es crítico porque `ProfileClassifier.isMultiShiftStable()` en F3 detecta el caso y el `multi-shift-stable` profileType instruye a Merlin a no señalar OSD como problema. Evaluar si vale la pena el esfuerzo de rediseñar OSD por grupo de turno.
---

## Fase F5 — Merlin: diagnóstico real con datos numéricos

> **Branch:** `feat/heuristic-v2-task-integration`
> **Fecha:** 2026-06-06
> **Build:** ✅ `api-express/` compila sin errores
> **Commit:** `a7195cb`

### Qué se hizo

Reescritura completa de `api-express/src/customGPT/infraestructure/promptBuilders/branchInterpret.builder.ts`.

---

#### El cambio fundamental: de "describir" a "diagnosticar"

**Antes (V1):**
- El AI recibía 18 indicadores con labels genéricos (`status=error; consequence: High dispersion`)
- `patternSummary = "N/A (metrics omitted)"` — sin datos reales del patrón
- El AI producía: *"Hay dispersión de arranques → revisar turnos"*

**Después (F5):**
- El AI recibe los valores numéricos reales del `BranchPattern`
- El AI produce: *"El 68% de los arranques caen entre las 07:00 y las 10:00 (±88min respecto a la media de 08:30), lo que indica ausencia de ventana horaria definida"*

---

#### 1. Nuevo system prompt — enfoque diagnóstico

**Antes:** "Your role is to explain operational signals to a business user"
**Ahora:** "Your job: DIAGNOSE root causes and prescribe specific actions — not describe what the indicators say"

Instrucciones de diagnóstico añadidas:
- Preguntar WHY antes de reportar WHAT
- Cross-referenciar señales de timing con calidad de datos: si `dataQuality < 50%`, las anomalías de timing pueden ser ruido, no problemas reales
- Si la mayoría de errores vienen de baja `dataQuality`, diagnosticar calidad de datos, no operaciones
- Conectar 2-3 señales en una historia coherente, no listar observaciones aisladas

**Tabla de umbrales** incluida en el system prompt:
```
OSD: < 0.5h = disciplinado | 0.5-1.0h = moderado | > 1.0h = severo
WTB: 7.5-9.0h = normal | < 6.5h = infrautilización | > 9.5h = horas extra sistemáticas
dataQuality: > 75% = fiable | 50-75% = parcial | < 50% = validar antes de actuar
costCV: < 20% = estable | 20-50% = normal | > 50% = alta volatilidad
taskOnTimeRate: > 85% = alto | 70-85% = aceptable | < 70% = problema de planificación
taskRejectionRate: < 10% = sano | 10-25% = investigar | > 25% = problema sistémico
rating (0-1): > 0.75 = excelente (4★+) | 0.50-0.75 = bueno | < 0.375 = crítico (< 2.5★)
```

---

#### 2. Bloque de valores reales del patrón (el salto clave)

Antes: `patternSummary = "N/A (metrics omitted; base on heuristics only)"`

Ahora el AI recibe un bloque como este:
```
Pattern values (use these numbers in your diagnosis):
- Timing: avg start 08:30, avg end 17:06, avg workday 8.4h
- Start dispersion: +/-89min global, end +/-34min
- Dispersion by day (start): Lun=+/-18min, Mar=+/-22min, Mie=+/-108min, Jue=+/-31min, Vie=+/-40min
- Hours by weekday: Lun=8.2h, Mar=8.5h, Mie=7.1h, Jue=8.6h, Vie=8.8h
- Scheduled hours/day: 8.0h
- Cost variability (CV): 18%
- Data: 196 cycles, maturity=90%, quality=49%
- Task on-time rate: 82% (47 tasks)
- Task rejection rate: 5%
- Avg supervisor rating: 3.9★
```

El AI ahora puede decir: *"El miércoles concentra la mayor dispersión de arranques (±108min) y la jornada más corta (7.1h), lo que sugiere un turno específico con problemas de puntualidad ese día."*

Campos extraídos de `BranchPattern`:
- `avgStartHour`, `avgEndHour` → formateados como HH:MM
- `stdStartHour`, `stdEndHour` → convertidos a minutos
- `stdStartByDay[]` → desglose por día con std en minutos (solo días con ≥ 3 registros)
- `weeklyWorkAvg[]` → horas por día de la semana
- `avgScheduledHours` → horas planificadas del WorkSchedule
- `costCV` → como porcentaje
- `avgDistance` → en metros
- `taskSignals` → onTimeRate, rejectionRate, branchAvgRating (en ★), criticalTaskOnTimeRate

---

#### 3. Pre-filtrado de heurísticos por severidad

Antes: el AI recibía los 18 indicadores con igual peso.

Ahora:
- **Máx 5 errores** (los más críticos)
- **Máx 3 warnings** (secundarios)
- **Máx 2 successes** (para la nota positiva)

Formato simplificado:
```
Priority issues:
- [ERROR] OSI (Low stability); High instability or erratic data
- [ERROR] WLB (Underload); Low efficiency due to idleness

Watch:
- [WARNING] GHI (Alert); General performance deterioration

Working well:
- [SUCCESS] WTB (Balanced); Productive workday
```

El AI ya no recibe 18 señales de igual peso — se fuerza a profundizar en los 5 problemas reales.

---

#### 4. Guía de tono por perfil (mejorada)

La `profileGuidance` es ahora parte del user prompt con instrucción explícita:

| profileType | Instrucción al AI |
|-------------|-------------------|
| `data-weak` | Do NOT diagnose operations. Only recommend improving data collection |
| `multi-shift-stable` | High global dispersion is STRUCTURAL. Do NOT flag start dispersion |
| `elite` | Consolidate and replicate what works |
| `discipline-gap` | Focus on task execution and rejection root causes |
| `understaffed` | Headcount or shift allocation issues |
| `seasonal-volatile` | Focus on weekly scheduling |
| `neutral` | Standard balanced analysis |

---

#### Lo que se eliminó

- `FORBIDDEN_TERMS` y `ALLOWED_CONCEPTS` imports — ya no son necesarios, el system prompt los cubre mejor
- Reglas duplicadas (la misma regla de "no tareas" aparecía 2 veces en el V1)
- El `MAX_HEURISTICS = Number.MAX_SAFE_INTEGER` — ahora hay límites reales
- `commonVocabulary.ts` import — ya no se usa en este builder

---

### Impacto esperado en el output de Merlin

| Aspecto | Antes (V1) | Después (F5) |
|---------|-----------|-------------|
| Especificidad | Genérico ("revisar turnos") | Específico ("±89min en arranques globales; miércoles concentra el 40% de la dispersión") |
| Root cause | Síntoma ("hay dispersión") | Causa ("miércoles con jornada corta y alta dispersión → turno sin definir") |
| Datos | Solo labels de indicadores | Valores numéricos reales (horas, %, estrellas) |
| Volumen | 18 señales por igual | 5 errores + 3 warnings + 2 successes |
| Tono | Genérico universal | Ajustado al profileType de la sucursal |
| dataQuality < 50% | Igual análisis operativo | Solo diagnóstico de calidad de datos |

---

## Estado final del branch `qa/heuristic-v2-task-integration`

| Fase | Qué resuelve | Estado |
|------|-------------|--------|
| **F1** | 12 indicadores con matemáticas correctas (Welford, WLB real, QHI!=GHI) | ✅ |
| **F2** | Task signals en patrones + 4 indicadores de tarea + QHI basado en tareas | ✅ |
| **F3** | 8 arquetipos empleado + 6 sucursal, persistidos en Firestore, Merlin con tono por perfil | ✅ |
| **F5** | Merlin diagnóstico real: valores numéricos, pre-filtrado, umbrales, root cause | ✅ |
| **F4** | OSD calculado por grupo de turno | ⏭️ Deprioritizado — mitigado por archetype `multi-shift-stable` en F3 |

**Nota de nombres Firebase:** Las tres funciones de trigger superaban el límite de 62 caracteres y fueron renombradas en los exports:
- `onWriteBranchPattern` → export `onBranchPattern` (60 chars)
- `onWriteEmployeePattern` → export `onEmpPattern` (57 chars)
- `onWriteTaskForPattern` → export `onTaskPattern` (58 chars)

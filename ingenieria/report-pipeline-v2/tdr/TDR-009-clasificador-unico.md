# TDR-009 — Un solo clasificador de perfiles, con la base de tiempo en el patrón

**Fecha:** 2026-11-09
**Estado:** Implementado en `fix/perfiles-contra-el-plan` (encodebiz-api), sin desplegar
**Componentes:** `packages/shared/src/analysis/profileClassifier.ts`, `packages/shared/src/analysis/planTiming.ts`, `services/firebase_sdk/src/fichaje/writeController.ts`, `services/analytics/src/application/heuristic/ProfileClassifier.ts` (alias), `services/merlin/src/modules/domain/employeeProfile.ts`
**Continúa:** TDR-008 (variabilidad contra el plan)

---

## Problema

Había tres clasificadores de perfil (arquetipo) que debían decir lo mismo y no lo hacían:

| Dónde | Qué hacía | Qué fallaba |
|---|---|---|
| `firebase_sdk/patrones/ProfileClassifier.ts` | Corre en `onChecklogWrite` con cada salida y guarda `profileType` en `checkbiz_branch_patterns` y `checkbiz_employee_patterns`. | Medía la variabilidad con la **hora del reloj** (`stdStartHour`/`stdEndHour`). En «Por tareas» la hora de entrada cambia cada día porque cambia el plan. |
| `analytics/heuristic/ProfileClassifier.ts` | Copia de la anterior, con la vista contra el plan del TDR-008 y las tareas del espejo. | Misma tabla, otra copia; `(ts.branchOnTimeRate ?? 0)` convertía una señal ausente en un 0. |
| `merlin/modules/domain/employeeProfile.ts` (`classifyQuadrant`) | Cuadrante de la ficha de persona, con su propia tabla de cinco etiquetas. | `costTrend === "down"` ⇒ AT-RISK; `efficiencyIndex < 0.35` ⇒ GHOST; umbrales de dispersión (0,2 h) que no existían en ningún otro sitio. |

Medido el 2026-11-09 en staging con SaludStart (`318Ey5ZHBMeqm5fsQ0Md`, 29 personas «Por tareas», ciclos de 90-150 min, unas 3 tareas por persona y día; la gente entra a ±6 min del plan y el 93 % de las entradas cae en tolerancia):

- `profileType` guardado: `maverick` en **50 de 65** patrones de persona (26 de 29 globales).
- Cuadrante de Merlin: **AT-RISK para 10 de 29**, por `costTrend: "down"` (un coste que baja no es un riesgo de la persona) y por trabajar al ~90 % del plan.
- Señales sin base: `criticalTaskOnTimeRate: 0` sin tareas críticas, `avgRating: 0` sin valoraciones, `branchAvgRating: 0` que ningún trigger escribe.

## Decisión

### 1. Una sola función, en `shared`

`packages/shared/src/analysis/profileClassifier.ts` exporta `profileEmployee`, `profileBranch` (devuelven el perfil **con la base y la regla que decidió**), `classifyEmployee`, `classifyBranch` y una clase `ProfileClassifier` con los dos estáticos para no tocar las llamadas existentes. Los tres sitios la consumen:

- **firebase_sdk**: `patrones/ProfileClassifier.ts` queda como alias. `writeController.ts` y `onWriteTaskForPattern.ts` no cambian su llamada.
- **analytics**: `heuristic/ProfileClassifier.ts` queda como alias; `HeuristicCore` no cambia.
- **merlin**: `classifyQuadrant(pattern, tasks)` = `QUADRANT_OF[profileEmployee(pattern, tasks).profileType]`. Los ocho arquetipos se pliegan en los cinco cuadrantes que conoce el front (`anchor`, `high-potential`, `specialist` → ANCHOR; `at-risk`, `compliance-risk` → AT-RISK; `maverick`, `ghost`, `neutral` tal cual). El arquetipo completo y su motivo van en `evidence.archetype` / `evidence.archetypeReason`.

### 2. La base de tiempo viaja en el patrón: `timingBasis`, `planTiming`, `planWindow`

El trigger no puede leer Postgres, pero cada salida trae en el fichaje de entrada su `scheduleApplied` (el turno o la tarea que se aplicó al fichar, congelado). `writeController.ts` resuelve la **observación del ciclo contra su plan** (`observePlanCycle`, en `planTiming.ts`: desvío de entrada y salida en minutos, si entró en tolerancia, horas trabajadas y planificadas, fuente) y la acumula en el patrón:

```
planWindow:  { v: 1, size: 60, recent: [obs | null, …], cyclesSeen, updatedAt }   // últimos 60 ciclos; null = sin plan
planTiming:  PlanTiming   // el mismo resumen que da el espejo (TDR-008): basis, dispersión P10–P90, mediana, puntualidad, cobertura
timingBasis: "plan" | "clock"
```

`summarizePlanWindow` y `computePlanTiming` (espejo) comparten la función `summarizePlanObservations`: **misma matemática, mismos mínimos** (≥ 10 ciclos con plan y ≥ 50 % de los ciclos). Sesenta ciclos son unas cuatro semanas en «Por tareas» y unos tres meses con un ciclo al día, del orden de los 90 días del espejo. Se guardan observaciones y no acumuladores para poder calcular la dispersión robusta (P10–P90) y para que un fichaje atípico salga de la ventana en vez de quedarse para siempre (una EMA o Welford lo arrastrarían).

Las tres lecturas de la base, por prioridad:

1. **analytics** (`HeuristicCore`): `applyPlanTiming(pattern, timing)` con el espejo de 90 días; la vista ahora lleva `timingBasis: "plan"` y `planTiming`. Si el espejo no da plan, la vista es el documento tal cual, con la base que guardó el trigger.
2. **merlin** (`withPlanTiming`): igual; si el espejo no da plan y el documento trae `timingBasis: "plan"`, se respeta el del trigger.
3. **trigger**: lo acumulado en el propio patrón.

El clasificador lee `timingBasis`: con `plan`, la dispersión es `planTiming.startSpreadMin / 60` (o `stdStartHour` si la vista ya lo volcó ahí) y existen `punctuality` y `planCoverage`; con `clock`, `stdStartHour`/`stdEndHour` del patrón y ninguna de las dos.

### 3. Sin dato ⇒ null ⇒ la regla no aplica

Cada señal pasa por `known()` (número finito o null). La valoración solo existe con `ratingCount > 0`; las señales de tareas solo con `taskCount > 0`; la evidencia del espejo (`TaskEvidence`) manda sobre las EMA del patrón cuando la trae. Una regla con una señal null no se cumple ni se incumple: se salta.

### 4. `costTrend` fuera de la clasificación

Se quita de los tres sitios. El coste medio por ciclo baja cuando la persona hace ciclos más cortos, cuando cambia de puesto o cuando el patrón madura; no describe un riesgo de la persona. Sigue en `evidence.costTrend` y en `clean.operational_metrics.cost_trend` para quien lo quiera leer.

## Tabla de reglas final

Umbrales en `PROFILE_THRESHOLDS`. «Disp.» es la suma de la dispersión de entrada y de salida, en horas, en la base que toque. El orden importa: gana la primera.

### Persona

| # | Perfil | Regla | Umbral y por qué |
|---|---|---|---|
| 1 | `ghost` | `dataPoints < 20` o sin `reliability` o `reliability < 0,3` | 20 = mínimo con el que `HeuristicCore` responde «datos insuficientes». |
| 2 | `at-risk` | `reliability < 0,5` **o** (≥ 5 tareas y (en plazo < 60 % **o** valoración < 2,5★)) | Reliability es madurez × calidad del fichaje: por debajo de 0,5 con ≥ 20 ciclos hay fichajes incompletos o fuera de zona. Las de tareas solo con dato. |
| 3 | `compliance-risk` | `reliability ≥ 0,7` y ≥ 5 tareas y rechazos > 25 % | Sin cambio. Solo con veredicto. |
| 4 | `anchor` | `reliability ≥ 0,8` y disp. < 0,8 h y (puntualidad desconocida o ≥ 80 %) y (sin tareas o (en plazo desconocido o ≥ 85 %) y (valoración desconocida o ≥ 4★)) | **Nuevo:** puntualidad ≥ 80 % cuando se conoce (uno de cada cinco fuera de hora no es un pilar). El `neutral` dice qué impidió el anchor. |
| 5 | `high-potential` | experiencia < 1 año y ≥ 3 tareas y valoración ≥ 4★ y en plazo ≥ 80 % | Sin cambio. Exige valoraciones. |
| 6 | `specialist` | 1-2 puestos y ≥ 5 tareas y valoración ≥ 4★ | Sin cambio. Exige valoraciones. |
| 7 | `maverick` | disp. > 0,8 h y `reliability ≥ 0,7` y (valoración desconocida o ≥ 4★) | Con base plan es irregularidad **frente al plan** (TDR-008 mantiene la escala). Con reloj, como antes. |
| 8 | `neutral` | resto | Con el motivo: qué le faltó para anchor. |

### Sucursal

| # | Perfil | Regla | Umbral y por qué |
|---|---|---|---|
| 1 | `data-weak` | `dataPoints < 20` o sin `reliability` o `dataQuality < 0,35` | **Cambia:** antes `dataMaturity < 0,4` (≈ 3 ciclos) y a partir del cuarto ya opinaba. Mismo mínimo que la persona y que `HeuristicCore`. |
| 2 | `multi-shift-stable` | **solo reloj:** disp. > 1 h y ≥ 2 días de la semana con ≥ 3 ciclos y σ < 0,4 h | Con plan, el plan ya absorbe los turnos. |
| 3 | `elite` | disp. < 0,5 h y `reliability > 0,85` y (puntualidad desconocida o ≥ 85 %) y (sin tareas o onTime × completion desconocido o > 0,85) | **Cambia:** una señal de tareas ausente ya no vale 0 (antes bloqueaba `elite` a toda sucursal sin `taskSignals`). **Nuevo:** puntualidad ≥ 85 % con plan. |
| 4 | `discipline-gap` | `reliability > 0,75` y ≥ 5 tareas y rechazos > 20 % | Sin cambio. |
| 5 | `understaffed` | ≥ 5 tareas y en plazo < 60 % **y**, solo con reloj, ciclo medio corto (< 80 % de `avgScheduledHours` si se conoce, si no < 7 h) | **Cambia:** vuelve a la regla documentada (`heuristica.md` §5.1 exigía las tres; el código devolvía `understaffed` con `taskCount = 0`). Un ciclo corto solo es un turno de 4 h o una tarea de hora y media. Con plan la duración del ciclo no dice nada. |
| 6 | `seasonal-volatile` | **solo reloj:** > 2 h entre el día de la semana con más y menos horas por ciclo, contando días con ≥ 3 ciclos | **Cambia:** un sábado con un ciclo no es una estación. Con plan, la variación entre días es la del plan. |
| 7 | `neutral` | resto | |

## Resultado con SaludStart (staging, 2026-11-09, solo lectura)

Script: `scratchpad/perfiles/comparar.js` (reconstruye la ventana del trigger a partir de los fichajes de Firestore y clasifica con el código de `origin/develop` y con el nuevo).

| | Guardado / viejo | Merlin viejo | Nuevo (trigger) | Merlin nuevo |
|---|---|---|---|---|
| 29 personas (patrón global) | 26 `maverick`, 2 `neutral`, 1 `at-risk` | 13 `anchor`, 6 `neutral`, **10 `at-risk`** | **17 `anchor`, 11 `neutral`, 1 `at-risk`** | igual que el trigger |
| 65 patrones de persona (global + sucursal) | 50 `maverick`, 8 `neutral`, 5 `ghost`, 2 `at-risk` | — | 31 `anchor`, 27 `neutral`, 5 `ghost`, 2 `at-risk` | — |
| Badalona | `neutral` (oscilaba a `understaffed`) | — | `elite` (disp. 11 min contra el plan, puntualidad 93 %, cobertura 92 %, tareas 0,91) | — |
| Barcelona | `neutral` | — | `elite` (disp. 18 min, puntualidad 93 %, cobertura 90 %) | — |

Las 11 `neutral` lo son por una de dos razones, y el motivo lo dice: `reliability` entre 0,66 y 0,8 (25-42 ciclos: aún no hay historial para «pilar») o tareas en plazo entre 75 % y 83 % según la EMA del patrón (< 85 %). El único `at-risk` es el empleado del owner (23 tareas, 49 % en plazo, 74 % de cobertura): observado en la siembra, no un artefacto. La base es `plan` para los 29 y las 2 sucursales (914 y 486 ciclos con plan en 90 días).

## Lo que no cambia / queda abierto

- **Los `profileType` ya guardados** siguen diciendo `maverick` hasta que cada patrón reciba una salida (el trigger reclasifica con cada ciclo) y **acumule 10 ciclos con plan** en `planWindow`. Para no esperar, hay que recalcular: recorrer los ciclos cerrados de cada patrón en orden y aplicar `pushPlanObservation`/`summarizePlanWindow`, escribir `planWindow`, `planTiming`, `timingBasis` y `profileType`. `comparar.js` ya hace el cálculo (solo lectura); falta el `--apply`.
- **`taskOnTimeRate` del patrón es una EMA (α = 0,15, ~13 tareas de memoria efectiva)**: con un 10 % de tareas tardías oscila entre 0,75 y 0,95. En analytics y merlin manda la evidencia del espejo (recuentos de 90 días); el trigger solo tiene la EMA, así que el `profileType` guardado puede diferir del de la heurística en las personas cerca del 85 %. Mejora propuesta: que `onWriteTaskForPattern` acumule recuentos (`onTimeCount`, `lateCount`) además de la EMA.
- **Las sucursales no tienen evidencia de tareas del espejo** en analytics (`fetchTaskEvidence` solo admite `employeeId`). Propuesta: ampliar la consulta a `branchId` y pasarla a `classifyBranch` desde `heuristic.router.ts`.
- `skillLevel` y `promotionScore` siguen llevando dentro la variabilidad del reloj (TDR-008).
- `BuildPatternSnapshot` copia `raw_pattern` entero: ahora incluye `planWindow` (~60 observaciones, ~4 KB). Propuesta: excluirlo del `raw_pattern` del snapshot y añadir `timingBasis` y `planTiming` a `extractHeuristicScores`.
- El prompt de Merlin describe GHOST como «present but low value»; el clasificador lo define como «sin datos para clasificar» (< 20 ciclos o `reliability < 0,3`). Hay que alinear el texto.

# Módulo Heurística V2 — Referencia Canónica

> Versión activa: **V2** (F1+F2+F3+F5 implementados, en producción desde 2026-07-03)
> Rama: `main` (merge desde `qa/heuristic-v2-task-integration` completado)
> Última actualización: 2026-07-03
> Changelog detallado: [heuristica-changelog.md](./heuristica-changelog.md)

---

## 1. Resumen

El motor heurístico convierte dos fuentes de datos operativos — **ciclos de fichaje** y **ejecución de tareas** — en patrones estadísticos (`BranchPattern`, `EmployeePattern`) y 22 indicadores analíticos que alimentan al intérprete IA Merlin.

El sistema distingue tres dimensiones independientes:

| Dimensión | Señal de entrada | Output |
|-----------|-----------------|--------|
| **Asistencia** | Ciclos checkin→checkout válidos | Timing, costes, fiabilidad, dispersión |
| **Calidad de ejecución** | Tareas validated/rejected + ratings | task signals, rejection rate, compliance |
| **Perfil archetype** | Combinación de ambas | `profileType` — acción RR.HH. recomendada |

---

## 2. Pipeline de datos

### 2.1 Ciclos de fichaje → BranchPattern / EmployeePattern

**Trigger:** `onChecklogWrite` en `entities/{entityId}/checklogs/{checklogId}`

Solo se procesa si el checkout tiene `status: valid` e `isSuspect: false`.

```
checkout válido
  → calculatePatternStats() [helper.ts]
    → Welford: costStd, costCV, costM2
    → EMA: avgStartHour, avgEndHour, weeklyWorkAvg[]
    → Welford per-day: stdStartByDay[], stdEndByDay[]
    → dataMaturity (logarítmica), dataQuality (EMA de cycleQuality)
    → scheduledHours (del WorkSchedule de la sucursal)
  → writeController.ts
    → consolida en checkbiz_branch_patterns/{branchId}
    → consolida en checkbiz_employee_patterns/{empId}_{branchId}_{entityId}
    → consolida en checkbiz_employee_patterns/{empId}_{entityId}
    → ProfileClassifier.classifyBranch/Employee() → persiste profileType
```

### 2.2 Tareas → task signals en patrones

**Trigger:** `onTaskPattern` en `entities/{entityId}/tasks/{taskId}`

Solo procesa transiciones hacia `validated` o `rejected`. No reprocesa si el estado anterior ya era terminal.

```
tarea validated/rejected
  → updateBranchTaskSignals() [transacción]
    → EMA(alpha=0.15): onTimeRate, rejectionRate, completionRate, criticalTaskOnTimeRate
    → ProfileClassifier.classifyBranch() → persiste profileType
  → updateEmployeeTaskSignals() [transacción en ambos patrones]
    → EMA(alpha=0.15): onTimeRate, startDelayAvg, validationRate, rejectionRate,
                       completionRate, priorityWeightedScore
    → ProfileClassifier.classifyEmployee() → persiste profileType
```

**priorityWeightedScore:**
```
weight = {critical:1.0, high:0.75, medium:0.50, low:0.25}
outcome = {on_time:1.0, late:0.5, rejected:0.0}
score = weight × outcome
```

### 2.3 Ratings de tareas → avgRating en patrones

**Trigger:** `onWriteTaskRating` en `entities/{entityId}/tasks/{taskId}/ratings/{employeeId}`

Tras actualizar `employee.ratingTask`, sincroniza `avgRating` normalizado `(stars-1)/4` a todos los `EmployeePattern` del empleado en esa entidad via EMA(alpha=0.15).

---

## 3. Modelo de datos — Patrón V2

### BranchPattern

```typescript
{
  // Identificación
  branchId: string;
  entityId: string;

  // Timing — EMA
  avgStartHour: number;          // hora decimal (8.5 = 08:30)
  avgEndHour: number;
  weeklyStartAvg: (number|null)[];  // [dom, lun, ... sab]
  weeklyEndAvg: (number|null)[];
  weeklyWorkAvg: (number|null)[];   // horas netas trabajadas por día

  // Dispersión horaria — Welford por día
  stdStartByDay: Array<{mean, m2, count, std} | null>;  // 7 posiciones
  stdEndByDay:   Array<{mean, m2, count, std} | null>;
  stdStartHour: number;  // media global de stds por día
  stdEndHour: number;

  // Adherencia de jornada (V2)
  avgScheduledHours?: number;  // EMA de horas planificadas del WorkSchedule

  // Fiabilidad descompuesta (V2)
  dataMaturity?: number;  // 0–1: madurez por volumen de ciclos (logarítmica)
  dataQuality?: number;   // 0–1: calidad de datos EMA (consistencia × GPS)
  reliability: number;    // 0–1: compuesto retrocompatible

  dataPoints: number;

  // Costes — Welford (V2)
  avgCycleCost: number;
  avgEffectiveCost: number;
  avgCostEfficiency: number;
  effectiveRealCost: number;
  totalCost: number;
  costM2?: number;    // acumulador Welford interno
  costStd?: number;   // σ del coste por ciclo
  costCV?: number;    // coeficiente de variación σ/μ (0.2 = 20% variación)
  costVariance?: number; // legacy — equivale a costCV

  avgCostHour: number;
  avgDistance?: number;

  // Task signals (V2 — F2)
  taskSignals?: TaskSignalsBranch;

  // Archetype (V2 — F3)
  profileType?: BranchProfileType;

  updatedAt: Date;
}
```

**TaskSignalsBranch:**
```typescript
{
  branchOnTimeRate: number;       // % tareas completadas en plazo (EMA)
  branchRejectionRate: number;    // % tareas rechazadas (EMA)
  branchCompletionRate: number;   // % tareas validadas / asignadas (EMA)
  branchAvgRating: number;        // media de ratings 0-1 (EMA)
  criticalTaskOnTimeRate: number; // % tareas críticas en plazo (EMA)
  taskCount: number;
  updatedAt: Date;
}
```

**BranchProfileType:** `"elite" | "understaffed" | "discipline-gap" | "multi-shift-stable" | "data-weak" | "seasonal-volatile" | "neutral"`

---

### EmployeePattern

Igual que BranchPattern más:

```typescript
{
  employeeId: string;
  // branchId puede ser null en el patrón global (employee_entity)

  // Experiencia laboral
  experienceByJob: Array<{nameJob, avgPrice, totalHours, firstWorked, lastWorked}>;
  experienceByResponsibility: Array<{responsibility, totalHours, years}>;
  totalExperienceYears: number;
  avgLevel: number;
  skillLevel: number;      // 0–1
  promotionScore: number;  // 0–1
  efficiencyIndex: number;

  // Task signals (V2 — F2)
  taskSignals?: TaskSignalsEmployee;

  // Archetype (V2 — F3)
  profileType?: EmployeeProfileType;
}
```

**TaskSignalsEmployee:**
```typescript
{
  avgRating: number;            // 0–1 normalizado: (stars-1)/4
  ratingCount: number;
  ratingTrend: "up" | "down" | "-";
  taskOnTimeRate: number;
  taskStartDelayAvg: number;    // minutos de retraso medio
  taskValidationRate: number;
  taskRejectionRate: number;
  taskCompletionRate: number;
  priorityWeightedScore: number; // 0–1
  taskCount: number;
  updatedAt: Date;
}
```

**EmployeeProfileType:** `"anchor" | "high-potential" | "specialist" | "maverick" | "at-risk" | "compliance-risk" | "ghost" | "neutral"`

---

## 4. Indicadores heurísticos (22 total)

Mínimo `dataPoints ≥ 20` para activar el análisis. En caso contrario, `analyzeHeuristic` devuelve `error: analyze/insufficient_data`.

### Indicadores de timing y turno

| ID | Nombre | Fórmula | Escala | Referencia |
|----|--------|---------|--------|-----------|
| **WTB** | Working Time Balance | `avgEndHour - avgStartHour` | horas | 7.5–9h = normal; < 6.5h = infrautilización |
| **OSD** | Operational Shift Deviation | `stdStartHour + stdEndHour` | horas | < 0.5h = disciplinado; > 1.0h = alta dispersión |

### Indicadores de fiabilidad y patrón

| ID | Fórmula | Escala | Referencia |
|----|---------|--------|-----------|
| **HCI** | `reliability × (1 - e^(-dataPoints/30))` | 0–1 | > 0.8 = patrón sólido |
| **PSS** | `(dataMaturity + dataQuality) / 2` | 0–1 | > 0.75 = patrón fiable |

### Indicadores de coste (usan costCV de Welford)

| ID | Fórmula | Escala | Referencia |
|----|---------|--------|-----------|
| **RCV** | `costCV` (= σ/μ del coste) | 0–∞ | < 0.2 = estable; > 0.5 = alta dispersión |
| **OSI** | `(1 - min(costCV, 1)) × reliability` | 0–1 | > 0.7 = operación estable |
| **CVH** | `min(costCV, 2) × (1 - reliability)` | 0–2 | < 0.3 = bajo riesgo |
| **CRI** | `min(costCV, 2) × avgCycleCost / 100` | > 0 | riesgo económico en unidades monetarias |
| **CPD** | `effectiveRealCost - avgCycleCost` | ± | desviación del coste real vs esperado |

### Indicadores de eficiencia operativa

| ID | Fórmula | Escala |
|----|---------|--------|
| **OER** | `avgEffectiveCost / avgCycleCost` | 0–∞ |
| **ECR** | `avgCostEfficiency / (avgCycleCost / 100)` | > 0 |
| **ERP** | `avgCostEfficiency × (1 - min(costCV, 1))` | 0–1 |
| **ROIh** | `avgCostEfficiency / workHours` | > 0 |
| **CEE** | `avgCostEfficiency - avgEffectiveCost/avgCycleCost` | ± |
| **WLB** | `workHours / avgScheduledHours` — `null` si sin WorkSchedule | 0–2 | 0.95–1.05 = óptimo; > 1.10 = horas extra |

### Índices globales

| ID | Fórmula | Escala |
|----|---------|--------|
| **SSR** | `(PSS + OER) / 2` | 0–∞ |
| **GHI** | `(ECR + OSI + HCI) / 3` | 0–1 aprox |
| **QHI** | Con taskSignals: `(TAC + TQI + (1-TRI)) / 3`; sin taskSignals: `(dataMaturity + dataQuality + OER) / 3` | 0–1 |

### Indicadores de tareas (F2 — requieren taskSignals)

| ID | Nombre | Fórmula | Referencia |
|----|--------|---------|-----------|
| **TAC** | Task Adherence Coefficient | `branchOnTimeRate × branchCompletionRate` | > 0.85 = alto rendimiento |
| **TQI** | Task Quality Index | `branchAvgRating × branchCompletionRate` | > 0.75 = excelente |
| **TRI** | Task Rejection Index | `branchRejectionRate` (bajo = mejor) | < 0.10 = sano; > 0.25 = sistémico |
| **PTC** | Priority Task Compliance | `criticalTaskOnTimeRate` | > 0.90 = comprometido |

Si `taskSignals` es null o `taskCount = 0`, los cuatro devuelven 0 (no aparecen como error).

---

## 5. Arquetipos de perfil (ProfileClassifier)

Clase estática pura en `application/heuristic/ProfileClassifier.ts`. Sin dependencias Firestore. Se llama en:
- `writeController.ts` (cada checkout)
- `onWriteTaskForPattern.ts` (cada tarea terminal)
- `HeuristicCore.analyzeBranch()` (cada llamada al endpoint)

### 5.1 Arquetipos de sucursal

Orden de evaluación (el primero que se cumple gana):

| # | Archetype | Condición | Acción operativa |
|---|-----------|-----------|-----------------|
| 1 | `data-weak` | `dataMaturity < 0.4` O `dataQuality < 0.35` | No analizar operaciones. Mejorar calidad de fichaje |
| 2 | `multi-shift-stable` | OSD > 1.0h global PERO ≥ 2 días con std por día < 0.4h | Normal — no señalar OSD como problema |
| 3 | `elite` | OSD < 0.5h AND TAC > 0.85 AND reliability > 0.85 AND ≥ 5 tareas | Replicar modelo |
| 4 | `discipline-gap` | reliability > 0.75 AND rejectionRate > 0.2 AND ≥ 5 tareas | Auditar calidad de ejecución |
| 5 | `understaffed` | WTB < 7h AND onTimeRate < 0.6 AND ≥ 5 tareas | Revisar headcount / asignación |
| 6 | `seasonal-volatile` | `max(weeklyWorkAvg) - min(weeklyWorkAvg) > 2h` | Planificación por día de semana |
| 7 | `neutral` | resto | Análisis estándar |

### 5.2 Arquetipos de empleado

| # | Archetype | Condición | Acción RR.HH. |
|---|-----------|-----------|--------------|
| 1 | `ghost` | dataPoints < 20 O reliability < 0.3 | Verificar si el empleado está activo y fichando |
| 2 | `at-risk` | taskCount ≥ 5 AND (onTimeRate < 0.6 O avgRating < 0.375) | Reunión 1:1 inmediata, plan de mejora |
| 3 | `compliance-risk` | reliability ≥ 0.7 AND rejectionRate > 0.25 AND ≥ 5 tareas | Auditar calidad de trabajo |
| 4 | `anchor` | reliability ≥ 0.8 AND onTimeRate ≥ 0.85 AND avgRating ≥ 0.75 AND ≥ 5 tareas | Candidato a promoción / referente |
| 5 | `high-potential` | experienceYears < 1 AND avgRating ≥ 0.75 AND onTimeRate ≥ 0.80 AND ≥ 3 tareas | Acelerar carrera |
| 6 | `specialist` | 1-2 tipos de trabajo AND avgRating ≥ 0.75 AND ≥ 5 tareas | No rotar. Asignar a su especialidad |
| 7 | `maverick` | OSD > 0.8h AND avgRating ≥ 0.75 AND ≥ 5 tareas | Horario flexible |
| 8 | `neutral` | resto | Seguimiento estándar |

**Nota de escala:** `avgRating` está normalizado 0–1. `0.75 = 4.0★`, `0.375 = 2.5★`.

---

## 6. Endpoint de análisis

**HTTP:** `POST .../analyzeHeuristic`

**Parámetros:** `entityId`, `branchId` (o `employeeId`), `lang: "es"|"en"`

**Respuesta:**
```json
{
  "branchId": "br_001",
  "reliability": 0.87,
  "dataPoints": 196,
  "dataMaturity": 0.91,
  "dataQuality": 0.74,
  "profileType": "neutral",
  "results": [
    { "id": "OSI", "value": 0.72, "severity": "success", "label": "..." },
    { "id": "WLB", "value": null },
    ...
  ]
}
```

`WLB` aparece como `null` cuando la sucursal no tiene `WorkSchedule` configurado.

El endpoint activa heurísticos de sucursal o empleado según el nivel del patrón pasado. Para empleados usa el motor de reglas en Firestore (`checkbiz_heuristic_indicators_employee`).

---

## 7. Integración con Merlin (F5)

`branchInterpret.builder.ts` construye el prompt que recibe el modelo. Cambios clave de V2:

1. **Bloque de valores reales del patrón** — el AI recibe los números, no solo labels:
   - Horarios en HH:MM, dispersión en minutos, horas por día de la semana
   - `costCV` como porcentaje, `avgScheduledHours`, `avgDistance` en metros
   - `taskSignals`: tasa de cumplimiento, rechazo, rating en ★

2. **Pre-filtrado por severidad** — máx 5 errores + 3 warnings + 2 successes. El AI no recibe 22 señales con igual peso.

3. **Tabla de umbrales en el system prompt:**
   ```
   OSD: < 0.5h=disciplinado | 0.5-1.0h=moderado | > 1.0h=severo
   WTB: 7.5-9.0h=normal | < 6.5h=infrautilización | > 9.5h=horas extra
   dataQuality: > 75%=fiable | 50-75%=parcial | < 50%=validar antes de actuar
   costCV: < 20%=estable | 20-50%=normal | > 50%=alta volatilidad
   taskOnTimeRate: > 85%=alto | 70-85%=aceptable | < 70%=problema
   rating 0-1: > 0.75=excelente(4★+) | < 0.375=crítico(< 2.5★)
   ```

4. **Guía de tono por profileType:**

   | profileType | Instrucción al AI |
   |-------------|------------------|
   | `data-weak` | Solo hablar de mejorar calidad de datos. No diagnosticar operaciones |
   | `multi-shift-stable` | OSD alto es estructural. No señalar dispersión de inicio |
   | `elite` | Consolidar. ¿Qué replicar? |
   | `discipline-gap` | Directo. Root cause del rechazo de tareas |
   | `understaffed` | Headcount / reasignación de turnos |
   | `seasonal-volatile` | Scheduling semanal |
   | `neutral` | Análisis balanceado estándar |

---

## 8. Colecciones Firestore

| Colección | Descripción |
|-----------|-------------|
| `checkbiz_branch_patterns` | Un documento por `branchId` por entidad |
| `checkbiz_employee_patterns` | Dos docs por empleado: `{empId}_{branchId}_{entityId}` y `{empId}_{entityId}` |
| `checkbiz_heuristic_indicators` | Umbrales y metadata de indicadores de sucursal |
| `checkbiz_heuristic_indicators_employee` | Reglas del motor de empleados |

**Índice requerido** en `checkbiz_employee_patterns`: `employeeId ASC` + `entityId ASC` (necesario para `syncRatingToPatterns`).

---

## 9. Constantes clave

| Constante | Valor | Dónde |
|-----------|-------|-------|
| `EMA_ALPHA` | 0.10 | helper.ts — checklog patterns |
| `TASK_EMA_ALPHA` | 0.15 | onWriteTaskForPattern.ts |
| `TASK_RATING_EMA_ALPHA` | 0.15 | onWriteTaskRating.ts |
| `MATURITY_BASE` | 0.20 | helper.ts — piso de dataMaturity |
| `MATURITY_TARGET` | 100 | helper.ts — dataPoints para saturación |
| `MIN_DATA_POINTS` | 20 | HeuristicCore.ts — mínimo para análisis |

---

## 10. Umbrales de Firestore a revisar (pendiente)

Con los cambios de F1, las escalas de estos indicadores cambiaron respecto a V1:

| Indicador | Escala V1 | Escala V2 | Acción |
|-----------|----------|-----------|--------|
| **RCV** | rota | CV real 0–∞ (< 0.2 = estable) | Actualizar thresholds en Firestore |
| **WLB** | sin sentido | ratio 0–2 (1.0 = perfecto) | Actualizar: success 0.9–1.1, warning fuera de 0.8–1.2 |
| **OSI** | basado en costVar rota | 0–1 con costCV correcto | Revisar si threshold < 0.5 sigue siendo apropiado |
| **CVH** | inestable | 0–2 más estable | Revisar |

---

## 11. Limitaciones conocidas

- **`avgCostEfficiency`** (y por tanto ECR, ERP, ROIh, CEE) mide calidad de datos del ciclo, no eficiencia operativa real. La eficiencia real requiere datos de output de tareas que ahora están disponibles via `taskSignals`; la migración de esos indicadores es trabajo futuro.
- **CPD** converge a ~0 con suficientes datos por ser auto-referencial. Benchmark cross-branch es trabajo futuro.
- **F4 (OSD por grupo de turno)** — deprioritizado; mitigado por el archetype `multi-shift-stable` en F3.

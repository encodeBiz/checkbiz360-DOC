# Heurística V2 — Roadmap de Rediseño

> Branch: `qa/heuristic-v2-task-integration`
> Fecha inicio: 2026-06-05
> **Estado: IMPLEMENTADO — F1, F2, F3, F5 completos. F4 deprioritizado.**
> Referencia del estado actual: [heuristica.md](./heuristica.md)
> Implementación detallada: [heuristica-changelog.md](./heuristica-changelog.md)

---

## 0. Diagnóstico del sistema actual (V3 → base para V2 API)

El motor heurístico actual tiene **errores matemáticos confirmados** y **deficiencias de diseño** que limitan el valor real del análisis. Este documento recoge el diagnóstico completo y el plan de corrección.

### Errores críticos (matemáticos)

#### E1 — QHI = GHI algebraicamente (indicadores idénticos)
```
GHI = (ECR + OSI + HCI) / 3
QHI = (GHI + ECR + OSI + HCI) / 4
    = ((ECR+OSI+HCI)/3 + ECR+OSI+HCI) / 4
    = (ECR+OSI+HCI) · (4/3) / 4
    = (ECR+OSI+HCI) / 3
    = GHI
```
**Impacto:** QHI y GHI son el mismo número. Cuando el AI recibe ambos en "error", los cuenta como dos señales distintas cuando es una sola.

#### E2 — `costVariance` no es varianza estadística
En `helper.ts`:
```typescript
const costVariance = Math.abs(costCycle - (pattern.avgCycleCost ?? costCycle));
```
Esto es una **desviación absoluta**, no una varianza (σ²). Luego en `HeuristicNormalizer`:
```typescript
const costVarNormalized = 1 - (1 / (1 + rawVar)); // rawVar es abs. deviation, no varianza
```
Y en `HeuristicCalculator`:
```typescript
const relativeCostVar = this.safeDiv(costVarianceAbs, avgCycleCost, 0);
// costVarianceAbs ya está normalizado 0..1 por el Normalizer
// dividir [0..1] / avgCycleCost (ej: 150€) = 0.006... sin dimensión operativa
```
**Impacto:** OSI, CVH, CRI, WLB, PSS, SSR, GHI usan este número roto. Sus valores no son interpretables.

#### E3 — WLB no mide carga de trabajo
```typescript
WLB = (workHours * avgCostEfficiency) / (1 + boundedCostVar)
```
Esto es eficiencia ponderada ajustada por varianza. El label "Underload / Overload" es ficticio porque la fórmula no compara horas reales vs horas planificadas. Un empleado con turno de 8h perfecto puede aparecer como "Underload".

#### E4 — `avgCostEfficiency` es `consistencyScore × reliability`, no eficiencia real
```typescript
costEfficiency = consistencyScore * newReliability  // = min(1, events/4) × reliability
```
No mide eficiencia operativa. Es un proxy de calidad de datos multiplicado por fiabilidad. Todos los indicadores que lo usan (ECR, ERP, ROIh, CEE, WLB) heredan este defecto conceptual.

### Deficiencias de diseño

#### D1 — 6 de 18 indicadores son variaciones de lo mismo
OSI, PSS, SSR, GHI, QHI dependen casi exclusivamente de `reliability` y `boundedCostVar`. Cuando ambos son bajos (reliability < 0.6) los seis disparan simultáneamente, inundando el AI con 6 señales que dicen "inestabilidad" desde el mismo dato.

#### D2 — OSD dispara falsos positivos en operaciones multi-turno
```typescript
OSD = stdStartHour + stdEndHour  // std GLOBAL sobre todos los turnos
```
Una empresa con turno 07:00-15:00 y turno 14:00-22:00 tiene `stdStartHour` alto por estructura, no por desorden. OSD debería calcularse **por grupo de turno**, no globalmente.

#### D3 — `reliability` hace trabajo doble
Mezcla madurez del patrón (cuántos dataPoints) con calidad de datos (consistency). Una sucursal nueva con fichajes perfectos tendrá baja reliability aunque sus datos sean excelentes. No se puede distinguir ambos casos.

#### D4 — Sin benchmarking cross-branch
Todos los indicadores son auto-referenciales (la sucursal se mide contra sí misma). No hay comparación entre sucursales de la misma entidad. CPD compara medias del mismo dataset, no contra una referencia externa.

#### D5 — Sin integración de datos de tareas
El dominio `Task` tiene señales riquísimas que no se incorporan al patrón:
- `TaskRating` (1-5 estrellas por supervisor) → ya existe en `employee.ratingTask` pero no en `EmployeePattern`
- `timeComplianceStatus`: on_time, completed_late, overdue
- `priority`: critical, high, medium, low
- `status`: validated vs rejected
- Tiempos scheduledStartAt → startedAt → completedAt

---

## 1. Arquitectura de datos disponibles

### BranchPattern (actual)
```
Timing:    avgStartHour, avgEndHour, stdStartHour, stdEndHour
           weeklyStartAvg[7], weeklyEndAvg[7], weeklyWorkAvg[7]
           stdStartByDay[7]{mean, m2, count, std}, stdEndByDay[7]
Cost:      avgCostHour, avgCycleCost, avgEffectiveCost, avgCostEfficiency
           effectiveRealCost, totalCost, costVariance, costTrend
Quality:   reliability, dataPoints, avgDistance, failedCount
```

### EmployeePattern (actual) — igual + experiencia
```
+ experienceByJob[]: {nameJob, avgPrice, totalHours, firstWorked, lastWorked}
+ experienceByResponsibility[]: {responsibility, totalHours, years}
+ totalExperienceYears, avgLevel, efficiencyIndex
+ skillLevel (0-1), promotionScore (0-1)
+ endCount, netWorkedHours
```

### Task domain (disponible, NO integrado)
```
Por tarea:
  status: draft|assigned|in_progress|completed|validated|rejected|cancelled
  timeComplianceStatus: not_started|on_time|at_risk|overdue|completed_on_time|completed_late
  priority: low|medium|high|critical
  scheduledStartAt, startedAt, completedAt, dueAt, validatedAt, rejectedAt

Por asignación (TaskAssignment):
  employeeId, status: assigned|accepted|working|completed|blocked|removed
  startedAt, completedAt

Por rating (TaskRating):
  employeeId, rating: 1-5, ratedBy, ratedByRole: supervisor|manager|owner

Ya agregado en employee.ratingTask:
  {average, count, sum, stars: {1:n, 2:n, 3:n, 4:n, 5:n}}
```

---

## 2. Plan de correcciones matemáticas (Fase 1)

### F1.1 — Corregir `costVariance` con algoritmo de Welford (ya aplicado a std horaria)

**Actual:** `costVariance = |costCycle - avgCycleCost|` (desviación absoluta, un solo punto)

**Correcto:** Usar Welford incremental igual que para `stdStartHour`:
```typescript
// En helper.ts — añadir al patrón:
// costM2: number (acumulador Welford)
// costCount: number (= dataPoints)

const costStats = updateStd(costCycle, pattern.avgCycleCost, pattern.costM2 ?? 0, pattern.dataPoints ?? 0);
// costStats.std es la desviación estándar real del coste por ciclo
// Coeficiente de variación (CV): costStats.std / costStats.mean
```

**Impacto:** OSI, CVH, CRI usan `boundedCostVar = relativeCostVar` que ahora será `σ_cost / avgCycleCost` — el coeficiente de variación real. Interpretable: CV < 0.2 = costes estables, CV > 0.5 = alta dispersión de costes.

### F1.2 — Eliminar HeuristicNormalizer (es el origen de la cadena de errores)

El `HeuristicNormalizer` transforma `costVariance` a 0..1 antes de que los cálculos la usen. Con Welford tendremos el CV directamente en escala operativa (0..∞, bounded a 2). El normalizer ya no es necesario y causa confusión.

### F1.3 — Separar `reliability` en `dataMaturity` + `dataQuality`

```typescript
// dataMaturity: crecimiento logarítmico por volumen de ciclos
dataMaturity = BASE + (1 - BASE) * min(1, log1p(dataPoints) / log1p(TARGET))

// dataQuality: EMA de consistencyScore * distanceFactor (calidad de cada ciclo)
dataQuality = EMA(prevDataQuality, consistencyScore * distanceFactor)

// reliability mantiene su significado compuesto pero ya se puede desagregar
reliability = dataMaturity * dataQuality
```

Esto permite al AI decir: "La sucursal tiene 196 ciclos (madurez alta) pero calidad de fichaje baja (0.49) → problema de consistencia en los registros, no de volumen".

### F1.4 — Redefinir WLB como adherencia de jornada real

```typescript
// WLB = horas reales trabajadas / horas planificadas (del WorkSchedule)
// Si no hay WorkSchedule configurado → WLB = null (no aplica)
// 0.95-1.05 = óptimo; < 0.85 = infrautilización; > 1.10 = horas extra sistemáticas
WLB = netWorkedHours / scheduledHours  // donde scheduledHours viene de Branch.advance.workSchedule
```

### F1.5 — Eliminar QHI o redefinirlo con información diferente

Opción A (eliminar): Quitar QHI del set de indicadores. 17 → 16.
Opción B (redefinir): `QHI = task quality contribution` (ver Fase 2).
**Decisión:** Opción B — QHI pasa a ser el índice de calidad de tareas.

---

## 3. Nuevos campos en los patrones (Fase 2 — Task Integration)

### 3.1 Extensión de EmployeePattern

```typescript
// Añadir al interface EmployeePattern:
taskSignals?: {
  // Ratings
  avgRating: number;           // EMA de ratings recibidos (0-5 normalizado a 0-1)
  ratingCount: number;         // total ratings recibidos
  ratingTrend: "up" | "down" | "-"; // tendencia últimas 10 valoraciones

  // Cumplimiento temporal
  taskOnTimeRate: number;      // completadas_en_plazo / total_completadas (EMA)
  taskStartDelayAvg: number;   // avg minutos de retraso en inicio vs scheduledStartAt (EMA)

  // Calidad
  taskValidationRate: number;  // validated / (validated + rejected) (EMA)
  taskRejectionRate: number;   // rejected / assigned (EMA)

  // Engagement
  taskCompletionRate: number;  // completed+validated / assigned (EMA)
  avgTasksPerMonth: number;    // media de tareas asignadas por mes (EMA)

  // Por prioridad (pesos: critical=4, high=3, medium=2, low=1)
  priorityWeightedScore: number; // score ponderado por prioridad (0-1)

  updatedAt: Date;
}
```

### 3.2 Extensión de BranchPattern

```typescript
// Añadir al interface BranchPattern:
taskSignals?: {
  branchAvgRating: number;       // media de ratings de todos los empleados (EMA)
  branchOnTimeRate: number;      // % tareas completadas en plazo (EMA)
  branchRejectionRate: number;   // % tareas rechazadas (EMA)
  branchCompletionRate: number;  // % tareas validadas / asignadas (EMA)
  criticalTaskOnTimeRate: number; // % tareas críticas completadas en plazo (EMA)
  avgOpenTasks: number;          // media de tareas abiertas simultáneamente (EMA)
  updatedAt: Date;
}
```

### 3.3 Trigger para actualizar patterns desde tareas

Crear `onWriteTaskForPattern` (Firestore trigger en `entities/{entityId}/tasks/{taskId}`):
- Se activa en: status → validated, rejected; cuando se añade TaskRating
- Actualiza `taskSignals` del EmployeePattern y BranchPattern afectados
- Usa EMA con `TASK_ALPHA = 0.15` (convergencia más lenta que checklog, menos frecuencia)

---

## 4. Nuevos indicadores heurísticos V2 (Fase 2)

### Indicadores de tarea para Branch

| ID | Nombre | Fórmula | Escala | Interpreta |
|----|--------|---------|--------|-----------|
| **TAC** | Task Adherence Coefficient | `taskOnTimeRate * completionRate` | 0–1 | % tareas entregadas bien y a tiempo |
| **TQI** | Task Quality Index | `avgRating/5 * validationRate` | 0–1 | Calidad percibida por supervisores |
| **TRI** | Task Rejection Index | `1 - validationRate` | 0–1 (bajo=bueno) | Tasa de rechazo normalizada |
| **PTC** | Priority Task Compliance | `criticalOnTimeRate` | 0–1 | Cumplimiento en tareas críticas |

**QHI redefinido:** `QHI = (TAC + TQI + (1-TRI)) / 3` — Índice de calidad real basado en tareas.

### Indicadores de tarea para Employee (motor de reglas en Firestore)

| ID | Nombre | Condición | Severidad |
|----|--------|-----------|-----------|
| **TRSC** | Task Rating Score | `avgRating < 3.0` | error; `3.0–3.9` = warning |
| **TDLC** | Task Deadline Compliance | `taskOnTimeRate < 0.7` | error; `0.7–0.85` = warning |
| **TVAL** | Task Validation Rate | `validationRate < 0.8` | warning |
| **TPRI** | Task Priority Response | `priorityWeightedScore < 0.6` | warning |

---

## 5. Perfiles (Archetypes) — Empleado y Sucursal

### 5.1 Arquetipos de Empleado

Los perfiles se calculan combinando señales de attendance + task. Se almacenan en `EmployeePattern.profileType`.

| Perfil | ID | Condición de clasificación | Acción RR.HH. |
|--------|----|---------------------------|---------------|
| **Ancla** | `anchor` | reliability ≥ 0.8 AND taskOnTimeRate ≥ 0.85 AND avgRating ≥ 4.0 | Candidato a promoción / referente de equipo |
| **Alto Potencial** | `high-potential` | experienceYears < 1 AND avgRating ≥ 4.0 AND taskOnTimeRate ≥ 0.80 | Mentoring, asignaciones de mayor responsabilidad |
| **Especialista** | `specialist` | avgRating ≥ 4.0 en ≤2 tipos de trabajo AND global avgRating < 3.5 | Asignar a su especialidad; no rotar |
| **Disruptor** | `maverick` | stdStartHour > 0.8 AND avgRating ≥ 4.0 | Horario flexible, no turno fijo |
| **En Riesgo** | `at-risk` | (taskOnTimeRate < 0.6 OR avgRating < 2.5) AND dataPoints > 30 | Entrevista 1:1 inmediata; plan de mejora |
| **Riesgo Compliance** | `compliance-risk` | taskRejectionRate > 0.25 AND reliability ≥ 0.7 | Auditar calidad de trabajo, posible retraining |
| **Fantasma** | `ghost` | dataPoints < 20 OR reliability < 0.3 | Validar si el empleado está activo y fichando |
| **Neutro** | `neutral` | No encaja en ningún perfil anterior | Seguimiento estándar |

### 5.2 Arquetipos de Sucursal

Se almacenan en `BranchPattern.profileType`.

| Perfil | ID | Señales clave | Implicación operativa |
|--------|----|--------------|----------------------|
| **Sucursal Élite** | `elite` | OSD < 0.5, TAC > 0.85, reliability > 0.85 | Referente de operaciones, modelo a replicar |
| **Infradotada** | `understaffed` | avgOpenTasks alto, taskOnTimeRate < 0.6, WTB < 7h | Evaluar headcount; revisión de asignación |
| **Brecha de Disciplina** | `discipline-gap` | reliability > 0.75 PERO taskRejectionRate > 0.2 | Problema de calidad de ejecución, no de presencia |
| **Multi-turno Estable** | `multi-shift-stable` | OSD > 1.0 PERO stdStartByDay[día].std < 0.4 por día | Normal, no confundir con desorden — ver por día |
| **Datos Débiles** | `data-weak` | dataMaturity < 0.4 OR dataQuality < 0.35 | No analizar hasta mejorar calidad de fichaje |
| **Volátil Estacional** | `seasonal-volatile` | Alta varianza en weeklyWorkAvg entre días, baja entre semanas | Revisar planificación de turnos por día de semana |

---

## 6. Revisión del indicador OSD (multi-turno)

El OSD actual usa `std` global. Para entidades multi-turno debe calcularse por grupo de turno.

**Nuevo OSD:**
```typescript
// Si Branch.advance.workSchedule está definido:
//   Asignar cada ciclo a su turno más cercano
//   Calcular std dentro de cada turno
//   OSD = media ponderada de std por turno (no std global)
// Si no hay workSchedule:
//   OSD = std global (comportamiento actual, con warning en el AI)
```

**Nuevo indicador STD_WEEK:** `max(weeklyWorkAvg) - min(weeklyWorkAvg)` donde ambos son non-null → detecta días de la semana con trabajo muy diferente al patrón (ej: lunes son 2h menos).

---

## 7. Reducción del set de indicadores (de 18 a 14 core + 4 task)

### Indicadores a mantener (14 core)
WTB, OSD, HCI*, OSI*, RCV*, CVH*, CPD*, CRI*, OER, ECR, ERP*, ROIh, CEE, SSR*

`*` = requieren corrección matemática de Fase 1.

### Indicadores a redefinir
- **WLB** → Adherencia de jornada real (horas reales / planificadas)
- **PSS** → `PSS = (dataMaturity + dataQuality) / 2` — ahora sí mide estabilidad del patrón
- **QHI** → Índice de calidad de tareas `(TAC + TQI + (1-TRI)) / 3`

### Indicadores nuevos de tarea (4)
TAC, TQI, TRI, PTC (para branches)

**Total: 18 indicadores con información real, sin redundancia.**

---

## 8. Mejoras al intérprete Merlin (Fase 3 — post correcciones)

Una vez corregida la capa heurística, el intérprete recibirá:

### Cambios en `branchInterpret.builder.ts`

1. **Pasar BranchPattern raw** (valores numéricos con contexto):
   ```
   avgStartHour=8.5, stdStartHour=1.48 → 68% de fichajes entre 7:00 y 10:00
   workHours=8.35 → jornada media de 8h 21min
   dataMaturity=0.9, dataQuality=0.49 → patrón maduro pero calidad de fichaje baja
   ```

2. **Pre-filtrar señales por severidad** (no enviar los 18):
   - Máximo 5 señales `error` + 3 `warning` + perfil de sucursal
   - Si todo es `success`: enviar solo GHI + WTB + profileType

3. **Añadir tabla de referencia al prompt**:
   ```
   OSD < 0.5h = disciplinado | 0.5-1.0h = moderado | > 1.0h = dispersión severa
   WTB 7.5-9h = jornada normal | < 6h = infrautilización | > 9.5h = sobretiempo
   dataQuality > 0.75 = datos fiables | 0.5-0.75 = parcialmente fiables | < 0.5 = validar
   taskOnTimeRate > 0.85 = cumplimiento alto | < 0.7 = problema de planificación
   avgRating > 4.0 = equipo de alto rendimiento | < 3.0 = problema grave
   ```

4. **Cambiar el approach de "describe" a "diagnostica"**:
   - Actual: "Hay dispersión horaria → revisar turnos"
   - Objetivo: "Con `stdStartHour=1.48h` y `dataQuality=0.49`, el 50% de los ciclos tienen calidad insuficiente. El patrón no ha convergido en calidad. Antes de rediseñar turnos, audita los puntos de fichaje y elimina los ciclos con distancia > 150m."

5. **Incluir profileType en el contexto** para personalizar el tono:
   - `data-weak` → lenguaje cauteloso, enfocado en mejorar datos
   - `elite` → lenguaje de consolidación, buscar qué replicar
   - `at-risk` → lenguaje directo, acciones inmediatas

---

## 9. Fases de implementación

| Fase | Scope | Archivos principales | Complejidad |
|------|-------|---------------------|-------------|
| **F1** | Correcciones matemáticas | `helper.ts`, `HeuristicCalculator.ts`, `HeuristicNormalizer` (eliminar) | Media |
| **F2a** | Separar reliability | `helpers.ts`, `writeController.ts`, `Branch.ts`, `Employee.ts` | Baja |
| **F2b** | WLB redefinido | `HeuristicCalculator.ts`, thresholds Firestore | Baja |
| **F2c** | OSD multi-turno | `HeuristicCalculator.ts`, `Branch.ts` | Media |
| **F3a** | Task signals en patterns | `Task.ts` interfaces, `writeController.ts` nuevo trigger | Media-Alta |
| **F3b** | Nuevos indicadores TAC/TQI/TRI/PTC | `HeuristicCalculator.ts`, nuevos docs Firestore | Media |
| **F4** | Perfiles archetype | `HeuristicCore.ts`, `Branch.ts`, `Employee.ts` | Media |
| **F5** | Merlin prompt upgrade | `branchInterpret.builder.ts`, `interpretBranches.ts` | Baja |

**Orden recomendado:** F1 → F2a → F2b → F3a → F3b → F4 → F2c → F5

**No iniciar F5 hasta que F1 esté completo** — mejorar el prompt con datos rotos tiene techo bajo.

---

## 10. Referencias de código

| Archivo | Relevancia |
|---------|-----------|
| `api-express/src/checkinbiz/application/heuristic/HeuristicCalculator.ts` | Fórmulas de indicadores — errores E1, E2, E3 |
| `api-express/src/checkinbiz/application/heuristic/HeuristicCore.ts` | Orquestación + HeuristicNormalizer (eliminar) |
| `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/helper.ts` | Welford std + costVariance (corregir E2) + reliability (separar) |
| `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/writeController.ts` | Consolidación de patrones + nuevo trigger de tareas |
| `functions/src/services-saas/checkinbiz/domain/entities/Task.ts` | Modelo completo de tareas |
| `functions/src/services-saas/checkinbiz/firebase-firestore-trigger/onWriteTaskRating.ts` | Trigger existente de ratings → extender a pattern |
| `api-express/src/customGPT/infraestructure/promptBuilders/branchInterpret.builder.ts` | Prompt Merlin para branch — mejoras Fase F5 |
| `api-express/src/checkinbiz/domain/entities/Branch.ts` — `BranchPattern` | Extender con `taskSignals`, `dataMaturity`, `dataQuality`, `profileType` |
| `api-express/src/checkinbiz/domain/entities/Employee.ts` — `EmployeePattern` | Extender con `taskSignals`, `dataMaturity`, `dataQuality`, `profileType` |

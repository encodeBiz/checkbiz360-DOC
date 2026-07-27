# 01 — Estado Actual (As-Is)

## 1. Entidades de dominio relevantes

### CheckLog
`Firestore: entities/{entityId}/checklogs/{checklogId}`

```
employeeId, entityId, branchId
timestamp          → timestamp operacional (ajustado si hubo corrección)
metadata.realDateMarket → marca horaria real del dispositivo del empleado
type: "checkin" | "checkout" | "restin" | "restout"
status: "valid" | "failed" | "pending-employee-validation" | "incomplete_workday"
isSuspect: boolean
geo: { lat, lng }
metadata.scheduleApplied → horario configurado en el momento del evento
metadata.etz → timezone del empleado en ese momento
checkin: string  → ID del checkin al que pertenece este checkout (vincula el ciclo)
```

Los checklogs se agrupan en **ciclos** por el campo `checkin`. Un ciclo válido requiere al menos un par checkin+checkout con `status === "valid"`.

### DailyReport
`Firestore: checkbiz_daily_report/{entityId}_{branchId}_{yyyyMMdd}`

Generado por el scheduler `dailyCollectorData` (cron cada hora; ejecuta para sucursales cuya hora local es 02:00).

Contiene:
- Métricas de branch: workedHours, totalCost, suspectRate, punctualidad (onTime/late)
- Array `employees[]` con breakdown por empleado: workedHours, jobName, price, totalCost, punctualidad individual

**Lo que NO contiene:** task ratings, histórico de patrones, datos de tarea completada.

### BranchPattern / EmployeePattern
`Firestore: branches/{branchId}` (campo embebido `pattern`)  
`Firestore: entities/{entityId}/employees/{employeeId}` (campo embebido `pattern`)

Estadísticas acumuladas: avgStartHour, stdStartHour, reliability, dataPoints, avgCostEfficiency, costVariance, weeklyStartAvg[], etc.

El patrón es **mutable y sin versión**. Cada actualización sobreescribe el anterior. No existe registro de evolución.

### Task / TaskRating
`Firestore: entities/{entityId}/tasks/{taskId}`

Las tareas tienen workers asignados. Una vez completada y validada, se puede valorar con `RateTaskWorker`. La valoración queda en el documento de la tarea (`workers[i].rating`).

**Actualmente no existe ningún vínculo entre task ratings y daily reports ni patrones.**

---

## 2. Flujos actuales

### Flujo de checkin (tiempo real)
```
App → POST /create-checklog
  → createChecklogController
    → CreateChecklog use case
      → FirestoreChecklogRepository.save()
      → onWhriteChecklog trigger (Firestore trigger)
        → actualiza BranchPattern con el nuevo ciclo
```

### Flujo de reporte diario
```
[Cron cada hora]
  → dailyCollectorDataController
    → para cada Branch activa:
        if (localHour === 2):
          → checklogRepository.findInterbalCheckLog(ayer, branch)
          → buildDailyReportFromChecklogs({ branch, checklogs, targetDate })
          → reportRepository.upsertDailyReport(dailyReport)
             → escribe en checkbiz_daily_report/{entityId}_{branchId}_{yyyyMMdd}
```

### Flujo de análisis IA (heurística)
```
Frontend → POST /analyzeHeuristic { entityId, branchId, lang }
  → validateToken
  → analyzePattern(entityId, branchId, lang)
    → patternsRepo.findPatternByBranch(branchId)  // snapshot actual
    → new HeuristicCore(repository, lang)
    → core.analyzeBranch(pattern, "branch")
      → HeuristicNormalizer.normalize(pattern)
      → HeuristicCalculator.computeBranch(indicatorId)  // por cada indicador: WTB, OSD, HCI, OSI, PSS, RCV, CVH, CPD, CRI...
      → HeuristicEvaluator.evaluate(id, value)
        → compara con thresholds de Firestore
    → retorna { branchId, reliability, dataPoints, results[] }
```

---

## 3. Limitaciones identificadas

| # | Limitación | Impacto |
|---|------------|---------|
| L1 | Reportes on-demand sobre Firestore | Costo de lecturas crece linealmente con volumen de datos. Con alto volumen → latencia alta, costo alto |
| L2 | No hay Data Warehouse | Imposible hacer queries SQL analíticos (percentiles, joins, agrupaciones complejas) |
| L3 | Task ratings ausentes en reportes | La valoración del trabajo de un empleado no aparece en su reporte diario. Pérdida de señal para IA |
| L4 | Patrones sin historia | No se puede ver si un empleado/branch mejoró o empeoró. Los patrones se disuelven con el tiempo |
| L5 | IA solo ve el presente | El motor heurístico analiza un snapshot plano. No tiene contexto de tendencia ("esto viene mejorando 3 semanas") |
| L6 | No hay deduplicación de patrones por fecha | Si el sistema se cae y vuelve, puede recalcular y sobreescribir patrones de días anteriores sin trazabilidad |

---

## 4. Volumen esperado

Estimaciones conservadoras para planificar el schema:

| Entidad | Volumen mensual por empresa | Acumulado a 12 meses (100 empresas) |
|---------|----------------------------|-------------------------------------|
| Checklogs | ~4 checkins/día × 50 empleados = ~6,000/mes | ~7.2M filas |
| DailyReports | ~30 docs/branch × 3 branches = ~90/mes | ~108K docs |
| TaskRatings | ~200/mes | ~240K |
| PatternSnapshots | ~30 snapshots/branch | ~108K |

PostgreSQL en un servidor privado maneja este volumen sin estrés. El problema actual es que Firestore cobra por lectura individual, no por query.

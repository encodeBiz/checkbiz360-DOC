# TDR-003 — Construcción del Daily Report enriquecido en el servidor privado

**Fecha:** 2026-06-02  
**Estado:** Diseño aprobado, pendiente implementación (Fase 2)  
**Componente:** Servidor privado — `POST /api/build/daily-report`

---

## Problema

`buildDailyReportFromChecklogs` en Firebase lee checklogs de Firestore y construye el `DailyReport`. Este proceso:

1. Es costoso en lecturas de Firestore a escala
2. No tiene acceso a task ratings (están en otra subcolección)
3. No guarda historia de patrones

El servidor privado debe replicar esta lógica leyendo de PostgreSQL y enriquecerla con task ratings.

---

## Análisis del algoritmo existente en `buildDailyReportFromChecklogs`

El algoritmo actual opera así:

```
1. Determinar horario de la branch para el día (workSchedule o defaults)
2. Agrupar checklogs por employeeId
3. Para cada empleado:
   a. Ordenar logs por timestamp ASC
   b. Identificar ciclos válidos (checkin + checkout con mismo .checkin ref)
   c. Para cada ciclo:
      - Calcular grossHours = checkout - checkin
      - Calcular breaks (restin → restout pairs)
      - Calcular netHours = grossHours - breaks (o grossHours - fixedBreak)
      - Acumular puntualidad IN: ¿checkin <= startDecimal?
      - Acumular puntualidad OUT: ¿checkout <= endDecimal?
   d. Agregar DailyEmployeeReport
4. Calcular métricas globales del branch
```

**Punto crítico de la lógica de ciclos:**  
Un ciclo se identifica por el campo `checkin_ref` (que en Firestore se llama `checkin`). El checkout tiene `checkin === checkinId`. En PostgreSQL esto es la columna `checkin_ref`.

```sql
-- Todos los logs de un ciclo válido:
SELECT * FROM checklogs_raw
WHERE entity_id = $1
  AND branch_id = $2
  AND DATE(real_date_market AT TIME ZONE $tz) = $targetDate
  AND status = 'valid'
  AND checkin_ref IN (
    SELECT id FROM checklogs_raw
    WHERE entity_id = $1 AND branch_id = $2
      AND type = 'checkin' AND status = 'valid'
      AND DATE(real_date_market AT TIME ZONE $tz) = $targetDate
  )
ORDER BY employee_id, timestamp ASC;
```

---

## Algoritmo del servidor privado

### Query base para checklogs del día

```sql
SELECT
  id, employee_id, type, status, timestamp, real_date_market,
  checkin_ref, is_suspect, geo_lat, geo_lng,
  etz, schedule_applied, employee_responsibility
FROM checklogs_raw
WHERE entity_id = $entityId
  AND branch_id = $branchId
  AND real_date_market >= $startOfDayUTC
  AND real_date_market <= $endOfDayUTC
ORDER BY employee_id, timestamp ASC;
```

**Por qué `real_date_market` como ventana temporal:**  
El campo `timestamp` puede ser ajustado administrativamente. `real_date_market` es la marca horaria original del dispositivo. El batch diario usa `realDateMarket` como fuente de verdad para determinar a qué día pertenece el evento (igual que el collector actual de Firebase).

### Query de task ratings del día

```sql
SELECT
  employee_id,
  AVG(rating) AS avg_rating,
  COUNT(*) FILTER (WHERE rating IS NOT NULL) AS tasks_rated,
  COUNT(*) AS tasks_total
FROM task_ratings_raw
WHERE entity_id = $entityId
  AND branch_id = $branchId
  AND DATE(rated_at AT TIME ZONE $tz) = $targetDate
GROUP BY employee_id;
```

### Algoritmo de construcción (pseudocódigo)

```
function buildDailyReportEnriched(checklogs, taskRatings, branchConfig, targetDate, tz):

  branchSchedule = extractSchedule(branchConfig, targetDate, tz)
  startDecimal = branchSchedule.startHour + branchSchedule.startMinute/60
  endDecimal = branchSchedule.endHour + branchSchedule.endMinute/60
  
  groupedByEmployee = groupBy(checklogs, 'employee_id')
  taskRatingByEmployee = indexBy(taskRatings, 'employee_id')
  
  employees = []
  for employeeId, logs of groupedByEmployee:
    
    // Identificar ciclos: checkins válidos de ese empleado ese día
    checkins = logs.filter(l => l.type == 'checkin' && l.status == 'valid')
    
    cycles = []
    for checkin of checkins:
      cycleId = checkin.checkin_ref ?? checkin.id
      cycleLogs = logs.filter(l => l.checkin_ref == cycleId && l.status == 'valid')
      cycleLogs.sort(by timestamp ASC)
      cycles.push(cycleLogs)
    
    employeeMetrics = initEmployeeMetrics(employeeId, logs)
    
    for cycle of cycles:
      checkinLog = cycle.find(l => l.type == 'checkin')
      checkoutLog = cycle.find(l => l.type == 'checkout')
      if (!checkinLog || !checkoutLog): continue  // ciclo incompleto
      
      tz_used = checkinLog.etz ?? tz
      start = toLocalDateTime(checkinLog.timestamp, tz_used)
      end = toLocalDateTime(checkoutLog.timestamp, tz_used)
      grossHours = end - start (in hours)
      
      // Breaks
      breakHours = calculateBreaks(cycle, tz_used, branchConfig.disableBreak)
      netHours = max(0, grossHours - breakHours)
      
      // Puntualidad IN
      startDecimalActual = start.hour + start.minute/60
      isOnTimeIn = startDecimalActual <= startDecimal
      lateMinutesIn = isOnTimeIn ? 0 : (startDecimalActual - startDecimal) * 60
      
      // Puntualidad OUT
      endDecimalActual = end.hour + end.minute/60
      isOnTimeOut = endDecimalActual <= endDecimal
      lateMinutesOut = isOnTimeOut ? 0 : (endDecimalActual - endDecimal) * 60
      
      // Acumular
      employeeMetrics.workedHours += netHours
      employeeMetrics.totalCheckins += 1
      employeeMetrics.onTimeCheckins += isOnTimeIn ? 1 : 0
      employeeMetrics.lateMinutesSumIn += lateMinutesIn
      employeeMetrics.totalCheckouts += 1
      employeeMetrics.onTimeCheckouts += isOnTimeOut ? 1 : 0
      employeeMetrics.lateMinutesSumOut += lateMinutesOut
    
    // Enriquecer con task ratings
    rating = taskRatingByEmployee[employeeId]
    employeeMetrics.avgTaskRating = rating?.avg_rating ?? null
    employeeMetrics.tasksRated = rating?.tasks_rated ?? 0
    
    employees.push(buildEmployeeReport(employeeMetrics, employeeId, logs))
  
  // Métricas globales de branch
  return buildBranchReport(employees, checklogs, targetDate, branchConfig)
```

---

## Escritura del resultado

El endpoint retorna el `DailyReportEnriched` al Cloud Function caller. El servidor privado también lo persiste en PostgreSQL antes de responder:

```
POST /api/build/daily-report
  → 1. BUILD: ejecutar el algoritmo sobre datos de PostgreSQL
  → 2. SAVE POSTGRES: UPSERT en daily_reports (id determinista)
  → 3. SAVE SNAPSHOT: UPSERT en pattern_snapshots (ver TDR-004)
  → 4. RETURN: el DailyReportEnriched al caller Firebase
  
Firebase recibe el resultado:
  → UPSERT en Firestore checkbiz_daily_report/{entityId}_{branchId}_{yyyyMMdd}
```

**Atomicidad:** Los pasos 2 y 3 están dentro de una transacción PostgreSQL. Si falla el snapshot, falla el daily report save también. El Cloud Function solo recibe éxito si ambos se guardaron.

---

## Compatibilidad con el formato actual de Firestore

El `DailyReportEnriched` es un superset del `DailyReport` actual. Los nuevos campos (`avgTaskRating`, `tasksCompleted`, `tasksRated`) son opcionales en la interfaz TypeScript existente. El frontend que lee `checkbiz_daily_report` sigue funcionando sin cambios; simplemente encuentra campos adicionales que puede ignorar o usar.

---

## Caso de no data (branch sin actividad ese día)

```
checklogs del día: 0
→ El servidor retorna { ok: false, code: "no_checklogs" }
→ El Cloud Function loguea y continúa con la siguiente branch
→ NO se escribe en PostgreSQL ni en Firestore para ese día/branch
→ Comportamiento idéntico al actual
```

---

## Rendimiento esperado

Por branch con 50 empleados y 300 checklogs del día:
- Query PostgreSQL: < 50ms (índice en entity_id + branch_id + real_date_market)
- Algoritmo de construcción (Node.js): < 200ms
- UPSERT en daily_reports + pattern_snapshots: < 100ms
- Response al Cloud Function: < 500ms total

Bajo el cron de 02:00 con 100 branches activas, el proceso completo toma < 2 minutos (las branches se procesan en paralelo, limitadas a 10 concurrentes para no saturar el servidor).

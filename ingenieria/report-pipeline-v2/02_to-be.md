# 02 — Arquitectura Objetivo (To-Be)

## Visión general

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ENCODEBIZ SAAS — DATA FLOW V2                   │
│                                                                         │
│   App / Frontend                                                        │
│        │                                                                │
│        ▼                                                                │
│   Firebase Functions (Cloud)         Servidor Privado (PostgreSQL)      │
│   ─────────────────────────          ──────────────────────────────     │
│                                                                         │
│   [Tiempo real - Operacional]        [Batch - Analítico]                │
│                                                                         │
│   createChecklog ──────────────────► POST /sync/checklogs               │
│        │                                    │                           │
│        ▼                                    ▼                           │
│   Firestore                         checklogs_raw (PostgreSQL)          │
│   entities/.../checklogs            (fuente analítica)                  │
│                                                                         │
│   rateTaskWorker ──────────────────► POST /sync/task-ratings            │
│        │                                    │                           │
│        ▼                                    ▼                           │
│   Firestore tasks                   task_ratings_raw (PostgreSQL)       │
│                                                                         │
│   [Cron 02:00 local]                [Batch diario]                      │
│   dailyCollectorData ──────────────► POST /build/daily-report           │
│        ▲                                    │                           │
│        │                         ┌──────────┴──────────┐               │
│        │                         ▼                     ▼               │
│        └──── Firestore      daily_reports         pattern_snapshots     │
│              checkbiz_      (PostgreSQL)          (PostgreSQL)          │
│              daily_report                                               │
│                                                                         │
│   [On demand - Frontend]                                                │
│   analyzeHeuristic ────────────────► GET /patterns/history              │
│        │                                    │                           │
│        │                            últimos 30 días de snapshots        │
│        ▼                                    │                           │
│   HeuristicCore V2 ◄───────────────────────┘                           │
│   (con contexto histórico)                                              │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Capa 1: Raw Data Sync (Firebase → PostgreSQL)

### Propósito
Mantener una réplica analítica de los checklogs y task ratings en PostgreSQL. Esta réplica es la fuente de verdad para todo el pipeline de reportes y IA. Firebase sigue siendo la fuente operacional para el app.

### Trigger: onChecklogWrite
Cuando se crea o actualiza un checklog en Firestore, el trigger existente `onWhriteChecklog` se extiende para también hacer un POST al servidor privado:

```
onWhriteChecklog (trigger Firestore existente)
  → [nuevo] SyncChecklogService.push(checklog)
      → POST {servidor_privado}/api/sync/checklogs
      → body: checklog completo en formato raw
      → si falla: log error, NO bloquea el flujo principal
```

**Regla crítica:** el sync a PostgreSQL es siempre **fire-and-forget**. Un fallo de conectividad no puede interrumpir el flujo operacional de checkin. Los datos siempre llegan a Firestore primero.

### Trigger: onWriteTaskRating (ya existe en el codebase)
Extender para también sincronizar ratings:

```
onWriteTaskRating
  → [nuevo] SyncTaskRatingService.push(rating)
      → POST {servidor_privado}/api/sync/task-ratings
```

### Idempotencia del sync
El servidor privado usa el `id` de Firestore como PRIMARY KEY en PostgreSQL. Un re-sync del mismo documento es un UPSERT inocuo.

---

## Capa 2: Daily Report Enriquecido

### Propósito
Reemplazar el cómputo on-demand (Firestore scan → buildDailyReport) por un proceso batch en el servidor privado que:
1. Lee checklogs del día desde PostgreSQL (query SQL, sin costo Firestore)
2. Lee task ratings del día por empleado desde PostgreSQL
3. Construye el DailyReport enriquecido con ratings
4. Escribe en PostgreSQL `daily_reports`
5. Escribe en Firestore `checkbiz_daily_report` (para el frontend)

### Nuevo flujo del cron
```
dailyCollectorDataController (cron 02:00 local)
  → para cada Branch activa:
      → POST {servidor_privado}/api/build/daily-report
         body: { entityId, branchId, date: "2026-06-01", timezone }
         
         [en el servidor privado]:
         → SELECT checklogs WHERE branch_id = ? AND date = ?
         → SELECT task_ratings WHERE branch_id = ? AND date = ?
         → buildDailyReportEnriched(checklogs, taskRatings, branchConfig)
         → UPSERT daily_reports (id determinista: entityId_branchId_yyyyMMdd)
         → UPSERT pattern_snapshots (id determinista: entityId_branchId_date)
         → return DailyReportEnriched
         
      → [en Firebase]: upsertDailyReport(reportEnriquecido) → Firestore
```

### DailyReport Enriquecido (nuevos campos)
```typescript
// Adición al DailyEmployeeReport existente
interface DailyEmployeeReportV2 extends DailyEmployeeReport {
  avgTaskRating?: number;      // media de ratings de tareas completadas ese día
  tasksCompleted?: number;     // nº de tareas completadas ese día
  tasksRated?: number;         // nº de tareas con rating ese día
}

// Adición al DailyReport existente
interface DailyReportV2 extends DailyReport {
  avgTaskRating?: number;      // media de ratings de todos los empleados ese día en la branch
  tasksCompleted?: number;
  tasksRated?: number;
}
```

---

## Capa 3: Histórico de Patrones (Pattern Snapshots)

### Problema actual
El patrón de una sucursal (`BranchPattern`) es un objeto mutable. Cada vez que llega un nuevo ciclo de checklog, se recalcula con los nuevos datos. El patrón anterior se pierde.

### Solución
Cuando el proceso batch diario construye el DailyReport, también toma una **fotografía del patrón** en ese momento y la guarda en `pattern_snapshots` con una clave `(entity_id, branch_id, date)`.

```sql
-- Clave única determinista → re-ejecución es idempotente
UNIQUE (entity_id, branch_id, snapshot_date)
```

El patrón que se guarda incluye todos los indicadores del día, incluidos los nuevos campos de task rating integrados.

### Qué habilita esto
- Ver la evolución de `reliability`, `avgCostEfficiency`, `stdStartHour` a lo largo del tiempo
- Detectar regresiones: "esta branch empezó a deteriorarse hace 2 semanas"
- Comparar períodos: "¿cómo era esta branch antes vs después de cambiar el horario?"
- Alimentar la IA con contexto temporal real

---

## Capa 4: IA con Contexto Histórico

### Problema actual
`HeuristicCore` recibe un `BranchPattern` (snapshot actual) y computa índices matemáticos. No tiene contexto de cómo llegó ese patrón a ese estado.

### Solución
Antes de llamar a `HeuristicCore`, se fetch el historial de snapshots de los últimos N días desde PostgreSQL. Este historial se incluye en el contexto del análisis.

```
analyzeHeuristic (request)
  → [nuevo] GET {servidor_privado}/api/patterns/history?entityId=&branchId=&days=30
      → retorna: array de 30 PatternSnapshot ordenados por fecha
  
  → HeuristicCore V2.analyzeBranch(currentPattern, patternHistory)
      → calcula indicadores actuales (igual que antes)
      → calcula tendencias sobre el historial (NUEVO):
           - tendencia de reliability (mejorando/empeorando/estable)
           - tendencia de punctuality (lateMinutesSumIn over time)
           - tendencia de avgTaskRating (mejorando la calidad del trabajo)
           - volatilidad: ¿el patrón es estable o errático?
      → pasa todo al prompt de IA con contexto enriquecido
```

El detalle del prompt rediseñado está en [06_ia-upgrade.md](./06_ia-upgrade.md).

---

## Decisiones de arquitectura

| Decisión | Alternativa descartada | Razón |
|----------|------------------------|-------|
| Servidor privado con Express + PostgreSQL | Supabase/PlanetScale cloud | Control total, sin costo por query, datos sensibles en infraestructura propia |
| Sync fire-and-forget desde Firebase trigger | Sync síncrono bloqueante | Un fallo del servidor privado no puede bloquear el app de los empleados |
| ID determinista para upserts | Auto-increment | Idempotencia: re-correr el proceso no genera duplicados |
| PostgreSQL como warehouse | BigQuery / Firestore analytics | SQL estándar, joins, sin costo por query, para datos de magnitud media |
| Firestore sigue siendo fuente del frontend | Migrar frontend a PostgreSQL | El frontend ya funciona. No se toca. Solo se enriquece lo que llega |
| Fases independientes | Big bang migration | Cada fase se puede desplegar y revertir sin afectar las demás |

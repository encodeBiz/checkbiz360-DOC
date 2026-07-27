# 04 — Fases de Implementación

Cada fase es **independiente y desplegable** sin romper el sistema actual.  
Ninguna fase requiere migración de datos históricos de Firestore.

---

## Fase 0: Contratos y Fundación Técnica

**Objetivo:** Cerrar contratos y dejar los fundamentos técnicos listos antes de tocar código productivo de Firebase.

**Prerequisito:** Ninguno.

### 0.1 Unificar payloads

Resolver las tres inconsistencias detectadas entre API contract, TDRs y schema:

| Campo | Decisión |
|---|---|
| Geo en ChecklogSyncPayload | Campos planos `geoLat`/`geoLng` (alineado con TDR-001 y schema). Sin objeto `geo` anidado. |
| `metadata` en ChecklogSyncPayload | No se incluye. Solo subcampos estructurados (`scheduleApplied`, `etz`, `employeeResponsibility`). |
| `rating` en TaskRatingSyncPayload | `number` (0.0–5.0, máx 1 decimal). El tipo `1\|2\|3\|4\|5` del TDR-001 queda corregido. Schema `NUMERIC(3,1)` ya es correcto. |

### 0.2 Migración SQL inicial

Crear el script de inicialización con las tablas de Fase 1:

```
analytics-server/migrations/001_initial.sql
```

Tablas: `checklogs_raw`, `task_ratings_raw`, `sync_log`.  
El script debe ser idempotente (`CREATE TABLE IF NOT EXISTS`).

### 0.3 Servidor analytics mínimo

Crear el servidor Express con:
- `GET /api/health` → `{ ok: true, db: "connected", timestamp: "..." }`
- Middleware de autenticación `X-Encodebiz-Key` en todas las rutas (401 si falta o no coincide)
- Pool de conexión PostgreSQL (pg o postgres.js)
- Logging estructurado (pino o equivalente) — todos los sync deben loguear `source_id`, `entity_id`, `status`, `duration_ms` y `error` si aplica
- Validación de payload con Zod en todos los endpoints de entrada (`/api/sync/checklogs`, `/api/sync/task-ratings`)

### 0.4 Formato de log Firebase (lado cliente)

Acordar el formato de `console.error` estructurado que usa el caller en Firebase cuando el sync falla. Este log es la única fuente de verdad cuando el servidor privado está caído:

```typescript
// SyncChecklogService — patrón obligatorio en el catch
console.error("[SyncChecklog] analytics sync failed", {
  checklogId: payload.id,
  entityId: payload.entityId,
  branchId: payload.branchId,
  error: (err as Error).message,
  ts: new Date().toISOString(),
});
```

Equivalente para `[SyncRating]`.

### 0.5 Tests de mappers

Antes de integrar con triggers, `SyncChecklogService` y `SyncTaskRatingService` deben tener unit tests cubriendo los casos definidos en TDR-001 §Testing: timestamps Firestore, geo null, rating decimal, metadata excluido, campos opcionales ausentes.

### Criterio de éxito Fase 0
- Contratos de API, TDRs y schema son consistentes (sin discrepancias documentales)
- `GET /api/health` responde `{ ok: true, db: "connected" }` en entorno local
- La migración SQL ejecuta sin errores sobre PostgreSQL 15 limpio
- Tests de `SyncChecklogService` y `SyncTaskRatingService` pasan para todos los casos límite
- No se ha tocado ningún archivo de Firebase Functions productivo

### Rollback
No aplica — Fase 0 no modifica código productivo.

---

## Fase 1: Raw Data Sync (Firebase → PostgreSQL)

**Objetivo:** Todo checklog y task rating creado o actualizado a partir de hoy queda también en PostgreSQL.

**Prerequisito:** Servidor privado desplegado con Express + PostgreSQL y endpoints de sync listos.

### Cambios en Firebase Functions

**1.1 Extender `onWhriteChecklog` (trigger existente)**

Archivo: `firebase-firestore-trigger/dataProcessing/onWhriteChecklog.ts`

Agregar al final del flujo (best-effort awaited):
```typescript
// Después del flujo existente (actualización de patrón, etc.)
try {
  await SyncChecklogService.push(checklogData);
} catch (err) {
  console.error("[SyncChecklog] Failed to sync to analytics server", err);
  // NO relanza — el flujo principal ya completó
}
```

**1.2 Extender `onWriteTaskRating` (trigger existente)**

Archivo: `firebase-firestore-trigger/onWriteTaskRating.ts`

Igual patrón best-effort awaited con `SyncTaskRatingService.push()`.

**1.3 Crear `SyncChecklogService` y `SyncTaskRatingService`**

```
functions/src/core/analytics/
  infrastructure/
    AnalyticsServerClient.ts    ← HTTP client con API key, timeout 7s, sin retry automático (ver ADR-002)
    SyncChecklogService.ts      ← mapea CheckLog → payload y llama al client
    SyncTaskRatingService.ts    ← mapea TaskRating → payload y llama al client
```

**Variables de entorno nuevas:**
```
ANALYTICS_SERVER_URL=https://analytics.tu-servidor.com
ANALYTICS_API_KEY=<secret>
```

### Cambios en el servidor privado

Crear los endpoints de recepción:
- `POST /api/sync/checklogs` → UPSERT en `checklogs_raw`
- `POST /api/sync/task-ratings` → UPSERT en `task_ratings_raw`
- `GET /api/health` → status check

### Criterio de éxito Fase 1
- Todos los nuevos checklogs aparecen en `checklogs_raw` en < 5 segundos
- Un fallo del servidor privado NO genera error en el app (solo log en Firebase)
- La tabla `sync_log` muestra tasa de éxito > 99%

### Rollback
Eliminar las líneas de `SyncChecklogService.push()` del trigger. Zero impact en el app.

---

## Fase 2: Daily Report Enriquecido desde PostgreSQL

**Objetivo:** El reporte diario se construye en el servidor privado con datos de PostgreSQL (no Firestore scan) e incluye task ratings.

**Prerequisito:** Fase 1 completada y con al menos 24 horas de datos acumulados.

### Cambios en Firebase Functions

**2.1 Modificar `dailyCollectorDataController`**

Reemplazar el bloque actual de:
```typescript
const checklogs = await checklogRepository.findInterbalCheckLog(...)
const dailyReport = buildDailyReportFromChecklogs(...)
await reportRepository.upsertDailyReport(dailyReport)
```

Por:
```typescript
const reportResult = await AnalyticsServerClient.buildDailyReport({
  entityId: branch.entityId,
  branchId: branch.id,
  date: targetDateLocal.toISODate(),  // "2026-06-01"
  timezone: timeZone,
  branchConfig: branch  // pasa la config de branch para el cálculo
});

if (reportResult.ok) {
  // El servidor ya guardó en PostgreSQL.
  // Firebase recibe el resultado para mantener la colección Firestore actualizada.
  await reportRepository.upsertDailyReport(reportResult.dailyReport);
}
```

**2.2 Agregar `buildDailyReport` al AnalyticsServerClient**

### Cambios en el servidor privado

Crear el endpoint:
- `POST /api/build/daily-report` — ver contrato en [05_contratos-api.md](./05_contratos-api.md)

El servidor implementa la lógica equivalente a `buildDailyReportFromChecklogs`, leyendo de PostgreSQL en lugar de Firestore.

**Enriquecimiento con task ratings:**
```sql
SELECT
  employee_id,
  AVG(rating) AS avg_rating,
  COUNT(*) AS tasks_rated
FROM task_ratings_raw
WHERE entity_id = $1
  AND branch_id = $2
  AND DATE(rated_at AT TIME ZONE $3) = $4::date
GROUP BY employee_id
```

Merge con el array de employees del DailyReport.

> **Nota sobre Fase 2 y Fase 3:** el endpoint `POST /api/build/daily-report` incluye la lógica de snapshot desde su implementación inicial, pero gateada por la variable de entorno `ENABLE_PATTERN_SNAPSHOTS`. En Fase 2 el flag está en `false` — el servidor guarda solo `daily_reports`. En Fase 3 se activa con `true`. Esto mantiene la transacción PostgreSQL entre ambas tablas intacta sin requerir cambios de código entre fases.

### Criterio de éxito Fase 2
- Los daily reports en Firestore `checkbiz_daily_report` contienen los campos `avgTaskRating`, `tasksCompleted`, `tasksRated`
- `ENABLE_PATTERN_SNAPSHOTS=false` — la tabla `pattern_snapshots` permanece vacía
- El frontend no requiere ningún cambio para mostrar los datos existentes
- El tiempo de generación del report no supera 10 segundos por branch

### Rollback
Revertir `dailyCollectorDataController` al código anterior. Los daily reports de Firestore vuelven al formato sin enrichment.

---

## Fase 3: Histórico de Patrones

**Objetivo:** Activar la captura de snapshots de patrón en cada ejecución de daily report. Los patrones dejan de disolverse.

**Prerequisito:** Fase 2 estable en producción.

> La lógica de snapshot ya existe en el endpoint `POST /api/build/daily-report` desde Fase 2 (ver nota anterior). Fase 3 es únicamente activar el flag.

### Cambio en el servidor privado

```bash
# Variable de entorno del servidor
ENABLE_PATTERN_SNAPSHOTS=true
```

Con el flag activo, al final de cada ejecución del endpoint, dentro de la misma transacción PostgreSQL:

```
1. Lee el BranchPattern actual desde Firestore via Admin SDK (branches/{branchId}.pattern)
2. Combina con los indicadores del daily report del día (punctuality rate, task rating, etc.)
3. UPSERT en pattern_snapshots con clave (entity_id, branch_id, snapshot_date)
4. Calcula los heuristic_scores del día y los guarda en el JSONB
```

No hay cambios en Firebase Functions para esta fase.

### Criterio de éxito Fase 3
- Después de 7 días, `pattern_snapshots` tiene 7 filas por branch activa
- Los snapshots son idempotentes: correr el proceso dos veces el mismo día no crea duplicados
- `GET /api/patterns/history?entityId=X&branchId=Y&days=30` retorna los snapshots

---

## Fase 4: IA con Contexto Histórico

**Objetivo:** El motor heurístico recibe los últimos 30 días de historial de patrones y genera análisis temporales enriquecidos.

**Prerequisito:** Fase 3 con al menos 14 días de snapshots acumulados.

### Cambios en Firebase Functions

**4.1 Modificar `analyzePattern` en `analyzePattern.ts`**

```typescript
// Antes de llamar a HeuristicCore:
const patternHistory = await AnalyticsServerClient.getPatternHistory({
  entityId,
  branchId,
  days: 30
});

// Pasar el historial al core
const core = new HeuristicCore(repository, lang as "es" | "en");
const report = await core.analyzeBranchV2(pattern, patternHistory);
```

**4.2 Crear `HeuristicCore.analyzeBranchV2`**

Misma lógica actual + capa de análisis temporal:
```typescript
computeTrend(history: PatternSnapshot[]): {
  reliabilityTrend: "improving" | "declining" | "stable",
  punctualityTrend: "improving" | "declining" | "stable",
  taskRatingTrend: "improving" | "declining" | "stable" | "no_data",
  volatility: "high" | "medium" | "low",
  daysOfData: number
}
```

### Criterio de éxito Fase 4
- La respuesta de `/analyzeHeuristic` incluye un campo `trend` con los indicadores temporales
- El análisis textual generado menciona la evolución temporal, no solo el estado actual
- Ver [06_ia-upgrade.md](./06_ia-upgrade.md) para el diseño completo del prompt

### Rollback
Eliminar el fetch a `getPatternHistory` de `analyzePattern.ts` y revertir a `HeuristicCore.analyzeBranch` (V1). Los snapshots en PostgreSQL no se tocan.

---

## Fase 5: Migración completa de heurística al servidor

**Objetivo:** `HeuristicCore` deja de ejecutarse en Firebase Functions. El servidor privado toma la responsabilidad del cálculo on-demand completo. Firebase queda como proxy delgado.

**Prerequisito:** Fase 4 completada y con al menos 14 días de snapshots acumulados.

### Contexto — por qué esta fase es necesaria

Después de Fase 3, el servidor ya computa `heuristic_scores` en el batch diario y los almacena en `pattern_snapshots`. Sin embargo, la petición on-demand de `analyzeHeuristic` sigue ejecutando `HeuristicCore V2` dentro de Firebase Functions, duplicando el cómputo y manteniendo una dependencia innecesaria en el entorno Firebase (cold start, límite de 60 s, lógica de negocio en una capa que debería ser solo de transporte).

### Cambios en Firebase Functions

**5.1 Convertir `analyzePattern.ts` en proxy**

El archivo pasa de orquestar el cálculo a ser un adaptador HTTP:

```typescript
// analyzePattern.ts — después de Fase 5: proxy puro, sin lógica de negocio
export const analyzePattern = async (entityId: string, branchId: string, lang: string) => {
  return AnalyticsServerClient.analyzeHeuristic({ entityId, branchId, lang });
};
```

El servidor lee directamente todo lo que necesita vía Admin SDK y PostgreSQL. Firebase no fetcha ni transforma nada. `HeuristicCore`, `HeuristicCalculator`, `HeuristicEvaluator` y `HeuristicNormalizer` dejan de invocarse desde Firebase. Pueden archivarse o eliminarse en una limpieza posterior.

### Cambios en el servidor privado

**5.2 Crear `POST /api/analyze/branch`**

```
POST /api/analyze/branch
body: { entityId, branchId, lang }

[servidor — todo via Admin SDK + PostgreSQL]:
→ Firestore Admin SDK: branches/{branchId}.pattern          → currentPattern (fresco, datos de hoy)
→ Firestore Admin SDK: heuristic_indicators (collection)    → thresholds de evaluación
→ PostgreSQL: SELECT 30 días de pattern_snapshots           → historial de tendencias
→ ComputeTrend(history)
→ HeuristicCore V2 (corre en Node en el servidor)
→ buildBranchNarrative(results, trend)
→ return BranchAnalysis
```

El servidor tiene Admin SDK, por lo que lee `currentPattern` fresco directamente desde Firestore sin intermediarios. Esto garantiza que el análisis usa los datos del día en curso (no el snapshot de ayer) y elimina la lectura en Firebase antes de la llamada.

Los thresholds de `heuristic_indicators` se leen vía Admin SDK en cada petición. Son documentos pequeños y de baja mutabilidad — pueden cachearse en memoria del proceso Express con TTL de 5 minutos para evitar lecturas repetidas.

**Estructura de respuesta** — idéntica a la V2 del motor actual, sin cambios en el contrato hacia el frontend:

```typescript
interface BranchAnalysisResponse {
  ok: true;
  branchId: string;
  reliability: number;
  dataPoints: number;
  results: HeuristicResultV2[];    // indicadores con trend y historicalContext
  trend: TrendAnalysis;            // resumen de tendencias
  narrative: BranchNarrative;      // highlights, alerts, positives
  lang: string;
  computedAt: string;              // ISO 8601
}
```

**5.3 Porta `HeuristicCore`, `HeuristicCalculator`, `HeuristicEvaluator` al servidor**

El servidor usa Firebase Admin SDK para:
- `branches/{branchId}.pattern` — `currentPattern` fresco
- Colección `heuristic_indicators` — thresholds de evaluación (con cache en memoria, TTL 5 min)

Sin migración de datos. Sin dependencia nueva: Admin SDK ya está inicializado en el servidor desde Fase 1 (se necesitaba para poder hacer writes de vuelta a Firestore en Fase 2 y lecturas en Fase 3).

### Criterio de éxito Fase 5
- `POST /api/analyze/branch` devuelve resultados equivalentes a los de `HeuristicCore V2` en Firebase
- Test de regresión: para un mismo `branchId` e historial, el servidor produce los mismos `results[]` que producía Firebase antes de la migración
- Firebase `analyzePattern.ts` tiene ≤ 5 líneas (proxy puro, sin imports de HeuristicCore)
- Cold start de Firebase no afecta el tiempo de respuesta de `analyzeHeuristic`
- `HeuristicCore`, `HeuristicCalculator`, `HeuristicEvaluator` marcados como `@deprecated` en Firebase (no eliminados hasta validación en producción)

### Rollback
Revertir `analyzePattern.ts` al estado de Fase 4 (Firebase orquesta HeuristicCore V2). El endpoint `/api/analyze/branch` puede quedar en el servidor sin efectos secundarios.

---

## Resumen del roadmap

```
Fase 0: Contratos y fundación [1-2 días]  → Payloads unificados, servidor mínimo, migración SQL, tests de mappers
Fase 1: Raw Sync              [1-2 días]  → Todos los eventos nuevos van a PostgreSQL
Fase 2: Daily Enriquecido     [2-3 días]  → Reportes con task ratings, sin Firestore scan
Fase 3: Pattern History       [1 día]     → Snapshots de patrones acumulándose
Fase 4: IA Histórica          [2-3 días]  → HeuristicCore V2 con contexto temporal (aún en Firebase)
Fase 5: Migración heurística  [2-3 días]  → HeuristicCore se mueve al servidor, Firebase queda como proxy
```

**Tiempo total estimado:** 9-14 días de desarrollo, con testing integrado entre fases.

**Orden estricto:** Las fases deben ejecutarse en orden. No empezar Fase 1 sin los criterios de éxito de Fase 0 cumplidos. Fase 5 requiere Fase 4 estable en producción.

# TDR-001 — AnalyticsServerClient: diseño del cliente HTTP Firebase → servidor privado

**Fecha:** 2026-06-02  
**Estado:** Diseño aprobado, pendiente implementación (Fase 1)  
**Componente:** `functions/src/core/analytics/infrastructure/AnalyticsServerClient.ts`

---

## Problema

Necesitamos un cliente HTTP en Firebase Cloud Functions que comunique con el servidor privado de PostgreSQL. Este cliente debe:
1. Manejar autenticación con API key
2. Tener timeout corto para no bloquear el trigger de checkin
3. Absorber fallos sin propagar errores al caller
4. Registrar fallos de forma útil para debugging
5. Ser reutilizable por todos los servicios de sync (checklogs, ratings, daily report)

---

## Restricciones del entorno

- **Timeout del trigger Firestore:** 60 segundos. El cliente no puede consumir más de ~8 segundos (el resto es el trabajo del trigger).
- **Cold start:** El cliente se instancia en tiempo de ejecución de la Cloud Function. No puede tener estado persistente entre invocaciones.
- **Sin HTTP/2:** Las Cloud Functions usan Node HTTP/1.1 estándar. El servidor privado debe aceptar HTTP/1.1.
- **Sin librerías de terceros pesadas:** El bundle de la Cloud Function tiene límites. Se usa el `fetch` nativo de Node 22 (disponible en Node 18+).
- **Terminología — "fire-and-forget" vs "best-effort awaited":** el cliente hace `await` con timeout de 7 s y captura el error. No es fire-and-forget puro (que no esperaría respuesta). El término preciso es **best-effort awaited**: se espera la confirmación si llega dentro del timeout, pero el fallo no se propaga al caller. La diferencia importa: si el servidor responde en 2 s con éxito, Firebase lo sabe y puede loguear el sync como exitoso; si el servidor tarda más de 7 s o está caído, Firebase absorbe el error con un log estructurado y el trigger finaliza normalmente.

---

## Decisión de diseño

### Estructura del cliente

```typescript
// functions/src/core/analytics/infrastructure/AnalyticsServerClient.ts

const BASE_URL = process.env.ANALYTICS_SERVER_URL;
const API_KEY = process.env.ANALYTICS_API_KEY;
const TIMEOUT_MS = 7000; // 7 segundos máximo

async function callServer<T>(
  method: "GET" | "POST",
  path: string,
  body?: object
): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        "X-Encodebiz-Key": API_KEY!,
      },
      body: body ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });

    if (!res.ok) {
      throw new Error(`Analytics server returned ${res.status} for ${path}`);
    }

    return res.json() as T;
  } finally {
    clearTimeout(timer);
  }
}

export const AnalyticsServerClient = {
  syncChecklogs: (checklogs: ChecklogSyncPayload[]) =>
    callServer<SyncResponse>("POST", "/api/sync/checklogs", { checklogs }),

  syncTaskRating: (rating: TaskRatingSyncPayload) =>
    callServer<SyncResponse>("POST", "/api/sync/task-ratings", { ratings: [rating] }),

  buildDailyReport: (params: BuildDailyReportParams) =>
    callServer<BuildDailyReportResponse>("POST", "/api/build/daily-report", params),

  getPatternHistory: (entityId: string, branchId: string, days: number) =>
    callServer<PatternHistoryResponse>(
      "GET",
      `/api/patterns/history?entityId=${entityId}&branchId=${branchId}&days=${days}`
    ),

  // Fase 5: proxy puro — el servidor resuelve currentPattern y thresholds via Admin SDK
  analyzeHeuristic: (params: { entityId: string; branchId: string; lang: string }) =>
    callServer<BranchAnalysisResponse>("POST", "/api/analyze/branch", params),
};
```

### Por qué fetch nativo y no axios/got

Node 22 tiene `fetch` nativo y estable. Añadir axios o got aumenta el bundle y añade una dependencia que hay que mantener. `AbortController` + `setTimeout` es suficiente para timeout.

### Por qué no retry automático

Ver ADR-002. El retry automático en contexto de trigger de Firestore es peligroso porque puede duplicar efectos laterales (el trigger ya actualizó el patrón). El retry solo se hace en el proceso de re-sync batch que opera sobre datos ya estabilizados.

### Manejo de errores en el caller (patrón obligatorio)

El cliente lanza excepciones. El caller es responsable de absorberlas:

```typescript
// En onChecklogWriteController — patrón fire-and-forget correcto
try {
  await AnalyticsServerClient.syncChecklogs([checklogPayload]);
} catch (err) {
  // Solo log. Nunca relanzar. El trigger ya completó su trabajo principal.
  console.error("[SyncChecklog] analytics sync failed", {
    checklogId: checkout.id,
    error: (err as Error).message,
    entityId: checkout.entityId,
    branchId: checkout.branchId,
  });
  // El sync_log del servidor (si llegó) ya registró el fallo.
  // Si no llegó, el proceso de re-sync batch puede recuperar desde Firestore.
}
```

---

## Ubicación en la arquitectura de capas

```
functions/src/
  core/
    analytics/                     ← nuevo módulo
      infrastructure/
        AnalyticsServerClient.ts   ← cliente HTTP (infra layer)
        SyncChecklogService.ts     ← mapeo CheckLog → payload (application layer)
        SyncTaskRatingService.ts   ← mapeo TaskRating → payload (application layer)
```

`SyncChecklogService` es la capa de aplicación que conoce el dominio (CheckLog) y lo transforma en el payload de la API. `AnalyticsServerClient` solo habla HTTP y no conoce el dominio.

---

## Payloads de sync

### ChecklogSyncPayload

Mapeado desde `CheckLog`:

```typescript
interface ChecklogSyncPayload {
  id: string;                    // Firestore doc ID
  entityId: string;
  branchId: string;
  employeeId: string;
  timestamp: string;             // ISO 8601 UTC
  realDateMarket: string | null; // ISO 8601 UTC, puede ser null
  type: "checkin" | "checkout" | "restin" | "restout";
  status: string;
  isSuspect: boolean;
  failedCode: string | null;
  checkinRef: string | null;     // campo 'checkin' del CheckLog
  closed: boolean;
  geoLat: number | null;
  geoLng: number | null;
  userAgent: string;
  deviceTrusted: boolean;
  scheduleApplied: object | null;
  etz: string | null;
  employeeResponsibility: object | null;
}
```

**Qué no se incluye en el payload:** el objeto `metadata` completo (puede ser grande y tiene campos variables). Solo se extraen los campos estructurados relevantes. El `metadata` completo se puede incluir en un campo `metadata: JSONB` si se necesita para auditoría, pero no para queries analíticas.

### TaskRatingSyncPayload

Mapeado desde `TaskRating` + params del trigger:

```typescript
interface TaskRatingSyncPayload {
  id: string;                    // `{taskId}_{employeeId}`
  entityId: string;
  branchId: string;
  employeeId: string;
  taskId: string;
  rating: number;               // 0.0–5.0, máximo 1 decimal (ej. 4.5) — ver 05_contratos-api.md y schema NUMERIC(3,1)
  ratedBy: string;
  ratedAt: string;               // ISO 8601 UTC
  comment: string | null;
  ratedByRole: string;
}
```

---

## Variables de entorno requeridas

```bash
# .env.encodebiz-services (producción)
ANALYTICS_SERVER_URL=https://analytics.encodebiz.internal
ANALYTICS_API_KEY=<secret-rotatable>

# .env.dev-encodebiz (desarrollo)
ANALYTICS_SERVER_URL=http://localhost:4000
ANALYTICS_API_KEY=dev-key-local
```

La URL de producción debe usar HTTPS. El servidor privado necesita certificado SSL válido (Let's Encrypt o similar).

---

## Testing

**`AnalyticsServerClient`** no tiene lógica de dominio → no necesita unit tests. Se cubre con un test de integración contra el servidor local (Express + PostgreSQL de test): verificar que un fallo del servidor no propaga error al caller.

**`SyncChecklogService` y `SyncTaskRatingService` SÍ necesitan unit tests** porque contienen lógica de mapeo y serialización con múltiples casos límite:

| Caso | Campo crítico |
|---|---|
| `timestamp` es Firestore `Timestamp` | conversión a ISO 8601 UTC |
| `realDateMarket` es `null` | debe producir `null` en el payload, no lanzar |
| `geo` es `null` o `undefined` | `geoLat: null, geoLng: null` en el payload |
| `rating` es `4.5` (decimal) | no debe truncarse a entero |
| `employeeResponsibility` ausente | `null` en el payload |
| `scheduleApplied` ausente | `null` en el payload |
| `metadata` presente en el CheckLog origen | no debe aparecer en el payload |

Tests de integración adicionales (contra servidor local):
- Sync exitoso produce fila en `checklogs_raw` con los valores esperados
- Re-sync del mismo checklog (UPSERT) no crea duplicados
- Servidor caído: el trigger de checkin completa sin error

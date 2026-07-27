# 05 — Contratos de API

Comunicación entre Firebase Cloud Functions y el servidor privado encodeBiz Analytics.

## Autenticación

Todos los requests llevan el header:
```
X-Encodebiz-Key: <API_KEY_SECRETA>
```

El servidor rechaza cualquier request sin este header con `401`. La key se configura en variables de entorno en ambos lados.

---

## POST /api/sync/checklogs

Sincroniza uno o más checklogs desde Firestore a PostgreSQL.

**Request:**
```json
{
  "checklogs": [
    {
      "id": "firestore_doc_id",
      "entityId": "qCUKnSnceXje2u6ECxmH",
      "branchId": "abc123",
      "employeeId": "emp456",
      "timestamp": "2026-06-01T08:03:00.000Z",
      "realDateMarket": "2026-06-01T08:03:12.000Z",
      "type": "checkin",
      "status": "valid",
      "isSuspect": false,
      "failedCode": null,
      "checkinRef": "checkin_id_vinculado",
      "closed": false,
      "geoLat": 40.416775,
      "geoLng": -3.703790,
      "userAgent": "Mozilla/5.0...",
      "deviceTrusted": true,
      "scheduleApplied": {
        "start": { "hour": 8, "minute": 0 },
        "end": { "hour": 17, "minute": 0 },
        "toleranceMinutes": 15,
        "source": "branch"
      },
      "etz": "Europe/Madrid",
      "employeeResponsibility": {
        "job": "Dependiente",
        "price": 12.50,
        "responsibility": "ventas"
      }
    }
  ]
}
```

> `metadata` completo no se incluye. Los subcampos con valor analítico (`scheduleApplied`, `etz`, `employeeResponsibility`) se mapean como campos de primer nivel. Ver TDR-002 para la lista completa de campos excluidos.
```

**Response 200:**
```json
{
  "ok": true,
  "synced": 1,
  "failed": 0
}
```

**Response 400:** Payload malformado.  
**Response 401:** API key inválida.  
**Response 500:** Error de base de datos (el caller loguea y no reintenta en esta request).

**Comportamiento del servidor:**
- UPSERT con `ON CONFLICT (id) DO UPDATE` → idempotente
- Inserta una fila en `sync_log` con status 'success' o 'failed'
- Acepta arrays de hasta 50 checklogs por request (batch sync en caso de reintento)

---

## POST /api/sync/task-ratings

Sincroniza valoraciones de tareas.

**Request:**
```json
{
  "ratings": [
    {
      "id": "taskId_employeeId",
      "entityId": "qCUKnSnceXje2u6ECxmH",
      "branchId": "abc123",
      "employeeId": "emp456",
      "taskId": "task789",
      "rating": 4.5,
      "ratedBy": "manager_uid",
      "ratedAt": "2026-06-01T16:30:00.000Z",
      "taskName": "Inventario semanal",
      "taskStatus": "validated",
      "taskCompletedAt": "2026-06-01T15:45:00.000Z"
    }
  ]
}
```

**Response 200:**
```json
{ "ok": true, "synced": 1, "failed": 0 }
```

---

## POST /api/build/daily-report

Construye el reporte diario enriquecido para una branch y fecha. Lee de PostgreSQL, escribe en PostgreSQL, devuelve el reporte para que Firebase lo guarde en Firestore.

**Request:**
```json
{
  "entityId": "qCUKnSnceXje2u6ECxmH",
  "branchId": "abc123",
  "date": "2026-06-01",
  "timezone": "Europe/Madrid",
  "branchConfig": {
    "id": "abc123",
    "entityId": "qCUKnSnceXje2u6ECxmH",
    "advance": {
      "startTimeWorkingDay": { "hour": 8, "minute": 0 },
      "endTimeWorkingDay": { "hour": 17, "minute": 0 },
      "disableBreak": false,
      "timeBreak": 30,
      "workScheduleEnable": true,
      "workSchedule": {
        "monday": { "start": { "hour": 8, "minute": 0 }, "end": { "hour": 17, "minute": 0 } }
      }
    },
    "address": { "timeZone": "Europe/Madrid" }
  },
  "currentPattern": {
    "branchId": "abc123",
    "entityId": "qCUKnSnceXje2u6ECxmH",
    "avgStartHour": 8.12,
    "avgEndHour": 17.03,
    "stdStartHour": 0.18,
    "stdEndHour": 0.22,
    "reliability": 0.87,
    "dataPoints": 142
  }
}
```

**Response 200:**
```json
{
  "ok": true,
  "dailyReport": {
    "entityId": "qCUKnSnceXje2u6ECxmH",
    "branchId": "abc123",
    "date": "2026-06-01T00:00:00.000Z",
    "workedHours": 72.4,
    "effectiveHours": 72.4,
    "totalCost": 905.0,
    "employeesCount": 8,
    "avgDistance": 12.3,
    "irregularEvents": 0,
    "failedChecklogs": 1,
    "validChecklogs": 32,
    "suspectRate": 0.03,
    "countSuspects": 1,
    "avgStartChecklogs": 8.08,
    "avgEndChecklogs": 17.05,
    "onTimeCheckins": 7,
    "totalCheckins": 8,
    "lateMinutesSumIn": 12.5,
    "onTimeCheckouts": 8,
    "totalCheckouts": 8,
    "lateMinutesSumOut": 0,
    "avgTaskRating": 4.2,
    "tasksCompleted": 12,
    "tasksRated": 10,
    "employees": [
      {
        "employeeId": "emp456",
        "workedHours": 8.2,
        "jobName": "Dependiente",
        "price": 12.50,
        "totalCost": 102.5,
        "responsibility": "ventas",
        "isValid": true,
        "isSuspect": false,
        "startChecklogs": 1,
        "endChecklogs": 1,
        "onTimeCheckins": 1,
        "totalCheckins": 1,
        "lateMinutesSumIn": 0,
        "onTimeCheckouts": 1,
        "totalCheckouts": 1,
        "lateMinutesSumOut": 0,
        "avgTaskRating": 4.5,
        "tasksCompleted": 2,
        "tasksRated": 2
      }
    ]
  },
  "patternSnapshot": {
    "entityId": "qCUKnSnceXje2u6ECxmH",
    "branchId": "abc123",
    "snapshotDate": "2026-06-01",
    "avgStartHour": 8.12,
    "reliability": 0.87,
    "avgTaskRating30d": 4.1
  }
}
```

**Response 404:**
```json
{ "ok": false, "code": "no_checklogs", "message": "No checklogs found for this branch and date" }
```

---

## GET /api/patterns/history

Retorna el historial de snapshots de patrón para una branch. Usado por `analyzeHeuristic` para el contexto temporal de la IA.

**Request:**
```
GET /api/patterns/history?entityId=qCUKnSnceXje2u6ECxmH&branchId=abc123&days=30
```

**Headers:** `X-Encodebiz-Key: ...`

**Response 200:**
```json
{
  "ok": true,
  "history": [
    {
      "snapshotDate": "2026-06-01",
      "avgStartHour": 8.12,
      "avgEndHour": 17.03,
      "stdStartHour": 0.18,
      "stdEndHour": 0.22,
      "reliability": 0.87,
      "dataPoints": 142,
      "avgCostEfficiency": 0.82,
      "costVariance": 0.15,
      "avgCycleCost": 125.30,
      "costTrend": "down",
      "avgTaskRating30d": 4.1,
      "tasksRated30d": 48,
      "heuristicScores": {
        "WTB": 8.91,
        "OSD": 0.40,
        "HCI": 0.78,
        "OSI": 0.74,
        "PSS": 0.76,
        "GHI": 0.65
      }
    }
  ],
  "daysRequested": 30,
  "daysAvailable": 12
}
```

**Notas:**
- `daysAvailable` puede ser menor a `daysRequested` si la Fase 3 lleva pocos días activa
- Si `daysAvailable < 7`, el caller debe omitir el análisis de tendencias (datos insuficientes)
- Ordenado **ASC por `snapshotDate`** (el más antiguo primero). El algoritmo TrendAnalyzer requiere orden cronológico para comparar primera mitad vs segunda mitad del historial (ver TDR-005). Si la UI necesita mostrar el más reciente primero, invierte el array en la capa de presentación.

---

## POST /api/analyze/branch

Ejecuta el análisis heurístico completo para una branch. El servidor resuelve todos los datos internamente vía Admin SDK y PostgreSQL. Firebase actúa como proxy puro.

**Fase:** 5

**Request:**
```json
{
  "entityId": "qCUKnSnceXje2u6ECxmH",
  "branchId": "abc123",
  "lang": "es"
}
```

El servidor lee internamente:
- `branches/{branchId}.pattern` vía Admin SDK → `currentPattern` fresco (incluye datos del día en curso)
- Colección `heuristic_indicators` vía Admin SDK → thresholds (cache en memoria, TTL 5 min)
- `pattern_snapshots` últimos 30 días vía PostgreSQL → historial de tendencias

**Response 200:**
```json
{
  "ok": true,
  "branchId": "abc123",
  "reliability": 0.87,
  "dataPoints": 142,
  "results": [
    {
      "id": "HCI",
      "value": 0.72,
      "severity": "warning",
      "label": { "es": "Índice de Confianza Heurística" },
      "consequence": { "es": "El patrón no está completamente consolidado" },
      "action": { "es": "Continuar acumulando ciclos de trabajo" },
      "trend": "improving",
      "trendNote": { "es": "Era 0.55 hace 14 días (+31%). Consolidándose." },
      "historicalContext": { "daysAnalyzed": 14, "valueNDaysAgo": 0.55, "delta": 0.17, "deltaPercent": 31 }
    }
  ],
  "trend": {
    "daysAvailable": 14,
    "dataQuality": "moderate",
    "reliability": "improving",
    "punctualityIn": "stable",
    "taskRating": "improving",
    "reliabilityDelta": 0.08,
    "volatilityAlert": false,
    "recoverySignal": false
  },
  "narrative": {
    "summary": { "es": "La sucursal muestra un patrón en consolidación..." },
    "highlights": [{ "es": "Confianza del patrón en crecimiento sostenido" }],
    "alerts": [],
    "positives": [{ "es": "Valoración de tareas por encima de la media (4.2/5)" }]
  },
  "lang": "es",
  "computedAt": "2026-06-05T10:00:00.000Z"
}
```

**Response 404:**
```json
{ "ok": false, "code": "branch_not_found", "message": "Branch pattern not found in Firestore" }
```

**Response 200 con `dataQuality: insufficient`:** se retorna el análisis actual sin sección de tendencias (`trend.daysAvailable < 7`).

**Notas:**
- El contrato de respuesta es idéntico al de `HeuristicCore V2` en Firebase — el frontend no necesita cambios.
- `trend` y `narrative` se omiten si `daysAvailable < 7`; el campo `trend.dataQuality` indica el motivo.

---

## GET /api/health

Status check. Usado por el monitor del servidor y por Firebase en el warm-up.

**Response 200:**
```json
{
  "ok": true,
  "db": "connected",
  "timestamp": "2026-06-01T10:00:00.000Z"
}
```

---

## Gestión de errores y reintentos

| Escenario | Comportamiento Firebase | Comportamiento Servidor |
|-----------|------------------------|------------------------|
| Servidor privado caído | Log error, continúa flujo normal | — |
| Timeout (> 8 segundos) | Log timeout, continúa flujo normal | Cancela request |
| 500 del servidor | Log error, NO reintenta automáticamente | Devuelve error, registra en sync_log |
| 401 (key inválida) | Log crítico + alerta (PagerDuty/email) | Rechaza con 401 |
| Checklog ya existe | — | UPSERT silencioso (idempotente) |

**No hay retry automático en tiempo real.** Si un sync falla, el dato sigue en Firestore y puede recuperarse con un proceso de re-sync manual o batch usando la colección de Firestore como fuente. El `sync_log` permite identificar qué documentos fallaron.

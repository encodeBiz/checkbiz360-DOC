# TDR-002 — Diseño del Raw Sync: qué datos se sincronizan, cuándo y cómo

**Fecha:** 2026-06-02  
**Estado:** Diseño aprobado, pendiente implementación (Fase 1)  
**Componentes:** `onChecklogWriteController`, `onWriteTaskRating`, `SyncChecklogService`, `SyncTaskRatingService`

---

## Problema

No todo evento de Firestore debe sincronizarse a PostgreSQL. El trigger `onChecklogWrite` se dispara para CUALQUIER escritura en `entities/{eid}/checklogs/{chid}`, incluyendo actualizaciones administrativas, correcciones manuales y checklogs fallidos. `onWriteTaskRating` se dispara tanto en creates como en updates.

Necesitamos definir exactamente:
1. Qué eventos disparan un sync
2. Qué datos se incluyen en el payload
3. Cómo se maneja un rating que se actualiza (re-valoración)

---

## Análisis del trigger onChecklogWrite actual

El `onChecklogWriteController` existente ya tiene una lógica de filtro:

```typescript
const checkout = change.data.after.exists ? (change.data.after.data() as CheckLog) : null;
if (!checkout || checkout.status !== "valid" || checkout.type !== "checkout" || checkout.isSuspect) {
  return console.log("Discarted Checklog", checkout?.type);
}
```

Solo procesa checkouts válidos y no sospechosos. Pero para el sync a PostgreSQL, **necesitamos sincronizar TODOS los tipos** (checkin, checkout, restin, restout) y **todos los estados** (valid, failed, pending-employee-validation), porque:

1. Los checklogs fallidos son datos analíticos importantes (tasa de error por branch, por dispositivo)
2. Los `restin`/`restout` son necesarios para calcular el tiempo neto trabajado en el servidor privado
3. Los checklogs `pending-employee-validation` deben aparecer en PostgreSQL para que cuando se resuelvan, el UPSERT actualice su estado

---

## Decisión: sync independiente del filtro del trigger

El sync se implementa en un bloque separado que NO comparte el filtro del trigger existente:

```typescript
export const onChecklogWriteController = async (event) => {
  const afterData = event.data.after.exists ? event.data.after.data() as CheckLog : null;
  const checklogId = event.params.chid;

  // ─── SYNC SIEMPRE (independiente del filtro de abajo) ───────────────────
  if (afterData) {
    // Si el documento existe después del write (no es delete), sincronizamos
    try {
      await SyncChecklogService.push({ id: checklogId, ...afterData });
    } catch (err) {
      console.error("[SyncChecklog] Failed", { id: checklogId, error: (err as Error).message });
    }
  }
  // ─────────────────────────────────────────────────────────────────────────

  // Filtro existente para actualización de patrones (no cambia)
  const checkout = afterData;
  if (!checkout || checkout.status !== "valid" || checkout.type !== "checkout" || checkout.isSuspect) {
    return;
  }
  // ... resto del código de actualización de patrones ...
};
```

### Por qué sync antes del filtro

Si el sync está después del filtro y el checklog es un `checkin` (que se descarta antes del filtro), nunca se sincronizaría. Un `checkin` sin su `checkout` correspondiente en PostgreSQL rompe el cálculo de ciclos.

### Caso delete (baja de checklog)

Si `afterData` es null (el documento se eliminó), NO se sincroniza. Las eliminaciones de checklogs son operaciones administrativas excepcionales. Si ocurren, el proceso de re-sync batch puede detectar divergencias entre Firestore y PostgreSQL mediante comparación de IDs. No se implementa sync de deletes en Fase 1.

---

## Análisis del trigger onWriteTaskRating

El trigger actual en `onWriteTaskRating`:
- Ruta: `entities/{entityId}/tasks/{taskId}/ratings/{employeeId}`
- Dispara en create Y update (onDocumentWritten)
- Ya maneja el delta (before/after) para actualizar el aggregate en Employee

El sync al servidor privado debe:
1. Dispararse solo si `after` existe (no en deletes)
2. Incluir `taskId` y `employeeId` de los params del trigger (ya disponibles)
3. El ID del registro PostgreSQL es `{taskId}_{employeeId}` → UPSERT actualiza si ya existe

```typescript
// En onWriteTaskRating, después del applyRatingDelta existente:
if (event.data?.after.exists) {
  const after = event.data.after.data()!;
  try {
    await SyncTaskRatingService.push({
      id: `${event.params.taskId}_${event.params.employeeId}`,
      entityId: event.params.entityId,
      taskId: event.params.taskId,
      employeeId: event.params.employeeId,
      branchId: after.branchId ?? null,
      rating: after.rating,
      ratedBy: after.ratedBy ?? null,
      ratedAt: (after.ratedAt as Timestamp).toDate().toISOString(),
      comment: after.comment ?? null,
      ratedByRole: after.ratedByRole ?? null,
    });
  } catch (err) {
    console.error("[SyncRating] Failed", err);
  }
}
```

---

## Transformaciones de tipos al serializar

El `CheckLog` de Firestore usa `Timestamp` de Firebase Admin para las fechas. Al serializar para el payload HTTP, se convierten a ISO 8601 UTC:

```typescript
// SyncChecklogService.ts
function toISO(ts: Date | Timestamp | null | undefined): string | null {
  if (!ts) return null;
  if (ts instanceof Date) return ts.toISOString();
  if (typeof (ts as any).toDate === "function") return (ts as any).toDate().toISOString();
  return null;
}
```

**Por qué no enviar Timestamps de Firestore directamente:** Los `Timestamp` son objetos con `seconds` y `nanoseconds`. El servidor privado (Node/Express) necesita strings ISO 8601 para parsear y guardar en columnas `TIMESTAMPTZ` de PostgreSQL. La conversión centralizada en `SyncChecklogService` evita errores de tipo en el servidor.

---

## Campos que NO se sincronizan

| Campo | Razón |
|-------|-------|
| `metadata` completo | Objeto muy variable, puede ser grande, no tiene queries analíticas directas |
| `requestUpdate` | Flag interno operacional, sin valor analítico |
| `deadline` | No usado en análisis de reportes |

Se sincronizan selectivamente los subcampos de `metadata` que sí tienen valor analítico: `scheduleApplied`, `etz`, `employeeResponsibility`, `realDateMarket`.

---

## Validación de integridad post-sync

Para Fase 1, la validación es manual y periódica:

```sql
-- Comparar conteos entre Firebase (vía export) y PostgreSQL
SELECT
  entity_id,
  COUNT(*) as postgres_count,
  DATE(timestamp) as fecha
FROM checklogs_raw
WHERE timestamp >= '2026-06-01'
GROUP BY entity_id, DATE(timestamp)
ORDER BY fecha DESC;
```

Se compara contra los conteos de Firestore. Una divergencia > 1% activa revisión del `sync_log`.

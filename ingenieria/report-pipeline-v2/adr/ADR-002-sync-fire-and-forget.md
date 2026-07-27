# ADR-002 — Sync a PostgreSQL como best-effort awaited desde triggers de Firestore

**Fecha:** 2026-06-02  
**Estado:** Aceptado  
**Decisionario:** Jose Acevedo

---

## Contexto

El trigger `onChecklogWrite` (Firestore) se dispara cada vez que un empleado hace checkin o checkout. Este trigger ya realiza trabajo crítico: recalcula el `BranchPattern` y el `EmployeePattern`. En este nuevo pipeline, también necesita sincronizar el checklog a PostgreSQL.

La pregunta es: **¿debe el trigger esperar confirmación del servidor PostgreSQL antes de finalizar, o debe enviarlo sin esperar?**

Hay dos posiciones:

**Opción A — Síncrono (await + propagación de error):**
```typescript
await SyncChecklogService.push(checklog); // bloquea hasta confirmación
```
Si el servidor privado falla → el trigger lanza error → Firestore reintenta el trigger → posibles efectos duplicados en el BranchPattern.

**Opción B — Fire-and-forget (try/catch absorbe error):**
```typescript
try {
  await SyncChecklogService.push(checklog); // espera pero absorbe fallo
} catch (err) {
  console.error("[Sync] Failed", err); // solo log
}
```
Si el servidor privado falla → el trigger termina normalmente → el checklog quedó en Firestore → se puede re-sincronizar después.

---

## Decisión

Se elige **Opción B: best-effort awaited**. El sync a PostgreSQL nunca puede interrumpir, retrasar ni causar reintento del flujo operacional de checkin.

> **Nota de terminología:** "fire-and-forget" sugiere que no hay `await`. Aquí sí hay `await`, pero con timeout de 7 s y el error se absorbe. El patrón correcto se llama **best-effort awaited**: el trigger espera la confirmación del servidor si esta llega dentro del timeout; si el servidor está caído o tarda demasiado, el error se captura con un log estructurado y el trigger finaliza normalmente. La diferencia práctica: podemos loguear éxitos y fallos en Firebase, no solo fallos.

---

## Justificación

**El checkin de un empleado es una operación de tiempo real con SLA implícito.**  
Un empleado ficha a las 08:00. Si el trigger falla por un problema de conectividad con el servidor privado y Firestore lo reintenta, el `BranchPattern` podría actualizarse dos veces con el mismo ciclo. Ese efecto lateral es peor que no sincronizar el dato a PostgreSQL temporalmente.

**Firebase garantiza durabilidad. PostgreSQL no es la fuente operacional.**  
El checklog siempre llega a Firestore primero. Si PostgreSQL no lo recibe en el sync inicial, el dato está seguro en Firestore y puede recuperarse. La pérdida de sync es temporal y recuperable; la doble actualización del patrón no lo es.

**El código del trigger ya es complejo.**  
`writeController.ts` recalcula el patrón del branch y del empleado (global y por branch), hasta 3 upserts. Añadir un punto de fallo síncrono más aumenta la superficie de errores difíciles de depurar.

---

## Protocolo de re-sync

Para que best-effort awaited no signifique "datos perdidos para siempre", se establece:

1. **Cuando el servidor está operativo** (fallo transitorio, timeout, 500): `sync_log` en PostgreSQL registra el intento con status `failed` + `error_message`.
2. **Cuando el servidor está caído** (no hay respuesta): `sync_log` no se puede escribir. En este caso, **el `console.error` estructurado de Firebase es la fuente de verdad**:
   ```typescript
   console.error("[SyncChecklog] analytics sync failed", {
     checklogId, entityId, branchId, error: err.message, ts: new Date().toISOString()
   });
   ```
   Estos logs se pueden exportar desde Cloud Logging para identificar los IDs no sincronizados.
3. Un proceso de re-sync batch (semanal o bajo demanda) reconstruye la lista de fallos uniendo:
   - `SELECT source_id FROM sync_log WHERE status = 'failed'`
   - IDs extraídos de logs de Cloud Logging si hubo caída del servidor
4. El endpoint `/api/sync/checklogs` acepta arrays de hasta 50 items para batch re-sync eficiente

> **Gap conocido:** si el servidor estuvo caído durante un período y Firebase Logging tampoco tiene los registros (ej. retención expirada), la única fuente canónica es Firestore. El proceso de reconciliación puede hacer una comparación por rango de fechas entre Firestore y `checklogs_raw` para detectar huecos.

---

## Consecuencias

**Positivas:**
- El app nunca se ve afectado por problemas del servidor privado
- El trigger es más simple y predecible
- Re-sync recuperable en cualquier momento

**Negativas / Compromisos aceptados:**
- Ventana de inconsistencia temporal entre Firestore y PostgreSQL si el servidor está caído
- Los daily reports de esa noche usarán datos que quizás tengan huecos (si el servidor lleva horas caído)
- Requiere proceso de re-sync implementado antes de producción

**Invariante que esta decisión protege:**
> *Un empleado nunca debe ver su fichaje fallido o lento por causa del pipeline analítico.*

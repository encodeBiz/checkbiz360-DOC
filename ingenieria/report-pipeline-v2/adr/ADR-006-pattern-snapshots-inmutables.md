# ADR-006 — Pattern snapshots idempotentes por fecha en lugar de patrón rolling único

**Fecha:** 2026-06-02  
**Estado:** Aceptado  
**Decisionario:** Jose Acevedo

---

## Contexto

El `BranchPattern` actual es un documento único por branch que se actualiza en cada ciclo de checkout mediante EMA (Exponential Moving Average). Es un "patrón vivo": nunca tiene historia, solo el estado presente ponderado por todos los ciclos pasados.

Para dar contexto histórico a la IA y a los dashboards de evolución, necesitamos poder responder preguntas como:
- "¿Cuál era la puntualidad de esta branch hace 3 semanas?"
- "¿La fiabilidad del patrón ha mejorado desde que se cambió el horario?"
- "¿Cuándo empezó a deteriorarse esta branch?"

Hay dos enfoques para preservar esa historia:

**Opción A — Versioning del patrón (append-only en Firestore):**
Cada vez que el patrón se actualiza, se crea un nuevo documento en Firestore `branches/{branchId}/pattern_history/{timestamp}`.

Problemas:
- Puede crearse un snapshot por cada checkout (decenas al día por branch)
- Firestore cobra por escritura
- Documentos de Firestore no son consultables con SQL

**Opción B — Snapshot diario en PostgreSQL (una fotografía por día):**
El proceso batch de las 02:00 toma una fotografía del patrón en ese momento y la guarda en `pattern_snapshots` con clave `(entity_id, branch_id, snapshot_date)`.

Características:
- Exactamente 1 snapshot por branch por día → volumen controlado
- Deduplicado: re-ejecución del batch no crea duplicados
- Consultable con SQL: `SELECT ... WHERE snapshot_date BETWEEN ...`
- El snapshot captura el estado del patrón *al cierre del día*, que es el momento más informativo

---

## Decisión

Se elige **Opción B**: snapshot diario idempotente en PostgreSQL, capturado durante el proceso batch de las 02:00 locales.

---

## Justificación

**La granularidad diaria es la correcta para análisis de tendencias.**  
Las tendencias de comportamiento laboral se manifiestan en días, semanas y meses, no en horas. Un snapshot por día es suficiente para detectar "la puntualidad empeoró esta semana" o "la fiabilidad mejora sistemáticamente los lunes".

**El momento de captura (02:00 local) es el óptimo.**  
El batch de 02:00 ya procesó todos los checklogs del día anterior. El patrón en ese momento refleja el estado más actualizado con los datos del día completo.

**El snapshot contiene más que el patrón actual.**  
Además de los campos del `BranchPattern` (avgStartHour, reliability, etc.), el snapshot incluye métricas del daily report del día (avgTaskRating, punctuality rate, total cost). Esto enriquece el histórico con datos que el patrón solo nunca tendría.

**Idempotencia es fundamental.**  
El snapshot de `(entity_id, branch_id, '2026-06-01')` usa `ON CONFLICT DO UPDATE`: si el batch se re-ejecuta, actualiza el mismo registro sin crear duplicados. Esto permite corregir datos tras un bug de batch simplemente re-corriendo el proceso — algo imposible con append-only. La compensación es que el histórico es mutable: un re-run posterior sobreescribe el snapshot del día. Es aceptable porque el batch siempre corre sobre los mismos datos fuente (checklogs ya estabilizados en PostgreSQL), por lo que una re-ejecución produce el mismo resultado salvo corrección explícita.

---

## Qué datos captura cada snapshot

```sql
-- Al momento de la captura (02:00 local de la branch):
snapshot_date          → ayer en hora local (el día que se reporta)
avg_start_hour         → del BranchPattern actual
avg_end_hour           → del BranchPattern actual
std_start_hour         → del BranchPattern actual
reliability            → del BranchPattern actual
data_points            → del BranchPattern actual
avg_cost_efficiency    → del BranchPattern actual
cost_trend             → del BranchPattern actual

-- Del daily_report del mismo día (nuevos):
avg_task_rating_30d    → media móvil de task ratings de los últimos 30 días
heuristic_scores       → JSON con todos los indicadores calculados ese día
                         { WTB, OSD, HCI, OSI, PSS, RCV, CVH, CPD, CRI, ... }

-- Backup completo:
raw_pattern            → JSON completo del BranchPattern para auditoría
```

---

## Consecuencias

**Positivas:**
- Volumen predecible y controlado (1 fila/branch/día)
- Historia del patrón nunca se pierde ni se sobreescribe
- Base para análisis de tendencias y contexto histórico para la IA
- Los heuristic_scores diarios permiten ver cómo evolucionaron los indicadores

**Negativas / Compromisos aceptados:**
- La historia empieza desde el día de activación de Fase 3 (no hay retroactividad automática)
- Si el batch falla para una branch en un día concreto, ese día no tiene snapshot (hueco en el histórico)
- El hueco se puede recuperar manualmente si se tiene el BranchPattern de ese día en Firestore (está disponible vía `branchRepo.findPatternByBranch`)

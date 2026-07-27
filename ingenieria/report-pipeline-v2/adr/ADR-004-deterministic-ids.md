# ADR-004 — IDs deterministas para todas las operaciones de upsert

**Fecha:** 2026-06-02  
**Estado:** Aceptado  
**Decisionario:** Jose Acevedo

---

## Contexto

El pipeline ejecuta procesos batch que pueden fallar a mitad y necesitar re-ejecutarse. Sin IDs predecibles, una re-ejecución crea registros duplicados. Con IDs predecibles, una re-ejecución es un UPSERT inocuo.

Los registros afectados son:

| Entidad | ID propuesto | Naturaleza |
|---------|-------------|------------|
| `checklogs_raw` | Firestore document ID | Ya es único por definición |
| `task_ratings_raw` | `{taskId}_{employeeId}` | Un empleado tiene un rating por tarea |
| `daily_reports` | `{entityId}_{branchId}_{yyyyMMdd}` | Un reporte por branch por día |
| `pattern_snapshots` | UNIQUE constraint `(entity_id, branch_id, snapshot_date)` | Un snapshot por branch por día |

La alternativa sería usar SERIAL / auto-increment y gestionar deduplicación a nivel de lógica de aplicación.

---

## Decisión

Todos los registros upsertables usan **IDs deterministas derivados de sus claves de negocio**. Las operaciones de inserción son siempre `INSERT ... ON CONFLICT DO UPDATE`.

---

## Justificación

**Re-ejecutabilidad sin deuda técnica.**  
Si el proceso de daily report falla al 60% (procesó 6 de 10 branches) y se re-ejecuta, las 6 primeras branches hacen UPSERT silencioso y las 4 restantes se procesan por primera vez. No hay lógica adicional de "¿ya lo procesé?".

**El ID determinista hace explícita la unicidad de negocio.**  
`{entityId}_{branchId}_{yyyyMMdd}` comunica directamente que "existe exactamente un reporte diario por branch por día". Esto es una regla de negocio, no solo un detalle técnico.

**Elimina necesidad de transacciones de coordinación.**  
Sin IDs deterministas, habría que buscar antes de insertar, o usar locks. Con UPSERT por clave, el motor de base de datos garantiza la atomicidad.

**El ID de Firestore ya es único y estable.**  
Para checklogs, el ID de Firestore es el ID natural. No hay riesgo de colisión. Solo se copia como PRIMARY KEY en PostgreSQL.

---

## Formato de IDs compuestos

```
daily_reports.id     = "{entityId}_{branchId}_{yyyyMMdd}"
                       ej: "qCUKnSnceXje2u6ECxmH_abc123_20260601"

task_ratings_raw.id  = "{taskId}_{employeeId}"
                       ej: "task789_emp456"

checklogs_raw.id     = Firestore document ID (sin transformación)
                       ej: "K9mXpR3vT8wQ..."
```

**Separador `_` en IDs compuestos:**  
Los IDs de Firestore son alfanuméricos sin guiones bajos. El separador `_` nunca colisiona con los componentes.

---

## Consecuencias

**Positivas:**
- Procesos batch son idempotentes por construcción
- No hay código de deduplicación en la lógica de aplicación
- El ID comunica la clave de negocio directamente
- Debugging trivial: el ID te dice exactamente qué representa el registro

**Negativas / Compromisos aceptados:**
- Los IDs de `daily_reports` son strings largos (no ints), levemente menos eficiente en índices B-tree de PostgreSQL
- No aplica para `pattern_snapshots` que usa SERIAL + UNIQUE constraint (el snapshot no tiene un ID de negocio significativo por sí solo)

**Invariante que esta decisión protege:**
> *Ningún proceso batch puede crear duplicados, independientemente de cuántas veces se re-ejecute.*

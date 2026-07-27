# ADR-007 — Task ratings en subcollección Firestore vs campo embebido en Task

**Fecha:** 2026-06-02  
**Estado:** Documentado (decisión pre-existente, no cambia)  
**Decisionario:** Jose Acevedo

---

## Contexto

Este ADR documenta una decisión arquitectónica ya implementada que es relevante para el pipeline v2: cómo están almacenadas las valoraciones de tareas en Firestore y por qué ese diseño facilita (o complica) el sync a PostgreSQL.

Las task ratings están en:
```
entities/{entityId}/tasks/{taskId}/ratings/{employeeId}
```

El documento del rating por employeeId contiene: rating (1-5), comment, ratedBy, ratedAt, employeeId, branchId, etc.

Alternativa que no se tomó: campo embebido en el documento `Task`:
```
tasks/{taskId}.workers[i].rating = { value: 4, ratedBy: ..., ratedAt: ... }
```

---

## Por qué la subcollección es la decisión correcta para el pipeline v2

**1. El trigger `onWriteTaskRating` ya existe y funciona.**  
Firestore dispara el trigger exactamente cuando se crea o modifica un rating. Con campo embebido en `Task`, el trigger sería `onTaskWrite`, que se dispara para CUALQUIER cambio en la tarea (asignación, cambio de estado, actualización). Habría que filtrar dentro del handler.

**2. La ruta del documento Firestore da el contexto completo.**  
`entities/{entityId}/tasks/{taskId}/ratings/{employeeId}` → el handler recibe `entityId`, `taskId` y `employeeId` como `event.params` sin leer el documento.

**3. Un documento por empleado por tarea es el ID natural para el sync.**  
Para `task_ratings_raw`, el ID en PostgreSQL es `{taskId}_{employeeId}`. Si el rating fuera un campo embebido en un array dentro de `Task`, tendríamos que extraer el employeeId del contenido y construir el ID nosotros.

**4. El aggregate `ratingTask` en el empleado se actualiza correctamente.**  
El trigger calcula el delta (before/after) y actualiza el aggregate de estrellas en el empleado sin re-leer todos los ratings de todas las tareas. Esto es O(1) por rating. Si estuviera embebido en `Task`, habría que leer todos los workers de la tarea para recalcular.

---

## Implicación para el pipeline v2

El sync de task ratings funciona así:

```
onWriteTaskRating (trigger existente)
  → ruta: entities/{entityId}/tasks/{taskId}/ratings/{employeeId}
  → event.params: { entityId, taskId, employeeId }
  → after.data(): { rating, ratedBy, ratedAt, branchId, comment, ... }
  
  [existente] → applyRatingDelta() → actualiza ratingTask en Employee
  [nuevo] → SyncTaskRatingService.push({
    id: `${taskId}_${employeeId}`,
    entityId,
    taskId,
    employeeId,
    branchId: after.data().branchId,
    rating: after.data().rating,
    ratedBy: after.data().ratedBy,
    ratedAt: after.data().ratedAt
  })
```

El diseño existente de subcollección hace que este sync sea trivial. No hay nada que cambiar en la estructura de datos de Firestore.

---

## Consecuencias para el pipeline

**Positivas:**
- Sync de ratings limpio y sin ambigüedad
- ID determinista natural (`taskId_employeeId`)
- El trigger correcto ya existe y está en producción

**Limitación a tener en cuenta:**
- `ratedAt` en el documento de rating es la fecha de valoración, no la fecha de la tarea. Cuando en el servidor privado se une `checklogs_raw` con `task_ratings_raw` para enriquecer el daily report, se debe usar `ratedAt` para determinar a qué día pertenece el rating, no `task.dueAt` ni `task.completedAt` (estos campos no están en el sync de ratings y requieren un fetch adicional si se necesitan).

# ADR-003 — Firestore sigue siendo la fuente de datos; cero migración de datos

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

`encodebiz-api` tiene dos almacenes: Firestore (operacional, vía Admin SDK) y PostgreSQL (analítico, warehouse del pipeline de reporting). Las tareas viven hoy en Firestore, en `entities/{entityId}/tasks/{taskId}` con subcolecciones `assignments`, `notes`, `resources`, `ratings`, `validations`, `activity`.

La pregunta: al montar el servicio `tasks`, ¿sigue leyendo/escribiendo Firestore, o se lleva el modelo a PostgreSQL como hizo el pipeline de reporting?

---

## Decisión

El servicio `tasks` **lee y escribe en el mismo Firestore**, con el mismo `FirestoreTaskRepository` portado tal cual. **No hay migración de datos** ni tabla nueva en PostgreSQL para esta iniciativa.

---

## Justificación

**Es una migración de cómputo, no de datos.** El objetivo es mover *quién sirve el HTTP*, no *dónde vive el dato*. Mantener Firestore hace la migración transparente: el dato no se mueve, no hay ventana de doble escritura, no hay backfill.

**Firestore es la fuente operacional de la plataforma.** Igual que fijó [ADR-003 del report-pipeline](../../report-pipeline-v2/adr/ADR-003-firestore-frontend-source.md), Firebase es la fuente en tiempo real del front y la app. Las tareas son datos operacionales en vivo (estados que cambian, evidencias, notas): pertenecen a Firestore.

**Los triggers/schedules que se quedan en Firebase dependen de Firestore.** Si el dato se moviera a PostgreSQL, la cadena reactiva (ver [ADR-002](./ADR-002-solo-http-lo-reactivo-en-firebase.md)) se rompería. Mantener Firestore mantiene esa cadena intacta.

**El analítico ya tiene su camino aparte.** Las valoraciones de tareas relevantes para reporting ya se sincronizan a PostgreSQL (`task_ratings_raw`) vía el pipeline existente. El servicio `tasks` no necesita duplicar eso.

---

## Consecuencias

**Positivas:**
- Migración sin riesgo de pérdida ni de inconsistencia de datos.
- El `FirestoreTaskRepository` se porta sin cambios de lógica (solo se ajusta la inicialización del Admin SDK al patrón de `@encodebiz/shared`).
- El front y la app pueden seguir leyendo Firestore en tiempo real mientras el HTTP se sirve desde el servidor.

**Negativas / Compromisos aceptados:**
- El servicio `tasks` no se beneficia de las capacidades analíticas de PostgreSQL (agregaciones, históricos). No es su rol: es API operacional.
- La latencia hacia Firestore desde el servidor depende de la región del proyecto Firebase; se acepta como coste conocido (el mismo que ya paga cualquier servicio del monorepo que usa Admin SDK).

# ADR-003 — Firestore sigue siendo la fuente; cero migración de datos

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El módulo documental guarda sus datos en Firestore (`entities/{entityId}/documents/...`, subcolecciones `acks` y `activity`, y la colección raíz `searchIndex`) y sus ficheros en Firebase Storage. Al portar la API, hay que decidir si los datos se mueven (p. ej. a PostgreSQL, como se hizo con el pipeline de checklogs) o se quedan donde están.

---

## Decisión

**Cero migración de datos.** Firestore permanece como fuente de verdad de los documentos, acks, actividad e índice de búsqueda. Firebase Storage sigue siendo el almacén de los ficheros. El servicio `documents` lee y escribe contra Firestore/Storage vía Admin SDK, exactamente igual que hoy hace `documentsHandler`.

---

## Justificación

- **El módulo es CRUD documental, no analítica.** No hay agregaciones ni consultas analíticas que justifiquen un modelo relacional; Firestore sirve bien las consultas por scope/tipo/estado con `orderBy` + cursor.
- **El índice de búsqueda ya vive en Firestore** (`searchIndex` con `keywords_prefix` para búsqueda por prefijo). Moverlo a otro motor sería un rediseño, fuera del alcance de un *lift-and-shift*.
- **Riesgo mínimo y reversibilidad total.** Al no tocar datos, el cutover es reversible con solo revertir la URL del cliente. No hay ventana de doble escritura ni backfill.
- **Consistencia con tasks** ([tasks-service/ADR-003]), que también conservó Firestore como fuente.

---

## Consecuencias

**Positivas:**
- El port no arrastra ningún trabajo de datos: ni esquema, ni backfill, ni sincronización.
- Firebase (triggers/otros consumidores, si los hubiera en el futuro) sigue viendo los mismos datos.

**Negativas / Compromisos aceptados:**
- El servicio depende de `GOOGLE_APPLICATION_CREDENTIALS` y del acceso a Firestore/Storage (misma dependencia que `tasks`/`reports`).
- La búsqueda sigue limitada a lo que permite el índice por prefijo en Firestore (un token de ≥3 caracteres, `array-contains`, tope 50). Mejorarla sería un cambio de motor, no de este port.

# ADR-006 — Conservar el índice de búsqueda en Firestore (`searchIndex`)

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

`GET /api/v1/documents?q=…` busca documentos por texto. En Firebase esto no se resuelve con una query directa sobre `documents` (Firestore no tiene full-text), sino con un **índice invertido propio** en la colección raíz `searchIndex`: cada documento genera una entrada con `keywords` y `keywords_prefix` (prefijos de 3–20 caracteres), y la búsqueda hace `array-contains` sobre un token normalizado.

Este índice lo mantiene el genérico `core/searchIndex` (tokenizer, generador de prefijos, `FirestoreSearchIndexRepository`) más el adaptador `documentSearchIndex.ts` del módulo. El subsistema **no existe todavía** en `encodebiz-api`.

**Opción A — Portar `core/searchIndex` tal cual** a `services/documents` y mantener el índice en Firestore.
**Opción B — Sustituir** la búsqueda por otro mecanismo (p. ej. índice en PostgreSQL, o un motor externo).

---

## Decisión

**Opción A: portar el subsistema de índice a `services/documents` y conservarlo en Firestore.** El servicio mantiene la entrada de `searchIndex` en cada alta (`indexDocument`), actualización (`reindexDocument`) y archivado (`removeDocumentIndex`).

---

## Justificación

- **Es un *lift-and-shift*, no un rediseño.** El objetivo del port es paridad de comportamiento, no mejorar la búsqueda. Cambiar el motor (Opción B) es un proyecto aparte con su propio backfill.
- **El índice ya está poblado en Firestore** para los documentos existentes; portar el mismo mecanismo mantiene esas entradas vigentes y coherentes.
- **Coste de port bajo.** `core/searchIndex` es pequeño (~200 LOC, autocontenido); su única dependencia externa es `firebase-admin`.
- **Consistencia con ADR-003** (Firestore sigue siendo la fuente).

---

## Consecuencias

**Positivas:**
- La búsqueda documental sigue funcionando idéntica tras el cutover, sobre las mismas entradas de `searchIndex`.
- El subsistema `core/searchIndex` queda disponible en `encodebiz-api` por si otro servicio lo necesita en el futuro.

**Negativas / Compromisos aceptados:**
- Se hereda la simplicidad del índice: búsqueda por **un solo token de ≥3 caracteres**, `array-contains`, tope 50 resultados, sin ranking. Es suficiente para el uso actual; mejorarla es trabajo futuro (Opción B).
- El reindexado es "borra + crea" (idempotente en reintentos) y `fire-and-forget` respecto a la respuesta HTTP: un fallo de índice no bloquea el alta, solo se loguea. Se preserva ese comportamiento.
- `core/searchIndex` se duplica si otro servicio ya lo tuviera; hoy no existe en `encodebiz-api`, así que se introduce una única vez en `documents`.

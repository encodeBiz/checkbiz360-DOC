# TDR-005 — Índice de búsqueda documental

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 2)
**Componente:** `services/documents` — `core/searchIndex` + `documentSearchIndex`

---

## Problema

`GET /api/v1/documents?q=…` busca por texto. Firestore no tiene full-text, así que el módulo
mantiene un índice invertido propio en la colección raíz `searchIndex`. Hay que portar el
subsistema genérico `core/searchIndex` (aún inexistente en `encodebiz-api`) y el adaptador
`documentSearchIndex.ts`.

## Subsistema `core/searchIndex` (a portar)

```
core/searchIndex/
  domain/SearchIndex.ts               InputSearchIndex / SearchIndex (keywords, keywords_prefix, type, index, entityId)
  domain/SearchIndexRepository.ts     create / update / delete
  infrastructure/FirestoreSearchIndexRepository.ts   colección "searchIndex", docId derivado del path (/ → __)
  interfaces/createIndex.controller.ts  normalizeText + tokenizeBasic (stopwords ES) + buildPrefixes(3..20)
```

- `createIndex({fields, type, index, entityId})`: normaliza (lowercase, quita acentos/símbolos),
  tokeniza (quita stopwords), genera prefijos de 3–20 chars, y hace `set()` (idempotente: un doc
  por `index` path).
- **Ajuste de import**: `FirestoreSearchIndexRepository` importa `admin` desde
  `core/shared/firebase/admin`; se reapunta a la init de firebase-admin del servicio `documents`.
- El `type` de `SearchIndex` incluye `"document"` (ya contemplado en la union).

## Adaptador `documentSearchIndex.ts`

- `indexDocument(doc, ctx)` → `reindexDocument`: borra la entrada previa (`searchIndexRepo.delete`) y crea una nueva (`createIndex`). Idempotente en reintentos.
- Path de índice: `/entities/{entityId}/documents/{documentId}`.
- Campos indexados: `title`, `type`, `filename`, `description?`, `branchName?`,
  `employeeName?`, `employeeEmail?` (de `DocumentIndexContext`), y `tags` (join de `metadata.tags`).
- `removeDocumentIndex(entityId, documentId)` — en archivado (los archivados salen de la búsqueda).
- `searchDocumentIds(entityId, q)`: normaliza `q` a **un** token de ≥3 chars y consulta
  `searchIndex where entityId == … and type == "document" and keywords_prefix array-contains token`
  con `limit 50`; devuelve los `documentId` (último segmento del `index`).

## Puntos de cableado en los casos de uso (sin cambios de lógica)

| Caso de uso | Llamada al índice |
|---|---|
| `CreateDocument` | `indexDocument(document, indexContext)` — `fire-and-forget`, error solo logueado |
| `UpdateDocument` | `reindexDocument(updated, indexContext)` — idem |
| `ArchiveDocument` | `removeDocumentIndex(entityId, documentId)` — idem |
| `FindDocuments` (flujo `q`) | `searchDocumentIds(entityId, q)` → `findByIds` → filtro por permiso |

## Consideraciones

- El índice es `fire-and-forget` respecto a la respuesta: un fallo al indexar **no** rompe el
  alta/actualización/archivado (se loguea). Se preserva.
- Firestore exige índices compuestos para algunas queries; `searchDocumentIds` usa
  `entityId + type + keywords_prefix(array-contains)`. Si el índice compuesto no existe en el
  proyecto, la primera búsqueda fallará con un enlace de creación — verificar en la prueba e2e.

## Criterio de aceptación

- Tras un alta, existe una entrada en `searchIndex` con `type:"document"` y `keywords_prefix`
  conteniendo prefijos del título.
- `GET /?q=<prefijo del título>` devuelve el documento (si el actor puede leerlo); tras archivar,
  deja de aparecer.

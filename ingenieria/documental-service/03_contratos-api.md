# 03 — Contratos de API

**Base:** `https://<host>/api/v1/documents`
**Auth:** cabecera `Authorization: Bearer <Firebase ID token>`. El actor y su nivel se resuelven en `DocumentPermissionService.resolveActor` (ver [TDR-002](./tdr/TDR-002-resolucion-actor-y-matriz-de-permisos.md)). **No hay staff JWT.**
**Contrato preservado:** request/response idénticos a los del `documentsHandler` actual en Firebase. Esta migración **no** cambia el contrato; solo cambia el host que lo sirve.

> Nota: bajo `documentsHandler` el router se monta en `/documents`; en el servicio se monta en `/api/v1/documents`. La ruta relativa de cada endpoint (`/`, `/:documentId`, …) es la misma.

Envoltura de respuesta: éxito → `{ ok: true, ... }`; error → `{ code, error }` con un `code` del catálogo `DOCUMENT_ERRORS` (ver final del documento).

Regla transversal de auth (todas las rutas): sin token → `401 auth/unauthorized`. Actor sin ninguna vinculación con la entidad (ni owner/admin, ni empleado activo, ni responsabilidades) → `403 documents/unauthorized`.

---

## Documentos

### `GET /` — listar / buscar documentos
Query: `entityId` (obligatorio), `q?` (búsqueda por índice), `scope?` (`entity|branch|employee`), `branchId?`, `employeeId?`, `type?`, `status?` (`active|archived`), `createdFrom?`, `createdTo?`, `limit?` (1–100, def. 20), `cursor?`.
Comportamiento:
- **Con `q`** → búsqueda por índice (`searchIndex`): resuelve IDs, carga los docs, filtra por permiso y por el resto de filtros en memoria. Sin paginación por cursor (`nextCursor: null`).
- **Con `employeeId` y sin `scope`** → vista "todo lo del empleado": fan-out sobre scope `entity` + cada sucursal del empleado + scope `employee`, mezcla, filtra por permiso, ordena `createdAt DESC` y pagina en memoria.
- **Resto** → listado por Firestore con `orderBy(createdAt DESC, id DESC)` + cursor.
- `status`: si no se especifica, para actores **no** owner/admin se fuerza a `active`; owner/admin ven todo.
- Cada documento se enriquece con `ackStatus` (para el actor si el doc requiere ack y el actor es empleado) y `branch` (`{id,name}` en docs de scope branch). Nunca incluye `storagePath`.
`200` → `{ ok, documents: DocumentWithAckStatus[], nextCursor, total }`. `400` si falta `entityId` o si `scope`/`type`/`status` son inválidos.

### `POST /` — crear documento  *(multipart/form-data)*
Permiso: `canCreate(actor, scope, branchId, type)`.
Campos (form-data): `entityId`, `scope`, `type`, `title` (obligatorios); `branchId?` (obligatorio si `scope=branch|employee`), `employeeId?` (obligatorio si `scope=employee`), `description?`, `visibleToRoles` (JSON array de `worker|supervisor|manager`, ≥1), `requiresAcknowledgement?` (`"true"`), `acknowledgementMode?`, `expiresAt?`, `metadata?` (JSON `{externalRef?, tags?}`), y el fichero en el campo `file`.
Validaciones clave:
- `scope∈{entity,branch,employee}`, `type∈` catálogo, `visibleToRoles` estricto (rechaza si algún valor es inválido).
- `requiresAcknowledgement=true` exige `acknowledgementMode` acorde al scope (`employee→single_employee`, `branch→branch_employees`); `entity` **no soportado en V1** → 400.
- Fichero: obligatorio; MIME en la allow-list; tamaño ≤ **10 MB**.
- Existencia: `branchId`/`employeeId` deben existir en la entidad; para tipos no-RRHH, el empleado debe tener responsabilidad activa en la sucursal indicada.
Efectos: sube el fichero a Storage (privado), crea el doc (`status: active`, `version: 1`, `uploadedBy`), lo indexa, registra actividad `created` y **espera** las notificaciones (`doc_uploaded` y, si aplica, `doc_ack_required`) antes de responder.
`201` → `{ ok, document }` (sin `storagePath`; desde el 2026-10-09 con `contentSha256`, el SHA-256 del fichero). Errores: `400` (bad_request, invalid_scope, invalid_type, branch_required, employee_required, invalid_visibility_roles, invalid_acknowledgement_mode, file_required, invalid_mime_type, file_too_large, employee_not_in_branch), `404` (branch_not_found, employee_not_found), `403` (unauthorized), `401`.

### `GET /:documentId` — detalle
Permiso: `canRead(actor, document)`.
Query: `entityId` (obligatorio).
`200` → `{ ok, document: DocumentWithAckStatus }` (con `ackStatus` y `branch`, sin `storagePath`). `404` not_found. `403` unauthorized. `400` si falta `documentId`/`entityId`.

### `PATCH /:documentId` — actualizar (metadatos)
Permiso: `canUpdate` (= `canArchive`). Documentos archivados no se pueden editar (`403`).
Body (JSON): `entityId` (obligatorio) + campos editables opcionales: `title`, `description`, `visibleToRoles`, `requiresAcknowledgement`, `acknowledgementMode`, `expiresAt` (fecha o `null` para limpiar), `metadata`.
Reglas de ack idénticas al alta, validadas contra el **scope actual** del documento (`entity` → 400). Cada PATCH incrementa `version` y reindexa. No cambia el fichero binario.
`200` → `{ ok, document }`. `404` not_found. `403` unauthorized (incluye documento archivado). `400` validaciones.

### `DELETE /:documentId` — archivar (soft-delete)
Permiso: `canArchive`.
Query: `entityId` (obligatorio), `archiveReason?`.
Efectos: `status → archived` (+ `archivedBy/At`, `archiveReason`), lo quita del índice de búsqueda, registra actividad `archived`. No borra el fichero de Storage ni el doc de Firestore.
`200` → `{ ok: true }`. `404` not_found. `409` already_archived. `403` unauthorized.

### `GET /:documentId/download` — URL de descarga firmada
Permiso: `canRead`.
Query: `entityId` (obligatorio).
Efectos: genera una **signed URL de lectura con TTL 1 minuto** para `storagePath`; registra actividad `download_requested`.
`200` → `{ ok, url, expiresAt (ISO) }`. `404` not_found. `403` unauthorized.

---

## Confirmación de lectura (Acknowledgements)

### `POST /:documentId/ack` — confirmar lectura
Permiso: `canAcknowledge` (el doc debe requerir ack; el actor debe poder leerlo y encajar en el `acknowledgementMode`).
Body (JSON): `entityId` (obligatorio); **desde el 2026-10-09, opcionales `challengeId` y `signature`**: el acuse va
firmado con la clave del móvil ([firma](../firma/README.md) §Lado del servidor). El reto se pide a
`POST /api/v1/checkinbiz/auth/signing-challenges` con `purpose: "documents.acknowledgement"` y el `subject` que
devuelve `GET /:documentId/signing-subject`.
Efectos: idempotente — si ya existe ack del empleado, lo devuelve sin tocarlo (un acuse pulsado no se «sube» a firmado
después); si no, crea `acks/{employeeId}` con `documentVersion` = versión actual y registra actividad `acknowledged`.
Con reto y firma, el servidor **comprueba la firma** contra las claves del empleado vigentes al emitir el reto y guarda en
el acuse `method` (`biometric_signature` | `device_credential`, según el nivel de la clave), `verified: true` y
`signature { challengeId, keyId, level, signature }`. Sin firma, el acuse queda como hasta ahora (`method: "tap"`,
`verified: false`).
`200` → `{ ok: true }`. `404` not_found. `400` acknowledgement_not_required / **signature_invalid** (con `reason`:
`challenge_not_found` | `challenge_expired` | `challenge_used` | `challenge_mismatch` | `no_signing_key` |
`signature_invalid`). `403` acknowledgement_not_allowed / unauthorized (o actor sin `employeeId`).

### `GET /:documentId/signing-subject` — qué se firma al acusar recibo
Permiso: `canRead`; el documento debe requerir acuse. Query: `entityId`.
`200` → `{ purpose: "documents.acknowledgement", subject: { documentId, version, contentSha256?, title } }`.
`contentSha256` es el SHA-256 del fichero, calculado al subirlo (los documentos anteriores al 2026-10-09 no lo
tienen y el `subject` lo omite): la firma queda atada al contenido, no solo al id.

### El acta de una firma (servicio `reports`)
Cada acuse firmado guarda `signature.challengeId` y `signature.evidence { path, sha256 }` (la evidencia cerrada en
Storage al firmar). El acta se pide a `reports`, con el ID token de Firebase y asiento en la empresa:
`GET /api/reports/signatures/acta?entityId&challengeId` → `{ url, expiresAt }` (PDF, URL firmada de 5 min) y
`GET /api/reports/signatures/evidence?entityId&challengeId` → `{ url, expiresAt, sha256 }` (el JSON para un perito).
En el panel: ficha del documento → confirmaciones → «Descargar el acta de firma». Diseño y contenido en
[firma §El acta](../firma/README.md).

### `GET /:documentId/acks` — listar confirmaciones
Permiso: **solo owner/admin** (`actor.isOwnerAdmin`); cualquier otro → `403`.
Query: `entityId` (obligatorio).
`200` → `{ ok, acks: DocumentAcknowledgement[], total }`. `404` not_found. `403` unauthorized.

---

## Tipos de referencia

`DocumentType`: `payroll | contract | warning | attention_call | justification | certificate | policy | procedure | risk_prevention | branch_protocol | project_document | other`.
- **RRHH-puros** (`payroll`, `contract`): solo owner/admin los crean/gestionan.
- **Disciplinarios** (`warning`, `attention_call`): en scope employee, solo `manager` exacto de la sucursal.

`DocumentScope`: `entity | branch | employee`. `DocumentVisibilityRole`: `worker | supervisor | manager`. `DocumentStatus`: `active | archived`.

`DocumentWithAckStatus` = `ManagedDocument` **sin** `storagePath`, **más** `ackStatus: DocumentAckStatus | null` y `branch: {id,name} | null`.

## Catálogo de códigos de error (`DOCUMENT_ERRORS`)

`documents/bad_request`, `documents/unauthorized`, `documents/not_found`, `documents/branch_required`, `documents/employee_required`, `documents/invalid_scope`, `documents/invalid_type`, `documents/invalid_visibility_roles`, `documents/invalid_acknowledgement_mode`, `documents/file_required`, `documents/file_too_large`, `documents/invalid_mime_type`, `documents/employee_not_found`, `documents/employee_not_in_branch`, `documents/branch_not_found`, `documents/restricted_document_type`, `documents/already_archived`, `documents/acknowledgement_not_required`, `documents/acknowledgement_not_allowed`. Auth de token: `auth/unauthorized`. Error interno: `documents/internal_error`.

## MIME permitidos

`application/pdf`, `image/jpeg`, `image/png`, `image/webp`, `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `application/vnd.ms-excel`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`. Tamaño máximo: **10 MB**.

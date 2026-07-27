# 05 — Integración: Front de administración

Guía de consumo del servicio `documents` desde el back office. Cuando termine el cutover (Fase 3), la base pasa de la URL de `documentsHandler` a `https://<host>/api/v1/documents`; el resto del contrato es idéntico.

## Autenticación

Todas las llamadas llevan `Authorization: Bearer <Firebase ID token>`. El servidor resuelve el actor (owner/admin, empleado, responsabilidades por sucursal) a partir del `uid` del token y del `entityId` de la petición. No hay staff JWT en documental.

## Nivel de permisos (qué puede hacer cada quién)

| Acción | Quién |
|---|---|
| Ver documento | owner/admin; en su sucursal, según `visibleToRoles` y nivel; el propio empleado ve sus docs de scope employee |
| Crear scope branch | owner/admin, o `manager+` de esa sucursal (nunca tipos RRHH) |
| Crear scope employee | owner/admin, o `manager+` de la sucursal; disciplinarios (`warning`/`attention_call`) solo `manager` exacto |
| Crear tipos RRHH (`payroll`, `contract`) | **solo owner/admin** |
| Crear scope entity | **solo owner/admin** |
| Actualizar / archivar | owner/admin; `manager+` de la sucursal (nunca tipos RRHH) |
| Listar acks (`GET /:id/acks`) | **solo owner/admin** |

Detalle completo en [TDR-002](./tdr/TDR-002-resolucion-actor-y-matriz-de-permisos.md).

## Flujos

### Subir un documento
`POST /api/v1/documents` como `multipart/form-data`:
- Campos: `entityId`, `scope`, `type`, `title` (obligatorios); `branchId`/`employeeId` según scope; `visibleToRoles` como **JSON string** (p. ej. `'["worker","manager"]'`); `requiresAcknowledgement` como `"true"`; `acknowledgementMode` acorde al scope; `metadata` como JSON string; y el binario en el campo `file`.
- Límite: 10 MB; MIME dentro de la allow-list (PDF, imágenes JPEG/PNG/WEBP, Word, Excel).
- Respuesta `201 { ok, document }`. El `document` no trae `storagePath` (privado).

### Listar y buscar
`GET /api/v1/documents?entityId=…` con filtros `scope`, `branchId`, `employeeId`, `type`, `status`, `createdFrom`, `createdTo`, `limit`, `cursor`. Búsqueda de texto con `q` (usa el índice; devuelve como máximo la primera página, sin cursor). Vista "todo del empleado": pasar `employeeId` **sin** `scope`.
Paginación por `cursor`: repetir la llamada con el `nextCursor` recibido hasta que sea `null`.

### Descargar
`GET /api/v1/documents/:id/download?entityId=…` → `{ url, expiresAt }`. La `url` es una signed URL con **1 minuto** de validez: descárgala inmediatamente, no la caches.

### Confirmación de lectura (ack)
Para documentos con `requiresAcknowledgement`, el destinatario llama `POST /api/v1/documents/:id/ack` con `{ entityId }`. Es idempotente. El estado por-actor viene en `ackStatus` al leer el documento. El listado de quién ha confirmado (`GET /:id/acks`) es solo para owner/admin.

### Editar / archivar
`PATCH /api/v1/documents/:id` (JSON) cambia metadatos y sube `version`; no cambia el fichero. `DELETE /api/v1/documents/:id?entityId=…&archiveReason=…` archiva (soft-delete): el documento deja de aparecer en búsquedas pero se conserva.

## Notas de contrato

- Los códigos de error vienen en `{ code, error }`; el `code` es del catálogo `documents/*` (ver [03_contratos-api.md](./03_contratos-api.md)).
- `403 documents/unauthorized` = el actor no tiene permiso; `403 auth/unauthorized` = token inválido/ausente.
- Un documento archivado no se puede editar (`403`) ni se archiva dos veces (`409 documents/already_archived`).
- El servicio expone CORS abierto (igual que el resto de servicios front-facing), por lo que el back office lo llama directo desde el navegador.

# TDR-003 — Storage privado, paths por scope, signed URL y multipart

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 2)
**Componente:** `services/documents` — `DocumentStorageService` + subida multipart

---

## Problema

El alta sube un fichero (hasta 10 MB) a Firebase Storage de forma privada; la descarga se sirve
con una URL firmada de vida corta. Hay que portar esa lógica y el parseo multipart sin cambiar
el contrato ni las rutas de almacenamiento.

## Subida (multipart)

- El alta es `multipart/form-data`. Se parsea con `parseMultipartFormDataFirebase`
  (portado de `services/tasks` como `parseMultipartFormData`), que devuelve `{fields, files}`;
  el fichero llega en el campo `file` como `{buffer, filename, mimeType}`.
- **Orden del controlador** (`createDocument`, ver [03_contratos-api.md](../03_contratos-api.md)):
  1. Validar token **antes** de consumir el body multipart.
  2. Parsear multipart y extraer campos.
  3. Validar campos requeridos, scope/type, ack-mode, `visibleToRoles`, `metadata`, `expiresAt`.
  4. Validar el fichero: presente, MIME en allow-list, tamaño ≤ 10 MB — antes de resolver el actor (errores descriptivos tempranos).
  5. Resolver actor + rechazar sin-vínculo.
  6. `canCreate` (reject rápido antes de tocar Firestore).
  7. Existencia de branch/employee (+ responsabilidad activa para tipos no-RRHH).
  8. Crear (upload + doc + índice + actividad + notificaciones).

## Paths por scope (`DocumentStorageService.buildStoragePath`)

El `documentId` se pre-genera (`randomUUID`) para que el path de Storage y el doc de Firestore
compartan ID. `filename` se sanea (`[^a-zA-Z0-9._-] → _`) y se prefija con `Date.now()`:

```
entity   → documents/entities/{entityId}/entity/{documentId}/{ts}-{safeFilename}
branch   → documents/entities/{entityId}/branch/{branchId}/{documentId}/{ts}-{safeFilename}
employee → documents/entities/{entityId}/employee/{employeeId}/{documentId}/{ts}-{safeFilename}
```

## Upload privado

`uploadPrivate(buffer, mimeType, storagePath)` → `bucket.file(path).save(buffer, {contentType,
metadata:{cacheControl:"private, no-store"}})`. El bucket es el por defecto del proyecto
(`getStorage().bucket()`); el servicio necesita el mismo bucket/credenciales que hoy usa la
function (vía `GOOGLE_APPLICATION_CREDENTIALS`).

## Descarga (signed URL)

`generateSignedUrl(storagePath, ttlMinutes=1)` → `bucket.file(path).getSignedUrl({action:"read",
expires})`. **TTL por defecto: 1 minuto.** El endpoint `GET /:id/download` devuelve
`{ url, expiresAt (ISO) }` y registra actividad `download_requested`.

## `storagePath` nunca sale al cliente

Todos los casos de uso que devuelven documentos hacen `Omit<ManagedDocument, "storagePath">`.
El `storagePath` solo se usa internamente para construir la signed URL.

## Criterio de aceptación

- Alta con PDF pequeño (scope branch) → 201; objeto en Storage en el path esperado con
  `cacheControl: private, no-store`.
- Fichero > 10 MB → `400 documents/file_too_large`; MIME fuera de la allow-list → `400 documents/invalid_mime_type`; sin fichero → `400 documents/file_required`.
- `GET /:id/download` → URL válida que expira en ~1 min; descarga real del binario correcto.

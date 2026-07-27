# TDR-003 — Subida de evidencias: Storage y multipart

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 1)
**Componente:** `services/tasks` — `POST /:taskId/resources` y `POST /:taskId/ratings`

---

## Problema

Dos endpoints reciben ficheros: la subida de recursos de tarea (`resources`, foto/vídeo como evidencia) y, opcionalmente, la imagen de una valoración (`ratings`). En Firebase, `tasksHandler` corre con `memory: 512MiB` y parsea el multipart con un helper propio y sube a Firebase Storage vía `StorageService`. Hay que replicar esto en el servidor sin degradar límites ni cambiar las rutas públicas de los ficheros.

---

## Flujo de subida (recursos)

```
POST /api/v1/tasks/:taskId/resources   (multipart/form-data)
  → resolveTaskActor → canOperateAssignedTask
  → parseMultipartFormDataFirebase(req)  → { fields, files[] }
  → validar tipo (photo|video) y tamaño contra task.config.maxPhotoSizeMB / maxVideoSizeMB
  → StorageService.uploadFile({ destination, mimeType, buffer, public: true })  → url pública
  → taskRepository.createResource(entityId, taskId, { type, filename, mimeType, url, storagePath, sizeKB, uploadedBy, employeeId })
  → recordTaskActivity(type: "resource_uploaded")
```

`destination` sigue el mismo convenio de rutas de Storage que hoy, para que las URLs ya emitidas y las nuevas sean homogéneas.

## Puntos técnicos del port

1. **Parser multipart.** Se porta `parseMultipartFormDataFirebase`. En Firebase el `req.rawBody` lo provee el runtime de Functions; en Express se garantiza el buffer crudo (p.ej. no consumir el body con `express.json()` en la ruta multipart, o usar el parser sobre el stream). El `app.ts` monta `express.json()` con límite alto pero las rutas de ficheros usan el parser de multipart, no el JSON.

2. **StorageService.** Se porta `core/shared/firebase/storage`. Usa el bucket del Admin SDK; en el servidor se cablea contra el bucket configurado (`APP_STORAGE_BUCKET`), la misma variable que Firebase.

3. **Límite de payload.** El origen corre a 512MiB de memoria. El contenedor `tasks` debe permitir cuerpos suficientes (límite de body de Express y del `proxy_pass` de nginx — `client_max_body_size` acorde al `maxVideoSizeMB`).

4. **Validación de tamaño/tipo.** Se conserva la validación contra `TaskConfig` (`maxPhotoSizeMB`, `maxVideoSizeMB`, `requireEvidenceOnCompletion`). El `sizeKB` se calcula del buffer.

## Configuración

- `APP_STORAGE_BUCKET` — bucket de Firebase Storage (mismo que Firebase).
- `client_max_body_size` en el `location /api/v1/tasks/` de nginx, dimensionado al vídeo máximo permitido.

## Criterio de éxito

- Subir una foto dentro de límite crea el `TaskResource` con `url` pública accesible y registra actividad `resource_uploaded`.
- Un fichero por encima de `maxVideoSizeMB` se rechaza con error de validación, sin escribir en Storage.
- Las URLs de recursos nuevos tienen el mismo formato que las creadas por Firebase.

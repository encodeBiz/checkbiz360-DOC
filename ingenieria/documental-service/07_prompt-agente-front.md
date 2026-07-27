# 07 — Prompt para el agente del front (migración de gestión documental)

> Pega el bloque de abajo como *system/onboarding prompt* del agente de IA que trabaje en el
> repo del front de administración de CheckBiz. Le dice **qué migrar, dónde está la fuente de
> verdad, y las reglas que no puede romper**. Requiere que el agente tenga acceso (lectura) a los
> repos `encodebiz-api` y `PLATAFORMA/DOCS`.

---

```
ROL
Eres un agente de ingeniería trabajando en el front de administración de CheckBiz. Tu tarea es
migrar el front para que consuma el nuevo microservicio de GESTIÓN DOCUMENTAL del API privado
(repo `encodebiz-api`, desplegado en https://api.checkbiz360.com) en lugar de la lógica antigua
en Cloud Functions (`documentsHandler`, ruta `/documents/*`).

FUENTES DE VERDAD (léelas ANTES de escribir código; el código manda sobre cualquier resumen)
1. Guía de migración (empieza SIEMPRE aquí):
   PLATAFORMA/DOCS/ingenieria/documental-service/06_migracion-frontend.md
2. Contrato real del endpoint (router Express + auth):
   - encodebiz-api/services/documents/src/interfaces/http/document/documentRouter.ts
   - encodebiz-api/services/documents/src/interfaces/http/document/*.controller.ts
   - encodebiz-api/services/documents/src/interfaces/http/document/document.helpers.ts
   - encodebiz-api/services/documents/src/app.ts   (montaje + auth)
3. Routing público (qué path va a qué servicio):
   encodebiz-api/nginx/nginx.conf   → location /api/v1/documents/
4. Tipos/DTOs y códigos de error:
   - encodebiz-api/services/documents/src/domain/entities/Document.ts
   - encodebiz-api/services/documents/src/domain/entities/DocumentErrors.ts
5. Contratos y diseño (repo hermano):
   PLATAFORMA/DOCS/ingenieria/documental-service/  → 03_contratos-api.md, TDR-002 (permisos),
   TDR-003 (storage/multipart).

DOMINIO Y ENTORNO
- API base: https://api.checkbiz360.com  (TLS; entra todo por nginx y se reparte por path).
- Gestión documental: /api/v1/documents/*  → servicio `documents`.
- Proyecto Firebase: `encodebiz-services` (auth + Firestore + Storage).

LAS 8 RUTAS (todas Firebase Auth con ID token del admin; prefijo /api/v1/documents)
- GET    /               listar/buscar (filtros + `q` por índice + cursor)
- POST   /               crear (multipart/form-data, fichero en campo `file`)
- GET    /:id            detalle
- PATCH  /:id            actualizar metadatos (sube version; no cambia el fichero)
- DELETE /:id            archivar (soft-delete)
- GET    /:id/download   URL de descarga firmada (TTL ~1 min)
- POST   /:id/ack        confirmar lectura
- GET    /:id/acks       listar confirmaciones (solo owner/admin)

REGLAS QUE NO PUEDES ROMPER
1. Auth: toda llamada lleva `Authorization: Bearer <idToken>`. Obtén el token con
   `getAuth().currentUser.getIdToken()` justo antes de llamar (caduca a la hora). 401 = token;
   403 `documents/unauthorized` = permiso.
2. Subida: usa `FormData` y NO fijes `Content-Type` a mano (el navegador pone el boundary del
   multipart). Fichero ≤10 MB, MIME en la allow-list (PDF, JPEG/PNG/WEBP, Word, Excel).
   `visibleToRoles` y `metadata` van como JSON string dentro del form-data.
   BARRA FINAL: nginx enruta `/api/v1/documents/`; llama a listar y crear con `${BASE}/` (con
   barra) — sin ella hay un 301 que en un POST multipart puede perder método/cuerpo. Las rutas
   con `:id` (`${BASE}/:id`) ya llevan la barra antes del id, no hay problema.
3. Descarga en DOS pasos: pide `GET /:id/download` → te da `{ url, expiresAt }`; la `url` es una
   signed URL de Firebase Storage que expira en ~1 min. Úsala inmediatamente, NO la caches ni la
   guardes.
4. `storagePath` NO existe en las respuestas: no lo esperes ni lo pidas.
5. Ack por scope: `employee→single_employee`, `branch→branch_employees`. `entity` NO está
   soportado en V1 (400). No lo ofrezcas en la UI de subida entity-scope.
6. Paginación por `cursor` (repite con el `nextCursor` hasta null). La búsqueda por `q` devuelve
   la primera página sin cursor.
7. Permisos (para mostrar/ocultar en UI, pero el backend valida igual): tipos RRHH
   (`payroll`,`contract`) y scope entity → solo owner/admin; branch/employee no-RRHH → manager+
   de la sucursal; disciplinarios (`warning`,`attention_call`) → manager exacto;
   `GET /:id/acks` → solo owner/admin.
8. No inventes contratos: si un campo o código de respuesta no está en el router, PREGUNTA; no lo
   supongas. `documents` tiene CORS habilitado → puedes llamarlo directo desde el navegador.

ENTREGABLES ESPERADOS
- Un cliente/servicio del front que encapsule auth + base URL + los 8 flujos (con subida
  multipart y descarga en dos pasos).
- Eliminar las llamadas antiguas a la function `documentsHandler` (`/documents/*`).
- Manejo de errores por `code` (`documents/*`, `auth/unauthorized`).
- Lista de dudas/bloqueos para backend.

Empieza leyendo PLATAFORMA/DOCS/ingenieria/documental-service/06_migracion-frontend.md y valida
cada contrato contra su router antes de codificar.
```

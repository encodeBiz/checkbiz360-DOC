# 06 — Guía de migración — Front de administración: Gestión Documental → API privado

> **Para:** equipo de front de la administración de CheckBiz.
> **Qué cubre:** cómo migrar el front para consumir el nuevo servicio **documents** del API
> privado (`https://api.checkbiz360.com`) en lugar de la lógica antigua de gestión documental en
> Cloud Functions (`documentsHandler`, ruta `/documents/*`).
> **Fuente de verdad:** el código del router en `encodebiz-api` (ver §9). Este doc resume los
> contratos; si hay discrepancia, manda el router.

---

## 1. Contexto y objetivo

La API de gestión documental **se ha movido de Cloud Functions a un microservicio propio**
(`documents`, puerto 3007) desplegado tras nginx en `https://api.checkbiz360.com`. El front debe
dejar de llamar a la function antigua y pasar al nuevo path. **El contrato no cambia**: mismos
request/response, misma auth; solo cambia el host y el prefijo de ruta.

| Necesidad en el front | Antes (`documentsHandler`) | Ahora (`documents`) |
|---|---|---|
| Listar / buscar documentos | `GET /documents` | `GET /api/v1/documents` |
| Subir documento (fichero) | `POST /documents` | `POST /api/v1/documents` |
| Detalle | `GET /documents/:id` | `GET /api/v1/documents/:id` |
| Actualizar metadatos | `PATCH /documents/:id` | `PATCH /api/v1/documents/:id` |
| Archivar | `DELETE /documents/:id` | `DELETE /api/v1/documents/:id` |
| URL de descarga (firmada) | `GET /documents/:id/download` | `GET /api/v1/documents/:id/download` |
| Confirmar lectura (ack) | `POST /documents/:id/ack` | `POST /api/v1/documents/:id/ack` |
| Listar confirmaciones | `GET /documents/:id/acks` | `GET /api/v1/documents/:id/acks` |

**Regla de migración:** la ruta relativa (`/`, `/:id`, `/:id/download`, …) es idéntica; solo se
antepone `https://api.checkbiz360.com/api/v1/documents`.

## 2. Arquitectura y routing

Todo entra por **nginx** (TLS Let's Encrypt) y se reparte por path. La gestión documental es
`/api/v1/documents/*` → servicio `documents`. **Auth: Firebase ID token** del usuario admin
(proyecto Firebase `encodebiz-services`). No hay `X-Encodebiz-Key` aquí: es superficie de front,
no S2S.

`client_max_body_size` en nginx para esta ruta es **12 MB** (límite de subida 10 MB + margen).

## 3. Autenticación (Firebase ID token)

Toda llamada lleva `Authorization: Bearer <ID_TOKEN>`. Obtén el token justo antes de llamar
(caduca a la hora):

```ts
import { getAuth } from "firebase/auth";
const token = await getAuth().currentUser!.getIdToken();
```

`401 auth/unauthorized` = token ausente/inválido. `403 documents/unauthorized` = el usuario no
tiene permiso sobre ese documento/acción.

## 4. Envoltura de respuesta y errores

- Éxito → `{ ok: true, ... }`.
- Error → `{ code, error }` con `code` del catálogo `documents/*` (ver §8 de
  [03_contratos-api.md](./03_contratos-api.md)).
- `documents` tiene **CORS habilitado** (`app.use(cors())`), así que el front lo llama directo
  desde el navegador.

## 5. Flujos con ejemplos

Base: `const BASE = "https://api.checkbiz360.com/api/v1/documents";`
Helper de auth: `const authHeaders = async () => ({ Authorization: \`Bearer ${await getAuth().currentUser!.getIdToken()}\` });`

> **⚠️ Barra final (importante).** nginx enruta `/api/v1/documents/` (con barra). Una petición a
> `/api/v1/documents` **sin** barra recibe un **301** a la versión con barra. En GET el navegador
> lo sigue solo, pero en un **POST multipart** un 301 puede degradar la petición (perder método o
> cuerpo). Por eso: en **listar** y **crear** usa `${BASE}/`; en las rutas con `:id`
> (`${BASE}/${id}`) ya no hay problema (la barra va antes del id).

### 5.1 Listar / buscar
```ts
const params = new URLSearchParams({ entityId, limit: "20" });
if (branchId) params.set("branchId", branchId);
if (q) params.set("q", q);            // búsqueda por índice (título/desc/tags…)
if (type) params.set("type", type);   // payroll | contract | warning | ...
if (status) params.set("status", status); // active | archived (admin ve ambos)
const res = await fetch(`${BASE}/?${params}`, { headers: await authHeaders() }); // ← barra final
const { documents, nextCursor, total } = await res.json();
// paginar: repetir con params.set("cursor", nextCursor) hasta que sea null
```
- Vista "todo de un empleado": pasa `employeeId` **sin** `scope`.
- La búsqueda `q` devuelve la primera página (sin cursor).

### 5.2 Subir documento (multipart)
```ts
const fd = new FormData();
fd.set("entityId", entityId);
fd.set("scope", "branch");                 // entity | branch | employee
fd.set("type", "policy");
fd.set("title", "Política de vacaciones");
fd.set("branchId", branchId);              // obligatorio si scope=branch|employee
// fd.set("employeeId", employeeId);       // obligatorio si scope=employee
fd.set("visibleToRoles", JSON.stringify(["worker","supervisor","manager"])); // ≥1
// fd.set("requiresAcknowledgement", "true");
// fd.set("acknowledgementMode", "branch_employees"); // acorde al scope
// fd.set("metadata", JSON.stringify({ tags: ["rrhh","2026"] }));
fd.set("file", fileBlob, filename);        // ≤10MB, MIME en la allow-list
const res = await fetch(`${BASE}/`, { method: "POST", headers: await authHeaders(), body: fd }); // ← barra final (evita el 301 en POST)
// NO pongas Content-Type manualmente: el navegador añade el boundary del multipart.
const { document } = await res.json(); // 201; document sin storagePath
```
Reglas de ack por scope: `employee→single_employee`, `branch→branch_employees`. `entity` **no
soportado en V1** (400). MIME permitidos: PDF, JPEG/PNG/WEBP, Word, Excel.

### 5.3 Detalle
```ts
const res = await fetch(`${BASE}/${id}?entityId=${entityId}`, { headers: await authHeaders() });
const { document } = await res.json(); // incluye ackStatus y branch; sin storagePath
```

### 5.4 Actualizar metadatos (JSON, sube `version`)
```ts
await fetch(`${BASE}/${id}`, {
  method: "PATCH",
  headers: { ...(await authHeaders()), "Content-Type": "application/json" },
  body: JSON.stringify({ entityId, title, description, visibleToRoles, expiresAt: null }),
});
```
No cambia el fichero binario. Un documento archivado no se puede editar (403).

### 5.5 Archivar (soft-delete)
```ts
await fetch(`${BASE}/${id}?entityId=${entityId}&archiveReason=${encodeURIComponent(reason)}`,
  { method: "DELETE", headers: await authHeaders() });
// 200 ok; 409 documents/already_archived si ya estaba archivado
```

### 5.6 Descargar (dos pasos: pedir URL firmada → descargar)
```ts
const res = await fetch(`${BASE}/${id}/download?entityId=${entityId}`, { headers: await authHeaders() });
const { url, expiresAt } = await res.json();
window.location.href = url;   // signed URL de Storage, TTL ~1 min: úsala YA, no la caches
```

### 5.7 Confirmar lectura (ack)
```ts
await fetch(`${BASE}/${id}/ack`, {
  method: "POST",
  headers: { ...(await authHeaders()), "Content-Type": "application/json" },
  body: JSON.stringify({ entityId }),
}); // idempotente; 400 si el doc no requiere ack; 403 si no te toca confirmarlo
```
El estado por-usuario viene en `ackStatus` al leer el documento.

### 5.8 Listar confirmaciones (solo owner/admin)
```ts
const res = await fetch(`${BASE}/${id}/acks?entityId=${entityId}`, { headers: await authHeaders() });
const { acks, total } = await res.json(); // 403 si no eres owner/admin
```

## 6. Permisos (qué mostrar/ocultar en la UI)

Resumen (detalle en [TDR-002](./tdr/TDR-002-resolucion-actor-y-matriz-de-permisos.md)):
- Tipos **RRHH** (`payroll`, `contract`) y scope **entity**: crear/editar/archivar solo owner/admin.
- Scope branch/employee no-RRHH: `manager+` de la sucursal. Disciplinarios (`warning`,
  `attention_call`): solo `manager` exacto.
- `GET /:id/acks`: solo owner/admin.
El backend valida siempre; ocultar en UI es cosmético (espera 403 igualmente).

## 7. Checklist de migración (front)

- [ ] Cliente/servicio que encapsule base URL + auth (`getIdToken()` en cada llamada).
- [ ] Reemplazar las llamadas a la function `documentsHandler` (`/documents/*`) por `…/api/v1/documents/*`.
- [ ] Usar **barra final** en listar (`${BASE}/`) y crear (`${BASE}/`) para evitar el 301.
- [ ] Subida: usar `FormData` **sin** fijar `Content-Type` a mano.
- [ ] Descarga en dos pasos; no cachear la signed URL (expira en ~1 min).
- [ ] Paginación por `cursor` hasta `null`; búsqueda por `q` sin cursor.
- [ ] Manejo de errores por `code` (`documents/*`, `auth/unauthorized`).
- [ ] No enviar `storagePath` (no existe en las respuestas).

## 8. Errores comunes (resumen)

| Síntoma | Causa | Fix |
|---|---|---|
| 401 `auth/unauthorized` | token ausente/caducado | `getIdToken()` justo antes de llamar |
| 403 `documents/unauthorized` | sin permiso sobre el doc/acción | revisar rol/nivel; no es bug |
| 400 `documents/invalid_mime_type` / `file_too_large` | fichero fuera de allow-list o >10MB | validar en cliente antes de subir |
| 400 `documents/invalid_acknowledgement_mode` | ack-mode no acorde al scope, o `entity` | `employee→single_employee`, `branch→branch_employees` |
| URL de descarga caducada | signed URL de 1 min cacheada | volver a pedir `/download` |
| POST de subida "se convierte en GET" o pierde el body | 301 por llamar sin barra final | POST a `${BASE}/` (con barra) |

## 9. Fuentes de verdad y dónde buscar

- Router y contrato real: `encodebiz-api/services/documents/src/interfaces/http/document/documentRouter.ts` + los `*.controller.ts` + `document.helpers.ts`.
- Auth y montaje: `encodebiz-api/services/documents/src/app.ts` (mismo `validateToken` + `resolveDocumentActor`).
- Routing público: `encodebiz-api/nginx/nginx.conf` (`location /api/v1/documents/`).
- Tipos/DTOs: `encodebiz-api/services/documents/src/domain/entities/Document.ts` y `DocumentErrors.ts`.
- Contratos resumidos: [03_contratos-api.md](./03_contratos-api.md). Diseño: ADRs/TDRs de esta carpeta.

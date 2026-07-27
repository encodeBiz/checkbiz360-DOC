# TDR-001 — Port del módulo `document` al servicio `documents`

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 2)
**Componente:** `services/documents` — traslado de la carpeta `document` de Functions

---

## Problema

Trasladar el módulo `document` (8 rutas, ~2.160 LOC) desde
`encodeBiz-SAAS/functions/src/services-saas/checkinbiz/…/document` a un microservicio
`services/documents` en `encodebiz-api`, **sin cambiar la lógica ni el contrato**, resolviendo
las rutas de import y las dependencias compartidas.

## Mapa de traslado

| Origen (Functions) | Destino (`services/documents/src/`) |
|---|---|
| `interfaces/http/document/*` (8 controllers + router + helpers) | `interfaces/http/document/*` |
| `application/use-cases/document/*` (8 casos de uso) | `application/use-cases/document/*` |
| `application/services/document/*` (Permission, Storage, searchIndex) | `application/services/document/*` |
| `application/notifications/DocumentNotificationService.ts` | `application/notifications/DocumentNotificationService.ts` |
| `domain/entities/Document.ts`, `DocumentErrors.ts` | `domain/entities/*` |
| `domain/interfaces/DocumentRepository.ts` | `domain/interfaces/*` |
| `infrastructure/repository/FirestoreDocumentRepository.ts` | `infrastructure/repository/*` |
| `core/searchIndex/*` (genérico) | `core/searchIndex/*` (ver [TDR-005](./TDR-005-indice-de-busqueda-documental.md)) |

## Reutilizado de `services/tasks` (copia local, no reimplementar)

- `infrastructure/repository/FirestoreBranchRepository.ts` — incl. `findById`, `findResponsibilities({entityId,branchId}, employeeId?, extraWhere?)`.
- `infrastructure/repository/FirestoreEmployeeRepository.ts` — `findById(id, entityId, "token_devices")`.
- `domain/entities/Employee.ts` (con `ResponsibilityKey`, `ResponsibilityLevel`) y `Branch.ts`.
- `core/shared/utils/validateToken.ts`, `core/shared/utils/parseMultipartFormData.ts`.
- `core/shared/firebase/*` (init admin / storage) según el patrón del servicio.
- `application/notifications/*` — scaffolding `CheckbizNotifier` / `CheckbizSentNotificationApp` / `CheckbizPushMessageFactory` / `messages` (este último **ya trae** `doc_uploaded`/`doc_ack_required`).

## Ajustes de import

Los archivos del módulo referencian rutas profundas de Functions
(`../../../../../core/shared/utils/validateToken`, `../../../../../core/searchIndex/...`). Al
copiar, se reescriben a la ubicación equivalente dentro de `services/documents/src`
(p. ej. `../../../core/shared/utils/validateToken`, `../../../core/searchIndex/...`).
**Ningún cambio de lógica**, solo rutas.

## Wiring del servicio

- `src/app.ts`: `express()` + `cors()` + `express.json({limit:"10mb"})` + `GET /health` (`{ ok:true, service:"documents" }`) + `app.use("/api/v1/documents", documentRouter)` + error handler global de 4 args (igual que el de `documents.ts` en Functions, devolviendo `documents/internal_error`).
- `src/server.ts`: `app.listen(PORT)` con `PORT=3007`.
- `document.helpers.ts`: mantiene las instancias singleton (`documentRepository`, `permissionService`, `branchRepository`, `employeeRepository`, use cases) y las funciones `validateDocumentToken` / `resolveDocumentActor` / `parseDocumentMultipart`.

## Estructura de datos (sin cambios)

`entities/{entityId}/documents/{documentId}` + subcolecciones `acks/{employeeId}` y `activity/{activityId}`; colección raíz `searchIndex`. Ficheros en Storage bajo `documents/entities/{entityId}/…`.

## Criterio de aceptación

- `npm run typecheck` verde en el workspace `documents` y en el monorepo.
- Las 8 rutas devuelven exactamente los status/JSON de [03_contratos-api.md](../03_contratos-api.md).
- `storagePath` nunca aparece en ninguna respuesta.

## Deuda registrada

- `Employee`/`Branch` y las utilidades de auth/multipart/notificaciones quedan **duplicadas** con `tasks`. Unificar en `@encodebiz/shared` es trabajo futuro (ver [ADR-001](../adr/ADR-001-microservicio-documents-dedicado.md)).

# 02 — Arquitectura objetivo (To-Be)

## Principio

> **Solo se mueve quién sirve el HTTP. El dato sigue en Firestore.**

La API documental pasa a ser un microservicio propio en `encodebiz-api`, detrás de nginx, mientras Firestore permanece como fuente de datos y Firebase sigue proveyendo la verificación de ID token y el bucket de Storage.

## Topología destino

```
                    ┌──────────────────────────── encodebiz-api (servidor privado) ────────────────────────────┐
   app móvil  ─┐    │  nginx                                                                                    │
   back office ┼───▶│   location /api/v1/documents/ ─▶ documents_service (documents:3007) ─▶ Firestore (Admin)  │
               │    │   location /api/v1/tasks/    ─▶ tasks:3006                                                 │
               │    │   location /api/reports/     ─▶ reports:3005  · /api/sync/ · /api/analytics/ · /api/v1/... │
               │    └───────────────────────────────────────────────────────────────────────────────────────┘
               │
               └────────────────────── Firebase (se mantiene) ──────────────────────
                        · Auth (Firebase ID token → verifyIdToken)
                        · Storage (bucket: upload privado + signed URL)
                        · (sin triggers ni schedules propios del módulo documental)
```

## El servicio `documents`

Espeja a `tasks`/`reports`/`sync`/`analytics`:

```
services/documents/               puerto 3007
  src/app.ts                      Express: cors + json(10mb) + /health + monta documentRouter en /api/v1/documents
  src/server.ts                   listen(3007); sin PostgreSQL (usa Firestore vía Admin SDK)
  src/interfaces/http/document/   router + 8 controladores + document.helpers  (port de TDR-001)
  src/application/use-cases/document/
  src/application/services/document/     PermissionService, StorageService, documentSearchIndex
  src/application/notifications/         reuso del scaffolding de tasks + DocumentNotificationService
  src/domain/{entities,interfaces}/
  src/infrastructure/repository/         Firestore Document/Branch/Employee
  src/core/searchIndex/                  subsistema de índice (portado)
  src/core/shared/                       validateToken, parseMultipartFormData, storage/admin
  Dockerfile                      copia del de tasks (EXPOSE 3007)
```

Ver el detalle del port en [TDR-001](./tdr/TDR-001-port-modulo-document.md).

## Auth

**Solo Firebase ID token, portado 1:1** (ver [ADR-004](./adr/ADR-004-auth-solo-firebase-token.md) y [TDR-002](./tdr/TDR-002-resolucion-actor-y-matriz-de-permisos.md)):
- **Firebase ID token** → `validateToken` portado tal cual (`verifyIdToken` sin `checkRevoked`). No se usa `requireFirebaseAuth` de shared.
- Resolución del actor: `DocumentPermissionService.resolveActor(uid, entityId)` lee `user_entity_roles` (owner/admin), el empleado activo por `uid`, y sus `employee_responsibilities` por sucursal.
- **No hay staff JWT** (a diferencia de tasks): documental es superficie de back-office/usuario autenticado.

## Datos

Mismo Firestore, mismo `FirestoreDocumentRepository`, mismas rutas `entities/{entityId}/documents/...`, `.../acks`, `.../activity` y la colección raíz `searchIndex`. Mismo bucket de Storage. **Cero migración** (ver [ADR-003](./adr/ADR-003-firestore-fuente-sin-migracion.md)).

## Frontera con Firebase

| Responsabilidad | Dónde queda |
|---|---|
| 8 endpoints HTTP de documental | **Servicio `documents`** (encodebiz-api) |
| Verificación de ID token | Firebase (SDK usado desde el servidor) |
| Storage: upload privado + signed URL | Firebase (bucket, vía Admin SDK desde el servidor) |
| Índice de búsqueda (`searchIndex`) | Firestore — lo mantiene el servicio en cada alta/update/archivado |
| Notificaciones push + in-app | Servicio (vía `@encodebiz/shared` → FCM + colección `notifications`) |
| Fuente de datos (Firestore) | Compartida — el servidor lee y escribe |

> El módulo documental **no** tiene triggers ni schedules propios; no queda nada reactivo en Firebase salvo el `documentsHandler`, que se marca *deprecated* en el cutover.

## Cutover

1. Se despliega `documents` en paralelo; la function `documentsHandler` sigue viva sirviendo `/documents` y `/reports`.
2. Se valida el servicio contra los contratos ([03_contratos-api.md](./03_contratos-api.md)).
3. El front admin y la app apuntan de la URL de `documentsHandler` (parte `/documents`) a `…/api/v1/documents`.
4. La parte `/documents` de `documentsHandler` se marca como *deprecated*; se retira tras un periodo de observación (la parte `/reports` ya está servida por el servicio `reports` desde su propio port).

El corte es reversible en cualquier punto: revertir la URL del cliente devuelve el tráfico a Firebase, sin pérdida de datos (misma Firestore, mismo Storage).

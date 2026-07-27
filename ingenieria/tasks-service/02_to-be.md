# 02 — Arquitectura objetivo (To-Be)

## Principio

> **Solo se mueve quién sirve el HTTP. El dato sigue en Firestore y lo reactivo sigue en Firebase.**

La API de tareas pasa a ser un microservicio propio en `encodebiz-api`, detrás de nginx, mientras Firestore permanece como fuente de datos y los schedules/triggers siguen en Firebase.

## Topología destino

```
                    ┌──────────────────────────── encodebiz-api (servidor privado) ────────────────────────────┐
   app móvil  ─┐    │  nginx                                                                                    │
   back office ┼───▶│   location /api/v1/tasks/  ──▶  tasks_service (tasks:3006)  ──▶  Firestore (Admin SDK)    │
               │    │   location /api/v1/checkinbiz/ ─▶ checkinbiz:3002                                         │
               │    │   location /api/reports/   ──▶  reports:3005   · /api/sync/ · /api/analytics/             │
               │    └───────────────────────────────────────────────────────────────────────────────────────┘
               │
               └────────────────────── Firebase (se mantiene) ──────────────────────
                        · Schedule aviso inicio tardío (findPendingStartNotifications)
                        · Triggers Firestore de tareas (push / side-effects)
                        · Auth (Firebase ID token) · Storage (bucket)
```

## El servicio `tasks`

Espeja a `reports`/`sync`/`analytics`:

```
services/tasks/               puerto 3006
  src/app.ts                  Express: cors + json + /health + monta taskRouter en /api/v1/tasks
  src/server.ts               listen(3006); sin PostgreSQL (usa Firestore vía @encodebiz/shared)
  src/interfaces/http/task/   router + 14 controladores + helpers  (port de TDR-001)
  src/application/use-cases/task/
  src/domain/{entities,interfaces}/
  src/infrastructure/repository/   Firestore Task/Branch/Employee
  Dockerfile                  copia del de reports (EXPOSE 3006)
```

Ver el detalle del port en [TDR-001](./tdr/TDR-001-port-modulo-task.md).

## Auth

Se conserva la doble vía **portada 1:1**, sin cambiar el comportamiento en producción (ver [ADR-004](./adr/ADR-004-auth-dual-conservada.md) y [TDR-002](./tdr/TDR-002-resolucion-actor-y-permisos.md)):
- **Firebase ID token** → `validateToken` portado tal cual (`verifyIdToken` sin `checkRevoked`) + `canWrite`. No se usa `requireFirebaseAuth` de shared.
- **Staff JWT** → `validateTokenJWT` portado (secreto `JWT_2FA_SECRET`).

## Datos

Mismo Firestore, mismo `FirestoreTaskRepository`, misma ruta `entities/{entityId}/tasks/...`. **Cero migración** (ver [ADR-003](./adr/ADR-003-firestore-fuente-sin-migracion-de-datos.md)).

## Frontera con Firebase

| Responsabilidad | Dónde queda |
|---|---|
| 14 endpoints HTTP de tareas | **Servicio `tasks`** (encodebiz-api) |
| Verificación de ID token / Storage / bucket | Firebase (SDK usado desde el servidor) |
| Schedule de aviso de inicio tardío | **Firebase** |
| Triggers Firestore (push, side-effects) | **Firebase** |
| Fuente de datos (Firestore) | Compartida — el servidor escribe, el trigger reacciona |

## Cutover

1. Se despliega `tasks` en paralelo; la function `tasksHandler` sigue viva.
2. Se valida el servicio contra los contratos ([03_contratos-api.md](./03_contratos-api.md)).
3. El front admin y la app apuntan de la URL de `tasksHandler` a `…/api/v1/tasks`.
4. `tasksHandler` se marca como *deprecated*; se retira tras un periodo de observación.

El corte es reversible en cualquier punto: revertir la URL del cliente devuelve el tráfico a Firebase, sin pérdida de datos (misma Firestore).

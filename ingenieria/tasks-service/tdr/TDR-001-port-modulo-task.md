# TDR-001 — Port del módulo `task` al servicio `tasks`

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 1)
**Componente:** `encodebiz-api` — `services/tasks`

---

## Problema

El módulo de tareas vive en `encodeBiz-SAAS/functions/src/services-saas/checkinbiz` con estructura hexagonal. Hay que trasladarlo a `encodebiz-api/services/tasks` conservando su estructura y comportamiento, adaptando solo el arranque (Express standalone en vez de `https.onRequest`) y la inicialización del Admin SDK.

---

## Inventario del origen (lo que se porta)

**Capa HTTP** — `interfaces/http/task/`
- `taskRouter.ts` — 14 rutas (ver [03_contratos-api.md](../03_contratos-api.md)).
- 14 controladores: `createTask`, `findTasks`, `findTaskById`, `findTaskActivity`, `updateTask`, `assignTaskWorkers`, `unassignTaskWorker`, `updateTaskStatus`, `addTaskNote`, `updateTaskNote`, `validateTask`, `rejectTask`, `uploadTaskResource`, `rateTaskWorker`.
- `task.helpers.ts` — wiring de repositorios + casos de uso, `resolveTaskActor`, matriz `can*`, parsers y validadores.

**Casos de uso** — `application/use-cases/task/` (12)
`AddTaskNote`, `AssignTaskWorkers`, `CreateTask`, `FindTaskById`, `FindTasks`, `RateTaskWorker`, `RejectTask`, `UpdateTask`, `UpdateTaskNote`, `UpdateTaskStatus`, `UploadTaskResource`, `ValidateTask`.

**Dominio** — `domain/`
- `entities/Task.ts` — `Task`, `TaskAssignment`, `TaskNote`, `TaskResource`, `TaskValidation`, `TaskRating`, `TaskActivity`, `TaskListFilters`, y los tipos `TaskStatus`/`TaskTimeComplianceStatus`/`TaskPriority`/`TaskActorRole`/`TaskConfig`.
- `interfaces/TaskRepository.ts`.
- Entidades de apoyo: `entities/Branch.ts`, `entities/Employee.ts` (con `ResponsibilityLevel`, `ResponsibilityKey`).

**Infraestructura** — `infrastructure/repository/`
- `FirestoreTaskRepository.ts` — opera sobre `entities/{entityId}/tasks/{taskId}` + subcolecciones.
- `FirestoreBranchRepository.ts`, `FirestoreEmployeeRepository.ts` (los usa `resolveTaskActor` y las validaciones).

**Cola desde `core/*`** (dependencias transversales, pequeñas)
- `core/auth/permissions/canWrite`
- `core/shared/utils/validateToken`, `core/shared/utils/validateTokenStaff`
- `core/shared/firebase/storage` (`StorageService`)
- `core/shared/utils/parseMultipartFormData`
- `core/shared/cors/corsConfig` (`ALLOWED_WEB_ORIGINS`, `webCorsMiddleware`)

---

## Estructura destino

```
services/tasks/
  src/
    app.ts                         ← Express: cors + json + /health + monta taskRouter en /api/v1/tasks
    server.ts                      ← dotenv + listen (PORT 3006); sin checkDbConnection (no usa PostgreSQL)
    interfaces/http/task/          ← router + 14 controladores + helpers (port 1:1)
    application/use-cases/task/    ← 12 casos de uso (port 1:1)
    domain/
      entities/{Task,Branch,Employee}.ts
      interfaces/TaskRepository.ts
    infrastructure/repository/     ← FirestoreTask/Branch/Employee repositories
    auth/                          ← resolveTaskActor deps portadas (canWrite, validateTokenStaff)
    shared/                        ← storage + parseMultipart + corsConfig portados
  Dockerfile                       ← copia de services/reports/Dockerfile (puerto 3006)
  package.json                     ← @encodebiz/tasks; deps: express, cors, express-async-errors, firebase-admin, busboy, jsonwebtoken, @encodebiz/shared
  tsconfig.json
```

## Adaptaciones necesarias (lo que NO es copia literal)

1. **Arranque HTTP.** El origen exporta `https.onRequest({...}, app)`. El destino usa `app.listen(PORT)` en `server.ts`, patrón idéntico a `services/reports/src/server.ts`.

2. **Inicialización Admin SDK.** El origen asume `admin.initializeApp()` en `index.ts` de Functions. El destino usa la instancia de Firestore/Admin que expone `@encodebiz/shared` (`firebase`). `getFirestore()` del repositorio se cablea contra esa instancia.

3. **CORS.** Se porta `ALLOWED_WEB_ORIGINS` y `webCorsMiddleware`, o se mapea al `cors()` que ya usan los otros servicios del monorepo, respetando los orígenes permitidos actuales.

4. **Verificación de ID token.** `validateToken` se porta **1:1** (`admin.auth().verifyIdToken(idToken)`); el único cambio es el tipo `Request` (`firebase-functions/https` → `express`). No se sustituye por `requireFirebaseAuth` de shared para no alterar el comportamiento en producción. Ver [TDR-002](./TDR-002-resolucion-actor-y-permisos.md).

5. **`findPendingStartNotifications`.** Se conserva en la interfaz e implementación del repositorio, pero **no se cablea ninguna ruta** que lo consuma: su cliente es el schedule que se queda en Firebase (ver [ADR-002](../adr/ADR-002-solo-http-lo-reactivo-en-firebase.md)).

6. **Notificaciones push in-line.** Los controladores disparan notificaciones (`taskNotificationService.notify*`) que arrastraban `core/notifications`. El framework genérico se extrajo a `@encodebiz/shared` y las fábricas de mensajes checkbiz/tarea (`TaskNotificationService`, `CheckbizNotifier`, `CheckbizOperationals`, `TaskRecipientResolver`, `Checkbiz*MessageFactory`, `messages`) viven en `src/application/notifications/` consumiendo shared. Ver [ADR-005](../adr/ADR-005-notificaciones-a-shared.md).

## Dependencias npm del servicio

`express`, `cors`, `express-async-errors`, `firebase-admin` (Firestore + Storage + messaging vía Admin SDK), `busboy` (multipart), `jsonwebtoken` (staff JWT), `@encodebiz/shared`.

## Duplicación de dominio aceptada

`Branch` y `Employee` ya existen en `services/checkinbiz`. Para no arriesgar divergencia en esta fase, el servicio `tasks` **trae sus propias copias** del SaaS (las que sus casos de uso esperan). La unificación en `@encodebiz/shared` queda como deuda técnica registrada, fuera del alcance de esta migración.

## Criterio de éxito

- `GET /health` responde `{ ok: true, service: "tasks" }`.
- Las 14 rutas responden con el mismo contrato que `tasksHandler` en Firebase (contrato verificado endpoint a endpoint contra [03_contratos-api.md](../03_contratos-api.md)).
- Compila limpio en el pipeline del monorepo (misma estrategia tsc que el resto de servicios).
- Ningún archivo de Firebase Functions productivo se modifica en esta fase.

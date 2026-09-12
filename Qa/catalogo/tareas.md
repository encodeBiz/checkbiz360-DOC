# Catálogo de casos de uso — servicio `tasks` (prefijo TSK)

> **Verificación (2026-09-11).** Catálogo obtenido por análisis estático del código de los
> servicios, del panel y de la app, cruzado con lo desplegado de verdad en `dev-encodebiz`.
> **Salvo lo que abajo se marque como confirmado, el resto es lectura del código, no
> comprobación contra el entorno.** Los hallazgos de este catálogo que ya se han verificado
> uno a uno están en [hallazgos.md](./hallazgos.md); las sospechas sin verificar se quedan
> como tales y se comprobarán al escribir su prueba. El resultado esperado de cada caso es lo
> que hace el código HOY, no lo que debería hacer.

Inventario estático (2026-09-11) del servicio `services/tasks` del monorepo `encodebiz-api`, rama `develop`, frente a su equivalente en Cloud Functions (`tasksHandler`). Base para las pruebas automáticas de API contra desarrollo. El resultado esperado es lo que hace el código HOY; lo que parece incorrecto va en «Sospechas».

## Abreviaturas de rutas de fichero

- `CT/` = `encodebiz-api/services/tasks/src/interfaces/http/task/`
- `H` = `CT/task.helpers.ts`
- `REPO` = `encodebiz-api/services/tasks/src/infrastructure/repository/FirestoreTaskRepository.ts`
- `CF/` = `encodeBiz-SAAS/functions/src/services-saas/checkinbiz/interfaces/http/task/` (router CF: `CF/taskRouter.ts:19-32`, montado en `/tasks` por `firebase-checkinbiz-http/tasks.ts:9`, exportado en `firebase-checkinbiz-http/index.ts:42`)
- `PSVC` = `encodebiz-front-saas/src/services/checkinbiz/task.service.ts`
- `PDET` = `encodebiz-front-saas/src/app/main/[entityId]/checkinbiz/tasks/[id]/detail/page.controller.tsx`
- `PLIST` = `encodebiz-front-saas/src/app/main/[entityId]/checkinbiz/tasks/page.controller.tsx`
- `ADS` = `checkbiz360/lib/features/task/data/datasources/task_remote_datasource.dart`
- `AREPO` = `checkbiz360/lib/features/task/data/repositories/task_repository_impl.dart`

## Actores adicionales (además del vocabulario común)

- `OP_*` sin sufijo: el trabajador se autentica con **EMP_JWT**, que es lo que hace la app. El `sessionToken` lleva `{employeeId, entityId}`, se firma sin caducidad (`services/checkinbiz/src/interfaces/http/auth/validateEmployee.controller.ts:59-63`, `signOptions = {}`).
- `OP_* (Firebase)`: el mismo trabajador, pero presentando un ID token de Firebase de un usuario cuyo `uid` figura en su ficha de empleado.
- `PROP+EMP` / `ADMIN+EMP`: PROP o ADMIN que además tiene ficha de empleado en la entidad (`employees.uid` = su uid).
- `S2S(actorUid=X)`: llamada con `x-encodebiz-key` a la ruta de sistema. El actor efectivo es el usuario X que viene en el body.

## Convenciones para las pruebas

- **Base de desarrollo**: `http://141.95.47.135:8080`. nginx de desarrollo sirve tanto `location = /api/v1/tasks` como `location /api/v1/tasks/` hacia `tasks:3006` (`nginx/nginx.staging.conf:82-85` y `:118-121`), las dos con `client_max_body_size 30m`. Por encima de 30 MB, nginx responde 413 antes de llegar al servicio.
- **Error estándar** del servicio: `{code, error}`. `error` es un **array** en los errores de configuración (`CT/createTask.controller.ts:30`, `CT/updateTask.controller.ts:56`, `CT/duplicateTask.controller.ts:49`).
- **Jornada abierta** del empleado. El último `checklog` con `type == "checkin"` debe cumplir tres cosas: `status == "valid"`, `closed !== true`, y `deadline` ausente o futuro (`packages/shared/src/checkbiz/repositories/FirestoreWorkSessionRepository.ts:43-75`).
- **Orden de comprobaciones**. Casi todas las rutas validan el body y **cargan la tarea antes de autenticar**. Por eso ANON puede recibir 400 o 404 antes que 401; los casos lo reflejan.
- **Panel**. El navegador llama a `/api/proxy/checkinbiz_tasks_handler/...` (`PSVC:22`). El proxy de Next exige y verifica el ID token de Firebase: sin él, o si no es válido, responde **403 `auth/forbidden`** sin llegar al contenedor (`encodebiz-front-saas/src/lib/http/serverBackendProxy.ts:462-463` y `:570-581`). Después reenvía `Authorization`, añade la barra final a `/api/v1/tasks` (`:513-516`) y no sigue redirecciones (`:613`). La URL de desarrollo es `NEXT_BACKEND_URI_CHECKINBIZ_TASKS_HANDLER=http://141.95.47.135:8080/api/v1/tasks` (`encodebiz-front-saas/.env.development:101`). Los casos de este catálogo se lanzan contra nginx directamente.
- **Lecturas de los clientes**. El panel lee tareas y subcolecciones **directamente de Firestore** (`PSVC:60-151`), y la app también (`AREPO:29,73`). Ningún cliente consume por HTTP las rutas GET del servicio.
- **`workSite` sin llamar a Google**. Mandar solo `{geo:{lat,lng}, radiusMeters}` no pasa por `placeDetails` ni `geocodeAddress` (`H:398-436`), así que no genera llamadas facturadas. Con `placeId` o `street` sin `geo` sí se llama a Google.

## Resolución del actor (`H:149-210`)

1. Primero se intenta `validateToken`, que verifica un ID token de Firebase (`packages/shared/src/checkbiz/auth/validateToken.ts:5-21`).
   - `isEntityWriter` = `user_entity_roles/{uid}_{entityId}.role` ∈ {owner, admin} (`packages/shared/src/checkbiz/auth/canWrite.ts:17-21`).
   - Se buscan las fichas de empleado del usuario en esa entidad (`H:153`) y sus responsabilidades activas en `branchId` (`active == 1`, `scope.branchId`). Si no hay `branchId`, entran **todas las sucursales**.
   - Si no es writer ni tiene responsabilidad → **403 `task/unauthorized`** (`H:169-171`).
   - `role` = responsabilidad más alta; si no hay, el rol de entidad (`owner`/`admin`) (`H:175,183`).
   - `level` = max(nivel de la responsabilidad, 4 si es writer) (`H:184`).
   - `employeeId` = ficha de la responsabilidad más alta o, en su defecto, la primera ficha (`H:177,181`).
2. Si **cualquier cosa** lanza dentro de ese `try` (sin cabecera, token no Firebase, error de Firestore), se pasa a `validateTokenJWT`, que verifica con `JWT_2FA_SECRET` (`packages/shared/src/checkbiz/auth/validateTokenStaff.ts:29-50`).
   - Sin cabecera → **401 `auth/unauthorized`** «Token required».
   - Firma, formato o emisor malos → **401 `auth/unauthorized`** «Invalid or expired token».
   - Sin `employeeId`, o `entityId` del token ≠ `entityId` pedido → **403 `task/unauthorized`** (`H:191-194`).
   - Ficha inexistente en la entidad → **404 `task/employee_not_found`** (`H:195-199`).
   - `level` = responsabilidad más alta en la sucursal; si no tiene ninguna, **worker (1) por defecto** (`H:200-207`). `isEntityWriter = false`.
   - **No se mira `employee.status`**.
3. **Jornada abierta obligatoria** para quien tiene `employeeId` y no es writer (`H:499-501`). Solo se aplica a iniciar, completar y reanudar.
4. Niveles: worker 1, supervisor 2, manager 3, owner 4 (`packages/shared/src/checkbiz/entities/Employee.ts:77-82`).

## Matriz de permisos (`H:212-238`)

| Función | PROP / ADMIN | OP_OWNER | OP_MANAGER | OP_SUPERVISOR | OP_WORKER asignado | OP_WORKER no asignado | OP_OTRA_SUCURSAL (JWT) | OP_OTRA_SUCURSAL (Firebase) | AJENO | EMP_INACTIVO |
|---|---|---|---|---|---|---|---|---|---|---|
| `canManageTask` (`H:212-214`) | sí | sí | sí | solo si `allowSupervisorCreation` | no | no | no (nivel 1) | 403 al resolver | 403 al resolver | lo que diga su nivel (el estado no se mira) |
| `canAssignTaskWorkers` (`H:216-218`) | sí | sí | sí | sí (sin interruptor) | no | no | no | 403 al resolver | 403 | ídem |
| `canValidateOrRejectTask` (`H:220-222`) | sí | sí | sí | solo si `allowSupervisorValidation` | no | no | no | 403 | 403 | ídem |
| `canRateTask` (`H:224-226`) | sí | sí | sí | solo si `allowSupervisorRating` | no | no | no | 403 | 403 | ídem |
| `canViewTask` / `canOperateAssignedTask` / `canAddTaskNote` (`H:228-238`) | sí | sí | sí | sí, aunque no esté asignado | sí | no | solo si figura en `assignedEmployeeIds` | 403 | 403 | ídem |

## Interruptores de `TaskConfig` (`H:325-343`)

- **`allowSupervisorCreation`**, vía `canManageTask`. Se evalúa sobre la config enviada en el body en `POST /` y `POST /system`, sobre la del original en `duplicate`, y sobre la de la tarea en `PATCH /:taskId`, en `PATCH /status` a `cancelled`/`assigned`/`draft` y en `PATCH /notes/:noteId`.
- **`allowSupervisorValidation`**: `POST /validation` y `POST /rejection`.
- **`allowSupervisorRating`**: `POST /ratings`.
- **`completionPolicy`**: se normaliza y se guarda (`H:334`) y **ningún controlador lo lee**. Solo aparece en `domain/entities/Task.ts:29` y `H:334`.
- **`requireEvidenceOnCompletion`**: `PATCH /status` → `completed` exige al menos un recurso (`CT/updateTaskStatus.controller.ts:111-116`).
- **`notifyIfNotStarted`**: calcula `scheduledStartNotificationAt` = `scheduledStartAt` + 15 min (`H:351-356`) en alta, edición, duplicado y sistema. El aviso lo envía la CF `taskStartDelayNotifier` (`encodeBiz-SAAS/.../firebase-checkinbiz-http/task-start-delay.ts`), no este servicio.
- **`maxPhotoSizeMB` / `maxVideoSizeMB`**: por defecto 5 y 25; deben ser finitos y > 0, o 400 (`H:337-341`). Limitan las evidencias (`CT/uploadTaskResource.controller.ts:41-44`) y la imagen de la valoración, que usa `maxPhotoSizeMB` (`CT/rateTaskWorker.controller.ts:51-53`).
- **Normalización**: `Boolean(x)`, así que la cadena `"false"` cuenta como verdadero. Una config ausente en `PATCH` no se toca; una presente **reemplaza la config entera** (`CT/updateTask.controller.ts:53-58`).

## Máquina de estados

Estados: `draft`, `assigned`, `in_progress`, `completed`, `validated`, `rejected`, `cancelled` (`domain/entities/Task.ts:1-8`). La pausa **no es un estado**: es `in_progress` con `pausedAt` (`Task.ts:139-152`).

| Acción | Desde | Hacia | Permiso | Precondiciones / efectos | Rechazos |
|---|---|---|---|---|---|
| `POST /` | — | `draft` si no hay asignados; `assigned` si los hay | `canManageTask` (config del body) | sucursal activa, empleados asignables | 400/403/404 |
| `POST /system` | — | `assigned` si ≥1 asignable; si no, `draft` | `canManageTask` del actorUid | idempotente por `externalRef` | 401/400/403/404 |
| `POST /duplicate` | original en cualquier estado | `draft`, sin asignados | `canManageTask` (config del original) | — | 400/403/404 |
| `POST /assignments` | `draft` → `assigned`; los demás estados no cambian | igual | `canAssignTaskWorkers` | — | 400/403/404 |
| `DELETE /assignments/:e` | `assigned` → `draft` si se queda vacía; los demás no cambian | igual | `canAssignTaskWorkers` | — | 403/404 |
| `PATCH /status` `in_progress` | **cualquiera**, sin comprobar el origen | `in_progress` | `canOperateAssignedTask` | jornada (empleado no writer); `geo` si hay `workSite`, **bloquea** fuera de la valla | 403, 400 `no_open_session`/`geo_required`/`out_of_worksite` |
| `PATCH /status` `completed` | **cualquiera** | `completed` | `canOperateAssignedTask` | jornada; `geo` si hay `workSite` (**solo mide**); evidencia si se exige; **cierra la pausa** (`completed`) | 403, 400 `no_open_session`/`geo_required`/`evidence_required` |
| `PATCH /status` `cancelled` | **cualquiera** | `cancelled` | `canManageTask` | cierra la pausa (`cancelled`) | 403 |
| `PATCH /status` `assigned` | **cualquiera** | `assigned` | `canManageTask` | ≥1 asignado; borra `started`/`completed`/`cancelled*` pero **no** `validated*`/`rejected*`; cierra la pausa (`reset`) y pone los contadores a 0 | 403, 400 |
| `PATCH /status` `draft` | **cualquiera** | `draft` | `canManageTask` | borra todos los sellos; contadores a 0; no toca `assignedEmployeeIds` | 403 |
| `PATCH /status` `validated`/`rejected`/otro | — | — | se resuelve el actor antes | — | 400 `task/bad_request` «Unsupported status transition» |
| `POST /validation` | **solo** `completed` | `validated` | `canValidateOrRejectTask` | no toca pausas | 400 `task/invalid_status` (**antes de autenticar**) |
| `POST /rejection` | **cualquiera** | `rejected` (+ `timeComplianceStatus: rejected`) | `canValidateOrRejectTask` | **no cierra la pausa** | 403 |
| `POST /pause` | `in_progress` sin pausa, comprobado en transacción | `in_progress` + `pausedAt` | `canOperateAssignedTask` | sin jornada ni geocerca | 400 `not_in_progress`/`already_paused` |
| `POST /resume` | con `pausedAt`, **en cualquier estado** | quita `pausedAt` y suma `pausedMs` | `canOperateAssignedTask` | jornada + geocerca (bloquea) | 400 `not_paused`/`no_open_session`/`geo_required`/`out_of_worksite` |

`timeComplianceStatus` según el momento:
- Creación y reapertura: `not_started`.
- Inicio: `on_time` u `overdue` según `dueAt` (`CT/updateTaskStatus.controller.ts:106`).
- Completar: `completed_on_time` o `completed_late` (`H:248-250`).
- Rechazo: `rejected`.
- Este servicio nunca escribe `at_risk`.

---

## GET /api/v1/tasks/  ·  TSK-01
- Servicio: tasks, `taskRouter.ts:22` → `CT/findTasks.controller.ts:5-20`. También responde `GET /api/v1/tasks` sin barra (nginx, location exacta).
- Consumidores: ninguno detectado. El panel lista desde Firestore (`PSVC:60-71`) y la app también (`AREPO:29`); `ADS:144-171` existe, pero no se usa.
- Origen: portado desde la CF `CF/findTasks.controller.ts`.
- Diferencias con la CF: ninguna visible (solo cambia un import).
- Autenticación: `resolveTaskActor` (Firebase → JWT de empleado) con el `branchId` de la query, o sin sucursal si no viene.
- Autorización: cualquier actor resuelto. Si `!isEntityWriter && level < supervisor`, se fuerza `employeeId = actor.employeeId` (`CT/findTasks.controller.ts:14-16`). Sin `branchId`, el nivel se calcula sobre las responsabilidades de **todas** las sucursales (`H:157`).
- Entrada: query `entityId`, obligatorio (se acepta también en el body, `H:314`). Opcionales: `branchId`, `status`, `timeComplianceStatus`, `employeeId`, `from` y `to` (una fecha inválida se ignora, `H:307-311`) y `limit` (100 por defecto, `REPO:141`).
- Respuesta correcta: 200, array de `Task` sin envoltura, ordenado por `dueAt` ascendente (`REPO:134-143`).
- Efectos: ninguno.
- Criticidad: baja — ningún cliente la usa hoy, pero expone el listado de la entidad.
- Casos:
  - TSK-01-01 · ANON · sin `entityId` → 400 `task/bad_request`
  - TSK-01-02 · ANON · con `entityId` → 401 `auth/unauthorized` («Token required»)
  - TSK-01-03 · TOKEN_INVALIDO · con `entityId` → 401 `auth/unauthorized` («Invalid or expired token»)
  - TSK-01-04 · PROP · `entityId` propio → 200, todas las tareas de la entidad (≤100)
  - TSK-01-05 · ADMIN · `branchId=B` → 200, solo tareas de B
  - TSK-01-06 · PROP · `status=in_progress` → 200, filtradas. Requiere un índice compuesto con `orderBy dueAt`: sin confirmar que exista, y si falta → 500 `internal_error`
  - TSK-01-07 · PROP · `employeeId=E` → 200, tareas con E en `assignedEmployeeIds`
  - TSK-01-08 · PROP · `from`/`to` válidos → 200, `dueAt` en el rango; `from=basura` → 200, filtro ignorado
  - TSK-01-09 · PROP · `limit=5` → 200, ≤5 elementos; `limit=abc` → sin confirmar (`limit(NaN)` en Firestore, probablemente 500)
  - TSK-01-10 · OP_SUPERVISOR · `branchId` de su sucursal → 200, todas las tareas de la sucursal, sin filtro por empleado
  - TSK-01-11 · OP_SUPERVISOR · sin `branchId` → 200, **todas las tareas de todas las sucursales** de la entidad
  - TSK-01-12 · OP_MANAGER / OP_OWNER · `branchId` → 200, todas las de la sucursal
  - TSK-01-13 · OP_WORKER · `branchId` y `employeeId=OTRO` → 200, solo las suyas (su `employeeId` sobrescribe el filtro)
  - TSK-01-14 · OP_OTRA_SUCURSAL (JWT) · `branchId` de la otra sucursal → 200, solo tareas en las que figure (normalmente `[]`)
  - TSK-01-15 · OP_OTRA_SUCURSAL (Firebase) · `branchId` de la otra sucursal → 403 `task/unauthorized`
  - TSK-01-16 · AJENO (Firebase) · `entityId` de otra entidad → 403 `task/unauthorized`
  - TSK-01-17 · AJENO (EMP_JWT de otra entidad) · `entityId` ajeno → 403 `task/unauthorized`
  - TSK-01-18 · EMP_JWT · ficha borrada de la entidad → 404 `task/employee_not_found`
  - TSK-01-19 · EMP_INACTIVO (`status: "fired"`) · token vigente → 200, igual que un activo
  - TSK-01-20 · PROP · `GET /api/v1/tasks` sin barra final → 200, mismo resultado
- Sospechas:
  - Un supervisor de una sola sucursal que no manda `branchId` obtiene nivel 2 y lista las tareas de toda la entidad: títulos, descripciones y direcciones de `workSite` (`CT/findTasks.controller.ts:11-16` y `H:157`).
  - Ante el 403 de `H:170`, `resolveTaskActor` devuelve el objeto `Response`, no `null`. El controlador sigue: con `level` indefinido el filtro de `:14` resulta falso y la consulta se ejecuta. El cliente recibe 403, pero el segundo `res.json` lanza `ERR_HTTP_HEADERS_SENT` en el log. Afecta a todas las rutas.
  - EMP_INACTIVO conserva el acceso: el token no caduca y `H:195-208` no mira `employee.status`.

## POST /api/v1/tasks/  ·  TSK-02
- Servicio: tasks, `taskRouter.ts:23` → `CT/createTask.controller.ts:22-149`.
- Consumidores:
  - panel: `NEXT_BACKEND_URI_CHECKINBIZ_TASKS_HANDLER`, `PSVC:153-161`, llamado desde `PLIST:226`
  - app: `AppConstants.taskCollectionEndpoint`, `ADS:194-210` y `AREPO:96`
- Origen: portado desde la CF `CF/createTask.controller.ts`.
- Diferencias con la CF:
  - `workSite` es nuevo, con dos errores que la CF no tiene: 400 `task/worksite_invalid` y `task/worksite_imprecise`.
  - Emite los eventos `task.created` y `task.assigned`.
  - La actividad lleva `actorRole: "admin"` para ADMIN; la CF ponía `"owner"` (`CF/task.helpers.ts:128`).
- Autenticación: `resolveTaskActor` con el `branchId` del body.
- Autorización: `canManageTask(actor, config del body)` (`CT/createTask.controller.ts:37`).
- Entrada:
  - Obligatorios: `entityId`, `branchId`, `title`, `dueAt` (`:24`) y `config`, que debe ser un objeto (`H:327-329`).
  - Opcionales: `description`, `scheduledStartAt`, `priority` (un valor fuera de low/medium/high/critical se descarta en silencio, `H:345-348`), `assignedEmployeeIds` (cada uno activo y con responsabilidad activa en la sucursal, `H:264-278`) y `workSite` (`H:378-460`).
  - Orden de las comprobaciones: campos → config → actor → permiso → sucursal → fechas → `workSite` → empleados.
- Respuesta correcta: 201, el documento `Task` (no `TaskDetail`) (`:147-148`).
- Efectos:
  - Escribe `entities/{e}/tasks/{id}`, `assignments/{employeeId}` con `status: "assigned"` y la actividad `created` (más `assigned` si hay asignados).
  - Notifica `task_created`/`task_assigned` a los asignados, por push e in-app, sin esperar (`:135-138`).
  - Emite los eventos `task.created`/`task.assigned`.
  - Dispara el trigger CF `onWriteTaskForPattern` (`firebase-firestore-trigger/onWriteTaskForPattern.ts:151`).
- Criticidad: alta — es el alta de trabajo, desde el panel y desde la app.
- Casos:
  - TSK-02-01 · ANON · falta `title` → 400 `task/bad_request`
  - TSK-02-02 · ANON · sin `config` → 400 `task/bad_request`, `error: ["config is required"]`
  - TSK-02-03 · ANON · body completo → 401 `auth/unauthorized`
  - TSK-02-04 · TOKEN_INVALIDO · body completo → 401 `auth/unauthorized`
  - TSK-02-05 · PROP · body mínimo sin asignados → 201. `status: draft`, `timeComplianceStatus: not_started`, sin `priority`, config normalizada (5/25 MB, `any_assigned_worker`)
  - TSK-02-06 · ADMIN · 2 asignados válidos → 201, `status: assigned`. Dos `assignments`, actividad `created` + `assigned`, `actorRole: "admin"`
  - TSK-02-07 · OP_MANAGER / OP_OWNER · body válido → 201
  - TSK-02-08 · OP_SUPERVISOR · `config.allowSupervisorCreation=true` → 201
  - TSK-02-09 · OP_SUPERVISOR · `allowSupervisorCreation=false` → 403 `task/unauthorized`
  - TSK-02-10 · OP_WORKER · `allowSupervisorCreation=true` → 403 `task/unauthorized`
  - TSK-02-11 · OP_OTRA_SUCURSAL (JWT) · `branchId` ajeno a sus responsabilidades → 403 `task/unauthorized` (nivel 1)
  - TSK-02-12 · OP_OTRA_SUCURSAL (Firebase) → 403 `task/unauthorized` al resolver
  - TSK-02-13 · AJENO · `entityId` de otra entidad → 403 `task/unauthorized`
  - TSK-02-14 · PROP · `branchId` inexistente → 404 `task/branch_not_found`
  - TSK-02-15 · PROP · sucursal con `status != active` → 400 `task/branch_inactive`
  - TSK-02-16 · PROP · `dueAt: "no-fecha"` → 400 `task/bad_request` («dueAt must be a valid date»)
  - TSK-02-17 · PROP · `scheduledStartAt` inválido → 400 `task/bad_request`
  - TSK-02-18 · PROP · `config.maxPhotoSizeMB=0` → 400 `task/bad_request`, `error` es un array con «must be a positive number»
  - TSK-02-19 · PROP · `config: "texto"` → 400 `task/bad_request`, `["config is required"]`
  - TSK-02-20 · PROP · `config: {}` → 201, con todos los interruptores a `false`
  - TSK-02-21 · PROP · `completionPolicy: "all_assigned_workers"` → 201, se guarda; con `"otra"` → se guarda `any_assigned_worker`
  - TSK-02-22 · PROP · `notifyIfNotStarted=true` y `scheduledStartAt` → 201, `scheduledStartNotificationAt` = `scheduledStartAt` + 15 min; sin `scheduledStartAt` → campo ausente
  - TSK-02-23 · PROP · `priority: "urgent"` → 201, sin `priority`
  - TSK-02-24 · PROP · asignado con `status: inactive` → 400 `task/invalid_employees`, `invalidEmployees: [id]`
  - TSK-02-25 · PROP · asignado sin responsabilidad en la sucursal → 400 `task/invalid_employees`
  - TSK-02-26 · PROP · asignado inexistente → 400 `task/invalid_employees`
  - TSK-02-27 · PROP · `workSite: {geo:{lat:40.4,lng:-3.7}}` sin radio → 201, `radiusMeters` = `ratioChecklog` de la sucursal, o 150
  - TSK-02-28 · PROP · `workSite` con `radiusMeters: -5` → 400 `task/worksite_invalid`
  - TSK-02-29 · PROP · `workSite.geo: {lat:200,lng:0}` → 400 `task/worksite_invalid` («out of range»)
  - TSK-02-30 · PROP · `workSite: "texto"` → 400 `task/worksite_invalid`
  - TSK-02-31 · PROP · `workSite: {street:"Madrid"}` (precisión `approximate`) → 400 `task/worksite_imprecise` (llama a Google)
  - TSK-02-32 · PROP · `workSite: {}` → 400 `task/worksite_invalid` («needs a placeId, a street or a geo point»)
  - TSK-02-33 · PROP · `assignedEmployeeIds: [A, A]` → 201, se guarda `[A, A]` sin deduplicar
  - TSK-02-34 · OP_SUPERVISOR · EMP_JWT de otra entidad → 403 `task/unauthorized`
- Sospechas:
  - `allowSupervisorCreation` se evalúa sobre la config que manda el propio creador (`CT/createTask.controller.ts:28-39`): un OP_SUPERVISOR se concede a sí mismo el alta enviando `true`.
  - `assignedEmployeeIds` no se valida como array ni se deduplica (`:23,67,83`); en `POST /assignments` sí se deduplica.
  - Una `priority` inválida se descarta sin error (`H:345-348`) y en `PATCH` da 400: incoherencia.

## GET /api/v1/tasks/:taskId  ·  TSK-03
- Servicio: tasks, `taskRouter.ts:24` → `CT/findTaskById.controller.ts:4-23`.
- Consumidores: ninguno detectado. El panel compone el detalle desde Firestore (`PSVC:139-151`) y la app también (`AREPO:73`); `ADS:174-191` no se usa.
- Origen: portado desde la CF `CF/findTaskById.controller.ts`.
- Diferencias con la CF: ninguna visible en el controlador. El cuerpo trae campos nuevos (`workSite`, `pausedAt`, `pausedBy`, `pauseId`, `pausedMs`, `pauseCount`) y roles `"admin"`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canViewTask` (`H:228-230`).
- Entrada: `taskId` en la ruta y `entityId` en la query (o en el body).
- Respuesta correcta: 200 `{task, assignments, notes, resources, ratings, activity, validations}` (`H:81-93`):
  - `assignments` incluye las `removed`
  - `activity` trae las 50 más recientes (`REPO:225`)
- Efectos: ninguno.
- Criticidad: baja — sin consumidores HTTP.
- Casos:
  - TSK-03-01 · ANON · sin `entityId` → 400 `task/bad_request`
  - TSK-03-02 · ANON · tarea inexistente → 404 `task/not_found` (antes de autenticar)
  - TSK-03-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-03-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-03-05 · PROP → 200 `TaskDetail`
  - TSK-03-06 · ADMIN → 200
  - TSK-03-07 · OP_OWNER / OP_MANAGER → 200
  - TSK-03-08 · OP_SUPERVISOR · no asignado → 200
  - TSK-03-09 · OP_WORKER · asignado → 200, con las valoraciones y validaciones de todos
  - TSK-03-10 · OP_WORKER · no asignado → 403 `task/unauthorized`
  - TSK-03-11 · OP_WORKER · desasignado (`removed`) → 403 `task/unauthorized`
  - TSK-03-12 · OP_OTRA_SUCURSAL (JWT) · no figura → 403 `task/unauthorized`
  - TSK-03-13 · OP_OTRA_SUCURSAL (Firebase) → 403 `task/unauthorized`
  - TSK-03-14 · AJENO · con el `entityId` de la víctima → 403 `task/unauthorized`
  - TSK-03-15 · AJENO · con su propio `entityId` y el `taskId` de la víctima → 404 `task/not_found`
  - TSK-03-16 · EMP_JWT · ficha borrada → 404 `task/employee_not_found`
  - TSK-03-17 · EMP_INACTIVO · asignado → 200
- Sospechas: el 404 llega antes de autenticar (`:11-17`), así que ANON con un `entityId` conocido puede distinguir tareas que existen (401) de las que no (404). Riesgo bajo, porque los ids son aleatorios.

## GET /api/v1/tasks/:taskId/activity  ·  TSK-04
- Servicio: tasks, `taskRouter.ts:25` → `CT/findTaskActivity.controller.ts:4-24`.
- Consumidores: ninguno detectado; el panel la lee de Firestore (`PSVC:129-137`).
- Origen: portado desde la CF `CF/findTaskActivity.controller.ts`.
- Diferencias con la CF: ninguna visible. Aparecen tipos de actividad nuevos: `start_rejected`, `paused`, `resumed`, `resume_rejected`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canViewTask`.
- Entrada: `taskId` en la ruta y `entityId` en la query.
- Respuesta correcta: 200, array de `TaskActivity` con las 100 más recientes, en orden descendente (`:22`).
- Efectos: ninguno.
- Criticidad: baja.
- Casos:
  - TSK-04-01 · ANON · sin `entityId` → 400 `task/bad_request`
  - TSK-04-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-04-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-04-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-04-05 · PROP → 200, ≤100 elementos, descendente
  - TSK-04-06 · OP_SUPERVISOR · no asignado → 200
  - TSK-04-07 · OP_WORKER · asignado → 200
  - TSK-04-08 · OP_WORKER · no asignado → 403 `task/unauthorized`
  - TSK-04-09 · AJENO → 403 `task/unauthorized`
  - TSK-04-10 · PROP · tras un inicio rechazado por la valla → 200, incluye `type: "start_rejected"` con `geo`, `distanceMeters` y `withinWorkSite: false`
- Sospechas: las mismas que en TSK-03 (404 antes de autenticar).

## PATCH /api/v1/tasks/:taskId  ·  TSK-05
- Servicio: tasks, `taskRouter.ts:26` → `CT/updateTask.controller.ts:7-113`.
- Consumidores:
  - panel: `PSVC:163-171`, llamado desde `PDET:181`. El panel manda el cambio de estado aparte, por `/status` (`PDET:179,191-193`).
  - app: `AppConstants.taskEndpoint`, `ADS:213-230` y `AREPO:109`.
- Origen: portado desde la CF `CF/updateTask.controller.ts`.
- Diferencias con la CF:
  - `workSite` es nuevo: `null` lo borra; un valor inválido da 400 `task/worksite_invalid` o `task/worksite_imprecise`.
  - Emite el evento `task.updated`.
  - `FieldValue.delete()` ahora borra de verdad. El `stripUndefined` de la CF no protege los centinelas (`encodeBiz-SAAS/.../infrastructure/repository/FirestoreTaskRepository.ts:32`, sin `instanceof FieldValue`), así que allí `scheduledStartNotifiedAt` quedaba como `{}` (`REPO:38-42`).
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canManageTask(actor, task.config)` (`:21`).
- Entrada:
  - Obligatorios: `taskId` y `entityId`.
  - Opcionales:
    - `title`, `description`, `dueAt`
    - `scheduledStartAt` (`null` o `""` intentan vaciarlo)
    - `priority` (un valor inválido da 400)
    - `config` (reemplaza la config entera)
    - `workSite` (`null` lo borra)
- Respuesta correcta: 200, el documento `Task` actualizado.
- Efectos:
  - `set` con merge sobre la tarea.
  - Recalcula `scheduledStartNotificationAt` y borra `scheduledStartNotifiedAt` (`:77-93`).
  - Actividad `updated`, cuya `metadata` es la lista de claves.
  - Notificación `task_updated` a los asignados.
  - Evento `task.updated`.
- Criticidad: media — edición desde el panel y desde la app.
- Casos:
  - TSK-05-01 · ANON · sin `entityId` → 400 `task/bad_request`
  - TSK-05-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-05-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-05-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-05-05 · PROP · `title` nuevo → 200 con el título cambiado; actividad `updated`
  - TSK-05-06 · ADMIN · `description` → 200
  - TSK-05-07 · OP_MANAGER / OP_OWNER · cambio válido → 200
  - TSK-05-08 · OP_SUPERVISOR · `task.config.allowSupervisorCreation=true` → 200
  - TSK-05-09 · OP_SUPERVISOR · `allowSupervisorCreation=false` → 403 `task/unauthorized`
  - TSK-05-10 · OP_WORKER · asignado → 403 `task/unauthorized`
  - TSK-05-11 · AJENO → 403 `task/unauthorized`
  - TSK-05-12 · PROP · `dueAt` inválido → 400 `task/bad_request`
  - TSK-05-13 · PROP · `scheduledStartAt` inválido → 400 `task/bad_request`
  - TSK-05-14 · PROP · `priority: "urgent"` → 400 `task/bad_request` («priority is invalid»)
  - TSK-05-15 · PROP · `config.maxVideoSizeMB: -1` → 400 `task/bad_request`, `error` es un array
  - TSK-05-16 · PROP · `config` parcial `{allowSupervisorRating:true}` → 200. Los demás interruptores vuelven a `false`, `completionPolicy` a `any_assigned_worker` y los límites a 5/25 MB
  - TSK-05-17 · PROP · `title: ""` → 200, se guarda el título vacío
  - TSK-05-18 · PROP · `scheduledStartAt: null` → 200, pero `scheduledStartAt` **no se borra**
  - TSK-05-19 · PROP · `notifyIfNotStarted=true` y `scheduledStartAt` → 200, `scheduledStartNotificationAt` = +15 min y `scheduledStartNotifiedAt` borrado
  - TSK-05-20 · PROP · `config` con `notifyIfNotStarted=false` → 200, se borran los dos campos de aviso
  - TSK-05-21 · PROP · `workSite: {geo:{lat,lng}}` → 200, radio de la sucursal o 150
  - TSK-05-22 · PROP · `workSite: null` → 200, `workSite` desaparece del documento
  - TSK-05-23 · PROP · `workSite` inválido → 400 `task/worksite_invalid`
  - TSK-05-24 · PROP · tarea en `validated` o `cancelled` → 200 (no hay restricción de estado)
  - TSK-05-25 · OP_SUPERVISOR · con `allowSupervisorCreation=true`, manda `config.allowSupervisorValidation=true` → 200; a partir de ahí puede validar (TSK-14)
  - TSK-05-26 · PROP · body con `status: "completed"` → 200, el estado no cambia (`status` no se lee aquí)
- Sospechas:
  - `scheduledStartAt: null` o `""` no vacía el campo. `:36-37` asigna `undefined`, `stripUndefined` lo quita (`REPO:53,105`), y además el aviso se recalcula con la fecha vieja (`:80-82`).
  - Una `config` parcial reemplaza la config completa y desactiva en silencio los interruptores no enviados (`:53-58`, `H:330-339`).
  - Un supervisor con `allowSupervisorCreation` puede concederse `allowSupervisorValidation` o `allowSupervisorRating` editando la config: escalada de permisos.
  - Se acepta un título vacío en la edición (`:26`), aunque el alta lo exige.

## POST /api/v1/tasks/:taskId/duplicate  ·  TSK-06
- Servicio: tasks, `taskRouter.ts:27` → `CT/duplicateTask.controller.ts:26-128`.
- Consumidores: panel (`PSVC:181-194`, llamado desde `PLIST:248` y `PDET:300`). La app no la usa.
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente. En un rollback del panel a la CF, duplicar dejaría de funcionar: el router CF no tiene la ruta (`CF/taskRouter.ts:19-32`) y la CF no instala manejador 404 propio, así que respondería el 404 por defecto de Express (sin confirmar el formato exacto).
- Autenticación: `resolveTaskActor` con el `branchId` del original.
- Autorización: `canManageTask(actor, config normalizada del original)` (`:53`).
- Entrada: obligatorios `entityId` y `dueAt`; opcionales `scheduledStartAt` y `title`.
- Respuesta correcta: 201, el documento `Task` de la copia.
- Efectos:
  - Crea una tarea `draft`, con `assignedEmployeeIds: []` y sin `metadata`.
  - Copia `description`, `priority`, `workSite` (literal, sin volver a Google) y `config`.
  - Actividad `created` con `metadata.duplicatedFrom`.
  - Evento `task.created`. Sin notificación.
- Criticidad: media — el panel la usa en el listado y en el detalle.
- Casos:
  - TSK-06-01 · ANON · sin `dueAt` → 400 `task/bad_request`
  - TSK-06-02 · ANON · original inexistente → 404 `task/not_found`
  - TSK-06-03 · ANON · original existente → 401 `auth/unauthorized`
  - TSK-06-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-06-05 · PROP · `dueAt` válido → 201. `status: draft`, título «<original> (copia)», sin asignados, `workSite` idéntico, sin `metadata`, actividad con `duplicatedFrom`
  - TSK-06-06 · PROP · `title: "Nuevo"` → 201 con ese título; `title: "   "` → 201 con «(copia)»
  - TSK-06-07 · ADMIN → 201
  - TSK-06-08 · OP_MANAGER / OP_OWNER → 201
  - TSK-06-09 · OP_SUPERVISOR · original con `allowSupervisorCreation=true` → 201
  - TSK-06-10 · OP_SUPERVISOR · original con `allowSupervisorCreation=false` → 403 `task/unauthorized`
  - TSK-06-11 · OP_WORKER · asignado al original → 403 `task/unauthorized`
  - TSK-06-12 · AJENO → 403 `task/unauthorized`
  - TSK-06-13 · PROP · el original tiene guardado `config.maxPhotoSizeMB: 0` → 400 `task/source_config_invalid`
  - TSK-06-14 · PROP · sucursal del original inactiva → 400 `task/branch_inactive`; borrada → 404 `task/branch_not_found`
  - TSK-06-15 · PROP · `dueAt` inválido → 400 `task/bad_request`
  - TSK-06-16 · PROP · `scheduledStartAt` inválido → 400 `task/bad_request`
  - TSK-06-17 · PROP · original importado por un add-on (`metadata.externalRef`) → 201, la copia sale sin `metadata`
  - TSK-06-18 · PROP · original en `cancelled` o `validated` → 201 (el estado del original no se mira)
  - TSK-06-19 · PROP · original con `notifyIfNotStarted=true` y `scheduledStartAt` nuevo → 201, `scheduledStartNotificationAt` = +15 min
  - TSK-06-20 · OP_WORKER · original con config inválida → 400 `task/source_config_invalid`, no 403: la config se valida antes que el permiso (`:47-55`)
- Sospechas: un actor sin permiso recibe `task/source_config_invalid` en vez de 403 cuando el original tiene la config rota (`:47-55`). Revela algo del original a quien no puede gestionarlo; impacto bajo.

## POST /api/v1/tasks/:taskId/pause  ·  TSK-07
- Servicio: tasks, `taskRouter.ts:28` → `CT/pauseTask.controller.ts:21-71`; la transacción está en `REPO:247-269`.
- Consumidores: app (`AppConstants.taskEndpoint`, `ADS:261-282`, `AREPO:144`). El panel no tiene la acción (`PSVC` no la define).
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente. En un rollback la app perdería la pausa.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canOperateAssignedTask` (`:35`). No se exige jornada ni geocerca (diseño D5 de `DOCS/ingenieria/tasks-service/08_pausas.md:57-61`).
- Entrada:
  - `entityId`, obligatorio.
  - `reason`, opcional: se recorta y, si queda vacío, no se guarda.
  - `geo`, opcional: se guarda si es válido, pero no se juzga.
- Respuesta correcta: 200, el `Task` con `pausedAt`, `pausedBy`, `pauseId` y `pauseCount` incrementado.
- Efectos:
  - En una sola transacción:
    - crea `pauses/{pauseId}` con `startedAt`, `startedBy`, `startedByRole` y `reason`;
    - actualiza `pausedAt`, `pausedBy`, `pauseId`, `pauseCount`, `updatedAt` y `updatedBy` de la tarea.
  - Después, actividad `paused` con `pauseId`, `reason` y `geo`.
  - Evento `task.paused`, sin el motivo (`events/task.ts:74-78`).
  - Sin notificación.
- Criticidad: alta — flujo diario de la app.
- Casos:
  - TSK-07-01 · ANON · sin `entityId` → 400 `task/bad_request`
  - TSK-07-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-07-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-07-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-07-05 · OP_WORKER · asignado, tarea `in_progress`, **sin jornada abierta** → 200, `pauseCount: 1` (pausar no pide jornada)
  - TSK-07-06 · OP_WORKER · asignado, `reason: " comer "` → 200; la pausa guarda `"comer"` y el evento no lleva el motivo
  - TSK-07-07 · OP_WORKER · asignado, `geo` válido → 200; la actividad lleva `metadata.geo`
  - TSK-07-08 · OP_WORKER · asignado, `geo: {lat:"x"}` → 200; la actividad va sin `geo`
  - TSK-07-09 · OP_WORKER · no asignado → 403 `task/unauthorized`
  - TSK-07-10 · OP_SUPERVISOR · no asignado → 200
  - TSK-07-11 · OP_MANAGER / OP_OWNER → 200
  - TSK-07-12 · PROP / ADMIN → 200 (`startedByRole` = `owner` / `admin`)
  - TSK-07-13 · OP_OTRA_SUCURSAL (JWT) · no figura en la tarea → 403 `task/unauthorized`
  - TSK-07-14 · AJENO → 403 `task/unauthorized`
  - TSK-07-15 · EMP_INACTIVO · asignado → 200
  - TSK-07-16 · OP_WORKER · tarea `assigned` (sin iniciar) → 400 `task/not_in_progress`
  - TSK-07-17 · PROP · tarea en `completed`, `validated`, `draft`, `cancelled` o `rejected` → 400 `task/not_in_progress`
  - TSK-07-18 · OP_WORKER · tarea ya pausada → 400 `task/already_paused`
  - TSK-07-19 · 2 × OP_WORKER · pausan a la vez → una 200 y la otra 400 `task/already_paused` (lo decide la transacción)
  - TSK-07-20 · OP_WORKER · segunda pausa tras reanudar → 200, `pauseCount: 2`, conserva el `pausedMs` acumulado
  - TSK-07-21 · OP_WORKER · tarea con `workSite`, lejos y sin `geo` → 200 (pausar no mira la geocerca)
- Sospechas: ninguna sobre el comportamiento diseñado.

## POST /api/v1/tasks/:taskId/resume  ·  TSK-08
- Servicio: tasks, `taskRouter.ts:29` → `CT/resumeTask.controller.ts:25-120`; la transacción está en `REPO:271-282`.
- Consumidores: app (`AppConstants.taskEndpoint`, `ADS:285-306`, `AREPO:160`). El panel no la usa.
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización y orden de comprobaciones:
  1. `canOperateAssignedTask` (`:39`).
  2. `task.pausedAt`; si no está → 400 `task/not_paused` (`:45-47`).
  3. Jornada abierta para empleados que no son writers (`:50-51`).
  4. Si la tarea tiene `workSite`: `geo` obligatorio y dentro de la valla (`:58-92`).
- Entrada: `entityId`, obligatorio; `geo`, obligatorio si la tarea tiene `workSite`.
- Respuesta correcta: 200, el `Task` sin `pausedAt`, `pausedBy` ni `pauseId`, y con `pausedMs` = anterior + duración de la pausa.
- Efectos:
  - Transacción que cierra la pausa (`pauses/{id}`: `endedAt`, `endedBy`, `endedReason: "resumed"`, `durationMs`) y suma la duración a la tarea.
  - Actividad `resumed` con `pauseId`, `durationMs` y, si aplica, `geo`, `workSite`, `distanceMeters`, `withinWorkSite` y `openSession`.
  - Evento `task.resumed` con `pause_duration_ms`.
  - Si la valla lo rechaza: actividad `resume_rejected`.
- Criticidad: alta — flujo diario de la app.
- Casos:
  - TSK-08-01 · ANON · sin `entityId` → 400 `task/bad_request`
  - TSK-08-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-08-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-08-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-08-05 · OP_WORKER · asignado, pausada, jornada abierta, sin `workSite` → 200; sin `pausedAt`, `pausedMs` sumado, pausa con `endedReason: "resumed"`
  - TSK-08-06 · OP_WORKER · asignado, pausada, sin jornada → 400 `task/no_open_session`
  - TSK-08-07 · OP_WORKER · asignado, tarea no pausada y sin jornada → 400 `task/not_paused` (se comprueba antes que la jornada)
  - TSK-08-08 · OP_WORKER · no asignado → 403 `task/unauthorized`
  - TSK-08-09 · OP_SUPERVISOR · no asignado, con jornada → 200
  - TSK-08-10 · OP_SUPERVISOR · sin jornada → 400 `task/no_open_session`
  - TSK-08-11 · OP_MANAGER / OP_OWNER · sin jornada → 400 `task/no_open_session` (no son writers)
  - TSK-08-12 · PROP / ADMIN · sin jornada, tarea sin `workSite` → 200 (están exentos)
  - TSK-08-13 · PROP+EMP · sin jornada → 200 (exento por ser writer, `H:499-501`)
  - TSK-08-14 · OP_WORKER · tarea con `workSite`, sin `geo` → 400 `task/geo_required`
  - TSK-08-15 · OP_WORKER · tarea con `workSite`, `geo` fuera del radio → 400 `task/out_of_worksite` con `details: {distanceMeters, allowedRadiusMeters}`; actividad `resume_rejected`; la tarea sigue pausada
  - TSK-08-16 · OP_WORKER · tarea con `workSite`, `geo` dentro → 200; actividad con `withinWorkSite: true`
  - TSK-08-17 · PROP · tarea con `workSite`, sin `geo` → 400 `task/geo_required` (la exención de jornada no alcanza a la valla)
  - TSK-08-18 · AJENO → 403 `task/unauthorized`
  - TSK-08-19 · EMP_INACTIVO · asignado, con jornada → 200
  - TSK-08-20 · 2 × OP_WORKER · reanudan a la vez → una 200 y la otra 400 `task/not_paused` (`REPO:277-278`)
  - TSK-08-21 · OP_WORKER · tarea `rejected` que conserva una pausa abierta (ver TSK-15-13) → 200; el estado sigue `rejected`
  - TSK-08-22 · OP_OTRA_SUCURSAL (JWT) · no figura en la tarea → 403 `task/unauthorized`
- Sospechas:
  - Reanudar no mira el estado de la tarea (`:45` y `REPO:271-282` solo miran `pausedAt`). Una pausa que sobrevive a un rechazo, que no la cierra (TSK-15), se reanuda con la tarea en `rejected`.
  - La valla exige `geo` a todos los actores, writers incluidos (`:58-61`). Hoy no rompe nada porque el panel no reanuda.

## POST /api/v1/tasks/:taskId/assignments  ·  TSK-09
- Servicio: tasks, `taskRouter.ts:30` → `CT/assignTaskWorkers.controller.ts:6-73`.
- Consumidores:
  - panel: `PSVC:196-209`, llamado desde `PDET:205`
  - app: `AppConstants.taskEndpoint`, `ADS:309-324` y `AREPO:176`
- Origen: portado desde la CF `CF/assignTaskWorkers.controller.ts`.
- Diferencias con la CF: ninguna visible; solo se añade el evento `task.assigned`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canAssignTaskWorkers` (`:20`): writer, o nivel supervisor o superior. No hay interruptor.
- Entrada:
  - `entityId`, obligatorio.
  - `employeeIds`, obligatorio y array. Se convierte a texto, se recorta, se quitan vacíos y se deduplica (`:24`).
  - Cada empleado debe estar activo y tener responsabilidad en la sucursal de la tarea.
- Respuesta correcta: 200, array con **todas** las `TaskAssignment` de la tarea, incluidas las `removed` (`:66,72`).
- Efectos:
  - Upsert de `assignments/{employeeId}` con `status: "assigned"` y `assignedAt` para **todos** los enviados (`:33-45`).
  - `assignedEmployeeIds` pasa a ser la unión; si la tarea estaba en `draft`, pasa a `assigned` (`:47-53`).
  - Actividad `assigned`.
  - Solo a los recién asignados: evento `task.assigned` y notificación `task_assigned`, esta **esperada con `await`** (`:68-71`).
- Criticidad: alta — reparto del trabajo desde el panel y desde la app.
- Casos:
  - TSK-09-01 · ANON · `employeeIds` **que no es un array** (una cadena, un número) → 400 `task/bad_request`. Corregido el 2026-09-12 al ejecutarlo: con `employeeIds` **ausente** NO da 400, porque el controlador desestructura con `employeeIds = []` y una lista vacía pasa la comprobación; la petición sigue hasta el 404.
  - TSK-09-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-09-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-09-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-09-05 · PROP · tarea `draft` con `[A]` válido → 200. `status: assigned`, asignación de A en `assigned`, notificación a A, evento con `newly_assigned_employee_ids: [A]`
  - TSK-09-06 · ADMIN · tarea `in_progress` con `[B]` → 200, el estado sigue `in_progress` y B queda `assigned`
  - TSK-09-07 · OP_SUPERVISOR → 200 (no depende de interruptores)
  - TSK-09-08 · OP_MANAGER / OP_OWNER → 200
  - TSK-09-09 · OP_WORKER · asignado → 403 `task/unauthorized`
  - TSK-09-10 · OP_OTRA_SUCURSAL (JWT) → 403 `task/unauthorized`
  - TSK-09-11 · AJENO → 403 `task/unauthorized`
  - TSK-09-12 · PROP · empleado inactivo → 400 `task/invalid_employees` con `invalidEmployees`
  - TSK-09-13 · PROP · empleado sin responsabilidad en la sucursal → 400 `task/invalid_employees`
  - TSK-09-14 · PROP · `[A, " A ", ""]` → 200, se deduplica a `[A]`
  - TSK-09-15 · PROP · `[]` → 200. Sin cambios en la tarea; se registra igualmente una actividad `assigned` con `employeeIds: []`
  - TSK-09-16 · PROP · reenvía A, que está `working` → 200. La asignación de A **vuelve a `assigned`** con `assignedAt` nuevo; sin notificación, porque A no es nuevo
  - TSK-09-17 · PROP · A estaba `removed` → 200. A vuelve a `assignedEmployeeIds` y a `assigned`; `removedAt` se conserva
  - TSK-09-18 · PROP · tarea `validated` o `cancelled` con `[C]` → 200, el estado no cambia
  - TSK-09-19 · PROP · empleado válido cuya ficha no tiene `uid` → sin confirmar: 200, o 500 `internal_error` con la asignación ya escrita (la notificación in-app llevaría `uid: undefined`)
  - TSK-09-20 · EMP_INACTIVO · con nivel supervisor → 200 (no se mira el estado del actor)
- Sospechas:
  - Reenviar a un empleado ya asignado reinicia su asignación a `assigned` aunque estuviera `working` o `completed` (`:33-45`, `REPO:146-155`). Sin confirmar si el panel manda la lista completa o solo los nuevos.
  - La notificación se espera con `await` (`:70`). Si falla la escritura in-app (`packages/shared/src/checkbiz/notifications/CheckbizOperationals.ts:207`, con `uid: employee.uid as string`; `document.create` no filtra `undefined` en `packages/shared/src/notifications/FirestoreAppNotificationsRepository.ts:34-37`; y `ignoreUndefinedProperties` no aparece en `shared`), la petición responde 500 con la asignación ya hecha. Las demás rutas notifican sin esperar.
  - Se puede asignar gente a tareas cerradas (`validated`, `cancelled`, `rejected`).

## DELETE /api/v1/tasks/:taskId/assignments/:employeeId  ·  TSK-10
- Servicio: tasks, `taskRouter.ts:31` → `CT/unassignTaskWorker.controller.ts:5-61`.
- Consumidores:
  - panel: `PSVC:211-226`, con `entityId` en la query, llamado desde `PDET:201`
  - app: `ADS:327-342` y `AREPO:190`
- Origen: portado desde la CF `CF/unassignTaskWorker.controller.ts`.
- Diferencias con la CF: ninguna visible; solo se añade el evento `task.unassigned`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canAssignTaskWorkers` (`:21`).
- Entrada: `taskId` y `employeeId` en la ruta; `entityId` en el body o en la query (`:8`).
- Respuesta correcta: 200, array de `TaskAssignment`, incluidas las `removed`.
- Efectos:
  - La asignación pasa a `status: "removed"` con `removedAt`.
  - Se quita al empleado de `assignedEmployeeIds`; si la tarea estaba `assigned` y se queda vacía, pasa a `draft` (`:38`).
  - Actividad de tipo `assigned` con `metadata.action: "unassigned"`.
  - Evento `task.unassigned`. No se notifica al retirado.
- Criticidad: media.
- Casos:
  - TSK-10-01 · ANON · sin `entityId` → 400 `task/bad_request`
  - TSK-10-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-10-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-10-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-10-05 · PROP · tarea `assigned` con `[A, B]`, retira a A → 200; A queda `removed` y la tarea sigue `assigned`
  - TSK-10-06 · PROP · tarea `assigned` con `[A]`, retira a A → 200, la tarea pasa a `draft`
  - TSK-10-07 · PROP · tarea `in_progress` con `[A]`, retira a A → 200, sigue `in_progress` sin nadie asignado
  - TSK-10-08 · ADMIN / OP_MANAGER / OP_OWNER → 200
  - TSK-10-09 · OP_SUPERVISOR → 200
  - TSK-10-10 · OP_WORKER → 403 `task/unauthorized`
  - TSK-10-11 · AJENO → 403 `task/unauthorized`
  - TSK-10-12 · PROP · `employeeId` que no está asignado → 404 `task/assignment_not_found`
  - TSK-10-13 · PROP · `employeeId` ya `removed` → 404 `task/assignment_not_found`
  - TSK-10-14 · PROP · `entityId` en la query (como el panel y la app) → 200; en el body → 200
  - TSK-10-15 · OP_WORKER · A, ya retirado, intenta completar → 403 `task/unauthorized` (ver TSK-11)
- Sospechas: retirar al último asignado de una tarea en curso la deja `in_progress` sin nadie y con la pausa abierta, si la había (`:36-41`).

## PATCH /api/v1/tasks/:taskId/status  ·  TSK-11
- Servicio: tasks, `taskRouter.ts:32` → `CT/updateTaskStatus.controller.ts:9-203`. Caso de uso: `application/use-cases/task/UpdateTaskStatus.ts:7-22`. Cierre de pausa en transacción: `REPO:284-298`.
- Consumidores:
  - panel: `PSVC:228-251`, llamado desde `PDET:192` (editar), `PDET:196` (botones de estado) y `PDET:208` (cancelar). Traduce `cancellationReason` a `reason` (`PSVC:244-245`) y **no manda `geo`**.
  - app: `AppConstants.taskEndpoint`, `ADS:233-258` (`changeStatus`, con `reason` y `geo`) y `AREPO:126`.
- Origen: portado desde la CF `CF/updateTaskStatus.controller.ts`.
- Diferencias con la CF:
  - `in_progress` y `completed` exigen jornada abierta a empleados que no son writers → 400 `task/no_open_session` (`:51-52`). La CF no lo exigía.
  - Con `workSite`, `geo` es obligatorio para **cualquier** actor → 400 `task/geo_required` (`:57-60`). Iniciar fuera de la valla → 400 `task/out_of_worksite` y actividad `start_rejected` (`:76-98`). La CF no tenía nada de esto.
  - `completed`, `cancelled`, `assigned` y `draft` cierran la pausa abierta en la transacción (`:120,131,146,164`); `assigned` y `draft` ponen además `pausedMs` y `pauseCount` a 0.
  - `FieldValue.delete()` borra de verdad. En la CF, el `stripUndefined` sin guarda dejaba `startedAt: {}` y similares al reabrir (`REPO:38-42`).
  - `actorRole: "admin"` en la actividad; evento `task.status_changed`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización según el destino:
  - `in_progress` y `completed` → `canOperateAssignedTask` (`:45`).
  - `cancelled`, `assigned` y `draft` → `canManageTask(task.config)` (`:125,133,148`).
  - cualquier otro valor → 400 (`:165-167`).
- Entrada:
  - Obligatorios: `entityId` y `status`.
  - Opcionales: `reason` (cancelación) y `geo {lat,lng}`.
- Respuesta correcta: 200, el `Task` actualizado.
- Efectos:
  - Se actualiza la tarea.
  - Si el actor tiene `employeeId`, se escribe su asignación con merge: `working` al iniciar, `completed` al completar (`:107-109`, `:121-123`, `REPO:157-159`). **Se crea aunque no esté asignado.**
  - Se cierra la pausa, si la hay.
  - Actividad `started`, `completed`, `cancelled` o `status_changed`, con `fromStatus`, `toStatus` y `metadata` de geo y jornada.
  - Evento `task.status_changed`.
  - Notificación `task_started` / `task_completed` sin esperar.
  - Dispara el trigger CF `onWriteTaskForPattern`.
- Criticidad: alta — es el núcleo del trabajo en la app: iniciar y completar.
- Casos:
  - Generales
    - TSK-11-01 · ANON · sin `status` → 400 `task/bad_request`
    - TSK-11-02 · ANON · tarea inexistente → 404 `task/not_found`
    - TSK-11-03 · ANON · tarea existente, `status` válido → 401 `auth/unauthorized`
    - TSK-11-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
    - TSK-11-05 · AJENO (Firebase) → 403 `task/unauthorized`
    - TSK-11-06 · AJENO (EMP_JWT de otra entidad) → 403 `task/unauthorized`
    - TSK-11-07 · EMP_JWT · ficha borrada → 404 `task/employee_not_found`
    - TSK-11-08 · PROP · `status: "validated"` → 400 `task/bad_request` («Unsupported status transition»)
    - TSK-11-09 · PROP · `status: "rejected"` → 400 `task/bad_request` («Unsupported status transition»)
    - TSK-11-10 · PROP · `status: "foo"` → 400 `task/bad_request`
    - TSK-11-11 · ANON · `status: "foo"` sobre una tarea existente → 401 `auth/unauthorized` (el actor se resuelve antes de mirar el destino)
  - → `in_progress`
    - TSK-11-12 · OP_WORKER · asignado, jornada abierta, tarea `assigned` sin `workSite`, antes de `dueAt` → 200. Queda `in_progress` con `startedAt` y `timeComplianceStatus: on_time`; su asignación pasa a `working`; actividad `started` con `metadata.openSession`; evento; notificación `task_started`
    - TSK-11-13 · OP_WORKER · ídem con `dueAt` ya pasado → 200, `timeComplianceStatus: overdue`
    - TSK-11-14 · OP_WORKER · asignado, sin jornada → 400 `task/no_open_session`
    - TSK-11-15 · OP_WORKER · asignado, último check-in con `status != valid`, `closed: true` o `deadline` vencido → 400 `task/no_open_session`
    - TSK-11-16 · OP_WORKER · no asignado → 403 `task/unauthorized`
    - TSK-11-17 · OP_OTRA_SUCURSAL (JWT) · no figura en la tarea → 403 `task/unauthorized`
    - TSK-11-18 · OP_OTRA_SUCURSAL (Firebase) → 403 `task/unauthorized`
    - TSK-11-19 · OP_SUPERVISOR · no asignado, con jornada → 200. Se crea `assignments/{su employeeId}` en `working`, sin que figure en `assignedEmployeeIds`
    - TSK-11-20 · OP_SUPERVISOR · sin jornada → 400 `task/no_open_session`
    - TSK-11-21 · OP_MANAGER / OP_OWNER · no asignado: con jornada → 200; sin jornada → 400 `task/no_open_session`
    - TSK-11-22 · PROP · sin ficha, sin jornada, tarea sin `workSite` → 200, sin tocar ninguna asignación
    - TSK-11-23 · ADMIN+EMP · sin jornada → 200 (exento); la asignación de su ficha pasa a `working` (se crea el documento)
    - TSK-11-24 · OP_WORKER · tarea con `workSite`, sin `geo` → 400 `task/geo_required`
    - TSK-11-25 · OP_WORKER · tarea con `workSite`, `geo: {lat:200,lng:0}` → 400 `task/geo_required` (`parseGeoPayload` lo descarta)
    - TSK-11-26 · OP_WORKER · tarea con `workSite`, `geo` fuera del radio → 400 `task/out_of_worksite` con `details: {distanceMeters, allowedRadiusMeters}`; actividad `start_rejected`; la tarea no cambia
    - TSK-11-27 · OP_WORKER · tarea con `workSite`, `geo` dentro → 200; actividad con `geo`, copia de `workSite`, `distanceMeters`, `withinWorkSite: true` y `openSession`
    - TSK-11-28 · PROP · tarea con `workSite`, sin `geo` (como el panel) → 400 `task/geo_required`
    - TSK-11-29 · OP_WORKER · tarea `completed` → 200 `in_progress`: no se controla el origen; conserva `startedAt` y `completedAt`
    - TSK-11-30 · OP_WORKER · tarea `validated`, `cancelled` o `rejected` → 200 `in_progress`
    - TSK-11-31 · OP_SUPERVISOR · tarea `draft` sin asignados, con jornada → 200 `in_progress`
    - TSK-11-32 · OP_WORKER · tarea pausada, con jornada → 200. Sigue `in_progress` y **`pausedAt` se mantiene**: iniciar no reanuda ni cierra la pausa
    - TSK-11-33 · OP_WORKER · un segundo asignado inicia una tarea ya `in_progress` → 200; `startedAt` no cambia, su asignación pasa a `working` y se recalcula `timeComplianceStatus`
    - TSK-11-34 · EMP_INACTIVO · asignado, con jornada → 200
  - → `completed`
    - TSK-11-35 · OP_WORKER · asignado, con jornada, sin evidencia exigida → 200 `completed`. `completedAt`, `completedBy` = su `employeeId`, `timeComplianceStatus: completed_on_time`; su asignación pasa a `completed`; notificación `task_completed`
    - TSK-11-36 · OP_WORKER · ídem con `dueAt` ya pasado → 200, `timeComplianceStatus: completed_late`
    - TSK-11-37 · OP_WORKER · `requireEvidenceOnCompletion=true` y ningún recurso → 400 `task/evidence_required`
    - TSK-11-38 · OP_WORKER · `requireEvidenceOnCompletion=true` y al menos un recurso, de quien sea y del tipo que sea → 200
    - TSK-11-39 · OP_WORKER · `requireEvidenceOnCompletion=false`, sin recursos → 200
    - TSK-11-40 · OP_WORKER · sin jornada → 400 `task/no_open_session`
    - TSK-11-41 · OP_WORKER · tarea con `workSite`, sin `geo` → 400 `task/geo_required`
    - TSK-11-42 · OP_WORKER · tarea con `workSite`, `geo` fuera del radio → 200: completar solo mide, y la actividad lleva `withinWorkSite: false`
    - TSK-11-43 · OP_WORKER · tarea pausada → 200. La pausa se cierra con `endedReason: "completed"`, `pausedMs` suma la duración y `pausedAt` desaparece
    - TSK-11-44 · OP_WORKER A · `completionPolicy: all_assigned_workers`, asignados `[A, B]`, completa A → 200. **La tarea entera queda `completed`**; la asignación de B no cambia
    - TSK-11-45 · OP_WORKER A · `completionPolicy: any_assigned_worker` → 200, mismo resultado que el caso 44
    - TSK-11-46 · OP_WORKER B · completa después, con la tarea ya `completed` → 200; se sobrescriben `completedAt` y `completedBy`, y su asignación pasa a `completed`
    - TSK-11-47 · OP_WORKER · tarea `assigned`, nunca iniciada → 200 `completed`, sin `startedAt`
    - TSK-11-48 · OP_WORKER · tarea `validated`, `cancelled` o `rejected` → 200 `completed`
    - TSK-11-49 · PROP · sin jornada, tarea sin `workSite` → 200; `completedBy` = su uid (o su `employeeId` si es PROP+EMP)
    - TSK-11-50 · OP_WORKER · no asignado → 403 `task/unauthorized`
    - TSK-11-51 · OP_SUPERVISOR · no asignado, con jornada → 200; se crea su asignación en `completed`
  - → `cancelled`
    - TSK-11-52 · PROP · `reason: "x"` → 200 `cancelled`, con `cancelledAt`, `cancelledBy` y `cancellationReason: "x"`; actividad `cancelled`
    - TSK-11-53 · PROP · manda `cancellationReason` en vez de `reason` → 200, sin `cancellationReason`
    - TSK-11-54 · OP_MANAGER / OP_OWNER · sin jornada → 200 (cancelar no pide jornada)
    - TSK-11-55 · OP_SUPERVISOR · `allowSupervisorCreation=true` → 200
    - TSK-11-56 · OP_SUPERVISOR · `allowSupervisorCreation=false` → 403 `task/unauthorized`
    - TSK-11-57 · OP_WORKER · asignado → 403 `task/unauthorized`
    - TSK-11-58 · PROP · tarea pausada → 200; la pausa se cierra con `endedReason: "cancelled"`
    - TSK-11-59 · PROP · tarea `validated` → 200 `cancelled`; tarea ya `cancelled` → 200, se reescribe `cancelledAt`
  - → `assigned` (reabrir)
    - TSK-11-60 · PROP · tarea `completed` con asignados → 200 `assigned`. Se borran `startedAt`, `completedAt`, `completedBy` y `cancelled*`; `timeComplianceStatus: not_started`; `pausedMs: 0` y `pauseCount: 0`
    - TSK-11-61 · PROP · tarea sin asignados → 400 `task/bad_request` («Cannot set status to assigned without assigned workers»)
    - TSK-11-62 · OP_SUPERVISOR · `allowSupervisorCreation=true` → 200
    - TSK-11-63 · OP_SUPERVISOR · `allowSupervisorCreation=false` → 403 `task/unauthorized`
    - TSK-11-64 · OP_WORKER · asignado → 403 `task/unauthorized`
    - TSK-11-65 · PROP · tarea `validated` → 200 `assigned`, pero **se conservan `validatedAt` y `validatedBy`**
    - TSK-11-66 · PROP · tarea `rejected` → 200 `assigned`, pero **se conservan `rejectedAt`, `rejectedBy` y `rejectionReason`**; `timeComplianceStatus: not_started`
    - TSK-11-67 · PROP · tarea pausada → 200; la pausa se cierra con `endedReason: "reset"` y los contadores quedan a 0
  - → `draft` (reabrir)
    - TSK-11-68 · PROP · tarea `validated` → 200 `draft`. Se borran todos los sellos (inicio, fin, validación, rechazo, cancelación); `not_started`; contadores a 0
    - TSK-11-69 · PROP · tarea con asignados → 200 `draft`, **conservando `assignedEmployeeIds`**
    - TSK-11-70 · OP_SUPERVISOR · `allowSupervisorCreation=true` → 200
    - TSK-11-71 · OP_SUPERVISOR · `allowSupervisorCreation=false` → 403 `task/unauthorized`
    - TSK-11-72 · OP_WORKER · asignado → 403 `task/unauthorized`
    - TSK-11-73 · PROP · tarea pausada → 200; la pausa se cierra con `endedReason: "reset"`
  - Carreras
    - TSK-11-74 · PROP · la tarea se borra entre la lectura y la escritura de `completed`, `cancelled`, `assigned` o `draft` → 404 `task/not_found` (`REPO:290`). Sin confirmar que se pueda reproducir.
    - TSK-11-75 · OP_WORKER · la tarea se borra entre la lectura y la escritura de `in_progress` → sin confirmar: 200 y un documento parcial recreado, porque ese camino hace `set` con merge sin transacción (`UpdateTaskStatus.ts:17`, `REPO:104-106`)
- Sospechas:
  - **No se controla el estado de origen** (`:104-167`). Un trabajador asignado puede iniciar o completar tareas `validated`, `cancelled` o `rejected`, y un gestor puede cancelar o reabrir desde cualquier estado.
  - **`completionPolicy` no se aplica.** Con `all_assigned_workers`, el primer asignado que completa cierra la tarea para todos (`:110-123`). Solo `H:334` lee el campo, para normalizarlo.
  - Iniciar una tarea pausada devuelve 200 y deja la pausa abierta (`:104-109`, sin `closePause`). El trabajador cree que ha reanudado y sigue contando pausa.
  - La asignación del actor se escribe aunque no esté asignado (`:107-109`, `:121-123`). Supervisores, managers y PROP+EMP generan asignaciones fantasma que aparecen en el detalle, pero no en `assignedEmployeeIds`.
  - Reabrir a `assigned` no borra `validatedAt`/`validatedBy`/`rejected*` (`:139-145`); reabrir a `draft` sí (`:152-162`). La tarea queda `assigned` con sellos de validación o rechazo.
  - La valla pide `geo` también a PROP y ADMIN (`:57-60`), aunque `H:491-501` los exime de jornada precisamente para que el panel pueda cerrar tareas. Hoy el panel no puede iniciar ni completar una tarea con `workSite`; `encodebiz-front-saas/src/config/errorLocales.ts:102` lo asume en el mensaje.
  - EMP_INACTIVO opera igual que un activo.

## POST /api/v1/tasks/:taskId/notes  ·  TSK-12
- Servicio: tasks, `taskRouter.ts:33` → `CT/addTaskNote.controller.ts:6-51`.
- Consumidores:
  - panel: `PSVC:253-266`, llamado desde `PDET:206`
  - app: `ADS:345-364` y `AREPO:205`
- Origen: portado desde la CF `CF/addTaskNote.controller.ts`.
- Diferencias con la CF: ninguna visible. Añade el evento `task.note_added`, y `createdByRole` puede valer `"admin"`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canAddTaskNote` (`:20`).
- Entrada:
  - Obligatorios: `entityId` y `content` (se exige que no sea vacío **antes** de recortarlo).
  - Opcional: `type`, por defecto `operational_note`. No se valida contra el enumerado de `Task.ts:177`.
- Respuesta correcta: 201, la `TaskNote` creada.
- Efectos:
  - Crea `notes/{id}` y la actividad `note_added`.
  - Evento `task.note_added`, sin el texto.
  - Notificación `task_updated` a los asignados, sin esperar.
- Criticidad: media — comunicación desde el panel y desde la app.
- Casos:
  - TSK-12-01 · ANON · sin `content` → 400 `task/bad_request`
  - TSK-12-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-12-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-12-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-12-05 · PROP · `type: "specification"` → 201, `createdByRole: "owner"` (o la responsabilidad de su ficha, si es PROP+EMP)
  - TSK-12-06 · ADMIN → 201, `createdByRole: "admin"`
  - TSK-12-07 · OP_SUPERVISOR · no asignado → 201
  - TSK-12-08 · OP_MANAGER / OP_OWNER → 201
  - TSK-12-09 · OP_WORKER · asignado, sin `type` → 201, `type: "operational_note"` y `createdByRole: "worker"`
  - TSK-12-10 · OP_WORKER · no asignado → 403 `task/unauthorized`
  - TSK-12-11 · OP_OTRA_SUCURSAL (JWT) → 403 `task/unauthorized`
  - TSK-12-12 · AJENO → 403 `task/unauthorized`
  - TSK-12-13 · PROP · `type: "cualquier_cosa"` → 201, se guarda tal cual
  - TSK-12-14 · PROP · `content: "   "` → 201, `content: ""`
  - TSK-12-15 · PROP · `content: 123` → 201, `content: "123"`
  - TSK-12-16 · EMP_INACTIVO · asignado → 201
  - TSK-12-17 · PROP · tarea `validated` o `cancelled` → 201 (no hay restricción de estado)
- Sospechas:
  - `type` no se valida (`:8,30`).
  - Un contenido de solo espacios pasa el control y se guarda vacío (`:9` frente a `:29`).

## PATCH /api/v1/tasks/:taskId/notes/:noteId  ·  TSK-13
- Servicio: tasks, `taskRouter.ts:34` → `CT/updateTaskNote.controller.ts:5-50`.
- Consumidores: ninguno detectado. `PSVC:268-282` define `updateTaskNote`, pero nada en `src/` la usa; la app no tiene la acción.
- Origen: portado desde la CF `CF/updateTaskNote.controller.ts`.
- Diferencias con la CF: ninguna visible (el controlador es idéntico).
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canManageTask(actor, task.config)` (`:20`). No depende de quién escribió la nota.
- Entrada: `entityId` y `content`, obligatorios.
- Respuesta correcta: 200 `{noteId, updatedAt}`.
- Efectos:
  - Merge de `content`, `updatedAt` y `updatedBy` en la nota.
  - Actividad `note_updated`.
  - Notificación `task_updated`.
- Criticidad: baja — sin consumidores.
- Casos:
  - TSK-13-01 · ANON · sin `content` → 400 `task/bad_request`
  - TSK-13-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-13-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-13-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-13-05 · PROP · nota existente → 200 `{noteId, updatedAt}`
  - TSK-13-06 · ADMIN / OP_MANAGER / OP_OWNER · nota escrita por otra persona → 200
  - TSK-13-07 · OP_SUPERVISOR · `allowSupervisorCreation=true` → 200
  - TSK-13-08 · OP_SUPERVISOR · `allowSupervisorCreation=false` → 403 `task/unauthorized`
  - TSK-13-09 · OP_WORKER · autor de la nota → 403 `task/unauthorized`
  - TSK-13-10 · AJENO → 403 `task/unauthorized`
  - TSK-13-11 · PROP · `noteId` inexistente → 404 `task/note_not_found`
  - TSK-13-12 · PROP · `noteId` de otra tarea → 404 `task/note_not_found`
- Sospechas: el trabajador no puede corregir su propia nota, y un gestor reescribe la de otro sin que quede el texto anterior (`:20`, `:31-35`).

## POST /api/v1/tasks/:taskId/validation  ·  TSK-14
- Servicio: tasks, `taskRouter.ts:35` → `CT/validateTask.controller.ts:6-66`.
- Consumidores:
  - panel: `PSVC:284-297`, llamado desde `PDET:198`
  - app: `ADS:367-381` (sin `comment`) y `AREPO:221`
- Origen: portado desde la CF `CF/validateTask.controller.ts`.
- Diferencias con la CF: ninguna visible. `validatedByRole` puede valer `"admin"`; añade el evento `task.validated`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canValidateOrRejectTask` (`:23`).
- Entrada: `entityId`, obligatorio; `comment`, opcional, se guarda como `reason`. La tarea tiene que estar `completed`, y eso se comprueba **antes de autenticar** (`:17-19`).
- Respuesta correcta: 200, la `TaskValidation`: `{id, result: "validated", reason, validatedBy, validatedByRole, validatedAt, …}`.
- Efectos:
  - Crea `validations/{id}`.
  - La tarea pasa a `validated`, con `validatedAt` y `validatedBy`.
  - Actividad `validated`.
  - Notificación `task_validated` a los asignados.
  - Evento `task.validated`.
- Criticidad: media.
- Casos:
  - TSK-14-01 · ANON · sin `entityId` → 400 `task/bad_request`
  - TSK-14-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-14-03 · ANON · tarea no completada → 400 `task/invalid_status` (sin autenticar)
  - TSK-14-04 · ANON · tarea `completed` → 401 `auth/unauthorized`
  - TSK-14-05 · TOKEN_INVALIDO · tarea `completed` → 401 `auth/unauthorized`
  - TSK-14-06 · PROP · tarea `completed` → 200, `result: "validated"`; la tarea queda `validated`
  - TSK-14-07 · ADMIN · `comment: "ok"` → 200, `reason: "ok"` y `validatedByRole: "admin"`
  - TSK-14-08 · OP_MANAGER / OP_OWNER → 200
  - TSK-14-09 · OP_SUPERVISOR · `allowSupervisorValidation=true` → 200
  - TSK-14-10 · OP_SUPERVISOR · `allowSupervisorValidation=false` → 403 `task/unauthorized`
  - TSK-14-11 · OP_WORKER · asignado → 403 `task/unauthorized`
  - TSK-14-12 · AJENO · tarea `completed` → 403 `task/unauthorized`
  - TSK-14-13 · PROP · tarea `in_progress`, `assigned` o `draft` → 400 `task/invalid_status`
  - TSK-14-14 · PROP · tarea ya `validated` → 400 `task/invalid_status`
  - TSK-14-15 · PROP · tarea `rejected` → 400 `task/invalid_status`
  - TSK-14-16 · PROP · dos validaciones simultáneas → sin confirmar: las dos 200 y dos documentos en `validations` (no hay transacción, `:28-45`)
  - TSK-14-17 · EMP_INACTIVO · con nivel manager → 200
- Sospechas:
  - Comprobar el estado antes de autenticar permite a ANON saber si una tarea está completada (`:17-19`).
  - Validar no es atómico: dos validaciones a la vez pueden duplicar el registro.

## POST /api/v1/tasks/:taskId/rejection  ·  TSK-15
- Servicio: tasks, `taskRouter.ts:36` → `CT/rejectTask.controller.ts:6-65`.
- Consumidores:
  - panel: `PSVC:299-312`, llamado desde `PDET:207`
  - app: `ADS:384-399` y `AREPO:234`
- Origen: portado desde la CF `CF/rejectTask.controller.ts`.
- Diferencias con la CF: ninguna visible; añade el evento `task.rejected`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea.
- Autorización: `canValidateOrRejectTask` (`:20`). **No mira el estado de la tarea.**
- Entrada: `entityId` y `reason`, obligatorios; `reason` se exige no vacío antes de recortarlo.
- Respuesta correcta: 200, la `TaskValidation` con `result: "rejected"`.
- Efectos:
  - Crea `validations/{id}`.
  - La tarea pasa a `rejected`, con `timeComplianceStatus: rejected`, `rejectedAt`, `rejectedBy` y `rejectionReason` (`:36-44`).
  - Actividad `rejected`.
  - Notificación `task_rejected`.
  - Evento `task.rejected`, **con el motivo**.
- Criticidad: media.
- Casos:
  - TSK-15-01 · ANON · sin `reason` → 400 `task/bad_request`
  - TSK-15-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-15-03 · ANON · tarea existente → 401 `auth/unauthorized`
  - TSK-15-04 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-15-05 · PROP · tarea `completed`, `reason: "falta foto"` → 200, `result: "rejected"`; la tarea queda `rejected` con `timeComplianceStatus: rejected`
  - TSK-15-06 · ADMIN → 200, `validatedByRole: "admin"`
  - TSK-15-07 · OP_MANAGER / OP_OWNER → 200
  - TSK-15-08 · OP_SUPERVISOR · `allowSupervisorValidation=true` → 200
  - TSK-15-09 · OP_SUPERVISOR · `allowSupervisorValidation=false` → 403 `task/unauthorized`
  - TSK-15-10 · OP_WORKER → 403 `task/unauthorized`
  - TSK-15-11 · AJENO → 403 `task/unauthorized`
  - TSK-15-12 · PROP · tarea `draft`, `assigned` o `in_progress` → 200 `rejected` (sin control de estado)
  - TSK-15-13 · PROP · tarea `in_progress` pausada → 200 `rejected`, con `pausedAt` y `pauseId` todavía abiertos
  - TSK-15-14 · PROP · tarea `validated` → 200 `rejected`, sin borrar `validatedAt`
  - TSK-15-15 · PROP · tarea `cancelled` → 200 `rejected`
  - TSK-15-16 · PROP · `reason: "   "` → 200, `rejectionReason: ""`
  - TSK-15-17 · EMP_INACTIVO · con nivel manager → 200
- Sospechas:
  - Se puede rechazar una tarea en cualquier estado (`:9-22`), mientras que validar exige `completed` (`CT/validateTask.controller.ts:17-19`).
  - El rechazo no cierra la pausa (`:36-44` usa `updateTaskUseCase`, no `updateClosingPause`). La pausa queda abierta, `pausedMs` no la suma nunca, y la tarea rechazada se puede reanudar (TSK-08-21).
  - El evento `task.rejected` publica el motivo (`events/task.ts:112-118`); el de pausas y el de notas lo omiten por posibles datos personales (`:74-78`, `:126-127`).

## POST /api/v1/tasks/:taskId/resources  ·  TSK-16
- Servicio: tasks, `taskRouter.ts:37` → `CT/uploadTaskResource.controller.ts:9-88`. Parser: `services/tasks/src/core/shared/utils/parseMultipartFormData.ts:3-57`. Storage: `services/tasks/src/core/shared/firebase/storage.ts:12-28`.
- Consumidores:
  - panel: `PSVC:362-390` (fetch multipart), llamado desde `PDET:218-226`
  - app: `ADS:457-504` y `AREPO:280`
- Origen: portado desde la CF `CF/uploadTaskResource.controller.ts`.
- Diferencias con la CF:
  - El parser lee el stream (`req.pipe(busboy)`, `:52`); la CF usaba `busboy.end(req.rawBody)` (`encodeBiz-SAAS/functions/src/core/shared/utils/parseMultipartFormData.ts:52`). El contrato es el mismo.
  - Añade el evento `task.resource_uploaded`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea, pero **después** de leer el multipart completo (`:11` va antes que `:28`).
- Autorización: `canOperateAssignedTask` (`:30`). No se exige jornada.
- Entrada (multipart):
  - Obligatorios: `entityId`, `branchId`, `type` y `file` (el campo del fichero se llama `file`).
  - Opcionales: `employeeId` y `description`.
  - Tipo MIME según `type`: `photo` admite jpeg, png y webp; **cualquier otro valor** de `type` admite mp4 y webm (`:34`).
  - Tamaño máximo según la config de la tarea: `maxPhotoSizeMB` o `maxVideoSizeMB`. nginx corta en 30 MB.
- Respuesta correcta: 201, el `TaskResource` con `url` (firmada hasta 2050-01-01), `storagePath` y `sizeKB`.
- Efectos:
  - Sube a Storage: `media/entities/{e}/checkinbiz/tasks/{t}/{ts}-{filename}`.
  - Crea `resources/{id}` y la actividad `resource_uploaded`.
  - Evento `task.resource_uploaded`, con la URL.
  - Notificación `task_resource_uploaded`.
- Criticidad: alta — son las evidencias, y `requireEvidenceOnCompletion` depende de ellas.
- Casos:
  - TSK-16-01 · ANON · body JSON (no multipart) → 500 `internal_error`: el parser rechaza antes de autenticar
  - TSK-16-02 · ANON · multipart sin `file` → 400 `task/bad_request`
  - TSK-16-03 · ANON · multipart sin `branchId` → 400 `task/bad_request`
  - TSK-16-04 · ANON · multipart completo, tarea inexistente → 404 `task/not_found`
  - TSK-16-05 · ANON · multipart completo, tarea existente → 401 `auth/unauthorized`
  - TSK-16-06 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-16-07 · OP_WORKER · asignado, foto jpeg de 1 MB → 201, `type: "photo"`, `employeeId` el suyo, URL firmada
  - TSK-16-08 · OP_WORKER · asignado, vídeo mp4 de 10 MB (`maxVideoSizeMB: 25`) → 201
  - TSK-16-09 · OP_WORKER · no asignado → 403 `task/unauthorized`
  - TSK-16-10 · OP_SUPERVISOR · no asignado → 201
  - TSK-16-11 · PROP · `employeeId: ""` (como manda el panel) → 201; `employeeId` es su ficha o no aparece
  - TSK-16-12 · ADMIN → 201
  - TSK-16-13 · AJENO → 403 `task/unauthorized`
  - TSK-16-14 · OP_WORKER · `type: "photo"` con `image/gif` → 400 `task/invalid_mime_type`
  - TSK-16-15 · OP_WORKER · `type: "video"` con `video/quicktime` → 400 `task/invalid_mime_type`
  - TSK-16-16 · OP_WORKER · foto de 6 MB con `maxPhotoSizeMB: 5` → 400 `task/file_too_large`
  - TSK-16-17 · OP_WORKER · foto de 6 MB con `maxPhotoSizeMB: 10` → 201
  - TSK-16-18 · OP_WORKER · vídeo de 26 MB con `maxVideoSizeMB: 25` → 400 `task/file_too_large`
  - TSK-16-19 · OP_WORKER · fichero de más de 30 MB → 413 de nginx (no llega al servicio)
  - TSK-16-20 · OP_WORKER · `type: "documento"` con `video/mp4` → 201, se guarda `type: "documento"`
  - TSK-16-21 · OP_WORKER · `employeeId` de otro empleado → 201, el recurso queda atribuido al otro
  - TSK-16-22 · OP_WORKER · `branchId` distinto del de la tarea → 201 (el del body se ignora; manda el de la tarea)
  - TSK-16-23 · OP_WORKER · el fichero va en el campo `image` en vez de `file` → 400 `task/bad_request`
  - TSK-16-24 · OP_WORKER · tarea `validated` o `cancelled` → 201 (no hay restricción de estado)
  - TSK-16-25 · OP_WORKER · asignado, sin jornada abierta → 201
  - TSK-16-26 · EMP_INACTIVO · asignado → 201
- Sospechas:
  - `employeeId` es libre (`:14,58`): cualquiera que opere la tarea puede atribuir una evidencia a otro empleado.
  - `type` es libre (`:15,34`) y se guarda sin validar.
  - Un content-type que no es multipart da 500 en vez de 400 (`parseMultipartFormData.ts:9-11` y `app.ts:27-30`).
  - El fichero se carga entero en memoria antes de autenticar (`:11`), hasta 30 MB por petición anónima.
  - La URL de lectura es válida hasta 2050 (`storage.ts:24`) y además viaja en el evento (`events/task.ts:141`).

## POST /api/v1/tasks/:taskId/ratings  ·  TSK-17
- Servicio: tasks, `taskRouter.ts:38` → `CT/rateTaskWorker.controller.ts:8-103`.
- Consumidores:
  - panel: `PSVC:314-360`, JSON o multipart con el campo `image`, llamado desde `PDET:210-216`
  - app: `ADS:402-454` y `AREPO:253`
- Origen: portado desde la CF `CF/rateTaskWorker.controller.ts`.
- Diferencias con la CF:
  - `ratedByRole` ya no se normaliza. La CF convertía en `"owner"` cualquier rol que no fuera supervisor, manager u owner (`CF/task.helpers.ts:185-187`); el contenedor guarda el rol tal cual (`H:244-246`), así que ahora pueden salir `"admin"` y `"worker"`.
  - El panel tipa `ratedByRole` como `Exclude<ResponsibilityKey,"worker">` (`encodebiz-front-saas/src/domain/features/checkinbiz/ITask.ts:182`), sin `"admin"`. La app lo trata como `String?` (`checkbiz360/lib/features/task/data/models/task_model.g.dart:284`).
  - Añade el evento `task.worker_rated`.
- Autenticación: `resolveTaskActor` con el `branchId` de la tarea. Antes se comprueban el empleado asignado y el rango de la nota (`:22-29`).
- Autorización: `canRateTask` (`:33`), y solo el autor original puede cambiar una valoración existente (`:38-42`).
- Entrada: JSON o multipart.
  - Obligatorios: `entityId`, `employeeId` (tiene que estar en `assignedEmployeeIds`) y `rating`, entero de 1 a 5.
  - Opcionales: `comment` y una imagen en `image` o `file` (jpeg, png o webp, hasta `maxPhotoSizeMB`).
- Respuesta correcta: 200, la `TaskRating`.
- Efectos:
  - Si hay imagen, la sube a Storage (`.../ratings/{employeeId}-{ts}-{filename}`).
  - Upsert con merge de `ratings/{employeeId}`.
  - Actividad `rated`.
  - Evento `task.worker_rated`, que incluye el comentario.
  - Notificación `task_worker_rated` al valorado.
  - Dispara dos triggers CF: `onWriteTaskRating` (EmployeePattern) y `onTaskRatingSync` (analítica) (`firebase-firestore-trigger/onWriteTaskRating.ts:113-114` y `onTaskRatingSync.ts:5-6`).
- Criticidad: media.
- Casos:
  - TSK-17-01 · ANON · sin `rating` → 400 `task/bad_request`
  - TSK-17-02 · ANON · tarea inexistente → 404 `task/not_found`
  - TSK-17-03 · ANON · `employeeId` no asignado → 400 `task/bad_request` («Employee is not assigned to this task»), sin autenticar
  - TSK-17-04 · ANON · `rating: 6` → 400 `task/bad_request`, sin autenticar
  - TSK-17-05 · ANON · petición válida → 401 `auth/unauthorized`
  - TSK-17-06 · TOKEN_INVALIDO → 401 `auth/unauthorized`
  - TSK-17-07 · PROP · JSON con `rating: 4` → 200, `rating: 4`, `ratedByRole: "owner"`
  - TSK-17-08 · ADMIN → 200, `ratedByRole: "admin"` (la CF devolvía `"owner"`)
  - TSK-17-09 · PROP+EMP · con responsabilidad de worker en la sucursal → 200, `ratedByRole: "worker"`
  - TSK-17-10 · OP_MANAGER / OP_OWNER → 200, `ratedByRole` `manager` / `owner`
  - TSK-17-11 · OP_SUPERVISOR · `allowSupervisorRating=true` → 200, `ratedByRole: "supervisor"`
  - TSK-17-12 · OP_SUPERVISOR · `allowSupervisorRating=false` → 403 `task/unauthorized`
  - TSK-17-13 · OP_WORKER · asignado, valora a un compañero → 403 `task/unauthorized`
  - TSK-17-14 · AJENO → 403 `task/unauthorized`
  - TSK-17-15 · PROP · multipart con `rating: "4"` → 200, `rating: 4`
  - TSK-17-16 · PROP · `rating` 4.5, 0 o `"abc"` → 400 `task/bad_request` («rating must be an integer between 1 and 5»)
  - TSK-17-17 · PROP · multipart con imagen png de 1 MB → 200, con `image: {url, storagePath, sizeKB}`
  - TSK-17-18 · PROP · imagen gif → 400 `task/invalid_mime_type`
  - TSK-17-19 · PROP · imagen de 6 MB con `maxPhotoSizeMB: 5` → 400 `task/file_too_large`
  - TSK-17-20 · PROP · imagen en el campo `file` → 200 (se acepta `image` o `file`)
  - TSK-17-21 · PROP · vuelve a valorar al mismo empleado → 200, se sobrescribe el mismo documento
  - TSK-17-22 · ADMIN · cambia una valoración hecha por PROP → 403 `task/rating_author_mismatch`
  - TSK-17-23 · PROP · valora a un empleado ya retirado → 400 `task/bad_request`
  - TSK-17-24 · PROP · tarea `in_progress` o `draft` → 200 (no hay control de estado)
  - TSK-17-25 · PROP · multipart mal formado → sin confirmar: 500 `internal_error`
  - TSK-17-26 · EMP_INACTIVO · con nivel manager → 200
- Sospechas:
  - Se puede valorar trabajo que no ha terminado (no hay control de estado).
  - Comprobar la asignación antes de autenticar permite a ANON saber si un empleado está asignado a una tarea (`:22-24`).
  - `ratedByRole` puede valer `"admin"` o `"worker"`, valores que el tipo del panel no contempla. Sin confirmar cómo los pinta.
  - El evento publica el comentario de la valoración (`events/task.ts:151-158`), a diferencia de notas y pausas.

## POST /api/v1/tasks/system  ·  TSK-18
- Servicio: tasks. Montado en `app.ts:22` detrás de `requireApiKey`, con `systemTaskRouter.ts:7` → `CT/createSystemTask.controller.ts:54-234`. Por nginx es accesible desde fuera (entra por `location /api/v1/tasks/`); solo la protege la clave.
- Consumidores:
  - S2S: `services/rentman/src/infrastructure/HttpTasksClient.ts:58-95`, que manda la config fija de `:45-56` y lee `body.task?.id ?? body.id` y `body.code`.
  - S2S: la herramienta de demo `services/merlin/src/soporte/puesta-en-marcha/demo/sad/montar.cli.ts:159`.
  - Ni el panel ni la app.
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: cabecera `x-encodebiz-key` igual a `ENCODEBIZ_API_KEY` (`packages/shared/src/middleware/apiKeyAuth.ts:4-9`). El actor se resuelve desde `actorUid` con `resolveActorByUid` (`H:115-147`): mismas reglas que el camino Firebase, pero sin JWT.
- Autorización: `canManageTask(actor, config del body)` (`:91`). Un actor sin rol ni responsabilidad → 403 «Actor cannot manage this entity» (`:87-90`).
- Entrada:
  - Obligatorios: `entityId`, `branchId`, `title`, `dueAt` y `actorUid`.
  - `config`, obligatorio salvo que la tarea ya exista por `externalRef`.
  - Opcionales: `description`, `scheduledStartAt`, `priority`, `assignedEmployeeIds` (**no se rechaza a los inválidos**), `externalRef`, `source` y `workSite`.
- Respuesta correcta:
  - 201, el `Task` creado.
  - 200, la tarea ya existente si `externalRef` coincide (`:73-79`).
- Efectos:
  - Igual que TSK-02, más `metadata`: `externalRef`, `source` y `staffing` cuando hay bloqueados (`:42-52,123-132`).
  - Crea asignaciones para **todos** los asignados, también los bloqueados.
  - Estado `assigned` si al menos uno es asignable; si no, `draft` (`:158`).
- Criticidad: media — la importación de add-ons (Rentman) depende de ella.
- Casos:
  - TSK-18-01 · ANON · sin `x-encodebiz-key` → 401 `{ok:false, error:"unauthorized"}`, sin `code`
  - TSK-18-02 · S2S · clave incorrecta → 401 `{ok:false, error:"unauthorized"}`
  - TSK-18-03 · S2S · falta `actorUid` → 400 `task/bad_request`
  - TSK-18-04 · S2S · falta `dueAt` → 400 `task/bad_request`
  - TSK-18-05 · S2S(actorUid=ADMIN) · body completo, sin `externalRef`, 2 asignados activos → 201. `status: assigned`, sin `metadata.staffing`, actividad con `actorRole: "admin"`
  - TSK-18-06 · S2S(actorUid=PROP) · `externalRef` nuevo y `source: {addon, …}` → 201, con `metadata: {externalRef, source}`
  - TSK-18-07 · S2S(actorUid=PROP) · repite el mismo `externalRef` → 200 con la tarea existente; no crea nada
  - TSK-18-08 · S2S(actorUid=AJENO) · `externalRef` existente y config inválida → 200 con la existente: la idempotencia va antes de validar la config y el actor
  - TSK-18-09 · S2S(actorUid=PROP) · sin `config` → 400 `task/bad_request` `["config is required"]`
  - TSK-18-10 · S2S(actorUid=uid inexistente o sin rol ni ficha) → 403 `task/unauthorized` («Actor cannot manage this entity»)
  - TSK-18-11 · S2S(actorUid=OP_SUPERVISOR (Firebase)) · `allowSupervisorCreation=false` → 403 `task/unauthorized` («Unauthorized»)
  - TSK-18-12 · S2S(actorUid=OP_SUPERVISOR (Firebase)) · `allowSupervisorCreation=true` → 201
  - TSK-18-13 · S2S(actorUid=OP_WORKER (Firebase)) → 403 `task/unauthorized`
  - TSK-18-14 · S2S(actorUid=AJENO) · `externalRef` nuevo → 403 `task/unauthorized` («Actor cannot manage this entity»)
  - TSK-18-15 · S2S(actorUid=PROP) · sucursal inexistente → 404 `task/branch_not_found`
  - TSK-18-16 · S2S(actorUid=PROP) · sucursal inactiva → 400 `task/branch_inactive` (Rentman lo interpreta como «esperar»)
  - TSK-18-17 · S2S(actorUid=PROP) · `dueAt` inválido → 400 `task/bad_request`
  - TSK-18-18 · S2S(actorUid=PROP) · todos los asignados inactivos → 201. `status: draft`, `assignedEmployeeIds` con todos, `metadata.staffing: {assigned, ready: 0, blocked, status: "no_active_staff"}`, asignaciones creadas para todos
  - TSK-18-19 · S2S(actorUid=PROP) · asignados en parte válidos → 201, `status: assigned`, `staffing.status: "partial"`
  - TSK-18-20 · S2S(actorUid=PROP) · `workSite: {geo}` → 201 con `workSite`
  - TSK-18-21 · S2S(actorUid=PROP) · `workSite` inválido → 400 `task/worksite_invalid`
  - TSK-18-22 · S2S(actorUid=ADMIN) · `priority: "urgent"` → 201 sin `priority`
  - TSK-18-23 · ANON · `GET /api/v1/tasks/system` → 401 `{ok:false, error:"unauthorized"}` (el middleware cubre cualquier método bajo `/system`)
- Sospechas:
  - La idempotencia responde antes de validar el actor (`:73-79`): con la clave, cualquier `actorUid` obtiene cualquier tarea de la entidad si conoce su `externalRef`. El riesgo es bajo porque la clave es interna, pero la ruta está publicada por nginx.
  - Los empleados bloqueados quedan en `assignedEmployeeIds` y reciben asignación (`:163,180-194`). Si un bloqueado tiene EMP_JWT, puede operar la tarea (OP_OTRA_SUCURSAL por JWT, nivel 1 + asignado).
  - `findByExternalRef` no es transaccional (`REPO:117-125`). Dos pasadas simultáneas pueden duplicar la tarea; sin confirmar.
  - El 401 tiene otra forma que el resto (`{ok, error}`, sin `code`).

## GET /health  ·  TSK-19
- Servicio: tasks, `app.ts:17`.
- Consumidores: ninguno detectado. nginx no lo enruta al servicio: `location = /health` responde el propio nginx (`nginx/nginx.staging.conf:55-58`).
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: ninguna.
- Autorización: ninguna.
- Entrada: ninguna.
- Respuesta correcta: 200 `{ok: true, service: "tasks"}`.
- Efectos: ninguno.
- Criticidad: baja.
- Casos:
  - TSK-19-01 · ANON · `GET http://tasks:3006/health` desde la red de contenedores → 200 `{ok:true, service:"tasks"}`
  - TSK-19-02 · ANON · `GET http://141.95.47.135:8080/health` → 200 `{"ok":true,"service":"nginx","env":"staging"}`: responde nginx, no el servicio, así que no sirve como sonda de `tasks`
- Sospechas: ninguna.

## * /api/v1/tasks/* (transversal: rutas desconocidas y errores)  ·  TSK-20
- Servicio: tasks, `app.ts:12` (CORS), `app.ts:15` (`express.json` con límite de 10 MB), `app.ts:25` (404) y `app.ts:27-30` (manejador de errores). Usa `express-async-errors` (`app.ts:6`).
- Consumidores: todos.
- Origen: nativo del contenedor.
- Diferencias con la CF:
  - La CF no instala `express-async-errors` (búsqueda sin resultados en `encodeBiz-SAAS/functions/src`) ni manejadores 404 o de error propios (`firebase-checkinbiz-http/tasks.ts:6-11`). Allí una ruta desconocida recibe el 404 por defecto de Express, en HTML, y un error asíncrono deja la petición sin respuesta hasta el timeout; sin confirmar el código exacto.
  - La CF limita CORS a `ALLOWED_WEB_ORIGINS`; el contenedor usa `cors()` abierto.
- Autenticación: no aplica.
- Autorización: no aplica.
- Entrada: no aplica.
- Respuesta correcta: no aplica.
- Efectos: ninguno.
- Criticidad: media — define qué ve un cliente ante cualquier fallo.
- Casos:
  - TSK-20-01 · PROP · `GET /api/v1/tasks/abc/xyz` → 404 `{ok:false, error:"not_found"}`
  - TSK-20-02 · PROP · `DELETE /api/v1/tasks/:taskId` (método sin ruta) → 404 `{ok:false, error:"not_found"}`
  - TSK-20-03 · PROP · `POST /api/v1/tasks/` con JSON mal formado → 500 `{ok:false, error:"internal_error"}` (el 400 de body-parser se pierde en `app.ts:27-30`)
  - TSK-20-04 · PROP · body JSON de más de 10 MB y menos de 30 MB → 500 `{ok:false, error:"internal_error"}`
  - TSK-20-05 · PROP · error de Firestore no controlado (por ejemplo, falta un índice) → 500 `{ok:false, error:"internal_error"}`
  - TSK-20-06 · PROP · token de Firebase válido, pero Firestore falla durante la resolución del actor → 401 `auth/unauthorized`, porque cae al camino JWT (`H:187-189`). Sin confirmar que se pueda reproducir.
  - TSK-20-07 · ANON · `OPTIONS` de preflight desde un origen cualquiera → 204 con `Access-Control-Allow-Origin: *`
- Sospechas:
  - Los errores del cliente (JSON mal formado, cuerpo demasiado grande, multipart ausente en TSK-16) salen como 500 en vez de 4xx (`app.ts:27-30`).
  - Un error de infraestructura durante la autenticación se presenta como 401 (`H:187-189`).

---

## Resumen
- Endpoints: 19 (18 rutas de routers y `/health`), más un bloque transversal (TSK-20).
  - Consumidos por clientes: 14. Por el panel, 11: TSK-02, 05, 06, 09, 10, 11, 12, 14, 15, 16 y 17. Por la app, 12: TSK-02, 05, 07, 08, 09, 10, 11, 12, 14, 15, 16 y 17. Por S2S, 1: TSK-18.
  - Sin consumidor detectado: TSK-01, 03, 04, 13 y 19. El panel y la app leen tareas directamente de Firestore.
- Casos: 427.
- Diferencias con Cloud Functions que pueden romper a un cliente:
  - `PATCH /status` a `in_progress` o `completed` exige jornada abierta a todo empleado que no sea PROP ni ADMIN → 400 `task/no_open_session` (`CT/updateTaskStatus.controller.ts:51-52`). La CF no lo exigía.
  - Geocerca en `PATCH /status` y en `/resume`: con `workSite`, `geo` es obligatorio para **cualquier** actor → 400 `task/geo_required`. Iniciar o reanudar fuera de la valla → 400 `task/out_of_worksite`. El panel no manda `geo`, así que PROP y ADMIN ya no pueden iniciar ni completar desde el panel una tarea con lugar de trabajo; una app que no envíe `geo` tampoco.
  - Roles registrados: ADMIN aparece como `"admin"` en `actorRole`, `createdByRole`, `validatedByRole` y `startedByRole`, donde la CF ponía `"owner"` (`CF/task.helpers.ts:128`). `ratedByRole` ya no se normaliza (`CF/task.helpers.ts:185-187`), así que pueden salir `"admin"` y `"worker"`. Los tipos del panel no incluyen `"admin"` (`ITask.ts:137,182,196`); sin confirmar cómo lo pinta.
  - Rutas que solo existen en el contenedor: duplicar, pausar, reanudar y sistema. En un rollback a la CF, el panel pierde duplicar, la app pierde pausar y reanudar, y la CF no cierra las pausas abiertas al completar.
  - Errores: el contenedor devuelve 404 y 500 en JSON `{ok:false}`, y un JSON mal formado da 500. En la CF: 404 en HTML, 400 por defecto de Express y peticiones colgadas en errores asíncronos (sin confirmar).
  - Cambio que no rompe: reabrir una tarea borra de verdad los sellos; la CF los dejaba como `{}`.
- Sospechas principales:
  - La máquina de estados no controla el origen. `PATCH /status` acepta `in_progress`, `completed`, `cancelled`, `assigned` y `draft` desde cualquier estado, y `POST /rejection` rechaza en cualquier estado: un trabajador puede completar o reiniciar tareas validadas, canceladas o rechazadas.
  - `completionPolicy: all_assigned_workers` no se aplica: el primer asignado que completa cierra la tarea para todos.
  - EMP_INACTIVO sigue operando: el JWT del empleado no caduca y `resolveTaskActor` no mira `employee.status`.
  - Un supervisor que lista sin `branchId` ve las tareas de todas las sucursales de la entidad.
  - `allowSupervisorCreation` se evalúa sobre la config que manda el propio creador. Además, `PATCH` con `config` reemplaza la config entera y permite a un supervisor gestor concederse validar y valorar.
  - Pausas:
    - iniciar una tarea pausada no reanuda y deja la pausa abierta;
    - rechazar no cierra la pausa;
    - reanudar no mira el estado de la tarea.
  - Asignaciones:
    - iniciar o completar crea asignaciones fantasma del actor no asignado;
    - reenviar a un asignado reinicia su estado a `assigned`;
    - la notificación de asignación se espera con `await` y puede dar 500 con la asignación ya escrita.
  - Reabrir a `assigned` conserva los sellos de validación y rechazo; `scheduledStartAt: null` no vacía el campo.
  - La geocerca exige `geo` también a PROP y ADMIN, en contra de la exención de back office.
  - Comprobaciones antes de autenticar filtran información a ANON: existencia (404), estado (`task/invalid_status`) y asignación (`ratings`). Errores del cliente salen como 500.
  - Ante el 403 de `H:170`, `resolveTaskActor` devuelve el objeto `Response` en vez de `null`. El controlador sigue y responde dos veces (`ERR_HTTP_HEADERS_SENT`).
  - Recursos: `employeeId` y `type` son libres, y la URL de lectura dura hasta 2050 y viaja en el evento.

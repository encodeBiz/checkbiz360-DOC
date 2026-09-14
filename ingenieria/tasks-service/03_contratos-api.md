# 03 — Contratos de API

**Base:** `https://<host>/api/v1/tasks`
**Auth:** cabecera `Authorization: Bearer <token>` — Firebase ID token (back office) o staff JWT (app). El actor y su nivel se resuelven en `resolveTaskActor` (ver [TDR-002](./tdr/TDR-002-resolucion-actor-y-permisos.md)).
**Contrato preservado:** request/response idénticos a los del `tasksHandler` actual en Firebase. Esta migración **no** cambia el contrato; solo cambia el host que lo sirve.

> Nota: bajo `tasksHandler` el router se monta en `/tasks`; en el servicio se monta en `/api/v1/tasks`. La ruta relativa de cada endpoint (`/`, `/:taskId`, …) es la misma.

---

## Tareas

### `GET /` — listar tareas
Query: `entityId` (obligatorio), `branchId?`, `status?`, `timeComplianceStatus?`, `employeeId?`, `from?`, `to?`, `limit?`.
Scoping: un actor con `level < supervisor` (y no entityWriter) solo ve sus tareas (`employeeId` forzado).
`200` → `Task[]`. `400` si falta `entityId`.

### `POST /` — crear tarea
Permiso: `canManageTask`.
Body: `entityId`, `branchId`, `title`, `description?`, `priority?`, `scheduledStartAt?`, `dueAt`, `assignedEmployeeIds?`, `config` (`TaskConfig`), `workSite?` (`TaskWorkSite`, ver [TDR-005](./tdr/TDR-005-worksite-y-geocerca-de-tarea.md) §2).
Efectos: crea la tarea (`status: draft|assigned`), asignaciones iniciales, actividad `created`; si `config.notifyIfNotStarted` y hay `scheduledStartAt`, calcula `scheduledStartNotificationAt` (+15 min).
`201` → `TaskDetail`. `400` config/prioridad inválida. `404` branch inexistente. `403` sin permiso.

### `POST /:taskId/duplicate` — duplicar tarea
Permiso: `canManageTask` (sobre la `config` del original).
Body: `entityId`, `dueAt` (obligatorio), `scheduledStartAt?`, `title?` (por defecto, el del original + `" (copia)"`).
Copia el encargo: `branchId`, `description`, `priority`, `config` (normalizada por `validateTaskConfig`) y `workSite` **literal**, sin volver a resolverlo —re-resolverlo llamaría a Google por el `placeId` y podría mover la valla—.
No copia: asignaciones, evidencias, notas, valoraciones, historial ni `metadata` (`externalRef` es la clave de idempotencia del add-on; duplicarla rompería la sincronización).
Efectos: crea la tarea en `status: draft` con `assignedEmployeeIds: []`, actividad `created` con `metadata.duplicatedFrom`, evento `task.created`. Sin notificación: no hay nadie a quien avisar hasta que se asigne.
`201` → `TaskDetail`. `400` falta `dueAt` o es inválido; `404` original inexistente; `400` `task/source_config_invalid` si la `config` del original no es usable.

### `GET /:taskId` — detalle
Permiso: `canViewTask`.
`200` → `TaskDetail` = `{ task, assignments, notes, resources, ratings, activity, validations }`. `404` si no existe.

### `GET /:taskId/activity` — historial de actividad
Permiso: `canViewTask`.
Query: `limit?`.
`200` → `TaskActivity[]` (orden descendente por fecha).

### `PATCH /:taskId` — actualizar tarea
Permiso: `canManageTask`.
Body: campos editables (`title`, `description`, `priority`, `scheduledStartAt`, `dueAt`, `config`, `workSite`, …).
`workSite: null` borra la geocerca de la tarea.
Efectos: `update` + actividad `updated`. `200` → `TaskDetail`.

### `PATCH /:taskId/status` — cambiar estado
Permiso: `canOperateAssignedTask` (worker asignado puede iniciar/completar; supervisor+ según flujo).
Body: `status` (`TaskStatus`) + campos de transición + `geo?` (`{lat, lng}`).
Efectos: aplica la transición (`started`/`completed`/…), sella `startedAt`/`completedAt`, recalcula `timeComplianceStatus` (`computeCompletionStatus`), actividad `status_changed`.
`200` → `TaskDetail`. `400` transición inválida. `403` sin permiso.

**Precondiciones para `in_progress` y `completed`** (ver [TDR-005](./tdr/TDR-005-worksite-y-geocerca-de-tarea.md)):

1. **Jornada abierta.** El actor empleado necesita un check-in válido sin cerrar. Exento el actor de back office (`isEntityWriter`). Sin ella → `400 task/no_open_session`. La app ya lo impedía por su cuenta; ahora también el servidor.
2. **Geocerca de la tarea**, solo si `task.workSite` existe:
   - falta `geo` → `400 task/geo_required`
   - al **iniciar**, fuera de radio → `400 task/out_of_worksite` con `{distanceMeters, allowedRadiusMeters}`; el estado no cambia y queda actividad `start_rejected`.
   - al **completar**, la distancia se registra pero **no bloquea**.

Una tarea sin `workSite` no tiene comprobación geográfica: la valla que le corresponde es la de su sucursal, ya aplicada en el check-in que la precondición 1 exige.

---

### `POST /:taskId/pause` — pausar
Permiso: `canOperateAssignedTask` (asignado, o supervisor en adelante).
Body: `entityId`, `reason?` (texto libre), `geo?` (se guarda, no se juzga).
**Sin precondiciones de jornada ni geocerca**: se pausa precisamente cuando uno se va (ver [08_pausas.md](./08_pausas.md), D5).
Efectos, en una transacción sobre la tarea: abre `pauses/{pauseId}`, sella `pausedAt`, `pausedBy`, `pauseId` y suma 1 a `pauseCount`. La tarea **sigue `in_progress`** (D2). Actividad `paused`; evento `task.paused` (sin el motivo, que puede llevar datos personales).
`200` → `Task`. `400` `task/not_in_progress` o `task/already_paused`. `403` sin permiso. `404` inexistente.

### `POST /:taskId/resume` — reanudar
Permiso: `canOperateAssignedTask`.
Body: `entityId`, `geo?` (obligatorio si la tarea tiene `workSite`).
**Mismas precondiciones que iniciar**: jornada abierta (salvo back office) y, con `workSite`, estar dentro de la valla. Fuera de ella se rechaza y queda actividad `resume_rejected`, igual que `start_rejected` al iniciar.
Efectos, en una transacción: cierra la pausa (`endedReason: resumed`, `durationMs`), suma su duración a `pausedMs` y borra `pausedAt`/`pausedBy`/`pauseId`. Actividad `resumed`; evento `task.resumed` con `pause_duration_ms`.
`200` → `Task`. `400` `task/not_paused`, `task/no_open_session`, `task/geo_required` o `task/out_of_worksite`. `403` sin permiso. `404` inexistente.

**Cambios de estado con una pausa abierta** (`PATCH /:taskId/status`): `completed` y `cancelled` la cierran en la misma transacción que el cambio (`endedReason` con el estado); `assigned` y `draft` la cierran como `reset` y ponen `pausedMs` y `pauseCount` a cero (D4, D8).

---

## Asignaciones

### `POST /:taskId/assignments` — asignar trabajadores
Permiso: `canAssignTaskWorkers`.
Body: `employeeIds: string[]`.
Valida empleados asignables (activos y con responsabilidad en la branch — `validateAssignableEmployees`). `upsertAssignments` + actividad `assigned`.
`200` → `TaskDetail`. `400` empleados inválidos.

### `DELETE /:taskId/assignments/:employeeId` — desasignar
Permiso: `canAssignTaskWorkers`.
Marca la asignación `removed` (`removedAt`) y actualiza `assignedEmployeeIds`. `200` → `TaskDetail`.

---

## Notas

### `POST /:taskId/notes` — añadir nota
Permiso: `canAddTaskNote`.
Body: `content`, `type` (`specification|operational_note|clarification|incident_note`).
`createNote` (sella `createdByRole`) + actividad `note_added`. `201` → `TaskNote`.

### `PATCH /:taskId/notes/:noteId` — editar nota
Permiso: autor o `level ≥ supervisor` (según regla del controlador).
Body: `content`. `updateNote` + actividad `note_updated`. `200` → `TaskNote`.

---

## Validación y rechazo

### `POST /:taskId/validation` — validar
Permiso: `canValidateOrRejectTask`.
Efectos: `createValidation(result: "validated")`, `status → validated`, `validatedAt/By`, actividad `validated`.
`200` → `TaskDetail`.

### `POST /:taskId/rejection` — rechazar
Permiso: `canValidateOrRejectTask`.
Body: `reason`.
Efectos: `createValidation(result: "rejected")`, `status → rejected`, `rejectedAt/By`, `rejectionReason`, actividad `rejected`.
`200` → `TaskDetail`.

---

## Evidencias y valoraciones

### `POST /:taskId/resources` — subir evidencia  *(multipart/form-data)*
Permiso: `canOperateAssignedTask`.
Form: fichero (`photo`/`video`) + `description?`.
Valida tipo/tamaño contra `TaskConfig`, sube a Storage, `createResource`, actividad `resource_uploaded`. Ver [TDR-003](./tdr/TDR-003-storage-evidencias-y-multipart.md).
`201` → `TaskResource`. `400` tipo/tamaño inválido.

### `POST /:taskId/ratings` — valorar a un trabajador
Permiso: `canRateTask`.
Body: `employeeId`, `rating` (1–5), `comment?`, `image?` (opcional, multipart).
`upsertRating` (uno por empleado, sella `ratedByRole`) + actividad `rated`.
`200` → `TaskRating`. `403` sin permiso.

---

## Códigos de error comunes

| Código | HTTP | Significado |
|---|---|---|
| `task/bad_request` | 400 | Falta parámetro obligatorio |
| `task/unauthorized` | 403 | Token inválido o sin nivel suficiente |
| `task/branch_not_found` | 404 | Branch inexistente |
| `task/branch_inactive` | 400 | Branch no activa |
| `task/source_config_invalid` | 400 | La `config` de la tarea que se duplica no es usable |
| `task/not_in_progress` | 400 | Solo se puede pausar una tarea en curso |
| `task/already_paused` | 400 | La tarea ya está pausada |
| `task/not_paused` | 400 | Se pide reanudar una tarea que no está pausada |
| `task/employee_not_found` | 404 | Empleado del staff JWT inexistente |
| `task/no_open_session` | 400 | El empleado no tiene jornada abierta |
| `task/geo_required` | 400 | La tarea tiene `workSite` y el body no trae `geo` |
| `task/out_of_worksite` | 400 | Fuera del radio del lugar de trabajo de la tarea |
| `task/worksite_invalid` | 400 | `workSite` mal formado o dirección no resoluble |
| `task/worksite_imprecise` | 400 | Geocodificación con precisión `approximate` (no vale para una valla) |

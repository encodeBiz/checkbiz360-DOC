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
Body: `entityId`, `branchId`, `title`, `description?`, `priority?`, `scheduledStartAt?`, `dueAt`, `assignedEmployeeIds?`, `config` (`TaskConfig`).
Efectos: crea la tarea (`status: draft|assigned`), asignaciones iniciales, actividad `created`; si `config.notifyIfNotStarted` y hay `scheduledStartAt`, calcula `scheduledStartNotificationAt` (+15 min).
`201` → `TaskDetail`. `400` config/prioridad inválida. `404` branch inexistente. `403` sin permiso.

### `GET /:taskId` — detalle
Permiso: `canViewTask`.
`200` → `TaskDetail` = `{ task, assignments, notes, resources, ratings, activity, validations }`. `404` si no existe.

### `GET /:taskId/activity` — historial de actividad
Permiso: `canViewTask`.
Query: `limit?`.
`200` → `TaskActivity[]` (orden descendente por fecha).

### `PATCH /:taskId` — actualizar tarea
Permiso: `canManageTask`.
Body: campos editables (`title`, `description`, `priority`, `scheduledStartAt`, `dueAt`, `config`, …).
Efectos: `update` + actividad `updated`. `200` → `TaskDetail`.

### `PATCH /:taskId/status` — cambiar estado
Permiso: `canOperateAssignedTask` (worker asignado puede iniciar/completar; supervisor+ según flujo).
Body: `status` (`TaskStatus`) + campos de transición.
Efectos: aplica la transición (`started`/`completed`/…), sella `startedAt`/`completedAt`, recalcula `timeComplianceStatus` (`computeCompletionStatus`), actividad `status_changed`.
`200` → `TaskDetail`. `400` transición inválida. `403` sin permiso.

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
| `task/employee_not_found` | 404 | Empleado del staff JWT inexistente |

# Módulo Task — Gestión de Tareas Operativas

> Fuente única de verdad para backend, backoffice y app móvil.
> Incluye las últimas actualizaciones de permisos (canManageTask unificado, supervisor con acceso a notas/recursos sin asignación).

## 1. Resumen

El módulo de gestión de tareas permite crear, asignar, ejecutar, completar, validar, rechazar y valorar tareas operativas vinculadas a una entidad, sucursal y equipo de trabajadores.

Se integra como una sección del backoffice de CheckBiz y como un tab en la app móvil. No es una herramienta aislada.

## 2. Roles y Permisos

El módulo no inventa roles nuevos. Usa `EmployeeResponsibility`.

```typescript
worker     = 1
supervisor = 2
manager    = 3
owner      = 4
```

### Owner / Manager

Administradores del módulo. Permisos completos:
- Crear, editar, cancelar tareas
- Asignar y desasignar trabajadores
- Validar y rechazar tareas
- Valorar trabajadores
- Agregar notas y subir recursos en cualquier tarea

### Supervisor

- Crear tareas si `config.allowSupervisorCreation = true`
- Editar, cancelar y cambiar estado si `allowSupervisorCreation = true`
- Validar y rechazar si `config.allowSupervisorValidation = true`
- Valorar trabajadores si `config.allowSupervisorRating = true`
- **Agregar notas en cualquier tarea de su sucursal — sin necesidad de estar asignado**
- **Subir recursos/evidencias en cualquier tarea de su sucursal — sin necesidad de estar asignado**
- Ver tareas de su sucursal

> Un supervisor puede gestionar dos sucursales a la vez sin autoasignarse a las tareas. Las acciones sobre notas y recursos no requieren config adicional — siempre permitidas para level >= supervisor.

### Worker

- Ver tareas asignadas
- Marcar `in_progress` y `completed`
- Subir evidencias si está asignado
- Agregar notas si está asignado

### Regla de notas y recursos

Puede crear nota o subir recurso quien sea:
- Empleado asignado a la tarea
- Supervisor (cualquier tarea de su sucursal)
- Manager
- Owner

## 3. Configuración

### Por tarea (`TaskConfig`)

```typescript
interface TaskConfig {
  allowSupervisorCreation: boolean;
  allowSupervisorValidation: boolean;
  allowSupervisorRating: boolean;
  completionPolicy: "any_assigned_worker" | "all_assigned_workers";
  requireEvidenceOnCompletion: boolean;
  maxPhotoSizeMB: number;   // default 5
  maxVideoSizeMB: number;   // default 25
}
```

Decisión actual: `completionPolicy: "any_assigned_worker"`.

## 4. Máquina de Estados

### Estado principal

```
draft → assigned → in_progress → completed → validated
                       │               │
                       └──────────────►└──► rejected → in_progress
                  cancelled (desde cualquier estado, manager+)
```

Estados soportados en la API actual: `draft`, `in_progress`, `completed`, `cancelled`.

### Subestado temporal (`TimeComplianceStatus`)

```typescript
type TimeComplianceStatus =
  | "not_started"
  | "on_time"
  | "at_risk"          // < 20% tiempo restante
  | "overdue"
  | "completed_on_time"
  | "completed_late";
```

### Estado por asignación (`TaskAssignment.status`)

```
assigned → accepted → working → completed
                              → blocked
                    removed
```

## 5. Modelo de Dominio

### Task

```typescript
interface Task {
  id?: string;
  entityId: string;
  branchId: string;
  title: string;
  description?: string;
  status: "draft" | "assigned" | "in_progress" | "completed" | "validated" | "rejected" | "cancelled";
  timeComplianceStatus: TimeComplianceStatus;
  priority?: "low" | "medium" | "high" | "critical";
  scheduledStartAt?: Date;
  dueAt: Date;
  startedAt?: Date;
  completedAt?: Date;
  validatedAt?: Date;
  rejectedAt?: Date;
  cancelledAt?: Date;
  createdBy: string;
  updatedBy?: string;
  completedBy?: string;
  validatedBy?: string;
  rejectedBy?: string;
  cancelledBy?: string;
  rejectionReason?: string;
  cancellationReason?: string;
  assignedEmployeeIds: string[];
  config: TaskConfig;
  createdAt: Date;
  updatedAt: Date;
  dueSoonNotifiedAt?: Date;
  overdueNotifiedAt?: Date;
}
```

### TaskAssignment

```typescript
interface TaskAssignment {
  id?: string;
  taskId: string;
  entityId: string;
  branchId: string;
  employeeId: string;
  status: "assigned" | "accepted" | "working" | "completed" | "blocked" | "removed";
  assignedBy: string;
  assignedAt: Date;
  startedAt?: Date;
  completedAt?: Date;
  removedAt?: Date;
  notes?: string;
}
```

### TaskNote

```typescript
interface TaskNote {
  id?: string;
  taskId: string;
  entityId: string;
  branchId: string;
  content: string;
  type: "specification" | "operational_note" | "clarification" | "incident_note";
  createdBy: string;
  createdByRole: "worker" | "supervisor" | "manager" | "owner";
  createdAt: Date;
  updatedBy?: string;
  updatedAt?: Date;
}
```

### TaskResource

```typescript
interface TaskResource {
  id?: string;
  taskId: string;
  entityId: string;
  branchId: string;
  uploadedBy: string;
  employeeId?: string;
  description?: string;
  type: "photo" | "video";
  filename: string;
  mimeType: string;
  url: string;
  storagePath: string;
  sizeKB: number;
  createdAt: Date;
}
```

### TaskRating

```typescript
interface TaskRating {
  id?: string;
  taskId: string;
  entityId: string;
  branchId: string;
  employeeId: string;
  rating: 1 | 2 | 3 | 4 | 5;
  comment?: string;
  ratedBy: string;
  ratedByRole: "supervisor" | "manager" | "owner";
  ratedAt: Date;
}
```

### TaskValidation

```typescript
interface TaskValidation {
  id?: string;
  taskId: string;
  entityId: string;
  branchId: string;
  result: "validated" | "rejected";
  reason?: string;
  validatedBy: string;
  validatedByRole: "supervisor" | "manager" | "owner";
  validatedAt: Date;
}
```

### TaskActivity

```typescript
interface TaskActivity {
  id?: string;
  taskId: string;
  entityId: string;
  branchId: string;
  type: "created" | "updated" | "assigned" | "status_changed" | "started" | "completed"
      | "validated" | "rejected" | "cancelled" | "note_added" | "note_updated"
      | "resource_uploaded" | "rated" | "commented";
  actorId: string;
  actorRole: "worker" | "supervisor" | "manager" | "owner";
  employeeId?: string;
  fromStatus?: string;
  toStatus?: string;
  metadata?: Record<string, unknown>;
  createdAt: Date;
}
```

## 6. Persistencia

### Firestore

```
entities/{entityId}/tasks/{taskId}
entities/{entityId}/tasks/{taskId}/assignments/{assignmentId}
entities/{entityId}/tasks/{taskId}/notes/{noteId}
entities/{entityId}/tasks/{taskId}/resources/{resourceId}
entities/{entityId}/tasks/{taskId}/ratings/{ratingId}
entities/{entityId}/tasks/{taskId}/validations/{validationId}
entities/{entityId}/tasks/{taskId}/activity/{activityId}
```

Cada documento hijo duplica: `entityId`, `branchId`, `taskId`, `employeeId` (si aplica), `createdAt`.

### Storage

```
media/entities/{entityId}/checkinbiz/tasks/{taskId}/{timestamp}-{filename}
```

Tipos MIME permitidos:
- Fotos: `image/jpeg`, `image/png`, `image/webp`
- Videos: `video/mp4`, `video/webm`

## 7. API HTTP

Cloud Function: `apiV100-firebaseEntryHttp-checkinbiz-tasksHandler`

Base: `/tasks`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/tasks` | Listar tareas (`entityId`, `branchId`, `status`, `employeeId`, `from`, `to`) |
| `GET` | `/tasks/:taskId` | Detalle completo (task + assignments + notes + resources + ratings + validations + activity) |
| `GET` | `/tasks/:taskId/activity` | Solo actividad |
| `POST` | `/tasks` | Crear tarea |
| `PATCH` | `/tasks/:taskId` | Editar tarea |
| `POST` | `/tasks/:taskId/assignments` | Asignar trabajadores |
| `DELETE` | `/tasks/:taskId/assignments/:employeeId` | Desasignar trabajador |
| `PATCH` | `/tasks/:taskId/status` | Cambiar estado |
| `POST` | `/tasks/:taskId/notes` | Agregar nota |
| `PATCH` | `/tasks/:taskId/notes/:noteId` | Actualizar nota |
| `POST` | `/tasks/:taskId/validation` | Validar tarea |
| `POST` | `/tasks/:taskId/rejection` | Rechazar tarea |
| `POST` | `/tasks/:taskId/resources` | Subir evidencia (multipart/form-data) |
| `POST` | `/tasks/:taskId/ratings` | Valorar trabajador |

### Crear tarea — payload

```json
{
  "entityId": "entity_123",
  "branchId": "branch_123",
  "title": "Limpieza de zona A",
  "description": "Completar limpieza y subir evidencia",
  "scheduledStartAt": "2026-04-24T08:00:00.000Z",
  "dueAt": "2026-04-24T16:00:00.000Z",
  "priority": "medium",
  "assignedEmployeeIds": ["emp_1", "emp_2"],
  "config": {
    "allowSupervisorCreation": false,
    "allowSupervisorValidation": true,
    "allowSupervisorRating": true,
    "completionPolicy": "any_assigned_worker",
    "requireEvidenceOnCompletion": true,
    "maxPhotoSizeMB": 5,
    "maxVideoSizeMB": 25
  }
}
```

### Subir recurso — campos multipart

```
entityId, branchId, employeeId, type (photo|video), description (opcional), file
```

## 8. Función de permisos — `canManageTask`

```typescript
function canManageTask(actor: ResolvedTaskActor, config: TaskConfig): boolean {
  return actor.isEntityWriter
    || actor.level >= ResponsibilityLevel.manager
    || (actor.level >= ResponsibilityLevel.supervisor && config.allowSupervisorCreation);
}

function canOperateAssignedTask(actor: ResolvedTaskActor, task: Task): boolean {
  return actor.isEntityWriter
    || actor.level >= ResponsibilityLevel.supervisor
    || (!!actor.employeeId && task.assignedEmployeeIds.includes(actor.employeeId));
}

function canAddTaskNote(actor: ResolvedTaskActor, task: Task): boolean {
  return actor.isEntityWriter
    || actor.level >= ResponsibilityLevel.supervisor
    || (!!actor.employeeId && task.assignedEmployeeIds.includes(actor.employeeId));
}
```

`canManageTask` reemplaza a `canCreateTask` y es la única función de permisos de creación/edición.

## 9. Validaciones clave

**Crear:** `entityId`, `branchId`, `title`, `dueAt` requeridos; `assignedEmployeeIds` deben existir y pertenecer a la sucursal; actor con permisos.

**Completar:** actor asignado o admin autorizado; tarea no en `validated`/`cancelled`; si `requireEvidenceOnCompletion = true` debe existir al menos un recurso.

**Validar/Rechazar:** tarea en `completed`; actor con permiso de validación; rechazo requiere motivo.

**Valorar:** `rating` 1–5; trabajador valorado asignado a la tarea; actor con permiso de valoración; registrar `ratedBy`, `ratedByRole`, `ratedAt`.

**Notas/Recursos:** `content` no vacío; actor con permisos (ver regla en sección 2); generar actividad.

## 10. Notificaciones

Usa el sistema existente: `CheckbizNotifier`, `TaskNotificationService`, `TaskRecipientResolver`.

Tipos de notificación:

| Tipo | Destinatario |
|---|---|
| `task_created` | Workers asignados |
| `task_assigned` | Worker recién asignado |
| `task_updated` | Workers asignados |
| `task_started` | Equipo asignado |
| `task_completed` | Equipo asignado |
| `task_validated` | Workers asignados |
| `task_rejected` | Workers asignados |
| `task_due_soon` | Equipo asignado |
| `task_overdue` | Equipo asignado |
| `task_resource_uploaded` | Equipo asignado |
| `task_worker_rated` | Worker valorado |

Idioma: `Employee.language ?? "es"`. Si destinatarios tienen distintos idiomas, enviar por agrupaciones.

## 11. Frontend / Backoffice

### Rutas

- Listado: `/main/[entityId]/checkinbiz/tasks`
- Crear: `/main/[entityId]/checkinbiz/tasks/new`
- Detalle: `/main/[entityId]/checkinbiz/tasks/:taskId`

### Vistas mínimas

- Listado de tareas (filtros: estado, sucursal, empleado, fechas)
- Detalle (resumen, equipo, notas, evidencias, valoraciones, actividad/timeline)
- Formulario de creación y edición
- Gestión de asignados
- Upload de evidencias

### Información por card/fila

Título, sucursal, prioridad, fecha límite, estado principal, subestado temporal, número de asignados, indicador de evidencia requerida.

### Acciones contextuales (según permisos efectivos y estado)

Crear, editar, asignar, iniciar, completar, agregar nota, validar, rechazar, valorar, subir recurso.

Refrescar detalle y actividad después de cada mutación.

## 12. App Móvil

### Rutas

| Constante | Path |
|---|---|
| `taskRoute` | `/attendance/tasks` |
| `taskCreateRoute` | `/attendance/tasks/new` |
| `taskDetailRoute` | `/attendance/tasks/:taskId` |

Tab en bottom nav (índice 0 dentro de `AttendanceShellPage`).

### Providers relevantes

- `taskFirestoreDataSourceProvider`
- `taskLookupDataSourceProvider`
- `taskRemoteDataSourceProvider`
- `taskRepositoryProvider`

### Lectura

La app puede leer tareas directamente desde Firestore (streams en tiempo real). Las mutaciones siempre van por HTTP.

## 13. Errores estándar

```typescript
"task/bad_request"
"task/not_found"
"task/unauthorized"
"task/evidence_required"
"task/note_not_found"
```

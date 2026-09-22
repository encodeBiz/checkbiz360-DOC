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

### Acciones desde la lista y desde inicio (1.6.0)

Iniciar, pausar, reanudar y completar no viven solo en la ficha. Están en la tarjeta de la lista y en la tarjeta «Tareas de hoy» del home de asistencia.

- `taskQuickActionsFor(task, isAssigned)` decide qué botones salen: `assigned` → iniciar; en curso → pausar + completar; pausada → reanudar + completar. Solo en tareas propias.
- `taskQuickActionProvider` ejecuta la mutación sin cargar la ficha entera, marca la tarea como ocupada mientras la llamada va por el aire —el segundo toque se ignora— y parchea la lista con la tarea que devuelve el servidor, vía `taskListItemPatchProvider`.
- Sin jornada abierta el toque no falla en silencio: avisa y lleva a fichar. Reanudar no la exige (08_pausas.md, D5).
- Completar con `requireEvidenceOnCompletion` abre la ficha en lugar de llamar al servidor: desde la lista no se sabe si ya hay evidencias.
- Completar pide confirmación, en la lista y en la ficha. Es la única acción que el empleado no deshace solo.

### Separación de lo propio para supervisor+ (1.6.0)

- `taskOwnerGroups(tasks, employeeId)` parte la lista en «Mis tareas» y «Tareas del equipo», con lo empezado primero dentro de cada mitad. Solo de supervisor para arriba; un worker ve la agrupación por estado de siempre.
- `TaskOwnershipBadge` marca las propias: chip con etiqueta en la lista, solo icono en la fila de inicio. `showsTaskOwnership` exige rol supervisor+ y estar asignado.
- `taskOwnFirst(tasks, employeeId)` en `todayScheduledTasksProvider` ordena la tarjeta de inicio con lo propio delante, sin tocar el orden interno.

### Buscadores de sucursal y trabajador

- `TaskLookupField` precarga las diez primeras opciones al enfocar, sin escribir nada, y las cachea cinco minutos.
- Por debajo de tres letras filtra en local esas sugerencias: el backend genera los prefijos de `keywords_prefix` desde tres caracteres (`buildPrefixes(tokens, min = 3)`), así que con dos la consulta no puede devolver nada.
- La lista de resultados se pinta en una capa flotante anclada al campo, no colgando de él.

## 13. Errores estándar

```typescript
"task/bad_request"
"task/not_found"
"task/unauthorized"
"task/evidence_required"
"task/note_not_found"
```

## 14. Evolución — Geo a nivel Task (Fase 2, NO implementado)

> Estado: **propuesta de roadmap**. Nada de esta sección existe todavía en el modelo ni en la API. Documenta la siguiente evolución acordada para no perder el diseño.

### Motivación

CheckBiz nace con el geo-fence a dos niveles: **entidad** (`ratioChecklog` global) y **sucursal** (`Branch.address.geo` + su `ratioChecklog`). Ese modelo asume ubicaciones fijas.

En empresas **de eventos y cuadrillas móviles** (caso real: Sonoibiza, audiovisuales en Ibiza) el equipo no trabaja en un punto fijo: cada evento ocurre en un venue distinto (boda, club, hotel, corporativo). Hoy esto se modela con **sucursales = departamentos** (Sonido, Iluminación, Vídeo), todas compartiendo el geo de la base/almacén, y con las **tareas** representando cada evento. Con ese enfoque el fichaje solo prueba "presencia en base", no presencia en el evento real.

La Fase 2 cierra ese hueco: **dar coordenada propia a la tarea**, de modo que el fichaje pueda validarse contra la ubicación del evento sobre el terreno.

### Jerarquía de geo resultante (3 niveles)

| Nivel | Fuente del geo | Qué valida | Estado |
|---|---|---|---|
| Entidad | `ratioChecklog` global | Radio por defecto | ✅ Actual |
| Sucursal / Departamento | `Branch.address.geo` + `ratioChecklog` | Presencia "en base" (preparar/cargar) | ✅ Actual |
| **Tarea** | `Task.geo` + `Task.ratioChecklog` | Presencia **en el evento**, sobre el terreno | 🔜 Fase 2 |

### Diseño propuesto (aditivo — no rompe nada)

Añadir campos **opcionales** a `Task`. Cuando están ausentes, el comportamiento es idéntico al actual (validación contra el geo de la sucursal / entidad).

```typescript
interface Task {
  // ...campos actuales...
  geo?: {
    lat: number;
    lng: number;
    address?: string;      // dirección legible del evento
    timeZone?: string;
  };
  ratioChecklog?: number;     // radio en metros específico del evento; hereda de branch/entidad si se omite
  disableRatioChecklog?: boolean; // permitir fichaje sin radio para esta tarea concreta
}
```

### Resolución del geo efectivo (cascada)

Al fichar contra una tarea, el radio y centro se resuelven en cascada de lo más específico a lo más general:

```
Task.geo / Task.ratioChecklog
  └─ si ausente → Branch.address.geo / Branch.ratioChecklog
       └─ si ausente → Entity.ratioChecklog (radio global)
```

`Task.disableRatioChecklog = true` anula la validación de radio solo para esa tarea (eventos donde no aplica geo-fence).

### Impacto y compatibilidad

- **Modelo:** solo se **suman** campos opcionales a `Task`. Los documentos hijos ya duplican `branchId`/`taskId`; se puede propagar el geo de la tarea al `CheckLog` asociado si el fichaje se vincula a una tarea.
- **Datos existentes:** cero migración. Tareas sin `geo` siguen validando contra la sucursal.
- **Demo / configuración actual (departamentos + tareas):** todo lo montado hoy sigue siendo válido íntegramente; las tareas solo ganarán ubicación cuando llegue la Fase 2.
- **Pendiente de definir en su momento:** vínculo `CheckLog ↔ Task` (hoy el fichaje no referencia tarea), UI de captura de coordenada del evento, y cómo se refleja en el radio efectivo del cliente móvil.

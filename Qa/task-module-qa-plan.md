# QA - Modulo Task

> Documento orientado a QA para validar el modulo de gestion de tareas operativas de CheckBiz.
> Fuente funcional base: `DOCS/modulos/task.md`, `DOCS/DOMINIO.md`, `DOCS/capas/backend.md`.

## 1. Objetivo

Validar que el modulo Task permite crear, asignar, ejecutar, completar, validar, rechazar, comentar, adjuntar evidencias y valorar tareas respetando:

- permisos por `EmployeeResponsibility`,
- scopes por `entityId` y `branchId`,
- estados de tarea y asignacion,
- reglas de configuracion `TaskConfig`,
- persistencia Firestore,
- subida de recursos a Storage,
- actividad/auditoria,
- notificaciones no bloqueantes.

## 2. Alcance QA

### Incluido

- API HTTP `apiV100-firebaseEntryHttp-checkinbiz-tasksHandler`.
- Rutas bajo `/tasks`.
- Backoffice.
- App movil.
- Permisos por rol operativo.
- Subida de evidencias.
- Validacion/rechazo.
- Rating de trabajadores.
- Activity log.
- Casos de error esperados.

### Excluido

- Gestion documental.
- Checklog manual.
- Heuristica.
- Notificaciones de otros modulos.
- Integraciones de pago/suscripcion salvo limites que bloqueen creacion si aplican.

## 3. Entorno

### Dev

Cloud Function:

```txt
apiV100-firebaseEntryHttp-checkinbiz-tasksHandler
```

Base local emulator documentada:

```txt
http://127.0.0.1:5001/encodebiz-services/us-central1/apiV100-firebaseEntryHttp-checkinbiz-tasksHandler/tasks
```

Base remota dev:

```txt
https://us-central1-dev-encodebiz.cloudfunctions.net/apiV100-firebaseEntryHttp-checkinbiz-tasksHandler/tasks
```

Si se usa URL Cloud Run directa, debe verificarse en el despliegue vigente.

## 4. Datos Minimos De Prueba

QA necesita preparar:

- `entityId` activa.
- `branchId` activa.
- Empleado worker asignable.
- Supervisor con responsabilidad activa en el `branchId`.
- Manager con responsabilidad activa en el `branchId`.
- Owner operativo con responsabilidad activa en el `branchId`.
- Usuario owner/admin global en `user_entity_roles`.
- Tokens validos:
  - Firebase/admin token cuando aplique.
  - Session token empleado/staff para app movil.

### Responsabilidades esperadas

```txt
worker     level 1
supervisor level 2
manager    level 3
owner      level 4
```

La responsabilidad debe estar activa y asociada al mismo `branchId` de la tarea.

## 5. API Bajo Prueba

| Metodo | Ruta | Objetivo |
|---|---|---|
| `GET` | `/tasks` | Listado filtrado |
| `POST` | `/tasks` | Crear tarea |
| `GET` | `/tasks/:taskId` | Detalle completo |
| `GET` | `/tasks/:taskId/activity` | Actividad |
| `PATCH` | `/tasks/:taskId` | Editar tarea |
| `POST` | `/tasks/:taskId/assignments` | Asignar trabajadores |
| `DELETE` | `/tasks/:taskId/assignments/:employeeId` | Desasignar trabajador |
| `PATCH` | `/tasks/:taskId/status` | Cambiar estado |
| `POST` | `/tasks/:taskId/notes` | Agregar nota |
| `PATCH` | `/tasks/:taskId/notes/:noteId` | Actualizar nota |
| `POST` | `/tasks/:taskId/resources` | Subir evidencia |
| `POST` | `/tasks/:taskId/validation` | Validar tarea |
| `POST` | `/tasks/:taskId/rejection` | Rechazar tarea |
| `POST` | `/tasks/:taskId/ratings` | Valorar trabajador |

## 6. Modelo Funcional A Validar

### Task

Campos criticos:

- `entityId`
- `branchId`
- `title`
- `status`
- `timeComplianceStatus`
- `dueAt`
- `assignedEmployeeIds`
- `config`
- `createdAt`
- `updatedAt`

### TaskConfig

```typescript
{
  allowSupervisorCreation: boolean;
  allowSupervisorValidation: boolean;
  allowSupervisorRating: boolean;
  completionPolicy: "any_assigned_worker" | "all_assigned_workers";
  requireEvidenceOnCompletion: boolean;
  maxPhotoSizeMB: number;
  maxVideoSizeMB: number;
}
```

Decision vigente:

```txt
completionPolicy = "any_assigned_worker"
```

## 7. Matriz De Permisos QA

| Accion | Worker asignado | Worker no asignado | Supervisor mismo branch | Manager mismo branch | Owner operativo | Owner/Admin global |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Ver tarea | si | no | si | si | si | si |
| Crear tarea | no | no | si, si `allowSupervisorCreation` | si | si | si |
| Editar tarea | no | no | si, si `allowSupervisorCreation` | si | si | si |
| Cancelar tarea | no | no | si, si `allowSupervisorCreation` | si | si | si |
| Asignar workers | no | no | si | si | si | si |
| Desasignar workers | no | no | si | si | si | si |
| Cambiar a `in_progress` | si | no | si | si | si | si |
| Cambiar a `completed` | si | no | si | si | si | si |
| Agregar nota | si | no | si | si | si | si |
| Subir recurso | si | no | si | si | si | si |
| Validar/rechazar | no | no | si, si `allowSupervisorValidation` | si | si | si |
| Valorar worker | no | no | si, si `allowSupervisorRating` | si | si | si |

Punto critico: supervisor puede agregar notas y subir recursos en cualquier tarea de su sucursal sin estar asignado.

## 8. Estados Esperados

### Estado principal

```txt
draft -> assigned -> in_progress -> completed -> validated
completed -> rejected -> in_progress
any -> cancelled
```

### Estados soportados

```txt
draft
assigned
in_progress
completed
validated
rejected
cancelled
```

### TimeComplianceStatus

```txt
not_started
on_time
at_risk
overdue
completed_on_time
completed_late
rejected
```

QA debe validar que:

- una tarea completada antes de `dueAt` queda `completed_on_time`;
- una tarea completada despues de `dueAt` queda `completed_late`;
- una tarea rechazada puede volver a flujo operativo segun endpoint de status;
- cancelar no debe dejar asignaciones incoherentes.

## 9. Casos De Prueba Funcionales

### TC-TASK-001 - Crear tarea como manager

Precondiciones:

- Actor manager activo en el `branchId`.

Pasos:

1. Enviar `POST /tasks` con payload valido.
2. Incluir `assignedEmployeeIds`.
3. Verificar respuesta 201/200 segun contrato real.

Resultado esperado:

- Se crea task.
- `status` inicial coherente.
- `assignedEmployeeIds` persiste.
- Se crean assignments si el caso de uso los materializa.
- Se registra activity `created`.

### TC-TASK-002 - Crear tarea como supervisor con flag desactivado

Precondiciones:

- Actor supervisor activo en branch.
- `allowSupervisorCreation = false`.

Resultado esperado:

- HTTP 403.
- Codigo `task/unauthorized` o equivalente.
- No se crea task.

### TC-TASK-003 - Crear tarea como supervisor con flag activado

Precondiciones:

- Actor supervisor activo en branch.
- `allowSupervisorCreation = true`.

Resultado esperado:

- Tarea creada.
- Activity registra actor supervisor.

### TC-TASK-004 - Worker no asignado no puede ver detalle

Pasos:

1. Crear tarea en branch.
2. Usar token de worker no asignado.
3. Solicitar `GET /tasks/:taskId`.

Resultado esperado:

- 403 o 404 segun politica de ocultacion.
- No se filtran datos de la tarea.

### TC-TASK-005 - Worker asignado ve detalle

Resultado esperado:

- HTTP 200.
- Detalle incluye task, assignments, notes, resources, ratings, validations, activity.

### TC-TASK-006 - Asignar trabajador

Actor permitido:

- supervisor, manager, owner, owner/admin global.

Resultado esperado:

- Se agrega assignment.
- `assignedEmployeeIds` se actualiza sin duplicados.
- Activity `assigned`.
- Notificacion fire-and-forget si aplica.

### TC-TASK-007 - Asignar empleado invalido

Casos:

- empleado inexistente;
- empleado inactivo;
- empleado sin responsabilidad/branch valido;
- empleado de otra entidad.

Resultado esperado:

- HTTP 400.
- No hay escrituras parciales.

### TC-TASK-008 - Desasignar trabajador

Resultado esperado:

- Assignment pasa a `removed` o se elimina segun implementacion real.
- `assignedEmployeeIds` deja de contener employeeId.
- Activity registra desasignacion.

### TC-TASK-009 - Worker asignado cambia estado a `in_progress`

Resultado esperado:

- `status = in_progress`.
- `startedAt` seteado.
- Activity `started` o `status_changed`.

### TC-TASK-010 - Worker asignado completa tarea

Resultado esperado:

- `status = completed`.
- `completedAt` seteado.
- `completedBy` seteado.
- `timeComplianceStatus` correcto.
- Activity `completed`.

### TC-TASK-011 - Requiere evidencia para completar

Precondicion:

```txt
config.requireEvidenceOnCompletion = true
```

Pasos:

1. Intentar completar sin recursos.
2. Subir recurso valido.
3. Completar de nuevo.

Resultado esperado:

- Primer intento falla.
- Segundo intento pasa.

### TC-TASK-012 - Supervisor sube recurso sin estar asignado

Precondicion:

- Supervisor activo en mismo branch.
- No esta en `assignedEmployeeIds`.

Resultado esperado:

- Puede subir recurso.
- Activity `resource_uploaded`.
- `uploadedBy` corresponde al actor operativo.

### TC-TASK-013 - Supervisor de otro branch no sube recurso

Resultado esperado:

- HTTP 403.
- No se sube archivo a Storage.
- No se crea resource.

### TC-TASK-014 - Validar tarea como manager

Precondicion:

- Tarea `completed`.

Resultado esperado:

- `status = validated`.
- `validatedAt` seteado.
- `validatedBy` seteado.
- Se crea `TaskValidation`.
- Activity `validated`.

### TC-TASK-015 - Validar tarea como supervisor con flag desactivado

Precondicion:

```txt
allowSupervisorValidation = false
```

Resultado esperado:

- HTTP 403.

### TC-TASK-016 - Validar tarea como supervisor con flag activado

Precondicion:

```txt
allowSupervisorValidation = true
```

Resultado esperado:

- HTTP 200.
- Validacion registrada.

### TC-TASK-017 - Rechazar tarea

Resultado esperado:

- `status = rejected`.
- `rejectedAt` seteado.
- `rejectedBy` seteado.
- `rejectionReason` requerido o validado segun contrato real.
- Activity `rejected`.
- Worker puede volver a trabajar si el flujo lo permite.

### TC-TASK-018 - Agregar nota como worker asignado

Resultado esperado:

- Nota creada.
- `createdByRole = worker`.
- Activity `note_added`.

### TC-TASK-019 - Agregar nota como supervisor no asignado mismo branch

Resultado esperado:

- Nota creada.
- `createdByRole = supervisor`.
- No requiere autoasignacion.

### TC-TASK-020 - Actualizar nota

Validar:

- autor original o responsable autorizado segun regla real;
- `updatedBy`;
- `updatedAt`;
- Activity `note_updated`.

### TC-TASK-021 - Subir foto valida

Multipart:

```txt
entityId
branchId
employeeId
type=photo
description?
file=image/jpeg|image/png|image/webp
```

Resultado esperado:

- Archivo en Storage bajo `media/entities/{entityId}/checkinbiz/tasks/{taskId}/...`.
- Resource creado.
- URL firmada/publica segun implementacion actual.

### TC-TASK-022 - Rechazar MIME invalido

Ejemplos:

- `application/pdf`
- `text/plain`
- imagen con MIME falso.

Resultado esperado:

- HTTP 400.
- No hay resource.
- No hay archivo persistido.

### TC-TASK-023 - Rechazar archivo superior a limite

Validar:

- foto > `maxPhotoSizeMB`;
- video > `maxVideoSizeMB`.

Resultado esperado:

- HTTP 400.
- No hay escrituras parciales.

### TC-TASK-024 - Valorar trabajador como manager

Payload:

```json
{
  "entityId": "entityId",
  "employeeId": "employeeIdAsignado",
  "rating": 5,
  "comment": "Buen trabajo"
}
```

Resultado esperado:

- Rating creado.
- `ratedByRole = manager`.
- Activity `rated`.

### TC-TASK-025 - Valorar trabajador no asignado

Resultado esperado:

- HTTP 400.
- Error "Employee is not assigned to this task" o equivalente.

### TC-TASK-026 - Supervisor valora con flag desactivado

Precondicion:

```txt
allowSupervisorRating = false
```

Resultado esperado:

- HTTP 403.

### TC-TASK-027 - Rating fuera de rango

Valores:

- `0`
- `6`
- `4.5`
- string no numerico.

Resultado esperado:

- HTTP 400.
- Mensaje de rango 1-5.

### TC-TASK-028 - Editar rating de otro autor

Precondicion:

- Rating existente creado por manager A.
- Manager B intenta modificarlo.

Resultado esperado:

- HTTP 403.
- Codigo `task/rating_author_mismatch`.

### TC-TASK-029 - Listado por filtros

Validar filtros:

- `entityId`;
- `branchId`;
- `status`;
- `employeeId`;
- `from`;
- `to`;
- `limit`.

Resultado esperado:

- No devuelve tareas fuera de permisos.
- Orden consistente.
- Filtros combinados funcionan.

### TC-TASK-030 - Activity completa

Tras un flujo completo:

```txt
created -> assigned -> started -> resource_uploaded -> note_added -> completed -> validated -> rated
```

Resultado esperado:

- Activity contiene eventos relevantes.
- Cada evento tiene `actorId`, `actorRole`, `entityId`, `branchId`, `taskId`, `createdAt`.

## 10. Casos De Seguridad

### SEC-TASK-001 - Sin token

Resultado esperado:

- HTTP 401.

### SEC-TASK-002 - Token invalido

Resultado esperado:

- HTTP 401.

### SEC-TASK-003 - entityId de otra entidad

Resultado esperado:

- HTTP 403 o 404.
- No se filtran datos.

### SEC-TASK-004 - branchId manipulado

Pasos:

1. Actor tiene responsabilidad en branch A.
2. Envía request contra task de branch B.

Resultado esperado:

- HTTP 403.

### SEC-TASK-005 - employeeId manipulado en rating/resource

Resultado esperado:

- No permite operar en nombre de otro empleado salvo rol autorizado.
- No debe confiar en `employeeId` del body para resolver actor.

### SEC-TASK-006 - IDOR por taskId conocido

Pasos:

1. Usuario conoce `taskId`.
2. No pertenece a la entidad/branch.

Resultado esperado:

- No puede ver ni operar.

## 11. Casos De Regresion Criticos

### REG-TASK-001 - Supervisor puede subir recurso sin asignarse

Este caso no debe romperse. Es requisito documentado.

### REG-TASK-002 - Supervisor puede agregar nota sin asignarse

Este caso no debe romperse.

### REG-TASK-003 - Supervisor no valida si flag esta desactivado

Evita escalada de permisos.

### REG-TASK-004 - Manager valida aunque flags de supervisor esten desactivados

Manager no depende de `allowSupervisorValidation`.

### REG-TASK-005 - Owner/admin global pasa aunque no tenga employee responsibility

Validar `isEntityWriter`.

### REG-TASK-006 - Responsabilidad debe ser del mismo branch

Evita que un responsable de branch A opere task de branch B.

### REG-TASK-007 - Rating author mismatch

Evita que otro responsable sobrescriba valoraciones previas.

### REG-TASK-008 - Storage bucket correcto por entorno

Subida de recursos debe usar bucket dev/prod correcto. No debe aparecer `.firebasestorage.app`.

## 12. Validaciones De Persistencia

### Firestore

Verificar rutas:

```txt
entities/{entityId}/tasks/{taskId}
entities/{entityId}/tasks/{taskId}/assignments/{assignmentId}
entities/{entityId}/tasks/{taskId}/notes/{noteId}
entities/{entityId}/tasks/{taskId}/resources/{resourceId}
entities/{entityId}/tasks/{taskId}/ratings/{ratingId}
entities/{entityId}/tasks/{taskId}/validations/{validationId}
entities/{entityId}/tasks/{taskId}/activity/{activityId}
```

Verificar timestamps:

- `createdAt`;
- `updatedAt`;
- `startedAt`;
- `completedAt`;
- `validatedAt`;
- `rejectedAt`;
- activity `createdAt`.

### Storage

Verificar path:

```txt
media/entities/{entityId}/checkinbiz/tasks/{taskId}/{timestamp}-{filename}
```

Validar:

- archivo existe;
- MIME correcto;
- sizeKB correcto;
- resource guarda `storagePath`;
- URL accesible segun politica actual.

## 13. Validaciones De Notificaciones

Las notificaciones son fire-and-forget. QA debe validar:

- fallo de FCM no rompe el endpoint principal;
- se invoca notificacion al asignar tarea;
- se invoca notificacion al subir recurso si aplica;
- se invoca notificacion al validar/rechazar/ratear si aplica;
- payload contiene `taskId`, `entityId`, `branchId` cuando corresponda.

No bloquear pruebas funcionales por errores transitorios de FCM si la operacion principal persiste correctamente.

## 14. Criterios De Aceptacion

El modulo Task se considera validado cuando:

- todos los roles respetan la matriz de permisos;
- no hay acceso cruzado entre branches;
- workers solo operan tareas asignadas;
- supervisor puede notas/recursos sin asignacion en su branch;
- supervisor requiere flags para crear/editar/validar/ratear;
- manager/owner tienen permisos completos en su branch;
- owner/admin global tiene acceso superior;
- estados y timestamps son coherentes;
- activity refleja las acciones principales;
- recursos se suben a Storage correctamente;
- MIME/tamano se validan;
- ratings respetan autor original;
- endpoints devuelven 400/401/403/404 segun caso;
- no hay escrituras parciales en errores esperados.

## 15. Evidencias Recomendadas

Para cada ciclo QA guardar:

- curl o request exportado;
- response status/body;
- captura de Firestore antes/despues;
- captura Storage para recursos;
- token/rol usado sin exponer secretos;
- branchId/entityId/taskId de prueba;
- screenshots backoffice/app si aplica.

## 16. Checklist Rapido De Smoke Test

- [ ] Crear task como manager.
- [ ] Listar task como manager.
- [ ] Ver task como worker asignado.
- [ ] Bloquear worker no asignado.
- [ ] Asignar worker.
- [ ] Worker cambia a `in_progress`.
- [ ] Worker sube evidencia.
- [ ] Worker completa.
- [ ] Manager valida.
- [ ] Manager ratea.
- [ ] Supervisor agrega nota sin estar asignado.
- [ ] Supervisor sube recurso sin estar asignado.
- [ ] Supervisor no valida si flag esta false.
- [ ] Activity contiene eventos.
- [ ] Storage contiene archivo.
- [ ] No hay acceso cross-branch.


# 05 — Integración: Front de administración

> **Para:** equipo del front de administración (back office) de CheckBiz.
> **Qué cubre:** cómo consumir el servicio `tasks` (`/api/v1/tasks`) desde el back office.
> **Fuente de verdad:** los controladores en `encodebiz-api/services/tasks`. Este doc resume el contrato; si hay discrepancia, manda el router.

---

## 1. Qué cambia

La API de tareas se movió de la Cloud Function `tasksHandler` a un servicio propio detrás de nginx. **El contrato no cambia**; solo cambia la URL base.

| | Antes | Ahora |
|---|---|---|
| URL | URL de la function `tasksHandler` (`…/tasksHandler/tasks/...`) | `https://api.checkbiz360.com/api/v1/tasks/...` |
| Auth | Firebase ID token | **Firebase ID token** (idéntico) |
| Payloads / respuestas | — | **iguales** |

Migración en el front: sustituir la URL base. Nada más.

---

## 2. Autenticación (Firebase ID token)

Igual que hoy: cabecera con el ID token del usuario administrador (proyecto `encodebiz-services`).

```
Authorization: Bearer <ID_TOKEN>
```

```ts
import { getAuth } from "firebase/auth";

const BASE = "https://api.checkbiz360.com/api/v1/tasks";
const token = await getAuth().currentUser!.getIdToken();

const res = await fetch(`${BASE}?entityId=${entityId}`, {
  headers: { "Authorization": `Bearer ${token}` },
});
```

El token caduca a la hora; `getIdToken()` lo refresca solo. El servidor valida con `verifyIdToken` (sin `checkRevoked`, igual que la function original).

---

## 3. Permisos por nivel

El servidor resuelve el actor y su **nivel de responsabilidad** sobre la entidad/sucursal. Un usuario con permiso de escritura sobre la entidad (`owner`/`admin` en `user_entity_roles`) equivale a `owner`.

| Acción | Nivel mínimo |
|---|---|
| Crear / editar tarea | `manager`, o `supervisor` si `config.allowSupervisorCreation` |
| Asignar / desasignar trabajadores | `supervisor` |
| Validar / rechazar | `manager`, o `supervisor` si `config.allowSupervisorValidation` |
| Valorar trabajador | `manager`, o `supervisor` si `config.allowSupervisorRating` |
| Ver / listar | `supervisor` ve todo; por debajo, solo tareas propias |

Si el actor no tiene nivel suficiente → `403 task/unauthorized`.

---

## 4. Endpoints (base `…/api/v1/tasks`)

Contrato completo en [03_contratos-api.md](./03_contratos-api.md). Resumen de uso del back office:

### Listar
```
GET /?entityId=X&branchId=&status=&timeComplianceStatus=&employeeId=&from=&to=&limit=
→ 200 Task[]
```

### Crear
```ts
await fetch(BASE, {
  method: "POST",
  headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    entityId, branchId,
    title: "Reponer almacén",
    description: "...",
    priority: "high",                 // low|medium|high|critical
    scheduledStartAt: "2026-07-27T08:00:00.000Z",
    dueAt: "2026-07-27T14:00:00.000Z",
    assignedEmployeeIds: ["emp_1", "emp_2"],
    config: {
      allowSupervisorCreation: true,
      allowSupervisorValidation: true,
      allowSupervisorRating: true,
      completionPolicy: "any_assigned_worker",   // | all_assigned_workers
      requireEvidenceOnCompletion: true,
      notifyIfNotStarted: true,
      maxPhotoSizeMB: 5,
      maxVideoSizeMB: 25
    }
  }),
});
→ 201 TaskDetail   // { task, assignments, notes, resources, ratings, activity, validations }
```

### Detalle / actividad
```
GET /:taskId                 → 200 TaskDetail
GET /:taskId/activity?limit  → 200 TaskActivity[]
```

### Editar / estado
```
PATCH /:taskId               body: { title?, description?, priority?, dueAt?, config? }  → 200 TaskDetail
PATCH /:taskId/status        body: { status }                                            → 200 TaskDetail
```

### Asignaciones
```
POST   /:taskId/assignments               body: { employeeIds: string[] }  → 200 TaskDetail
DELETE /:taskId/assignments/:employeeId                                     → 200 TaskDetail
```

### Notas
```
POST  /:taskId/notes          body: { content, type }        → 201 TaskNote
PATCH /:taskId/notes/:noteId  body: { content }              → 200 TaskNote
```

### Validación / rechazo / valoración
```
POST /:taskId/validation                       → 200 TaskDetail   // status → validated
POST /:taskId/rejection    body: { reason }     → 200 TaskDetail   // status → rejected
POST /:taskId/ratings      body: { employeeId, rating (1-5), comment? }  → 200 TaskRating
```

---

## 5. Errores

| HTTP | Código | Cuándo |
|---|---|---|
| 400 | `task/bad_request` | Falta `entityId` u otro obligatorio |
| 401 | — | Falta/!Bearer en `Authorization` |
| 403 | `task/unauthorized` | Token válido pero sin nivel suficiente |
| 404 | `task/branch_not_found` | Branch inexistente |
| 400 | `task/branch_inactive` | Branch no activa |

Patrón recomendado en el front: si `401`, refrescar token y reintentar una vez; si `403`, ocultar/inhabilitar la acción en la UI según el nivel del usuario.

---

## 6. Notas importantes

- **Datos en tiempo real:** el servidor escribe en la misma Firestore (`entities/{entityId}/tasks/...`). Si el front ya escucha esos documentos en tiempo real, sigue funcionando sin cambios.
- **Notificaciones:** el ciclo de vida (crear, asignar, validar…) sigue disparando push como hasta ahora — no requiere nada en el front.
- **CORS:** el servicio responde a los orígenes del back office; si añades un dominio nuevo, hay que incluirlo en la config de CORS del servicio.

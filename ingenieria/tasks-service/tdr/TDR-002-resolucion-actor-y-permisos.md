# TDR-002 — Resolución del actor y matriz de permisos

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 1)
**Componente:** `services/tasks` — `resolveTaskActor` y funciones `can*`

---

## Problema

Cada operación de tarea se autoriza según **quién** la pide y **qué nivel de responsabilidad** tiene sobre la entidad/sucursal. Esta lógica (`resolveTaskActor` + matriz `can*`) debe portarse sin perder ninguna de sus dos vías de autenticación ni ninguna regla de nivel.

---

## Resolución del actor (`resolveTaskActor`)

Dos ramas, en orden:

### Rama 1 — Firebase ID token (back office)
```
decoded = validateToken(req)                  // portado 1:1 → admin.auth().verifyIdToken(idToken)
isEntityWriter = canWrite(decoded.uid, entityId)   // permiso de escritura sobre la entidad
employees = employeeRepository.findAllByUid(decoded.uid).filter(e => e.entityId === entityId)
responsibilities = para cada employee → findResponsibilities({entityId, branchId}, employee.id)
highestRole = el de mayor level entre todas las responsibilities
if (!isEntityWriter && !highestRole) → 403 task/unauthorized
level = max(highestRole.level, isEntityWriter ? owner : 0)
```

### Rama 2 — Staff JWT (app móvil del empleado), fallback si la rama 1 lanza
```
validation = validateTokenJWT(req, res)       // JWT propio de staff
payload = { employeeId, entityId }
if (!payload.employeeId || (payload.entityId && payload.entityId !== entityId)) → 403
employee = employeeRepository.findById(payload.employeeId, entityId)  // 404 si no existe
responsibilities = findResponsibilities({entityId, branchId}, payload.employeeId)
role = highestRole?.role ?? "worker"; level = highestRole?.level ?? worker
isEntityWriter = false
```

El resultado es un `ResolvedTaskActor`:
```typescript
interface ResolvedTaskActor {
  uid?: string;
  employeeId?: string;
  role: TaskActorRole;      // "worker" | "supervisor" | "manager" | "owner"
  level: number;            // ResponsibilityLevel
  isEntityWriter: boolean;
  employee?: Employee | null;
}
```

## Niveles de responsabilidad

`ResponsibilityLevel`: `worker < supervisor < manager < owner`. Un `isEntityWriter` (usuario con permiso de escritura sobre la entidad) equivale a `owner` a efectos de nivel.

## Matriz de permisos (`can*`)

| Función | Regla |
|---|---|
| `canManageTask(actor, config)` | entityWriter **o** `level ≥ manager` **o** (`level ≥ supervisor` **y** `config.allowSupervisorCreation`) |
| `canAssignTaskWorkers(actor)` | entityWriter **o** `level ≥ supervisor` |
| `canValidateOrRejectTask(actor, task)` | entityWriter **o** `level ≥ manager` **o** (`level ≥ supervisor` **y** `task.config.allowSupervisorValidation`) |
| `canRateTask(actor, task)` | entityWriter **o** `level ≥ manager` **o** (`level ≥ supervisor` **y** `task.config.allowSupervisorRating`) |
| `canViewTask(actor, task)` | entityWriter **o** `level ≥ supervisor` **o** el `employeeId` está en `task.assignedEmployeeIds` |
| `canOperateAssignedTask(actor, task)` | igual que `canViewTask` |
| `canAddTaskNote(actor, task)` | igual que `canViewTask` |

**Regla de scoping en listados:** en `findTasks`, si el actor no es entityWriter y su `level < supervisor`, el filtro se fuerza a `employeeId = actor.employeeId` (un worker solo ve sus tareas asignadas).

## Cola de dependencias a portar

- `validateToken(req)` — verificación del ID token de Firebase, **portado 1:1** (`admin.auth().verifyIdToken(idToken)`, sin `checkRevoked`). Único cambio: el tipo `Request` pasa de `firebase-functions/https` a `express` (type-only).
- `validateTokenJWT` — verificación del JWT de staff (secreto `JWT_2FA_SECRET`), portado tal cual.
- `canWrite(uid, entityId)` — consulta de permiso de escritura sobre la entidad (Firestore), portado tal cual.
- `employeeRepository.findAllByUid`, `findById`, `findResponsibilities` — ya vienen con `FirestoreEmployeeRepository` (portado en [TDR-001](./TDR-001-port-modulo-task.md)).

**No se usa `requireFirebaseAuth` de `@encodebiz/shared`**: verifica con `verifyIdToken(token, true)` (`checkRevoked: true`), más estricto que el original y por tanto un cambio de comportamiento inaceptable con app y front ya en producción (ver [ADR-004](../adr/ADR-004-auth-dual-conservada.md)).

## Configuración

- `JWT_2FA_SECRET` — secreto de firma del JWT de staff que verifica `validateTokenJWT` (la rama 2). Debe estar disponible como variable de entorno del servicio `tasks`, con el mismo valor que en Firebase.
  > Nota de implementación: la rama 2 usa `validateTokenJWT` (secreto `JWT_2FA_SECRET`), no `validateTokenStaff` (`STAFF_JWT_SECRET`). Ambos helpers se portaron, pero `task.helpers` cablea `validateTokenJWT`.

## Criterio de éxito

- Un ID token de back office con permiso de entidad resuelve a `isEntityWriter=true`, `level=owner`.
- Un staff JWT de un empleado asignado resuelve a `role/level` según sus responsabilidades y puede operar sus tareas.
- Un worker no ve tareas ajenas en `GET /` (scoping forzado).
- Token inválido/ausente por ambas vías → `403 task/unauthorized`.

# TDR-002 — Resolución del actor y matriz de permisos

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 2)
**Componente:** `services/documents` — `DocumentPermissionService`

---

## Problema

Cada operación documental se autoriza según **quién** la pide, **qué nivel** tiene sobre la
entidad/sucursal y **qué tipo/scope** tiene el documento. Esta lógica
(`resolveActor` + matriz `can*`) debe portarse sin perder ninguna regla.

## Resolución del actor (`resolveActor(uid, entityId)`)

Una sola vía (Firebase ID token; ver [ADR-004](../adr/ADR-004-auth-solo-firebase-token.md)):

```
[roleSnap, empSnap] = paralelo(
  user_entity_roles/{uid}_{entityId},                       // owner | admin (global)
  entities/{entityId}/employees where uid == uid  limit 1   // empleado de la entidad
)
globalRole    = roleSnap.role ∈ {owner, admin} ? ese : undefined
isOwnerAdmin  = globalRole !== undefined
employeeId    = (empleado existe y status ∉ {fired, inactive}) ? empDoc.id : undefined
branchResponsibilities = si hay employeeId →
    entities/{entityId}/employee_responsibilities where employeeId == … and active == 1
    → Map<branchId, {role, level}>  (se queda el de mayor level por sucursal)
actorRole = isOwnerAdmin ? (globalRole ?? "admin")
                         : rol de la responsabilidad de mayor level (def. "worker")
```

Resultado `DocumentActor`:
```typescript
interface DocumentActor {
  uid: string;
  employeeId: string | undefined;
  isOwnerAdmin: boolean;
  globalRole: "owner" | "admin" | undefined;
  branchResponsibilities: Map<string, {role, level}>;
  actorRole: "worker" | "supervisor" | "manager" | "owner" | "admin";
}
```

**Rechazo de actor sin vínculo** (en `resolveDocumentActor`, antes de cada operación): si
`!isOwnerAdmin && employeeId === undefined && branchResponsibilities.size === 0` → `403 documents/unauthorized`.

## Niveles de responsabilidad

`ResponsibilityLevel`: `worker < supervisor < manager < owner`. `owner` aquí es el **owner
operativo** de una sucursal (nivel 4), distinto del owner/admin global (`isOwnerAdmin`).

## Tipos con reglas especiales

- **RRHH-puros** (`RESTRICTED_DOCUMENT_TYPES` = `payroll`, `contract`): gestionados **solo por owner/admin global**. Ni crear, ni actualizar, ni archivar por managers.
- **Disciplinarios** (`DISCIPLINARY_DOCUMENT_TYPES` = `warning`, `attention_call`): en scope employee, solo `manager` **exacto** (nivel 3) — el owner operativo (nivel 4) queda excluido, porque el aviso formal lo emite el manager.

## Matriz de permisos (`can*`)

| Función | Regla |
|---|---|
| `canCreate(actor, scope, branchId, type)` | owner/admin → siempre. `scope=entity` → solo owner/admin. `scope=branch` → `manager+` en la branch, y **nunca** tipos RRHH. `scope=employee` → RRHH nunca; disciplinarios → `manager` exacto de la branch; resto → `manager+` de la branch. |
| `canRead(actor, doc)` | owner/admin → siempre. `entity` → owner operativo, o rol del actor ∈ `visibleToRoles`. `branch` → visible en la branch por rol (owner operativo siempre). `employee` → el propio empleado siempre; si no, RRHH nunca, y para el resto visible en la branch por rol. |
| `canUpdate(actor, doc)` | igual que `canArchive`. |
| `canArchive(actor, doc)` | owner/admin → siempre. RRHH → nunca (solo owner/admin). Sin `branchId` (scope entity) → solo owner/admin. Resto → `manager+` en la branch. |
| `canAcknowledge(actor, doc)` | requiere `requiresAcknowledgement` y `canRead`. `single_employee` → `actor.employeeId === doc.employeeId`. `branch_employees` → el actor tiene responsabilidad en `doc.branchId`. `entity_employees` → el actor tiene ≥1 responsabilidad. |

Reglas auxiliares: `roleVisibleInBranch` (owner operativo bypasea `visibleToRoles`);
`actorVisibleForEntityScope` (owner operativo o rol ∈ `visibleToRoles` en cualquier branch).

## Scoping en listados (`FindDocuments`)

- `status`: si no se pide explícitamente, para actores **no** owner/admin se fuerza a `active`.
- Los tres flujos (búsqueda por índice, "todo del empleado", y listado normal) **siempre**
  filtran cada documento por `canRead` antes de devolverlo. La paginación por cursor cuenta
  sobre lo visible; el flujo de índice y el "todo del empleado" paginan en memoria.

## Criterio de aceptación

Portado 1:1 desde `DocumentPermissionService`. Casos de verificación mínimos: (a) empleado sin
rol suficiente sobre un `payroll` ajeno → 403; (b) `manager` de sucursal crea `warning` en su
sucursal → OK, pero `owner` operativo no; (c) owner/admin ve documentos `archived`, un empleado
no.

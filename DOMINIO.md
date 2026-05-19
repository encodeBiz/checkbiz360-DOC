# Dominio Core — Entidades, Roles y Modelos

## 1. Entidades Principales

### Entity (Empresa)
Raíz del árbol de datos. Todo dato pertenece a una `entityId`.

```typescript
interface Entity {
  entityId: string;
  name: string;
  timezone: string;
  defaultSchedule: WeeklySchedule;
  advance: ScheduleAdvance;
}
```

### Branch (Sucursal)
```typescript
interface Branch {
  branchId: string;
  entityId: string;
  name: string;
  address: {
    geo: { lat: number; lng: number };
    timeZone: string;
  };
  ratioChecklog?: number;
  disableRatioChecklog?: boolean;
  advance?: { enableDayTimeRange: boolean; notifyBeforeMinutes: number };
}
```

### Employee (Empleado)
```typescript
interface Employee {
  employeeId: string;
  entityId: string;
  uid: string;              // Firebase Auth UID
  name: string;
  email: string;
  branchId: string[];       // puede estar en varias sucursales
  enableRemoteWork?: boolean;
  address?: { timeZone?: string };
  language?: string;        // para notificaciones push
}
```

### EmployeeResponsibility
```typescript
interface EmployeeResponsibility {
  entityId: string;
  branchId: string;
  employeeId: string;
  responsibility: "worker" | "supervisor" | "manager" | "owner";
  level: ResponsibilityLevel; // 1-4
  active: boolean;
  job?: { id: string; name: string; price: number };
}
```

### CheckLog
```typescript
interface CheckLog {
  id: string;
  entityId: string;
  employeeId: string;
  branchId: string;
  type: "checkin" | "checkout";
  status: "valid" | "failed" | "pending-employee-validation" | "incomplete_workday";
  timestamp: Date;          // UTC
  geo: { lat: number; lng: number };
  userAgent: string;
  isSuspect: boolean;
  checkin: string;          // id del checkin asociado (en checkout)
  closed?: boolean;         // true solo en checkout válido
  metadata: CheckLogMetadata;
}
```

## 2. Roles y Niveles

```typescript
enum ResponsibilityLevel {
  worker     = 1,   // solo opera tareas/checklogs propios
  supervisor = 2,   // gestiona su(s) sucursal(es), configurable con flags
  manager    = 3,   // administrador de sucursal
  owner      = 4,   // propietario de entidad
}
```

### Matriz de permisos generales

| Acción | worker | supervisor | manager | owner | entityWriter |
|---|:---:|:---:|:---:|:---:|:---:|
| Ver datos de su sucursal | ✓ | ✓ | ✓ | ✓ | ✓ |
| Crear/editar recursos propios | ✓ | ✓ | ✓ | ✓ | ✓ |
| Gestionar empleados de sucursal | — | — | ✓ | ✓ | ✓ |
| Crear solicitudes manuales | — | ✓* | ✓ | ✓ | ✓ |
| Acceso global multi-sucursal | — | — | — | ✓ | ✓ |

`*` con nivel >= supervisor y `canWrite(..., minResponsibilityLevel: 2)`

## 3. Máquina de Estados — CheckLog

```
[checkin creado]
     │
     ▼
  pending-employee-validation  ──────► failed
     │ (empleado aprueba)             (empleado rechaza)
     ▼
   valid
     │
     ▼ (checkout válido con closed: true)
  [ciclo completo → daily report → heurística]
```

### Estados
- `valid`: checklog validado, cuenta en reportes y heurística
- `failed`: rechazado o fallido, no cuenta
- `pending-employee-validation`: solicitud manual pendiente de aprobación del empleado
- `incomplete_workday`: jornada sin cierre detectada

## 4. Máquina de Estados — Task

```
draft ──► assigned ──► in_progress ──► completed ──► validated
  │                        │               │              │
  │                        │               └──► rejected  │
  └──────────────────────────────────────────────────────┘
                   cancelled (desde cualquier estado por manager+)
```

### Time Compliance Status
```typescript
type TimeComplianceStatus =
  | "not_started"        // aún no iniciada
  | "on_time"            // en progreso antes del límite
  | "at_risk"            // a <20% del tiempo restante
  | "overdue"            // pasada la fecha límite sin completar
  | "completed_on_time"  // completada antes del límite
  | "completed_late";    // completada después del límite
```

## 5. Calendar — Estructura

```typescript
interface WeeklySchedule {
  monday: DaySchedule;
  tuesday: DaySchedule;
  // ...
  sunday: DaySchedule;
}

interface DaySchedule {
  disabled: boolean;
  shifts: Array<{
    id: string;
    start: { hour: number; minute: number };
    end: { hour: number; minute: number };
  }>;
}
```

Resolución de calendario (prioridad alta → baja):
1. Employee override (si `overridesDisabled = false`)
2. Branch override (si `overridesDisabled = false`)
3. Entity default schedule

Resolución de timezone (prioridad alta → baja):
1. `employee.address.timeZone` (si `enableRemoteWork = true`)
2. `branch.address.timeZone`
3. Timezone resuelto por calendario
4. `UTC` (fallback técnico)

## 6. Metadata de CheckLog

```typescript
interface CheckLogMetadata {
  tz: string;
  etz?: string;                    // timezone del empleado (remote work)
  ratioChecklog?: number;
  disableRatioChecklog?: boolean;
  enableDayTimeRange?: boolean;
  enableRemoteWork?: boolean;
  employeeResponsibility?: object;
  distance: number;
  realDateMarket: Date;
  adjustedTimestamp: Date | null;
  scheduleApplied: ScheduleApplied | null;
  updated: { uid: string; updatedAt: Date };
  requestUpdates: RequestUpdateEntry[];  // append-only, nunca se borran
  // campos de solicitud manual:
  manualRequest?: boolean;
  requestedByUid?: string;
  reason?: string;
  geoSource?: "branch_autofill" | "gps";
  timeSource?: "effective_calendar" | "explicit";
  autofilledFields?: string[];
  rejectionReason?: string;
}
```

### requestUpdates — pila de trazabilidad

Cada entrada es append-only (nunca se borra). `updated` siempre refleja la última entrada.

```typescript
interface RequestUpdateEntry {
  id: number;           // timestamp millis — único por documento
  createdAt: Date;
  action: "created" | "manual_request_created" | "manual_checkout_created" | "edited" | "approved" | "rejected";
  reason?: string;
  updateBy: string;     // uid del actor
  data: {               // valores propuestos/aplicados
    id: string;
    entityId: string;
    employeeId: string;
    status: CheckLog["status"];
    timestamp: Date;
    closed?: boolean;
  };
}
```

## 7. Códigos de Error Estándar

```typescript
// Auth
"auth/unauthorized"              // sin permisos
"auth/token_expired"             // token caducado

// CheckLog
"checklog/bad_request"
"checklog/manual_request_created"
"checklog/duplicate_pending"
"checklog/overlap_detected"
"checklog/day_disabled"
"checklog/calendar_not_resolved"
"checklog/employee_not_found"
"checklog/branch_geo_required"
"checklog/checkin_not_found"
"checklog/checkin_not_open"
"checklog/checkout_already_exists"
"checklog/rejection_reason_required"
"checklog/not_found"

// Task
"task/bad_request"
"task/not_found"
"task/unauthorized"
"task/evidence_required"
"task/note_not_found"

// Document
"documents/bad_request"
"documents/unauthorized"
"documents/not_found"
"documents/branch_required"
"documents/employee_required"
"documents/invalid_scope"
"documents/invalid_type"
"documents/invalid_visibility_roles"
"documents/invalid_acknowledgement_mode"
"documents/file_required"
"documents/file_too_large"
"documents/invalid_mime_type"
"documents/employee_not_found"
"documents/branch_not_found"
"documents/restricted_document_type"
"documents/already_archived"
"documents/acknowledgement_not_required"
"documents/acknowledgement_not_allowed"

// Employee
"employee/not_found"
"employee/branchId_required"

// Branch
"branch/not_found"
"checklog_update/not_found"
"checklog_update/updateId_required"
```

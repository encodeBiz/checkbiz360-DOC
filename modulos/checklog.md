# Módulo CheckLog — Asistencia y Solicitud Manual

## 1. Resumen

CheckLog gestiona el ciclo de asistencia: checkin → checkout. Cada par forma una jornada laboral. Los logs se almacenan en Firestore bajo `entities/{entityId}/checklogs/{checklogId}`.

Existen tres formas de crear checklogs:
1. **Flujo real** — app móvil en tiempo real (GPS, timestamp real)
2. **Solicitud manual** — supervisor crea jornada pendiente de aprobación del trabajador
3. **Edición** — supervisor propone cambios sobre un checklog existente

## 2. Máquina de Estados

```
[checkin creado]
     │
     ▼
pending-employee-validation ──────► failed
     │ (empleado aprueba)           (empleado rechaza)
     ▼
   valid
     │
     ▼ (checkout válido con closed: true)
  [ciclo completo → daily report → heurística]
```

| Estado | Descripción |
|---|---|
| `valid` | Validado, cuenta en reportes |
| `failed` | Rechazado, no cuenta |
| `pending-employee-validation` | Pendiente de aprobación del empleado |
| `incomplete_workday` | Jornada sin cierre detectada |

## 3. Solicitud Manual — Modo A (jornada completa)

Se usa cuando la jornada no existe. Crea checkin + checkout pendientes.

### Permisos

- Owner / admin de entidad
- Responsabilidad activa en la sucursal con `level >= supervisor`

### Endpoint

```http
POST /checkinbiz/requestManualChecklog
```

Cloud Function: `apiV100-firebaseEntryHttp-checkinbiz-requestManualChecklog`

### Payload

```typescript
{
  entityId: string;
  employeeId: string;
  branchId: string;
  date: string;        // YYYY-MM-DD — obligatorio en Modo A
  reason: string;
  checkinAt?: string;  // HH:mm — si no viene, el backend lo autocompleta desde el calendario
  checkoutAt?: string; // HH:mm — ídem
}
```

### Respuesta exitosa

```json
{
  "message": "Manual checklog request created",
  "code": "checklog/manual_request_created",
  "checkinId": "abc123",
  "checkoutId": "def456",
  "autofilledFields": ["geo", "checkinAt", "checkoutAt"]
}
```

## 4. Solicitud Manual — Modo B (solo checkout)

Se usa cuando el checkin ya existe y está válido pero sin checkout. El backend infiere la fecha del checkin.

### Payload

```typescript
{
  entityId: string;
  employeeId: string;
  branchId: string;
  checkinId: string;   // id del checkin válido y abierto
  reason: string;
  checkoutAt?: string; // HH:mm opcional
}
```

### Errores específicos Modo B

| Code | Status | Descripción |
|---|---|---|
| `checklog/checkin_not_found` | 404 | checkinId no existe |
| `checklog/checkin_not_open` | 409 | Checkin no válido, no es del empleado/branch, o no es tipo checkin |
| `checklog/checkout_already_exists` | 409 | Ya existe un checkout para ese checkin |

### Fix Timestamp (importante)

`findById` devuelve `doc.data()` sin convertir timestamps. El modo B usa el timestamp del checkin existente. La conversión correcta es:

```typescript
const checkinTs = (existingCheckin.timestamp as any)?.toDate?.() ?? new Date(existingCheckin.timestamp as any);
```

## 5. Autocompletado Backend

El frontend **no debe enviar** estos campos — el backend los resuelve:

| Campo | Fuente |
|---|---|
| `geo` | `branch.address.geo` → `metadata.geoSource = "branch_autofill"` |
| `timezone` | Prioridad: employee remote > branch > calendario > UTC |
| `checkinAt`/`checkoutAt` | Primer shift del calendario efectivo si no vienen |
| `ratioChecklog` | Branch |
| `scheduleApplied` | Calendario resuelto |
| `employeeResponsibility` | `employee_responsibilities` para `employeeId + branchId` |
| `realDateMarket` | Calculado por backend |

`metadata.timeSource`: `"effective_calendar"` o `"explicit"` (cuando front los envía).

## 6. Aprobación / Rechazo por el Trabajador

El trabajador aprueba o rechaza cada documento (checkin y checkout) de forma independiente usando el endpoint estándar `updateChecklog`. Cada documento tiene su propio `updateId`.

### Endpoint

```http
POST /checkinbiz/updateChecklog
```

Cloud Function: `apiV100-firebaseEntryHttp-checkinbiz-updateChecklog`

### Payload de aprobación

```typescript
{
  entityId: string;
  employeeId: string;
  branchId: string;
  id: string;         // checkinId o checkoutId del FCM payload
  updateId: number;   // updateId del FCM payload
  status: "valid";
  timestamp: string;  // ISO — timestamp del checkin/checkout
}
```

### Payload de rechazo

```typescript
{
  entityId: string;
  employeeId: string;
  branchId: string;
  id: string;
  updateId: number;
  status: "failed";
  timestamp: string;
  rejectionReason?: string;  // opcional — se guarda en metadata si se envía
}
```

### Comportamiento del backend

- El empleado autenticado debe ser propietario del checklog (`employee.uid == req.uid`)
- El backend aplica `update.data` + `status` enviado por el empleado — **nunca ignora el status del empleado**
- Si `status = "failed"`: elimina `closed: true` del documento (no cerrar un checkout rechazado)
- Siempre sincroniza `metadata.updated = { uid, updatedAt }` con la última acción
- Guarda `rejectionReason` en metadata si se proporciona

## 7. Estructura de Trazabilidad

### requestUpdates (append-only)

```typescript
interface RequestUpdateEntry {
  id: number;       // timestamp millis — único por documento
  createdAt: Date;
  action: "created" | "manual_request_created" | "manual_checkout_created" | "edited" | "approved" | "rejected";
  reason?: string;
  updateBy: string; // uid del actor
  data: {
    id: string;
    entityId: string;
    employeeId: string;
    status: CheckLog["status"];
    timestamp: Date;
    closed?: boolean;
  };
}
```

`metadata.updated` siempre refleja la última entrada de `requestUpdates`.

### Metadata de solicitud manual

```typescript
metadata.manualRequest = true;
metadata.requestedByUid = string;  // uid del supervisor/admin
metadata.reason = string;
metadata.geoSource = "branch_autofill";
metadata.timeSource = "effective_calendar" | "explicit";
metadata.autofilledFields = string[];
metadata.scheduleApplied = object | null;
```

El checkout referencia al checkin via el campo `checkin` (patrón estándar de ciclo).

## 8. Comportamiento con Reportes y Heurística

- Mientras `status = "pending-employee-validation"`: no cuentan en reportes, no afectan heurística
- Al aprobar: el par pasa a `valid`, forma ciclo completo y puede ser procesado por heurística
- Al rechazar: queda trazabilidad, no impacta métricas

## 9. Casos Límite

| Escenario | Comportamiento |
|---|---|
| Sin calendario efectivo y sin horas explícitas | Error `checklog/calendar_not_resolved` |
| Día deshabilitado sin turnos | Error `checklog/day_disabled` |
| Solapamiento con jornada válida | Error `checklog/overlap_detected` |
| Solicitud duplicada (mismo empleado/branch/fecha) | Error `checklog/duplicate_pending` |
| Branch sin geo | Error `checklog/branch_geo_required` |
| Checklog no encontrado en updateChecklog | 404 `checklog/not_found` |

## 10. Notificación FCM

El tipo de notificación es `update_checklog_pending`. Payload incluye:
- `updateId` — para identificar la entrada en `requestUpdates`
- `id` — docId del checklog
- `entityId`, `employeeId`, `requestAction: true`

El empleado recibe dos notificaciones independientes: una para el checkin, otra para el checkout.

## 11. Códigos de Error

```typescript
"checklog/bad_request"
"checklog/manual_request_created"      // código de éxito en respuesta 200
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
"auth/unauthorized"
```

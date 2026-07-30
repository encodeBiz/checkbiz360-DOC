# 03 — Contratos de API

Base: `https://api.checkbiz360.com/api/v1/checkinbiz`

El contrato es **el mismo que sirve Firebase hoy**, campo por campo y código por código. Este documento es la referencia contra la que se verifica el port: si algo aquí no coincide con lo que responde el contenedor, es un fallo del port, no una mejora.

---

## 1. `POST /checklogs` — crear fichaje

Reemplaza a `apiV100-firebaseEntryHttp-checkinbiz-createChecklog`.

### Auth

- **App móvil:** `Authorization: Bearer <sessionToken>` — el JWT que devuelve `POST /auth/validate`. El servidor extrae `employeeId` y `entityId` del payload y los mezcla en el body.
- **Administrador:** `Authorization: Bearer <Firebase ID token>` **y** `isAdmin: true` en el body. Requiere `canWrite(uid, entityId)`.

### Request

```json
{
  "entityId": "ent_123",
  "employeeId": "emp_456",
  "branchId": "br_789",
  "type": "checkin",
  "geo": { "lat": 39.5696, "lng": 2.6502 },
  "isAdmin": false
}
```

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `entityId` | string | sí | no vacío |
| `employeeId` | string | sí | no vacío |
| `branchId` | string | sí | validado más adelante que el resto: su ausencia da `employee/branchId_required`, no `bad_request` |
| `type` | `checkin` \| `checkout` \| `restin` \| `restout` | sí | |
| `geo.lat` | number | sí | −90..90 |
| `geo.lng` | number | sí | −180..180 |
| `isAdmin` | boolean | no | cambia el modo de auth |

El `user-agent` de la petición se usa como huella de dispositivo (`base64(user-agent)`) y se compara contra `trustedDevicesId`. **El cliente debe enviar el mismo `user-agent` que registró el dispositivo**, o el fichaje se rechaza con `auth/untrusted_device`.

### Respuesta `201`

```json
{
  "message": "Checklog created",
  "code": "checklog/created",
  "checkLog": { "…": "documento CheckLog completo, con metadata" }
}
```

### Errores

| HTTP | `code` | Cuándo |
|---|---|---|
| 400 | `checklog/bad_request` | payload inválido; incluye `details: string[]` |
| 401 | `auth/unauthorized` | token ausente o inválido |
| 401 | `auth/untrusted_device` | 2FA activo y dispositivo no registrado |
| 403 | `auth/unauthorized` | `isAdmin` sin permiso de escritura en la entidad |
| 404 | `employee/not_found` | |
| 404 | `employee/not_resposibility` | el empleado no tiene responsabilidad en esa sucursal *(el typo es del contrato actual y se conserva)* |
| 400 | `employee/branchId_required` | |
| 404 | `branch/not_found` | |
| 400 | `branch/inactive` | |
| 400 | `calendar/not_resolved` | no se pudo resolver el calendario efectivo |
| 400 | `checklog/day_disabled` | día deshabilitado, sin turnos, o festivo |
| 400 | `checklog/out_of_schedule` | el fichaje no cae en ningún turno con tolerancia |
| 400 | `checklog/out_of_radius` | fuera de geocerca — **el fichaje se guarda igualmente** con `status: "failed"` |
| 400 | `checklog/two_type_followed` | dos fichajes seguidos del mismo tipo |
| 400 | `checklog/invalid_checkin` \| `invalid_checkout` \| `invalid_restin` \| `invalid_restout` | secuencia inválida |
| 400 | `checklog/different_branches` | checkout en sucursal distinta a la del checkin |
| 400 | `checklog/invalid` | no se encuentra el checkin relacionado |
| 400 | `checklog/unknown_type` | |
| 500 | `checklog/internal_error` | |

`checklog/out_of_radius` añade detalle:

```json
{
  "error": "Outside allowed radius",
  "code": "checklog/out_of_radius",
  "details": { "distanceMeters": 412, "allowedRadiusMeters": 150, "branchId": "br_789" }
}
```

### Lo que se persiste

Además de los campos visibles, el fichaje congela en `metadata` el contexto del momento — es lo que consume la analítica y **no debe cambiar de forma**:

```
metadata.tz, metadata.etz                     zona horaria aplicada y la del empleado
metadata.ratioChecklog                        radio de geocerca vigente
metadata.disableRatioChecklog                 geocerca desactivada en la sucursal
metadata.enableRemoteWork                     empleado en remoto
metadata.enableDayTimeRange                   modo de rango estricto de jornada
metadata.realDateMarket                       instante real del marcaje
metadata.adjustedTimestamp                    instante real si el timestamp se ajustó al borde del turno
metadata.distance                             distancia al centro de la sucursal (m)
metadata.employeeResponsibility               puesto, responsabilidad y nivel en esa sucursal
metadata.scheduleApplied.{start,end,toleranceMinutes,source,shifts}
metadata.scheduleApplied.scheduleDay          día efectivo completo: fecha, weekday, isWorkingDay,
                                              isHoliday, disabled, shifts, plannedMinutes,
                                              breakMinutes, weekPlan, weekPlannedMinutes
metadata.requestUpdates[]                     historial de cambios (la primera entrada es "created")
metadata.updated                              último autor y fecha
deadline                                      solo en checkin: fin de turno + 6 h (lo usa el sanitizer)
```

---

## 2. `POST /checklogs/update` — corregir fichaje

Reemplaza a `apiV100-firebaseEntryHttp-checkinbiz-updateChecklog`.

### Auth

`Authorization: Bearer <Firebase ID token>`. El actor puede ser el administrador de la entidad (`canWrite`) o el propio empleado dueño del fichaje.

### Request — el circuito tiene dos pasos

**Paso 1 — el administrador propone:**

```json
{
  "entityId": "ent_123",
  "employeeId": "emp_456",
  "branchId": "br_789",
  "id": "chk_abc",
  "status": "valid",
  "timestamp": "2026-07-30T08:05:00.000Z",
  "reason": "El empleado avisó de que el móvil no tenía cobertura"
}
```

El fichaje pasa a `status: "pending-employee-validation"`, se apila una entrada en `metadata.requestUpdates` con `previousStatus` y `previousDate`, y el empleado recibe push + notificación in-app (`update_checklog_pending`).

**Paso 2 — el empleado responde:**

```json
{
  "entityId": "ent_123",
  "employeeId": "emp_456",
  "branchId": "br_789",
  "id": "chk_abc",
  "status": "valid",
  "updateId": 1753876543210,
  "rejectionReason": "No es correcto, entré a las 8:30"
}
```

`status: "valid"` acepta el cambio; `status: "failed"` lo rechaza, borra `closed` y guarda `rejectionReason`.

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `entityId`, `employeeId`, `branchId`, `id` | string | sí | |
| `status` | `valid` \| `failed` | no | por defecto `failed` |
| `timestamp` | fecha ISO | no | por defecto ahora; se normaliza a UTC |
| `reason` | string | sí en el paso 1 | |
| `updateId` | number | sí en el paso 2 | id de la entrada de `requestUpdates` |
| `rejectionReason` | string | no | solo se guarda si `status: "failed"` |

### Respuesta `200`

```json
{ "message": "Checklog created", "code": "checklog/updated" }
```

> El `message` dice "created" en una actualización. Es un error de copia del handler original; **se conserva tal cual** porque el port no cambia contrato. Corregirlo es una decisión posterior al cutover, y toca revisar antes si algún cliente lo compara.

### Errores

| HTTP | `code` |
|---|---|
| 400 | `checklog/bad_request` (con `details`) |
| 403 | `auth/unauthorized` |
| 404 | `employee/not_found` |
| 404 | `checklog/not_found` |
| 400 | `checklog_update/reason_required` |
| 400 | `checklog_update/updateId_required` |
| 400 | `checklog_update/bad_request` |
| 400 | `checklog_update/not_found` |
| 400 | `employee/branchId_required` |
| 404 | `branch/not_found` |
| 500 | `checklog/internal_error` |

---

## 3. `POST /checklogs/manual-request` — jornada manual

Reemplaza a `apiV100-firebaseEntryHttp-checkinbiz-requestManualChecklog`.

### Auth

`Authorization: Bearer <Firebase ID token>`. Permiso más laxo que las otras dos: owner/admin de la entidad **o** responsable de la sucursal con nivel ≥ 2.

### Request

**Modo jornada completa** — `date` obligatorio, `checkinId` ausente:

```json
{
  "entityId": "ent_123",
  "employeeId": "emp_456",
  "branchId": "br_789",
  "date": "2026-07-29",
  "checkinAt": "08:00",
  "checkoutAt": "16:00",
  "reason": "Olvidó fichar; jornada confirmada por el responsable"
}
```

`checkinAt` y `checkoutAt` son opcionales: si faltan, se rellenan con el primer turno del calendario efectivo de ese día y se listan en `autofilledFields`.

**Modo cierre** — `checkinId` presente; la fecha se infiere del checkin:

```json
{
  "entityId": "ent_123",
  "employeeId": "emp_456",
  "branchId": "br_789",
  "checkinId": "chk_abc",
  "checkoutAt": "16:00",
  "reason": "Se fue sin fichar la salida"
}
```

| Campo | Tipo | Obligatorio |
|---|---|---|
| `entityId`, `employeeId`, `branchId`, `reason` | string | sí |
| `date` | `YYYY-MM-DD` | sí salvo en modo cierre |
| `checkinId` | string | activa el modo cierre |
| `checkinAt`, `checkoutAt` | `HH:mm` | no |

### Respuesta `201`

```json
{
  "message": "Manual checklog request created",
  "code": "checklog/manual_request_created",
  "checkinId": "chk_new1",
  "checkoutId": "chk_new2",
  "autofilledFields": ["geo", "checkinAt", "checkoutAt"]
}
```

Ambos fichajes nacen en `pending-employee-validation` con `geo` de la sucursal y `userAgent: "manual-request"`; el empleado recibe una notificación por cada uno y debe confirmarlos vía `/checklogs/update`.

### Errores

| HTTP | `code` | Cuándo |
|---|---|---|
| 400 | `checklog/bad_request` | payload inválido (con `details`) |
| 403 | `auth/unauthorized` | sin permiso sobre la sucursal |
| 400 | `checklog/invalid_range` | rango imposible o `checkout` ≤ `checkin` |
| 400 | `checklog/branch_geo_required` | la sucursal no tiene geo y no se puede autorrellenar |
| 400 | `checklog/calendar_not_resolved` | |
| 400 | `checklog/day_disabled` | día sin turnos y sin horas explícitas |
| 404 | `checklog/branch_not_found` \| `checklog/employee_not_found` \| `checklog/checkin_not_found` | |
| 409 | `checklog/checkin_not_open` | el checkin no está válido/abierto para ese empleado y sucursal |
| 409 | `checklog/checkout_already_exists` | ya hay checkout para ese checkin |
| 409 | `checklog/duplicate_pending` | ya hay una solicitud pendiente ese día |
| 409 | `checklog/overlap_detected` | el rango solapa con fichajes válidos |
| 500 | `checklog/internal_error` | |

---

## 4. Verificación del port

Para dar la Fase 1 por buena, cada fila de las tres tablas de error debe reproducirse contra el contenedor y devolver **el mismo HTTP y el mismo `code`** que Firebase. Los cuatro casos que más fácil se rompen en un port y que hay que probar sí o sí:

1. `checklog/out_of_radius` — que el documento se guarde con `status: "failed"` además de responder 400.
2. `deadline` presente en los checkin — si falta, el sanitizer deja de cerrar jornadas incompletas y no lo notará nadie hasta fin de mes.
3. `metadata.scheduleApplied.scheduleDay.weekPlan` completo — lo consume la analítica de horas planificadas.
4. El checkout marca `closed: true` en su checkin asociado.

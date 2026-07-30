# 01 — Estado actual (As-Is)

Dónde vive hoy cada pieza del fichaje, quién la llama y de qué depende.

---

## 1. Las tres funciones

Todas son `https.onRequest` de Firebase Functions v2, en el codebase por defecto (`functions/`), exportadas desde `src/services-saas/checkinbiz/firebase-checkinbiz-http/index.ts` y anidadas bajo `apiV100.firebaseEntryHttp.checkinbiz.*`.

### `createChecklog`

`firebase-checkinbiz-http/create-checklog.ts` → `interfaces/http/checklog/createChecklogController.ts` (436 líneas) → `application/use-cases/checklog/CreateChecklog.ts`.

Configuración: `cpu: 1`, `concurrency: 20`, `memory: 512MiB`, `maxInstances: 20`. Acepta un ping `{_warmup: true}` que responde `200` sin tocar nada — lo usa `criticalHandler` para calentar la instancia.

Es la función con más lógica de las tres. En orden:

1. Valida el payload (`entityId`, `employeeId`, `type` ∈ checkin/checkout/restin/restout, `geo.lat`/`geo.lng` en rango).
2. Si `isAdmin`, comprueba `canWrite(uid, entityId)`.
3. Deriva un `deviceId` como base64 del `user-agent`.
4. Carga empleado y sus responsabilidades en la sucursal; sin responsabilidad → `404 employee/not_resposibility`.
5. **Dispositivo de confianza**: si `employee.enableA2F !== false` y no es admin, el `deviceId` debe estar en `security/trustedDevicesId` → si no, `401 auth/untrusted_device`.
6. Carga la sucursal; valida que exista y esté `active`.
7. **Resuelve el calendario efectivo** (`ResolveEffectiveDayUseCase`, herencia entidad → sucursal → empleado): zona horaria, turnos del día, festivos, tolerancia.
8. Calcula `weekPlan` y `weekPlannedMinutes` — los minutos planificados de **cada día de la semana vigente**, que se congelan dentro del checklog. Sin esto, un día sin marcaje sería indistinguible entre "no vino" y "no le tocaba", y consultar el calendario después daría el horario *actual*, no el vigente entonces.
9. Elige el turno en el que cae el fichaje (con tolerancia); fuera de turno → `400 checklog/out_of_schedule`.
10. Construye el `CheckLog` con un `metadata.scheduleApplied.scheduleDay` completo (día efectivo, turnos, `plannedMinutes`, `breakMinutes`, `weekPlan`).
11. Si `enableDayTimeRange`, ajusta el `timestamp` al borde del turno y guarda el real en `metadata.adjustedTimestamp`.
12. **Geocerca**: si la sucursal no la tiene desactivada y el empleado no es remoto, calcula la distancia Haversine al centro de la sucursal. Fuera de radio → **se persiste igualmente** el checklog con `status: "failed"` y `failedCode: "checklog/out_of_radius"`, y se responde `400`.
13. Guarda con `status: "valid"`; si es `checkout`, marca `closed: true` en el checkin asociado.

`CreateChecklog` (el caso de uso) es quien impone la máquina de estados: no dos fichajes seguidos del mismo tipo, `checkout` solo tras `checkin`/`restout`, `restin` solo tras `checkin`/`restout`, misma sucursal en toda la jornada, y marca `isSuspect` si la jornada dura menos de 3 h o más de 10 h.

### `updateChecklog`

`firebase-checkinbiz-http/update-checklog.ts` → `interfaces/http/checklog/updateChecklogController.ts` (239 líneas) → `UpdateChecklog`.

Sin configuración especial (defaults). Implementa el **circuito de doble confirmación** de una corrección de fichaje:

- Un administrador propone un cambio con `reason` → el checklog pasa a `status: "pending-employee-validation"` y se apila una entrada en `metadata.requestUpdates` con el estado y la fecha previos. Se envía notificación push + in-app al empleado (`update_checklog_pending`).
- El empleado responde con `updateId` → se resuelve esa entrada, aplicando `status` `valid` o `failed`. Si rechaza (`failed`), se borra `closed` con `FieldValue.delete()` y se guarda `rejectionReason`.

El caso `isAdminEmployee` (el propio usuario es admin de la entidad) permite ambas cosas.

### `requestManualChecklog`

`firebase-checkinbiz-http/request-manual-checklog.ts` → `interfaces/http/checklog/requestManualChecklogController.ts` → `application/use-cases/checklog/RequestManualChecklogCreation.ts` (332 líneas).

Configuración: `cpu: 1`, `concurrency: 20`, `memory: 256MiB`, `maxInstances: 10`.

Permiso más fino que las otras dos: `canWrite(uid, entityId, {branchId, includeBranchResponsibility: true, minResponsibilityLevel: 2})` — un supervisor de la sucursal basta, no hace falta ser owner/admin.

Dos modos:

- **Jornada completa** (`date`, sin `checkinId`): crea checkin + checkout en un `batch`, ambos en `pending-employee-validation`. Si no se dan `checkinAt`/`checkoutAt`, los rellena desde el primer turno del calendario efectivo y lo anota en `autofilledFields`. La geo se autorrellena con la de la sucursal (`geoSource: "branch_autofill"`).
- **Cierre** (`checkinId`): solo crea el checkout de un checkin abierto y válido. Rechaza si ya existe checkout para ese checkin.

Verifica duplicados (`findPendingByEmployeeBranchDate`) y solapes con fichajes válidos (`findOverlapInRange`) antes de escribir.

---

## 2. Auth: quién presenta qué token

| Función | Cliente | Token | Verificación |
|---|---|---|---|
| `createChecklog` | App móvil | `sessionToken` — JWT firmado con `JWT_2FA_SECRET`, emitido por `/auth/validate` | `validateTokenJWT` |
| `createChecklog` (`isAdmin: true`) | — | Firebase ID token | `validateToken` + `canWrite` |
| `updateChecklog` | App móvil (`access_token`) y back office | Firebase ID token | `validateToken` |
| `requestManualChecklog` | Back office | Firebase ID token | `validateToken` + `canWrite` con nivel de responsabilidad |

Detalle que conviene no perder de vista: la app usa **dos tokens distintos** según la operación. Ficha con el JWT de empleado y confirma correcciones con el ID token de Firebase (`AppConstants.accessTokenKey`).

---

## 3. Clientes

**App móvil** (`checkbiz360`, Flutter) — `lib/core/constants/app_constants.dart` guarda la URL completa de cada función, distinta en dev y prod:

- `createChecklogEndpoint` → `attendance_remote_datasource.dart::createLog`
- `updateChecklogEndpoint` → `attendance_remote_datasource.dart::updateChecklog`

**Back office** (`encodebiz-front-saas`, Next.js) — no llama a las funciones directamente: pasa por `/api/proxy/<handler>`, y `src/lib/http/serverBackendProxy.ts` resuelve la URL destino desde variables de entorno:

- `checkinbiz_update_log` → `NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_LOG` (usado por `report.service.ts::updateChecklog`)
- `checkinbiz_request_manual_checklog` → `NEXT_BACKEND_URI_CHECKINBIZ_REQUEST_MANUAL_CHECKLOG` (usado por `manualChecklog.service.ts`)
- `checkinbiz_create_log` → registrado en la allowlist, **sin ningún consumidor en el código del front**

Consecuencia operativa: mover el back office es cambiar una variable de entorno. Mover la app requeriría publicar en las stores.

---

## 4. Dependencias del código a portar

| Dependencia | Dónde está hoy | Situación en `encodebiz-api` |
|---|---|---|
| `ResolveEffectiveDayUseCase` | `application/calendar/` | ✅ ya en `@encodebiz/shared` |
| `FirestoreCalendarRepository` | `infrastructure/repository/` | ✅ ya en `services/checkinbiz` |
| `EmployeeFirestoreRepository` | `infrastructure/repository/` | ✅ ya en `services/checkinbiz` (con `findResponsibilities` y `findSecurity`) |
| `FirestoreBranchRepository` | `infrastructure/repository/` | ⚠️ en `checkinbiz` solo existe la parte de patrones; falta `findById` (sí está en `tasks`) |
| `FirestoreChecklogRepository` | `infrastructure/repository/` | ❌ falta (la interfaz `ChecklogRepository` sí existe) |
| `CreateChecklog` / `UpdateChecklog` / `RequestManualChecklogCreation` | `application/use-cases/checklog/` | ❌ faltan |
| `canWrite` | `core/auth/permissions/` | ⚠️ copia idéntica en `tasks` |
| `validateToken` / `validateTokenJWT` | `core/shared/utils/` | ⚠️ copias idénticas en `tasks` y `documents` |
| `getDistanceInMeters` | `core/shared/utils/` | ❌ falta |
| `CheckbizSentNotificationApp` + `messages` | `application/notifications/` | ⚠️ copias idénticas en `tasks` y `documents`; incluyen ya la clave `update_checklog_pending` |
| `FirestoreAppNotificationsRepository` | `core/notifications/` | ✅ ya en `@encodebiz/shared` |

Las marcas ⚠️ son el duplicado ya registrado como deuda en el TDR-001 de `tasks-service`. Este trabajo lo cierra en vez de ampliarlo — ver [ADR-003](./adr/ADR-003-promocion-a-shared-sin-tercera-copia.md).

---

## 5. Lo reactivo que NO se toca

Estos triggers y schedules operan sobre la colección `entities/{entityId}/checklogs` y **seguirán disparándose exactamente igual** cuando quien escriba sea el contenedor:

| Pieza | Qué hace |
|---|---|
| `onWhriteChecklog` | Procesamiento del dato al crear/actualizar un fichaje |
| `onChecklogSync` | Envío del fichaje al servicio `sync` → PostgreSQL |
| `onChecklogWebhook` | Webhooks salientes hacia integraciones del cliente |
| `sanitizer-checklogs` | Cierre de jornadas incompletas vencidas (usa el campo `deadline`) |
| `dailyCollectorData` | Agregación diaria del reporte |
| `onCreateIssues` | Incidencias derivadas de fichajes anómalos |

Es la razón de que no haya migración de datos: la frontera se dibuja en el HTTP, no en Firestore.

---

## 6. Limitaciones del estado actual

1. **Cold start en el camino crítico.** Un fichaje es la primera petición del día de ese empleado: casi siempre toca instancia fría.
2. **Despliegue acoplado.** Cambiar una línea del cálculo de geocerca obliga a desplegar todo el bundle de Functions.
3. **Contrato disperso.** La lógica del fichaje vive en Firebase mientras el calendario que la alimenta ya vive en el servidor: dos despliegues para un mismo flujo.
4. **Duplicación creciente.** Cada servicio migrado se ha llevado su propia copia de notificaciones, repos y auth.

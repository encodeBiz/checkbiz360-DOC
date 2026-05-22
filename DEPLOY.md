# Deploy — Entornos y Comandos

## 1. Entornos

| Entorno | Firebase Project | Base URL |
|---|---|---|
| Dev | `dev-encodebiz` | `https://us-central1-dev-encodebiz.cloudfunctions.net/` |
| Prod | `encodebiz-saas` | `https://us-central1-encodebiz-saas.cloudfunctions.net/` |

## 2. Versión API

Todas las funciones siguen el patrón:

```
apiV100-{tipo}-{servicio}-{nombre}
```

Ejemplo:
```
apiV100-firebaseEntryHttp-checkinbiz-tasksHandler
```

## 3. Comandos de deploy

### Dev

```bash
npm run deploy:function:dev -- <nombre-funcion> [nombre-funcion2 ...]
```

### Prod

```bash
npm run deploy:function:prod -- <nombre-funcion> [nombre-funcion2 ...]
```

## 4. Funciones activas

### HTTP Functions

| Nombre | Endpoint base |
|---|---|
| `apiV100-firebaseEntryHttp-checkinbiz-tasksHandler` | `/tasks` |
| `apiV100-firebaseEntryHttp-checkinbiz-documentsHandler` | `/documents` |
| `apiV100-firebaseEntryHttp-checkinbiz-requestManualChecklog` | `/checkinbiz/requestManualChecklog` |
| `apiV100-firebaseEntryHttp-checkinbiz-updateChecklog` | `/checkinbiz/updateChecklog` |
| `apiV100-firebaseEntryHttp-checkinbiz-createChecklog` | `/checkinbiz/createChecklog` |
| `apiV100-firebaseEntryHttp-checkinbiz-calendarHandler` | `/calendar` |
| `apiV100-firebaseEntryHttp-checkinbiz-createEmployee` | `/checkinbiz/createEmployee` |
| `apiV100-firebaseEntryHttp-checkinbiz-updateEmployee` | `/checkinbiz/updateEmployee` |
| `apiV100-firebaseEntryHttp-checkinbiz-deleteEmployee` | `/checkinbiz/deleteEmployee` |
| `apiV100-firebaseEntryHttp-checkinbiz-createBranch` | `/checkinbiz/createBranch` |
| `apiV100-firebaseEntryHttp-checkinbiz-updateBranch` | `/checkinbiz/updateBranch` |
| `apiV100-firebaseEntryHttp-checkinbiz-deleteBranch` | `/checkinbiz/deleteBranch` |
| `apiV100-firebaseEntryHttp-checkinbiz-employeesExportHandler` | `/checkinbiz/export/employees` |
| `apiV100-firebaseEntryHttp-checkinbiz-checkbizNotifications` | `/checkinbiz/notifications` |
| `apiV100-firebaseEntryHttp-users` | `/users` |
| `apiV100-firebaseEntryHttp-sendEmail` | `/email` |
| `apiV100-firebaseEntryHttp-merlinIa` | `/merlin` |
| `apiV100-firebaseEntryHttp-stripeWebhook` | `/stripeWebhook` |
| `apiV100-firebaseEntryHttp-criticalHandler` | `/auth/login`, `/auth/validate`, `/calendar` (GET) |

### Firestore Triggers

| Nombre | Trigger |
|---|---|
| `apiV100-firebaseFirestoreTriggersCheckinBiz-onChecklogWrite` | `entities/{entityId}/checklogs/{checklogId}` — onWrite |
| `apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateIssues` | issues — onCreate |
| `apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateEmployee` | `entities/{entityId}/employees/{employeeId}` — onCreate |

## 5. Deploy batch — rama `feat/documental-manage`

Funciones modificadas en la rama actual. Usar este comando para sincronizar dev:

```bash
npm run deploy:function:dev -- \
  apiV100-firebaseEntryHttp-checkinbiz-calendarHandler \
  apiV100-firebaseEntryHttp-checkinbiz-tasksHandler \
  apiV100-firebaseEntryHttp-checkinbiz-documentsHandler \
  apiV100-firebaseEntryHttp-checkinbiz-requestManualChecklog \
  apiV100-firebaseEntryHttp-checkinbiz-updateChecklog \
  apiV100-firebaseEntryHttp-checkinbiz-createChecklog \
  apiV100-firebaseEntryHttp-checkinbiz-createEmployee \
  apiV100-firebaseEntryHttp-checkinbiz-updateEmployee \
  apiV100-firebaseEntryHttp-checkinbiz-deleteEmployee \
  apiV100-firebaseEntryHttp-checkinbiz-createBranch \
  apiV100-firebaseEntryHttp-checkinbiz-updateBranch \
  apiV100-firebaseEntryHttp-checkinbiz-deleteBranch \
  apiV100-firebaseEntryHttp-checkinbiz-employeesExportHandler \
  apiV100-firebaseEntryHttp-checkinbiz-checkbizNotifications \
  apiV100-firebaseEntryHttp-users \
  apiV100-firebaseEntryHttp-sendEmail \
  apiV100-firebaseEntryHttp-merlinIa \
  apiV100-firebaseEntryHttp-stripeWebhook \
  apiV100-firebaseFirestoreTriggersCheckinBiz-onChecklogWrite \
  apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateIssues \
  apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateEmployee \
  apiV100-firebaseEntryHttp-criticalHandler
```

Mismo bloque para prod reemplazando `deploy:function:dev` por `deploy:function:prod`.

## 6. Qué cambió por función (rama actual)

| Función | Cambios |
|---|---|
| `calendarHandler` | Fix `dateLocal` query param ignorado + fallback `DateTime.utc()` → `DateTime.now().setZone(tz)` |
| `tasksHandler` | Módulo tasks completo + `canManageTask` unificado (supervisor puede crear/editar/cancelar/notas/recursos en su sucursal sin asignarse) |
| `documentsHandler` | Documents Manage V1 completo: scope=employee no requiere branchId, `DocumentStorageService` employee path corregido, `employeeAllFlow` fan-out (entity+branch+employee), `total` en todos los listados, cursor pagination, `branch` solo en scope=branch, `UpdateDocument` devuelve `DocumentWithAckStatus`, GET `:id/acks`, notificaciones fix (push falla no bloquea in-app) |
| `requestManualChecklog` | Modo A (jornada completa) + Modo B (solo checkout) + fix Firestore Timestamp en `_executeCheckoutOnly` |
| `updateChecklog` | Fix status ignorado en resolución empleado + fix `closed` en checkout rechazado + sync `metadata.updated` + guard 404 checklog not found + `rejectionReason` opcional |
| `createChecklog` | `canWrite` con branch responsibility + detección de overlap en repo + fix `resolveEffectiveDay` medianoche |
| `createEmployee` | Controller actualizado |
| `updateEmployee` | Fix search index duplicado: `FirestoreSearchIndexRepository.create()` usa doc ID determinístico por path + `set()` en lugar de `create()` |
| `deleteEmployee` | Fix `FirestoreSearchIndexRepository.delete()` — delete directo por doc ID (sin query) |
| `createBranch` | Fix search index: `set()` idempotente (sin duplicados en retries) |
| `updateBranch` | Fix search index duplicado en cada actualización: mismo fix que `updateEmployee` |
| `deleteBranch` | Fix `FirestoreSearchIndexRepository.delete()` — delete directo por doc ID |
| `employeesExportHandler` | CSV export (nuevo) |
| `checkbizNotifications` | Serialización FCM + normalización de idioma |
| `users` | Controllers `assignUser` + `createUser` |
| `sendEmail` | Email service + mailer controller |
| `merlinIa` | API express proxy |
| `stripeWebhook` | Fix selección de secret: usaba siempre `STRIPE_WEBHOOK` (prod) — ahora usa `STRIPE_WEBHOOK_SECRET_TEST` cuando `ENV !== "production"` |
| `onChecklogWrite` | `writeController` patterns |
| `onCreateIssues` | Issues trigger |
| `onCreateEmployee` | Fix search index: `FirestoreSearchIndexRepository` compartido — mismo fix que branches/employees |
| `criticalHandler` | **NUEVA** — Express bundle startup: `POST /auth/login`, `POST /auth/validate` (+ warm-up ping a createChecklog), `GET /calendar`. `1GiB, 2CPU, concurrency:200` |
| `createChecklog` | Guard `_warmup: true` — responde 200 inmediato sin procesar, para warm-up desde criticalHandler |

## 7. URLs de dev conocidas

```
requestManualChecklog:
  https://us-central1-dev-encodebiz.cloudfunctions.net/apiV100-firebaseEntryHttp-checkinbiz-requestManualChecklog

updateChecklog:
  https://apiv100-firebaseentryhttp-checkinbiz-updatecheckl-3bnjgtprva-uc.a.run.app

tasksHandler (local emulator):
  http://127.0.0.1:5001/encodebiz-services/us-central1/apiV100-firebaseEntryHttp-checkinbiz-tasksHandler/tasks

documentsHandler:
  https://us-central1-dev-encodebiz.cloudfunctions.net/apiV100-firebaseEntryHttp-checkinbiz-documentsHandler
```

Nota: `documentsHandler` es la URI base del handler Express. Las rutas funcionales se resuelven sobre esa base, por ejemplo `/documents`, `/documents/:id/download`, `/documents/:id/ack`.

## 8. Deploy recomendado — Documents Manage

### Dev

```bash
npm run deploy:function:dev -- apiV100-firebaseEntryHttp-checkinbiz-documentsHandler
```

### Prod

Pendiente hasta validar Fase 6 Frontend/App y QA en dev.

```bash
npm run deploy:function:prod -- apiV100-firebaseEntryHttp-checkinbiz-documentsHandler
```

---

## 10. Fix Frontend — BUG-5: Empleados inactivos en detalle de sucursal

### Problema

Al desasignar un branch a un empleado (`active: 0` en `EmployeeEntityResponsibility`), el empleado seguía apareciendo como activo en la lista de empleados del detalle del branch. El filtro usaba `employee.status !== 'active'` (estado general del empleado) en lugar de `item.active === 0` (estado de la asignación al branch).

### Archivos modificados (frontend)

| Archivo | Cambio |
|---|---|
| `branch/[id]/detail/detail.controller.tsx` | Eliminado filtro `employee.status !== 'active'`; nuevo filtro `item.active !== 0`; `showInactive` state + `onToggleInactive`; estilo visual en columnas (opacity 0.45 + Tooltip) para filas inactivas |
| `branch/[id]/detail/components/EmployeeList.tsx` | Añadido Switch "Mostrar inactivos" con props `showInactive` + `onToggleInactive` |
| `branch/[id]/detail/Detail.tsx` | Props `showInactive` + `onToggleInactive` añadidas y pasadas a `EmployeeList` |
| `branch/[id]/detail/page.tsx` | Destructura y pasa `showInactive` + `onToggleInactive` desde controller a `Detail` |
| `locales/es/common.json` | +`sucursal.employeeInactive`, `sucursal.showInactive` |
| `locales/en/common.json` | +`sucursal.employeeInactive`, `sucursal.showInactive` |

### Comportamiento resultante

- Por defecto solo se muestran empleados con `active !== 0`.
- El Switch "Mostrar inactivos" revela también los desasignados.
- Filas inactivas aparecen con `opacity: 0.45`, texto en color `text.disabled` y un Tooltip explicativo en la columna de nombre.
- Las filas inactivas no son clickables (no navegan al detalle del empleado).

### No requiere deploy de funciones

Cambio exclusivamente frontend. No hay modificaciones en Cloud Functions ni Firestore.

---

## 9. Deploy — QA Bugs + Auth + 2FA Backoffice (sesión 2025-05-22)

### Funciones modificadas

| Función | Cambio |
|---|---|
| `apiV100-firebaseEntryHttp-checkinbiz-tasksHandler` | BUG-1: `updateTaskStatus` — `FieldValue.delete()` en cancelación/draft; BUG-2: `updateTask` — limpiar campos de notificación correctamente |
| `apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateIssues` | BUG-4a: título notificación `"Issue received"` → `"Checkbiz360"` |
| `apiV100-firebaseEntryHttp-enable2FAUser` | **NUEVA** — Genera secreto TOTP para usuario backoffice |
| `apiV100-firebaseEntryHttp-verify2FAUser` | **NUEVA** — Verifica código TOTP y activa 2FA |
| `apiV100-firebaseEntryHttp-get2FAUserStatus` | **NUEVA** — Consulta si el usuario tiene 2FA activo |

### Dev

```bash
# Bugs QA
npm run deploy:function:dev -- \
  apiV100-firebaseEntryHttp-checkinbiz-tasksHandler \
  apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateIssues

# 2FA usuario backoffice (nuevas)
npm run deploy:function:dev -- \
  apiV100-firebaseEntryHttp-enable2FAUser \
  apiV100-firebaseEntryHttp-verify2FAUser \
  apiV100-firebaseEntryHttp-get2FAUserStatus

# Índices Firestore (BUG-4b: índice issues status → state)
firebase deploy --only firestore:indexes --project dev-encodebiz
```

### Prod

```bash
npm run deploy:function:prod -- \
  apiV100-firebaseEntryHttp-checkinbiz-tasksHandler \
  apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateIssues \
  apiV100-firebaseEntryHttp-enable2FAUser \
  apiV100-firebaseEntryHttp-verify2FAUser \
  apiV100-firebaseEntryHttp-get2FAUserStatus

firebase deploy --only firestore:indexes --project encodebiz-saas
```

### Variables de entorno frontend — añadir en `.env.production`

```bash
NEXT_PUBLIC_BACKEND_URI_STATUS2FA_USER=https://apiv100-firebaseentryhttp-get2fauserstatus-3bnjgtprva-uc.a.run.app
NEXT_PUBLIC_BACKEND_URI_ENABLE2FA_USER=https://apiv100-firebaseentryhttp-enable2fauser-3bnjgtprva-uc.a.run.app
NEXT_PUBLIC_BACKEND_URI_VERIFY2FA_USER=https://apiv100-firebaseentryhttp-verify2fauser-3bnjgtprva-uc.a.run.app
```

### Checklist pre-deploy

- [ ] `npx eslint src/...` sin errores (`✖ 0 problems`)
- [ ] `npx tsc --noEmit --skipLibCheck` sin errores
- [ ] Verificar que las URLs generadas por Firebase en dev coinciden con las del `.env.development`
- [ ] Añadir las 3 variables 2FA al `.env.production` antes de deploy de frontend
- [ ] Verificar Firestore Rules: `users/{uid}/security/**` solo accesible por el propio usuario

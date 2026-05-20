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
  apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateEmployee
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

# Entornos y Cloud Functions — Referencia rápida

> Última actualización: 2026-05-22

---

## Proyectos Firebase

| Entorno | Project ID | Cloud Run hash |
|---------|-----------|----------------|
| **Producción** | `encodebiz-services` | `jxvyznhhja` |
| **Desarrollo** | `dev-encodebiz` | `3bnjgtprva` |

### Patrón de URL — Cloud Run v2

```
https://apiv100-firebaseentryhttp-{slug}-{HASH}-uc.a.run.app
```

El `{slug}` es el nombre completo de la función exportada en **minúsculas**, truncado a **49 caracteres** si supera ese límite.

**Ejemplo de truncación:**
- Función: `apiV100-firebaseEntryHttp-checkinbiz-createEmployee`
- Slug completo: `apiv100-firebaseentryhttp-checkinbiz-createemployee` (51 chars → se trunca a 49)
- Slug final: `apiv100-firebaseentryhttp-checkinbiz-createemploy`

---

## Archivos de entorno

| Archivo | Entorno | Notas |
|---------|---------|-------|
| `.env.development` | DEV (`dev-encodebiz`) | Todas las URLs apuntan al hash `jxvyznhhja` |
| `.env.production` | PROD (`encodebiz-services`) | Hash `3bnjgtprva` |
| `.env.productionxxx` | Archivo transitorio (no usar) | Mix de hashes — ignorar |

---

## Mapa completo: Variable → Cloud Function

### Core / Entity

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_CREATE_ENTITY` | `entity.createEntity` | `apiv100-firebaseentryhttp-entity-createentity` |
| `NEXT_PUBLIC_BACKEND_URI_UPDATE_ENTITY` | `entity.updateEntity` | `apiv100-firebaseentryhttp-entity-updateentity` |
| `NEXT_PUBLIC_BACKEND_URI_DELETE_ENTITY` | `entity.deleteEntity` | `apiv100-firebaseentryhttp-entity-deleteentity` |
| `NEXT_PUBLIC_BACKEND_URI_UPDATE_BRANDNG_ENTITY` | `entity.updateEntityBranding` | `apiv100-firebaseentryhttp-entity-updateentitybran` *(truncado)* |

### Users

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_CREATE_USER` | `users.createUsers` | `apiv100-firebaseentryhttp-users-createusers` |
| `NEXT_PUBLIC_BACKEND_URI_ASSING_USER` | `users.assingUser` | `apiv100-firebaseentryhttp-users-assinguser` |
| `NEXT_PUBLIC_BACKEND_URI_RECOVERY_PASS` | `users.recoveryPassUsers` | `apiv100-firebaseentryhttp-users-recoverypassusers` |

### Subscriptions

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_SUBCRIBE` | `subscriptions.subscribe` | `apiv100-firebaseentryhttp-subscriptions-subscribe` |
| `NEXT_PUBLIC_BACKEND_URI_CONFIGBILLING` | `subscriptions.configBilling` | `apiv100-firebaseentryhttp-subscriptions-configbil` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_UNSUBCRIBE` | `subscriptions.unsubscribe` | `apiv100-firebaseentryhttp-subscriptions-unsubscri` *(truncado)* |

### Passinbiz

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_CREATE_HOLDER` | `passinbiz.createHolder` | `apiv100-firebaseentryhttp-passinbiz-createholder` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_VALIDATE_HOLDER` | `passinbiz.validateHolder` | `apiv100-firebaseentryhttp-passinbiz-validateholde` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_IMPORT_HOLDER` | `passinbiz.importHoldersFromCsv` | `apiv100-firebaseentryhttp-passinbiz-importholders` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_UPDATE_HOLDER` | `passinbiz.updateHolder` | `apiv100-firebaseentryhttp-passinbiz-updateholder` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_STATS` | `passinbiz.statsGetdata` | `apiv100-firebaseentryhttp-passinbiz-statsgetdata` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_CREATE_STAFF` | `passinbiz.createStaff` | `apiv100-firebaseentryhttp-passinbiz-createstaff` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_DELETE_STAFF` | `passinbiz.deleteStaff` | `apiv100-firebaseentryhttp-passinbiz-deletestaff` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_VALIDATE_STAFF` | `passinbiz.validateStaff` | `apiv100-firebaseentryhttp-passinbiz-validatestaff` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_UPDATE_STAFF` | `passinbiz.updateStaff` | `apiv100-firebaseentryhttp-passinbiz-updatestaff` |

> ⚠️ **`PASSINBIZ_UPDATE_STAFF`** — Esta función **no está desplegada en dev** (`dev-encodebiz`). Usar la URL de prod si se necesita, o no invocar en local.

### Passinbiz — Eventos

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_CREATE_EVENT` | `createEvent` | `apiv100-firebaseentryhttp-createevent` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_UPDATE_EVENT` | `updateEvent` | `apiv100-firebaseentryhttp-updateevent` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_DELETE_EVENT` | `deleteEvent` | `apiv100-firebaseentryhttp-deleteevent` |

### Checkinbiz

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_CREATE_EMPLOYEE` | `checkinbiz.createEmployee` | `apiv100-firebaseentryhttp-checkinbiz-createemploy` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_UPDATE_EMPLOYEE` | `checkinbiz.updateEmployee` | `apiv100-firebaseentryhttp-checkinbiz-updateemploy` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_DELETE_EMPLOYEE` | `checkinbiz.deleteEmployee` | `apiv100-firebaseentryhttp-checkinbiz-deleteemploy` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_VALIDATE_EMPLOYEE` | `checkinbiz.validateEmployee` | `apiv100-firebaseentryhttp-checkinbiz-validateempl` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_ADD_DEVICE` | `checkinbiz.addDeviceEmployee` | `apiv100-firebaseentryhttp-checkinbiz-adddeviceemp` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_CREATE_SUCURSAL` | `checkinbiz.createBranch` | `apiv100-firebaseentryhttp-checkinbiz-createbranch` |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_UPDATE_SUCURSAL` | `checkinbiz.updateBranch` | `apiv100-firebaseentryhttp-checkinbiz-updatebranch` |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_DELETE_SUCURSAL` | `checkinbiz.deleteBranch` | `apiv100-firebaseentryhttp-checkinbiz-deletebranch` |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_CREATE_LOG` | `checkinbiz.createChecklog` | `apiv100-firebaseentryhttp-checkinbiz-createcheckl` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_UPDATE_LOG` | `checkinbiz.updateChecklog` | `apiv100-firebaseentryhttp-checkinbiz-updatecheckl` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_GENERATE_REPORT` | `checkinbiz.generateReport` | `apiv100-firebaseentryhttp-checkinbiz-generaterepo` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_RESPONSABILITY_HANDLER` | `checkinbiz.responsibilitiesHandler` | `apiv100-firebaseentryhttp-checkinbiz-responsibili` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_STATS` | `checkinbiz.analyzeHeuristic` | `apiv100-firebaseentryhttp-checkinbiz-analyzeheuri` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_STATS_PANEL` | `checkinbiz.checkbizStatsController` | `apiv100-firebaseentryhttp-checkinbiz-checkbizstat` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_GEO` | `geo` | `apiv100-firebaseentryhttp-geo` |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_CALENDAR_HANDLER` | `checkinbiz.calendarHandler` | `apiv100-firebaseentryhttp-checkinbiz-calendarhand` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_TASKS_HANDLER` | `checkinbiz.tasksHandler` | `apiv100-firebaseentryhttp-checkinbiz-taskshandler` + `/tasks` |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_NOTIFICATIONS` | `checkinbiz.checkbizNotifications` | `apiv100-firebaseentryhttp-checkinbiz-checkbiznoti` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_REQUEST_MANUAL_CHECKLOG` | `checkinbiz.requestManualChecklog` | `apiv100-firebaseentryhttp-checkinbiz-requestmanua` *(truncado)* |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_DOCUMENTS_HANDLER` | `checkinbiz.documentsHandler` | `apiv100-firebaseentryhttp-checkinbiz-documentshan` *(truncado)* + `/documents` |

### Auth — Empleados (app móvil)

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_ENABLE2AF_EMPLOYEE` | `enable2FA` | `apiv100-firebaseentryhttp-enable2fa` |
| `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_VERIFY2AF_EMPLOYEE` | `verify2FA` | `apiv100-firebaseentryhttp-verify2fa` |

### Auth — Usuarios Backoffice (2FA)

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_ENABLE2FA_USER` | `enable2FAUser` | `apiv100-firebaseentryhttp-enable2fauser` |
| `NEXT_PUBLIC_BACKEND_URI_VERIFY2FA_USER` | `verify2FAUser` | `apiv100-firebaseentryhttp-verify2fauser` |
| `NEXT_PUBLIC_BACKEND_URI_STATUS2FA_USER` | `get2FAUserStatus` | `apiv100-firebaseentryhttp-get2fauserstatus` |

### Media / Webhooks / Helpers

| Variable `.env` | Cloud Function | Slug Cloud Run |
|----------------|----------------|----------------|
| `NEXT_PUBLIC_BACKEND_URI_UPLOAD_MEDIA` | `uploadMedia` | `apiv100-firebaseentryhttp-uploadmedia` |
| `NEXT_PUBLIC_BACKEND_URI_DELETE_MEDIA` | `deleteMedia` | `apiv100-firebaseentryhttp-deletemedia` |
| `NEXT_PUBLIC_BACKEND_URI_CREATE_WEBHOOK` | `createWebhookEndpoint` | `apiv100-firebaseentryhttp-createwebhookendpoint` |
| `NEXT_PUBLIC_BACKEND_URI_DELETE_WEBHOOK` | `deleteWebhookEndpoint` | `apiv100-firebaseentryhttp-deletewebhookendpoint` |
| `NEXT_PUBLIC_BACKEND_HELPER_MAPBOX` | `geo` *(alias)* | `apiv100-firebaseentryhttp-geo` |
| `NEXT_PUBLIC_BACKEND_ENDPOINT_CONTACT` | `sendEmail` | `apiv100-firebaseentryhttp-sendemail` |

> **Nota:** `NEXT_PUBLIC_BACKEND_HELPER_MAPBOX` apunta a la función `geo` en ambos entornos. La función `mapboxGeocode` ya no existe — fue reemplazada por `geo`.

### Sin desplegar en dev

| Variable `.env` | Cloud Function | Razón |
|----------------|----------------|-------|
| `NEXT_PUBLIC_BACKEND_URI_CREATE_PLAN` | `helperCreateServicePlan` | Comentada en `functions/src/firebase-entry-http/index.ts` |
| `NEXT_PUBLIC_BACKEND_URI_PASSINBIZ_UPDATE_STAFF` | `passinbiz.updateStaff` | No exportada en `firebase-passinbiz-http/index.ts` |

---

## Funciones desplegadas en dev — Listado completo

Todas son **v2 / us-central1 / nodejs22**. Actualizado 2026-05-22.

### HTTP (`https` trigger)

```
apiV100-firebaseEntryHttp-checkinbiz-addDeviceEmployee
apiV100-firebaseEntryHttp-checkinbiz-analyzeHeuristic
apiV100-firebaseEntryHttp-checkinbiz-calendarHandler
apiV100-firebaseEntryHttp-checkinbiz-checkbizNotifications
apiV100-firebaseEntryHttp-checkinbiz-checkbizStatsController
apiV100-firebaseEntryHttp-checkinbiz-createBranch
apiV100-firebaseEntryHttp-checkinbiz-createChecklog
apiV100-firebaseEntryHttp-checkinbiz-createEmployee
apiV100-firebaseEntryHttp-checkinbiz-deleteBranch
apiV100-firebaseEntryHttp-checkinbiz-deleteEmployee
apiV100-firebaseEntryHttp-checkinbiz-documentsHandler
apiV100-firebaseEntryHttp-checkinbiz-employeesExportHandler
apiV100-firebaseEntryHttp-checkinbiz-generateReport
apiV100-firebaseEntryHttp-checkinbiz-requestManualChecklog
apiV100-firebaseEntryHttp-checkinbiz-responsibilitiesHandler
apiV100-firebaseEntryHttp-checkinbiz-tasksHandler
apiV100-firebaseEntryHttp-checkinbiz-updateBranch
apiV100-firebaseEntryHttp-checkinbiz-updateChecklog
apiV100-firebaseEntryHttp-checkinbiz-updateEmployee
apiV100-firebaseEntryHttp-checkinbiz-validateEmployee
apiV100-firebaseEntryHttp-createEvent
apiV100-firebaseEntryHttp-createWebhookEndpoint
apiV100-firebaseEntryHttp-criticalHandler
apiV100-firebaseEntryHttp-deleteEvent
apiV100-firebaseEntryHttp-deleteMedia
apiV100-firebaseEntryHttp-deleteWebhookEndpoint
apiV100-firebaseEntryHttp-enable2FA
apiV100-firebaseEntryHttp-enable2FAUser
apiV100-firebaseEntryHttp-entity-createEntity
apiV100-firebaseEntryHttp-entity-deleteEntity
apiV100-firebaseEntryHttp-entity-updateEntity
apiV100-firebaseEntryHttp-entity-updateEntityBranding
apiV100-firebaseEntryHttp-geo
apiV100-firebaseEntryHttp-get2FAUserStatus
apiV100-firebaseEntryHttp-loginEmployee
apiV100-firebaseEntryHttp-merlinIa
apiV100-firebaseEntryHttp-passinbiz-createHolder
apiV100-firebaseEntryHttp-passinbiz-createStaff
apiV100-firebaseEntryHttp-passinbiz-deleteStaff
apiV100-firebaseEntryHttp-passinbiz-deliverApplePass
apiV100-firebaseEntryHttp-passinbiz-importHoldersFromCsv
apiV100-firebaseEntryHttp-passinbiz-statsGetdata
apiV100-firebaseEntryHttp-passinbiz-updateHolder
apiV100-firebaseEntryHttp-passinbiz-validateHolder
apiV100-firebaseEntryHttp-passinbiz-validateStaff
apiV100-firebaseEntryHttp-planifierHelper
apiV100-firebaseEntryHttp-sendEmail
apiV100-firebaseEntryHttp-stripeWebhook
apiV100-firebaseEntryHttp-subscriptions-configBilling
apiV100-firebaseEntryHttp-subscriptions-subscribe
apiV100-firebaseEntryHttp-subscriptions-unsubscribe
apiV100-firebaseEntryHttp-updateAuth
apiV100-firebaseEntryHttp-updateEvent
apiV100-firebaseEntryHttp-uploadMedia
apiV100-firebaseEntryHttp-users-assingUser
apiV100-firebaseEntryHttp-users-createUsers
apiV100-firebaseEntryHttp-users-recoveryPassUsers
apiV100-firebaseEntryHttp-verify2FA
apiV100-firebaseEntryHttp-verify2FAUser
apiV100-scheduleCheckbiz-sanitizerChecklogHelper
health
```

### Scheduled / Firestore triggers

```
apiV100-firebaseEntrySchedule-cleanupUnverifiedUsers
apiV100-firebaseEntrySchedule-processPendingEmails
apiV100-firebaseEntrySchedule-webhookWorker
apiV100-firebaseFirestoreTriggers-beforeUserCreatedTrigger
apiV100-firebaseFirestoreTriggers-onCreateSentEmail
apiV100-firebaseFirestoreTriggers-onDeleteEntity
apiV100-firebaseFirestoreTriggers-onDeleteEvent
apiV100-firebaseFirestoreTriggers-onDocumentWriteSubscriptions
apiV100-firebaseFirestoreTriggers-processInvoices
apiV100-firebaseFirestoreTriggersCheckinBiz-onActivateCheckbiz
apiV100-firebaseFirestoreTriggersCheckinBiz-onChecklogWrite
apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateBranch
apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateEmployee
apiV100-firebaseFirestoreTriggersCheckinBiz-onCreateIssues
apiV100-firebaseFirestoreTriggersCheckinBiz-onIssuesResponse
apiV100-firebaseFirestoreTriggersPassinbiz-onCreateHolders
apiV100-firebaseFirestoreTriggersPassinbiz-onCreateStaff
apiV100-firebaseFirestoreTriggersPassinbiz-onCreateTrace
apiV100-firebaseFirestoreTriggersPassinbiz-onDeleteHolder
apiV100-firebaseFirestoreTriggersPassinbiz-onDeleteStaff
apiV100-scheduleCheckbiz-dailyCollectorData
apiV100-scheduleCheckbiz-employeePlanifierWorker
apiV100-scheduleCheckbiz-planifierNotificationWorker
apiV100-scheduleCheckbiz-sanitizerChecklog
```

---

## Cómo actualizar el `.env` cuando se despliega una función nueva

1. Obtener el nombre de función tal como aparece en el Firebase CLI: `firebase functions:list --project {PROJECT_ID}`
2. Convertir a slug: bajar a minúsculas, mantener guiones, truncar a 49 chars si es necesario
3. Construir la URL: `https://{slug}-{HASH}-uc.a.run.app`
4. Añadir la variable al `.env.development` (hash `jxvyznhhja`) y al `.env.production` (hash `3bnjgtprva`)

**Truncación rápida en terminal:**
```bash
FNAME="apiv100-firebaseentryhttp-checkinbiz-mynewfunction"
echo ${FNAME:0:49}
```

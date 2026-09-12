# Mapa de la migración HTTP — panel y app contra el entorno de desarrollo

> **Verificación (2026-09-11).** Catálogo obtenido por análisis estático del código de los
> servicios, del panel y de la app, cruzado con lo desplegado de verdad en `dev-encodebiz`.
> **Salvo lo que abajo se marque como confirmado, el resto es lectura del código, no
> comprobación contra el entorno.** Los hallazgos de este catálogo que ya se han verificado
> uno a uno están en [hallazgos.md](./hallazgos.md); las sospechas sin verificar se quedan
> como tales y se comprobarán al escribir su prueba. El resultado esperado de cada caso es lo
> que hace el código HOY, no lo que debería hacer.

Análisis estático, 2026-09-11. Repos leídos: `encodebiz-api` (rama develop), `encodeBiz-SAAS/functions`,
`encodebiz-front-saas`, `checkbiz360`. Sin peticiones de red ni ejecución.

Convenciones:
- **C** = contenedor tras el nginx de desarrollo (`141.95.47.135:8080`, `nginx/nginx.staging.conf`).
- **CF** = Cloud Function del proyecto `dev-encodebiz` (nombre desplegado `apiV100-firebaseEntryHttp-<grupo>-<nombre>`,
  compuesto en `functions/src/index.ts:20-31` y `functions/src/firebase-entry-http/index.ts:37-86`).
- Rutas de ficheros del panel relativas a `encodebiz-front-saas/`, de la app a `checkbiz360/lib/`, del contenedor a
  `encodebiz-api/services/`, de las functions a `encodeBiz-SAAS/functions/src/`.

**Aviso sobre las variables del panel.** La sección 1 sale de `.env.development`. El panel desplegado lee sus
variables de **Vercel**, que pueden no coincidir con este fichero. Antes de dar por buena una fila contra el panel
desplegado hay que contrastarla con Vercel (dev).

**Aviso sobre la app.** Los endpoints de la app son getters que dependen de `AppConfig.isDevelopment`, y el entorno por
defecto es `production` (`core/config/app_config.dart:7-10`, `core/constants/app_constants.dart:36-38`). Una build
de pruebas sin `--dart-define=ENVIRONMENT=development` llama a `https://api.checkbiz360.com`, que es producción.

## Cómo llama el panel a un backend

Todo pasa por un único proxy de Next: `src/app/api/proxy/[handler]/route.ts` y `[...handler]/route.ts` →
`src/lib/http/serverBackendProxy.ts:518-654`. El navegador pide `/api/proxy/<handler>[/subruta]`, y el proxy:
1. Busca `<handler>` en la allowlist `BACKEND_PROXY_TARGETS` (`serverBackendProxy.ts:49-432`) y comprueba el método.
2. Resuelve la URL con la primera variable definida de `envKeys` (`:436-442`): primero `NEXT_BACKEND_URI_*`, luego
   `BACKEND_URI_*` y, como respaldo antiguo, `NEXT_PUBLIC_BACKEND_URI_*`.
3. Si `requiresAuth`, verifica el Bearer como **ID token de Firebase** con el Admin SDK (`:571-581`).
4. Reenvía método, cuerpo, query, `Authorization`, `locale` y cookies con `redirect: 'error'` (`:595-614`). Añade la
   barra final a las raíces `/api/v1/tasks` y `/api/v1/documents` (`:513-516`).

Antes del proxy actúa el middleware `src/proxy.ts`. Exige cookie de sesión 2FA a todo `/api/proxy/*` salvo
`recovery_pass`, `create_user`, `status2fa_user`, `enable2fa_user` y `verify2fa_user` (`src/proxy.ts:88-94, 136-190`).
Además redirige `/tools/checking` a `/tools/checking/maintenance` (bloque «/tools/checking redirect», ~l.124-133).

---

## 1. Panel → backend (una fila por variable de `.env.development`)

Métodos: los que usa el código del panel, no los que admite la allowlist. «SBP» = `src/lib/http/serverBackendProxy.ts`.

| ID | Variable | Ruta | Destino | Método(s) | Servicio · router del contenedor | Ficheros de `src` | Problema |
|---|---|---|---|---|---|---|---|
| MAP-P01 | `NEXT_BACKEND_URI_CREATE_USER` | `/api/v1/users` | C | POST | entities · `entities/src/interfaces/http/user.router.ts:19` (montado con `requireFirebaseAuth`, `app.ts:31`) | `app/api/auth/register/route.ts:38-47,142` (servidor); SBP:86-91; `services/core/account.service.ts:104` | — |
| MAP-P02 | `NEXT_BACKEND_URI_RECOVERY_PASS` | `/api/v1/users/recovery` | C | POST | entities · `user.router.ts:167` (pública, `app.ts:22`) | SBP:74-79 (Turnstile `recovery`); `services/core/account.service.ts:56` | — |
| MAP-P03 | `NEXT_BACKEND_URI_ASSING_USER` | `/api/v1/entities/collaborators` | C | POST | entities · `entities/src/interfaces/http/collaborator.router.ts:28` (`app.ts:28`) | SBP:114-118; `services/core/entity.service.ts:269` | — |
| MAP-P04 | `NEXT_BACKEND_URI_CREATE_ENTITY` | `/api/v1/entities` | C | POST | entities · `entity.router.ts:56` | SBP:94-98; `entity.service.ts:113` | — |
| MAP-P05 | `NEXT_BACKEND_URI_UPDATE_ENTITY` | `/api/v1/entities/update` | C | POST | entities · `entity.router.ts:150` | SBP:99-103; `entity.service.ts:169` | — |
| MAP-P06 | `NEXT_BACKEND_URI_DELETE_ENTITY` | — (URL de Cloud Function `…entity-deleteentity…run.app`) | **CF** `deleteEntity` (`firebase-entry-http/entity/delete-entity.ts:8`) | DELETE | **Ninguno.** `entity.router.ts:15-19` lo deja fuera a propósito: arrastra la cascada `onDeleteEntity` | SBP:109-113; `entity.service.ts:245-250` ← `app/main/[entityId]/entity/page.controller.tsx:41` | **NO MIGRADO.** Única operación de negocio del panel que sigue en Cloud Functions por el proxy |
| MAP-P07 | `NEXT_BACKEND_URI_UPDATE_BRANDNG_ENTITY` | `/api/v1/entities/branding` | C | POST | entities · `entity.router.ts:162` | SBP:104-108; `entity.service.ts:195` | — |
| MAP-P08 | `NEXT_BACKEND_URI_SUBCRIBE` | `/api/v1/billing/subscriptions` | C | POST | billing · `billing/src/interfaces/http/billing.router.ts:31` (`app.ts:31`) | SBP:132-136; `services/core/subscription.service.ts:46` | — |
| MAP-P09 | `NEXT_BACKEND_URI_CONFIGBILLING` | `/api/v1/billing/portal` | C | POST | billing · `billing.router.ts:91` | SBP:142-146; `subscription.service.ts:91` | — |
| MAP-P10 | `NEXT_BACKEND_URI_UNSUBCRIBE` | `/api/v1/billing/subscriptions/unsubscribe` | C | POST | billing · `billing.router.ts:78` | SBP:137-141; `subscription.service.ts:68` | — |
| MAP-P11 | `NEXT_BACKEND_URI_DELETE_MEDIA` | `/api/v1/media` | C | DELETE (cuerpo JSON) | entities · `media.router.ts:87` (`app.ts:35`) | SBP:166-170; `services/core/media.service.ts:103-108` | — |
| MAP-P12 | `NEXT_BACKEND_URI_UPLOAD_MEDIA` | `/api/v1/media` | C | POST (multipart) | entities · `media.router.ts:34` | SBP:161-165; `media.service.ts:10,20` | — (nginx da 12 MB: `nginx.staging.conf:197-200`) |
| MAP-P13 | `NEXT_PUBLIC_BACKEND_URI_UPLOAD_MEDIA` | `/api/v1/media` | C | — | — | Solo como tercera clave de respaldo, SBP:162 | **Redundante**: nunca se lee porque P12 tiene prioridad (SBP:436-441), y como `NEXT_PUBLIC` expone la URL en el bundle. El comentario «Direct multipart upload — not proxied» (`.env.development:51`) es falso: `media.service.ts:10` va por el proxy |
| MAP-P14 | `NEXT_BACKEND_URI_CHECKINBIZ_CREATE_EMPLOYEE` | `/api/v1/employees` | C | POST | employees · `employees/src/interfaces/http/employee.router.ts:350` (`app.ts:35`) | SBP:197-201; `services/checkinbiz/employee.service.ts:188` | Nombre engañoso: «CHECKINBIZ», pero lo atiende el servicio employees |
| MAP-P15 | `NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_EMPLOYEE` | `/api/v1/employees/update` | C | POST | employees · `employee.router.ts:353` | SBP:202-206; `employee.service.ts:214` | — |
| MAP-P16 | `NEXT_BACKEND_URI_CHECKINBIZ_DELETE_EMPLOYEE` | `/api/v1/employees` | C | DELETE (cuerpo `{employeeId, entityId}`) | employees · `employee.router.ts:356` | SBP:207-211; `employee.service.ts:272-278` | — |
| MAP-P17 | `NEXT_BACKEND_URI_CHECKINBIZ_VALIDATE_EMPLOYEE` | `/api/v1/employees/validate` | C | POST | employees · `employeePublic.router.ts:13` (pública, `app.ts:22`) | SBP:223-227; `employee.service.ts:362` ← solo `app/tools/checking/page.context.tsx:97` | **Credencial incoherente.** La ruta del contenedor es pública, pero el proxy exige un ID token de Firebase (SBP:226) y el middleware una cookie 2FA. El panel manda como Bearer el `customToken` de la URL (`page.context.tsx:83,97`). Previsiblemente 403 en el proxy (sin confirmar). **Y la pantalla es inalcanzable**: `/tools/checking` redirige a mantenimiento |
| MAP-P18 | `NEXT_BACKEND_URI_CHECKINBIZ_ENABLE2AF_EMPLOYEE` | `/api/v1/checkinbiz/auth/2fa/enable` | C | POST | checkinbiz · `checkinbiz/src/interfaces/http/auth/auth.router.ts:59` (`withEmployeeSession`: valida un JWT propio con `JWT_2FA_SECRET`, `packages/shared/src/checkbiz/auth/validateTokenStaff.ts:29-41`) | SBP:228-232; `employee.service.ts:386` ← `app/tools/checking/ConfigTwoFA/ConfigTwoFA.tsx:56` | **Credencial incompatible.** El proxy verifica el Bearer como ID token de Firebase (SBP:577) y el contenedor como JWT de sesión de empleado (el `sessionToken` de `/validate`, `page.context.tsx:111`). No se pueden cumplir las dos cosas → 403. Solo desde `/tools/checking`, en mantenimiento |
| MAP-P19 | `NEXT_BACKEND_URI_CHECKINBIZ_VERIFY2AF_EMPLOYEE` | `/api/v1/checkinbiz/auth/2fa/verify` | C | POST | checkinbiz · `auth.router.ts:62` | SBP:233-237; `employee.service.ts:410` ← `ConfigTwoFA.tsx:70`, `VerifyTwoFA/VerifyTwoFA.tsx:43` | Igual que P18 |
| MAP-P20 | `NEXT_BACKEND_URI_CHECKINBIZ_RESPONSABILITY_HANDLER` | `/api/v1/employees/responsibilities` | C | POST, PATCH, DELETE (verbo dinámico, `employee.service.ts:234-247`) | employees · `responsibility.router.ts:51,122,189` | SBP:212-217; `employee.service.ts:240` | — (el GET `:229` no lo usa el panel: lee Firestore) |
| MAP-P21 | `NEXT_BACKEND_URI_CHECKINBIZ_CREATE_SUCURSAL` | `/api/v1/branches` | C | POST | branches · `branches/src/interfaces/http/branch.router.ts:174` | SBP:180-184; `services/checkinbiz/sucursal.service.ts:48` | — |
| MAP-P22 | `NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_SUCURSAL` | `/api/v1/branches/update` | C | POST | branches · `branch.router.ts:177` | SBP:185-189; `sucursal.service.ts:74` | — |
| MAP-P23 | `NEXT_BACKEND_URI_CHECKINBIZ_DELETE_SUCURSAL` | `/api/v1/branches` | C | DELETE | branches · `branch.router.ts:182` | SBP:190-194; `sucursal.service.ts:107` | — |
| MAP-P24 | `NEXT_BACKEND_URI_CHECKINBIZ_CREATE_LOG` | `/api/v1/checkinbiz/checklogs` | C | POST | checkinbiz · `http/checklog/checklog.router.ts:22` (`app.ts:34`) | SBP:218-222; `employee.service.ts:299` ← `attendance/AttendanceFormModal/AttendanceFormModal.controller.tsx:75`, `tools/checking/page.context.tsx:188` (mantenimiento) | — |
| MAP-P25 | `NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_LOG` | `/api/v1/checkinbiz/checklogs/update` | C | POST | checkinbiz · `checklog.router.ts:50` | SBP:266-270; `services/checkinbiz/report.service.ts:232` ← `AttendanceFormModal.controller.tsx:88` | — |
| MAP-P26 | `NEXT_BACKEND_URI_CHECKINBIZ_REQUEST_MANUAL_CHECKLOG` | `/api/v1/checkinbiz/checklogs/manual-request` | C | POST | checkinbiz · `checklog.router.ts:65` | SBP:425-429; `manualChecklog.service.ts:31` ← `ManualChecklogRequestModal.controller.tsx:218` | — |
| MAP-P27 | `NEXT_BACKEND_URI_CHECKINBIZ_STATS` | `/api/analytics/heuristic` | C | POST | analytics · `analytics/src/interfaces/heuristic.router.ts:32` (`app.ts:23`) | SBP:240-244; `services/checkinbiz/stats.service.ts:108` | Nombre engañoso: lo atiende analytics |
| MAP-P28 | `NEXT_BACKEND_URI_CHECKINBIZ_STATS_PANEL` | `/api/analytics/panel/stats` | C | POST | analytics · `panel.router.ts:29` (`app.ts:18`) | SBP:245-249; `app/main/[entityId]/checkinbiz/panel/components/hooks/useCheckbizStats.ts:6,179` | — |
| MAP-P29 | `NEXT_BACKEND_URI_CHECKBIZ360_MERLIN` | `/api/v1/gpt/interpret` | C | POST | merlin · `merlin/src/interfaces/merlin.router.ts:45` (`app.ts:21`) | SBP:278-282; `services/merlin.service.ts:15,44` | — |
| MAP-P30 | `NEXT_BACKEND_URI_CHECKBIZ360_MERLIN_PANEL` | `/api/v1/gpt/panel` | C | POST | merlin · `merlin.router.ts:14` | SBP:286-290; `merlin.service.ts:18,70` | — |
| MAP-P31 | `NEXT_BACKEND_URI_CHECKBIZ360_REPORTS` | `/api/reports/generate` | C | POST | reports · `reports/src/interfaces/report.router.ts:24` | SBP:291-295; `report.service.ts:30,106` | — |
| MAP-P32 | `NEXT_BACKEND_URI_CHECKBIZ360_REPORTS_TASKS` | `/api/reports/tasks` | C | POST | reports · `report.router.ts:50` | SBP:298-302; `report.service.ts:33,153` | — |
| MAP-P33 | `NEXT_BACKEND_URI_CHECKINBIZ_CALENDAR_HANDLER` | `/api/v1/checkinbiz/calendar` | C | GET, POST (`?action=savePreset`), PATCH, DELETE | checkinbiz · `http/calendar/calendar.router.ts:37,58,59,61` (`app.ts:46`) | SBP:418-422; `services/checkinbiz/calendar.service.ts:11-12,30,48,89,100,125` | Sin `subPathPattern` (ver nota A). Borrar un preset no pasa por aquí: va directo a Firestore (MAP-W13) |
| MAP-P34 | `NEXT_BACKEND_URI_CHECKINBIZ_CALENDAR_AVAILABILITY` | `/api/v1/checkinbiz/calendar/availability` (+ `/day`) | C | GET | checkinbiz · `calendar.router.ts:29,33` | SBP:406-415; `services/checkinbiz/availability.service.ts:13-14,76,98` | — |
| MAP-P35 | `NEXT_BACKEND_URI_CHECKINBIZ_TASKS_HANDLER` | `/api/v1/tasks` (+ subrutas) | C | POST, PATCH, DELETE (ningún GET) | tasks · `tasks/src/interfaces/http/task/taskRouter.ts:23,26,27,30-38` | SBP:396-400; `services/checkinbiz/task.service.ts:22,156-370` | El panel **no lee tareas por HTTP**: las lee de Firestore (`task.service.ts:60-139`). Tampoco usa `/pause`, `/resume` ni `GET /:taskId/activity` |
| MAP-P36 | `NEXT_BACKEND_URI_ADDONS_HANDLER` | `/api/v1` (+ `/rentmanbiz/…`) | C | GET, POST | rentman · `rentman/src/interfaces/http/rentman.router.ts:43-456` (detalle en la tabla 1b) | SBP:316-343; `services/integrations/addons.connection.service.ts:27,129,178-252`; `addons.operations.service.ts:49-202` | La allowlist admite `mappings` y `mappings/:id` (SBP:339), que **no existen** en el contenedor (serían 404), y `crew/:id`. Ninguna de las tres tiene llamante |
| MAP-P37 | `NEXT_BACKEND_URI_EVENTS_HANDLER` | `/api/v1/events` (+ subrutas) | C | GET, POST, PATCH, DELETE | events · `events/src/interfaces/http/events.router.ts:37,57,115,138,148,161,196,211` | SBP:390-394; `services/core/events.service.ts:25,51,…` | El **listado** de endpoints no usa `GET /endpoints` (`events.router.ts:94`): el panel lo lee de Firestore (`services/core/integration.service.ts:18-21` ← `integration/tabs/tabWebHook/page.controller.tsx:200`) |
| MAP-P38 | `NEXT_BACKEND_URI_CHECKINBIZ_DOCUMENTS_HANDLER` | `/api/v1` (+ `/documents…`) | C | GET, POST (multipart), PATCH, DELETE | documents · `documents/src/interfaces/http/document/documentRouter.ts:22-29` | SBP:349-353; `services/checkinbiz/document.service.ts:18,25,71,88,103,134,170,206,225` | Raíz `/api/v1` **sin `subPathPattern`** (nota A) |
| MAP-P39 | `NEXT_BACKEND_URI_CHECKINBIZ_DOWNLOAD_DOCUMENTS` | `/api/v1` (+ `/documents/:id/download`) | C | GET | documents · `documentRouter.ts:27` | SBP:359-363; `document.service.ts:22,26,151` | Comentarios obsoletos: SBP:355-358 y `document.service.ts:19-21` hablan de la «OLD documents-handler Cloud Function», pero en dev apunta al contenedor. Sin `subPathPattern` |
| MAP-P40 | `NEXT_BACKEND_URI_CHECKINBIZ_DOWNLOAD_REPORTS` | `/api` (+ `/reports/:id/download`) | C | GET | reports · `report.router.ts:102` | SBP:371-383; `report.service.ts:25,217` | Comentario obsoleto en `.env.development:119` («does not expose /reports/:id/download yet (404)»): el contenedor sí la tiene. Base `/api` sin `subPathPattern` |
| MAP-P41 | `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_NOTIFICATIONS` | `/api/v1/employees/notifications` | C | — | employees · `notification.router.ts:28` (POST) | Ninguno (solo `.env.example:183`) | **Declarada y sin uso.** Ningún llamante en el panel envía avisos a la plantilla |
| MAP-P42 | `NEXT_BACKEND_URI_CHECKINBIZ_GEO` | `/api/v1/checkinbiz/geo` | C | POST | checkinbiz · `http/geo/geo.router.ts:23` (`requireFirebaseAuth`, `app.ts:48`) | SBP:173-177; `services/core/helper.service.ts:69` ← `components/common/forms/fields/AddressComplexInput.tsx:80,131`, `tasks/components/TaskWorkSiteField.tsx:82,110` | El proxy marca `requiresAuth:false` (SBP:176) y el contenedor exige token. Funciona porque el panel manda el Bearer igualmente |
| MAP-P43 | `NEXT_BACKEND_URI_ENABLE2FA_USER` | `/api/v1/checkinbiz/auth/2fa/user/enable` | C | POST | checkinbiz · `auth.router.ts:86` (`requireFirebaseAuth`, `app.ts:45`) | SBP:57-61; `account.service.ts:185` | — |
| MAP-P44 | `NEXT_BACKEND_URI_VERIFY2FA_USER` | `/api/v1/checkinbiz/auth/2fa/user/verify` | C | POST | checkinbiz · `auth.router.ts:89` | SBP:62-66; `account.service.ts:199` | — |
| MAP-P45 | `NEXT_BACKEND_URI_STATUS2FA_USER` | `/api/v1/checkinbiz/auth/2fa/user/status` | C | GET | checkinbiz · `auth.router.ts:83` | SBP:52-56; `account.service.ts:171` | — |
| MAP-P46 | `NEXT_BACKEND_URI_CHECKINBIZ_PANEL_OVERVIEW` | `/api/analytics/panel/overview` | C | GET | analytics · `panel.router.ts:92` | SBP:254-258; `panel/components/hooks/usePanelOverview.ts:12,499` | — |
| MAP-P47 | `NEXT_BACKEND_URI_CHECKINBIZ_COLLABORATORS_HANDLER` | `/api/v1/checkinbiz/collaborators/:userId` | C | DELETE | checkinbiz · `http/collaborator/collaborator.router.ts:191` (`app.ts:40`) | SBP:124-129; `entity.service.ts:334-339` | — |
| MAP-P48 | `NEXT_PUBLIC_BACKEND_HELPER_MAPBOX` (otro prefijo) | — (URL de Cloud Function `…firebaseentryhttp-geo…`) | CF `geo` (`firebase-entry-http/helpers/geo.ts:8`) | — | Equivalente: `/api/v1/checkinbiz/geo` (P42) | Ninguno (solo `.env.example:203`) | **Declarada y sin uso**, y apunta a Cloud Function |
| MAP-P49 | `NEXT_PUBLIC_BACKEND_ENDPOINT_CONTACT` (otro prefijo) | — (URL de Cloud Function `…firebaseentryhttp-sendemail…`) | **CF** `sendEmail` (`firebase-entry-http/mailer/send-email.ts:49`) | POST **directo desde el navegador, sin proxy** | **Ninguno** | `services/core/helper.service.ts:115-135` (`sendFormContact`) ← `components/common/modals/ContactModal/ContactModal.controller.tsx:40` | **NO MIGRADO y fuera del proxy**: el navegador llama a la Cloud Function con el ID token del usuario |

**Nota A — handlers de raíz sin `subPathPattern`.** `checkinbiz_documents_handler` y `checkinbiz_download_documents`
(base `/api/v1`), `checkinbiz_download_reports` (base `/api`), `events_handler`, `checkinbiz_tasks_handler` y
`checkinbiz_calendar_handler` reenvían cualquier subruta. Con la base `/api/v1` y cuatro métodos, el navegador puede
alcanzar **cualquier** ruta `/api/v1/*` del contenedor a través de un proxy que ya pone el token. Es justo lo que el
comentario de SBP:11-16 dice querer evitar. No provoca 404, pero es una incoherencia de la allowlist.

**Handlers de la allowlist sin variable en `.env.development` y sin llamantes** (código muerto): `create_webhook`
(SBP:149-153), `delete_webhook` (SBP:154-158) y `checkinbiz_generate_report` (SBP:261-265).

### 1b. Detalle de las subrutas por proxy (lo que realmente pide el panel)

| ID | Handler | Método y ruta final en el contenedor | Router | Llamante del panel |
|---|---|---|---|---|
| MAP-P35a | tasks | `POST /api/v1/tasks/` | `taskRouter.ts:23` | `task.service.ts:156` |
| MAP-P35b | tasks | `PATCH /api/v1/tasks/:taskId` | `:26` | `task.service.ts:166` |
| MAP-P35c | tasks | `POST /:taskId/duplicate` | `:27` | `:189` |
| MAP-P35d | tasks | `POST /:taskId/assignments` | `:30` | `:204` |
| MAP-P35e | tasks | `DELETE /:taskId/assignments/:employeeId` | `:31` | `:221` |
| MAP-P35f | tasks | `PATCH /:taskId/status` | `:32` | `:246` |
| MAP-P35g | tasks | `POST /:taskId/notes` | `:33` | `:261` |
| MAP-P35h | tasks | `PATCH /:taskId/notes/:noteId` | `:34` | `:277` |
| MAP-P35i | tasks | `POST /:taskId/validation` | `:35` | `:292` |
| MAP-P35j | tasks | `POST /:taskId/rejection` | `:36` | `:307` |
| MAP-P35k | tasks | `POST /:taskId/ratings` (JSON o multipart) | `:38` | `:330,355` |
| MAP-P35l | tasks | `POST /:taskId/resources` (multipart) | `:37` | `:370` |
| MAP-P38a | documents | `GET /api/v1/documents/` | `documentRouter.ts:22` | `document.service.ts:71` |
| MAP-P38b | documents | `GET /api/v1/documents/:id` | `:24` | `:88` |
| MAP-P38c | documents | `POST /api/v1/documents/` (multipart) | `:23` | `:103` |
| MAP-P38d | documents | `PATCH /api/v1/documents/:id` | `:25` | `:134` |
| MAP-P38e | documents | `GET /api/v1/documents/:id/acks` | `:29` | `:170` |
| MAP-P38f | documents | `POST /api/v1/documents/:id/ack` | `:28` | `:206` |
| MAP-P38g | documents | `DELETE /api/v1/documents/:id` | `:26` | `:225` |
| MAP-P37a | events | `GET /catalogue` | `events.router.ts:37` | `events.service.ts` (`fetchEventCatalogue`) |
| MAP-P37b | events | `POST /endpoints` | `:57` | `createEndpoint` |
| MAP-P37c | events | `PATCH /endpoints/:id` | `:115` | `updateEndpoint` (l.103) |
| MAP-P37d | events | `DELETE /endpoints/:id` | `:138` | `deleteEndpoint` (l.112) |
| MAP-P37e | events | `POST /endpoints/:id/test` | `:161` | `testEndpoint` (l.125) |
| MAP-P37f | events | `POST /endpoints/:id/rotate-secret` | `:148` | `rotateEndpointSecret` (l.135) |
| MAP-P37g | events | `GET /deliveries` | `:196` | `fetchDeliveries` (l.152) |
| MAP-P37h | events | `POST /deliveries/:id/replay` | `:211` | `replayDelivery` (l.158) |
| MAP-P36a | addons | `GET /rentmanbiz/connection/:entityId` | `rentman.router.ts:118` | `addons.connection.service.ts:179` |
| MAP-P36b | addons | `POST /rentmanbiz/activate` | `:43` | `:200` |
| MAP-P36c | addons | `POST /rentmanbiz/connect` | `:72` | `:222` |
| MAP-P36d | addons | `POST /rentmanbiz/disconnect` | `:92` | `:236` |
| MAP-P36e | addons | `POST /rentmanbiz/active` | `:108` | `:251` |
| MAP-P36f | addons | `GET /rentmanbiz/test-connection/:entityId` | `:125` | `addons.operations.service.ts:50` |
| MAP-P36g | addons | `GET /rentmanbiz/catalogue/summary/:entityId` | `:181` | `:64` |
| MAP-P36h | addons | `GET /rentmanbiz/catalogue/preview/:entityId` | `:168` | `:74` |
| MAP-P36i | addons | `POST /rentmanbiz/catalogue/import` | `:236` | `:87` |
| MAP-P36j | addons | `POST /rentmanbiz/settings/crew-folders` | `:205` | `:109` |
| MAP-P36k | addons | `GET /rentmanbiz/pending/:entityId` | `:282` | `:120` |
| MAP-P36l | addons | `POST /rentmanbiz/pending/crew/complete` | `:268` | `:133` |
| MAP-P36m | addons | `GET /rentmanbiz/hours/summary/:entityId` | `:322` | `:145` |
| MAP-P36n | addons | `GET /rentmanbiz/hours/entries/:entityId` | `:373` | `:167` |
| MAP-P36o | addons | `POST /rentmanbiz/hours/sync-now` | `:420` | `:180` |
| MAP-P36p | addons | `GET /rentmanbiz/hours/divergences/:entityId` | `:456` | `:190` |
| MAP-P36q | addons | `GET /rentmanbiz/activity/:entityId` | `:294` | `:202` |

Método y ruta coinciden en todas las filas: no hay ningún 404 ni 405 previsible en rutas vivas.

### 1c. Llamadas del panel a un backend que no salen de esas variables

| ID | Llamada | Fichero | Destino | Nota |
|---|---|---|---|---|
| MAP-P50 | `POST /api/auth/register` (ruta de Next) | `app/api/auth/register/route.ts:56-171` ← `services/core/account.service.ts:86` | Admin SDK `createUser` (`:95`), `createCustomToken` (`:124,164`), REST de Identity Toolkit `accounts:signInWithCustomToken` (`:126-134`) y después `POST NEXT_BACKEND_URI_CREATE_USER` (`:142`) | Alta hecha en el servidor. Si falla, hace rollback con `deleteUser` (`:111`) |
| MAP-P51 | `POST/DELETE /api/auth/2fa-session`, `POST /api/auth/2fa-session/refresh` | `app/api/auth/2fa-session/route.ts`, `…/refresh/route.ts` ← `auth/2fa/page.controller.tsx:93`, `auth/2fa/setup/page.controller.tsx:98`, `main/user/account/page.controller.tsx:200`, `components/common/modals/TwoFAGateModal.tsx:144`, `lib/firebase/authentication/logout.ts:10`, `lib/http/sessionRefresh.ts:25` | Local (cookie firmada en Next y verificación del ID token con el Admin SDK) | No hay backend detrás |
| MAP-P52 | `POST /api/auth/verify-token` | `app/api/auth/verify-token/route.ts` | Local (Admin SDK) | Sin backend detrás; llamantes sin comprobar |
| MAP-P53 | Cloudflare Turnstile `siteverify` | `lib/turnstile/verifyTurnstileToken.ts:119` | Tercero | No es nuestro backend |

No hay URLs de Cloud Functions ni del contenedor escritas a mano en `src` (búsqueda de `run.app`, `cloudfunctions`,
`141.95`, `:8080` y `checkbiz360.com`: solo aparecen enlaces de marketing y assets).

---

## 2. Panel → Firestore y Storage directos (lo que queda fuera de la migración HTTP)

Las escrituras pasan por helpers genéricos (`lib/firebase/firestore/updateDocument.ts:13`,
`addDocument.ts:16,20` —`addDoc` seguido de un `setDoc {id}` con merge, o sea, dos escrituras—,
`deleteDocument.ts:12`) o por llamadas directas. La tabla da el sitio que decide la colección.

| ID | Colección o ruta | Operación | Fichero:línea | Llamantes | ¿Sensible? |
|---|---|---|---|---|---|
| MAP-W01 | `user_entity_roles/{id}` | `updateDoc` `{status:'active'}` | `services/core/entity.service.ts:69` (`updateAuth`) | `app/layouts/AdminLayout.tsx:75`, `components/common/modals/WelcomeInvite.tsx:48` | **Sí — colaboradores/roles.** El contenedor ya tiene `PATCH /api/v1/checkinbiz/collaborators/:userId`, que «sustituye a `updateAuth`» (`checkinbiz/…/collaborator.router.ts:158-162`) y nadie llama |
| MAP-W02 | `user_entity_roles/{id}` (una por entidad) | `updateDoc` `{isActive}` | `entity.service.ts:89` (`saveStateCurrentEntity`) | `contexts/entityContext.tsx:166` | **Sí — colaboradores.** Además es un `forEach(async…)` sin `await` (`entity.service.ts:88`) |
| MAP-W03 | `entities/{id}` | `updateDoc` `{language}` | `entity.service.ts:137` (`updateExtraEntity`) | `components/common/LocaleSwitcher.tsx:102` | **Sí — empresas** |
| MAP-W04 | `entities/{id}` | `updateDoc` `{config}` | `entity.service.ts:152` (`updateEntityConfig`) | `app/main/[entityId]/entity/tabs/tabBranding/page.controller.tsx:113` | **Sí — empresas** (existen `POST /entities/update` y `/branding`) |
| MAP-W05 | `users/{uid}` | `updateDoc` `{photoURL, phoneNumber, fullName}` | `services/core/account.service.ts:215` (`updateAccout`) | `app/main/user/account/page.controller.tsx:137` | Moderado (perfil propio). Sin ruta en el contenedor |
| MAP-W06 | `entities/{e}/jobs/{id}` | `updateDoc` `{job, price}` | `services/checkinbiz/employee.service.ts:136` (`addJobs`) | `branch/[id]/detail/components/FormLink.controller.tsx:84`, `employee/[id]/detail/Branch/SucursalFromItem/SucursalFromItem.controller.tsx:82`, `employee/[id]/detail/FormLink/FormLink.controller.tsx:107` | **Sí — empresa** (tarifa por puesto). Sin ruta |
| MAP-W07 | `entities/{e}/jobs` | `addDoc` + `setDoc {id}` | `employee.service.ts:145` → `addDocument.ts:16,20` | ídem | **Sí — empresa**. Sin ruta |
| MAP-W08 | `entities/{e}/jobs/{id}` | `deleteDoc` | `employee.service.ts:171` (`deleteJobs`) | `branch/…/FormLink.controller.tsx:162`, `employee/…/FormLink.controller.tsx:186`, `SucursalFromItem.controller.tsx:151` | **Sí — empresa**. Sin ruta |
| MAP-W09 | `issues/{id}/responses` | `addDoc` + `setDoc {id}` | `employee.service.ts:480` (`addResponse`) | `issues/[id]/detail/components/ResponseFormModal/ResponseFormModal.controller.tsx:40` | No (incidencias). Sin ruta |
| MAP-W10 | `issues/{id}` | `updateDoc` del documento entero | `employee.service.ts:708` (`updateIssue`) | `issues/form/form.controller.tsx:80`, `ResponseFormModal.controller.tsx:52` | No (incidencias). Sin ruta |
| MAP-W11 | `issues` | `addDoc` + `setDoc {id}` | `employee.service.ts:723` (`addIssue`) | `issues/form/form.controller.tsx:82`; `tools/checking/Contact/Form/form/form.controller.tsx:64` (en mantenimiento) | No (incidencias). Sin ruta |
| MAP-W12 | `entities/{e}/reports/{id}` | `updateDoc` | `services/checkinbiz/report.service.ts:256` (`updateReport`) | `app/main/[entityId]/checkinbiz/report/page.controller.tsx:316` | **Sí — informes de jornada (fichajes)**. Sin ruta |
| MAP-W13 | `entities/{e}/calendar/{id}`, `…/branches/{b}/calendar/{id}`, `…/employees/{emp}/calendar/{id}` | `deleteDoc` directo | `services/checkinbiz/calendar.service.ts:81` (`deleteCalendarPreset`) | `calendar/components/CalendarSection.tsx:702` | **Sí — calendario laboral de empresa, sucursal y empleado.** Existe `DELETE /api/v1/checkinbiz/calendar` (`calendar.router.ts:61`), pero no se usa para esto |
| MAP-W14 | Storage (ruta variable) | `uploadBytesResumable` | `lib/firebase/storage/fileManager.ts:24` (`uploadFile`) | **Ninguno** | Código muerto: el panel no sube nada a Storage. `setDocument` (`updateDocument.ts:25`) y `createDocumentWithId` (`addDocument.ts:27-34`) tampoco tienen llamantes |

**Totales del panel:** 13 sitios de escritura vivos en Firestore (W01–W13) y 0 en Storage. De ellos, **9 sensibles**
(W01, W02, W03, W04, W06, W07, W08, W12 y W13), más W05 como perfil propio. Las incidencias (W09–W11) no entran en
las categorías sensibles, pero tampoco tienen ruta en el contenedor.

### 2b. Lecturas directas del panel a colecciones sensibles (resumen)

| Colección | Sitios de lectura |
|---|---|
| `user_entity_roles` | `entity.service.ts:30` (entidades del usuario), `:295` (`fetchAllOwnerOfEntity`) |
| `entities` | `entity.service.ts:20` (`getOne`), `:346` (`onSnapshot`) |
| `users` | `services/core/users.service.ts:12` (**`getAll` de la colección entera**; llamantes sin comprobar), `:25`; `account.service.ts:136` |
| `entities/{e}/employees` (+ `/security`) | `employee.service.ts:27`, `:37` (subcolección `security`), `:55`, `:504`, `:602`, `:771` (`watchEmployeesChange`) |
| `entities/{e}/checklogs` (fichajes) | `employee.service.ts:335`, `:351`, `:435`, `:543`, `:778`; `report.service.ts:58` |
| `entities/{e}/employee_responsibilities` | `employee.service.ts:95`, `:113`; `branch/page.controller.tsx:222`; `employee/[id]/detail/components/EmployeeDocumentsSection.tsx:78` |
| `entities/{e}/branches` | `sucursal.service.ts:19`, `:36`, `:138`; `EmployeeDocumentsSection.tsx:93`; `calendar/components/EmployeeHolidaysTab.tsx:133` |
| `entities/{e}/reports` | `report.service.ts:50`, `:77`, `:86` |
| Suscripciones y facturación | `subscription.service.ts:25` (`service`), `:111` y `:131` (`entities/{e}/subscriptions`), `:122` (`entities/{e}/invoices`) |
| `entities/{e}/tasks` + subcolecciones | `task.service.ts:63-131` (tarea, assignments, notes, resources, ratings, validations, activity) |
| `entities/{e}/webhook_endpoints` | `services/core/integration.service.ts:21` |
| Calendarios | `calendar.service.ts:67`, `:145`; `getRefByPathData` en `branch/form/form.controller.tsx:398-399,468`, `EntityCalendarTab.tsx:88`, `EmployeeHolidaysTab.tsx:124,134`, `employee/form/form.controller.tsx:294-295,546`, `EmployeeCalendarDetail.tsx:164-166`, `BranchCalendarDetail.tsx:118,125` |
| Otras | `searchIndex` (`helper.service.ts:108`), `issues` (`employee.service.ts:450-470,750,761`), `jobs` (`:71`), `media` (`media.service.ts:62`), patrones y heurística (`stats.service.ts:34,69,86`), caché de Merlin (`merlin.service.ts:97,111`) |

Casi toda la lectura del panel va directa a Firestore. Por HTTP solo lee calendario, disponibilidad, documentos,
eventos, add-ons, estadísticas y el estado de 2FA.

---

## 3. Panel → Firebase Auth

| ID | Operación | Fichero:línea | Nota |
|---|---|---|---|
| MAP-A01 | Inicio de sesión con email y contraseña | `lib/firebase/authentication/login.ts:18` (`signInWithEmailAndPassword`) | — |
| MAP-A02 | Inicio con Google | `login.ts:32` (`signInWithPopup`) ← `services/core/account.service.ts:31` | — |
| MAP-A03 | Token personalizado | `login.ts:38` (`signInWithCustomToken`) ← `account.service.ts:21`, tras el alta de MAP-P50 | En el servidor: `createUser` y `createCustomToken` (`app/api/auth/register/route.ts:95,124,164`), `deleteUser` como rollback (`:111`) y REST `accounts:signInWithCustomToken` (`:126-134`) |
| MAP-A04 | Cierre de sesión | `lib/firebase/authentication/logout.ts:11` (`signOut`), precedido de `DELETE /api/auth/2fa-session` (`:10`) | — |
| MAP-A05 | Escucha de sesión | `lib/firebase/authentication/stateChange.ts:8` (`onIdTokenChanged`) | — |
| MAP-A06 | ID tokens | `getIdToken()` / `getIdToken(true)` en `contexts/authContext.tsx:77,191`, `app/auth/login/page.controller.tsx:57,84`, `app/auth/2fa/page.controller.tsx:57,84,89`, `app/auth/2fa/setup/page.controller.tsx:59,89,94`, `app/main/user/account/page.controller.tsx:163,179,195,199`, `TwoFAGateModal.tsx:105,137,141`, `merlin.service.ts:33`, `report.service.ts:103,150`, `useCheckbizStats.ts:178`, `usePanelOverview.ts:497` | — |
| MAP-A07 | Actualizar perfil de Auth | `services/core/account.service.ts:210` (`updateProfile`) | Va unido a la escritura MAP-W05 |
| MAP-A08 | Cambio de contraseña | `login.ts:57` (`updatePassword`, `changePass`) | **Sin llamantes.** Según el comentario de SBP:73, la pestaña de contraseña usa `recovery_pass` (sin confirmar) |
| MAP-A09 | Borrado de la cuenta | `login.ts:61` (`deleteUser`, `deleteAccount`) | **Sin llamantes** |
| MAP-A10 | Recuperación de contraseña | No usa Firebase Auth: proxy `recovery_pass` → `POST /api/v1/users/recovery` (`account.service.ts:56`) | — |
| MAP-A11 | 2FA | No usa el `multiFactor` de Firebase. TOTP propio en el contenedor (P43–P45) y cookie firmada en Next (MAP-P51) | — |
| MAP-A12 | Verificación de email y reautenticación | Ninguna llamada (`sendEmailVerification`, `applyActionCode` y `reauthenticateWithCredential` no aparecen en `src`) | — |

---

## 4. App → backend

Todas las llamadas usan un único `Dio` (`core/network/dio_client.dart:15-17`) cuya `baseUrl` es
`AppConfig.apiBaseUrl`, es decir, Cloud Functions (`app_config.dart:12-16`). Como todos los endpoints vivos son URLs
absolutas, esa `baseUrl` no se usa. Base privada en desarrollo: `http://141.95.47.135:8080` (`app_constants.dart:34`).
No hay otros clientes HTTP en `lib/` (ni `package:http` ni `HttpClient`).

«Rollback posible» = existe una Cloud Function equivalente **desplegada en dev-encodebiz**, según
`dev-funciones-desplegadas.csv`.

| ID | Constante (`app_constants.dart`) | Ruta | Destino | Método y llamada | Servicio · router | Rollback posible | Problema |
|---|---|---|---|---|---|---|---|
| MAP-A01 | `loginEmployeeEndpoint` (:50) | `/api/v1/checkinbiz/auth/login` | C | POST — `features/auth/data/datasources/auth_remote_datasource.dart:37` | checkinbiz · `auth.router.ts:67` (`requireFirebaseAuth`, `app.ts:45`) | **Sí**: `loginEmployee`. El rollback documentado (`criticalHandler/auth/login`, :47-49) **no está desplegado** | — |
| MAP-A02 | `validateEmployeeEndpoint` (:51) | `/api/v1/checkinbiz/auth/validate` | C | POST — `auth_remote_datasource.dart:82` | checkinbiz · `auth.router.ts:32` (pública) | **Sí**: `checkinbiz-validateEmployee` (mismo controlador; `criticalHandler`, no desplegado, la despachaba en `critical-handler.ts:46-47`) | — |
| MAP-A03 | `enable2FAEndpoint` (:61) | `/api/v1/checkinbiz/auth/2fa/enable` | C | POST — `:100` | checkinbiz · `auth.router.ts:59` | **Sí**: `enable2FA` | — |
| MAP-A04 | `verify2FAEndpoint` (:62) | `/api/v1/checkinbiz/auth/2fa/verify` | C | POST — `:127` | checkinbiz · `auth.router.ts:62` | **Sí**: `verify2FA` | — |
| MAP-A05 | `recoveryPassEndpoint` (:65-67) | URL de Cloud Function (`…users-recoverypassusers…run.app`) | **CF** `users-recoveryPassUsers` (`firebase-entry-http/users/recovery-pass-users.ts:73`), **desplegada** | POST — `:174` ← `auth_provider.dart:1609` ← `forgot_password_page.dart:38` | Equivalente: `POST /api/v1/users/recovery` (`entities/…/user.router.ts:167`), que el panel ya usa | (ya está en la función) | **NO MIGRADO en la app** |
| MAP-A06 | `addDeviceEmployeeEndpoint` (:70-72) | URL de Cloud Function (`…checkinbiz-adddeviceemp…run.app`) | **CF** `checkinbiz-addDeviceEmployee` (`…/firebase-checkinbiz-http/add-device-employee.ts:11`), **desplegada** | POST — `:154` | **Sin ruta en el contenedor.** Según `app_constants.dart:57-58`, el `verify` del contenedor ya registra el dispositivo | (ya está en la función) | **NO MIGRADO**, y redundante según el propio comentario |
| MAP-A07 | `createChecklogEndpoint` (:77) | `/api/v1/checkinbiz/checklogs` | C | POST — `features/attendance/data/datasources/attendance_remote_datasource.dart:31` | checkinbiz · `checklog.router.ts:22` | **No**: `createChecklog` no está desplegada | — |
| MAP-A08 | `updateChecklogEndpoint` (:79-80) | `/api/v1/checkinbiz/checklogs/update` | C | POST — `:51`; también `ValidateChecklogUpdate` (`domain/usecases/validate_checklog_update.dart:9`) ← `update_checklog_notification_page.dart:147,210` | checkinbiz · `checklog.router.ts:50` | **No**: `updateChecklog` no está desplegada | — |
| MAP-A09 | `attendanceCalendarEndpoint` (:82) | `/api/v1/checkinbiz/calendar` | C | GET — `:75` | checkinbiz · `calendar.router.ts:37` | **Sí**: `checkinbiz-calendarHandler` (el rollback documentado vía `criticalHandler` no está desplegado) | — |
| MAP-A10 | `taskCollectionEndpoint` (:91) | `/api/v1/tasks/` | C | GET — `features/task/data/datasources/task_remote_datasource.dart:153`; POST — `:199` | tasks · `taskRouter.ts:22,23` | **No**: `tasksHandler` no está desplegada (el rollback de :85-86 ya no existe) | — |
| MAP-A11 | `taskEndpoint` + `/:taskId` (:87) | `/api/v1/tasks/:taskId` | C | GET — `:180`; PATCH — `:219` | tasks · `taskRouter.ts:24,26` | No | — |
| MAP-A12 | ídem + `/status` | `/api/v1/tasks/:taskId/status` | C | PATCH — `:242` | `taskRouter.ts:32` | No | — |
| MAP-A13 | ídem + `/pause` | `/api/v1/tasks/:taskId/pause` | C | POST — `:268` | `taskRouter.ts:28` | No (no hay equivalente en Cloud Functions) | — |
| MAP-A14 | ídem + `/resume` | `/api/v1/tasks/:taskId/resume` | C | POST — `:292` | `taskRouter.ts:29` | No (no hay equivalente en Cloud Functions) | — |
| MAP-A15 | ídem + `/assignments` | `/api/v1/tasks/:taskId/assignments` | C | POST — `:316` | `taskRouter.ts:30` | No | — |
| MAP-A16 | ídem + `/assignments/:employeeId` | `…/assignments/:employeeId` | C | DELETE — `:334` | `taskRouter.ts:31` | No | — |
| MAP-A17 | ídem + `/notes` | `/api/v1/tasks/:taskId/notes` | C | POST — `:353` | `taskRouter.ts:33` | No | — |
| MAP-A18 | ídem + `/validation` | `/api/v1/tasks/:taskId/validation` | C | POST — `:373` | `taskRouter.ts:35` | No | — |
| MAP-A19 | ídem + `/rejection` | `/api/v1/tasks/:taskId/rejection` | C | POST — `:391` | `taskRouter.ts:36` | No | — |
| MAP-A20 | ídem + `/ratings` | `/api/v1/tasks/:taskId/ratings` | C | POST — `:438` | `taskRouter.ts:38` | No | — |
| MAP-A21 | ídem + `/resources` | `/api/v1/tasks/:taskId/resources` | C | POST (multipart) — `:487` | `taskRouter.ts:37` | No | — |
| MAP-A22 | `documentsCollectionEndpoint` (:99) | `/api/v1/documents/` | C | GET — `features/documents/data/datasources/document_remote_datasource.dart:60` | documents · `documentRouter.ts:22` | **No**: `documentsHandler` no está desplegada | — |
| MAP-A23 | `documentsEndpoint` + `/:id` (:96) | `/api/v1/documents/:id` | C | GET — `:88` | `documentRouter.ts:24` | No | — |
| MAP-A24 | `documentsDownloadEndpoint` + `/:id/download` (:108) | `/api/v1/documents/:id/download` | C | GET — `:108` | `documentRouter.ts:27` | No | — |
| MAP-A25 | `documentsEndpoint` + `/:id/ack` | `/api/v1/documents/:id/ack` | C | POST — `:127` | `documentRouter.ts:28` | No | — |
| MAP-A26 | `authEndpoint`, `attendanceEndpoint`, `employeeEndpoint`, `teamEndpoint`, `projectEndpoint` (:7-12) | Relativas a la `baseUrl` de Cloud Functions | CF | — | — | — | **Constantes muertas.** `attendanceEndpoint` solo aparece en la rama de producción de `addDeviceEmployee` (:72). Cualquier ruta relativa nueva iría a Firebase, no al contenedor |

Método y ruta coinciden en todas las filas vivas: no hay 404 ni 405 previsibles.

---

## 5. App → Firestore, Storage y Firebase Auth

### 5a. Escrituras directas

| ID | Colección o ruta | Operación | Fichero:línea | Llamantes | ¿Sensible? |
|---|---|---|---|---|---|
| MAP-AW01 | `issues/{id}` | `set` | `features/support/data/datasources/issue_firestore_datasource.dart:75` (`createIssue`) | `issue_repository_impl.dart:17` ← `issue_form_provider.dart:100` | No (incidencias) |
| MAP-AW02 | `issues/{id}/responses/{r}` + `issues/{id}` | `runTransaction`: `set` + `update {state, responseCount++}` | `issue_firestore_datasource.dart:91,100,103-106` (`replyToIssue`) | `issue_detail_provider.dart:76` | No, aunque cambia el estado de la incidencia |
| MAP-AW03 | `entities/{e}/employees/{emp}` | `update {…data, updated_at}` | `data/datasources/firestore/employee_firestore_datasource.dart:37` | `auth_provider.dart:711` (idioma tras el login), `features/attendance/presentation/widgets/attendance_drawer.dart:300` (cambio de idioma) | **Sí — empleados.** Hoy solo manda `language`, pero el método acepta cualquier `Map` |
| MAP-AW04 | `notification_tokens/{employeeId}` + `devices/{deviceId}` | `batch` con `set` y `update` (`arrayUnion`, timestamps) | `features/notifications/data/datasources/notification_token_firestore_datasource.dart:37-89` (`addDeviceToken`, :20) | Registro de FCM | No (tokens de dispositivo) |
| MAP-AW05 | `notification_tokens/{employeeId}[/devices/{deviceId}]` | `delete` y `update` | `:114,124,128` (`removeDeviceToken`, :104) | `application/services/fcm_registration_controller.dart:31` | No |
| MAP-AW06 | `notification_tokens/…/devices` (limpieza) | `batch.delete` + `update` | `:186-192` | Interno del datasource | No |
| MAP-AW07 | `in_app_notifications/{id}` | `update {isRead}` | `in_app_notification_firestore_datasource.dart:197` | `notification_detail_page.dart:32`, `update_checklog_notification_page.dart:161` | No |
| MAP-AW08 | `in_app_notifications` (del empleado) | `batch.update {isRead}` | `:206-217` (`markAllAsRead`) | `in_app_notification_repository_impl.dart:36` | No |
| MAP-AW09 | `in_app_notifications/{id}` | `delete` | `:222` | `in_app_notification_repository_impl.dart:41` | No |
| MAP-AW10 | `in_app_notifications/{id}` | `update {validationStatus}` | `:228` (`updateValidationStatus`) | `update_checklog_notification_page.dart:157` | **Sí, indirecto — fichajes.** Marca como aceptado un cambio de fichaje. El cambio real va por HTTP justo antes (`POST /checklogs/update`, `:147-152`), pero el estado de la validación lo escribe el cliente |
| MAP-AW11 | Genérico `FirebaseFirestoreService` | `set`, `update`, `delete` | `infrastructure/firebase/firestore/firebase_firestore_service.dart:58,68,73` | **Ninguno** (solo se usa `getDocumentById`: `branch_firestore_datasource.dart:52`) | Código muerto |

**Storage:** ninguna operación (`firebase_storage` no aparece en `lib/`).
**Totales de la app:** 10 sitios de escritura vivos (AW01–AW10), 2 de ellos sensibles (AW03 y AW10).

### 5b. Lecturas directas de la app a colecciones sensibles

| Colección | Sitios |
|---|---|
| `entities` | `data/datasources/firestore/entity_firestore_datasource.dart:31-34` |
| `employees` en **todas las empresas** (`collectionGroup` por `uid`) | `entity_firestore_datasource.dart:71-74` |
| `entities/{e}/employees/{emp}` | `employee_firestore_datasource.dart:13-16` (get), `:49-52` (snapshots) |
| `entities/{e}/branches` | `features/attendance/data/datasources/branch_firestore_datasource.dart:45-52`, `:119-122` |
| `entities/{e}/checklogs` (fichajes) | `checklog_firestore_datasource.dart:73,126,180,236,301-306` |
| `entities/{e}/employee_responsibilities` | `responsibility_firestore_datasource.dart:31-33`, `:55-57` |
| `entities/{e}/tasks` + subcolecciones | `features/task/data/datasources/task_firestore_datasource.dart:51-61,185-306` |
| Otras | `searchIndex` (`task_lookup_datasource.dart:35,59,70`), `in_app_notifications`, `issues`, `app_config/global` (`data/datasources/remote/app_config_firestore_datasource.dart:14`) |

### 5c. Firebase Auth en la app

| ID | Operación | Fichero:línea | Nota |
|---|---|---|---|
| MAP-AA01 | Email y contraseña | `features/auth/presentation/providers/auth_provider.dart:895`; `infrastructure/firebase/authentication/firebase_auth_service.dart:30` | — |
| MAP-AA02 | Google | `firebase_auth_service.dart:94-116` (`signInWithCredential`, :116) ← `auth_provider.dart:819` | — |
| MAP-AA03 | Apple | `firebase_auth_service.dart:127-158` (:158) ← `auth_provider.dart:847` | — |
| MAP-AA04 | Cierre de sesión | `auth_provider.dart:374,566,805,852,1210`; `firebase_auth_service.dart:77-85` (con `GoogleSignIn.signOut`, :80) | — |
| MAP-AA05 | Escucha de sesión y tokens | `authStateChanges` (`auth_provider.dart:935`, `firebase_auth_service.dart:53`); `getIdToken(true)` (`firebase_auth_service.dart:49`, `infrastructure/network/auth_retry_interceptor.dart:75`); `getIdToken()` (`:62`) | — |
| MAP-AA06 | Cambio de contraseña con reautenticación | `firebase_auth_service.dart:217-225` (`reauthenticateWithCredential` + `updatePassword`) ← `auth_provider.dart:1581` ← `presentation/pages/settings/change_password_page.dart:46` | — |
| MAP-AA07 | Recuperación de contraseña | No usa Firebase: `auth_provider.dart:1607-1610` → CF `recoveryPassUsers` (MAP-A05) | `firebase_auth_service.dart:232-234` (`sendPasswordResetEmail` de Firebase) no tiene llamantes |
| MAP-AA08 | Alta | `firebase_auth_service.dart:69` (`createUserWithEmailAndPassword`) | **Sin llamantes** |
| MAP-AA09 | 2FA, verificación de email y tokens personalizados | TOTP propio en el contenedor (A03–A04). No hay `multiFactor`, `sendEmailVerification` ni `signInWithCustomToken` | — |
| MAP-AA10 | FCM (no es Auth) | `infrastructure/firebase/messaging/firebase_messaging_service.dart:426-468` (`subscribeToTopic`) | Se anota porque también queda fuera del HTTP |

---

## 6. Cloud Functions HTTP que algún cliente sigue llamando

Estado de despliegue tomado de `dev-funciones-desplegadas.csv`, entregado por el coordinador; no lo he obtenido yo.
De sus 65 funciones sin tipo de evento, 9 son programadas (`dev-programadas.csv`) y **56 son HTTP**.

| ID | Función desplegada | Fichero en encodeBiz-SAAS | ¿Desplegada en dev? | Quién la llama | Desde dónde |
|---|---|---|---|---|---|
| MAP-F01 | `apiV100-firebaseEntryHttp-entity-deleteEntity` | `firebase-entry-http/entity/delete-entity.ts:8` | **Sí** (CSV l.63) | Panel (servidor Next, por el proxy) | `.env.development:40` → SBP:109-113 → `entity.service.ts:245` ← `entity/page.controller.tsx:41` |
| MAP-F02 | `apiV100-firebaseEntryHttp-sendEmail` | `firebase-entry-http/mailer/send-email.ts:49` | **Sí** (l.76) | Panel (**directo desde el navegador**) | `.env.development:135` → `helper.service.ts:127-128` ← `ContactModal.controller.tsx:40` |
| MAP-F03 | `apiV100-firebaseEntryHttp-users-recoveryPassUsers` | `firebase-entry-http/users/recovery-pass-users.ts:73` | **Sí** (l.48) | App | `app_constants.dart:65-67` → `auth_remote_datasource.dart:174` |
| MAP-F04 | `apiV100-firebaseEntryHttp-checkinbiz-addDeviceEmployee` | `services-saas/checkinbiz/firebase-checkinbiz-http/add-device-employee.ts:11` | **Sí** (l.66) | App | `app_constants.dart:70-72` → `auth_remote_datasource.dart:154` |

Las cuatro están desplegadas, así que ninguna llamada viva de un cliente cae en una función inexistente. Queda sin
confirmar que los hosts `…-3bnjgtprva-uc.a.run.app` escritos en los clientes correspondan a esas funciones: el CSV da
nombres, no URLs.

**Rollbacks documentados en comentarios que ya no existen en dev** (volver a ellos daría error):
- `criticalHandler`: `app_constants.dart:47-49,81`. No aparece en el CSV.
- `tasksHandler`: `.env.development:107` y `app_constants.dart:85-86`, ambos presentados como «kept for rollback». No
  está desplegada.
- `documentsHandler`: `app_constants.dart:95,107`.
- `createChecklog` y `updateChecklog`: `app_constants.dart:76,78`.

Una referencia más, declarada pero sin llamada: `geo` (desplegada, l.29), a través de `NEXT_PUBLIC_BACKEND_HELPER_MAPBOX`
(MAP-P48).

---

## 7. Cloud Functions HTTP desplegadas que ningún cliente llama

Son las 52 restantes (56 − 4). «Equivalente» es la ruta del contenedor que la sustituye. Con equivalente, son
candidatas a prueba comparativa y después a retirarse. Sin equivalente, o nadie usa esa funcionalidad o se llama por
otra vía.

| ID | Función (sufijo tras `apiV100-firebaseEntryHttp-`) | Fichero | Equivalente en el contenedor |
|---|---|---|---|
| MAP-N01 | `geo` | `firebase-entry-http/helpers/geo.ts:8` | `POST /api/v1/checkinbiz/geo` |
| MAP-N02 | `enable2FAUser` | `auth/enable2FAUser.ts:10` | `POST /api/v1/checkinbiz/auth/2fa/user/enable` |
| MAP-N03 | `verify2FAUser` | `auth/verify2FAUser.ts:10` | `POST …/2fa/user/verify` |
| MAP-N04 | `get2FAUserStatus` | `auth/get2FAUserStatus.ts:10` | `GET …/2fa/user/status` |
| MAP-N05 | `enable2FA` | `auth/enable2FA.ts:8` | `POST /api/v1/checkinbiz/auth/2fa/enable` |
| MAP-N06 | `verify2FA` | `auth/verify2FA.ts:8` | `POST …/auth/2fa/verify` |
| MAP-N07 | `loginEmployee` | `auth/login-employee.ts:55` | `POST /api/v1/checkinbiz/auth/login` |
| MAP-N08 | `updateAuth` | `auth/update-auth.ts:8` | `PATCH /api/v1/checkinbiz/collaborators/:userId`, que tampoco llama nadie: el panel escribe Firestore (MAP-W01) |
| MAP-N09 | `uploadMedia` | `media/upload-media.ts:8` | `POST /api/v1/media` |
| MAP-N10 | `deleteMedia` | `media/delete-media.ts:8` | `DELETE /api/v1/media` |
| MAP-N11 | `listWebhookEndpoints` | `webhook-delivery/list-webhook-endpoint.ts:8` | `GET /api/v1/events/endpoints` |
| MAP-N12 | `createWebhookEndpoint` | `webhook-delivery/create-webhook-endpoint.ts:8` | `POST /api/v1/events/endpoints` |
| MAP-N13 | `deleteWebhookEndpoint` | `webhook-delivery/delete-webhook-endpoint.ts:8` | `DELETE /api/v1/events/endpoints/:id` |
| MAP-N14 | `toggleWebhookEndpoint` | `webhook-delivery/toggle-webhook-endpoint.ts:8` | `PATCH /api/v1/events/endpoints/:id` (campo `enabled`) |
| MAP-N15 | `stripeWebhook` | `webhooks/stripeWebhook.ts:5` | `POST /api/v1/billing/webhook`. La llama Stripe, no un cliente. Qué URL tiene configurada la cuenta de pruebas de Stripe: sin confirmar |
| MAP-N16 | `users-createUsers` | `users/create-users.ts:8` | `POST /api/v1/users` |
| MAP-N17 | `users-assingUser` | `users/assing-user.ts:8` | `POST /api/v1/entities/collaborators` |
| MAP-N18 | `entity-createEntity` | `entity/create-entity.ts:8` | `POST /api/v1/entities` |
| MAP-N19 | `entity-updateEntity` | `entity/update-entity.ts:8` | `POST /api/v1/entities/update` |
| MAP-N20 | `entity-updateEntityBranding` | `entity/update-entity-branding.ts:8` | `POST /api/v1/entities/branding` |
| MAP-N21 | `subscriptions-subscribe` | `subscriptions/subscribe.ts:8` | `POST /api/v1/billing/subscriptions` |
| MAP-N22 | `subscriptions-unsubscribe` | `subscriptions/unsubscribe.ts:8` | `POST /api/v1/billing/subscriptions/unsubscribe` |
| MAP-N23 | `subscriptions-configBilling` | `subscriptions/configBilling.ts:8` | `POST /api/v1/billing/portal` |
| MAP-N24 | `checkinbiz-createEmployee` | `services-saas/checkinbiz/firebase-checkinbiz-http/create-employee.ts:8` | `POST /api/v1/employees` |
| MAP-N25 | `checkinbiz-updateEmployee` | `…/update-employee.ts:8` | `POST /api/v1/employees/update` |
| MAP-N26 | `checkinbiz-deleteEmployee` | `…/delete-employee.ts:8` | `DELETE /api/v1/employees` |
| MAP-N27 | `checkinbiz-employeesExportHandler` | `…/employees-export.ts:6` | `GET /api/v1/employees/export`, que tampoco llama nadie |
| MAP-N28 | `checkinbiz-validateEmployee` | `…/validate-employee.ts:7` | `POST /api/v1/checkinbiz/auth/validate` (mismo controlador `validateEmployee`). Con `/api/v1/employees/validate` (`validateEmployeeToken`) la equivalencia está sin confirmar |
| MAP-N29 | `checkinbiz-createBranch` | `…/create-branch.ts:8` | `POST /api/v1/branches` |
| MAP-N30 | `checkinbiz-updateBranch` | `…/update-branch.ts:8` | `POST /api/v1/branches/update` |
| MAP-N31 | `checkinbiz-deleteBranch` | `…/delete-branch.ts:8` | `DELETE /api/v1/branches` |
| MAP-N32 | `checkinbiz-responsibilitiesHandler` | `…/responsibility.ts:6` | `/api/v1/employees/responsibilities` (GET, POST, PATCH, DELETE) |
| MAP-N33 | `checkinbiz-analyzeHeuristic` | `…/analyzePattern.ts:46` | `POST /api/analytics/heuristic` |
| MAP-N34 | `checkinbiz-checkbizNotifications` | `…/evaluateNotificationsPush.ts:23` | `POST /api/v1/employees/notifications`, que tampoco llama nadie |
| MAP-N35 | `checkinbiz-checkbizStatsController` | `services-saas/checkinbiz/interfaces/http/report/stats.controller.ts:17` | `POST /api/analytics/panel/stats` |
| MAP-N36 | `checkinbiz-calendarHandler` | `…/calendar.ts:5` | `/api/v1/checkinbiz/calendar`. No cubre `/availability`: la función despacha por `action` (`calendar.ts:9-14`) |
| MAP-N37 | `checkinbiz-recalcDailyReport` | `…/interfaces/http/report/recalculateDailyReport.controller.ts:20` | **Sin equivalente**. Sin confirmar si lo cubre `POST /api/reports/cron/trigger` (S2S) |
| MAP-N38 | `createEvent` | `event/create-event.ts:8` | **Sin equivalente.** Son eventos de PassinBiz (`core/events`), no los webhooks del servicio `events` |
| MAP-N39 | `updateEvent` | `event/update-event.ts:8` | **Sin equivalente** |
| MAP-N40 | `deleteEvent` | `event/delete-event.ts:8` | **Sin equivalente** |
| MAP-N41 | `planifierHelper` | `services-saas/checkinbiz/firebase-entry-schedule/planifierNotificationWorker.ts:17` | **Sin equivalente.** Helper HTTP del worker programado, no de cliente |
| MAP-N42 | `passinbiz-createHolder` | `services-saas/passinbiz/firebase-passinbiz-http/create-holder.ts:8` | **Sin equivalente** (producto PassinBiz; ni panel ni app lo llaman) |
| MAP-N43 | `passinbiz-validateHolder` | `…/validate-holder.ts:8` | Sin equivalente |
| MAP-N44 | `passinbiz-importHoldersFromCsv` | `…/import-holders-from-csv.ts:8` | Sin equivalente |
| MAP-N45 | `passinbiz-deliverApplePass` | `…/deliver-apple-pass.ts:7` | Sin equivalente |
| MAP-N46 | `passinbiz-createStaff` | `…/create-staff.ts:9` | Sin equivalente |
| MAP-N47 | `passinbiz-deleteStaff` | `…/delete-staff.ts:8` | Sin equivalente |
| MAP-N48 | `passinbiz-validateStaff` | `…/validate-staff.ts:7` | Sin equivalente |
| MAP-N49 | `passinbiz-updateHolder` | `…/update-holder.ts:8` | Sin equivalente |
| MAP-N50 | `passinbiz-statsGetdata` | `…/stats-getdata.ts:8` | Sin equivalente |
| MAP-N51 | `apiV100-scheduleCheckbiz-sanitizerChecklogHelper` | `services-saas/checkinbiz/firebase-entry-schedule/sanitizer-checklogs.ts:18` | **Sin equivalente.** Disparo manual por HTTP del saneado programado |
| MAP-N52 | `health` (codebase `health`) | `encodeBiz-SAAS/functions-health/index.js:5` | Sin equivalente (monitorización) |

**Resumen de la sección 7:** 36 funciones con equivalente en el contenedor (N01–N36: candidatas a prueba comparativa
y a retirarse) y 16 sin él (N37–N52: PassinBiz, eventos de PassinBiz, helpers de jobs y monitorización).

### 7a. En el código y no desplegadas en dev (una línea cada una)

Salvo `criticalHandler` y los helpers comentados, están exportadas en el codebase `default`. Un `firebase deploy` de
ese codebase **las volvería a crear**: el código y el despliegue no coinciden.
- `criticalHandler`: `functions-critical/index.js:48` (codebase `critical`; el original en `firebase-entry-http/critical-handler.ts:76` está comentado en `firebase-entry-http/index.ts:24,73`). Su upstream por defecto es producción si no se define `CRITICAL_UPSTREAM_BASE` (`functions-critical/index.js:25`).
- `merlinIa`: `firebase-entry-http/api-express/merlin-ia.ts:11`.
- `checkinbiz-createChecklog`: `services-saas/checkinbiz/firebase-checkinbiz-http/create-checklog.ts:9`.
- `checkinbiz-updateChecklog`: `…/update-checklog.ts:8`.
- `checkinbiz-requestManualChecklog`: `…/request-manual-checklog.ts:8`.
- `checkinbiz-generateReport`: `…/generate-report.ts:12`.
- `checkinbiz-tasksHandler`: `…/tasks.ts:11`.
- `checkinbiz-documentsHandler`: `…/documents.ts:25`.
- `taskStartDelay`: `…/task-start-delay.ts:48` (no exportada en `firebase-checkinbiz-http/index.ts`).
- `helperCreateAuth`, `helperCreateServicePlan`, `helperCreatePass`, `helperCreateDocument`, `helperOnCreateInvoice`, `helpeCatchWebhook`, `helperCreateIndexWebhook`: `firebase-entry-http/helper.ts:15,28,40,50,59,69,82` (comentados en `firebase-entry-http/index.ts:44-54`).

### 7b. Rutas del contenedor con equivalente en Cloud Functions: rollback posible

«Rollback posible» = la función equivalente está desplegada en dev. Las filas con «sí» son las candidatas a prueba
comparativa función/contenedor.

| ID | Ruta del contenedor | Método(s) | Función equivalente | ¿Rollback posible? | La consume |
|---|---|---|---|---|---|
| MAP-R01 | `/api/v1/users` | POST | `users-createUsers` | **Sí** | Panel (P01) |
| MAP-R02 | `/api/v1/users/recovery` | POST | `users-recoveryPassUsers` | **Sí** | Panel (P02). La app sigue en la función (A05) |
| MAP-R03 | `/api/v1/entities/collaborators` | POST | `users-assingUser` | **Sí** | Panel (P03) |
| MAP-R04 | `/api/v1/entities` | POST | `entity-createEntity` | **Sí** | Panel (P04) |
| MAP-R05 | `/api/v1/entities/update` | POST | `entity-updateEntity` | **Sí** | Panel (P05) |
| MAP-R06 | `/api/v1/entities/branding` | POST | `entity-updateEntityBranding` | **Sí** | Panel (P07) |
| MAP-R07 | `/api/v1/billing/subscriptions` | POST | `subscriptions-subscribe` | **Sí** | Panel (P08) |
| MAP-R08 | `/api/v1/billing/subscriptions/unsubscribe` | POST | `subscriptions-unsubscribe` | **Sí** | Panel (P10) |
| MAP-R09 | `/api/v1/billing/portal` | POST | `subscriptions-configBilling` | **Sí** | Panel (P09) |
| MAP-R10 | `/api/v1/billing/webhook` | POST | `stripeWebhook` | **Sí** | Stripe |
| MAP-R11 | `/api/v1/media` | POST | `uploadMedia` | **Sí** | Panel (P12) |
| MAP-R12 | `/api/v1/media` | DELETE | `deleteMedia` | **Sí** | Panel (P11) |
| MAP-R13 | `/api/v1/employees` | POST | `checkinbiz-createEmployee` | **Sí** | Panel (P14) |
| MAP-R14 | `/api/v1/employees/update` | POST | `checkinbiz-updateEmployee` | **Sí** | Panel (P15) |
| MAP-R15 | `/api/v1/employees` | DELETE | `checkinbiz-deleteEmployee` | **Sí** | Panel (P16) |
| MAP-R16 | `/api/v1/employees/export` | GET | `checkinbiz-employeesExportHandler` | **Sí** | Nadie |
| MAP-R17 | `/api/v1/employees/validate` | POST | `checkinbiz-validateEmployee` (equivalencia sin confirmar) | Sin confirmar | Panel (P17, inalcanzable) |
| MAP-R18 | `/api/v1/employees/responsibilities` | GET, POST, PATCH, DELETE | `checkinbiz-responsibilitiesHandler` | **Sí** | Panel (P20: POST, PATCH, DELETE) |
| MAP-R19 | `/api/v1/employees/notifications` | POST | `checkinbiz-checkbizNotifications` | **Sí** | Nadie |
| MAP-R20 | `/api/v1/branches` | POST | `checkinbiz-createBranch` | **Sí** | Panel (P21) |
| MAP-R21 | `/api/v1/branches/update` | POST | `checkinbiz-updateBranch` | **Sí** | Panel (P22) |
| MAP-R22 | `/api/v1/branches` | DELETE | `checkinbiz-deleteBranch` | **Sí** | Panel (P23) |
| MAP-R23 | `/api/v1/checkinbiz/auth/login` | POST | `loginEmployee` | **Sí** | App (A01) |
| MAP-R24 | `/api/v1/checkinbiz/auth/validate` | POST | `checkinbiz-validateEmployee` | **Sí** | App (A02) |
| MAP-R25 | `/api/v1/checkinbiz/auth/2fa/enable` | POST | `enable2FA` | **Sí** | App (A03); panel (P18, roto) |
| MAP-R26 | `/api/v1/checkinbiz/auth/2fa/verify` | POST | `verify2FA` | **Sí** | App (A04); panel (P19, roto) |
| MAP-R27 | `/api/v1/checkinbiz/auth/2fa/user/enable` | POST | `enable2FAUser` | **Sí** | Panel (P43) |
| MAP-R28 | `/api/v1/checkinbiz/auth/2fa/user/verify` | POST | `verify2FAUser` | **Sí** | Panel (P44) |
| MAP-R29 | `/api/v1/checkinbiz/auth/2fa/user/status` | GET | `get2FAUserStatus` | **Sí** | Panel (P45) |
| MAP-R30 | `/api/v1/checkinbiz/collaborators/:userId` | PATCH | `updateAuth` | **Sí** | Nadie |
| MAP-R31 | `/api/v1/checkinbiz/calendar` | GET, POST, PATCH, DELETE | `checkinbiz-calendarHandler` | **Sí** | Panel (P33), app (A09) |
| MAP-R32 | `/api/v1/checkinbiz/geo` | POST | `geo` | **Sí** | Panel (P42) |
| MAP-R33 | `/api/analytics/heuristic` | POST | `checkinbiz-analyzeHeuristic` | **Sí** | Panel (P27) |
| MAP-R34 | `/api/analytics/panel/stats` | POST | `checkinbiz-checkbizStatsController` | **Sí** | Panel (P28) |
| MAP-R35 | `/api/v1/events/endpoints` | GET, POST | `listWebhookEndpoints`, `createWebhookEndpoint` | **Sí** | Panel: solo POST (P37b) |
| MAP-R36 | `/api/v1/events/endpoints/:id` | PATCH, DELETE | `toggleWebhookEndpoint` (solo `enabled`), `deleteWebhookEndpoint` | **Sí** (PATCH, parcial) | Panel (P37c-d) |
| MAP-R37 | `/api/v1/checkinbiz/checklogs` | POST | `checkinbiz-createChecklog` | **No** (no desplegada) | Panel (P24), app (A07) |
| MAP-R38 | `/api/v1/checkinbiz/checklogs/update` | POST | `checkinbiz-updateChecklog` | **No** | Panel (P25), app (A08) |
| MAP-R39 | `/api/v1/checkinbiz/checklogs/manual-request` | POST | `checkinbiz-requestManualChecklog` | **No** | Panel (P26) |
| MAP-R40 | `/api/v1/gpt/interpret` | POST | `merlinIa` (a su vez un proxy al contenedor, `merlin-ia.ts:9`) | **No** | Panel (P29) |
| MAP-R41 | `/api/reports/generate` | POST | `checkinbiz-generateReport` | **No** | Panel (P31) |
| MAP-R42 | `/api/reports/:reportId/download` | GET | `checkinbiz-documentsHandler` (reportRouter) | **No** | Panel (P40) |
| MAP-R43 | `/api/v1/tasks/*` (salvo pause, resume y duplicate, que no tienen equivalente) | GET, POST, PATCH, DELETE | `checkinbiz-tasksHandler` | **No** | Panel (P35), app (A10–A21) |
| MAP-R44 | `/api/v1/documents/*` | GET, POST, PATCH, DELETE | `checkinbiz-documentsHandler` | **No** | Panel (P38–P39), app (A22–A25) |

Sin equivalente en Cloud Functions (el rollback no aplica): `/api/analytics/panel/overview`, `/api/v1/gpt/panel`,
`/api/reports/tasks`, `/calendar/availability[/day]`, `DELETE /checkinbiz/collaborators/:userId`, las tareas
`pause`, `resume` y `duplicate`, `events` catálogo/test/rotate-secret/deliveries/replay, y todo `rentmanbiz`.

**Lo que más pesa:** fichajes, tareas, documentos e informes (el núcleo operativo de la app y del panel) no tienen
rollback en dev. Sus funciones se retiraron del despliegue.

---

## 8. Rutas del contenedor publicadas en nginx que ni el panel ni la app llaman

Todas las rutas quedan publicadas por los `location` de prefijo de `nginx.staging.conf:93-200`. Se excluyen las S2S y
los webhooks entrantes (lista al final).

| ID | Servicio | Ruta sin llamante | Router | Nota |
|---|---|---|---|---|
| MAP-U01 | checkinbiz | `GET /api/v1/checkinbiz/status` | `checkinbiz.router.ts:14` | Sonda |
| MAP-U02 | checkinbiz | `POST /api/v1/checkinbiz/collaborators` | `collaborator.router.ts:122` | — |
| MAP-U03 | checkinbiz | `PATCH /api/v1/checkinbiz/collaborators/:userId` | `collaborator.router.ts:162` | Sustituye a `updateAuth`, pero el panel sigue escribiendo `user_entity_roles` a mano (W01, W02) |
| MAP-U04 | employees | `GET /api/v1/employees/export` | `employee.router.ts:327` | — |
| MAP-U05 | employees | `PATCH /api/v1/employees/:employeeId` | `employee.router.ts:362` | — |
| MAP-U06 | employees | `DELETE /api/v1/employees/:employeeId` | `employee.router.ts:367` | — |
| MAP-U07 | employees | `POST /api/v1/employees/:employeeId/email` | `employee.router.ts:372` | El comentario la atribuye al panel de add-ons, pero no hay llamante |
| MAP-U08 | employees | `GET /api/v1/employees/responsibilities` | `responsibility.router.ts:229` | El panel y la app leen Firestore |
| MAP-U09 | employees | `POST /api/v1/employees/notifications` | `notification.router.ts:28` | Hay variable (P41), pero sin uso |
| MAP-U10 | employees | `POST /api/v1/employees/validate` | `employeePublic.router.ts:13` | Solo la pide P17, inalcanzable. Su comentario (:9) dice que la usa la app, pero la app va a `/checkinbiz/auth/validate` |
| MAP-U11 | branches | `PATCH /api/v1/branches/:branchId` | `branch.router.ts:186` | — |
| MAP-U12 | branches | `DELETE /api/v1/branches/:branchId` | `branch.router.ts:190` | — |
| MAP-U13 | entities | `PATCH /api/v1/entities/:entityId` | `entity.router.ts:154` | — |
| MAP-U14 | billing | `GET /api/v1/billing/subscriptions/:entityId` | `billing.router.ts:14` | El panel lee las suscripciones de Firestore |
| MAP-U15 | billing | `GET /api/v1/billing/subscriptions/:entityId/:serviceId` | `billing.router.ts:20` | — |
| MAP-U16 | billing | `DELETE /api/v1/billing/subscriptions/:entityId/:serviceId` | `billing.router.ts:59` | — |
| MAP-U17 | events | `GET /api/v1/events/status` | `events.router.ts:29` | Sonda |
| MAP-U18 | events | `GET /api/v1/events/endpoints` | `events.router.ts:94` | El panel lista desde Firestore (`integration.service.ts:21`) |
| MAP-U19 | tasks | `GET /api/v1/tasks/:taskId/activity` | `taskRouter.ts:25` | El panel y la app leen la subcolección `activity` de Firestore |
| MAP-U20 | rentman | `GET /api/v1/rentmanbiz/status` | `rentman.router.ts:30` | Sonda |
| MAP-U21 | rentman | `GET /api/v1/rentmanbiz/crew/:entityId` | `rentman.router.ts:133` | Admitida en la allowlist (SBP:339), sin llamante |
| MAP-U22 | rentman | `POST /api/v1/rentmanbiz/tasks/push` | `rentman.router.ts:444` | Sin llamante en panel, app, SAAS ni monorepo |
| MAP-U23 | merlin | `/api/interpret` | `merlin/src/app.ts:24` | Alias que nginx **no publica**: inalcanzable desde fuera |
| MAP-U24 | sales | `POST /api/v1/sales/leads` | `sales.router.ts:188` | La usa la landing, un cliente externo fuera de este alcance |
| MAP-U25 | sales | `GET /api/v1/sales/exports/google-ads-leads.csv` | `salesExport.router.ts:54-55` | Google Ads (Basic auth), externo |
| MAP-U26 | backoffice | `/api/v1/backoffice/*` (config, session, staff, entities, employees, branches, leads, stats, maintenance, puesta-en-marcha) y `/backoffice/` | `backoffice.router.ts:18-28`, `publicConfig.router.ts:15` | La consume la SPA `encodebiz-api/apps/backoffice-web`, no el panel ni la app |

**Excluidas como S2S o webhook:**
- analytics `/patterns/*`, `/dimensions/sync` y `/build/pattern-snapshot` (`requireApiKey`, `analytics/src/app.ts:26`; llamante `encodeBiz-SAAS/functions/src/core/analytics/infrastructure/AnalyticsServerClient.ts:34`).
- sync `/checklogs` y `/task-ratings` (`AnalyticsServerClient.ts:26,30`).
- reports `/cron/trigger` y `/status` (`report.router.ts:69,77`).
- tasks `/system` (`rentman/src/infrastructure/HttpTasksClient.ts:58`).
- events `/s2s/publish` (`events.router.ts:237`).
- backoffice `/s2s/maintenance/*`.
- checkinbiz `/collaborators/one` y `/collaborators/session` (`backoffice/src/infrastructure/clients/CheckinbizClient.ts:56,85`).
- rentman `/sync/hours` (`:516`) y `/webhook/:entityId` (`:532`).
- billing `/webhook` (Stripe) y `/internal/invoices/:id/send`.
- merlin `/gpt/soporte/*`.
- sales con `hiddenApiKey` (`/status`, `/ga4/*`, `GET /leads`, `/conversions`, `/maintenance/cleanup`).

---

## Resumen

- **Endpoints consumidos por el panel: 92 (contenedor 90 · Cloud Functions 2).** Pares método+ruta distintos: 45 de
  ruta fija (sección 1) y 45 de subruta por proxy (sección 1b). Las dos funciones son `deleteEntity` y `sendEmail`.
  3 de los 90 (P17, P18 y P19) solo se piden desde `/tools/checking`, que el middleware redirige a mantenimiento.
- **Endpoints consumidos por la app: 27 (contenedor 25 · Cloud Functions 2).** Las dos funciones son
  `recoveryPassUsers` y `addDeviceEmployee`, las dos desplegadas.
- **Problemas de mapeo.** No hay ninguna ruta viva con método distinto ni 404 previsible. Sí hay esto:
  1. MAP-P06: borrar una empresa sigue en la función `deleteEntity`. La exclusión es deliberada (`entity.router.ts:15-19`).
  2. MAP-P49: el formulario de contacto llama a la función `sendEmail` desde el navegador, sin proxy y sin equivalente en el contenedor.
  3. MAP-A05: la app recupera la contraseña en la función, aunque `POST /api/v1/users/recovery` ya existe.
  4. MAP-A06: la app llama a `addDeviceEmployee` en una función que no tiene ruta en el contenedor.
  5. MAP-P17, P18 y P19: en el 2FA de empleado y el validate del panel, el proxy exige un ID token de Firebase y el contenedor un JWT de sesión propio. Resultado previsible: 403. Además, la pantalla es inalcanzable.
  6. MAP-P36: la allowlist admite `mappings`, que no existe en el contenedor (sería 404), y `crew`, que nadie llama.
  7. Variables sin uso: P41 (`…_NOTIFICATIONS`) y P48 (`…_HELPER_MAPBOX`). Redundante: P13. Handlers sin variable: `create_webhook`, `delete_webhook` y `checkinbiz_generate_report`.
  8. MAP-P42: el proxy de geo no exige auth y el contenedor sí.
  9. Nota A: seis handlers de raíz sin `subPathPattern`, que abren todo `/api/v1` o `/api`.
  10. Comentarios y rollbacks obsoletos: `.env.development:51,107,119`, SBP:355-358 y `app_constants.dart:47-49,76-86,95`. Remiten a `criticalHandler`, `tasksHandler`, `documentsHandler`, `createChecklog` y `updateChecklog`, ninguna desplegada.
  11. La app cae a producción si la build no lleva `ENVIRONMENT=development` (`app_config.dart:7-10`).
- **Escrituras directas a Firestore/Storage desde el panel: 13, de ellas sensibles: 9** (más el perfil propio, W05).
  Storage: 0 (el helper de subida está muerto).
- **Escrituras directas desde la app: 10**, de ellas sensibles 2: `employees.language` (AW03) y
  `in_app_notifications.validationStatus` de un cambio de fichaje (AW10). Storage: 0.
- **Rollback en dev** (7b): 34 rutas del contenedor tienen su función equivalente desplegada (R01–R16 y R18–R36; R17
  sin confirmar). **Fichajes, tareas, documentos, informes y Merlin no lo tienen** (R37–R44).
- **Lo que falta para poder decir «migración HTTP completa»:**
  1. Resolver `deleteEntity`: portarlo con su cascada `onDeleteEntity` o dejar escrito que se queda en Firebase y excluirlo del alcance.
  2. Dar al formulario de contacto una ruta en el contenedor detrás del proxy y retirar `NEXT_PUBLIC_BACKEND_ENDPOINT_CONTACT`.
  3. En la app: pasar la recuperación a `/api/v1/users/recovery` y retirar `addDeviceEmployee`, o crearle ruta. Hace falta build nueva.
  4. Llevar al contenedor las escrituras sensibles del panel. Con ruta ya existente: W01 y W02 → `PATCH /checkinbiz/collaborators/:userId`; W03 y W04 → `/entities/update` o `PATCH /entities/:id`; W13 → `DELETE /checkinbiz/calendar`. Sin ruta todavía: `jobs` (W06–W08), `reports` (W12), `users` (W05) e `issues` (W09–W11).
  5. En la app: pasar a HTTP la escritura en `employees` (AW03) y el estado de validación de fichajes (AW10). `issues` y `notification_tokens` no tienen ruta.
  6. Arreglar o retirar `/tools/checking`, y con él los handlers P17–P19.
  7. Limpiar variables y handlers muertos y **contrastar las variables efectivas en Vercel (dev)**, que pueden no coincidir con `.env.development`.
  8. Alinear el código de las functions con lo desplegado (sección 7a) antes del próximo `firebase deploy`. Si se quiere rollback para fichajes, tareas y documentos, hay que redesplegar sus funciones a propósito.
  9. Si «completa» incluye las lecturas: casi todas van directas a Firestore en los dos clientes (secciones 2b y 5b). Algunas tienen ya un GET en el contenedor sin usar (U08, U14, U18, U19; tareas y responsabilidades). Otras no lo tienen: fichajes, empleados, sucursales, informes y usuarios.


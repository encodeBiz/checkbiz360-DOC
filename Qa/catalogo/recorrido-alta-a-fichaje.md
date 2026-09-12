# Recorrido de alta a primer fichaje — catálogo para la prueba de punta a punta (desarrollo)

> **Verificación (2026-09-11).** Este catálogo sale de un análisis estático del código del
> panel, la app y los servicios, y antes de publicarlo se ha comprobado por muestreo contra
> el código. Confirmado:
>
> - Suscribir una empresa con datos legales pero sin cliente de Stripe acaba en **500
>   `internal_error`**. `Subscribe.ts` lanza un error con el código
>   `subscribe/entity_not_configured` dentro del texto, nadie lo captura y el manejador
>   general de billing lo convierte en un 500 genérico.
> - El formulario de sucursal crea la sucursal **con la geocerca desactivada** si nadie
>   marca la casilla: el campo significa «activar», arranca en `false` y se envía invertido.
> - El formulario de empleado crea al empleado con **`enableA2F: false`**.
> - La sucursal automática la crea el trigger **`onActivateCheckbiz`** al nacer
>   `entities/{eid}/subscriptions/{sid}`; está desplegado y activo en desarrollo.
>
> Lo que no aparece aquí como confirmado es lectura del código, no comprobación.

Análisis estático, 2026-09-11. No se ha hecho ninguna petición ni se ha ejecutado nada. Todas las
referencias son `fichero:línea` sobre estas raíces (todas bajo `/Users/joseacevedo/Documents/EncodeBiz-ALL/PLATAFORMA/`):

- `PANEL:` → `encodebiz-front-saas/src/`
- `APP:` → `checkbiz360/lib/`
- `API:` → `encodebiz-api/`
- `FN:` → `encodeBiz-SAAS/functions/src/`

**Aviso sobre las URLs del panel.** Las que se citan salen de `encodebiz-front-saas/.env.development`
(sin valores sensibles). Las variables que usa de verdad un panel desplegado viven en Vercel y pueden no
coincidir con ese fichero; `NEXT_PUBLIC_URI` apunta ahí a `http://localhost:3000` (`.env.development:1`),
así que ese fichero describe un panel local. No se ha leído ningún `.env` de producción.

---

## Lo que vale para todos los pasos

**Panel → navegador → proxy de Next → contenedor.** El navegador nunca llama al contenedor: llama a
`/api/proxy/<handler>` de su mismo origen con `Content-Type: application/json`, `Cache-Control: no-store`,
`authorization: Bearer <ID token de Firebase>` y `locale` (`PANEL:lib/http/httpClientFetchNext.ts:62-71`).
El proxy comprueba el handler contra su lista (`PANEL:lib/http/serverBackendProxy.ts:49-432`), verifica el
ID token con el Admin SDK (`:570-581`) y reenvía al contenedor **solo** `Authorization`, `locale`,
`Content-Type` y `Cookie` (`:595-601`), con `redirect: 'error'` (`:613`). El contenedor no ve ni el `Origin`
ni el `User-Agent` del navegador: ve los del runtime de Node de Next (valor exacto sin confirmar).

**Middleware del panel (`PANEL:proxy.ts`).** Exige la cookie `2fa_session` en `/main/**` y en todo
`/api/proxy/**` salvo `recovery_pass`, `create_user`, `status2fa_user`, `enable2fa_user` y `verify2fa_user`
(`:88-94`, `:136-193`). Sin cookie, `/main/**` redirige a `/auth/2fa?redirect=…` (`:182-185`, `:217-222`) y el
proxy responde 401 `auth/2fa_required`. Solo actúa si existe `NEXT_2FA_SESSION_SECRET` (`:140-150`);
`.env.development:27` la define. La cookie dura 1 h y es un HMAC de `uid.expiresAt`
(`PANEL:lib/auth/twoFASessionCookie.ts:14-15`, `:61-69`).

**Observado:** ningún contenedor mira las claims `twoFA`/`admin`. `requireFirebaseAuth` solo hace
`verifyIdToken(token, true)` (`API:packages/shared/src/middleware/firebaseAuth.ts:4-21`). El segundo factor del
panel lo impone únicamente ese middleware de Next: una prueba que llame directa al contenedor no pasa por él.

**nginx de desarrollo** (`API:nginx/nginx.staging.conf`): `141.95.47.135:8080`, sin TLS. Solo reescribe `Host`
y `X-Forwarded-*` (`:50-53`), así que el `User-Agent` llega intacto. Raíces exactas sin barra
(`:67-80`) y prefijos (`:98-191`).

**App.** Base de desarrollo `http://141.95.47.135:8080` si se compila con `ENVIRONMENT=development`
(`APP:core/constants/app_constants.dart:33-38`, `APP:core/config/app_config.dart:7-10,38`). Dio manda
`Content-Type` y `Accept: application/json` (`APP:core/network/dio_client.dart:21-24`) y un interceptor pone
**`User-Agent: <deviceId persistente>`** en cada petición (`:37-46`; `APP:main_development.dart:57-59`;
`APP:application/services/device_info_service.dart:65-112`). Ante cualquier 401, o `code: auth/unauthorized`,
`AuthRetryInterceptor` refresca el ID token de Firebase y **reintenta una vez sustituyendo `Authorization` por
ese ID token** (`APP:infrastructure/network/auth_retry_interceptor.dart:26-93`). Si falla otra vez, publica
«sesión caducada» y la app rehace login + validate (`:52`).

---

## REC-01 · Registro del usuario en el panel

**Quién.** `PANEL:app/auth/register/page.controller.tsx:76-99` → `registerAccount` (`PANEL:services/core/account.service.ts:82-95`).

**1a. Navegador → ruta de Next (mismo origen).** `POST /api/auth/register`.
- Cabeceras: `Content-Type: application/json`, `Cache-Control: no-store`, `locale`, `cf-turnstile-response`.
- Cuerpo: `{ email, password, fullName, phone }`, tal cual los teclea el usuario en el formulario.

**1b. Lo que hace la ruta en el servidor** (`PANEL:app/api/auth/register/route.ts`):
- Turnstile primero (`:60-65`). **En desarrollo se da por pasado** (`PANEL:lib/turnstile/verifyTurnstileToken.ts:49`, `NEXT_PUBLIC_ENV === 'dev'`).
- Valida el correo con una expresión regular, la contraseña (8 caracteres como mínimo) y el nombre (`:77-84`).
- **Crea la cuenta con el Admin SDK**: `createUser({ email, password, displayName: fullName })` (`:95-104`). No hay ningún `accounts:signUp` desde el navegador.
- Canjea un custom token por un ID token en `https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=<API key web de dev>` (`:124-137`).
- **Crea la ficha, de servidor a servidor**: `POST http://141.95.47.135:8080/api/v1/users` (`NEXT_BACKEND_URI_CREATE_USER`, `.env.development:33`) con `Content-Type`, `Authorization: Bearer <idToken>` y `locale`, y cuerpo `{ fullName, phoneNumber, uid, email }` (`:142-153`).
- Si algo falla después de crear la cuenta, borra el usuario de Auth (`:109-115`, `:167-170`).
- Responde 201 `{ customToken, uid }`, con un custom token nuevo (`:163-166`).

**1c. Contenedor `entities`** (nginx `= /api/v1/users` → entities, `nginx.staging.conf:80`; montaje autenticado en `API:services/entities/src/app.ts:31`).
`userRouter.post("/")` (`API:services/entities/src/interfaces/http/user.router.ts:19-66`):
- 403 si el `uid` del cuerpo no coincide con el del token (`:28-30`). 400 si falta alguno de los cuatro campos (`:23-37`).
- Escribe `users/{uid}` = `{ uid, email, fullName, phoneNumber, createdAt, lastLoginAt, active: true }` (`:39-47`).
- Si la persona no tiene asiento en ninguna empresa, envía el correo `WELLCOME_EMAIL` (`:54-63`).
- Responde 201 `{ message: "Usuario creado" }`.

**1d. Navegador.** `signInWithCustomToken(customToken)` (SDK de Firebase Auth; `PANEL:lib/firebase/authentication/login.ts:36-47`).
`updateUserData` lee `users/{uid}` directamente de Firestore (`PANEL:contexts/authContext.tsx:56-66`; `account.service.ts:131-142`).
Después navega a `/main/core/entity/create` (`page.controller.tsx:86`).

**Verificación de correo:** no existe. No hay `sendEmailVerification` ni comprobación de `email_verified` en el panel, la app ni la API (búsqueda sin resultados).

**1e. Segundo factor del panel (obligatorio con el middleware activo).** Al entrar en `/main/core/entity/create` sin cookie, el middleware redirige a `/auth/2fa?redirect=/main/core/entity/create`.
- **Estado.** `GET /api/proxy/status2fa_user` con `Authorization: Bearer <idToken>` (`PANEL:app/auth/2fa/page.controller.tsx:57-58`; `account.service.ts:167-175`) → `GET http://141.95.47.135:8080/api/v1/checkinbiz/auth/2fa/user/status` (`.env.development:131`; `API:services/checkinbiz/src/interfaces/http/auth/auth.router.ts:83`; `…/user2FA.controller.ts:36-54`). Responde `{ enabled: false }` y el panel lleva a `/auth/2fa/setup?redirect=…` (`2fa/page.controller.tsx:49,59-61`).
- **Activación.** `POST /api/proxy/enable2fa_user`, sin cuerpo (`2fa/setup/page.controller.tsx:59-63`; `account.service.ts:181-189`) → `POST …/api/v1/checkinbiz/auth/2fa/user/enable` (`.env.development:129`; `user2FA.controller.ts:57-95`). Guarda `users/{uid}/security/twoFA` = `{ secret, otpauthUrl, verifiedAt: null, createdAt }`; si ya había un alta a medias, reutiliza ese secreto (`:73-86`). Responde `{ secret, otpauthUrl, qrImage }`.
- **Verificación.** `POST /api/proxy/verify2fa_user` con `{ code }` (`setup/page.controller.tsx:89-91`; `account.service.ts:195-203`) → `POST …/auth/2fa/user/verify` (`user2FA.controller.ts:98-139`). Errores: 400 `twofactor/not_activated`, 401 `twofactor/invalid_code`. Si el código es bueno, pone `verifiedAt`, borra `otpauthUrl` y **fija las claims `admin: true, twoFA: true`** (`:127-137`).
- **Cookie de sesión.** El panel refresca el token con `getIdToken(true)` (`setup:94`) y llama a `POST /api/auth/2fa-session` con `{ idToken }`, que devuelve `Set-Cookie: 2fa_session` (`setup:98-102`; `PANEL:app/api/auth/2fa-session/route.ts:24-45`). Después sigue el `redirect` o consulta `user_entity_roles` en Firestore (`setup:119-132`; `PANEL:services/core/entity.service.ts:26-62`).

**Qué se usa después:** el `uid`, la sesión de Firebase (ID token y refresh token), el `secret` TOTP y la cookie `2fa_session` (solo si se pasa por el proxy).
**Precondiciones:** ninguna.
**Camino alternativo:** `/main/user/complete-profile` todavía crea la ficha por `/api/proxy/create_user` (`account.service.ts:101-126`; `serverBackendProxy.ts:86-91`). No forma parte del alta normal.

---

## REC-02 · Alta de la empresa (entidad)

**Quién.** `PANEL:app/main/core/entity/create/page.controller.tsx:63-98` → `createEntity` (`PANEL:services/core/entity.service.ts:107-130`).

**Llamada.** `POST /api/proxy/create_entity` → `POST http://141.95.47.135:8080/api/v1/entities` (`.env.development:38`; nginx `= /api/v1/entities`, `:79`).
- Cabeceras: `authorization: Bearer <ID token>` (el token lo guarda `authContext.tsx:77`) y `locale`. Por el proxy, además, la cookie `2fa_session`.

**Cuerpo** (`page.controller.tsx:67-79`):
```
{ name, slug: createSlug(name), billingEmail /* por defecto, el correo del usuario */,
  language /* 'ES' | 'EN'; 'ES' si falta */,
  legal: { legalName, taxId /* por defecto "N/A" */, address },
  active: true }
```
`address` lo rellena `AddressComplexInput` con lo que devuelve el geocodificador (mismas llamadas que en REC-05): `{ country, postalCode, street, geo: { lat, lng }, timeZone }` (`PANEL:components/common/forms/fields/AddressComplexInput.tsx:141-148`).

**Obligatorio en el formulario:** `name`, `language`, `taxId`, `legalName`, y de la dirección solo `country` y `postalCode` (`page.controller.tsx:55-62`; `PANEL:config/yupRules.tsx:81-85`). La calle, `geo` y `timeZone` no son obligatorios en el formulario.
**Obligatorio en el contenedor:** solo `name` (cadena) y `active` (booleano) (`API:services/entities/src/interfaces/http/entity.router.ts:60-64`).

**Qué hace el contenedor** (`entity.router.ts:56-96`):
- Crea `entities/{autoId}` con todo el cuerpo más `slug: slugify(name)` —el `slug` del panel se sobrescribe—, `language`, `createdAt` e `id` (`:69-76`; `API:packages/shared/src/platform/FirestoreEntityRepository.ts:10-15`).
- Indexa la entidad en `searchIndex` (`:78`, `:42-52`).
- **Documento de rol.** `grantSeat` hace una llamada S2S `POST http://checkinbiz:3002/api/v1/checkinbiz/collaborators` con `x-encodebiz-key` y `{ entityId, email: <correo del token>, role: "owner", grantedBy: uid }` (`:84-89`; `API:services/entities/src/application/collaborators.ts:30-62`). Ese servicio escribe **`user_entity_roles/{uid}_{entityId}`** = `{ userId, entityId, role: "owner", status: "active", createdAt, grantedBy, grantedReason: null, support: false }` (`API:services/checkinbiz/src/interfaces/http/collaborator/collaborator.router.ts:122-150`; `…/manageCollaborator.ts:120-148`; `…/FirestoreEntityMembershipRepository.ts:59-78`).
- **Observado:** el resultado de `grantSeat` no se comprueba (`entity.router.ts:86`). Si el asiento falla, o si el token no trae correo (`:84-89`), la entidad se crea sin propietario y la respuesta sigue siendo 201.
- Responde 201 `{ code: "entity/create_success", message, entity }` (`:91-95`).

**Qué hace el panel después.** Usa `entity.id` (`page.controller.tsx:80-86`) y llama a `changeCurrentEntity`, que **escribe directamente en Firestore** `user_entity_roles/{id}` = `{ isActive, updatedAt }` (`PANEL:contexts/entityContext.tsx:146-166`; `entity.service.ts:84-101`). Luego navega a `/main/{entityId}/dashboard`.

**Qué queda configurado:** nombre, datos legales y dirección (con `timeZone` y `geo` solo si se eligió una sugerencia del buscador).
**Qué no queda:** `stripeCustomerId`, `billingConfig`, calendario, suscripción y sucursal.
**Precondiciones:** REC-01 completo (con la cookie 2FA si se va por el proxy) y un ID token que traiga `email`.

---

## REC-03 · Plan del servicio de fichaje

**Orden del panel.** El onboarding pone el pago primero: `payment, schedule, workplace, team, testCheckin` (`PANEL:domain/features/onboarding/IOnboarding.ts:33-35`; `PANEL:components/features/onboarding/OnboardingEngine.tsx:108-119`).
Los planes se leen directamente de Firestore, en `service/{service}/plan` (`PANEL:services/core/subscription.service.ts:14-21`), y se muestran en `PANEL:app/main/[entityId]/[service]/onboarding/page.tsx:8,82`.

**Botón del plan** (`PANEL:components/common/PricingCard/PricingCard.controller.tsx:83-100`):
- Si el plan es `freemium`, suscribe directamente (`:85-86`).
- En cualquier otro plan exige `billingEmail`, `legal.legalName`, `legal.taxId` y `billingConfig.payment_method` no vacío; si falta algo, abre el modal de facturación (`:88-89`). Los planes conocidos en el código son `freemium | bronze | enterprise` (`PANEL:domain/core/IService.tsx:37`).

**Llamada.** `POST /api/proxy/subcribe` → `POST http://141.95.47.135:8080/api/v1/billing/subscriptions` (`.env.development:44`).
- Cabeceras: `authorization: Bearer`, `locale`.
- Cuerpo: `{ entityId, serviceId: "checkinbiz", planId }` (`PricingCard.controller.tsx:28-35`; `subscription.service.ts:43-61`).

**Contenedor `billing`** (`API:services/billing/src/interfaces/http/billing.router.ts:31-56`):
- 400 `invalid_payload` si falta un campo; 400 `unknown_service`; 403 `forbidden` si no pasa `canWrite`; 404 `entity_not_found`.
- **Sin datos legales** —`name`, `legal.taxId`, `legal.legalName`, `legal.address`— responde **400 `entity_not_configured`** (`:44-47`; `FirestoreEntityRepository.ts:51-57`). Ojo: `taxId: "N/A"` cuenta como dato legal.
- 409 `already_subscribed`.
- `Subscribe.execute` (`API:services/billing/src/application/Subscribe.ts:20-72`) busca el plan (`subscribe/not_found`) y **exige `entity.stripeCustomerId`**; si no lo hay, lanza un `Error` (`:23-25`) que acaba en **500 `internal_error`** (`API:services/billing/src/app.ts:35-38`).
- Crea `entities/{eid}/subscriptions/checkinbiz` con `status: "pending"` (`Subscribe.ts:29-38`; `…/FirestoreSubscriptionRepository.ts:50-53`).
- Crea la suscripción en Stripe con `quantity` igual al uso actual y 45 días de prueba si la empresa no ha estado suscrita antes (`Subscribe.ts:9,55-62`).
- Pasa a `active` solo si el plan es `freemium` o `payPerUse`; si no, se queda `pending` (`:64-67`).
- Responde 201 `{ ok: true, sid }`.

**De dónde sale `stripeCustomerId`.** Solo de `POST /api/v1/billing/portal` (`billing.router.ts:91-107`). El panel lo llama al montar la pestaña de facturación, siempre que haya `legalName` o `taxId` (`PANEL:app/main/[entityId]/entity/tabs/tabBilling/page.controller.tsx:65-79`; handler `configbilling`, `.env.development:45`). La búsqueda de escrituras de `stripeCustomerId` no encuentra otro sitio en la API.
**Observado:** quien va directo a `freemium` sin haber abierto antes esa pestaña obtiene un 500.
La tarjeta llega a `billingConfig.payment_method` por el webhook `payment_method.attached` (`API:services/billing/src/application/StripeWebhookHandler.ts:67-73,233-253`).

**Efectos en Cloud Functions.**
- `onActivateCheckbiz` (europe-west1) se dispara al **crearse** `entities/{eid}/subscriptions/{sid}` con `serviceId: checkinbiz` y crea la **sucursal automática** si la empresa no tiene ninguna (`FN:services-saas/checkinbiz/firebase-firestore-trigger/onActivateCheckbiz.ts:6-14`; `FN:services-saas/checkinbiz/interfaces/triggers/createEntityBranch.controller.ts:116-183`). Esa sucursal toma `address = entity.legal.address`, `name = entity.name`, `ratioChecklog: 500`, `disableRatioChecklog: false` y `advance` 08:00–17:00 con 60 min de descanso (`:131-153`). Si la dirección no trae `street`, `country`, `timeZone` y `geo` numérico, no la crea y solo deja un `console.error` (`:25-55`, `:154-164`).
- `onDocumentWriteSubscriptions` envía un correo cada vez que cambia el estado (`FN:firebase-firestore-trigger/subscriptions/onDocumentWrite-subscriptions.ts:5-19`).

**Precondición de los pasos siguientes.** Para crear sucursales y empleados hace falta que exista `entities/{eid}/subscriptions/checkinbiz` con `plan` (el `status` no se mira) y el documento de plan `service/checkinbiz/plan/{plan}`. Si no, 403 `subscription/limit_off` (`API:packages/shared/src/checkbiz/plan/subscriptionLimits.ts:29-69`).

**Sin confirmar:** si en `dev-encodebiz` existe el plan `freemium` con `stripePrice`, si `billing` de desarrollo tiene claves de Stripe de prueba y si el webhook de Stripe llega al entorno de desarrollo.

---

## REC-04 · Horario y calendario de empresa

**Quién.** `PANEL:app/main/[entityId]/checkinbiz/calendar/components/EntityCalendarTab.tsx`.
- La zona horaria es `entity.legal.address.timeZone`, o `"UTC"` si falta (`:81`).
- Lee `entities/{id}/calendar/config` directamente de Firestore (`:88`).
- Guarda con `CalendarSection.handleSave` (`…/CalendarSection.tsx:391-440`).

**Horario.** `PATCH /api/proxy/checkinbiz_calendar_handler` (`PANEL:services/checkinbiz/calendar.service.ts:11,24-39`) → `PATCH http://141.95.47.135:8080/api/v1/checkinbiz/calendar` (`.env.development:96`).
- Cuerpo (`CalendarSection.tsx:408-422`; tipos en `PANEL:domain/features/checkinbiz/ICalendar.ts:14-79`):
```
{ scope: "entity", entityId,
  defaultSchedule: { monday: { shifts: [{ start: {hour,minute}, end: {hour,minute}, id }],
                               strictRange?: true, disabled: bool }, … sunday },
  timezone,
  advance: { enableDayTimeRange, disableBreak, timeBreak, notifyBeforeMinutes },
  overridesDisabled }
```
- Esa forma de día es la de `sanitizeSchedule` en `PANEL:app/main/[entityId]/checkinbiz/branch/form/form.controller.tsx:108-128`. La función equivalente dentro de `CalendarSection` no se ha leído.

**Festivos.** Una llamada por festivo al mismo endpoint, con `{ scope, entityId, holiday: { id, name, date: "YYYY-MM-DD", description?, paid? } }` (`CalendarSection.tsx:442-469`).

**Contenedor.** `calendar.router.ts:41-59` reparte por `scope` hacia `upsertEntityCalendarController` (`API:services/checkinbiz/src/interfaces/http/calendar/upsertEntityCalendar.controller.ts:8-48`):
- Exige `entityId` y al menos uno de `defaultSchedule`, `holiday`, `timezone` o `advance`.
- Valida la semana con `validateWeeklySchedule`.
- Responde 200 `{ code: "calendar/entity_upserted", entityId }`.
- **Observado:** en ese controlador no hay comprobación de `canWrite`; basta con un ID token válido.

**Por qué importa.**
- Sin calendario de entidad, `GET /calendar` devuelve 404 `calendar/not_found`; sin zona horaria, 400 `calendar/missing_timezone` (`API:packages/shared/src/calendar/resolveEffectiveCalendar.usecase.ts:55-62`). Eso rompe REC-10.
- El fichaje, en cambio, cae a una jornada abierta 00:00–23:59 cuando no hay nada configurado (`API:services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts:204-230`).
- El onboarding solo da el paso por hecho si hay algún turno en la semana (`PANEL:services/onboarding/onboardingState.service.ts:27-35,138`). Para saberlo, primero lee `GET …/calendar?scope=entity&entityId=…` (`:80-93`; `calendar.service.ts:119-130`).

**Horario por defecto del panel:** los valores de `buildDefaultSchedule` en `EntityCalendarTab` no se han leído (sin confirmar).
**Precondiciones:** la entidad existe. Para que haya zona horaria, `legal.address.timeZone` tiene que venir del geocodificador.

---

## REC-05 · Alta de sucursal

**Geocodificación.** `AddressComplexInput` → `POST /api/proxy/checkinbiz_geo` → `POST http://141.95.47.135:8080/api/v1/checkinbiz/geo` (`.env.development:126`; `PANEL:services/core/helper.service.ts:63-84`).
- Cabeceras: `authorization: Bearer`, `locale`.
- **Autocompletar:** `{ address: <texto en minúsculas>, country: <ISO-2 o "">, sessionToken: <uuid>, action: "autocomplete" }` (`AddressComplexInput.tsx:54,80`). Responde `[{ addressQuery, country, lat: null, lng: null, placeId, provider, resolvedText, sessionToken, timeZone }]` (`helper.service.ts:31-41`), o 404 `{ predictions: [] }` si no hay nada.
- **Detalle:** `{ placeId, provider, sessionToken, action: "placedetails" }` (`AddressComplexInput.tsx:131`). Responde `{ formattedAddress, lat, lng, provider, timeZone, country?, countryCode?, region?, city?, postalCode? }` (`helper.service.ts:43-62`), o 204 si no hay detalle.
- Contenedor: `API:services/checkinbiz/src/interfaces/http/geo/geo.router.ts:23-54`, con Firebase Auth (`API:services/checkinbiz/src/app.ts:48`).
- El formulario guarda `address = { street: resolvedText, geo: { lat, lng }, timeZone, country, postalCode }` (`AddressComplexInput.tsx:141-148`).

**Alta.** `PANEL:app/main/[entityId]/checkinbiz/branch/form/form.controller.tsx:164-241` → `POST /api/proxy/checkinbiz_create_sucursal` (`PANEL:services/checkinbiz/sucursal.service.ts:42-66`) → `POST http://141.95.47.135:8080/api/v1/branches` (`.env.development:66`; nginx `:78`).
- Cuerpo (`form.controller.tsx:167-185`):
```
{ name, ratioChecklog /* 201 por defecto (:63) */, disableRatioChecklog: !<toggle>,
  status: "active", nif: "N/A", metadata: {…}, id: undefined,
  address: { street, geo: {lat,lng}, timeZone, country, postalCode },
  entityId,
  advance: { enableDayTimeRange, disableBreak, timeBreak /* 60 */, notifyBeforeMinutes /* 15 */ } }
```
- **Observado:** el formulario envía el valor contrario al del interruptor (`:170`) y ese interruptor empieza en `false` (`:64`). Con los valores por defecto se envía **`disableRatioChecklog: true`**, es decir, la geocerca desactivada. Qué dice la etiqueta `core.label.disableRatioChecklogE` está sin confirmar.

**Horario propio de la sucursal.** Si se tocó el calendario del formulario, después se llama al calendario con `{ scope: "branch", entityId, branchId: resp.id, overridesSchedule, advance, timezone: address.timeZone ?? <tz de la entidad> ?? "UTC", overridesDisabled }` (`:218-240`).

**Contenedor `branches`.** La función `create` está en `API:services/branches/src/interfaces/http/branch.router.ts:68-101`; su registro de ruta está más abajo en ese fichero y no se ha leído.
- Validación (`API:services/branches/src/interfaces/http/branch.validation.ts:95-174`): `name`, `entityId`, `address.street`, `address.country` y `address.timeZone` no vacíos, `geo.lat`/`geo.lng` numéricos y dentro de rango, `ratioChecklog > 0` (200 si no viene), `status` en `archived | active`.
- `canCreateBranch` responde 403 `subscription/limit_off` cuando se supera el cupo (`branch.router.ts:74-79`); el panel lo muestra con un modal (`form.controller.tsx:258-264`).
- Responde 201 con la sucursal completa, `id` incluido (`:100`).

**Precondiciones:** suscripción (REC-03). La sucursal automática de REC-03 puede existir ya; el onboarding toma la más antigua como principal (`onboardingState.service.ts:54,111-113`). Con el cupo del plan gratuito, una segunda sucursal podría dar 403 (valores del plan sin confirmar).

---

## REC-06 · Alta de empleado

**Quién.** `PANEL:app/main/[entityId]/checkinbiz/employee/form/form.controller.tsx:173-277` → `POST /api/proxy/checkinbiz_create_employee` (`PANEL:services/checkinbiz/employee.service.ts:182-206`) → `POST http://141.95.47.135:8080/api/v1/employees` (`.env.development:56`; nginx `:77`).

**Cuerpo** (`form.controller.tsx:199-213`, tras quitar los campos de calendario en `:179-197`):
```
{ fullName, email, phone, role: "internal" | "collaborator", status: "active", nationalId: "N/A",
  enableA2F /* el panel lo envía a false por defecto (:91) */, biometricRequired /* true */,
  enableRemoteWork /* false; si es false no se envía address */,
  uid: <id del ADMIN> /* el contenedor lo ignora */, metadata: {…}, id: undefined, entityId }
```

**Contenedor `employees`** (`API:services/employees/src/interfaces/http/employee.router.ts:163-219`, ruta en `:350`):
- **Validación** (`:103-143`): exige `fullName`, `role` y `entityId`. Rellena valores por defecto: `status` siempre `"active"`, `enableA2F ?? true`, `biometricRequired ?? true`, `phone ?? "-"`, `branchId`, `jobTitle` y `nationalId` a `null`.
- **Errores:** 403 si no pasa `canWrite` (`:173`); 403 `subscription/limit_off` (`:184-189`); 400 con `error` = JSON anidado con `code: employee/exist_employee` si ya existe (`:193-204`).
- **Si el cuerpo trae `id`**, no crea a nadie: solo reenvía las credenciales (`:175-180`).
- **Acceso** (`createEmployee` en `API:packages/shared/src/checkbiz/employees/manageEmployee.ts:39-101`):
  - Usuario de Auth creado con el Admin SDK: `createUser({ email, emailVerified: false })`, o reutilizado si el correo ya existe (`…/employeeAccess.ts:22-40`).
  - Ficha `entities/{eid}/employees/{id}` escrita **con** `uid` (`manageEmployee.ts:65`) e indexada en `searchIndex` (`:72-74`).
- **Correo de bienvenida** (`sendWelcomeEmail`, `employeeAccess.ts:49-92`):
  - Fija una **contraseña aleatoria de 6 dígitos** con `updateUser` (`:61-62`).
  - Genera un enlace de restablecimiento de contraseña (`:63`).
  - `customToken = base64(JSON { employeeId, entityId, fullName })` (`:64-66`).
  - Plantilla `WELLCOME_EMPLOYEE` con `{ displayName, companyName, customToken, recoveryPass, email, newPass, androidUrl, iosUrl }` (`:68-86`), enviada por SMTP. Las plantillas viven en Firestore `emails_template` (`API:packages/shared/src/notifications/EmailService.ts:2-10,141-189,201`).
  - **La contraseña no se guarda en ningún sitio**: solo viaja en el correo.
- El disparador `onCreateEmployee` de Functions se aparta porque la ficha nace con `uid`, así que no hay segunda bienvenida (`FN:services-saas/checkinbiz/interfaces/triggers/onCreateEmployee.controller.ts:29`).
- Responde 201 `{ message, code: "employee/created", employee }` (`employee.router.ts:212-215`).

**Después, en el panel.** Usa `response.employee.id` (`form.controller.tsx:241,276`). Si el calendario quedó modificado, llama al calendario con `{ scope: "employee", entityId, employeeId, overridesSchedule, advance, holidays, timezone, overridesDisabled }` (`:246-262`). Si con los valores sin tocar el calendario cuenta como modificado está sin confirmar.

**El token del correo.** La app **no lo usa**: no hay manejo de enlaces profundos (búsqueda de `app_links`, `uni_links` y `getInitialLink` sin resultados). El `validate` que llama la app recibe otro token equivalente, `tokenValidateEmployee` (REC-08). `POST /api/v1/employees/validate` (`…/employeePublic.router.ts:13-33`) lo usa la herramienta web `/tools/checking` del panel (`employee.service.ts:358-379`), no la app.

**Precondiciones:** suscripción (REC-03). Para que el empleado pase por el segundo factor en REC-09, hay que enviar **`enableA2F: true`**.

---

## REC-07 · Asignación de responsabilidad (sucursal, nivel, puesto y precio)

**Quién.** Hay dos puntos de entrada en el panel, con el mismo cuerpo:
- Desde el empleado: `PANEL:app/main/[entityId]/checkinbiz/employee/[id]/detail/FormLink/FormLink.controller.tsx:72-111`. Antes comprueba en Firestore que no exista ya (`:76`).
- Desde la sucursal: `PANEL:app/main/[entityId]/checkinbiz/branch/[id]/detail/components/FormLink.controller.tsx:57-82`.

**Llamada.** `POST /api/proxy/checkinbiz_responsability_handler` (`employee.service.ts:234-258`) → `POST http://141.95.47.135:8080/api/v1/employees/responsibilities` (`.env.development:62`).

**Cuerpo** (`FormLink.controller.tsx:83-101`, lado empleado):
```
{ id: `${branchId}_${entityId}_${employeeId}`, employeeId,
  responsibility: "owner" | "manager" | "supervisor" | "worker",
  scope: { entityId, branchId, scope: "branch" },
  job: { job, price }, metadata: {…}, assignedBy: <uid>, active: 1, entityId,
  workSchedule, workScheduleEnable }
```
Después **escribe directamente en Firestore** `entities/{eid}/jobs` (`addJobs`, `employee.service.ts:126-159`; `FormLink.controller.tsx:106-107`).

**Contenedor** (`API:services/employees/src/interfaces/http/responsibility.router.ts:51-118`; montado antes que la plantilla en `API:services/employees/src/app.ts:27`):
- Exige `employeeId`, `responsibility` válida, `scope.entityId`, `job.job` y **`job.price` numérico** (`:55-66`). Si el formulario lo envía como número o como cadena está sin confirmar.
- `canWrite` (`:80-85`). El empleado y la sucursal tienen que existir (`:87-90`), así que en la práctica `scope.branchId` es obligatorio.
- Calcula `level` (`:97`) y toma `assignedBy` del token, no del cuerpo (`:102`).
- Ignora `id`, `workSchedule` y `workScheduleEnable` (`:94-106`).
- El repositorio escribe con id `${employeeId}_${entityId}_${branchId}` —el orden del panel es otro, pero da igual porque se ignora— y añade `branchId` al array de la ficha del empleado (`API:packages/shared/src/checkbiz/repositories/FirestoreEmployeeRepository.ts:46-57`).
- Envía una notificación push `assign_created` (`:110-115`) y responde 201 `{ success: true, data }`.

**Horario propio del empleado:** no va aquí, sino en el calendario de `scope: "employee"` (REC-06).
**Por qué importa:** `validate` devuelve las sucursales a partir de las responsabilidades (REC-08), y el fichaje responde 404 `employee/not_resposibility` si el empleado no tiene responsabilidad en esa sucursal (`createChecklog.controller.ts:147-161`).

---

## REC-08 · App, primer arranque: validación e inicio de sesión

**Arranque.** `initializeAuthFlow` (`APP:presentation/pages/splash_page.dart:65-78`; `APP:features/auth/presentation/providers/auth_provider.dart:366-412`). Sin sesión, va al login (`splash_page.dart:175-176`). El token del correo no interviene.

**8a. Firebase Auth.** `signInWithEmailAndPassword(email en minúsculas, contraseña de 6 dígitos del correo)` y después `getIdToken` (`auth_provider.dart:890-924`), con el SDK y el proyecto de `firebase_options_dev.dart` (no leído).

**8b. Login.** `POST http://141.95.47.135:8080/api/v1/checkinbiz/auth/login` (`app_constants.dart:44,50`), sin cuerpo.
- Cabeceras: `Authorization: Bearer <ID token de Firebase>`, `User-Agent: <deviceId>` (`APP:features/auth/data/datasources/auth_remote_datasource.dart:34-44`).
- Contenedor (`auth.router.ts:67-71`; `API:services/checkinbiz/src/interfaces/http/auth/loginEmployee.controller.ts:10-50`):
  - Busca fichas por `uid`. Si no hay ninguna, responde 204 y la app lanza `NoEmployeeAccessException` (`auth_remote_datasource.dart:46-52`).
  - Fija la claim `employee: true` (`:21-24`).
  - Responde `[{ employeeId, uid, email, entity: { entityId, name }, fullName, tokenValidateEmployee: base64(JSON { employeeId, entityId }) }]` (`:26-45`).
- Si hay más de una empresa, la app pide elegir (`auth_provider.dart:616-630`).

**8c. Validación.** `POST http://141.95.47.135:8080/api/v1/checkinbiz/auth/validate`, sin `Authorization`, con cuerpo `{ token: tokenValidateEmployee }` (`auth_remote_datasource.dart:77-94`).
- Contenedor, ruta pública (`API:services/checkinbiz/src/app.ts:29`; `…/auth/validateEmployee.controller.ts:7-87`):
  - Decodifica el base64 y busca la ficha.
  - `sessionToken = jwt.sign({ employeeId, entityId }, JWT_2FA_SECRET)`, **sin caducidad** (`:59-63`).
  - Responde `{ message, payload: { name, twoFa, entityId, employeeId, biometricRequired }, sessionToken, expiresAt: null, branchId: [<ids de sucursal de sus responsabilidades activas>] }` (`:64-78`).
  - `twoFa` vale `true` si el empleado tiene `enableA2F === false`; si no, vale `!!twoFA.verifiedAt` (`:64,69`).
- El modelo de la app exige `branchId` (`APP:features/auth/data/models/auth_models.dart:126-152`). `payload.trustedDevicesId` no llega nunca, así que `isTrustedDevice` queda en `false` (`auth_provider.dart:730`).
- Si `validate` falla, la app repite login + validate una vez (`:660-687`).

**Qué guarda la app** (`auth_provider.dart:689-735`):
- En preferencias: `access_token` (el ID token de Firebase), `token_validate_employee`, `session_token` y `selected_entity_id` (`:694-699`), y opcionalmente las credenciales cifradas (`:701-704`).
- Lee la ficha del empleado y la entidad directamente de Firestore (`:689-692`, `:706`, `:542-549`).
- **Escribe directamente** `entities/{eid}/employees/{id}` = `{ language, updated_at }` (`:709-718`; `APP:data/datasources/firestore/employee_firestore_datasource.dart:26-41`).
- Arranca FCM, que escribe en `notification_tokens/{employeeId}/devices/{deviceId}` (`:737-754`; `APP:features/notifications/data/datasources/notification_token_firestore_datasource.dart:11-12,30-32`; detalle sin confirmar).
- Las sucursales se leen de Firestore: `entities/{eid}/branches` con `status == "active"`, cruzadas con `branchIds` (`APP:features/attendance/data/datasources/branch_firestore_datasource.dart:107-130`).

**Siguiente paso.** Si `!hasTwoFA`, la app va a la pantalla de seguridad (`APP:features/auth/presentation/pages/login_page.dart:247-249`).
**Precondiciones:** REC-06 y REC-07, y conocer la contraseña.

---

## REC-09 · App: segundo factor y dispositivo de confianza

**Solo ocurre si el empleado tiene `enableA2F: true`.** Con los valores por defecto del panel, `twoFa` llega a `true` y este paso no ocurre; tampoco se exige dispositivo de confianza al fichar (`createChecklog.controller.ts:174`).

**9a. Activación.** Al abrir la pantalla (`APP:features/auth/presentation/pages/configure_security_page.dart:46-68`) se llama a `enable2FA` (`auth_provider.dart:1117-1148`).
- `POST http://141.95.47.135:8080/api/v1/checkinbiz/auth/2fa/enable` (`app_constants.dart:61`).
- Cabeceras: `Authorization: Bearer <sessionToken>`, `User-Agent`. Cuerpo: `{ employeeId, entityId }` (`auth_remote_datasource.dart:97-117`).
- El contenedor valida el JWT con `JWT_2FA_SECRET` y **sobrescribe el cuerpo con el contenido del token** (`auth.router.ts:43-59`; `API:packages/shared/src/checkbiz/auth/validateTokenStaff.ts:29-50`).
- Guarda `twoFA` = `{ secret, verifiedAt: null }` (`…/Generate2FASecret.ts:13-26`) y responde `{ otpauthUrl, secret, qrImage }`, o 204 si la ficha no existe (`…/enable2FA.controller.ts:16-47`).

**9b. Verificación.** Código de 6 dígitos (`configure_security_page.dart:125-143`) → `verify2FA` (`auth_provider.dart:1151-1195`).
- `POST …/auth/2fa/verify` con cuerpo `{ code, employeeId, entityId }` y las mismas cabeceras (`auth_remote_datasource.dart:120-145`).
- El contenedor (`…/verify2FA.controller.ts:16-46`):
  - Toma **`deviceId = base64(User-Agent)`** (`:31-34`).
  - Comprueba el TOTP (`…/Verify2FACode.ts:14-28`).
  - **Da de alta el dispositivo**: añade ese valor a `trustedDevicesId.ids` (`…/UpdateDevicesEmployee.ts:20-31`).
  - Responde 200 `{ message, expiresIn: 300 }`.
- Con un código malo, responde **401 `{ error: "<JSON con message y code twofactor/invalid_code>" }`**: el código va dentro de la cadena, no en `code`. Como es un 401, el interceptor de la app reintenta con el ID token de Firebase (que el JWT rechaza) y después rehace la sesión (`auth_retry_interceptor.dart:57-93`).

**9c. `addDeviceEmployee`.** Existe en el datasource (`auth_remote_datasource.dart:148-169`; `app_constants.dart:70-72`, que en desarrollo apunta a una Cloud Function), pero **nadie lo llama** (búsqueda sin más resultados). De todos modos, esa Function exige `purpose: "2fa-authorization"` en el JWT (`FN:core/shared/utils/validate2FAToken.ts:17-19`), y el `sessionToken` no lo lleva.

**Qué identifica al dispositivo:** solo la cabecera `User-Agent`, que contiene el `deviceId` persistente de la app. El servidor guarda `base64` de ese valor. No hay otra cabecera de dispositivo.

**Antes de cada fichaje.** Si el móvil no tiene biometría y el empleado tiene el segundo factor, la app pide otro código y vuelve a llamar a `verify` (`APP:features/attendance/presentation/pages/attendance_page.dart:505-533`; `APP:presentation/widgets/dialogs/verify_2fa_dialog.dart:56-60`).

---

## REC-10 · App: calendario efectivo

**Quién.** `todayScheduleProvider` (`APP:features/attendance/presentation/providers/schedule_provider.dart:47-64`) → `getResolvedSchedule` (`APP:features/attendance/data/repositories/attendance_repository_impl.dart:56-78`).

**Llamada.** `GET http://141.95.47.135:8080/api/v1/checkinbiz/calendar?entityId=…&employeeId=…&branchId=…&scope=employee&dateLocal=YYYY-MM-DD` (`APP:features/attendance/data/datasources/attendance_remote_datasource.dart:66-90`; `app_constants.dart:82`).
- Cabecera `Authorization: Bearer <ID token de Firebase>`: el parámetro se llama `sessionToken` pero lo que se lee de preferencias es `access_token` (`attendance_repository_impl.dart:62-74`). También va `User-Agent`.

**Contenedor.** `requireFirebaseAuth` (`API:services/checkinbiz/src/app.ts:46`) → `…/getEffectiveCalendar.controller.ts:9-52`.
- 404 `calendar/not_found` sin calendario de entidad; 400 `calendar/missing_timezone` sin zona horaria (`resolveEffectiveCalendar.usecase.ts:55-62`).
- Responde `{ code, data: { timezone, weeklySchedule, advance, holidays, overridesDisabled, overridesDisabledByScope, sources, ids }, effectiveDay }` (`:88-107`; controlador `:36-51`).
- **Observado:** no hay comprobación de pertenencia a la empresa en el controlador.

**Qué usa la app.** Fusiona `data` con `effectiveDay` (`attendance_remote_datasource.dart:91-99`) y lee `timezone`, `dateLocal`, `day`, `weeklySchedule`, `holidays`, `advance`, `sources`, `isHoliday` e `isWorkingDay` (`APP:features/attendance/data/models/schedule_model.dart:138-167`). De qué nivel toma `dateLocal` y `day` está sin confirmar (el resto de `fromJson` no se ha leído).

---

## REC-11 · App: fichaje (entrada, inicio y fin de descanso, salida)

**Quién.** `attendance_page.dart:630-654` → `registerAttendance` (`APP:features/attendance/presentation/providers/attendance_provider.dart:266-412`).
- Primero se decide la seguridad: con `biometricRequired` (por defecto `true`) exige biometría del móvil; sin hardware y con segundo factor, pide el código (`attendance_page.dart:476-534`).
- La ubicación sale de caché reciente, de un fijo nuevo o de un respaldo, con `source` = `fresh | last_known | fallback | cached_warmup` (`attendance_provider.dart:296-325`, `:114`, `:314`, `:460`).

**Llamada.** `POST http://141.95.47.135:8080/api/v1/checkinbiz/checklogs` (`app_constants.dart:77`).
- Cabeceras: `Authorization: Bearer <sessionToken JWT>`, `User-Agent: <deviceId>`, `Content-Type: application/json` (`attendance_remote_datasource.dart:28-45`).
- Cuerpo (`attendance_provider.dart:328-346`; `auth_models.dart:53-103`):
```
{ branchId, type: "checkin" | "restin" | "restout" | "checkout",
  geo: { lat, lng, accuracy, capturedAt, source },
  biometric?: { method: "biometric", verifiedAt, deviceId },
  metadata?: { canValidateSecurity: false } }
```
- No lleva `entityId` ni `employeeId`: el router los toma del JWT y los mezcla en el cuerpo (`API:services/checkinbiz/src/interfaces/http/checklog/checklog.router.ts:22-45`).
- **Observado:** el contenedor no lee `biometric` ni `metadata`, ni `accuracy`, `capturedAt` o `source`; solo usa `lat` y `lng` (`createChecklog.controller.ts:26-73`).

**Respuestas del contenedor, en el orden en que se comprueban** (`createChecklog.controller.ts:120-547`):

| Estado | `code` | Motivo |
|---|---|---|
| 401 | `auth/unauthorized` | JWT inválido (`validateTokenStaff.ts:29-50`) |
| 400 | `checklog/bad_request` | Payload inválido (`:122-130`) |
| 404 | `employee/not_found` | `:149-154` |
| 404 | `employee/not_resposibility` | Sin responsabilidad en esa sucursal (`:156-161`) |
| 401 | `auth/untrusted_device` | `enableA2F !== false` y `base64(UA)` no está en `trustedDevicesId` (`:170-180`) |
| 400 | `employee/branchId_required` | `:182-187` |
| 404 / 400 | `branch/not_found`, `branch/inactive` | `:189-201` |
| 400 | `calendar/not_resolved` | Solo si hay configuración y aun así no se resuelve (`:214-221`) |
| 400 | `checklog/day_disabled` | Día desactivado, sin turnos o festivo (`:278-294`) |
| 400 | `checklog/out_of_schedule` | Entrada fuera de [inicio − `notifyBeforeMinutes` (15 por defecto), fin] (`:296-347`); también con rango estricto (`:462-469`) |
| 400 | `checklog/out_of_radius` | `details: { distanceMeters, allowedRadiusMeters, branchId }`; **deja guardado un fichaje `failed`**. No aplica si la sucursal tiene la geocerca desactivada o el empleado trabaja en remoto (`:490-512`) |
| 400 | secuencia | `{ message, code }`: `two_type_followed`, `invalid_checkin`, `invalid_checkout`, `different_branches`, `invalid_restin`, `invalid_restout`, `unknown_type`, `invalid` (`API:services/checkinbiz/src/application/use-cases/checklog/CreateChecklog.ts:19-66`) |
| 201 | `checklog/created` | `{ message: "Checklog created", code, checkLog }` (`:536-540`) |
| 500 | `checklog/internal_error` | `:541-546` |

**Secuencia válida:** `checkin` (sin fichaje previo o tras un `checkout`) → `restin` → `restout` → `checkout`, en la misma sucursal (`CreateChecklog.ts:25-55`). Una salida con menos de 3 h o más de 10 h de jornada se marca `isSuspect: true`; no es un error (`:69-78`).

**Qué hace la app con cada error** (`APP:core/errors/error_parser.dart:7-35,44-230`; `attendance_provider.dart:357-402`):
- `auth/unauthorized` y `twofactor/invalid_token`: rehace la sesión (login + validate) y reintenta una vez con el `sessionToken` nuevo (`:359-375`; `auth_provider.dart:308-364`).
- `auth/untrusted_device`: lanza `UntrustedDeviceException` a la interfaz (`:381-384`). Como es un 401, el interceptor además repite la petición con el ID token de Firebase antes de que llegue ahí.
- `checklog/two_type_followed` y `checklog/out_of_schedule`: excepciones propias que suben a la interfaz (`:394-399`).
- `out_of_radius`, `day_disabled` y el resto: caen en el `catch` genérico, que devuelve `false` con el error en el estado (`:400-402`). Cómo llega a abrirse `out_of_range_dialog` no se ha leído.
- **Observado:** el parser espera `checklog/invalid_checki` (`error_parser.dart:91`) pero el contenedor envía `checklog/invalid_checkin`. `different_branches`, `not_resposibility`, `branch/inactive` y `calendar/not_resolved` no aparecen en el tramo leído; qué hace la rama por defecto está sin confirmar.

---

## Atajos que necesita una prueba automática

1. **Turnstile (REC-01).** En desarrollo no se comprueba (`verifyTurnstileToken.ts:49`): vale cualquier `cf-turnstile-response`. Si la prueba no ejecuta el panel, reproduce la ruta `/api/auth/register` tal cual: Admin SDK `createUser`, canje `signInWithCustomToken` por REST con la API key web de dev y `POST /api/v1/users` con el ID token. Es exactamente lo que hace el servidor de Next.

2. **Contraseña del propietario.** La genera la propia prueba.

3. **Sesiones de Firebase.** El custom token se canjea por REST (`accounts:signInWithCustomToken`) y la contraseña del empleado por `accounts:signInWithPassword`. Los refrescos van por `securetoken` con el refresh token. Es lo mismo que hace el SDK.

4. **TOTP del panel y del empleado.** El código se calcula a partir del `secret` en base32 que devuelven `…/2fa/user/enable` y `…/2fa/enable`. Los parámetros de `TwoFactorVerificationService` (algoritmo, paso, dígitos) no se han leído; lo esperable es TOTP estándar de 6 dígitos cada 30 s, sin confirmar. Tras el `verify` del panel hay que refrescar el ID token para que traiga `admin` y `twoFA`, aunque ningún contenedor las mira.

5. **Cookie `2fa_session`.** Solo hace falta si la prueba pasa por el proxy del panel: se obtiene con `POST /api/auth/2fa-session { idToken }`. Llamando directo al contenedor no se necesita, pero entonces no se prueba el guardián del panel (ver la observación del principio).

6. **Buscador de direcciones.** Se puede usar una consulta fija y la primera sugerencia (autocompletar + detalle; consume Places, y la clave de desarrollo está sin confirmar). O saltarlo y enviar `address` con `street`, `country`, `postalCode`, `geo` fijos y un `timeZone` IANA: el contenedor solo valida la forma. Para que salga la sucursal automática, la dirección de la entidad tiene que traer `geo` y `timeZone`.

7. **Pago y `stripeCustomerId`.** Primero hay que llamar a `POST /api/v1/billing/portal { entityId }`, como hace la pestaña de facturación, y después suscribir. En `freemium` el portal no requiere que nadie meta una tarjeta. En un plan de pago, la tarjeta solo puede adjuntarse con la API de Stripe en modo de prueba, lo que ya no es lo que hace un humano en el panel, y depende de que el webhook llegue a `billing` de desarrollo (sin confirmar).

8. **Sucursal automática.** La crea una Cloud Function de forma asíncrona: la prueba tiene que sondear `entities/{eid}/branches` con el Admin SDK hasta que aparezca, o crear la sucursal por REC-05.

9. **Contraseña temporal del empleado.** Solo viaja en el correo. Sin buzón, la alternativa es fijar una conocida con el Admin SDK (`updateUser(uid, { password })`), el mismo mecanismo que usa el contenedor. Es una desviación: sustituye a la del correo. Otra opción es entrar con un custom token del `uid`, pero eso se salta el paso de la contraseña.

10. **Dispositivo.** Un `User-Agent` fijo (por ejemplo, un UUID) usado igual en `verify` y en todos los fichajes. El servidor lo guarda en base64. No hace falta escribir en `trustedDevicesId`.

11. **Biometría.** El contenedor no la mira. Se envía `biometric: { method: "biometric", verifiedAt, deviceId }` como haría la app en un móvil con biometría, o se crea el empleado con `biometricRequired: false` y se envía `metadata: { canValidateSecurity: false }`.

12. **GPS y permisos.** Coordenadas fijas iguales a las de la sucursal (distancia 0). Los permisos del móvil no intervienen a nivel de API.

13. **Reloj.** La entrada tiene que caer en un turno del día efectivo en la zona horaria de la sucursal. Conviene configurar en REC-04 un turno que cubra el momento de la prueba, por ejemplo 00:00–23:59 todos los días. La salida a los pocos minutos quedará `isSuspect: true`.

14. **Correos reales.** El alta envía de verdad las bienvenidas del propietario y del empleado por SES. Hay que usar direcciones de un dominio propio: los rebotes perjudican al remitente (`onCreateEmployee.controller.ts:31-44`).

## Pasos que hoy no se pueden automatizar sin cambiar algo

1. **Leer la contraseña del empleado tal y como la recibe.** Se genera, se fija en Auth y solo viaja en el correo; ni Firestore ni `EmailService` la guardan (`employeeAccess.ts:61-86`). Para hacerlo con fidelidad hace falta un buzón de pruebas legible por la prueba (el código no tiene ninguno) o un cambio que la exponga en desarrollo. Sin eso, la prueba tiene que sobrescribirla (atajo 9).

2. **Dar de alta una tarjeta como lo hace un cliente** (planes de pago). Ocurre en el portal alojado por Stripe. Solo el plan `freemium` evita ese paso, y depende de que ese plan exista en `dev-encodebiz` (sin confirmar).

3. **Hacer «la misma llamada» del alta y del segundo factor del panel sin ejecutar el panel.** `/api/auth/register`, `/api/auth/2fa-session` y el guardián de la cookie son rutas y middleware de Next, no del contenedor. Una prueba que solo hable con `141.95.47.135:8080` los reproduce, pero no los ejercita. Para ejercitarlos necesita un panel en marcha: local con `.env.development` o el despliegue de desarrollo en Vercel, cuyas variables pueden diferir.

No bloquean nada, pero conviene saberlo: la biometría real del móvil no es automatizable y el contenedor tampoco la valida; el token del correo de bienvenida no lo consume la app; y `addDeviceEmployee` no se llama.

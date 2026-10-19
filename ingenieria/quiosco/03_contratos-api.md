# 03 — Contratos de API del quiosco (implementación, rama `feat/quiosco`)

**Fecha:** 2026-10-18 · **Estado:** contrato de la implementación en curso. Manda sobre el
resumen de contratos del [README](./README.md) donde difieran; las diferencias están al final.

Base: `https://api.checkbiz360.com/api/v1/checkinbiz` (dev: la del entorno). Todas las
respuestas de error son `{ error, code, details? }` como el resto de `checkinbiz`.

---

## Credenciales

| Quién | Credencial | Dónde se usa |
|---|---|---|
| Tablet (usuario de quiosco) **para abrir sesión** | ID token de Firebase del usuario de quiosco (claim `kind: "kiosk"`) | `POST /auth/kiosk/session` |
| Tablet **ya en modo quiosco** | `kioskToken` (JWT propio, `kind: "kiosk"`) en `Authorization: Bearer` | `/kiosk/*` |
| Empleado en su móvil | `sessionToken` de siempre (el de `/auth/validate`) | `GET /kiosk/me/qr` |
| Panel | ID token de Firebase del administrador, `canWrite` sobre `entityId` | `/kiosks/*` |

El usuario de quiosco es una cuenta de Firebase Auth normal (correo y contraseña). La app hace
el `signInWithEmailAndPassword` de siempre, lee los claims del ID token
(`getIdTokenResult().claims`) y, si `kind == "kiosk"`, **no llama a `/auth/login`** sino a
`/auth/kiosk/session`. El login de empleados no cambia.

---

## Tablet

### `POST /auth/kiosk/session` — abrir el quiosco en este dispositivo

```json
{ "deviceId": "…", "device": { "model": "SM-X200", "os": "android", "osVersion": "14", "appVersion": "1.9.0+65" },
  "geo": { "lat": 41.39, "lng": 2.11, "accuracy": 18 } }
```

`200`:

```json
{ "kind": "kiosk", "kioskToken": "…", "expiresAt": "2027-10-18T…Z",
  "entity": { "id": "…", "name": "Serlimar" },
  "branch": { "id": "…", "name": "Edificio Colonial", "timeZone": "Europe/Madrid", "geo": { "lat": 41.39, "lng": 2.11 } },
  "activationRadiusMeters": 200, "maxAccuracyMeters": 100,
  "settings": { "photo": true, "methods": ["qr", "code"] },
  "replacedPrevious": false }
```

Abrir sesión **sustituye** al dispositivo anterior (`replacedPrevious: true`); el anterior
recibe `401 kiosk/replaced` en su siguiente llamada.

| HTTP | `code` | Cuándo | `details` |
|---|---|---|---|
| 401 | `unauthenticated` | sin ID token o caducado | |
| 403 | `kiosk/not_kiosk_user` | el usuario no es de quiosco | |
| 401 | `kiosk/disabled` | el módulo está desactivado en la empresa o el quiosco deshabilitado | |
| 409 | `kiosk/no_branch_geo` | la sucursal no tiene dirección geolocalizada | |
| 400 | `kiosk/device_not_eligible` | el dispositivo no cumple | `{ reason, accuracyMeters?, maxAccuracyMeters? }` |
| 403 | `kiosk/out_of_radius` | lejos de la sucursal | `{ distanceMeters, allowedRadiusMeters, branchName }` |

`reason` ∈ `location_missing` (no vino `geo`) · `low_accuracy` (`accuracy` > `maxAccuracyMeters`,
100 m) · `os_unsupported` (Android < 10 o iOS < 15). La app comprueba antes, en el dispositivo,
`location_off`, `location_denied`, `low_accuracy` y `no_front_camera`, y no llama si falla: esos
motivos también son válidos para enseñar con el mismo texto.

### `POST /kiosk/heartbeat` — al arrancar la app y cada 24 h

`{ "deviceId": "…", "geo": { "lat", "lng", "accuracy" } }` → `200 { "status": "active" }` o
`200 { "status": "suspended", "reason": "out_of_radius" | "low_accuracy", "details": {…} }`.
Suspendido, la tablet bloquea el teclado con el motivo y vuelve a llamar cada 5 minutos; al
cumplir, `active` otra vez.

### `POST /kiosk/identify` — QR o código

`{ "deviceId": "…", "qr": "CB360K1.…" }` **o** `{ "deviceId": "…", "code": "482913" }` →

```json
{ "sessionId": "…", "expiresAt": "…(60 s)",
  "employee": { "id": "…", "firstName": "Marta" },
  "suggested": "checkin", "allowed": ["checkin"] }
```

`allowed` sale del último fichaje válido: sin jornada abierta → `["checkin"]`; trabajando →
`["checkout", "restin"]`; en pausa → `["restout"]`. `suggested` es el primero.

| HTTP | `code` | Cuándo |
|---|---|---|
| 404 | `kiosk/code_not_found` | QR o código que no existe en esta empresa (o QR revocado) |
| 403 | `kiosk/employee_not_in_branch` | la persona no tiene responsabilidad en esta sucursal |
| 429 | `kiosk/too_many_attempts` | 5 fallos en 60 s; `details.retryAfterSeconds` |
| 423 | `kiosk/suspended` | el quiosco está suspendido (radio/precisión) |

### `POST /kiosk/checklogs` — fichar

```json
{ "deviceId": "…", "sessionId": "…", "type": "checkin",
  "geo": { "lat", "lng", "accuracy" },
  "photo": { "contentType": "image/jpeg", "data": "<base64 sin prefijo data:>" } }
```

Foto: JPEG, ≤ 400 KB decodificada (la app la manda a 640 px de lado mayor, calidad 70, ~60 KB).

`201 { "code": "checklog/created", "checkLog": { "id", "type", "timestamp" }, "employee": { "firstName" } }`.

Errores propios: `400 kiosk/photo_required`, `400 kiosk/photo_invalid`, `410 kiosk/session_expired`,
`400 kiosk/type_not_allowed`, `502 kiosk/photo_upload_failed`, `423 kiosk/suspended`. Y **todos
los del fichaje de siempre** (`checklog/out_of_schedule`, `checklog/day_disabled`,
`checklog/two_type_followed`, `checklog/absence`, `checklog/invalid_*`, `checklog/different_branches`,
`employee/not_resposibility`, `branch/inactive`…), con su `code`: la app los traduce con las claves
que ya tiene para el fichaje.

### `POST /kiosk/unlock` — salir del modo quiosco en la tablet

`{ "deviceId": "…", "pin": "123456" }` → `200 { "ok": true }` y la sesión del dispositivo queda
cerrada (la app borra el token y vuelve al login). `403 kiosk/unlock_invalid`, `429 kiosk/too_many_attempts`.
El PIN es del quiosco (6 dígitos), se ve en el panel junto a las credenciales.

### Errores de sesión en cualquier `/kiosk/*`

| HTTP | `code` | Qué hace la app |
|---|---|---|
| 401 | `kiosk/unauthorized` | token ausente, mal firmado o caducado → login |
| 401 | `kiosk/replaced` | otro dispositivo abrió el quiosco → login con «Este quiosco se ha activado en otro dispositivo» |
| 401 | `kiosk/revoked` | sesión cerrada desde el panel o credenciales regeneradas → login |
| 401 | `kiosk/disabled` | módulo desactivado → login |

## Empleado (su móvil)

### `GET /kiosk/me/qr` — «Mi QR»

`Authorization: Bearer <sessionToken>` → `200 { "qr": "CB360K1.…", "branchIds": ["…"] }`;
`404 kiosk/not_enabled` si la empresa no tiene el módulo activo (la app oculta la entrada).

## Panel (ID token, `canWrite`)

**Add-on de pago, como el inventario** (2026-10-19): sin la suscripción `kiosk` activa o en
prueba, todas las rutas salvo `GET /kiosks` responden **403 `kiosk/not_subscribed`**, y las de
la tablet **401 `kiosk/not_subscribed`** (la tablet cierra la sesión). No hay activar ni
desactivar: contratar y dar de baja se hacen en `billing`, con el servicio `kiosk` y el plan
`standard` (`alta-servicio-quiosco`; sin precio de Stripe no es contratable).

| Ruta | Cuerpo / query | Responde |
|---|---|---|
| `GET /kiosks?entityId` | | `{ subscribed, subscriptionStatus, settings: { photo, photoRetention }, kiosks: [Kiosk & { credentialsIssued }], skipped: [{ branchId, branchName, reason: "no_branch_geo" }] }` — lo único que responde sin el add-on; con él, crea los quioscos que faltan |
| `POST /kiosks/:branchId/credentials` | `{ entityId }` | `Credentials`: las primeras o unas nuevas; cierra la sesión del dispositivo |
| `DELETE /kiosks/:branchId/device?entityId` | | `{ ok: true }` |
| `PATCH /kiosks/:branchId` | `{ entityId, activationRadiusMeters }` (50-500) | `Kiosk` |
| `GET /kiosks/:branchId/cards?entityId` | | `{ cards: [{ employeeId, fullName, qr }] }` — el panel pinta las tarjetas |
| `POST /kiosks/:branchId/codes` | `{ entityId, regenerate?: false }` | `{ codes: [{ employeeId, fullName, code }] }` — **una sola vez**; por lotes de 200 escrituras; sin `regenerate` sólo a quien no tiene |
| `POST /kiosks/employees/:employeeId/qr` | `{ entityId }` | `{ qr }` — revoca el anterior |
| `POST /kiosks/employees/:employeeId/code` | `{ entityId }` | `{ code }` — **una sola vez** |
| `GET /kiosks/:branchId/review?entityId&date=YYYY-MM-DD` | | `{ items: [ReviewItem], bursts: [{ startedAt, count, checklogIds }] }` |
| `POST /kiosks/review/:checklogId/reject` | `{ entityId, reason? }` | `{ ok: true }` — fichaje a `failed`, `rejectionReason: "kiosk_identity"`, QR y código de esa persona revocados |

```ts
type Kiosk = {
  branchId: string; branchName: string; email: string;
  status: "active" | "suspended" | "disabled"; suspendedReason?: "out_of_radius" | "low_accuracy";
  activationRadiusMeters: number; hasBranchGeo: boolean;
  device: null | { model: string; os: string; osVersion?: string; appVersion?: string;
                   activatedAt: string; lastSeenAt: string; lastDistanceMeters?: number; lastAccuracyMeters?: number };
  burstsToday: number;
};
type Credentials = { branchId: string; branchName: string; email: string; password: string; unlockPin: string };
type ReviewItem = {
  checklogId: string; employeeId: string; fullName: string;
  type: "checkin" | "checkout" | "restin" | "restout"; timestamp: string; status: string;
  identification: "qr+photo" | "code+photo"; photoUrl: string | null;   // URL firmada, 5 min
  inBurst: boolean; outOfRadius: boolean;
};
```

## El QR

`CB360K1.<employeeId>.<mac>`: `mac` = los primeros 16 bytes, en base64url, de
`HMAC-SHA256(KIOSK_SECRET, "qr:" + entityId + ":" + employeeId + ":" + version)`. `version`
vive en `employees/{id}.kioskQr.version` (1 si no existe). **No se guarda el QR**: se calcula
cuando se pide (tarjetas, «Mi QR») y se comprueba al leerlo. Regenerar = subir la versión.

---

## Diferencias con el README, decididas al implementar

- **Login:** ruta propia `POST /auth/kiosk/session` en vez de que `POST /auth/login` aprenda el
  claim: el login de empleados es camino crítico y no se toca.
- **QR calculado, no generado por lotes:** activar el módulo no escribe nada por empleado; todo
  empleado (también los nuevos) tiene QR desde el primer momento; lo que se hace por lotes es
  generar los **códigos** de una sucursal (200 escrituras por lote).
- **Salir de la tablet:** PIN de desbloqueo del quiosco (en el panel con las credenciales), no el
  código de un administrador.
- **Rutas de tablet** bajo `/kiosk/*` (un router con el `kioskToken`); las de panel bajo `/kiosks/*`.
- **Foto en JSON base64**, no multipart: ~80 KB por fichaje, dentro del límite del servicio.
- **Pendiente en esta rama:** aviso push de ráfaga y de dispositivo sustituido (quedan en el
  quiosco y en la revisión), crear el quiosco al dar de alta una sucursal nueva (hoy: «Activar»
  otra vez, que es idempotente), Cloud Tasks. Las fotos van al bucket del sistema (decisión del 2026-10-19);
  `KIOSK_MEDIA_BUCKET` queda para el día que haga falta otro.

---

## Estado de la implementación (2026-10-18)

Rama `feat/quiosco`, desde `develop`, en un worktree por repositorio. **Nada empujado ni
desplegado.** Ninguna pieza se ha probado todavía contra un servidor vivo ni en un dispositivo.

| Repo (worktree) | Commits | Comprobado |
|---|---|---|
| `encodebiz-api-quiosco` | `shared`: módulo `checkbiz/kiosk` y `checkbiz/storage`; refactor del fichaje a `registerChecklog(body, actor)`; rutas del quiosco; reglas | typecheck de `shared` y `checkinbiz` limpio; 13 tests nuevos de `shared` en verde; el servicio arranca en local contra dev y las rutas nuevas responden 401 con el `code` del contrato sin credencial; prueba de reglas con el emulador, 0 fallos (10 casos nuevos) |
| `checkbiz360-quiosco` | dependencias y permisos; feature `lib/features/kiosk`; rama del login, arranque, router, «Mi QR»; tests | `flutter analyze` sin issues nuevos (67 antes y después); 349 tests en verde (57 nuevos); compilan el APK de Android y la app de iOS en simulador |
| `encodebiz-front-saas-quiosco` | tipos, servicio y proxy; página Quiosco con tarjetas, códigos y revisión | `tsc` y `lint` igual que la base (29 errores previos de imágenes; 0 errores de lint) |

### Decisiones de implementación que no estaban en el diseño

- **QR y foto con dos cámaras, no una.** ML Kit en iOS sólo llega por CocoaPods y la app es
  sólo Swift Package Manager; se usa `mobile_scanner` en la pantalla de inicio y `camera` en la de
  confirmar, con un relevo de cámara de unos cientos de milisegundos.
- **Tras abrir la sesión del quiosco, la app cierra la sesión de Firebase**: el `kioskToken` es
  la única credencial que necesita. Y las reglas de Firestore dejan fuera a cualquier sesión con
  el claim `kind: "kiosk"`, por si las credenciales salen del centro.
- **«Fuera de turno»** en el quiosco dice «Fuera de tu turno. Avisa al encargado»; el resto de
  códigos de fichaje reutilizan los textos de la app.

### Lo que hace falta para probarlo en dev

1. Variables del servicio `checkinbiz`: `KIOSK_SECRET` (sin ella usa `JWT_2FA_SECRET`, sólo para
   dev) y `KIOSK_MEDIA_BUCKET` (sin ella, el bucket por defecto).
2. Variable del panel: `NEXT_BACKEND_URI_CHECKINBIZ_KIOSKS_HANDLER=<API>/api/v1/checkinbiz/kiosks`;
   sin ella el proxy responde 403.
3. Desplegar las reglas de Firestore a dev (`--project dev-encodebiz`).
4. Índice compuesto de `checklogs` por `(branchId, timestamp)` para la revisión: está declarado
   en `encodeBiz-SAAS/firestore.indexes.json`, pero hay que comprobar con `gcloud` que está
   desplegado.
5. Una empresa de prueba con una sucursal geolocalizada y dos o tres empleados.

### Pendiente (no bloquea la demo)

- **Fotos en el bucket por defecto = legibles por cualquier sesión** según `storage.rules`
  (comodín `request.auth != null`). En producción `KIOSK_MEDIA_BUCKET` tiene que ser el bucket
  europeo, que no expone reglas de cliente; o añadir `match /kiosk/{p=**} { allow read, write: if false; }`.
- Aviso push de ráfaga y de dispositivo sustituido (hoy quedan en el quiosco y en la revisión).
- Crear el quiosco al dar de alta una sucursal nueva (hoy: «Crear los que faltan» en el panel).
- Prueba de extremo a extremo en `qa/tests/con-datos` (activar, sesión dentro y fuera del radio,
  sustitución, identificar, fichar con foto, ráfaga, rechazo) y catálogo de QA.
- La foto en la fila de asistencia del panel, y la edición de foto y retención por empresa.
- La reconciliación nocturna del almacenamiento y la migración de los demás módulos al contador.
- iOS: el bloqueo es Acceso Guiado configurado a mano; el iPhone queda en vertical.

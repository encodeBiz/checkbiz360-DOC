# Segundo factor del empleado — port de Firebase a `checkinbiz`

El TOTP del empleado (el QR que se escanea con Google Authenticator y el código que se
teclea después) vivía en dos Cloud Functions, `enable2FA` y `verify2FA`. Ahora lo sirve el
servicio `checkinbiz`, detrás de nginx, sin cold start.

El TOTP del **panel** —`enable2FAUser`, `verify2FAUser`, `get2FAUserStatus`— sigue en
Firebase: ver [Lo que queda fuera](#lo-que-queda-fuera).

## Las rutas

| Antes (Cloud Function) | Ahora |
|---|---|
| `apiV100-firebaseEntryHttp-enable2FA` | `POST /api/v1/checkinbiz/auth/2fa/enable` |
| `apiV100-firebaseEntryHttp-verify2FA` | `POST /api/v1/checkinbiz/auth/2fa/verify` |

La credencial no cambia: el `sessionToken` firmado con `JWT_2FA_SECRET` que emite
`/auth/validate`, en la cabecera `Authorization: Bearer`. De ese token salen `employeeId` y
`entityId`, que **pisan** lo que venga en el cuerpo — si los tomara del cuerpo, cualquiera
podría pedir el QR de un compañero.

Las respuestas son las mismas byte a byte: `{secret, otpauthUrl, qrImage}` al dar de alta y
`{message, expiresIn: 300}` al verificar, con los códigos `twofactor/not_activated` y
`twofactor/invalid_code` que la app ya sabe leer.

## Lo que no es evidente

**Verificar el código también da de alta el teléfono.** El fichaje rechaza con
`auth/untrusted_device` cualquier aparato que no esté en `security/trustedDevicesId`, y este
endpoint es donde el teléfono se gana el sitio. Portar la verificación sin esa parte deja a
la persona validada y sin poder fichar, con un error que no menciona el 2FA por ningún lado.

**Dar de alta pisa el secreto anterior.** `enable` acuña uno nuevo y pone `verifiedAt` a
null. Probarlo contra alguien que ya tiene el 2FA configurado le obliga a volver a escanear.
Para las pruebas, empleado de pruebas.

**El código maestro ya no está escrito a fuego.** En Firebase había un `042691` en el código
fuente que abría el segundo factor de cualquier empleado, tuviera secreto o no. La salida de
emergencia se conserva pero apagada: sin `TWOFA_MASTER_CODE` en el entorno, no existe.

## El corte

El orden importa, y es el de siempre: contenedor verde primero, cliente después.

1. Desplegar a `staging` y comprobar que el contenedor responde con un `sessionToken` real:
   `/auth/validate` para conseguirlo, `2fa/enable` para el QR, `2fa/verify` con el código.
2. Comprobar que `JWT_2FA_SECRET` es **el mismo valor** que en Firebase. Si no, los tokens
   que la app ya tiene no valen y el 2FA falla con `auth/unauthorized`.
3. Solo entonces, en `checkbiz360/lib/core/constants/app_constants.dart`:

```dart
static String get enable2FAEndpoint => '$_checkinbizBase/auth/2fa/enable';
static String get verify2FAEndpoint => '$_checkinbizBase/auth/2fa/verify';
```

**Rollback** — devolver esas dos constantes a lo que había:

```dart
// dev
'https://apiv100-firebaseentryhttp-enable2fa-3bnjgtprva-uc.a.run.app'
'https://apiv100-firebaseentryhttp-verify2fa-3bnjgtprva-uc.a.run.app'
// prod
'$authEndpoint-enable2FA'
'$authEndpoint-verify2FA'
```

Las funciones se quedan desplegadas hasta que el corte lleve un tiempo en pie: apagarlas es
una decisión aparte y posterior.

## Lo que queda fuera

El segundo factor del panel no se ha portado porque **no tiene servicio donde vivir**. Toca
`users/{uid}` y escribe *custom claims* de Firebase Auth, o sea la cuenta de la plataforma,
no checkbiz. Meterlo en `checkinbiz` sería convertirlo en el cajón que
[ADR-0001](adr/0001-limite-de-checkinbiz-y-servicio-critico.md) dice que no sea, y `backoffice`
es el panel del staff de encodeBiz, otro público distinto.

Cuando se decida su casa, el algoritmo ya está compartido: `TwoFactorVerificationService` vive
en `@encodebiz/shared` justamente para eso. Y el corte allí es barato — tres variables
`NEXT_BACKEND_URI_*` del front, sin release de app de por medio.

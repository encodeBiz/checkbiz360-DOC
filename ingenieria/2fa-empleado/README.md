# Segundo factor del empleado — port de Firebase a `checkinbiz`

El TOTP del empleado (el QR que se escanea con Google Authenticator y el código que se
teclea después) vivía en dos Cloud Functions, `enable2FA` y `verify2FA`. Ahora lo sirve el
servicio `checkinbiz`, detrás de nginx, sin cold start.

El TOTP del **panel** —`enable2FAUser`, `verify2FAUser`, `get2FAUserStatus`— también vive ya
en `checkinbiz` desde el 2026-09-08: ver [El segundo factor del panel](#el-segundo-factor-del-panel).

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
2. Solo entonces, en `checkbiz360/lib/core/constants/app_constants.dart`:

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

Sobre `JWT_2FA_SECRET` no hace falta preocuparse: hoy la app ya pide el `sessionToken` al
contenedor y se lo presenta a las funciones de Firebase, y eso funciona. O sea que las dos
casas firman con el mismo secreto desde antes de este port. Después del corte, además, ya no
hay dos casas.

Las funciones se quedan desplegadas hasta que el corte lleve un tiempo en pie: apagarlas es
una decisión aparte y posterior.

## El segundo factor del panel

Portado el **2026-09-08**, también a `checkinbiz`.

| Antes (Cloud Function) | Ahora |
|---|---|
| `apiV100-firebaseEntryHttp-get2FAUserStatus` | `GET /api/v1/checkinbiz/auth/2fa/user/status` |
| `apiV100-firebaseEntryHttp-enable2FAUser` | `POST /api/v1/checkinbiz/auth/2fa/user/enable` |
| `apiV100-firebaseEntryHttp-verify2FAUser` | `POST /api/v1/checkinbiz/auth/2fa/user/verify` |

Cuelga del router **autenticado** y no del público, porque su credencial sí es el ID token de
Firebase: quien configura el segundo factor del panel ya ha entrado con su correo y su
contraseña. El `uid` sale de ese token, nunca del cuerpo.

Va bajo `/2fa/user/…` y no bajo `/2fa/…` para no chocar con el del empleado. Comparten motor
—`TwoFactorVerificationService` de `@encodebiz/shared`, mismo secreto en base32 y misma
etiqueta `otpauth://`— y no comparten nada más: aquí el sujeto es un usuario del panel y su
secreto vive en `users/{uid}/security/twoFA`.

### Por qué se decidió lo contrario de lo que decía este documento

La versión anterior de esta sección decía que el 2FA del panel **no tenía servicio donde
vivir**, y que meterlo en `checkinbiz` lo convertiría en un cajón. Las dos cosas eran ciertas
cuando se escribieron. Han cambiado dos:

1. **Ya hay un criterio escrito de qué es el núcleo**, y el acceso lo es sin discusión: esto
   entra en cada inicio de sesión de un administrador. Ver
   [salida-del-monolito/ADR-003](../salida-del-monolito/adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md).
2. **`checkinbiz` ha dejado de ser un cajón**: la gestión de plantilla salió a `employees`, y
   los centros y la empresa nacieron en `branches` y `entities`. El servicio se ha hecho más
   pequeño, no más grande, y lo que queda dentro es el camino del fichaje y sus dependencias.

Lo que no cambia es el riesgo que aquella advertencia señalaba, así que sigue anotado: el
criterio de entrada al núcleo son dos varas —que un error propio salga como un fichaje que no
cuenta, y que no sea código que se toque a menudo—, y hay que sostenerlas.

### Lo que hay que mirar al cortar

`verify2FAUser` no solo valida el código: **escribe custom claims en Firebase Auth**
(`admin:true`, `twoFA:true`), mezclándolas con las que ya hubiera —escribirlas a pelo borraría
cualquier otra que llevara la cuenta—. De esas claims cuelga el guard de sesión del Edge del
panel, y el front tiene que **refrescar el ID token** justo después de la llamada o seguirá
presentando el de antes, sin `twoFA`.

Por eso el síntoma de un corte mal hecho aquí no es un error visible: es alguien entrando al
panel sin segundo factor.

El corte es barato: tres variables `NEXT_BACKEND_URI_*` del front, sin release de app.

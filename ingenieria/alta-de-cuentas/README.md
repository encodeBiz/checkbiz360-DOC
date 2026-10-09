# Alta de cuentas — llevarla al contenedor y firmar la llamada

**Estado:** diseño aterrizado, sin implementar. Rama `feat/alta-firmada-s2s` desde
`develop`, en `encodebiz-api` y en `encodebiz-front-saas` (2026-09-29).

El alta de una cuenta la hace un servidor nuestro desde el 2026-09-04, y su ficha se escribe
llamando a un backend. Faltan dos cosas: que ese backend **sea el portado** —lo es en el
código y no en producción— y que **pueda comprobar quién le habla**.

## El hallazgo que ordena todo lo demás

El alta está portada al contenedor: `services/entities/src/interfaces/http/user.router.ts`,
montado en `POST /api/v1/users` detrás de `requireFirebaseAuth`, con el mismo contrato y el
mismo `201 {"message": "Usuario creado"}`.

**Producción no la usa.** En Vercel, `NEXT_BACKEND_URI_CREATE_USER` apunta a
`https://apiv100-firebaseentryhttp-users-createusers-…-uc.a.run.app`, la Cloud Function.
Por eso las 19 altas de la oleada medida aparecen en los logs de esa función.

No es un caso aislado: de las variables `NEXT_BACKEND_URI_*` de producción, **18 apuntan al
contenedor y 24 siguen en `run.app`**. El port se hizo; la variable no se movió. Es la misma
deriva que ya está documentada en otros sitios —el código portado y el tráfico yendo al
sitio viejo— y aquí tiene una consecuencia concreta: producción corre la versión **más
débil** de las dos.

Porque la portada comprueba cosas que la función no:

| | Función (la que usa prod) | Contenedor (la portada) |
|---|---|---|
| `uid` del cuerpo ≠ `uid` del token | lo sobreescribe con el del token | responde `403 uid mismatch` |
| Recuperación de contraseña | sin límite de intentos, y filtra si el correo existe | 3 intentos por 15 min y respuesta genérica siempre |
| Límite de peticiones | no hay | `security_rate_limits`, contador transaccional por hash de correo e IP |

Ese `security_rate_limits` es, además, la pieza que faltaba para poder estrangular las altas:
está escrito, probado y en producción, sirviendo a la recuperación de contraseña.

## La decisión

Tres movimientos, en este orden:

1. **Apuntar el alta al contenedor.** Cambiar una variable de entorno en Vercel. Sin código.
2. **Firmar la llamada.** La ruta del panel firma con HMAC sobre marca de tiempo y nonce; el
   contenedor verifica antes de tocar nada. Sin firma válida y fresca, el endpoint no existe.
3. **Retirar la función.** `users-createusers`, y detrás `recoverypassusers`, cuyo gemelo
   portado también es mejor.

El contrato de la firma está en [02_contrato.md](02_contrato.md), el porqué de que sea
rotatoria y no una clave fija en
[ADR-001](adr/ADR-001-firma-rotatoria-en-lugar-de-clave-fija.md), y el orden de despliegue
—que no es negociable— en [03_fases.md](03_fases.md).

## Dónde vive cada pieza, y por qué

| Pieza | Dónde | Por qué ahí |
|---|---|---|
| El verificador | `encodebiz-api` → `packages/shared/src/middleware/` | Ahí ya vive `apiKeyAuth.ts` con `x-encodebiz-key`: el idioma existe y se replica, no se inventa |
| La firma del alta | `encodebiz-front-saas` → `src/app/api/auth/register/route.ts` | Única ruta de `api/` que llama al backend con `fetch` directo |
| La firma de lo demás | `encodebiz-front-saas` → `src/lib/http/serverBackendProxy.ts` | Firmar aquí hace que cualquier llamada S2S futura lo herede sin tocar código |
| El secreto | Vercel producción, y `.env.staging` / `.env.production` del stack | Los dos lados son nuestros: lo que se comparte es un secreto, no una identidad |

La variante buena del idioma es `services/sales/src/interfaces/http/hiddenApiKey.ts`:
comparación en tiempo constante y **404 en vez de 401**, porque un 401 confirma que en esa
URL hay algo que proteger. Es la que se copia.

## Quién llama al alta, que es lo que hace esto posible

Dos caminos, y **ninguno sale del navegador**:

- `registerAccount` → `/api/auth/register` → `fetch` directo al backend.
- `signUpEmail` → `/api/proxy/create_user` → `serverBackendProxy` → el backend. Lo usa
  completar perfil.

Por eso se puede exigir firma sin romper nada. El día que un formulario llame al backend
desde el navegador, esto se cae: el navegador no puede firmar sin llevar el secreto dentro,
y un secreto en el bundle no es un secreto.

De paso, el comentario de cabecera de `user.router.ts` dice que la cuenta de Auth «la crea el
NAVEGADOR antes de llegar aquí». Eso dejó de ser verdad el 4 de septiembre: la crea la ruta
de servidor con el Admin SDK. Se corrige al tocar el fichero.

## Alcance — lo que esto cubre y lo que no

Cubre que la llamada venga de nuestro Vercel, y acota a dos minutos lo que vale un valor
filtrado. Cierra la llamada directa al alta, que hoy acepta a cualquiera que traiga un ID
token de Firebase válido —y eso lo tiene cualquiera que se haya registrado—.

No distingue al script del cliente. Las altas del bot entran por
`POST /api/auth/register`, o sea por nuestro propio servidor, y la firma se emite dentro de
él: de las 19 altas medidas, 18 eran del bot y una de un cliente real, y las 19 salieron de
Vercel. Una firma las habría validado todas. Queda escrito para que dentro de seis meses
nadie deduzca de la existencia de este documento que las altas falsas quedaron resueltas.

Lo que sí las separa —y sigue abierto— está en
[01_as-is.md](01_as-is.md#lo-que-queda-abierto): el teléfono imposible, el correo de
bienvenida que sale a direcciones sin verificar, y el límite de altas por ventana, que con
`security_rate_limits` ya no hay que construir.

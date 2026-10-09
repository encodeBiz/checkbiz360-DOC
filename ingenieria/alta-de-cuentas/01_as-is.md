# 01 — Lo que se midió en producción

**Fecha de la medición:** 2026-09-29, sobre `encodebiz-services`. Todo lectura: export de
Firebase Auth, config de Identity Platform, IAM de Cloud Run, logs de Cloud Logging y una
consulta a Firestore. El único POST fue sin cuerpo y sin token contra la ruta del alta, que
no puede crear nada.

218 cuentas en Auth. **50 llevan huella de bot.**

## La huella, y por qué es fiable

Una cuenta es de bot si cumple las tres: el alta y su último acceso están separados por
**menos de dos segundos**, no tiene claims, y no tiene el correo verificado.

Los dos segundos son la clave. La ruta del alta crea la cuenta y acto seguido canjea un
custom token, y ese canje cuenta como acceso: por eso toda cuenta recién creada nace con el
acceso a unos 300 ms. En una cuenta de persona real ese valor se sobrescribe la primera vez
que vuelve a entrar, y pasa a horas o días. Que siga a 300 ms meses después significa
exactamente una cosa: **nadie volvió nunca**.

El control que lo demuestra son tus dos cuentas de prueba del 4 de septiembre,
`jose-test@encodebiz.com` (324 ms) y `codex-human-browser-…@example.com` (283 ms): mismo
valor, porque tampoco volvieron.

## Dos oleadas, no una

| | Hasta el 04-09 08:53 | Del 23-09 al 28-09 |
|---|---|---|
| Cuentas | 30 | 18 |
| Alta → acceso | **0 ms exactos** | 265–363 ms |
| Nombre declarado | ninguno | basura (`Jetnwplep`, `Zqrljcvvi`, `Daaaptksu`) |
| Vía | `accounts:signUp` con la API key pública | `POST /api/auth/register` |

La primera murió el mismo día que subió el alta en servidor —última cuenta a las 08:53, el
cambio en `main` a las 15:37, el `beforeCreate` cableado a las 14:04—. La correlación es
limpia; no se afirma más que eso.

La segunda entra por la ruta nueva. Lo prueban tres cosas del mismo alta de las 22:00:19 del
28-09: la cuenta nace a las `.227`, el canje del custom token marca acceso a las `.533`, y la
llamada a `users-createusers` devuelve `201` a las `.611` desde una IP de AWS con
`User-Agent: node` —que es el `fetch` de nuestro propio Vercel—. La ficha de Firestore
quedó escrita a las `.028` del segundo siguiente, con `fullName: "Daaaptksu"` y
`phoneNumber: "342012409623"`.

## Por qué los controles que hay no las ven

`beforeUserCreated` **está desplegado y cableado** (`blockingFunctions.triggers.beforeCreate`,
actualizado el 2026-09-04 a las 14:04). No se dispara porque **las blocking functions de
Identity Platform no se ejecutan cuando la cuenta la crea el Admin SDK**, y la ruta del alta
usa el Admin SDK precisamente para poder desactivar el alta pública. El filtro quedó fuera
del camino por construcción, no por avería. Lo mismo `disabledUserSignup: true`: cierra la
puerta del cliente, y esta no lo es.

Y aunque se disparara, no las pillaría. El validador de
`services/firebase_sdk/src/auth/emailFraud.validator.ts` aplicado a los 18 de la oleada nueva
**bloquea 1**, y por accidente: `john@csdllc.org`, por empezar por `john`. Los puntos
—que son la señal real— solo suman 20 puntos y el umbral está en 50.

Añadido: `recaptchaConfig.emailPasswordEnforcementState` está en `UNSPECIFIED`. Las claves
existen, la protección no está exigida.

## Para qué es el ataque

No es para entrar. Ninguna verifica el correo, ninguna vuelve, ninguna crea entidad ni
suscripción. Lo único que produce un alta es el **correo de bienvenida**, y
`EmailService.sendEmail` lo manda directo por SMTP con nodemailer, sin cola, desde
`hola@encodebiz.com`.

Las direcciones son reales y ajenas: `ulrike.kaltenbach@schwarzwaldmilch.de`,
`dior.dieng@mindshareworld.com`, `chief@wcfpd.net`, `christian.praters@ravapor.de`. Y **las
24 de Gmail llevan todas puntos insertados** en la parte local, que Gmail ignora al entregar
y sirven para esquivar el deduplicado de quien tenga una lista.

Es list bombing: se usa nuestra alta para sembrar el buzón de un tercero. Lo que se quema es
la reputación de nuestro SES.

## Cómo pasan Turnstile: no establecido

La puerta está puesta y funciona. Comprobado en caliente: un POST sin token a
`https://saas.encodebiz.com/api/auth/register` responde `403 turnstile/failed`.
`TURNSTILE_SECRET` y `TURNSTILE_HOSTNAMES` están definidas en Vercel producción desde hace
25 días, y el verificador comprueba `success`, `action` y `hostname`, y falla cerrado.

Así que llegan con un token válido para la acción `signup` y un dominio aceptado. **Cómo lo
consiguen no está establecido.** Caben al menos dos lecturas que no se pueden separar con lo
que se ve desde producción: un servicio de resolución, o un valor de `TURNSTILE_HOSTNAMES`
que les permita fabricar tokens en otro sitio —el propio fichero advierte de localhost—. Lo
que lo resolvería: leer el valor de esa variable y mirar las analíticas del widget en
Cloudflare, que dicen desde qué hostname se resuelven los retos.

## Lo que queda abierto

**El teléfono imposible.** Los 18 de la oleada nueva declaran `34` seguido de **diez**
dígitos aleatorios (`342012409623`, `348062167225`, `347257232443`…). Un número español
tiene nueve después del 34, y además estos empiezan por 2, 3, 4 o 5, que no son inicios
válidos. Tus dos cuentas de prueba declaran once dígitos, correctos. La ruta hoy no lo mira:
coge el campo, lo recorta a 256 caracteres y lo pasa tal cual, y ni siquiera es obligatorio.
Es una regla de formato, no una heurística que haya que afinar. **Falta comprobar que ningún
cliente real tiene un teléfono que fallaría esa validación**; sin eso no se puede activar.

**El correo de bienvenida a direcciones sin verificar.** Mientras salga antes de que la
dirección esté probada, el ataque paga aunque acierten con el teléfono. Detrás de la
verificación, un alta falsa deja una fila inútil y no molesta a nadie.

**Las 50 cuentas siguen ahí.** `ghostUsersMaintenance` no las va a retirar: su criterio es
la cuenta huérfana sin ficha, y estas tienen ficha en `users/{uid}`, escrita por el propio
alta.

**Tres endpoints más publicados a `allUsers`** en IAM: `entity-createentity`,
`subscriptions-subscribe` y `criticalhandler`. Llevan su propia comprobación de token
dentro; merecen una revisión aparte. `recoverypassusers` es el cuarto y es el candidato
natural a heredar la firma, porque su camino es el mismo: navegador → proxy → función.

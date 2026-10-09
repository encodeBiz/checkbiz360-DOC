# 03 — El orden del despliegue

Cinco pasos. El orden importa porque hay un tramo en el que una comprobación nueva no
devuelve un error visible: **borra la cuenta del cliente**.

## Por qué el orden no es negociable

Cuando la llamada al backend falla, la ruta del alta ya ha creado la cuenta de Auth. Su
`catch` llama a `rollback()`, que hace `deleteUser(uid)`. El cliente ve
`auth/registration-failed` y en Firebase Auth **no queda ni rastro de que existió**.

Así que si el verificador empieza a exigir la firma antes de que el panel la mande, no se ve
un pico de errores en Auth: se ve silencio. El síntoma no se parece a la causa, y el registro
está roto para todo el mundo mientras dure.

## Fase 0 — Apuntar el alta al contenedor

`NEXT_BACKEND_URI_CREATE_USER` pasa a `https://api.checkbiz360.com/api/v1/users`.

Sin código. Y tiene premio inmediato, más allá de dejar el alta en el repo donde vive el
idioma de la firma: **la función que usa producción hoy borra la cuenta si el correo de
bienvenida falla.** En `createUserController`, el `await sendEmail(...)` está dentro del
`try` y su excepción cae en un `catch` que responde `500`; el `500` hace que la ruta del
panel llame a `rollback()`. Un hipo de SES deja al cliente sin cuenta. La versión del
contenedor manda ese mismo correo con `.catch()` colgado, así que el alta sobrevive.

Cómo se prueba, con el panel en local contra el API de desarrollo —`npm run start:dev`, que
lee `.env.development`; en Vercel no hay preview ni staging, solo producción, así que sus
variables no se tocan para probar—:

1. Un alta completa de principio a fin, con acento y `ñ` en el nombre.
2. Otra desde **completar perfil**, que es el segundo camino (`/api/proxy/create_user`).
3. Que el correo de bienvenida llegue una sola vez, y que a un colaborador invitado no le
   llegue ninguno.

Después, la variable en Vercel producción. El despliegue del panel es automático al tocar
`main`, pero una variable de entorno **no redespliega sola**: hay que relanzar el último
despliegue para que la coja.

## Fase 1 — El verificador, permisivo

`requireS2SSignature` en `packages/shared/src/middleware/`, aplicado a
`/api/v1/users` en `entities`, en modo permisivo:

- Si la cabecera viene, se verifica. Si no cuadra, `404`.
- Si **no** viene, se registra y se deja pasar.

Con eso, nada puede romperse: el panel todavía no firma y las altas siguen entrando. Y el
log dice cuántas llegan firmadas y cuántas no, que es lo que hay que mirar antes de la fase 3.

Aquí entra también la línea del `verify` en `app.ts` para guardar el cuerpo en bruto
(ver [02_contrato.md](02_contrato.md)).

Por `feat/alta-firmada-s2s → develop → staging`, y comprobado en el VPS de desarrollo:

```bash
docker compose -f docker-compose.staging.yml -p encodebiz-api-dev logs -f entities
```

## Fase 2 — El panel firma

La firma en `route.ts` y en `serverBackendProxy.ts`, y el secreto en Vercel producción.

Al acabar, el log de la fase 1 tiene que mostrar **todas** las altas firmadas y ninguna sin
firmar. Si aparece una sin firmar, hay un tercer camino que no estaba en el mapa y hay que
encontrarlo antes de seguir. Conviene dejar pasar unos días: las altas reales son pocas —una
o dos por semana— y con una tarde de datos no se distingue «no hay tráfico sin firmar» de
«no hay tráfico».

## Fase 3 — Exigir la firma

Se quita el modo permisivo: sin cabecera, `404`.

El interruptor es una variable, no un despliegue de código —`S2S_SIGNATURE_REQUIRED`— para
poder volver atrás sin esperar un build si aparece algo no previsto.

## Fase 4 — Retirar la función

`users-createusers` deja de tener tráfico y se borra. Detrás va `recoverypassusers`, cuyo
gemelo del contenedor es mejor: limita a 3 intentos por 15 minutos, responde siempre lo
mismo exista o no la cuenta, y respeta el idioma de la cabecera.

Borrar funciones es el paso con más filo de todos y no se hace de pasada: `firebase deploy`
**siempre** con `--project` explícito, y con producción de por medio se para y se pregunta
antes. Hay precedente de un despliegue que podó lo que no tocaba.

Quedan 22 variables más apuntando a `run.app` con su port hecho. Cada una es esta misma
fase 0, y ninguna corre prisa hasta que alguien mire si la versión portada y la desplegada
siguen diciendo lo mismo.

## Lo que este despliegue no arregla

Las altas falsas siguen entrando, porque entran por la ruta del panel y la firma se emite
dentro de ella. Lo que las separa de un cliente real está en
[01_as-is.md](01_as-is.md#lo-que-queda-abierto). El candidato con menos coste y sin falsos
positivos conocidos es el teléfono imposible; el que no se puede sortear es no mandar el
correo de bienvenida a una dirección sin verificar.

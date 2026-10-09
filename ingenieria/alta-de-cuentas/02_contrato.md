# 02 — El contrato de la firma

Una cabecera, un secreto compartido y una ventana de dos minutos. Quien firma es una ruta de
servidor del panel, en Vercel; quien verifica es el contenedor.

## La cabecera

```
x-encodebiz-sign: t=1790632819227,n=9f2c1a…,v1=4b7d…e1
```

| Campo | Qué es |
|---|---|
| `t` | Marca de tiempo en milisegundos, la del firmante |
| `n` | Nonce aleatorio de 16 bytes en hexadecimal |
| `v1` | El HMAC en hexadecimal. El `v1` es la versión del esquema, para poder cambiarlo sin romper lo desplegado |

Se firma esta cadena, exactamente:

```
${t}.${n}.${sha256hex(cuerpo_en_bruto)}
```

`HMAC-SHA256` con `ENCODEBIZ_S2S_SECRET`. Se manda además de la cabecera `Authorization`
que ya va: la firma dice **de dónde** viene la llamada, el ID token dice **de quién** es la
cuenta. Son dos preguntas distintas y las dos hay que responderlas.

## El cuerpo se firma en bruto, y aquí está la trampa

Se firma el byte a byte que viaja, no el objeto. Es el mismo problema que ya está resuelto en
`services/billing/src/interfaces/http/webhook.router.ts` para los webhooks de Stripe, y su
comentario lo dice mejor que yo: *«la firma se calcula sobre el cuerpo tal y como llegó, así
que si `express.json` lo parsea antes, la verificación falla siempre»*.

En `billing` eso se resuelve con `raw({type: "application/json"})` en la propia ruta. En
`entities` no se puede copiar tal cual: `express.json({limit: "1mb"})` está montado en
`app.ts` **antes** de los routers, así que cuando llega el middleware el stream ya está
consumido y `raw()` recibiría un buffer vacío.

Dos salidas, y la primera es la buena:

- **Guardar el buffer al parsear.** `express.json({ limit: "1mb", verify: (req, _res, buf) => { (req as any).rawBody = buf } })`. Una línea en `app.ts`, no cambia el orden de nada y los routers siguen leyendo `req.body` como siempre.
- Montar la ruta firmada antes del parser con `raw()`. Funciona, obliga a reordenar `app.ts` y a parsear a mano dentro del router. Más superficie para equivocarse por menos ganancia.

Lo que **no** vale es recalcular el hash con `JSON.stringify(req.body)`: el orden de las
claves, los espacios y el escapado de los caracteres no ASCII pueden no coincidir con lo que
serializó el otro lado, y entonces la firma falla en las altas con una `ñ` o un acento en el
nombre y en ninguna otra. Un fallo que solo aparece con ciertos nombres es un fallo que se
descubre tarde y se diagnostica peor.

Y firmar el hash del cuerpo es lo que impide que una firma capturada sirva para dar de alta
**otra** cosa: vale para esa petición y para ninguna más.

## La ventana

Se acepta si `|ahora - t| <= 120_000`. Dos minutos, y en los dos sentidos, porque el reloj
del firmante y el del verificador no son el mismo.

Dentro de esa ventana, repetir la petición entera —misma firma, mismo cuerpo— se aceptaría.
El nonce no se guarda, a propósito: costaría una escritura por cada alta para impedir algo
cuyo único efecto es intentar escribir dos veces la misma ficha del mismo uid, y la ficha se
escribe con el `uid` del token. Queda dicho para que se sepa que es una decisión y no un
olvido. El día que la firma cubra endpoints donde repetir sí tenga consecuencias, el nonce
hay que empezar a quemarlo, y `security_rate_limits` ya sabe hacer contadores
transaccionales.

## El secreto

`ENCODEBIZ_S2S_SECRET`, 32 bytes aleatorios en hexadecimal, el mismo valor en los dos lados
y **distinto en desarrollo y en producción**. Si el de desarrollo se filtra, no abre nada.

- **Vercel**, entorno de producción, y **sin** el prefijo `NEXT_PUBLIC_`. Una variable
  `NEXT_PUBLIC_` acaba en el bundle que sirve el navegador; un secreto en el bundle no es un
  secreto, es la llave colgada al lado de la puerta.
- **El stack**, en `.env.staging` y `.env.production`, junto a `ENCODEBIZ_API_KEY`, que es su
  hermana mayor y ya vive ahí.

No se reutiliza `ENCODEBIZ_API_KEY`: esa la comparten hoy los servicios entre sí y el
backoffice, y la gracia de la nueva es que solo la conozcan dos partes.

## La respuesta cuando no cuadra

`404`, con el mismo cuerpo que da cualquier ruta inexistente de la casa
—`app.ts` de `entities` ya termina con `res.status(404).json({ok: false, error: "not_found"})`—:

```json
{ "ok": false, "error": "not_found" }
```

No `401`. Es el criterio ya razonado en
`services/sales/src/interfaces/http/hiddenApiKey.ts`: un `401` confirma que en esa URL hay
algo que proteger, y eso es justo la pista que busca quien sondea. Sin firma válida, el
endpoint no existe.

La comparación en tiempo constante, con la `safeEqual` de ese mismo fichero, que además
compara contra sí misma cuando las longitudes difieren para no delatar el tamaño.

## Sin secreto, la puerta se cierra

Si `ENCODEBIZ_S2S_SECRET` no está definida en el verificador, se responde `404`. No se pasa
de largo y no hay valor por defecto.

Esto va a contracorriente de lo que hay en el repo del SaaS, donde
`functions/src/core/shared/utils/validate2FAToken.ts` y `validateTokenStaff.ts` hacen
`process.env.JWT_2FA_SECRET || "fallback_dev_secret"`: si la variable falta, la verificación
**sigue pareciendo funcionar** con un secreto escrito en el código y subido a GitHub. Ese
patrón no se copia aquí, y queda apuntado como cosa a revisar por su cuenta.

Es el mismo criterio que ya aplica el verificador de Turnstile del panel: falta de
configuración es puerta cerrada, no puerta abierta.

## El orden dentro de la ruta del alta

La firma se calcula en el paso 5 de `route.ts`, el que llama al backend. Los pasos 1 a 4
—Turnstile, validación, `createUser`, canje del token— no se tocan.

Con una consecuencia que manda en el despliegue: cuando la llamada al backend falle, la
cuenta de Auth **ya existe**, y el `catch` de la ruta llama a `rollback()` y la borra. Es el
comportamiento correcto, y es lo que hace que el orden de [03_fases.md](03_fases.md) no sea
negociable.

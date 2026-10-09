# ADR-001 — Firma rotatoria en lugar de la clave fija que ya usamos

**Estado:** aceptada · 2026-09-29
**Contexto:** el alta de cuentas la llama un servidor del panel, y el backend no tiene forma
de comprobarlo: acepta a cualquiera que traiga un ID token de Firebase válido, y eso lo
tiene cualquiera que se haya registrado. Entre servicios ya existe una credencial S2S,
`x-encodebiz-key`, comprobada por `packages/shared/src/middleware/apiKeyAuth.ts`.

---

## La pregunta

¿Basta con poner `x-encodebiz-key` en esta llamada, como en las demás, o hace falta algo que
cambie en cada petición?

## La decisión

**Firma rotatoria.** `HMAC-SHA256` sobre marca de tiempo, nonce y hash del cuerpo, con una
ventana de dos minutos. La clave fija se queda donde está y no se extiende aquí.

## Por qué no la clave fija

El mismo valor viaja idéntico en cada petición, y esta petición cruza dos proveedores: sale
de Vercel y entra por nuestro nginx. Vive en las variables de entorno de los dos, y puede
acabar en un log, en una captura de pantalla o en un volcado de cabeceras de cualquiera de
los dos lados.

Y si se filtra, vale **para siempre**, sin que nadie se entere de cuándo empezó a valer para
otro. Un HMAC con ventana convierte una fuga permanente en una fuga de dos minutos: lo que se
capture nace muerto.

Hay además un motivo operativo. Rotar una clave fija compartida obliga a cambiarla a la vez
en los dos lados, y lo que hay entre los dos cambios es una ventana de registro caído. La
firma permite tener dos secretos válidos a la vez el día que haya que rotar, porque el
esquema lleva su número de versión (`v1=`) en la propia cabecera.

## Por qué no asimétrica

Una clave privada en Vercel y la pública en el contenedor también resolvería el problema, y
además evitaría compartir secreto. No compra nada aquí: **los dos lados son nuestros**, y no
hay ningún tercero que deba verificar sin poder firmar. Lo que sí trae es gestión de un par
de claves, su caducidad y su distribución, para una llamada entre dos piezas propias.

Se deja anotado como el camino a tomar el día que quien firme sea alguien de fuera —un
add-on, un cliente con su propia integración—. Ese día el `v1=` de la cabecera es lo que
permite convivir con esto.

## Qué se hace ahora

El contrato completo está en [02_contrato.md](../02_contrato.md). Lo que no es negociable de
él:

1. Se firma el cuerpo **en bruto**, no el objeto reserializado.
2. Comparación en **tiempo constante**.
3. Si falta el secreto, **404**. Nunca un valor por defecto: en el repo del SaaS hay dos
   verificadores que hacen `|| "fallback_dev_secret"` y siguen pareciendo funcionar con un
   secreto que está en GitHub.
4. `404` y no `401`, para no confirmar que en esa URL hay algo que proteger.

## Lo que esta decisión no decide

No distingue al script del cliente. Las altas falsas entran por la ruta del panel, y la firma
se emite dentro de ella: las 19 altas medidas —18 de bot y una de un cliente real— salieron
de Vercel y una firma las habría validado todas. Esta ADR responde «quién llama», no «quién
hay detrás».

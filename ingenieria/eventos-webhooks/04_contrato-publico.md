# 04 — Contrato público

Lo que ve quien integra. Se mantiene compatible con el módulo actual: quien ya consuma
webhooks de la plataforma no tiene que cambiar nada.

---

## 1. Entrega

`POST` a la URL suscrita, `Content-Type: application/json`. La URL debe ser **HTTPS**.

```json
{
  "id": "evt_9f3c1a7b2d4e5f60718293a4",
  "type": "attendance.clock_in",
  "version": "2025-08-01",
  "occurred_at": "2026-08-26T07:14:22.318Z",
  "entity_id": "ent_abc123",
  "data": { }
}
```

`data` tiene forma propia por evento, definida por un mapeador explícito del modelo interno al
externo. **No es un volcado del documento interno**, y ese es un cambio respecto al
comportamiento actual: hoy `attendance.clock_in` publica el checklog entero.

## 2. Cabeceras

| Cabecera | Contenido |
|---|---|
| `X-EncodeBiz-Event-Id` | `evt_…` — identificador único del evento |
| `X-EncodeBiz-Signature` | `t=<unix>,v1=<hmac_sha256>` |
| `X-EncodeBiz-Retry` | Número de reintento; `0` en el primer envío |
| `User-Agent` | `EncodeBiz Webhooks` |

## 3. Verificación de la firma

HMAC-SHA256 sobre la cadena `"{t}.{body}"` —el `t` de la cabecera, un punto, y el cuerpo crudo
tal cual llegó— con el `secret` del endpoint (`whsec_…`).

```js
const [t, v1] = header.split(",").map((p) => p.split("=")[1]);
const expected = crypto.createHmac("sha256", secret).update(`${t}.${rawBody}`).digest("hex");
const ok = crypto.timingSafeEqual(Buffer.from(v1), Buffer.from(expected));
```

Comparar en tiempo constante y rechazar si `t` se aleja más de cinco minutos del reloj propio.
El cuerpo tiene que ser el **crudo**: si el framework lo parsea y lo vuelve a serializar, la
firma no cuadra.

## 4. Respuesta esperada

`2xx` en menos de **4 segundos**. Cualquier otra cosa se considera fallo.

El consumidor no debe hacer trabajo pesado dentro de la petición: acusa recibo y procesa
aparte. Cuatro segundos es un timeout, no un presupuesto.

## 5. Reintentos

`[0, 30s, 2m, 10m, 1h]`, cinco intentos como máximo.

Se reintenta con `408`, `429`, `500`, `502`, `503`, `504` y con fallo de red o timeout.
Cualquier otro código se considera definitivo y la entrega muere sin más intentos.

Un endpoint se desactiva automáticamente tras **20 entregas muertas consecutivas**, no tras
una. Al desactivarse se notifica al administrador de la entidad.

## 6. Idempotencia — obligatoria

**El mismo evento puede llegar más de una vez.** No es un caso teórico: al emitir en el
momento de la acción, un reintento del emisor puede producir una entrega duplicada.

El consumidor debe guardar los `X-EncodeBiz-Event-Id` procesados y descartar los repetidos. Un
identificador visto dos veces es el mismo hecho, no dos.

Tampoco hay garantía de orden: dos eventos de la misma entidad pueden llegar cruzados. Si el
orden importa, ordenar por `occurred_at`.

## 7. Versionado

`version` viaja en cada evento. La versión vigente es `2025-08-01`.

- Añadir un campo a `data` **no** cambia la versión. El consumidor debe ignorar lo que no
  conoce.
- Quitar o renombrar un campo, o cambiar su significado, sí la cambia.
- Un endpoint queda fijado a la versión con la que se creó, y la migración es explícita: se
  publican ambas hasta que el cliente cambia.

## 8. Suscripción

Un endpoint declara a qué eventos se suscribe. Se admiten tres formas:

- El tipo exacto: `attendance.clock_in`
- La familia entera: `attendance.*`
- Todo: `*`

Los comodines son la diferencia práctica con el módulo actual: quien se suscribe a
`attendance.*` recibe los eventos nuevos de esa familia sin tocar su configuración.

El catálogo completo, con descripción y ejemplo por evento, se consulta en
`GET /api/v1/events/catalogue`.

## 9. Prueba

`POST /api/v1/events/endpoints/:id/test` emite un `endpoint.test` contra esa URL. Sirve para
validar firma y conectividad sin esperar a que ocurra nada real.

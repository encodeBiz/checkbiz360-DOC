# 07 — Estado verificado en desarrollo

**Fecha de la comprobación:** 2026-09-04
**Entorno:** desarrollo (`encodebiz-api-dev`, Firebase `dev-encodebiz`, base `encodebiz_staging`)

Este documento no diseña nada. Registra **qué se midió y qué salió**, para que la siguiente
persona que pregunte «¿los webhooks funcionan?» no tenga que volver a averiguarlo. Los
apartados 1 y 2 son hechos observados; el 3 son dos problemas abiertos que la comprobación
sacó a la luz.

---

## 1. La fontanería funciona

El módulo nuevo entrega. Comprobado de punta a punta, no por inspección de código.

Se dio de alta un endpoint desde el panel —`wh_0ec1…`, en
`entities/{entityId}/webhook_endpoints`, apuntando a un bin de webhook.site y suscrito a
`attendance.*`— y se emitió un `attendance.clock_in` real por la ruta S2S
(`POST /api/v1/events/s2s/publish`, API key, desde dentro de la red de contenedores):

| | |
|---|---|
| Entrega | `dly_327c50ac17bcf13b85ac572d` |
| Estado | `delivered`, intento 1, `last_status` 200 |
| Encolada | 21:53:38.660 UTC |
| Entregada | 21:53:38.817 UTC — **158 ms** |

Con eso queda verificado el camino entero: fan-out a los endpoints suscritos, resolución del
comodín `attendance.*`, firma HMAC, POST con las cabeceras del contrato, marcado en
`webhook_delivery` y respuesta 200 del receptor. El contenedor `events` está sano en
desarrollo, con el rescate cada cinco minutos y la purga a las 04:30, y la base tiene el
esquema esperado: `webhook_delivery` existe y `webhook_endpoint` no, que es exactamente lo que
dejó la migración `018_events_endpoints_a_firestore.sql`.

## 2. Lo que no ha salido, y por qué

Antes de esa prueba, `webhook_delivery` estaba **vacía**: cero entregas, ni pendientes ni
muertas. El `webhook_outbox` de Firestore —la cola del módulo viejo— también tenía **cero
documentos**. O sea que en desarrollo no había salido nunca un evento de negocio.

No es un fallo de entrega. Es que **nadie emitía** —esto es lo que se arregló ese mismo día,
ver la nota del final—. El único `publish()` del monorepo es el de
la propia ruta S2S de `services/events`; ningún caso de uso lo llama todavía, y
`services/firebase_sdk` no tiene ni un trigger montado.

Se hicieron dos fichajes reales desde la app durante la comprobación, y ninguno produjo nada,
por dos causas **distintas**:

- **El inicio de descanso (`restin`) no lo emite nadie, por diseño.**
  `attendance.break_start` está en el catálogo como `planned`, y el trigger viejo excluye
  `restin`/`restout` explícitamente. Nunca iba a salir.
- **La entrada (`checkin`) sí llegó a un emisor vivo, y aun así no salió.**
  `onChecklogWebhook` está desplegado en desarrollo y arrancó una instancia a las 21:50:05,
  segundos después del `POST /api/v1/checkinbiz/checklogs` que devolvió 201 a las 21:50:04. No
  encoló nada porque el módulo viejo compara la suscripción con `subscribedEvents.includes(type)`
  —cadena exacta— y el endpoint estaba suscrito a `attendance.*`. **El comodín solo existe en el
  módulo nuevo.**

De paso, esa segunda medición aclara una duda de arquitectura: **el fichaje ya entra por el
contenedor**. `createChecklog`, `updateChecklog` y `requestManualChecklog` no aparecen en
`firebase functions:list`, y el tráfico entra por nginx a `checkinbiz`. Es lo que hace que los
diez eventos de `attendance` sean cableables hoy — ver [03 §3.1](./03_catalogo-de-eventos.md).

## 3. Dos problemas abiertos

### 3.1 Dos módulos vivos sobre la misma colección de endpoints

El módulo viejo (`encodeBiz-SAAS/functions/src/core/webhook`) y el nuevo leen **la misma
colección**, `entities/{entityId}/webhook_endpoints`. Siguen desplegados su emisor
(`onChecklogWebhook`), su repartidor (`webhookWorker`, programado) y sus tres endpoints HTTP de
gestión.

Hoy no colisionan por casualidad: el viejo no casa comodines, y la única suscripción existente
es un comodín. **El día que alguien se suscriba a `attendance.clock_in` por el tipo exacto, ese
fichaje se entregará dos veces**, una por cada módulo, con dos firmas distintas y dos
identificadores de entrega distintos. El integrador lo verá como un duplicado inexplicable.

No hay decisión pendiente sobre esto —[05 §Oleada 2](./05_fases.md) ya dice que
`onChecklogWebhook` se borra—, pero sí un orden: **se borra en el mismo movimiento en que se
cablea `publish()` en `createChecklog.controller.ts`**, no antes ni después. Antes, deja de
emitirse lo poco que se emite; después, se abre la ventana del duplicado.

### 3.2 El catálogo promete lo que no entrega

`attendance.clock_in` y `attendance.clock_out` están marcados `available` en
`packages/shared/src/events/catalogue.ts`. Lo estaban con razón cuando los emitía el módulo
viejo; hoy, con el panel leyendo el catálogo nuevo, `available` le dice a quien integra que si
se suscribe los va a recibir. Y no los va a recibir: el módulo nuevo no tiene emisor para
ellos.

De los 53 eventos declarados, el panel ofrece los 53 como suscribibles y solo sale
`endpoint.test`.

**Resuelto el mismo día**, y en la otra dirección: en vez de devolver esos dos a `planned`, se
cablearon los 32 lanzadores que ya tenían su escritura en el contenedor y el catálogo pasó a
marcarlos `available`. Los 20 que siguen sin emisor se quedan en `planned`, que es lo que el
panel debe enseñar como todavía-no.

---

## Cómo repetir la comprobación

```bash
# ¿Ha salido algo? (dev)
docker compose -f docker-compose.staging.yml -p encodebiz-api-dev exec -T postgres \
  psql -U encodebiz -d encodebiz_staging -c \
  "SELECT event_type, status, attempt, last_status, created_at, delivered_at
     FROM webhook_delivery ORDER BY created_at DESC LIMIT 20;"

# ¿Quién está suscrito? (colección de Firestore, no Postgres)
#   entities/{entityId}/webhook_endpoints

# ¿Sigue vivo el módulo viejo?
firebase functions:list --project dev-encodebiz | grep -iE "webhook|checklog"
```

El disparo de prueba del panel (`POST /api/v1/events/endpoints/:id/test`) hace lo mismo que se
hizo aquí a mano y no necesita que nadie fiche. Es lo primero que debería probar quien integre.

---

## Nota posterior — 2026-09-04, misma fecha

Lo de arriba es la foto de antes. Después de tomarla se cableó `publish()` en los 32 casos de
uso de §3.1 del [03](./03_catalogo-de-eventos.md), en la rama `feat/eventos-oleada-2`. **Está
sin desplegar**: hasta que llegue a `staging`, todo lo medido en §2 sigue siendo cierto.

Lo único que queda del problema §3.1 es el orden de la retirada. Hoy no se duplica nada porque
el único endpoint suscrito usa comodín, así que desplegar estos 32 es seguro tal cual. Pero
`onChecklogWebhook` tiene que morir antes de que alguien se suscriba a `attendance.clock_in`
por el tipo exacto, o ese suscriptor recibirá cada fichaje dos veces.

# ADR-004 — La outbox en PostgreSQL; la configuración se queda en Firestore

**Fecha:** 2026-08-26 · **Revisada:** 2026-08-26, el mismo día
**Estado:** Aceptado (sustituye a la primera versión, que se llevaba las dos cosas a PostgreSQL)
**Decisionario:** Jose Acevedo

## Contexto

El módulo guarda dos cosas en Firestore: los **endpoints suscritos** de cada entidad
(`entities/{entityId}/webhook_endpoints`) y la **outbox de entregas**
(`entities/{entityId}/webhook_outbox`).

La primera versión de esta decisión se llevaba las dos a PostgreSQL, con un argumento que
solo era válido para una: la outbox no se purga nunca, no hay forma de escribirla en la
misma transacción que un dato de PostgreSQL, y el panel no puede consultarla con más de un
filtro sin añadir índices.

**Eso no describía a los endpoints.** Son configuración de la entidad: diez documentos por
cliente como mucho, que no crecen, que viven junto al resto de su configuración y que el
panel lee **en vivo** — el front escucha la colección y la lista se actualiza sola. Moverlos
convertía una lista reactiva en una que hay que refrescar a mano, y a cambio de nada.

## Decisión

Se parte en dos, por la línea que las separa de verdad: **lo que crece sin fin va a
PostgreSQL; la configuración se queda en Firestore.**

- `webhook_delivery` → **PostgreSQL**.
- `entities/{entityId}/webhook_endpoints` → **Firestore**, donde ya estaba y donde el front
  ya la lee.

El alta, la edición y la baja las **sigue sirviendo el contenedor** por HTTP; lo que cambia
es dónde escribe.

## Razones

**Las entregas crecen sin techo y nadie las mira en vivo.** Una por evento y por endpoint
suscrito. Se purgan por antigüedad con una sentencia, se consultan por estado, evento y fecha
sin un índice por combinación, y pueden escribirse en la misma transacción que el dato que
las origina.

**Los endpoints son pocos, son del cliente y se miran en vivo.** Reactividad, cercanía al
resto de la configuración de la entidad, y cero ganancia en moverlos.

## Consecuencias

- `publish()` hace **una lectura de Firestore por evento** para resolver los suscritos. Es
  una consulta pequeña y acotada; si algún día el volumen lo pide, se cachea con TTL corto,
  asumiendo que un cambio de configuración tarde unos segundos en surtir efecto. Hoy no hace
  falta y no se hace.
- La garantía transaccional cubre la entrega, no la lectura de endpoints: son dos almacenes
  distintos. Es la parte que importaba.
- Todas las operaciones sobre un endpoint **piden `entityId`**, porque la ruta en Firestore es
  por entidad. Efecto secundario bueno: es imposible tocar el endpoint de otro cliente
  conociendo solo su id.
- Al borrar un endpoint ya no se borran en cascada sus entregas. Correcto: el histórico de lo
  enviado no debería desaparecer porque alguien retire una URL. De ellas se encarga la purga.
- **El front no se toca en esta parte.** Su lista sigue leyendo `webhook_endpoints` de
  Firestore, en vivo, como hasta ahora.
- Migración `018` deshace la tabla que creó la `017`.

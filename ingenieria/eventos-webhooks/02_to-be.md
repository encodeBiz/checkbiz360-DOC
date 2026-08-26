# 02 — Arquitectura destino

Todo en `encodebiz-api`. `encodeBiz-SAAS` no recibe una línea más.

---

## 1. Dónde vive cada pieza

```
packages/shared/src/events/          ← el núcleo, reutilizable por cualquier servicio
  registry.ts                        catálogo: registro + consulta + metadatos por evento
  emit.ts                            publish(): valida, persiste en outbox, dispara entrega
  deliver.ts                         firma HMAC, POST, clasifica el resultado
  backoff.ts                         política de reintentos
  domain/                            Event, Endpoint, Delivery
  infrastructure/PgOutboxRepository.ts
  infrastructure/PgEndpointRepository.ts

services/events/                     ← servicio propio (puerto libre siguiente)
  worker de rescate (node-cron)      reintentos vencidos y huérfanos
  router de gestión                  CRUD de endpoints, catálogo, entregas, replay
  router S2S                         publish desde otros servicios que no importen shared

services/firebase_sdk/               ← residuo transitorio (ver ADR-006)
  solo triggers de Firestore para lo que todavía no escribe el contenedor
```

El núcleo en `shared` y no en el servicio es deliberado: quien emite es cada servicio, en su
propio caso de uso. El servicio `events` es el que gestiona, reparte lo pendiente y da la cara
al panel.

## 2. Emisión: donde ocurre la acción

**Regla:** el evento se emite en el caso de uso que escribe, inmediatamente después de que la
escritura sea firme.

```ts
await this.repository.save(task);
await publish("task.created", entityId, toTaskPayload(task));   // ← aquí
```

El trigger de Firestore deja de ser el mecanismo por defecto y queda solo para lo que no pasa
por el contenedor: escrituras que hace la app móvil directamente contra Firestore, o dominios
que todavía viven en Firebase. Ver [03_catalogo-de-eventos.md](./03_catalogo-de-eventos.md)
para el mapa exacto de qué lanzador va dónde hoy.

## 3. Entrega: en el acto, con red debajo

Corrección respecto al diseño original: el argumento de "no bloquear el fichaje" **no
sostenía** la cola. El fichaje escribe y devuelve; el trigger corre en otra invocación. Nada
del camino crítico dependía de la entrega.

Lo que sí sostiene la cola es otra cosa, más estrecha: **una invocación no puede esperar una
hora**, y el backoff llega a 3600 s. Y si el intento muere a mitad —proceso reciclado, timeout,
caída— sin registro durable el evento se perdió y nadie se entera.

De ahí el diseño:

1. `publish()` escribe la entrega en la outbox (durable, dentro de la transacción del caso de
   uso cuando el dato es de PostgreSQL).
2. **Se intenta entregar inmediatamente**, sin esperar a ningún ciclo. En el contenedor, sin
   bloquear la respuesta HTTP al usuario.
3. Solo lo que falla queda pendiente con su `next_attempt_at`.
4. Un worker de rescate recorre lo vencido. Deja de ser el repartidor: es la red.

Resultado: latencia de milisegundos en el caso normal, y las mismas garantías de durabilidad
que hoy. Ver [ADR-003](./adr/ADR-003-entrega-inmediata-outbox-como-rescate.md).

## 4. Almacenamiento: PostgreSQL

La outbox y los endpoints pasan a PostgreSQL, que es donde ya vive lo transaccional del
contenedor y donde se puede: escribir el evento en la misma transacción que el dato, mantener
un índice compuesto sin ceremonia, purgar por antigüedad con una sentencia y consultar el
histórico de entregas para el panel. Ver [ADR-004](./adr/ADR-004-outbox-en-postgres.md).

## 5. Lo que se arregla de paso

Cada punto responde a un límite del [01_as-is.md](./01_as-is.md) §6.

**Comodines en la suscripción.** `attendance.*` y `*` además del tipo exacto. Un evento nuevo
de una familia ya suscrita llega solo, sin que el cliente toque su configuración.

**Purga de la outbox.** Las entregas `delivered` se borran a los 30 días; las `dead` se
conservan 90 para poder reproducirlas. Configurable.

**El endpoint no se apaga por un 4xx.** Se apaga tras N entregas muertas consecutivas
(por defecto 20), y al apagarse se notifica. Un payload que le siente mal al consumidor no le
corta el resto del catálogo.

**Payload con forma propia.** Cada evento define su `data` explícitamente, mediante un mapeador
del modelo interno al externo. Nunca `{...entidad}`.

**Catálogo consultable.** `GET /api/v1/events/catalogue` devuelve el registry con nombre,
descripción, versión y ejemplo de payload por evento. Es lo que pinta el panel.

**Entregas visibles y reproducibles.** `GET /deliveries` con filtro por estado y evento, y
`POST /deliveries/:id/replay` para reintentar a mano lo que murió.

**Evento de prueba.** `POST /endpoints/:id/test` emite un `endpoint.test` contra esa URL para
que quien integra valide firma y conectividad sin esperar a que alguien fiche.

## 6. Idempotencia y entregas duplicadas

Al mover la entrega al momento de la acción, un reintento del trigger o del caso de uso puede
producir la misma entrega dos veces. Ya está cubierto por `evt_id` y la cabecera
`X-EncodeBiz-Event-Id`, pero **deja de ser teórico** y hay que documentarlo como obligación del
consumidor. Ver [04_contrato-publico.md](./04_contrato-publico.md).

## 7. Qué NO cambia

- El contrato de firma: HMAC-SHA256 sobre `"{t}.{body}"`, cabecera `t=<unix>,v1=<mac>`.
- El formato del sobre: `id`, `type`, `version`, `occurred_at`, `entity_id`, `data`.
- El modelo multi-tenant: endpoints por `entityId`, secreto por endpoint.
- La política de backoff `[0, 30s, 2m, 10m, 1h]`.

Quien ya integre contra el módulo actual no tiene que cambiar nada.

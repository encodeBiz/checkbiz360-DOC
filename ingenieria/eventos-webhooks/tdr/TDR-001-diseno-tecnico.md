# TDR-001 — Diseño técnico del módulo de eventos

**Fecha:** 2026-08-26
**Estado:** Diseño
**Autor:** Jose Acevedo
**Decisiones que implementa:** [ADR-001](../adr/ADR-001-modulo-en-el-contenedor.md) …
[ADR-006](../adr/ADR-006-firebase-sdk-residuo-transitorio.md)

---

## 1. Reparto de responsabilidades

| Pieza | Dónde | Qué hace |
|---|---|---|
| Núcleo | `packages/shared/src/events/` | Registry, `publish()`, entrega, firma, backoff, repositorios |
| Servicio | `services/events` (puerto **3012**) | Gestión de endpoints, catálogo, entregas, replay, worker de rescate |
| Triggers residuales | `services/firebase_sdk` | Lo que aún debe emitir desde Firebase; publica por HTTP contra `services/events` |

El núcleo va en `shared` porque **quien emite es cada servicio**: `checkinbiz`, `tasks`,
`documents`, `reports`, `billing` y `rentman` importan `publish()` y lo llaman en su caso de
uso. El servicio `events` no es un intermediario obligatorio: es el que gestiona, rescata y da
la cara al panel.

## 2. Esquema (migración `017_events.sql`)

```sql
CREATE TABLE webhook_endpoint (
  id                   TEXT PRIMARY KEY,              -- wh_<hex>
  entity_id            TEXT NOT NULL,
  url                  TEXT NOT NULL,
  secret               TEXT NOT NULL,                 -- whsec_<hex>
  enabled              BOOLEAN NOT NULL DEFAULT TRUE,
  subscribed_events    TEXT[] NOT NULL,               -- admite 'attendance.*' y '*'
  version              TEXT NOT NULL DEFAULT '2025-08-01',
  consecutive_failures INT NOT NULL DEFAULT 0,
  disabled_reason      TEXT,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (entity_id, url)
);

CREATE TABLE webhook_delivery (
  id              TEXT PRIMARY KEY,                   -- dly_<hex>
  endpoint_id     TEXT NOT NULL REFERENCES webhook_endpoint(id) ON DELETE CASCADE,
  entity_id       TEXT NOT NULL,
  event_id        TEXT NOT NULL,                      -- evt_<hex>
  event_type      TEXT NOT NULL,
  event           JSONB NOT NULL,                     -- el sobre completo, tal como se envía
  status          TEXT NOT NULL,                      -- pending|delivered|failed|dead
  attempt         INT NOT NULL DEFAULT 0,
  next_attempt_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_error      TEXT,
  last_status     INT,
  delivered_at    TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (endpoint_id, event_id)                      -- idempotencia del fan-out
);

CREATE INDEX ON webhook_delivery (status, next_attempt_at) WHERE status = 'pending';
CREATE INDEX ON webhook_delivery (entity_id, created_at DESC);
CREATE INDEX ON webhook_delivery (event_type, created_at DESC);
```

El `UNIQUE (endpoint_id, event_id)` es lo que hace que reemitir el mismo evento no genere dos
entregas: el segundo `INSERT` choca y se ignora.

El índice parcial sobre `pending` mantiene barata la consulta del worker de rescate por muchas
entregas históricas que haya.

## 3. El registry, con metadatos

El registry actual es un `Set<string>`. Con cincuenta eventos hace falta más, porque el panel
necesita pintar el catálogo y quien integra necesita saber qué recibe:

```ts
registerEvents([
  {
    type: "attendance.clock_in",
    since: "2025-08-01",
    description: { es: "Entrada válida registrada", en: "Valid clock-in recorded" },
    example: { checklog_id: "chk_…", employee_id: "emp_…", branch_id: "br_…",
               occurred_at: "2026-08-26T07:14:22Z", source: "mobile" },
  },
]);
```

Se sigue registrando por servicio y por efecto de import, como hoy: es el mecanismo que evita
que el núcleo conozca eventos concretos. `publish()` sigue rechazando lo no registrado, ahora
con el tipo declarado en un solo sitio.

## 4. `publish()`

```ts
export async function publish(
  type: string,
  entityId: string,
  data: unknown,
  opts?: { tx?: PoolClient; eventId?: string },
): Promise<void>
```

1. Valida `type` contra el registry. No registrado → lanza; es un error de programación.
2. Compone el sobre: `id`, `type`, `version`, `occurred_at`, `entity_id`, `data`.
3. Busca los endpoints habilitados de la entidad que casen por tipo exacto, por familia
   (`attendance.*`) o por `*`.
4. Inserta una fila de `webhook_delivery` por endpoint, **en la transacción del caso de uso** si
   se pasa `tx`.
5. Tras el commit, dispara la entrega sin esperarla (ADR-003). Si el proceso muere antes de
   intentarlo, la fila queda `pending` y la recoge el rescate.

`opts.eventId` permite que el llamante fije el identificador y consiga idempotencia de extremo a
extremo cuando reintenta.

## 5. Entrega

Sin cambios de contrato respecto al módulo actual: `POST` con `Content-Type: application/json`,
firma `t=<unix>,v1=<hmac_sha256("{t}.{body}")>` con el secreto del endpoint, cabeceras
`X-EncodeBiz-Event-Id`, `X-EncodeBiz-Signature` y `X-EncodeBiz-Retry`, timeout de 4 s.

Clasificación del resultado:

- `2xx` → `delivered`, `consecutive_failures = 0` en el endpoint.
- `0` (red/timeout), `408`, `429`, `5xx` → reintento con `[0, 30s, 2m, 10m, 1h]`, máximo 5.
- Cualquier otro código → `dead` sin más intentos.
- `consecutive_failures >= 20` → el endpoint se deshabilita con `disabled_reason` y se notifica.
  **Nunca por una sola entrega muerta**, que es el comportamiento actual.

## 6. Worker de rescate

`node-cron` dentro de `services/events`, cada 5 minutos:

```sql
SELECT * FROM webhook_delivery
 WHERE status = 'pending' AND next_attempt_at <= now()
 ORDER BY next_attempt_at
 LIMIT 500
 FOR UPDATE SKIP LOCKED;
```

`FOR UPDATE SKIP LOCKED` permite más de una instancia sin repartir dos veces la misma entrega.
Ya no es el camino normal, así que la frecuencia baja y el lote sube.

Purga diaria: `delivered` con más de 30 días y `dead` con más de 90. Configurable por variable
de entorno.

## 7. API de gestión (`/api/v1/events`)

| Método y ruta | Qué hace |
|---|---|
| `GET /catalogue` | Catálogo de eventos con descripción, versión y ejemplo |
| `GET /endpoints` | Endpoints de la entidad |
| `POST /endpoints` | Alta. Devuelve el secreto **una sola vez** |
| `PATCH /endpoints/:id` | URL, eventos suscritos, activar/pausar |
| `DELETE /endpoints/:id` | Baja |
| `POST /endpoints/:id/test` | Emite `endpoint.test` contra esa URL |
| `POST /endpoints/:id/rotate-secret` | Rota el secreto |
| `GET /deliveries` | Histórico con filtro por estado, evento y fecha |
| `POST /deliveries/:id/replay` | Reintenta una entrega muerta |
| `POST /publish` (S2S, API key) | Publicación desde fuera del contenedor — lo usa `firebase_sdk` |

Autenticación como el resto del contenedor: Firebase ID token para la gestión, API key para el
router S2S, en prefijos distintos para no repetir el error de doble montaje de `reports`.

## 8. Convivencia y corte

1. Se despliega el módulo nuevo con la doble escritura desactivada.
2. Se migran los `webhook_endpoints` de Firestore a PostgreSQL. La outbox **no** se migra: se
   drena lo pendiente antes del corte.
3. Los eventos nuevos salen ya por el módulo nuevo.
4. `onChecklogWebhook` se reapunta al router S2S y deja de escribir en Firestore.
5. Cuando no queda nada emitiendo desde el SaaS, se borra `core/webhook` de
   `encodeBiz-SAAS`.

## 9. Pruebas mínimas

- Publicar un tipo no registrado lanza.
- Un endpoint suscrito a `attendance.*` recibe un evento nuevo de esa familia sin tocar su
  configuración.
- Reemitir el mismo `event_id` al mismo endpoint no crea una segunda entrega.
- Un `500` reintenta con el backoff previsto; un `422` muere al primer intento.
- Veinte entregas muertas consecutivas deshabilitan el endpoint; diecinueve no.
- La firma que genera el emisor la verifica un consumidor de referencia con el cuerpo crudo.
- Si el proceso muere entre el `INSERT` y el envío, el rescate entrega la fila `pending`.

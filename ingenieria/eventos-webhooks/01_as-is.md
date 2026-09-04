# 01 — Cómo está hoy

**Fecha de la foto:** 2026-08-26 · Verificado contra código (`encodeBiz-SAAS@main`) y contra
producción (`firebase functions:list`).

> **Sigue siendo el presente, no el pasado.** A 2026-09-04 este módulo continúa desplegado en
> desarrollo —emisor, repartidor programado y endpoints de gestión— y lee **la misma colección
> de endpoints** que el módulo nuevo. Lo que aquí se describe convive hoy con
> [02](./02_to-be.md), y esa convivencia tiene una consecuencia concreta que hay que evitar:
> ver [07 §3.1](./07_estado-verificado.md).

---

## 1. Dónde vive

```
encodeBiz-SAAS/functions/src/
  core/webhook/
    domain/interfaces.ts     WebhookEvent<T>, WebhookEndpoint, WebhookDelivery
    registry.ts              catálogo global; cada servicio registra los suyos
    emit.ts                  publishEvent(): valida, asigna evt_id, hace fan-out a la outbox
    worker.ts                processWebhooks(): firma, POST, backoff, dead-letter
    backoff.ts               [0, 30s, 2m, 10m, 1h], MAX_ATTEMPTS = 5
    application/             Create/Delete/List/Toggle WebhookEndpoint
    infraestructure/         FirestoreWebhookEndpointRepository
    interfaces/              controladores HTTP de gestión
  core/shared/utils/signature.ts   sign() HMAC-SHA256 y generateWebhookSecret()
  services-saas/<servicio>/webhook-events.ts   catálogo del servicio + helper tipado
  services-saas/checkinbiz/firebase-firestore-trigger/onChecklogWebhook.ts   único emisor
```

El registro de eventos es **por efecto de import**: `index.ts` importa cada
`webhook-events.ts` y eso puebla el `Set` del registry. `publishEvent` rechaza cualquier tipo
no registrado.

## 2. Modelo de datos (Firestore)

```
entities/{entityId}/webhook_endpoints/{wh_id}   url, secret whsec_…, enabled, subscribedEvents[]
entities/{entityId}/webhook_outbox/{dly_id}     event, status, attempt, nextAttemptAt, lastError
```

Índice compuesto de grupo de colección sobre `webhook_outbox`: `status` + `nextAttemptAt`.

## 3. Flujo actual

1. La app o el back office escribe un checklog en Firestore.
2. `onChecklogWebhook` (trigger `onDocumentWritten`) ve la transición a `status: "valid"`,
   mapea `checkin → attendance.clock_in` / `checkout → attendance.clock_out` y llama al helper.
3. `publishEvent` valida el tipo contra el registry, asigna `evt_id`, `occurred_at` y
   `version`, y escribe **un documento de outbox por endpoint suscrito**.
4. `webhookWorker`, un `onSchedule("* * * * *")`, lee hasta 100 entregas pendientes vencidas,
   firma el cuerpo y hace `POST` con timeout de 4 s.
5. 2xx → `delivered`. 0/408/429/5xx → reintento con backoff. Resto o agotados → `dead`, y
   **el endpoint se desactiva**.

## 4. Catálogo actual

| Servicio | Eventos |
|---|---|
| checkinbiz | `attendance.clock_in`, `attendance.clock_out` |
| passinbiz | `pass.created(.failed)`, `pass.revoked`, `pass.sent(.failed)`, `credential.created(.failed)`, `credential.sent(.failed)`, `validation.scanned(.success/.failed)` |

`restin` / `restout` están mapeados a nada de forma deliberada (fuera de alcance de F1).

De los doce de passinbiz, ocho tienen emisor real: los `.created` desde
`createPassOnDemand.controller.ts`, los `.sent` desde el **worker de emails** —que llama a
`publishEvent` directamente, sin pasar por el helper tipado— y los `validation.scanned.*`
desde `ValidatePass.ts`. `pass.revoked` y el genérico `validation.scanned` no los emite nadie.

## 5. Desfase entre repositorio y producción

Comprobado el 2026-08-26:

| Función | dev (`dev-encodebiz`) | prod |
|---|---|---|
| `onChecklogWebhook` (emisor) | desplegada | **ausente** |
| `webhookWorker` | desplegada | desplegada |
| `createWebhookEndpoint` | desplegada | desplegada |
| `deleteWebhookEndpoint` | desplegada | desplegada |
| `listWebhookEndpoints` | desplegada | **ausente** |
| `toggleWebhookEndpoint` | desplegada | **ausente** |

Consecuencia: en producción **no se emite ni un solo evento de asistencia**. El worker corre
cada minuto sobre una outbox que nunca recibe nada, y el panel no puede listar ni pausar
endpoints. El código está en `main` desde el 24 de julio; lo que faltó fue el despliegue.

## 6. Límites reales del diseño actual

Ninguno estorba con catorce eventos. Todos estorban con cincuenta.

**Techo de reparto.** `limit(100)` por pasada de un minuto, para toda la plataforma, con
fan-out de una entrega por endpoint suscrito. El síntoma al saturar no es un error: es retraso
creciente y silencioso.

**Latencia de base.** Un cron de un minuto son ~30 s de latencia media aunque no haya carga.

**La outbox no se limpia.** Los `delivered` se acumulan indefinidamente: coste y degradación
de la consulta.

**Un 4xx aislado apaga el endpoint.** `enabled: false` al primer no reintentable. Con dos
eventos casi nunca ocurre; con un catálogo grande, un payload nuevo que le siente mal al
consumidor le corta *todo* lo demás sin avisar.

**Sin comodines.** `subscribedEvents` son cadenas exactas: el que quiera "todo lo de
asistencia" enumera, y cuando añades un evento nuevo no lo recibe ningún endpoint existente.

**El payload es un volcado interno.** `{checklogId, ...cl}` publica el documento tal cual, así
que cualquier refactor interno es un cambio de contrato para quien integra.

**El catálogo no se puede consultar.** `listRegistered()` existe y no la llama nadie: el panel
no tiene de dónde sacar la lista de eventos suscribibles.

**El emisor depende de Firestore.** Un trigger por colección observada. Lo que se escribe
desde el contenedor a PostgreSQL —tareas, documentos, informes, rentman— no tiene trigger que
lo vea.

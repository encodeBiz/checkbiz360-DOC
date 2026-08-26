# 06 — Integración en el front (contrato + prompt)

> Base: `{NEXT_BACKEND_URI_EVENTS_HANDLER}` → `/api/v1/events` · autenticación: Firebase ID token.
> Todo lo de aquí está **desplegado y verificado en desarrollo** (2026-08-26).

---

## 0. Lo que ya existe, y por qué no vale

El front **ya tiene** una pantalla de webhooks: `integration/tabs/tabWebHook`, con su formulario
de alta y su servicio en `services/core/integration.service.ts`. No se parte de cero: se
migra. Y hay tres cosas que dejan de funcionar solas, sin que nadie las rompa a propósito:

**La lista se lee de Firestore.** `fetchWebHookByEntity` hace `searchFirestore` sobre
`entities/{entityId}/webhooks`. Los endpoints ahora viven en PostgreSQL
([ADR-004](./adr/ADR-004-outbox-en-postgres.md)), así que esa consulta devolverá vacío. No es
un fallo que se vea: es una lista que se queda en blanco.

**El catálogo está cableado en el front.** `IWebHook.ts` declara
`WebhookEventType = "attendance.clock_in" | "attendance.clock_out"` y el formulario construye
el desplegable con esas dos cadenas. Con cincuenta eventos eso no se mantiene a mano: el
catálogo se pide al servidor.

**Faltan la mitad de las acciones.** No hay pausar, ni probar, ni ver entregas, ni reintentar,
ni rotar el secreto. Algunas ni existían antes; otras existían en el backend viejo y nunca se
llegaron a desplegar.

## 1. El contrato, endpoint por endpoint

Todos responden `{ok: false, error, …}` en el error, con el código en `error`.

| Llamada | Devuelve | Errores propios |
|---|---|---|
| `GET /catalogue` | `{ok, version, events}` | — |
| `GET /endpoints?entityId=` | `{ok, endpoints}` — secreto **enmascarado** | **400** `entityId_required` |
| `POST /endpoints` `{entityId, url, subscribedEvents, enabled?, description?}` | **201** `{ok, endpoint, secretShownOnce}` — el secreto **en claro, una sola vez** | **400** `url_must_be_https` · **400** `unknown_events` + `detail[]` · **400** `too_many_endpoints` + `max` · **409** `url_already_registered` |
| `PATCH /endpoints/{id}` `{url?, subscribedEvents?, enabled?, description?}` | `{ok, endpoint}` | **404** `endpoint_not_found` · las mismas de validación |
| `DELETE /endpoints/{id}` | `{ok}` | **404** `endpoint_not_found` |
| `POST /endpoints/{id}/test` | `{ok, eventId, status, lastStatus, lastError}` | **404** `endpoint_not_found` |
| `POST /endpoints/{id}/rotate-secret` | `{ok, secret, secretShownOnce}` | **404** `endpoint_not_found` |
| `GET /deliveries?entityId=&status=&eventType=&endpointId=&limit=` | `{ok, count, deliveries}` | **400** `entityId_required` |
| `POST /deliveries/{id}/replay` | `{ok, status}` | **409** `delivery_not_replayable` |

```jsonc
// GET /catalogue
{ "ok": true, "version": "2025-08-01",
  "events": [
    { "type": "attendance.clock_in", "status": "available", "since": "2025-08-01",
      "description": { "es": "Entrada válida registrada", "en": "Valid clock-in recorded" },
      "example": { "checklog_id": "chk_7f2a…", "employee_id": "emp_4c1b…", "is_suspect": false } }
  ] }
// status: "available" = ya lo emite alguien · "planned" = declarado y aún sin cablear

// endpoint (lista y PATCH: el secreto viene truncado, "whsec_1234…")
{ "id": "wh_…", "entityId": "…", "url": "https://…", "secret": "whsec_1234…",
  "enabled": true, "subscribedEvents": ["attendance.*"], "version": "2025-08-01",
  "description": null, "consecutiveFailures": 0, "disabledReason": null,
  "createdAt": "…", "updatedAt": "…" }

// delivery
{ "id": "dly_…", "endpointId": "wh_…", "eventId": "evt_…", "eventType": "attendance.clock_in",
  "event": { /* el sobre completo, tal como se envió */ },
  "status": "pending | delivered | failed | dead",
  "attempt": 1, "lastStatus": 200, "lastError": null,
  "nextAttemptAt": "…", "deliveredAt": "…" }
```

### Suscripción: tres formas

`subscribedEvents` admite el tipo exacto (`attendance.clock_in`), la familia
(`attendance.*`) y todo (`*`). **La familia es la opción que hay que empujar en la interfaz**:
es la que hace que un evento nuevo llegue solo, sin que el cliente vuelva a configurar nada.

---

## PROMPT

Rehaz la pantalla de **Webhooks** del área de integraciones. Ya existe, pero fue escrita
para un módulo con dos eventos y ahora el catálogo pasa de cincuenta.

### Lo que tiene que entender quien lo implemente

Un webhook es una llamada que **nosotros** hacemos al servidor **del cliente** cuando pasa
algo. El cliente no consulta: le avisamos. Eso cambia lo que la pantalla tiene que resolver,
porque el que integra necesita tres certezas que no puede obtener por su cuenta.

**Qué puedo recibir.** El catálogo. Nunca una lista escrita a mano en el front: se pide a
`GET /catalogue`, viene con descripción bilingüe y ejemplo de payload, y trae marcado qué se
emite ya y qué está declarado pero todavía sin cablear. Enseña las dos cosas, distinguidas —
prometer lo que aún no sale es peor que no anunciarlo.

**Está llegando de verdad.** El botón de probar. `POST /endpoints/{id}/test` dispara un evento
real, firmado, contra su URL, sin esperar a que nadie fiche. Es lo primero que necesita quien
integra y hoy no existe.

**Qué pasó con lo que ya salió.** El histórico de entregas, con su estado y su motivo de
fallo. Que el cliente pueda ver un `dead` con su `HTTP 500` en vez de escribir un correo
preguntando.

### La pantalla

**Lista de endpoints.** Por cada uno: la URL, a qué está suscrito, si está activo, y el
número de fallos seguidos si lo hay. Un endpoint puede venir **apagado por el servidor**
—`enabled: false` con `disabledReason`—: eso no es que el cliente lo pausara, es que
acumuló veinte entregas muertas. Dilo con esas palabras y ofrece reactivarlo con el `PATCH`,
que además pone el contador a cero.

**Alta.** URL (solo HTTPS, el servidor lo rechaza si no), descripción opcional y selector de
eventos construido desde el catálogo, agrupado por familia. Cada familia con su casilla de
"toda la familia" que envía `attendance.*` en vez de enumerar. Al crear, el servidor devuelve
el secreto **en claro y por única vez**: enséñalo en un bloque copiable, con la advertencia de
que no vuelve a aparecer, y no lo guardes en ningún sitio del front. Después solo se ve
truncado.

**Probar.** Un botón por endpoint. La respuesta trae `status` y `lastStatus`: si es
`delivered`, verde y a otra cosa; si no, enseña `lastError` tal cual — el mensaje del servidor
del cliente es exactamente lo que el cliente necesita leer para arreglarlo.

**Entregas.** Tabla filtrable por estado y por evento. Estado, evento, código HTTP e intentos.
Las `dead` con botón de reintentar (`replay`); las demás, no — el `409` está para eso.

**Rotar el secreto.** Devuelve uno nuevo en claro, misma regla que el alta. Advierte de lo
obvio antes de hacerlo: las peticiones firmadas con el viejo dejan de validar en cuanto rote.

### Lo que NO hace esta pantalla

No lee Firestore. Los endpoints y las entregas están en PostgreSQL y solo se llega a ellos por
la API. Si ves `searchFirestore` en el servicio de webhooks, eso es lo que hay que quitar.

No guarda el secreto. Ni en estado global, ni en almacenamiento local, ni en la URL, ni en
logs. Se muestra y se olvida.

No inventa el catálogo. Si un evento no está en `GET /catalogue`, no se ofrece.

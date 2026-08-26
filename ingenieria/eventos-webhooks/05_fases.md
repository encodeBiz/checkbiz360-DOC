# 05 — Plan de ejecución

Cinco oleadas. Cada una deja el sistema en un estado utilizable; ninguna depende de que la
siguiente llegue.

---

## Oleada 0 — Desatascar lo que ya existe

Lo más barato de todo y lo que más desbloquea, porque hoy en producción no se emite nada.

- Desplegar en producción las tres funciones ausentes: `onChecklogWebhook`,
  `listWebhookEndpoints`, `toggleWebhookEndpoint`.
- Retirar passinbiz del catálogo — los cuatro sitios de
  [03 §4](./03_catalogo-de-eventos.md#4-retirada-de-passinbiz), sin olvidar el worker de
  emails.
- Exponer el catálogo (`listRegistered()` ya escrita y sin usar) para que el panel pueda pintar
  el selector.

Al final de esta oleada la plataforma emite de verdad `attendance.clock_in` y `clock_out`, y
el panel funciona entero.

## Oleada 1 — El núcleo, en el contenedor

- `packages/shared/src/events/`: registry con metadatos, `publish()`, entrega, backoff.
- Migración de esquema: `webhook_endpoint`, `webhook_delivery` (ver
  [TDR-001](./tdr/TDR-001-diseno-tecnico.md)).
- `services/events`: router de gestión, worker de rescate, replay, `endpoint.test`.
- Comodines, purga, umbral de desactivación, mapeadores de payload.
- Doble escritura temporal: lo que emite Firebase sigue emitiendo; lo nuevo va al contenedor.

## Oleada 2 — checkinbiz completo

Todo el dominio `attendance`, `workday` e `issue`, con los lanzadores en los casos de uso del
contenedor. Los lanzadores están localizados todos ([03 §3](./03_catalogo-de-eventos.md#3-mapa-de-lanzadores));
lo único que queda por decidir antes de publicar es la normalización de `Issue.type`, que hoy se
escribe de dos formas distintas.

Al terminar, `onChecklogWebhook` se borra.

## Oleada 3 — Tareas y documentos

Los catorce eventos de `task.*` y `document.*`. Es la oleada más mecánica: un controlador por
acción, correspondencia uno a uno, cero incógnitas. Buen sitio para asentar el patrón de
mapeador de payload.

## Oleada 4 — Empleados, centros y horarios

`employee.*` sale directo del contenedor. `branch.*`, `schedule.*` y `calendar.*` necesitan que
antes se porte su CRUD, o pasan por `services/firebase_sdk` mientras tanto.

## Oleada 5 — Transversales

`report.generated`, `alert.raised`, `service.*`, `addon.*`, `invoice.*`. Son pocos y de dueños
distintos; van al final porque ninguno bloquea a nadie.

---

## Criterio de cierre

El módulo está terminado cuando `services/firebase_sdk` está vacío. Ese es el indicador de que
`encodeBiz-SAAS` ya no participa en la emisión de eventos.

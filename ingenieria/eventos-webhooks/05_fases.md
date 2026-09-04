# 05 — Plan de ejecución

Cinco oleadas. Cada una deja el sistema en un estado utilizable; ninguna depende de que la
siguiente llegue.

**Estado a 2026-09-04**, comprobado en desarrollo — ver [07](./07_estado-verificado.md) para la
evidencia. La oleada 1 está hecha y desplegada: el módulo entrega, medido de punta a punta.
Ese mismo día se cablearon los 32 lanzadores que ya tenían su escritura en el contenedor, lo
que cierra el grueso de la oleada 2 y, de paso, la 3 entera y la mitad de la 5. Está desplegado
en desarrollo y **comprobado evento a evento**: los 33 salieron, ver
[08](./08_prueba-de-los-33-eventos.md). El catálogo se recortó a esos 33 y el selector del panel
ya no ofrece lo que no emite.

---

## Oleada 0 — Desatascar lo que ya existe · *a medias*

Lo más barato de todo y lo que más desbloquea, porque hoy en producción no se emite nada.

- ✅ Desplegar las tres funciones ausentes: `onChecklogWebhook`, `listWebhookEndpoints`,
  `toggleWebhookEndpoint`. **Las tres están desplegadas en desarrollo** (`firebase
  functions:list --project dev-encodebiz`, 2026-09-04). En producción no se ha comprobado.
- ❌ Retirar passinbiz del catálogo — los cuatro sitios de
  [03 §4](./03_catalogo-de-eventos.md#4-retirada-de-passinbiz), sin olvidar el worker de
  emails. **Sin hacer:** `services-saas/passinbiz/webhook-events.ts` sigue existiendo, sigue
  importado en `functions/src/index.ts`, y `email-worker.ts` sigue llamando a `publishEvent`.
  El catálogo *nuevo* sí nace sin `pass.*`.
- ✅ Exponer el catálogo para que el panel pueda pintar el selector. Lo sirve
  `GET /api/v1/events/catalogue`.

El resultado que esta oleada prometía —«la plataforma emite de verdad `attendance.clock_in` y
`clock_out`»— **no se ha cumplido**, y no por lo que faltaba desplegar: el emisor viejo sí
está vivo, pero solo casa suscripciones por tipo exacto, así que un endpoint suscrito a
`attendance.*` no recibe nada. Está medido en [07 §2](./07_estado-verificado.md).

## Oleada 1 — El núcleo, en el contenedor · *hecha*

- `packages/shared/src/events/`: registry con metadatos, `publish()`, entrega, backoff.
- Migración de esquema (ver [TDR-001](./tdr/TDR-001-diseno-tecnico.md)). Aplicada en
  desarrollo: `017_events.sql` y `018_events_endpoints_a_firestore.sql`, que devuelve los
  endpoints a Firestore y deja solo `webhook_delivery` en Postgres.
- `services/events` (puerto 3012): router de gestión, worker de rescate cada cinco minutos,
  purga a las 04:30, replay, `endpoint.test`.
- Comodines, purga, umbral de desactivación, mapeadores de payload.
- Doble escritura temporal: lo que emite Firebase sigue emitiendo; lo nuevo va al contenedor.

Verificado en vivo: entrega de un `attendance.clock_in` en 158 ms con 200 del receptor.

## Oleada 2 — checkinbiz completo · *cableada salvo lo que sigue en Firebase*

Todo el dominio `attendance`, `workday` e `issue`, con los lanzadores en los casos de uso del
contenedor.

El alcance ha cambiado desde que se escribió este plan, y a mejor: en agosto los fichajes
todavía se creaban en Firebase, y hoy `createChecklog`, `updateChecklog` y
`requestManualChecklog` **ya viven en el contenedor** —comprobado por tráfico real, no por
lectura—. Eso convierte los diez eventos de `attendance` y `workday.closed` en un cableado
directo sobre `services/checkinbiz`, sin depender de nadie. Ver
[03 §3.1](./03_catalogo-de-eventos.md).

Hechos: los diez de `attendance` y `workday.closed`, con sus mapeadores en
`services/checkinbiz/src/events/`. Lo que sigue fuera del contenedor y necesita
`services/firebase_sdk`: `workday.incomplete` e `issue.opened`, que salen los dos del
`sanitizerChecklog`, y los otros tres de `issue`.

Dos condiciones antes de publicar:

- **`issue.opened` espera a la conversión de datos.** Las incidencias ya creadas conservan
  `journey_registration` en snake_case; publicarlas así le enseña dos tipos al integrador para
  el mismo hecho. Ver [03 §3.6](./03_catalogo-de-eventos.md).
- **`onChecklogWebhook` se borra en el mismo movimiento** en que se cablea `publish()` en
  `createChecklog.controller.ts`. Ni antes —deja de emitirse lo poco que se emite— ni después
  —se abre una ventana en la que un suscriptor por tipo exacto recibe cada fichaje dos veces,
  con dos firmas distintas—. Ver [07 §3.1](./07_estado-verificado.md).

## Oleada 3 — Tareas y documentos · *cableada*

Los catorce eventos de `task.*` y `document.*`. Es la oleada más mecánica: un controlador por
acción, correspondencia uno a uno, cero incógnitas. Buen sitio para asentar el patrón de
mapeador de payload.

Nota de la revisión: los catorce estaban ya en el contenedor, así que se hicieron a la vez que
la oleada 2 — no había ninguna dependencia que esperar, solo prioridad. Mapeadores en
`services/tasks/src/events/task.ts` y `services/documents/src/events/document.ts`.

## Oleada 4 — Empleados, centros y horarios

`employee.*` sale directo del contenedor. `branch.*`, `schedule.*` y `calendar.*` necesitan que
antes se porte su CRUD, o pasan por `services/firebase_sdk` mientras tanto.

Nota de la revisión: `calendar.*` **ya no espera a nadie** —el calendario se edita contra el
contenedor, con tráfico real— y `branch.*` sigue entero en Firebase. `employee.*` y
`schedule.*` tienen las dos implementaciones vivas a la vez, y eso hay que desempatarlo
mirando qué URL llama el panel antes de cablear nada. Ver
[03 §3.2](./03_catalogo-de-eventos.md).

## Oleada 5 — Transversales

`report.generated`, `alert.raised`, `service.*`, `addon.*`, `invoice.*`. Son pocos y de dueños
distintos; van al final porque ninguno bloquea a nadie.

Nota de la revisión: `report.generated`, los dos de `invoice` y los dos de `addon` ya están
cableados; se hicieron con la oleada 2 porque eran una línea cada uno. Quedan los dos de
`service`, que siguen en Firebase, y `alert.raised`, que no tiene hoy dónde emitirse —merlin no
tiene concepto de alerta en el código—: o se implementa el hecho de negocio o se retira del
catálogo.

---

## Criterio de cierre

El módulo está terminado cuando `services/firebase_sdk` está vacío. Ese es el indicador de que
`encodeBiz-SAAS` ya no participa en la emisión de eventos.

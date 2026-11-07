# Corregir una jornada de una vez · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS — CheckBiz360
**Dominio:** incidencias × fichajes × app del empleado
**Fecha:** 2026-11-07
**Estado:** Diseño cerrado el 2026-11-07
**Autor:** Jose Acevedo

---

## De dónde sale

Cuando una jornada se queda sin salida, el lote de jornadas incompletas
(`sanitizerChecklogs`) la cierra: marca como `incomplete_workday` **todos** los fichajes de esa
entrada (entrada, pausas y salida), fabrica la salida a la hora planificada y abre una
incidencia `journeyRegistration` por cada entrada sin cerrar. La incidencia solo lleva un
texto; el fichaje no está enlazado más que dentro de su id
(`incomplete_workday_{entityId}_{checkinId}`).

Arreglarla hoy:

1. La gestora lee la incidencia.
2. Va a Asistencia, busca a la persona y el día, y corrige **cada fichaje por separado**, con
   su motivo.
3. A la empleada le llega **un aviso por fichaje** y los acepta uno a uno.
4. La gestora vuelve a la incidencia y la cierra a mano: nada la cierra sola.

Una jornada partida de cinco tramos son cinco incidencias, una veintena de correcciones y otros
tantos avisos.

Jose, 2026-11-07: «lo veo como lo mismo que hay hoy paso a paso pero facilitado […] levantaría
un modal con estas dos o tres que hay en esa jornada y confirmaría cada una de las jornadas
incompletas y un solo motivo que se replique a todas, así lo haces todo con un solo click y en
un solo lugar. Lo mismo con la app: ahora el empleado debe aceptar notificación por jornada,
imagina una jornada partida de 5 turnos, qué caos».

## El principio

> **Se corrige la jornada, no el fichaje.** El circuito legal no cambia —la empresa propone,
> la persona acepta— pero se hace una vez por jornada: un modal, un motivo, un aviso, un sí.

Nada nuevo en el sentido de la aprobación: sigue siendo la empresa quien corrige y la
trabajadora quien da conformidad, como exige el registro de jornada.

## Qué es «la jornada»

El día local de una entrada (en la zona del propio fichaje: `metadata.tz`, después
`metadata.etz`, después la de la sucursal) para esa persona. Entran **todas** las entradas de
ese día y, con cada una, los fichajes que cuelgan de ella (`checkin == id`). Un turno de noche
que cruza las 00:00 va con el día de su entrada.

La jornada se calcula en el servidor, siempre desde una entrada concreta. El panel no decide
qué fichajes son de qué día: los pide.

## Panel: el modal «Corregir jornada»

En el detalle de una incidencia de jornada incompleta (id con prefijo
`incomplete_workday_`) aparece **Corregir jornada**. Abre un modal con la jornada entera,
tramo a tramo:

- Cada tramo con su casilla. Vienen marcados los que tienen algún fichaje incompleto.
- Dentro de cada tramo, sus fichajes con la hora editable. La salida que puso el sistema se
  distingue («puesta por el sistema a la hora planificada»).
- Un único **motivo**, que se copia a todos los fichajes corregidos.
- **Corregir y enviar**: un clic.

Los fichajes de un tramo marcado viajan **todos**, cambie su hora o no: así la jornada entera
sale de `incomplete_workday` cuando la persona acepta, no solo la salida. Un tramo con algo ya
pendiente de validar no se puede volver a enviar hasta que se resuelva.

Mientras espera, la incidencia dice «Corrección enviada, esperando a {persona}». Si la rechaza,
lo dice con su motivo y se puede volver a corregir. Si la acepta, **todas** las incidencias de
esa jornada se cierran solas.

## App: un aviso, una aceptación

Un único push por jornada: «Han corregido tu jornada del {día} ({n} fichajes)». En la bandeja
la jornada es **una sola tarjeta**. Al abrirla se ve el día con el antes y el después de cada
fichaje y dos botones: **Aceptar** todo o **Rechazar** con motivo.

**Todo o nada.** Si rechaza, la jornada entera vuelve a la gestora. Así no quedan jornadas a
medio validar.

## Cómo, por detrás

### Endpoints (checkinbiz)

Cuelgan de `/checklogs/update` para reutilizar el handler del proxy del panel y su variable de
entorno (`NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_LOG`), sin tocar Vercel.

| Método y ruta | Quién | Qué |
|---|---|---|
| `GET /checklogs/update/workday?entityId&employeeId&checkinId` | gestora (puede escribir en la empresa) | La jornada: día, zona, tramos con sus fichajes y si hay algo pendiente |
| `POST /checklogs/update/workday` | gestora | Propone la corrección de los fichajes enviados, con un motivo |
| `POST /checklogs/update/workday/respond` | la propia empleada | Acepta o rechaza la jornada entera |

Propuesta:

```json
{ "entityId", "employeeId", "checkinId", "reason",
  "corrections": [{ "id": "<checklogId>", "timestamp": "<ISO>" }] }
```

- Cada id tiene que ser de esa jornada y de esa persona. Si no, devuelve 400 `workday_correction/foreign_checklog`.
- Ninguna hora puede ser futura (misma regla y holgura que `/update`).
- Si algún fichaje está ya `pending-employee-validation`, devuelve 409 `workday_correction/pending_exists`.
- Admite hasta 100 fichajes.

Respuesta de la empleada:

```json
{ "entityId", "employeeId", "groupId", "accept": true|false, "rejectionReason"? }
```

### El lote de corrección

`entities/{entityId}/workdayCorrections/{groupId}`:

```text
{ employeeId, branchId, date, timeZone, checkinIds[], reason,
  items: [{ checklogId, updateId }],
  state: "pending" | "accepted" | "rejected" | "partial",
  requestedBy, requestedAt, resolvedBy?, resolvedAt?, rejectionReason? }
```

Cada fichaje recibe una entrada normal en `metadata.requestUpdates` (la misma forma que escribe
`/update`, con `previousStatus` y `previousDate`), más un campo `groupId`. Todo se escribe en un
único *batch*: o se propone la jornada entera o nada.

**Aceptar** aplica cada propuesta como `/update`: la hora propuesta, `status: valid` y
`requestUpdate`. **Rechazar** devuelve cada fichaje a su `previousStatus` (HAL-15). Una
jornada incompleta rechazada sigue incompleta y su incidencia sigue abierta. Las dos cosas van
en una transacción y son idempotentes: un lote que ya no está `pending` responde 409.

Los eventos de corrección (`emitCorrectionRequested` / `emitCorrectionResolved`) se emiten **por
fichaje**, igual que hoy. Lo que se mide de las correcciones no cambia.

### Incidencias

El cierre **no escribe respuestas** en la incidencia. Cada respuesta dispara un push a la otra
parte (`onIssuesResponse`), y se volvería a la lluvia de avisos. Va como campos de la propia
incidencia:

- al proponer: `correction: { groupId, state: "pending", requestedAt, requestedBy }`;
- al aceptar: `state: "resolved"` y `correction.state = "accepted"`, en **todas** las
  incidencias de las entradas del lote (`incomplete_workday_{entityId}_{checkinId}`);
- al rechazar: `correction.state = "rejected"` con `rejectionReason`; la incidencia sigue `in_review`.

Las incidencias antiguas sirven tal cual: la entrada sale del id. El lote de jornadas
incompletas no se toca.

### Avisos y compatibilidad con la app publicada

La app publicada solo sabe aceptar fichaje a fichaje desde la bandeja (`in_app_notifications`
de tipo `update_checklog_pending`). Para no romperla:

- **Un solo push** por lote, con el texto de la jornada.
- **En la bandeja, un aviso por fichaje**, como hoy, de tipo `update_checklog_pending`, cada uno
  con su `updateId` **y el `groupId`**.
- La app publicada los ve como hoy: puede aceptarlos uno a uno, y el push ya es solo uno.
- La app nueva junta los avisos con el mismo `groupId` en una tarjeta y responde con
  `/workday/respond`.
- El servidor marca `validationStatus` de todos los avisos del lote al responder.

Si la empleada responde fichaje a fichaje con la app vieja, `/update` lo aplica como siempre.
Cuando el último fichaje del lote queda resuelto, el lote se da por cerrado:

- `accepted` si todos se aceptaron, y entonces cierra las incidencias;
- `rejected` si todos se rechazaron;
- `partial` si hay de las dos cosas, y entonces las incidencias quedan abiertas.

## Fuera

- Corregir desde Asistencia o jornadas que no sean incompletas. El mecanismo vale para
  cualquier día, pero se empieza solo por la incidencia.
- Aceptar un tramo y rechazar otro desde la app nueva.
- Cambiar el lote de jornadas incompletas (sigue fabricando la salida y la incidencia como hoy).

## Orden

1. API (checkinbiz + una clave de mensaje en `shared`).
2. Panel: el modal en el detalle de la incidencia. Ya sirve con la app publicada.
3. App: la tarjeta agrupada y la pantalla de la jornada. Sale con la próxima versión.

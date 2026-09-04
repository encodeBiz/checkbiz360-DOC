# 08 — Los 33 eventos que salen, y cómo se comprueba que salen

**Ejecutado el:** 2026-09-04 · **Entorno:** desarrollo · **Sonda:**
`services/events/scripts/probe-events.js`

Los 33 eventos marcados `available` en el catálogo tienen lanzador cableado. Este documento
dice **cuáles son, qué acción dispara cada uno y cómo se provoca esa acción** — y deja el
resultado de haberlo hecho de verdad, no de haberlo leído.

La sonda no es un test unitario. Hace acciones reales contra el entorno de desarrollo —ficha,
corrige fichajes, crea tareas, sube documentos, conecta el add-on, manda un webhook firmado de
Stripe— y después se mira `webhook_delivery`. Es la única forma de comprobar un lanzador: lo
que puede fallar no es el `emit()`, es que la línea esté en el camino equivocado del
controlador, y eso no lo ve ningún tipo.

---

## 1. Resultado

**Los 33 tipos se emitieron. 49 de las 50 entregas salieron con 200 a la primera**, entre 45 y
265 ms, con la mediana en torno a los 90 ms.

La que falta es un `invoice.issued` que el receptor rechazó con **429: «Request limit exceeded.
Sign up to unlock more requests»**. El receptor de esta prueba era un bin gratuito de
webhook.site y la tanda agotó su cuota. No es un fallo de la plataforma ni del lanzador —el
evento se emitió y se encoló como los demás—, sino del buzón que lo recibía.

Y sirvió para ver funcionar la maquinaria que nadie prueba a propósito: la entrega quedó
`pending`, el rescate la reintentó cinco minutos después (intento 2, mismo 429, porque la cuota
sigue agotada) y seguirá con el backoff `[30s, 2m, 10m, 1h]` hasta morir como `dead`. Desde ahí
se reproduce a mano con `POST /api/v1/events/deliveries/:id/replay` cuando el receptor vuelva a
aceptar.

**Consecuencia práctica:** para probar en serio hace falta un receptor sin cuota. Un bin
gratuito de webhook.site aguanta la demostración, no la tanda entera.

## 2. Los 33, y qué los dispara

### attendance — 10 eventos · `services/checkinbiz`

| Evento | Qué acción lo dispara | Cómo lo provoca la sonda |
|---|---|---|
| `attendance.clock_in` | Entrada válida | `POST /checkinbiz/checklogs` con `type: "checkin"` |
| `attendance.clock_out` | Salida válida | ídem con `type: "checkout"` |
| `attendance.break_start` | Inicio de descanso | ídem con `type: "restin"` |
| `attendance.break_end` | Fin de descanso | ídem con `type: "restout"` |
| `attendance.clock_rejected` | El fichaje se rechaza en el acto | Fichar dos entradas seguidas → `two_type_followed`. También lo disparan la valla, el fuera de turno y el día sin turnos |
| `attendance.clock_flagged` | El fichaje cuenta pero queda señalado | Sale solo: una jornada de minutos entra en «menos de 3 horas» y `CreateChecklog` marca `isSuspect` |
| `attendance.manual_requested` | Alta de jornada manual desde el back office | `POST /checklogs/manual-request` con `date`, `checkinAt`/`checkoutAt` en `HH:mm` |
| `attendance.correction_requested` | Se propone una corrección | `POST /checklogs/update` con el token del administrador y un `reason` |
| `attendance.correction_accepted` | El empleado la confirma | `POST /checklogs/update` con el token **del empleado**, el `updateId` y `status: "valid"` |
| `attendance.correction_rejected` | El empleado la rechaza | ídem con `status: "failed"` y `rejectionReason` |

Los tres de corrección necesitan **dos identidades distintas**: el administrador propone y el
empleado resuelve. La sonda acuña las dos con `createCustomToken` y las canjea por ID tokens.

### workday — 1 evento · `services/checkinbiz`

| Evento | Qué acción lo dispara | Cómo lo provoca la sonda |
|---|---|---|
| `workday.closed` | El checkout que cierra la entrada | Sale con el `clock_out`. Lleva las horas ya calculadas: brutas, descanso del centro y netas |

### calendar — 2 eventos · `services/checkinbiz`

| Evento | Qué acción lo dispara | Cómo lo provoca la sonda |
|---|---|---|
| `calendar.holiday_changed` | Alta o borrado de un festivo, en cualquiera de los tres ámbitos | `POST /checkinbiz/calendar` con `holiday`, y `DELETE` con `kind: "holiday"` |
| `calendar.preset_saved` | Se guarda el calendario como plantilla | `POST /checkinbiz/calendar?action=savePreset` |

### task — 10 eventos · `services/tasks`

| Evento | Qué acción lo dispara | Cómo lo provoca la sonda |
|---|---|---|
| `task.created` | Alta de tarea | `POST /tasks` |
| `task.assigned` | Se asigna a uno o varios trabajadores | `POST /tasks/:id/assignments` |
| `task.unassigned` | Se retira a un trabajador | `DELETE /tasks/:id/assignments/:employeeId` |
| `task.updated` | Cualquier edición | `PATCH /tasks/:id` — el evento lleva `changed_fields` |
| `task.status_changed` | Cambio de estado | `PATCH /tasks/:id/status` |
| `task.note_added` | Nota nueva | `POST /tasks/:id/notes` |
| `task.resource_uploaded` | Evidencia subida | `POST /tasks/:id/resources`, multipart con `entityId`, `branchId`, `type` y `file` |
| `task.validated` | Se da por buena | `POST /tasks/:id/validation` — la tarea tiene que estar `completed` |
| `task.rejected` | Se rechaza | `POST /tasks/:id/rejection` — hace falta una **segunda** tarea: la primera ya se validó |
| `task.worker_rated` | Se puntúa al trabajador | `POST /tasks/:id/ratings` |

### document — 4 eventos · `services/documents`

| Evento | Qué acción lo dispara | Cómo lo provoca la sonda |
|---|---|---|
| `document.created` | Alta | `POST /documents`, multipart con el fichero |
| `document.updated` | Edición | `PATCH /documents/:id` |
| `document.acknowledged` | Acuse de recibo — el que tiene valor legal | `POST /documents/:id/ack` con el token **del empleado**; el documento se crea con `requiresAcknowledgement` y ámbito de empleado |
| `document.archived` | Archivado | `DELETE /documents/:id` |

### Transversales — 5 eventos

| Evento | Servicio | Qué acción lo dispara | Cómo lo provoca la sonda |
|---|---|---|---|
| `report.generated` | reports | Informe legal generado | `POST /api/reports/generate`. Si el rango no tiene jornadas devuelve 204 y **no** emite, que es lo correcto |
| `invoice.issued` | billing | Stripe finaliza la factura | Webhook `invoice.finalized` firmado con el secreto del entorno |
| `invoice.payment_failed` | billing | Falla el cobro | Webhook `invoice.payment_failed` |
| `addon.connected` | rentman | Se conecta el add-on | `POST /rentmanbiz/activate` y luego `/connect` con el token de la cuenta de pruebas |
| `addon.disconnected` | rentman | Se retira la credencial | `POST /rentmanbiz/disconnect` |
| `endpoint.test` | events | Disparo de prueba del panel | `POST /events/endpoints/:id/test` |

Sobre la factura sintética: va con `livemode: true` **a propósito**. La clave de desarrollo es
de pruebas, así que `SendInvoiceEmail` la descarta por modo distinto y no se manda ningún
correo a nadie. El evento se emite después de ese descarte, que es justo lo que se quería
comprobar.

## 3. Lo que la sonda no cubre, y por qué

Los otros 20 no están en el catálogo: quedaron comentados en `catalogue.ts` con lo que hay que
portar en cada caso, porque no hay nada que probar todavía.

- **12** tienen su escritura en Firebase (`issue.*`, `workday.incomplete`, `branch.*`,
  `service.*`, `employee.responsibility_changed`). Ver [03 §3.3](./03_catalogo-de-eventos.md).
- **7** tienen el camino duplicado —`employee.*` y `schedule.*`— y hay que desempatar cuál usa
  el panel antes de cablear. Ver [03 §3.2](./03_catalogo-de-eventos.md).
- **1**, `alert.raised`, no tiene hoy dónde emitirse.

## 4. Cómo repetirla

La sonda no se despliega: se copia dentro del contenedor y se ejecuta ahí, que es donde están
las credenciales y la red.

```bash
scp services/events/scripts/probe-events.js almalinux@<host>:/tmp/probe.js
ssh almalinux@<host> 'docker cp /tmp/probe.js encodebiz-api-dev-events-1:/app/probe.js'
ssh almalinux@<host> "cd /opt/encodebiz-api-dev && \
  docker compose -f docker-compose.staging.yml -p encodebiz-api-dev \
  exec -T -e PROBE_PHASE=all events node /app/probe.js"
```

`PROBE_PHASE` admite `subscribe`, `attendance`, `calendar`, `tasks`, `resource`, `documents`,
`report`, `addon`, `billing`, `endpoint` o `all`. La de `billing` corre en el contenedor de
billing —es el que tiene el secreto del webhook— y la de `addon` necesita `RENTMAN_TOKEN`.

El recuento, después:

```sql
SELECT event_type, count(*) AS n, count(*) FILTER (WHERE status = 'delivered') AS ok
  FROM webhook_delivery GROUP BY event_type ORDER BY event_type;
```

### Dos cosas que hay que saber antes de correrla

**Escribe datos que se quedan.** Fichajes, dos tareas, un documento archivado, una jornada
manual y un festivo que se crea y se borra. Todo va marcado `[sonda]` en los textos libres. En
desarrollo es aceptable; en producción no se corre.

**Necesita el endpoint suscrito a `*`.** Con `attendance.*` solo se verían once de los treinta
y tres: el resto de familias no llegarían a encolarse siquiera, porque `publish()` sale antes
si nadie está suscrito. La fase `subscribe` lo pone, y conviene devolverlo a lo que estaba
cuando se termine.

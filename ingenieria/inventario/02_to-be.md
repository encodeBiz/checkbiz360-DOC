# 02 — Arquitectura objetivo (To-Be)

## Principio

> **Un solo camino de escritura.** La app y el panel hablan con `inventory` por HTTP;
> `inventory` escribe el movimiento y el saldo juntos, en una transacción de Firestore, y
> copia el movimiento a Postgres en la misma petición. Firestore lleva el instante; Postgres,
> el histórico.

«Instante» significa lo que el admin ve al abrir el inventario: *en Vallecas hay 30 toallas,
20 comprometidas; la fregadora #2 está ahora en el Lidl Sur y el jueves reservada para
Arendel*. Nada más. Todo lo demás es lo que produce esos números.

## Topología destino

```
                 ┌───────────────────── encodebiz-api (un solo servidor) ─────────────────────┐
  app móvil  ─┐  │  nginx                                                                      │
  panel web   ┼─▶│   location /api/v1/inventory/ ─▶ inventory_service (inventory:3016)         │
              │  │                                    │                                        │
              │  │                                    ├──▶ Firestore (Admin SDK)  ← el instante│
              │  │                                    └──▶ Postgres (red interna) ← el espejo  │
              │  │                                    ▲                                        │
              │  │   events (publish) ── entrega interna S2S ─┘  task.status_changed / validated │
              │  │   location /api/v1/tasks/     ─▶ tasks:3006                                 │
              │  │   location /api/reports/      ─▶ reports:3005                               │
              │  └───────────────────────────────────────────────────────────────────────────┘
              │
              └──────── Firestore (Google) — lectura en vivo desde el panel ─────────────
```

`postgres` no tiene `ports:` en el compose: solo se alcanza desde la red de contenedores. El
único tramo que sale de la máquina es Firestore.

## El servicio `inventory`

Espeja a `tasks` y `billing`. Puerto **3016** — el 3015 es `entities` y es el último ocupado.

```
services/inventory/            puerto 3016
  src/app.ts                   Express: cors + json + /health + routers en /api/v1/inventory
  src/server.ts                listen(3016); Firestore vía @encodebiz/shared + pool de Postgres
  src/interfaces/http/         warehouse · item · unit · stock · task-material · board · movement
  src/interfaces/http/internal/  endpoint S2S que recibe las entregas de task.* (TDR-002 §6)
  src/application/use-cases/
  src/infrastructure/          Firestore*Repository + PgMovementMirror (escritura) + Pg*Reader
  src/jobs/                    remirror (reintento del espejo) · recompute (recálculo de saldos)
  Dockerfile                   copia del de tasks (EXPOSE 3016)
```

El dominio —entidades e interfaces— vive en `@encodebiz/shared`, bajo
`packages/shared/src/checkbiz/inventory/`, junto al resto del dominio de checkbiz.

## Un solo camino de escritura

La app **no escribe en Firestore** —no lo hace hoy para nada, y no va a empezar por esto—. Cada
salida, consumo o devolución es una llamada HTTP a `inventory` con un `movementId` que genera
la app. `inventory`:

1. Resuelve actor, permisos y almacén.
2. En **una transacción de Firestore**: si el `movementId` ya existe, devuelve lo que hay y no
   toca nada; si no, escribe el movimiento y aplica el delta al saldo.
3. Tras confirmar, inserta el movimiento en Postgres con `ON CONFLICT DO NOTHING`, **a mejor
   esfuerzo**: si Postgres no responde, la petición no falla y el movimiento queda
   `mirrored: false` para el job.

El `movementId` de cliente cuesta una línea y compra la idempotencia de un reintento de red:
si la petición se corta y Dio la repite, el segundo intento es el mismo apunte. Es el mismo
criterio que el `eventId` de `publish()`.

## Reparto del dato

### Firestore — el instante

| Qué | Por qué ahí |
|---|---|
| Artículos, almacenes, ejemplares | Maestros que el panel edita y lee en vivo |
| Existencias (`onHand` / `committed`) | Es el número que se mira |
| Agenda de los ejemplares | Reservas y huecos de no disponibilidad |
| Material de las tareas **abiertas** | «Salieron 30, llevas 20 declaradas» es estado actual, no historia |
| Movimientos | Se escriben aquí, en la misma transacción que el saldo |

### Postgres — el histórico

| Qué | Tabla | Quién lo escribe |
|---|---|---|
| Espejo de maestros | `dim_items`, `dim_warehouses`, `dim_item_units` | `SyncDimensions` en `analytics`, como las demás |
| Libro completo de movimientos | `item_movements_raw` | `inventory`, en la petición + job de reintento |
| Historial de ocupación | `unit_reservations_raw` | `inventory`, ídem |

Los informes —consumo por tarea, empleado, sucursal y periodo; coste; ocupación— se sirven
desde aquí. **El libro es un informe más.**

### Por qué Firestore para el instante

Es una decisión de **coherencia, no de necesidad**. Con un solo camino de escritura en
servidor, Postgres podría llevar el libro y el saldo en una transacción SQL y proyectar el
número a Firestore; la revisión del 2026-09-28 lo dejó sobre la mesa como viable. Se elige
Firestore porque ahí vive el resto del dominio de checkbiz, el panel lo lee en vivo, y meter la
primera entidad de dominio en Postgres haría de inventario el raro. Si algún día pesa más otra
cosa, es una decisión que se puede revisar sin drama. Ver
[ADR-005](./adr/ADR-005-instante-firestore-historico-postgres.md).

### La regla que gobierna la frontera

> **Lo que viaje entre los dos lados tiene que poder reconstruirse desde el otro.**

El movimiento está en los dos sitios: en Firestore porque es donde se escribe, en Postgres
porque es donde se consulta. Perder una inserción en Postgres retrasa un informe hasta que el
job la reintenta; nunca pierde un apunte. Y de ahí la prohibición operativa: **no se poda nada
de Firestore hasta que el espejo esté confirmado** (`mirrored: true`). En v1 no se poda de
todos modos.

## Por qué un servicio propio y no dentro de `tasks`

Tres razones, desarrolladas en [ADR-001](./adr/ADR-001-servicio-inventory-add-on-de-pago.md):

1. Es un **add-on que se contrata**. Un proceso aparte hace que la puerta de suscripción sea
   trivial de imponer y el módulo trivial de apagar.
2. Tiene **ritmo propio**: avisos de mínimo, recálculo de saldos, reintento del espejo.
3. `tasks` ya es grande, y el acoplamiento iría en la dirección equivocada.

## Quién habla con quién

`inventory` es dueño de su dato y **`tasks` no sabe que existe**. La app habla directamente con
`inventory` pasándole el `taskId`.

Para enterarse de lo que pasa con la tarea, `inventory` **no escucha un bus**, porque no lo
hay: `publish()` es un sistema de webhooks salientes que vuelve sin encolar si el cliente no
tiene endpoints. La forma es un **suscriptor interno**: la resolución de suscriptores devuelve,
además de los del cliente, un endpoint S2S hacia `inventory` para `task.*`. Hereda firma,
`webhook_delivery`, backoff y rescate. `inventory` responde 204 rápido a las entidades sin
suscripción y es idempotente por entrega, porque las entregas se reintentan.

Los eventos que consume son **los tres que existen**: `task.status_changed` (con `status` y
`previous_status`), `task.validated` y `task.rejected`. El detalle de qué hace con cada uno, y
las tres trampas del control de estado, en [TDR-002 §6](./tdr/TDR-002-saldos-movimientos-y-conciliacion.md).

Lo único que este módulo toca fuera de su casa es un valor nuevo en el enum de `TaskActivity`
(`item_consumed`), en `shared`. Aditivo, una línea.

## Auth

Doble vía, idéntica a la de `tasks`: **Firebase ID token** para el panel y **staff JWT** para la
app. Los permisos siguen la escala de responsabilidad ya existente, `admin` incluido. El
endpoint interno usa la autenticación S2S que ya emplean campañas.

## La puerta de suscripción

Middleware en `inventory`, antes de cualquier ruta que no sea `/health` ni la interna:

```
entities/{entityId}/subscriptions/inventory   → { plan, status }
```

Una sola comprobación: suscripción en `active` o `trialing` → si no, **403**
`inventory/not_subscribed` (403 y no 402: la plataforma no usa 402 y un código nuevo obliga a
tocar el proxy del panel y Dio; el código en el cuerpo basta para que el panel ofrezca el alta).

No hay un «módulo activado» aparte de la suscripción: contratar es activar. Y **no hay
límites que comprueben nada: un límite de plan nunca para el servicio.** Si una empresa se
pasa de lo que sea, se le cobra; no se le impide dar de alta una fregadora a mitad de turno.
Por eso el módulo lee la suscripción y nunca el plan — el plan es cosa de `billing`.

**El precio es 29 € al mes hasta 50 empleados y 0,75 € por cada empleado a partir del 51**,
y **no se elige**: hay un único plan, `standard`, y el precio reacciona solo a la plantilla.
Es un precio con tramos graduados en Stripe sobre la cantidad de empleados, así que `getCount`,
el recuento al fin de prueba y los 15 días de prueba (`BILLING_TRIAL_DAYS=15`; el 45 es solo
el valor por defecto del código) funcionan tal cual.
Sin tope de ejemplares. **Nunca por movimiento**:
sería ponerle precio a la acción que el módulo necesita que el operario repita veinte veces al
día. Ver [06 §D2](./06_decisiones-abiertas.md).

## Sin conexión — fase posterior

No hay offline en v1. Cuando se retome, la forma es un *outbox* local en la app: copia de la
petición en el almacenamiento del dispositivo si no hay red o la API falla, aviso al operario, y
reenvío idempotente al recuperar cobertura. Dos cosas quedan preparadas desde ahora para no
tocar el contrato entonces: el `movementId` de cliente y un `occurredAt` opcional en las rutas
de salida y consumo. Ver [06 §D3](./06_decisiones-abiertas.md).

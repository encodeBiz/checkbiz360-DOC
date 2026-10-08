# ADR-001 — Servicio `inventory` dedicado, contratable como add-on de pago

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Dos clientes piden inventario. La pregunta de partida era doble: dónde vive el código y si el
módulo se cobra aparte.

Sobre lo segundo hay precedente cerrado: la integración de Rentman se diseñó como **add-on de
pago** con entitlement propio, en paridad con checkbiz y passbiz
([rentman-integration/04](../../rentman-integration/04_activacion-saas.md)). Reutilizar ese
motor es gratis; inventar una monetización nueva, no.

Sobre lo primero había tres caminos:

**A — Dentro de `tasks`.** El inventario se consume desde la tarea, así que el acoplamiento es
natural y no hay servicio nuevo que montar.

**B — Dentro de `checkinbiz`.** Es el servicio del dominio.

**C — Servicio propio `inventory:3016`.**

## Decisión

**Opción C**, y el módulo se cobra como add-on mensual sobre checkinbiz.

## Justificación

**Un proceso aparte hace la puerta trivial.** Un add-on que se contrata necesita una frontera
donde comprobar el entitlement. Si el código vive dentro de `tasks`, esa comprobación se
esparce por rutas que también sirven a clientes que no lo han contratado, y basta olvidarla en
una para regalar el módulo. Con servicio propio es un middleware delante de todo.

**Se puede apagar.** Quitar la suscripción tiene que dejar de servir el inventario **sin**
tocar tareas ni fichaje. Eso solo es limpio si el módulo es un proceso.

**Tiene ritmo propio.** Avisos de mínimo, recálculo de saldos y reintento del espejo son
trabajo de fondo que no pinta nada en el camino HTTP de una tarea.

**`tasks` ya es grande** y el acoplamiento iría en la dirección equivocada: el núcleo pasaría a
depender de un módulo opcional.

## Consecuencias

- Puerto **3016** (el 3015 es `entities`). Bloque en compose, upstream y location en nginx.
- `inventory` es dueño de su dato; **`tasks` no lo conoce**. La app llama a `inventory` con el
  `taskId`.
- Para reaccionar a la tarea, `inventory` **no escucha un bus** —`publish()` es un sistema de
  webhooks salientes y no encola nada si el cliente no tiene endpoints—. Se engancha como
  **suscriptor interno** en la resolución de suscriptores, con endpoint S2S, y hereda la cola,
  la firma y los reintentos de `webhook_delivery`. Consume los tres eventos que existen:
  `task.status_changed`, `task.validated`, `task.rejected`.
- Lo único que este módulo toca fuera de su casa es un valor nuevo en el enum de
  `TaskActivity` (`item_consumed`), en `shared`. Aditivo, una línea.
- Alta del servicio: `inventory` en el tipo `SERVICES` de `shared` y en `OUR_SERVICES` de
  `billing`, planes en `service/inventory/plan/*` y precio en Stripe. **No hay trigger que
  portar**: la suscripción la escribe `billing`, y `onActivateCheckbiz` —ya en este repo— solo
  crea la sucursal inicial.
- Modelo de cobro: **29 € al mes hasta 50 empleados y 0,75 € por cada empleado a partir del
  51** —tramos graduados en Stripe sobre la misma cantidad de empleados, mismo recuento, los
  mismos 15 días de prueba—, servicio y factura aparte. **No se elige plan**: hay uno y el
  precio reacciona solo a la plantilla; los importes se controlan en Stripe. Sin tope de
  ejemplares —**un límite de plan nunca para el servicio: si se pasa, se cobra**— y **nunca**
  por movimiento. Ver [06 §D2](../06_decisiones-abiertas.md).

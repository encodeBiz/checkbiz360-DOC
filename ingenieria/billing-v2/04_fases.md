# Cobro y facturación — plan de migración por fases

Camino de `01_as-is.md` a `02_to-be.md`. Siete fases, cada una desplegable y
reversible por separado.

**Criterio innegociable: nada de cortes en seco sobre facturación en
producción.** Ninguna fase apaga un camino de cobro el mismo día que enciende su
sustituto. Cada una se valida contra producción antes de que la anterior se
corte, y deja el rollback preparado y probado.

## Cómo funciona el rollback

Toda fase es **un commit + un despliegue selectivo**. El rollback es
`git revert` del commit y volver a desplegar la misma lista de funciones:

```bash
npm run build
npm run deploy:function:prod -- --only functions:<lista de la fase>
```

Los cambios que no son código —eventos suscritos en el endpoint de Stripe,
ajustes del dashboard— son **interruptores**, y cada fase dice cuál toca. Se
apagan sin desplegar nada, que es la vía de escape más rápida cuando algo va mal
en un corte.

Tres reglas de proceso:

1. **Cada fase se prueba primero en `dev-encodebiz`** con
   `deploy:function:dev`, y ahí se usan **test clocks** de Stripe para comprimir
   un ciclo de facturación de un mes en minutos. `StripeService` ya tiene
   `preventTestClockError`, así que el terreno está preparado.
2. **Las puertas que dependen de un corte real de facturación se validan en
   producción y tardan un ciclo.** No hay atajo: el calendario del plan lo
   marca el día de corte de los clientes, no el nuestro. Las fases se pueden
   preparar en paralelo; las puertas no se pueden adelantar.
3. **Modo sombra antes de cada corte de importe.** El motor nuevo calcula y
   registra; el viejo sigue aplicando. Se corta cuando coinciden al céntimo
   durante los ciclos que fije la puerta. Es la forma concreta de cumplir el
   criterio innegociable.

## Resumen

| Fase | Qué hace | Cambia el importe | Se valida en |
|---|---|---|---|
| F0 | Red y observabilidad | No | 1 ciclo |
| F1 | Retirar el segundo motor | No (a verificar) | 1 día 5 |
| F2 | Sincronizar Firestore↔Stripe | No | Muestra + 1 ciclo |
| F3 | `BillingMode` en sombra → corte | No (debe ser idéntico) | 2 ciclos en sombra |
| F4 | Proyección de facturas y emails | No | 1 ciclo |
| F5 | Add-on Rentman | Sí, solo quien lo contrate | Entidad de prueba |
| F6 | Passinbiz medido | **Sí** — go-live de negocio | Sombra + aviso previo |

---

## F0 — Red y observabilidad, sin tocar ni un importe

La primera fase no cambia cuánto se cobra a nadie. Solo hace que los fallos se
vean y que Stripe deje de recibir respuestas equivocadas. Va primera porque todas
las puertas posteriores se apoyan en los datos que empieza a registrar.

**Cambios**

- `getMetaParent` — resolver campo a campo con `||` sobre metadata de factura,
  `parent.subscription_details.metadata` y metadata de línea (R6). Es el arreglo
  que desbloquea la conciliación de R12.
- Códigos de respuesta del webhook: firma inválida → 400; evento ajeno o no
  manejado → **200**; fallo transitorio → 5xx (R6).
- Deduplicación de eventos en `stripe_events/{event.id}`, marcando `done`
  **después** del handler.
- Comprobar el `Result` de `updateSubscription`, `finalizeInvoice` y
  `deleteInvoice`; fallo ⇒ excepción ⇒ 5xx ⇒ Stripe reintenta (R11, R18).
- `await` en `updateInvoice`, `cancelSubscription` y la escritura de
  `handleInvoicePaid` (R13).
- Registro `entities/{eid}/billingRuns/{stripeInvoiceId}` en cada ajuste.
- Suscribir `invoice.created` **en modo solo-observar**: compara el draft con lo
  esperado y registra la discrepancia. No corrige nada todavía.

**Despliegue**

```bash
npm run deploy:function:prod -- --only functions:apiV100-firebaseEntryHttp-stripeWebhook
```

Y en el endpoint de Stripe: añadir `invoice.created`.

**Puerta de salida** — un ciclo de facturación completo con:

- Cero respuestas 400 en el log de webhooks de Stripe salvo firma inválida.
- Un doc en `billingRuns` por cada factura emitida, con el conteo y el instante.
- Contador de discrepancias de `invoice.created` en cero. **Si no es cero, se
  para el plan y se investiga**: significa que ya hoy se está facturando algo
  distinto de lo que el sistema cree.

**Rollback** — revert + redeploy de una función; quitar `invoice.created` del
endpoint. Sin efecto sobre facturación en ningún momento.

**Riesgo residual** — un fallo que antes era silencioso ahora devuelve 5xx y
Stripe reintenta. Es lo que se busca, pero conviene mirar el log de webhooks los
primeros días: un 5xx persistente indica un fallo real que llevaba meses oculto.

---

## F1 — Retirar el segundo motor

Elimina R8 (doble motor), R12 (facturas del cron rechazadas por su propio
webhook) y R16 (bucle latente de emisión) **por construcción**, no con parches.

**Puerta de ENTRADA — verificación obligatoria, no suposición**

Antes de tocar nada hay que confirmar en el Firestore de **producción** que
ningún `service/{id}/plan/{planId}` tiene un `stripePrice` con valor que el cron
llegase a cobrar. El as-is lo da por cierto pero está marcado *sin confirmar*, y
los `stripePrice` vacíos que se ven en el repo son los del fixture
`passinbiz.plans.ts`, no los planes reales. **Si algún plan tiene precio,
retirar el cron deja de cobrar algo real** y esta fase cambia de naturaleza:
habría que migrar ese cobro a la suscripción antes de apagar nada.

**Cambios**

- Quitar `triggerInvoiceWorker` de `core/firebase-entry-schedule/index.ts` y
  `processInvoices` de `firebase-firestore-trigger/index.ts`.
- Sustituir la guarda de `deleteEntity` por `HasOutstandingInvoices(entityId)`,
  que consulta Stripe en vez de fabricar una factura (R15).
- `InvoicePaymentProcessor` deja de ser emisor. Su lógica de «qué es facturable»
  se conserva para F3; su camino de creación de facturas se retira.

**Despliegue**

```bash
npm run deploy:function:prod -- --only \
  functions:apiV100-firebaseEntrySchedule-triggerInvoiceWorker,\
functions:apiV100-firebaseFirestoreTriggers-processInvoices,\
functions:apiV100-firebaseEntryHttp-entity-deleteEntity
```

Retirar un export **borra** la función desplegada; Firebase pedirá confirmación.

**Puerta de salida**

- Pasa un día 5 sin que aparezca ninguna factura nueva en Stripe a las 3:00 UTC
  ni ningún doc `origin: "launcher"` en `invoices`.
- `deleteEntity` devuelve 400 `payment/pending` con una entidad que tenga una
  factura `open` en Stripe, y 201 con una que no.

**Rollback** — revert + redeploy: los exports vuelven y las funciones se
recrean. El cron es idempotente por día, así que recrearlo no duplica nada.

**Riesgo residual** — bajo, condicionado a la puerta de entrada. Si se salta esa
verificación, el riesgo es dejar de cobrar sin darse cuenta.

---

## F2 — Sincronizar Firestore↔Stripe

Cierra R2, R3, R9 y R14. No toca importes: solo hace que el estado que ve la
plataforma sea el real.

**Cambios**

- Renombrar `handleSubscriptionUpsert` → `createStripeSubscription` y **quitar la
  sobrecarga `Stripe.Event`** de `StripeRepository` (R14). Esto es lo primero:
  mientras la sobrecarga exista, alguien puede volver a descomentar los eventos y
  romper producción.
- Escribir `handleSubscriptionUpdated(event)` de cero, con el mapa de estados de
  `02_to-be.md`, incluido `endTestPeriod` ← `trial_end` (R3).
- Ampliar `Subscription.status`; retirar `"pending-pay"` y el checkout de saldo
  de `handleCancelSub` (R9).
- Backfill de una pasada: leer Stripe y corregir los docs divergentes.

**Orden dentro de la fase** — el backfill se ejecuta **después** de que el
handler esté desplegado y verificado. Al revés, los meses de divergencia se
corrigen y vuelven a divergir al día siguiente.

**Despliegue**

```bash
npm run deploy:function:prod -- --only \
  functions:apiV100-firebaseEntryHttp-stripeWebhook,\
functions:apiV100-firebaseFirestoreTriggers-onDocumentWriteSubscriptions
```

Y en el endpoint de Stripe: añadir `customer.subscription.created` y
`customer.subscription.updated`.

**Puerta de salida**

- Sobre una muestra de entidades, el estado del doc coincide con el de Stripe.
- Ningún doc en `pending` con suscripción activa en Stripe.
- Los docs en trial tienen `endTestPeriod` y coincide con `trial_end`.
- **Ningún email de alta o baja duplicado**: `onDocumentWriteSubscriptions`
  manda correo al cambiar de estado, y esta fase empieza a cambiar estados que
  antes se quedaban quietos. Es el efecto secundario a vigilar de esta fase.

**Rollback** — quitar los dos eventos del endpoint de Stripe (interruptor,
inmediato) y revert del código. El backfill no se revierte: solo escribió en
Firestore lo que Stripe ya decía.

**Riesgo residual** — la avalancha de emails del punto anterior. Mitigación:
desplegar con el envío de `SUBSCRIBE`/`CANCELLED` silenciado durante el backfill
y reactivarlo después.

---

## F3 — `BillingMode` en sombra, y luego el corte

La fase que toca el cálculo del importe. Por eso va en dos tiempos y con el modo
sombra en medio.

**Cambios**

- `BillingMode`, `ChargeStrategy` y sus dos registros (`kind` y `countSource`).
- Mapear item → doc de suscripción **por id de item, no por índice**: es el
  requisito para que un add-on pueda ser un segundo item.
- Abrir `SERVICES` a `string` y `Subscription.plan`; añadir `"SKIPPED_TRIAL"` a
  `InvoiceStatus` o retirarlo (R19). Dejar de pasar `any` en `updateInvoice`, que
  es lo que ocultaba estos estados al compilador.
- Migración de datos: cada plan real gana
  `billing: {kind: "per_seat", stripePrice: <el que ya tiene>, countSource:
  "checkinbiz.employees", minItems: <minItemsPay>}`. **Con los mismos precios**,
  para que el importe calculado sea idéntico.

**F3a — sombra.** El camino nuevo calcula la quantity y la escribe en
`billingRuns` como `expectedNew`; el que **aplica** sigue siendo el viejo. Nadie
nota nada.

**Puerta entre F3a y F3b** — **dos ciclos** en los que `expectedNew` coincide con
lo aplicado **al céntimo, en todas las entidades**. Una sola discrepancia
reinicia el contador. Dos ciclos, no uno: uno solo no distingue entre «es
correcto» y «coincidió por casualidad este mes».

**F3b — corte.** El camino nuevo pasa a aplicar. La sombra se invierte: ahora el
viejo calcula y registra sin aplicar, durante un ciclo más, antes de borrarlo.

**Despliegue** — `apiV100-firebaseEntryHttp-stripeWebhook` en las dos
subfases. El interruptor entre sombra y corte es una variable de entorno, para
que volver atrás no requiera desplegar código.

**Rollback** — F3a: no hay nada que revertir, solo escribe logs. F3b: cambiar la
variable de entorno. Si eso no bastara, revert + redeploy.

**Riesgo residual** — el mayor del plan, y por eso es el que más red lleva: dos
ciclos de sombra, interruptor sin despliegue y un ciclo de sombra invertida
después del corte.

---

## F4 — Proyección de facturas y emails

Cierra R5, R7, R10 y R17, y es la fase que hace que las facturas lleguen por
email — el síntoma que originó toda la investigación.

**Cambios**

- `invoices` como read model: escribir `paymentData` con el objeto de Stripe y
  retirar `inviceData`. **El front no se toca**: ya lee `paymentData.total` y
  `paymentData.invoice_pdf`, así que las filas a 0,00 € sin número ni PDF se
  arreglan solas (R10).
- `update()` sobre ref conocido en lugar de `set(merge: true)` que crea (R5).
- Quitar el filtro `includes("check")` de `handleInvoicePaymentFailed` (R17).
- `EmailType.PAYMENT_FAILED` y su plantilla, disparado desde
  `invoice.payment_failed` (D4).
- Rellenar `email` en los Customers de Stripe que no lo tengan, desde
  `entity.billingEmail`; `configBilling` deja de crear Customers sin email.

**El envío lo hace la plataforma, no el interruptor** (D5, invertida el
2026-08-26). Al recibir `invoice.finalized` se descarga el PDF de Stripe y se
manda adjunto, con plantilla `INVOICE` en `emails_template`, y cada envío queda
registrado en `invoice_emails/{stripeInvoiceId}` con su desenlace. El
interruptor *«Send finalized invoices and credit notes to customers»* **se queda
apagado**: encenderlo ahora significa factura por duplicado.

El backfill de emails sigue siendo necesario, pero por otro motivo — sin
`billingEmail` la factura queda anotada como `skipped` / `sin_destinatario` en
vez de salir.

**Puerta de salida**

- Un ciclo con las facturas llegando al `billingEmail` de cada entidad, y un
  documento en `invoice_emails` por cada una — enviada, o con el motivo por el
  que no.
- Un solo doc por factura en `invoices`, con número, total y PDF, y la tabla del
  front mostrando el importe correcto.
- Ningún Customer de Stripe sin `email`.

**Rollback** — el envío se apaga con `BILLING_SEND_INVOICE_DISABLED` o parando el
servicio; ya no basta con un interruptor del dashboard, que es el precio de
llevarlo nosotros. La proyección es escritura en Firestore: revert + redeploy,
sin efecto fiscal.

**Riesgo residual** — el primer ciclo con envío activado manda facturas a
direcciones que llevan meses sin recibir nada. Conviene revisar la lista de
`billingEmail` antes de encender el interruptor.

---

## F5 — Add-on Rentman

La primera fase que cobra algo nuevo, pero solo a quien lo contrate
explícitamente. Riesgo acotado por definición: nadie lo tiene hasta que lo pide.

**Puerta de entrada** — el **precio** cerrado (D6a). El diseño es agnóstico al
número, pero no se puede crear el Price de Stripe sin él.

**Cambios**

- Alta de datos: `service/rentman` + `service/rentman/plan/standard` con
  `billing: {kind: "flat", stripePrice: "price_…"}` y `monthlyPrice` informativo.
- `subscribeAddon`: exige el servicio anfitrión activo o en trial (D6d), añade el
  item a **su** suscripción de Stripe con `proration_behavior: "none"` (D6c), y
  crea el doc con `kind: "addon"`, `hostServiceId` y `stripeSubscriptionItemId`.
- La baja del anfitrión arrastra sus add-ons en la misma operación.

**Puerta de salida** — en una entidad de prueba con checkinbiz activo: contratar
el add-on **no** genera ninguna factura intermedia, la línea aparece en el
`invoice.upcoming` del corte siguiente junto a la de checkinbiz, y la factura
final lleva las dos líneas y **un solo número EBZSTRIPE**. Y contratarlo sin
checkinbiz se rechaza.

**Rollback** — quitar el item de la suscripción y desactivar el plan en
Firestore. Con cero contrataciones, el rollback es borrar un documento.

**Riesgo residual** — bajo. El más real es olvidar el arrastre en la baja y
dejar un item huérfano cobrando; lo detecta el vigilante diario de F0.

---

## F6 — Passinbiz medido

Va última **por negocio, no por dificultad técnica**. Hoy las suscripciones de
passinbiz facturan 0,00 € (R4). Encender el cobro por emisión empieza a cobrar
por primera vez a clientes que llevan meses sin pagar.

**Puerta de entrada** — dos cosas, ninguna técnica:

1. Aviso previo a los clientes de passinbiz afectados.
2. Tu OK explícito para empezar a cobrarles.

**Cambios**

- Meter y Price medido en Stripe.
- Reportar `meterEvent` en la emisión (`createPassOnDemand`), con
  **identificador idempotente** = id del pase, para que un reintento no cuente
  dos veces.
- `billing: {kind: "metered", …}` en el plan; la estrategia devuelve `null`
  porque un item medido no se ajusta en `invoice.upcoming`.

**F6a — sombra.** Se reportan los eventos de uso **sin asociar el Price**. Se
acumula el consumo real y se compara con lo esperado durante un ciclo, sin
cobrar nada.

**F6b — corte.** Se asocia el Price medido y empieza a facturar.

**Puerta entre F6a y F6b** — un ciclo en el que el uso reportado coincide con las
emisiones registradas en la plataforma, y el importe que saldría es el que se
comunicó a los clientes.

**Rollback** — F6a no cobra nada. F6b: quitar el item medido de las
suscripciones; el uso reportado se queda sin efecto económico.

**Riesgo residual** — es una decisión de negocio con impacto directo en clientes
reales. La parte técnica es la menos delicada de esta fase.

---

## Lo que queda fuera del plan

- **Las 8 facturas de 0 € ya emitidas** (EBZSTRIPE-0027..0030 y 0036..0039). Se
  quedan como están por decisión tomada: son facturas a 0 € sin efecto contable y
  anularlas añadiría movimientos a la serie fiscal. Quedan documentadas en
  `01_as-is.md` como incidencia conocida.
- **Bloqueo de servicio por impago.** Descartado en D4.
- **Plantilla propia de factura sobre SES.** Descartada en D5; la manda Stripe.
- **Congelar el importe en la fecha de corte.** Descartado en D3: se sigue
  contando cuando Stripe pregunta. Los `billingRuns` de F0 dejan el registro que
  faltaba, así que la decisión se puede revisar más adelante con datos.

# Cobro y facturación — as-is (agosto 2026)

Estado real del módulo de cobro de encodeBiz SaaS antes de rehacerlo. Todo lo
que hay aquí está verificado contra el código y contra el dashboard de Stripe
de producción, salvo lo marcado como *sin confirmar*.

## Dónde vive

- Repo `PLATAFORMA/encodeBiz-SAAS`, codebase `functions` (Firebase Functions v2,
  node 22, `europe-west1`, proyecto `encodebiz-services`).
- Stripe SDK `^18.2.1` — API 2025, la metadata de suscripción viaja en
  `invoice.parent.subscription_details.metadata`, no en `invoice.subscription`.
- Firestore: `entities/{eid}/subscriptions/{serviceId}`,
  `entities/{eid}/subscriptions-deleted/{...}`, `entities/{eid}/invoices/{id}`,
  `service/{serviceId}/plan/{planId}`.
- Front: `encodebiz-front-saas`, pestaña de facturas en
  `src/app/main/[entityId]/entity/tabs/tabFacturas/`.

Piezas desplegadas que intervienen:

- HTTP: `subscriptions-subscribe`, `subscriptions-unsubscribe`,
  `subscriptions-configBilling`, `stripeWebhook`, `entity-deleteEntity`.
- Triggers: `firebaseFirestoreTriggers-processInvoices` (onCreate de invoices),
  `firebaseFirestoreTriggers-onDocumentWriteSubscriptions`.
- Schedule: `firebaseEntrySchedule-triggerInvoiceWorker` (`0 3 5 * *`, sin
  timeZone → 3:00 UTC).

## El ciclo, paso a paso

1. **`configBilling`** crea el Customer en Stripe si falta (`email:
   entity.billingEmail`, nombre legal, `metadata.entityId`) y devuelve una URL
   del Customer Portal. `payment_method.attached` guarda marca y last4 en
   `entity.billingConfig.payment_method`. Sin `stripeCustomerId` el alta corta.
2. **`subscribe`** crea el doc de suscripción con `status: "pending"` y la
   suscripción en Stripe con `quantity: 0`, metadata `{entityId, serviceId,
   subscriptionId, usageCount, subId}` y `trial_period_days: 45` solo si es la
   primera vez. Si hubo una baja previa, entra con el count real y sin trial.
3. **Trial de 45 días.** Stripe emite una factura a 0 € al arrancarlo; es
   normal y no debe confundirse con las fantasma del punto siguiente.
4. **Cada ciclo, `invoice.upcoming`** → `handleInvoiceUpcoming` cuenta empleados
   (`countByEntity`) y actualiza la quantity con `proration_behavior: "none"`.
   **Este es el único punto donde se calcula el importe de checkinbiz.**
5. **Stripe factura y cobra** con `charge_automatically` sobre la tarjeta.
6. **`invoice.paid`** → `handleInvoicePaid` escribe el resultado en Firestore.
7. **`invoice.payment_failed`** → marca `FAILED`. Sin reintento ni aviso propio.
8. **`unsubscribe`** → `cancel_at_period_end: true`; el trigger de suscripciones
   manda el email de cancelación y, si el plan es payPerUse, genera un checkout
   por el saldo pendiente. `customer.subscription.deleted` mueve el doc a
   `subscriptions-deleted`.
9. **En paralelo**, el cron del día 5 monta una factura pay-per-use aparte
   contando lo mismo que ya cuenta la suscripción.

## Roturas confirmadas

**R1 — El cron emitía una factura de 0 € por entidad activa, cada mes.**
`InvoicePaymentProcessor` creaba la invoice en Stripe *antes* de saber si había
ítems, con `auto_advance: true`; cuando no los había el `deleteInvoice` se
lanzaba sin `await` y Cloud Functions cortaba la CPU antes de completarlo, así
que Stripe finalizaba la draft sola. Evidencia en producción: EBZSTRIPE-0036 a
0039 (5 ago 5:00 CEST) y 0027 a 0030 (5 jul 5:00), sin líneas, sin frecuencia.
**Ya arreglado** — ver más abajo.

**R2 — Los webhooks de suscripción están comentados.**
`customer.subscription.created` y `.updated` en
`stripeWebhookController.controller.ts:38-41`. El `status` de Firestore nunca se
sincroniza con Stripe: un plan de pago normal se queda en `pending` para
siempre. Firestore y Stripe divergen desde el alta.

**R3 — `endTestPeriod` nunca se escribe.** Declarado en `Subscription`, leído
solo por `InvoicePaymentProcessor`. El trial vive únicamente en Stripe; la
plataforma no sabe quién está en prueba.

**R4 — `handleInvoiceUpcoming` solo cubre checkinbiz.** El filtro
`serviceId.toLowerCase().includes("checkinbiz")`
(`StripeSuscriptionRepository.ts:123`) deja passinbiz sin corregir nunca, así
que sus suscripciones facturan 0,00 € indefinidamente. Visto en producción:
EBZSTRIPE-0026, 0031, 0033, 0035, todas mensuales y a cero.

**R5 — `invoice.paid` crea documentos en vez de actualizarlos.**
`handleInvoicePaid` usa el id de Stripe como ref (`StripeSuscriptionRepository.ts:44`)
en lugar del `invoiceRef` que el propio sistema mete en la metadata al crear la
factura, y `updateInvoice` hace `set(merge:true)`
(`FirestoreSubscriptionRepository.ts:118-122`), que **crea** el doc si no
existe. Resultado: dos documentos por factura, el original congelado en
`PROCESSING` y uno nuevo con los datos buenos. Además pisa `createdAt`.

**R6 — El webhook responde 400 a eventos que no le incumben.**
`stripeWebhookController.controller.ts:18` lanza `UNHANDLED_EVENT` para todo
evento `invoice.*` sin `serviceId`, y el wrapper lo traduce a 400. Para Stripe
es una entrega fallida: reintenta durante días y con volumen suficiente puede
deshabilitar el endpoint. Agravado por un bug en `getMetaParent`
(`StripeSuscriptionRepository.ts:21-27`): `fromParentMeta ?? fromLineMeta` nunca
cae al fallback porque el `|| {}` previo deja el primero siempre definido.

**R7 — Stripe no envía las facturas al cliente.** No es el código: con
`auto_advance` activo al finalizar, Stripe puede enviarlas. Falta activar
**Settings → Billing → Subscriptions and emails → "Send finalized invoices and
credit notes to customers"**. Requisito adicional: el Customer debe tener
`email` (viene de `entity.billingEmail`, que puede estar vacío).

**R8 — Dos motores de facturación para el mismo consumo.** La suscripción de
Stripe y el cron del día 5 cuentan ambos empleados/holders. Hoy el cron no
factura nada (todos los planes del repo tienen `stripePrice: ""` — *sin
confirmar en Firestore de producción*), pero el día que un plan tenga precio y
supere `minItemsPay` emitiría un segundo cargo por lo mismo.

**R9 — Estado `"pending-pay"` fuera del tipo.** `subscriptionsWrite.controller.ts:40`
lo escribe; `Subscription.status` solo admite `active | trialing | cancelled | pending`.

**R10 — El front lee un campo que el flujo del cron nunca rellena.** La tabla
usa `paymentData.total ?? amount_paid ?? amount_due ?? 0`; el doc del launcher
guarda su snapshot en `inviceData` (con el typo) y capturado antes de añadir
ítems, así que la fila sale a 0,00 €, sin número y sin PDF.

## Lo ya arreglado (no rehacer)

Rama `fix/stripe-invoice-cero`, commit `069d39cc`. Desplegada **solo**
`apiV100-firebaseFirestoreTriggers-processInvoices`.

- `InvoicePaymentProcessor` decide qué es facturable antes de tocar Stripe; la
  invoice solo nace si va a llevar importe, y el camino de error borra la draft
  con `await` y marca `FAILED`.
- `makeInvoice` crea con `auto_advance: false` — lo activa `finalizeInvoice`.
- `await` en las escrituras que iban sueltas.
- `StripeService.deleteInvoice` no asignaba su resultado (devolvía error aunque
  el borrado fuese bien) y tenía mal los tipos.

Pendiente de limpieza manual: las 8 facturas ya emitidas. No se pueden borrar,
hay que anularlas con `voidInvoice` filtrando por `metadata.invoiceRef` y
`total === 0` para no tocar ninguna buena.

## Lo que el módulo no cubre y va a tener que cubrir

**Add-ons de pago con cuota fija.** El primero es Rentman.

Servicios y planes se definen **en Firestore** (`service/{id}` y su subcolección
`plan/{planId}`, que es de donde lee `findPlansServices`), así que dar de alta
Rentman como un servicio más es cuestión de datos. Y el modelo de plan ya
contempla la cuota fija: tiene `monthlyPrice` y `payPerUse`.

El hueco está en el **código de cobro**, que solo sabe cobrar por cantidad:

- Nadie lee `monthlyPrice` para facturar. El importe sale siempre de
  `stripePrice` multiplicado por un count.
- `GetCountPayPerUse` es un `switch` sobre el serviceId con `default: return 0`:
  un servicio nuevo cuenta cero y nunca se cobra.
- `handleInvoiceUpcoming` filtra por `includes("checkinbiz")`, así que tampoco
  ajusta nada para otro servicio.
- El tipo `SERVICES` (`core/services/domain/Service.ts`) es cerrado a
  `"passinbiz" | "checkinbiz"` — detalle de tipado, pero hay que tocarlo.

Ni una aparición de `addon` ni de `rentman` en `encodeBiz-SAAS/functions/src`.
El add-on vive en otro repo: `encodebiz-api/services/rentman`, microservicio con
sync bidireccional por polling.

El módulo nuevo tiene que soportar las dos formas de cobro conviviendo —variable
por uso y fija por add-on contratado— y decidir si comparten factura o van
separadas.

Contexto en `encodeBiz-SAAS/DOCS/addons/rentman-integration.md`. Ojo: ese
documento **no fija el precio del add-on**, lo dejaba pendiente de cerrar en la
fase 0 contra la cuenta real del cliente.

## Decisiones de producto abiertas

Hay que resolverlas **antes** de diseñar el to-be; no asumir ninguna:

1. ¿El modelo pay-per-use por cron se descarta del todo, o algún plan debe
   cobrarse así? De ello depende si el cron se retira o se arregla.
2. ¿Passinbiz debe facturar por número de holders igual que checkinbiz, o tiene
   un modelo propio?
3. ¿El importe debe congelarse en la fecha de corte o seguir siendo "empleados
   vivos el día que Stripe pregunta"? Hoy es lo segundo, sin registro de qué se
   contó ni cuándo.
4. ¿Qué debe pasar ante un impago: dunning de Stripe, bloqueo del servicio,
   aviso propio? Hoy no hay nada.
5. ¿La factura la envía Stripe o la queremos enviar nosotros con plantilla
   propia (el `EmailService` sobre SES ya existe, pero no tiene tipo de factura)?
6. Add-ons: ¿cuánto cuesta el de Rentman y con qué periodicidad? ¿Va en la misma
   factura que el servicio o en una aparte? ¿Se prorratea si se contrata a mitad
   de ciclo, o entra en el ciclo siguiente? ¿Se puede contratar sin tener
   checkinbiz activo?

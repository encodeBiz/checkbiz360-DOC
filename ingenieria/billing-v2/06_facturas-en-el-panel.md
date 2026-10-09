# Las facturas del panel salen de Stripe (9 oct 2026)

## El problema

La pestaña **Facturas** de la ficha de la empresa lee `entities/{id}/invoices` en Firestore.
Esa colección la llenaba la Cloud Function al cobrar (`handleInvoicePaid` con
`set(merge)`), y el servicio `billing` dejó de escribir ahí a propósito: crear un documento en
esa colección enciende `processInvoices`, cuyo siguiente paso es emitir otra factura al mismo
cliente (HAL-31). Desde el porte, **ninguna factura de suscripción aparece en el panel**, ni la
mensual de checkinbiz ni la del add-on de inventario. Lo único que cae en la colección son los
documentos del ciclo de pago por uso del día 5, que se dio por retirado.

Se vio el 9 de octubre con la entidad `qCGqm283pVbxa2O4V80z` de desarrollo: su factura de
inventario (29 €) se emitió, se envió, se cobró al segundo intento y no salía en Facturas.

## La decisión

La pestaña pide las facturas a `billing`, y `billing` las lee de **Stripe**, que es donde
viven, con su PDF y su enlace. Firestore deja de ser la fuente de la lista.

**Solo las de checkbiz360.** La cuenta de Stripe cobra también cosas que no son de la
plataforma (mantenimientos, el «Departamento Tecnológico Adjunto»), a veces **al mismo
cliente de Stripe** que paga el plan: Arendel tiene en un solo `cus_` el Plan Bronze, su
mantenimiento y el departamento adjunto. Listar por cliente no sirve.

Una factura es de la plataforma si es de **una suscripción de la empresa a un servicio de la
plataforma** (`checkinbiz`, `passinbiz` y los add-ons, hoy `inventory`). Las suscripciones se
reúnen de dos sitios, porque ninguno basta solo:

1. **Firestore**: `entities/{id}/subscriptions` y `entities/{id}/subscriptions-deleted`, su
   `stripeSubscriptionId`. Cubre las suscripciones antiguas que nacieron **sin metadata** en
   Stripe (ACB2PAINTING, `sub_1T7PUQ`), que por la metadata no se reconocerían.
2. **Stripe**: las suscripciones del cliente (`status: all`) cuya metadata lleva
   `entityId` = la empresa y `serviceId` de la plataforma. Cubre la que se pierde en Firestore
   cuando una empresa vuelve a contratar antes de que la baja anterior se archive: `Subscribe`
   reescribe `subscriptions/{serviceId}` y el id viejo desaparece de ahí.

Un add-on nuevo entra solo, sin tocar este código, en cuanto esté en la lista de servicios de
la plataforma: su suscripción vive en la misma colección y lleva la misma metadata.

**Qué no entra**: los borradores (`draft`), que todavía no son una factura; y las facturas
sueltas del ciclo del día 5 (metadata `invoiceRef`, sin suscripción), retirado y cuyas
emisiones fueron todas a 0 € sin líneas. Las de 0 € de inicio de prueba **sí** se listan: son
facturas emitidas y el portal de Stripe también las enseña.

**El envío por correo no cambia.** `SendInvoiceEmail` sigue mandando **todas** las facturas
que emite la cuenta, sean de la plataforma o no. El filtro es solo de lo que se enseña en el
panel.

## El contrato

`GET /api/v1/billing/invoices/:entityId?page=0&limit=10&order=desc` — Firebase Auth, owner o
admin activo de la empresa (`canWrite`, el mismo permiso que el portal de pagos).

```json
{ "ok": true, "total": 14, "page": 0, "limit": 10,
  "invoices": [{ "id": "in_…", "number": "EBZSTRIPE-0057", "serviceId": "checkinbiz",
                 "status": "paid", "total": 5600, "currency": "eur", "createdAt": "2026-10-…",
                 "paidAt": "2026-10-…", "pdfUrl": "https://…", "hostedUrl": "https://…" }] }
```

`status` es el de Stripe (`open`, `paid`, `void`, `uncollectible`). La paginación es del
servidor, con `total` para la tabla. Por debajo se leen todas las facturas de esas
suscripciones —una al mes por servicio, una docena al año— y se ordenan y cortan en el
servicio: Stripe pagina por suscripción y no permite unir varias en una consulta.

En el panel, un handler nuevo del proxy, `NEXT_BACKEND_URI_BILLING_INVOICES`, con la base
`…/api/v1/billing/invoices` y como subruta solo el id de la empresa. **Hace falta darla de alta
en Vercel** al pasar a producción.

## Visto de paso, fuera de este cambio

- En producción hay empresas en `bronze` sin `stripeSubscriptionId` (`BS58CX9Agj77EpXp5Zbg`,
  `YTQ3YQQBAio79YeAJsok`, `u59dle7JadTTIQcbMRrv` con checkinbiz y passinbiz): su pestaña saldrá
  vacía, y hay que mirar si se les cobra.
- El plan `passinbiz/bronze` de producción apunta a un precio de la cuenta de Stripe de
  desarrollo (`price_1RuA6x…R97dgHV4NJ`): contratarlo fallaría.
- No hay correo de «pago recibido»: una factura que se cobra tras un fallo solo se envía al
  emitirse.

# IVA en las altas nuevas (3 nov 2026)

## El problema

Las facturas de la plataforma salen **sin IVA**. Ningún camino del cobro lo aplica: ni
`Subscribe` al crear la suscripción en Stripe, ni el enlace de pago de la baja, ni el exceso
de almacenamiento. Tampoco hay un tipo de impuesto dado de alta en Stripe para estas
suscripciones. Y el cliente de Stripe se crea con nombre y correo, sin dirección ni CIF, que
una factura completa con IVA tiene que llevar.

## La decisión

Jose, 3 nov 2026: **«es importante que no afecte a los que ya están; fue nuestro error y lo
tenemos que asumir»**. El IVA se cobra solo a los clientes nuevos.

**Quién es nuevo, por fecha y no por suscripción.** Un cliente es nuevo si su cliente de
Stripe (`cus_`) se creó en o después de `BILLING_VAT_SINCE`. Quien ya lo era queda fuera para
siempre **en el plan base**, también si se da de baja y vuelve: una suscripción nueva de un
cliente de antes no es un cliente nuevo. La fecha de Stripe no se puede tocar desde el panel y
queda en el propio cliente, así que la decisión se puede reconstruir en cualquier momento.

**Los add-ons, siempre más IVA (Jose, 5 nov 2026).** «Los add-ons van con IVA siempre; solo el
base se queda sin IVA para los que ya están.» Inventario y quiosco llevan el 21 % para todos,
también para el cliente de antes, en cuanto se contratan. Las suscripciones de add-on que ya
existían no se tocan («si se contrata nuevo va con IVA»). Sus precios de Stripe no tienen
comportamiento fiscal (`tax_behavior: unspecified`), así que el tipo exclusivo se suma sin un
segundo precio. Está en `ADDONS` de `services/billing/src/domain/Vat.ts`; un add-on nuevo se
añade ahí.

**Un tipo fijo, no Stripe Tax.** Un `tax_rate` de Stripe del 21 %, **exclusivo** (se suma al
precio: 40 € + 8,40 €), apuntado en `BILLING_VAT_TAX_RATE`. Es lo mismo que ya usan las
facturas que se hacen a mano en Billing (Jose: Stripe Tax no se ha activado nunca). Stripe Tax
cobra un 0,5 % por transacción; el tipo fijo no tiene coste.

- Desarrollo: `txr_1UXnRnR97dgHV4NJThACYXNU` (creado por API el 3 nov 2026; probado:
  19,00 € + 3,99 € = 22,99 €).
- Producción: el «IVA 21 %» que ya existe en la cuenta, que es exclusivo (Jose, 3 nov 2026:
  «se suma»). No se crea otro: se apunta su `txr_` en `BILLING_VAT_TAX_RATE`.

**El precio de los nuevos.** Los precios de los planes están en Stripe como «IVA incluido»
(en dev, el Bronze de checkinbiz; medido el 3 nov 2026) y Stripe no deja sumarles un tipo
exclusivo: el alta daba un 500. Un precio no cambia de comportamiento fiscal una vez creado,
así que el plan lleva un segundo precio, el mismo importe «más IVA», en
`service/{serviceId}/plan/{planId}.stripePriceVat`. El cliente nuevo va a ese; el de antes
sigue en `stripePrice` (Jose: «los actuales mantienen IVA incluido»). Un precio sin
comportamiento fiscal (`unspecified`) admite el IVA tal cual y no necesita el segundo. Si aun
así Stripe rechaza el IVA, el alta y el enlace de pago salen sin IVA con un
`[billing][ALERTA]`: un problema de impuestos no deja a nadie sin contratar.

- Dev: Bronze checkinbiz `stripePriceVat = price_1UXoPwR97dgHV4NJ9L6QvcqO` (2,00 € exclusivo).
- Prod: pendiente de mirar qué precios son «IVA incluido» y crear su par.

**Según dónde está la empresa** (propuesta a confirmar con la gestoría):

| Empresa | IVA | Motivo en el log |
|---|---|---|
| España peninsular y Baleares | 21 % | — |
| Canarias (CP 35, 38), Ceuta (51), Melilla (52) | no | `canarias_ceuta_melilla` |
| Otro país de la UE, con número de IVA | no, inversión del sujeto pasivo | `ue_inversion_sujeto_pasivo` |
| Otro país de la UE, sin número de IVA | 21 % | — |
| Fuera de la UE | no | `fuera_de_la_ue` |
| País que no se reconoce | no | `pais_no_reconocido` |

A la empresa de la UE con número de IVA se le marca el cliente de Stripe como
`tax_exempt: reverse` y se le pone en el pie de factura la mención de la inversión del sujeto
pasivo (art. 84.Uno.2º y 69 LIVA; art. 196 de la Directiva). Su número se da de alta como
`eu_vat`, que Stripe espera con el prefijo del país (`FR…`, `PT…`).

Las que quedan sin IVA no pasan en silencio: el alta deja un `[billing][REVISAR]` en el log
con la empresa y el motivo. El número de IVA intracomunitario no se comprueba en VIES antes
de facturar: por eso se revisa a mano.

El país se guarda en tres formatos (`ES`, `Spain`, `España`; medido en dev: 431, 10 y 2 de
443 empresas): se normaliza.

**Dónde se aplica:**

- `Subscribe`: la suscripción nace con `default_tax_rates`. Stripe copia ese tipo a cada
  factura de la suscripción, y lo aplica también a las líneas sueltas que se añaden al
  borrador, como el exceso de almacenamiento (`AddStorageCharge`).
- `Unsubscribe`: el enlace de pago del pendiente de pago por uso lleva el tipo en su línea.
- En el mismo alta, al cliente nuevo se le completan en Stripe la dirección y el CIF de
  `entity.legal` si no los tiene, para que la factura salga con los datos del cliente. Si
  Stripe rechaza el formato del CIF, se avisa en el log y el alta sigue: un CIF mal escrito
  no puede dejar a nadie sin contratar.

**Interruptor.** Sin `BILLING_VAT_TAX_RATE` o sin `BILLING_VAT_SINCE` no se aplica a nadie.
Desplegar el código no cambia ninguna factura; lo enciende el `.env`.

## Fuera de esto

- Los clientes de antes siguen sin IVA. Si un día se decide cambiarlo, es otra decisión.
- Las facturas manuales del dashboard (mantenimientos, departamento adjunto) no pasan por el
  servicio: su IVA se pone a mano, como hasta ahora.
- Los precios que enseñan el panel y la landing: si dicen «sin IVA» o no lo dicen, hay que
  revisarlos aparte.

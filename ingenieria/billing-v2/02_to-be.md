# Cobro y facturación — to-be (agosto 2026)

Diseño del módulo de cobro después de las decisiones de producto. El punto de
partida es `01_as-is.md`: R1–R19 y las seis decisiones, ya resueltas. El plan de
migración por etapas va en `04_fases.md`; aquí está el destino, no el camino.

> **Revisión del 2026-08-26.** Dos cosas cambiaron después de escribir esto y
> están corregidas más abajo: el módulo **se ha portado a `encodebiz-api` como
> servicio `billing` (puerto 3011, `/api/v1/billing/`)** en lugar de seguir en
> las Cloud Functions, y la **decisión 5 se ha invertido** — la factura la manda
> la plataforma, no Stripe. El resto del diseño se mantiene: lo que aquí se
> decide sigue siendo el destino, solo cambia la casa. El plan de fases de
> `04_fases.md` está escrito contra el código de Functions y hay que releerlo
> con eso en mente.

## Decisiones tomadas

| # | Decisión | Resuelto |
|---|---|---|
| 1 | Motor de cobro | **Uno solo: la suscripción de Stripe.** El cron del día 5 se retira. |
| 2 | Passinbiz | **Por emisión**, no por stock de holders. |
| 3 | Base de cálculo | **Vivos cuando Stripe pregunta** (no se congela), pero **se registra** qué se contó. |
| 4 | Impago | **Dunning de Stripe + aviso propio.** Sin bloqueo de servicio. |
| 5 | Envío de factura | **La plataforma**, con el PDF de Stripe adjunto. Invertida el 2026-08-26; antes era Stripe. |
| 6a | Precio del add-on | **Mensual**, importe en Firestore (`plan.monthlyPrice` + Price de Stripe), a cerrar en Fase 0 de Rentman. |
| 6b | Factura del add-on | **La misma que el servicio**, en línea aparte. |
| 6c | Prorrateo | **No.** Entra en el ciclo siguiente (`proration_behavior: "none"`). |
| 6d | Add-on suelto | **No.** Requiere checkinbiz activo. |
| — | Las 8 facturas de 0 € ya emitidas | **Se quedan.** Incidencia conocida documentada, no se anulan. |

Dos decisiones se cruzan y hay que reconciliarlas de forma explícita: «un solo
motor» (D1) y «passinbiz por emisión» (D2). La forma de tener las dos sin
resucitar el cron es **facturación medida de Stripe**: cada emisión se reporta
como evento de uso contra la propia suscripción, y Stripe lo factura al cierre
del ciclo. El cobro por emisión deja de necesitar un proceso propio.

## Principios que no se negocian

Nacen de las dos restricciones del contexto —hay clientes cobrando ahora mismo y
la serie EBZSTRIPE es fiscal— y aplican a todo el diseño:

1. **Un número EBZSTRIPE solo se quema con una factura que se pretende cobrar.**
   Stripe asigna el número al **finalizar**, no al crear. Por tanto toda
   corrección de importe ocurre sobre el **draft**, donde no cuesta nada.
2. **Nunca se emite una factura fuera del ciclo de la suscripción.** No hay
   ningún camino de código que cree y finalice una factura por su cuenta. La
   emisión es siempre de Stripe, en su corte.
3. **Ningún proceso automático anula, emite ni corrige a ciegas.** Los
   vigilantes (`sweepers`) informan; no mutan.
4. **Toda llamada que muta en Stripe lleva `idempotency_key`.** Hoy no la lleva
   ninguna, y Stripe reintenta los webhooks: es la protección directa de la
   serie fiscal contra los duplicados.
5. **El webhook nunca responde 400 a un evento legítimo.** 400 se reserva a
   firma inválida. Lo que no incumbe → 200. Lo que falla por algo transitorio →
   5xx, para que Stripe reintente.
6. **Firestore es proyección, no fuente.** La verdad del cobro está en Stripe.
   La subcolección `invoices` es un read model; no manda nada.

## Arquitectura

### El modelo de cargo: `BillingMode`

Es la pieza central y la que resuelve el hueco de los add-ons. Hoy el importe
solo puede salir de `stripePrice × count`, y el count solo lo sabe calcular un
`switch` cerrado sobre dos serviceIds (`GetCountPayPerUse`, R en el as-is: el
`default: return 0`). El to-be sustituye ese switch por un **modo de cobro
declarado en el plan**, que vive en Firestore:

```ts
// core/subscriptions/domain/BillingMode.ts
export type BillingMode =
  | {kind: "per_seat"; stripePrice: string; countSource: string; minItems: number}
  | {kind: "metered";  stripePrice: string; meter: string}
  | {kind: "flat";     stripePrice: string}
  | {kind: "free"}
```

- `per_seat` — cobro variable por uso. `countSource` nombra al contador
  (`"checkinbiz.employees"`), no al servicio. checkinbiz.
  `minItems` sustituye a `minItemsPay`.
- `metered` — cobro por evento. Stripe acumula el uso; nosotros solo reportamos.
  passinbiz.
- `flat` — cuota fija mensual. **Los add-ons.** Rentman.
- `free` — freemium y contratos gestionados a mano. No genera línea.

El plan de Firestore (`service/{serviceId}/plan/{planId}`) gana un campo
`billing: BillingMode`. `monthlyPrice` se conserva como dato informativo para el
front y para el alta del Price; el importe que se cobra es siempre el del
`stripePrice` referenciado por el modo, porque es el que Stripe conoce.

**Dar de alta un servicio o un add-on nuevo pasa a ser un alta de datos.**
`service/rentman` + `service/rentman/plan/standard` con
`billing: {kind: "flat", stripePrice: "price_…"}` y ya factura. Ninguna línea de
código nueva, que era el requisito.

### El registro de estrategias

```ts
// core/subscriptions/domain/ChargeStrategy.ts
export interface ChargeStrategy {
  // null = este modo no ajusta quantity (metered, flat, free)
  resolveQuantity(entityId: string, sub: Subscription): Promise<number | null>;
}
```

Un registro mapea `BillingMode.kind` → estrategia, y para `per_seat` un segundo
registro mapea `countSource` → contador. Los servicios registran su contador;
el módulo de cobro no los conoce por nombre.

Con esto desaparecen las tres barreras del as-is de golpe: el `default: return 0`
de `GetCountPayPerUse`, el `includes("checkinbiz")` de `handleInvoiceUpcoming` y
el tipo cerrado `SERVICES`. `SERVICES` pasa a `string` —los servicios son datos
de Firestore, ese es su tipo honesto— conservando las constantes conocidas;
`Subscription.plan` deja de ser `"freemium" | "bronze" | "enterprise"`.

### Add-ons: item sobre la suscripción del servicio

D6b + D6d fijan la forma: el add-on es un **segundo item** de la suscripción de
Stripe de checkinbiz. Una factura, un cargo, un número fiscal.

Esto rompe una suposición que hoy está por todo el código: **que una suscripción
tiene un solo item**. `handleInvoiceUpcoming` usa `subscription.items.data[0]`;
`subscribe` monta `items: [{…}]`. Con add-ons hay N items, y hay que mapear
item → documento de suscripción **por id de item, nunca por índice**.

El documento de suscripción gana:

```ts
kind: "service" | "addon";
stripeSubscriptionItemId?: string;  // el item que representa este doc
hostServiceId?: string;             // solo addons: de quién cuelga
```

Reglas derivadas:

- Contratar un add-on exige `subscriptions/{hostServiceId}` en estado activo o
  en trial. Si no lo hay, se rechaza (D6d).
- Se añade con `proration_behavior: "none"`, así que el primer cargo llega en el
  corte siguiente y **no se emite ninguna factura intermedia** (D6c). El cliente
  estrena el add-on gratis los días que queden de ciclo: es intencionado.
- Dar de baja el servicio anfitrión arrastra sus add-ons, en la misma operación.

### La red debajo de `invoice.upcoming`

D3 mantiene «vivos cuando Stripe pregunta», así que `invoice.upcoming` sigue
siendo el momento de verdad. La diferencia con el as-is es que deja de estar
solo. Cuatro capas, de más barata a más cara:

**1. Que el fallo se note (R11).** `updateSubscription` devuelve un `Result` que
hoy se descarta. Se comprueba `.success`; si falla, se lanza, y el webhook
responde **5xx** para que Stripe reintente. Un fallo transitorio se arregla
solo; uno permanente queda en el log de webhooks de Stripe y en la alerta. Lo
mismo con `finalizeInvoice` y `deleteInvoice` (R18).

**2. Registro de lo que se contó.** Cada ajuste escribe en
`entities/{eid}/billingRuns/{stripeInvoiceId}`: qué items, qué quantity, de qué
`countSource`, en qué instante, con qué plan y qué Price. Es lo que el as-is
echaba en falta —«sin registro de qué se contó ni cuándo»— y es la base para
poder comparar dos motores en paralelo durante la migración.

**3. Segunda oportunidad sobre el draft (`invoice.created`).** Es la pieza que
convierte un punto único de fallo en dos intentos independientes. La secuencia
de Stripe para una factura de suscripción es:

```
invoice.upcoming ──(días antes, ajuste de quantity)──▶
invoice.created  ──(draft, ventana de ~1h)──▶ invoice.finalized ──▶ cobro
                    ↑ aquí el número aún NO está asignado
```

Al recibir `invoice.created` se recalcula lo esperado y se compara con las
líneas del draft. Si no cuadra y la factura sigue en draft, **se corrige la
línea** y se registra la corrección. Corregir un draft no consume número de
serie, así que esta capa es gratis en términos fiscales. Si la factura ya está
finalizada, no se toca nada: se registra la discrepancia y se avisa.

> Nota de implementación: corregir un draft **no** se hace con
> `updateSubscription` —eso no reescribe líneas ya materializadas— sino
> actualizando la línea de la factura
> (`/v1/invoices/{invoice}/lines/{line_item_id}`). Hay que verificar la firma
> exacta contra el SDK v18 antes de escribirlo; si no estuviera disponible, la
> capa 3 se degrada a solo-observar y la 4 gana peso.

**4. Vigilante diario.** Un `schedule` que busca incoherencias estructurales:
suscripción con plan `per_seat` y quantity 0, documento de Firestore en `pending`
con suscripción activa en Stripe, add-on sin anfitrión. **Solo informa.** No
corrige y no emite (principio 3).

### Sincronización Firestore↔Stripe

R2 no se arregla descomentando: `handleSubscriptionUpsert` es un **creador** de
suscripciones disfrazado de handler por una sobrecarga de la interfaz (R14).
Llamarlo con un evento crearía una suscripción con `customer: undefined`. Se
separa en dos piezas con nombres que no engañan:

- `createStripeSubscription(params)` — lo que hoy hace, sin la sobrecarga
  `Stripe.Event` de `StripeRepository`.
- `handleSubscriptionUpdated(event)` — nuevo, escrito de cero. Traduce el estado
  de Stripe al documento y **nada más**: no crea nada en Stripe.

El mapa de estados, que es el que hoy no existe:

| Stripe | Firestore |
|---|---|
| `trialing` | `trialing` + `endTestPeriod` ← `subscription.trial_end` |
| `active` | `active` |
| `past_due` | `past_due` |
| `unpaid` | `unpaid` |
| `canceled` | `cancelled` |
| `cancel_at_period_end: true` | `pending_cancellation` |

Escribir `endTestPeriod` desde `trial_end` cierra R3: la plataforma pasa a saber
quién está en prueba sin preguntárselo a Stripe. `Subscription.status` se amplía
a esa lista y `"pending-pay"` desaparece (R9): con un solo motor no hay saldo
suelto que cobrar aparte, así que la baja de un plan medido la liquida Stripe en
la factura final del ciclo y el checkout ad-hoc de `handleCancelSub` se retira.

Meses de divergencia acumulada no se arreglan solos: hace falta un **backfill de
una pasada** que lea Stripe y corrija los documentos. Es idempotente, solo
escribe en Firestore y no toca Stripe, así que es de las operaciones más seguras
del plan.

### Endurecer el webhook

- **`getMetaParent` (R6).** La cadena `fromParentMeta ?? fromLineMeta` nunca cae
  al fallback porque el `|| {}` previo deja el primero siempre definido. Se
  encadena con `||` sobre los tres orígenes reales —metadata de la factura,
  `parent.subscription_details.metadata`, metadata de la línea— y se resuelve
  campo a campo, no objeto a objeto. Arreglar esto es lo que desbloquea la
  conciliación de R12.
- **Códigos de respuesta.** Firma inválida → 400. Evento no manejado o ajeno →
  **200**. Fallo transitorio → 5xx. Nunca más un 400 que Stripe interprete como
  entrega fallida y reintente durante días.
- **Deduplicación de eventos.** `stripe_events/{event.id}` con `create()`: si ya
  existe y está `done`, se responde 200 sin volver a procesar. El marcador se
  pasa a `done` **después** de que el handler termine bien; un `processing` más
  viejo que unos minutos se considera abandonado y se permite reprocesar. El
  orden importa: marcar `done` antes de procesar convertiría un fallo en una
  pérdida silenciosa de evento.

### Facturas en Firestore: read model

La subcolección `invoices` pasa a ser proyección de las facturas de Stripe.

- Se escribe **`paymentData`** con el objeto de la factura de Stripe. El front
  ya lee `paymentData.total ?? amount_paid ?? amount_due` y
  `paymentData.invoice_pdf`, así que esto arregla R10 —filas a 0,00 €, sin
  número y sin PDF— **sin tocar el front**. `inviceData`, con su typo, se retira.
- **No se crean documentos por accidente (R5).** Se escribe con `update()` sobre
  un ref conocido, o con una creación explícita. `set(merge: true)` sobre un id
  que no existe queda prohibido en este camino.
- **Se espera la escritura (R13).** `updateInvoice` hace `await` de su `set`; hoy
  no, lo que significa que ningún cambio de estado de factura está garantizado.
- **El bucle de R16 desaparece por construcción**, no por parche: el trigger
  `processInvoices` que escucha `onCreate` de `invoices` es el trigger del cron,
  y el cron se retira (D1). Sin ese trigger, escribir en `invoices` no puede
  disparar facturación. Por eso en `04_fases.md` la retirada del cron va
  **antes** de tocar `invoice.paid`.

### Emails y dunning

- **La factura la manda la plataforma (D5, invertida el 2026-08-26).** Al recibir
  `invoice.finalized` se descarga el PDF de Stripe (`invoice_pdf`, URL firmada
  que no pide clave), se comprueba que es un PDF de verdad y se manda adjunto por
  el canal SMTP de siempre, con plantilla `INVOICE` en `emails_template` (es/en).
  El PDF no se almacena en ningún sitio: viaja en memoria y se descarta, porque
  el binario ya vive en Stripe.

  El motivo del cambio es el que originó toda la investigación: **trazabilidad**.
  Delegando en Stripe no hay forma de responder «¿le llegó la factura a este
  cliente y cuándo?». Cada envío deja ahora un documento en
  `invoice_emails/{stripeInvoiceId}` con su desenlace: `sent` con `sentAt` y
  destinatario, `skipped` con el motivo (`importe_cero`, `sin_destinatario`) o
  `failed` con el error y los intentos. El cerrojo se resuelve en transacción:
  lo enviado no se reenvía nunca, lo fallido sí, y un envío a medias se retoma
  a los diez minutos.

- **El interruptor de Stripe se queda APAGADO.** *Settings → Billing → Customer
  emails → «Send finalized invoices and credit notes to customers»*. Encenderlo
  con esto en marcha significa **factura por duplicado**. No se puede tocar por
  API: es solo dashboard, así que la única protección es que esté escrito aquí.
  Conviene mirar de paso «Successful payments», que manda el recibo del cobro —
  no es la factura, pero al cliente se lo parece.

- **Las de 0 € no se mandan.** Inicios de prueba y cupones al 100% generan
  facturas a cero que solo desconciertan a quien las recibe. Quedan registradas
  como `skipped` con el motivo, no se envían.
- **Sigue haciendo falta un destinatario.** Se resuelve por `entity.billingEmail`
  y, si la entidad no aparece o no lo tiene, por el email del Customer de Stripe.
  Si no hay ninguno de los dos, la factura queda registrada como `skipped` /
  `sin_destinatario` — reintentar no arregla que no haya a quién escribir, pero
  al menos queda a la vista a quién hay que rellenárselo. `configBilling` deja de
  crear Customers sin email y un backfill rellena los existentes.
- **Aviso propio de impago (D4).** Nuevo `EmailType.PAYMENT_FAILED` —el enum hoy
  no tiene ningún tipo de factura— disparado desde `invoice.payment_failed`, con
  el estado del reintento y el enlace al portal. Se elimina el filtro
  `includes("check")` que hoy hace que un impago de passinbiz no se registre
  nunca (R17).
- **Sin bloqueo de servicio (D4).** Stripe reintenta según su política y nosotros
  informamos. Ningún camino de código degrada el servicio por impago.

### `deleteEntity`

La guarda de impagos actual fabrica una factura para averiguar si hay deuda:
llama a `InvoicePaymentProcessor.execute(entityId, "-", true)`, que adjunta ítems
a la factura `"-"` y termina en 500 (R15). Hoy no se alcanza porque no hay planes
con precio, así que **la guarda es código muerto y toda entidad se borra sin
comprobar nada**.

Se sustituye por un caso de uso que **pregunta** en vez de crear:
`HasOutstandingInvoices(entityId)` lista las facturas del Customer en estado
`open` / `past_due` / `uncollectible` y devuelve 400 `payment/pending` con el
detalle. No crea nada en Stripe, así que no puede quemar un número.

## Cómo queda el ciclo

```
1. configBilling   → Customer con email garantizado + portal
2. subscribe       → doc pending + suscripción Stripe (items según BillingMode)
                     + idempotency_key
3. customer.subscription.created/.updated → estado real en Firestore,
                     endTestPeriod desde trial_end
4. (uso) passinbiz → meterEvent por emisión, identificador idempotente
5. invoice.upcoming → por cada item, ChargeStrategy resuelve quantity.
                      Fallo ⇒ 5xx ⇒ Stripe reintenta. Se registra en billingRuns
6. invoice.created  → se compara el draft con lo esperado.
                      Discrepancia ⇒ se corrige la línea (aún sin número fiscal)
7. invoice.finalized → Stripe asigna número EBZSTRIPE; la plataforma descarga el
                      PDF, lo manda adjunto y registra el envío en invoice_emails
8. invoice.paid | .payment_failed → proyección en invoices (update, no create);
                      en fallo, dunning de Stripe + aviso propio
9. unsubscribe      → cancel_at_period_end + arrastre de add-ons.
                      Stripe liquida el uso pendiente en la factura final
```

Y en paralelo, un vigilante diario que compara Firestore con Stripe y **solo
informa**.

## Qué se retira

| Pieza | Motivo |
|---|---|
| `firebaseEntrySchedule-triggerInvoiceWorker` | D1: segundo motor |
| `firebaseFirestoreTriggers-processInvoices` | Trigger del cron; su retirada elimina R16 |
| `InvoicePaymentProcessor` como emisor | Ningún camino propio emite facturas |
| `GetCountPayPerUse` | Sustituido por el registro de `ChargeStrategy` |
| `handleCancelSub` (checkout de saldo) + estado `pending-pay` | Stripe liquida el uso en la factura final |
| Campo `inviceData` | Sustituido por `paymentData` (R10) |
| Sobrecarga `handleSubscriptionUpsert(event)` | Mentira de tipos que habilita R14 |

## Cabos sueltos y riesgos

- **Passinbiz medido cambia lo que paga el cliente.** Hoy sus suscripciones
  facturan 0,00 € (R4). Activar el cobro por emisión es un **go-live de negocio**,
  no un despliegue: empieza a cobrar por primera vez a clientes que llevan meses
  sin pagar. Va en la última fase y con aviso previo a esos clientes.
- **R8 sigue sin confirmar en producción.** Si algún plan de
  `service/{id}/plan/{planId}` tiene `stripePrice` con valor, retirar el cron
  podría dejar de cobrar algo real. Es un **gate de verificación** antes de la
  fase que lo retira, no una suposición.
- **La ventana del draft no está garantizada.** El retardo de `invoice.upcoming`
  y la duración del draft son ajustes del dashboard de Stripe. El diseño no debe
  depender del valor exacto: la capa 3 es una segunda oportunidad, no la
  principal.
- **El precio del add-on de Rentman sigue abierto** (D6a). El diseño es agnóstico
  al número, pero la Fase 5 no puede cerrarse sin él.
- **`countSource` es un contrato entre módulos.** Un `countSource` mal escrito en
  Firestore deja un plan sin contador. Debe fallar ruidosamente —y no facturar—
  en lugar de devolver 0 en silencio, que es exactamente el fallo del as-is.

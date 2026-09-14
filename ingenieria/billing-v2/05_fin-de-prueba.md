# El primer corte: qué pasa cuando acaba la prueba (5 sep 2026)

Nota de trabajo, no diseño cerrado. Se abre porque el 4 de septiembre una prueba
en dev terminó **sin cobrar en la primera iteración**, y al mirarlo aparece un
hueco que ni `01_as-is.md` ni `02_to-be.md` cubren: los dos documentos razonan
sobre el ciclo mensual —«cada ciclo, `invoice.upcoming`»— y **ninguno habla de la
primera factura**, la que Stripe emite al terminar el trial de 45 días. Que es,
para la caja, la más importante de todas: es el primer euro que entra por cada
cliente nuevo.

No hay que escribir código todavía. Esto queda anotado para retomarlo.

## El hecho, y lo que todavía no es un hecho

**Observado.** El 4 de septiembre de 2026, en el entorno de desarrollo, una
suscripción de prueba llegó a su primer corte y no generó cobro.

**Observado en el código** (`services/billing`, en producción desde el 04-09):

- `Subscribe` fija la `quantity` **en el instante del alta**, con lo que devuelva
  `GetCountPayPerUse` en ese momento. Para checkinbiz eso es la plantilla viva.
  Una entidad recién creada no tiene empleados todavía —primero se contrata el
  servicio, después se da de alta a la gente—, así que nace en **cero**.
- El **único** punto que vuelve a contar es `invoice.upcoming`
  (`StripeWebhookHandler.refreshSubscriptionQuantity`). No hay ningún manejo de
  `customer.subscription.trial_will_end`.

**Consecuencia si el recuento no llega a tiempo:** la factura del día 45 sale a
0 €, y el primer importe real es el del día 75. Un mes de retraso sobre lo
previsto, encima de los 45 días de prueba: **2,5 meses desde el alta hasta el
primer ingreso**. Es el síntoma que motivó esta nota.

**Hipótesis principal, SIN verificar.** Que `invoice.upcoming` no esté suscrito
en el endpoint del webhook. Las notas del alta del endpoint de dev
(`we_1U8be9R97dgHV4NJYIdAy2Tv`, 2026-08-26) solo mencionan `invoice.finalized`, y
lo mismo dice la lista de tareas para el endpoint de producción. Si es así, el
recuento no se ejecuta **nunca** —ni en el primer corte ni en los siguientes— y
el fallo es silencioso por diseño: un evento no suscrito no produce error, no
deja rastro en el log y no distingue de un evento que llegó y no hizo nada.

No está confirmado. **Es lo primero que hay que mirar**, y no requiere esperar a
otro ciclo de prueba: es la lista de eventos del endpoint, en dev y en prod.

`01_as-is.md` ya lo dejó anotado en agosto bajo «Qué no se ha podido verificar»:
*«qué eventos tiene realmente suscritos el endpoint del webhook en Stripe»*. El
cabo suelto se quedó suelto.

## Cómo se distingue una cosa de la otra

Dos datos, en la siguiente prueba, y se cierra el diagnóstico:

1. Si en el log de billing aparece `ajustada a N unidades antes de cobrar`. Si no
   aparece, el evento no llegó. Si aparece con `N` mal, el recuento cuenta mal.
2. La `quantity` que tiene la suscripción en Stripe al llegar el corte.

## Qué se hace, y en qué orden

**Primero, la casilla.** Suscribir `invoice.upcoming` en el endpoint —dev y
prod—. Si la hipótesis es correcta, esto solo ya arregla el ciclo mensual y
probablemente también el primer corte: `invoice.upcoming` dispara antes de la
factura de fin de prueba, no solo antes de las renovaciones.

**Segundo, `customer.subscription.trial_will_end`.** Es el evento que Stripe
tiene hecho para esto y salta **tres días antes** de que acabe el trial. Conviene
dejar claro qué es y qué no es: **no hace nada nuevo**. Ejecuta el mismo recuento
que `invoice.upcoming`, contra la misma función. La diferencia es *cuándo* llega
—atado al fin de la prueba, no al corte de facturación— y que da un segundo
disparador para el momento que más dinero mueve. Es cinturón además de tirantes,
no un mecanismo aparte.

Encaja como **capa 0** de las cuatro de «La red debajo de `invoice.upcoming`»
(§ `02_to-be.md`), y comparte con la capa 3 (`invoice.created`) la misma razón de
ser: que el ajuste no dependa de un solo aviso.

**Tercero, y esto es lo que de verdad cambia la naturaleza del fallo:** la lista
de eventos suscritos en Stripe **es parte del diseño, no configuración de
consola**. Hoy vive en la cabeza de quien dio de alta el endpoint. Tiene que
estar escrita aquí, verificarse en el guion del pase a producción, y —mejor— ser
comprobable desde el propio servicio al arrancar. Un evento que falta no avisa de
que falta: es la misma familia de fallo que R11 del as-is, donde el único punto
de cálculo fallaba en silencio.

## Lo que no entra en esta nota

Se quedan fuera a propósito, para no mezclar: el aviso al cliente de que su
prueba termina, la comprobación de método de pago antes del corte, y
`trial_settings.end_behavior.missing_payment_method` (hoy en el valor por
defecto: sin tarjeta, factura abierta que nadie paga y servicio funcionando
gratis). Son decisiones de producto con su propia conversación.

## Decisión de producto abierta

**¿Cuál es el mínimo facturable al terminar la prueba?** Hoy, si un cliente llega
al día 45 con cero empleados, se le factura 0 € y es correcto según el código.
`Plan.minItemsPay` existe en Firestore y **`Subscribe` no lo aplica nunca** —solo
se usa al darse de baja, en `Unsubscribe`—. Si debe haber un suelo, hay que
decidir el número; mientras no se decida, el comportamiento es el actual.

## Pendiente con fecha

**Entregalia termina prueba el 27 de septiembre de 2026 con `quantity: 0`** (alta
el 13 de agosto). Ninguna de las capas de arriba la salva si se programan
después: hay que corregir esa suscripción a mano en Stripe antes de esa fecha, o
se repite la historia con un cliente real. Mismo caso, ya consumado, en
ACB2PAINTING: factura 0 € desde el 5 de marzo.

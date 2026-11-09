# 06 — Decisiones abiertas y aplazadas

Lo que falta por responder, y lo que se ha aplazado con su boceto para no discutirlo desde
cero. Ninguna bloquea la Fase 0; D1 bloquea el alta en Stripe de la Fase 0, no el código.

---

## D1 — Precio del portal del cliente (fase dos)

**Bloquea:** el precio en Stripe de la Fase 6; nada de las Fases 0 a 5, que son gratis
(decidido el 2026-11-03: la cartera básica es core).
**Estado:** sin decidir.

**Recomendación:** la mecánica de inventario y el quiosco: plan único `standard`, 15 días de
prueba, factura aparte, importes en Stripe y no en el código. Queda una decisión de forma:
**por plantilla** (tramos sobre empleados, como inventario) o **por cliente con portal
activo** (lo que paga la empresa crece con lo que vende). La segunda es más honesta con el
valor y más fácil de repercutir al cliente final, pero exige que la cantidad en Stripe sea
«contactos con acceso activo», un recuento nuevo. Recomiendo la segunda si el recuento sale
barato de mantener; si no, la primera. Sin tope de clientes, lugares ni accesos: **un límite
de plan nunca para el servicio**.

---

## D2 — Neteges: quién confirma qué sucursal es qué

**Bloquea:** ejecutar `branches-to-customers --apply` en producción. No bloquea la demo.
**Estado:** sin respuesta de Neteges.

El script convierte sucursales en clientes uno a uno, pero hay cuatro parejas de centros que
comparten edificio (la demo lo detectó: 142 centros, 138 ubicaciones). ¿Son un cliente con
dos lugares, o dos clientes? Y la sucursal base, la que se queda, ¿es «Oficina Badalona» o
una por zona? Hace falta que lo digan ellos con la lista delante. Hasta entonces, el script
se queda en simulación y la demo sigue siendo demo.

---

## D3 — Qué ve el trabajador del cliente por defecto

**Bloquea:** el valor por defecto de `visibleToWorkers` en el contacto y de `visibleToRoles`
en el documento del cliente.
**Estado:** propuesto, sin confirmar.

**Propuesta:** por defecto **nada**. El contacto no se ve salvo que se marque; el documento no
se ve salvo que lleve `worker`. En limpieza casi siempre querrán marcar el teléfono del
portero; en SAD, el de la hija de Juana es otra cosa. Es más seguro empezar cerrado y que la
empresa abra, que al revés. Con la pega de que una empresa de limpieza tendrá que marcar la
casilla en cada contacto; si duele, se añade un valor por defecto por empresa.

---

## D4 — El contrato, ¿cuenta visitas?

**Bloquea:** nada en v1.
**Estado:** aplazado.

Una comunidad contrata «dos limpiezas por semana». El contrato podría llevar la frecuencia y
el informe comparar lo contratado con lo hecho. Es útil y es barato de guardar, pero
compararlo bien exige saber qué tarea cuenta como «limpieza» y cuál no, y eso es un tipo de
tarea que hoy no existe. Se guarda la idea, se escribe el contrato con fechas y documento, y
se vuelve cuando alguien lo pida con un caso.

---

## D5 — Tarifa por tipo de tarea

**Bloquea:** nada en v1.
**Estado:** aplazado.

La tarifa va por cliente y por lugar. Una tarifa por tipo de trabajo («cristales a 22 €,
limpieza general a 18 €») necesita el mismo «tipo de tarea» que D4. Si llega, la tarifa gana
una tabla por tipo y el importe se calcula por tarea en vez de por hora. El modelo de
`customer_hours_daily` lo soporta porque ya guarda `task_id`.

---

## D6 — Cliente al fichar sin tarea

**Bloquea:** nada.
**Estado:** aplazado, con boceto.

En una sucursal con varios clientes y gente en Semana tipo o Por turnos, las jornadas no se
imputan a nadie salvo que haya tarea. El boceto es un selector de cliente en el gesto de
fichar cuando la sucursal tenga varios clientes y la persona no tenga tarea en ese momento,
guardado en el checklog. Es una versión de app y una decisión sobre el gesto de fichar, que
hoy es sagrado. **No se hace mientras la tarea resuelva el caso**, y en SAD y limpieza lo
resuelve.

---

## D7 — El evento y la obra como «lugar con fechas», ¿basta?

**Bloquea:** nada en v1.
**Estado:** decidido para v1: **sí, basta**.

Se barajó un nivel «proyecto» entre el cliente y la tarea. Se descartó el 2026-10-29: en
construcción el proyecto ya existe y se llama sucursal (es donde fichan), y en eventos el
lugar con `startsAt`/`endsAt` cubre la boda del 14 de junio. El 2026-11-03 el «proyecto»
recibió nombre sin recibir entidad: **el montaje es una sucursal o una tarea con un contrato
vinculado** ([ADR-006](./adr/ADR-006-el-contrato-es-el-montaje.md)). Si una constructora pide
control por capítulos dentro de una obra, eso son tareas con contrato dentro de la sucursal.
Si pide algo más, se vuelve aquí con el caso.

---

## D8 — Lo que Merlin y el panel operativo hacen con el cliente

**Bloquea:** nada.
**Estado:** fuera de v1, como hizo inventario con su TDR-006.

Con las horas por cliente en Postgres, Merlin puede narrar («Diagonal 400 lleva un 20 % menos
de horas que el mes pasado») y el panel operativo puede agrupar por cliente. Es un TDR aparte
cuando la Fase 3 esté en producción y haya datos que mirar.

---

## D9 — Borrar las sucursales falsas de Neteges

**Bloquea:** nada. Es de ellos.
**Estado:** no lo hace el script.

Convertidas las sucursales en clientes y recolocadas las tareas, las 134 sucursales siguen
ahí con su historial de fichajes. Borrarlas pierde ese historial en las pantallas que
filtran por sucursal. La recomendación es dejarlas, inactivas si el panel lo permite, y que
sea Neteges quien decida cuándo. El script lo lista en la simulación y no las toca.

---

## D10 — Los adjuntos de la tarea no se convierten en documentos del cliente

**Bloquea:** nada.
**Estado:** cerrada el 2026-11-03 por Jose.

El TDR-007 deja subir ficheros a la tarea (`isEvidence: false`) y así se queda: hay empresas
que no van a relacionar clientes y siguen subiendo a la tarea directamente. La Fase 4 añade
los documentos del cliente **al lado**, no en sustitución, y no hay script que convierta ni
mueva los adjuntos existentes.

---

## D11 — El corte del MVP de clientes

**Estado:** CERRADA por Jose la noche del 2026-11-03, tras debate. «En esta versión no vamos a
contemplar horas por clientes; vamos a sacar un MVP de clientes y después agregamos subcapas, si
no no vamos a salir del hueco.»

**Por qué.** El fichaje nunca va sin sucursal pero sí puede ir sin tarea (horario por turnos), y
en una sucursal con varios clientes no hay forma honesta de saber de quién fue cada hora fichada.
Resolverlo exige bajar un nivel (lugares, dedicadas, o preguntar al fichar), y cada nivel es un
concepto más que explicar. Se aplaza entero; la cartera arranca como capa opcional que no
condiciona nada de lo que ya funciona.

**Lo que entra en el MVP**
- Ficha del cliente: tipo, nombre, NIF, referencia, **dirección**, contactos con «lo ve quien va a
  trabajar», notas de campo y de gestión (Markdown), y sus **sucursales, al menos una** (sin
  «toda la empresa»: un cliente sin sucursal no es nada, como el almacén).
- En la tarea: **después de elegir sucursal y solo si tiene clientes asignados**, se elige uno;
  la **dirección del cliente entra por defecto como valla**, con un check para quitarla. El
  detalle enseña el cliente; la lista filtra por cliente.
- La app, cuando se publique versión: un bottom sheet de «datos del cliente» desde la tarea con
  nombre, notas de campo y contactos visibles (del snapshot `task.customer`). Hasta entonces la
  tarea funciona igual, con la valla del cliente.

**Lo que sale de la pantalla (la API lo conserva sin usarse hasta un pase tranquilo)**
- Lugares del cliente (`sites`), sucursales dedicadas (`dedicatedBranchIds`), `scope: "entity"`.

**Lo que se aplaza**
- Horas por cliente, espejo e informe (antigua Fase 3): sin fecha. ADR-003 queda sin efecto.
- Script de Neteges (`branches-to-customers`): **descartado hasta tener todo claro**.
- Tarifas, rentabilidad y portal: siguen **definidos en la Fase 5** (ADR-006) y la Fase 6; no
  salen en esta versión.

**Lo primero que se añade después del MVP:** documentos del cliente con los roles del módulo de
documentos (la ficha del SAD para el trabajador, el contrato para dirección), visibles desde cada
tarea del cliente. Es la Fase 4 (hecha el 04-nov, TDR-003). Después, la Fase 5 (TDR-004), que
sigue con la pregunta **core o add-on** abierta: la API se construye sin puerta y con su sitio
(`requireProfitability`); la decisión es precio y bloquea el pase a producción, no el código.

---

## D17 — Del qué cuelga el contrato

**Estado:** CERRADA por Jose el 2026-11-05: «un cliente puede tener varios contratos a
la vez; un contrato no puede colgarse de la sucursal sino del cliente, como un documento más».
Se retira el vínculo a sucursal (ADR-006 §2 y la propuesta del 04-nov de «sucursal si el cliente
está solo»). Con varios contratos vigentes, **la tarea dice de cuál es**: lo pide solo cuando el cliente
tiene más de uno vigente, y con uno se pone solo (Jose: «tu recomendación me parece bien»).

## D18 — Quién ve el importe, el coste y el margen

**Estado:** CERRADA por Jose el 2026-11-05: «como lo dices». Importe, coste, margen y lo leído
por la IA, solo owner y admin; el resto ve horas. Y en el documental: el contrato y el
presupuesto del cliente son **documentación administrativa**; al subirlos la visibilidad sale
en gestores, y marcar supervisores o trabajadores se puede, pero con aviso en rojo («puedes
revelar documentación sensible a los empleados»). Hecho en el panel el 05-nov
(`ADMINISTRATIVE_CUSTOMER_TYPES` en `documentUi.tsx`).

## D11 bis — Core o add-on

**Estado:** CERRADA por Jose el 2026-11-05: la rentabilidad es **core**. «El add-on es la capa
de app cliente» (el portal, Fase 6). Quitado `requireProfitability`.

## Contratos en su propia pestaña de la ficha (anotado el 2026-11-08)

Jose lo propuso como **sugerencia**: Contratos, en una pestaña aparte de la ficha del cliente (Detalle / Contratos / Análisis), que solo se cargue al abrirla, por rendimiento y para ordenar una ficha que puede crecer sin fin. **Decidido: se sale así**, con los contratos en el Detalle. Lo que sí se hace ya es la paginación con «Cargar más» y alto máximo en Documentación, Contratos, Gastos sin contrato y los gastos de cada contrato, con los totales de todo (la API de contratos pagina con `limit`/`cursor`). Se retoma cuando la ficha lo pida.

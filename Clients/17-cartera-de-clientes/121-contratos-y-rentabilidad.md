# Contratos y rentabilidad

Un contrato con un cliente fija un importe y, a menudo, unas horas. Lo difícil es saber, mientras se trabaja, si se va a cumplir: si las horas alcanzan, si el coste se come el margen. En CheckBiz360 cada contrato junta su importe con las tareas que se hacen para él y con lo que se paga fuera, y enseña el margen mientras todavía se puede hacer algo.

Los contratos están en la ficha de cada cliente, pestaña **Detalle**, bloque **Contratos**.

---

## Qué resuelve

- **Saber si un contrato deja dinero**, con las horas y los gastos reales, no con una estimación de memoria.
- **Ver venir el problema.** Las horas hechas frente a las previstas, en rojo cuando se pasan, y la fecha aproximada en que el coste superaría el importe.
- **No teclear el contrato.** La IA lee el PDF y propone importe, fechas y horas, con la frase de la que sale cada dato.
- **Ir del contrato a sus tareas y volver.** Cada contrato lista sus tareas y cada tarea enlaza con su contrato.
- **Prever el siguiente.** Con los contratos cerrados, la plataforma estima horas, coste y margen de los nuevos.

---

## Antes de empezar

- La rentabilidad necesita que las personas tengan su **tarifa horaria** en la sucursal. Sin ella, sus horas se cuentan pero no cuestan, y el contrato avisa de que el coste se queda corto. Ver [Qué es la cartera de clientes](./117-que-es-la-cartera-de-clientes.md#antes-de-empezar-el-precio-de-los-puestos).
- Crear, editar, cerrar y borrar contratos, y ver importes, costes y márgenes, es cosa del **propietario y los administradores**. Managers y supervisores ven los contratos de sus clientes con sus horas y sus tareas, sin dinero.

---

## Crear un contrato

Un cliente puede tener **varios contratos a la vez** (por ejemplo, el mantenimiento anual y un trabajo puntual).

1. En la ficha del cliente, bloque **Contratos**, pulse **Nuevo contrato**.
2. En **Documento del cliente**, elija el PDF del contrato o del presupuesto si ya lo subió a **Documentos**; o pulse **Subir PDF** para subirlo ahora (solo PDF, hasta 10 MB). El documento queda guardado como contrato del cliente, visible solo para Administración. Si no tiene PDF, deje **Sin PDF**.
3. Con un PDF elegido, puede pulsar **Leer el PDF** (ver más abajo).
4. Rellene o revise:
   - **Nombre del contrato** (obligatorio).
   - **Empieza** y **Acaba**. Deje **Acaba** vacío si es indefinido.
   - **Importe (€)**: el precio cerrado con el cliente, **sin IVA**.
   - **Horas estimadas**: horas de trabajo, no días.
   - **Complejidad**, de *1 · Sencillo* a *5 · Muy complejo*. Sirve para comparar con contratos parecidos al prever.
   - **Notas**.
5. Guarde.

### Leer el PDF con IA

**Leer el PDF** lee el documento y rellena el importe, las fechas, las horas y la complejidad. Debajo de cada dato aparece la frase de la que sale, *Del documento: «…»*, o *No está en el documento*. **Revise lo leído antes de guardar**: la IA propone, usted decide.

Si el documento no parece un contrato ni un presupuesto, el formulario lo avisa. Un PDF escaneado como imagen, sin texto, no se puede leer: rellene los datos a mano.

> **Privacidad.** Antes de leerlo con IA, se quitan del documento los nombres de personas y empresas, DNI y CIF, direcciones, teléfonos, correos y cuentas bancarias: al modelo solo le llega el resto. Aun así, suba solo lo que haga falta leer y nunca datos de salud. El aviso aparece en el propio formulario.

---

## Qué tareas son de un contrato

Cada tarea dice de qué contrato es en su desplegable **Contrato** (ver [El cliente en la tarea](./119-el-cliente-en-la-tarea.md#el-contrato-de-la-tarea)):

- Al crear una tarea, si el cliente tiene un único contrato vigente, viene propuesto.
- **Sin contrato** la deja fuera de todos, y se respeta.
- Crear un contrato, cambiar sus fechas o reabrirlo **no se lleva tareas**: una tarea solo cambia de contrato cuando se elige en ella.

---

## La tarjeta del contrato

Cada contrato es una tarjeta con su nombre, su periodo (*Del … al …* o *Indefinido*) y su estado (**En curso** o **Cerrado el …**). Si algo no cuadra, una marca de **avisos**. Pulse **Expandir** para ver el detalle.

| Cifra | Qué es |
|---|---|
| **Importe** | El precio del contrato, sin IVA. |
| **Horas planificadas / hechas / previstas** | *Planificadas*: las que suman sus tareas, de su inicio previsto a su vencimiento, por cada persona asignada. *Hechas*: las trabajadas, según los fichajes de sus tareas o, si no los hay, cuándo se empezaron y se terminaron. *Previstas*: las **Horas estimadas** del contrato (si no las puso, solo salen las dos primeras). En rojo si las hechas pasan de las previstas. |
| **Coste en bruto** | Las horas hechas por la tarifa de cada persona (sin cargas sociales), más el material consumido en sus tareas si tiene inventario, más los gastos aprobados del contrato. En rojo si ya pasa del importe. |
| **Margen** | Lo que queda del importe después del coste, en euros y en porcentaje. |

Debajo:

- **Tareas (n)**: cada tarea del contrato con su estado, su fecha y sus personas, de la más reciente a la más antigua, de 5 en 5 con **Cargar más**. El nombre de la tarea lleva a su ficha; desde la ficha de la tarea, el contrato lleva de vuelta aquí.
- El coste del material y qué parte de las horas tiene tarifa, si no la tienen todas.
- **Gastos por aprobar** y **Gastos externos**. Ver [Gastos del contrato y de la tarea](./122-gastos-del-contrato-y-de-la-tarea.md).
- **Previsión** (ver más abajo).

Encima de las tarjetas, **Total del cliente**: lo contratado, el coste y el margen de todos sus contratos.

### Los avisos

| Aviso | Qué hacer |
|---|---|
| *Ninguna tarea es todavía de este contrato.* | Elija el contrato en las tareas que le correspondan. |
| *Hay horas de personas sin tarifa: el coste se queda corto.* | Ponga la tarifa horaria a esas personas en su sucursal. |
| *Hay material sin coste unitario: cuenta en cantidad, no en importe.* | Ponga el coste en la ficha del artículo de inventario. |
| *Hay jornadas sin hora de salida: no se valoran.* | Corrija esas jornadas para que cuenten. |
| *Algunas tareas no tienen fichajes: sus horas salen de cuándo se empezaron y terminaron.* | Es informativo: esas horas son aproximadas. |

---

## La previsión

Con los contratos ya **cerrados** como referencia, cada contrato en curso con horas estimadas enseña:

- **Horas previstas**: un intervalo, con la cifra más probable.
- **Coste previsto** y **Margen previsto**.
- Si a este ritmo el coste pasaría del importe, **hacia qué fecha**.

Se compara con contratos parecidos (de la misma complejidad cuando los hay). Mientras no haya bastantes contratos cerrados, lo dice: *Aún no hay suficientes contratos cerrados para prever*. Sin horas estimadas: *Pon las horas estimadas para tener previsión*.

---

## Editar, cerrar, reabrir y borrar

- **Editar** cambia los datos del contrato y permite añadir o quitar gastos externos.
- **Cerrar contrato**: cuando termina el trabajo. Sus cifras pasan al histórico con el que se prevén los siguientes. Se puede **Reabrir**.
- **Borrar**: solo si ninguna tarea es de ese contrato. Si ya tiene tareas, ciérrelo.

Las tareas de un contrato cerrado siguen siendo suyas y se pueden editar. Lo que no se puede es elegir un contrato cerrado para una tarea nueva.

---

## Problemas frecuentes

**El margen sale muy alto o el coste sale vacío.** Faltan tarifas horarias: el contrato lo avisa. Póngalas en la vinculación de cada persona con su sucursal.

**Las horas hechas son cero aunque se ha trabajado.** Las tareas no son de ese contrato: ábralas y elíjalo en **Contrato**.

**«Leer el PDF» no rellena nada.** El PDF es una imagen escaneada o no es un contrato. Rellene los datos a mano.

**No veo el importe ni el botón Nuevo contrato.** Solo lo ven propietarios y administradores.

**No me deja borrar un contrato.** Tiene tareas. Ciérrelo en su lugar.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [El cliente en la tarea](./119-el-cliente-en-la-tarea.md) | El desplegable de contrato en la tarea |
| [Gastos del contrato y de la tarea](./122-gastos-del-contrato-y-de-la-tarea.md) | Lo que se paga fuera y cuenta en el coste |
| [Documentos del cliente](./120-documentos-del-cliente.md) | El PDF del contrato y quién lo ve |
| [El cliente en los análisis](./123-el-cliente-en-los-analisis.md) | La rentabilidad del cliente mes a mes y las alertas de contrato |
| [Crear y gestionar empleados](../02-empleados/06-crear-y-gestionar-empleados.md) | Dónde se pone la tarifa horaria |

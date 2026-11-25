# Complementos: conducción, festivo, nocturnidad

El convenio o el acuerdo con la plantilla dicen que ciertos trabajos se pagan aparte: conducir más de cien kilómetros, trabajar en festivo, hacer noche, un plus de peligrosidad. Hasta ahora eso se anotaba fuera y el coste de la tarea salía corto.

Los **complementos** son lo que una persona cobra **además** del precio de su puesto por una tarea o un turno concreto. Se definen una vez en el catálogo de su empresa y se eligen después, al asignar la tarea o al cargar el turno de quien los cobra. El fichaje los guarda, y el informe de tareas, los contratos y los análisis los suman al coste, desglosados.

---

## Qué resuelve

- **Costear la tarea con lo que de verdad cuesta**, pluses incluidos.
- **No teclear cantidades cada vez.** El complemento se define una vez; en la tarea solo se elige.
- **Tener la traza.** El informe dice qué complemento cobró cada persona, en qué tarea, por qué fichaje y cuánto importó.

---

## Los tres tipos

| Tipo | Qué significa | Ejemplo |
|---|---|---|
| **Fijo** | Un importe por tarea o por sesión de fichaje, sin mirar las horas. | Plus de conducción: una cantidad por el día que conduce. |
| **Por hora** | Un importe por cada hora trabajada, además del precio del puesto. | Nocturnidad como cantidad por hora. |
| **Porcentaje** | Un porcentaje sobre el precio por hora del puesto. | Festivo: *25* significa un 25 % más sobre el precio por hora. |

Un porcentaje se calcula sobre el precio del puesto con el que se hizo el trabajo, así que un mismo «Festivo, 25 %» vale distinto para un oficial y para un peón. Es lo que suele decir el convenio.

---

## Crear el catálogo

Los complementos están en **Entidad**, pestaña **Complementos**. El mismo catálogo se abre también en una ventana desde donde se usa: el botón **Catálogo de complementos** está al asignar la tarea, en **Puesto y complementos** y en el editor del turno, para crear el que falte sin salir de lo que estaba haciendo.

1. Pulse **Añadir complemento**.
2. Escriba el **Nombre**, como lo nombra su convenio: *Plus de conducción*, *Festivo*, *Nocturnidad*.
3. Elija el **Tipo**: *Fijo*, *Por hora* o *Porcentaje*.
4. Ponga el **Importe** (o el **Porcentaje**, de 0 a 500).
5. Guarde.

No puede haber dos complementos con el mismo nombre. **Editar** cambia nombre, tipo o valor para lo que se elija a partir de entonces: **lo ya asignado conserva el valor que tenía al elegirlo**. **Dar de baja** lo quita de los selectores sin borrar nada; lo que ya lo tenía no cambia, y se puede **Reactivar**.

El valor de los complementos solo lo ven y lo editan el **propietario y los administradores**. Los gestores ven el catálogo por nombre y pueden elegirlos en tareas y turnos, sin ver importes.

---

## Elegirlos en la tarea o en el turno

Un complemento es **de una persona en un trabajo concreto**, no de la tarea entera: en una tarea de tres personas puede cobrarlo solo quien conduce.

| Dónde | Cómo |
|---|---|
| **Al asignar una tarea** | En la fila de cada persona asignada, pulse **Complemento** y elija uno del catálogo; repita si cobra más de uno. Cada uno sale como una etiqueta que se puede quitar. Ver [Asignar tareas a empleados](../06-tareas/41-asignar-tareas-a-empleados.md#con-qué-puesto-y-qué-complementos). |
| **Desde la ficha de la tarea** | En **Equipo asignado**, la acción **Puesto y complementos** de cada persona permite cambiarlos mientras la tarea no esté completada. |
| **Al cargar un turno** | En **Más opciones** del editor del turno, el campo **Complementos**. Vale para los turnos del cuadrante y para la semana tipo. Ver [Por turnos](../04-calendario-y-horarios/114-calendario-de-turnos-por-fecha.md#el-puesto-y-los-complementos-del-turno). |

Si una persona tiene además [varios puestos](./140-varios-puestos-por-persona.md), en la misma fila elige con cuál va.

Cuando la persona ficha, el fichaje guarda los complementos que tocaban: los de la tarea que inicia o, si no, los del turno. Cada uno se guarda con el valor que tenía en ese momento.

Un complemento **fijo** se cobra una vez por sesión de fichaje (o una vez por la asignación, si la tarea no tuvo fichajes). Los de **por hora** y **porcentaje** van con las horas de esa persona en esa tarea.

---

## Dónde se nota

- **Informe de tareas**: cada fila de persona lleva **Complementos** (los nombres con su valor) y **Complementos (importe)**, y el coste de la persona los incluye. La hoja **Complementos** es la traza, línea a línea. Ver [Informes de tareas](../06-tareas/48-informes-de-tareas.md).
- **Contratos y análisis del cliente**: el coste en bruto del contrato suma los complementos como partida propia, junto al personal, el material y los gastos. Ver [Contratos y rentabilidad](../17-cartera-de-clientes/121-contratos-y-rentabilidad.md).
- **Estadísticas y costes**: el coste de la sucursal, el coste por hora y la desviación económica los incluyen y los dicen aparte.

El informe de jornada no los lleva: es de tiempo, no de dinero.

---

## Qué ve la persona en la app

Nada: ni valores ni importes. Los complementos son una herramienta de administración.

---

## Problemas frecuentes

**No veo la pestaña «Complementos» ni los importes.** Su cuenta es de gestor. El propietario y los administradores crean el catálogo; usted puede elegirlos por su nombre en tareas y turnos.

**No puedo elegir un complemento en la tarea.** El catálogo está vacío o todos están de baja. Créelo en **Entidad → Complementos**, o pulse **Catálogo de complementos** en la propia asignación.

**He corregido el valor de un complemento y el informe no cambia.** Lo ya elegido conserva su valor. Si fue un error en una tarea concreta, quite el complemento de esa persona desde **Puesto y complementos** y vuelva a añadirlo: entra con el valor nuevo.

**Quiero que el festivo o la noche se apliquen solos.** Hoy los complementos se eligen a mano en la tarea o el turno: la plataforma no decide por usted qué día es festivo para su convenio. Cargue el turno del festivo con su complemento.

**Un plus que es una cantidad por kilómetro.** Defínalo como fijo con el importe del tramo habitual, o cree dos (*Conducción corta*, *Conducción larga*). La cantidad exacta por kilómetro no se calcula.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Varios puestos para la misma persona](./140-varios-puestos-por-persona.md) | Puestos con su precio y el predeterminado |
| [Asignar tareas a empleados](../06-tareas/41-asignar-tareas-a-empleados.md) | Elegir puesto y complementos al asignar |
| [Por turnos: el horario son los turnos que usted carga](../04-calendario-y-horarios/114-calendario-de-turnos-por-fecha.md) | «Más opciones» del turno |
| [Informes de tareas](../06-tareas/48-informes-de-tareas.md) | Las hojas Por persona y Complementos |
| [Contratos y rentabilidad](../17-cartera-de-clientes/121-contratos-y-rentabilidad.md) | Los complementos en el coste del contrato |

# Varios puestos para la misma persona

En muchas empresas una persona no hace siempre lo mismo. El montador que un día conduce la furgoneta, la auxiliar que cubre de coordinadora, el camarero que en un evento hace de jefe de sala. Cada puesto suele tener su precio por hora, y hasta ahora la ficha solo admitía uno por sucursal: el coste de ese día salía con el precio equivocado.

Ahora una persona puede tener **varios puestos en la misma sucursal**, cada uno con su precio por hora. Uno de ellos es el **predeterminado**, el que se aplica cuando nadie elige otro. Al asignarle una tarea o cargarle un turno se elige con qué puesto va, y las horas de ese trabajo se valoran con ese precio.

---

## Qué resuelve

- **Pagar y costear cada trabajo con su precio**, no con el del puesto habitual.
- **No duplicar fichas.** Una sola persona, una sola ficha, varios puestos.
- **Saber después qué hizo cada cual.** El informe de tareas dice el puesto con el que trabajó cada persona en cada tarea.

---

## Dónde se configura

En la ficha de la persona, bloque de la sucursal, junto a su responsabilidad. Todos sus puestos en ese centro están en una sola lista, **Puestos en esta sucursal**, cada uno con su **Ocupación** y su **Precio por hora**:

1. Abra **Empleados**, entre en la ficha de la persona y abra la sucursal correspondiente.
2. El primer puesto de la lista es el **predeterminado**, y así lo marca la etiqueta *Predeterminado*. Si la persona tiene uno solo, es ese.
3. Pulse **Añadir puesto** y ponga la **Ocupación** (del catálogo de puestos de su empresa o una nueva) y su **Precio por hora**. Al elegir una ocupación del catálogo, su precio habitual entra solo. El icono de la calculadora convierte un salario mensual o semanal en precio por hora.
4. Repita con cada puesto. **Quitar puesto** lo retira de la lista.
5. Guarde.

Para que otro puesto pase a ser el habitual, pulse **Hacer predeterminado** en su fila: sube a la primera posición. Un puesto no puede estar dos veces en la misma sucursal, y el último de la lista no se puede quitar: toda vinculación tiene al menos un puesto.

Los puestos son **por sucursal**: la misma persona puede tener en cada centro los suyos.

El precio de cada puesto solo lo ven y lo editan el **propietario y los administradores**. Los gestores ven los nombres de los puestos, sin precio.

---

## Dónde se elige el puesto

Con un solo puesto no hay nada que elegir: todo va con ese. En cuanto una persona tiene más de uno en una sucursal, aparece un selector **Como** en tres sitios:

| Dónde | Qué pasa |
|---|---|
| **Al asignar una tarea** | En la fila de cada persona asignada, **Como** ofrece sus puestos de esa sucursal, con el predeterminado marcado. Se puede cambiar después desde **Equipo asignado** en la ficha de la tarea. Ver [Asignar tareas a empleados](../06-tareas/41-asignar-tareas-a-empleados.md#con-qué-puesto-y-qué-complementos). |
| **Al cargar un turno** | En **Más opciones** del editor del turno, el campo **Puesto**. Vale para los turnos del cuadrante y para la semana tipo. Ver [Por turnos](../04-calendario-y-horarios/114-calendario-de-turnos-por-fecha.md#el-puesto-y-los-complementos-del-turno). |
| **Si no se elige nada** | Se aplica el predeterminado. |

Cuando la persona ficha, el fichaje guarda el puesto que tocaba ese día: el de la tarea que inicia, si no el del turno, si no el predeterminado. Cambiar después el precio de un puesto en la ficha **no cambia** lo ya fichado.

---

## Dónde se nota

- **Informe de tareas**: la columna **Puesto** de cada fila dice con qué puesto trabajó la persona, y el precio por hora es el de ese puesto. Ver [Informes de tareas](../06-tareas/48-informes-de-tareas.md).
- **Rentabilidad de los contratos** y **análisis del cliente**: las horas se valoran con el puesto con el que se hicieron. Ver [Contratos y rentabilidad](../17-cartera-de-clientes/121-contratos-y-rentabilidad.md).
- **Estadísticas y costes**: el coste por hora de una persona pasa a ser el efectivo, el de los puestos que de verdad ocupó.
- **Equipos**: un equipo lleva un puesto por persona, el que se da de alta como predeterminado. Los adicionales se añaden después en la sucursal. Ver [Equipos](./99-equipos.md).

El informe de jornada no cambia: es de tiempo, no de dinero.

---

## Qué ve la persona en la app

Nada de precios. Si quiere, el puesto con el que va cada tarea puede aparecer en su detalle en una versión próxima de la app; hoy la app no lo enseña y no hace falta actualizarla para usar esto.

---

## Problemas frecuentes

**No veo la lista de puestos.** Abra la sucursal dentro de la ficha de la persona, debajo de la responsabilidad. Si ve las ocupaciones pero no los precios, su cuenta es de gestor.

**No me sale el selector «Como» en la tarea.** Esa persona tiene un solo puesto en esa sucursal. Añádale el segundo en su ficha.

**He cambiado el precio y el informe del mes pasado sigue igual.** Es lo esperado: cada fichaje guarda el precio que tenía al hacerse. Lo nuevo vale para los fichajes a partir de ahora.

**Quiero que el predeterminado sea otro.** **Hacer predeterminado** en la fila del puesto, y guardar.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Complementos](./141-complementos.md) | Lo que una persona cobra además del precio de su puesto |
| [Asignar empleados a sucursales](../08-sucursales-y-entidad/60-asignar-empleados-a-sucursales.md) | Dónde se pone la responsabilidad, el puesto y el salario por hora |
| [Asignar tareas a empleados](../06-tareas/41-asignar-tareas-a-empleados.md) | El selector «Como» en la asignación |
| [Informes de tareas](../06-tareas/48-informes-de-tareas.md) | Una fila por tarea y persona, con su puesto |
| [Análisis de costes](../07-inteligencia-operativa/54-analisis-de-costes.md) | De dónde sale el coste por hora |

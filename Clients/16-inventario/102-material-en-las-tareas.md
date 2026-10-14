# Material en las tareas

El inventario está pensado para que el material se siga en el mismo sitio donde se sigue el trabajo: la tarea. Esta guía recorre el ciclo completo, de la planificación al cierre.

---

## El ciclo, en cuatro pasos

| Paso | Quién | Qué pasa |
|---|---|---|
| **1. Reservar** | Quien planifica | Se decide qué material necesita la tarea. Queda comprometido en el almacén, pero no sale todavía. |
| **2. Sacar** (opcional) | Quien lleva el almacén | Desde la ficha del almacén o del artículo, **Dar salida** y, en **¿A qué va?**, **Tarea**: el material sale hacia ese trabajo. Si nadie lo hace, la salida la apunta el consumo. |
| **3. Declarar** | El trabajador | Indica cuánto se gastó, previsto o no. |
| **4. Cuadrar** | Quien valida | Lo que quedó sin declarar se resuelve: de lo que salió, cuánto volvió al almacén; de lo reservado, cuánto se gastó. El resto vuelve al almacén. |

Asignar material no es gastarlo: hasta que no se declara o se cuadra, la plataforma no lo da por consumido.

---

## 1. Asignar material al crear la tarea

En el formulario de **Nueva tarea** aparece el bloque **Material para la tarea**:

1. Elija primero la **sucursal**: los almacenes salen de ella.
2. Pulse **Añadir material** y busque el artículo.
3. Si se gasta, indique la **cantidad** (y el almacén si la sucursal tiene varios). Si se presta, elija el **ejemplar**.
4. Cree la tarea. El material se reserva en ese momento.

Si no hay bastante existencia, se reserva igual y se avisa. Si un ejemplar ya está reservado por otra tarea en ese tramo, se indica con qué tarea choca.

---

## 2. El material en el detalle de la tarea

El detalle de la tarea muestra una tabla con todo su material, del tipo que sea:

- Para lo que se gasta: lo reservado, lo que salió, lo gastado, lo devuelto y lo **sin declarar**.
- Para lo que se presta: el ejemplar, su tramo y el estado de la reserva.

Desde ahí, **Añadir material** reserva más y **Declarar consumo** apunta lo gastado desde el backoffice, sobre lo reservado o sobre lo no previsto, sin registrar antes ninguna salida: es lo práctico cuando la tarea se planifica y se cierra desde el backoffice. Las salidas no se dan desde la tarea, sino desde el almacén o el artículo. Un ejemplar se puede **liberar** si ya no hace falta: la plataforma pregunta **¿Dónde queda?** —en la tarea o en un almacén—, porque liberarlo no lo devuelve al almacén (ver [Dónde está cada equipo](./106-donde-esta-cada-equipo.md)). Uno **fuera de regla** se puede reservar igualmente, después de aceptar el aviso.

---

## 3. En la app: el trabajador solo declara el consumo

El trabajador ve el material de la tarea en la propia tarea de la app y tiene un único botón, **Declarar consumo**: viene precargado con lo reservado; si se gastó todo, basta con confirmar. Puede corregir cantidades y añadir lo que gastó sin estar previsto. No tiene que registrar ninguna salida: si el almacén no la dio, la plataforma la apunta al declarar.

Si la sucursal tiene varios almacenes y añade algo no previsto, la app pregunta de cuál salió.

La tarjeta de cada equipo dice dónde está. Un supervisor o superior puede **liberarlo** desde la app, diciendo si queda en la tarea o vuelve a un almacén; el trabajador ve que se libera al completar la tarea.

---

## 4. Cuadrar al validar

Al validar una tarea completada, si queda material sin declarar, la plataforma pide **cuadrarlo** antes de validar:

- De lo que **salió** y nadie declaró: cuánto volvió al almacén; el resto se da por gastado.
- De lo **reservado** que no consta que saliera: cuánto se gastó (llega precargado con todo lo reservado); lo demás vuelve al almacén.

Así ninguna tarea se cierra con material perdido por el camino. En una tarea ya cerrada, la tabla de material enseña lo que se reservó, lo que se liberó al cerrar y, si no se registró nada, lo dice.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Existencias, almacenes y entradas](./101-existencias-almacenes-y-entradas.md) | Cómo se da de alta el material |
| [Validación de tareas](../06-tareas/45-validacion-de-tareas.md) | El paso de validación donde se cuadra el material |
| [Informes de tareas](../06-tareas/48-informes-de-tareas.md) | El material de cada tarea en el informe |
| [Dónde está cada equipo](./106-donde-esta-cada-equipo.md) | Liberar un equipo, lo que hay que recoger y recibirlo en el almacén |

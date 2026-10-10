# Dónde está cada equipo

Un equipo —una fregadora, una furgoneta, un andamio— puede estar libre y, aun así, no estar en el almacén: se usó en una obra y se quedó allí. Esta guía explica cómo sabe la plataforma dónde está cada uno y cómo se recoge. Requiere el complemento de inventario contratado o en prueba.

---

## Libre no es lo mismo que en el almacén

La plataforma separa dos cosas:

- **Si se puede reservar.** Un equipo deja de estar reservado cuando se libera: lo libera la tarea al cerrarse, o un supervisor a mano.
- **Dónde está.** Liberar un equipo no lo devuelve al almacén. Sigue donde estaba hasta que alguien diga otra cosa, y la plataforma lo apunta.

Así, un equipo libre puede reservarse enseguida para otra tarea, y a la vez se sabe que sigue en la obra y que alguien tiene que ir a por él.

---

## Qué mueve a un equipo de sitio

| Qué pasa | Dónde queda |
|---|---|
| Se da de alta | En su almacén base. |
| Su tarea empieza | En el sitio de la tarea. |
| Su tarea se cierra | Sigue en el sitio de la tarea. |
| Se libera a mano | Donde diga quien lo libera: en la tarea o en un almacén. |
| Se entrega a una persona | Con esa persona. |
| Se devuelve o se recibe en un almacén | En ese almacén. |
| Se cambia su almacén base | Si estaba en su base, en la nueva. |

Cada uno de estos hechos queda apuntado con quién lo dijo y cuándo.

---

## Liberar un equipo de una tarea

Cuando un equipo ya no hace falta en una tarea —se reservó el día entero y se usó solo por la mañana—, un supervisor o superior puede liberarlo para que lo use otra tarea.

En el detalle de la tarea, o en la tarjeta del equipo en la app, pulse **Liberar equipo**. La plataforma pregunta **¿Dónde queda?**:

- **Queda en la tarea**: el equipo sigue en el sitio de la tarea hasta que alguien lo recoja.
- **Vuelve al almacén**: elija a qué almacén. Su almacén base sale el primero.

Entregar un equipo a una persona no es liberarlo: se hace con **Entregar**, como se explica en [Equipos: documentos, revisiones y entregas](./104-equipos-documentos-revisiones-y-entregas.md).

En la app, el trabajador no libera equipos: ve **Se libera al completar la tarea**.

---

## Lo que hay que ir a recoger

Un equipo libre que no está en su almacén base aparece marcado **Fuera de base**:

- En **Existencias**, el filtro de estado **Fuera de base** deja solo los equipos libres que están fuera. Cada fila dice cuántos ejemplares hay que recoger.
- En el calendario del artículo, la fila del ejemplar dice **Libre · fuera de base** y dónde está.

Es la lista de lo que el almacén tiene que ir a buscar. Estar fuera de base no impide reservarlo para otra tarea.

---

## Recibir un equipo en el almacén

Cuando el equipo vuelve, quien lo recibe lo apunta desde la ficha del artículo, en la fila del ejemplar:

1. Pulse **Recibir en almacén**.
2. Elija el **almacén que recibe**.
3. Indique el **estado**: **Bien**, **Dañado** o **Perdido**, y una nota si quiere.
4. Pulse **Recibir**.

Si llega dañado o se ha perdido, queda **no disponible** con ese motivo, y no se ofrece para nuevas tareas hasta que alguien lo vuelva a poner disponible desde su ficha. Si el equipo estaba entregado a una persona, recibirlo cierra también esa entrega.

No se puede recibir un equipo que su tarea tiene en uso: primero hay que liberarlo.

---

## Dónde ha estado

En la ficha del artículo, cada ejemplar dice **dónde está** ahora y desde cuándo. Con **Dónde ha estado** se ve su historia completa: cada vez que cambió de sitio, por qué y quién lo dijo.

---

## Quién puede hacer qué

| Rol | Puede |
|---|---|
| Worker | Ver dónde está el equipo de sus tareas |
| Supervisor, Manager, Owner | Además, liberar equipos de una tarea y recibirlos en un almacén |

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Material en las tareas](./102-material-en-las-tareas.md) | Cómo se reserva y se sigue el material de cada tarea |
| [Equipos: documentos, revisiones y entregas](./104-equipos-documentos-revisiones-y-entregas.md) | Entregar un equipo a una persona y devolverlo |
| [Existencias, almacenes y entradas](./101-existencias-almacenes-y-entradas.md) | El control de lo que hay |

# Prioridades y fechas límite

La combinación de prioridades y fechas límite permite al responsable comunicar al empleado qué tareas son más urgentes y cuánto tiempo tiene para completarlas. Gestionar correctamente ambos parámetros reduce los olvidos, ordena el trabajo del equipo y genera datos fiables sobre el cumplimiento operativo.

---

## Sistema de prioridades

CheckBiz360 clasifica las tareas en tres niveles de prioridad:

| Prioridad | Uso recomendado |
|---|---|
| **Alta** | La tarea debe completarse antes que cualquier otra. Afecta directamente a la operativa del negocio o tiene consecuencias si se retrasa. |
| **Media** | La tarea es importante pero admite cierta flexibilidad en el tiempo de ejecución. |
| **Baja** | La tarea es conveniente pero no crítica. Puede posponerse si surgen tareas de mayor urgencia. |

La prioridad se establece al crear la tarea y puede modificarse en cualquier momento desde el backoffice, siempre que la tarea no esté en estado "validada".

---

## Cómo afecta la prioridad a la visualización en la app

El empleado ve sus tareas activas ordenadas por prioridad de mayor a menor. Las tareas de prioridad alta aparecen en la parte superior de la lista, resaltadas visualmente para captar la atención de inmediato.

Cuando hay varias tareas con la misma prioridad, el sistema las ordena por fecha límite: primero las que vencen antes. Esta lógica ayuda al empleado a decidir por dónde empezar sin necesidad de consultar al responsable.

> **Consejo:** Reserve la prioridad alta para situaciones realmente urgentes. Si todas las tareas tienen prioridad alta, el sistema pierde efectividad como herramienta de organización y el empleado deja de diferenciar entre lo urgente y lo importante.

---

## Fechas límite: configuración

La fecha límite se establece durante la creación de la tarea y define el momento máximo en que debe quedar marcada como completada. Puede incluir fecha y hora exacta, o solo fecha (en cuyo caso el sistema toma las 23:59 como hora de corte).

### Consideraciones al fijar una fecha límite

- Tenga en cuenta el turno del empleado asignado. Si la tarea vence a las 10:00 y el empleado entra a las 11:00, la tarea vencerá antes de que pueda atenderla.
- Para tareas periódicas que se repiten en los mismos días, la fecha límite define el ciclo de cada instancia.
- Puede modificar la fecha límite de una tarea activa desde el backoffice. El empleado recibirá una notificación si la fecha se adelanta.

---

## Alertas automáticas de vencimiento próximo

CheckBiz360 genera alertas automáticas cuando una tarea se aproxima a su fecha límite sin haber sido completada. Estas alertas se envían tanto al empleado (notificación push en la app) como al responsable (notificación en el backoffice).

El tiempo de anticipación con el que se envía la alerta es configurable en los ajustes del módulo de tareas. El valor predeterminado es 24 horas antes del vencimiento.

---

## Qué ocurre cuando una tarea vence sin completar

Cuando la fecha límite llega y la tarea no está en estado "completada" o superior, el sistema la marca automáticamente como "vencida". Este cambio es inmediato y no requiere ninguna acción manual.

Las consecuencias del estado "vencida" son:

- La tarea aparece resaltada como vencida en la lista del empleado en la app.
- El responsable recibe una notificación informándole del vencimiento.
- La tarea queda registrada como vencida en los informes de cumplimiento.
- El empleado puede seguir completando la tarea aunque haya vencido, salvo que el responsable la archive.

> **Importante:** Una tarea vencida no desaparece ni se cierra automáticamente. El empleado puede marcarla como completada después del vencimiento, pero el registro de que superó el plazo queda en el historial y se refleja en los informes de desempeño.

---

## Extensión de plazo

Si las circunstancias justifican dar más tiempo al empleado, el responsable puede modificar la fecha límite de una tarea desde el backoffice en cualquier momento. Esta acción queda registrada en el historial de la tarea con la fecha del cambio y el usuario que lo realizó.

### Pasos para ampliar el plazo de una tarea

1. Acceda al backoffice y abra el detalle de la tarea.
2. Pulse sobre el campo **Fecha límite** y seleccione la nueva fecha.
3. Añada un comentario interno explicando el motivo de la extensión si lo considera oportuno.
4. Pulse **Guardar**. El empleado recibirá una notificación con la nueva fecha.

La extensión de plazo no modifica el estado de la tarea. Si ya estaba marcada como "vencida", permanecerá en ese estado hasta que el empleado la complete y el responsable la valide.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una tarea](./40-crear-una-tarea.md) | Campos disponibles al crear una tarea |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida y transiciones de estado |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Seguimiento del progreso en tiempo real |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Alertas automáticas de vencimiento |
| [Informes de tareas](./48-informes-de-tareas.md) | Tareas vencidas vs. completadas a tiempo |

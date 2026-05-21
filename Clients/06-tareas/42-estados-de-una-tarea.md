# Estados de una tarea

Cada tarea en CheckBiz360 atraviesa un ciclo de vida definido, desde el momento en que se crea hasta que queda archivada. Comprender los distintos estados y las transiciones entre ellos es fundamental para hacer un seguimiento correcto del trabajo asignado.

---

## El ciclo de vida de una tarea

El recorrido habitual de una tarea sigue esta secuencia:

**Pendiente → En curso → Completada → Validada**

Sin embargo, existen estados alternativos que puede alcanzar dependiendo de lo que ocurra durante su ejecución:

**Completada → Rechazada → Pendiente**

Adicionalmente, el sistema registra un **indicador de cumplimiento temporal** (`timeComplianceStatus`) que refleja si la tarea fue completada dentro del plazo establecido, independientemente de su estado. Este indicador no constituye un estado de tarea en sí mismo, sino un dato de seguimiento.

A continuación se describe cada estado en detalle.

---

## Tabla de estados

| Estado | Descripción | Quién puede activarlo |
|---|---|---|
| **Pendiente** | La tarea ha sido creada y asignada, pero el empleado aún no ha comenzado a trabajar en ella. | Sistema (al crear la tarea) |
| **En curso** | El empleado ha iniciado la tarea y está trabajando en ella. | Empleado desde la app |
| **Completada** | El empleado ha marcado la tarea como terminada y está pendiente de revisión por el responsable. | Empleado desde la app |
| **Validada** | El responsable ha revisado la tarea completada y la ha aceptado como correctamente ejecutada. | Manager o supervisor con permiso |
| **Rechazada** | El responsable revisó la tarea marcada como completada y la devolvió al empleado por no cumplir los requisitos. | Manager o supervisor con permiso |

---

## Qué desencadena cada cambio de estado

### De pendiente a en curso

El empleado abre la tarea en la app y pulsa el botón de inicio. Este cambio indica que ha tomado conciencia de la actividad y ha comenzado a trabajar en ella. El backoffice refleja este cambio en tiempo real.

### De en curso a completada

El empleado pulsa el botón de finalización en la app. Antes de confirmar, el sistema puede pedirle un comentario de cierre o la carga de una evidencia adjunta, dependiendo de la configuración de la tarea.

### De completada a validada

El manager o supervisor con permiso de validación revisa la tarea desde el backoffice y la acepta. En ese momento la tarea queda cerrada y se pueden activar las acciones de valoración del empleado.

### De completada a rechazada

El responsable revisa la tarea y considera que no cumple los requisitos. La rechaza indicando el motivo, y la tarea vuelve automáticamente al estado "pendiente" con el comentario del rechazo visible para el empleado.

### Indicador de cumplimiento temporal

Cuando una tarea supera su fecha límite sin haber sido completada, el sistema actualiza el indicador `timeComplianceStatus` para reflejar el incumplimiento. Este indicador es visible en el detalle de la tarea desde el backoffice y permite al responsable identificar retrasos sin que la tarea cambie a un estado diferente.

---

### Estado "vencida" automático

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La transición automática al estado explícito "vencida" y el marcado periódico programado de tareas como vencidas están planificados para una versión futura. En V1, el seguimiento del cumplimiento de plazos se realiza a través del indicador `timeComplianceStatus`.

---

## Diferencia entre completada y validada

Esta distinción es importante porque implica niveles de responsabilidad diferentes.

**Completada** significa que el empleado ha declarado que ha terminado la tarea. Es una acción unilateral: el empleado la cierra desde su lado, pero el responsable aún no ha verificado el resultado.

**Validada** significa que el responsable ha comprobado el trabajo y lo ha aceptado como correcto. Es el estado final definitivo de una tarea bien ejecutada.

En organizaciones donde la calidad de ejecución es crítica, como en restauración, logística o instalaciones técnicas, la distinción entre ambos estados garantiza que ninguna tarea quede cerrada sin supervisión.

> **Importante:** Las valoraciones de desempeño del empleado solo pueden registrarse sobre tareas en estado "validada". Una tarea "completada" pero no validada no genera puntuación en el índice de eficiencia del empleado.

---

## Visualización de estados en el backoffice

Desde el panel de tareas del backoffice, es posible filtrar las tareas por estado. Esto permite al responsable:

- Ver de un vistazo cuántas tareas están pendientes de validación.
- Identificar tareas con incumplimiento de plazo a través del indicador de cumplimiento temporal.
- Comprobar el avance general de las tareas activas en una sucursal o para un empleado concreto.

Los estados se muestran con etiquetas de color para facilitar la lectura rápida: gris (pendiente), azul (en curso), verde (completada), verde oscuro (validada) y rojo (rechazada).

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una tarea](./40-crear-una-tarea.md) | Campos y opciones al crear una tarea |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Cómo el empleado actualiza el progreso |
| [Prioridades y fechas límite](./44-prioridades-y-fechas-limite.md) | Configuración de plazos y alertas |
| [Validación de tareas](./45-validacion-de-tareas.md) | Flujo de validación y permisos |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Avisos automáticos por cambio de estado |

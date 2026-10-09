# Estados de una tarea

Cada tarea en CheckBiz360 atraviesa un ciclo de vida definido, desde que se crea hasta que queda cerrada. Comprender los estados y las transiciones entre ellos es fundamental para hacer un seguimiento correcto del trabajo asignado.

Una tarea lleva **dos indicadores independientes**: su **estado**, que refleja en qué punto del trabajo está, y su **cumplimiento temporal**, que refleja cómo va respecto a la fecha límite. Conviene no confundirlos: una tarea puede estar *en progreso* y a la vez *vencida*.

---

## El ciclo de vida de una tarea

El recorrido habitual es:

**Borrador → Asignada → En progreso → Completada → Validada**

Con dos desvíos posibles: el responsable puede **rechazar** una tarea completada, o **cancelar** la tarea en cualquier momento antes de su cierre.

Mientras está *en progreso*, la tarea puede quedar **en pausa** una o varias veces. La pausa no es un estado más: se explica en [Tarea en pausa](#tarea-en-pausa).

---

## Tabla de estados

| Estado | Descripción | Quién puede activarlo |
|---|---|---|
| **Borrador** | La tarea está creada pero aún no se ha puesto en circulación. Sirve para prepararla antes de enviarla al equipo. | Quien la crea, desde el backoffice |
| **Asignada** | La tarea está enviada a sus responsables, que han recibido la notificación, pero nadie ha empezado todavía. | Quien la crea, o el sistema al asignar |
| **En progreso** | Un empleado asignado ha iniciado la tarea y está trabajando en ella. | Empleado desde la app |
| **Completada** | El empleado ha marcado la tarea como terminada y queda pendiente de revisión. | Empleado desde la app |
| **Validada** | El responsable ha revisado el trabajo y lo ha aceptado como correcto. Es el cierre satisfactorio. | Manager, u owner o supervisor con permiso de validación |
| **Rechazada** | El responsable ha revisado la tarea completada y la ha devuelto con un motivo obligatorio. | Manager, u owner o supervisor con permiso de validación |
| **Cancelada** | La tarea se anula porque ya no procede. Requiere motivo y no computa como incumplimiento. | Manager u owner desde el backoffice |

Los estados *Validada*, *Rechazada* y *Cancelada* no pueden asignarse a mano al crear o editar una tarea: son resultado de una acción del ciclo de vida (validar, rechazar, cancelar). De ellos solo se sale **reabriendo** la tarea, como se explica más abajo.

---

## Indicador de cumplimiento temporal

En paralelo al estado, cada tarea mantiene un indicador de cumplimiento frente a su fecha límite:

| Indicador | Qué significa |
|---|---|
| **Sin iniciar** | Todavía no se ha empezado a trabajar en ella |
| **A tiempo** | En marcha, dentro de plazo |
| **En riesgo** | En marcha, pero acercándose a la fecha límite |
| **Vencida** | Ha superado la fecha límite sin completarse |
| **Completada a tiempo** | Se cerró dentro del plazo |
| **Completada tarde** | Se cerró después de la fecha límite |

Cuando la tarea está rechazada, el indicador muestra *Rechazada*, porque el cumplimiento del plazo deja de ser la información relevante.

---

## Qué desencadena cada cambio de estado

### De borrador a asignada

Quien crea la tarea la guarda con estado *Asignada*, o edita una tarea en borrador para ponerla en circulación. En ese momento los empleados asignados reciben la notificación push.

### De asignada a en progreso

El empleado abre la tarea en la app y pulsa iniciar. Necesita tener la jornada abierta y, si la tarea tiene lugar de trabajo propio, estar dentro de su margen. El backoffice refleja el cambio y, si la tarea tenía activado el aviso de inicio tardío, ese aviso deja de estar pendiente.

### De en progreso a completada

El empleado pulsa finalizar en la app. Si la tarea tiene activada la exigencia de evidencia, el sistema no permite cerrarla sin al menos una foto o vídeo adjuntos, y devuelve el error `task/evidence_required`. Si la tarea estaba en pausa, la pausa se cierra en ese momento.

### De completada a validada

El responsable revisa el trabajo desde el backoffice y lo acepta. La tarea queda cerrada y se habilita la valoración del empleado.

### De completada a rechazada

El responsable revisa el trabajo y lo devuelve indicando un **motivo obligatorio**, visible para el empleado en el detalle de la tarea. Si el trabajo debe rehacerse, el responsable puede editar la tarea y devolverla al estado *Asignada*.

### Cancelación

Una tarea que ya no procede se cancela indicando un motivo. Es un cierre administrativo: no se contabiliza como incumplimiento del empleado. El motivo queda guardado en la tarea y aparece en su historial; si había una pausa abierta, se cierra.

> **Nota:** las cancelaciones hechas desde el backoffice antes del 11 de septiembre de 2026 no conservaron su motivo, aunque el diálogo lo pidiera. Las posteriores sí lo conservan.

### Reabrir una tarea

Una tarea validada, rechazada o cancelada se reabre desde **Editar**, cambiando su estado a **Asignada** o a **Borrador**. Pueden hacerlo owners y managers. Para volver a *Asignada* la tarea tiene que tener al menos un empleado asignado.

Al reabrir:

- Se retiran la validación, el rechazo o la cancelación anteriores, con sus motivos, de modo que la tarea no arrastra la firma de la ejecución pasada.
- El cumplimiento temporal vuelve a *Sin iniciar*. Revise la fecha límite si ya ha pasado.
- Los contadores de pausa vuelven a cero.
- El historial conserva todo lo ocurrido antes de reabrir.

---

## Tarea en pausa

Una tarea *en progreso* se puede **pausar** y **reanudar** tantas veces como haga falta, desde la app o desde el detalle de la tarea en el backoffice. Los pasos y las condiciones se explican en [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md#pausar-y-reanudar-una-tarea).

La pausa **no es un estado**: la tarea sigue *en progreso* a todos los efectos —filtros, informes, cumplimiento temporal— y la etiqueta de estado muestra **En pausa** mientras dura. La fecha límite no se amplía por estar en pausa.

---

### Estado "vencida" automático

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

El paso automático a un estado explícito de tarea "vencida" está planificado para una versión futura. Hoy el vencimiento se refleja en el indicador de cumplimiento temporal, no en el estado de la tarea.

---

## Diferencia entre completada y validada

Esta distinción implica niveles de responsabilidad diferentes.

**Completada** significa que el empleado ha declarado que ha terminado. Es una acción unilateral: cierra desde su lado, pero el responsable aún no ha verificado el resultado.

**Validada** significa que el responsable ha comprobado el trabajo y lo ha aceptado. Es el cierre definitivo de una tarea bien ejecutada.

En organizaciones donde la calidad de ejecución es crítica —restauración, logística, instalaciones técnicas— esta distinción garantiza que ninguna tarea quede cerrada sin supervisión.

> **Importante:** la valoración del empleado se registra sobre el trabajo ya revisado. Una tarea completada pero no validada no cierra el circuito de calidad.

---

## Visualización de estados en el backoffice

Desde el listado de tareas se puede filtrar por estado y por prioridad. Esto permite al responsable:

- Ver de un vistazo cuántas tareas están pendientes de validación.
- Identificar tareas vencidas o en riesgo a través del indicador de cumplimiento temporal.
- Comprobar el avance de las tareas activas en una sucursal o para un empleado concreto.

Cada tarea muestra dos etiquetas de color: una para el estado y otra para el cumplimiento temporal. El código de color es coherente en toda la plataforma: gris para lo que aún no ha arrancado o está detenido (borrador, cancelada, sin iniciar, en pausa), azul para lo que está en curso o a la espera de revisión (asignada, completada), ámbar para lo que requiere atención (en progreso, en riesgo, completada tarde), verde para lo correcto (validada, a tiempo, completada a tiempo) y rojo para lo que ha fallado (rechazada, vencida).

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una tarea](./40-crear-una-tarea.md) | Campos y opciones al crear una tarea |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Cómo se actualiza el progreso, las pausas y el historial |
| [Prioridades y fechas límite](./44-prioridades-y-fechas-limite.md) | Configuración de plazos y alertas |
| [Validación de tareas](./45-validacion-de-tareas.md) | Flujo de validación y permisos |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Avisos automáticos por cambio de estado |

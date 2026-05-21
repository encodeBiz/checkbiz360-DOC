# Validación de tareas

La validación es el paso por el que un responsable confirma que el trabajo realizado por el empleado cumple los requisitos exigidos. CheckBiz360 separa la acción de completar una tarea (que realiza el empleado) de la acción de validarla (que realiza el manager o supervisor autorizado), garantizando así un doble nivel de control sobre la calidad del trabajo.

---

## Flujo de validación

El proceso de validación sigue siempre el mismo orden:

1. El empleado ejecuta la tarea y la marca como **completada** desde la app.
2. El sistema notifica al responsable que hay una tarea pendiente de revisión.
3. El responsable accede al backoffice, revisa el trabajo y decide si lo **acepta** o lo **rechaza**.
4. Si acepta, la tarea pasa a estado **validada** y queda cerrada definitivamente.
5. Si rechaza, la tarea vuelve a estado **pendiente** con el motivo del rechazo visible para el empleado.

Este flujo aplica únicamente a las tareas configuradas con validación obligatoria. Si el manager opta por no requerir validación, la tarea queda cerrada en el momento en que el empleado la marca como completada.

---

## Aceptar una tarea completada

Para validar una tarea, el responsable debe:

1. Acceder al backoffice y abrir la sección **Tareas**.
2. Filtrar las tareas por estado **Completada** para ver las pendientes de revisión.
3. Abrir el detalle de la tarea que desea revisar.
4. Leer los comentarios del empleado y revisar los adjuntos o evidencias que haya aportado.
5. Pulsar **Validar tarea**.
6. Opcionalmente, añadir un comentario de cierre antes de confirmar.

Una vez validada, la tarea queda en estado definitivo. No puede modificarse su estado de forma retroactiva. Si la valoración del empleado está habilitada, el campo de puntuación se activa a continuación.

---

## Rechazar una tarea completada

Si el responsable considera que la tarea no se ha completado correctamente, puede rechazarla. El rechazo devuelve la tarea al empleado para que la ejecute de nuevo.

### Pasos para rechazar una tarea

1. Desde el detalle de la tarea en el backoffice, pulse **Rechazar tarea**.
2. Escriba el motivo del rechazo en el campo de texto obligatorio. Este comentario lo verá el empleado en la app.
3. Confirme el rechazo.

La tarea cambia de estado "completada" a "pendiente". El empleado recibe una notificación push indicando que la tarea ha sido devuelta, y al abrirla verá el motivo del rechazo junto al historial completo.

> **Importante:** El motivo del rechazo es obligatorio. Proporcionar una explicación clara al empleado es esencial para que pueda corregir el trabajo y evitar el mismo error en el futuro.

---

## Consecuencias del rechazo

Cuando una tarea es rechazada:

- Vuelve a estado **pendiente** y reaparece en la lista activa del empleado en la app.
- La fecha límite original sigue vigente. Si ya ha vencido, la tarea permanecerá marcada como vencida aunque esté de nuevo pendiente.
- El historial de la tarea registra el rechazo, el motivo y la fecha, de modo que queda evidencia del ciclo completo.
- El empleado puede volver a marcarla como completada una vez que haya corregido el trabajo, reiniciando el ciclo de validación.

---

## Delegación del permiso de validación a supervisores

Por defecto, solo los managers y owners pueden validar tareas. Sin embargo, el manager puede delegar este permiso en los supervisores de su equipo para descentralizar la gestión operativa.

### Cómo habilitar la validación para un supervisor

1. Acceda al backoffice y abra el perfil del supervisor en la sección **Empleados**.
2. En el apartado de permisos del módulo de tareas, active la opción **Validar tareas**.
3. Guarde los cambios. El supervisor podrá validar y rechazar tareas desde ese momento.

> **Nota:** La delegación de validación se aplica por supervisor individual. Puede habilitar el permiso para unos supervisores y no para otros, en función de la estructura de su organización.

El manager mantiene siempre visibilidad completa sobre las validaciones realizadas por sus supervisores. Todas las acciones quedan registradas en el historial con el nombre del responsable que las ejecutó.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida y significado de cada estado |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Cómo el empleado actualiza el progreso |
| [Valoración del trabajador](./46-valoracion-del-trabajador.md) | Puntuación de desempeño tras la validación |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Avisos al validar o rechazar una tarea |
| [Roles y niveles de responsabilidad](../02-empleados/07-roles-y-niveles-de-responsabilidad.md) | Descripción de permisos por rol |

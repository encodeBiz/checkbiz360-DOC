# Asignar tareas a empleados

La asignación es el mecanismo por el que una tarea pasa de existir en el sistema a estar activa en el dispositivo de un empleado. CheckBiz360 ofrece flexibilidad para asignar tareas de forma individual o a grupos de empleados, y permite reasignarlas en cualquier momento si las circunstancias cambian.

---

## Asignación individual

La asignación individual vincula una tarea a un único empleado. Es el método más habitual para actividades concretas donde la responsabilidad recae en una persona específica.

Al seleccionar al empleado durante la creación o edición de la tarea, el sistema lo registra como responsable. Desde ese momento, la tarea aparece en su lista de tareas pendientes dentro de la app y recibe una notificación push.

Este método es adecuado para tareas de mantenimiento, formación específica, gestión de una incidencia o cualquier actividad que deba completar una persona concreta.

---

## Asignación por equipo o sucursal

Cuando la tarea es de carácter colectivo o se quiere distribuir trabajo entre varios miembros, es posible seleccionar más de un empleado durante la asignación. Todos los destinatarios recibirán la tarea en su app simultáneamente.

> **Importante:** en la asignación múltiple hay **una sola tarea** compartida por todos los asignados, no una copia para cada uno. Por defecto, **cualquiera de ellos puede completarla**, y al hacerlo la tarea queda cerrada para el grupo. Lo que sí se registra por separado es la participación de cada empleado: su asignación, cuándo empezó y qué aportó.

Si necesita que cada persona ejecute el trabajo de forma independiente, cree una tarea por empleado.

Una tarea pertenece siempre a una sucursal, así que la selección de empleados se hace sobre los que trabajan en ese centro.

> **Nota:** los [equipos](../02-empleados/99-equipos.md) de la sección Empleados se aplican a sucursales, no a tareas. Después de aplicar un equipo a la sucursal, sus miembros se seleccionan en la tarea uno a uno, como el resto de la plantilla. Añadir un equipo entero a una tarea de una vez está pendiente de desarrollo.

---

## Reasignación de tareas

Las circunstancias cambian: un empleado puede ausentarse, cambiar de turno o resultar no ser la persona adecuada para una tarea concreta. CheckBiz360 permite reasignar una tarea a otro empleado en cualquier momento, siempre que no esté en estado "completada" o "validada".

### Pasos para reasignar una tarea

1. Acceda al backoffice y abra el listado de **Tareas**.
2. Localice la tarea que desea reasignar y pulse sobre ella para abrir el detalle.
3. Pulse **Editar**. En el campo de empleados asignados, quite al empleado actual y seleccione al nuevo destinatario.
4. Pulse **Guardar**. Al guardar, se asigna a quien ha añadido y se retira a quien ha quitado. El nuevo empleado recibe una notificación push.
5. Si lo considera oportuno, añada una nota explicando el motivo del cambio.

También puede retirar a una persona directamente desde el bloque **Equipo asignado** del detalle de la tarea.

> **Importante:** Al reasignar, el empleado original deja de ver la tarea en su app. Si ya había iniciado la tarea o dejado comentarios, esas anotaciones se conservan y son visibles desde el backoffice.

> **Nota:** la sucursal de una tarea no se puede cambiar al editarla, así que los empleados que se añadan tienen que trabajar en esa misma sucursal.

---

## Qué ve el empleado en la app

Cuando se le asigna una tarea, el empleado recibe una notificación push en su dispositivo. Al abrir la app, encontrará la tarea en su lista de tareas activas, ordenadas por prioridad y fecha límite.

Dentro del detalle de la tarea, el empleado puede consultar:

- El título y la descripción completa de la actividad, con su formato: listas, listas de comprobación, títulos y enlaces.
- La prioridad asignada (crítica, alta, media o baja).
- La fecha y hora límite, y la fecha prevista de inicio si se indicó.
- El lugar de trabajo, si la tarea tiene uno propio, con el enlace **Ver en Maps**.
- Las evidencias ya subidas y las notas de la tarea.
- El tiempo invertido y el total de pausas, y el historial de la tarea (desde la versión 1.4.0 de la app).

El empleado puede iniciar la tarea, pausarla y reanudarla, añadir notas de progreso, subir evidencias y, cuando finalice, marcarla como completada.

---

## Notificación push automática al asignar

En el momento en que se guarda la asignación, CheckBiz360 envía automáticamente una notificación push al dispositivo del empleado. No es necesaria ninguna acción adicional por parte del responsable.

La notificación incluye el título de la tarea y la fecha límite, de modo que el empleado tenga la información esencial sin necesidad de abrir la app.

Si el empleado tiene las notificaciones push desactivadas en su dispositivo, la tarea seguirá apareciendo en su lista dentro de la app, pero no recibirá el aviso en pantalla.

---

## Quién ha trabajado en la tarea

El bloque **Equipo asignado** del detalle de la tarea muestra a las personas asignadas. La sección **Historial** cuenta el recorrido completo —quién la creó, quién la inició, quién la pausó o la completó— con fecha y rol de cada actuación; se describe en [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md#historial-de-la-tarea).

Nada de esto se puede modificar ni eliminar desde el backoffice.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una tarea](./40-crear-una-tarea.md) | Campos y pasos para crear una tarea desde cero |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida y cambios de estado |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Cómo el empleado actualiza el progreso |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Tipos de notificación y configuración |
| [Roles y niveles de responsabilidad](../02-empleados/07-roles-y-niveles-de-responsabilidad.md) | Descripción de cada rol en la plataforma |

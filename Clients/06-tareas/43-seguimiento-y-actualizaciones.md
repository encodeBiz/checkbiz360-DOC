# Seguimiento y actualizaciones de tareas

Una vez que una tarea ha sido asignada, tanto el empleado como el responsable tienen herramientas para comunicarse sobre su evolución y mantener el estado actualizado en todo momento. Este artículo explica cómo se gestiona el seguimiento desde ambas partes: la app del empleado y el backoffice del responsable.

---

## Cómo actualiza el empleado el estado de una tarea

El empleado gestiona sus tareas desde la sección de tareas de la app móvil. Allí encuentra una lista de todas las tareas que tiene asignadas, ordenadas por prioridad y fecha límite.

### Iniciar una tarea

Cuando el empleado está listo para comenzar, abre el detalle de la tarea y pulsa **Iniciar tarea**. El estado cambia de "pendiente" a "en curso" y el responsable lo ve reflejado en el backoffice en tiempo real.

### Marcar una tarea como completada

Una vez finalizada la actividad, el empleado pulsa **Marcar como completada**. El sistema puede solicitar un comentario de cierre o una evidencia adjunta antes de confirmar, si el responsable ha configurado ese requisito al crear la tarea.

> **Consejo:** Animar a los empleados a añadir un comentario breve al completar la tarea —aunque no sea obligatorio— mejora la calidad del registro y facilita la validación por parte del responsable.

---

## Comentarios y notas de progreso

Durante el tiempo que una tarea esté activa, el empleado puede añadir comentarios en cualquier momento desde el detalle de la tarea en la app. Estos comentarios son visibles para el responsable en el backoffice.

Los comentarios son útiles para:

- Informar de que se ha completado una parte de la tarea y se continúa con otra.
- Comunicar una incidencia o dificultad encontrada durante la ejecución.
- Adjuntar una foto o documento como evidencia parcial de progreso.
- Solicitar aclaraciones o confirmación antes de continuar.

El responsable también puede añadir comentarios desde el backoffice, que el empleado verá en la app. Esto permite una comunicación directa sobre la tarea sin necesidad de llamadas ni mensajes externos.

---

## Historial de cambios de estado

Cada tarea mantiene un registro cronológico e inmutable de todos los cambios de estado que ha experimentado. El historial es accesible desde el detalle de la tarea en el backoffice e incluye:

- Fecha y hora exacta de cada cambio de estado.
- Estado anterior y estado nuevo.
- Nombre del usuario o del sistema que realizó el cambio.
- Comentario asociado al cambio, si lo hubo.

Este historial no puede editarse ni eliminarse. Garantiza la trazabilidad completa de la tarea y sirve como base para resolver discrepancias o auditar el desempeño del equipo.

---

## Seguimiento en tiempo real desde el backoffice

El responsable no necesita esperar a que el empleado informe: los cambios de estado se sincronizan de forma inmediata entre la app y el backoffice.

Desde el panel de tareas del backoffice, el manager o supervisor puede:

- Ver el estado actual de todas las tareas activas, filtradas por empleado, sucursal, tipo o fecha.
- Acceder al detalle de cada tarea para leer los comentarios del empleado.
- Consultar el porcentaje de tareas completadas en un periodo determinado.
- Identificar tareas que llevan demasiado tiempo en estado "en curso" sin avance.

> **Nota:** Si una tarea permanece en estado "en curso" durante más tiempo del esperado sin nuevas actualizaciones, el sistema puede generar una alerta al responsable según la configuración de recordatorios establecida.

---

## Notificaciones de actualización

Cuando el estado de una tarea cambia, el sistema notifica a las partes implicadas de forma automática. El responsable recibe una notificación en el backoffice cuando el empleado marca una tarea como completada o añade un comentario relevante. El empleado recibe una notificación push cuando el responsable valida, rechaza o comenta una tarea.

Esto elimina la necesidad de hacer seguimiento manual: el sistema informa a cada persona en el momento en que debe actuar.

Para una descripción detallada de todos los tipos de notificación, consulte el artículo [Notificaciones de tareas](./47-notificaciones-de-tareas.md).

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida y transiciones de estado |
| [Validación de tareas](./45-validacion-de-tareas.md) | Flujo de validación por el responsable |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Tipos de aviso y canales de notificación |
| [Informes de tareas](./48-informes-de-tareas.md) | Métricas de seguimiento y exportación |
| [Asignar tareas a empleados](./41-asignar-tareas-a-empleados.md) | Cómo asignar y reasignar tareas |

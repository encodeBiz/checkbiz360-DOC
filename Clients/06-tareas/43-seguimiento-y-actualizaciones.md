# Seguimiento y actualizaciones de tareas

Una vez que una tarea ha sido asignada, tanto el empleado como el responsable tienen herramientas para comunicarse sobre su evolución y mantener el estado actualizado en todo momento. Este artículo explica cómo se gestiona el seguimiento desde ambas partes: la app del empleado y el backoffice del responsable.

---

## Cómo actualiza el empleado el estado de una tarea

El empleado gestiona sus tareas desde la sección de tareas de la app móvil. Allí encuentra una lista de todas las tareas que tiene asignadas, ordenadas por prioridad y fecha límite.

### Iniciar una tarea

Cuando el empleado está listo para comenzar, pulsa **Iniciar**. El estado cambia de *asignada* a *en progreso* y el responsable lo ve reflejado en el backoffice.

**Desde la versión 1.6.0 de la app** el botón está en tres sitios, y hace lo mismo en los tres: en la propia tarjeta de la lista de tareas, en la tarjeta **Tareas de hoy** de la pantalla de asistencia, y dentro del detalle como hasta ahora. Ya no hace falta abrir la tarea para empezarla.

Los botones solo aparecen en las tareas que el empleado tiene asignadas. Un supervisor que ve tareas de su equipo sigue actuando sobre ellas desde el detalle.

Para iniciar hace falta tener la **jornada abierta** (haber fichado la entrada) y, si la tarea tiene lugar de trabajo propio, estar dentro de su margen. Ver [Relación con el control horario](./39-que-es-el-modulo-de-tareas.md#relación-con-el-control-horario) y [Lugar de trabajo propio](./40-crear-una-tarea.md#lugar-de-trabajo-propio).

### Marcar una tarea como completada

Una vez finalizada la actividad, el empleado pulsa **Completar**. Si la tarea tiene activada la exigencia de evidencia —lo está por defecto—, el sistema no permite cerrarla sin al menos una foto o vídeo adjuntos, y devuelve el error `task/evidence_required`.

**Desde la versión 1.6.0**, completar pide confirmación antes de cerrar la tarea. Es la única de las cuatro acciones que el empleado no puede deshacer por su cuenta: para volver atrás hace falta que un responsable la rechace. Iniciar, pausar y reanudar no preguntan, porque se deshacen con otro toque.

Si la tarea exige evidencia y se pulsa **Completar** desde la lista, la app abre el detalle en vez de intentar cerrarla: es donde se suben las fotos.

---

## Pausar y reanudar una tarea

Cuando el trabajo se interrumpe —para comer, para ir a por material, o porque sigue al día siguiente—, la tarea se **pausa** y después se **reanuda**, tantas veces como haga falta. El tiempo en pausa se suma aparte y sale en el [informe de tareas](./48-informes-de-tareas.md).

### Desde la app

En el detalle de una tarea en progreso, el empleado pulsa **Pausar**; para seguir, pulsa **Reanudar**. Está disponible **desde la versión 1.4.0 de la app**.

**Desde la 1.6.0** están también fuera del detalle: en la tarjeta de la lista de tareas, junto a **Completar**, y en **Tareas de hoy** como botón de icono al lado del principal.

- En la app, el botón de pausar aparece cuando el empleado tiene la jornada fichada.
- **Reanudar** pide lo mismo que iniciar: jornada abierta y, si la tarea tiene lugar de trabajo propio, estar dentro de su margen.
- El detalle muestra el **tiempo invertido** —de inicio a fin, o hasta ahora, descontando las pausas— y el total de pausas.

### Desde el backoffice

En el detalle de una tarea en progreso aparecen los botones **Pausar** y **Reanudar**. En el resumen de la tarea, la cifra **Pausas** indica desde cuándo está pausada o, si ya no lo está, cuánto han sumado las pausas.

Pueden pausar y reanudar los empleados asignados y, desde el backoffice, supervisores, managers y owners.

> **Importante:** una tarea con lugar de trabajo propio no se puede reanudar ni completar desde el backoffice, porque el panel no envía ubicación. Debe hacerlo un empleado desde la app. Pausarla desde el backoffice sí es posible.

### Reglas de la pausa

- **La pausa es de la tarea**, no de cada persona. Solo hay una pausa abierta a la vez: si hay varios asignados, cualquiera de ellos la pausa o la reanuda, y queda anotado quién lo hizo.
- **Completar, cancelar o rechazar** una tarea en pausa está permitido: la pausa se cierra en ese momento. No hace falta reanudar solo para poder cerrarla.
- **Reabrir** la tarea pone a cero los contadores de pausa; el historial conserva las pausas anteriores.
- La pausa **no amplía la fecha límite**: el cumplimiento temporal se sigue calculando igual.
- Pausar y reanudar **no envían notificaciones**.

> **Consejo:** Animar a los empleados a añadir un comentario breve al completar la tarea —aunque no sea obligatorio— mejora la calidad del registro y facilita la validación por parte del responsable.

---

## Notas de progreso

Durante el tiempo que una tarea esté activa, el empleado puede añadir notas en cualquier momento desde el detalle de la tarea en la app. Son visibles para el responsable en el backoffice, y viceversa.

Cada nota se clasifica con un tipo, que permite distinguir de un vistazo la naturaleza de la comunicación:

| Tipo de nota | Para qué se usa |
|---|---|
| **Especificación** | Precisar cómo debe hacerse el trabajo |
| **Nota operativa** | Informar del avance o del día a día de la ejecución |
| **Aclaración** | Resolver una duda planteada sobre la tarea |
| **Nota de incidencia** | Dejar constancia de un problema encontrado durante la ejecución |

Las notas son útiles para:

- Informar de que se ha completado una parte de la tarea y se continúa con otra.
- Comunicar una incidencia o dificultad encontrada durante la ejecución.
- Adjuntar una foto o documento como evidencia parcial de progreso.
- Solicitar aclaraciones o confirmación antes de continuar.

El responsable también puede añadir comentarios desde el backoffice, que el empleado verá en la app. Esto permite una comunicación directa sobre la tarea sin necesidad de llamadas ni mensajes externos.

---

## Historial de la tarea

La sección **Historial** del detalle de la tarea cuenta su recorrido completo, en orden: creada, asignada, iniciada, pausada y reanudada, completada, validada o rechazada, cancelada, y los cambios de estado hechos a mano. Cada línea indica:

- Fecha y hora.
- Quién lo hizo y con qué rol. Las acciones automáticas aparecen como **Sistema**; si una persona del backoffice no tiene nombre registrado, aparece como **Usuario del panel**.
- El motivo, en las validaciones, los rechazos y la última cancelación.

También quedan anotados los intentos de iniciar o reanudar una tarea **fuera de su lugar de trabajo** («Inicio rechazado: fuera del lugar de trabajo»), que ayudan a entender por qué un empleado no pudo empezar.

Las notas, evidencias y valoraciones tienen su propia sección en el detalle y no se repiten en el historial. Desde la versión 1.4.0, la app muestra también el historial de la tarea, pausas incluidas.

Este historial no puede editarse ni eliminarse. Garantiza la trazabilidad completa de la tarea y sirve como base para resolver discrepancias o auditar el desempeño del equipo.

---

## Seguimiento en tiempo real desde el backoffice

El responsable no necesita esperar a que el empleado informe: los cambios de estado se sincronizan de forma inmediata entre la app y el backoffice.

Desde el panel de tareas del backoffice, el manager o supervisor puede:

- Ver el estado actual de todas las tareas activas, filtradas por estado, prioridad, empleado o sucursal.
- Acceder al detalle de cada tarea para leer las notas del empleado y revisar sus evidencias.
- Identificar tareas que llevan demasiado tiempo *en progreso* sin avance.
- Detectar las que están *en riesgo* o *vencidas* por el indicador de cumplimiento temporal.

> **Nota:** el sistema avisa por su cuenta en dos situaciones: cuando una tarea con hora prevista de inicio no ha arrancado 15 minutos después, y cuando se acerca o se supera la fecha límite. Que una tarea lleve mucho tiempo *en progreso* sin novedades no dispara ningún aviso automático: eso se detecta revisando el listado.

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
| [Calendario semanal de tareas](./111-calendario-semanal-de-tareas.md) | La semana de un vistazo, día a día y hora a hora, con los huecos y los solapes |

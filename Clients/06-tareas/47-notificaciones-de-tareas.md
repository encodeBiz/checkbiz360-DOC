# Notificaciones de tareas

CheckBiz360 envía notificaciones automáticas a las personas implicadas cada vez que ocurre un evento relevante en el ciclo de vida de una tarea. El objetivo es que nadie tenga que revisar manualmente el estado de las tareas: el sistema informa a cada persona en el momento exacto en que debe actuar o estar al tanto.

Las notificaciones se basan en eventos concretos del ciclo de vida —asignación, validación, rechazo, actualización— y en dos avisos que dispara el propio sistema: el de **inicio tardío** y los de **vencimiento**. Ambos se describen más abajo.

---

## Canales de notificación

Las notificaciones de tareas se distribuyen por dos canales:

**Notificaciones push en la app móvil:** Se envían al dispositivo del empleado. Aparecen como alertas en la pantalla del teléfono aunque la app no esté abierta, siempre que el empleado haya concedido permiso de notificaciones a la aplicación.

**Notificaciones en el backoffice:** Se acumulan en el panel de notificaciones del backoffice y son visibles para el manager y el supervisor. Incluyen un contador de notificaciones no leídas en el icono de la campana del menú superior.

---

## Tipos de notificación

### Nueva tarea asignada

**Destinatario:** Empleado asignado a la tarea.

**Canal:** Push en la app.

**Cuándo se envía:** En el momento en que el responsable guarda la tarea con el empleado asignado.

**Contenido:** Título de la tarea, prioridad asignada y fecha límite. El empleado puede tocar la notificación para abrir directamente el detalle de la tarea en la app.

---

### Tarea validada

**Destinatario:** Empleado cuya tarea ha sido validada.

**Canal:** Push en la app.

**Cuándo se envía:** En el momento en que el manager o supervisor confirma la validación.

**Contenido:** Título de la tarea, nombre del responsable que la validó y puntuación obtenida si se ha registrado una valoración.

---

### Tarea rechazada

**Destinatario:** Empleado cuya tarea ha sido rechazada.

**Canal:** Push en la app.

**Cuándo se envía:** En el momento en que el manager o supervisor registra el rechazo.

**Contenido:** Título de la tarea, nombre del responsable que la rechazó y motivo del rechazo. El empleado puede tocar la notificación para ver el detalle completo y el comentario asociado.

---

### Tarea actualizada por el empleado

**Destinatario:** Manager o supervisor responsable de la tarea.

**Canal:** Notificación en backoffice; opcionalmente push si el responsable tiene la app instalada.

**Cuándo se envía:** Cuando el empleado cambia el estado de la tarea (inicia, completa) o añade un comentario.

**Contenido:** Nombre del empleado, título de la tarea y naturaleza del cambio realizado.

> **Nota:** pausar y reanudar una tarea no envía ninguna notificación. Es una acción rutinaria, y avisar de cada pausa haría que se ignoraran los avisos importantes. Las pausas se consultan en el historial de la tarea.

---

### Aviso de inicio tardío

**Destinatario:** las personas implicadas en la tarea.

**Cuándo se envía:** cuando han pasado **15 minutos** de la fecha prevista de inicio sin que la tarea se haya iniciado.

**Requisitos:** la tarea debe tener **fecha prevista de inicio** y la opción **Notificar si no inicia a tiempo** activada. Sin fecha prevista de inicio, la opción no tiene efecto.

Es el único aviso que se configura tarea a tarea, y se activa al crearla o editarla. El envío queda registrado en la actividad de la tarea, de modo que el responsable puede comprobar si llegó a producirse.

---

### Avisos de vencimiento

**Destinatario:** las personas implicadas en la tarea.

**Cuándo se envían:** cuando la tarea se acerca a su fecha límite y cuando la supera sin completarse.

Cada aviso se emite **una sola vez por tarea** y queda registrado, para que un mismo vencimiento no genere notificaciones repetidas día tras día.

---

## Configuración de la frecuencia de los avisos

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La antelación de los avisos de vencimiento no es configurable por el cliente en la versión actual. Poder ajustar esa anticipación, activar un segundo recordatorio y variar la frecuencia según la prioridad de la tarea está planificado para una versión futura.

---

## Requisitos para recibir notificaciones push

Para que el empleado reciba notificaciones push en su dispositivo, deben cumplirse las siguientes condiciones:

1. Tener la app de CheckBiz360 instalada y haber iniciado sesión al menos una vez.
2. Haber concedido permisos de notificaciones a la app cuando el sistema operativo lo solicitó.
3. Tener conexión a internet en el dispositivo en el momento del envío, o recibirla en cuanto se conecte.

Si el empleado ha desactivado los permisos de notificaciones del dispositivo, las alertas no llegarán a su pantalla. En ese caso, la tarea seguirá apareciendo en su lista dentro de la app, pero el empleado deberá abrirla manualmente para ver las novedades.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Asignar tareas a empleados](./41-asignar-tareas-a-empleados.md) | Notificación automática al asignar |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Eventos que generan notificaciones |
| [Prioridades y fechas límite](./44-prioridades-y-fechas-limite.md) | Alertas de vencimiento y configuración |
| [Validación de tareas](./45-validacion-de-tareas.md) | Notificación al validar o rechazar |
| [Qué es el módulo de tareas](./39-que-es-el-modulo-de-tareas.md) | Visión general del módulo |

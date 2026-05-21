# Notificaciones de tareas

CheckBiz360 envía notificaciones automáticas a las personas implicadas cada vez que ocurre un evento relevante en el ciclo de vida de una tarea. El objetivo es que nadie tenga que revisar manualmente el estado de las tareas: el sistema informa a cada persona en el momento exacto en que debe actuar o estar al tanto.

Las notificaciones disponibles en V1 se basan en eventos concretos: nueva asignación, validación y rechazo de una tarea. Los recordatorios automáticos de vencimiento se describen al final de este artículo.

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

---

## Recordatorios automáticos y configuración de frecuencia

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

Los recordatorios automáticos programados (aviso previo al vencimiento y notificación en el momento exacto en que una tarea vence) están planificados para una versión futura. Cuando estén disponibles, permitirán configurar la antelación del aviso, activar un segundo recordatorio y ajustar la frecuencia por prioridad de tarea.

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

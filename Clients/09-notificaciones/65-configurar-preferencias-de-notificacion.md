# Configurar preferencias de notificación

CheckBiz360 envía notificaciones push y en-app de forma automática cuando se producen eventos relevantes en la plataforma. Las notificaciones llegan al centro de notificaciones de la app (empleados) o del backoffice (responsables) sin necesidad de ninguna configuración previa.

## Notificaciones que envía el sistema automáticamente

El sistema genera notificaciones ante los siguientes tipos de eventos:

### Para empleados (app móvil)

| Evento | Descripción |
|---|---|
| Nuevo documento disponible | Se asigna un documento al empleado para su consulta o firma |
| Nueva tarea asignada | El responsable asigna una tarea al empleado |
| Tarea validada o rechazada | El responsable emite el resultado de la validación de una tarea completada |
| Jornada aprobada o rechazada | El responsable resuelve una solicitud de jornada manual |

### Para responsables (backoffice y app)

| Evento | Descripción |
|---|---|
| Fichaje sospechoso | El sistema detecta un fichaje irregular en el equipo |
| Empleado que no ha fichado | Un empleado con turno no ha registrado entrada |
| Jornada manual pendiente de aprobación | Un empleado ha enviado una solicitud de jornada que requiere validación |
| Documento firmado | Un empleado ha firmado un documento asignado |
| Tarea completada | Un empleado ha marcado una tarea como terminada |

---

## Configuración de preferencias por el usuario

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La posibilidad de que cada usuario configure de forma individual qué notificaciones desea recibir o desactivar está planificada para una versión futura. Cuando esté disponible, permitirá a los empleados gestionar sus preferencias desde la app y a los responsables configurar la distribución de alertas entre los miembros de su equipo desde el backoffice.

---

## Artículos relacionados

- [Tipos de notificación](63-tipos-de-notificacion.md)
- [Notificaciones push en la app](64-notificaciones-push-en-la-app.md)
- [Alertas para responsables](66-alertas-para-responsables.md)
- [Notificaciones por email](68-notificaciones-por-email.md)

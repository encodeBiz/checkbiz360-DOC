# Tipos de notificación

CheckBiz360 genera notificaciones automáticas para informar a los distintos usuarios de la plataforma sobre eventos relevantes en tiempo real. Las notificaciones están organizadas por categorías según el área operativa a la que pertenecen, y cada tipo tiene unos destinatarios predefinidos según el rol de cada usuario. Este artículo describe todas las categorías y tipos de notificación disponibles en el sistema.

## Categorías de notificación

### Notificaciones de asistencia

Las notificaciones de asistencia informan sobre eventos relacionados con el registro de jornada de los empleados.

| Tipo | Descripción | Destinatarios |
|---|---|---|
| Empleado que no ha fichado | Se genera cuando un empleado con turno activo no ha registrado la entrada pasada la hora configurada como umbral | Manager, Supervisor |
| Jornada incompleta | Se genera al finalizar el turno si el empleado no ha registrado la salida | Manager, Supervisor, Worker |
| Fichaje sospechoso | Se genera cuando el sistema detecta que un fichaje presenta un indicador de anomalía | Manager |
| Fichaje fuera de geocerca | El empleado ha fichado desde una ubicación fuera del radio definido para su sucursal | Manager, Supervisor |
| Jornada manual aprobada | Notifica al empleado que su solicitud de jornada manual ha sido aprobada por el responsable | Worker |
| Jornada manual rechazada | Notifica al empleado que su solicitud de jornada manual ha sido rechazada | Worker |

### Notificaciones de documentos

Las notificaciones de documentos gestionan la distribución de documentos y el seguimiento del acuse de recibo.

| Tipo | Descripción | Destinatarios |
|---|---|---|
| Nuevo documento disponible | Se envía al empleado cuando se le asigna un documento para su consulta | Worker |
| Acuse de recibo pendiente | Recordatorio de que un documento asignado está pendiente de confirmar | Worker |

> **Nota:** la plataforma gestiona **acuse de recibo**, no firma electrónica. No existe, por tanto, una notificación de "documento firmado" ni de rechazo de firma.

### Notificaciones de tareas

Las notificaciones de tareas mantienen informados a empleados y responsables sobre el estado de las tareas asignadas.

| Tipo | Descripción | Destinatarios |
|---|---|---|
| Nueva tarea asignada | Se envía al empleado cuando se le asigna una nueva tarea | Worker |
| Tarea retirada | La tarea se ha borrado, cancelado o ya no está asignada al empleado | Worker |
| Recordatorio de vencimiento | Alerta de que una tarea asignada vence en las próximas horas o al día siguiente | Worker |
| Tarea completada | Notifica al responsable que el empleado ha marcado la tarea como completada | Manager, Supervisor |
| Tarea pendiente de validación | El empleado ha completado la tarea y el sistema espera validación del responsable | Manager, Supervisor |
| Tarea validada | Notifica al empleado que su tarea ha sido validada por el responsable | Worker |
| Tarea rechazada | Notifica al empleado que su tarea ha sido rechazada y requiere revisión | Worker |

### Alertas de seguridad

Las alertas de seguridad son notificaciones de alta prioridad relacionadas con la integridad del sistema y la autenticación. No pueden desactivarse.

| Tipo | Descripción | Destinatarios |
|---|---|---|
| Fichaje sospechoso | Fichaje marcado como potencialmente fraudulento por el motor de análisis | Manager, Owner |
| Dispositivo no autorizado | Se detecta un intento de fichaje desde un dispositivo que no ha sido autorizado para el empleado | Manager, Owner |
| Acceso desde nueva ubicación | Inicio de sesión en el backoffice desde una dirección IP o ubicación inusual | Usuario afectado, Owner |
| Intento de acceso fallido repetido | Se han producido varios intentos fallidos consecutivos de acceso a una cuenta | Usuario afectado, Owner |

> **Aviso:** Las alertas de seguridad no pueden desactivarse por ningún usuario, independientemente de su rol o configuración de preferencias. Su recepción está garantizada por diseño para proteger la integridad operativa de la plataforma.

### Notificaciones administrativas

Las notificaciones administrativas informan sobre procesos que requieren intervención manual por parte de los responsables.

| Tipo | Descripción | Destinatarios |
|---|---|---|
| Jornada manual pendiente de aprobación | Un empleado ha solicitado el registro manual de una jornada que requiere validación | Manager, Supervisor |
| Solicitud de vacaciones o permiso | No se envía aviso: la solicitud aparece en **Contacto → Solicitudes**, con el número de pendientes en la pestaña | Owner, administradores |
| Vacaciones o permiso aprobados / rechazados | Avisa a la persona de la decisión y la lleva a **Mi calendario** (con la próxima versión de la app) | Worker |
| Empleado nuevo activado | Un nuevo empleado ha completado el proceso de activación de su cuenta | Manager, Owner |
| Acceso que no ha llegado | Alerta de la portada del panel cuando el correo de acceso de alguien rebotó, se marcó como spam o no salió | Owner, administradores |

## Canales de entrega

Las notificaciones de CheckBiz360 se envían a través de dos canales principales:

- **Notificación push en la app**: para los empleados (Workers) y, cuando corresponde, para los responsables que tengan la app instalada.
- **Notificación en el backoffice**: aparece en el centro de notificaciones del panel de administración, visible para Manager, Supervisor y Owner.

Algunos tipos de notificación disponen adicionalmente de un canal de respaldo por correo electrónico para garantizar su entrega incluso cuando el dispositivo no está disponible. Los detalles sobre configuración de canales y preferencias se describen en los artículos correspondientes de esta sección.

---

> **Nota de rol:** La visualización de notificaciones depende del rol del usuario. Cada rol recibe únicamente las notificaciones que le corresponden según la tabla anterior. El Owner recibe todas las notificaciones administrativas y de seguridad de forma consolidada para toda la entidad.

## Artículos relacionados

- [Notificaciones push en la app](64-notificaciones-push-en-la-app.md)
- [Configurar preferencias de notificación](65-configurar-preferencias-de-notificacion.md)
- [Alertas para responsables](66-alertas-para-responsables.md)
- [Historial de notificaciones](67-historico-de-notificaciones.md)
- [Notificaciones por email](68-notificaciones-por-email.md)

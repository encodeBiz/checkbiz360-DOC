# Notificaciones push en la app

Las notificaciones push son el canal principal mediante el que CheckBiz360 comunica eventos relevantes a los empleados en tiempo real. Cuando ocurre un evento que requiere la atención del empleado —una tarea asignada, un documento pendiente de acuse de recibo, una aprobación de jornada— el sistema envía una notificación directamente al dispositivo móvil, incluso si la app no está abierta en ese momento. Este artículo explica cómo funcionan estas notificaciones, qué información contienen y qué hacer si no llegan correctamente.

## Cómo llegan las notificaciones push al dispositivo

Cuando se genera un evento en CheckBiz360 que tiene a un empleado como destinatario, el servidor envía una notificación push a través del servicio de mensajería del sistema operativo del dispositivo: APNs (Apple Push Notification service) para dispositivos iOS y FCM (Firebase Cloud Messaging) para dispositivos Android.

El proceso completo, desde que se genera el evento hasta que aparece la notificación en la pantalla del empleado, dura habitualmente menos de cinco segundos si el dispositivo está conectado a internet. Si el dispositivo está sin conexión en el momento del envío, la notificación se entregará en cuanto recupere la conectividad, siempre que no haya transcurrido el tiempo de expiración del sistema operativo (generalmente 24 horas).

## Qué información contiene cada notificación

El contenido de cada notificación varía según su tipo, pero todas incluyen como mínimo:

- **Título**: identifica el tipo de evento de forma concisa (por ejemplo, "Nuevo documento disponible" o "Tarea asignada").
- **Cuerpo**: breve descripción del evento con el dato más relevante (nombre del documento, nombre de la tarea, nombre del responsable que ha aprobado la jornada).
- **Marca de tiempo**: momento en que se generó el evento.

Algunos tipos de notificación incluyen información adicional:

- Las notificaciones de **documentos pendientes de acuse de recibo** incluyen el nombre del documento.
- Las notificaciones de **tareas** incluyen el nombre de la tarea, la fecha de vencimiento y la sucursal o proyecto al que está vinculada.
- Las notificaciones de **jornada** incluyen el resultado de la validación (aprobada o rechazada) y, en caso de rechazo, el motivo indicado por el responsable.

## Comportamiento al pulsar la notificación

Pulsar sobre una notificación push abre la app CheckBiz360 y navega directamente al recurso al que hace referencia esa notificación. No es necesario buscar manualmente la información dentro de la app; el sistema lleva al empleado al lugar exacto donde debe actuar.

| Tipo de notificación | Destino en la app |
|---|---|
| Nuevo documento / Acuse pendiente | Pantalla de detalle del documento con el botón de acuse de recibo visible |
| Tarea asignada / Recordatorio de vencimiento | Pantalla de detalle de la tarea con las acciones disponibles |
| Jornada aprobada / rechazada | Registro de jornada correspondiente |
| Alerta de seguridad | Pantalla de seguridad de la cuenta |

Si la app no está instalada en el dispositivo o el empleado no ha iniciado sesión, pulsar la notificación abrirá la tienda de aplicaciones o la pantalla de inicio de sesión según corresponda.

## Requisitos para recibir notificaciones push

Para que las notificaciones push funcionen correctamente deben cumplirse las siguientes condiciones:

1. **La app CheckBiz360 debe estar instalada** en el dispositivo del empleado (iOS o Android).
2. **El empleado debe haber iniciado sesión** al menos una vez en la app, para que el sistema registre el token de dispositivo necesario para el envío.
3. **Los permisos de notificación deben estar concedidos** en el sistema operativo del dispositivo. Si el empleado denegó los permisos durante la instalación, las notificaciones no llegarán aunque el sistema las envíe correctamente.
4. **El dispositivo debe tener conexión a internet** en algún momento dentro del periodo de validez de la notificación.

> **Aviso:** El sistema operativo del dispositivo puede limitar o demorar las notificaciones en función del modo de ahorro de batería, del modo de no molestar o de restricciones de segundo plano de la app. Si el empleado tiene activado alguno de estos modos, puede que no reciba las notificaciones de forma inmediata.

## Qué hacer si no llegan las notificaciones

Si un empleado no recibe las notificaciones push, siga estos pasos de diagnóstico en orden:

### 1. Verificar los permisos del sistema operativo

**En iOS:**
1. Abra **Ajustes** en el iPhone o iPad.
2. Desplácese hasta la app **CheckBiz360** y púlsela.
3. Acceda a **Notificaciones** y compruebe que el interruptor principal está activado.
4. Asegúrese de que el tipo de alerta seleccionado es **Pantalla de bloqueo**, **Centro de notificaciones** o **Banners**, o todos ellos.

**En Android:**
1. Mantenga pulsado el icono de la app **CheckBiz360** y seleccione **Información de la app**.
2. Pulse **Notificaciones** y compruebe que están activadas.
3. Verifique que no hay canales de notificación específicos desactivados.

### 2. Verificar que la sesión está activa

El empleado debe tener una sesión activa en la app. Si la sesión ha expirado por inactividad prolongada, el token de dispositivo puede haber quedado desactualizado. Cerrar sesión y volver a iniciarla regenera el token y restablece la recepción de notificaciones.

### 3. Comprobar la conexión a internet

Asegúrese de que el dispositivo tiene conexión activa a internet, tanto por WiFi como por datos móviles.

### 4. Contactar con soporte

Si los pasos anteriores no resuelven el problema, contacte con el equipo de soporte de CheckBiz360 indicando el sistema operativo y versión del dispositivo, la versión de la app instalada y el tipo de notificación que no está recibiendo.

---

> **Nota de rol:** Las notificaciones push en la app están dirigidas principalmente al rol **Worker**. Los roles **Manager** y **Supervisor** también pueden recibir notificaciones push si tienen la app instalada, aunque su canal principal de notificaciones es el backoffice web.

## Artículos relacionados

- [Tipos de notificación](63-tipos-de-notificacion.md)
- [Configurar preferencias de notificación](65-configurar-preferencias-de-notificacion.md)
- [Historial de notificaciones](67-historico-de-notificaciones.md)
- [Notificaciones por email](68-notificaciones-por-email.md)

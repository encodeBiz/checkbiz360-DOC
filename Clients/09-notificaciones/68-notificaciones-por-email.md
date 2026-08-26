# Notificaciones por email

CheckBiz360 envía correos electrónicos automáticos en determinados eventos del ciclo de vida de la cuenta. Este artículo describe qué correos envía el sistema, cuándo y desde qué dirección, y qué hacer si alguno de estos correos no llega al destinatario.

## Remitente de los correos del sistema

Todos los correos automáticos de CheckBiz360 se envían desde la dirección `hola@encodebiz.com`. Si algún miembro de su organización no encuentra un correo esperado, debe revisar la carpeta de spam o correo no deseado y comprobar que esta dirección no está bloqueada por el filtro de correo corporativo.

> **Aviso:** Algunos sistemas de correo corporativo con filtros estrictos (como Microsoft 365 con políticas de seguridad avanzadas) pueden clasificar los correos de `hola@encodebiz.com` como spam o retenerlos en cuarentena. Si esto ocurre de forma sistemática, solicite al administrador de TI de su organización que añada el dominio `encodebiz.com` a la lista de remitentes de confianza.

## Correos automáticos del sistema

### Bienvenida al nuevo empleado

Cuando el Owner o un Manager añade un nuevo empleado a la plataforma y envía la invitación, el sistema genera automáticamente un correo de bienvenida dirigido a la dirección de email del empleado. Este correo contiene:

- Un mensaje de bienvenida a la plataforma en nombre de la empresa.
- Las credenciales de acceso iniciales: dirección de email y contraseña temporal.
- Un enlace directo para descargar la app CheckBiz360 en iOS y Android.
- Instrucciones básicas para completar el primer acceso y cambiar la contraseña temporal.

Este correo es el primer punto de contacto del empleado con la plataforma y es fundamental para que pueda activar su cuenta. Por ello, es especialmente importante que la dirección de email del empleado sea correcta en el momento de crear su ficha.

### Reenvío de invitación

Si el empleado no ha podido activar su cuenta (no encontró el correo, expiró el enlace o ingresó datos incorrectos), el responsable puede reenviar la invitación desde el backoffice:

1. Navegue a **Empleados** y abra la ficha del empleado cuya invitación desea reenviar.
2. Localice el indicador de estado de la cuenta. Si la cuenta no está activada, aparecerá el botón **Reenviar invitación**.
3. Pulse el botón. El sistema enviará un nuevo correo de bienvenida con una nueva contraseña temporal a la dirección de email del empleado.

> **Aviso:** Reenviar la invitación invalida la contraseña temporal anterior. Si el empleado ya había recibido la primera invitación y la estaba usando, deberá emplear la nueva contraseña del segundo envío.

### Restablecimiento de contraseña

Cuando un usuario solicita restablecer su contraseña (desde la pantalla de inicio de sesión, pulsando "He olvidado mi contraseña"), el sistema envía un correo con un enlace seguro de restablecimiento. Este enlace es válido durante 30 minutos desde el momento del envío. Una vez expirado, el usuario debe solicitar un nuevo enlace.

El correo incluye:
- Un botón con el enlace de restablecimiento.
- La hora de expiración del enlace.
- Un aviso de que si el usuario no solicitó el restablecimiento, puede ignorar el correo.

---

## Notificaciones por email adicionales y fallback

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

El envío de notificaciones operativas por email (alertas de eventos, recordatorios de acuse de recibo, avisos de tareas, etc.) y el mecanismo de fallback automático por email cuando una notificación push no puede entregarse al dispositivo del usuario están planificados para una versión futura de la plataforma.

---

## Qué hacer si el correo no llega

Si un empleado o responsable no recibe un correo esperado del sistema, siga estos pasos:

1. **Revise la carpeta de spam o correo no deseado** en el cliente de correo. Los correos de `hola@encodebiz.com` pueden ser clasificados incorrectamente la primera vez.
2. **Verifique la dirección de email** del destinatario en el backoffice. Acceda a la ficha del empleado o usuario y confirme que la dirección está escrita correctamente y sin espacios adicionales.
3. **Reenvíe la invitación** si se trata del correo de bienvenida (véase el apartado anterior).
4. **Contacte con el administrador de TI** de su organización para verificar que el dominio `encodebiz.com` no está bloqueado o en cuarentena.
5. Si el problema persiste, contacte con el soporte de CheckBiz360 indicando la dirección de email del destinatario y el tipo de correo que no está llegando.

---

> **Nota de rol:** Los correos de bienvenida y restablecimiento de contraseña van dirigidos a todos los usuarios independientemente de su rol. El reenvío de invitaciones puede realizarlo el **Owner** y el **Manager**.

## Artículos relacionados

- [Tipos de notificación](63-tipos-de-notificacion.md)
- [Notificaciones push en la app](64-notificaciones-push-en-la-app.md)
- [Configurar preferencias de notificación](65-configurar-preferencias-de-notificacion.md)
- [Historial de notificaciones](67-historico-de-notificaciones.md)

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

### Saber si llegó y reenviar el acceso

En la ficha de cada empleado, el bloque **Acceso a la app** dice qué ha pasado con su correo de bienvenida: entregado, rebotado, marcado como spam o sin enviar. También dice si la persona ya ha usado la app. Si el correo no ha llegado, la portada del panel lo avisa con la alerta **Acceso que no ha llegado**.

Para mandarlo otra vez:

1. Navegue a **Empleados** y abra la ficha del empleado.
2. En **Acceso a la app**, pulse **Reenviar acceso**.
3. Confirme. El sistema envía un nuevo correo de bienvenida con una contraseña nueva.

> **Aviso:** Reenviar el acceso invalida la contraseña anterior, también para el panel si la persona lo usa. Si el correo rebotó, la dirección está mal: cámbiela con **Cambiar correo** y mande el acceso a la nueva.

Se explica entero en [Acceso a la app y cambio de correo](../02-empleados/116-acceso-a-la-app-y-cambio-de-correo.md).

### Tarjeta del punto de fichaje

Con el [punto de fichaje](../03-control-horario/113-punto-de-fichaje.md) contratado, cada persona puede recibir por correo su tarjeta, con su QR y su código de 6 cifras. Se envía desde la ficha del empleado o para toda una sucursal desde **Punto de fichaje → Tarjetas QR**.

### Restablecimiento de contraseña

Cuando un usuario solicita restablecer su contraseña (desde la pantalla de inicio de sesión, pulsando "He olvidado mi contraseña"), el sistema envía un correo con un enlace seguro de restablecimiento. Este enlace es válido durante 30 minutos desde el momento del envío. Una vez expirado, el usuario debe solicitar un nuevo enlace.

El correo incluye:
- Un botón con el enlace de restablecimiento.
- La hora de expiración del enlace.
- Un aviso de que si el usuario no solicitó el restablecimiento, puede ignorar el correo.

---

## Avisos de trabajo por correo, para quien no usa la app

Hay personas que no llevan la app, o que no la miran. Para ellas, en **Horarios y festivos** de su ficha está la casilla **Enviar notificaciones por email**. Con ella marcada, además de los avisos de la app, recibe por correo:

- **Sus tareas**: las que le asignan, le cambian o le retiran. Llegan agrupadas para no llenarle el buzón: el correo sale cuando pasan 15 minutos sin cambios nuevos. Si la tarea empieza en las próximas 24 horas, el aviso sale al momento.
- **Su horario de la semana siguiente**, el domingo a las 18:00 en la hora de la empresa, con sus turnos, sus tareas y el lugar de cada una. Si no ha cambiado nada desde el último envío, no se repite.

Nada del fichaje va por correo. La casilla viene desmarcada y se marca persona a persona.

## Aviso de almacenamiento

Cuando su empresa llega al 90 % del almacenamiento incluido en su plan, el propietario recibe un correo en la dirección de facturación. Se manda una sola vez. Vuelve a mandarse solo si el uso baja del 80 % y después sube otra vez. Ver [Planes, precios y funcionalidades](../14-referencia/91-planes-y-funcionalidades.md#almacenamiento).

## Alertas operativas por correo

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

El envío por correo de las alertas de la portada a los responsables, y el respaldo automático por correo cuando una notificación push no llega al dispositivo, están planificados para una versión futura.

---

## Qué hacer si el correo no llega

Si un empleado o responsable no recibe un correo esperado del sistema, siga estos pasos:

1. **Revise la carpeta de spam o correo no deseado** en el cliente de correo. Los correos de `hola@encodebiz.com` pueden ser clasificados incorrectamente la primera vez.
2. **Verifique la dirección de email** del destinatario en el backoffice. Acceda a la ficha del empleado o usuario y confirme que la dirección está escrita correctamente y sin espacios adicionales.
3. **Mire el bloque Acceso a la app** de su ficha si se trata del correo de bienvenida: dice si se entregó, si rebotó o si se marcó como spam. Después, **reenvíe el acceso** (véase el apartado anterior).
4. **Contacte con el administrador de TI** de su organización para verificar que el dominio `encodebiz.com` no está bloqueado o en cuarentena.
5. Si el problema persiste, contacte con el soporte de CheckBiz360 indicando la dirección de email del destinatario y el tipo de correo que no está llegando.

---

> **Nota de rol:** Los correos de bienvenida y restablecimiento de contraseña van dirigidos a todos los usuarios independientemente de su rol. Reenviar el acceso y cambiar el correo puede hacerlo quien edita las fichas de los empleados: el **Owner**, los administradores y el **Manager**.

## Artículos relacionados

- [Tipos de notificación](63-tipos-de-notificacion.md)
- [Notificaciones push en la app](64-notificaciones-push-en-la-app.md)
- [Configurar preferencias de notificación](65-configurar-preferencias-de-notificacion.md)
- [Historial de notificaciones](67-historico-de-notificaciones.md)

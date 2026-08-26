# Autenticación en dos factores (2FA)

La autenticación en dos factores (2FA) añade una capa de seguridad adicional al proceso de inicio de sesión en CheckBiz360. Una vez activada, el acceso a la cuenta requiere no solo la contraseña del usuario, sino también un código de verificación generado por una aplicación en su dispositivo móvil.

Esta medida reduce significativamente el riesgo de accesos no autorizados, incluso en caso de que la contraseña de un empleado sea comprometida. Su activación es especialmente recomendable para perfiles con nivel de acceso elevado, como managers y owners.

---

## Cómo funciona la autenticación en dos factores

Cuando el empleado activa el 2FA, cada vez que inicia sesión en CheckBiz360 debe completar dos pasos:

1. Introducir su email y contraseña habituales.
2. Introducir un código numérico de 6 dígitos generado por su aplicación autenticadora.

El código es válido durante un intervalo de tiempo breve (generalmente 30 segundos) y se regenera automáticamente. Este diseño garantiza que, aunque alguien obtenga la contraseña, no pueda acceder sin tener también el dispositivo físico del empleado.

---

## Configurar el 2FA desde la aplicación

### Paso a paso para el empleado

1. Inicie sesión con sus credenciales: en la app móvil, desde la sección de perfil; en el backoffice, desde **Mi cuenta**.
2. Localice el apartado de **seguridad** de su cuenta.
3. Active la opción **Autenticación en dos factores**.
4. La plataforma generará un código QR y una clave secreta manual.
5. Abra su aplicación autenticadora (ver opciones en la siguiente sección) y añada una nueva cuenta.
6. Escanee el código QR con la cámara de su dispositivo o, si prefiere introducirlo manualmente, copie la clave secreta mostrada en pantalla.
7. La aplicación autenticadora comenzará a generar códigos de 6 dígitos de forma automática.
8. Introduzca el código actual de 6 dígitos en la pantalla de verificación de CheckBiz360 y pulse **Confirmar**.

El 2FA quedará activado a partir de ese momento.

---

## Aplicaciones autenticadoras compatibles

CheckBiz360 es compatible con cualquier aplicación que implemente el estándar TOTP (Time-based One-Time Password). Las más habituales son:

- **Google Authenticator** — Disponible para Android e iOS.
- **Microsoft Authenticator** — Disponible para Android e iOS.
- **Authy** — Disponible para Android, iOS y escritorio. Permite copias de seguridad cifradas en la nube.

> **Nota:** Se recomienda utilizar Authy si el empleado desea mantener una copia de seguridad de sus tokens en caso de pérdida o cambio de dispositivo.

---

## Dispositivos de confianza

Durante el proceso de verificación con 2FA, la aplicación puede ofrecer la opción de marcar el dispositivo actual como **dispositivo de confianza**. Esta opción permite que el sistema no solicite el código 2FA en los próximos inicios de sesión desde ese mismo dispositivo, durante un periodo de tiempo configurado.

Los dispositivos de confianza son útiles para empleados que trabajan habitualmente desde el mismo teléfono o tableta y no quieren introducir el código en cada acceso.

> **Nota:** No marque un dispositivo como de confianza si no es de uso exclusivo personal. En dispositivos compartidos, desactive esta opción para mantener la seguridad del acceso.

---

## Activar o desactivar el 2FA desde el backoffice

Los responsables de la empresa pueden gestionar el estado del 2FA de cualquier empleado directamente desde el backoffice, sin necesidad de que el propio empleado intervenga:

1. Acceda al backoffice con credenciales de manager u owner.
2. Vaya a **Empleados** y abra el perfil del empleado.
3. En la sección **Seguridad**, localice el control **Autenticación en dos factores**.
4. Active o desactive el interruptor según corresponda.
5. Guarde los cambios.

> **Nota:** La desactivación del 2FA desde el backoffice elimina inmediatamente el requisito del segundo factor para ese empleado. Use esta opción con cautela y solo cuando sea estrictamente necesario.

---

## Recuperación de acceso si se pierde el dispositivo

Si un empleado pierde el dispositivo con el que había configurado el 2FA y no puede generar el código de verificación, el proceso de recuperación es el siguiente:

1. El empleado contacta con su manager u owner.
2. El responsable accede al backoffice y desactiva temporalmente el 2FA en el perfil del empleado.
3. El empleado inicia sesión con su contraseña habitual sin necesidad de código.
4. Una vez dentro, el empleado configura el 2FA de nuevo con su nuevo dispositivo siguiendo los pasos descritos anteriormente.
5. El manager puede volver a habilitar el requisito de 2FA una vez completada la reconfiguración.

---

## Quién puede gestionar el 2FA de otros empleados

La activación y desactivación del 2FA desde el backoffice está disponible para los roles **manager** (nivel 3) y **owner** (nivel 4). Los propios empleados pueden configurar su 2FA desde la aplicación móvil independientemente de su rol.

---

## Artículos relacionados

- [Biometría y dispositivos de confianza](10-biometria-y-dispositivos-de-confianza.md)
- [Crear y gestionar empleados](06-crear-y-gestionar-empleados.md)
- [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md)
- [Empleados multi-entidad](11-empleados-multi-entidad.md)

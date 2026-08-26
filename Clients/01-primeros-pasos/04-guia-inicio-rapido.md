# Guía de inicio rápido

Esta guía le permite tener CheckBiz360 completamente operativo —con su primera sucursal configurada, un empleado activo y un fichaje validado— en menos de quince minutos. Está pensada para el responsable de cuenta (rol Owner) que acaba de registrarse y quiere verificar que todo funciona correctamente antes de extender la plataforma al resto del equipo.

Siga los diez pasos en orden. Cada uno construye sobre el anterior.

**Tiempo estimado:** 10-15 minutos.

**Prerrequisitos:**
- Conexión a internet.
- Dispositivo Android (5.0 o superior) o iOS (13 o superior).
- Correo electrónico corporativo para la cuenta Owner.

---

## Los 10 pasos

### Paso 1. Crear cuenta y entidad

Acceda a `saas.encodebiz.com` y regístrese con su correo corporativo, su teléfono y una contraseña. Al enviar el formulario, el sistema le lleva directamente a la creación de la entidad: **nombre de la empresa**, **razón social** y **dirección** son obligatorios; el NIF y el email de facturación, opcionales.

La zona horaria se resuelve a partir de la dirección y sirve como valor por defecto para las sucursales.

> **Nota:** para poder contratar el plan hará falta tener completos los datos legales y un método de pago. Consulte [Planes, precios y funcionalidades](../14-referencia/91-planes-y-funcionalidades.md).

### Paso 2. Crear la primera sucursal con geocerca

Entre en **Sucursales** y cree una:

- **Nombre** de la sucursal (por ejemplo, "Oficina Principal").
- **Dirección** completa del centro; de ella salen las coordenadas y la zona horaria.
- **Zona de chequeo en metros**: empiece por **100** si no tiene una referencia.

Guarde la sucursal.

### Paso 3. Configurar el horario de la sucursal

Vaya a **Calendario** y sitúese en la pestaña **Sucursal**:

1. Seleccione los días laborables (por ejemplo, lunes a viernes).
2. Establezca la hora de entrada y la de salida de cada día (por ejemplo, 09:00-17:00).
3. Elija la **modalidad de jornada**: estricta, si manda el horario oficial; flexible, si manda el tiempo realmente trabajado.
4. Guarde el calendario.

Este horario es la referencia contra la que el sistema valida cada fichaje.

> **Nota:** puede añadir varios turnos por día y pausas dentro de cada turno. Para este primer arranque, un horario simple es suficiente. La alternancia automática de semanas A/B no está disponible; consulte [Turnos rotativos](../04-calendario-y-horarios/27-turnos-rotativos.md).

### Paso 4. Crear el primer empleado

Entre en **Empleados** y cree uno nuevo con los datos obligatorios: **nombre completo**, **correo electrónico**, **teléfono** y **tipo de relación** (interno o colaborador).

Guarde. Después, desde la ficha del empleado, **vincúlelo con la sucursal**: es ahí donde se elige su responsabilidad —para este arranque, *worker*—, su puesto y su tarifa horaria.

### Paso 5. El empleado recibe el correo de bienvenida

El sistema enviará automáticamente un correo al empleado con:

- El enlace para activar la cuenta y establecer su contraseña.
- Las instrucciones para descargar la app.

> **Nota:** si el correo no llega en unos minutos, pida al empleado que revise la carpeta de spam y compruebe que la dirección está bien escrita en su ficha. Consulte [Problemas frecuentes y soluciones](../13-soporte-e-incidencias/88-problemas-frecuentes-y-soluciones.md).

### Paso 6. El empleado descarga la app CheckBiz360

El empleado descarga la aplicación desde la tienda oficial de su dispositivo:

- **iOS**: App Store — buscar "CheckBiz360".
- **Android**: Google Play — buscar "CheckBiz360".

La instalación tarda menos de un minuto en la mayoría de dispositivos con conexión WiFi.

### Paso 7. El empleado inicia sesión en la app

Con la app instalada, el empleado:

1. Abre la app CheckBiz360.
2. Introduce su correo electrónico y la contraseña que estableció al activar la cuenta.
3. Selecciona la organización si aparece más de una (habitual cuando un empleado trabaja para varias empresas).
4. Accede a la pantalla principal de fichaje.

### Paso 8. El empleado configura la autenticación en dos factores (2FA)

Aunque opcional, se recomienda activar el 2FA en el primer inicio de sesión. El empleado lo activa desde el apartado de seguridad de su perfil, siguiendo las instrucciones en pantalla para vincular su cuenta con una app de autenticación.

> **Nota:** El 2FA puede configurarse como obligatorio para todos los empleados desde la configuración de la entidad en el backoffice. Si su empresa maneja datos sensibles o tiene requisitos de auditoría, se recomienda activar esta opción.

### Paso 9. Primer fichaje de entrada desde la app

Con el empleado ya dentro de la sucursal o en sus proximidades:

1. El empleado abre la app CheckBiz360.
2. Pulsa el botón **Fichar entrada**.
3. La app valida la ubicación GPS frente a la geocerca de la sucursal.
4. Si la ubicación es correcta, el fichaje queda registrado y aparece un mensaje de confirmación.

Si la ubicación no es válida, la app indicará que el dispositivo está fuera del perímetro definido.

### Paso 10. Verificar el registro en el backoffice

En el backoffice, entre en **Asistencia**.

Compruebe que:

- Aparece el registro del empleado con estado **válido**.
- La hora coincide con el fichaje realizado.

Si el registro aparece como **fallido**, el detalle indica el código del motivo —fuera de la zona de chequeo, fuera de horario— que puede consultar en [Códigos de error completos](../14-referencia/90-codigos-de-error-completos.md).

---

## Resultado al completar los 10 pasos

Al terminar esta guía, su cuenta de CheckBiz360 tiene:

- Una entidad y una sucursal configuradas.
- Un empleado activo con acceso a la app.
- El primer registro de asistencia validado y visible en el backoffice.

A partir de este punto, puede replicar el proceso para el resto de sucursales y empleados, o explorar los módulos avanzados: análisis de costes, informes de cumplimiento normativo y gestión documental.

## Artículos relacionados

- [Crear cuenta y configurar la entidad](03-crear-cuenta-y-configurar-entidad.md)
- [Estructura de la plataforma](05-estructura-de-la-plataforma.md)
- [Check-in y check-out desde la app](../03-control-horario/14-checkin-checkout-desde-app.md)
- [Crear y gestionar sucursales](../08-sucursales-y-entidad/57-crear-y-gestionar-sucursales.md)

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

Acceda a [encodebiz.com](https://encodebiz.com), regístrese con su correo corporativo y complete el asistente de configuración de la entidad: nombre de la empresa, NIF/CIF, dirección fiscal y zona horaria por defecto.

Cuando el asistente termine, accederá directamente al backoffice de CheckBiz360.

> **Nota:** Verifique su correo electrónico antes de continuar. Sin verificación, no podrá enviar invitaciones a empleados.

### Paso 2. Crear la primera sucursal con geocerca

Diríjase a **Sucursales > Nueva sucursal** e introduzca:

- Nombre de la sucursal (por ejemplo, "Oficina Principal").
- Dirección completa del centro.
- Radio de geocerca: comience con **100 metros** si no tiene un valor de referencia.
- Zona horaria (deje la heredada de la entidad si opera en la misma zona).

Guarde la sucursal. El mapa mostrará la geocerca activa sobre la dirección introducida.

### Paso 3. Configurar el horario de la sucursal

Dentro de la sucursal recién creada, acceda a la pestaña **Horarios** y defina el horario base:

1. Seleccione los días laborables (por ejemplo, lunes a viernes).
2. Establezca la hora de entrada y la hora de salida (por ejemplo, 09:00-17:00).
3. Guarde el horario.

Este horario es la referencia que el sistema utilizará para calcular tardanzas, ausencias y horas extra.

> **Nota:** Puede configurar horarios por turnos (mañana, tarde, noche) o semanas alternas desde la sección de horarios avanzados. Para este primer arranque, un horario fijo es suficiente.

### Paso 4. Crear el primer empleado

Diríjase a **Empleados > Nuevo empleado** e introduzca:

- Nombre completo.
- Correo electrónico del empleado.
- Rol: seleccione **Worker**.
- Sucursal asignada: la que acaba de crear.

Haga clic en **Guardar y enviar invitación**.

### Paso 5. El empleado recibe el correo de bienvenida

El sistema enviará automáticamente un correo al empleado con:

- Sus credenciales de acceso (o enlace para establecer contraseña).
- El enlace de descarga de la app CheckBiz360.
- El nombre de la sucursal y el rol asignado.

El empleado tiene 72 horas para activar su cuenta.

> **Nota:** Si el correo no llega en los primeros 5 minutos, solicite al empleado que revise la carpeta de spam. También puede reenviar la invitación desde **Empleados > [nombre del empleado] > Reenviar invitación**.

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

Aunque opcional, se recomienda activar el 2FA en el primer inicio de sesión. El empleado puede hacerlo desde **Perfil > Seguridad > Activar 2FA**, siguiendo las instrucciones en pantalla para vincular su cuenta con una app de autenticación.

> **Nota:** El 2FA puede configurarse como obligatorio para todos los empleados desde **Configuración > Seguridad** en el backoffice. Si su empresa maneja datos sensibles o tiene requisitos de auditoría, se recomienda activar esta opción.

### Paso 9. Primer fichaje de entrada desde la app

Con el empleado ya dentro de la sucursal o en sus proximidades:

1. El empleado abre la app CheckBiz360.
2. Pulsa el botón **Fichar entrada**.
3. La app valida la ubicación GPS frente a la geocerca de la sucursal.
4. Si la ubicación es correcta, el fichaje queda registrado y aparece un mensaje de confirmación.

Si la ubicación no es válida, la app indicará que el dispositivo está fuera del perímetro definido.

### Paso 10. Verificar el registro en el backoffice

En el backoffice, diríjase a **Registros > Hoy** (o a **Sucursales > [su sucursal] > Registros**).

Compruebe que:

- Aparece el registro del empleado con estado **Válido**.
- La hora coincide con el fichaje realizado.
- La ubicación se muestra dentro del perímetro de la geocerca.

Si el registro aparece con estado **Anomalía**, consulte el detalle para ver el motivo (ubicación fuera de geocerca, fichaje fuera de horario, entre otros).

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
- [Cómo funciona el fichaje en la app](../10-app-movil/)
- [Gestión de sucursales y geocercas](../08-sucursales-y-entidad/)

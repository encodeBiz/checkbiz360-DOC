# Crear cuenta y configurar la entidad

Antes de que cualquier empleado pueda fichar, es necesario configurar la estructura base de su organización en CheckBiz360. Este proceso se realiza una sola vez y establece los cimientos sobre los que se construirá todo lo demás: horarios, sucursales, empleados y políticas de control.

Este artículo le guía por los cinco pasos necesarios para pasar de cero a tener su primera sucursal operativa y el primer empleado invitado a la plataforma.

> **Nota:** Este proceso debe realizarlo el propietario de la cuenta (rol Owner). Ningún otro rol tiene permisos para crear o modificar la configuración de la entidad.

## Conceptos previos

Antes de comenzar, conviene tener claros tres términos que estructuran la plataforma:

- **Entidad**: es su empresa. Contiene la configuración global: zona horaria por defecto, festivos nacionales y políticas base que se aplican a toda la organización.
- **Sucursal**: es cada unidad operativa (tienda, oficina, obra, proyecto). Hereda la configuración de la entidad, pero puede tener su propia zona horaria, geocerca y festivos locales.
- **Empleado**: se asigna a una o varias sucursales con un rol determinado. Hereda la configuración de la entidad y la sucursal, con posibilidad de excepciones individuales.

## Paso 1. Registrarse en encodebiz.com

1. Acceda a [encodebiz.com](https://encodebiz.com) desde cualquier navegador.
2. Haga clic en **Empezar gratis** o **Crear cuenta**.
3. Introduzca su nombre, dirección de correo electrónico y contraseña.
4. Acepte los términos de servicio y la política de privacidad.
5. Haga clic en **Crear cuenta**.
6. Recibirá un correo de verificación. Ábralo y haga clic en el enlace para confirmar su dirección.

> **Nota:** Utilice una dirección de correo corporativa. Esta dirección quedará vinculada como Owner de la cuenta y recibirá todas las notificaciones administrativas de la plataforma.

## Paso 2. Crear la entidad

Una vez verificada su cuenta, el sistema le guiará automáticamente por el asistente de configuración inicial. Si ya tiene acceso al backoffice, diríjase a **Configuración > Entidad**.

Rellene los siguientes campos:

| Campo | Descripción | Ejemplo |
|---|---|---|
| Nombre de la empresa | Denominación comercial o razón social | Distribuciones García, S.L. |
| NIF / CIF | Identificación fiscal | B12345678 |
| Dirección fiscal | Domicilio social de la empresa | Calle Mayor, 10, Madrid |
| Zona horaria por defecto | Se aplicará a todas las sucursales salvo que se especifique otra | Europe/Madrid |
| Sector de actividad | Ayuda a personalizar las alertas y recomendaciones | Retail |

Haga clic en **Guardar entidad** para continuar.

## Paso 3. Crear la primera sucursal

Con la entidad configurada, el siguiente paso es dar de alta al menos una sucursal. Diríjase a **Sucursales > Nueva sucursal**.

Rellene los campos obligatorios:

1. **Nombre de la sucursal**: nombre interno que identifica la unidad operativa (por ejemplo, "Tienda Centro" o "Oficina Madrid").
2. **Dirección**: dirección completa del centro. El sistema la geocodificará automáticamente para obtener las coordenadas GPS.
3. **Radio de geocerca (metros)**: distancia máxima desde la cual un empleado puede realizar un fichaje válido. El valor habitual oscila entre 50 y 200 metros en función del tamaño del centro.
4. **Zona horaria**: si la sucursal opera en una zona horaria diferente a la de la entidad, especifíquela aquí. En caso contrario, heredará el valor por defecto.

> **Nota:** La geocerca es el mecanismo que impide los fichajes fraudulentos desde fuera del centro. Un radio demasiado amplio reduce su efectividad; un radio demasiado estrecho puede generar falsos rechazos por imprecisión del GPS del dispositivo móvil. Para la mayoría de oficinas y tiendas, un radio de 100 metros es un punto de partida adecuado.

Haga clic en **Guardar sucursal**.

## Paso 4. Invitar al primer empleado

Con la sucursal creada, puede dar de alta al primer empleado. Diríjase a **Empleados > Nuevo empleado**.

1. Introduzca el nombre completo, el correo electrónico y el rol (en este primer caso, seleccione **Worker**).
2. Asigne el empleado a la sucursal que acaba de crear.
3. Haga clic en **Enviar invitación**.

El empleado recibirá un correo electrónico con un enlace de activación y las instrucciones para descargar la app CheckBiz360.

> **Nota:** El enlace de invitación tiene una validez de 72 horas. Si el empleado no activa su cuenta en ese plazo, puede reenviar la invitación desde el panel de empleados.

## Paso 5. Descargar la app CheckBiz360

La app CheckBiz360 está disponible de forma gratuita en las tiendas oficiales:

- **iOS**: App Store, buscando "CheckBiz360"
- **Android**: Google Play, buscando "CheckBiz360"

El empleado debe descargarla en su dispositivo antes de realizar el primer fichaje. Una vez instalada, iniciará sesión con las credenciales que recibió por correo.

## Estado al finalizar estos pasos

Cuando complete este proceso, su organización tendrá:

- Una entidad configurada con su información fiscal y zona horaria.
- Una sucursal operativa con geocerca activa.
- Un empleado invitado con acceso a la app.

A partir de aquí, puede replicar el proceso para crear más sucursales e invitar al resto de su equipo, o consultar la guía de inicio rápido para hacer el primer fichaje de prueba.

## Artículos relacionados

- [Guía de inicio rápido](04-guia-inicio-rapido.md)
- [Estructura de la plataforma](05-estructura-de-la-plataforma.md)
- [Gestión de sucursales](../08-sucursales-y-entidad/)
- [Roles y permisos](../02-empleados/)

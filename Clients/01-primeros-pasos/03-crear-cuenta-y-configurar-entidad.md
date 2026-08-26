# Crear cuenta y configurar la entidad

Antes de que cualquier empleado pueda fichar hay que montar la estructura base de su organización en CheckBiz360. Es un proceso que se hace una sola vez y que deja los cimientos sobre los que se apoya todo lo demás: horarios, sucursales, empleados y políticas de control.

Este artículo recorre el camino desde el registro hasta tener la primera sucursal operativa y el primer empleado invitado.

> **Nota:** quien completa este proceso queda como **Owner** de la entidad. La gestión de la suscripción es exclusiva de ese rol; el resto de la configuración puede delegarse después en un Manager.

---

## Conceptos previos

Tres términos estructuran la plataforma:

- **Entidad**: su empresa. Contiene la configuración global —datos legales, idioma, dirección y zona horaria— que se aplica a toda la organización.
- **Sucursal**: cada unidad operativa (tienda, oficina, obra, proyecto). Hereda la configuración de la entidad, pero puede tener su propia zona horaria, zona de chequeo, horario y festivos.
- **Empleado**: se vincula a una o varias sucursales. En cada vinculación se define su responsabilidad, su puesto y su tarifa. Hereda el calendario de su sucursal, salvo que tenga uno propio.

---

## Paso 1. Crear la cuenta

El registro se hace en el propio backoffice, en `saas.encodebiz.com`.

1. Abra `saas.encodebiz.com` en cualquier navegador.
2. Desde la pantalla de acceso, entre en el formulario de registro.
3. Rellene los campos, **todos obligatorios**:
   - **Nombre completo**
   - **Correo electrónico**
   - **Teléfono**
   - **Contraseña** y su **confirmación**
4. Acepte los términos y la política de privacidad.
5. Envíe el formulario.

No hay paso intermedio de verificación por correo: al completar el registro, el sistema le lleva **directamente a la pantalla de creación de la entidad**.

> **Nota:** use una dirección de correo corporativa. Esa dirección queda vinculada como Owner de la cuenta y es a la que llegan las comunicaciones administrativas. Si el correo ya está en uso, el sistema lo indica con el error `auth/email-already-in-use`.

---

## Paso 2. Crear la entidad

Es la pantalla a la que llega justo después de registrarse. Si ya está dentro del backoffice, se accede desde **Entidad** en el menú lateral.

| Campo | Obligatorio | Descripción |
|---|---|---|
| **Nombre de la empresa** | Sí | Denominación comercial, la que verá su equipo en la plataforma |
| **Idioma principal** | — | Español o inglés. Alemán y portugués están en desarrollo |
| **Razón social** | Sí | Denominación legal, la que aparece en la documentación |
| **Email de facturación** | — | Dirección a la que se envían las facturas; se propone la de registro |
| **NIF / CIF** | — | Identificación fiscal de la entidad |
| **Dirección** | Sí | Domicilio de la empresa. Al seleccionarla se resuelven las coordenadas y la **zona horaria**, que actúa como valor por defecto para las sucursales que no tengan una propia |

Guarde para continuar.

> **Importante:** la razón social y los datos fiscales no son un trámite opcional. **Sin ellos no se puede contratar el plan**: el backoffice bloquea la suscripción hasta que los datos legales y un método de pago estén completos.

---

## Paso 3. Activar CheckBiz

Con la entidad creada, hay que activar el servicio. En el menú lateral, entre en **CheckBiz** y revise los planes disponibles.

Antes de contratar, el sistema comprueba dos requisitos y avisa si falta alguno, enlazando a la pantalla correspondiente:

- **Datos de la empresa** completos.
- **Método de pago** configurado.

Recuerde que la primera suscripción incluye **45 días de prueba**. Consulte [Planes, precios y funcionalidades](../14-referencia/91-planes-y-funcionalidades.md).

---

## Paso 4. Crear la primera sucursal

En el menú lateral, dentro de CheckBiz, entre en **Sucursales** y cree una.

| Campo | Obligatorio | Descripción |
|---|---|---|
| **Nombre** | Sí | Identificador de la unidad operativa: "Tienda Centro", "Oficina Madrid" |
| **Dirección** | Sí | El sistema la geocodifica para obtener las coordenadas y la zona horaria del centro |
| **Zona de chequeo en metros** | Sí | El radio dentro del cual se acepta un fichaje. Entre 50 y 200 metros según el tamaño del centro |
| **NIF** | — | Solo si el centro tiene identificación fiscal propia |
| **Estado** | — | Activa por defecto |

> **Nota:** la zona de chequeo es lo que impide fichar desde fuera del centro. Un radio demasiado amplio la vuelve inútil; uno demasiado estrecho genera rechazos por imprecisión del GPS. Para la mayoría de oficinas y tiendas, **100 metros** es un buen punto de partida, y se ajusta después con los datos de las primeras semanas.

Guarde. Después podrá configurar su horario semanal desde **Calendario**.

---

## Paso 5. Dar de alta al primer empleado

En **Empleados**, cree uno nuevo.

1. Rellene los datos obligatorios: **nombre completo**, **correo electrónico**, **teléfono** y **tipo de relación** (interno o colaborador).
2. Guarde. El sistema crea el perfil y **envía automáticamente el correo de bienvenida** con las instrucciones de activación.
3. Abra la ficha del empleado y **vincúlelo con la sucursal** que acaba de crear. Es en esa vinculación donde se define su **responsabilidad** —worker, supervisor, manager u owner—, su **puesto** y su **tarifa horaria**.

> **Importante:** el nivel de responsabilidad no se elige en el alta, sino en la vinculación con cada sucursal. Una misma persona puede ser worker en un centro y supervisora en otro.

Si el empleado no recibe el correo, revise el apartado correspondiente en [Problemas frecuentes y soluciones](../13-soporte-e-incidencias/88-problemas-frecuentes-y-soluciones.md).

---

## Paso 6. Instalar la app

El empleado necesita la app de CheckBiz360 en su móvil para fichar. Está disponible sin coste para iOS y Android.

Al abrirla por primera vez, iniciará sesión con el correo y la contraseña que definió al activar su cuenta desde el correo de bienvenida.

---

## Estado al finalizar

Al completar estos pasos su organización tiene:

- Una entidad con sus datos legales y su zona horaria.
- El servicio CheckBiz activo.
- Una sucursal operativa con su zona de chequeo.
- Un empleado dado de alta, vinculado a esa sucursal y con acceso a la app.

Desde aquí puede replicar los pasos 4 y 5 para el resto de centros y de personas, o pasar a la guía de inicio rápido para hacer el primer fichaje de prueba.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Guía de inicio rápido](04-guia-inicio-rapido.md) | Del alta al primer fichaje validado |
| [Estructura de la plataforma](05-estructura-de-la-plataforma.md) | Entidad, sucursal y empleado |
| [Crear y gestionar sucursales](../08-sucursales-y-entidad/57-crear-y-gestionar-sucursales.md) | Campos, geocodificación y estados |
| [Crear y gestionar empleados](../02-empleados/06-crear-y-gestionar-empleados.md) | Alta, estados laborales y opciones de seguridad |
| [Planes, precios y funcionalidades](../14-referencia/91-planes-y-funcionalidades.md) | Precio, prueba de 45 días y cómo contratar |

# Configuración de entidad

La entidad es el nivel organizativo superior de CheckBiz360: representa a la empresa que ha contratado el servicio y engloba sucursales, empleados y datos. Lo que se configura aquí actúa como referencia para toda la estructura.

Se accede desde **Entidad** en el menú lateral, y la pantalla está organizada en seis pestañas.

---

## Las seis pestañas

| Pestaña | Qué contiene |
|---|---|
| **Datos de la Empresa** | Nombre comercial, idioma principal, razón social, NIF/CIF, email de facturación y dirección |
| **Entorno de trabajo** | Cómo se llaman las cosas en su organización: por ejemplo, si sus centros se llaman *Sucursal*, *Proyecto* u *Obra* |
| **Configurar Facturación** | Métodos de pago de la cuenta |
| **Suscripciones** | Plan contratado y su estado |
| **Facturas** | Historial de facturación |
| **Colaboradores** | Usuarios con acceso al backoffice de esta entidad |

**Datos de la Empresa** y **Configurar Facturación** muestran un aviso visual mientras estén incompletas. No es decorativo: **sin razón social y sin método de pago no se puede contratar el plan**.

---

## Entorno de trabajo

Antes se llamaba *Identidad visual*. Ya no configura colores ni imágenes: sirve para adaptar el nombre de los centros de trabajo al vocabulario de su organización. Si sus centros son proyectos u obras, el backoffice lo dirá así en el menú, en los listados y en las fichas —por ejemplo, «Detalles de Obra»—. Dejar el campo en blanco usa el nombre por defecto.

En esta misma pestaña está **Conectar con Claude o ChatGPT**: la dirección de conexión de su empresa y los pasos para añadirla a su asistente, de modo que pueda pedirle la semana, las altas y los cambios en sus propias palabras. Se explica en [Su gestor operativo en Claude o ChatGPT](../15-integraciones/109-su-gestor-operativo-en-claude-o-chatgpt.md).

---

## Colaboradores

Los colaboradores son las personas con acceso al backoffice de la entidad, cada una con su rol: **Propietario** o **Administrador**. Se invitan por correo desde la pestaña **Colaboradores**.

- **Invitación.** Mientras la persona no entra, su invitación figura como *Pendiente a aceptar*. Se da por aceptada en cuanto inicia sesión con la entidad asignada; no depende de pulsar nada en la bienvenida.
- **Quién gestiona.** Invitar, cambiar el rol o retirar colaboradores lo hacen propietarios y administradores con acceso **activo**; una invitación sin aceptar o un acceso desactivado no permiten gestionar a nadie.
- **El escalón de propietario.** Solo un propietario puede nombrar a otro propietario o retirarlo.
- **Nunca sin propietario.** No se puede retirar al **único propietario activo** de la entidad: añada antes a otro propietario.

Retirar a un colaborador elimina sus permisos sobre la entidad y no se puede deshacer; para devolverle el acceso hay que invitarle de nuevo.

---

## Datos de la empresa

| Campo | Obligatorio | Para qué sirve |
|---|---|---|
| **Nombre de la empresa** | Sí | Denominación comercial, la que ve su equipo en la plataforma |
| **Idioma principal** | — | Español o inglés. Alemán y portugués están en desarrollo |
| **Razón social** | Sí | Denominación legal. Necesaria para contratar y para la documentación |
| **NIF / CIF** | — | Identificación fiscal de la entidad |
| **Email de facturación** | — | Dirección a la que llegan las facturas |
| **Dirección** | Sí | Domicilio de la empresa, elegido del buscador de direcciones. De ella salen las coordenadas y la **zona horaria**. No hay campo de ciudad aparte: la dirección normalizada ya la incluye |

No existe un campo de "sector de actividad": la plataforma no clasifica la entidad por sector ni ajusta nada en función de él.

---

## Zona horaria

La zona horaria de la entidad se toma de su dirección y actúa como **valor por defecto** para las sucursales que no tengan una propia. Si toda su organización opera en el mismo huso, basta con dejar que las sucursales la hereden.

> **Aviso:** al cambiar la dirección de la entidad, la nueva zona horaria solo afecta a las sucursales que no tengan una configurada. Las que tienen la suya no se ven alteradas.

---

## Seguridad

La verificación en dos pasos se activa **por usuario y por empleado**, no como política global de la entidad: cada ficha de empleado tiene su propia opción de 2FA, y cada usuario puede activarla desde el apartado de seguridad de su cuenta.

> **Estado: No disponible**
> Una política de 2FA obligatoria para toda la entidad, que fuerce a configurarlo a todos los usuarios del backoffice, no está implementada en la versión actual.

Si su organización necesita 2FA generalizado, actívelo empleado a empleado en su ficha. Consulte [Autenticación en dos factores](../02-empleados/09-autenticacion-dos-factores.md).

---

## Facturación y suscripción

Desde **Suscripciones** el Owner consulta el plan contratado y su estado, y desde **Facturas** el historial. Los métodos de pago se gestionan en **Configurar Facturación**.

La facturación del plan Bronce es **por empleado y mes**: no hay un cupo de empleados incluidos que se pueda agotar. Consulte [Planes, precios y funcionalidades](../14-referencia/91-planes-y-funcionalidades.md).

### Almacenamiento

Debajo de los módulos contratados, **Suscripciones** enseña el bloque **Almacenamiento**: lo que ocupa su empresa frente a los 2 GB incluidos, repartido entre documentos, tareas, firmas, informes y fotos del punto de fichaje, y lo que se facturaría este mes por encima de lo incluido.

La casilla **Ampliar almacenamiento por encima de 2 GB** viene marcada. Si la desmarca, no se cobra nada de más, pero al llegar a 2 GB no podrá subir más documentos. Al acercarse al límite, el bloque lo avisa. Ver [Planes, precios y funcionalidades](../14-referencia/91-planes-y-funcionalidades.md#almacenamiento).

---

## Cómo se propaga la configuración a las sucursales

Los valores de la entidad son la referencia que las sucursales heredan o sobrescriben:

1. **Entidad**: define el valor global por defecto.
2. **Sucursal**: si define el suyo, tiene prioridad.
3. **Empleado**: si define el suyo, tiene prioridad sobre el de su sucursal.

Por ejemplo, con la entidad en `Europe/Madrid` y una sucursal en Canarias con `Atlantic/Canary`, esa sucursal usa la suya y el resto hereda Madrid. Lo mismo ocurre con el calendario: horario semanal, pausas y modalidad de jornada bajan en cascada por esos tres niveles.

Los datos fiscales y la facturación no tienen equivalente en la sucursal: son estrictamente globales.

---

## Diferencia entre configuración de entidad y de sucursal

| Aspecto | Entidad | Sucursal |
|---|---|---|
| Alcance | Toda la organización | Un único centro de trabajo |
| Acceso | Owner | Owner y Manager |
| Parámetros exclusivos | Datos fiscales, entorno de trabajo, colaboradores, facturación y suscripción | Zona de chequeo y su radio |
| Herencia | Valor por defecto | Sobrescribe el de la entidad |
| Impacto de un cambio | Toda la organización | Solo ese centro y sus empleados |

La regla es sencilla: lo que afecta a la empresa como conjunto se configura en la entidad; lo que es propio de un centro, en la sucursal.

---

## Cómo acceder

1. Inicie sesión en el backoffice con una cuenta **Owner**.
2. En el menú lateral, seleccione **Entidad**.
3. Sitúese en la pestaña que necesite y modifique los parámetros.
4. Guarde.

> **Aviso:** los cambios en los datos fiscales afectan a la documentación generada a partir de ese momento; no alteran facturas ni informes ya emitidos.

---

> **Nota de rol:** la configuración de entidad, y en particular la suscripción, corresponde al **Owner**. Para delegar la gestión del día a día —sucursales, empleados, tareas y documentos— use el rol **Manager**.

---

## Firma electrónica

En la pestaña **Entorno de trabajo** hay un apartado **Firma electrónica** con el certificado de CheckBiz360 y los pasos para instalarlo en Acrobat Reader, para que los PDF firmados por sus trabajadores se vean en verde. Se explica en [Acuse de recibo y firma electrónica](../05-gestion-documental/35-firma-electronica.md).

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear cuenta y configurar la entidad](../01-primeros-pasos/03-crear-cuenta-y-configurar-entidad.md) | El proceso completo de alta |
| [Crear y gestionar sucursales](./57-crear-y-gestionar-sucursales.md) | Campos, geocodificación y estados |
| [Configuración avanzada de sucursal](./58-configuracion-avanzada-de-sucursal.md) | Zona de chequeo, horario y modalidad de jornada |
| [Herencia de configuración](../04-calendario-y-horarios/26-herencia-de-configuracion.md) | Cómo se resuelve el calendario efectivo |
| [Planes, precios y funcionalidades](../14-referencia/91-planes-y-funcionalidades.md) | Precio, prueba de 15 días y cómo contratar |

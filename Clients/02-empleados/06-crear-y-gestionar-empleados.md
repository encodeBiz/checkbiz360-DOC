# Crear y gestionar empleados

La gestión del equipo humano es el punto de partida de cualquier operación en CheckBiz360. Desde el backoffice, los responsables de la empresa pueden incorporar nuevos empleados, actualizar su información en cualquier momento y controlar su estado laboral a lo largo del tiempo.

Este artículo explica cómo crear un empleado desde cero, qué campos son obligatorios y cuáles opcionales, y cómo gestionar correctamente los diferentes estados que puede atravesar una persona durante su relación laboral con la organización.

---

## Crear un nuevo empleado

### Campos obligatorios

Para dar de alta a un empleado en la plataforma, es necesario completar los siguientes datos:

- **Nombre completo** — Nombre y apellidos tal como deben aparecer en los registros oficiales.
- **Correo electrónico** — Dirección de email única en la plataforma. Será el identificador principal del empleado y la dirección a la que se enviará el acceso inicial.
- **Rol de sistema** — Nivel de acceso asignado al empleado (worker, supervisor, manager u owner). Consulte el artículo *Roles y niveles de responsabilidad* para una descripción detallada de cada nivel.

### Pasos para crear un empleado

1. Acceda al backoffice de CheckBiz360 con sus credenciales de manager u owner.
2. En el menú lateral, seleccione **Empleados** y pulse **Nuevo empleado**.
3. Complete los campos obligatorios: nombre completo, email y rol.
4. Si lo desea, rellene los campos opcionales descritos en la siguiente sección.
5. Pulse **Guardar**. El sistema creará el perfil y enviará automáticamente un email de bienvenida al empleado.

### Email de bienvenida automático

Una vez guardado el perfil, CheckBiz360 envía de forma automática un correo al empleado con las instrucciones para activar su cuenta y acceder a la aplicación móvil. No es necesaria ninguna acción adicional por parte del administrador.

---

## Campos opcionales

Aunque no son obligatorios para crear el perfil, completar estos campos mejora el seguimiento y la trazabilidad del equipo:

- **Teléfono** — Número de contacto directo.
- **DNI / Número de identificación nacional** — Útil para auditorías y exportaciones de datos de RRHH.
- **Puesto de trabajo** — Cargo o función dentro de la organización (por ejemplo, "Técnico de soporte", "Responsable comercial").
- **Idioma preferido** — Configura el idioma de la interfaz para ese empleado.
- **Sucursales asignadas** — Un empleado puede pertenecer a una o varias sucursales. Si se asigna a varias, puede tener roles distintos en cada una de ellas.
- **Tipo de relación** — Indica si el empleado es interno (plantilla) o colaborador externo (freelance o proveedor de servicios).
- **Trabajo remoto habilitado** — Activa la posibilidad de que el empleado fiche desde fuera de las instalaciones.

---

## Estados del empleado

Durante su ciclo de vida en la empresa, un empleado puede encontrarse en distintas situaciones laborales. CheckBiz360 contempla los siguientes estados:

| Estado | Descripción |
|---|---|
| **Activo** | El empleado trabaja con normalidad y tiene acceso a la plataforma. |
| **Inactivo** | El empleado no está operativo temporalmente, pero el perfil se conserva. |
| **Baja** | La relación laboral ha concluido. El empleado no puede acceder a la app. |
| **Vacaciones** | El empleado se encuentra de vacaciones. |
| **Baja por enfermedad** | El empleado está de baja médica. |
| **Excedencia** | El empleado disfruta de una excedencia voluntaria o forzosa. |
| **Baja de paternidad** | El empleado está en permiso de paternidad. |
| **Baja de maternidad** | La empleada está en permiso de maternidad. |

Para cambiar el estado de un empleado, acceda a su perfil en el backoffice, pulse **Editar** y seleccione el nuevo estado en el desplegable correspondiente.

---

## Editar los datos de un empleado

Para modificar cualquier dato del perfil de un empleado:

1. Acceda a **Empleados** en el menú lateral.
2. Localice al empleado mediante el buscador o los filtros disponibles.
3. Pulse sobre su nombre para abrir el perfil.
4. Seleccione **Editar** y realice los cambios necesarios.
5. Pulse **Guardar cambios**.

Los cambios surten efecto de forma inmediata.

---

## Desactivar frente a eliminar un empleado

Estas dos acciones tienen consecuencias muy distintas:

- **Desactivar**: El empleado pierde el acceso a la plataforma, pero todo su historial (fichajes, documentos, tareas, incidencias) se conserva íntegramente. Es la opción recomendada cuando la relación laboral finaliza o cuando se necesita suspender temporalmente el acceso.
- **Eliminar**: Se borra el perfil del empleado de forma permanente. Esta acción es irreversible y puede implicar la pérdida de datos históricos asociados. Solo debe utilizarse en casos excepcionales, como la creación errónea de un perfil duplicado.

> **Nota:** CheckBiz360 recomienda desactivar en lugar de eliminar para mantener la trazabilidad y cumplir con las obligaciones de conservación de registros laborales.

---

## Quién puede realizar estas acciones

Esta funcionalidad está disponible para los roles **manager** (nivel 3) y **owner** (nivel 4). Los supervisores y workers no tienen acceso a la gestión de perfiles de otros empleados.

---

## Artículos relacionados

- [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md)
- [Matriz de permisos por rol](08-matriz-de-permisos-por-rol.md)
- [Autenticación en dos factores](09-autenticacion-dos-factores.md)
- [Exportar empleados a CSV](12-exportar-empleados-csv.md)

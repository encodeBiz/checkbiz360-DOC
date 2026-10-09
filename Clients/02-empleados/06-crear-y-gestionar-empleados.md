# Crear y gestionar empleados

La gestión del equipo humano es el punto de partida de cualquier operación en CheckBiz360. Desde el backoffice, los responsables de la empresa pueden incorporar nuevos empleados, actualizar su información en cualquier momento y controlar su estado laboral a lo largo del tiempo.

Este artículo explica cómo crear un empleado desde cero, qué campos son obligatorios y cuáles opcionales, y cómo gestionar los estados que puede atravesar una persona durante su relación laboral con la organización.

---

## Crear un nuevo empleado

### Campos obligatorios

- **Nombre completo** — Nombre y apellidos tal como deben aparecer en los registros.
- **Correo electrónico** — Dirección única en la plataforma. Es el identificador del empleado y la dirección a la que se envía el acceso inicial. **No puede modificarse una vez creado el perfil.**
- **Teléfono** — Número de contacto, con prefijo internacional.
- **Tipo de relación** — *Plantilla* (personal de la empresa) o *Colaborador* (externo, freelance o proveedor de servicios). Aparece en la ficha junto al estado, y no es un dato menor: los colaboradores **no se incluyen en el informe de registro de jornada**, que es obligatorio para la relación laboral. Ver [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md#tipo-de-relación-interno-frente-a-colaborador).

> **Importante:** el nivel de responsabilidad —worker, supervisor, manager u owner— **no se asigna en el alta**. Se define al vincular al empleado con una sucursal, porque una misma persona puede tener responsabilidades distintas en cada centro. Consulte [Asignar empleados a sucursales](../08-sucursales-y-entidad/60-asignar-empleados-a-sucursales.md).

### Pasos para crear un empleado

1. Acceda al backoffice con credenciales de manager u owner.
2. En el menú lateral, seleccione **Empleados** y pulse el botón de nuevo empleado.
3. Complete los datos personales obligatorios.
4. Ajuste las opciones de seguridad y los datos adicionales que necesite.
5. Configure el calendario del empleado si difiere del de su sucursal.
6. Guarde. El sistema crea el perfil y envía el correo de bienvenida.
7. Vincule al empleado con su sucursal y asígnele allí su responsabilidad y su puesto.

### Email de bienvenida automático

Al guardar el perfil, CheckBiz360 envía automáticamente un correo al empleado con las instrucciones para activar su cuenta y acceder a la app móvil. No requiere ninguna acción adicional del administrador.

---

## Opciones de seguridad y trabajo

Tres opciones se activan o desactivan por empleado:

| Opción | Qué hace |
|---|---|
| **Verificación en dos pasos (2FA)** | Exige un código temporal además de la contraseña |
| **Biometría requerida** | El empleado debe autenticarse con huella o reconocimiento facial antes de que se acepte su fichaje |
| **Trabajo fuera del centro** | Permite fichar fuera de la geocerca de la sucursal (antes se llamaba *Trabajo remoto*). Al activarlo, **la dirección del empleado pasa a ser obligatoria**, porque es la referencia con la que se valida el fichaje. Ver [Trabajo fuera del centro](../03-control-horario/15-fichaje-en-remoto.md) |

---

## Otros campos

- **Documento de identidad** — Útil para auditorías y exportaciones de RRHH.
- **Dirección** — Opcional, salvo que se active el trabajo fuera del centro. Se elige del buscador de direcciones; no hay campo de ciudad aparte, porque la dirección normalizada ya la incluye.
- **Calendario del empleado** — Horario propio y excepciones, cuando difieren de los de su sucursal. Si no se configura, el empleado hereda el calendario de la sucursal.
- **Datos adicionales** — Campos libres en formato clave/valor para información propia de su organización (número de empleado, convenio, centro de coste…).

Al vincular al empleado con una sucursal se definen además su **responsabilidad** en ese centro, su **puesto** y su **tarifa horaria**, esta última es la que alimenta el análisis de costes.

---

## Estados del empleado

CheckBiz360 contempla siete estados laborales, más el estado **Pendiente** para las fichas a medio completar:

| Estado | Descripción |
|---|---|
| **Pendiente** | La ficha existe pero todavía no puede trabajar, normalmente porque le falta el correo electrónico (es habitual en fichas importadas desde una integración). No recibe acceso ni correo de bienvenida, y **no se factura**. Sale de este estado al completar el correo. No se asigna a mano. |
| **Activo** | El empleado trabaja con normalidad y tiene acceso a la plataforma. |
| **Inactivo** | El empleado no está operativo. Es el estado que se usa al finalizar la relación laboral: el perfil y su historial se conservan. |
| **Vacaciones** | El empleado se encuentra de vacaciones. |
| **Baja médica** | El empleado está de baja por enfermedad. |
| **Excedencia** | El empleado disfruta de una excedencia. |
| **Permiso de paternidad** | El empleado está en permiso de paternidad. |
| **Permiso de maternidad** | La empleada está en permiso de maternidad. |

Para cambiar el estado, abra el perfil del empleado, pulse **Editar** y seleccione el nuevo estado. El filtro de estado del listado de empleados incluye **Pendiente**, para localizar las fichas que faltan por completar.

> **Importante:** a efectos de facturación, cuenta todo empleado que no esté pendiente ni eliminado. Un empleado **Inactivo** o de baja sigue formando parte de la plantilla y **sí se factura**.

> **Nota:** los estados de ausencia (vacaciones, bajas, excedencia) también pueden gestionarse como **ausencias con fechas** desde el calendario, lo que permite planificarlas por adelantado en lugar de cambiar el estado a mano el día que empiezan.

---

## Editar los datos de un empleado

1. Acceda a **Empleados** en el menú lateral.
2. Localice al empleado con el buscador o los filtros.
3. Pulse sobre su nombre para abrir el perfil.
4. Seleccione **Editar** y realice los cambios.
5. Guarde.

Los cambios surten efecto de forma inmediata. El correo electrónico es el único dato que no puede modificarse.

---

## Desactivar frente a eliminar un empleado

Estas dos acciones tienen consecuencias muy distintas:

- **Desactivar** (estado *Inactivo*): el empleado pierde el acceso a la plataforma, pero todo su historial —fichajes, documentos, tareas, incidencias— se conserva íntegramente. Es la opción correcta cuando finaliza la relación laboral o cuando hay que suspender el acceso temporalmente.
- **Eliminar**: borra el perfil de forma permanente. Es irreversible. Reserve esta acción para casos excepcionales, como un perfil creado por error o duplicado.

> **Importante:** el registro de jornada debe conservarse cuatro años conforme al RDL 8/2019. Desactivar, y no eliminar, es lo que permite cumplir esa obligación.

---

## Quién puede realizar estas acciones

La gestión de perfiles está disponible para **manager** (nivel 3) y **owner** (nivel 4). Supervisores y workers no tienen acceso a la gestión de perfiles de otros empleados.

---

## Artículos relacionados

- [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md)
- [Matriz de permisos por rol](08-matriz-de-permisos-por-rol.md)
- [Autenticación en dos factores](09-autenticacion-dos-factores.md)
- [Asignar empleados a sucursales](../08-sucursales-y-entidad/60-asignar-empleados-a-sucursales.md)
- [Exportar el listado de empleados](12-exportar-empleados-csv.md)
- [Equipos](99-equipos.md)

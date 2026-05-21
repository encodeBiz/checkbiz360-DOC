# Empleados multi-entidad

CheckBiz360 permite que una misma persona pueda estar vinculada a varias empresas dentro de la plataforma utilizando un único acceso. Este modelo, denominado multi-entidad, es habitual en grupos empresariales, organizaciones con varias razones sociales o proveedores de servicios que trabajan simultáneamente para distintos clientes de la plataforma.

El diseño multi-entidad garantiza que cada empresa mantiene su información completamente aislada de las demás, mientras que el empleado puede cambiar de contexto de trabajo con facilidad desde la misma aplicación.

---

## Cómo funciona el modelo multi-entidad

En CheckBiz360, la identidad de un usuario se basa en su dirección de correo electrónico y su identificador único (UID). Cuando ese email es añadido como empleado en más de una entidad (empresa), el sistema lo reconoce como un único usuario con múltiples contextos de trabajo.

Cada entidad en la que el usuario está dado de alta tiene su propio espacio independiente:

- Horarios y turnos propios.
- Sucursales distintas.
- Documentos, contratos y nóminas separados.
- Tareas e incidencias específicas.
- Roles y niveles de acceso que pueden diferir entre entidades.

Un empleado puede ser worker en una empresa y supervisor en otra, sin que los permisos de una se trasladen a la otra.

---

## Flujo de acceso con múltiples entidades

Cuando un usuario con acceso a varias entidades inicia sesión en CheckBiz360, el proceso es el siguiente:

1. El usuario introduce su email y contraseña en la pantalla de inicio de sesión.
2. Si tiene el 2FA activado, completa la verificación con el código de su aplicación autenticadora.
3. Tras la autenticación, la plataforma detecta que el usuario pertenece a más de una entidad y muestra un **selector de entidad**.
4. El usuario selecciona la empresa con la que desea trabajar en esa sesión.
5. La aplicación carga el contexto completo de la entidad seleccionada: sucursales, horarios, tareas, documentos y configuración propia.

Si el usuario solo pertenece a una entidad, el selector no aparece y el acceso es directo.

---

## Token de sesión específico por entidad

Cada vez que el usuario selecciona una entidad, el sistema genera un token de sesión vinculado exclusivamente a esa empresa. Este diseño garantiza que:

- Las operaciones que el usuario realiza (fichajes, validaciones, visualización de documentos) corresponden únicamente a la entidad activa.
- No es posible acceder accidentalmente a datos de otra empresa sin cambiar explícitamente de contexto.
- Las auditorías de acceso y las trazas de actividad quedan correctamente separadas por entidad.

Para cambiar de entidad durante la misma jornada, el usuario debe cerrar la sesión activa y volver a iniciar sesión, repitiendo el proceso de selección de entidad.

---

## Casos de uso habituales

### Proveedores de servicios externos

Un consultor, técnico de mantenimiento o profesional freelance puede prestar servicios para varios clientes que utilizan CheckBiz360. Cada cliente tiene su propia entidad en la plataforma, y el proveedor aparece como colaborador en cada una de ellas. Desde una sola app, el proveedor puede fichar en la empresa A por la mañana y en la empresa B por la tarde, con registros completamente independientes.

### Grupos empresariales con varias razones sociales

Una corporación puede gestionar varias empresas bajo diferentes denominaciones legales, cada una como una entidad distinta en CheckBiz360. Un director de RRHH corporativo puede estar dado de alta como manager en todas ellas, accediendo al contexto de cada empresa para revisar fichajes, gestionar empleados o generar informes, sin mezclar los datos de las distintas organizaciones.

### Empleados con doble contrato

En algunos casos, un empleado puede tener contratos simultáneos con dos empresas del mismo grupo. El modelo multi-entidad le permite registrar su actividad en cada empresa de forma separada, con registros horarios y documentación independientes para cada relación laboral.

---

## Alta de un empleado en varias entidades

Para que un usuario aparezca en varias entidades, el proceso es independiente en cada empresa:

1. El manager u owner de cada entidad debe crear el perfil del empleado de forma separada en su propia empresa, utilizando el mismo email del usuario.
2. La plataforma vincula automáticamente los perfiles al mismo UID cuando detecta que el email ya existe en el sistema.
3. Cada entidad puede asignar al usuario el rol y las sucursales que considere oportuno, independientemente de lo configurado en otras entidades.

> **Nota:** El hecho de que un usuario esté dado de alta en varias entidades no implica que pueda ver la información de las otras. Cada entidad es un espacio completamente aislado. El usuario solo ve los datos de la entidad en la que tiene la sesión activa en ese momento.

---

## Quién puede gestionar estas configuraciones

La creación y gestión de perfiles de empleados en cada entidad es responsabilidad del **manager** (nivel 3) o el **owner** (nivel 4) de esa entidad concreta. No es posible que el responsable de una empresa gestione empleados en otra empresa aunque compartan usuarios.

---

## Artículos relacionados

- [Crear y gestionar empleados](06-crear-y-gestionar-empleados.md)
- [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md)
- [Autenticación en dos factores](09-autenticacion-dos-factores.md)
- [Biometría y dispositivos de confianza](10-biometria-y-dispositivos-de-confianza.md)

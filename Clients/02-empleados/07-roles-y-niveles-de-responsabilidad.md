# Roles y niveles de responsabilidad

CheckBiz360 estructura el acceso a la plataforma mediante un sistema de cuatro niveles de rol. Cada nivel determina qué puede ver y hacer un usuario dentro del sistema, desde el empleado de base hasta el propietario de la cuenta.

Entender cómo funcionan los roles y cómo se aplican según el ámbito de responsabilidad es fundamental para configurar correctamente la plataforma y garantizar que cada persona accede únicamente a la información que le corresponde.

---

## Los cuatro niveles de rol

### Nivel 1 — Worker (Empleado)

Es el nivel de acceso más básico. El worker puede fichar, consultar su propio historial, solicitar jornadas manuales, ver sus propios documentos y crear incidencias. No tiene visibilidad sobre los datos del resto del equipo ni capacidad para modificar la configuración de la plataforma.

**Casos de uso típicos:** operario de producción, agente de atención al cliente, técnico de campo.

### Nivel 2 — Supervisor

El supervisor tiene acceso ampliado sobre el equipo que tiene asignado. Puede consultar el historial de fichajes de su sucursal, validar y corregir fichajes, y acceder a ciertos documentos del equipo. Algunos de sus permisos son configurables por el manager: la capacidad de crear tareas, validarlas o valorar a los trabajadores puede estar habilitada o no según la configuración de la empresa.

**Casos de uso típicos:** encargado de turno, responsable de equipo en una sucursal, jefe de sección.

### Nivel 3 — Manager (Responsable)

El manager dispone de acceso completo a la gestión operativa: puede crear y gestionar empleados, configurar sucursales, validar cualquier fichaje, gestionar documentos, generar informes y acceder a la inteligencia operativa de la empresa. Es el perfil habitual del director de RRHH o el gerente de área.

**Casos de uso típicos:** director de recursos humanos, gerente de área, responsable de operaciones.

### Nivel 4 — Owner (Propietario)

El owner tiene acceso absoluto a la plataforma, incluyendo la configuración global de la entidad, la gestión de la suscripción y todas las funcionalidades del manager. Solo una o pocas personas en la organización deben tener este nivel.

**Casos de uso típicos:** CEO, socio fundador, director general, administrador de sistemas.

---

## Tipo de relación: interno frente a colaborador

Independientemente del nivel de rol asignado, cada empleado tiene un tipo de relación con la empresa:

- **Interno** — Empleado de plantilla con contrato laboral vigente. Forma parte de la estructura habitual de la organización.
- **Colaborador** — Persona externa que trabaja para la empresa de forma puntual o recurrente sin pertenecer a la plantilla. Puede ser un freelance, un proveedor de servicios o un autónomo.

Ambos tipos pueden tener cualquier nivel de rol, aunque en la práctica los colaboradores suelen operar como workers o supervisores con un alcance limitado.

---

## Ámbito de responsabilidad: entidad frente a sucursal

El rol de un empleado puede aplicarse a dos ámbitos distintos:

### Responsabilidad a nivel de entidad

Cuando se asigna un rol a nivel de entidad, el usuario tiene ese nivel de acceso en toda la empresa, independientemente de cuántas sucursales existan. Un manager a nivel de entidad puede gestionar empleados, fichajes y documentos de todas las sucursales.

### Responsabilidad a nivel de sucursal

Cuando se asigna un rol vinculado a una sucursal concreta, el acceso del usuario queda limitado a esa ubicación. Un supervisor con responsabilidad en la sucursal Madrid solo verá los fichajes y el equipo de esa sucursal, sin acceso a los datos de otras ubicaciones.

---

## Un empleado, varios roles simultáneos

CheckBiz360 permite que un mismo empleado tenga roles distintos en diferentes sucursales. Esta flexibilidad cubre situaciones reales como las siguientes:

- Una persona puede ser **supervisor** en la sucursal de Barcelona (donde lleva el equipo de turno) y **worker** en la sucursal de Madrid (donde colabora puntualmente).
- Un responsable de RRHH puede tener rol de **manager** a nivel de entidad, mientras que en una sucursal específica actúa adicionalmente como supervisor para tareas de gestión directa.

Para configurar este escenario, acceda al perfil del empleado y asigne las responsabilidades correspondientes para cada sucursal.

---

## Asignación de responsabilidades: quién puede asignar qué

No todos los usuarios pueden asignar cualquier rol. Las restricciones son las siguientes:

- Un **owner** puede asignar cualquier nivel de rol a cualquier empleado en cualquier ámbito.
- Un **manager** puede asignar roles hasta el nivel de supervisor a empleados dentro de su ámbito de gestión.
- Un **supervisor** no puede asignar roles.
- Un **worker** no puede asignar roles.

> **Nota:** Se recomienda revisar periódicamente las asignaciones de responsabilidades, especialmente tras cambios organizativos como rotaciones de equipo, promociones o incorporaciones de nuevos responsables.

---

## Quién puede realizar estas acciones

La configuración de roles y responsabilidades está disponible para los roles **manager** (nivel 3) y **owner** (nivel 4).

---

## Artículos relacionados

- [Crear y gestionar empleados](06-crear-y-gestionar-empleados.md)
- [Matriz de permisos por rol](08-matriz-de-permisos-por-rol.md)
- [Empleados multi-entidad](11-empleados-multi-entidad.md)
- [Exportar el listado de empleados](12-exportar-empleados-csv.md)

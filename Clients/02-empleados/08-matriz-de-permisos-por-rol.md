# Matriz de permisos por rol

CheckBiz360 aplica un modelo de control de acceso basado en roles que determina con precisión qué puede hacer cada usuario dentro de la plataforma. Esta matriz es la referencia definitiva para entender qué acciones están disponibles para cada nivel y en qué condiciones.

Consulte esta tabla al configurar nuevos perfiles, resolver dudas sobre accesibilidad a funcionalidades o revisar la política de permisos de su organización.

---

## Tabla de permisos

| Acción | Worker | Supervisor | Manager | Owner |
|---|---|---|---|---|
| Crear fichaje propio | Sí | Sí | Sí | Sí |
| Ver historial propio | Sí | Sí | Sí | Sí |
| Ver historial del equipo | No | Sí (sucursal) | Sí | Sí |
| Solicitar jornada manual | Sí | Sí | Sí | Sí |
| Validar y corregir fichajes | No | Sí (sucursal) | Sí | Sí |
| Crear tareas | No | Configurable | Sí | Sí |
| Validar tareas | No | Configurable | Sí | Sí |
| Valorar trabajadores | No | Configurable | Sí | Sí |
| Subir documentos | No | No | Sí | Sí |
| Ver documentos propios | Sí | Sí | Sí | Sí |
| Ver documentos del equipo | No | Sí (por rol) | Sí | Sí |
| Ver nóminas y contratos | Solo los propios | Solo los propios | Equipo | Todos |
| Crear incidencias | Sí | Sí | Sí | Sí |
| Configurar sucursal | No | No | Sí | Sí |
| Gestionar empleados | No | No | Sí | Sí |
| Ver inteligencia operativa | No | Parcial | Sí | Sí |
| Generar informes | No | No | Sí | Sí |
| Configurar entidad | No | No | No | Sí |

---

## Notas sobre la tabla

### Permisos de supervisor configurables

Algunos permisos del rol **supervisor** están marcados como "Configurable" en la tabla. Esto significa que el comportamiento por defecto puede ser habilitado o deshabilitado por el manager o el owner según las necesidades operativas de la empresa. En concreto:

- **Crear tareas** — Por defecto, los supervisores no pueden crear tareas. El manager puede habilitar esta capacidad para supervisores específicos.
- **Validar tareas** — Igual que la creación: deshabilitado por defecto, activable por el manager.
- **Valorar trabajadores** — Permite al supervisor registrar valoraciones de desempeño sobre los workers de su equipo. Deshabilitado por defecto.

Para modificar estos permisos, acceda al perfil del supervisor en cuestión y ajuste la configuración de permisos avanzados.

### Alcance por sucursal en el rol supervisor

Cuando en la tabla aparece "Sí (sucursal)", significa que el supervisor únicamente puede ejercer esa acción sobre los empleados o datos pertenecientes a la sucursal en la que tiene asignada la responsabilidad de supervisor. No tiene visibilidad ni capacidad de actuación sobre otras sucursales.

### Visualización de documentos del equipo para supervisores

La columna del supervisor indica "Sí (por rol)" para la visualización de documentos del equipo. Esto significa que el supervisor puede ver documentos del personal que tenga asignado bajo su responsabilidad, siempre que esos documentos hayan sido marcados como accesibles para su nivel de rol por parte del manager que los subió.

### Ver nóminas y contratos

Este permiso tiene un comportamiento diferenciado según el rol:

- **Worker y Supervisor** — Solo pueden ver sus propios documentos de nómina y contrato.
- **Manager** — Puede ver los documentos de nómina y contrato de todos los empleados de su equipo o sucursales asignadas.
- **Owner** — Tiene acceso a todos los documentos de nóminas y contratos de la entidad, sin restricción de sucursal ni de equipo.

### Inteligencia operativa para supervisores

El acceso "Parcial" del supervisor a la inteligencia operativa implica que puede consultar métricas y estadísticas básicas del equipo de su sucursal (como horas trabajadas o tasas de asistencia), pero no tiene acceso a los paneles de análisis estratégico, comparativas entre sucursales ni indicadores financieros agregados que sí están disponibles para el manager y el owner.

### Configurar entidad

Esta acción está reservada en exclusiva para el rol **owner**. Incluye la configuración de parámetros globales de la empresa como el nombre de la entidad, la zona horaria, las integraciones con sistemas externos y la gestión de la suscripción.

---

## Consideraciones sobre la seguridad de acceso

La asignación de roles debe revisarse con regularidad, especialmente en los siguientes momentos:

- Cuando un empleado cambia de puesto o de responsabilidades.
- Cuando un supervisor pasa a gestionar una sucursal diferente.
- Cuando un empleado causa baja en la empresa.
- Tras reestructuraciones organizativas o aperturas de nuevas sucursales.

> **Nota:** Asignar un nivel de rol superior al necesario puede comprometer la confidencialidad de la información. Se recomienda aplicar el principio de mínimo privilegio: cada empleado debe tener únicamente el nivel de acceso que necesita para desempeñar sus funciones.

---

## Quién puede consultar esta configuración

La visualización y modificación de los permisos de rol está disponible para los roles **manager** (nivel 3) y **owner** (nivel 4).

---

## Artículos relacionados

- [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md)
- [Crear y gestionar empleados](06-crear-y-gestionar-empleados.md)
- [Gestión documental](../05-gestion-documental/)
- [Inteligencia operativa](../07-inteligencia-operativa/)

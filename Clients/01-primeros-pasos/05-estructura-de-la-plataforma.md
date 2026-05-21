# Estructura de la plataforma

CheckBiz360 organiza la información en tres niveles jerárquicos: entidad, sucursal y empleado. Esta arquitectura permite que una empresa con decenas de centros y cientos de empleados opere desde una única cuenta, con configuraciones diferenciadas por unidad y excepciones individuales donde sea necesario.

Comprender esta estructura es fundamental para configurar correctamente los horarios, los calendarios y las políticas de control. Una configuración bien pensada elimina la necesidad de introducir datos repetidamente y garantiza que cada empleado opere siempre con las reglas correctas.

## Los tres niveles jerárquicos

### Nivel 1: Entidad

La entidad representa a la empresa como organización. Es el nivel más alto de la jerarquía y el contenedor de todo lo demás.

La configuración a nivel de entidad establece los valores por defecto que se aplicarán a todas las sucursales y empleados, salvo que alguno de los niveles inferiores los sobreescriba explícitamente.

Qué se configura a nivel de entidad:

- Datos fiscales y corporativos (nombre, NIF/CIF, dirección).
- Zona horaria por defecto.
- Calendario laboral global (festivos nacionales, días no laborables que afectan a toda la organización).
- Horarios base que pueden ser heredados por las sucursales.
- Políticas de seguridad (2FA obligatorio, tiempo máximo entre fichajes, etc.).
- Configuración de notificaciones globales.

### Nivel 2: Sucursal o proyecto

La sucursal es la unidad operativa. Puede representar una tienda, una oficina, una obra, un departamento o cualquier otra agrupación funcional de empleados.

La sucursal hereda toda la configuración de la entidad, pero puede sobreescribir aquellos elementos que difieran de la configuración global. Esto permite que una empresa con centros en distintas comunidades autónomas tenga calendarios de festivos locales diferentes sin necesidad de crear cuentas separadas.

Qué se puede configurar a nivel de sucursal:

- Nombre, dirección y coordenadas GPS.
- Radio de geocerca (en metros).
- Zona horaria propia, si difiere de la entidad.
- Horario base de la sucursal (puede diferir del horario base de la entidad).
- Calendario de festivos locales.
- Tolerancias de fichaje específicas (margen de tardanza, tiempo mínimo entre entrada y salida, etc.).

> **Nota:** Una sucursal no puede tener configuraciones más permisivas que las restricciones de seguridad definidas a nivel de entidad. Por ejemplo, si la entidad exige 2FA, ninguna sucursal puede desactivarlo para sus empleados.

### Nivel 3: Empleado

El empleado es la unidad mínima de la jerarquía. Se asigna a una o varias sucursales con un rol determinado y recibe el calendario efectivo resultante de combinar la configuración de la entidad y la de su sucursal.

En casos específicos —empleados remotos, trabajadores con horarios irregulares, personal en comisión de servicio— es posible definir excepciones individuales que sobrescriban los valores de la sucursal.

Qué se puede configurar a nivel de empleado:

- Zona horaria propia (para empleados remotos en otra región).
- Excepciones de horario (cambios puntuales o periódicos).
- Coste horario (para el análisis de costes).
- Documentos asociados (contratos, nóminas, certificados).

## La herencia en cascada

El calendario efectivo de un empleado en un día concreto se resuelve siguiendo un orden de prioridad claro:

```
Configuración del empleado  (máxima prioridad)
         |
         v
Configuración de la sucursal
         |
         v
Configuración de la entidad  (prioridad base)
```

En la práctica, esto significa que si la entidad define el horario base como 09:00-17:00, pero la sucursal "Almacén Sur" tiene horario 07:00-15:00, y el empleado Juan García tiene una excepción individual de horario para el turno de tarde (15:00-23:00), el sistema aplicará el horario de Juan García y usará ese como referencia para calcular tardanzas, ausencias y horas extra.

Esta lógica de herencia elimina la necesidad de configurar cada empleado desde cero y garantiza que los cambios a nivel de entidad o sucursal se propaguen automáticamente a todos los empleados afectados.

## Roles del backoffice

Los responsables que administran la plataforma desde el backoffice web operan bajo uno de estos tres roles:

| Rol | Alcance | Capacidades principales |
|---|---|---|
| Owner | Toda la entidad | Configuración completa, facturación, creación de sucursales, gestión de todos los empleados, acceso a todos los informes |
| Manager | Sucursales asignadas | Gestión de empleados y horarios en sus sucursales, acceso a registros e informes de sus centros |
| Supervisor | Sucursales asignadas | Revisión y validación de registros, gestión de incidencias, consulta de informes básicos |

> **Nota:** Un manager puede gestionar varias sucursales simultáneamente. Un empleado puede tener rol de manager en una sucursal y rol de supervisor en otra, si así lo requiere la organización.

## Rol de la app móvil

El rol **Worker** corresponde al empleado que utiliza la app CheckBiz360 para fichar. Este rol no tiene acceso al backoffice web.

Desde la app, el Worker puede:

- Registrar entrada y salida.
- Consultar sus propios registros de asistencia.
- Ver su horario asignado.
- Recibir notificaciones de la plataforma.
- Acceder a sus documentos laborales (si el módulo documental está activo).
- Consultar y gestionar las tareas asignadas (si el módulo de tareas está activo).

## Módulos disponibles por rol

| Módulo | Owner | Manager | Supervisor | Worker (app) |
|---|---|---|---|---|
| Control horario y fichajes | Completo | Por sucursal | Por sucursal | Solo propio |
| Gestión de empleados | Completo | Por sucursal | Consulta | No |
| Configuración de horarios | Completo | Por sucursal | No | No |
| Análisis de costes | Completo | Por sucursal | No | No |
| Inteligencia operativa | Completo | Por sucursal | Resumen | No |
| Gestión documental | Completo | Por sucursal | No | Solo propios |
| Tareas operativas | Completo | Por sucursal | Por equipo | Solo asignadas |
| Informes y exportaciones | Completo | Por sucursal | Básico | No |
| Configuración de entidad | Completo | No | No | No |
| Facturación y suscripción | Completo | No | No | No |

> **Nota:** Los módulos disponibles en su cuenta dependen del plan de suscripción contratado. Consulte la sección de planes en encodebiz.com para ver el detalle de cada nivel.

## Artículos relacionados

- [Qué es CheckBiz360](01-que-es-checkbiz360.md)
- [Crear cuenta y configurar la entidad](03-crear-cuenta-y-configurar-entidad.md)
- [Gestión de sucursales y geocercas](../08-sucursales-y-entidad/)
- [Roles y permisos de empleados](../02-empleados/)
- [Configuración de horarios y calendarios](../04-calendario-y-horarios/)

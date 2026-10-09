# Asignar empleados a sucursales

La asignación de un empleado a una sucursal es el mecanismo por el que CheckBiz360 vincula a una persona con un centro de trabajo concreto. Esta vinculación determina desde qué sucursal puede fichar el empleado, qué horarios se aplican, qué responsables supervisan sus registros y qué geocerca se usa para validar su ubicación. Este artículo explica cómo realizar esta asignación, cómo gestionar empleados que trabajan en varias sucursales y qué impacto tiene la asignación en el sistema.

## Conceptos previos: responsabilidades y asignación a sucursal

Cada empleado en CheckBiz360 tiene asociadas una o varias **responsabilidades**. Cada responsabilidad define el contexto en el que ese empleado opera: la asignación a sucursal, el rol que tiene en ella y, opcionalmente, el proyecto o área funcional.

La asignación a sucursal es el vínculo que une a un empleado con una sucursal. Cuando el empleado ficha desde la app, el sistema identifica a qué sucursal pertenece ese fichaje a partir de esta asignación. Si un empleado no tiene ninguna responsabilidad con sucursal asignada, no podrá fichar.

## Asignar un empleado a una sucursal

### Desde la ficha del empleado

1. Acceda al backoffice web y navegue a **Empleados** en el menú lateral.
2. Localice al empleado que desea asignar y pulse sobre su nombre para abrir su ficha.
3. Desplácese hasta la sección **Responsabilidades** o **Asignaciones**.
4. Pulse **Añadir responsabilidad**.
5. Seleccione la sucursal en el desplegable **Sucursal**. El listado muestra únicamente las sucursales activas de su entidad.
6. Asigne el rol que tendrá el empleado en esa sucursal: **Worker**, **Supervisor** o **Manager**.
7. Si procede, seleccione el calendario efectivo que se aplicará a este empleado en esa sucursal.
8. Pulse **Guardar**. La asignación se aplica de inmediato.

### Desde la gestión de la sucursal

También puede asignar empleados directamente desde la ficha de la sucursal:

1. Navegue a **Sucursales** y abra la sucursal deseada.
2. Acceda a la pestaña **Empleados** dentro de la ficha de la sucursal.
3. Pulse **Asignar empleado** e introduzca el nombre o el correo electrónico del empleado en el buscador.
4. Seleccione el rol y el calendario y pulse **Confirmar**.

### Dar de alta a un equipo entero

Si la misma cuadrilla trabaja en varios proyectos, no hace falta vincular a cada persona por separado. En la lista de empleados de la ficha de la sucursal, **Aplicar equipo** da de alta de una vez a todos los miembros de un equipo, cada uno con su responsabilidad, su puesto y su precio, y salta a quien ya estaba. **Guardar como equipo** hace lo contrario: convierte la plantilla de la sucursal en un equipo reutilizable. Consulte [Equipos](../02-empleados/99-equipos.md).

## Multi-sucursal: un empleado en varias sucursales

CheckBiz360 admite que un mismo empleado esté asignado a varias sucursales simultáneamente, con roles distintos en cada una. Esta funcionalidad está diseñada para cubrir casos como:

- Un empleado que trabaja en dos tiendas de forma alternada.
- Un responsable que actúa como Supervisor en su sucursal habitual y como Manager en una sucursal de menor tamaño.
- Equipos de campo que se desplazan entre instalaciones según la planificación semanal.

### Cómo funciona el multi-sucursal

Cuando un empleado con múltiples responsabilidades ficha desde la app, el sistema determina automáticamente en qué sucursal está fichando comparando la ubicación GPS del dispositivo con las coordenadas y radios de cada sucursal asignada. Si el empleado está dentro del radio de la sucursal A, el fichaje se registra en la sucursal A; si está en el radio de la sucursal B, se registra en la sucursal B.

En caso de que el empleado esté fuera del radio de todas sus sucursales asignadas y la geocerca no esté desactivada, el fichaje será rechazado con el código `checklog/out_of_radius`.

> **Aviso:** Si los radios de dos sucursales se solapan geográficamente, puede haber ambigüedad en la asignación del fichaje. En esos casos, el sistema prioriza la sucursal cuyo centro esté más próximo a la posición real del empleado. Revise los radios configurados si detecta asignaciones incorrectas de forma recurrente.

### Roles distintos por sucursal

Cada responsabilidad es independiente. Un mismo empleado puede ser Worker en una sucursal y Supervisor en otra. Los permisos que se aplican en cada contexto son los del rol de esa responsabilidad concreta, no del rol más elevado del empleado.

## Impacto de la asignación en el calendario efectivo

Al asignar un empleado a una sucursal, el sistema vincula esa asignación con el calendario efectivo seleccionado. El calendario define los días laborables, los festivos propios de esa sucursal y los turnos de trabajo. Este vínculo tiene las siguientes implicaciones:

- Los fichajes del empleado se comparan con los turnos del calendario para detectar anomalías (llegadas tardías, ausencias, salidas anticipadas).
- El cómputo de horas trabajadas se calcula en relación con los turnos previstos en ese calendario.
- Las notificaciones de ausencia o jornada incompleta se generan en función de los turnos del calendario de esa sucursal.

Si un empleado trabaja en dos sucursales con calendarios distintos, cada fichaje se valida contra el calendario de la sucursal en la que se produce.

## Impacto de la asignación en los fichajes

Una vez que el empleado tiene una o más responsabilidades activas, la app mostrará automáticamente el botón de fichaje y la información de la sucursal correspondiente. El empleado no necesita seleccionar manualmente su sucursal en la app; el sistema la detecta por GPS.

Si el empleado no tiene ninguna asignación activa o su única sucursal asignada está inactiva, la app mostrará un mensaje de error y no le permitirá fichar.

## Eliminar o modificar una asignación

Para desvincular un empleado de una sucursal:

1. Abra la ficha del empleado en **Empleados**.
2. Localice la responsabilidad que desea eliminar en la sección **Responsabilidades**.
3. Pulse el icono de eliminación junto a la responsabilidad correspondiente.
4. Confirme la operación. El empleado dejará de poder fichar en esa sucursal a partir de ese momento. El histórico de fichajes anteriores en esa sucursal se conserva intacto.

---

> **Nota de rol:** La asignación de empleados a sucursales está disponible para los roles **Owner** y **Manager**. El rol **Supervisor** puede visualizar las asignaciones de los empleados de su equipo, pero no puede crearlas ni modificarlas.

## Artículos relacionados

- [Crear y gestionar sucursales](57-crear-y-gestionar-sucursales.md)
- [Equipos](../02-empleados/99-equipos.md)
- [Estados de una sucursal](59-estados-de-una-sucursal.md)
- [Configuración de entidad](61-configuracion-de-entidad.md)
- [Vista global multi-sucursal](62-vista-global-multi-sucursal.md)

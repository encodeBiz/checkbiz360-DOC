# Calendario laboral en CheckBiz360

El calendario laboral es el registro de días no laborables que el sistema consulta en cada fichaje para determinar si ese día está habilitado para trabajar. En CheckBiz360, este calendario puede configurarse a distintos niveles jerárquicos, lo que permite que una misma organización gestione festivos nacionales comunes junto con festivos locales específicos de cada sucursal.

---

## Qué es el calendario laboral

El calendario laboral en CheckBiz360 es una lista de fechas que el sistema marca como no laborables. Cuando un empleado intenta fichar en una de esas fechas, el sistema lo detecta y devuelve el código `checklog/day_disabled`, rechazando el fichaje.

Este mecanismo protege la integridad de los registros de asistencia y evita que se generen jornadas en días en los que la empresa, por normativa o por política interna, no opera.

---

## Tipos de día no laborable

CheckBiz360 permite clasificar cada entrada del calendario en función de su alcance:

- **Festivo nacional:** Aplica a toda la entidad y, por herencia, a todas sus sucursales y empleados.
- **Festivo autonómico o local:** Se configura a nivel de sucursal. Solo afecta a los empleados de esa sucursal concreta.
- **Día no laborable interno:** Puede ser cualquier fecha que la empresa decida marcar como no laborable por motivos propios (cierre por inventario, puente de empresa, etc.).

Cada tipo tiene un alcance diferente dentro de la jerarquía de configuración, lo que se detalla en la siguiente sección.

---

## Jerarquía entity → branch → employee

El calendario laboral sigue la misma jerarquía de tres niveles que el resto de la configuración en CheckBiz360: entidad, sucursal y empleado.

### Nivel entidad

Los festivos configurados en la entidad aplican por defecto a todos los empleados de la organización, independientemente de la sucursal a la que pertenezcan. Este es el nivel adecuado para gestionar festivos nacionales o cierres corporativos.

### Nivel sucursal

Cada sucursal puede tener su propio calendario de días no laborables adicionales. Estos días se suman a los festivos heredados de la entidad. Un festivo configurado en una sucursal no afecta al resto de sucursales.

### Nivel empleado

Un empleado concreto puede tener excepciones individuales que marquen días específicos como no laborables (o, por el contrario, como laborables si la sucursal los tiene marcados como festivos). Las excepciones individuales tienen la mayor prioridad en la jerarquía.

> **Nota:** La resolución jerárquica sigue la regla de que la configuración más cercana al empleado prevalece sobre la más general. Si una fecha es festivo en la entidad pero el empleado tiene una excepción individual que la marca como laborable, el empleado podrá fichar ese día.

---

## Cómo añadir un festivo

Para añadir un festivo al calendario laboral, siga estos pasos:

**A nivel entidad:**

1. Acceda al backoffice con rol owner.
2. Navegue a **Calendario** y sitúese en la pestaña **Configuración general**.
3. Pulse el botón **Añadir día no laborable**.
4. Seleccione la fecha en el selector de calendario.
5. Indique el tipo (festivo nacional, puente, cierre interno, etc.) y, opcionalmente, añada una descripción.
6. Guarde el registro.

**A nivel sucursal:**

1. Acceda al backoffice con rol owner o manager.
2. Navegue a **Sucursales** y seleccione la sucursal correspondiente.
3. Acceda a **Calendario** y sitúese en la pestaña **Sucursal**.
4. Siga los pasos 3 a 6 del procedimiento anterior.

Los cambios son efectivos de forma inmediata. Una vez guardado el festivo, cualquier intento de fichaje en esa fecha por parte de los empleados afectados será bloqueado.

---

## Impacto en los fichajes

Cuando un empleado intenta registrar su entrada o salida en una fecha marcada como no laborable en su calendario efectivo, el sistema devuelve el código de error `checklog/day_disabled`.

Este error queda registrado en el historial del empleado con su timestamp y los datos del intento. No se genera ninguna jornada ni se computan horas.

| Situación | Resultado |
|---|---|
| Fichaje en día laborable activo | Proceso de validación normal. |
| Fichaje en festivo de entidad | `checklog/day_disabled`. Fichaje rechazado. |
| Fichaje en festivo de sucursal | `checklog/day_disabled`. Fichaje rechazado. |
| Fichaje en día desactivado en el horario base | `checklog/day_disabled`. Fichaje rechazado. |

> **Aviso:** Si su empresa trabaja habitualmente en festivos (por ejemplo, sectores de retail u hostelería), debe revisar la configuración del calendario para no bloquear fichajes válidos. Consulte el artículo [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md) para conocer cómo gestionar este caso.

---

## Consultar el calendario de un empleado

Desde el backoffice, el responsable puede consultar qué días están marcados como no laborables para un empleado concreto:

1. Acceda a **Empleados** y seleccione el empleado.
2. Abra la sección **Calendario efectivo**.
3. El sistema muestra el calendario mensual con los días laborables, festivos heredados de la entidad y sucursal, y las excepciones individuales del empleado.

Esta vista es especialmente útil para depurar situaciones en las que un empleado reporta que no pudo fichar en una fecha determinada.

---

## Artículos relacionados

- [Horarios base y turnos](23-horarios-base-y-turnos.md)
- [Excepciones de horario](25-excepciones-de-horario.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md)
- [Estados y códigos de error](../03-control-horario/22-estados-y-codigos-de-error.md)

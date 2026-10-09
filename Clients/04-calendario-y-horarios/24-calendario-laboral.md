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

Un empleado concreto puede tener sus propios días no laborables: vacaciones, permisos o cualquier ausencia. Se suman a los festivos de la entidad y de su sucursal y solo le afectan a él.

> **Importante:** los festivos **se suman** entre niveles; no se anulan. Un festivo de la entidad o de la sucursal se aplica a todos sus empleados aunque alguno tenga un horario personalizado con turno ese día: el fichaje se rechaza igualmente con `checklog/day_disabled`. La herencia en la que manda el nivel más cercano al empleado es la del **horario semanal**, no la de los festivos. Si en su organización solo una parte de la plantilla trabaja un festivo, consulte [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md#qué-ocurre-si-la-empresa-trabaja-en-festivo).

Cada día no laborable indica de qué nivel viene —entidad, sucursal o empleado—, de modo que en la ficha del empleado se distingue lo que cierra la empresa de lo que es una ausencia propia.

---

## Cómo añadir un festivo

Para añadir un festivo al calendario laboral, siga estos pasos:

**A nivel entidad:**

1. Acceda al backoffice con rol owner.
2. Abra **Horarios** en el menú lateral y sitúese en la pestaña **Configuración general**.
3. En **Festivos de la entidad**, pulse **Añadir festivo**.
4. Escriba el nombre del festivo y seleccione la fecha; si lo desea, añada una descripción.
5. Pulse **Guardar festivo**.

**A nivel sucursal:**

1. Acceda al backoffice con rol owner o manager.
2. Abra la ficha de la sucursal correspondiente.
3. En el bloque de **días libres** de la sucursal, añada el festivo con los mismos datos.

**A nivel empleado:** las ausencias de una persona se registran desde su ficha o directamente desde el [tablero de disponibilidad](98-tablero-de-disponibilidad.md). La pestaña **No laborables de empleados** de **Horarios** permite buscar a un empleado y consultar sus días no laborables con su origen. Una ausencia puede cubrir un **rango de fechas** y llevar la marca **Retribuida**; se explica en [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md#ausencias-de-un-empleado).

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
| Fichaje en un día no laborable propio del empleado (vacaciones, permiso) | `checklog/day_disabled`. Fichaje rechazado. |
| Fichaje con una ausencia registrada que cubre ese día | `checklog/absence`. Fichaje rechazado. |

Desde la versión 1.3.2, la app no se limita a mostrar el código: explica en un diálogo que ese día no es laborable y que, si el empleado trabajó, puede [solicitar una jornada manual](../03-control-horario/19-solicitar-jornada-manual.md). En la tarjeta del día distingue además un **festivo** de un **día libre**.

> **Aviso:** Si su empresa trabaja habitualmente en festivos (por ejemplo, sectores de retail u hostelería), debe revisar la configuración del calendario para no bloquear fichajes válidos. Consulte el artículo [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md) para conocer cómo gestionar este caso.

---

## Consultar el calendario de un empleado

Desde el backoffice, el responsable puede consultar qué días están marcados como no laborables para un empleado concreto:

1. Acceda a **Empleados** y abra la ficha del empleado.
2. Abra la pestaña de horarios.
3. Junto a su horario, la ficha muestra sus días no laborables separados por origen: **Heredados de la entidad**, **heredados de su sucursal** y **propias del empleado**. Las ausencias de varios días seguidos aparecen agrupadas en una sola fila con su rango.

Esta vista es especialmente útil para depurar situaciones en las que un empleado reporta que no pudo fichar en una fecha determinada. Para ver de un vistazo quién está disponible cada día en toda una sucursal, use el [tablero de disponibilidad](98-tablero-de-disponibilidad.md).

---

## Artículos relacionados

- [Horarios base y turnos](23-horarios-base-y-turnos.md)
- [Excepciones de horario](25-excepciones-de-horario.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md)
- [Tablero de disponibilidad](98-tablero-de-disponibilidad.md)
- [Estados y códigos de error](../03-control-horario/22-estados-y-codigos-de-error.md)

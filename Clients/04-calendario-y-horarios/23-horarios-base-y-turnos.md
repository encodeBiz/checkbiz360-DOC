# Horarios base y turnos en CheckBiz360

El horario base define cuándo se espera que un empleado esté presente en su puesto de trabajo. En CheckBiz360, este horario no se configura empleado por empleado de forma individual, sino que se define a nivel de entidad o de sucursal y se hereda de forma automática. Este artículo explica qué es un horario base, cómo se configura y cómo el sistema selecciona el turno activo en el momento de cada fichaje.

---

## Qué es un horario base

El horario base es el conjunto de turnos que forman la jornada laboral estándar de un grupo de empleados. Se define en la entidad o en cada sucursal y especifica, para cada día de la semana, qué turnos están activos y en qué franja horaria se encuadran.

Cuando un empleado ficha, el sistema consulta su calendario efectivo y localiza el turno correspondiente a ese momento. Si el fichaje cae dentro de la franja de un turno activo (considerando la tolerancia de entrada configurada), el registro se acepta como válido.

---

## Tipos de turno

### Turno único diario

Es el tipo de turno más habitual. El empleado tiene una sola franja horaria continua al día: una hora de entrada y una hora de salida.

La franja se define mediante cuatro parámetros:

- `start.hour` y `start.minute`: hora y minuto de inicio del turno.
- `end.hour` y `end.minute`: hora y minuto de fin del turno.

Por ejemplo, un turno de mañana estándar podría configurarse con `start.hour: 9`, `start.minute: 0`, `end.hour: 17`, `end.minute: 0`.

### Múltiples turnos por día

Algunas empresas estructuran la jornada en dos bloques: mañana y tarde. En estos casos es posible definir dos turnos para el mismo día, cada uno con su propia franja horaria.

Un ejemplo típico sería el turno de mañana de 09:00 a 14:00 y el turno de tarde de 16:00 a 20:00. El empleado realiza dos fichajes de entrada y dos fichajes de salida, uno por cada bloque.

El sistema evalúa el fichaje contra el turno cuya franja horaria corresponde al momento del registro. Si el empleado ficha a las 09:05, el sistema lo vincula al turno de mañana. Si ficha a las 16:00, lo vincula al turno de tarde.

---

## Cómo el sistema selecciona el turno activo

En el momento del fichaje, el sistema recorre los turnos activos del día y determina cuál está vigente en ese instante. La selección se basa en la comparación entre la hora del fichaje y las franjas horarias de los turnos definidos para ese día.

Si hay varios turnos en el día, el sistema selecciona aquel cuya ventana de tiempo incluye el momento del fichaje. Si el fichaje cae entre dos turnos (por ejemplo, durante una pausa entre el bloque de mañana y el de tarde), el sistema puede rechazarlo con el código `checklog/out_of_schedule` si no existe una tolerancia que cubra ese intervalo.

> **Nota:** La tolerancia de entrada amplía la ventana de aceptación antes del inicio del turno, pero no extiende el cierre del turno anterior. Este ajuste se explica en detalle en el artículo sobre horario flexible.

---

## Semana laboral: días laborables y días desactivados

El horario base no solo define las franjas horarias, sino también qué días de la semana son laborables para ese empleado o sucursal.

Para cada día de la semana es posible indicar si está activo o desactivado. Un día desactivado equivale a un día no laborable: si un empleado intenta fichar en un día marcado como desactivado, el sistema devuelve el código `checklog/day_disabled`.

### Configurar los días de la semana

La configuración de días laborables se realiza desde el backoffice, en la sección de horarios de la entidad o la sucursal:

1. Acceda al backoffice con un rol con permisos de edición (owner o manager).
2. Navegue a la sección **Configuración** de la entidad o sucursal correspondiente.
3. Acceda al apartado **Horarios**.
4. Para cada día de la semana, marque si el día está activo o desactivado.
5. Guarde los cambios.

Los cambios en los días laborables tienen efecto inmediato sobre el calendario efectivo de todos los empleados que hereden ese horario.

> **Aviso importante:** Desactivar un día laborable afecta a todos los empleados que hereden el horario de esa entidad o sucursal. Si necesita desactivar un día solo para un empleado concreto, utilice las excepciones individuales de horario descritas en el artículo [Excepciones de horario](25-excepciones-de-horario.md).

---

## Configuración del horario base en la entidad y en la sucursal

El horario base puede configurarse a dos niveles:

- **Nivel entidad:** Define el horario general que aplica a toda la organización. Es el punto de partida de la jerarquía.
- **Nivel sucursal:** Permite que cada sucursal tenga un horario diferente al de la entidad. Si una sucursal tiene su propio horario configurado, los empleados de esa sucursal heredan el horario de la sucursal en lugar del de la entidad.

Esta arquitectura es especialmente útil en empresas con múltiples centros que operan en diferentes franjas horarias o con distintos días laborables.

---

## Artículos relacionados

- [Calendario laboral](24-calendario-laboral.md)
- [Excepciones de horario](25-excepciones-de-horario.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Turnos rotativos](27-turnos-rotativos.md)
- [Horario flexible](28-horario-flexible.md)
- [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md)

# Horarios base y turnos en CheckBiz360

El horario base define cuándo se espera que un empleado esté presente en su puesto de trabajo. En CheckBiz360, este horario no se configura empleado por empleado de forma individual, sino que se define a nivel de entidad o de sucursal y se hereda de forma automática. Este artículo explica qué es un horario base, cómo se configura y cómo el sistema selecciona el turno activo en el momento de cada fichaje.

---

> **Tres formas de organizar el horario.** En **Horarios y festivos**, el apartado **Cómo se organiza el horario** elige entre **Horario semanal**, la semana tipo que describe este artículo; **Horario por tareas**, donde cada tarea del día es un turno; y **Calendario**, donde los turnos se cargan fecha a fecha. Si cada semana es distinta, consulte [Calendario: turnos cargados por fecha](114-calendario-de-turnos-por-fecha.md).

## Qué es un horario base

El horario base es el conjunto de turnos que forman la jornada laboral estándar de un grupo de empleados. Se define en la entidad o en cada sucursal y especifica, para cada día de la semana, qué turnos están activos y en qué franja horaria se encuadran.

Cuando un empleado ficha, el sistema consulta su calendario efectivo y localiza el turno correspondiente a ese momento. Si el fichaje cae dentro de la franja de un turno activo (según el horario y la modalidad de jornada configurada), el registro se acepta como válido.

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

La salida sigue la misma regla: se atribuye al turno que contiene la hora de salida y, si ya han terminado todos, al último que empezó, que es el que se está cerrando tarde. Con jornada estricta, una salida a las 20:10 en un día de 09:00–14:00 y 16:00–20:00 se ajusta al fin del turno de tarde, no al de mañana.

---

## Cómo el sistema selecciona el turno activo

En el momento del fichaje, el sistema recorre los turnos activos del día y determina cuál está vigente en ese instante. La selección se basa en la comparación entre la hora del fichaje y las franjas horarias de los turnos definidos para ese día.

Si hay varios turnos en el día, el sistema selecciona aquel cuya ventana de tiempo incluye el momento del fichaje. Si el fichaje cae entre dos turnos —por ejemplo, durante la pausa entre el bloque de mañana y el de tarde— el sistema lo rechaza con el código `checklog/out_of_schedule`.

> **Nota:** que el tiempo trabajado fuera de la franja cuente o no depende de la modalidad de jornada —estricta o flexible— configurada en el calendario. Se explica en detalle en [Jornada estricta y jornada flexible](28-horario-flexible.md).

---

## Semana laboral: días laborables y días desactivados

El horario base no solo define las franjas horarias, sino también qué días de la semana son laborables para ese empleado o sucursal.

Para cada día de la semana es posible indicar si está activo o desactivado. Un día desactivado equivale a un día no laborable: si un empleado intenta fichar en un día marcado como desactivado, el sistema devuelve el código `checklog/day_disabled`.

### Configurar los días de la semana

La configuración de días laborables se realiza desde el backoffice:

1. Acceda al backoffice con un rol con permisos de edición (owner o manager).
2. Para el horario de la entidad, abra **Horarios** en el menú lateral y la pestaña **Configuración general**. Para una sucursal o un empleado, abra su ficha: el horario se hereda mientras esté activado **Usar horario base**, y al desactivarlo puede definir un **horario personalizado**.
3. En el **Horario semanal**, active o desactive cada día. Un día apagado muestra «No hay turnos definidos».
4. Añada los turnos de los días activos.
5. Pulse **Guardar calendario**. Se pide confirmación, y en ese mismo paso puede guardar el horario también como plantilla (ver [Plantillas de horario](#plantillas-de-horario)).

Los cambios en los días laborables tienen efecto inmediato sobre el calendario efectivo de todos los empleados que hereden ese horario.

### Si todavía no hay ningún horario

El registro de jornada es una obligación legal y no puede fallar porque aún no se haya configurado el horario. Por eso, **mientras no exista ningún horario en ningún nivel** —ni en la entidad, ni en la sucursal, ni en el empleado, o no haya un solo turno en toda la semana—, el fichaje se acepta con una franja abierta de 00:00 a 23:59.

Es solo una red de seguridad para los primeros días: sin horario no se puede saber si alguien llegó tarde o hizo horas de más. La guía inicial del backoffice pide configurarlo antes que nada.

En cuanto hay un horario definido, manda ese horario: una semana configurada con todos los días apagados **cierra** esos días y el fichaje se rechaza con `checklog/day_disabled`.

> **Aviso importante:** Desactivar un día laborable afecta a todos los empleados que hereden el horario de esa entidad o sucursal. Si necesita desactivar un día solo para un empleado concreto, utilice las excepciones individuales de horario descritas en el artículo [Excepciones de horario](25-excepciones-de-horario.md).

---

## Configuración del horario base en la entidad y en la sucursal

El horario base puede configurarse a dos niveles:

- **Nivel entidad:** Define el horario general que aplica a toda la organización. Es el punto de partida de la jerarquía.
- **Nivel sucursal:** Permite que cada sucursal tenga un horario diferente al de la entidad. Si una sucursal tiene su propio horario configurado, los empleados de esa sucursal heredan el horario de la sucursal en lugar del de la entidad.

Esta arquitectura es especialmente útil en empresas con múltiples centros que operan en diferentes franjas horarias o con distintos días laborables.

También puede configurarse a **nivel de empleado**, para quienes tengan un horario propio distinto al de su sucursal.

---

## Pausas dentro del turno

Además de los turnos, cada día admite **pausas** con su hora de inicio y de fin. Se configuran en el mismo horario semanal, bajo el día correspondiente, y pueden añadirse varias.

Cómo se computen esas pausas —con la duración fija configurada o con el tiempo real que marque el empleado— depende de la modalidad de descanso elegida. Consulte [Jornada estricta y jornada flexible](28-horario-flexible.md).

---

## Plantillas de horario

Configurar el horario semanal centro a centro es repetitivo cuando varias sucursales comparten el mismo patrón. Para evitarlo, un horario puede **guardarse como plantilla** y aplicarse después donde haga falta.

- **Guardar una plantilla.** En la configuración general, pulse **Guardar calendario**; en la confirmación, marque **Guardar como plantilla** y dele un nombre. En la ficha de una sucursal o de un empleado, use el botón **Guardar como plantilla**.
- **Aplicar una plantilla.** En **Selecciona una plantilla**, elija la que quiera: al elegirla se vuelca sobre el horario que está editando. Revise el resultado y guarde.
- Las plantillas que dejen de usarse pueden eliminarse.

La plantilla es una copia del **horario ya guardado**, no de lo que haya en pantalla. Por eso, al dar de alta una sucursal o un empleado, **Guardar como plantilla** está deshabilitado hasta que el registro existe: guarde primero y cree la plantilla después.

Es la vía práctica para dar de alta una sucursal nueva con el horario de las demás sin rehacerlo día por día.

---

## Artículos relacionados

- [Calendario laboral](24-calendario-laboral.md)
- [Excepciones de horario](25-excepciones-de-horario.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Turnos rotativos](27-turnos-rotativos.md) — no disponible en la versión actual; alternativas
- [Jornada estricta y jornada flexible](28-horario-flexible.md)
- [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md)
- [Tablero de disponibilidad](98-tablero-de-disponibilidad.md)
- [Calendario: turnos cargados por fecha](114-calendario-de-turnos-por-fecha.md)

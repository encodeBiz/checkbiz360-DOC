# Herencia de configuración: cómo se resuelve el calendario efectivo

Cuando un empleado ficha, el sistema necesita determinar qué horario debe aplicar en ese momento concreto. Esta determinación no se hace consultando un único valor: el sistema recorre una cadena jerárquica de configuraciones y aplica la regla que tenga mayor proximidad al empleado. Este mecanismo se denomina herencia de configuración o cascada de horarios.

---

## Los tres niveles de la jerarquía

CheckBiz360 organiza la configuración de horarios en tres niveles:

1. **Entidad:** El nivel más general. Define los parámetros que aplican a toda la organización.
2. **Sucursal:** El nivel intermedio. Una sucursal puede tener su propia configuración que reemplaza parcialmente o por completo la de la entidad.
3. **Empleado:** El nivel más específico. Las excepciones individuales de un empleado tienen prioridad absoluta sobre cualquier configuración de nivel superior.

La regla fundamental es que la configuración más cercana al empleado siempre gana.

---

## Algoritmo de resolución en cascada

Cuando el sistema necesita conocer el horario efectivo de un empleado para una fecha y hora concretas, ejecuta el siguiente proceso:

1. Consulta si el empleado tiene una excepción individual activa para ese día (excepción puntual) o para ese día de la semana (excepción periódica).
2. Si existe una excepción individual, la utiliza como horario efectivo y detiene la búsqueda. No consulta los niveles superiores.
3. Si no existe excepción individual, consulta si la sucursal del empleado tiene un horario propio configurado.
4. Si la sucursal tiene horario propio, lo utiliza como horario efectivo y detiene la búsqueda.
5. Si la sucursal no tiene horario propio, consulta el horario de la entidad y lo utiliza.

Este proceso garantiza que siempre existe un horario efectivo válido, incluso si los niveles intermedios no tienen configuración propia.

---

## Ejemplo concreto con tres niveles distintos

Suponga la siguiente configuración en una empresa con una entidad principal y una sucursal en una ciudad diferente:

| Nivel | Día | Inicio | Fin |
|---|---|---|---|
| Entidad | Lunes a viernes | 09:00 | 17:00 |
| Sucursal Madrid | Lunes a viernes | 08:30 | 16:30 |
| Empleado García | Lunes a viernes | 07:00 | 15:00 (excepción periódica) |

El empleado García trabaja en la sucursal Madrid. Su horario efectivo no es el de la entidad (09:00–17:00) ni el de la sucursal (08:30–16:30), sino su excepción individual (07:00–15:00). Si García ficha a las 07:05, el sistema lo acepta porque cae dentro de su turno efectivo.

Un empleado de la sucursal Madrid sin excepción individual fichará con el horario de la sucursal (08:30–16:30). Un empleado de una sucursal sin configuración propia heredará directamente el horario de la entidad (09:00–17:00).

---

## Qué configuraciones se heredan y cuáles no

La herencia no funciona igual para todos los parámetros. En términos generales:

- El **calendario de festivos** se acumula: los festivos de la entidad más los festivos propios de la sucursal forman el calendario de días no laborables de los empleados de esa sucursal.
- El **horario de turnos** se reemplaza: si la sucursal tiene un horario propio, reemplaza completamente al de la entidad. No se mezclan.
- Las **excepciones individuales** de un empleado reemplazan completamente el horario del nivel superior para las fechas o días a los que aplican.

> **Nota:** El comportamiento de acumulación de festivos significa que un empleado de una sucursal local puede heredar tanto los festivos nacionales de la entidad como los festivos locales de su sucursal. Esto es intencionado y refleja la realidad normativa de la mayoría de las empresas.

---

## Cómo depurar el horario efectivo de un empleado en el backoffice

Si un responsable necesita verificar qué horario está usando un empleado en un momento determinado, puede consultarlo desde el backoffice siguiendo estos pasos:

1. Acceda al backoffice con rol owner o manager.
2. Navegue a **Empleados** y seleccione el empleado cuyo horario desea revisar.
3. Abra la sección **Calendario efectivo**.
4. El sistema muestra el calendario del mes en curso con el origen de cada configuración: si el día usa el horario de la entidad, el de la sucursal o una excepción individual, queda indicado claramente.
5. Para consultar un mes diferente, use los controles de navegación del calendario.
6. Para ver el detalle de un día concreto (turnos activos, franjas horarias, excepciones aplicadas), pulse sobre la celda del día.

Esta herramienta es la primera referencia cuando un empleado reporta que no pudo fichar o que el sistema validó su entrada en un horario inesperado.

---

## Errores habituales relacionados con la herencia

### El empleado no puede fichar cuando debería poder

Verifique que no existe una excepción individual que marque ese día como no laborable. Las excepciones individuales prevalecen sobre el horario de la sucursal, por lo que una excepción activa puede estar bloqueando fichajes válidos.

### El empleado puede fichar en un horario que no le corresponde

Compruebe si existe una excepción periódica activa con una franja horaria más amplia que la del horario de sucursal. Si existe, el sistema la utilizará en lugar del horario estándar.

### La sucursal tiene festivo pero el empleado puede fichar

El empleado puede tener una excepción individual que marque ese día como laborable. Las excepciones individuales anulan los festivos de nivel superior cuando están configuradas explícitamente.

> **Aviso:** Antes de contactar con soporte por un comportamiento inesperado en el fichaje de un empleado, revise siempre el calendario efectivo desde el backoffice. La mayoría de las incidencias tienen su origen en una excepción individual configurada incorrectamente o en un festivo que no se eliminó tras quedar obsoleto.

---

## Artículos relacionados

- [Horarios base y turnos](23-horarios-base-y-turnos.md)
- [Calendario laboral](24-calendario-laboral.md)
- [Excepciones de horario](25-excepciones-de-horario.md)
- [Turnos rotativos](27-turnos-rotativos.md)
- [Horario flexible](28-horario-flexible.md)
- [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md)

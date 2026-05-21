# Excepciones de horario

El horario base de una sucursal o entidad define las condiciones estándar de trabajo para el grueso de los empleados. Sin embargo, existen situaciones legítimas en las que un empleado necesita un horario diferente al del resto: una reducción de jornada por motivos familiares, una adaptación temporal durante un período de recuperación, o un horario especial acordado contractualmente.

Para dar cobertura a estos casos, CheckBiz360 permite configurar excepciones individuales de horario. Una excepción es una regla de horario vinculada exclusivamente a un empleado concreto que prevalece sobre el horario heredado de la sucursal o la entidad.

---

## Tipos de excepción

### Excepción puntual

Una excepción puntual se aplica a un único día concreto. Es útil para casos aislados: el empleado entra antes o después de lo habitual un día específico, o ese día está marcado como no laborable solo para él.

Ejemplo: el 15 de junio, el empleado tiene una cita médica y su jornada comienza a las 11:00 en lugar de las 09:00. Se crea una excepción puntual para esa fecha con el turno ajustado.

### Excepción periódica

Una excepción periódica se repite de forma sistemática, generalmente con una cadencia semanal. Es la modalidad más adecuada para situaciones de larga duración como una jornada reducida por guarda legal o un horario de adaptación laboral post-baja.

Ejemplo: todos los viernes, el empleado tiene jornada intensiva y sale a las 15:00 en lugar de las 17:00. Se configura una excepción periódica que aplica cada viernes mientras esté vigente el período de adaptación.

---

## Cómo crear una excepción de horario

1. Acceda al backoffice con rol owner o manager.
2. Navegue a **Empleados** y seleccione el empleado correspondiente.
3. Acceda a la sección **Horario y calendario**.
4. Pulse el botón **Nueva excepción**.
5. Seleccione el tipo de excepción: **Puntual** o **Periódica**.
6. Si es puntual, indique la fecha concreta.
7. Si es periódica, seleccione los días de la semana a los que aplica y defina la fecha de inicio y, opcionalmente, la fecha de fin.
8. Configure la franja horaria de la excepción: hora de inicio (`start.hour`, `start.minute`) y hora de fin (`end.hour`, `end.minute`).
9. Si la excepción marca el día como no laborable para ese empleado, active la opción **Día no laborable**.
10. Guarde la excepción.

Una vez guardada, la excepción entra en vigor de forma inmediata. El sistema la utilizará en los próximos fichajes del empleado.

> **Aviso:** Las excepciones de horario no tienen efecto retroactivo sobre fichajes ya registrados. Solo afectan a los fichajes realizados a partir del momento de su creación.

---

## Casos de uso habituales

### Empleado con jornada reducida

Un empleado con reducción de jornada por conciliación familiar trabaja de 09:00 a 14:00 en lugar del horario estándar de 09:00 a 17:00. Se configura una excepción periódica que aplica de lunes a viernes con el turno reducido. El resto de empleados de la sucursal mantienen su horario habitual sin ninguna alteración.

### Horario de adaptación laboral

Un empleado que se reincorpora después de una baja larga comienza con jornadas más cortas durante las primeras semanas. Se crea una excepción periódica con una fecha de fin definida. Cuando llega esa fecha, el sistema deja de aplicar la excepción y el empleado vuelve automáticamente al horario de la sucursal.

### Día puntual no laborable

Un empleado solicita un día de permiso no retribuido. El responsable puede crear una excepción puntual que marque ese día como no laborable para ese empleado. Cualquier intento de fichaje ese día generará el código `checklog/day_disabled`, igual que ocurre en los festivos del calendario general.

---

## Prioridad de las excepciones individuales

Cuando el sistema resuelve el calendario efectivo de un empleado, sigue un orden de prioridad. Las excepciones individuales tienen la mayor prioridad y siempre prevalecen sobre el horario de la sucursal y el de la entidad.

La lógica es la siguiente:

1. El sistema comprueba si el empleado tiene una excepción individual activa para ese día.
2. Si existe una excepción, la utiliza como referencia para validar el fichaje.
3. Si no existe ninguna excepción, consulta el horario de la sucursal.
4. Si la sucursal no tiene un horario propio configurado, utiliza el horario de la entidad.

Esto significa que una excepción individual puede tanto restringir como ampliar el horario heredado. Si el horario de la sucursal define un turno de 09:00 a 17:00 pero el empleado tiene una excepción de 07:00 a 15:00, el sistema utilizará el turno de 07:00 a 15:00 para ese empleado.

> **Nota:** Para una explicación completa del algoritmo de resolución jerárquica, consulte el artículo [Herencia de configuración](26-herencia-de-configuracion.md).

---

## Gestión y revisión de excepciones activas

El responsable puede consultar en cualquier momento las excepciones activas de un empleado desde la ficha del empleado en el backoffice. La sección **Horario y calendario** muestra la lista de excepciones vigentes con su tipo, fechas de aplicación y la franja horaria configurada.

Para desactivar una excepción antes de su fecha de fin prevista, selecciónela y pulse **Desactivar**. La excepción queda archivada y el empleado recupera el horario heredado de la sucursal o la entidad.

---

## Artículos relacionados

- [Horarios base y turnos](23-horarios-base-y-turnos.md)
- [Calendario laboral](24-calendario-laboral.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Horario flexible](28-horario-flexible.md)
- [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md)

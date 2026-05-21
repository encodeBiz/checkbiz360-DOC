# Turnos rotativos

En determinados sectores y empresas, la jornada laboral no es uniforme de una semana a otra. Los trabajadores alternan entre diferentes franjas horarias siguiendo un patrón cíclico predefinido. CheckBiz360 soporta esta modalidad mediante la configuración de turnos rotativos, que permiten definir ciclos de alternancia semanal y asignarlos a los empleados que los requieran.

---

## Qué es un turno rotativo

Un turno rotativo es un esquema de horario en el que el empleado no trabaja siempre en la misma franja horaria, sino que alterna entre dos o más franjas siguiendo un ciclo regular. El ciclo más habitual es la alternancia semanal (semana A y semana B), aunque el sistema permite ciclos más largos.

Esta modalidad es frecuente en sectores como la industria, la logística, la sanidad y la hostelería, donde la cobertura horaria continua o ampliada requiere distribuir las horas entre equipos que se alternan.

---

## Configuración de alternancia semanal (semana A / semana B)

Para configurar un turno rotativo con alternancia semanal, es necesario definir dos grupos de turnos: los que aplican en la semana A y los que aplican en la semana B. Cada grupo especifica las franjas horarias para cada día activo de esa semana.

### Paso a paso para crear un turno rotativo

1. Acceda al backoffice con rol owner o manager.
2. Navegue a **Configuración > Horarios** en la entidad o sucursal correspondiente.
3. Pulse **Nuevo horario** y seleccione el tipo **Rotativo**.
4. Defina el ciclo de rotación: indique el número de semanas que compone un ciclo completo (2 para el ciclo A/B estándar).
5. Configure la semana A: para cada día activo, defina los parámetros del turno (`start.hour`, `start.minute`, `end.hour`, `end.minute`).
6. Configure la semana B: repita el proceso con los valores horarios correspondientes a esta semana.
7. Defina la fecha de inicio del ciclo: esta fecha ancla el calendario y determina qué semana es A y cuál es B en cualquier fecha futura.
8. Guarde el horario.
9. Asigne el horario rotativo a los empleados que deban seguirlo.

---

## Ejemplo real: entrada a las 7:00 en semana A, 15:00 en semana B

Imagine una empresa de logística que necesita cobertura de turno de mañana y turno de tarde. Dos grupos de empleados se alternan cada semana:

| Semana | Lunes a viernes | Inicio | Fin |
|---|---|---|---|
| Semana A (mañana) | Activos | 07:00 | 15:00 |
| Semana B (tarde) | Activos | 15:00 | 23:00 |

La configuración de la semana A tiene `start.hour: 7`, `start.minute: 0`, `end.hour: 15`, `end.minute: 0`. La semana B tiene `start.hour: 15`, `start.minute: 0`, `end.hour: 23`, `end.minute: 0`.

Si el ciclo comienza el lunes 5 de enero con la semana A, el sistema calculará automáticamente que:

- La semana del 5 de enero es semana A (turno de mañana).
- La semana del 12 de enero es semana B (turno de tarde).
- La semana del 19 de enero vuelve a ser semana A.
- Y así sucesivamente de forma indefinida.

---

## Ciclo de rotación

El ciclo de rotación es el número de semanas que transcurren antes de que el patrón se repita. Para una alternancia A/B, el ciclo es de 2 semanas. Es posible configurar ciclos más largos, por ejemplo de 3 semanas (A, B, C), para esquemas de rotación más complejos.

La fecha de inicio del ciclo es el parámetro crítico: define el punto de anclaje desde el que el sistema calcula qué semana del ciclo corresponde a cada fecha. Si esta fecha se configura incorrectamente, todos los turnos quedan desfasados una semana.

> **Aviso:** Verifique siempre la fecha de inicio del ciclo antes de activar un horario rotativo. Una vez que los empleados empiezan a fichar con este horario, corregir el anclaje del ciclo puede requerir revisar y ajustar fichajes ya registrados.

---

## Consideraciones de festivos con turnos rotativos

Los festivos del calendario laboral se aplican con independencia del tipo de turno. Esto significa que si una fecha está marcada como festivo en la entidad o la sucursal, el sistema devolverá `checklog/day_disabled` incluso si ese día corresponde a un turno activo dentro del ciclo rotativo.

Esta interacción puede generar situaciones específicas que conviene gestionar con anticipación:

- Si un festivo cae en semana A y otro en semana B, ambos se bloquean igualmente independientemente del turno vigente.
- Si la empresa trabaja en festivo, debe desactivar el festivo para la fecha concreta o para la sucursal afectada antes de que los empleados intenten fichar.
- Si solo trabajan los empleados de turno de tarde en un festivo, la forma más precisa de gestionar este caso es mediante excepciones individuales que anulen el festivo solo para esos empleados.

> **Nota:** Para una guía completa sobre cómo manejar el trabajo en festivos, consulte el artículo [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md).

---

## Asignación de horarios rotativos a empleados

Una vez creado el horario rotativo en la configuración de la sucursal o entidad, puede asignarse a empleados concretos desde su ficha individual o de forma masiva desde la gestión de horarios.

Si varios grupos de empleados siguen el mismo ciclo pero con desfase (un grupo empieza en semana A mientras otro empieza en semana B), deberá crear dos instancias del horario rotativo con fechas de inicio de ciclo diferentes: una anclada en semana A y otra en semana B.

---

## Artículos relacionados

- [Horarios base y turnos](23-horarios-base-y-turnos.md)
- [Calendario laboral](24-calendario-laboral.md)
- [Excepciones de horario](25-excepciones-de-horario.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Festivos y días no laborables](29-festivos-y-dias-no-laborables.md)

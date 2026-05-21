# Horario flexible

El horario flexible en CheckBiz360 no significa que el empleado pueda fichar a cualquier hora sin control. Significa que el sistema ofrece un margen de tolerancia de entrada configurable y un mecanismo de ajuste automático de horario que garantiza que las horas trabajadas se computen de forma correcta, independientemente de que el empleado llegue unos minutos antes o después de la hora oficial del turno.

---

## Qué es el horario flexible en CheckBiz360

En un entorno de control de asistencia estricto, un fichaje registrado 10 minutos antes del inicio del turno generaría un cómputo de horas incorrecto: el sistema contaría esos 10 minutos como tiempo trabajado aunque el empleado aún no estuviera en su puesto en horario oficial.

El horario flexible resuelve este problema mediante dos mecanismos complementarios:

- La **tolerancia de entrada**, que define cuántos minutos antes del inicio del turno el sistema acepta el fichaje como válido.
- El **ajuste automático de horario**, que normaliza el timestamp del registro a la hora oficial del turno cuando el empleado ficha dentro del margen de tolerancia.

---

## Tolerancia de entrada

Este parámetro define el margen de tolerancia de entrada, expresado en minutos, antes del inicio oficial del turno. Si un empleado intenta fichar antes de que el turno haya comenzado pero dentro de ese margen, el sistema acepta el fichaje en lugar de rechazarlo.

Por ejemplo, si el turno comienza a las 09:00 y la tolerancia de entrada tiene un valor de 15, el sistema acepta fichajes a partir de las 08:45. Un fichaje a las 08:47 se procesa normalmente. Un fichaje a las 08:30 (30 minutos antes del turno, fuera del margen) generaría el error `checklog/out_of_schedule`.

Este parámetro no amplía el cómputo de horas: su función es simplemente determinar si el fichaje se acepta o se rechaza. El ajuste del timestamp es responsabilidad del segundo mecanismo.

### Cómo configurar la tolerancia de entrada

1. Acceda al backoffice con rol owner o manager.
2. Navegue a **Configuración** de la entidad o sucursal.
3. Acceda al apartado **Horarios y tolerancias**.
4. Localice el campo **Tolerancia de entrada (minutos)** y establezca el valor deseado.
5. Guarde los cambios.

> **Nota:** La tolerancia de entrada se configura a nivel de sucursal o entidad y se aplica a todos los empleados que hereden ese horario. Si necesita una tolerancia diferente para un empleado concreto, puede definirla dentro de una excepción individual de horario.

---

## Ajuste automático de horario

Cuando esta opción está activada, el sistema aplica el ajuste automático de timestamp en los fichajes que se realizan dentro del margen de tolerancia pero antes del inicio oficial del turno.

El funcionamiento es el siguiente: si el empleado ficha a las 08:52 y el turno comienza a las 09:00, el timestamp almacenado en el registro no será las 08:52 sino las 09:00. El sistema desplaza la hora registrada al inicio oficial del turno.

Este ajuste se almacena de forma interna en el registro de fichaje. El timestamp original (08:52) también se conserva para auditoría, pero el cómputo de horas utiliza el timestamp ajustado.

### Por qué es importante activar el ajuste automático de horario

Sin este ajuste, un empleado que tiene la costumbre de llegar 10 minutos antes acumularía, a lo largo del mes, entre 3 y 4 horas de tiempo registrado antes del inicio oficial de sus turnos. Estas horas quedarían reflejadas en los informes de jornada y podrían generar discrepancias con la nómina o con la política de la empresa.

Con el ajuste activado, todos los fichajes dentro del margen quedan normalizados a la hora oficial y el cómputo de horas refleja únicamente el tiempo de jornada contratado.

---

## Casos de uso del horario flexible

### Flexibilidad de entrada con cómputo de horas correcto

Una empresa de servicios profesionales permite a sus empleados llegar entre las 08:30 y las 09:30. El turno oficial comienza a las 09:00 pero la tolerancia de entrada tiene un valor de 30. Los empleados que llegan a las 08:45 fichan sin problemas. Con el ajuste automático de horario activado, su registro de entrada queda ajustado a las 09:00 y no se generan horas extra no deseadas.

### Notificación de entrada anticipada sin ajuste de timestamp

Algunas empresas prefieren registrar la hora real de llegada pero recibir una alerta si el empleado entra con mucha antelación. En este caso, se activa la tolerancia de entrada pero se desactiva el ajuste automático de horario. El sistema acepta el fichaje anticipado y almacena el timestamp real sin ajuste, lo que permite al responsable revisar el patrón de entradas.

### Control estricto de entradas

Si la empresa necesita un control estricto sin margen de tolerancia, se configura la tolerancia de entrada a 0 o a un valor muy bajo (1-2 minutos). El empleado solo puede fichar a partir del inicio exacto del turno, con un margen mínimo para evitar rechazos por desfases de segundos en el reloj del dispositivo.

---

## Interacción entre tolerancia y ajuste de timestamp

| Tolerancia de entrada | Ajuste automático de horario | Comportamiento |
|---|---|---|
| 15 minutos | Activado | Acepta fichajes 15 min antes. El timestamp se ajusta al inicio del turno. |
| 15 minutos | Desactivado | Acepta fichajes 15 min antes. El timestamp registra la hora real. |
| 0 minutos | Cualquiera | Solo acepta fichajes a partir del inicio exacto del turno. |

> **Aviso:** Si activa el ajuste automático de horario sin configurar la tolerancia de entrada, el ajuste automático solo tendrá efecto si el fichaje cae dentro de la ventana activa del turno, que por defecto empieza en el instante exacto de inicio. Asegúrese de configurar ambos ajustes de forma coherente.

---

## Artículos relacionados

- [Horarios base y turnos](23-horarios-base-y-turnos.md)
- [Excepciones de horario](25-excepciones-de-horario.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Turnos rotativos](27-turnos-rotativos.md)
- [Cómo funciona el fichaje](../03-control-horario/13-como-funciona-el-fichaje.md)
- [Estados y códigos de error](../03-control-horario/22-estados-y-codigos-de-error.md)

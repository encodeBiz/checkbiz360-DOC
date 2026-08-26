# Jornada estricta y jornada flexible

CheckBiz360 no computa las horas trabajadas de una única manera: cada calendario decide si aplica el **horario oficial** o el **tiempo realmente trabajado**. Esa decisión se toma con un interruptor, **Jornada estricta / Jornada flexible**, y es probablemente el ajuste que más impacto tiene sobre los informes de horas.

Existe el mismo interruptor para los descansos, con la misma lógica.

---

## Jornada estricta

Con la jornada estricta, **manda el horario configurado**. El sistema no reconoce tiempo trabajado fuera de la franja oficial:

- Las entradas **antes** del horario no se contabilizan.
- Las entradas tarde y las salidas anticipadas **se descuentan**.
- Las salidas **después** del horario no se contabilizan como tiempo extra.

Es la opción adecuada cuando la jornada está cerrada por convenio o por política interna y no se quiere que la costumbre de llegar diez minutos antes acabe generando horas extra en el informe. El empleado que llega a las 08:50 a un turno de 09:00 no acumula esos diez minutos; el que llega a las 09:10, sí ve el retraso descontado.

## Jornada flexible

Con la jornada flexible, **manda lo que registró el empleado**:

- Se contabiliza la jornada real trabajada.
- El tiempo trabajado antes o después del horario **se suma como extra**.
- Los retrasos y las salidas anticipadas **se descuentan**.

Es la opción adecuada cuando el horario es una referencia y lo que se quiere medir es la dedicación efectiva: equipos de campo, servicios con picos de trabajo, turnos que se alargan por necesidad operativa.

> **Importante:** ninguna de las dos modalidades cambia lo que el empleado registra. El fichaje siempre guarda la hora real; lo que cambia es cómo se computa esa hora al calcular el tiempo trabajado. La trazabilidad del registro original se conserva en ambos casos.

---

## Cómo se configura

1. Acceda a **Calendario** en el menú lateral.
2. Elija el ámbito sobre el que quiere trabajar: **Configuración general** (entidad), **Sucursal** o **Empleado**.
3. Bajo el horario semanal, localice el interruptor de **Jornada estricta / Jornada flexible**.
4. Actívelo o desactívelo. El recuadro que aparece debajo resume las reglas de cómputo que quedan aplicadas, para que no haya duda de lo que se está eligiendo.
5. Guarde el calendario.

Al ser parte del calendario, sigue la misma **herencia** que el resto de la configuración: lo que se define en la entidad baja a las sucursales, y lo que se define en una sucursal baja a sus empleados, salvo que ese nivel tenga su propia configuración. Consulte [Herencia de configuración](./26-herencia-de-configuracion.md).

---

## Descanso estricto y descanso flexible

Los descansos tienen su propio interruptor, con una diferencia importante respecto a la jornada: **cambia lo que el empleado tiene que hacer**.

| Modalidad | Cómo se computa | Qué hace el empleado |
|---|---|---|
| **Descanso estricto** | Se aplica exactamente la duración configurada. No se reconocen descansos más largos ni más cortos | **No marca** inicio ni fin de la pausa |
| **Descanso flexible** | Se contabiliza el tiempo real de descanso, según la duración efectiva | **Marca** el inicio y el fin de cada pausa desde la app |

Con el descanso estricto se indica además la **duración en minutos** que el sistema descontará de la jornada.

La elección depende de la operativa real: el descanso estricto simplifica —nadie tiene que acordarse de fichar la pausa— pero no refleja las desviaciones; el flexible refleja lo que ocurrió, a cambio de exigir dos fichajes más al día.

---

## Cómo elegir entre una y otra

| Situación | Recomendación |
|---|---|
| Jornada cerrada por convenio, sin horas extra | Jornada estricta |
| Se quiere evitar que las llegadas anticipadas generen tiempo extra | Jornada estricta |
| Equipos de campo o servicios con jornada variable | Jornada flexible |
| Se retribuyen o se compensan las horas extra realmente trabajadas | Jornada flexible |
| Pausa fija de comida, igual todos los días | Descanso estricto |
| Pausas variables según la carga de trabajo | Descanso flexible |

> **Aviso:** cambiar de modalidad afecta al cómputo de las jornadas que se registren a partir de ese momento. Antes de cambiarla en una entidad con actividad, valore hacerlo coincidir con el inicio de un periodo de nómina para que el informe del mes no mezcle dos criterios de cómputo.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Horarios base y turnos](./23-horarios-base-y-turnos.md) | Configuración del horario semanal y de varios turnos por día |
| [Excepciones de horario](./25-excepciones-de-horario.md) | Ajustes puntuales sobre el horario heredado |
| [Herencia de configuración](./26-herencia-de-configuracion.md) | Prioridad entre entidad, sucursal y empleado |
| [Descansos y pausas](../03-control-horario/17-descansos-y-pausas.md) | Cómo se registran las pausas desde la app |
| [Cómo funciona el fichaje](../03-control-horario/13-como-funciona-el-fichaje.md) | Las validaciones que se aplican en cada fichaje |

# Turnos rotativos

En sectores como la industria, la logística, la sanidad o la hostelería la jornada no es uniforme de una semana a otra: los equipos alternan franjas horarias siguiendo un ciclo. Este artículo explica cómo se cubre esa necesidad en CheckBiz360.

---

## Estado de la funcionalidad

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

CheckBiz360 **no dispone de un tipo de horario rotativo** con ciclo de alternancia automático: no existe una configuración de "semana A / semana B" con fecha de anclaje que el sistema resuelva por su cuenta. El horario semanal configurado para una entidad, sucursal o empleado se repite igual todas las semanas.

---

## Cómo cubrir la rotación con lo que existe hoy

Hay tres formas de operar con equipos rotativos. La elección depende de si la rotación es estable o cambia con frecuencia.

### Opción 1: una sucursal por turno (rotación estable)

Si los turnos son fijos y lo que rota son las personas, configure **una sucursal por franja horaria** —por ejemplo "Planta - Mañana" y "Planta - Tarde", con las mismas coordenadas y la misma geocerca— y mueva la asignación del empleado de una a otra cuando le toque cambiar.

Es la opción más limpia: cada sucursal tiene su horario, sus festivos y su calendario efectivo, y el histórico de fichajes queda imputado a la franja en la que realmente se trabajó.

### Opción 2: horario personalizado en el empleado (rotación variable)

Si la rotación es irregular, configure el horario en la ficha del **empleado** en lugar de heredarlo de la sucursal, y ajústelo al cambiar de ciclo. El calendario del empleado tiene prioridad sobre el de su sucursal.

Es más flexible, pero exige mantener el cambio a mano en cada ciclo y para cada persona.

### Opción 3: el modo Por turnos (rotación planificada)

Si planifica las semanas por adelantado, ponga la sucursal en el modo **Por turnos** y cargue los turnos de cada persona semana a semana. **Copiar a la semana siguiente** repite una semana y después se retoca lo que cambie, y el importador del cuadrante carga la semana de toda la sucursal desde Excel. El ciclo no se genera solo, pero no hay que cambiar ningún horario al pasar de una semana a otra. Tenga en cuenta que en **Por turnos** una semana sin cargar libra entera. Ver [Por turnos: el horario son los turnos que usted carga](114-calendario-de-turnos-por-fecha.md).

> **Aviso:** en las dos primeras opciones, cambie el horario **antes** de que empiece el ciclo nuevo. Cada fichaje se valida contra el calendario efectivo vigente en ese momento; actualizar el horario después no reevalúa los fichajes ya registrados.

---

## Ejemplo: mañana y tarde alternas

Una empresa de logística necesita cobertura de 07:00 a 15:00 y de 15:00 a 23:00, con dos equipos que se alternan cada semana.

Con la Opción 1, se crean dos sucursales sobre la misma nave:

| Sucursal | Horario de lunes a viernes |
|---|---|
| Nave - Mañana | 07:00 – 15:00 |
| Nave - Tarde | 15:00 – 23:00 |

Cada lunes de cambio, el responsable reasigna los empleados de una sucursal a la otra. El fichaje de cada semana se valida contra el horario correcto y los informes distinguen la actividad de cada franja.

---

## Rotación y festivos

Los festivos se aplican por fecha, con independencia del turno que tocara ese día: un festivo configurado en la entidad o en la sucursal deshabilita el día para todos los empleados que hereden ese calendario, y un intento de fichaje devuelve `checklog/day_disabled`.

Si en su organización se trabaja en festivo por turnos, no marque el día como festivo en la sucursal: trátelo como laborable y registre las ausencias de quienes libran en la ficha de cada empleado. Consulte [Festivos y días no laborables](./29-festivos-y-dias-no-laborables.md).

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Horarios base y turnos](./23-horarios-base-y-turnos.md) | Configuración del horario semanal y de varios turnos por día |
| [Calendario laboral](./24-calendario-laboral.md) | Festivos y calendario efectivo |
| [Excepciones de horario](./25-excepciones-de-horario.md) | Ajustes puntuales sobre el horario heredado |
| [Herencia de configuración](./26-herencia-de-configuracion.md) | Prioridad entre entidad, sucursal y empleado |
| [Asignar empleados a sucursales](../08-sucursales-y-entidad/60-asignar-empleados-a-sucursales.md) | Mover a un empleado entre centros o turnos |

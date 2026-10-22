# Festivos y días no laborables

La gestión de festivos es uno de los aspectos más delicados del control de asistencia, especialmente en empresas que operan en varias regiones o en sectores que trabajan habitualmente en días que para otros son no laborables. CheckBiz360 ofrece un sistema flexible que permite tanto bloquear fichajes en festivos como habilitarlos cuando la actividad de la empresa así lo requiere.

---

## Tipos de festivo y día no laborable

CheckBiz360 clasifica los días no laborables en distintas categorías que determinan su alcance dentro de la jerarquía de configuración:

### Festivo nacional

Un festivo nacional es una fecha declarada como no laborable por la normativa estatal y que aplica a toda la organización. Se configura a nivel de entidad y se hereda automáticamente por todas las sucursales y empleados.

### Festivo autonómico

Un festivo autonómico aplica únicamente a las sucursales ubicadas en la comunidad autónoma correspondiente. Se configura a nivel de sucursal para que solo afecte a los empleados de ese centro.

### Festivo local

Similar al autonómico, el festivo local aplica a un municipio o zona concreta. Se gestiona a nivel de sucursal, permitiendo que solo los empleados de esa sucursal queden afectados por el bloqueo de fichaje.

### Puente

Un día de puente es un día laborable que la empresa, por decisión interna, convierte en no laborable para facilitar la continuidad de un festivo oficial. Se configura como un día no laborable interno con una descripción que lo identifique.

### Día no laborable interno

Esta categoría cubre cualquier fecha que la empresa decida bloquear por motivos propios: cierres por inventario, reformas, formaciones obligatorias en las que no existe jornada regular, etc.

---

## Ausencias de un empleado

Las vacaciones, los permisos y los días libres de una persona concreta se registran como **ausencias** en su calendario. Se añaden desde la ficha del empleado o desde el [tablero de disponibilidad](98-tablero-de-disponibilidad.md), y se consultan también en la pestaña **No laborables de empleados** de **Horarios**.

- **Rango de fechas.** Una ausencia puede cubrir varios días seguidos. En las listas aparece como una sola fila con su inicio, su fin y el número de días (por ejemplo, «1 – 15 sep · 15 días»), que se despliega para ver o quitar días sueltos.
- **Retribuida.** Cada ausencia de empleado lleva una casilla **Retribuida** con tres valores posibles: *retribuida*, *no retribuida* o *sin definir*. *Sin definir* significa que no consta —por ejemplo, en las ausencias registradas antes de que existiera la casilla— y se muestra distinto de *no retribuida* para no confundir un dato que falta con un «no». Los festivos de la entidad o de la sucursal no llevan esta marca.

Un día de ausencia bloquea el fichaje de esa persona igual que un festivo.

Las personas también pueden pedir sus vacaciones o permisos desde la app, en **Mi calendario**. Al aprobarlas en **Contacto → Solicitudes**, los días quedan como ausencias, con la marca de retribuida que elija quien aprueba. Ver [Vacaciones y permisos desde la app](115-vacaciones-y-permisos-desde-la-app.md).

---

## Cómo CheckBiz360 bloquea fichajes en días no laborables

Cuando un empleado intenta registrar su entrada o salida en una fecha marcada como no laborable en su calendario efectivo, el sistema devuelve el código de error `checklog/day_disabled` y rechaza el fichaje.

Este bloqueo opera antes de cualquier otra validación. El sistema no comprueba la ubicación ni el turno activo si el día está marcado como no laborable: el rechazo es inmediato.

Los intentos de fichaje en días no laborables quedan registrados en el historial con su timestamp, el dispositivo utilizado y el código de error, lo que permite al responsable detectar si un empleado está intentando fichar en un día que no le corresponde.

---

## Qué ocurre si la empresa trabaja en festivo

Existen sectores en los que trabajar en festivo es la norma: el comercio minorista, la hostelería, el transporte o los servicios de emergencia operan con normalidad en días que para otras empresas son no laborables.

Un festivo configurado se aplica a **todos** los empleados de su ámbito: no hay forma de anularlo solo para una sucursal o solo para una persona. Ni siquiera un horario personalizado con turno ese día lo salta; el fichaje se rechaza con `checklog/day_disabled`. Por eso, la forma de trabajar en festivo es no marcar como festivo lo que no cierra.

### Toda la sucursal trabaja ese día

- Si el festivo está en la **sucursal**, elimínelo de sus días libres. La fecha deja de estar bloqueada para los empleados de esa sucursal.
- Si el festivo está en la **entidad**, afecta a todas las sucursales. Retírelo de la entidad y añádalo como festivo local solo en las sucursales que sí cierran.

### Solo una parte de la plantilla trabaja ese día

Si solo trabaja una parte (por ejemplo, el personal de atención al cliente pero no el de administración):

1. No marque el día como festivo en la sucursal: trátelo como laborable.
2. Registre una **ausencia** ese día a quienes libran, desde su ficha o desde el [tablero de disponibilidad](98-tablero-de-disponibilidad.md).
3. Quienes trabajan fichan con normalidad; quienes tienen la ausencia quedan bloqueados.

> **Aviso:** los festivos de entidad, sucursal y empleado **se suman**; no se anulan entre sí. La herencia en la que el nivel del empleado prevalece es la del horario semanal, no la de los festivos.

---

## Consideraciones por sector

### Retail y comercio minorista

El comercio suele operar durante puentes, festivos locales e incluso algunos festivos nacionales. Es habitual configurar la sucursal con un calendario sin festivos y gestionar los cierres puntuales (por ejemplo, Navidad o Año Nuevo) añadiendo manualmente los días que la tienda permanece cerrada.

### Hostelería y restauración

La hostelería trabaja prácticamente sin interrupción durante el año, incluidos los festivos más señalados. En este sector es recomendable dejar el calendario de la sucursal limpio de festivos y añadir únicamente los días de cierre real del establecimiento.

### Servicios sanitarios y de emergencias

En estos sectores, el trabajo en festivos es parte del convenio colectivo. CheckBiz360 permite registrar la jornada en festivo sin bloqueos y, si la empresa necesita identificar los días festivos trabajados para el cálculo de complementos salariales, puede utilizar los informes de jornada filtrados por tipo de día.

### Actividades estacionales

Las empresas con actividad estacional (turismo, agricultura, eventos) pueden tener períodos en los que operan con normalidad durante festivos y otros en los que permanecen cerradas. La configuración recomendada en estos casos es definir el calendario de festivos a nivel de entidad con los festivos nacionales y gestionar las particularidades de cada temporada mediante el calendario de la sucursal o mediante días no laborables internos.

---

## Gestión de festivos por anticipado

Se recomienda configurar el calendario de festivos al inicio de cada año natural o con suficiente antelación respecto a cada festivo. CheckBiz360 no aplica automáticamente los festivos oficiales del país: el responsable debe introducirlos manualmente o importarlos si la plataforma dispone de esa funcionalidad en su plan de suscripción.

> **Nota:** Si un festivo no está configurado en el calendario y los empleados fichan ese día, los registros quedarán como válidos. No existe forma de marcar retroactivamente un fichaje ya registrado como "festivo trabajado" sin revisar y ajustar manualmente los registros afectados. La configuración anticipada del calendario evita este tipo de incidencias.

---

## Artículos relacionados

- [Horarios base y turnos](23-horarios-base-y-turnos.md)
- [Calendario laboral](24-calendario-laboral.md)
- [Excepciones de horario](25-excepciones-de-horario.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Turnos rotativos](27-turnos-rotativos.md) — no disponible en la versión actual; alternativas
- [Tablero de disponibilidad](98-tablero-de-disponibilidad.md)
- [Vacaciones y permisos desde la app](115-vacaciones-y-permisos-desde-la-app.md)
- [Estados y códigos de error](../03-control-horario/22-estados-y-codigos-de-error.md)

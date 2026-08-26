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

## Cómo CheckBiz360 bloquea fichajes en días no laborables

Cuando un empleado intenta registrar su entrada o salida en una fecha marcada como no laborable en su calendario efectivo, el sistema devuelve el código de error `checklog/day_disabled` y rechaza el fichaje.

Este bloqueo opera antes de cualquier otra validación. El sistema no comprueba la ubicación ni el turno activo si el día está marcado como no laborable: el rechazo es inmediato.

Los intentos de fichaje en días no laborables quedan registrados en el historial con su timestamp, el dispositivo utilizado y el código de error, lo que permite al responsable detectar si un empleado está intentando fichar en un día que no le corresponde.

---

## Qué ocurre si la empresa trabaja en festivo

Existen sectores en los que trabajar en festivo es la norma: el comercio minorista, la hostelería, el transporte o los servicios de emergencia operan con normalidad en días que para otras empresas son no laborables.

CheckBiz360 permite deshabilitar un festivo puntualmente para que los empleados afectados puedan fichar con normalidad ese día.

### Deshabilitar un festivo de forma puntual para toda la sucursal

1. Acceda al backoffice con rol owner o manager.
2. Navegue a **Sucursales** y seleccione la sucursal que trabaja ese día.
3. Acceda a **Calendario** en el menú lateral.
4. Localice la fecha del festivo en la lista de días no laborables.
5. Seleccione la entrada y pulse **Desactivar para esta fecha**.
6. Confirme la acción. La fecha deja de estar bloqueada para los empleados de esa sucursal.

### Deshabilitar un festivo solo para empleados concretos

Si solo una parte de los empleados trabaja en el festivo (por ejemplo, el personal de atención al cliente pero no el de administración), la forma más precisa de gestionar esto es mediante excepciones individuales:

1. Acceda a la ficha de cada empleado que trabaja ese día.
2. Cree una excepción puntual para esa fecha que marque el día como laborable y defina el turno correspondiente.
3. Los empleados con excepción podrán fichar ese día. Los demás continuarán con el bloqueo del festivo.

> **Aviso:** Recuerde que las excepciones individuales tienen prioridad sobre el calendario de la sucursal. Una excepción individual que marque un festivo como laborable permite al empleado fichar aunque ese festivo esté activo a nivel de entidad o sucursal.

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
- [Estados y códigos de error](../03-control-horario/22-estados-y-codigos-de-error.md)

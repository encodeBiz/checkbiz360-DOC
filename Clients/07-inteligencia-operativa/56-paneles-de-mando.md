# Paneles de mando

## Qué son los paneles de mando

Los paneles de mando, o dashboards, son las vistas del backoffice desde las que los responsables acceden de forma resumida a los indicadores más relevantes de la inteligencia operativa. No requieren configuración adicional: se nutren automáticamente de los datos que la plataforma acumula con el uso diario.

Existen cuatro paneles diferenciados, cada uno orientado a una dimensión distinta del análisis operativo: asistencia, eficiencia, costes y anomalías. Pueden consultarse de forma independiente o en una vista combinada según la configuración del usuario.

## Panel de KPIs de asistencia

Este panel ofrece una fotografía en tiempo real de la presencia del equipo. Sus indicadores principales son:

**Tasa de presencia hoy.** Porcentaje de empleados con turno activo que han fichado su entrada en el día en curso. Permite detectar de un vistazo si hay ausencias no comunicadas antes de que afecten a la operación.

**Asistencia de los últimos 30 días.** Evolución de la tasa de presencia del equipo durante el último mes, representada en gráfica de línea. Permite identificar si existe alguna tendencia de deterioro o si hay días de la semana con ausencias recurrentes.

**Empleados sin fichar.** Lista actualizada en tiempo real de los empleados que tienen turno activo pero todavía no han registrado su entrada. Incluye el tiempo transcurrido desde el inicio del turno previsto.

### Cómo interpretar este panel

Una caída sostenida en la tasa de presencia de los últimos 30 días que no está relacionada con vacaciones ni festivos programados es una señal que conviene investigar a nivel de equipo. Si la caída se concentra en una sola sucursal, el problema es probablemente local; si afecta a toda la entidad, puede indicar un factor más amplio.

## Panel de eficiencia

Este panel muestra la distribución de los índices de eficiencia del equipo y permite identificar tanto a los empleados con mayor rendimiento horario como a los que presentan desviaciones recurrentes.

**Distribución por rangos.** Gráfica que agrupa a los empleados según su índice de eficiencia actual en los rangos definidos (alto, aceptable, moderado, bajo). Permite ver de forma inmediata si la mayor parte del equipo está en rangos saludables o si hay una concentración de empleados con eficiencia baja.

**Evolución del índice medio.** Tendencia del índice de eficiencia promedio del equipo o la sucursal durante el periodo seleccionado. Un descenso sostenido puede indicar problemas de dimensionamiento de turnos, alta rotación o cambios en las condiciones operativas.

**Empleados con mayor desviación.** Lista de los empleados cuyas horas reales se alejan más de las planificadas en el periodo, ordenados por magnitud de la desviación.

### Qué acciones se derivan

Cuando un empleado aparece de forma recurrente en la lista de mayor desviación, conviene revisar si el problema es de comportamiento o de planificación. A veces la desviación no indica un problema del empleado sino que el turno asignado no se ajusta a la carga de trabajo real.

## Panel de costes

Este panel traduce los datos de asistencia en información económica comparativa. Es el panel más orientado al control de gestión y a la dirección.

**Comparativa de coste por sucursal.** Vista comparativa del coste real acumulado de cada sucursal durante el periodo seleccionado, frente al coste planificado. Permite identificar qué centros están dentro del presupuesto y cuáles presentan sobrecoste.

**Coste por hora real trabajada.** Indicador que normaliza el coste en función de las horas efectivamente trabajadas, lo que permite comparar sucursales con distinto número de empleados o distintas jornadas de forma equitativa.

**Evolución temporal del coste.** Gráfica del coste real acumulado por semana o mes, con la línea de coste planificado como referencia. Las semanas con desviación significativa quedan visualmente resaltadas.

**Detalle por empleado.** Vista de tabla con el coste real, el coste planificado y la desviación de cada empleado en el periodo.

### Qué acciones se derivan

Una sucursal con coste por hora real trabajada consistentemente superior a las demás merece una revisión de su gestión de horas extra y de la disciplina horaria del equipo. El panel no explica el motivo, pero señala dónde buscar.

## Panel de anomalías

Este panel centraliza la información sobre empleados con el indicador de anomalía activo y ofrece al Manager y al Owner una vista de las alertas pendientes de revisión.

**Empleados con indicador activo.** Lista de todos los empleados cuyo patrón de fichaje ha activado la detección de anomalías, con la fecha en que se activó el indicador y el tipo de patrón detectado (regularidad temporal, geolocalización estática u otros).

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La gestión del estado de revisión de cada alerta (marcar como revisada, archivar, consultar historial de alertas resueltas) no está disponible en la versión actual. En una versión futura, el panel permitirá distinguir entre alertas pendientes y alertas ya gestionadas y llevará un registro completo del ciclo de vida de cada indicador.

### Qué acciones se derivan

El procedimiento de actuación ante una alerta activa está descrito en detalle en el artículo sobre detección de anomalías. Desde este panel, el primer paso es siempre acceder al historial completo del empleado antes de tomar ninguna acción.

> **Importante:** El panel de anomalías es visible exclusivamente para los roles de Manager y Owner. No es accesible para supervisores ni para los propios empleados.

## Exportación de datos de los paneles

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La exportación de los datos de los paneles de mando en formato CSV o PDF no está disponible en la versión actual. Los paneles son consultables en el backoffice, pero la información no puede descargarse. Esta capacidad de exportación está prevista en el roadmap de la plataforma.

## Permisos de acceso a los dashboards por rol

| Panel | Owner | Manager | Supervisor |
|---|---|---|---|
| KPIs de asistencia | Acceso completo (toda la entidad) | Acceso a sus sucursales | Acceso a su equipo directo |
| Eficiencia | Acceso completo | Acceso a sus sucursales | Solo indicadores básicos |
| Costes | Acceso completo | Acceso a sus sucursales | Sin acceso |
| Anomalías | Acceso completo | Acceso a sus sucursales | Sin acceso |

> **Nota:** Los permisos de acceso indicados son los que el sistema aplica por defecto. El Owner puede ajustar el nivel de acceso de cada rol dentro de los límites que permite la configuración de la plataforma. Consulte el artículo sobre roles y permisos para más detalle.

## Artículos relacionados

- [Qué es la inteligencia operativa](49-que-es-la-inteligencia-operativa.md)
- [El patrón de comportamiento del empleado](50-patron-de-comportamiento.md)
- [Índice de fiabilidad](51-indice-de-fiabilidad.md)
- [Índice de eficiencia](52-indice-de-eficiencia.md)
- [Puntuación de promoción](53-puntuacion-de-promocion.md)
- [Análisis de costes](54-analisis-de-costes.md)
- [Detección de anomalías](55-deteccion-de-anomalias.md)

# Informes de tareas

CheckBiz360 ofrece dos vías para analizar la ejecución de tareas: las métricas que se consultan directamente en el backoffice y el **informe de tareas en Excel**, que se genera bajo demanda y queda archivado en el histórico de informes.

---

## Métricas visibles en el backoffice

Desde el listado y el detalle de tareas, managers y owners pueden consultar:

- **Tareas por estado:** cuántas hay en borrador, asignadas, en progreso, completadas, validadas, rechazadas o canceladas, para toda la entidad o filtradas por sucursal.
- **Tareas por empleado:** las tareas asignadas a cada persona con su estado actual, lo que permite identificar cargas de trabajo desequilibradas o tareas atascadas a la espera de validación.
- **Cumplimiento temporal:** para cada tarea, si va a tiempo, en riesgo, vencida, o si se completó dentro o fuera de plazo.
- **Valoraciones registradas:** la puntuación otorgada al empleado queda visible en el detalle de la tarea y en su perfil.

> **Nota:** las métricas reflejan el estado actual conforme empleados y responsables interactúan con las tareas.

---

## Informe de tareas en Excel

El informe de tareas se genera desde la sección **Informes** del backoffice y se descarga en formato **Excel (XLSX)**.

### Cómo generarlo

1. Acceda a **Informes** en el menú lateral.
2. Pulse el botón para generar un informe nuevo.
3. En **Tipo de informe**, seleccione *Informe de tareas*. El formato queda fijado a Excel (XLSX), que es el único disponible para este informe.
4. Seleccione el **periodo** (fecha de inicio y fin).
5. Si lo necesita, filtre por **sucursal** y por **estado** de las tareas.
6. Genere el informe. Cuando esté listo, aparecerá en el histórico de informes, desde donde puede descargarlo.

> **Importante:** el periodo del informe se aplica sobre la **fecha límite** de cada tarea, no sobre su fecha de creación. Un informe de julio incluye las tareas que vencían en julio, aunque se crearan en junio.

### Qué contiene

La hoja **Tareas** lleva **una fila por tarea y persona asignada**, agrupadas por tarea. Una tarea de tres personas ocupa tres filas, y las columnas de la tarea (Empresa, Centro, Cliente si lo hay, Título, Estado, Prioridad, Inicio, Fin, los tiempos, Completada por, Valoración y Nº evidencias) se repiten en cada una, de modo que al filtrar por una persona se sigue viendo de qué tarea era cada fila. Cada tarea cierra con una fila **Total {tarea}** y el informe, con **Total del periodo**. El signo **−** del margen izquierdo de Excel pliega las personas de una tarea y deja solo su total.

Es el formato pensado para que un contable trabaje con él: una fila por persona y tarea permite sumar, filtrar y hacer tablas dinámicas por persona, por puesto, por cliente o por complemento sin deshacer nada a mano.

Las columnas de la persona:

| Columna | Qué es |
|---|---|
| **Persona** | Quién estaba asignado. |
| **Puesto** | Con qué puesto trabajó en esa tarea: el elegido al asignarla o, si no se eligió, su predeterminado. Ver [Varios puestos para la misma persona](../02-empleados/140-varios-puestos-por-persona.md). |
| **Horas de la persona** | Sus horas en la tarea. |
| **Origen de las horas** | *Fichajes*, si la persona fichó en la tarea; *Reloj de la tarea*, si no hubo fichajes y las horas salen de cuándo se inició y se terminó, menos las pausas. Si una jornada quedó sin salida, lo dice: *Fichajes · 1 sin salida*. |
| **Precio por hora** | El precio del puesto con el que trabajó, tal como estaba el día del fichaje. |
| **Coste puesto** | Horas por precio por hora. |
| **Complementos** | Los que cobró en esa tarea, con su valor entre paréntesis. Ver [Complementos](../02-empleados/141-complementos.md). |
| **Complementos (importe)** | Lo que suman. |
| **Coste persona** | Coste del puesto más complementos. |

La fila **Total** de cada tarea suma las horas y el coste de su gente, los complementos, el material si tiene inventario y el **coste bruto** de la tarea.

Si alguna tarea del informe tiene cliente, se añade la columna **Cliente** detrás de **Centro** (ver [El cliente en la tarea](../17-cartera-de-clientes/119-el-cliente-en-la-tarea.md)).

Las columnas de dinero las ve quien puede generar el informe: el propietario y los administradores. Los importes **no llevan símbolo de moneda**: la moneda de su empresa se indica una vez en la cabecera de cada hoja (*Moneda: EUR*) y se configura en [Configuración de entidad](../08-sucursales-y-entidad/61-configuracion-de-entidad.md#datos-de-la-empresa). Una persona sin precio en su puesto deja el coste vacío, no a cero.

**Completada por** dice quién cerró la tarea; si se cerró desde el panel, lleva *(desde administración)*, y el inicio y el fin son las horas que se indicaron al cerrarla. Ver [cerrarla desde administración](./127-quien-termina-la-tarea-y-cierre-desde-administracion.md).

Conviene leer bien las columnas de tiempo:

| Columna | Qué mide |
|---|---|
| **Tiempo invertido (h)** | El tiempo transcurrido entre el inicio y el fin de la tarea. No es tiempo trabajado: una tarea que se empieza el viernes y se termina el lunes incluye el fin de semana. |
| **En pausa (h)** | La suma de las pausas de la tarea. |
| **Nº pausas** | Cuántas veces se pausó. |
| **Tiempo invertido sin pausas (h)** | El tiempo invertido menos el tiempo en pausa. Descuenta las pausas que alguien registró, no las interrupciones que nadie marcó. |

Una tarea que todavía no se ha iniciado deja las columnas de pausa vacías. Si una tarea está en pausa al generar el informe, la pausa abierta cuenta hasta ese momento.

### Las hojas «Por persona» y «Complementos»

El fichero trae dos hojas más, que salen de las mismas filas:

- **Por persona**: el resumen del periodo, una fila por persona: cuántas tareas, horas, con qué puestos, coste del puesto, complementos (importe), coste total y, en **Complementos del periodo**, qué complementos cobró y cuántas veces. Es la hoja para preparar la nómina o cotejar con la gestoría.
- **Complementos**: la traza. Una línea por complemento cobrado, con la tarea, el centro, el cliente, la persona, su puesto, el complemento, su tipo y su valor, las horas, el precio por hora, el **importe** y el **origen**: el fichaje de entrada del que sale o, si la tarea no tuvo fichajes, la asignación de la tarea. Al pie, cómo se calcula cada tipo. Si en el periodo no se cobró ninguno, la hoja lo dice.

### Incidencias

Si alguna tarea del periodo tuvo una [incidencia](./125-incidencia-en-la-tarea.md), la hoja **Tareas** gana la columna **Incidencia**: *Abierta* (en rojo) o *Resuelta · Replanificada*, *Cancelada* o *Resuelta*.

El fichero trae además siempre la hoja **Incidencias**, con una fila por incidencia, abierta o resuelta: Centro, Cliente, Tarea, Estado de la tarea, Marcada, Marcada por, Nota, Archivo, Incidencia, Resolución, Resuelta, Resuelta por y Nota de resolución. Si en el periodo no hubo ninguna, la hoja lo dice.

### Material de cada tarea

Si su empresa tiene contratado el [inventario](../16-inventario/100-que-es-el-inventario.md) (o lo está probando), el informe responde además a una pregunta que el parte de trabajo no suele contestar: **qué material se gastó en cada servicio y cuánto costó**.

La hoja de tareas gana tres columnas al final:

| Columna | Qué es |
|---|---|
| **Material** | Lo consumido en la tarea: cada artículo con su cantidad, y los equipos por su ejemplar. |
| **Sin cuadrar** | Lo que salió y nadie ha declarado ni devuelto. Es lo que conviene revisar antes de validar. |
| **Coste material** | Lo consumido por su coste unitario. Vacío si ningún artículo tiene coste en su ficha. Va en la fila **Total** de la tarea. |

Y el fichero trae una hoja más, **Material**, con una fila por tarea y artículo o ejemplar: almacén de donde salió, cantidades reservada, salida, consumida, devuelta y sin cuadrar, coste, y para los equipos su tramo de reserva y su uso. Es la hoja para filtrar o hacer tablas dinámicas.

Sin el inventario, el informe es exactamente el de siempre.

### Si no hay resultados

Si ninguna tarea cumple los filtros seleccionados, el sistema lo indica y no genera un fichero vacío. Amplíe el periodo o revise los filtros de sucursal y estado.

---

## Histórico de informes

Todos los informes generados quedan listados en la sección **Informes**, identificados por tipo (tareas o registro de jornada) y por formato (Excel o PDF), con la fecha de generación y el periodo cubierto. Desde ahí se descargan tantas veces como haga falta sin volver a generarlos.

---

## Análisis agregado del rendimiento

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

Las métricas agregadas calculadas por la plataforma —tasa de completitud, tiempo medio de resolución, tasa de rechazo y valoración media por periodo— y las comparativas automáticas entre sucursales están planificadas para una versión futura. Hoy esos análisis pueden construirse a partir del informe en Excel.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Varios puestos para la misma persona](../02-empleados/140-varios-puestos-por-persona.md) | De dónde sale la columna Puesto y su precio por hora |
| [Complementos](../02-empleados/141-complementos.md) | Qué son, los tres tipos y dónde se eligen |
| [Valoración del trabajador](./46-valoracion-del-trabajador.md) | Cómo se generan las puntuaciones de desempeño |
| [Prioridades y fechas límite](./44-prioridades-y-fechas-limite.md) | Configuración de plazos que afectan al seguimiento |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Significado de los estados y del cumplimiento temporal |
| [Tipos de informe](../11-informes-y-exportacion/76-tipos-de-informe.md) | Todos los informes disponibles en la plataforma |
| [Exportar datos](../11-informes-y-exportacion/78-exportar-a-excel-y-csv.md) | Formatos de exportación disponibles |

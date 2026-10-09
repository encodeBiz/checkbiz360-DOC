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

Una fila por tarea, con estas columnas: Empresa, Centro, Título, Estado, Prioridad, Inicio, Fin, **Tiempo invertido (h)**, **En pausa (h)**, **Nº pausas**, **Tiempo invertido sin pausas (h)**, Equipo, Valoración y Nº evidencias.

Conviene leer bien las columnas de tiempo:

| Columna | Qué mide |
|---|---|
| **Tiempo invertido (h)** | El tiempo transcurrido entre el inicio y el fin de la tarea. No es tiempo trabajado: una tarea que se empieza el viernes y se termina el lunes incluye el fin de semana. |
| **En pausa (h)** | La suma de las pausas de la tarea. |
| **Nº pausas** | Cuántas veces se pausó. |
| **Tiempo invertido sin pausas (h)** | El tiempo invertido menos el tiempo en pausa. Descuenta las pausas que alguien registró, no las interrupciones que nadie marcó. |

Una tarea que todavía no se ha iniciado deja las columnas de pausa vacías. Si una tarea está en pausa al generar el informe, la pausa abierta cuenta hasta ese momento.

### Material de cada tarea

Si su empresa tiene contratado el [inventario](../16-inventario/100-que-es-el-inventario.md) (o lo está probando), el informe responde además a una pregunta que el parte de trabajo no suele contestar: **qué material se gastó en cada servicio y cuánto costó**.

La hoja de tareas gana tres columnas al final:

| Columna | Qué es |
|---|---|
| **Material** | Lo consumido en la tarea: cada artículo con su cantidad, y los equipos por su ejemplar. |
| **Sin cuadrar** | Lo que salió y nadie ha declarado ni devuelto. Es lo que conviene revisar antes de validar. |
| **Coste material (€)** | Lo consumido por su coste unitario. Vacío si ningún artículo tiene coste en su ficha. |

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
| [Valoración del trabajador](./46-valoracion-del-trabajador.md) | Cómo se generan las puntuaciones de desempeño |
| [Prioridades y fechas límite](./44-prioridades-y-fechas-limite.md) | Configuración de plazos que afectan al seguimiento |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Significado de los estados y del cumplimiento temporal |
| [Tipos de informe](../11-informes-y-exportacion/76-tipos-de-informe.md) | Todos los informes disponibles en la plataforma |
| [Exportar datos](../11-informes-y-exportacion/78-exportar-a-excel-y-csv.md) | Formatos de exportación disponibles |

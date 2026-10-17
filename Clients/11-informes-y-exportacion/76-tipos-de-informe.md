# Tipos de informe disponibles en CheckBiz360

CheckBiz360 centraliza la información operativa de su empresa en dos formas distintas, y conviene no confundirlas:

- **Informes descargables**, que se generan bajo demanda desde la sección **Informes**, quedan archivados en el histórico y se descargan como fichero. Son tres: el **informe de asistencia** (PDF o Excel), el **informe de tareas** (Excel) y el informe **«Equipos y EPIs»** (Excel, con el complemento de inventario). Con el inventario contratado, el de tareas incluye además el material de cada tarea, y el inventario tiene su propio **informe de consumo**.
- **Análisis en pantalla**, que se consultan en el panel operativo y en las fichas de sucursal y empleado: puntualidad, costes y anomalías. No generan fichero descargable en la versión actual.

Esta guía describe cada uno y los roles que tienen acceso.

---

## Informe de asistencia

El informe de asistencia es el documento base del módulo. Recoge los datos de presencia de los empleados en un periodo determinado y permite obtener una visión completa del comportamiento horario del equipo.

### Qué incluye

- Listado de presencias y ausencias por empleado y día.
- Horas trabajadas totales por empleado en el periodo seleccionado.
- Desglose por turno, sucursal o periodo.
- Estado de cada jornada: completa, ausencia justificada, ausencia sin justificar, jornada parcial.
- En los días con más de una entrada y salida (jornada partida, varios servicios seguidos): la **jornada**, de la primera entrada a la última salida, y los **huecos entre turnos**, medidos de los fichajes. El informe enseña lo medido; qué se paga lo decide la empresa.

> **Importante:** el informe recoge al personal de **plantilla**. Los empleados marcados como **colaboradores** no aparecen, porque el registro horario es una obligación de la relación laboral y no se aplica a un autónomo que factura a la empresa. Los empleados sin tipo de relación registrado se siguen incluyendo. Consulte [Roles y niveles de responsabilidad](../02-empleados/07-roles-y-niveles-de-responsabilidad.md#tipo-de-relación-interno-frente-a-colaborador).

Si no hay ningún fichaje que cumpla los filtros, el sistema lo indica y no genera el fichero.

### Para qué sirve

Es el informe más utilizado para la supervisión operativa diaria y para el cálculo de variables salariales como horas extras o descuentos por ausencia. También es la base del informe de cumplimiento normativo descrito en el artículo [79](./79-informe-de-cumplimiento-normativo.md).

### Acceso por rol

| Rol | Acceso |
|---|---|
| Owner | Todas las sucursales y todos los empleados |
| Manager | Empleados de las sucursales que gestiona |
| Supervisor | Empleados de su equipo directo, si el manager lo ha habilitado |
| Worker | Solo sus propios datos de asistencia desde la app |

---

## Análisis en pantalla: puntualidad, costes y anomalías

Estas tres lecturas **no son informes descargables**: se consultan en el panel de Operación y en las fichas de sucursal y empleado. La exportación de sus datos está en el roadmap.

### Puntualidad y desviaciones de horario

Recoge las tardanzas, las salidas anticipadas y la desviación acumulada entre las horas previstas y las efectivamente trabajadas. Permite distinguir si la impuntualidad es puntual o un patrón, y si es de una persona o de un centro entero.

### Costes

Cruza la asistencia con la tarifa horaria configurada en la vinculación de cada empleado con su sucursal: coste por hora trabajada, por jornada, por rendimiento y acumulado del periodo.

Contiene información sensible y solo es accesible para **Owner** y **Manager**. Requiere que las tarifas estén configuradas: sin ellas, los indicadores económicos aparecen vacíos.

### Anomalías

Reúne los registros que el sistema ha identificado como potencialmente irregulares —precisión temporal excesiva, geolocalización estática, dispositivos no autorizados— junto con las correcciones manuales realizadas sobre fichajes, con su autor, su momento y su motivo.

Afloran en la pestaña de **Análisis** del panel, que ordena la lectura de menos a más señalable: primero el proceso y la configuración, al final las personas. Exclusivo de **Owner** y **Manager**.

---

## Informe de tareas

El informe de tareas recoge las tareas del periodo con su estado y su cumplimiento de plazo. Es un **informe descargable en Excel (XLSX)**.

### Qué incluye

- Las tareas cuya **fecha límite** cae dentro del periodo seleccionado, con su estado y su cumplimiento temporal.
- El tiempo de cada tarea: tiempo invertido, tiempo en pausa, número de pausas y tiempo invertido sin pausas. Se explican en [Informes de tareas](../06-tareas/48-informes-de-tareas.md#qué-contiene).
- Filtros por sucursal y por estado de la tarea.
- Los datos necesarios para calcular en la hoja de cálculo lo que se necesite: completadas frente a asignadas, vencidas, rechazadas.

- Con el [inventario](../16-inventario/100-que-es-el-inventario.md) contratado: el material consumido por tarea, su coste y lo que quedó sin cuadrar, más una hoja de detalle por artículo. Ver [Informes de tareas](../06-tareas/48-informes-de-tareas.md#material-de-cada-tarea).

> **Nota:** las métricas agregadas ya calculadas —porcentaje de completitud, tiempo medio de resolución, valoración media— están en el roadmap. Hoy el informe entrega el detalle y el cálculo se hace en la hoja.

### Para qué sirve

Complementa el control de presencia con datos sobre la actividad real realizada durante la jornada. Permite evaluar el rendimiento del equipo con criterios objetivos y documentados.

### Acceso por rol

| Rol | Acceso |
|---|---|
| Owner | Todas las sucursales |
| Manager | Sucursales que gestiona |
| Supervisor | Su equipo directo, si el manager lo habilita |
| Worker | Solo sus propias tareas desde la app |

---

## Informe de consumo (inventario)

Exclusivo del complemento de inventario. Responde a **dónde se va el material y cuánto cuesta**: agrupa el consumo de un periodo por artículo, tarea, empleado, sucursal o almacén, valorado al coste de cada artículo, y se exporta a CSV junto con el libro de movimientos. Se abre desde la sección Inventario. Ver [Informe de consumo y movimientos](../16-inventario/103-informe-de-consumo-y-movimientos.md).

---

> **Nota:** los análisis de costes y anomalías contienen información especialmente sensible. Asegúrese de que solo los roles con acceso autorizado tienen credenciales activas en la plataforma. Revise periódicamente los usuarios con rol de Manager u Owner en la sección de gestión de equipo.

---

## Informe «Equipos y EPIs»

Se lista siempre en Informes; sin el complemento de inventario aparece en rojo y explica qué es y cómo activarlo. Es la prueba para una inspección de trabajo, en dos hojas: **Entregas** (qué se entregó a cada trabajador, con qué documentos y versión, quién lo entregó, cómo lo confirmó y si la firma fue verificada, cuándo y cómo lo devolvió) y **Equipos y revisiones** (cada ejemplar con su estado, quién lo tiene y cada papel con su resultado y caducidad). Ver [Equipos: documentos, revisiones y entregas](../16-inventario/104-equipos-documentos-revisiones-y-entregas.md).

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Generar y filtrar informes](./77-generar-y-filtrar-informes.md) | Pasos para generar un informe con filtros personalizados |
| [Exportar datos](./78-exportar-a-excel-y-csv.md) | Formatos de exportación y consideraciones de uso |
| [Informe de cumplimiento normativo](./79-informe-de-cumplimiento-normativo.md) | El informe para el RDL 8/2019 y la Inspección de Trabajo |
| [Informes automáticos](./80-informes-automaticos.md) | Envío periódico por email: planificado, no disponible |
| [Detección de anomalías](../07-inteligencia-operativa/55-deteccion-de-anomalias.md) | Cómo funciona el mecanismo de detección automática |

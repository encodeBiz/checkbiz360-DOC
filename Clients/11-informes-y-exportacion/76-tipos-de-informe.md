# Tipos de informe disponibles en CheckBiz360

CheckBiz360 centraliza la información operativa de su empresa en dos formas distintas, y conviene no confundirlas:

- **Informes descargables**, que se generan bajo demanda desde la sección **Informes**, quedan archivados en el histórico y se descargan como fichero. Hoy son dos: el **informe de asistencia** (PDF o Excel) y el **informe de tareas** (Excel).
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
- Filtros por sucursal y por estado de la tarea.
- Los datos necesarios para calcular en la hoja de cálculo lo que se necesite: completadas frente a asignadas, vencidas, rechazadas.

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

> **Nota:** los análisis de costes y anomalías contienen información especialmente sensible. Asegúrese de que solo los roles con acceso autorizado tienen credenciales activas en la plataforma. Revise periódicamente los usuarios con rol de Manager u Owner en la sección de gestión de equipo.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Generar y filtrar informes](./77-generar-y-filtrar-informes.md) | Pasos para generar un informe con filtros personalizados |
| [Exportar datos](./78-exportar-a-excel-y-csv.md) | Formatos de exportación y consideraciones de uso |
| [Informe de cumplimiento normativo](./79-informe-de-cumplimiento-normativo.md) | El informe para el RDL 8/2019 y la Inspección de Trabajo |
| [Informes automáticos](./80-informes-automaticos.md) | Envío periódico por email: planificado, no disponible |
| [Detección de anomalías](../07-inteligencia-operativa/55-deteccion-de-anomalias.md) | Cómo funciona el mecanismo de detección automática |

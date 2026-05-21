# Tipos de informe disponibles en CheckBiz360

CheckBiz360 ofrece un módulo de informes que centraliza toda la información operativa de su empresa en documentos estructurados y exportables. Cada tipo de informe responde a una necesidad concreta: desde el cumplimiento legal hasta el análisis de costes o la detección de irregularidades. Esta guía describe los cinco tipos de informe disponibles y los roles que tienen acceso a cada uno.

---

## Informe de asistencia

El informe de asistencia es el documento base del módulo. Recoge los datos de presencia de los empleados en un periodo determinado y permite obtener una visión completa del comportamiento horario del equipo.

### Qué incluye

- Listado de presencias y ausencias por empleado y día.
- Horas trabajadas totales por empleado en el periodo seleccionado.
- Desglose por turno, sucursal o periodo.
- Estado de cada jornada: completa, ausencia justificada, ausencia sin justificar, jornada parcial.

### Para qué sirve

Es el informe más utilizado para la supervisión operativa diaria y para el cálculo de variables salariales como horas extras o descuentos por ausencia. También es la base del informe de cumplimiento normativo descrito en el artículo 79.

### Acceso por rol

| Rol | Acceso |
|---|---|
| Owner | Todas las sucursales y todos los empleados |
| Manager | Empleados de las sucursales que gestiona |
| Supervisor | Empleados de su equipo directo, si el manager lo ha habilitado |
| Worker | Solo sus propios datos de asistencia desde la app |

---

## Informe de puntualidad

El informe de puntualidad analiza las desviaciones entre el horario previsto de cada empleado y los fichajes reales registrados.

### Qué incluye

- Tardanzas: fichajes de entrada producidos después de la hora prevista, con el tiempo de retraso exacto.
- Salidas anticipadas: fichajes de salida antes de que finalizara el turno asignado.
- Desviaciones de horario: diferencia acumulada entre horas previstas y horas efectivamente trabajadas en el periodo.
- Frecuencia de incidencias: número de veces que se ha producido cada tipo de desviación por empleado.

### Para qué sirve

Permite identificar patrones de impuntualidad individuales o sistémicos, distinguir si las tardanzas son puntuales o recurrentes y tomar decisiones de gestión con datos objetivos.

### Acceso por rol

El acceso es equivalente al del informe de asistencia. El Worker puede consultar sus propios datos de puntualidad desde la app, pero no puede ver los de otros empleados.

---

## Informe de costes

El informe de costes cruza los datos de asistencia con la información salarial configurada en la plataforma para calcular el coste real de las horas trabajadas.

### Qué incluye

- Coste por empleado en el periodo seleccionado.
- Coste por sucursal y comparativa entre sucursales.
- Coste de horas extra frente a horas ordinarias.
- Evolución del coste mes a mes cuando se selecciona un rango de varios periodos.

### Para qué sirve

Facilita la toma de decisiones sobre dimensionamiento de plantilla, asignación de turnos y control presupuestario. Es especialmente útil para presentar a dirección o a una gestoría financiera.

### Acceso por rol

Este informe contiene datos salariales sensibles. Solo tienen acceso los roles de Owner y Manager. Los supervisores y workers no pueden acceder al informe de costes.

---

## Informe de anomalías

El informe de anomalías reúne los registros que el sistema ha identificado como potencialmente irregulares, basándose en los mecanismos de detección automática de la plataforma.

### Qué incluye

- Fichajes marcados como sospechosos por precisión temporal excesiva o geolocalización estática.
- Registros procedentes de dispositivos no autorizados en la configuración de geocerca.
- Empleados con el indicador de anomalía activo y resumen de los patrones detectados.
- Correcciones manuales realizadas sobre fichajes: quién las realizó, cuándo y con qué justificación.

### Para qué sirve

Proporciona al responsable una vista consolidada de todas las señales de alerta operativa, sin necesidad de revisar empleado por empleado. Es la herramienta de partida para cualquier investigación de irregularidades.

### Acceso por rol

Exclusivo de Owner y Manager. Los supervisores no tienen acceso al informe de anomalías.

---

## Informe de tareas

El informe de tareas ofrece métricas de desempeño operativo basadas en las tareas asignadas y su nivel de completitud.

### Qué incluye

- Porcentaje de tareas completadas frente a tareas asignadas por empleado y periodo.
- Tiempo medio de resolución de tareas por empleado o por tipo de tarea.
- Valoraciones registradas por el manager al validar cada tarea completada.
- Tareas vencidas sin completar y tareas rechazadas.

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

> **Nota:** Los informes de costes y anomalías contienen información especialmente sensible. Asegúrese de que solo los roles con acceso autorizado tienen credenciales activas en la plataforma. Revise periódicamente los usuarios con rol de Manager u Owner en la sección de gestión de equipo.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Generar y filtrar informes](./77-generar-y-filtrar-informes.md) | Pasos para generar un informe con filtros personalizados |
| [Exportar a Excel y CSV](./78-exportar-a-excel-y-csv.md) | Formatos de exportación y consideraciones de uso |
| [Informe de cumplimiento normativo](./79-informe-de-cumplimiento-normativo.md) | El informe para el RDL 8/2019 y la Inspección de Trabajo |
| [Informes automáticos](./80-informes-automaticos.md) | Configurar el envío periódico de informes por email |
| [Detección de anomalías](../07-inteligencia-operativa/55-deteccion-de-anomalias.md) | Cómo funciona el mecanismo de detección automática |

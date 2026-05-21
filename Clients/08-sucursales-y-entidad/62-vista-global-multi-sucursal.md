# Vista global multi-sucursal

El panel global de CheckBiz360 es la herramienta de supervisión consolidada para organizaciones que operan en varias sucursales. Desde una única pantalla, los responsables pueden ver el estado de asistencia de toda la organización en tiempo real, comparar el rendimiento entre centros, detectar anomalías y exportar datos consolidados sin necesidad de navegar sucursal por sucursal. Este artículo describe las funcionalidades del panel global y cómo sacarles el mayor partido.

## A quién está dirigida esta vista

La vista global está concebida para perfiles que supervisan operaciones a escala: directores de operaciones con varias tiendas, responsables de RRHH de empresas multi-centro, gerentes regionales o cualquier persona que necesite una visión de conjunto antes de entrar en el detalle de cada sucursal.

Un ejemplo de caso de uso típico es el de un director de operaciones con 20 tiendas que, a las 9:30 de la mañana, quiere saber en menos de un minuto cuántas tiendas tienen empleados que todavía no han fichado, qué centros están operando con el personal completo y en cuál hay una anomalía crítica que requiere atención inmediata.

## Cómo acceder al panel global

1. Acceda al backoffice web e inicie sesión con un rol de **Owner** o **Manager** con acceso a múltiples sucursales.
2. En el menú lateral, seleccione **Panel global** o **Dashboard**.
3. El sistema cargará automáticamente la vista consolidada con los datos del día en curso.

## Vista de asistencia consolidada hoy

La sección principal del panel global muestra, para el día en curso, el estado de asistencia de todos los empleados de todas las sucursales a las que tiene acceso el usuario. La información se organiza por sucursal y permite identificar de forma inmediata la situación de cada centro.

### KPIs globales

En la parte superior del panel se muestran los indicadores clave de asistencia del día:

- **Empleados presentes**: número y porcentaje de empleados que han fichado entrada y están actualmente en turno.
- **Ausencias**: empleados que debían fichar y no lo han hecho. Se distingue entre ausencias justificadas (registradas con permiso aprobado) y no justificadas (sin registro ni justificación).
- **Anomalías**: fichajes marcados automáticamente por el sistema como sospechosos o irregulares, incluyendo entradas tardías, salidas anticipadas, fichajes fuera de geocerca y jornadas incompletas.
- **Pausas activas**: empleados que se encuentran en pausa en este momento.

Los KPIs se actualizan en tiempo real a medida que los empleados van fichando a lo largo del día.

## Filtros por sucursal

El panel global permite filtrar los datos para visualizar únicamente las sucursales que le interesen en cada momento. Los filtros disponibles son:

- **Por sucursal específica**: seleccione una o varias sucursales del listado para ver únicamente sus datos.
- **Por región o grupo**: si su organización ha agrupado las sucursales por regiones o tipologías, puede filtrar por esa agrupación.
- **Por estado**: active el filtro de anomalías para ver únicamente las sucursales con incidencias activas.

Los filtros son acumulables y persistentes durante la sesión. Si abandona el panel global y regresa, los filtros aplicados se mantendrán.

## Comparativas entre sucursales

La sección de comparativas permite analizar el rendimiento relativo de las sucursales a lo largo del tiempo. Las métricas disponibles para comparación incluyen:

### Coste y eficiencia

- **Coste horario total**: suma del coste de las horas trabajadas por todos los empleados de cada sucursal en el periodo seleccionado.
- **Coste medio por empleado**: coste horario dividido entre el número de empleados activos en la sucursal.
- **Horas trabajadas vs. horas previstas**: porcentaje de cumplimiento del horario planificado.

### Asistencia y puntualidad

- **Tasa de puntualidad**: porcentaje de fichajes de entrada realizados dentro del margen de tolerancia configurado.
- **Tasa de ausencia**: porcentaje de ausencias sobre el total de jornadas previstas en el periodo.
- **Anomalías por empleado**: número medio de anomalías por empleado en el periodo, útil para identificar sucursales con problemas sistemáticos de cumplimiento.

Las comparativas pueden visualizarse en formato de tabla o de gráfico de barras. El periodo de análisis es configurable: hoy, esta semana, este mes o un rango personalizado.

> **Aviso:** Las comparativas de coste son más precisas cuando todos los empleados tienen el coste horario correctamente configurado en sus fichas. Si algún empleado no tiene coste configurado, esas horas se computan como coste cero y pueden distorsionar las métricas de la sucursal.

## Exportación de datos consolidados

Desde el panel global puede exportar un informe con los datos de todas las sucursales seleccionadas en un único archivo. El proceso es el siguiente:

1. Aplique los filtros de sucursal y periodo que desee incluir en el informe.
2. Pulse el botón **Exportar** en la esquina superior derecha del panel.
3. Seleccione el formato de exportación: CSV para análisis en hojas de cálculo o PDF para informes ejecutivos.
4. El sistema generará el archivo y lo descargará automáticamente. Para volúmenes grandes de datos (más de 90 días o más de 50 sucursales), la generación puede tardar unos segundos y el archivo se enviará también por correo electrónico a la dirección del usuario.

El informe consolidado incluye, para cada sucursal, el resumen de horas trabajadas, ausencias, anomalías y coste del periodo seleccionado.

## Alertas activas en el panel global

El panel global incorpora una sección de alertas que agrupa todas las incidencias activas en tiempo real de toda la organización. Desde aquí puede:

- Ver qué sucursales tienen alertas sin resolver.
- Acceder directamente al registro problemático con un solo clic.
- Asignar la gestión de una alerta a un responsable concreto.

---

> **Nota de rol:** El panel global está disponible para los roles **Owner** y **Manager**. El Owner ve todas las sucursales de la entidad. El Manager ve únicamente las sucursales a las que está asignado. El rol **Supervisor** no tiene acceso al panel global; accede únicamente a la vista de su sucursal.

## Artículos relacionados

- [Crear y gestionar sucursales](57-crear-y-gestionar-sucursales.md)
- [Asignar empleados a sucursales](60-asignar-empleados-a-sucursales.md)
- [Configuración de entidad](61-configuracion-de-entidad.md)
- [Tipos de notificación](../09-notificaciones/63-tipos-de-notificacion.md)
- [Alertas para responsables](../09-notificaciones/66-alertas-para-responsables.md)

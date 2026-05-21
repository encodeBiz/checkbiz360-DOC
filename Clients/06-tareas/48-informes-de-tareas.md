# Informes de tareas

El backoffice de CheckBiz360 muestra estadísticas básicas sobre la ejecución de tareas directamente en el panel del módulo. Estos datos permiten a los responsables hacer un seguimiento del trabajo asignado y detectar patrones de incumplimiento sin necesidad de herramientas externas.

---

## Métricas visibles en el backoffice (V1)

Desde el panel de tareas del backoffice, los managers y owners pueden consultar:

- **Número de tareas por estado:** Cuántas tareas están pendientes, en curso, completadas, validadas o rechazadas en un momento dado, para toda la entidad o filtradas por sucursal.
- **Tareas por empleado:** Vista de las tareas asignadas a cada empleado con su estado actual, lo que permite identificar a empleados con alta carga de trabajo pendiente o con tareas bloqueadas en validación.
- **Indicador de cumplimiento temporal:** Para cada tarea, el sistema registra si fue completada dentro del plazo establecido o después (`timeComplianceStatus`). Este indicador es visible en el detalle de la tarea.
- **Valoraciones registradas:** Si se ha registrado una puntuación al validar una tarea, esa valoración queda visible en el detalle de la tarea y en el perfil del empleado.

> **Nota:** Las métricas se actualizan en tiempo real conforme los empleados y responsables interactúan con las tareas.

---

## Informes exportables de tareas

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

Los informes avanzados con exportación en formato CSV o Excel, junto con métricas agregadas como tasa de completitud, tiempo medio de resolución, tasa de rechazo y valoraciones medias por periodo, están planificados para una versión futura. Cuando estén disponibles, permitirán generar análisis de rendimiento del equipo, comparativas entre sucursales y exportaciones de datos para evaluaciones de desempeño.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Valoración del trabajador](./46-valoracion-del-trabajador.md) | Cómo se generan las puntuaciones de desempeño |
| [Prioridades y fechas límite](./44-prioridades-y-fechas-limite.md) | Configuración de plazos que afectan al seguimiento |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Significado de los estados y del indicador de cumplimiento temporal |
| [Validación de tareas](./45-validacion-de-tareas.md) | Relación entre validaciones y valoraciones |
| [Qué es el módulo de tareas](./39-que-es-el-modulo-de-tareas.md) | Visión general del módulo |

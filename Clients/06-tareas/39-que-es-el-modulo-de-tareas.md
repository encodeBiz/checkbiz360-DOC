# Qué es el módulo de tareas

El módulo de tareas de CheckBiz360 permite a los responsables de la empresa crear, asignar y hacer seguimiento de actividades operativas concretas. A diferencia del control horario, que registra cuándo trabaja un empleado, el módulo de tareas registra qué hace ese empleado durante su jornada y si lo ha completado correctamente.

Se trata de una herramienta complementaria que aporta visibilidad sobre el trabajo real realizado en cada turno, sucursal o departamento.

---

## Diferencia entre tareas y fichajes

El control horario y el módulo de tareas tienen objetivos distintos y se complementan.

| Aspecto | Control horario | Módulo de tareas |
|---|---|---|
| Qué registra | Presencia: entrada y salida | Actividad: qué se ha hecho |
| Unidad de medida | Tiempo trabajado | Tarea completada o no |
| Quién actúa | El empleado ficha | El empleado actualiza el estado |
| Para qué sirve | Nóminas y cumplimiento normativo | Seguimiento operativo y desempeño |

Un empleado puede haber fichado correctamente y aun así no haber completado las tareas asignadas para ese turno. El módulo de tareas permite detectar esa diferencia.

---

## Casos de uso habituales

### Checklist de apertura y cierre de establecimiento

Los comercios y locales de atención al público necesitan que se realicen una serie de acciones concretas antes de abrir o al cerrar. El responsable crea una tarea de apertura y escribe los pasos como **lista de comprobación en la descripción**, que el empleado de turno sigue desde la app y confirma al terminar.

### Tareas de mantenimiento

Las incidencias técnicas o las revisiones periódicas de instalaciones pueden gestionarse como tareas asignadas al responsable de mantenimiento. El sistema guarda el historial de ejecución y permite adjuntar evidencias en foto o vídeo del resultado.

### Actividades de formación

Cuando un empleado debe completar un módulo de formación, visualizar un documento corporativo o asistir a una sesión interna, esa obligación puede convertirse en una tarea con fecha límite. El manager puede comprobar quién la ha completado y quién no.

### Seguimiento de objetivos operativos

Los objetivos de corto plazo —llenar un stock, contactar con una lista de clientes, completar un informe— pueden descomponerse en tareas asignadas a las personas adecuadas, con prioridad y fecha límite claramente definidas.

### Servicios a domicilio o en casa del cliente

Cuando el trabajo cambia de dirección cada día —una reparación, una limpieza, una visita técnica—, la tarea puede llevar su **propio lugar de trabajo** sin dar de alta una sucursal por encargo. El empleado solo puede iniciarla estando en esa dirección. Se explica en [Crear una tarea](./40-crear-una-tarea.md#lugar-de-trabajo-propio).

### Trabajo que se repite

Un encargo que se repite con pocas variaciones no hace falta escribirlo de nuevo: la tarea se **duplica** desde el listado o desde su ficha, y la copia solo pide título y fechas. Se explica en [Crear una tarea](./40-crear-una-tarea.md#duplicar-una-tarea).

---

## Roles que interactúan con el módulo

El módulo de tareas respeta la jerarquía de roles de CheckBiz360. Cada rol tiene capacidades distintas:

### Owner y Manager

Tienen acceso completo al módulo. Pueden crear, asignar, modificar y cancelar tareas en cualquier sucursal de la entidad, validarlas y valorar el desempeño del empleado.

### Supervisor

Su alcance se decide **en cada tarea**, no en su perfil. Toda tarea incluye dos opciones —**Permitir validación por supervisor** y **Permitir valoración por supervisor**, ambas activadas por defecto— que habilitan al supervisor de la sucursal a cerrar el circuito de esa tarea concreta. La creación de tareas por supervisores está desactivada por defecto.

### Worker (empleado)

Recibe las tareas asignadas, consulta su descripción y sus evidencias, inicia el trabajo, lo pausa y lo reanuda cuando tiene que interrumpirlo, añade notas de progreso, sube evidencias y marca la tarea como completada. No puede crear ni asignar tareas a otros empleados.

---

## Relación con el control horario

Tareas y fichajes miden cosas distintas, pero no van por separado: para **iniciar**, **reanudar** o **completar** una tarea, el empleado tiene que tener la **jornada abierta**, es decir, haber fichado la entrada. Estar en un descanso cuenta como jornada abierta. Si no ha fichado, la acción se rechaza con el error `task/no_open_session`.

**Pausar** no lo exige: se pausa justo en el momento de irse.

Los propietarios y administradores que actúan desde el backoffice no tienen jornada que abrir y quedan exentos; así pueden, por ejemplo, cerrar la tarea de alguien que ya se ha marchado. Un supervisor o manager que trabaja con su propia ficha de empleado sí necesita tener la jornada abierta.

Las fechas, en cambio, son libres: una tarea puede tener la fecha límite en un día festivo o fuera del horario habitual si la operativa lo requiere.

---

> **Nota:** Para aprovechar al máximo el módulo de tareas, le recomendamos combinarlo con el módulo de informes operativos. Los datos de completitud de tareas alimentan los indicadores de eficiencia del equipo en la sección de inteligencia operativa.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una tarea](./40-crear-una-tarea.md) | Campos, pasos y opciones al crear una tarea |
| [Asignar tareas a empleados](./41-asignar-tareas-a-empleados.md) | Asignación individual y por equipo |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida completo de una tarea |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Iniciar, pausar, reanudar y el historial de la tarea |
| [Validación de tareas](./45-validacion-de-tareas.md) | Flujo de validación y permisos |
| [Informes de tareas](./48-informes-de-tareas.md) | Métricas y exportación de datos |

# Crear una tarea

Crear una tarea en CheckBiz360 es el punto de partida para asignar trabajo concreto a uno o varios empleados. Desde el backoffice, los managers y los supervisores con permiso pueden definir todos los detalles de la actividad antes de enviarla al equipo.

Este artículo describe todos los campos disponibles al crear una tarea y explica el proceso paso a paso.

---

## Campos de una tarea

### Campos obligatorios

- **Título** — Nombre breve y descriptivo de la tarea. Debe ser suficientemente claro para que el empleado entienda de qué se trata sin necesidad de leer la descripción completa. Máximo 100 caracteres.
- **Empleado asignado** — La persona o personas responsables de completar la tarea. Puede ser un único empleado o varios a la vez.
- **Fecha límite** — La fecha y hora antes de la cual debe completarse la tarea. Si se supera sin completar, el sistema registra el incumplimiento en el indicador de cumplimiento temporal de la tarea.

### Campos opcionales pero recomendados

- **Descripción** — Explicación detallada de lo que hay que hacer, incluyendo instrucciones específicas, condiciones a cumplir o información de contexto. No tiene límite de extensión.
- **Tipo de tarea** — Categoría que facilita el filtrado y los informes. Ejemplos: mantenimiento, formación, operativo, comercial, administrativo.
- **Prioridad** — Nivel de urgencia de la tarea: alta, media o baja. Afecta al orden en que aparece la tarea en la app del empleado.
- **Sucursal** — Centro de trabajo al que pertenece la tarea. Si la entidad tiene varias sucursales, especificar la sucursal permite filtrar los informes y limitar la visibilidad a los responsables de esa ubicación.

---

## Pasos para crear una tarea desde el backoffice

1. Acceda al backoffice con sus credenciales de manager, owner o supervisor con permiso de creación.
2. En el menú lateral, seleccione **Tareas** y pulse **Nueva tarea**.
3. Escriba el **título** de la tarea en el campo correspondiente.
4. Si lo desea, añada una **descripción** detallada con instrucciones para el empleado.
5. Seleccione el **tipo de tarea** y la **prioridad** en los menús desplegables.
6. Establezca la **fecha límite**: elija fecha y hora. Si no se indica hora, el sistema asume las 23:59 del día seleccionado.
7. En el campo **Empleado asignado**, busque y seleccione la persona o personas destinatarias.
8. Si la entidad tiene varias sucursales, seleccione la **sucursal** correspondiente.
9. Si necesita adjuntar material de apoyo, pulse **Adjuntar archivo** y suba las fotos o vídeos necesarios.
10. Revise la información y pulse **Guardar**. La tarea se crea con estado "pendiente" y el empleado recibe una notificación push de forma automática.

---

## Adjuntar instrucciones o imágenes

El campo de adjuntos permite incluir material visual de apoyo que el empleado necesite para completar la tarea. Los formatos admitidos en V1 son:

- Fotos: JPG, PNG
- Vídeos: MP4 y formatos de vídeo estándar
- Tamaño máximo por archivo: 10 MB

Los adjuntos son visibles desde la app del empleado en el detalle de la tarea. Esto resulta especialmente útil cuando la tarea requiere identificar un elemento a partir de una fotografía o seguir una demostración en vídeo.

> **Consejo:** Para tareas de mantenimiento o inspección, adjunte una fotografía del elemento a revisar. Reducirá las dudas del empleado y mejorará la calidad de ejecución.

---

### Adjuntos de tipo documento

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La posibilidad de adjuntar documentos en formato PDF, Word o Excel a una tarea está planificada para una versión futura. Cuando esté disponible, permitirá incluir protocolos, formularios y hojas de datos directamente en el detalle de la tarea.

---

## Asignación a varios empleados

Una misma tarea puede asignarse a más de un empleado. Existen dos supuestos habituales:

**Tarea compartida:** Todos los empleados seleccionados ven la misma tarea y cualquiera de ellos puede marcarla como completada. Esta modalidad es útil cuando la actividad la puede resolver el primero que esté disponible.

**Tarea individual replicada:** Si necesita que cada empleado complete la tarea de forma independiente, cree una tarea por empleado. Puede usar la función de duplicado para no tener que rellenar los campos desde cero.

> **Nota:** Cuando asigna una tarea a varios empleados al mismo tiempo, cada uno de ellos recibe su propia notificación push. El historial de acciones de cada empleado sobre la tarea queda registrado de forma individual.

---

## Duplicar una tarea existente

Si necesita crear una tarea similar a una ya existente, puede duplicarla desde el listado de tareas del backoffice. El sistema crea una copia con todos los campos del original, que puede editar antes de guardar. Esta función es especialmente útil para tareas periódicas o para asignar el mismo trabajo a empleados de distintas sucursales.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Qué es el módulo de tareas](./39-que-es-el-modulo-de-tareas.md) | Visión general del módulo y sus casos de uso |
| [Asignar tareas a empleados](./41-asignar-tareas-a-empleados.md) | Asignación individual y por equipo |
| [Prioridades y fechas límite](./44-prioridades-y-fechas-limite.md) | Cómo gestionar la urgencia y los plazos |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida de una tarea |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Qué notificaciones reciben los empleados |

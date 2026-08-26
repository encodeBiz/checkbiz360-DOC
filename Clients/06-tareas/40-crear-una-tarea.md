# Crear una tarea

Crear una tarea en CheckBiz360 es el punto de partida para asignar trabajo concreto a uno o varios empleados. Desde el backoffice, los managers y los supervisores con permiso pueden definir todos los detalles de la actividad antes de enviarla al equipo.

Este artículo describe todos los campos disponibles al crear una tarea y explica el proceso paso a paso.

---

## Campos de una tarea

### Campos obligatorios

- **Título** — Nombre breve y descriptivo de la tarea. Debe ser suficientemente claro para que el empleado entienda de qué se trata sin necesidad de leer la descripción completa.
- **Sucursal** — Centro de trabajo al que pertenece la tarea. Determina, además, la **zona horaria operativa** con la que se interpretan las fechas de la tarea; si la sucursal no tiene zona horaria propia, se usa la de la entidad.
- **Fecha límite** — Fecha y hora antes de la cual debe completarse la tarea. Si se supera sin completar, la tarea pasa a *vencida* en su indicador de cumplimiento temporal.

### Campos opcionales

- **Descripción** — Explicación detallada de lo que hay que hacer. Admite formato: títulos, listas, **listas de tareas con casillas**, citas, negrita, cursiva y enlaces. No tiene límite de extensión.
- **Fecha prevista de inicio** — Hora a la que se espera que el empleado empiece. No bloquea nada por sí sola: su utilidad es activar el aviso de inicio tardío.
- **Notificar si no inicia a tiempo** — Si se activa y la tarea tiene fecha prevista de inicio, el sistema envía una notificación automática cuando han pasado **15 minutos** de esa hora sin que la tarea se haya iniciado. Sin fecha prevista de inicio, la opción no tiene efecto.
- **Estado** — Estado con el que nace la tarea. Lo habitual es *Borrador* (no visible aún para el equipo) o *Asignada* (ya enviada). Los estados *Validada*, *Rechazada* y *Cancelada* no pueden seleccionarse manualmente en la creación: son el resultado del ciclo de vida de la tarea.
- **Prioridad** — Baja, media, alta o **crítica**. Afecta al orden en que aparece la tarea en la app del empleado.
- **Empleados asignados** — Persona o personas responsables de completarla. Puede buscarse y seleccionarse a varios.

### Opciones de configuración de la tarea

Tres opciones controlan cómo se cierra y se revisa la tarea:

| Opción | Por defecto | Qué hace |
|---|---|---|
| **Requerir evidencia al completar** | Activada | El empleado no puede marcar la tarea como completada sin adjuntar al menos una foto o vídeo. Si lo intenta, recibe el error `task/evidence_required` |
| **Permitir validación por supervisor** | Activada | Un supervisor de la sucursal puede validar o rechazar la tarea, sin necesidad de un manager |
| **Permitir valoración por supervisor** | Activada | Un supervisor puede puntuar el trabajo del empleado al cerrar la tarea |

---

## Pasos para crear una tarea desde el backoffice

1. Acceda al backoffice con sus credenciales de manager, owner o supervisor con permiso de creación.
2. En el menú lateral, seleccione **Tareas** y pulse el botón de nueva tarea.
3. Escriba el **título**.
4. Redacte la **descripción**. Use la barra de formato para añadir listas de comprobación, títulos o enlaces si la tarea tiene varios pasos.
5. Busque y seleccione la **sucursal**. Bajo el campo aparece la zona horaria con la que se enviarán las fechas.
6. Si procede, indique la **fecha prevista de inicio** y active **Notificar si no inicia a tiempo**.
7. Establezca la **fecha límite** (fecha y hora).
8. Elija **estado** y **prioridad**.
9. Busque y seleccione a los **empleados asignados**.
10. Revise las tres opciones de configuración (evidencia, validación y valoración por supervisor).
11. Pulse **Guardar**. Los empleados asignados reciben una notificación push automática.

> **Consejo:** para tareas con varios pasos —una apertura de local, una revisión de material, un protocolo de limpieza— use una lista de tareas en la descripción. El empleado lee la secuencia completa en la app sin que haga falta crear una tarea por paso.

---

## Redactar la descripción con formato

El campo de descripción incorpora una barra de herramientas con negrita, cursiva, código, título, lista con viñetas, lista numerada, **lista de tareas**, cita y enlace. Al pulsar Intro dentro de una lista, la lista continúa automáticamente.

La pestaña **Vista previa** muestra cómo se verá el texto una vez guardado.

Un ejemplo de descripción con lista de comprobación:

```
## Apertura del local
- [ ] Revisar cámaras
- [ ] Contar caja
- [ ] Abrir persiana

**Importante:** avisar al supervisor si falta efectivo.
```

> **Nota:** las casillas de la descripción son parte del texto de la tarea, no un estado guardado. Sirven como guion de trabajo para el empleado; el avance real de la tarea se refleja con los cambios de estado, las notas y las evidencias.

---

## Evidencias y adjuntos

Las evidencias no se adjuntan al crear la tarea: se suben durante su ejecución, desde la app del empleado o desde el detalle de la tarea en el backoffice.

- Desde el **backoffice** se adjuntan fotos en formato JPG, PNG o WEBP, con un máximo de **5 MB** por archivo.
- Desde la **app del empleado** se admiten además vídeos, con un máximo de **25 MB** por archivo.

Los límites son los valores por defecto de la plataforma y pueden ajustarse por configuración.

### Adjuntos de tipo documento

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

Adjuntar documentos en formato PDF, Word o Excel a una tarea está planificado para una versión futura. Cuando esté disponible, permitirá incluir protocolos, formularios y hojas de datos directamente en el detalle de la tarea.

---

## Asignación a varios empleados

Una misma tarea puede asignarse a más de un empleado. Por defecto, **cualquiera de los asignados puede completarla**: es útil cuando la actividad la resuelve el primero que esté disponible.

Si necesita que cada empleado la complete de forma independiente, cree una tarea por empleado.

> **Nota:** cuando asigna una tarea a varios empleados, cada uno recibe su propia notificación push, y el historial de acciones de cada uno queda registrado por separado en la actividad de la tarea.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Qué es el módulo de tareas](./39-que-es-el-modulo-de-tareas.md) | Visión general del módulo y sus casos de uso |
| [Asignar tareas a empleados](./41-asignar-tareas-a-empleados.md) | Asignación individual y por equipo |
| [Prioridades y fechas límite](./44-prioridades-y-fechas-limite.md) | Cómo gestionar la urgencia y los plazos |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida de una tarea |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Qué notificaciones reciben los empleados |

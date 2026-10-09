# Crear una tarea

Crear una tarea en CheckBiz360 es el punto de partida para asignar trabajo concreto a uno o varios empleados. Desde el backoffice, los managers y los supervisores con permiso pueden definir todos los detalles de la actividad antes de enviarla al equipo.

Este artículo describe todos los campos disponibles al crear una tarea y explica el proceso paso a paso.

---

## Campos de una tarea

### Campos obligatorios

- **Título** — Nombre breve y descriptivo de la tarea. Debe ser suficientemente claro para que el empleado entienda de qué se trata sin necesidad de leer la descripción completa.
- **Sucursal** — Centro de trabajo al que pertenece la tarea. Determina, además, la **zona horaria operativa** con la que se interpretan las fechas de la tarea; si la sucursal no tiene zona horaria propia, se usa la de la entidad. **No se puede cambiar una vez creada la tarea**: si se eligió mal, cancele la tarea y cree otra en la sucursal correcta.
- **Fecha límite** — Fecha y hora antes de la cual debe completarse la tarea. Si se supera sin completar, la tarea pasa a *vencida* en su indicador de cumplimiento temporal.

### Campos opcionales

- **Descripción** — Explicación detallada de lo que hay que hacer. Admite formato: títulos, listas, **listas de tareas con casillas**, citas, negrita, cursiva y enlaces. No tiene límite de extensión.
- **Lugar de trabajo** — Dirección donde se hace el trabajo cuando no es la propia sucursal, con su **margen** en metros. Ver [Lugar de trabajo propio](#lugar-de-trabajo-propio).
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
6. Si el trabajo se hace en otra dirección, rellene **Lugar de trabajo (opcional)** y revise el **margen**.
7. Si procede, indique la **fecha prevista de inicio** y active **Notificar si no inicia a tiempo**.
8. Establezca la **fecha límite** (fecha y hora).
9. Elija **estado** y **prioridad**.
10. Busque y seleccione a los **empleados asignados**.
11. Revise las tres opciones de configuración (evidencia, validación y valoración por supervisor).
12. Pulse **Guardar**. Los empleados asignados reciben una notificación push automática.

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

## Lugar de trabajo propio

Por defecto, una tarea se hace en su sucursal, y la única comprobación de ubicación es la del fichaje: la geocerca de la sucursal al abrir la jornada.

Cuando el trabajo se hace en otra dirección —el domicilio de un cliente, una obra, un local que cambia cada día—, la tarea puede llevar su **propio lugar de trabajo**. Así no hace falta dar de alta una sucursal por cada encargo.

### Cómo se configura

1. En el formulario de la tarea, escriba la dirección en **Lugar de trabajo (opcional)** y **elíjala de la lista** de sugerencias.
2. Revise el **margen**: es el radio, en metros, dentro del cual se considera que el empleado está en el lugar. Por defecto toma el de la sucursal y puede ampliarse; un garaje subterráneo o una nave necesitan más margen que un portal.
3. Guarde la tarea.

Si la dirección no es lo bastante precisa para situar el punto —por ejemplo, falta el número del portal—, la tarea no se guarda y se indica el error `task/worksite_imprecise`. Complete la dirección y vuelva a elegirla.

### Qué cambia para el empleado

- **Iniciar** la tarea exige estar dentro del margen. La app envía la posición y el servidor la comprueba; fuera del margen, el inicio se rechaza con `task/out_of_worksite`, que indica la distancia y el margen permitido, y el intento queda anotado en el historial de la tarea.
- **Reanudar** una tarea pausada exige lo mismo que iniciarla.
- **Completar** no se bloquea: la posición se registra, pero la tarea se puede cerrar aunque el empleado ya se haya marchado del lugar.
- En la app, el detalle de la tarea muestra la dirección y un enlace **Ver en Maps** para llegar hasta ella.

En el backoffice, el bloque **Lugar de trabajo** del detalle de la tarea muestra la sucursal, la dirección, el margen y un botón para abrir el mapa.

> **Importante:** una tarea con lugar de trabajo propio **solo se puede iniciar, reanudar o completar desde la app**, porque el backoffice no envía ninguna ubicación: si se intenta desde el panel, la acción se rechaza con `task/geo_required`. Pausarla, cancelarla, validarla o rechazarla desde el backoffice funciona con normalidad.

---

## Duplicar una tarea

Cuando un encargo se repite, no hace falta volver a rellenar el formulario. Una tarea se duplica con la acción **Duplicar**, disponible en el listado de tareas y en la ficha de la tarea.

La copia se crea en la **misma sucursal** y hereda el encargo: descripción, prioridad, opciones de configuración y lugar de trabajo. **No hereda** su ejecución: ni empleados asignados, ni evidencias, notas, valoraciones o historial.

### Pasos

1. Pulse **Duplicar** en la tarea que quiere copiar.
2. Revise el **título de la copia**, que se propone con el del original.
3. Indique la **fecha límite** y, si procede, la **fecha prevista de inicio**. Las fechas del original no se heredan a propósito: una copia con el plazo antiguo nacería ya vencida. Se interpretan con la zona horaria de la sucursal.
4. Pulse **Duplicar**.

La copia nace en **Borrador** y sin asignar. Desde la ficha, duplicar le lleva directamente a la copia: el paso siguiente es editarla, asignar a los empleados y ponerla en **Asignada**.

Puede duplicar quien puede crear tareas en esa sucursal. La sucursal tiene que estar activa.

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
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Iniciar, pausar y reanudar una tarea |
| [Geocercas y radio de fichaje](../03-control-horario/16-geocercas-radio-de-fichaje.md) | La comprobación de ubicación al fichar |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Qué notificaciones reciben los empleados |

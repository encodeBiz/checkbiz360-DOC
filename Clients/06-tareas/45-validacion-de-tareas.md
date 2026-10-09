# Validación de tareas

La validación es el paso por el que un responsable confirma que el trabajo realizado por el empleado cumple los requisitos exigidos. CheckBiz360 separa la acción de completar una tarea (que realiza el empleado) de la de validarla (que realiza el responsable), garantizando un doble nivel de control sobre la calidad del trabajo.

---

## Flujo de validación

El proceso sigue siempre el mismo orden:

1. El empleado ejecuta la tarea y la marca como **completada** desde la app.
2. El sistema avisa al responsable de que hay trabajo pendiente de revisión.
3. El responsable accede al backoffice, revisa el trabajo y decide si lo **acepta** o lo **rechaza**.
4. Si acepta, la tarea pasa a **validada** y queda cerrada.
5. Si rechaza, la tarea pasa a **rechazada**, con el motivo visible para el empleado.

---

## Aceptar una tarea completada

Para validar una tarea, el responsable debe:

1. Acceder al backoffice y abrir la sección **Tareas**.
2. Filtrar por estado **Completada** para ver las que están a la espera de revisión.
3. Abrir el detalle de la tarea.
4. Leer las notas del empleado y revisar las evidencias aportadas.
5. Validar la tarea.

Una vez validada, la tarea queda cerrada: el estado *validada* no se asigna a mano desde el formulario de edición. Si hubiera que volver sobre ella, se **reabre** devolviéndola a *Asignada*, lo que retira la validación (ver [Reabrir una tarea](./42-estados-de-una-tarea.md#reabrir-una-tarea)). Si la valoración está habilitada, a continuación puede puntuar el trabajo del empleado.

---

## Rechazar una tarea completada

Si el responsable considera que el trabajo no es correcto, puede rechazarlo.

### Pasos para rechazar una tarea

1. Desde el detalle de la tarea en el backoffice, pulse **Rechazar**.
2. Escriba el motivo del rechazo. **Es obligatorio**: sin texto, la acción no se puede confirmar.
3. Confirme el rechazo.

La tarea pasa al estado **rechazada** y el motivo queda visible para el empleado junto al historial completo de la tarea.

> **Importante:** el motivo del rechazo es obligatorio. Una explicación clara es lo que permite al empleado corregir el trabajo y no repetir el error.

---

## Consecuencias del rechazo

Cuando una tarea es rechazada:

- Queda en estado **rechazada**, que es un cierre con motivo: la tarea no vuelve sola a la lista de trabajo del empleado.
- El indicador de cumplimiento temporal pasa a mostrar *Rechazada*, porque el cumplimiento del plazo deja de ser lo relevante.
- El historial registra el rechazo, el motivo, el autor y la fecha, de modo que queda evidencia del ciclo completo.

**Si el trabajo debe rehacerse**, el responsable edita la tarea y la devuelve al estado **asignada**, ajustando la fecha límite si procede. Al hacerlo se retira el rechazo anterior, aunque sigue constando en el historial. El empleado la recupera en su lista y el ciclo vuelve a empezar.

---

## Quién puede validar

Por defecto validan **managers y owners**. Cada tarea incorpora además la opción **Permitir validación por supervisor**, activada por defecto, que habilita a los supervisores de la sucursal a validar o rechazar esa tarea.

Es una decisión **por tarea**, no un permiso del perfil del empleado: se marca al crear la tarea o al editarla, junto a las opciones de valoración y de evidencia obligatoria. Esto permite descentralizar la operativa del día a día y reservar la validación de las tareas sensibles para el manager.

> **Nota:** el manager mantiene siempre visibilidad completa sobre las validaciones de sus supervisores. Toda acción queda registrada en el historial con el nombre de quien la ejecutó y su nivel de responsabilidad.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida y significado de cada estado |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Cómo el empleado actualiza el progreso |
| [Valoración del trabajador](./46-valoracion-del-trabajador.md) | Puntuación de desempeño tras la validación |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Avisos al validar o rechazar una tarea |
| [Roles y niveles de responsabilidad](../02-empleados/07-roles-y-niveles-de-responsabilidad.md) | Descripción de permisos por rol |

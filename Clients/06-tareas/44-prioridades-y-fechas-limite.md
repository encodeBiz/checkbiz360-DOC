# Prioridades y fechas límite

La combinación de prioridades y fechas límite permite al responsable comunicar al empleado qué tareas son más urgentes y cuánto tiempo tiene para completarlas. Gestionar correctamente ambos parámetros reduce los olvidos, ordena el trabajo del equipo y genera datos fiables sobre el cumplimiento operativo.

---

## Sistema de prioridades

CheckBiz360 clasifica las tareas en cuatro niveles de prioridad:

| Prioridad | Uso recomendado |
|---|---|
| **Crítica** | La tarea no admite demora: hay un riesgo operativo, de seguridad o legal si no se resuelve de inmediato. |
| **Alta** | Debe completarse antes que el resto del trabajo del día. Afecta directamente a la operativa o tiene consecuencias si se retrasa. |
| **Media** | Importante, pero admite cierta flexibilidad en el momento de ejecución. |
| **Baja** | Conveniente pero no crítica. Puede posponerse si surgen tareas más urgentes. |

La prioridad se establece al crear la tarea y puede modificarse después desde el backoffice mientras la tarea siga abierta. En el listado, cada prioridad tiene su color: rojo para crítica, ámbar para alta, azul para media y verde para baja.

> **Consejo:** reserve las prioridades crítica y alta para lo que realmente lo es. Si todas las tareas son urgentes, la prioridad deja de ordenar el trabajo y el empleado pierde el criterio para decidir por dónde empezar.

---

## Fechas de una tarea

Una tarea maneja dos fechas, con propósitos distintos:

- **Fecha límite** (obligatoria): el momento máximo en que la tarea debe quedar completada. Es la referencia del indicador de cumplimiento temporal.
- **Fecha prevista de inicio** (opcional): la hora a la que se espera que el empleado empiece. No bloquea nada por sí sola; sirve para activar el aviso de inicio tardío.

Ambas se interpretan en la **zona horaria operativa de la sucursal** de la tarea. Si la sucursal no tiene zona horaria propia, se usa la de la entidad. Esto es importante en organizaciones con centros en distintos husos: la fecha límite de las 18:00 significa las 18:00 del centro donde se ejecuta la tarea, no las del navegador de quien la creó.

### Consideraciones al fijar una fecha límite

- Tenga en cuenta el turno del empleado asignado. Si la tarea vence a las 10:00 y el empleado entra a las 11:00, vencerá antes de que pueda atenderla.
- Para tareas que se repiten, la fecha límite delimita el ciclo de cada instancia.
- Puede modificar la fecha límite de una tarea abierta en cualquier momento desde el backoffice.

---

## Aviso de inicio tardío

Es el aviso automático que sí se configura tarea a tarea. Si la tarea tiene **fecha prevista de inicio** y está activada la opción **Notificar si no inicia a tiempo**, el sistema envía una notificación cuando han pasado **15 minutos** de esa hora sin que la tarea se haya iniciado.

El envío queda registrado en la actividad de la tarea, de modo que el responsable puede comprobar si el aviso llegó a producirse.

Sin fecha prevista de inicio, la opción no tiene efecto: no hay hora contra la que medir el retraso.

---

## Avisos de vencimiento

Además del aviso de inicio tardío, la plataforma avisa cuando una tarea se acerca a su fecha límite y cuando la supera. Cada aviso se emite una sola vez por tarea y queda registrado, para que un mismo vencimiento no genere notificaciones repetidas.

> **Estado: Pendiente de desarrollo**
> La antelación de estos avisos no es configurable por el cliente en la versión actual. Poder ajustar la anticipación, activar un segundo recordatorio o variar la frecuencia según la prioridad forma parte del roadmap.

---

## Qué ocurre cuando una tarea vence sin completar

Cuando llega la fecha límite y la tarea no está completada, **no cambia de estado**: sigue en *asignada* o *en progreso*. Lo que cambia es su **indicador de cumplimiento temporal**, que pasa a *vencida*.

Las consecuencias son:

- La tarea aparece marcada como vencida en el listado del backoffice y en la app del empleado.
- El vencimiento queda registrado y se refleja en el informe de tareas.
- El empleado puede seguir completándola después de vencer. Al cerrarla, el indicador pasará a *completada tarde*, no a *completada a tiempo*.

> **Importante:** una tarea vencida no desaparece ni se cierra sola. El registro de que superó el plazo permanece en el histórico aunque después se complete y se valide.

---

## Ampliar el plazo

Si las circunstancias justifican dar más tiempo, el responsable puede editar la tarea y cambiar la fecha límite. El cambio queda reflejado en la actividad de la tarea, con el usuario que lo hizo y el momento.

### Pasos para ampliar el plazo

1. Acceda al backoffice y abra el detalle de la tarea.
2. Pulse **Editar**.
3. Modifique el campo **Fecha límite**.
4. Guarde los cambios.

Si además quiere dejar constancia del motivo para el empleado, añada una **nota** a la tarea: es el mecanismo previsto para la comunicación escrita dentro de una tarea.

Ampliar el plazo no cambia el estado de la tarea. El indicador de cumplimiento temporal se recalcula contra la nueva fecha límite.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una tarea](./40-crear-una-tarea.md) | Campos disponibles al crear una tarea |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida, estados y cumplimiento temporal |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Seguimiento del progreso en tiempo real |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Avisos automáticos de la plataforma |
| [Informes de tareas](./48-informes-de-tareas.md) | Tareas vencidas frente a completadas a tiempo |

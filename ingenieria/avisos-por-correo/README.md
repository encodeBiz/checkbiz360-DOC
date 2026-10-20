# Avisos de trabajo por correo · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS — CheckBiz360
**Dominio:** notificaciones de tareas y cuadrante × correo
**Fecha:** 2026-10-20
**Estado:** Diseño cerrado el 2026-10-20 · sin implementar
**Autor:** Jose Acevedo

---

## De dónde sale

El punto de fichaje ([quiosco](../quiosco/README.md)) es para quien no usa el móvil, y esa
persona no recibe los avisos push de la app. Jose, 2026-10-20: «las alertas deben poder
enviarse por correo, las del cuadrante, o sea de las tareas, pero las del fichaje no; y
habilitado por empleado, un check en Horarios y festivos: enviar notificaciones por email». Y:
«el semanal sale el domingo, pero solo a los que tengan esa casilla puesta, ya que serán los
menos, los problemáticos».

Antes, el mismo día, pidió poder mandar el cuadrante semanal por correo, automático, «pero lo
que no puede ser es que se envíen mil», y que lo crítico son los horarios partidos y por tareas.

## El principio

> **Por correo va lo que cambia cuándo o dónde trabaja una persona, y nada más. Y solo a quien
> tiene marcada la casilla.** Ni un correo por tarea: se agrupa.

## La casilla

- En la ficha de la persona, sección **Horarios y festivos**: «Enviar notificaciones por
  email». **Desmarcada por defecto.**
- Se guarda con el resto de su calendario: `entities/{e}/employees/{p}/calendar/config
  .emailNotifications: true`. Lo escribe el mismo formulario y el mismo endpoint de calendario.
- Si la persona no tiene un correo real (alta `pending`, correo de relleno como
  `sin-correo+…@rentmanbiz.local`, o dada de baja), la casilla sale desactivada con el motivo.
- El correo va **además** del push: si la persona también tiene la app, le llegan los dos.

## Qué va por correo

| Aviso | Cuándo | Hoy por push |
|---|---|---|
| **Tarea asignada** | le asignan una tarea (también al crearse ya asignada, incluido el cuadrante) | sí (`task_assigned`) |
| **Tarea cambiada** | cambia el día, la hora o el lugar de una tarea suya; con el antes y el después | sí (`task_updated`), sin el antes |
| **Tarea retirada** | se la quitan, se cancela o la borra un cuadrante | **no**: hoy nadie avisa (ver §Hueco) |
| **Su semana** | el domingo, la semana siguiente entera | no existe |

**Fuera**, a propósito: los recordatorios de fichar (`task_checkin_reminder`,
`task_checkout_reminder`, `task_switch_reminder`), «tarea no empezada» (`task_start_delay`, es
para el encargado), validada, rechazada, valorada, recursos subidos, y todo lo de fichajes e
incidencias.

## Que no lleguen mil: el resumen de 15 minutos

Un cuadrante crea o mueve muchas tareas de golpe. Cada aviso de tarea de una persona con la
casilla se **apunta**, no se manda:

```text
email_digest/{entityId}_{employeeId} = {
  entityId, employeeId,
  events: [{ kind: "assigned"|"updated"|"removed", taskId, title, before?, after?, at }],
  firstAt, lastAt, dueAt, urgent
}
```

- `dueAt = lastAt + 15 min`: mientras sigan llegando cambios, espera. Al cuarto de hora sin
  novedades, sale **un correo** con todo: «Tienes 10 tareas nuevas esta semana», con la lista.
- **Excepción, lo de las próximas 24 horas:** si un evento toca una tarea que empieza antes de
  24 h, `dueAt = ahora` y sale en la siguiente pasada. Que te muevan la tarea de mañana a las
  7:00 no puede esperar.
- Si una misma tarea se asigna y se retira dentro del margen, se anulan y no se manda nada. Si
  cambia varias veces, se manda el estado final con el «antes» del primer evento.
- Lo despacha un trabajo cada 5 minutos que toma los resúmenes vencidos, los manda y los borra
  en una transacción (un resumen vencido no se manda dos veces).

## El correo semanal

- **Domingo a las 18:00** en la zona horaria de la empresa, con la semana siguiente (lunes a
  domingo). Configurable por empresa más adelante; hoy fijo.
- **Solo a las personas con la casilla.**
- **Lo mismo que ve en la app, día a día** (`ResolveEffectiveDay` día a día de la semana):
  - **jornada partida**: cada tramo en su línea — «Lunes · 08:00–12:00 y 16:00–20:00»;
  - **por tareas** (`scheduleMode: "tasks"`): cada tarea con hora, nombre y **dónde** (el
    nombre de la sucursal, o la dirección de la obra si la tarea tiene `workSite`); si dos se
    solapan, salen las dos;
  - libranzas y festivos, marcados.
- **Si nada cambió desde el último envío, no se manda nada.** Huella de la semana enviada en
  `schedule_emails/{entityId}_{employeeId}_{lunes}` = `{ hash, sentAt }`; también impide que
  un relanzamiento repita el envío.
- Las tareas de más de un día no entran en el horario por tareas (el generador las salta); en
  el correo salen aparte, «Tareas de varios días», para que no se pierdan.

## Hueco que este diseño cierra: la tarea retirada

Hoy, cuando un cuadrante retira tareas (`borrarPorTareas`) o se cancela una tarea, la persona
no recibe nada, ni por push. Se añade el aviso `task_removed` en `TaskNotificationService` y se
llama desde los dos caminos. Lo reciben por push todos, y por correo quien tenga la casilla.

## Cómo se manda

- Plantillas en `emails_template`: `TASKS_DIGEST` (resumen) y `WEEKLY_SCHEDULE` (semana), en el
  idioma de la persona (persona → empresa → inglés), con respaldo en el código y subidas por el
  script `email-templates`, como las del almacenamiento.
- Remitente y SMTP: los de siempre (`EmailService`).
- **Escala:** mil personas con casilla son mil correos el domingo; el pool de SES lo aguanta,
  pero no en un solo proceso en serie. El semanal se reparte por empresa y por lotes de 100,
  y es el primer uso natural del reparto de [programadas a escala](../programadas-a-escala/README.md).
  Mientras ese reparto no exista, corre por empresa con concurrencia acotada (como
  `checkActiveEmployeeWorker`, 8 en paralelo).

## Piezas

| Pieza | Dónde |
|---|---|
| Casilla en el calendario de la persona y su validación (correo real) | `shared/calendar` + panel, Horarios y festivos |
| Apuntar eventos en `email_digest` desde los avisos de tarea, y `task_removed` | `shared/checkbiz/notifications/TaskNotificationService` |
| Trabajo de resúmenes (cada 5 min) y semanal (cada hora, empresas cuyo domingo 18:00 local ha llegado) | `services/firebase_sdk` (`onSchedule`), lógica en `shared` |
| Resolver la semana de una persona (7 días, con lugar de cada tarea) | `shared/calendar` |
| Plantillas `TASKS_DIGEST` y `WEEKLY_SCHEDULE` | `shared` + script `email-templates` |
| Reglas: `email_digest` y `schedule_emails` solo servidor | `firestore.rules` |

## Fuera de alcance

- Avisos de fichaje por correo (decisión de Jose).
- Elegir día y hora del semanal por empresa (se fija domingo 18:00; se abre si alguien lo pide).
- Ausencias por rangos (`EmployeeCalendar.absences`): el cálculo del horario no las aplica hoy;
  las vacaciones que pone el panel sí (van como festivo de la persona).

# Tarea sin empezar a su hora

Una visita que tenía que empezar a las 9:00 y a las 9:05 nadie ha pulsado **Iniciar**. Puede ser un olvido o puede ser que no haya nadie allí. CheckBiz360 lo avisa a los **5 minutos**: a la persona, para que la inicie si ya está trabajando, y a la dirección, para que llame antes de que el cliente lo note.

---

## Qué resuelve

- **Se entera a los 5 minutos**, no al final del día.
- **La persona tiene su recordatorio** en el móvil, por si se le pasó pulsar **Iniciar**.
- **Varias tareas, un solo correo**: si se quedan varias sin empezar a la vez, llegan juntas en una lista.
- **En Inicio desde la primera**: basta una tarea sin empezar para verla en la portada.

---

## Cómo se activa

El aviso es de cada tarea. Al crearla o editarla:

1. Indique la **Fecha prevista de inicio**.
2. Marque **Notificar si no inicia a tiempo**.
3. Pulse **Guardar**.

Sin fecha prevista de inicio, la casilla no tiene efecto. En la ficha de la tarea, la etiqueta **Aviso de inicio** indica que está programado y cambia a **Aviso enviado** cuando sale.

> **Nota:** el texto de ayuda de la casilla todavía habla de 15 minutos. El aviso sale a los 5.

---

## Qué pasa a los 5 minutos

Si a los 5 minutos de la hora prevista la tarea sigue asignada y sin iniciar:

| Quién | Qué recibe |
|---|---|
| **Las personas asignadas** | Un aviso en la app. |
| **Propietarios y administradores** | Un correo con la tarea y su hora. Si se han quedado varias sin empezar a la vez, va un solo correo con la lista: hasta tres con su hora (y su centro, si son de varios) y cuántas más hay. |
| **Propietarios y administradores, en el panel** | La alerta **Tareas sin empezar** en **Requiere atención** de **Inicio**, desde una sola tarea. En **Hoy**, la cifra **Tareas** las cuenta como *sin empezar a su hora*. |

**Inicio** cuenta todas las tareas asignadas con fecha prevista de inicio que llevan 5 minutos sin empezar, tengan o no marcada la casilla del aviso: la casilla decide el aviso en la app y el correo, no lo que se ve en la portada. En cuanto alguien inicia la tarea, deja de contar.

El correo llega también para quien trabaja con horario por tareas.

---

## Cuándo no avisa

- **La tarea está en borrador.** Todavía no está en circulación.
- **La tarea tiene una [incidencia](./125-incidencia-en-la-tarea.md) abierta.** Ya se sabe por qué no ha empezado.
- **La hora de inicio pasó hace más de una hora** cuando la tarea entró en el aviso, por ejemplo porque se creó o se asignó tarde. No se envían avisos de algo que ya es viejo.
- **Ya se avisó una vez.** Cada tarea avisa una sola vez.

---

## Cómo se apaga

- **Para una tarea concreta:** desmarque **Notificar si no inicia a tiempo** en la tarea. No sale ni el aviso en la app ni el correo; si tiene fecha prevista de inicio, en **Inicio** sigue contando como sin empezar.
- **Solo el correo, para toda la empresa:** en **Herramientas → Alertas por correo → Configurar alertas**, grupo **Al momento, en la operación**, desmarque **Tarea sin empezar** y pulse **Guardar**. Las personas siguen recibiendo su aviso en la app y la alerta de **Inicio** sigue saliendo.

Las alertas por correo las configuran propietarios y administradores, y lo que se marca vale para todos ellos.

---

## Problemas frecuentes

| Situación | Qué hacer |
|---|---|
| No ha llegado ningún aviso | Compruebe que la tarea tiene **Fecha prevista de inicio** y **Notificar si no inicia a tiempo** marcada, y que no está en borrador ni tiene una incidencia abierta. |
| Llega el aviso en la app pero no el correo | Revise en **Herramientas → Alertas por correo** que **Tarea sin empezar** está marcada y que las alertas por correo están activadas. |
| La persona había empezado y le llegó el aviso igual | Seguramente estaba trabajando pero no pulsó **Iniciar** en la tarea. El aviso mira la tarea, no el fichaje. |
| Llegan demasiados correos | Desmarque **Tarea sin empezar** en las alertas por correo, o quite el aviso de las tareas en que no haga falta. |

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una tarea](./40-crear-una-tarea.md) | La fecha prevista de inicio y la casilla del aviso |
| [Notificaciones de tareas](./47-notificaciones-de-tareas.md) | Todos los avisos de las tareas |
| [Incidencia en la tarea](./125-incidencia-en-la-tarea.md) | Cuando la tarea no se puede hacer |
| [La portada: el hoy, las alertas y las últimas semanas](../07-inteligencia-operativa/112-la-portada-el-hoy-las-alertas-y-las-ultimas-semanas.md) | La alerta **Tareas sin empezar** y la cifra de **Hoy** |

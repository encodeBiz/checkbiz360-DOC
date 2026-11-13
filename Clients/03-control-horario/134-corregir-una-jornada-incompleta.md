# Corregir una jornada incompleta de una vez

Cuando alguien olvida fichar la salida, la jornada queda incompleta y se abre una incidencia. Si la jornada era partida, con varios turnos, puede haber varios fichajes que corregir. Desde la incidencia se corrige la jornada entera en una sola pantalla, con un solo motivo, y la persona recibe un único aviso para aceptarla o rechazarla.

---

## Qué resuelve

- **Una jornada partida de cinco turnos no son cinco correcciones.** Se ven todos los turnos del día juntos y se corrigen de una vez.
- **Un solo motivo** para todos los fichajes corregidos, en lugar de escribirlo en cada uno.
- **Un solo aviso a la persona**, que acepta o rechaza la jornada entera desde la app.
- **La incidencia se cierra sola** cuando la persona acepta.

La corrección no cambia nada hasta que la persona la acepta: el registro de jornada sigue siendo el que ella da por bueno.

---

## Corregir la jornada desde el panel

1. Abra la incidencia de la jornada incompleta, en **Contacto → Incidencias**.
2. Pulse **Corregir jornada**. Se abre una ventana con el nombre de la persona y el día, y debajo cada **Turno** de esa jornada con sus fichajes (entrada, descansos y salida) y su estado: *Jornada incompleta*, *Válido* o *Pendiente de validar*.
3. Marque los turnos que quiere corregir y ajuste las horas. Si la salida la puso el sistema a la hora planificada, lo indica: *Puesta por el sistema a la hora planificada*. Las horas están en la zona horaria que indica la propia ventana.
4. Escriba el motivo en **Motivos del cambio**. Es uno solo para todos los fichajes corregidos.
5. Pulse **Corregir y enviar**. El botón dice cuántos fichajes se envían.

Desde ese momento, la incidencia dice *Corrección enviada. Esperando a que [persona] la acepte.* Mientras espera, no se puede enviar otra corrección de la misma jornada.

> **Aviso:** no se puede poner una hora en el futuro. Si alguna lo está, la ventana lo avisa antes de enviar.

---

## Lo que hace la persona en la app

Le llega un único aviso. Al abrirlo ve **Corrección de tu jornada**, con una tarjeta por cada turno: lo que se ha corregido aparece tachado junto a la hora nueva, y la salida que faltaba aparece como *sin fichar* seguida de la hora propuesta.

- **Aceptar jornada**: se aplican todas las correcciones de la jornada. Los fichajes quedan válidos y la incidencia se cierra.
- **Rechazar**: la jornada entera vuelve a la empresa para que la revise. Puede escribir por qué no está de acuerdo; es opcional.

Para ver la jornada entera en una sola pantalla, la persona necesita la última versión de la app. Con una versión anterior, los cambios le llegan como avisos sueltos y los acepta fichaje a fichaje; cuando acepta el último, la corrección queda igual de cerrada.

---

## Lo que ve usted después

En la propia incidencia:

| Mensaje | Qué ha pasado |
|---|---|
| *[Persona] aceptó la corrección de la jornada.* | Fichajes válidos con las horas corregidas e incidencia resuelta. |
| *[Persona] rechazó la corrección.* | Los fichajes siguen como estaban y la incidencia sigue abierta, con el motivo si lo escribió. Puede enviar otra corrección. |
| *La corrección se aceptó solo en parte. Revisa los fichajes de la jornada.* | La persona, con una versión anterior de la app, aceptó unos fichajes y otros no. |

Cada fichaje corregido deja su entrada en el historial de cambios, con el motivo, quién lo propuso y quién lo aceptó. Ver [Trazabilidad e historial de cambios](./21-trazabilidad-historial-de-cambios.md).

---

## Quién puede hacerlo

Corrige la jornada el propietario, un administrador o un responsable con rol de manager. Aceptar o rechazar solo puede hacerlo la propia persona, desde su app.

---

## Problemas frecuentes

**No veo el botón Corregir jornada.** Solo aparece en las incidencias de jornada incompleta que siguen abiertas y sin una corrección esperando respuesta.

**La persona dice que no le ha llegado nada.** Pídale que abra la app y mire sus avisos; si tiene las notificaciones del móvil desactivadas, el aviso está igualmente en la app. Si usa una versión antigua, que la actualice.

**Ya aceptó y el fichaje sigue marcado como sospechoso.** Aceptar la corrección no cambia esa marca. Ver [Detección de anomalías](../07-inteligencia-operativa/55-deteccion-de-anomalias.md).

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Revisión y validación de fichajes](./20-revision-y-validacion-de-fichajes.md) | Correcciones de un solo fichaje y jornadas manuales |
| [Estados y códigos de error](./22-estados-y-codigos-de-error.md) | Qué significa una jornada incompleta |
| [Trazabilidad e historial de cambios](./21-trazabilidad-historial-de-cambios.md) | Lo que queda registrado de cada corrección |
| [Alertas por correo](../09-notificaciones/133-alertas-por-correo.md) | El aviso de jornadas sin cerrar en el resumen de la mañana |

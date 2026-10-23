# Avisos de tareas agrupados · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS — CheckBiz360
**Dominio:** notificaciones de tareas × push y app
**Fecha:** 2026-10-23
**Estado:** Diseño cerrado el 2026-10-23
**Autor:** Jose Acevedo

---

## De dónde sale

Al confirmar un cuadrante, cada tarea manda su propio aviso. Un mes de una persona con unas 90
tareas son 90 avisos en el móvil; con 20 personas, unos 1.800. Y reconfirmar una semana es
peor: el cuadrante por tareas la sustituye (borra y vuelve a crear), y cada tarea avisa
«ya no la tienes» y después «te la han asignado».

Jose, 2026-10-23: «hay que ver cómo las agrupamos para que no sea un despropósito, imagina un
cuadrante de un mes». Y sobre la forma: «el tipo de mensaje no debe cambiar, sino el mensaje
en sí; y no iría a una tarea sino al listado, pero por lo menos que lance la notificación
agrupada. Esto es solo para tareas».

Antecedente: el 2026-10-19 se quitó el aviso de «tarea creada», que llegaba duplicado con el
de asignación. Quedaba uno por tarea.

## El principio

> **Una ráfaga de cambios en las tareas de una persona es un solo aviso.** Una tarea suelta
> sigue avisando como siempre.

Es el mismo mecanismo que ya agrupa los [avisos por correo](../avisos-por-correo/README.md),
con un margen corto, porque el push tiene que llegar casi en el momento.

## Qué se agrupa

Solo los tres avisos que un cuadrante (o cualquier cambio en bloque) dispara a la persona
asignada:

| Aviso | Tipo |
|---|---|
| Tarea asignada (también al nacer ya asignada) | `task_assigned` |
| Tarea cambiada | `task_updated` |
| Tarea retirada, cancelada o borrada | `task_removed` |

**Fuera**, y siguen saliendo al momento: empezada, terminada, validada, rechazada, valorada,
evidencias, «no empezada a tiempo» y los recordatorios de fichar. Son de una tarea concreta y
no vienen en ráfaga. Tampoco se toca nada del fichaje ni de otros módulos.

## Cómo

Cada uno de esos avisos se **apunta** en lugar de mandarse:

```text
push_digest/{entityId}_{employeeId} = {
  entityId, employeeId,
  events: [{ kind, taskId, ref?, branchId, title, startAt, endAt, place, at }],
  firstAt, lastAt, dueAt, claimedAt
}
```

- `dueAt = lastAt + 1 min`: mientras sigan llegando cambios, espera. Un trabajo cada minuto
  manda los vencidos. Una tarea creada a mano llega, como mucho, unos dos minutos más tarde
  que hoy.
- Los eventos de la misma tarea se juntan como en el correo: asignada y retirada se anulan,
  asignada y cambiada sigue siendo asignada, y cambiada y retirada queda como retirada.
- **Reconfirmar no es «todo nuevo».** El cuadrante retira las tareas y las crea con otro id,
  así que juntar por `taskId` no basta. Se junta también por la referencia del cuadrante
  (`externalRef`, `cuadrante:{persona}:{fecha}:{inicio}`). Si una retirada y una asignada con
  la misma referencia traen el mismo título, hora y lugar, se anulan y no se avisa de nada. Si
  algo cambió, cuenta como «cambiada». Esto también arregla el resumen por correo, que usa la
  misma regla.
- Reclamar, mandar y borrar funciona igual que en el correo: transacción con `claimedAt` para
  no mandar dos veces, y solo se quitan los eventos ya enviados.

## El mensaje

**El tipo no cambia, cambia el texto.**

- **Un solo evento**: el aviso de hoy, idéntico. Mismo tipo, mismo texto, y al tocarlo abre la
  tarea (`screen: "task_detail"` con `taskId`).
- **Varios eventos**: un aviso con el tipo del evento principal (`task_assigned` si hay alguna
  nueva; si no, `task_updated`; si no, `task_removed`) y un texto que lo resume con las fechas
  en la zona horaria de la empresa:
  - «Tienes 87 tareas nuevas del 3 al 30 de noviembre.»
  - «Tienes 20 tareas nuevas del 3 al 9 de noviembre, 3 cambiadas y 2 retiradas.»
  - «Han cambiado 5 de tus tareas del 4 al 6 de noviembre.»
  - «Ya no tienes 12 tareas del 10 al 14 de noviembre.»

  Los datos llevan `module: "checkbiz_tasks"`, `screen: "task_list"`, `private: true`,
  `entityId` y `branchId` (si todas son de la misma sucursal), sin `taskId`.

Idioma: el de la persona, después el de la empresa y, en último caso, inglés. Es la regla de
siempre.

## La app

Comprobado en master 1.10.0, 1.7.0 y 1.4.0, que se comportan igual:

- **Versiones publicadas**: el aviso agrupado llega y se ve, en el push y en la lista de la
  app. Al tocarlo, el gestor no reconoce `screen: "task_list"` (solo navega con
  `task_detail` y `taskId`). Desde el push abre la app; desde la lista abre la ficha genérica
  del aviso con el título y el texto. No rompe nada y no hace falta publicar versión.
- **Siguiente versión**: una rama más en `notification_navigation_handler.dart`:
  `checkbiz_tasks` + `task_list` → `AppConstants.taskRoute`, con las mismas comprobaciones de
  `private` y de destinatario que el resto de avisos privados.

## Piezas

| Pieza | Dónde |
|---|---|
| Apuntar en `push_digest` en lugar de mandar (asignada, cambiada, retirada) | `shared/checkbiz/notifications/TaskNotificationService` |
| Agrupar, redactar (textos es/en del resumen) y mandar los vencidos | `shared/checkbiz/notifications/taskPushDigest` |
| Juntar también por `externalRef` (push y correo) | `shared/checkbiz/notifications/workEmail` (`mergeWorkEvents`) |
| Trabajo cada minuto, `taskPushDigests` | `services/firebase_sdk/src/programadas/avisosAgrupados` |
| `checkbiz_tasks` + `task_list` → listado de tareas | app, próxima versión |
| `push_digest` solo servidor | sin regla: lo que ninguna regla abre, Firestore lo niega al cliente |

## Orden de despliegue

En cada entorno, **primero la función `taskPushDigests`** y después el servicio de tareas. Con
el servicio nuevo y sin la función, los avisos se apuntan y no sale ninguno. Al revés no pasa
nada: la función no encuentra qué mandar.

Si apuntar falla (Firestore no responde), el aviso de esa persona sale al momento, como antes.

## Fuera de alcance

- Que reconfirmar no retire y vuelva a crear lo que no cambió. El aviso ya no lo nota, pero
  las tareas cambian de id. Es otro frente, en [cuadrantes](../cuadrantes/).
- Agrupar avisos que no son de tareas.

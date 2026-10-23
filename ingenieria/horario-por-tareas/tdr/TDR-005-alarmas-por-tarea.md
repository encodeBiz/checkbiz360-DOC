# TDR-005 — Fase 3: las alarmas pertenecen a la tarea

**Fecha:** 2026-10-16
**Estado:** En producción desde el 2026-10-17 (pase §1.8: `employeePlanifierWorker`, `planifierNotificationWorker` y `taskStartNotificationWorker`); redesplegadas con el `shared` del TDR-009 el 2026-10-22
**Componente:** `encodebiz-api` — `packages/shared` (calendar, notifications), `services/firebase_sdk` (planificador, aviso de tarea no iniciada), `services/checkinbiz` (activación)
**Decisiones de referencia:** [README](../README.md) D7 y D9

---

## 1. La decisión que faltaba

Jose, 2026-10-16: **en el modo manda el recordatorio de entrada.** Para quien está en
«Horario por tareas», el aviso de tarea no iniciada (`task_start_delay`, a los quince minutos)
deja de enviarse a esa persona: decía lo mismo que el recordatorio.

Los avisos de entrada fuera de patrón y de salida anticipada (`pattern_mismatch_*`,
`out_of_day_window`) **no van a la persona**: van a sus supervisores, y se calculan en el SaaS
(`CheckbizOperationals`), no en esta API. No son parte del triple aviso y quedan como están.
Apagar la salida anticipada en el modo (D9) queda pendiente de que esa heurística salga del
SaaS.

## 2. Qué cambia

Hoy el job de las 04:00 crea, para el día siguiente, un recordatorio de entrada y otro de
salida por turno, con clave `empleado_tipo_fecha_índice`, y al sonar calla si ese **día** ya
hay un fichaje del tipo: en una jornada partida los del segundo turno no suenan nunca.

En el modo:

- **Las alarmas se escriben con el día.** `regenerateGeneratedDay`, el único escritor de días
  (trigger de tareas y activación), reescribe también las alarmas de ese día: borra las que
  había de esa persona y fecha con `metadata.source = "tasks"` y crea las nuevas, una entrada
  y una salida por tarea, con clave `empleado_task_fecha_tipo_taskId`. Una tarea que se mueve
  mueve su alarma; una que se cancela la pierde; una creada a media mañana para la tarde
  tiene la suya sin esperar a las 04:00. Un día pasado no se toca.
- **La regla del hueco.** Los avisos van a −5, 0 y +5 minutos. Si entre el fin de una tarea y
  el inicio de la siguiente no caben los dos trenes (10 minutos o menos), se quitan la salida
  de la primera y la entrada de la segunda y queda **un solo aviso al inicio de la segunda**
  que dice las dos cosas: termina esta, empieza aquella.
- **Antes de sonar, la alarma pregunta a su tarea**, no a los fichajes: la de entrada calla si
  la tarea ya no está pendiente de empezar; la de salida, si la tarea ya está cerrada; las dos,
  si la tarea ya no existe, no es de la persona, o la persona ya no está en el modo.
- **El job de las 04:00 no planifica a quien está en el modo**: lo suyo ya lo escribió el día.
- **Los textos nombran la tarea:** `task_checkin_reminder`, `task_checkout_reminder` y
  `task_switch_reminder`, en español e inglés como el resto. WhatsApp sigue con sus plantillas
  aprobadas de siempre, que no se pueden cambiar sin pasar otra vez por Meta.

## 3. Lo que no cambia

Nadie fuera del modo: el job de las 04:00, sus claves, sus desfases y su `already_marked` siguen
igual. El planificador que dispara (`employeePlanifierWorker`, cada cinco minutos) es el mismo;
solo distingue las alarmas de tarea por `metadata.source`.

## 4. Pruebas

Unitarias de la función pura que decide las alarmas de un día (`planTaskAlarms`): tres tareas
con huecos de 5 minutos (un aviso de inicio, dos de cambio, uno de salida), dos con hueco largo
(cuatro trenes), y el día vacío. La escritura y el disparo, en dev: activar a una persona con
una tarea dentro de unos minutos y mirar `checkbiz_employee_planifiers`.

## 5. Hecho el 2026-10-16

`shared`: `taskAlarms.ts` (`planTaskAlarms`, pura, y `FirestoreTaskAlarmsWriter`),
`regenerateGeneratedDay` con `alarms` opcional, y los tres mensajes en `messages.ts` y
`CheckbizPushMessageFactory`. `firebase_sdk`: `onTaskDay` pasa el escritor; el job de las 04:00
salta a quien está en el modo; `executeEmployeePlanifier` trata `metadata.source = "tasks"`;
`taskStartNotificationWorker` no avisa a quien está en el modo. `checkinbiz`: la activación
también escribe las alarmas. 31 pruebas de `shared` en verde.

Comprobado contra el Firestore de `dev-encodebiz` con una persona ficticia: la consulta que borra
las alarmas viejas (`employeeId`, `metadata.source`, `metadata.planDate`, solo igualdades) va sin
índice compuesto; reescribir sin una tarea quita sus dos alarmas; la entrada de las 08:00 sale a
las 07:55 y el cambio de las 10:05 lleva un solo aviso. Borrado al acabar.

**Para que funcione en staging** hacen falta, a la vez: el contenedor `checkinbiz` de `develop`
(activación) y desplegar en `dev-encodebiz` con `--solo` `onTaskDay`,
`employeePlanifierWorker`, `planifierNotificationWorker` y `taskStartNotificationWorker`.

## 6. En staging, 2026-10-16

Por indicación de Jose, igual que la fase 2: merge a `staging` con `[skip ci]` (1ed0b71), y en el
servidor de desarrollo `git pull`, `up --build -d checkinbiz reports` y
`up -d --force-recreate nginx`. Desplegadas en `dev-encodebiz` con `--solo`: `onTaskDay`,
`employeePlanifierWorker`, `planifierNotificationWorker` y `taskStartNotificationWorker`.

QA `54-horario-por-tareas` contra staging: 15/15. Y en Firestore, las tareas de esa ejecución
generaron por el trigger real 5 alarmas de tarea —1 entrada, 3 salidas y 1 cambio de tarea— y
ninguna por turno del job de las 04:00.

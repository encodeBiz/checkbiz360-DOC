# TDR-006 — Tareas de varias personas en el horario por tareas

**Fecha:** 2026-10-22
**Estado:** Implementado el 2026-10-22 en `develop` (a3fb7bd) y `staging` (53e8c8b, a mano). Pendiente de producción.
**Componente:** `encodebiz-api` — `services/checkinbiz` (`tasksModeAttendance.ts`, `createChecklog`), `services/firebase_sdk` (`executeEmployeePlanifier`); `services/tasks` no cambia
**Decisiones de referencia:** [README](../README.md) D5 y D6; [TDR-003](./TDR-003-el-fichaje-mueve-la-tarea.md); [TDR-005](./TDR-005-alarmas-por-tarea.md); `tasks-service/08_pausas.md`

---

## 1. El hueco

El fichaje es de cada persona, pero en el modo lee y mueve el estado de la tarea entera. Con una
sola persona da igual. Con varias, la primera arrastra a las demás. Leído en el código de `main`
el 2026-10-22:

| Gesto | Qué pasa hoy con dos personas, A y B | Dónde |
|---|---|---|
| Entrar | Fichan los dos, pero solo la entrada de A inicia la tarea. Para B la tarea ya está en curso y el fichaje no la toca: su asignación se queda en `assigned`, sin hora de inicio, aunque esté trabajando | `createChecklog`: `if (type === "checkin" && status !== "in_progress")` |
| Descanso | La pausa es de la tarea, no de la persona (08_pausas D2). Si A descansa, la tarea queda en pausa para B, que sigue trabajando. Si B descansa después, no pasa nada. La primera que vuelve la reanuda aunque la otra siga de descanso | `restin` solo pausa si no está pausada; `restout` reanuda si lo está |
| Salir | La política por defecto es «basta con uno» (`any_assigned_worker`). La salida de A completa la tarea de los dos con B dentro. La salida de B entra, pero la tarea ya estaba cerrada | `moveTask(complete)`; `isClosedTask` en la salida |
| Alarmas | El aviso de entrada se calla en cuanto la tarea deja de estar pendiente: cuando entra A, B deja de recibirlo aunque no haya llegado. El de salida se calla cuando A completa | `executeEmployeePlanifier`: `task.status !== "assigned"`, `CLOSED_TASK` |

Consecuencia: el tiempo de la tarea, su cumplimiento (`on_time` / `late`), lo que ve el
supervisor y la actividad cuentan una sola persona. Los fichajes de cada uno sí están bien: el
registro de jornada y el informe no se ven afectados.

## 2. La regla

**En el modo, el fichaje mueve la parte de cada persona. La tarea entera solo cambia cuando el
cambio es de todos.**

La pieza ya existe: cada tarea tiene una asignación por persona (`TaskAssignment.status`:
`assigned`, `working`, `completed`…), y el servicio de tareas ya la mueve por persona al iniciar
y al completar su parte («todos completan», HAL-36). Lo que falta es que el fichaje la use.

### 2.1 Entrar

Siempre se pide iniciar, aunque la tarea ya esté en curso, salvo que **la asignación de esa
persona** ya esté `working` o `completed`. `updateTaskStatus` ya admite `in_progress →
in_progress` y en ese caso marca la asignación del que llama como `working` con su hora. La
comprobación previa (`startableProblem`) mira además que la parte de esa persona no esté
completada.

### 2.2 Salir

En el modo, Salir completa **la parte de quien sale**, y la tarea se completa cuando sale la
última persona que tiene parte, sea cual sea la política de la tarea. Es la regla «todos
completan», que ya está hecha: el fichaje pide al servicio de tareas que la aplique a esta
llamada (`completionPolicy: "all_assigned_workers"` solo para el gesto delegado del fichaje; la
tarea guardada no cambia). Fuera del modo, y desde el panel, la política de siempre.

Si la parte de esa persona ya está completada, o la tarea cerrada por el supervisor, Salir no la
toca, como hoy.

### 2.3 Descanso

La pausa sigue siendo de la tarea (08_pausas D2 no cambia). Lo que cambia es cuándo:

- **Descanso** pausa la tarea solo si nadie más está trabajando en ella: ninguna otra asignación
  `working` sin descanso abierto.
- **Fin de descanso** reanuda la tarea si estaba pausada, que es el caso de quien vuelve el
  primero de un descanso de todos.

El descanso de cada persona sigue escrito en su fichaje y descuenta en su informe, que es donde
cuenta la nómina. Lo que deja de pasar es que el descanso de uno pause el trabajo de otro.

Se descartó la pausa por persona (una pausa en cada asignación): cambia el modelo de pausas,
que ya está en producción y en la app, por un caso que la regla de arriba resuelve sin tocarlo.

### 2.4 Alarmas

Antes de sonar, la alarma pregunta a **la asignación de su persona**, no a la tarea: la de
entrada calla si esa persona ya está `working` o `completed`; la de salida, si su parte está
completada o la tarea cerrada por el supervisor.

## 3. Lo que no cambia

Las tareas de una sola persona, que hoy van bien: todas las reglas de arriba dan lo mismo con una.
El panel, la validación, el rechazo y la puntuación del supervisor. El servicio de tareas: todo
lo que hace falta ya lo tiene, salvo aceptar que el gesto delegado del fichaje pida «todos
completan» (§2.2), que es un campo opcional en la llamada.

## 4. Pruebas

QA `54-horario-por-tareas`, casos nuevos con una tarea de dos personas, A y B, las dos en el modo:

| Caso | Esperado |
|---|---|
| A entra, B entra | Las dos asignaciones `working` con su hora; la tarea `in_progress` |
| A descansa | La tarea no se pausa (B sigue trabajando) |
| A y B descansan | La tarea se pausa al descansar la segunda; se reanuda al volver la primera |
| A sale | La parte de A `completed`; la tarea sigue `in_progress` |
| B sale | La tarea `completed` |
| Alarma de entrada de B con A ya dentro | Suena (la parte de B sigue `assigned`) |

Y una tarea de una sola persona con todos los pasos, para fijar que no cambia nada.

## 5. Hecho el 2026-10-22

Rama `feat/horario-por-tareas-varias-personas` (empujada). `checkinbiz`: `tasksModeAttendance.ts`
(`loadMyAssignment`, `isClosedForMe`, `myPartStarted`, `someoneElseWorking`, y `completionPolicy`
en el gesto de Salir) y `createChecklog`. `tasks`: `updateTaskStatus` acepta «todos completan»
por la puerta delegada y **un segundo inicio no reescribe el cumplimiento de plazo** (se fija con
el primero). `firebase_sdk`: la alarma mira la asignación de su persona.

**Antes de escribirlo, qué lee cada cosa que cambia** (Jose: «que no rompa estadísticas ni
analítica»): el espejo `tasks_raw` solo guarda la tarea entera, no la parte de cada persona; el
dashboard operativo lee estado, pausa abierta y completado, y no el cumplimiento (ADR-005); el
informe de tareas, inicio, fin, pausas y su número; los patrones, el cumplimiento y el inicio al
validar. Con el cambio: la tarea se ve en curso hasta que sale la última, en pausa solo cuando
para todo el equipo, el tiempo va de la primera entrada a la última salida, y el cumplimiento
se fija con el primer inicio y se recalcula al completar. Las tareas de una persona, igual.

**Validado en staging:** typecheck de shared, checkinbiz, tasks, firebase_sdk, analytics, reports
y merlin; 85 pruebas de shared y 5 de reports. QA contra staging: 135/135 (horario por tareas con
HPT-16-01..03, las seis de tareas, informes y espejo con programadas) y 28/28 (dashboard
operativo y panel). `employeePlanifierWorker` desplegada en `dev-encodebiz`.

**Para producción:** contenedores `checkinbiz` y `tasks`, y `employeePlanifierWorker` con
`--solo`. Sin migraciones.

# TDR-007 — «Calendario»: turnos cargados por fecha, con fichaje normal

**Fecha:** 2026-10-22
**Estado:** Diseño cerrado en conversación con Jose el 2026-10-22; implementación en `feat/horario-calendario` de `encodebiz-api` (worktree)
**Componente:** `encodebiz-api` — `packages/shared` (calendar), `services/checkinbiz` (calendar), `services/firebase_sdk` (`weeklyFromTaskDays`), `services/analytics` (espejo, migración 043), `services/merlin` (cuadrantes `aplicar`), `services/assistant` (`cambiar_modo_horario`); `encodebiz-front-saas` (selector y calendario semanal de turnos)
**Decisiones de referencia:** [README](../README.md) D1, D3, D11 y **D12**; [TDR-001](./TDR-001-modo-dias-generados-y-escritor.md) §3, §5 y §7

---

## 1. De dónde sale

Un cliente que ya ficha por tareas (bien para el personal de obra y de oficina) no consigue
organizar el cuadrante: generó tareas para hacer de turnos, no puede meter nada dentro de una
tarea y lo encuentra lioso. Lo que pide, con sus palabras: «generar horarios, como si fuesen a
turnos de forma mensual, que fichen normal y dentro de esos horarios meter las tareas».

Lo que hay hoy no lo permite. El horario semanal es una plantilla de siete días que se repite
(TDR-001, punto 1 de lo comprobado): no hay dónde decir que el martes 21 tiene un turno y el
martes 28 otro. El importador de cuadrantes lo sortea escribiendo una semana y dejando que la
siguiente la pise. Y en «Horario por tareas» el contenedor es la tarea, que es justo lo que al
cliente le sobra.

Lo que sí hay, desde la fase 1, es casi todo lo demás: los días por fecha de cada persona
(`calendar_days`), el resolutor que los lee antes que la plantilla, el espejo a Postgres, la
disponibilidad que los cruza, el planificador de alarmas que resuelve el día siguiente con ese
mismo resolutor, y la plantilla semanal sincronizada desde los días (D11) para que la app pinte
la semana correcta. Todo eso está condicionado a que el modo sea `tasks`. Este TDR lo abre a un
tercer modo que no depende de las tareas.

## 2. La regla

> **En «Calendario», el horario de una persona es lo que se ha cargado por fecha. Un día sin
> cargar es libre. La persona ficha con el gesto de siempre contra esos turnos, y las tareas de
> ese día son tareas normales, dentro del turno.**

Y lo que no cambia: el fichaje no mueve ninguna tarea (eso es solo de `tasks`); la semana tipo
no se usa en el modo salvo como espejo de la semana activa (D11); los días pasados no se
reescriben nunca (TDR-001 §3.4).

Por qué un tercer modo y no «la semana tipo con fechas encima». Se discutió el 2026-10-22 y se
descartó la segunda: con la plantilla de respaldo, una persona tendría turno un martes que
nadie le cargó, y a quien planifica mes a mes eso le parece un fallo. Un cuadrante significa
que si no estás en él, no trabajas. Es la misma semántica que ya tiene `tasks` (sin tareas no
hay jornada), así que no hay dos estados que explicar.

## 3. El modo

### 3.1 Valor y nombre

`ScheduleMode` gana `calendar`. En el panel es la tercera opción del selector «Cómo se organiza
el horario», con la etiqueta **«Calendario»** (decidido por Jose): «Horario semanal», «Horario
por tareas», «Calendario». En inglés «Calendar», portugués «Calendário», alemán «Kalender».

### 3.2 Niveles y cascada

A diferencia de `tasks`, **`calendar` se puede poner en la empresa, en la sucursal y en el
empleado**, y se hereda con la cascada de siempre: gana el nivel más cercano que tenga valor.
Un cuadrante se planifica por sucursal, así que es ahí donde tiene sentido activarlo; la
administrativa de esa sucursal se queda en `weekly` poniéndoselo en su ficha.

`tasks` sigue siendo solo del empleado (D1, 2026-10-16): en empresa y sucursal se responde
`400 calendar/schedule_mode_employee_only` **solo para `tasks`**; `calendar` y `weekly` se
aceptan en los tres niveles. Si por cualquier vía quedara `tasks` escrito en una sucursal o en
la empresa, el resolutor lo ignora: no hay forma de generar días desde tareas a nivel de grupo.

`resolveScheduleMode(entityCal, branchCal, employeeCal)` devuelve `{mode, source}` con `source`
en `entity | branch | employee`. `EffectiveCalendarOutput.sources.scheduleMode` lo expone, como
hasta ahora.

### 3.3 Activar y desactivar

Poner `calendar` no comprueba nada ni genera nada: los días los carga alguien después. Al
activarlo en una sucursal, **todo el que no tenga cuadrante cargado pasa a tener los días
libres** y el fichaje le responderá `checklog/day_disabled`. Es lo correcto, y el panel lo
avisa al activar y enseña en rojo a quién le falta semana (§8); no se bloquea nada.

Quitar `calendar` no borra días: dejan de leerse, como en `tasks` (TDR-001 §2.2). Pasar de
`tasks` a `calendar` conserva los días que las tareas generaron, con sus `taskId`; en
`calendar` se leen como turnos normales y el fichaje no mueve esas tareas. Pasar de
`calendar` a `tasks` sí regenera desde tareas, como cualquier activación de `tasks`.

## 4. Los días cargados

Misma subcolección, mismo documento: `entities/{e}/employees/{p}/calendar_days/{YYYY-MM-DD}`
(TDR-001 §3). Cambia lo mínimo:

```ts
type GeneratedShift = {
  start: DayTime; end: DayTime;
  taskId?: string;   // antes obligatorio: solo lo lleva un turno que forma una tarea
  title?: string;
  branchId: string;  // la sucursal del turno: en «Calendario», la del cuadrante que se carga
};
type GeneratedDay = {
  …;
  taskIds: string[];              // los turnos con tarea; vacío en «Calendario»
  generatedBy: "tasks_trigger" | "mode_activation" | "panel" | "cuadrante";
};
```

Nada se borra: un día que se deja sin turnos se escribe con `shifts: []`, que es «libra». Un
día sin documento también libra. Las dos cosas significan lo mismo para el fichaje; la única
diferencia es que la segunda no ha pasado nunca por nadie, y el panel la pinta como «sin
cargar» para que se note.

**Un solo escritor por modo.** En `tasks` sigue escribiendo el trigger de tareas, y nada más.
En `calendar` escriben el panel (por la ruta de §5) y el importador de cuadrantes (§7), y el
trigger de tareas no toca a quien está en `calendar` (ya hoy sale si el modo no es `tasks`).
Crear una tarea a alguien en `calendar` no cambia su día.

## 5. Las rutas, en `checkinbiz`

Bajo `/calendar`, con la misma puerta que el resto del módulo (`requireFirebaseAuth` y la
delegada `requireDelegatedUser`).

### 5.1 Leer

```
GET /calendar/days?entityId&employeeId&from&to      → una persona
GET /calendar/days?entityId&branchId&from&to        → todas las personas de la sucursal
```

`from` y `to` fechas locales `YYYY-MM-DD`, ambas incluidas, 62 días como mucho. Responde
`{code: "calendar/days", data: {days: GeneratedDay[]}}`, ordenados por persona y fecha. Por
sucursal es **una** consulta de grupo (`listForEntity`, índice `calendar_days` (entityId,
date) que ya existe) filtrada por las personas activas de esa sucursal. Permiso: el alcance del
actor como en la disponibilidad (`resolveActorScope`): asiento, o responsabilidad sobre la
sucursal; una persona leyendo su propio mes ya tiene `GET /calendar/me/month`.

### 5.2 Escribir

```
PUT /calendar/days
{
  entityId, employeeId, branchId,
  days: [{date: "2026-11-03", shifts: [{start: {hour: 8, minute: 0}, end: {hour: 14, minute: 0}}, …]}, …]
}
```

Permiso: `requireCalendarWriter` con ámbito empleado (asiento, o supervisor de alguna sucursal
de la persona). Reglas, todas con `400`:

| Qué | Código |
|---|---|
| La persona no está en `calendar` (modo resuelto) | `calendar/days_require_calendar_mode` — escribir días que nadie va a leer sería el fallo silencioso |
| Una fecha anterior a hoy, en la zona efectiva de la persona | `calendar/day_in_the_past`, con las fechas en `details.dates`; hoy sí se puede tocar |
| Más de 400 días hacia delante, más de 100 días en una llamada, fecha mal formada | `calendar/bad_request` |
| Un turno con fin no posterior al inicio, horas fuera de rango, o dos turnos que se cruzan | `calendar/bad_request`, con el día en el mensaje |

Escribe un documento por fecha (`set` sin merge, como el trigger), `generatedBy: "panel"`,
`taskIds: []`, turnos ordenados por inicio. Si alguna fecha cae en la semana activa de la
persona, después de escribir llama a `sincronizarPlantillaDeLaSemana` (D11) en la misma
petición, para que la app y el panel enseñen la semana al momento; un fallo ahí se registra y
no deshace los días. Responde `{code: "calendar/days_upserted", written, weekMirrored}`.

Lo que **no** hace: no borra nada, no toca otras fechas que las que vienen, no crea tareas.

## 6. Lo que cambia en la lectura

- `ResolveEffectiveDayUseCase`: la rama que hoy entra con `scheduleMode === "tasks" && employeeId`
  entra con `tasks` **o** `calendar`. Devuelve `scheduleMode` tal cual y `sources.schedule`
  igual al modo (`"tasks"` o `"calendar"`); el tipo de `ScheduleApplied.source` del checklog
  gana `"calendar"`. El resto, idéntico: semana sintetizada de siete días, `isWorkingDay`,
  `generatedDay`.
- `ResolveAvailabilityUseCase`: lee los días generados si alguien está en `tasks` o en
  `calendar`, y **también si el modo viene de la sucursal o de la empresa** (hoy mira solo las
  fichas; con la cascada tiene que resolver el modo de cada par). `buildPair` usa los días en
  los dos modos.
- `createChecklog`: `tasksMode` sigue siendo `scheduleMode === "tasks"`. En `calendar` el
  fichaje es el normal: tolerancia de la empresa, sin mover tareas, descanso fijo de la
  sucursal como en `weekly`.
- Planificador de las 04:00 (`checkActiveEmployeeWorker`): sin cambios. Resuelve el día con el
  mismo resolutor, así que ve los turnos cargados y crea los recordatorios de entrada y salida
  por turno; solo sale si el modo es `tasks`, que tiene sus alarmas por tarea. La limitación
  del `already_marked` por día (TDR-001, punto 4) sigue ahí para la jornada partida.
- `weeklyFromTaskDays` (D11, cron 03:00 y 15:00): copia la semana activa a la plantilla propia
  para quien está en `tasks` **o** en `calendar`. Es lo que hace que la app pinte la semana sin
  publicar nada.
- Postgres: `dim_calendars.schedule_mode` admite `calendar` (migración 043, `DROP` + `ADD` del
  CHECK), el espejo copia el modo de los tres niveles (ya lo hacía; ahora los repositorios de
  entidad y sucursal lo devuelven), y `PostgresCalendarRepository` resuelve con la misma
  cascada. `dim_calendar_days.generated_by` es `VARCHAR(20)`: `panel` y `cuadrante` caben.

## 7. El importador de cuadrantes (D10, ampliada)

`aplicar` en `services/merlin/src/soporte/cuadrantes/application/aplicar.ts` decide por el modo
resuelto de la persona:

| Modo | Horario | Tareas |
|---|---|---|
| `weekly` | la semana tipo, como hoy | una por servicio |
| `tasks` | nada: el trigger genera los días | una por servicio |
| `calendar` | **un día por fecha** de la propuesta: la franja del día (primera a última hora, `p.dias[i].inicio`–`fin`), `shifts: []` si viene vacío; `generatedBy: "cuadrante"`; fechas pasadas se saltan | una por servicio |

Escribe con `FirestoreGeneratedDaysRepository` de shared (merlin ya usa shared para el
calendario) y, si alguna fecha cae en la semana activa, sincroniza la plantilla (D11). La
plantilla de sucursal (cuadrantes TDR-001) pasa por el mismo `aplicar`, así que un Excel con un
mes entero carga el mes de cada persona: la plantilla ya dice que mandan las fechas que se
escriben. **El importador no cambia el modo de nadie**: si la sucursal está en `calendar`, las
personas lo heredan; si no, se comporta como hasta ahora.

## 8. El panel (`encodebiz-front-saas`)

Decidido por Jose el 2026-10-22, con sus palabras: «pongo Horario semanal, Horario por tareas,
Calendario y que se haga igual que el calendario semanal de tareas con el mismo componente pero
en vez de asignar una tarea asignas un horario».

- **Selector**: la tercera opción «Calendario» en `CalendarSection` (Horarios y festivos de la
  empresa, de la sucursal y del empleado). Para `tasks` el selector sigue solo en el empleado.
  Al elegir «Calendario» en empresa o sucursal, un aviso en el propio guardado: «Quien no tenga
  turnos cargados tendrá el día libre hasta que se le carguen».
- **Calendario de turnos**: el mismo componente del calendario semanal de tareas
  (`TaskWeekCalendar`), con turnos en vez de tareas: navega por semanas, una fila por persona en
  la sucursal (o la persona sola en su ficha), una tarjeta por turno. Añadir un turno a un día
  es pinchar en el hueco; un día puede llevar varios (partido). Copiar la semana a la siguiente.
  Lee con `GET /calendar/days` y guarda con `PUT /calendar/days`. Un día pasado se pinta y no
  se edita. Un día «sin cargar» se distingue de «libre».
- **Tarea desde el turno**: en la tarjeta del turno, «Crear tarea», que abre el alta de tarea
  con la persona, la sucursal, la fecha y la franja ya puestas. Es una tarea normal.
- **Importar**: los botones que ya existen (ficha de sucursal y de empleado) no se mueven; el
  resultado cambia solo en el servidor (§7).
- **La app**: no se toca ni se publica nada. Ficha con el gesto normal y pinta la semana desde
  la plantilla, que el espejo ya reescribe.

## 9. El asistente (MCP)

`cambiar_modo_horario` admite `modo: "calendario"` y, para `calendario` y `semanal`, un
`sucursalId` en vez de `personaId` (para `tareas` sigue siendo solo persona). `cambiar_horario`
(la semana tipo) responde `horario_por_calendario` a quien está en el modo, como hoy responde
`horario_por_tareas`: los turnos se cargan por fecha en el panel.

## 10. Inventario de cambios

| Sitio | Qué |
|---|---|
| `packages/shared/src/calendar/Calendar.ts` | `calendar` en `ScheduleMode`; `scheduleMode` en `BaseCalendar`; `taskId`/`title` opcionales en `GeneratedShift`; `generatedBy` ampliado |
| `packages/shared/src/calendar/scheduleMode.ts` | cascada por nivel más cercano; `tasks` solo cuenta en el empleado; `isScheduleMode` |
| `packages/shared/src/calendar/resolveEffectiveCalendar.usecase.ts`, `resolveEffectiveDay.usecase.ts`, `resolveAvailability.usecase.ts` | §6 |
| `packages/shared/src/calendar/loadedDays.ts` (nuevo) | validación y construcción pura de los días cargados (`buildLoadedDay`), con pruebas |
| `packages/shared/src/checkbiz/entities/CheckLog.ts` | `source: "calendar"` |
| `services/checkinbiz/.../calendar/days.controller.ts` (nuevo), `calendar.router.ts`, `scheduleMode.helpers.ts`, los tres `upsert*Calendar` | §5 y §3 |
| `services/firebase_sdk/src/calendario/syncWeeklyFromTaskDays.ts` | los dos modos |
| `services/analytics`: `migrations/043_horario_calendario.sql`, `SyncDimensions.ts`, `PostgresCalendarRepository.ts`, `PostgresAvailabilityRepository.ts` | §6 |
| `services/merlin/.../cuadrantes/application/aplicar.ts` | §7 |
| `services/assistant`: `domain/core.ts`, `infrastructure/PlatformCore.ts`, `mcp/tools/cambios.ts` | §9 |
| `qa/tests/con-datos/55-horario-calendario.spec.ts` (nuevo) | §11 |

Nada de lo anterior cambia la forma de lo que ya existe para `weekly` ni para `tasks`: valores
nuevos en uniones, campos opcionales, rutas nuevas. Nadie cambia al desplegar: sin valor sigue
siendo `weekly`.

## 11. Pruebas

**Unitarias, en shared** (`node:test`): la cascada del modo (empleado > sucursal > empresa;
`tasks` ignorado fuera del empleado); `buildLoadedDay` (orden, solape, fin antes del inicio,
día vacío); el resolutor del día en `calendar` (con documento, sin documento, semana
sintetizada); la disponibilidad con el modo heredado de la sucursal.

**QA, Playwright, `qa/tests/con-datos/55-horario-calendario.spec.ts`**, con la técnica de la
54: la sucursal en una zona donde ahora son las 12.

| Caso | Qué comprueba |
|---|---|
| HCA-01 | La sucursal pasa a `calendar`; una persona sin días cargados: `scheduleMode` `calendar` con `sources.scheduleMode` `branch`, día cerrado, la entrada responde `checklog/day_disabled` |
| HCA-02 | `PUT /calendar/days` con un turno de hoy que cubre ahora: `GET /calendar` lo enseña con `sources.schedule` `calendar`; la entrada entra y congela `source: "calendar"` y los minutos planificados |
| HCA-03 | `GET /calendar/days` por sucursal devuelve su día; la disponibilidad del día la ve esperada con ese turno |
| HCA-04 | Una fecha pasada → `calendar/day_in_the_past`; turnos cruzados y fin antes del inicio → `calendar/bad_request`; una persona en `weekly` → `calendar/days_require_calendar_mode` |
| HCA-05 | El mismo día se reescribe con `shifts: []`: día cerrado y la entrada rechazada |
| HCA-06 | Una compañera con `weekly` en su ficha sigue con la plantilla de la sucursal (`sources.scheduleMode` `employee`) |
| HCA-07 | `tasks` en la sucursal sigue dando `calendar/schedule_mode_employee_only`; `calendar` en la empresa se acepta |
| HCA-08 | Tras cargar la semana activa, `data.weeklySchedule` del `GET /calendar` lleva el turno del día de hoy (D11 en la misma petición) y `overridesDisabled` es `false` |

## 12. Pase a producción

Va como PENDIENTE en `DOCS/deployment-prod/proximo-pase-back.md` §15. Resumen: migración 043 a
mano; contenedores `checkinbiz`, `analytics`, `merlin`, `assistant` (y `tasks`, `reports` solo
por rebuild de shared); `weeklyFromTaskDays` con `desplegar.mjs --project encodebiz-services
--solo weeklyFromTaskDays`; sin reglas ni índices nuevos; panel detrás del back.

## 13. Fuera de este TDR

Un patrón de rotación («semana A, semana B, cada cuatro semanas») que genere el mes solo: se
carga a mano o por Excel; si el cliente lo pide, es otro TDR. Que la salida exija las tareas del
turno completadas: no, la tarea es una lista de trabajo y el fichaje es el registro legal. El
cuadrante de un ERP en matriz: sigue fuera (cuadrantes, «lo que queda por decidir»).

# Horario por tareas — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — calendario y fichaje · tasks · alarmas (firebase_sdk) · reports · analytics · app móvil
**Fecha de inicio:** 2026-10-15
**Estado:** En producción: API, funciones y panel desde el 2026-10-17 (pase §1); después TDR-006 a TDR-009, todos en prod el 2026-10-22. app en `master` 1.10.0+68, publicada en tiendas. Registro en `deployment-prod/proximo-pase-back.md`
**Autor:** Jose Acevedo

---

## Contexto y Motivación

Hay empresas cuya jornada no es un horario sino una lista de trabajos: ayuda a domicilio,
limpieza por centros, mantenimiento, obra. La persona no entra a las 8 y sale a las 17; va a
tres sitios, cada uno a su hora, y entre uno y otro no está trabajando. Hoy checkbiz360 les
obliga a escribir un horario además de las tareas, y las dos cosas dicen lo mismo con
palabras distintas. La importación de cuadrantes ya lo sufrió: calcula la franja del día a
partir de las tareas y la escribe como horario, y en cuanto una tarea se mueve el horario
miente.

Lo que se decide aquí es que, para quien lo active, **el horario se genera a partir de las
tareas y el fichaje se hace a través de ellas**. Se gana versatilidad sin inventar un segundo
modelo: el calendario ya sabe de días con varios turnos, el fichaje ya elige el turno en el
que cae la hora, y las alarmas, los informes y las alertas ya consumen turnos sin preguntar
de dónde vienen.

## Principio de diseño

> **Cada tarea es un turno. El horario se genera, no se escribe a mano. El fichaje sigue
> siendo el gesto y el registro legal; la tarea va detrás.**

Y una regla sobre quién escribe: **un solo escritor**. El día generado de una persona lo
regenera un trigger sobre la colección de tareas, venga la escritura de donde venga. Nadie
tiene que acordarse de regenerar nada.

## Alcance

**Dentro:** un modo explícito del horario, heredado por entidad, sucursal y empleado; los días
generados por fecha en el calendario del empleado y su espejo en Postgres; el fichaje que
inicia y completa la tarea del turno con un solo gesto; las alarmas por tarea; dos líneas
nuevas en el informe de jornada, la jornada y los huecos entre turnos; las reglas que hacen
a una tarea incompatible con el modo; y lo que cambia en la app.

**Fuera:** fundir tareas con hueco corto en un mismo turno (decidido que no, ver D2); turnos
que cruzan la medianoche, que el fichaje de hoy tampoco admite; cualquier cambio en el
flujo del supervisor, que queda intacto (D5); y cambiar nada a los clientes que no activen
el modo.

## Lo que se comprobó en el código antes de decidir

Esto es lo que había, leído el 2026-10-15. Cada decisión de abajo se apoya en uno de estos
puntos; sin ellos el diseño sería otro.

1. **El calendario es una plantilla semanal, no un calendario por fechas.**
   `WeeklySchedule` en `packages/shared/src/calendar/Calendar.ts` tiene siete claves, lunes a
   domingo. No hay dónde guardar que el martes 21 tiene tres turnos y el martes 28 dos. La
   importación de cuadrantes convive con ello escribiendo una semana y dejando que la
   siguiente la pise (`services/merlin/src/soporte/cuadrantes/application/horario.ts`), y el
   pasado no sufre porque cada fichaje congela su día.

2. **El fichaje ya sabe vivir sin horario y ya sabe de varios turnos.** Sin ninguna semana
   configurada aplica una ventana abierta de 00:00 a 23:59 marcada `source: "default"`
   (`packages/shared/src/calendar/defaultDay.ts`). Con horario, elige el turno en el que cae
   la hora, admite la entrada desde `notifyBeforeMinutes` antes (15 por defecto), congela en
   el checklog el día entero con `plannedMinutes` y `weekPlan`, y fija el plazo de jornada
   incompleta en el fin del turno más seis horas
   (`services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts`).

3. **La tarea depende hoy de la jornada, no al revés.** Iniciar o completar una tarea desde la
   app exige jornada abierta: `task/no_open_session`
   (`services/tasks/src/interfaces/http/task/task.helpers.ts`, `ensureOpenWorkSession`). El
   back office está exento. Pausar es libre; reanudar pide jornada y geocerca.

4. **Las alarmas de fichaje nacen de madrugada y se apagan por día, no por turno.** El job
   de las 04:00 (`services/firebase_sdk/src/programadas/checkActiveEmployeeWorker.controller.ts`)
   lee el día siguiente, crea un recordatorio de entrada y otro de salida por turno con
   desfases −5, 0 y +5 minutos, con clave `empleado_tipo_fecha_índice`, y marca
   `lastDayPlanned` para no repetir. Al disparar
   (`executeEmployeePlanifier.controller.ts`) busca si ese día ya hay un fichaje válido del
   mismo tipo y, si lo hay, calla con `already_marked`. **Mira el día entero, así que en una
   jornada partida los recordatorios del segundo turno nunca suenan.** Leído en código, no
   reproducido en producción. El aviso de tarea no iniciada es otro worker
   (`taskStartNotificationWorker.ts`), a los 15 minutos de `scheduledStartAt`.

5. **La tarea solo tiene obligatorio el vencimiento.** `scheduledStartAt` es opcional en
   `packages/shared/src/checkbiz/entities/Task.ts`.

6. **El informe de jornada es una tabla plana por ciclo.** `BuildEmployeeDailyReports.ts`
   calcula por ciclo bruto, descansos y neto; con descanso fijo (`disableBreak` y
   `timeBreak`) **resta el fijo en cada ciclo**. El PDF y el Excel pintan una fila por ciclo:
   Fecha, Entrada, Salida, Descanso (min), Horas netas, Ajustado, Estricto, y un total de
   horas trabajadas. Nada agrupa por día.

7. **Las alertas no miran el horario en vivo.** Los avisos de patrón y de ventana los decide
   el trigger del SaaS a partir de lo congelado en el checklog
   (`CheckbizOperationals.ts`); «no vino» y «llegó tarde» las calcula analytics cruzando
   quién debía venir, que sale del calendario espejado en Postgres
   (`BuildOperationalDay.ts`), con quién fichó; el sanitizador cierra por el plazo del
   checklog; los eventos `attendance.clock_rejected` y `workday.closed` llevan motivo y
   minutos planificados del propio registro.

8. **Firebase no llega a Postgres.** Postgres no está expuesto fuera de la red de
   contenedores, y las alarmas corren en Firebase.

## Decisiones

### D1. Un modo explícito del horario, heredado, que se llama «Horario por tareas»


> **Cambiado el 2026-10-16, por decisión de Jose:** el modo es **solo de cada empleado**.
> Nadie comparte tareas con nadie, así que heredarlo de la empresa o de la sucursal no tiene
> sentido. Solo la ficha del empleado lo fija; la empresa y la sucursal responden 400
> `calendar/schedule_mode_employee_only`, y el panel solo enseña el selector en la ficha del
> empleado. Lo que este documento diga de herencia por niveles queda sustituido por esto.

El modo es un valor del calendario, no un interruptor suelto, y se hereda como el resto:
entidad, sucursal, empleado. Es distinto de «sin horario», que hoy abre el día entero y hace
que el panel avise de que falta configurar. El interruptor puede ponerse en la sucursal para
no activarlo veinte veces; **lo generado vive siempre en el empleado**, porque las tareas son
de personas.

**Nombre** (decidido el 2026-10-15). Se llama «Horario por tareas», y en el panel no es un
interruptor sino una elección entre dos cosas que la empresa ya entiende, en Horarios y
festivos: «el horario lo marca la semana» o «el horario lo marcan las tareas», con etiquetas
cortas «Horario semanal» y «Horario por tareas». Se descartaron «modo tareas», que cuenta
mecánica del sistema; «jornada por tareas», que en lenguaje laboral sugiere que la jornada
legal es cada tarea, cuando lo que se parte es el horario; y «turnos por tarea», que suena a
industria de turnos. En los otros idiomas: inglés «Weekly schedule» y «Schedule from tasks»,
portugués «Horário semanal» y «Horário por tarefas», alemán «Wochenplan» y «Zeitplan aus
Aufgaben».

**Campo.** Un solo campo en el calendario, en los tres niveles y heredado como el resto:
`scheduleMode`, con valores `weekly` y `tasks`. Sin valor es `weekly`, así que nadie cambia
al desplegar.

### D2. Cada tarea es un turno; no se funden

El día de una persona en el modo es la lista de sus tareas de esa fecha, cada una un turno
de `scheduledStartAt` a `dueAt`. Entre dos turnos la persona está fuera, y ese hueco no es
tiempo trabajado. Se descartó fundir tareas con hueco corto: el hueco se enseña en el
informe (D8) y la empresa decide qué hace con él.

Consecuencia para ayuda a domicilio: con el lunes real del cuadrante de ServiSAD, tres
servicios de 8:00 a 10:00, 10:05 a 12:05 y 12:10 a 14:40, hoy el horario es un turno de 8:00
a 14:40 y la jornada mide 6 h 40, lo mismo que imprime el papel. En el modo son tres turnos
y lo trabajado suma 6 h 30; los 10 minutos de calle quedan fuera. **A ese cliente no se le
cambia nada**: el modo es opcional, y pasarse a él es una decisión de nómina suya.

### D3. Los días generados se guardan por fecha, en Firestore, y se espejan en Postgres

Se materializan, no se calculan al leer, por dos razones: un día ya pasado **no se regenera
nunca**, y eso deja constancia de lo que estaba planificado aunque nadie fichara, que hoy
solo existe cuando hay un fichaje que lo congele; y lo que lee el panel sale de Postgres,
que es donde la analítica ya cruza esperados con fichados.

Viven en Firestore porque el fichaje resuelve el día contra Firestore y las alarmas corren
en Firebase (punto 8). Una subcolección de días por empleado, un documento por fecha
`YYYY-MM-DD`, con sus turnos y la tarea de cada uno. El resolutor del día efectivo, en el
modo, mira esa subcolección antes que la plantilla semanal; sin documento para esa fecha,
el día está cerrado: sin tareas no hay jornada. La plantilla semanal no se toca en el modo,
así que no hay días que «pisar» ni aviso que dar. El espejo a Postgres va como el resto del
calendario, y el resolutor de analytics lee de ahí.

**Un solo escritor.** Un trigger de Firestore sobre `tasks` regenera el día de cada asignado
afectado, el de antes y el de después si la tarea cambió de fecha o de persona, y con él las
alarmas de ese día (D7). Cubre el panel, la app, el cuadrante, el sync de Rentman y las
tareas de sistema sin que ninguno sepa que existe. Qué estados cuentan queda en «Lo que
queda por decidir».

### D4. Lo que es incompatible con el modo se rechaza

Para quien está en el modo, al crear o editar una tarea se rechaza, con código propio:

- una tarea que empieza y vence en fechas locales distintas (el fichaje de hoy tampoco
  admite un turno que cruce la medianoche);
- una tarea sin hora de inicio, porque un turno sin inicio no existe;
- una tarea que se solape en el tiempo con otra de la misma persona, porque Entrar tiene que
  arrancar una sola. Dos cosas a la vez en el mismo sitio son una tarea con una lista en la
  descripción, que ya existe en Markdown.

Y al activar el modo a alguien que ya tiene tareas así, se rechaza también y la respuesta
las enumera. Vale igual para las tareas que escribe el sync de Rentman: si un proyecto genera
tareas de más de un día o solapadas, esa persona **no entra en el modo**; el adaptador no las
parte (decidido el 2026-10-15).

### D5. El fichaje manda; la tarea va detrás

El gesto es el de siempre. En el modo, **Entrar inicia la tarea del turno, Salir la completa,
Descanso la pausa y Fin de descanso la reanuda.** Los botones de iniciar y completar de la
tarea desaparecen de la app; la pantalla de la tarea sigue para leerla, dejar notas y subir
evidencias. Explícito en los dos lados: el botón dice qué va a hacer («Entrar · Limpieza en
calle Albuñuelas, 10:05»); el fichaje guarda la tarea que arrancó, la tarea guarda el fichaje
y su historial anota «iniciada por fichaje».

Qué tarea arranca Entrar lo decide el fichaje como hoy: el turno en el que cae la hora, con
sus quince minutos de margen por delante, y en el modo cada turno lleva su tarea. Si no hay
ninguna a esa hora, el rechazo es el `out_of_schedule` de siempre, con el mismo evento y
motivo, pero el texto dice «no tienes ninguna tarea ahora».

Orden: primero el fichaje, con todas sus comprobaciones, ausencia, festivo, geocerca de la
sucursal, secuencia; después la tarea. Si el fichaje falla, la tarea no arranca y el error es
el del fichaje. Si la tarea fallara después, la jornada queda abierta y repetir Entrar
funciona, que es el fallo bueno. La app manda posición siempre, también en tareas sin lugar
propio, porque ahora es un fichaje. Salir completa la tarea y, si la tarea exige algo al
completar, la app lo pide en la salida.

Iniciar una segunda tarea con otra en marcha no vuelve a fichar, y completar una mientras
otra sigue abierta no cierra; en el modo no debería ocurrir por D4, pero el servidor no
depende de que no ocurra. En tareas de varias personas con política de que completen todas,
el Salir de cada una cierra su turno y marca su parte, y la tarea se completa cuando sale la
última: el turno es de la persona, el estado es de la tarea.

**El supervisor queda intacto.** El fichaje solo dispara las transiciones que ya son del
trabajador. Validar, rechazar con motivo, puntuar, notas, cancelar y completar desde el panel
la tarea de alguien que ya se fue siguen igual, y validada, rechazada o cancelada siguen
selladas. Completar desde el panel no toca el fichaje de la persona; si quedó abierto lo
cierra el sanitizador. **Deshacer la completada** desde la app no está disponible en el
modo: la salida ya está escrita y es registro legal. Si salió por error, vuelve a Entrar si
todavía le cabe el turno, o pide la jornada manual, que existe.

### D6. Pausa y descanso son lo mismo

Pausar la tarea escribe el inicio de descanso del fichaje y reanudar lo cierra; el neto del
informe y el tiempo de la tarea restan lo mismo. En el modo **no aplica el descanso fijo**
de la sucursal: con un turno por tarea restaría el fijo en cada tarea (punto 6). Cuenta el
real.

### D7. Las alarmas pertenecen a la tarea

El trigger de D3 regenera, con el día, las alarmas de ese día: borra las que había y crea
las nuevas con la tarea como clave. Una tarea que se mueve mueve su alarma, una cancelada la
pierde, y una creada a las diez para las cuatro tiene la suya sin esperar a las 04:00. Antes
de sonar, la alarma pregunta a su tarea, no a los fichajes: iniciada o completada, calla; si
no, suena. Eso quita de en medio el `already_marked` por día del punto 4. Los textos nombran
la tarea: «entra, a las 10:05 empieza tal».

Regla del hueco: al generar las alarmas del día se miran las tareas de dos en dos; si entre
el fin de una y el inicio de la siguiente no caben los dos trenes de tres avisos, menos de
diez minutos con los desfases de hoy, se tira el tren de salida de la primera y el de entrada
de la segunda y queda **un solo aviso al inicio de la segunda**, que dice las dos cosas. Si
caben, cada tarea lleva sus seis como un turno normal.

### D8. El informe agrupa por día y enseña la jornada y los huecos

Las filas por ciclo siguen; lo nuevo es agruparlas por fecha y añadir dos líneas, solo cuando
la fecha tiene más de un ciclo:

```
Lunes 21   Jornada 8:00 – 14:40                       6 h 40
           Turno 1   8:00 – 10:00                     2 h 00
           Turno 2   10:05 – 12:05                    2 h 00
           Turno 3   12:10 – 14:40                    2 h 30
           Trabajado                                  6 h 30
           Huecos entre turnos                        0 h 10
```

La jornada es de la primera entrada real a la última salida real; lo trabajado es la suma
de los turnos con sus descansos quitados; los huecos son la diferencia, medidos de los
fichajes y no de las tareas: si terminó el primero a las 10:03 y empezó el segundo a las
10:06, el hueco son 3 minutos. Se mantiene aparte de los descansos, que van dentro de un
ciclo. **No se reutilizan «bruto» y «neto»**, que ya significan otra cosa en el informe. El
total del mes sigue siendo lo trabajado y lleva al lado la suma de huecos. Sale de los
fichajes, así que vale para cualquier jornada partida, no solo para el modo. Panel y app
enseñan el día igual: la jornada con sus turnos dentro, nunca un bloque único.

### D9. Las alertas siguen igual, con una apagada

Todas se apoyan en los turnos del día y en la copia congelada del fichaje (punto 7), y en el
modo las dos cosas tienen la misma forma. Rechazos en el acto, patrón y ventana, sospechoso
por horas, `workday.closed`, jornada sin cerrar seis horas después del vencimiento, «no
vino» y «llegó tarde» desde el espejo de los días generados: iguales.

Se apaga en el modo la de **salida antes de tiempo**: completar una tarea antes de su
vencimiento casi siempre es bueno, y avisar de algo que está bien enseña a ignorar la lista.
El cumplimiento de la tarea ya dice si acabó a tiempo o tarde.

### D10. El cuadrante, en el modo, solo crea tareas

Para una persona en el modo el importador de cuadrantes no escribe horario: crea las tareas
y el día se genera solo. Para quien no está en el modo sigue escribiendo la franja entera
como hasta ahora.

### D11. La plantilla semanal es el espejo de la semana activa (2026-10-16)

Decidido por Jose el 2026-10-16, al probar el cuadrante en staging: «el calendario por días es
la fuente de verdad; solo hay que sincronizar la plantilla semanal con la semana
correspondiente; eso cierra el círculo sin inventar nada». Y «sin sorpresas peligrosas».

Por qué: la app enseña la semana con la plantilla semanal (`data.weeklySchedule` de
`GET /calendar`) y solo el día de hoy con el día efectivo. El panel lee la plantilla de
Firestore. Sin esto, quien está en el modo ve en la app y en el panel una semana que no es la
suya, aunque el fichaje use bien los días generados. Corrige lo que D3 decía de la plantilla
(«no se toca en el modo»): se toca, pero solo como copia.

- **La fuente es el día generado.** La plantilla propia de la persona en el modo se reescribe
  con los turnos de los días generados de la **semana activa** (de lunes a domingo, en su zona
  horaria): un turno por tarea, y un día sin día generado sale **libre**, que es lo que aplica
  el fichaje.
- **Cuándo.** Cuando el trigger regenera un día que cae en la semana activa, y además dos veces
  al día (03:00 y 15:00 hora de Madrid) para el cambio de semana del lunes y para curar
  cualquier desajuste. Un cambio en una tarea de otra semana no toca la plantilla: se recoge
  cuando esa semana pase a ser la activa.
- **Sin sorpresas:**
  - solo personas cuyo modo resuelto es `tasks`, y solo su plantilla **propia**; nunca la de la
    sucursal ni la de la empresa, nunca a nadie en modo semanal;
  - solo se escribe si cambia algo;
  - enciende el horario propio (`overridesDisabled: false`), porque si no ni la app ni el
    panel lo enseñan;
  - la **primera vez** guarda la plantilla que la persona tenía (`plantillaAnterior`), para
    poder devolvérsela si sale del modo; devolverla es manual hasta que el selector del modo lo
    haga solo;
  - un fallo en la sincronización se registra y no corta la generación de los días ni las
    alarmas.
- **El cuadrante (D10)** sigue sin escribir horario para quien está en el modo: crea las tareas,
  el trigger genera los días y el espejo hace el resto.

### D12. «Calendario»: turnos cargados por fecha, con fichaje normal (2026-10-22)

Decidido con Jose el 2026-10-22 a partir del aviso de un cliente que ya ficha por tareas y no
consigue organizar el cuadrante: generó tareas para hacer de turnos, no puede meter nada dentro
de una tarea y le resulta lioso. Pide «horarios, como a turnos de forma mensual, fichar normal y
dentro de esos horarios meter las tareas».

Es un **tercer modo**, `scheduleMode: "calendar"`, que en el panel se llama «Calendario»
(Jose) junto a «Horario semanal» y «Horario por tareas». El horario de la persona es lo que se
ha cargado por fecha en sus `calendar_days`; un día sin cargar es libre; ficha con el gesto de
siempre y las tareas de ese día son tareas normales dentro del turno. Reutiliza entero lo de la
fase 1 (días por fecha, resolutor, espejo, disponibilidad, planificador, D11): lo único nuevo
es quién escribe los días, el panel y el importador de cuadrantes, y que el modo **sí se
hereda** de la empresa y de la sucursal (un cuadrante se planifica por sucursal); `tasks`
sigue siendo solo del empleado.

Se descartó «la semana tipo con fechas encima»: con la plantilla de respaldo, alguien tendría
turno un martes que nadie le cargó, y a quien planifica mes a mes eso es un fallo. También se
descartaron las subtareas: duplicarían el modelo de tareas para un problema de calendario.

Diseño completo en [TDR-007](./tdr/TDR-007-calendario-turnos-por-fecha.md). La app no se toca:
ficha normal y pinta la semana desde la plantilla, que D11 ya reescribe.

> **Sustituido en parte por D13 el mismo 2026-10-22.** El modo «Calendario» se retira del
> selector y la regla pasa a ser la de la semana completa, dentro de «Horario semanal».

### D13. El cuadrante son los turnos, y la semana cargada manda (2026-10-22)

Decidido por Jose al probar D12 en producción. Tres reglas:

- **El cuadrante son los turnos y es la fuente de verdad del horario.** Las tareas van dentro
  de los turnos y dependen de ellos, nunca al revés. Cargar un cuadrante, por el panel, el
  Excel o el asistente, nunca crea, mueve, cancela ni borra una tarea. Crear tareas en bloque
  es otra acción.
- **La semana completa.** Si la semana de una persona tiene al menos un día cargado, manda la
  semana cargada entera y los días que no vengan libran. Si no tiene ninguno, manda la semana
  tipo. En un día cargado no se aplica el descanso fijo: el descanso es el hueco entre turnos.
- **Cargar turnos a quien está en horario por tareas** cambia su fuente de verdad a los
  turnos: pasa a horario semanal, sus tareas se quedan dentro y ya no se inician al fichar.
  Lo decide quien carga, y la vista previa lo dice antes del sí, con las tareas que caen fuera
  de los turnos.

Con esto, «Calendario» sobra y se retira del selector. Diseño en
[TDR-008](./tdr/TDR-008-el-cuadrante-son-los-turnos.md).

### D14. Tres modos, y cada uno enseña y aplica solo lo suyo (2026-10-22, noche)

Decidido por Jose al ver D13 en el panel: con la semana tipo y los turnos cargados dentro del
mismo modo, la fuente del horario cambia semana a semana sin que nadie lo elija, y la pantalla
mezcla las dos. Vuelven tres modos, y **el modo es la única fuente del horario**:

- **Semana tipo** (`weekly`): solo la semana tipo. Los días cargados no cuentan.
- **Por turnos** (`calendar`): solo los turnos cargados, semana a semana; **una semana sin cargar
  libra**, avisada en rojo. Se hereda de la empresa y de la sucursal.
- **Por tareas** (`tasks`): sus tareas; solo de cada persona.

La ficha es solo de consulta y todo lo que cambia algo va en Editar; cada modo enseña solo lo
suyo. Sustituye la regla de la semana de D13. Diseño en
[TDR-009](./tdr/TDR-009-tres-modos-cada-uno-lo-suyo.md).

## Lo que cambia en la app

Es Flutter, se publica a mano y es el peldaño más lento de la cadena. En el modo: los botones
de iniciar y completar de la tarea se esconden; Entrar, Salir, Descanso y Fin de descanso
llevan el nombre de la tarea del turno; se manda posición siempre; Salir pide lo que la
tarea exija al completar; el estado de asistencia cambia con la respuesta del fichaje; no
hay deshacer la completada; la pantalla de horario enseña los turnos etiquetados con su
tarea. La app detecta el modo en la lectura con la que arranca, la misma que trae el horario.

## Fases

Ordenadas por lo que la persona ve primero, no por comodidad técnica.

1. **Modelo y generación** ([TDR-001](./tdr/TDR-001-modo-dias-generados-y-escritor.md)).
   El modo en el calendario y su herencia; la subcolección de días generados; el trigger
   escritor; el resolutor del día en ambos lados, Firestore y Postgres; el espejo; las reglas
   de D4; las reglas de Firestore y los índices que haga falta. Al acabar, una persona en el
   modo ficha contra los turnos de sus tareas con el gesto doble de hoy, y el panel la ve
   esperada. Sirve para validar todo lo demás sin tocar la app.
2. **Gesto único.** El fichaje inicia, completa, pausa y reanuda la tarea (D5, D6); enlace
   guardado en los dos lados; descanso fijo apagado en el modo. Después, la app.
3. **Alarmas por tarea** (D7) en `firebase_sdk`, y apagar la salida anticipada en el modo (D9).
4. **Informe** (D8): agrupación por día, jornada y huecos, PDF y Excel, total mensual.
5. **Cuadrantes en el modo** (D10).

Cada fase lleva su TDR en `tdr/` cuando arranca, y entra por `develop`; a `staging` sube una
versión usable, no cada peldaño.

## Lo que queda por decidir

Nada abierto del diseño. Cerradas al implementar:

- **Cuál de los avisos de entrada tarde manda en el modo:** el recordatorio de entrada (Jose,
  2026-10-16). El de tarea no iniciada deja de ir a esa persona. Los de patrón van a
  supervisores y se calculan en el SaaS; apagar ahí la salida anticipada (D9) queda pendiente
  de que esa heurística salga del SaaS (TDR-005 §1).
- **Qué estados forman turno:** todos menos borrador y cancelada (TDR-001 §3.3).
- **El nombre de la línea de huecos:** «Huecos entre turnos». El informe de jornada solo existe
  en español, así que no hay otros idiomas que nombrar (TDR-004 §2).

## Estado de las fases (2026-10-16)

| Fase | Estado |
|---|---|
| 1. Modelo y generación | En `develop` y `staging` (API), QA 15/15 contra staging |
| — Selector en el panel, solo en el empleado | En `develop` del panel (TDR-002) |
| 2. El fichaje mueve la tarea | En `develop` y `staging` (API) y en `develop` de la app (TDR-003) |
| 3. Alarmas por tarea | En `develop` y `staging` (API, TDR-005), funciones en `dev-encodebiz`; QA 15/15 y alarmas generadas por el trigger real |
| 4. Informe: jornada y huecos | En `develop` y `staging` (API, TDR-004) |
| 5. Cuadrantes en el modo | Hecho por otra sesión con D10 y D11: `aplicar` no escribe horario a quien está en el modo, solo tareas; la plantilla de sucursal pasa por el mismo `aprobar → aplicar`; prueba en `services/merlin/test/plantilla.test.ts` |
| — Tareas de varias personas | **Hueco encontrado el 22-oct** (TDR-006): arreglado y en producción desde el 22-oct (hotfix, PR #211) |
| 6. «Calendario»: turnos por fecha (D12) | API en producción el 22-oct ([TDR-007](./tdr/TDR-007-calendario-turnos-por-fecha.md)), migración 043 incluida; panel en `develop` y `staging`, PR 115 sin fusionar; conector con `cargar_turnos` en producción |
| 7. El cuadrante son los turnos (D13) | Diseñado el 22-oct ([TDR-008](./tdr/TDR-008-el-cuadrante-son-los-turnos.md)), sin implementar. Sustituye partes de la fase 6 |
| 8. Tres modos, cada uno lo suyo (D14) | Diseñado el 22-oct ([TDR-009](./tdr/TDR-009-tres-modos-cada-uno-lo-suyo.md)), sin implementar. Sustituye la regla de la semana de D13 |

## Documentos

- [TDR-001](./tdr/TDR-001-modo-dias-generados-y-escritor.md): fase 1, el modo, los días
  generados y quién los escribe.
- [TDR-002](./tdr/TDR-002-selector-en-el-panel.md): el selector del modo en el panel, en la
  ficha del empleado.
- [TDR-003](./tdr/TDR-003-el-fichaje-mueve-la-tarea.md): fase 2, el fichaje mueve la tarea.
- [TDR-004](./tdr/TDR-004-jornada-y-huecos-en-el-informe.md): fase 4, la jornada y los huecos en
  el informe.
- [TDR-005](./tdr/TDR-005-alarmas-por-tarea.md): fase 3, las alarmas pertenecen a la tarea.
- [TDR-006](./tdr/TDR-006-tareas-de-varias-personas.md): tareas de varias personas; el fichaje
  mueve la parte de cada una (pendiente).
- [TDR-008](./tdr/TDR-008-el-cuadrante-son-los-turnos.md): el cuadrante son los turnos; la
  semana cargada manda sobre la semana tipo; cargar turnos no toca tareas.
- [TDR-009](./tdr/TDR-009-tres-modos-cada-uno-lo-suyo.md): tres modos (Semana tipo, Por turnos,
  Por tareas); el modo es la única fuente del horario; la ficha es de consulta.
- [TDR-007](./tdr/TDR-007-calendario-turnos-por-fecha.md): «Calendario», el tercer modo: turnos
  cargados por fecha con fichaje normal, heredable por sucursal; rutas `/calendar/days`, el
  importador y el panel.
- Importación de cuadrantes: [cuadrantes/README.md](../cuadrantes/README.md), que escribe
  hoy la franja de la primera tarea a la última.
- Pausas de tarea: [tasks-service/08_pausas.md](../tasks-service/08_pausas.md).
- Geocerca de la tarea: [tasks-service/tdr/TDR-005](../tasks-service/tdr/TDR-005-worksite-y-geocerca-de-tarea.md).
- Disponibilidad y el espejo del calendario en Postgres: [disponibilidad/README.md](../disponibilidad/README.md).
- Catálogo de eventos: [eventos-webhooks/03_catalogo-de-eventos.md](../eventos-webhooks/03_catalogo-de-eventos.md).

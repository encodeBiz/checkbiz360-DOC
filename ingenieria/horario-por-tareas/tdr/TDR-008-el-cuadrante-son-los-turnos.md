# TDR-008: el cuadrante son los turnos, y la semana cargada manda

**Fecha:** 2026-10-22
**Estado:** Implementado el 2026-10-22 en `develop` y `staging` de API y panel; staging desplegado a mano y QA 54+55 26/26. **Sin subir a producción.** Cambios al implementar, en el §10.
**Componente:** `encodebiz-api`: `packages/shared` (resolutores), `services/checkinbiz` (`/calendar/days`, `GET /calendar`, fichaje), `services/firebase_sdk` (`weeklyFromTaskDays`), `services/merlin` (cuadrantes, `aplicar`), `services/assistant` (`cargar_turnos`, `proponer_cuadrante`); `encodebiz-front-saas` (selector, calendario de turnos, importador)
**Sustituye:** partes de [TDR-007](./TDR-007-calendario-turnos-por-fecha.md), las que se enumeran en el §7
**Decisión de referencia:** [README](../README.md), D13

---

## 1. De dónde sale

El TDR-007 se puso en producción el 2026-10-22 con un tercer modo, «Calendario», en el que un
día sin cargar libra. Al probarlo ese mismo día aparecieron tres huecos:

1. **Una persona con turnos y sin tareas.** Debería trabajar con sus turnos. Sin ellos, con la
   semana tipo. Tener que elegir antes un modo es un paso que nadie entiende.
2. **El cuadrante de Jose**, del lunes 26 al domingo 1:

   | Día | Turnos | Descanso | Horas |
   |---|---|---|---|
   | Lunes 26 | Libre | — | 0 |
   | Martes 27 | 09:00–15:00 y 16:00–18:00 | 15:00–16:00 | 8 |
   | Miércoles 28 | 10:00–14:00 y 15:00–19:00 | 14:00–15:00 | 8 |
   | Jueves 29 | 10:00–14:00 y 15:00–19:00 | 14:00–15:00 | 8 |
   | Viernes 30 | 10:00–14:00 y 15:00–19:00 | 14:00–15:00 | 8 |
   | Sábado 31 | 09:00–14:00 | — | 5 |
   | Domingo 1 | Libre | — | 0 |

   El lunes tiene que librar, no tomar el lunes de la semana tipo. Y las horas tienen que salir
   8, no 6: el descanso es el hueco entre turnos, no el descanso fijo de la sucursal.
3. **ChatGPT, con el conector de producción**, avisó de que al aplicar un cuadrante «se
   retirarán las 9 tareas del cuadrante actual». Viene de `proponer_cuadrante`: crea una tarea
   por trabajo y borra las tareas de cuadrante de esa semana que la propuesta ya no trae
   (conector-asistente ADR-006). Ese diseño nació para ayuda a domicilio, donde el cuadrante
   del ERP es una lista de servicios y el horario se sacaba de las tareas.

## 2. La regla

> **El cuadrante son los turnos, y es la fuente de verdad del horario. Las tareas van dentro de
> los turnos y dependen de ellos, nunca al revés. Cargar un cuadrante nunca crea, mueve,
> cancela ni borra una tarea.**

Y para saber qué horario tiene una persona una fecha concreta:

> **Si la semana de esa persona (lunes a domingo, en su zona) tiene al menos un día cargado,
> manda la semana cargada entera, y los días que no vengan libran. Si no tiene ninguno, manda
> la semana tipo.**

«Horario por tareas» sigue aparte y explícito, porque cambia el gesto: el fichaje inicia y
completa la tarea. Es el único modo en que las tareas forman el horario.

## 3. Los modos, después de esto

| Modo | De dónde sale el horario | El fichaje |
|---|---|---|
| `weekly`, «Horario semanal» | La semana cargada si la hay; si no, la semana tipo | Normal; las tareas van por sus botones |
| `tasks`, «Horario por tareas» | Las tareas de cada día (TDR-001) | Inicia, pausa y completa la tarea del turno |
| `calendar` | **Retirado del selector.** El servidor lo sigue aceptando y lo trata igual que `weekly` | Igual que `weekly` |

Por qué se retira `calendar`: con la regla de la semana, «Horario semanal» ya cubre a quien
planifica por cuadrante. Lo único que añadía era que una semana sin cargar librase entera, y
Jose prefiere que caiga en la semana tipo. Comprobado en producción el 2026-10-22: ninguna
ficha, sucursal ni empresa tiene `calendar`, y no hay días cargados desde el panel ni desde el
cuadrante. Retirarlo no cambia el horario de nadie.

## 4. El servidor

### 4.1 Qué días cuentan como cargados

Solo los de `calendar_days` con `generatedBy` igual a `panel` o `cuadrante`. Los que escribió
el trigger de tareas (`tasks_trigger`, `mode_activation`) son de «Horario por tareas»: fuera de
ese modo no se leen nunca, aunque la persona estuviera antes en él y sus documentos sigan ahí.

### 4.2 El resolutor del día (`resolveEffectiveDay.usecase.ts`)

- En `tasks`: igual que hoy, desde los días generados.
- En `weekly` y `calendar`: se leen los siete días de la semana de esa fecha. Si alguno está
  cargado (§4.1), el día y la `weeklySchedule` sintetizada salen de la semana cargada, con los
  días que faltan libres y `sources.schedule = "loaded"`. Si ninguno lo está, la plantilla, como
  siempre.
- Una lectura más por resolución: siete días de una persona, por rango, sin índice nuevo.

`ScheduleApplied.source` en el checklog admite `"loaded"`. El `"calendar"` del TDR-007 se
mantiene para leer lo ya escrito.

### 4.3 El descanso fijo

En un día de semana cargada no se aplica el descanso fijo de la sucursal: el descanso es el
hueco entre turnos, como en «Horario por tareas» (D6). `createChecklog` ya pone 0 cuando la
fuente es `tasks`; se añade `loaded`. El informe de jornada (TDR-004) ya agrupa por día y
enseña los huecos entre turnos.

### 4.4 La disponibilidad (`resolveAvailability.usecase.ts`)

La misma regla, por par (persona, sucursal) y por semana del rango. Se leen los días cargados
de la entidad en el rango, en la misma consulta de grupo que ya existe, filtrando por
`generatedBy`.

### 4.5 Lo que ve la app: la semana efectiva, sin espejo

En `weekly` la semana tipo es el respaldo, y copiar encima la semana cargada (D11) la
destruiría. Por eso:

- `weeklyFromTaskDays` vuelve a actuar **solo** en `tasks`.
- `PUT /calendar/days` deja de copiar la semana a la plantilla.
- `GET /calendar` devuelve en `data.weeklySchedule` la **semana efectiva** de la fecha pedida, o
  de hoy: la cargada si la hay, la plantilla si no. La plantilla guardada va aparte, en
  `data.templateSchedule`, para el panel. La app pinta lo correcto sin publicar nada.
- A quien se le copió la plantilla en `calendar` (nadie en producción) no hace falta devolverle
  nada.

### 4.6 `PUT /calendar/days`

- Acepta a quien está en `weekly` o `calendar`.
- **A quien está en `tasks`** solo con `fromTasks: true` en el cuerpo. Sin la bandera responde
  `400 calendar/days_person_in_tasks_mode`, con las tareas de esa semana que caerían fuera de
  los turnos que se cargan. Con la bandera, en la misma petición: pone `scheduleMode: "weekly"`
  en su ficha, escribe los días y no toca ninguna tarea. Así el cambio de fuente lo decide
  quien carga y queda dicho antes del sí.
- Sigue sin aceptar fechas pasadas ni turnos que se cruzan.
- `GET /calendar/days` no cambia.

### 4.7 Tareas fuera de los turnos

Una tarea que cae fuera de los turnos de su día no se puede iniciar, porque iniciar exige la
jornada abierta. Ni el servidor ni la carga lo bloquean. La vista previa del cuadrante y la
del asistente las enumeran, y el panel las pinta en rojo en el calendario de turnos: se avisa
en rojo, no se bloquea.

## 5. El cuadrante, en todos sus caminos

### 5.1 El importador (`services/merlin/src/soporte/cuadrantes`)

`aplicar` deja de crear tareas y de retirarlas. De cada persona de la propuesta escribe los
días de esa semana como días cargados (`generatedBy: "cuadrante"`), con un turno por franja.
Si un día trae varias franjas, varios turnos. Nada más.

- Se retira `retirar.ts` del camino de `aplicar`: no hay tareas que retirar. La función queda
  sin uso y se borra en el mismo cambio.
- Lo que hoy se lee de cada fila como servicio (para quién, dirección, qué se hace) ya no se
  convierte en tarea. Se enseña en la propuesta como nota del día, para que nadie pierda
  información sin enterarse.
- La plantilla de sucursal (cuadrantes TDR-001) se lee igual: una pestaña por persona, una
  fila por franja.
- Vale para los dos caminos que comparten `aplicar`: el panel (ficha de la sucursal y del
  empleado) y el asistente (`proponer_cuadrante`).

### 5.2 El asistente (`services/assistant`)

- `proponer_cuadrante` describe lo que hace ahora: carga turnos. Ni una palabra de tareas.
- `cargar_turnos` acepta `weekly` y `tasks`. Con alguien en `tasks`, la vista previa dice que
  pasa a horario semanal con estos turnos, que sus tareas se quedan dentro y ya no se inician
  al fichar, y cuáles caen fuera. Al confirmar manda `fromTasks: true`.
- `cambiar_modo_horario` deja de ofrecer `calendario`.
- `ver_semana` enseña la semana efectiva y de dónde sale: cargada o semana tipo.
- Instrucciones del servidor MCP: la regla del §2, dicha en una frase.

**Hecho el 2026-10-22** en `feat/asistente-cuadrante-son-turnos` (API), en `develop` y `staging`,
**sin subir a producción hasta que estén §4 y §5.1**:

- La semana efectiva se calcula en el conector con la regla del §2 sobre `GET /calendar/days`
  (solo `panel` y `cuadrante`, §4.1), así no depende del `GET /calendar` nuevo.
- La vista previa de `cargar_turnos` aplica la regla de la semana completa: enseña también los
  días de esa semana que no se mandan y pasan a librar (`noSeManda`,
  `diasQuePasanALibrarSinMandarse`). Las tareas fuera de turno se enumeran para todos, no solo
  para quien viene de `tasks` (§4.7). Con alguien en `tasks` manda `fromTasks: true`.
- `ver_semana` devuelve `semanaEfectiva: {fuente: "turnos cargados" | "semana tipo", dias}` y la
  `semanaTipo` aparte; a quien tiene `calendar` guardado lo trata y lo nombra como semanal.
- `cambiar_horario` deja de rechazar `calendar` y avisa de que la semana tipo solo vale en las
  semanas sin turnos cargados.
- Pruebas: once en `herramientas.test.ts` (sustituyen las ocho de TDR-007 §15); suite 148/148.

### 5.3 Crear tareas en bloque

Si un cliente trae una lista de trabajos (el caso de ayuda a domicilio), crear esas tareas es
otra acción, no el cuadrante. Queda fuera de este TDR. Mientras tanto, las tareas se crean una
a una, desde el turno en el panel o con `crear_tarea`.

## 6. El panel (`encodebiz-front-saas`)

- **Selector**: vuelve a dos opciones, «Horario semanal» y «Horario por tareas» (esta solo en
  el empleado). El PR 115, todavía sin fusionar, se rehace con esto antes de salir.
- **Calendario de turnos**: sale siempre que el modo resuelto sea `weekly`, en la ficha de la
  sucursal y en la del empleado. Distingue «semana cargada» de «semana tipo», y en una semana
  sin nada cargado enseña la plantilla en gris, para que se vea qué aplicará.
- **Importar cuadrante**: los textos dicen que se cargan turnos, no tareas.
- **Vista unificada** (pedida por Jose el 2026-10-22): en Horarios y festivos, el mismo diseño
  del calendario semanal de tareas, con tareas, turnos y semana tipo como elementos de la
  rejilla. Se acoplan en la celda de la hora en que empiezan, con «N elementos» a partir de
  tres y el panel lateral para la lista y el detalle, igual que hoy las tareas. Es la fase
  siguiente a esta y lleva su propio TDR.

## 7. Lo que sustituye del TDR-007

| TDR-007 | Ahora |
|---|---|
| §2 y §3: un tercer modo `calendar`, con los días sin cargar libres | Retirado del selector; la regla es la de la semana completa, dentro de `weekly` |
| §4: «en `calendar` escriben el panel y el importador» | Escriben en `weekly`, y en `tasks` con `fromTasks` |
| §5.2: `PUT /calendar/days` solo en `calendar` y copiando la semana a la plantilla | `weekly`, y `tasks` con bandera; sin copia a la plantilla |
| §6: `weeklyFromTaskDays` en `tasks` y `calendar` | Solo en `tasks`; la app recibe la semana efectiva de `GET /calendar` |
| §7: el importador crea una tarea por servicio y además escribe el día | Solo turnos; ni crea ni retira tareas |
| §8: tercera opción «Calendario» en el selector | Dos opciones; el calendario de turnos sale en `weekly` |
| §9 y §15: el asistente con `calendario` | §5.2 de aquí |
| §13: la geocerca | No cambia: sucursal para el fichaje, tarea para la tarea |

## 8. Pruebas

**Unitarias, en shared**: la regla de la semana, con una semana con un día cargado (los demás
libran), una semana sin nada (plantilla), una semana a caballo de dos meses, y días de
`tasks_trigger` que no cuentan fuera de `tasks`. El descanso fijo a cero en `loaded`.

**QA, `55-horario-calendario.spec.ts` reescrita**:

| Caso | Qué comprueba |
|---|---|
| HCA-01 | Persona en semanal sin nada cargado: la plantilla de la sucursal manda |
| HCA-02 | El cuadrante de Jose (§1) cargado: el lunes libra aunque la plantilla diga que no; el martes ficha contra los dos turnos; planificado 480 minutos; sin descanso fijo |
| HCA-03 | La semana siguiente, sin nada cargado, vuelve a la plantilla |
| HCA-04 | `GET /calendar` devuelve la semana cargada en `weeklySchedule` y la plantilla en `templateSchedule`; la plantilla guardada no ha cambiado |
| HCA-05 | Persona en `tasks`: sin `fromTasks`, 400 con las tareas fuera de turno; con él, pasa a `weekly`, los días se escriben y sus tareas siguen intactas (mismo id, estado y hora) |
| HCA-06 | Disponibilidad del día: la persona sale esperada con los turnos cargados, y el lunes no |
| HCA-07 | Aplicar un cuadrante desde el importador no crea ni borra tareas |
| HCA-08 | Fecha pasada, turnos cruzados: los 400 de siempre |

## 9. Despliegue

Sin migración: `dim_calendar_days` ya guarda `generated_by`, y el CHECK de la 043 sigue valiendo.
Contenedores `checkinbiz`, `analytics`, `merlin`, `assistant`, y los que se reconstruyen por
shared. `weeklyFromTaskDays` con `--solo`, en dev y en prod. A mano, sin Actions, como el resto
del 22-oct.

## 10. Lo que cambió al implementar (2026-10-22, noche)

**El importador: dos cuadrantes, y no se eligen (Jose).** Al ver el §5.1 escrito («solo turnos»)
Jose lo corrigió: quien está en «Horario por tareas» y sube tareas tiene que crear tareas. Y no se
ofrecen los dos tipos: **se ofrece el que toca a su modo, y se dice qué modo cambiar para subir el
otro**. Queda así:

- **Por turnos**, a quien está en semanal. Cada fila es una franja (fecha, entrada, salida) y las
  de un día son sus turnos; dos que se pisan se unen. No crea, mueve, cancela ni borra ninguna
  tarea. Escribe días con `generatedBy: "cuadrante"`.
- **Por tareas**, a quien está en «Horario por tareas». Una tarea por fila, como siempre, con su
  dirección como geocerca; el día lo genera el trigger. No escribe turnos ni semana tipo.
- **Ninguna tarea se borra** en ningún caso: la retirada del ADR-006 desaparece (`retirar.ts`
  borrado). Volver a subir la misma fila con la misma fecha y hora no duplica (`externalRef`);
  una tarea que cambió de hora entra como nueva y la vieja se queda. Queda abierto con Jose si
  esas se cancelan.
- **La plantilla** saca cada pestaña del tipo de su persona: por turnos solo con fecha, entrada y
  salida; por tareas con todas las columnas. El tipo va marcado en la fila de identidad
  (`cuadrante:turnos` / `cuadrante:tareas`, en gris) y con su nombre al lado; la portada lo
  dice por persona. En un fichero de antes, sin marca, se deduce de las columnas.
- **Si una pestaña no casa con el modo** de su persona al subirla (alguien lo cambió entretanto),
  esa persona se bloquea con «para subirle turnos, pásala a horario semanal» o al revés; las
  demás siguen. Y si el modo cambia entre proponer y aplicar, no se escribe nada.
- En el asistente (`proponer_cuadrante`), el tipo lo pone el modo de cada persona. Si a alguien en
  semanal le llegan para quién, dirección o trabajo, se avisa de que no se cargan.

**`PUT /calendar/days` con `fromTasks`**: se mantiene para el asistente (§5.2, ya hecho por su
sesión). El panel no lo usa: a quien está por tareas le dice que cambie de modo, que es la regla
de Jose para el importador. **Pendiente de decidir** si el asistente debe hacer lo mismo y se
retira la bandera.

**El panel**:

- Selector de vuelta a «Horario semanal» y «Horario por tareas», solo en el empleado.
- El cuadrante de turnos sale siempre en la ficha de la sucursal y en la de la persona. Una
  semana sin cuadrante enseña la semana tipo en gris (`GET /calendar/days` trae la de cada
  persona). Tocar un día de una semana sin cuadrante **carga la semana entera desde hoy**,
  partiendo de la semana tipo con el cambio, y se pregunta antes: cargar un día suelto haría
  librar al resto, por la regla del §2. Los días ya pasados de esa semana no se pueden escribir,
  y en las lecturas (disponibilidad) quedan libres; los fichajes ya hechos no cambian.
- Copiar la semana solo copia semanas cargadas, con los días libres como libres.
- La tabla «Horario semanal» de la ficha lee `templateSchedule`, no la semana efectiva.
- Importar cuadrante: textos y resultado según el modo (días de turnos o tareas creadas).

**Comprobado**: shared 103/103 (con `semanaCargada.test.ts`, el cuadrante del §1: lunes libre,
37 h), merlin 46/46, assistant 148/148, typecheck de todo el monorepo; QA 55 reescrita (HCA-01..06,
08) y 54, 26/26 contra staging. El panel, typecheck y lint sin errores; **sin probar con sesión**.

**Lo que queda, en orden:**

1. Jose prueba el panel con `start:dev` contra staging.
2. Decidir: tareas que cambiaron de hora al resubir un cuadrante por tareas (cancelar o dejar), y
   si el asistente deja de usar `fromTasks`.
3. Pase a producción: `proximo-pase-back.md` §16. Sin migración.

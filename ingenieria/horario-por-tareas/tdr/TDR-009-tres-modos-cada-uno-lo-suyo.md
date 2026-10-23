# TDR-009: tres modos, y cada uno enseña y aplica solo lo suyo

**Fecha:** 2026-10-22 (noche)
**Estado:** En producción desde el 2026-10-22 (noche): API `main` 869cc51, cinco funciones, merlin #222 y panel #119. Registro en `deployment-prod/proximo-pase-back.md` §16 ter.
**Componente:** `encodebiz-api`: `packages/shared` (resolutores), `services/checkinbiz` (`/calendar/days`, `GET /calendar`, fichaje), `services/merlin` (cuadrantes), `services/assistant`; `encodebiz-front-saas` (selector, Editar, ficha)
**Sustituye:** la regla de la semana del [TDR-008](./TDR-008-el-cuadrante-son-los-turnos.md) (§2, §3, §4.2, §4.4, §4.5 y §6); lo que se enumera en el §8
**Decisión de referencia:** [README](../README.md), D14

---

## 1. De dónde sale

El TDR-008 metió los turnos cargados dentro de «Horario semanal»: si una semana tiene algún día
cargado manda la semana cargada; si no, la semana tipo. Al verlo en el panel el mismo día, Jose:

> «Si voy a semana por turnos me muestras abajo la semana tipo y me lías una que no veas. Por eso
> soy partidario de los tres selectores, Semana tipo, Por tareas, Por turnos, y que cada uno
> muestre solo lo que implica, no el batiburrillo que tenéis ahora.»

El problema no es de pantalla: es que en un mismo modo conviven dos fuentes de horario y la que
manda cambia semana a semana sin que nadie lo elija. Una oficina de lunes a viernes de 9 a 17
no tiene por qué ver un cuadrante, y quien planifica por turnos no tiene por qué ver una semana
tipo que no usa.

## 2. La regla

> **Cada persona tiene un modo, y el modo es la única fuente de su horario.**

| Modo (valor) | En pantalla | De dónde sale el horario | Una semana sin nada |
|---|---|---|---|
| `weekly` | **Semana tipo** | Solo la semana tipo, igual todas las semanas | No existe: siempre hay semana tipo |
| `calendar` | **Por turnos** | Solo los turnos cargados, semana a semana | **Libra** (decidido por Jose) |
| `tasks` | **Por tareas** | Las tareas de cada día; el fichaje las inicia (TDR-001, TDR-003) | Libra |

- En **Semana tipo** los días cargados no se leen nunca, aunque existan.
- En **Por turnos** la semana tipo no se lee nunca, aunque exista.
- **Por turnos** se hereda como la semana tipo: se pone a la empresa, a una sucursal o a una
  persona. **Por tareas** sigue siendo solo de cada persona (D1).
- **Cargar turnos nunca crea, mueve, cancela ni borra una tarea** (TDR-008 §2, se mantiene).
- Los valores internos no cambian: no hay migración de modos. `calendar` vuelve a ser un modo de
  verdad, con el nombre «Por turnos».

## 3. Por qué «libra» y no «cae en la semana tipo»

Si una semana sin cargar cayera en la semana tipo, «Por turnos» tendría que enseñarla para que no
fuera una fuente escondida, y volveríamos al batiburrillo. Libra, y el riesgo de que una semana se
quede sin cargar se cubre con avisos (§6): en rojo, no bloqueando.

## 4. El servidor

### 4.1 El resolutor del día (`resolveEffectiveDay.usecase.ts`)

- `weekly`: la plantilla, como antes del TDR-008. No lee días cargados.
- `calendar`: el día cargado de esa fecha (`generatedBy` `panel` o `cuadrante`, TDR-008 §4.1);
  sin documento, o con `shifts: []`, libra. `sources.schedule = "loaded"`. La `weeklySchedule`
  sintetizada es la semana cargada de esa fecha, con los días sin cargar libres.
- `tasks`: igual que hoy.
- El descanso fijo no se aplica en `calendar` (como en `loaded`, TDR-008 §4.3).

### 4.2 La disponibilidad (`resolveAvailability.usecase.ts`)

Por par (persona, sucursal), según el modo resuelto: `weekly` la plantilla, `calendar` los días
cargados (sin cargar, no esperado), `tasks` los generados. Se retira `loadedWeeks` del par.

### 4.3 `GET /calendar`

`data.weeklySchedule` es la semana efectiva de la fecha pedida según el modo: la plantilla en
`weekly`, la semana cargada en `calendar` (sin cargar, libre), la generada en `tasks`. La plantilla
guardada sigue en `data.templateSchedule`.

### 4.4 `PUT /calendar/days`

- Solo a quien está en `calendar`. En `weekly`: `400 calendar/days_require_calendar_mode`.
- A quien está en `tasks`, solo con `fromTasks: true`: lo pasa a **`calendar`** (antes, a
  `weekly`), escribe los días y no toca ninguna tarea.
- Sigue sin fechas pasadas ni turnos cruzados.

### 4.5 El importador (`services/merlin/src/soporte/cuadrantes`)

El tipo lo pone el modo, como en TDR-008 §10:

- **Por turnos** a quien está en `calendar`.
- **Por tareas** a quien está en `tasks`.
- A quien está en **Semana tipo** no se le sube cuadrante: se bloquea con «para subirle turnos,
  pásala a Por turnos». Las demás personas siguen.

### 4.6 Datos ya escritos

Ninguno. Del TDR-008 solo llegó a producción el back (ni el panel ni la app), y comprobado en
producción el 2026-10-22: **0 días cargados** desde el panel o el cuadrante en las 16 empresas.
Nadie en `weekly` pierde horario con este cambio, y no hace falta script.

## 5. El asistente (`services/assistant`)

- `cambiar_modo_horario`: `semanal` («Semana tipo»), `turnos` («Por turnos») y `tareas`. Semana
  tipo y Por turnos se pueden poner a una sucursal entera.
- `cargar_turnos`: solo a quien está en Por turnos. En Semana tipo, «no se carga: pásala a Por
  turnos con cambiar_modo_horario». En Por tareas, solo con `pasarATurnos` pedido expresamente
  (sustituye a `pasarASemanal`), que manda `fromTasks`. La vista previa ya no aplica «la semana
  completa»: cada día que se manda es ese día, y los que no se mandan siguen como estaban (sin
  cargar = libre).
- `cambiar_horario` (la semana tipo): solo en Semana tipo; en Por turnos responde
  `horario_por_turnos` («sus turnos se cargan con cargar_turnos»).
- `ver_semana`: la fuente es el modo. Semana tipo: la semana tipo. Por turnos: los días cargados,
  con «sin cargar» marcado (libra). Por tareas: sus tareas.
- `proponer_cuadrante`: Por turnos o Por tareas según el modo; a quien está en Semana tipo, se
  bloquea con el modo que tiene que cambiar.
- Instrucciones: la regla del §2 en una frase.

## 6. El panel (`encodebiz-front-saas`)

La ficha es solo de consulta; todo lo que cambia algo va en **Editar** (Jose, 2026-10-22). Y cada
modo enseña solo lo suyo.

**Selector**, en Editar: empresa y sucursal con «Semana tipo» y «Por turnos»; empleado con los
tres, más «como su sucursal».

| Modo | Editar | Ficha (consulta) |
|---|---|---|
| Semana tipo | La semana tipo (franjas, descanso, tolerancia, plantillas) | La semana tipo |
| Por turnos | El cuadrante de turnos editable por semanas, «copiar a la semana siguiente», importar cuadrante por turnos | La semana cargada, con flechas de semana; una semana sin cargar sale «sin cuadrante» en rojo |
| Por tareas | Importar cuadrante por tareas; las tareas se gestionan en Tareas | Su semana de tareas |

- Festivos y ausencias siguen en su sitio y valen para los tres modos.
- **Aviso** en Por turnos: en la ficha de la sucursal y en la portada, «N personas sin turnos la
  semana que viene», en rojo.
- Al cambiar a Por turnos una sucursal o persona sin nada cargado, el propio guardado avisa: «la
  semana que viene libra hasta que se carguen sus turnos».
- Desaparece de la ficha el cuadrante editable y el botón de importar (hoy en la ficha de
  sucursal y de empleado).

## 7. Pruebas

**Unitarias, en shared**: `weekly` ignora días cargados; `calendar` con un día cargado (los demás
libran), sin nada (libra entera) y sin leer la plantilla; `tasks` sin cambios; descanso fijo a 0
en `calendar`.

**QA, `55-horario-calendario.spec.ts` reescrita**: persona en Semana tipo con días cargados que no
cuentan; persona en Por turnos con el cuadrante de Jose (TDR-008 §1): lunes libra, martes 480
minutos sin descanso fijo; semana siguiente sin cargar, libra; `PUT` a Semana tipo, 400; a Por
tareas con `fromTasks`, pasa a Por turnos y sus tareas siguen intactas; importador a Semana tipo,
bloqueado.

**Asistente**: `cargar_turnos` por modo; `ver_semana` por modo; `cambiar_modo_horario` con los
tres.

## 8. Lo que sustituye del TDR-008

| TDR-008 | Ahora |
|---|---|
| §2: «si la semana tiene algún día cargado, manda la semana cargada; si no, la semana tipo» | El modo es la única fuente (§2) |
| §3: `calendar` retirado, tratado como `weekly` | `calendar` es «Por turnos», un modo de verdad, heredable |
| §4.2 y §4.4: `weekly` lee la semana cargada | `weekly` solo la plantilla; `calendar` solo lo cargado |
| §4.6: `PUT` en `weekly`; `fromTasks` pasa a `weekly` | `PUT` solo en `calendar`; `fromTasks` pasa a `calendar` |
| §5.2: `cargar_turnos` en semanal y tareas; `pasarASemanal` | Solo en Por turnos; `pasarATurnos` |
| §6 y §10: el cuadrante en la ficha, la semana tipo en gris debajo, «cargar la semana desde hoy» | Cada modo enseña solo lo suyo; la ficha es de consulta (§6) |

Se mantienen del TDR-008: qué días cuentan como cargados (§4.1), el descanso como hueco entre
turnos (§4.3), cargar turnos no toca tareas, y los dos cuadrantes según el modo (§10).

## 9. Despliegue

Orden: servidor (`shared`, `checkinbiz`,
`analytics`, `merlin`); asistente; panel. Sin migración de base de datos. A mano, sin Actions.

# ADR-009 — El material sale hacia una tarea, una persona o una sucursal

**Fecha:** 2026-10-14
**Estado:** Aceptado (Jose, 2026-10-14: «me encaja perfectamente, documéntalo todo y prepáralo para desarrollo hoy mismo»)
**Decisionario:** Jose Acevedo
**Decisiones de referencia:** [ADR-004](./ADR-004-asignar-no-es-consumir.md) (los tres momentos y el sobrante), [ADR-007](./ADR-007-entrega-es-asignacion-con-acuse.md) (el equipo en manos de una persona), [ADR-002](./ADR-002-almacen-entidad-propia-multisucursal.md) (el almacén sirve a sucursales)
**Diseño técnico:** [TDR-008](../tdr/TDR-008-cuentas-de-material-por-destino.md)

---

## Contexto

Todo el flujo de material cuelga de la tarea. El libro **rechaza** una salida, un consumo o una
devolución sin tarea (`inventory/task_required`); la cuenta de material es `task_materials`; la
declaración se hace desde la tarea en la app; el sobrante se cuadra al validarla. Sin tarea solo
hay entradas, recuentos y traspasos, y entregar un operable a una persona (ADR-007). Para un
consumible no existe ningún camino sin tarea.

El caso que lo rompe, 2026-10-14:

> Jose: «Nos ha surgido un problema importante: cómo asigno o gestiono el material sin tareas
> asignadas. Debo poder gestionarlo porque, por ejemplo, en la empresa de limpieza su jornada es
> de limpieza y no tienen tareas: ¿cómo asigna los productos?»

En esa empresa el trabajo es la jornada en el centro del cliente, no una tarea: la plataforma
sigue sabiendo **quién** (ficha), **dónde** (el centro) y **cuándo** (la jornada). Lo único que
falta de la frase fundacional del módulo —«este material salió con Juan, en la tarea 482, en el
domicilio del cliente, a las 10:40»— es la tarea, que es el grano más fino, no el único.

Se valoraron tres salidas:

**A — Una tarea por jornada.** Crear tareas «de limpieza» para que el material tenga dónde
colgar. Es la burocracia que el README avisó que mata el módulo: obligar a planificar lo que
nadie planifica.

**B — La persona como segundo anclaje.** Además de la tarea, una cuenta de material por
persona, gemela de la de la tarea, declarada desde la jornada.

**C — El destino de la salida: tarea, persona o sucursal.**

> Jose: «Yo creo que deberíamos poder relacionar salida con una tarea, un empleado o incluso una
> sucursal.»

## Decisión

**Opción C.** El material sale del almacén **hacia un destino**, que es una de tres cosas:

| Destino | Qué es | Ejemplo |
|---|---|---|
| **Tarea** | Material para un trabajo concreto. Lo de siempre. | «Para la limpieza del Lidl del jueves, 30 toallas.» |
| **Persona** | Material en manos de alguien, como ya pasa con los equipos. | «A María, 5 litros de lejía.» |
| **Sucursal** | Material que se manda a un centro para que lo use quien trabaje allí. | «Al Lidl Sur, 20 litros para el mes.» |

Y **las cuatro operaciones son las mismas para los tres**: reservar (asignar), sacar,
declarar el gasto y cuadrar el sobrante. Lo que cambia es contra qué cuenta se apuntan y quién
puede hacerlo. La cuenta de material tiene un destino; la de la tarea es un caso de los tres.

### Lo que decide cada destino

| | Tarea | Persona | Sucursal |
|---|---|---|---|
| **Quién reserva** («dotación») | supervisor o superior | supervisor o superior | supervisor o superior |
| **Quién saca** | asignado a la tarea, o supervisor+ | la propia persona, o supervisor+ | fichado en la sucursal, o supervisor+ |
| **Quién declara el gasto** | asignado a la tarea, o supervisor+ | la propia persona, o supervisor+ | fichado en la sucursal, o supervisor+ (la declaración lleva quién fue) |
| **Dónde se cuadra el sobrante** | al validar la tarea, obligatorio | desde su ficha o «Mi material», cuando toque | desde la ficha de la sucursal, cuando toque |
| **Qué se puede resolver** | devuelto o gastado, hasta cero | devuelto o gastado; lo demás sigue en su poder | devuelto o gastado; **lo demás queda en el centro** |
| **Dónde se ve lo pendiente** | detalle de la tarea | ficha del empleado, «Mi material» | ficha de la sucursal |

Y una vista nueva que sale sola de las tres cuentas: **cuánto material hay fuera del almacén y
dónde** —en qué tareas, en manos de quién, en qué centros—, la hermana de «fuera de base» de
los operables (ADR-008).

### Dos reglas

1. **Reservar también vale para los tres.** Para una tarea es lo planificado; para una persona
   o un centro es su dotación: «a María le tocan 5 litros a la semana». Es la misma mecánica y
   da gratis «consume más de lo asignado» por persona y por centro, que es el eje que ya pide
   el panel ([TDR-006](../tdr/TDR-006-material-en-el-panel-y-en-merlin.md) §4.3).
2. **El material sale siempre del almacén hacia un destino, y vuelve al almacén.** No pasa de
   una persona a una sucursal ni de una sucursal a una persona: si hace falta, es una
   devolución y una salida. Dos apuntes, cada uno con su verdad.

### La sucursal como destino no sustituye al almacén por sucursal

Son dos niveles de control y cada cliente elige. Quien quiera existencias, mínimos y
recuentos en un centro, le crea un almacén (ADR-002) y lo repone por traspaso, que ya existe.
Quien solo quiera saber cuánto se mandó y cuánto se gastó, usa el destino. Y cuando en un
centro nadie declara, el recuento de su almacén ya dice cuánto se fue; registrar ese recuento
como consumo del periodo en vez de como discrepancia es un paso posterior, fuera de esta
decisión.

### Por qué no la opción A

Una tarea que nadie pidió es un formulario más entre el trabajador y su trabajo. El módulo
vive de que declarar cueste un clic; cada tarea de mentira es un motivo para no declarar.

### Por qué no se queda en la opción B

Con la persona como único anclaje nuevo, el material del centro habría tenido que colgar de
alguien que no lo tiene: el que lo recoge, el encargado. Es falso y vuelve a la trampa de
nombrar a quien no corresponde (ADR-004 §3). El centro es un destino real, y el que declara
sigue quedando apuntado.

### Por qué no contradice «asignar no es consumir»

Los tres momentos de ADR-004 siguen intactos; solo cambia contra qué cuenta se apuntan. Y
donde no hay un momento forzado de cuadre (persona, sucursal), el pendiente no desaparece ni
se infla: se queda a la vista en la ficha hasta que alguien lo resuelve.

## Consecuencias — qué implementa cada sesión

El detalle, contrato a contrato, en [TDR-008](../tdr/TDR-008-cuentas-de-material-por-destino.md).

### API (`encodebiz-api`, `services/inventory` + `shared`) — **sesión del servidor, primero**

- Los movimientos que tocan una cuenta (`reservation`, `reservation_released`, `issue`,
  `consumption`, `return`) llevan **`accountKind: task | employee | branch`**; el libro resuelve
  la cuenta por destino. `task_materials` queda como está; las cuentas de persona y sucursal
  van en `material_accounts`, con la misma forma.
- Rutas nuevas bajo **`/materials`** (reserve, issue, consume, settle, lectura por destino,
  «Mi material» y «fuera del almacén»). Las de `/tasks/:taskId/materials/*` no cambian.
- Columna `account_kind` en `item_movements_raw` (migración a mano). Los informes ya agrupan
  por empleado y centro sin tarea; ganan el eje «destino».

### Panel (`encodebiz-front-saas`) — **sesión del panel**

- **Salida** y **Asignar** desde el almacén o el artículo preguntan **a qué va**: tarea,
  persona o sucursal.
- **Ficha del empleado**, pestaña Material: los consumibles que lleva, con lo pendiente y el
  cuadre. **Ficha de la sucursal**: bloque Material con lo mandado, lo gastado y lo que queda,
  con su cuadre y «queda en el centro».
- **Existencias**: «Fuera del almacén», lo que está en tareas, personas y centros.

### App (`checkbiz360`) — **sesión de la app**

- **«Declarar consumo» desde la jornada**, no solo desde la tarea: contra la sucursal donde
  está fichado. Precargado con lo que ese centro tiene sin declarar, y lo no previsto se
  añade como en la tarea.
- **«Mi material»** enseña también los consumibles en su poder, con declarar y devolver.
- Textos en los cuatro idiomas de la app; errores por código.

### Orden

API primero (tipos, libro, rutas, espejo, migración); panel y app en paralelo sobre los
contratos del TDR-008. Hasta que la API lleve `/materials`, el panel y la app siguen como hoy.

## Aplazado

- **El recuento del almacén de un centro como consumo del periodo**, para los centros donde
  nadie declara.
- **Dotación periódica** («5 litros a la semana» que se renueva sola): hoy la dotación se
  reserva a mano cada vez.

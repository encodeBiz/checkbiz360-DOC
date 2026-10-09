# TDR-006 — El material en el panel operativo y en Merlin

**Fecha:** 2026-10-09
**Estado:** Diseño aprobado, sin código
**Componente:** `encodebiz-api` — `analytics` (overview del panel), `merlin` (relato del panel), `tasks` (espejo de tareas); panel `checkinbiz/panel`
**Decisiones de referencia:** [ADR-004](../adr/ADR-004-asignar-no-es-consumir.md),
[ADR-005](../adr/ADR-005-instante-firestore-historico-postgres.md),
[panel-operativo-v2/TDR-005](../../panel-operativo-v2/tdr/TDR-005-panel-analisis-cruce-de-ejes.md) (el cruce de ejes),
[TDR-004](./TDR-004-espejo-postgres-e-informes.md) (el espejo que lo alimenta)

---

## 1. Lo que dijo el propietario

> «Traduciendo lo que tenemos a lenguaje de operativa, que es nuestro nicho principal: un
> empleado que no declara lo que usa no cumple, por tanto su fiabilidad debe bajar. Y un
> empleado que gasta más de lo que se le asigna es un problema que hay que identificar, o
> bien de administración o bien del propio empleado.» (2026-10-08)

Eso fija el encargo. El inventario no entra en el panel como un cuadro de existencias, que es
lo que el [README](../README.md) rechazó desde el primer día. Entra como **una fuente más
para las tres preguntas que el panel ya hace** —dónde actuar, con quién contar, qué está
pasando— y como un **eje más de la fiabilidad de la persona**, con las mismas reglas que
los otros cuatro: hechos observados, nunca causas; `sin_evidencia` no penaliza; lo que es de
la mayoría es de la operación y no de las personas; lo que tiene explicación estructural es
un aviso a administración, no un juicio.

## 2. La puerta, una sola y en el origen

**Lo primero es que el módulo esté activado.** `analytics` llama a `getInventoryAccess` de
`shared` (cuenta `active` y `trialing`) al montar `GET /panel/overview`:

- **Sin add-on:** el overview no lleva bloque `material`, el cruce sigue con los ejes de hoy,
  `dataHealth` no menciona el inventario y el panel no cambia en nada. Merlin no recibe
  vocabulario de material, así que no puede ni mencionarlo como pendiente ni sugerir
  contratarlo.
- **Con add-on:** va el bloque entero, el eje y la madurez. Ver
  [[feedback-inventario-todo-si-habilitado]]: nada de subconjuntos.

El panel y Merlin **no deciden**: reaccionan a que el bloque venga o no. Lo único que Merlin
toca por la puerta es incluir «con material sí/no» en la clave de caché del relato, para que
activar el add-on no deje un relato viejo durante las 24 horas de caché.

## 3. Prerrequisito que no es del inventario: las tareas en Postgres

El panel lee solo Postgres (panel-operativo-v2, ADR-001). Hoy de las tareas solo se espejan
las valoraciones (`task_ratings_raw`). Todo lo de persona de este TDR —declara o no, gasta
sobre lo asignado— **se mide sobre tareas cerradas**, y el cierre vive en `tasks`.

Hace falta `tasks_raw`: id, entidad, sucursal, estado, asignados, `started_at`,
`completed_at`, `validated_at`, `due_at`. La escribe `tasks` en la propia petición con su job
de reespejo, igual que hace `inventory` con sus apuntes (TDR-004 §2 y §3). Es el mismo
prerrequisito que tiene la reapertura del eje de tareas del cruce, aplazado por decisión el
2026-07-29 porque el módulo entonces no escribía: **se paga una vez y sirve a los dos ejes.**

## 4. Qué aporta el material, y de dónde sale cada hecho

Todo sale de `item_movements_raw`, `unit_reservations_raw`, `dim_items`, `dim_item_units` y
`dim_warehouses`, en la ventana del mes con su mes de comparación, como el resto del panel.
**Ningún umbral se elige a mano**: cada señal es un hecho del libro o una comparación contra
algo que el propio cliente declaró (lo que asignó, sus propios compañeros).

### 4.1 Motivos de centro (pestaña Sucursales)

Entran en `reasons` de cada centro y, por tanto, en el orden de atención:

| Clave | Hecho que la produce |
|---|---|
| `material_sin_cuadrar` | Material que salió a tareas ya cerradas y nadie declaró ni devolvió (`pending` que sobrevive al cierre). |
| `sobrecompromiso` | Existencias comprometidas a tareas por encima de lo que hay (`Σ committed_delta` > saldo). Es planificación de administración. |
| `recuento_desviado` | Saldo en negativo: alguien gastó lo que el sistema creía que no había. El recuento estaba mal; no dice nada de quién. |
| `equipo_parado` | Ejemplares que pasaron el mes en base sin reserva mientras en el mismo centro hubo choques o reservas rechazadas. |

### 4.2 El eje de material de la persona (pestañas Empleados y Análisis)

Cada apunte lleva **a quién se imputa** (`employee_id`) y **quién lo registró**
(`registered_by`). Para cada persona, sobre sus tareas cerradas en el mes: cuánto salió a su
nombre, cuánto declaró ella misma, cuánto cuadró otro al validar, cuánto sigue sin cuadrar.

| Valor | Significado |
|---|---|
| `declara` | Lo que salió a su nombre lo declaró o devolvió ella antes del cierre. |
| `declaracion_irregular` | Parte la declaró ella; parte la cuadró otro o quedó sin cuadrar. |
| `no_declara` | La mayor parte de lo que sacó lo cuadró otro al validar o sigue sin cuadrar. |
| `sin_evidencia` | No sacó material en el periodo. No penaliza. |

Es el mismo tratamiento que el eje de registro de jornada: **declarar es obligación de quien
saca el material**, así que `no_declara` sí es un hallazgo sobre la persona… **cuando no es
general**. Si la mayoría de la plantilla está en `no_declara`, la empresa no usa la
declaración desde la app y lo cuadra el encargado: hallazgo sobre la operación, dicho una vez.

### 4.3 Gasta más de lo asignado

Consumido contra reservado, tarea a tarea. La clasificación es la que el panel ya aplica
para separar `valla_corta` de `patron_de_conducta`:

| Clave | Cuándo | A quién |
|---|---|---|
| `asignacion_corta` | El exceso es general en el centro para el mismo tipo de tarea. | Aviso de configuración a administración, **sin nombres**. |
| `consumo_sobre_asignacion` | Una persona consume por encima de lo asignado y el resto del centro consume lo asignado en tareas comparables. | Excepción con nombre: el hecho y la proporción. La causa la pone el gestor. |
| `salida_sin_asignacion` | En un centro casi todo el material sale sin reserva previa. | Aviso a administración: la planificación no se está usando. |
| `sin_evidencia` | No hubo asignación con la que comparar (la reserva es opcional, ADR-004). | Nadie. |

La referencia no la elegimos nosotros: lo asignado lo declaró el cliente al reservar, y la
comparación es contra sus propios compañeros en el mismo centro.

## 5. Fiabilidad y cruce

- `BuildWorkerProfile`: el material es el **quinto eje, detrás de tareas**. El orden sigue
  siendo «cada eje invalida la evidencia del siguiente»: si las tareas no se validan, el
  material no se puede juzgar; es **un problema visto dos veces**, como horas sobre registro.
- `BuildEmployeeReliability`: quinta señal, la declaración de material.
- `axesInService` pasa de 3 a 5 cuando tareas y material estén en servicio; `deferredAxes`
  se actualiza. `sin_evidencia` sigue sin penalizar (ADR-005 del panel).
- `BranchRow.reasons` gana los cuatro motivos de §4.1. Cambia el `attentionRank`, que es el
  objetivo.

## 6. Madurez y frescura

`dataHealth.material`, con la convención del resto: `warming` hasta tener tareas cerradas con
material en el mes y comparación con el anterior; `partial` si el espejo está atrasado, con
la medida de frescura que `inventory` ya calcula (TDR-004 §5); `ready` en otro caso. Sin
add-on, la entrada no existe.

## 7. El panel

Sin pestaña nueva. Los motivos de material salen en **Sucursales** con su etiqueta; la señal
de declaración en **Empleados**; el quinto eje en **Análisis**. `merlinPanelPayload` reenvía el
bloque si existe. No hace falta `useInventoryAccess` en el panel: la API ya decidió.

## 8. Merlin

Merlin narra y prioriza, no calcula: recibe las claves y cifras que el panel ya publicó. Las
claves nuevas **se traducen a frase antes del prompt**, como se hizo con las de geocerca
cuando el modelo se inventó el significado de una:

| Clave | Frase que entra al prompt |
|---|---|
| `no_declara` | sacó material y no lo declaró; lo cuadró otro al validar o sigue sin cuadrar |
| `declaracion_irregular` | declaró parte de lo que sacó |
| `consumo_sobre_asignacion` | consumió por encima de lo que la empresa le asignó, mientras el resto del centro consumió lo asignado (hecho medido; la causa NO está establecida) |
| `asignacion_corta` | la asignación de material de este centro se queda corta de forma general (configuración de administración, no de las personas) |
| `material_sin_cuadrar` | material que salió a tareas ya cerradas y nadie cuadró |
| `sobrecompromiso` | se promete a tareas más material del que hay |
| `recuento_desviado` | el recuento del almacén estaba mal: salió más de lo apuntado |
| `equipo_parado` | ejemplares en base sin uso mientras otras tareas del centro los pedían |

Tres reglas en el tab: `no_declara` es de la persona cuando no es general y de la operación
cuando lo es; `consumo_sobre_asignacion` es un exceso contra lo asignado, nunca una
afirmación sobre el destino del material; `asignacion_corta` es de administración y no se
nombra a nadie. **El coste no viaja**: no entra en el payload, y el lenguaje financiero ya
está vetado en el prompt. `PROMPT_VERSION` sube.

Lo que Merlin añade que la pantalla no puede: «el material no se cuadra porque las tareas no
se validan», «en Vallecas se promete más de lo que hay y por eso las tareas salen sin
material», «la fregadora parada en base es la misma que chocó tres veces».

## 9. Fuera, a propósito

- **El dinero.** El panel apartó el coste porque la tarifa entra a cero cuando nadie la
  configura; el coste unitario de la ficha tiene el mismo sesgo. Vive en los informes
  ([TDR-005](./TDR-005-material-en-el-informe-de-tareas.md) y el de consumo). En el panel, a lo
  sumo una cifra con madurez `partial`, y nunca en el relato.
- **Quién registra por toda la cuadrilla** (`registered_by` ≠ `employee_id` de forma
  sistemática). Es un hecho interesante y fácil de leer como culpa: fuera del relato en v1.
- **Las entregas con acuse** (Fase 6, `unit_assignments_raw`): señales del tipo «equipo
  entregado sin acuse» como avisos en rojo, más adelante.

## 10. Orden de entrega

1. Espejo de tareas `tasks_raw` (§3), compartido con la reapertura del eje de tareas.
2. Motivos de centro (§4.1), `dataHealth.material` y sus frases en Merlin. No necesitan persona.
3. Eje de persona (§4.2) en fiabilidad y cruce, junto con la reapertura del eje de tareas.
4. Consumo sobre asignación con su clasificación (§4.3).
5. Entregas con acuse como avisos en rojo.

## 11. Criterio de éxito

Con una entidad con add-on y un mes de tareas cerradas con material, el overview trae el
bloque `material`, los centros con material sin cuadrar suben en el orden de atención con su
motivo, cada persona tiene su valor en el eje de material y la fiabilidad lo refleja, y el
relato de Merlin dice qué implica un hallazgo sobre otro sin recitar la pantalla ni nombrar a
nadie de los avisos de configuración. Con una entidad sin add-on, el overview y el relato son
idénticos a los de hoy.

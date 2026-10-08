# TDR-005 — El material de cada tarea en el informe de tareas

**Fecha:** 2026-10-08
**Estado:** Implementado y en `develop` y `staging` desde el 2026-10-08 (desplegado en el entorno de desarrollo por el Staging CI/CD, run 37756082894); pendiente del siguiente pase a producción
**Componente:** `encodebiz-api` — `reports` (`POST /api/reports/tasks`) + `@encodebiz/shared`
**Decisiones de referencia:** [ADR-004](../adr/ADR-004-asignar-no-es-consumir.md),
[tasks-service/TDR-004](../../tasks-service/tdr/TDR-004-informe-tareas-xlsx.md)

---

## 1. La regla

> **Si la entidad tiene el add-on de inventario, el informe de tareas lleva todo el material.
> Si no lo tiene, el informe es el de siempre.**

La única condición es la suscripción, leída con `getInventoryAccess` de `shared`, que cuenta
`active` y `trialing` igual que el servicio `inventory` y el panel. No hay casilla en el
formulario, ni versión «con coste» y «sin coste», ni subconjunto para empezar: el add-on se
contrata entero y el informe lo refleja entero. Y sin add-on no aparece **nada** de
inventario: ni columnas vacías, ni avisos, ni una hoja en blanco. El fichero es idéntico al
de hoy.

Esto no es el caso de los informes que *dependen* del add-on, que se listan siempre en
Informes y en rojo cuando no está contratado. El de tareas no depende de él: se enriquece con
él, y una columna vacía en cada fila pidiendo contratar algo sería ruido.

## 2. Qué lleva el informe con el add-on

### Hoja «Tareas» — tres columnas más, al final

| Columna | Qué es |
|---|---|
| Material | Lo consumido por la tarea, en texto: `Toallas: 20 unidad · Desengrasante: 2 litro · Fregadora industrial FR-2`. Cada consumible con su cantidad y la unidad que el cliente escribió en la ficha; los operables por su ejemplar (identificador, o etiqueta si no lo tiene). Vacío si la tarea no tiene material. |
| Sin cuadrar | Lo que salió y nadie ha declarado ni devuelto, en el mismo formato: `Toallas: 10 unidad`. Vacío si no hay nada pendiente. Es lo que alguien quiere ver antes de validar. |
| Coste material (€) | Σ consumido × coste unitario de la ficha, `0.00`. Vacío si ningún artículo consumido tiene coste: un cero parecería un dato. |

### Hoja «Material» — una fila por tarea y artículo

Solo existe con el add-on. Es la hoja que alguien va a filtrar o pivotar; sin ella, las tres
columnas de arriba se quedan cortas.

| Columna | Consumible | Operable |
|---|---|---|
| Centro | nombre de la sucursal de la tarea | ídem |
| Tarea | título | ídem |
| Estado | estado de la tarea (etiqueta ES) | ídem |
| Tipo | «Consumible» | «Operable» |
| Artículo | nombre de la ficha | nombre de la ficha |
| Ejemplar | — | identificador, o etiqueta si no lo tiene |
| Unidad | unidad de la ficha (`unidad`, `litro`…) | unidad de uso (`h`, `km`, `días`) |
| Almacén | de dónde salió | base del ejemplar |
| Reservado · Salido · Consumido · Devuelto · Sin cuadrar | los cinco contadores de `task_materials`, `0.000` | — |
| Coste unitario (€) · Coste (€) | de la ficha; coste = consumido × unitario. Vacíos sin coste | — |
| Desde · Hasta | — | intervalo de la reserva, hora local del centro |
| Uso | — | `usageEnd − usageStart` si hay las dos lecturas; vacío si no |
| Reserva | — | Reservada / En uso / Liberada |

Una tarea con tres artículos y una fregadora son cuatro filas. Las reservas **canceladas no
salen**: una reserva cancelada es material que no llegó a ir.

## 3. De dónde sale

De **Firestore**, como el resto del informe, no del espejo en Postgres. El informe incluye
tareas abiertas, y en una tarea abierta lo que importa es el estado actual del material,
incluido lo que está sin cuadrar: eso solo lo tiene `task_materials`. El espejo lleva su
retraso y obligaría a reagregar movimientos para llegar al mismo número.

| Dato | Lectura |
|---|---|
| Material de las tareas | `entities/{e}/task_materials` con `taskId in [...]`, de 30 en 30 |
| Reservas de ejemplares | `entities/{e}/unit_reservations` con `taskId in [...]`, de 30 en 30 |
| Fichas (nombre, unidad, coste, unidad de uso) | `items` por id, de 30 en 30 (`findByIds`, ya existe) |
| Ejemplares (identificador, etiqueta, almacén base) | `item_units` por id, de 30 en 30 (`findByIds`, nuevo) |
| Nombres de almacén | `warehouses` de la entidad, una lectura |

Las dos consultas por lote son `in` sobre un solo campo: **no piden índice compuesto**. Hoy
el informe hace dos lecturas por tarea (valoraciones y evidencias); con material son dos
consultas más **por cada treinta tareas**, no por tarea. Con el tope de mil tareas del
informe son unas setenta lecturas más, no dos mil.

Las fichas se piden por id y salen aunque estén archivadas: un artículo con movimientos no se
borra, se archiva, y su historia tiene que seguir diciendo su nombre.

## 4. Lo que se añade a `shared`

```ts
LedgerRepository.findTaskMaterialsByTasks(entityId, taskIds): Promise<TaskMaterial[]>
ReservationRepository.findByTasks(entityId, taskIds): Promise<UnitReservation[]>
ItemUnitRepository.findByIds(entityId, ids): Promise<ItemUnit[]>
```

Los tres con el troceado de 30 que ya usan `findStock({itemIds})` y `Item.findByIds`. Nada
cambia en `inventory`, en `tasks` ni en la app.

## 5. El coste

Consumido × coste unitario **de la ficha, el actual**: la misma valoración que declara el
informe de consumo (`valuation: "unit_cost"`), así los dos números cuadran entre sí. Sin
FIFO ni precio medio: fuera de v1 desde el README.

## 6. Dónde se toca

- `services/reports/src/application/GenerateTaskReport.ts`: tras leer las tareas, lee la
  suscripción; con add-on carga el material y lo resuelve a nombres con las mismas cachés
  que ya usa para centros y empleados.
- `services/reports/src/application/GenerateTaskReportXLSX.ts`: las tres columnas y la
  segunda hoja, las dos condicionadas **al add-on, no a que haya material**: con add-on y
  sin material en el periodo, las columnas van vacías y la hoja lo dice en una línea, en
  vez de desaparecer y dejar la duda. Las celdas combinadas de la cabecera se calculan
  sobre el número real de columnas, en vez del `A1:N1` fijo de hoy.
- `packages/shared`: los tres métodos del §4.

El formulario del panel no cambia: pide el informe igual y recibe más. El histórico sigue
siendo `type: "task"`, `format: "xlsx"`. Si el add-on se da de baja, los informes
siguientes salen sin material; los ya generados son ficheros en Storage y no cambian.

## 7. Casos borde

- **Tarea sin material** → las tres columnas vacías; no sale en la hoja «Material».
- **Tarea abierta con material salido** → «Sin cuadrar» con lo pendiente; sus reservas vivas
  salen como Reservada o En uso.
- **Ejemplar sin lecturas de contador** → «Uso» vacío, no cero.
- **Artículo archivado** o **ejemplar retirado** → salen por su nombre; la historia no cambia.
- **Almacén sin nombre resoluble** → el id, como hace el informe con el centro.
- **Entidad sin add-on con `task_materials` viejos** (lo tuvo y lo dejó) → no se leen ni se
  enseñan: la regla es la suscripción, no la existencia de datos.

## 8. Criterio de éxito

Con una entidad con add-on, `POST /api/reports/tasks` devuelve un Excel con la hoja «Tareas»
ampliada en tres columnas y una hoja «Material» con una fila por tarea y artículo, y los
totales de la hoja «Material» cuadran con lo que enseña la ficha de la tarea en el panel.
Con una entidad sin add-on, el fichero es el mismo que antes de este cambio. Compila limpio
en el pipeline del monorepo.

## 9. Comprobado el 2026-10-08

En local contra dev, reproduciendo el pipeline sin subir a Storage ni escribir histórico:

- **Cuidama Servicios** (add-on `active`), una tarea con material entre el 10 y el 10 de
  octubre: la hoja «Tareas» sale con 17 columnas y la hoja «Material» con cuatro filas, tres
  consumibles reservados y sin salir (reservado 100 / 20 / 20, consumido 0, coste 0 con
  coste unitario en la ficha) y una fregadora `FR-2` reservada del 9 al 10 con unidad de uso
  en días. La columna «Material» de la tarea dice solo `Fregadora FR-2`: los consumibles aún
  no se han consumido, y esa columna es lo consumido. «Sin cuadrar» y «Coste material» van
  vacíos, que es lo correcto con todo todavía en el almacén.
- **Entidad de QA** (sin add-on), cinco tareas: 14 columnas, una sola hoja, igual que antes.
- `shared`, `reports` e `inventory` compilan; los tres envoltorios de `inventory` delegan los
  métodos nuevos.

Fusionado a `develop` (`df7f94b`) y a `staging` (`b845811`) el mismo día; el despliegue de
staging pasó con el borde verificado. Lo que queda: el pase a producción con el siguiente
`staging → main`, y en el primer informe real mirar si la columna «Material» de una tarea
abierta debería decir también lo reservado y no solo lo consumido. Hoy sigue el §2 al pie de
la letra; la hoja «Material» ya enseña lo reservado.

# TDR-008 — Cuentas de material por destino: tarea, persona o sucursal

**Fecha:** 2026-10-14
**Estado:** Implementado el 2026-10-14 en API, panel y app; API y panel en staging, app en `develop`; sin pasar a producción
**Componente:** `encodebiz-api` — `@encodebiz/shared` (libro y entidades), `inventory:3016`; `reports`; panel `checkinbiz/inventory`, `employee`, `branch`; app `checkbiz360`
**Decisión de referencia:** [ADR-009](../adr/ADR-009-el-material-sale-hacia-una-tarea-una-persona-o-una-sucursal.md)
**Se apoya en:** [TDR-002](./TDR-002-saldos-movimientos-y-conciliacion.md) (el invariante del libro), [03 §6](../03_modelo-de-datos.md) (`task_materials`), [04 §Material de una tarea](../04_contratos-api.md)

---

## 1. La idea en una frase

Donde hoy hay una **cuenta por tarea y artículo**, pasa a haber una **cuenta por destino y
artículo**, con tres destinos: tarea, persona, sucursal. Los contadores, los tipos de
movimiento y el invariante del libro son exactamente los de hoy; lo único nuevo es **contra
qué cuenta** se apunta y **quién** puede apuntar.

## 2. Modelo de datos

### 2.1 La cuenta

```ts
export type MaterialAccountKind = "task" | "employee" | "branch";

/** La cuenta de material de un destino y un artículo. `TaskMaterial` es el caso `task`. */
export interface MaterialAccount {
  /** `${kind}_${targetId}_${itemId}` */
  id?: string;
  entityId: string;
  kind: MaterialAccountKind;
  /** El id del destino: taskId, employeeId o branchId, según `kind`. */
  targetId: string;
  /** Siempre: la sucursal de la tarea, la del centro, o la última donde se sacó o declaró para una persona. */
  branchId?: string;
  itemId: string;
  /** El último almacén del que salió. En una tarea no cambia (03 §6); en persona y sucursal, sí. */
  warehouseId?: string;
  reserved: number;
  issued: number;
  reservedIssued: number;
  consumed: number;
  returned: number;
  released: number;
  /** issued - consumed - returned: lo que está fuera del almacén en este destino. */
  pending: number;
  updatedAt: Date;
}
```

**Dónde vive.** `task_materials` **no se toca**: sigue siendo la cuenta de las tareas, con su
clave `${taskId}_${itemId}`, y todo lo que la lee (app, panel, informe de tareas, cuadre al
validar) sigue igual. Las cuentas de persona y sucursal van en una colección nueva,
`entities/{e}/material_accounts/{kind}_{targetId}_{itemId}`, con la forma de arriba. Un solo
tipo en `shared`, `MaterialAccount`, del que `TaskMaterial` es `kind: "task"`. No hay
migración de datos: es lo que permite empezar hoy sin tocar lo que funciona.

**La regla de un almacén por artículo** (03 §6, `material_warehouse_mismatch`) es de la tarea,
que dura días. Una cuenta de persona o de sucursal dura meses: María saca lejía del central en
enero y del almacén de Vallecas en marzo, y es la misma cuenta. En esas dos, `warehouseId` es
**el último almacén del que salió** y no bloquea nada; lo único que depende del almacén es la
devolución, que lo pide (§4.4).

**Salvo una reserva viva.** La dotación sube el `committed` de la existencia de *un* almacén.
Mientras a la cuenta le quede reserva sin salir, `warehouseId` es el de esa reserva y no se
mueve: otra reserva o una liberación desde otro almacén dan `409
inventory/material_warehouse_mismatch`, y una salida desde otro almacén se apunta pero no
descuenta dotación (el compromiso está en el otro). Sin reserva viva, la salida y la
devolución mueven `warehouseId` al almacén del apunte.

### 2.2 El movimiento

`ItemMovement` gana un campo:

```ts
/** En los tipos que tocan una cuenta: contra cuál. Ausente en receipt, adjustment y traspasos. */
accountKind?: MaterialAccountKind;
```

Los ids del destino van en los campos que ya existen, con la semántica de siempre:

| `accountKind` | La cuenta es | `taskId` | `branchId` | `employeeId` |
|---|---|---|---|---|
| `task` | `task_materials/{taskId}_{itemId}` | la tarea | la de la tarea | a quién se imputa (puede ser otro) |
| `employee` | `material_accounts/employee_{employeeId}_{itemId}` | — | donde está (la jornada), si se sabe | **el titular de la cuenta** |
| `branch` | `material_accounts/branch_{branchId}_{itemId}` | — | **el centro de la cuenta** | quién declaró, si fue una persona |

`registeredBy` sigue siendo quien lo escribió. En una cuenta de sucursal, `employeeId` es lo
que permite que el informe por empleado no pierda nada aunque el material fuera del centro.

### 2.3 El libro

`FirestoreLedgerRepository.apply`:

- Los `TASK_TYPES` pasan a llamarse `ACCOUNT_TYPES` (`reservation`, `reservation_released`,
  `issue`, `consumption`, `return`). Para ellos, **`accountKind` es obligatorio** y con él el id
  que corresponda; si faltan, `LedgerError("inventory/account_required")` (sustituye a
  `task_required`, que se mantiene como alias para no romper a nadie).
- La transacción lee y escribe el documento de la cuenta según `accountKind`: el de
  `task_materials` o el de `material_accounts`. **El delta a los contadores es el mismo
  código que hoy** (TDR-002 §1 y 03 §Cómo mueve cada tipo el saldo); solo cambia la referencia.
- Solo en `task` se comprueba `material_warehouse_mismatch`. En las otras dos, `issue` y `return`
  actualizan `warehouseId` de la cuenta al del movimiento.
- `pending` y `outstandingReservation` se calculan igual en las tres.

`findTaskMaterials` sigue como está; se añaden `findAccounts(entityId, kind, targetId)` y
`findAccount(…, itemId)` —con `kind: "task"` leen `task_materials` y la devuelven como cuenta—, y
`findOutstandingAccounts(entityId, kind?)`: cuentas con `pending > 0` de las dos colecciones. El
filtro por almacén se aplica después, sobre ese conjunto, que es lo que está fuera ahora y no
un histórico.

### 2.4 Espejo a Postgres

`item_movements_raw` gana `account_kind VARCHAR(16)` (nullable; `'task'` para lo anterior se
rellena en la misma migración con `UPDATE … WHERE task_id IS NOT NULL`). Migración `034_inventario_cuentas_destino.sql` en
`migrations/` (la 033 es la última a 2026-10-14; si alguien ocupa la 034 antes, la siguiente libre), a
mano por SSH como todas. Las cuentas son instante y no se espejan, como `task_materials`.
`PgMirror.movement` escribe la columna; si la base aún no la tiene (error 42703), escribe sin
ella y vuelve a probar a los diez minutos, para que aplicar la migración no pida reiniciar ni
deje de espejar el resto del libro. `remirror` no cambia.

### 2.5 Índices de Firestore

**Ninguno compuesto.** La ficha es `targetId == … AND kind == …` (dos igualdades, que Firestore
cruza con los índices de campo único) y «fuera del almacén» es `pending > 0` (desigualdad sobre
un solo campo). Comprobado contra dev el 2026-10-14 sin crear nada.

## 3. Permisos

Misma escala (04 §Permisos). Quién puede operar una cuenta, en `permissions.ts`:

```ts
canOperateAccount(actor, kind, targetId, task?):
  task     → canOperateTask(actor, task)                 // como hoy
  employee → actor.employeeId === targetId || canReserve(actor)
  branch   → actor.branchIds.includes(targetId) || canReserve(actor)
```

Reservar (dotación) es siempre de `supervisor` o superior, para los tres. Cuadrar: en la tarea,
quien valida (como hoy); en persona y sucursal, `supervisor` o superior.

## 4. Contratos

Las rutas de `/tasks/:taskId/materials/*` **no cambian**. Las nuevas cuelgan de `/materials` y
llevan el destino en el cuerpo o en la query. `kind: "task"` también se acepta en ellas y
delega en lo de hoy, para que el panel y la app puedan tener un solo cliente.

### 4.1 Lectura

```
GET /materials?entityId&kind=employee|branch|task&id=<targetId>
→ 200 { accounts: MaterialAccount[] }   con itemName, itemUnit, itemType y warehouseName en cada línea
```

Permiso: `canOperateAccount`. Es lo que pinta la pestaña Material del empleado, el bloque
Material de la sucursal y, en la app, «Mi material».

```
GET /me/materials?entityId
→ 200 { accounts: MaterialAccount[] }   las de kind=employee del empleado de la sesión
```

```
GET /materials/outstanding?entityId&warehouseId?&kind?
→ 200 { accounts: Array<MaterialAccount & { targetName, itemName, itemUnit, outstandingReservation }> }
```

Permiso: `supervisor` o superior. Lo que está fuera del almacén, por destino, con nombre
(título de la tarea, nombre de la persona, nombre del centro). Es la vista «Fuera del almacén»
de Existencias y, filtrada por almacén, la de la ficha del almacén.

### 4.2 Asignar (dotación)

```
POST /materials/reserve
{ entityId, movementId, kind, id, items: [{ itemId, warehouseId, quantity }] }
→ 201 { results: [...], warnings: [{ itemId, available, requested }] }
```

Permiso: `supervisor` o superior. Igual que `reserve` de la tarea: sube `committed`, no toca
`onHand`, avisa si no hay bastante y no bloquea. El almacén, el de la línea (cualquiera activo
de la entidad: un centro se puede abastecer desde el central aunque el central no le sirva), o
el de la reserva viva, o se resuelve como en §4.3.

### 4.3 Salida

```
POST /materials/issue
{ entityId, movementId, kind, id, items: [{ itemId, warehouseId?, quantity }], branchId?, employeeId?, occurredAt? }
→ 201 { results: [...] }
```

Permiso: `canOperateAccount`. Efectos como `issue` de la tarea: baja `onHand`, baja
`committed` en lo reservado. **Resolución del almacén**, en este orden: el `warehouseId` de la
línea (cualquiera activo de la entidad); si no, el de la cuenta, si sigue activo; si no, el único almacén que sirve a `branchId` (con `kind: "branch"`, `branchId` es el
centro; con `employee`, el `branchId` del cuerpo, que la app manda con el de la jornada); si
no, el único almacén activo de la entidad; si no, `400 inventory/warehouse_required` con los
candidatos, sin preseleccionar (ADR-002 §4).

`employeeId` con `kind: "branch"` es quién sacó, si fue una persona; con `employee` es el
titular y no se manda.

### 4.4 Declarar gasto y devolver

```
POST /materials/consume
{ entityId, movementId, kind, id, items: [{ itemId, quantity }], branchId?, employeeId?, occurredAt? }
→ 201 { results: [...] }
```

Permiso: `canOperateAccount`. Como `consume` de la tarea: actualiza `consumed` y `pending`. Y
**como en la tarea, si no consta salida, la salida la apunta el consumo**: declarar 2 litros
con 0 sacados genera `issue` + `consumption` con el almacén resuelto como en §4.3. Es lo que
hace que el trabajador nunca tenga que registrar salidas (02 §3 de la guía de cliente).

```
POST /materials/return
{ entityId, movementId, kind, id, items: [{ itemId, warehouseId?, quantity }] }
→ 201 { results: [...] }
```

Permiso: `canOperateAccount`. Con `kind: "task"` responde `400`: el sobrante de una tarea se
cuadra al validarla, como siempre. Devolver lo que sobra: `return`, sube `onHand` del almacén que
recibe, baja `pending`. El almacén se resuelve como en §4.3, con el `warehouseId` de la cuenta
(el último del que salió) como primer candidato. `409 inventory/exceeds_issued` si se devuelve
más de lo pendiente, como hoy.

### 4.5 Cuadrar

```
POST /materials/settle
{ entityId, movementId, kind, id, items: [{ itemId, resolution: "consumed" | "returned" | "released", quantity, warehouseId? }] }
→ 200 { results: [...] }
```

Permiso: `supervisor` o superior (en `task`, quien valida, como hoy, y con sus resoluciones de
siempre: `consumed | returned | used`). `consumed` y `returned`
resuelven pendiente; `released` suelta reserva viva que no va a salir (`reservation_released`,
baja `committed`). **Lo que no se resuelve se queda**: en una persona, en su poder; en una
sucursal, «queda en el centro». No hay obligación de llegar a cero fuera de la tarea.

### 4.6 Lo que no cambia

`GET /tasks/:taskId/materials`, `reserve`, `issue`, `consume` y `settle` de la tarea, el cuadre
al validar, el evento `task.validated` que libera la reserva, la actividad `item_consumed` (solo
en `task`) y los avisos de mínimo (la salida baja `onHand` igual desde donde venga).

### 4.7 Errores nuevos

| Código | Cuándo |
|---|---|
| `400 inventory/account_required` | Un tipo de cuenta sin `accountKind` o sin el id del destino |
| `404 inventory/employee_not_found` | `kind: "employee"` con un empleado que no es de la entidad |
| `404 inventory/branch_not_found` | `kind: "branch"` con una sucursal que no es de la entidad |
| `400 inventory/warehouse_required` | Como hoy, con la lista de candidatos |

## 5. Informes

- **Consumo** (`GET /api/reports/inventory/consumption`): ya agrupa por empleado, centro y
  almacén sin necesitar tarea; gana `groupBy: "destination"` (= `account_kind`, con el nombre
  del destino) para responder «cuánto se va por tareas, cuánto por personas y cuánto por
  centros».
- **Informe de tareas** ([TDR-005](./TDR-005-material-en-el-informe-de-tareas.md)): no cambia;
  es por tarea.
- **Panel y Merlin** ([TDR-006](./TDR-006-material-en-el-panel-y-en-merlin.md)): el eje
  `declara` de la persona se alimenta también de sus declaraciones en cuentas de persona y de
  sucursal (`employee_id` del movimiento), y «consumo sobre asignación» por persona y por centro
  sale de la dotación de §4.2.

## 6. Panel

- **Salida** y **Asignar**, desde el almacén o la ficha del artículo: un selector **A qué va**
  con tarea (buscador de tareas abiertas, como hoy), persona (buscador de empleados) o
  sucursal. El resto del diálogo es el mismo.
- **Ficha del empleado**, pestaña Material: además de los equipos, los consumibles que lleva
  (`GET /materials?kind=employee`), con pendiente, y las acciones declarar, devolver y cuadrar.
- **Ficha de la sucursal**: bloque Material (`kind=branch`) con mandado, gastado, devuelto y lo
  que queda, y el cuadre con «queda en el centro» como lo que no se resuelve.
- **Existencias**: entrada «Fuera del almacén» (`/materials/outstanding`), agrupada por destino,
  con enlace a cada ficha. En la ficha del almacén, lo mismo filtrado por ese almacén.
- Permisos del proxy: añadir `materials(?:/(?:reserve|issue|consume|return|settle|outstanding))?`
  y `me/materials` a la allowlist de `checkinbiz_inventory_handler` (la trampa del 10-oct).

## 7. App

- **«Declarar consumo» desde la jornada**: en la pantalla de fichaje, con una jornada abierta,
  el botón declara contra la **sucursal donde está fichado** (`kind: "branch"`, `id` = ese
  `branchId`, `branchId` igual). Llega precargado con lo que ese centro tiene sin declarar, y lo
  no previsto se añade como en la tarea; si el centro tiene varios almacenes y es no previsto,
  pregunta de cuál, como hoy.
- **«Mi material»**: además de los equipos, los consumibles en su poder (`GET /me/materials`),
  con declarar (`kind: "employee"`) y devolver.
- Si la API no tiene `/materials` todavía, la app esconde los dos puntos y sigue como hoy.
- Textos en los cuatro idiomas; errores por código, nunca el texto crudo.

## 8. Orden de desarrollo

1. **`shared`**: `MaterialAccount`, `accountKind` en el movimiento, el libro (§2.3), repositorio.
2. **`inventory`**: `MaterialOperations` (reserve/issue/consume/return/settle por destino,
   reutilizando lo de `TaskMaterialOperations`), permisos, rutas de §4, migración y espejo.
3. **Prueba contra dev** con el servicio en local: los tres destinos de punta a punta, incluido
   «declarar sin salida apunta la salida» y el cuadre parcial.
4. **Panel y app en paralelo** sobre §6 y §7.
5. **Informes**: el eje destino (§5), después.

## 9. Criterio de éxito

Una empresa sin tareas: administración manda 20 litros de lejía al Lidl Sur desde el almacén
central; una limpiadora fichada allí declara desde la app 2 litros sin haber registrado
ninguna salida; la ficha de la sucursal dice 20 mandados, 2 gastados, 18 que quedan; el informe
de consumo del mes los atribuye al centro y a ella; y nadie ha creado una tarea. Una empresa
con tareas no nota ningún cambio.

## 10. Implementación de la API (2026-10-14)

Rama `feat/material-por-destino` de `encodebiz-api`, desde `develop`.

- `shared`: `entities/MaterialAccount.ts` (tipo, id, `taskMaterialAsAccount`), `accountKind` en
  `ItemMovement`, `inventory/account_required` en `LedgerError`, el libro resolviendo la cuenta
  por destino (`accountOf`) con la regla de la reserva viva de §2.1, y `findAccounts`,
  `findAccount`, `findOutstandingAccounts`.
- `inventory`: `application/use-cases/materials.ts` (`MaterialOperations`: reserve, issue, consume,
  giveBack, settle), `interfaces/http/material/material.router.ts` (las rutas de §4; `kind:
  "task"` delega en `TaskMaterialOperations`), `canOperateAccount` en permisos, espejo con
  `account_kind`, y `migrations/034_inventario_cuentas_destino.sql`.

**Probado contra dev** con el servicio en local, en la entidad de limpieza (Alvarez, sin
tareas), con el owner y con un trabajador:

| Paso | Resultado |
|---|---|
| Salida de 20 al centro sin decir almacén | Sale del único activo; cuenta del centro con 20 pendientes |
| Reintento con el mismo `movementId` | Nada nuevo |
| Declarar 2 en el centro por una persona | Pendiente 18; el apunte lleva a la persona |
| Declarar 3 a una persona sin salida previa | Apunta salida y consumo; pendiente 0 |
| Dotación de 5, salida de 2, devolver 1, cuadre (liberar 3, devolver 1) | `committed` sube a 5 y vuelve a 0; pendiente 0 |
| Fuera del almacén | El centro con 18, con nombre |
| Errores | `kind` inválido 400, persona ajena 404, devolver de más 400, `return` de tarea 400 |
| Trabajador | Su cuenta y la de su centro sí; otra persona, dotación, cuadre y «fuera del almacén», 403 |
| Tarea | `GET /tasks/:id/materials` y `GET /materials?kind=task` dan lo mismo |

El saldo del artículo terminó en lo de partida menos lo declarado (30 → 25, con 5 declarados).
Los apuntes quedan `mirrored: false` en local, sin Postgres; los recoge el `remirror` de
staging.

**Para staging:** aplicar la 034 a mano antes o después del despliegue (el espejo tolera las
dos órdenes) y añadir las rutas a la allowlist del proxy del panel (§6).

## 11. Panel y app (2026-10-14)

**Panel** (`encodebiz-front-saas`, develop y staging):

- «Dar salida» (antes «Salida a una tarea») pregunta **¿A qué va?**: tarea, persona o sucursal.
  Persona y sucursal se buscan en el índice de búsqueda.
- Pestaña **Material** en la ficha del empleado y de la sucursal, solo con el add-on:
  asignar, dar salida, declarar (en la sucursal, con «quién lo usó» opcional), devolver y
  cuadrar.
- Existencias gana la pestaña **Fuera del almacén**, filtrable por destino y almacén.
- Allowlist del proxy con `materials(/reserve|issue|consume|return|settle|outstanding)` y
  `me/materials`, comprobada contra la expresión del proxy.
- Compila en producción. **No probado en el navegador**: el proxy exige sesión con doble
  factor y la prueba quedó en las llamadas directas a la API.

**App** (`checkbiz360`, develop, 1.8.0+58):

- Con la jornada iniciada, la pantalla de fichaje muestra **Material del centro** con
  «Declarar consumo» contra la sucursal donde se ficha; abre la hoja de consumo de la tarea
  y pregunta el almacén si hay varios. La tarjeta lleva a una pantalla con la cuenta del
  centro.
- **Mi material** enseña los consumibles en su poder, con declarar y devolver.
- Sin el add-on, o con una API sin `/materials` (404), no aparece nada.
- `flutter analyze` limpio en lo tocado. Sin probar en un dispositivo.

## 12. Para el pase a producción

1. Migración `034_inventario_cuentas_destino.sql` a mano, antes o después del despliegue (el
   espejo tolera las dos órdenes). Aplicada en staging el 2026-10-14.
2. API: `shared` + `inventory` con la cadena `develop → staging → main`.
3. Panel: el mismo paso; la allowlist del proxy va en el propio código.
4. App: versión 1.8.0+58 o posterior; sin la API nueva, la app esconde lo nuevo.
5. Sin índices de Firestore nuevos.

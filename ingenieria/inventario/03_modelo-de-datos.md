# 03 — Modelo de datos

Siete colecciones en Firestore y su espejo en Postgres. El dominio vive en
`packages/shared/src/checkbiz/inventory/`.

## Vocabulario

Un **artículo** es cualquier cosa que la empresa guarda y usa. Tiene un **tipo**:

- **consumible** — se gasta y no vuelve (toallas, desengrasante, tornillos).
- **operable** — se ocupa un rato y vuelve entero.

Un operable **no es necesariamente una máquina**: una fregadora, una furgoneta, un andamio o un
perro de seguridad entran por la misma puerta. El vocabulario del modelo es neutro a propósito
—identificador y no «número de serie», contador de uso y no «horómetro», no disponible y no
«en mantenimiento»— porque el sesgo de taller cierra mercados que el modelo ya cubre.

Un **almacén** es un sitio donde se guardan artículos. Sirve a una, varias o todas las
sucursales. Una sucursal puede tirar de varios.

---

## 1. `warehouses` — el almacén

```ts
export type WarehouseScope = "entity" | "branches";

export interface Warehouse {
  id?: string;
  entityId: string;
  name: string;
  /** Siempre "branches" desde el 2026-09-29; "entity" solo se lee en documentos anteriores. */
  scope: WarehouseScope;
  /** Al menos una sucursal. El almacén general vive en la principal. */
  branchIds: string[];
  address?: {
    street: string;
    geo?: {lat: number; lng: number};
    postalCode?: string;
    country?: string;
  };
  status: "active" | "inactive";
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}
```

El `scope` es explícito y no «array vacío = todos»: quitar la última sucursal de un almacén no
puede convertirlo en global sin que nadie lo pida. Y simplifica la consulta de «sirve a X o a
todas»: `scope == "entity"` ∪ `branchIds array-contains X`.

La relación con la sucursal va como **array y no como registro aparte**: hoy no lleva ningún
dato propio, y `array-contains` resuelve la consulta. Si algún día la relación necesita
atributos se saca a colección propia siguiendo `EmployeeResponsibility`.

**No hay «almacén principal».** Si una sucursal tiene acceso a varios, el operario elige de cuál
sacó el material; si tiene uno solo, no se le pregunta nada. El porqué, en
[ADR-002](./adr/ADR-002-almacen-entidad-propia-multisucursal.md), «Sin almacén principal».

---

## 2. `items` — la ficha del artículo

```ts
export type ItemType = "consumable" | "operable";

/** Unidad del contador de uso de un operable. Horas para una fregadora,
 *  kilómetros para una furgoneta, jornadas para un animal. */
export type UsageUnit = "hours" | "kilometers" | "days";

export interface Item {
  id?: string;
  entityId: string;
  type: ItemType;
  name: string;
  /** Referencia compartida entre almacenes. Es lo que permite sumar las toallas
   *  de Madrid y las de Barcelona sin que sean dos artículos distintos. */
  reference?: string;
  /** Unidad de medida del consumible: unidad, litro, caja, metro. Texto libre. */
  unit?: string;
  unitCost?: number;
  /** Solo operables: en qué se mide su uso. Obligatorio al crear uno. */
  usageUnit?: UsageUnit;
  category?: string;
  active: boolean;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}
```

**Una sola ficha por empresa**, compartida por todos los almacenes. El `type` decide **dos cosas
y nada más**: cómo existe el artículo en el almacén (cantidades o ejemplares) y cómo se gasta
(se resta o se ocupa). Todo lo demás es común. Ver
[ADR-003](./adr/ADR-003-un-catalogo-consumible-y-operable.md).

---

## 3. `item_units` — el ejemplar de un operable

```ts
export type UnitStatus = "available" | "unavailable" | "retired";

export interface ItemUnit {
  id?: string;
  entityId: string;
  itemId: string;
  /** Serie, matrícula, crotal o microchip. La etiqueta la pone el cliente. */
  identifier?: string;
  label?: string;
  /** Almacén base: donde vive cuando no está asignado. NO es su posición. */
  warehouseId: string;
  status: UnitStatus;
  /** Solo con status "unavailable": avería, revisión, veterinario, descanso… */
  unavailableReason?: string;
  unavailableUntil?: Date;
  /** Lectura acumulada del contador, en la unidad que declara el artículo. */
  usageCounter?: number;
  active: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

Tres fregadoras del mismo modelo son **una ficha y tres ejemplares**.

**Ni la posición ni el «en uso» se guardan en el ejemplar.** Los dos se derivan de la reserva
activa: la posición, del `workSite` de la tarea; el en uso, de que la tarea haya entrado en
curso. Guardar `in_use` aquí contradecía al propio [ADR-006](./adr/ADR-006-operable-se-asigna-a-tareas-con-hora.md):
lo que se deriva no se guarda.

El estado `unavailable` con motivo libre cubre por igual una avería, una ITV, el veterinario y
el descanso obligatorio. Es un estado y un texto, no cuatro estados.

---

## 4. `stock` — la existencia de un consumible

```ts
export interface Stock {
  /** id compuesto: `${itemId}_${warehouseId}` — escritura directa, sin buscar. */
  id?: string;
  entityId: string;
  itemId: string;
  warehouseId: string;
  /** Lo que hay en la estantería. */
  onHand: number;
  /** Lo prometido a tareas que aún no lo han sacado. */
  committed: number;
  /** Umbral de aviso. Ausente = sin aviso. */
  minimum?: number;
  /** onHand < 0: alguien gastó lo que el sistema creía que no había. */
  hasDiscrepancy: boolean;
  updatedAt: Date;
}
```

`onHand - committed` es lo **libre**, y es el número que mira quien asigna. Los tres se
escriben en servidor, en la misma transacción que el movimiento que los cambia.

**`onHand` puede quedar negativo y no se impide.** Si dos cuadrillas gastan las últimas diez
toallas y las dos apuntan diez, las dos dicen la verdad: el que estaba mal era el recuento.
Se registra, se deja el saldo en negativo y se marca `hasDiscrepancy`. Rechazar el segundo
apunte sería borrar un gasto que ocurrió.

Un operable **no tiene `stock`**: tiene ejemplares.

---

## 5. `unit_reservations` — la agenda del operable

```ts
export type ReservationStatus = "reserved" | "in_use" | "released" | "cancelled";
export type ReleaseReason = "completed" | "cancelled" | "rejected" | "manual";

export interface UnitReservation {
  id?: string;
  entityId: string;
  unitId: string;
  itemId: string;
  taskId: string;
  branchId: string;
  startAt: Date;
  endAt: Date;
  status: ReservationStatus;
  reservedBy: string;
  reservedAt: Date;
  releasedAt?: Date;
  releasedReason?: ReleaseReason;
  /** Lecturas del contador al empezar y al terminar. */
  usageStart?: number;
  usageEnd?: number;
}
```

`in_use` lo pone `task.status_changed → in_progress`, de forma **idempotente** —puede llegar
más de una vez, por el «deshacer» `completed → in_progress`—. `released` lo pone el cierre de
la tarea con su motivo; `ReleaseReason` es tipo propio, no reutiliza `TaskPauseEndReason`.

El **choque** se detecta por solapamiento real de intervalos, con hora
([ADR-006](./adr/ADR-006-operable-se-asigna-a-tareas-con-hora.md)).

---

## 6. `task_materials` — la cuenta de material de una tarea

```ts
export interface TaskMaterial {
  /** id compuesto: `${taskId}_${itemId}` */
  id?: string;
  entityId: string;
  taskId: string;
  branchId: string;
  itemId: string;
  /** De qué almacén sale. Se fija en la primera reserva o salida y no cambia. */
  warehouseId?: string;
  /** Prometido por administración. Puede ser 0 si el operario lo cogió sin plan. */
  reserved: number;
  /** Lo que salió físicamente del almacén. */
  issued: number;
  /** La parte de `issued` que salió contra la reserva y descontó compromiso. Lo que sale sin plan no cuenta aquí. */
  reservedIssued: number;
  /** Lo que el operario declara haber gastado. */
  consumed: number;
  /** Lo que volvió al almacén. */
  returned: number;
  /** Compromiso devuelto sin haber salido (al validar, cancelar o rechazar). */
  released: number;
  /** issued - consumed - returned. Si > 0 al validar, hay que cuadrarlo. */
  pending: number;
  updatedAt: Date;
}
```

Es lo que el operario ve en la tarea para saber qué lleva en la furgoneta, y lo que aparece en
la validación para cuadrar el sobrante.

**Un almacén por artículo y tarea.** La clave `taskId_itemId` no permite sacar el mismo
artículo de dos almacenes en una misma tarea, y se acepta a propósito: la declaración de
consumo es *por artículo* —el operario no sabe qué toalla vino de qué estante— y una devolución
repartida entre dos almacenes obligaría a adivinar. Un segundo almacén para el mismo artículo
devuelve `409 inventory/material_warehouse_mismatch`. Es raro, y el libro conserva la verdad
igual.

Va como colección propia y no como subcolección de `tasks/{taskId}/…` para que `inventory` no
escriba dentro de la casa de `tasks`.

---

## 7. `item_movements` — el libro

```ts
export type MovementType =
  | "receipt"              // entrada de compra
  | "reservation"          // compromiso: sube committed, no toca onHand
  | "reservation_released" // lo reservado que no llegó a salir: baja committed
  | "issue"                // salida del almacén hacia una tarea
  | "consumption"          // declaración de gasto
  | "return"               // devolución del sobrante
  | "adjustment"           // ajuste de recuento
  | "transfer_out"         // traspaso: salida
  | "transfer_in";         // traspaso: entrada

export interface ItemMovement {
  /** Lo genera la APP: un reintento de red es la misma escritura, no una segunda. */
  id: string;
  entityId: string;
  type: MovementType;
  itemId: string;
  warehouseId: string;
  /** Solo operables. */
  unitId?: string;
  /** Presente cuando el movimiento viene del campo. */
  taskId?: string;
  branchId?: string;
  /** Consumibles: SIEMPRE positiva. El signo lo pone el tipo. */
  quantity?: number;
  /** Solo traspasos: el mismo en transfer_out y transfer_in. */
  transferId?: string;
  /** Solo adjustment: lo que había antes, para que el ajuste sea auditable. */
  previousOnHand?: number;
  /** Operables: el intervalo ocupado. */
  startAt?: Date;
  endAt?: Date;
  usageCounter?: number;
  /** Quien lo escribe — sale del token, no se pregunta nunca. */
  registeredBy: string;
  registeredByRole: TaskActorRole;
  /** A quién se le imputa el gasto. Por defecto el mismo; puede ser otro. */
  employeeId?: string;
  note?: string;
  /** Cuándo ocurrió. Lo pone el servidor; la app puede mandarlo (preparado para el offline). */
  occurredAt: Date;
  createdAt: Date;
  /** Escrito SIEMPRE, como booleano: Firestore no encuentra campos ausentes. */
  mirrored: boolean;
  mirroredAt?: Date;
}
```

**El movimiento es la verdad; el saldo es derivado.** Si el saldo se desordena, se rehace desde
aquí.

Los dos campos de persona son el corazón del producto. Si el movimiento solo guardara el del
token, el informe de consumo por empleado acabaría diciendo que el 80% se lo gastó el
supervisor. El precedente es `TaskResource.uploadedBy` / `employeeId`.

### Cómo mueve cada tipo el saldo

| Tipo | `onHand` | `committed` |
|---|---|---|
| `receipt` | + | |
| `reservation` | | + |
| `reservation_released` | | − |
| `issue` | − | − (hasta lo reservado) |
| `consumption` | | |
| `return` | + | |
| `adjustment` | = contado | |
| `transfer_out` / `transfer_in` | − / + | |

`consumption` no toca el saldo: el material ya salió con `issue`. Toca `task_materials`.

---

## 8. `unit_assignments` y los papeles del ejemplar — Fase 6, solo diseño

El ejemplar en manos de una persona (`unit_assignments`: quién, desde cuándo, con el acuse del
trabajador y la devolución) y sus documentos (los del servicio documental, con `scope` `unit` e
`item`). Está descrito entero en [07](./07_operables-documentos-y-entregas.md); aquí solo la
regla que afecta a lo demás: **un ejemplar con asignación activa no se ofrece a las tareas**, y
**una revisión obligatoria caducada lo marca en rojo y hace avisar al asignarlo, sin
bloquearlo** (Jose, 2026-10-08). No se añade ningún campo al ejemplar.

## Relaciones

```
Entity ─┬─< Warehouse ─── scope/branchIds >─── Branch   (N:M)
        ├─< Item ─┬─< ItemUnit ──────────> Warehouse    (base)
        │         └─< Stock ─────────────> Warehouse    (1 por artículo+almacén)
        └─< ItemMovement ──> Item, Warehouse, Unit?, Task?, Employee(imputado), Actor(registra)

Task ─┬─< TaskMaterial ──> Item, Warehouse (uno por artículo)
      └─< UnitReservation ──> ItemUnit
```

- La **empresa** tiene almacenes y artículos.
- El **almacén** sirve a varias sucursales; una sucursal puede tirar de varios. Madrid Norte y
  Madrid Sur comparten Vallecas.
- El **artículo** tiene una existencia por almacén si es consumible, y ejemplares si es
  operable, cada uno con su almacén base.
- La **tarea** es la bisagra: tiene material asignado y ejemplares reservados, y de ella cuelgan
  su sucursal, sus empleados y su sitio.
- El **movimiento** ata a todos.

## Espejo en Postgres — migración `023`

`dim_warehouses`, `dim_items`, `dim_item_units` (por `SyncDimensions`), `item_movements_raw` y
`unit_reservations_raw` (por `inventory`). Detalle en
[TDR-004](./tdr/TDR-004-espejo-postgres-e-informes.md). La migración se aplica **a mano por
SSH**, nunca desde el despliegue.

## Índice de búsqueda

Si artículos y almacenes se buscan desde el panel, entran en `searchIndex` — y su borrado tiene
que acordarse de retirar la entrada. Ver [06 §D7](./06_decisiones-abiertas.md).

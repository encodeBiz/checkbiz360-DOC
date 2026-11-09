# 03 — Modelo de datos

Todo en `packages/shared/src/checkbiz/customers/`, con repositorios Firestore como el resto
del dominio ([shared como único dueño del dominio](../../ingenieria/)). Nombre en código:
`customer`, no `client`: `client` ya es el cliente OAuth del asistente y el cliente HTTP de
media docena de sitios. En pantalla, **«Clientes»**.

## El cliente

```ts
export type CustomerKind = "company" | "person";
export type CustomerStatus = "active" | "inactive";

export interface CustomerContact {
  name: string;
  role?: string;          // «presidenta de la comunidad», «hija», «jefe de obra»
  phone?: string;
  email?: string;
  /** Lo ve la persona de campo desde la tarea. Por defecto false: el teléfono de la hija de Juana no es de toda la plantilla. */
  visibleToWorkers: boolean;
}

export interface Customer {
  id?: string;
  entityId: string;
  kind: CustomerKind;
  name: string;              // «Comunidad Diagonal 400», «Juana Pérez», «Constructora X»
  taxId?: string;
  reference?: string;        // su código en el programa de facturación de la empresa
  contacts: CustomerContact[];
  /**
   * Dónde está el cliente: su domicilio o su sede. La forma del `workSite` de la tarea
   * (calle, punto, margen), capturada con el mismo campo del panel. Los sitios donde se
   * trabaja para él son `sites`, aparte (añadido 2026-11-03).
   */
  address?: TaskWorkSite;
  /**
   * A qué sucursales se asigna. Misma forma que el almacén (inventario ADR-002): `entity` es
   * «todas» y es explícito; `branches` lista. Quitar la última sucursal no convierte al
   * cliente en global sin que nadie lo pida.
   */
  scope: "entity" | "branches";
  branchIds: string[];
  /**
   * Sucursales DEDICADAS a este cliente: las jornadas fichadas allí son suyas aunque la
   * tarea no lleve cliente (construcción: la obra). Subconjunto de `branchIds`. El servidor
   * impide que una sucursal esté dedicada a dos clientes. Ver ADR-003.
   */
  dedicatedBranchIds: string[];
  /** Lo que la persona de campo tiene que saber al llegar: «llaves en el buzón», «llamar antes». */
  fieldNotes?: string;
  /** Notas de gestión; no salen de la ficha. */
  notes?: string;
  status: CustomerStatus;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface CustomerRate {
  hourly: number;            // céntimos, como el resto de importes de la plataforma
  currency: "EUR";
  validFrom: Date;
}
```

El cliente **no lleva horario, ni empleados, ni tareas**. Las tareas apuntan a él; él no
apunta a ellas. Es la misma dirección que almacén → movimientos.

## El lugar

Subcolección `customers/{customerId}/sites`. Un cliente tiene uno o varios. La forma es la
del `workSite` de la tarea, porque es lo que la tarea va a recibir copiado:

```ts
export type CustomerSiteKind = "address" | "branch";

export interface CustomerSite {
  id?: string;
  entityId: string;
  customerId: string;
  name: string;                       // «Domicilio», «Edificio A», «Obra Meridiana»
  kind: CustomerSiteKind;
  /** `address`: la dirección geocodificada con su geocerca. Misma forma que `TaskWorkSite`. */
  workSite?: TaskWorkSite;
  /** `branch`: el lugar ES una sucursal (construcción). La dirección se lee de la sucursal, no se copia. */
  branchId?: string;
  /** Un lugar puede tener principio y fin: una obra, un evento. Solo informativo en v1; en rojo si la tarea cae fuera. */
  startsAt?: Date;
  endsAt?: Date;
  status: "active" | "inactive";
  createdAt: Date;
  updatedAt: Date;
}
```

Juana: un lugar `address`, «Domicilio». La comunidad con tres edificios: tres `address`.
Constructora X: tres lugares `branch`, uno por obra, y las tres sucursales en
`dedicatedBranchIds`. Un lugar `branch` solo puede apuntar a una sucursal de `branchIds`.

## El contrato

Subcolección `contracts`. Un contrato es **un documento del documental con vigencia y, si
se quiere, alcance**:

```ts
/** Dónde se ejecuta el contrato: el montaje. Una sucursal o una tarea, nunca un cliente ni varias (ADR-006, D12). */
export type ContractLink =
  | { kind: "branch"; branchId: string }
  | { kind: "task"; taskId: string };

/** Lo que dice el contrato y que se puede leer del PDF. Todo opcional, todo editable. */
export interface ContractTerms {
  amount?: number;                    // céntimos; el precio cerrado con el cliente
  currency?: "EUR";
  estimatedHours?: number;            // horas de trabajo, no días de calendario
  complexity?: 1 | 2 | 3 | 4 | 5;
}

export interface CustomerContract extends ContractTerms {
  id?: string;
  entityId: string;
  customerId: string;
  title: string;
  /** El PDF, en `documents` con `scope: "customer"`. Opcional: hay contratos verbales que igual conviene apuntar. */
  documentId?: string;
  /** El montaje. Sin él, el contrato solo tiene vigencia (Fase 4); con él, rentabilidad (Fase 5). */
  link?: ContractLink;
  startsAt: Date;
  endsAt?: Date;                      // sin fin = indefinido
  /** Cuántos días antes del fin se pone en rojo. Por defecto 30. */
  warnDaysBefore: number;
  notes?: string;
  /**
   * Lo que la IA leyó del PDF al subirlo, con la cita de la que sale cada dato. Se guarda
   * una vez y no se reescribe aunque el documento se vuelva a leer: es la evidencia de por
   * qué el formulario salió relleno como salió.
   */
  extraction?: {
    terms: ContractTerms & { startsAt?: Date; endsAt?: Date };
    evidence: Array<{ field: keyof ContractTerms | "startsAt" | "endsAt"; quote: string; page?: number }>;
    confidence: "high" | "medium" | "low";
    model: string;
    extractedAt: Date;
  };
  /**
   * Lo estimado la primera vez que se guardó con vínculo. Solo lectura: la previsión aprende
   * de esto, no de `estimatedHours`, que alguien puede corregir al final para que cuadre.
   */
  initialEstimate?: ContractTerms & { savedAt: Date };
  /** El montaje acabó. Desde aquí entra en el histórico de previsión (`contract_outcomes`). */
  closedAt?: Date;
  closedBy?: string;
  status: "active" | "ended";
  createdAt: Date;
  updatedAt: Date;
}
```

Vencido o a punto de vencer: **rojo en la ficha y en la lista, y nada más**. No se bloquea
crear tareas a un cliente sin contrato vigente; la empresa sabe mejor que nosotros por qué
sigue yendo.

Vincular a una sucursal exige que esté en `dedicatedBranchIds` del cliente: así sus jornadas
ya son del cliente por el ADR-003 y no hace falta otra regla. Si no lo está, 409
`BRANCH_NOT_DEDICATED` y el panel ofrece dedicarla en el mismo gesto. Una tarea solo se
vincula si es del mismo cliente (`task.customerId`). Un montaje —sucursal o tarea— tiene como
mucho un contrato activo vinculado; una tarea con contrato dentro de una sucursal con
contrato se ve por separado y **cuenta dentro** de la sucursal, no dos veces en el cliente.

## El presupuesto

**No existe como objeto** desde el 2026-11-03 ([ADR-006](./adr/ADR-006-el-contrato-es-el-montaje.md)).
Lo que se acordó con el cliente es el contrato, con su `amount`; el desvío es la rentabilidad
del contrato vinculado. `CustomerBudget` y `customer_budgets` no se construyen.

## La rentabilidad

No se guarda: **se calcula al leer** sobre lo que el montaje imputa en el periodo del
contrato (de `startsAt` a `endsAt`, o a hoy):

- **Horas y coste de RRHH**: filas de `customer_hours_daily` con `branch_id` del vínculo
  (sucursal) o `task_id` del vínculo (tarea). `minutes × hourly_cost_cents / 60`, en bruto.
  Las horas de jornadas sin cerrar se cuentan aparte y no se valoran; la respuesta dice su
  cobertura, como la carga operativa.
- **Material**: `item_movements_raw` con ese `task_id` o ese `branch_id` en el periodo,
  `quantity × unit_cost` de `dim_items`. Sin `unit_cost`: cantidad sí, importe no.
- **Margen**: `amount − (labour + materials)`, solo si hay `amount`. Sin importe, coste y
  horas, y ningún margen que parezca un cero.

## La previsión

Aprende del histórico de montajes cerrados, nunca de un formulario:

- Al **cerrar** un contrato vinculado se escribe una fila en `contract_outcomes` con lo
  estimado al principio (`initialEstimate`), lo estimado al final, lo real (minutos, coste,
  material, personas, días) y el importe.
- El **sesgo** de la empresa por complejidad es la mediana de `actual / initialEstimate`
  sobre sus montajes cerrados de esa complejidad; la horquilla, los percentiles 25 y 75. Hace
  falta un mínimo de **5 cerrados** de esa complejidad, o 5 en total para un sesgo global sin
  partir por complejidad. Por debajo, `insufficient_history` y ningún número.
- **Antes de empezar**: `estimatedHours × sesgo × coste medio por hora` de los montajes
  parecidos → horquilla de coste y de margen.
- **Durante**: lo consumido + `(estimatedHours × sesgo − horas reales) × coste medio por hora
  de este montaje` → horquilla y, si cruza el importe, la fecha prevista a ritmo de los
  últimos 7 días (`overBudgetAt`).

Se calcula al leer. **Pero cada previsión que se enseña se guarda** (`contract_forecasts`,
abajo): una previsión que no queda registrada no se puede corregir después. Se afina por
equipo (qué personas fueron) **después**, si los números lo piden.

## El histórico: lo que se guarda para poder predecir

Decidido el 2026-11-03 con Jose: *«los datos son nuestra fuerza para ir tirando a
predicción; todo esto tributa sobre análisis, analítica e IA y debe quedar registrado»*. Lo
que ya hay en Postgres es mucho y **no se borra nunca** —no existe ninguna purga en el
repositorio, comprobado el 2026-11-03—: `checklogs_raw` guarda cada fichaje con su
`employee_price` congelado, `tasks_raw` cada tarea con inicio, fin y pausas,
`item_movements_raw` cada movimiento con tarea y sucursal, `task_ratings_raw`,
`employee_daily_reports`, `operational_daily` (con `labor_cost`, `material_cost` y
`rate_coverage` por sucursal y día), `pattern_snapshots`, `headcount_daily` y
`employee_status_events`. Lo que falta son cuatro huecos concretos, y tres reglas.

### Las tres reglas

1. **Nada agregado sin su crudo.** Un agregado (`customer_hours_daily`, `contract_outcomes`)
   se puede recalcular desde el crudo; el crudo no se puede recuperar desde el agregado. El
   crudo manda, y se queda.
2. **Cada decisión humana es un evento con fecha y autor.** Quién estimó qué, quién cambió
   la estimación, quién vinculó, quién cerró. El estado actual está en la ficha; cómo se
   llegó a él, en la tabla de eventos. Es lo que permite distinguir «estimó mal» de
   «corrigió al final para que cuadrase».
3. **Cada predicción se guarda con su base.** Qué se enseñó, cuándo, sobre cuántos cerrados
   y con qué sesgo. Cuando el montaje cierra, la predicción se puede puntuar. Sin eso, el
   modelo no mejora: solo cambia.

### Los cuatro huecos

| Hueco | Qué pasa hoy | Qué se añade |
|---|---|---|
| **El fichaje no sabe de qué tarea fue** en Postgres | `CheckLog.taskId` existe en Firestore (horario por tareas) y el espejo no lo copia | `checklogs_raw.task_id`; el esfuerzo por persona en una tarea pasa de inferido a registrado |
| **El puesto no se espeja, y su precio tampoco** | `dim_responsibilities` lleva responsabilidad y nivel; `dim_employees`, un `job_title`; el precio solo viaja en el fichaje | `dim_responsibilities.job_name` y `job_price_cents`, y `responsibility_events` con cada cambio de puesto o de precio, fechado. Así se aprende «dos electricistas y un peón», no solo «tres personas» |
| **La tarea solo guarda su estado final** | `assigned_employee_ids` es el actual; quién entró, quién salió y cuándo se pierde; el historial de la tarea vive solo en Firestore | `task_events_raw`: espejo del historial de la tarea (asignación, inicio, pausa, cierre, validación, rechazo), con actor y fecha |
| **El contrato y la previsión no dejan rastro** | nada, porque no existen todavía | `contract_events` y `contract_forecasts`, abajo |

### Postgres: los tres primeros huecos, hechos (migración `050`, rama `feat/historico-prevision`, 2026-11-03)

Van en la `050` y no en la `049` porque no dependen de la cartera: la `049` sigue siendo de
clientes. Lo que se tapó y cómo:

- **`checklogs_raw.task_id`**, rellenado hacia atrás desde `schedule_applied->>'taskId'`
  (ahí estaba ya, dentro del JSON) y a partir de ahora en cada fichaje, derivado en
  `upsertChecklogRaw` de `shared` sin tocar el payload del trigger.
- **`dim_responsibilities.job_name` y `job_price`** (tarifa por hora, misma unidad que
  `checklogs_raw.employee_price`, para sumarlas sin convertir; no céntimos) y
  **`responsibility_events`**, una fila por alta, retirada o cambio de puesto o precio, con
  `previous_*`. Las escribe `SyncDimensions` de `analytics` al ver la diferencia con lo que
  tenía; `changed_at` es la fecha del alta (`assignedAt`) o, en un cambio, la de la pasada
  que lo vio. No hay `changed_by`: el panel no deja quién cambió el puesto en la
  responsabilidad, y no se inventa.
- **`task_events_raw`**, espejo 1:1 de `activity` de cada tarea: `id, entity_id, task_id,
  branch_id, type, actor_id, actor_role, payload, occurred_at`. Lo escribe el propio
  `FirestoreTaskRepository` de `shared` (gancho `afterActivity`, a mejor esfuerzo) porque el
  historial lo alimentan cuatro servicios —`tasks`, `inventory`, `checkinbiz`,
  `firebase_sdk`—; el `remirror` de tareas lo repasa en su ventana y
  `backfill-tasks --history` lo rellena hacia atrás. `employee_id`, `fromStatus`, `toStatus` y
  `metadata` van dentro de `payload`.

El SQL exacto está en `migrations/050_historico_prevision.sql`.

### Postgres: lo que queda para la Fase 5 (con el contrato)

```sql
-- Cada decisión humana sobre el contrato. El estado actual está en customer_contracts; aquí,
-- cómo se llegó a él.
CREATE TABLE IF NOT EXISTS contract_events (
  id                BIGSERIAL PRIMARY KEY,
  entity_id         TEXT NOT NULL,
  contract_id       TEXT NOT NULL,
  type              TEXT NOT NULL,         -- 'extracted' | 'terms_set' | 'terms_changed' | 'linked' | 'unlinked' | 'closed' | 'reopened'
  actor_id          TEXT,                  -- NULL cuando el actor es la IA ('extracted')
  field             TEXT,                  -- 'amount' | 'estimatedHours' | 'complexity' | 'startsAt' | 'endsAt'
  previous_value    JSONB,
  new_value         JSONB,
  source            TEXT,                  -- 'ai' | 'panel' | 'assistant' | 'script'
  occurred_at       TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS contract_events_contract_idx ON contract_events (contract_id, occurred_at);

-- Cada previsión que se enseñó. Al cerrar el contrato se puntúa contra contract_outcomes.
CREATE TABLE IF NOT EXISTS contract_forecasts (
  id                BIGSERIAL PRIMARY KEY,
  entity_id         TEXT NOT NULL,
  contract_id       TEXT NOT NULL,
  made_at           TIMESTAMPTZ NOT NULL,
  stage             TEXT NOT NULL,         -- 'before_start' | 'in_progress'
  hours_consumed    NUMERIC(10,2),         -- en qué punto estaba el montaje
  hours_low         NUMERIC(10,2), hours_mid NUMERIC(10,2), hours_high NUMERIC(10,2),
  cost_low_cents    BIGINT, cost_mid_cents BIGINT, cost_high_cents BIGINT,
  over_budget_at    DATE,
  basis_closed_contracts SMALLINT NOT NULL,
  basis_complexity  SMALLINT,
  basis_bias        NUMERIC(6,3),
  model_version     TEXT NOT NULL,         -- 'median-bias-v1'; cuando cambie la fórmula, cambia esto
  -- Rellenado al cerrar: error de la previsión mid frente a lo real.
  scored_at         TIMESTAMPTZ,
  hours_error_pct   NUMERIC(6,2),
  within_range      BOOLEAN
);
CREATE INDEX IF NOT EXISTS contract_forecasts_contract_idx ON contract_forecasts (contract_id, made_at);
```

Con esto, al cabo de un año una empresa tiene, por cada montaje: el contrato tal como se leyó,
cada corrección y quién la hizo, quién trabajó cada día y a qué precio, con qué puesto, qué
material salió, cuánto se predijo en cada momento y cuánto se acertó. Es lo que hace falta
para pasar del sesgo por complejidad a la previsión por equipo, y para que Merlin narre
«estimáis bien las obras pequeñas y os vais en las grandes» con el dato detrás.

## El cliente en la tarea

En `Task` (`shared`), aditivo y todo opcional:

```ts
export interface Task {
  …
  customerId?: string;
  customerSiteId?: string;
  /**
   * Snapshot para la app, que lee la tarea de Firestore y no va a ir a otra colección a
   * buscar el nombre. Lo escribe el panel al asignar; si el cliente cambia de nombre, las
   * tareas pasadas conservan el que tenían, que es lo correcto en un histórico.
   */
  customer?: {
    id: string;
    name: string;
    /** Solo contactos con `visibleToWorkers`. */
    contacts?: Array<{name: string; role?: string; phone?: string}>;
    fieldNotes?: string;
  };
}
```

El `workSite` de la tarea se **copia** del lugar al asignar. No se referencia: si la geocerca
del lugar cambia después, la tarea de ayer fichó contra la de ayer y eso es lo que tiene que
quedar. Cambiar el lugar del cliente actualiza las tareas **futuras** (`scheduledStartAt`
posterior a ahora, estado `draft` o `assigned`) en el momento de guardar, y lo dice.

En `tasks_raw`: `customer_id`, `customer_site_id`. El `customer.name` no se espeja: se
resuelve por `dim_customers` y, si no está, «cliente desconocido».

## El documento del cliente

En `documents`, aditivo:

```ts
export type DocumentScope = "entity" | "branch" | "employee" | "item" | "unit" | "customer";
// ManagedDocument
customerId?: string;   // required if scope = "customer"
```

Ruta en Storage: `media/entities/{entityId}/checkinbiz/customers/{customerId}/documents/…`.
Lleva la empresa y el trigger lo cuenta solo. `visibleToRoles` decide qué ve quién; para que
una trabajadora vea un documento del cliente tiene que llevar `worker` **y** ella tener una
tarea asignada de ese cliente (lo comprueba `customers`, no `documents`: el documental sigue
sin saber de tareas).

## El índice de búsqueda

Una entrada por cliente en `searchIndex` con `kind: "customer"`, nombre, NIF, referencia y la
calle de su dirección, como la sucursal.
Se escribe en el repositorio al crear y editar, se retira al borrar, y
`reindex-search` de rentman la reconstruye con el resto. Los lugares no se indexan: se buscan
dentro del cliente.

## Postgres (migración `049`)

```sql
CREATE TABLE IF NOT EXISTS dim_customers (
  customer_id       TEXT PRIMARY KEY,
  entity_id         TEXT NOT NULL,
  kind              TEXT NOT NULL,
  name              TEXT NOT NULL,
  tax_id            TEXT,
  reference         TEXT,
  scope             TEXT NOT NULL,
  status            TEXT NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL,
  updated_at        TIMESTAMPTZ NOT NULL,
  deleted_at        TIMESTAMPTZ,
  synced_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dim_customer_sites (
  site_id           TEXT PRIMARY KEY,
  customer_id       TEXT NOT NULL,
  entity_id         TEXT NOT NULL,
  name              TEXT NOT NULL,
  kind              TEXT NOT NULL,
  branch_id         TEXT,
  lat               DOUBLE PRECISION,
  lng               DOUBLE PRECISION,
  radius_m          INTEGER,
  time_zone         TEXT,
  starts_at         TIMESTAMPTZ,
  ends_at           TIMESTAMPTZ,
  status            TEXT NOT NULL,
  updated_at        TIMESTAMPTZ NOT NULL,
  synced_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS customer_branch_links (
  customer_id       TEXT NOT NULL,
  branch_id         TEXT NOT NULL,
  entity_id         TEXT NOT NULL,
  dedicated         BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (customer_id, branch_id)
);
-- Una sucursal dedicada a un solo cliente: lo impone el servidor en Firestore y lo
-- vigila aquí un índice único parcial.
CREATE UNIQUE INDEX IF NOT EXISTS customer_branch_links_dedicated_uq
  ON customer_branch_links (branch_id) WHERE dedicated;

CREATE TABLE IF NOT EXISTS customer_contracts ( … );   -- espejo 1:1 de la subcolección
-- Espejo 1:1 de la subcolección, con lo que dice el contrato y el vínculo (ADR-006).
CREATE TABLE IF NOT EXISTS customer_contracts (
  contract_id       TEXT PRIMARY KEY,
  customer_id       TEXT NOT NULL,
  entity_id         TEXT NOT NULL,
  title             TEXT NOT NULL,
  document_id       TEXT,
  link_kind         TEXT,                 -- 'branch' | 'task' | NULL
  link_branch_id    TEXT,
  link_task_id      TEXT,
  starts_at         TIMESTAMPTZ NOT NULL,
  ends_at           TIMESTAMPTZ,
  amount_cents      BIGINT,
  estimated_hours   NUMERIC(10,2),
  complexity        SMALLINT,
  initial_estimated_hours NUMERIC(10,2),
  initial_complexity      SMALLINT,
  closed_at         TIMESTAMPTZ,
  status            TEXT NOT NULL,
  updated_at        TIMESTAMPTZ NOT NULL,
  synced_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- Un montaje, un contrato activo.
CREATE UNIQUE INDEX IF NOT EXISTS customer_contracts_branch_active_uq
  ON customer_contracts (link_branch_id) WHERE link_kind = 'branch' AND status = 'active';
CREATE UNIQUE INDEX IF NOT EXISTS customer_contracts_task_active_uq
  ON customer_contracts (link_task_id) WHERE link_kind = 'task' AND status = 'active';
-- customer_budgets NO se crea (ADR-006).

-- Lo que dejó cada montaje al cerrarse: de aquí aprende la previsión. Una fila por cierre;
-- reabrir y volver a cerrar la sustituye.
CREATE TABLE IF NOT EXISTS contract_outcomes (
  contract_id       TEXT PRIMARY KEY,
  entity_id         TEXT NOT NULL,
  customer_id       TEXT NOT NULL,
  link_kind         TEXT NOT NULL,
  complexity        SMALLINT,              -- la inicial
  initial_estimated_hours NUMERIC(10,2),
  final_estimated_hours   NUMERIC(10,2),
  actual_minutes    INTEGER NOT NULL,      -- solo jornadas fiables
  unclosed_minutes  INTEGER NOT NULL,
  labour_cost_cents BIGINT NOT NULL,
  material_cost_cents BIGINT,              -- NULL si no hay inventario o nada tiene coste
  amount_cents      BIGINT,
  people_count      SMALLINT NOT NULL,
  days_count        SMALLINT NOT NULL,
  closed_at         TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS contract_outcomes_entity_idx
  ON contract_outcomes (entity_id, complexity, closed_at);

ALTER TABLE tasks_raw ADD COLUMN IF NOT EXISTS customer_id TEXT;
ALTER TABLE tasks_raw ADD COLUMN IF NOT EXISTS customer_site_id TEXT;
CREATE INDEX IF NOT EXISTS tasks_raw_customer_idx ON tasks_raw (entity_id, customer_id, due_at);

-- Horas por cliente y día. La materializa un job de customers (cada noche y al cerrar
-- cada tarea con cliente); el informe no recalcula desde los fichajes.
CREATE TABLE IF NOT EXISTS customer_hours_daily (
  entity_id         TEXT NOT NULL,
  customer_id       TEXT NOT NULL,
  site_id           TEXT,
  employee_id       TEXT NOT NULL,
  day               DATE NOT NULL,
  source            TEXT NOT NULL,        -- 'task' | 'dedicated_branch'
  task_id           TEXT,
  branch_id         TEXT,
  minutes           INTEGER NOT NULL,
  -- Jornada bien cerrada o no (los tres cajones de la carga operativa). Solo las fiables se valoran.
  reliable          BOOLEAN NOT NULL DEFAULT true,
  -- `employee_responsibility.job.price` del puesto en esa sucursal el día del fichaje, en
  -- céntimos/hora, bruto. Se congela aquí para que subir el sueldo no reescriba el pasado.
  hourly_cost_cents INTEGER,
  computed_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS customer_hours_daily_branch_idx
  ON customer_hours_daily (entity_id, branch_id, day) WHERE branch_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS customer_hours_daily_task_idx
  ON customer_hours_daily (entity_id, task_id) WHERE task_id IS NOT NULL;
-- Una clave primaria no admite expresiones; la unicidad va por índice sobre la fuente
-- concreta (la tarea o la sucursal dedicada).
CREATE UNIQUE INDEX IF NOT EXISTS customer_hours_daily_uq
  ON customer_hours_daily (entity_id, customer_id, employee_id, day, source, COALESCE(task_id, branch_id));
CREATE INDEX IF NOT EXISTS customer_hours_daily_period_idx
  ON customer_hours_daily (entity_id, customer_id, day);
```

La regla que llena `customer_hours_daily` está en el
[ADR-003](./adr/ADR-003-la-tarea-lleva-el-cliente-y-las-horas-se-imputan-por-tarea-o-por-sucursal-dedicada.md):
`source = 'task'` para los minutos de una tarea con cliente (de `started_at` a
`completed_at` menos `paused_ms`); `source = 'dedicated_branch'` para las jornadas de
`checklogs_raw` en una sucursal dedicada **que no caigan dentro de una tarea con cliente del
mismo empleado ese día**, para no contar dos veces la misma hora.

## Borrados

- **Cliente:** blando, `status: "inactive"`, desaparece de los selectores y se queda en el
  histórico. Borrado de verdad solo si no tiene ninguna tarea ni documento; si los tiene,
  409 y se dice cuántos. Retira la entrada de `searchIndex`.
- **Lugar:** blando. Las tareas futuras que lo usan se avisan en la respuesta; no se tocan.
- **Sucursal con clientes asignados:** el borrado de sucursal ya devuelve 409 y pide elegir
  cuando tiene tareas; se le añade el aviso de clientes asignados y se desasigna. El cliente
  **no** se borra con la sucursal: es suyo, no de ella.

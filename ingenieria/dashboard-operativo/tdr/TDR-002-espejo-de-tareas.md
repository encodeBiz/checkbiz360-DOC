# TDR-002 — Espejo de tareas: `tasks_raw`, repositorio espejado, reintento y backfill

**Fecha:** 2026-10-10
**Estado:** Diseño
**Componente:** `services/tasks` — `src/infrastructure/MirroredTaskRepository.ts`, `src/jobs/remirror.ts`, `src/scripts/backfill-tasks.ts`; migración `026_tareas_espejo.sql`
**Decisión de referencia:** [ADR-003](../adr/ADR-003-las-tareas-se-espejan-desde-el-servicio-de-tareas.md)
**Patrón copiado:** [inventario TDR-004](../../inventario/tdr/TDR-004-espejo-postgres-e-informes.md)

---

## 1. Qué se espeja y quién lo escribe

| Origen (Firestore) | Destino (Postgres) | Quién | Cadencia |
|---|---|---|---|
| `entities/{e}/tasks/{t}` | `tasks_raw` | **`tasks`**, en la petición | Inmediata + job cada 5 min |

Sólo el documento de la tarea. Asignaciones, notas, evidencias, valoraciones, validaciones,
pausas y actividad **no** se espejan: el dashboard no las necesita y `task_ratings_raw` ya
existe por otro camino.

**No pasa por `sync`** ni por un trigger de Firebase. Todas las escrituras que cambian una
tarea entran por `tasks` ([01_as-is §3](../01_as-is.md)), así que es `tasks` quien inserta.

## 2. Migración `026_tareas_espejo.sql`

```sql
-- encodeBiz Analytics — espejo de tareas (dashboard-operativo, ADR-003).
-- Motor: PostgreSQL 16+ | Todas las sentencias son idempotentes.
--
-- Lo escribe `tasks` en la propia petición, tras confirmar Firestore, a mejor esfuerzo; el
-- job `remirror` recoge lo que no llegó. Una fila por tarea, upsert por `task_id`: la tarea
-- cambia de estado, así que no vale un `DO NOTHING`. Un borrado no borra la fila: deja
-- `deleted_at`, porque el histórico semanal no puede perder una tarea que existió.

CREATE TABLE IF NOT EXISTS tasks_raw (
  task_id                 VARCHAR(128)  PRIMARY KEY,
  entity_id               VARCHAR(128)  NOT NULL,
  branch_id               VARCHAR(128)  NOT NULL,
  title                   TEXT          NOT NULL,
  status                  VARCHAR(20)   NOT NULL,   -- draft | assigned | in_progress | completed | validated | rejected | cancelled
  -- Se espeja por completitud y para el Panel mensual. El dashboard NO lo lee para decidir
  -- retrasos: sólo cambia al iniciar o completar (ADR-005).
  time_compliance_status  VARCHAR(24),
  priority                VARCHAR(10),
  scheduled_start_at      TIMESTAMPTZ,
  due_at                  TIMESTAMPTZ   NOT NULL,
  started_at              TIMESTAMPTZ,
  completed_at            TIMESTAMPTZ,
  validated_at            TIMESTAMPTZ,
  rejected_at             TIMESTAMPTZ,
  cancelled_at            TIMESTAMPTZ,
  assigned_employee_ids   JSONB         NOT NULL DEFAULT '[]',
  paused_at               TIMESTAMPTZ,
  paused_ms               BIGINT        NOT NULL DEFAULT 0,
  pause_count             INTEGER       NOT NULL DEFAULT 0,
  created_by              VARCHAR(128),
  completed_by            VARCHAR(128),
  validated_by            VARCHAR(128),
  -- La referencia con la que `findByExternalRef` reconoce una tarea creada por un sistema
  -- (Rentman, cuadrantes). Se mapea desde donde la lea el repositorio.
  external_ref            TEXT,
  -- Zona del lugar de trabajo cuando la tarea tiene `workSite`; si no, la del centro.
  work_site_tz            VARCHAR(80),
  created_at              TIMESTAMPTZ   NOT NULL,
  updated_at              TIMESTAMPTZ   NOT NULL,
  deleted_at              TIMESTAMPTZ,
  synced_at               TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- Las de hoy y las que arrastran (TDR-001 §1, consulta 5).
CREATE INDEX IF NOT EXISTS idx_tasks_raw_entity_due
  ON tasks_raw (entity_id, due_at) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_tasks_raw_entity_status_due
  ON tasks_raw (entity_id, status, due_at) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_tasks_raw_entity_branch
  ON tasks_raw (entity_id, branch_id, due_at) WHERE deleted_at IS NULL;
-- Para el cierre diario por `completed_at` y para el Panel mensual.
CREATE INDEX IF NOT EXISTS idx_tasks_raw_entity_completed
  ON tasks_raw (entity_id, completed_at) WHERE completed_at IS NOT NULL;
-- Para la frescura y el remirror.
CREATE INDEX IF NOT EXISTS idx_tasks_raw_entity_synced
  ON tasks_raw (entity_id, synced_at DESC);
-- Filtros por persona, cuando lleguen.
CREATE INDEX IF NOT EXISTS idx_tasks_raw_assignees
  ON tasks_raw USING GIN (assigned_employee_ids);
```

**Se aplica a mano por SSH**, nunca desde el despliegue. En producción, mirando el resultado.

## 3. `MirroredTaskRepository`

En `services/tasks/src/infrastructure/`, extiende `FirestoreTaskRepository` de `shared` y
sustituye a `taskRepository` en `task.helpers.ts` (hoy `new FirestoreTaskRepository()`).
Mismo molde que `MirroredItemRepository` de inventario:

```ts
async create(task)                 { const c = await super.create(task); await quietly(c.id, () => this.mirror.task(c)); return c; }
async update(id, entityId, data)   { await super.update(id, entityId, withUpdatedAt(data)); await this.remirrorOne(entityId, id); }
async updateClosingPause(...)      { await super.updateClosingPause(...); await this.remirrorOne(entityId, id); }
async pause(...) / resume(...)     { const r = await super.pause(...); await this.remirrorOne(entityId, id); return r; }
async delete(entityId, id)         { const snapshot = await this.findById(id, entityId); const r = await super.delete(entityId, id);
                                     if (snapshot) await quietly(id, () => this.mirror.deleted(snapshot, new Date())); return r; }
```

- **Después de Firestore, nunca antes, nunca dentro de la transacción.** El usuario no espera a
  Postgres para saber que su tarea existe.
- **A mejor esfuerzo.** `quietly` atrapa, escribe `console.warn("[tasks] espejo pendiente de
  <id>")` y no relanza. La petición no falla por Postgres.
- `remirrorOne` relee la tarea (`findById`) y hace el upsert con el documento entero. Releer
  cuesta una lectura y evita espejar un `Partial`.
- **`withUpdatedAt`** garantiza `updatedAt: new Date()` en todo `update` que no lo traiga. Es
  lo que hace posible el job del §4 sin un flag en Firestore. La fase 0-bis revisa qué
  controladores ya lo mandan.
- El upsert es `INSERT … ON CONFLICT (task_id) DO UPDATE SET … , synced_at = NOW()`, todas
  las columnas menos la clave. **Nunca una lista escrita a mano a la que le falte una
  columna**: es el error que HAL-34 ya costó en `checklogs_raw`.
- `deleted(snapshot, at)` hace el mismo upsert con `deleted_at = at`.

## 4. Job `remirror`

En `services/tasks/src/jobs/remirror.ts`, arrancado desde `server.ts` con `setInterval`
como hace `inventory`: **cada 5 minutos, re-espeja las tareas con `updatedAt ≥ ahora − 15 min`**
de cada entidad con CheckBiz, con el mismo upsert idempotente. La ventana triplica el
intervalo para que un fallo transitorio de Postgres no deje nada atrás.

- Entidad a entidad, sin `collectionGroup`. La consulta `where("updatedAt", ">=", since)` sólo
  necesita el índice automático de campo único.
- Deja en el log cuántas re-espejó y cuántas fallaron. Si fallan en tres pasadas seguidas, es
  Postgres, no la tarea.
- **No hay flag `mirrored` en Firestore.** Inventario lo necesita porque su libro es
  append-only y se consulta por él; aquí la tarea ya se upserta y `updatedAt` basta. Un
  campo menos que escribir en cada cambio.

## 5. Backfill

`services/tasks/src/scripts/backfill-tasks.ts --entity <id> | --all [--since YYYY-MM-DD] [--apply]`.

- Simula por defecto: cuenta cuántas tareas espejaría por entidad y estado. Con `--apply`,
  upserta en lotes de 200 y escribe al final el recuento por estado en Firestore y en
  `tasks_raw` para la misma entidad. **Si no coinciden, lo dice y sale con error.**
- `--since` acota por `createdAt` para producción, donde la primera pasada puede ser grande.
  Para el histórico de ocho semanas basta `--since` ocho semanas antes del arranque; el
  Panel mensual agradecerá la pasada completa después.
- Se ejecuta dentro del contenedor, que ya tiene credenciales:

```bash
docker compose -f docker-compose.staging.yml -p encodebiz-api-dev exec -T tasks \
  node services/tasks/dist/scripts/backfill-tasks.js --entity <entityId> --apply
```

## 6. Lo que puede fallar y qué se ve

| Situación | Qué pasa | Dónde se ve |
|---|---|---|
| Postgres caído durante una escritura | La tarea existe; el espejo no. El job la recoge en ≤ 5 min | `console.warn` en `tasks`; `freshness.tasks.lastMirroredAt` se queda atrás |
| Un controlador escribe sin `updatedAt` | `withUpdatedAt` lo añade | Fase 0-bis, lista de controladores |
| Una tarea escrita fuera de `tasks` (el `tasksHandler` del SaaS) | No se espeja hasta el siguiente backfill | Fase 0-bis la descarta; si existe, se repunta el cliente |
| Borrado de tarea | Fila con `deleted_at`; sale de todas las consultas del hoy | Histórico intacto |
| Backfill con recuentos distintos | El script sale con error y no marca nada como completo | `dataHealth.tasksMirror = warming` |

## 7. Verificación (fase 1a)

En dev, por la API, con la entidad de pruebas: crear → asignar → iniciar → pausar → reanudar
→ completar → validar → borrar. Tras cada paso, `SELECT status, paused_at, deleted_at FROM
tasks_raw WHERE task_id = …` devuelve lo esperado en menos de 2 s. Parar Postgres, cambiar una
tarea, arrancarlo: el job la trae. Backfill: recuentos iguales. Caso QA **DAS-01**.

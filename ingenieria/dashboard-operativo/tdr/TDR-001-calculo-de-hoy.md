# TDR-001 — Cálculo del hoy: plan de lectura, estados, coste y tareas

**Fecha:** 2026-10-10
**Estado:** Diseño
**Componente:** `services/analytics/src/application/BuildOperationalDay.ts` + `@encodebiz/shared` (`buildWorkSessions`)
**Decisiones de referencia:** [ADR-001](../adr/ADR-001-postgres-es-la-fuente-del-ahora.md) · [ADR-002](../adr/ADR-002-el-dashboard-vive-en-analytics.md) · [ADR-005](../adr/ADR-005-el-retraso-se-calcula-contra-el-reloj.md)

---

## Resumen

Una función pura sobre Postgres:

```ts
buildOperationalDay(pool, {
  entityId: string;
  branchIds: string[] | null;   // null = todos los activos
  day?: string;                 // YYYY-MM-DD en la zona de cada centro; defecto: hoy en cada zona
  asOf: Date;                   // ahora, o el fin del día para el cierre
}): Promise<OperationalDayResult>
```

Devuelve, por centro, los tres bloques (`attendance`, `tasks`, `cost`) con totales y detalle.
`GET /panel/today` la llama con `asOf = new Date()` y agrega los totales de entidad. El cierre
diario ([TDR-003](./TDR-003-cierre-diario-y-semanas.md)) la llama por centro con
`asOf = fin del día + cola` y persiste.

**No trae reglas nuevas de jornada.** Reusa `buildWorkSessions` (promovida de
`attendanceSummary.ts`) y `ResolveEffectiveDayUseCase` sobre `PostgresCalendarRepository`.

## 1. Plan de lectura

Por entidad, en este orden, y **si cualquiera falla, falla la petición**:

| Paso | SQL (esquemático) | Notas |
|---|---|---|
| 1 | `SELECT branch_id, name, tz FROM dim_branches WHERE entity_id=$1 AND status IS DISTINCT FROM 'inactive'` | Zona de cada centro. Sin `tz`: la de la entidad en `dim_calendars`; sin ella, `UTC`, y se avisa en `dataHealth.calendars` |
| 2 | `SELECT employee_id, display_name, status, branch_ids FROM dim_employees WHERE entity_id=$1 AND status IN (…computables…)` | Plantilla y pares (empleado, centro) |
| 3 | `SELECT scope, scope_id, … FROM dim_calendars WHERE entity_id=$1` | Una consulta; `PostgresCalendarRepository` ya cachea por instancia. Se le precarga para no hacer una consulta por scope |
| 4 | `SELECT … FROM checklogs_raw WHERE entity_id=$1 AND timestamp >= $2 AND timestamp <= $3 ORDER BY employee_id, timestamp` | `$2` = inicio del día del centro más temprano **menos 16 h**; `$3` = `asOf`. Índice `idx_checklogs_entity_branch_ts` por `entity_id` + rango |
| 5 | `SELECT … FROM tasks_raw WHERE entity_id=$1 AND deleted_at IS NULL AND (due_at BETWEEN $2 AND $3 OR (status IN ('assigned','in_progress','completed') AND (due_at < $3 OR scheduled_start_at < $3 OR completed_at BETWEEN $2 AND $3)))` | Las de hoy y las que arrastran. Índices de [TDR-002](./TDR-002-espejo-de-tareas.md) |
| 5b | `SELECT m.*, i.unit_cost FROM item_movements_raw m JOIN dim_items i USING (item_id) WHERE m.entity_id=$1 AND m.type='consume' AND m.occurred_at BETWEEN $2 AND $3` | Sólo si devuelve filas viaja el bloque de material. **Confirmar el valor literal de `type`** para consumo en `services/inventory` (fase 2) |

Seis consultas como máximo, independientemente del número de centros y de personas. Los
nombres salen de los pasos 1 y 2; no hay lectura por persona ni por tarea.

Las ventanas se calculan **por centro** en su zona: `dayStart = 00:00 local`, `dayEnd = 24:00
local`. La consulta 4 usa la unión de todas las ventanas menos 16 h (una jornada que cruza la
medianoche empieza ayer); el reparto exacto por centro y día se hace en memoria.

## 2. Quién debería estar

Por cada par (empleado, centro) de la plantilla computable, `ResolveEffectiveDayUseCase(day)`
sobre `PostgresCalendarRepository` devuelve el día efectivo: si es laborable, sus turnos, si
está desactivado, si es festivo, si hay ausencia. La regla de quién entra y por qué no entra el
resto es **la de disponibilidad** ([TDR-001 §2–3](../../disponibilidad/tdr/TDR-001-calculo-de-disponibilidad.md)),
sin reimplementar: se reusa la misma clasificación (`noShift | holiday | absence | employeeStatus`).

- `expected` = los que tienen turno hoy en ese centro.
- `closedToday` = nadie trabaja y nadie debería (festivo del centro o día desactivado para
  todos), la regla de `closed` de disponibilidad.
- El sobreconteo multi-sucursal se hereda: quien está en dos centros se espera en los dos.

**Cuando no hay calendario espejado para un centro** (sync pendiente), el centro sale con
`expected = null`, `dataHealth.calendars = partial`, y sólo se publican los que fichan. Nunca
se asume «nadie previsto».

## 3. Quién está: jornadas sobre `checklogs_raw`

Cada fila de la consulta 4 se mapea a la forma mínima de `buildWorkSessions`:

| Forma mínima | Columna |
|---|---|
| `id` | `id` |
| `employeeId` / `branchId` | `employee_id` / `branch_id` |
| `type` / `status` | `type` / `status` |
| `timestamp` | `COALESCE(adjusted_timestamp, timestamp)` — la hora corregida manda, como en el panel |
| `checkin` | `checkin_ref` |
| `tz` | `COALESCE(metadata_raw->>'tz', etz, tz del centro)` — la misma prioridad que `getChecklogTimeZone` del front |

`buildWorkSessions` devuelve jornadas con estado, pausas, minutos e incidencias, exactamente
como hoy en «Asistencia». Lo que añade este TDR es el **mapeo a presencia** por persona y
centro, el de [02 §6](../02_to-be.md):

| Jornada del día en este centro | `presence` |
|---|---|
| Ninguna, y ninguna en otro centro hoy | `no_log` |
| Ninguna aquí, pero sí en otro centro suyo hoy | `other_branch` (con el otro centro) |
| `working` | `working` |
| `on_break` | `on_break` |
| `completed` | `finished` |
| con incidencia `pending_validation` | `pending_validation` |
| con incidencia `incomplete_workday` | `incomplete` |
| con `failed_log` únicamente | cuenta en `rejectedAttempts`; la persona sigue `no_log` |

- **La jornada pertenece al día de su checkin en su zona.** Una jornada abierta ayer que sigue
  abierta a `asOf` va a `openSinceYesterday`, no a `working` de hoy.
- Un `status = failed` es un intento que no ocurrió para la jornada, y un hecho para
  `rejectedAttempts`.
- `minutesFromShiftStart` = minutos entre el inicio del primer turno y `firstCheckinAt` (o
  `asOf` si no fichó). `toleranceMinutes` = la del `schedule_applied` del checkin o, sin
  fichaje, la que resuelve la cascada. `late` = `minutesFromShiftStart > toleranceMinutes`
  ([ADR-005](../adr/ADR-005-el-retraso-se-calcula-contra-el-reloj.md)).
- `workedMinutes` = minutos de la jornada hasta `asOf` para las abiertas, descontando las
  pausas cerradas y la abierta hasta `asOf`; con tope de **16 h** por jornada
  (`MAX_CYCLE_HOURS` de `BuildOperatingCost`): más que eso es un cierre olvidado.
- `unexpected` = jornadas de hoy en este centro de quien no estaba previsto aquí (sin turno,
  festivo, ausencia, o ni siquiera en la plantilla del centro). Se publican sin juicio.
- `alert = no_presence` si `expected > 0`, nadie `working`/`on_break`, y
  `asOf > inicio del primer turno + tolerancia`.

## 4. Las tareas de hoy

Sobre las filas de la consulta 5, todo contra `asOf` y en la zona del centro de la tarea:

| Señal | Regla |
|---|---|
| `due_today` | `due_at ∈ [dayStart, dayEnd)` |
| `in_progress` | `status = in_progress` y `paused_at IS NULL` |
| `paused` | `status = in_progress` y `paused_at IS NOT NULL` |
| `start_late` | `status = assigned` y `scheduled_start_at IS NOT NULL` y `scheduled_start_at < asOf` |
| `overdue` | `status ∈ {assigned, in_progress}` y `due_at < asOf` |
| `pending_validation` | `status = completed` |
| `completed_today` | `completed_at ∈ [dayStart, dayEnd)` (cualquier estado posterior) |

Una tarea puede llevar varias señales. `draft`, `cancelled`, `rejected` y `validated` no
generan señal salvo `completed_today` si aplica. Los asignados se resuelven contra
`dim_employees` del paso 2 (incluidos los no computables: una tarea puede estar asignada a
alguien de baja, y eso también es dato).

## 5. El coste

**Horas:** por jornada, `workedMinutes` del §3 × `employee_price / 60` del **checkin** de esa
jornada. Las jornadas `incomplete` **no suman** minutos ni coste —su salida la fabricó el
saneador— y se cuentan en `untrackedSessions` (añadido al implementar). Es la tarifa vigente cuando la persona entró, que es la que se le paga.
`rateCoverage` = jornadas con tarifa / jornadas. Por debajo de 0,8 el front marca «parcial».
El importe no lleva moneda ([README, decisiones abiertas](../README.md)).

**Material:** `SUM(quantity × unit_cost)` de la consulta 5b, por `branch_id` del movimiento o,
si viene nulo, por la sucursal de su `task_id` en `tasks_raw`. Sin filas, el bloque no viaja.

No se calcula coste planificado: la tarifa de quien no fichó no está en Postgres.

## 6. Agregación de entidad

`GET /panel/today` sin `branchId` suma los `counts` de los centros. **No** deduplica personas
entre centros (sobreconteo declarado). El tope de detalle de [03](../03_contratos-api.md) se
aplica aquí: por encima de 300 previstos, `people: null` por centro.

## 7. Frescura y salud

- `freshness.checklogs.lastSyncedAt` = `MAX(synced_at)` de `checklogs_raw` para la entidad en
  las últimas 48 h (si no hay, `null`).
- `freshness.reconcile` = última fila `reconcile` de `sync_log` para la entidad.
- `freshness.dimensions.syncedAt` = `MAX(synced_at)` de `dim_sync_log` con `status = success`
  para la entidad.
- `freshness.tasks.lastMirroredAt` = `MAX(synced_at)` de `tasks_raw` para la entidad.
- `dataHealth.tasksMirror` = `warming` si `tasks_raw` tiene menos filas que las que el backfill
  dejó anotadas para la entidad; `unavailable` si no hay ninguna.

## 8. Límites

- **Plantilla:** sin tope duro. Con 500 personas la consulta 4 trae los fichajes de un día
  (unos 1.500) y la cascada se resuelve 500 veces en memoria sobre un calendario cacheado:
  decenas de milisegundos. El tope de 300 es de **detalle en la respuesta**, no de cálculo.
- **Centros:** sin tope. La zona se resuelve por centro.
- **Tiempo objetivo:** < 300 ms para 200 personas y 20 centros, medido en dev antes de cerrar
  la fase 2. Si se supera, la primera palanca es cachear 30 s por `(entityId, branchId)`.

## 9. Pruebas

Unitarias sobre `buildOperationalDay` con fixtures de filas (no de Firestore): jornada que
cruza la medianoche; persona en dos centros que ficha en uno; `failed` seguido de `valid`;
`incomplete_workday`; tarea con `scheduled_start_at` pasado; tarea completada hoy; centro sin
calendario espejado; tolerancia 0; `asOf` antes del primer turno (sin alerta).

Y la de paridad de la fase 2a: las jornadas de `shared` coinciden con las del front.

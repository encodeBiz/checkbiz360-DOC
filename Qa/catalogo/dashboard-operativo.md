# Dashboard operativo — DAS

> **Verificación (2026-10-11):** escrito contra el código de `develop` (commits `cf05643`,
> `0a6c6c2`, `1eb7049`). El cálculo del día está verificado sin red
> (`services/analytics/src/scripts/verificar-dia-operativo.ts`, 23 casos) y contra la base de
> dev en local. La prueba `54-dashboard-operativo.spec.ts` **no se ha ejecutado todavía**:
> necesita las rutas desplegadas en staging.

Diseño: `DOCS/ingenieria/dashboard-operativo/`.

## GET /api/analytics/panel/today  ·  DAS-03
- Servicio: analytics — `panel.router.ts`, `application/operational/BuildPanelToday.ts`
- Consumidores: la portada del panel (pendiente)
- Autenticación: Firebase ID token · Autorización: `owner`/`admin` de la entidad
- Entrada: `entityId`, `branchId` opcional
- Respuesta: 200 `{ok, asOf, freshness, attendance, tasks, cost, dataHealth}`; 404 `branch_not_found`; 503 `source_unavailable`
- Efectos: ninguno (solo lectura de Postgres)
- Casos:
  - DAS-03-01 · PROP · un trabajador ficha → aparece `working` en su centro (previsto o inesperado)
  - DAS-03-02 · PROP · `people.length === counts.expected` en cada centro con calendario; `freshness.dimensions.syncedAt` presente
  - DAS-03-03 · ANON → 401 · PROP sobre `entidadAjenaId` → 403 · `branchId` inexistente → 404

## Espejo de tareas (`tasks_raw`)  ·  DAS-01
- Servicio: tasks — `MirroredTaskRepository`, job `remirror`, script `backfill-tasks`
- Casos:
  - DAS-01-01 · PROP crea una tarea con `scheduledStartAt` pasado → sale en `/panel/today` con señal `start_late`
  - DAS-01-02 · PROP la borra → deja de salir (fila con `deleted_at`)

## POST /api/analytics/reconcile/checklogs  ·  DAS-02
- Servicio: analytics — `ReconcileChecklogs.ts` · Autenticación: `x-encodebiz-key`
- Entrada: `entityId` opcional, `hours` (1–744, defecto 48), `dryRun`
- Casos:
  - DAS-02-01 · S2S · `dryRun=true` → 200, `pulled: 0`, `scanned > 0`

## POST /api/analytics/close-day  ·  DAS-06
- Servicio: analytics — `CloseOperationalDay.ts` · Autenticación: `x-encodebiz-key`
- Entrada: `entityId`, `date` (YYYY-MM-DD), `branchId` opcional
- Efectos: upsert en `operational_daily` con `source = manual`, sube `version`
- Casos:
  - DAS-06-01 · S2S · cerrar ayer → 200 con el centro y el día; rehacerlo sube `version`; `/panel/weeks` responde con las semanas pedidas

## GET /api/analytics/panel/weeks  ·  DAS-07
- Servicio: analytics — `BuildOperationalWeeks.ts` · Autenticación como `/today`
- Entrada: `entityId`, `branchId` opcional, `weeks` 1–26 (defecto 8)
- Casos:
  - DAS-07-01 · PROP · `weeks=0` y `weeks=27` → 400 `validation_error`

## Sin prueba automática todavía
- Cierre por planificador a las 04:xx locales y reintento a las 05:xx (depende de la hora).
- Conciliación real trayendo un fichaje perdido (exige borrar una fila del espejo).
- Cron de dimensiones al :20.

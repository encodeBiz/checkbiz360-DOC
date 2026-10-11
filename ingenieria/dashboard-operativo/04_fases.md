# 04 — Fases de implementación

El orden es de dependencias, no de calendario. API primero; el front, cuando el backend esté
verificado en dev. Cadena `develop → staging → main`. A `staging` sólo sube algo usable: como
pronto, fases 1 y 2 juntas.

Migraciones **a mano por SSH**, nunca desde el despliegue; en producción una a una mirando el
resultado. Los scripts que escriben simulan por defecto y actúan con `--apply`.

---

## Fase 0 — Estudio y documentación ✔

2026-10-10. Esta carpeta.

---

## Fase 0-bis — Comprobaciones del lunes por la mañana

Media mañana. Ninguna es código; todas cambian algo si salen mal.

1. **La Cloud Function `tasksHandler` no recibe tráfico en producción.** Mirar sus
   invocaciones en la consola de Firebase de `encodebiz-services` de los últimos 7 días. Si
   recibe, hay un cliente que no pasó el cutover y el espejo desde `tasks` tendría un agujero:
   se localiza y se repunta antes de la fase 1.
2. **Huecos del espejo de fichajes en producción.** Con un token real, contar fichajes de los
   últimos 7 días en Firestore (una entidad grande, `select()` de ids) y en `checklogs_raw`.
   La diferencia es el tamaño del problema que la conciliación va a tapar. Se anota aquí.
3. **`updatedAt` se escribe en todas las rutas de escritura de `tasks`.** El repositorio hace
   `set(..., {merge: true})` con lo que le pasan; si algún controlador no manda `updatedAt`,
   el repositorio espejado lo añade (TDR-002 §3). Lista de controladores revisados, aquí.
4. **Los fichajes de descanso llevan `checkin`.** `buildWorkSessions` ancla pausas por
   referencia o por orden temporal según lo que haga hoy `attendanceSummary.ts`; confirmar con
   una jornada real de dev qué trae `restin`/`restout`.
5. **Frescura de `dim_calendars` en producción.** `SELECT max(synced_at) FROM dim_sync_log`.
   Si es de julio, el backfill de la fase 3 y el hoy de la fase 2 arrancan con un sync completo.

**Entregable:** las cinco respuestas escritas en este documento, con fecha.

**Respuestas (2026-10-11):**

- 3 · `updatedAt`: pausar y reanudar ya lo escriben; `updateClosingPause` y algunos `update` no
  lo garantizan. Lo añade siempre `MirroredTaskRepository` (`withUpdatedAt`). Resuelto.
- 4 · Pausas con `checkin`: en dev, el 100 % de `restin`/`restout` de 30 días lleva
  `checkin_ref` (258 y 166). El agrupado por referencia vale. El tipo de consumo de material es
  `consumption`.
- 1, 2 y 5 · **Pendientes**: son de producción y el hook la bloquea. Se hacen en el pase.

---

## Fase 1 — Cimientos del espejo

Lo que hace que Postgres sea fiable como fuente del ahora. Va antes que cualquier pantalla.

### 1a. Espejo de tareas ([TDR-002](./tdr/TDR-002-espejo-de-tareas.md))

- Migración `026_tareas_espejo.sql`: `tasks_raw` e índices.
- `MirroredTaskRepository` en `services/tasks/src/infrastructure/`, que extiende
  `FirestoreTaskRepository` y espeja tras confirmar Firestore, a mejor esfuerzo.
- Job `remirror` en `tasks`: cada 5 min re-espeja lo tocado en los últimos 15.
- Script `services/tasks/src/scripts/backfill-tasks.ts --entity <id> | --all [--apply]`.
- `dataHealth.tasksMirror` lo alimenta `tasks_raw` (cuántas filas, última).

**Verificación:** en dev, crear, asignar, iniciar, pausar, reanudar, completar, validar y
borrar una tarea por la API; cada paso aparece en `tasks_raw` en menos de 2 s con el estado
correcto; el borrado deja `deleted_at`. Backfill de la entidad de pruebas: el recuento por
estado coincide con Firestore. Caso QA **DAS-01** en `54-dashboard-operativo.spec.ts`.

### 1b. Conciliación de fichajes ([TDR-004 §1](./tdr/TDR-004-endurecer-el-espejo.md))

- `POST /api/analytics/reconcile/checklogs` y planificador en `analytics` (no en `sync`: no
  tiene credenciales de Firebase): cada 30 min las últimas 2 h; a las 03:30 UTC las últimas 48 h.
- `sync_log` gana filas `reconcile` con `missing` y `pulled`.

**Verificación:** borrar a mano una fila de `checklogs_raw` en dev, lanzar la conciliación y
verla volver. Caso QA **DAS-02**.

### 1c. Cron de dimensiones ([TDR-004 §2](./tdr/TDR-004-endurecer-el-espejo.md))

- Planificador en `analytics` (`setInterval`, sin dependencia nueva): `SyncDimensions` cada
  hora al :20 para las entidades con actividad en los últimos 30 días.

**Verificación:** `dim_sync_log` muestra una fila por entidad y hora sin que nadie llame.
Caso QA **ANA-05-01** sigue valiendo para la llamada a mano.

**Entregable de la fase:** `tasks_raw` poblado y vivo en dev; conciliación y cron corriendo;
`04_fases.md` con las medidas de la fase 0-bis antes y después.

---

## Fase 2 — El hoy

### 2a. Lógica de jornada en `shared`

`buildWorkSessions` sale de `attendanceSummary.ts` del front a
`packages/shared/src/checkbiz/attendance/`, con sus pruebas, sobre la forma mínima de fichaje
([02 §8](./02_to-be.md)). El front pasa a importarla; **no cambia una línea de lo que pinta**.
Si Presencia ya la promovió, se usa la suya.

**Verificación:** para la entidad de pruebas y un rango de una semana, las jornadas que
devuelve `shared` coinciden una a una con las que pintaba el front antes del cambio (misma
`sessionKey`, mismo estado, mismos minutos).

### 2b. `buildOperationalDay` y `GET /panel/today` ([TDR-001](./tdr/TDR-001-calculo-de-hoy.md))

- `services/analytics/src/application/BuildOperationalDay.ts`: la función de los dos momentos.
- Ruta en `panel.router.ts` con el contrato de [03](./03_contratos-api.md).
- `freshness` y `dataHealth`.

**Verificación:** para la entidad `Wl8ZCvpdmIXzEE0mhT7W` en dev:

- `attendance.branches[*].expected` coincide uno a uno con `available` del desglose del día
  de disponibilidad para la misma fecha.
- Los estados de presencia coinciden con lo que pinta «Asistencia» para los mismos fichajes.
- Un fichaje nuevo aparece en `/today` en el siguiente sondeo.
- Una tarea con `scheduled_start_at` pasado y sin iniciar sale con `start_late`; una con
  `due_at` pasado y abierta, con `overdue`; la misma tarea completada deja de salir en ambas.
- Ninguna lectura falla en silencio: con Postgres parado la ruta devuelve `503`.
- Tiempo de respuesta < 300 ms con la entidad de pruebas.

Casos QA **DAS-03** (jornada), **DAS-04** (tareas), **DAS-05** (coste con y sin material).
Atención a la ventana 22:00–00:00 UTC: INF-02/03/05 ya caen solas por «hoy en Madrid vs UTC»;
los casos nuevos usan la zona del centro de la entidad de pruebas, no la del runner.

**Entregable de la fase:** `/today` verificado en dev; sube a `staging` junto con la fase 1.

---

## Fase 3 — El histórico

### 3a. `operational_daily` y cierre diario ([TDR-003](./tdr/TDR-003-cierre-diario-y-semanas.md))

- Migración `027_dashboard_operativo.sql`.
- Cron horario en `analytics`: cada centro se cierra a las **04:xx de su zona** para el día
  anterior, llamando a `buildOperationalDay` con `asOf = fin del día + cola`. Mismo patrón que
  `DailyReportCron` de `reports`.
- `POST /api/analytics/close-day` para rehacer un día.

### 3b. Backfill

- Script `services/analytics/src/scripts/cerrar-dias.ts --entity <id> --from --to [--apply]`,
  que cierra con `source: backfill`. Se lanza para las 8 semanas anteriores al arranque.

### 3c. `GET /panel/weeks`

**Verificación:**

- Cerrar «ayer» a mano para la entidad de pruebas y comparar la fila con lo que `/today`
  devolvía ayer a última hora (guardado en la QA): mismos totales.
- Una semana cerrada entera suma sus siete días; `coverage` = `withLog / expected` sobre las
  sumas.
- Corregir un fichaje de un día cerrado y rehacerlo con `close-day`: la fila cambia,
  `version` sube, `source` pasa a `manual`.
- Semanas de backfill salen con `source: backfill`.

Casos QA **DAS-06** (cierre), **DAS-07** (semanas).

---

## Fase 4 — La portada del panel ([05](./05_integracion-front.md))

- Bloque «Hoy» arriba: tres tiles con total y desglose por centro, rojo donde `alert`.
- «Ver más» por bloque: drawer con las listas que ya vienen en la respuesta.
- «Últimas 8 semanas» debajo: tres gráficas pequeñas y la tabla por centro.
- Sondeo cada 60 s con la pestaña visible; «actualizado hace…» desde `freshness`.
- Dos handlers en el proxy y sus variables en `.env.development` del portátil.

**Verificación:** en local contra `api-staging`, con la entidad de pruebas: lo que pinta la
portada coincide con la respuesta cruda; cambiar un fichaje desde la app lo mueve en un
minuto; sin CheckBiz contratado el bloque no se renderiza ni dispara la llamada.

---

## Fase 5 — Pase a producción

En el orden de siempre, y todo a mano:

1. Migraciones `026` y `027`, una a una.
2. Despliegue de la rama (`staging → main`).
3. `POST /dimensions/sync` completo; backfill de tareas (`--all --apply`); backfill de ocho
   semanas de cierres.
4. Variables nuevas en Vercel (`NEXT_BACKEND_URI_CHECKINBIZ_PANEL_TODAY`,
   `NEXT_BACKEND_URI_CHECKINBIZ_PANEL_WEEKS`) y despliegue del front.
5. Verificación con token real sobre una entidad grande: `/today` responde, los totales
   cuadran con «Asistencia», `freshness.reconcile.missing = 0` tras la primera conciliación.
6. Entrada en el registro de pases de `DOCS/deployment-prod/`.

---

## Qué queda fuera y dónde se recoge

- Coste planificado del día → cuando se espejen las responsabilidades (tarifa por puesto).
- Avisos push desde el dashboard → Presencia fase 3.
- Turno por día y sucursal → cuadrantes.
- Retirar `tasksHandler` del SaaS → tasks-service fase 4; con el espejo hecho, es el momento.

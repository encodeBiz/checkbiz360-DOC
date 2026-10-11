# 03 — Contratos de API

**Servicio:** `services/analytics`, router `panel` (front) y `analytics` (S2S).
**Vía el front:** `/api/proxy/checkinbiz_panel_today` y `/api/proxy/checkinbiz_panel_weeks` —
dos entradas nuevas en la allowlist del proxy (`methods: ['GET']`, `requiresAuth: true`) y una
variable por entorno cada una. Ver [05](./05_integracion-front.md).
**Auth (front):** `Authorization: Bearer <Firebase ID token>` + `requireEntityAccess`
(`owner` | `admin` sobre la entidad). El JWT de empleado de la app no se acepta.
**Auth (S2S):** `X-Encodebiz-Key`, sin CORS, nunca accesibles desde el navegador.

Las dos rutas del panel son de **sólo lectura** y no escriben nada. Siguen el estilo de
`overview`: `{ ok: true, ... }` en éxito y `{ ok: false, error, message? }` en error.

---

## `GET /api/analytics/panel/today` — el ahora

Cómo está la operativa en este instante, por centro y en total, con el detalle dentro.

### Query

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `entityId` | sí | Entidad |
| `branchId` | no | Baja a un centro. Trae siempre las listas completas de ese centro |

### `200`

```jsonc
{
  "ok": true,
  "asOf": "2026-10-13T06:32:11Z",
  "scope": { "entityId": "…", "branchId": null },

  // Lo que permite al front decir «actualizado hace…» sin inventar umbrales.
  "freshness": {
    "checklogs":  { "lastSyncedAt": "2026-10-13T06:31:40Z" },
    "reconcile":  { "lastRunAt": "2026-10-13T06:00:04Z", "missing": 0 },
    "dimensions": { "syncedAt": "2026-10-13T06:20:02Z" },
    "tasks":      { "lastMirroredAt": "2026-10-13T06:29:55Z" }
  },

  "attendance": {
    "totals": {
      "expected": 42, "working": 30, "onBreak": 3, "finished": 2,
      "noLog": 7, "late": 4, "otherBranch": 1, "incomplete": 0,
      "pendingValidation": 0, "unexpected": 2, "rejectedAttempts": 3,
      "openSinceYesterday": 1
    },
    "branches": [
      {
        "branchId": "bcn-norte", "branchName": "Obra Norte", "timezone": "Europe/Madrid",
        "closedToday": false,                       // nadie debía trabajar (festivo / fin de semana)
        "counts": { "expected": 10, "working": 4, "onBreak": 1, "finished": 0, "noLog": 4, "late": 2,
                    "otherBranch": 1, "incomplete": 0, "pendingValidation": 0, "unexpected": 0,
                    "rejectedAttempts": 1, "openSinceYesterday": 0 },
        "alert": "no_presence" | "none",            // previstos > 0, nadie dentro y ya pasó el primer turno + tolerancia
        "people": [
          {
            "employeeId": "emp_123", "fullName": "Ana Ferrer",
            "shifts": [{ "start": { "hour": 8, "minute": 0 }, "end": { "hour": 16, "minute": 0 } }],
            "presence": "working",
            "firstCheckinAt": "2026-10-13T06:04:00Z", "lastMovementAt": "2026-10-13T06:04:00Z", "lastMovementType": "checkin",
            "minutesFromShiftStart": 4, "toleranceMinutes": 10, "late": false,
            "workedMinutes": 28, "incidents": []
          },
          {
            "employeeId": "emp_456", "fullName": "Luis Ruiz",
            "shifts": [{ "start": { "hour": 8, "minute": 0 }, "end": { "hour": 16, "minute": 0 } }],
            "presence": "no_log",
            "minutesFromShiftStart": 32, "toleranceMinutes": 10, "late": true
          },
          {
            "employeeId": "emp_789", "fullName": "Pablo Mora",
            "shifts": [ … ], "presence": "other_branch",
            "otherBranch": { "id": "bcn-sur", "name": "Obra Sur" }, "firstCheckinAt": "2026-10-13T05:58:00Z"
          }
        ],
        "unexpected": [                             // fichó hoy aquí sin estar previsto. Se enseña, no se juzga
          { "employeeId": "emp_900", "fullName": "Marta Cano", "presence": "working", "firstCheckinAt": "…", "workedMinutes": 40 }
        ],
        "openSinceYesterday": [                     // jornada de ayer sin cerrar: ni se cuenta hoy ni se juzga
          { "employeeId": "emp_321", "fullName": "Nadia Sáez", "firstCheckinAt": "2026-10-12T13:02:00Z" }
        ]
      }
    ]
  },

  "tasks": {
    "totals": { "dueToday": 12, "inProgress": 5, "paused": 1, "startLate": 2, "overdueOpen": 3,
                "pendingValidation": 4, "completedToday": 6 },
    "branches": [
      {
        "branchId": "bcn-norte", "branchName": "Obra Norte",
        "counts": { "dueToday": 4, "inProgress": 2, "paused": 0, "startLate": 1, "overdueOpen": 1, "pendingValidation": 1, "completedToday": 2 },
        "items": [
          {
            "taskId": "t_1", "title": "Montaje andamio", "status": "assigned", "priority": "high",
            "scheduledStartAt": "2026-10-13T06:00:00Z", "dueAt": "2026-10-13T14:00:00Z",
            "assignees": [{ "employeeId": "emp_123", "fullName": "Ana Ferrer" }],
            "signals": ["start_late", "due_today"]   // cero o varias; calculadas contra `asOf`
          }
        ]
      }
    ]
  },

  "cost": {
    "totals": { "workedMinutes": 5400, "untrackedSessions": 2, "laborCost": 1234.5, "rateCoverage": 0.98,
                "materialCost": 85.2, "materialMovements": 4 },
    "branches": [
      { "branchId": "bcn-norte", "branchName": "Obra Norte",
        "workedMinutes": 1230, "laborCost": 312.4, "rateCoverage": 1,
        "materialCost": 85.2, "materialMovements": 4 }
    ]
  },

  "dataHealth": {
    "tasksMirror":   { "status": "ready" | "warming" | "unavailable", "note": "backfill_pending" },
    "costCoverage":  { "status": "ready" | "partial", "covered": 41, "total": 42 },
    "calendars":     { "status": "ready" | "partial", "have": 20, "need": 20, "unit": "branches" }
  }
}
```

### Reglas del contrato

- `attendance.totals.expected` = suma de `expected` de los centros. Con el sobreconteo conocido:
  quien pertenece a dos centros cuenta en los dos hasta que exista turno por día y sucursal.
- `people` trae **a toda la plantilla prevista del centro**, en este orden: `no_log` primero
  (los `late` antes), después `working`/`on_break`, después `finished`, `incomplete`,
  `pending_validation`, `other_branch`. El front no reordena por defecto.
- `late` sólo puede ser `true` con turno conocido: `minutesFromShiftStart > toleranceMinutes`.
  `toleranceMinutes` sale del turno aplicado del fichaje, o de la cascada del calendario para
  quien no fichó. Para `finished` y `incomplete` se evalúa igual contra `firstCheckinAt`.
- `alert: "no_presence"` sólo cuando `expected > 0`, nadie está `working`/`on_break`, y ya
  pasó el inicio del primer turno más su tolerancia. Antes de esa hora no hay alerta: no se
  acusa a un centro de vacío a las 7:00 si abre a las 8:00.
- `rejectedAttempts` son fichajes con `status = failed` de hoy en ese centro: intentos que el
  sistema rechazó. Se publican como hecho, nunca como fraude.
- `unexpected` y `openSinceYesterday` **no** entran en `expected` ni en ninguna tasa.
- **Tope de detalle.** A nivel entidad, las listas (`people`, `unexpected`, `items`) viajan
  completas mientras `attendance.totals.expected ≤ 300`. Por encima, cada centro trae
  `people: null` y `detail: "by_branch"`, y el front pide `&branchId=` al abrir el «ver más».
  Es la misma idea que `headcount_too_large` en disponibilidad: no se pagina una suma; se acota.
- Instantes en ISO UTC; `shifts` estructurados; el front los pinta en `timezone` del centro.
- `cost.*.untrackedSessions` cuenta las jornadas «sin cerrar»: no suman minutos ni coste, porque
  su salida la fabricó el saneador.
- `cost.*.laborCost` es un número sin moneda. `rateCoverage` es la fracción de jornadas con
  tarifa; por debajo de 0,8 el front marca el importe como parcial (mismo umbral que
  `BuildOperatingCost`).
- `cost.*.materialCost` sólo aparece si la entidad tiene movimientos de consumo en el día;
  si no, el bloque de material **no viaja** (`materialCost` ausente, no `0`).

### Errores

| HTTP | `error` | Cuándo |
|---|---|---|
| `400` | `validation_error` | Falta `entityId` |
| `401` | `unauthenticated` | Sin token válido |
| `403` | `forbidden` | El usuario no es `owner`/`admin` de la entidad |
| `404` | `branch_not_found` | `branchId` no es de la entidad |
| `503` | `source_unavailable` | Una de las lecturas de Postgres falló. **No hay respuesta parcial** |

---

## `GET /api/analytics/panel/weeks` — las últimas semanas

Los mismos números del hoy, cerrados por día y sumados por semana.

### Query

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `entityId` | sí | Entidad |
| `branchId` | no | Baja a un centro |
| `weeks` | no | Semanas completas hacia atrás. Defecto 8, máximo 26 |

### `200`

```jsonc
{
  "ok": true,
  "scope": { "entityId": "…", "branchId": null },
  "range": { "from": "2026-08-10", "to": "2026-10-05", "weeks": 8, "weekStartsOn": "monday" },

  // La semana en curso: sólo días ya cerrados. El hoy va en /today.
  "current": { "week": "2026-10-06", "days": 7, "closedDays": 4, "inProgress": true, "attendance": { … }, "tasks": { … }, "cost": { … }, "source": "close" },

  "weeks": [
    {
      "week": "2026-09-29", "days": 7, "closedDays": 7, "workingDays": 5,
      "attendance": {
        "expected": 290, "withLog": 260, "noLog": 30, "late": 22, "incomplete": 5, "otherBranch": 3,
        "coverage": 0.8966,          // withLog / expected
        "lateRate": 0.0846,          // late / withLog
        "lateMinutes": 410
      },
      "tasks": {
        "due": 60, "completed": 53, "completedOnTime": 44, "completedLate": 9,
        "overdueAtClose": 7, "startLate": 5, "validated": 40, "rejected": 2,
        "onTimeRate": 0.8302         // completedOnTime / completed
      },
      "cost": {
        "workedMinutes": 120000, "laborCost": 20400, "rateCoverage": 0.97,
        "materialCost": 310.5, "materialMovements": 18
      },
      "source": "close" | "backfill" | "mixed"
    }
  ],

  // Sólo a nivel entidad: una fila compacta por centro para pintar el ranking semanal.
  "branches": [
    { "branchId": "bcn-norte", "branchName": "Obra Norte",
      "weeks": [ { "week": "2026-09-29", "coverage": 0.91, "lateRate": 0.05, "onTimeRate": 0.9, "laborCost": 3100, "source": "close" } ] }
  ],

  "dataHealth": {
    "history": { "status": "ready" | "warming", "have": 23, "need": 56, "unit": "days", "note": "backfill_only_until_2026-10-14" }
  }
}
```

### Reglas del contrato

- Semana ISO, de lunes a domingo, en la zona del centro. A nivel entidad, cada centro aporta
  sus días en su zona; una semana «de entidad» es la suma de las semanas de sus centros.
- **Las tasas se recalculan sobre las sumas**, nunca se promedian tasas de días o de centros.
- `closedDays` cuenta días con fila en `operational_daily`. Una semana con `closedDays < days`
  se pinta como incompleta; no se extrapola.
- `source: backfill` marca semanas reconstruidas con el calendario actual
  ([ADR-004](./adr/ADR-004-el-historico-se-congela-al-cerrar-el-dia.md)). `mixed` cuando
  conviven días cerrados y reconstruidos.
- Días con `closedDay = true` (nadie debía trabajar) **no** cuentan en `expected` ni en
  `workingDays`, pero sí suman sus tareas y su coste si los hubo.

### Errores

Los de `/today`, más `400 validation_error` si `weeks` no es un entero entre 1 y 26.

---

## Rutas S2S (`X-Encodebiz-Key`)

### `POST /api/analytics/close-day?entityId=…&date=YYYY-MM-DD[&branchId=…]`

Calcula y guarda el cierre de un día. Idempotente: pisa la fila con `source: manual` y sube
`version`. Lo usa el cron internamente (con `source: close`), el script de backfill (con
`source: backfill`) y quien tenga que rehacer un día después de corregir un fichaje.

Respuesta: `{ ok: true, closed: [{ branchId, day, source, version }], failed: [] }`.

### `POST /api/analytics/dimensions/sync[?entityId=…]`

Ya existe. El cron lo llama por dentro, no por HTTP. Sigue disponible a mano.

### `POST /api/analytics/reconcile/checklogs?entityId=…&hours=48[&dryRun=true]`

Compara los ids de `checklogs` de Firestore de las últimas `hours` horas con `checklogs_raw` y
trae los que faltan. Con `dryRun=true` sólo cuenta. Respuesta:
`{ ok, dryRun, hours, entities, missing, pulled, failed, results[] }`, con `scanned` y `skipped`
por entidad. Sin `entityId`, todas las entidades con actividad en 30 días. `hours` entre 1 y
744. Deja fila en `sync_log` con `source = 'reconcile'` (no en `dryRun`). Detalle en [TDR-004](./tdr/TDR-004-endurecer-el-espejo.md).

---

## Notas de contrato

**Sin paginación.** Una suma no se pagina. El tamaño se acota por día y por tope de detalle.

**Claves estables, texto en el front.** `presence`, `signals`, `alert`, `source`, `status`
son claves; el idioma lo pone el panel.

**Compatibilidad.** `overview` y `stats` no cambian. `today` y `weeks` son rutas nuevas bajo la
misma puerta.

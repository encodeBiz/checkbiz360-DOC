# TDR-006 — Disponibilidad de la semana y alertas del dashboard

**Fecha:** 2026-10-12
**Estado:** Diseño
**Componente:** `services/analytics` — `application/alerts/*`, `application/availability/BuildAvailabilityWeek.ts`, rutas `/panel/availability-week` y `/panel/alerts`
**Decisión de referencia:** [ADR-007](../adr/ADR-007-alertas-que-se-leen.md)

---

## 1. Disponibilidad de la semana — `GET /panel/availability-week?entityId`

Los próximos 7 días (hoy incluido) por centro, con el MISMO caso de uso que la pestaña de
disponibilidad (`ResolveAvailabilityUseCase`) sobre `PostgresAvailabilityRepository`. No copia la
pantalla: por centro, plantilla, disponibles por día, días cerrados y el peor día laborable.

```jsonc
{ "ok": true, "from": "2026-10-12", "to": "2026-10-18",
  "branches": [ { "branchId": "…", "branchName": "Obra Norte", "total": 10,
      "days": [ { "date": "2026-10-12", "available": 8, "closed": false, "rate": 0.8 } ],
      "worst": { "date": "2026-10-15", "available": 3, "rate": 0.3 } } ] }
```

El front pinta una fila por centro con siete celdas de color y el peor día; «ver más» abre
`/checkinbiz/calendar?tab=availability`.

## 2. Alertas — `GET /panel/alerts?entityId`

Se calculan al pedirlas sobre lo que ya calcula la portada: el día (`buildOperationalDay`), la
disponibilidad de la semana, las semanas cerradas (`operational_daily`), los costes estimados y
la plantilla (`employee_status_events`).

```jsonc
{ "ok": true, "alerts": [
  { "id": "availability_low:bcn-norte", "rule": "availability_low", "severity": "high",
    "scope": { "branchId": "bcn-norte", "branchName": "Obra Norte" },
    "params": { "date": "2026-10-15", "available": 3, "total": 10, "rate": 0.3, "days": 2 },
    "target": "availability" } ] }
```

El texto lo pone el front con la clave `rule` y los `params`.

### Catálogo y umbrales

| Regla | Salta cuando | Mínimo absoluto | Gravedad | Destino |
|---|---|---|---|---|
| `availability_low` | Un día laborable de los próximos 7 con disponibles/plantilla < 35 % | plantilla ≥ 3 y faltan ≥ 3 | high si < 20 %, si no medium | disponibilidad |
| `no_presence` | Centro con previstos y nadie dentro pasada la hora más el margen | previstos ≥ 2 | high | asistencia |
| `attendance_low` | Hoy, pasado el primer turno + margen, han fichado < 50 % de los previstos | previstos ≥ 4 y sin fichar ≥ 3 | high si < 25 %, si no medium | asistencia |
| `late_high` | Hoy, con retraso > 30 % de los que han fichado | retrasos ≥ 3 | medium | asistencia |
| `week_coverage_low` | La última semana cerrada fichó < 50 % de los previstos | previstos ≥ 10 en la semana | medium | panel |
| `tasks_overdue` | Tareas vencidas sin cerrar en un centro | ≥ 5 | medium (high si ≥ 15) | tareas |
| `tasks_start_late` | Tareas sin empezar a su hora hoy | ≥ 3 | medium | tareas |
| `untracked_high` | Ayer, jornadas «sin cerrar» > 20 % de las jornadas | ≥ 3 | medium | asistencia |
| `cost_rising` | Coste diario del mes > 25 % sobre el del mes anterior | ≥ 5 días cerrados en cada mes | medium | panel |
| `rate_missing` | Horas del mes sin tarifa > 20 % | ≥ 20 h | medium | empleados |
| `exits_high` | Bajas del mes > 10 % de los activos | ≥ 3 bajas | medium | plantilla (portada) |

Una alerta por regla y ámbito. Máximo 8 en la respuesta, `high` primero y, dentro, por tamaño.

## 3. Verificación

Casos sin red (`scripts/verificar-alertas.ts`): cada regla salta con el doble umbral y no salta
con solo uno de los dos; 2 de 20 sin fichar no salta; el tope de 8 y el orden.

# 03 — Contratos de API

**Handler:** `apiV100-firebaseEntryHttp-checkinbiz-calendarHandler`
**Vía el front:** `/api/proxy/checkinbiz_calendar_handler` — el proxy de Next reenvía la query
string tal cual y pone el token. No hace falta registrar nada nuevo en la allowlist.
**Auth:** `Authorization: Bearer <Firebase ID token>`. Sólo back office; el staff JWT de la app
**no** se acepta en estas dos acciones.
**Permisos:** por nivel de responsabilidad del actor — `owner`/`manager` ven toda la entidad,
`supervisor` sólo sus sucursales, `worker` recibe `403`.

Ambas acciones son de **solo lectura** y no escriben nada.

> El desglose del día también da de alta y borra ausencias
> ([ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md)), pero **no añade contrato**:
> reusa `PATCH` (`upsertCalendar`) y `DELETE` (`deleteCalendarItem`) del mismo handler, ya
> existentes. Lo único que el backend tiene que aceptar de nuevo es el campo `paid` dentro de
> `holiday`, del [ADR-004](./adr/ADR-004-ausencias-retribuidas.md).

---

## `GET ?action=availability` — rejilla de cobertura

Cuánta gente hay disponible cada día, agrupada por sucursal.

### Query

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `action` | sí | `availability` |
| `entityId` | sí | Entidad |
| `from` | sí | `YYYY-MM-DD`, inclusive |
| `to` | sí | `YYYY-MM-DD`, inclusive. Máximo 62 días desde `from` |
| `branchId` | no | Limita el cálculo a una sucursal. Obligatorio por encima del tope de plantilla |
| `includeUnassigned` | no | `true` por defecto. Incluye el grupo de quien no tiene sucursal |

### `200` — `calendar/availability_resolved`

```json
{
  "code": "calendar/availability_resolved",
  "data": {
    "range": { "from": "2026-09-01", "to": "2026-09-30", "timezone": "Europe/Madrid" },
    "headcount": 200,
    "groups": [
      { "id": "bcn-norte", "kind": "branch", "name": "Sucursal Norte", "total": 48 },
      { "id": "__unassigned__", "kind": "unassigned", "name": null, "total": 6 }
    ],
    "rows": [
      {
        "groupId": "bcn-norte",
        "total": 48,
        "cells": [
          { "date": "2026-09-01", "available": 43, "closed": false },
          { "date": "2026-09-05", "available": 0,  "closed": true }
        ]
      }
    ]
  }
}
```

- `cells` trae **un elemento por día del rango**, en orden, sin huecos.
- `total` es la plantilla computable del grupo, y es el denominador de todas sus celdas.
- `closed` significa *nadie trabaja y nadie debería* —fin de semana o festivo—, y es distinto
  de `available: 0` con `closed: false`, que es un agujero de cobertura. La regla exacta, en el
  [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) §3.
- `headcount` es la plantilla computable de **toda la entidad**, no la suma de los grupos: quien
  pertenece a varias sucursales cuenta en cada una de ellas, así que la suma de `total` puede
  ser mayor.

### Errores

| Código HTTP | `code` | Cuándo |
|---|---|---|
| `400` | `calendar/missing_params` | Falta `entityId`, `from` o `to` |
| `400` | `calendar/invalid_range` | `to` anterior a `from`, o fechas mal formadas |
| `400` | `calendar/range_too_long` | Más de 62 días. Devuelve `{ days, limit }` |
| `400` | `calendar/headcount_too_large` | Plantilla por encima del tope sin `branchId`. Devuelve `{ headcount, limit }` para que el front pida elegir sucursal |
| `403` | `calendar/forbidden` | Nivel insuficiente, o `branchId` fuera del alcance del actor |
| `404` | `calendar/entity_not_found` | La entidad no existe |

**Nunca se devuelve una rejilla parcial.** Si una lectura falla, la respuesta es un error: un
número de cobertura incompleto es peor que ninguno.

---

## `GET ?action=availabilityDay` — desglose de un día

Quién está disponible ese día en ese grupo, y por qué no lo está el resto.

### Query

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `action` | sí | `availabilityDay` |
| `entityId` | sí | Entidad |
| `date` | sí | `YYYY-MM-DD` |
| `groupId` | sí | Id de sucursal, o `__unassigned__` |

### `200` — `calendar/availability_day_resolved`

```json
{
  "code": "calendar/availability_day_resolved",
  "data": {
    "date": "2026-09-08",
    "group": { "id": "bcn-norte", "kind": "branch", "name": "Sucursal Norte", "total": 48 },
    "closed": false,
    "available": [
      {
        "employeeId": "emp_123",
        "fullName": "Ana Ferrer",
        "shifts": [{ "start": { "hour": 9, "minute": 0 }, "end": { "hour": 17, "minute": 0 } }]
      }
    ],
    "unavailable": [
      { "employeeId": "emp_456", "fullName": "Luis Ruiz",  "reason": "holiday",        "reasonName": "Diada",     "reasonSource": "branch" },
      { "employeeId": "emp_789", "fullName": "Marta Cano", "reason": "absence",        "reasonName": "Vacaciones", "reasonSource": "employee", "absenceId": "vacaciones-2026-09-08", "paid": true },
      { "employeeId": "emp_012", "fullName": "Pablo Mora", "reason": "employeeStatus", "reasonName": "sick_leave" },
      { "employeeId": "emp_345", "fullName": "Nadia Sáez", "reason": "noShift" }
    ]
  }
}
```

- `available.length + unavailable.length === group.total`.
- `shifts` va estructurado, no formateado: el formato de hora depende del locale y es del
  cliente.
- `reason` ∈ `noShift | holiday | absence | employeeStatus`. Precedencia y significado en el
  [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) §2.
- `reasonName` es el nombre que escribió quien creó el festivo o la ausencia; para
  `employeeStatus` es la **clave** del estado (`vacation`, `sick_leave`, …), que el cliente
  traduce. Ausente para `noShift`.
- `reasonSource` ∈ `entity | branch | employee`, sólo para `holiday` y `absence`.
- `absenceId` y `paid` van **sólo** cuando `reason` es `absence` con `reasonSource: employee`:
  son lo que necesita el panel para poder borrarla y para decir si se cobra. `paid` ausente
  significa *no consta*, que no es lo mismo que `false` — ver
  [ADR-004](./adr/ADR-004-ausencias-retribuidas.md).

### Errores

Los mismos que la rejilla, más:

| Código HTTP | `code` | Cuándo |
|---|---|---|
| `404` | `calendar/group_not_found` | El `groupId` no es una sucursal de la entidad |

---

## Notas de contrato

**Sin paginación.** Una suma no se pagina: para contar hay que mirarlo todo. El tamaño se acota
por rango (62 días) y por plantilla (`headcount_too_large` obliga a elegir sucursal), no
troceando la respuesta.

**Idempotente y cacheable.** Ambas acciones son puras respecto al estado del calendario.
Cuando se materialice la rejilla (Fase 4) el contrato no cambia; sólo de dónde sale el número.

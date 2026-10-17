# 03 — Contratos de API

**Servicio:** `services/checkinbiz` (contenedor), router `calendar`
**Rutas:** `GET /api/v1/checkinbiz/calendar/availability` y `.../availability/day`
**Vía el front:** `/api/proxy/checkinbiz_calendar_availability[/day]` — requiere **entrada nueva
en la allowlist** del proxy (`methods: ['GET']`, `subPathPattern` limitado a la raíz y `/day`) y
una variable de entorno por entorno. No basta con reusar `checkinbiz_calendar_handler`: ese
apunta a la Cloud Function.
**Auth:** `Authorization: Bearer <Firebase ID token>`. El staff JWT de la app **no** se acepta.
**Permisos:** `owner`/`manager` ven toda la entidad, `supervisor` sólo sus sucursales, `worker`
recibe `403`.

Ambas rutas son de **solo lectura** y no escriben nada.

> El desglose del día también da de alta y borra ausencias
> ([ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md)), pero **no añade contrato
> aquí**: reusa las escrituras de calendario que ya existen. Lo único nuevo que el backend tiene
> que aceptar es `paid` dentro de `holiday`
> ([ADR-004](./adr/ADR-004-ausencias-retribuidas.md)). Esas escrituras viven hoy en la Cloud
> Function y se portan al contenedor en la Fase 4.

---

## `GET /availability` — rejilla de cobertura

Cuánta gente hay disponible cada día, agrupada por sucursal.

### Query

| Parámetro | Obligatorio | Descripción |
|---|---|---|
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
    ],
    "warnings": { "discardedHolidays": 0 }
  }
}
```

- `cells` trae **un elemento por día del rango**, en orden, sin huecos.
- `total` es la plantilla computable del grupo, y es el denominador de todas sus celdas.
- `closed` significa *nadie trabaja y nadie debería* —fin de semana o festivo del grupo—, y es
  distinto de `available: 0` con `closed: false`, que es un agujero de cobertura. La regla exacta,
  en el [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) §3.
- `headcount` es la plantilla computable de **toda la entidad**, no la suma de los grupos: quien
  pertenece a varias sucursales cuenta en cada una, así que la suma de `total` puede ser mayor.
  Es un sobreconteo conocido — TDR §2.2.
- `warnings.discardedHolidays` cuenta los festivos con fecha ilegible que se descartaron. Va en
  la respuesta y no sólo en un log: descartar en silencio y devolver un número entero es el mismo
  fallo que este diseño rechaza, sólo que más pequeño.

### Errores

| HTTP | `code` | Cuándo |
|---|---|---|
| `400` | `calendar/missing_params` | Falta `entityId`, `from` o `to` |
| `400` | `calendar/invalid_range` | `to` anterior a `from`, o fechas mal formadas |
| `400` | `calendar/range_too_long` | Más de 62 días. Devuelve `{ days, limit }` |
| `400` | `calendar/headcount_too_large` | Plantilla por encima del tope sin `branchId`. Devuelve `{ headcount, limit }` |
| `403` | `calendar/forbidden` | Nivel insuficiente, o `branchId` fuera del alcance del actor |
| `404` | `calendar/entity_not_found` | La entidad no existe |

**Nunca se devuelve una rejilla parcial.** Si una lectura falla, la respuesta es un error: un
número de cobertura incompleto es peor que ninguno.

---

### `format=xlsx` — la rejilla en Excel (2026-10-17)

Con `format=xlsx` (y `lang`, `groupId` opcional) la misma ruta devuelve el fichero generado en el
servidor, en `data`: `{ filename, mimeType, base64 }`. Dos hojas: la rejilla como se ve —equipos en
filas, días en columnas, coloreada con los umbrales del panel (70 % y 55 %)— y el detalle día a
día. «Sin …» usa la etiqueta de sucursal de la empresa (`config.labels.branch.singular`). Idiomas
`es`, `en` y `pt`; cualquier otro, en inglés. Los errores son los de la rejilla.

Jose, 2026-10-17: «reportes e informes salen de backend». Sustituye al CSV que montaba el panel.

---

## `GET /availability/day` — desglose de un día

Quién está disponible ese día en ese grupo, y por qué no lo está el resto.

### Query

| Parámetro | Obligatorio | Descripción |
|---|---|---|
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
      { "employeeId": "emp_456", "fullName": "Luis Ruiz",  "reason": "holiday",        "reasonName": "Diada",      "reasonSource": "branch" },
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
- `reason` ∈ `noShift | holiday | absence | employeeStatus`. Significado y orden en el
  [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) §3.
- `reasonName` es el nombre que escribió quien creó el festivo o la ausencia; para
  `employeeStatus` es la **clave** del estado (`vacation`, `sick_leave`, …), que el cliente
  traduce. Ausente para `noShift`.
- `reasonSource` ∈ `entity | branch | employee`, sólo para `holiday` y `absence`. Sale del
  `source` que la **TAREA 2** añade a los festivos resueltos; hoy el resolutor lo tira, y sin
  él este campo no se puede rellenar.
- `absenceId` y `paid` van **sólo** cuando `reason` es `absence` con `reasonSource: employee`:
  son lo que necesita el panel para poder borrarla y para decir si se cobra. `paid` ausente
  significa *no consta*, que no es lo mismo que `false` — ver
  [ADR-004](./adr/ADR-004-ausencias-retribuidas.md).

### Por qué el motivo se queda

Se valoró retirarlo y dejar dos listas de nombres: el tablero diría *si* alguien está
disponible y no *por qué* no lo está. Habría simplificado el cálculo, el contrato y las
pruebas.

**No se puede**, porque el desglose no es solo lectura: da de alta y borra ausencias
([ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md)). Y una superficie de
escritura tiene que saber qué puede escribir — qué fila es reversible sale de
`reason: absence` con `reasonSource: employee`, el borrado necesita `absenceId`, y los tres
motivos irreversibles necesitan `reason` y `reasonName` para explicar por qué la flecha está
apagada.

El coste real es menor de lo que parecía: con el `source` dentro —que hace falta igual para
`closed`— el reparto entre motivo colectivo y personal ya está hecho, y nombrar cuál es apenas
un paso más.

### Errores

Los mismos que la rejilla, más:

| HTTP | `code` | Cuándo |
|---|---|---|
| `404` | `calendar/group_not_found` | El `groupId` no es una sucursal de la entidad |

---

## Notas de contrato

**Sin paginación.** Una suma no se pagina: para contar hay que mirarlo todo. El tamaño se acota
por rango (62 días) y por plantilla (`headcount_too_large`), no troceando la respuesta.

**Idempotente y cacheable.** Ambas rutas son puras respecto al estado del calendario. Cuando
entre el snapshot de [ADR-005](./adr/ADR-005-snapshot-del-calendario-resuelto-en-postgres.md) el
contrato no cambia; sólo de dónde sale el número.

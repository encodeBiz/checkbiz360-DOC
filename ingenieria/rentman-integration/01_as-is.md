# 01 — La API de Rentman (as-is, verificado)

> **Fuente:** exploración real contra la cuenta del cliente (token OpenAPI, cuenta `encodebiz`) el 2026-07-26.
> **Qué cubre:** cómo es de verdad la API, no cómo la suponíamos. Corrige los supuestos del esqueleto.

---

## 1. Autenticación

- Base URL: `https://api.rentman.net`.
- **Bearer token personal** (JWT). Se genera en Rentman → **Configuration → Account
  → Integrations**. Validez ~10 años (`client_type: openapi`).
- El token identifica cuenta + un `medewerker` (crew member) creador.
- **Almacenamiento:** cifrado por tenant (AES-256-GCM) en Firestore
  `entities/{entityId}/integrations/rentman`. Nunca en claro, nunca en el repo.

## 2. Forma de las respuestas

Listas: `{ "data": [...], "itemCount": N, "limit": L, "offset": O }`.
Detalle por id: `{ "data": { ... }, "itemCount": 1 }`.
Paginación: parámetros `limit` / `offset`.

### ⚠️ Dos correcciones clave sobre los supuestos iniciales

1. **Las referencias son rutas string, no IDs numéricos.**
   Ej.: `"crewmember": "/crew/226"`, `"function": "/projectfunctions/8"`,
   `"time_registration": "/timeregistration/20"`. Al escribir hay que mandar la ruta.
2. **La duración va en segundos.** `duration: 18000` = 5 h.

## 3. Objetos relevantes

### `timeregistration` — **esto es el fichaje**
Leído por id (`GET /timeregistration/20`):
```json
{
  "id": 20, "crewmember": "/crew/226",
  "start": "2026-07-14T14:00:00+02:00", "end": "2026-07-14T19:00:00+02:00",
  "duration": 18000, "break_duration": 0, "travel_time": 0,
  "leavetype": "/leavetypes/1", "status": "approved"
}
```
Es el registro horario: empleado + inicio + fin + descanso + estado. **Mapea 1:1 con
nuestra jornada** (checkin→`start`, checkout→`end`). Es el destino natural del push de horas.

### `timeregistrationactivity` — desglose de horas por función (costes)
```json
{
  "id": 1, "time_registration": "/timeregistration/20",
  "project_function": "/projectfunctions/490",
  "description": "Technician (hourly rate) - ...",
  "duration": 18000, "is_activity": true, "from": null, "to": null
}
```
**No es el fichaje**: es la imputación de esas horas a una función de proyecto, para
coste/facturación. Capa aparte, probablemente fuera del MVP.
**Candidato natural para mapear nuestras _tareas_**: cada tarea (que cuelga de una función
de proyecto) → un `timeregistrationactivity`, mientras que la jornada completa →
`timeregistration`. Ver `02_to-be.md` §4.5.

### `project` — cliente/trabajo
Trae `customer` (→ `/contacts/{id}`), `location`, `planperiod_*`, `usageperiod_*`,
`project_type`, `number`, `name`. El "cliente" de Rentman es un `contact`.

### `projectcrew` — **la asignación de trabajador**
```json
{
  "crewmember": "/crew/228", "function": "/projectfunctions/8",
  "planperiod_start": "...14:00", "planperiod_end": "...03:00",
  "hours_planned": 46800, "hours_registered": 0, "activity_status": "no_registration"
}
```
Cruza trabajador + función de proyecto + periodo planificado. Es "quién va a qué
proyecto y cuándo". Mapea a nuestras asignaciones / turnos esperados.

### `projectfunction` — el pivote
`/projectfunctions/{id}` = una plaza/rol dentro de un proyecto (`project`, `subproject`,
`name`, `cost_rate`, `price_rate`). Aparece tanto en `projectcrew.function` como en
`timeregistrationactivity.project_function`.

### `crew` — el trabajador
`id`, `displayname`, `firstname`, `lastname`, `email`, `phone`, `active`, `birthdate`,
`tags`, `custom`, … Mapea a nuestro `Employee`. Candidato a auto-match por `email`.

## 4. Quirks de endpoints (verificado)

| Endpoint | Resultado |
|---|---|
| `GET /crew`, `/projects`, `/projectcrew`, `/appointments`, `/contacts`, `/projectfunctions`, `/subprojects`, `/timeregistrationactivities` | ✅ 200 |
| `GET /timeregistration/{id}`, `/projectfunctions/{id}` (por id) | ✅ 200 |
| `GET /crewmembers`, `/functions`, `/timeregistrations` (colección en plural) | ❌ 403 con mensaje raro de auth (`Invalid key=value pair … Authorization header`) |

**Lectura:** usar `/crew` (no `/crewmembers`); el "padre" de horas se lee por id
(`/timeregistration/{id}`) aunque su colección en plural dé 403. La escritura del
`timeregistration` (POST) **aún no está probada** — ver decisiones abiertas.

## 5. Escritura y límites — VERIFICADO en sandbox (2026-08-01)

Cuenta sandbox `encodebiz`. Todo lo de abajo está ejecutado de verdad, no inferido.

### La escritura de `timeregistration` funciona

`POST /timeregistration` (singular; la plural sigue dando 403). Cuerpo que funciona:

```json
{
  "crewmember": "/crew/226",
  "start": "2026-08-01T08:00:00+02:00",
  "end": "2026-08-01T16:00:00+02:00",
  "duration": 27000,
  "break_duration": 1800,
  "leavetype": "/leavetypes/1",
  "remark": "checkbiz:<checkinId>"
}
```

Cuatro cosas que sólo se aprenden escribiendo:

1. **`leavetype` es obligatorio.** Sin él la API responde **500** ("No se pudieron
   guardar los ítems"), sin decir qué falta. Hay que mandar el tipo *trabajado* de la
   cuenta (`is_labor: "worked"`, `type: "G"`); los ids no son universales, así que se
   resuelve leyendo `/leavetypes`, no se cablea.
2. **`duration` es NETO y lo recalcula Rentman.** Enviado 28800 (8 h bruto) con
   `break_duration` 1800 → guardó **27000** (7,5 h). Mandar el bruto sólo consigue que
   nuestra copia no cuadre con la suya y que la auditoría de D2 marque falsos positivos.
3. **`remark` se guarda y se devuelve** → sirve de trazabilidad hacia el checklog origen.
4. **Rechaza solapes**: mismo crew member con horas o ausencia en ese periodo →
   **400** "Ya se ha registrado el horario o se ha solicitado una ausencia para este
   periodo". Es un no definitivo: reintentarlo no cambia nada.

`DELETE /timeregistration/{id}` → 200 (usado para limpiar las pruebas).
`status` nace como `pending` (no `approved`) y es cosa de Rentman, no nos incumbe.

### El 403 no era rate limit

**120 GET seguidos en 16 s sin un solo corte.** Los 403 que veíamos son de colecciones
que no existen (`/crewmembers`, `/functions`, `/timeregistrations`) y traen un mensaje
de auth de AWS. O sea: el rate limit no es la restricción que asumíamos, y tratar el
403 como throttling sólo hacía reintentar contra un endpoint que nunca responde.

### No hay filtro por `modified`, pero sí orden

`?modified=gt,…` y `?modified[gt]=…` no filtran (devuelven vacío o lo ignoran).
`?sort=-modified` **sí** funciona, y `?fields=` recorta la respuesta. Con eso el delta
del pull sale barato igual: se pagina por `modified` descendente y se corta al llegar a
la marca de agua. Paginación por `limit`/`offset` verificada (también hay cursor en
`next_page_url`, no hace falta).

### Lo que sigue sin probarse

- Creación de `project` y `projectcrew` (capa de catálogo, bloqueada por D3–D5).
- Comportamiento en la cuenta REAL del cliente: esto es un sandbox.

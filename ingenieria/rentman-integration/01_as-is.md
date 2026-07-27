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

## 5. Lo que aún no se ha medido / probado

- **Rate limit real.** Rentman corta con 403 pero no documenta el techo por endpoint.
  Hay que medirlo (script de Fase 0 `ratelimit`) porque marca la cadencia del polling.
- **Filtro por `modified`.** Si la API permite `modified > X` / ordenar por `modified`,
  el polling trae solo el delta (barato). Si no, hay que diffear por `updateHash`.
- **Escritura.** Ningún POST/PUT ejecutado todavía (no se escribe en la cuenta real
  sin autorización). Falta validar la creación de `timeregistration`, `project`,
  `projectcrew`.

# 04 — Contratos de API

**Base:** `https://<host>/api/v1/sales/crm`
**Auth:** cabecera `X-Encodebiz-Key` con una de dos claves ([TDR-002](./tdr/TDR-002-superficie-interna-y-actor.md)):

| Clave | Quién la tiene | Qué abre |
|---|---|---|
| `ENCODEBIZ_API_KEY` | El backoffice (y el resto de servicios) | Todo `/crm` |
| `SALES_CRM_AGENT_KEY` | Solo el plugin de Cowork | Solo `POST /crm/mcp` ([TDR-003](./tdr/TDR-003-servidor-mcp-y-plugin-cowork.md)) |

Sin clave válida: **404** `{ ok: false, error: "not_found" }`, igual que el resto de la
superficie interna de `sales`.

**Actor:** toda escritura de esta API exige `X-Encodebiz-Actor: staff:<uid>`. Sin él, **400**
`actor_required`. Por el MCP el actor lo pone el servidor (`agent:cowork`).

**Formato:** el de `sales`. Éxito `{ ok: true, ... }`. Error `{ ok: false, error: "<codigo>" }`;
en validación se añade `details: ["campo: mensaje"]`.

| HTTP | `error` | Cuándo |
|---|---|---|
| 400 | `invalid_request` | El cuerpo no pasa el esquema `zod` |
| 400 | `actor_required` | Falta o no encaja `X-Encodebiz-Actor` |
| 404 | `not_found` | Sin clave, o el recurso no existe |
| 409 | `duplicate_account` | CIF o dominio ya registrados (devuelve `accountId` existente) |
| 409 | `profile_required` | Actividad saliente sin perfil vigente ([ADR-003](./adr/ADR-003-sin-perfil-no-hay-contacto.md)) |
| 409 | `contact_opted_out` | Actividad saliente a un contacto con oposición |
| 409 | `email_not_allowed` | Email saliente a un contacto por interés legítimo que nunca ha escrito ([06 §D5](./06_decisiones-abiertas.md)) |
| 409 | `contact_required` | Email saliente sin `contactId` |
| 409 | `invalid_transition` | Cambio de etapa no permitido o sin el dato que exige |
| 429 | `too_many_requests` | Límite de la clave del agente (solo `/crm/mcp`) |

---

## Cuentas

### `GET /accounts`
Query: `niche?`, `stage?`, `ownerStaffId?`, `q?` (nombre, dominio o CIF), `limit` (≤ 100,
por defecto 50), `cursor?` (id).
```json
{ "ok": true, "accounts": [ { "id": 12, "name": "Limpiezas Norte", "niche": "limpieza",
  "stage": "researched", "icpFit": 78, "nextActionAt": "2026-10-15T09:00:00Z",
  "liveSignals": 2 } ], "nextCursor": 11 }
```

### `GET /accounts/:id`
Cuenta completa con `contacts`, `liveSignals`, `profile` (vigente o `null`) y las 20
actividades más recientes.

### `POST /accounts`
```json
{ "name": "Limpiezas Norte", "niche": "limpieza", "cif": "B12345678",
  "domain": "limpiezasnorte.es", "province": "Bizkaia", "employeesBand": "50-99",
  "source": "outbound", "icpFit": 78 }
```
`201 { ok: true, accountId }` · `409 duplicate_account` con `accountId`.

### `PATCH /accounts/:id`
Campos editables: datos de empresa, `motion`, `icpFit`, `nextAction`, `nextActionAt`.
**No** cambia `stage` ni `owner`.

### `POST /accounts/:id/stage`
```json
{ "stage": "trial", "entityId": "abc123" }
{ "stage": "lost", "lostReason": "competitor" }
```
Valida la transición ([03](./03_modelo-de-datos.md), [02](./02_to-be.md#el-embudo)).

### `PATCH /accounts/:id/owner`
`{ "ownerStaffId": "uid" }`. Asignar dueño es cosa del personal: no tiene herramienta MCP.

## Perfil

### `PUT /accounts/:id/profile`
Crea una versión nueva. Si la cuenta está en `signal`, la pasa a `researched`.
```json
{ "summary": "…", "pains": [ { "pain": "…", "evidence": "https://…" } ],
  "hook": "…", "roiInputs": { "workers": 60, "assumed": false },
  "sources": [ "https://…" ] }
```

## Contactos

### `POST /accounts/:id/contacts`
```json
{ "fullName": "Ana Ruiz", "roleTitle": "Jefa de operaciones", "decisionRole": "decider",
  "email": "ana@limpiezasnorte.es", "emailSource": "apollo", "linkedinUrl": "https://…" }
```

### `POST /contacts/:id/opt-out`
Registra la oposición. Irreversible desde la API.

## Señales

### `POST /accounts/:id/signals`
```json
{ "kind": "tender_awarded", "title": "Adjudicada limpieza de 14 colegios en Getxo",
  "sourceUrl": "https://…", "strength": "high",
  "detectedAt": "2026-10-13T08:00:00Z", "expiresAt": "2026-12-13T00:00:00Z" }
```

## Actividad

### `POST /accounts/:id/activities`
```json
{ "contactId": 31, "type": "linkedin", "direction": "outbound",
  "summary": "Mensaje de conexión con gancho de licitación", "occurredAt": "…" }
```
Efectos en el caso de uso, en una transacción:
- primera `outbound` → `stage = contacted`;
- primera `inbound` con `outcome` `replied` o `interested` → `stage = conversation`, también
  desde `signal` o `researched` (y [ADR-007](./adr/ADR-007-sales-lead-qualified-lo-emite-el-crm.md));
- `outcome = booked` → `stage = demo`;
- `outcome = opted_out` → `opted_out_at` en el contacto.

## Leads

### `POST /leads/:id/promote`
Convierte un lead `accepted` en cuenta (`source = lead`) y contacto. Si el dominio del email o
el CIF ya existen, enlaza el lead a esa cuenta en vez de duplicarla.
`201 { ok: true, accountId, created: true|false }`.

## Lectura agregada

### `GET /next-actions`
Query: `due` (`today` | `overdue` | `week`), `ownerStaffId?`. Cuentas abiertas ordenadas por
`nextActionAt`.

### `GET /pipeline`
Query: `niche?`. `{ ok: true, byStage: { "signal": 40, "researched": 12, ... }, byNiche: {...} }`.

## Importación

### `POST /import`
`Content-Type: text/csv` (≤ 1 MB, ≤ 1.000 filas). Columnas en [TDR-005](./tdr/TDR-005-importacion-enriquecimiento-y-senales.md).
Query `apply=1` para escribir; sin él **simula** y devuelve lo que haría, como los scripts del repo.
```json
{ "ok": true, "applied": false, "create": 120, "link": 8, "skipped": [ { "row": 14, "reason": "missing_niche" } ] }
```

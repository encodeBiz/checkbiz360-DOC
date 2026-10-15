# 03 — Modelo de datos

Migración **`031_sales_crm.sql`**, en `encodebiz-api/migrations/`. Idempotente como las
anteriores (`CREATE TABLE IF NOT EXISTS`, `CHECK` con nombre comprobado en `pg_constraint`).
Se aplica a mano por SSH, como todas: primero en `encodebiz_staging`, después en
`encodebiz_analytics`.

> Comprobar antes de crearla que ninguna rama abierta ha reservado el `031` (ya hay dos `013`).

Convenciones heredadas de `sales_leads`: `BIGSERIAL`, `TIMESTAMPTZ DEFAULT NOW()`, enumerados
como `VARCHAR` + `CHECK`, nombres de columna en `snake_case`.

---

## `sales_accounts` — la empresa

| Columna | Tipo | Notas |
|---|---|---|
| `id` | `BIGSERIAL PK` | |
| `name` | `VARCHAR(160) NOT NULL` | Nombre comercial |
| `legal_name` | `VARCHAR(200)` | Razón social |
| `cif` | `VARCHAR(16)` | Normalizado a mayúsculas sin separadores |
| `domain` | `VARCHAR(160)` | Dominio web sin `www.`, en minúsculas |
| `niche` | `VARCHAR(16) NOT NULL` | `construccion`, `limpieza`, `sad`, `eventos` |
| `cnae` | `VARCHAR(8)` | Código CNAE declarado o inferido |
| `employees_band` | `VARCHAR(10)` | `1-9`, `10-49`, `50-99`, `100-249`, `250+` |
| `province` | `VARCHAR(60)` | |
| `linkedin_url` | `TEXT` | |
| `stage` | `VARCHAR(14) NOT NULL DEFAULT 'signal'` | Ver [02](./02_to-be.md#el-embudo) |
| `lost_reason` | `VARCHAR(24)` | Obligatorio si `stage = 'lost'` (`CHECK`) |
| `motion` | `VARCHAR(8)` | `enter`, `grow`, `protect` ([ADR-004](./adr/ADR-004-la-oportunidad-nace-en-la-senal.md)) |
| `icp_fit` | `SMALLINT` | 0–100; criterios en la skill `tam-icp` |
| `source` | `VARCHAR(10) NOT NULL` | `lead`, `outbound`, `import`, `referral` |
| `lead_id` | `BIGINT REFERENCES sales_leads(id) ON DELETE SET NULL` | Ver nota de retención |
| `entity_id` | `VARCHAR(64)` | `entities/{id}` de Firestore; obligatorio en `trial` y `won` (`CHECK`) |
| `owner_staff_id` | `VARCHAR(128)` | uid del personal (`backoffice_users`) |
| `next_action` | `TEXT` | |
| `next_action_at` | `TIMESTAMPTZ` | |
| `created_by` | `VARCHAR(160) NOT NULL` | Actor ([TDR-002](./tdr/TDR-002-superficie-interna-y-actor.md)) |
| `created_at`, `updated_at` | `TIMESTAMPTZ` | |

**Índices:** `UNIQUE (cif) WHERE cif IS NOT NULL` · `UNIQUE (lower(domain)) WHERE domain IS NOT NULL`
· `(stage, niche)` · `(next_action_at) WHERE stage NOT IN ('won','lost')` · `(owner_staff_id, stage)`.

**Nota de retención.** La limpieza de `sales` borra leads aceptados a los 730 días. Por eso
`lead_id` es `ON DELETE SET NULL` y **promover un lead copia** a la cuenta y al contacto lo que
haga falta (nombre, empresa, email, teléfono): la cuenta no depende de que el lead siga ahí.

**`lost_reason`:** `no_fit`, `no_budget`, `competitor`, `no_response`, `timing`, `other`.
Cerrado a propósito: un texto libre no se puede contar.

## `sales_contacts` — la persona que decide

| Columna | Tipo | Notas |
|---|---|---|
| `id` | `BIGSERIAL PK` | |
| `account_id` | `BIGINT NOT NULL REFERENCES sales_accounts(id)` | |
| `full_name` | `VARCHAR(120) NOT NULL` | |
| `role_title` | `VARCHAR(120)` | Cargo tal como lo pone la persona |
| `decision_role` | `VARCHAR(12)` | `decider`, `influencer`, `user`, `gatekeeper` |
| `email`, `phone`, `linkedin_url` | | |
| `email_source` | `VARCHAR(40)` | Proveedor que dio el email (cascada, [TDR-005](./tdr/TDR-005-importacion-enriquecimiento-y-senales.md)) |
| `email_verified_at` | `TIMESTAMPTZ` | |
| `lawful_basis` | `VARCHAR(20) NOT NULL DEFAULT 'legitimate_interest'` | `legitimate_interest`, `consent`, `contract` |
| `informed_at` | `TIMESTAMPTZ` | Cuándo se le dio la información del art. 14 RGPD |
| `opted_out_at` | `TIMESTAMPTZ` | Oposición. Con valor, no admite actividad saliente |
| `created_by`, `created_at` | | |

**Índices:** `(account_id)` · `UNIQUE (lower(email)) WHERE email IS NOT NULL`.

## `sales_signals` — por qué ahora

| Columna | Tipo | Notas |
|---|---|---|
| `id` | `BIGSERIAL PK` | |
| `account_id` | `BIGINT NOT NULL REFERENCES sales_accounts(id)` | |
| `kind` | `VARCHAR(24) NOT NULL` | `tender_awarded`, `new_site`, `field_hiring`, `new_branch`, `season`, `inspection`, `leadership_change`, `funding`, `competitor_pain`, `other` |
| `title` | `VARCHAR(200) NOT NULL` | Una línea, en lenguaje del nicho |
| `source_url` | `TEXT` | Obligatoria salvo `kind = 'other'`: una señal sin fuente es una suposición |
| `strength` | `VARCHAR(6) NOT NULL` | `low`, `medium`, `high` |
| `detected_at` | `TIMESTAMPTZ NOT NULL` | |
| `expires_at` | `TIMESTAMPTZ NOT NULL` | Una señal caducada no cuenta ([ADR-004](./adr/ADR-004-la-oportunidad-nace-en-la-senal.md)) |
| `created_by`, `created_at` | | |

**Índices:** `(account_id, expires_at DESC)` · `(kind, detected_at DESC)`.

## `sales_account_profiles` — conocer antes de contactar

Versionado: cada investigación es una fila nueva. El perfil vigente es el último.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | `BIGSERIAL PK` | |
| `account_id` | `BIGINT NOT NULL REFERENCES sales_accounts(id)` | |
| `summary` | `TEXT NOT NULL` | Qué hace, cómo opera en campo, tamaño de cuadrillas |
| `pains` | `JSONB NOT NULL` | `[{ pain, evidence }]` — dolor principal y el que engancha |
| `hook` | `TEXT NOT NULL` | Dolor A → dolor B, en jerga del nicho |
| `roi_inputs` | `JSONB` | Solo datos con fuente; los supuestos van marcados `assumed: true` |
| `sources` | `JSONB NOT NULL` | URLs consultadas |
| `researched_by` | `VARCHAR(160) NOT NULL` | Actor |
| `researched_at` | `TIMESTAMPTZ NOT NULL DEFAULT NOW()` | |

**Índice:** `(account_id, researched_at DESC)`.

## `sales_activities` — lo que pasó

**Solo se añade.** No hay `UPDATE` ni `DELETE` en la API: una corrección es una actividad
`note` nueva. Es el histórico que se enseña a un cliente si pregunta qué se le dijo y cuándo.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | `BIGSERIAL PK` | |
| `account_id` | `BIGINT NOT NULL REFERENCES sales_accounts(id)` | |
| `contact_id` | `BIGINT REFERENCES sales_contacts(id)` | |
| `type` | `VARCHAR(10) NOT NULL` | `email`, `linkedin`, `call`, `meeting`, `demo`, `note` |
| `direction` | `VARCHAR(8) NOT NULL` | `outbound`, `inbound`, `internal` |
| `summary` | `TEXT NOT NULL` | |
| `outcome` | `VARCHAR(16)` | `no_answer`, `replied`, `interested`, `not_interested`, `booked`, `opted_out` |
| `occurred_at` | `TIMESTAMPTZ NOT NULL` | |
| `actor` | `VARCHAR(160) NOT NULL` | Quién lo registró |
| `created_at` | `TIMESTAMPTZ DEFAULT NOW()` | |

**Índices:** `(account_id, occurred_at DESC)`.

`outcome = 'opted_out'` escribe además `sales_contacts.opted_out_at` en la misma transacción.

---

## Retención

Pendiente de decidir ([06 §D4](./06_decisiones-abiertas.md)). Propuesta: cuentas `lost` sin
actividad en 24 meses → se anonimizan sus contactos (nombre, email, teléfono, LinkedIn a
`NULL`) y se conservan cuenta, señales y actividad para medir. Se añade al barrido existente
`POST /maintenance/cleanup` y al script, con `--apply` como siempre.

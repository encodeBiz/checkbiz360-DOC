# TDR-001 — Dominio, casos de uso y repositorios del CRM en `sales`

**Fecha:** 2026-10-13
**Estado:** Diseño propuesto
**Componente:** `encodebiz-api` — `services/sales`
**Decisiones de referencia:** [ADR-001](../adr/ADR-001-el-crm-vive-en-sales.md),
[ADR-002](../adr/ADR-002-la-cuenta-es-la-unidad-el-lead-una-entrada.md),
[ADR-003](../adr/ADR-003-sin-perfil-no-hay-contacto.md),
[ADR-005](../adr/ADR-005-el-agente-habla-con-sales-por-mcp-propio.md)

---

## 1. Dónde vive

Dentro de `services/sales/src`, con las mismas capas que ya usa el servicio. El CRM no va a
`packages/shared`: ningún otro servicio lo necesita y el backoffice lo pide por HTTP.

```
domain/
  entities/crm/Account.ts          Account, AccountStage, Niche, Motion, LostReason
  entities/crm/Contact.ts          Contact, DecisionRole, LawfulBasis
  entities/crm/Signal.ts           Signal, SignalKind, SignalStrength
  entities/crm/AccountProfile.ts   AccountProfile
  entities/crm/Activity.ts         Activity, ActivityType, Direction, Outcome
  crm/stageMachine.ts              transiciones permitidas y requisitos (puro, sin I/O)
  interfaces/crm/*Repository.ts    un repositorio por agregado
application/crm/
  CreateAccount.ts  UpdateAccount.ts  ChangeStage.ts  AssignOwner.ts
  SaveProfile.ts    AddContact.ts     OptOutContact.ts
  AddSignal.ts      LogActivity.ts    PromoteLead.ts
  ListAccounts.ts   GetAccount.ts     NextActions.ts  Pipeline.ts
  crmConfig.ts      constantes con nombre (ver §4)
infrastructure/crm/
  PostgresAccountRepository.ts  PostgresContactRepository.ts
  PostgresSignalRepository.ts   PostgresProfileRepository.ts
  PostgresActivityRepository.ts
  withTransaction.ts            BEGIN/COMMIT/ROLLBACK sobre un cliente de `pool`
interfaces/http/
  crm.schemas.ts                shapes de zod, compartidos por la API y el MCP
  crm.router.ts                 rutas HTTP; nada de lógica
  crmAccess.ts                  las dos claves y el actor (TDR-002)
interfaces/mcp/
  crm.mcp.ts                    servidor MCP; cada herramienta llama a un caso de uso (TDR-003)
```

La API HTTP y el MCP son dos puertas al mismo caso de uso. Ninguna regla vive en ellas.

## 2. Reglas del dominio y dónde se comprueban

| Regla | Dónde |
|---|---|
| Transiciones de etapa y sus requisitos (`entity_id` en `trial`/`won`, `lost_reason` en `lost`) | `stageMachine.ts`, llamado por `ChangeStage` y `LogActivity` |
| Sin perfil vigente no hay actividad saliente | `LogActivity` |
| Sin actividad saliente a contacto con `opted_out_at` | `LogActivity` |
| Email saliente solo a quien ha escrito o con `consent`/`contract` ([06 §D5](../06_decisiones-abiertas.md)) | `LogActivity` |
| `outcome = opted_out` marca el contacto | `LogActivity`, en la misma transacción |
| Avance automático de etapa por actividad | `LogActivity` → `stageMachine` |
| `SaveProfile` en `signal` pasa a `researched` | `SaveProfile`, en la misma transacción |
| Deduplicación por CIF y dominio | `CreateAccount` y `PromoteLead`, respaldada por los índices únicos |
| Una cuenta `lost` solo vuelve a `signal` con señal nueva | `AddSignal` |

`stageMachine.ts` es una tabla, no una cascada de `if`, y no avanza nunca hacia atrás salvo
`lost → signal`. Avanzar de forma automática solo mueve hacia delante y puede saltar etapas
(`signal → conversation` cuando un lead responde): una respuesta tardía de una cuenta ya en `demo`
no la devuelve a `conversation`. Las transiciones manuales son la tabla de
[02 §El embudo](../02_to-be.md#el-embudo).

## 3. Transacciones

`LogActivity`, `SaveProfile`, `ChangeStage` y `PromoteLead` escriben en más de una tabla.
Todas pasan por `withTransaction` con un cliente propio de `pool` (no `pool.query`, que puede
usar una conexión distinta por sentencia). Los repositorios aceptan el cliente como argumento
opcional.

## 4. Constantes

En `crmConfig.ts`, leídas del entorno con valor por defecto:

| Constante | Variable | Por defecto |
|---|---|---|
| `PROFILE_MAX_AGE_DAYS` | `CRM_PROFILE_MAX_AGE_DAYS` | 90 |
| `LIST_DEFAULT_LIMIT` / `LIST_MAX_LIMIT` | — | 50 / 100 |
| `IMPORT_MAX_ROWS` | `CRM_IMPORT_MAX_ROWS` | 1000 |
| `COLD_EMAIL_ALLOWED` | `CRM_COLD_EMAIL_ALLOWED` | `false` |

## 5. Normalización

- CIF: mayúsculas, sin espacios, guiones ni puntos.
- Dominio: minúsculas, sin protocolo, sin `www.`, sin ruta. Se deriva del email del contacto si
  la cuenta no lo trae y el email no es de un dominio genérico (lista en `crmConfig.ts`).
- Email: el saneado que ya existe en `application/security/sanitize.ts` (`isSafeEmail`).

## 6. Tests

`node --test`, como `test/ads.test.ts`:

- `stageMachine`: todas las transiciones de la tabla, permitidas y prohibidas. Unidad pura.
- Casos de uso con repositorios en memoria: `profile_required`, `contact_opted_out`, avance
  automático, `lost → signal`, duplicados.
- `PromoteLead` cuando el lead ya no existe (borrado por retención) y cuando la empresa ya existe.

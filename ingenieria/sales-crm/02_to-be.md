# 02 — Arquitectura objetivo (To-Be)

## Quién habla con quién

```
 Landing ──POST /leads──────────────┐
                                    ▼
                          ┌───────────────────┐   Postgres
 Backoffice (personal) ──▶│  services/sales   │──▶ sales_leads (existe)
   SalesClient            │  /crm/*  (nuevo)  │    sales_accounts, sales_contacts,
   ENCODEBIZ_API_KEY      └───────────────────┘    sales_signals, sales_account_profiles,
                                    ▲              sales_activities (nuevas, 031)
 Cowork (plugin GTM) ──MCP (HTTP)───┘
   /crm/mcp, SALES_CRM_AGENT_KEY
```

- **`sales` es el único que escribe.** Las reglas del dominio (sin perfil no hay contacto,
  etapas, opt-out) viven en sus casos de uso y valen igual venga la llamada del panel o del
  agente. [ADR-001](./adr/ADR-001-el-crm-vive-en-sales.md)
- **El agente no tiene la clave de la plataforma.** Usa una clave propia que solo abre el servidor
  MCP de `/crm`, y sus herramientas llaman a los mismos casos de uso que la API.
  [ADR-005](./adr/ADR-005-el-agente-habla-con-sales-por-mcp-propio.md)
- **Toda escritura lleva actor**: `staff:<uid>` desde el backoffice, `agent:cowork` puesto por el servidor cuando entra con la clave del agente.
  [TDR-002](./tdr/TDR-002-superficie-interna-y-actor.md)

## El embudo

```
señal ─▶ investigada ─▶ contactada ─▶ conversación ─▶ demo ─▶ prueba ─▶ cliente
  │           │              │              │           │        │
  └───────────┴──────────────┴──────────────┴───────────┴────────┴──▶ perdida (motivo)
```

| Etapa (`stage`) | Entra cuando | Quién |
|---|---|---|
| `signal` | Existe la cuenta con al menos una señal viva, o llega de un lead o una importación | SDR / agente |
| `researched` | Tiene perfil de cuenta reciente ([ADR-003](./adr/ADR-003-sin-perfil-no-hay-contacto.md)) | SDR / agente |
| `contacted` | Primera actividad saliente registrada | SDR |
| `conversation` | Primera respuesta registrada (actividad entrante) | SDR |
| `demo` | Demo agendada. **Aquí pasa de SDR a AE** | AE |
| `trial` | Prueba de 15 días iniciada; exige `entity_id` | AE |
| `won` | Primera suscripción de pago | AE |
| `lost` | Desde cualquier etapa, con `lost_reason` obligatorio | SDR / AE |

Una cuenta `lost` vuelve a `signal` solo con una señal nueva: así no se reabre por inercia.

**Avance automático y saltos (decidido el 2026-10-13).** Las actividades mueven la etapa hacia
delante y pueden **saltarse** las intermedias: un lead que responde sin que antes haya salido nada
pasa de `signal` (o `researched`) directo a `conversation`; un `booked` lleva a `demo` desde
cualquier etapa anterior. Nunca hacia atrás, y nunca sobre `won` ni `lost`.

A mano (`POST /accounts/:id/stage`) solo se mueve lo que no tiene actividad que lo dispare:

| Desde | A mano puede ir a |
|---|---|
| `signal`, `researched` | `lost` |
| `contacted`, `conversation` | `demo`, `lost` |
| `demo` | `trial`, `won`, `lost` |
| `trial` | `won`, `lost` |
| `won`, `lost` | — (`lost → signal` solo con señal nueva) |

`researched`, `contacted` y `conversation` no se fijan a mano: los pone el perfil o la actividad
que los demuestra.

## Reparto SDR / AE

Un solo campo `owner_staff_id`. El traspaso es cambiar de dueño al entrar en `demo`. Hoy SDR y
AE son la misma persona; el modelo no necesita saberlo hasta que dejen de serlo.

## El agente (plugin de Cowork)

Siete skills que comparten un contexto de producto y escriben en el CRM a través del servidor
MCP de `sales`. Detalle en [TDR-003](./tdr/TDR-003-servidor-mcp-y-plugin-cowork.md).

| Skill | Etapa que mueve |
|---|---|
| `contexto-checkbiz360` | — (conocimiento: producto, precios, posicionamiento, nichos, jerga, competidores) |
| `tam-icp` | crea cuentas en `signal` (importación) |
| `senales` | añade señales; fija `motion` |
| `investigar-cuenta` | `signal` → `researched` |
| `outreach` | redacta; registra actividad → `contacted` |
| `marca-personal` | — (contenido de LinkedIn ligado a señales del momento) |
| `crm` | agenda del día, pipeline, próxima acción, cambios de etapa |

## Medición

Al pasar a `conversation` una cuenta que vino de un lead con consentimiento, `sales` emite
`sales_lead_qualified` a GA4 y Google Ads por el mismo camino que `sales_lead_accepted`.
[ADR-007](./adr/ADR-007-sales-lead-qualified-lo-emite-el-crm.md)

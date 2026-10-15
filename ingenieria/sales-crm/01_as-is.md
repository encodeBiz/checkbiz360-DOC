# 01 — Estado actual (As-Is)

Revisado contra `encodebiz-api` en `develop` (`e078f3b`, 2026-10-13).

## `services/sales` (puerto 3009, prefijo `/api/v1/sales`)

Hace una cosa y la hace bien: **captar**. La landing envía un formulario, el servicio lo pasa
por nueve barreras antispam, lo guarda en Postgres, avisa a la bandeja comercial y mide la
conversión en GA4 (`sales_lead_accepted`) y Google Ads (Data Manager API).

**Tres superficies, montadas en este orden en `src/app.ts`:**

| Superficie | Router | Acceso |
|---|---|---|
| Pública | `salesPublicRouter` | La landing (`POST /leads`, `POST /conversions`) |
| Exportación | `salesExportRouter` | Basic auth (Google Ads) |
| Interna | `salesRouter` detrás de `hiddenApiKey` | `X-Encodebiz-Key` = `ENCODEBIZ_API_KEY`; sin ella, **404** |

El orden importa: `hiddenApiKey` se monta sobre todo `/api/v1/sales`, así que cualquier
router que necesite otra credencial tiene que ir **antes**. Es lo que ya hace la exportación.

**Tablas** (base `encodebiz_analytics` en producción, `encodebiz_staging` en desarrollo):

| Tabla | Migración | Qué guarda |
|---|---|---|
| `sales_leads` | `004`, ampliada en `005`, `019`, `029`, `030` | Cada intento del formulario, con su clasificación (`accepted`, `spam`, `bot`, `duplicate`, `blocked`, `flooded`) y el estado de aviso, GA4 y Ads |
| `sales_blocklist` | `005` | Bloqueo manual por email, dominio o IP |
| `sales_conversions` | `020` | Clics de WhatsApp |

**Lo que condiciona este diseño:**

- **La retención borra leads aceptados.** `POST /maintenance/cleanup` elimina los `accepted`
  con más de `SALES_LEAD_RETENTION_DAYS` (730 por defecto). Cualquier tabla que apunte a
  `sales_leads` tiene que sobrevivir a ese borrado.
- **El id del lead no se reutiliza nunca.** Google Ads lo usa como `order_id`;
  `limpiar-sales.ts` no reinicia la secuencia por eso. El CRM no puede renumerar leads.
- **Stack del servicio:** Express, `pg` por `pool` de `@encodebiz/shared`, `zod` para validar,
  tests con `node --test` (`test/ads.test.ts`). No hay ORM.
- **Formato de respuesta:** `{ ok: true, ... }` / `{ ok: false, error: "<codigo>" }`.

## `services/backoffice` + `apps/backoffice-web`

Panel interno del personal de encodeBiz (React + MUI, servido por el propio servicio en
`/backoffice`).

- **Puerta:** `requireStaff` sobre todo `backofficeRouter`: token de Firebase **y** ficha activa
  en `backoffice_users`. Una ruta nueva nace protegida.
- **Permisos:** una sola tabla en `application/staff/permissions.ts`. Ya existen `leads:read` y
  `leads:write`; el rol `editor` solo escribe sobre leads.
- **Auditoría:** `auditTrail` apunta toda llamada a `/api/v1/backoffice`.
- **Leads:** `modules/leads.router.ts` → `SalesClient.findLeads()` → `GET /api/v1/sales/leads`
  con `ENCODEBIZ_API_KEY`. El backoffice no lee `sales_leads` aunque comparta la base: la
  tabla es de `sales`. `LeadsPage.tsx` los lista con filtro por estado.

## Lo que no existe

- Ninguna noción de **empresa objetivo**, **contacto**, **etapa**, **señal** ni **actividad**.
- Nada que diga qué pasó con un lead después de llegar a la bandeja.
- El evento `sales_lead_qualified`: está anunciado en el README de `sales` y no tiene quien lo
  emita.
- Ninguna vía para que un agente (Claude en Cowork) lea o escriba datos comerciales.

## Herramientas fuera del repo

- **n8n:** instancia cloud de Jose, con conexión MCP verificada desde Claude Desktop.
- **Apollo:** previsto como base de empresas y personas; sin integración hoy.

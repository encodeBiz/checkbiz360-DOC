# TDR-002 — Montaje de `/crm`, las dos claves, el actor y la validación

**Fecha:** 2026-10-13
**Estado:** Diseño propuesto
**Componente:** `encodebiz-api` — `services/sales`
**Decisiones de referencia:** [ADR-001](../adr/ADR-001-el-crm-vive-en-sales.md),
[ADR-005](../adr/ADR-005-el-agente-habla-con-sales-por-mcp-propio.md)

---

## 1. Montaje en `app.ts`

Hoy `hiddenApiKey` se monta sobre todo `/api/v1/sales` y solo acepta `ENCODEBIZ_API_KEY`. El
router del CRM necesita aceptar además la clave del agente, así que va **antes** de esa línea,
con su propia puerta, igual que ya se hizo con `salesExportRouter`:

```ts
// ── CRM (S2S: plataforma o agente) ── antes del router interno, por lo mismo que la exportación
app.use("/api/v1/sales/crm", crmAccess, crmRouter);

// ── Gestión INTERNA ──
app.use("/api/v1/sales", hiddenApiKey, salesRouter);
```

## 2. `crmAccess`

Reutiliza `safeEqual` de `hiddenApiKey.ts` (tiempo constante). Cada clave abre una sola puerta:

| Clave | Abre | No abre |
|---|---|---|
| `ENCODEBIZ_API_KEY` | La API HTTP de `/crm` | `/crm/mcp` |
| `SALES_CRM_AGENT_KEY` | `POST /crm/mcp` | Ninguna ruta HTTP de `/crm` |

- Clave que no corresponde a la ruta → **404** `not_found`, como `hiddenApiKey`.
- `SALES_CRM_AGENT_KEY` vacía o sin definir → el MCP no existe; la API sigue disponible.

Separar así hace que el agente solo pueda hacer lo que exponen las herramientas, y que el
backoffice no pueda colarse por el MCP.

## 3. Límite del agente

`express-rate-limit` (ya es dependencia de `sales`) solo en `/crm/mcp`:
`CRM_AGENT_RATE_LIMIT` peticiones por minuto, 60 por defecto. Responde
`429 { ok: false, error: "too_many_requests" }` sin cabeceras `RateLimit-*`, como el endpoint
público.

## 4. Actor

| Llamante | Valor | Quién lo pone |
|---|---|---|
| Backoffice (API HTTP) | `staff:<uid>` | `SalesClient`, en la cabecera `X-Encodebiz-Actor`, con el uid de `staffOf(req)` |
| Agente (MCP) | `agent:cowork` | `sales`, al entrar con la clave del agente. El cliente no lo declara |

En la API HTTP la cabecera es obligatoria en `POST`, `PUT` y `PATCH`, validada con `zod`:
`^staff:[A-Za-z0-9_-]{1,128}$`. Se guarda en `created_by`, `researched_by` o `actor` según la tabla.

En la API HTTP `sales` se fía del actor porque solo la plataforma tiene esa clave.
La identidad real de la persona la garantiza el backoffice (`requireStaff`) y queda además en
su `auditTrail`.

## 5. Validación

Un esquema `zod` por ruta en `crm.router.ts`, con `.strict()` en los cuerpos: un campo
desconocido es `400 invalid_request` con `details`. A diferencia del formulario público, aquí
los llamantes son nuestros y un campo de más indica un error del llamante, no un formulario que
ha cambiado.

Textos: `stripControlChars` de `security/sanitize.ts` en todo campo de una línea; `stripBodyChars`
en `summary`, `hook` y `title`.

## 6. Errores no controlados

Los recoge el manejador final de `app.ts` (`500 internal_error`). En el log, el código de error y
el id de la cuenta; nunca el email, el teléfono ni el texto de la actividad.

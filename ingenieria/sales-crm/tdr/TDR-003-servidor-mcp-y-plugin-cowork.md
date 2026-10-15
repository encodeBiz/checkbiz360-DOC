# TDR-003 — Servidor MCP del CRM y plugin de Cowork

**Fecha:** 2026-10-13
**Estado:** Diseño propuesto
**Componentes:** `services/sales` · plugin `checkbiz360-gtm`
**Decisiones de referencia:** [ADR-003](../adr/ADR-003-sin-perfil-no-hay-contacto.md),
[ADR-005](../adr/ADR-005-el-agente-habla-con-sales-por-mcp-propio.md),
[ADR-006](../adr/ADR-006-claude-prepara-la-persona-envia.md)

---

## 1. El servidor MCP en `sales`

**Ruta:** `POST /api/v1/sales/crm/mcp`, detrás de `crmAccess` ([TDR-002](./TDR-002-superficie-interna-y-actor.md)).
Solo acepta la clave del agente: con `ENCODEBIZ_API_KEY` responde 404. La plataforma usa la
API HTTP, no el MCP.

**Pieza:** `interfaces/mcp/crm.mcp.ts`, con `McpServer` y el transporte HTTP «streamable» del
SDK oficial (`@modelcontextprotocol/sdk`), en modo **sin sesión**: un servidor y un transporte por
petición, sin estado en memoria. El contenedor se puede reiniciar o escalar sin romper a nadie.

### Comprobado el 2026-10-13

Con una prueba de concepto fuera del repo, con las mismas piezas que `sales` (Node 22,
TypeScript 5.4 con `module: commonjs`, `express` 4.22.2, `zod` 3.25.76):

| Punto | Resultado |
|---|---|
| Versión | `@modelcontextprotocol/sdk` **1.32.1** (última publicada). Se fija exacta, sin `^` |
| `zod` | El SDK pide `^3.25 \|\| ^4.0` como *peer*. El lockfile del monorepo ya resuelve **3.25.76**. Se sube el rango de `services/sales/package.json` de `^3.23.8` a `^3.25.0` para que no dependa de la casualidad |
| CommonJS | Funciona: el SDK publica `dist/cjs` para `require` y `typesVersions` para la resolución de TypeScript del monorepo |
| Express 4 | `transport.handleRequest(req, res, req.body)` acepta el `req`/`res` de Express 4. El SDK trae su propio Express 5 anidado; no choca con el de `sales` |
| Modo sin sesión | `new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true })`, un `McpServer` por petición, cerrados en `res.on("close")`. `initialize`, `tools/list` y `tools/call` responden en JSON plano |
| Esquemas | `server.registerTool(nombre, { description, inputSchema: shape }, handler)` con un *shape* de zod. El SDK publica el JSON Schema con `additionalProperties: false`, el mismo criterio que `.strict()` en la API |
| Validación | Una entrada inválida no llega al handler: el SDK devuelve `isError: true` con el detalle de zod |

`server.tool(...)` está marcado como obsoleto en esta versión: se usa `registerTool`.

**Esquemas:** los esquemas de entrada se definen una vez en `interfaces/http/crm.schemas.ts` como
*shapes* de zod. La API HTTP los usa con `z.object(shape).strict()` y el MCP los pasa como
`inputSchema` de cada herramienta. Un campo nuevo se añade en un solo sitio.

**Herramientas** — cada una llama al caso de uso de [TDR-001](./TDR-001-dominio-y-capas-en-sales.md)
con actor `agent:cowork`:

| Herramienta | Caso de uso | Equivale a |
|---|---|---|
| `crm_search_accounts` | `ListAccounts` | `GET /accounts` |
| `crm_get_account` | `GetAccount` | `GET /accounts/:id` |
| `crm_create_account` | `CreateAccount` | `POST /accounts` |
| `crm_update_account` | `UpdateAccount` | `PATCH /accounts/:id` |
| `crm_change_stage` | `ChangeStage` | `POST /accounts/:id/stage` |
| `crm_save_profile` | `SaveProfile` | `PUT /accounts/:id/profile` |
| `crm_add_contact` | `AddContact` | `POST /accounts/:id/contacts` |
| `crm_add_signal` | `AddSignal` | `POST /accounts/:id/signals` |
| `crm_log_activity` | `LogActivity` | `POST /accounts/:id/activities` |
| `crm_next_actions` | `NextActions` | `GET /next-actions` |
| `crm_pipeline` | `Pipeline` | `GET /pipeline` |

No hay herramienta para reasignar dueño, registrar una oposición ni importar: son cosas de una
persona desde el backoffice.

**Errores:** un error de negocio (`profile_required`, `contact_opted_out`,
`invalid_transition`, `duplicate_account`) se devuelve como resultado de herramienta con error y
con el mismo código que la API, para que el agente sepa qué hacer (por ejemplo, investigar antes
de registrar el contacto). Los errores inesperados no llevan detalle interno.

**Descripciones de las herramientas:** son parte del contrato. Cada una dice qué hace y cuándo
falla («falla con `profile_required` si la cuenta no tiene perfil de los últimos 90 días»).

## 2. El plugin `checkbiz360-gtm`

```
checkbiz360-gtm/
  .claude-plugin/plugin.json
  .mcp.json                         servidor "checkbiz360-crm" (HTTP), clave desde variable de entorno
  skills/
    contexto-checkbiz360/SKILL.md
      references/producto.md        módulos, precios, prueba, roadmap (de Clients/14-referencia/91)
      references/posicionamiento.md control operativo de campo; competidores
      references/nicho-limpieza.md  jerga, dolores encadenados, decisores, señales típicas
      references/nicho-construccion.md
      references/nicho-sad.md
      references/nicho-eventos.md   incluye RentmanBiz
    tam-icp/SKILL.md                + references/fuentes.md, references/criterios-icp.md
    senales/SKILL.md                + references/tipos-y-caducidad.md
    investigar-cuenta/SKILL.md      + references/plantilla-perfil.md
    outreach/SKILL.md               + references/roi-tiempo-administrativo.md
    marca-personal/SKILL.md
    crm/SKILL.md
  README.md
```

El formato de plugin de Cowork admite servidores MCP de tipo `http` con `headers` y expansión
`${VARIABLE}` en `.mcp.json` (referencia de componentes del autor de plugins de Cowork). No hace
falta OAuth:

```json
{
  "mcpServers": {
    "checkbiz360-crm": {
      "type": "http",
      "url": "https://api.checkbiz360.com/api/v1/sales/crm/mcp",
      "headers": { "X-Encodebiz-Key": "${CHECKBIZ360_CRM_AGENT_KEY}" }
    }
  }
}
```

Una copia del plugin por entorno, o la URL también como variable
(`${CHECKBIZ360_CRM_URL}`), para apuntar a `api-staging.checkbiz360.com` en desarrollo.

**Lo único que queda por probar en la máquina de Jose:** que la app de escritorio ve la
variable de entorno. En macOS una app abierta desde el Dock no hereda el `~/.zshrc`. Si al
instalar el plugin el servidor no conecta, es lo primero que se mira; no hace falta cambiar el
diseño.

**El contexto es uno.** Las demás skills cargan `contexto-checkbiz360` en lugar de repetir
producto, precios o jerga. Los precios se copian de la documentación pública con fecha, y la
skill avisa si la fecha tiene más de 30 días.

## 3. Lo que cada skill hace contra el CRM

| Skill | Lee | Escribe | Regla |
|---|---|---|---|
| `tam-icp` | — | `crm_create_account` (uno a uno hasta la Fase 4) | Cada cifra de TAM con su fuente y fecha |
| `senales` | `crm_search_accounts` | `crm_add_signal`, `crm_update_account` (`motion`) | Sin `sourceUrl` no hay señal |
| `investigar-cuenta` | `crm_get_account` | `crm_save_profile`, `crm_add_contact` | Fuentes en el perfil; supuestos marcados |
| `outreach` | `crm_get_account` | `crm_log_activity` cuando la persona confirma el envío | Sin perfil, llama antes a `investigar-cuenta`; email solo según [06 §D5](../06_decisiones-abiertas.md) |
| `marca-personal` | `crm_pipeline` y señales vivas | — | — |
| `crm` | `crm_next_actions`, `crm_pipeline` | `crm_change_stage`, `crm_update_account` | — |

## 4. ROI de tiempo administrativo

`outreach` calcula el ahorro con los datos del prospecto (número de trabajadores, centros, horas
semanales que dedica hoy a cuadrar fichajes, partes o documentación) y enseña la fórmula. Los
datos que no da el prospecto se marcan como supuestos y se dicen como tales en el mensaje. No hay
cifras genéricas de ahorro en la skill.

## 5. Secretos

- `SALES_CRM_AGENT_KEY` vive en el entorno del contenedor de `sales` y en la variable de entorno
  local de quien usa el plugin. No se escribe en el plugin ni en el repositorio.
- El plugin se puede compartir sin exponer nada.
- Revocar al agente es cambiar o vaciar `SALES_CRM_AGENT_KEY` y redesplegar `sales`.

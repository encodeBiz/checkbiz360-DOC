# ADR-005 — El agente habla con `sales` por un servidor MCP propio, con una clave que solo abre `/crm`

**Fecha:** 2026-10-13
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («queremos algo muy centralizado en CheckBiz360, no genérico»)

---

## Contexto

El agente GTM es un plugin de Cowork. Para leer y escribir el CRM necesita alcanzar `sales`
desde fuera de la red de contenedores.

`ENCODEBIZ_API_KEY` es la clave S2S **de toda la plataforma**: la aceptan `sales`, `sync`,
`analytics` y el resto de rutas internas. No puede salir de nuestros servidores.

## Decisión

1. **Servidor MCP dentro de `sales`**, en `/api/v1/sales/crm/mcp`. Cada herramienta llama
   directamente al caso de uso del CRM y usa los mismos esquemas `zod` que la API HTTP.
2. **Clave propia del agente:** `SALES_CRM_AGENT_KEY`. Solo la acepta `sales`, solo en `/crm`, no
   permite reasignar dueño y lleva su propio límite de peticiones.
3. **El actor lo pone el servidor**, no el cliente: lo que entra con la clave del agente se
   registra como `agent:cowork`.

## Ampliación (2026-10-14): conector de claude.ai con URL secreta

Comprobado en uso: **Cowork no carga servidores MCP desde un plugin**; solo usa los conectores
de claude.ai, y estos no admiten cabeceras propias (solo OAuth o nada). Para que Cowork llegue
al CRM se añade una segunda puerta al mismo servidor MCP:

- `POST /api/v1/sales/crm/mcp/c/<token>`, con `SALES_CRM_CONNECTOR_TOKEN`: un token propio,
  distinto de `SALES_CRM_AGENT_KEY`, para rotarlo por separado. Solo abre el MCP.
- nginx no registra esa ruta en el access log y `sales` tapa el token en los suyos.
- GET y DELETE responden 405, como pide MCP para un servidor sin sesión.

Decidido por Jose frente a OAuth completo (más seguro, pero días de trabajo). Riesgo aceptado:
quien tenga la URL entra a las 11 herramientas del agente, con su límite de peticiones; se
revoca cambiando el token. OAuth queda como mejora si el conector se comparte con más gente.

## Por qué no n8n

Se propuso n8n como puente y se descartó:

- **Esquemas duplicados.** Cada herramienta de n8n repetiría a mano el contrato que `sales` ya
  valida. Dos fuentes de verdad para el mismo contrato acaban divergiendo.
- **Datos personales fuera de casa.** Nombres, emails y teléfonos de prospectos pasarían por un
  tercero, que pasaría a ser encargado del tratamiento.
- **Un salto y un punto de fallo más**, y depuración repartida en dos sistemas.
- **No es CheckBiz360.** El objetivo es que el contexto comercial viva en la plataforma, no en
  una herramienta de automatización genérica.

## Consecuencias

- `sales` incorpora `@modelcontextprotocol/sdk` 1.32.1, fijada exacta. Es la única dependencia
  nueva del CRM; compatibilidad comprobada en [TDR-003](../tdr/TDR-003-servidor-mcp-y-plugin-cowork.md).
- Las reglas del dominio ([ADR-003](./ADR-003-sin-perfil-no-hay-contacto.md)) valen igual para
  el agente que para el backoffice, porque los dos llegan al mismo caso de uso.
- La clave del agente se rota o revoca sin tocar ningún otro servicio.
- n8n queda, si acaso, para procesos por lotes de la Fase 4, y se revisa entonces
  ([TDR-005](../tdr/TDR-005-importacion-enriquecimiento-y-senales.md)).

# 05 — Fases de implementación

Cada fase es **independiente y desplegable**, por la cadena de siempre
(`feat/x → develop → staging → main`). El orden es por uso: primero lo que permite vender
esta semana. Tope de alcance: **todo lo que no sirva para contactar la semana siguiente
espera a la fase siguiente**.

---

## Fase 0 — Decisiones

**Objetivo:** cerrar lo que bloquea en [06](./06_decisiones-abiertas.md). D1 (puente) cerrada el
2026-10-13: servidor MCP en `sales`. Queda D2 (permisos), que bloquea la Fase 3. D3 y D4 no bloquean.

**Criterio de éxito:** D2 decidida antes de empezar la Fase 3.

---

## Fase 1 — Núcleo del CRM en `sales`

**Rama:** `feat/sales-crm` · **Repos:** `encodebiz-api`

- Migración `031_sales_crm.sql` ([03](./03_modelo-de-datos.md)); aplicada en `encodebiz_staging`.
- Dominio, casos de uso y repositorios ([TDR-001](./tdr/TDR-001-dominio-y-capas-en-sales.md)).
- `crm.router.ts` montado con `crmAccess` antes de `hiddenApiKey`, con actor obligatorio
  ([TDR-002](./tdr/TDR-002-superficie-interna-y-actor.md)). En esta fase solo `ENCODEBIZ_API_KEY`.
- Esquemas en `crm.schemas.ts` como *shapes* de zod, listos para que el MCP los reutilice.
- Todas las rutas de [04](./04_contratos-api.md) salvo `POST /import`.
- Tests `node --test` de los casos de uso: transiciones, `profile_required`,
  `contact_opted_out`, duplicados, promoción de lead tras borrado por retención.

**Estado (2026-10-13):** hecha y desplegada en desarrollo; migración `031` aplicada en
`encodebiz_staging`; criterio de éxito comprobado contra `api-staging.checkbiz360.com`.

**Criterio de éxito:** en desarrollo, con `curl`, se crea una cuenta, se intenta registrar un
contacto saliente y devuelve `409 profile_required`; se guarda el perfil y entonces pasa.

---

## Fase 2 — El agente

**Rama:** `feat/sales-crm-mcp` · **Repos:** `encodebiz-api`, plugin

- `SALES_CRM_AGENT_KEY` y su límite de peticiones ([TDR-002](./tdr/TDR-002-superficie-interna-y-actor.md)).
- Servidor MCP en `POST /api/v1/sales/crm/mcp` con las 11 herramientas ([TDR-003](./tdr/TDR-003-servidor-mcp-y-plugin-cowork.md)).
- `@modelcontextprotocol/sdk@1.32.1` y `zod` a `^3.25.0` en `services/sales/package.json`.
- Plugin de Cowork `checkbiz360-gtm` con las 7 skills, empezando por `contexto-checkbiz360`,
  `investigar-cuenta` y `crm`.

**Estado (2026-10-13):** servidor MCP desplegado en desarrollo con `SALES_CRM_AGENT_KEY`
propia; el plugin vive en `encodebiz-api/plugins/checkbiz360-gtm/` con las 7 skills y los
cuatro ficheros de nicho.

**Criterio de éxito:** desde Cowork, Jose investiga 10 empresas de limpieza, quedan en el CRM
en `researched` con perfil y fuentes, y la agenda del día sale de `GET /next-actions`.

---

## Fase 3 — Backoffice

**Ramas:** `feat/backoffice-crm` · **Repos:** `encodebiz-api` (`services/backoffice`, `apps/backoffice-web`)

- `SalesClient` ampliado, `crm.router.ts` en el backoffice, permisos `crm:*`
  ([TDR-004](./tdr/TDR-004-backoffice-proxy-permisos-y-paginas.md)).
- Páginas Pipeline y Cuenta. Botón «Pasar a cuenta» en `LeadsPage`.

**Criterio de éxito:** un `editor` ve el pipeline y registra una actividad; no puede reasignar
dueño.

---

## Fase 4 — Volumen y medición

**Rama:** `feat/sales-crm-senales`

- `POST /import` y la cascada de enriquecimiento ([TDR-005](./tdr/TDR-005-importacion-enriquecimiento-y-senales.md)).
- Fuentes de señales automáticas, empezando por licitaciones.
- `sales_lead_qualified` a GA4 y Google Ads ([ADR-007](./adr/ADR-007-sales-lead-qualified-lo-emite-el-crm.md)).
- Retención del CRM en el barrido, si D4 se cierra.

**Estado (2026-10-13):** `POST /import` (simula salvo `apply=1`, transacción por lote) con su
diálogo en el backoffice; `sales_lead_qualified` a GA4 (migración `032`), Ads directo pendiente
de crear la acción de conversión; señales automáticas tras la verificación de
[07](./07_verificacion-fuentes-senales.md). Retención (D4) sin tocar: pide la LIA.

**Criterio de éxito:** una importación de Apollo de un nicho entra en simulación, se revisa y
se aplica sin duplicados; el evento cualificado aparece en GA4 DebugView.

---

## Lo que exige cada entorno

| | Desarrollo | Producción |
|---|---|---|
| Migración `031` | A mano por SSH en `encodebiz_staging` | A mano, sola, mirando el resultado |
| `SALES_CRM_AGENT_KEY` | `.env.staging` | `.env.production` (no se commitea) |
| Plugin | `.mcp.json` apuntando a `api-staging.checkbiz360.com` | Apuntando a `api.checkbiz360.com`, con su propia clave |
| nginx | Nada: `/api/v1/sales/` ya está publicado | Ídem |

---

## Pase a producción — 2026-10-14

Solo el CRM, por PR #147 (`release/crm-prod` → `main`, rama montada desde `main` con las rutas
del CRM tal como estaban validadas en staging). Fuera, a propósito: inventario ADR-009
(migración `034`), script de apuntes espejados y `firestore.rules`.

1. Migraciones `031`, `032` y `033` aplicadas a mano en `encodebiz_analytics`, una a una y
   comprobando cada una (los 8 leads, intactos).
2. `SALES_CRM_AGENT_KEY` propia de producción en `.env.production`
   (copia `.env.production.bak-2026-10-14-crm`); la local, en `secrets/crm-agent-key-prod.md`.
3. Merge del PR → *Production CI/CD* en verde; desplegado `f791ea6`.
4. Comprobado solo con lecturas: el CRM da 404 sin clave y con la del agente, el MCP da 404
   con la de plataforma y publica 11 herramientas con la del agente, pipeline vacío,
   backoffice 200, leads de la landing intactos, `sales` y `backoffice` sanos.

Queda apagado en producción: el barrido de la PLACSP (`CRM_PLACSP_SWEEP`). El evento
`sales_lead_qualified` sale a GA4 con la configuración de GA4 que ya tiene producción.

---

## Fase 6 — Merlin investiga (2026-10-16)

**Rama:** `feat/crm-investigacion-merlin` · **Diseño:** [ADR-009](./adr/ADR-009-merlin-investiga-en-el-servidor.md),
[TDR-007](./tdr/TDR-007-investigacion-con-merlin.md), [08](./08_el-prompt-de-investigacion.md)

- Merlin investiga con la API de OpenAI y búsqueda web; `sales` guarda solo lo que tiene
  prueba en una página consultada. Migración `038` (`sales_research_runs`).
- Botón «Investigar con Merlin» en la ficha y script `investigar-merlin.js` (simula por
  defecto). Cola diaria apagada (`CRM_INVESTIGACION`) hasta la prueba de 10.

**Primera ejecución real (2026-10-16, Serlimar, en seco):** 13 búsquedas, identidad confirmada
por CIF en tres fuentes, dossier correcto, 81 s, ~3 céntimos. Salió `insuficiente` porque las
anotaciones de cita de la API llegan vacías con `gpt-5-mini`; corregido pidiendo las fuentes
de la búsqueda (`include`). La regla hizo lo que debía: ante la duda, no guardar.

**Prueba de 10 (2026-10-16, en seco, `gpt-5-mini`):** 9 de 10 con perfil; identidad
confirmada en las 10; GESPROLIM salió `insuficiente` (identificada, sin dolor con prueba).
Entre 6 y 25 búsquedas y ~5 céntimos por empresa. Comparadas con las de Claude: correctas y
mejor documentadas en fuentes, menos afiladas en el gancho (Claude encuentra el detalle que
engancha; Merlin se queda en el dolor del nicho probado). Siguiente: probar el modelo grande
en dos cuentas y decidir.

**Ajustes del CRM** ([TDR-008](./tdr/TDR-008-ajustes-del-crm.md)): los topes diarios
(empresas nuevas por licitaciones, investigaciones) y el resto de la configuración pasan a
editarse en el panel, sin redesplegar.

**Criterio de éxito:** las 10 cuentas de limpieza investigadas por Claude, reinvestigadas en
seco por Merlin, y Jose decide con las dos delante si la calidad basta y con qué modelo.

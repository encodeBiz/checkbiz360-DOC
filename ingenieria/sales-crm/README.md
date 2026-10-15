# CRM de ventas de CheckBiz360 y agente Go-to-Market — Documento de Ingeniería

**Proyecto:** encodebiz-api
**Dominio:** `services/sales` — CRM comercial de CheckBiz360
**Fecha de inicio:** 2026-10-13
**Estado:** Diseño, sin código. ADRs 001, 003 y 005 aceptados; el resto propuestos hasta que Jose los cierre (ver [06](./06_decisiones-abiertas.md))
**Autor:** Jose Acevedo

---

## Contexto y Motivación

CheckBiz360 tiene producto suficiente para vender. Lo que falta es el sistema que convierte
un mercado en conversaciones: saber **cuántas empresas** hay en cada nicho, **cuál** toca
ahora y **por qué ahora**, **quién** decide en ella y **qué decirle** en su idioma.

Hoy `services/sales` sabe recibir un formulario, filtrar el spam y medir la conversión en GA4
y Google Ads. No sabe nada de lo que pasa después ni de las empresas que todavía no han
escrito. Su propio README lo deja dicho: *«`accepted` no es `cualificado` (…) será otro evento
posterior —`sales_lead_qualified`— alimentado desde el CRM»*. Ese CRM no existe.

## Principio de diseño

> **La oportunidad nace en la señal, no en el lead. Y nadie contacta a una empresa que no
> conoce.**

De ahí salen las tres decisiones que gobiernan el resto:

1. **El CRM es parte de `sales`.** Un solo dueño del dato comercial, en Postgres, junto a los
   leads que ya guarda. El backoffice y el agente lo piden por HTTP; ninguno toca sus tablas.
2. **La empresa (cuenta) es la unidad**, no el lead. El lead de la landing es una forma más de
   que una cuenta entre en el embudo; la señal y la importación son las otras.
3. **El agente prepara y la persona envía.** Claude investiga, perfila, detecta señales y
   redacta; el contacto lo hace un humano.

## Alcance

**Dentro:** cuentas, contactos, señales, perfil de cuenta, actividad, etapas del embudo SDR → AE,
próxima acción; promoción de un lead a cuenta; importación por CSV; API interna en `sales`;
servidor MCP en `sales` para el agente; plugin de Cowork con 7 skills; páginas de Pipeline y Cuenta en el
backoffice interno; evento `sales_lead_qualified`.

**Fuera (explícitamente):** envío automático de emails o mensajes de LinkedIn; secuencias
programadas; previsión de ingresos; multi-producto (solo CheckBiz360); cualquier cambio en la
app o el panel del cliente.

**Nichos de partida:** construcción, limpieza, SAD (ayuda a domicilio) y eventos (Rentman).
Limpieza es el que más resultado está dando (Jose, 2026-10-13).

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | Qué hay hoy en `sales` y en el backoffice, y qué se reutiliza |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Quién habla con quién, embudo y reparto SDR / AE |
| 03 | [Modelo de datos](./03_modelo-de-datos.md) | Tablas de la migración `031`, estados y reglas |
| 04 | [Contratos de API](./04_contratos-api.md) | Rutas `/api/v1/sales/crm/*`, auth, request/response |
| 05 | [Fases de implementación](./05_fases.md) | Orden por uso: primero lo que permite vender |
| 06 | [Decisiones abiertas](./06_decisiones-abiertas.md) | Lo que falta por responder antes o durante la implementación |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-el-crm-vive-en-sales.md) | El CRM vive en `services/sales`; backoffice y agente lo piden por HTTP | Aceptado |
| [ADR-002](./adr/ADR-002-la-cuenta-es-la-unidad-el-lead-una-entrada.md) | La cuenta es la unidad; el lead es una forma de entrar | Propuesto |
| [ADR-003](./adr/ADR-003-sin-perfil-no-hay-contacto.md) | Sin perfil de cuenta reciente no se registra ningún contacto saliente | Aceptado |
| [ADR-004](./adr/ADR-004-la-oportunidad-nace-en-la-senal.md) | Las señales son entidad propia, con caducidad; la cuenta lleva entrar / crecer / proteger | Propuesto |
| [ADR-005](./adr/ADR-005-el-agente-habla-con-sales-por-mcp-propio.md) | El agente habla con `sales` por un servidor MCP propio, con una clave que solo abre `/crm/mcp` | Aceptado |
| [ADR-006](./adr/ADR-006-claude-prepara-la-persona-envia.md) | Sin envío automático: Claude prepara, la persona envía | Propuesto |
| [ADR-007](./adr/ADR-007-sales-lead-qualified-lo-emite-el-crm.md) | `sales_lead_qualified` lo emite el CRM al entrar en conversación | Propuesto |
| [ADR-008](./adr/ADR-008-acciones-planificadas-por-contacto.md) | Acciones planificadas por contacto; la etapa sigue siendo de la empresa | Aceptado |

## Technical Design Records (TDRs)

| ID | Diseño | Fase |
|----|--------|------|
| [TDR-001](./tdr/TDR-001-dominio-y-capas-en-sales.md) | Dominio, casos de uso y repositorios del CRM dentro de `sales` | 1 |
| [TDR-002](./tdr/TDR-002-superficie-interna-y-actor.md) | Montaje de `/crm`, las dos claves, el actor y la validación | 1–2 |
| [TDR-003](./tdr/TDR-003-servidor-mcp-y-plugin-cowork.md) | Servidor MCP del CRM en `sales` y plugin de Cowork (7 skills) | 2 |
| [TDR-004](./tdr/TDR-004-backoffice-proxy-permisos-y-paginas.md) | `SalesClient`, permisos `crm:*` y páginas Pipeline / Cuenta | 3 |
| [TDR-005](./tdr/TDR-005-importacion-enriquecimiento-y-senales.md) | Importación CSV, enriquecimiento en cascada y fuentes de señales | 4 |
| [TDR-006](./tdr/TDR-006-acciones-planificadas.md) | Acciones planificadas: modelo, reglas, API, MCP y panel | 5 |

## Referencias

- `encodebiz-api/services/sales/README.md` — el servicio tal como está
- `encodebiz-api/migrations/004_sales.sql`, `005`, `019`, `020`, `029`, `030` — esquema de `sales_leads`
- `encodebiz-api/services/backoffice/src/application/staff/permissions.ts` — permisos del personal

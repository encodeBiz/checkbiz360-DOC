# TDR-006 — Acciones planificadas

**Fecha:** 2026-10-15
**Estado:** En implementación
**Decisión:** [ADR-008](../adr/ADR-008-acciones-planificadas-por-contacto.md)

---

## 1. Modelo (migración `036`)

`sales_planned_actions`: `id`, `account_id` (FK), `contact_id` (FK, nulo = con la empresa),
`type` (los de actividad), `title` (una línea: «InMail de presentación»), `draft` (texto),
`due_at`, `status` (`pending`/`done`/`skipped`), `activity_id` (la actividad que la cerró),
`skip_reason`, `created_by`, `created_at`, `completed_by`, `completed_at`.
Índices: pendientes por fecha, por contacto y por cuenta.

## 2. Casos de uso

| Caso | Reglas |
|---|---|
| `PlanAction` | Cuenta existe y no está perdida; contacto de esa cuenta y sin oposición; si el tipo es un contacto saliente (todo salvo `note`): perfil vigente y, si es `email`, permitido (D5) |
| `UpdateAction` | Solo pendientes: fecha, título, borrador |
| `CompleteAction` | Solo pendientes. Registra la actividad (`direction: outbound`, o `internal` si es `note`) con `LogActivity` en la misma transacción; resumen = el dado o el título + borrador |
| `SkipAction` | Solo pendientes; motivo obligatorio |
| `ListActions` | Filtros: estado, `due` (`overdue`/`today`/`week`/`all`), cuenta, contacto, dueño |

`LogActivity` se parte en un núcleo que recibe los repositorios (para usarse dentro de otra
transacción) y la envoltura de siempre.

## 3. Estado de contacto (derivado)

`overdue` si tiene una pendiente con fecha pasada; `pending` si tiene alguna; si no,
`replied` si alguna vez escribió (actividad entrante); `contacted` si se le escribió;
`untouched` si nada. En la lista de contactos es columna y filtro (`state`).

## 4. API y MCP

HTTP: `POST /accounts/:id/actions`, `GET /actions`, `PATCH /actions/:id`,
`POST /actions/:id/complete`, `POST /actions/:id/skip`. La ficha de cuenta y la de contacto
traen sus pendientes; el listado de cuentas, `pendingActions`, `overdueActions` y
`nextPlannedAt`. `GET /next-actions` añade `plannedActions`.

MCP: `crm_plan_action`, `crm_list_actions`, `crm_update_action`, `crm_complete_action`,
`crm_skip_action`.

## 5. Panel

Página **Pendientes** (bloque Comercial): acciones por fecha, con «Hecho» y «Descartar».
En la cuenta y en la ficha de contacto, sus acciones y «Planificar». En el pipeline, columna
de pendientes; en Contactos, estado de contacto.

# TDR-004 — Backoffice: proxy, permisos y páginas

**Fecha:** 2026-10-13
**Estado:** En implementación (D2 decidida el 2026-10-13)
**Componentes:** `services/backoffice`, `apps/backoffice-web`

---

## 1. `SalesClient`

`services/backoffice/src/infrastructure/clients/SalesClient.ts` gana un método por ruta del CRM.
Mismo patrón que `findLeads`: `ENCODEBIZ_API_KEY`, `404` traducido a `sales_s2s_unauthorized`.
Novedad: las escrituras reciben el `staffUid` y lo mandan como `X-Encodebiz-Actor: staff:<uid>`.

Los errores de negocio de `sales` (`409 profile_required`, `invalid_transition`…) se propagan
al panel con el mismo código, para que la pantalla diga qué falta.

## 2. Permisos

Propuesta (D2), en `application/staff/permissions.ts`:

| Permiso | root | admin | editor |
|---|---|---|---|
| `crm:read` | sí | sí | sí (en `READ_ONLY`) |
| `crm:write` | sí | sí | sí |
| `crm:assign` | sí | sí | no |

## 3. Rutas del backoffice

`modules/crm.router.ts`, montado en `backofficeRouter.use("/crm", crmRouter)`. Hereda
`requireStaff` y `auditTrail`. Cada ruta con `requirePermission(...)` y `describeAction(...)`,
como `leads.router.ts`. Es un proxy: valida la forma, pone el actor y llama a `SalesClient`.

## 4. Páginas

| Página | Ruta | Contenido |
|---|---|---|
| `PipelinePage.tsx` | `/crm` | Tabla filtrable por nicho, etapa y dueño; contadores por etapa; columna de señal viva y próxima acción |
| `AccountPage.tsx` | `/crm/:id` | Datos, perfil vigente con fuentes, señales, contactos, actividad, próxima acción; cambio de etapa |
| `LeadsPage.tsx` | `/leads` | Botón «Pasar a cuenta» en los `accepted` (`POST /leads/:id/promote`) |

MUI y `useApi`, como el resto del panel. Sin kanban en esta fase.

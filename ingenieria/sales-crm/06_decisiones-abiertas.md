# 06 — Decisiones abiertas

---

## D1 — Puente entre Cowork y `sales`

**Estado:** **decidida el 2026-10-13** por Jose: servidor MCP propio dentro de `sales`
([ADR-005](./adr/ADR-005-el-agente-habla-con-sales-por-mcp-propio.md)). Se descartó n8n por duplicar esquemas, sacar datos personales a un tercero
y no estar centrado en CheckBiz360.

## D2 — Permisos en el backoffice

**Bloquea:** nada. **Estado:** decidida el 2026-10-13: se aplica la propuesta tal cual
(Jose: «lo que mejor veas»). `crm:read` en `READ_ONLY`, `crm:write` para los tres roles,
`crm:assign` solo `root` y `admin`.

Reutilizar `leads:read` / `leads:write` o crear `crm:read` / `crm:write`. Propuesta: crear
`crm:*` con el mismo reparto que `leads:*` (el editor lee y escribe), más `crm:assign` solo para
`root` y `admin`. Razón: el CRM guarda datos de personas que no han escrito a encodeBiz; mezclar
el permiso con el de los leads haría imposible separarlos después sin tocar roles.

## D3 — Unidad comercial frente a entidad

**Bloquea:** nada (afecta a `trial` y `won`). **Estado:** sin decidir.

¿Una entidad de CheckBiz360 (`entity_id`) es siempre una cuenta del CRM, o un grupo con varias
razones sociales es una sola cuenta? El modelo admite hoy una entidad por cuenta.

## D4 — Retención de prospectos

**Bloquea:** nada (Fase 4). **Estado:** propuesta en [03 §Retención](./03_modelo-de-datos.md#retención).

Requiere además la evaluación de interés legítimo (LIA) documentada fuera de este repo.

## D5 — Base legal del email en frío

**Bloquea:** el uso de `type = email` saliente a contactos que no hayan escrito antes.
**Estado:** pendiente de revisión legal.

El art. 21 de la LSSI exige consentimiento previo para comunicaciones comerciales por correo
electrónico salvo relación contractual previa. Hasta que haya criterio legal, el agente redacta
emails solo para contactos `lawful_basis = consent` o que vinieron de un lead; para el resto,
LinkedIn y teléfono. Ver [ADR-006](./adr/ADR-006-claude-prepara-la-persona-envia.md).

**Aplicación (decidido el 2026-10-13):** la regla vive en el servidor, no solo en la skill, por
la misma razón que [ADR-003](./adr/ADR-003-sin-perfil-no-hay-contacto.md): desde el backoffice se
la saltaría cualquiera. `LogActivity` rechaza con **409 `email_not_allowed`** una actividad
`type = email`, `direction = outbound` si el contacto tiene `lawful_basis = legitimate_interest`
**y** no tiene ninguna actividad `inbound` registrada (nunca nos ha escrito). Una actividad
saliente de email exige por eso `contactId`.

`PromoteLead` registra el formulario de la landing como actividad `note` / `inbound` del contacto
(sin `outcome`, así que no mueve etapa): quien vino de un lead queda habilitado por el mismo
criterio, sin un caso especial. Cuando haya criterio legal, `CRM_COLD_EMAIL_ALLOWED=true` levanta
la regla sin tocar código.

## D6 — Posicionamiento en la documentación pública

**Bloquea:** nada. **Estado:** resuelta el 2026-10-13 para el agente: la skill toma el
posicionamiento de `DOCS/MARKETING/nichos-prioritarios-checkbiz360.md` (decisión del
2026-09-21, «capa de ejecución en campo») y los precios del 91; la página 01 no se usa como
fuente. Sigue pendiente corregir la propia página pública.

`DOCS/Clients/01-primeros-pasos/01-que-es-checkbiz360.md` abre con «plataforma SaaS de control
horario», y Jose posiciona CheckBiz360 como control operativo de campo. La skill no puede tomar
esa página como fuente mientras diga lo contrario.

## D7 — Fuentes de señales

**Bloquea:** nada. **Estado:** verificada el 2026-10-13 ([07](./07_verificacion-fuentes-senales.md)):
PLACSP implementada; BORME para una segunda fase; portales de empleo descartados.

Candidatas: Plataforma de Contratación del Sector Público (licitaciones), BORME (constituciones
y cambios de administradores), portales de empleo (ofertas de personal de campo). Antes de
diseñar la ingesta hay que confirmar, para cada una, formato de acceso, condiciones de uso y si
permite filtrar por CNAE o por objeto del contrato.

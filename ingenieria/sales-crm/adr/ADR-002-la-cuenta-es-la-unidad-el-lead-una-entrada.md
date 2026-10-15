# ADR-002 — La cuenta es la unidad; el lead es una forma de entrar

**Fecha:** 2026-10-13
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

`sales_leads` guarda intentos de formulario, incluidos los rechazados, y los borra por
retención (730 días los aceptados). Una empresa puede escribir dos veces, o no escribir nunca y
llegar por una señal.

## Decisión

- La unidad del CRM es la **cuenta** (empresa). El contacto cuelga de ella.
- Una cuenta entra por cuatro vías (`source`): `lead`, `outbound`, `import`, `referral`.
- **Promover** un lead copia sus datos a cuenta y contacto y guarda `lead_id` con
  `ON DELETE SET NULL`.
- La deduplicación es por CIF y por dominio. Promover un lead de una empresa que ya existe lo
  enlaza a esa cuenta.

## Por qué

- Vender B2B es vender a una empresa, con varias personas dentro.
- Copiar en vez de referenciar hace que la retención de leads no rompa el CRM.
- No se toca `sales_leads` ni su secuencia (Google Ads usa el id como `order_id`).

## Consecuencias

- Un lead sin empresa (`company` nulo y email de dominio genérico) se promueve con el nombre de
  la persona como nombre provisional de cuenta y `domain` nulo.
- `LeadsPage` gana un botón «Pasar a cuenta» (Fase 3).

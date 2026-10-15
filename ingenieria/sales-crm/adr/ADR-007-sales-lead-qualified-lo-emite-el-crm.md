# ADR-007 — `sales_lead_qualified` lo emite el CRM

**Fecha:** 2026-10-13
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

Google Ads puja hoy por `sales_lead_accepted`: un formulario que ha pasado el antispam. El README
de `sales` ya advierte que eso no es un lead cualificado y que esa señal tendría que venir del CRM.

## Decisión

Cuando una cuenta con `source = lead` pasa a `conversation`, `sales` emite
`sales_lead_qualified` a GA4 (Measurement Protocol) y a Google Ads (Data Manager API) por las
mismas piezas que ya usa para `sales_lead_accepted`, con el mismo `client_id`, el mismo
consentimiento y el `lead_id` original.

- Una vez por lead. Se anota el resultado, como `ga_status` y `ads_status`.
- Sin consentimiento de marketing, `skipped`.
- Si el lead ya se borró por retención (`lead_id` nulo), no se emite.

## Consecuencias

- Pasa a ser posible usar `sales_lead_qualified` como conversión principal en Ads. Cambiarlo es
  una decisión de campaña, fuera de este ADR.
- El resultado se anota en `sales_lead_qualifications` (migración `032`), una fila por lead:
  la clave primaria es la garantía de «una vez por lead».

## Implementación (2026-10-13)

- **GA4: hecho.** `application/crm/reportQualifiedLead.ts`, llamado por `LogActivity` después
  de confirmar la transacción. La fecha del evento es la de la cualificación (GA4 descarta
  eventos de más de 72 horas). `SALES_GA4_QUALIFIED_EVENT_NAME` y `SALES_GA4_QUALIFIED_VALUE`.
- **Google Ads directo: pendiente.** La Data Manager API sube a UNA acción de conversión
  (`SALES_ADS_API_CONVERSION_ACTION_ID`, hoy la de leads aceptados). Para el cualificado hace
  falta crear otra acción en la cuenta, que es decisión de campaña. Mientras, el evento de GA4
  puede importarse en Ads como conversión.

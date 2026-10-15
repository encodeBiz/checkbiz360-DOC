# ADR-001 — El CRM vive en `services/sales`

**Fecha:** 2026-10-13
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («el CRM back hay que meterlo en el servicio de sales»)

---

## Contexto

Hacen falta cuentas, contactos, señales y actividad. Hay tres sitios posibles: un servicio
nuevo, el backoffice, o `sales`.

## Decisión

El CRM es parte de `services/sales`: mismas tablas `sales_*` en la misma base, mismos
casos de uso, misma superficie interna. El backoffice y el agente lo piden por HTTP.

## Por qué

- **Un dueño del dato comercial.** El lead y la cuenta son el mismo embudo. Partirlos en dos
  servicios obligaría a sincronizar la promoción de un lead y la medición de
  `sales_lead_qualified` entre ellos.
- **El precedente ya está escrito.** `SalesClient.ts` del backoffice: *«El backoffice no habla
  con `sales_leads` por su cuenta aunque comparta la misma base (…) así un cambio en el modelo
  de leads no se queda a medias en dos sitios»*. Vale igual para el CRM.
- **La superficie interna existe** (`hiddenApiKey`, 404 sin clave) y la medición en GA4 y Ads
  también.

## Alternativas descartadas

- **Servicio `crm` nuevo:** un contenedor, un puerto y un bloque de nginx más para un dominio que
  comparte datos con `sales`.
- **Dentro del backoffice:** el agente tendría que pasar por la puerta del personal
  (`requireStaff`), pensada para personas, y las reglas del dominio vivirían en el panel.
- **Módulo en Firestore:** el resto de `sales` está en Postgres y el CRM se consulta por
  agregados (pipeline por etapa y nicho), que es lo que Postgres hace bien.

## Consecuencias

- `sales` deja de ser solo captación. Su README se actualiza al cerrar la Fase 1.
- Toda regla del CRM se escribe una vez, en los casos de uso de `sales`.

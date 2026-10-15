# ADR-004 — La oportunidad nace en la señal

**Fecha:** 2026-10-13
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

De las notas de la reunión del 2026-10-13: *«el cuándo es muy importante», «hay que identificar
señales», «decisiones entrar, crecer o proteger», «la oportunidad nace antes que el lead, nace
en las señales»*.

## Decisión

- La señal es **entidad propia** (`sales_signals`), no un campo de texto en la cuenta.
- Toda señal lleva **fuente** (`source_url`) y **caducidad** (`expires_at`). Una señal caducada
  deja de contar como «viva» en el pipeline y en la agenda.
- La cuenta lleva **`motion`**: `enter` (abrir cuenta o nicho), `grow` (ampliar en un cliente:
  más sucursales, Inventario, RentmanBiz), `protect` (cliente con señal de riesgo).

## Por qué

- Sin caducidad, una licitación de hace un año sigue pareciendo un motivo para escribir.
- Sin fuente, una señal es una suposición, y el mensaje que se apoya en ella no se puede
  defender ante el cliente.
- `motion` separa las tres conversaciones, que no se parecen: entrar se gana con el dolor,
  crecer con el uso y proteger con el servicio.

## Consecuencias

- La skill `senales` fija una caducidad por defecto según el tipo (en su `references/`).
- `GET /accounts` devuelve `liveSignals`; la agenda prioriza cuentas con señal viva `high`.

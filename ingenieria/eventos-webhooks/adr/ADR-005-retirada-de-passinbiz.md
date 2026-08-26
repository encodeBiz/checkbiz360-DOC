# ADR-005 — Retirada completa de los eventos de passinbiz

**Fecha:** 2026-08-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Doce de los catorce eventos del catálogo son de passinbiz: `pass.*`, `credential.*` y
`validation.*`. El producto está descontinuado y en proceso de eliminación de la plataforma.

## Decisión

Se retira el catálogo entero de passinbiz, sin periodo de gracia y sin comprobar suscriptores.

## Consecuencias

Cuatro puntos de código, y el cuarto es el que se olvida:

1. `services-saas/passinbiz/webhook-events.ts` — borrar.
2. `functions/src/index.ts` — quitar el import; el registro es por efecto de import.
3. `ValidatePass.ts` y `createPassOnDemand.controller.ts` — quitar las llamadas a
   `emitPassEvent`.
4. `core/firebase-entry-schedule/mailer/email-worker.ts` — llama a `publishEvent`
   **directamente**, sin el helper tipado, con `pass.sent` / `credential.sent` y sus `.failed`.
   Si se borra el catálogo sin tocar esto, `publishEvent` lanza en cada email enviado.

El registry queda con los dos eventos de asistencia hasta que empiece la oleada 2.

# ADR-003 — Sin perfil de cuenta reciente no hay contacto saliente

**Fecha:** 2026-10-13
**Estado:** Aceptado — revisado el 2026-10-28
**Decisionario:** Jose Acevedo («investigar los clientes, nunca contactar sin conocer al cliente»)

> **Revisión 2026-10-28** ([TDR-010 §7](../tdr/TDR-010-historial-y-cierre-de-acciones.md)): la regla
> se queda en **planificar**, no en **registrar**. Muchas acciones se hacen en caliente (una
> reunión, un evento) y se pasan al CRM después; bloquear el registro dejaba la empresa en
> «Señal» y el historial incompleto. Registrar lo que ya pasó nunca se bloquea por falta de
> perfil: se guarda, la etapa avanza y la cuenta se marca en rojo como «contactada sin
> investigar». Jose: «se hacen acciones en caliente que después deben pasarse al CRM, por
> ejemplo en reuniones».

---

## Contexto

Un mensaje genérico a un jefe de obra o a una gerente de SAD se ignora. El que funciona habla de
su operativa, en su jerga y del dolor que tiene ahora. Eso exige haber investigado antes.

## Decisión

Una actividad `direction = outbound` solo se registra si la cuenta tiene un perfil con
`researched_at` dentro de los últimos `CRM_PROFILE_MAX_AGE_DAYS` (90 por defecto). Si no,
**409 `profile_required`**.

La regla vive en el caso de uso `LogActivity`, no en el panel ni en el plugin: vale igual
venga de donde venga la llamada.

## Por qué en el servidor

Si la regla estuviera en el plugin, un registro desde el backoffice se la saltaría; y al revés.
Es la misma razón por la que el resto de reglas del dominio viven en los casos de uso.

## Consecuencias

- El perfil es obligatorio y versionado (`sales_account_profiles`).
- La skill `outreach` pide el perfil vigente antes de redactar; si no existe, llama primero a
  `investigar-cuenta`.
- Las actividades `inbound` e `internal` no exigen perfil: responder a quien escribe no espera.

# ADR 0001 — Sync bidireccional por polling, sin webhooks

- **Estado:** Aceptada (planificación)
- **Fecha:** 2026-07-26
- **Contexto:** integración Rentman ↔ encodeBiz (ver `../README.md`).

## Contexto

La integración debe ser **bidireccional**: los clientes que ya usan Rentman siguen
operando allí, y encodeBiz es la cabina de gestión. Hay que propagar cambios en ambos
sentidos (clientes/proyectos, asignaciones, horas). Rentman ofrece dos mecanismos para
enterarse de cambios en su lado: **webhooks** (push en tiempo real) y **polling** de la
REST API.

## Decisión

Hacemos el sync **por polling** desde el servicio `sync`, con un job programado.
**No usamos webhooks.**

## Razones

- **Control del ritmo.** Nosotros decidimos la cadencia; no dependemos de que Rentman
  nos entregue eventos. Importa porque Rentman corta por rate-limit (403) con un techo
  no documentado.
- **Idempotente y sin pérdida.** Si una pasada falla o nos cortan, la siguiente retoma.
  Con webhooks, un evento perdido es un desincronizado silencioso.
- **Menos superficie.** Sin endpoint público, sin secret de webhook por tenant, sin
  exponer entrada. Menos que asegurar y mantener.
- **Auditable.** Cada pasada deja rastro en `rentman_sync_log` de qué se reconcilió y en
  qué sentido — relevante porque tocamos horas legales.

## Consecuencias

- **No es tiempo real:** la latencia es el intervalo de sondeo. Aceptable para este dominio.
- **Consume presupuesto de rate-limit** de forma continua → la cadencia depende de medir
  el límite real (Fase 0, F0-1) y de si Rentman permite filtrar por `modified` (F0-2).
- Prevención de bucles vía `updateHash` + `updatedAt` por lado (ver `../02_to-be.md` §3).
- El stub de webhook del esqueleto queda **aparcado**, no es la vía.

## Alternativa descartada

**Webhooks:** tiempo real, pero entrega no garantizada, requiere endpoint público +
gestión de secret por tenant, y cede a Rentman el control del ritmo. Rechazada por
control y robustez.

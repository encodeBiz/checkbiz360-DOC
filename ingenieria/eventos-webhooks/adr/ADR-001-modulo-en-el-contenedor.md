# ADR-001 — El módulo de eventos se rehace en `encodebiz-api`, no se amplía en el SaaS

**Fecha:** 2026-08-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Existe un módulo de webhooks salientes funcionando en `encodeBiz-SAAS/functions/src/core/webhook`:
registry, firma HMAC, outbox, worker con backoff, dead-letter y gestión de endpoints. Está bien
construido y documentado.

Hay que multiplicar el catálogo de catorce eventos a unos cincuenta, y la mayor parte de las
acciones que deben emitirlos ya no se ejecutan en Firebase: fichajes, tareas, documentos,
empleados e informes viven en servicios Express del contenedor.

Además, `encodeBiz-SAAS` es un repositorio en retirada: la dirección declarada es traerlo todo
a `encodebiz-api` y descontinuar el otro.

## Decisión

El módulo se **rehace en `encodebiz-api`**. El núcleo va a `packages/shared/src/events` y la
gestión a un servicio `services/events`. En `encodeBiz-SAAS` no se escribe una línea nueva:
solo se le quita passinbiz y se despliega lo que ya estaba escrito.

## Razones

- **Donde está la acción.** Emitir desde el caso de uso exige que el emisor esté donde el caso
  de uso vive. Ampliar el módulo en Firebase obligaría a que cada escritura del contenedor
  llamara de vuelta a Firebase para emitir: un salto de red por evento, y un acoplamiento en la
  dirección contraria a la que va la plataforma.
- **Coherencia con la retirada.** Todo lo que se construya en el SaaS habrá que moverlo después.
- **Transaccionalidad.** Con la outbox en PostgreSQL, el evento se escribe en la misma
  transacción que el dato. En Firestore, desde otro proceso, no hay forma.

## Consecuencias

- Convivencia temporal: mientras queden emisores en Firebase, hay dos módulos vivos. Se acepta,
  acotado por [ADR-006](./ADR-006-firebase-sdk-residuo-transitorio.md).
- El contrato público no cambia, así que la convivencia es invisible para quien integra.
- La documentación del módulo original (`encodeBiz-SAAS/DOCS/modulos/webhooks`) queda como
  referencia histórica; la vigente es esta carpeta.

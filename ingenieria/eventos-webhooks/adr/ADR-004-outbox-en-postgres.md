# ADR-004 — La outbox y los endpoints, en PostgreSQL

**Fecha:** 2026-08-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Hoy ambos viven en Firestore, en subcolecciones por entidad, con un índice de grupo de
colección sobre `status` + `nextAttemptAt`. Funciona, pero: la outbox no se purga nunca, no hay
forma de escribir el evento en la misma transacción que un dato que vive en PostgreSQL, y el
panel no puede consultar el histórico de entregas con más de un filtro sin añadir índices.

## Decisión

`webhook_endpoint` y `webhook_delivery` pasan a **PostgreSQL**, en el esquema del contenedor,
con su migración numerada como el resto.

## Razones

- **Transacción única.** El caso de uso escribe el dato y la entrega a la vez. O las dos cosas
  o ninguna: se acaba el evento emitido de algo que luego falló al guardarse.
- **Purga trivial.** `DELETE ... WHERE status = 'delivered' AND created_at < now() - interval`.
  En Firestore es un job que recorre y borra documento a documento.
- **Consulta libre.** El panel necesita filtrar entregas por estado, evento, endpoint y fecha.
  En SQL es una consulta; en Firestore, un índice por combinación.
- **Coste.** Una entrega es una escritura y una lectura por intento. Con cincuenta eventos y
  fan-out, el volumen de operaciones en Firestore deja de ser despreciable.

## Consecuencias

- Los endpoints de gestión cambian de repositorio. El contrato HTTP no cambia.
- Hace falta una migración de los endpoints ya configurados en Firestore. La outbox no se
  migra: lo pendiente se drena antes del corte y lo entregado no vale nada.
- El emisor que quede en Firebase necesita alcanzar PostgreSQL. Lo hace por HTTP contra
  `services/events`, no con conexión directa.

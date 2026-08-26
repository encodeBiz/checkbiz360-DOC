# ADR-002 — El evento se emite en el caso de uso, no en un trigger

**Fecha:** 2026-08-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Hoy el único emisor es `onChecklogWebhook`, un trigger de Firestore que observa la colección de
checklogs y publica cuando ve la transición a `valid`. El patrón viene de que la app móvil
escribe directamente en Firestore: no había código propio en el camino donde emitir.

Eso ya no es cierto para la mayor parte del catálogo. Tareas, documentos, empleados, informes y
fichajes pasan por controladores y casos de uso del contenedor, y una parte creciente del dato
vive en PostgreSQL, donde no hay triggers que observar.

**Opción A — Trigger por colección.** Un trigger de Firestore por cada colección observada.
**Opción B — Emisión en el caso de uso.** Una llamada a `publish()` tras la escritura firme.

## Decisión

**Opción B.** El evento se emite en el caso de uso que escribe. El trigger queda como excepción
para escrituras que no pasan por el contenedor.

## Razones

- **Intención, no inferencia.** El caso de uso sabe *qué pasó*; el trigger solo ve un documento
  antes y después y tiene que deducirlo. `attendance.correction_accepted` y
  `correction_rejected` son dos caminos distintos del mismo controlador que producen un cambio
  de estado parecido: desde el caso de uso son dos líneas, desde un trigger es adivinar.
- **Cobertura.** Lo que se escribe en PostgreSQL no tiene trigger posible.
- **Coste.** Una función más por cada colección observada, invocada en cada escritura, emita o
  no emita.
- **Localidad.** El que añade una acción nueva ve la emisión al lado. Un trigger en otro
  repositorio se queda desactualizado sin que nadie lo note.

## Consecuencias

- Cada caso de uso gana una línea. Es trabajoso, pero mecánico y revisable.
- Riesgo de olvido: una acción nueva sin su `publish()`. Se mitiga con la tabla de
  correspondencia de [03](../03_catalogo-de-eventos.md) como lista de verificación.
- La emisión pasa a ser responsabilidad del dominio, no de la infraestructura. Es lo correcto:
  qué es un hecho de negocio lo decide el negocio.

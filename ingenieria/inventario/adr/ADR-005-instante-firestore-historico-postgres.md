# ADR-005 — Un solo camino de escritura; instante en Firestore, histórico en Postgres

**Fecha:** 2026-09-28 (revisado el mismo día)
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

La norma general de la plataforma es **Firebase para lo que necesita seguimiento en tiempo real
y exacto, Postgres para el resto**. Aplicarla al inventario pasó por tres posiciones, y merece
la pena dejarlas escritas porque la discusión volverá.

**A — El libro en Firestore, espejo a Postgres.** Movimiento y saldo juntos en una transacción
de Firestore.

**B — El libro en Postgres, proyección a Firestore.** Postgres nació para el histórico y la
trazabilidad; hace transacciones entre tablas mejor que Firestore y resuelve la concurrencia
del contador con un `UPDATE` con condición.

**A′ — A, decidida por el offline.** Primera versión de este ADR: se eligió A con el argumento
de que el operario trabaja sin cobertura y la persistencia offline de Firestore lo resolvía sin
complejidad. Ese argumento **era falso**: la app no escribe en Firestore para nada —todo va por
HTTP con Dio— y no tiene cola local. Además implicaba dos caminos de escritura para la misma
operación (el HTTP con validación y el directo sin nada), reglas de seguridad para siete
colecciones nuevas y un listener de larga vida en el contenedor. La revisión del 2026-09-28 lo
tumbó, con razón.

## Decisión

**Un solo camino de escritura, y Firestore para el instante por coherencia.**

- La app y el panel llaman a `inventory` por HTTP. **Nadie escribe en Firestore desde el
  cliente.**
- `inventory` escribe el movimiento y el saldo **juntos, en una transacción de Firestore**, y
  copia el movimiento a Postgres en la misma petición, a mejor esfuerzo.
- Firestore lleva el instante: maestros, saldos, agenda de ejemplares y material de las tareas
  abiertas. Postgres lleva el histórico: el libro completo, los informes, el coste y los
  cruces. **El libro es un informe más.**
- El trabajo sin conexión queda **fuera de v1** ([06 §D3](../06_decisiones-abiertas.md)).

## Justificación

**Un solo camino es el criterio que ya está fijado** para las escrituras sensibles: pasan por el
backend con autorización. Y con un solo escritor, la atomicidad entre movimiento y saldo deja de
ser un problema: no hay dos mitades que puedan desparejarse porque no hay dos escritores.

**Firestore para el instante es coherencia, no necesidad.** Con la escritura en servidor, la
posición B es técnicamente viable y hay que decirlo: Postgres podría llevar libro y saldo en una
transacción SQL y proyectar el número a Firestore. Se elige Firestore porque ahí vive el resto
del dominio de checkbiz, el panel lo lee en vivo, y meter la primera entidad de dominio en
Postgres haría de inventario el raro. Es una decisión revisable sin drama, y se toma sabiendo
que lo es.

## El movimiento es la verdad; el saldo es derivado

El saldo existe porque nadie quiere sumar cuatro años de apuntes para pintar una pantalla, no
porque sea el dato bueno. Si se desordena, se rehace desde el libro. Un job periódico recalcula
los saldos con actividad reciente y corrige la deriva dejándola registrada.

## El saldo puede quedar negativo

Dos cuadrillas gastan las últimas diez toallas y las dos apuntan diez. **Las dos dicen la
verdad**: el que estaba mal era el recuento. Se registran los dos movimientos, el saldo queda en
−10 y se marca `hasDiscrepancy`. Rechazar el segundo apunte sería borrar un gasto que ocurrió
y enseñar a la gente a no registrar consumos.

Por la misma razón, **la falta de existencias no bloquea una tarea**. Avisa. El recuento va a
estar mal durante meses —siempre lo está— y romper el trabajo de campo el primer día es la forma
más rápida de que el módulo se desinstale.

## La regla que gobierna la frontera

> **Lo que viaje entre los dos lados tiene que poder reconstruirse desde el otro.**

Es mejor regla que «Firestore para esto, Postgres para lo otro», porque dice qué pasa cuando la
copia falla: una inserción perdida en Postgres retrasa un informe hasta que el job la reintenta;
nunca pierde un apunte. Y de ahí la prohibición: **no se poda nada de Firestore hasta que el
espejo esté confirmado** (`mirrored: true`). En v1 no se poda de todos modos.

## Cuándo un movimiento deja de ser instante

Mientras la tarea del Lidl está abierta, «salieron 30, llevas 20 declaradas» es estado actual.
Cuando se valida y el sobrante se cuadra, ya no cambia nunca más.

> **Un movimiento es instante mientras su tarea está abierta, e histórico cuando se cierra.**

## Consecuencias

- El `id` del movimiento **lo genera la app**. No por el offline —que no hay— sino porque un
  reintento de red de Dio tiene que ser el mismo apunte. Mismo criterio que el `eventId` de
  `publish()`. Un solo mecanismo de idempotencia: dentro de la transacción, si el documento
  existe, se devuelve y no se toca nada.
- Las rutas de salida y consumo aceptan un `occurredAt` opcional. Hoy no lo manda nadie; está
  para que el offline, cuando llegue, no toque el contrato.
- El espejo a Postgres lo escribe `inventory`, no `sync`. Ver
  [TDR-004](../tdr/TDR-004-espejo-postgres-e-informes.md).
- No hay observador de Firestore, ni `appliedAt`, ni «último saldo conocido» en la app: todo
  eso era de A′ y se retira.

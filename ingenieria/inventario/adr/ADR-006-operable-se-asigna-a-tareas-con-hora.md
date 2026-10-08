# ADR-006 — El operable se asigna a tareas, con hora, no a obras por rango

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Al cuadrar maquinaria en construcción, el ejemplo natural es «el lunes tengo la excavadora en
Building A, el martes la muevo a B y el miércoles la uso». Building A suena a **obra**, no a
tarea, y si en esa obra hay quince tareas esa semana, obligar a asignar la máquina a las quince
es exactamente la fricción que el módulo viene a quitar.

Se valoraron dos formas de ocupar un operable:

**A — Ocupación por destino y rango.** La máquina se asigna a una obra o sucursal durante un
intervalo, y las tareas de dentro la usan sin volver a pedirla.

**B — Ocupación por tarea, con hora.**

## Decisión

**Opción B.** El operable se reserva **para una tarea**, con hora de inicio y fin.

## Justificación

Se puede tener **dos tareas con la misma máquina en el mismo edificio a horas distintas**. Con
ocupación por rango y destino, esas dos tareas son indistinguibles: el sistema no sabe cuál de
ellas tenía la fregadora a las nueve y cuál a las doce, y por tanto no puede imputar el uso ni
detectar que alguien las solapó.

Ligarla a la tarea es además lo que hace que el resto del modelo funcione sin esfuerzo: la tarea
ya lleva sucursal, empleados, geocerca y validación, así que el uso del operable hereda toda esa
atribución gratis.

## Consecuencias

**El choque se calcula por solapamiento real de intervalos**, no por día. La misma fregadora
puede aparecer en dos tareas del mismo martes sin conflicto, igual que una persona. Al intentar
reservar sobre una ocupación existente, `409` **con la reserva que choca en el cuerpo**.

**Lo que se deriva no se guarda.** La posición del ejemplar sale de la tarea que lo tiene
reservado, que ya lleva su `workSite`. Y el «en uso» sale de que esa tarea haya entrado en
curso: vive en la **reserva** (`status: "in_use"`), puesto por `task.status_changed →
in_progress` de forma idempotente, y **no en el ejemplar** — guardarlo ahí sería mantener a mano
lo que ya dice la agenda. El almacén del ejemplar es su **base**, no su posición.

**Liberar no puede depender de que alguien se acuerde.** Un operable no se consume al completar
la tarea: se libera. Si nadie lo libera, queda ocupado para siempre y el tablero miente. Lo
cierra el evento de la tarea —`status_changed` a `completed` o `cancelled`, `validated`,
`rejected`— con su motivo en `ReleaseReason`, tipo propio (`completed | cancelled | rejected |
manual`). Y dos trampas del control de estado que hay que respetar: el completado parcial no
emite nada, y `rejected` puede llegar después de `validated`, cuando ya se liberó — entonces no
hace nada.

**El tablero es una pantalla nueva.** La primera versión de este ADR decía que era el
`AvailabilityBoard` con otras filas. No lo es: aquel es un mapa de calor —una fila por sucursal,
una celda con un contador—, y este es una **agenda** —una fila por ejemplar, una celda con la
tarea y el sitio—. Contrato propio (`UnitBoard`) y componente propio en el panel. Lo que sí se
reutiliza es la cascada de festivos y ausencias para los huecos de no disponibilidad.

## Aplazado

**Tiempo mínimo entre asignaciones.** Dos tareas seguidas con la misma excavadora en obras
distintas no chocan en el calendario pero son imposibles en la carretera; y un animal necesita
descanso obligatorio entre jornadas. Es el mismo campo para los dos casos. Fuera de v1, ver
[06 §D6](../06_decisiones-abiertas.md).

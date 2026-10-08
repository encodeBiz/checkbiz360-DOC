# ADR-003 — Un solo catálogo de artículos, con tipo consumible u operable

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

En el diseño inicial se propuso **separar** lo que se gasta de lo que se presta: un módulo de
stock para consumibles y otro de custodia para herramientas, argumentando que son dos productos
con dos pantallas y que la v1 tenía que elegir.

Se rechazó, y con razón: **deben coexistir**. Son lo mismo con distinta forma de gastarse, y
separarlos obliga al cliente a aprender dos altas, dos buscadores y dos informes para contestar
una sola pregunta.

## Decisión

**Un solo catálogo** (`items`) con un campo `type: "consumable" | "operable"`.

## Justificación

**El tipo decide dos cosas y nada más:**

1. **Cómo existe en el almacén.** El consumible existe como **cantidad**: un registro por
   artículo y almacén, con físicas y comprometidas. El operable existe como **ejemplares**: un
   registro por cada uno, con su identificador y su agenda — porque la fregadora #2 no es
   intercambiable con la #3, una está el jueves en Arendel y la otra no.
2. **Cómo se gasta.** El consumible se resta y no vuelve. El operable se ocupa un rato y vuelve
   entero.

**Todo lo demás es común:** la ficha, el almacén del que sale, el movimiento que lo registra,
la tarea a la que se imputa, quién lo sacó y quién lo firmó. El mismo libro para los dos; lo
único que cambia es que el apunte del consumible lleva cantidad y el del operable lleva un
intervalo.

**Y eso es lo que compra la unificación:** un alta, un buscador, un informe. El admin da de
alta «toallas» y «fregadora industrial» en la misma pantalla y solo marca el tipo distinto. Y
el informe de la tarea del Lidl dice «20 toallas y 4 horas de fregadora» en la misma tabla, no
en dos.

**Visto de otra manera: todo el material se presta.** La máquina se reserva, sale y vuelve
entera; la toalla se reserva, sale y vuelve la parte que no se gastó. Es el mismo ciclo, y la
única diferencia entre un operable y un consumible es cuánto vuelve.

## Un operable no es una máquina

El vocabulario del modelo es **neutro a propósito**. Un operable puede ser una fregadora, una
furgoneta, un andamio o un perro de seguridad. Por eso:

| En vez de | Va | Porque |
|---|---|---|
| `serialNumber` | `identifier` | Serie, matrícula, crotal o microchip |
| `hourMeter` | `usageCounter` + `usageUnit` en la ficha | Horas, kilómetros o jornadas |
| `status: "maintenance"` | `status: "unavailable"` + `unavailableReason` | Avería, ITV, veterinario, descanso |
| `status: "in_use"` en el ejemplar | `status: "in_use"` en la **reserva** | Lo que se deriva no se guarda (ADR-006) |

El sesgo de taller no es cosmético: cierra mercados —agrícola, seguridad con perros, equino—
que el modelo ya cubre sin cambiar una línea.

Y el descanso obligatorio de un animal no es un concepto nuevo: es la misma cascada de
disponibilidad que ya tienen los empleados en `packages/shared/src/calendar/`. Un hueco de
veterinario y un hueco de mantenimiento son el mismo hueco.

## Consecuencias

- `items.type` **no es editable**: un consumible no se convierte en operable, porque su
  historia de movimientos no se podría reinterpretar. Para eso se crea otro artículo.
- `usageUnit` es obligatorio al crear un operable.
- Un operable no tiene documento en `stock`; un consumible no tiene `item_units`.
- El panel tiene **una** pantalla de catálogo, con el tipo como columna y como filtro.

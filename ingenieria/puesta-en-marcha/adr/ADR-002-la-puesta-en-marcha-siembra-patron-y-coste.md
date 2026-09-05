# ADR-002 — La puesta en marcha crea el patrón de sucursal y el coste por hora

**Fecha:** 2026-09-05
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto — dos medidas contra `dev-encodebiz` (2026-09-03)

Sembrando un mes de asistencia real (1.371 fichajes, 446 jornadas, 20 empleados) aparecieron
dos cosas que dejan a un cliente recién montado sin la mitad del producto, **y ninguna de
las dos da error**.

### El trigger no acumula si la sucursal no tiene patrón

`onChecklogWrite` empieza comprobando `existsPatterns(branchId)` contra la colección
`checkbiz_branch_patterns`. Si el documento no existe, la función retorna sin hacer nada.

Una sucursal recién creada no tiene ese documento. El resultado es un cliente que ficha con
normalidad durante semanas y no acumula ni un dato de comportamiento: ni patrones de
sucursal, ni patrones de empleado, ni coste, ni fiabilidad. El panel enseña ceros y no hay
nada en los registros que explique por qué.

### El coste viaja congelado dentro del fichaje

`createChecklog` no guarda una referencia a la responsabilidad: guarda una **copia
aplanada** en `metadata.employeeResponsibility`, hecha con `{...data.job, responsibility,
level}` — de modo que el precio queda suelto en la raíz. De ahí lo lee el cálculo de
patrones (`employeeResponsibility?.price`).

Consecuencia: si las responsabilidades nacen con `price: 0` —como estaban las 21 de dev—,
todo el análisis de coste sale plano. Y corregir el precio más tarde **no arregla lo ya
fichado**, porque cada fichaje se llevó su copia.

## Decisión

La puesta en marcha no termina cuando existen las sucursales y la plantilla. Termina cuando:

1. **Cada sucursal tiene su documento en `checkbiz_branch_patterns`**, creado con
   `buildInitialBranchPattern`.
2. **Cada responsabilidad tiene su coste por hora puesto**, antes de que se registre el
   primer fichaje.

Las dos cosas son parte del seed, no de un paso posterior ni de una tarea manual.

## Consecuencias

**La plantilla de alta debe pedir el coste por hora**, y `coste_mes` sale de ella: en el
modelo sólo existe `Job.price` y es por hora. Pedir las dos cosas sin una regla que decida
cuál manda es pedir una contradicción.

**Un cliente que ya esté fichando con precio 0 arrastra el error.** Los fichajes viejos no
se pueden arreglar poniendo el precio ahora; habría que reprocesarlos. Es una razón más para
que esto se haga en el alta.

**`buildInitialBranchPattern` usa `Math.random()`** para el horario base cuando la sucursal
no trae `advance.startTimeWorkingDay`. En una puesta en marcha conviene que la sucursal ya
traiga ese dato, para que el patrón no arranque de un valor sorteado.

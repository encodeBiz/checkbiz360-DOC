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
`checkbiz_branch_patterns`. Si el documento no existe, la función retorna sin hacer nada. Un
cliente puede fichar con normalidad durante semanas y no acumular ni un dato: ni patrones, ni
coste, ni fiabilidad. El panel enseña ceros y nada en los registros explica por qué.

**Corrección del 2026-09-05.** Ese documento *sí* se crea solo: la Cloud Function
`onCreateBranch` escucha `entities/{entityId}/branches/{branchId}`, construye el patrón con
`buildInitialBranchPattern` y es idempotente. La primera versión de este ADR decía que crear
la sucursal no bastaba, y no era cierto.

Lo que queda en pie es el riesgo, que es otro y más fino:

- **Es asíncrono.** Entre crear la sucursal y tener su patrón pasa un tiempo que nadie
  controla, y el seed sigue adelante mientras tanto.
- **Vive en el otro repositorio.** Esa ruta ya se rompió una vez en producción, cuando `main`
  de `encodeBiz-SAAS` se quedó por detrás y dejó de crearse la sucursal automática. Cuando eso
  pasa, no hay error: hay silencio.

Así que la regla no es crear el patrón —eso competiría con el trigger por el mismo
documento—, sino **comprobar que apareció, y parar si no**.

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

1. **Cada sucursal tiene su documento en `checkbiz_branch_patterns`.** Lo crea el trigger
   `onCreateBranch`; el seed espera a que aparezca y **se detiene si no aparece**, porque sin
   él todo lo que venga después será invisible para la analítica.
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
no trae `advance.startTimeWorkingDay`. Como lo ejecuta el trigger y no el seed, la única forma
de que el patrón no arranque de un valor sorteado es que la sucursal se cree ya con ese dato.

**Y el seed depende de que las functions estén al día.** No es una dependencia que se pueda
mirar hacia otro lado: si `onCreateBranch` no está desplegada, la puesta en marcha parece
correcta y el cliente nace ciego.

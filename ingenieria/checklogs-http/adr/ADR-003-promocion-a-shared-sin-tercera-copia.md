# ADR-003 — Lo común se promueve a `@encodebiz/shared`; no se crea una tercera copia

**Estado:** Aceptado
**Fecha:** 2026-07-30
**Contexto:** checklogs-http

---

## Contexto

Las migraciones anteriores siguieron un patrón de copia: cada servicio nuevo se llevó su propia versión de las piezas transversales. Hoy `tasks` y `documents` contienen, **byte a byte idénticos** salvo la línea de import:

- el stack de notificaciones de checkbiz (`CheckbizNotifier`, `CheckbizOperationals`, `messages`, las dos factories)
- `FirestoreBranchRepository` completo
- `canWrite`
- `validateToken` / `validateTokenJWT` / `authError`

El TDR-001 de `tasks-service` ya registró esto como deuda, con la unificación aplazada a una fase futura que nunca tuvo dueño.

Los checklogs necesitan las cuatro piezas. Copiarlas otra vez daría **tres** copias del mismo código, incluida la tabla `messages` que contiene precisamente la clave `update_checklog_pending` que usa el circuito de corrección de fichajes.

## Decisión

Antes de portar nada, se promueven esas piezas a `packages/shared/src/checkbiz/` y se repuntan `tasks` y `documents` para que importen de `@encodebiz/shared`, borrando sus copias locales. `checkinbiz` consume desde shared desde el primer día y no copia nada.

Se sube también `getDistanceInMeters`, que hoy solo existe en Firebase y va a necesitar cualquier servicio que trabaje con geocercas.

Las entidades `Employee` y `Branch` se suben en su versión superset —la de `tasks`, estructuralmente idéntica a la de `checkinbiz` salvo por tres campos que añade— solo en la medida en que el repositorio compartido necesita tiparlas. Unificar las entidades por completo es un trabajo mayor y sigue siendo deuda.

## Justificación

Tres copias de una tabla de mensajes no es un problema de estética: es que el día que haya que corregir un texto legal o añadir un idioma, se corrige en una y se olvida en dos, y el fallo aparece en el canal que menos se mira.

El momento es este porque el coste nunca va a ser más bajo: los ficheros son idénticos, así que la promoción es mecánica y el typecheck del monorepo la valida entera. Cada servicio nuevo que se migre encarece la operación.

## Consecuencias

**A favor**

- Una sola copia de cada pieza transversal; la deuda del TDR-001 de `tasks` queda cerrada en vez de ampliada.
- El siguiente servicio que se migre no tiene que decidir qué copiar.

**En contra**

- Toca dos servicios ya desplegados (`tasks` y `documents`) en una fase que, por sí sola, no entrega funcionalidad nueva. Hay que desplegarlos y verificarlos aunque el usuario no note nada.
- `@encodebiz/shared` gana peso y con él acoplamiento: un cambio en `messages` ahora afecta a tres servicios a la vez. Es el intercambio consciente — un punto de cambio en lugar de tres puntos de olvido.

**Límite explícito**

La promoción es *mover*, no *rediseñar*. No se cambia ni una firma ni un comportamiento en esta fase. Si algo de lo promovido merece un rediseño, se hace después, ya en un único sitio.

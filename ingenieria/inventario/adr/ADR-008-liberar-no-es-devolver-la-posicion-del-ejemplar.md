# ADR-008 — Liberar no es devolver: la posición del ejemplar lleva su propio rastro

**Fecha:** 2026-10-10
**Estado:** Aceptado (Jose, 2026-10-10: «me parece bien, documéntalo para que cada sesión implemente su parte»)
**Decisionario:** Jose Acevedo
**Decisión de referencia:** [ADR-006](./ADR-006-operable-se-asigna-a-tareas-con-hora.md), [ADR-007](./ADR-007-entrega-es-asignacion-con-acuse.md)

---

## Contexto

El caso que lo dispara, 2026-10-10: la fregadora FR-3 se reservó para una tarea el día entero,
se usó solo por la mañana y el supervisor quiere soltarla a mediodía para que la use otra tarea.
Desde la app no puede: la liberación a mano (`DELETE /tasks/:taskId/units/:unitId`) existe en
la API y en el panel, pero la app nunca la tuvo. Y al mirar por qué, apareció la laguna de
verdad:

> Jose: «se debe poder liberar por el supervisor, pero la trazabilidad de ese equipo debe seguir,
> porque está libre pero ¿dónde está ahora mismo? Liberar no implica devolución ni nada».

Según [ADR-006](./ADR-006-operable-se-asigna-a-tareas-con-hora.md), la posición de un ejemplar
**se deriva de la reserva activa**: está en el sitio de la tarea que lo tiene reservado, y su
almacén es su base, no su posición. En cuanto la reserva se libera, no queda nada de lo que
deducir dónde está. El tablero lo enseña libre, y libre suena a «en el almacén», que es
mentira si sigue en la obra.

Se valoraron dos salidas:

**A — Recepción obligatoria en el almacén.** Nadie da por devuelto un equipo salvo el almacén;
hasta que lo recibe, no está libre. Jose, 2026-10-10: «creo que nadie puede dar por devuelto
algo que no sea el inventario o almacén».

**B — Dos rastros distintos: la agenda y la posición.** Liberar sigue siendo soltar la agenda;
la posición pasa a tener siempre un último hecho conocido, con quién y cuándo.

## Decisión

**Opción B.** Liberar y devolver son dos cosas, y cada una lleva su rastro.

- **La agenda** dice si el ejemplar se puede reservar. La cierra la tarea sola (completada,
  cancelada, validada, rechazada) o el supervisor a mano. **No cambia nada** de lo decidido en
  ADR-006 y TDR-003 §3.
- **La posición** dice dónde está físicamente. Deja de deducirse solo de la reserva activa y
  pasa a ser **el último hecho de un rastro**: cada hecho lleva dónde, quién lo dijo y cuándo.
  Nunca hay un ejemplar «sin posición»: como poco, la base.

### Los hechos que mueven la posición

| Hecho | Posición que deja | Quién |
|---|---|---|
| Alta del ejemplar | su almacén base | sistema |
| La tarea entra en curso (`in_use`) | el sitio de esa tarea (`workSite`, o la sucursal) | sistema, por evento |
| La tarea se cierra sola (`completed`, `cancelled`, `validated`, `rejected`) | **queda en el sitio de la tarea** | sistema, por evento |
| Liberación a mano | lo que conteste el supervisor a **«¿Dónde queda?»**: **la tarea actual o un almacén real**, nada más (Jose, 2026-10-10: «solo debe admitir la tarea actual o un almacén real»; «se lo lleva alguien, quítalo, no aporta nada») | supervisor o superior |
| Entrega a una persona ([ADR-007](./ADR-007-entrega-es-asignacion-con-acuse.md)) | con esa persona | supervisor o superior; el acuse, la persona |
| Devolución de la entrega | el almacén que recibe, con estado (`ok` · `damaged` · `lost`) | supervisor o superior |
| **Recepción en almacén** (nuevo) | el almacén que recibe, con estado | supervisor o superior |
| Traspaso del ejemplar | su nuevo almacén base | quien gestiona el catálogo |

Dos reglas que lo sostienen:

1. **Liberar sola no pregunta nada.** Cuando la tarea se cierra, el ejemplar queda «en el sitio
   de la tarea X desde las 18:00». Es lo honesto: nadie ha dicho otra cosa. No se vuelve a la
   trampa que ADR-006 evita: la agenda nunca depende de que alguien se acuerde.
2. **Recibir no bloquea.** Un ejemplar libre y fuera de base **se puede reservar** para otra
   tarea; el tablero lo enseña marcado («libre · fuera de base · en obra X») y eso es, para el
   almacén, **la lista de lo que hay que ir a recoger**. Recibirlo solo mueve la posición a la
   base y, si viene dañado, lo deja `unavailable` con el motivo (como la devolución de una
   entrega).

### Por qué no la opción A

Un rol de almacén que da por devuelto exigiría crear ese rol (hoy no existe: liberar,
entregar y recibir las puede hacer cualquier supervisor o superior y los administradores),
decidir qué pasa con lo liberado y no recibido, y romper la liberación automática al cerrar la
tarea. Con B, el almacén gana lo que pedía —saber dónde está cada equipo y qué falta por
recoger— sin ser un cuello de botella para la agenda.

### Por qué no contradice «lo que se deriva no se guarda»

La posición mientras hay reserva activa sigue coincidiendo con la agenda (la escribe el mismo
evento). La posición **después** de liberar no se puede deducir de nada: apuntarla no duplica
lo que dice la agenda, es el único sitio donde vive. Un solo escritor, el servicio
(ADR-005).

## Consecuencias — qué implementa cada sesión

### API (`encodebiz-api`, `services/inventory`) — **sesión del servidor**

- **Rastro de posición del ejemplar.** Un hecho por fila con `{ kind: task_site | warehouse |
  person, taskId?, branchId?, warehouseId?, employeeId?, condition?, reason, by, at }` y, en el
  ejemplar, **`position`** con el último hecho (lo escribe solo el servicio, como `signingKey`
  en el dispositivo). Dónde guardar el rastro —subcolección del ejemplar o el libro
  `item_movements` con tipos nuevos, como ya hace `assignment` / `assignment_returned`— lo fija
  el servidor; el espejo a Postgres sigue el patrón de `unit_assignments_raw` (TDR-004).
- **`DELETE /tasks/:taskId/units/:unitId`** admite en el cuerpo **`leaveAt: "site" |
  "warehouse"`** (por defecto `site`) y, con `warehouse`, **`warehouseId` obligatorio**: un
  almacén activo de la entidad, o 400. No hay «se lo lleva alguien»: entregar a una persona es
  «Mi material» (ADR-007), no liberar. Sigue siendo de supervisor o superior (`canReserve`).
- **Las reservas** de `GET /tasks/:id/materials` llevan `unitWarehouseId` (ya lo hacen): la app
  pone ese almacén el primero.
- **`POST /units/:unitId/receive`** (nuevo) — `{ warehouseId?, condition: ok | damaged | lost,
  note? }`. Supervisor o superior. `damaged` y `lost` dejan el ejemplar `unavailable` con motivo,
  igual que la devolución de una entrega (retirarlo es una decisión desde su ficha). Si el ejemplar tiene una reserva en curso,
  `409 inventory/unit_in_use` con la tarea en el cuerpo: primero se libera.
- **Los eventos de tarea** que ya liberan (`internal.router`) escriben el hecho «queda en el
  sitio de la tarea» al liberar, y «en el sitio» al entrar en curso.
- **Lectura:** `GET /units/:id`, `GET /tasks/:taskId/materials` (cada reserva) y `GET /board`
  llevan `position`; `GET /stock/overview` admite el filtro **`outOfBase=true`** para operables
  libres cuya posición no es su base.
- Contratos completos en [04](../04_contratos-api.md) cuando se implemente; códigos nuevos en
  el catálogo de errores.

### Panel (`encodebiz-front-saas`) — **sesión del panel** — hecho el 2026-10-10 (rama `feat/inventario-posicion-ejemplar`)

> Lo hecho en el panel, que funciona con la API de hoy y se completa solo cuando llegue la nueva:
> - **Liberar desde la tarea** (material de la tarea): el botón abre «Liberar equipo». Si la reserva
>   trae el campo `position` (aunque sea `null`) **y está en uso**, pregunta **«¿Dónde queda?»** con «Queda en la
>   tarea» y los almacenes activos, el base primero, y manda `leaveAt` + `warehouseId`. Si no lo
>   trae, es una confirmación sin pregunta: la respuesta no se guardaría. Error
>   `inventory/reservation_not_found` → «Este equipo ya estaba liberado.» y recarga.
> - **La fila del equipo** en la tarea enseña dónde está (`position` de la reserva), sin hora. La
>   frase usa `site` («En la tarea "X", Calle…») y una posición `unknown` con `reason: lost` se
>   lee «Perdido», como en la app.
> - **Ficha del artículo, ejemplares:** columna **«Dónde está»** (último hecho, con «desde» y la
>   etiqueta «Fuera de base»), la acción **«Dónde ha estado»** con el rastro
>   (`GET /units/:id/positions`, la posición actual arriba y cada hecho con su motivo, estado y
>   nota) y la acción **«Recibir en almacén»** en los que están fuera de base:
>   almacén (el base primero), estado `ok · damaged · lost` y nota → `POST /units/:id/receive`.
>   `409 inventory/unit_in_use` → aviso con la tarea (lee `taskTitle`, o `taskId` y la busca).
> - **Calendario de ocupación** (ficha del artículo): bajo el ejemplar fuera de base, «Fuera de base ·
>   en {sitio}», con la hora en el tooltip.
> - **Existencias:** «Fuera de base» en el desplegable de estado → `outOfBase=true` (con
>   `type=operable`); en la fila del operable, «Fuera de base N» en el desglose.
> - **Lo que el panel espera de la API** (además de lo de arriba):
>   - `position` en `GET /items/:id/units` (cada ejemplar) y en las filas de `GET /board`, con la
>     forma que pide la app (`kind`, `at` y los nombres `taskTitle`, `warehouseName`,
>     `employeeName` además de los ids). Sin nombre, el panel dice «En un almacén», nunca un id.
>   - **`units.outOfBase`** (número) en las filas de operables de `GET /stock/overview`: el ADR
>     pide el filtro pero no el recuento por fila.
>   - En el `409 inventory/unit_in_use` de `receive`, `taskId` y, si puede, `taskTitle` en el cuerpo.
> - **Revisado contra la API de `feat/inventario-posicion-ejemplar` (2026-10-10):** «Perdido» deja
>   el ejemplar no disponible (el diálogo de recibir lo dice así), `receive` devuelve
>   `{ position, assignment? }` y el `409 inventory/unit_in_use` trae `taskId` en la raíz del cuerpo.

- **Ocupación (tablero):** el ejemplar libre fuera de base se enseña como «Libre · fuera de base
  · en {sitio} desde {hora}» y un filtro «Fuera de base» da la lista de lo que hay que recoger.
- **Liberar desde la tarea** pregunta «¿Dónde queda?»: la tarea actual o un almacén real de la
  lista, con el almacén base primero.
- **Ficha del ejemplar:** bloque «Dónde está» con el último hecho y el rastro, y la acción
  **«Recibir en almacén»** con estado y nota.
- **Existencias:** en la fila de un operable, cuántos ejemplares están fuera de base.

### App (`checkbiz360`) — **sesión de la app** — hecho el 2026-10-10, sin commit

> Lo hecho en la app, en dos tiempos y sin tocar nada cuando llegue la API:
> - **Con la API de hoy:** el supervisor o superior ve **«Liberar equipo»** en la tarjeta del
>   equipo, con una confirmación simple; llama a `DELETE /tasks/:taskId/units/:unitId` con
>   `{ entityId }` y la liberación ya funciona (el servidor lo deja como hasta ahora). Quien no
>   puede liberar ve **«Se libera al completar la tarea.»**
> - **Cuando la API mande `position` en las reservas** de `GET /tasks/:id/materials`, la app lo
>   detecta sola: al liberar abre un solo selector **«¿Dónde queda?»** con «Queda en la tarea» y,
>   debajo, los almacenes activos (`GET /warehouses?status=active`), el base primero; manda
>   `leaveAt` y `warehouseId`. Un toque; y la tarjeta enseña **«Dónde está»** en una frase corta, sin hora: «En la
>   tarea "Limpieza Lidl"», «En el almacén Vallecas» (Jose, 2026-10-10: «con que marque dónde
>   está basta»). La hora la apunta el servidor y no la escribe nadie; la app no la enseña.
> - **Lo que la app espera en `position`:** `kind` (`task_site` · `warehouse` · `person`), `at`, y
>   los nombres **`taskTitle`, `warehouseName`, `employeeName`** además de los ids: la app no
>   carga catálogos para nombrar, y sin nombre dice «En el almacén» o «Con una persona», nunca un
>   id. Un `kind` desconocido se enseña como «Sin datos».
> - **Revisado contra la API de `origin/develop` (2026-10-10):** el contrato coincide. Dos ajustes
>   en la app: solo pregunta «¿Dónde queda?» si la reserva está **en uso** (la tarea empezó y el
>   equipo salió); si solo estaba reservada, confirmación simple y sin `leaveAt`, y el servidor lo
>   deja donde estaba. Y una posición `unknown` con `reason: lost` se lee «Perdido».
> - Errores por código: `inventory/reservation_not_found` («Este equipo ya estaba liberado.», y
>   recarga) y, de paso, la pantalla de material deja de enseñar el texto crudo de una excepción.

- **Material de la tarea, tarjeta del equipo:** para supervisor o superior (misma regla que el
  panel: `canReserve`), el botón **«Liberar equipo»** con la pregunta «¿Dónde queda?» (la tarea
  actual o un almacén real). Para el trabajador, en vez
  del botón, la línea **«Se libera al completar la tarea»**. La tarjeta enseña dónde está el
  equipo ahora (`position` de la reserva).
- **Recibir en almacén** no va en la app en esta vuelta: es del panel. Si el almacén lo pide
  desde el móvil, es una fila más en la tarjeta con la misma llamada.
- Los textos, en los cuatro idiomas de la app (es, en, pt, de; el panel tiene además fr); errores por código, nunca el texto crudo.

### Orden

API primero (rastro, `leaveAt`, `receive`, lecturas); panel y app pueden ir en paralelo sobre
los contratos de arriba. Hasta que la API lleve `position`, la app enseña la tarjeta como hoy.

## Aplazado

- **Recepción con lectura de contador** (`usageEnd` al recibir, no solo al liberar): cuando el
  mantenimiento por contador entre en juego.
- **Aviso al almacén** cuando un ejemplar lleva más de N horas libre y fuera de base: es un
  caso de Fase 5 (avisos) cuando se pida.

## Implementación de la API (2026-10-10)

Hecha en `feat/inventario-posicion-ejemplar` de `encodebiz-api` (commit `38917a3`), sin fusionar.
Probada contra dev de punta a punta: alta, en curso, cierre, liberación sin respuesta y al
almacén, recepción con daños, traspaso de base, filtros «fuera de base» y eventos repetidos sin
duplicar; todo lo creado se borró.

**Lo que quedó fijado y el documento dejaba abierto:**

- **El rastro va en una subcolección del ejemplar**, `item_units/{unitId}/positions`, no en el
  libro. El ejemplar lleva `position` (el último hecho) y `outOfBase` (para filtrar sin cargar
  todos). Espejo a Postgres en `unit_positions_raw`, **migración 025, a aplicar a mano**.
- **Contrato del hecho:** `{ id, kind: warehouse | task_site | person | unknown, reason, warehouseId?,
  taskId?, branchId?, site?, employeeId?, assignmentId?, reservationId?, condition?, note?, by, at }`.
  `reason`: `created`, `task_in_progress`, `task_closed`, `released`, `assigned`,
  `assignment_returned`, `received`, `base_changed`, `lost`. `site` es la calle del sitio de la tarea.
- **Liberar sin `leaveAt`**: en el sitio si la reserva estaba en uso; si no llegó a estar en uso,
  la posición no cambia (el equipo no salió). Igual al cerrarse la tarea sola: solo lo que estaba
  en uso queda «en el sitio».
- **`leaveAt` solo admite `site` o `warehouse`**, y con `warehouse` el `warehouseId` de un almacén
  activo, o 400; `person` es un 400 (se quitó el 2026-10-10). Se comprueba antes de soltar la
  agenda: o se hace entero o nada.
- **Recibir con el equipo entregado a alguien cierra esa entrega** en el mismo gesto, en el almacén
  que recibe. Solo bloquea una reserva **en uso** (`409 inventory/unit_in_use`); una que no ha
  empezado no impide recibir ni se cancela.
- **`lost` deja el ejemplar no disponible, no retirado**, como ya hacía la devolución de una
  entrega: retirarlo es decisión de alguien desde su ficha. La posición pasa a `unknown`.
- **Traspaso de base:** si el ejemplar estaba en su base, la posición se va con ella
  (`base_changed`); si estaba fuera, sigue donde esté y solo se recalcula `outOfBase`.
- **Lectura:** `GET /units/:unitId` (con `position`, reserva en curso o próxima y entrega activa),
  `GET /units/:unitId/positions?limit` (lo último primero), `position` en cada reserva de
  `GET /tasks/:taskId/materials`, `position` y `outOfBase` en cada fila de `GET /board`
  (también `?outOfBase=true`), y `?outOfBase=true` en `GET /stock/overview`, con
  `units.outOfBase` en cada fila: libres fuera de base, sin contar lo que está en uso o entregado.
- **Lo anterior al rastro** no tiene posición guardada y se enseña en su base. Para que diga la
  verdad hay que pasar `backfill-positions.js --entity <id> --apply` por cada entidad con el
  módulo (simula sin `--apply`): entregado → con la persona; en uso → en el sitio; si no, su base.

**Pendiente en la API:** el reespejo periódico del rastro a Postgres (hoy solo en la petición) y
los contratos en [04](../04_contratos-api.md).


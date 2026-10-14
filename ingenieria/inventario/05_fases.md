# 05 — Fases de implementación

Cada fase es **independiente y desplegable**. El orden es por uso: lo que se toca veinte veces
al día antes que lo que se toca una vez al mes.

Cada fase lleva tres partidas: **API** (este repo), **panel** y **app** (otros repos, liberación
manual). Las de app y panel no son una línea al pie: son el camino crítico de las Fases 2 y 3.

---

## Fase 0 — Fundación

**Objetivo:** el esqueleto en pie, con la puerta puesta desde el primer día.

**API**
- `services/inventory/` con `app.ts`, `server.ts`, `package.json`, `tsconfig.json`, `Dockerfile`
  (copia del de `tasks`, puerto 3016).
- `GET /health` → `{ok: true, service: "inventory"}`.
- Bloque en `docker-compose.yml` y `docker-compose.staging.yml`; upstream y location en nginx.
- Middleware de suscripción, **antes que cualquier funcionalidad**: una puerta añadida al final
  se olvida en alguna ruta.
- `inventory` en el tipo `SERVICES` de `shared` y en `OUR_SERVICES` de `billing`; plan en
  `service/inventory/plan/*`, sin límites; precio en Stripe con tramos graduados: **29 € hasta
  50 empleados y 0,75 € por cada empleado a partir del 51**. La cantidad, el recuento y los
  15 días de prueba son los de siempre: nada nuevo en facturación.

**Panel** — nada aún. **App** — nada aún. (El panel de la Fase 0 llegó con la Fase 1: servicio `inventory` en `BizType`, proxy, puerta por `GET /access` y entrada de menú.)

**Criterio de éxito:** `/health` responde; cualquier otra ruta devuelve 403 sin suscripción; una
entidad con suscripción de prueba pasa. ✅ Hecho el 2026-09-28 (`feat/inventory-fase-0` →
`develop`), probado en local contra dev.

---

## Fase 1 — Maestros

**Objetivo:** que el admin pueda dar de alta lo que tiene.

**API**
- `warehouses`, `items`, `item_units` en `shared` y sus rutas.
- `searchIndex` si se decide que se buscan desde el panel ([06 §D7](./06_decisiones-abiertas.md)).

**Panel**
- Catálogo con el tipo como columna y filtro; alta y edición.
- Almacenes con `scope` y sucursales; ejemplares por artículo.

**App** — nada aún.

**Criterio de éxito:** un cliente da de alta Vallecas sirviendo a Madrid Norte y Madrid Sur,
crea «toallas» y «fregadora industrial» en la misma pantalla, y registra tres fregadoras con su
identificador.

✅ **API hecha el 2026-09-29** (`feat/inventory-fase-1` → `develop`), probada en local contra dev
firmando como el owner de la entidad: todos los caminos y todos los errores del contrato.
✅ **Panel hecho el 2026-09-29** (`feat/inventario-panel` → `develop` de encodebiz-front-saas): catálogo con el tipo como columna y filtro, detalle del artículo con existencias por almacén o ejemplares, almacenes con ámbito y sucursales. `searchIndex` sin decidir (D7).

---

## Fase 2 — Consumibles de punta a punta

**Objetivo:** el ciclo completo del material que se gasta, **conciliación incluida**. Sin ella
los informes de la Fase 4 se construirían sobre `pending` sin cerrar.

**API**
- `stock`, `item_movements`, `task_materials`.
- Entradas, ajustes y traspasos.
- Reserva, salida, consumo, devolución y cuadre desde la tarea, en transacción con el saldo.
- Idempotencia por `movementId`; `occurredAt` opcional aceptado.
- Actividad `item_consumed` (valor nuevo en `TaskActivity`, en `shared`).
- Endpoint interno `POST /internal/task-events` y el suscriptor interno en la resolución de
  `publish()`: liberación de compromiso al validar/cancelar/rechazar.
- Job de recálculo de saldos.

**Panel**
- Existencias con filtro por almacén y por sucursal, entradas, ajustes, traspasos.
- Reserva de material en la tarea.
- **Paso de cuadre en la pantalla de validación**: «salieron 30, se declararon 20, faltan 10».

**App**
- Pantalla de material en la tarea (`GET /tasks/:id/materials`).
- Salida con selector de almacén **solo cuando hay varios**, sin preselección.
- Declaración de consumo precargada con lo que salió.
- Tratamiento del `403 inventory/not_subscribed` (esconder el módulo).

**Criterio de éxito:** un operario saca 30 toallas, declara 20, el validador cuadra las 10, y el
saldo de Vallecas y el libro cuentan lo mismo.

✅ **API hecha el 2026-09-29** (`feat/inventory-fase-2` → `develop`), probada en local contra dev con
una tarea creada por la API real: reserva → salida → consumo → cuadre, reintento idempotente,
traspaso en una transacción, saldo negativo marcado, evento `task.validated` firmado que libera lo
reservado, recálculo sin desviación y `item_consumed` en la tarea. La prueba encontró y corrigió
un hueco del modelo (`reservedIssued`, TDR-002 §1). ✅ **Panel hecho el 2026-09-29**: existencias con filtros, entrada, recuento, traspaso y mínimo; reserva, salida y consumo desde el detalle de la tarea; y el **cuadre como paso previo a «Validar»** cuando queda material sin declarar. **2026-10-07 (Jose: «es un planificador el que crea las tareas y asigna recursos»)**: el material se asigna en el **alta de la tarea** (bloque «Material para la tarea»: consumibles por cantidad y ejemplares de operables, reservados nada más crearla); en el detalle las acciones quedan a la vista. ✅ **App hecha el 2026-09-29** (`feat/inventario-material` → `develop` de checkbiz360): tarjeta «Material» en el detalle de la tarea y pantalla de material (`/attendance/tasks/:taskId/materials`), salida precargada con lo reservado y con selector de almacén **solo cuando el servidor devuelve los candidatos** (400 `inventory/warehouse_required`, mismo `movementId` al reintentar), consumo precargado con lo que salió, ejemplares reservados, y el 403 `inventory/not_subscribed` recordado por sesión para no volver a preguntar ni pintar nada.

Requiere en el `.env` del servidor `INVENTORY_INTERNAL_URL` (sin ella el motor de eventos no
encola entregas al módulo) e `INVENTORY_RECOMPUTE_MINUTES`.

**Rollback:** el módulo se apaga quitando la suscripción; ni `tasks` ni la app dejan de
funcionar.

---

## Fase 3 — Operables

**Objetivo:** cuadrar lo que se presta y vuelve. Es la fase que vende el módulo en construcción
y en limpieza — y la que más crece respecto al diseño inicial, porque el tablero es nuevo.

**API**
- `unit_reservations` y detección de choque por solapamiento, en transacción.
- Reserva y liberación desde la tarea; liberación automática por evento.
- `in_use` derivado de `task.status_changed → in_progress`, idempotente.
- Huecos de no disponibilidad, reutilizando la cascada de `calendar`.
- `GET /board` con el contrato `UnitBoard`.

**Panel**
- Reserva de ejemplares en la tarea, con el choque enseñado con su tarea rival.
- **Tablero de ocupación: componente nuevo** (agenda por ejemplar), no el de disponibilidad.

**App**
- Ejemplares reservados en la pantalla de material de la tarea.

**Criterio de éxito:** asignar la fregadora #2 a dos tareas solapadas devuelve 409 con la
reserva que choca; el tablero enseña dónde está cada ejemplar cada día sin que nadie lo apunte.

✅ **API hecha el 2026-09-29** (`feat/inventory-fase-3` → `develop`), probada en local contra dev con
dos tareas creadas por la API real: choque con la tarea rival en el cuerpo, intervalos pegados
sin choque, no disponible con fecha que corta antes y no después, `affectedReservations` al
inhabilitar, `currentReservation` derivada, agenda, tablero con obra y sitio de la tarea,
`in_progress` idempotente, `completed` que libera con motivo, y liberación manual que acumula
el contador de uso. ✅ **Panel hecho el 2026-09-29**: reserva de ejemplares desde la tarea con el choque enseñado con su tarea rival, ejemplares con «ahora» y reservas afectadas al inhabilitar, y el **tablero de ocupación** como componente nuevo (agenda por ejemplar y día). **2026-10-07**: la pestaña se llama «Ocupación»; crear un operable lleva a su ficha con el alta del primer ejemplar abierta, porque un operable sin ejemplares no aparece en la ocupación ni se puede reservar (Jose creó «Mac 1» como operable y la ocupación salía vacía). ✅ **App**: los ejemplares reservados se ven en la pantalla de material (la reserva es del supervisor, en el panel).

Conocido: una entidad sin calendario da `timezone: UTC` en el tablero; el siguiente respaldo
razonable es la zona horaria de la dirección de la entidad.

---

## Fase 4 — Espejo e informes

**Objetivo:** que el libro conteste preguntas.

**API**
- Migración `023`: `dim_*`, `item_movements_raw`, `unit_reservations_raw`.
- Inserción en Postgres desde `inventory` en la misma petición + job `remirror` sobre
  `mirrored: false`.
- Las tres dimensiones en `SyncDimensions` (`analytics`).
- `GET /movements` desde Postgres, con `staleness`.
- Informe de consumo por tarea, empleado, sucursal y periodo, en `reports`.

**Panel** — pantalla del informe, como la del informe de tareas. **App** — nada.

**Criterio de éxito:** el informe dice cuánto material se fue en cada obra del último trimestre
y quién lo sacó, y avisa si hay movimientos sin espejar.

✅ **API hecha el 2026-09-29** (`feat/inventory-fase-4` → `develop`), probada en local con un Postgres
desechable levantado desde cero con las 23 migraciones (valida la `023` tal cual) y Firestore de
dev: espejo en la propia petición, reserva upsertada al cambiar de estado, `GET /movements`
paginado por `(occurred_at, movement_id)`, un apunte «perdido» que `staleness` delata y
`POST /internal/remirror` recoge, `SyncDimensions` con las tres dimensiones y su `dim_sync_log`,
y el informe de consumo por artículo, tarea y empleado con el 403 a quien no tiene asiento.
✅ **Panel hecho el 2026-09-29**: informe de consumo con totales y CSV (agrupado por artículo, tarea, empleado, sucursal o almacén). **Corrección del 2026-10-07 (Jose)**: el libro **no es una pestaña**, es la descarga CSV «Descargar movimientos» dentro del informe, con su periodo y filtros y el aviso de `staleness` —«el libro es un informe más» (ADR-005)—. La pestaña «Libro» que se había puesto se retiró.

**Para desplegarlo en dev** hace falta, a mano y en este orden: aplicar `migrations/023_inventario.sql`
por SSH (`docker compose … exec -T postgres psql -U encodebiz -d encodebiz_staging -f -`), y
añadir a `.env.staging` `INVENTORY_INTERNAL_URL`, `INVENTORY_RECOMPUTE_MINUTES` e
`INVENTORY_REMIRROR_MINUTES` (ver `.env.staging.example`). La `023` amplía el `CHECK` de
`dim_sync_log.dimension`: sin ella, el registro de las dimensiones nuevas falla.

---

## Fase 5 — Avisos y discrepancias

**Objetivo:** que el módulo hable solo.

**API** — aviso de mínimo por artículo y almacén, sobre el framework de notificaciones de
`shared`; listado de discrepancias (`onHand` negativo).
**Panel** — bandeja de discrepancias con el ajuste a un clic.

✅ **API hecha el 2026-09-29** (`feat/inventory-fase-5` → `develop`). El libro detecta el cruce
—del mínimo y del cero— en el único sitio que ve el antes y el después, y un decorador del
repositorio dispara el aviso a mejor esfuerzo: dos claves nuevas en `messages.ts`
(`stock_below_minimum`, `stock_discrepancy`) por el mismo camino que los avisos de tareas, a
supervisores y superiores de las sucursales del almacén (o responsables de entidad si sirve a
toda). **Se avisa al cruzar, no en cada apunte por debajo.** `GET /stock/discrepancies` es la
bandeja con nombres; las respuestas de salida y entrada llevan los cruces (`alerts`,
`crossedBelowMinimum`, `crossedNegative`) para que el panel diga «aviso enviado». Probado en
dev con una entidad de QA con supervisor, responsable y owner: tres avisos in-app al cruzar el
mínimo, ninguno en la salida siguiente, tres de discrepancia al cruzar el cero, y la bandeja
vacía tras el recuento. Los destinatarios se resuelven sin índice compuesto (el resolutor de
tareas pide uno que dev no tiene). ✅ **Panel hecho el 2026-09-29**: los cruces de la salida se dicen en el momento. **Corrección del 2026-10-07 (Jose)**: la bandeja **no es una pestaña**: es el filtro «discrepancia» de Existencias, con un aviso arriba que lo activa y el recuento a un clic en la fila. La pestaña «Discrepancias» se retiró.

---

## Panel: la forma final (2026-10-07)

Tras probarlo, Jose fijó el criterio: «lo más intuitivo y minimalista posible sin perder
versatilidad», y «Existencias es el core, el centro de mando». El panel quedó así:

- **Dos pestañas: Existencias y Almacenes**, como paneles de una sola página (`GenericTabs`,
  igual que «Horarios y festivos»): los controladores viven en la página y cambiar de pestaña
  no vuelve a cargar nada; la cabecera cambia título y acciones con la pestaña, y
  `?tab=warehouses` abre la segunda (Jose, 2026-10-07: «¿por qué recargas toda la vista al
  cambiar de tabs?»). Las fichas y el informe sí son rutas propias.
- **Existencias** es la lista de artículos, sea del tipo que sea, con filtro por tipo: un
  consumible enseña lo que hay en cada almacén (disponible, en almacén, comprometido, mínimo,
  estado); un operable enseña sus ejemplares y cuántos están libres ahora (una sola llamada al
  tablero del día). Lo recién creado aparece a cero. Desde la fila: ficha, entrada, recuento,
  traspaso, mínimo, editar, archivar. Arriba, una sola acción principal, **Nueva entrada**, y
  un desplegable con traspaso e **Informe**. No hay «nuevo artículo»: el artículo nace en su
  primera entrada (el desplegable de artículo ofrece «＋ Nuevo artículo» y despliega la ficha),
  y si es un operable lo que entra es su primer ejemplar, con identificador. Una entrada es la
  única puerta por la que algo pasa a existir (Jose, 2026-10-07: «ya nuevo artículo no existe»).
- **La ficha del artículo** tiene todo lo suyo: para un consumible, existencias por almacén con
  sus acciones, movimientos de los últimos 30 días y la descarga CSV del año; para un operable,
  sus ejemplares (con «ahora») y su **calendario** de ocupación.
- **La ficha del almacén** tiene su resumen (artículos, ejemplares libres, bajo mínimo,
  discrepancias), a quién sirve, el contenido artículo a artículo con sus acciones, y sus
  movimientos recientes con la descarga CSV del año.
- **El informe** de consumo es una acción desde Existencias (ruta sin pestaña), y el libro es
  la descarga CSV dentro del informe. Las discrepancias son un filtro con aviso.
- **Todo es material.** Jose, 2026-10-07: «es el mismo item, todos son materiales con
  diferentes tipos y comportamiento». Ninguna pantalla separa consumibles y operables como si
  fueran dos entidades: hay **una lista de material** y el tipo del artículo decide qué pide
  cada línea —cantidad y almacén si se gasta, ejemplar si se presta—. En el alta de la tarea,
  una sola lista con «Añadir material»; en el detalle, una sola tabla (Material · Reservado ·
  Estado) y una sola acción principal, «Añadir material», con salida y consumo en un
  desplegable y el cuadre solo cuando toca. Que por detrás una línea vaya a existencias o a
  reservas de ejemplar es cosa del servicio, no de la pantalla. Aplicado también a la entrada
  (el artículo nace ahí, y si se presta entra su primer ejemplar), al traspaso (cantidad o
  ejemplar, que cambia de almacén base), a las acciones de fila de Existencias y a la ficha
  del artículo (mismo esqueleto: acciones, existencias, historia). Recuento y mínimo quedan
  solo para lo que se cuenta: un ejemplar no se cuenta, se edita. En la app, la pantalla de
  material de la tarea es también una sola lista: la tarjeta de un ejemplar enseña estado y
  tramo donde la de un consumible enseña cantidades. Para eso la API manda con cada reserva
  `unitIdentifier`, `unitLabel` y `unitWarehouseId` (GET /tasks/:id/materials), y ni el panel
  ni la app van a buscar el ejemplar por su id.
- **Listas y buscadores siguen el patrón de la plataforma** (Jose, 2026-10-07: «ninguna tabla
  de la plataforma funciona así»; «creía que estaba indexando los artículos, los almacenes, todo,
  para poder hacer búsquedas blandas»). La primera versión traía el catálogo y las existencias
  enteros (`GET /items` y `GET /stock` sin límite) y buscaba y paginaba en el navegador: con
  cien artículos no se nota, con un almacén de eventos de mil sí, y es un camino distinto al
  del resto del panel. Queda así:
  - **Artículos y almacenes se indexan en `searchIndex`** (`type: item` / `warehouse`), en
    las cuatro operaciones —crear, editar, archivar o desactivar, borrar— desde los casos de
    uso del servicio, con la misma mecánica que empleados y sucursales (`indexItem`,
    `indexWarehouse` en shared). Se buscan por nombre, referencia y categoría; en `metadata`
    va lo que el selector necesita sin otra llamada (tipo, unidad). Un artículo archivado o un
    almacén inactivo sale del índice. `services/inventory/src/scripts/reindex-search.ts`
    repara una entidad (simula; `--apply` escribe).
  - **El selector de material** (líneas de la tarea, diálogo de almacén, salida) busca en el
    índice como el de sucursal: sugerencias al abrir y prefijo al teclear.
  - **Existencias pagina en servidor**: `GET /stock/overview` devuelve la fila ya compuesta
    (artículo con cantidades por almacén o ejemplares libres/ocupados/no disponibles) con
    cursor y total, y resuelve los filtros: texto (vía índice), tipo, almacén y estado. Sin
    filtros, la página sale de Firestore por nombre (índices compuestos de `items`:
    `active+name` y `active+type+name`); con texto, almacén o estado de existencias, el
    subconjunto es acotado y se ordena y pagina en el servicio. La página es de artículos; un
    artículo con varios almacenes ocupa varias filas.
  - **Las filas llevan su nombre**: el material de la tarea (`GET /tasks/:id/materials`)
    trae `itemName`, `itemUnit` e `itemType`, y la ficha del artículo lee `GET /items/:id`.
    Los movimientos salen de Postgres ya con nombre de artículo y de almacén (unidos a
    `dim_items` y `dim_warehouses` en el lector), así que ninguna pantalla carga el catálogo
    entero: el hook `useInventoryCatalog` se queda con almacenes y sucursales.
  - **Lo que exige cada entorno**: los dos índices compuestos de `items` (creados en
    `dev-encodebiz` el 2026-10-07 con `gcloud firestore indexes composite create
    --project=dev-encodebiz …`; en producción hay que crearlos igual, con `--project` explícito
    porque el proyecto por defecto de gcloud es producción) y un `reindex-search --apply` por
    cada entidad con el add-on, para que lo creado antes del índice salga en el buscador.
- **El material se asigna al crear la tarea** (bloque «Material para la tarea», con la reserva
  hecha nada más crearla); en el detalle de la tarea las acciones van a la vista.
- Se retiraron las pestañas Catálogo, Tablero/Ocupación, Libro y Discrepancias.

## Fase 6 — Operables con papeles (diseño 2026-10-07; 6a hecha el 2026-10-08)

**Objetivo:** que un operable pueda demostrar de quién es, qué revisiones ha pasado y en manos
de quién está, para una inspección de trabajo. Jose, 2026-10-07: «dentro de inventario, como
una funcionalidad nueva, ya que esto es estricto contra operables».

El diseño completo está en [07](./07_operables-documentos-y-entregas.md) y la decisión de
fondo en [ADR-007](./adr/ADR-007-entrega-es-asignacion-con-acuse.md): el papel del ejemplar es
el documento del servicio documental colgado de un sitio nuevo (`scope` `unit` e `item`, siete
tipos), y la entrega a una persona es una asignación (`unit_assignments`) con el acuse del
trabajador desde la app. Por uso: **6a** entrega con acuse («Mi material» en la app, «Entregar»
en Existencias, ficha del ejemplar) y el informe «Equipos y EPIs» en Informes, **6b**
documentos y revisiones con caducidad: rojo en cada sitio y aviso fehaciente al asignar, **sin
bloquear** (Jose, 2026-10-08), **6c** el acuse con firma verificable: huella o cara que
desbloquea una clave del chip seguro del móvil y firma un reto del servidor (`biometric_signature`);
sin biometría, PIN del móvil; sin bloqueo, contraseña (D8, decidida). El informe se ve siempre y
en rojo si el inventario no está habilitado, con la explicación de qué es y cómo habilitarlo.

Pendiente de Jose: firma dibujada opcional por empresa ([06 §D8](./06_decisiones-abiertas.md)).
Fuera por decisión: EPIs consumibles ([06 §D9](./06_decisiones-abiertas.md)).

---

## Posición del ejemplar: liberar no es devolver (decidido el 2026-10-10)

Caso: la fregadora reservada el día entero se usó solo por la mañana; el supervisor la libera a
mediodía y la agenda queda libre, pero nadie sabe dónde está. Se decidió separar la agenda (la
suelta la tarea o el supervisor, como hasta ahora) de la posición (un rastro de hechos: en el
sitio de la tarea, en el almacén, con una persona). Al liberar a mano se pregunta «¿Dónde
queda?»; la tarea cerrada deja el equipo en su sitio; «Recibir en almacén» mueve la posición sin
bloquear la agenda; el tablero marca lo libre fuera de base como lista para recoger. Reparto por
sesión (API, panel, app) en [ADR-008](./adr/ADR-008-liberar-no-es-devolver-la-posicion-del-ejemplar.md).
Hasta que la API lleve `position`, la app enseña el equipo como hoy.

## Material sin tarea: destino tarea, persona o sucursal (decidido el 2026-10-14)

**Objetivo:** que una empresa sin tareas gestione el material igual que una con ellas. La salida, la
declaración, la devolución y el cuadre valen contra una tarea, una persona o un centro
([ADR-009](./adr/ADR-009-el-material-sale-hacia-una-tarea-una-persona-o-una-sucursal.md)).

- **API** (primero): `MaterialAccount` con `kind`, `accountKind` en el movimiento, el libro resolviendo la
  cuenta por destino, rutas `/materials/*`, migración de `account_kind` y espejo
  ([TDR-008](./tdr/TDR-008-cuentas-de-material-por-destino.md) §2–§4).
- **Panel**: «A qué va» en Salida y Asignar; Material en la ficha del empleado y de la sucursal; «Fuera del
  almacén» en Existencias; allowlist del proxy.
- **App**: «Declarar consumo» desde la jornada contra la sucursal fichada; consumibles en «Mi material».
- **Informes**: eje «destino» en el de consumo, después.

**Criterio de éxito:** una limpiadora fichada en un centro declara 2 litros sin que nadie haya creado una
tarea ni registrado una salida, y la ficha del centro y el informe del mes lo cuentan.
**Rollback:** sin `/materials` el panel y la app siguen como hoy; `task_materials` no se toca.

---

## Fuera de estas fases

**Sin conexión.** Fase posterior, con el boceto en [06 §D3](./06_decisiones-abiertas.md):
copia local de la petición cuando no hay red o la API falla, aviso al operario, reenvío
idempotente por `movementId`, `occurredAt` de la app. Los dos ganchos —el `movementId` de
cliente y el `occurredAt` opcional— ya están en la v1 para no tocar el contrato entonces.

**Lo demás que se dejó fuera a propósito** está en el [README §Alcance](./README.md#alcance):
valoración (FIFO, precio medio), recuento masivo, códigos de barras y QR, mantenimiento
preventivo por contador, tiempo mínimo entre asignaciones, y la poda de Firestore.

# Análisis a escala: el panel, el cierre diario, los patrones y Merlin — Documento de Ingeniería

**Proyecto:** encodebiz-api (`services/analytics`, `services/merlin`, `services/firebase_sdk/src/fichaje`, `packages/shared/src/db.ts`) · encodebiz-front-saas (panel)
**Dominio:** resumen del panel (`/panel/overview`), día operativo y alertas, cierre diario, trigger de patrones por fichaje, interpretaciones de Merlin, barridos globales sobre Postgres
**Fecha de inicio:** 2026-10-16
**Prioridad:** 🔴 **URGENTE.** Tercera, detrás de [reglas-firestore](../reglas-firestore/README.md) y [programadas-a-escala](../programadas-a-escala/README.md); el índice del punto 1 va en la **misma migración** que los de programadas, el primer día.
**Estado:** diseñado el 2026-10-16; nada implementado
**Autor:** Jose Acevedo

---

## Contexto y motivación

Los análisis se sacaron de Firebase al servidor justo para esto: sin tope de invocaciones,
sin arranque en frío, y Merlin contesta al momento y trabaja en segundo plano. Esa decisión
fue correcta y se mantiene. Lo que este documento recoge es que **el problema se ha movido**:
ya no está en dónde corren los análisis sino en cómo consultan Postgres y Firestore, y con
una entidad de mil personas y trescientas sucursales eso se rompe antes que cualquier worker.

Lo leído el 2026-10-16 (rutas relativas a `encodebiz-api`; `front:` es
`encodebiz-front-saas/src`):

- Un pool de **10 conexiones** por servicio con 5 s para conseguir una (`packages/shared/src/db.ts:3-8`)
  y **ningún `statement_timeout`** en ningún sitio.
- `checklogs_raw` tiene índices por `(entity_id, branch_id, timestamp)`, `(employee_id, timestamp)`
  y `checkin_ref` (`migrations/001_init.sql:62-64`). **No hay `(entity_id, timestamp)`**, y
  Postgres 16 no hace *skip scan*: una consulta de toda la entidad por fechas lee su historia
  entera y filtra después. Crece cada mes.
- El resumen del panel se calcula **en cada petición**, sin caché, con unas quince consultas.

## Principio de diseño

> **Ninguna petición del panel recorre el mes entero en memoria de Node, ninguna consulta
> correla fila a fila, y lo que no cambia desde ayer se precalcula por entidad. Lo que sí
> cambia, el día de hoy, se calcula una vez por entidad y se reutiliza.**

Es el mismo principio de [programadas-a-escala](../programadas-a-escala/README.md), aplicado
al SQL.

---

## Los cinco riesgos, por orden

### 1. El resumen del panel (`GET /panel/overview`) — se rompe primero y lo ve el cliente

`BuildPanelOverview.ts:370-391` lanza siete consultas en paralelo y después cinco
constructores en paralelo (evolución hace tres, coste operativo dos). Unas quince consultas
por carga, **nueve a la vez**: una sola petición casi llena el pool de diez. Dos personas
abriendo el panel a la vez dejan al resto de rutas de analytics en «timeout exceeded when
trying to connect».

| Constructor | Forma de la consulta | Dónde duele con 1000/300 |
|---|---|---|
| `BuildEvolution.ts:111-138` (tres consultas, dos meses) | agrega por ámbito y semana, con una **subconsulta correlada por grupo** sobre el CTE `cyc` (`:133-134`) | nivel empleado: ~9 000 grupos × 45 000 ciclos ≈ **400 M** comparaciones; nivel sucursal ≈ 120 M. Devuelve series de los mil empleados (`:308`). **El peor** |
| `BuildBranchEffect.ts:153-180` (×2) | `GROUPING SETS` por (empleado, sucursal) y (empleado), `clean_rate` correlada por grupo (`:174-178`) | ~2 000 grupos × 22 000 ciclos ≈ 44 M, dos veces |
| `BuildBranchBehaviour.ts:88-118` (×2) | agrega por sucursal con dos subconsultas correladas por sucursal (`:113-115`) | 300 × 22 000 × 2 × 2 |
| `BuildGeoCompliance.ts:169-190` | **sin `GROUP BY`: carga todas las marcas del mes en Node** (45-90 k filas) | cada marca fuera de valla se cruza con las 300 sucursales (`:349-351`) y después con todas las demás marcas fuera (`:365-371`): Haversine **O(n²)** |
| `BuildCheckFailure.ts:186-198` | sin `GROUP BY`: todas las marcas del mes en Node | memoria y CPU de Node por petición |
| `BuildEmployeeExperience.ts:75-86` | `snapshot_date <= $2` **sin cota inferior** | `DISTINCT ON` sobre todo el histórico de `pattern_snapshots` (~2 000 filas/día): crece sin límite |
| `BuildOperatingCost.ts:254-289` (`computeWindow` ×2, `:620-621`) | agrega en SQL por empleado, sucursal y día | ~22 000 filas a Node por ventana; aceptable |
| `BuildBranchRisk.ts:114-145`, `loadDataHealth` (`:294-322`), `loadEmployeeProfiles` (`:592-612`) | agregan en SQL | aceptables |

**Síntoma**: el panel en blanco a los 120 s de nginx, y peor cada mes.

**Arreglo**:

1. Índice `checklogs_raw (entity_id, timestamp DESC)`. Primer día, misma migración que los
   de programadas.
2. `statement_timeout` de 30 s en el pool y `max` por variable de entorno. Una consulta
   desbocada no puede retener la conexión de los demás.
3. Reescribir las tres correladas (evolución, efecto de sucursal, comportamiento) como un
   solo paso: pre-agregar `cyc` por (ámbito, semana) y hacer `JOIN`, o funciones de ventana.
   Objetivo: una lectura de `marks` por constructor.
4. Geocerca y fallos de fichaje **en SQL**: contadores por sucursal y empleado agregados; a
   Node sólo las marcas fuera de valla, con tope, y el cruce con sucursales por caja
   delimitadora antes de Haversine. El cruce persona-persona se limita a N marcas.
5. Cota inferior en experiencia del empleado (90 días).
6. **Precalcular el resumen por entidad cada noche** en una tabla (`panel_overview_daily` o
   similar), con una task por entidad como en programadas, y servir de ahí. Es lo que ya hace
   el dashboard operativo con `operational_daily` (`BuildOperationalWeeks.ts:104-115`), que
   por eso es barato. En vivo sólo lo de hoy.
7. Mientras llega el precálculo, caché del resumen por (entidad, periodo) de 10 minutos.

### 2. El cierre diario y la vista de hoy

- `CloseDue.ts:44-53` cierra las sucursales **en serie**; cada `closeOperationalDay(branchId)`
  crea un repositorio nuevo (`BuildOperationalDay.ts:181`) que recarga `dim_employees` y
  `dim_calendars` enteras, y `loadLogs` (`:108-121`) lee los fichajes del día **de toda la
  entidad**, sin filtrar por sucursal. Con todas las sucursales en la misma zona horaria son
  300 × (tres consultas de dimensiones + ~4 000 filas) en un solo tick. Si el tick dura más de
  una hora, el siguiente se salta por el cerrojo `running`.
- `GET /panel/today` calcula el día en vivo en cada petición (`BuildOperationalDay.ts:71-90`;
  el bucle por sucursal es en memoria, no N+1).
- `GET /panel/alerts` vuelve a calcular el día operativo y la semana de disponibilidad
  (`alerts/BuildPanelAlerts.ts:39-41`) en cada carga del panel.

**Arreglo**: cargar dimensiones y fichajes del día **una vez por entidad** y cerrar todas sus
sucursales en una pasada; entidades en paralelo con `p-limit`; `/today` cacheado 60 s y
`/alerts` reutiliza ese resultado en vez de recalcular.

### 3. El trigger de patrones pierde datos cuando la gente sale junta

`onWhriteChecklog.ts:4-13` (512 MiB, tiempo por defecto, sin `maxInstances`) sólo actúa en
la salida válida (`writeController.ts:32-54`). Por salida: unas 10 lecturas (`:55-66`, `:117`,
`:144`, `:171`, `:217`) y 3 escrituras (`:115`, `:214`, `:261`), más la cascada:
`onWriteBranchPattern`/`onWriteEmployeePattern` (transacción sobre `pattern_history`, **tope
de 5 versiones al día**, las demás se descartan en silencio:
`patrones/FirestorePatternHistoryRepository.ts:13,32`), `onBranchPatternSync`/`onEmpPatternSync`
(tres `POST /build/pattern-snapshot` con **7 s** de margen, `sync/AnalyticsServerClient.ts:3,33`)
y `onChecklogSync` (un POST por escritura). Unas ocho invocaciones y cuatro llamadas HTTP por
salida. **El volumen lo aguanta**: mil salidas en diez minutos son ~16 000 lecturas.

Lo que no aguanta: el patrón de sucursal se **lee** (`:57-58`) y se **vuelve a escribir con
`set(merge)`** (`:115` → `FirestoreBranchRepository.ts:146`) **sin transacción**. Dos salidas
de la misma sucursal con cien milisegundos de diferencia leen el mismo `dataPoints` y
`totalCost`, y la última pisa a la primera. Sin error, sin reintento (los upserts de empleado
hacen `.catch(console.log)`, `:214`, `:261`), sin rastro. En limpieza las cuadrillas salen a la
vez. El trigger de tareas ya lo hace bien (`onWriteTaskForPattern.ts:54,99`, `runTransaction`).

**Arreglo**: `runTransaction` en los tres patrones como en tareas; dejar que la función falle
para que Firebase reintente (`retry: true`) en vez de tragarse el error; y los snapshots hacia
analytics por una cola con intentos, como pide ya el espejo de fichajes
([sync sin reintentos](../../deployment-prod/proximo-pase-back.md)), no por un POST con 7 s.

### 4. Merlin: dos agujeros concretos, no de volumen

Rutas `POST /api/v1/gpt/panel` y `/interpret` (`merlin.router.ts:14-42,44-90`). Las llama el
panel al montar (`front: .../dashboard/MerlinAssistant.tsx:211-216`, una pestaña a la vez,
`CheckbizStatsDashboard.tsx:170-174`); la ficha de sucursal manda **un solo** `branchId`
(`MerlinAssistant.tsx:168`). El servidor escribe `status: analysing` en
`ai-analizer/{md5(filtros)}`, devuelve 202 y hace la llamada en segundo plano
(`getOrCreateBranchAnalysis.ts:50-75`, `getOrCreatePanelAnalysis.ts:111-136`); el front escucha
el documento y se rinde a los **75 s** (`front: services/merlin.service.ts:91-108`). Modelo
`gpt-5-mini`, 6 000 tokens de salida en panel y 2 000 en sucursal; caché 24 h panel, 7 días
sucursal y empleado. En régimen son unas decenas de llamadas pequeñas al día: **barato**.

Los agujeros:

- La pestaña de sucursales mete **las 300 en el prompt** (`front: merlinPanelPayload.ts:39`,
  `panelAnalysis.builder.ts:299-310`); el tope de 6 000 tokens se midió con entidades pequeñas
  (`:31-46`). Si la respuesta sale inservible se guarda como `error` y **no se cachea**
  (`getOrCreatePanelAnalysis.ts:118-122`): cada visita vuelve a pagar.
- Si el contenedor se reinicia a mitad de un análisis, el documento se queda en `analysing`
  hasta que caduca, porque `isFresh` aplica la misma TTL (`getOrCreateBranchAnalysis.ts:45-47`,
  `getOrCreatePanelAnalysis.ts:120-122`): **7 días** en sucursal y empleado, 24 h en panel. El
  reintento del panel recibe `ai/analysing` y nunca relanza. El modelo caído sí está cubierto
  (`saveFailure` en el `catch`).
- `/interpret` no limita `branchIds` ni comprueba pertenencia (`merlin.router.ts:50-53`);
  `interpretBranches.ts:22-45` hace una llamada **por sucursal, en serie**, y
  `getOrCreateBranchAnalysis.ts:57` se queda con la primera. Hoy inofensivo porque el front
  manda una; con N paga N y guarda una.
- Se guarda la respuesta cruda entera en el documento (`openai.renderer.ts:39`).

**Arreglo**: en sucursales, top N por señal más un agregado del resto; cachear el `error` una
hora; tratar un `analysing` de más de 10 minutos como caducado y relanzar; `branchIds` a uno
y de la entidad del que pide; no guardar `raw`.

### 5. Barridos globales que crecen con la historia de todos los clientes

- `listActiveEntities` (`ReconcileChecklogs.ts:121-127`): `DISTINCT entity_id WHERE synced_at >= …`
  **sin índice en `synced_at`**, recorrido completo de `checklogs_raw` cada 30 minutos y cada
  hora. El índice ya está en programadas-a-escala.
- `StatsCron` (03:20, `harvestSnapshot.ts:171-177`): filtra por
  `(timestamp AT TIME ZONE $2)::date = $1`, que ningún índice puede usar: recorrido completo,
  global, cada noche. Se arregla calculando el rango en la aplicación y filtrando por
  `timestamp >= … AND timestamp < …`.
- `BuildEmployeeExperience` sin cota inferior (punto 1).

No rompen nada solos: hacen más lento el punto 1.

## Lo que no preocupa

La heurística (`POST /heuristic`) crece con el catálogo de indicadores, no con la plantilla, y
Merlin no la usa (`interpretBranches.ts:33`). El EMA es CPU pura por salida. Rentman,
inventario y ventas no dependen de empleados ni de fichajes.

---

## Pruebas

- **Entidad sintética en dev**: script que siembra en Postgres una entidad con 1 000 empleados,
  300 sucursales y un mes de fichajes (unas 45 000 marcas con geo). Sin esto nada de lo de
  arriba se puede medir.
- `EXPLAIN ANALYZE` de cada constructor antes y después. Objetivo del resumen completo:
  **menos de 3 s** y nunca más de 4 conexiones a la vez.
- Cinco peticiones de `/panel/overview` en paralelo: ninguna falla por conexión.
- Trigger: dos salidas de la misma sucursal con 50 ms de diferencia → `dataPoints` sube en
  dos, no en uno.
- Merlin: matar el contenedor a mitad de un análisis → a los 10 minutos el panel relanza.

## Plan de ejecución

- [ ] **Día 1** (compartido con programadas): migración con el índice `(entity_id, timestamp)`
      y los tres de programadas; `statement_timeout` y `max` por variable en el pool.
- [ ] **Día 2**: transacción en el trigger de patrones y `retry: true`; los tres arreglos de
      Merlin; caché de 10 minutos del resumen.
- [ ] **Días 3-4**: reescritura de evolución, efecto y comportamiento sin correladas; geocerca
      y fallos en SQL; cota en experiencia; filtro por rango en `StatsCron`.
- [ ] **Día 5**: cierre diario una pasada por entidad; `/today` cacheado y `/alerts` reutiliza.
- [ ] **Después**: precálculo nocturno del resumen por entidad (una task por entidad) y servir
      de tabla.
- [ ] **Producción**: en el pase. Fuera del código: la migración a mano, la variable del pool
      en `.env.production`, y el trigger con su nueva configuración desplegado por nombre.
      Anotado en [proximo-pase-back §9](../../deployment-prod/proximo-pase-back.md).

## Decisiones abiertas (Jose)

1. El periodo en curso del resumen: ¿en vivo con caché de 10 minutos, o también precalculado
   y se acepta que vaya con un día de retraso?
2. Tamaño del pool por servicio: ¿uno común o más grande sólo para analytics?
3. Merlin, pestaña de sucursales: ¿cuántas entran enteras en el prompt antes de agregar el resto?

## Referencias

- [programadas-a-escala](../programadas-a-escala/README.md): la migración de índices es la misma.
- [dashboard-operativo](../dashboard-operativo/README.md): `operational_daily`, el precedente del precálculo.
- [modulos/heuristica.md](../../modulos/heuristica.md) y [modulos/reporting-analitica.md](../../modulos/reporting-analitica.md).
- [deployment-prod/proximo-pase-back.md](../../deployment-prod/proximo-pase-back.md) §9.

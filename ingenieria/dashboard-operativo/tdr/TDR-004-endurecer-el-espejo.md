# TDR-004 — Endurecer el espejo: conciliación de fichajes y cron de dimensiones

**Fecha:** 2026-10-10
**Estado:** Diseño
**Componente:** `services/analytics` (`src/application/ReconcileChecklogs.ts`, `src/jobs/scheduler.ts`, ruta `POST /api/analytics/reconcile/checklogs`) · `@encodebiz/shared` (`mirror/checklogsRaw.ts`)

> **Implementado el 2026-10-11 (`cf05643`) con un cambio:** la conciliación vive en `analytics`
> y no en `sync`, porque `sync` no tiene montadas las credenciales de Firebase y dárselas exigía
> tocar los dos compose. El upsert pasó a `shared` y lo usan los dos.
**Decisión de referencia:** [ADR-001](../adr/ADR-001-postgres-es-la-fuente-del-ahora.md)

---

## Por qué va primero

Con [ADR-001](../adr/ADR-001-postgres-es-la-fuente-del-ahora.md) el espejo deja de ser un
insumo de estadística y pasa a ser **lo que el gerente ve**. Hoy tiene dos agujeros medidos
([01_as-is §3](../01_as-is.md)):

1. El trigger de fichajes **no reintenta**. Si el contenedor no responde en 7 s, el registro no
   llega nunca y nadie lo sabe. En dev, cero fallos en 7 días; en producción, sin medir.
2. Las dimensiones **no se refrescan solas**. Un empleado dado de alta ayer no está en
   `dim_employees` hasta que alguien llame al sync. En el dashboard sería un «fichó sin estar
   previsto» que sí estaba previsto.

Ninguno de los dos se arregla tocando Firebase: los dos se arreglan desde el contenedor,
leyendo Firestore fuera de la ruta caliente. Es la única lectura de Firestore que este proyecto
añade, y es «inevitable» en el sentido de Jose: no hay otra forma de saber qué falta.

## 1. Conciliación de fichajes (`sync`)

### Qué hace

Para una entidad y una ventana de `hours` horas:

1. Firestore: `entities/{e}/checklogs` con `timestamp >= ahora − hours`, **sólo ids**
   (`select()` sin campos: la lectura más barata que existe y un único round trip por página).
2. Postgres: `SELECT id FROM checklogs_raw WHERE entity_id = $1 AND timestamp >= $2`.
3. Diferencia: los ids de Firestore que no están en Postgres.
4. Para los que faltan, `getAll` por lotes de 100 y el **mismo upsert** de `POST /sync/checklogs`
   (se extrae a una función compartida en el propio servicio; no se duplica el SQL).
5. `INSERT INTO sync_log (source, source_id, entity_id, status) VALUES ('reconcile', '<n missing>', $1, 'success')`,
   y en `error_message` —aunque sea `success`— el resumen `scanned/missing/pulled/failed` para
   que `freshness.reconcile` lo lea sin otra tabla.

**No borra nada.** Un fichaje borrado en Firestore sigue en Postgres: el trigger ignora
borrados a propósito y la conciliación respeta ese criterio.

### Cuándo

Tareas del planificador de `analytics` (`setInterval`, sin dependencia nueva):

| Pasada | Cron (UTC) | Ventana | Para qué |
|---|---|---|---|
| Corta | `*/30 * * * *` | 2 h | Lo que el trigger perdió hace un rato |
| Larga | `30 3 * * *` | 48 h | Red para cortes largos del contenedor y para la hora corregida que llega tarde |

Entidad a entidad, sólo las que tienen fichajes en Postgres en los últimos 30 días (las demás
no tienen nada que conciliar). Para 60 entidades y 2 h de ventana son 60 consultas de ids
pequeñas cada media hora: despreciable.

### La ruta

`POST /api/analytics/reconcile/checklogs?entityId=…&hours=48` (S2S) ejecuta lo mismo bajo demanda y
devuelve `{ ok, scanned, missing, pulled, failed }`. Con `&dryRun=true` cuenta y no escribe:
es lo que usa la fase 0-bis para medir el agujero en producción con `hours=168`. Sin
`dryRun`, trae lo que falta; sirve después de un corte.

### Qué se ve

- `freshness.reconcile = { lastRunAt, missing }` en `/today`. `missing > 0` tras una pasada
  es una pasada que no terminó de traer: el front avisa, no oculta.
- `sync_log` queda como registro: cuántos faltaron cada vez. Si una entidad pierde fichajes a
  diario, el problema es el trigger o la red, y el dato para la conversación está ahí.

## 2. Cron de dimensiones (`analytics`)

`SyncDimensions` ya existe y ya sabe sincronizar una entidad. Lo que falta es quien lo llame:

- Tarea del planificador de `analytics` al minuto :20 de cada hora UTC: para cada entidad con fichajes o tareas en
  Postgres en los últimos 30 días, `syncDimensions(entityId)`. Secuencial, con el `dim_sync_log`
  de siempre.
- Una pasada completa (`--all`) el día del arranque y en cada pase a producción.

**Por qué un cron y no escritura directa como inventario.** Escritura directa sería lo
correcto: `employees`, `branches` y `calendar` ya se escriben desde contenedores. Pero son
tres servicios y tres repositorios, y el dashboard no puede esperar a tocarlos. El cron da una
frescura de una hora hoy; la escritura directa, cuando llegue, la baja a segundos y el cron
queda de red, como `remirror`. Se anota como deuda en [04_fases](../04_fases.md).

Lo que una hora de retraso significa en pantalla, para que nadie lo descubra en producción:

| Cambio | Hasta el siguiente sync |
|---|---|
| Empleado nuevo que ya ficha | Aparece en `unexpected` del centro, con su nombre si el fichaje lo trae; si no, con su id |
| Baja de empleado | Sigue en `expected` → un `no_log` de más |
| Cambio de horario o ausencia nueva | El `expected` de hoy no lo refleja |
| Centro nuevo | Sus fichajes se agrupan bajo un centro sin nombre |

Ninguno miente sobre quién fichó. Todos se corrigen solos en menos de una hora. Y el front
enseña `freshness.dimensions.syncedAt`.

## 3. Qué no se toca

- El trigger `onChecklogSync` del SaaS. Sigue igual; la conciliación lo cubre por detrás.
  Añadirle reintentos sería mejor, y es otro repo y otro despliegue: se anota en
  [04_fases](../04_fases.md) como mejora de `encodeBiz-SAAS`.
- `POST /sync/checklogs`. Mismo upsert; se refactoriza a función compartida sin cambiar el SQL.

## 4. Verificación (fase 1b y 1c)

- Borrar a mano una fila de `checklogs_raw` en dev, lanzar `reconcile` con `hours=24`: vuelve,
  y `sync_log` lo cuenta. Con `dryRun=true`, lo cuenta y no vuelve. Caso QA **DAS-02**.
- Dar de alta un empleado en dev y esperar al :20: aparece en `dim_employees` sin que nadie
  llame. `dim_sync_log` muestra una fila por entidad y hora.
- En producción, fase 0-bis: `reconcile` en `dryRun` con `hours=168` sobre la entidad más
  grande. El `missing` que devuelva es el tamaño del agujero, y se anota en
  [04_fases](../04_fases.md).

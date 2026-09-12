# Catálogo de listeners, programadas y snapshots — entorno de desarrollo

> **Verificación (2026-09-11).** Este catálogo sale de un análisis estático, filtrado con lo
> que está desplegado de verdad en `dev-encodebiz` (funciones y jobs de Cloud Scheduler
> listados ese día), y antes de publicarlo se ha comprobado por muestreo. Confirmado:
>
> - Los **25 triggers** de Firestore desplegados en desarrollo están los 25 en la sección 1, y
>   no falta ninguno.
> - **Cada fichaje sale dos veces por webhook** en desarrollo: el contenedor lo emite al crear
>   el fichaje y `onChecklogWebhook` sigue activo. Registrado como HAL-02.
> - La sucursal automática la crea **`onActivateCheckbiz`** al nacer
>   `entities/{eid}/subscriptions/{sid}`, y está activo en desarrollo.
> - El barrido de cuentas fantasma **solo simula en desarrollo**: la función desplegada tiene
>   `MAINTENANCE_GHOST_APPLY` vacía, y `esCierto('')` es `false`
>   (`encodebiz-api/services/firebase_sdk/src/maintenance/config.ts:12`). No borra usuarios
>   de las pruebas.
> - La facturación del día 5 sigue programada en desarrollo. Registrado como HAL-05; ninguna
>   prueba la fuerza.
>
> Lo que no aparece aquí como confirmado es lectura del código, no comprobación.

Fecha del análisis: 2026-09-11. Análisis estático; no se ha ejecutado nada ni se ha hecho ninguna petición de red.

**Alcance.** Solo lo que está **activo en desarrollo**:

- **Cloud Functions:** solo lo que aparece en `dev-funciones-desplegadas.csv` (25 triggers de Firestore activos) y en `dev-programadas.csv` (9 jobs de Cloud Scheduler, todos ENABLED).
- **Contenedores:** lo que arranca solo al iniciar un servicio que está en `docker-compose.staging.yml`.
- Lo que existe en el código y no está desplegado va en una lista al final.

**Abreviaturas de ruta**

- `SAAS/` = `PLATAFORMA/encodeBiz-SAAS/functions/src/`
- `API/` = `PLATAFORMA/encodebiz-api/`

**Nombres desplegados.** La exportación va anidada en `apiV100` (`SAAS/index.ts:20-31`), así que el nombre desplegado es `apiV100-<grupo>-<export>`.

- Grupos de triggers:
  - `firebaseFirestoreTriggers` (`SAAS/firebase-firestore-trigger/index.ts:8-15`).
  - `firebaseFirestoreTriggersCheckinBiz` (`SAAS/services-saas/checkinbiz/firebase-firestore-trigger/index.ts:16-32`).
  - `firebaseFirestoreTriggersPassinbiz` (`SAAS/services-saas/passinbiz/firebase-passinbiz-trigger/index.ts:7-13`).
- Grupos de programadas:
  - `firebaseEntrySchedule` (`SAAS/core/firebase-entry-schedule/index.ts:9-13`).
  - `scheduleCheckbiz` (`SAAS/services-saas/checkinbiz/firebase-entry-schedule/index.ts:7-14`).
- `ghostUsersMaintenance` no va anidado: lo despliega otro codebase, `triggers`, desde `API/firebase.json:2-13` y `API/services/firebase_sdk/src/index.ts:41`.

**Regiones**

- Todos los triggers de Firestore declaran `europe-west1`.
- Las programadas no declaran región y no hay `setGlobalOptions`, así que van a `us-central1`, que es lo que dice el CSV.
- Las programadas sin `timeZone` corren en UTC, que también es lo que dice el CSV.

**Cómo se observa desde una prueba.** La suite `API/qa` ya tiene service account de `dev-encodebiz` (`API/qa/README.md`, sección «Credenciales»), así que puede leer Firestore con el SDK de administración.

- **Postgres** (`encodebiz_staging`) solo se ve dentro de la red `encodebiz-dev`.
- **Endpoints S2S** (`X-Encodebiz-Key`): algunas tablas se ven desde fuera por endpoints S2S que pasan por el nginx de dev (`http://141.95.47.135:8080`). Esa clave **no** está entre las credenciales que lista `qa/README.md`; habría que añadir la `ENCODEBIZ_API_KEY` de dev.
- **Endpoints de usuario** (token de Firebase): otras tablas se ven por endpoints de usuario.

**Aviso de entorno.** Los triggers que llaman a los contenedores (LIS-02, LIS-09, LIS-10, LIS-13) atrapan el error y solo lo escriben en el log. Si el nginx de dev no se reinicia tras un `up -d` (gotcha de `API/CLAUDE.md`), esas llamadas dan 502 y el efecto no llega, sin que nadie lo vea salvo en Cloud Logging.

---

## 1. Listeners de Cloud Functions (25, todos desplegados en dev)

### Checkinbiz

## LIS-01 · onChecklogWrite (patrones al cerrar jornada)
- **Tipo:** trigger Firestore onWrite sobre `/entities/{eid}/checklogs/{chid}`, con 512 MiB.
- **Dónde:**
  - Trigger: `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/onWhriteChecklog.ts:4-14`.
  - Controlador: `.../dataProcessing/writeController.ts:35-262`.
  - Desplegado como `apiV100-firebaseFirestoreTriggersCheckinBiz-onChecklogWrite`.
- **Qué lo dispara:** cualquier escritura en un fichaje. Solo actúa cuando el fichaje **pasa a ser** un checkout con `status=valid` y `isSuspect=false`:
  - La condición está en `writeController.ts:32-33`.
  - Si el `before` ya lo era, lo ignora (`:53-54`).
- **Qué hace:**
  - Exige que ya exista el patrón de la sucursal (`:55-56`).
  - Reconstruye el ciclo con los fichajes válidos que comparten `checkin` (`:63-67`).
  - Recalcula el patrón de la sucursal: EMA, desviaciones, coste y `profileType` (`:76-115`).
  - Si faltan, crea los patrones de empleado, el de sucursal y el global, con `source:init_config` (`:117-168`).
  - Después los recalcula (`:171-214` y `:217-261`).
- **Qué deja escrito:**
  - `checkbiz_branch_patterns/{branchId}`, con `dataPoints+1`, `source:"update"` y `updatedAt`. Repositorio: `SAAS/.../repository/FirestoreBranchRepository.ts:118-122`.
  - `checkbiz_employee_patterns/{docId}`, en dos documentos: `{employeeId}_{branchId}_{entityId}` y `{employeeId}_{entityId}`. El formato del id se deduce de `onWriteTaskForPattern.ts:91-92`; en el repositorio (`FirestoreEmployeeRepository.ts:220`) no se ha confirmado.
- **Cómo se comprueba:** leer `checkbiz_branch_patterns/{branchId}` con el SDK de administración, comprobar que `dataPoints` subió en 1 y que `updatedAt` es posterior al checkout. Luego leer los dos documentos de empleado.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** crear un checkout válido de 3 a 10 h tras el checkin (`POST /api/v1/checkinbiz/checklogs`). Reescribir el mismo documento no vuelve a disparar la acumulación, por la guarda de transición.
- **Criticidad:** alta. Es el origen de todos los patrones, de su histórico y de los snapshots de Postgres, y lo que alimenta a Merlin.
- **Sospechas:**
  - Si la sucursal no tiene patrón porque LIS-05 falló o la sucursal es anterior a él, **nunca** se generan patrones de esa sucursal y no queda rastro (`:55-56`).
  - Un checkout de menos de 3 h o más de 10 h sale `isSuspect=true` (`API/services/checkinbiz/src/application/use-cases/checklog/CreateChecklog.ts:73-77`) y se descarta aquí. En una prueba hay que respetar esa ventana.

## LIS-02 · onChecklogSync (fichaje → Postgres)
- **Tipo:** trigger Firestore onWrite sobre `/entities/{eid}/checklogs/{chid}`.
- **Dónde:**
  - Trigger: `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onChecklogSync.ts:5-23`.
  - Carga útil: `SAAS/core/analytics/infrastructure/SyncChecklogService.ts:28-81`.
  - Cliente HTTP: `.../AnalyticsServerClient.ts:5-16` y `:25-27`, con `X-Encodebiz-Key` y timeout de 7 s.
  - Desplegado.
  - `ANALYTICS_SERVER_URL` y `ANALYTICS_API_KEY` están definidas en `functions/.env.dev-encodebiz`; solo se ha comprobado que existen, no su valor.
- **Qué lo dispara:** cualquier alta o modificación de un fichaje, en cualquier estado (válido, `failed`, `incomplete_workday`). Los borrados se ignoran (`:9`).
- **Qué hace:** manda el fichaje serializado por POST a `{ANALYTICS_SERVER_URL}/api/sync/checklogs`, que atiende LIS-26.
- **Qué deja escrito:** en Postgres, una fila en `checklogs_raw` (upsert por `id`) y otra en `sync_log`. Lo detalla LIS-26.
- **Cómo se comprueba:**
  - Dentro del servidor: `SELECT status, closed FROM checklogs_raw WHERE id='<chid>'`.
  - Desde fuera no hay lectura directa de la fila. Se ve indirectamente:
    - Por el panel de analytics, con token de Firebase: `POST /api/analytics/panel/stats` y `GET /api/analytics/panel/overview`, que leen `checklogs_raw`.
    - Por reports, tras PRG-10.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** escribir o actualizar el fichaje. El reenvío es idempotente, por el upsert.
- **Criticidad:** alta. Sin esto, informes (PRG-10), panel, backoffice y Rentman no ven fichajes.
- **Sospechas:**
  - Un fallo solo va a `console.error` (`:14-21`) y no se reintenta: la fila se pierde hasta la siguiente escritura de ese fichaje.
  - Los borrados no se propagan, así que la limpieza de una prueba deja residuo en Postgres.

## LIS-03 · onChecklogWebhook (webhook de fichaje por la vía Firebase)
- **Tipo:** trigger Firestore onWrite sobre `/entities/{eid}/checklogs/{chid}`.
- **Dónde:**
  - Trigger: `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onChecklogWebhook.ts:17-44`.
  - Emisor: `SAAS/services-saas/checkinbiz/webhook-events.ts:8-19`.
  - Cola: `SAAS/core/webhook/emit.ts:21-65`.
  - Desplegado.
- **Qué lo dispara:** la transición de un fichaje a `status=valid`, solo para `checkin` y `checkout` (`:7-10` y `:25-33`).
- **Qué hace:** lee `entities/{eid}/webhook_endpoints` con `enabled==true` (`emit.ts:35-38`). Por cada endpoint suscrito con coincidencia exacta del tipo (`:47`), encola una entrega `attendance.clock_in` o `attendance.clock_out`.
- **Qué deja escrito:** `entities/{eid}/webhook_outbox/{id}` con `status:"pending"`, `attempt:0` y `nextAttemptAt:now` (`emit.ts:49-60`). La entrega real la hace PRG-02.
- **Cómo se comprueba:** registrar un endpoint suscrito y leer `entities/{eid}/webhook_outbox` con el SDK de administración.
- **Latencia esperable:** segundos para encolar; la entrega llega en 1 minuto o menos (PRG-02).
- **Cómo forzarlo en desarrollo:** crear un fichaje válido.
- **Criticidad:** media. Solo afecta a entidades con webhooks; es un efecto hacia terceros.
- **Sospechas:** **doble emisión**. El contenedor ya emite `attendance.clock_in` y `attendance.clock_out` al crear el fichaje:
  - Emisión en `API/services/checkinbiz/src/events/attendance.ts:73-78`, llamada desde `API/services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts:531`.
  - Va a la cola de Postgres (LIS-29).
  - Los dos caminos leen la misma colección `webhook_endpoints`.

  Resultado: un endpoint suscrito recibe cada fichaje **dos veces**, con distinto `id` de evento y distinto formato:
  - Firebase manda el fichaje en crudo y en camelCase (`onChecklogWebhook.ts:36`).
  - El contenedor manda snake_case (`attendance.ts:50-66`).

  `API/services/firebase_sdk/src/index.ts:58-60` dice que `attendance.*` «ya no pasa por Firebase», pero este trigger sigue exportado y activo (línea 21 del CSV).

## LIS-04 · onCreateEmployee (acceso y bienvenida por la vía antigua)
- **Tipo:** trigger Firestore onCreate sobre `entities/{entityId}/employees/{employeeId}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onCreateEmployee.ts:4-7`. Controlador: `SAAS/services-saas/checkinbiz/interfaces/triggers/onCreateEmployee.controller.ts:11-125`. Desplegado.
- **Qué lo dispara:** crear la ficha de un empleado.
- **Qué hace:**
  - Sale sin hacer nada si la ficha trae `uid`, que es el alta del contenedor (`:29`), o si viene `status:"pending"` (`:44`).
  - Si no, crea o actualiza el usuario de Auth con una contraseña de 6 dígitos (`:63-81`).
  - Guarda `uid` y `customToken` en la ficha (`:83-85`).
  - Indexa en `searchIndex` (`:97-106`).
  - Manda el correo `WELLCOME_EMPLOYEE` por SMTP (`:107-123`).
- **Qué deja escrito:**
  - Solo por la vía antigua: el usuario de Auth, los campos `uid` y `customToken` en la ficha, `searchIndex/{docId}` y un correo real.
  - Por la vía del contenedor, **nada**.
- **Cómo se comprueba:**
  - Alta por el contenedor: comprobar que la ficha **no** cambia tras unos segundos, es decir, que conserva el `uid` con el que nació y no aparece un `customToken` nuevo.
  - Alta por la vía antigua: leer la ficha y comprobar `uid` y `customToken`.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** crear un empleado sin `uid`. La HTTP antigua `apiV100-firebaseEntryHttp-checkinbiz-createEmployee` sigue desplegada (línea 40 del CSV).
- **Criticidad:** media. En la vía nueva es un «no hacer nada» que evita la segunda bienvenida.
- **Sospechas:** si una prueba escribe la ficha directamente con el SDK, sin `uid`, dispara un correo real y un usuario de Auth.

## LIS-05 · onCreateBranch (patrón inicial de sucursal)
- **Tipo:** trigger Firestore onCreate sobre `entities/{entityId}/branches/{branchId}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/onCreateBranch.ts:12-25`. Patrón: `SAAS/services-saas/checkinbiz/application/patterns/buildInitialBranchPattern.ts:42-62`. Desplegado.
- **Qué lo dispara:** crear una sucursal, sea por el contenedor (`POST /api/v1/branches`), por la sucursal automática de LIS-06 o por la HTTP antigua `checkinbiz-createBranch`.
- **Qué hace:** si no existe patrón (idempotente, `:14`), escribe el patrón inicial.
- **Qué deja escrito:** `checkbiz_branch_patterns/{branchId}` con `source:"init_config"`, `dataPoints:0` y `reliability:0.1`. Esa escritura dispara LIS-07 y LIS-09.
- **Cómo se comprueba:** leer `checkbiz_branch_patterns/{branchId}` y comprobar que existe con `dataPoints==0`.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** crear una sucursal.
- **Criticidad:** alta. Sin este documento, LIS-01 no calcula nada para esa sucursal.
- **Sospechas:** usa `branch.id` del **contenido** del documento (`:23`, `buildInitialBranchPattern.ts:43`).
  - Los dos repositorios que crean sucursales lo escriben: `API/packages/shared/src/checkbiz/repositories/FirestoreBranchRepository.ts:14-18` y `SAAS/.../FirestoreBranchRepository.ts:11-18`.
  - Pero una sucursal escrita a mano sin campo `id` rompería el patrón.

## LIS-06 · onActivateCheckbiz (sucursal automática al contratar)
- **Tipo:** trigger Firestore onCreate sobre `/entities/{eid}/subscriptions/{sid}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onActivateCheckbiz.ts:6-14`. Controlador: `SAAS/services-saas/checkinbiz/interfaces/triggers/createEntityBranch.controller.ts:116-183`. Desplegado.
- **Qué lo dispara:** crear la suscripción de `serviceId=="checkinbiz"`. Hoy la crea `POST /api/v1/billing/subscriptions` (`API/services/billing/src/application/Subscribe.ts:38`), que escribe `entities/{e}/subscriptions/{serviceId}` según `FirestoreSubscriptionRepository.ts:50-51`.
- **Qué hace:**
  - Si la entidad no tiene ninguna sucursal (`:124-127`), crea una con el nombre y la dirección legal de la entidad: radio 500 y horario de 8 a 17 (`:129-153`).
  - La valida (`:154-164`), la crea (`:165`) y la indexa (`:167-176`).
- **Qué deja escrito:** `entities/{e}/branches/{id}` y `searchIndex`. Eso dispara LIS-05 y, detrás, LIS-07 y LIS-09.
- **Cómo se comprueba:** tras suscribir, consultar `entities/{e}/branches` y comprobar que hay una sucursal con `name` igual al de la entidad.
- **Latencia esperable:** segundos, y otros segundos para el patrón.
- **Cómo forzarlo en desarrollo:** crear la suscripción con la entidad sin sucursales.
- **Criticidad:** alta. Sin sucursal no hay dónde fichar.
- **Sospechas:**
  - Exige `entity.legal.address` con calle, país, zona horaria y geo. `POST /api/v1/entities` no lo pide (`API/services/entities/src/interfaces/http/entity.router.ts:56-78`).
  - Si la suscripción llega antes del `update` con datos legales, la sucursal se rechaza con un `console.error` y ya no se vuelve a intentar (onCreate).
  - Esta vía no emite `branch.created`, cosa que sí hace la del contenedor.

## LIS-07 · onBranchPattern (histórico del patrón de sucursal)
- **Tipo:** trigger Firestore onWrite sobre `checkbiz_branch_patterns/{branchId}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onWriteBranchPattern.ts:6-26`. En el código se exporta como `onWriteBranchPattern` y en el índice como `onBranchPattern`. Repositorio: `SAAS/services-saas/checkinbiz/infrastructure/repository/FirestorePatternHistoryRepository.ts:13-48`. Desplegado.
- **Qué lo dispara:** cualquier escritura del patrón de sucursal: LIS-05, LIS-01 o LIS-11.
- **Qué hace:** añade la foto completa del patrón como una versión del día.
- **Qué deja escrito:** `pattern_history/{branchId}_{YYYY-MM-DD}` con `versions.{isoTimestamp}`. Guarda como máximo 5 versiones al día (`:11` y `:33`).
- **Cómo se comprueba:** leer `pattern_history/{branchId}_{fecha UTC}` y contar las claves de `versions`.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** escribir el patrón, es decir, crear una sucursal o cerrar una jornada.
- **Criticidad:** baja. Es histórico.
- **Sospechas:** a partir de la sexta escritura del día no se guarda nada, y lo hace en silencio.

## LIS-08 · onEmpPattern (histórico del patrón de empleado)
- **Tipo:** trigger Firestore onWrite sobre `checkbiz_employee_patterns/{docId}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onWriteEmployeePattern.ts:6-27`. Desplegado como `onEmpPattern`.
- **Qué lo dispara:** escrituras de patrones de empleado: LIS-01, LIS-11 y LIS-12.
- **Qué hace y qué deja escrito:** igual que LIS-07, en `pattern_history/{docId}_{YYYY-MM-DD}`.
- **Cómo se comprueba:** leer ese documento.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** cerrar una jornada.
- **Criticidad:** baja.
- **Sospechas:** un solo checkout escribe cada patrón de empleado hasta dos veces, al crearlo y al actualizarlo (`writeController.ts:119/146` y `:214/261`). El tope de 5 al día se alcanza pronto.

## LIS-09 · onBranchPatternSync (patrón de sucursal → Postgres)
- **Tipo:** trigger Firestore onWrite sobre `checkbiz_branch_patterns/{branchId}`.
- **Dónde:**
  - Trigger: `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onBranchPatternSync.ts:5-32`.
  - Cliente: `SAAS/core/analytics/infrastructure/AnalyticsServerClient.ts:33-35`.
  - Desplegado.
- **Qué lo dispara:** cualquier escritura del patrón de sucursal.
- **Qué hace:** manda por POST `{entityId, branchId, snapshotDate: hoy en UTC, rawPattern}` a `/api/analytics/build/pattern-snapshot`, que atiende LIS-28.
- **Qué deja escrito:** una fila en `pattern_snapshots` de Postgres, en upsert por día.
- **Cómo se comprueba:** desde fuera, con la clave S2S: `GET /api/analytics/patterns/history?entityId=X&branchId=Y&days=7` (`API/services/analytics/src/interfaces/analytics.router.ts:55-126`).
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** escribir el patrón.
- **Criticidad:** media. Alimenta la tendencia y Merlin.
- **Sospechas:** el fallo solo va al log (`:23-30`).

## LIS-10 · onEmpPatternSync (patrón de empleado → Postgres)
- **Tipo:** trigger Firestore onWrite sobre `checkbiz_employee_patterns/{docId}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onEmployeePatternSync.ts:5-34`. Desplegado.
- **Qué lo dispara:** escrituras de patrones de empleado.
- **Qué hace:** lo mismo que LIS-09, con `employeeId`. `branchId` va a null en el patrón global.
- **Qué deja escrito:** una fila en `pattern_snapshots` con `employee_id`.
- **Cómo se comprueba:** `GET /api/analytics/patterns/history?entityId=X&employeeId=Z`, con la clave S2S.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** cerrar una jornada.
- **Criticidad:** media.
- **Sospechas:** las mismas que LIS-09.

## LIS-11 · onTaskPattern (señales de tareas en los patrones)
- **Tipo:** trigger Firestore onWrite sobre `entities/{entityId}/tasks/{taskId}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onWriteTaskForPattern.ts:150-182`. En el código es `onWriteTaskForPattern`. Desplegado.
- **Qué lo dispara:** que la tarea **pase** a `validated` o `rejected` (`:158-163`), con `branchId`. El resto de escrituras se ignoran.
- **Qué hace:** actualiza con EMA `taskSignals` y `profileType`:
  - En el patrón de la sucursal (`:48-80`).
  - En los dos patrones de cada asignado (`:85-129`).
  - Si el patrón no existe, no hace nada (`:56` y `:101`).
- **Qué deja escrito:** `checkbiz_branch_patterns/{branchId}.taskSignals` y `checkbiz_employee_patterns/{…}.taskSignals`. Eso dispara LIS-07 a LIS-10.
- **Cómo se comprueba:** validar la tarea y leer `taskSignals.taskCount` en los patrones.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** validar o rechazar una tarea.
- **Criticidad:** media.
- **Sospechas:** a un empleado que aún no ha cerrado ninguna jornada no se le crea patrón (lo crea LIS-01), así que esta señal se pierde.

## LIS-12 · onWriteTaskRating (agregado de valoraciones)
- **Tipo:** trigger Firestore onWrite sobre `/entities/{entityId}/tasks/{taskId}/ratings/{employeeId}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onWriteTaskRating.ts:113-155`. Desplegado.
- **Qué lo dispara:** valorar a un trabajador. El contenedor escribe `ratings/{employeeId}` en `API/services/tasks/src/infrastructure/repository/FirestoreTaskRepository.ts:195`.
- **Qué hace:**
  - Aplica el delta de estrellas en transacción a la ficha del empleado (`:71-111`).
  - Actualiza `taskSignals.avgRating`, `ratingCount` y `ratingTrend` en sus patrones (`:30-69`).
- **Qué deja escrito:** `entities/{e}/employees/{id}.ratingTask{average,count,sum,stars,updatedAt}` (SNP-09) y `checkbiz_employee_patterns/*.taskSignals`.
- **Cómo se comprueba:** leer `ratingTask` de la ficha.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** valorar una tarea.
- **Criticidad:** media.
- **Sospechas:** ninguna concreta.

## LIS-13 · onTaskRatingSync (valoración → Postgres)
- **Tipo:** trigger Firestore onWrite sobre `/entities/{entityId}/tasks/{taskId}/ratings/{employeeId}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onTaskRatingSync.ts:5-34` y `SAAS/core/analytics/infrastructure/SyncTaskRatingService.ts:22-40`. Desplegado.
- **Qué lo dispara:** valorar, con una nota entre 0 y 5 distinta de 0 (`:10-11`).
- **Qué hace:** manda por POST a `/api/sync/task-ratings`, que atiende LIS-27.
- **Qué deja escrito:** `task_ratings_raw`, con `id={taskId}_{employeeId}`.
- **Cómo se comprueba:** dentro del servidor, con SQL. Desde fuera, de forma indirecta, por el panel de analytics, que lee `task_ratings_raw`.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** valorar.
- **Criticidad:** baja.
- **Sospechas:** el fallo solo va al log.

## LIS-14 · onCreateIssues (aviso de incidencia)
- **Tipo:** trigger Firestore onCreate sobre `/issues/{id}`.
- **Dónde:**
  - Trigger: `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onCreateIssues.ts:41-79`.
  - Destinatarios: `:14-39`.
  - Envío: `SAAS/services-saas/checkinbiz/application/notifications/CheckbizOperationals.ts:169-215`.
  - Desplegado.
- **Qué lo dispara:** crear una incidencia. La crea PRG-07 al detectar una jornada incompleta, o el front o la app. En el contenedor no se ha encontrado quien escriba `issues`.
- **Qué hace:** resuelve los destinatarios, que son el trabajador si `toRole=="worker"` o los responsables de la sucursal según su rol, y les manda un push `issueReceived`.
- **Qué deja escrito:** un push por FCM y, siempre, un documento `in_app_notifications/{id}` con `entityId`, `employeeId`, `uid`, `type`, `module` y `createdAt`. La colección está en `SAAS/core/notifications/infrastructure/FirestoreAppNotificationsRepository.ts:14`.
- **Cómo se comprueba:** consultar `in_app_notifications` con `employeeId==X` y `createdAt` posterior a la incidencia. El push como tal no se puede observar.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** crear un documento en `issues`.
- **Criticidad:** media.
- **Sospechas:** si faltan destinatarios, solo deja un `logger.info` y no se crea nada.

## LIS-15 · onIssuesResponse (aviso de respuesta)
- **Tipo:** trigger Firestore onCreate sobre `/issues/{id}/responses/{rid}`.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onCreateIssues.ts:81-108`. Desplegado.
- **Qué lo dispara:** responder a una incidencia.
- **Qué hace:** manda al empleado de la incidencia un push `issueResponseReceived`.
- **Qué deja escrito:** `in_app_notifications` y un push.
- **Cómo se comprueba:** `in_app_notifications` con el `employeeId` de la incidencia.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** crear una respuesta.
- **Criticidad:** baja.
- **Sospechas:** ninguna.

### Núcleo

## LIS-16 · onDocumentWriteSubscriptions (correo de servicio activado o cancelado)
- **Tipo:** trigger Firestore onWrite sobre `/entities/{eid}/subscriptions/{sid}`.
- **Dónde:** `SAAS/firebase-firestore-trigger/subscriptions/onDocumentWrite-subscriptions.ts:5-19`. Controlador: `SAAS/core/subscriptions/interfaces/subscriptionsWrite.controller.ts:55-113`. Desplegado.
- **Qué lo dispara:** un cambio de `status` de la suscripción (`:13`). Al crearse pasa de `undefined` a `pending` y no manda nada. Al pasar a `active`, manda.
- **Qué hace:**
  - Con `status=="active"`, manda el correo SUBSCRIBE a `entity.billingEmail` (`:76-82` y `:108`).
  - Con `cancel_at` puesto, manda el correo CANCELLED y, si el plan es de pago por uso, genera un enlace de cobro en Stripe y marca `pending-pay` (`:19-53` y `:84-97`).
- **Qué deja escrito:** un correo real por SMTP. Si se cancela, además una sesión de checkout en Stripe y el cambio del documento a `status:"pending-pay"`.
- **Cómo se comprueba:** no se puede observar en Firestore; el correo solo se ve en el buzón o en los logs. La parte de Stripe se ve en el `status` del documento de la suscripción.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** suscribir con un plan freemium o de pago por uso, que queda `active` al instante (`Subscribe.ts:66`).
- **Criticidad:** media. Tiene efecto externo, un correo al cliente.
- **Sospechas:** **correo duplicado**. El contenedor de billing ya manda «Servicio Activado» al suscribir (`API/services/billing/src/application/BillingNotifier.ts:13-20`, llamado desde `Subscribe.ts:69`). Con planes freemium o de pago por uso, el cliente recibe dos.

## LIS-17 · processInvoices (factura del ciclo en Stripe)
- **Tipo:** trigger Firestore onCreate sobre `/entities/{eid}/invoices/{iid}`.
- **Dónde:** `SAAS/firebase-firestore-trigger/subscriptions/processInvoices.ts:5-13`, `SAAS/core/subscriptions/interfaces/processInvoices.controller.ts:12-27` y `SAAS/core/subscriptions/application/InvoicePaymentProcessor.ts:15-107`. Desplegado.
- **Qué lo dispara:** crear un documento de factura. Hoy solo lo hace PRG-03, el día 5.
- **Qué hace:** si no hay nada que facturar, marca la factura `SKIPPED_TRIAL` o `CANCELLED` (`:56-58`). Si lo hay, crea la factura en Stripe, añade las líneas y la finaliza (`:68-99`). Si falla, la borra y marca `FAILED` (`:106-107`).
- **Qué deja escrito:** el `status` de la factura en Firestore (`PROCESSING`, `FAILED`, etc.) y la factura en la cuenta Stripe de dev, lo que a su vez provoca el webhook `invoice.finalized` hacia LIS-32.
- **Cómo se comprueba:** leer `entities/{e}/invoices/{iid}.status`.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** crear un documento de factura a mano. **No recomendado**, porque toca Stripe.
- **Criticidad:** alta en producción. En una prueba, evitarlo.
- **Sospechas:** convive con billing, que según `docker-compose.staging.yml:316-319` es quien decide los cobros. Ver PRG-03.

## LIS-18 · onCreateSentEmail (correo por cola de Firestore)
- **Tipo:** trigger Firestore onCreate sobre `email-sent/{id}`.
- **Dónde:** `SAAS/firebase-firestore-trigger/mailer/onCreate-sentEmail.ts:5`, `SAAS/core/mailer/interfaces/triggers/sendEmail.controller.ts:3-6` y `SAAS/core/shared/mailer/email.service.ts:96-103`. Desplegado.
- **Qué lo dispara:** que alguien escriba en `email-sent`. En el contenedor no se ha encontrado nadie que lo haga; el grep de `email-sent` en `API/` sale vacío.
- **Qué hace:** manda el correo con la plantilla de `emails_template`.
- **Qué deja escrito:** un correo real; nada en Firestore.
- **Cómo se comprueba:** no se puede observar desde fuera.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** escribir el documento.
- **Criticidad:** baja.
- **Sospechas:** no tiene emisor conocido en el flujo de CheckBiz.

## LIS-19 · onDeleteEntity (limpieza del buscador)
- **Tipo:** trigger Firestore onDelete sobre `/entities/{eid}`.
- **Dónde:** `SAAS/firebase-firestore-trigger/entities/onDelete.ts:5-14`, `SAAS/core/searchIndex/infrastructure/FirestoreSearchIndexRepository.ts:26`. Desplegado.
- **Qué lo dispara:** borrar el documento de la entidad.
- **Qué hace:** borra la entrada de `searchIndex` de esa entidad.
- **Qué deja escrito:** `searchIndex/{docId}` borrado. No borra subcolecciones.
- **Cómo se comprueba:** leer `searchIndex/<id de la ruta>` y comprobar que ya no existe.
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** borrar la entidad.
- **Criticidad:** baja. Útil para la limpieza de las pruebas.
- **Sospechas:** los índices de empleados y sucursales de esa entidad no se tocan.

## LIS-20 · onDeleteEvent
- **Tipo:** trigger Firestore onDelete sobre `/entities/{eid}/events/{eid}`.
- **Dónde:** `SAAS/firebase-firestore-trigger/events/onDelete.ts:5-14`. Desplegado.
- **Qué lo dispara:** borrar un evento de passinbiz.
- **Qué hace y qué deja escrito:** borra su `searchIndex`.
- **Cómo se comprueba:** leer `searchIndex`.
- **Latencia esperable:** segundos.
- **Criticidad:** baja. Fuera del flujo de CheckBiz.
- **Sospechas:** ninguna.

### Passinbiz (fuera del flujo de CheckBiz; activos en dev)

## LIS-21 · onCreateHolders (pase bajo demanda)
- **Tipo:** trigger Firestore onWrite sobre `/entities/{e_id}/holders/{h_id}`, con 2 GiB, concurrencia 5 y 300 s.
- **Dónde:** `SAAS/services-saas/passinbiz/firebase-passinbiz-trigger/holders/onCreate-holders.ts:6-21`. Controlador: `SAAS/services-saas/passinbiz/interfaces/triggers/createPassOnDemand.controller.ts`. Desplegado.
- **Qué lo dispara:** que el titular pase a `status=="pending"`.
- **Qué hace:** genera el pase y encola el correo.
- **Qué deja escrito:** `pendingEmails` (`:175`), el titular con `passStatus:"active"` y `status:"made"` (`:179-185`) o `failed` (`:196`), y emite eventos de pase por la vía de Firebase hacia `webhook_outbox` (`:187` y `:197`).
- **Cómo se comprueba:** leer el titular.
- **Latencia esperable:** de segundos a minutos.
- **Criticidad:** baja para CheckBiz.
- **Sospechas:** ninguna revisada.

## LIS-22 · onCreateTrace
- **Tipo:** trigger Firestore onWrite sobre `/entities/{e_id}/holders/{h_id}/traces/{tid}`.
- **Dónde:** `.../holders/onCreateTrace.ts:5-18`. Desplegado.
- **Qué deja escrito:** el titular con `isValidated`, `lastValidatedAt` y `validatedResult`.
- **Latencia esperable:** segundos.
- **Criticidad:** baja.

## LIS-23 · onDeleteHolder
- **Tipo:** trigger Firestore onDelete sobre `/entities/{eid}/holders/{eid}`.
- **Dónde:** `.../holders/onDelete.ts:5-14`. Desplegado.
- **Qué deja escrito:** borra su `searchIndex`.
- **Criticidad:** baja.

## LIS-24 · onCreateStaff
- **Tipo:** trigger Firestore onCreate sobre `/entities/{e_id}/staff/{h_id}`.
- **Dónde:** `.../staff/onCreate-staff.ts:7-13`. Controlador: `SAAS/services-saas/passinbiz/interfaces/triggers/onCreateStaff.controller.ts:30`. Desplegado.
- **Qué deja escrito:** un correo real. El resto del controlador no se ha revisado en detalle.
- **Criticidad:** baja.

## LIS-25 · onDeleteStaff
- **Tipo:** trigger Firestore onDelete sobre `/entities/{eid}/staff/{eid}`.
- **Dónde:** `.../staff/onDelete.ts:5-13`. Desplegado.
- **Qué deja escrito:** borra su `searchIndex`.
- **Criticidad:** baja.

---

## 2. Receptores y consumidores en contenedores

Todos cuentan como **activos**: su servicio está en `docker-compose.staging.yml` y la ruta se monta al arrancar la app. En los contenedores **no** hay listeners de Firestore (`onSnapshot`) ni de Postgres (`LISTEN`); el grep sobre `API/services` y `API/packages` sale vacío.

## LIS-26 · sync — ingesta de fichajes
- **Tipo:** receptor S2S en contenedor, `POST /api/sync/checklogs` con `X-Encodebiz-Key`.
- **Dónde:** `API/services/sync/src/app.ts:10` y `API/services/sync/src/interfaces/sync.router.ts:65-137`. Servicio `sync` en `docker-compose.staging.yml:166-181`. Ruta de nginx: `nginx/nginx.staging.conf:103-105`.
- **Qué lo dispara:** LIS-02.
- **Qué hace:** hace upsert por `id` en `checklogs_raw`, actualizando `status`, `closed`, `is_suspect`, `metadata_raw` y el resto (`:71-120`). Escribe `sync_log` con `success` o `failed` (`:123-132`).
- **Qué deja escrito:** `checklogs_raw` y `sync_log` en Postgres.
- **Cómo se comprueba:** solo dentro de la red de contenedores. El endpoint escribe y no hay GET.
- **Latencia esperable:** menos de un segundo desde que llega.
- **Cómo forzarlo en desarrollo:** llamando al endpoint con la clave S2S. No es recomendable, porque inventa un fichaje en Postgres.
- **Criticidad:** alta.
- **Sospechas:** `sync_log` solo guarda el `id` del primer elemento del lote (`:124-126`).

## LIS-27 · sync — ingesta de valoraciones
- **Tipo:** receptor S2S, `POST /api/sync/task-ratings`.
- **Dónde:** `API/services/sync/src/interfaces/sync.router.ts:139-159`.
- **Qué lo dispara:** LIS-13.
- **Qué deja escrito:** upsert en `task_ratings_raw`.
- **Cómo se comprueba:** dentro del servidor, o por el panel de analytics.
- **Latencia esperable:** menos de un segundo.
- **Criticidad:** baja.
- **Sospechas:** no escribe `sync_log`.

## LIS-28 · analytics — foto del patrón
- **Tipo:** receptor S2S, `POST /api/analytics/build/pattern-snapshot`.
- **Dónde:** `API/services/analytics/src/app.ts:26`, `API/services/analytics/src/interfaces/analytics.router.ts:134-150` y `API/services/analytics/src/application/BuildPatternSnapshot.ts:117-135`. Servicio `analytics` en `docker-compose.staging.yml:184-200`.
- **Qué lo dispara:** LIS-09 y LIS-10.
- **Qué hace:** guarda el patrón que calculó Firebase, más las valoraciones de Postgres, sin recalcular nada.
- **Qué deja escrito:** `pattern_snapshots`, en upsert por `(entity, branch, employee, snapshot_date)`. Es SNP-04.
- **Cómo se comprueba:** `GET /api/analytics/patterns/history`, con la clave S2S, desde fuera por nginx.
- **Latencia esperable:** menos de un segundo.
- **Cómo forzarlo en desarrollo:** reescribir el patrón en Firestore.
- **Criticidad:** media.
- **Sospechas:** ninguna.

## LIS-29 · Eventos de la plataforma — encolado y entrega inmediata
- **Tipo:** consumidor de outbox dentro del proceso de cada servicio emisor.
- **Dónde:**
  - Encolado y entrega: `API/packages/shared/src/events/publish.ts:37-83` (`publish`) y `:102-111` (`emit`).
  - Cola: `API/packages/shared/src/events/infrastructure/PgDeliveryRepository.ts:34-47`.
  - Intento de entrega: `API/packages/shared/src/events/deliver.ts:53-89`.
  - Emisores:
    - `checkinbiz`: `API/services/checkinbiz/src/events/attendance.ts:73-166` y `API/services/checkinbiz/src/events/calendar.ts:27,52`.
    - `tasks`: `API/services/tasks/src/events/task.ts:48-151`.
    - `branches`: `API/services/branches/src/events/branch.ts:8-53`.
    - `billing`: `API/services/billing/src/events/invoice.ts:32-36`.
    - `documents`: `API/services/documents/src/events/document.ts:47-92`.
    - `rentman`: `API/services/rentman/src/events/addon.ts:13-21`.
    - `reports`: `API/services/reports/src/events/report.ts:16`.
- **Qué lo dispara:** el caso de uso de cada servicio. En la cadena del fichaje, `createChecklog.controller.ts:531-534` emite `attendance.clock_in`, `attendance.clock_out`, `attendance.break_start`, `attendance.break_end`, `attendance.clock_flagged` y `workday.closed`. El rechazo por geocerca emite `clock_rejected` (`:498-502`).
- **Qué hace:**
  - Lee los endpoints suscritos en Firestore `entities/{e}/webhook_endpoints`, admitiendo comodines.
  - Encola una fila por endpoint, sin duplicar por `(endpoint, event_id)`.
  - Intenta la entrega en el acto sin bloquear la respuesta.
- **Qué deja escrito:** `webhook_delivery` en Postgres, con estado `pending`, `delivered` o `dead`. Hace un POST firmado a la URL del cliente y actualiza `consecutiveFailures` en el endpoint de Firestore.
- **Cómo se comprueba:** desde fuera, con token de Firebase: `GET /api/v1/events/deliveries?entityId=X` (`API/services/events/src/interfaces/http/events.router.ts:196-208`).
- **Latencia esperable:** segundos.
- **Cómo forzarlo en desarrollo:** ejecutar la acción. Para probar un endpoint concreto: `POST /api/v1/events/endpoints/:id/test` (`:161-191`).
- **Criticidad:** media. Tiene efecto hacia terceros.
- **Sospechas:**
  - Duplica LIS-03 en `attendance.clock_in` y `attendance.clock_out`.
  - Si `emit` falla, solo lo escribe en el log.

## LIS-30 · events — emisión S2S
- **Tipo:** receptor S2S, `POST /api/v1/events/s2s/publish`.
- **Dónde:** `API/services/events/src/app.ts:18` y `API/services/events/src/interfaces/http/events.router.ts:227-249`. Servicio `events` en `docker-compose.staging.yml:340-356`.
- **Qué lo dispara:** estaba pensado para los triggers de `firebase_sdk`, pero hoy no hay ninguno que emita (`API/services/firebase_sdk/src/index.ts:43-62`). **Sin llamante conocido.**
- **Qué hace:** llama a `publish()`, que es LIS-29.
- **Qué deja escrito:** `webhook_delivery`.
- **Cómo se comprueba:** `GET /api/v1/events/deliveries`.
- **Latencia esperable:** segundos.
- **Criticidad:** baja. Hoy no tiene uso.

## LIS-31 · backoffice — constancia del mantenimiento
- **Tipo:** receptor S2S, `POST /api/v1/backoffice/s2s/maintenance/runs` y `/runs/:id/ghosts`.
- **Dónde:** `API/services/backoffice/src/app.ts:48`, `API/services/backoffice/src/interfaces/http/s2s/maintenance.s2s.router.ts:72,142` y `API/services/backoffice/src/infrastructure/repository/PostgresMaintenanceRepository.ts:82,96,139,168`.
- **Qué lo dispara:** PRG-09.
- **Qué deja escrito:** `maintenance_runs` y `maintenance_ghost_users` en Postgres. Es SNP-11.
- **Cómo se comprueba:** con usuario del backoffice y permiso `maintenance:read`: `GET /api/v1/backoffice/maintenance/runs` y `/ghosts` (`API/services/backoffice/src/interfaces/http/modules/maintenance.router.ts:35-105`).
- **Latencia esperable:** en la misma pasada.
- **Criticidad:** media.

## LIS-32 · billing — webhook de Stripe
- **Tipo:** receptor externo, `POST /api/v1/billing/webhook` con el cuerpo en bruto y firma de Stripe.
- **Dónde:** `API/services/billing/src/app.ts:20`, `API/services/billing/src/interfaces/http/webhook.router.ts:15` y `API/services/billing/src/application/StripeWebhookHandler.ts:33-77`. Servicio `billing` en `docker-compose.staging.yml:320-333`, que no tiene tareas programadas (`:318-319`).
- **Qué lo dispara:** Stripe (la cuenta de dev):
  - `invoice.finalized`
  - `invoice.paid`
  - `invoice.payment_failed`
  - `invoice.upcoming`
  - `customer.subscription.trial_will_end`
  - `customer.subscription.deleted`
  - `payment_method.attached` y `payment_method.detached`
- **Qué hace:**
  - Con `finalized`, envía la factura por correo y emite `invoice.issued` (`:35-41`).
  - Con `paid` y `payment_failed`, anota el ciclo (`:123-148`) y emite `invoice.payment_failed`.
  - Con `upcoming` y `trial_will_end`, ajusta las unidades.
- **Qué deja escrito:** `entities/{e}/invoices/{id}.status`, `invoice_emails/{stripeInvoiceId}`, el correo de la factura y `webhook_delivery`.
- **Cómo se comprueba:** leer los documentos de Firestore. Reenviar una factura: `POST /api/v1/billing/internal/invoices/:invoiceId/send`, con la clave S2S (`internal.router.ts:7`).
- **Latencia esperable:** segundos tras el evento de Stripe.
- **Criticidad:** alta en producción; en dev, media.
- **Sospechas:** la función HTTP antigua `apiV100-firebaseEntryHttp-stripeWebhook` sigue desplegada en dev (línea 70 del CSV). No se sabe si la cuenta Stripe de dev la tiene también dada de alta.

## LIS-33 · rentman — webhook de Rentman
- **Tipo:** receptor externo, `POST /api/v1/rentmanbiz/webhook/:entityId`, validado con `X-Rentman-Token`.
- **Dónde:** `API/services/rentman/src/app.ts:19` y `API/services/rentman/src/interfaces/http/rentman.router.ts:532-560`.
- **Qué lo dispara:** Rentman, en la cuenta sandbox en dev.
- **Qué hace:** `handleRentmanWebhook`, no detallado.
- **Qué deja escrito:** sin confirmar.
- **Criticidad:** baja para CheckBiz.
- **Sospechas:** el propio código dice que la verificación de firma es provisional (`:543-548`).

## LIS-34 · tasks — alta de tareas de sistema
- **Tipo:** receptor S2S, `POST /api/v1/tasks/system`.
- **Dónde:** `API/services/tasks/src/app.ts:22` y `API/services/tasks/src/interfaces/http/task/systemTaskRouter.ts:7`. El llamante es `API/services/rentman/src/infrastructure/HttpTasksClient.ts:58`, por la red interna.
- **Qué lo dispara:** rentman, al empujar tareas (`POST /api/v1/rentmanbiz/tasks/push`, `rentman.router.ts:444`).
- **Qué deja escrito:** `entities/{e}/tasks/{id}`. Detrás van los efectos de una tarea: LIS-11 y PRG-08.
- **Criticidad:** baja.

## LIS-35 · merlin — análisis en segundo plano
- **Tipo:** otro. Es un trabajo asíncrono dentro del proceso, lanzado por petición HTTP.
- **Dónde:** `API/services/merlin/src/modules/application/getOrCreateBranchAnalysis.ts:41-79` y `API/services/merlin/src/modules/infrastructure/FirestoreAnalysisRepository.ts:6-45`.
- **Qué lo dispara:** `POST /api/v1/gpt/interpret` o `/api/interpret`, con token de Firebase.
- **Qué hace:**
  - Si hay un análisis fresco completado, lo devuelve (`:41-42`).
  - Si no, marca `analysing` y lanza el cálculo contra OpenAI; la petición responde con `202` y `path`.
- **Qué deja escrito:** `ai-analizer/{md5(filtros)}`, con `status` en `analysing` y luego `completed` o `failed` (`:32` y `:45`). Es SNP-08.
- **Cómo se comprueba:** leer ese documento hasta que tenga `status:"completed"`.
- **Latencia esperable:** de segundos a decenas de segundos, porque llama a OpenAI.
- **Criticidad:** baja para la cadena del fichaje.
- **Sospechas:** hace una llamada real a OpenAI y cuesta dinero.

---

## 3. Programadas de Cloud Functions (9, todas ENABLED en dev)

Cómo forzar cualquiera en desarrollo:

```
gcloud scheduler jobs run <job> --project dev-encodebiz --location us-central1
```

Los nombres de job están copiados de `dev-programadas.csv`.

## PRG-01 · processPendingEmails
- **Tipo:** cron en Cloud Functions, `* * * * *` en UTC.
- **Dónde:** `SAAS/core/firebase-entry-schedule/mailer/email-worker.ts:8-73`. Exportado en `SAAS/core/firebase-entry-schedule/index.ts:10`. Desplegado.
- **Qué lo dispara:** el reloj. Consume `pendingEmails` con `status=="pending"` y `nextAttempt<now`, de 100 en 100 (`:11-16`). Los encola LIS-21, el pase de passinbiz.
- **Qué hace:**
  - Envía cada correo y lo marca `sent`.
  - Publica `credential.sent` o `pass.sent` por la vía de Firebase (`:38-44`).
  - Si falla, reintenta a la hora; a partir del sexto intento lo da por `error` y marca el titular `passStatus:"failed"` (`:47-66`).
- **Qué deja escrito:** `pendingEmails/{id}.status`, los correos reales y `webhook_outbox`.
- **Cómo se comprueba:** leer `pendingEmails/{id}.status`.
- **Latencia esperable:** 1 minuto o menos.
- **Cómo forzarlo:** `firebase-schedule-apiV100-firebaseEntrySchedule-processPendingEmails-us-central1`.
- **Efectos externos al forzarlo:** **manda correos reales** a todo lo pendiente de dev y encola webhooks hacia terceros.
- **Criticidad:** baja para CheckBiz. Solo passinbiz usa esta cola.
- **Sospechas:** ninguna para CheckBiz.

## PRG-02 · webhookWorker (entregas de la vía Firebase)
- **Tipo:** cron en Cloud Functions, `* * * * *` en UTC.
- **Dónde:** `SAAS/core/firebase-entry-schedule/webhook/index.ts:5-7`, `SAAS/core/webhook/worker.ts:9-127` y `SAAS/core/webhook/backoff.ts:1-5`. Desplegado.
- **Qué lo dispara:** el reloj. Consume la colección `webhook_outbox` de todas las entidades, con `status=="pending"` y `nextAttemptAt<=now`, 100 cada vez (`:11-16`). La alimentan LIS-03, LIS-21 y PRG-01.
- **Qué hace:**
  - Hace un POST firmado con un timeout de 4 s.
  - Si sale bien, marca `delivered`.
  - Si falla, reintenta a los 30 s, 2 min, 10 min y 1 h.
  - Al agotar los intentos, marca `dead` y **deshabilita el endpoint** (`:110-123`).
- **Qué deja escrito:** el estado de `entities/{e}/webhook_outbox/{id}` y, en `webhook_endpoints/{id}`, los campos `consecutiveFailures` y `enabled`. Además, el POST a la URL del cliente.
- **Cómo se comprueba:** leer el documento de la cola y comprobar `status=="delivered"`, o mirar el receptor de pruebas.
- **Latencia esperable:** 1 minuto o menos.
- **Cómo forzarlo:** `firebase-schedule-apiV100-firebaseEntrySchedule-webhookWorker-us-central1`.
- **Efectos externos al forzarlo:** **llama a URLs de terceros** registradas en cualquier entidad de dev y puede deshabilitar sus endpoints.
- **Criticidad:** media.
- **Sospechas:**
  - Es la mitad duplicada de LIS-03 frente a LIS-29.
  - Al fallar, deshabilita el endpoint en el **mismo** documento que usa el contenedor, así que un fallo por esta vía también apaga las entregas del contenedor.

## PRG-03 · triggerInvoiceWorker (ciclo del día 5)
- **Tipo:** cron en Cloud Functions, `0 3 5 * *` en UTC.
- **Dónde:** `SAAS/core/firebase-entry-schedule/subscritions/create-worker-invoice.ts:5-32`. Desplegado.
- **Qué lo dispara:** el reloj. La próxima ejecución es el 2026-10-05 a las 03:00 UTC.
- **Qué hace:** por cada `entities` con `active==true`, crea `invoices/{id}` con `status:"PENDING_PROCESSING"`. Eso dispara LIS-17.
- **Qué deja escrito:** facturas en Firestore y, a través de LIS-17, facturas en Stripe de dev y correos (LIS-32).
- **Cómo se comprueba:** leer `entities/{e}/invoices`.
- **Latencia esperable:** según el cron: una vez al mes.
- **Cómo forzarlo:** `firebase-schedule-apiV100-firebaseEntrySchedule-triggerInvoiceWorker-us-central1`.
- **Efectos externos al forzarlo:** **toca Stripe y manda facturas por correo** de **todas** las entidades activas de dev, no solo la de la prueba. **No forzar en una prueba.**
- **Criticidad:** alta.
- **Sospechas:** `docker-compose.staging.yml:316-319` dice que el cobro lo decide Stripe y que billing no programa nada; este job sigue activo en dev y puede facturar en paralelo.

## PRG-04 · dailyCollectorData (agregado diario por sucursal)
- **Tipo:** cron en Cloud Functions, `0 * * * *` en UTC.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-entry-schedule/dailyCollectorData.ts:4-7`, `SAAS/services-saas/checkinbiz/interfaces/triggers/dailyCollectorData.controller.ts:14-80` y `SAAS/services-saas/checkinbiz/infrastructure/repository/FirestoreReportRepository.ts:45-53`. Desplegado.
- **Qué lo dispara:** el reloj. Recorre las sucursales `active` (`:20-22`) y **solo procesa las que tienen las 02:xx en su `address.timeZone`** (`:30-32`).
- **Qué hace:** toma los fichajes de ayer, en hora local, y construye un `DailyReport` con horas, puntualidad, sospechosos y coste (`:47-66`).
- **Qué deja escrito:** `checkbiz_daily_report/{entityId}_{branchId}_{yyyyMMdd}`, en upsert. Es SNP-05.
- **Cómo se comprueba:** leer ese documento.
- **Latencia esperable:** según el cron: la noche siguiente, a las 02:xx locales.
- **Cómo forzarlo:**
  - Job: `firebase-schedule-apiV100-scheduleCheckbiz-dailyCollectorData-us-central1`. Al forzarlo solo actúa sobre las sucursales que tienen las 02:xx **en ese momento**. Truco: crear la sucursal de prueba en una zona horaria donde lo sean.
  - Alternativa dirigida, desplegada: HTTP `apiV100-firebaseEntryHttp-checkinbiz-recalcDailyReport` con `{entityId, branchId, date}` (`SAAS/services-saas/checkinbiz/interfaces/http/report/recalculateDailyReport.controller.ts:27-79`). Pide token de Firebase; no se han revisado los permisos que exige.
- **Efectos externos al forzarlo:** ninguno; solo escribe en Firestore.
- **Criticidad:** media. Lo lee el panel de estadísticas (`API/services/analytics/src/infrastructure/StatsFirestoreRepository.ts:12`).
- **Sospechas:** `FirestoreReportRepository.findRangeReport` lee `daily_report` (`:74`), pero se escribe en `checkbiz_daily_report`. No está confirmado quién usa esa lectura.

## PRG-05 · employeePlanifierWorker (recordatorios de fichar)
- **Tipo:** cron en Cloud Functions, `*/5 * * * *` en UTC, con 1 GiB.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-entry-schedule/employeePlanifierWorker.ts:23-38`, `SAAS/services-saas/checkinbiz/interfaces/triggers/executeEmployeePlanifier.controller.ts:18-175` y `SAAS/services-saas/checkinbiz/infrastructure/repository/FirestoreEmployeePlanifierRepository.ts:8,38-41`. Desplegado.
- **Qué lo dispara:** el reloj. Toma `checkbiz_employee_planifiers` con `status=="active"` y `nextRunAt<=now+5min`, de 100 en 100. Los crea PRG-06.
- **Qué hace:**
  - Resuelve el día efectivo.
  - Si ya ha fichado el tipo que toca, marca `processed` y `already_marked` (`:66-80`).
  - Si no, manda un push (`:105-127`) y un **WhatsApp** (`:130-148`).
  - Reprograma con los desfases -5, 0 y +5 min, o cierra (`:150-170`).
- **Qué deja escrito:**
  - `checkbiz_employee_planifiers/{id}`: `status` (`active`, `processed` o `failed`), `attempts` y `metadata.attemptIndex`.
  - Un push FCM y un WhatsApp por la API de Meta (`SAAS/core/shared/whatsapp/WhatsAppService.ts:15-26`).
  - **No** escribe `in_app_notifications`.
- **Cómo se comprueba:** leer el planificador y comprobar que `attempts` sube o que `status` cambia.
- **Latencia esperable:** 5 minutos o menos respecto a `nextRunAt`.
- **Cómo forzarlo:** `firebase-schedule-apiV100-scheduleCheckbiz-employeePlanifierWorker-us-central1`. Para que haga algo, antes hay que poner `nextRunAt` en el pasado.
- **Efectos externos al forzarlo:** **push y WhatsApp reales** a los empleados de dev con teléfono y token. No está confirmado que dev tenga credenciales de Meta.
- **Criticidad:** media.
- **Sospechas:** ninguna más.

## PRG-06 · planifierNotificationWorker (genera los recordatorios de mañana)
- **Tipo:** cron en Cloud Functions, `0 4 * * *` en UTC.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-entry-schedule/planifierNotificationWorker.ts:9-14` y `SAAS/services-saas/checkinbiz/interfaces/triggers/checkActiveEmployeeWorker.controller.ts:35-151`. Desplegado.
- **Qué lo dispara:** el reloj. Recorre todos los empleados activos en lotes.
- **Qué hace:** para el día siguiente, con turnos y sin festivo, crea planificadores de checkin y checkout 5 minutos antes de cada turno, deduplicados por id (`:97-125`). Marca `lastDayPlanned` (`:139-141`).
- **Qué deja escrito:** `checkbiz_employee_planifiers/{employeeId}_{tipo}_{fecha}_{idx}` y `entities/{e}/employees/{id}.metadata.lastDayPlanned`.
- **Cómo se comprueba:** leer los planificadores con el id del empleado.
- **Latencia esperable:** según el cron: diario.
- **Cómo forzarlo:**
  - Job: `firebase-schedule-apiV100-scheduleCheckbiz-planifierNotificationWorker-us-central1`.
  - Alternativa desplegada: HTTP `apiV100-firebaseEntryHttp-planifierHelper`, que lo ejecuta con `force=true` e ignora `lastDayPlanned` (`planifierNotificationWorker.ts:17-32`). Exige un token con el claim `admin`.
- **Efectos externos al forzarlo:** ninguno directo; solo escribe en Firestore. Pero deja preparado lo que PRG-05 enviará.
- **Criticidad:** media.
- **Sospechas:** un empleado con varias sucursales no tiene sucursal de planificación (`:50-58`); se planifica sin `branchId`.

## PRG-07 · sanitizerChecklog (jornadas incompletas)
- **Tipo:** cron en Cloud Functions, `0 * * * *` en Etc/UTC.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-entry-schedule/sanitizer-checklogs.ts:7-15`, `SAAS/services-saas/checkinbiz/interfaces/triggers/sanitizerChecklogs.controller.ts:15-157` y la consulta en `SAAS/services-saas/checkinbiz/infrastructure/repository/FirestoreChecklogRepository.ts:135-160`. Desplegado.
- **Qué lo dispara:** el reloj. Busca en todas las colecciones `checklogs` los checkins válidos con `deadline` dentro de **la última hora**, `[now-1h, now)` (`:22-23`). El `deadline` lo pone el contenedor en cada checkin: fin del turno más 6 h (`API/services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts:357,444`).
- **Qué hace:**
  - Marca el checkin y los fichajes ligados con `closed:true`, `status:"incomplete_workday"` y `metadata.incompleteWorkday` (`:50-80`).
  - Si no hay checkout, crea uno sintético (`:84-120`).
  - Crea una incidencia para el trabajador (`:123-141`).
- **Qué deja escrito:**
  - Fichajes con `status:"incomplete_workday"`.
  - `entities/{e}/checklogs/incomplete_workday_{checkinId}`.
  - `issues/incomplete_workday_{entityId}_{checkinId}`, que dispara LIS-14: push e `in_app_notifications`.
  - Cada escritura de fichaje dispara también LIS-02, que actualiza `checklogs_raw`.
- **Cómo se comprueba:** leer el checkin y comprobar su `status`, luego el documento sintético y la incidencia.
- **Latencia esperable:** según el cron: hasta 1 h después del `deadline`.
- **Cómo forzarlo:**
  - Job: `firebase-schedule-apiV100-scheduleCheckbiz-sanitizerChecklog-us-central1`. Solo procesa `deadline` de la última hora; en una prueba, poner el `deadline` del checkin con el SDK de administración a unos minutos atrás y lanzar el job.
  - Alternativa desplegada: HTTP `apiV100-scheduleCheckbiz-sanitizerChecklogHelper`, con token y claim `admin` (`:18-31`).
- **Efectos externos al forzarlo:** push reales a los trabajadores afectados. Modifica fichajes de **cualquier** entidad de dev cuyo `deadline` caiga en esa hora.
- **Criticidad:** alta. Cambia el registro legal.
- **Sospechas:** la ventana es fija, de una hora. Si un tick no se ejecuta, esos checkins **no se procesan nunca**.

## PRG-08 · taskStartNotificationWorker (aviso de tarea no iniciada)
- **Tipo:** cron en Cloud Functions, `*/5 * * * *` en UTC.
- **Dónde:** `SAAS/services-saas/checkinbiz/firebase-entry-schedule/taskStartNotificationWorker.ts:7-28`, `SAAS/services-saas/checkinbiz/infrastructure/repository/FirestoreTaskRepository.ts:200-210` y `SAAS/services-saas/checkinbiz/application/notifications/TaskNotificationService.ts:120-124`. Desplegado.
- **Qué lo dispara:** el reloj. Busca en todas las colecciones `tasks` las que tienen `scheduledStartNotificationAt<=now` y `status` en `draft` o `assigned`, con límite de 200, y luego filtra las ya avisadas. `scheduledStartNotificationAt` lo calcula el contenedor al crear la tarea (`API/services/tasks/src/interfaces/http/task/createTask.controller.ts:86`).
- **Qué hace:** manda al equipo de la tarea un push `task_start_delay` y escribe `scheduledStartNotifiedAt`.
- **Qué deja escrito:** `entities/{e}/tasks/{id}.scheduledStartNotifiedAt`, `in_app_notifications` y un push.
- **Cómo se comprueba:** leer `scheduledStartNotifiedAt` y consultar `in_app_notifications`.
- **Latencia esperable:** 5 minutos o menos.
- **Cómo forzarlo:** `firebase-schedule-apiV100-scheduleCheckbiz-taskStartNotificationWorker-us-central1`.
- **Efectos externos al forzarlo:** push reales a los equipos de las tareas vencidas de dev.
- **Criticidad:** media.
- **Sospechas:** las tareas ya avisadas siguen entrando en la consulta, porque el filtro va después del `limit(200)` y `scheduledStartNotificationAt` no se borra. Al acumularse, tapan a las nuevas. Necesita el índice `status` → `scheduledStartNotificationAt`.

## PRG-09 · ghostUsersMaintenance (cuentas fantasma)
- **Tipo:** cron en Cloud Functions, `15 4 * * *` en Europe/Madrid, con 540 s y sin reintentos. Va en el codebase `triggers` de `API/`.
- **Dónde:** `API/services/firebase_sdk/src/maintenance/ghostUsers.ts:38-97`, `API/services/firebase_sdk/src/maintenance/config.ts:67-83` y `API/services/firebase_sdk/src/environment.ts:90-102`. Desplegado (línea 57 del CSV).
- **Qué lo dispara:** el reloj.
- **Qué hace:**
  - Hace censo de roles y fichas, y recorre Auth.
  - Clasifica las cuentas sin rol ni ficha con 7 días o más.
  - Solo borra si `MAINTENANCE_GHOST_APPLY` está puesto, con topes de 25 por pasada y un 10 % de lo escaneado.
- **Qué deja escrito:** por S2S (LIS-31), `maintenance_runs` y `maintenance_ghost_users`. Si está armado, además borra usuarios de Auth.
- **Cómo se comprueba:** backoffice → `GET /api/v1/backoffice/maintenance/runs`.
- **Latencia esperable:** según el cron: diario.
- **Cómo forzarlo:** `firebase-schedule-ghostUsersMaintenance-us-central1`.
- **Efectos externos al forzarlo:** **puede borrar cuentas de Auth de dev** si está armado; no está confirmado que en dev esté apagado. Las cuentas recién creadas por una prueba quedan protegidas, porque tienen menos de 7 días.
- **Criticidad:** alta si está armado.
- **Sospechas:** el comentario de `ghostUsers.ts:37` dice que corre «después de la foto del backoffice, que es a las 3:20». Pero PRG-14 no fija zona horaria y ni los Dockerfile ni los `.env` de ejemplo fijan `TZ`, así que en el contenedor es probablemente UTC: las 04:15 de Madrid son las 02:15 UTC en verano y corre **antes**.

---

## 4. Programadas dentro de contenedores

Cuentan como activas porque su servicio está en `docker-compose.staging.yml` y el mecanismo arranca en `server.ts`.

Revisado y **sin** tareas programadas: `checkinbiz`, `tasks`, `billing` (`docker-compose.staging.yml:318-319`), `analytics`, `merlin`, `sync`, `sales`, `documents`, `employees`, `branches` y `entities`. Por eso:

- **Facturación:** solo PRG-03 en Functions, más el webhook LIS-32.
- **Avisos de tareas:** en Functions (PRG-08).
- **Mantenimiento de cuentas:** en Functions (PRG-09).
- **Agregados de analítica:** reactivos (LIS-28), sin cron.

## PRG-10 · reports — construcción diaria de informes
- **Tipo:** cron en contenedor, con node-cron `5 * * * *` y `timezone: "UTC"`.
- **Dónde:** `API/services/reports/src/application/DailyReportCron.ts:121-132`. Tick en `:81-119`, construcción en `:19-77` y en `API/services/reports/src/application/BuildEmployeeDailyReports.ts:175`. Arranca en `API/services/reports/src/server.ts:17`. Activo: servicio `reports` en `docker-compose.staging.yml:203-219`.
- **Qué lo dispara:** el reloj. Descubre los centros con fichajes sincronizados en los últimos 30 días y la zona de cada uno (`etz` → `metadata_raw.tz` → UTC). Construye **ayer** para los centros que tienen las 02:xx locales.
- **Qué hace:**
  - Lee `checklogs_raw` y resuelve la identidad en Firestore.
  - Solo cuentan los ciclos cerrados y válidos.
- **Qué deja escrito:** `employee_daily_reports` en Postgres. Es SNP-06.
- **Cómo se comprueba:** desde fuera, con la clave S2S: `GET /api/reports/status?entityId=X&start=YYYY-MM-DD&end=YYYY-MM-DD` (`API/services/reports/src/interfaces/report.router.ts:77-100`). Devuelve el recuento por sucursal y día.
- **Latencia esperable:** según el cron: la noche siguiente, a las 02:05 locales.
- **Cómo forzarlo:** `POST /api/reports/cron/trigger {"date":"YYYY-MM-DD"}` con la clave S2S (`report.router.ts:64-74`). Construye todos los centros de esa fecha.
- **Efectos externos al forzarlo:** ninguno; solo escribe en Postgres.
- **Criticidad:** alta. Es la base del registro legal.
- **Sospechas:** una jornada `incomplete_workday` no aparece en el informe. Es lo que se busca, pero hay que saberlo para las pruebas.

## PRG-11 · events — rescate de entregas
- **Tipo:** cron en contenedor, con node-cron `EVENTS_RESCUE_CRON` (por defecto `*/5 * * * *`) y la zona horaria del contenedor.
- **Dónde:** `API/services/events/src/application/RescueWorker.ts:14,25-59`. Arranca en `API/services/events/src/server.ts:19`. Activo salvo que `EVENTS_RESCUE_DISABLED=true`.
- **Qué lo dispara:** el reloj. Consume `webhook_delivery` con `status='pending'` y `next_attempt_at<=now()`, bloqueando filas con `FOR UPDATE SKIP LOCKED` y hasta 500 cada vez.
- **Qué hace:** reintenta la entrega (LIS-29).
- **Qué deja escrito:** el estado de `webhook_delivery` y POSTs a terceros.
- **Cómo se comprueba:** `GET /api/v1/events/deliveries?entityId=X`.
- **Latencia esperable:** 5 minutos o menos.
- **Cómo forzarlo:** no hay forma de lanzar la pasada. Para una entrega concreta: `POST /api/v1/events/deliveries/:id/replay`, con token de Firebase.
- **Efectos externos al forzarlo:** llamadas a URLs de terceros.
- **Criticidad:** media.
- **Sospechas:** el rescate se salta los endpoints apagados sin marcar la entrega (`:31-34`).

## PRG-12 · events — purga de entregas
- **Tipo:** cron en contenedor, `EVENTS_PURGE_CRON` (por defecto `30 4 * * *`).
- **Dónde:** `API/services/events/src/application/RescueWorker.ts:15-18,61-68` y `API/packages/shared/src/events/infrastructure/PgDeliveryRepository.ts:135-143`.
- **Qué hace:** borra las entregas `delivered` de más de 30 días y las `dead` o `failed` de más de 90.
- **Qué deja escrito:** `DELETE` en `webhook_delivery`.
- **Cómo se comprueba:** no se puede de forma práctica.
- **Latencia esperable:** diaria.
- **Cómo forzarlo:** no hay forma, salvo cambiar la variable.
- **Efectos externos al forzarlo:** ninguno.
- **Criticidad:** baja.

## PRG-13 · rentman — sincronización de horas
- **Tipo:** cron en contenedor, `RENTMAN_HOURS_CRON` (por defecto `*/15 * * * *`).
- **Dónde:** `API/services/rentman/src/application/RentmanHoursCron.ts:13-50` y `API/services/rentman/src/application/syncHoursToRentman.ts:259,330`. Arranca en `API/services/rentman/src/server.ts:20`. Activo salvo que `RENTMAN_HOURS_CRON_DISABLED=true`.
- **Qué lo dispara:** el reloj, solo para las entidades con Rentman conectado y empleados mapeados.
- **Qué hace:** lee las jornadas de Postgres y las imputa en Rentman.
- **Qué deja escrito:** `rentman_sync_log` y las horas en Rentman, que en dev es la cuenta sandbox.
- **Cómo se comprueba:** con token de Firebase: `GET /api/v1/rentmanbiz/activity/:entityId`, que lee `rentman_sync_log` (`rentman.router.ts:294-320`), y `/hours/entries/:entityId`.
- **Latencia esperable:** 15 minutos o menos.
- **Cómo forzarlo:** `POST /api/v1/rentmanbiz/sync/hours {"entityId":…}` con la clave S2S (`rentman.router.ts:516-521`), o `/hours/sync-now` con token (`:420`).
- **Efectos externos al forzarlo:** escribe en Rentman sandbox, que es un tercero.
- **Criticidad:** baja para CheckBiz sin Rentman.

## PRG-14 · backoffice — foto diaria de la plataforma
- **Tipo:** cron en contenedor, `BACKOFFICE_SNAPSHOT_CRON` (por defecto `20 3 * * *`) sin zona explícita.
- **Dónde:** `API/services/backoffice/src/application/stats/StatsCron.ts:12-41`, `API/services/backoffice/src/application/stats/harvestSnapshot.ts` y `API/services/backoffice/src/infrastructure/repository/PostgresSnapshotRepository.ts:52`. Arranca en `API/services/backoffice/src/server.ts:10`. Activo salvo que `BACKOFFICE_SNAPSHOT_CRON_DISABLED=true`.
- **Qué lo dispara:** el reloj. Hace la foto de ayer en la zona `BACKOFFICE_SNAPSHOT_TZ`, por defecto Europe/Madrid.
- **Qué hace:** cuenta entidades, empleados, sucursales, cuentas de Auth, fichajes, sospechosos, leads, webhooks y valoraciones. Los fichajes salen de Postgres. Si falla una fuente, marca la foto como parcial.
- **Qué deja escrito:** `backoffice_snapshot_daily` en Postgres. Es SNP-10.
- **Cómo se comprueba:** `GET /api/v1/backoffice/stats`, con usuario del backoffice y permiso `stats:read` (`API/services/backoffice/src/interfaces/http/modules/stats.router.ts:43`).
- **Latencia esperable:** diaria.
- **Cómo forzarlo:** `POST /api/v1/backoffice/stats/harvest`, con usuario del backoffice (`stats.router.ts:93`). No se ha revisado el cuerpo que espera.
- **Efectos externos al forzarlo:** ninguno.
- **Criticidad:** baja.
- **Sospechas:** su hora y la de PRG-09 dependen de la zona horaria del contenedor.

## PRG-15 · backoffice — relleno de la foto al arrancar
- **Tipo:** otro. Se ejecuta una vez al arrancar el servicio, salvo que `BACKOFFICE_SNAPSHOT_BACKFILL=false`.
- **Dónde:** `API/services/backoffice/src/application/stats/StatsCron.ts:43-57`.
- **Qué hace:** si falta la foto de ayer, la hace.
- **Qué deja escrito:** `backoffice_snapshot_daily`.
- **Cómo forzarlo:** solo reiniciando el contenedor, que queda fuera del protocolo. Se puede usar PRG-14.
- **Criticidad:** baja.

---

## 5. Snapshots

Nota: `checklogs_raw` y `task_ratings_raw` son réplicas continuas y no fotos; vienen de LIS-26 y LIS-27. `checkbiz_employee_planifiers` es una cola (PRG-05 y PRG-06).

| ID | Qué es | Lo crea | Dónde se guarda | Cómo se lee |
|---|---|---|---|---|
| SNP-01 | Patrón de sucursal, con `taskSignals` y `profileType` | LIS-05 (inicial), LIS-01 (cada checkout válido), LIS-11 (tareas) | Firestore `checkbiz_branch_patterns/{branchId}` | SDK de administración |
| SNP-02 | Patrón de empleado, uno por sucursal y otro global | LIS-01 (lo crea en el primer checkout válido), LIS-11, LIS-12 | Firestore `checkbiz_employee_patterns/{employeeId}_{branchId}_{entityId}` y `…/{employeeId}_{entityId}` | SDK de administración |
| SNP-03 | Histórico diario de patrones, hasta 5 versiones al día | LIS-07 y LIS-08 | Firestore `pattern_history/{docIdOrigen}_{YYYY-MM-DD}.versions` | SDK de administración |
| SNP-04 | Serie diaria de patrones | LIS-09 y LIS-10, que pasan por LIS-28 | Postgres `pattern_snapshots`, una fila por día y ámbito | `GET /api/analytics/patterns/history` con la clave S2S; también el panel y Merlin |
| SNP-05 | Agregado diario por sucursal | PRG-04, o el HTTP `recalcDailyReport` | Firestore `checkbiz_daily_report/{entityId}_{branchId}_{yyyyMMdd}` | SDK de administración; el panel de estadísticas |
| SNP-06 | Informe diario por empleado, base del registro legal | PRG-10, o `POST /api/reports/cron/trigger` | Postgres `employee_daily_reports` | `GET /api/reports/status` con la clave S2S (recuentos); el panel de analytics |
| SNP-07 | Informe legal generado, en PDF o XLSX | Acción `POST /api/reports/generate` con token, que emite `report.generated` (LIS-29) | Storage `checkbiz/reports/entities/{e}/…` e historial en Firestore `entities/{e}/reports/{id}` | SDK de administración; `GET /api/reports/:reportId/download?entityId=` |
| SNP-08 | Análisis de Merlin, en caché 7 días | LIS-35, lanzado por `POST /api/v1/gpt/interpret` | Firestore `ai-analizer/{md5(filtros)}` | SDK de administración, esperando a `status=="completed"` |
| SNP-09 | Agregado de valoraciones del empleado | LIS-12 | Firestore `entities/{e}/employees/{id}.ratingTask` | SDK de administración |
| SNP-10 | Foto diaria de la plataforma | PRG-14 y PRG-15 | Postgres `backoffice_snapshot_daily` | `GET /api/v1/backoffice/stats`, con usuario del backoffice |
| SNP-11 | Pasadas y candidatas del barrido de cuentas, con copia de la ficha | PRG-09, que pasa por LIS-31 | Postgres `maintenance_runs` y `maintenance_ghost_users` | `GET /api/v1/backoffice/maintenance/runs` y `/ghosts` |
| SNP-12 | Dimensiones: sucursales, empleados y calendarios | **Solo a demanda**: `POST /api/analytics/dimensions/sync[?entityId=]` con la clave S2S (`API/services/analytics/src/interfaces/analytics.router.ts:42-50`) | Postgres `dim_branches`, `dim_employees`, `dim_calendars` y `dim_sync_log` | Indirecto, por el panel de analytics (lee `dim_*`) |

Sospechas de esta sección:

- **SNP-12:** el código dice que está «pensado para cron diario» (`analytics.router.ts:40-41`), pero no hay ningún cron que lo lance. Una sucursal o un empleado nuevos no llegan a `dim_*` hasta que alguien lo pide, y el panel lee de ahí.
- **SNP-03:** a partir de la sexta escritura del día no guarda nada.
- **SNP-04:** solo guarda el último estado de cada día.

---

## 6. Cadenas

### 6.1 Fichaje válido (entrada o descanso) — `POST /api/v1/checkinbiz/checklogs`
En dev, el fichaje entra **solo por el contenedor**: la HTTP antigua `checkinbiz-createChecklog` no está en el CSV de desplegadas.

1. **En la misma petición**, antes del 201:
   - Se escribe `entities/{e}/checklogs/{id}` con `status:"valid"`. Si es un checkin, lleva `deadline` igual al fin del turno más 6 h (`createChecklog.controller.ts:357,444,516`).
   - Se lanza `emitChecklogCreated`: `attendance.clock_in` o `break_*`, y `clock_flagged` si es sospechoso. Eso es **LIS-29**, con una fila en `webhook_delivery` y el intento inmediato.
2. **Segundos después**, triggers en paralelo sobre el documento del fichaje:
   - **LIS-02**, que pasa por **LIS-26**: una fila en `checklogs_raw` y otra en `sync_log`.
   - **LIS-03**: si hay un endpoint suscrito, una entrega en `entities/{e}/webhook_outbox`.
   - **LIS-01**: lo descarta, porque no es un checkout.
3. **En 1 minuto o menos:** **PRG-02** entrega lo de LIS-03 y el cliente recibe el segundo webhook (el duplicado).
4. **En 5 minutos o menos:** **PRG-11** reintenta lo que falló de LIS-29.
5. **Si nadie cierra antes del `deadline`:** **PRG-07**, dentro de la hora siguiente, marca `incomplete_workday`, crea el checkout sintético y la incidencia. La incidencia dispara **LIS-14**: push e `in_app_notifications`. Las escrituras disparan otra vez **LIS-02**.
6. **Recordatorios:** **PRG-05** comprueba que ya se ha fichado ese tipo y cierra el planificador (`already_marked`).
7. **La noche siguiente, a las 02:xx locales:**
   - **PRG-04**: `checkbiz_daily_report` (SNP-05).
   - **PRG-10**, a las 02:05: `employee_daily_reports` (SNP-06). Solo recoge la jornada si está cerrada y es válida.
8. **Periódico:**
   - **PRG-13**, cada 15 minutos, si la entidad tiene Rentman.
   - **PRG-14**, a las 03:20: cuenta el fichaje en `backoffice_snapshot_daily`.
9. **Un fichaje rechazado por la geocerca** también se escribe, con `status:"failed"` (`:498`). Emite `attendance.clock_rejected` (LIS-29) y dispara LIS-02, que lo sincroniza como `failed`. No dispara LIS-01 ni LIS-03.

### 6.2 Cierre de jornada (checkout)

1. **En la petición:**
   - Checkout `valid` con `checkin` referenciado y `isSuspect` si la jornada dura menos de 3 h o más de 10 h (`CreateChecklog.ts:68-77`).
   - Actualización del checkin con `closed:true` (`createChecklog.controller.ts:519-521`).
   - `attendance.clock_out`, más `clock_flagged` si procede.
   - `workday.closed`, que se compone asíncronamente leyendo el checkin (`attendance.ts:136-166`).
   - Todo eso sale por **LIS-29**.
2. **Segundos después:**
   - **LIS-02** dos veces, una por el checkout y otra por el checkin cerrado.
   - **LIS-03** con `clock_out`.
   - **LIS-01**, si el checkout es válido y no sospechoso: SNP-01 y SNP-02. Esas escrituras disparan en cascada **LIS-07** y **LIS-08** (SNP-03) y **LIS-09** y **LIS-10**, que pasan por **LIS-28** (SNP-04).
3. **En 1 minuto o menos:** **PRG-02**, con el webhook duplicado de `clock_out`.
4. **Esa noche o la siguiente:** **PRG-04**, **PRG-10**, **PRG-13** y **PRG-14**, como en 6.1.

### 6.3 Alta de empleado — `POST /api/v1/employees`

1. **En la petición:**
   - `createEmployee` de shared crea el usuario de Auth.
   - Escribe la ficha **con `uid`** e indexa en `searchIndex`.
   - Manda la bienvenida por SMTP.
   - Referencias: `API/packages/shared/src/checkbiz/employees/manageEmployee.ts:39-93` y `API/services/employees/src/interfaces/http/employee.router.ts:207,350`.
   - No emite eventos: `employee.*` está comentado en el catálogo, `API/packages/shared/src/events/catalogue.ts:155-160`.
2. **Segundos después:** **LIS-04** sale sin hacer nada, porque la ficha trae `uid`.
3. **A las 04:00 UTC:** **PRG-06** crea los planificadores de mañana si el empleado tiene una sola sucursal, turnos y el día no es festivo. Después, **PRG-05** manda los recordatorios en la hora del turno.
4. **En su primer checkout válido**, **LIS-01** crea sus patrones (SNP-02).
5. **PRG-12 no aplica.** **SNP-12** no se actualiza solo.

### 6.4 Alta de sucursal — `POST /api/v1/branches`

1. **En la petición:** se escribe la sucursal con `id` y se indexa en `searchIndex` (`API/packages/shared/src/checkbiz/repositories/FirestoreBranchRepository.ts:11-19`). Se emite `branch.created` por **LIS-29** (`API/services/branches/src/interfaces/http/branch.router.ts:93`).
2. **Segundos después:** **LIS-05** crea SNP-01 con `dataPoints:0`. Detrás van **LIS-07** (SNP-03) y **LIS-09**, que pasa por **LIS-28** (SNP-04).
3. **Cada noche a las 02:xx locales:** **PRG-04** la recorre, pero solo escribe si ha habido fichajes. Para **SNP-12** hay que llamar a `dimensions/sync`.

### 6.5 Alta de empresa — `POST /api/v1/entities` y después `POST /api/v1/billing/subscriptions`

1. **Crear la entidad:**
   - Se escribe la entidad y se indexa en `searchIndex`.
   - El asiento de propietario se da por la red interna, con `CHECKINBIZ_INTERNAL_URL`, y queda en `user_entity_roles` (`entity.router.ts:56-90`).
   - No hay trigger sobre la creación de la entidad.
2. **Suscribir:**
   - Se escribe `entities/{e}/subscriptions/{serviceId}` en `pending`.
   - Se crea la suscripción en Stripe de dev, con prueba gratuita.
   - Pasa a `active` si el plan es freemium o de pago por uso.
   - Se manda el correo «Servicio Activado» (`Subscribe.ts:38-69`).
3. **Segundos después:**
   - **LIS-06** crea la sucursal automática si hay datos legales completos. Detrás van **LIS-05** → SNP-01 → **LIS-07** y **LIS-09**.
   - **LIS-16**: al pasar de `pending` a `active`, manda **el segundo** correo «Servicio Activado».
4. **El día 5 a las 03:00 UTC:** **PRG-03** crea una factura, que dispara **LIS-17** → Stripe → **LIS-32**.

### 6.6 Creación de tarea — `POST /api/v1/tasks`

1. **En la petición:**
   - Se escribe `entities/{e}/tasks/{id}` con `scheduledStartNotificationAt` si `notifyIfNotStarted` está puesto (`createTask.controller.ts:86`).
   - Se manda el push de creación y de asignación, que deja `in_app_notifications` (`:135-137`).
   - Se emiten `task.created` y `task.assigned` por **LIS-29** (`:142-144`).
2. **Segundos después:** **LIS-11** se dispara pero no hace nada, porque la tarea no ha llegado a un estado final.
3. **Pasado `scheduledStartNotificationAt`,** si la tarea sigue en `draft` o `assigned`: **PRG-08**, en 5 minutos o menos, manda el push `task_start_delay`, escribe `in_app_notifications` y pone `scheduledStartNotifiedAt`.
4. **Al validarla o rechazarla:** **LIS-11** actualiza `taskSignals` en SNP-01 y SNP-02, lo que dispara **LIS-07** a **LIS-10**.
5. **Al valorarla:** **LIS-12** (SNP-09 y `taskSignals.avgRating`) y **LIS-13**, que pasa por **LIS-27** a `task_ratings_raw`.

---

## 7. Resumen

**Recuentos (solo lo activo en dev)**

| | Cloud Functions | Contenedores | Total |
|---|---|---|---|
| Listeners (LIS) | 25 triggers de Firestore (LIS-01 a LIS-25) | 10 receptores o consumidores (LIS-26 a LIS-35) | **35** |
| Programadas (PRG) | 9 jobs (PRG-01 a PRG-09) | 6 (PRG-10 a PRG-15) | **15** |
| Snapshots (SNP) | — | — | **12** |

**Se pueden forzar en desarrollo**

- **Las 9 programadas de Functions**, con `gcloud scheduler jobs run … --project dev-encodebiz --location us-central1`.
  - **Seguras para una prueba:**
    - PRG-06.
    - PRG-04: solo actúa sobre sucursales que tienen las 02:xx en ese momento; se puede usar `recalcDailyReport`.
    - PRG-07: preparando el `deadline`. Tiene efectos sobre otras entidades de dev.
    - PRG-08 y PRG-05: mandan push y PRG-05 posiblemente WhatsApp.
  - **No forzar:**
    - **PRG-03**: Stripe y facturas de todas las entidades.
    - **PRG-09**: puede borrar cuentas si está armado.
    - **PRG-01** y **PRG-02**: correos y webhooks reales de todo dev.
- **HTTP auxiliares desplegadas:**
  - `apiV100-scheduleCheckbiz-sanitizerChecklogHelper`, con el claim `admin`.
  - `apiV100-firebaseEntryHttp-planifierHelper`, con el claim `admin`.
  - `apiV100-firebaseEntryHttp-checkinbiz-recalcDailyReport`.
- **Contenedores:**
  - PRG-10: `POST /api/reports/cron/trigger`, con la clave S2S.
  - PRG-13: `POST /api/v1/rentmanbiz/sync/hours`, con la clave S2S.
  - PRG-14: `POST /api/v1/backoffice/stats/harvest`, con usuario del backoffice.
- **Triggers:** se fuerzan escribiendo el documento que escuchan, mejor a través de la API.

**No se pueden forzar:** PRG-11 (solo `replay` de una entrega concreta), PRG-12 y PRG-15 (solo reiniciando). LIS-18 y LIS-30 no tienen emisor en el flujo de CheckBiz.

**Efectos que solo se ven desde dentro del servidor, o no se ven**

- **Sin lectura desde fuera:**
  - Postgres `checklogs_raw` fila a fila, `sync_log`, `task_ratings_raw`, `dim_sync_log`.
  - `employee_daily_reports` fila a fila; desde fuera solo hay recuentos.
- **Se ven desde fuera con credenciales que `qa/` hoy no tiene** (clave S2S o usuario del backoffice): `pattern_snapshots`, los recuentos de `employee_daily_reports`, `backoffice_snapshot_daily` y `maintenance_*`.
- **Solo en Cloud Logging o en el buzón:**
  - Push FCM. Solo se ven cuando dejan `in_app_notifications`, que no es el caso de PRG-05.
  - WhatsApp.
  - Correos SMTP de LIS-04, LIS-16, LIS-18, LIS-24, PRG-01 y de billing.
  - Los fallos silenciados de LIS-02, LIS-09, LIS-10, LIS-13 y LIS-29.

**Sospechas principales**

1. **Webhooks de fichaje duplicados:** LIS-03 más PRG-02 frente a LIS-29.
2. **Doble correo «Servicio Activado»:** LIS-16 frente a `BillingNotifier`.
3. **PRG-03 activo en dev** junto a billing.
4. **Sin patrón inicial no hay patrones nunca** (LIS-01 y LIS-05); y la sucursal automática depende de los datos legales (LIS-06).
5. **PRG-07 pierde lo de una hora** si falla un tick.
6. **PRG-08 se atasca** cuando se acumulan más de 200 tareas avisadas.
7. **SNP-12 sin cron.**
8. **Orden de PRG-09 frente a PRG-14** según la zona horaria del contenedor.

---

## En el código pero no desplegado en desarrollo

- `beforeUserCreatedTrigger`, un trigger de Auth: `SAAS/firebase-firestore-trigger/auth/beforeUserCreated.ts:7`. Se exporta en `SAAS/firebase-firestore-trigger/index.ts:14` pero no está en el CSV, así que en dev no hay bloqueo de altas fraudulentas.
- `cleanupUnverifiedUsers`, programada: `SAAS/auth/cleanup/cleanupUnverifiedUsers.ts:9-56`. No se exporta (`SAAS/core/firebase-entry-schedule/index.ts:5-7`) y no está desplegada.
- `onEmpRespPlanifier`, trigger sobre `employee_responsibilities`: `SAAS/services-saas/checkinbiz/firebase-firestore-trigger/onEmployeeResponsibilityPlanifier.ts:1-12`. Está comentado.
- `task-start-delay.ts`, ruta de Cloud Tasks para el aviso de tarea: `SAAS/services-saas/checkinbiz/firebase-checkinbiz-http/task-start-delay.ts`. No aparece en `firebase-checkinbiz-http/index.ts`.
- `employeeHelperWorker`: `SAAS/services-saas/checkinbiz/firebase-entry-schedule/employeePlanifierWorker.ts:40-51`. Es una función auxiliar que no se exporta.

**Desplegado sin código localizado:** ninguno. Los 25 triggers, los 9 jobs y las 3 HTTP auxiliares citadas se corresponden con exportaciones del código.

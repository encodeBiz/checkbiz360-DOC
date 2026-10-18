# Tareas programadas a escala: repartir en lotes, no recorrer en serie — Documento de Ingeniería

**Proyecto:** encodebiz-api (`services/firebase_sdk/src/programadas`, `services/analytics`, `services/reports`)
**Dominio:** avisos de fichaje y de tarea, planificador diario, cierres de fichajes abiertos, recolector de sucursal, dimensiones, informe diario
**Fecha de inicio:** 2026-10-16
**Prioridad:** 🔴 **ALERTA.** Segunda, justo detrás de [reglas-firestore](../reglas-firestore/README.md). Arranca el **17 o el 18 de octubre de 2026** en cuanto el paso 1 de reglas esté desplegado.
**Estado:** diseñado el 2026-10-16; nada implementado
**Autor:** Jose Acevedo

---

## Contexto y motivación

Todo el trabajo programado de la plataforma está escrito igual desde el primer día: **una
ejecución recorre a todos los clientes**, en serie, con un tope fijo en el código. Funciona
con decenas de empleados por cliente, que es lo que ha habido. Deja de funcionar en cuanto
entra uno grande, y no de golpe: se degrada en silencio.

El caso que lo destapó: una negociación con una empresa de limpieza de mil personas. Con la
cadena de avisos de hoy, mil personas que entran a la misma hora reciben el recordatorio de
fichar a lo largo de los cincuenta minutos siguientes, y como los avisos tienen tres intentos a
−5, 0 y +5 minutos, la mayoría se agota antes de salir. Nadie se entera: el estado queda en
`processed` con motivo `exhausted_offsets`.

Pero no es un problema de ese cliente. Es que **el tiempo de cada job es la suma de todos los
clientes**, así que el grande retrasa a los pequeños, y cada cliente nuevo alarga la cola de
todos. Eso es lo que condiciona la escalabilidad, y por eso se arregla el patrón entero, no
un tope.

## Principio de diseño

> **Ninguna ejecución recorre a todos los clientes. El programador reparte en lotes y cada
> lote es una invocación propia, que Functions escala sola. Los límites los pone la cola, no
> un número en el código.**

---

## Lo que hay hoy

Rutas relativas a `encodebiz-api`. Lo de `firebase_sdk` son Cloud Functions (`onSchedule`)
desplegadas por nombre desde `services/firebase_sdk/src/index.ts:201-228`; lo de `analytics` y
`reports` corre dentro del contenedor con `node-cron`.

| Job | Dónde | Cada | Cómo recorre | Tope | Con mil personas |
|---|---|---|---|---|---|
| **Avisos de fichaje** | `programadas/employeePlanifierWorker.ts:29-38` → `executeEmployeePlanifier.controller.ts` | 5 min | `findDue(horizon, 100)`: `status == active`, `nextRunAt <= ahora+5min`, `limit 100` (`FirestoreEmployeePlanifierRepository.ts:38-43`); 8 en paralelo | **100 por pasada para todos los clientes** | El último aviso sale 50 min tarde; los *offsets* se agotan (`:82-85`, `:150-162`) y la mayoría no sale nunca |
| **Avisos de tarea** | `programadas/taskStartNotificationWorker.ts` | — | Mismo patrón (por confirmar al implementar) | — | Igual |
| **Planificador diario** (crea los avisos del día) | `planifierNotificationWorker.ts:5` (04:00 UTC) → `checkActiveEmployeeWorker.controller.ts:37-48,147` | día | **Todos los empleados activos de todos los clientes** por `collectionGroup`, lotes de 100, 8 en paralelo, 3-5 lecturas por persona | Sin `timeoutSeconds` | Crece con la suma de clientes; el día que pase del tiempo máximo, se corta a medias sin aviso |
| **Cierre de fichajes abiertos** | `sanitizerChecklogs.controller.ts:23` | hora | En serie, mira **sólo la última hora** | — | Lo que no cabe en una pasada no se vuelve a mirar |
| **Recolector de sucursal** | `dailyCollectorData.controller.ts` | hora | Todas las sucursales activas del mundo por `collectionGroup`, en serie | — | Crece con la suma de clientes |
| **Dimensiones** | `analytics/src/jobs/scheduler.ts` (job `dimensiones`, a los :20) → `SyncDimensions.ts:106,258,282` | hora | Ya va **por entidad** (`forEachActiveEntity`), pero en serie, y cada entidad lee toda su plantilla documento a documento y hace un upsert por fila | — | Miles de lecturas y de inserts en serie cada hora |
| **Informe diario** | `reports/src/application/DailyReportCron.ts:93,123` | hora (:05) | `WHERE synced_at >= NOW() - 30 días` **sin índice**; `real_date_market` sin índice | — | Recorre la tabla entera de fichajes cada hora |

---

## Diseño

### 1. Avisos de fichaje: reparto por lotes con Cloud Tasks

Se queda en `firebase_sdk` (ya usamos `firebase-functions` 6, que trae
`firebase-functions/v2/tasks`). No hay corte entre Firebase y un contenedor, y las instancias
las escala Functions.

**El programador deja de enviar y pasa a repartir.** `employeePlanifierWorker` conserva su
nombre y su horario (así no conviven dos emisores) y cambia por dentro:

1. Cada **minuto** (hoy cinco), horizonte `ahora + 1 min`.
2. Consulta todo lo vencido **sin tope**, paginando de 500 en 500 si hace falta.
3. En el mismo lote de escritura marca cada planificador como `queued` con `queuedAt`.
   Es la primera barrera contra el doble envío: la pasada del minuto siguiente no lo vuelve
   a coger.
4. Parte en **lotes de 100** y encola un task por lote en la cola `avisosFichajeLote`
   (`getFunctions().taskQueue(...)`), con nombre `lote-<minuto>-<n>`. Cloud Tasks rechaza un
   nombre repetido durante un tiempo: segunda barrera.

**El handler** (`onTaskDispatched`) recibe los cien ids y, con 10 en paralelo:

- Carga el planificador. Si ya no está en `queued`, lo salta: alguien lo procesó.
- Si lleva más de **10 minutos** de retraso, lo marca `processed` con motivo `expired`, **sin
  enviar**. Un recordatorio de fichar que llega a y media hace daño. Hoy ocurre algo parecido
  con los *offsets* agotados, pero sin dejar constancia de que llegó tarde.
- Si no, ejecuta lo que ya hace `ExecuteEmployeePlanifierController` (push, WhatsApp, y
  reprogramar el siguiente *offset* con `nextRunAt` y `status: active`).

**Rescate**: un planificador en `queued` más de 15 minutos es un task perdido; el programador
lo devuelve a `active` en su siguiente pasada. Hoy ese caso no existe porque no hay cola; con
cola hay que cubrirlo.

**Límites, y dónde viven:**

| Límite | Dónde | Valor de salida |
|---|---|---|
| Envíos en paralelo entre lotes | cola: `rateLimits.maxConcurrentDispatches` | 20 |
| Reintentos de un lote | cola: `retryConfig.maxAttempts`, `minBackoffSeconds` | 3, 10 s |
| Instancias de la función | `maxInstances` | 50 |
| Tiempo por lote | `timeoutSeconds` | 120 |
| Tamaño de lote y paralelismo interno | código | 100 y 10 |
| Caducidad y rescate | código | 10 min y 15 min |

**Control**, que es lo que hoy no existe:

- Cada lote deja una línea de log con `{lote, enviados, fallidos, caducados, retrasoMax}`.
- Una revisión nocturna lista los planificadores con `nextRunAt` pasada hace más de 15
  minutos que sigan en `active` o `queued`. Si la lista no está vacía, nos quedamos cortos
  en algún sitio y lo sabemos antes que el cliente.
- La profundidad de la cola se ve en la consola de GCP. Umbral de alarma: retraso máximo por
  encima de 2 minutos, o un solo caducado.

**Aritmética**: mil personas a la misma hora son diez lotes; con 20 lotes en paralelo y 10
envíos por lote, el último aviso sale en segundos. El pico real de un cliente de mil es menor,
porque entran escalonados por centro.

### 2. Avisos de tarea: el mismo motor

`taskStartNotificationWorker` pasa por el mismo programador y el mismo tipo de handler, con su
propia cola. Medio día una vez hecho el de fichaje.

### 3. Batch horarios y diarios: una task por entidad

El mismo principio, con otro grano: el programador lista las entidades activas y encola **una
task por entidad**; el handler trabaja sólo con esa entidad, leyendo por su ruta
(`entities/{e}/…`) y no por `collectionGroup` global. Así un cliente de mil cabe en su propia
invocación y nunca retrasa a nadie.

- **Planificador diario (04:00)**: task por entidad, `timeoutSeconds: 540`. Es el que más
  se beneficia: hoy es la única ejecución que recorre a toda la plataforma persona a persona.
- **Cierre de fichajes abiertos**: task por entidad, y la ventana pasa de una hora a tres. Ya
  usa ids determinísticos para no duplicar (`sanitizerChecklogs.controller.ts:83`), así que
  solaparse es seguro.
- **Recolector de sucursal**: task por entidad.
- **Dimensiones**: esto corre en el contenedor de analytics, no en Functions, así que no lleva
  Cloud Tasks. Se arregla con lo mismo a otra escala: cuatro entidades en paralelo
  (`p-limit`), lecturas en bloque (`getAll`) y un solo `INSERT … ON CONFLICT` por tabla en vez
  de uno por fila. Incremental por `updatedAt` en una fase posterior.
- **Informe diario**: no es diseño, es una migración con tres índices:
  `checklogs_raw(synced_at)`, `checklogs_raw(real_date_market)` y
  `checklogs_raw(entity_id, ts)`. Se hace el primer día.

### Coste

Cloud Tasks cobra por millón de operaciones; mil personas son unos cien lotes al día. Las
invocaciones de Functions y las lecturas de Firestore son las mismas que hoy, sólo que
repartidas. No hay infraestructura nueva nuestra.

---

## Pruebas

- **Carga sintética en dev**: un script crea mil planificadores en `active` con el mismo
  `nextRunAt` para una entidad de pruebas y se mide el retraso máximo entre `nextRunAt` y
  el envío. Objetivo: **menos de dos minutos**. Hoy serían cincuenta.
- **Doble envío**: lanzar el programador dos veces seguidas sobre el mismo lote y comprobar
  que el handler salta los que ya no están en `queued`.
- **Task perdido**: dejar uno en `queued` y comprobar que el rescate lo recupera a los 15 min.
- **Caducidad**: uno con `nextRunAt` de hace 20 min no se envía y queda `expired`.
- Suite de QA entera después, fuera de la ventana de medianoche de Madrid.

## Plan de ejecución

Casillas por rellenar con hora, quién y resultado.

- [ ] **Día 1**: migración de índices del informe diario; programador y handler de avisos de
      fichaje; función nueva en `index.ts` **por su nombre** (lo que no está en el índice se
      poda al desplegar); activar la API de Cloud Tasks en `dev-encodebiz`; deploy a dev con
      `--project dev-encodebiz`; carga sintética y medida.
- [ ] **Día 2**: log por lote, revisión nocturna y umbral de alarma; avisos de tarea sobre el
      mismo motor; planificador diario por entidad.
- [ ] **Día 3**: cierre de fichajes y recolector por entidad; dimensiones en paralelo y en
      bloque; a staging; apuntar en
      [proximo-pase-back §7](../../deployment-prod/proximo-pase-back.md) lo que necesita prod.
- [ ] **Producción**: en el pase, con las reglas ya cerradas. Necesita fuera del código: la API
      de Cloud Tasks en `encodebiz-services`, la migración, y las funciones nuevas en el
      despliegue por nombre.

## Trampas conocidas

- **Functions se despliegan por nombre**: una función que no esté en `index.ts` se poda. Fue
  lo que nos quitó funciones en el pase de septiembre.
- El programador y el handler **tienen que salir en el mismo despliegue**: el programador
  nuevo ya no envía, así que sin handler no sale ningún aviso.
- Cloud Tasks es *al menos una vez*: el handler se diseña para repetirse. Las dos barreras de
  arriba no son opcionales.
- La cola la crea Firebase en el primer despliegue, pero la API tiene que estar activada antes
  en cada proyecto, dev primero.

## Decisiones abiertas (Jose)

1. Caducidad del aviso: ¿10 minutos, o el último *offset* (+5) y nada más?
2. Dimensiones: ¿incremental por `updatedAt` ahora, o después de ver cuánto baja con el
   paralelismo y los inserts en bloque?
3. ¿La revisión nocturna avisa a soporte por in-app, o basta con el log y el panel del backoffice?

## Referencias

- [reglas-firestore](../reglas-firestore/README.md): va antes que esto.
- [modulos/notificaciones.md](../../modulos/notificaciones.md): push FCM e in-app.
- [DEPLOY.md](../../DEPLOY.md) y [entornos-cloud-functions.md](../../entornos-cloud-functions.md): despliegue de functions por nombre y por proyecto.
- [deployment-prod/proximo-pase-back.md](../../deployment-prod/proximo-pase-back.md) §7.

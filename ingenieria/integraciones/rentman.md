# Add-on RentmanBiz — funcionamiento detallado

> `addonId`: **`rentmanbiz`** (patrón Biz, como checkinbiz o passinbiz). El tercero con el
> que habla se llama Rentman; nuestro add-on, RentmanBiz.

Qué hace, cuándo lo hace y qué pasa cuando algo va mal. Es el documento de referencia
del comportamiento; el diseño y las decisiones están en `../rentman-integration/`.

Servicio: `services/rentman` (Express, puerto 3008) en **encodebiz-api**.

---

## 1. La idea en una frase

Cuando un trabajador cierra su jornada en checkbiz, las horas aparecen solas en el
proyecto de Rentman — y si alguien las cambia allí, checkbiz no se entera de oídas: lo
detecta y avisa, porque la autoridad sobre el registro horario es suya.

## 2. Por qué checkbiz manda en las horas (D2)

El `timeregistration` de Rentman es, para el cliente, un dato de proyecto. Para checkbiz
es el **registro legal de jornada**, del que responde ante una inspección. No pueden
tener el mismo peso, así que la decisión (cerrada el 2026-08-01) es que **encodeBiz es
siempre la autoridad**:

- Una edición hecha en Rentman **nunca** vuelve ni sobreescribe el fichaje.
- Se detecta, se marca `diverged` y se avisa. La decisión es del cliente, con las dos
  versiones delante.
- Tampoco se pisa su edición automáticamente: reimputar por nuestra cuenta sería otra
  decisión de producto, y no está tomada.

## 3. Una pasada, paso a paso

El servicio ejecuta una pasada por cliente **cada 15 minutos** (`RENTMAN_HOURS_CRON`),
sin solaparse consigo misma. Cada pasada hace tres cosas, en este orden.

### 3.1 Detectar

Lee `checklogs_raw` de PostgreSQL — la tabla que llena el servicio `sync`— buscando
**jornadas cerradas** en los últimos 7 días (`RENTMAN_HOURS_LOOKBACK_DAYS`).

- Una jornada es un **ciclo**: el checkin y todo lo que cuelga de él por `checkin_ref`.
- La ventana se aplica sobre el **checkout**, no sobre la entrada: quien entra a las
  23:50 y sale a las 07:00 aparece cuando cierra, no antes.
- Solo cuentan los eventos con `status = 'valid'`. Un fichaje fallido no existe para esto.
- Sin checkout no hay jornada. Las jornadas abiertas o incompletas **no se imputan**.

**El descanso no viaja en el fichaje.** O el centro lo tiene fijo por configuración
(`advance.disableBreak` + `timeBreak`, en minutos, leído de Firestore), o se deduce
sumando los pares restin/restout válidos. Es **la misma regla que el informe legal**, a
propósito: si aquí divergiera, el cliente tendría dos verdades para la misma jornada.

De ahí salen tres cifras: **bruto** (salida − entrada), **descanso** y **neto**.

Cada jornada se encola en `rentman_time_registration` con una **huella** (`pushed_hash`)
de sus horas. Si la huella no cambia, no se toca nada. Si la jornada se corrigió en
checkbiz, la huella cambia y vuelve a la cola: mandamos nosotros, así que Rentman se entera.

Los empleados **sin mapeo** se ignoran en silencio: no es un error, es que no hay a quién
imputar.

### 3.2 Empujar

Cada jornada pendiente se escribe en Rentman como `timeregistration` (el fichaje), no
como `timeregistrationactivity` (que es el desglose de coste por función). Como máximo
50 por pasada (`RENTMAN_HOURS_PUSH_BUDGET`).

El cuerpo lleva la referencia del trabajador **como ruta** (`/crew/226`), inicio y fin en
ISO con el **offset del centro** —Rentman muestra la hora tal como se la mandas—, la
duración **neta en segundos**, el descanso, el tipo de horas *trabajado* de esa cuenta y
un `remark` con `checkbiz:{checkinId}` para poder rastrear el origen desde Rentman.

### 3.3 Auditar

Las jornadas ya imputadas se releen de Rentman cada 24 h
(`RENTMAN_HOURS_AUDIT_EVERY_HOURS`), como mucho 25 por pasada
(`RENTMAN_HOURS_AUDIT_BUDGET`). Se comparan inicio, fin, duración neta y descanso:

- Si coinciden, se sella la comprobación y sigue.
- Si no, la jornada pasa a `diverged` con el detalle de qué cambió, se anota en
  `rentman_sync_log` y aparece en el endpoint de divergencias.
- Si el registro **ya no existe** en Rentman, también es divergencia.

Un error puntual de lectura no convierte una jornada en divergente: se reintenta.

## 4. Estados de una jornada

| Estado | Qué significa |
|---|---|
| `pending` | Detectada y en cola; aún no imputada |
| `synced` | Imputada en Rentman; se auditará cada 24 h |
| `failed` | Fallo transitorio (red, 5xx). Se reintenta en la siguiente pasada |
| `skipped` | Rentman dijo que no, o no había nada que imputar. **No se reintenta** |
| `diverged` | Alguien la editó o la borró en Rentman. El fichaje sigue intacto |

## 5. Qué pasa cuando algo va mal

- **Rentman caído o lento** → la jornada queda `failed` y la siguiente pasada lo reintenta.
  El fichaje del empleado no se entera: el flujo es *best-effort* de punta a punta.
- **Rate limit (429)** → se corta la pasada entera y se retoma en la siguiente. Medido en
  sandbox: 120 peticiones en 16 s sin cortes, así que hoy no es la restricción.
- **403** → no es rate limit, aunque durante meses se creyó que sí. Lo devuelven
  endpoints que no existen. Es terminal: no se reintenta.
- **400 — solape** → Rentman rechaza dos registros del mismo trabajador en el mismo
  periodo ("Ya se ha registrado el horario o se ha solicitado una ausencia para este
  periodo"). Es un **no definitivo**: la jornada queda `skipped` con el motivo, para que
  se vea, en vez de reintentarse eternamente contra un muro.
- **Empleado sin mapear** → se ignora; aparece como cobertura incompleta en el panel.
- **Jornada sin tiempo neto** → `skipped`.
- **La integración se desactiva** → la pasada termina de inmediato con
  `integration_disabled`. Nada se borra: si se reactiva, sigue donde estaba.

## 6. Endpoints

**Gestión** (Firebase ID token) — `/api/v1/rentmanbiz`:

| Método y ruta | Para qué |
|---|---|
| `GET /status` | Vivo y versión del módulo |
| **Conexión** | |
| `POST /activate` `{entityId}` | Alta del add-on. 409 si falta checkbiz activo |
| `POST /connect` `{entityId, token}` | Valida contra Rentman, cifra y conecta |
| `POST /disconnect` `{entityId}` | Retira la credencial; sigue de alta |
| `POST /active` `{entityId, active}` | Enciende/apaga sin borrar nada |
| `GET /connection/:entityId` | Estado: `{active, status, tokenRef, lastError, …}` |
| `GET /test-connection/:entityId` | Reprueba la credencial ya guardada |
| **Catálogo** | |
| `GET /catalogue/preview/:entityId` | Qué se importaría. **No escribe nada** |
| `GET /catalogue/summary/:entityId` | Qué hay importado **ahora mismo**, por tipo y estado. Persiste entre recargas, al contrario que el resultado de importar |
| `POST /catalogue/import` `{entityId, dryRun?, warehouseTasks?}` | Importa. **Simula por defecto** |
| `GET /pending/:entityId` | Lo que falta por completar, con su motivo |
| `POST /pending/crew/complete` `{entityId, rentmanCrewId, email}` | Completa el correo y crea la ficha |
| `GET /activity/:entityId` | Bitácora reciente (sale de PostgreSQL) |

> **`detail` es siempre texto, o `null`.** En los tres endpoints que lo devuelven
> —`/activity`, `/pending` y `/hours/divergences`— es una frase pensada para leerse en
> pantalla, nunca un objeto. Cuando el motivo viene del proveedor y el proveedor no da
> una frase, se sustituye por una nuestra y el cuerpo original queda en nuestros logs, no
> en la respuesta: `detail` es campo de pantalla, no volcado de diagnóstico. Quien lo
> consuma puede pintarlo tal cual sin comprobar de qué tipo es.
| **Personas** | |
| `GET /crew/:entityId` | Plantilla de Rentman y quién está sin mapear |
| `GET /mappings/:entityId` · `POST /mappings` | Emparejamientos empleado ↔ crew |
| **Horas** | |
| `GET /hours/summary/:entityId` | Recuento por estado y última imputación |
| `GET /hours/entries/:entityId?from=&to=&limit=` | Jornadas imputadas del periodo **con su total en horas** y el nombre del empleado. Por defecto, 30 días |
| `POST /hours/sync-now` `{entityId}` | Sincroniza al momento. 429 si hay una pasada en curso o no ha pasado el enfriamiento |
| `GET /hours/divergences/:entityId` | Jornadas tocadas en Rentman |

**S2S** (`x-encodebiz-key`): `POST /api/v1/rentmanbiz/sync/hours` — fuerza una pasada;
`{entityId}` opcional, sin él va a por todos los clientes con empleados mapeados.

**Webhook**: existe la ruta pero está **aparcada**. La vía es el sondeo.

## 7. Persistencia

- `entities/{entityId}/integrations/rentman` (Firestore) — token cifrado y `enabled`.
- `rentman_employee_mapping` (PostgreSQL) — `crew ↔ employee` por cliente.
- `rentman_time_registration` (PostgreSQL, migración 009) — una fila por jornada
  imputada: horas, huella, estado, id de Rentman, última auditoría.
- `rentman_sync_log` (PostgreSQL) — bitácora: `push_hours`, `hours_divergence`, …

> Las migraciones **no** las aplica el despliegue. Toda migración nueva se aplica a mano
> por SSH en cada entorno.

## 8. Lo que la API de Rentman enseñó (verificado en sandbox)

Cuatro cosas que solo se aprenden escribiendo, y que costaron un rediseño:

1. **`leavetype` es obligatorio.** Sin él, la API responde 500 sin decir qué falta. Hay
   que mandar el tipo *trabajado* de esa cuenta, y los ids **no son universales**: se
   resuelve leyendo `/leavetypes` de cada cliente.
2. **`duration` es neto** y lo recalcula Rentman (`fin − inicio − descanso`). Comparar
   contra el bruto habría marcado como divergente toda jornada con descanso.
3. **`remark` persiste**, así que la trazabilidad viaja dentro del propio registro.
4. **Rechaza solapes** con un 400 explícito.

Además: la colección de fichajes es **singular** (`/timeregistration`; la plural da 403),
las referencias son rutas string, las duraciones van en segundos, no hay filtro por
`modified` pero sí `sort=-modified`, y `DELETE /timeregistration/{id}` funciona.

## 9. Configuración

| Variable | Por defecto | Para qué |
|---|---|---|
| `ENC_KEY` | — | Clave AES-256-GCM de las credenciales de add-ons |
| `RENTMAN_HOURS_CRON` | `*/15 * * * *` | Cadencia de la pasada |
| `RENTMAN_HOURS_CRON_DISABLED` | `false` | Apagar el cron sin tocar código |
| `RENTMAN_HOURS_LOOKBACK_DAYS` | `7` | Ventana de jornadas por pasada |
| `RENTMAN_HOURS_PUSH_BUDGET` | `50` | Máximo de imputaciones por pasada |
| `RENTMAN_HOURS_AUDIT_BUDGET` | `25` | Máximo de auditorías por pasada |
| `RENTMAN_HOURS_AUDIT_EVERY_HOURS` | `24` | Cada cuánto se re-audita |
| `RENTMAN_SYNC_NOW_COOLDOWN_SECONDS` | `60` | Enfriamiento entre sincronizaciones a mano |
| `RENTMAN_LEAVETYPE_REF` | *(auto)* | Fuerza el tipo de horas |
| `RENTMAN_TIMEREGISTRATION_PATH` | `/timeregistration` | Ruta de escritura |

## 10. La capa de catálogo: eventos, asignaciones y tareas

**Implementada** (`importCatalogue`). Cinco pasos, en el orden que impone la realidad:
personas → centros → responsabilidades → tareas de montaje → trabajo de almacén. Simula
por defecto: escribir exige `dryRun: false`.

### 10.1 El evento es el centro de trabajo (D1, cerrada)

Un `project` de Rentman —un montaje, un evento— se corresponde con un **branch** de
checkbiz, con la localización del evento convertida en **geocerca de fichaje**. La razón
es del oficio: en eventos y AV nadie ficha en la oficina del cliente, se ficha en el
pabellón o en el teatro. El proyecto es lo que semánticamente equivale a un centro de
trabajo, y cada semana hay centros nuevos.

El **cliente** de Rentman (`customer` → `contact`) **no** es un centro. En esta fase se
guarda como atributo del branch; la estructura de Clientes/Contactos es una iniciativa de
plataforma (Fase 2), no del add-on.

Sincronización **bidireccional**, con la salvaguarda de siempre: los campos que solo
existen en checkbiz —geocerca afinada a mano, horarios, biometría— **no los pisa nunca la
sincronización**. Un proyecto que llega sin coordenadas se crea **inactivo**, marcado como
"requiere configuración", y la pasada continúa: un dato incompleto no bloquea al resto.

### 10.2 La asignación genera las tareas

`projectcrew` cruza trabajador, función de proyecto y periodo previsto. No es un turno ni
una jornada: es **el trabajo**. De ahí se derivan las **tareas** del módulo `tasks`, que
son solo de checkbiz — Rentman no tiene tareas y no se le devuelve nada a ese nivel.

Es la pieza de adopción: el trabajador abre la app, ve a qué evento va, ficha dentro de la
geocerca de ese evento, ejecuta las tareas de su función y, al cerrar, las horas vuelven
solas a Rentman imputadas a ese proyecto. El recorrido completo sin transcribir nada.

No confundir las tres capas: la **asignación** define el trabajo (→ tareas), la **jornada**
es el envoltorio de tiempo (→ `timeregistration`) y puede cubrir varias tareas, y el
**desglose por función** (→ `timeregistrationactivity`) es la capa de coste, que sigue
fuera de alcance.

### 10.3 El trabajo de almacén (alquileres y ventas)

Un alquiler en seco o una venta no llevan gente a ningún sitio, pero sí generan trabajo:
alguien prepara el material antes de que el cliente lo recoja y alguien lo revisa cuando
vuelve. Ese trabajo hoy no lo registra nadie, y para una empresa de alquiler es
probablemente lo que más valor añade el add-on.

El **dónde** no se pregunta: lo dice el subproyecto en `asset_location_from` (en la cuenta
de pruebas lo traen los 57). Por eso se sigue por subproyecto y no por proyecto — uno
grande puede partirse en varios con almacenes distintos, y si cambian el almacén de
origen, la tarea se mueve sola.

Dos tareas y no una: preparar para la salida (`equipment_period_from`) y recibir a la
vuelta (`equipment_period_to`). Cuando no hay vuelta —una venta no vuelve— sólo la primera.

Nacen **sin asignar**: en Rentman no hay nadie apuntado a esto, así que inventar el
destinatario sería peor que dejarlo abierto. Lo reparte quien sabe qué gente tiene esa
mañana, y ya tiene delante la plantilla del almacén porque su adscripción también se
importa.

**Apagado de fábrica** (`warehouseTasks: true` para encenderlo): decenas de operaciones por
semana llenarían el móvil del almacén de tareas que quizá esa empresa no gestiona así.

### 10.4 Qué falta para poder implementarlo

- **Tablas de mapeo propias** para `project` y `projectcrew`, con `updateHash`, `updatedAt`
  por lado y `syncedAt`, igual que la de empleados.
- **Pull incremental**: no hay filtro por `modified` en la API, pero sí `sort=-modified`;
  se pagina en orden descendente hasta la marca de agua.
- **Prevención de eco**: se guarda el `updateHash` de Rentman tras cada escritura y lectura;
  si vuelve el hash que ya teníamos, es nuestro propio cambio y se ignora.
- **Escritura de `project` y `projectcrew`**: nunca probada, ni siquiera en sandbox.
- **Tres decisiones de producto**: rol por defecto del empleado importado (D3), qué hacer
  cuando un proyecto no trae `lat/lng` —geocodificar o dejarlo a mano— (D4), y qué hacer con
  un crew sin correo (D5).

## 11. Lo que todavía no está

- **La pantalla del front.** El back está entero; la interfaz se está implementando con
  `prompt-front-rentmanbiz.md`.
- **Empujar tareas a Rentman.** Se creía imposible; su OpenAPI 1.15.0 demuestra que
  **sí tienen tareas** (`POST /tasks`, con asignaciones, subtareas y estados). Queda para
  la siguiente fase.
- **Empujar personas o asignaciones**: eso sí es imposible. `/crew` y `/projectcrew` sólo
  admiten lectura. No es un permiso: la operación no existe en su API.
- **Corregir horas ya imputadas**: `PUT /timeregistration/{id}` existe, pero por D2 no se
  pisan las ediciones del cliente. Decisión, no limitación.
- **La monetización** (en beta no se cobra por activar).
- **La cuenta real del cliente**: todo lo probado hasta hoy es sandbox.

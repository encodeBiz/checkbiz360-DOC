# Alertas operativas por correo · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS — CheckBiz360
**Dominio:** alertas del dashboard operativo × correo a owner, admin y supervisores
**Fecha:** 2026-10-22
**Estado:** diseño cerrado el 2026-10-22 · fases 1 y 2 (suelo y resumen de la mañana) en
producción para todas las empresas desde el 2026-10-28 (#233, hotfix #235) · fases 3 y 4 sin
empezar · **fase 3b (pendientes de decisión, §12) y ajustes en Herramientas → Alertas por correo (§6): en producción el 2026-10-29** (API #240, panel #125)
**Autor:** Jose Acevedo

---

## De dónde sale

Jose, 2026-10-22: «es necesario configurar en alguna parte del panel las alertas por email
para la empresa: que los supervisores, admin, owner o todos reciban las alertas más
importantes, como *no se ha fichado en tal sucursal*». Tres condiciones del mismo día:

- «En el caso de supervisores solo deben llegar las alertas a los branches adecuados.»
- «El momentum es increíblemente importante: a qué hora salen los correos es el momento
  operativo que hay que fijar.»
- «Cuidado con la escalabilidad, puede que entre un cliente de 1000 empleados.» Y: «esto no
  puede ir contra Firebase; son cosas de back que no necesitan reactividad, es Postgres que
  guarda históricos».

No confundir con [avisos-por-correo](../avisos-por-correo/README.md): aquél es el correo **a la
persona** con sus tareas y su semana; éste es el correo **al que manda** con lo que va mal.

## El principio

> **Las alertas que ya calcula el dashboard salen por correo a quien puede actuar, en el
> momento en que todavía puede, y nunca dos veces por lo mismo. El supervisor ve su centro;
> el dueño, la empresa. Todo sobre Postgres: el cálculo, los destinatarios, el histórico y la
> cola de envío.**

---

## Lo que hay hoy

Rutas relativas a `encodebiz-api`.

- **Las alertas existen y están bien hechas.** `GET /api/analytics/panel/alerts`
  (`services/analytics/src/interfaces/panel.router.ts`) → `BuildPanelAlerts.ts` → `rules.ts`.
  Doce reglas con doble umbral ([ADR-007](../dashboard-operativo/adr/ADR-007-alertas-que-se-leen.md)),
  cada una con `scope.branchId` (o `null` si es de empresa), `severity`, `target` y `params`.
  Se calculan al pedirlas y se cortan a 8 (`THRESHOLDS.maxAlerts`).
- **No salen por ningún canal.** ADR-007 §Consecuencias: «sin envío por push o correo en esta
  fase». El único correo que hoy recibe una empresa es de facturación, almacenamiento y el
  código de soporte, todos a `billingEmail`.
- **No hay preferencia de avisos** por empresa ni por administrador. La única casilla es por
  empleado (`calendar/config.emailNotifications`, de avisos-por-correo).
- **Los destinatarios viven en Firestore.** Owner y admin del panel en
  `user_entity_roles/{uid}_{entityId}` (`role`, `status`, sin correo: el correo está en Auth).
  Supervisores en `entities/{e}/employee_responsibilities` (`level`, `scope.branchId`).
  Ninguno de los dos está espejado en Postgres.
- **Infraestructura de correo:** `EmailService` (shared) por SMTP de SES, plantillas en
  `emails_template/{TYPE}_{locale}`, y desde la migración 042 cada envío queda en
  `email_message` con lo que SES cuenta de él.
- **Planificador de analytics** (`services/analytics/src/jobs/scheduler.ts`): un tic por
  minuto; dimensiones a los :20, cierre diario a los :10 (04:00 locales de cada centro),
  conciliación de fichajes cada 30 min. Recorre las entidades activas en serie con
  `forEachActiveEntity`.
- **El espejo de fichajes** (`checklogs_raw`) lo escribe el trigger `onChecklogSync`
  (`services/firebase_sdk/src/sync/onChecklogSync.ts`) con 7 s de tiempo máximo y **sin
  reintento**: si falla, lo anota y lo suelta. La conciliación de los :00 y :30 (TDR-004) lo
  recoge hasta media hora después. Para una pantalla vale; para un correo que sale a los 5
  minutos, no (§7).

---

## 1. Qué alertas, con qué ritmo y a quién

| Regla | Ámbito | Ritmo | Owner/admin | Supervisor |
|---|---|---|---|---|
| `no_presence` Nadie en el centro | sucursal | inmediata | sí | su centro |
| `attendance_low` Fichaje bajo hoy | sucursal | inmediata | sí | su centro |
| `tasks_start_late` Tareas sin empezar | sucursal | inmediata | sí | su centro |
| `late_high` Muchos retrasos | sucursal | resumen (ayer) | sí | su centro |
| `untracked_high` Jornadas sin cerrar | sucursal | resumen (ayer) | sí | su centro |
| `tasks_overdue` Tareas vencidas | sucursal | resumen | sí | su centro |
| `availability_low` Disponibilidad baja | sucursal | resumen | sí | su centro |
| `week_coverage_low` Fichaje bajo (semana) | sucursal | resumen, **lunes** | sí | su centro |
| `cost_rising` Coste al alza | empresa | resumen, **lunes** | sí | no |
| `rate_missing` Faltan tarifas | empresa | resumen, **lunes** | sí | no |
| `exits_high` Muchas bajas | empresa | resumen, **lunes** | sí | no |
| `access_not_delivered` Acceso que no llegó | empresa | resumen | sí | no |
| `notice_unsigned` Hoja informativa sin firmar | empresa | resumen, **rojo** | sí | no |
| `long_day` Jornadas de más de 9 h (configuradas) | empresa | resumen, naranja | sí | no |
| `no_weekly_rest` Sin descanso semanal (configurado) | empresa | resumen, naranja | sí | no |

**Las tres últimas, Jose, 2026-11-06:** «12 personas con jornada configurada de más de 9 h, esto
es crucial igual que los empleados sin informe firmado […] si no tienen un documento de tipo Hoja
informativa de protección de datos debe saltar alarma». Las dos de horario eran avisos de la
pestaña Análisis (`BuildPlannedHours`) que nadie veía en la portada ni en el correo. Salen del
`weekPlan` que checkinbiz guarda en el **último fichaje de los 14 días** de cada persona activa
(misma fuente primera que el análisis, sin recorrer el calendario): quien no ha fichado no entra.
Umbrales en `rules.ts` (9 h; 7 días con horas). Naranja porque un convenio puede ampararlo: se
dice el hecho y se pide comprobar la ficha. La hoja sale de `dim_employees.notice_signed_at`
(migración 056, espejo de `employee.dataProtectionNotice` cada hora): toda ficha que puede
acusar recibo (ni `fired`, ni `inactive`, ni `pending`) sin firma, enviada o no; el texto dice
cuántas están sin enviar. Roja desde una persona. Las tres repiten como las demás: el día que
aparecen, al subir de gravedad y los lunes.

Las tres de ahora mismo son las únicas en las que una llamada a tiempo cambia el día. El
resto describe ayer, la semana o el mes: se leen con el café, no interrumpen.

Las de empresa (coste, tarifas, bajas, acceso) son cosa del dueño. Al supervisor no le llegan
nunca, tenga el alcance que tenga.

## 2. Quién lo recibe: owner y admin, nadie más

> **Cambio del 2026-10-28.** Tras el primer resumen en producción, Jose: «esto solo es para
> admin y owner, nadie más». Queda sin efecto el reparto por sucursal a supervisores y managers
> del 22-oct, y las direcciones extra. Hotfix #235.

- **Owner y admin del panel** (`user_entity_roles`, `status = active`, sin los asientos de
  soporte), espejados en `dim_panel_users`: todas las alertas de todos los centros, más las de
  empresa. Una persona con los dos asientos, o con el mismo correo en dos, recibe **un** correo.
- **Nadie más.** Una responsabilidad de supervisor o manager con centro no da correo; tampoco
  ser empleado. Las columnas `to_supervisors` y `extra_recipients` de `alert_email_settings`
  siguen en la tabla y no se leen.

Ojo: tener asiento de admin basta. Una cuenta de admin puesta para otra cosa (la del revisor de
OpenAI, `openia@`, sin buzón) también lo recibe; si no debe, se le quita el asiento.

Las alertas se calculan **una vez por empresa**; el correo es el mismo para todos sus owners y
admins, salvo el saludo y el pie («propietario» / «administrador»).

## 3. El momento

Hora local de la **sucursal** para lo inmediato (sus turnos), hora local de la **empresa**
para el resumen (`dim_calendars` con `scope = 'entity'`, columna `timezone`).

### Inmediatas

| Alerta | Sale cuando | Tope |
|---|---|---|
| Nadie en el centro | A los 5 min de pasar la hora del primer turno + tolerancia, sin nadie fichado (la regla ya exige 2 previstos) | 1 por sucursal y día |
| Fichaje bajo hoy | Falta más de la mitad de los que ya debían estar, **sostenido 10 min** (dos comprobaciones seguidas) | 1 por sucursal y día |
| Tareas sin empezar | 3 o más con la hora de inicio pasada y en `assigned`, sostenido 10 min | 1 por sucursal y día |

Si a las 9:40 entra alguien, no se manda un «ya hay gente»: quien llamó ya lo sabe. Si a las
9:06 faltan 3 de 4 y a las 9:16 están todos, no sale nada: la confirmación de dos
comprobaciones es la diferencia entre llegar a tiempo y gritar por un semáforo.

### Resumen de la mañana

Un correo, a las **8:00 hora local de la empresa** (configurable entre 6:00 y 10:00). Va
detrás del cierre diario de las 04:00, así que lo de ayer ya está en `operational_daily`, y
antes de que el dueño se meta en el día.

- **Cada día, lo nuevo:** jornadas sin cerrar de ayer, muchos retrasos de ayer, tareas
  vencidas, disponibilidad baja de la semana.
- **Solo el lunes, lo lento:** cobertura baja de la semana cerrada y las de empresa (coste al
  alza, faltan tarifas, muchas bajas) mientras sigan vivas.
- Una alerta entra además el día que **aparece por primera vez** o **sube de gravedad**,
  aunque no sea lunes. Después, solo el lunes.
- **Sin nada nuevo, no hay correo.** Un resumen que a veces no llega vale más que uno que
  llega siempre vacío: si coste al alza sale veinte mañanas seguidas, el día 21 nadie lo lee.

### Cuándo no se manda nada

- Sucursal sin turno previsto ese día (domingo, festivo del calendario, cerrada).
- Empresa sin actividad en 30 días (`listActiveEntities`).
- **Nunca entre las 22:00 y las 6:00 locales**, aunque un turno nocturno dispare la regla:
  queda para el resumen.
- Empresa con el interruptor general apagado, o la regla apagada en sus ajustes.

## 4. Cómo se calcula sin recorrer a nadie

Lo que no puede pasar con mil empleados: un tic de 5 minutos que recorra todas las empresas y
recalcule el día de cada una para mirar, casi siempre, nada. El coste tiene que depender de
cuántas comprobaciones hay pendientes, no de cuánta gente tiene nadie.

### 4.1 Lo inmediato se programa, no se sondea

El **cierre diario** de las 04:00 ya recorre cada centro. En esa misma pasada, con
`dim_calendar_days` del día que empieza, deja escritos los **momentos de comprobación** del
centro en `alert_checks`:

```text
sucursal X · no_presence     · 09:10
sucursal X · attendance_low  · 09:15 y 09:25   (la segunda confirma la primera)
sucursal X · tasks_start_late· cada 30 min mientras haya tareas con inicio hoy
```

El tic de 5 minutos del planificador **no recorre empresas**: lee las filas con `check_at <=
now()` y `checked_at IS NULL`, que son un puñado en cualquier instante. Cada comprobación es
una consulta acotada a los fichajes y tareas **de hoy de esa sucursal** (`buildOperationalDay`
con `branchId`), sobre el índice `(entity_id, timestamp)` de `checklogs_raw` que
[analisis-a-escala](../analisis-a-escala/README.md) ya señala que falta.

Una empresa de mil personas y ochenta centros con tres turnos genera unas 250 comprobaciones
al día, repartidas; el tic ve diez o doce cada vez. La unidad de trabajo es la sucursal, que es
justo lo que [programadas-a-escala](../programadas-a-escala/README.md) quiere: el día que se
reparta con Cloud Tasks, se mueve sin tocar la lógica.

Si un centro cambia de horario a media mañana, sus momentos de hoy no se rehacen: el cierre
de mañana los escribe con el calendario nuevo. Se acepta.

### 4.2 El resumen no cabe en el formato del panel

El panel corta a 8 alertas. Para una empresa de 80 centros ese tope descartaría las de 70, y
el supervisor de uno de ellos no recibiría la suya. `evaluateAlerts` recibe un parámetro para
**no cortar**; el panel sigue con 8, el correo calcula todas y reparte.

El correo del dueño de esa empresa no puede ser 60 líneas: **se agrupa por tipo con recuento
y los tres centros peores**, y el enlace al panel para el detalle. El del supervisor va al
detalle, porque son dos o tres cosas de su centro.

### 4.3 Lo de ayer no se recalcula

`operational_daily` ya tiene por centro y día lo que piden jornadas sin cerrar, retrasos y
cobertura; el resumen lo suma, no vuelve al crudo. `buildPanelAlerts` ya hace esto para
`week_coverage_low` y `untracked_high`; `late_high` del resumen pasa a leer `late` y
`late_minutes` de ayer en lugar del día en curso. Las de empresa van una vez por semana y son
baratas.

### 4.4 Los destinatarios no se resuelven en Firestore cada mañana

Resolver cien supervisores con sus sucursales es cien lecturas por empresa y día; con muchas
empresas, miles. Se espejan en el **job de dimensiones** (`SyncDimensions`, cada hora a los
:20), como calendarios y empleados:

- `dim_panel_users` (`uid`, `entity_id`, `role`, `status`, `email`, `language`, `source`):
  de `user_entity_roles`, sin los asientos de soporte. El correo sale de Auth por `uid` una
  vez y se guarda; solo se vuelve a Auth cuando aparece un uid nuevo.
- `dim_responsibilities` (`entity_id`, `employee_id`, `key`, `level`, `branch_id`): de
  `employee_responsibilities`. El correo del empleado lo da `dim_employees`, que gana la
  columna `email`.
- La zona horaria y el idioma de la empresa ya están o se añaden al espejo de la entidad
  (`dim_calendars` scope `entity`; `language` junto a `dim_panel_users`).

El reparto es un `JOIN`. Y es la **única lectura de Firestore de todo el frente**: la que ya
se hace hoy, en el job que ya existe.

### 4.5 El envío se encola, no se hace en el job

Cien supervisores más los admins son cien correos a las 8:00 de una sola empresa. Si el job
los manda uno a uno por SMTP se queda bloqueado y arrastra a las empresas siguientes.

- El job escribe cada correo en `email_outbox` y termina.
- Un **despachador** (tic del mismo planificador) toma lo pendiente, manda por `EmailService`
  con concurrencia acotada (8) y dentro de la cuota de SES, marca `sent_at` o `attempts++` y
  `last_error`. Tres intentos con espera creciente; después queda `failed` y a la vista.
- La hora del resumen es «no antes de»: los resúmenes se reparten en los **veinte minutos
  siguientes** por lotes de empresas, en vez de disparar todos a la vez a las 8:00:00 de
  Madrid.
- Cada envío queda en `email_message` como el resto de correos (`kind = alerts_immediate |
  alerts_digest`, `entity_id`, `employee_id` cuando lo hay).

No pasa por el trigger de Firestore `email-sent`.

## 5. Tablas

Todas en Postgres, en `analytics`. Migración `047_alertas_por_correo.sql`.

```sql
-- Qué quiere cada empresa. Una fila por empresa; sin fila = los valores por defecto.
alert_email_settings (
  entity_id        PK,
  enabled          BOOLEAN   DEFAULT TRUE,
  digest_hour      SMALLINT  DEFAULT 8,          -- 6..10, hora local de la empresa
  rules_off        TEXT[]    DEFAULT '{}',       -- reglas apagadas
  to_supervisors   BOOLEAN   DEFAULT TRUE,
  extra_recipients TEXT[]    DEFAULT '{}',       -- gestoría, encargado sin panel; reciben como admin
  updated_by, updated_at
)

-- Momentos de comprobación del día, escritos por el cierre diario.
alert_checks (
  id, entity_id, branch_id, rule, check_at TIMESTAMPTZ, seq SMALLINT,  -- seq 1|2: la segunda confirma
  checked_at, result TEXT,          -- fired | clear | skipped
  UNIQUE (entity_id, branch_id, rule, check_at)
)
INDEX (check_at) WHERE checked_at IS NULL

-- Lo que se ha avisado: dedupe, rearme y «qué se te ha mandado» en los ajustes.
alert_sent (
  id, entity_id, branch_id, rule, alert_id, severity, channel TEXT,  -- immediate | digest
  recipient_kind TEXT,   -- owner | admin | supervisor | extra
  recipient TEXT,        -- correo en minúsculas
  employee_id, uid,
  day DATE,              -- día local de la empresa
  outbox_id, created_at
)
INDEX (entity_id, day DESC); INDEX (entity_id, alert_id, created_at DESC)

-- Cola de envío.
email_outbox (
  id, entity_id, kind TEXT, recipient TEXT, language TEXT,
  template_type TEXT, payload JSONB,     -- lo que la plantilla pinta; sin credenciales
  not_before TIMESTAMPTZ, attempts SMALLINT DEFAULT 0, last_error TEXT,
  sent_at, email_message_id, created_at
)
INDEX (not_before) WHERE sent_at IS NULL
```

Y dos más que salieron al implementar (migración `047_alertas_por_correo.sql`):

```sql
-- Una fila por empresa y día cuando el resumen se ha evaluado, haya salido correo o no: impide
-- evaluarlo dos veces y dice «hoy no había nada nuevo».
alert_digest_runs (entity_id, day, ran_at, alerts, emails, detail, PK (entity_id, day))

-- La ficha de la empresa (nombre, idioma, zona horaria, billing_email), para el correo.
dim_entities (entity_id PK, name, language, timezone, billing_email, active)
```

`alert_sent` y `alert_digest_runs` se conservan **90 días**; `alert_checks` y `email_outbox`,
30. Lo purga el planificador a las 02:15 UTC.

**Dedupe:** una inmediata se manda si no hay fila en `alert_sent` con el mismo
`(entity_id, branch_id, rule, day)`. En el resumen, por destinatario y nunca dos veces el
mismo día: los **hechos de ayer** (`untracked_high`, `late_high`) entran cada día que se dan,
porque cada día es un hecho nuevo; el resto (`tasks_overdue`, `availability_low`,
`access_not_delivered`, `week_coverage_low`, `cost_rising`, `rate_missing`, `exits_high`)
entra el día que aparece, cuando sube de gravedad, y después solo el lunes mientras siga
viva (`entersDigest`, `digest.ts`). `late_high` del resumen se calcula sobre el **ayer** de
`operational_daily`, no sobre el día en curso.

## 6. Ajustes en el panel

**Dónde:** en **Herramientas**, el menú del panel donde ya están el asistente y la firma
(lo ven owner y admin; «Preferencias» solo el propietario). Una entrada nueva, **Alertas**,
que abre un **modal con las casillas**: el cliente decide qué le llega. Jose, 2026-10-29:
«que sea el cliente quien decida; puede ir en Herramientas, una nueva sección de alertas, y
que se abra un modal con los checks». Es un ajuste de la empresa, no de cada persona: lo que
marca un admin vale para todos los que reciben el correo. (Antes decía «ajustes de la
empresa, sección Avisos por correo»; el sitio cambia, el contenido no.)

**Qué, en el modal:** el interruptor general, la hora del resumen, y las casillas, una por
alerta, agrupadas en «resumen de la mañana» y «pendientes de decisión» (§12: solicitudes,
incidencias, firma). El bloque «ahora mismo» (nadie en el centro, fichaje bajo, tareas sin
empezar) entra con la fase 3: hasta que esos correos existan, su casilla no se enseña. El
catálogo lo da el servidor (`ALERT_EMAIL_GROUPS`), no el panel. Cada casilla con el nombre que enseña el
panel y una línea de qué avisa, sin mecánica interna. Lo de supervisores y direcciones
extra **no se enseña**: quedó sin efecto el 28-oct (§2). «Últimos avisos enviados», de
`alert_sent`, en el mismo modal o en una segunda pestaña, para cuando alguien diga que no
le llegó.

**Por defecto:** encendido, a las 8:00, todas las casillas marcadas. Nadie configura nada
para empezar a recibirlo. El administrador desmarca lo que no quiere.

**Lo que no se configura:** los umbrales (son los de ADR-007, en `THRESHOLDS`), la
confirmación de 10 minutos, la ventana nocturna, el lunes de las lentas. Fijo para que el
cliente no tenga que pensar.

**API (hecha el 2026-10-29, `feat/alertas-pendientes`):** `GET /api/analytics/panel/alert-emails?entityId=…`
devuelve `{ settings: { enabled, digestHour, rulesOff }, groups, digestHours }`; `PUT` con
`{ entityId, enabled?, digestHour?, rulesOff? }` guarda (una regla desconocida es 400); `GET
…/alert-emails/sent` da los últimos 100 avisos con si salieron. Las tres con
`requireEntityAccess` (owner o admin). El panel lo llama por el proxy de siempre.

## 7. Prerrequisitos: el espejo tiene que ser verdad

Las alertas leen `checklogs_raw`. Una inmediata que diga «nadie en el centro» a las 9:15
cuando hay dos personas fichadas que el espejo perdió es exactamente el aviso que enseña a
ignorar la lista entera. La red de la conciliación de los :00 y :30 (TDR-004) llega tarde
para un correo de 5 minutos. Se arregla **donde se pierde**, no con una segunda lectura:

1. **El trigger reintenta.** `onChecklogSync` hoy captura el error y lo anota. Pasa a
   relanzarlo con `retry: true` en la definición de la función: Functions lo reintenta con
   espera creciente hasta que el contenedor responde. El upsert de `checklogs_raw` ya es
   idempotente, así que repetir no duplica. Un cambio de cinco líneas en `firebase_sdk`, en
   este repo.
2. **`freshness` en el correo.** Si la última conciliación de la empresa dejó `missing > 0`, o
   el trigger lleva más de 5 minutos sin escribir nada de una empresa con turno en marcha, las
   inmediatas de esa empresa se **saltan** (`result = skipped`) y se anota. No se envía lo que
   no se sabe.
3. **Índice** `checklogs_raw (entity_id, timestamp)`, pendiente de analisis-a-escala.

Con esto `checklogs_raw` es la única fuente, también para lo inmediato. Si un fichaje no llegó
al espejo, el fallo es del espejo y se ve en su cola; no se tapa.

## 8. Textos

El hecho medible, como la alerta del panel: «Obra Norte: a las 9:10 no había nadie fichado de
8 previstos». Nunca «faltan trabajadores», nunca la causa. Los `params` de cada regla ya
traen las cifras; las claves de texto son las de `operationalDashboard.alerts` del panel, para
que el correo y la pantalla digan lo mismo.

- Plantillas `ALERTS_IMMEDIATE` y `ALERTS_DIGEST` en `emails_template`, con respaldo en el
  código y subidas por el script `email-templates`.
- Idioma del destinatario: ficha de la persona → empresa → inglés.
- Cada alerta enlaza a su pantalla (`target`) con el `entityId` y el `branchId` en la URL.
- Pie fijo: «Recibes esto porque eres administrador / supervisor de X en CheckBiz360.
  Ajustes → Avisos por correo». Para las direcciones extra, el mismo pie sin el enlace.

## 9. Escala, en números

| | 10 empleados | 1000 empleados, 80 centros |
|---|---|---|
| Comprobaciones al día | 3-6 | ~250, repartidas por turnos |
| Coste de cada una | 1 consulta de hoy, 1 sucursal | igual |
| Resumen | 5 consultas sobre datos cerrados | igual, una vez; reparto en memoria |
| Correos a las 8:00 | 1-2 | ~100, en cola, 20 min |
| Lecturas a Firestore | 0 | 0 |

Lo único que crece con el tamaño es el número de correos, que es lo único que de verdad tiene
que crecer.

## 10. Piezas

| Pieza | Dónde |
|---|---|
| Migración 047: cuatro tablas, `email` en `dim_employees`, `dim_panel_users`, `dim_responsibilities` | `migrations/` |
| Espejo de asientos y responsabilidades (y correo de Auth por uid nuevo) | `analytics/application/SyncDimensions.ts` |
| Momentos de comprobación escritos en el cierre diario | `analytics/application/operational/CloseDue.ts` |
| Job «comprobaciones» (cada 5 min), job «resumen» (cada hora, empresas cuya hora ha llegado), «despachador» (cada minuto), purga | `analytics/jobs/scheduler.ts` + `application/alerts/` |
| `evaluateAlerts` sin tope; `late_high` de ayer para el resumen | `analytics/application/alerts/rules.ts`, `BuildPanelAlerts.ts` |
| Reparto por destinatario y armado del correo | `analytics/application/alerts/Deliver*.ts` |
| Plantillas `ALERTS_IMMEDIATE`, `ALERTS_DIGEST` | `shared` + script `email-templates` |
| `retry: true` y relanzar el error en `onChecklogSync` | `firebase_sdk/src/sync/onChecklogSync.ts` |
| Ajustes y historial: API | `analytics/interfaces/panel.router.ts` |
| Ajustes y historial: pantalla | panel, Herramientas → Alertas (modal con casillas) |

## 11. Fases

1. **Espejo y suelo** — retry del trigger, índice, migración 047, espejo de asientos y
   responsabilidades. Sin correos todavía. Se verifica en dev que los espejos cuadran con
   Firestore.
2. **Resumen de la mañana** — el camino largo entero: cálculo sin tope, reparto, cola,
   despachador, plantilla, `email_message`. A owner y admin primero; supervisores en la misma
   fase cuando el reparto esté probado. Es el que más gente ve y el menos arriesgado.
3. **Inmediatas** — momentos de comprobación en el cierre, job de 5 minutos, confirmación de
   dos tics, guarda de `freshness`. Primero con una empresa de dev, con la hora de un turno
   real.
3b. **Pendientes de decisión** (§12) — solicitudes, incidencias y firma de documentos en el
   resumen; «documento firmado» inmediato. No depende de la fase 3: reutiliza el resumen y
   el despachador que ya están en producción.
4. **Ajustes en el panel** — API y el modal de Herramientas → Alertas (§6). Hasta aquí, todo
   por defecto. Va **detrás de 3b**, para que el modal nazca ya con las casillas de pendientes.

Cada fase que sube a staging y necesita algo fuera del código (plantillas, migración, índice)
va el mismo día a `DOCS/deployment-prod/proximo-pase-back.md`.

## 12. Pendientes de decisión (fase 3b)

**Jose, 2026-10-29:** «identificar los procesos que requieran intervención de administración y
enviar emails de notificación: solicitudes, contactos, incidencias, firma de documentos». Y,
sobre el «no por email» de las solicitudes del 22-oct ([vacaciones](../vacaciones/README.md)):
«ahora sí por email, ya que tenemos el módulo hecho: solo hay que ampliar las alertas a owner y
administradores». Alcance cerrado por Jose; lo que no está aquí (fichajes manuales por aprobar,
tareas sin validar, inventario) **no entra** «por el momento».

### El principio

> Las alertas dicen lo que pasó; los pendientes dicen lo que alguien espera que decidas. Van en
> el **mismo correo**, con la misma caja, el mismo pie y los mismos destinatarios (owner y
> admin, §2). Ni una plantilla por proceso, ni un correo por solicitud.

«Contacto» es la sección del panel donde la plantilla escribe desde la app: sus dos pestañas son
las incidencias y las solicitudes. No hay un «contacto» aparte.

### Qué entra y cuándo

| Pendiente | Qué dice la caja | Ritmo | Lleva a |
|---|---|---|---|
| `requests_pending` Solicitudes por decidir | «3 solicitudes de vacaciones o permisos esperan respuesta: Ana, Luis, Eva. La más antigua es de hace 4 días.» | resumen | Contacto → Solicitudes |
| `request_soon` Solicitud que empieza pronto | «Ana pide vacaciones desde pasado mañana y sigue sin respuesta» | **inmediata**, al quedar a menos de 48 h del inicio; 1 por solicitud | Contacto → Solicitudes |
| `issues_open` Incidencias abiertas | «5 incidencias abiertas por la plantilla siguen en revisión. La más antigua es de hace 6 días.» | resumen | Contacto → Incidencias |
| `issue_opened` Incidencia nueva de una persona | «Luis ha abierto una incidencia de configuración en Obra Norte» | **inmediata**, al abrirse; solo las que abre un trabajador, no las del sanitizer | la incidencia |
| `docs_unsigned` Documento sin firmar | «Protocolo: faltan 4 de 12 personas por firmar (Ana, Eva, Luis y 1 más). Enviado hace 5 días.» Una caja por documento; con 12 o más, agrupadas | resumen, **solo dos veces**: a los 2 días de enviarlo y 7 días después (día 9), en rojo la segunda (Jose, 2026-10-29) | la ficha del documento |
| `doc_signed` Documento firmado | «Ana ha firmado «Nómina de octubre» a las 10:42 con huella o cara desde su móvil.» Si solo pulsó, «ha confirmado la lectura…, sin firma» | **inmediata**, en cada acuse | la ficha del documento |

Los dos de firma solo existen para documentos **con acuse de recibo activado**
(`requiresAcknowledgement`), que son los que se firman: cualquier acuse se puede firmar con el
móvil. Un acuse «pulsado» sin firma también cierra el pendiente y también avisa, diciendo que
fue sin firma: es lo observado. «No conforme» no existe todavía en el acuse; cuando exista, el
texto lo dirá.

Quién debe firmar sale del espejo, como lo resuelve el documental al avisar: la persona
(`single_employee`), las responsabilidades de la sucursal con rol visible más el owner
operativo (`branch_employees`) o toda la plantilla (`entity_employees`); en los tres, sin las
fichas `fired`, `inactive` o `pending`.

Las incidencias que crea el cierre automático (`userId: "system"`) quedan **fuera de los dos**,
resumen e inmediato: una jornada sin salida crea una por persona y día, y ya salen como
«Jornadas sin cerrar». Contarlas otra vez sería avisar dos veces del mismo hecho.

### Reglas que ya valen y aquí se mantienen

- **Sin nada nuevo, no hay correo** (§3): un pendiente entra en el resumen el día que aparece y,
  después, cada día mientras siga abierto **si cambia** (una solicitud más, un firmante más) o
  cada lunes si no cambia. Se hace con el `id` de la alerta: el de solicitudes e incidencias
  lleva una huella del conjunto; si cambia, es nuevo. El documento sin firmar no sigue esta regla: sale el día 2 y el día 9 y nunca más. Una solicitud que lleva tres semanas sin respuesta sale el lunes con
  «desde hace 21 días», no veinte mañanas seguidas.
- **Nunca entre las 22:00 y las 6:00** locales: lo inmediato de la noche espera al resumen.
- **Nombrar lo observado**: «sigue sin respuesta», nunca «se te ha olvidado».
- Apagado por regla en `rules_off` con estas seis claves, como las demás. El interruptor
  general de la empresa manda sobre todo.

### De dónde salen los datos

Las alertas de §1 se calculan desde Postgres (§4). Los pendientes **no están espejados**:
`absence_requests` (Firestore, por empresa), `issues` (colección raíz, `entityId` +
`state = in_review`) y los acuses del documental (`documents/{id}/acks`). Para el resumen, por
empresa, son **tres consultas filtradas** —cada una devuelve decenas, no miles— y se hacen en
el job del resumen justo antes de armar el correo; no justifican un espejo. El coste a vigilar
es `docs_unsigned`: hay que saber cuántos deben firmar y cuántos han firmado por documento. Se
calcula solo para documentos con acuse de los **últimos 90 días** y el documental expone el
recuento (`acknowledged / expected`) en lugar de que analytics recorra los acks; si al medirlo
pesa, se espeja el recuento y no los acks.

Las inmediatas no se sondean (§4.1): nacen donde ocurre el hecho.

| Hecho | Dónde ocurre | Quién encola |
|---|---|---|
| Acuse firmado | `documents` · `AcknowledgeDocument` tras guardar el acuse | el documental llama al S2S de analytics, que encola en `email_outbox` (`alerts_immediate`) para los owner/admin de la empresa |
| Incidencia abierta por una persona | `onCreateIssues` (Firebase, mientras no se porte) | el trigger llama al mismo S2S; `fromRole` distingue persona de sanitizer |
| Solicitud a menos de 48 h | nadie la «abre»: es el paso del tiempo | job «solicitudes próximas» de analytics, cada hora a :05: una pasada por empresa activa sobre `pending` con `hoy ≤ startDate ≤ hoy + 2`; avisa una vez por solicitud |

El S2S de analytics es una ruta nueva y pequeña, `POST /api/analytics/alerts/pending` (clave
S2S), que recibe el hecho (`doc_signed` o `issue_opened`, con sus ids), lo convierte en alerta,
resuelve destinatarios desde `dim_panel_users` y encola. Se llama con `reportPendingAlert` de
shared, que nunca lanza. Un aviso inmediato no se repite: `alert_sent` con `channel =
'immediate'` y el mismo `id` lo corta. De noche (22–6) se encola para la hora del resumen.
Si analytics no responde, el documental y el trigger **no fallan**: el acuse y la incidencia ya
están guardados, y el pendiente saldrá en el resumen de la mañana.

### Textos y plantilla

Misma plantilla `ALERTS_DIGEST` / `ALERTS_IMMEDIATE`; las seis claves nuevas se añaden a
`ALERT_COPY` (es/en) y, cuando el panel las enseñe, a `operationalDashboard.alerts`. `target`
gana `contact_requests`, `contact_issues`, `issue` y `document` (con el id en la ruta).
Gravedad: `request_soon` e `issue_opened`, `high`; solicitudes, incidencias y documentos que
llevan 7 días o más esperando, `high`; el resto, `medium`.

`ALERTS_IMMEDIATE` deja de ser de centro: la entrada, el botón y el final del asunto los pone
el código (`{{intro}}`, `{{button}}`, `{{where}}`, función `immediateParts`), porque «documento
firmado» no tiene centro ni «ver quién está». Como cambia la plantilla, hay que subirla con
`email-templates --apply --replace` en dev y en prod; ningún inmediato salía aún, así que no
rompe nada en vuelo.

### Fuera de esta fase

- Avisar a la persona (le llega push cuando se decide su solicitud; eso no cambia).
- Recordatorio al trabajador que no firma: es del documental, y es push.
- Las de fichaje manual, tareas sin validar e inventario: Jose, 2026-10-29, «limítate a lo que
  te pedí por el momento».

## Fuera de alcance

- Push a supervisores por «nadie en el centro» de su sucursal: es el `team_missing_checkin`
  de [presencia, fase 3](../presencia/README.md#avisos-a-supervisores-fase-3). Cuando exista,
  el supervisor recibirá push y correo; no se duplica aquí.
- Umbrales por empresa. Los de ADR-007 valen para todas; se abre si alguien lo pide con un
  caso.
- Reglas nuevas. Lo que no está en el panel no sale por correo: si hace falta una alerta
  nueva, nace en `rules.ts` y la ven el panel, el asistente y el correo a la vez. Los
  pendientes de decisión (§12) no son reglas: son colas que el panel ya enseña (Contacto, la
  ficha del documento) y el correo solo las recuerda.
- Repartir con Cloud Tasks. El diseño ya tiene la unidad de trabajo (sucursal, empresa) para
  que el cambio sea de transporte, no de lógica.

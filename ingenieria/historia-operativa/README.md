# Historia operativa — la memoria de la plataforma para los modelos de mañana · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** transversal — espejo Postgres de `analytics` × `salud` (copias) × BigQuery
**Fecha de inicio:** 2026-11-09
**Estado:** Fase 3 y `mirror_versions` **EN PRODUCCIÓN desde el 2026-11-17** (hotfix #293; pase §73 y §75). **20-nov:** las 5 empresas reales tienen sector y además nicho de actividad (`entities.niche` = {id, name, sector}, catálogo en `niches/{id}`); se agrupa por `niche.id`, nunca por nombre. El sector llega a `dim_entities` por el sync de la hora; el nicho llega al espejo con la migración 070 (`dim_entities.niche_id` y `dim_niches`, EN PRODUCCIÓN el 20-nov, hotfix #308, pase §84). **Desde el 20-nov el alta de empresa pide el nicho, obligatorio** (panel #168, API #304): toda empresa nueva entra en la historia ya etiquetada. Antes, EN STAGING desde el 2026-11-16 (Jose, 16-nov: «puedes ir haciendo las migraciones y escritura de datos»): migración 066, `Entity.sector`, `calendar_day_versions`, script `sector-empresa` (develop `040fe42` #282, staging `7273b2c` #283; pase §73). **17-nov, Jose: «solo estamos recogiendo datos, no metemos nada todavía a BigQuery, todo se queda en Postgres por el momento».** La foto a BigQuery queda escrita y apagada; en su lugar, `mirror_versions` (migración 067, pase §75): cada versión de las filas que el espejo pisa, dentro de Postgres (§Lo que se construyó). **Fase 1 (la foto) EN STAGING desde el 2026-11-17 en código, APARCADA** (`salud/src/foto.ts`, develop `926a51c` #284, staging `f637d26` #285; pase §74), **desactivada** hasta que Jose cree bucket, dataset y cuenta con `salud/scripts/historia-gcp.sh` (a Claude no le dejaron crear recursos en Google Cloud). Fase 2 (hechos) sin empezar.
**Autor:** Jose Acevedo (diseño conversado con Claude el 08 y 09-nov-2026)

---

## De dónde sale

Jose, 08-nov-2026, a partir de una propuesta externa de «modelos propios de EncodeBiz para la
operativa de campo»: «no tenía planeado hacer esto hasta los 1.000 empleados, pero sí quiero ir
allanando el problema y decisiones y nutriendo la BD». Y acotándolo: «exportaciones masivas a la
semana o gradualmente, pero en ningún caso interfiriendo en la plataforma core por el momento;
sobre todo definiendo la estructura de datos». Y la fuente: «los perfiles de empleado y sucursal,
tareas, tiempos, fichajes, comportamientos, eso sí lo tenemos y es justamente el punto de partida».

La propuesta externa tenía una pregunta buena, la única que importa ahora: **¿conservamos el
historial de los cambios o solo el estado final?** Este documento la contesta y decide cómo
dejar de perder lo que hoy se pierde, sin construir ningún modelo.

## El modelo, en cinco líneas

1. **La fuente es el espejo de Postgres**, no Firestore. Es lo que ya lee el panel, ya está
   normalizado y leerlo no cuesta dinero. Lo que no esté en el espejo no entra en la historia:
   la forma de «nutrir la BD» es bajar al espejo lo que falte, que además es la dirección que ya
   lleva la plataforma (Postgres primero en el panel).
2. **Una foto cada noche, desde `salud`, a las 02:30**, en el mismo momento y con el mismo rol
   de solo lectura con que ya hace la copia de seguridad. No hay triggers, no hay código nuevo
   en ningún servicio, no hay lecturas nuevas de Firestore. Es lo más cerca de «no tocar el
   núcleo» que existe sin dejar de medir.
3. **La foto va a un bucket europeo y de ahí a BigQuery**, en dos capas: lo crudo tal cual llega,
   que no se toca nunca, y las tablas de hechos que se derivan de lo crudo y se pueden rehacer
   enteras el día que la estructura resulte estar mal.
4. **Sin nombres.** La foto sale ya sin nombres, correos, teléfonos, textos libres ni
   coordenadas. Los identificadores son opacos y la llave que los une a personas se queda en
   Postgres. Es la misma regla que Merlín.
5. **Diaria, no semanal.** Entre dos fotos se pierde lo que pasa en medio; a la semana una tarea
   que se crea el lunes, se mueve el miércoles y se cierra el viernes aparece una vez y cerrada.
   Al día, la diferencia entre ayer y hoy ya es un cambio registrado. Lo intradía se pierde igual
   con cualquier foto; para eso está, el día que se quiera, el historial de la tarea (§Lo que ya
   es histórico).

## Lo que ya tenemos, visto de cerca (espejo `encodebiz_analytics`, 70 tablas)

Lo que Jose llamó el punto de partida está, y parte ya es histórico de verdad, no una foto:

| Qué | Tabla(s) | Es historia ya? |
|---|---|---|
| Empresas | `dim_entities` (idioma, zona horaria, activa) | No: estado actual |
| Centros | `dim_branches` (ciudad, país, zona horaria, horario, geolocalización 007) | No: estado actual |
| Personas | `dim_employees` (puesto, rol, estado, centros) | No: estado actual |
| **Plantilla en el tiempo** | `employee_status_events` (cada cambio de estado fechado), `headcount_daily` (activos por centro y día) | **Sí** (028) |
| **Puesto y precio por hora** | `dim_responsibilities` + `responsibility_events` (cada cambio fechado) | **Sí** (050) |
| Calendarios | `dim_calendars` (horario semanal, festivos, **ausencias** del empleado, config), `dim_calendar_days` | No: estado actual, las ausencias como lista |
| **Fichajes** | `checklogs_raw`: hora real y ajustada, `schedule_applied` (el horario que regía en ese momento), dispositivo, remoto, precio congelado, **`task_id`** (050) | **Sí**: cada fichaje es un evento |
| Jornadas calculadas | `employee_daily_reports` (ciclos, descansos, netos), `daily_reports`, `operational_daily` | Sí por construcción (una fila por persona y día) |
| **Comportamiento** | `pattern_snapshots`: hora media de entrada y salida, desviación, fiabilidad, puntuaciones heurísticas, por fecha | **Sí** (fechado) |
| Tareas | `tasks_raw`: planificado, inicio, fin, pausas, quién, validación, cliente y contrato | No: estado final, se sobreescribe |
| **Historial de la tarea** | `task_events_raw` (050): quién entró y salió, inicio, pausa, cierre, validación, con actor y hora | **Sí**. En staging desde el 04-nov; **en prod pendiente** (pase §34) |
| Valoraciones | `task_ratings_raw` | Sí |
| Material | `item_movements_raw`, `unit_*_raw` (inventario) | Sí |
| Cartera | `dim_customers`, `customer_contracts`, `contract_*` | Estado + eventos |
| Dirección | `direccion_snapshot_daily`, `backoffice_snapshot_daily` | Sí, agregados |

Dos correcciones a lo que se dijo en la conversación del 08-nov: **el historial de la tarea sí
baja a Postgres** desde la migración 050 (`activity` de Firestore → `task_events_raw`), y **las
ausencias sí están**, dentro de `dim_calendars.absences`. Lo que sigue sin estar es lo de abajo.

## Lo que falta en el espejo, y por tanto en la historia

**Revisado el 16-nov-2026 con el código delante.** De las cuatro piezas, dos ya estaban (mal
contadas el 09-nov) y dos se hicieron ese día; queda una:

- **Incidencias: ya eran historia.** La incidencia de la tarea (TDR-009, migración 064) deja
  actividad `incident_reported` / `incident_resolved` en Firestore y cada actividad baja a
  `task_events_raw`. El estado va en `tasks_raw.incident_*`; la secuencia completa, en los eventos.
- **El plan confirmado: ya bajaba, pero se pisaba. Hecho (066).** Los turnos cargados y los
  cuadrantes confirmados escriben por `PUT /calendar/days`, y el sync los espeja en
  `dim_calendar_days` con `ON CONFLICT … DO UPDATE`: el plan original desaparecía al retocarlo.
  Desde la 066, `calendar_day_versions` guarda una fila por cada versión del día; la primera de
  cada (persona, día) es el plan antes de que lo tocara nadie. Semilla con lo que había.
- **El sector de la empresa. Hecho (066).** `Entity.sector` con lista corta (`limpieza`, `sad`,
  `oficina`, `construccion`, `eventos`, `mantenimiento`, `otros`), `dim_entities.sector`, y el
  script `sector-empresa` para rellenarlo a mano. Desde el 20-nov el alta del panel pide el nicho, obligatorio, y con él el sector (73.5).
- **El tipo de tarea: PENDIENTE**, decisión de Jose (§Decisiones).

**La cartera de clientes ya está en Postgres** (Jose, 16-nov: «el círculo completo se cierra con
clientes y no sé si eso se está espejando»): clientes en `dim_customers`, contratos en
`customer_contracts` con sus `contract_events`, gastos en `customer_expenses`, y la tarea lleva
`customer_id`, `customer_site_id` y `contract_id`. Lo que se queda solo en Firestore son los
sitios del cliente (direcciones) y los documentos, que no hacen falta para la historia.

Lo escrito el 09-nov, para el registro:

1. **Incidencias.** No hay ninguna tabla. Explican por qué una jornada o una tarea se desvía;
   sin ellas el modelo aprende la desviación y no la causa. Es un espejo nuevo (`incidents_raw`),
   crudo, con el mismo patrón que las tareas.
2. **El plan antes de que lo toque nadie.** Los turnos cargados y los cuadrantes confirmados
   (proponer/confirmar cuadrante del conector) no tienen espejo. Hay que localizar dónde quedan en
   Firestore (hay `cuadrante_presets`, que son plantillas, no el plan) y bajar «lo que se
   confirmó, cuándo y para quién». Las tareas conservan `scheduledStartAt` original en
   `task_events_raw` cuando se mueven, así que para «Por tareas» ya está; falta para «Por turnos».
3. **El tipo de tarea.** La tarea tiene título libre, descripción, cliente y contrato, pero no
   un tipo. Sin tipo no se puede comparar limpiezas con limpiezas, y el título no sirve: es
   texto libre y además puede llevar nombres. Decisión abierta (§Decisiones de Jose).
4. **El sector de la empresa.** `Entity.type` es la forma jurídica (`company`, `autonomous`,
   `organization`, `event`), no el sector. Para modelos por limpieza, SAD, oficina, eventos o
   construcción hace falta `entities.sector`, rellenado a mano para las empresas que hay y pedido
   en el alta a partir de ahora, y espejado en `dim_entities`.

Ninguna de las cuatro bloquea la foto. La foto empieza con lo que hay.

## La foto: cómo se hace y por qué así

**Dónde.** En `salud/src/copias.ts`, como segundo paso de la copia nocturna de las 02:30. Ya
tiene el rol `copias` (`pg_read_all_data`, migración 057), ya corre a esa hora y ya sube a Google.
Si la foto falla, la copia no se ve afectada, y `salud` lo cuenta en su informe diario como cuenta
la copia.

**Qué saca.** Un `\copy (SELECT …) TO STDOUT` por tabla, en JSON por líneas comprimido, **con
la lista de columnas escrita en el SELECT**, nunca `*`: ahí es donde se quitan los nombres
(§Sin nombres). Dos ritmos:

- **Tablas que solo crecen** (`checklogs_raw`, `task_events_raw`, `employee_status_events`,
  `responsibility_events`, `item_movements_raw`, `task_ratings_raw`): solo las filas con
  `synced_at` posterior a la última foto. Fotografiarlas enteras cada día multiplicaría por 365
  algo que no cambia.
- **Tablas que mutan** (`tasks_raw`, `dim_*`, `dim_calendars`, `pattern_snapshots`,
  `employee_daily_reports` de los últimos 45 días): enteras cada día. Son pequeñas (miles de
  filas) y la comparación entre fotos es precisamente la historia que no teníamos.

**A dónde.** Bucket nuevo `encodebiz-services-historia`, en la UE, con ruta
`<tabla>/dt=AAAA-MM-DD/parte.jsonl.gz`. **No** al bucket de copias: aquel es cifrado, con
retención bloqueada y solo lo abre la clave privada del portátil; este es legible por BigQuery,
sin cifrar porque no lleva nombres, y con ciclo de vida de 30 días porque BigQuery es el almacén
de largo plazo. La cuenta `copias-servidor` recibe `objectCreator` también sobre este bucket.

**Por qué no desde la copia cifrada.** Habría sido redondo (restaurar la copia en una máquina
aparte y de paso comprobar que restaura), pero exige poner la clave privada en otra máquina, y la
decisión del 07-nov fue que esa clave solo vive en el portátil. No se deshace una decisión de
seguridad para ahorrar un paso.

**Por qué no desde Firestore.** Cada exportación relee la colección entera y cobra una lectura
por documento; con los fichajes serían millones de lecturas al mes a mil empleados. Y Jose no
quiere nada nuevo escuchando al núcleo. La extensión «Stream Firestore to BigQuery» queda como
mejora futura si algún día se quiere el historial al minuto: se añade encima y lo acumulado sigue
valiendo.

## Lo que se construyó el 17-nov (Fase 1) y en qué se aparta del diseño

- **La carga la hace `salud`, no Data Transfer.** Tras subir cada fichero lanza un trabajo de carga de
  BigQuery por la API (`crudo_<tabla>$AAAAMMDD`, `WRITE_TRUNCATE`, esquema autodetectado con
  adición de campos): una pieza menos que configurar fuera del código y la misma cuenta para todo.
- **Lo JSON sale como texto** (`::text`), no como objeto: BigQuery no tiene que adivinar un esquema
  distinto cada día; se consulta con las funciones JSON.
- **21 tablas**, no «todas»: las de la cartera (`dim_customers`, `customer_contracts`, `contract_events`,
  `customer_expenses`) y el inventario (`item_movements_raw`) entran; las de ventas, backoffice,
  correo, alertas y salud no son historia operativa y no salen.
- **Incrementales** por su marca: `checklogs_raw` (`GREATEST(synced_at, updated_at)`: un fichaje
  ajustado vuelve a salir), `task_events_raw`, `employee_status_events`, `responsibility_events`,
  `contract_events`, `task_ratings_raw`, `item_movements_raw`. La marca avanza solo después de
  cargar: un fallo repite, nunca pierde. Las demás, enteras; `employee_daily_reports` solo 45 días.
- **Lo que se limpia dentro del JSON**: `absences` sin `note`, `shifts` sin `title`, el `payload` de
  los eventos de tarea por lista blanca (`employeeId`, `fromStatus`, `toStatus`), los valores de
  `contract_events` a NULL cuando el campo es texto libre. `foto.test.ts` recorre cada SELECT
  buscando las columnas prohibidas y falla si una se cuela.

## 17-nov: todo en Postgres, por ahora (`mirror_versions`, migración 067)

Jose aparcó BigQuery el mismo día: «solo estamos recogiendo datos». Lo que la foto iba a conservar
fuera se conserva dentro, con el mismo criterio de «la primera versión es cómo estaba cuando
empezamos a mirar»:

- **Una tabla, `mirror_versions`**: tabla de origen, clave de la fila, empresa, la fila entera como
  JSON y su hash, y cuándo la vio el espejo. Solo inserción. La purga la borra sola (tiene
  `entity_id`).
- **Seis tablas entran**, las que el espejo pisa y no tenían historial aparte: `dim_entities`,
  `dim_branches`, `dim_employees`, `dim_calendars` (horario semanal, festivos, ausencias, modo),
  `dim_customers` y `tasks_raw` (fechas planificadas, asignados, estado, cliente, contrato…). Las
  demás ya eran historia: `employee_status_events`, `responsibility_events`, `contract_events`,
  `task_events_raw`, `calendar_day_versions`, `checklogs_raw`, `pattern_snapshots`.
- **Cuándo se guarda**: tras cada escritura del espejo (`packages/shared/src/mirror/rowVersions.ts`),
  una sentencia que compara el hash de la fila con el de su última versión; `synced_at` y
  `updated_at` quedan fuera del hash (y `source_updated_at` en empleados), o cada sync sería una
  versión. En `analytics` una sentencia por empresa tras el sync; en `tasks` y `customers`, por fila
  tras su upsert.
- **Dentro de Postgres van los nombres**, como en las tablas de origen: la regla «sin nombres» es
  para lo que salga fuera (la foto), y la foto está apagada. El día que se encienda, `mirror_versions`
  se añade a su lista con el JSON limpio igual que las demás.

## 20-nov: el nicho, y para qué se usa ya (migración 070)

El nicho se hizo para este frente (Jose, 20-nov): el sector parte la historia en siete trozos y
eso es grueso; «limpieza de oficinas» y «limpieza industrial» no planifican igual. Desde el 20-nov
las empresas reales llevan `entities.niche` = {id, name, sector} con catálogo en `niches/{id}`.
Lo que se hace con él, de lo que sirve hoy a lo que servirá con volumen:

1. **Está en la historia (hoy).** `dim_entities.niche_id` y el catálogo entero en `dim_niches`,
   por el sync de la hora. Al ser una columna de `dim_entities`, cada cambio de nicho queda en
   `mirror_versions` sin más código. `dim_niches` guarda también los pendientes, rechazados y
   fusionados, porque la historia anterior a una fusión sigue con el id viejo y `merged_into` es
   lo que la une al nuevo. **Se agrupa por `niche_id`, nunca por el nombre.**
2. **Merlin escribe para esa actividad (hoy).** El relato del panel recibe una línea
   «Actividad: Ayuda a domicilio (sector sad)» que Merlin lee de la ficha, no del cliente. La
   regla: sirve para hablar como habla el gestor (usuarios y domicilios en SAD) y para no tomar
   por raro lo que es la forma de trabajar del sector; **nunca es una causa ni una comparación**,
   porque no tiene datos de otras empresas. Prompt `panel-v5`. Los relatos de centro y de
   persona todavía no la llevan.
3. **Valores de referencia por nicho (cuando haya con qué).** Percentiles de duración de tarea,
   cobertura de fichaje o retrasos por nicho, calculados en Postgres. Solo se enseñan con un
   mínimo de **cinco empresas** en el nicho: con una, «la media del nicho» es la empresa de otro
   cliente con otro nombre. Hoy hay una empresa por nicho, así que no se construye todavía.
4. **El modelo propio (cuando haya volumen).** El nicho es la clave de cohorte: un modelo de
   duraciones se entrena por nicho o lo lleva como variable.

## BigQuery: dos capas (APARCADO el 17-nov; la foto existe y está apagada)

**Dataset `historia`, región EU** (multirregión; Firestore está en `eur3` y las copias en EU).
Un dataset por entorno: el de dev en `dev-encodebiz` con la foto de `encodebiz_staging`, el de
prod en `encodebiz-services`.

**Capa 1, `crudo`.** Una tabla nativa por tabla del espejo, particionada por `dt` (día de la
foto), cargada cada mañana por **BigQuery Data Transfer Service** desde el bucket (transferencia
de Cloud Storage programada, gestionada por Google, sin código). Nativa y no externa a
propósito: hay que poder borrar por `entity_id` (§Purga) y una tabla externa no se puede borrar
por filas. Nunca se actualiza ni se borra salvo por purga de empresa. Si la capa 2 está mal, se
rehace desde aquí.

**Capa 2, `hechos`.** Tablas que se recalculan cada día con consultas programadas de BigQuery,
una fila por cosa que ocurre, todas con las mismas claves (`entity_id`, `branch_id`,
`employee_id`, `dt`) y el mismo contexto (día de la semana, festivo del ámbito, modo de horario de
la persona ese día, sector de la empresa cuando exista):

- `hechos_jornada`: por persona y día, horario previsto (de `schedule_applied` del primer
  fichaje) frente a real, minutos netos, descansos, retraso, cierre fabricado o no, ausencia
  declarada.
- `hechos_tarea`: por tarea cerrada o cancelada, planificado frente a real, duración, pausas,
  personas asignadas y las que realmente ficharon en ella (`checklogs_raw.task_id`), cliente y
  contrato, estado de cumplimiento, valoración.
- `hechos_cambio_tarea`: de `task_events_raw` y de la diferencia entre fotos de `tasks_raw`:
  qué cambió (fecha, personas, estado), quién y cuándo, cuánto antes del inicio previsto.
- `hechos_plantilla`: altas, bajas y cambios de puesto o precio, de `employee_status_events` y
  `responsibility_events`.
- `hechos_ausencia`: de la diferencia entre fotos de `dim_calendars.absences`.
- `hechos_comportamiento`: `pattern_snapshots` tal cual, con el contexto común.

Las dimensiones (`dim_*`) se exponen como la última foto, sin nombres. Las vistas que use
cualquiera que no sea Jose son de la capa 2.

## Sin nombres

La regla, igual que en Merlín: **el bucket y BigQuery no contienen nunca un nombre, un correo, un
teléfono, un texto libre ni una coordenada**. Los `id` son opacos y la llave está solo en Postgres.
Eso se decide en el SELECT de la foto, tabla por tabla:

- `dim_entities` sin `name`, `billing_email`; `dim_employees` sin `display_name` ni ningún
  contacto; `dim_branches` sin `name` ni calle (sí ciudad, país, zona horaria).
- `checklogs_raw` sin `user_agent`, sin coordenadas (si hace falta, distancia al centro en
  metros, calculada en el SELECT), sin `metadata_raw`.
- `tasks_raw` sin `title` ni descripción. `task_events_raw.payload` **por lista blanca** de
  claves (estados, fechas, ids), nunca entero: puede llevar notas.
- `dim_calendars.absences` solo fechas y estado, sin `note`. `task_ratings_raw` sin `comment`.

Lo que se seudonimiza así sigue siendo dato personal a efectos del RGPD (el id es reidentificable
con la llave), y por eso la purga de abajo y la frase legal siguen haciendo falta. Pero el daño de
una fuga queda en «fechas de alguien a quien no se sabe quién es».

## Lo legal, en una frase

El contrato de encargo del tratamiento (`proteccion-de-datos/`) tiene que decir que los datos
operativos se conservan seudonimizados y se usan de forma agregada para mejorar el servicio y
elaborar estadísticas. Hoy el espejo ya conserva indefinidamente lo mismo, así que la retención
no es nueva; lo nuevo es el **uso** futuro, y sin la frase no hay base para entrenar nada dentro
de un año. La redacta Jose con quien valide el texto legal. Hasta entonces la historia se acumula
y no se usa para otra cosa que lo que ya hace el panel.

Entrenar con datos de **varias empresas juntas** es lo que hace útil un modelo con cinco
empresas de 30 personas, y es exactamente lo que exige esa base. Es otro motivo para escribir la
frase ahora y entrenar después.

## Purga

Cuando se borra una empresa (herramienta de purga en prod, 05-nov) hay que borrar también su
historia: `DELETE … WHERE entity_id = …` en cada tabla de `crudo` y `hechos`, y los ficheros del
bucket caen solos por el ciclo de vida de 30 días. La herramienta de purga gana ese paso.

## Costes

Lo que cobra Google (precios de lista en la UE **de memoria, sin comprobar**; se contrastan con las páginas de precios antes de la Fase 1):

| Pieza | Precio | Hoy (~150 personas) | A 1.000 personas |
|---|---|---|---|
| Lecturas del espejo | 0 € (es nuestro Postgres, a las 02:30, mismo rol que la copia) | 0 € | 0 € |
| Bucket `historia` (30 días) | ~0,02 €/GB·mes | céntimos | céntimos |
| BigQuery almacenamiento | 10 GB gratis, luego ~0,02 €/GB·mes (la mitad pasados 90 días) | 0 € | 1 a 2 €/mes |
| BigQuery consultas | 1 TB/mes gratis | 0 € | 0 € |
| Data Transfer desde Cloud Storage | gratis | 0 € | 0 € |
| Consultas programadas | se cobran como consultas | 0 € | 0 € |

El volumen que manda es `checklogs_raw` incremental (estimado: hoy unas 600 filas al día, a mil personas
unas 4.000, un kilobyte cada una): decenas de megas al año. Las fotos enteras de tareas y
dimensiones suman del orden de un gigabyte al año hoy y unos diez a mil personas. **El coste es
el tiempo de montarlo: dos o tres días**, y se mantiene solo.

Para que las consultas sigan gratis cuando haya años: todo particionado por `dt` y las consultas
siempre con rango de fechas. Es la única disciplina.

## Fases

- **Fase 0 — Decisiones.** Este documento. Nada corre hasta que Jose lo lea.
- **Fase 1 — La foto, en dev.** Bucket y dataset en `dev-encodebiz`; paso de foto en `salud`
  con los SELECT sin nombres; transferencia programada; comprobar durante una semana que cada
  mañana hay partición nueva y que no entra ningún nombre (una consulta de control que busque
  `@` y columnas prohibidas). Se prueba en staging y **a prod va en un pase**, con el bucket, el
  permiso de la cuenta `copias-servidor` y el dataset creados por Jose o con su OK expreso.
- **Fase 2 — Los hechos.** Consultas programadas de la capa 2 y vistas. Primera consulta útil
  sin modelo alguno: por tipo de tarea y centro, duración planificada frente a mediana real,
  para el aviso «esta tarea suele durar más de lo que has puesto».
- **Fase 3 — Lo que falta en el espejo.** Sector de la empresa, tipo de tarea, incidencias,
  plan confirmado. Cada pieza, al entrar en el espejo, entra en la foto. Sin fecha: a su ritmo.
- **Después, con mil personas.** Modelos. Con lo de arriba hecho, el conjunto de entrenamiento
  existe, está separado del núcleo, no lleva nombres y tiene base legal. La propuesta externa
  tenía razón en que la propiedad está en el dato preparado; esto es prepararlo sin construir
  nada encima todavía.

## Decisiones de Jose (abiertas)

1. **Región de BigQuery**: EU multirregión (propuesta) o Madrid (`europe-southwest1`). Nace y no
   se mueve.
2. **El tipo de tarea**: ¿un campo `kind` que elige quien crea la tarea (una lista corta por
   sector), o se deriva del contrato/plantilla del que nace? Propuesta: campo propio con lista
   corta, porque las tareas sueltas sin contrato son la mayoría hoy.
3. **La lista de sectores** para `entities.sector`: propuesta `limpieza`, `sad`, `oficina`,
   `construccion`, `eventos`, `mantenimiento`, `otros`.
4. **La frase legal** en el contrato de encargo: cuándo y con quién.
5. **Incidencias al espejo ahora o después**: es la pieza que más explica y la que menos cuesta
   (un espejo más con el patrón de tareas).

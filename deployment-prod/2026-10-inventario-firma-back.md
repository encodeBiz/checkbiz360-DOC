# Pase a producción — inventario, documentos de los equipos y firma (octubre 2026)

**Estado: documentación del despliegue del 2026-10-11.** Jose, 2026-10-10 por la noche: «déjalo
marcado como documentación de despliegue para mañana». Se ejecuta en el orden de §10, empezando
por el paso 0, y cada paso se anota en §11 con hora y resultado. (El origen: 2026-10-09, «ve
documentando todo para cuando pasemos a prod».)
**Alcance:** todo lo que entró en `develop`/`staging` de `encodebiz-api` entre el 2026-09-28 y el
2026-10-09 y aún no está en `main`: el servicio `inventory` (Fases 0–6d), el material en el
informe de tareas (TDR-005), los documentos de los equipos y la entrega con documentos (6b, 6d),
y el módulo de firma (registro de claves, retos, acuse firmado en inventario y documental).
Se suman tres cambios de facturación del 2026-10-09 (§6.1, §6.2): los despedidos que ficharon
en el periodo se cobran, el cliente recibe un correo cuando falla un cobro, y la pestaña de
facturas del panel las lee de Stripe en vez de una colección que ya nadie llena.
**Última revisión de este registro:** 2026-10-10 por la noche, contrastado entero con
`git diff origin/main..origin/staging` de la API, del panel y del SaaS; lo que cambió lleva la
marca «rev. 10-oct». Al 2026-10-10, `origin/staging` de los dos repos ya contiene todo lo que
hay en `origin/develop`: no queda nada por subir a staging; va 154 commits (API) y 115 (panel)
por delante de `origin/main`.
**Cómo se usa:** se va completando; el día del pase se ejecuta en el orden de §10 y se anota
aquí lo hecho, como en [2026-09-05-back.md](./2026-09-05-back.md).

> **Rev. 10-oct — el hook `block-prod.sh` está desenganchado**: `.claude/settings.json` tiene
> `"PreToolUse": []`, igual que antes del 2026-09-07. La regla sigue valiendo (es de Jose, no del
> fichero) y este registro se ha hecho sin mirar producción; pero conviene rearmarlo **antes** del
> día del pase, que es cuando más comandos de prod se escriben al lado de los de dev.
>
> Lo que **no se ha podido comprobar en producción** porque producción no se mira desde aquí: el
> ruleset de Firestore vigente, los índices compuestos que existen, los eventos suscritos en
> el endpoint de Stripe, el contenido de `.env.production` y si la pestaña de Facturas del panel
> enseña algo hoy (§6.2). Cada uno tiene su aviso abajo.

---

## 0. Lo primero, porque no es evidente

1. **El servicio `inventory` no existe en producción**: ni en `docker-compose.yml`, ni en
   `nginx/nginx.conf`, ni en `.env.production`. Staging lo tiene desde el 2026-09-28. El pase
   es añadir un contenedor, no solo código (§1, §2, §3).
2. **`firebase.json` de `encodebiz-api` declara ahora `firestore.rules`** (2026-10-09). Un
   `firebase deploy` sin `--only` desplegaría **functions y reglas** a la vez. Reglas: siempre
   `--only firestore:rules`; functions: siempre por nombre. Y siempre `--project`.
3. **Las reglas de Firestore de producción no se han leído nunca.** El fichero del repo da por
   hecho el comodín abierto que había en dev. Antes de desplegarlo en prod hay que leer el
   ruleset vigente (§5.3): si es otro, se funde; si no, se pisaría algo que no conocemos.
4. **El inventario se cobra por plantilla con un precio de Stripe que en vivo no existe** (§6).
   Sin él, el plan queda dado de alta pero nadie puede contratarlo. No es bloqueante para
   desplegar: el servicio responde 403 `inventory/not_subscribed` y el panel enseña la puerta.
5. **Los índices de `items` no se crean solos** (§5.1). Sin ellos, Existencias responde 500 a
   la primera entidad que active el módulo.
6. **La pestaña de facturas del panel no enseña ninguna factura de suscripción**, y este lote
   lo arregla (§6.2): leía `entities/{id}/invoices`, y nadie llena esa colección desde que la
   facturación se portó a `billing` (leído en el código, **no comprobado en prod**: el webhook
   anota sobre documentos que ya existan y nunca los crea). El arreglo depende de una clave de Vercel (§8.1), y si falta, la pestaña
   se queda vacía igual. El síntoma del olvido es idéntico al del fallo que se venía a corregir,
   así que esa clave se comprueba mirando la pestaña, no el despliegue.
7. **La firma dentro del PDF (PAdES) SÍ entra en este lote** (rev. 10-oct; §9b decía lo
   contrario). Los commits del documental del 2026-10-09 (`443da75`, `5747cd0`, `1386354`) están
   en `staging`. Sin la CA en el servidor no rompe nada: preparar la firma de un PDF responde
   `ca_not_configured` y el acuse sigue por el camino de siempre; pero ninguna nómina sale firmada
   por dentro hasta que la CA exista. Es una decisión del día del pase: con CA o sin ella (§9b).
8. **El `docker-compose.yml` de producción no tiene los anclajes `x-service` ni `x-health`** que
   usa el de staging (rev. 10-oct). El bloque de `inventory` va escrito desarrollado (§1); copiado
   tal cual de staging, compose no parsea el fichero y el despliegue entero falla.

---

## 1. `docker-compose.yml` de producción — un bloque a añadir y dos líneas en los secretos

**Rev. 10-oct.** El compose de producción **no tiene** los anclajes `x-service`/`x-health` del de
staging (solo `x-secret-volumes`): cada servicio va escrito entero, con `env_file:
.env.production`, su `healthcheck` completo y `restart`. El bloque, en esa forma, al estilo de
`billing` o `events`, y **fuera del `depends_on` de nginx** (como `employees`: tocar esa lista
recrea nginx, y el workflow ya lo reinicia tras el `up`):

```yaml
  # ── Inventario — add-on (puerto 3016) ─────────────────────────────────────
  # Consumibles y operables ligados a las tareas. Servicio y factura aparte: sin
  # suscripción activa responde 403 a todo menos /health. Ver DOCS/ingenieria/inventario/
  inventory:
    build:
      context: .
      dockerfile: services/inventory/Dockerfile
    env_file: .env.production
    environment:
      - NODE_ENV=production
      - PORT=3016
    volumes: *secret-volumes
    depends_on:
      postgres:
        condition: service_healthy
    expose:
      - "3016"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3016/health"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

Y en `x-secret-volumes`, las dos líneas que staging tiene desde el 2026-10-09 para la CA de
firma (§9b). Van en el PR **con o sin CA**: si los ficheros no existen en el servidor, Docker
monta un directorio vacío en su lugar y el servicio arranca igual, sin emitir certificados:

```yaml
x-secret-volumes: &secret-volumes
  - ./secrets/firebase-sa.json:/secrets/firebase-sa.json:ro
  - ./secrets/signing-ca.key:/secrets/signing-ca.key:ro
  - ./secrets/signing-ca.crt:/secrets/signing-ca.crt:ro
```

Lee el mismo `env_file` y los mismos secretos que los demás. Postgres lo alcanza por la red de
contenedores (espeja a las `dim_*` y `*_raw` de la 023–025; de ahí el `depends_on`). Arranca
tres trabajos propios: recálculo de saldos (30 min), reespejo a Postgres (5 min) y avisos de
caducidad de papeles (6 h y a los 2 min de arrancar). El `deploy.yml` hace `up --build -d` del
fichero entero, así que no hay ninguna lista de servicios que ampliar.

## 2. `nginx/nginx.conf` de producción — un upstream y dos rutas

Copiar de `nginx.staging.conf` (líneas 36, 111 y 191–192):

```nginx
  upstream inventory_service  { server inventory:3016; }
  …
    location = /api/v1/inventory  { proxy_pass http://inventory_service/api/v1/inventory; }
  …
    location /api/v1/inventory/ {
      client_max_body_size 4m;   # importación por plantilla (TDR-007): sin esto nginx corta en 1 MB
      proxy_pass http://inventory_service/api/v1/inventory/;
    }
```

El `client_max_body_size` llegó con la importación masiva por plantilla (2026-10-09): la subida
viaja como base64 dentro de JSON y un fichero de más de ~750 KB pasa del mega por defecto de
nginx. Staging lo tiene desde esa fecha; si el pase no lleva la importación, sobra pero no estorba.

Todo lo demás de este lote cuelga de rutas que prod **ya** proxya (comprobado en
`nginx/nginx.conf`, rev. 10-oct): `/api/reports/` (informe de equipos y de consumo, actas),
`/api/v1/documents/` (ámbitos, vínculos, `signing-subject`, `sign/prepare`),
`/api/v1/checkinbiz/auth/` (`signing-keys`, `signing-challenges`, `signing-ca/bundle`) y
`/api/v1/billing/` (facturas). El `deploy.yml` reinicia nginx tras el `up -d` (resuelve los
upstreams al arrancar).

## 3. Variables de entorno — `/opt/encodebiz-api/.env.production`

### 3.1 Obligatoria — sin ella el inventario no se entera de las tareas

| Clave | Valor | Por qué |
|---|---|---|
| `INVENTORY_INTERNAL_URL` | `http://inventory:3016/api/v1/inventory/internal/task-events` | El inventario es un **suscriptor interno** del motor de eventos (`shared/events/internalSubscribers.ts`): solo existe si su URL está en el entorno. Sin ella, al validar o cancelar una tarea no se liberan reservas ni se cuadra material, **en silencio**. Firma con `ENCODEBIZ_API_KEY`, que ya está. |

El `env_file` es común a todos los contenedores, así que se pone una vez y la ven `tasks` (que
emite) y `events` (que rescata).

### 3.2 Con defecto — para fijar el comportamiento

| Clave | Defecto | Qué |
|---|---|---|
| `INVENTORY_RECOMPUTE_MINUTES` | `30` | recálculo de saldos desde el libro; `0` lo apaga |
| `INVENTORY_REMIRROR_MINUTES` | `5` | reintento del espejo a Postgres; `0` lo apaga |
| `INVENTORY_DOC_EXPIRY_HOURS` | `6` | avisos de papeles por caducar / caducados; `0` lo apaga |
| `BILLING_TRIAL_DAYS` | ya existe (`15`) | la prueba del inventario es la misma |
| `SIGNING_CA_KEY_PATH` / `SIGNING_CA_CERT_PATH` | `/secrets/signing-ca.key` / `.crt` | dónde busca la CA de firma (§9b); con el montaje de §1 no hay que tocarlas (rev. 10-oct) |

`.env.example` del repo —la plantilla de producción— **no lleva ninguna clave de inventario**;
`.env.staging.example` sí (rev. 10-oct). Añadirlas en el mismo PR: es donde el siguiente las
va a buscar.

### 3.3 Ya deberían estar — comprobar, no añadir

`ENCODEBIZ_API_KEY`, `DATABASE_URL` (o las `PG*`), `FIREBASE_STORAGE_BUCKET`, las de `billing`
y `reports`. Nada nuevo para la firma: usa Firestore con el Admin SDK y `crypto` de Node.

## 4. Migraciones de Postgres (`encodebiz_analytics`)

Tres, **a mano, por SSH, una a una, mirando el resultado**, como manda CLAUDE.md. Las tres son
`IF NOT EXISTS`: repetirlas no rompe.

| Orden | Fichero | Qué crea |
|---|---|---|
| 023 | `migrations/023_inventario.sql` | `dim_warehouses`, `dim_items`, `dim_item_units` (con sus índices por entidad), `item_movements_raw` (5 índices), `unit_reservations_raw`; amplía el `CHECK` de `dim_sync_log` |
| 024 | `migrations/024_inventario_entregas.sql` | `unit_assignments_raw` (3 índices) |
| 025 | `migrations/025_inventario_posiciones.sql` | `unit_positions_raw` (2 índices): el rastro de dónde ha estado cada ejemplar (ADR-008). Sin ella el servicio funciona, pero no espeja el rastro y lo avisa en el log |

```bash
# producción — una cada vez, y leer la salida
docker compose --env-file .env.production -f docker-compose.yml exec -T postgres \
  psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 \
  -f /docker-entrypoint-initdb.d/023_inventario.sql
```

La ruta es la del montaje real (rev. 10-oct): el compose de prod monta `./migrations` en
`/docker-entrypoint-initdb.d` del contenedor de Postgres, y así se pasó la 010 en septiembre.
El fichero tiene que estar ya en el servidor, o sea **después** del `git pull` del despliegue,
o por la tubería del ssh como se hizo con la 022. En staging se ejecutaron el 2026-09-28, el
2026-10-08 y, la 025, el 2026-10-10.

Lo único de la 023 que no es `IF NOT EXISTS` es el `CHECK` de `dim_sync_log`: hace `DROP
CONSTRAINT IF EXISTS dim_sync_log_dimension_check` y lo vuelve a crear con seis valores. El
nombre es el que Postgres le puso solo en la 006 (CHECK en línea sobre la columna `dimension`),
así que el DROP lo encuentra y repetirla tampoco rompe. `analytics` la necesita también (§7).

**No hay columna nueva para los documentos de la entrega ni para la firma**: viven en Firestore
(`unit_assignments.documents`, `acknowledgement.signature`); el informe los lee de ahí.

## 5. Firestore

### 5.1 Índices compuestos — con `gcloud`, nunca con `firebase deploy`

Dev tiene dos del inventario que prod no tendrá (TDR-003: Existencias pagina por nombre con
filtro de activo y tipo). El resto de consultas del inventario, de los documentos de los
equipos (`array-contains`, `array-contains-any`, `in`) y de la firma son de un solo campo o
igualdades y no piden índice.

```bash
gcloud firestore indexes composite create --project=encodebiz-services \
  --collection-group=items --query-scope=COLLECTION \
  --field-config=field-path=active,order=ascending \
  --field-config=field-path=name,order=ascending
gcloud firestore indexes composite create --project=encodebiz-services \
  --collection-group=items --query-scope=COLLECTION \
  --field-config=field-path=active,order=ascending \
  --field-config=field-path=type,order=ascending \
  --field-config=field-path=name,order=ascending
```

Los 14 índices de `documents` que dev tiene vienen del documental de julio; comprobar en
consola que prod los tiene (debería: el documental está en prod desde el 2026-07-26).
**El hook bloquea `--project=encodebiz-services`: lo ejecuta Jose.**

**Comprobado contra lo desplegado en dev, no contra el fichero (rev. 10-oct, noche):**
`gcloud firestore indexes composite list --project=dev-encodebiz` devuelve 133 índices y, de
inventario, solo esos dos de `items`. Cuadra con el código: todas las demás consultas del
inventario, de los papeles de los equipos y de la firma son igualdades, `in` o `array-contains`
sin `orderBy` (índices de un campo, que Firestore funde solo), y los dos `orderBy` que hay van
sobre `name` en `items` (los dos índices) y sobre `at` en la subcolección `positions` (un campo).
El de `checklogs (employeeId, status, timestamp)` de §5.7 está `READY` en dev, y los 14 de
`documents`, también. El recuento de despedidos (§6.1) filtra `status` en memoria a propósito,
para no pedir `(status, updatedAt)`.

### 5.2 Ficha del add-on — `service/inventory` y `service/inventory/plan/standard`

```bash
# dentro del contenedor inventory de prod; sin --apply simula
node services/inventory/dist/scripts/alta-servicio.js --stripe-price price_live_xxx --apply
```

Desde el 2026-10-08 el script **no borra** un precio ya puesto si se repite sin
`--stripe-price`. Sin precio, el plan no es contratable (HAL-13). La tarjeta y la página de alta
del panel sacan sus textos de i18n (`salesPlan.plans.standard`), no de este documento.

### 5.3 Reglas de Firestore — `encodebiz-api/firestore.rules`

Versionadas desde el 2026-10-09 en `encodebiz-api` (antes no estaban en ningún repo) y
desplegadas en dev ese día. El fichero conserva el comodín abierto hasta 2030 que había en dev y
le quita solo lo del módulo de firma: `signing_keys` y `signing_challenges` sin acceso desde el
cliente, y `signingKey` del documento del dispositivo sin crear ni cambiar desde el cliente.

**Antes de tocar prod:**

1. Leer el ruleset vigente en prod (consola de Firebase, o la API de firebaserules con
   `x-goog-user-project: encodebiz-services`) y **guardar copia** en
   `deployment-prod/` (es el rollback).
2. Si es el mismo comodín que tenía dev → desplegar el fichero tal cual.
3. Si es distinto → fundir a mano: lo que hay que conservar es el `match /{collection}/{document=**}`
   con `!soloServidor(collection)` y `noTocaSigningKey()`.

```bash
cd encodebiz-api && firebase deploy --only firestore:rules --project encodebiz-services
```

La app publicada hoy (1.2.0+47) **no escribe `signingKey`** (eso lo hace solo la versión aún no
publicada, por API), así que estas reglas no le afectan.

### 5.3b Storage — nada que crear, pero sí que saber

La evidencia de cada firma se escribe en el bucket de `FIREBASE_STORAGE_BUCKET` bajo
`signatures/evidence/{entityId}/{purpose}/{challengeId}.json` **una sola vez** (precondición de
generación 0), y las actas bajo
`checkbiz/reports/entities/{e}/actas/{layout}/acta_{challengeId}.pdf`, donde `{layout}` es la
versión del dibujo del acta: **`v2` desde el 2026-10-09**. La carpeta lleva la versión a
propósito, para que al cambiar el dibujo las actas ya guardadas se vuelvan a generar en la
carpeta nueva sin tocar la evidencia, que no cambia. En prod no hay nada que migrar porque
todavía no existe ninguna acta; en dev quedan las de `v1`, huérfanas y sin borrar.

Ninguna regla de retención debe borrar la evidencia: es la prueba. Conviene activar en el bucket
la **retención** (o al menos el versionado) de `signatures/`, que hoy no está en ningún entorno.

### 5.4 Colecciones que se crean solas

Además de lo de abajo, con el rastro de posición: `entities/{e}/item_units/{unitId}/positions`. Los ejemplares ganan
`position` y `outOfBase`. **Ningún índice nuevo**: el filtro «fuera de base» son dos igualdades
(`active`, `outOfBase`) y el rastro ordena por un solo campo dentro de su subcolección.

`signing_keys/{employeeId}/keys`, `signing_challenges`, `entities/{e}/inventory_notices`, y
bajo cada entidad con el módulo: `items`, `warehouses`, `item_units`, `stock`, `movements`,
`unit_reservations`, `unit_assignments`, `task_materials` y, con la importación por plantilla,
`import_batches` (con sus subcolecciones `rows` y `results`). `documents` gana campos
(`itemId`, `unitId`, `linkedItemIds`, `linkedUnitIds`, `contentSha256`, `metadata.result`) sin
migrar nada: los anteriores no los tienen y el código lo contempla.

### 5.5 Por cada entidad que active el inventario

```bash
node services/inventory/dist/scripts/reindex-search.js --entity <entityId> --apply
node services/inventory/dist/scripts/mirror-dimensions.js --entity <entityId> --apply
```

Solo hacen falta para datos que existieran antes del código que los indexa y espeja (en prod,
ninguno): se anotan por si se importa un catálogo a mano.

```bash
node services/inventory/dist/scripts/backfill-positions.js --entity <entityId>           # simula
node services/inventory/dist/scripts/backfill-positions.js --entity <entityId> --apply   # lo hace
```

Da su primera posición (ADR-008) a los ejemplares dados de alta antes del rastro: entregado →
con la persona, en uso → en el sitio de su tarea, si no → su base. **En prod no hay ejemplares
anteriores**: lo que se dé de alta ya nace con posición, así que solo hace falta si se importó o
se migró algo a mano. En staging se pasó el 2026-10-10 a la única entidad con ejemplares
(Cuidama: 3 en su base, 2 con una persona).

### 5.6 Plantillas de correo del cobro fallido — `emails_template`

`PAYMENT_FAILED_es` y `PAYMENT_FAILED_en`, creadas en dev el 2026-10-09 con el mismo diseño que
`INVOICE_*`. En prod **no existen**: hay que copiarlas desde dev (mismos ids, `type` y `locale`;
con `create`, que falla si ya están). Sin ellas el correo sale igual, pero con el texto de
respaldo del código, sin diseño. El hook bloquea `encodebiz-services`: lo ejecuta Jose.

Comprobación: `emails_template where type == "PAYMENT_FAILED"` devuelve 2 documentos (`es`, `en`).

### 5.7 Índice que usa el recuento de despedidos

`checklogs (employeeId, status, timestamp)` — el mismo que ya usa `findOverlapInRange`, así que
debería existir. En dev está `READY`; **en prod sin comprobar**. Si faltase, la cuenta de
`invoice.upcoming` fallaría y la suscripción no se ajustaría antes de cobrar.

## 6. Stripe (cuenta en vivo)

- **Precio del plan `standard` del inventario**: 29 €/mes hasta 50 empleados + 0,75 € por cada
  empleado a partir del 51, como precio **graduado por cantidad** sobre el producto nuevo
  «Inventario» (inventario 06 §D2). El `price_live_…` resultante va a §5.2.
- **Webhook**: el endpoint de prod apunta a `billing:3011` desde el 2026-09-04. Comprobar que
  tiene los 8 eventos, en particular `invoice.upcoming` y `customer.subscription.trial_will_end`
  (son los que ponen la cantidad = plantilla antes de cobrar; sin ellos la primera factura del
  inventario saldría a 0 €, ver memoria «cobro al fin de la prueba»). **Sin comprobar en prod.**
- `GetCountPayPerUse` ya cuenta plantilla para `inventory` igual que para `checkinbiz`.
- Entre los eventos del webhook tiene que estar `invoice.payment_failed`: es el que dispara el
  correo de §6.1. **Sin comprobar en prod.**
- (rev. 10-oct) El router de billing contrata y da de baja solo lo que está en
  `PlatformServices` —antes una lista fija `checkinbiz`/`passinbiz`, y el alta del inventario
  moría en `unknown_service` antes de llegar a Stripe—, y para `inventory` pide a la empresa lo
  mismo que para checkinbiz: datos legales y método de pago, no `slug` ni logo. Las rutas de alta
  y baja son las de siempre, así que las variables `…_SUBCRIBE`, `…_UNSUBCRIBE` y
  `…_CONFIGBILLING` de Vercel (a billing desde el 12-sep) sirven sin tocarlas.
  `GET /invoices/:entityId` exige `canWrite` (owner o admin) y 404 si la empresa no existe.

### 6.1 Cambios de facturación que entran (billing)

1. **Despedidos con actividad.** En `invoice.upcoming`, el borrador y la auditoría de la factura,
   a la plantilla viva se suman los empleados en `fired` con **al menos 6 fichajes `valid`** en el
   periodo de la factura (en `trial_will_end`, el de la prueba). Cubre a quien contrata gente
   unos días y la despide antes del corte. `inactive` ya contaba y sigue igual. Alta y baja
   cuentan solo la plantilla viva. Rama `feat/facturar-despedidos-con-fichajes`, en `staging`
   desde el 2026-10-09.
   Efecto en prod: la primera factura tras el pase puede subir respecto a la anterior en
   entidades con bajas en el mes. No es un error; conviene saberlo si un cliente pregunta.
2. **Correo al cliente cuando falla un cobro**, de cualquier servicio, una vez por intento
   fallido, con el enlace de Stripe para pagar o cambiar la tarjeta. Registro en
   `invoice_emails/{factura}_payment_failed_{intento}`. Pide las plantillas de §5.6. Rama
   `feat/aviso-cobro-fallido`, en `develop` y `staging` desde el 2026-10-09.

Comprobación tras el pase: en el siguiente `invoice.payment_failed` real, el documento en
`invoice_emails` queda en `sent`; y en la próxima renovación, el log de billing
`ajustada a N unidades` cuadra con plantilla + despedidos con actividad.

### 6.2 Las facturas del panel salen de Stripe

`GET /api/v1/billing/invoices/:entityId`, paginado en el servicio (`page`, `limit` ≤ 100,
`order`) y solo para quien pueda escribir en la entidad (owner o admin). Enseña las facturas de
las suscripciones de la empresa a **servicios de la plataforma**, add-ons incluidos, y nada más
de lo que cobre la cuenta de Stripe, que a veces le cobra al mismo cliente cosas que no son de
checkbiz360. Los borradores no salen: un borrador todavía puede cambiar o no emitirse.

Las suscripciones se reúnen de dos sitios porque ninguno basta solo: Firestore guarda las
antiguas que nacieron sin metadata, y Stripe guarda la que Firestore pierde cuando alguien
vuelve a contratar antes de que la baja anterior se archive.

Qué pide en producción: **nada en Stripe y nada en Firestore**. Lee con la clave que billing ya
tiene y no escribe. Lo único que hace falta es la clave de Vercel de §8.1; la ruta
`/api/v1/billing/` ya está en el `nginx.conf` de prod desde el porte de septiembre.

Qué arregla: antes la pestaña leía `entities/{id}/invoices`, y esa colección no la llena nadie
desde el porte —el webhook anota sobre documentos que ya existan, pero nunca los crea—, así que
no sale ninguna factura de suscripción, ni de checkinbiz ni del inventario. Eso está **leído en
el código, no comprobado en producción**; se confirma mirando la pestaña antes del pase, que es
además la forma de distinguir después si la clave de §8.1 se puso o se olvidó.

La lista de servicios de la plataforma queda en un solo sitio,
`billing/src/domain/PlatformServices.ts`, y la usan el alta, la baja, el webhook y esta
pestaña. **Un add-on nuevo se añade ahí y en ningún otro sitio**, que es lo que conviene
recordar la próxima vez.

Comprobación tras el pase: abrir Facturación → Facturas con una entidad que tenga al menos una
factura emitida y ver la fila con su servicio, su estado traducido y el PDF descargable. Vacía
con una entidad que sí tiene facturas en Stripe significa que falta la clave de §8.1.

## 7. Servicios que cambian (ya desplegados por CI al fusionar `staging → main`)

| Servicio | Qué entra |
|---|---|
| `inventory` | **nuevo** (§1–§3), con la importación por plantilla (TDR-007) y el rastro de posición del ejemplar (ADR-008): liberar pregunta «¿dónde queda?» (tarea o almacén), `POST /units/:id/receive`, `GET /units/:id`, `GET /units/:id/positions`, `outOfBase` en tablero y Existencias |
| `reports` | material en el informe de tareas (TDR-005); `POST /api/reports/equipment` (Excel, 2 hojas; 402 sin add-on); `GET /api/reports/inventory/consumption` |
| `documents` | ámbitos `item`/`unit`, 8 tipos nuevos, `POST/DELETE /:id/links`, `contentSha256`, acuse firmado y `GET /:id/signing-subject`; y (rev. 10-oct, faltaba) la **firma dentro del PDF**: `POST /:id/sign/prepare`, el acuse con reto PAdES incrusta la firma y **el PDF firmado sustituye al original** (se descarga como `<nombre>-firmado.pdf`; el original queda a un lado). Solo documentos dirigidos a un único empleado. Sin CA responde `ca_not_configured` y el acuse sigue el camino normal. Permisos: los papeles de `item`/`unit` los ve quien tenga nivel *manager* en alguna sucursal; los tipos restringidos y disciplinarios no admiten esos ámbitos. Los vínculos a equipos van en `linkedItemIds`/`linkedUnitIds` (`array-contains`, sin índice compuesto); en la ruta de Storage el id del equipo ocupa el sitio del de la sucursal |
| `checkinbiz` | `POST /auth/signing-keys`, `POST /auth/signing-challenges`; públicos `GET /auth/signing-ca.crt` y `GET /auth/signing-ca/bundle` (zip con .cer, .crt e instrucciones; lo que usa la clave `…_SIGNING_CA` de §8.1). Una clave registrada antes de que exista la CA recibe su certificado la siguiente vez que se usa, sin tocar el móvil |
| `shared` | inventario, cumplimiento de papeles, firma, `internalSubscribers`, avisos `unit_*` |
| `billing` | despedidos con actividad en el recuento; correo de cobro fallido (§6.1); `GET /api/v1/billing/invoices/:entityId` para la pestaña de facturas (§6.2) |
| `analytics` | (rev. 10-oct, faltaba) `SyncDimensions` espeja también `warehouses`, `items` e `item_units` a las `dim_*` por el mismo camino que sucursales y empleados; **necesita la 023**. Mientras ninguna entidad tenga inventario no toca esas tablas y no da error, pero el orden de §10 pone la migración primero igual |
| `merlin` | (rev. 10-oct, faltaba) herramienta de soporte `puesta-en-marcha` (`92d7c7f`, 07-oct): rechaza como geocerca la dirección que Google solo casa en parte, avisa en vez de bloquear por calle sin número, admite plantilla sin responsabilidad y sembrar sobre una entidad existente sin bloque de empresa. Solo CLI; sin infra ni variables nuevas |
| `firebase_sdk` | sin cambios en este lote (lo que tiene pendiente de despliegue es de septiembre: §9d) |

Nada de esto rompe a quien no tiene el add-on: sin suscripción el inventario responde 403, el
informe de tareas sale idéntico al de siempre y los documentos siguen igual.

## 8. Front (`encodebiz-front-saas`, Vercel) — proxy, variables y promoción

### 8.0 Entradas del proxy (rev. 10-oct)

El navegador no habla con la API: pasa por `/api/proxy/<handler>`, y solo existen los handlers
dados de alta en `src/lib/http/serverBackendProxy.ts`, cada uno con su variable, sus métodos y,
si la base es una raíz, la lista de subrutas que deja pasar. Este lote da de alta **seis**, uno
por clave de §8.1:

| Handler | Variable | Métodos | Subrutas | Quién lo usa |
|---|---|---|---|---|
| `checkinbiz_inventory_handler` | `…_CHECKINBIZ_INVENTORY_HANDLER` | GET, POST, PATCH, DELETE | allowlist de las rutas del contrato: `access`, `board`, `movements`, `warehouses…` (+ `import-template`, `imports`), `imports/:id(/apply)`, `items…` (+ `units`, `documents`), `units/:id/{schedule,assign,assignments,documents,positions,receive}`, `assignments/:id/{acknowledge,return}`, `employees/:id/assignments`, `me/assignments`, `stock/{overview,discrepancies,receipts,adjustments,transfers,minimum}`, `tasks/:id/materials{,/reserve,/issue,/consume,/settle}` y `tasks/:id/units(/:id)`. `/internal/*` fuera a propósito | toda la sección Inventario, el material de la tarea, los equipos del empleado |
| `checkbiz360_reports_equipment` | `…_REPORTS_EQUIPMENT` | POST | ninguna (URL completa) | informe «Equipos y EPIs» |
| `checkbiz360_reports_inventory` | `…_REPORTS_INVENTORY` | GET | ninguna | informe de consumo |
| `checkbiz360_reports_signatures` | `…_REPORTS_SIGNATURES` | GET | `/acta`, `/evidence` | «Descargar el acta» en la ficha del documento |
| `checkinbiz_signing_ca` | `…_CHECKINBIZ_SIGNING_CA` | GET | ninguna | «Certificado de firma» en Entorno de trabajo |
| `billing_invoices` | `…_BILLING_INVOICES` | GET | `/:entityId` | Facturación → Facturas |

Y **reutiliza cuatro que prod ya tiene**, sin tocar su variable: `checkinbiz_documents_handler`
(reenvía cualquier subruta con GET/POST/PATCH/DELETE, así que `/documents/:id/links` y
`/documents/:id/signing-subject` pasan sin cambios en el proxy), y `subcribe`, `unsubcribe` y
`configbilling`, que desde el 12-sep apuntan a billing en Vercel y ahora sirven también para
contratar y dar de baja el add-on.

### 8.1 Claves nuevas en Vercel (producción)

| Clave | Valor |
|---|---|
| `NEXT_BACKEND_URI_CHECKINBIZ_INVENTORY_HANDLER` | `https://api.checkbiz360.com/api/v1/inventory` |
| `NEXT_BACKEND_URI_CHECKBIZ360_REPORTS_INVENTORY` | `https://api.checkbiz360.com/api/reports/inventory/consumption` |
| `NEXT_BACKEND_URI_CHECKBIZ360_REPORTS_EQUIPMENT` | `https://api.checkbiz360.com/api/reports/equipment` |
| `NEXT_BACKEND_URI_CHECKBIZ360_REPORTS_SIGNATURES` | `https://api.checkbiz360.com/api/reports/signatures` |
| `NEXT_BACKEND_URI_CHECKINBIZ_SIGNING_CA` | `https://api.checkbiz360.com/api/v1/checkinbiz/auth/signing-ca/bundle` |
| `NEXT_BACKEND_URI_BILLING_INVOICES` | `https://api.checkbiz360.com/api/v1/billing/invoices` |

Son **seis claves**, y cada una se nota en un sitio distinto:

| Si falta | Lo que ve el cliente |
|---|---|
| `…_INVENTORY_HANDLER` | toda la sección Inventario responde «el proxy rechazó la llamada» |
| `…_REPORTS_INVENTORY` | el informe de consumo falla al generar |
| `…_REPORTS_EQUIPMENT` | el informe «Equipos y EPIs» falla al generar |
| `…_REPORTS_SIGNATURES` | «Descargar el acta de firma» no funciona en la ficha del documento |
| `…_SIGNING_CA` | no se descarga el certificado de la CA desde «Entorno de trabajo» |
| `…_BILLING_INVOICES` | la pestaña de Facturas sigue vacía, igual que antes del arreglo (§6.2) |

Vercel solo tiene producción: no se tocan para probar.

Las seis son exactamente las que el código del panel lee de nuevo entre `main` y `staging`
(comprobado, rev. 10-oct). El `.env.example` del panel documenta **cuatro**: le faltan
`…_REPORTS_SIGNATURES` y `…_SIGNING_CA`. Completarlo en el PR del panel para que la plantilla
y esta tabla digan lo mismo (`…_CALENDAR_AVAILABILITY` y `…_UPLOAD_MEDIA` tampoco están en la
plantilla, pero eso viene de antes de este lote).

### 8.2 Promoción

Al 2026-10-10 el panel ya está empujado y `origin/staging` tiene todo lo de `origin/develop`:
los 11 commits que el 09-oct estaban sin subir ya están arriba. `origin/staging` va **115 commits
por delante de `origin/main`** en el panel y **154** en la API (rev. 10-oct, noche). La cadena
sigue siendo `develop → staging → main`, y el `main` lo fusiona y redespliega Jose en Vercel.

Revisado si `main` tiene algo que `staging` no tenga (pasó en septiembre):
- **API:** solo los merges de los PR #134–#141. Nada que reconciliar.
- **Panel:** un commit, `d7e4b3d7` «Bump version from 2.1.4 to 2.1.5», hecho directamente en
  `main`; `staging` sigue en 2.1.4. El merge no da conflicto (probado con `merge-tree`) y se
  queda con 2.1.5. Conviene fusionar `main → develop` antes, para que la versión no viva solo
  en `main`, que es lo que pasó con Turnstile.

### 8.3 Qué entra en el panel, por pantalla (rev. 10-oct)

115 commits, 2026-09-28 → 2026-10-10. **Ninguno añade lecturas ni escrituras directas a
Firestore** (comprobado en el diff: ni `getDocs`, ni `setDoc`, ni `onSnapshot` nuevos): todo lo
nuevo va por el proxy, que es lo que las reglas de §5.3 y «Postgres primero» piden. La pestaña
de facturas, de hecho, deja de leer Firestore.

| Área | Qué cambia |
|---|---|
| **Inventario** (nuevo, 40 ficheros) | la sección entera: tablero, Existencias (con «Fuera de base»), almacenes, artículos y ejemplares, movimientos, entregas, importación por plantilla, ficha del ejemplar con su posición; entrada **«Inventory» en el menú siempre que CheckBiz esté contratado** (sin add-on enseña la puerta de alta); `useInventoryAccess` pregunta a la API, no al contexto |
| **Tareas** (8) | material en la tarea: planificador al crear, sección de materiales en el detalle, diálogos de reservar, entregar, consumir y liberar |
| **Documentos** (7) | ámbitos `item`/`unit` y tipos de equipo en el modal de subida; diálogo de **vincular** un documento a equipos (`/links`); en la ficha, cómo se firmó cada acuse (biometría, PIN, contraseña o pulsado) y el botón del **acta** |
| **Facturación** | Facturas deja de leer `entities/{id}/invoices` y pide `billing_invoices`, paginado por el servidor, con servicio y estado traducidos; la tarjeta del plan trata `inventory` como add-on (un solo plan, el botón entra en el módulo, la baja desde la tarjeta); los textos del plan salen de i18n `salesPlan.plans.standard` |
| **Entorno de trabajo** (branding) | sección «Certificado de firma»: descarga el zip de la CA |
| **Empleados** | sección de equipos entregados en la ficha |
| **Informes** | «Equipos y EPIs» y «Consumo de material» en el modal de informes |
| **Contexto de la entidad** | **cambio de comportamiento**: una suscripción `trialing` cuenta como contratada (antes solo `active`). Afecta también a checkinbiz: quien esté de prueba ve los módulos como activos. Arregla que el detalle de la tarea escondiera el material a quien probaba el add-on |
| **Buscador** | `searchIndex` admite los tipos `employee`, `branch`, `document`, `item` y `warehouse` (los dos últimos los escribe el servicio de inventario) |
| **Errores e idiomas** | 37 códigos `inventory/*` traducidos; sección `inventory` en los cinco idiomas (de, en, es, fr, pt) |
| **Maquetación** | el aviso flotante de incidencias ya no tapa el menú lateral; el pie deja de ir por encima del menú |

## 9. App móvil (`checkbiz360`)

Lo lleva otra sesión. Del ADR-008, la app libera el equipo desde la tarea («¿Dónde queda?»:
la tarea o un almacén) y enseña dónde está. Al 2026-10-10 por la noche (rev.), `develop` de
`PLATAFORMA/checkbiz360` ya lleva el merge «material de la tarea con nombres y orden, el
supervisor libera equipos, fuera de radio legible y la firma del PDF dice su clave
(**1.7.0+55**)», con 7 ficheros todavía sin commitear en el árbol. La versión publicada sigue
siendo 1.2.0+47 según la última mirada a las consolas (04-sep); no se ha vuelto a comprobar.
El panel ya tiene la posición en `origin/staging` (`positionUi.tsx`, «Fuera de base» en
Existencias, diálogos de liberar y recibir): la rama `feat/inventario-posicion-ejemplar` quedó
fusionada y el árbol está limpio. Lo que no cuadraba con la API quedó dicho a sus sesiones: el
texto «si se perdió, retirado» (la API lo deja no disponible), el rastro sin enseñar en la ficha
y el tipo de vuelta de recibir; falta comprobar que se recogió.

 Para prod hace falta **una versión nueva publicada** (no sale de `master`,
sin tags, subida a mano): módulo de inventario («Mi material», declarar consumo), documentos de
la entrega, y la firma (registro de la clave por `POST /auth/signing-keys` en el login, reto y
acuse firmado). Hasta que se publique, la app actual sigue confirmando entregas con el
desbloqueo del móvil o la contraseña, que el servidor acepta igual. Pendiente de probar en un
Android y un iPhone reales (clave con solo PIN, gama baja sin StrongBox).

## 9b. Lo que NO entra en este lote (para no buscarlo)

**Corrección (rev. 10-oct): la firma incrustada en el PDF SÍ entra entera**, no solo la parte
de auth; este apartado decía lo contrario. PAdES con CA propia,
[documental 08](../ingenieria/documental-service/08_firma-incrustada-en-el-pdf.md): auth (CA,
certificado por clave, `GET /auth/signing-ca.crt` y `/signing-ca/bundle`) **y** el documental
(`POST /:id/sign/prepare`, acuse con reto PAdES, el firmado sustituye al original) están en
`staging` desde el 2026-10-09 (`443da75`, `5747cd0`, `1386354`); QA FIR-04 lo cubre con una
nómina sintética. Solo para documentos dirigidos a un único empleado.

**Qué pasa en prod sin la CA:** nada se rompe. `loadSigningCa` prueba una vez y se queda con
«no hay»; preparar la firma responde `ca_not_configured`, la app cae al acuse de siempre y el
acuse firmado con la clave del móvil (sin PDF) funciona igual. El coste es que, hasta que exista
la CA, ninguna nómina sale firmada por dentro. Y la CA puede llegar **después** sin rehacer
nada: a una clave registrada antes se le emite el certificado la siguiente vez que se usa
(`ensureCertificate`). Lo que sí hace falta al ponerla es **reiniciar `checkinbiz` y
`documents`**, porque la ausencia se cachea en el proceso.

**Decisión para el día del pase: ¿con CA de producción o sin ella?** Si es con ella:
1. generar la CA de producción desde el portátil con `services/checkinbiz/src/scripts/signing-ca.ts`
   (`--name "CheckBiz360 Firma CA" --out <dir> --apply`), **guardar la clave fuera de cualquier repo**;
2. copiar `signing-ca.key` (600) y `signing-ca.crt` (644) a `/opt/encodebiz-api/secrets/` y
   reiniciar `checkinbiz` y `documents`;
3. las dos líneas de `x-secret-volumes` ya van en §1, con o sin CA;
4. `SIGNING_TSA_URL`, solo cuando llegue el sello de tiempo (documental, pendiente).

**El cierre por impago está decidido y no pide código** (Jose, 2026-10-11: «no se cierra
mientras está en periodo de gracia»). Durante los reintentos de Stripe la suscripción queda
`past_due`, el inventario sigue abierto y el cliente recibe el correo de cobro fallido en cada
intento (§6.1). Al agotarse los reintentos Stripe cancela, manda `customer.subscription.deleted`
y billing cierra el add-on. **Depende de un ajuste de la cuenta que la API no expone**: Billing →
Revenue recovery → Retries, «si fallan todos los reintentos» = **cancelar la suscripción**. Con
«marcar como impagada» o «dejarla vencida» no llega nunca el evento y el add-on no se cierra.
Comprobarlo en la cuenta en vivo (caso que lo destapó: Full Certificado, 2026-10-09).

**El correo de la factura sigue mandando todas.** El filtro de «solo lo de la plataforma» de
§6.2 es de la pestaña del panel; `SendInvoiceEmail` no lo tiene, así que en cada
`invoice.finalized` de la cuenta el cliente recibe su factura aunque no sea de checkbiz360. Es
el comportamiento de hoy y no empeora con el pase, pero queda escrito para no buscarlo cuando
alguien pregunte por qué el panel y el correo no dicen lo mismo.

**Cambio del 2026-10-11 (Jose):** desactivado en Stripe «Enviar facturas finalizadas a los
clientes», porque billing ya las manda y llegaban duplicadas. Consecuencia: las facturas que no
son de la plataforma (p. ej. mantenimientos) ya solo las manda billing. Sin empresa en la
plataforma, `SendInvoiceEmail` cae a `invoice.customer_email` y la envía **con la plantilla de
CheckBiz360 y el nombre de empresa vacío**; sin correo en el cliente de Stripe, no sale ninguna
(`invoice_emails` en `skipped`, `sin_destinatario`). El arreglo es que el correo filtre por
`PlatformServices` como la pestaña del panel, y que las de fuera las mande Stripe o nadie:
decisión pendiente, fuera de este pase.

## 9c. Aceptación antes de subir

No se fusiona `staging → main` hasta pasar en staging el guion
[Qa/manuales/2026-10-firma-documentos-inventario-e2e.md](../Qa/manuales/2026-10-firma-documentos-inventario-e2e.md)
(panel → app → perito → informes → inventario → consumo → avisos) con la versión de la app que
se va a publicar. Tras el pase se repiten allí los pasos 1, 2 y 7 con una empresa piloto.

## 9d. Pendiente para producción que no lleva este lote y ningún otro registro recoge (rev. 10-oct)

Está aquí para que «todo lo pendiente» tenga un sitio donde mirarse. Nada de esto bloquea el
pase de inventario y firma, y nada de esto se arrastra con el PR `staging → main` de la API.

| Qué | Dónde está | Qué falta |
|---|---|---|
| **Cloud Functions (`encodeBiz-SAAS`)** | `develop` va 33 commits por delante de `main` (23-ago → 21-sep): índices de `tasks` y `documents` en `firestore.indexes.json` (+264 líneas), retirar del índice `onChecklogWebhook`, `processInvoices` y `triggerInvoiceWorker`, correos del colaborador en su idioma, ficha del colaborador y aviso de incidencia, pie del informe, asunto del correo desde la plantilla, la B mayúscula del push | **No hay registro de qué está desplegado en prod y qué no**: el 05-sep se desplegaron nueve por nombre y `main` se recortó a eso. Y **el SaaS no se promueve por merge**: su `develop` borra el codebase `critical` (los proxies que prod sigue usando); se despliega función a función, por nombre y con `--project`. Los índices, con `gcloud` (`deploy --only firestore:indexes` poda lo que el fichero no declara). Sigue pendiente quitar `onDocumentWriteSubscriptions` del índice del SaaS: el próximo deploy lo recrearía y duplicaría correos y checkout |
| **`services/firebase_sdk`** | 22 triggers portados el 12-sep (+ la B mayúscula el 17-sep), en `main` | Sin constancia de despliegue en prod; va por nombre con `scripts/desplegar.mjs`, nunca `--only functions` a secas. `MAINTENANCE_GHOST_CUTOFF_DATE` está en el código de `main` desde el 05-sep y puesta en el entorno de la función en prod, **sin desplegar**: el CI solo levanta contenedores |
| **Campañas in-app** | API en prod desde el 16-sep (PR #137) | La parte del panel (otra sesión) y las reglas de `campaigns` en prod. Sin comprobar en prod: una subida de imagen real y el 3 MB de nginx |
| **Baja de colaboradores por backend** | API y panel en prod desde el 15-sep | No se comprobó si `NEXT_BACKEND_URI_CHECKINBIZ_COLLABORATORS_HANDLER` estaba en Vercel antes del pase; sin ella el proxy da 403 al retirar a alguien. Se comprueba con una baja real |
| **`firestore.indexes.json` unión** | generado en septiembre (132 índices) | Sin commitear en el SaaS; el `develop` del SaaS declara 122 |
| **Reglas de Firestore de prod** | §5.3 | Nunca leídas. Es el primer paso del día del pase, no el sexto |

## 10. Orden de ejecución el día del pase

0. (rev. 10-oct) Rearmar el hook `block-prod.sh` (`PreToolUse` de `.claude/settings.json`).
   Leer y guardar el ruleset de Firestore de prod (§5.3). Decidir si el pase va con CA de firma
   (§9b) y, si va, generarla y copiarla antes del despliegue.
1. Migraciones 023, 024 y 025 (§4), una a una, desde `/docker-entrypoint-initdb.d/`.
2. `.env.production`: `INVENTORY_INTERNAL_URL` y, si se quiere, las de §3.2.
3. `docker-compose.yml` (bloque de `inventory` **desarrollado, sin anclajes**, y las dos líneas
   de la CA en `x-secret-volumes`), `nginx/nginx.conf` y `.env.example` (§1, §2, §3.2)
   **commiteados en el PR** `staging → main`; en el panel, antes, `main → develop` por el bump
   de versión (§8.2); fusionar; el `deploy.yml` levanta el contenedor y reinicia nginx.
4. Comprobar: `docker compose … ps` (16 → 17 contenedores `healthy`, `inventory` entre ellos) y
   `curl https://api.checkbiz360.com/api/v1/inventory/access?entityId=…` con un token de prod
   → 403 `inventory/not_subscribed` (no 502).
5. Índices de `items` (§5.1).
6. Reglas de Firestore (§5.3), con la copia del ruleset anterior guardada antes.
7. Stripe: precio en vivo (§6) y `alta-servicio.js --stripe-price … --apply` (§5.2); que el
   webhook tenga `invoice.payment_failed`.
7b. Plantillas `PAYMENT_FAILED_es/en` copiadas de dev (§5.6) e índice de `checklogs` (§5.7).
7c. (añadido el 11-oct) Plantillas del alta y la baja del inventario en `emails_template` de
   prod. **Hechas**: copiadas de dev antes del despliegue. Para la próxima plantilla que nazca en
   código: `node services/billing/dist/scripts/email-templates.js --apply` en el contenedor
   `billing`. Sin ellas el correo sale igual, con el respaldo que vive en el código.
8. Vercel: las **seis** claves (§8.1) y el PR del panel (§8.2).
9. Primera entidad: contratar desde Suscripciones; comprobar que nace `active` con 15 días de
   prueba y `quantity` = plantilla; abrir Existencias (índices), subir una entrada, generar el
   informe «Equipos y EPIs» (402 sin add-on, Excel con add-on).
9a. Rastro de posición: un ejemplar recién dado de alta sale «en su almacén»; reservarlo, poner
   la tarea en curso y liberarla desde el panel lo deja «en la tarea»; recibirlo, de nuevo en el
   almacén. Si se migró algún ejemplar a mano, `backfill-positions.js` (§5.5).
9b. Facturación → Facturas de una entidad con facturas ya emitidas: salen con servicio, estado
   y PDF (§6.2). Es la comprobación de la clave `…_BILLING_INVOICES`, que no se nota en ningún
   log.
10. App: cuando haya versión publicada (§9), un registro de clave real y un acuse firmado.

**Rollback:** el inventario es aditivo (quitar el bloque del compose y las rutas devuelve el
estado anterior; las tablas pueden quedarse). Reglas: redesplegar la copia guardada en §5.3.
Precio de Stripe: archivarlo deja el plan no contratable sin tocar código.

## 11. Registro de lo ejecutado — 2026-10-11

Una fila por paso de §10, en el orden en que se haga. Lo que no se haga, también se escribe,
con el motivo: es lo que permite saber después qué está corriendo.

| Paso (§10) | Hora | Quién | Resultado y lo que se vio |
|---|---|---|---|
| 0a. Hook | 11:20 → 12:20 | Jose / Claude | **Se deja desenganchado a propósito**: Jose decide que los pasos de prod los ejecute Claude, uno a uno con aprobación. **Rearmado a las 12:20**, al acabar los pasos de servidor: `PreToolUse` con la ruta absoluta del script, y la lista de contenedores del script ampliada con los cinco servicios nacidos desde agosto (`backoffice`, `billing`, `events`, `employees`, `inventory`) y `certbot` |
| 0b. QA de staging previo | 11:15 | Claude | El run del 10-oct falló por **una** prueba (CHK-08-70, ventana de turno que cruza medianoche a las 23h de la zona de la persona); fichero sin cambios desde el 14-sep y pasó en los runs anteriores: no es regresión. 438 de 439 en verde |
| 0c. Rama de config | 11:20–11:27 | Claude | `feat/inventario-en-produccion` en API (compose desarrollado + CA en secretos, nginx, `.env.example`) y panel (dos claves en la plantilla + merge de `main` por el bump 2.1.5) → develop → staging. `docker compose config` ok; `nginx -t` del nginx de prod ok en contenedor desechable en el VPS |
| 0d. CA de producción | 11:28 | Claude | Generada en el portátil, `~/encodebiz-secrets/signing-ca-produccion/` (fuera de repos). `CN=CheckBiz360 Firma CA, O=encodeBiz, C=ES`, hasta 2036-10-10, SHA-256 `42:E3:7E:89:…:DA:F4:4A`. Copiada a `/opt/encodebiz-api/secrets/` (key 600, crt 644) **antes** del despliegue; huella comprobada en el servidor |
| 0e. Ruleset de prod | 11:29 | Claude | **Distinto del de dev**: leer `if true`, escribir `if request.auth != null`. Copia en `2026-10-11-firestore-rules-prod-antes.rules`. El fichero del repo habría abierto escrituras anónimas: se funde (ver paso 6) |
| 1. Migraciones 023 / 024 / 025 | 11:32 | Claude | Copia previa `~/backups/encodebiz_analytics_antes_pase_2026-10-11.sql.gz` (1,7 MB, completa). Las tres por la tubería del ssh con `ON_ERROR_STOP`, exit 0. 7 de 7 tablas; CHECK de `dim_sync_log` con seis valores |
| 2. `INVENTORY_INTERNAL_URL` en el entorno | 11:33 | Claude | Copia `~/backups/env.production.antes_pase_2026-10-11`. Añadidas `INVENTORY_INTERNAL_URL`, `_RECOMPUTE_MINUTES=30`, `_REMIRROR_MINUTES=5`, `_DOC_EXPIRY_HOURS=6`. `ENCODEBIZ_API_KEY` y `FIREBASE_STORAGE_BUCKET` presentes; la de Stripe se llama `STRIPE_PRO_KEY` |
| 3. PR `staging → main` (compose, nginx, `.env.example`) y despliegue | 12:00 | Jose / CI | PR #142 abierto por Claude a las 11:55 y **fusionado por Jose a las 12:00, con el QA de staging del último commit todavía en marcha** (el del commit anterior había dado 445/445). *Production CI/CD* `38130411079` en verde a las 12:02 (2 min): `up --build -d`, reinicio de nginx |
| 4. `ps` 17 `healthy` · `inventory/access` → 403 | 12:10 | Claude | 17 contenedores, 15 `healthy` + nginx y certbot (sin healthcheck). Desde fuera: `/health` 200; `inventory/access`, raíz de inventory, `billing/invoices` y `reports/equipment` sin token → **401** (no 502); `signing-ca.crt` devuelve la CA de prod con la huella `42:E3:…:F4:4A`; `signing-ca/bundle` 200. Sin errores en los logs del arranque |
| 5. Índices de `items` | 11:31 | Claude | Descargados los de prod antes (137, copia en `2026-10-11-indices-prod-antes.json`) y comparados con dev (133). **Solo `create`, nunca deploy de índices.** Prod: los dos de `items` (137 → 139). Fundidos hacia abajo: los 12 que prod tenía y dev no (tareas por prioridad, documentos, incidencias, responsabilidades, planificadores) creados en dev (133 → 145). Los 6 de `fleetbiz_glovo` que solo tiene dev, sin tocar (otro producto) |
| 6. Reglas de Firestore | 11:30 | Claude | Fichero fundido: lectura como prod (abierta salvo `signing_keys`/`signing_challenges`), escritura con sesión como prod, más el cierre de `signingKey`. Desplegado **primero en dev** y comprobado sin sesión (leer 200, escribir 403, `signing_challenges` 403); luego en prod con el mismo resultado. Commit en la rama → develop → staging |
| 7. Precio Stripe · `alta-servicio.js` · webhook | 11:40 | Claude | Copiada la forma del precio de dev. **IVA incluido** (decisión de Jose, como el Bronze en vivo). Producto `prod_VQ9ScpOvvMYTWE` «Inventario» y precio `price_1UPJ9qJdldmbRy89Sp7nY5xl`: graduado, 2900 fijo hasta 50 + 75 por unidad desde 51, mensual/licensed, metadata `serviceId`/`planId`. `alta-servicio.js --stripe-price … --apply` ejecutado a las 12:12 en el contenedor de prod (simulado antes): `service/inventory` activo y `plan/standard` con el precio en vivo y `payPerUse`. `INVENTORY_INTERNAL_URL` visible en `tasks` y `events`. Webhook de prod: llegan `upcoming`, `trial_will_end`, `payment_failed`, `finalized`, `paid`, `deleted`; **falta `invoice.created`** (conciliación del borrador, en código de prod desde el 13-sep y nunca recibida). No se añade sin decisión de Jose |
| 7b. Plantillas `PAYMENT_FAILED_*` · índice `checklogs` | 11:43 | Claude | `PAYMENT_FAILED_es` y `_en` creadas en prod con `create` desde dev (0 → 2). Índice `checklogs (employeeId, status, timestamp)` `READY` en prod |
| 7c. Correo del alta/baja del inventario | 11:34–12:00 | Jose / Claude | **Desvío**: al probar el alta en staging, el correo era el de bienvenida general de CheckBiz360 y la baja anunciaba la cancelación de todo. Jose lo corrige en `develop → staging` (`dd09631`, `7b387a9`): `SUBSCRIBE_INVENTORY`/`CANCELLED_INVENTORY` con plantilla en código como respaldo y script `email-templates.js`. Revisado: autosuficiente (shared ya tenía `fallbackHtml`); `BILLING_CHECKOUT_SUCCESS_URL` no está en prod y el botón «Acceder» cae a `https://saas.encodebiz.com`, que es el panel. Plantillas copiadas de dev a prod a las 12:05 con `create` (las cuatro: `SUBSCRIBE_INVENTORY_es/en`, `CANCELLED_INVENTORY_es/en`); el paso 7c de §10 queda hecho antes del despliegue. PR de la API abierto: #142 |
| 8. Vercel, seis claves · PR del panel | 11:42 | Claude | Las seis en Production con la CLI (Preview no: el panel no tiene ese entorno). `…_COLLABORATORS_HANDLER` ya estaba en Production desde hace 30 días: cierra el pendiente de §9d. **PR del panel abierto a las 12:13**: encodebiz-front-saas-clean#96 (`staging → main`, 127 commits, `main` sin nada que staging no tenga); lo fusiona Jose y Vercel redespliega |
| 9. Primera entidad: alta, Existencias, informe | | | |
| 9a. Rastro de posición | | | |
| 9b. Pestaña Facturas | | | |
| 10. App (cuando haya versión) | | | |

**Incidencias y desvíos del guion:**

- **Reglas de prod distintas de las de dev** (0e). El fichero del repo copiaba el comodín de dev
  (todo abierto hasta 2030); prod pedía sesión para escribir. Desplegarlo tal cual habría abierto
  las escrituras anónimas en producción. Se fundió con la semántica de prod y se desplegó primero
  en dev. Lección: **leer el ruleset vigente antes de versionar reglas**, no después.
- **Índices en los dos sentidos** (5). Prod tenía 12 compuestos que dev no tenía (tareas por
  prioridad, documentos, incidencias, responsabilidades, planificadores): dev llevaba semanas sin
  reproducir consultas de prod. Bajados a dev. Siempre `create`, nunca deploy de índices.
- **El correo del alta del inventario era el de CheckBiz360 entero** (7c), visto al probar el alta
  en staging. Corregido por Jose en 25 minutos; plantillas copiadas a prod antes del despliegue.
- **El PR de la API se fusionó con el QA del último commit en marcha** (3). Terminó en verde
  (445/445) nueve minutos después del despliegue. El commit anterior sí tenía QA en verde.
- **`invoice.created` no llega al webhook de prod**: la conciliación del borrador (en código desde
  el 13-sep) nunca ha corrido allí. No se añade sin decisión: cambia lo que se cobra. Pendiente.
- **Stripe deja de mandar facturas** (Jose, durante el pase): desactivado «Enviar facturas
  finalizadas a los clientes» para evitar el duplicado con billing. Las facturas que no son de la
  plataforma ya solo las manda billing, con plantilla de CheckBiz360. Pendiente de decidir (§9b).
- **Cierre por impago**: decidido, sin código (§9b). Comprobar en la cuenta en vivo que al agotar
  reintentos Stripe **cancela** la suscripción.
- **TSK-05-27 y TSK-05-28** (editar tarea desde el formulario del panel) fallan al primer intento
  y pasan al reintento en los tres últimos runs de staging. Inestables, no rotas: mirar después.

**Queda para Jose, en el panel, cuando fusione encodebiz-front-saas-clean#96:** pasos 9, 9a y 9b
(primera empresa: contratar el inventario, Existencias, informe «Equipos y EPIs», rastro de
posición, pestaña Facturas). Y el paso 10 cuando la app tenga versión publicada.

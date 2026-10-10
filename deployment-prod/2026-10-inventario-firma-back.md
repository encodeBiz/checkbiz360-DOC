# Pase a producción — inventario, documentos de los equipos y firma (octubre 2026)

**Estado:** en preparación. Jose, 2026-10-09: «ve documentando todo para cuando pasemos a prod».
**Alcance:** todo lo que entró en `develop`/`staging` de `encodebiz-api` entre el 2026-09-28 y el
2026-10-09 y aún no está en `main`: el servicio `inventory` (Fases 0–6d), el material en el
informe de tareas (TDR-005), los documentos de los equipos y la entrega con documentos (6b, 6d),
y el módulo de firma (registro de claves, retos, acuse firmado en inventario y documental).
Se suman tres cambios de facturación del 2026-10-09 (§6.1, §6.2): los despedidos que ficharon
en el periodo se cobran, el cliente recibe un correo cuando falla un cobro, y la pestaña de
facturas del panel las lee de Stripe en vez de una colección que ya nadie llena.
**Última revisión de este registro:** 2026-10-10. Al 2026-10-10, `origin/staging` de los dos
repos ya contiene todo lo que hay en `origin/develop`: no queda nada por subir a staging.
**Cómo se usa:** se va completando; el día del pase se ejecuta en el orden de §10 y se anota
aquí lo hecho, como en [2026-09-05-back.md](./2026-09-05-back.md).

> Lo que **no se ha podido comprobar en producción** porque el hook no deja mirarla: el
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

---

## 1. `docker-compose.yml` de producción — un bloque a añadir

Copiar de `docker-compose.staging.yml` (líneas 378–391 al 2026-10-09), con los anclajes de prod:

```yaml
  # ── Inventario — add-on (puerto 3016) ─────────────────────────────────────
  inventory:
    <<: *service
    build:
      context: .
      dockerfile: services/inventory/Dockerfile
    environment:
      - NODE_ENV=production
      - PORT=3016
    volumes: *secret-volumes
    expose:
      - "3016"
    healthcheck:
      <<: *health
      test: ["CMD", "wget", "-qO-", "http://localhost:3016/health"]
```

Lee el mismo `env_file` y los mismos secretos (`firebase-sa.json`) que los demás. Postgres lo
alcanza por la red de contenedores. Arranca tres trabajos propios: recálculo de saldos (30 min),
reespejo a Postgres (5 min) y avisos de caducidad de papeles (6 h y a los 2 min de arrancar).

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

Todo lo demás de este lote cuelga de rutas que prod **ya** proxya: `/api/reports/` (informe de
equipos y de consumo), `/api/v1/documents/` (ámbitos, vínculos, `signing-subject`) y
`/api/v1/checkinbiz/auth/` (`signing-keys`, `signing-challenges`). El `deploy.yml` reinicia
nginx tras el `up -d` (resuelve los upstreams al arrancar).

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
  psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 -f /migrations/023_inventario.sql
```

(Ajustar la ruta al montaje real de `migrations/` en el contenedor de prod; en staging se
ejecutaron el 2026-09-28, el 2026-10-08 y, la 025, el 2026-10-10.)

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
| `documents` | ámbitos `item`/`unit`, 8 tipos nuevos, `POST/DELETE /:id/links`, `contentSha256`, acuse firmado y `GET /:id/signing-subject` |
| `checkinbiz` | `POST /auth/signing-keys`, `POST /auth/signing-challenges` |
| `shared` | inventario, cumplimiento de papeles, firma, `internalSubscribers`, avisos `unit_*` |
| `billing` | despedidos con actividad en el recuento; correo de cobro fallido (§6.1); `GET /api/v1/billing/invoices/:entityId` para la pestaña de facturas (§6.2) |
| `firebase_sdk` | sin cambios en este lote |

Nada de esto rompe a quien no tiene el add-on: sin suscripción el inventario responde 403, el
informe de tareas sale idéntico al de siempre y los documentos siguen igual.

## 8. Front (`encodebiz-front-saas`, Vercel) — variables y promoción

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

### 8.2 Promoción

Al 2026-10-10 el panel ya está empujado y `origin/staging` tiene todo lo de `origin/develop`:
los 11 commits que el 09-oct estaban sin subir ya están arriba. `origin/staging` va **106 commits
por delante de `origin/main`** en el panel y **148** en la API. La cadena sigue siendo
`develop → staging → main`, y el `main` lo fusiona y redespliega Jose en Vercel. Antes de
fusionar, revisar que `main` no tenga hotfixes que `develop` no tenga (pasó en septiembre).

## 9. App móvil (`checkbiz360`)

Lo lleva otra sesión. Del ADR-008, la app libera el equipo desde la tarea («¿Dónde queda?»:
la tarea o un almacén) y enseña dónde está; al 2026-10-10 estaba a medio hacer y sin commitear.
El panel, igual: diálogos de liberar y recibir, «Fuera de base» en Existencias y la posición en
la ficha del ejemplar, a medio hacer en `feat/inventario-posicion-ejemplar` sin commitear. Lo
que no cuadraba con la API quedó dicho a sus sesiones: el texto «si se perdió, retirado» (la API
lo deja no disponible), el rastro sin enseñar en la ficha y el tipo de vuelta de recibir.

 Para prod hace falta **una versión nueva publicada** (no sale de `master`,
sin tags, subida a mano): módulo de inventario («Mi material», declarar consumo), documentos de
la entrega, y la firma (registro de la clave por `POST /auth/signing-keys` en el login, reto y
acuse firmado). Hasta que se publique, la app actual sigue confirmando entregas con el
desbloqueo del móvil o la contraseña, que el servidor acepta igual. Pendiente de probar en un
Android y un iPhone reales (clave con solo PIN, gama baja sin StrongBox).

## 9b. Lo que NO entra en este lote (para no buscarlo)

La firma incrustada en el PDF (PAdES con CA propia, [documental 08](../ingenieria/documental-service/08_firma-incrustada-en-el-pdf.md)):
la parte de **auth está construida** (CA, certificado por clave, `GET /auth/signing-ca.crt`) y
**sí entra** en este lote con el código; el documental (preparar y montar el PDF) todavía no.
Lo que pide en prod, cuando se quiera que emita certificados (sin esto arranca igual y no emite):
1. generar la CA de producción desde el portátil con `services/checkinbiz/src/scripts/signing-ca.ts`
   (`--name "CheckBiz360 Firma CA" --out <dir> --apply`), **guardar la clave fuera de cualquier repo**;
2. copiar `signing-ca.key` (600) y `signing-ca.crt` (644) a `/opt/encodebiz-api/secrets/`;
3. añadir a `x-secret-volumes` del `docker-compose.yml` de prod las dos líneas que ya tiene el de
   staging (`./secrets/signing-ca.key:/secrets/signing-ca.key:ro` y `.crt`), en el mismo PR;
4. `SIGNING_TSA_URL`, solo cuando llegue el sello de tiempo (documental, pendiente).

**El cierre del add-on por impago tampoco entra.** Billing solo reacciona a
`customer.subscription.deleted`; mientras Stripe deja la suscripción en `past_due`/`unpaid`, el
documento sigue `active` y el inventario abierto. Falta decidir si se cierra al primer fallo o
tras un margen (caso que lo destapó: Full Certificado, 2026-10-09).

**El correo de la factura sigue mandando todas.** El filtro de «solo lo de la plataforma» de
§6.2 es de la pestaña del panel; `SendInvoiceEmail` no lo tiene, así que en cada
`invoice.finalized` de la cuenta el cliente recibe su factura aunque no sea de checkbiz360. Es
el comportamiento de hoy y no empeora con el pase, pero queda escrito para no buscarlo cuando
alguien pregunte por qué el panel y el correo no dicen lo mismo.

## 9c. Aceptación antes de subir

No se fusiona `staging → main` hasta pasar en staging el guion
[Qa/manuales/2026-10-firma-documentos-inventario-e2e.md](../Qa/manuales/2026-10-firma-documentos-inventario-e2e.md)
(panel → app → perito → informes → inventario → consumo → avisos) con la versión de la app que
se va a publicar. Tras el pase se repiten allí los pasos 1, 2 y 7 con una empresa piloto.

## 10. Orden de ejecución el día del pase

1. Migraciones 023, 024 y 025 (§4), una a una.
2. `.env.production`: `INVENTORY_INTERNAL_URL` y, si se quiere, las de §3.2.
3. `docker-compose.yml` y `nginx/nginx.conf` (§1, §2) **commiteados en el PR** `staging → main`;
   fusionar; el `deploy.yml` levanta el contenedor y reinicia nginx.
4. Comprobar: `docker compose … ps` (16 → 17 contenedores `healthy`, `inventory` entre ellos) y
   `curl https://api.checkbiz360.com/api/v1/inventory/access?entityId=…` con un token de prod
   → 403 `inventory/not_subscribed` (no 502).
5. Índices de `items` (§5.1).
6. Reglas de Firestore (§5.3), con la copia del ruleset anterior guardada antes.
7. Stripe: precio en vivo (§6) y `alta-servicio.js --stripe-price … --apply` (§5.2); que el
   webhook tenga `invoice.payment_failed`.
7b. Plantillas `PAYMENT_FAILED_es/en` copiadas de dev (§5.6) e índice de `checklogs` (§5.7).
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

## 11. Registro de lo ejecutado

_(vacío: se rellena el día del pase)_

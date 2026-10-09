# Pase a producción — inventario, documentos de los equipos y firma (octubre 2026)

**Estado:** en preparación. Jose, 2026-10-09: «ve documentando todo para cuando pasemos a prod».
**Alcance:** todo lo que entró en `develop`/`staging` de `encodebiz-api` entre el 2026-09-28 y el
2026-10-09 y aún no está en `main`: el servicio `inventory` (Fases 0–6d), el material en el
informe de tareas (TDR-005), los documentos de los equipos y la entrega con documentos (6b, 6d),
y el módulo de firma (registro de claves, retos, acuse firmado en inventario y documental).
**Cómo se usa:** se va completando; el día del pase se ejecuta en el orden de §10 y se anota
aquí lo hecho, como en [2026-09-05-back.md](./2026-09-05-back.md).

> Lo que **no se ha podido comprobar en producción** porque el hook no deja mirarla: el
> ruleset de Firestore vigente, los índices compuestos que existen, los eventos suscritos en
> el endpoint de Stripe y el contenido de `.env.production`. Cada uno tiene su aviso abajo.

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
      proxy_pass http://inventory_service/api/v1/inventory/;
    }
```

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

Dos, **a mano, por SSH, una a una, mirando el resultado**, como manda CLAUDE.md. Las dos son
`IF NOT EXISTS`: repetirlas no rompe.

| Orden | Fichero | Qué crea |
|---|---|---|
| 023 | `migrations/023_inventario.sql` | `dim_warehouses`, `dim_items`, `dim_item_units` (con sus índices por entidad), `item_movements_raw` (5 índices), `unit_reservations_raw`; amplía el `CHECK` de `dim_sync_log` |
| 024 | `migrations/024_inventario_entregas.sql` | `unit_assignments_raw` (3 índices) |

```bash
# producción — una cada vez, y leer la salida
docker compose --env-file .env.production -f docker-compose.yml exec -T postgres \
  psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 -f /migrations/023_inventario.sql
```

(Ajustar la ruta al montaje real de `migrations/` en el contenedor de prod; en staging se
ejecutaron el 2026-09-28 y el 2026-10-08.)

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
generación 0), y las actas bajo `checkbiz/reports/entities/{e}/acta_{challengeId}.pdf`. Ninguna
regla de retención debe borrarlas: son la prueba. Conviene activar en el bucket la
**retención** (o al menos el versionado) de `signatures/`, que hoy no está en ningún entorno.

### 5.4 Colecciones que se crean solas

`signing_keys/{employeeId}/keys`, `signing_challenges`, `entities/{e}/inventory_notices`, y
bajo cada entidad con el módulo: `items`, `warehouses`, `item_units`, `stock`, `movements`,
`unit_reservations`, `unit_assignments`, `task_materials`. `documents` gana campos
(`itemId`, `unitId`, `linkedItemIds`, `linkedUnitIds`, `contentSha256`, `metadata.result`) sin
migrar nada: los anteriores no los tienen y el código lo contempla.

### 5.5 Por cada entidad que active el inventario

```bash
node services/inventory/dist/scripts/reindex-search.js --entity <entityId> --apply
node services/inventory/dist/scripts/mirror-dimensions.js --entity <entityId> --apply
```

Solo hacen falta para datos que existieran antes del código que los indexa y espeja (en prod,
ninguno): se anotan por si se importa un catálogo a mano.

## 6. Stripe (cuenta en vivo)

- **Precio del plan `standard` del inventario**: 29 €/mes hasta 50 empleados + 0,75 € por cada
  empleado a partir del 51, como precio **graduado por cantidad** sobre el producto nuevo
  «Inventario» (inventario 06 §D2). El `price_live_…` resultante va a §5.2.
- **Webhook**: el endpoint de prod apunta a `billing:3011` desde el 2026-09-04. Comprobar que
  tiene los 8 eventos, en particular `invoice.upcoming` y `customer.subscription.trial_will_end`
  (son los que ponen la cantidad = plantilla antes de cobrar; sin ellos la primera factura del
  inventario saldría a 0 €, ver memoria «cobro al fin de la prueba»). **Sin comprobar en prod.**
- `GetCountPayPerUse` ya cuenta plantilla para `inventory` igual que para `checkinbiz`.

## 7. Servicios que cambian (ya desplegados por CI al fusionar `staging → main`)

| Servicio | Qué entra |
|---|---|
| `inventory` | **nuevo** (§1–§3) |
| `reports` | material en el informe de tareas (TDR-005); `POST /api/reports/equipment` (Excel, 2 hojas; 402 sin add-on); `GET /api/reports/inventory/consumption` |
| `documents` | ámbitos `item`/`unit`, 8 tipos nuevos, `POST/DELETE /:id/links`, `contentSha256`, acuse firmado y `GET /:id/signing-subject` |
| `checkinbiz` | `POST /auth/signing-keys`, `POST /auth/signing-challenges` |
| `shared` | inventario, cumplimiento de papeles, firma, `internalSubscribers`, avisos `unit_*` |
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
| `NEXT_BACKEND_URI_CHECKINBIZ_SIGNING_CA` | `https://api.checkbiz360.com/api/v1/checkinbiz/auth/signing-ca.crt` |

Sin la primera, toda la sección Inventario responde «el proxy rechazó la llamada»; sin las dos
siguientes, los dos informes nuevos fallan al generar; sin la cuarta, «Descargar el acta de firma»
en la ficha del documento no funciona; sin la quinta, no se descarga el certificado de la CA desde
«Entorno de trabajo». Vercel solo tiene producción: no se tocan para
probar.

### 8.2 Promoción

`develop` del panel lleva (al 2026-10-09) **11 commits sin empujar** —los de la ficha rediseñada,
la página de alta y los documentos de la entrega—; la cadena es `develop → staging → main`,
y el `main` lo fusiona y redespliega Jose en Vercel. Revisar antes que `main` no tenga hotfixes
que `develop` no tenga (pasó en septiembre).

## 9. App móvil (`checkbiz360`)

Lo lleva otra sesión. Para prod hace falta **una versión nueva publicada** (no sale de `master`,
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

## 9c. Aceptación antes de subir

No se fusiona `staging → main` hasta pasar en staging el guion
[Qa/manuales/2026-10-firma-documentos-inventario-e2e.md](../Qa/manuales/2026-10-firma-documentos-inventario-e2e.md)
(panel → app → perito → informes → inventario → consumo → avisos) con la versión de la app que
se va a publicar. Tras el pase se repiten allí los pasos 1, 2 y 7 con una empresa piloto.

## 10. Orden de ejecución el día del pase

1. Migraciones 023 y 024 (§4), una a una.
2. `.env.production`: `INVENTORY_INTERNAL_URL` y, si se quiere, las de §3.2.
3. `docker-compose.yml` y `nginx/nginx.conf` (§1, §2) **commiteados en el PR** `staging → main`;
   fusionar; el `deploy.yml` levanta el contenedor y reinicia nginx.
4. Comprobar: `docker compose … ps` (16 → 17 contenedores `healthy`, `inventory` entre ellos) y
   `curl https://api.checkbiz360.com/api/v1/inventory/access?entityId=…` con un token de prod
   → 403 `inventory/not_subscribed` (no 502).
5. Índices de `items` (§5.1).
6. Reglas de Firestore (§5.3), con la copia del ruleset anterior guardada antes.
7. Stripe: precio en vivo (§6) y `alta-servicio.js --stripe-price … --apply` (§5.2).
8. Vercel: las tres claves (§8.1) y el PR del panel (§8.2).
9. Primera entidad: contratar desde Suscripciones; comprobar que nace `active` con 15 días de
   prueba y `quantity` = plantilla; abrir Existencias (índices), subir una entrada, generar el
   informe «Equipos y EPIs» (402 sin add-on, Excel con add-on).
10. App: cuando haya versión publicada (§9), un registro de clave real y un acuse firmado.

**Rollback:** el inventario es aditivo (quitar el bloque del compose y las rutas devuelve el
estado anterior; las tablas pueden quedarse). Reglas: redesplegar la copia guardada en §5.3.
Precio de Stripe: archivarlo deja el plan no contratable sin tocar código.

## 11. Registro de lo ejecutado

_(vacío: se rellena el día del pase)_

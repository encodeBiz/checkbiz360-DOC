# Próximo pase a producción — API (documento vivo)

**Abierto:** 2026-10-16 · **Ejecutado:** 2026-10-17, de 10:40 a 11:31 UTC, por Claude con la
orden de Jose («hoy es el pase, encárgate de todo»). Registro al final.
**Estado:** EJECUTADO en todo lo que depende del servidor, de Firebase, de Vercel y del panel
(§1 a §6 y §8). Queda lo que necesita a Jose con sesión real (2.17, 3.5 y 3.6, 8.6), la app
(1.11 y 1.12), el manual (3.7, 2.18), las TTL opcionales (2.11) y las §7 y §9, que no tienen
código todavía. Cada fila de los guiones dice «HECHO 17-oct» o por qué no.
**Regla del documento:** cada cosa que entra en `staging` y necesita algo fuera del código
(migración, índice, variable, servicio, regla, función, dato) se apunta aquí **el mismo día**,
como pendiente. El día del pase se ejecuta de arriba abajo y cada fila se marca con hora,
quién y lo que se vio, como en el registro de octubre
([2026-10-inventario-firma-back.md](./2026-10-inventario-firma-back.md)).

Producción no se toca fuera de ese día. Todo con `--project encodebiz-services` explícito y
con autorización de Jose paso a paso.

---

## 0. Lo que hay en `staging` y no en `main`

Inventario por `git log --first-parent origin/main..origin/develop` del 2026-10-16. **Ojo:**
parte del CRM entró en producción el 14-oct por un PR propio (#147, migraciones 031-033), así
que esta lista sobrecuenta: antes del pase hay que cruzarla con lo que corre de verdad.

| Rama | Qué | Necesita fuera del código | Sección |
|---|---|---|---|
| `feat/horario-por-tareas*`, `fix/horario-por-tareas-*` y otras sesiones (D11, importación) | Horario por tareas, fases 1 y 2, D11 | migraciones 037 y 040, dos índices, `onTaskDay` y `weeklyFromTaskDays`, reglas, panel y app | §1 |
| `feat/conector-asistente`, `feat/importacion-plantilla` | Conector de Claude y ChatGPT (fases 1 y 2, tandas) y alta por plantilla; sin cupo | servicios `assistant` y **`branches`** nuevos en prod, nginx, secretos, dominio en Firebase Auth, reglas, dos variables en Vercel | §2 |
| `feat/cuadrantes-plantilla` | Cuadrante por plantilla de sucursal y de persona; el Excel de otros programas; el horario propio al aprobar; reglas que cierran las subcolecciones | nginx (`client_max_body_size`), reglas, panel, manual | §3 |
| `fix/buscador-varias-palabras` (panel) | Los buscadores del índice encuentran con varias palabras («maria campo») | nada: solo panel | §3 |
| `feat/material-por-destino` | Material hacia tarea, persona o sucursal | migración 034 | §4 |
| `feat/calendario-tareas-resumen` | Calendario semanal de tareas resumido en Postgres (ADR-008) | migración 040, un índice | §8 |
| `fix/reglas-collection-group` | Consultas de grupo | **ya en prod desde el 14-oct**; falta que `main` tenga el fichero | §5 |
| `feat/reglas-paso-2a` | Reglas: cada sesión ve sólo las entidades de las que es miembro | función `onEmpMember` (antes que las reglas), reconciliación en `checkinbiz`, reglas | §10 |
| `feat/almacenamiento-cobro` (API) y `feat/almacenamiento-panel` (front) | Almacenamiento por empresa: trigger que cuenta, exceso de 2 GB a 0,25 €, interruptor, bloqueo del documental, aviso al 90 % | triggers, carga inicial, Price, variable, webhook, Vercel | §11 |
| `feat/quiosco` y sus `fix/quiosco-*`, `feat/quiosco-*`, `feat/cuota-quiosco-y-almacenamiento` | Punto de fichaje (quiosco) | `KIOSK_SECRET`, reglas, ciclo de vida, Price y alta, Vercel, panel y app | §12 |
| `feat/avisos-por-correo` | Avisos de trabajo por correo con casilla por persona; `task_removed`; reglas que cierran almacenamiento | reglas, índice de grupo, 2 functions | §13 |
| CRM (`feat/sales-crm*`, `feat/crm-*`, `feat/backoffice-crm`) | CRM comercial | **sin inventariar**: cruzar con #147 | — |
| `feat/mi-material-aviso-e-historial`, `fix/avisos-*`, `fix/backfill-account-kind`, `fix/backoffice-sucursales-direccion` | Avisos, idioma, material, backoffice | **sin inventariar** | — |

> Lo marcado «sin inventariar» no significa que no necesite nada: significa que nadie lo ha
> mirado todavía para este documento.

---

## 1. Horario por tareas (fases 1 a 4, selector del panel, D11) — EJECUTADO el 2026-10-17 (API, funciones y panel); la app, pendiente

Diseño: `DOCS/ingenieria/horario-por-tareas` (README D1–D11, TDR-001, TDR-002, TDR-003). En
staging desde el 2026-10-16, QA `54-horario-por-tareas` 15/15 contra staging. Nadie está en el
modo hasta que alguien lo active, así que subirlo no cambia nada a ningún cliente; **activarlo a
alguien en producción exige antes la app publicada** (1.12).

Lo que sube, para tenerlo delante:

| Pieza | Dónde | Lo hizo |
|---|---|---|
| Modo por empleado, días generados, reglas D4, resolutor, disponibilidad | `shared`, `checkinbiz`, `tasks`, `analytics` | fase 1, solo empleado (16-oct) |
| El fichaje mueve la tarea; descanso real en el informe | `checkinbiz`, `tasks`, `reports` | fase 2 |
| Jornada y huecos entre turnos en el informe (PDF y Excel) | `reports` | fase 4 |
| Alarmas por tarea; el aviso de tarea no iniciada no va a quien está en el modo | `shared`, `firebase_sdk`, `checkinbiz` | fase 3 |
| `onTaskDay` (regenera días; sale si la escritura no cambia el día; copia la semana, D11) | `firebase_sdk` | fases 1–2 y otra sesión (D11) |
| `weeklyFromTaskDays` (copia la semana activa a las 03:00 y 15:00 de Madrid) | `firebase_sdk` | otra sesión (D11) |
| Modo de cada persona en la importación por plantilla | `employees` (`horario.ts`, `importacion.ts`) | otra sesión |
| Cuadrante: en el modo solo crea tareas (D10) | `merlin` (`cuadrantes/application/aplicar.ts`) | sesión de cuadrantes, hecho y probado en staging el 16-oct (§3) |
| Selector «Horario semanal / por tareas» en la ficha del empleado | panel | TDR-002 |
| Fichar mueve la tarea, tarea del turno bajo los botones, avisos | app | TDR-003 §8 |

### Guion, en orden

| # | Paso | Cómo | Estado |
|---|---|---|---|
| 1.2 | Índices en prod, solo con `gcloud` | `gcloud firestore indexes composite list --project encodebiz-services` y crear solo los que falten con `gcloud firestore indexes composite create … --project encodebiz-services`: `tasks` colección `assignedEmployeeIds` CONTAINS + `scheduledStartAt` ASC y `calendar_days` grupo de colecciones `entityId` ASC + `date` ASC. Esperar a `READY` antes de 1.6. No hay fichero de índices que actualizar: el SaaS está retirado y `encodebiz-api` no declara índices en su `firebase.json`, así que ningún despliegue los poda | HECHO 17-oct, ver registro |
| 1.3 | Migración 037 | A mano, sola y leyendo la salida: `… exec -T postgres psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 < migrations/037_horario_por_tareas.sql`. Esperado: `ALTER TABLE`, `CREATE TABLE`, `CREATE INDEX`, `ALTER TABLE`, `ALTER TABLE`. **Antes** de que corra el job `dimensiones` con el código nuevo (minuto 20 de cada hora), o su `INSERT` con `schedule_mode` falla y queda en `dim_sync_log` | HECHO 17-oct, ver registro |
| 1.4 | Migración 040 (otra sesión: índice del calendario semanal de tareas) | Igual que 1.3, con `040_tareas_calendario.sql`. Esperado: `CREATE INDEX` | HECHO 17-oct, ver registro |
| 1.5 | Reglas de Firestore | Con el fichero de `main` ya fusionado (§5): `calendar_days` en `soloServidor`. Guardar antes el ruleset vivo | HECHO 17-oct, ver registro |
| 1.6 | Contenedores | Los despliega el workflow al fusionar `staging → main`: `checkinbiz`, `tasks`, `reports`, `analytics`, `employees`, `merlin` con el código nuevo. **Nunca a mano en prod** | HECHO 17-oct, ver registro |
| 1.7 | Entorno de prod | Comprobar que `checkinbiz` y `employees` reciben `ENCODEBIZ_API_KEY` (los dos llaman a otros servicios con la clave S2S). `TASKS_INTERNAL_URL`, `CHECKINBIZ_INTERNAL_URL` y `BRANCHES_INTERNAL_URL` tienen valor por defecto en el código (`http://tasks:3006`, `http://checkinbiz:3002`, `http://branches:3014`) y valen en prod: no hay que añadirlas. **Corregido el 17-oct:** `branches` no corre en prod hasta que lo arranque §2.2; sin él, lo que llama a `branches:3014` falla | HECHO 17-oct, ver registro |
| 1.8 | Funciones de Firebase | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo <nombre>` con cada una: `onTaskDay`, `weeklyFromTaskDays` y, por la fase 3 (TDR-005), `employeePlanifierWorker`, `planifierNotificationWorker` y `taskStartNotificationWorker`. Nunca el codebase entero (README de `firebase_sdk`). Las tres de la fase 3 cambian también para quien NO está en el modo solo en que el job de las 04:00 salta a quien sí lo está | HECHO 17-oct, ver registro |
| 1.9 | Comprobación de la API | `firebase functions:list --project encodebiz-services` con las dos; `\d dim_calendar_days` en prod; `GET /calendar` de cualquier empleado devuelve `scheduleMode: "weekly"`; `PATCH /calendar` con `scope: "branch"` y `scheduleMode: "tasks"` responde 400 `calendar/schedule_mode_employee_only` | HECHO 17-oct, ver registro |
| 1.10 | Panel | `encodebiz-front-saas`: `develop → main` y promoción en Vercel. Sin variables nuevas. El selector está solo en la ficha del empleado, al apagar «Usar horario base» | HECHO 17-oct, ver registro |
| 1.11 | App | `checkbiz360`: `develop` con la fase 2 → versión nueva publicada en las dos tiendas | PENDIENTE: el 17-oct `master` y `staging` siguen en 1.7.0+57 y `develop` en 1.8.0+61 con la fase 2 y el material; falta promover y subir a las tiendas |
| 1.12 | **No activar el modo a nadie en prod** hasta que 1.11 esté publicada y la persona la tenga instalada | Con una app vieja la persona vería los botones de la tarea y la jornada en blanco | SIGUE EN PIE hasta 1.11 |

> **Staging se desplegó a mano el 16-oct** (merge con `[skip ci]`, `git pull` y
> `up --build -d checkinbiz tasks reports` en el servidor, por indicación de Jose). Para
> producción no vale: va por `staging → main` y su workflow (1.6).

---

## 2. Conector de Claude y ChatGPT y alta por plantilla — EJECUTADO el 2026-10-17; quedan 2.11 (opcional), 2.17 y 2.18

**Detallado el 2026-10-17.** Jose lo da por probado para una primera versión: conectado de
punta a punta con ChatGPT web y con Claude en staging, sobre la empresa de demo (Álvarez), con
las 22 herramientas, el alta masiva y el cuadrante por tandas.

Diseño: [conector-asistente](../ingenieria/conector-asistente/README.md) (ADR-001 a ADR-007,
TDR-001 y TDR-002) y [alta-por-plantilla](../ingenieria/alta-por-plantilla/README.md)
(TDR-001). Van juntos porque el alta masiva del asistente es el lote de la plantilla, y las
dos crean sucursales por el mismo contenedor.

> **2026-10-18, cuarta:** la confirmación de las herramientas de escritura del conector pasa a ser un `confirmacionId` firmado que devuelve la vista previa, con espera mínima de cinco segundos y caducidad de quince minutos (TDR-002 §9); los lotes tampoco se confirman en el acto. Lo detectó Jose probando los casos negativos del directorio de ChatGPT. Nada fuera del código. Las páginas legales del panel (`/legal/privacy-policy`, `/legal/terms-and-conditions`) se renderizan ya en el servidor e indexables, para la evaluación automática de la política de privacidad de OpenAI (panel, `release/legales-ssr`, Vercel).

> **2026-10-18, tercera:** la ruta de verificación de dominio del directorio de apps de ChatGPT (`/.well-known/openai-apps-challenge`, sirve `OPENAI_APPS_CHALLENGE` en texto plano; sin variable, 404) y el paquete del plugin en `encodebiz-api/plugins/checkbiz360`. **HECHO el 18-oct:** `OPENAI_APPS_CHALLENGE` puesto en el entorno de producción (copia previa `.env.production.bak-2026-10-18-*`), `assistant` recreado y nginx reiniciado; `curl` devuelve el token exacto en `text/plain`. Queda pulsar «Verificar» y «Escanear herramientas» en el portal. **Decidido por Jose el 18-oct:** cuenta de revisión `openia@encodebiz.com`, admin de Encodebiz, exenta del segundo factor por `ASSISTANT_REVIEW_UIDS` (en el conector desde el PR de ese día; sin la variable, nadie está exento). **HECHO el 18-oct (PR #169 + cuenta creada por script en el contenedor, con autorización expresa de Jose tras un primer bloqueo del control de seguridad de la sesión):** cuenta en Auth (uid `FnqTSYJmRLYPMIZp6ULYUzn6RqJ2`), ficha `users`, asiento admin en Encodebiz (`support: false`), `ASSISTANT_REVIEW_UIDS` en el entorno de producción (copia previa `.env.production.bak-2026-10-18`), credenciales en `encodebiz-api/secrets/openai-review-account.md`. **Verificado en prod** recorriendo el flujo como ChatGPT (cliente CIMD de chatgpt.com): sesión → consentimiento directo con «Encodebiz», código, canje, `listar_empresas` → Encodebiz/admin, `ver_hoy` → 3 sucursales, revocación → 401. Queda: subir el ZIP, el token de verificación de dominio, y dar al revisor las credenciales por el portal.

> **2026-10-18, segunda:** las estadísticas para el asistente (TDR-003 §9: `ver_estadistica` con las 19 métricas de `/panel/stats`, `estadisticas_sucursal` y `estadisticas_persona` desde el patrón de Firestore) en producción con el PR #167 (`13ffb76`), directo. Nada fuera del código.

> **2026-10-18:** el análisis entero para el asistente (TDR-003 §8: `ver_mes`, `analisis_sucursal`, `analisis_persona`, `trayectoria`, `ver_plantilla`; puertas delegadas de heurística y patrones en `analytics`) en producción con el PR #165 (`6c646d1`), directo y sin parada en staging a petición de Jose; sondas: las dos puertas nuevas responden 403 a un actor inexistente. Lección: un PR a producción sale de la rama principal o de una base contenida en ella, nunca de `develop` (el #164 llegó con conflictos por arrastrar otras sesiones).

> **En producción el 2026-10-17, ~16:45 UTC** (PR #163, `461f3fb`, *Production CI/CD* en verde): fase 3 (gestor operativo), multiempresa (ADR-009, URL personal `/api/v1/assistant/mcp`) y corte de sesiones (baja o desactivación de colaborador en `checkinbiz`; corte desde el panel por empresa). Sondas: metadatos de la URL personal 200, MCP personal y por empresa 401 sin token, `/connections?entityId=` 401 sin token, puerta delegada de `analytics` 403 a una cuenta inexistente. Antes, a petición de Jose, se revocó la única conexión viva de prod (Claude de hola@encodebiz.com). **El panel no ha subido** (Jose: «olvida el panel»): el apartado «Conexiones» y las sesiones en la ficha del colaborador están solo en `develop` del panel (`730185ef`).

### Lo que sube

| Pieza | Dónde | En staging desde |
|---|---|---|
| Servidor de autorización OAuth 2.1 (PKCE, CIMD, `private_key_jwt` de ChatGPT), pantalla de consentimiento con el login y el 2FA del panel, MCP por empresa en `/mcp/e/{entityId}` | `services/assistant` (nuevo, 3017) | 15-oct (fase 1) |
| 22 herramientas: lectura, cuadrante por tandas, cambios de tareas, horario y modo, altas sueltas y masivas, bienvenidas | `services/assistant` | 16-oct (fase 2); tandas, 16-oct (ADR-007) |
| Persona delegada: la clave S2S más `x-actor-uid` con los permisos de esa persona (ADR-005) | `shared` (`requireDelegatedUser`), montada en `tasks`, `checkinbiz` (calendario), `employees` y `branches` | 16-oct |
| Cuadrante desde filas, Excel rellenado por el servidor, retirada de lo que ya no está (ADR-006), tandas con `loteId` | `merlin` (`soporte/cuadrantes`) | 16-oct |
| Alta por plantilla: plantilla en cinco idiomas, propuesta que no escribe, aplicación en segundo plano, ocupaciones del catálogo, modo de horario, bienvenida aparte | `employees` (`/import`, `/welcome`, `/delegated/*`) | 16-oct |
| Fase 3, el gestor operativo: `ver_hoy`, `ver_alertas`, `ver_disponibilidad`, `ver_disponibilidad_dia`, `quien_puede_cubrir`, `ver_semanas`, `ver_costes`, `informe_jornada` (ADR-008, TDR-003) | `services/assistant`; puerta delegada nueva en `analytics` (`/api/analytics/delegated/panel`) y en `reports` (`POST /api/reports/delegated/generate`) | 17-oct |
| Sin cupo: `canCreateBranch` y `canCreateEmployee` solo exigen suscripción activa o en prueba | `shared` (`checkbiz/plan/subscriptionLimits.ts`) | 16-oct |
| Panel: la dirección del conector y el paso a paso en «Entorno de trabajo»; el diálogo «Importar plantilla» en empleados y sucursales | `encodebiz-front-saas`, solo en `develop` | — |

**Cambio visible para los clientes:** con el «sin cupo», un alta de empleado o de sucursal que
hoy `checkinbiz` rechaza por el límite del plan pasará a entrar (decisión de Jose, 16-oct). El
tope de diez empleados que aplica el **panel** en el plan gratuito sigue ahí y queda
incoherente con la regla: decisión aparte, no bloquea el pase.

### Depende de otras secciones

- **§1 (horario por tareas):** `cambiar_modo_horario` y la columna «Horario» de la plantilla
  escriben por la ruta delegada del calendario de `checkinbiz`, que es de §1.
- **§3 (cuadrantes por plantilla):** las herramientas del cuadrante son el lote de §3.
- **§5 (reglas):** `assistant_.*` y `staff_imports` ya están en `soloServidor` del
  `firestore.rules` de staging. Van en el despliegue único de §5, no en uno propio.

Orden: §1 y §3 antes que este. Si §1 se aplaza, el conector puede subir igual: la herramienta
del modo y la columna «Horario» fallarán con un error legible, y el resto funciona.

### 🔴 Lo que no estaba apuntado: el contenedor `branches` no existe en producción

El código de `services/branches` está en `main` desde el 8-sep (salida del monolito, fase 2),
pero `docker-compose.yml` de producción **no lo arranca**. En prod las sucursales del panel
siguen en Firebase. El conector (`crear_sucursal`, el alta masiva) y la importación por
plantilla crean sucursales por `http://branches:3014/api/v1/branches/delegated`. Sin el
contenedor, esa llamada falla y la persona ve el error de la herramienta.

Decisión para este pase: **arrancar `branches` solo en la red interna**, sin ruta en nginx. El
panel sigue creando sucursales por Firebase como hoy. Abrir `/api/v1/branches/` al público es
el corte de la fase 2 de la salida del monolito y **no** entra aquí. Lo mismo con `entities`,
que este pase no necesita.

### Guion, en orden

| # | Paso | Cómo | Estado |
|---|---|---|---|
| 2.1 | Código | Entra con el despliegue normal (`staging → main`, action *CI/CD*). Comprobar antes en el PR que `main` recibe `services/assistant`, los cambios de `merlin`, `employees`, `branches`, `tasks`, `checkinbiz` y `shared`, y `5c38f5e` (las tandas) | HECHO 17-oct, ver registro |
| 2.2 | `docker-compose.yml` de prod: `branches` | Bloque calcado de `docker-compose.staging.yml` (`<<: *service`, `PORT=3014`, `expose: 3014`, healthcheck a `/health`), **sin** `ports:`. Va en el mismo PR que 2.1 | HECHO 17-oct, ver registro |
| 2.3 | `docker-compose.yml` de prod: `assistant` | Calcado del de staging con `ASSISTANT_PUBLIC_URL=https://api.checkbiz360.com/api/v1/assistant` y `ASSISTANT_CLIENT_HOSTS=claude.ai,claude.com,chatgpt.com,openai.com`. Las `*_INTERNAL_URL` (checkinbiz, tasks, merlin, employees, branches) tienen el valor por defecto correcto; ponerlas igual que en staging para que se lean. **Nunca** `ASSISTANT_ALLOW_LOCALHOST`. Mismo PR | HECHO 17-oct, ver registro |
| 2.4 | `employees` en prod: `BRANCHES_INTERNAL_URL=http://branches:3014` | En el bloque `employees` de `docker-compose.yml`, como en staging (el código ya lo tiene por defecto; se pone para que se vea). Mismo PR | HECHO 17-oct, ver registro |
| 2.5 | `nginx/nginx.conf` de prod: el conector | `upstream assistant_service { server assistant:3017; }` (hoy **no** está, contra lo que decía este documento); `location = /api/v1/assistant`; `location ^~ /.well-known/oauth-authorization-server` y `location ^~ /.well-known/oauth-protected-resource` hacia `assistant_service`; `location /api/v1/assistant/` con `client_max_body_size 4m` (ADR-007). Todo como en `nginx.staging.conf`. Mismo PR | HECHO 17-oct, ver registro |
| 2.6 | `nginx/nginx.conf` de prod: la importación | Hoy prod abre solo `/api/v1/employees/teams`, y a propósito (el comentario lo explica). Abrir **solo** `location /api/v1/employees/import/` y `location = /api/v1/employees/import` con `client_max_body_size 4m`, y `location = /api/v1/employees/welcome`. **No** abrir el prefijo entero: el alta, la edición y la baja de producción siguen en Firebase. Las rutas `/delegated/*` no se abren: son internas del conector. Mismo PR | HECHO 17-oct, ver registro |
| 2.7 | `.env.production` | `ASSISTANT_COOKIE_SECRET` (32 bytes nuevos, `openssl rand -base64 32`, **distinto** del de staging) y la config web de Firebase de **`encodebiz-services`**: `ASSISTANT_FIREBASE_API_KEY`, `_AUTH_DOMAIN`, `_PROJECT_ID`, `_APP_ID` (de la consola de Firebase, app web del panel; `vercel env pull` las devuelve vacías). Copia antes: `cp .env.production .env.production.bak-$(date +%F)`. Sin estas variables el servicio arranca con la autorización apagada y lo avisa en el log | HECHO 17-oct, ver registro |
| 2.8 | Firebase Auth de prod: dominio autorizado | Añadir `api.checkbiz360.com` a los dominios autorizados de `encodebiz-services`. Como en dev el 16-oct: leer primero la lista (`GET` de la config de Identity Toolkit admin v2) y hacer `PATCH … ?updateMask=authorizedDomains` con **la lista entera más el dominio**, nunca solo el nuevo. O desde la consola. Sin esto, la pantalla de consentimiento no deja entrar | HECHO 17-oct, ver registro |
| 2.9 | Reglas | En el despliegue único de §5. Comprobar que el fichero que sale lleva `assistant_.*` y `staff_imports` en `soloServidor` | HECHO 17-oct, ver registro |
| 2.9b | Fase 3: nada fuera del código | Las puertas delegadas de `analytics` y `reports` son internas: **sin** rutas en nginx. El conector las llama por `http://analytics:3004` y `http://reports:3005`, que son los valores por defecto del código; en el compose de prod basta con ponerlas en el bloque `assistant` para que se lean (`ANALYTICS_INTERNAL_URL`, `REPORTS_INTERNAL_URL`). `analytics` y `reports` se reconstruyen con el despliegue normal | PENDIENTE |
| 2.10 | Índices | **Ninguno.** Las consultas del conector y de la importación son de igualdad y van con los índices de campo (TDR-001 §16) | — |
| 2.11 | TTL (opcional) | Política TTL sobre `expiresAt` en `assistant_auth_requests` y `assistant_tokens`. Mientras no esté, el servicio barre lo vencido al escribir | OPCIONAL, no hecho el 17-oct |
| 2.12 | Arranque | Tras el deploy: `docker compose -p encodebiz-api --env-file .env.production -f docker-compose.yml ps assistant branches employees merlin` → los cuatro `healthy`. Reiniciar nginx (el action lo hace; a mano, `restart nginx`). Log de `assistant` **sin** «la autorización está apagada» | HECHO 17-oct, ver registro |
| 2.13 | Sondas sin sesión | `curl -s -o /dev/null -w '%{http_code}' https://api.checkbiz360.com/.well-known/oauth-authorization-server` → `200`; `…/.well-known/oauth-protected-resource/api/v1/assistant/mcp/e/<entityId>` → `200`; `curl -s -X POST https://api.checkbiz360.com/api/v1/assistant/mcp/e/<entityId>` → `401` con cabecera `WWW-Authenticate`. `GET https://api.checkbiz360.com/api/v1/employees/import/template` sin token → `401`, **no** `404` (el `404` es nginx sin la ruta de 2.6) | HECHO 17-oct, ver registro |
| 2.14 | `branches` desde dentro | `docker compose … exec -T employees wget -qO- http://branches:3014/health` → responde. Si no, el alta de sucursales del conector y de la plantilla fallará | HECHO 17-oct, ver registro |
| 2.15 | Panel: variables en Vercel (producción) | `NEXT_PUBLIC_ASSISTANT_CONNECTOR_BASE=https://api.checkbiz360.com/api/v1/assistant` y `NEXT_BACKEND_URI_STAFF_IMPORT_HANDLER=https://api.checkbiz360.com/api/v1/employees`. **Antes** del despliegue del panel: la primera es pública y se compila dentro | HECHO 17-oct, ver registro |
| 2.16 | Panel: código | `develop → staging → main` del panel **después** de 2.12. Hoy `staging` del panel no tiene ni la sección del conector (`94d39ab6`) ni el diálogo de importación (`24440960`, `5d285adc` y anteriores). Ojo: `develop` del panel lleva también el calendario de §8 y otras sesiones. Se sube junto, en el orden de §8.5 | HECHO 17-oct, ver registro |
| 2.17 | Prueba con sesión real (con Jose) | En una empresa de prueba de producción, nunca en la de un cliente: (a) Entorno de trabajo → copiar la dirección del conector; (b) en Claude y en ChatGPT web, añadir el conector, entrar con la cuenta del panel y el 2FA, aceptar; (c) `conexion_actual`, `listar_sucursales`, `ver_semana`; (d) `proponer_cuadrante` de una persona **sin confirmar**, abrir el enlace del Excel y descartar; (e) en el panel, «Importar plantilla» con dos personas y una sucursal: proponer, confirmar, comprobar que aparecen en el buscador; (f) en el panel, revocar la conexión y comprobar que el asistente pierde el acceso | PENDIENTE: Jose, con sesión real (la infraestructura está sondeada, ver registro) |
| 2.17b | Prueba de la fase 3 (con Jose) | En la misma empresa de prueba: «¿cómo va hoy?» (`ver_alertas`, `ver_hoy`), «¿quién puede cubrir esta tarea?» sobre una tarea de hoy, y un `informe_jornada` corto. El informe queda en el histórico de informes del panel: hacerlo en la empresa de prueba | PENDIENTE |
| 2.18 | Instrucciones para clientes | El texto para el proyecto de ChatGPT (17-oct, en la conversación con Jose) va al manual de clientes antes de anunciarlo | PENDIENTE: manual |

### ✅ Hallazgo de seguridad al margen del pase: Merlin sin control de empresa — RESUELTO el 17-oct

**Arreglado en producción el 2026-10-17 a las 15:30 UTC** (PR #161, `cdfb499`, action *Production CI/CD* en verde). Las dos rutas exigen pertenecer a la empresa (`requireEntityMember`: asiento o ficha de empleado). Probado antes en staging con sesiones reales: una cuenta ajena y una owner pidiendo otra empresa reciben 403. Comprobado después en el contenedor de prod. También en `develop` y `staging`. Lo que sigue es el texto original del hallazgo.


Visto el 17-oct al diseñar la fase 3 (ADR-008, Consecuencias). `POST /api/v1/gpt/panel` y
`POST /api/v1/gpt/interpret` de `merlin` exigen sesión de Firebase, pero **no comprueban que
quien pide pertenezca a la empresa**. Cualquier cuenta con sesión obtiene el relato del panel
o la interpretación de patrones de otra empresa si conoce su `entityId`. **Afecta a
producción hoy**, con o sin este pase. No se ha tocado: antes hay que saber si la app llama a
`interpret` con `audience: "employee"` para la propia persona, porque un control de owner o
admin la rompería. Decisión de Jose.

### Si algo falla

Todo es aditivo y nada de lo existente depende de ello:

- **Conector:** parar el contenedor (`… stop assistant`). Las conexiones quedan en Firestore, pero
  sin servicio no hay acceso. Revocar en bloque, si hiciera falta, es borrar
  `assistant_tokens`. No hay migraciones que deshacer.
- **Importación:** quitar las rutas de 2.6 y reiniciar nginx. El panel enseña el error en el
  diálogo y nada más cambia.
- **`branches`:** pararlo deja sin alta de sucursales al conector y a la plantilla. El panel no se entera.
- **Sin cupo:** es código de `shared`. Volver atrás es un revert de ese fichero, no un dato.

---

## 3. Cuadrantes por plantilla — EJECUTADO el 2026-10-17; quedan 3.5, 3.6 y 3.7

Diseño: [cuadrantes/tdr/TDR-001](../ingenieria/cuadrantes/tdr/TDR-001-importacion-por-plantilla-de-sucursal.md).
Detalle, pruebas y decisiones: [2026-10-cuadrantes-plantilla.md](./2026-10-cuadrantes-plantilla.md).
En `staging` de la API desde el 2026-10-15 y en `develop` del panel; probado por Jose en staging
el 16-oct con su panel local (§7b de ese registro).

**Qué cambia para el cliente.** En la ficha de la sucursal, «Importar cuadrante»: una plantilla
de Excel con una pestaña por persona, una subida para toda la plantilla, revisión por persona y
confirmar. En la ficha del empleado, además del documento de su programa, «Descargar plantilla»
con solo su pestaña. Y todos los buscadores del panel encuentran con varias palabras.

**Qué no necesita.** Ni contenedor, ni variable, ni migración, ni índice, ni clave de Vercel
(todo va por `cuadrantes_handler`, en uso en prod desde el 20-sep). Las colecciones nuevas
(`cuadrante_lotes`) se crean solas.

**Lo que puede fallar y qué se vería.**

- *Sin el `client_max_body_size 4m`* nginx corta en un mega: un Excel de más de unos 750 KB llega
  como 413 y el panel dice «No se ha podido leer». Va en `nginx/nginx.conf` de `develop`; llega con
  el merge y el `deploy.yml` reinicia nginx.
- *Sin las reglas corregidas* (§5) las propuestas y los lotes, con nombres y domicilios de las
  personas atendidas, se pueden leer desde el navegador. Hoy ya pasa en prod con las propuestas
  (existen desde el 20-sep) por el comodín de lectura: lo cierra la §6 y lo remata la §5.
- *Un Excel guardado con otro programa* que no sea Excel ya no falla (se normaliza al abrir).
- *Personas en «Horario por tareas»*: el cuadrante solo crea tareas y la plantilla la copia
  `weeklyFromTaskDays`; depende de la §1.8. Sin esas funciones, la importación funciona igual pero
  la semana de esas personas no se ve en la app hasta que estén.

| # | Paso | Cómo | Estado |
|---|---|---|---|
| 3.1 | Código de la API | Llega con `staging → main` (§1.6): solo `merlin` cambia por esto. Sonda sin token: `curl -s -o /dev/null -w "%{http_code}" "https://api.checkbiz360.com/api/v1/gpt/cuadrantes/plantilla?entityId=x&branchId=y"` → **401** (un 404 es contenedor viejo; 502, nginx con IPs viejas) | HECHO 17-oct, ver registro |
| 3.2 | nginx | Comprobar en el servidor que el fichero desplegado lleva el límite: `grep -n -A2 "location /api/v1/gpt/ {" /opt/encodebiz-api/nginx/nginx.conf` → `client_max_body_size 4m;` | HECHO 17-oct, ver registro |
| 3.3 | Reglas | En el único despliegue de la §5 (o en el de la §6 si va antes, con el fichero de `develop`). Comprobación propia, sin sesión, con una entidad que no exista: `GET …/documents/entities/zz-prueba/cuadrante_proposals/x` y `…/cuadrante_lotes/x` → **403**; `…/entities/zz-prueba/calendar/x` → 404 (permitido y no existe) | HECHO 17-oct, ver registro |
| 3.4 | Panel | Con el resto del panel (§1.10 y §8.5): entran el modal de la sucursal, la plantilla desde la ficha del empleado, la ruta del proxy (`/plantilla` y `/lotes` en `cuadrantes_handler`) y el arreglo del buscador. **Después de 3.1**: el panel nuevo contra la API vieja da 404 al descargar la plantilla | HECHO 17-oct, ver registro |
| 3.5 | Prueba con sesión real en prod | En la entidad de pruebas, no en la de un cliente: descargar la plantilla de una sucursal (una pestaña por persona); rellenar una persona y subir; ver «Lista»; confirmar; en su ficha, el horario de esa semana y las tareas con dirección; volver a subir el mismo fichero y comprobar que no duplica. En un buscador del panel, dos palabras («nombre apellido») encuentran a alguien | PENDIENTE: Jose, con sesión real |
| 3.6 | Limpiar la prueba | Desde el contenedor `merlin` de prod, `node services/merlin/dist/soporte/cuadrantes/cli/limpiar.cli.js --entity <e> --employee <p>` (simula; `--apply` para borrar), con autorización | PENDIENTE: tras 3.5 |
| 3.7 | Manual de clientes | Publicar `Clients*/04-*/108-*` (ya en DOCS `main`). El párrafo de «Horario por tareas» solo si la §1 sube en el mismo pase; si no, quitarlo hasta entonces | PENDIENTE: publicar; la §1 subió en la API y el panel, pero la app no (1.11), así que el párrafo de «Horario por tareas» espera a la app |
| 3.8 | Si algo falla | El panel se deshace solo (revert de sus merges en `main`); la API es aditiva —rutas nuevas y una lectura más tolerante— y se queda. Las reglas se deshacen redesplegando la copia guardada en la §5 | — |

## 4. Material por destino — EJECUTADO el 2026-10-17

| # | Paso | Estado |
|---|---|---|
| 4.1 | Migración 034 (`034_inventario_cuentas_destino.sql`), a mano y antes que la 037. El registro del 14-oct dice que se dejó fuera a propósito; ver `inventario/tdr/TDR-008` | HECHO 17-oct, ver registro |

---

## 5. Reglas de Firestore: un solo despliegue — EJECUTADO el 2026-10-17 (con el fichero de la §6)

`firestore.rules` en `main` estaba en la versión del 09-oct (el 16-oct se dijo aquí que no existía; existía, viejo). El arreglo de las consultas de grupo
ya corre en prod desde el 14-oct, desplegado desde rama. El pase tiene que dejar `main` con el
fichero que suma las cuatro cosas: consultas de grupo, cuadrantes, conector y `calendar_days`,
y desplegarlo **una vez**:

1. Guardar el ruleset vivo de prod (API de firebaserules, como el 14-oct).
2. `firebase deploy --only firestore:rules --project encodebiz-services` desde `main`.
3. Probar sin sesión: lectura de `calendar` y `employees` por consulta de grupo 200;
   `signing_keys`, `calendar_days`, `cuadrante_proposals` y `assistant_*` 403.

> **Las tres subcolecciones solo dan 403 con el fichero corregido el 16-oct** (`ac3ee5f`, en
> `develop` y `staging`): hasta entonces `soloServidor` miraba solo la colección raíz, y
> `cuadrante_proposals`, `cuadrante_lotes` (bajo `entities/{e}`) y `calendar_days` (bajo
> `entities/{e}/employees/{p}`) quedaban abiertas aunque estuvieran en la lista. Cualquier rama
> desde la que se desplieguen reglas —también la del paso 1 de la §6— tiene que llevarlo. Antes
> de desplegar, la prueba con el emulador, que tiene que acabar en `fallos: 0`:
> `qa/reglas/probar-reglas.sh` (instrucciones en `qa/reglas/README.md`; Java 21 o más). En dev
> está desplegado y comprobado desde el 16-oct
> ([2026-10-cuadrantes-plantilla.md](./2026-10-cuadrantes-plantilla.md) §8).

Estado: EJECUTADO el 2026-10-17 a las 10:58 UTC, en un solo despliegue con el fichero de la §6
(`3d036ac` de staging: consultas de grupo, cuadrantes, conector, `calendar_days`, `staff_imports`
y lectura con sesión). `main` lo tiene desde el PR #160. Copia previa y sondas en el registro.

---

## 6. Reglas de Firestore: lectura sólo con sesión — EJECUTADO el 2026-10-17 a las 10:58 UTC (paso 1); el paso 2 sigue pendiente

Diseño y plan de ejecución completos en
[ingenieria/reglas-firestore](../ingenieria/reglas-firestore/README.md). Hoy cualquiera lee
todo Firestore sin sesión (empleados con DNI, fichajes con geolocalización, de todos los
clientes). El paso 1 exige `request.auth != null` para leer, con `app_config` pública en
lectura y cerrada en escritura. Inventariado el 2026-10-16: no rompe nada en uso (el fichaje
web `/tools/checking` ya está en mantenimiento; la app tolera que falle la versión mínima).

**No espera al pase**: va a producción el 17 o el 18 de octubre desde la rama, como el
arreglo del 14-oct, con autorización de Jose paso a paso:

1. Guardar el ruleset vivo de prod (API de firebaserules, `x-goog-user-project`) en
   `deployment-prod/<fecha>-firestore-rules-prod-antes.rules`.
2. `firebase deploy --only firestore:rules --project encodebiz-services`.
3. Por REST, sin SDK: consulta de grupo sobre `employees` anónima → **403**; con ID token de
   trabajador → 200; `app_config/global` anónimo → 200; `signing_keys` → 403 para todos.
4. Media hora de vigilancia: fichaje en la app, lista de empleados y presets de calendario en
   el panel, cerrar sesión en los dos.
5. Vuelta atrás: redesplegar el fichero del punto 1.

Cuando se haga, §5 sigue en pie: `main` tiene que acabar con **este** fichero, que ya suma
todo lo anterior.

Estado: EJECUTADO el 2026-10-17 (paso 1). Emulador 38/38 con `qa/reglas/probar-reglas.sh`
reescrito; dev a las 10:53 y prod a las 10:58 UTC, con copias previas de los dos rulesets y
sondas por REST con y sin sesión (registro). La vigilancia de media hora con un cliente real
(punto 4) no la hizo nadie: Jose la hace al abrir el panel y la app. **El paso 2 (aislar por
entidad) sigue pendiente** en [ingenieria/reglas-firestore](../ingenieria/reglas-firestore/README.md).

---

## 7. Tareas programadas a escala: reparto por lotes — 🔴 ALERTA, por detallar

Diseño en [ingenieria/programadas-a-escala](../ingenieria/programadas-a-escala/README.md).
Hoy cada job programado recorre a todos los clientes en serie con un tope fijo (los avisos de
fichaje: 100 cada 5 minutos para toda la plataforma). Arranca el 17/18-oct detrás de las
reglas; entra en staging por días y lo que necesita en prod se detalla aquí según se haga:

1. API de Cloud Tasks activada en `encodebiz-services` (antes del deploy; la cola la crea
   Firebase).
2. Migración de índices de `checklogs_raw` (`synced_at`, `real_date_market`, `(entity_id, ts)`),
   a mano por SSH como todas.
3. Functions nuevas (handlers de lotes) presentes en el despliegue **por nombre**; el
   programador y su handler salen juntos o no sale ningún aviso.
4. Verificación: un planificador de prueba vencido se envía en menos de dos minutos; la
   revisión nocturna devuelve lista vacía.

Estado: PENDIENTE, por detallar.

---

## 8. Calendario semanal de tareas resumido en Postgres — EJECUTADO el 2026-10-17; queda 8.6

Entró en `staging` el 2026-10-16 (merges `74c7471` y el fix de doble respuesta que le sigue;
pase a mano por SSH sin el action: pull, migración, sólo el contenedor `tasks` y nginx
recreado). Ver
[ADR-008](../ingenieria/tasks-service/adr/ADR-008-calendario-semanal-resumido-en-el-servidor.md)
y el contrato en [03](../ingenieria/tasks-service/03_contratos-api.md) (`GET /calendar`,
`GET /calendar/cell`).

**Qué toca y qué no.** Dos rutas nuevas en el servicio `tasks` y un índice en `tasks_raw`.
No hay servicio nuevo, ni variable de entorno nueva, ni cambio en nginx (`/api/v1/tasks/`
ya enruta al contenedor y las subrutas entran por ahí, comprobado en staging), ni cambio en
Firestore ni en reglas. El único consumidor es el front: la pestaña «Calendario semanal» de
Gestión de tareas. Ninguna otra pantalla ni la app móvil llaman a estas rutas.

**Lo que puede fallar y qué se vería.**

- *Sin el índice* el endpoint funciona igual, sólo más lento: recorre las tareas vivas de la
  entidad en vez de ir por `scheduled_start_at`. Con el volumen actual son milisegundos de
  más; no se notaría. Por eso la migración puede ir antes o después del código.
- *Si el espejo `tasks_raw` está incompleto* en producción, el calendario enseñará menos
  tareas que la tabla. La tabla lee Firestore; el calendario lee Postgres. Antes del pase,
  comprobar que el backfill de tareas se corrió en producción (TDR-002 §5 del dashboard
  operativo): `SELECT count(*) FROM tasks_raw WHERE deleted_at IS NULL` frente al número de
  tareas de una entidad grande en Firestore. Si no cuadra, correr `backfill-tasks` antes de
  pasar el front.
- *Zona horaria.* La agrupación usa la zona del navegador (`tz`). Postgres tiene que conocer
  el nombre IANA; con `postgres:16-alpine` los tiene todos. Si alguien ve las tareas a horas
  raras, mirar primero qué `tz` manda su navegador, no el servidor.
- *Un 400 con «entityId is required»* en `/calendar` sin parámetros es lo correcto: es la
  sonda de que la ruta existe. Un `404` significa que el contenedor `tasks` no se
  reconstruyó.
- *Nginx con IPs viejas* tras recrear `tasks`: el síntoma es `502` en `/api/v1/tasks/*`. El
  despliegue normal ya reinicia nginx; en un pase a mano hay que recrearlo.

**Orden del pase.** Back primero, front después, nunca al revés: el front en producción
llamaría a una ruta que todavía no existe y la pestaña quedaría en blanco con un toast de
error. Si hay que deshacer, se deshace el front (es el único consumidor); las rutas del back
son aditivas y pueden quedarse.

| # | Qué | Estado |
|---|---|---|
| 8.1 | Comprobar el espejo: `docker compose -p encodebiz-api --env-file .env.production -f docker-compose.yml exec -T postgres psql -U encodebiz -d encodebiz_analytics -Atc "SELECT count(*) FROM tasks_raw WHERE deleted_at IS NULL"` y cruzar con Firestore. Si falta, backfill antes de seguir | HECHO 17-oct, ver registro |
| 8.2 | Migración 040 (`040_tareas_calendario.sql`): índice parcial `idx_tasks_raw_entity_start` sobre `tasks_raw (entity_id, scheduled_start_at) WHERE deleted_at IS NULL`. A mano, por SSH, sola y leyendo la salida: `docker compose -p encodebiz-api --env-file .env.production -f docker-compose.yml exec -T postgres psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 < migrations/040_tareas_calendario.sql`. Esperado: `CREATE INDEX`. Es `IF NOT EXISTS`: repetirla no hace daño. Bloquea escrituras en `tasks_raw` mientras se construye; en staging fue instantáneo. Verificar: `SELECT indexname FROM pg_indexes WHERE tablename='tasks_raw' AND indexname='idx_tasks_raw_entity_start'` | HECHO 17-oct, ver registro |
| 8.3 | Código: entra con el despliegue normal (`staging → main`, action *CI/CD*), que reconstruye `tasks` y reinicia nginx. Sonda: `curl -s https://api.checkbiz360.com/api/v1/tasks/calendar` debe responder `400 {"code":"task/bad_request","error":"entityId is required"}`; lo mismo `/calendar/cell`. `404` = contenedor viejo; `502` = nginx con IPs viejas | HECHO 17-oct, ver registro |
| 8.4 | Logs limpios: `docker compose … logs --tail=50 tasks` sin «Cannot set headers after they are sent» tras las sondas (era el fallo de doble respuesta, ya corregido en staging) | HECHO 17-oct, ver registro |
| 8.5 | Front: pasar `develop → staging → main` del panel DESPUÉS de 8.3 (los merges `35167ec2` y anteriores del calendario). Sin variables nuevas en Vercel: `NEXT_BACKEND_URI_CHECKINBIZ_TASKS_HANDLER` ya apunta a `api.checkbiz360.com/api/v1/tasks` | HECHO 17-oct, ver registro |
| 8.6 | Prueba con sesión real en producción: Gestión de tareas → pestaña «Calendario semanal» → la semana carga, los contadores de la leyenda cuadran con la tabla filtrada por estado, una tarjeta «N tareas» abre la lista y «Abrir ficha» lleva a la tarea. Probar también la fila «Fecha límite» y el filtro por empleado | PENDIENTE: Jose, con sesión real (la ruta responde 200 con sesión, ver registro) |
| 8.7 | Si falla 8.6 y no es evidente: deshacer sólo el front (revert del merge del calendario en `main` del panel). El back se queda | — |

---

## 9. Análisis a escala: panel, cierre diario, patrones y Merlin — 🔴 URGENTE, por detallar

Diseño en [ingenieria/analisis-a-escala](../ingenieria/analisis-a-escala/README.md). El resumen
del panel hace unas quince consultas sin caché con subconsultas correladas y carga el mes en
memoria; el trigger de patrones pierde salidas simultáneas de la misma sucursal; Merlin se
queda en «analizando» 7 días si el contenedor se reinicia a mitad. Lo que necesita en prod,
según se vaya haciendo:

1. La migración de índices es la **misma** que §7 (añade `checklogs_raw (entity_id, timestamp DESC)`).
2. Variables nuevas en `.env.production`: tamaño del pool y `statement_timeout` por servicio.
3. El trigger `onWhriteChecklog` con `retry: true`, desplegado por nombre.
4. Verificación: `/panel/overview` de la entidad más grande en menos de 3 s; dos salidas
   simultáneas en una sucursal suben `dataPoints` en dos.

Estado: PENDIENTE, por detallar.

---

## 10. Reglas de Firestore y Storage, paso 2a: aislar por entidad — EJECUTADO en prod el 2026-10-19 (17:05 y 17:07 UTC)

Diseño en [ingenieria/reglas-firestore/paso-2a.md](../ingenieria/reglas-firestore/paso-2a.md).
Con el registro abierto, cualquier cuenta recién creada lee y escribe todas las entidades. Con
esto, `entities/{e}/…` sólo para sus miembros: dueños y administradores por su asiento,
empleados por el espejo `entity_members` que mantiene la función `onEmpMember`. Las raíces
(`users`, `issues`, `searchIndex`…) siguen pidiendo sólo sesión hasta el 2b.

**El orden es lo que importa: si las reglas salen antes que el espejo, nadie ficha.**

| # | Qué | Cómo | Estado |
|---|---|---|---|
| 10.1 | Contenedor `checkinbiz` con el script | Con el despliegue normal de `main` | NO HIZO FALTA: el 19-oct la reconciliación se lanzó copiando el módulo compilado al contenedor de prod (y se borró). El script llegará con el próximo pase |
| 10.2 | Función | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo onEmpMember --con-reintentos` (la primera vez pide aceptar los reintentos; hace falta el `.env.encodebiz-services` en `services/firebase_sdk`) | HECHO 19-oct, ver registro |
| 10.3 | Reconciliación simulada | En el contenedor `checkinbiz` de prod: `node services/checkinbiz/dist/scripts/reconcile-entity-members.js`. Mirar las dos últimas líneas: fichas sin `entityId` y asientos con otro id tienen que ser **0**, o se revisan uno a uno antes de seguir | HECHO 19-oct, ver registro |
| 10.4 | Reconciliación | La misma con `--apply`, y otra vez sin él: **cero diferencias** o no se sigue | HECHO 19-oct, ver registro |
| 10.5 | Copia del ruleset vivo | API de firebaserules con `x-goog-user-project: encodebiz-services`, a `deployment-prod/<fecha>-firestore-rules-prod-antes.rules` | HECHO 19-oct, ver registro |
| 10.6 | Reglas | `firebase deploy --only firestore:rules --project encodebiz-services` | HECHO 19-oct, ver registro |
| 10.7 | Verificación | Por REST con sesiones reales de dos entidades (dueño de X lee X y no Y; empleado lee su ficha, sus fichas por grupo, sus fichajes y no otra entidad; nadie lee `entity_members`), como en dev | HECHO 19-oct, ver registro |
| 10.6b | Storage | Guardar el ruleset vivo de **cada** bucket con release (`firebaserules … /releases`, los `firebase.storage/<bucket>`) y `firebase deploy --only storage --project encodebiz-services`. Comprobar con sesión: metadatos, descarga, listado y subida → 403; una URL firmada y una con token → 200. Si prod tiene más de un bucket con reglas, el `firebase.json` sólo cubre el de por defecto: preguntar antes | HECHO 19-oct, ver registro |
| 10.8 | Vigilancia | Media hora con un cliente real: fichaje en la app, cambio de empresa, lista de empleados, presets de calendario, invitación de un colaborador | PENDIENTE |

**Registro de prod, 2026-10-19** (Claude, con autorización de Jose tras probar él en staging):

- 17:0x `onEmpMember` desplegada por nombre (`--solo onEmpMember --con-reintentos`).
- Reconciliación dentro del contenedor `checkinbiz` de prod (módulo compilado de la rama, borrado
  después): 127 fichas, 113 espejos creados, 0 fichas sin `entityId`; segunda pasada sin
  diferencias. **Un asiento con otro id**: `924Gvb…_tkVs6…` (Sonoibiza), con `userId`
  `LoZQ5A…` y una cuenta `924Gvb…` que ya no existe en Auth. Jose: «fue un posible cliente que
  no cuajó» → se deja; ese usuario deja de ver Sonoibiza (su otro dueño, `6TyHj4…`, no cambia).
- Trigger probado en vivo con `entities/zz-prueba-espejo` (alta y baja, 4 s; sin restos).
- Copias previas: `2026-10-19-firestore-prod-antes.rules` (igual que `main`),
  `2026-10-19-storage-encodebiz-services.firebasestorage.app-prod-antes.rules` (el del SaaS,
  abierto con sesión) y `2026-10-19-storage-encodebiz-services-frontend-prod-antes.rules`.
- 17:05:14 reglas de Firestore. Verificación por REST con un dueño de encodeBiz, otro dueño y un
  empleado reales: todo lo esperado; la lectura del espejo dio 200 en el primer minuto y 403 a
  partir de las 17:06 (propagación).
- 17:07 reglas de Storage en el bucket por defecto: con sesión todo 403; URL firmada y la de
  token de `assets/android.png` (pantalla de mantenimiento) 200. El bucket
  `encodebiz-services-frontend` no se toca: sus reglas de prueba caducaron el 2026-07-24 y ya lo
  niegan todo al cliente.
- **Queda:** `main` no tiene estas reglas ni `storage.rules` (lo versionado en `main` no refleja
  prod hasta el próximo PR a `main`); la vigilancia con un cliente real (10.8).

**Vuelta atrás:** redesplegar la copia del 10.5 (menos de un minuto). La función y el espejo
pueden quedarse: sin la regla nadie los lee.

**En dev, 2026-10-19:** `checkinbiz` reconstruido con `d010f4d`; `onEmpMember` desplegada;
reconciliación: 8043 fichas, 7613 espejos creados, 0 fichas sin `entityId`, 0 asientos con
otro id, segunda pasada sin diferencias; el trigger, probado en vivo con una ficha de prueba
(alta, baja, vuelta y borrado, 4 s cada uno, sin restos). Reglas hacia las 10:50 UTC (copia previa
en `2026-10-19-firestore-rules-dev-antes.rules`); por REST con dos dueños y un empleado reales,
todo lo esperado. Storage cerrado al cliente a las 16:30 UTC (copia previa en
`2026-10-19-storage-rules-dev-antes.rules`): con sesión todo 403, URLs firmadas y con token 200.
Falta la prueba con el panel (`start:dev`) y con la app de desarrollo: la QA
de Playwright no la cubre, porque lee con Admin SDK y se salta las reglas.

---

## 11-13. Guion del pase: almacenamiento, punto de fichaje y avisos por correo

Las tres secciones se pisan: este es el orden. Cada paso remite a su fila, que tiene el comando.
Todo con `--project encodebiz-services` explícito y autorización de Jose paso a paso.

**Antes del día:**
- A. QA completa contra `staging` fuera de 22:00-00:00 UTC (la del 19-oct: 466 bien, sin
  regresiones; repetirla con lo del 20-oct).
- B. Front: empujar `feat/quiosco` (commits locales del 20-oct, encima de una fusión de
  `develop` de Jose), fusionarla en `develop` y probar el panel en local contra `staging`.
- C. App: `feat/quiosco` de `checkbiz360` a `develop` y versión lista para publicar (§12.8).
- D. Stripe de prod: crear los dos precios —«Almacenamiento» 0,25 € pago único (§11.6) y
  «Quiosco» por tramos (§12.5)— y apuntar sus `price_…`.

**Rama y PR (20-oct):** `release/pase-2026-10-20` (`2b8e355`), creada con
`merge-tree --merge-base=555ad20 origin/main bfc1417`: código idéntico a `staging`. **PR #199**
abierto contra `main`, sin fusionar. QA de `staging` a las 19:43 UTC: 466 bien, 2 rojos de
informes que pasan sueltos (INF-01-07, INF-05-01), y los conocidos HAL-38.

**El día, en este orden:**
1. **`KIOSK_SECRET`** propio en el `.env` de `checkinbiz` (§12.1). Antes que nada del quiosco.
2. **API a prod**: PR desde la rama principal (nunca desde `develop`) con `checkinbiz`, `billing`,
   `tasks` y `documents` (§11.2, §11.11, §12.2, §13.1).
3. **Reglas de Firestore** (§12.3 y §13.2, un solo despliegue): cierran el quiosco, los avisos y
   **el contador de almacenamiento**. Tienen que ir antes que el paso 5.
4. **Índice de grupo** `calendar.emailNotifications` (§13.3).
5. **Triggers de almacenamiento** (§11.1) y, después, **carga inicial** en simulación y real
   (§11.3, §11.4). Mirar qué empresas pasan de 2 GB (§11.5: avisarlas antes de cobrar).
6. **Ciclo de vida** del quiosco en el bucket del sistema (§12.4), leyendo antes el actual.
7. **Funciones de avisos** `workEmailDigests` y `weeklyScheduleEmails` (§13.4); SMTP en las
   functions (§11.12).
8. **Plantillas de correo** (§11.10 / §13.5b): un solo `email-templates --apply`.
9. **Alta del servicio del quiosco** con su precio (§12.5).
10. **Encender el cobro de almacenamiento**: `STRIPE_STORAGE_GB_PRICE` (§11.7) y
    `invoice.created` en el webhook (§11.8).
11. **Vercel** (producción): `NEXT_BACKEND_URI_BILLING_STORAGE` (§11.9) y
    `NEXT_BACKEND_URI_CHECKINBIZ_KIOSKS_HANDLER` (§12.6); después, el panel a `main` (§12.7).
12. **App** publicada (§12.8).
13. **Pruebas en prod** (§12.9): activar un punto de fichaje, fichar con QR y código, revisar,
    desactivar; marcar la casilla de avisos a una persona nuestra y comprobar el correo.

**Registro del 20-oct (Claude, con orden de Jose), noche UTC:**
- D. Stripe real: «Quiosco» `prod_VThfKSWkc0lK0j` / `price_1USkGMJdldmbRy89HqsEdePP` (mensual,
  tramos, IVA incluido como el inventario); «Almacenamiento» `prod_VThfXJ0tXG8ZWh` /
  `price_1USkGNJdldmbRy898X36fLx5` (0,25 €, pago único).
- 2. PR #199 fusionado (`5c0dcea`), Production CI/CD 39494769587 en verde; rutas nuevas
  respondiendo; `checkinbiz` sano.
- 3. Reglas publicadas desde `origin/main` (hash `4c1001e…`, desde una carpeta aparte: el
  checkout estaba en otra rama de otra sesión).
- 4. Índice de grupo `calendar.emailNotifications` creado y READY (con los tres por defecto).
- 5. Triggers `storageUsageFinalized`/`Deleted` en `us-central1` sobre el bucket del sistema,
  con reintentos. Carga inicial: 178 ficheros de 14 empresas, la mayor 0,055 GB (nadie cerca de
  2 GB: §11.5 no aplica); aplicada y verificada («el contador ya cuadra»).
- 6. Seis reglas de retención `kiosk/r…/` en el bucket de prod (antes estaba vacío).
- 7. `workEmailDigests` y `weeklyScheduleEmails` desplegadas; SMTP presente en las functions.
- 8. Plantillas: 6 nuevas, 4 del inventario al día.
- 9. `service/kiosk` y su plan `standard` con el precio real.
- 10. `STRIPE_STORAGE_GB_PRICE` añadido al `.env.production` (copia previa
  `.env.production.bak-20261020-storage`); `billing` lo carga al recrearse. **Falta
  `invoice.created` en el webhook `we_1UC0XbJdldmbRy898C0g0ah7`**: encenderlo activa también la
  corrección de cantidades del borrador (HAL-19) para todas las facturas; decisión de Jose.
- 11 (parte): **variables de Vercel en producción creadas** (`vercel env add`, proyecto
  `encodebiz-front-saas`): `NEXT_BACKEND_URI_BILLING_STORAGE` y
  `NEXT_BACKEND_URI_CHECKINBIZ_KIOSKS_HANDLER`, con la base `https://api.checkbiz360.com/api/v1/…`
  (misma forma que en `.env.development`). Toman efecto en el próximo despliegue del panel.
- 21-oct: **`fix/quiosco-lista-activos` (`d3b3cf5`, de Jose) en `staging`** (develop `9a1e551`,
  staging `8918ea1` `[skip ci]`, solo `checkinbiz` reconstruido). Al contratar, el primer listado
  enseñaba todos los puntos de fichaje como activos. **El fallo está en prod** (va en el #199):
  tiene que subir antes de que nadie contrate el punto de fichaje (hotfix desde `main`).
- 21-oct, **hotfixes a prod sin CI** (PR con `[skip ci]`, `git pull` en el servidor y solo el
  contenedor tocado): #202 lista de activos (este sí lanzó el CI por error), #203 «20 activos
  incluidos» (`billing`), #204 correo de alta y baja propio del punto de fichaje (`billing`,
  plantillas `SUBSCRIBE_KIOSK`/`CANCELLED_KIOSK` subidas). Los tres también en `staging`.
- 21-oct, **«Mi semana» en el quiosco** (`b6b0895`, otra sesión): en `staging` y **en prod**
  con el #205 (`c684e9b`, `[skip ci]`): solo `checkinbiz` reconstruido; reglas con `kiosk_views`
  publicadas desde `origin/main` (iguales a `staging`; emulador 0 fallos).
- 22-oct, **app (C)**: `feat/quiosco` de `checkbiz360` fusionada en `develop` (`63bbf07`, sin
  conflictos; incluye «Mi semana» en la tablet, `f10acf6`, sin probar en dispositivo contra el
  servidor), versión **1.9.0+67** (`6653a43`), `develop → staging → master` empujados. Analyze en
  su base (67) y 359 tests en verde. El panel ya estaba en `main` (#114 incluye `689876fc`).
- Pendiente de Jose: **publicar la app** en las tiendas desde `master` 1.9.0+67 (12), pruebas en
  prod (13), `invoice.created` (10).

**Índices:** comprobados el 20-oct. La revisión del quiosco usa `checklogs (branchId, timestamp)`,
que ya existe en prod; las demás consultas nuevas tiran de índices de un solo campo. Solo
falta el de grupo del paso 4.

**Sin hacer (código), no bloquea el pase:** correo de alta propio del quiosco; aviso push de
ráfaga al encargado; tareas de varios días en el semanal; comprobar que la app no se rompe con
el tipo de aviso `task_removed` (§13.7).

## 11. Almacenamiento por empresa: contador y exceso de 2 GB — PENDIENTE (en `staging` el 2026-10-19)

Diseño: [ingenieria/almacenamiento](../ingenieria/almacenamiento/README.md), ADR-002. Rama
`feat/almacenamiento-cobro` (e88eda6). Cuenta lo que ocupa cada empresa con triggers de
Storage y añade `⌊GB⌋ − 2` a 0,25 € a la factura de renovación de checkinbiz.

En desarrollo: `billing` reconstruido en el VPS el 19-oct; probado con sesión real de dueño (200 con su empresa, 403 con otra) y carga inicial aplicada a una empresa (`3xcfwyMj6ixsFyDbPera`, 40 ficheros; repetirla no cambia nada); la carga inicial en simulación ve
1.111 ficheros de 123 empresas, ninguno contado. **Triggers desplegados en dev el 19-oct**
(`europe-west1`, con reintentos) y probados: subir 1 MB a la carpeta de una empresa sumó
exactamente 1.048.576 bytes y borrarlo los restó.

Por orden, y el orden importa (los triggers antes que la carga inicial, o lo subido entre
medias no lo cuenta nadie):

| # | Qué | Cómo |
|---|---|---|
| 11.1 | Triggers en el bucket del proyecto | `node scripts/desplegar.mjs --project encodebiz-services --solo storageUsageFinalized,storageUsageDeleted --con-reintentos` (región `us-central1`, la del bucket de prod) |
| 11.2 | `billing` en prod | con el pase de la API |
| 11.3 | Carga inicial, simulando | `docker compose … exec -T billing node services/billing/dist/scripts/storage-backfill.js` — mirar qué empresas pasan de 2 GB |
| 11.4 | Carga inicial, de verdad | lo mismo con `--apply` |
| 11.5 | Avisar a las empresas que pasan de 2 GB | antes de su próxima renovación (decisión de Jose: cómo y cuándo) |
| 11.6 | Price en Stripe de prod | 0,25 €, pago único, EUR, producto «Almacenamiento» |
| 11.7 | Encender el cobro | `STRIPE_STORAGE_GB_PRICE=<price_…>` en el `.env` de prod de `billing` y reiniciarlo. Sin la variable no se cobra nada |
| 11.8 | `invoice.created` en el webhook de Stripe de prod | si no está activado, la línea no se añade nunca |
| 11.9 | Panel: bloque de almacenamiento en Entidad → Suscripciones | `NEXT_BACKEND_URI_BILLING_STORAGE=https://api.checkbiz360.com/api/v1/billing/storage` en Vercel (producción) y la rama `feat/almacenamiento-panel` del front (7fae4d62 en develop). Sin la variable el bloque da error al abrirse |
| 11.10 | Plantilla del aviso del 90 % (ver también 13.5b, mismo script) | `docker compose … exec -T billing node services/billing/dist/scripts/email-templates.js --apply` (sube `STORAGE_ALERT`; sin ella sale el respaldo del código) |
| 11.11 | `documents` en prod | con el pase de la API: es quien bloquea la subida con la ampliación desmarcada |
| 11.12 | SMTP en las functions | los triggers mandan el correo del aviso: comprobar que `SMTP_USER`/`SMTP_PASS` están en el entorno de las functions de prod (ya los usa `onCreateEmployee`) |
| 11.13 | La cuota del inicio enseña el exceso | va con `billing` (11.2) y el panel de 12.7; nada aparte |

Pendiente de decidir: las empresas sin suscripción de pago se cuentan y no se cobran.

## 12. Quiosco (punto de fichaje) — en `staging` desde el 2026-10-19; PENDIENTE para prod

Diseño: [ingenieria/quiosco](../ingenieria/quiosco/README.md) y
[03_contratos-api](../ingenieria/quiosco/03_contratos-api.md). Las fotos van al bucket del
sistema también en prod (decisión de Jose del 19-oct, sin bucket europeo).

**Qué hay en `staging`** (API en `develop`, desplegada a mano con `[skip ci]`):
- 19-oct: el módulo entero (`feat/quiosco`): sesión de tablet con radio y dispositivo único,
  identificar por QR o código, fichaje con foto, revisión, reglas, add-on de pago.
- 19-oct: `fix/quiosco-alta-configurada` — contratarlo ya no pide logo ni slug.
- 20-oct: `fix/quiosco-credencial-por-persona` — QR y código **por persona** (los mismos en
  todas sus sucursales); códigos, contraseña y PIN guardados cifrados y **siempre visibles**,
  ocultos con ver y copiar; todo acceso queda en `entities/{e}/kiosk_audit`.
- 20-oct: `feat/quiosco-rafaga-30s` — ráfaga por cadena (menos de 30 s entre fichajes) sin
  esperas; `faceDetected` en el fichaje y «Sin cara» primero en la revisión.
- 20-oct: `feat/quiosco-activar-por-sucursal` — activar y desactivar por sucursal; **solo se
  cobran los activos** (con credenciales).
- 20-oct: `feat/cuota-quiosco-y-almacenamiento` — la cuota estimada del inicio incluye el
  punto de fichaje y el exceso de almacenamiento.

Probado en dev el 20-oct con una tablet real (Samsung SM-X210): sesión, identificación por QR,
fichaje válido con foto, **cara detectada en la tablet**, foto de 48 KB en `kiosk/r30/` y
contada por el trigger de almacenamiento. QA completa el 19-oct sin regresiones (466 bien).

**Panel y app, sin integrar todavía:**
- Panel: rama `feat/quiosco` del front (página del quiosco, tarjetas, códigos, revisión,
  activar/desactivar, ver/copiar credenciales, cuota del inicio). A 20-oct tiene commits
  locales **sin empujar** encima de una fusión de `develop` hecha por Jose.
- App: rama `feat/quiosco` de `checkbiz360`, empujada (pantalla Foto con condiciones y
  detección de cara nativa en Android; iOS sin cambios, sigue en Swift Package Manager y 15.0).

Por orden:

| # | Qué | Cómo |
|---|---|---|
| 12.1 | **`KIOSK_SECRET` propio en prod, ANTES de activar ningún quiosco** | en el `.env` de prod de `checkinbiz`. Firma los QR **y cifra** códigos, contraseñas y PIN guardados: cambiarlo después deja ilegibles todas las tarjetas y credenciales. Sin él usa `JWT_2FA_SECRET`, que se rota por otros motivos |
| 12.2 | `checkinbiz` y `billing` en prod | con el pase de la API |
| 12.3 | Reglas de Firestore | el fichero de `develop` cierra al cliente `kiosks`, `kiosk_sessions` y `kiosk_audit` además del paso 2a. `firebase deploy --only firestore:rules --project encodebiz-services`; antes, el emulador (`qa/reglas`) |
| 12.4 | Las seis reglas de retención del quiosco en el bucket del sistema de prod | `gs://encodebiz-services.firebasestorage.app`, `kiosk/r15/` … `kiosk/r1460/` con su edad. **Antes, leer su ciclo de vida actual**: `--lifecycle-file` reemplaza el entero (el 18-oct estaba vacío). En dev, puestas el 19-oct |
| 12.5 | Precio del quiosco en Stripe de prod y alta del servicio | producto «Quiosco», mensual EUR, `licensed`, tramos graduados (hasta 20: `flat_amount` 1900, `unit_amount` 0; desde 21: `unit_amount` 90). **Hecho en prod el 2026-10-21**: `price_1UT200JdldmbRy89jhWXHXRG`, y `service/kiosk/plan/standard.stripePrice` apunta a él; las dos suscripciones en prueba pasaron a él sin prorrateo y el de 50 está archivado. Después `node services/checkinbiz/dist/scripts/alta-servicio-quiosco.js --stripe-price price_… --apply`. Sin esto el panel dice «El módulo todavía no tiene un plan contratable». En dev, hecho el 19-oct: `prod_VTJYJGvvD6VDsI` / `price_1USMv2R97dgHV4NJU5rRJEB3` |
| 12.6 | Variable del proxy del quiosco en Vercel (producción) | `NEXT_BACKEND_URI_CHECKINBIZ_KIOSKS_HANDLER=https://api.checkbiz360.com/api/v1/checkinbiz/kiosks`. Sin ella el panel del quiosco no carga |
| 12.7 | Panel: `feat/quiosco` del front a `main` | antes, empujar la rama (commits locales) y fusionar `develop`. Lleva la allowlist del proxy con `…/credentials/reveal` y `…/code/reveal` (sin ellas, «no tienes permisos» al ver o copiar) |
| 12.8 | App: versión con la pantalla Foto | `checkbiz360` `feat/quiosco` → `develop` → publicación Android. El modelo de caras lo baja Play Services al instalar (`com.google.mlkit.vision.DEPENDENCIES=face`); sin él, el fichaje sale sin marca, nunca se bloquea |
| 12.9 | Prueba en prod con una sucursal | activar, entrar en la tablet, fichar con QR y con código, revisar la foto, desactivar |

**Sin hacer (código):** correo de alta propio del quiosco (hoy llega el genérico de
CheckBiz); aviso push de ráfaga al encargado (hoy solo se marca y se ve en la revisión).

## 13. Avisos de trabajo por correo — en `staging` desde el 2026-10-20; PENDIENTE para prod

Diseño: [ingenieria/avisos-por-correo](../ingenieria/avisos-por-correo/README.md). Rama
`feat/avisos-por-correo` (API). Para quien no usa el móvil: casilla «Enviar notificaciones por
email» en Horarios y festivos; tareas asignadas, cambiadas o retiradas agrupadas (15 min, o al
momento si tocan las próximas 24 h) y el horario del domingo a las 18:00. Nada del fichaje.
Añade además `task_removed` (push a todos al borrar, cancelar o desasignar) y **cierra en las
reglas `storage_objects` y `entities/{e}/storage_shards`, que estaban abiertas** (un miembro
podía rebajarse el contador de almacenamiento; ver §11).

Probado en dev el 20-oct: la casilla se guarda; una tarea para mañana se apuntó como urgente con
su lugar; el semanal forzado salió (1 enviado) y al repetirlo no se reenvió (huella igual).

| # | Qué | Cómo |
|---|---|---|
| 13.1 | `tasks` y `checkinbiz` en prod | con el pase de la API |
| 13.2 | **Reglas de Firestore** | el fichero de `develop` cierra `email_digest`, `schedule_emails`, `storage_objects` y `storage_shards`. **Con o antes que §11**: sin esto, el contador de almacenamiento queda escribible por los miembros. Emulador antes (`qa/reglas`, 0 fallos el 20-oct) |
| 13.3 | Índice de grupo de colecciones `calendar.emailNotifications` | `gcloud` no deja elegir el alcance: PATCH a la API de Firestore `collectionGroups/calendar/fields/emailNotifications?updateMask=indexConfig` con los tres índices por defecto (`COLLECTION` asc, desc, contains) **y** `COLLECTION_GROUP` asc (así se hizo en dev el 20-oct). Sin él el semanal falla |
| 13.4 | Funciones `workEmailDigests` y `weeklyScheduleEmails` | `node scripts/desplegar.mjs --project encodebiz-services --solo workEmailDigests,weeklyScheduleEmails` |
| 13.5 | SMTP en las functions de prod | ya lo exige §11.12 |
| 13.5b | Plantillas en Firestore | `docker compose … exec -T billing node services/billing/dist/scripts/email-templates.js` (simula) y luego `--apply`: sube `TASKS_DIGEST`, `WEEKLY_SCHEDULE` y `STORAGE_ALERT` en es/en a `emails_template`, con la maqueta de la marca; las del inventario deben salir «al día». En dev, hecho el 20-oct (6 nuevas, 4 al día) |
| 13.6 | Panel: la casilla | va en la rama `feat/quiosco` del front (§12.7) |
| 13.7 | App: tipo `task_removed` | la app enseña los avisos por su `type`; comprobar que uno desconocido no rompe la lista, o añadir su texto |

## Registro del día del pase — 2026-10-17

Ejecutado por Claude con la orden de Jose de las 10:44 UTC («hoy es el pase, ahora mismo,
encárgate de todo»). El hook `block-prod.sh` estaba desarmado desde antes y se dejó así durante
el pase; se rearmó al cerrar, con `assistant`, `branches` y `entities` en su lista de
contenedores. Nada se desplegó a mano: la API por `staging → main` y su workflow, el panel por
Vercel, las funciones por nombre con `desplegar.mjs`, las reglas con `--only firestore:rules`.

| Paso | Hora (UTC) | Quién | Resultado y lo que se vio |
|---|---|---|---|
| Lectura previa y fusión de prueba | 10:40 | Claude | `git merge-tree` staging→main limpio en API y panel, pese a los PR `release/*` del CRM con SHAs distintos. Prod: ninguna de 034/037/040 aplicada; índice `tasks` (assignedEmployeeIds + scheduledStartAt) ya existía, `calendar_days` no. `tasks_raw` 100 vivas y `backfill-tasks` en simulación coincide entidad a entidad (78/11/4/3/3/1): espejo completo (8.1). `.env.production` ya tenía `FIREBASE_WEB_*`. Staging venía con el QA en rojo: EMP-09-01 por la ocupación en minúsculas (regla del 16-oct) y CHK-08-70 a las 10:06 con «en su casa son las 23h» tras pasar a las 09:41. |
| Copia del ruleset vivo de prod | 10:49 | Claude | [2026-10-17-firestore-rules-prod-antes.rules](./2026-10-17-firestore-rules-prod-antes.rules) (3428 bytes: el del 14-oct ya con la regla de consultas de grupo). Dominios autorizados de Auth leídos: localhost, firebaseapp, web.app, saas.encodebiz.com. |
| Código: reglas con sesión, prueba del emulador, infra de prod, QA | 10:50 | Claude | `firestore.rules` paso 1 (`publica('app_config')`; lectura y consultas de grupo con sesión). `qa/reglas/probar-reglas.sh` reescrito: 38 comprobaciones, `fallos: 0` con el JDK 26. `docker-compose.yml` de prod: `branches` (sin `ports`) y `assistant` (URL pública de prod, `INTERNAL_URL`s), `employees` con `BRANCHES_INTERNAL_URL` (2.2–2.4). `nginx/nginx.conf`: upstream `assistant_service`, `= /api/v1/assistant`, los dos `.well-known`, `/api/v1/assistant/`, `= /api/v1/employees/import`, `/api/v1/employees/import/`, `= /api/v1/employees/welcome` (2.5–2.6). QA EMP-09-01 adaptada a la ocupación en minúsculas. |
| Vercel (Production) | 10:51 | Claude | `NEXT_PUBLIC_ASSISTANT_CONNECTOR_BASE=https://api.checkbiz360.com/api/v1/assistant` (Config) y `NEXT_BACKEND_URI_STAFF_IMPORT_HANDLER=https://api.checkbiz360.com/api/v1/employees` (Sensitive), con la CLI. Comprobado con `env pull` (2.15). |
| Índice `calendar_days` en prod | 10:51 | Claude | `gcloud firestore indexes composite create`, grupo de colecciones, `entityId` ASC + `date` ASC, `--async`. SUCCESSFUL a las 11:02. El de `tasks` ya existía (1.2). |
| Firebase Auth de prod: dominio | 10:51 | Claude | PATCH `authorizedDomains` con la lista entera más `api.checkbiz360.com`; la respuesta trae los cinco (2.8). |
| Copias en el servidor de prod | 10:51 | Claude | `~/backups/encodebiz_analytics_antes_pase_2026-10-17.sql.gz` (2,2 MB) y `~/backups/env.production.antes_pase_2026-10-17`. |
| `.env.production`: conector | 10:51 | Claude | Añadidas `ASSISTANT_COOKIE_SECRET` (`openssl rand -base64 32`, distinto del de staging) y `ASSISTANT_FIREBASE_{API_KEY,AUTH_DOMAIN,PROJECT_ID,APP_ID}` copiadas de `FIREBASE_WEB_*` del mismo fichero (proyecto `encodebiz-services`). Los valores no se vieron desde aquí (2.7). |
| Validación de la infra de prod | 10:52 | Claude | `docker compose config` con el compose nuevo en el servidor de prod: 19 servicios, `ASSISTANT_PUBLIC_URL` y `BRANCHES_INTERNAL_URL` resueltos. `nginx -t` del `nginx.conf` de prod en la red `encodebiz-dev` del VPS (certificados de staging montados): «syntax is ok / test is successful». Docker no corre en el portátil. |
| Migración 034 | 10:52 | Claude | `ALTER TABLE`, `UPDATE 1`, `CREATE INDEX`, rc 0 (4.1). |
| Reglas a dev | 10:53 | Claude | Copia previa [2026-10-17-firestore-rules-dev-antes.rules](./2026-10-17-firestore-rules-dev-antes.rules). `firebase deploy --only firestore:rules --project dev-encodebiz`. REST sin sesión: grupo `employees`/`calendar` 403, `entities` 403, `users` 403, `app_config` 200. Con sesión (custom token de un usuario de dev): grupo `employees`/`calendar` 200, `entities` 200, `signing_keys` 403, escribir `app_config` 403. |
| Migración 037 | 10:54 | Claude | `ALTER TABLE`, `CREATE TABLE`, `CREATE INDEX`, `ALTER TABLE`, `ALTER TABLE`, rc 0 (1.3). Antes del job de dimensiones de las 11:20, que ya corrió con el código nuevo y escribió `calendar_days` con `success`. |
| Migración 040 | 10:54 | Claude | `CREATE INDEX`, rc 0 (1.4, 8.2). Verificadas las tres: `account_kind`, `dim_calendar_days`, `schedule_mode`, `idx_tasks_raw_entity_start`. |
| Rama, develop y staging | 10:55 | Claude | `feat/pase-prod-2026-10-17` (`f392729`) → develop (`540d658`) → staging (`3d036ac`). Staging CI/CD 39026746896. |
| Panel: develop → staging | 10:57 | Claude | Al hacer el pull, otra sesión había fundido ya «calendario de MUI unificado» en develop y staging (`ebe3ead4`); el merge de aquí quedó vacío. |
| Reglas a PRODUCCIÓN | 10:58 | Claude | `firebase deploy --only firestore:rules --project encodebiz-services` con el fichero de staging. Sondas desde el contenedor `tasks` de prod (solo códigos, el token no sale del contenedor): sin sesión grupo `employees`/`calendar`/`checklogs` 403, `entities` 403, `users` 403, `app_config/global` 200. Con sesión (jose@encodebiz.com por custom token): grupo `employees`/`calendar` 200, `entities` 200, escribir `app_config` 403, `signing_keys` 403, `calendar_days` 403, `cuadrante_proposals` 403 (§5, §6, 1.5, 2.9, 3.3). |
| PR API staging → main | 10:59 | Claude | #160 abierto; lleva `services/assistant` (47 ficheros), `services/branches`, compose, nginx, reglas y 034/037/040 (2.1). |
| Funciones de Firebase a prod | 11:02–11:05 | Claude | `desplegar.mjs --project encodebiz-services --solo onTaskDay,weeklyFromTaskDays,employeePlanifierWorker,planifierNotificationWorker,taskStartNotificationWorker`. Antes: las dos primeras no existían en prod; los tres workers sí, en `default`. Ninguna usa `EVENTS_API_*` (la función que lo exige no la llama nadie, y dev corre igual sin ellas). Resultado: dos creadas en europe-west1, tres actualizadas en us-central1, «Deploy complete». `functions:list` las enseña en `default`, nodejs22; Cloud Scheduler `0 3,15 * * *` Europe/Madrid, ENABLED (1.8, 1.9). |
| QA de staging | 11:13 | CI | 473 pasadas, 0 fallos (EMP-09-01 con la expectativa nueva y CHK-08-70 pasan). |
| PR #160 fusionado, despliegue de producción | 11:14–11:17 | Claude / CI | Merge `c0cc926`. Production CI/CD 39027939538 en verde a las 11:17. `ps`: 19 servicios, todos `healthy`, `assistant` y `branches` incluidos. Log de `assistant`: «Listening on :3017 — issuer https://api.checkbiz360.com/api/v1/assistant», sin «autorización apagada». `branches` responde desde `employees`. nginx desplegado con el `4m` del gpt y las rutas nuevas. `tasks` sin «Cannot set headers» (1.6, 1.7, 2.12, 2.14, 3.2, 8.4). |
| Sondas sin sesión | 11:18 | Claude | `/health` 200; `gpt/cuadrantes/plantilla` 401 (3.1); `tasks/calendar` y `/cell` 400 «entityId is required» (8.3); `.well-known/oauth-authorization-server` 200 con el issuer de prod; `POST mcp/e/x` 401 con `WWW-Authenticate … resource_metadata`; `employees/import/template` 401; `employees/welcome` 401; `/api/v1/branches/` 404 y `/api/v1/employees/` 404, cerrados como se quería (2.13). El `protected-resource` con un id inventado da 404 `not_found` del propio servicio, igual que en staging; con la entidad real, 200. |
| Comprobación 1.9 con sesión | 11:29 | Claude | Desde el contenedor `tasks`, con la sesión de jose@encodebiz.com en la entidad `OdX1eMPbRpwxjDfwdNkN`: `GET /calendar` 200 con `scheduleMode: weekly`; `PATCH` scope `branch` + `tasks` → 400 `calendar/schedule_mode_employee_only`; `GET /tasks/calendar` 200 con `countsByStatus`. |
| Panel a producción | 11:30 | Claude | PR encodebiz-front-saas-clean#106 (staging → main, 85 commits, con «calendario de MUI unificado» de otra sesión) fusionado. Vercel: deployment de producción **Ready** a las 11:31 (37 s) (1.10, 2.16, 3.4, 8.5). |
| Cierre | 11:35 | Claude | Hook `block-prod.sh` rearmado en `.claude/settings.json` con los tres contenedores nuevos. Registro escrito; `2026-10-cuadrantes-plantilla.md` §8 con su fila. |

## 14. Vacaciones y permisos desde la app — PENDIENTE (rama `feat/vacaciones`, 2026-10-22)

Diseño: [ingenieria/vacaciones](../ingenieria/vacaciones/README.md). Solo `checkinbiz` (rutas
nuevas bajo `/calendar`) y `shared`; aprobar escribe los mismos días libres del empleado que el
panel. Todo `--project encodebiz-services` explícito y con autorización de Jose.

| # | Qué | Cómo |
|---|---|---|
| 14.1 | Código: `checkinbiz` (y `billing` solo por el script de plantillas) | PR desde la rama principal, como siempre |
| 14.2 | Reglas de Firestore: `absence_requests` cerrada al cliente | `firebase deploy --only firestore:rules --project encodebiz-services` desde `origin/main`; antes, emulador 0 fallos |
| 14.3 | Índices compuestos de `absence_requests` (colección): `(employeeId ASC, endDate ASC)` y `(status ASC, createdAt DESC)` | `gcloud firestore indexes composite create --collection-group=absence_requests --query-scope=COLLECTION --field-config=field-path=employeeId,order=ascending --field-config=field-path=endDate,order=ascending` y el segundo con `status`/`createdAt desc`. En dev creados el 22-oct |
| 14.4 | Plantilla de correo `ABSENCE_REQUESTED` (es/en) | `node services/billing/dist/scripts/email-templates.js --apply` (ya la incluye) |
| 14.5 | Panel (pestaña Calendario → Solicitudes) y app («Mi calendario», versión nueva) | detrás del back; el panel usa el proxy de calendario que ya existe, sin variable nueva |
| 14.6 | Prueba en prod | pedir desde la app con una persona nuestra, correo al administrador, aprobar en el panel, ver la ausencia en Disponibilidad y el aviso en la app |

## 15. «Calendario»: turnos cargados por fecha — PENDIENTE (rama `feat/horario-calendario`, 2026-10-22)

Diseño: [ingenieria/horario-por-tareas/tdr/TDR-007](../ingenieria/horario-por-tareas/tdr/TDR-007-calendario-turnos-por-fecha.md).
Tercer modo del horario, `scheduleMode: "calendar"`, heredable por empresa y sucursal; los días
se cargan desde el panel (`PUT /calendar/days`) o por el importador de cuadrantes. Sin reglas
ni índices nuevos: usa `calendar_days` y su índice de grupo. Todo `--project encodebiz-services`
explícito y con autorización de Jose.

| # | Qué | Cómo |
|---|---|---|
| 15.1 | Migración `043_horario_calendario.sql` (el CHECK de `dim_calendars.schedule_mode` admite `calendar`) | a mano por SSH, mirando el resultado, **antes** de los contenedores |
| 15.2 | Contenedores: `checkinbiz`, `analytics`, `merlin`, `assistant`; y `tasks`, `reports`, `firebase_sdk` solo porque cambian tipos de shared | PR desde la rama principal; `build --no-deps` de los tocados |
| 15.3 | Función `weeklyFromTaskDays` (copia la semana también a quien está en `calendar`) | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo weeklyFromTaskDays` |
| 15.4 | Panel: selector con «Calendario» y el calendario semanal de turnos | detrás del back; sin variable nueva |
| 15.5 | Prueba en prod | una sucursal de prueba en `calendar`, cargar la semana desde el panel, fichar con la app publicada (1.7.0) y ver el turno en Disponibilidad |

## 6. Firebase: un solo origen para las funciones — PENDIENTE (Jose: «ahora no»)

Comprobado el 2026-10-17 con `gcloud functions describe`: el código de las funciones está
migrado a `services/firebase_sdk` (24 funciones, `npm run deploy:listar -w services/firebase_sdk`),
pero en producción la mayoría corre lo desplegado antes del porte (`onChecklogWrite` 29-jul,
`onActivateCheckbiz` 4-sep, `onTaskPattern` 3-jul); solo las cinco del horario por tareas salen
de `firebase_sdk`. Orden decidido por Jose: **primero staging (`dev-encodebiz`), validar todo, y
después producción**, una a una con `desplegar.mjs --solo`.

| # | Paso | Estado |
|---|---|---|
| 6.1 | Inventario en dev: fecha de despliegue de cada una de las 24 frente al porte (12-sep) | PENDIENTE |
| 6.2 | Desplegar en `dev-encodebiz` las que falten, con `--solo`, y validar cada una (QA `45-espejo-y-programadas` y la prueba propia de cada trigger) | PENDIENTE |
| 6.3 | Producción, una a una, comprobando cada una | PENDIENTE |

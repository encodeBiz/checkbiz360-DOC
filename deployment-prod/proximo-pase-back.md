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

## 1. Horario por tareas (fases 1 a 4, selector del panel, D11) — EJECUTADO el 2026-10-17 (API, funciones y panel); app en `master` 1.10.0+68, publicada en tiendas

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
| 1.11 | App | `checkbiz360`: `develop` con la fase 2 → versión nueva publicada en las dos tiendas | HECHO: 1.10.0+68 publicada en las dos tiendas (el 17-oct `master` seguía en 1.7.0+57) |
| 1.12 | **No activar el modo a nadie en prod** hasta que 1.11 esté publicada y la persona la tenga instalada | Con una app vieja la persona vería los botones de la tarea y la jornada en blanco | LEVANTADO: 1.11 publicada |

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
- App publicada en las tiendas (hoy 1.10.0+68). Pendiente de Jose: pruebas en
  prod (13), `invoice.created` (10).

**Índices:** comprobados el 20-oct. La revisión del quiosco usa `checklogs (branchId, timestamp)`,
que ya existe en prod; las demás consultas nuevas tiran de índices de un solo campo. Solo
falta el de grupo del paso 4.

**Sin hacer (código), no bloquea el pase:** ~~correo de alta propio del quiosco~~ (hecho, #204 del 21-oct); aviso push de
ráfaga al encargado; tareas de varios días en el semanal; comprobar que la app no se rompe con
el tipo de aviso `task_removed` (§13.7).

## 11. Almacenamiento por empresa: contador y exceso de 2 GB — EJECUTADO el 2026-10-20; queda 11.8 (`invoice.created`, decisión de Jose): sin él no se cobra

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

## 12. Quiosco (punto de fichaje) — EJECUTADO el 2026-10-20 y 21 (API, reglas, precio, panel #114) y app publicada; queda la prueba en prod (12.9)

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

**Sin hacer (código):** ~~correo de alta propio del quiosco~~ (hecho, #204 del 21-oct); aviso push de ráfaga al encargado (hoy solo se marca y se ve en la revisión).

## 13. Avisos de trabajo por correo — EJECUTADO el 2026-10-20; queda 13.7 (la app con `task_removed`)

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

## 14. Vacaciones y permisos desde la app — servidor y panel EN PROD el 2026-10-22 (#212, #118); app en `master` 1.10.0+68, publicada en tiendas

Diseño: [ingenieria/vacaciones](../ingenieria/vacaciones/README.md). Solo `checkinbiz` (rutas
nuevas bajo `/calendar`) y `shared`; aprobar escribe los mismos días libres del empleado que el
panel. Todo `--project encodebiz-services` explícito y con autorización de Jose.

| # | Qué | Cómo |
|---|---|---|
| 14.1 | Código: `checkinbiz` (y `billing` solo por el script de plantillas) | PR desde la rama principal, como siempre |
| 14.2 | Reglas de Firestore: `absence_requests` cerrada al cliente | `firebase deploy --only firestore:rules --project encodebiz-services` desde `origin/main`; antes, emulador 0 fallos |
| 14.3 | Índices compuestos de `absence_requests` (colección): `(employeeId ASC, endDate ASC)` y `(status ASC, createdAt DESC)` | `gcloud firestore indexes composite create --collection-group=absence_requests --query-scope=COLLECTION --field-config=field-path=employeeId,order=ascending --field-config=field-path=endDate,order=ascending` y el segundo con `status`/`createdAt desc`. En dev creados el 22-oct |
| 14.4 | ~~Plantilla de correo `ABSENCE_REQUESTED`~~ | Retirada el 22-oct (Jose: «no por email»); las dos filas `ABSENCE_REQUESTED_es/en` subidas a dev y prod quedan sin uso, se pueden borrar de `emails_template` |
| 14.5 | Panel (Contacto → Solicitudes; «Incidencias» pasa a «Contacto») y app («Mi calendario», versión nueva) | detrás del back; el panel usa el proxy de calendario que ya existe, sin variable nueva |
| 14.6 | Prueba en prod | pedir desde la app con una persona nuestra, verla en Contacto → Solicitudes, aprobar, ver la ausencia en Horarios y festivos y el aviso en la app |

**Registro del 22-oct:** PR #212 (`release/vacaciones`, idéntico a `staging`) fusionado en `main`;
reglas publicadas en prod; los dos índices creados (CREATING → READY); plantilla subida y después
retirada del código con el hotfix #213 (`release/vacaciones-sin-correo`, Production CI/CD en verde). **El servidor de vacaciones está completo en prod.** Quedan panel (Contacto → Solicitudes, en `develop`) y app («Mi calendario», en `develop`).

**Registro del 23-oct (14.7, a mano, sin Actions):** PR #224 (`release/mi-calendario-duenos`, idéntico a
`staging`, un solo fichero: `absenceRequests.controller.ts`) fusionado en `main` a 80b1728. Qué
cambia: quien tiene asiento de propietario o administrador **y** ficha de empleado ya ve «Mi
calendario» y pide vacaciones (antes 403, porque el guard compartido no le buscaba la ficha); y el
aviso de aprobada o rechazada lleva `employeeId` y `uid`, que la app exige para abrir la pantalla.
Sin migración, índice, variable, función ni reglas. GitHub Actions no arrancaba (facturación:
«recent account payments have failed or your spending limit needs to be increased»), así que, por
orden de Jose, Claude lo desplegó a mano en `/opt/encodebiz-api` a las 10:32 UTC: `git pull
--ff-only origin main` + `up -d --build --no-deps checkinbiz` + `restart nginx`. Comprobado:
contenedor `healthy` con el código nuevo dentro, `/health` 200, las rutas de calendario responden
401 sin token (no 502) y el resto de servicios pasan por nginx. Probado antes en staging con
cuentas reales de dev: dueño con ficha 200 en mes y solicitudes; administrador sin ficha, 403 en
ambos. La QA automática no corrió (Actions parado). Pendiente de Jose: arreglar la facturación de
Actions y la prueba 14.6 con sesión real.

## 15. «Calendario»: turnos cargados por fecha — EJECUTADO el 2026-10-22 (API #214, migración 043, panel #115) y sustituido el mismo día por §16 (TDR-008) y §16 ter (TDR-009)

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
| 15.0 | Estado | En `staging` de API y panel el 22-oct, QA 54+55 28/28. Sin Actions (minutos agotados): la API de prod se despliega a mano en el servidor, `git pull` + `build --no-deps` de los mismos seis servicios que en staging + `restart nginx`. El panel de `staging` lleva además vacaciones (§14) |
| 15.5 | Prueba en prod | una sucursal de prueba en `calendar`, cargar la semana desde el panel, fichar con la app publicada (1.7.0) y ver el turno en Disponibilidad |

## 16. Alertas operativas por correo — EN PRODUCCIÓN el 2026-10-28 (fases 1-2), **para todas las empresas, solo owner y admin**

**Ejecutado el 2026-10-28 por Claude con la orden de Jose («ya bájalo a prod», «para probar primero sobre nosotros»).**
El código ya estaba en `main` desde el #233 de otra sesión; no hubo PR propio. A mano, sin CI:
047 aplicada en `encodebiz_analytics` (8 tablas, 10 índices, 4 ALTER, sin error); **las 8 empresas
restantes con datos, apagadas** (`alert_email_settings.enabled = false`, `updated_by = 'pase-2026-10-28…'`)
antes de arrancar el contenedor; `build --no-deps analytics billing`, nginx reiniciado, sin 502;
4 plantillas nuevas (`--apply`: 4 nuevas, 14 al día); SMTP y `SES_CONFIGURATION_SET` presentes en
`analytics`; sync de dimensiones de `nDON8mv1S1tuPAxx7jQI` (4 usuarios de panel, 6 responsabilidades).
Por orden de Jose («lánzamelo ahora») se lanzó el resumen real ese día: 3 alertas, 5 correos enviados
(4 owner/admin, 1 supervisor con solo su centro). **Para encenderlo a todos:**
`DELETE FROM alert_email_settings WHERE updated_by LIKE 'pase-2026-10-28%';`
**Pendiente:** 16.4 (`onChecklogSync` con retry, no hace falta para el resumen), fases 3 y 4.
**Mismo día, más tarde:** Jose vio que a jose@ le llegaba por su responsabilidad de manager:
«esto solo es para admin y owner, nadie más». Se apagó todo (16:5x UTC), hotfix #235 (fuera
supervisores, managers y direcciones extra; pie «propietario»/«administrador»), `build --no-deps
analytics`, y por orden de Jose («actívalos ya para todos») **encendido para todas las empresas**
(`DELETE` de las 9 filas `pase-2026-10-28%`). Llevado a develop (1172187) y staging (4f23ae6).

Diseño: [ingenieria/alertas-por-correo](../ingenieria/alertas-por-correo/README.md). Las 12
alertas del dashboard salen por correo a owner, admin, direcciones extra y supervisores (estos
solo las de sus sucursales): el resumen de la mañana (8:00 local de la empresa, fase 2, hecha)
y las inmediatas (fase 3, pendiente). Todo en Postgres: espejos de destinatarios, histórico y
cola de envío. Ajustes por empresa (fase 4, pendiente); mientras, los defectos: encendido,
8:00, todas las reglas, con supervisores.

| # | Qué | Cómo |
|---|---|---|
| 16.1 | Migración `047_alertas_por_correo.sql` (dim_entities, dim_panel_users, dim_responsibilities, email/idioma en dim_employees, índice `(entity_id, timestamp)` en checklogs_raw, alert_*, email_outbox) | a mano por SSH, mirando el resultado, **antes** del contenedor de analytics. El índice sobre `checklogs_raw` tarda lo que tarde la tabla de prod |
| 16.2 | Contenedores: `analytics` (jobs y espejos); `billing` solo por el script de plantillas; los que recompilan por tipos de shared | PR desde la rama principal; `build --no-deps` de los tocados |
| 16.3 | Plantillas `ALERTS_DIGEST` y `ALERTS_IMMEDIATE` en `emails_template` | `exec -T billing node services/billing/dist/scripts/email-templates.js` (simula) y `--apply` |
| 16.4 | Función `onChecklogSync` con `retry: true` (el espejo reintenta en vez de soltar el fichaje) | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo onChecklogSync` |
| 16.5 | Primer sync de dimensiones tras la migración (asientos, responsabilidades, correos) | `POST /api/analytics/dimensions/sync` S2S, o esperar al :20 |
| 16.6 | Variable `PANEL_URL` en `.env.production` (opcional: por defecto `https://saas.encodebiz.com`) | solo si el dominio del panel cambia |
| 16.7 | SMTP en el contenedor de analytics | ya viene por el `env_file` común; comprobar `SMTP_USER` en `analytics` antes del primer resumen |
| 16.8 | Prueba en prod | una empresa nuestra con alertas vivas: a las 8:00 locales llega un correo al owner; `alert_digest_runs` y `email_message` con `kind = alerts_digest` |

## 1c. Horario por tareas: tareas de varias personas (TDR-006) — EN PRODUCCIÓN (22-oct)

| # | Paso | Estado |
|---|---|---|
| 1c.1 | Contenedores `checkinbiz` y `tasks` | **HECHO 2026-10-22 14:42 UTC** como hotfix: PR #211 a main con `[skip ci]` (b993357), `git pull` y `up --build -d --no-deps checkinbiz tasks` + `restart nginx` en el servidor; los dos sanos y con el código nuevo |
| 1c.2 | `employeePlanifierWorker` | **HECHO 14:44 UTC** con `desplegar.mjs --project encodebiz-services --solo`, desde main; `ACTIVE` |
| 1c.3 | Comprobar con una tarea de dos personas en prod | PENDIENTE: prueba de Jose con la app |

## 16. El cuadrante son los turnos (TDR-008) — EJECUTADO el 2026-10-22 (orden de Jose: «despliega a prod, estamos probando ahí directamente»)

Diseño: [TDR-008](../ingenieria/horario-por-tareas/tdr/TDR-008-el-cuadrante-son-los-turnos.md).
Sin migración, reglas ni índices. Va **a la vez** que la parte del asistente (`assistant`, TDR-008
§5.2), que ya está en `staging` y depende de este servidor. A mano, sin Actions.

| # | Qué | Cómo |
|---|---|---|
| 16.1 | API: `checkinbiz`, `analytics`, `merlin`, `assistant`, `tasks`, `reports` | release desde `main` con `staging`, PR con `[skip ci]` en el asunto, `git pull` en el servidor y `build --no-deps` de esos seis, `restart nginx` |
| 16.2 | `weeklyFromTaskDays` (vuelve a ser solo de «Horario por tareas») | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo weeklyFromTaskDays` |
| 16.3 | Panel: selector a dos opciones, cuadrante de turnos, importar por modo | release desde `main` con solo los commits del TDR-008 (el `staging` del panel puede traer más), PR a `main`; Vercel publica |
| 16.4 | Comprobar | una persona de prueba en semanal: cargar una semana desde el panel, ver el lunes libre y fichar contra el turno; una en «Horario por tareas»: bajar la plantilla y ver su pestaña por tareas |

**Registro, 2026-10-22 (UTC), a mano y sin Actions:**

| Paso | Resultado |
|---|---|
| 16.1 API | Release `release/cuadrante-turnos` desde `main` con `staging`. Tres conflictos en `services/assistant` contra b868dc3 (la versión parcial que la sesión del asistente había subido sin el cambio de `proponer_cuadrante`): resueltos con la de `staging`; el árbol resultante es **idéntico** al de `staging` (QA 54+55 26/26). PR #217 fusionado con `[skip ci]` (4ddaf5c), sin workflow. En el servidor: `git pull`, `build --no-deps` de checkinbiz, analytics, merlin, assistant, tasks y reports, `restart nginx`; los siete sanos, `/health` 200 |
| 16.2 Función | `weeklyFromTaskDays` en `encodebiz-services` con `--solo`: «Successful update operation» |
| 16.3 Panel | Release desde `main` con solo b7529d33 (cherry-pick; los idiomas, resueltos desde `main` más las claves de este cambio, sin nada de vacaciones). PR #116 fusionado (36f5ba3e); Vercel Production `success` a las 17:22 |
| Sincronización | `main → develop` en API (a654a90) y panel (db27ae28) |
| Sondas | `/health` 200; `GET /calendar/days` y `GET /calendar` sin sesión, 401; logs de checkinbiz, merlin y assistant sin errores al arrancar |
| 16.4 Prueba con sesión | **la hace Jose en producción** |

Entre las 15:31 (PR #115) y las 17:22 el panel de producción ofreció «Calendario» en empresa y
sucursal. El espejo de Postgres (15:20) no cubre esa ventana; con el código nuevo, quien lo tenga
guardado funciona como semanal, así que no hace falta limpiarlo.

**16 bis, 2026-10-22:** #218 (por tareas sustituye la semana; `pasarASemanal` en el asistente), a mano: merlin y assistant reconstruidos y sanos, `restart nginx`, sin workflow.

**16 ter, 2026-10-22 (noche), TDR-009 «tres modos» — EJECUTADO el back; el panel PENDIENTE.** Orden de Jose: «despliega en prod, estamos probando ahí».
- API `main` 869cc51 en el servidor (`git pull --ff-only`); reconstruidos checkinbiz, analytics, merlin, assistant, tasks e inventory (los que usan los resolutores del horario), todos *healthy*; `restart nginx`. Comprobado en el contenedor: `days_require_calendar_mode` presente. QA 55 en staging antes: 9/9.
- Functions: `desplegar.mjs --project encodebiz-services --solo onTaskDay,weeklyFromTaskDays,employeePlanifierWorker,planifierNotificationWorker,taskStartNotificationWorker`, «Deploy complete» (llevan el `shared` nuevo).
- Sin migración. 0 días cargados en prod antes del pase (TDR-009 §4.6).
- merlin: la revisión del cuadrante según el modo (por turnos no habla de tareas; en «Semana tipo» se bloquea), PR #222, f7b32d3, merlin reconstruido en prod y staging.
- **Panel EJECUTADO:** PR #119 del panel (staging → main, 808788fa), Vercel *success*. Sin variables nuevas.

## 17. Avisos de tareas agrupados — EJECUTADO en prod el 2026-10-28 (orden de Jose: «sí, súbelo»)

Diseño: [ingenieria/avisos-agrupados](../ingenieria/avisos-agrupados/README.md). Asignada,
cambiada y retirada ya no se mandan una a una: se apuntan en `push_digest` y sale **un aviso por
persona** al minuto sin novedades («Tienes 84 tareas nuevas del 3 al 30 de noviembre»). Una
tarea suelta llega como siempre, hasta ~2 min más tarde. El tipo del aviso no cambia. Reconfirmar
un cuadrante sin cambios ya no avisa (también arregla el resumen por correo).

**En dev el 2026-10-28** (orden de Jose: «súbelos, eso es importante»): develop `f1401cc`,
staging `d0a6187`. Función `taskPushDigests` (y `workEmailDigests`, por el cambio de
`mergeWorkEvents`) desplegadas en `dev-encodebiz` a las 15:59 UTC; `tasks` reconstruido en el VPS
a las 16:02. Con TSK-19 (7/7) y HPT-17 (22/22) en verde, la función mandó agrupados sin fallos
(`{ sent: 2..5, failed: 0 }` por minuto). En prod, 17.1 lleva también `workEmailDigests`.

**En prod el 2026-10-28.** El código llegó a `main` con el #233 (otra sesión, 17:10 Madrid),
sin reconstruir `tasks`: el contenedor seguía siendo del 27-oct, así que no se perdió ningún aviso.
16:56 UTC: `taskPushDigests` + `workEmailDigests` en `encodebiz-services` desde `main` `0f6cfc0`
(el primer intento creó la función y falló en IAM; el segundo, «Successful update»; job de
Scheduler `* * * * *` ENABLED). 16:58 UTC: `build --no-deps tasks` + `restart nginx`, tasks
healthy, API 400 (no 502); la función responde 200 cada minuto. Falta 17.3 (tarea real con app)
y 17.4 (app).

**Orden obligatorio: la función antes que el contenedor.** Con `tasks` nuevo y sin
`taskPushDigests`, esos avisos se apuntan y no sale ninguno.

| # | Qué | Cómo |
|---|---|---|
| 17.1 | Función `taskPushDigests` (cada minuto) | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo taskPushDigests,workEmailDigests` — **primero** |
| 17.2 | Contenedor `tasks` | con el pase de la API, `build --no-deps tasks`, **después** de 17.1 |
| 17.3 | Comprobar | crear una tarea a mano para alguien con la app: un aviso en ~1-2 min; `push_digest` vacío después |
| 17.4 | App, siguiente versión | `checkbiz_tasks` + `screen: task_list` → listado de tareas en `notification_navigation_handler.dart`. Sin ella el aviso agrupado se ve, pero al tocarlo solo abre la app |

## 18. Borrar una sucursal con tareas abiertas — EJECUTADO el 2026-10-26 (orden de Jose: «sí, recuerda sin CI»)

Ramas `hotfix/borrar-sucursal-con-tareas` en la API (67b8142) y en el panel (b838f452).
El 26-oct un borrado de dos sucursales en Ayudarte (`OPnlEi3npBbLDyKa4wTj`, una prueba) dejó
306 tareas abiertas colgando de centros inexistentes. `onTaskDay` resuelve el calendario con la
sucursal de la tarea, falla sin decir nada, y los días y **499 alarmas de noviembre** seguían
vivos. Reparado a mano ese día en prod: tareas a `draft` sin `scheduledStartNotificationAt`,
alarmas a `inactive` (`metadata.disabledReason: branch_deleted`), sin enviar ningún push.

Ahora `DELETE /api/v1/branches` con tareas en borrador, asignadas o en curso devuelve 409
`branch/has_open_tasks`. El panel pregunta: a borrador en otra sucursal, cancelar (avisa a los
asignados) o no borrar. Rutas nuevas de tareas: `GET/POST /api/v1/tasks/system/branch-open|branch-close`.

**Orden: la API antes que el panel.** Con la API nueva y el panel viejo, el borrado se para con
un error en inglés, que es seguro. Al revés, el panel manda campos que la API vieja ignora.

| # | Qué | Cómo |
|---|---|---|
| 18.1 | Contenedores `tasks` y `branches` | `build --no-deps tasks branches` + reiniciar nginx |
| 18.2 | Panel | PR del hotfix contra `main` del front (Vercel) |
| 18.3 | Comprobar | borrar una sucursal de prueba con una tarea asignada: aparece el aviso; a borrador → la tarea está en el destino |
| 18.4 | Llevar a `develop` | cherry-pick de los dos commits |

**Hecho, sin CI:** API en `develop` (a173fe5), `staging` (30fd50e) y `main` (#225, 437ae9f), con
`[skip ci]`. Staging y prod reconstruidos a mano (`build --no-deps tasks branches` + nginx).
QA contra staging: SUC-06 (4 casos nuevos), 36, 54 y 55 en verde (47). En prod,
`branches → tasks /system/branch-open` contesta 200 con la clave. Panel: #120 en `main`
(1f67b960), Vercel publicado; `develop` y `staging` del front también. Falta la prueba de
Jose desde el panel.

Queda fuera del hotfix: `onTaskDay` debería resolver con la sucursal actual de la persona, no
con la de la tarea; el aviso de «no iniciada» sale también para borradores con asignados
(`findPendingStartNotifications`); la Cloud Function antigua `deleteBranch` sigue sin bloqueo
(el panel ya no la usa).

## 19. Quién da la tarea por terminada, con encargada — API EN PRODUCCIÓN el 2026-10-26; panel pendiente de la prueba de Jose

Salió de «Formación PRL» en Ayudarte (13 asignadas, la primera que completó la cerró para
todas). La API ya aplicaba «todas» desde el 13-sep, pero el panel no dejaba elegir y al editar
devolvía cualquier tarea a «basta con una». Ahora el formulario ofrece **basta con una / todas /
una encargada** (buscador entre las asignadas). Con encargada, solo ella inicia, pausa y completa
desde la app (403 `task/responsible_only` al resto) y al completar la cierra para todas; la gestión
puede siempre. **Horario por tareas:** el fichaje queda fuera de la regla; la Salida de la
encargada cierra la tarea, la de las demás solo su parte. La encargada tiene que estar asignada y
no se la puede quitar sin elegir otra.

De paso: el aviso de «no iniciada» ya no sale para borradores (`findPendingStartNotifications`
solo `assigned`), que avisaba en las tareas reabiertas o de sucursales borradas.

QA en staging: TSK-19 (5) y HPT-17 (3) nuevos; 46-49 y 54 en verde (64). Función
`taskStartNotificationWorker` ya desplegada en dev.

| # | Qué | Cómo |
|---|---|---|
| 19.1 | Contenedor `tasks` | `build --no-deps tasks` + reiniciar nginx |
| 19.2 | Función `taskStartNotificationWorker` | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo taskStartNotificationWorker` desde la rama (con `shared` compilado de la rama) |
| 19.3 | Panel | PR `fix/politica-de-terminacion` del front contra `main` |
| 19.4 | App, siguiente versión | esconder Iniciar/Pausar/Completar a quien no es la encargada; hoy le sale el error del servidor |

**Hecho, sin CI:** API #226 en `main` (5016e5c), `tasks` reconstruido en prod + nginx, sano.
`taskStartNotificationWorker` desplegada en `encodebiz-services` (paquete con `status in
["assigned"]`). Panel: rama en `develop` del front (6f532407); PR #121 contra `main` **sin
fusionar** hasta que Jose lo pruebe en local.

## 18. Tareas con responsable: ser gestor no exime — API EN PROD el 2026-10-27 12:57 UTC (hotfix #227); panel EN PROD el 27-oct (PR #121)

Diseño: [tasks-service/09_encargada](../ingenieria/tasks-service/09_encargada.md). Visto en prod
el 27-oct (tarea «Prueba», Encodebiz): un gestor asignado, que no era el responsable, la inició.
Ahora solo la persona responsable la inicia, pausa y completa; la excepción de gestión vale solo
para quien no está asignado. En «Por tareas», el fichaje de otra asignada solo mueve su parte.

| # | Qué | Cómo |
|---|---|---|
| 18.1 | Contenedor `tasks` | **HECHO 2026-10-27 12:57 UTC**, orden de Jose («mete esto por hotfix y despliega sin ci»): `hotfix/responsable-solo-ella` desde `main`, PR #227 `[skip ci]`, en `/opt/encodebiz-api` `git pull --ff-only` (0a9b6b9) + `up -d --build --no-deps tasks` + `restart nginx`. `tasks` healthy, «Listening on :3006», la API responde por nginx (sin 502). En `develop` (313a668) |
| 18.2 | Panel: «Responsable» en vez de «Encargada» | **HECHO 2026-10-27**, orden de Jose («listo despliega el panel»): PR #121 (selector de quién termina + «Responsable») fusionado a `main` (a239c317), Vercel en verde. En `develop` del front (f99f8bad) |
| 18.3 | QA | TSK-19 (incluido 19-06) y HPT-17: PENDIENTE de pasar en staging (staging aún no tiene el cambio) |
| 18.4 | App, siguiente versión | esconder botones a quien no es responsable; mostrar `task/responsible_only`; «Tu parte está hecha» si la tarea no se cierra |

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

## 20. Panel de dirección y registro de uso del conector — EJECUTADO el 2026-10-28 (orden de Jose: «bajalo a prod»)

Diseño en `DOCS/ingenieria/panel-de-direccion/README.md`. Dos servicios y una migración.

**Lo que sube**
- Migración **044** `assistant_tool_calls` (aplicada en dev el 28-oct). A mano por SSH, antes
  que los contenedores; sin ella el conector sigue funcionando y sólo avisa en el log.
- Contenedor `assistant`: apunta cada llamada a una herramienta (sin argumentos).
- Contenedor `backoffice`: `GET /api/v1/backoffice/direccion` y la pantalla «Dirección»
  (entrada por defecto del panel). Sin variables nuevas; opcional
  `BACKOFFICE_ENTIDADES_INTERNAS=id1,id2` para excluir empresas nuestras que el nombre no delata.

**Guion**: `psql < migrations/044_assistant_tool_calls.sql` → `git pull` → build `--no-deps`
de `assistant` y `backoffice` → reiniciar nginx → abrir `/backoffice/direccion` y comprobar que
el aviso «todavía no se mide» no aparece.

**Si algo falla**: la pantalla vieja `/stats` sigue intacta; la tabla puede quedarse vacía sin
consecuencias.

**Hecho, sin CI (28-oct, 11:11–11:20 UTC):** `develop` (bccbd83) → `staging` (b5dacae) → `main`
(#228, c5d5fe2), con `[skip ci]`. Staging reconstruido a mano y comprobado (401 en
`/direccion`, SPA servida). Prod: migración 047 en `encodebiz_analytics` (tabla vacía), `git pull`,
`up -d --build --no-deps assistant backoffice`, nginx reiniciado; los dos contenedores sanos.
Falta: la primera lectura de Jose en `/backoffice/direccion` y, si hace falta, poner en
`BACKOFFICE_ENTIDADES_INTERNAS` los ids de empresas nuestras que el nombre no delata.

## 21. «Estadísticas» pasa a Comercial como «Conversión Ads» — EJECUTADO el 2026-10-28 (orden de Jose: «directo a prod»)

Jose, al ver prod: «las estadísticas siguen siendo la misma mierda […] llévatelo a los CRM y le
pones Conversión Ads». Solo SPA del backoffice: la serie diaria sale del bloque principal y
va al grupo Comercial con leads, leads buenos, clics a WhatsApp, medidas en GA4 y lo que se
pierde (sin medir, sin avisar). `/stats` redirige a `/conversion-ads`. Sin migración ni variables.

**Hecho, sin CI:** `develop` → `staging` (0cc4add) → `main` (#229, f3bed96), con `[skip ci]`;
staging y prod reconstruidos a mano (`build --no-deps backoffice` + nginx).

## 22. CRM: historial y cierre de acciones, etapas que se corrigen (issue #201) — EJECUTADO el 2026-10-28 (orden de Jose: «baja lo pendiente a prod»)

Diseño en `DOCS/ingenieria/sales-crm/tdr/TDR-010-historial-y-cierre-de-acciones.md` (§1-§7) y
ADR-003 revisado. Dos servicios y una migración.

**Lo que sube**
- Migración **045** `sales_crm_historial`: canal `comment` en actividades y acciones,
  `sales_activities.in_reply_to`, y cada cuenta abierta con `next_action` escrito gana una acción
  `note` pendiente si tenía fecha, o una nota en la cronología si no la tenía (en prod, 27 de 65
  textos sin fecha eran comentarios, no tareas). `created_by`/`actor` = `migracion:045`. Idempotente. Las columnas `next_action*` se
  quedan sin leerse: **PENDIENTE** borrarlas en un pase posterior.
- `sales`: «Hecho» idempotente, respuesta enlazada, próxima acción derivada, cronología paginada,
  `crm_list_activities` (19 herramientas MCP), perfil exigido al planificar y no al registrar,
  cambio de etapa a cualquier otra con `note`, trial/won sin `entityId` obligatorio. La agenda
  diaria pierde las secciones por cuenta.
- `backoffice` (API + SPA): ruta `GET /crm/accounts/:id/activities`, cronología, próxima acción,
  diálogo de etapa nuevo, avisos en rojo, etapa desde la ficha de contacto.
- Sin variables nuevas.

**Guion**: `psql < migrations/045_sales_crm_historial.sql` → `git pull` → build `--no-deps` de
`sales` y `backoffice` → reiniciar nginx → `ps` → lectura de comprobación.

**Si algo falla**: la migración solo añade (constraint ampliado, columna nula, filas `note`); el
código anterior la tolera. Volver a la imagen anterior de `sales`/`backoffice` basta.

**Staging (28-oct, 11:40–11:50 UTC):** `develop` (5103e0f) → `staging` (98e07c6), `[skip ci]`.
045 aplicada en `encodebiz_staging` (0 cuentas con `next_action`). `sales` y `backoffice`
reconstruidos, sanos. Recorrido con cuenta de prueba «QA TDR-010» (id 4, queda en dev): alta con
`nextAction` → nota; reunión sin perfil → 201, `contacted`, `withoutProfile: true`; etapa a mano a
`demo` con `note` → 200; cronología 2 entradas; MCP 19 herramientas con `crm_list_activities`.
Proxy del backoffice: `/crm/accounts/4/activities` → 401 sin sesión (ruta montada).

**045 ajustada antes de prod** tras leer prod (solo lectura): `c62553b`, por `develop` (a10e9dc) y
`staging` (6d59e14) con `commit-tree` porque `develop` estaba abierta en el checkout principal; en
dev reaplicada (0 filas).

**Producción (28-oct, ~12:15 UTC):** PR #230 → `main` (20a3d48), `[skip ci]`, 37 ficheros. En
`/opt/encodebiz-api`: `git pull`, 045 en `encodebiz_analytics` → **38 acciones** creadas (textos con
fecha) y **27 notas** en la cronología (sin fecha), constraints con los nombres esperados;
`up -d --build --no-deps sales backoffice`, nginx reiniciado, los tres sanos. Lectura de
comprobación: listado 200 (35/100 con próxima acción, 10 con vencidas), ficha coherente, cronología
con `inReplyTo`, agenda de hoy 18 acciones, MCP 19 herramientas, proxy `/crm/accounts/1/activities`
→ 401 sin sesión. Sin errores en los logs.
**Después:** PENDIENTE la prueba de la responsable de marketing en `/backoffice/crm` y reinstalar
el plugin de Cowork (skills `crm` e `investigar-cuenta` cambiadas); el conector de claude.ai puede
necesitar reconectarse para ver `crm_list_activities`.

## 23. CRM: sección de Contenido (ADR-011, TDR-011) — EJECUTADO el 2026-10-28 (orden de Jose: «sube», «prod»)

Marketing planifica contenido (perfiles, fichas, publicaciones con estado y pistas de texto,
imagen y revisión), sube su Excel del plan editorial y los agentes lo leen por el MCP.

**Lo que sube**
- Migración **046** `sales_content`: 6 tablas, 8 índices y 5 perfiles sembrados (Instagram y
  LinkedIn CheckBiz360, Blog, LinkedIn e Instagram encodeBiz). Solo añade.
- `sales`: API `/crm/content/*`, importación del Excel (`exceljs` + `jszip`, ya en el lock del
  monorepo), 11 herramientas MCP (30 en total).
- `backoffice` (API + SPA): proxy, subida de imágenes/PDF al bucket del sistema en
  `crm/contenido/…` (no cuenta para el cobro de almacenamiento), ficheros servidos con sesión,
  pantalla «Contenido» en Comercial.
- **nginx** (`nginx/nginx.conf`, montado): `location /api/v1/backoffice/crm/content/` con
  `client_max_body_size 22m`. Tras el `git pull`, `nginx -t` y reiniciar.
- Sin variables nuevas (usa `FIREBASE_STORAGE_BUCKET`, ya presente en el backoffice).

**Guion**: `psql < migrations/046_sales_content.sql` → `git pull` → `build --no-deps sales
backoffice` → `nginx -t` → reiniciar nginx → lectura de comprobación (`/content/profiles`,
`/content/items`, MCP 30 herramientas) y POST de 5 MB a `/api/v1/backoffice/crm/content/import`
sin sesión → 401 (no 413).

**Si algo falla**: la migración solo crea tablas nuevas; volver a la imagen anterior de `sales` y
`backoffice` basta. El bloque de nginx se puede quitar sin afectar a nada más.

**Staging (28-oct):** `develop` → `staging` (ba8fb91) con `[skip ci]`; 046 aplicada en
`encodebiz_staging`; `sales`, `backoffice` y nginx reiniciados, sanos. Importado el Excel real de
marketing (`Plan_editorial_CheckBiz360_actualizado_28-10-2026.xlsx`): simular no escribe; aplicar →
18 fichas, 45 publicaciones (31 + 14 ya publicadas), 6 dependencias, 2 notas de perfil, 0
problemas; reimportar → 0 creadas. MCP: un agente que valida sin petición recibe
`approval_requires_person`. Storage desde el backoffice: escribir/leer/borrar en `crm/contenido/`
OK. nginx: 5 MB a `/crm/content/import` → 401; a otra ruta del backoffice → 413.
Destapó y se arregló en staging: el tipo de evento no cabía con el nombre del fichero (y un error de
base contaba como 62 «problemas»), y las fechas `t="d"` del Excel salían en 1905.

**Producción (28-oct):** PR #231 → `main` (61f3eeb), `[skip ci]`, 45 ficheros. En `/opt/encodebiz-api`:
`git pull`, 046 en `encodebiz_analytics` (6 tablas, 8 índices, 5 perfiles), `up -d --build --no-deps
sales backoffice`, `nginx -t` correcto, nginx reiniciado; los tres sanos. Lectura de comprobación:
perfiles 5, publicaciones 0, ya publicado 0, ficha de empresa con `content`, MCP 30 herramientas,
bucket `encodebiz-services.firebasestorage.app`; 5 MB a `/crm/content/import` → 401, a otra ruta del
backoffice → 413; SPA 200; sin errores en los logs. **No se importó nada en prod**: el Excel lo sube
marketing desde la pantalla. Sin prueba con sesión real todavía (PENDIENTE: marketing).
**Después:** reinstalar el plugin de Cowork (skills `crm`, `outreach`, `marca-personal`); el
conector de claude.ai puede necesitar reconectar para ver las herramientas de contenido.

## 24. Hotfix: el menú del backoffice marca la sección activa — EJECUTADO el 2026-10-28 (orden de Jose: «hotfix a prod»)

El menú lateral no resaltaba ninguna sección: `NavLink` pone la clase `active` y MUI solo pinta
`Mui-selected`. Ahora `selected` va en el enlace más largo que contiene la ruta (`/crm/12` marca
CRM; `/crm/contenido/fichas/3`, Contenido). Solo `apps/backoffice-web/src/layout/Shell.tsx`.

**Producción:** PR #232 desde `main` → 9eb15ad, `[skip ci]`. `git pull`, `up -d --build --no-deps
backoffice`, `nginx -t` correcto, nginx reiniciado; sano. La SPA servida cambia de `index-DUCxQn2S.js`
a `index-D96Eiq2W.js`. **develop** (d707560) y **staging** (13eda0f) con el mismo cambio; desplegado
en dev. En el VPS de dev el `git pull` necesita `GIT_SSH_COMMAND="ssh -i ~/.ssh/github_deploy -o
IdentitiesOnly=yes"`: no hay `~/.ssh/config` que use la clave de despliegue.

## 22. Foto diaria de dirección (048) y bloque de crecimiento — EJECUTADO el 2026-10-28 (orden de Jose: «vale, inténtalo de nuevo»)

Jose, al revisar «Dirección» en prod: «no me estás poniendo estadísticas ni gráficos de
crecimiento ni previsiones de cobro […] lo que tienes que hacer es un snapshot diario de
históricos de estas estadísticas, así tienes históricos». Lista de campos aprobada por él
(«por el momento no me falta nada, tú eres el experto»).

**Lo que sube**
- Migración **048** `direccion_snapshot_daily`: una foto por día (zona Madrid) con tamaño,
  uso, dinero y asistente, sólo clientes reales. A mano, antes del contenedor.
- `backoffice`: cosecha a las 3:20 detrás de la de estadísticas, hueco de ayer al arrancar,
  `POST /direccion/snapshot?date&from`, script `foto-direccion.js`, y bloque «Crecimiento» en
  la pantalla (titular semana vs semana, tabla semana/mes, curvas a 26 semanas, previsión de
  cobro con pruebas que vencen y tendencia a 4 y 12 semanas).

**Guion, en orden**
1. `psql -d encodebiz_analytics < migrations/048_direccion_snapshot_diario.sql`
2. Fusionar PR #233 (`staging → main`, `[skip ci]`); en `/opt/encodebiz-api`: `git pull --ff-only origin main`
3. `docker compose --env-file .env.production up -d --build --no-deps backoffice` + `restart nginx`
4. Relleno hacia atrás (idempotente, ~1 s por día):
   `docker compose exec -T backoffice node services/backoffice/dist/scripts/foto-direccion.js --from 2025-09-01`
5. Abrir `/backoffice/direccion`: el bloque «Crecimiento» tiene que decir «N de N fotos son reconstruidas» y no «sin fotos».

**Hecho:** `develop` → `staging` (cd6d224), con `[skip ci]`. Staging reconstruido, migración 048
aplicada en dev y 57 días rellenados (1-sep a 27-oct); comprobado el cálculo con datos reales.
**En prod (28-oct, 17:30–17:45 UTC):** #233 fusionado (0f6cfc0), 048 aplicada en
`encodebiz_analytics`, `backoffice` reconstruido, nginx reiniciado, **422 fotos** rellenadas
(1-sep-2025 → 27-oct-2026, sin parciales). Primera lectura: 14 clientes, 110 de plantilla,
8 pagando, 214 € de cuota estimada; este mes frente al anterior: plantilla 62 → 110, cuota
102 → 214 €, fichajes 371 → 957. La cosecha de cierre empieza con la foto del 28-oct (3:20 del 29).

**OJO, lo que entró en `main` con #233 sin desplegarse:** `develop` traía trabajo de otras
sesiones (sales, analytics, shared, firebase_sdk, billing, migración 047 alertas por correo).
Sólo se reconstruyó `backoffice`. Quien lleve §16 (alertas) y lo de analytics/firebase_sdk tiene
que saber que su código ya está en `main` y en `/opt/encodebiz-api` sin contenedor nuevo.

## 23. Dirección: la prueba la sabe Stripe — EJECUTADO el 2026-10-28

Jose, en prod: «Pagando · en prueba · gratis 8 · 0 · 6 está mal, en pruebas hay uno (Ayudarte)».
En Firestore `entities/*/subscriptions/checkinbiz` se queda en `active` desde el alta y
`endTestPeriod` no se rellena: la prueba (45 días) sólo la conoce Stripe (`trial_period_days`).

- `billing`: ruta interna S2S `GET /api/v1/billing/internal/subscriptions/stripe` (todas las
  suscripciones de Stripe con estado, inicio y fin de prueba, empresa y servicio de los metadatos).
- `backoffice`: `BillingClient`; cruza Firestore con Stripe; `trialing`/`trial_end` mandan; si
  billing no responde, sigue con Firestore y lo dice en la pantalla y en la nota de la foto.

**Hecho, sin CI:** develop → staging (2b417fe) → main (#234, dce9c6c). Prod: `billing` y
`backoffice` reconstruidos, nginx, y las 422 fotos reescritas con los días de prueba. Resultado:
7 pagando · 1 en prueba · 6 gratis; Ayudarte en prueba hasta el 30-oct (40 €/mes si sigue).

**OJO:** reconstruir `billing` llevó a prod también lo que `main` traía de otras sesiones en
`shared` (alertas por correo, plantillas ALERTS_*): compila y arranca («Stripe en modo REAL»),
pero es código ajeno que entró sin su pase. Quien lleve §16 debe saberlo.

Pendiente menor: en la foto, «gratis» cuenta sólo suscripciones `freemium`; en el pulso cuenta
también las empresas sin suscripción (3 en prod). La tabla de crecimiento no enseña «gratis», así
que no se nota; alinear en la próxima tanda.

## 25. Hotfix: el alta escribe siempre `enableA2F` y `biometricRequired` — EJECUTADO el 2026-10-29 (orden de Jose: «despliega», «hot fix urgente»)

9 de los 28 empleados de Neteges Bisbal (`eR5gNPUdmipJtxUZskub`) no podían fichar. La app les pedía
un código del autenticador y el servidor respondía `twofactor/not_activated`. Las fichas venían
de la puesta en marcha del 05-oct y no tenían `enableA2F`. El panel muestra ese campo vacío como
desactivado, pero el servidor y la app lo tratan como activado. Además, la celda
`biometria_obligatoria` vacía se leía como «no». Con A2F activado y sin biometría, el móvil nunca
queda como de confianza.

- **Datos (prod):** `enableA2F: false` a los 9; antes se pasó una simulación y después se
  comprobó cada ficha.
- **Código:** `createEmployee` (shared) escribe siempre `enableA2F` (`false` por defecto) y
  `biometricRequired` (`true` por defecto). La puesta en marcha lee la celda de biometría vacía
  como «sí».
- **Reproducido en staging** contra la API: 401 `untrusted_device` → `not_activated`; con
  `enableA2F: false`, 201.

**Hecho, sin CI:** PR #236 → `main` (5427b85). Prod: `git pull --ff-only` y se reconstruyeron
`employees`, `merlin` y `rentman` (healthy, con el código nuevo dentro), y se reinició nginx.
Llevado a develop (ace8043). Staging no se ha reconstruido.

Barrido de prod: nadie más bloqueado. Quedan 6 fichas sin `enableA2F` (Mayo Software, Lorem
ipsum, ACB2, Mi empresa SA), todas con la biometría activada.

Pendientes:
- Los 24 empleados de Neteges siguen con la biometría desactivada. Activarla es decisión del
  cliente.
- En la app, ante `not_activated`, llevar a configurar el autenticador en vez de repetir el
  diálogo del código.

## 26. Informes de una, varias o todas las sucursales — EJECUTADO el 2026-10-29 (orden de Jose: «despliega a prod todo ya»)

El informe de jornada y el de tareas aceptan `branchIds` (ninguna = todas); `branchId` se sigue
aceptando porque lo usa el conector. En el panel, el campo de sucursal es ahora el buscador de la
asignación de empleados (índice en servidor). Antes la lista se cargaba con `limit: 100`, y
Neteges tiene 138 sucursales.

**Hecho, sin CI:**
- API: PR #237 → `main` (fe0fcd8), con solo el commit de `reports` sacado de `main` en
  cherry-pick. Prod: se reconstruyó `reports` (healthy) y se reinició nginx.
- Panel: PR #122 → `main` (fb5f5169) con solo este commit. Vercel Production en success.

En el panel, `develop` lleva dos commits de otras sesiones que NO han ido a main: «Responsable»
en tareas (e321e741) y el modo de horario independiente de «Horario base» (03e0648e).

Probado en staging contra la API: una, dos, todas y el `branchId` antiguo → 201 con las
sucursales correctas. Tareas → 204 sin errores. Falta probarlo en prod con Neteges (138).

## 27. Hotfix: el trabajador no ve los borradores en los que figura — EJECUTADO el 2026-10-29 (orden de Jose: «arréglalo como hotfix», «súbelo todo a prod»)

En CENTRO DE FORMACIÓN AYUDARTE (`OPnlEi3npBbLDyKa4wTj`), los empleados veían en la app tareas
en borrador. Eran las 302 que la reparación del 26-oct (§18) pasó a `draft` dejando a la persona
asignada. Un borrador con gente dentro también sale de borrar una sucursal con «a borrador», o
de reabrir una tarea.

**Datos, antes del arreglo (orden de Jose):**
- Se borraron las 302 en BD, con la cascada del servicio: subcolecciones (1313),
  Storage (0 ficheros) y `tasks_raw.deleted_at`.
- No se llamó a `notifyTaskRemoved` ni se emitió `task.deleted`, así que no hubo avisos.
- Copia completa en `/Volumes/Externo-1/Checkbiz360-Copias-produccion/2026-10-29-ayudarte-borradores/`.
- Después del borrado no queda ningún borrador en ninguna empresa de prod.

**API: PR #238 → `main` (568376f).** Para quien solo es trabajador:
- `GET /tasks` filtra los borradores;
- el calendario los quita de las celdas y de la leyenda (`hiddenStatus`);
- el detalle y la actividad devuelven 403 (`canViewTask`).

Prod: se reconstruyó `tasks` (healthy) y se reinició nginx. Cherry-pick a `develop` (8e12ab6).

**App: PR #56 → `master` (4ff2238), versión 1.10.1+69.** La lista de Tareas del trabajador
(stream de Firestore) deja fuera los borradores. Cherry-pick a `develop`. **No está publicada en
tiendas**: hasta que lo esté, la app instalada sigue enseñando un borrador con gente dentro.

Pendiente:
- Publicar 1.10.1+69.
- Decidir si, al pasar las tareas a borrador por borrar su sucursal, se saca de ellas a la gente
  (cortaría el problema en las apps ya instaladas).

## 28. Alertas por correo, fase 3b: pendientes de decisión — EJECUTADO el 2026-10-29 (orden de Jose: «bájalo a prod, todo llegó bien»)

Diseño: `ingenieria/alertas-por-correo/README.md` §12. Owner y admin reciben, en el resumen de
la mañana, solicitudes por decidir, incidencias abiertas por la plantilla y documentos sin
firmar; y al momento, la solicitud que empieza en menos de 48 h, la incidencia nueva de una
persona y el documento firmado.

Servicios: `shared` (textos, plantilla inmediata genérica, `reportPendingAlert`), `analytics`
(pendientes en el resumen, `POST /api/analytics/alerts/pending`, job «solicitudes próximas» a
:05), `documents` (avisa al guardar el acuse), `billing` (solo por el script de plantillas) y
`firebase_sdk` (`onCreateIssues`).

Fuera del código, por este orden:

1. Sin migración: usa las tablas de la 047.
2. Desplegar `analytics`, `documents` y `billing` (el `--no-deps` de siempre).
3. Plantillas: `node services/billing/dist/scripts/email-templates.js --apply --replace` en el
   contenedor de billing. **Con `--replace`**: `ALERTS_IMMEDIATE` cambia (entrada y botón los
   pone el código). Mirar antes, sin `--apply`, que lo único distinto sea `ALERTS_IMMEDIATE`; si
   sale otra plantilla, alguien la retocó a mano y no se pisa sin preguntar.
4. `firebase deploy --only functions:onCreateIssues --project <dev-encodebiz | encodebiz-services>`
   desde `services/firebase_sdk`. Comprobar antes qué `onCreateIssues` corre en cada proyecto
   (este o el del SaaS): si es el del SaaS, el inmediato de incidencias no sale, pero el resumen
   sí las cuenta. `ANALYTICS_SERVER_URL` y `ANALYTICS_API_KEY` ya están en los `.env`.
5. Prueba en dev: una solicitud pendiente con inicio mañana (aviso en la siguiente :05), una
   incidencia abierta desde la app y un acuse firmado; los tres en `email_outbox` y en
   `alert_sent` con `channel = 'immediate'`.

**Staging, 2026-10-29 (orden de Jose: «despliega en staging»).** `develop` → `staging` (92a9c59) a
mano, Actions sigue parado; reconstruidos `analytics`, `documents`, `billing` y `tasks` (entró el
hotfix 8e12ab6, que faltaba en staging). Plantillas en dev con `--replace`: las cuatro de
alertas; `ALERTS_DIGEST` también difería, solo por el pie de #235 (y ahora el pie lleva a
Herramientas → Alertas por correo). `onCreateIssues` desplegado en `dev-encodebiz` con
`desplegar.mjs --solo onCreateIssues`: en dev es el de `firebase_sdk` (se actualizó, no se creó).
Prueba en EncodeBiz S.L (`Wl8ZCvpdmIXzEE0mhT7W`, solo jose@): solicitudes, incidencia, dos
documentos y un acuse con «[PRUEBA alertas]» y plantilla `seed-emp-0x`; salieron los cuatro
correos (documento firmado, incidencia nueva, solicitud próxima y resumen con tres pendientes).
Ojo: EncodeBiz no tiene fichajes en 30 días y no cuenta como activa; el resumen y la pasada de
solicitudes se lanzaron a mano solo para ella.

**Producción, 2026-10-29.** #239 (staging → main) chocaba con los squash de #235; cerrado y
sustituido por #240 (`release/alertas-pendientes`, el árbol exacto de staging encima de main,
squash d77ca31). En `/opt/encodebiz-api`: `git pull`, `up -d --build --no-deps analytics
documents billing`, `restart nginx`; los tres sanos, planificador con «solicitudes próximas a
:05». Plantillas con `--replace`: las cuatro de alertas, comprobado antes que en prod solo
diferían el pie (#235) y las líneas cambiadas del inmediato. `onCreateIssues` desplegado en
`encodebiz-services` con `desplegar.mjs --solo onCreateIssues`: era el código del SaaS; el
portado solo cambia los imports, el título «CheckBiz360» y el aviso a analytics.
`onIssuesResponse` sigue con el del SaaS.

**Probado en prod el 29-oct con la app 1.10.1+69.**
- jose@encodebiz.com en Encodebiz se bajó a trabajador, con copia de su responsabilidad de manager.
- Se creó un borrador para el 30-oct asignado a él, sin avisos.
- Jose confirmó que en Tareas no le sale.
- Después se borró la tarea (en `tasks_raw` quedó con `deleted_at`) y se le devolvió el rol de manager.

## 29. Adjuntos en la tarea (TDR-007) — EJECUTADO el 2026-11-02 (orden de Jose: «a prod»); queda la app

Diseño: `ingenieria/tasks-service/tdr/TDR-007-adjuntos-en-la-tarea.md`. Un recurso de la tarea con
`isEvidence: false` es un adjunto (el expediente de la clienta en ayuda a domicilio): no cuenta
como evidencia ni en el informe, no avisa, y el duplicado lo lleva como referencia al mismo
fichero (`tasks/adjuntos/`, se cobra una vez). Ruta nueva `DELETE /:taskId/resources/:resourceId`.
Sin `isEvidence` es evidencia: la app instalada no cambia.

Servicios: `shared` (tipo y repositorio), `tasks` y `reports`. Commits 291af10 y 312b516.

Fuera del código, por este orden:

1. Sin migración.
2. **Exención de índice de grupo** para `resources.storagePath` en `encodebiz-services`.
   `gcloud firestore indexes fields update` no admite el ámbito de grupo: se hace con la API REST
   (PATCH del campo con `updateMask=indexConfig`), conservando los tres índices de colección por
   defecto y añadiendo `COLLECTION_GROUP` ascendente. Mirar antes con
   `gcloud firestore indexes fields describe storagePath --collection-group=resources --project encodebiz-services`.
   Esperar a `READY`. Sin ella, quitar un adjunto funciona pero el fichero se queda en Storage
   (log «no se pudo contar quién más usa…»).
3. Desplegar `tasks` y `reports` (el `--no-deps` de siempre) y `restart nginx`.
4. Panel: check «Es evidencia del trabajo hecho» al adjuntar y la ficha con «Documentos adjuntos» y «Evidencias». En `develop` del panel (8c49429b, 30-oct); a prod con su PR a `main` y Vercel, **después** de `tasks`.
5. App: no bloquea; la 1.10.x enseña el PDF con icono de foto y lo abre fuera. Adjuntar al crear y editar, y la ficha separando adjuntos de evidencias, en `develop` de la app (ebaeff9, 30-oct; nueva dependencia `file_picker`): sale con la próxima versión, que debe publicarse **después** de `tasks` en prod (sin el servidor nuevo, el adjunto subido desde la app contaría como evidencia).

**Staging, 2026-10-29 (orden de Jose: «sí»).** `develop` → `staging` a mano (2d97ddd y 268200b,
Actions sigue parado); `git pull` en el VPS y reconstruidos `tasks` y `reports`. Exención de
índice creada en `dev-encodebiz` por REST (solo `ADD` del de grupo; READY en unos minutos). QA
desde el portátil contra staging: `55-tareas-adjuntos` 12/12, y 46, 47, 50, 51 y 54 sin regresión
(98/98).

**Producción, 2026-11-02 (orden de Jose: «a prod», tras validar en staging).** Ver §30, que fue en el mismo pase.

## 30. Casillas de la descripción (TDR-008) y aviso agrupado con fechas — EJECUTADO el 2026-11-02 (orden de Jose: «a prod»)

`PATCH /:taskId/description` (el trabajador marca casillas; cada cambio deja `description_updated`
con la casilla), el duplicado con las casillas sin marcar (D6) y el push agrupado con
`dateFrom`/`dateTo`. Sin migración ni variables.

| Paso | Qué | Hora (UTC) | Resultado |
|---|---|---|---|
| 29.2 | Exención de índice de grupo `resources.storagePath` en `encodebiz-services`, por REST | 12:27 | Solo `ADD` del `COLLECTION_GROUP`; los tres de colección intactos. `READY` hacia las 12:40 |
| 30.1 | API `staging → main` | 12:27 | PR checkbiz-api#241, merge `a527b9a`. El árbol fusionado = `staging` (los hotfixes de `main` ya estaban con otro hash) |
| 30.2 | Despliegue | 12:28–12:29 | **Actions vuelve a funcionar**: Production CI/CD 41444891438 en verde (1 min 41 s). 17 servicios `healthy`, nginx reiniciado por el CI; `tasks` con el código nuevo |
| 30.3 | `taskPushDigests` | 12:32 | `desplegar.mjs --project encodebiz-services --solo taskPushDigests` desde un worktree de `main`, con `.env.encodebiz-services` copiado (sin él la función se queda sin configuración: el empaquetador avisa) |
| 30.4 | Panel `staging → main` | 12:34 | PR front#126, merge `9ba6500f`; conflicto solo de comentario en `ITask.ts`, resuelto con el árbol de `staging`. Vercel `Ready` en `saas.encodebiz.com` a las 12:35. Sin variables nuevas: el código lee las mismas claves que el `main` anterior |
| 30.5 | Comprobación | 12:45 | `PATCH …/description`, `DELETE …/resources/:id` y `POST …/duplicate` responden 400 sin `entityId` (existen); `tasks` sin errores en el log |
| 30.6 | App | — | PENDIENTE: publicar la 1.10.1+69 (casillas, adjuntos, historial igual que el panel, responsable, aviso agrupado que abre esos días). Ya puede, porque `tasks` está en prod |
| 30.7 | Manual | — | PENDIENTE: «las casillas no son un estado guardado» (Crear una tarea, ES/EN/PT) se cambia cuando la app esté publicada |


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

## 31. Hotfix: festivos y ausencias desde el conector — EJECUTADO el 2026-11-03 (orden de Jose: «bájalo directamente a prod, es un hotfix, los clientes esperan»)

El conector solo leía festivos y ausencias; un cliente no pudo meter los de Madrid (2 y 9-nov,
7, 8 y 25-dic) y el lunes 2 se contó como laborable. Cinco herramientas nuevas en `assistant`:
`ver_festivos`, `crear_festivos`, `crear_ausencia`, `cambiar_festivo`, `borrar_festivos`. Si es
retribuido se pregunta siempre (sin respuesta, `falta_retribuido`), con vista previa y
`confirmacionId`. Solo `services/assistant`; sin migración, variables, índices ni reglas.

| Paso | Qué | Hora (UTC) | Resultado |
|---|---|---|---|
| 31.1 | Rama `hotfix/conector-festivos-ausencias` desde `main` | — | Commit `245b242`, 164/164 tests |
| 31.2 | `develop` y `staging` | ~09:40 | Merges `[skip ci]` `b6ada0f` y `272cc3f`, por `commit-tree`. **Staging del VPS sin reconstruir**: se fue directo a prod por orden de Jose |
| 31.3 | `main` | ~09:41 | PR checkbiz-api#242, merge `a57e337` con `[skip ci]`; no arrancó ningún CI |
| 31.4 | Despliegue | ~09:43 | `/opt/encodebiz-api`: `git pull --ff-only` + `up -d --build --no-deps assistant` (con `--env-file .env.production`) + `restart nginx`. `assistant` `healthy`, `festivos.js` en `dist`, MCP sin token 401 |
| 31.5 | Prueba real | — | PENDIENTE: que el cliente (o Jose) pida al conector meter un festivo y lo vea en el panel. Los conectores ya autorizados tienen que **volver a leer la lista de herramientas** (reconectar o nueva conversación) |
| 31.6 | Staging del VPS | ~09:47 | `git pull` a `272cc3f` + `up -d --build --no-deps assistant` + `restart nginx`; `healthy` |

## 32. Hotfix: descripciones de cuadrante para el escaneo de OpenAI — EJECUTADO el 2026-11-03

El escaneo del portal marcó `proponer_cuadrante` y `confirmar_cuadrante` como «description missing,
blank, or unclear». `confirmar_cuadrante` además decía que no tocaba tareas y en «Por tareas» las
sustituye. De paso, `crear_festivos`/`crear_ausencia` dicen «ya existe» antes de preguntar si es retribuido.

| Paso | Qué | Resultado |
|---|---|---|
| 32.1 | `develop` `8dd390a`, `staging` `c8624ad` (`[skip ci]`) | VPS de dev: `assistant` reconstruido + nginx |
| 32.2 | PR checkbiz-api#243, `main` `04612af` (`[skip ci]`) | Prod: `git pull` + `up -d --build --no-deps assistant` + `restart nginx`; `healthy` |
| 32.3 | Comprobado con la cuenta de revisión (OAuth real, sin 2FA) | 44 herramientas; descripciones nuevas servidas; los ocho casos responden. Las escrituras, solo en vista previa |
| 32.4 | PENDIENTE | `ver_hoy` y `ver_alertas` de Encodebiz enseñan «Servi SAD» y «Encodebiz TEST», sucursales borradas, por sus tareas huérfanas; `listar_sucursales` solo da «Encodebiz» |
| 32.5 | Limpieza de Encodebiz (datos de prod, orden de Jose) | Servi SAD (sucursal borrada): 9 tareas canceladas por `tasks /system/branch-close` (`cancel`). Encodebiz: 18 abiertas anteriores al 02-nov canceladas y «Cocinar doradas fritas…» (23-oct, en curso) completada, por `PATCH /delegated/:id/status` con hola@ como autor. `ver_alertas` sin alertas. **Sigue pendiente:** `ver_hoy` lista «Encodebiz TEST» (borrada) a ceros; el arreglo de fondo es que `analytics` no cuente sucursales borradas |

## 33. Cartera de clientes (MVP + documentos del cliente) — PENDIENTE (en staging el 2026-11-03/04)

Lo que hay en `staging` y no en `main`, por orden de entrada (`git log --first-parent origin/main..origin/develop`):

| Merge en `develop` | Qué | TDR |
|---|---|---|
| `5ab4f25` + `ef81b9f` | Servicio `customers:3018`, clientes y sucursales asignadas; fix nginx de la raíz | [TDR-001](../ingenieria/cartera-de-clientes/tdr/TDR-001-fundacion-y-maestros.md) |
| `0281aa7` | Dirección del cliente (forma del `workSite`) | TDR-001 §Dirección |
| `d73fbdd` + `e0292ac` | El cliente en la tarea: `Task.customerId/customerSiteId/customer`, `/for-task`, dirección del cliente por defecto como valla; fuera la tarifa | [TDR-002](../ingenieria/cartera-de-clientes/tdr/TDR-002-el-cliente-en-la-tarea.md) |
| `7bba626` | Documentos del cliente: `scope: "customer"` en el documental, tipos `customer_*`, `contractsExpiring` | [TDR-003](../ingenieria/cartera-de-clientes/tdr/TDR-003-documentos-del-cliente.md) |

Decisión de alcance: 06 §D11 de la cartera (MVP: sin lugares, sin dedicadas, sin «toda la
empresa», sin horas por cliente; lo que la API conserva de eso no lo usa nadie). **Sin migración
de Postgres, sin reglas de Firestore, sin funciones, sin variables nuevas en la API.** Todo es
aditivo: sin cliente, ningún servicio hace nada distinto.

**Lo que cambia en `shared`** (lo leen casi todos los servicios): `checkbiz/customers/*`,
`searchIndex` (tipo `customer`), `entities/Task` (tres campos opcionales),
`FirestoreTaskRepository.findAll` (filtro `customerId`), `taskCustomerSnapshot`. Por eso en el
pase se reconstruye **todo el stack** (`up -d --build`), no solo `customers`.

### 33.a — Servidor (`/opt/encodebiz-api`, por SSH, el día del pase)

| Paso | Qué | Resultado |
|---|---|---|
| 33.1 | `docker-compose.yml` de prod: bloque `customers`, copiado del de staging (abajo), con `--env-file .env.production` como el resto. Sin variables nuevas: usa las mismas credenciales que `inventory` | PENDIENTE |
| 33.2 | `nginx/nginx.conf` de prod: `upstream customers_service { server customers:3018; }` y las dos `location` de abajo. La exacta (`=`) es obligatoria: sin ella la raíz devuelve 301 y el POST del alta llega como GET (comprobado en staging el 03-nov) | PENDIENTE |
| 33.3 | `git pull --ff-only` a `main` + `docker compose --env-file .env.production up -d --build` (todo: `shared` cambia) + `restart nginx`. Esperar `healthy` en `customers`, `tasks`, `documents` | PENDIENTE |
| 33.4 | Índices compuestos de Firestore en **`encodebiz-services`** con gcloud (los tres existen ya en dev): `tasks (customerId ASC, dueAt ASC)`, `tasks (customerId ASC, createdAt DESC)`, `documents (customerId ASC, createdAt DESC)`. Tardan minutos en construirse; hasta entonces el filtro por cliente de la lista de tareas y la lista de documentos del cliente dan error de índice, nada más | PENDIENTE |
| 33.5 | Comprobación sin token: `curl -s -o /dev/null -w "%{http_code}" https://api.checkbiz360.com/api/v1/customers?entityId=x` → **401** (301 = falta la `location =`; 502 = nginx con IPs viejas → `restart nginx`). Con token de owner de una empresa de pruebas: `GET /api/v1/customers?entityId=…` → lista vacía | PENDIENTE |
| 33.6 | Vuelta atrás: quitar el bloque de nginx y el servicio; las tareas y documentos siguen igual (los campos nuevos son opcionales y el código viejo los ignora). Los índices no estorban | — |

Bloque de compose (igual que `docker-compose.staging.yml`):

```yaml
  customers:
    <<: *service
    build:
      context: .
      dockerfile: services/customers/Dockerfile
    environment:
      - NODE_ENV=production
      - PORT=3018
    volumes: *secret-volumes
    expose:
      - "3018"
    healthcheck:
      <<: *health
      test: ["CMD", "wget", "-qO-", "http://localhost:3018/health"]
```

Bloque de nginx (igual que `nginx.staging.conf`):

```nginx
  upstream customers_service  { server customers:3018; }
  …
    # Customers — cartera de clientes. La lista vive en la raíz sin barra: sin la exacta, 301.
    location = /api/v1/customers {
      proxy_pass http://customers_service;
    }
    location /api/v1/customers/ {
      proxy_pass http://customers_service/api/v1/customers/;
    }
```

### 33.b — Panel (`encodebiz-front-saas`)

Rama `feat/cartera-de-clientes`, **siete commits sin push**, sobre `develop` `9f72ec59`:
`29f380a3` (lista, ficha, sucursales), `5e3cab2a` (zona horaria de la dirección), `06cdab3e`
(fuera la tarifa), `fafac272` (cliente en la tarea), `b7ce6ffd` (MVP: fuera lugares y dedicadas,
dirección por defecto), `ef5b40ff` (cabecera de la ficha), `367b866e` (documentos del cliente).
Dos de ellos son de la otra sesión de Claude (`encodebiz-front-saas-9a`).

| Paso | Qué | Resultado |
|---|---|---|
| 33.7 | Push de la rama, merge a `develop` y de ahí lo que mande el flujo del panel hasta producción (Vercel solo despliega prod; staging del panel es el portátil) | PENDIENTE |
| 33.8 | Variable en Vercel (prod): `NEXT_BACKEND_URI_CHECKINBIZ_CUSTOMERS_HANDLER=https://api.checkbiz360.com/api/v1/customers`. Sin ella el proxy `checkinbiz_customers_handler` responde error de configuración y la pantalla «Clientes» sale vacía con aviso | PENDIENTE |
| 33.9 | Comprobar en prod con una empresa de pruebas: menú «Clientes» → alta con dirección y contactos → en una tarea de esa sucursal aparece «Cliente» y el check de la dirección → ficha con bloque «Documentos»: subir ficha (`worker`) y contrato (`manager`, con fecha de fin próxima) → la cabecera avisa del contrato → Gestión documental filtra por «Cliente» | PENDIENTE |

### 33.c — App (`checkbiz360`)

Rama `feat/cliente-en-la-tarea`, commit `9c8b3ed` sobre `develop` `559ef83` (versión `1.11.1+71`,
la misma que `master`). Añade `customerId`/`customer` al modelo de la tarea, «Cliente: nombre» y
«Ver datos del cliente» en el detalle, y el panel inferior con notas de campo, contactos con
llamada y documentos del cliente (`GET /customers/for-task/:taskId` + descarga del documental).
Sin cliente, la tarea se enseña igual. **Las apps ya instaladas funcionan con la API nueva** (la
valla del cliente les llega como un `workSite` normal).

| Paso | Qué | Resultado |
|---|---|---|
| 33.10 | Merge a `develop` **hecho el 2026-11-05** (`2a53347`, sin CI en el repo de la app). Probar contra dev con `flutter run -t lib/main_development.dart --flavor development --dart-define=ENVIRONMENT=development` (ver `project-app-version-publicada`) en una tarea de la demo de Neteges con cliente: nombre, contactos visibles, ficha visible, contrato NO visible como trabajadora | PENDIENTE |
| 33.11 | Subir versión (`1.12.0+72`), `master`, publicar en tiendas. Solo después de que la API esté en prod (33.3): la app nueva contra la API vieja pide `/api/v1/customers` y recibe 404 → el panel del cliente dice que no se pudieron cargar los documentos, nada más | PENDIENTE |

### 33.d — Lo que no entra en este pase

- `branches-to-customers` (Neteges): descartado hasta tener todo claro (06 §D11).
- Horas por cliente, informe y portal: Fases 3 y 6, sin fecha. Los contratos del cliente y su rentabilidad (Fase 5) van aparte, en §35.
- Columna «Cliente» en la plantilla del cuadrante por tareas: sin decidir.

## 34. Histórico para la previsión: la tarea del fichaje, el puesto con su precio y el historial de la tarea — PENDIENTE (en staging el 2026-11-03/04)

Solo datos: no cambia ninguna pantalla ni ninguna ruta. Es la base de la rentabilidad y la previsión de
la Fase 5 de la cartera (`DOCS/ingenieria/cartera-de-clientes/03_modelo-de-datos.md` §«El histórico»,
ADR-006), que no sale en esta versión (06 §D11). En `develop` `8fb2e8a` y `staging` `cdac13d`
(`[skip ci]`). Sin reglas, sin índices de Firestore, sin variables, sin funciones (`firebase_sdk` no
escribe historial de tareas: compila y no se despliega).

Tres cosas nuevas en Postgres, todas con relleno hacia atrás: `checklogs_raw.task_id` (sale del JSON
`schedule_applied`; la migración lo rellena), `dim_responsibilities.job_name/job_price` más
`responsibility_events` (alta, retirada y cada cambio de puesto o precio; lo siembra el job de
dimensiones en su primera pasada, un evento de alta por responsabilidad con `changed_at = assignedAt`),
y `task_events_raw`, espejo 1:1 de la subcolección `activity` escrito desde `shared` por todos los
servicios que escriben historial (`tasks`, `inventory`, `checkinbiz`).

| Paso | Qué | Resultado |
|---|---|---|
| 34.1 | Migración 050 (`050_historico_prevision.sql`), a mano y **antes** de reconstruir `analytics`: su `INSERT` en `dim_responsibilities` lleva `job_name` y sin la columna el job de dimensiones (minuto 20 de cada hora) falla y queda en `dim_sync_log`. `… psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 < migrations/050_historico_prevision.sql`. Esperado: `ALTER TABLE`, `UPDATE n`, `CREATE INDEX`, `ALTER TABLE` ×2, `CREATE TABLE`, `CREATE INDEX`, `CREATE TABLE`, `CREATE INDEX` ×2. Todo `IF NOT EXISTS`: repetirla no hace daño. En dev: `UPDATE 621` de 10 938 fichajes | PENDIENTE |
| 34.2 | Contenedores, por SSH y sin CI: `git pull` + `up -d --build --no-deps sync analytics tasks inventory checkinbiz` + `restart nginx`. Los cinco llevan `shared` (`checklogsRaw`, `FirestoreTaskRepository.afterActivity`); `analytics` además `SyncDimensions`. Los demás no cambian | PENDIENTE |
| 34.3 | Historial hacia atrás: en el contenedor `tasks`, `node services/tasks/dist/scripts/backfill-tasks.js --entity <una grande> --apply --history` y después `--all --apply --history`. Es un upsert; repetirlo no duplica. En dev, `--all` tardó más de diez minutos y dejó 24 787 entradas de 9 685 tareas | PENDIENTE |
| 34.4 | Esperar al job de dimensiones (minuto 20) y comprobar: `SELECT count(*) FROM responsibility_events` > 0 y `count(*) FROM dim_responsibilities WHERE job_price IS NOT NULL` cerca del total; `dim_sync_log` sin error. En dev: 5 646 eventos, 5 623 con precio | PENDIENTE |
| 34.5 | Vigilancia: `logs --since 1h tasks inventory checkinbiz` sin «espejo pendiente del historial»; `GET /api/v1/tasks/calendar` sin parámetros → 400 (502 = nginx con IPs viejas) | PENDIENTE |
| 34.6 | Vuelta atrás: nada que deshacer. Las columnas y tablas nuevas son aditivas y ningún lector las usa todavía; el código viejo las ignora | — |

**Registro de dev, 2026-11-03 22:11 UTC → 04-nov:** `git pull` en el VPS (`cdac13d`), migración 050 con la
salida esperada (`UPDATE 621`), los cinco contenedores reconstruidos `healthy`, nginx reiniciado,
`backfill-tasks --all --apply --history` terminado sin fallos (24 787 entradas, 9 685 tareas), job de
dimensiones de las 08:20 UTC con 5 646 eventos de puesto, sin «espejo pendiente» en el log de `tasks`,
`/api/v1/tasks/calendar` → 400.

## 35. Contratos del cliente y su rentabilidad (cartera, Fase 5, TDR-004) — PENDIENTE (API en staging y panel commiteado el 2026-11-05)

El contrato cuelga **del cliente**, como un documento más, y un cliente puede tener varios a la
vez (Jose, 05-nov). Cada tarea dice de qué contrato es (`Task.contractId`): se pone solo si el
cliente tiene un único contrato vigente en la fecha de la tarea; con varios, lo elige el panel;
nunca se bloquea una tarea por no tener contrato. El coste de un contrato es la suma de sus
tareas, **en bruto**: fichajes de la tarea (`checklogs_raw.task_id`, migración 050) o, si no los
tiene, su reloj por el precio del puesto. Importe, coste y margen solo owner y admin. **Core, sin
puerta** («el add-on es la capa de app cliente»). La lectura del PDF va por `merlin`, con el borde
que tacha nombres, DNI, direcciones, teléfonos, correos e IBAN antes de llegar a OpenAI.

Diseño: [TDR-004](../ingenieria/cartera-de-clientes/tdr/TDR-004-rentabilidad-del-montaje.md),
06 §D17, §D18 y §D11 bis. En `develop` `7335a36` y `staging` `b06ecd4` (`[skip ci]`), rama
`feat/customers-rentabilidad` (`99f76e1`, `8a56ace`, `69a03ed`, `6e1f2e1`, `0316b1a`, `c4ba349`, `2e51214`, `df52293`, `a12c247`, `233bf33`, `b5815df`, `dabb2d3`, `0045fe5`, `f105998`). Los merges
`f6f6c67`/`7335a36` y `cd38de2`/`b06ecd4` llevan el mismo contenido (un reintento); no estorban.

**Depende de §33** (servicio `customers` en prod) **y de §34** (`checklogs_raw.task_id` y
`dim_responsibilities.job_price`, sin los que las horas y el coste salen vacíos). Va en el mismo
pase o después, nunca antes.

**Lo que cambia en `shared`:** `checkbiz/customers/entities/CustomerContract`, su repositorio,
`contractForecast`, `taskContract`, `Task.contractId` (opcional) y `downloadPrivateFile`. Si §33 ya
reconstruye todo el stack, esto entra en esa misma reconstrucción.

### 35.a — Servidor

| Paso | Qué | Resultado |
|---|---|---|
| 35.1 | Migración 051 (`051_contratos_montaje.sql`), a mano: `… psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 < migrations/051_contratos_montaje.sql`. Esperado: `CREATE TABLE` y `CREATE INDEX` ×4 (`customer_contracts`, `contract_events`, `contract_outcomes`, `contract_forecasts`). Todo `IF NOT EXISTS`. Antes de reconstruir `customers`: si no, el espejo falla a mejor esfuerzo y solo deja avisos en el log | PENDIENTE |
| 35.2 | Contenedores: `customers`, `tasks` y `merlin` (o todo el stack si va con §33). `restart nginx`. Sin variables nuevas: `customers` ya lee `DATABASE_URL` del `env_file` común y `merlin` ya tiene `OPENAI_API_KEY` | PENDIENTE |
| 35.3 | Firestore: **ningún índice compuesto**. `tasks where contractId ==` usa el de campo único que Firestore crea solo; `customerContracts where customerId == and status ==` se resuelve fusionando índices de igualdad | — |
| 35.4 | Comprobación sin token: `POST https://api.checkbiz360.com/api/v1/gpt/contratos/leer` → 401; `GET …/api/v1/customers/contracts/x?entityId=x` → 401. Con token de owner de una empresa de pruebas: cliente → contrato con importe y horas → tarea del cliente sin decir contrato → la tarea lleva `contractId` → `GET /:customerId/contracts` con la tarea contada | PENDIENTE |
| 35.5 | Vuelta atrás: los campos y tablas son aditivos; las tareas con `contractId` siguen funcionando con el código viejo, que lo ignora | — |

**Registro de dev, 2026-11-05:** `git pull` en el VPS (`a0056fb`), migración 051 con la salida
esperada, `customers`, `tasks` y `merlin` reconstruidos `healthy`, nginx reiniciado. Prueba contra
staging con la demo de Neteges: contrato con estimación → `initialEstimate` congelado; un vigente
→ la tarea lo toma sola; dos vigentes → sin contrato, `options` dice 2, el PATCH con id lo pone,
un id inexistente da 400 y `null` lo quita; la lista suma sin doble cuenta; borrar un contrato con
tareas da 409; cerrar y reabrir. Datos de prueba borrados de Firestore y de Postgres.

**Registro de dev, 2026-11-05 (2):** `merlin` reconstruido con el arreglo del recuento (`768b052`),
`POST /api/v1/gpt/contratos/leer` sin token → 401. Prueba de punta a punta **por el proxy del panel
en local** (`:3100`) contra staging: PDF de contrato inventado subido a un cliente de la demo →
«Leer el PDF» devuelve importe 8 400 € sin IVA, inicio y fin, 96 h (tres operarios × cuatro jornadas
× ocho horas) y complejidad 5, cada dato con su frase, sin avisos → contrato creado con lo leído
(201) y la extracción guardada como evidencia (evento `extracted`) → `options` vigente →
`contracts` con total. Limpieza: contrato, documento, fichero del bucket, cliente y filas de
Postgres. **Sin probar todavía:** un PDF real de cliente, uno escaneado (422) y una tarea con
fichajes reales.

**Registro de dev, 2026-11-05 (3) — RGPD:** Jose fijó que **todo documento que llega a un modelo
va anonimizado**. La sombra del contrato dejaba pasar nombres que no estaban en Firestore ni
llevaban «D.»/«Dña.» delante; ahora tacha todo tramo con mayúscula que no sea vocabulario seguro
de contrato (`0316b1a`, tests de la fuga). `merlin` reconstruido en el VPS con esa versión
(comprobado dentro del contenedor), nginx reiniciado, `contratos/leer`, `customers`, `tasks` y
`documents` sin token → 401. **Antes del pase a prod esto es condición:** sin `0316b1a`, la
lectura de contratos no sale.

**Velocidad de la lectura (05-nov, `c4ba349`).** El modelo con el razonamiento de serie tardaba
30–41 s en un contrato de 20.000 caracteres; ahora el lector de contratos —y solo él— va con
`reasoning.effort: "low"`: 17–18 s punta a punta por el endpoint, misma lectura (importe y horas).
`CONTRATOS_ESFUERZO` en el `.env` lo cambia sin código; en prod **no** hay que ponerla. En
staging `develop` `9875a38` y `staging` `19f5906` (solo ese fichero: el develop → staging habría
arrastrado `purgaEmpresas.ts` de otra sesión), `merlin` reconstruido y nginx reiniciado.
Antes del pase, probar con un contrato real largo que «low» lea igual.

**Rentabilidad desde Postgres (05-nov, `df52293`, migración 053).** Las tareas de cada contrato
se leían de Firestore en cada apertura de la ficha (una lectura por tarea, sin tope, por
contrato). Ahora `tasks_raw.contract_id` + `PostgresContractTasks`: 1000 tareas en 1 ms frente a
1165 lecturas y ~0,35 s. El recuento que impide borrar un contrato con tareas sigue en Firestore.
Los fichajes de las tareas van con dos uniones por índice (14 ms frente a 26 ms con 100.000
fichajes). **Orden en prod, que importa:**
1. Aplicar `053_contrato_en_tasks_raw.sql` en `encodebiz_analytics` (a mano, mirando el resultado).
2. Desplegar `tasks` (el espejo escribe `contract_id`; sin la 053 cada escritura del espejo
   fallaría y quedaría para el `remirror`) y `customers`.
3. `backfill-tasks --all --apply` dentro del contenedor `tasks` (sale con error si no cuadra).
En staging: 053 aplicada, desplegados, backfill de QA y Neteges Demo «cuadra», la rentabilidad
de los cuatro contratos idéntica antes y después, y una tarea de prueba espejada con su contrato
y marcada al borrarla.

**Tareas de un contrato cerrado (06-nov, `a12c247` y `233bf33`).** Editar una tarea cuyo contrato
se había cerrado devolvía `task/contract_closed` (el panel reenvía el contrato al guardar) y no
se podía tocar. Ahora el que ya tenía se conserva; asignar uno cerrado sigue rechazado. Duplicar
copiaba el contrato cerrado; ahora la copia sale sin contrato (no el único vigente: en staging un
montaje se colgaba del mantenimiento). Reproducido antes y comprobado después en staging, con el
contrato «Stand feria» de QA cerrado y reabierto.

**Borrar un contrato borra su PDF (06-nov, `b5815df`, solo `customers`).** Jose: «si o si». Se
van el fichero (y el original si se firmó), la ficha del documento con su historial y su entrada
de `searchIndex`, salvo que otro contrato del cliente cuelgue del mismo documento. El espacio lo
descuenta `storageUsageDeleted`. Comprobado en staging (QA Eventos): antes ficha, buscador y
fichero; después, ninguno.

**La ficha lee los contratos de Postgres (06-nov, `0045fe5` y `f105998`, migración 054).** Todo
lo calculado ya salía de Postgres; la lista de contratos del cliente y el selector de la tarea
aún leían Firestore. Ahora leen `customer_contracts` y vuelven a Firestore solo si Postgres no
responde. La 054 añade `notes`, `extraction` e `initial_amount_cents`. **Orden en prod:** aplicar
la 054 → desplegar `customers` → `backfill-contracts.js --all` (simula) → `--all --apply`. En
staging: 5 contratos, 0 faltaban, 0 sobraban; comparado campo a campo con Firestore, iguales
(solo cambia el orden de claves de `extraction`, que reordena JSONB). La ficha: ~0,4 s.

**Panel, mismo día (`feat/cartera-de-clientes`, sin commitear aún):** el total del cliente dice
«contratado» y no «cobrado»; las horas del contrato salen «planificadas / hechas / previstas»
(«10,7 / 0 / 136 h»; sin estimación, las dos primeras; en rojo si las hechas pasan de las
previstas). Las planificadas las da la API (`plannedMinutes`, solo `customers`): de la hora de
inicio al vencimiento de cada tarea, por persona asignada, desde `tasks_raw`; el bloque de documentos del cliente dentro de la tarea solo enseña lo visible para
trabajadores (los contratos se quedan en la ficha del cliente).

**El conflicto de «horario por tareas» con nombre y tarea (05-nov, `2e51214`).**
`task/incompatible_with_tasks_mode` añade `employeeName` y `withTask {title, date, start, end}`
(opcionales). El panel monta «X ya tiene «Y» de 09:55 a 12:25 ese día…»; sin esos campos, el
texto genérico. `tasks` desplegado en staging.

### 35.b — Panel (`encodebiz-front-saas`)

Tres commits más en `feat/cartera-de-clientes`, sin push, encima de los siete de §33.b: `1a094562`
(documentación administrativa), `c6647d05` (contratos) y `9d5556ab` (aviso de la IA), y otros tres del 05-nov por la tarde, `d75b57c3`, `c627fc28` y `fdbc5393`: «Subir PDF» dentro de «Nuevo contrato» (`ContractFormDialog.tsx`, `CustomerContractsSection.tsx`, cinco locales): el PDF se sube como contrato del cliente, solo gestores, y queda elegido para leerlo. `TaskFormDialog.tsx` deja de poner solo el cliente cuando la sucursal tiene uno (una tarea de administración no es de ningún cliente), `errorLocales.ts` + `task.service.ts` montan el aviso del conflicto de horario por tareas con nombre y tarea, y `ITask.ts` deja «Requerir evidencia al completar» desactivado por defecto (lo había pedido Jose; las tareas existentes conservan su valor). Van en el mismo push y merge que §33.7.
**Ojo al mergear:** la sesión de la hoja informativa toca `DocumentUploadModal.tsx` como hotfix a
`main` (un tipo sin fichero); `1a094562` toca el mismo fichero (visibilidad por defecto y aviso).

| Paso | Qué | Resultado |
|---|---|---|
| 35.6 | Documentación administrativa: el contrato y el presupuesto del cliente salen visibles solo para gestores, y marcar supervisores o trabajadores enseña un aviso en rojo (06 §D18). `1a094562` | PENDIENTE |
| 35.7 | Contratos: bloque «Contratos» en la ficha con tarjeta de rentabilidad, total y previsión; diálogo con «Leer el PDF» y la cita debajo de cada dato; «Contrato» en la tarea solo con más de un vigente; nombre del contrato en el detalle. `c6647d05` | PENDIENTE |
| 35.7b | Aviso de lo que llega a la IA (`AiPrivacyNotice`) en «Leer el PDF» del contrato y en la importación del cuadrante de una persona. `9d5556ab` | PENDIENTE |
| 35.8 | Variable nueva en Vercel (prod): `NEXT_BACKEND_URI_CONTRATOS_LEER=https://api.checkbiz360.com/api/v1/gpt/contratos/leer`. Sin ella «Leer el PDF» da error de configuración del proxy; el resto de contratos funciona (va por `NEXT_BACKEND_URI_CHECKINBIZ_CUSTOMERS_HANDLER`, de §33.8) | PENDIENTE |
| 35.9 | Comprobar en prod con una empresa de pruebas: subir un contrato a un cliente → Contratos → Nuevo contrato → elegir el PDF → «Leer el PDF» → revisar citas → guardar → crear una tarea del cliente: sin selector con un contrato; con dos vigentes, el selector sale | PENDIENTE |

**App:** nada.


## 36. Cerrar desde administración pide inicio y cierre; informe de tareas desde Postgres — EJECUTADO el 2026-11-05 (orden de Jose: «si ya lo has probado todo y funciona bien bájalo a prod»)

**Por qué.** Un cliente cerraba tareas desde administración y «no salían en el informe»: pasaban
de Asignada a Completada sin `startedAt` y el Excel dejaba en blanco Inicio, Tiempo y Pausas
(reproducido en staging). Y el informe leía Firestore con `limit(1000)` por vencimiento: en la
demo de Neteges de staging, noviembre tiene 1.143 tareas y el lector viejo devolvía 1.000, sin
aviso. El «verde que no actualiza» de la app (supervisor asignado, «Todas las personas») es solo
su parte cerrada: el aviso «Tu parte está hecha» está en la app desde el 28-oct y **no está en la
1.10.0+68** de las tiendas.

**Qué cambia.**
- `tasks`: cerrar entera una tarea sin inicio sin ser parte de ella exige `startedAt` y
  `completedAt` (400 `task/times_required` / `task/invalid_times`). La tarea guarda
  `completionSource` (`administration` | `assignee`) y la actividad `manualTimes`. El espejo
  gana `evidence_count` y `completion_source`; subir o quitar un recurso reespeja la tarea.
- `reports`: el informe de tareas sale de `tasks_raw` + `task_ratings_raw` + dimensiones, sin
  tope; columna nueva «Completada por» con «(desde administración)». El material del add-on sigue
  en Firestore, por lotes.
- Panel: diálogo «Completar tarea» con Inicio y Cierre (botón y «Editar»); «Completada por … ·
  desde administración» en la ficha y las horas en el historial.
- App: mensaje propio para `task/times_required` (solo llega con la pantalla desfasada).

Ramas `fix/tareas-cierre-desde-gestion` en API (staging `5ce14f9`), panel (`develop` `37d1d86a`)
y app (`develop` `3579ca1`). QA: TSK-20-01..13, INF-02-20; TSK-11-47 cambió a esperar el 400.
Panel probado en local contra staging con Playwright (los dos caminos).

**🔴 Orden.** Panel **antes o a la vez** que la API: con la API nueva y el panel viejo, completar
una tarea sin iniciar desde el panel da error. El panel nuevo contra la API vieja no rompe nada
(manda dos campos que se ignoran).

| Paso | Qué | Hora (UTC) | Resultado |
|---|---|---|---|
| 36.0 | Solo el arreglo, no `staging` | — | `staging`/`develop` llevan §33-§35 sin aprobar: ramas `hotfix/tareas-cierre-desde-gestion` desde `main` con cherry-pick por `merge-tree`. API: `c48f91b`, `f4a8569`, `48b7bce`; único conflicto el `import` de `TaskPgMirror.ts` (sin `TaskActivity`/`upsertTaskEventRaw` del histórico). Panel: `0ef79376`. `tsc` limpio en `tasks`/`reports`, `reports` 5/5; los 29 errores de `tsc` del panel son los mismos que en `main` (imágenes) |
| 36.1 | Panel a `main` y Vercel | 15:51 | PR front#149, merge `26c0704c` **sin** `[skip ci]` (lo despliega Vercel). Vercel `Production` en verde antes de tocar la API |
| 36.2 | Migración 052 en `encodebiz_analytics` | 15:51 | `ALTER TABLE` ×2, `ON_ERROR_STOP`; antes no existían las columnas |
| 36.3 | API a `main` y despliegue | 15:53 | PR checkbiz-api#255, merge `b4696aa` con `[skip ci]` (no arrancó CI). `git pull --ff-only` + `up -d --build --no-deps tasks reports` (con `--env-file .env.production`) + `restart nginx`; los dos `healthy`, `PostgresTaskReportClient.js` en `dist` |
| 36.4 | Backfill | ~15:56 | Simulado: 5 empresas, 168 tareas, 0 filas a marcar borradas. Con `--apply`: «cuadra» en las cinco; las 168 con `evidence_count` |
| 36.5 | Comprobación | ~15:58 | Lector nuevo ejecutado en solo lectura dentro de `reports` (oct-nov): nDON8… 66 filas, 27 cerradas, las 27 con inicio; OPnlEi… 15 filas, 8 cerradas, 7 con inicio (la que falta es de antes del arreglo: sin hora que recuperar). **PENDIENTE:** prueba real en el panel (completar una sin iniciar pide horas) y el informe del cliente que se quejó |
| 36.6 | App | — | PENDIENTE: el mensaje nuevo va con la próxima versión; la 1.11.x ya trae «Tu parte está hecha» |

## 33. Purga de empresas: de 16 a 5 — EJECUTADO el 2026-11-05 (orden de Jose: «cancela suscripción y bórralas también»)

Se quedan Ayudarte, Neteges, Tapissat (`W6aVQj7L…`), Arendel y Encodebiz. Se borraron las otras 11.

**Incidente:** el borrado se ejecutó a las **12:19–12:23 UTC** con la primera versión del script (sin copia previa, con `--resto`), desde una orden que Jose interrumpió en el cliente: el `docker exec` siguió corriendo en el contenedor. Claude lo dio por no ejecutado sin comprobarlo en el servidor y lo descubrió a las 16:20. Borró exactamente las 11 ordenadas (15.306 docs, 7.429 filas, 69 ficheros, 44 cuentas). Sin copia previa; Firestore tiene PITR de 7 días y Storage soft delete de 7 días por si hiciera falta recuperar algo hasta el 12-nov.

| Paso | Qué | Resultado |
|---|---|---|
| 33.1 | Stripe | Bitfera `sub_1TdYuv…` cancelada en el acto (0 €). ACB2 LLC ya estaba cancelada en Stripe desde sep. Clientes de Stripe y facturas, intactos |
| 33.2 | Regla de ciclo de vida | `system/respaldos/r30/` se borra a los 30 días, en `encodebiz-services` y `dev-encodebiz` (las 6 reglas del quiosco, intactas) |
| 33.3 | Código | PR checkbiz-api#256 (`47af5c0`, `[skip ci]`), solo `backoffice` reconstruido. Probado antes en staging en cuatro pasadas |
| 33.4 | Residuo limpiado | ACB2 LLC: 191 filas de Postgres reescritas por la sync de analytics durante el borrado; 23 tokens de avisos de las 44 cuentas; 10 docs de `ai-analizer`. Copia de todo en `gs://encodebiz-services.firebasestorage.app/system/respaldos/r30/purga-empresas/2026-11-05/`, con el informe del borrado |
| 33.5 | Comprobación | 5 empresas, intactas (personas, sucursales, roles, pertenencias, buscador). De las 11: 0 en Firestore, Storage, Auth y Postgres, salvo `backoffice_audit` (se conserva a propósito) |
| 33.6 | PENDIENTE | Conectar la purga a la pantalla de Mantenimiento del backoffice (`application/maintenance/purgaEmpresas.ts`). `ai-analizer` ya cubierto en develop (`85cbf68`), no en prod |
| 33.7 | Panel de dirección | Foto provisional del 05-nov (`backfill`, la sustituye el cierre de las 04:20). Histórico: recalculados solo `clientes`, `clientes_de_baja`, `altas` y `clientes_activos` de 379 de 430 fotos con las empresas que existen (orden de Jose: «sí, corrige»); el resto de cada foto, intacto. Valores de antes en `…/purga-empresas/2026-11-05/direccion-contadores-antes.json` |
| 33.8 | Panel de dirección, suscripciones | Recalculados `pagando`, `en_prueba`, `gratis`, cuota y pruebas que vencen de 379 fotos con las empresas que existen (antes 8 pagando el 04-nov, ahora 4). Comparado antes de escribir: solo cambiaba la parte de las borradas (−4 pagando, −3 gratis, ~−54 €). Valores de antes en `…/2026-11-05/direccion-cuotas-antes.json` |
| 33.9 | Panel de dirección, plantilla | `plantilla_activa` recalculada en 369 fotos con las empresas que existen (130 → 100 el 04-nov; ninguna sube). Cuadra con la cuota: 100 × 2 € = 200 €. Valores de antes en `…/2026-11-05/direccion-plantilla-antes.json`. Fichajes, empleados que fichan y tareas del histórico siguen con las borradas |

## 37. IVA: todos más IVA, viejos y nuevos — PENDIENTE (en staging el 2026-11-03 y 05)

Diseño: [07_iva-altas-nuevas.md](../ingenieria/billing-v2/07_iva-altas-nuevas.md).

> **DECISIÓN VIGENTE (Jose, 05-nov, noche): «es mejor ponerle el IVA a todos, viejos y
> nuevos»; «todos por el billing nuevo»; se hace en el pase de esta versión, no antes.** Sustituye
> a las anteriores (03-nov «solo a los nuevos»; 05-nov tarde «add-ons siempre, el base de los de
> antes sin IVA»). Mientras no se pase, en prod queda lo hecho el 05-nov: el IVA **incluido y
> desglosado** en las suscripciones de antes (ver abajo). Con el pase, todos pagan «2 € + IVA».

**Lo que esto añade al pase** (además de 37.1–37.7):
- `BILLING_VAT_SINCE` con una fecha antigua (p. ej. `2020-01-01T00:00:00Z`): toda alta, de quien
  sea, es «nueva» y va más IVA; desaparece el hueco del cliente que vuelve.
- **Migrar las suscripciones que ya existen** al precio «más IVA» con el tipo sumado. Stripe NO
  deja poner el tipo sumado sobre un precio «IVA incluido» (probado en el Stripe de pruebas el
  05-nov: *«One or more prices has a `tax_behavior` that conflicts with the tax rates…»*), y la
  marca de un precio no se cambia: hay que cambiarles el **precio** a `stripePriceVat`. Script en
  `billing` con la misma lógica que el alta (`vatPrice` + `vatTreatment`), simula por defecto,
  `--apply`, sin prorrateo; probarlo antes en staging. Afecta a Ayudarte (82 → 99,22 €), Neteges
  (56 → 67,76), Tapissat (8 → 9,68), Encodebiz (14 → 16,94) y Arendel checkbiz (56 → 67,76); el
  Departamento de Arendel ya va sumado.
- **Aviso a cada cliente antes de su próxima factura** (Jose lo envía o da el OK al texto). Antes,
  mirar cómo figura el precio en la web y en las condiciones aceptadas («2 € + IVA» o «2 €»).
- Opcional: quitar del código la distinción nuevo/de antes, que deja de tener sentido.

Código (`billing` y `shared`): `433e5fd` (IVA 21 % con tipo fijo de Stripe), `4dab648` (precio
«más IVA» `stripePriceVat`), `9bdbe55` (add-ons siempre). En staging `e7fb011`, `billing`
reconstruido el 05-nov; QA de facturación en verde el 03-nov (sin repetir tras `9bdbe55`).

Lo comprobado en staging (Stripe de pruebas, 05-nov): tipo `IVA 21%` con `inclusive: false`;
Bronze `stripePrice` «inclusive» y `stripePriceVat` «exclusive», los dos 2 €; inventario y
quiosco `tax_behavior: unspecified` (admiten el tipo sin segundo precio). La regla, con los
cinco casos (base de antes sin IVA; add-ons de antes, base nuevo y add-on nuevo con IVA; sin
`BILLING_VAT_TAX_RATE` nada). **Punta a punta (05-nov, 20:41 UTC):** Neteges Demo, cliente de
Stripe del 30-oct (de antes del corte `2026-11-03`), contrató inventario → suscripción con el
21 %, sin `[billing][ALERTA]`; en prueba, factura a 0 € no enviada.

**Los clientes que ya están: IVA desglosado, EJECUTADO en prod el 05-nov** (Jose: «no se le suma
pero se le desglosa», «solo para los que ya están», configuración de Stripe y no código). Antes,
solo Arendel desglosaba, con el cálculo automático de Stripe que había puesto Jose a mano y que
costaba ~26 €/mes (≈1,1 % de lo facturado con él). Simulado en el Stripe de pruebas (82 € →
67,77 + 14,23; 1.950 € → +409,50) y en prod sin escribir; después, con un script desde el
contenedor `billing` de prod:
- Suscripciones checkinbiz de Ayudarte, Neteges, Tapissat, Encodebiz y Arendel: tipo **21 %
  incluido**, mismo total (Ayudarte 82 € = 67,77 + 14,23; Neteges 56 = 46,28 + 9,72; Tapissat
  8 = 6,61 + 1,39; Encodebiz 14 = 11,57 + 2,43; Arendel igual que antes).
- Departamento Tecnológico Adjunto de Arendel (1.950 € «más IVA»): tipo **21 % sumado**, mismo
  2.359,50 €.
- Las dos de Arendel, cálculo automático **apagado** (fuera la comisión).
- Ayudarte, Neteges y Tapissat no tenían en Stripe ni CIF ni dirección: se pusieron los de su
  ficha legal (misma lógica que `completeCustomerForVat`). El CIF de Encodebiz (`ES60466706M`)
  Stripe no lo acepta como `es_cif`: va como campo «CIF/NIF» de la factura.
- Sin prorrateo: ninguna factura emitida cambia; se nota desde la próxima de cada uno (Encodebiz
  17-nov, Neteges 21-nov, Tapissat 22-nov, Arendel DTA 26-nov, Ayudarte 30-nov, Arendel 03-dic).
  Comprobado con la vista previa de Stripe y leyendo el estado final.

**Hueco que queda con el código del §37:** un cliente de antes que se dé de baja del plan base y
vuelva sale **sin** IVA (el código solo sabe «sin IVA» para el base de los de antes). Hasta
cambiarlo, ponerle a mano el tipo incluido. Si se quiere en código: el base de un cliente de antes
con `txr_…iXjfPX36`.

| # | Paso | Cómo |
|---|---|---|
| 37.1 | Tipo de IVA en el Stripe real | **HECHO el 05-nov.** No había ninguno (las facturas a mano de Arendel iban con el cálculo automático, no con un tipo). Creados `txr_1UYXo6JdldmbRy89Ng7DZlRX` (21 %, se suma: el de `BILLING_VAT_TAX_RATE`) y `txr_1UYXo6JdldmbRy89iXjfPX36` (21 % incluido) |
| 37.2 | Precio «más IVA» de Bronze en el Stripe real | **No existe** (leído el 05-nov: el producto solo tiene 2 € `inclusive` ×2, 2,50 € y 3 € `unspecified`). Crear 2 €/mes `tax_behavior: exclusive` y apuntarlo en `service/checkinbiz/plan/bronze.stripePriceVat` de `encodebiz-services` |
| 37.3 | Precios de los add-ons en el Stripe real | Leído el 05-nov. **Inventario `price_1UPJ9q…` es `inclusive`** («29 EUR/mes hasta 50 empleados + 0,75 EUR por empleado a partir del 51 (IVA incluido)»): sin su par, el alta de inventario saldría **sin IVA** con `[billing][ALERTA]`. Crear el mismo escalonado `exclusive` y apuntarlo en `service/inventory/plan/standard.stripePriceVat`. Quiosco `price_1UT200…` es `unspecified`: sirve tal cual. (En staging inventario es `unspecified`, por eso allí funcionó.) |
| 37.4 | `.env.production` | `BILLING_VAT_TAX_RATE=<txr_ de 37.1>` y `BILLING_VAT_SINCE=<fecha y hora del pase, ISO>`: los clientes de Stripe creados desde ahí son «nuevos» |
| 37.5 | Desplegar `billing` | Por la cadena `staging → main`; `shared` va dentro de la imagen |
| 37.6 | Verificar | Un alta nueva de prueba con Bronze → la suscripción de Stripe lleva el tipo; el log no dice `[billing][ALERTA]`. Una empresa de antes que contrate un add-on → con IVA; su plan base, sin |
| 37.7 | Si algo falla | Quitar `BILLING_VAT_TAX_RATE` del `.env` y reiniciar `billing`: sin ella no se aplica IVA a nadie |

## 38. Hotfix: el documento personal de otra persona solo lo ven owner y admin, y desde la app nadie — EJECUTADO el 2026-11-06 (orden de Jose: «sí y urgente», «lo pruebas directamente en main»)

Cindy veía desde la app los documentos de empleado de Jose en Encodebiz. Dos causas: `canRead`
dejaba ver un documento personal ajeno a cualquier compañero de la misma sucursal con su rol en
`visibleToRoles` (el panel marca los tres por defecto), y la lista de la app pide sin
`employeeId`, con lo que a una owner (Cindy lo es) le devolvía todo, contratos incluidos. Regla
nueva (Jose): empresa y sucursal son públicos para quien pertenece; el de otro empleado solo
owner/admin, y desde la app nadie sea quien sea. El canal se saca del `User-Agent` (la app lo
sustituye por la huella del dispositivo; el panel es `Mozilla/…`); Jose lo acepta como hotfix y
pide un método comprobable en una fase 2 (TDR-002 de `documental-service`). Solo
`services/documents`; sin migración, variables, índices ni reglas.

| Paso | Qué | Hora (UTC) | Resultado |
|---|---|---|---|
| 38.1 | Rama `hotfix/documentos-empleado-solo-propios` desde `main`, en worktree sin `node_modules` (enlaces al árbol principal para `tsc`), borrado al terminar | ~11:30 | Commit `1cbdb33`, `tsc` limpio en `documents` |
| 38.2 | Foto de antes en prod | ~12:00 | Sonda dentro del contenedor `tasks` (custom token → ID token, `GET /api/v1/documents?entityId=…` con `User-Agent` de dispositivo y de navegador). Cindy (owner, supervisora): 8 personales ajenos en los dos canales. Jose Domingo (worker): 0 —los documentos de Encodebiz van sin sucursal, así que el camino del compañero no se daba aquí |
| 38.3 | `main` | ~12:05 | PR checkbiz-api#258, merge `953f6a0` con `[skip ci]`; no arrancó ningún CI |
| 38.4 | Despliegue | ~12:08 | `/opt/encodebiz-api`: `git pull --ff-only` + `up -d --build --no-deps documents` + `restart nginx`. `documents` `healthy` |
| 38.5 | Foto de después | ~12:10 | Cindy como app: 6 documentos, **0 ajenos**; como panel: los 14 de antes (owner). Jose Domingo y Jose Manuel: 0 ajenos en los dos canales. Sonda borrada del contenedor |
| 38.6 | `develop` | ~12:15 | Cherry-pick por `merge-tree` + `commit-tree`: `ea665eb` `[skip ci]`. **`staging` sin tocar**: lleva §33-§35 y §37 sin aprobar |
| 38.7 | Fase 2 | — | PENDIENTE: canal comprobable (dispositivo de confianza del 2FA + cabecera de cliente), opciones y recomendación en TDR-002. Y decidir si `canCreate`/`canArchive` de documentos de empleado pasan también a owner/admin: hoy un manager puede subir uno que ya no puede leer |
| 38.8 | Panel | — | PENDIENTE (no urgente): el formulario de la ficha del empleado marca `worker/supervisor/manager` por defecto en `visibleToRoles`; ya no abre nada, pero engaña |
| 38.9 | **Incidente**: la gestión documental del panel salía vacía a owner/admin (reportado por un cliente, ~13:36–14:00 UTC) | ~14:00 | El panel no llama desde el navegador: su servidor en Vercel hace el fetch con Node y llega con `User-Agent: node`, que 38.3 tomaba por app. Respuestas de 121 bytes en nginx. PR checkbiz-api#259 (`6602d82`, `[skip ci]`): `node`, `undici` y `Next.js` son panel. Desplegado igual que 38.4; sonda con tres `User-Agent` (dispositivo, `node`, navegador): Cindy 6/14/14, Jose Domingo 4/4/4 sin ajenos. `develop` `7bb0a6e` |
| 38.10 | Fase 2 | 10-nov | DECIDIDA con Jose: el panel demuestra que es el panel con un código rotatorio estilo 2FA (`HMAC-SHA256(PANEL_CHANNEL_SECRET, floor(unix/30))` en `X-CheckBiz-Panel`, desde `serverBackendProxy.ts`); válido → panel, todo lo demás → app, y el `User-Agent` desaparece. Tres pasos A/B/C sin ventana vacía. Diseño en TDR-002 «Fase 2»; tarea en CheckBiz360 para Jose Manuel el martes 10-nov 09:00-13:00 (`zGRy0s1AStJ3bWhr1Hyo`) |

## 39. Alertas: jornada de más de 9 h, sin descanso semanal y hoja informativa sin firmar — PENDIENTE en prod; EN STAGING el 2026-11-07 (056 aplicada en encodebiz_staging, analytics y assistant reconstruidos; panel en develop)

Jose, 06-nov: «12 personas con jornada configurada de más de 9 h, esto es crucial igual que los
empleados sin informe firmado […] debe saltar alarma». Tres reglas nuevas en el panel de alertas
y en el resumen de la mañana: `long_day` y `no_weekly_rest` (naranja, del `weekPlan` del último
fichaje) y `notice_unsigned` (rojo, del espejo de la hoja). Diseño en alertas-por-correo §1.

- API: rama `feat/alertas-jornada-y-hoja` (`2a3a62f` + `38c66d9`, que la renumera de 054 a 056; develop `1db8bd7`, staging `1607e35`), servicios `analytics` y `assistant`;
  `shared` va dentro de las imágenes. **Migración 056** (tres columnas en `dim_employees`).
- Panel: rama `feat/alertas-jornada-y-hoja` (`4d2cbab5`, ya en develop por avance rápido), solo textos en 5 idiomas y el tipo.
- Sin variables ni índices. Plantillas de correo sin cambios: las cajas las pinta el código.

| # | Paso | Cómo |
|---|---|---|
| 39.1 | Migración 056 en dev, luego en prod | A mano por SSH, **antes** de desplegar `analytics`: sin las columnas el sync de empleados falla en su INSERT y `/panel/alerts` entero da error (si una fuente falla, falla todo, a propósito) |
| 39.2 | Desplegar `analytics` y `assistant` | Por la cadena, con `[skip ci]` y a mano el servicio que cambia; `restart nginx` después |
| 39.3 | Primera pasada del espejo | Esperar al job de dimensiones (:20) o lanzarlo por la ruta de sync; comprobar `SELECT COUNT(*) FILTER (WHERE notice_signed_at IS NOT NULL) FROM dim_employees` |
| 39.4 | Verificar | `GET /api/analytics/panel/alerts` de una empresa con hojas sin firmar y otra con jornadas de 13 h: salen las cajas; el número de `long_day` puede no coincidir con el de la pestaña Análisis (esa recorre el mes entero con el calendario; esta, el último fichaje) |
| 39.5 | Panel | Vercel, después de la API: sin textos, la caja sale con la clave cruda |
| 39.6 | Aviso | El primer día saltará «hoja sin firmar» en casi todas las empresas: la plantilla de antes del 04-nov no la tiene. Es lo esperado; la salida es enviarla desde el modal de documentos |
| 39.7 | Si algo falla | Apagar por empresa con `rules_off`, o revertir `analytics`: las columnas de 056 no molestan a nadie |

**Staging, 2026-11-07:** 39.1–39.4 hechos en dev. Primera pasada del espejo: 263 empresas, 9355
fichas activas, 146 hojas enviadas y 6 firmadas. Neteges Demo: 29 sin firmar (29 sin enviar);
empresa QA `h9D8X3tt…`: `notice_unsigned` 80, `no_weekly_rest` 34, `long_day` 27. Falta ver las
cajas en el panel de develop en local. En prod no se ha tocado nada.

## 40. Salud de la plataforma: servicio `salud`, alertas a support@ e informe diario — EJECUTADO el 2026-11-06 (orden de Jose: «bájalo a prod»)

Jose, 06-nov: «¿se puede hacer automatizado y mostrarlo en backoffice?», «es un servicio nuevo,
un docker nuevo», «no puede estar ligado a nada del sistema», «alertas en caso de críticos de
estabilidad al email de support@encodebiz.com», «cada 5 min: disco, memoria, CPU, ancho de
banda». Diseño en `DOCS/ingenieria/salud-plataforma/README.md`.

- API: rama `feat/salud-plataforma`. Servicio **nuevo** `salud` (carpeta `salud/`, fuera de los
  workspaces, sin `shared`), **migración 055**, ruta y pantalla del backoffice (permiso
  `salud:read`, root y admin) y **`nginx/nginx.conf` con el formato de log `combinado_tiempos`**.
- No va en el CI de nadie: `salud` se construye con su carpeta como contexto.
- **En dev desde el 2026-11-06 15:24 UTC**: muestras cada 5 min, 14 días reconstruidos (23-oct a
  05-nov) con todas las partes `ok`, pantalla probada con token root (las tres rutas 200) y un
  correo de prueba aceptado por SES hacia support@. Cuenta `salud-lector@dev-encodebiz` creada
  el mismo día con solo `roles/monitoring.viewer` (clave `b14e0395…`).

| # | Paso | Cómo |
|---|---|---|
| 40.1 | Migración 055 | A mano: `docker compose --env-file .env.production exec -T postgres psql -v ON_ERROR_STOP=1 -U encodebiz -d encodebiz_analytics -f - < migrations/055_salud_plataforma.sql`. Crea las tres tablas y el rol `salud` **sin acceso** |
| 40.2 | Contraseña del rol | `P=$(openssl rand -hex 24)`; añadir `SALUD_DB_PASSWORD=$P` a `.env.production`; `ALTER ROLE salud LOGIN PASSWORD '$P';` en `encodebiz_analytics` |
| 40.3 | Cuenta de Google propia (la decide Jose: es un cambio de IAM en prod) | `gcloud iam service-accounts create salud-lector --project encodebiz-services`; `gcloud projects add-iam-policy-binding encodebiz-services --member=serviceAccount:salud-lector@encodebiz-services.iam.gserviceaccount.com --role=roles/monitoring.viewer --condition=None`; `gcloud iam service-accounts keys create salud-sa.json --iam-account=salud-lector@encodebiz-services.iam.gserviceaccount.com`. **No** se le da el rol a `firebase-adminsdk-fbsvc-clean` |
| 40.4 | Clave al servidor | `scp` a `/opt/encodebiz-api/secrets/salud-sa.json`, luego `sudo chown root:root` y `chmod 600`: el contenedor es root **sin capacidades** y no lee un 600 de `almalinux` (pasó en dev). Borrar la copia local |
| 40.5 | Correo | Usa `SMTP_HOST/PORT/SECURE/USER/PASS/FROM` del `.env.production` por interpolación del compose, sin cargar el fichero entero. Comprobar que están; si se quiere un remitente propio, un usuario SMTP de SES aparte |
| 40.6 | Desplegar | Con el resto del pase, o suelto: `git pull --ff-only origin main` y `docker compose --env-file .env.production up -d --build --no-deps salud backoffice`; después **`restart nginx`** (recoge el formato de log y las IPs nuevas). Probar antes la config: `docker run --rm -v $PWD/nginx/nginx.conf:/etc/nginx/nginx.conf:ro -v $PWD/certbot/conf:/etc/letsencrypt:ro --add-host=… nginx:1.27-alpine nginx -t` |
| 40.7 | Verificar | `ps` con `salud (healthy)`; `SELECT tomada_en, datos->'cpu', datos->'discoPct' FROM salud_muestras ORDER BY id DESC LIMIT 2`; en el log, «correo configurado» y el informe de ayer «cerrado» al minuto de arrancar |
| 40.8 | Rellenar hacia atrás | `docker compose exec -T salud node dist/cli.js informe --desde <hace 14 días> --hasta <ayer>`: los días salen «reconstruido», sin recursos (no había muestras). Los logs de nginx de prod llegan hasta finales de octubre |
| 40.9 | Lo que va a decir el primer día | Ámbar «SSH admite contraseña» todos los días hasta que se cierre (prod sigue con `PasswordAuthentication yes` del `50-cloud-init.conf`). Es verdad y es lo que tiene que decir |
| 40.10 | Si algo falla | `docker compose stop salud`: nadie depende de él. Las tablas de 055 no molestan a nadie |

**Registro del 2026-11-06 (Claude, con la orden de Jose).** Rama mínima `hotfix/salud-plataforma`
desde `main` con solo los commits de salud (no arrastra nada de staging): PR #260, #261 (el
correo: producción solo define `SMTP_USER`/`SMTP_PASS` y el resto sale de los valores por
defecto de `shared`; el compose los copia) y #262 (certificado reintentado, red con dos
decimales, «entrada pública» en vez de «borde»). Los tres con `[skip ci]`: ningún workflow.

- 40.1 HECHO 15:45 UTC — 055 aplicada en `encodebiz_analytics`, sin errores.
- 40.2 HECHO 15:46 — `SALUD_DB_PASSWORD` añadida al final de `.env.production` (comprobado que
  el resto del fichero no cambió) y `ALTER ROLE salud LOGIN`.
- 40.3 HECHO 15:48 — `salud-lector@encodebiz-services`, solo `roles/monitoring.viewer`, clave
  `b8dc6980…`. La cuenta de Firebase no se tocó.
- 40.4 HECHO 15:49 — clave en `secrets/salud-sa.json`, `root:root 600`; copia local borrada.
- 40.5 HECHO — el compose resuelve host `email-smtp.eu-north-1.amazonaws.com`, puerto 465,
  remitente `EncodeBiz <encodebiz@encodebiz.com>`. En dev salió un correo de prueba a support@.
- 40.6 HECHO 15:51 y 16:00 — `nginx -t` con los certificados reales en verde; `up -d --build
  --no-deps salud backoffice` y `restart nginx`. 20 contenedores sanos, `/health` y
  `/backoffice/` 200, el log de nginx ya trae `rt=` y `urt=`.
- 40.7 HECHO 16:04 — muestras cada 5 min; la de las 16:04 con certificado (44 días), entrada
  pública en 206 ms, CPU 2 %. La primera tras cada despliegue sale «no responde» porque
  coincide con el reinicio de nginx: una sola muestra no abre alerta (hacen falta dos). 0 alertas.
- 40.8 HECHO 15:53 — 14 días reconstruidos (23-oct a 05-nov), todas las partes `ok`. El 05-nov
  dice en ámbar el 5xx de `employeeplanifierworker`, el timeout que ya se vio a mano.
- 40.9 Pendiente de que ocurra: el informe de cada día a las 03:30 de Madrid; el ámbar de
  «SSH admite contraseña» saldrá cada día hasta que se cierre.
- 40.9 VISTO 07-nov 02:39 UTC — el primer informe automático (06-nov) salió y mandó correo a
  support@ con un **rojo falso**: «la entrada no respondió en 2 muestras». Eran las de los dos
  reinicios de nginx de los despliegues, nunca seguidas, y la alerta en vivo no se abrió. Y
  «faltan 87 de 288»: el servicio arrancó a las 16:51. Corregido en #263 (`[skip ci]`, solo
  `salud`): rojo con dos muestras seguidas, como la alerta; el día de arranque se cuenta desde la
  primera muestra. Informe del 06 rehecho: queda el ámbar de SSH y tres info. Desplegado en dev
  y prod el 07-nov.
- 40.11 HECHO 07-nov (PR #264, `[skip ci]`, `salud` + `backoffice` + `restart nginx`, dev y prod):
  «Cuándo se usa más el servidor» en Sistema → Salud. Sale de las muestras de la máquina (CPU,
  carga, red, disco) por hora de Madrid, no del tráfico de clientes (Jose: «no la de mis
  clientes»). Hoy dice «sin hora punta»: CPU plana al 0,4 %. La entrada pública por horas pasa
  a líneas, con clientes y escáneres separados; 14 días rehechos para traer `porHoraClientes`.

## 41. Postgres de producción: `shared_buffers` a 4 GB — EJECUTADO el 2026-11-07 (orden de Jose: «sube postgres a 4 GB»)

PR #265 (`[skip ci]`): `command: ["postgres", "-c", "shared_buffers=4GB"]` en `docker-compose.yml`
(solo producción; dev sigue con su tope de 1 GB). De fábrica eran 128 MB en 32 GB.

- 07:31 UTC — antes: 25 peticiones en 10 min, ninguna consulta larga, `SHOW shared_buffers` 128MB.
- 07:36 — `up -d --no-deps postgres`: sano en 11 s, `SHOW shared_buffers` 4GB, sin errores.
- **Efecto no previsto: analytics se cayó y Docker lo levantó** (07:36:34, `RestartCount` 1). El
  pool de `shared` (`packages/shared/src/db.ts`) no tiene `pool.on("error")`: cuando Postgres
  corta una conexión ociosa (57P01), node-postgres emite un error sin capturar y el proceso muere.
  Solo analytics tenía conexiones abiertas en ese instante; **los 11 servicios que usan ese pool
  están expuestos a lo mismo en cualquier reinicio de Postgres**. Salud lo vio y avisó a support@
  (07:37:59, «analytics se ha reiniciado solo»). PENDIENTE de decisión de Jose: añadir el manejador
  (una línea en `shared`, pero reconstruye todos los servicios).
- Datos intactos: mismas filas que antes del reinicio en las 7 tablas grandes, 63 MB.
- **Copia hecha** a las 07:39 UTC: `/var/lib/encodebiz-api/backups/encodebiz_analytics-20261107-0739Z.dump`
  (`pg_dump -Fc`, 3,8 MB, root 600, 70 tablas con datos verificadas con `pg_restore --list`). Está
  en el MISMO servidor: protege de un error, no de perder la máquina. Sigue sin haber copias
  automáticas ni fuera del servidor.

## 42. Copias de seguridad: servidor cifrado y ficheros de Storage, en Europa — EJECUTADO el 2026-11-07 (orden de Jose: «créalo tú y haz toda la configuración»)

Diseño y cómo restaurar: `DOCS/ingenieria/salud-plataforma/copias.md`. PR #266 (copia del
servidor dentro de `salud`, por indicación de Jose) y #267 (Sistema → Copias), `[skip ci]`.

- HECHO 07:51 UTC — buckets `encodebiz-services-copias` (EU, retención 30 días, borrado a los 90,
  acceso público bloqueado) y `encodebiz-services-copias-ficheros` (EU, versiones, versiones viejas
  a los 90 días).
- RETIRADO 08:00 — exportación diaria de Firestore (tarea de Scheduler, cuenta `copias-firestore`
  y permisos): duplicaba la PITR de 7 días y la copia semanal nativa. No llegó a correr.
- HECHO 08:00 — cuenta `copias-servidor` (solo `objectCreator` en el bucket de copias), clave en
  `secrets/copias-sa.json` (root 600), certificado `secrets/copias-publica.pem`. Clave privada SOLO
  en el portátil de Jose (`encodebiz-api/secrets/copias-clave-privada.pem`): **PENDIENTE que Jose
  la guarde en su gestor de contraseñas.**
- HECHO 08:00 — migración 057 (rol `copias`, solo lectura) y `COPIAS_DB_PASSWORD` en
  `.env.production`.
- HECHO 08:03 — primera copia: `servidor/2026/11/07/prod-20261107T080334Z.tar.cms`, 3,9 MB, 70
  tablas. Restauración probada (descifrado, sumas, `PGDMP`); `gcloud storage rm` rechazado por la
  retención.
- HECHO 08:2x — Storage Transfer Service: API activada, agente con lectura en el origen y escritura
  en el destino, trabajo `copias-ficheros-diaria` a la 01:00 UTC desde el 08-nov. **No se forzó la
  primera ejecución (Jose: «déjalo para que salte mañana»). PENDIENTE comprobarla el 08-nov.**
- HECHO 09:00 — Sistema → Copias en el backoffice; 37 días de informes rehechos con el tamaño de
  cada bucket. Ficheros de clientes: 113 MB el 01-oct, 204 MB el 06-nov.
- Visto, sin tocar: `gcf-v2-sources-…-us-central1` ocupa 8,9 GB de código de funciones antiguas.

## 43. Documentos «Administración»: solo propietario o administrador, desde el panel — PENDIENTE en prod; EN STAGING el 2026-11-07 (develop `0d64a35d`, staging `5d88bfa8`; `documents` y `customers` reconstruidos)

Jose, 07-nov: un documento que **solo se vea desde el panel** y solo por propietario o
administrador (contrato o presupuesto de un cliente, papeles de dirección). Valor nuevo `admin`
en `visibleToRoles`, que el panel lee «Administración». Regla y decisiones en TDR-002 §Nivel
«Administración»; el principio: la app es de la plantilla, y quien entra por ella, aunque sea
owner, es un empleado más.

- API: rama `feat/documentos-administracion` (`d37d4f9` y `b319668`, desde develop `245ba67`),
  servicios `documents` y `customers`. Sin migraciones, variables ni índices. `shared` no cambia.
  `b319668` extiende el principio a todo documento: **por la app**, propietario, administrador y
  owner operativo leen solo lo que lleve `worker` (supervisor y manager conservan su rol), y el
  listado no enseña archivados. Esto cambia lo que hoy ve un owner en la app de producción: deja
  de ver los documentos marcados solo para managers o supervisores.
- Panel: `3085d580`, ya dentro de `feat/cartera-de-clientes` (fast-forward el 07-nov): va con la
  cartera, que todavía no está en prod.
- Comprobado en staging (Neteges Demo, cuenta de Jose, owner): la hoja del cliente de la tarea
  «QA Visita SAD» por la app lista solo «QA Ficha de la usuaria»; el listado de documentos de QA
  Usuaria SAD da ficha y contrato con User-Agent de navegador y solo la ficha con el de la app.
  **Jose lo probó en staging el 07-nov: «probado lo de Administración».**
- Script opcional `services/customers/src/scripts/contracts-to-administration.ts`: pasa contratos y
  presupuestos de cliente que están en `["manager"]` exacto a `["admin"]`. Simula por defecto.

| # | Paso | Cómo |
|---|---|---|
| 43.1 | `documents` y `customers` a la vez | Por la cadena con `[skip ci]` y a mano los dos servicios; `restart nginx` después. Antes que el panel: un panel nuevo contra una API vieja recibe 400 `invalid_visibility_roles` al subir un contrato. El panel viejo no manda `admin`, así que la API nueva sola no cambia nada visible, salvo que `for-task` (la hoja del cliente en la app) deja de listarle a gestores lo que no es de `worker` |
| 43.2 | Comprobar la descarga del panel (también es la **lentitud** que vio Jose el 07-nov). **Variable CAMBIADA en Vercel prod el 2026-11-07** (orden de Jose: «cambia esto urgente») a `https://api.checkbiz360.com/api/v1`; `DOWNLOAD_REPORTS` ya existía en prod, así que los informes no caen a ella. Antes se comprobó que `api.checkbiz360.com/api/v1/documents/:id/download` responde 401 sin token. **Redesplegado** el mismo día (`vercel redeploy` del vivo `mpylezpke`, sin cambio de código; nuevo `aebn0n45w`, alias saas.encodebiz.com, orden de Jose: «redespliega tú»). Comprobado: el proxy de descarga responde 401 sin token. Falta que Jose abra un documento real y confirme que va rápido | `NEXT_BACKEND_URI_CHECKINBIZ_DOWNLOAD_DOCUMENTS` en Vercel (es sensible, no se lee): tiene que ir al contenedor (`…/api/v1`) y no a la función `documentsHandler` del SaaS, que no conoce ni el canal ni `admin` y dejaría descargar un solo-`admin` de empresa al owner operativo que tenga el id. Se ve en el log de nginx de prod: una descarga desde el panel tiene que entrar por `/api/v1/documents/:id/download` |
| 43.3 | Panel | Vercel, después de la API (va con la cartera) |
| 43.4 | Verificar | Owner desde el panel sube un contrato de cliente: nace «Administración», lo abre. El gerente de una sucursal del cliente no lo ve en el panel, y un PATCH directo suyo da 403. Desde la app nadie lo ve, owner incluido (hoja del cliente de la tarea incluida). Un documento de sucursal solo-`admin` no manda push. Con acuse de recibo, 400 `admin_only_acknowledgement` |
| 43.5 | Script, solo si Jose lo pide | En el contenedor `customers`: `node services/customers/dist/scripts/contracts-to-administration.js --all`, revisar la lista y repetir con `--apply` |
| 43.6 | Si algo falla | Revertir `documents` y `customers`. Lo ya marcado `admin` con la API vieja: owner/admin lo ven (también desde la app), el owner operativo también, el gerente no; editarlo da 400 hasta volver a la nueva |

**La descarga lenta en prod (Jose, 07-nov, «tarda una eternidad»).** Sin medir: no se ha tocado
prod. Lo que dice el código: `.env.production` del panel apunta
`NEXT_BACKEND_URI_CHECKINBIZ_DOWNLOAD_DOCUMENTS` a la función `documentsHandler` en `us-central1`
(1 GiB, sin instancias mínimas), que ya no tiene rutas propias y reenvía al contenedor de OVH. Si
Vercel tiene lo mismo, cada descarga cruza el Atlántico dos veces y, en frío, arranca la función.
En desarrollo la variable va directa a `api-staging…/api/v1`. El arreglo es el de 43.2:
reapuntarla en Vercel a `https://api.checkbiz360.com/api/v1`, con OK de Jose. **Sin token:** la
URL que devuelve la API es una URL firmada de Storage que caduca al minuto
(`SIGNED_URL_TTL_MINUTES = 1`); conseguirla sí exige token y permiso, abrirla no.


## 44. Ficha de cliente con análisis de Merlin en el backoffice — EJECUTADO el 2026-11-07 (orden de Jose: «bájalo hasta prod… baja solo tu rama directa a producción, después súbela a develop»)

Página por cliente en el backoffice (`/backoffice/clientes/:id`, enlazada desde Clientes y
Dirección) y botón «Analizar con Merlin»: dossier de agregados sin personas → `gpt-5.5` con
razonamiento alto, en un hilo de OpenAI por cliente. Diseño en
`ingenieria/ficha-de-cliente/README.md`. Solo esta rama: **nada de `staging`**, que lleva trabajo
de otras sesiones sin aprobar. Toca `backoffice`, `merlin` y `billing` (ruta interna nueva) y
añade la migración 058; nginx no cambia.

| Paso | Qué | Hora (UTC) | Resultado |
|---|---|---|---|
| 44.1 | Esquema de prod, solo lectura | ~09:35 | Faltan `tasks_raw.contract_id` (053) y `dim_employees.notice_*` (056). La 053 ya tenía alternativa; para la 056 se añadió (`b396e46`). Las 21 consultas de la ficha, en `BEGIN READ ONLY` contra `encodebiz_analytics`: 20/21, la que falla es la de `contract_id` y su alternativa pasa |
| 44.2 | Rama `feat/backoffice-ficha-cliente-prod` desde `main` con solo los commits de la ficha (`merge-tree` + `commit-tree`) | ~09:40 | Mismos 22 ficheros que la rama; `tsc` limpio en backoffice, billing, merlin y web sobre `main`; 13 tests |
| 44.3 | `main` | ~09:45 | PR checkbiz-api#268, merge `b5e67b5` con `[skip ci]`; no arrancó ningún CI |
| 44.4 | Migración 058 `backoffice_cliente_hilo` en `encodebiz_analytics` | ~09:52 | `CREATE TABLE`; tabla nueva, ninguna de clientes tocada |
| 44.5 | Despliegue | ~09:53 | `/opt/encodebiz-api` en `53df6c8` sin cambios locales → `git pull --ff-only` + `up -d --build --no-deps backoffice merlin billing` + `restart nginx`. Los tres `healthy`; borde 200. Entró con billing el `shared` de firma/hoja/tareas ya desplegado en los servicios que lo usan |
| 44.6 | Prueba real | ~10:00 | Ficha de Neteges en el contenedor: 2,8 s, señales coherentes (13 de 29 sin fichar nunca, 47 cierres del sistema, un solo gestor). Análisis real de **Encodebiz** (interna): `gpt-5.5`, 127 s, 7.046 entrada / 9.369 salida; hilo creado en OpenAI, apuntado en la 058 y releído. Scripts de prueba borrados del contenedor |
| 44.7 | Plantilla paginada y buscador (petición de Jose) y títulos de Merlin sin su explicación | ~10:30 | PR checkbiz-api#269, merge `abc4319` `[skip ci]`; `up -d --build --no-deps backoffice merlin` + `restart nginx`. Probado en prod: 29/31, filtros, «MARÍA» = «maria», `%_` escapado |
| 44.8 | Hoja informativa | — | **Sin Firestore** (Jose: «espera al espejado»): sale de `dim_employees.notice_*`; en prod «sin medir» hasta que baje la 056 (§39) |
| 44.9 | `develop` | ~10:40 | Merge `f37fe0b` `[skip ci]` por `commit-tree`. `staging` sin tocar |
| 44.10 | Dev | — | PENDIENTE cuando la ficha suba a `staging`: aplicar la 058 en `encodebiz_staging` (`psql -f - < migrations/058_backoffice_cliente_hilo.sql`) y reconstruir `backoffice merlin billing` |
| 44.11 | Pendiente de producto | — | Último acceso al panel de quien lleva la cuenta (no se recoge; sale «sin medir»). Queda en el hilo de Encodebiz el análisis de prueba de 44.6 |
| 44.12 | Webhooks internos fuera de los recuentos (pregunta de Jose: «¿a qué URL se han entregado?») | ~11:00 | Las 716 de Ayudarte iban a `wh_internal_inventory`, nuestro inventario suscrito a `task.*`; en prod las 1.017 entregas son internas, ninguna de cliente. Ficha, módulo Webhooks de Dirección y foto diaria las contaban como integración (el fallo de Dirección es anterior a la ficha). PR checkbiz-api#270, merge `7a8a965` `[skip ci]`; `up -d --build --no-deps backoffice` + `restart nginx`. `develop` `1092459`. Estadísticas sigue contándolas (salud de las entregas). Fotos diarias ya guardadas (`direccion_snapshot_daily.modulos.webhooks`) con el recuento viejo: **se dejan así** (Jose, 07-nov: «eventualmente se corrige sola»), las nuevas salen bien; el análisis de prueba de Encodebiz (44.6) recomendó Plan Empresarial por «301 webhooks», que eran internos |

## 48. El nombre del cliente a la plantilla, solo con autorización, y «Datos complementarios» en la app — PENDIENTE en prod; EN STAGING el 2026-11-07 (develop `fe3c62b0`, staging `a8fa6c74`; `customers` y `tasks` reconstruidos)

Jose, 07-nov, en la QA de la app: el nombre del cliente es un dato sensible —en una subcontrata,
nombre más teléfono del contacto es entregar el cliente— y tiene que ser una autorización expresa
del cliente, apagada por defecto; y los datos del cliente, una tarjeta más del detalle de la tarea,
no un botón. Diseño: [cartera-de-clientes/tdr/TDR-005](../ingenieria/cartera-de-clientes/tdr/TDR-005-datos-complementarios-y-nombre-del-cliente.md).

- API: rama `feat/datos-complementarios` (`ca2d144`, desde develop). Toca `shared` (`Customer`,
  `TaskCustomerSnapshot`, `taskCustomerSnapshot`), así que hay que reconstruir **`customers` y
  `tasks`** (y todo servicio que use la copia: ninguno más la lee hoy). Sin migraciones ni
  variables. Script `refresh-task-customer-copies` (simula por defecto).
- Panel: `38228381` en `feat/cartera-de-clientes`: casilla «Mostrar el nombre del cliente a la
  plantilla» con su ayuda, aviso en los contactos visibles, el detalle de la tarea lee el nombre del
  cliente. Va con la cartera.
- App: `checkbiz360` rama `feat/datos-complementarios` (`7c0f94a`, desde develop `71e0609`, sin
  push): tarjeta «Datos complementarios» encima de «Equipo», perezosa (`visibility_detector`),
  oculta si no hay datos o si falla; fuera el botón y la hoja. Próxima versión de tiendas.
- Comprobado en staging (Neteges Demo): tras el script, la copia de «QA Visita SAD» y `for-task`
  van sin nombre y con `nameVisible: false`; marcar la casilla en QA Eventos S.A. pone el nombre en
  sus dos tareas abiertas sin editarlas.

| # | Paso | Cómo |
|---|---|---|
| 48.1 | `customers` y `tasks` | Con la cartera (§33–§35) o después: por la cadena con `[skip ci]` y a mano los dos; `restart nginx` |
| 48.2 | Script | En prod la cartera aún no tiene tareas con cliente, así que no debería haber nada: `node services/customers/dist/scripts/refresh-task-customer-copies.js --all`, y `--apply` solo si lista algo |
| 48.3 | Panel | Con la cartera, después de la API |
| 48.4 | App | La versión que lleve `7c0f94a`. Una app vieja con la API nueva no pinta nombre si no viene: deja de verlo, que es lo seguro |
| 48.5 | Verificar | Cliente sin la casilla: la app no ve su nombre ni en la tarea ni en la tarjeta, y el documento de la tarea en Firestore no lleva `customer.name`. Marcarla: sus tareas abiertas lo enseñan sin editarlas. El panel sigue mostrando el nombre en el detalle de la tarea |
| 48.6 | Si algo falla | Revertir `customers` y `tasks`: las copias nuevas quedan sin nombre (la app vieja no lo pinta); el panel lo lee del cliente igual |

**Fuera de este trabajo:** el nombre del lugar (`siteName`) sigue en la copia y puede delatar al
cliente si se le llama como él; y `searchIndex` guarda los nombres de los clientes y hoy lo lee
cualquier sesión (reglas 2b).

## 45. El radio de la valla con la dirección del cliente — PENDIENTE en prod; EN STAGING el 2026-11-07 (develop `6947d0c9`, staging `cade6a96`; `tasks` reconstruido)

Jose, 07-nov, en la QA de la app (A8): la tarea con la dirección del cliente cogía la valla con
100 m y no había dónde cambiarlo. La dirección del cliente se captura sin radio y el panel, al
marcar «usar la dirección del cliente», escondía el campo de la valla entero.

- API: `b1c085a` (rama `fix/radio-direccion-cliente`), servicio `tasks`: alta y edición aceptan
  `workSiteRadiusMeters` junto a `useCustomerAddress`; ausente, se queda el de la dirección;
  negativo o no numérico, 400 `task/worksite_invalid`.
- Panel: `eba7909e` en `feat/cartera-de-clientes`: el radio sale debajo de la dirección del
  cliente. Va con la cartera.
- Comprobado en staging: «QA Visita SAD» con 250 m queda en Carrer del Mar 40 a 250 m; `-3` da 400.

| # | Paso | Cómo |
|---|---|---|
| 45.1 | `tasks` | Con la cartera (§33–§35); un panel viejo no manda el campo y todo sigue igual |
| 45.2 | Verificar | Tarea con cliente y su dirección: cambiar el radio en el panel, guardar, reabrir: conserva el radio |


## 46. Eliminar documentos y liberar el espacio — PENDIENTE en prod; EN STAGING el 2026-11-07 (develop `cbf96af9`, staging `58f6f881`; `documents`, `inventory` y `events` reconstruidos)

Jose, 07-nov: «cobramos por espacio pero no dejamos a los clientes liberar; hay que poder
eliminar documentos con sus avisos». Y: «se borra todo, y en los registros se queda el registro y
estado borrado; así, si nos reclaman, tenemos pruebas». Diseño en
`DOCS/ingenieria/documental-service/09_eliminar-documentos.md`.

- API: `bd3388a` + `48e1390` (límite de 50 por llamada), rama `feat/eliminar-documentos`. `documents`: `GET /:id/delete-preview`,
  `POST /:id/delete`, `POST /delete` (hasta 50 por llamada; el panel manda lotes de 50); solo owner/admin desde el panel. Borra del bucket
  el fichero, el original firmado, los PDF firmados, la evidencia de cada firma y su acta; el
  documento queda con `status: "deleted"`, acuses y actividad. Descargar un eliminado da 410.
  `inventory` y `shared` (cumplimiento de equipos) dejan de contar los eliminados; `events`, el
  tipo `document.deleted` en el catálogo. Sin migración, sin variables, sin índices.
- Panel: `e893995d` + `97f32164` (lotes de 50), rama `feat/eliminar-documentos`, ya en develop por avance rápido. Ficha:
  Eliminar junto a Archivar, con los avisos en rojo y casilla; lista: selección y eliminar varios;
  estado «Eliminado». Textos en 5 idiomas.
- Comprobado en staging (script dentro de `documents`, empresa QA `h9D8X3tt…`): un documento con
  fichero, PDF firmado, evidencia, acta y acuse → vista previa 4 ficheros / 3.700 B con el
  firmante; eliminado: los 4 fuera del bucket, el contador los descontó (sus registros de
  `storage_objects` desaparecieron), registro `deleted` con motivo y bytes, acuse conservado,
  actividad `deleted`; la segunda vez, `already_deleted`. Rutas vivas tras nginx (401 sin token).
  Falta probarlo desde el panel de develop en local.

| # | Paso | Cómo |
|---|---|---|
| 46.1 | `documents`, `inventory`, `events` | Por la cadena con `[skip ci]` y a mano solo esos tres; `restart nginx` |
| 46.2 | Panel | Vercel, después de la API: sin ella, la vista previa da 404 y el modal se cierra con error |
| 46.3 | Verificar | En una empresa de prueba de prod: subir un documento, eliminarlo, ver que la ficha enseña el registro sin descarga y que el almacenamiento usado de la empresa baja |
| 46.4 | Saber contestar | Las copias de ficheros (§42) guardan lo copiado antes de eliminarlo hasta 90 días, como versión vieja; el bucket, 7 días de borrado blando. «Se borra todo» es del producto, no de las copias |
| 46.5 | Si algo falla | Revertir `documents`: los ya eliminados se quedan como registro (`status: "deleted"`); la versión anterior no los da a la plantilla (solo ve activos), pero a Administración se le verían en la lista con la descarga rota |

## 49. El cliente en los análisis: parte, pestaña «Análisis», resumen de Inicio y alertas — PENDIENTE en prod; EN STAGING el 2026-11-07 (develop `424f8129`, staging `19153fde`; 059 aplicada en `encodebiz_staging`; `tasks customers reports analytics` reconstruidos)

Jose, 07-nov: «es uno de los pluses que más van a convertir». Diseño:
[cartera-de-clientes/tdr/TDR-006](../ingenieria/cartera-de-clientes/tdr/TDR-006-parte-del-cliente.md).

- API: `1d7eac5` (rama `feat/cliente-en-analisis`) + `fix/analisis-cliente-param` (un `$4` sin
  tipo en la consulta de personas: 503 `source_unavailable`). Toca `shared` (`customerReader`,
  textos de `alertEmail`), así que reconstruir **`tasks customers reports analytics`**. `reports`
  gana `sharp` (misma versión que `entities`, imagen `node:22-alpine`).
- Migración **`059_cliente_en_analisis.sql`**: `tasks_raw.customer_id`/`customer_site_id`, índice,
  `dim_customers`. **Antes** de desplegar `tasks` y `customers`.
- Backfills, por entidad o `--all`, primero sin `--apply`: `backfill-customers` (contenedor
  `customers`) y `backfill-tasks` (contenedor `tasks`).
- Panel: `da45c4e8`, ya dentro de `feat/cartera-de-clientes` (merge `dfa3d7de` del 07-nov, sobre
  `5c21bafa` de la sesión del panel: filtros de documentos y tarjeta del cliente en la tarea). Va con la
  cartera. Sin push.
- Variables nuevas del panel (Vercel prod y `.env.development`):
  `NEXT_BACKEND_URI_CHECKINBIZ_CUSTOMERS_ANALYTICS=<API>/api/analytics/customers` y
  `NEXT_BACKEND_URI_CHECKBIZ360_REPORTS_CUSTOMER=<API>/api/reports/customer`. Sin ellas, 403.
- Comprobado en staging (Neteges Demo, cuenta de Jose): espejo con el cliente en 6 tareas;
  `summary` lista QA Eventos, QA Comunidad y QA Usuaria; `overview` de QA Eventos responde
  (`enoughData: false`: tareas solo de noviembre); parte de QA Eventos de noviembre en PDF (201,
  1,9 s) y Excel (201, 0,8 s).

- **Cliente en el informe de tareas** (Jose, 07-nov): `5a35cf73` (rama `feat/informe-tareas-cliente`,
  develop `4d449f80`, staging `f6b9b836`), servicio `reports`. Columna «Cliente» detrás de «Centro»,
  de `dim_customers` (059), solo si alguna tarea del informe lleva cliente. Comprobado en staging:
  octubre de Neteges Demo, 838 filas con cliente, 19 columnas.
- **Inicio más claro** (Jose, 07-nov: «no sé qué son esos números»): `b296341e` (develop `c36723be`,
  staging `76d9fff5`), `analytics`, añade `period`, `customersWithTasks`, `totalMinutes`, `sharePct` y
  `missedCustomers` al resumen; panel `a928838e` en `feat/cartera-de-clientes`.

- **Análisis a fondo del cliente** (TDR-007, Jose 07-nov: «no estás mostrando si el cliente es
  rentable»): `8a4564e5` + arreglo `d3bc1050` (rama `feat/cliente-analisis-a-fondo` y
  `fix/insights-cifras`; develop `d384e9aa`, staging `8e5837ca`), servicio `analytics`:
  `GET /api/analytics/customers/:id/insights`. Sin migración: lee `tasks_raw`, `customer_contracts`,
  `dim_responsibilities.job_price`, `task_ratings_raw` e `item_movements_raw`. Panel `28996dce` en
  `feat/cartera-de-clientes` (el proxy deja pasar `/:id/insights` con la misma variable
  `…_CUSTOMERS_ANALYTICS`). Comprobado en staging: Bon Preu rentable (octubre 16 173 € frente a
  9 106 €, 44 %), señales «4 sin hacer» y «horas del contrato agotadas», 17 personas; Cardona 10 «sin
  importe». **Para que la rentabilidad salga, los puestos tienen que tener precio** (`job_price`):
  en prod, comprobar cuántas empresas lo tienen antes de anunciarlo.

| # | Paso | Cómo |
|---|---|---|
| 49.1 | 059 | A mano por SSH en `encodebiz_analytics`, mirando el resultado |
| 49.2 | `tasks customers reports analytics` | Por la cadena con `[skip ci]` y a mano; `restart nginx` |
| 49.3 | Backfills | `backfill-customers --all` y `backfill-tasks --all`, revisar, repetir con `--apply` |
| 49.4 | Panel | Con la cartera; las dos variables en Vercel **antes** del despliegue |
| 49.5 | Verificar | Ficha de un cliente: pestaña Análisis; «Parte del cliente» en PDF y Excel; Inicio con el bloque «Clientes» si hay tareas este mes; un gerente solo ve sus sucursales y no ve las alertas de contrato |
| 49.6 | Si algo falla | Revertir los cuatro servicios; la 059 solo añade columnas y una tabla, se queda |


## 47. Corregir una jornada incompleta de una vez — PENDIENTE en prod; API EN STAGING el 2026-11-07 (develop `a7a299b`, staging `cec6647`; `checkinbiz` reconstruido); panel en develop y en `feat/cartera-de-clientes`; app en develop

Jose, 07-nov: «levantaría un modal con las que hay en esa jornada y confirmaría cada una de las
jornadas incompletas y un solo motivo que se replique a todas […] lo mismo con la app: imagina una
jornada partida de 5 turnos, qué caos». Diseño en `DOCS/ingenieria/correccion-de-jornada/README.md`.

- API: `e3730ad` (rama `feat/correccion-jornada`). `checkinbiz`: `GET`/`POST
  /checklogs/update/workday` (gestora: owner/admin o responsable ≥ 2) y `POST
  /checklogs/update/workday/respond` (solo la propia persona). Lote en
  `entities/{id}/workdayCorrections`; cada fichaje con su entrada en `requestUpdates` + `groupId`.
  Un push por jornada y un aviso de bandeja por fichaje (la app publicada los acepta uno a uno; `/update`
  cierra el lote al caer el último). Al aceptar, las incidencias `incomplete_workday_*` de la jornada
  pasan a `resolved` sin escribir respuestas. `shared`: la clave `update_workday_pending` (es/en). Sin
  migración, sin variables, sin índices nuevos.
- Panel: `da0876f1` (rama `feat/correccion-jornada`, en develop `2bbe369c`; el 07-nov, por orden de Jose, también en
  `feat/cartera-de-clientes` como `d4a1608f` —cherry-pick, no merge: el merge arrastraba lo de eliminar
  documentos de develop—, así que sube a Vercel con la cartera si va antes). «Corregir jornada» en el
  detalle de la incidencia; estado de la corrección en la propia incidencia. El handler
  `checkinbiz_update_log` admite `GET` y la subruta `/workday`: **sin variable nueva en Vercel**.
  Textos en 5 idiomas.
- App: `8d33535` + `75e9265` + `0c75a84` (rama `feat/correccion-jornada`, en develop `d8c1f74`). La bandeja junta los avisos
  del mismo `groupId` en una tarjeta; pantalla «Corrección de tu jornada» con una tarjeta por tramo (entrada,
  descansos y salida; lo corregido, tachado; la salida que puso el sistema, «sin fichar → hora») y Aceptar
  jornada o Rechazar con motivo. Cada bloque se llama «Turno n» (Jose: «no pongas tramo», también en el panel:
  `c1bb7479`, develop `eaa0f5e2`, cartera `8e429751`). Sale con la próxima versión; mientras, la publicada acepta fichaje a fichaje.
- Comprobado contra Firestore de `dev-encodebiz` llamando a los controladores (empresa QA ficticia,
  borrada después), 32 comprobaciones: jornada de 2 tramos y 6 fichajes, 403 sin permiso, 400 por
  fichaje de otro día y por hora futura, 409 por propuesta encima y por responder dos veces; rechazo →
  fichajes de vuelta a `incomplete_workday` e incidencia abierta con el motivo; aceptación → los 6
  `valid`, la salida a la hora corregida y las 2 incidencias cerradas; aceptar por `/update` (app
  vieja) cierra el lote y la incidencia. Rutas vivas tras nginx (401 sin token). Falta probarlo
  desde el panel de develop en local y con la app de develop.
- Para probarlo en staging hay una jornada partida incompleta sembrada (06-nov, 2 tramos, 2 incidencias)
  para «QA op_worker» en la empresa QA `zhSbHC7PnPkfd34QUke5`, marcada `qaSeed: "correccion-jornada"`;
  propietario `success+qa-20261106-17w1-prop@simulator.amazonses.com` con contraseña de prueba. Borrarla al acabar.
- Demo pedida por Jose (07-nov): en «Neteges Demo (ficticia)» (`318Ey5ZH…`), Jose Manuel Acevedo Medina, jornada
  del 06-nov con 4 tramos partidos (06:00, 10:00, 15:00 y 19:00), cada uno con su descanso y sin salida: 16 fichajes y
  4 incidencias, marcados `qaSeed: "demo-correccion-jornada"`. Solo en staging.

| # | Paso | Cómo |
|---|---|---|
| 47.1 | `checkinbiz` | Por la cadena con `[skip ci]` y a mano solo `checkinbiz` (lleva `shared`, que se compila dentro); `restart nginx` |
| 47.2 | Panel | Vercel, después de la API: sin ella el modal no carga la jornada (404). Si la cartera (§33.b) sube antes, este commit ya va dentro: la API de §47.1 tiene que estar en prod para entonces |
| 47.3 | App | Con la próxima versión publicada; no hace falta esperarla para 47.1 y 47.2 |
| 47.4 | Verificar | En una empresa de prueba de prod: una jornada sin salida → incidencia → «Corregir jornada» → llega un solo push → aceptar → fichajes válidos e incidencia resuelta |
| 47.5 | Si algo falla | Revertir `checkinbiz` y el panel. Un lote pendiente se puede seguir aceptando fichaje a fichaje con la app publicada; `workdayCorrections` se queda, no lo lee nadie más |

## 50. Cartera de clientes entera: el orden del pase — PENDIENTE en prod (resumen del 2026-11-07)

La cartera sube a prod de una vez, pero está repartida en §33, §34, §35, §43, §45, §48 y §49. Esto
es el orden conjunto, sin repetir lo que dice cada sección; el detalle y la verificación, en ella.
**Producción no se toca sin la orden de Jose**, y las migraciones van a mano, una a una, mirando la
salida.

| # | Paso | Dónde |
|---|---|---|
| 50.1 | Migraciones en `encodebiz_analytics`, por este orden: **050 → 051 → 053 → 054 → 059 → 060 → 061 → 062** | §34.1, §35.1, §35 (053 y 054), §49 |
| 50.2 | `docker-compose.yml` y `nginx.conf` de prod: bloque `customers` y sus `location` (la exacta `=` incluida) | §33.1, §33.2 |
| 50.3 | API a prod por la cadena (`develop → staging → main`), sin CI y a mano. Al tocar `shared`, el stack entero: como mínimo `customers tasks documents reports analytics merlin sync inventory checkinbiz`; `restart nginx` | §33.3, §34.2, §35.2, §43.1, §45.1, §48.1, §49.2 |
| 50.4 | Índices compuestos de Firestore en `encodebiz-services` con gcloud | §33.4 |
| 50.5 | Backfills, primero sin `--apply`: `backfill-tasks --all --apply --history` (rellena también contrato y cliente), `backfill-contracts --all`, `backfill-customers --all`, `refresh-task-customer-copies --all` (en prod no debería listar nada) | §34.3, §35, §49.3, §48.2 |
| 50.6 | Variables en Vercel prod **antes** del panel: `NEXT_BACKEND_URI_CHECKINBIZ_CUSTOMERS_HANDLER`, `NEXT_BACKEND_URI_CONTRATOS_LEER`, `NEXT_BACKEND_URI_CHECKINBIZ_CUSTOMERS_ANALYTICS`, `NEXT_BACKEND_URI_CHECKBIZ360_REPORTS_CUSTOMER`. `…_DOWNLOAD_DOCUMENTS` ya está hecha (§43.2) | §33.8, §35.8, §49.4 |
| 50.7 | Panel: `feat/cartera-de-clientes` (`dfa3d7de` el 07-nov, **sin push**; lleva también los filtros de documentos y la tarjeta del cliente en la tarea de la sesión del panel) → push, PR a `develop` y de ahí a `main` | §33.7 |
| 50.8 | App, después de la API: la versión que lleve «el cliente en la tarea» (`9c8b3ed`, en develop) y «Datos complementarios» (`7c0f94a`, rama `feat/datos-complementarios`, sin push) | §33.10–11, §48.4 |
| 50.9 | Verificar con una empresa de pruebas, sección por sección | §33.9, §35.4, §43.4, §45.2, §48.5, §49.5 |

**Va con la cartera:** el conector del asistente (`assistant`) no tenía frase para
`customer_tasks_missed`, `customer_hours_drop`, `contract_hours_over`, `contract_ending` ni
`expenses_pending`, y `ver_alertas` las daba como «Alerta sin texto: díselo a soporte.». Arreglado
el 2026-11-10 (develop `98fca80`, staging `d67c161`, `assistant` reconstruido en staging) con el
texto del panel; un test compara `rules.ts` con el mapa `ALERTA`. Sube con `assistant` en §50.3.

**No sube a prod:** los datos de demo de Neteges Demo en staging (117 clientes `DEMO-*`, octubre
recreado con `demo-cartera-oct`, fotos en `…/tasks/demo-cartera/`). Son para enseñar, solo en staging.

**Abierto, antes o después del pase, a decidir por Jose:** la alerta `customer_hours_drop` pide 10 h
en el mes anterior a la misma altura, y en una empresa de visitas semanales (Neteges) solo la
alcanza un cliente: se propuso cambiarla por «visitas que faltan frente a su ritmo de siempre».

## 51. Gastos externos del contrato (TDR-008, Fase 1) — PENDIENTE en prod; EN STAGING el 2026-11-07 (develop `2e4e4a70`, staging `1fa6a28d`; 060 aplicada en `encodebiz_staging`; `customers` y `analytics` reconstruidos)

Jose, 07-nov: «a los contratos le puedas meter un campo de gastos adicionales … para que sea aún más
preciso». Diseño: [cartera-de-clientes/tdr/TDR-008](../ingenieria/cartera-de-clientes/tdr/TDR-008-gastos-externos.md).

- API: `d4e4be4d` (rama `feat/gastos-externos`). Migración **`060_gastos_externos.sql`**
  (`customer_expenses`, dos índices). `customers`: `GET/POST /contracts/:id/expenses`,
  `PATCH/DELETE /contracts/expenses/:id`, solo propietario y administrador; el coste del contrato
  gana `expenses`. `analytics`: `insights` gana `expenseCents` por mes y lo resta del margen.
- Panel: `04a30078` en `feat/cartera-de-clientes` (tarjeta con 5 y «Cargar más»; Editar con lista
  dinámica, fila a fila; contratos cerrados con «Añadir gasto» propio). Va con la cartera.
- Comprobado en staging: 7 gastos en el contrato de Bon Preu (1 962 €): página de 5 + 2, el contrato
  los suma al coste, el margen de octubre del cliente baja del 44 % al 32 %.

| # | Paso | Cómo |
|---|---|---|
| 51.1 | 060 | A mano en `encodebiz_analytics`, después de la 059 (orden de §50.1: **050 → 051 → 053 → 054 → 059 → 060**) |
| 51.2 | `customers` y `analytics` | Con la cartera (§50.3) |
| 51.3 | Verificar | Un contrato: añadir, cambiar y borrar un gasto en Editar; la tarjeta enseña el total; el gerente no ve nada y `POST` le da 403 |

## 52. Gastos desde la tarea y su aprobación (TDR-008, Fases 2 y 3) — PENDIENTE en prod; EN STAGING el 2026-11-07 (develop `0c26002e`, staging `79af80e8`; 061 aplicada en `encodebiz_staging`; `customers analytics merlin` reconstruidos)

Jose, 07-nov: «las dos fases, es muy importante y tributa directamente al cliente»; D1 (reembolso) no,
D2 (la IA lee el ticket) sí. Diseño: TDR-008 §6 bis.

- API: `9035ed03` (rama `feat/gastos-desde-la-tarea`). Migración **`061_gastos_desde_la_tarea.sql`**
  (`resource_id`, `rejection_reason`, `reviewed_by`, `reviewed_at`, índice por tarea). `customers`:
  gastos de la tarea, aprobar/rechazar, pendientes de la empresa. `merlin`: `POST /api/v1/gpt/gastos/leer`
  por el borde de anonimización; **las fotos no se leen** (sin texto que anonimizar), solo PDF con texto:
  pendiente de decisión de Jose. `analytics`: alerta `expenses_pending`. `shared`: textos del correo.
- Panel: `c0a2e87e` dentro de `feat/cartera-de-clientes` (merge `95cbaede`), más el arreglo del proxy
  `9f42338d` (la Fase 1 daba 403 desde el panel). Variable nueva **`NEXT_BACKEND_URI_GASTOS_LEER`**
  (`.env.development` hecho; Vercel prod, con el resto de §50.6).
- App: `checkbiz360` `75e7bc2` (rama `feat/gastos-desde-la-tarea`, sobre `feat/datos-complementarios`,
  sin push). Próxima versión de tiendas.
- **nginx de prod no tiene `customers`** todavía: lo añade §33.2.
- Comprobado en staging (Neteges Demo): Mireia sube un ticket y apunta 3,50 € en «Martí Pujol 428» →
  `pending`, origen app, con su contrato; ella no puede aprobar (403); la alerta cuenta 1; Jose lo
  aprueba y Mireia lo ve aprobado. La lectura de una foto devuelve vacío sin error.

- **IVA del ticket y tickets sueltos** (§6 ter, Jose «como tú digas» y «ponla en el panel también»):
  API `fcc17b15` (develop `f1129806`, staging `966d1d6d`), migración **`062_gastos_iva.sql`** (`total_cents`,
  `vat_unknown`), `customers`: total obligatorio para la asignada, base al aprobar, `DELETE
  /tasks/:id/tickets/:resourceId`. Panel `7c1d1461` en `feat/cartera-de-clientes`. App `856e112` en
  `feat/gastos-desde-la-tarea`.
- **Fotos de tickets con OCR local** (opción A, Jose «vale»): `5cdfd5f3` (develop `45192972`, staging
  `05d0a1da`), `merlin`: `sharp` + **Tesseract 5.5 en el Dockerfile de merlin** (`apk add tesseract-ocr
  tesseract-ocr-data-spa tesseract-ocr-data-eng`, `OMP_THREAD_LIMIT=1`; la imagen crece unos 45 MB). La
  imagen no sale del servidor: al modelo solo llega el texto tachado. Comprobado en staging con el modelo
  real: parking (8,40 / base 6,94), taller con nombre, NIF y matrícula tachados (102,85 / 85,00),
  ferretería y térmico «IVA incluido» sin base inventada; de 8 a 14 s por ticket. HEIC no se lee (la
  app manda JPEG).

- **Justificante de gasto** (§6 quater): API `a338f4c` + `07cde46b` (develop `b9439870`, staging `49b98055`),
  `documents` (tipo `customer_expense`, no subible a mano: 400 `documents/type_not_uploadable`) y
  `customers` (al aprobar, copia el ticket al documental del cliente, solo Administración; borrar el
  gasto lo archiva). Script **`file-expense-receipts`** (simula por defecto) para los aprobados antes del
  cambio. Panel `55cfef6d` en `feat/cartera-de-clientes`. Comprobado en staging: el gasto de Mireia
  tiene su justificante «Parking comunidad · 3,50 € · 07/11/2026»; Jose lo ve en el panel, no por la
  app; Mireia, 403.
- **App en develop** el 07-nov (`bea1179`): «Datos complementarios» y gastos desde la tarea con el
  total del ticket; conflictos solo de traducciones, resueltos juntando las claves.

- **La lectura del ticket con IA, descartada en panel y app** (Jose, 07-nov: «solo provoca
  inseguridad»; «déjalo en la API»). Panel `b6134149` sin el botón ni el proxy: **ya no hace falta
  `NEXT_BACKEND_URI_GASTOS_LEER` en Vercel** (52.3 se cae). La ruta, el OCR y Tesseract siguen en
  `merlin` sin uso. App sin lectura en develop: merge `2d6b250` (rama `fix/gastos-sin-lectura-ia`,
  `fd41521`; la trabajadora apunta concepto y total, la base la pone quien aprueba). También en la rama de la cartera: «Añadir gasto» directo en el contrato con
  fichero (`86f4450b`) y su API (`2cc5d71`, ya en staging).

| # | Paso | Cómo |
|---|---|---|
| 52.1 | 061 y 062 | A mano, después de la 060 (§50.1 queda **… → 059 → 060 → 061 → 062**) |
| 52.2 | `customers analytics merlin documents` | Con la cartera (§50.3); `merlin` con Tesseract en la imagen. Después, `file-expense-receipts --all` y `--apply` |
| 52.3 | Vercel | ~~`NEXT_BACKEND_URI_GASTOS_LEER`~~: ya no hace falta (lectura descartada en el panel, 07-nov) |
| 52.4 | App | La versión que lleve `75e7bc2`, después de la API |
| 52.5 | Verificar | Trabajadora apunta un gasto con ticket → pendiente; alerta en Inicio; aprobar desde la tarea o el contrato; rechazar con motivo y verlo en la app |

## 53. Fichaje sospechoso según el turno planificado — PENDIENTE en prod; EN STAGING el 2026-11-08 (develop `1bd93a9`, staging `90e106b`; `checkinbiz` y `analytics` reconstruidos)

Dos fallos con más de una jornada al día («Por tareas», turno partido, semana tipo con salida al
mediodía), vistos el 08-nov con la demo Neteges y los fichajes reales del 30-oct. Los dos **hotfixes
ya están en prod** desde el 08-nov, a mano y sin CI: **#271** (`checkinbiz`: un ciclo con
`scheduleApplied.source === "tasks"` queda fuera de la regla 3-10 h) y **#272** (`analytics`: Inicio
mide la llegada con la PRIMERA jornada del día contra el primer turno; antes cogía la última y todo
el que tenía dos jornadas salía «llegó tarde»; también `ver_hoy` y el cierre diario).

Lo que queda para el pase es la **regla buena**, acordada con la sesión de cartera (`2d72cd8`,
`CreateChecklog.ts`, funciones `plannedMinutesOf` / `isSuspectDuration`): planificado = minutos del
turno de la ENTRADA (`scheduleApplied.start/end`; +24 h si cruza medianoche; `null` con `source:
"default"`); sospechoso si dura menos de la mitad o más de planificado + 2 h; sin horario, los 3 y
10 h de siempre. La excepción de «tareas» desaparece. No va como hotfix: cambia el significado de
«sospechoso» para todos los clientes. Solo afecta a fichajes nuevos. Aceptar una corrección de
jornada (§47) **no recalcula** `isSuspect`; queda fuera a propósito.

| # | Paso | Cómo |
|---|---|---|
| 53.1 | `checkinbiz` | Con el resto del pase; sin migración |
| 53.2 | Decidir con Jose | Script que desmarque las salidas ya guardadas como sospechosas (simula por defecto, `--apply`, primero dev); y si se recalculan los cierres diarios desde el 30-oct, que tienen el retraso inflado |
| 53.3 | Verificar | Ciclo de tarea de 2 h → no sospechoso; refuerzo de 2 h cumplido → no; jornada de 8 h cerrada a las 3 h → sí; persona con dos jornadas puntual → sin «llegó tarde» en Inicio |


## 54. Auditoría del análisis: previsión, fiabilidad, heurística contra el plan, overview por persona, señales y patrones en transacción — PENDIENTE en prod; EN STAGING el 2026-11-08 (develop `27238c4`, staging `d3f1f91`; `analytics merlin assistant` reconstruidos; `onChecklogWrite` desplegada en `dev-encodebiz`; panel `c6a9fc65` en `feat/cartera-de-clientes`)

Sale de auditar el análisis contra la siembra de SaludStart (staging). Lo que se cuenta (horas,
coste, tareas, alertas, material) ya era exacto; lo que fallaba era la interpretación:

- **Previsión de fin de mes del cliente** (`CustomerInsights.ts`, `insightRules.ts`): se restaba el
  coste del mes entero al ingreso solo hasta hoy, y 11 de los 18 clientes rentables salían con
  pérdidas. Ahora el ingreso es el del mes completo. Además, el 1/12 de un contrato sin fin se
  recorta hasta hoy en lo realizado. TDR-007.
- **Fiabilidad** (`utils/regularity.ts`, `BuildBranchBehaviour`, `BuildEvolution`,
  `BuildEmployeeReliability`, `BuildBranchEffect`): la regularidad pasa a ser la fracción de
  entradas a ±15 min del plan, sin techo relativo. `dispersionMinutes` es ahora la mediana del
  desvío. SaludStart, octubre: 43 % → 94,5 %. TDR-004.
- **Heurística y Merlin contra el plan** (`packages/shared/src/analysis/planTiming.ts`, `HeuristicCore`,
  `ProfileClassifier`, `heuristic.router.ts`, `merlin` `fetchPlanTiming.ts` y los prompt builders):
  - la variabilidad se mide contra lo planificado de cada ciclo, con P10-P90 robusto;
  - el número de tareas sale de `tasks_raw`;
  - con lectura contra el plan, `efficiencyIndex` es la cobertura del plan, y eso también mueve
    `promote_high_performer` y `role_reassignment_candidate`.

  SaludStart: «variabilidad horaria elevada» 25 → 0; maverick 26 → 0. Nuevo TDR-008 en
  `report-pipeline-v2`.
- **Overview por persona** (`BuildPanelOverview.buildEmployeeOverview` y el conector `assistant`):
  con `employeeId` devolvía la empresa entera. Ahora cada bloque es de la persona, o `unavailable`
  con su motivo. 404 si la persona no es de la entidad; 400 con sucursal y persona a la vez. TDR-004.
- **Señales del cliente:** las comparaciones con meses anteriores solo usan meses con trabajo.
  - Nueva señal `contract_hours_over`, con la fecha del cruce, en rojo y visible al gerente.
  - El último día del contrato cuenta entero, en la zona de la entidad.
  - SaludStart: de 36 señales a 9. TDR-007 §3.1.
- **Patrones en transacción** (`firebase_sdk/src/fichaje/writeController.ts`): sucursal, persona en
  la sucursal y persona global se leen, recalculan y escriben en `runTransaction`. Antes dos salidas
  a la vez se pisaban, y Badalona de SaludStart quedó en 9 dataPoints con 1344 ciclos.

| # | Paso | Cómo |
|---|---|---|
| 54.1 | `analytics`, `merlin`, `assistant` | Con el resto del pase; sin migración. `shared` cambia (`planTiming`), así que se reconstruyen los tres |
| 54.2 | `onChecklogWrite` | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo onChecklogWrite`, tras confirmar que en prod la función viene de `firebase_sdk` y no del SaaS, que tiene otra copia en `dataProcessing/writeController.ts` sin arreglar |
| 54.3 | Panel | `c6a9fc65`: el texto de `contract_hours_over` en los 5 idiomas, con la cartera (§50) |
| 54.4 | Decidir con Jose | Si se rehacen los patrones de sucursal de prod que hayan perdido puntos. Script de la siembra: `siembra-saludstart/auditoria/a6-rehacer-patron-sucursal.js`, que simula por defecto y hay que portar antes |
| 54.6 | Señales de tareas con las completadas (`e3669c8`, `5a78912`, staging `8eee17b`) | `onTaskPattern` cuenta cada tarea una vez al terminarse (completed, validated o rejected); una completada que se revisa después solo mueve validación y rechazo. Sin valoraciones no hay nota media (`ratingCount > 0`), en el clasificador de analytics y en el del trigger: sin esto, al llegar las señales a quien nadie valora, salía «at-risk». Desplegar `--solo onTaskPattern,onChecklogWrite` y reconstruir `analytics` |
| 54.7 | Decidir con Jose | La media móvil de las señales de tareas (α 0,15) solo mira las últimas ~12 tareas. En una sucursal con 50 al día da un 64 % a tiempo frente al 88 % real (Badalona de SaludStart). Es diseño, no un fallo del pase |
| 54.5 | Verificar | Un cliente rentable da un margen de fin de mes positivo. La fiabilidad de la empresa cuadra con sus semanas. Una persona «Por tareas» puntual no recibe `correct_high_variability`. `ver_mes` con `personaId` trae solo sus cifras |

## 55. Tarea con cliente: guardar, gastos sin contrato, el contrato recoge lo que cubre, el panel firma como administración y contratos por páginas — PENDIENTE en prod; EN STAGING el 2026-11-08 (develop → staging `ec68b92` y `2351871`; `tasks customers documents` reconstruidos; panel en `develop` `b90ada6d`, `e5e70675`)

Visto con Cuidama (staging). Lo que entra en el pase:

- **Guardar con cliente** (`task.helpers.ts` `sameWorkSite`, `updateTask.controller.ts`; panel `TaskFormDialog`):
  - Editar una tarea con una valla sin `placeId` (las del cuadrante o el asistente) daba 400 `task/worksite_invalid`.
  - Ahora, si es el mismo sitio, se queda con la valla que tenía.
  - El panel solo reenvía la valla si cambió.
- **Gastos sin contrato** (`customers`):
  - `GET /:customerId/expenses/without-contract`, para el bloque «Gastos sin contrato» de la ficha.
  - `PATCH /expenses/:id/contract`, para asignar, cambiar o quitar el contrato. Queda en `contract_events` como `expense_assigned` / `expense_unassigned`.
  - Un gasto nuevo toma el contrato de su tarea o, si la tarea no tiene, el único vigente ese día.
  - El proxy del panel tiene que dejar pasar las dos rutas: `b90ada6d`. Sin eso, el bloque sale vacío.
- **El contrato recoge lo que cubre** (`application/linkCustomerContracts.ts`):
  - Al crear un contrato, cambiar su vigencia o reabrirlo, entran las tareas con cliente y sin contrato, y sus gastos, que ahora cubre. Solo si es el único vigente en esa fecha.
  - Queda en `contract_events` como `tasks_linked`.
  - Script `link-task-contracts --entity <id> [--customer <id>] [--apply]`, que simula por defecto.
- **El panel firma como administración**:
  - `packages/shared/src/checkbiz/auth/clientChannel.ts` (`resolveClientChannel`, el que ya usaba documents) y `services/tasks/.../taskActor.ts`.
  - Con canal panel o asistente y asiento owner/admin, firma la cuenta: actorId = uid y actorRole = owner/admin. Desde la app, la ficha de empleado, como siempre.
  - En prod hoy toda acción del panel de un owner/admin con ficha queda firmada con su ficha, y con el rol de su responsabilidad en la sucursal.
  - Panel `031ccc18`: «Asignada a {nombres}» / «Asignación retirada» y «Por {cuenta} · Administración».
  - La app tiene el mismo fallo de pintado; el contrato se pasó a su sesión.
- **Contratos por páginas:** `GET /:customerId/contracts?limit&cursor` → `{items, nextCursor, count, totals}`, con totales solo en la primera página. Sin `limit`, igual que antes.
- **Céntimos:** el panel redondeaba a euros los importes del contrato y del análisis (`e5e70675`).

| # | Paso | Cómo |
|---|---|---|
| 55.1 | `tasks`, `customers`, `documents` | Con el resto del pase; sin migración (`contract_events.type` es texto). `shared` cambia (`clientChannel`) |
| 55.2 | Panel | `develop` del panel con las ramas de la cartera (§50) |
| 55.3 | Decidir con Jose | Medir en prod con `reattribute-panel-activity --all`, SOLO simulación, cuántas entradas firmó la ficha en lugar de la cuenta. En staging: 4013 movidas, 132 sin tocar. Aplicar solo con su OK |
| 55.4 | Verificar | Editar una tarea del cuadrante con cliente guarda. Un gasto de la app sin contrato sale en la ficha y se asigna. Cambiar las fechas de un contrato recoge las tareas del cliente. El historial de una acción del panel dice «Administración» |

## 60. «Nadie ha fichado» con todo el centro ya fuera — PENDIENTE en prod; EN STAGING el 2026-11-10 (develop `98fca80`, staging `d67c161`; `analytics` y `assistant` reconstruidos)

**Candidato a hotfix desde `main`. Jose aún no lo ha autorizado.** El fallo está en producción.

- **Lo observado.** La alerta `no_presence` («Nadie ha fichado y había N personas previstas»)
  solo miraba a quien seguía trabajando o en pausa. En cuanto la plantilla de un centro terminaba
  la jornada, saltaba. Caso real en staging el 10-nov: SaludStart (`318Ey5ZHBMeqm5fsQ0Md`),
  Oficina Barcelona (`FzXKjZW8odGbnw7AVjFX`), 20 entradas y 20 salidas con la alerta encendida.
- **El arreglo** (`services/analytics/src/application/operational/OperationalDay.ts`, `alertFor`).
  Solo salta si nadie ha tenido hoy jornada en el centro. Cuentan trabajando, en pausa,
  terminada, sin cerrar, pendiente de validar y quien fichó sin estar previsto. Lo cubre el test
  `services/analytics/test/operationalDayAlert.test.ts` y un caso de `verificar-dia-operativo.ts`.
- **Cambia en:** el panel (`/panel/today`, `/panel/alerts`), el resumen por correo
  (`no_presence` es de hoy, `digest.ts`) y el conector (`ver_alertas`, `ver_hoy`).

| # | Paso | Cómo |
|---|---|---|
| 60.1 | Orden de Jose | Hotfix desde `main` o con el próximo pase |
| 60.2 | Hotfix | Worktree desde `origin/main`, cherry-pick de `945af58` (solo `analytics`: `OperationalDay.ts`, el test y el script de verificación), PR a `main` con `[skip ci]`; después, `up -d --build --no-deps analytics` y `restart nginx`. Sin migración ni `shared` |
| 60.3 | Verificar en prod | Pasada la hora de salida, un centro con todas sus jornadas cerradas no sale en `/panel/alerts`. Un centro sin ningún fichaje pasada la hora de entrada sigue saliendo |
| 60.4 | Verificado en staging | HECHO el 2026-11-10, ~12:52 UTC. Oficina Barcelona da `alert: "none"`, con 11 terminadas, 1 en otro centro y nadie dentro. `/panel/alerts` de SaludStart ya no lleva `no_presence`, y `ver_alertas` del conector tampoco |

# Próximo pase a producción — API (documento vivo)

**Abierto:** 2026-10-16
**Estado:** Abierto. Todo lo de abajo está **PENDIENTE** mientras no lleve fecha y resultado.
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
| `feat/horario-por-tareas` | Horario por tareas, fase 1 | migración 037, dos índices, función `onTaskDay`, reglas | §1 |
| `feat/conector-asistente` | Conector de Claude y ChatGPT, fase 1 | servicio `assistant` nuevo, nginx, secretos, reglas | §2 |
| `feat/cuadrantes-plantilla` (×2) | Cuadrante por plantilla de sucursal y de persona | nginx (`client_max_body_size`), reglas | §3 |
| `feat/material-por-destino` | Material hacia tarea, persona o sucursal | migración 034 | §4 |
| `feat/calendario-tareas-resumen` | Calendario semanal de tareas resumido en Postgres (ADR-008) | migración 040, un índice | §8 |
| `fix/reglas-collection-group` | Consultas de grupo | **ya en prod desde el 14-oct**; falta que `main` tenga el fichero | §5 |
| CRM (`feat/sales-crm*`, `feat/crm-*`, `feat/backoffice-crm`) | CRM comercial | **sin inventariar**: cruzar con #147 | — |
| `feat/mi-material-aviso-e-historial`, `fix/avisos-*`, `fix/backfill-account-kind`, `fix/backoffice-sucursales-direccion` | Avisos, idioma, material, backoffice | **sin inventariar** | — |

> Lo marcado «sin inventariar» no significa que no necesite nada: significa que nadie lo ha
> mirado todavía para este documento.

---

## 1. Horario por tareas, fase 1 — PENDIENTE

Diseño: `DOCS/ingenieria/horario-por-tareas` (README y `tdr/TDR-001`, §13). En staging desde
el 2026-10-16, QA 462/462 con HPT-01..09. Nadie entra en el modo hasta que alguien lo active,
así que el pase no cambia nada a ningún cliente.

| # | Paso | Cómo | Estado |
|---|---|---|---|
| 1.1 | Índices en el fichero del SaaS, **antes** de cualquier despliegue desde allí | Añadir a `encodeBiz-SAAS/firestore.indexes.json`: `tasks` colección `assignedEmployeeIds` CONTAINS + `scheduledStartAt` ASC (ya existe en dev, falta en el fichero) y `calendar_days` grupo `entityId` ASC + `date` ASC. Si no, el próximo `firebase deploy` del SaaS los poda | PENDIENTE |
| 1.2 | Índices en prod | `gcloud firestore indexes composite list --project encodebiz-services` y crear solo los que falten con `gcloud firestore indexes composite create … --project encodebiz-services`. Esperar a `READY` antes del 1.5 | PENDIENTE |
| 1.3 | Migración 037 | A mano, por SSH, sola y leyendo la salida: `docker compose … exec -T postgres psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 < migrations/037_horario_por_tareas.sql`. Esperado: `ALTER TABLE`, `CREATE TABLE`, `CREATE INDEX`, `ALTER TABLE`, `ALTER TABLE` | PENDIENTE |
| 1.4 | Reglas de Firestore | Con el fichero de `main` ya fusionado (§5). `calendar_days` en `soloServidor`. Guardar antes el ruleset vivo, como el 14-oct | PENDIENTE |
| 1.5 | Función `onTaskDay` | `node services/firebase_sdk/scripts/desplegar.mjs --project encodebiz-services --solo onTaskDay`. Nunca el codebase entero | PENDIENTE |
| 1.6 | Comprobación | `firebase functions:list --project encodebiz-services \| grep onTaskDay`; `\d dim_calendar_days` en prod; `GET /calendar` de cualquier empleado devuelve `scheduleMode: "weekly"` | PENDIENTE |
| 1.7 | Panel: el selector del modo, solo en la ficha del empleado (16-oct) | `feat/horario-por-tareas` de `encodebiz-front-saas` → develop → main y promoción en Vercel. Sin variables nuevas. Antes, probarlo en local contra staging (TDR-002 §4) | PENDIENTE |

Orden: 1.1 antes que nada; 1.3 antes de que el job `dimensiones` corra con el código nuevo
(al minuto 20 de cada hora), o su `INSERT` con `schedule_mode` fallará y lo dejará en
`dim_sync_log`; 1.2 antes de 1.5.


### 1b. Horario por tareas, fase 2 — PENDIENTE

TDR-003. El fichaje mueve la tarea.

| # | Paso | Cómo | Estado |
|---|---|---|---|
| 1b.1 | `checkinbiz` llega a `tasks` | `TASKS_INTERNAL_URL` (por defecto `http://tasks:3006`, vale en prod) y `ENCODEBIZ_API_KEY` en el entorno de `checkinbiz` de prod: comprobar que la tiene | PENDIENTE |
| 1b.2 | `onTaskDay` con la salida temprana | Redesplegar la función: `desplegar.mjs --project encodebiz-services --solo onTaskDay` (va con 1.5 si es el mismo pase) | PENDIENTE |
| 1b.0 | Staging se desplegó a mano el 16-oct | Para producción no vale: va por `staging → main` y su workflow, como siempre. En staging, el siguiente push sin `[skip ci]` vuelve a dejarlo todo en manos del CI | NOTA |
| 1b.3 | App | Versión de la app con la fase 2 publicada en las tiendas **antes** de activar el modo a nadie en prod | PENDIENTE |

---

## 2. Conector de Claude y ChatGPT, fase 1 — PENDIENTE, por detallar

Diseño: `DOCS/ingenieria/conector-asistente` (TDR-001). En staging desde el 2026-10-15.

| # | Paso | Estado |
|---|---|---|
| 2.1 | `docker-compose.yml` de prod: el bloque `assistant` (puerto 3017) calcado del de staging, con `ASSISTANT_PUBLIC_URL=https://api.checkbiz360.com/api/v1/assistant` | PENDIENTE |
| 2.2 | `nginx/nginx.conf` de prod: hoy solo tiene el upstream; faltan las rutas `.well-known/oauth-authorization-server`, `.well-known/oauth-protected-resource` (con `^~`) y `/api/v1/assistant/` como en `nginx.staging.conf` | PENDIENTE |
| 2.3 | `.env.production`: `ASSISTANT_COOKIE_SECRET` y la config web de Firebase de prod (`ASSISTANT_FIREBASE_API_KEY`, `_AUTH_DOMAIN`, `_PROJECT_ID`, `_APP_ID`) | PENDIENTE |
| 2.4 | Reglas: `assistant_.*` en `soloServidor` (va en el mismo despliegue que 1.4) | PENDIENTE |
| 2.5 | Lo que diga el TDR del conector sobre su despliegue y pruebas: **leerlo y traer aquí lo que falte** | PENDIENTE |

---

## 3. Cuadrantes por plantilla — PENDIENTE, por detallar

| # | Paso | Estado |
|---|---|---|
| 3.1 | nginx de prod: `client_max_body_size 4m` en la ruta de cuadrantes (ya está en `nginx/nginx.conf` de staging; comprobar que llega con el merge) | PENDIENTE |
| 3.2 | Reglas: `cuadrante_proposals` y `cuadrante_lotes` en `soloServidor` (mismo despliegue que 1.4) | PENDIENTE |
| 3.3 | Lo que diga `cuadrantes/tdr/TDR-001` §11: **leerlo y traer aquí lo que falte** | PENDIENTE |

---

## 4. Material por destino — PENDIENTE

| # | Paso | Estado |
|---|---|---|
| 4.1 | Migración 034 (`034_inventario_cuentas_destino.sql`), a mano y antes que la 037. El registro del 14-oct dice que se dejó fuera a propósito; ver `inventario/tdr/TDR-008` | PENDIENTE |

---

## 5. Reglas de Firestore: un solo despliegue — PENDIENTE

`firestore.rules` no existe en `main` (desde el 09-oct). El arreglo de las consultas de grupo
ya corre en prod desde el 14-oct, desplegado desde rama. El pase tiene que dejar `main` con el
fichero que suma las cuatro cosas: consultas de grupo, cuadrantes, conector y `calendar_days`,
y desplegarlo **una vez**:

1. Guardar el ruleset vivo de prod (API de firebaserules, como el 14-oct).
2. `firebase deploy --only firestore:rules --project encodebiz-services` desde `main`.
3. Probar sin sesión: lectura de `calendar` y `employees` por consulta de grupo 200;
   `signing_keys`, `calendar_days`, `cuadrante_proposals` y `assistant_*` 403.

Estado: PENDIENTE.

---

## 6. Reglas de Firestore: lectura sólo con sesión — 🔴 ALERTA MÁXIMA, 17/18-oct

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

Estado: PENDIENTE.

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

## 8. Calendario semanal de tareas resumido en Postgres — PENDIENTE

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
| 8.1 | Comprobar el espejo: `docker compose -p encodebiz-api --env-file .env.production -f docker-compose.yml exec -T postgres psql -U encodebiz -d encodebiz_analytics -Atc "SELECT count(*) FROM tasks_raw WHERE deleted_at IS NULL"` y cruzar con Firestore. Si falta, backfill antes de seguir | PENDIENTE |
| 8.2 | Migración 040 (`040_tareas_calendario.sql`): índice parcial `idx_tasks_raw_entity_start` sobre `tasks_raw (entity_id, scheduled_start_at) WHERE deleted_at IS NULL`. A mano, por SSH, sola y leyendo la salida: `docker compose -p encodebiz-api --env-file .env.production -f docker-compose.yml exec -T postgres psql -U encodebiz -d encodebiz_analytics -v ON_ERROR_STOP=1 < migrations/040_tareas_calendario.sql`. Esperado: `CREATE INDEX`. Es `IF NOT EXISTS`: repetirla no hace daño. Bloquea escrituras en `tasks_raw` mientras se construye; en staging fue instantáneo. Verificar: `SELECT indexname FROM pg_indexes WHERE tablename='tasks_raw' AND indexname='idx_tasks_raw_entity_start'` | PENDIENTE |
| 8.3 | Código: entra con el despliegue normal (`staging → main`, action *CI/CD*), que reconstruye `tasks` y reinicia nginx. Sonda: `curl -s https://api.checkbiz360.com/api/v1/tasks/calendar` debe responder `400 {"code":"task/bad_request","error":"entityId is required"}`; lo mismo `/calendar/cell`. `404` = contenedor viejo; `502` = nginx con IPs viejas | PENDIENTE |
| 8.4 | Logs limpios: `docker compose … logs --tail=50 tasks` sin «Cannot set headers after they are sent» tras las sondas (era el fallo de doble respuesta, ya corregido en staging) | PENDIENTE |
| 8.5 | Front: pasar `develop → staging → main` del panel DESPUÉS de 8.3 (los merges `35167ec2` y anteriores del calendario). Sin variables nuevas en Vercel: `NEXT_BACKEND_URI_CHECKINBIZ_TASKS_HANDLER` ya apunta a `api.checkbiz360.com/api/v1/tasks` | PENDIENTE |
| 8.6 | Prueba con sesión real en producción: Gestión de tareas → pestaña «Calendario semanal» → la semana carga, los contadores de la leyenda cuadran con la tabla filtrada por estado, una tarjeta «N tareas» abre la lista y «Abrir ficha» lleva a la tarea. Probar también la fila «Fecha límite» y el filtro por empleado | PENDIENTE |
| 8.7 | Si falla 8.6 y no es evidente: deshacer sólo el front (revert del merge del calendario en `main` del panel). El back se queda | — |

---

## Registro del día del pase

Vacío hasta el día del pase.

| Paso | Hora (UTC) | Quién | Resultado y lo que se vio |
|---|---|---|---|

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

## Registro del día del pase

Vacío hasta el día del pase.

| Paso | Hora (UTC) | Quién | Resultado y lo que se vio |
|---|---|---|---|

# Próximo pase a producción — Panel (documento vivo)

**Abierto:** 2026-10-17
**Repositorio:** `encodebiz-front-saas` · **Cadena:** `develop → staging → main` · **Producción:** Vercel, proyecto `encodebiz-front-saas`, despliega `main`
**Va con:** [proximo-pase-back.md](./proximo-pase-back.md). Este documento es solo el panel; lo
del back aparece como **prerrequisito**, con su número de sección allí.
**Estado:** Abierto. Todo está **PENDIENTE** mientras no lleve fecha y resultado.

---

## 0. Resumen

- **Variables de Vercel: faltan dos, y nada más.** Revisado el 17-oct contra el código de
  `develop`, entrada a entrada de la tabla del proxy y cada `process.env`. Las dos son de la §2
  del back (conector y alta por plantilla). Si faltan, el panel no se rompe: la sección del
  conector dice «no disponible» y el diálogo de importar plantilla da un error. Ver §2.
- **El back va primero, siempre.** Casi todo lo nuevo del panel llama a rutas que hoy solo
  existen en `staging` de la API. Con el panel nuevo y la API vieja, esas pantallas dan error
  (ninguna tumba nada más). Ver §3.
- **Sin cambios de build.** Ni dependencias, ni `package.json`, ni `next.config.ts`.
- **Ramas sanas.** `main` está entero dentro de `staging` y de `develop`. `develop → staging`
  fusiona sin conflictos (`git merge-tree`, 17-oct).
- **Lo que no entra:** ~20 variables de producción siguen apuntando a Cloud Functions mientras
  staging ya usa la API nueva (asignar usuario, alta de empleado y sucursal, entidad, medios…).
  No es un olvido de Vercel: en producción no corren los contenedores `entities` ni `branches`.
  Ver §5.

---

## 1. Qué entra

76 commits de `develop` que `main` no tiene (39 sin contar merges), 84 ficheros, +5.396 / −636.
Último despliegue de producción: 14-oct, `576a94d3` (PR #102).

| Qué ve el cliente | Merges | Necesita en el back |
|---|---|---|
| Calendario semanal en Gestión de tareas, resumido en el servidor | `08583fed`, `a3460ab4`, `585023c8`, `77c683c3`, `35167ec2` | back §8 (`/tasks/calendar`, `/calendar/cell`, migración 040) |
| Horario semanal o por tareas, solo en el empleado | `3c6020bd`, `26bd3e07` | back §1 |
| Importar cuadrante por plantilla: sucursal y persona; primero en la ficha; semana solo en lunes | `d12ae371`, `a793e510`, `c2224d3e`, `d21f59d6` | back §3 (`/plantilla`, `/lotes` en `cuadrantes_handler`) |
| Conectar con Claude o ChatGPT desde Entorno de trabajo | `94d39ab6` | back §2 (servicio `assistant`) |
| Importar plantilla de empleados y sucursales | (con el conector) | back §2 (`/api/v1/employees/import`, `/welcome`) |
| Material hacia tarea, persona o sucursal | `4ccb774b` | back §4 (migración 034) y rutas `/materials/*` de `inventory` |
| Informes de inventario: nombres y ficheros desde el servidor; el informe sigue a los filtros; historial de almacén en Excel | `3ffeee9f`, `e4d8c94d`, y los de historial | **sin apuntar en el back**: `inventory` con `/warehouses/history-report` y el informe de consumo en Excel. Ver §3 |
| Disponibilidad en Excel desde el servidor | `870d5078` | **sin apuntar en el back**: `checkinbiz`, `availability` con `format=xlsx`. Ver §3 |
| Descargas que avisan si no llega fichero | `22eef410` | nada |
| Buscadores con varias palabras | (fix/buscador-varias-palabras) | nada |
| Dirección del remoto opcional bajo el interruptor; turnos; ocupación al editar | `b6a4a422`, `735d4b26`, `c8ca1823` | nada |
| Alta de empleado sin ausencias y con «Horario semanal» | `e61474a5`, `73258976` | nada |
| QA del 17-oct: #103, #93, #85 y #104 | `2f2ddb5a` | nada |
| Un solo calendario de MUI en toda la app (idioma, semana en lunes, sin selectores nativos) | `da54c2ac` | nada |

---

## 2. Variables de Vercel (producción)

### 2.1 Cómo se revisó (17-oct)

1. Se sacaron de `develop` todas las variables que pide el código: las de `process.env` y las de
   la tabla `BACKEND_PROXY_TARGETS` de `src/lib/http/serverBackendProxy.ts`, que las lee con
   `process.env[envKey]` y que un `grep` de `process.env.` no ve.
2. Se cruzaron con `vercel env ls` del proyecto. Cada entrada del proxy acepta varias claves y
   basta una: se dio por cubierta si existe al menos una en Production.
3. Con `vercel env pull --environment=production` se miró a dónde apunta cada URL de backend.
   Las marcadas *sensitive* salen vacías y no se pueden leer: se comprueban con sondas (§4).

### 2.2 Lo que hay que añadir

| Variable | Valor | Cuándo | Si falta |
|---|---|---|---|
| `NEXT_PUBLIC_ASSISTANT_CONNECTOR_BASE` | `https://api.checkbiz360.com/api/v1/assistant` | **Antes** del build del pase: es pública y se compila dentro | La sección del conector dice «no disponible». Nada más |
| `NEXT_BACKEND_URI_STAFF_IMPORT_HANDLER` | `https://api.checkbiz360.com/api/v1/employees` | Antes del build del pase | El proxy da `403 auth/forbidden` y el diálogo «Importar plantilla» falla |

Las dos en **Production** y en ningún otro entorno. Es el paso 2.15 del back, y depende de
que el back haya abierto las rutas (2.5 y 2.6 allí). Cuidado con dos cosas:

- La base del alta va **sin** `/import`: el panel añade `/import`, `/import/template`,
  `/import/<lote>`, `/import/<lote>/apply` y `/welcome`.
- **No** poner `https://api.checkbiz360.com/api/v1/employees` en ninguna otra variable: el alta,
  la edición y la baja de empleados de producción siguen en Cloud Functions (§5).

### 2.3 Lo que ya está y vale

- Las 66 entradas del proxy, menos la nueva, tienen variable en Production. Las nuevas subrutas de
  `cuadrantes_handler`, `checkinbiz_inventory_handler` y `checkinbiz_tasks_handler` no piden
  variable: van por la misma base. `CUADRANTES_HANDLER` (`…/api/v1/gpt/cuadrantes`) y
  `TASKS_HANDLER` (`…/api/v1/tasks`) apuntan a la API nueva.
- `NEXT_PUBLIC_GA_ID` no está en producción y no hace falta: el código cae a `G-1RKB5RT7NG`.
- Las `NEXT_PUBLIC_FIREBASE_DEV_*` son de desarrollo y en producción no se leen.
- **Corrige una nota del pase de septiembre:** `NEXT_BACKEND_URI_CHECKINBIZ_DOWNLOAD_REPORTS`
  sí está definida en producción desde hace unos 43 días, con `https://api.checkbiz360.com/api`.
  La regla de dejarla sin definir ya no aplica.
- Las variables creadas el 11 y 12 de octubre (panel de hoy, avisos, cobros, inventario, firma)
  ya están compiladas: el despliegue vivo es del 14-oct.

### 2.4 Sin verificar desde aquí

Las *sensitive* no se pueden leer: `CHECKINBIZ_INVENTORY_HANDLER`, `CHECKBIZ360_REPORTS*`,
`CHECKBIZ360_MERLIN*`, `PANEL_OVERVIEW`, `STATS_PANEL`, `DOWNLOAD_DOCUMENTS`, `SIGNING_CA`,
`BILLING_INVOICES`. Las nuevas del panel en inventario e informes de inventario pasan por
`CHECKINBIZ_INVENTORY_HANDLER` y `CHECKBIZ360_REPORTS_INVENTORY`. Se dan por buenas porque las
pantallas que ya están en producción con ellas funcionan, y se confirman en §4.

### 2.5 Preview no es staging

El entorno Preview de Vercel casi no tiene variables (solo `TEAMS_HANDLER` y
`COLLABORATORS_HANDLER`). Un despliegue de rama en Vercel no sirve para probar este pase: se
prueba con el panel local contra `api-staging` (`npm run start:dev`), como hasta ahora.

---

## 3. Orden y dependencias con el back

**Regla:** el panel sube **después** de que el back haya pasado `staging → main` y sus sondas den
bien. Si el panel sube antes, nada se cae, pero estas pantallas dan error:

| Pantalla | Con la API vieja se vería |
|---|---|
| Calendario semanal de tareas | En blanco con un toast de error (`404` en `/tasks/calendar`) |
| Importar cuadrante (descargar plantilla, lotes) | Error al descargar la plantilla (`404`) |
| Conector | La dirección se copia pero no conecta |
| Importar plantilla de empleados | Error en el diálogo (`404` de nginx) |
| Material por destino | Error al cargar el material de la ficha |
| Historial de almacén e informe de consumo en Excel | Aviso de «la descarga no trae fichero» |
| Disponibilidad en Excel | Aviso de «la descarga no trae fichero» (la API vieja ignora `format=xlsx` y devuelve la rejilla) |

**🔴 Falta en el guion del back.** Dos cosas que el panel usa y que solo están en `staging` de
`encodebiz-api` no aparecen en `proximo-pase-back.md`:

- `inventory`: `/warehouses/history-report` y `/warehouses/:id/history-report`, el informe de
  consumo en Excel (`format=xlsx` en el informe de inventario) y `/materials/*`. Este último
  sí está en §4 por su migración, pero no sus rutas.
- `checkinbiz`: la disponibilidad en Excel (`AvailabilityXLSX`, `format=xlsx` en
  `/calendar/availability`).

No piden variable ni nginx nuevos, pero sí que `inventory`, `reports` y `checkinbiz` se
reconstruyan con el código de `staging`. Apuntarlos en §0 del back antes del día.

### Guion, en orden

| # | Paso | Cómo | Estado |
|---|---|---|---|
| F.1 | Back hecho | §1, §3, §8 y §2 del back con sus sondas en verde; como mínimo 1.6, 2.12–2.14, 3.1 y 8.3 | PENDIENTE |
| F.2 | Variables | Añadir las dos de §2.2 en Vercel, solo Production. Comprobar con `vercel env ls production` que salen | **HECHO 17-oct**, por otra sesión, minutos antes de que fuera a añadirlas: las dos en Production y en ningún otro entorno. `NEXT_PUBLIC_ASSISTANT_CONNECTOR_BASE` leída y correcta. `NEXT_BACKEND_URI_STAFF_IMPORT_HANDLER` es *sensitive* y no se puede leer: se confirma en 4.2 (si da `403`, revisar su valor) |
| F.3 | `develop → staging` | Merge `--no-ff` y push. Hoy `develop` lleva 3 commits que `staging` no tiene (calendario MUI, cuadrante solo lunes, cuadrante primero). `staging` tiene `aa225e38`, que es la copia del hotfix #102 que `main` y `develop` ya tienen: el merge no da conflicto | PENDIENTE |
| F.4 | Comprobación en local contra staging | `npm run start:dev` con `staging` y una vuelta por las pantallas de §1 | PENDIENTE |
| F.5 | `staging → main` | PR `staging → main` y merge. Vercel despliega solo. Antes, `git rev-list --count origin/staging..origin/main` debe dar `0`: si alguien metió un hotfix en `main`, reconciliar primero como en septiembre | PENDIENTE |
| F.6 | Build | En Vercel, el despliegue de `main` en `Ready`. Su `created` tiene que ser posterior a F.2; si no, *Redeploy* sin caché | PENDIENTE |
| F.7 | Sondas y prueba con sesión | §4 | PENDIENTE |

---

## 4. Comprobación en producción

En la empresa de pruebas, nunca en la de un cliente.

| # | Qué | Bien si | Estado |
|---|---|---|---|
| 4.1 | Entorno de trabajo → «Conectar con Claude o ChatGPT» | Sale la dirección `https://api.checkbiz360.com/api/v1/assistant/mcp/e/<entityId>`, no el aviso de «no disponible». Si sale el aviso, F.2 no llegó al build | PENDIENTE |
| 4.2 | Empleados → «Importar plantilla» → descargar | Baja el Excel. Un `403` es la variable; un `404`, nginx del back | PENDIENTE |
| 4.3 | Gestión de tareas → «Calendario semanal» | Carga la semana; prueba 8.6 del back | PENDIENTE |
| 4.4 | Sucursal → «Importar cuadrante» (primer bloque) → descargar plantilla | Baja el Excel; el calendario solo deja lunes; prueba 3.5 del back | PENDIENTE |
| 4.5 | Inventario → historial de un almacén y de todos; informe de consumo en Excel | Bajan los ficheros | PENDIENTE |
| 4.6 | Horarios → Disponibilidad → Excel | Baja el fichero | PENDIENTE |
| 4.7 | Material de una sucursal o persona | Columna «En el centro» / «En su poder» con datos | PENDIENTE |
| 4.8 | Calendarios | En español y en inglés, la semana empieza en lunes; fechas con hora en crear tarea | PENDIENTE |
| 4.9 | QA del 17-oct | Tabla de sucursales con búsqueda: empleados y paginación bien (#104); quitar sucursal a un empleado dice «Quitar» (#93); sin «Hoy» en reportes (#85); onboarding sin la frase (#103) | PENDIENTE |

## 5. Lo que sigue en Cloud Functions, y por qué no entra

En producción, estas variables apuntan a Cloud Functions (`apiv100-firebaseentryhttp-…`). En
`.env.development` apuntan a la API nueva de staging. **No hay que cambiarlas en este pase**: en
producción no hay nada detrás de la ruta nueva.

| Variable de producción | En staging va a | Servicio | En prod |
|---|---|---|---|
| `ASSING_USER` (invitar colaborador) | `/api/v1/entities/collaborators` | `entities` | no corre |
| `CREATE_ENTITY`, `UPDATE_ENTITY`, `UPDATE_BRANDNG_ENTITY` | `/api/v1/entities…` | `entities` | no corre |
| `CREATE_USER`, `RECOVERY_PASS` | `/api/v1/users…` | `entities` | no corre |
| `UPLOAD_MEDIA`, `DELETE_MEDIA`, `NEXT_PUBLIC_…UPLOAD_MEDIA` | `/api/v1/media` | `entities` | no corre |
| `CREATE_SUCURSAL`, `UPDATE_SUCURSAL`, `DELETE_SUCURSAL` | `/api/v1/branches…` | `branches` | no corre (el back §2.2 lo arranca solo en red interna) |
| `CHECKINBIZ_CREATE/UPDATE/DELETE/VALIDATE_EMPLOYEE`, `RESPONSABILITY_HANDLER` | `/api/v1/employees…` | `employees` | corre, pero nginx solo abre `/teams` (y §2.6 abrirá `/import` y `/welcome`) |
| `CHECKINBIZ_ENABLE2AF_EMPLOYEE`, `CHECKINBIZ_VERIFY2AF_EMPLOYEE` | `/api/v1/checkinbiz/auth/2fa/…` | `checkinbiz` | por comprobar |
| `CHECKINBIZ_STATS` | `/api/analytics/heuristic` | `analytics` | por comprobar |
| `CREATE_WEBHOOK`, `DELETE_WEBHOOK` | — (no están en dev) | — | — |
| `DELETE_ENTITY` | Cloud Function también en dev | — | — |

**Por qué asignar usuario tira a Firebase.** La invitación completa (crear la cuenta si no
existe y mandar el correo) está portada en `services/entities`, ruta
`/api/v1/entities/collaborators`. El núcleo (`checkinbiz`, `POST /collaborators`) solo da asiento
a quien ya tiene cuenta, y por eso el panel no puede usarlo para invitar. `entities` no está en
el `docker-compose.yml` ni en el `nginx/nginx.conf` de producción: es el corte de la fase 2 de la
salida del monolito, que el back deja fuera de este pase a propósito. Quitar un colaborador sí va
ya por la API nueva (`COLLABORATORS_HANDLER`).

**Para migrarlo**, en un pase propio:

1. Back: arrancar `entities` en producción y abrir en nginx al menos
   `location /api/v1/entities/collaborators`, sin abrir el resto del prefijo. Sonda sin token →
   `401`, no `404`.
2. Vercel: `NEXT_BACKEND_URI_ASSING_USER=https://api.checkbiz360.com/api/v1/entities/collaborators`
   y redeploy (no hace falta código: el panel ya lo usa así en staging).
3. Prueba: invitar a un correo sin cuenta y a uno con cuenta en la empresa de pruebas; los dos
   reciben el correo y aparecen en Colaboradores.
4. Vuelta atrás: devolver la variable a la Cloud Function y redeploy.

El resto de la tabla va igual, servicio a servicio, cuando el back abra cada uno.

---

## 6. Si algo falla

- **Una pantalla nueva da error:** casi siempre es el back sin desplegar (§3). Mirar primero la
  sonda del back, no el panel.
- **`403 auth/forbidden` en el proxy:** antes que la sesión, la variable del handler. La
  comprobación de la variable va antes que la del token.
- **Volver atrás el panel entero:** en Vercel, *Promote to Production* del despliegue anterior
  (`encodebiz-front-saas-8grdmyvmu`, 14-oct). Es inmediato y no toca variables. Después, revertir
  el merge en `main` para que el siguiente despliegue no lo vuelva a subir.
- **Volver atrás una variable:** borrarla en Vercel y *Redeploy*: sin redeploy el build vivo la
  sigue llevando.

---

## Registro del día del pase

Vacío hasta el día del pase.

| Paso | Hora (UTC) | Quién | Resultado y lo que se vio |
|---|---|---|---|

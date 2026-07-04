# encodebiz-api — Servidor V2 (Microservicios)

> Repo: `PLATAFORMA/encodebiz-api/` — standalone, git propio  
> Stack: Node 22 · TypeScript strict · npm workspaces · Docker Compose · nginx  
> Última actualización: 2026-07-04

---

## Por qué existe este servidor

El punto de inflexión fue el **modelo de reportes**. El sistema anterior generaba reportes diarios escaneando Firestore bajo demanda — miles de lecturas en tiempo real por reporte. Con el crecimiento del volumen eso no escala, cuesta dinero y produce información incompleta:

- Los patrones heurísticos se sobreescriben con cada update: **no hay historia**
- Las valoraciones de tareas no estaban integradas en los reportes
- La IA (Merlin) analizaba solo el snapshot actual: no sabía si algo mejoraba o empeoraba

`encodebiz-api` resuelve esto implementando el **Report Pipeline V2**:

> **Firebase = fuente operacional (tiempo real). PostgreSQL = fuente analítica (histórico para IA).**

Además centraliza la lógica que antes estaba en `api-express` (customGPT, checkinbiz) como microservicios propios, independientes de Firebase Functions.

**Documentación de ingeniería completa:** [`DOCS/ingenieria/report-pipeline-v2/`](../ingenieria/report-pipeline-v2/README.md)

---

## Arquitectura

```
encodebiz-api/
├── packages/
│   └── shared/              → firebase admin, openai, pg pool, middlewares
├── services/
│   ├── merlin/    :3001      → IA interpretación operativa (OpenAI)
│   ├── checkinbiz/:3002      → HeuristicCore V2 on-demand
│   ├── sync/      :3003      → Ingesta Firebase → PostgreSQL (S2S)
│   └── analytics/ :3004      → Histórico patrones, reportes, TrendAnalysis
├── nginx/nginx.conf          → Reverse proxy (puerto 80)
├── migrations/001_init.sql   → Schema PostgreSQL (idempotente)
├── docker-compose.yml        → Producción: nginx + postgres + 4 servicios
└── docker-compose.dev.yml    → Desarrollo local: solo postgres en :5435
```

---

## Servicios

### merlin — IA de interpretación operativa (:3001)

Lee patrones pre-computados de Firestore y genera análisis ejecutivos vía OpenAI.  
Auth: **Firebase JWT** (`Authorization: Bearer <token>`)

```
POST /api/v1/gpt/interpret    → análisis de sucursal o empleado
POST /api/interpret           → alias legacy (compatibilidad api-express)
```

Builders disponibles: `BranchInterpret`, `EmployeeAdminInterpret`, `EmployeeFeedback`, `BranchCompare`, `EmployeeCompare`

Ver documentación completa: [`DOCS/modulos/merlin.md`](./merlin.md)

---

### checkinbiz — HeuristicCore on-demand (:3002)

Ejecuta el motor heurístico V2 sobre petición. En Fase 5 del pipeline, Firebase Functions pasan a ser proxy delgado que apunta aquí.  
Auth: **Firebase JWT** (`Authorization: Bearer <token>`)

```
GET /api/v1/checkinbiz/status    → healthcheck del servicio
# Fase 5 (pendiente):
POST /api/v1/checkinbiz/analyze  → HeuristicCore V2 on-demand con TrendAnalysis
```

**Scope actual:** heurística (`HeuristicCore`, `HeuristicCalculator`, `HeuristicEvaluator`, `ProfileClassifier`) + patrones (`buildInitialBranchPattern`). El CRUD de employees, branches y checklogs permanece en Firebase Functions.

---

### sync — Ingesta Firebase → PostgreSQL (:3003)

Recibe eventos de los Firestore triggers de Firebase y persiste en PostgreSQL.  
Auth: **API key S2S** (`X-Encodebiz-Key: <secret>`)  
Implementa **Fase 1** del pipeline.

```
POST /api/sync/checklogs       → UPSERT en checklogs_raw
POST /api/sync/task-ratings    → UPSERT en task_ratings_raw
GET  /api/sync/health          → status del servicio + conexión DB
```

**Patrón de llamada desde Firebase (best-effort awaited):**
```typescript
// En el trigger onWhriteChecklog:
try {
  await SyncChecklogService.push(checklogData);  // timeout 7s
} catch (err) {
  console.error("[SyncChecklog] analytics sync failed", { checklogId, entityId, error: err.message });
  // NO relanza — el flujo principal ya completó
}
```

---

### analytics — Histórico y reportes analíticos (:3004)

Construye reportes enriquecidos desde PostgreSQL y sirve histórico de patrones.  
Auth: **API key S2S** (`X-Encodebiz-Key: <secret>`)

```
# Implementado (Fase 3 lectura):
GET  /api/analytics/patterns/history    → snapshots históricos de patrones

# Pendiente (Fase 2):
POST /api/analytics/build/daily-report  → reporte diario enriquecido con task ratings
```

---

## Pipeline de Reportes V2 — Estado de implementación

| Fase | Descripción | Estado | Servicio |
|------|-------------|--------|----------|
| **0** | Fundación: servidor, migrations SQL, health, auth, Zod | ✅ **Completo** | Todos |
| **1** | Raw Sync: Firebase triggers → PostgreSQL | ✅ **Completo** (server-side). Falta: `SyncChecklogService` en Firebase Functions | `sync` |
| **2** | Daily Report enriquecido desde PostgreSQL + task ratings | ⏳ **Pendiente** | `analytics` |
| **3** | Histórico de patrones: snapshot diario en `pattern_snapshots` | ⏳ **Pendiente** (GET existe, captura no activa hasta Fase 2) | `analytics` |
| **4** | IA con contexto histórico: TrendAnalysis → Merlin | ⏳ **Pendiente** | `merlin` + `analytics` |
| **5** | HeuristicCore migrado al servidor, Firebase como proxy puro | ⏳ **Pendiente** | `checkinbiz` |

**Siguiente paso concreto (Fase 1 cierre):** implementar `SyncChecklogService` y `SyncTaskRatingService` en Firebase Functions (`functions/src/core/analytics/`) y conectarlos a los triggers existentes `onWhriteChecklog` y `onWriteTaskRating`.

Ver diseño completo: [`04_fases.md`](../ingenieria/report-pipeline-v2/04_fases.md)

---

## Schema PostgreSQL

```
checklogs_raw       → réplica analítica de checklogs (Fase 1)
task_ratings_raw    → valoraciones de tareas (Fase 1)
sync_log            → auditoría de syncs con status/duration_ms
daily_reports       → reportes diarios pre-computados (Fase 2)
pattern_snapshots   → fotografía diaria del BranchPattern (Fase 3)
```

Schema completo: [`migrations/001_init.sql`](../../encodebiz-api/migrations/001_init.sql)  
Referencia de diseño: [`03_schema-postgres.md`](../ingenieria/report-pipeline-v2/03_schema-postgres.md)

---

## Auth

| Servicio | Header | Descripción |
|---|---|---|
| `merlin`, `checkinbiz` | `Authorization: Bearer <Firebase JWT>` | Usuario final autenticado |
| `sync`, `analytics` | `X-Encodebiz-Key: <secret>` | Llamadas S2S desde Firebase Functions |

La `ENCODEBIZ_API_KEY` debe coincidir en el `.env` del servidor y en las variables de Firebase Functions.

---

## Desarrollo local

```bash
# 1. Levantar solo PostgreSQL (puerto 5435)
docker compose -f docker-compose.dev.yml up -d

# 2. Construir todo
npm install
npm run build

# 3. Levantar un servicio en modo watch
npm run dev:merlin
npm run dev:sync
npm run dev:analytics
npm run dev:checkinbiz

# 4. Variables de entorno
cp .env.example .env
# Completar: DATABASE_URL, ENCODEBIZ_API_KEY, OPENAI_API_KEY,
#            GOOGLE_APPLICATION_CREDENTIALS (path al firebase-sa.json)
```

**PostgreSQL puertos:**
- `5432` — sistema
- `5433` — GroundApp dev
- `5435` — encodebiz-api dev (este repo)

---

## Deploy (producción)

```bash
# Build y arranque completo
docker compose up --build -d

# Solo un servicio
docker compose up --build merlin

# Ver logs
docker compose logs -f merlin
docker compose logs -f sync
```

**Secretos requeridos en el servidor:**
```
./secrets/firebase-sa.json   → service account de Firebase (montado como volumen)
.env                         → DATABASE_URL, ENCODEBIZ_API_KEY, OPENAI_API_KEY
```

El archivo `./secrets/firebase-sa.json` no se sube al repo (está en `.gitignore`). Se provisiona manualmente en el servidor.

---

## Variables de entorno

| Variable | Servicio | Descripción |
|---|---|---|
| `DATABASE_URL` | sync, analytics, checkinbiz | PostgreSQL connection string |
| `ENCODEBIZ_API_KEY` | sync, analytics | API key S2S compartida con Firebase Functions |
| `OPENAI_API_KEY` | merlin | Clave OpenAI para Responses API |
| `GOOGLE_APPLICATION_CREDENTIALS` | todos | Path a firebase-sa.json |
| `PORT` | todos | Puerto del servicio (default: 3001/3002/3003/3004) |
| `NODE_ENV` | todos | `production` en prod |

---

## Nginx — rutas

```nginx
/api/v1/gpt/        → merlin:3001
/api/v1/checkinbiz/ → checkinbiz:3002
/api/sync/          → sync:3003
/api/analytics/     → analytics:3004
```

---

## Migración gradual desde Firebase Functions

Firebase Functions actúan como proxy delgado hacia los servicios de `encodebiz-api` mientras la migración avanza:

```
Estado actual:
  ✅ merlin      — Firebase merlinIa → proxy → encodebiz-api/merlin (pendiente de conectar)
  ⏳ sync        — Falta SyncChecklogService en Firebase Functions
  ⏳ checkinbiz  — Falta en Fase 5 (Firebase analyzeHeuristic → proxy → checkinbiz:3002)

Permanece en Firebase (sin plan de migración):
  - CRUD employees, branches, checklogs
  - Autenticación / login
  - Notificaciones FCM
  - Documentos, passinbiz
```

Ver estado de funciones activas: [`DOCS/DEPLOY.md`](../DEPLOY.md)

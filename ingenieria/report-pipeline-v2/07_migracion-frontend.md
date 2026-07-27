# Guía de migración — Front de administración CheckBiz → API privado (`api.checkbiz360.com`)

> **Para:** equipo de front de la administración de CheckBiz.
> **Qué cubre:** cómo migrar el front para consumir el nuevo API privado (`encodebiz-api`) en
> lugar de la lógica antigua en Cloud Functions. Servicios afectados: **merlin** (IA),
> **reports** (PDF/Excel) y **analytics** (patrones/tendencias).
> **Fuente de verdad:** el código de los routers en `encodebiz-api` (ver §10). Este doc resume
> los contratos; si hay discrepancia, manda el router.

---

## 1. Contexto y objetivo

La lógica de IA, generación de informes y analítica de patrones **se ha movido de Cloud
Functions a un API privado propio** desplegado en `https://api.checkbiz360.com`. El front debe
dejar de llamar a las Functions antiguas para estas cosas y pasar a:

| Necesidad en el front | Antes | Ahora |
|---|---|---|
| Interpretación IA de centros/empleados | Function | **merlin** — `POST /api/v1/gpt/interpret` (async + snapshot) |
| Generar informe de jornada (PDF) | Function | **reports** — `POST /api/reports/generate` |
| Generar informe en **Excel** | *no existía* | **reports** — mismo endpoint, `format: "xlsx"` |
| Histórico de patrones / tendencias | Function / Firestore | **analytics** (S2S — ver §6, el front NO lo llama directo) |

---

## 2. Arquitectura y routing

Todo entra por **nginx** en `https://api.checkbiz360.com` (TLS Let's Encrypt) y se reparte por path:

| Path público | Servicio | Auth | ¿Lo llama el front (navegador)? |
|---|---|---|---|
| `/api/v1/gpt/*` | merlin | **Firebase ID token** | ✅ Sí |
| `/api/v1/checkinbiz/*` | checkinbiz | **Firebase ID token** | ✅ Sí (en migración, ver §7) |
| `/api/reports/*` | reports | por-ruta (ver §5) | ✅ `/generate` (Firebase); ❌ `/cron`, `/status` (S2S) |
| `/api/analytics/*` | analytics | **`X-Encodebiz-Key`** (S2S) | ❌ **No** (ver §6) |
| `/api/sync/*` | sync | **`X-Encodebiz-Key`** (S2S) | ❌ No |
| `/health` | nginx | pública | — |

**Regla de oro:** el front solo llama a endpoints con **Firebase Auth**. Los endpoints con
`X-Encodebiz-Key` son server-to-server; **la key nunca puede ir en el navegador**.

---

## 3. Autenticación (Firebase ID token)

Los endpoints front-facing verifican un **Firebase ID token** del usuario administrador
(proyecto Firebase `encodebiz-services`). El middleware exige la cabecera:

```
Authorization: Bearer <ID_TOKEN>
```

En el front (Firebase Web SDK):

```ts
import { getAuth } from "firebase/auth";

const token = await getAuth().currentUser!.getIdToken();
const res = await fetch("https://api.checkbiz360.com/api/v1/gpt/interpret", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  },
  body: JSON.stringify({ request: { /* ... */ } }),
});
```

- El token **caduca a la hora**; `getIdToken()` lo refresca solo si hace falta. Pídelo justo
  antes de cada llamada (no lo caches largo rato).
- Un token inválido/caducado → **401** `{ error: "unauthenticated", message }`.

---

## 4. Merlin — interpretación IA (**async + snapshot**) ⭐

Es el cambio más importante de patrón. **Merlin NO devuelve el resultado en la respuesta HTTP**
(salvo cache hit): lanza un job en segundo plano y el front **se suscribe a un documento de
Firestore** para recibir el resultado.

### Endpoint
```
POST /api/v1/gpt/interpret        (Firebase Auth)
```

### Request

Envoltorio: `{ "request": { ... } }`.

**Interpretar/comparar CENTROS:**
```jsonc
{
  "request": {
    "entityId": "qCUKnSnceXje2u6ECxmH",      // requerido
    "branchIds": ["Gj8AsdQW...", "1Wm37TN..."], // 1+ ids
    "mode": "interpret",                       // "interpret" | "compare"
    "lang": "es",                              // "es" | "en"
    "locale": "es"                             // "es" | "en" | "pt"
  }
}
```

**Interpretar un EMPLEADO:**
```jsonc
{
  "request": {
    "entityId": "qCUKnSnceXje2u6ECxmH",  // requerido
    "employeeId": "hctKZJFw...",          // requerido para target empleado
    "branchId": "Gj8AsdQW...",            // opcional (si falta → patrón a nivel entidad)
    "target": "employee",
    "audience": "admin",                  // "admin" (por defecto) | "employee"
    "lang": "es",
    "locale": "es"
  }
}
```

Validación (400 `invalid_request` si no se cumple): hace falta `entityId` + (`branchIds` no
vacío **o** `employeeId`); `mode ∈ {interpret, compare}`; `target ∈ {branch, employee}`;
`lang ∈ {es, en}`; `locale ∈ {es, en, pt}`.

### Respuesta HTTP

| `code` | HTTP | Significado | Trae `result`? |
|---|---|---|---|
| `ai/cache_hit` | **200** | Ya había un análisis fresco (cache TTL 7 días) | **Sí**, inline |
| `ai/analysing` | **202** | Se lanzó el job; suscríbete al doc | No — usa `path` |
| `pattern/not_found` | **404** | No hay patrón para ese empleado | No |
| (error interno) | 500 | — | No |

Cuerpo (ejemplo 202):
```json
{ "code": "ai/analysing", "cached": false, "path": "ai-analizer/6f1c2a…" }
```

### El flujo async (lo que tiene que hacer el front)

1. `POST /interpret`.
2. Si **200** (`ai/cache_hit`) → usa `response.result` directamente. Fin.
3. Si **202** (`ai/analysing`) → **suscríbete al documento Firestore** que indica `path`
   (colección `ai-analizer`, id = md5 de los filtros). Espera a que `status === "completed"` y
   lee `result`.
4. Si **404** → no hay datos suficientes para ese empleado; muéstralo como tal.

Documento en `ai-analizer/{id}`:
```jsonc
{
  "id": "6f1c2a…",
  "filters": { "type": "interpret-branch", "branchIds": [...], "lang": "es", "entityId": "...", "promptVersion": "v2" },
  "status": "analysing" | "completed" | "insufficient_data",
  "result": { /* InterpretationResult, presente cuando completed */ },
  "createdAt": <Timestamp>,
  "updatedAt": <Timestamp>
}
```

Suscripción (Firebase Web SDK):
```ts
import { doc, onSnapshot } from "firebase/firestore";

function subscribeAnalysis(path: string, onResult, onError) {
  const unsub = onSnapshot(doc(db, path), (snap) => {
    const d = snap.data();
    if (!d) return;
    if (d.status === "completed")          { unsub(); onResult(d.result); }
    else if (d.status === "insufficient_data") { unsub(); onError("insufficient_data"); }
    // status "analysing" → seguir esperando
  });
  return unsub;
}
```

### `InterpretationResult` (el `result`)
```ts
interface InterpretationResult {
  version?: string;        // versión de Merlin que lo generó (ej. "0.2.0")
  headline: string;
  summary: string;
  body: string;
  actions: string[];
  confidenceNote: string;
  profileType?: "anchor" | "maverick" | "ghost" | "at-risk" | "neutral";
  diagnosis?: Array<{ tag: string; reason: string; evidence?: Record<string, unknown> }>;
  evidence?: Record<string, unknown>;
  clean?: Record<string, unknown>;
  raw?: unknown;
}
```

### Notas / gotchas de merlin
- **Cache 7 días**: la misma consulta (mismos filtros) devuelve `ai/cache_hit` durante 7 días.
  Para forzar recálculo hay que cambiar algún filtro o esperar a que caduque.
- **Fragilidad conocida**: si el job de fondo se cae a mitad, el doc puede quedarse en
  `analysing` sin auto-recuperarse. **El front debe poner un timeout** (ej. 60–90 s) y ofrecer
  reintentar en vez de quedarse colgado en el `onSnapshot`.
- El `result.version` sirve para saber con qué versión de Merlin se generó un análisis cacheado.

---

## 5. Reports — informe de jornada (PDF / **Excel**)

### Endpoint
```
POST /api/reports/generate        (Firebase Auth)
```

### Request
```jsonc
{
  "entityId": "qCUKnSnceXje2u6ECxmH",  // requerido
  "start": "2026-06-01",               // YYYY-MM-DD
  "end":   "2026-06-30",               // YYYY-MM-DD
  "branchId": "Gj8AsdQW...",           // opcional (filtra a un centro)
  "employeeId": "hctKZJFw...",         // opcional (filtra a un empleado)
  "format": "pdf"                      // opcional: "pdf" (defecto) | "xlsx"  ← NUEVO
}
```

### Respuesta
```jsonc
// 201
{
  "reporData": {
    "branch": "Venice Shores, Montage at Midtown",
    "employee": "Elvia Larios, Mirla, …",
    "entity": "ACB2 Painting Services LLC",
    "entityId": "qCUKnSnceXje2u6ECxmH",
    "start": "2026-06-01T00:00:00.000Z",
    "end":   "2026-06-30T23:59:59.999Z",
    "status": "active",
    "ref": { "path": "checkbiz/reports/entities/{entityId}/{start}-{end}_{ts}.pdf" }
  },
  "code": "report/success"
}
// 204  → no hay datos para esos filtros (code "report/not_checklog_found")
```

- **`format: "xlsx"`** genera un Excel: hoja *Registro de jornada* (una fila por jornada, con
  autofiltro y fila TOTAL) + hoja *Resumen por trabajador*. El `ref.path` termina en `.xlsx`.
- **`ref.path` es una ruta en Firebase Storage, no una URL.** Para descargar, resuélvela con el
  SDK de Storage:
  ```ts
  import { getStorage, ref as sref, getDownloadURL } from "firebase/storage";
  const url = await getDownloadURL(sref(getStorage(), reporData.ref.path));
  ```

### CORS
`reports` **tiene CORS habilitado** (`app.use(cors())`, igual que merlin/checkinbiz), así que el
front **puede llamar `/api/reports/generate` directamente desde el navegador** con el Bearer
token. (Requiere que el backend esté desplegado con ese cambio.)

---

## 6. Analytics y Sync — S2S (el front **NO** los llama directo)

`/api/analytics/*` y `/api/sync/*` usan `X-Encodebiz-Key` (secreto server-to-server). **No se
pueden llamar desde el navegador** (la key no puede exponerse).

- Endpoint relevante: `GET /api/analytics/patterns/history?entityId=…&branchId=…&days=30`
  (o con `employeeId`). Devuelve `snapshots[]` + `evidence` (pack de tendencias TDR-007).
- **Cómo obtiene el front estos datos:**
  1. Gran parte de la analítica ya viene **narrada** dentro del `result` de merlin (`evidence`,
     `diagnosis`, `actions`).
  2. Para datos crudos de patrones/tendencias, exponer un **proxy en Cloud Functions** que
     llame a analytics con la key server-side, o leerlos de **Firestore** (colecciones
     `checkbiz_branch_patterns` / `checkbiz_employee_patterns`).

---

## 7. Checkinbiz — en migración

`/api/v1/checkinbiz/*` (Firebase Auth) hoy es casi placeholder (solo `GET /status`). Las rutas
de heurística y `patterns/history` se irán migrando desde Firebase. **No cablear nada del front
contra checkinbiz todavía** salvo `/status`; consultar con backend el calendario.

---

## 8. Checklist de migración (front)

- [ ] Configurar base URL `https://api.checkbiz360.com`.
- [ ] Adjuntar `Authorization: Bearer <idToken>` (refrescado) en toda llamada front-facing.
- [ ] **Merlin**: implementar el flujo async — POST, y si 202 suscribirse al doc `path` en
      Firestore hasta `status: completed`; manejar `insufficient_data`, `pattern/not_found` y
      **timeout** de `analysing`.
- [ ] Reutilizar cache (no re-lanzar la misma consulta; 200 `cache_hit` llega solo).
- [ ] **Reports**: selector **PDF/Excel** (`format`), resolver `ref.path` → download URL con
      Storage. CORS ya habilitado → se llama directo desde el navegador.
- [ ] **Analytics**: NO llamar directo; consumir vía merlin / proxy Function / Firestore.
- [ ] Quitar del front las llamadas antiguas a Cloud Functions para IA/informes.

---

## 9. Errores comunes (resumen)

| Código | Dónde | Causa |
|---|---|---|
| 401 `unauthenticated` | merlin/checkinbiz/reports-generate | falta/expiró el Bearer token |
| 400 `invalid_request` | merlin | faltan `entityId`/`branchIds`/`employeeId` o enum inválido |
| 400 `validation_error` | reports | `start`/`end` no son `YYYY-MM-DD`, o `format` inválido |
| 404 `pattern/not_found` | merlin (empleado) | no hay patrón para ese empleado |
| 204 `report/not_checklog_found` | reports | no hay jornadas para esos filtros |

---

## 10. Fuentes de verdad y dónde buscar

- **Contratos (código, manda sobre este doc):** routers en `encodebiz-api/services/*/src/interfaces/*.router.ts`
  y el auth en cada `services/*/src/app.ts`. Routing público en `encodebiz-api/nginx/nginx.conf`.
- **Tipos:** `services/merlin/src/domain/index.ts` (`InterpretationResult`),
  `services/reports/src/domain/ReportTypes.ts`.
- **Documentación canónica (repo hermano `PLATAFORMA/DOCS`):**
  `ingenieria/report-pipeline-v2/` — TDRs (`TDR-003` daily build, `TDR-005/007` tendencias) y
  ADRs (`ADR-002` sync, `ADR-008` tz del cron). `modulos/merlin.md` para Merlin.
- **Dominio / entorno:** API en `https://api.checkbiz360.com`; Firebase `encodebiz-services`.

# CheckinBiz App — Startup V2: Critical Handler + Warm-up

## 1. Contexto y problema

### Flujo V1 (actual)

Desde que el empleado abre la app hasta que puede marcar asistencia se encadenan **4 Cloud Functions independientes**, cada una con su propio cold start:

```
App abre
  → loginEmployee          CF independiente  → cold start #1 (3-8s)
  → validateEmployee       CF independiente  → cold start #2 (3-8s)
  → calendarHandler        CF independiente  → cold start #3 (3-8s)
  → createChecklog         CF independiente  → cold start #4 (3-8s)
                                               ──────────────────────
                                               Total peor caso: ~20-32s
```

Cold start ocurre cuando Firebase no tiene una instancia activa de esa función (inactividad, primer uso del día, escalado desde cero).

---

## 2. Solución V2

Dos estrategias combinadas:

### 2.1 `criticalHandler` — Express bundle

`loginEmployee`, `validateEmployee` y `calendarHandler` se consolidan en **un único Cloud Function Express**. Un solo cold start cubre los tres pasos de arranque de la app.

```
criticalHandler (Express — 1 sola CF)
  POST  /auth/login        ← loginEmployee logic
  POST  /auth/validate     ← validateEmployee logic
  GET   /calendar/*        ← calendarHandler routes
```

### 2.2 Warm-up ping a `createChecklog`

`createChecklog` se mantiene separado (tiene config especial: `cpu:1, concurrency:20, memory:512MiB`). Se pre-calienta automáticamente como efecto secundario del login: `validateEmployee` dispara un ping HTTP fire-and-forget **antes de devolver la respuesta** al cliente. Cuando el empleado llega a la pantalla de marcaje, la función ya está caliente.

```
criticalHandler.validateEmployee()
  1. Procesa la validación
  2. dispara warmupChecklog() → fire & forget (no bloquea)
  3. devuelve respuesta al cliente

createChecklog recibe /_warmup → retorna 200 inmediatamente
  → instancia queda caliente para el marcaje real
```

### Flujo V2

```
App abre
  → criticalHandler/auth/login     1 cold start cubre los 3 pasos
  → criticalHandler/auth/validate  ← warm, misma instancia
    ↳ dispara ping a createChecklog en background
  → criticalHandler/calendar/*     ← warm, misma instancia
  → createChecklog                 ← ya caliente por el ping ✅
                                   ──────────────────────────────
                                   Total: 1 cold start (~3-8s)
```

---

## 3. Especificación técnica

### Cloud Function: `criticalHandler`

```typescript
functions.https.onRequest({
  cors: true,
  concurrency: 200,
  memory: "256MiB",
  minInstances: 0,   // sin costo fijo; el warm-up ping mantiene caliente
  maxInstances: 10,
  timeoutSeconds: 30,
})
```

### Warm-up endpoint en `createChecklog`

Se agrega **antes** de la validación JWT:

```typescript
// create-checklog entry
if (req.body?._warmup === true) {
  return res.status(200).json({ ok: true });
}
```

El ping se emite desde `validateEmployee` como fire-and-forget:

```typescript
function warmupChecklog(): void {
  fetch(`${process.env.CHECKLOG_INTERNAL_URL}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ _warmup: true }),
  }).catch(() => {}); // error intencional — no afecta al caller
}
```

`CHECKLOG_INTERNAL_URL` se define en `.env`:
```
CHECKLOG_INTERNAL_URL=https://us-central1-dev-encodebiz.cloudfunctions.net/apiV100-firebaseEntryHttp-checkinbiz-createChecklog
```

---

## 4. Cambio de endpoints — Guía de integración para la app

> **La app debe actualizar las 3 llamadas de arranque al nuevo handler.**  
> El contrato de request/response es idéntico — solo cambia la URL base.

### Base URL

| Entorno | V1 (actual) | V2 (nuevo) |
|---|---|---|
| Dev | `https://us-central1-dev-encodebiz.cloudfunctions.net/` | `https://us-central1-dev-encodebiz.cloudfunctions.net/apiV100-firebaseEntryHttp-criticalHandler` |
| Prod | `https://us-central1-encodebiz-saas.cloudfunctions.net/` | `https://us-central1-encodebiz-saas.cloudfunctions.net/apiV100-firebaseEntryHttp-criticalHandler` |

### Mapa de endpoints

| Función | Endpoint V1 | Endpoint V2 | Cambio |
|---|---|---|---|
| Login empleado | `POST .../apiV100-firebaseEntryHttp-loginEmployee` | `POST .../criticalHandler/auth/login` | URL |
| Validar empleado (QR) | `POST .../apiV100-firebaseEntryHttp-checkinbiz-validateEmployee` | `POST .../criticalHandler/auth/validate` | URL |
| Calendario efectivo | `GET .../apiV100-firebaseEntryHttp-checkinbiz-calendarHandler/calendar/*` | `GET .../criticalHandler/calendar/*` | URL |
| Crear checklog | `POST .../apiV100-firebaseEntryHttp-checkinbiz-createChecklog` | **sin cambio** | — |

### Detalle por endpoint

#### `POST /auth/login`

**Request** — igual que V1:
```json
Headers:
  Authorization: Bearer <firebase-token>

Body: (ninguno)
```

**Response** — igual que V1:
```json
[
  {
    "employeeId": "abc123",
    "uid": "uid",
    "email": "empleado@empresa.com",
    "entity": { "entityId": "ent123", "name": "Mi Empresa" },
    "fullName": "Juan Pérez",
    "tokenValidateEmployee": "<base64>"
  }
]
```

#### `POST /auth/validate`

**Request** — igual que V1:
```json
Headers:
  (sin auth header — usa sessionToken propio)

Body:
{
  "token": "<base64-employee-token>"
}
```

**Response** — igual que V1:
```json
{
  "message": "Employee validated successfully",
  "payload": {
    "name": "Juan Pérez",
    "twoFa": true,
    "entityId": "ent123",
    "employeeId": "emp456"
  },
  "sessionToken": "<jwt>",
  "expiresAt": null,
  "branchId": ["branch1", "branch2"]
}
```

> **Nota:** internamente este endpoint también dispara el warm-up de `createChecklog`. La app no necesita hacer nada adicional.

#### `GET /calendar/*`

Mismas rutas y parámetros que el `calendarHandler` V1, solo cambia el prefijo base.

---

## 5. Variables de entorno nuevas

Agregar en `functions/.env` y `functions/.env.production`:

```bash
# URL interna para warm-up de createChecklog
CHECKLOG_INTERNAL_URL=https://us-central1-dev-encodebiz.cloudfunctions.net/apiV100-firebaseEntryHttp-checkinbiz-createChecklog
```

```bash
# Production
CHECKLOG_INTERNAL_URL=https://us-central1-encodebiz-saas.cloudfunctions.net/apiV100-firebaseEntryHttp-checkinbiz-createChecklog
```

---

## 6. Función nueva a desplegar

```bash
# Dev
npm run deploy:function:dev -- apiV100-firebaseEntryHttp-criticalHandler

# Prod (tras validar en dev)
npm run deploy:function:prod -- apiV100-firebaseEntryHttp-criticalHandler
```

Las funciones V1 (`loginEmployee`, `validateEmployee`) **se mantienen activas** durante la transición para no romper versiones anteriores de la app. Se pueden deprecar una vez que la app actualice los endpoints.

---

## 7. Estado

| Fase | Estado |
|---|---|
| Documentación | ✅ Completa |
| Implementación backend | 🔄 En progreso |
| Testing en dev | ⏳ Pendiente |
| Integración app | ⏳ Pendiente — requiere actualizar 3 endpoints |
| Deploy prod | ⏳ Bloqueado hasta validar dev |

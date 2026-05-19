# Capa Backend — Cloud Functions

## 1. Stack

| Componente | Tecnología |
|---|---|
| Runtime | Node 22, TypeScript strict |
| Framework | Firebase Functions v2 (`firebase-functions/v2`) |
| Admin SDK | firebase-admin v12 |
| DB | Firestore (Admin SDK directo) |
| Date/Time | Luxon (`DateTime`) |
| Push | FCM via firebase-admin/messaging |
| Storage | Firebase Storage |
| Email | Nodemailer (lazy import) |
| PDF | pdfkit (lazy import) |
| SMS | Twilio (lazy import) |
| Imagen | sharp (lazy import) |
| Arquitectura | DDD — domain / application / infrastructure / interfaces |

## 2. Estructura de Carpetas

```
functions/src/services-saas/checkinbiz/
  domain/
    entities/             → entidades de dominio (Task, CheckLog, Employee...)
    interfaces/           → interfaces de repositorios
  application/
    use-cases/
      checklog/           → CreateChecklog, RequestManualChecklogCreation, UpdateChecklog...
      task/               → CreateTask, UpdateTask, AssignTaskWorkers...
    notifications/        → TaskNotificationService, CheckbizNotifier...
  infrastructure/
    repository/           → FirestoreChecklogRepository, FirestoreTaskRepository...
  interfaces/
    http/
      checklog/           → controllers de checklog
      task/               → controllers de task (taskRouter.ts)
  firebase-checkinbiz-http/
    tasks.ts              → entry point para tasksHandler
    index.ts              → exporta todas las Cloud Functions
```

## 3. Patrón de Entry Point

Cada Cloud Function HTTP monta un router/app Express interno:

```typescript
// firebase-checkinbiz-http/tasks.ts
import * as functions from "firebase-functions/v2";
import {taskRouter} from "../interfaces/http/task/taskRouter";

export const tasksHandler = functions.https.onRequest(taskRouter);
```

El router interno usa Express y gestiona autenticación, validación, y enrutamiento.

## 4. Nomenclatura de Funciones

```
apiV100-{tipo}-{servicio}-{nombre}

Tipos:
  firebaseEntryHttp              → HTTP functions
  firebaseFirestoreTriggers*     → Firestore triggers
  firebaseScheduled*             → Scheduled functions
```

## 5. Autenticación

```
1. Firebase Auth → idToken (JWT)
2. POST /auth/loginEmployee con idToken
3. Backend valida y genera sessionToken (JWT propio)
4. Todas las llamadas: Authorization: Bearer {sessionToken}
5. validateToken() middleware: decodifica y setea req.body.uid
```

## 6. Cold Start — Lazy Imports

Los paquetes pesados usan lazy import para no penalizar el arranque del bundle:

| Paquete | Peso | Patrón |
|---|---|---|
| `sharp` | ~8–10 MB | `await import("sharp")` (función async) |
| `pdfkit` | ~500 KB | `await import("pdfkit")` (función async) |
| `twilio` | ~1–2 MB | `import type` + `require()` (mantiene API síncrona) |
| `nodemailer` | ~500 KB | `import type` + `require()` (constructor síncrono) |

**Impacto:** ~12–14 MB eliminados del proceso de inicialización para funciones que no usan estos paquetes.

**Por qué `require()` para twilio/nodemailer:** Sus APIs son síncronas (`TwilioClient.getClient()`, constructor de `EmailService`). Convertir a `async` requeriría actualizar todos los callers. En CJS (compilación de Firebase Functions), `require()` dentro de una función es lazy por naturaleza.

`firebase-admin` no es candidato a lazy load — es obligatorio para todas las funciones.

## 7. Patrones Firestore

### Timestamps

`findById` devuelve `doc.data()` sin conversión automática de Timestamps. Las comparaciones de fechas requieren:

```typescript
const ts = (doc.timestamp as any)?.toDate?.() ?? new Date(doc.timestamp as any);
```

Algunos repositorios hacen la conversión explícitamente en `findAll*`. Verificar siempre el método específico antes de asumir tipo `Date`.

### Escrituras atómicas

```typescript
// Batch para escrituras relacionadas
const batch = db.batch();
batch.set(ref1, data1);
batch.set(ref2, data2);
await batch.commit();

// arrayUnion para arrays append-only
FieldValue.arrayUnion(newEntry)  // requestUpdates, etc.

// set({merge: true}) — deep merge, NO reemplaza nested maps
db.collection(path).doc(id).set(changes, {merge: true})
```

### Lecturas eficientes

```typescript
// Solo campos necesarios
db.collection(path).select("field1", "field2")

// Nunca leer documentos completos si solo se necesitan campos específicos
```

### Índices compuestos

Documentar en `firestore.indexes.json`. Queries con múltiples `where` + `orderBy` requieren índice compuesto.

## 8. Manejo de Errores HTTP

Formato estándar de error:

```json
{
  "error": "Descripción legible",
  "code": "module/error_code",
  "details": ["campo: mensaje"]  // opcional, solo en validación
}
```

Los códigos de error están en [DOMINIO.md](../DOMINIO.md#7-códigos-de-error-estándar).

## 9. Reglas Operativas

- Nunca enviar secretos en código fuente ni en logs
- Validar toda entrada en controllers/routes (borde del sistema)
- Cloud Functions para operaciones sensibles — nunca directamente desde cliente
- `FieldValue.arrayUnion()` para arrays append-only (nunca sobrescribir `requestUpdates`)
- `set({merge: true})` no reemplaza nested maps — úsalo conscientemente
- Notificaciones FCM: fire-and-forget, nunca bloquear flujo principal
- Heavy deps: siempre lazy import (cold start)

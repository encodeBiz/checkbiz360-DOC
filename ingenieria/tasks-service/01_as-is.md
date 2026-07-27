# 01 — Estado actual (As-Is)

## Dónde vive hoy

El módulo de tareas es parte de `checkinbiz` dentro de Firebase Functions:

```
encodeBiz-SAAS/functions/src/services-saas/checkinbiz/
  firebase-checkinbiz-http/
    tasks.ts                         ← https.onRequest(app)  → export tasksHandler
  interfaces/http/task/
    taskRouter.ts                    ← 14 rutas
    *.controller.ts                  ← 14 controladores
    task.helpers.ts                  ← wiring + resolveTaskActor + matriz can*
  application/use-cases/task/         ← 12 casos de uso
  domain/entities/Task.ts             ← Task + subentidades + tipos
  domain/interfaces/TaskRepository.ts
  infrastructure/repository/FirestoreTaskRepository.ts
```

`tasks.ts` es un Express montado dentro de una Cloud Function:

```typescript
const app = express();
app.use(webCorsMiddleware);
app.use(express.json({limit: "10mb"}));
app.use("/tasks", taskRouter);
export const tasksHandler = https.onRequest({cors: ALLOWED_WEB_ORIGINS, memory: "512MiB", cpu: 1}, app);
```

## Superficie funcional

- **14 endpoints HTTP** (CRUD de tareas, asignaciones, notas, estado, validación, rechazo, recursos, valoraciones, actividad). Detalle en [03_contratos-api.md](./03_contratos-api.md).
- **Auth dual**: Firebase ID token (back office) + staff JWT (app móvil), resuelta en `resolveTaskActor`.
- **Permisos por nivel de responsabilidad**: `worker < supervisor < manager < owner`, gobernados por la matriz `can*` y por `TaskConfig`.
- **Evidencias**: subida de fotos/vídeos a Firebase Storage (multipart).

## Datos

Firestore, bajo la entidad:

```
entities/{entityId}/tasks/{taskId}
  ├── (doc Task)
  ├── assignments/{employeeId}
  ├── notes/{noteId}
  ├── resources/{resourceId}
  ├── ratings/{employeeId}
  ├── validations/{validationId}
  └── activity/{activityId}
```

## Superficie reactiva (que NO se migra)

- **Schedule** de aviso de inicio tardío: barre tareas con `findPendingStartNotifications` (`scheduledStartNotificationAt` vencido y no notificado) y dispara notificación.
- **Triggers** de Firestore sobre las tareas (notificaciones push / side-effects).

Ambos permanecen en Firebase (ver [ADR-002](./adr/ADR-002-solo-http-lo-reactivo-en-firebase.md)).

## Limitaciones del modelo actual

1. **Latencia por cold start.** Cada invocación HTTP puede pagar el arranque en frío de la función, penalizando la app móvil y el back office.
2. **Coste por invocación.** El tráfico de usuario final (listados, cambios de estado, subidas) factura por invocación de Functions.
3. **Acoplamiento de despliegue.** La API de tareas se despliega junto al resto del bundle de Functions; no escala ni se versiona de forma independiente.

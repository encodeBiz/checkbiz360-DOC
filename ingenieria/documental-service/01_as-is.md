# 01 — Estado actual (As-Is)

## Dónde vive hoy

El módulo de gestión documental es parte de `checkinbiz` dentro de Firebase Functions:

```
encodeBiz-SAAS/functions/src/services-saas/checkinbiz/
  firebase-checkinbiz-http/
    documents.ts                     ← https.onRequest(app) → export documentsHandler
                                        (monta /documents Y /reports en el mismo Express)
  interfaces/http/document/
    documentRouter.ts                ← 8 rutas
    *.controller.ts                  ← 8 controladores
    document.helpers.ts              ← wiring + resolveDocumentActor + validaciones MIME/tamaño
  application/use-cases/document/     ← 8 casos de uso
  application/services/document/
    DocumentPermissionService.ts     ← resolveActor + matriz can*
    DocumentStorageService.ts        ← paths por scope + upload privado + signed URL
    documentSearchIndex.ts           ← índice de búsqueda del documento
  application/notifications/
    DocumentNotificationService.ts   ← doc_uploaded / doc_ack_required
  domain/entities/Document.ts         ← ManagedDocument + tipos + acks + actividad
  domain/entities/DocumentErrors.ts   ← catálogo de códigos de error
  domain/interfaces/DocumentRepository.ts
  infrastructure/repository/FirestoreDocumentRepository.ts
core/searchIndex/                     ← subsistema genérico de índice (compartido)
```

`documents.ts` es un Express montado dentro de una Cloud Function:

```typescript
const app = express();
app.use(webCorsMiddleware);
app.use(express.json({limit: "10mb"}));
app.use("/documents", documentRouter);
app.use("/reports", reportRouter);
export const documentsHandler = https.onRequest(
  {cors: false, memory: "1GiB", cpu: 1, concurrency: 10, maxInstances: 10}, app);
```

> Nota: `documentsHandler` monta `/documents` **y** `/reports` en el mismo handler. En `encodebiz-api` `reports` ya es un servicio propio, así que el port de documental solo se lleva `/documents`.

## Superficie funcional

- **8 endpoints HTTP.** Detalle en [03_contratos-api.md](./03_contratos-api.md):
  `GET /` (listar/buscar), `POST /` (crear, multipart), `GET /:id`, `PATCH /:id`,
  `DELETE /:id` (archivar), `GET /:id/download` (signed URL), `POST /:id/ack`, `GET /:id/acks`.
- **Auth: solo Firebase ID token** (`validateToken` → `verifyIdToken`). No hay staff JWT: es superficie de front-admin / usuario autenticado. El actor y su nivel se resuelven en `DocumentPermissionService.resolveActor`.
- **Modelo de permisos por scope + tipo + nivel.** Scopes `entity | branch | employee`; niveles `worker < supervisor < manager < owner`; tipos RRHH-puros (`payroll`, `contract`) restringidos a owner/admin; disciplinarios (`warning`, `attention_call`) reservados a `manager` exacto de la sucursal. Ver [TDR-002](./tdr/TDR-002-resolucion-actor-y-matriz-de-permisos.md).
- **Ficheros privados en Storage** (multipart en el alta; descarga vía URL firmada de vida corta).
- **Índice de búsqueda** en Firestore (colección `searchIndex`, `type: "document"`), mantenido en alta/actualización/archivado.
- **Notificaciones** push + in-app en el alta (`doc_uploaded`) y cuando el documento requiere confirmación de lectura (`doc_ack_required`).

## Datos

Firestore, bajo la entidad:

```
entities/{entityId}/documents/{documentId}
  ├── (doc ManagedDocument)
  ├── acks/{employeeId}         ← confirmaciones de lectura (una por empleado)
  └── activity/{activityId}     ← trail: created / download_requested / acknowledged / updated / archived
searchIndex/{docId}             ← entrada de búsqueda (type: "document"), colección a nivel raíz
```

- El fichero binario se guarda en **Firebase Storage** (privado, `cacheControl: private, no-store`), no en Firestore. Rutas por scope:
  `documents/entities/{entityId}/{entity|branch/{branchId}|employee/{employeeId}}/{documentId}/{ts}-{filename}`.
- `storagePath` nunca sale al cliente: los casos de uso lo eliminan (`Omit<ManagedDocument, "storagePath">`); la descarga se resuelve con una signed URL de **1 minuto** de TTL.

## Superficie reactiva (que NO se migra)

**El módulo documental no tiene triggers de Firestore ni schedules propios.** Toda la reacción a la escritura (índice, notificaciones, actividad) ocurre *dentro* de los casos de uso HTTP, de forma síncrona a la petición. Por tanto no hay superficie reactiva que dejar en Firebase salvo el propio `documentsHandler`, que se retira en el cutover (ver [ADR-002](./adr/ADR-002-solo-http-lo-reactivo-en-firebase.md)).

## Dependencias del módulo (a resolver en el port)

- **Firebase Admin SDK**: Firestore, Storage (upload + signed URL), Auth (`verifyIdToken`).
- **Repos compartidos** `FirestoreBranchRepository` y `FirestoreEmployeeRepository` (con `findById(id, entityId, "token_devices")`) — ya portados en `services/tasks`.
- **`core/searchIndex`** (tokenizer, generador de prefijos, `FirestoreSearchIndexRepository`) — subsistema aún no presente en `encodebiz-api`.
- **Framework de notificaciones**: `CheckbizSentNotificationApp` + `messages` (ya presentes en `services/tasks`, con las plantillas `doc_uploaded`/`doc_ack_required` incluidas) sobre `@encodebiz/shared` (`NotificationService`, `FirestoreAppNotificationsRepository`).

## Limitaciones del modelo actual

1. **Latencia por cold start.** Cada invocación HTTP puede pagar el arranque en frío de la función.
2. **Coste por invocación.** El tráfico de usuario final (listados, subidas, descargas) factura por invocación de Functions.
3. **Acoplamiento de despliegue.** La API documental se despliega junto al resto del bundle de Functions —y encima comparte handler con `reports`—; no escala ni se versiona de forma independiente.
4. **`entity_employees` ack no soportado en V1.** El alta y la actualización bloquean (400) el ack a nivel entidad porque falta un resolvedor de destinatarios paginado. Se conserva tal cual en el port.

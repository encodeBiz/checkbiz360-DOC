# Catálogo de casos de uso — servicio `documents` (prefijo DOC)

> **Verificación (2026-09-11).** Catálogo obtenido por análisis estático del código de los
> servicios, del panel y de la app, cruzado con lo desplegado de verdad en `dev-encodebiz`.
> **Salvo lo que abajo se marque como confirmado, el resto es lectura del código, no
> comprobación contra el entorno.** Los hallazgos de este catálogo que ya se han verificado
> uno a uno están en [hallazgos.md](./hallazgos.md); las sospechas sin verificar se quedan
> como tales y se comprobarán al escribir su prueba. El resultado esperado de cada caso es lo
> que hace el código HOY, no lo que debería hacer.

Análisis estático, 2026-09-11. El resultado esperado es lo que hace el código hoy.

## Abreviaturas de rutas
- `svc/` = `encodebiz-api/services/documents/src/`
- `ctl/` = `svc/interfaces/http/document/`
- `uc/` = `svc/application/use-cases/document/`
- `perm` = `svc/application/services/document/DocumentPermissionService.ts`
- `repo` = `svc/infrastructure/repository/FirestoreDocumentRepository.ts`
- `cf/` = `encodeBiz-SAAS/functions/src/services-saas/checkinbiz/`
- `front/` = `encodebiz-front-saas/src/`
- `app/` = `checkbiz360/lib/`
- `nginx` = `encodebiz-api/nginx/nginx.staging.conf`

## Actores adicionales
- OP_SIN_RESP: empleado de la entidad con `status` activo y ninguna `employee_responsibilities` activa.
- PROP_SIN_FICHA / PROP_CON_FICHA: PROP sin (o con) documento en `entities/{E}/employees` cuyo `uid` sea el suyo. La distinción cambia `ackStatus` y el acuse.
- Nota: aquí los OP_* y EMP_INACTIVO se autentican con **Firebase ID token**, que es lo que manda la app (`app/features/auth/presentation/providers/auth_provider.dart:319-321`; `app/core/constants/app_constants.dart:94`). EMP_JWT aparece solo como actor rechazado.

## Reglas transversales (se aplican a los 8 endpoints)
- **Enrutado.** nginx sirve `location = /api/v1/documents` y `location /api/v1/documents/` hacia `documents:3007`, con `client_max_body_size 12m` y `proxy_read_timeout 120s` (`nginx:18`, `nginx:87-90`, `nginx:124-127`). Express monta el router en `/api/v1/documents` (`svc/app.ts:17`). Las rutas están en `ctl/documentRouter.ts:22-29`.
- **Autenticación.** Todas las rutas usan `Authorization: Bearer <Firebase ID token>`, verificado con `admin.auth().verifyIdToken` sin `checkRevoked` (`encodebiz-api/packages/shared/src/checkbiz/auth/validateToken.ts:8-19`). Tanto la falta de token como un token inválido dan `401 {code:"auth/unauthorized", error:"Unauthorized"}` (`ctl/document.helpers.ts:52-60`).
- **Resolución del actor** (`perm:49-99`):
  - Rol global: se lee `user_entity_roles/{uid}_{entityId}`. Solo los valores literales `"owner"` o `"admin"` activan `isOwnerAdmin`; cualquier otro valor cuenta como ausencia de rol (`perm:62-65`).
  - Empleado: se busca `entities/{E}/employees where uid==uid limit 1`. Se descarta si `status` es `fired`, `inactive` o `pending` (`perm:67-72`). Los estados `vacation`, `sick_leave`, `leave_of_absence`, `paternity_leave` y `maternity_leave` cuentan como activos (lista de estados en `packages/shared/src/checkbiz/entities/Employee.ts:49`).
  - Responsabilidades: se leen las de `active==1` y se guarda el nivel más alto por sucursal (`perm:76-95`). Los niveles son worker 1, supervisor 2, manager 3 y owner 4 (`Employee.ts:77-82`).
  - Actor sin rol global y sin empleado activo: `403 {code:"documents/unauthorized"}`. Si falla la resolución: `401 auth/unauthorized` (`ctl/document.helpers.ts:62-81`).
  - PROP y ADMIN tienen **los mismos permisos**. Solo cambia el `actorRole` que se registra en la actividad (`perm:36`).
- **Alcance del documento** (`scope`): `entity`, `branch` o `employee`. Solo esos tres existen (`svc/domain/entities/Document.ts:1`).
  - Tipos RRHH-puros: `payroll` y `contract` (`Document.ts:31-34`).
  - Tipos disciplinarios: `warning` y `attention_call` (`Document.ts:37-40`).
- **Matriz de lectura `canRead`** (`perm:132-151`):
  - PROP y ADMIN: leen todo.
  - Scope `entity`: lo lee quien tenga nivel ≥4 en alguna sucursal, o cuyo rol en alguna sucursal esté en `visibleToRoles` (`perm:215-224`).
  - Scope `branch`: lo lee quien tenga responsabilidad en esa sucursal y además sea owner operativo o tenga su rol literal en `visibleToRoles`. **No hay jerarquía**: un manager no lee un documento visible solo para `["worker"]` (`perm:203-213`).
  - Scope `employee`: lo lee el propio empleado. Si no es el propio y el tipo es RRHH-puro, nadie más. En los demás tipos se aplica la misma regla que en `branch` (`perm:144-149`).
- **Escritura** (`perm:153-164`): `canUpdate` y `canArchive` coinciden. PROP y ADMIN pueden siempre. Los demás, nunca sobre RRHH-puros ni sobre `entity`; en los otros casos basta nivel ≥ manager en la sucursal del documento, **sin mirar `visibleToRoles`**.
- **Estados del documento**: `active` y `archived` (`Document.ts:19`). La única transición es `active → archived`, que hace `DELETE`. No existe desarchivar. La edición sube `version` (`uc/UpdateDocument.ts:48`).
- **Storage** (`svc/application/services/document/DocumentStorageService.ts`):
  - Ruta: `documents/entities/{E}/{entity|branch/{B}|employee/{X}}/{docId}/{ts}-{nombre saneado}` (`:8-29`).
  - Subida privada con `cacheControl: private, no-store` (`:31-37`).
  - URL firmada de lectura con caducidad de **1 minuto** (`:5`, `:39-50`).
  - El archivado no borra el fichero.
  - El bucket es `FIREBASE_STORAGE_BUCKET` (`packages/shared/src/firebase.ts:7`).
- **Errores fuera de controlador**:
  - Ruta desconocida: `404 {ok:false, error:"not_found"}` (`svc/app.ts:19`).
  - Excepción: `500 {ok:false, error:"internal_error"}` (`svc/app.ts:21-24`). La CF respondía `500 {code:"documents/internal_error", error:"Internal server error"}` (`cf/firebase-checkinbiz-http/documents.ts:18-23`).
- **CORS**: el contenedor usa `cors()` abierto (`svc/app.ts:10`); la CF tenía lista blanca (`cf/firebase-checkinbiz-http/documents.ts:9`). Ningún cliente se ve afectado: el panel pasa por su proxy de servidor y la app es nativa.
- **Proxy del panel**: sin token o con token inválido, el proxy de Next responde `403 {code:"auth/forbidden"}` **antes** de llegar al contenedor (`front/lib/http/serverBackendProxy.ts:570-581`). Añade la barra final a la raíz de colección (`:513-516`) y reenvía status y cuerpo tal cual (`:639-641`). Las pruebas contra nginx ven los 401 del servicio.
- **Paridad con la CF**:
  - `perm`, casos de uso, repositorio, entidades, códigos de error y `DocumentStorageService` son idénticos a los de `cf/` (comprobado con `diff`).
  - El contenedor solo añade los eventos `document.*` en 4 controladores.
  - El parser multipart difiere en la lectura: la CF hacía `busboy.end(req.rawBody)`, el contenedor `req.pipe(busboy)` (`svc/core/shared/utils/parseMultipartFormData.ts:52`).
  - Según `app/core/constants/app_constants.dart:101-105` y `front/../.env.development:114-116`, la CF `documentsHandler` **se retiró de dev-encodebiz**, así que en desarrollo no hay rollback que comparar en vivo.
- **Fuera del catálogo**: `GET /health` del contenedor (`svc/app.ts:15`) no se publica bajo `/api/v1/documents`; el `/health` de nginx es del propio nginx (`nginx:55`).

---

## GET /api/v1/documents  ·  DOC-01
- **Servicio:** documents. Ruta en `ctl/documentRouter.ts:22`; controlador en `ctl/findDocuments.controller.ts:19-60`; caso de uso en `uc/FindDocuments.ts`.
- **Consumidores:**
  - Panel: `NEXT_BACKEND_URI_CHECKINBIZ_DOCUMENTS_HANDLER` (`.env.development:113`) → `/api/proxy/checkinbiz_documents_handler/documents`. Llamada en `front/services/checkinbiz/document.service.ts:71`, usada desde:
    - `front/app/main/[entityId]/checkinbiz/documents/page.controller.tsx:106`: todos los filtros.
    - `.../branch/[id]/detail/components/BranchDocumentsSection.tsx:69-73`: `scope=branch&branchId&status=active&limit=20`.
    - `.../employee/[id]/detail/components/EmployeeDocumentsSection.tsx:122-126`: `scope=employee&employeeId&status=active&limit=20`.
  - App: `AppConstants.documentsCollectionEndpoint` (`app/core/constants/app_constants.dart:99`), llamada en `app/features/documents/data/datasources/document_remote_datasource.dart:60-74`. Envía `entityId`, `limit`, `q`, `branchId`, `createdFrom`, `createdTo`, `type` y `cursor`; **nunca** `scope`, `employeeId` ni `status`. Lee `documents` y `nextCursor`, no `total`.
- **Origen:** portado desde la CF `cf/interfaces/http/document/findDocuments.controller.ts`.
- **Diferencias con la CF:** ninguna visible en el controlador ni en el caso de uso (idénticos). Solo cambia el cuerpo de un 500 no controlado (ver transversal).
- **Autenticación:** Firebase ID token.
- **Autorización:**
  - Actor vinculado a la entidad (`ctl/document.helpers.ts:62-81`).
  - Filtro por fila con `canRead` (`uc/FindDocuments.ts:146`, `:193`, `:271`).
  - Estado efectivo: si no se pide, PROP y ADMIN ven todo y el resto solo `active`. Si se pide `status`, se respeta para cualquier actor (`uc/FindDocuments.ts:173-174`).
- **Entrada (query):**
  - `entityId` (obligatorio). `scope`, `type` y `status` se validan contra catálogo **antes** del token (`ctl/findDocuments.controller.ts:20-38`).
  - `branchId`, `employeeId`, `q`, `cursor`: opcionales.
  - `createdFrom` y `createdTo`: si no son fecha válida, se ignoran en silencio (`:13-17`).
  - `limit`: por defecto 20; el controlador lo recorta a 100 (`:43-44`) y el caso de uso a 50 (`uc/FindDocuments.ts:72`, `:85`).
- **Respuesta correcta:** `200 {ok:true, documents: DocumentWithAckStatus[], nextCursor: string|null, total: number}`.
  - Ningún documento lleva `storagePath`.
  - `branch` es `{id,name}` solo en scope `branch`; en el resto, `null`.
  - `ackStatus` es `null` si el documento no pide acuse (`uc/FindDocuments.ts:39-51`, `:102-116`).
- **Tres flujos:**
  - Con `q`: búsqueda en `searchIndex` con `array-contains` del primer token de 3 o más caracteres, hasta 50 IDs. Sin paginación (`nextCursor:null`) y `total` = número de visibles en la página (`uc/FindDocuments.ts:131-163`; `svc/application/services/document/documentSearchIndex.ts:66-94`).
  - Con `employeeId` y sin `scope`: reparto sobre `entity`, cada sucursal del empleado y `employee`, hasta 500 por consulta. Se ordena en memoria y `total` = visibles (`uc/FindDocuments.ts:216-305`).
  - Resto: Firestore con `orderBy(createdAt desc, __name__ desc)`. Pide `limit*2` y filtra por permiso; `total` sale de un `count()` **sin filtro de permisos** (`uc/FindDocuments.ts:167-209`; `repo:123-152`, `repo:186-197`).
- **Efectos:** ninguno, solo lectura. Lee `acks` por `collectionGroup` si el actor tiene ficha de empleado (`repo:169-184`).
- **Criticidad:** alta. Es la entrada del módulo en panel y app, y filtra por fila documentos de RRHH.
- **Casos:**
  - DOC-01-01 · ANON · `entityId=E` → 401 `auth/unauthorized`
  - DOC-01-02 · TOKEN_INVALIDO · `entityId=E` → 401 `auth/unauthorized`
  - DOC-01-03 · EMP_JWT · `entityId=E` → 401 `auth/unauthorized` (`verifyIdToken` no acepta el JWT de sesión)
  - DOC-01-04 · ANON · sin `entityId` → 400 `documents/bad_request` (la validación precede al token)
  - DOC-01-05 · PROP · `scope=company` → 400 `documents/invalid_scope`
  - DOC-01-06 · PROP · `type=invoice` → 400 `documents/invalid_type`
  - DOC-01-07 · PROP · `status=deleted` → 400 `documents/bad_request`
  - DOC-01-08 · PROP · E con documentos activos y archivados de los 3 scopes, sin filtros → 200. Incluye los archivados; ninguno trae `storagePath`; los de scope `branch` traen `branch:{id,name}` y el resto `branch:null`.
  - DOC-01-09 · ADMIN · misma precondición → 200, mismo conjunto que PROP
  - DOC-01-10 · OP_WORKER (B1) · sin filtros → 200. Solo `active` y solo:
    - `entity` con `"worker"` en `visibleToRoles`;
    - `branch` de B1 con `"worker"`;
    - sus propios `employee`, incluidos `payroll` y `contract`.
    Ninguno de B2.
  - DOC-01-11 · OP_WORKER (B1) · `status=archived` → 200 con los archivados que puede leer
  - DOC-01-12 · OP_OWNER (B1) · sin filtros → 200. Todos los `entity`, todos los `branch` de B1 sin mirar `visibleToRoles` y los `employee` de B1 salvo `payroll`/`contract` ajenos.
  - DOC-01-13 · OP_MANAGER (B1) · documento `branch` de B1 con `visibleToRoles:["worker"]` → no aparece (no hay jerarquía de roles)
  - DOC-01-14 · OP_OTRA_SUCURSAL · E con documentos solo de B1 → 200 sin esos documentos; `total` sí los cuenta
  - DOC-01-15 · AJENO · `entityId=E` → 403 `documents/unauthorized`
  - DOC-01-16 · EMP_INACTIVO (`status=fired`, sin rol de panel) → 403 `documents/unauthorized`
  - DOC-01-17 · EMP_INACTIVO (`status=inactive`, y aparte `pending`) → 403 `documents/unauthorized`
  - DOC-01-18 · EMP_INACTIVO (`status=vacation`, y aparte `sick_leave`) con responsabilidad worker en B1 → 200, igual que DOC-01-10
  - DOC-01-19 · OP_SIN_RESP · → 200. Solo sus documentos `employee` activos; ningún `entity`.
  - DOC-01-20 · OP_WORKER · `q=nomina` → 200 con `nextCursor:null`, `total` = documentos devueltos, solo activos y visibles
  - DOC-01-21 · PROP · `q=ab` (ningún token de 3 o más caracteres) → 200 `{documents:[], nextCursor:null, total:0}`
  - DOC-01-22 · PROP · `q=<título de un documento archivado>&status=archived` → 200 vacío (al archivar se retira del índice)
  - DOC-01-23 · PROP · `employeeId=X`, sin `scope` → 200 con el reparto `entity` + `branch` de las sucursales activas de X + `employee` de X, ordenado `createdAt desc`, y `total` = número de visibles
  - DOC-01-24 · OP_WORKER · `employeeId=<el suyo>`, sin `scope` → 200. Usa sus responsabilidades ya cargadas; no ve documentos de sucursales donde no tiene responsabilidad.
  - DOC-01-25 · PROP · `scope=employee&employeeId=X&status=active` (petición del panel) → 200 solo con los `employee` activos de X
  - DOC-01-26 · PROP · `scope=branch&branchId=B1&status=active` (petición del panel) → 200 solo con los `branch` activos de B1
  - DOC-01-27 · PROP · `limit=100` con más de 60 documentos → 200 con **50** como máximo
  - DOC-01-28 · PROP · `limit=0`, `limit=-5` o `limit=abc` → 200 con 20 como máximo
  - DOC-01-29 · PROP · `limit=2`, siguiendo `nextCursor` hasta `null` → sin duplicados ni saltos, en orden `createdAt desc, id desc`
  - DOC-01-30 · PROP · `cursor=basura` → 200, primera página (el cursor se ignora)
  - DOC-01-31 · PROP · `createdFrom=no-fecha` → 200 sin aplicar el filtro
  - DOC-01-32 · OP_WORKER · los 2×`limit` documentos más recientes de E no son visibles para él → 200 con `documents:[]` y `nextCursor` no nulo
  - DOC-01-33 · PROP · `entityId=E2` (otra entidad, sin rol en ella) → 403 `documents/unauthorized`
  - DOC-01-34 · OP_WORKER · documento con acuse, sin acusar y luego acusado → `ackStatus` pasa de `{required:true, acknowledged:false}` a `{required:true, acknowledged:true, acknowledgedAt, documentVersion}`
  - DOC-01-35 · PROP_SIN_FICHA · documento con acuse → `ackStatus:{required:true, acknowledged:false}` (el detalle DOC-03 devuelve `null` para el mismo documento)
- **Sospechas:**
  - `total` cuenta documentos que el actor no puede ver: `countAll` no aplica `canRead` (`uc/FindDocuments.ts:189`). El panel lo muestra como total (`documents/page.controller.tsx:108`).
  - La paginación puede devolver páginas vacías o cortas con `nextCursor` no nulo (`uc/FindDocuments.ts:196-201`).
  - `limit` se recorta a 50, no a 100: el controlador permite 100 y el caso de uso 50. El contrato dice «1–100» (`DOCS/ingenieria/documental-service/03_contratos-api.md:18`).
  - Cualquier actor puede listar archivados con `status=archived`.
  - `ackStatus` para un actor sin ficha de empleado es `{required:true, acknowledged:false}` aquí y `null` en el detalle, contra el comentario de `Document.ts:84`.
  - El buscador no indexa nombre de sucursal ni de empleado: `indexContext` nunca llega desde el controlador (`ctl/createDocument.controller.ts:174-187`).
  - Las consultas combinadas dependen de índices compuestos. `firestore.indexes.json` de encodeBiz-SAAS declara 12 para `documents` y 1 de grupo para `acks`; si falta uno desplegado, sale 500 `internal_error`. Sin confirmar lo desplegado en dev.

## POST /api/v1/documents  ·  DOC-02
- **Servicio:** documents. Ruta en `ctl/documentRouter.ts:23`; controlador en `ctl/createDocument.controller.ts:37-201`; caso de uso en `uc/CreateDocument.ts`.
- **Consumidores:** panel, con la misma variable que DOC-01. Llamada en `front/services/checkinbiz/document.service.ts:103-110` (fetch multipart al proxy, que lee el cuerpo entero con `arrayBuffer`, `front/lib/http/serverBackendProxy.ts:486`), usada desde:
  - `documents/page.controller.tsx:146-171`: cualquier scope; manda `requiresAcknowledgement:"false"` en `entity` y `metadata` con `externalRef` y `tags`.
  - `BranchDocumentsSection.tsx:87-98`: `scope=branch`, modo `branch_employees`.
  - `EmployeeDocumentsSection.tsx:140-153`: `scope=employee`, modo `single_employee`, `branchId` opcional.
  - App: no la usa.
- **Origen:** portado desde la CF `cf/interfaces/http/document/createDocument.controller.ts`.
- **Diferencias con la CF:**
  - El contenedor emite además `document.created` (`:198`).
  - Parser: `req.pipe(busboy)` frente a `busboy.end(req.rawBody)`.
  - Límite de cuerpo: nginx corta a 12 MB con un 413 HTML (`nginx:125`). En la CF, el límite de petición de Cloud Functions (32 MB, dato de plataforma, no está en el código) dejaba que un fichero de 12 a 32 MB llegara al controlador y recibiera `400 documents/file_too_large`.
  - Si el `Content-Type` no es multipart: 500 `{ok:false, error:"internal_error"}`, frente a `{code:"documents/internal_error"}` en la CF.
- **Autenticación:** Firebase ID token, validado **antes** de leer el multipart (`:39-40`).
- **Autorización:** `canCreate` (`perm:101-130`):
  - PROP y ADMIN: todo.
  - Scope `entity`: nadie más.
  - Scope `branch`: exige `branchId`, tipo no RRHH-puro y nivel ≥ manager en esa sucursal.
  - Scope `employee`: exige `branchId` y tipo no RRHH-puro. Los disciplinarios, solo con nivel **exactamente** manager (3); los demás, nivel ≥ manager.
  - El actor se resuelve **después** de validar campos y fichero (`:137-143`).
- **Entrada** (multipart; orden de validación del controlador):
  1. `entityId`, `scope`, `type` y `title` obligatorios → `bad_request`.
  2. `scope` ∈ catálogo → `invalid_scope`; `type` ∈ catálogo → `invalid_type`.
  3. `branchId` si `scope=branch` → `branch_required`; `employeeId` si `scope=employee` → `employee_required`.
  4. `visibleToRoles`: array JSON no vacío de `worker`, `supervisor` o `manager` → `invalid_visibility_roles`.
  5. `acknowledgementMode` válido → `invalid_acknowledgement_mode`. Prohibido si `requiresAcknowledgement` no es literalmente `"true"`. Con `"true"`: `entity` se rechaza, el modo es obligatorio y debe casar con el scope (`employee → single_employee`, `branch → branch_employees`).
  6. `expiresAt` debe ser una fecha válida → `bad_request`.
  7. `metadata` debe ser JSON válido, sin validar su forma → `bad_request`.
  8. `file` obligatorio → `file_required`; MIME **declarado** en la allow-list (`ctl/document.helpers.ts:18-27`) → `invalid_mime_type`; tamaño ≤ 10 MB → `file_too_large`.
  9. Actor.
  10. `canCreate`.
  11. Existencia de `branchId` → 404 `branch_not_found`; de `employeeId` → 404 `employee_not_found`.
  12. Si el tipo no es RRHH-puro y hay `branchId`, el empleado debe tener responsabilidad activa en esa sucursal → 400 `employee_not_in_branch` (`:150-171`).
  - Referencias: `:45-134`.
  - En `employee`, `branchId` **no** es obligatorio para PROP y ADMIN.
- **Respuesta correcta:** `201 {ok:true, document}`.
  - `document` lleva `id` (UUID), `entityId`, `scope`, `branchId?`, `employeeId?`, `type`, `title`, `description?`, `filename`, `mimeType`, `sizeBytes`, `visibleToRoles`, `status:"active"`, `version:1`, `requiresAcknowledgement`, `acknowledgementMode?`, `uploadedBy` (`employeeId` del actor, o si no su `uid`), `expiresAt?`, `metadata?`, `createdAt` y `updatedAt`.
  - Sin `storagePath`, `ackStatus` ni `branch` (`uc/CreateDocument.ts:94-95`).
- **Efectos:**
  - Storage: sube el fichero con `contentType` = MIME declarado (`uc/CreateDocument.ts:53`).
  - Firestore: `entities/{E}/documents/{id}` (`repo:94-101`).
  - `searchIndex`, doc `entities__{E}__documents__{id}`: fuera de la petición y con los fallos solo registrados (`uc/CreateDocument.ts:81`).
  - Actividad `created` en `.../documents/{id}/activity`, también fuera de la petición.
  - Notificaciones, esperadas con `allSettled` (`:191-196`). Cada una es push FCM más un documento de notificación in-app (`packages/shared/src/checkbiz/notifications/CheckbizOperationals.ts:169-215`):
    - `employee` sin acuse: `doc_uploaded` al empleado.
    - `employee` con acuse: solo `doc_ack_required`.
    - `branch`: `doc_uploaded` a las responsabilidades activas de la sucursal cuyo rol esté en `visibleToRoles` o sea owner. Con acuse, además `doc_ack_required` a los mismos.
    - `entity`: ninguna.
    - En `payroll`, `contract`, `warning` y `attention_call`, el `title` del push va vacío (`svc/application/notifications/DocumentNotificationService.ts:40-75`, `:80-138`).
  - Evento `document.created`, sin ruta ni URL (`svc/events/document.ts:46-48`).
- **Criticidad:** alta. Escribe en Storage y Firestore, notifica a empleados y gobierna quién puede emitir RRHH y documentos disciplinarios.
- **Casos:**
  - DOC-02-01 · ANON · multipart válido → 401 `auth/unauthorized`
  - DOC-02-02 · TOKEN_INVALIDO · multipart válido → 401 `auth/unauthorized`
  - DOC-02-03 · EMP_JWT · multipart válido → 401 `auth/unauthorized`
  - DOC-02-04 · PROP · cuerpo JSON en vez de multipart → 500 `{ok:false, error:"internal_error"}`
  - DOC-02-05 · PROP · sin `title` (repetir sin `entityId`, sin `scope` y sin `type`) → 400 `documents/bad_request`
  - DOC-02-06 · PROP · `scope=company` → 400 `documents/invalid_scope`
  - DOC-02-07 · PROP · `type=invoice` → 400 `documents/invalid_type`
  - DOC-02-08 · PROP · `scope=branch`, sin `branchId` → 400 `documents/branch_required`
  - DOC-02-09 · PROP · `scope=employee`, sin `employeeId` → 400 `documents/employee_required`
  - DOC-02-10 · PROP · `visibleToRoles` ausente o `"[]"` → 400 `documents/invalid_visibility_roles`
  - DOC-02-11 · PROP · `visibleToRoles='["worker","owner"]'` → 400 `documents/invalid_visibility_roles`
  - DOC-02-12 · PROP · `visibleToRoles='worker'` (no es JSON) → 400 `documents/invalid_visibility_roles`
  - DOC-02-13 · PROP · `requiresAcknowledgement=true`, `acknowledgementMode=foo` → 400 `documents/invalid_acknowledgement_mode`
  - DOC-02-14 · PROP · sin `requiresAcknowledgement` (o `"false"`), con `acknowledgementMode` → 400 `documents/invalid_acknowledgement_mode`
  - DOC-02-15 · PROP · `scope=entity`, `requiresAcknowledgement=true`, `acknowledgementMode=entity_employees` → 400 `documents/invalid_acknowledgement_mode` («not supported in V1»)
  - DOC-02-16 · PROP · `scope=employee`, `requiresAcknowledgement=true`, sin modo → 400 `documents/invalid_acknowledgement_mode`
  - DOC-02-17 · PROP · `scope=branch`, `requiresAcknowledgement=true`, `single_employee` → 400 `documents/invalid_acknowledgement_mode`
  - DOC-02-18 · PROP · `requiresAcknowledgement=TRUE` (o `1`), con modo válido → 400 `documents/invalid_acknowledgement_mode` (se interpreta como false, `:52`)
  - DOC-02-19 · PROP · `expiresAt=no-fecha` → 400 `documents/bad_request`
  - DOC-02-20 · PROP · `metadata={malformado` → 400 `documents/bad_request`
  - DOC-02-21 · PROP · sin parte `file` → 400 `documents/file_required`
  - DOC-02-22 · PROP · `file` declarado `text/plain` (repetir con `image/gif`) → 400 `documents/invalid_mime_type`
  - DOC-02-23 · PROP · fichero `.exe` declarado `application/pdf` → 201 (solo se mira el MIME declarado)
  - DOC-02-24 · PROP · PDF de 10 485 761 bytes, cuerpo total menor de 12 MB → 400 `documents/file_too_large`
  - DOC-02-25 · PROP · PDF de exactamente 10 485 760 bytes → 201
  - DOC-02-26 · PROP · cuerpo mayor de 12 MB → 413 de nginx, cuerpo HTML (no JSON)
  - DOC-02-27 · AJENO · payload válido con `entityId=E` → 403 `documents/unauthorized`
  - DOC-02-28 · AJENO · payload sin `title` → 400 `documents/bad_request` (la validación precede al actor)
  - DOC-02-29 · EMP_INACTIVO (`status=fired`) · payload válido → 403 `documents/unauthorized`
  - DOC-02-30 · PROP_SIN_FICHA · `scope=entity`, `type=policy` → 201 con `status:"active"`, `version:1`, `uploadedBy=<uid>` y sin `storagePath`. El fichero queda en `documents/entities/E/entity/<id>/…`; no hay notificación; hay evento `document.created` y actividad `created` con `actorRole:"owner"`.
  - DOC-02-31 · ADMIN · `scope=entity` → 201 con actividad `actorRole:"admin"`
  - DOC-02-32 · PROP_CON_FICHA · `scope=entity` → 201 con `uploadedBy=<employeeId del PROP>`
  - DOC-02-33 · PROP · `scope=branch`, B1, `type=procedure`, `visibleToRoles=["worker"]` → 201. Push `doc_uploaded` y notificación in-app a los worker y owner de B1; los supervisor y manager de B1 no reciben nada.
  - DOC-02-34 · PROP · `scope=branch` con acuse `branch_employees` → 201; los destinatarios reciben `doc_uploaded` **y** `doc_ack_required`
  - DOC-02-35 · PROP · `scope=employee`, X, B1, `certificate`, con acuse `single_employee` → 201; X recibe solo `doc_ack_required`
  - DOC-02-36 · PROP · `scope=employee`, `type=warning` → 201; el push a X lleva `title` vacío
  - DOC-02-37 · PROP · `scope=employee`, `payroll`, X, `branchId=B2` donde X no tiene responsabilidad → 201 (los RRHH-puros saltan `employee_not_in_branch`)
  - DOC-02-38 · PROP · `scope=employee`, `certificate`, sin `branchId` → 201 con documento sin `branchId`
  - DOC-02-39 · PROP · `branchId` inexistente (o de otra entidad) → 404 `documents/branch_not_found`
  - DOC-02-40 · PROP · `employeeId` inexistente (o de otra entidad) → 404 `documents/employee_not_found`
  - DOC-02-41 · PROP · `scope=employee`, `certificate`, X, B1, sin responsabilidad activa de X en B1 → 400 `documents/employee_not_in_branch`
  - DOC-02-42 · OP_MANAGER (B1) · `scope=branch`, B1, `procedure` → 201
  - DOC-02-43 · OP_OWNER (B1) · `scope=branch`, B1, `procedure` → 201
  - DOC-02-44 · OP_SUPERVISOR (B1) · `scope=branch`, B1 → 403 `documents/unauthorized`
  - DOC-02-45 · OP_WORKER (B1) · `scope=employee` sobre sí mismo, B1, `justification` → 403 `documents/unauthorized`
  - DOC-02-46 · OP_MANAGER (B1) · `scope=entity` → 403 `documents/unauthorized`
  - DOC-02-47 · OP_MANAGER (B1) · `scope=branch`, `branchId=B2` → 403 `documents/unauthorized`
  - DOC-02-48 · OP_MANAGER (B1) · `scope=branch`, `type=payroll` → 403 `documents/unauthorized` (no `restricted_document_type`)
  - DOC-02-49 · OP_MANAGER (B1) · `scope=employee`, `type=contract`, X en B1 → 403 `documents/unauthorized`
  - DOC-02-50 · OP_MANAGER (B1) · `scope=employee`, `type=warning`, X en B1 → 201
  - DOC-02-51 · OP_OWNER (B1) · `scope=employee`, `type=warning`, X en B1 → 403 `documents/unauthorized` (solo manager exacto)
  - DOC-02-52 · OP_OWNER (B1) · `scope=employee`, `type=certificate`, X en B1 → 201
  - DOC-02-53 · OP_MANAGER (B1) · `scope=employee`, X, sin `branchId` → 403 `documents/unauthorized`
  - DOC-02-54 · OP_MANAGER (B1) · `scope=employee`, B1, X sin responsabilidad en B1 → 400 `documents/employee_not_in_branch`
  - DOC-02-55 · OP_OTRA_SUCURSAL (manager en B2) · `scope=branch`, B1 → 403 `documents/unauthorized`
  - DOC-02-56 · PROP · `metadata={"tags":"abc"}` → 201, pero una búsqueda `q` por su título no lo encuentra: la indexación lanza en silencio
  - DOC-02-57 · PROP · fichero `Nómina marzo.pdf` → 201; comparar `filename` con el enviado (codificación sin confirmar)
- **Sospechas:**
  - `metadata` no se valida en su forma: con `tags` que no sea un array, `buildIndexFields` lanza (`svc/application/services/document/documentSearchIndex.ts:32`), el error queda en el log y el documento se crea **sin** entrada en el buscador.
  - PROP y ADMIN crean documentos `employee` sin `branchId`. El contrato lo declara obligatorio (`03_contratos-api.md:29`); el código no.
  - El tipo de fichero se decide por el MIME que declara el cliente, no por el contenido.
  - Si falla la escritura en Firestore tras la subida, el fichero queda huérfano en Storage: no hay compensación (`uc/CreateDocument.ts:53-79`).
  - `sendToRoles` no filtra por estado del empleado: notifica a quien tenga responsabilidad `active==1` aunque su ficha esté `fired` (`DocumentNotificationService.ts:129-136`). Sin confirmar si el despido desactiva las responsabilidades.
  - busboy decodifica por defecto los parámetros de `Content-Disposition` como latin1, así que un `filename` UTF-8 podría guardarse corrupto. Sin confirmar la versión de busboy ni el comportamiento real; es igual que en la CF.
  - El panel no sube directo: el cuerpo pasa entero por la ruta `/api/proxy` de Next. Si el hosting del panel limita el cuerpo por debajo de 10 MB, el límite efectivo es menor. Sin confirmar.
  - Un fichero de 12 a 32 MB recibe un 413 HTML de nginx. El proxy lo envuelve como `{message:"<html…>"}` (`serverBackendProxy.ts:470-471`) y `handleServiceError` muestra ese texto en el toast (`document.service.ts:53`).

## GET /api/v1/documents/:documentId  ·  DOC-03
- **Servicio:** documents. Ruta en `ctl/documentRouter.ts:24`; controlador en `ctl/findDocumentById.controller.ts:6-27`; caso de uso en `uc/FindDocumentById.ts`.
- **Consumidores:**
  - Panel: `NEXT_BACKEND_URI_CHECKINBIZ_DOCUMENTS_HANDLER`. Llamada en `front/services/checkinbiz/document.service.ts:88`, usada en `documents/[id]/detail/page.controller.tsx:100`.
  - App: `AppConstants.documentsEndpoint` + `/$id` (`app_constants.dart:96`), llamada en `document_remote_datasource.dart:88-92`. Lee `document` o, si no existe, el propio sobre.
- **Origen:** portado desde la CF `cf/interfaces/http/document/findDocumentById.controller.ts`.
- **Diferencias con la CF:** ninguna visible (idénticos).
- **Autenticación:** Firebase ID token.
- **Autorización:** actor vinculado y `canRead` (`uc/FindDocumentById.ts:21`). **No mira `status`**: un documento archivado se lee igual.
- **Entrada:** `:documentId`; query `entityId` obligatorio, que se valida antes del token (`:10-12`).
- **Respuesta correcta:** `200 {ok:true, document}`.
  - `document` es un `ManagedDocument` sin `storagePath`, más `ackStatus` y `branch`.
  - `ackStatus` es `null` si no pide acuse **o si el actor no tiene ficha de empleado**. Si no, `{required:true, acknowledged, acknowledgedAt?, documentVersion?}` (`:24-30`).
  - `branch` es `{id,name}` solo en scope `branch` y si la sucursal existe; si no, `null` (`:32-36`).
- **Efectos:** ninguno.
- **Criticidad:** alta. Expone metadatos de documentos de RRHH y es la puerta del detalle en panel y app.
- **Casos:**
  - DOC-03-01 · ANON · `entityId=E` → 401 `auth/unauthorized`
  - DOC-03-02 · TOKEN_INVALIDO · `entityId=E` → 401 `auth/unauthorized`
  - DOC-03-03 · ANON · sin `entityId` → 400 `documents/bad_request`
  - DOC-03-04 · PROP · `documentId` inexistente → 404 `documents/not_found`
  - DOC-03-05 · PROP · `documentId` de E2 con `entityId=E` → 404 `documents/not_found`
  - DOC-03-06 · PROP · `documentId` de E2 con `entityId=E2` (sin rol en E2) → 403 `documents/unauthorized`
  - DOC-03-07 · AJENO · documento de E → 403 `documents/unauthorized`
  - DOC-03-08 · EMP_INACTIVO (`status=fired`) · su propio `payroll` → 403 `documents/unauthorized`
  - DOC-03-09 · PROP_SIN_FICHA · documento `branch` de B1 con acuse → 200 con `branch:{id:B1, name}`, `ackStatus:null` y sin `storagePath`
  - DOC-03-10 · ADMIN · `payroll` de X → 200
  - DOC-03-11 · OP_WORKER (X) · su propio `payroll` → 200
  - DOC-03-12 · OP_WORKER (B1) · `payroll` de otro empleado de B1 → 403 `documents/unauthorized`
  - DOC-03-13 · OP_OWNER (B1) · `contract` de un empleado de B1 → 403 `documents/unauthorized`
  - DOC-03-14 · OP_OWNER (B1) · documento `branch` de B1 con `visibleToRoles:["worker"]` → 200
  - DOC-03-15 · OP_MANAGER (B1) · documento `branch` de B1 con `visibleToRoles:["worker"]` → 403 `documents/unauthorized`
  - DOC-03-16 · OP_WORKER (B1) · `warning` de otro empleado de B1 con `branchId=B1` y `visibleToRoles` que incluye `"worker"` → 200
  - DOC-03-17 · OP_OTRA_SUCURSAL · documento `branch` de B1 → 403 `documents/unauthorized`
  - DOC-03-18 · OP_WORKER · documento `entity` con `visibleToRoles:["manager"]` → 403 `documents/unauthorized`
  - DOC-03-19 · OP_OWNER (de cualquier sucursal) · documento `entity` con `visibleToRoles:["manager"]` → 200
  - DOC-03-20 · OP_SIN_RESP · documento `entity` → 403 `documents/unauthorized`; su propio documento `employee` → 200
  - DOC-03-21 · OP_WORKER · documento archivado que podía leer → 200 con `status:"archived"`, `archivedBy`, `archivedAt` y `archiveReason`
  - DOC-03-22 · OP_WORKER · documento con acuse ya acusado → 200 con `ackStatus:{required:true, acknowledged:true, acknowledgedAt, documentVersion}`
  - DOC-03-23 · PROP · documento `employee` con `branchId` → 200 con `branch:null`
  - DOC-03-24 · PROP · documento `branch` cuya sucursal se ha borrado → 200 con `branch:null`
  - DOC-03-25 · EMP_INACTIVO (`status=sick_leave`) · su propio documento → 200
- **Sospechas:**
  - Los documentos archivados siguen siendo legibles por quien podía leerlos. El contrato llama al archivado «soft-delete» (`03_contratos-api.md:49-52`); no está establecido si la lectura posterior es intencionada.
  - Los disciplinarios (`warning`, `attention_call`) no están en `RESTRICTED_DOCUMENT_TYPES`. Los compañeros de sucursal cuyo rol esté en `visibleToRoles` los leen, y el owner operativo siempre (`perm:144-149`, `perm:211`).
  - `ackStatus` difiere del listado para PROP_SIN_FICHA (ver DOC-01-35).

## PATCH /api/v1/documents/:documentId  ·  DOC-04
- **Servicio:** documents. Ruta en `ctl/documentRouter.ts:25`; controlador en `ctl/updateDocument.controller.ts:17-108`; caso de uso en `uc/UpdateDocument.ts`.
- **Consumidores:**
  - Panel: `NEXT_BACKEND_URI_CHECKINBIZ_DOCUMENTS_HANDLER`. Llamada en `front/services/checkinbiz/document.service.ts:134`, usada en `documents/[id]/detail/page.controller.tsx:183-190`. Envía siempre `entityId`, `title`, `visibleToRoles` y `expiresAt: valor || null`, y `description` solo si no está vacía.
  - App: no la usa.
- **Origen:** portado desde la CF `cf/interfaces/http/document/updateDocument.controller.ts`.
- **Diferencias con la CF:** el contenedor emite además `document.updated` con `changed_fields` = claves del cuerpo salvo `entityId` (`:105`). Nada más.
- **Autenticación:** Firebase ID token.
- **Autorización:**
  - Actor vinculado y `canUpdate` = `canArchive` (`perm:153-164`).
  - Si el documento está archivado → `"forbidden"` **antes** de mirar el permiso (`uc/UpdateDocument.ts:44`).
  - Las reglas de acuse se validan en el controlador leyendo el documento **antes** del permiso (`:57-84`).
- **Entrada (JSON):**
  - `entityId` obligatorio.
  - `visibleToRoles`: array no vacío del catálogo.
  - `expiresAt`: fecha o `null`.
  - `requiresAcknowledgement`: boolean.
  - `acknowledgementMode`: del catálogo y coherente con el scope actual; en `entity` se rechaza.
  - `title` y `description`: se convierten con `String(x).trim()`, sin comprobar que no estén vacíos (`:87-88`).
  - `metadata`: se guarda tal cual, sin validar.
- **Respuesta correcta:** `200 {ok:true, document}`, con la misma forma que DOC-03, calculada con el documento fusionado en memoria (`uc/UpdateDocument.ts:66`, `:81-103`).
- **Efectos:**
  - `set(merge)` con `version+1` y `updatedAt`, eliminando antes las claves `undefined` (`repo:103-105`, `repo:41-57`).
  - Reindexa, borrando y creando la entrada, fuera de la petición (`uc/UpdateDocument.ts:68`).
  - Actividad `updated`.
  - Evento `document.updated`.
  - Sin notificaciones. El fichero no cambia.
- **Criticidad:** media. Es edición de metadatos desde el panel; puede cambiar quién ve un documento.
- **Casos:**
  - DOC-04-01 · ANON · cuerpo `{entityId:E, title:"x"}` → 401 `auth/unauthorized`
  - DOC-04-02 · TOKEN_INVALIDO · el mismo cuerpo → 401 `auth/unauthorized`
  - DOC-04-03 · PROP · cuerpo sin `entityId` → 400 `documents/bad_request`
  - DOC-04-04 · PROP · `visibleToRoles:[]` → 400 `documents/invalid_visibility_roles`
  - DOC-04-05 · PROP · `visibleToRoles:["admin"]` → 400 `documents/invalid_visibility_roles`
  - DOC-04-06 · PROP · `expiresAt:"nope"` → 400 `documents/bad_request`
  - DOC-04-07 · PROP · `requiresAcknowledgement:"true"` (cadena) → 400 `documents/bad_request`
  - DOC-04-08 · PROP · `acknowledgementMode:"foo"` → 400 `documents/invalid_acknowledgement_mode`
  - DOC-04-09 · PROP · documento `entity` con `requiresAcknowledgement:true` → 400 `documents/invalid_acknowledgement_mode`
  - DOC-04-10 · PROP · documento `employee` sin modo, con `requiresAcknowledgement:true` y sin `acknowledgementMode` → 400 `documents/invalid_acknowledgement_mode`
  - DOC-04-11 · PROP · documento `branch` con `requiresAcknowledgement:true` y `single_employee` → 400 `documents/invalid_acknowledgement_mode`
  - DOC-04-12 · PROP · documento sin acuse, con `acknowledgementMode:"branch_employees"` y sin `requiresAcknowledgement` → 400 `documents/invalid_acknowledgement_mode`
  - DOC-04-13 · PROP · `documentId` inexistente → 404 `documents/not_found`
  - DOC-04-14 · PROP · `{entityId, title:"Nuevo"}` → 200 con `title` cambiado, `version` subida en 1 y `updatedAt` nuevo; evento con `changed_fields:["title"]`; una búsqueda `q=nuevo` lo encuentra
  - DOC-04-15 · ADMIN · lo mismo → 200
  - DOC-04-16 · PROP · cuerpo con solo `{entityId}` → 200 con `version` subida en 1 y ningún otro cambio
  - DOC-04-17 · PROP · `expiresAt:null` sobre un documento con `expiresAt` → 200 con el `expiresAt` ausente en la respuesta. **Un GET posterior (DOC-03) devuelve el `expiresAt` anterior.**
  - DOC-04-18 · PROP · `title:null` → 200 con `title:"null"`; `title:""` → 200 con `title:""`
  - DOC-04-19 · PROP · documento archivado → 403 `documents/unauthorized`
  - DOC-04-20 · OP_MANAGER (B1) · documento `branch` de B1 (`procedure`) → 200
  - DOC-04-21 · OP_MANAGER (B1) · documento `branch` de B1 con `visibleToRoles:["worker"]`, que no puede leer (DOC-03-15) → 200
  - DOC-04-22 · OP_OWNER (B1) · `warning` `employee` de B1 → 200
  - DOC-04-23 · OP_MANAGER (B1) · `payroll` de un empleado de B1 → 403 `documents/unauthorized`
  - DOC-04-24 · OP_MANAGER (B1) · documento `entity` → 403 `documents/unauthorized`
  - DOC-04-25 · OP_SUPERVISOR (B1) · documento `branch` de B1 → 403 `documents/unauthorized`
  - DOC-04-26 · OP_WORKER (B1) · documento `branch` de B1 → 403 `documents/unauthorized`
  - DOC-04-27 · OP_OTRA_SUCURSAL (manager en B2) · documento de B1 → 403 `documents/unauthorized`
  - DOC-04-28 · AJENO · documento de E → 403 `documents/unauthorized`
  - DOC-04-29 · EMP_INACTIVO (`status=fired`) · antes era manager en B1 → 403 `documents/unauthorized`
  - DOC-04-30 · OP_WORKER · documento `entity` con `requiresAcknowledgement:true` → 400 `documents/invalid_acknowledgement_mode` (no 403)
  - DOC-04-31 · PROP · documento `branch` sin acuse, con `{requiresAcknowledgement:true, acknowledgementMode:"branch_employees"}` → 200 sin push `doc_ack_required`
  - DOC-04-32 · PROP · documento con `single_employee` y `{requiresAcknowledgement:false}` → 200 con `acknowledgementMode` intacto
  - DOC-04-33 · PROP · `metadata:{"tags":"x"}` → 200, y el documento deja de salir en la búsqueda `q`
  - DOC-04-34 · OP_WORKER · tras un PATCH que sube `version`, su acuse previo → `ackStatus.acknowledged:true` con el `documentVersion` antiguo
- **Sospechas:**
  - **`expiresAt:null` no borra la fecha.** `UpdateDocument` la pone en `undefined` (`:60`), `stripUndefined` quita la clave y `set(merge)` conserva el valor (`repo:103-105`), pero la respuesta sale sin él. El panel envía `null` cada vez que el campo está vacío (`detail/page.controller.tsx:188`), así que la ficha muestra la fecha borrada hasta recargar.
  - Un manager u owner operativo edita y archiva documentos que no puede leer ni descargar, porque `canArchive` no mira `visibleToRoles`.
  - La validación de acuse se hace antes del permiso: un actor sin permiso recibe 400 y deduce que el documento existe y es de scope `entity`.
  - `title:null` se guarda como `"null"` y se acepta un título vacío; el alta sí lo exige.
  - Un PATCH sin cambios sube `version`.
  - Activar el acuse por PATCH no notifica, a diferencia del alta.
  - Una `metadata.tags` que no sea array borra la entrada del índice: `reindexDocument` borra primero y lanza después (`documentSearchIndex.ts:51-57`).
  - Subir `version` no invalida los acuses anteriores.
  - `expiresAt` no se aplica en ningún sitio: listado, detalle y descarga lo ignoran.

## DELETE /api/v1/documents/:documentId  ·  DOC-05
- **Servicio:** documents. Ruta en `ctl/documentRouter.ts:26`; controlador en `ctl/archiveDocument.controller.ts:7-41`; caso de uso en `uc/ArchiveDocument.ts`.
- **Consumidores:**
  - Panel: `NEXT_BACKEND_URI_CHECKINBIZ_DOCUMENTS_HANDLER`. Llamada en `front/services/checkinbiz/document.service.ts:223-225`, con `entityId` y `archiveReason` en la query. Se usa en `documents/[id]/detail/page.controller.tsx:152`, `BranchDocumentsSection.tsx:123` y `EmployeeDocumentsSection.tsx:178`.
  - App: no la usa.
- **Origen:** portado desde la CF `cf/interfaces/http/document/archiveDocument.controller.ts`.
- **Diferencias con la CF:** el contenedor emite además `document.archived` (`:33-38`). Nada más.
- **Autenticación:** Firebase ID token.
- **Autorización:** actor vinculado y `canArchive` (`perm:157-164`). El orden es: inexistente → 404; ya archivado → 409; sin permiso → 403 (`uc/ArchiveDocument.ts:20-23`). Por tanto el 409 **precede** al permiso.
- **Entrada:** `:documentId`; query `entityId` obligatorio (se valida antes del token) y `archiveReason` opcional.
- **Respuesta correcta:** `200 {ok:true}`.
- **Efectos:**
  - Firestore `set(merge)` con `status:"archived"`, `archivedBy` (`employeeId` o `uid`), `archivedAt`, `archiveReason?` y `updatedAt`. **No sube `version`** (`uc/ArchiveDocument.ts:26-32`).
  - Borra la entrada de `searchIndex` fuera de la petición (`:34`).
  - Actividad `archived` con `metadata.archiveReason` (`:36-46`).
  - Evento `document.archived`.
  - **No** borra el fichero de Storage ni el documento de Firestore.
- **Criticidad:** media. Es un borrado lógico y reversible solo a mano, que saca el documento del listado de los empleados.
- **Casos:**
  - DOC-05-01 · ANON · `entityId=E` → 401 `auth/unauthorized`
  - DOC-05-02 · TOKEN_INVALIDO · `entityId=E` → 401 `auth/unauthorized`
  - DOC-05-03 · PROP · sin `entityId` → 400 `documents/bad_request`
  - DOC-05-04 · PROP · `documentId` inexistente → 404 `documents/not_found`
  - DOC-05-05 · PROP · documento activo, `archiveReason=Duplicado` → 200 `{ok:true}`. Después:
    - GET DOC-03 muestra `status:"archived"`, `archiveReason:"Duplicado"`, `archivedBy` y la misma `version`;
    - la búsqueda `q` ya no lo devuelve;
    - la URL de descarga (DOC-06) sigue funcionando.
  - DOC-05-06 · ADMIN · documento activo → 200 con actividad `actorRole:"admin"`
  - DOC-05-07 · PROP · documento activo, sin `archiveReason` → 200 sin campo `archiveReason`
  - DOC-05-08 · PROP · documento ya archivado → 409 `documents/already_archived`
  - DOC-05-09 · OP_WORKER (B1) · documento de B1 ya archivado → 409 `documents/already_archived` (no 403)
  - DOC-05-10 · OP_MANAGER (B1) · documento `branch` de B1 → 200
  - DOC-05-11 · OP_MANAGER (B1) · `warning` `employee` de B1 → 200
  - DOC-05-12 · OP_OWNER (B1) · documento `branch` de B1 → 200
  - DOC-05-13 · OP_MANAGER (B1) · documento `branch` de B1 con `visibleToRoles:["worker"]` → 200
  - DOC-05-14 · OP_MANAGER (B1) · `payroll` o `contract` de un empleado de B1 → 403 `documents/unauthorized`
  - DOC-05-15 · OP_MANAGER (B1) · documento `entity` → 403 `documents/unauthorized`
  - DOC-05-16 · OP_SUPERVISOR (B1) · documento `branch` de B1 → 403 `documents/unauthorized`
  - DOC-05-17 · OP_WORKER (X) · su propio `justification` → 403 `documents/unauthorized`
  - DOC-05-18 · OP_OTRA_SUCURSAL (manager en B2) · documento de B1 → 403 `documents/unauthorized`
  - DOC-05-19 · AJENO · documento de E → 403 `documents/unauthorized`
  - DOC-05-20 · EMP_INACTIVO (`status=fired`) · antes era manager en B1 → 403 `documents/unauthorized`
  - DOC-05-21 · OP_WORKER (B1) · tras archivar un documento `branch` visible para él → no aparece en DOC-01 sin `status`, pero sí con `status=archived` y en DOC-03
- **Sospechas:**
  - El 409 se devuelve antes del permiso: un actor sin permiso distingue un documento archivado de uno activo.
  - Archivar no retira acceso de lectura, descarga ni acuse (ver DOC-03, DOC-06 y DOC-07). No está establecido si es intencionado.
  - Un manager archiva documentos que no puede leer (DOC-05-13).

## GET /api/v1/documents/:documentId/download  ·  DOC-06
- **Servicio:** documents. Ruta en `ctl/documentRouter.ts:27`; controlador en `ctl/downloadDocument.controller.ts:6-31`; caso de uso en `uc/GenerateDocumentDownloadUrl.ts`.
- **Consumidores:**
  - Panel: `NEXT_BACKEND_URI_CHECKINBIZ_DOWNLOAD_DOCUMENTS` (`.env.development:120`) → `/api/proxy/checkinbiz_download_documents/documents/:id/download`, solo GET (`serverBackendProxy.ts:359-363`). Llamada en `front/services/checkinbiz/document.service.ts:151-153`, usada en `documents/[id]/detail/page.controller.tsx:139`, `BranchDocumentsSection.tsx:112` y `EmployeeDocumentsSection.tsx:167`.
  - App: `AppConstants.documentsDownloadEndpoint` + `/$id/download` (`app_constants.dart:108`), llamada en `document_remote_datasource.dart:108-113`. Lee `url` (obligatoria) y `expiresAt`.
- **Origen:** portado desde la CF `cf/interfaces/http/document/downloadDocument.controller.ts`.
- **Diferencias con la CF:** ninguna visible (idénticos). La firma la hace ahora la credencial del contenedor en vez de la cuenta de servicio de la CF. Sin confirmar que la credencial del contenedor pueda firmar; si no puede, 500 `internal_error`.
- **Autenticación:** Firebase ID token.
- **Autorización:** actor vinculado y `canRead` (`uc/GenerateDocumentDownloadUrl.ts:28`). No mira `status`.
- **Entrada:** `:documentId`; query `entityId` obligatorio, que se valida antes del token.
- **Respuesta correcta:** `200 {ok:true, url, expiresAt}`.
  - `url` es la URL firmada de lectura de `storagePath` en el bucket por defecto.
  - `expiresAt` es ISO, igual a ahora + 60 s (`DocumentStorageService.ts:5`, `:39-50`).
  - No devuelve `documentId` ni `filename`, aunque el caso de uso los calcula (`:26-30`).
- **Efectos:** actividad `download_requested` con `metadata.filename`, fuera de la petición (`uc/GenerateDocumentDownloadUrl.ts:32-42`).
- **Criticidad:** alta. Entrega el binario (nóminas, contratos); un fallo de permiso aquí filtra el fichero.
- **Casos:**
  - DOC-06-01 · ANON · `entityId=E` → 401 `auth/unauthorized`
  - DOC-06-02 · TOKEN_INVALIDO · `entityId=E` → 401 `auth/unauthorized`
  - DOC-06-03 · EMP_JWT · `entityId=E` → 401 `auth/unauthorized`
  - DOC-06-04 · PROP · sin `entityId` → 400 `documents/bad_request`
  - DOC-06-05 · PROP · `documentId` inexistente → 404 `documents/not_found`
  - DOC-06-06 · PROP · `documentId` de E2 con `entityId=E` → 404 `documents/not_found`
  - DOC-06-07 · PROP · documento propio → 200 `{ok:true, url, expiresAt}` con `expiresAt − ahora ≈ 60 s`. Un GET a `url` antes de 60 s devuelve los bytes subidos con el `Content-Type` del alta.
  - DOC-06-08 · PROP · repetir el GET a `url` pasados más de 60 s → Storage lo rechaza. El código exacto de GCS no está en el código; sin confirmar.
  - DOC-06-09 · ADMIN · `payroll` de X → 200
  - DOC-06-10 · OP_WORKER (X) · su propio `payroll` → 200
  - DOC-06-11 · OP_WORKER (B1) · `payroll` de otro empleado → 403 `documents/unauthorized`
  - DOC-06-12 · OP_OWNER (B1) · `contract` de un empleado de B1 → 403 `documents/unauthorized`
  - DOC-06-13 · OP_MANAGER (B1) · documento `branch` de B1 con `visibleToRoles:["worker"]` → 403 `documents/unauthorized`
  - DOC-06-14 · OP_OWNER (B1) · el mismo documento → 200
  - DOC-06-15 · OP_OTRA_SUCURSAL · documento `branch` de B1 → 403 `documents/unauthorized`
  - DOC-06-16 · AJENO · documento de E → 403 `documents/unauthorized`
  - DOC-06-17 · EMP_INACTIVO (`status=fired`) · su propio `payroll` → 403 `documents/unauthorized`
  - DOC-06-18 · EMP_INACTIVO (`status=vacation`) · su propio `payroll` → 200
  - DOC-06-19 · OP_WORKER · documento archivado que podía leer → 200 con URL válida
  - DOC-06-20 · OP_WORKER · respuesta de DOC-06-10 → el cuerpo tiene exactamente las claves `ok`, `url` y `expiresAt`
  - DOC-06-21 · PROP · tras DOC-06-07 → hay una actividad `download_requested` nueva en `entities/E/documents/{id}/activity`
- **Sospechas:**
  - Los documentos archivados se siguen descargando.
  - Un empleado de baja (`vacation`, `sick_leave`…) mantiene el acceso completo; solo `fired`, `inactive` y `pending` lo pierden. Está en el código; no está establecido si es la política deseada.
  - `verifyIdToken` se llama sin `checkRevoked`: el token de un usuario deshabilitado o revocado sirve hasta que caduca.

## POST /api/v1/documents/:documentId/ack  ·  DOC-07
- **Servicio:** documents. Ruta en `ctl/documentRouter.ts:28`; controlador en `ctl/acknowledgeDocument.controller.ts:7-38`; caso de uso en `uc/AcknowledgeDocument.ts`.
- **Consumidores:**
  - Panel: la función `acknowledgeDocument` existe (`front/services/checkinbiz/document.service.ts:198-212`), pero no se ha detectado ninguna llamada en `front/`.
  - App: `AppConstants.documentsEndpoint` + `/$id/ack` (`app_constants.dart:96`), llamada en `document_remote_datasource.dart:127-131` con cuerpo `{entityId}`.
- **Origen:** portado desde la CF `cf/interfaces/http/document/acknowledgeDocument.controller.ts`.
- **Diferencias con la CF:** el contenedor emite además `document.acknowledged` con id determinista `evt_<md5(entity:doc:employee)[0..24]>`, así que repetir el acuse no publica dos veces (`svc/events/document.ts:85-103`). Nada más.
- **Autenticación:** Firebase ID token.
- **Autorización:**
  - Orden: inexistente → 404; sin acuse requerido → 400; `canAcknowledge` falso → 403 `acknowledgement_not_allowed`; sin `employeeId` → 403 `unauthorized`. Esta última rama es inalcanzable en la práctica (`uc/AcknowledgeDocument.ts:21-25`).
  - `canAcknowledge` exige `canRead` y además, según el modo (`perm:166-181`):
    - `single_employee`: el actor es el empleado del documento;
    - `branch_employees`: el actor tiene responsabilidad activa en la sucursal del documento;
    - `entity_employees`: tiene alguna responsabilidad. Este modo no se puede crear por API.
  - No mira `status`.
- **Entrada:** `:documentId`; `entityId` en el **cuerpo JSON**, no en la query (`:9`).
- **Respuesta correcta:** `200 {ok:true}`, tanto al crear el acuse como al repetirlo.
- **Efectos:**
  - Crea `entities/{E}/documents/{id}/acks/{employeeId}` con `{employeeId, uid, documentId, entityId, acknowledgedAt, documentVersion = version actual}` (`uc/AcknowledgeDocument.ts:31-40`; `repo:155-157`).
  - Actividad `acknowledged` con `metadata.documentVersion`.
  - Evento `document.acknowledged`.
  - Si ya existía un acuse, no escribe nada nuevo y devuelve el existente (`:27-28`).
- **Criticidad:** alta. Es el acuse de recibo con valor legal (comentario en `svc/events/document.ts:77-78`) y lo usa la app.
- **Casos:**
  - DOC-07-01 · ANON · cuerpo `{entityId:E}` → 401 `auth/unauthorized`
  - DOC-07-02 · TOKEN_INVALIDO · cuerpo `{entityId:E}` → 401 `auth/unauthorized`
  - DOC-07-03 · EMP_JWT · cuerpo `{entityId:E}` → 401 `auth/unauthorized`
  - DOC-07-04 · OP_WORKER · cuerpo `{}` → 400 `documents/bad_request`
  - DOC-07-05 · OP_WORKER · `?entityId=E` en la query y cuerpo vacío → 400 `documents/bad_request`
  - DOC-07-06 · OP_WORKER · `documentId` inexistente → 404 `documents/not_found`
  - DOC-07-07 · OP_WORKER (X) · su documento sin acuse → 400 `documents/acknowledgement_not_required`
  - DOC-07-08 · OP_WORKER (X) · documento `employee` de X con `single_employee` → 200 `{ok:true}`. Se crea `acks/X` con `uid`, `documentVersion = version` y `acknowledgedAt`. DOC-03 pasa a mostrar `ackStatus.acknowledged:true`.
  - DOC-07-09 · OP_WORKER (X) · repetir DOC-07-08 → 200 `{ok:true}` con el mismo `acknowledgedAt` y sin actividad nueva
  - DOC-07-10 · OP_WORKER (Y) · documento `single_employee` de X, sin poder leerlo → 403 `documents/acknowledgement_not_allowed`
  - DOC-07-11 · OP_MANAGER (B1) · documento `employee` `single_employee` de X en B1 con `visibleToRoles:["manager"]` (puede leerlo) → 403 `documents/acknowledgement_not_allowed`
  - DOC-07-12 · OP_WORKER (B1) · documento `branch` de B1, `branch_employees`, con `"worker"` en `visibleToRoles` → 200
  - DOC-07-13 · OP_SUPERVISOR (B1) · documento `branch` de B1, `branch_employees`, `visibleToRoles:["worker"]` → 403 `documents/acknowledgement_not_allowed`
  - DOC-07-14 · OP_OWNER (B1) · el mismo documento → 200
  - DOC-07-15 · OP_OTRA_SUCURSAL · documento `branch` de B1 → 403 `documents/acknowledgement_not_allowed`
  - DOC-07-16 · PROP_SIN_FICHA · documento `branch` con acuse → 403 `documents/acknowledgement_not_allowed`
  - DOC-07-17 · PROP_CON_FICHA con responsabilidad en B1 · documento `branch` de B1, `branch_employees`, aunque su rol no esté en `visibleToRoles` → 200
  - DOC-07-18 · AJENO · documento de E → 403 `documents/unauthorized`
  - DOC-07-19 · EMP_INACTIVO (`status=fired`) · su documento `single_employee` → 403 `documents/unauthorized`
  - DOC-07-20 · EMP_INACTIVO (`status=maternity_leave`) · su documento `single_employee` → 200
  - DOC-07-21 · OP_WORKER (X) · documento `single_employee` de X **archivado** → 200 y se crea el acuse
  - DOC-07-22 · OP_WORKER (X) · acuse hecho en la versión 1; PATCH sube a 2; repetir el POST → 200 y el acuse sigue con `documentVersion:1`
- **Sospechas:**
  - Se puede acusar un documento archivado.
  - Tras editar un documento no se puede volver a acusar la versión nueva: el acuse es único por empleado, sin mirar la versión.
  - El PROP con ficha acusa documentos `branch_employees` aunque su rol no esté en `visibleToRoles`, porque `canRead` sale verdadero por `isOwnerAdmin`.
  - La rama `"forbidden"` (`uc/AcknowledgeDocument.ts:25`) es inalcanzable; no genera ningún caso.

## GET /api/v1/documents/:documentId/acks  ·  DOC-08
- **Servicio:** documents. Ruta en `ctl/documentRouter.ts:29`; controlador en `ctl/findDocumentAcks.controller.ts:6-27`; caso de uso en `uc/FindDocumentAcks.ts`.
- **Consumidores:**
  - Panel: `NEXT_BACKEND_URI_CHECKINBIZ_DOCUMENTS_HANDLER`. Llamada en `front/services/checkinbiz/document.service.ts:170-172`, usada en `documents/[id]/detail/page.controller.tsx:83`. El panel acepta `acks`, `acknowledgements` o un array.
  - App: no la usa.
- **Origen:** portado desde la CF `cf/interfaces/http/document/findDocumentAcks.controller.ts`.
- **Diferencias con la CF:** ninguna visible (idénticos).
- **Autenticación:** Firebase ID token.
- **Autorización:** solo `actor.isOwnerAdmin`, comprobado **antes** de ver si el documento existe (`uc/FindDocumentAcks.ts:13-15`).
- **Entrada:** `:documentId`; query `entityId` obligatorio, que se valida antes del token.
- **Respuesta correcta:** `200 {ok:true, acks: [{employeeId, uid, documentId, entityId, acknowledgedAt, documentVersion}], total}`, sin orden explícito (`repo:199-205`).
- **Efectos:** ninguno.
- **Criticidad:** media. Es el registro de acuses que consulta RRHH desde la ficha del documento.
- **Casos:**
  - DOC-08-01 · ANON · `entityId=E` → 401 `auth/unauthorized`
  - DOC-08-02 · TOKEN_INVALIDO · `entityId=E` → 401 `auth/unauthorized`
  - DOC-08-03 · PROP · sin `entityId` → 400 `documents/bad_request`
  - DOC-08-04 · PROP · documento con 2 acuses → 200 con `acks` de 2 elementos, cada uno con las 6 claves, y `total:2`
  - DOC-08-05 · ADMIN · el mismo documento → 200, igual que PROP
  - DOC-08-06 · PROP · documento sin acuses (o sin acuse requerido) → 200 `{ok:true, acks:[], total:0}`
  - DOC-08-07 · PROP · `documentId` inexistente → 404 `documents/not_found`
  - DOC-08-08 · PROP · documento archivado con acuses → 200 con los acuses
  - DOC-08-09 · OP_OWNER (B1) · documento de B1 → 403 `documents/unauthorized`
  - DOC-08-10 · OP_MANAGER (B1) · documento de B1 → 403 `documents/unauthorized`
  - DOC-08-11 · OP_WORKER · `documentId` inexistente → 403 `documents/unauthorized` (no 404)
  - DOC-08-12 · AJENO · documento de E → 403 `documents/unauthorized`
  - DOC-08-13 · EMP_INACTIVO (`status=fired`) → 403 `documents/unauthorized`
- **Sospechas:**
  - El responsable operativo (owner o manager de la sucursal) que emite un documento con acuse no puede consultar quién lo ha acusado. Es coherente con el contrato (`03_contratos-api.md:72`), pero deja a quien crea el documento sin el seguimiento.

## Resumen
- **Endpoints:** 8 (consumidos por clientes: 8).
  - El panel usa 7; el POST de acuse lo tiene definido, pero no se ha detectado ninguna llamada.
  - La app usa 4: listado, detalle, descarga y acuse.
- **Casos:** 228. Por endpoint:

  | Endpoint | Casos |
  |---|---|
  | DOC-01 | 35 |
  | DOC-02 | 57 |
  | DOC-03 | 25 |
  | DOC-04 | 34 |
  | DOC-05 | 21 |
  | DOC-06 | 21 |
  | DOC-07 | 22 |
  | DOC-08 | 13 |

- **Diferencias con Cloud Functions que pueden romper a un cliente:**
  - **Límite de subida.** nginx corta a 12 MB con un 413 **HTML** (`nginx:125`). Con la CF, un fichero de 12 a 32 MB recibía un JSON `400 documents/file_too_large`. En el panel, el proxy envuelve el HTML como `{message}` y el toast lo muestra en crudo.
  - **Cuerpo de los 500 no controlados.** El contenedor responde `{ok:false, error:"internal_error"}` (`svc/app.ts:23`); la CF respondía `{code:"documents/internal_error", error:"Internal server error"}`. El diccionario de errores del panel no puede traducirlo y el usuario ve el literal `internal_error`. Afecta, por ejemplo, a un POST no multipart o a un índice de Firestore que falte.
  - **Ruta desconocida.** El contenedor da un 404 JSON; la CF daba el 404 HTML de Express. Ningún cliente depende de ello.
  - **Sin rollback en dev.** Los comentarios de la app y del panel dicen que `documentsHandler` ya no está desplegada en dev-encodebiz (`app_constants.dart:101-105`; `.env.development:114-116`). No se puede comparar en vivo en desarrollo, contra lo que supone el enunciado.
  - **Sin diferencias funcionales.** `perm`, casos de uso, repositorio, errores y Storage son idénticos (`diff`). Lo único nuevo son los eventos `document.*`.
- **Sospechas principales:**
  1. `PATCH expiresAt:null` responde sin fecha, pero Firestore la conserva (`uc/UpdateDocument.ts:60` + `repo:103-105`). El panel manda `null` en cada guardado con el campo vacío.
  2. Un manager u owner operativo edita y archiva documentos que no puede leer ni descargar, porque `canArchive` ignora `visibleToRoles`.
  3. El `total` del listado cuenta documentos no visibles para el actor, y hay páginas vacías con `nextCursor`.
  4. Los documentos archivados siguen legibles, descargables y acusables. Cualquier actor los lista con `status=archived`. No está establecido si es intencionado.
  5. Los disciplinarios (`warning`, `attention_call`) los leen los compañeros si su rol está en `visibleToRoles`; el owner operativo, siempre.
  6. Solo `fired`, `inactive` y `pending` pierden el acceso. Un empleado de baja o de vacaciones conserva todos los permisos.
  7. Se valida antes de autorizar: el 409 `already_archived` y el 400 de acuse en PATCH delatan el estado o el scope ante actores sin permiso.
  8. `metadata` no se valida: unas `tags` que no sean array dejan el documento fuera del buscador (alta) o lo sacan de él (PATCH), sin error visible.
  9. `limit` se recorta a 50 frente al 100 del contrato. Un actor sin ficha recibe `ackStatus` distinto en el listado y en el detalle.
  10. PROP y ADMIN crean documentos `employee` sin `branchId`; `title:null` se guarda como `"null"`; activar el acuse por PATCH no notifica; `expiresAt` no se aplica en ningún sitio.
  11. El tipo de fichero se decide por el MIME declarado; un fallo tras la subida deja el fichero huérfano en Storage; las notificaciones de sucursal no filtran por el estado del empleado (sin confirmar).


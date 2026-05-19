# Modulo Documentos - Gestion Documental

> Estado: ingenieria aprobada para V1, implementacion en curso en rama `feat/documental-manage`.
> Fuente canonica para backend, backoffice y app movil.

## 1. Auditoria de la documentacion previa

### Hallazgos

**Alta - El modelo estaba correcto pero incompleto.**
La version anterior definia `scope`, `visibleToRoles`, Firestore y Storage, pero no cerraba reglas por tipo documental, permisos de escritura, acuse, auditoria ni codigos de error.

**Alta - `visibleToRoles` no podia ser la unica regla para documentos sensibles.**
Nominas, contratos, amonestaciones y llamadas de atencion requieren una politica adicional por `type`. Un supervisor/manager no debe ganar acceso a cualquier documento individual solo por estar en el mismo `branchId`.

**Media - No estaba cerrada la semantica de `owner` operativo.**
El dominio CheckBiz usa responsabilidades `worker | supervisor | manager | owner`, pero `visibleToRoles` solo expone `worker | supervisor | manager`. La V1 mantiene `owner/admin` global como bypass superior, y trata el `owner` operativo como nivel superior en helpers backend aunque no se exponga como checkbox de frontend.

**Media - Faltaba contrato de acuse.**
La version anterior solo indicaba `requiresAcknowledgement`, sin definir objetivo, modo, versionado ni subcoleccion.

**Media - Faltaba estructura de arquitectura.**
No habia ADRs, TDRs, roadmap, indices ni arquitectura de carpetas.

### Decision de auditoria

La documentacion se mantiene como un unico archivo canonico en `DOCS/modulos/documentos.md`, estructurado con:

- objetivo y alcance,
- dominio,
- permisos,
- flujos,
- API,
- persistencia,
- ADRs,
- TDRs,
- roadmap,
- riesgos y checklist.

---

## 2. Objetivo

Crear un modulo transversal de gestion documental para CheckBiz que permita almacenar, clasificar, listar, descargar, archivar y solicitar acuse de documentos relacionados con operaciones, RRHH y cumplimiento.

Ejemplos:

- nominas,
- contratos,
- amonestaciones,
- llamadas de atencion,
- justificantes,
- certificados,
- protocolos de sucursal/proyecto,
- documentacion PRL,
- politicas internas,
- documentacion operativa de centro o proyecto.

El modulo debe funcionar para backoffice y app movil, siempre con permisos resueltos en backend.

---

## 3. Ambitos

```typescript
type DocumentScope = "entity" | "branch" | "employee";
```

| Scope | Campos requeridos | Uso |
|---|---|---|
| `entity` | `entityId` | Documento global de empresa |
| `branch` | `entityId`, `branchId` | Documento de sucursal/proyecto |
| `employee` | `entityId`, `branchId`, `employeeId` | Documento individual de empleado |

`branchId` en scope `employee` actua como contexto de autorizacion: define en que sucursal se enmarca el documento y contra que responsabilidades se evaluan los permisos de responsables. No es el branch del empleado en general sino el branch del documento. Resuelve la ambiguedad en empleados multi-branch.

`branchId` representa sucursal o proyecto operativo. No existe `projectId`.

---

## 4. Tipos documentales

```typescript
type DocumentType =
  | "payroll"
  | "contract"
  | "warning"
  | "attention_call"
  | "justification"
  | "certificate"
  | "policy"
  | "procedure"
  | "risk_prevention"
  | "branch_protocol"
  | "project_document"
  | "other";
```

### Clasificacion operativa por tipo

| Tipo | Scope habitual | Sensibilidad funcional | Regla base |
|---|---|---|---|
| `payroll` | `employee` | Alta RRHH | Solo owner/admin y empleado afectado |
| `contract` | `employee` | Alta RRHH | Solo owner/admin y empleado afectado |
| `warning` | `employee` | Disciplinaria | Owner/admin; manager del branch; empleado afectado |
| `attention_call` | `employee` | Disciplinaria | Owner/admin; manager del branch; empleado afectado |
| `justification` | `employee` | Media | Owner/admin; empleado; responsables autorizados |
| `certificate` | `employee` | Media | Owner/admin; empleado; responsables autorizados |
| `policy` | `entity` | Interna | Segun `visibleToRoles` |
| `procedure` | `entity`/`branch` | Interna | Segun `visibleToRoles` |
| `risk_prevention` | `branch` | Operativa/legal | Segun `visibleToRoles` y acuse si aplica |
| `branch_protocol` | `branch` | Operativa | Segun `visibleToRoles` |
| `project_document` | `branch` | Operativa | Segun `visibleToRoles` |
| `other` | variable | variable | Segun `scope` + `visibleToRoles` |

La clasificacion anterior no introduce un campo `sensitivity`. Es una regla de negocio derivada de `type`.

---

## 5. Visibilidad

```typescript
type DocumentVisibilityRole = "worker" | "supervisor" | "manager";

visibleToRoles: DocumentVisibilityRole[];
```

**Regla global:** `owner/admin` de entidad tienen acceso total siempre y no necesitan aparecer en `visibleToRoles`.

**Owner operativo:** una responsabilidad CheckBiz `owner` se trata en backend como nivel superior para lectura/gestion operativa del branch, aunque no se expone en `visibleToRoles` de V1.

### Semantica del array

`visibleToRoles` es exacto, no jerarquico.

Ejemplos:

| `visibleToRoles` | Quien ve |
|---|---|
| `["worker", "supervisor", "manager"]` | Todos los empleados/responsables del ambito |
| `["supervisor", "manager"]` | Responsables operativos, no workers |
| `["manager"]` | Managers, owner operativo y owner/admin global |

Si se quiere que manager vea un documento visible para worker, el frontend debe enviar tambien `"manager"`.

### Regla de resolucion por scope

**scope = `entity`:** visible a cualquier empleado activo de la entidad cuyo rol este en `visibleToRoles`, sin importar en que branch trabaja. No se require responsabilidad por branch especifico. Owner/admin siempre acceden.

**scope = `branch`:** visible a empleados con responsabilidad activa en ese `branchId` cuyo rol este en `visibleToRoles`.

**scope = `employee`:** visible al empleado afectado. Responsables con responsabilidad activa en el `branchId` del documento pueden acceder si su rol esta en `visibleToRoles` y el `type` no es RRHH restringido. Los responsables de otros branches del mismo empleado no acceden.

---

## 6. Modelo de dominio

```typescript
interface ManagedDocument {
  id?: string;
  entityId: string;
  scope: "entity" | "branch" | "employee";
  branchId?: string;     // requerido si scope = "branch" o "employee"
  employeeId?: string;   // requerido si scope = "employee"
  type: DocumentType;
  title: string;
  description?: string;
  filename: string;
  mimeType: string;
  sizeBytes: number;
  storagePath: string;
  visibleToRoles: Array<"worker" | "supervisor" | "manager">;
  status: "active" | "archived";
  version: number;       // empieza en 1, incrementa en cada PATCH
  requiresAcknowledgement: boolean;
  acknowledgementMode?: "single_employee" | "branch_employees" | "entity_employees";
  uploadedBy: string;    // actor.employeeId || actor.uid
  archivedBy?: string;
  archivedAt?: Date;
  archiveReason?: string;
  expiresAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  metadata?: DocumentMetadata;
}

interface DocumentMetadata {
  externalRef?: string;  // referencia a id en sistema externo (HRIS, ERP)
  tags?: string[];       // max 10 items, solo strings sin PII
}
```

La URL firmada no forma parte persistente del documento. Se genera bajo demanda en el endpoint de descarga.

Nota V1: aunque el dominio reserva `entity_employees`, el backend no permite crear ni actualizar documentos `scope = "entity"` con `requiresAcknowledgement = true`. El acuse masivo de entidad queda diferido a V2 porque requiere resolucion paginada de destinatarios y notificaciones masivas.

### Acuse

```typescript
interface DocumentAcknowledgement {
  employeeId: string;
  uid: string;
  documentId: string;
  entityId: string;
  acknowledgedAt: Date;
  documentVersion: number; // version del ManagedDocument en el momento del acuse
}
```

### Actividad

```typescript
type DocumentActivityType =
  | "created"
  | "download_requested"
  | "acknowledged"
  | "updated"
  | "archived";

interface DocumentActivity {
  id?: string;
  entityId: string;
  documentId: string;
  actorId: string;
  actorRole: "worker" | "supervisor" | "manager" | "owner" | "admin";
  type: DocumentActivityType;
  createdAt: Date;
  metadata?: Record<string, unknown>;
}
```

---

## 7. Permisos

### Principios

1. Backend es la unica fuente de permisos.
2. Frontend solo adapta la UX.
3. `owner/admin` global de entidad tiene acceso total.
4. El acceso operativo se resuelve con `EmployeeResponsibility`.
5. `visibleToRoles` controla lectura dentro del ambito, pero `type` puede endurecer reglas.
6. Un trabajador no puede leer documentos sensibles de otro empleado.

### Matriz por operacion — V1 cerrada

| Operacion | Owner/Admin | Owner operativo | Manager branch | Supervisor branch | Worker |
|---|:---:|:---:|:---:|:---:|:---:|
| Crear documento `entity` | si | no | no | no | no |
| Crear documento `branch` | si | si | si | no | no |
| Crear documento `employee` no sensible | si | si | si (mismo branch) | no | no |
| Crear documento `employee` disciplinario (`warning`, `attention_call`) | si | no | si (mismo branch) | no | no |
| Crear documento `employee` RRHH puro (`payroll`, `contract`) | si | no | no | no | no |
| Listar/descargar segun scope | si | segun ambito | segun `visibleToRoles` | segun `visibleToRoles` | segun `visibleToRoles` |
| Archivar documento | si | si (mismo branch) | si (mismo branch) | no | no |
| Acusar documento propio | si aplica | si aplica | si aplica | si aplica | si aplica |

Notas V1:
- Supervisor no puede crear documentos. Se habilita en V2 con flag de configuracion.
- Manager puede crear docs disciplinarios (`warning`, `attention_call`) en su branch porque es el emisor habitual de amonestaciones.
- Manager NO puede crear `payroll` ni `contract` — esos son exclusivos de owner/admin.
- "mismo branch" = el `branchId` del documento coincide con un branch activo del actor.

### Regla para documentos de empleado (scope = "employee")

Puede leer el documento quien sea:
- owner/admin global, siempre,
- el empleado afectado (`employeeId` del documento == employeeId del actor),
- un responsable con responsabilidad activa en el `branchId` del documento, cuyo rol este en `visibleToRoles`, siempre que `type` no sea RRHH restringido.

**Resolucion multi-branch:** el `branchId` del documento es el unico que importa para evaluar responsables. Si el empleado trabaja en tres branches, solo los responsables del branch del documento tienen acceso potencial.

Para V1, `payroll` y `contract` quedan restringidos a owner/admin + empleado afectado sin excepcion.

### Regla para documentos de entidad (scope = "entity")

Puede leer el documento quien sea:
- owner/admin global, siempre,
- cualquier empleado activo de la entidad cuyo rol este en `visibleToRoles`, sin importar en que branch trabaja.

El backend verifica que el actor tenga al menos una responsabilidad activa en la entidad (`entityId` coincide, `active == 1`).

---

## 8. Flujos esperados

### Flujo A: Subida de documento

1. Cliente envia `multipart/form-data`.
2. Backend valida auth.
3. Backend valida `entityId`, `scope`, `type`, `title`, `visibleToRoles`.
4. Backend valida campos condicionales:
   - `branchId` si `scope = "branch"`,
   - `branchId` y `employeeId` si `scope = "employee"` (ambos requeridos),
   - `entityId` solo si `scope = "entity"`.
5. Backend valida permisos de escritura.
6. Backend valida MIME y tamano.
7. Backend sube archivo a Storage privado.
8. Backend crea documento en Firestore.
9. Backend registra actividad `created`.
10. Si `requiresAcknowledgement = true`, prepara acuses esperados.
11. Backend dispara notificacion fire-and-forget si aplica.

### Flujo B: Listado

1. Cliente solicita listado con filtros.
2. Backend resuelve actor.
3. Backend consulta documentos candidatos con indices.
4. Backend filtra permiso efectivo.
5. Backend nunca devuelve `storagePath` al cliente.
6. Backend nunca devuelve URL firmada en listados.

### Flujo C: Descarga

1. Cliente solicita descarga por `documentId`.
2. Backend carga documento.
3. Backend valida permiso efectivo.
4. Backend genera URL firmada temporal.
5. Backend registra `download_requested`.
6. Backend devuelve `{url, expiresAt}`.

### Flujo D: Acuse

1. Empleado abre documento visible.
2. Cliente llama endpoint de acuse.
3. Backend valida que el documento requiere acuse.
4. Backend valida que el empleado es sujeto esperado del acuse.
5. Backend escribe/actualiza ack idempotente por `employeeId`.
6. Backend registra actividad `acknowledged`.

### Flujo E: Archivado

1. Actor autorizado solicita archivar.
2. Backend valida permiso.
3. Backend cambia `status` a `archived`.
4. Backend registra `archivedBy`, `archivedAt`, `archiveReason`.
5. Backend registra actividad `archived`.
6. No se borra el archivo fisico en V1.

---

## 9. API HTTP

Cloud Function: `apiV100-firebaseEntryHttp-checkinbiz-documentsHandler`

Router Express interno: `/documents`

| Metodo | Ruta | Descripcion |
|---|---|---|
| `POST` | `/documents` | Subir documento |
| `GET` | `/documents` | Listar documentos visibles |
| `GET` | `/documents/:documentId` | Detalle de documento visible |
| `GET` | `/documents/:documentId/download` | Generar URL firmada |
| `PATCH` | `/documents/:documentId` | Editar metadata permitida |
| `POST` | `/documents/:documentId/ack` | Acusar recibo |
| `DELETE` | `/documents/:documentId` | Archivar |

### POST `/documents`

Content-Type:

```txt
multipart/form-data
```

Campos:

```typescript
{
  entityId: string;
  scope: "entity" | "branch" | "employee";
  branchId?: string;
  employeeId?: string;
  type: DocumentType;
  title: string;
  description?: string;
  visibleToRoles: Array<"worker" | "supervisor" | "manager">;
  requiresAcknowledgement?: boolean; // default false
  acknowledgementMode?: "single_employee" | "branch_employees" | "entity_employees"; // entity_employees reservado para V2
  expiresAt?: string;
  metadata?: string; // JSON serializado de DocumentMetadata
  file: File;
}
```

Respuesta:

```typescript
{
  ok: true;
  document: Omit<ManagedDocument, "storagePath">;
}
```

Restriccion V1: si `scope = "entity"`, el frontend debe enviar `requiresAcknowledgement = false` y no debe enviar `acknowledgementMode`. El backend rechaza acuse de entidad en V1.

### GET `/documents`

Query:

```typescript
{
  entityId: string;
  scope?: "entity" | "branch" | "employee";
  branchId?: string;
  employeeId?: string;
  type?: DocumentType;
  status?: "active" | "archived";
  createdFrom?: string;
  createdTo?: string;
  q?: string;         // busqueda semiblanda via searchIndex
  limit?: number;     // default 20, max 100
  cursor?: string;    // cursor opaco: documentId|createdAt del ultimo item (base64)
}
```

Respuesta:

```typescript
{
  ok: true;
  documents: ManagedDocument[];  // sin storagePath
  nextCursor: string | null;
  total?: number;                // solo si scope + branchId/employeeId permite conteo exacto
}
```

**Estrategia de paginacion segura:** el backend pagina DESPUES de resolver el scope mas estrecho posible via query (scope + branchId o employeeId cuando esten presentes). El filtrado de permisos fino se aplica sobre el resultado ya paginado, con overfetch controlado de hasta `limit * 2` documentos candidatos para compensar. Si el cliente recibe menos items que `limit` con `nextCursor` no nulo, debe solicitar la siguiente pagina. `storagePath` nunca se devuelve en listados.

### GET `/documents/:documentId`

Query:

```typescript
{
  entityId: string;
}
```

Respuesta:

```typescript
{
  ok: true;
  document: Omit<ManagedDocument, "storagePath">;
}
```

### PATCH `/documents/:documentId`

Payload (solo campos editables):

```typescript
{
  entityId: string;
  title?: string;
  description?: string;
  visibleToRoles?: Array<"worker" | "supervisor" | "manager">;
  requiresAcknowledgement?: boolean;
  acknowledgementMode?: "single_employee" | "branch_employees" | "entity_employees";
  expiresAt?: string | null;
  metadata?: DocumentMetadata;
}
```

Restricciones: no se puede editar `scope`, `type`, `employeeId`, `branchId`, `filename`, `mimeType`, `storagePath`. Cada PATCH incrementa `version`.

Respuesta:

```typescript
{
  ok: true;
  document: Omit<ManagedDocument, "storagePath">;
}
```

### DELETE `/documents/:documentId`

Query:

```typescript
{
  entityId: string;
  archiveReason?: string;
}
```

Respuesta:

```typescript
{
  ok: true;
}
```

### Shape de error por status HTTP

| HTTP | Codigo | Cuando |
|---|---|---|
| 400 | `documents/bad_request` | Payload invalido, campo faltante, MIME no permitido |
| 400 | `documents/invalid_scope` | scope desconocido |
| 400 | `documents/branch_required` | scope branch/employee sin branchId |
| 400 | `documents/employee_required` | scope employee sin employeeId |
| 400 | `documents/file_too_large` | archivo supera limite |
| 400 | `documents/invalid_mime_type` | MIME no en allowlist |
| 400 | `documents/file_required` | no se adjunto archivo en POST |
| 400 | `documents/invalid_visibility_roles` | visibleToRoles con valores fuera del enum |
| 400 | `documents/invalid_acknowledgement_mode` | acknowledgementMode incompatible con scope |
| 409 | `documents/already_archived` | intento de archivar un documento ya archivado (conflicto con estado actual) |
| 400 | `documents/acknowledgement_not_required` | ack en doc sin requiresAcknowledgement |
| 401 | `auth/unauthorized` | token invalido o ausente |
| 403 | `documents/unauthorized` | token valido pero sin permisos |
| 403 | `documents/restricted_document_type` | type sensible sin permiso |
| 403 | `documents/acknowledgement_not_allowed` | empleado no es sujeto del acuse |
| 404 | `documents/not_found` | documentId no existe o no es visible para el actor |
| 404 | `documents/employee_not_found` | employeeId no existe en la entidad |
| 404 | `documents/branch_not_found` | branchId no existe en la entidad |

### GET `/documents/:documentId/download`

Query:

```typescript
{
  entityId: string;
}
```

Respuesta:

```typescript
{
  ok: true;
  url: string;
  expiresAt: string;
}
```

### POST `/documents/:documentId/ack`

Payload:

```typescript
{
  entityId: string;
}
```

El backend deriva el `employeeId` desde el actor autenticado. El cliente no debe acusar por otro empleado.

---

## 10. Codigos de error

```typescript
"documents/bad_request"
"documents/unauthorized"
"documents/not_found"
"documents/branch_required"
"documents/employee_required"
"documents/invalid_scope"
"documents/invalid_type"
"documents/invalid_visibility_roles"
"documents/invalid_acknowledgement_mode"
"documents/file_required"
"documents/file_too_large"
"documents/invalid_mime_type"
"documents/employee_not_found"
"documents/branch_not_found"
"documents/restricted_document_type"
"documents/already_archived"
"documents/acknowledgement_not_required"
"documents/acknowledgement_not_allowed"
```

Formato estandar:

```json
{
  "error": "Human readable message",
  "code": "documents/error_code",
  "details": []
}
```

---

## 11. Persistencia

### Firestore

```txt
entities/{entityId}/documents/{documentId}
entities/{entityId}/documents/{documentId}/acks/{employeeId}
entities/{entityId}/documents/{documentId}/activity/{activityId}
```

### Storage

```txt
documents/entities/{entityId}/entity/{documentId}/{timestamp}-{filename}
documents/entities/{entityId}/branch/{branchId}/{documentId}/{timestamp}-{filename}
documents/entities/{entityId}/employee/{employeeId}/{documentId}/{timestamp}-{filename}
```

### SearchIndex

El proyecto ya tiene un indice global:

```txt
searchIndex/{searchIndexId}
```

El modulo documentos V1 reutiliza esa infraestructura en vez de guardar `searchTokens` dentro de cada documento.

Shape conceptual alineado con `core/searchIndex`:

```typescript
interface SearchIndex {
  id?: string;
  keywords: string[];
  keywords_prefix: string[];
  fields: Record<string, string>;
  type: "document";
  index: string;    // /entities/{entityId}/documents/{documentId}
  entityId: string;
  updatedAt: Date;
  metadata?: Record<string, string>;
}
```

`type = "document"` debe añadirse al union existente de `SearchIndex.type` cuando se implemente el modulo.

Campos fuente para construir `fields`:

```typescript
{
  title: string;
  description?: string;
  type: DocumentType;
  filename: string;
  branchName?: string;
  employeeFullName?: string;
  employeeEmail?: string;
  tags?: string; // metadata.tags join(" ")
}
```

La logica existente de `createIndex`:

- normaliza a lowercase,
- elimina tildes,
- elimina simbolos,
- elimina stop words ES,
- genera `keywords`,
- genera `keywords_prefix` desde longitud 3 hasta 20.

El frontend nunca envia `keywords` ni `keywords_prefix`. Solo envia `q`.

### Indices candidatos

| Coleccion | Campos | Uso |
|---|---|---|
| `entities/{entityId}/documents` | `scope ASC`, `status ASC`, `createdAt DESC` | listado por ambito |
| `entities/{entityId}/documents` | `scope ASC`, `branchId ASC`, `status ASC`, `createdAt DESC` | documentos de branch |
| `entities/{entityId}/documents` | `scope ASC`, `employeeId ASC`, `status ASC`, `createdAt DESC` | documentos de empleado |
| `entities/{entityId}/documents` | `type ASC`, `status ASC`, `createdAt DESC` | filtros por tipo |
| `entities/{entityId}/documents` | `status ASC`, `expiresAt ASC` | expiraciones |
| `entities/{entityId}/documents` | `status ASC`, `createdAt DESC` | vista global sin filtro de scope |
| `entities/{entityId}/documents` | `branchId ASC`, `status ASC`, `createdAt DESC` | vista global filtrada por branch |
| `entities/{entityId}/documents` | `employeeId ASC`, `status ASC`, `createdAt DESC` | vista global filtrada por empleado |
| `searchIndex` | `entityId ASC`, `type ASC`, `keywords ARRAY` | busqueda por token exacto |
| `searchIndex` | `entityId ASC`, `type ASC`, `keywords_prefix ARRAY` | busqueda por prefijo |

Los indices definitivos estan declarados en `firestore.indexes.json` (confirmado en `feat/documental-manage`).

**Indices desplegados — coleccion `documents` (COLLECTION scope):**

| Campos | Uso principal |
|---|---|
| `scope ASC · status ASC · createdAt DESC · __name__ DESC` | Listado por scope sin filtro adicional |
| `scope ASC · branchId ASC · status ASC · createdAt DESC · __name__ DESC` | Listado por scope + branch |
| `scope ASC · employeeId ASC · status ASC · createdAt DESC · __name__ DESC` | Listado por scope + empleado |
| `type ASC · status ASC · createdAt DESC · __name__ DESC` | Filtro por tipo documental |
| `status ASC · expiresAt ASC` | Deteccion de documentos expirados |
| `status ASC · createdAt DESC · __name__ DESC` | Vista global sin filtro de scope |
| `branchId ASC · status ASC · createdAt DESC · __name__ DESC` | Vista global filtrada por branch |
| `employeeId ASC · status ASC · createdAt DESC · __name__ DESC` | Vista global filtrada por empleado |
| `scope ASC · createdAt DESC · __name__ DESC` | Cursor sin filtro de status (owner/admin) |
| `branchId ASC · createdAt DESC · __name__ DESC` | Cursor por branch sin filtro de status |
| `employeeId ASC · createdAt DESC · __name__ DESC` | Cursor por empleado sin filtro de status |

**Indices desplegados — coleccion `searchIndex`:**

| Campos | Uso principal |
|---|---|
| `entityId ASC · type ASC · keywords ARRAY-CONTAINS` | Busqueda por token exacto |
| `entityId ASC · type ASC · keywords_prefix ARRAY-CONTAINS` | Busqueda por prefijo (flujo `q`) |

El campo `__name__` en los indices de cursor permite usar `startAfter(createdAt, docId)` de forma estable sin indices adicionales.

---

## 12. Arquitectura backend

Ubicacion propuesta:

```txt
functions/src/services-saas/checkinbiz/
  domain/
    entities/Document.ts
    interfaces/DocumentRepository.ts
  application/
    use-cases/document/
      CreateDocument.ts
      FindDocuments.ts
      FindDocumentById.ts
      UpdateDocument.ts
      SearchDocuments.ts
      GenerateDocumentDownloadUrl.ts
      AcknowledgeDocument.ts
      ArchiveDocument.ts
    services/document/
      DocumentPermissionService.ts
      DocumentStorageService.ts
  infrastructure/
    repository/FirestoreDocumentRepository.ts
  interfaces/
    http/document/
      documentRouter.ts
      createDocument.controller.ts
      findDocuments.controller.ts
      findDocumentById.controller.ts
      updateDocument.controller.ts
      downloadDocument.controller.ts
      acknowledgeDocument.controller.ts
      archiveDocument.controller.ts
  firebase-checkinbiz-http/
    documents.ts
```

El router `/documents` se expone mediante un handler Express propio: `documentsHandler`.

No se monta dentro de `tasksHandler` porque tasks y documents son modulos desacoplados. Documents tiene reglas propias de Storage privado, documentos sensibles, acuses y auditoria.

---

## 13. ADRs

### ADR-001: Modulo transversal dentro de CheckBiz

**Estado:** Aprobado.

**Contexto:** Los documentos pueden pertenecer a entidad, sucursal/proyecto o empleado.

**Decision:** Crear modulo documental transversal bajo CheckBiz, no un modulo exclusivo de empleados.

**Consecuencia:** El dominio debe soportar `scope` y permisos por ambito.

### ADR-002: `branchId` representa sucursal/proyecto

**Estado:** Aprobado.

**Contexto:** El dominio actual ya usa `branchId` como sucursal o proyecto operativo.

**Decision:** No crear `projectId`.

**Consecuencia:** Documentos de proyecto usan `scope = "branch"` y `branchId`.

### ADR-003: Coleccion canonica `entities/{entityId}/documents`

**Estado:** Aprobado.

**Contexto:** Se necesita listar documentos mezclados por entidad, branch y empleado.

**Decision:** Usar una coleccion unica `documents` por entidad.

**Consecuencia:** Queries con filtros requieren indices compuestos.

### ADR-004: Storage privado y URL firmada temporal

**Estado:** Aprobado.

**Contexto:** Los documentos pueden contener datos laborales y personales.

**Decision:** No exponer URLs publicas permanentes. Generar URL firmada al descargar.

**Consecuencia:** Cada descarga pasa por backend y se audita.

### ADR-005: Visibilidad por array exacto de roles

**Estado:** Aprobado.

**Contexto:** Un documento puede ser visible para supervisor y manager, pero no worker.

**Decision:** Usar `visibleToRoles` como array exacto.

**Consecuencia:** El frontend debe enviar todos los roles que deben ver el documento.

### ADR-006: `type` endurece permisos sin crear `sensitivity`

**Estado:** Aprobado.

**Contexto:** `sensitivity` duplicaria visibilidad y complicaria el contrato.

**Decision:** Los tipos sensibles se gobiernan con matriz de reglas por `type`.

**Consecuencia:** `payroll` y `contract` tienen reglas especificas V1.

### ADR-007: `branchId` requerido en scope employee como contexto de autorizacion

**Estado:** Aprobado.

**Contexto:** Un empleado puede tener responsabilidades en multiples branches. Sin `branchId` en el documento, no hay forma cerrada de saber que responsables pueden acceder.

**Decision:** `branchId` es requerido cuando `scope = "employee"`. Representa el branch bajo el cual se emite el documento, no todos los branches del empleado.

**Consecuencia:** Los responsables de otros branches del mismo empleado no tienen acceso al documento. El backend valida presencia de `branchId` en la subida.

### ADR-008: Documents Manage se expone como un unico `documentsHandler` Express

**Estado:** Aprobado.

**Contexto:** El modulo documental es un bounded context distinto de tasks. Tiene multipart upload, Storage privado, URL firmada, acuses, permisos sensibles y auditoria propia.

**Decision:** Exponer Documents Manage como una unica Cloud Function HTTP:

```txt
apiV100-firebaseEntryHttp-checkinbiz-documentsHandler
```

Internamente usa Express y monta las rutas bajo:

```txt
/documents
```

No se implementa como funciones separadas por endpoint y no se monta dentro de `tasksHandler`.

**Consecuencia:** El modulo mantiene un deploy independiente, un solo cold start para sus rutas y configuracion propia de memoria/timeout sin acoplarse al ciclo de tasks.

### ADR-009: scope = "entity" visible a cualquier empleado activo con rol en visibleToRoles

**Estado:** Aprobado.

**Contexto:** Los documentos de entidad (politicas, procedimientos) deben ser accesibles a toda la empresa sin requerir pertenecer a un branch especifico.

**Decision:** Para `scope = "entity"`, el backend verifica que el actor tenga al menos una responsabilidad activa en la entidad y que su rol este en `visibleToRoles`.

**Consecuencia:** No se require branch en la evaluacion de permisos para documentos entity. Un empleado que cambia de branch sigue viendo los documentos entity que le eran visibles.

### ADR-010: Archivado logico en V1

**Estado:** Aprobado.

**Contexto:** Los documentos laborales pueden tener valor historico/legal.

**Decision:** `DELETE` archiva. No hay borrado fisico en V1.

**Consecuencia:** `status` solo permite `active | archived`.

### ADR-011: Busqueda semiblanda con `searchIndex` global

**Estado:** Aprobado.

**Contexto:** Backoffice necesita una entrada global de Gestion Documental con lista infinita y filtros por fecha, sucursal, empleado, tipo y texto. Firestore no ofrece full-text search real, pero el proyecto ya tiene infraestructura `core/searchIndex` con `keywords` y `keywords_prefix`.

**Decision:** Documents V1 reutiliza la coleccion global `searchIndex` para busqueda semiblanda. No se guarda `searchTokens` embebido en `entities/{entityId}/documents/{documentId}` y no se introduce motor externo en V1.

**Consecuencia:** El listado con `q` primero consulta `searchIndex` para obtener paths de documentos candidatos (`index`) y despues carga documentos, aplica filtros y permisos efectivos. La busqueda soporta tokens y prefijos, no ranking avanzado ni fuzzy real.

---

## 14. TDRs

### TDR-001: Validar en controller antes de subir a Storage

La request debe validar `scope`, campos condicionales, `type`, `visibleToRoles`, MIME y tamano antes de cualquier subida.

### TDR-002: `acknowledgementMode` obligatorio si `requiresAcknowledgement = true`

Combinaciones validas:

| Scope | Modo permitido |
|---|---|
| `employee` | `single_employee` |
| `branch` | `branch_employees` |
| `entity` | No soportado en V1 |

`entity_employees` queda reservado para V2. En V1, `scope = "entity"` no puede activar acuse porque no existe todavia resolucion paginada de empleados de entidad ni entrega masiva de notificaciones.

### TDR-003: El acuse se deriva del actor autenticado

El endpoint de acuse no acepta `employeeId` arbitrario para evitar IDOR. El backend resuelve el empleado del token.

### TDR-004: `download_requested` como evento de auditoria

Generar URL firmada no confirma descarga real. Por tanto, el evento correcto es `download_requested`, no `downloaded`.

### TDR-005: `owner/admin` via `canWrite`

El permiso global se evalua primero con `canWrite(uid, entityId)`. Si es true, se concede acceso superior.

### TDR-006: `uploadedBy` se resuelve como `employeeId || uid`

Patrón del proyecto (ver `uploadTaskResource.controller.ts`):

```typescript
uploadedBy: actor.employeeId || actor.uid || "system"
```

`employeeId` tiene preferencia porque es la identidad operativa. Si el actor es owner/admin sin `employeeId` (acceso API directo), se usa `uid`. Nunca se acepta `uploadedBy` del cliente.

### TDR-007: Storage rules para `documents/`

**Estado: implementado en `storage.rules` (`feat/documental-manage`).**

El path `documents/{allPaths=**}` tiene `allow read, write: if false`. Firebase Storage aplica la regla mas especifica que coincide con el path solicitado, por lo que este bloque tiene precedencia sobre el catch-all del resto de modulos.

Mecanismos de acceso legitimo que bypasean las reglas (comportamiento de Firebase por diseno):
- **Admin SDK** (backend): uploads y lecturas en servidores, nunca expuesto al cliente.
- **Signed URLs** (descarga cliente): URL firmada generada por el backend con credenciales de service account, TTL 60 min, expira automaticamente.

El catch-all `allow read, write: if true` sigue activo para otros paths (entorno dev). Antes del deploy de cualquier otro modulo a produccion, debe reemplazarse por reglas explicitas por path y eliminar el catch-all.

### TDR-008: Responsabilidades activas por branch

Para permisos operativos se consulta `employee_responsibilities` con:

```txt
employeeId == actor.employeeId
scope.branchId == document.branchId
active == 1
```

El dominio actual persiste `active` como `0 | 1`; no usar boolean en queries V1.

### TDR-009: MIME allowlist

Allowlist inicial:

```txt
application/pdf
image/jpeg
image/png
image/webp
application/msword
application/vnd.openxmlformats-officedocument.wordprocessingml.document
application/vnd.ms-excel
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

### TDR-010: Tamano maximo configurable

Default V1:

```txt
10 MB
```

Debe vivir como constante de modulo, no numero magico en controller.

### TDR-011: Paginacion segura con filtrado posterior

El backend no usa `offset` ni carga toda la coleccion para paginar. Usa cursor sobre candidatos indexados y aplica overfetch controlado antes de devolver la pagina visible.

Estrategia:

1. Query Firestore por el scope mas estrecho disponible: si hay `branchId` o `employeeId`, incluirlos en la query para reducir candidatos.
2. Si el scope es `entity` (sin branchId/employeeId), la query puede devolver muchos candidatos — usar `limit * 2` como overfetch para compensar el filtrado.
3. Aplicar filtrado de permisos efectivos sobre los candidatos.
4. Devolver hasta `limit` items y calcular `nextCursor`.
5. El cliente debe manejar paginas con menos items que `limit` como comportamiento normal.

Nunca usar `offset` — usar cursor compuesto `documentId|createdAt` codificado en base64 para estabilidad. El frontend lo trata como opaco.

### TDR-012: Fire-and-forget para notificaciones

La creacion de documento no debe fallar si falla FCM. Registrar error, no bloquear flujo principal.

### TDR-013: `searchIndex` de documentos se genera en backend

Al crear o actualizar un documento, backend crea o actualiza su entrada en `searchIndex`.

Reglas:

- `type = "document"`.
- `index = /entities/{entityId}/documents/{documentId}`.
- `entityId` siempre obligatorio.
- `fields` se construye solo con campos permitidos.
- No indexar contenido binario del archivo en V1.
- No indexar metadata arbitraria; solo `metadata.tags`.
- No aceptar keywords generadas desde frontend.

Fuentes V1:

```typescript
title
description
type
filename
branch.name
employee.fullName
employee.email
metadata.tags
```

Para `q`, backend normaliza el texto con la misma logica de `createIndex` y consulta:

```txt
searchIndex
  where entityId == ...
  where type == "document"
  where keywords_prefix array-contains tokenNormalizado
```

Si `q` contiene varios tokens, V1 puede resolver por el primer token significativo y filtrar el resto en memoria sobre `keywords`/`keywords_prefix` de los candidatos. Si se requiere ranking, fuzzy real o busqueda por frases, se evaluara motor externo en V2.

---

## 15. Roadmap

### Fase 1 - Dominio

- Crear tipos `DocumentScope`, `DocumentType`, `DocumentVisibilityRole`.
- Crear entidad `ManagedDocument`.
- Crear interfaces de repositorio.
- Crear codigos de error.

### Fase 2 - Permisos

- Crear `DocumentPermissionService`.
- Resolver actor por token.
- Resolver `owner/admin` via `canWrite`.
- Resolver responsabilidad branch.
- Aplicar matriz por `type`.

### Fase 3 - Persistencia y Storage

- Implementar `FirestoreDocumentRepository`.
- Implementar subida privada.
- Implementar URL firmada.
- Implementar activity y acks.
- Integrar `searchIndex` para create/update/archive.

### Fase 4 - HTTP

- Crear `documentRouter`.
- Crear `firebase-checkinbiz-http/documents.ts`.
- Exponer `apiV100-firebaseEntryHttp-checkinbiz-documentsHandler`.
- Montar `documentRouter` en un Express propio bajo `/documents`.
- Implementar endpoints V1.
- Validar contratos y errores.

### Fase 5 - Notificaciones

- Notificar documento asignado.
- Notificar acuse requerido.
- No bloquear flujo si FCM falla.

### Fase 6 - Frontend/App

- Listado con filtros.
- Detalle.
- Subida con selector de scope.
- Selector `visibleToRoles`.
- Descarga.
- Acuse.
- Archivado.

---

## 16. Riesgos

- Exponer documentos sensibles por mezclar rol global y responsabilidad branch.
- Permitir acuse por otro empleado.
- Persistir URLs firmadas como permanentes.
- Subir archivo antes de validar permisos.
- No declarar indices compuestos.
- No declarar indices de `searchIndex`.
- Borrar fisicamente documentos legales.
- Confundir `projectId` con `branchId`.
- Sobreconceder acceso a documentos de empleado evaluando todos los branches del empleado en vez del branchId del documento.
- Paginar antes de filtrar permisos y devolver paginas vacias al cliente.
- Usar metadata como campo libre y persistir PII inadvertidamente.
- Olvidar incrementar `version` en PATCH, rompiendo la trazabilidad del acuse.
- Indexar PII no necesaria o contenido binario en `searchIndex`.
- Tratar `searchIndex` como motor full-text real en V1.

---

## 17. Checklist de salida

- [ ] No existe `projectId`.
- [ ] `visibleToRoles` es obligatorio y validado.
- [ ] `visibleToRoles` se interpreta como array exacto.
- [ ] `owner/admin` global tiene acceso superior.
- [ ] `owner` operativo se trata como nivel superior en backend.
- [ ] `payroll` y `contract` estan restringidos en V1.
- [ ] Acuse deriva empleado desde token.
- [ ] No se persiste URL firmada.
- [ ] Descarga registra `download_requested`.
- [ ] `DELETE` archiva, no borra fisicamente.
- [ ] Indices en `firestore.indexes.json`.
- [ ] `SearchIndex.type` soporta `"document"`.
- [ ] `searchIndex` se crea/actualiza desde backend, nunca desde frontend.
- [ ] `q` consulta `searchIndex` y luego aplica permisos efectivos sobre documentos.
- [ ] `branchId` requerido cuando `scope = "employee"`.
- [ ] Permisos de responsables de employee docs se evaluan contra `branchId` del documento, no contra todos los branches del empleado.
- [ ] scope `entity` verifica responsabilidad activa en entidad, no en branch especifico.
- [ ] Supervisor no puede crear documentos en V1.
- [ ] `version` se inicializa en 1 e incrementa en cada PATCH.
- [ ] `metadata` solo acepta `externalRef` y `tags` (max 10 items).
- [ ] Paginacion usa cursor, no offset.
- [ ] `storagePath` nunca se devuelve en listados.
- [ ] Storage rules bloqueadas antes de deploy a produccion.
- [ ] Tests unitarios para permisos.
- [ ] Tests de integracion para repository y endpoints criticos.

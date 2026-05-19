# UX/UI - Documents Manage

> Documento orientado a UX/UI para disenar las pantallas, flujos y estados del modulo Gestion Documental.
> Fuente funcional: `DOCS/modulos/documentos.md`.

## 1. Objetivo De Producto

Gestion Documental permite consultar, subir, descargar, editar metadata, archivar y acusar recibo de documentos de CheckBiz.

El modulo no es exclusivo de empleados. Debe cubrir documentos de:

- entidad,
- sucursal/proyecto,
- empleado.

El backoffice tendra una entrada principal en menu: **Gestion Documental**. Desde ahi se podra llegar a todos los niveles mediante filtros. En los detalles de entidad, sucursal/proyecto y empleado tambien debe existir una seccion documental contextual.

---

## 2. Principios UX

1. El frontend no decide permisos reales. Muestra acciones segun el usuario, pero el backend siempre valida.
2. Nunca mostrar ni guardar `storagePath`.
3. La descarga siempre se solicita al backend. No hay URL persistente.
4. El filtro `visibleToRoles` es exacto, no jerarquico.
5. `owner/admin` global siempre tiene acceso superior y no necesita aparecer en visibilidad.
6. Documentos sensibles deben mostrarse con tratamiento visual discreto.
7. El acuse es una accion formal. Debe quedar claro que confirma recepcion de una version concreta del documento.

---

## 3. Roles Y Visibilidad Para UI

### Roles seleccionables en UI

```txt
worker
supervisor
manager
```

No mostrar `owner` ni `admin` como checks de visibilidad. Son permisos superiores resueltos en backend.

### Comportamiento del selector `visibleToRoles`

Debe ser un multi-select/checklist obligatorio.

Ejemplos:

| Seleccion | Resultado |
|---|---|
| Worker + Supervisor + Manager | todos los roles operativos del ambito |
| Supervisor + Manager | responsables, no workers |
| Manager | solo managers, owner operativo y owner/admin global |

Importante: si se quiere que manager vea un documento visible para worker, hay que seleccionar tambien manager.

---

## 4. Niveles Del Modulo

### Entidad

Uso:

- politicas internas,
- procedimientos generales,
- comunicaciones de empresa.

UI:

- Acceso principal desde menu: `Gestion Documental`.
- Filtro `scope = entity`.
- No requiere sucursal ni empleado.

### Sucursal / Proyecto

Uso:

- protocolos,
- PRL,
- documentacion operativa,
- documentos de proyecto.

UI:

- Seccion documental dentro del detalle de sucursal/proyecto.
- Tambien accesible desde Gestion Documental filtrando por sucursal.
- Requiere `branchId`.

### Empleado

Uso:

- nominas,
- contratos,
- amonestaciones,
- llamadas de atencion,
- justificantes,
- certificados.

UI:

- Seccion documental dentro del detalle de empleado.
- Tambien accesible desde Gestion Documental filtrando por empleado.
- Requiere `employeeId` y `branchId`.
- El `branchId` representa el contexto bajo el que se emite el documento.

---

## 5. Pantallas Esperadas

### 5.1 Gestion Documental - Backoffice

Entrada principal del modulo.

Contenido:

- listado infinito de documentos visibles,
- buscador textual,
- filtros,
- accion de subir documento,
- acceso a detalle,
- accion de descargar,
- accion de archivar si aplica.

Filtros:

```txt
Texto q
Rango de fechas createdFrom / createdTo
Scope: entity / branch / employee
Sucursal / proyecto
Empleado
Tipo documental
Estado: active / archived
```

Notas:

- Por defecto listar activos.
- Solo owner/admin deberia tener UX para ver archivados o todos.
- La busqueda `q` es semiblanda mediante `searchIndex`.
- Si hay `nextCursor`, mostrar carga incremental.

### 5.2 Documentos En Detalle De Entidad

Vista contextual.

Filtros preaplicados:

```txt
entityId
scope = entity
```

Acciones:

- ver detalle,
- descargar,
- subir documento de entidad si tiene permiso,
- archivar si tiene permiso.

### 5.3 Documentos En Detalle De Sucursal / Proyecto

Vista contextual.

Filtros preaplicados:

```txt
entityId
branchId
scope = branch
```

Acciones:

- ver detalle,
- descargar,
- subir documento de sucursal si tiene permiso,
- archivar si tiene permiso.

### 5.4 Documentos En Detalle De Empleado

Vista contextual.

Filtros preaplicados:

```txt
entityId
employeeId
scope = employee
```

La UI debe pedir o inferir `branchId` si el empleado pertenece a varias sucursales/proyectos.

Acciones:

- ver detalle,
- descargar,
- subir documento de empleado si tiene permiso,
- archivar si tiene permiso,
- mostrar estado de acuse si aplica.

### 5.5 App Movil - Documentos Del Trabajador

Objetivo:

- ver documentos propios,
- descargar,
- acusar recibo cuando aplique.

No debe mostrar:

- documentos de otros empleados,
- selector de visibilidad,
- acciones administrativas,
- `storagePath`.

---

## 6. Flujo De Listado

1. Usuario entra en Gestion Documental.
2. Front llama:

```txt
GET /documents?entityId=...
```

3. Backend devuelve documentos visibles sin `storagePath`.
4. UI renderiza tarjetas/filas.
5. Si `nextCursor` existe, cargar siguiente pagina al hacer scroll o al pulsar cargar mas.

Respuesta esperada:

```typescript
{
  ok: true;
  documents: ManagedDocument[];
  nextCursor: string | null;
}
```

Campos utiles para UI:

- `title`,
- `type`,
- `scope`,
- `branchId`,
- `employeeId`,
- `filename`,
- `mimeType`,
- `sizeBytes`,
- `visibleToRoles`,
- `requiresAcknowledgement`,
- `acknowledgementMode`,
- `status`,
- `version`,
- `expiresAt`,
- `createdAt`,
- `updatedAt`.

---

## 7. Flujo De Busqueda Y Filtros

### Busqueda textual

Campo UI: buscador.

Query:

```txt
q=<texto>
```

Busca sobre:

- titulo,
- descripcion,
- tipo,
- filename,
- nombre de sucursal si backend lo indexa,
- nombre/email empleado si backend lo indexa,
- tags.

UX:

- usar debounce.
- mantener filtros activos visibles.
- mostrar estado vacio si no hay resultados.

### Filtros importantes

| Filtro | Campo API | UI |
|---|---|---|
| Fecha desde | `createdFrom` | date picker |
| Fecha hasta | `createdTo` | date picker |
| Sucursal | `branchId` | selector |
| Empleado | `employeeId` | selector con busqueda |
| Tipo | `type` | select |
| Estado | `status` | tabs o select |
| Ambito | `scope` | segmented control |

---

## 8. Flujo De Subida

### Entrada

Accion: `Subir documento`.

Puede abrir modal o pantalla lateral.

### Campos

Obligatorios:

```txt
entityId
scope
type
title
visibleToRoles
file
```

Condicionales:

```txt
branchId requerido si scope = branch o employee
employeeId requerido si scope = employee
acknowledgementMode requerido si requiresAcknowledgement = true
```

Opcionales:

```txt
description
expiresAt
metadata.externalRef
metadata.tags
```

### Reglas De UI

Al seleccionar `scope`:

- `entity`: ocultar sucursal y empleado.
- `branch`: mostrar sucursal, ocultar empleado.
- `employee`: mostrar sucursal y empleado.

Al activar acuse:

| Scope | acknowledgementMode |
|---|---|
| employee | `single_employee` |
| branch | `branch_employees` |
| entity | No soportado en V1 |

La UI puede autoseleccionar el modo correcto y no mostrarlo como selector si no aporta decision al usuario.

Restriccion V1: si `scope = entity`, la UI debe desactivar la opcion de acuse. No enviar `requiresAcknowledgement = true` ni `acknowledgementMode` para documentos de entidad. `entity_employees` queda reservado para V2.

### Archivo

MIME permitidos:

```txt
pdf
jpg
png
webp
doc
docx
xls
xlsx
```

Tamano maximo:

```txt
10 MB
```

### Request

```txt
POST /documents
Content-Type: multipart/form-data
```

Respuesta:

```typescript
{
  ok: true;
  document: Omit<ManagedDocument, "storagePath">;
}
```

### Estados UI

- loading al subir,
- error de validacion por campo,
- error de permisos,
- subida completada,
- documento agregado al listado.

---

## 9. Flujo De Detalle

1. Usuario pulsa un documento.
2. Front llama:

```txt
GET /documents/:documentId?entityId=...
```

3. Backend devuelve:

```typescript
{
  ok: true;
  document: Omit<ManagedDocument, "storagePath">;
}
```

Secciones recomendadas:

- resumen,
- archivo,
- clasificacion,
- visibilidad,
- acuse,
- fechas,
- acciones.

No mostrar `storagePath`.

---

## 10. Flujo De Descarga

1. Usuario pulsa descargar.
2. Front llama:

```txt
GET /documents/:documentId/download?entityId=...
```

3. Backend responde:

```typescript
{
  ok: true;
  url: string;
  expiresAt: string;
}
```

4. Front abre la URL o inicia descarga.

Notas UX:

- La URL expira.
- Si falla por expiracion, pedir una nueva.
- No guardar URL firmada en estado persistente.

---

## 11. Flujo De Acuse

### Cuando Mostrarlo

Mostrar CTA de acuse si:

- `requiresAcknowledgement = true`,
- el documento es visible para el usuario,
- el usuario es sujeto del acuse.

La validacion definitiva la hace backend.

### Accion

```txt
POST /documents/:documentId/ack
```

Payload:

```typescript
{
  entityId: string;
}
```

Respuesta:

```typescript
{
  ok: true;
}
```

### Copy Recomendado

Usar un texto formal:

```txt
Confirmo que he recibido y revisado este documento.
```

### Estados

- pendiente de acuse,
- acuse registrado,
- no requiere acuse,
- no autorizado.

El acuse se vincula a la version del documento en el momento de confirmar.

---

## 12. Flujo De Edicion

Accion disponible para usuarios con permiso.

Endpoint:

```txt
PATCH /documents/:documentId
```

Campos editables:

- `title`,
- `description`,
- `visibleToRoles`,
- `requiresAcknowledgement`,
- `acknowledgementMode`,
- `expiresAt`,
- `metadata`.

Campos no editables:

- `scope`,
- `type`,
- `branchId`,
- `employeeId`,
- `filename`,
- `mimeType`,
- `storagePath`.

Cada edicion incrementa `version`.

UX:

- avisar si cambiar acuse/visibilidad puede afectar quien ve o debe aceptar el documento.
- refrescar detalle al guardar.

---

## 13. Flujo De Archivado

Accion:

```txt
DELETE /documents/:documentId?entityId=...&archiveReason=...
```

Respuesta:

```typescript
{
  ok: true;
}
```

UX:

- usar confirmacion antes de archivar.
- pedir motivo opcional.
- no presentar como borrado fisico.
- mover a estado `archived`.
- ocultar de listados activos.

Texto recomendado:

```txt
Archivar este documento lo ocultara de los listados activos, pero se mantendra para trazabilidad.
```

---

## 14. Tipos Documentales Para UI

| Valor | Label sugerido |
|---|---|
| `payroll` | Nomina |
| `contract` | Contrato |
| `warning` | Amonestacion |
| `attention_call` | Llamada de atencion |
| `justification` | Justificante |
| `certificate` | Certificado |
| `policy` | Politica interna |
| `procedure` | Procedimiento |
| `risk_prevention` | Prevencion de riesgos |
| `branch_protocol` | Protocolo de sucursal/proyecto |
| `project_document` | Documento de proyecto |
| `other` | Otro |

---

## 15. Estados Visuales

### Estado Del Documento

| Estado | UI |
|---|---|
| `active` | visible en listados normales |
| `archived` | marcado como archivado; solo en filtro de archivados |

### Estado De Acuse

| Estado UX | Condicion |
|---|---|
| No requiere acuse | `requiresAcknowledgement = false` |
| Pendiente | requiere acuse y el usuario aun no ha confirmado |
| Confirmado | el usuario ya acuso recibo |
| No permitido | backend devuelve `documents/acknowledgement_not_allowed` |

---

## 16. Errores UX

| Codigo | Tratamiento UX |
|---|---|
| `auth/unauthorized` | pedir iniciar sesion |
| `documents/unauthorized` | mostrar sin permisos |
| `documents/not_found` | documento no encontrado o no visible |
| `documents/file_required` | pedir archivo |
| `documents/file_too_large` | indicar maximo 10 MB |
| `documents/invalid_mime_type` | indicar formatos permitidos |
| `documents/invalid_visibility_roles` | revisar visibilidad |
| `documents/invalid_acknowledgement_mode` | revisar configuracion de acuse |
| `documents/branch_not_found` | sucursal no valida |
| `documents/employee_not_found` | empleado no valido |
| `documents/already_archived` | ya estaba archivado |
| `documents/acknowledgement_not_required` | ocultar accion de acuse |
| `documents/acknowledgement_not_allowed` | usuario no puede acusar este documento |

---

## 17. Notificaciones

V1 puede notificar:

- documento disponible,
- documento que requiere acuse.

UX:

- al abrir desde push, navegar a `document_detail`.
- usar `documentId` y `entityId` del payload.
- si backend devuelve 403/404 al abrir, mostrar mensaje neutro: documento no disponible.

Notas de seguridad:

- No confiar en que recibir una notificacion implique permiso.
- El detalle siempre debe cargar desde backend.
- Para documentos sensibles, evitar mostrar contenido sensible en previews del cliente.

---

## 18. Pendientes / Decisiones Para UX

1. Busqueda `q` puede estar limitada en V1 si backend no pagina resultados de searchIndex.
2. Si el empleado pertenece a varias sucursales, UX debe pedir branch de contexto para documentos de empleado.
3. `entity_employees` queda diferido a V2; en V1 la UI no debe permitir acuse para documentos de entidad.
4. El estado exacto de acuse por documento puede requerir un endpoint adicional si se quiere mostrar "confirmado" sin intentar acusar.
5. Para documentos sensibles, conviene usar labels genericos en notificaciones y cards compactas.

---

## 19. Checklist UX/UI

- [ ] Gestion Documental aparece en menu principal de backoffice.
- [ ] Detalle de entidad muestra documentos `scope=entity`.
- [ ] Detalle de sucursal/proyecto muestra documentos por `branchId`.
- [ ] Detalle de empleado muestra documentos por `employeeId` y branch de contexto.
- [ ] Listado principal soporta filtros de fecha, sucursal, empleado, tipo, estado y texto.
- [ ] Formulario de subida cambia campos segun `scope`.
- [ ] `visibleToRoles` es obligatorio y exacto.
- [ ] No se muestra `storagePath`.
- [ ] Descarga usa URL firmada bajo demanda.
- [ ] Acuse tiene confirmacion explicita.
- [ ] Archivado no se presenta como borrado fisico.
- [ ] Errores backend se traducen a mensajes de campo o estado.
- [ ] Push abre detalle y revalida permisos.

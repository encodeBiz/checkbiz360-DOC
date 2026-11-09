# TDR-003 — Documentos del cliente: `scope: "customer"` en el documental

**Fecha:** 2026-11-04
**Estado:** API en `develop` (7bba626) y `staging` (8cb6a59), desplegada a mano en el VPS de dev con `[skip ci]` (`documents` y `customers`); panel en `encodebiz-front-saas` `feat/cartera-de-clientes` (367b866e), sin push. **Probado contra staging.** Pendiente publicar el panel y la app.
**Componente:** `services/documents`, `services/customers`; panel (documentos, clientes, tareas)
**Estudio previo:** [08](../08_documentos-del-cliente.md). Decisiones D12–D16 cerradas con la recomendación del estudio (Jose, 2026-11-03: «ya implementa esta fase»).

---

## 1. Qué se ha hecho

### El documental (`documents`)

- `DocumentScope` gana `customer`; `ManagedDocument` gana `customerId` (obligatorio con ese
  ámbito) y `customerBranchIds`, **transitorio**: las sucursales del cliente, cargadas al leer el
  documento (`findById`, `findByIds`, `findAll`) con una consulta por cliente distinto, para
  que los permisos se decidan sin otra lectura. Nunca se guarda; `create` y `update` lo quitan.
- Tipos nuevos: `customer_record` (la ficha), `customer_contract` (el contrato; su fin es
  `expiresAt`), `customer_quote` (presupuesto o tarifa enviada). `contract` sigue siendo el
  laboral, RRHH puro, y no se reutiliza (D12).
- **Permisos** (D13, D14), copiando la regla de sucursal sobre las sucursales del cliente:
  - subir, editar, archivar: owner/admin, o manager o superior en alguna sucursal del cliente;
  - ver: owner/admin, o el rol del actor está en `visibleToRoles` en alguna sucursal del cliente
    (`roleVisibleInBranch` por cada una; el owner operativo de la sucursal siempre).
  - Tipos RRHH y disciplinarios, nunca en este ámbito.
- El alta comprueba que el cliente existe y está activo (`documents/customer_not_found`, 404);
  sin `customerId`, 400; con acuse de recibo, 400: lo que firma el cliente final es el portal.
- Ruta de Storage `documents/entities/{e}/customer/{customerId}/{docId}/…` (la empresa en la
  ruta; el contador de almacenamiento lo cuenta solo).
- `GET /?scope=customer&customerId=` lista; el fan-out «todo lo del empleado» no incluye los
  documentos de cliente. Índice compuesto `documents (customerId ASC, createdAt DESC)` creado en
  dev con gcloud; el de prod va en el pase (§33.7).
- Notificaciones: ninguna (D15). El servicio de notificaciones solo actúa en `employee` y
  `branch`, así que no hubo que tocarlo.

### `customers`

- `GET /for-task/:taskId` rellena `documents`: los activos del cliente; a la persona de campo,
  solo los que llevan `worker`; a quien gestiona, todos. Sin `storagePath`: la descarga pasa por
  `documents/:id/download`, que aplica sus permisos.
- `GET /:customerId` cuenta `contractsExpiring`: `customer_contract` activos con `expiresAt` en
  30 días o ya pasado (D16).

### El panel (`feat/cartera-de-clientes`, 367b866e)

- Gestión documental: ámbito «Cliente» en el filtro y en la subida (buscador por el índice),
  tipos propios, sin acuse; en el detalle del documento, el nombre del cliente.
- Ficha del cliente: bloque **Documentos** (`CustomerDocumentsSection`, copia del de sucursal
  con el ámbito cambiado): subir con tipo, visibilidad y vencimiento; lista con quién lo ve y el
  contrato **en rojo** cuando vence en 30 días o ya venció; descargar; archivar. La cabecera
  avisa de cuántos contratos vencen.
- Detalle de la tarea con cliente: el mismo bloque, solo lectura.

## 2. Lo que se probó (2026-11-04, staging, Neteges Demo, token del owner)

Cliente de prueba → ficha con `worker` (201, `storagePath` oculto) → contrato con `manager` que
vence en 10 días (201) → sin `customerId` 400, cliente inexistente 404, con acuse 400 → lista por
cliente con los dos → `contractsExpiring: 1` → tarea con cliente y `for-task` como owner con los
dos documentos y sus roles → descarga firmada → archivar el contrato (200; `entityId` va en la
query) y la lista activa baja a uno → borrado duro del cliente con documentos: **409
`has_history`**, como debe. Limpieza en dev: documentos, actividad, índice y ficheros borrados;
el cliente después, en duro. La demo queda sin clientes.

## 3. Lo que NO está

- **La app**: la sección «Documentos del cliente» en el bottom sheet de la tarea, leyendo
  `GET /customers/for-task/:taskId` y descargando por `documents/:id/download`. Es la única
  llamada nueva de la app del módulo.
- **Prueba con una trabajadora real** (token de empleada): que vea la ficha y no el contrato.
  Solo se probó como owner; la regla es la de sucursal, ya probada en ese ámbito.
- Producción: índice y reconstrucción de `documents` y `customers` (§33.7 del pase).

# 08 — Documentos del cliente: estudio de la siguiente fase

**Fecha:** 2026-11-03 (noche)
**Estado:** ESTUDIO. Nada construido. Jose: «ve estudiando la siguiente fase». Las decisiones
que necesita van al final, con mi recomendación en cada una.

---

## 1. Lo que Jose quiere, con sus palabras

- «Si escojo el cliente se relaciona la documentación que esté en esa tarea con los permisos
  pertinentes de cada documento: trabajador, supervisor, manager, etc.»
- «Un documento de ficha de cliente lo ve un trabajador, y todo cristo si se pone para todos;
  pero un contrato es solo para managers, owners y admin. O sea, lo normal de los permisos.»
- «Necesito ficha, porque si no obligas a una tarea de SAD a copiar la ficha del cliente todas
  las semanas.»
- «El cliente no puede condicionar nada de lo que ya funciona y mucho menos cambiar lógica.»

Traducido: la ficha del usuario del SAD (plan de cuidados, medicación, cómo entrar) es un
documento del cliente que la auxiliar ve desde **cualquier** tarea de ese cliente sin que nadie
lo vuelva a pegar; el contrato con la comunidad es otro documento del mismo cliente que la
auxiliar no ve. Los permisos son los del documental, sin regla nueva.

## 2. Lo que ya existe y se reutiliza tal cual

El servicio `documents:3007` ([documental-service](../documental-service/README.md)) ya tiene
todo lo que hace falta menos un ámbito:

- **Ámbitos** (`scope`): `entity`, `branch`, `employee`, y desde el inventario `item` y `unit`.
  Añadir `item`/`unit` fue exactamente el ejercicio que ahora toca con `customer`
  ([inventario 07 §4.1](../inventario/07_operables-documentos-y-entregas.md)): un valor más en
  el `scope`, un id más en el documento, una rama más en permisos y en la ruta de Storage.
- **Visibilidad por rol**: `visibleToRoles: worker | supervisor | manager`, elegida al subir y
  editable después. Owner y admin lo ven todo. Es «lo normal de los permisos» que pide Jose.
- **Vencimiento**: `expiresAt` ya existe y el inventario ya lo usa para seguros y revisiones. El
  contrato con fecha de fin no necesita campo nuevo: es `expiresAt`.
- **Metadatos**: `externalRef` (número de contrato), `tags`.
- **Descarga firmada** con TTL de un minuto y registro de actividad; **confirmación de lectura**
  (`ack`) y **firma incrustada en el PDF** (documental 08), que en el futuro sirven para que la
  familia o la comunidad firmen, pero eso es el portal (Fase 6), no esto.
- **Índice de búsqueda** documental y **notificaciones** de alta (`doc_uploaded`).
- En el panel: `BranchDocumentsSection` y `EquipmentDocumentsSection`, el mismo bloque de
  «Documentos» incrustado en la ficha de sucursal y en la del operable, con subida, lista,
  descarga y archivo. El de clientes es una copia con el ámbito cambiado.

## 3. Lo que hay que añadir

### En `documents`

- `scope: "customer"` y `customerId` en `ManagedDocument`; obligatorio con ese ámbito; el
  servicio comprueba que el cliente existe y está activo leyendo `entities/{e}/customers`.
- Ruta de Storage `documents/entities/{entityId}/customer/{customerId}/{documentId}/…`: lleva
  la empresa, el contador de almacenamiento lo cuenta solo (CLAUDE.md).
- **Tipos nuevos** en el catálogo. Ojo: `contract` ya existe y es RRHH puro (contrato laboral,
  solo owner/admin); reutilizarlo para el contrato con el cliente mezclaría dos cosas con reglas
  distintas. Propuesta: `customer_record` (la ficha), `customer_contract` (contrato, con
  `expiresAt`), `customer_quote` (presupuesto o tarifa enviada al cliente) y el `other` de
  siempre. Ninguno es RRHH ni disciplinario.
- **Permisos**, copiando la regla de sucursal sobre las sucursales del cliente:
  - *Subir, editar, archivar*: owner/admin, o manager o superior en alguna sucursal a la que el
    cliente está asignado. Igual que subir a una sucursal.
  - *Ver*: owner/admin; si no, el rol del actor está en `visibleToRoles` **y** el actor tiene
    responsabilidad en alguna sucursal del cliente. Es la misma regla que hoy tiene un documento
    de sucursal, aplicada a las sucursales del cliente. La trabajadora de la base de Neteges con
    `worker` en `visibleToRoles` ve la ficha; el contrato con `manager` no lo ve.
- **Listar**: `GET /documents?scope=customer&customerId=…`, y en la vista «todo lo del
  empleado» (fan-out) **no** entran los documentos de cliente: se llega a ellos por el cliente o
  por la tarea, no por la bandeja personal. Índice compuesto nuevo en Firestore:
  `documents (scope ASC, customerId ASC, status ASC, createdAt DESC)`, como los que ya hay por
  sucursal. Dev con gcloud; prod en el pase.
- **Notificaciones**: ninguna en esta fase. La ficha se consulta, no se empuja; un `doc_uploaded`
  a toda la plantilla de la base cada vez que se sube la ficha de un cliente sería ruido.

### En `customers`

- `GET /for-task/:taskId` ya devuelve `documents: []`: pasa a devolver los documentos activos
  del cliente que el actor puede ver (misma regla de arriba; para la trabajadora, los que llevan
  `worker`), sin `storagePath`, con `id`, `title`, `type`, `expiresAt`. La descarga va por
  `documents/:id/download` como siempre.
- `GET /:customerId` ya devuelve `contractsExpiring: 0`: pasa a contar los `customer_contract`
  con `expiresAt` en los próximos 30 días. Nada más.

### En el panel

- Ficha del cliente: bloque **Documentos** (`CustomerDocumentsSection`, copia del de sucursal
  con `scope: "customer"`): subir con tipo, visibilidad y fecha de fin; lista con tipo, quién lo
  ve, vencimiento en rojo cuando falta menos de 30 días o ya pasó; descargar; archivar.
- Gestión documental: el ámbito «Cliente» en el filtro y en la subida (buscador de clientes,
  el mismo índice), y en el detalle del documento el nombre del cliente con enlace a su ficha.
- Detalle de la tarea: si tiene cliente, bloque «Documentos del cliente» con la misma lista
  (quien gestiona la tarea los ve según su rol).

### En la app (fuera de este repo)

- En el bottom sheet de «datos del cliente» de la tarea, la lista de documentos de
  `GET /customers/for-task/:taskId` y la descarga por `documents/:id/download`. Es la única
  llamada nueva de la app en todo el módulo, y ya existe en staging.

## 4. Lo que NO toca nada de lo que funciona

Todo es aditivo: un valor nuevo en un `scope`, un campo opcional, ramas nuevas en permisos que
solo se ejecutan con ese ámbito, un bloque nuevo en una ficha nueva. Los documentos de
sucursal, empleado, empresa y operable no cambian de regla ni de pantalla. El patrón es el mismo
con el que el inventario añadió `item` y `unit` el 8 de octubre sin tocar los anteriores.

## 5. Tamaño

- API (`documents` + `customers`): un día. Patrón conocido.
- Panel: un día (bloque en la ficha, ámbito en Gestión documental, bloque en la tarea).
- App: la pantalla del bottom sheet, con el equipo de la app.
- Prod: índice de Firestore y reconstruir `documents` y `customers`.

## 6. Decisiones que necesita Jose (con mi recomendación)

- **D12 — Los tipos.** ¿Bastan `customer_record`, `customer_contract`, `customer_quote` y
  `other`? Recomiendo sí: pocos tipos y claros. Reutilizar `contract` (laboral) no, por sus
  reglas RRHH.
- **D13 — Quién sube.** ¿Manager de una sucursal del cliente, o solo owner/admin? Recomiendo
  manager de una sucursal del cliente, como en la sucursal: la coordinadora del SAD sube la ficha
  de Juana sin pedírselo a dirección.
- **D14 — Quién ve.** ¿Por rol en las sucursales del cliente (como la sucursal), o solo quien
  tiene una tarea del cliente? Recomiendo por rol en las sucursales del cliente: es la regla que
  ya existe, no necesita mirar tareas, y «lo ve quien va a trabajar» ya está dicho con
  `visibleToRoles`. La trabajadora llega al documento por la tarea, pero el permiso es el de
  siempre.
- **D15 — Avisos al subir.** Recomiendo ninguno en esta fase.
- **D16 — El contrato y su fin.** ¿`expiresAt` como fecha de fin, con rojo a 30 días? Recomiendo
  sí, y el número de días fijo en 30 hasta que alguien pida otro.

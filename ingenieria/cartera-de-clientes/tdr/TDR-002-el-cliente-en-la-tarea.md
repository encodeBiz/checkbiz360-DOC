# TDR-002 — El cliente en la tarea: `customerId`, `customerSiteId`, la copia para la app y el traslado de Neteges

**Fecha:** 2026-11-03
**Estado:** API en `develop` (e0292ac) y `staging` (bedfc59), desplegada a mano en el VPS de dev el 2026-11-03 con `[skip ci]`; panel en `encodebiz-front-saas` `feat/cartera-de-clientes` (b7ce6ffd), sin push. **Recortado al MVP** esa misma noche (06 §D11) y **probado contra staging**. Pendiente publicar el panel.
**Componente:** `encodebiz-api` — `packages/shared` (`Task`, `taskCustomerSnapshot`), `services/tasks`, `services/customers`; panel (tareas)
**Fase:** 2 de [05](../05_fases.md)

---

## 1. Qué se ha hecho

### El modelo

`Task` gana tres campos opcionales: `customerId`, `customerSiteId` y `customer`, la copia que
lee la app sin ir a otra colección (`TaskCustomerSnapshot`: `id`, `name`, `contacts` solo los
`visibleToWorkers` con nombre, cargo y teléfono, `fieldNotes`, `siteName`). Ausentes, la tarea es
la de siempre. `TaskListFilters` gana `customerId`.

### Quién construye la copia: el servidor

El diseño original decía «la escribe el panel». Se cambió: el panel manda los **ids** y el
servidor (`services/tasks/.../taskCustomer.ts`, `resolveTaskCustomer`) comprueba que el cliente
existe, está activo y **está asignado a la sucursal de la tarea** (`task/customer_not_assigned`),
que el lugar existe, está activo y es suyo (`task/customer_site_not_found`), y construye la copia
con `taskCustomerSnapshot` de `shared`. Así nadie puede colar en la tarea un nombre o un
teléfono que no está en la ficha, y el script de Neteges escribe exactamente lo mismo.

### La valla

Si el lugar es una dirección y la petición no trae `workSite`, el servidor copia **literal** la
valla del lugar: sin volver a Google y sin que la copia sea «parecida». Si el panel manda un
`workSite`, manda el suyo (la visita excepcional en otra dirección).

### Dónde entra

- `POST /tasks`: `customerId`, `customerSiteId`.
- `PATCH /tasks/:id`: `customerId: null` quita cliente, lugar y copia; un id lo pone o lo cambia
  (y suelta el lugar si el cliente es otro); `customerSiteId` cambia el lugar del cliente que ya
  tiene y, si no vino `workSite`, trae su valla.
- `POST /tasks/:id/duplicate`: copia los tres campos tal cual.
- `POST /tasks/system`: igual que el alta (cuadrante por tareas y add-ons).
- `GET /tasks?customerId=`: filtro. **Índice compuesto** `tasks (customerId ASC, dueAt ASC)`;
  el panel, que lee Firestore directo ordenado por `createdAt`, necesita además
  `tasks (customerId ASC, createdAt DESC)`. Los dos **creados en dev con gcloud** el 2026-11-03;
  los de prod van en el pase. Con los demás filtros (sucursal, estado, persona) Firestore
  fusiona índices.
- `customers`: `GET /for-task/:taskId` → `{customer, site, documents: []}` solo para quien está
  en `assignedEmployeeIds` o gestiona y alcanza al cliente (`customers/forbidden_for_task`, 403).
  La app no la necesita todavía: le basta `task.customer`. Es para la Fase 4.

### El script

`branches-to-customers --move-tasks`: además de crear cliente y lugar, las tareas **abiertas**
(`draft`, `assigned`, `in_progress`) de cada sucursal falsa pasan a la base con `branchId`,
`customerId`, `customerSiteId`, la copia y la valla del lugar si no tenían una; las terminadas,
validadas, rechazadas y canceladas se quedan donde están. A las personas se les quita la
sucursal falsa y se les pone la base. Vale también para sucursales cuyo cliente ya existía. Simula
por defecto. Sigue sin borrar sucursales (06 §D9).

### Fuera la tarifa

Jose, 2026-11-03: «tarifas y presupuestos siguen siendo documentos». Se quitó `rate` de
`Customer` y `CustomerSite` y `parseRate` de los routers; ADR-004 queda reemplazado; la Fase 5
ya no tiene 5a.

## 1b. El recorte del MVP (06 §D11, misma noche)

Jose decidió sacar un MVP: fuera lugares, dedicadas y «toda la empresa» de la pantalla; sin horas
por cliente en esta versión. En la API cambió una cosa: **la dirección del cliente es la valla por
defecto**. `resolveTaskCustomer` devuelve `customer.address` como `workSite` cuando no hay lugar;
el alta y `/tasks/system` la copian salvo `useCustomerAddress: false`; el `PATCH` la copia al poner
o cambiar el cliente, `useCustomerAddress: true` la vuelve a poner y `false` la deja fuera. Probado
contra staging: con cliente y sin `workSite` la tarea sale con la dirección del cliente; con
`false`, sin valla; `PATCH {useCustomerAddress:true}` la pone; quitar el cliente conserva la valla.
Los lugares (`customerSiteId`) y `GET /for-task` siguen en la API sin que el panel los use.

## 2. El panel (`feat/cartera-de-clientes`, fafac272 + b7ce6ffd)

- `TaskFormDialog`: **después de elegir sucursal y solo si tiene clientes asignados**, «Cliente»
  (uno solo en el alta → puesto; varios → se elige, sin preseleccionar). Con cliente, el check
  «Usar la dirección del cliente como lugar de trabajo», marcado por defecto: oculta el campo de
  dirección propia y el servidor copia la del cliente. Desmarcado, el campo de siempre. Cambiar de
  sucursal suelta el cliente. Al editar, quitar el cliente manda `customerId: null`. (El selector
  de lugar existió en fafac272 y se quitó en b7ce6ffd.)
- Detalle de la tarea: cliente con enlace a su ficha y nombre del lugar, en «Lugar de trabajo».
- Lista: filtro **Cliente** por el índice de búsqueda (tipo `customer` añadido a
  `SearchIndexInput`, `searchIndex.ts` y `helper.service.ts`), solo si la empresa tiene clientes.
- Ficha del cliente: sin «Lugares» ni dedicadas; la asignación es la lista de sucursales, al menos una.
- Textos `tasks.customer.*` en los cinco idiomas.

## 2b. Lo que se probó (2026-11-03, staging, Neteges Demo, token del owner)

Cliente «Juana» con dos contactos (uno visible, otro no) y un lugar `address` → tarea con
`customerId` + `customerSiteId` y sin `workSite` (201): la copia lleva nombre, notas de campo,
**solo el contacto visible** y `siteName`; el `workSite` es el del lugar con su radio y su zona
horaria. `customerId` inexistente → 400 `task/customer_not_found`. `GET /tasks?customerId=`
devuelve la tarea (índice en dev). `GET /customers/for-task/:id` como owner → 200 con cliente y
lugar. `PATCH customerId:null` deja la tarea sin cliente ni copia y conserva la valla. `PATCH`
con `customerId` sin lugar → copia sin `siteName`. Duplicar copia el cliente. Limpieza: tareas
borradas, cliente borrado en duro; la demo queda sin clientes.

## 3. Lo que NO está

- **Plantilla del cuadrante por tareas** con columna «Cliente»: pendiente de decidir si entra en el MVP.
  La API ya acepta `customerId` por fila en `/tasks/system`.
- **Script de Neteges** (`--move-tasks`): descartado hasta tener todo claro (06 §D11).
- **App**: sin versión nueva enseña la tarea como hoy con el `workSite` copiado. La primera
  versión que toque tareas lee `task.customer` (nombre, notas de campo, contactos visibles).
- Índices de prod y reconstrucción de `tasks` y `customers` en el pase (§33 del próximo pase).

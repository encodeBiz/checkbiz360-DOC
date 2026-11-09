# TDR-001 — Fundación y maestros: `customers:3018`, clientes, lugares y sucursales asignadas

**Fecha:** 2026-11-03
**Estado:** API en `develop` y **desplegada en staging** el 2026-11-03 (merge 5ab4f25 + fix nginx ef81b9f); dirección del cliente fusionada a `develop` (0281aa7) y `staging` (6d4cb8b) el 2026-11-03. Panel implementado en `encodebiz-front-saas`, rama `feat/cartera-de-clientes`, **sin commitear**, probándose en local contra staging
**Componente:** `encodebiz-api` — `services/customers` (nuevo), `packages/shared` (`checkbiz/customers`, `searchIndex`), compose y nginx de staging
**Fases:** 0 y 1 de [05](../05_fases.md)

---

## 1. Qué se ha hecho

### El servicio

`services/customers/` copia el esqueleto de `inventory` sin la puerta: `app.ts` monta
`requireCredential` (auth dual, ID token de Firebase o sesión de trabajador) →
`requireEntity` (el `entityId` de query, body o ruta; una sesión de trabajador solo habla de
su entidad) → `resolveActor` (nivel más alto en cualquier centro, sucursales con mando) →
routers. `requireEntity` ocupa el sitio de la puerta de inventario para que, cuando llegue el
portal, su `requirePortalSubscription` se cuelgue detrás sin mover nada
([ADR-001](../adr/ADR-001-servicio-customers-en-el-core-gratuito.md), [ADR-005](../adr/ADR-005-el-portal-del-cliente-es-el-add-on-como-el-quiosco.md)).

Puerto 3018, `GET /health`, bloque en `docker-compose.staging.yml`, upstream y location en
`nginx.staging.conf`, `dev:customers` y `build:customers` en el `package.json` raíz y en las
cadenas `build` y `typecheck`. Los de producción se añaden en el pase, como dice el 05.

### El dominio, en `shared`

`packages/shared/src/checkbiz/customers/`: `Customer`, `CustomerContact`, `CustomerRate`,
`CustomerSite` y sus repositorios Firestore en `entities/{e}/customers/{id}` y
`…/customers/{id}/sites/{id}`. El listado lee la colección entera de la entidad y filtra y
ordena en memoria, como los almacenes: decenas o pocos cientos de documentos, y el
«asignado a X o a todas» exigiría dos consultas y un índice compuesto para ahorrar nada.

`searchIndex` gana el tipo `customer`, `customerIndexPath` e `indexCustomer` (nombre, NIF,
referencia y calle; el tipo en `metadata`). El buscador del panel y `GET /?q=` van por ahí.

**Dirección del cliente** (2026-11-03, pedido de Jose): `Customer.address?: TaskWorkSite`, la
misma forma que el lugar y que el `workSite` de la tarea, parseada por el mismo
`parseWorkSite` (`interfaces/http/customer/parseWorkSite.ts`, compartido con `site.router`).
`POST` la acepta, `PATCH` la cambia o la quita con `address: null`. El script
`branches-to-customers` da al cliente la dirección de la sucursal además del lugar. Es *dónde
está* el cliente; *dónde se trabaja* para él siguen siendo los lugares.

### Las reglas que impone el servidor

- `scope: "branches"` exige al menos una sucursal (`customers/branches_required`); con
  `"entity"`, `branchIds` se guarda vacío.
- `dedicatedBranchIds ⊆ branchIds` (`customers/branch_not_assigned`); con `"entity"`,
  cualquier sucursal activa.
- Una sucursal dedicada a **un solo** cliente: `customers/branch_already_dedicated` con el
  cliente que la tiene ([ADR-003](../adr/ADR-003-la-tarea-lleva-el-cliente-y-las-horas-se-imputan-por-tarea-o-por-sucursal-dedicada.md)).
- Toda sucursal nombrada tiene que existir y estar activa (`customers/branch_not_found`).
- Un lugar `address` lleva `street`, `geo` y `radiusMeters` (la valla de `Geofence`, la
  misma de la tarea y la sucursal); un lugar `branch` apunta a una sucursal asignada al
  cliente.
- `PUT /:id/branches` sustituye la asignación entera; los lugares `branch` que apuntan a una
  sucursal que deja de estar asignada se desactivan y se devuelven en `warnings`.
- Las sucursales **no** se tocan por `PATCH`: 400 que señala a `PUT /branches`. Es otro gesto
  en el panel y otro permiso.
- Borrado blando por defecto (`inactive`, fuera del buscador y de los selectores). Duro con
  `?hard=true` solo sin tareas ni documentos con `customerId` (`customers/has_history`,
  contados con `count()` sobre `entities/{e}/tasks` y `…/documents`); hoy ninguno los lleva,
  la pregunta ya está hecha para las Fases 2 y 4.

### Permisos

| | Owner, admin, responsable nivel owner | Gestor con mando | Supervisor | Trabajador |
|---|---|---|---|---|
| Listar y ver | Todo | Los de sus sucursales | Los de sus sucursales | 403 (verá el cliente de su tarea en la Fase 2) |
| Crear y editar | Sí | Sí, solo asignando a sus sucursales; nunca `scope: "entity"` | No | No |
| `PUT /branches` | Sí | Solo si todas las sucursales son suyas | No | No |
| Borrar | Sí | No (desactiva con `status`) | No | No |

### Los scripts

- `branches-to-customers --entity --base [--branches a,b] [--radius 150] [--out mapa.json]
  [--apply]`: por cada sucursal activa que no sea la base crea un cliente (empresa, nombre y
  NIF de la sucursal, asignado a la base) y un lugar `address` con su dirección, coordenadas
  y radio de fichaje. Idempotente por nombre. **No borra ni desactiva sucursales (06 §D9), no
  mueve empleados ni tareas** (`--move-tasks` es de la Fase 2). Simula por defecto.
- `reindex-search --entity [--apply]`: reescribe la entrada de cada cliente activo y retira
  las huérfanas.

## 2. Lo que se probó (2026-11-03, local contra `dev-encodebiz`, Neteges Demo)

Servicio arrancado en local con la cuenta de servicio de dev y un ID token del owner de la
demo. Sin token, 401; con token basura, 401; ruta inexistente, 404. Después, de punta a punta
sobre la demo: lista vacía → crear cliente con sucursal dedicada (201) → segundo cliente
dedicado a la misma sucursal (409 con el nombre del primero) → `branches` sin sucursales
(400) → lista por sucursal devuelve el cliente → búsqueda `q=comunidad` por el índice → ficha
con `sitesCount` → lugar `address` (201) → lugar sin valla (400) → lugar `branch` (201) → PATCH
nombre y tarifa → `PUT /branches` a `entity` (la sucursal dedicada se suelta; el lugar `branch`
sigue válido porque `entity` cubre todas las sucursales, así que `warnings` vacío) → PATCH con
`branchIds` (400) → borrado blando (204; 0 activos, 1 inactivo) → borrado duro (204; 404
después) → la entrada del buscador desaparece. La demo quedó como estaba: sin clientes.

Dirección del cliente (2026-11-03, misma demo, servicio local): alta con `address` (201), sin
coordenadas (400 `address.geo`), la ficha la devuelve, `q=layret` encuentra al cliente por la
calle, `PATCH {address: null}` la quita y la búsqueda por la calle deja de encontrarlo, `PATCH`
la vuelve a poner, borrado duro (204, 404 después, índice vacío). La demo quedó sin clientes.

`branches-to-customers` en simulación contra la demo: 0 candidatas, porque la demo ya tiene
una sola sucursal. La prueba con sucursales de verdad es contra la entidad real de Neteges,
**simulada y con ellos delante** (06 §D2).

## 2b. El panel (2026-11-03, `encodebiz-front-saas`, rama `feat/cartera-de-clientes`)

- Entrada **«Clientes»** en el menú de CheckBiz, tras Sucursales, sin bloque premium: es core.
- Proxy `checkinbiz_customers_handler` (`NEXT_BACKEND_URI_CHECKINBIZ_CUSTOMERS_HANDLER`, base
  `/api/v1/customers`) con allowlist de la raíz, `/:id`, `/:id/branches` y `/:id/sites[/:id]`.
- `customers.service.ts`: el transporte de inventario (token fresco, 2FA, cuerpo del error
  intacto). `ICustomer.ts` con los tipos. Errores `customers/*` en `errorLocales` (es, en).
- Lista paginada en servidor con búsqueda por índice (desde tres letras), filtro por sucursal y
  estado; alta y edición en diálogo (tipo, nombre, NIF, referencia, contactos con «lo ve quien
  va a trabajar», notas de campo, notas de gestión; en el alta, sucursales y dedicadas).
- Ficha consultiva: cabecera con tipo, estado, sucursales (la dedicada con estrella), métricas,
  contactos, lugares (dirección con la valla de la tarea, reutilizando `TaskWorkSiteField`, o
  una sucursal asignada), notas. «Editar sucursales» aparte (`PUT /branches`); desactivar y
  reactivar desde la ficha.
- Diálogos con `dynamic()`; textos en los cinco idiomas del panel.
- Dirección en el alta y la edición con `TaskWorkSiteField` (al que se le añadieron `title`,
  `description` y `label` opcionales para no decir «lugar de trabajo»); en la ficha, bajo la
  cabecera. Notas de campo y de gestión con `RichTextEditor` (Markdown, el de la tarea) y
  `RichTextViewer` en la ficha.
- Estilo alineado con el resto del panel (2026-11-03, segunda pasada): filtros dentro de
  `GenericTable` como `topFilter` (buscador, sucursal y estado), la fila abre la ficha,
  `EmptyList` solo sin clientes y sin filtros; pastillas con `CustomChip`; la ficha en
  `DetailBlock` (`components/common/detail/DetailBlocks`), cabecera sin cambios.
- **Nginx**: la raíz `/api/v1/customers` sin barra devolvía 301; se añadió `location =` exacta
  para que el POST del alta no llegue como GET.

## 2c. El recorte del MVP (06 §D11, noche del 03-nov)

Del panel salieron **Lugares**, **sucursales dedicadas** y **«toda la empresa»**; la asignación es
la lista de sucursales, al menos una. La API conserva `sites`, `dedicatedBranchIds` y
`scope: "entity"` sin que nadie los mande, hasta un pase tranquilo. El script
`branches-to-customers` queda **descartado hasta tener todo claro**.

## 3. Lo que NO está

- **Panel sin commitear**: el repo del panel exige permiso explícito para commitear; los
  cambios están en el árbol de trabajo de `feat/cartera-de-clientes`.
- **Producción**: ni compose ni nginx de prod; van en el pase.
- **Espejo a Postgres**: Fase 3. Los lugares no actualizan tareas futuras: Fase 2.
- **Pruebas automáticas**: el servicio no tiene tests unitarios; la prueba fue la de humo de
  arriba. Si se quiere una red, el sitio es `packages/shared/test` para las reglas de
  asignación, que son funciones puras.

## 4. Cómo desplegar en desarrollo

Tras fusionar a `develop` y de ahí a `staging`, el *Staging CI/CD* levanta el servicio con el
resto (`up --build -d` y reinicio de nginx). Si se hace a mano, el orden de siempre: `git pull`,
`build --no-deps customers`, `up -d customers`, reiniciar nginx. Comprobación:
`curl https://api-staging.checkbiz360.com/api/v1/customers/health` no existe (el health está
en la raíz del contenedor), así que `docker compose … exec -T customers wget -qO-
http://localhost:3018/health` y una llamada autenticada a `GET /api/v1/customers?entityId=…`.

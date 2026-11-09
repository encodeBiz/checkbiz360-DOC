# 05 — Fases de implementación

Cada fase es **independiente y desplegable**. El orden es por uso, y el primer uso tiene
nombre: **Neteges**, que ya tiene la demo del horario por tareas en staging y a quien la
cartera le cierra la cadena sucursal → tarea → cliente → empleado. La empresa de ayuda a
domicilio del TDR-007 es el segundo caso y manda sobre la Fase 4.

Cada fase lleva tres partidas: **API** (este repo), **panel** (`encodebiz-front-saas`) y
**app**. La app pinta poco en este módulo hasta la Fase 4, y eso es a propósito: el lugar del
cliente viaja en el `workSite` que la app ya conoce.

Ritual de despliegue mientras GitHub Actions siga parado: a mano, con el orden de
`feedback-desplegar-solo-lo-que-cambia`, y la migración `049` siempre por SSH, antes del
servicio que la necesita.

---

## Fase 0 — Fundación

**Objetivo:** el esqueleto en pie con la puerta puesta desde el primer día.

**API**
- `services/customers/` con `app.ts`, `server.ts`, `package.json`, `tsconfig.json`, `Dockerfile`
  (copia del de `inventory`, puerto 3018).
- `GET /health` → `{ok: true, service: "customers"}`.
- Bloque en los dos compose; upstream y location `/api/v1/customers/` en los dos nginx.
- **Sin puerta de suscripción** (ADR-001, revisado el 03-nov): credencial de checkinbiz y
  `resolveActor`, como `tasks`. Nada en `SERVICES`, nada en `billing`, nada en Stripe. La
  puerta del portal llega en la Fase 6.

**Panel** — nada aún. **App** — nada.

**Criterio de éxito:** `/health` responde; cualquier otra ruta devuelve 401 sin credencial y
pasa con la de una empresa de dev.

---

## Fase 1 — Clientes, lugares y sucursales

**Objetivo:** que el admin pueda dar de alta a quién trabaja y dónde, y que Neteges pueda
pasar sus 134 sucursales falsas a clientes.

**API**
- `Customer`, `CustomerSite` en `shared` con repositorios Firestore; entrada en `searchIndex`
  con `kind: "customer"`.
- Rutas de clientes, `PUT /branches`, rutas de lugares ([04](./04_contratos-api.md)).
- Reglas del servidor: `dedicatedBranchIds ⊆ branchIds`, una sucursal dedicada a un solo
  cliente, lugar `branch` solo sobre sucursal asignada.
- **Script `branches-to-customers`** (`services/customers/src/scripts/`): para una entidad,
  toma las sucursales que se le indiquen (todas menos la base, o una lista), crea un cliente
  por sucursal con un lugar `address` copiado de la dirección y la geocerca de la sucursal,
  lo asigna a la sucursal base, y deja un fichero de correspondencia `branchId → customerId`.
  **Simula por defecto, actúa con `--apply`.** No borra sucursales: eso es una decisión de la
  empresa, después de ver que las tareas ya apuntan a clientes. Reasignar a los empleados a
  la base y recolocar tareas existentes es la Fase 2 del mismo script (`--move-tasks`), porque
  depende de que la tarea tenga el campo.

**Panel**
- Servicio `customers` en `BizType`, proxy, entrada de menú **«Clientes»** para toda
  empresa con checkinbiz.
- Lista paginada en servidor con búsqueda por `searchIndex`, filtro por sucursal y estado.
- Ficha del cliente en pestañas: **Datos** (tipo, nombre, NIF, referencia, contactos con su
  «lo ve el trabajador», notas de campo), **Lugares** (mapa y geocerca, el mismo componente
  del `workSite` de la tarea; «este lugar es una sucursal» para construcción), **Sucursales**
  (a cuáles se asigna, cuáles son dedicadas, con la frase que lo explica: «las jornadas
  fichadas aquí cuentan para este cliente»). Pestañas Actividad, Documentos, Contratos y
  Presupuestos aparecen en su fase.
- Ficha consultiva; edición en Editar, como el resto del panel.

**App** — nada.

**Criterio de éxito:** Neteges Demo (staging, `318Ey5ZHBMeqm5fsQ0Md`) con sus 142 centros
convertidos en 142 clientes con lugar bajo «Oficina Badalona», buscables desde el panel.

---

## Fase 2 — El cliente en la tarea

**Objetivo:** que la tarea sepa para quién es y la trabajadora llegue al sitio sin que nadie
teclee una dirección.

**API**
- `customerId`, `customerSiteId`, `customer` (snapshot) en `Task` de `shared`; `tasks` los
  acepta y guarda opacos en `POST`, `PATCH` y `duplicate`.
- `/tasks/system` (carga de cuadrante por tareas) acepta `customerId` por fila.
- `GET /for-task/:taskId` en `customers` (lo usará la app en la Fase 4; se hace ya para que
  el panel lo pruebe).
- Script `branches-to-customers --move-tasks`: recoloca las tareas de cada sucursal falsa a
  la base con su cliente y su lugar, y los empleados a la base. Simula; `--apply`.

**Panel**
- En el formulario de la tarea, bajo la sucursal: **Cliente**, solo si la sucursal tiene
  alguno asignado. Un cliente
  en esa sucursal → puesto solo, sin desplegable. Varios → desplegable obligatorio **sin
  preseleccionar**. Ninguno → el formulario de siempre. Elegido el cliente, **Lugar** con la
  misma regla, y el mapa del `workSite` se rellena del lugar y queda editable para ese caso
  concreto (una visita excepcional en otra dirección no obliga a crear un lugar).
- Detalle de la tarea: nombre del cliente y lugar, con enlace a la ficha.
- Plantilla del cuadrante por tareas: columna «Cliente» (nombre o referencia); la propuesta
  marca las filas que no casan y las deja sin cliente, nunca en error.
- Lista de tareas: filtro por cliente.

**App**
- Sin versión nueva, enseña la tarea como hoy con el `workSite` del cliente. En la primera
  versión posterior a 1.10.1 que toque tareas: nombre del cliente, notas de campo y los
  contactos con `visibleToWorkers` leídos del snapshot `task.customer`, en el detalle de la
  tarea. Sin llamada nueva, sin regla nueva.

**Criterio de éxito:** en Neteges Demo, el cuadrante de noviembre regenerado con cliente por
tarea; una auxiliar en la demo SAD de staging ve en la tarea a quién va a ver y con qué
teléfono.

---

## Fase 3 — Espejo, horas e informe por cliente

**Objetivo:** la frase completa: para quién, cuántas horas, quién, con qué fotos y material.

**API**
- Migración `049`: tablas del módulo, columnas en `tasks_raw`, `customer_hours_daily`.
- Espejo desde `customers` en la misma petición, job de reintento (`/internal/mirror/retry`).
- Job de imputación: cada noche para el día anterior y al cerrar cada tarea con cliente;
  `/internal/hours/recompute` para rehacer un periodo. Regla del
  [ADR-003](./adr/ADR-003-la-tarea-lleva-el-cliente-y-las-horas-se-imputan-por-tarea-o-por-sucursal-dedicada.md).
- `GET /:customerId/activity`.
- En `reports`: informe **«Por cliente»** (XLSX) y columna «Cliente» en el informe de tareas,
  ambos **solo si la empresa tiene algún cliente**; sin clientes, los informes de siempre.

**Panel**
- Pestaña **Actividad** en la ficha: horas por mes y por persona, tareas con sus evidencias,
  material si hay inventario; «Descargar informe» con periodo y lugar.
- En Informes, «Por cliente» junto al resto.
- Filtro «cliente desconocido» en la lista de tareas (tareas con `customerId` que no resuelve).

**App** — nada.

**Criterio de éxito:** el informe de octubre de un cliente de la demo cuadra con la suma de
sus tareas; una obra dedicada en una empresa de construcción de dev imputa las jornadas
fichadas sin que ninguna tarea lleve cliente.

---

## Fase 4 — Documentos del cliente (contratos, presupuestos y tarifas incluidos)

**Objetivo:** el expediente de Juana vive en Juana y lo ve quien va a su casa hoy.

**Lo que Jose fijó el 2026-11-03:** contratos, presupuestos y tarifas **son documentos del
cliente**, no objetos aparte. El contrato es un PDF con fechas y aviso de vencimiento; el
presupuesto o la tarifa que la empresa mandó a su cliente es otro PDF. No hay `rate` en el
cliente ni en el lugar (se quitó de la API ese día) ni `CustomerBudget`.

**API**
- `scope: "customer"` en `documents`; ruta de Storage bajo `customers/{customerId}/documents/`.
- Un documento del cliente puede llevar `kind: "contract" | "quote" | "rate" | "other"` y, si es
  contrato, `startsAt`, `endsAt` y `warnDaysBefore`: vencimiento en rojo en `GET /:customerId`
  y en la lista. Es el `CustomerContract` del 03, pero **dentro** del documento.
- `GET /for-task/:taskId` devuelve los documentos con `visibleToRoles ∋ worker`.
- Los adjuntos de la tarea (TDR-007, `isEvidence: false`) **se quedan donde están y como
  están**: se sigue subiendo a la tarea directamente, para quien no quiera relacionar
  clientes. No hay script que los convierta ni que los mueva (decisión de Jose, 2026-11-03).

**Panel**
- Pestaña **Documentos** en la ficha (el componente del documental con el ámbito cliente; «lo
  ve el trabajador» por documento); los contratos salen con su vigencia y en rojo a X días
  del fin. Sin pestaña «Contratos» aparte.

**App**
- En el detalle de la tarea, sección «Documentos del cliente» llamando a `for-task`. Es la
  única llamada nueva de la app en todo el módulo. Cada apertura queda en `DocumentActivity`.

**Criterio de éxito:** en la demo SAD de staging, la auxiliar con tarea de Juana ve su
expediente; otra auxiliar sin tarea de Juana no, aunque sea del mismo centro.

---

## Fase 5 — Rentabilidad del montaje

Rediseñada el 2026-11-03 ([ADR-006](./adr/ADR-006-el-contrato-es-el-montaje.md)) a raíz de un
prospecto que quiere la inversión, el coste y el beneficio de cada montaje. **Lo único que
pide es el PDF que la empresa ya tiene; el resto sale solo.** Si D11 la hace add-on, lleva
puerta como inventario. La tarifa estructurada (`rate`) que había aquí **se quitó** el mismo
día: la tarifa es un documento del cliente (Fase 4); el importe del montaje sale del contrato
leído.

**Objetivo:** que cada montaje enseñe lo que costó frente a lo que se cobró, y que la empresa
sepa antes de empezar cuánto se le suele ir.

**Rehecha el 2026-11-05 en [TDR-004](./tdr/TDR-004-rentabilidad-del-montaje.md)** (API en staging): el contrato cuelga del cliente, puede haber varios a la vez y la tarea dice de cuál es. Lo que sigue es el diseño original de ADR-006; donde difiere, manda el TDR.

### 5b — El contrato es el montaje

**API**
- `CustomerContract` gana `amount`, `estimatedHours`, `complexity`, `link`, `extraction`,
  `initialEstimate`; `POST /contracts/extract` lee el PDF por el camino de la lectura de
  cuadrantes y devuelve la propuesta con la cita de cada dato, sin guardar nada.
- `POST /contracts/:id/link` a una sucursal dedicada o a una tarea del cliente; 409 si la
  sucursal no está dedicada, con `?dedicate=true` para hacerlo en el mismo gesto.
- `customer_hours_daily` gana `reliable` y `hourly_cost_cents`; el job que la llena los
  rellena desde el cajón de la jornada y el `price` del puesto ese día.
- `GET /contracts/:id/profitability`: horas (fiables y sin cerrar), coste de RRHH en bruto,
  material con y sin coste, margen si hay importe. `GET /:customerId/profitability` agrega.

**Panel**
- Al subir un contrato: el formulario sale relleno con lo leído, cada campo con su cita al
  lado, y se confirma o se corrige. Lo que no se encontró, vacío.
- Tarjeta **Rentabilidad** en la sucursal y en la tarea con contrato vinculado; pestaña
  **Contratos** del cliente con la misma tarjeta por contrato y el total. Etiqueta «en
  bruto» visible, cobertura de jornadas fiables, y en rojo cuando el coste pasa del importe.
- Tiempo estimado y complejidad editables siempre; la primera estimación se ve, en gris.

**App** — nada.

### 5c — Cierre y previsión

**API**
- `POST /contracts/:id/close` escribe `contract_outcomes`.
- `profitability.forecast`: sesgo por empresa y complejidad sobre los cerrados (mínimo 5),
  horquilla de horas, coste y margen antes y durante, `overBudgetAt` a ritmo de los últimos
  7 días. Sin histórico suficiente, `insufficient_history` y ningún número.

**Panel**
- Botón «Cerrar montaje» en la tarjeta; la previsión como horquilla, nunca una cifra sola,
  con el pie «sobre N montajes cerrados de complejidad X». Sin histórico, la frase que lo
  dice y nada más.

**Merlin** — fuera de esta fase (D8): cuando haya cierres que leer, narra la desviación.

**Criterio de éxito:** en dev, un contrato subido en PDF sale con importe y horas leídos y
citados; vinculado a una obra, al día siguiente de fichar enseña coste y margen en bruto; con
cinco montajes cerrados sembrados, el sexto enseña su horquilla antes de empezar, y con
cuatro dice que no hay histórico suficiente. Una comunidad con tarifa sigue dando el importe
de octubre que la empresa teclearía en su programa de facturación.

---

## Fase 6 — Portal del cliente (add-on)

**Objetivo:** cerrar el círculo: el cliente de nuestro cliente ve cuándo vienen, firma lo que
hay que firmar, lee el parte con las fotos y pide lo que necesita. Boceto, lo que se copia de
otros y lo que no, y sus subfases 6a/6b/6c en [07](./07_portal-del-cliente.md). Se cobra como
el quiosco ([ADR-005](./adr/ADR-005-el-portal-del-cliente-es-el-add-on-como-el-quiosco.md)).
Se detalla en TDR al arrancar; depende de las Fases 2, 3 y 4.

---

## Después, si lo piden

- **Merlin** leyendo clientes: «este mes Diagonal 400 lleva un 20 % menos de horas que el
  anterior».
- **Cliente al fichar sin tarea**: elegir cliente en el gesto de fichar cuando la sucursal
  tiene varios y no hay tarea. Hoy se resuelve creando la tarea.
- **Rutas**: el reparto que hizo el script de la demo de Neteges (zonas, cercanía, 40 horas)
  como función del panel. Es un módulo entero.
- **Avisos** de contrato a punto de vencer y de presupuesto superado en el correo de owner y
  admin (alertas por correo, fase 3 de ese módulo).

## Lo que exige cada entorno

| | Desarrollo | Producción |
|---|---|---|
| Suscripción | ninguna para el básico; el portal (Fase 6) con script `suscripcion-de-prueba` | ninguna para el básico; el portal con precio en Stripe en vivo y alta del servicio |
| Compose y nginx | `docker-compose.staging.yml`, `nginx.staging.conf` | `docker-compose.yml`, `nginx.conf`, en el pase |
| Migración `049` | por SSH en `encodebiz_staging` | por SSH en `encodebiz_analytics`, una a una |
| Índices Firestore | `--project dev-encodebiz` explícito | `--project encodebiz-services`, en el pase |
| `searchIndex` | `reindex-search --apply` por entidad | ídem, por entidad |
| Panel | Vercel solo prod; staging desde el portátil | variables en Vercel |
| Neteges | demo en staging con el script | script contra la entidad real, **simulado primero y con Neteges delante** |

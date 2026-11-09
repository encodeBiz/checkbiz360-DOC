# TDR-008 — Gastos externos del contrato (y, después, desde la tarea)

**Fecha:** 2026-11-07
**Estado:** Fases 1, 2, 3, §6 ter y §6 quater EN STAGING el 2026-11-07 (pase §51 y §52); app en develop (`bea1179`). Decidido por Jose el 2026-11-07 («sí»). Fases 2 y 3 decididas el mismo día («las dos fases después, es muy importante y tributa directamente al cliente»; D1 no, D2 sí): van detrás de la 1.
**Componente:** `migrations/060`, `services/customers` (contratos y su rentabilidad), `services/analytics` (análisis del cliente), panel (tarjeta y formulario del contrato)
**Amplía:** [TDR-004](TDR-004-rentabilidad-del-montaje.md) (coste del contrato) y [TDR-007](TDR-007-analisis-a-fondo-del-cliente.md) (rentabilidad del cliente)

---

## 1. Para qué

Hoy el coste de un contrato es personal (horas × precio del puesto) más material del inventario. Lo que
se paga fuera —subcontratas, alquiler de maquinaria, desplazamientos y parking, dietas, un producto
comprado para ese cliente— no cuenta, y el margen sale mejor de lo que es. Jose: «un listado de gastos
externos a empleados para que sea aún más preciso».

## 2. Lo decidido

- Cada gasto: **concepto**, **importe** (sin IVA, en céntimos) y **fecha**, que viene rellena con hoy. La
  fecha es la que lo coloca en su mes del análisis; sin ella habría que repartirlo y una subcontrata de
  2 000 € se desdibuja.
- **Tarjeta del contrato:** los 5 más recientes y «Cargar más», paginado en el servidor.
- **Editar:** lista dinámica —Concepto, Importe, Fecha, «Añadir gasto», papelera por fila—, y **cada fila
  se guarda sola**: un contrato de un año puede llevar cien gastos y uno mal escrito no puede bloquear los
  demás.
- **Solo propietario y administrador** (es dinero, TDR-004): el gerente no los ve ni los toca.
- **El parte del cliente no los lleva** (se manda al cliente, TDR-006 §2).
- En Postgres, de donde lee ya todo el análisis.

## 3. Modelo (Fase 1, pensado para las Fases 2 y 3)

Migración **`060_gastos_externos.sql`**, tabla `customer_expenses`:

| Columna | |
|---|---|
| `expense_id` | `UUID` PK (`gen_random_uuid()`) |
| `entity_id`, `customer_id` | `VARCHAR(64) NOT NULL` |
| `contract_id` | `VARCHAR(64)`; en la Fase 1, siempre |
| `task_id` | `VARCHAR(64)`; Fases 2 y 3 |
| `concept` | `TEXT NOT NULL` (1–200) |
| `amount_cents` | `BIGINT NOT NULL CHECK (amount_cents > 0)` |
| `spent_on` | `DATE NOT NULL` |
| `document_id` | `VARCHAR(64)`: el ticket o la factura (Fases 2 y 3) |
| `source` | `'panel' | 'app'`, por defecto `'panel'` |
| `status` | `'approved' | 'pending' | 'rejected'`, por defecto `'approved'`: solo cuentan los `approved` |
| `created_by`, `created_at`, `updated_by`, `updated_at`, `deleted_at` | borrado blando |

Índices: `(entity_id, contract_id, spent_on DESC)` y `(entity_id, customer_id, spent_on)`, los dos con
`deleted_at IS NULL`.

La fuente es Postgres (no hay copia en Firestore): un gasto es un dato de gestión que solo lee el panel y
el análisis, y Postgres es donde se suma. Si Postgres no responde, la ruta da error y no se guarda nada a
medias.

## 4. API (`customers`), solo propietario y administrador

- `GET  /contracts/:id/expenses?entityId&limit=5&cursor` → `{ items: [{ id, concept, amountCents, spentOn, createdAt }], nextCursor, totalCents, count }` — por `spent_on DESC, created_at DESC`; `totalCents` y `count` del contrato entero.
- `POST /contracts/:id/expenses` `{ entityId, concept, amountCents, spentOn? }` → el gasto. Contrato cerrado: se puede (un gasto llega tarde).
- `PATCH /contracts/expenses/:expenseId` `{ entityId, concept?, amountCents?, spentOn? }`.
- `DELETE /contracts/expenses/:expenseId?entityId` → borrado blando.
- Borrar un contrato marca borrados sus gastos.

## 5. Dónde cuentan

- **Rentabilidad del contrato** (`profitabilityOf`, TDR-004): `costCents` = personal + material +
  **gastos externos** con `spent_on <= asOf`; bloque nuevo `expenses: { cents, count }` en la respuesta
  para pintarlo como línea propia. Se tapa para el gerente igual que el resto del dinero.
- **Análisis del cliente** (`insights`, TDR-007): cada mes gana `expenseCents` (gastos aprobados de los
  contratos del cliente, por `spent_on`), y el coste y el margen lo incluyen; `last3` igual.
- **Panel:** en la tarjeta del contrato, «Gastos externos: {total}» junto al coste, y la lista.

## 6. Estudio: gastos desde la tarea (Fases 2 y 3, sin fecha)

Muchos gastos nacen en la tarea —el parking de la visita, el producto comprado para ese servicio, la grúa
del montaje— y quien tiene el ticket es quien está en ella.

**Fase 2 — desde el panel, en «Archivos» de la tarea.** Al adjuntar un fichero, marcar «Es un gasto»:
concepto, importe y fecha. Se guarda el adjunto como hoy (TDR-007 de tareas, `isEvidence: false`) y un
gasto con `task_id`, el `contract_id` de la tarea (o solo `customer_id` si no tiene contrato) y
`document_id`. Aprobado al momento: lo apunta quien gestiona. El gasto se ve en la tarea y en su
contrato.

**Fase 3 — desde la app.** La trabajadora fotografía el ticket y pone el importe. Entra como `pending`
y no cuenta hasta que quien gestiona lo aprueba en el panel; rechazado, queda con su motivo. Abre dos
preguntas para Jose antes de hacerla:

1. **¿Reembolso?** Si lo pagó ella de su bolsillo, eso es una nota de gastos (devolverle el dinero), un
   módulo aparte. Recomendación: no meterse; aquí el gasto es coste del cliente, no una deuda con la
   persona.
2. **¿Leer el importe del ticket con la IA?** Encaja con la lectura de PDF de contratos y con el borde
   de anonimización (RGPD). Recomendación: después, cuando haya uso.

El modelo de §3 ya lleva `task_id`, `document_id`, `source` y `status` para que las Fases 2 y 3 no
cambien la tabla.

## 6 bis. Fases 2 y 3: lo decidido (07-nov)

**D1 — reembolso: no.** El gasto es coste del cliente, no una deuda con la persona. No hay «nota de
gastos» ni «pagado por»: si un día hace falta, es otro módulo.

**D2 — la IA lee el ticket: sí.** Como «Leer el PDF» del contrato (`merlin`, `/gpt/contratos/leer`):
ruta nueva `POST /gpt/gastos/leer` con la imagen o el PDF del ticket → `{ concept, amountCents,
spentOn, merchant }` con lo citado del documento, **pasando por el borde de anonimización** (RGPD:
nombres, NIF de personas y matrículas fuera antes de llegar al modelo) y con el aviso de lo que llega
a la IA junto al fichero. Solo rellena el formulario: quien lo sube revisa y guarda. Si no lee nada,
el formulario queda vacío, sin error.

**Quién hace qué.**

| | Panel (Fase 2) | App (Fase 3) |
|---|---|---|
| Quién | propietario y administrador (dinero, TDR-004) | la persona asignada a la tarea |
| Dónde | «Archivos» de la tarea: «Añadir gasto» | detalle de la tarea: «Añadir gasto» |
| Fichero | opcional (adjunto de la tarea, `isEvidence: false`) | **obligatorio**: foto del ticket o PDF |
| Estado al guardar | `approved` | `pending` |
| Ve | todos los gastos de la tarea | los suyos, con su estado (y el importe que puso) |

**Aprobar.** Los `pending` los aprueba o rechaza (con motivo) **propietario o administrador** en el panel:
en la tarea y en un bloque «Gastos por aprobar» del contrato. Hasta aprobarse no cuentan en nada. Inicio
avisa: alerta `expenses_pending` «{n} gastos de la plantilla por aprobar» (owner/admin). Rechazado, la
persona lo ve con el motivo en la app.

**A qué cuenta.** `task_id` siempre; `contract_id` el de la tarea si lo tiene (y si no, el único
vigente el día del gasto: §6 octies); `customer_id` el de la tarea. Una tarea sin cliente no admite gastos (no hay a quién imputarlos): el botón no sale.

**API (`customers`, que ya es dueño de `customer_expenses`).**

- `GET  /tasks/:taskId/expenses?entityId` → los de la tarea (owner/admin: todos; asignada: los suyos).
- `POST /tasks/:taskId/expenses` `{ entityId, concept, amountCents, spentOn?, resourceId? }` →
  owner/admin `approved`; asignada `pending` y `resourceId` obligatorio (el adjunto ya subido por la ruta
  de recursos de la tarea).
- `POST /expenses/:id/approve` · `POST /expenses/:id/reject` `{ reason }` → owner/admin.
- `GET  /contracts/:id/expenses?status=pending` para el bloque del contrato.
- La asignada puede borrar el suyo mientras esté `pending`.

**Contrato de la API de las Fases 2 y 3** (para que API, panel y app vayan en paralelo). Migración
**`061_gastos_desde_la_tarea.sql`**: `customer_expenses` gana `resource_id VARCHAR(64)`,
`rejection_reason TEXT`, `reviewed_by VARCHAR(128)`, `reviewed_at TIMESTAMPTZ` e índice
`(entity_id, task_id)` con `deleted_at IS NULL`.

Un gasto, en toda respuesta: `{ id, concept, amountCents, spentOn, createdAt, status, source, taskId,
contractId, resourceId, createdBy, createdByName, rejectionReason }` (`null` lo que no haya).

- `GET  /api/v1/customers/tasks/:taskId/expenses?entityId` → `{ items, approvedCents }`. Owner/admin:
  todos y `approvedCents`; persona asignada: los suyos y `approvedCents: null`.
- `POST /api/v1/customers/tasks/:taskId/expenses` `{ entityId, concept, amountCents, spentOn?,
  resourceId? }` → 201 el gasto. Tarea sin cliente: 400 `customers/task_without_customer`. Asignada sin
  `resourceId`: 400 `customers/ticket_required`.
- `DELETE /api/v1/customers/expenses/:id?entityId` → 204. Owner/admin cualquiera; la asignada, el suyo
  solo en `pending`.
- `POST /api/v1/customers/expenses/:id/approve` `{ entityId }` · `/reject` `{ entityId, reason }` → 200 el
  gasto. Owner/admin; solo desde `pending`.
- `GET  /api/v1/customers/contracts/:id/expenses?entityId&status=pending` → la página de §4 con los
  items en la forma de arriba. Y `GET /api/v1/customers/expenses/pending?entityId&limit&cursor` → los
  pendientes de toda la empresa (para el panel y la alerta).
- `POST /api/v1/gpt/gastos/leer` (`merlin`) `{ entityId, taskId, resourceId }` → `{ concept?,
  amountCents?, spentOn?, merchant?, quotes: { concept?, amount?, date?, merchant? } }`. Entra la
  persona asignada a la tarea u owner/admin. Por el borde de anonimización; nada se guarda.
- Alerta de Inicio `expenses_pending` `{ count }` (owner/admin).
- El fichero del ticket se sube antes por la ruta de recursos de la tarea, como adjunto
  (`isEvidence: false`), y su `resourceId` va en el `POST`.

**Orden.** API → panel → app (la app, en su próxima versión). La lectura del ticket, a la vez que la API.

## 6 ter. El IVA del ticket y los tickets sueltos (07-nov)

Jose delega la decisión («como tú digas»). Lo decidido:

- **La trabajadora apunta el total del ticket (con IVA)**, que es lo que tiene delante. La lectura con
  IA saca el total y, si viene, la base sin IVA.
- **Lo que cuenta en la rentabilidad es siempre la base sin IVA** (`amount_cents`), como el ingreso.
- Si no hay base (ni leída ni escrita), el gasto se guarda con `amount_cents = total_cents` y
  **`vat_unknown = true`**: en la aprobación se ve «Total del ticket: X €» con la base editable; al
  aprobar con una base, la marca se quita. Un `approved` con `vat_unknown` cuenta su total (mejor que
  no contarlo) y el panel lo enseña marcado.
- **Desde el panel, igual** (Jose, 07-nov: «ponla en el panel también»): en los gastos de la tarea, total del ticket con IVA obligatorio y base sin IVA opcional; sin base, la misma marca `vat_unknown`. Los gastos del contrato (Fase 1) siguen con el importe sin IVA: son facturas de proveedor ya desglosadas.

**Migración `062_gastos_iva.sql`:** `customer_expenses` gana `total_cents BIGINT` (nulo en los del
panel) y `vat_unknown BOOLEAN NOT NULL DEFAULT false`.

**Contrato:**
- El gasto, en toda respuesta, gana `totalCents` y `vatUnknown`.
- `POST /api/v1/customers/tasks/:taskId/expenses`: la asignada manda `totalCents` (obligatorio) y
  `amountCents` (la base) si la tiene; sin base → `amountCents = totalCents`, `vatUnknown: true`.
  Owner/admin, igual que antes (`amountCents`).
- `POST /api/v1/customers/expenses/:id/approve` acepta `{ entityId, amountCents? }`: la base corregida;
  con ella, `vatUnknown` pasa a `false`.
- `gastos/leer` devuelve además `totalCents?` y `baseCents?` (y `amountCents` = la base si la hay, si
  no el total), con sus citas en `quotes.total` y `quotes.base`.

**Tickets sueltos.** El ticket se sube antes de guardar (la lectura necesita el `resourceId`); si la
persona cancela o cambia de ticket, el adjunto quedaba en la tarea y ella no podía quitarlo.
`DELETE /api/v1/customers/tasks/:taskId/tickets/:resourceId?entityId` → 204: lo puede usar quien lo
subió (`uploadedBy` = su empleado) mientras **ningún gasto lo use**; borra el documento del recurso y
su fichero del bucket. Owner/admin, igual. Con un gasto que lo use: 409
`customers/ticket_in_use`. La app y el panel lo llaman al cancelar o al cambiar de ticket.

## 6 quater. El ticket, también como documento «Justificante de gasto» (07-nov)

Jose: «y lo de cargar el ticket también subido como un documento tipo Gastos». El ticket es el
justificante y tiene que quedar con los papeles del cliente aunque se borren los archivos de la tarea.

- **Cuándo:** al pasar a `approved` (al aprobar uno de la app, o al guardar uno del panel con fichero,
  que nace aprobado). Un rechazado no deja justificante.
- **Qué:** `customers` crea en el documental un documento `scope: "customer"` del cliente del gasto, tipo
  nuevo **`customer_expense`** («Justificante de gasto»), `visibleToRoles: ["admin"]` (Administración,
  TDR-002 del documental: lleva importes), título «{concepto} · {total}
  · {fecha}» y descripción con base, total, tarea y contrato. Indexado en `searchIndex` como los demás.
- **El fichero se copia** del adjunto de la tarea a la ruta del documental
  (`…/documents/entities/{entityId}/…`, cuenta en el espacio de la empresa). Copia y no enlace: borrar el
  adjunto de la tarea no se lleva el justificante.
- `customer_expenses.document_id` apunta al documento: la tarjeta del contrato y las listas de gastos
  lo abren.
- **Borrar un gasto aprobado** archiva su justificante (borrado blando del documental), no lo destruye.
  Borrar el contrato, igual que con sus documentos.
- **Gestión documental:** el tipo «Justificante de gasto» en el filtro de tipos del ámbito «Cliente».
  `documents` acepta el tipo nuevo (catálogo de tipos y `CUSTOMER_DOCUMENT_TYPES`); no se crea a mano
  desde «Subir documento»: nace del gasto.
- Va detrás de §6 ter (mismos ficheros).

## 6 quinquies. El gasto del contrato con fichero y lectura, y «Añadir gasto» directo (07-nov)

Jose: «desde gastos del cliente debe poder subirse también el archivo y leerse igual que en la app;
además ponme un botón directo añadir gasto al contrato sin tener que ir a editar».

- **Botón «Añadir gasto» en la tarjeta del contrato** (owner/admin), también con el contrato cerrado:
  abre el mismo diálogo que el de la tarea —fichero opcional (factura o ticket, imagen o PDF), «Leer el
  ticket», total con IVA, base sin IVA, concepto, fecha— con el aviso de la IA. El editor de Editar
  sigue, pero ya no es el único camino.
- **El fichero, directo al justificante.** Un gasto del contrato no tiene tarea a la que adjuntarlo:
  - `POST /api/v1/customers/contracts/:id/expense-receipts` (multipart `file`, `entityId`) → 201
    `{ documentId }`: crea en el documental el documento `customer_expense` del cliente del contrato
    (Administración, la ruta y la forma del §6 quater) con título provisional «Justificante de gasto».
    Mismos límites de fichero que el documental (tipo y tamaño); el espacio lo cuenta el trigger.
  - `DELETE /api/v1/customers/contracts/:id/expense-receipts/:documentId?entityId` → 204: borra
    documento y fichero **solo si ningún gasto lo usa** (409 `customers/receipt_in_use`). Lo llama el
    diálogo al cancelar o al cambiar de fichero.
- **Leer:** `POST /api/v1/gpt/gastos/leer` acepta también `{ entityId, documentId }` (sin `taskId`), solo
  owner/admin, y lee ese documento por el mismo camino (PDF con texto, u OCR + borde en las fotos).
- **Guardar:** `POST /contracts/:id/expenses` acepta `documentId?`, `totalCents?` y `amountCents?` con la
  misma regla de IVA que la tarea (§6 ter): con total y sin base → `vatUnknown`. Si lleva `documentId`, el
  justificante pasa a su título y descripción definitivos (§6 quater). `PATCH` del gasto **reescribe el
  título y la descripción** de su justificante (también arregla los de la tarea). Borrar el gasto archiva
  el justificante, como ya hace.
- Las listas de gastos del contrato enseñan el enlace «Justificante» cuando hay `documentId`.

## 6 sexies. La foto que no se lee bien, y leer no bloquea (07-nov)

Una foto real de un ticket arrugado salió a 100 € (lo entregado en efectivo) en vez de 75,30, y
después a 6,84 (la cuota del IVA): con un OCR así de malo, ninguna instrucción al modelo evita una
cifra falsa. Jose: «¿no puedes identificar si a la foto le falta calidad y descartarla?» y «que no
se lea desde la foto no impide que se suba el gasto; mientras se lee no debe bloquear».

**Calidad.** Tesseract devuelve la seguridad de cada palabra. La foto es de **baja calidad** si la
seguridad media es < 70, si menos de la mitad de las palabras tiene ≥ 80, o si más de un 8 % de los
caracteres es basura (constante `CALIDAD` en `merlin/.../gastos/infrastructure/ocr.ts`). Medido en
el contenedor: tickets legibles 85–92 / 76–100 % / ≤ 2 %; la foto de Jose 49 / 14 % / 11,8 %.

**Contrato de `POST /api/v1/gpt/gastos/leer`** (mismo cuerpo y credenciales que en §6 bis):

| Caso | HTTP | Cuerpo |
|---|---|---|
| Foto de baja calidad | 200 | `{ "quotes": {}, "quality": "low" }`: sin datos, el modelo no se llama |
| Foto leída | 200 | los campos leídos + `"quality": "ok"` |
| PDF | 200 | los campos leídos, sin `quality` |
| Nada que leer (sin ticket, HEIC, sin OCR) | 200 | `{ "quotes": {} }` |
| Permisos o recurso | 400/403/404 | como antes |

**Panel y app.** Leer es una ayuda, nunca un paso obligado, pero **mientras lee, el diálogo entero se
desactiva**: campos, Guardar, Cancelar y cambiar o quitar el ticket (Jose, 07-nov: «que no quede
basura» y «tampoco escribir en los campos, si no es un caos»). La lectura rellena lo que sigue vacío. Al terminar —aunque falle, se agote la espera (30 s en
la app) o llegue `quality: "low"`— se reactivan y el gasto se apunta a mano. Con `quality: "low"`, aviso («La foto no se lee bien. Escribe los datos a mano
o haz otra foto…; el fichero se guarda igual como justificante») y **no se exige otra foto**: el
ticket sigue valiendo como justificante. Defensas añadidas en el parser: una cita de caja (entrega,
efectivo, cambio, devolución, propina, tarjeta) o con dos importes nunca vale como total; sin total
legible, total = base + cuota; si no cuadran, vacío.

## 6 septies. La lectura del ticket con IA, descartada (07-nov)

Jose, tras probar con dos fotos reales —un ticket de súper arrugado (salió a 100 € y luego a 6,84 en
vez de 75,30) y un justificante de tarjeta nítido (descartado por calidad: el OCR no lee bien la letra
de los datáfonos)—: «descarta esta funcionalidad, solo provoca inseguridad»; «que suba la foto y
pongan los datos a mano, tampoco son muchos, son dos y punto»; y sobre el código: «déjalo en la API».

- **Panel y app:** sin «Leer el ticket», sin avisos de IA ni de calidad, sin citas. El fichero (foto o
  PDF) se sube igual como justificante; concepto, total con IVA, base opcional y fecha, a mano.
  Panel: `b6134149` (fuera también el proxy `gastos_leer` y su variable). App: la sesión de la app.
- **API:** `POST /api/v1/gpt/gastos/leer`, el OCR y Tesseract en la imagen de `merlin` **se quedan**,
  sin nadie que los llame. Si un día se retoma, el camino que falta es un lector mejor que Tesseract
  para fotos reales, no más reglas sobre su texto.
- Quedan sin efecto D2 y las partes de lectura de §6 bis, §6 ter, §6 quinquies y §6 sexies; el resto
  (IVA, justificante, gastos del contrato con fichero) sigue.

## 6 octies. El gasto sin contrato (08-nov)

**Lo observado.** En staging (Cuidama), una tarea a la que se puso cliente desde el panel y su gasto
desde la app quedaron sin contrato: el único contrato del cliente empieza el 16-nov y la tarea y el
gasto son del 08-nov. La regla de la tarea (`resolveTaskContract`, TDR-004) acertó: ese día no había
contrato vigente. Lo que fallaba es que un gasto sin contrato **no se veía en la ficha del cliente**:
la ficha solo enseñaba gastos dentro de la tarjeta de cada contrato. Se veía en la tarea, en el aviso
`expenses_pending` de Inicio (el pendiente) y contaba en el Análisis (que suma por `customer_id`).

**Lo decidido.**

- **El contrato del gasto.** El de la tarea si lo tiene; si no, el único contrato activo del cliente
  vigente el **día del gasto** (`spent_on` a las 00:00 UTC, con la regla de la tarea; el fin es el último
  día incluido). Con varios o ninguno, sin contrato: no se adivina. No se escribe en la tarea: el
  contrato de la tarea es de la tarea. Al crear el gasto (`POST /tasks/:taskId/expenses`) y nada más.
- **Un contrato que aún no ha empezado no se asigna**, ni a la tarea ni al gasto, ni por script.
- **«Gastos sin contrato» en la ficha del cliente** (Detalle, debajo de Contratos), solo
  propietario y administrador: todos los gastos del cliente con `contract_id` nulo, en cualquier estado,
  con Aprobar/Rechazar en los pendientes, enlace a su tarea y el total aprobado. Si no hay ninguno, el
  bloque no sale.
  `GET /api/v1/customers/:customerId/expenses/without-contract?entityId&limit&cursor` →
  `{ items, nextCursor, totalCents, count, pendingCount }` (`totalCents`/`count`: aprobados).
- **«Asignar a contrato»** (Jose, 08-nov: «un justificante asignado a un cliente debes poderlo
  asignar a un contrato, ya que queda en el aire»). En cada gasto de «Gastos sin contrato» y en cada
  gasto de la tarjeta de un contrato (para cambiarlo de contrato o quitarlo). Elige entre los contratos
  activos del cliente, **los vigentes el día del gasto primero**; los no vigentes salen detrás marcados
  «fuera de vigencia». Se deja elegir uno no vigente porque lo elige una persona que sabe por qué
  (como el contrato de la tarea, TDR-004, y como `POST /contracts/:id/expenses`, que admite contratos
  cerrados porque un gasto llega tarde); lo automático nunca lo hace. Un cerrado se puede elegir desde
  la API (llega tarde), pero el selector solo ofrece activos.
  `PATCH /api/v1/customers/expenses/:id/contract { entityId, contractId | null }` → 200 el gasto.
  Owner/admin (dinero). 400 `customers/contract_not_of_customer` si el contrato es de otro cliente, 404
  `customers/contract_not_found`, 409 `customers/expense_changed` si alguien lo movió entre medias (la
  condición va en el `UPDATE`). El estado no cambia (un pendiente sigue pendiente, ahora en «Gastos por
  aprobar» de ese contrato); desde ahí sale en la lista del contrato y cuenta en su coste
  (`totalUpTo`). El justificante (`document_id`) no se toca: sigue ligado, y se le reescribe el título
  con el contrato nuevo. Historial: `contract_events` `expense_assigned` en el contrato que lo recibe y
  `expense_unassigned` en el que lo pierde, con el gasto en el valor (sin migración: `type` es texto
  libre).
- La tarea con cliente puesto después ya tomaba el único contrato vigente al guardarse (`services/tasks`,
  crear y editar, panel/MCP/app por la misma API). No se re-resuelve al mover la tarea de fecha ni al
  editar otra cosa: no hay forma de distinguir «sin contrato porque no había» de «se lo quitaron».
- Arreglo de datos: `services/customers/src/scripts/link-task-contracts.ts --entity <id> [--apply]`
  aplica esta misma regla a las tareas y gastos sin contrato que ya existan. Para Cuidama no cambia
  nada.

## 7. Pruebas

- Bon Preu: tres gastos (subcontrata 1 200 €, maquinaria 300 €, parking 45 €) en octubre → el coste de
  octubre del análisis sube 1 545 € y el margen baja; la tarjeta del contrato enseña «Gastos externos:
  1 545 €» y los tres.
- Siete gastos: la tarjeta enseña 5 y «Cargar más» trae los otros 2.
- Editar: añadir, cambiar el importe y borrar un gasto, cada uno se guarda solo.
- Un gerente: ni la lista ni el total, y `POST` le da 403.

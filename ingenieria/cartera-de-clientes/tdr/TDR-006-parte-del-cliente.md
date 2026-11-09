# TDR-006 — El cliente en los análisis: el parte, la pestaña «Análisis», el resumen de Inicio y las alertas

**Fecha:** 2026-11-07
**Estado:** decidido por Jose el 2026-11-07 («es uno de los pluses que más van a convertir», «dale caña»; «que entren alertas y el resumen en inicio además del detalle en la ficha»; «dos tabs al cliente como el resto, el de detalle y el de análisis»). API en staging el mismo día (`1d7eac5` + fix; 059 aplicada en staging), panel `da45c4e8` en `feat/cliente-en-analisis` sin juntar. Pase en §49.
**Componente:** `migrations/059`, `services/tasks` (espejo), `services/customers` (espejo de clientes), `services/reports` (parte), `services/analytics` (análisis, Inicio, alertas); panel (ficha con pestañas, Inicio, Informes)
**Retoma:** la Fase 3 de [05](../05_fases.md), aplazada porque el fichaje va por sucursal. El parte no lo necesita: sus horas salen de las tareas, que sí llevan cliente.

---

## 1. Para qué

La pregunta que hoy nadie contesta sin una tarde de Excel: **«¿qué le he hecho este mes a este
cliente?»**. Vincular clientes a las tareas tiene que devolver algo desde el primer mes, y lo
que devuelve es el parte: con él se justifica la factura y se cierra un «no vinisteis el martes»
con pruebas. La empresa se lo manda a su cliente. Es también la base del portal del cliente
(Fase 6): el portal es este parte visto por el cliente.

## 2. Lo que lleva

Un parte por **cliente y periodo** (por defecto, el mes anterior), opcionalmente de un lugar del
cliente.

- **Cabecera:** la empresa (nombre y logo si lo tiene), el cliente, su dirección, el periodo y la
  fecha de emisión.
- **Resumen:** tareas hechas de las programadas, horas trabajadas, personas distintas,
  evidencias. Si hay contrato vigente con horas previstas: horas del contrato en el periodo.
- **Una fila por tarea:** fecha, tarea, lugar, quién (nombre de las personas asignadas), hora de
  inicio y de fin, horas trabajadas (inicio→fin menos pausas, como el informe de tareas), estado
  y nº de evidencias. Las canceladas salen aparte, al final, como «Canceladas», para que el
  cliente vea lo que se movió y no parezca que se escondió.
- **Fotos (solo PDF):** las evidencias de imagen, en miniatura bajo su tarea: hasta 3 por tarea y
  100 por parte, redimensionadas a ~800 px y JPEG; si hay más, «y N más». Así el PDF se puede
  mandar por correo. Sin `sharp` en la imagen de Docker no se meten fotos y el parte sale igual.
- **Material**, solo si la empresa tiene inventario: lo que se gastó en cada tarea, reutilizando
  `TaskReportMaterial`.
- **No lleva** costes, precios ni márgenes: el parte es para mandarlo al cliente. El dinero se ve
  en la ficha (TDR-004), no aquí.

El **Excel** lleva las mismas filas, una por tarea, más una hoja «Personas» (horas por persona) y,
con inventario, «Material». Es para trabajarlo: facturar, cuadrar.

## 3. De dónde sale: Postgres

Todo del espejo, como el informe de tareas (`PostgresTaskReportClient`):

- **Migración `059_cliente_en_tasks_raw.sql`:** `tasks_raw.customer_id VARCHAR(64)` y
  `customer_site_id VARCHAR(64)`, con índice `(entity_id, customer_id, due_at)` donde
  `customer_id IS NOT NULL AND deleted_at IS NULL`. Hoy el espejo guarda el contrato pero no el
  cliente.
- `TaskPgMirror` escribe las dos columnas; `backfill-tasks --apply` rellena lo que ya existe.
- El periodo se aplica a la **fecha prevista** (`scheduled_start_at`, y `due_at` si no la hay):
  el parte cuenta lo que tocaba hacer en el periodo.
- Nombres de personas y sucursales, de las dimensiones (`dim_employees`, `dim_branches`); el
  cliente y su dirección, de `customers` en Firestore (una lectura).
- Las fotos: de los recursos de la tarea en Firestore (solo los `isEvidence` de imagen) y el
  fichero de Storage. Es la única lectura por tarea, y solo en el PDF.

## 4. Quién lo saca

- Propietario y administrador: cualquier cliente.
- Gerente y supervisor: los clientes que alcanzan (`canReachCustomer`), y el parte **solo con las
  tareas de sus sucursales**: no ven el trabajo de otra sucursal aunque sea el mismo cliente. Lo
  dice el pie: «Incluye las tareas de: …».
- La plantilla, no.

## 5. Cómo se pide y dónde se guarda

Como el informe de tareas: `POST /reports/customer` (`entityId`, `customerId`, `customerSiteId?`,
`start`, `end`, `format: pdf | xlsx`), genera el fichero, lo sube a
`…/entities/{entityId}/reports/…` (cuenta en el espacio de la empresa) y lo apunta en el
historial de informes. El nombre lo pone el servidor: `Parte {cliente} {AAAA-MM}.pdf`.

## 6. En el panel

- **Ficha del cliente:** botón «Parte del cliente» en la cabecera → periodo (mes anterior por
  defecto, o desde/hasta), lugar si tiene varios, PDF o Excel → descarga.
- **Informes:** «Parte del cliente» junto al resto, con el selector de cliente.

## 7. Orden y pase

1. 059 a mano por SSH (antes de `tasks` y `customers`, que escriben las columnas y la tabla).
2. `tasks` y `customers`; `backfill-tasks --apply` y `backfill-customers --apply` por entidad.
3. `reports` y `analytics`.
4. Panel.

## 8. La ficha del cliente con dos pestañas: «Detalle» y «Análisis»

Como la sucursal y el empleado (`HelpTabs`). **Detalle** es lo que hay hoy (datos, contactos,
notas, contratos, documentos). **Análisis** es nuevo, todo de Postgres, de
`GET /api/analytics/customers/:customerId/overview?entityId&months=6`:

- **Mes a mes** (últimos 6): tareas programadas, hechas, canceladas y sin hacer; horas trabajadas;
  si hay contrato con horas previstas, la línea de lo previsto.
- **Este mes frente al anterior, al mismo día**: tareas hechas y horas, con la variación.
- **Cumplimiento**: de las hechas, cuántas a tiempo y cuántas tarde (`time_compliance_status`);
  tareas vencidas sin hacer.
- **Quién trabaja para él**: personas por horas en el periodo (las cinco primeras).
- **Evidencias**: tareas hechas con y sin evidencia.
- Con el mismo alcance que el parte: gerente y supervisor, solo sus sucursales, y lo dice.
- Sin datos suficientes (menos de un mes con tareas): la frase que lo dice, nada de gráficos vacíos.

## 9. Inicio: resumen y alertas

**Resumen** en Inicio, un bloque «Clientes» si la empresa tiene alguno con tareas este mes, de
`GET /api/analytics/customers/summary?entityId`: los clientes con más horas este mes (cinco), con
su variación frente al mes anterior al mismo día, y cuántos tienen tareas sin hacer. Cada fila
lleva a la pestaña Análisis del cliente.

**Alertas** nuevas en `rules.ts` (las lee el panel y el correo de alertas, ADR-007 de analytics).
Dicen el hecho medible, no la causa:

| Regla | Cuándo | Texto (es) |
|---|---|---|
| `customer_tasks_missed` | tareas de un cliente con fecha límite en los últimos 7 días que no se hicieron (ni hechas ni canceladas) | «{cliente}: {n} tareas de los últimos 7 días sin hacer» |
| `customer_hours_drop` | este mes, al mismo día, ≥30 % menos horas que el anterior, y el anterior tuvo ≥10 h | «{cliente}: {h} h este mes, un {p} % menos que el mes pasado a estas alturas» |
| `contract_hours_over` | contrato vigente con horas hechas por encima de las previstas | «{contrato} ({cliente}): {hechas} h hechas de {previstas} previstas» |
| `contract_ending` | contrato vigente que termina en 30 días o menos | «{contrato} ({cliente}) termina el {fecha}» |

`contract_hours_over` y `contract_ending` hablan de contratos: solo las ven propietario y
administrador (el dinero y los contratos son suyos, TDR-004).

## 10. El espejo de clientes

Hoy Postgres tiene los contratos y no los clientes. La misma `059` crea `dim_customers`
(`customer_id`, `entity_id`, `name`, `kind`, `status`, `scope`, `branch_ids JSONB`,
`updated_at`), que escribe `customers` en la petición, después de Firestore y a mejor esfuerzo
(como `customer_contracts`), y rellena un `backfill-customers` (simula por defecto). La leen el
análisis, el resumen y las alertas para el nombre y el alcance por sucursal.

## 11. Después (no en este TDR)

- Merlin narrando el cliente («qué implica», no lo que se ve).
- Mandar el parte al cliente desde la plataforma (correo con el PDF), y el portal.

## 12. Pruebas

- Cliente de la demo con tareas en noviembre: el parte cuenta las mismas tareas y horas que el
  informe de tareas filtrado a esas tareas.
- Un gerente de Badalona saca el de QA Eventos (Badalona y Madrid): solo salen las de Badalona y
  el pie lo dice.
- PDF con fotos de varias tareas: pesa poco y se abre; sin fotos, igual.
- Empresa sin inventario: ni columna ni hoja de material.
- Pestaña Análisis de QA Eventos: las horas de noviembre cuadran con el parte del mismo periodo.
- Inicio: QA Eventos aparece en el resumen; una tarea suya vencida sin hacer enciende
  `customer_tasks_missed`, y al hacerla se apaga en la siguiente lectura.
- Un gerente no ve `contract_hours_over` ni `contract_ending`.


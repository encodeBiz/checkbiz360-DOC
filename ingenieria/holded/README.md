# Integración con Holded — estudio (RRHH, clientes y márgenes)

**Proyecto:** encodebiz-api
**Dominio:** add-on de integración con Holded (ERP y RRHH para pymes) por su API v2
**Fecha:** 2026-11-23
**Estado:** **Estudio.** Sin decisión, sin cuenta de Holded, sin código. Todo lo que dice de la API
está leído en la documentación pública de Holded el 23-11-2026 (URLs al final); lo que no se ha
podido leer va marcado *a confirmar con la cuenta*.
**Autor:** Jose Acevedo

---

## 1. Qué es Holded y por qué nos interesa

Holded es un ERP español para pymes: facturación, contabilidad, CRM, proyectos e inventario, con un
módulo de **Equipo (RRHH)** que vende fichaje con geolocalización, ausencias y vacaciones, portal del
empleado, documentos del empleado y **nóminas calculadas dentro de Holded** (Gema Nóminas). Sus
clientes son exactamente nuestros nichos: pymes de servicios que ya facturan y llevan la plantilla
en Holded y a las que les falta el control horario serio, con geocerca, tareas y evidencia.

Lo que lo hace distinto de a3innuva, y más fácil:

- **API pública y documentada**, sin partner ni contrato previo. Se accede con una clave de API que
  el propio cliente genera en *Ajustes → API*, con permisos por ámbito (`team:employees.read`,
  `team:time-tracking.write`…). Autenticación `Authorization: Bearer <clave>`.
- **Cuenta de pruebas al alcance**: cualquier plan de pago tiene API (el gratuito *Light* no). Las
  gemas de RRHH se pagan por empleado, así que una cuenta con cinco empleados de prueba cuesta poco.
- La API v1 (`developers.holded.com`) está **retirada**; todo lo nuevo va contra `/api/v2`.
- Tiene **servidor MCP** propio (OAuth 2.1, `mcp.holded.com/mcp`) y su documentación lleva
  instrucciones pensadas para asistentes de IA. Eso no es la integración, pero sí dice que un
  cliente podrá tener en Claude o ChatGPT el conector de CheckBiz y el de Holded a la vez.

Precios públicos a la fecha (sin IVA): planes Starter 19 €, Growth/Basic 34 €, Standard 69 €,
Advanced 115 €, Premium 229 € al mes (mitad el primer año). **Team Pro** (fichajes, ausencias,
portal) 3 € por empleado y mes; **Nóminas** 5 € por empleado y mes desde Growth/Basic.

## 2. Lo que la API permite (verificado)

### 2.1 Equipo / RRHH

| Recurso | Qué hay | Lo que importa para nosotros |
|---|---|---|
| **Empleados** `/api/v2/employees` | listar (con `search` por nombre, correo y código), leer, crear (`name`, `last_name`, `email` obligatorios; `code`, `social_security_number`, `workplace_id`, `team_ids`, `iban`…), actualizar datos personales, borrar | La ficha trae `current_contract` con `job_title`, `schedule_hours`, `salary`, `salary_interval`, `salary_payments`, `start_date`/`end_date`; `terminated`; `fiscal_address.id_number` (el NIF). El correo es único: crear uno repetido da 409 |
| **Contrato activo** `/employees/{id}/contract` | leer y **reemplazar entero** (`contractType` SEPE, `startDate`, `jobTitle`, `professionalCategory`, `scheduleHours`, `scheduleMode`, `workingDays`, `vacationDays`, `salary`, `salaryInterval`, `salaryPayments`, `workModality`) | Aquí está el puesto y el salario bruto **sin leer ningún PDF** |
| **Fichajes** `/employee-times`, `/employees/{id}/times` | listar todos o por empleado (`start_at`, `end_at`, `duration` en segundos, `status` running/done, `approved`), **crear una jornada cerrada con pausas**, editar, borrar; y en vivo `clock-in`, `clock-out`, `pause`, `resume` con latitud/longitud | Es la pieza de salida. Las horas van **en hora local de la cuenta y sin zona** (`2026-03-01T09:00:00`); una jornada futura o que solape con otra da 422 y no se reintenta |
| **Ausencias** `/employees/time-offs`, `/employees/{id}/time-offs` | listar con **rango de fechas obligatorio** (`status` pending/accepted/rejected/cancelled, `time_off_type_id`, `team_id`), crear (tipo, fechas, medio día u horas, motivo), **cambiar solo la fecha de fin** | No se aprueba ni se rechaza por API. Los **tipos de ausencia no se listan** por API: el `time_off_type_id` solo se aprende de las ausencias existentes |
| **Nóminas** `/payslips` | listar (`net_salary`, **`total_company_cost`**, `period_start/end`, `payslip_kind`, `is_draft`, `payment_status`), crear en lote por periodo (asíncrono, **sin confirmación y no idempotente**), aprobar, pagar, PDF | Solo existen en cuentas con la Gema de RRHH (402 si no). La nómina la **calcula Holded desde el contrato**: **no hay API para cargar horas extra, pluses ni incidencias variables** |
| **Registros salariales** `/salary-records` | el asiento contable manual de la nómina (cuatro líneas: salario, S.S., gasto S.S. empresa, IRPF) | Es contabilidad de la gestoría, no RRHH. Fuera |
| **Cuentas de partner** `/partner/accounts` | lista las cuentas cliente a las que accede una cuenta de asesoría | Para una gestoría que lleve varias empresas con un solo token. *A confirmar*: si lo pueden usar terceros o solo asesorías del programa |

Lo que **no** hay: endpoints de centros de trabajo (`workplace_id`), equipos (`team_ids`) ni tipos
de ausencia (son identificadores opacos); aprobar fichajes o ausencias; webhooks de nada de RRHH.

### 2.2 Clientes, facturas y proyectos

| Recurso | Qué hay | Lo que importa |
|---|---|---|
| **Contactos** `/contacts` | listar con filtro exacto por **`code` (NIF/CIF)**, `email`, `custom_id` (nuestra referencia); `type` client/supplier, `trade_name`, dirección de facturación, condiciones de pago; crear y editar | Emparejar nuestro `Customer.taxId` con `contact.code`, y guardar nuestro `customerId` en `custom_id` |
| **Facturas** `/invoices` | listar por `contact_id`, fecha de emisión o vencimiento, `status` (pending, partial, **outstanding, overdue**, completed), con `payments_total` y `payments_pending`; crear, aprobar, enviar, PDF | **Lo facturado de verdad a cada cliente y lo que debe.** Esto es lo que hoy nos falta en el margen |
| **Compras** `/purchases` | listar por proveedor, fechas y estado de pago | Candidatas a *gastos externos* del contrato (TDR-008) |
| **Proyectos** `/projects` | listar con `contact_id`, `billable`, estado; resumen; **tiempos de proyecto** con coste tomado de la configuración del proyecto y `user_id` de Holded | Es otro modelo (usuario de Holded, no empleado). Se queda fuera |
| **Servicios** `/services` | catálogo de servicios con precio | Para una futura línea de factura |

### 2.3 Límites y mecánica

- **Cuota por plan y por cuenta**, compartida por todas las claves y por sus asistentes de IA:
  Starter 500 llamadas al mes, Growth/Basic 2 000, Standard 7 500, Advanced 30 000, Premium 100 000
  (con exceso facturado). Ráfaga de 60 a 600 por minuto. Al pasarse, 429 con `Retry-After` y
  `X-RateLimit-Remaining`. **Es la restricción de diseño más seria** (§5).
- Paginación por cursor (`items`, `cursor`, `has_more`), hasta 200 por página en Equipo.
- Errores en formato *problem+json*; 400 y 422 son un «no» definitivo, 429 y 5xx se reintentan.
- **Webhooks** firmados (HMAC-SHA256) pero solo para documentos comerciales, contactos, productos y
  stock. Para RRHH, **sondeo**, que es lo que ya hacemos (`integraciones/README.md` §5).

## 3. Dónde está el valor, y qué recomiendo

> **CheckBiz mide y manda los hechos; Holded administra y factura.** Igual que con a3 y Rentman: del
> core se lee, el adaptador absorbe todo, y nunca se escribe en Holded lo que una persona no ha
> aprobado.

### Eje RRHH

**A. Las jornadas cerradas, de CheckBiz a Holded** (`checkbiz_authority`, como en Rentman). Cada
jornada validada de `employee_daily_reports` (la misma tabla que el informe legal) se crea como
*time entry* con sus pausas. Quien lleve la plantilla en Holded ve las horas donde ya mira, y la
nómina o la exportación a la gestoría salen de ahí. Condición de uso: **en Holded no se ficha**;
si el empleado también ficha en su portal, Holded rechaza por solape y la jornada queda como
divergente, exactamente como con Rentman. Es la primera capacidad y la que vende el add-on.

**B. Los empleados y su contrato, de Holded a CheckBiz.** Holded suele ser el maestro
administrativo. Importar fichas (nombre, correo, código, NIF, puesto) crea empleados con
`metadata.source` como ya hace Rentman, en `pending` si falta el correo. Y el **contrato activo nos
da el puesto y el salario bruto** para `job` y `price` de la responsabilidad, que es justo lo que
hoy intentamos sacar leyendo el PDF del contrato con el modelo: con Holded, para ese cliente,
**no hace falta el PDF**. La conversión a bruto por hora es la misma regla que ya existe
(salario, pagas, horas semanales).

**C. Ausencias.** Primero **leer** las aceptadas de Holded, para que el cuadrante y la
disponibilidad las conozcan sin volver a teclearlas. Después, si se quiere, crear en Holded la
que se aprueba en nuestro panel. Hace falta una **pantalla de correspondencias de tipos**
(nuestros `vacation/personal/medical/other` ↔ sus `time_off_type_id`), aprendidos de las ausencias
que ya tenga la cuenta, porque no hay endpoint para listarlos. Mismo patrón que TDR-003 de a3.

**D. Nómina: no se manda nada.** No hay API de variables y la nómina la calcula Holded desde el
contrato. Lo que sí se hace es **leer** las nóminas: `total_company_cost` por persona y mes es el
**coste real** del empleado, mejor que el precio por hora estimado. Eso alimenta directamente la
rentabilidad (§Eje clientes), y es lo que convierte un «coste estimado» en «coste según nómina».

### Eje clientes y márgenes

**E. La cartera, emparejada con los contactos.** `Customer.taxId` ↔ `contact.code`; importar los
contactos de tipo cliente que falten y escribir nuestro `customerId` en `custom_id` para que el
vínculo sobreviva a cambios de nombre. Dirección de facturación y condiciones de pago, de Holded.

**F. El margen con ingreso real.** Hoy el análisis del cliente (TDR-007) reparte el importe del
contrato por días porque es lo que tenemos. Con Holded, el ingreso del mes es **lo facturado a ese
contacto en ese mes**, y aparece además lo **pendiente de cobro y vencido**: un cliente que deja de
pagar es la señal de «puede estar cambiando de proveedor» que Jose pedía. Margen real = facturado −
(horas × precio o coste según nómina + material + gastos externos). Esto no toca el core: el add-on
expone sus cifras y el panel enseña una tarjeta «Según Holded» en la pestaña Análisis solo cuando
el add-on está conectado.

**G. Gastos externos desde compras.** Las compras de Holded con el proveedor o la etiqueta del
cliente se **proponen** como gastos externos del contrato (TDR-008), y una persona los acepta. Nunca
se imputan solos: una compra general no es de un cliente.

**H. Preparar la factura en Holded.** ADR-004 dice *valorar, no facturar*, y sigue en pie: nosotros
no emitimos facturas. Pero Holded sí, y el parte del cliente (TDR-006) tiene todo lo que lleva una
línea de factura. Crear en Holded un **borrador** de factura con las horas e importe del periodo,
que la empresa revisa y aprueba en Holded, respeta la letra del ADR y se come el último tecleo.
**Es una decisión de Jose**, no de este estudio; va en una fase posterior.

**I. Fuera:** proyectos y tiempos de proyecto de Holded (otro modelo, usuario de Holded ≠ empleado),
registros salariales (contabilidad), escribir nóminas, webhooks.

## 4. Encaje con nuestro modelo

| Nuestro dato | Holded | Nota |
|---|---|---|
| `Employee.email` | `employee.email` | Clave de emparejamiento. Único en Holded |
| `Employee.nationalId` / `metadata.dni` | `fiscal_address.id_number` | Segunda clave; en Holded puede faltar |
| `Employee.jobTitle`, `price` de la responsabilidad | `current_contract.job_title`, `salary` + `salary_interval` + `salary_payments` + `schedule_hours` | Bruto por hora derivado, marcado «según contrato de Holded» |
| `Employee.status` (`fired`, bajas) | `terminated`, `terminated_type` | Solo lectura; la baja en CheckBiz sigue siendo una decisión nuestra |
| Jornada de `employee_daily_reports` (entrada, salida, descanso) | `POST /employees/{id}/times` con `pauses` | Convertir de UTC a la **zona horaria de la cuenta de Holded** y mandar sin offset. *A confirmar*: si `GET /account` devuelve la zona; si no, se configura al conectar |
| `absence_requests` (`type`, fechas, `status: approved`) | `time-offs` (`time_off_type_id`, `start_date`, `end_date`, `status: accepted`) | Días enteros y medios días; nuestras ausencias no tienen horas, las suyas sí |
| `Customer.taxId`, `Customer.id` | `contact.code`, `contact.custom_id` | Filtro exacto en la API |
| Ingreso del contrato repartido (TDR-007) | `invoices` por `contact_id` y mes, `payments_pending` | Se enseña al lado, no en lugar de: si no hay factura no hay cero |
| Gasto externo (TDR-008) | `purchases` | Propuesta, nunca automático |
| Coste de personal (horas × `job_price`) | `payslips.total_company_cost` | Coste real cuando hay nómina en Holded |

## 5. Arquitectura propuesta

Microservicio propio **`services/holdedbiz`** (addonId `holdedbiz`, puerto siguiente libre del
compose, a confirmar), siguiendo al pie de la letra `integraciones/contrato-activacion.md`:

- **Activar → conectar**: el cliente genera en Holded una clave con los ámbitos justos
  (`team:employees.read`, `team:time-tracking.write`, `team:time-off.read/write`,
  `accounting:payrolls.read`, `contacts:contacts.read`, `sales:invoices.read`,
  `accounting:purchases.read`) y la pega en el panel. Se valida contra `GET /api/v2/employees?limit=1`
  antes de cifrarla con `ENC_KEY`. Si falta un ámbito, el 403 lo dice y se le enseña cuál.
- **Emparejamientos**: empleados por correo, clientes por NIF, tipos de ausencia a mano. Con
  revisión antes de confirmar (vista previa, como la alta masiva del conector).
- **Sondeo con presupuesto**: la cuota mensual es **del cliente y compartida** con sus otras
  integraciones. Una empresa de 30 personas que mande cada jornada gasta unas 660 llamadas al mes
  solo en fichajes; en Starter (500) no cabe, en Standard (7 500) sobra. El add-on tiene que **leer
  `X-RateLimit-Remaining`, reservarse un tope configurable** (por ejemplo, no pasar del 40 % de la
  cuota) y **enseñar al cliente lo que consume**; agrupar por jornada cerrada, nunca fichaje a
  fichaje; leer facturas y nóminas una vez al día, no por pantalla.
- **Idempotencia por huella** (`pushed_hash` de entrada, salida y pausas), un «no» definitivo en
  422 (`skipped`, con el motivo), divergencia cuando Holded ya tiene otra cosa.
- **Tablas `holdedbiz_*`** en migración propia: `employee_mapping`, `customer_mapping`,
  `time_off_type_mapping`, `time_entry`, `time_off`, `invoice_month` (ingreso y pendiente por
  cliente y mes), `payslip_cost` (coste por persona y mes), `sync_log`.
- **Del core solo se lee**: `employee_daily_reports`, `absence_requests`, `customers`,
  `customer_contracts`, `dim_responsibilities`. El análisis del cliente **no** lee tablas del add-on;
  el add-on expone `GET /api/v1/holdedbiz/customers/{id}/summary` y el panel lo pinta aparte.

## 6. Fases, de lo más usado a lo menos

**Fase 0 — la cuenta y las dudas (1–2 días).** Contratar Holded Standard (34,50 €/mes el primer
año) con Team Pro y Nóminas para cuatro o cinco empleados ficticios. Comprobar la lista del §8.
Sin esto no se diseña en firme nada de lo que sigue.

**Fase 1 — RRHH.** Conexión y catálogo; emparejar e importar empleados con puesto y salario;
**jornadas cerradas a Holded**; leer ausencias aceptadas. Es lo que se enseña y lo que se cobra.

**Fase 2 — clientes y márgenes.** Emparejar clientes; **ingreso facturado y cobro pendiente** en el
análisis del cliente; coste real desde nóminas. Aquí el add-on deja de ser «ahorrar tecleo» y pasa a
«saber si el cliente es rentable con cifras de verdad».

**Fase 3 — si se decide.** Ausencias hacia Holded; compras como gastos externos propuestos; borrador
de factura en Holded desde el parte del cliente (decisión sobre ADR-004).

**Fuera:** nómina (sin API de variables), proyectos de Holded, registros salariales.

## 7. Modelo de negocio (para que lo decida Jose)

Como Rentman y a3: **add-on de pago**, el cliente paga su Holded y pone su clave. Sin coste de
partner ni de API por nuestra parte, así que la cuenta sale mejor que con a3 (donde asumimos
Conectia). Referencia: a3 se pensó a 20–25 € al mes por empresa. La cartera de clientes sigue siendo
core gratuito (ADR-001 de cartera); lo que se cobra es la conexión, con las dos capacidades dentro
del mismo add-on y cada una con su `status` en el catálogo.

Para venderlo conviene mirar el **directorio de integraciones** y el programa de *Solution Partners*
de Holded (hay partners que publican integraciones por API); el proceso de aparecer ahí no está
documentado en público y hay que preguntarlo.

## 8. Lo que hay que verificar con la cuenta

1. **Zona horaria**: si `GET /api/v2/account` (grupo *account*) devuelve la zona de la cuenta, para
   convertir nuestras horas UTC; si no, se pide al conectar.
2. **Contrato activo**: los campos reales de `GET /employees/{id}/contract` (la doc enseña `{}`), y
   si una cuenta sin Team Pro tiene contrato.
3. **Fichajes**: si una *time entry* creada por API nace `approved`; si acepta pausas múltiples; si
   `date` y `start_at` pueden diferir (jornada nocturna); qué pasa con una jornada de más de 24 h.
4. **Ausencias**: cómo descubrir los tipos (`time_off_type_id`) de una cuenta nueva sin ausencias;
   si se puede crear ya `accepted` o nace `pending` y alguien la aprueba en Holded.
5. **Cuota**: cómo se reparte entre nuestras llamadas y las del propio cliente; si `X-RateLimit-*`
   viene en cada respuesta y no solo en el 429.
6. **Partner**: si una cuenta normal puede acceder a `/partner/accounts`, para gestorías.
7. **Nóminas**: que `total_company_cost` esté en nóminas aprobadas de meses cerrados y qué devuelve
   en una cuenta sin la gema.
8. **Contactos**: que `custom_id` sea escribible desde `PUT /contacts/{id}` y filtrable como dice la doc.

## 9. Decisiones que son de Jose

1. **Política de fichaje**: con el add-on, ¿en Holded no se ficha? (Recomiendo que sí: una sola
   fuente, la nuestra, como con Rentman.)
2. **Borrador de factura en Holded**: ¿se abre esa puerta o ADR-004 se queda como está?
3. **Alcance de la primera entrega**: ¿solo RRHH, o RRHH y clientes a la vez? (Recomiendo RRHH
   primero, con clientes a las pocas semanas: la segunda fase reutiliza la conexión entera.)
4. **Precio** del add-on.
5. **Contratar la cuenta de Holded** para la Fase 0.

---

## Fuentes (leídas el 2026-11-23)

- Portal de desarrolladores: https://www.holded.com/developers/getting-started ·
  https://www.holded.com/developers/authentication · https://www.holded.com/developers/rate-limiting ·
  https://www.holded.com/developers/pagination · https://www.holded.com/developers/errors ·
  https://www.holded.com/developers/webhooks · https://www.holded.com/developers/v1 (v1 retirada) ·
  https://www.holded.com/developers/mcp
- Equipo: https://www.holded.com/developers/api-reference/employees/list-all-employees ·
  …/employees/create-an-employee · …/employees/update-an-employee · …/employees/get-active-contract ·
  …/employees/update-active-contract ·
  https://www.holded.com/developers/api-reference/employee-time-tracking/list-all-employee-time-entries ·
  …/employee-time-tracking/create-a-time-entry-for-an-employee · …/employee-time-tracking/clock-in-an-employee ·
  …/employee-time-tracking/pause-an-employee-time-session ·
  https://www.holded.com/developers/api-reference/time-off/list-all-time-off-requests-absences-holidays ·
  …/time-off/create-a-time-off-request-absence-holiday · …/time-off/update-time-off-end-date-absence-holiday ·
  https://www.holded.com/developers/api-reference/payslips/list-payslips · …/payslips/create-payslips-in-bulk ·
  https://www.holded.com/developers/api-reference/salary-records/create-a-salary-record ·
  …/salary-records/get-salary-record-form-data ·
  https://www.holded.com/developers/api-reference/partners/list-client-accounts-accessible-to-the-partner
- Clientes: https://www.holded.com/developers/api-reference/contact/list-contacts ·
  https://www.holded.com/developers/api-reference/invoices/list-invoices ·
  https://www.holded.com/developers/api-reference/purchases/list-purchases ·
  https://www.holded.com/developers/api-reference/projects/list-projects ·
  …/project-time-tracking/create-a-time-entry-for-a-project · …/services/list-services
- Precios y producto: https://www.holded.com/es/precios · https://www.holded.com/es/gestion-de-recursos-humanos ·
  https://www.holded.com/llms.txt (planes, cuotas de API y precio de las gemas) ·
  https://www.holded.com/es/solution-partners · https://www.holded.com/es/directorio-solution-partners
- Centro de ayuda (citado por el asistente público de Holded): generar y usar la API
  (help.holded.com/es/articles/6896051), programa de partners (…/7040649), tipos de ausencia
  (…/12959535), centros de trabajo (…/9991873), equipos (…/9991876), FAQ de la gema de Nóminas (…/13938214).

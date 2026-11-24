# TDR-010 — Varios puestos por persona y complementos en la tarea y el turno, con el coste desglosado

**Fecha:** 2026-11-24
**Estado:** Diseño aprobado (Jose, 2026-11-24). **Construido y en `develop` el 24-nov-2026:** API `encodebiz-api` a0eddd8 (fases 1, 2 y 4; con la moneda de la empresa fusionada) y panel `encodebiz-front-saas` 7ead315f (fase 3). Tests y typecheck en verde. **Sin pasar a staging**: hacen falta las migraciones 071 y 072 a mano y el guion de QA §10 con SaludStart o Cuidama. Panel: dar de alta `NEXT_BACKEND_URI_CHECKINBIZ_SUPPLEMENTS_HANDLER` en los entornos. **Manual de clientes escrito el 24-nov** (`DOCS/Clients/02-empleados/140` y `141`, más 48, 41, 114, 61 y otros; en/pt): se publica con el pase a producción. Campaña in-app redactada; la crea Jose en backoffice.
**Componente:** `encodebiz-api` — `@encodebiz/shared`, `checkinbiz` (fichaje), `tasks`, `reports`, `customers`, `analytics`, `assistant`, `rentman`, `merlin`, `employees`; panel. La app no cambia.
**Origen:** reunión con un cliente de eventos (23-nov-2026). Decisiones de Jose del 24-nov.

---

## Resumen

Hoy una persona cuesta un único precio por hora en cada sucursal: el `price` del puesto de su
responsabilidad. En eventos, limpieza o SAD la misma persona hace cosas distintas que se pagan
distinto —técnica de sonido un día, conductora al siguiente— y además cobra complementos que el
convenio manda por tarea o por hora: conducción de más de 100 km, festivo, nocturnidad. Nada de
eso se puede registrar, así que el coste que sale en la cartera y en las estadísticas es
aproximado y el informe de tareas no lleva coste de personal.

Se añaden dos cosas pequeñas y aditivas:

1. **Varios puestos por persona en la misma sucursal**, con uno predeterminado. El `job` de
   hoy pasa a ser el predeterminado; todo lo que lo lee sigue igual.
2. **Complementos como «skills»**: un catálogo por empresa (nombre, tipo, valor) que se añade
   una vez y se selecciona después. Tipos: fijo, por hora y porcentaje.

Las dos se eligen en el mismo sitio y de la misma manera: **al asignar una tarea** y **al crear
un turno** (semana tipo, turnos cargados, cuadrante). El fichaje, que ya congela el turno y el
puesto, congela también el puesto elegido y la lista de complementos. Toda la analítica lee del
fichaje, así que informe de tareas, cartera, estadísticas y análisis recogen el precio correcto
y desglosado sin inventar otro camino.

El informe de tareas cambia de unidad: **una fila por tarea y persona asignada**, agrupadas por
tarea, con el coste por persona y sus complementos. Jose: «ahora sí sirve para un contable».

---

## 1. Lo que hay

- **El coste es un número por persona y sucursal.** `EmployeeResponsibility.job: Job {id, job,
  price}` (`packages/shared/src/checkbiz/entities/Employee.ts`), en euros brutos por hora, sin
  Seguridad Social de la empresa. El catálogo de ocupaciones vive en `entities/{e}/jobs`
  (`services/employees/src/application/ocupaciones.ts`): «se toma si existe y se añade si no».
- **El fichaje congela el puesto.** `createChecklog.controller.ts` (`checkinbiz`) hace `pop()`
  de las responsabilidades de la persona en la sucursal y escribe `metadata.employeeResponsibility
  = {...job, responsibility, level}`. El espejo lo saca a `checklogs_raw.employee_price` y
  `employee_responsibility` (`packages/shared/src/mirror/checklogsRaw.ts`). El fichaje manual
  (`RequestManualChecklogCreation.ts`) hace lo mismo.
- **El turno ya lleva la tarea.** `Shift {start, end, taskId?, title?}` (`CheckLog.ts`) es el
  mismo tipo en semana tipo, turnos cargados (`calendar/loadedDays.ts`) y horario por tareas.
  El fichaje congela el turno en `metadata.scheduleApplied` con su `taskId`.
- **La asignación de la tarea no sabe de dinero.** `Task.assignedEmployeeIds: string[]` y un
  documento por persona en `entities/{e}/tasks/{t}/assignments/{employeeId}` (`TaskAssignment`:
  estado, fechas, notas). No hay espejo de asignaciones en Postgres.
- **El coste de personal se calcula en tres sitios**, todos desde el fichaje: día operativo
  (`analytics/.../operational/BuildOperationalDay.ts` → `operational_daily.labor_cost`), coste de
  la jornada (`BuildOperatingCost.ts`) y rentabilidad del contrato
  (`customers/.../profitability/montageCosts.ts`). Este último, para tareas sin fichaje, usa el
  reloj de la tarea × `dim_responsibilities.job_price` **actual**; el análisis del cliente
  (`CustomerInsights.ts`) también usa el precio actual. Es un hueco: el histórico de precios
  existe (`responsibility_events`, migración 050) y no se usa.
- **El informe de tareas** (`reports/.../GenerateTaskReportXLSX.ts`, TDR-004) da una fila por
  tarea, horas de la tarea entera, el equipo concatenado y, con inventario, el coste del
  material. Sin coste de personal.
- **Rentman** trae el coste por hora de cada plaza (`RentmanProjectFunction.hourlyCost`) y lo
  pierde: crea una responsabilidad por sucursal con la primera plaza y no vuelve a tocarla
  (`importCatalogue.ts`, `ensureResponsibility`).
- **Complementos: en ningún sitio.** El lector de contratos laborales los detecta y solo avisa.
  El diseño de a3-nómina los deja para su fase 3 «porque CheckBiz hoy no los registra»
  (`a3-nomina/tdr/TDR-002`, §2), y decide que a la nómina van **unidades, no euros**
  (`a3-nomina/adr/ADR-003`) y que **cada línea sabe de dónde sale** (`ADR-005`).

## 2. Decisiones

### D1. Varios puestos por responsabilidad; `job` es el predeterminado

`EmployeeResponsibility` gana `jobs?: Job[]` con los puestos adicionales, tomados del catálogo
de ocupaciones. `job` no cambia de nombre ni de significado: es el predeterminado, el que se
aplica cuando nadie elige otro. En el panel es una lista dinámica con el mismo selector de
ocupación de hoy y un marcador «predeterminado». Quien no añade segundos puestos no ve nada
nuevo.

### D2. Complementos como skills: catálogo por empresa

Colección `entities/{e}/supplements` (`Supplement`): `name`, `kind: "fixed" | "hourly" |
"percent"`, `value` (importe para fijo y por hora; fracción para porcentaje, `0.25` = 25 %),
`active`. Misma regla que las ocupaciones: se compara en minúsculas y sin tildes, se toma si
existe y se añade si no. Se gestiona en Configuración, junto a las ocupaciones. Sin catálogo,
ni el chip ni las columnas aparecen.

### D3. Dónde se eligen: en la asignación de la tarea y en el turno, con los mismos dos campos

Un turno y una asignación de tarea son la misma cosa: «esta persona va a hacer esto, con estos
extras». Las dos ganan los mismos dos campos opcionales:

- `TaskAssignment.job?: Job` y `TaskAssignment.supplements?: SupplementSnapshot[]`.
- `Shift.job?: Job` y `Shift.supplements?: SupplementSnapshot[]`, y por tanto en semana tipo,
  turnos cargados y cuadrante (dos columnas opcionales en el Excel).

`SupplementSnapshot = {id, name, kind, value}` es una **copia** del catálogo en ese momento, como
`job` es copia de la ocupación: si el catálogo cambia después, lo ya asignado no cambia.

En el panel, en el chip de cada persona asignada: un selector «como: {puesto}» **solo si tiene
más de un puesto**, y «+ complemento» que abre la lista del catálogo. Lo mismo en «Equipo
asignado» de la ficha de la tarea y en el editor de turnos. El gestor elige por nombre; el
importe no lo ve (D10).

### D4. El fichaje congela las partes, no la suma

Al fichar la entrada, el puesto y el precio que se escriben en `metadata.employeeResponsibility`
salen, por este orden: de la asignación de la tarea si el turno viene de una tarea
(`scheduleApplied.source = "tasks"`), del turno si lo dice, y si no, del predeterminado de la
responsabilidad. A su lado se escribe `metadata.supplements: SupplementSnapshot[]` con los del
mismo origen.

`checklogs_raw.employee_price` **conserva su significado**: precio por hora del puesto. Los
complementos van en una columna nueva `supplements JSONB`. No se guarda ninguna suma: un
complemento fijo no es por hora y al fichar la entrada no se saben las horas; y el desglose es
justo lo que se quiere ver y trazar.

Esto se aplica en los tres caminos del fichaje: normal y quiosco
(`createChecklog.controller.ts`), manual (`RequestManualChecklogCreation.ts`) y modo por tareas
(`tasksModeAttendance.ts`, que ya conoce la asignación de la persona).

### D5. Una fórmula, una implementación

```
coste de una sesión = horas × precio_puesto
                    + horas × Σ complementos_por_hora
                    + horas × precio_puesto × Σ porcentajes
                    + Σ complementos_fijos                    (una vez por sesión de fichaje
                                                               o, sin fichaje, por asignación)
```

Vive en **un solo sitio**, `packages/shared/src/checkbiz/costs/labourCost.ts`, pura y con tests,
y la usan `reports`, `customers` y `analytics`. Hoy cada uno multiplica por su cuenta; con dos
sumandos más eso se desincroniza seguro.

Sin precio de puesto el resultado es `null`, nunca 0 (regla de la casa). Un fichaje sin salida
cuenta las horas pero no se valora, como hoy.

### D6. El informe de tareas pasa a una fila por tarea y persona

Validado con una demo el 24-nov. Descartados: concatenar puesto y complementos en la fila de la
tarea («así no funciona») y una hoja por tarea («hacer cálculos en el Excel se hace imposible»).

**Hoja «Tareas».** Una fila por tarea y persona asignada, **agrupadas por tarea** (outline de
Excel: el «−» del margen pliega el grupo) y con filtro automático en la cabecera. Las columnas
de la tarea se repiten en cada fila para que filtrar por persona siga enseñando la tarea:

| Columna | Origen |
|---|---|
| Empresa, Centro, Cliente, Tarea, Estado, Prioridad, Inicio, Fin, Duración de la tarea, En pausa, Completada por, Valoración, Nº evidencias | la tarea, como hoy |
| **Persona** | la asignación |
| **Puesto** | `job` congelado en el fichaje o en la asignación |
| **Horas de la persona** | sus sesiones de fichaje en la tarea (`checklogs_raw.task_id`); sin fichajes, el reloj de la tarea menos pausas |
| **Origen de las horas** | «Fichajes» o «Reloj de la tarea» |
| Precio por hora, Coste puesto | D5 |
| **Complementos** | nombres con su valor entre paréntesis |
| Complementos (importe), Coste persona | D5 |

Cada tarea cierra con una fila **«Total {tarea}»**: horas y coste de su gente, complementos,
material (su detalle sigue en la hoja «Material») y coste bruto. Al final, total del periodo.

**Hoja «Por persona».** Resumen del periodo: persona, nº de tareas, horas, puestos, coste del
puesto, complementos, coste, y qué complementos cobró y cuántas veces. Sale de las mismas filas.

**Hoja «Complementos».** La traza: una línea por complemento con tarea, persona, puesto, tipo,
valor, horas, precio por hora, importe y **origen** (el fichaje de entrada que lo lleva, o «la
asignación de la tarea» si no hubo fichaje). Es el ADR-005 de a3 aplicado aquí.

Las hojas «Material» e «Incidencias» no cambian. **Sin unidad monetaria en ninguna cabecera**
(ADR 0003 de ingeniería, «la moneda es de la empresa»): «Coste», «Importe», «Precio por hora».
Las cabeceras actuales «Coste material (€)», «Coste unitario (€)» y «Coste (€)» se corrigen.

Las columnas de dinero solo van en el informe de propietario y administrador (D10); el gestor
recibe el mismo informe sin ellas.

### D7. Cartera: el mismo número que el informe

`montageCosts.ts` (rentabilidad del contrato) y `CustomerInsights.ts` (análisis del cliente)
pasan a usar `labourCost` de D5 con el precio **congelado** y los complementos. Las dos fugas
de hoy se tapan en la misma pasada: el reloj de la tarea valora con el `job` de la asignación
(o el precio vigente en `responsibility_events` en la fecha) y el análisis del cliente deja de
leer el `job_price` actual. Los complementos aparecen como línea propia (`labour.supplements`)
junto al personal, el material y los gastos externos (TDR-008 de cartera). Tarea, contrato y
cliente dan la misma cifra.

### D8. Estadísticas y análisis: los complementos se suman aparte

`operational_daily` gana `supplement_cost NUMERIC(14,2)`; `labor_cost` sigue siendo horas ×
precio del puesto. Coste por sucursal, coste por hora, personas con más coste y desviación
económica enseñan el total con el desglose, y Merlin lo nombra («de ellos, X en complementos»).
Los perfiles no se tocan: `experienceByJob` ya agrupa por nombre de puesto y se afina solo; el
coste medio por hora de la persona pasa a ser el efectivo y se etiqueta así.

### D9. El informe de jornada no se toca; a3 recibe unidades

El informe legal de jornada es de tiempo de trabajo y no lleva dinero. Para a3-nómina, los
complementos del fichaje son la fuente que faltaba para su fase 3: se mandarán como **unidades**
(un plus de conducción, dos festivos), nunca en euros (a3 ADR-003). La nocturnidad y el festivo
**medidos** (22:00–06:00, calendario) siguen en el diseño de a3; aquí solo entran los que la
empresa elige a mano. Si quiere verlos en euros, define «Nocturnidad, +25 %» en el catálogo.

### D10. Dinero solo propietario y administrador

Como la cartera (D18 de `cartera-de-clientes/06_decisiones-abiertas.md`): el gestor y el
supervisor eligen puesto y complementos por su nombre y no ven ni precio ni importes, en el
panel, en el informe ni en el asistente.

### D11. La tarea no tiene precio propio

Salió en la reunión y Jose lo cerró el 24-nov: «no, ya entra con esto». El ingreso es el
contrato del cliente (ADR-006 de cartera); el margen se mira por contrato y por cliente.

### D12. Sin unidad monetaria

Ni en cabeceras, ni en etiquetas, ni en el asistente. La moneda es un dato de la empresa y se
aplica al formato numérico (ADR 0003 de ingeniería).

## 3. Modelo

### 3.1 `@encodebiz/shared`

```ts
// Employee.ts
export interface EmployeeResponsibility {
  job: Job;                 // predeterminado; sin cambios
  jobs?: Job[];             // puestos adicionales (D1); nunca repite el predeterminado
  // ...
}

// supplements/Supplement.ts
export type SupplementKind = "fixed" | "hourly" | "percent";
export interface Supplement {
  id?: string; name: string; kind: SupplementKind;
  /** fijo y por hora: importe en la unidad del precio del puesto; porcentaje: fracción (0.25). */
  value: number;
  active: boolean; createdAt: Date; updatedAt?: Date;
}
export type SupplementSnapshot = Pick<Supplement, "id" | "name" | "kind" | "value">;

// Task.ts
export interface TaskAssignment { /* ... */ job?: Job; supplements?: SupplementSnapshot[]; }

// CheckLog.ts
export interface Shift { start; end; taskId?; title?; job?: Job; supplements?: SupplementSnapshot[]; }
// metadata del fichaje
metadata.employeeResponsibility  // {...job, responsibility, level}: el puesto ELEGIDO (D4)
metadata.supplements?: SupplementSnapshot[]
metadata.jobSource?: "assignment" | "shift" | "default"   // trazabilidad

// costs/labourCost.ts (D5)
export function labourCost(input: {minutes: number; price: number | null; supplements: SupplementSnapshot[]})
  : {base: number | null; hourly: number; percent: number | null; fixed: number; total: number | null}
```

### 3.2 Firestore

- `entities/{e}/supplements/{id}`: el catálogo (D2). Reglas: lectura gestores y superiores;
  escritura por el backend (`employees`), como las ocupaciones.
- `entities/{e}/employee_responsibilities/{id}.jobs` y
  `entities/{e}/teams/{t}/team_responsibilities/{id}.jobs` (las plantillas de equipo se copian
  con sus puestos).
- `entities/{e}/tasks/{t}/assignments/{employeeId}.job / .supplements`.
- Turnos: en `workSchedule` de la responsabilidad y la sucursal, en `generated_days` /
  `loaded` y en `scheduleApplied` del fichaje, por ser el mismo `Shift`.

### 3.3 Postgres (migraciones a mano, una a una)

- **071_complementos_en_el_fichaje.sql:** `checklogs_raw.supplements JSONB`,
  `checklogs_raw.job_source TEXT`; `operational_daily.supplement_cost NUMERIC(14,2)`;
  `dim_responsibilities.jobs JSONB` (los adicionales; `job_name`/`job_price` siguen siendo el
  predeterminado).
- **072_asignaciones_espejo.sql:** `task_assignments_raw (entity_id, task_id, employee_id,
  status, job_name, job_price, supplements JSONB, assigned_at, started_at, completed_at,
  removed_at, synced_at)`, PK `(entity_id, task_id, employee_id)`, índice por
  `(entity_id, employee_id)`. Lo escribe `TaskPgMirror` al espejar la tarea. Es de donde leen
  el informe y la cartera para las tareas sin fichaje y para saber «como qué» fue cada uno.
- `supplement_events` no hace falta: el catálogo se copia en cada uso (3.1), así que el
  histórico está en los propios fichajes y asignaciones.

## 4. API

**`employees`**
- `PATCH /responsibilities` admite `jobs: Job[]` (y los valida contra el catálogo, como `job`).
- Catálogo: `GET/POST/PATCH/DELETE /supplements` (`DELETE` = `active: false`; lo ya copiado no
  se toca). `POST` con el mismo nombre normalizado devuelve el existente.

**`tasks`**
- `POST /:taskId/assignments` admite `assignments: [{employeeId, jobId?, supplementIds?}]`
  además de `employeeIds` (que sigue valiendo y cae al predeterminado). El servidor copia `job`
  (de los puestos de la responsabilidad de esa persona en esa sucursal; si `jobId` no es suyo,
  400) y los `SupplementSnapshot` del catálogo.
- `PATCH /:taskId/assignments/:employeeId` `{jobId?, supplementIds?}` para editar desde la ficha.
  Cambios al historial de la tarea (`task_events_raw`), como el resto.

**Turnos** (`employees` semana tipo, `checkinbiz`/`shared` turnos cargados, `assistant`
cuadrante): `Shift` acepta `jobId?` y `supplementIds?` y se guardan copiados. El Excel del
cuadrante gana dos columnas opcionales, «Puesto» y «Complementos» (nombres separados por coma);
`proponer_cuadrante` las valida contra los puestos de la persona y el catálogo y lo dice en los
hallazgos.

**`checkinbiz`:** sin cambio de contrato; cambia lo que congela (D4).

**`reports`:** `POST /api/reports/tasks` sin cambio de contrato; cambia el Excel (D6).

**`assistant`:** `crear_tarea`, `reasignar_tarea` y `cargar_turnos` admiten puesto y
complementos por nombre; `informe_tareas` devuelve el nuevo Excel; `ver_costes` y las
estadísticas enseñan el desglose solo a propietario y administrador.

## 5. Panel

- **Ficha de la persona, bloque de la sucursal** (`SucursalFromItem`): lista dinámica de puestos
  con el selector de ocupación de hoy y el marcador «predeterminado». Precio visible solo con
  permiso de dinero.
- **Configuración → Complementos:** lista nombre / tipo / valor, al lado de las ocupaciones.
- **Formulario de tarea** (`TaskFormDialog`): en cada chip del multiselect, «como: {puesto} ▾»
  solo si la persona tiene más de un puesto en esa sucursal, y «+ complemento». Misma edición en
  «Equipo asignado» de la ficha (`detail/page.tsx`).
- **Turnos** (`WorkScheduleField`, turnos cargados, cuadrante): los dos campos opcionales en el
  editor de cada turno; vacíos por defecto.
- **Informe de tareas:** sin cambios en el modal; el Excel llega distinto.
- **Dinero:** formato con la moneda de la empresa a través del formateador único del ADR 0003.

## 6. App

Nada obligatorio. La trabajadora no ve dinero. Opcional y aditivo: «como: conductora» en el
detalle de la tarea y del turno, leído de la asignación. La app vieja ignora los campos nuevos.

## 7. Adaptadores y Merlin

- **Rentman:** la plaza de cada proyecto (`name`, `hourlyCost`) deja de perderse: va a
  `TaskAssignment.job` de la tarea del proyecto. La responsabilidad sigue con la primera plaza
  como predeterminado. Si la plaza no está en el catálogo de ocupaciones, se añade (regla de
  «se toma si existe y se añade si no»).
- **Merlin, contratos laborales** (`aplicar.ts`): escribe oficio y precio en el puesto
  **predeterminado**; la referencia al convenio (`agreementRef`, TDR-001 de convenios) cuelga
  del mismo. Si el contrato nombra un segundo oficio, lo propone como puesto adicional sin
  precio, y la persona decide.
- **Equipos:** las plantillas de miembro llevan `jobs` y se copian al aplicar.
- **Catálogo de ocupaciones:** sin cambios.

## 8. Compatibilidad

Todo es aditivo. Nada que migrar, nada que rellenar:

- `job` sigue siendo el predeterminado: fichaje, Merlin, Rentman, equipos,
  `dim_responsibilities`, perfiles y estadísticas funcionan igual con responsabilidades sin `jobs`.
- `employee_price` conserva su significado. Los fichajes anteriores no tienen `supplements` y se
  valoran como hasta ahora.
- Las tareas ya asignadas no tienen `job` en la asignación y caen al predeterminado.
- Un `Shift` sin los campos nuevos es un turno de hoy.
- El informe de tareas cambia de forma: el cliente que lo lee recibe el nuevo. Es la decisión
  de Jose del 24-nov; se avisa en el pase.

## 9. Fases

| Fase | Qué | Dónde |
|---|---|---|
| **1. Modelo y fichaje** | Tipos de 3.1, catálogo de complementos con su API, `jobs` en la responsabilidad, `job`/`supplements` en asignación y turno, D4 en los tres caminos del fichaje, espejo (071, 072), `labourCost` con tests | `shared`, `employees`, `tasks`, `checkinbiz`, `analytics` (espejo) |
| **2. Lectura** | Informe de tareas (D6), cartera (D7), día operativo y estadísticas (D8), herramientas del asistente de lectura | `reports`, `customers`, `analytics`, `assistant` |
| **3. Panel** | Lista de puestos, Configuración → Complementos, chips de la asignación, editores de turno, cuadrante | `encodebiz-front-saas` |
| **4. Escritura asistida y adaptadores** | `crear_tarea`/`cargar_turnos`/`proponer_cuadrante` con puesto y complementos; Rentman; Merlin | `assistant`, `rentman`, `merlin` |

La fase 1 sola no cambia nada visible; la 2 ya da el informe nuevo con el predeterminado de
cada persona (puesto y horas por persona), que es valor por sí mismo.

## 10. Guion de QA (staging, solo empresas de prueba)

1. Persona con dos puestos en la misma sucursal; en la tarea el chip enseña el selector; en otra
   persona con uno, no.
2. Catálogo con un complemento de cada tipo. Tarea con una persona que lleva los tres.
3. Fichaje en modo por tareas: `employee_price` es el del puesto elegido, `supplements` tiene
   los tres, `job_source = "assignment"`.
4. Turno cargado con puesto y complemento, fichaje normal: `job_source = "shift"`.
5. Fichaje sin nada elegido: predeterminado, `job_source = "default"`, `supplements` vacío.
6. Informe de tareas: fila por persona, totales por tarea que cuadran con «Por persona» y
   «Complementos»; el gestor no recibe columnas de dinero; ninguna cabecera con símbolo.
7. Contrato con esa tarea: el coste de personal coincide con la suma de «Coste persona» de la
   tarea; complementos como línea propia.
8. Cambiar el precio del puesto después: las tareas pasadas no cambian (congelado).
9. Rentman: dos plazas distintas de la misma persona en dos proyectos → dos asignaciones con
   puestos distintos.

## 11. Fuera de este TDR

- Coste de empresa (Seguridad Social): el coste sigue siendo bruto y se dice así (ADR-006 de
  cartera).
- Precio de la tarea (D11).
- Nocturnidad y festivo **medidos** del fichaje: diseño de a3-nómina (TDR-002).
- Envío de complementos a a3 (su fase 3): este TDR les da la fuente.
- Moneda de la empresa: ADR 0003 de ingeniería, en curso.
- Recalcular patrones y estadísticas pasadas con el histórico de precios (59.4 de la revisión
  del análisis): el cálculo nuevo solo mira hacia delante.

## Referencias

- [TDR-004 — Informe de tareas](./TDR-004-informe-tareas-xlsx.md) · [09 — Encargada](../09_encargada.md)
- Cartera: [ADR-006 — El contrato es el montaje](../../cartera-de-clientes/adr/ADR-006-el-contrato-es-el-montaje.md), [TDR-008 — Gastos externos](../../cartera-de-clientes/tdr/TDR-008-gastos-externos.md), D18 en [06](../../cartera-de-clientes/06_decisiones-abiertas.md)
- a3-nómina: [ADR-003 — Unidades, no euros](../../a3-nomina/adr/ADR-003-unidades-no-euros.md), [ADR-005 — Cada línea sabe de dónde sale](../../a3-nomina/adr/ADR-005-cada-linea-sabe-de-donde-sale.md), [TDR-002 — El cierre del periodo](../../a3-nomina/tdr/TDR-002-el-cierre-del-periodo.md)
- Contratos laborales: [README](../../contratos-laborales/README.md), [TDR-001 — Catálogo de convenios](../../contratos-laborales/tdr/TDR-001-catalogo-de-convenios.md)
- [ADR 0003 — La moneda es de la empresa](../../adr/0003-la-moneda-es-de-la-empresa.md)

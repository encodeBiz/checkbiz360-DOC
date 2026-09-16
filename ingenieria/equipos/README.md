# Equipos — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Plantilla (empleados y responsabilidades) → Equipos
**Fecha de inicio:** 2026-09-13
**Estado:** Diseño acordado · en dos pasos: sucursal, después tarea · paso 1 en implementación
**Autor:** Jose Acevedo

---

## Contexto y motivación

Poner gente a trabajar es hoy una operación de uno en uno, y en plantillas grandes se vuelve
tedioso. Son dos operaciones distintas, y conviene no mezclarlas:

1. **Dotar un proyecto.** En checkbiz un proyecto es una sucursal. Dotarla es crear una
   responsabilidad por persona, cada una con su nivel, su puesto y su precio por hora, en un
   formulario por persona. Cuando la misma cuadrilla pasa de un proyecto a otro, se vuelve a
   teclear lo mismo.
2. **Asignar una tarea.** El selector busca por nombre en toda la empresa (`searchIndex` solo
   indexa nombre, correo y teléfono), no sabe de qué sucursal es la tarea, y el servidor
   rechaza después con `task/invalid_employees` a quien no tiene responsabilidad allí.

**El caso que lo motiva es Tapissat.** Trabajan con equipos fijos a los que asignan proyectos,
y quieren configurar el equipo una vez y asignarlo de golpe. Su puesta en marcha ya lo
anticipaba: en la hoja de responsabilidades dejaron `nombre_sucursal` vacío para decir «el
mismo puesto y el mismo coste en todas sus sucursales»
([02_caso-real-tapissat.md §2](../puesta-en-marcha/02_caso-real-tapissat.md)). Una
responsabilidad sin sucursal que se reparte después: es exactamente un miembro de equipo.
Sus «sucursales», además, son obras dentro de fábricas de clientes, que es la lectura de
sucursal como proyecto.

---

## Principio de diseño

> **Un equipo es una plantilla de responsabilidades sin sucursal. Aplicarlo a una sucursal las
> copia con la sucursal puesta. La plantilla no manda sobre lo aplicado: la sucursal es la verdad.**

---

## Alcance

Se hace en dos pasos, y cada uno se entrega solo. El primero resuelve dotar un proyecto; el
segundo, asignar una tarea. El primero no toca tareas, y el segundo no necesita que el primero
esté en producción salvo para «añadir equipo».

**Paso 1 · Sucursal.**

- La colección `teams`, su subcolección `team_responsibilities` y sus tipos en `@encodebiz/shared`.
- Crear, renombrar y borrar equipos, y añadir, editar y quitar miembros, en el servicio `employees`.
- Aplicar un equipo a una sucursal.
- Guardar la plantilla de una sucursal como equipo.
- Que la baja de un empleado lo retire de sus equipos.
- Las pantallas del panel para todo lo anterior.

Al terminar el paso 1, quien entra en una sucursal por un equipo ya es asignable a las tareas de
esa sucursal con el selector de hoy. El paso 2 lo hace cómodo, no posible.

**Paso 2 · Tarea.**

- El selector de empleados de la tarea: plantilla de la sucursal con su puesto, filtro por
  puesto, «todos» y «añadir equipo».

**Fuera de los dos:**

- **La app móvil.** No cambia: solo lee `employee_responsibilities`, y lo aplicado son
  responsabilidades normales.
- **Skills o categorías** paralelas al catálogo de puestos (ver D1).
- **Propagar cambios** del equipo a sucursales ya dotadas (ver D3).
- **Que la tarea referencie al equipo** (ver D5).
- **Procedencia.** Una responsabilidad aplicada no guarda de qué equipo salió. Se puede añadir
  después como campo nuevo sin tocar lo guardado.
- **Los equipos que propondría Merlin** a partir de los perfiles. Esto es agrupación manual.
  Un equipo declarado a mano es, en todo caso, el insumo que esa fase necesitaría.
- **Un bloque «Equipos» en la ficha del empleado.** Es solo lectura y se puede añadir en
  cualquier momento; no hace falta para dotar un proyecto.
- **Simular antes de aplicar en el servidor.** Ver la confirmación en el panel.

---

## Decisiones

### D1 · Equipos, no skills

Un skill es un atributo («sabe hacer X»); un equipo es una decisión («estos trabajan juntos»).
Agrupar por skill da a todos los electricistas, no a la cuadrilla que va a una obra. Además,
un catálogo de skills competiría con el de puestos (`entities/{id}/jobs`), que ya es texto libre
deduplicado en el navegador. Y viviría en el empleado, por empresa, mientras el puesto vive en
la responsabilidad, por sucursal.

### D2 · Los miembros, en una subcolección del equipo, con el tipo de siempre

Un miembro es un `EmployeeResponsibility` con el ámbito apuntando al equipo, y se guarda en
`teams/{teamId}/team_responsibilities/{employeeId}`.

**Por qué no en `employee_responsibilities` con `branchId` a null**, aunque tenga la misma forma:

1. **El identificador sin sucursal es único por empleado y entidad**
   (`{employeeId}_{entityId}`). Una persona no podría estar en dos equipos.
2. **Hay lectores que no filtran por sucursal** y tomarían la plantilla por una responsabilidad
   real:

| Lector | Qué haría con la plantilla mezclada |
|---|---|
| App, asistencia (`responsibility_firestore_datasource.dart`) | La enseñaría como un sitio más, sin sucursal. Arreglarlo es publicar la app. |
| `TaskRecipientResolver` (shared) | Avisa de cada tarea a toda responsabilidad de nivel manager o superior de la entidad, sin mirar la sucursal: un manager de plantilla recibiría todos los avisos. |
| `DocumentPermissionService` (documents y SaaS) | La tendría en cuenta al resolver permisos de documentos. |
| CSV de empleados del SaaS | La volcaría como una responsabilidad más. |

**Por qué no una sola colección de miembros sin documento de equipo.** El nombre se repetiría en
cada miembro, y renombrar sería reescribirlos todos. No podría existir un equipo vacío. Y listar
equipos costaría una lectura por miembro: treinta equipos de quince personas son 450 lecturas
para pintar treinta nombres.

**Por qué subcolección y no una colección hermana de `teams`.** Leer los miembros de un equipo es
leer una ruta, sin filtro ni índice, y el identificador del miembro se reduce al empleado. Lo
único que empeora es buscar a una persona en todos sus equipos, y no hace falta consulta para
eso: como el documento se llama como el empleado, su ruta en cada equipo se conoce.

### D3 · La plantilla no propaga

Cambiar el precio de alguien en el equipo no toca las sucursales ya dotadas. El precio que usan
el coste y los informes es el de la responsabilidad de la sucursal, y además
[viaja congelado dentro de cada fichaje](../puesta-en-marcha/adr/ADR-002-la-puesta-en-marcha-siembra-patron-y-coste.md).
Si el equipo propagara, el cliente creería haber corregido un proyecto cuyo pasado no cambia.
La pantalla del equipo tiene que decirlo.

### D4 · Aplicar nunca pisa

Al aplicar se salta a quien ya tiene responsabilidad en esa sucursal, activa o no, y se dice a
quién. `POST /employees/responsibilities` hace hoy un `set` sin merge sobre
`{employeeId}_{entityId}_{branchId}`: aplicar sin esta regla borraría el precio afinado y
reenviaría el aviso de alta. Las altas se escriben con `create`, que falla si el documento
apareció entre la comprobación y la escritura.

### D5 · La tarea no referencia al equipo (paso 2)

En la tarea, el equipo se expande a personas en el selector y la tarea sigue guardando
`assignedEmployeeIds`. Así no cambian ni la app ni `POST /tasks/:id/assignments`. Y un cambio
en el equipo no altera tareas ya creadas, ni sus informes, ni obliga a avisar a quien entra tarde.

### D6 · Todo lo que escribe va por el contenedor

Equipos, miembros y aplicar se escriben por el servicio `employees`, con la misma puerta que
las responsabilidades: `canWrite(uid, entityId)`, que exige asiento activo de owner o admin.
Aplicar crea permisos, y eso no se hace desde el navegador. Ver
[salida-del-monolito/ADR-003](../salida-del-monolito/adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md)
sobre por qué la plantilla vive en `employees`.

---

## Modelo de datos

```
entities/{entityId}/employees/{employeeId}
entities/{entityId}/employee_responsibilities/{employeeId}_{entityId}_{branchId}

entities/{entityId}/teams/{teamId}
entities/{entityId}/teams/{teamId}/team_responsibilities/{employeeId}
```

```ts
// packages/shared/src/checkbiz/entities/Team.ts
export interface Team {
  id?: string;
  entityId: string;
  name: string;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}

// packages/shared/src/checkbiz/entities/Employee.ts — el ámbito gana `teamId`
export type ResponsibilityScope = { entityId: string; branchId?: string; teamId?: string };
```

Una escritura lleva **exactamente uno** de los dos, `branchId` o `teamId`. Una persona puede estar
en varios equipos y no dos veces en el mismo.

**La subcolección se llama `team_responsibilities`, y nunca `employees`.** El código consulta en
varios sitios todas las colecciones llamadas `employees` a la vez (`collectionGroup`) para
encontrar a un empleado por su usuario o su id. Una subcolección con ese nombre bajo `teams`
aparecería en esas búsquedas.

**Qué pasa con cada campo al aplicar:**

| Campo | En `team_responsibilities` | En `employee_responsibilities` |
|---|---|---|
| `employeeId`, `responsibility`, `level`, `job`, `metadata` | Los del miembro | Se copian |
| `scope` | `{entityId, teamId}` | `{entityId, branchId}` |
| `id` | `{employeeId}` | `{employeeId}_{entityId}_{branchId}` |
| `assignedBy`, `assignedAt` | Quién lo añadió al equipo, y cuándo | Quién aplica, y cuándo |
| `active` | Siempre `1`: quitar es borrar | `1` |
| `workScheduleEnable`, `workSchedule` | No se guardan | No se ponen: el horario se afina en la sucursal |

**El repositorio elige la ruta por el ámbito**, y el resto se reutiliza.
`findResponsibilities({entityId})` sigue yendo a `employee_responsibilities`, así que los
lectores actuales no cambian.

**Índices.** No hay consultas nuevas con filtro compuesto: los miembros se leen por ruta, y la
baja de un empleado borra por ruta en cada equipo. No hace falta desplegar índices.

---

## Reglas de negocio

- **Nombre único por entidad**, comparado sin mayúsculas, sin tildes y sin espacios sobrantes.
  Se comprueba en el API y no en el identificador, para que renombrar no cambie el documento.
- **Para entrar en un equipo**, el empleado existe en la entidad y no está `fired`. Vacaciones,
  baja médica o `pending` no impiden estar en una plantilla. `job.job` no está vacío y
  `job.price` es un número finito y no negativo.
- **Añadir o quitar un miembro no avisa a nadie.** No le da acceso a ningún sitio todavía.
- **Aplicar** salta a quien ya está en la sucursal y a quien está `fired` o `pending`. Escribe
  en un solo lote las responsabilidades y el `Employee.branchId` de cada uno, y después envía el
  aviso `assign_created` solo a los creados.
- **Guardar una sucursal como equipo** copia sus responsabilidades activas a un equipo nuevo,
  sin horario y saltando a quien esté `fired`. Una sucursal sin nadie no se guarda.
- **Borrar un equipo** borra primero sus `team_responsibilities`: Firestore no borra una
  subcolección al borrar su documento. Las responsabilidades ya aplicadas se quedan.
- **La baja de un empleado** borra también su documento en cada equipo de la entidad, en
  `deleteEmployee` de shared, donde hoy ya borra sus responsabilidades y su entrada del buscador.
- **Los equipos no entran en `searchIndex`.** Por entidad serán decenas, y así no hay nada que
  retirar al borrar.

---

## Contratos de API

En `employees`, bajo `/api/v1/employees/teams`, con ID token de Firebase y `canWrite`. El router
se monta **antes** que el de plantilla, igual que el de responsabilidades, para que
`/teams` no lo capture `/:employeeId`. Las respuestas siguen la forma de responsabilidades:
`{success, data}` o `{error, code}`.

| Método | Ruta | Cuerpo o consulta | Responde |
|---|---|---|---|
| `GET` | `/teams` | `?entityId=` | `200` equipos con `memberCount` |
| `POST` | `/teams` | `{entityId, name}` | `201` equipo · `409 team/name_taken` |
| `GET` | `/teams/:teamId` | `?entityId=` | `200 {team, members}` · `404 team/not_found` |
| `PATCH` | `/teams/:teamId` | `{entityId, name}` | `200` equipo · `404` · `409 team/name_taken` |
| `DELETE` | `/teams/:teamId` | `entityId` en consulta o cuerpo | `200 {deletedMembers}` · `404` |
| `POST` | `/teams/:teamId/members` | `{entityId, employeeId, responsibility, job, metadata?}` | `201` miembro · `404 employee/not_found` · `400 employee/fired` · `409 team/member_exists` |
| `PATCH` | `/teams/:teamId/members/:employeeId` | `{entityId, responsibility?, job?, metadata?}` | `200` miembro · `404 team/member_not_found` |
| `DELETE` | `/teams/:teamId/members/:employeeId` | `entityId` en consulta o cuerpo | `200` · `404 team/member_not_found` |
| `POST` | `/teams/:teamId/apply` | `{entityId, branchId}` | `200` resultado · `404 branch/not_found` · `409 team/apply_conflict` |
| `POST` | `/teams/from-branch` | `{entityId, branchId, name}` | `201 {team, members, skipped}` · `400 team/branch_without_staff` |

Todas son del paso 1. El paso 2 no necesita rutas nuevas: la tarea sigue usando
`POST /tasks/:id/assignments` con una lista de personas.

`apply` responde a quién ha dado de alta y a quién ha saltado, y por qué:

```json
{
  "branchId": "…",
  "created": ["empA", "empB"],
  "skipped": [{ "employeeId": "empC", "reason": "already_in_branch" }]
}
```

Motivos posibles: `already_in_branch`, `employee_not_found`, `employee_not_active`.
`409 team/apply_conflict` significa que alguien dio de alta a uno de ellos en esa sucursal
mientras se aplicaba: no se ha escrito nada, y repetir la operación lo salta.

---

## Panel

**Paso 1 · Sucursal.**

- **Empleados → pestaña «Equipos».** Lista, crear, renombrar y borrar. La ficha del equipo
  lista sus miembros. Añadir un miembro reutiliza el formulario de responsabilidad, con el
  campo de sucursal cambiado por el equipo.
- **Ficha de sucursal → lista de empleados.** Dos acciones nuevas. «Aplicar equipo» elige un
  equipo, enseña sus miembros con puesto y precio, y pide confirmación. Después muestra a quién
  dio de alta y a quién saltó. «Guardar como equipo» pide un nombre.

La confirmación importa más de lo que parece: aplicar el equipo equivocado a la obra
equivocada son treinta avisos de alta, y deshacerlo son treinta bajas y treinta avisos más. No
hace falta simulación en el servidor para eso; el panel ya tiene los miembros cargados.

**Paso 2 · Tarea.**

- **Alta y edición de la tarea.** El selector lista la plantilla de la sucursal de la tarea, con
  su puesto, filtro por puesto y «todos». «Añadir equipo» añade a los miembros que están en esa
  sucursal y dice quién queda fuera.

Cada ruta nueva necesita su entrada en la lista del proxy (`lib/http/serverBackendProxy.ts`) y
su variable `NEXT_BACKEND_URI_*` en Vercel **antes** de que el front llegue a `main`. Sin ella,
el proxy responde 403.

---

## Fases

### Paso 1 · Sucursal

| Fase | Qué | Verificación | Estimación gruesa |
|---|---|---|---|
| **1.1 · Dominio y API** | Tipos y ámbito en shared, repositorio por ámbito, baja de empleado, router `teams` en `employees`, casos en la suite de QA | En desarrollo: aplicar un equipo a una sucursal donde uno ya está; ese queda saltado con su precio intacto, y los creados pueden fichar | 2 jornadas |
| **1.2 · Panel** | Pestaña de equipos, aplicar y guardar desde la sucursal, proxy y variables | Montar en desarrollo un equipo con la forma de Tapissat y aplicarlo a sus cuatro obras | 3 jornadas |

El paso 1 no tiene dependencias fuera de sí mismo: no toca tareas, ni la app, ni Firebase.

### Paso 2 · Tarea

| Fase | Qué | Verificación | Estimación gruesa |
|---|---|---|---|
| **2.1 · Panel: selector de tarea** | Plantilla de la sucursal, filtro por puesto, «todos», «añadir equipo» | Una tarea asignada a una cuadrilla entera; con `all_assigned_workers`, sigue en curso hasta que termina el último | 2 jornadas |

**Dependencias del paso 2.**

- **HAL-36**, la política de terminación, está corregida en desarrollo desde el 2026-09-13.
  Tiene que estar en producción antes que el paso 2: con treinta asignados, el primero que
  terminaba cerraba la tarea de todos.
- **HAL-38.** La edición de la tarea no asigna aunque el formulario lo mande, y el arreglo está
  sin decidir. El selector nuevo vive en ese formulario.

Cadena de siempre para los dos repos y los dos pasos: `develop → staging → main`.

---

## Lo que no es evidente

**El repositorio toca la ficha del empleado al crear y borrar.** `createResponsibility` hace
`arrayUnion(scope.branchId)` sobre `Employee.branchId`, y `deleteResponsibility` hace
`arrayRemove`. Con ámbito de equipo, `branchId` no existe, y esas dos líneas no deben
ejecutarse. `Employee.branchId` es lo que el volcado CSV del contenedor enseña como
sucursales, y lo que el alta de responsabilidades mantiene sincronizado.

**Los miembros huérfanos no se ven.** Si se borra el documento de un equipo antes que sus
miembros, la subcolección sigue existiendo, la consola la enseña bajo un documento en cursiva y
ninguna pantalla la encuentra. Por eso el orden: primero los miembros.

**Un lote de Firestore admite 500 escrituras.** Aplicar son dos por alta: 250 personas por
aplicación. Guardar una sucursal son una por miembro más el equipo. Sobra para un equipo, y el
API lo comprueba antes de escribir.

**Las reglas de Firestore de desarrollo están abiertas.** Mientras cualquiera pueda escribir en
cualquier colección, el permiso del contenedor es decorativo para `teams` igual que para
`employee_responsibilities`. Producción está sin mirar.

---

## Decisiones abiertas

1. **¿El precio de una persona es el mismo en todos sus proyectos?** Lo observado en Tapissat:
   su plantilla dio un puesto y un coste por persona para todas sus sucursales. Pero esos costes
   eran los del ejemplo, así que el valor real no se conoce. El paso 1 va con precio fijo en el
   equipo y afinado en la sucursal después de aplicar. Si varía en casi todos los proyectos, la
   confirmación de aplicar tendría que dejar editar el precio antes de dar de alta. Conviene
   preguntárselo a Tapissat.
2. **El horario no va en la plantilla.** Es la opción por defecto del paso 1, porque el horario
   es de la obra y no de la persona. Si hiciera falta, el tipo ya lo admite.

---

## Relacionado

- [tasks-service](../tasks-service/README.md): asignación de tareas y `validateAssignableEmployees`.
- [puesta-en-marcha/02_caso-real-tapissat.md](../puesta-en-marcha/02_caso-real-tapissat.md): el cliente y su plantilla.
- [Qa/catalogo/equipos.md](../../Qa/catalogo/equipos.md): los casos del paso 1.
- [Qa/catalogo/hallazgos.md](../../Qa/catalogo/hallazgos.md): HAL-23, HAL-36 y HAL-38.

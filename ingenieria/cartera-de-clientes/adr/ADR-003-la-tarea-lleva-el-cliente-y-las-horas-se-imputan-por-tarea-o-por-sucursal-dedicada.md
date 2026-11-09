# ADR-003 — La tarea lleva el cliente; las horas se imputan por tarea o por sucursal dedicada, explícita

**Fecha:** 2026-10-29
**Estado:** Sin efecto desde el 2026-11-03 (06 §D11): el MVP no contempla horas por cliente ni sucursales dedicadas. Se conserva la primera parte, la tarea lleva el cliente.
**Decisionario:** Jose Acevedo

---

## Contexto

Hay que responder dos preguntas con una sola regla: **qué lleva el cliente** y **de dónde
salen sus horas**. Y los sectores no se comportan igual:

- **Construcción**: una sucursal por obra, la gente ficha allí con Semana tipo o Por turnos.
  Las horas del cliente son las jornadas fichadas en la obra. Puede que ni haya tareas.
- **Limpieza por centros (Neteges)**: una sucursal base, la gente va a tres o cuatro centros
  al día con horario Por tareas. Las horas del cliente son las de la tarea; el fichaje en la
  base no dice de quién es la hora.
- **Ayuda a domicilio**: una sucursal centro con cuarenta clientas, la gente va Por turnos y
  dentro del turno hace tareas. Las horas de Juana son las de su tarea, no las del turno.

La tentación era mirar el **modo de horario** para decidir: Por tareas → imputar por tarea;
Semana tipo o Por turnos → imputar por sucursal. No vale: el modo **es de cada persona**
(decidido el 2026-10-16, [horario-por-tareas TDR-009](../../horario-por-tareas/tdr/TDR-009-tres-modos-cada-uno-lo-suyo.md)),
una misma sucursal tiene gente en los tres, y el SAD va Por turnos y aun así imputa por
tarea.

## Decisión

**La tarea lleva el cliente** (`customerId`, `customerSiteId`, snapshot `customer`), elegido
entre los asignados a su sucursal, y se lleva el lugar del cliente como `workSite`. Es lo
único que la operación toca.

**Las horas se imputan por dos fuentes, y las dos son explícitas:**

1. **Por tarea.** Los minutos de una tarea con cliente (de `startedAt` a `completedAt`, menos
   `pausedMs`) son de ese cliente. Vale para los tres modos.
2. **Por sucursal dedicada.** Las jornadas fichadas (`checklogs_raw`) en una sucursal que el
   cliente tiene en `dedicatedBranchIds` son de ese cliente, **salvo los tramos que ya caen
   dentro de una tarea con cliente del mismo empleado ese día**, que ya se contaron por la
   fuente 1.

Dedicada lo dice una persona al asignar la sucursal («las jornadas fichadas aquí cuentan para
este cliente»), nunca se deduce de que la sucursal tenga un solo cliente. Una sucursal solo
puede estar dedicada a un cliente; lo impone el servidor.

## Justificación

**Una sola regla para los tres sectores.** La constructora marca sus obras como dedicadas y
no crea ni una tarea. Neteges no marca nada y todo va por tarea. El SAD no marca Carabanchel
(es de la empresa, no de Juana) y todo va por tarea dentro del turno. Nadie tiene que saber
qué modo tiene cada persona.

**Explícito, no deducido.** Si «un solo cliente en la sucursal» bastara para imputar, la
oficina de una empresa de limpieza con un cliente asignado por error imputaría las horas de
administración a ese cliente. Un bit que hay que marcar es la diferencia entre una decisión y
un accidente, igual que `--apply`.

**No se cuenta dos veces.** La exclusión de los tramos de tarea dentro de la jornada dedicada
cubre el caso mixto: una obra dedicada donde además se crean tareas con cliente para
controlar trabajos concretos. La hora es una.

**El modo de horario queda fuera del modelo.** Que es como tiene que ser: el modo explica la
forma de cada sector, no decide la imputación. Si mañana el modo cambia (ya cambió tres veces
en octubre), la cartera no se entera.

**`tasks` sigue sin conocer el módulo.** Guarda los tres campos como guarda `workSite`; el
espejo de `customers` señala los que no resuelven. Es el mismo trato que inventario le dio a
la tarea.

## Consecuencias

- `Task.customerId?`, `Task.customerSiteId?`, `Task.customer?` (snapshot con nombre,
  contactos visibles y notas de campo, para la app que lee Firestore). `workSite` **copiado**
  del lugar, no referenciado: la tarea de ayer fichó contra la geocerca de ayer.
- `tasks_raw.customer_id`, `customer_site_id`; `customer_hours_daily` con `source: 'task' |
  'dedicated_branch'`, materializada por un job de `customers` cada noche y al cerrar cada
  tarea con cliente. El informe lee de ahí; no recalcula desde los fichajes.
- `dedicatedBranchIds ⊆ branchIds` en `Customer`; índice único parcial en
  `customer_branch_links (branch_id) WHERE dedicated`.
- Las jornadas en una sucursal **no dedicada** con varios clientes y sin tarea **no se imputan
  a nadie**. Se enseñan en el informe como «sin cliente», no se reparten. Repartir sería
  inventar ([06 §D6](../06_decisiones-abiertas.md) guarda el boceto de elegir cliente al
  fichar, por si algún día hace falta).
- El selector del panel: un cliente → puesto solo; varios → obligatorio sin preseleccionar;
  ninguno → la tarea de siempre. Lo mismo con el lugar dentro del cliente. El `workSite`
  queda editable para la visita excepcional en otra dirección.

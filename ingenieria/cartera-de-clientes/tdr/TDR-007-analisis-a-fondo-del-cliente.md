# TDR-007 — El análisis a fondo del cliente: rentabilidad, previsión, colaboración, servicio y señales

**Fecha:** 2026-11-07
**Estado:** pedido por Jose el 2026-11-07. API en staging el mismo día (`8a4564e5` + `d3bc1050`), panel `28996dce` en `feat/cartera-de-clientes`. Pase en §49.
**Decisiones de implementación:** el ingreso de un contrato con fin se reparte con su último día incluido; el del mes en curso, solo hasta hoy (también el 1/12 de un contrato sin fin); la previsión de fin de mes, en cambio, compara el coste proyectado del mes entero con el ingreso del mes entero, no con el de hasta hoy (con el corte, un cliente rentable salía en pérdidas a principio de mes); un contrato sin fin aporta 1/12 al mes. Minutos por tarea para horas y servicio, por persona asignada para coste y equipo. Gerente y supervisor ven horas de contrato y sus dos señales, nunca euros. La valoración va de 0 a 5.
**Componente:** `services/analytics` (endpoint nuevo), panel (pestaña «Análisis» de la ficha del cliente)
**Amplía:** [TDR-006](TDR-006-parte-del-cliente.md) §8. La pestaña Análisis de hoy cuenta tareas y horas y se queda corta.

---

## 1. Lo que Jose ha pedido

> «En el análisis te comiste los costes, previsiones y crecimiento de la colaboración con tu cliente, y lo
> más importante: no estás mostrando si el cliente es rentable. Puede estar cambiando de proveedor; si hay
> algo que deba mirar. Tenemos suficientes datos para hacer un estudio más profundo para ese cliente: si
> debería agregar más personal o más tareas, si se están cumpliendo los plazos en tiempo y forma. Todo esto
> es estadística que puedes sacar ahora mismo.»

La pestaña tiene que responder, en este orden: **¿me sale rentable?, ¿hay algo que deba mirar?, ¿cómo va la
relación?, ¿estoy dando el servicio bien?, ¿tengo el equipo justo?**. Todo de Postgres, sin IA: son cuentas.
Merlin podrá narrarlo después.

## 2. Reglas de redacción

- **Lo observado, no la causa.** «Las tareas de este cliente duran un 18 % más de lo planificado», no «el
  equipo es lento». Si no hay dato, se dice que no hay dato.
- **Sin dinero para gerente y supervisor** (TDR-004): ven todo lo demás en horas y tareas.
- Cada cifra con su referencia (contra qué periodo, sobre cuántas tareas).

## 3. Las piezas

### 3.1 El resumen arriba: «Lo que hay que mirar»

Una lista corta (máximo 5), con gravedad, de **señales** calculadas con reglas, la más grave primero. Si no
hay ninguna, una frase: «Nada fuera de lo normal en los últimos 3 meses».

| Señal | Cuándo | Texto (es) |
|---|---|---|
| `margin_negative` | margen del último mes cerrado < 0 (solo owner/admin) | «En {mes} costó {coste} y se facturaron {ingreso}: {margen} de margen» |
| `margin_falling` | margen % del último mes cerrado ≥ 10 puntos por debajo de la media de los 3 anteriores | «Margen de {mes}: {m} %, frente a un {media} % de media los tres meses anteriores» |
| `hours_falling` | horas del último mes cerrado ≥ 25 % por debajo de la media de los 3 anteriores | «{h} h en {mes}, un {p} % menos que la media de los tres meses anteriores» |
| `fewer_scheduled` | tareas programadas en los próximos 30 días ≥ 30 % por debajo de lo que hizo de media al mes | «Hay {n} tareas programadas para los próximos 30 días; de media se hacen {m} al mes» |
| `cancellations_rising` | canceladas del último mes cerrado ≥ 2 y ≥ 10 % | «{n} tareas canceladas en {mes}, el {p} % de las programadas» |
| `contract_ending_no_followup` | un contrato vigente termina en ≤ 45 días y no hay otro que empiece después | «{contrato} termina el {fecha} y no hay otro detrás» |
| `contract_hours_over` | las horas hechas del contrato vigente ya llegan a las previstas (rojo); sustituye a la de abajo | «{contrato}: {hechas} h hechas de {h} previstas; se superaron el {fecha}» |
| `contract_hours_exhausting` | al ritmo de los últimos 30 días, las horas previstas del contrato se acaban antes de su fin (aún no superadas) | «A este ritmo, las {h} h de {contrato} se acaban el {fecha}, antes de su fin ({fin})» |
| `late_rising` | % tarde del último mes ≥ 15 % y ≥ 5 puntos sobre la media de los 3 anteriores | «El {p} % de las tareas de {mes} terminaron tarde (media: {m} %)» |
| `missed` | tareas vencidas sin hacer en los últimos 30 días | «{n} tareas sin hacer en los últimos 30 días» |
| `overrun` | duración real ≥ 15 % por encima de la planificada (sobre ≥ 10 tareas del último mes) | «Las tareas duran un {p} % más de lo planificado ({real} frente a {plan} de media)» |
| `single_person` | una persona hace ≥ 70 % de las horas de los últimos 3 meses (con ≥ 20 h) | «{persona} hace el {p} % de las horas de este cliente» |

`margin_*` solo para propietario y administrador.

**Meses sin trabajo no son la media.** Toda comparación con «los meses anteriores» cuenta solo
los meses con trabajo en esa métrica: para el margen, con minutos de personal (un mes con ingreso
y sin trabajo da 100 % y no es una costumbre); para las horas, con minutos; para la tarde, con
tareas con cumplimiento, y entre todos al menos 5, la misma base que el último mes; para
`fewer_scheduled`, los meses con alguna hecha, y al menos dos (su media incluye el último
cerrado). Sin ese mínimo la señal no salta: un cliente que empezó en octubre no «sube» de un 0 %
que nunca existió. El margen del último mes tampoco se juzga si ese mes no tuvo trabajo.

**El último día de un contrato cuenta entero.** `ends_at` es el último día incluido: la vigencia
llega hasta las 00:00 del día siguiente en la zona de la empresa (`dim_entities.timezone`; sin
ella, UTC). Así lo usan el filtro de vigentes, `contract_ending_no_followup` y la previsión.

`contract_hours_over` lo ve quien ve las horas del contrato (TDR-004 §6), como la previsión; la
alerta de Inicio del mismo nombre (TDR-006 §9) sigue siendo solo de propietario y administrador.
La fecha es la del primer día (fecha prevista de la tarea) en que lo hecho acumulado llega a lo
previsto.

### 3.2 Rentabilidad (solo propietario y administrador)

Por mes, los últimos 6:

- **Ingreso**: el importe de cada contrato con importe, **repartido por días** de su vigencia que caen en el
  mes (un contrato de 48 000 € de octubre a diciembre aporta lo de los días de cada mes). Contratos sin fin:
  el importe es anual → /12 por mes (decisión de este TDR; si Jose lo quiere distinto, se cambia aquí).
- **Coste de personal**: minutos trabajados de cada tarea (inicio→fin menos pausas, como el parte) × el
  precio por hora del puesto de **cada persona asignada** (`dim_responsibilities.job_price` en la sucursal de
  la tarea; si no, el de cualquier sucursal). Minutos sin precio → aviso «{h} h sin precio de puesto».
- **Material**, si hay inventario: como en `contractCosts`.
- **Margen** € y %, **coste por hora** y **ingreso por hora**.
- **Veredicto** en una frase: «Rentable: {margen} ({m} %) en los últimos 3 meses», «No rentable: …», o «Sin
  importe de contrato: se sabe lo que cuesta ({coste} en 3 meses), no lo que deja».

### 3.3 Previsión

- **Este mes al ritmo actual**: horas, coste y margen proyectados a fin de mes (lo hecho + lo programado que
  queda; no una regla de tres). El margen es contra el ingreso del mes entero: coste y ingreso del mismo periodo.
- **Próximos 30 días**: tareas programadas, horas planificadas, coste previsto (horas × precio de las
  personas asignadas).
- **Contratos**: horas previstas, hechas, que quedan y en qué fecha se acaban al ritmo de los últimos 30 días.

### 3.4 La colaboración

- Cliente desde (primera tarea), meses con trabajo.
- Tendencia: horas, tareas e ingreso de los últimos 3 meses cerrados frente a los 3 anteriores, en %.
- Gráfico mes a mes (lo que ya hay), con el ingreso y el coste superpuestos para owner/admin.

### 3.5 El servicio: ¿en tiempo y forma?

Últimos 3 meses (y el mes en curso aparte): % a tiempo, % tarde, retraso medio de las tardías (min), sin
hacer, canceladas, **duración real frente a planificada** (media y %), con evidencia (%), rechazadas en la
validación (%), valoración media si la hay.

### 3.6 El equipo: ¿hace falta más gente o más tiempo?

- Personas distintas, horas por persona, concentración (la primera persona, % de horas).
- Carga: horas de este cliente sobre las horas totales de cada persona en el periodo (si una persona dedica
  ≥ 60 % de su tiempo a este cliente, se dice).
- **Lectura** (frase, sin prescribir causa): cuando coinciden duración real > planificada y tareas tarde,
  «Las tareas duran más de lo planificado y un {p} % termina tarde: revisa el tiempo asignado a cada tarea o
  el equipo»; cuando sobran (real < 80 % de lo planificado), «Se hacen en un {p} % menos del tiempo
  planificado».

## 4. API

`GET /api/analytics/customers/:customerId/insights?entityId` (mismo actor y alcance que `overview`):

```
{ customerId, name, asOf, seesMoney: boolean,
  scope: { branchIds: string[] | null, branchNames: string[] },
  signals: [{ id, severity: "high" | "medium" | "low", params: {...} }],
  profitability: null | {                       // null para gerente y supervisor
    months: [{ month, revenueCents, labourCents, materialCents, marginCents, marginPct, minutes, unpricedMinutes }],
    last3: { revenueCents, costCents, marginCents, marginPct, costPerHourCents, revenuePerHourCents },
    verdict: "profitable" | "unprofitable" | "no_revenue" | "no_data",
    hasRevenue: boolean },
  forecast: { monthEnd: { minutes, costCents|null, marginCents|null }, next30: { tasks, plannedMinutes, costCents|null },
              contracts: [{ contractId, title, estimatedHours, doneHours, remainingHours, exhaustsOn: string|null, endsAt: string|null }] },
  relationship: { since: string|null, activeMonths, trend: { hoursPct, tasksPct, revenuePct|null } },
  service: { last3: { done, onTimePct, latePct, avgDelayMin, missed, cancelled, overrunPct, evidencePct, rejectedPct, avgRating|null },
             current: { … mismo … } },
  team: { people, top: [{ employeeId, name, minutes, sharePct, dedicationPct }], concentrationPct, reading: "overrun_late" | "underrun" | null } }
```

Los importes, en céntimos; `null` cuando el rol no ve dinero. Se calcula al pedirlo; nada se guarda.

## 5. Panel

La pestaña «Análisis» se reordena: **Lo que hay que mirar** (señales) → **Rentabilidad** (veredicto, cifras
de 3 meses y el gráfico ingreso/coste por mes; solo owner/admin) → **Previsión** → **Colaboración** → **Servicio**
→ **Equipo**. Lo que hay hoy (mes a mes de tareas y horas, este mes frente al anterior) se queda dentro de
Colaboración. Textos de las señales en los cinco idiomas.

## 6. Pruebas (Neteges Demo, staging)

- Bon Preu: rentabilidad con ingreso (contrato Q4), coste de 29 personas con precio, margen; previsión con
  `contract_hours_exhausting` (900 h); servicio con su % a tiempo.
- Cdad. Prop. Carrer Cardona, 10: sin contrato → «Sin importe de contrato…»; señal `missed`.
- Un gerente ve señales, servicio y equipo, sin un solo euro.

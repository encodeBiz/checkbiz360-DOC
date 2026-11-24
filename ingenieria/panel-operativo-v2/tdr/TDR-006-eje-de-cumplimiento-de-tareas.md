# TDR-006 — El eje de tareas: cumplimiento, desviaciones y vallas

**Estado**: **EN PRODUCCIÓN desde el 2026-11-18** (API #298 `513ed12`, migración 069; panel #164 `5de91b13`; pase back §82) · **Fecha**: 2026-11-18
**Completa a**: TDR-005 (el cruce de los ejes), que dejó «tareas» aplazado el 2026-07-29
**Depende de**: TDR-004 (contrato del panel), ADR-005 (ausencia de evidencia), TDR-009 de tareas (incidencias)

---

## 1. De dónde sale

Jose, 18-nov-2026, mirando el cumplimiento de ubicación de Ayudarte: «no se está analizando el
cumplimiento de tareas en general, desviaciones, vallas, etc., y es muy importante». Y dónde:
«en el Inicio como resumen y después en la capa de análisis orientado a cada nivel: Sucursales,
Empleados y Análisis general». Lo pidió como hotfix.

Lo que había ese día:

- El cruce de ejes dice «3 ejes en servicio; tareas queda pendiente» (`TasksAxis = "sin_evidencia"`).
- De las tareas solo se analizaba la valla **al empezar**, dentro del eje de ubicación
  (`taskGeoMarks.ts`), y contando **intentos**: en Ayudarte, noviembre, 67 rechazos eran 8
  tareas, 27 de ellos de una persona en un día contra una valla de 46 m.
- La valla **al terminar** se mide (el evento `completed` trae `withinWorkSite`) y nadie la leía:
  44 cierres con valla en Ayudarte, 11 fuera.
- `time_compliance_status` del espejo no lo mantiene ningún planificador (ver
  `OperationalDay.ts`): no sirve para saber si una tarea va tarde. Todo se mide contra el reloj.

Para quien trabaja en casa del cliente, el fichaje sale casi todo «fuera del centro» y la tarea
es la única prueba de presencia y de trabajo hecho. Este eje es el que más dice de esas plantillas.

## 2. Qué tarea cuenta en un periodo

- Fecha que cuenta: la prevista, o el vencimiento si no la hay (`PLANNED_AT_SQL` de
  `customerPeriods.ts`, la misma regla que el parte del cliente).
- Fuera: borradas (`deleted_at`), borradores (`draft`) y canceladas. Una cancelada no se
  incumplió: se decidió no hacerla.
- Una tarea con **incidencia abierta** no cuenta como incumplida (TDR-009 D7): se cuenta aparte.

## 3. Lo que se mide de cada tarea

Todo con los fragmentos SQL que ya existen (`customerPeriods.ts`), no con otros nuevos:

| Medida | Regla |
|---|---|
| **Hecha a tiempo** | `completed`/`validated` con `completed_at <= due_at` |
| **Hecha con retraso** | `completed`/`validated` con `completed_at > due_at`; se guarda la mediana de minutos de retraso |
| **Empezó tarde** | `started_at > scheduled_start_at + 5 min` (`TASK_START_GRACE_MINUTES`) |
| **Sin hacer** | `missedSql(now)`: ni hecha ni cancelada, vencida y sin incidencia abierta |
| **Sin empezar** | `assigned` con la hora de inicio pasada en más de 5 min y aún sin vencer |
| **Desviación de duración** | minutos trabajados (`WORKED_MINUTES_SQL`) frente a planificados (`PLANNED_DURATION_SQL`); mediana del porcentaje, solo en las que tienen las dos |
| **Rechazada** | `status = 'rejected'` (la gestión no la dio por buena) |
| **Pausas** | número de tareas con pausas y suma de `pause_count` |

## 4. La valla de la tarea: ocasiones, no intentos

- **Al empezar.** Una ocasión es *una persona × una tarea*. Si alguno de sus intentos entró en
  la valla, la ocasión es «dentro». Si todos rebotaron, es «fuera». Los 27 reintentos de un día
  cuentan una vez. Se guarda además el número de intentos, para que se vea el ruido sin que
  pese en el veredicto.
- **Al terminar.** Cada evento `completed` con `workSite`: dentro, fuera o sin posición. Al
  terminar no se bloquea, así que no hay reintentos: se cuenta cada uno.
- El eje de ubicación (TDR-005) **sigue igual**: no se toca en este hotfix. Las ocasiones son del
  eje de tareas.

## 5. A quién se le carga (decisión de Jose, 18-nov-2026)

Las acciones con autora conocida van a quien las hizo: un inicio, un rechazo de valla, un
cierre. Lo que no tiene autora —una tarea sin hacer, sin empezar, con retraso o fuera de
plazo— se carga así:

1. Con **encargada** (`completionPolicy = "responsible_worker"`, `responsibleEmployeeId`): a la encargada.
2. Sin encargada y con **una sola persona** asignada: a esa persona.
3. Sin encargada y con **varias**: **se descarta del ámbito personal**. Cuenta en la sucursal y
   en la empresa, nunca en la ficha de nadie, porque no se puede saber quién debía hacerla.

Para esto el espejo necesita la encargada: migración **069** (`tasks_raw.completion_policy`,
`tasks_raw.responsible_employee_id`), escrita a mejor esfuerzo por `TaskPgMirror` como la 064
(ignora `42703` si la columna no existe) y rellenada con `backfill-tasks --all --apply`.

## 6. El veredicto por persona (cruce de ejes)

`TasksAxis` deja de ser solo `"sin_evidencia"`:

| Valor | Cuándo |
|---|---|
| `sin_evidencia` | menos de 3 tareas atribuibles en el periodo (ADR-005) |
| `deja_sin_hacer` | sin hacer ≥ 20 % de las atribuibles y al menos 2 |
| `fuera_de_valla` | ocasiones fuera (inicio o cierre) ≥ 20 % de las suyas con valla y al menos 2 |
| `con_retraso` | hechas con retraso ≥ 30 % de las hechas y al menos 2 |
| `cumple` | ninguna de las anteriores |

Si hay varias, gana en ese orden. `axesInService` pasa a 4 y `deferredAxes` a `[]`. Los
hallazgos nuevos entran en `ProfileFinding` (`tareas_sin_hacer`, `tareas_fuera_de_valla`,
`tareas_con_retraso`) y en la cascada del hallazgo dominante **detrás de los de registro y
delante de horas**. Los umbrales son el punto de partida y se dicen en el código con nombre.

Una sucursal con la mayoría de sus fuera de valla en tareas de radio menor de 100 m da un aviso
de configuración («vallas de tarea cortas»), no un hallazgo de persona: es la lección de
Ayudarte, en el mismo sitio que `valla_corta` del fichaje.

## 7. Dónde se ve

Un solo bloque, `tasks: TaskCompliance`, calculado por un solo builder
(`BuildTaskCompliance.ts`) para los tres niveles:

- **Análisis general** (empresa): en `GET /api/analytics/panel/overview`, junto a `geo`. Con
  desglose por sucursal y la lista de personas con hallazgo.
- **Sucursal**: el mismo overview con `branchId`. La ficha de sucursal del panel lo pinta en su
  pestaña de comportamiento.
- **Empleado**: el mismo overview con `employeeId`. La ficha de la persona lo pinta en su perfil
  de trabajo, con el veredicto del eje.
- **Inicio**: una tarjeta «Tareas del mes» con hechas a tiempo, con retraso, sin hacer y fuera
  de valla, que enlaza al análisis.

Para no calcular el overview entero en Inicio ni en las fichas, el overview acepta
`sections=tasks`: devuelve `scope`, `period` y `tasks` y nada más. **No hace falta ninguna
variable nueva en Vercel**: todo va por el proxy `checkinbiz_panel_overview` que ya existe.

## 8. Contrato

```ts
type TaskComplianceCounts = {
  planned: number;          // tareas del periodo (§2)
  done: number; onTime: number; late: number;
  lateMedianMinutes: number | null;
  startedLate: number;
  missed: number;           // sin hacer
  notStarted: number;       // sin empezar, aún en plazo
  inProgress: number;
  rejected: number;
  openIncident: number;
  durationDeviationMedianPct: number | null;
  withPauses: number;
  fence: {
    start: { occasions: number; inside: number; outside: number; attempts: number };
    finish: { total: number; inside: number; outside: number; noPosition: number };
  };
};

type TaskCompliance = {
  totals: TaskComplianceCounts;
  compare: TaskComplianceCounts | null;        // mes anterior al mismo día, como el resto
  unattributed: number;                         // varias personas sin encargada (§5)
  byBranch: Array<{ branchId: string; name: string } & TaskComplianceCounts>; // solo nivel empresa
  people: Array<{ employeeId: string; name: string; verdict: TasksAxis } & TaskComplianceCounts>; // empresa y sucursal
  person?: { verdict: TasksAxis } & TaskComplianceCounts; // solo nivel empleado
  configWarnings: Array<{ kind: "valla_de_tarea_corta"; branchId: string; outside: number }>;
};
```

Las claves de los textos las pone el front (`statsDashboard.operational.tasks.*`); el servidor
solo manda claves estables, como el resto del panel. Sin literales en el TSX.

## 9. Lo que no entra

- Merlin no narra todavía el eje nuevo; recibe `axesInService = 4` y el bloque, sin texto.
- Evidencias y valoraciones: quedan fuera hasta que haya uso.
- No cambia nada de lo que decide el fichaje ni la app.

## 10. Lo que cambió al construirlo (18-nov-2026)

- Campos añadidos al contrato: `pending` (asignada con la hora de inicio aún por llegar) y `pauseCount` en
  cada bloque de cuentas; `comparePeriod` y `balanced` en `TaskCompliance`; `name` y `shortRadiusOutside` en
  los avisos; `branchId` en cada persona. Causa estructural nueva: `valla_de_tarea_corta`.
- Los cajones son excluyentes, en este orden: hecha, rechazada, incidencia abierta, sin hacer, en curso, sin
  empezar, pendiente. «Sin hacer» no incluye las rechazadas.
- A nivel empresa `people` solo trae a quien tiene hallazgo; a nivel sucursal, a todas.
- La comparación es con el mes anterior hasta el mismo día si el mes está en curso, y entero si está cerrado.
- Los hallazgos de tareas van detrás de `patron_de_conducta` y delante de `trabaja_de_menos`.
- Las ocasiones de valla se cuentan sobre las tareas del periodo (por su fecha prevista), no por la fecha del
  evento: así todas las cifras hablan de las mismas tareas.
- En el panel: la tarjeta de Análisis va en su propia fila; las fichas van siempre con el mes en curso.

## 11. Corrección tras el recuento a mano (18-nov-2026, hotfix #299, pase §83)

- **Hecha con retraso** = cerrada más de **15 min** después del vencimiento (Jose: «15 de margen, como la
  jornada»). Los minutos de retraso se siguen contando desde el vencimiento. El margen del inicio sigue en 5.
- **`noDeadline`**: hecha con el vencimiento anterior al inicio; ni a tiempo ni tarde. `done = onTime + late + noDeadline`.
- **Valla al terminar**: solo los cierres de la persona en tareas con valla. Los de la gestión desde el panel
  no cuentan; «sin posición» es un cierre de la persona en tarea con valla que llegó sin coordenadas.

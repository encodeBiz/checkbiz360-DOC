# 02 — Arquitectura objetivo (To-Be)

---

## 1. Topología

```
                 Firestore (GCP)                          Postgres (OVH, red interna)
                 ───────────────                          ───────────────────────────
  app / panel ─▶ checkinbiz ─▶ checklogs ──trigger──▶ sync ─▶ checklogs_raw ◀── analytics (cron: conciliar) ──▶ Firestore (ids)
  app / panel ─▶ tasks ──────▶ tasks ─────────────────────────▶ tasks_raw     ◀── tasks (job: remirror)  ──▶ Firestore (updatedAt ≥)
  app / panel ─▶ inventory ──▶ item_movements ───────────────▶ item_movements_raw (ya existe)
                                                               dim_employees / dim_branches / dim_calendars ◀── analytics (cron) ──▶ Firestore
                                                                        │
                                                                        ▼
                                              analytics ── buildOperationalDay(entity, branch, day, asOf)
                                                   │                       │
                                       asOf = ahora │                       │ asOf = fin del día (cron por zona)
                                                   ▼                       ▼
                                      GET /panel/today            operational_daily ──▶ GET /panel/weeks
                                                   ▲                                          ▲
                                                   └──────── navegador (proxy, cada 60 s) ─────┘
```

Tres flechas nuevas hacia Firestore, las tres **fuera de la ruta caliente** y las tres de
lectura: conciliar fichajes, re-espejar tareas, refrescar dimensiones. El navegador nunca toca
Firestore y `analytics` tampoco al servir una petición.

## 2. Dónde vive cada pieza

| Pieza | Dónde | Por qué ahí |
|---|---|---|
| Lógica de jornada (`buildWorkSessions`) | `@encodebiz/shared` | La usan el front, Presencia y esto. Una copia |
| `tasks_raw` y su repositorio espejado | `services/tasks` | Quien escribe la tarea escribe su espejo, como `inventory` ([ADR-003](./adr/ADR-003-las-tareas-se-espejan-desde-el-servicio-de-tareas.md)) |
| Conciliación de fichajes | `services/analytics` | Tiene credenciales de Firebase; `sync` no. El upsert es el de `shared` ([TDR-004](./tdr/TDR-004-endurecer-el-espejo.md)) |
| Cron de dimensiones | `services/analytics` | `SyncDimensions` ya está ahí |
| `buildOperationalDay`, cierre diario, `operational_daily` | `services/analytics` | Dueño del cálculo del panel y del repositorio de calendario sobre Postgres ([ADR-002](./adr/ADR-002-el-dashboard-vive-en-analytics.md)) |
| `/panel/today`, `/panel/weeks` | `services/analytics`, `panel.router.ts` | Misma puerta que `overview` |
| Portada | `encodebiz-front-saas`, `/main/[entityId]/dashboard` | Donde el gerente entra |

## 3. Una función, dos momentos

```
buildOperationalDay(pool, { entityId, branchId, day, asOf }) → OperationalDay
```

- **Hoy:** `day = hoy en la zona del centro`, `asOf = ahora`. Se calcula en cada petición y no
  se guarda. Las jornadas abiertas cuentan hasta `asOf`.
- **Cierre:** `day = ayer en la zona del centro`, `asOf = fin del día + cola de medianoche`. Se
  calcula una vez por el cron y se guarda en `operational_daily`.

Es la misma función con el mismo código. Lo que garantiza que el hoy y el histórico cuadran no
es una prueba: es que no hay dos cálculos. Detalle en [TDR-001](./tdr/TDR-001-calculo-de-hoy.md)
y [TDR-003](./tdr/TDR-003-cierre-diario-y-semanas.md).

## 4. Plan de lectura del hoy

Todo sobre Postgres, por entidad, en **cinco consultas** que no crecen con el número de
centros:

| Paso | Lectura | Para qué |
|---|---|---|
| 1 | `dim_branches` activas de la entidad | Centros, nombre y zona |
| 2 | `dim_employees` de la entidad con estado computable | Plantilla y pertenencias |
| 3 | `dim_calendars` de la entidad (los tres niveles, una consulta) | Resolver el día previsto de cada par (empleado, centro) con `ResolveEffectiveDayUseCase` |
| 4 | `checklogs_raw` de la entidad desde el inicio del día más temprano menos 16 h hasta ahora | Jornadas de hoy y las de ayer sin cerrar |
| 5 | `tasks_raw` de la entidad con `due_at` en la ventana del día, o abiertas con `due_at` o `scheduled_start_at` pasados | Las tareas de hoy y las que arrastran |
| 5b | `item_movements_raw` de consumo de hoy, unidas a `dim_items` | Coste de material, sólo si hay movimientos |

Los nombres salen de las dimensiones; no hay lectura por persona. **Si cualquier lectura
falla, la petición falla.** Nunca una lista parcial.

El estado «computable» de la plantilla es el de disponibilidad (TDR-001 §2.1): entran
`active`, `vacation`, `sick_leave`, `leave_of_absence`, `paternity_leave`, `maternity_leave`;
quedan fuera `pending`, `inactive` y `fired`. Los cinco estados de ausencia entran para que su
ausencia se vea.

## 5. Frontera: quién decide qué

| Decisión | Dónde | Por qué |
|---|---|---|
| Quién está previsto hoy y por qué no el resto | Backend | La cascada del calendario, sobre Postgres |
| Estado de jornada e incidencias | Backend | Una copia de la regla, en `shared` |
| Si llega tarde y cuánto | Backend | Hecho medible contra la tolerancia **configurada** del turno ([ADR-005](./adr/ADR-005-el-retraso-se-calcula-contra-el-reloj.md)) |
| Si una tarea está vencida o sin empezar a destiempo | Backend | Contra el reloj, no contra el campo |
| Coste de las horas registradas | Backend | Minutos × tarifa del propio fichaje |
| Qué centro va en rojo | Backend | `alert` con clave estable; el texto, el front |
| Orden, agrupación, moneda, etiqueta de centro | Front | Presentación |
| Cuándo refrescar | Front | 60 s con la pestaña visible |

## 6. Vocabulario compartido con Presencia

Los estados de presencia son los del [contrato de Presencia](../presencia/README.md#contrato-de-api),
sin añadir ninguno:

| `presence` | Significado |
|---|---|
| `no_log` | Previsto hoy y sin ningún fichaje en ningún centro |
| `working` | Checkin válido sin checkout |
| `on_break` | Pausa abierta |
| `finished` | Checkin y checkout válidos |
| `pending_validation` | Jornada manual pendiente de que el trabajador la apruebe |
| `incomplete` | Marcada `incomplete_workday` por el saneador. «Jornada sin cerrar»; no se juzga |
| `other_branch` | Sin fichaje aquí, pero hoy fichó en otro centro suyo |

`late` **no es un estado**: es un booleano sobre `minutesFromShiftStart` y
`toleranceMinutes`, que viajan juntos. Y quien fichó sin estar previsto aparece en una lista
aparte (`unexpected`), sin juicio: puede ser un cambio de turno que el calendario no sabe.

## 7. Lo que el histórico congela

Por centro y día, al cerrarse: los totales de los tres bloques y un `detail` por persona y
por tarea, para que el «ver más» de una semana pueda decir quién acumuló retrasos sin releer
el crudo. La semana es la suma de sus días; las tasas se recalculan sobre las sumas, nunca se
promedian tasas. El día lleva `source` (`close | backfill | manual`) y el front lo marca.

## 8. Lo que se promueve a `shared`

`buildWorkSessions` sale de `attendanceSummary.ts` del front **tal cual**, con sus reglas y
sus pruebas, sobre una forma mínima de fichaje (`id`, `employeeId`, `branchId`, `type`,
`status`, `timestamp`, `checkin`, `tz`) a la que se mapean tanto un documento de Firestore
como una fila de `checklogs_raw`. El front pasa a importarla. Presencia la necesita igual:
está en su fase 1 con el mismo nombre. Quien arranque antes la hace; el otro la hereda. Misma
regla que [checklogs-http/ADR-003](../checklogs-http/adr/ADR-003-promocion-a-shared-sin-tercera-copia.md):
lo común se promueve, no se copia una tercera vez.

## 9. Frescura declarada

Cada respuesta del hoy lleva un bloque `freshness` con el último fichaje espejado de la
entidad, la última conciliación y sus huecos, la última sincronización de dimensiones y el
último espejo de tareas. No es decoración: es lo que permite al front decir «actualizado hace
2 min» o «los nombres pueden estar desactualizados» sin inventar umbrales, en la línea del
[ADR-004 de panel-operativo-v2](../panel-operativo-v2/adr/ADR-004-madurez-del-dato-explicita.md).

## 10. Rendimiento

- El hoy: cinco consultas acotadas al día sobre índices existentes
  (`idx_checklogs_entity_branch_ts`) y dos nuevos (`tasks_raw (entity_id, due_at)` y
  `(entity_id, status, due_at)`). Objetivo: < 300 ms para una entidad de 200 personas y 20
  centros, medido en dev antes de cerrar la fase 2.
- Las semanas: una consulta sobre `operational_daily` por clave primaria. Milisegundos.
- El sondeo del front cada 60 s por gerente conectado. Con 50 gerentes son 50 peticiones por
  minuto: nada. Si creciera, la respuesta es cacheable 30 s por `(entityId, branchId)`.

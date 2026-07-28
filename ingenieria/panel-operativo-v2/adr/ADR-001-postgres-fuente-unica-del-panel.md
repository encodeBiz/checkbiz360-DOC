# ADR-001 — PostgreSQL como fuente única del panel; tablas de dimensión propias

**Fecha:** 2026-07-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El panel se servía desde `FetchCheckbizStats` (Cloud Function), que lee la colección Firestore
`checkbiz_daily_report`. El módulo ya fue portado a `encodebiz-api/services/analytics`, pero el
port conservó la fuente: **sigue leyendo Firestore**.

Al mismo tiempo, el warehouse ya tiene el dato crudo. Medido en producción (2026-07-28):

- `checklogs_raw`: 1.022 filas, de las cuales **1.021 traen `schedule_applied`** (con turnos y
  `toleranceMinutes`) y **1.021 traen `employee_responsibility`** (`job`, `responsibility`,
  `level`, `price`). 1.021 con geolocalización.
- `pattern_snapshots`: 489 filas, con granularidad dual empleado/sucursal.

Es decir: **el crudo en Postgres contiene más información que el agregado de Firestore**, incluida
la que hace falta para operatividad (horario planificado) y para cohortes (puesto y
responsabilidad).

El obstáculo no es el dato de hechos, son las **dimensiones**. No existen tablas `branches` ni
`employees` en Postgres. Hoy los nombres se rescatan del JSONB de `employee_daily_reports`, que
solo tiene fila para quien llegó a generar jornada. Cobertura medida:

- 28 de 36 empleados resuelven nombre → 8 saldrían como id crudo
- 6 de 8 sucursales resuelven nombre → 2 saldrían como id crudo

---

## Opciones consideradas

**A — Mantener Firestore para el panel.** Funciona hoy, cero trabajo. Pero perpetúa el coste por
lectura, impide cualquier query analítica (percentiles, ventanas, joins entre perfiles y hechos) y
deja el panel atado a un agregado más pobre que el crudo.

**B — Postgres para métricas, Firestore para nombres.** Resuelve el 95 % pero mantiene una
dependencia viva de Firestore en la ruta caliente del panel, con su latencia y su cuota, solo para
poner etiquetas.

**C — Postgres como fuente única, con tablas de dimensión propias.** Se crean `dim_branches` y
`dim_employees`, mantenidas por el servicio `sync` que ya existe.

---

## Decisión

**Opción C.** El panel no lee Firestore. Se crean tablas de dimensión en Postgres pobladas por el
sync existente.

---

## Justificación

**Es el patrón estándar de warehouse.** Hoy hay tablas de hechos (`checklogs_raw`,
`pattern_snapshots`) sin tablas de dimensión. Por eso el nombre viaja de prestado dentro de un
JSONB de otra tabla. Es la causa raíz, no un detalle de implementación.

**Desbloquea filtros que hoy son imposibles.** Con dimensiones se puede filtrar por sucursal
activa, por puesto, por estado del empleado o por responsabilidad sin salir de SQL. Sin ellas, cada
filtro nuevo obliga a otra lectura de Firestore.

**Elimina el N+1 de raíz.** La versión original leía la colección de sucursales dos veces por
petición y los empleados uno a uno.

**Firebase sigue siendo el dueño del dato operativo.** Esto no cambia: los triggers y el cron
siguen escribiendo en Firestore, y el sync replica hacia Postgres. Lo que cambia es de dónde
**lee** el panel. No se modifica nada en Firebase.

---

## Consecuencias

**Positivas**
- Fuente única, coste de lectura estable, latencia predecible
- Métricas calculables desde el crudo, más ricas que desde el agregado
- Cohortes por puesto y responsabilidad disponibles en SQL

**Negativas / compromisos**
- Hay que construir y mantener `dim_branches` y `dim_employees`, y un backfill inicial
- Nueva dependencia: si el sync de dimensiones se para, los nombres se quedan obsoletos (los
  hechos no se ven afectados)
- `FetchCheckbizStats` queda como puente: sus 19 métricas deberán recalcularse desde
  `checklogs_raw` para completar la migración

---

## Alcance explícito

**No se modifica nada en Firebase** (`encodeBiz-SAAS`). Ni triggers, ni Functions, ni el cron
`dailyCollectorData`, que sigue escribiendo `checkbiz_daily_report` con normalidad.

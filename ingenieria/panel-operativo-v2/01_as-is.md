# 01 — Estado actual (As-Is)

**Fecha del levantamiento:** 2026-07-28
**Fuente:** código en `encodebiz-front-saas`, `encodeBiz-SAAS/functions`, `encodebiz-api`, y
**consulta directa a la base de producción** (`encodebiz_analytics`, servidor OVH).

Todos los volúmenes de este documento están medidos, no estimados.

---

## 1. Qué es hoy el panel

`encodebiz-front-saas/src/app/main/[entityId]/checkinbiz/panel/`

Tres pestañas (**Costes**, **Estimación salarial**, **Cumplimiento**) con 12 tarjetas activas
y 3 comentadas. Cada tarjeta llama por su cuenta a `useCheckbizStats` con una `metric` distinta,
contra `/api/proxy/checkinbiz_stats_panel`.

El backend era `FetchCheckbizStats` (Cloud Function, 1.298 líneas, 19 métricas), que lee la
colección Firestore `checkbiz_daily_report` y agrega en memoria.

> **Nota:** ese módulo ya fue portado a `encodebiz-api/services/analytics` (2026-07-28) con
> paridad de cálculo verificada. Este documento describe el comportamiento funcional, que no
> cambió con el port.

---

## 2. Limitaciones estructurales

| # | Limitación | Consecuencia |
|---|---|---|
| L1 | `MetricRequest` solo acepta `from`/`to`. **No existe ventana de comparación** en ningún punto de la cadena | Es imposible por diseño responder "¿mejor o peor que antes?". No es un bug: es el contrato |
| L2 | 12 tarjetas → 12 peticiones, cada una repite `findRange` del mismo rango | ~1.000 lecturas de Firestore por pintado de panel; se repite al cambiar de pestaña |
| L3 | Métricas descriptivas, sin referencia | Un número sin percentil, sin histórico y sin significancia no dice si hay que actuar |
| L4 | Comparación entre sucursales por **valores absolutos** | Compara tamaño disfrazado de rendimiento: un centro de 40 personas siempre "gasta más" que uno de 5 |
| L5 | 7 de 19 métricas dependen de `price`, que entra como `0` si no está configurado (`base.price ?? 0`) | El coste sale sesgado a la baja **sin ninguna marca**. Un dato falso con apariencia de precisión |
| L6 | Cero explotación del perfil de trabajador, arquetipos, tareas, experiencia o supervisión | El activo más diferencial del producto no aparece en pantalla |
| L7 | No hay estado de madurez del dato | Una métrica sin datos suficientes se pinta igual que una consolidada |

---

## 3. Estado real de los datos en producción (2026-07-28)

### 3.1 Volúmenes

| Tabla | Filas | Rango | Estado |
|---|---:|---|---|
| `checklogs_raw` | 1.022 | 2026-06-25 → 2026-07-28 | ✅ Sano y completo |
| `pattern_snapshots` (empleado) | 405 | desde 2026-01-01 | ✅ **El activo principal** |
| `pattern_snapshots` (sucursal) | 84 | desde 2026-07-02 | ⚠️ 26 días, con huecos |
| `employee_daily_reports` | 289 | — | ✅ |
| `task_ratings_raw` | 1 | — | ⚠️ Módulo de tareas recién estrenado |
| `daily_reports` | **0** | — | ❌ Tabla creada en `001_init.sql:85` y **nunca conectada** |

`checklogs_raw` está sorprendentemente completo: 1.021 de 1.022 filas traen `schedule_applied`
(con turnos y `toleranceMinutes`) y `employee_responsibility` (`job`, `responsibility`, `level`,
`price`), y 1.021 traen geolocalización. **Todo el cálculo operativo es posible sin salir de
Postgres.**

> **Aclaración importante:** la colección Firestore `checkbiz_daily_report` **funciona
> correctamente** — el cron `dailyCollectorData` la escribe cada hora. Lo que está vacío es la
> tabla `daily_reports` de PostgreSQL, que se creó anticipando el warehouse y nunca se pobló.
> No hay ninguna avería en producción.

### 3.2 Señales rotas o inservibles hoy

| Señal | Estado medido | Causa |
|---|---|---|
| `reliability` (sucursal) | **Constante en 0,5** los 20 días de la serie más larga | Bug conocido de `consistencyScore` / `dataQuality` |
| `profileType` (sucursal) | **`neutral` en todos** | Consecuencia de lo anterior |
| `avg_task_rating_30d` | **0 de 84** filas con valor | Solo hay 1 rating en `task_ratings_raw` |
| `HCI` | **0 de 84** filas con valor | `fetchPatternSeries` lo **lee** de `heuristic_scores`, pero `BuildPatternSnapshot` **nunca lo escribe** (no está en su lista de claves) |

Consecuencia: al pasar la serie real de producción por el motor de evidencia (TDR-007), de las 8
métricas de sucursal **6 salen `stable` sin señal y 2 `insufficient`**. Cero `keyChanges`, cero
`archetypeShifts`, cero rachas. **La capa de evolución a nivel sucursal no es publicable hoy.**

### 3.3 El activo que sí está sano: el perfil de trabajador

Los 405 snapshots de empleado tienen **todos** los campos poblados (406 de 406):

`promotionScore`, `skillLevel`, `efficiencyIndex`, `totalExperienceYears`, `avgLevel`,
`experienceByJob`, `experienceByResponsibility`, `profileType`, `reliability`, `dataQuality`,
`dataMaturity`, `weeklyStartAvg` / `weeklyEndAvg` / `weeklyWorkAvg`, `stdStartByDay` /
`stdEndByDay`, `netWorkedHours`, `costCV`, `costStd`, `effectiveRealCost`.

(`taskSignals` solo en 46 de 406 — el módulo de tareas es reciente; ver ADR-004.)

**Y existe granularidad dual**, que es la base del valor diferencial:

- 203 snapshots de empleado **con** `branch_id` → cómo rinde esa persona *en ese centro*
- 204 snapshots de empleado **sin** `branch_id` → cómo rinde esa persona *en general*
- 5 empleados tienen historial en más de una sucursal
- 27 empleados con perfil

### 3.4 Sesgo de arranque (crítico)

Distribución real de arquetipos de empleado:

| Perfil | Personas | promotionScore (min–max) | skillLevel | efficiencyIndex | Experiencia |
|---|---:|---|---:|---:|---:|
| `at-risk` | 17 | 0,193 – 0,324 | 0,24 | 0,071 | 0,21 años |
| `ghost` | 18 | 0,133 – 0,236 | 0,24 | 0,020 | 0,05 años |
| `neutral` | 9 | 0,206 – 0,370 | 0,29 | 0,076 | 0,26 años |

**Cero `anchor`, cero `high-potential`, cero `specialist`, cero `maverick`.**

`totalExperienceYears` está entre 0,05 y 0,26 años — semanas. Como `dataMaturity` crece con la
masa de datos observada, **el sistema está midiendo antigüedad en la plataforma, no calidad del
trabajador**. Un encargado con 20 años de oficio aparece como `ghost` porque CheckBiz lleva 3
meses observándolo.

El sistema hoy **confunde "todavía no lo sé" con "va mal"**. Publicar esas etiquetas tal cual
diría a un cliente que 35 de sus 44 personas están en riesgo o desaparecidas, con implicaciones
laborales serias y sin fundamento estadístico. Ver ADR-005.

### 3.5 Dimensiones ausentes

No existen tablas `branches` ni `employees` en Postgres. Los nombres se rescatan del JSONB de
`employee_daily_reports`, que solo tiene fila para quien generó jornada:

- **28 de 36** empleados resuelven nombre → 8 aparecerían como id crudo
- **6 de 8** sucursales resuelven nombre → 2 aparecerían como id crudo

Hay tablas de hechos sin tablas de dimensión. Ver ADR-001.

---

## 4. Cuestión abierta (bloquea la capa de ejecución)

`incomplete_workday` representa el **31 %** de los fichajes (317 de 1.022). Al agrupar por ciclo,
la tasa de jornadas completadas cae al 46,6 % en una sucursal.

**Falta confirmar con negocio si ese estado significa "jornada mal cerrada" o "jornada todavía
abierta"** (alguien que fichó entrada y aún no ha salido). De ello depende que el indicador de
ejecución denuncie un problema real o acuse en falso. **No se publicará ninguna métrica basada
en ese estado hasta que quede confirmado.**

---

## 5. Diagnóstico

El panel no falla por cómo dibuja: falla por **qué elige medir**. Dedica dos de sus tres pestañas
al dato más frágil del sistema (coste derivado de una tarifa que puede no existir), compara
sucursales por magnitudes que dependen del tamaño, no tiene ninguna noción de pasado, y deja sin
usar el único activo que ningún competidor del nicho posee: el perfil de trabajador con
trayectoria histórica y granularidad por centro.

# Módulo Heurística — Analytics e Indicadores Operativos

> Versión implementada: HeuristicCalculator V3 + consolidación EMA.
> Módulo: `checklogStatsUpdater` / `writeController`

## 1. Resumen

El motor heurístico convierte ciclos completos y válidos (`status: valid`, `isSuspect: false`, checkin → checkout) en métricas analíticas para medir eficiencia, fiabilidad y coste operativo por empleado y sucursal.

La consolidación usa EMA (exponential moving average) sobre patrones (`BranchPattern` y `EmployeePattern`).

**Importante:** la heurística solo procesa checkouts válidos no sospechosos. Los reportes diarios estadísticos usan todos los checklogs del día.

## 2. Métricas Generadas

### Horarias

| Campo | Descripción |
|---|---|
| `weeklyStartAvg[]` | Promedio de hora de inicio por día de la semana (detecta retrasos sistemáticos) |
| `weeklyEndAvg[]` | Promedio de hora de fin por día de la semana |
| `weeklyWorkAvg[]` | Promedio de horas netas trabajadas por día |
| `avgStartHour` | Promedio general de inicio |
| `avgEndHour` | Promedio general de salida |

### Fiabilidad

| Campo | Rango | Descripción |
|---|---|---|
| `reliability` | 0–1 | `EMA(reliability_prev, baseReliability * distanceFactor)`. ≥ 0.85 = patrón sólido; < 0.6 = irregular |
| `consistencyScore` | 0–1 | `min(1, completeCycle.length / 4)` — completitud de eventos |
| `distanceFactor` | 0.5–1.0 | Precisión geográfica via `calculateDistanceReliability()` |
| `dataPoints` | N | Volumen de registros procesados. Mín. 20 para activar heurística avanzada |

### Económicas

| Campo | Descripción |
|---|---|
| `avgCostHour` | Precio promedio por hora (input metadata) |
| `avgCycleCost` | Coste promedio por ciclo (jornada completa) |
| `avgEffectiveCost` | Coste ajustado por fiabilidad |
| `avgCostEfficiency` | Relación coste efectivo / teórico (0–1). Cercano a 1.0 = óptimo; < 0.7 = ineficiencia |

### Contextuales

| Campo | Fuente |
|---|---|
| `enableRemoteWork` | metadata del ciclo |
| `disableRatioChecklog` | metadata del ciclo |
| `distance` | metadata del ciclo |
| `gpsAccuracy` | constante 30 m |

## 3. Procesamiento — Fases

El trigger es `onChecklogWrite` en `entities/{entityId}/checklogs/{checklogId}`.

1. **Validación** — Solo procesa checkouts con `status: valid` e `isSuspect: false`
2. **Ciclo completo** — Agrupa logs del empleado con mismo `checkin` y `status: valid`
3. **Fiabilidad contextual** — Penalización por distancia sobre fiabilidad base
4. **Consistencia temporal** — Completitud de eventos (`restin`/`restout`) → `consistencyScore`
5. **Costes y eficiencia** — Coste del ciclo (`price × horas netas`), penalizaciones, EMA de costes
6. **EMA Updates** — Actualiza promedios horarios, desviaciones estándar por día, fiabilidad y coste
7. **Persistencia** — Consolida en `patterns/branch/{branchId}` y `patterns/employee/{employeeId}`

## 4. Modelo de Datos — Patrón de Sucursal

```json
{
  "branchId": "br_001",
  "weeklyStartAvg": [8.1, 8.2, 8.0, 7.9, 8.3, null, null],
  "weeklyEndAvg": [17.9, 18.0, 17.8, 17.6, 18.2, null, null],
  "weeklyWorkAvg": [8.5, 8.4, 8.3, 8.2, 8.6, null, null],
  "avgStartHour": 8.1,
  "avgEndHour": 17.9,
  "avgCostHour": 49.5,
  "avgCycleCost": 420.8,
  "avgEffectiveCost": 390.4,
  "avgCostEfficiency": 0.93,
  "reliability": 0.91,
  "dataPoints": 312,
  "updatedAt": "2025-10-25T17:00:00Z",
  "source": "update"
}
```

## 5. Ubicación en Firestore

```
entities/{entityId}/patterns/branch/{branchId}
entities/{entityId}/patterns/employee/{employeeId}
entities/{entityId}/daily_reports/{reportId}
```

## 6. Interpretación

| Métrica | Alta | Baja |
|---|---|---|
| `reliability` | Equipo estable | Inconsistencia o errores de fichaje |
| `weeklyWorkAvg` | Carga adecuada | Subutilización o abandono temprano |
| `avgCostEfficiency` | Rentabilidad saludable | Desperdicio de recursos |
| `distanceFactor` | Buena precisión GPS | Riesgo de irregularidades de ubicación |

## 7. Condición para Activar Heurística

El patrón debe estar en estado `ready` con `dataPoints >= 20` (constante en `HeuristicCore`).

Mientras el patrón no tenga suficientes datos, las métricas no se consideran estadísticamente significativas.

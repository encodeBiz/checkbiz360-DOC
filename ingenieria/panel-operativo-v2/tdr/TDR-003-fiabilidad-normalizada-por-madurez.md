# TDR-003 — Fiabilidad normalizada por madurez

**Fecha:** 2026-07-28
**Estado:** Diseño para aprobación
**Componente:** `encodebiz-api/packages/shared/src/analysis/` (nueva utilidad, consumida por el panel)
**Decisión de producto:** ADR-005

---

## Problema

`reliability = dataMaturity × dataQuality`.

`dataMaturity` crece logarítmicamente con `dataPoints`: mide **cuánto se ha observado**.
`dataQuality` mide **cómo de bien lo hace** con lo observado.

Al multiplicarlas, una persona excelente con pocas semanas de historial es indistinguible de una
persona mediocre con mucho historial. Medido en producción (2026-07-28): 35 de 44 perfiles caen en
`at-risk` o `ghost`, con `totalExperienceYears` entre 0,05 y 0,26 años. El indicador está midiendo
antigüedad en la plataforma.

Además, a nivel **sucursal** `reliability` sale **constante en 0,5** en toda la serie disponible,
por el bug conocido de `consistencyScore` / `dataQuality`. Cero varianza, cero señal.

---

## Decisión

Separar los dos componentes y **no volver a multiplicarlos para comparar**.

```typescript
interface NormalizedReliability {
  quality: number | null;      // dataQuality — lo único que entra en comparaciones
  maturity: number;            // dataMaturity — determina el ESTADO, no el valor
  observedDays: number;
  dataPoints: number;
  status: "ready" | "warming" | "unavailable";
  // Sin ranking mientras status !== "ready"
  cohortPercentile: number | null;
}
```

### Reglas

1. **Solo `quality` entra en comparaciones** entre personas o entre centros.
2. **`maturity` decide el estado**, no rebaja el valor:

   | Condición | Estado |
   |---|---|
   | `dataPoints < MIN_POINTS (20)` o `observedDays < 14` | `warming` |
   | `quality` nula o sin varianza en la serie | `unavailable` |
   | resto | `ready` |

3. **Ninguna etiqueta de arquetipo se publica si el estado no es `ready`.** En `warming` se
   devuelve el progreso (`dataPoints` sobre el mínimo), nunca `at-risk` ni `ghost`.
4. **El percentil de cohorte solo se calcula entre perfiles `ready`** del mismo `job` y
   `responsibility`, y con un mínimo de 3 miembros. Con menos, `null`.

---

## Detección de señal muerta

Antes de publicar cualquier serie de fiabilidad se comprueba que **varíe**:

```typescript
function hasSignal(series: Array<number | null>): boolean {
  const vals = series.filter((v): v is number => v !== null);
  if (vals.length < 6) return false;
  return new Set(vals.map(v => Math.round(v * 1000))).size > 1;
}
```

Si `hasSignal` es falso → `unavailable` con motivo `flat_series`. Esto habría evitado publicar la
fiabilidad de sucursal, que está clavada en 0,5, como si fuera un dato.

Es una salvaguarda de producto, **no un sustituto de arreglar el bug aguas arriba**: mientras
`consistencyScore` penalice el descanso fijo por sucursal, esa señal seguirá muerta en origen y
además seguirá inflando el modelo de sobrecoste operativo (`effectiveRealCost`), donde entra en
tres de sus cinco penalizaciones.

---

## Comparación relativa, nunca absoluta

Coherente con ADR-005, `quality` no se compara contra una escala universal sino contra:

1. **La propia línea base** de la persona o centro (deriva sobre su historia — motor TDR-007)
2. **La cohorte**: mismo `job` + `responsibility`, mínimo 3 miembros `ready`
3. **Los demás centros** del mismo cliente

Los arquetipos `at-risk` y `ghost` pasan a derivarse de una **caída observada contra la propia
línea base**, no del valor absoluto del score.

---

## Impacto esperado

Con los datos actuales, la mayoría de los 44 perfiles pasará a `warming` en lugar de `at-risk`.
Es el resultado correcto: refleja que el sistema lleva poco observando, en vez de acusar a 35
personas sin fundamento.

Conforme se acumulen `dataPoints`, los perfiles irán pasando a `ready` y el arquetipo recuperará
su valor informativo.

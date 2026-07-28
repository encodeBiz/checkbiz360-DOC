# TDR-002 — Fragilidad del centro y redundancia por puesto

**Fecha:** 2026-07-28
**Estado:** Diseño para aprobación
**Componente:** `encodebiz-api/services/analytics/src/application/BuildBranchRisk.ts` (nuevo)
**Decisión de producto:** ADR-002 (tercer eje de la espina dorsal)

---

## Qué responde

> ¿De cuántas manos depende este centro, y quién cubre si mañana falta alguien?

Dos indicadores complementarios: **fragilidad** (concentración de la operación) y **redundancia**
(relevo disponible por puesto).

---

## Fuente

`checklogs_raw` — el crudo, no el agregado. Contiene `employee_responsibility` (con `job`,
`responsibility`, `level`) en 1.021 de 1.022 filas medidas en producción, y permite reconstruir
jornadas por persona y centro sin salir de Postgres.

Para experiencia acumulada por puesto se usa `raw_pattern->>'experienceByJob'` de
`pattern_snapshots` (presente en 406 de 406).

---

## 1. Fragilidad — concentración de cobertura

### Unidad

La **jornada cubierta**, no la hora ni la persona (coherente con la regla 1 del To-Be). Una
jornada es un ciclo de trabajo identificado por `COALESCE(checkin_ref, id)`.

### Cálculo

Para cada centro y ventana, se cuenta cuántas jornadas aportó cada trabajador y se mide cuán
concentrado está el reparto con un índice de Herfindahl normalizado:

```
share(e)  = jornadas(e) / jornadas_totales_del_centro
HHI       = Σ share(e)²
HHI_norm  = (HHI - 1/n) / (1 - 1/n)      con n = nº de trabajadores del centro
```

`HHI_norm` va de 0 (reparto perfectamente equilibrado) a 1 (una sola persona lo cubre todo). La
normalización es imprescindible: sin ella, un centro de 2 personas parecería siempre más frágil
que uno de 20 por pura aritmética.

Se acompaña de dos cifras que son las que de verdad se enseñan:

```
topShare      = share del trabajador más presente
busFactor     = nº mínimo de personas que acumulan el 50 % de las jornadas
```

### Lectura publicada

| `busFactor` | Lectura |
|---|---|
| 1 | Media operación depende de una sola persona |
| 2 | Depende de dos personas |
| ≥ 3 | Reparto saludable |

El valor de `HHI_norm` **no se muestra**: se usa para ordenar. Lo que ve el usuario es
`busFactor` y `topShare` en lenguaje natural.

### Mínimos

| Condición | Estado |
|---|---|
| `n < 2` trabajadores | `unavailable` — un centro unipersonal no tiene concentración que medir |
| `jornadas_totales < 20` | `warming` |
| resto | `ready` |

---

## 2. Redundancia por puesto

### Cálculo

Para cada centro y cada `job` presente:

```
titulares(job, b)   = trabajadores con jornadas de ese job en ese centro (ventana)
capacitados(job, b) = trabajadores del centro con experiencia acumulada en ese job
                      (experienceByJob[].totalHours ≥ MIN_HOURS), aunque no lo hayan
                      ejercido en la ventana
relevo(job, b)      = capacitados - titulares
```

`MIN_HOURS = 20` como umbral inicial para considerar a alguien capacitado en un puesto. Es un
parámetro a calibrar con negocio.

### Lectura publicada

| `relevo` | Lectura |
|---|---|
| 0 | Sin relevo: si falta, no hay quien cubra |
| 1 | Relevo único |
| ≥ 2 | Cubierto |

Es la respuesta directa a "si mañana falta el de mantenimiento, ¿quién lo cubre?".

---

## 3. Agregación a nivel entidad

Coherente con ADR-002, el mismo concepto se lee arriba:

```
centrosFragiles     = nº de centros con busFactor ≤ 1
puestosSinRelevo    = nº de pares (centro, job) con relevo = 0
```

Y a nivel empleado:

```
criticidad(e, b) = share(e) en su centro
```

Que responde "cuánto depende este centro de esta persona" — la lectura individual del mismo eje.

---

## Por qué esta métrica resiste el estado actual de los datos

Sale íntegramente de `checklogs_raw`, que está sano y completo. **No depende** de `reliability`
(plano en 0,5), ni de `price`, ni de `task_ratings_raw`, ni de los arquetipos afectados por el
sesgo de arranque.

La única dependencia externa es `experienceByJob` para la redundancia, presente en el 100 % de los
snapshots de empleado.

---

## Dependencia pendiente

El recuento de jornadas requiere decidir qué ciclos cuentan como cubiertos. Mientras no se
confirme el significado de `incomplete_workday` (ver `01_as-is.md` §4), se contarán **todos los
ciclos iniciados**, que es una base neutra: la concentración de cobertura no cambia
significativamente por cómo se cierre la jornada, porque afecta por igual al numerador y al
denominador de cada trabajador.

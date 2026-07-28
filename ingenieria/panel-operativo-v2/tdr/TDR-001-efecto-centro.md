# TDR-001 — Cálculo del efecto centro

**Fecha:** 2026-07-28
**Estado:** Implementado y validado contra producción
**Componente:** `encodebiz-api/services/analytics/src/application/BuildBranchEffect.ts`
**Decisión de producto:** ADR-003

> **Revisión 2026-07-28 (v2):** la fuente cambia de `pattern_snapshots` a
> `checklogs_raw`. Ver §Fuente descartada.

---

## Qué responde

> ¿Este centro mejora o degrada a la gente que pasa por él?

Separa el **efecto del entorno** del **talento individual**, comparando a cada
trabajador consigo mismo en distintos centros.

---

## Fuente descartada: `pattern_snapshots` (por qué no vale)

El diseño inicial iba a aprovechar la granularidad dual de `pattern_snapshots`
(`employee_id` + `branch_id` para el patrón en un centro; `employee_id` con
`branch_id NULL` para el global).

**Al validar contra producción se comprobó que ambas filas contienen el mismo
patrón duplicado.** Comparación literal, misma fecha y mismo empleado:

| employee_id | dataQuality global | dataQuality centro | std global | std centro | dataPoints |
|---|---|---|---|---|---|
| `5NgXbUFL…` | 0,494062295 | 0,494062295 | 0,4150 | 0,4150 | 53 / 53 |
| `F3Girpbl…` | 0,5 | 0,5 | 1,0797 | 1,0797 | 95 / 95 |
| `IjupK1kA…` | 0,5 | 0,5 | 0,7491 | 0,7491 | 45 / 45 |

Restar una de otra da **0,0000 exacto** para todos los centros. La granularidad
dual existe en el esquema pero **no en el cálculo aguas arriba**: se escribe el
mismo patrón dos veces.

Corregirlo exigiría cambiar el cálculo del patrón en Firebase, que está fuera de
alcance. Se opta por calcular el efecto desde el crudo.

---

## Fuente adoptada: `checklogs_raw`

El crudo sí distingue por centro de forma real. Medido en producción
(2026-07-28): **7 empleados fichan en más de una sucursal**, con 25–62 fichajes
cada uno.

Validación con dos centros y las mismas personas:

| Sucursal | Personas | Δ regularidad |
|---|---:|---:|
| `1Wm37TNg…` | 2 | **−0,158** (menos regulares aquí que en su media) |
| `Gj8AsdQW…` | 5 | **+0,126** (más regulares aquí) |

Casi 17 minutos de diferencia en desviación típica de entrada, para los mismos
trabajadores. **El efecto existe y es medible.**

---

## Métricas comparadas

Por cada par (empleado, ámbito), sobre los `checkin` con `schedule_applied`:

| Métrica | Cálculo | Dirección | Peso |
|---|---|---|---:|
| **Regularidad** | `STDDEV_POP(hora_local − hora_planificada)`, acotada a 1 h y normalizada | ↓ mejor → se invierte | 0,60 |
| **Puntualidad** | `AVG(hora_local ≤ planificada + tolerancia)` | ↑ mejor | 0,25 |
| **Calidad de ciclo** | ciclos con todas las marcas `valid` y sin sospecha | ↑ mejor | 0,15 |

La regularidad domina porque es la que discrimina con más finura.

### Zona horaria (resuelto)

**Regla de dominio:** `etz` solo se rellena cuando el empleado es **remoto** —
ficha desde una zona distinta a la de su centro. Para trabajo presencial viene
vacío a propósito (34 de 991 checklogs lo traen), y entonces la zona correcta es
la de la sucursal.

Jerarquía aplicada: `etz` (remoto) → `dim_branches.tz` (presencial) → `UTC`.

Nunca el tz del empleado: al anteponerlo, la puntualidad de las entidades
españolas se desplomaba, porque `worker_meta.tz` no es fiable.

Antes de aplicar esta jerarquía todo caía a UTC y las entidades de EEUU se
desplazaban 4–5 h. Efecto medido:

| Centro | Desfase (UTC) | Desfase (tz sucursal) | Puntualidad corregida |
|---|---:|---:|---:|
| Venice Shores | +262 min | +23 min | 33 % |
| Montage at Midtown | — | +26 min | 71 % |
| St Pete Clever | — | +14 min | 70 % |
| Encodebiz | −75 min | +45 min | 59 % |
| GEST DRIVER | — | +72 min | 16 % |
| Arendel Technology | — | +143 min | 7 % |

Cinco de seis centros pasan a valores plausibles. **Arendel Technology sigue
anómalo** (+143 min): ahí la desviación no es de zona horaria sino de
configuración —el horario planificado no refleja la operativa real— o de
comportamiento. Es un caso a revisar con el cliente, no un defecto del cálculo.

---

## Algoritmo

### Paso 1 — Comportamiento por ámbito

Una sola pasada sobre `checklogs_raw` con `GROUPING SETS`, que produce a la vez la
fila por (empleado, centro) y la fila global del empleado:

```sql
GROUP BY GROUPING SETS ((employee_id, branch_id), (employee_id))
```

### Paso 2 — Score de comportamiento

```
score = (0,60 · regularidad + 0,25 · puntualidad + 0,15 · calidad) / Σ pesos presentes
```

Los pesos de las métricas ausentes se reparten entre las presentes: a nadie le
penaliza que una métrica no exista en su caso.

### Paso 3 — Delta individual

```
delta(e, b) = score(e en b) − score(e global)
```

**Solo se calcula para empleados presentes en 2 o más centros.** Para quien solo
trabaja en uno, su ámbito global *es* ese centro y el delta sería 0 por
construcción; incluirlos diluiría el efecto hacia cero — que es exactamente el
error que produjo la versión anterior.

Mínimo `MIN_CHECKINS = 8` checkins de esa persona en ese centro.

### Paso 4 — Efecto del centro

```
branchEffect(b) = mediana( delta(e, b) )
```

Mediana y no media: con pocos contribuyentes, un caso extremo mandaría.

---

## Mínimos y estados

| Condición | Estado |
|---|---|
| `contributors < 2` | `unavailable` — no se publica efecto |
| `2 ≤ contributors < 4` | `partial` — señal presente, atribución débil |
| `contributors ≥ 4` | `ready` |

Un centro sin trabajadores compartidos con otros centros **no tiene efecto
medible**. Debe explicarse así en el front, nunca dibujarse como cero.

---

## Interpretación publicada

El valor crudo no sale a pantalla; se traduce a una clave estable y el front pone
el texto:

| Rango | Clave |
|---|---|
| `> +0,10` | `potencia` |
| `+0,03` a `+0,10` | `ligeramente_positivo` |
| `−0,03` a `+0,03` | `neutro` |
| `−0,10` a `−0,03` | `ligeramente_negativo` |
| `< −0,10` | `degrada` |

Umbrales iniciales, a recalibrar con 3 meses de datos y más movilidad.

---

## Por qué resiste el estado actual de los datos

- Compara a cada persona **consigo misma** → inmune al sesgo de arranque (ADR-005)
- Sale de `checklogs_raw`, que está sano y completo (1.021 de 1.022 filas con
  `schedule_applied`)
- **No depende** de `reliability` (plano en 0,5), ni de `price`, ni de
  `task_ratings_raw`, ni de `HCI`, ni de los patrones duplicados

---

## Riesgos

**Sesgo de asignación.** Si la empresa manda sistemáticamente a sus mejores
trabajadores al centro difícil, el efecto de ese centro saldrá peor de lo que
merece. Se mitiga con la mediana, pero **no se elimina**: debe advertirse en la
documentación de producto.

**Depende de la movilidad.** Solo 7 empleados multi-centro hoy, concentrados en
una entidad. Los centros sin personal compartido salen `unavailable`. La cobertura
crece sola conforme haya rotación entre centros.

**Depende de `dim_branches.tz`.** Si el poblado de dimensiones no ha corrido, los
centros presenciales caen a UTC y la puntualidad se desploma. El job de
sincronización es prerrequisito operativo de esta métrica, no un accesorio.

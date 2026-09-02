# TDR-001 — Cálculo de disponibilidad: plan de lectura, reglas y límites

**Fecha:** 2026-09-02
**Estado:** Diseño
**Componente:** Firebase Functions — `checkinbiz` / módulo `calendar`
**Decisiones de referencia:** [ADR-001](../adr/ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md) · [ADR-002](../adr/ADR-002-entityid-en-los-documentos-de-calendario.md)

---

## Resumen

Dos casos de uso nuevos, `ResolveAvailabilityUseCase` y `ResolveAvailabilityDayUseCase`, que
comparten la misma resolución y se diferencian sólo en qué devuelven: la suma o los nombres.

Las reglas de este documento no son nuevas: están implementadas y probadas contra la vista en
`src/lib/common/availability.ts` del prototipo, y se recogen aquí para que el backend las
reproduzca exactamente. Es la parte del prototipo que sobrevive, aunque el código no lo haga.

---

## 1. Plan de lectura

| Paso | Lectura | Coste |
|---|---|---|
| 1 | `entities/{e}/calendar/config` | 1 doc |
| 2 | `entities/{e}/branches` con `status != 'inactive'` | 1 query, B docs |
| 3 | `entities/{e}/employees` con estado computable (§2.1) | 1 query, N docs |
| 4 | Configs de las B sucursales | 1 `getAll`, B docs |
| 5 | Configs de los empleados | 1 query `collectionGroup` (ADR-002) o 1 `getAll` de N referencias |

Todo se lee una vez por petición, antes de evaluar ningún día. El rango de fechas **no** afecta
al plan de lectura: se leen los mismos documentos para un día que para un mes.

**Si cualquier lectura falla, la petición falla.** No hay degradación parcial: es la corrección
central de lo que hacía mal el prototipo, donde una lectura fallida se interpretaba como
herencia y acababa inflando la cobertura.

## 2. Resolución

### 2.1 Quién cuenta como plantilla

Entran: `active`, `vacation`, `sick_leave`, `leave_of_absence`, `paternity_leave`,
`maternity_leave`.

Quedan fuera: `pending` (todavía no se ha incorporado) e `inactive` (ya no está). No son
plantilla que pueda cubrir un turno, así que no deben engordar el denominador.

Los cinco estados de ausencia **sí** entran, y entran precisamente para que su ausencia se vea:
si no contaran, una plantilla de baja daría 100% de cobertura.

### 2.2 Unidad de cálculo: el par (empleado, sucursal)

Un empleado pertenece a varias sucursales (`branchId: string[]`) y su horario efectivo es
**distinto en cada una**, porque la capa intermedia de la herencia cambia. La unidad no es el
empleado: es el par.

Quien está en dos sucursales cuenta en las dos filas. La suma de `total` de los grupos puede
superar `headcount`, y por eso ambos van en la respuesta.

Quien no tiene ninguna sucursal válida cae en el grupo `__unassigned__`, con el horario de la
entidad y sus festivos.

### 2.3 Horario efectivo

La cascada de siempre, la de `ResolveEffectiveCalendarUseCase`:

```
entity.defaultSchedule
  └─ branch.overridesSchedule    si branch.overridesDisabled !== true
      └─ employee.overridesSchedule  si employee.overridesDisabled !== true
```

Día a día, no en bloque: un nivel que define sólo el martes hereda el resto.
`overridesDisabled` es `true` cuando el documento no existe.

Un día se normaliza así, aplanando las tres formas históricas del dato: `disabled` manda sobre
`enabled`; si hay `shifts` no vacío se usa; si no, se cae a `start`/`end` sueltos; si tampoco,
9:00–17:00.

### 2.4 Días libres

Se indexan por fecha, con las capas heredadas primero y **sin pisarse**:

1. Festivos de la entidad → `source: entity`
2. Festivos de la sucursal → `source: branch`
3. Festivos propios del empleado (las ausencias) → `source: employee`

Que el heredado gane es deliberado: si alguien tiene una ausencia el mismo día que un festivo de
la entidad, ese día es festivo. De esa precedencia depende que el día se lea como descanso y no
como agujero de cobertura (§3).

## 3. Reglas de evaluación

### Precedencia del motivo

Para cada par (empleado, sucursal) y cada día, en este orden y parando en el primero que se
cumpla:

| # | Motivo | Cuándo |
|---|---|---|
| 1 | `noShift` | El horario efectivo no tiene turno ese día de la semana |
| 2 | `holiday` | Hay festivo de entidad o de sucursal esa fecha |
| 3 | `absence` | Hay ausencia propia del empleado esa fecha |
| 4 | `employeeStatus` | El estado de la ficha no es `active` |

Si no se cumple ninguno, **disponible**, y sus turnos son los del horario efectivo.

**El orden importa y no es arbitrario.** Quien está de baja un día festivo cae bajo `holiday`,
no bajo `employeeStatus`. Sin eso, un festivo con una sola persona de baja dejaría de contar
como descanso y aparecería en rojo como si faltara gente.

### Día cerrado

```
closed = total > 0
      && available === 0
      && todos los motivos ∈ { noShift, holiday }
```

Es *nadie trabaja y nadie debería*: fin de semana, o festivo para todo el grupo. Basta una baja
o una ausencia para que el día vuelva a ser cobertura y `closed` sea `false` — porque entonces
sí hay gente que debería estar y no está.

`closed` es dato, no estilo: distingue el gris del rojo, y esa distinción no la puede tomar el
cliente sin conocer los motivos de cada persona.

## 4. Límites

| Límite | Valor propuesto | Respuesta al superarlo |
|---|---|---|
| Rango de fechas | 62 días | `400 calendar/range_too_long` con `{ days, limit }` |
| Plantilla sin `branchId` | 1000 empleados computables | `400 calendar/headcount_too_large` con `{ headcount, limit }` |

El tope de plantilla se comprueba **después del paso 3** y antes de leer configs: si hay que
rechazar, que sea barato. Con `branchId` no aplica, porque el conteo ya está acotado a una
sucursal.

Nada se trunca en silencio. Un tablero al que le faltan personas da un número plausible y
equivocado, que es exactamente lo que hay que evitar.

## 5. Permisos

Trabajo nuevo: el handler de calendario no discrimina hoy por nivel de responsabilidad, y estas
dos acciones devuelven nombres de toda la plantilla.

| Nivel | Alcance |
|---|---|
| `owner`, `manager` | Todas las sucursales de la entidad |
| `supervisor` | Sólo aquellas donde tiene responsabilidad; `branchId` fuera de ellas → `403` |
| `worker` | `403` sin excepción |

Sólo Firebase ID token. El staff JWT de la app móvil no se acepta: un empleado no tiene por qué
saber quién está de baja.

## 6. Casos borde

| Caso | Comportamiento |
|---|---|
| Entidad sin sucursales | Un solo grupo, `__unassigned__`, con toda la plantilla |
| Sucursal sin empleados | No sale en `rows`. Un grupo vacío no dice nada |
| Empleado con `branchId` que apunta a una sucursal inactiva o borrada | Esa pertenencia se ignora; si no le queda ninguna, cae en `__unassigned__` |
| Entidad sin `calendar/config` | Se aplica el horario por defecto L-V 9:00–17:00, el mismo que enseña la pestaña de entidad |
| Festivo con fecha mal formada | Se descarta y se registra en log. No tumba la petición |
| Empleado sin `fullName` | Se responde con el email; si tampoco, con el id |
| Rango que cruza el cambio de hora | Irrelevante: se opera con fechas civiles `YYYY-MM-DD`, no con instantes |

## 7. Qué NO cambia

- `GET /calendar` (calendario efectivo), `PATCH`, `DELETE` y `POST?action=savePreset` siguen
  exactamente igual. Estas dos acciones son aditivas.
- No hay colección nueva, ni escritura, ni migración de datos — salvo el backfill de `entityId`
  del [ADR-002](../adr/ADR-002-entityid-en-los-documentos-de-calendario.md), que es un campo y
  es idempotente.
- `ResolveEffectiveCalendarUseCase` no se toca. Se reusa su lógica, no se modifica.

## 8. Verificación

La prueba que importa no es que el número parezca razonable, sino que **la agregación y la
resolución individual no se contradigan**: para una entidad de dev con festivos de entidad,
festivos de sucursal y ausencias de empleado, la rejilla tiene que coincidir, empleado a
empleado y día a día, con lo que devuelve `GET /calendar` preguntado uno por uno. Si divergen,
hay dos verdades y el módulo ha vuelto al problema que este diseño venía a quitar.

Casos mínimos: día normal, fin de semana, festivo de entidad, festivo de sucursal, ausencia de
empleado, baja de ficha, baja de ficha **en** festivo (que debe salir como `holiday` y dejar el
día `closed`), y empleado en dos sucursales.

## 9. Fuera de alcance (deuda registrada)

- **`Absence` con rango real.** Hoy son N festivos de un día. Para calcular da igual; para
  escribir y para explicar, no. Deuda §6.8 de [modulos/calendario.md](../../../modulos/calendario.md).
- **Estados de ficha sin fechas.** `vacation`, `sick_leave` y compañía son banderas
  permanentes: la disponibilidad sólo puede tratarlas como "no disponible en todo el rango".
  Con `Absence` real, esto lo absorbería el calendario.
- **Turno por día y sucursal.** No existe en el modelo, y sin él no se puede distinguir "libra"
  de "hoy trabaja en otro centro". Es el motivo por el que "turno en otra sucursal" quedó fuera
  del diseño de la vista.
- **Materialización de la rejilla.** Fase 4, y sólo con una medida delante.

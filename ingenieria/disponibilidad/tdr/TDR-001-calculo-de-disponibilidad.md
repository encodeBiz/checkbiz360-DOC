# TDR-001 — Cálculo de disponibilidad: plan de lectura, reglas y límites

**Fecha:** 2026-09-02 · **Revisado:** 2026-09-02 (verificado contra datos reales de dev)
**Estado:** Diseño
**Componente:** `services/checkinbiz` (contenedor) + `@encodebiz/shared` — módulo `calendar`
**Decisiones de referencia:** [ADR-001](../adr/ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md) · [ADR-002](../adr/ADR-002-entityid-en-los-documentos-de-calendario.md) · [ADR-005](../adr/ADR-005-snapshot-del-calendario-resuelto-en-postgres.md)

---

## Resumen

Dos casos de uso nuevos, `ResolveAvailabilityUseCase` y `ResolveAvailabilityDayUseCase`, en
`@encodebiz/shared`, expuestos como dos rutas del `calendarRouter` del contenedor. Comparten la
misma resolución y se diferencian en qué devuelven: la suma o los nombres.

**No traen reglas nuevas.** Reusan `ResolveEffectiveCalendarUseCase`, que ya resuelve la
cascada para el fichaje, para la app y para las horas planificadas. Lo único que cambia es la
**forma del bucle**, y hay un prerrequisito en el resolutor.

---

## 0. Prerrequisito: el `source` de los festivos

`ResolveEffectiveCalendarUseCase` fusiona los festivos de los tres niveles en una lista plana y
**tira el nivel**. Verificado contra dev: para un empleado con vacaciones propias, `GET /calendar`
devuelve diez festivos donde la Navidad de la entidad, el festivo de la sucursal y sus ocho días
de vacaciones son indistinguibles.

Sin el nivel no se puede calcular `closed` (§3), que es la mitad de lo que el tablero promete.
El arreglo —cinco líneas en `concatHolidays`, aditivo y auditado consumidor a consumidor— es la
**TAREA 2** de [06_tareas.md](../06_tareas.md) y **bloquea esta fase**.

## 1. Plan de lectura

El contenedor corre en OVH y Firestore está en GCP: lo que se paga son **round trips**, no sólo
lecturas facturadas. El plan minimiza los primeros.

| Paso | Lectura | Round trips |
|---|---|---|
| 1 | `entities/{e}/calendar/config` | 1 |
| 2 | `entities/{e}/branches` con `status != 'inactive'` | 1 |
| 3 | `entities/{e}/employees` con estado computable (§2.1) | 1 |
| 4 | Configs de las B sucursales — `getAll` | 1 |
| 5 | Configs de los empleados — `getAll` de N referencias, o `collectionGroup` ([ADR-002](../adr/ADR-002-entityid-en-los-documentos-de-calendario.md)) | 1 |

Cinco idas y vueltas, independientemente del tamaño de la plantilla. Nunca `getDoc` en bucle:
eso convierte N lecturas en N viajes entre nubes, que es exactamente lo que hacía el prototipo
mal.

Todo se lee una vez por petición, antes de evaluar ningún día. **El rango de fechas no afecta al
plan de lectura**: se leen los mismos documentos para un día que para un mes.

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
superar `headcount`, y por eso ambos van en la respuesta. **Es un sobreconteo conocido**: sin
asignación de turno por día y sucursal (§9) no se puede saber en cuál de las dos está esa
persona ese día, así que se la cuenta como disponible en ambas.

Quien no tiene ninguna sucursal válida cae en el grupo `__unassigned__`, con el horario de la
entidad y sus festivos.

### 2.3 Un bucle distinto, no reglas distintas

`ResolveEffectiveDayUseCase` ya responde "¿trabaja esta persona este día?" —y acierta: se
comprobó contra dev en festivo de entidad, festivo de sucursal, vacaciones propias, sábado y día
normal—. Pero **resuelve el calendario entero en cada llamada**: por empleado y por día serían
N × días resoluciones completas, inviable.

La disponibilidad resuelve **una vez por par (empleado, sucursal)** y recorre los días del rango
en memoria sobre ese resultado. Mismas reglas, una resolución en lugar de treinta.

### 2.4 Horario efectivo y días libres

La cascada de siempre, la de `ResolveEffectiveCalendarUseCase`:

```
entity.defaultSchedule
  └─ branch.overridesSchedule    si branch.overridesDisabled !== true
      └─ employee.overridesSchedule  si employee.overridesDisabled !== true
```

Día a día, no en bloque. `overridesDisabled` es `true` cuando el documento no existe.

**`overridesDisabled` corta el horario, no los festivos.** Los festivos de los tres niveles se
concatenan siempre. Comprobado en dev: con `overridesDisabled: true` en sucursal y empleado, el
horario sale de la entidad (`sources.schedule = "entity"`) y aun así llegan los festivos de los
tres. Es coherente —un festivo es aditivo, no un override— pero no estaba escrito.

Los días libres se indexan por fecha conservando su `source` (§0), que es lo que permite
distinguir *cierra la empresa* de *libro yo*.

## 3. Reglas de evaluación

### Disponible

```
disponible = tiene turno ese día de la semana
          && no hay día libre en esa fecha (de cualquier nivel)
          && el estado de la ficha es 'active'
```

### El motivo: dos cubos, y luego una etiqueta

Todo el cálculo se apoya en una sola distinción, y de ella salen tanto `closed` como el `reason`
del contrato:

- **Colectivo** — el horario no tiene turno ese día, o hay un día libre con `source` de entidad
  o de sucursal. Le pasa a todo el grupo por igual.
- **Personal** — día libre propio del empleado, o su ficha no está `active`.

**Lo colectivo se mira primero.** Si alguien está de baja un día festivo de la empresa, ese día
es festivo, no baja: sin esa precedencia, un festivo con una sola persona de baja dejaría de
leerse como descanso y aparecería en rojo como si faltara gente. Es la única regla de orden que
hay, y sustituye a la tabla de precedencias de cuatro niveles de la versión anterior.

Etiquetar es entonces un paso más sobre el cubo ya elegido:

| Cubo | `reason` | Cuándo |
|---|---|---|
| Colectivo | `noShift` | El horario efectivo no tiene turno ese día de la semana |
| Colectivo | `holiday` | Día libre con `source` de entidad o de sucursal |
| Personal | `absence` | Día libre propio del empleado (`source: employee`) |
| Personal | `employeeStatus` | El estado de la ficha no es `active` |

`absence` es el único reversible desde el panel, y por eso es el único que lleva `absenceId` y
`paid` en la respuesta ([ADR-003](../adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md),
[ADR-004](../adr/ADR-004-ausencias-retribuidas.md)). Los otros tres se explican y se bloquean.

**Todo esto depende del `source` (§0).** Sin él no se distingue `holiday` de `absence`, que es
la línea que separa el gris del rojo y lo reversible de lo que no.

### Día cerrado

```
closed = total > 0
      && available === 0
      && ningún ausente lo está por un motivo personal
```

*Nadie trabaja y nadie debería*: fin de semana, o festivo para todo el grupo. Basta una ausencia
personal para que el día vuelva a ser cobertura, porque entonces sí hay gente que debería estar
y no está.

`closed` es **dato, no estilo**: distingue el gris del rojo, y esa distinción no la puede tomar
el cliente sin conocer los motivos. Sin él, cada sábado saldría 0 de N en rojo igual que una
catástrofe de cobertura, y un tablero que grita ocho días de cada treinta por diseño enseña a no
mirarlo.

## 4. Límites

Los dos límites no hacen el mismo trabajo, y conviene no confundirlos:

| Límite | Valor | Qué protege | Respuesta |
|---|---|---|---|
| Rango de fechas | 62 días | El **tamaño de la respuesta** y las celdas a evaluar. No las lecturas: §1 no depende del rango | `400 calendar/range_too_long` con `{days, limit}` |
| Plantilla sin `branchId` | 1000 computables | Las **lecturas**. Es el único que acota el coste real | `400 calendar/headcount_too_large` con `{headcount, limit}` |

El tope de plantilla se comprueba **después del paso 3** y antes de leer configs: si hay que
rechazar, que sea barato.

Nada se trunca en silencio. Un tablero al que le faltan personas da un número plausible y
equivocado, que es exactamente lo que hay que evitar.

## 5. Permisos

| Nivel | Alcance |
|---|---|
| `owner`, `manager` | Todas las sucursales de la entidad |
| `supervisor` | Sólo aquellas donde tiene responsabilidad; `branchId` fuera de ellas → `403` |
| `worker` | `403` sin excepción |

Sólo Firebase ID token. El staff JWT de la app móvil no se acepta: un empleado no tiene por qué
saber quién está de baja.

No es trabajo desde cero: `resolveActorByUid` de `services/tasks/src/interfaces/http/task/task.helpers.ts`
ya hace exactamente esta resolución con `ResponsibilityLevel` y `findResponsibilities`, ambos en
`shared`. Se sube el resolutor a `shared` y se llama.

**Pendiente de decidir:** `headcount` es hoy la plantilla de toda la entidad, así que un
`supervisor` vería el tamaño de la empresa. O se acota a su alcance, o se documenta y se acepta.
Ídem con si el grupo `__unassigned__` le llega o no.

## 6. Casos borde

| Caso | Comportamiento |
|---|---|
| Entidad sin sucursales | Un solo grupo, `__unassigned__`, con toda la plantilla |
| Sucursal sin empleados | No sale en `rows`. Un grupo vacío no dice nada |
| `branchId` que apunta a sucursal inactiva o borrada | Esa pertenencia se ignora; si no le queda ninguna, cae en `__unassigned__` |
| Entidad sin `calendar/config` | Horario por defecto L-V 9:00–17:00, el mismo que enseña la pestaña de entidad |
| Festivo con fecha mal formada | Se descarta, **se cuenta y se informa en la respuesta**. Descartar en un log y devolver un número entero es el mismo fallo que este diseño rechaza, sólo que más pequeño |
| Empleado sin `fullName` | Se responde con el email; si tampoco, con el id |
| Rango que cruza el cambio de hora | Irrelevante: se opera con fechas civiles `YYYY-MM-DD` |

## 7. Qué NO cambia

- `GET /calendar` (calendario efectivo), y las escrituras de calendario, siguen igual salvo el
  campo `source` añadido a `holidays[]`, que es aditivo y está auditado en
  [06_tareas.md](../06_tareas.md).
- No hay colección nueva en Firestore, ni escritura, ni migración de datos.
- `ResolveEffectiveCalendarUseCase` no se reescribe. Se le añade el `source` y se reusa.

## 8. Verificación

La prueba que importa no es que el número parezca razonable, sino que **la agregación y la
resolución individual no se contradigan**: para una entidad de dev con festivos de entidad,
festivos de sucursal y ausencias de empleado, la rejilla tiene que coincidir, empleado a empleado
y día a día, con lo que devuelve `GET /calendar` preguntado uno por uno. Si divergen, hay dos
verdades y el módulo ha vuelto al problema que este diseño venía a quitar.

Casos mínimos: día normal, fin de semana, festivo de entidad, festivo de sucursal, vacaciones de
empleado, baja de ficha, baja de ficha **en** festivo (que debe dejar el día `closed`), y
empleado en dos sucursales.

Hay ya un banco de pruebas real en dev —entidad `Wl8ZCvpdmIXzEE0mhT7W`— con festivo de entidad,
festivo de sucursal, ocho días de vacaciones propias y overrides desactivados en dos niveles. Le
faltan un segundo centro y alguien en los dos.

## 9. Fuera de alcance (deuda registrada)

- **`Absence` con rango real.** El tipo, la API y la validación de solapamiento existen; el panel
  no los usa —`EmployeeAbsencesModal` tipa sus ausencias como `Holiday`— y el resolutor no lee
  `absences[]`. Latente hoy (en dev está vacío), activo el día que alguien use esa vía: entonces
  la app y el tablero dirían una cosa y `BuildPlannedHours` otra.
- **Estados de ficha sin fechas.** `vacation`, `sick_leave` y compañía son banderas permanentes,
  así que una ficha que nadie devolvió a `active` resta cobertura para siempre. Con `Absence`
  real esto lo absorbería el calendario.
- **Turno por día y sucursal.** No existe en el modelo, y sin él quien está en dos centros cuenta
  en los dos (§2.2). Conviene medir cuánta plantilla real está en esa situación antes de decidir
  si es nota al pie o problema.
- **Materialización.** [ADR-005](../adr/ADR-005-snapshot-del-calendario-resuelto-en-postgres.md),
  después de la Fase 2.

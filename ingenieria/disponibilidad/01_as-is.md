# 01 — Estado actual (As-Is)

## No hay disponibilidad en ninguna parte

Ni colección, ni endpoint, ni caso de uso. La disponibilidad no está guardada: es una pregunta
que hoy no se le puede hacer al sistema. Lo que sí existe es todo lo necesario para
responderla, repartido en tres sitios que nunca se han cruzado.

## Lo que ya existe

### El módulo calendario (backend), que está partido en dos

**Lectura, en el contenedor.** `services/checkinbiz` sirve
`GET /api/v1/checkinbiz/calendar` desde `interfaces/http/calendar/`, y la regla de herencia vive
en `@encodebiz/shared`:

```
packages/shared/src/calendar/resolveEffectiveCalendar.usecase.ts   ← la cascada
packages/shared/src/calendar/resolveEffectiveDay.usecase.ts        ← ¿trabaja este día?
packages/shared/src/calendar/Calendar.ts                            ← WeeklySchedule, Holiday, AbsenceRange
```

De ahí la consumen también el fichaje, la edición de fichaje y `BuildPlannedHours` de analytics.
Es núcleo compartido, no un rincón del panel.

**Escritura, todavía en Firebase.** `calendarHandler` conserva `upsertEntity/Branch/Employee`,
`delete` y `savePreset`, con **una copia entera del caso de uso** en
`encodeBiz-SAAS/functions/src/services-saas/checkinbiz/application/calendar/`. El panel escribe
contra esa Cloud Function.

`GET` devuelve el calendario efectivo de un scope: horario semanal fusionado, festivos
concatenados de los tres niveles, `sources` y `overridesDisabled`. Detalle en
[modulos/calendario.md](../../modulos/calendario.md).

**Y aplana el origen de los festivos**, que es la limitación que condiciona todo el diseño:
`concatHolidays` mete los tres niveles en una lista y tira el nivel. Comprobado contra dev — ver
[06_tareas.md](./06_tareas.md), TAREA 2.

### Los datos

```
entities/{entityId}/calendar/config                              ← defaultSchedule, advance, holidays[]
entities/{entityId}/branches/{branchId}/calendar/config          ← overridesSchedule, overridesDisabled, holidays[]
entities/{entityId}/employees/{employeeId}/calendar/config       ← ídem; sus holidays[] son las ausencias
entities/{entityId}/employees/{employeeId}                       ← status, branchId[]
entities/{entityId}/branches/{branchId}                          ← name, status
```

Prioridad alta → baja: employee override → branch override → entity default, cada nivel cortado
por su `overridesDisabled`.

### El prototipo (front)

Rama `feat/disponibilidad-horarios` de `encodebiz-front-saas`, tercera pestaña de *Horarios y
festivos*:

```
src/domain/features/checkinbiz/IAvailability.ts                  ← modelo de vista
src/lib/common/availability.ts                                    ← reglas puras: merge, evaluación por día, rejilla
src/services/checkinbiz/availability.service.ts                   ← el cruce contra Firestore
src/app/main/[entityId]/checkinbiz/calendar/components/
  AvailabilityTab.tsx                                             ← tablero, filtros, export
  AvailabilityDayDetail.tsx                                        ← desglose de un día
```

La vista funciona y es la que se conserva. Lo que no se conserva es
`availability.service.ts`, que es donde está el problema.

## Lo que cuesta hoy, por carga del tablero

| Lectura | Cantidad | Round trips |
|---|---|---|
| Config de la entidad | 1 doc | 1 |
| Listado de sucursales | 1 query | 1 |
| Listado de empleados (documentos completos) | 1 query, N docs | 1 |
| Config de cada sucursal | B docs | B |
| **Config de cada empleado** | **N docs** | **N** |

Las N últimas son `getDoc` sueltos: el SDK web no tiene lectura por lotes. Con el pool de 12
del prototipo, 200 empleados son ~17 tandas.

| Plantilla | Round trips | Espera estimada antes de pintar |
|---|---|---|
| 20 | ~24 | despreciable |
| 200 | ~204 | 1,5 – 3 s |
| 500 | ~504 | 4 – 7 s |
| 1000 | ~1004 | ~10 s |

Lo que **no** es problema: la CPU y la memoria del navegador. 200 empleados × 31 días son 6.200
evaluaciones — milisegundos. Y las lecturas de Firestore cuestan céntimos. El agrupamiento y el
pintado en el cliente aguantan de sobra; lo que no aguanta es la forma de traerse los datos.

## Limitaciones del modelo actual

1. **Coste lineal con la plantilla, pagado por cada navegador.** El mismo cruce se repite
   entero en cada pestaña que se abre, sin poder compartirse ni cachearse.
2. **Obliga a reglas de Firestore abiertas.** Cruzar desde el cliente exige que cualquier
   usuario del panel pueda leer el calendario de cualquier empleado. Además, las reglas de dev
   están abiertas desde diciembre de 2025, así que este problema **no se reproduce en dev**:
   aparecería directamente en producción.
3. **Los fallos se convierten en números optimistas.** `readConfig` trata cualquier error como
   "no hay documento", que en la cascada significa "hereda, sin ausencias" — o sea, empleado
   **disponible**. Un `permission-denied` no da error: infla la cobertura.
4. **Tercera copia de la regla de herencia.** `ResolveEffectiveCalendarUseCase` la tiene en el
   backend; `BranchCalendarDetail` y `EmployeeCalendarDetail` la reimplementan cada uno en el
   front; `lib/common/availability.ts` la reimplementa una tercera vez. El día que cambie la
   precedencia, el tablero mentirá sin avisar.
5. **Nada de esto es paginable ni acotable.** La rejilla necesita a *toda* la plantilla para
   contar; no hay forma de traer "la primera página" de una suma.

## Deudas del modelo que la disponibilidad hereda

No son culpa del tablero, pero lo condicionan y conviene tenerlas escritas:

- **Las ausencias no tienen rango, en la práctica.** `AbsenceRange` (con
  `startDate`/`endDate`/`status`) existe en `shared`, tiene API —`upsertEmployeeCalendar` acepta
  `absence` y valida solapamientos— y `BuildPlannedHours` ya la consume. Pero el panel no la usa:
  `EmployeeAbsencesModal` tipa sus ausencias como `Holiday` y guarda N festivos de un día, uno
  por `PATCH`. Verificado en dev: ocho entradas para unas vacaciones del 11 al 18 de noviembre,
  `absences` vacío. Encarece la escritura y, peor, deja dos modelos donde el resolutor sólo lee
  uno.
- **El estado del empleado no tiene fechas.** `status: vacation | sick_leave | …` es una
  bandera permanente en la ficha, sin desde–hasta. La disponibilidad sólo puede tratarla como
  "no disponible durante todo el periodo consultado".
- **No hay asignación de turno por día y sucursal.** Un empleado pertenece a varias sucursales
  (`branchId: string[]`) pero no hay dato de en cuál trabaja cada día. Por eso no se puede
  distinguir "libra" de "hoy está en otro centro", y quien está en dos sucursales cuenta en las
  dos filas.

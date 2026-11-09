# TDR-008 — Heurística: el horario se mide contra lo planificado de cada ciclo

**Fecha:** 2026-11-08
**Estado:** Implementado en `fix/heuristica-por-tareas` (encodebiz-api), sin desplegar
**Componentes:** `packages/shared/src/analysis/planTiming.ts`, `services/analytics/src/application/heuristic/*`, `services/analytics/src/interfaces/heuristic.router.ts`, `services/merlin` (interpretación de persona y sucursal)

---

## Problema

`POST /api/analytics/heuristic` evalúa las reglas de `engine_rules` y el perfil sobre el patrón
de Firestore. La variabilidad (`stdStartHour`, `stdEndHour`) es la desviación típica de la **hora
del reloj** a la que se entra y se sale. Eso solo se parece a la constancia con un turno fijo.
Con «Por turnos», y sobre todo con «Por tareas» (una tarea es un ciclo, a una hora distinta del
día), la hora del reloj se mueve porque **el plan** se mueve.

En la demo de SaludStart (staging, 28 personas «Por tareas») salía:

- `correct_high_variability` («variabilidad horaria elevada, revisar planificación») para 25 de 28,
  con `stdStartHour` entre 1 y 2,3 h, cuando la entrada mediana está a ±3 min de la hora de su
  tarea y entre el 85 % y el 100 % de las entradas caen dentro de la tolerancia.
- Perfil `maverick` para 26 de 28: el clasificador lee `taskSignals.taskCount`, que no existe en
  esos patrones (y que solo cuenta tareas validadas o rechazadas). Con `taskCount = 0` decide solo
  por la variabilidad del reloj, aunque cada persona haya terminado entre 24 y 86 tareas.
- `coaching_low_efficiency` («aprovechamiento parcial de la jornada») para 2: no es la misma
  causa. `efficiencyIndex` es una media móvil de calidad de datos × madurez del patrón
  (`fichaje/helper.ts`: «calidad de datos del ciclo, no eficiencia operativa real»), y esas dos
  personas tienen menos ciclos (24 y 26). Trabajaron el 88-89 % de lo planificado.

## Decisión

La capa que **lee** el patrón calcula una vista, sin escribir nada en Firestore (los triggers que
acumulan el patrón no se tocan):

1. **Desvío contra el plan del ciclo.** Del espejo (`checklogs_raw`, últimos 90 días) se toma cada
   entrada con su salida y el `schedule_applied` de la entrada. El plan de un ciclo es su tarea
   (`taskId` → `start`/`end`) o, sin tarea, el turno del día cuya entrada queda más cerca del
   fichaje (un día con mañana y tarde tiene dos). Vale para los tres modos. No cuenta como plan
   `source: "default"` ni una ventana de 20 h o más (el 00:00–23:59 de respaldo, que en staging
   llega también con `source: "entity"`).
2. **Medida robusta.** Dispersión = (P90 − P10) / 2,563 del desvío en minutos. Con datos normales
   vale lo mismo que una desviación típica, así que los umbrales de `engine_rules` (0,8 h) y del
   clasificador siguen significando lo mismo. Un 1 % de fichajes atípicos (un olvido corregido
   horas después) no la mueve, a diferencia de la desviación típica; si un 10 % o más de los
   ciclos se sale del plan, sí. Se descartó la MAD (rompe al 50 %): ocultaría a quien se salta
   el plan una vez de cada tres.
3. **Con plan**, la vista pone `stdStartHour`/`stdEndHour` = dispersión contra el plan (en horas)
   y `efficiencyIndex` = lo trabajado frente a lo planificado (Σ trabajado / Σ planificado, tope 1),
   que es lo que dice la regla. **Sin plan** (menos de 10 ciclos con plan o menos de la mitad),
   el patrón tal cual, como hasta ahora.
4. **Tareas para el perfil**, de `tasks_raw`: terminadas en 90 días, parte en plazo
   (`time_compliance_status`) y rechazadas. Se usa el mayor de `taskSignals.taskCount` y lo
   terminado. Una señal que falta (sin valoraciones, sin veredicto de plazo) es **sin evidencia**
   (`null`), nunca 0: con 0, alguien con 40 tareas y sin valoraciones salía `at-risk`.
5. La respuesta añade `timing` (base `plan`/`clock`, mediana y dispersión de entrada y salida,
   puntualidad, cobertura del plan, ciclos) y `tasks`. Si Postgres falla, `timing: null` y se
   evalúa el patrón como antes.
6. **Merlin** recibe la misma vista: la «consistencia de entrada/salida» se presenta como desvío
   respecto a la hora planificada, con la puntualidad; en «Por tareas» no se enseña una «hora
   habitual» de entrada y salida (es la media de tareas repartidas por el día) y el aprovechamiento
   se presenta como tiempo trabajado frente al planificado.

## Resultado con SaludStart (datos de staging del 08-nov)

| | Antes | Después |
|---|---|---|
| `correct_high_variability` | 25 | 0 |
| `coaching_low_efficiency` | 2 | 0 |
| Perfil | 26 `maverick`, 2 `neutral` | 16 `anchor`, 12 `neutral` |

Dispersión de la entrada contra el plan: entre 2,5 y 12,6 min. La prueba
`services/analytics/test/heuristicPlanTiming.test.ts` incluye a una persona irregular de verdad
(desvíos de −90 a +120 min respecto a su tarea): recibe la regla y sale `maverick`.

## Lo que no cambia

- El patrón de Firestore y su `profileType` guardado: los escribe el trigger con la hora del reloj.
  Quien lea `profileType` del documento, y no de esta ruta, sigue viendo `maverick`.
- `skillLevel` y `promotionScore` llevan dentro la variabilidad del reloj (se calculan en el
  trigger). Las reglas que los usan no se recalculan aquí.

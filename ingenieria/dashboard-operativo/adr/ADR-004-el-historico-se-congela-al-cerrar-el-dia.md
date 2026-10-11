# ADR-004 — El histórico se congela al cerrar el día; la semana es la suma de sus días

**Fecha:** 2026-10-10
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Jose pidió el 2026-10-10 que el dashboard tenga, además del hoy, un histórico semanal: «el hoy
da actualidad, el histórico da proyección». La pregunta es de dónde sale.

La forma obvia —recalcular cada semana desde `checklogs_raw` y `tasks_raw` al pedirla— tiene un
defecto que ya está escrito en `BuildPlannedHours` y en el
[ADR-005 de disponibilidad](../../disponibilidad/adr/ADR-005-snapshot-del-calendario-resuelto-en-postgres.md):
**`dim_calendars` guarda sólo la configuración actual, sin historia**. Cada sync la pisa. El
«previstos» de un lunes de hace tres semanas cambia hoy si alguien toca un horario. Recalcular
el pasado es reescribirlo.

Hay un segundo defecto, más silencioso: dos cálculos. El del hoy, sobre la ventana del día, y
el de la semana, sobre un rango. Tarde o temprano divergen en un detalle —una jornada que cruza
la medianoche, un `incomplete_workday` que el saneador marcó después— y el gerente ve un lunes
que a las 18:00 decía «8 de 10» y el martes, en la semana, dice «7 de 10».

## Decisión

**El día se cierra una vez y se guarda.** Un cron por zona horaria ejecuta, para cada centro y
para el día anterior, **la misma función** que sirve el hoy (`buildOperationalDay`) con
`asOf = fin del día`, y persiste el resultado en `operational_daily`: los totales de los tres
bloques y un detalle por persona y por tarea. **La semana es la suma de sus días.** Las tasas
se recalculan sobre las sumas; nunca se promedian tasas.

El día lleva `source`: `close` (el cron, con el calendario vigente ese día), `backfill` (la
reconstrucción de los días anteriores al arranque, con el calendario actual) o `manual` (un
rehacer tras corregir un fichaje). El front lo marca. Detalle en
[TDR-003](../tdr/TDR-003-cierre-diario-y-semanas.md).

## Alternativas descartadas

- **Recalcular al pedir.** Reescribe el pasado y duplica el cálculo. Descartada arriba.
- **Snapshot del calendario resuelto** (ADR-005 de disponibilidad, aplazado). Resolvería la
  historia del calendario, no la duplicidad de cálculo. Y lo que el dashboard necesita del
  pasado no es el calendario, es el resultado.
- **Reutilizar `employee_daily_reports`.** Es el registro de jornada legal por persona
  (`reports`, 02:xx local). No tiene previstos, ni tareas, ni coste, y su forma responde a otro
  requisito. Se copia su mecanismo de cron por zona; no su tabla.

## Consecuencias

- El pasado «de verdad» empieza el día que arranca el cron. Las ocho semanas anteriores se
  reconstruyen con el calendario actual, marcadas `backfill`, y así se enseñan. No se disimula.
- Corregir un fichaje de un día cerrado no cambia el histórico solo. Hay que rehacer el día
  (`POST /close-day`), y la fila sube de `version`. Es una decisión, no un accidente.
- `operational_daily` crece una fila por centro y día: 20 centros son 7.300 filas al año. Nada.
- El `detail` por persona y tarea hace que el «ver más» de una semana no relea el crudo, y
  que se pueda responder «quién acumula retrasos este mes» sin un cálculo nuevo. Es lo que da
  proyección de verdad: no la tasa, sino quién la mueve.

# ADR-005 — El retraso se calcula contra el reloj y la tolerancia configurada; «sin fichaje», nunca «ausente»

**Fecha:** 2026-10-10
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Dos de las cifras del dashboard son juicios sobre tiempo: una persona «con retraso» y una
tarea «vencida» o «sin empezar a su hora». Hay dos tentaciones, y las dos están en el código.

**La primera: leer un campo.** La tarea guarda `timeComplianceStatus`. El estudio comprobó que
sólo se escribe al iniciar (`on_time` u `overdue`) y al completar; **ningún planificador lo
revisa**. Una tarea asignada cuya fecha pasó hace dos días sigue en `not_started` hasta que
alguien la toque. Leerlo para el dashboard diría «todo en orden» en el peor momento.

**La segunda: inventar un umbral.** El diseño de Presencia dejó abierto «con cuántos minutos
se etiqueta retraso» y lo delegó en la app. En un dashboard de gerente hay que poner un número,
y el número ya existe: cada fichaje lleva `scheduleApplied.toleranceMinutes`, la tolerancia del
turno que el cliente configuró en su calendario y con la que el propio fichaje se evaluó.

Y una tercera, de tono, que el
[ADR-005 de panel-operativo-v2](../../panel-operativo-v2/adr/ADR-005-ausencia-de-evidencia-no-es-evidencia-negativa.md)
dejó escrita: la ausencia de evidencia no es evidencia negativa.

## Decisión

1. **Las tareas se evalúan contra `asOf`**, nunca contra el campo guardado:
   `start_late` si `scheduled_start_at < asOf` y `status = assigned`; `overdue` si
   `due_at < asOf` y `status ∈ {assigned, in_progress}`; `due_today` si `due_at` cae en el
   día del centro. El campo `time_compliance_status` se espeja por completitud y por el Panel
   mensual, pero el dashboard no lo lee para decidir.
2. **El retraso de una persona es un hecho más una regla del cliente:**
   `minutesFromShiftStart` contra `firstCheckinAt` si fichó y contra `asOf` si no, y
   `late = minutesFromShiftStart > toleranceMinutes`, con la tolerancia del turno aplicado del
   fichaje o, para quien no fichó, la de la cascada del calendario. Los dos números viajan
   juntos en la respuesta para que el front pueda explicar el booleano.
3. **Vocabulario.** `no_log` se enseña como «sin fichaje», nunca «ausente» ni «falta».
   `incomplete` es «jornada sin cerrar», sin adjetivo, y no entra en retraso ni en sin fichaje.
   `rejectedAttempts` son «intentos rechazados», no fraudes. Quien fichó sin estar previsto
   aparece en su lista, sin juicio.
4. **La alerta de centro vacío tiene hora.** `no_presence` sólo cuando ya pasó el inicio del
   primer turno más su tolerancia. Un centro que abre a las 8:00 no está vacío a las 7:00.

## Consecuencias

- Si el cliente no configuró tolerancia, el turno aplicado trae la del nivel superior o la
  por defecto del sistema; no hay caso «sin umbral». Si no hay turno, no hay retraso: `late`
  es `false` y `minutesFromShiftStart` no viaja.
- Una tarea que se completa deja de ser `overdue` en el siguiente sondeo, aunque el campo
  guardado diga lo que diga.
- Lo mismo que hoy se calcula contra `asOf = ahora`, el cierre lo calcula contra
  `asOf = fin del día`: «vencidas al cierre» y «sin empezar al cierre» son las cifras que se
  congelan ([ADR-004](./ADR-004-el-historico-se-congela-al-cerrar-el-dia.md)).
- Si algún día un planificador mantiene `timeComplianceStatus`, el dashboard no cambia: ya
  no dependía de él.

## Nota de implementación (2026-10-11) — decisión a revisar

Al implementar se vio que `scheduleApplied.toleranceMinutes` **no** es un margen de retraso
configurado: `createChecklog.controller` lo rellena con `advance.notifyBeforeMinutes ?? 15`, que
es la ventana para fichar **antes** del turno. Presencia ya lo advertía.

Se mantiene como margen porque el Panel mensual (`BuildBranchBehaviour`, puntualidad) ya lo usa
así, y dos pantallas con dos definiciones de «tarde» serían peor. Para quien no ha fichado se
resuelve igual: `notifyBeforeMinutes` de empleado → sucursal → entidad, o 15.

Si negocio quiere un margen de retraso propio, la solución es un campo nuevo en `advance` y
cambiar a la vez el dashboard y la puntualidad del Panel. Es una decisión de Jose.


# ADR-002 — Se envía el cierre aprobado del periodo, no cada fichaje

**Fecha:** 2026-10-26
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

Rentman recibe cada jornada en cuanto se cierra, por sondeo cada 15 minutos. Para una hoja de
proyecto eso es lo correcto. Para una nómina no: la nómina se calcula una vez por periodo, y
lo que entra en ella tiene efectos económicos y legales para una persona. Además, hoy
CheckBiz no tiene cierre de mes ni bloqueo de periodo: una jornada se puede corregir
semanas después.

## Decisión

1. **Lo que se envía es un cierre de periodo** por empresa: normalmente el mes, o el periodo
   de nómina que tenga el cliente.
2. **Antes de enviar hay una vista previa**: por persona, cada concepto con su cantidad y de
   dónde sale (ADR-005).
3. **Lo aprueba una persona** con permiso de administración en esa empresa. Sin aprobación no
   se envía nada. No hay envío automático, ni siquiera opcional, en v1.
4. **Lo que impide cerrar a una persona se dice, no se rellena:**
   - jornadas pendientes de validar;
   - jornadas sin salida;
   - personas sin asociar con A3;
   - conceptos sin correspondencia;
   - ausencias con «retribuida: no consta».

   Esa persona queda fuera del envío con el motivo a la vista. Las demás salen.
5. **El cierre es una foto.** Lo enviado se guarda tal cual se envió, con su huella, en las
   tablas del add-on. **No bloquea el núcleo**: una jornada se puede seguir corrigiendo en
   CheckBiz, y el siguiente cierre lo detecta como diferencia (TDR-002 §6).

## Justificación

**Es como trabaja quien hace nóminas.** Primero se revisa el mes y luego se calcula. Un goteo
de incidencias diarias obligaría a revisarlas en A3, que es justo lo que queremos evitar.

**Una persona firma lo que se paga.** Las horas extra y los permisos retribuidos son dinero.
Que pasen por los ojos de alguien antes de llegar a la nómina es la diferencia entre una
herramienta y un riesgo, igual que en el conector del asistente: nada se escribe sin que la
persona lo haya visto.

**Lo pendiente se dice, no se rellena.** Una jornada sin validar o una ausencia «no consta»
no se convierten en un valor por omisión. Es la regla de disponibilidad ADR-004: lo que no se
ha preguntado no se contesta por su cuenta.

**No bloquear el núcleo es la regla de oro.** Un bloqueo de periodo sería un cambio en el
producto para acomodar a un tercero. La foto vive en el add-on; el núcleo no se entera.

## Alternativas descartadas

- **Envío continuo, como Rentman:** obliga a revisar en A3 y no da un momento de firma.
- **Bloquear el periodo en CheckBiz al cerrar:** cambia el núcleo y rompe la corrección de
  jornadas, que es legal y necesaria.
- **Excluir en silencio a quien tiene algo pendiente:** un cierre al que le falta gente sin
  decirlo es peor que no cerrar.

## Consecuencias

- Hace falta un estado del cierre (borrador → aprobado → enviado / con errores) y su pantalla
  (TDR-002).
- Las correcciones posteriores no se pierden: aparecen como diferencia en el cierre
  siguiente. Cómo las recibe A3 está *a confirmar con la cuenta* (periodos ya calculados).

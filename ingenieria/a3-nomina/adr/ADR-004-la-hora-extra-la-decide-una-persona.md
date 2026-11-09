# ADR-004 — El exceso lo mide CheckBiz; que sea hora extra lo decide una persona

**Fecha:** 2026-10-26
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

Hoy CheckBiz no calcula horas extra por persona. La única cifra es una aproximación por
sucursal (`extraHours()` en `services/analytics/src/application/FetchCheckbizStats.ts`), que
estima lo previsto como la duración del horario de la sucursal por el número de personas.
Tampoco hay datos de contrato: ni jornada semanal ni tipo de contrato.

Legalmente, una hora extra es la que supera la jornada ordinaria. Esa jornada la fija el
convenio o el contrato, a menudo en cómputo anual, y una hora extra se puede pagar o
compensar con descanso. Lo que CheckBiz sí sabe es cuánto trabajó cada persona y qué horario
tenía previsto.

## Decisión

1. **CheckBiz mide el exceso**: el tiempo trabajado por encima del horario previsto de esa
   persona ese día. Es un hecho medible, y se llama así en pantalla: *exceso sobre su
   horario*, no *horas extra*.
2. **En la vista previa del cierre, quien aprueba decide** qué parte del exceso es hora
   extra a pagar. La propuesta inicial es todo el exceso. Lo que no confirme no se envía
   como hora extra.
3. **Lo previsto sale del modo de horario de cada persona:**
   - *Semana tipo*: su semana tipo.
   - *Por turnos*: sus turnos cargados.
   - *Por tareas*: sus tareas.

   Una persona sin horario previsto ese día no genera exceso medible, y se dice así.
4. **Horas nocturnas y en festivo** se miden directamente:
   - nocturnas: el tramo trabajado entre las 22:00 y las 06:00, en la hora local del
     centro;
   - en festivo: las horas trabajadas en un festivo de su calendario.

   Son hechos que no necesitan decisión. Se envían si el concepto está asociado.

## Justificación

**Nombrar lo observado, no la causa.** El exceso es un hecho. Que sea hora extra depende
del convenio, del cómputo anual y de lo pactado. Llamarlo *hora extra* sin saberlo sería
afirmar algo que el sistema no puede saber.

**Sin contrato no hay jornada ordinaria.** Hasta que leamos los contratos de A3 (fase 3), lo
único que tenemos es el horario previsto. Cuando haya contratos, el exceso podrá medirse
también contra la jornada contratada, pero la decisión de pagar seguirá siendo de una
persona.

## Consecuencias

- Hace falta calcular el exceso por persona y día (TDR-002 §3). Hoy no existe.
- La vista previa necesita poder ajustar las horas extra por persona, guardando quién lo
  ajustó y por qué (ADR-005).
- La aproximación por sucursal de las estadísticas no se reutiliza: mide otra cosa.

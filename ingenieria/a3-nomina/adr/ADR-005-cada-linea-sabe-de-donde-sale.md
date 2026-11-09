# ADR-005 — Cada línea enviada a la nómina sabe de dónde sale

**Fecha:** 2026-10-26
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

Lo que mandamos a A3 acaba en una nómina. Si un trabajador reclama, o una inspección
pregunta por qué se pagaron 14 horas nocturnas o 12 dietas, la respuesta tiene que estar en
el sistema, no en la memoria de quien cerró el mes. En sectores como el transporte, los
conceptos exentos sin justificar son un hallazgo de inspección clásico.

## Decisión

1. **Cada línea del cierre guarda su origen:** las jornadas (`checkin_id`) o las ausencias
   (`absence_request` / calendario) de las que sale, y la regla que la calculó.
2. **Cada ajuste manual guarda quién, cuándo y por qué:** una hora extra no confirmada, una
   persona excluida. El motivo es obligatorio.
3. **Lo enviado se guarda tal cual se envió** (cantidades, códigos A3 y respuesta de A3) y
   no se reescribe. Una corrección es un envío nuevo que apunta al anterior.
4. **El cierre se puede descargar** con ese detalle por persona: lo que se envió y de qué
   jornadas sale.

## Justificación

**Es el argumento de venta, no solo una defensa.** «Cada concepto de tu nómina lleva su
fichaje detrás» es justo lo que no puede decir quien teclea las horas a mano.

**Es la misma autoridad que en Rentman.** CheckBiz responde del registro de jornada. Si lo
que sale hacia la nómina no se puede rastrear hasta ese registro, esa autoridad no vale
nada.

## Consecuencias

- Tabla de líneas con referencias de origen y tabla de ajustes con autor y motivo (TDR-002 §5).
- Más volumen que un simple total por persona. Es asumible: hay una línea por persona,
  concepto y periodo, y el origen va en JSONB.

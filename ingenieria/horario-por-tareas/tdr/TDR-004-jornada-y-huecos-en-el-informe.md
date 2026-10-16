# TDR-004 — Fase 4: la jornada y los huecos en el informe

**Fecha:** 2026-10-16
**Estado:** Implementado el 2026-10-16 en `develop` (e2cb877); sin subir a `staging`. Comprobado con un PDF y un Excel de muestra generados con el lunes del cuadrante.
**Componente:** `encodebiz-api` — `services/reports` (`GenerateReportPDF.ts`, `GenerateReportXLSX.ts`, `domain/daySummary.ts`)
**Decisiones de referencia:** [README](../README.md) D8

---

## 1. Qué entrega

El informe de jornada sigue con una fila por ciclo (entrada–salida), y para cada día con **más
de un ciclo** añade lo que hoy no se ve:

- **Jornada:** de la primera entrada real a la última salida real del día.
- **Trabajado:** la suma de los ciclos, con sus descansos ya quitados (lo de siempre).
- **Huecos entre turnos:** lo que pasa entre la salida de un ciclo y la entrada del siguiente.

Medido de los fichajes, no de las tareas: si el primer servicio acabó a las 10:03 y el segundo
empezó a las 10:06, el hueco son 3 minutos. Los descansos van dentro de un ciclo y no son
huecos. No se reutilizan «bruto» ni «neto», que ya significan otra cosa. Vale para cualquier
jornada partida, no solo para el horario por tareas. El informe no decide qué se paga: enseña
lo medido.

## 2. Nombre

«Huecos entre turnos», el de D8. La pregunta abierta del README pedía el nombre en tres
idiomas, pero el informe de jornada solo existe en español; no hay más que nombrar hasta que
se traduzca.

## 3. Dónde se calcula

En el informe, sobre los ciclos que ya guarda `employee_daily_reports`: una función pura,
`summarizeDays(cycles, tz)`, agrupa los ciclos de una persona por **fecha local de la entrada**,
los ordena y devuelve por día `{date, firstIn, lastOut, workedMinutes, gapMinutes, cycles}`. Un
solapamiento entre ciclos (no debería pasar) cuenta como hueco 0, nunca negativo. No cambia el
fichaje, ni la tabla, ni el cron que la llena.

## 4. Cómo se ve

**PDF.** Las filas por ciclo siguen igual. Debajo de los ciclos de un día con más de uno, una
línea: «Jornada 08:00–14:40 (6 h 40) · Trabajado 6 h 30 · Huecos entre turnos 0 h 10». Al pie
de cada persona, junto al total de horas trabajadas, el total de huecos del periodo si no es
cero.

**Excel.** Una fila por ciclo, como hasta ahora, para que se pueda filtrar y sumar. Dos
columnas nuevas al final, **Jornada** («08:00–14:40») y **Huecos entre turnos (min)**, que se
rellenan solo en la última fila de cada día con más de un ciclo; así la columna de huecos se
suma sin contar nada dos veces. En la hoja de resumen, una columna más con los huecos del
periodo.

## 5. Pruebas

Unitarias de `summarizeDays` con `node:test` (`npm test -w services/reports`): el lunes del
cuadrante de ServiSAD (tres ciclos, 10 minutos de huecos), un día de un solo ciclo, la
medianoche local, y ciclos desordenados o solapados.

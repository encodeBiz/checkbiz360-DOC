# ADR-007 — Alertas que se leen: doble umbral, pocas y con destino

**Fecha:** 2026-10-12
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

El objetivo principal del dashboard, en palabras de Jose (2026-10-12): alertas concisas cuando
haya problemas en alguno de los ámbitos que enseña —disponibilidad, fichajes, costes…— que
lleven a mirar los datos, **sin ser atosigador**: que falten 2 de 20 por fichar no es un problema.

Un aviso que salta por todo enseña a ignorar la lista entera (CLAUDE.md, «nombrar lo observado»).

## Decisión

1. **Doble umbral en cada regla:** uno relativo (un porcentaje) y uno absoluto (un mínimo de
   personas, tareas o días afectados). Solo salta si se cumplen los dos. 2 de 20 sin fichar es un
   10 %: no salta. 3 de 4 sí.
2. **Pocas:** como mucho ocho, ordenadas por gravedad (`high` antes que `medium`) y, dentro, por
   tamaño del problema. Una por regla y ámbito: si un centro tiene tres días flojos, es una
   alerta que lo dice, no tres.
3. **Con destino:** cada alerta lleva la pantalla donde se mira (`target`), y el front la enlaza.
4. **El hecho, no la causa:** «Obra Norte: el jueves hay 3 de 10 disponibles (30 %)». Nunca
   «faltan trabajadores» ni juicios. Las jornadas «sin cerrar» se nombran así.
5. **Calculadas al pedirlas, sin guardar.** Son una lectura del momento sobre los mismos datos que
   pinta la portada; si el problema se arregla, la alerta desaparece en la siguiente lectura.
6. **Umbrales en un solo sitio**, con nombre, para ajustarlos sin buscar por el código.

## Consecuencias

- Una empresa pequeña puede no ver nunca ciertas alertas: el mínimo absoluto lo impide. Es lo
  buscado.
- Sin envío por push o correo en esta fase. Son de pantalla; el aviso activo es Presencia fase 3.

# ADR-007 — El cuadrante se llena por tandas

**Fecha:** 2026-10-16
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («no puede importar más de 300 tareas, eso es un caos: debes dejar importar de forma masiva también»)

---

## Contexto

En la primera prueba con Claude, el asistente se negó a cargar una semana grande: leyó en la
herramienta `trabajos: max 300` y lo entendió como un tope total. El tope de verdad era otro, y
peor: **todo el lote tenía que caber en una sola llamada** (60 personas como mucho, 300
trabajos por persona). Una sucursal de ayuda a domicilio con 80 auxiliares y 1.500 servicios
a la semana no cabe, y aunque cupiera, una llamada con miles de filas es la que un modelo
corta o resume sin avisar.

El Excel del panel no tiene el problema porque el fichero llega entero. El asistente
necesita lo mismo, pero en trozos.

## Decisión

1. **Un lote se puede ampliar.** `proponer_cuadrante` acepta el `loteId` de una tanda
   anterior. Sin él, crea un lote nuevo; con él, añade al mismo lote.
2. **Las tandas se reparten por personas, no por filas.** Cada persona va entera en una
   tanda (su semana completa, como siempre). Si una persona vuelve en otra tanda, **su
   semana nueva sustituye a la anterior** dentro del lote. Eso es también la forma de
   corregir a una persona sin reenviar a todas.
3. **La semana la fija la primera tanda.** Las siguientes tienen que caer en la misma; una
   fecha de otra semana bloquea a esa persona con el mismo mensaje que el Excel.
4. **Tope por llamada, no por lote**: 60 personas y 300 trabajos por persona en cada
   llamada. El lote no tiene tope de personas. Pasarse en una llamada es un error explícito,
   nunca un recorte silencioso (antes, la persona 61 se perdía sin decir nada).
5. **Sólo se amplía un lote propuesto.** Uno confirmado, aplicándose o descartado responde
   `lote_cerrado`. La fusión va en una transacción: dos tandas a la vez no se pisan.
6. **La respuesta de una tanda enseña sólo a las personas de esa tanda**, más los totales
   del lote entero. `ver_cuadrante` sigue enseñando todo. El Excel rellena a todo el lote.
7. **Varias semanas = varios lotes**, uno por semana (ADR-004 no cambia): un mes son cuatro
   cuadrantes, cada uno con su confirmación.

## Alternativas descartadas

- **Subir los topes.** Sólo mueve el muro: una llamada con 2.000 filas sigue siendo la que
  el modelo trunca, y la respuesta con 200 personas no le cabe al cliente en la pantalla.
- **Tandas por filas, juntando las de una persona entre llamadas.** Exige guardar filas
  crudas en el lote y deja a medias a quien tuvo un error en una tanda: sus filas buenas de
  la tanda anterior se perderían o se duplicarían según el orden. Por personas, cada tanda
  es completa en sí misma.
- **Un lote por tanda y confirmar varios.** El cliente revisaría y confirmaría N cosas para
  una sola semana, y el Excel saldría partido.

## Consecuencias

- `merlin`: `POST /lotes/filas` acepta `loteId`; `leerFilas` admite la semana fijada; el
  lote se funde por `employeeId` y las propuestas sustituidas se descartan.
- Los códigos de error de lote dejan de ser todos 404: `lote_cerrado` es 409 y
  `demasiadas_personas`, 400.
- Las instrucciones del conector dicen cómo partir: tandas de unas 20–30 personas, la misma
  `loteId`, y confirmar una sola vez al final.

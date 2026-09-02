# ADR-004 — La ausencia registra si es retribuida, y "no consta" no es "no"

**Fecha:** 2026-09-02
**Estado:** Propuesto — con un punto pendiente de confirmar (§Pendiente)
**Decisionario:** Jose Acevedo

---

## Contexto

Una ausencia guarda hoy nombre, fecha y descripción. No guarda lo único que distingue unas de
otras a efectos de nómina: **si se cobra o no**. Unas vacaciones y un permiso sin sueldo se ven
exactamente igual en el sistema, y la diferencia queda en el nombre que escribiera quien la dio
de alta —o en la memoria de alguien—.

El campo hace falta desde el momento en que las ausencias se dan de alta desde el tablero
([ADR-003](./ADR-003-el-desglose-del-dia-escribe-ausencias.md)): quien marca que alguien no
viene mañana sabe en ese momento si se le paga, y es el único momento en que lo sabe sin
preguntar.

---

## Decisión

`Holiday` gana `paid?: boolean`.

**Opcional de verdad:** sin valor significa **"no consta"**, que se pinta y se trata distinto de
`false`. La casilla se enseña **sólo en scope empleado**.

---

## Justificación

**En entidad y sucursal la casilla sobra.** Un festivo de la entidad o de la sucursal es
retribuido por definición: nadie pierde sueldo por el 25 de diciembre ni por la fiesta local.
Una casilla que siempre está marcada no informa, estorba, y acaba desmarcada por accidente
alguna vez. Donde el dato distingue algo es en la ausencia del empleado: vacaciones
(retribuidas), permiso sin sueldo (no), baja médica (la paga la Seguridad Social, que no es ni
lo uno ni lo otro y por eso conviene poder dejarlo sin marcar).

**El valor por defecto es la trampa.** Si el campo naciera en `false`, todas las ausencias que ya
existen pasarían a leerse como *no retribuidas* sin que nadie lo haya decidido; si naciera en
`true`, al revés, y alguien cobraría un permiso que no le tocaba. Ninguna de las dos es una
lectura legítima de un dato que nunca se preguntó. Por eso la ausencia de valor tiene que
significar exactamente eso, y verse.

**"No consta" es para el histórico, no para lo nuevo.** En un alta hecha desde el modal la
casilla está a la vista y se guarda lo que quede marcado, `true` o `false`: se ha preguntado y
hay respuesta. El estado sin valor es el de los registros que se crearon antes de que el campo
existiera, y sólo reaparece al editar uno de ellos.

**Es el mismo error que ya nos costó una arquitectura.** En el prototipo del tablero, una lectura
fallida se interpretaba como "sin ausencias", o sea como *disponible*: un valor por omisión
convertido en afirmación. La regla que sale de ahí, y que aquí se aplica antes de que muerda, es
que **lo que no se ha preguntado no se contesta por su cuenta**.

**Es cambio de contrato, no adorno del modal.** `Holiday` vive en `domain/entities/Calendar.ts`
y en `ICalendar.ts`; `upsertCalendar` tiene que persistirlo, `ResolveEffectiveCalendarUseCase`
devolverlo en `holidays[]` y `action=availabilityDay` traerlo para que el panel lo enseñe. Poco
código, pero en cuatro sitios y en los dos repos.

---

## Consecuencias

**Positivas:**

- La diferencia entre vacaciones y permiso sin sueldo deja de vivir en el nombre que alguien
  escribió a mano.
- Se registra en el momento en que se sabe, no en una revisión posterior.
- El histórico no se reescribe: lo que se dio de alta sin la pregunta se queda como "no consta",
  que es la verdad.

**Negativas / Compromisos aceptados:**

- Un estado más que pintar. "No consta" necesita su propia representación —ni marcado ni
  desmarcado— en el modal, en las tablas de ausencias y en el desglose del día.
- Convivencia larga: los registros antiguos se quedan sin valor indefinidamente, salvo que
  alguien decida una migración, que este ADR **no** propone.
- Si mañana el campo alimenta nómina o el informe de horas, deja de ser informativo y arrastra
  decisiones que hoy no se toman (§Pendiente).

---

## Pendiente de confirmar

**¿Es informativo o tiene efectos?** Se propone que **hoy sea sólo informativo**: se guarda, se
enseña y no computa en ningún cálculo. Si va a alimentar el informe de horas o la nómina, hay
que decidirlo ahora y no después, porque entonces hacen falta tres cosas más que un campo
booleano no trae: quién puede cambiarlo, bitácora de cambios, y qué pasa cuando alguien lo
cambia sobre un mes ya cerrado.

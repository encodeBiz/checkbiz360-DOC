# ADR-004 — El asistente es un lector más del lote de cuadrantes

**Fecha:** 2026-10-16
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («igual el agente debe de crear ese Excel, validarlo con el cliente y enviarlo a esta función»; «eso es lo potente»)

---

## Contexto

Configurar la semana es lo que más tiempo quita a un cliente, y es la razón del conector. La
plataforma ya tiene, en validación, el circuito entero de una semana: la **importación por
plantilla de sucursal** ([cuadrantes TDR-001](../../cuadrantes/tdr/TDR-001-importacion-por-plantilla-de-sucursal.md))
lee una pestaña por persona, reconoce a cada una, revisa contra festivos, ausencias y solapes,
deja un **lote** con una propuesta por persona que no escribe nada, y al confirmar aplica en
segundo plano y sin duplicar. Y el **horario por tareas** ([horario-por-tareas](../../horario-por-tareas/README.md))
hace que, en ese modo, configurar la semana sea sólo crear tareas: el horario se genera.

El propio TDR de la plantilla deja la puerta abierta (§9): «un segundo lector sobre el mismo
lote».

## Decisión

1. **El asistente no escribe semanas por su cuenta: propone un lote**, el mismo que produce
   subir la plantilla. A partir de las filas, todo es el código de la plantilla: revisión,
   propuesta por persona, firma, aplicación idempotente.
2. **Cuatro entradas al mismo lote**, y el lote no sabe de cuál viene:
   - el Excel de siempre, subido desde el panel;
   - **copiar una semana**: el asistente lee la anterior, cambia fechas y aplica los cambios;
   - **desde cero**: el asistente pregunta lo que falte y arma las filas;
   - **desde un documento** que el cliente sube a su propia IA (el PDF de su programa, una foto,
     un Excel a medias): la IA lo reorganiza en las filas de la plantilla.
3. **El modelo manda filas estructuradas, no un fichero.** Un modelo no envía bien un binario
   por una herramienta; las filas sí, y el servidor las valida una a una con los mismos
   lectores de fecha, hora y viaje que la plantilla.
4. **El Excel lo fabrica el servidor**: cada lote propuesto por el asistente trae un enlace a
   la plantilla **ya rellena** con lo propuesto, para que el cliente la revise en su
   herramienta de siempre o la corrija y la suba por el panel.
5. **El cruce de personas es por identificador, obligatorio.** El asistente busca a la gente
   de la sucursal y manda el `employeeId` de cada una; el servidor rechaza los que no son de
   esa sucursal. Al cliente sólo se le pregunta cuando no hay cruce o hay dos candidatas,
   enseñándole el correo para que reconozca a la persona.
6. **Red de totales**: si el documento trae horas impresas por persona, el asistente las
   manda y el servidor comprueba que la suma de las filas cuadra. Si no, esa persona queda
   bloqueada. Es la red que mejor funcionó con el cuadrante de ServiSAD.
7. **Validar es proponer**: crear el lote no escribe nada, así que el asistente propone,
   enseña los hallazgos, corrige con el cliente y vuelve a proponer cuantas veces haga falta.
   Sólo `confirmar` escribe.

## Alternativas descartadas

- **Herramientas que escriben horario y tareas directamente.** Una segunda forma de escribir
  la semana que diverge de la primera, sin la revisión de festivos y ausencias y sin un
  momento de «esto es lo que va a quedar».
- **Que el modelo genere el Excel y lo suba.** Un binario en base64 dentro de una llamada se
  corta o se corrompe sin que nadie lo note con trescientas filas.
- **Pedir el correo de cada persona al cliente.** Carga con algo que el sistema ya sabe, y un
  correo mal escrito cruza peor que el identificador.

## Consecuencias

- `merlin` gana una entrada nueva al lote, de filas en vez de bytes, y un generador de la
  plantilla rellena. El lector de la plantilla se parte en dos: leer el Excel a filas, y de
  filas en adelante, que es lo común ([TDR-002](../tdr/TDR-002-herramientas-de-la-semana.md) §3).
- El documento que el cliente sube a Claude o ChatGPT, con nombres y domicilios, va a **su**
  cuenta: es decisión suya y la pantalla de autorización ya lo avisa (ADR-001). Nosotros no
  tachamos nada porque no pasa por nosotros; lo que nos llega son las filas.
- Las cosas que el lote no hace tampoco las hace el asistente: dos semanas en una propuesta no
  caben, y una semana ya empezada se reescribe igual que con el Excel.

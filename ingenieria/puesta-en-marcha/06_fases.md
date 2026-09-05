# 06 — Fases de implementación

## Fase 0 — Diseño y documentación ✔

El reparto entre capas, el contrato del turno, el relato de la conversación y las cuatro
decisiones. Todo verificado contra el código y contra un fichero real de cliente.

**Entregable:** `ingenieria/puesta-en-marcha/`.

---

## Fase 1 — Del fichero al cliente montado, sin conversación

El normalizador y el seed. **Sin IA, sin rutas y sin interfaz**: un script que lee el fichero
que mande el cliente, construye el borrador con sus preguntas abiertas, y otro que lo siembra.

Tres piezas:

1. **El normalizador.** De un libro de Excel o unos CSV al borrador JSON. Cruza las hojas
   —las sedes de cada persona salen del bloque de gente, no del de responsabilidades—,
   detecta los valores que coinciden con la fila de ejemplo, y lo que no puede saber lo deja
   a `null` con su pregunta.
2. **El seed.** Simula por defecto, escribe con `--apply`, e incluye lo que no está en el
   borrador y sin lo cual el cliente no funciona: geocodificar enseñando la precisión, crear
   el patrón inicial de cada sucursal, y expandir responsabilidades y periodos de festivo
   ([ADR-002](./adr/ADR-002-la-puesta-en-marcha-siembra-patron-y-coste.md),
   [ADR-004](./adr/ADR-004-el-borrador-guarda-intencion.md)).
3. **El deshacer**, a la vez que el seed y no después. Borrado real: la ficha se queda en
   `fired`, la entrada del `searchIndex` no se va sola, el usuario de Auth sobrevive y los
   patrones no se restan.

**Va primero, y no la conversación, por dos razones.** La primera es que **valida la forma del
muñeco usándolo**: si el borrador tiene la estructura equivocada, se descubre montando un
cliente de verdad, no discutiéndolo. La segunda es que ya entrega valor sola — con esto, el
equipo monta un cliente desde su fichero en una tarde, que es la mayor parte del problema que
esto venía a resolver.

**Verificación:** [Tapissat](./02_caso-real-tapissat.md) montado en dev desde su propio
fichero. Concretamente: cuatro centros con coordenadas y su precisión a la vista, cuatro
personas, **16 responsabilidades** —y que las cuatro puedan fichar en los cuatro centros, que
es lo que falla si el ámbito se hace mal—, el horario 07:00–15:00 heredándose, 66 festivos, y
el patrón de cada sucursal existiendo. Y `--limpiar` devolviéndolo todo a cero.

---

## Fase 2 — El motor de turnos de la capa de soporte

La conversación, con **un solo bloque** para probarla: la empresa, que es el más simple.

La sesión y el borrador en backoffice; la ruta
`POST /api/v1/gpt/soporte/puesta-en-marcha/turno` en Merlin, síncrona, devolviendo **ediciones
por ruta** y no el borrador entero ([05_contratos-api](./05_contratos-api.md)).

Aquí se descubre si el contrato del turno aguanta: si el modelo sabe emitir
`empleados[<correo>].coste_hora = 18.5` de forma fiable, o si hay que estrechar el esquema.
Averiguarlo con un bloque cuesta una tarde; averiguarlo con seis, una semana.

**Verificación:** una conversación completa de un bloque, con interrupción y retomada en otra
sesión, y el borrador en disco coincidiendo con lo que se dijo.

---

## Fase 3 — Los seis bloques, sus plantillas y sus puertas

El relato completo ([04_el-relato](./04_el-relato.md)): las explicaciones que van antes de
cada CSV, la pregunta de los tres niveles de horario, y **la puerta de cada bloque**, que
relee el borrador entero y no sólo lo que acaba de llegar.

Y el documento de revisión: la configuración en el idioma del cliente, que es lo que aprueba
antes de sembrar.

**Verificación:** montar Tapissat otra vez, pero conversando, y que salga el mismo borrador
que salió en la Fase 1 desde su fichero. Si no coincide, uno de los dos caminos está mal.

---

## Fase 4 — La otra pata

Merlin en modo soporte, resolviendo dudas. Reutiliza el motor de turnos de la Fase 2 y lee la
configuración que dejó la puesta en marcha. Se documenta aparte.

---

## Fuera de estas fases, pero antes del primer cliente

**La decisión del [ADR-003](./adr/ADR-003-arranque-en-frio-y-fiabilidad.md).** Un cliente
recién montado verá a casi toda su plantilla marcada como «en riesgo» durante su primer mes,
porque `reliability` mezcla *cuánto dato hay* con *cómo de bueno es*. No lo arregla nada de lo
anterior: vive en `ProfileClassifier`, en `encodebiz-api`. Pero es lo primero que verá alguien
a quien acabamos de montar la casa, así que conviene resolverlo antes de estrenarla.

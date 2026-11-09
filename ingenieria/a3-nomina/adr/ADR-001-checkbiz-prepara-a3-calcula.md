# ADR-001 — CheckBiz prepara, A3 calcula

**Fecha:** 2026-10-26
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

Al conectar CheckBiz con a3innuva es tentador decir que «CheckBiz hace nóminas»: tenemos las
horas, las ausencias y, con la cuenta de A3, podríamos leer los contratos. Pero una nómina no
es solo un cálculo. Lleva el convenio aplicable, el IRPF, las bases y tipos de cotización,
las bonificaciones, los atrasos, y los envíos a la TGSS y al SEPE. A3 mantiene todo eso, y
la responsabilidad legal de la nómina es del cliente o de su gestoría.

## Decisión

**CheckBiz manda a A3 hechos medidos y aprobados; A3 calcula y emite la nómina.**

- No se construye un motor de nómina ni se calcula ningún importe que A3 ya sepa calcular.
- No se decide desde CheckBiz cómo tributa o cotiza un concepto: eso lo dice la
  configuración del concepto en la cuenta de A3 del cliente (ADR-003).
- Si la API deja lanzar el cálculo, se podrá ofrecer como comodidad («calcular ahora»). La
  nómina seguirá siendo de A3 y la responsabilidad, del cliente.

## Justificación

**Es el producto de otro, y muy regulado.** Un motor propio exigiría mantener todos los
convenios y cada cambio normativo, que es justo lo que A3 hace y cobra. Nuestro valor es que
los datos que entran en esa nómina sean reales y lleguen solos, no sustituir a A3.

**Nos deja en el sitio que sabemos defender.** CheckBiz responde del registro de jornada; esa
es su autoridad, la misma que ya se fijó con Rentman. Mandar a A3 lo que el registro dice es
coherente con esa autoridad. Calcular sueldos no lo es.

**Se vende mejor y con menos riesgo.** La frase es: «tu nómina en A3 sale de los fichajes
reales: cierras el mes y está lista para calcular, sin teclear nada». No nos coloca en un
terreno legal que no es el nuestro.

## Alternativas descartadas

- **Motor de nómina propio:** es otro producto entero y de los más regulados que hay.
- **Mandar importes ya calculados por CheckBiz:** se descarta por las razones de ADR-003.
  Tendríamos tarifas duplicadas, y la tributación la decidiríamos nosotros.

## Consecuencias

- El add-on solo escribe variables de periodo y ausencias. Nunca toca salarios, contratos ni
  datos fiscales en A3.
- La calidad del producto depende de lo bien que midamos (TDR-002) y de lo bien que el
  cliente asocie sus conceptos (TDR-003), no de saber hacer nóminas.

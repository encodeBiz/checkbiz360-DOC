# ADR-003 — Se mandan unidades, no euros, y cada empresa asocia sus conceptos

**Fecha:** 2026-10-26
**Estado:** Propuesto — la forma exacta depende de la API (*a confirmar con la cuenta*)
**Decisionario:** Jose Acevedo

---

## Contexto

En A3, cada concepto de nómina tiene su código, su precio (por convenio, por contrato o por
persona) y su tratamiento: si cotiza, si tributa, si está exento y hasta qué límite. Cada
empresa tiene **sus** códigos: las horas extra de un convenio de limpieza no son el mismo
concepto que las de uno de transporte.

En casos como el VTC aparecen además conceptos no sujetos (dietas, kilometraje) que son
justo lo que más mira la Inspección. Allí es donde se esconde salario para no cotizar.

## Decisión

1. **CheckBiz manda cantidades:**
   - horas ordinarias, nocturnas, en festivo y extra confirmadas;
   - días de vacaciones o de permiso;
   - en el futuro, número de dietas o kilómetros.

   El precio y la tributación los pone A3.
2. **Importes en euros solo cuando CheckBiz conoce el euro y A3 no:** por ejemplo, un gasto
   con su ticket. Nunca para algo que tiene precio en A3.
3. **Cada empresa asocia sus conceptos.** Una pantalla de correspondencias dice «nuestro
   concepto *horas nocturnas* es tu concepto A3 *0123*». **Sin correspondencia, ese concepto
   no se envía**, y el cierre lo dice (ADR-002). No hay códigos por defecto.
4. **CheckBiz no decide qué es exento.** Lo deciden el cliente y su asesor al configurar el
   concepto en A3.

## Justificación

**Una sola tarifa, en un solo sitio.** Si mandáramos euros, tendríamos que mantener los
precios de cada convenio y persona en paralelo a A3, y equivocarnos en cuanto cambie uno.

**La tributación no es nuestra.** Decidir que algo es exento es asesoramiento laboral y
fiscal. Si lo hiciera el sistema, sería el sistema quien responde ante una inspección.

**Sin códigos por defecto, porque un código equivocado paga mal.** Un concepto mal asociado
no da error: genera una nómina incorrecta que nadie mira hasta que alguien protesta. Es
mejor que el cierre diga «falta asociar *horas nocturnas*».

## Consecuencias

- La primera puesta en marcha de cada cliente incluye asociar sus conceptos. Es el corazón
  del piloto, no un trámite.
- Si la API solo admitiera importes en algún concepto, se tratará como excepción en el TDR,
  con el precio leído de A3 y no tecleado en CheckBiz.
- Las dietas y el kilometraje (fase 3) entran bajo esta misma regla y la de ADR-005: cada
  unidad respaldada por un dato real.

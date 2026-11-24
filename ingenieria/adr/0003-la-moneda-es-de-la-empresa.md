# ADR-0003 — La moneda es de la empresa

**Estado:** aceptada · 2026-11-24 (decidida con Jose Acevedo)
**Cierra:** la decisión abierta nº 1 de [dashboard-operativo/README](../dashboard-operativo/README.md#decisiones-abiertas)
**Código:** `encodebiz-api` y `encodebiz-front-saas`, rama `feat/moneda-de-la-empresa`

---

## Contexto

CheckBiz360 es un producto internacional, y el dinero que enseña es casi siempre **del
cliente**: lo que le cuesta su plantilla, lo que firmó con sus propios clientes en la cartera,
los gastos externos de un montaje, el material que consume una tarea, las estadísticas de
coste de un centro. Nada de eso tiene por qué estar en euros.

Hasta hoy, sí lo estaba, y por tres caminos distintos:

- La empresa (`Entity`) no tenía moneda: solo `language`.
- El panel fijaba `currency: "EUR"` a mano en diez sitios (`ContractCard`,
  `CustomerContractsSection`, `ContractExpenses`, `CustomerInsightsSections`,
  `ContractFormDialog`, `inventoryUi`, el contrato laboral…), y el tipo del contrato de la
  cartera (`CustomerContract.currency?: "EUR"`) no admitía otra cosa, ni en `shared` ni en el
  front.
- El informe de tareas llevaba el símbolo en tres cabeceras («Coste material (€)», «Coste
  unitario (€)», «Coste (€)»), y el asistente, los justificantes de gastos y la puesta en
  marcha escribían «€» o «EUR/h» en frases que lee el cliente.

La regla de Jose ya existía como criterio de producto: **nunca una unidad monetaria escrita en
cabeceras, etiquetas del panel, textos del asistente ni informes**. Se dice «Coste»,
«Importe», «Precio por hora». Y el dashboard operativo la había apuntado como decisión abierta
con un defecto declarado: «el importe sale sin moneda; el front pinta la moneda de la entidad;
si la entidad no la tiene configurada, pinta el número sin símbolo».

## Decisión

1. **La empresa tiene moneda.** `Entity.currency` es un código **ISO 4217 en mayúsculas**
   («EUR», «USD», «MXN»). Se normaliza al entrar (`normalizeEntityCurrency`: sin espacios, en
   mayúsculas, tres letras; otra cosa se rechaza). Se edita en la configuración de la empresa,
   junto al nombre y al idioma, con una lista corta de códigos frecuentes.
2. **Sin moneda, el número sin símbolo.** Una empresa que no la tiene configurada ve «1.234,56»
   y no «1.234,56 €». Nadie inventa euros por defecto en tiempo de lectura.
3. **La moneda nunca va escrita en el texto; va en el formato del número.** Las cabeceras y
   etiquetas dicen «Coste», «Importe», «Precio por hora». El símbolo lo pone el formateador
   (`Intl.NumberFormat` con la moneda de la empresa en el panel; `formatMoney` de `shared` en
   el servidor). En un fichero que no puede formatear por celda (el XLSX), la moneda se dice una
   sola vez en la cabecera de la hoja («Moneda: EUR»), y solo si la empresa la tiene.
4. **El contrato toma la moneda de la empresa.** `CustomerContract.currency` pasa a `string`
   (ISO). Al crear un contrato con importe y sin moneda, `customers` le pone la de la empresa;
   si la empresa no la tiene, el contrato se queda sin ella. Lo mismo hace la lectura por IA
   del PDF: primero la moneda que dice el documento, luego la de la empresa, nunca «EUR» fijo.
5. **Lo que cobra la plataforma queda fuera.** Almacenamiento (0,25 €/GB), quiosco, cuota de
   la suscripción, Stripe, el MRR del backoffice, el CRM de ventas: son nuestros precios y se
   cobran en euros. Esos textos no cambian.
6. **EUR a las existentes.** Todas las empresas en producción a esta fecha son españolas, así
   que el backfill les pone «EUR» y el alta de empresa nace con «EUR» mientras no se diga otra
   cosa. Es un dato escrito una vez, no un defecto que el código aplique al leer.

## Consecuencias

**Lo que cambia (rama `feat/moneda-de-la-empresa`):**

- `shared`: `Entity.currency?: string` + `normalizeEntityCurrency`; `platform/money.ts`
  (`formatMoney`, `currencySymbol`, `formatNumberEs`); `CustomerContract.currency: string`.
- `entities`: el alta escribe `currency: "EUR"` salvo que venga otra; la edición acepta
  `currency` y solo la toca si viene (un panel viejo no la borra). Script
  `scripts/backfill-entity-currency.ts`: simula por defecto, escribe con `--apply`.
- `customers`: el contrato toma la moneda de la empresa al crearse; `PATCH` admite cualquier
  ISO; el justificante del gasto escribe los importes con la moneda de la empresa o sin símbolo.
- `reports`: cabeceras «Coste material», «Coste unitario», «Coste»; línea «Moneda: X» en las
  hojas con dinero cuando la empresa la tiene.
- `assistant`: `PanelIdentity.entityCurrency`, `ToolContext.moneda()`, y todas las frases de
  la cartera y de gestionar la cartera formatean con ella. Las descripciones de las
  herramientas dicen «en la moneda de la empresa», no «en euros».
- `merlin`: la lectura del contrato del cliente toma la moneda del documento o de la empresa;
  la revisión y la siembra de la puesta en marcha dejan de escribir «€» y «EUR/h».
- Panel: `IEntity.currency`, un formateador único (`formatMoney` + `useMoney`), los diez sitios
  con `"EUR"` fijo pasan por él, selector «Moneda» en la configuración de la empresa,
  `ContractTerms.currency: string`.

**Backfill.** Una vez desplegado, en cada entorno:
`node services/entities/dist/scripts/backfill-entity-currency.js` (simula) y con `--apply`.
Hasta entonces, las empresas sin moneda ven los números sin símbolo: es el comportamiento
decidido, no un fallo.

**Lo que no cambia a propósito.** Los precios de la plataforma (`billing`, `pricing.ts`,
`storagePolicy.ts`, el quiosco, `MonthlyFeeCard` del panel), el backoffice (MRR, fichas) y el
CRM de ventas siguen en euros. El módulo de **contratos laborales** (convenios del BOE, SMI)
sigue escribiendo «€» en sus frases y `unit: "EUR"` en su dato: los convenios del catálogo son
españoles por construcción; se revisará cuando entre un convenio en otra moneda.

**Riesgo asumido.** Un panel sin desplegar contra una API nueva sigue mandando
`currency: "EUR"` en los contratos: la API lo acepta (es un ISO válido). Un panel nuevo contra
una API vieja mandaría la moneda de la empresa y la API vieja la rechazaría si no es «EUR»;
por eso la API va primero, como siempre.

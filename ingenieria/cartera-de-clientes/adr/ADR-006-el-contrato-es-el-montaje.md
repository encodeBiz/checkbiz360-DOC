# ADR-006 — El contrato es el montaje: un PDF del cliente, vinculado a una sucursal o a una tarea, contra el que el coste sale solo

**Fecha:** 2026-11-03
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Un posible cliente pidió sacar la **inversión, el coste y el beneficio de cada montaje**, y
que eso sirva para planificar y para la gestoría. La plataforma ya tiene las tres patas del
coste —horas con coste por hora del puesto, material con coste unitario y quién fue— pero
no tiene el ingreso, y la Fase 5 lo resolvía con un `CustomerBudget` aparte: horas o importe
tecleados para un lugar o para el cliente, contra los que se miraba el desvío.

Se barajó, y se descartó, un presupuesto por líneas (RRHH previsto, material previsto, otros
gastos). Jose lo paró en seco: *«no vamos a predecir ni calcular nada; si ellos tienen que
poner toda la info, ¿para qué nos quieren?»*. El valor está en que **lo real sale solo** de la
operativa y en que, con el histórico de montajes cerrados, se pueda **predecir algo** y
ahorrar tiempo.

## Decisión

1. **No hay presupuesto como objeto propio.** Lo que la empresa tiene es el contrato o el
   presupuesto que mandó a su cliente, **que es un PDF**. Ese PDF es el `CustomerContract`
   que ya existe en el documental (Fase 4), y lo único que se le añade es **lo que dice**:
   el importe, las fechas, el tiempo estimado y la complejidad.
2. **Un montaje es una sucursal o una tarea, nunca un cliente.** El contrato se **vincula**
   a una de las dos. Sin vínculo, el contrato solo tiene vigencia (rojo al vencer, como
   antes). Con vínculo, se convierte en un montaje con rentabilidad.
3. **Sin cliente no hay montaje.** La sucursal es una entidad libre y no cuelga nada de
   ella. El ingreso viene siempre de alguien que paga, y ese alguien es un cliente de la
   cartera. Lo que una empresa gasta en una sucursal propia sin nadie detrás ya lo ve en las
   estadísticas de coste; eso es control de gasto, no rentabilidad.
4. **Un contrato, un montaje.** Un contrato se vincula a **una** sucursal o a **una** tarea.
   Si cubre varias obras, se vincula a la sucursal que las agrupa y sus tareas quedan
   dentro. El margen es siempre `importe − coste`, sin repartir un importe entre montajes.
5. **El cliente agrega.** La ficha del cliente enseña sus contratos y, de cada uno, importe,
   coste, margen y previsión. Es la segunda capa que se pedía, sin un segundo presupuesto.
6. **Solo se pide lo que ya tienen.** Al subir el PDF, la IA lee importe, fechas, tiempo
   estimado y complejidad, y dice de dónde ha sacado cada cosa. Lo que no encuentra queda
   vacío, nunca inventado. **Todo es editable en cualquier momento.** La primera lectura y la
   primera estimación guardada se conservan aparte: la previsión aprende de lo que se estimó
   al principio, no de lo que alguien corrigió al final para que cuadrase.
7. **Lo real sale solo y en bruto.** Horas de quien fichó en esa sucursal o hizo esa tarea
   × el `price` del puesto (salario bruto por hora, el que ya hay en la ficha), más el
   material de los movimientos de inventario de esa sucursal o esa tarea × coste unitario.
   **Sin cotizaciones ni coste de empresa en esta versión**; si llega la nómina por a3innuva,
   se revisa entonces. Lo que no tiene coste se marca «sin coste», nunca cero.
8. **La previsión viene del histórico, no de un formulario.** Cada montaje cerrado deja lo
   estimado frente a lo real. De ahí sale, por empresa y por complejidad, cuánto se suelen
   desviar; con eso se da una **horquilla** de coste y margen antes de empezar y durante el
   montaje, y un aviso cuando lo proyectado pasa del importe. Con pocos montajes cerrados
   **no se enseña ninguna cifra**: se dice que no hay histórico suficiente.

## Justificación

**El contrato ya es un objeto del módulo.** Añadirle cuatro campos y un vínculo es mucho
menos que mantener dos cosas —contrato y presupuesto— que en la práctica son el mismo papel.
Y sitúa el ingreso donde está en la vida real: en lo que se firmó con el cliente.

**El montaje es donde se ficha y donde se trabaja.** La sucursal (construcción, eventos) y
la tarea (SAD, limpieza, un montaje puntual) son las dos unidades a las que ya se imputan
horas y material por el ADR-003 y por inventario. Colgar el contrato de una de ellas es usar
la imputación que existe, no inventar otra. El cliente no es una unidad de trabajo: es a
quien se le cobra, y por eso solo agrega.

**Lo que da valor es que no haya que mantenerlo.** Un presupuesto por líneas se queda viejo
el día que se asigna a alguien más o se saca un rollo de cable de más. Lo real, leído de la
operativa, no se queda viejo nunca. Y el único dato que pedimos —el PDF— ya existe y se sube
una vez.

**Lo estimado tiene que congelarse para poder aprender.** Si la previsión usara el tiempo
estimado «actual», bastaría con corregirlo al final para que la desviación desapareciera, y
con ella la señal. Por eso `initialEstimate` es de solo lectura.

**En bruto, porque es lo que tenemos y lo que se puede defender.** El `price` del puesto es
salario; el coste de empresa depende de contrato, actividad y convenio, y no lo sabemos. Un
margen en bruto con la etiqueta «en bruto» es honesto; un margen «neto» con una cotización
estimada es nombrar una causa que no está establecida. Es la regla de la casa: nombrar lo
observado.

## Consecuencias

- `CustomerBudget` desaparece del diseño antes de haberse construido. `customer_budgets` no
  se crea. La ADR-004 queda revisada: la tarifa sigue valorando las horas (importe facturable
  del periodo, para quien cobra por hora); el contrato con importe cubre el precio cerrado.
- `CustomerContract` gana `link`, `amount`, `estimatedHours`, `complexity`, `extraction`,
  `initialEstimate` y `closedAt`. Modelo en [03](../03_modelo-de-datos.md).
- Vincular un contrato a una sucursal exige que la sucursal esté **dedicada** a ese cliente
  (ADR-003); si no lo está, el servidor devuelve 409 y el panel ofrece dedicarla en el mismo
  gesto. Así las horas de esa sucursal ya son del cliente sin regla nueva.
- `customer_hours_daily` gana el coste por hora del puesto en el momento del fichaje, para
  que el coste de RRHH se sume sin volver a la ficha. Un contrato cerrado escribe una fila en
  `contract_outcomes`, que es de donde aprende la previsión.
- La lectura del PDF va por el mismo camino que la lectura de cuadrantes: propuesta con
  evidencia, confirmación, nada se guarda sin que alguien lo vea.
- Queda abierto si esta capa es **core o add-on** (D11 en [06](../06_decisiones-abiertas.md)).
  La cartera básica, los contratos con vigencia y el informe por cliente siguen siendo core;
  lo que decide D11 es la rentabilidad y la previsión.
- **Fuera**: presupuestos por líneas, coste de empresa y cotizaciones, reparto de un contrato
  entre varios montajes, previsión por equipo (qué personas fueron). Todo con su sitio para
  volver cuando alguien lo pida con un caso.

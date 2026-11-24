# TDR-001 — Consumo de IA por empresa

**Fecha:** 2026-11-24
**Estado:** Decisión de Jose del 22-nov-2026. Registro en código el 24-nov: en `develop` (9fe614c) y EN STAGING (5afe784) desde ese día. Precio, pantalla y cobro abiertos.
**Componentes:** `packages/shared` (registro y lectura), `services/merlin` (todas las llamadas
conectadas), `services/backoffice` y `services/billing` (pendientes).

---

## 1. Problema

Cada llamada a un modelo cuesta dinero y lo paga Encodebiz, haga la llamada quien la haga. La
API devuelve en cada respuesta cuántos tokens entraron, cuántos vinieron de caché, cuántos
salieron y cuántos fueron razonamiento, y hasta ahora ese dato **se tiraba**. Solo la lectura
de tablas de convenio lo guardaba, y para enseñarlo, no para sumarlo.

Medido en staging del 22 al 23-nov-2026 (contratos-laborales, TDR-001 del catálogo): una
lectura de contrato con tablas costaba **35–48 mil tokens**. Con el catálogo baja, pero sigue
sin saberse cuánto gasta cada empresa, y sin eso no se puede ni fijar un precio ni saber si una
empresa está costando más de lo que paga.

El almacenamiento tuvo el mismo problema y se resolvió contando todo desde un trigger
([almacenamiento/README.md](../../almacenamiento/README.md)). Aquí no hay trigger: el único
sitio por el que pasan todas las llamadas es el envoltorio de `shared`.

## 2. Decisión (Jose, 22-nov-2026)

«El consumo de tokens se va a cobrar a cada empresa como el almacenamiento (una cantidad
incluida y el exceso facturado), así que **desde ya se guarda por empresa**.»

De ahí salen tres reglas:

1. **Toda llamada que trabaje para una empresa apunta su consumo contra el `entityId`.** La que
   no trabaje para ninguna (el CRM, el análisis de un cliente para la dirección, lo que
   siembra Encodebiz) va a `system`.
2. **En un único punto**: `CustomGptService.create(params, ctx)` de `packages/shared/src/openai.ts`.
   Ningún módulo suma por su cuenta; contaría doble.
3. **Nada se limita todavía.** Se cuenta y se enseña; se cobra cuando haya precio. Igual que
   los 2 GB: lo que no se midió no se puede cobrar después.

## 3. Modelo de datos

### 3.1 `ai_usage/{entityId}_{YYYY-MM}` (colección raíz)

```ts
{
  entityId: string;            // "system" para lo que Encodebiz hace para sí
  month: string;               // "2026-11", UTC
  calls: number;
  inputTokens: number;         // incluye los de caché
  cachedInputTokens: number;   // parte de inputTokens servida de caché (más barata)
  outputTokens: number;        // incluye el razonamiento
  reasoningTokens: number;     // parte de outputTokens que fue razonamiento
  byPurpose: Record<string, Contadores>;   // los mismos cinco, por propósito
  byModel: Record<string, Contadores>;     // los mismos cinco, por modelo ("gpt-5-mini", "gpt-4_1")
  updatedAt: Date;
}
```

- Un documento por empresa y mes, con `set(…, {merge: true})` y `FieldValue.increment`. Sin
  trozos: Firestore aguanta una escritura por segundo en un documento y ninguna empresa llama
  al modelo a ese ritmo. Si algún día lo hace, se trocea como `storage_shards`.
- Las claves de los mapas llevan los puntos cambiados por `_`: en Firestore un punto en una
  clave es una ruta.
- `byModel` lleva los cinco contadores y no solo `calls` porque el precio es por modelo: sin
  los tokens por modelo no se puede poner la cifra después.

### 3.2 El contexto de la llamada

```ts
interface AiUsageContext { entityId: string | null; purpose: string }
```

`purpose` es para qué fue, en slug: `contrato_laboral`, `tabla_convenio`, `contrato_cliente`,
`gasto`, `cuadrante`, `puesta_en_marcha`, `relato_panel`, `interpretacion`, `analisis_cliente`,
`investigacion`. La tabla con cada una y de dónde sale su `entityId` está en el
[README](../README.md#para-qué-fue-purpose).

## 4. El único punto de registro

`packages/shared/src/platform/aiUsage.ts`:

- `aiUsageDelta(usage, model, ctx)` — puro y probado (`test/aiUsage.test.ts`): de un `usage`
  de la Responses API (`input_tokens`, `input_tokens_details.cached_tokens`, `output_tokens`,
  `output_tokens_details.reasoning_tokens`) saca los incrementos; `null` si no hay un `usage`
  legible (streaming, un fake de prueba, un error).
- `recordAiUsage(res, model, ctx, db?)` — escribe el documento del mes. **Nunca lanza ni
  retrasa**: `void …catch(console.error)`. La lectura de un contrato no puede fallar porque no
  se haya podido anotar lo que costó.
- `readAiUsage(db, entityId, month)` — lo lee.

`CustomGptService.create(params, ctx?)`: tras la respuesta, con `ctx` llama a `recordAiUsage`
con el modelo que de verdad se mandó (`merged.model`, que puede venir del defecto del
servicio); sin `ctx`, `console.warn` de una línea con el nombre del `json_schema`, para que en
los logs se vea lo que falta por conectar. No se corta la llamada.

Lo que **no** cuenta: el `usage` que `tablas.ts` guarda en `agreements/{a}/tables/{año}` sigue
ahí para enseñarlo en backoffice, pero no suma. Lo mismo el `consumo` que devuelven la
investigación y el análisis de cliente al que los pidió: informativo, no contable.

## 5. Llamadas conectadas (24-nov-2026)

Todas las de `services/merlin`. Las lecturas no cambian de comportamiento: solo reciben el
contexto, como último parámetro opcional, así que los fakes de las pruebas siguen valiendo.

| Dónde | `purpose` | `entityId` |
|---|---|---|
| `contratos-laborales/application/leer.ts` ← `leerTexto.ts` ← `infrastructure/lecturas.ts` | `contrato_laboral` | `c.entityId` del documento |
| `contratos-laborales/application/tablas.ts` ← `infrastructure/tablasConvenio.ts` | `tabla_convenio` | `fuente.entityId ?? (createdBy !== "system" ? createdBy : null)` |
| `contratos/application/leer.ts` ← `contratos.router.ts` | `contrato_cliente` | `:entityId` de la ruta |
| `gastos/application/leer.ts` (`leerTicket` ← `leerDesdeTexto` ← `leerFichero`) ← `gastos.router.ts` y `documento.ts` | `gasto` | `entityId` del cuerpo |
| `cuadrantes/application/leer.ts` ← `cuadrantes.router.ts` / `cuadrante.cli.ts` | `cuadrante` | cuerpo / `--entity` (sin él, `system`) |
| `turno/turno.ts` ← `soporte.router.ts` / `conversar.cli.ts` | `puesta_en_marcha` | `borrador.entityId` (sin él, `system`) |
| `infrastructure/openai.renderer.ts` ← `modules/application/getOrCreatePanelAnalysis.ts` | `relato_panel` | `request.entityId` |
| `infrastructure/openai.renderer.ts` ← `application/interpret.usecase.ts` | `interpretacion` | `request.entityId` |
| `analisis-cliente/analizar.ts` (directo, sin envoltorio: usa `conversation`) | `analisis_cliente` | `system` |
| `investigacion/investigar.ts` y `senales.ts` (dos llamadas cada uno) | `investigacion` | `system` |

`puesta-en-marcha/application/sembrar.ts` sale en el `grep` de `.create({` pero son altas en
los repositorios de entidad y sucursal, no llamadas al modelo.

Fuera de `merlin` nadie usa `CustomGptService` hoy. El día que otro servicio lo use, pasará
`ctx` o dejará la línea de aviso.

## 6. Abierto

1. **Precio e incluido por plan.** Sin cifra. Para fijarla hace falta el coste por millón de
   tokens de cada modelo en uso (entrada, entrada en caché, salida; el razonamiento se cobra
   como salida) y un mes de consumo real medido con esto. El modelo del almacenamiento (una
   cantidad incluida para todos, exceso en una línea aparte) es el punto de partida que dio
   Jose.
2. **Pantalla de backoffice**: consumo por empresa y mes, por propósito y por modelo; y la de
   `system`, que es lo que Encodebiz se gasta en sí misma.
3. **Aviso a la empresa** al acercarse a lo incluido: uno, como el del 90 % de Storage, por
   correo a `billingEmail` y en Suscripciones.
4. **Cobro en `billing`**: una línea en la factura del ciclo desde `invoice.created`, con
   `metadata.kind = "ai"`, una sola vez por factura, como la de GB. Y la misma decisión
   pendiente que allí: las empresas sin suscripción de pago se cuentan y se enseñan, no se
   cobran.
5. **Reglas de Firestore** de `ai_usage` (solo servidor) e **índice** si la pantalla lista por
   mes.
6. **`analisis_cliente` a `system`**: se ha decidido así porque lo pide la dirección de
   Encodebiz, no la empresa analizada. Si Jose prefiere apuntarlo a la empresa de la ficha, es
   un parámetro en la ruta `/analisis-cliente` y una línea.

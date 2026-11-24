# Consumo de IA por empresa — contar los tokens de los modelos · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** transversal — toda llamada a un modelo (`services/merlin`, y lo que venga) × `billing`
**Fecha de inicio:** 2026-11-22 (decisión de Jose) · **Código:** 2026-11-24
**Estado:** registro en código, en rama (`feat/convenios-abiertos`, pendiente de `develop` → `staging`). **No se cobra nada todavía:** falta fijar precio y cantidad incluida, la pantalla y la línea de factura. Ver [TDR-001](tdr/TDR-001-consumo-de-ia-por-empresa.md).
**Autor:** Jose Acevedo (decisión) · diseño con Claude

---

## Qué es

Cada vez que un módulo llama a un modelo para una empresa (leer un contrato, una tabla de
convenio, un ticket, un cuadrante; narrar el panel), la API devuelve cuánto costó en tokens.
Hasta el 24-nov-2026 ese dato se tiraba, salvo en la tabla del convenio, que lo guardaba para
enseñarlo. Desde esta rama **se apunta por empresa y mes**, con el mismo patrón que el
almacenamiento ([almacenamiento/README.md](../almacenamiento/README.md)): se cuenta todo lo que
se pueda atribuir, nada se limita, y lo que pase de lo incluido se cobrará cuando se fije el
precio.

Lo que Jose fijó el 22-nov: «el consumo de tokens se va a cobrar a cada empresa como el
almacenamiento, así que desde ya se guarda por empresa».

## Dónde se cuenta: un único punto

Todas las llamadas a OpenAI pasan por `CustomGptService.create(params, ctx)` en
`packages/shared/src/openai.ts`. El segundo parámetro, `ctx: {entityId, purpose}`, dice para qué
empresa y para qué se llama; con él, el envoltorio apunta el `usage` de la respuesta
(`packages/shared/src/platform/aiUsage.ts`). **Ningún módulo suma por su cuenta**: contaría
doble. Es la misma regla que en Storage, donde cuenta el trigger y no quien sube.

Una llamada **sin `ctx`** no se corta —la lectura vale más que el apunte— pero deja una línea en
el log para verla:

```text
[ia] llamada al modelo sin empresa a la que apuntar el consumo: <nombre del json_schema>
```

Si aparece en los logs de staging, hay una llamada nueva sin conectar.

La única llamada que no pasa por el envoltorio es el análisis de cliente del backoffice
(`soporte/analisis-cliente/analizar.ts`), que usa `conversation` y el cliente de OpenAI
directo; esa llama a `recordAiUsage` ella misma, en el mismo sitio donde lo haría el envoltorio.

## Dónde se guarda

Colección raíz `ai_usage`, **un documento por empresa y mes**:

```text
ai_usage/{entityId}_{YYYY-MM} = {
  entityId, month: "2026-11",
  calls, inputTokens, cachedInputTokens, outputTokens, reasoningTokens,
  byPurpose: { contrato_laboral: {calls, inputTokens, cachedInputTokens, outputTokens, reasoningTokens}, … },
  byModel:   { "gpt-5-mini": {calls, inputTokens, cachedInputTokens, outputTokens, reasoningTokens}, … },
  updatedAt
}
```

- Se escribe con `set(…, {merge: true})` y `FieldValue.increment`, como los trozos del contador
  de Storage. Sin trozos: una empresa no hace diez llamadas al modelo por segundo.
- `entityId` es **`system`** para lo que Encodebiz hace para sí (la investigación del CRM, las
  señales, el análisis de un cliente para la dirección, los convenios que siembra Encodebiz).
- `reasoningTokens` va **dentro** de `outputTokens` (es la parte de la salida que fue
  razonamiento) y `cachedInputTokens` dentro de `inputTokens`. Se separan porque se cobran a
  precios distintos.
- Las claves de `byModel` y `byPurpose` llevan los puntos cambiados por `_` (`gpt-4_1`), que un
  punto en una clave de Firestore es una ruta.
- El mes es el de UTC en el momento de la llamada.

El apunte **nunca lanza ni retrasa** a quien llama: `recordAiUsage` es `void` y traga el error
en el log (`[ia] consumo sin apuntar`). Un CLI sin credenciales de Firebase lee igual.

## Para qué fue: `purpose`

| `purpose` | Llamada | De dónde sale el `entityId` |
|---|---|---|
| `contrato_laboral` | lectura del contrato de trabajo (`contratos-laborales/application/leer.ts`) | el documento: `entities/{e}/documents/{d}` (`lecturas.ts`, `c.entityId`) |
| `tabla_convenio` | tablas de un convenio y año (`contratos-laborales/application/tablas.ts`) | la empresa que aportó el convenio: `source.entityId` de la tabla, o `createdBy` del convenio; sembrado por Encodebiz → `system` |
| `contrato_cliente` | contrato o presupuesto de un cliente (`contratos/application/leer.ts`) | la ruta: `/contratos/:entityId/...` |
| `gasto` | ticket o justificante (`gastos/application/leer.ts`) | el cuerpo de la petición (`entityId`), por la tarea o por el documental |
| `cuadrante` | cuadrante subido (`cuadrantes/application/leer.ts`) | el cuerpo de la petición; en el CLI, `--entity` o `system` |
| `puesta_en_marcha` | la conversación de alta (`turno/turno.ts`) | `borrador.entityId` si la empresa ya existe; si no, `system` |
| `relato_panel` | el relato del panel por tab (`getOrCreatePanelAnalysis.ts`) | `request.entityId` |
| `interpretacion` | relato de un centro o de una persona (`interpret.usecase.ts`) | `request.entityId` del contexto de interpretación |
| `analisis_cliente` | análisis de un cliente para la dirección (`analisis-cliente/analizar.ts`) | `system`: lo hace Encodebiz para sí |
| `investigacion` | investigación y señales del CRM (`investigacion/*.ts`) | `system`: es ventas de Encodebiz |

Un `purpose` nuevo es un slug en minúsculas con `_`. Se añade aquí al conectarlo.

## Cómo leerlo

En código, `readAiUsage(db, entityId, "2026-11")` de `@encodebiz/shared` devuelve los
contadores, `byPurpose` y `byModel` (`null` si la empresa no llamó ese mes). Desde el
contenedor de desarrollo, mientras no haya pantalla:

```bash
docker compose -f docker-compose.staging.yml -p encodebiz-api-dev exec -T merlin node -e '
const {firestore, readAiUsage} = require("@encodebiz/shared");
readAiUsage(firestore, process.argv[1], process.argv[2]).then((u) => console.log(JSON.stringify(u, null, 2)));
' <entityId> 2026-11
```

Lo que hace Encodebiz para sí: `readAiUsage(firestore, null, "2026-11")` (documento
`system_2026-11`).

## Qué falta

- **Precio y cantidad incluida** por plan. No hay cifra: Jose no la ha dado y no se inventa.
  Lo que hay que tener delante para fijarla es el coste por millón de tokens de cada modelo
  (entrada, entrada en caché, salida) y lo que consume de verdad una empresa en un mes, que es
  lo que esto empieza a medir.
- **Pantalla de backoffice** (consumo por empresa y mes, por propósito) y, cuando se cobre,
  **el bloque en Suscripciones del panel**, como el de almacenamiento.
- **Aviso a la empresa** cuando se acerque a lo incluido, uno solo, como el del 90 % de Storage.
- **La línea en la factura** desde `billing` (`invoice.created`), como el exceso de GB.
- **Reglas de Firestore** de `ai_usage`: solo el servidor escribe; hoy nadie la lee desde
  cliente.
- **Llegar a staging**: la rama está en `feat/convenios-abiertos`; hasta que pase por
  `develop` → `staging` no hay un solo documento en `ai_usage` de desarrollo.

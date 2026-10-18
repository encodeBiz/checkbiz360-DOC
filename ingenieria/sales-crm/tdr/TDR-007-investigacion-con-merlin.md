# TDR-007 — Investigación con Merlin

**Fecha:** 2026-10-16
**Estado:** En implementación
**Decisión:** [ADR-009](../adr/ADR-009-merlin-investiga-en-el-servidor.md)
**Componentes:** `services/merlin` (la IA), `services/sales` (la cola y la escritura), backoffice (botón)

---

## 1. Flujo

```
sales (cola o botón) ──POST /gpt/investigacion/cuenta──▶ merlin ──Responses API + web_search──▶ OpenAI
      ▲                                                     │  paso 1: dossier de hechos con URLs consultadas
      │                                                     │  paso 2: perfil JSON estricto, solo con esas URLs
      └── valida pruebas, guarda perfil/contactos/encaje ◀──┘  + lista de URLs citadas + consumo
```

**Dos llamadas, a propósito.** La primera busca y escribe un dossier en texto; de su
respuesta se extraen las URLs consultadas (`url_citation` de la API, no del texto del
modelo). La segunda, sin herramientas, convierte el dossier en el JSON del perfil y solo
puede citar URLs que estén en el dossier. Separarlas evita depender de cómo combine la API
las citas con la salida en JSON, deja el dossier como pieza auditable y hace la segunda
llamada barata.

## 2. Contrato de Merlin

`POST /api/v1/gpt/investigacion/cuenta` (S2S). Entrada: cuenta (`id`, `name`, `legalName`,
`cif`, `domain`, `niche`, `province`, `employeesBand`, `linkedinUrl`), señales vivas
(`kind`, `title`, `sourceUrl`, `detectedAt`), contactos ya conocidos (nombre y cargo) y, si
lo hay, el perfil anterior (resumen) para no repetir. Salida:

| Campo | Qué es |
|---|---|
| `estado` | `ok` · `no_identificada` (no se pudo atar la web a CIF/dominio/concurso) · `insuficiente` (identificada, pero sin dolores con prueba) |
| `identidad` | `{ confirmada, como, urls[] }`: qué dato la confirma |
| `perfil` | `summary`, `pains[{pain, evidence}]`, `hook`, `roiInputs`, `sources[]` — ya filtrados por las URLs citadas |
| `descartados` | dolores que el modelo propuso y se tiraron por falta de prueba (para medir) |
| `decisores` | `[{ nombre, cargo, fuenteUrl, papel }]` solo con fuente citada |
| `encaje` | `{ puntos 0-100, motivos[] }` según `tam-icp/references/criterios-icp.md` |
| `huecos` | lo que no se ha podido saber |
| `consumo` | modelo, tokens de entrada/salida/razonamiento, búsquedas, ms |

## 3. Comprobaciones en el servidor (las que no dependen del modelo)

1. `citadas` = las páginas que abrió la herramienta de búsqueda
   (`web_search_call.action.sources`, que hay que pedir con
   `include: ["web_search_call.action.sources"]`) más las anotaciones `url_citation` del
   mensaje, normalizadas (sin fragmento, sin `utm_*`). Las dos las produce la API, no el
   modelo. **Comprobado el 2026-10-16 en producción:** con `gpt-5-mini` las anotaciones
   llegan vacías siempre (incluso en texto plano), así que sin el `include` todo saldría
   `insuficiente`; fue lo que pasó en la primera ejecución real. Si `citadas` está vacía →
   `insuficiente` con motivo «no consultó la web».
2. Identidad: `identidad.confirmada` y al menos una de sus `urls` ∈ `citadas`; si no →
   `no_identificada`.
3. Cada `pain.evidence` ∈ `citadas`; si no, a `descartados`. Cero dolores → `insuficiente`.
4. `sources` = `citadas` ∩ (las usadas en el perfil), nunca más de 30.
5. `roiInputs`: toda cifra sin `fuente` ∈ `citadas` se marca `assumed: true`.
6. Decisores: `fuenteUrl` ∈ `citadas`; sin email ni teléfono salvo que vengan de la web de la
   propia empresa (dominio de la cuenta). Papel: `decider` solo si el cargo lo dice
   (gerente, director general, CEO, administrador); el resto, `influencer`.
7. Textos pasan por el saneado de `sales` al guardar (controles, longitudes).

## 4. Lo que `sales` guarda

- `estado = ok`: `SaveProfile` (actor `merlin:investigacion`) → la cuenta pasa a
  `researched`; contactos nuevos por nombre (sin duplicar por nombre dentro de la cuenta);
  `icpFit` si estaba vacío; nota interna «Investigada por Merlin: N dolores con prueba, M
  fuentes, huecos: …».
- `no_identificada` / `insuficiente`: nada en el perfil; nota interna con el motivo y lo
  que propuso sin prueba, para que una persona lo retome. La cuenta sigue en `signal`.
- Siempre: fila en `sales_research_runs` (migración `038`): cuenta, estado, modelo, tokens,
  búsquedas, duración, error, dolores aceptados/descartados.

## 5. La cola

`startResearchSweep` en `sales`, apagado salvo `CRM_INVESTIGACION=on`. Un día laborable a
las `CRM_INVESTIGACION_HORA` (7, Madrid), antes del correo de agenda: cuentas en `signal`
sin perfil, con señal `high` viva primero, luego por `icp_fit`, luego las más antiguas;
hasta `CRM_INVESTIGACION_MAX_DIARIAS` (5) y `CRM_INVESTIGACION_MAX_TOKENS_DIA` (400.000);
una cuenta con un intento real en los últimos `reintentoDias` (7) espera. Un intento
`failed` no cuenta —Merlin caído u OpenAI sin crédito no dicen nada de la empresa— y,
además, para el barrido del día: sin crédito las cinco fallarían igual (el 429 del
16-oct lo enseñó). Se ejecutan en serie. Manual: `POST /crm/accounts/:id/research` y botón «Investigar con Merlin» en la
ficha (permiso `crm:write`).

## 6. Configuración

| Variable | Por defecto | Qué |
|---|---|---|
| `CRM_INVESTIGACION_MODELO` | `gpt-5-mini` | Modelo de las dos llamadas |
| `CRM_INVESTIGACION_RAZONAMIENTO` | `medium` | `reasoning.effort` |
| `CRM_INVESTIGACION_BUSQUEDA` | `high` | `search_context_size` de la herramienta web (desde el 16-oct; elegible en Ajustes) |
| `CRM_INVESTIGACION_MAX_SALIDA` | `16000` | tokens de salida por llamada; en la familia gpt-5 el razonamiento cuenta dentro, y el perfil con esfuerzo alto usa el doble |
| `CRM_CONOCIMIENTO_DIR` | `/app/conocimiento-crm` | ficheros de nicho/producto (copiados del plugin) |
| `MERLIN_INTERNAL_URL` | `http://merlin:3001` | desde `sales` |
| `CRM_INVESTIGACION`, `_HORA`, `_MAX_DIARIAS`, `_MAX_TOKENS_DIA` | off, 7, 5, 400000 | la cola |

## 7. La prueba de 10

`node services/sales/dist/scripts/investigar-merlin.js --account <id> --dry-run` investiga
sin guardar y enseña el resultado junto al perfil actual (el de Claude). Se pasa por las 10
cuentas de limpieza ya investigadas; Jose compara. Repetible con `--model` para medir un
modelo mayor. El prompt está en [08](../08_el-prompt-de-investigacion.md).

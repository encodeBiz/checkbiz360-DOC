# TDR-009 — Prompts editables desde Ajustes y búsqueda de señales con Merlin

**Fecha:** 2026-10-18
**Estado:** En implementación
**Decisión:** [ADR-010](../adr/ADR-010-prompts-desde-ajustes-y-senales-con-merlin.md)

---

## 1. Ajustes (TDR-008, ampliado)

Nuevos campos en `sales_crm_settings.settings` (JSONB; sin migración):

```
investigacion.prompts: { dossier: string | null, perfil: string | null }
senales: {
  altaAutomatica: boolean,        // CRM_SENALES_ALTA_AUTOMATICA (on)
  maxNuevasPorBusqueda: number,   // CRM_SENALES_MAX_NUEVAS (10)
  diasAtras: number,              // CRM_SENALES_DIAS (30): ventana por defecto
  prompt: string | null
}
```

`null` o vacío = el de fábrica. Tope de 20.000 caracteres por prompt en el esquema zod.
Modelo, esfuerzo, lectura de página y tope de tokens son los de `investigacion`: no se
duplican.

`settingsView` devuelve además `prompts.porDefecto = { dossier, perfil, senales }`, que
`sales` pide a Merlin (`GET /gpt/investigacion/prompts`, con respaldo vacío si Merlin no
contesta: el panel entonces no enseña el de fábrica y lo dice).

## 2. Contrato de Merlin

### `GET /api/v1/gpt/investigacion/prompts`
`{ ok, dossier, perfil, senales }`: los textos de fábrica tal cual están en `prompt.ts`.

### `POST /api/v1/gpt/investigacion/cuenta` (TDR-007 §2, ampliado)
Acepta `instrucciones: { dossier?: string, perfil?: string }`. Si vienen con texto,
sustituyen a las de fábrica en su paso; lo demás (esquema, conocimiento, comprobaciones)
no cambia.

### `POST /api/v1/gpt/investigacion/senales`
Petición:
```json
{ "nicho": "limpieza", "dias": 30, "foco": "Andalucía",
  "modelo": "gpt-5.4-mini", "razonamiento": "medium", "busqueda": "high",
  "instrucciones": "…opcional…" }
```
Dos llamadas: (1) búsqueda web con `INSTRUCCIONES_SENALES` (o las recibidas) y una entrada
con el nicho en una línea, la ventana de fechas (hoy menos `dias`), el foco, la tabla de
tipos y caducidad del skill `senales` y la sección «Señales de por qué ahora» del fichero
del nicho; `include: web_search_call.action.sources`. (2) JSON estricto `ESQUEMA_SENALES`
sin herramientas, con las URL consultadas como únicas citables.

Respuesta:
```json
{ "ok": true, "estado": "ok" | "insuficiente",
  "senales": [{ "empresa": { "nombre", "web", "cif", "provincia" },
                "kind", "titulo", "resumen", "fuenteUrl", "fecha", "fuerza",
                "caducaDias", "encaja", "porQue" }],
  "descartadas": [{ …igual…, "porque" }],
  "avisos": [], "dossier": "…", "citadas": ["…"], "consumo": { … } }
```

## 3. Comprobaciones en el servidor (Merlin, sin fiarse del modelo)

Una señal pasa si: `fuenteUrl` normalizada está en `citadas`; `kind` es uno de los del CRM;
`fuerza` es low/medium/high; `fecha` (si viene) cae dentro de la ventana; `caducaDias`
entre 1 y 180; nombre de empresa no vacío. `cif` y `web` sólo se conservan si el modelo
los atribuye a una página consultada (van en el mismo objeto; se limpian si la `fuenteUrl`
no pasó). Duplicados dentro de la misma respuesta (misma empresa normalizada + misma URL +
mismo tipo) se quedan con el primero. Lo que no pasa va a `descartadas` con `porque`.

## 4. Lo que `sales` guarda

Migración `041_sales_signal_searches.sql`:

```
sales_signal_searches (
  id, niche, days, focus, status ('running'|'ok'|'insufficient'|'failed'),
  model, input_tokens, output_tokens, reasoning_tokens, searches, duration_ms,
  found, attached, created_accounts, discarded, dry_run,
  requested_by, error, result JSONB, created_at, finished_at
)
```

`result` lleva cada hallazgo con su decisión: `attached` (cuenta existente, con
`accountId`), `created` (alta nueva, con `accountId`), `duplicate` (la señal ya estaba:
`external_ref`), `skipped` con motivo (`no_encaja`, `tope_altas`, `alta_apagada`,
`cuenta_existente_sin_senal`), y las `descartadas` de Merlin con su `porque`. Y el
`dossier`.

Caso de uso `searchSignals(store, merlin, input, ctx)`:
1. Presupuesto: tokens de hoy (investigaciones + búsquedas) ≥ `maxTokensPorDia` → 409
   `budget_exhausted`. Búsqueda en curso del mismo nicho → 409 `search_in_progress`.
2. Fila `running`; llamada a Merlin con prompts y modelo de Ajustes.
3. Por hallazgo: `findDuplicate({cif, domain})` → si no, `findByNormalizedName(nombre)`
   → si existe, `addSignal` con `externalRef = "merlin:" + sha1(kind|url|nombreNorm)`.
   Si no existe: alta si `encaja && altaAutomatica && creadas < maxNuevasPorBusqueda`
   (`source: outbound`, `motion: enter`, `createdBy: merlin:senales`, nota de actividad
   «Dada de alta por Merlin al buscar señales (#id)»), y la señal.
4. Cierra la fila con contadores, consumo y `result`.

`external_ref` reutiliza el índice único de 033; `findByExternalRef` evita el doble alta
de la misma señal cuando se repite la búsqueda.

El presupuesto compartido: `usageToday` devuelve `tokens` = investigaciones + búsquedas,
más `busquedasSenales`; el barrido de investigación lee el mismo total.

## 5. API

`sales` (`/api/v1/sales/crm`):
- `POST /signals/search` `{ niche, days?, focus?, dryRun? }` → 202 `{ searchId }`.
- `GET /signals/searches?limit=` → las últimas, sin `result`.
- `GET /signals/searches/:id` → con `result`.
- `GET/PATCH /settings`: los campos nuevos.

Backoffice (`/api/v1/backoffice/crm`): proxy de las tres, `crm:write` para lanzar
(auditoría `crm.busqueda_senales_pedida`), `crm:read` para leer.

## 6. Panel

- **Ajustes → Investigación con Merlin:** dos editores («Qué buscar y cómo escribir el
  dossier», «Cómo convertir el dossier en perfil») con el de fábrica debajo plegado,
  chip «Afinado» cuando difieren y «Restaurar el de fábrica». Aviso fijo: lo que no venga
  de una página consultada se descarta igual.
- **Ajustes → Señales con Merlin:** interruptor de alta automática, tope por búsqueda,
  días por defecto y el editor del prompt, con las mismas piezas.
- **CRM (pipeline):** botón «Buscar señales con Merlin» (`crm:write`) → diálogo con
  nicho (el del filtro si lo hay), días, foco; al lanzar, 202 y la lista de búsquedas
  recientes, que se refresca sola mientras haya una en curso; cada fila se despliega con
  los hallazgos (empresa, señal, fuerza, fecha, fuente, qué se hizo) y los descartes con
  su porqué.

## 7. Pruebas

- Merlin: `senales` con servicio falso — filtra URL no consultada, fecha fuera de
  ventana, tipo desconocido; respeta `instrucciones`; `GET /prompts` devuelve los tres.
- Sales: `searchSignals` con Merlin falso — ata a cuenta existente por CIF, por dominio y
  por nombre normalizado; crea hasta el tope y marca el resto; no crea con alta apagada;
  rechaza sin presupuesto; `usageToday` suma las búsquedas; la fila queda `failed` con el
  error si Merlin cae.
- HTTP: `settingsPatchShape` acepta y recorta los prompts; 202 y 409.

## 8. Pase

Migración 041 a mano (staging, luego prod). Sin variables nuevas obligatorias. Plugin de
Cowork sin cambios (el skill `senales` sigue valiendo para Claude).

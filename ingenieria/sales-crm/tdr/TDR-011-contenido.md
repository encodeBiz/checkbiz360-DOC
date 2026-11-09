# TDR-011 — Contenido: perfiles, fichas, publicaciones, revisión, adjuntos y MCP

**Fecha:** 2026-10-28 (revisado el mismo día con el segundo ejemplo)
**Estado:** En producción desde el 2026-10-28 (PR #231, migración `046`)
**Decisión:** [ADR-011](../adr/ADR-011-contenido-en-el-crm.md)
**Modelos de referencia** (los dos tienen que caber):
- Parrilla de LinkedIn 26-oct → 20-nov (artifact `QHiCY5yqgXbBR8xmg8dnEa`): doce posts con nicho,
  dolor → solución → funcionalidad, enlace con UTM, imagen publicada o captura a pedir, texto listo.
- `Plan_editorial_CheckBiz360_actualizado_28-10-2026.xlsx` (marketing): hojas *Seguimiento*
  (31 publicaciones T01…T31), *Fichas de redes* (P0…P11, E1…E3, Q1), *Blog pendiente* (N1, N2) y
  *Ya publicado* (inventario con decisión editorial).

---

## 1. Lo que enseñan los ejemplos

- **Perfil, no canal.** Se publica en «Instagram CheckBiz360», «LinkedIn CheckBiz360», «LinkedIn
  encodeBiz», «Instagram encodeBiz», «Blog encodeBiz»: canal × marca.
- **Una ficha, varias publicaciones.** P1 sale en Instagram (T01, 3-nov) y en LinkedIn (T14,
  6-nov); «el mismo ID comparte contexto, pero cada canal tiene» su enfoque. La ficha es el encargo;
  la publicación, la salida con fecha y perfil.
- **Tres pistas de trabajo por publicación** además del estado general: texto, imagen y revisión.
- **Dependencias.** «Enlazar N1 publicado», «N1 publicado; adaptar el resumen», «Solo si existe
  pregunta real».
- **Lo ya publicado manda.** Cada pieza anterior lleva una decisión editorial («no repetir
  presentación ni catálogo general»). Es lo que los agentes tienen que leer antes de proponer.

## 2. Modelo (migración nueva)

**`sales_content_profiles`** — dónde se publica: `id`, `name` («Instagram CheckBiz360»),
`channel` (`instagram` | `linkedin` | `blog` | …), `brand` (`checkbiz360` | `encodebiz`), `url`,
`active`. Se editan en Ajustes del CRM.

**`sales_content_briefs`** — la ficha (el encargo), sin fecha:

| Campo | Ejemplo |
|---|---|
| `code` | `P1`, `N1`, `E2`, `Q1` (único, lo pone quien planifica) |
| `kind` | `post` \| `article` |
| `title` | «Una tarea terminada: qué revisa el responsable» |
| `niche` | Los del CRM + `transversal` |
| `objective` | «Qué queremos explicar» / «Pregunta y resumen» |
| `added_value` | «Qué aporta frente al blog actual» (artículos) |
| `pain`, `solution`, `feature`, `doc_url` | Cadena dolor → solución → funcionalidad (parrilla de LinkedIn) |
| `image_brief` | «Qué imagen debes aportar» / «Portada: material e instrucciones» |
| `image_prompt` | «Instrucción para la IA de imágenes» |
| `caption_focus` | «Enfoque del pie / adaptación» |
| `review_checklist` | «Qué revisar conmigo» |
| `limits` | «No mostrar funciones no verificadas; no presentar simulaciones como caso de éxito» |
| `status` | `to_define` (artículo «pendiente de definir») → `defined` |
| `owner_staff_id` | Responsable de la ficha |

**`sales_content_items`** — la publicación (la «tarea» del Excel):

| Campo | Ejemplo / valores |
|---|---|
| `code` | `T01` |
| `brief_id` | Su ficha (nulo para lo ya publicado sin ficha) |
| `profile_id` | «Instagram CheckBiz360» |
| `title` | «Una tarea terminada: qué revisa el responsable» (por defecto, el de la ficha) |
| `scheduled_at` | Fecha y hora propuestas, editables |
| `status` | `pending`, `preparing`, `in_review`, `ready`, `scheduled`, `published`, `skipped` (Pendiente, En preparación, En revisión, Listo, Programado, Publicado, Omitido) |
| `text_status`, `image_status` | `pending`, `preparing`, `in_review`, `ready`, `not_applicable` |
| `review_status` | `pending`, `to_review`, `validated` (Pendiente, Por revisar, Validado) |
| `body`, `link_url` | El texto de este canal y su enlace (con UTM) |
| `depends_on_item_id`, `next_step` | «Enlazar N1 publicado» → la publicación T28; texto libre del siguiente paso |
| `published_at`, `published_url` | Fecha y enlace publicados |
| `editorial_decision` | Para lo publicado: «No repetir presentación ni catálogo general» |
| `notes` | «Mis notas» |
| `owner_staff_id` | Responsable de la publicación |

**`sales_content_assets`** — adjuntos de la ficha (capturas a aportar, referencias) o de la
publicación (la imagen final): `brief_id` o `item_id`, `kind` (`upload` | `url` |
`capture_request`), `storage_path`, `content_type`, `url`, `description`, `fulfilled_at`. Imágenes
(png, jpg, webp) y PDF, hasta 20 MB.

**`sales_content_signals`** — `brief_id`, `signal_id`: las señales que impulsan la ficha.

**`sales_content_events`** — el historial de fichas y publicaciones, solo se añade: `brief_id` o
`item_id`, `kind` (`created`, `edited` con campos antes/después, `status`, `comment`, `asset_*`,
`signal_linked`, `imported`), `payload` JSON, `actor`, `at`.

## 3. Reglas

- **Validar** (`review_status = validated`) es de una persona del backoffice. Un agente solo
  valida si una persona se lo pide en ese momento: `crm_content_review` con `validated` exige `requestedBy` y la
  frase de la petición, que quedan en el historial; sin eso, `approval_requires_person` (Jose:
  «solo personas aprueban, a no ser que se le pida expresamente»).
- Cambiar el texto o la imagen de una publicación validada la devuelve a `to_review`.
- `published` exige `published_url` (salvo blog en borrador interno) y fija `published_at`.
  Publicada, el texto no cambia: una corrección es un comentario.
- **En rojo, sin bloquear:** publicación vencida sin publicar; depende de otra aún sin publicar a
  2 días de su fecha; captura a aportar sin entregar a 3 días; ficha impulsada por una señal que
  caduca en menos de 7 días; artículo «pendiente de definir» con publicación en menos de 7 días.
- El estado general no se calcula de las tres pistas: lo mueve la persona. La ficha enseña el
  resumen de sus publicaciones.

## 4. Adjuntos

Los sube el backoffice al bucket del sistema, `crm/contenido/{briefs|items}/{id}/{uuid}-{nombre}`
(`POST /crm/content/{briefs|items}/:id/upload`, fichero crudo con su `Content-Type`), y los registra
en `sales`; si `sales` no lo acepta, se borra. Fuera del cobro de almacenamiento: no son de ninguna
empresa cliente (apuntado en la tabla de prefijos de `almacenamiento` como «no cuenta»).

**Se sirven por el backoffice, no con URL firmada** (`GET /crm/content/assets/:id/file`, con
sesión y `crm:read`): no depende de que la cuenta de servicio pueda firmar (`signBlob` ya falló en
dev) y un enlace copiado no abre nada sin sesión. Quitar un adjunto deja el evento y el fichero.

nginx: `location /api/v1/backoffice/crm/content/` con `client_max_body_size 22m` en los dos
entornos; el resto del backoffice sigue en 3 MB.

## 5. API, backoffice y MCP

HTTP en `sales`: `/content/profiles`, `/content/briefs`, `/content/items` (filtros: fechas,
perfil, canal, marca, estado y pistas, responsable, nicho, ficha, señal; paginación en servidor),
`/content/items/:id` (con ficha, adjuntos, señales, dependencias e historial), `PATCH`, `/status`,
`/review`, `/comments`, `/assets`, `/signals`, `/import`. Proxy en el backoffice con `crm:*` y
auditoría.

MCP (11 herramientas; el CRM pasa de 19 a 30): `crm_content_published` (lo publicado con su
decisión editorial: lo que se lee antes de proponer), `crm_content_list`, `crm_content_profiles`
(con sus notas), `crm_content_get`, `crm_content_plan` (crea o actualiza en bloque; simula salvo
`apply`), `crm_content_update`, `crm_content_comment`, `crm_content_mark_published`,
`crm_content_review` (validar solo por petición expresa, con `requestedBy` y `request`),
`crm_content_link_signal`, `crm_content_add_asset` (por URL o captura a pedir; subir ficheros es del
backoffice). Skills `crm`, `outreach` y `marca-personal` del plugin, actualizadas.

`outreach` lee lo publicado de las últimas 4 semanas del nicho y lo publicado sobre las señales de la
cuenta antes de redactar; `crm_get_account` lo indica.

## 6. Importación del Excel

La plantilla de marketing es el formato de entrada: **Seguimiento** → publicaciones, **Fichas de
redes** y **Blog pendiente** → fichas, **Ya publicado** → publicaciones `published` con su decisión
editorial (sin ficha). El perfil se casa por nombre con `sales_content_profiles` (los que no existan
se proponen). Las dependencias se leen de la columna «Dependencia / siguiente paso» cuando nombran
una ficha («N1 publicado» → la publicación de N1 en el Blog); el resto queda como texto.

Simula y enseña qué crearía, qué actualizaría (mismo `code`) y qué no entiende; solo escribe con
confirmación. La simulación corre lo mismo que la aplicación dentro de una transacción que se
deshace: lo que se enseña es lo que pasará.

Detalles de la hoja **Ya publicado**, vistos en el Excel del 28-oct:
- Las filas que no son una publicación sino un dato del perfil («LinkedIn CheckBiz360 · Sin
  publicaciones · Confirmación 22/10/2026») van a las **notas del perfil** (`notes`), no a la lista.
- Lo publicado sin código recibe uno estable, `YP-` + 8 hex del perfil, título y fecha: reimportar
  no duplica.
- «18 de septiembre» sin año: el de la importación, o el anterior si cayera en el futuro. «Publicado»
  sin fecha se queda **sin fecha**, no con la de hoy; sin decisión editorial, vacía.
- `Publicado` en Seguimiento sin enlace se importa como `Programado` y se avisa.
- El Excel de marketing lo guarda un programa con prefijos y rutas absolutas que `exceljs` no
  abre: se normaliza como en `merlin/…/cuadrantes/infrastructure/libro.ts`.

Probado con el Excel real del 28-oct (sin guardarlo en el repo): 4 hojas reconocidas, 18 fichas,
45 publicaciones (31 + 14 ya publicadas), 6 dependencias, 2 notas de perfil, 0 problemas. Volver a subir la versión siguiente del Excel actualiza por `code` y deja en el
historial lo que cambió. También por MCP (`crm_content_plan`) para lo que nace en una conversación.

## 7. Panel

Sección **Contenido** en el bloque Comercial: calendario (semana / mes, color por perfil, marca
«impulsada por señal»), lista de publicaciones con las tres pistas a la vista, fichas, «Ya
publicado» y perfiles. Ficha con sus publicaciones, adjuntos con vista previa, señales e historial.
En la señal, «Crear ficha» con la señal y el nicho puestos.

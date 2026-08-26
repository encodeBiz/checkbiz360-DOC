# 03 — Decisiones abiertas

> Lo que falta cerrar **antes** de comprometer implementación. Las dos primeras son de
> negocio (las decide producto); las de Fase 0 son verificaciones técnicas contra la cuenta.

---

## Decisiones de negocio

### D1 — ¿Cómo aterriza un `project` de Rentman en encodeBiz? — ✅ CERRADA (2026-07-26)

**Decisión:**
- El **`project` (evento/montaje) de Rentman → `branch`** de checkbiz360. Cada evento es
  un centro de trabajo con su localización → **geocerca de fichaje**. Bidireccional.
- El **`customer` (`contact`, cliente) NO es un branch.** Se aborda en **Fase 2** como una
  **estructura "Clientes / Contactos" a nivel de checkbiz completo** (core de plataforma,
  **no del módulo Rentman**). Rentman solo se engancharía a ella cuando exista. Ver `05_fases.md`.

**Razón:** en eventos/AV el empleado ficha en el **venue del evento**, no en la oficina del
cliente; el proyecto/evento es lo que semánticamente equivale a un centro de trabajo. Un
cliente puede tener muchos proyectos en sitios distintos (ej.: *Constructora X* → *Building Y*).

**Estado:** ✅ resuelta.

### D2 — ¿Quién manda en las horas? — ✅ CERRADA (2026-08-01)
El `timeregistration` es un registro **legal**.

**Decisión: Opción A — encodeBiz es siempre la autoridad de las horas**, porque es
encodeBiz quien garantiza el cumplimiento normativo del registro horario.

Consecuencias, ya implementadas en `services/rentman`:
- Una edición hecha en Rentman **nunca** vuelve ni sobreescribe el fichaje de checkbiz.
- Lo que sí hacemos es **detectarla y avisar**: cada jornada imputada se re-lee de
  Rentman cada 24 h; si sus horas no son las que dejamos, la fila pasa a `diverged`,
  se anota en `rentman_sync_log` (`direction = 'hours_divergence'`) y se expone en
  `GET /api/v1/rentman/hours/divergences/:entityId`.
- Tampoco pisamos la edición del cliente por nuestra cuenta: se le avisa y decide él.
  Re-imputar automáticamente sería otra decisión de producto, no está hecho.
- La huella (`pushed_hash`) es de **nuestras** horas: si la jornada se corrige en
  checkbiz, cambia la huella y se vuelve a empujar; si cambia en Rentman, no.

**Estado:** ✅ resuelta.

### D3–D5 — Integridad de datos en la sync
Derivadas del mapeo `Branch`/`Employee` (detalle en `06_mapeo-y-validacion.md` §4):
- **D3** — Rol por defecto del empleado importado (`internal` fijo vs regla por `tags`).
- **D4** — Geo del branch cuando falta `lat/lng`: ¿geocodificar automático o completar a mano?
- **D5** — Crew sin email: ¿crear en `pending_config` u omitir hasta tener correo?

**Estado:** ⛔ pendientes.

---

## Verificaciones de Fase 0 (técnicas) — CERRADAS el 2026-08-01

Script: `encodebiz-api/services/rentman/scripts/rentman-phase0.ts`, ejecutado contra la
**cuenta sandbox** del cliente. Detalle completo en `01_as-is.md` §5.

### F0-1 — Rate limit real — ✅ no es una restricción
120 peticiones seguidas en 16 s, ningún corte. Los 403 que se atribuían a throttling son
de colecciones inexistentes. La cadencia de 15 min con presupuesto por pasada va sobrada.

### F0-2 — Filtro por `modified` — ✅ resuelto (por orden, no por filtro)
No hay filtro por rango (`modified=gt,…` devuelve vacío), pero `sort=-modified` sí
ordena y `fields=` recorta. El delta se saca paginando por fecha descendente hasta la
marca de agua: sale igual de barato.

### F0-3 — Escritura — ✅ VALIDADA para `timeregistration`
`POST /timeregistration` funciona. Cuatro hallazgos que cambiaron el código: `leavetype`
es **obligatorio** (sin él, 500), `duration` es **neto** y lo recalcula Rentman, `remark`
persiste (trazabilidad), y **rechaza solapes** con un 400 que es definitivo. Probado de
punta a punta con el cliente real del servicio: crear → releer → comparar → borrar.

Sigue sin probarse la creación de `project` y `projectcrew` (capa de catálogo, bloqueada
por D3–D5), y todo esto es un **sandbox**: la cuenta real del cliente no se ha tocado.

---

### F0-4 — Espejar el modelo de servicio + planes (monetización)
Inspeccionar en `encodeBiz-SAAS/functions` cómo están modelados en Firestore los
servicios y planes de **checkbiz / passbiz** (colección, campos, activador `onActivate…`)
para **crear el servicio `rentman` y sus planes** con la misma estructura y reutilizar el
motor de facturación. Detalle en `04_activacion-saas.md` §5. **No inventar el esquema.**

---

## Bloqueos

- ~~La implementación **no arranca** hasta cerrar D1 y D2.~~ D1 y D2 cerradas: la
  **capa de tiempo (jornada → `timeregistration`) ya está implementada**. Lo que sigue
  bloqueado es la capa de catálogo/empleados, que depende de D3–D5.
- El coste/cadencia del sync depende de F0-1 y F0-2.
- El flujo de horas depende de F0-3.
- La monetización (servicio + planes) depende de F0-4 y de fijar la **tarifa** (producto).

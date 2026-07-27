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

### D2 — ¿Quién manda en las horas?
El `timeregistration` es un registro **legal**.

- **Opción A:** encodeBiz es **siempre** la autoridad. Una edición en Rentman no
  sobreescribe el fichaje de encodeBiz (a lo sumo se detecta y se avisa).
- **Opción B:** bidireccional también en horas: una corrección manual en Rentman
  **vuelve** y actualiza encodeBiz (con guardia de `updateHash`).

**Recomendación:** A, por trazabilidad legal. **Estado:** ⛔ pendiente de producto.

### D3–D5 — Integridad de datos en la sync
Derivadas del mapeo `Branch`/`Employee` (detalle en `06_mapeo-y-validacion.md` §4):
- **D3** — Rol por defecto del empleado importado (`internal` fijo vs regla por `tags`).
- **D4** — Geo del branch cuando falta `lat/lng`: ¿geocodificar automático o completar a mano?
- **D5** — Crew sin email: ¿crear en `pending_config` u omitir hasta tener correo?

**Estado:** ⛔ pendientes.

---

## Verificaciones de Fase 0 (técnicas, requieren tocar la cuenta)

Script: `encodebiz-api/services/checkinbiz/scripts/rentman-phase0.ts`.

### F0-1 — Medir el rate limit real
Rentman corta con 403 sin documentar el techo. Determina la **cadencia** del polling.
`… rentman-phase0.ts ratelimit --n 80`.

### F0-2 — ¿Filtro por `modified`?
Si la API permite `modified > X` / ordenar por `modified`, el polling trae solo el delta
(barato). Si no, diff por `updateHash` (más pesado al crecer el catálogo). **Decide el
coste del sync.**

### F0-3 — Validar la escritura
Ningún POST/PUT ejecutado aún. Falta confirmar contra sandbox (o prueba controlada y
reversible) que se puede crear:
- `timeregistration` con `{ crewmember, start, end }`,
- `project`, `projectcrew`.

Requiere **autorización explícita** para escribir en una cuenta real, o una sandbox.

---

### F0-4 — Espejar el modelo de servicio + planes (monetización)
Inspeccionar en `encodeBiz-SAAS/functions` cómo están modelados en Firestore los
servicios y planes de **checkbiz / passbiz** (colección, campos, activador `onActivate…`)
para **crear el servicio `rentman` y sus planes** con la misma estructura y reutilizar el
motor de facturación. Detalle en `04_activacion-saas.md` §5. **No inventar el esquema.**

---

## Bloqueos

- La implementación **no arranca** hasta cerrar D1 y D2.
- El coste/cadencia del sync depende de F0-1 y F0-2.
- El flujo de horas depende de F0-3.
- La monetización (servicio + planes) depende de F0-4 y de fijar la **tarifa** (producto).

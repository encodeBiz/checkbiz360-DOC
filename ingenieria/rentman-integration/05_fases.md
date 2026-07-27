# 05 — Fases

> Alcance por fases. La Fase 1 es la integración Rentman en sí; lo demás son ampliaciones,
> algunas **a nivel de plataforma checkbiz** (no del módulo Rentman).

---

## Fase 1 — MVP de la integración (add-on Rentman)

El add-on activable y su sync bidireccional por polling. Todo dentro del módulo Rentman.

- **Catálogo:** `project` (evento/montaje) de Rentman ↔ **`branch`** de checkbiz360
  (con su localización → geocerca). Bidireccional.
- **Asignaciones:** `projectcrew` ↔ asignación de trabajador al branch/proyecto.
- **Trabajo:** las asignaciones **generan tareas** (módulo `tasks`, solo checkbiz).
- **Tiempo:** la jornada (fichaje) → `timeregistration` en Rentman. Best-effort.
- **Empleados:** `crew` ↔ `employee` (mapping, auto-match por email).
- **Monetización:** servicio `rentman` + planes en Firestore (ver `04_activacion-saas.md`).

## Fase 2 — Estructura "Clientes / Contactos" (⚠️ nivel checkbiz, NO del módulo Rentman)

Un apartado de **Clientes / Contactos a nivel de toda la plataforma checkbiz**, no exclusivo
de Rentman. Es lógica rica y transversal (un cliente con varios proyectos/centros; ej.
*Constructora X* → *Building Y*). Aporta valor **con o sin** Rentman.

- Vive en el **core de checkbiz**, no en `integrations/rentman`.
- Cuando exista, la integración Rentman **se engancha**: el `customer` (`contact`) de Rentman
  se refleja en esa estructura de clientes y se enlaza al branch/proyecto.
- Hasta entonces, en Fase 1 el cliente de Rentman se queda como **dato/atributo** del branch,
  sin apartado propio.

**Estado:** no planificada aquí; es una iniciativa de plataforma. Este doc solo deja
constancia del enganche futuro.

## Fase 2+ (dentro de Rentman) — Desglose de horas por tarea/función

- Imputar el tiempo de cada tarea a Rentman como `timeregistrationactivity`
  (`time_registration` + `project_function` + `duration`). Capa de coste/facturación.
- Requiere que la tarea conozca su `project_function`. Ver `02_to-be.md` §4.5.

---

## Fuera de alcance (por ahora)

- Sincronizar equipment / almacén de Rentman.
- Facturación/depósitos de Rentman.
- Cualquier reescritura del catálogo de Rentman que no nazca de la operación de checkbiz.

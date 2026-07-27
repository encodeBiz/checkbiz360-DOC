# 02 — Arquitectura objetivo (to-be)

> **Qué cubre:** cómo queda la integración: sync bidireccional por polling desde el servicio `sync`, con encodeBiz como cabina de gestión.

---

## 1. Topología

```
        encodeBiz (cabina)                         Rentman (paralelo)
  ┌─────────────────────────────┐            ┌──────────────────────────┐
  │ checkinbiz: clientes/proyec-│            │ projects / contacts      │
  │ tos, asignaciones, tareas,  │            │ projectcrew              │
  │ fichaje (checklogs)         │            │ projectfunctions / crew  │
  └──────────────┬──────────────┘            │ timeregistration(activity)│
                 │                            └───────────▲──────────────┘
                 │  escribe/lee (REST)                    │
        ┌────────▼─────────┐   poll cada X (REST)         │
        │  servicio `sync` │◄────────────────────────────┘
        │  (job programado)│   reconcilia en ambos sentidos
        └────────┬─────────┘
                 │  mapping + estado en PostgreSQL
        ┌────────▼─────────┐
        │ rentman_*_mapping│  (crew↔employee, project↔…, projectcrew↔…)
        │ rentman_sync_log │
        └──────────────────┘
```

- **Sin webhooks.** No exponemos endpoint público ni gestionamos secret de webhook.
- **El `sync` manda el ritmo.** Un job programado (cada pocos minutos) ejecuta la
  reconciliación. Ver `adr/0001`.

## 2. El ciclo de reconciliación (una pasada)

Por cada tenant con la integración activa:

1. **Pull de Rentman** — traer lo cambiado desde el último `syncedAt`
   (por `modified` si la API lo permite; si no, diff por `updateHash`).
2. **Comparar** contra nuestra copia usando el mapping (`rentman_*_id ↔ encodebiz_id`)
   y el `updateHash` guardado.
3. **Aplicar entrantes** — crear/actualizar en encodeBiz lo que cambió en Rentman.
4. **Push de salientes** — enviar a Rentman lo que cambió en encodeBiz desde la
   última pasada (REST create/update).
5. **Registrar** cada objeto reconciliado en `rentman_sync_log` (sentido, estado, ids).

Idempotente: si una pasada falla o Rentman corta por rate-limit, la siguiente retoma
sin pérdida (no hay "eventos perdidos" como con webhooks).

## 3. Prevención de bucles (eco)

El riesgo de todo sync bidireccional: yo escribo en Rentman → en la siguiente pasada
leo ese cambio → lo vuelvo a escribir → ∞.

Cortafuegos:
- Guardamos el `updateHash` de Rentman tras cada escritura/lectura. Si el objeto que
  llega trae el hash que ya tenemos, es eco → se ignora.
- Guardamos `updatedAt` por lado en el mapping. Solo se propaga el lado cuyo cambio es
  **más nuevo que la última reconciliación** de ese objeto.

## 4. Los flujos en detalle — tres capas

⚠️ **No confundir asignación con jornada.** La asignación define *el trabajo* (→ tareas);
la jornada es *el envoltorio de tiempo* y contiene varias tareas. Son capas distintas.

### Capa 1 — Catálogo (↔ bidireccional)

**4.1 Proyecto / evento → branch** (D1 ✅)
- Rentman `project` (evento/montaje) ↔ **`branch`** de checkbiz360, con su localización →
  **geocerca de fichaje**. Bidireccional.
- El **cliente** (`customer` → `contact`) **NO es un branch**. En Fase 1 se guarda como
  dato/atributo del branch. La estructura **Clientes/Contactos** es una iniciativa **a nivel
  de plataforma checkbiz (Fase 2)**, no de este módulo → `05_fases.md`.

**4.2 Asignaciones**
- Rentman `projectcrew` (crew + projectfunction + periodo) ↔ asignación de trabajador a proyecto.
- Es "quién trabaja en qué proyecto/función", **no** un turno ni una jornada.
- Requiere que crew y projectfunction ya estén mapeados.

### Capa 2 — Trabajo: tareas (solo encodeBiz)

**4.3 Tareas**
- Rentman no tiene tareas. Viven en el módulo `tasks`.
- **Se derivan de la asignación**: un trabajador asignado a un proyecto recibe las tareas
  a ejecutar para ese proyecto. La asignación es el origen; la tarea es la unidad de trabajo.
- Nada que empujar a Rentman a nivel de "tarea" como tal. Es el foso de adopción.

### Capa 3 — Tiempo: jornada y horas (→ Rentman)

**4.4 Jornada (fichaje)**
- El checklog cerrado (checkin+checkout) es la **jornada**: el registro horario legal y el
  **envoltorio de tiempo**. Una misma jornada **cubre varias tareas**.
- Jornada total → Rentman `timeregistration` (`crewmember`, `start`, `end`, `break_duration`;
  duración en **segundos**; refs como **rutas string**).
- **Best-effort:** el fallo contra Rentman nunca bloquea el fichaje.
- **Decisión abierta:** ¿encodeBiz es siempre autoridad de las horas, o una corrección
  manual en Rentman debe volver y sobreescribir? → `03_decisiones-abiertas.md` (D2).

**4.5 Desglose por tarea/función (opcional, costes)**
- El tiempo imputado a cada tarea (que cuelga de una función de proyecto) puede empujarse
  a Rentman como `timeregistrationactivity` (`time_registration` + `project_function` +
  `duration`). Es la capa de coste/facturación de Rentman.
- **Propuesta a validar:** tarea de checkbiz ↔ `timeregistrationactivity`. Requiere que la
  tarea conozca su `project_function`. Probablemente fuera del MVP; se decide en Fase 0.

## 5. Persistencia (PostgreSQL, capa analytics)

- `rentman_employee_mapping` (ya existe): `crew ↔ employee`.
- **Nuevas tablas de mapping** por dominio: `project`, `projectcrew`, y estado de sync
  (`updateHash`, `updatedAt` por lado, `syncedAt`).
- `rentman_sync_log` (ya existe): bitácora de reconciliación.

## 6. Qué cambia respecto al esqueleto actual

| Esqueleto (actual) | To-be |
|---|---|
| Push de horas one-way | Sync **bidireccional** |
| Webhook público + secret | **Polling** desde `sync`, sin endpoint público |
| Escribe `timeregistrationactivity` | Escribe `timeregistration` (el fichaje) |
| Refs numéricas, duración cruda | Refs **string**, duración en **segundos** |
| Vive en `checkinbiz` (composition local) | Job de reconciliación en servicio **`sync`** |

El stub de webhook queda **aparcado** (no se borra aún, pero no es la vía).

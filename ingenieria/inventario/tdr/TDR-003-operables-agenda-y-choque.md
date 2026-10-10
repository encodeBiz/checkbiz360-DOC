# TDR-003 — Operables: agenda, detección de choque y tablero

**Fecha:** 2026-09-28 (revisado el mismo día)
**Estado:** Diseño aprobado
**Componente:** `encodebiz-api` — `inventory:3016` + `@encodebiz/shared` (calendar) + panel
**Decisión de referencia:** [ADR-006](../adr/ADR-006-operable-se-asigna-a-tareas-con-hora.md)

---

## 1. La agenda

Un ejemplar tiene, en una ventana de fechas, tres clases de ocupación:

1. **Reservas** — `unit_reservations` con `taskId`, intervalo y estado.
2. **Huecos de no disponibilidad** — el ejemplar en `status: "unavailable"` con
   `unavailableReason` y `unavailableUntil`. Avería, ITV, veterinario, descanso.
3. **Cierres heredados** — festivos de la entidad o de la sucursal de su almacén base, por la
   cascada de `resolveEffectiveCalendar`.

Las dos últimas se resuelven igual que la disponibilidad de una persona. **Eso** es lo que se
reutiliza de `calendar`; el tablero no (§4).

## 2. Detección de choque

Al reservar `[startAt, endAt)` para `unitId`:

```
conflicto ⇔ ∃ r ∈ reservas(unitId) :
             r.status ∈ {reserved, in_use}
             ∧ r.startAt < endAt
             ∧ r.endAt   > startAt
```

Solapamiento estricto, **con hora**: `[09:00, 11:00)` y `[11:00, 13:00)` del mismo martes no
chocan. La comprobación se hace **dentro de la transacción**, no antes: la lectura del
controlador puede haberse quedado vieja. Mismo criterio que las pausas de tareas.

**Respuesta al choque:** `409 inventory/unit_conflict` con la reserva que pisa en el cuerpo
—`{taskId, taskTitle, startAt, endAt, branchId}`— para que el panel diga con qué choca.

## 3. Estado de la reserva

| Disparador | Estado | Motivo |
|---|---|---|
| `POST /tasks/:id/units` | `reserved` | — |
| `task.status_changed → in_progress` | `in_use` | idempotente: puede llegar dos veces |
| `task.status_changed → completed` | `released` | `completed` |
| `task.status_changed → cancelled` | `released` | `cancelled` |
| `task.validated` | `released` (si no lo estaba) | `completed` |
| `task.rejected` (no desde `validated`) | `released` | `rejected` |
| `DELETE /tasks/:id/units/:unitId` | `released` | `manual` |

`ReleaseReason` es tipo propio: `"completed" | "cancelled" | "rejected" | "manual"`. No es
`TaskPauseEndReason`, aunque se parezca.

**Nada de esto se guarda en el ejemplar.** `ItemUnit.status` solo distingue `available`,
`unavailable` y `retired`; el «en uso» y el «dónde está» se derivan de la reserva activa.

> 2026-10-10: el «dónde está» **después** de liberar no se deduce de nada, y por eso pasa a
> llevar su propio rastro (`position`, con «¿dónde queda?» al liberar a mano y recepción en
> almacén sin bloquear la agenda). La agenda de este TDR no cambia.
> [ADR-008](../adr/ADR-008-liberar-no-es-devolver-la-posicion-del-ejemplar.md).

Al liberar se registra `usageEnd` si el artículo declara `usageUnit`, y se acumula la diferencia
en `ItemUnit.usageCounter`. Ese contador no se usa todavía —el mantenimiento preventivo es fase
posterior— pero **no se puede rellenar hacia atrás**.

## 4. El tablero — contrato y componente nuevos

La primera versión de este TDR decía que el tablero era el `AvailabilityBoard` de `shared` con
otras filas. **No lo es.** Aquel tiene una fila por grupo —`kind: "branch" | "unassigned"`,
unión cerrada— y una celda que es un contador (`{date, available, closed}`): un mapa de calor.
Lo que hace falta aquí es una **agenda**: una fila por ejemplar y una celda con qué tarea y en
qué sitio está.

`GET /board` devuelve un contrato propio:

```ts
interface UnitBoard {
  range: {from: string; to: string; timezone: string};
  rows: Array<{
    unitId: string; itemId: string; itemName: string; label?: string; warehouseId: string;
    days: Array<{
      date: string;
      slots: Array<{
        kind: "reservation" | "unavailable";
        from: string; to: string;                       // hora local
        taskId?: string; taskTitle?: string; site?: string;   // de la tarea y su workSite
        reason?: string;                                 // de unavailable
      }>;
    }>;
  }>;
}
```

`site` sale del `workSite.street` de la tarea, o del nombre de la sucursal si no tiene: el
«dónde está» se deriva, no se guarda.

**En el panel es un componente nuevo.** El de disponibilidad pinta contadores; este pinta
franjas con hora dentro de cada día. La Fase 3 lo lleva como partida propia.

## 5. Aplazado

**Tiempo mínimo entre asignaciones.** El choque por solapamiento no ve que dos obras distintas
están a cuarenta minutos en camión, ni que un animal necesita descansar entre jornadas. Es un
campo en el artículo o en el ejemplar y una holgura añadida al cálculo del §2. Fuera de v1
([06 §D6](../06_decisiones-abiertas.md)), pero el §2 se escribe de forma que aceptar una
holgura después sea cambiar una constante por un campo.

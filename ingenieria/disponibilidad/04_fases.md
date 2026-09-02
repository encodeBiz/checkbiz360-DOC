# 04 — Fases de implementación

## Fase 0 — Contrato y documentación ✔

Este documento. Fija el reparto (qué decide el backend y qué el front), el contrato de las dos
acciones y las reglas de cálculo.

**Entregable:** `ingenieria/disponibilidad/`.

---

## Fase 1 — `entityId` en los documentos `calendar/config`

Requisito de la query única del paso 5 del plan de lectura. Ver
[ADR-002](./adr/ADR-002-entityid-en-los-documentos-de-calendario.md).

1. **Camino de escritura.** `upsertCalendar` ya recibe `entityId` en el payload; pasa a
   persistirlo en el documento, en los tres scopes.
2. **Backfill.** Script de una pasada sobre `entities/*/…/calendar/config` que escribe el campo
   donde falte. Es idempotente y no toca ningún otro campo.
3. **Índice.** `collectionGroup('calendar')` con `entityId ==` y `type !=` necesita índice
   compuesto; se declara en `firestore.indexes.json`.

**Se puede saltar.** Si se prefiere no tocar datos todavía, el Admin SDK resuelve el paso 5 con
`getAll()` sobre las N referencias: sigue siendo N lecturas facturadas pero un solo round trip,
que es lo que quita el problema de latencia. La Fase 1 es optimización, no bloqueo — pero
entonces hay que dejarlo escrito para que no se olvide.

**Verificación:** un doc de cada scope tiene `entityId`; la query devuelve tantos documentos
como empleados con calendario propio.

---

## Fase 2 — Las dos acciones en `calendarHandler`

El grueso. Ver [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md).

1. `ResolveAvailabilityUseCase` — plan de lectura, resolución por (empleado, sucursal),
   evaluación día a día, agregación.
2. `ResolveAvailabilityDayUseCase` — el desglose, reusando la misma resolución.
3. Resolución del actor y alcance por nivel de responsabilidad. **Es trabajo nuevo:** el
   handler de calendario no discrimina hoy por nivel.
4. Límites: rango de 62 días, tope de plantilla, y **fallo duro si una lectura falla**.

**Verificación:** contra una entidad de dev con festivos de entidad, festivos de sucursal y
ausencias de empleado, la rejilla coincide con lo que devuelve `fetchEffectiveCalendar` empleado
a empleado. Es la prueba que importa: que la agregación y la resolución individual no se
contradigan.

---

## Fase 3 — Cutover del front

1. Sustituir el cuerpo de `fetchAvailabilityDataset` por la llamada a `action=availability`.
2. Borrar el cruce contra Firestore y la resolución duplicada de
   `src/lib/common/availability.ts`.
3. El desglose de un día pasa a pedirse a `action=availabilityDay` al pinchar la celda, en vez
   de calcularse en memoria.
4. Tratar de verdad `headcount_too_large`: pedir que se elija sucursal, no fallar en silencio.

Sin bandera ni convivencia: el tablero no está publicado. Detalle en
[05](./05_integracion-front.md).

**Verificación:** una sola petición por carga del tablero. Cambiar de mes dentro del rango pedido
no genera ninguna; salirse de él, una.

---

## Fase 4 *(futuro)* — Materialización y ausencias con rango

Sólo si la latencia lo pide, y con medida delante:

- **Rejilla materializada** en `entities/{e}/availability/{YYYY-MM}`, refrescada por triggers de
  calendario y de empleados. El contrato de la Fase 2 no cambia: cambia de dónde sale el número.
- **`Absence` con rango real** (`startDate`/`endDate`/`status`), que es la deuda §6.8 de
  [modulos/calendario.md](../../modulos/calendario.md). Simplifica la escritura, permite
  responder "por qué falta" con una sola entrada y quita las N llamadas `PATCH` por rango.

---

## Dependencias entre fases

```
Fase 0 ──▶ Fase 2 ──▶ Fase 3
             ▲
   Fase 1 ───┘  (opcional: acelera, no bloquea)

Fase 4 ── independiente, después de medir
```

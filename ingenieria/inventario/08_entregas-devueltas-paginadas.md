# 08 — Entregas devueltas, paginadas en la API

**Fecha:** 2026-10-09
**Estado:** pendiente en la API · el panel ya lo consume (rama `fix/empleado-material-devuelto` del front), con respaldo mientras la API no exista
**Servicio:** `encodebiz-api/services/inventory` (+ `packages/shared`, repositorio de entregas)
**Relacionado:** [07 — Operables: documentos y entregas](./07_operables-documentos-y-entregas.md) §4.3 y la tabla de contratos, [ADR-007](./adr/ADR-007-entrega-es-asignacion-con-acuse.md)

---

## Por qué

En la ficha del empleado, pestaña «Material», el panel enseña lo que la persona tiene ahora
(pendiente de confirmar o confirmado) y, aparte y plegado, lo que ya devolvió. Lo devuelto es
historia y no para de crecer: con años de EPIs y equipos son cientos de filas. El panel lo
enseña de cinco en cinco, del más reciente al más antiguo, con «Cargar más» — y eso tiene que
salir paginado de la API, no descargarse entero para cortarlo en el navegador.

## Lo que hay hoy

```
GET /employees/:employeeId/assignments?status=active|all
GET /me/assignments?status=active|all
```

- Router: `services/inventory/src/interfaces/http/unit/assignment.router.ts`.
- Caso de uso: `assignmentOperations.byEmployee(entityId, employeeId, onlyActive)` en
  `services/inventory/src/application/use-cases/assignments.ts`.
- Repositorio: `FirestoreAssignmentRepository.findByEmployee` en
  `packages/shared/src/checkbiz/inventory/repositories/FirestoreAssignmentRepository.ts` —
  un `where employeeId ==` (y `where status == "active"` si `onlyActive`), **sin límite**, y
  ordena en memoria (`byNewest`).
- Responde un **array** de `AssignmentView`.

Ojo con un detalle que condiciona la compatibilidad: el router hace
`onlyActive = status !== "all"`, así que **cualquier** valor distinto de `all` —también
`returned`— devuelve hoy las **activas**.

## Lo que se pide

Un valor nuevo de `status`, paginado. `active` y `all` no cambian (siguen devolviendo un
array, que es lo que usan la app y otras pantallas).

```
GET /employees/:employeeId/assignments?status=returned&limit=5&cursor=<opaco>
```

| Parámetro | Valor |
|---|---|
| `status` | `returned` |
| `limit` | entero, por defecto **5**, máximo **50** (fuera de rango → 400 `inventory/bad_request`) |
| `cursor` | opaco, el `nextCursor` de la página anterior; ausente = primera página |

Respuesta (objeto, **no** array):

```json
{
  "assignments": [ /* AssignmentView[], misma forma que hoy */ ],
  "nextCursor": "k:2026-10-08T09:12:44.000Z|abc123",
  "total": 37
}
```

- **Orden:** `returnedAt` descendente y, a igualdad, id descendente (estable entre páginas).
- **`nextCursor`:** `null` cuando no hay más. Formato libre, pero que sea opaco para el
  cliente; se sugiere el de `overview.ts` (`k:<returnedAt ISO>|<id>`, con
  `encodeURIComponent` si hace falta).
- **`total`:** las devueltas de ese empleado, en todas las páginas (lo que el panel pone en el
  título: «Devuelto (37)»). Con `count()` de Firestore sobre la misma consulta sin cursor.
- **Permisos:** los mismos que hoy (`canReserve` o el propio empleado).
- `AssignmentView` sin cambios: con los nombres resueltos como ahora (`view()`), solo para las
  filas de la página.

### Consulta en Firestore

```
unit_assignments (de la entidad)
  where employeeId == :employeeId
  where status == "returned"
  orderBy returnedAt desc
  orderBy __name__ desc
  startAfter(<returnedAt>, <id>)   // si hay cursor
  limit(limit + 1)                 // el sobrante dice si hay siguiente
```

Pide un **índice compuesto** `employeeId ASC, status ASC, returnedAt DESC` (y `__name__`
DESC) en `unit_assignments`. Los índices de Firestore no viven en `encodebiz-api`: se
declaran en `encodeBiz-SAAS/firestore.indexes.json` y se despliegan con `--project` explícito
(`dev-encodebiz` primero), como los de `items`.

Una entrega devuelta siempre tiene `returnedAt`: lo escribe la devolución en
`FirestoreAssignmentRepository` (`status: "returned", returnedAt: now`). Si hubiera alguna
antigua sin él, quedaría fuera del `orderBy`: comprobarlo en dev antes de dar el cambio por
bueno.

### `/me/assignments`

«Mi material» en la app usa el mismo caso de uso. Conviene aceptar ahí también
`status=returned&limit&cursor` con la misma respuesta, aunque la app no lo pida todavía: así
el contrato es uno.

## Compatibilidad con el panel

El panel ya llama con `status=returned&limit=5&cursor=…` y distingue por la **forma** de la
respuesta (`src/services/checkinbiz/inventory.service.ts`, `fetchEmployeeReturnedAssignments`):

- **Objeto** (`{ assignments, nextCursor, total }`) → API nueva: lo usa tal cual.
- **Array** → API de hoy (que, como se dijo, habrá devuelto las activas): lo descarta, pide
  `status=all` y pagina en el navegador con un desplazamiento como cursor.

No hace falta coordinar el despliegue: el panel funciona antes y después. Cuando la API
pagine, el respaldo deja de usarse solo y se puede quitar más adelante.

## Criterios de aceptación

1. `status=returned` devuelve el objeto paginado; sin `limit` trae 5.
2. Recorriendo `nextCursor` hasta `null` salen todas las devueltas una sola vez, en orden
   `returnedAt` descendente, y su número coincide con `total`.
3. `status=active` y `status=all` devuelven exactamente lo mismo que hoy.
4. `limit` 0, negativo, no numérico o > 50 → 400 `inventory/bad_request`.
5. Un empleado sin devoluciones → `{ assignments: [], nextCursor: null, total: 0 }`.
6. Índice creado en dev y comprobado con un empleado que tenga más de 5 devoluciones.
7. La tabla de contratos de [07](./07_operables-documentos-y-entregas.md) recoge
   `status=active|returned|all` y la forma de la respuesta paginada.

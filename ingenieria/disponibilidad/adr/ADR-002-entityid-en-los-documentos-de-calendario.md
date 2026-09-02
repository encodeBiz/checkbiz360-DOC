# ADR-002 — `entityId` dentro de los documentos de calendario

**Fecha:** 2026-09-02
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

Para agregar la disponibilidad hay que leer el documento `calendar/config` de cada empleado de
la entidad. Están repartidos uno por empleado:

```
entities/{entityId}/employees/{employeeId}/calendar/config
```

Firestore no sabe recorrer "todos los `calendar/config` que cuelgan de esta entidad" en una sola
consulta: `collectionGroup('calendar')` alcanza todas las subcolecciones `calendar` de **toda la
base**, y para acotarla a una entidad hace falta un campo por el que filtrar.

Los presets ya se leen así —`type == 'preset'` y `entityId == …`—, o sea que el patrón existe y
funciona; lo que no está garantizado es que los documentos `config` lleven `entityId` dentro. El
payload de `upsertCalendar` sí lo recibe, así que el dato está disponible en el momento de
escribir: la duda es si se persiste.

Tres caminos.

**Opción A — Una lectura por empleado.** Lo que hace el prototipo. N `getDoc`.

**Opción B — `getAll()` con las N referencias.** El Admin SDK lee N documentos por sus rutas en
un solo round trip. Sigue facturando N lecturas, pero se paga una espera, no N.

**Opción C — Denormalizar `entityId` y consultar en una query.** Una consulta paginada, con
índice.

---

## Decisión

Se adopta la **Opción C**, con la **Opción B como camino intermedio** mientras la denormalización
no esté hecha.

`upsertCalendar` persiste `entityId` en el documento en los tres scopes, un backfill idempotente
lo escribe donde falte, y el índice compuesto se declara en `firestore.indexes.json`. Hasta
entonces, el caso de uso resuelve con `getAll()`.

---

## Justificación

**La Opción A sólo tenía sentido en el cliente, y ya no hay cliente.** El SDK web no tiene
lectura por lotes; el Admin SDK sí. Mantener N `getDoc` en el servidor sería arrastrar una
limitación que allí no existe.

**La Opción B ya resuelve el problema urgente.** Lo que hacía inaceptable el prototipo era la
latencia —N idas y vueltas encadenadas—, no el número de lecturas facturadas. `getAll()` la
elimina de un golpe y no requiere tocar ni un dato. Por eso es el camino intermedio y por eso la
Fase 1 no bloquea a la Fase 2.

**Pero `getAll()` no escala en lecturas ni admite paginar.** Sigue siendo una lectura por
empleado, y hay que construir N referencias antes de saber cuáles tienen calendario propio —que
son pocas: la mayoría de la plantilla hereda y no tiene documento—. La query sólo devuelve los
que existen, que en la práctica es una fracción pequeña de N.

**La denormalización no inventa un patrón, lo completa.** El módulo ya consulta la subcolección
`calendar` por `collectionGroup` para los presets, filtrando por `entityId`. Que unos documentos
de esa misma subcolección lo lleven y otros no es la incoherencia; añadirlo es quitarla.

**El dato ya está en la mano al escribir.** `entityId` viaja en el payload de `upsertCalendar`.
No hay que deducirlo, ni buscarlo, ni arriesgarse a que se desincronice: es inmutable para el
documento — un calendario no cambia de entidad.

---

## Consecuencias

**Positivas:**

- Una consulta en lugar de N lecturas, y sólo devuelve a quien tiene calendario propio.
- Coherencia dentro de la subcolección `calendar`: todos sus documentos se pueden consultar por
  entidad, presets y configs.
- Habilita, sin más trabajo, cualquier futura pregunta del tipo "todos los calendarios de esta
  entidad" — auditoría, migraciones, informes.

**Negativas / Compromisos aceptados:**

- Un backfill sobre datos de clientes. Es idempotente y escribe un solo campo, pero es una
  escritura masiva y hay que ejecutarla con cuidado y con conteo previo.
- Un índice compuesto más que mantener.
- Redundancia deliberada: `entityId` ya está en la ruta del documento. Se acepta porque
  Firestore no sabe filtrar por prefijo de ruta en un `collectionGroup`, que es justamente el
  motivo por el que la denormalización existe como patrón.
- Mientras convivan documentos con y sin el campo, la query devuelve resultados incompletos. Por
  eso el corte es: **primero el backfill, después usar la query**; y hasta entonces, `getAll()`.

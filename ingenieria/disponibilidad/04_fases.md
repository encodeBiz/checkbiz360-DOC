# 04 — Fases de implementación

## Fase 0 — Contrato y documentación ✔

Fija el reparto, el contrato de las dos rutas y las reglas de cálculo, con las premisas
verificadas contra el repo y contra datos reales de dev.

**Entregable:** `ingenieria/disponibilidad/`.

---

## Fase 1 — Portar el módulo calendar al contenedor

Los cinco controladores de escritura —`upsertEntity/Branch/Employee`, `deleteCalendarItem` y
`createCalendarPreset`— pasan de la Cloud Function a `services/checkinbiz`. El
`FirestoreCalendarRepository` ya está allí con todos los métodos implementados, así que son
controladores finos, rutas y repuntar la variable del front.

**Va primero, y no al final, por una razón práctica:** mientras el panel escriba contra Firebase,
cualquier cambio de tipo hay que hacerlo en los dos repos. Con el porte hecho, el `source` y el
`paid` de la Fase 2 se tocan **sólo en `shared`**. Hacerlo al revés es hacer el mismo trabajo dos
veces.

Y de paso quita la segunda copia de `resolveEffectiveCalendar`, que es el problema que el
[ADR-001](./adr/ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md) señala y que ningún
otro paso resuelve.

**Verificación:** las escrituras del panel siguen funcionando contra el contenedor —alta y
borrado de festivo en los tres scopes, ausencia con rango, preset—, y `GET /calendar` devuelve lo
mismo que antes.

---

## Fase 2 — `source` y `paid` en el calendario

Dos cambios de tipo y cinco líneas de código. **Bloquean el cálculo**, y con la Fase 1 hecha se
aplican en un solo sitio: `@encodebiz/shared`.
Detalle en [06_tareas.md](./06_tareas.md).

1. **`source` en `concatHolidays`** (TAREA 2). Que cada festivo resuelto salga etiquetado con su
   nivel de origen. Sin esto no se puede calcular `closed`, que es la mitad del tablero.
2. **`paid?: boolean` en `Holiday`** (TAREA 1). Declarar el campo que el front ya manda y que hoy
   viaja por accidente. Bloquea al front.

**Verificación:** ejecutar la lectura de dev antes y después. Salida idéntica salvo el campo
nuevo. El calendario es núcleo duro —fichaje, edición de fichaje, planificador, worker de
activos, horas planificadas y la app— y el análisis de impacto consumidor a consumidor está en
[06_tareas.md](./06_tareas.md).

---

## Fase 3 — Las dos rutas

El grueso. Ver [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md).

1. `ResolveAvailabilityUseCase` en `shared` — plan de lectura de cinco round trips, resolución
   **una vez por par** (empleado, sucursal), evaluación de los días en memoria, agregación.
2. `ResolveAvailabilityDayUseCase` — el desglose, reusando la misma resolución.
3. Los dos controladores en el `calendarRouter` del contenedor.
4. Resolución del actor y alcance por nivel, subiendo `resolveActorByUid` de `tasks` a `shared`.
5. Límites, y **fallo duro si una lectura falla**.

**Verificación:** contra la entidad de dev, la rejilla tiene que coincidir con
`GET /calendar` empleado a empleado y día a día. Es la prueba que importa: que la agregación y la
resolución individual no se contradigan.

---

## Fase 4 — Cutover del front

1. Sustituir el cuerpo de `fetchAvailabilityDataset` por la llamada a `/availability`.
2. Registrar el handler nuevo en la allowlist del proxy y la variable de entorno.
3. Borrar el cruce contra Firestore y la resolución duplicada de `lib/common/availability.ts`.
4. El desglose pasa a pedirse a `/availability/day`, y a pintar dos listas de nombres.
5. Tratar de verdad `headcount_too_large`: pedir que se elija sucursal, no fallar en silencio.

Sin bandera ni convivencia: el tablero no está publicado. Detalle en
[05](./05_integracion-front.md).

**Verificación:** una sola petición por carga. Cambiar de mes dentro del rango pedido no genera
ninguna; salirse de él, una.

**Aquí el tablero ya está vivo.**

### Fase 4-bis — El desglose escribe

[ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md): arrastre y botón para dar de
alta y borrar ausencias desde el propio desglose, con `HolidayModal` y el modal de ausencias
propias. Sólo `reason: 'absence'` es reversible; los otros tres motivos se bloquean con
explicación.

Se puede empezar antes, sobre el cruce local del prototipo, porque la escritura reusa
`upsertCalendar` y `deleteCalendarItem`. Lo que no se puede adelantar es la parte que depende de
que la respuesta traiga `reason`, `reasonSource`, `absenceId` y `paid` — o sea, de las fases 2 y 3.

Tiene dos decisiones de producto abiertas en el propio ADR: si el arrastre inverso se bloquea o
se explica después, y qué nivel puede escribir.

Lo que sigue es rendimiento.

---

## Fase 5 — Snapshot del calendario resuelto

[ADR-005](./adr/ADR-005-snapshot-del-calendario-resuelto-en-postgres.md). Las dos tablas, la
marca de sucio síncrona en los upserts —que ya viven en el contenedor desde la Fase 1—, la
reconstrucción asíncrona e idempotente y el TTL del censo.

No cambia el contrato: cambia de dónde sale el número. Y con la tabla vacía el sistema se
comporta exactamente como la Fase 3, así que se puede desplegar sin ventana de riesgo.

**Beneficio que no es del tablero:** `BuildPlannedHours` puede dejar de resolver contra
`dim_calendars`, que hoy sólo se sincroniza a mano.

---

## Dependencias

```
Fase 0 ──▶ Fase 1 ──▶ Fase 2 ──▶ Fase 3 ──▶ Fase 4      (tablero vivo)
             porte     tipos      rutas     cutover
                                              │
                                              └──▶ Fase 5   (rendimiento)
```

Cadena recta. La Fase 1 va delante porque evita duplicar en dos repos todo lo que viene detrás, y
porque es prerrequisito de la invalidación del snapshot. Lo que no se debe hacer es la 5 antes de
la 3: cachear algo que no se ha verificado convierte un bug en un bug persistido.

---

## Backlog, sin fecha

- **`entityId` en los `calendar/config`** — [ADR-002](./adr/ADR-002-entityid-en-los-documentos-de-calendario.md).
  Confirmado que no está, pero `getAll()` resuelve y el snapshot lo hace casi irrelevante.
- **`Absence` con rango real.** El tipo, la API y la validación existen; el panel no los usa y el
  resolutor no lee `absences[]`. Latente, no activo.
- **Medir la plantilla multi-sucursal.** Decide si el sobreconteo del §2.2 es nota al pie o
  problema. Hace falta una entidad de dev con dos centros y alguien en los dos.
- **Alcance de `headcount` para un `supervisor`.** Hoy vería el tamaño de toda la empresa.

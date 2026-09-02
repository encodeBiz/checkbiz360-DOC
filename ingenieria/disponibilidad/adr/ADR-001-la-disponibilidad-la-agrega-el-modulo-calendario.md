# ADR-001 — La disponibilidad la agrega el módulo calendario, y se calcula una vez

**Fecha:** 2026-09-02 · **Revisado:** 2026-09-02 (premisas verificadas contra el repo)
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El tablero de disponibilidad necesita, para cada día y cada sucursal, cuánta gente está
disponible. Ese número no está guardado en ninguna parte: sale de cruzar el horario efectivo de
cada empleado con los festivos de su entidad y su sucursal, con sus propias ausencias y con el
estado de su ficha.

El cruce es inevitable. La decisión es **quién lo hace y cuántas veces**.

Existe un prototipo que lo hace en el navegador y que sirvió para descubrir lo que costaba: con
200 empleados son 200 lecturas sueltas a Firestore desde el cliente, en cada carga de la
pestaña, de cada usuario. Los números están en [01_as-is.md](../01_as-is.md).

### Dónde vive hoy el módulo calendario

La primera versión de este ADR daba por hecho que el calendario era una Cloud Function. **No lo
es, o no del todo.** El estado real, comprobado:

- El **contenedor** `services/checkinbiz` sirve `GET /api/v1/checkinbiz/calendar`, montado en
  `calendar.router.ts` detrás de `requireFirebaseAuth`.
- La regla de herencia vive en **`@encodebiz/shared`**
  (`packages/shared/src/calendar/resolveEffectiveCalendar.usecase.ts`), y de ahí la consumen
  también los fichajes y `analytics`.
- En **Firebase** se quedaron las escrituras: `upsertEntity/Branch/Employee`, `delete` y
  `savePreset`, más una copia entera del caso de uso en
  `encodeBiz-SAAS/functions/src/services-saas/checkinbiz/application/calendar/`.

Esto cambia dos de los argumentos originales y hay que decirlo: la regla **ya está duplicada**
(shared y SAAS), y el "coste operativo cero" de reusar el handler de Firebase sólo valía
mientras el front apuntara allí.

Se valoraron cuatro caminos.

**Opción A — El front cruza los datos.** Lo que hay hoy en el prototipo.

**Opción B — El front pide el calendario efectivo empleado a empleado.** `GET /calendar` ya
devuelve el calendario resuelto de un empleado; bastaría con llamarlo N veces.

**Opción C — El módulo `calendar` agrega y devuelve la rejilla.** Dos lecturas nuevas sobre el
módulo que ya sirve el calendario efectivo.

**Opción D — Un servicio o módulo de disponibilidad propio.** Siguiendo el precedente de
`tasks`.

---

## Decisión

Se elige la **Opción C**, y el módulo `calendar` es **el del contenedor**.

`ResolveAvailabilityUseCase` y `ResolveAvailabilityDayUseCase` viven en `@encodebiz/shared`, al
lado de la resolución que reusan, y se exponen como dos rutas de solo lectura en el
`calendarRouter` de `services/checkinbiz`. El front deja de cruzar: pide la rejilla y la pinta.
Los umbrales de color se quedan en el cliente, porque son lectura visual y no dato.

---

## Justificación

**La regla de herencia debe existir una vez, y la que vale es la de `shared`.**
`ResolveEffectiveCalendarUseCase` resuelve entidad → sucursal → empleado con sus
`overridesDisabled` y su concatenación de festivos, y ya la comparten el fichaje, el calendario
de la app y las horas planificadas. Cualquier opción que no la reuse la duplica — y ya se ha
duplicado bastante: la copia de SAAS, más `BranchCalendarDetail` y `EmployeeCalendarDetail` en
el front, más el prototipo. Cuando la precedencia cambie, las copias no darán error: darán
números distintos.

**Y por eso no puede ir en el `calendarHandler` de Firebase.** Escribir la agregación allí
significaría construirla sobre la copia que está en retirada: una cuarta implementación de la
misma regla, en el repo del que el dominio se está yendo. Cuesta una variable de entorno nueva
en Vercel ponerla en el contenedor, y es un precio ridículo comparado con eso.

**El coste es lineal con la plantilla; la única decisión disponible es quién lo paga.** No hay
forma de contar sin mirar a todo el mundo. Lo que sí se puede decidir es si esa pasada la da
una vez el servidor o la da el navegador de cada persona que abre la pestaña, cada vez que la
abre. La Opción A y la Opción B eligen lo segundo: la A con N lecturas de Firestore, la B con N
peticiones HTTP que además atraviesan el proxy de Next y verifican el token una por una. La B
es peor que la A en todo salvo en corrección.

**Cruzar desde el cliente obliga a abrir las reglas de Firestore.** Para que el navegador pueda
leer el calendario de todos los empleados, la regla tiene que permitir a cualquier usuario del
panel leer el calendario de cualquiera. Es una ampliación de permisos hecha para pintar un
número. Y no se detectaría a tiempo: las reglas de dev están abiertas desde diciembre de 2025,
así que el problema aparecería directamente en producción.

**Y ahí el fallo no es un error, es una mentira.** En el prototipo, una lectura denegada se
interpreta como "este empleado no tiene ausencias", que en la cascada significa **disponible**.
Un tablero de cobertura que se equivoca callando —y siempre hacia arriba— es peor que uno que
no carga: alguien planifica un turno con gente que no está. No es un descuido corregible del
prototipo, es la consecuencia natural de repartir N lecturas independientes por una red poco
fiable: con N intentos, "casi todas han ido bien" es el caso normal, y hay que decidir qué se
hace con eso. En el servidor la respuesta es fácil: si una lectura falla, la petición falla
entera.

**La disponibilidad no tiene datos propios.** Es una lectura derivada, no una entidad. No hay
nada que guardar, ni ciclo de vida que gobernar, ni escrituras que ordenar. Un servicio nuevo
—Opción D— tendría que empezar por leer las tres colecciones de calendario y por reimplementar
la resolución, que es exactamente lo que se quiere evitar. El precedente de `tasks` no aplica:
allí se movió un módulo con dominio propio, catorce rutas y escrituras; aquí se añaden dos
lecturas sobre un dominio que ya está en su casa.

**Y deja abierta la única optimización que puede hacer falta.** Si la pasada lineal no llega, la
resolución se materializa en Postgres sin tocar el contrato ni el front — ver
[ADR-005](./ADR-005-snapshot-del-calendario-resuelto-en-postgres.md). Esa puerta sólo existe si
el número lo produce el servidor.

---

## Consecuencias

**Positivas:**

- Una petición por carga del tablero en lugar de N+B+2, y la espera deja de crecer con la
  plantilla.
- Las reglas de Firestore se quedan como están: el cliente no lee calendarios ajenos.
- Una sola implementación de la herencia, la de `shared`. El tablero no puede divergir del
  detalle de empleado porque ambos preguntan a lo mismo.
- Los fallos se ven. Sin rejilla parcial y sin números inventados hacia arriba.
- El contrato admite materializar la resolución después sin que el front se entere.
- El prototipo no se tira: la vista se conserva entera.

**Negativas / Compromisos aceptados:**

- **Una variable de entorno nueva en Vercel** y su despliegue, que es justo lo que la primera
  versión de este ADR quería evitar. Se acepta: la alternativa era escribir código nuevo en el
  repo que se está vaciando.
- **El contenedor no está donde está Firestore.** Corre en OVH (141.95.47.135) y Firestore está
  en GCP, así que cada ida y vuelta cruza nubes. No cambia la decisión —una petición del
  servidor sigue siendo mucho mejor que N del navegador— pero obliga a que el plan de lectura
  minimice **round trips**, no sólo lecturas facturadas. Ver [TDR-001](../tdr/TDR-001-calculo-de-disponibilidad.md) §1.
- El módulo `calendar` necesita, por primera vez, distinguir por nivel de responsabilidad: la
  disponibilidad devuelve nombres de toda la plantilla y un `worker` no debe verla. Es
  adaptación del resolutor de actor de `tasks`, no trabajo desde cero.

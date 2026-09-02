# ADR-001 — La disponibilidad la agrega el módulo calendario, y se calcula una vez

**Fecha:** 2026-09-02
**Estado:** Propuesto
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

Se valoraron cuatro caminos.

**Opción A — El front cruza los datos.** Lo que hay hoy. El navegador lee la configuración de
la entidad, de cada sucursal y de cada empleado, y agrega.

**Opción B — El front pide el calendario efectivo empleado a empleado.** `GET /calendar` ya
devuelve el calendario resuelto de un empleado; bastaría con llamarlo N veces.

**Opción C — El módulo `calendar` agrega y devuelve la rejilla.** Dos acciones nuevas de solo
lectura sobre el handler que ya existe.

**Opción D — Un servicio o módulo de disponibilidad propio.** Siguiendo el precedente de
`tasks`, un sitio nuevo dedicado a esto.

---

## Decisión

Se elige la **Opción C**.

El módulo `calendar` gana `action=availability` y `action=availabilityDay` en el handler que ya
sirve el calendario efectivo. El front deja de cruzar: pide la rejilla y la pinta. Los umbrales
de color se quedan en el cliente, porque son lectura visual y no dato.

---

## Justificación

**La regla de herencia ya existe una vez, y sólo debe existir una vez.**
`ResolveEffectiveCalendarUseCase` resuelve entidad → sucursal → empleado, con sus
`overridesDisabled` y su concatenación de festivos. Cualquier opción que no la reuse la duplica,
y ya se ha duplicado bastante: `BranchCalendarDetail` y `EmployeeCalendarDetail` la
reimplementan cada uno por su cuenta en el front, y el prototipo la reimplementó una tercera
vez. Cuando la precedencia cambie, las copias no darán error: darán números distintos. Eso
descarta la Opción A por sí solo.

**El coste es lineal con la plantilla; la única decisión disponible es quién lo paga.** No hay
forma de contar sin mirar a todo el mundo. Lo que sí se puede decidir es si esa pasada la da
una vez el servidor, dentro del mismo datacenter que Firestore, o la da el navegador de cada
persona que abre la pestaña, cada vez que la abre. La Opción A y la Opción B eligen lo segundo:
la A con N lecturas de Firestore, la B con N peticiones HTTP que además atraviesan el proxy de
Next y verifican el token una por una. La B es peor que la A en todo salvo en corrección.

**Cruzar desde el cliente obliga a abrir las reglas de Firestore.** Para que el navegador pueda
leer el calendario de todos los empleados, la regla tiene que permitir a cualquier usuario del
panel leer el calendario de cualquier empleado. Es una ampliación de permisos hecha para pintar
un número. Y no se detectaría a tiempo: las reglas de dev están abiertas desde diciembre de
2025, así que el problema aparecería directamente en producción.

**Y ahí el fallo no es un error, es una mentira.** En el prototipo, una lectura denegada se
interpreta como "este empleado no tiene ausencias", que en la cascada significa **disponible**.
Un tablero de cobertura que se equivoca callando —y siempre hacia arriba— es peor que uno que no
carga: alguien planifica un turno con gente que no está. Esto no es un descuido corregible del
prototipo, es la consecuencia natural de repartir N lecturas independientes por una red poco
fiable: con N intentos, "casi todas han ido bien" es el caso normal, y hay que decidir qué se
hace con eso. En el servidor la respuesta es fácil y es la correcta: si una lectura falla, la
petición falla entera.

**La disponibilidad no tiene datos propios.** Es una lectura derivada, no una entidad. No hay
nada que guardar, ni ciclo de vida que gobernar, ni escrituras que ordenar. Un servicio nuevo
—Opción D— tendría que empezar por leer las tres colecciones de calendario y por reimplementar
la resolución, que es exactamente lo que se quiere evitar. El precedente de `tasks` no aplica:
allí se movió un módulo con dominio propio, catorce rutas y escrituras; aquí se añaden dos
lecturas sobre un dominio que ya está en su casa.

**Reusar el handler que ya existe tiene un coste operativo de cero.** El front ya llega a
`calendarHandler` por el proxy de Next, que reenvía la query string tal cual. No hay variable de
entorno nueva, ni entrada nueva en la allowlist del proxy, ni redeploy en Vercel — que es donde
viven las variables y donde cada cambio cuesta un despliegue. Una acción nueva sobre un handler
registrado es, literalmente, desplegar la función y nada más.

**Y deja abierta la única optimización que puede hacer falta.** Si algún día la pasada lineal no
llega, la rejilla se materializa por mes y se refresca con triggers, sin tocar el contrato ni el
front. Esa puerta sólo existe si el número lo produce el servidor.

---

## Consecuencias

**Positivas:**

- Una petición por carga del tablero en lugar de N+B+2, y la espera deja de crecer con la
  plantilla.
- Las reglas de Firestore se quedan como están: el cliente no lee calendarios ajenos.
- Una sola implementación de la herencia, la que ya estaba. El tablero no puede divergir del
  detalle de empleado porque ambos preguntan a lo mismo.
- Los fallos se ven. Sin rejilla parcial y sin números inventados hacia arriba.
- El contrato admite materializar la rejilla después sin que el front se entere.
- El prototipo no se tira: la vista se conserva entera y sus reglas puras pasan a ser la
  especificación del backend ([TDR-001](../tdr/TDR-001-calculo-de-disponibilidad.md)).

**Negativas / Compromisos aceptados:**

- `calendarHandler` gana su endpoint más pesado: una pasada lineal sobre la plantilla dentro de
  una Cloud Function, con su arranque en frío. Es tráfico de back office y de baja frecuencia
  —alguien abre un tablero—, no tráfico de app, así que se acepta.
- El módulo `calendar` necesita, por primera vez, distinguir por nivel de responsabilidad: la
  disponibilidad devuelve nombres de toda la plantilla y un `worker` no debe verla. Es trabajo
  nuevo, no un port.
- Aparece un tope explícito de plantilla: por encima de él hay que elegir sucursal. Es preferible
  a truncar la respuesta en silencio, pero es una limitación visible en el producto.
- El front pierde la capacidad de recalcular al vuelo. Filtrar por sucursal y buscar un empleado
  siguen siendo locales, pero cambiar de periodo fuera del rango pedido cuesta una llamada.
- Queda una duplicación menor y deliberada: los umbrales de color viven en el cliente. Es
  presentación, y subirlos a la API convertiría una decisión de diseño en contrato.

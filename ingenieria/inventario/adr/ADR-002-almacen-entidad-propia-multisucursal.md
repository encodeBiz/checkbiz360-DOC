# ADR-002 — El almacén es entidad propia y sirve a varias sucursales

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

La plataforma es multientidad y multisucursal de nacimiento, así que la primera intuición fue
colgar las existencias de la sucursal: cada centro con su inventario, y un «inventario general»
para lo que no es de nadie.

El caso que la rompe es real y lo puso el cliente tipo: una empresa de limpieza con **Madrid
Norte, Madrid Sur y Barcelona Centro**, donde las dos de Madrid **comparten el mismo almacén**.

Si las existencias cuelgan de la sucursal, esa estantería tiene dos números. Uno repone y
apunta en Norte, otro gasta y descuenta en Sur, y a las dos semanas ninguno de los dos se
parece a lo que hay. No es un problema de sincronización: es que el modelo está diciendo que
hay dos estanterías donde hay una.

También se valoró copiar el modelo de Rentman, que maneja **almacenes distintos** como entidad
central. Rentman alquila material: sus almacenes son naves y son su negocio.

## Decisión

El **almacén es una entidad propia** (`warehouses`), y su relación con la sucursal es de muchos
a muchos: un almacén sirve a una, a varias o a todas.

**La sucursal no tiene inventario: tiene acceso a almacenes.**

## Justificación

**Una estantería, un número.** Es la única forma de que el que repone y el que gasta miren lo
mismo.

**No se pierde la vista por sucursal.** Que es lo que se temía al soltar la sucursal como eje.
La pantalla filtra por sucursal resolviendo por la relación, y también por almacén, que es la
vista del que repone. Dos ejes sobre los mismos datos.

**No se pierde el coste por centro.** El almacén dice **dónde está** el material; la tarea dice
**quién lo gastó**. El consumo se imputa a la tarea y, por ella, a su sucursal y a su empleado.
Compartir la estantería no mezcla las cuentas.

**Y desbloquea lo que más vale.** Si el almacén de Madrid sirve a Norte y a Sur, la fregadora
que vive ahí se cuadra entre tareas de las dos zonas y el tablero cruza sucursales. Con el
almacén atado a un solo centro, ese problema —que es el que duele en una empresa de limpieza—
ni siquiera se ve.

**Del modelo de Rentman se copia la idea, no la entidad.** Allí el almacén es una nave y es el
negocio. Aquí la nave ya tiene nombre y a veces se llama sucursal — pero no siempre, y ese «no
siempre» es justo el caso de Madrid.

## Consecuencias

- `warehouses` con `scope: "entity" | "branches"` y `branchIds: string[]`. Array y no colección
  de relación porque hoy no lleva datos propios y `array-contains` resuelve la consulta; es lo
  mismo que hace el empleado con su `branchId[]`. Si algún día la relación gana atributos, se
  saca a registro aparte siguiendo `EmployeeResponsibility`.
- El «almacén general» existe como `scope: "entity"`: un almacén que sirve a todas las
  sucursales, no un cajón por defecto. Y es un campo **explícito**, no «array vacío = todos»:
  quitar la última sucursal de un almacén no puede convertirlo en global sin que nadie lo pida.
- La existencia se indexa por **artículo + almacén**, nunca por sucursal.

## Sin «almacén principal»

Se propuso que cada sucursal marcase un almacén por defecto del que descontar sin preguntar.
**Se descarta.**

Cuando una sucursal tiene acceso a varios almacenes, el operario o el responsable **elige de
cuál se abasteció**. No somos adivinos: un valor preseleccionado se acepta por inercia y
acabaría firmando consumos contra el almacén equivocado, que es peor que preguntar.

La fricción solo aparece donde la ambigüedad es real. Con un solo almacén no se pregunta nada
—un desplegable de una opción es ruido— y el servidor lo resuelve. Con dos o más, campo
obligatorio y **sin preseleccionar**.

El movimiento **siempre** guarda el almacén, se haya preguntado o no. Lo que cambia es si lo
escribió una persona o se dedujo. Si no, el día que una sucursal pasa de un almacén a dos, el
histórico anterior no dice de dónde salió nada.

## Addendum 2026-09-29 — sin «almacén de toda la empresa»

Jose, probando el panel: la opción «a toda la empresa» chocaba con lo que tenía pensado, que
el almacén general viva **en la sucursal principal**. Decisión: **todo almacén cuelga de una o
varias sucursales**; `scope: "entity"` se retira del alta y de la edición, y `branchIds` pasa
a ser obligatorio (al menos una). Lo multisucursal se conserva tal cual: el mismo almacén
puede servir a varias. Los documentos anteriores con `scope: "entity"` siguen sirviendo a
todas hasta que alguien los edite, momento en que pasan a `"branches"` y ya no vuelven.

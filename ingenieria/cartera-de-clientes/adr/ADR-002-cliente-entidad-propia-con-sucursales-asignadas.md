# ADR-002 — El cliente es entidad propia y se le asignan sucursales, como al almacén

**Fecha:** 2026-10-29
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

La primera versión del diseño colgaba el cliente **de** la sucursal: cada sucursal con sus
clientes, y la comunidad de vecinos «dueña» de sus edificios-sucursal. Y añadía un nivel
«proyecto» entre el cliente y la tarea para la constructora.

Jose lo giró con el caso de Neteges: 134 sucursales dadas de alta que **son clientes**, una
empresa que en realidad tiene **una** sucursal, y un cuadrante que no se puede organizar
porque el modelo les obligó a llamar sucursal a lo que no lo era. Lo que les propuso es una
sola sucursal, horario por tareas y la tarea vinculada a un lugar. Lo que falta es el
cliente, y el cliente tiene que ser **una cosa propia a la que se le dice qué sucursales
tiene**, «como los almacenes en inventario».

## Decisión

El **cliente es una entidad propia** (`customers`), y su relación con la sucursal es de
muchos a muchos **desde el cliente**: al cliente se le asignan las sucursales que necesita,
igual que al almacén se le dicen las sucursales a las que sirve
([inventario ADR-002](../../inventario/adr/ADR-002-almacen-entidad-propia-multisucursal.md)).

**La sucursal no tiene clientes: tiene clientes asignados.** No cambia nada por tenerlos.

No hay nivel «proyecto». Lo que la constructora llama proyecto ya existe y se llama sucursal
(es donde fichan); lo que la agencia llama evento es un lugar del cliente con fechas.

## Justificación

**Un cliente, varias sucursales; una sucursal, varios clientes.** Constructora X tiene tres
obras, cada una su sucursal: un cliente, tres sucursales. Centro Carabanchel atiende a
cuarenta clientas: una sucursal, cuarenta clientes. Neteges, una sucursal, 134 clientes. Solo
la relación de muchos a muchos vale para los tres, y la dirección «desde el cliente» es la
que se entiende en la pantalla: abres a Juana y dices a qué centro pertenece.

**La sucursal sigue siendo lo que es.** Empleados, fichaje, geocerca, horario, tareas. Si el
cliente colgara de la sucursal, borrar o fusionar sucursales arrastraría clientes; así, el
cliente es suyo y la sucursal solo lo tiene asignado.

**El selector de la tarea sale solo.** Al crear una tarea en una sucursal, los clientes
posibles son los que la tienen asignada. Con uno, se pone solo. Con varios, se elige. Con
ninguno, la tarea de siempre. Es la misma regla que el almacén en el consumo.

**Y Neteges tiene camino de salida.** Cada sucursal falsa se convierte en un cliente con un
lugar copiado de su dirección y su geocerca, asignado a la sucursal real. Es un script, no
una migración de modelo.

## Consecuencias

- `Customer` con `scope: "entity" | "branches"` y `branchIds: string[]`, explícitos como en
  el almacén: `entity` es «todas» y se dice; quitar la última sucursal no convierte al
  cliente en global.
- `dedicatedBranchIds ⊆ branchIds`: las sucursales que **son** del cliente (la obra). Es lo
  que hace que las jornadas fichadas allí sean suyas. Ver [ADR-003](./ADR-003-la-tarea-lleva-el-cliente-y-las-horas-se-imputan-por-tarea-o-por-sucursal-dedicada.md).
- El **lugar** es del cliente (`sites`), con la forma del `workSite` de la tarea, o apuntando
  a una sucursal cuando el lugar es la sucursal. Puede llevar fechas: eso es la obra y el
  evento, sin nivel nuevo ([06 §D7](../06_decisiones-abiertas.md)).
- Array y no colección de relación, por la misma razón que el almacén: hoy la relación no
  lleva datos salvo el bit de dedicada, y `array-contains` resuelve la consulta del selector.
  Si gana atributos, se saca a registro aparte.

## Sin «cliente por defecto» en la sucursal

Se propuso que una sucursal con varios clientes marcase uno por defecto. **Se descarta**, con
el mismo argumento que el almacén principal: un valor preseleccionado se acepta por inercia y
acabaría imputando horas al cliente equivocado. Con uno no se pregunta; con varios, campo
obligatorio sin preseleccionar; la tarea **siempre** guarda el cliente, se haya preguntado o
no.

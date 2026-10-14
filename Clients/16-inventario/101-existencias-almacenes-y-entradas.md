# Existencias, almacenes y entradas

Esta guía explica cómo se pone en marcha el inventario y cómo se controla lo que hay. Requiere el complemento de inventario contratado o en prueba.

---

## 1. Crear los almacenes

Un almacén es el sitio de donde sale el material: un cuarto de limpieza, una nave, una furgoneta. **Todo almacén sirve al menos a una sucursal**, y una sucursal puede tener varios almacenes.

1. Vaya a **Inventario → Almacenes**.
2. Pulse **Nuevo almacén**, póngale nombre y elija las sucursales a las que sirve.

Cuando una tarea de esa sucursal necesite material, la plataforma ofrecerá solo sus almacenes. Si solo tiene uno, lo elige sola.

Cada almacén tiene su **ficha**, con un resumen —artículos, ejemplares libres, existencias bajo mínimo y discrepancias—, lo que contiene y sus movimientos recientes.

---

## 2. Registrar la primera entrada

El material entra siempre por **Nueva entrada**, en **Inventario → Existencias**. No hay que crear el artículo antes:

1. Pulse **Nueva entrada**.
2. En **Artículo**, escriba para buscarlo. Si no existe, elija **＋ Nuevo artículo** y rellene su ficha: tipo, nombre y unidad de medida (o unidad de uso, si es un operable), referencia, coste unitario y categoría.
3. Elija el **almacén**.
4. Si es un **consumible**, indique la **cantidad**. Si es un **operable**, la entrada es un **ejemplar nuevo**: póngale el identificador de su etiqueta (matrícula, número de serie) y, si quiere, un nombre corto («la fregadora roja»).
5. Pulse **Registrar entrada**.

> **Consejo:** el buscador empieza a buscar a partir de la tercera letra, igual que el resto de buscadores del backoffice.

Si tiene muchos artículos que dar de alta, cárguelos de una vez desde la ficha del almacén con **Importar**: se explica en [Importar material desde una plantilla](./105-importar-material-desde-una-plantilla.md).

---

## 3. Existencias: lo que hay, artículo a artículo

**Existencias** es el centro de mando del inventario. Cada fila es un artículo en un almacén:

- Un **consumible** muestra lo disponible, lo que hay en almacén, lo comprometido por tareas y su mínimo.
- Un **operable** muestra cuántos ejemplares están libres ahora, cuántos ocupados y cuántos no disponibles. Si alguno tiene sus papeles caducados, la fila dice cuántos están **fuera de regla** o **por revisar**.

La columna **Estado** resume si hay que hacer algo:

| Estado | Significa |
|---|---|
| **Correcto** | Un consumible sin avisos: ni bajo mínimo ni con discrepancia. |
| **Disponible** | Un operable con algún ejemplar libre ahora. |
| **Bajo mínimo** | Hay menos que el mínimo de aviso fijado para ese almacén. |
| **Discrepancia** | El saldo quedó en negativo: salió más de lo apuntado. Hace falta un recuento. |
| **Todos ocupados** | Ningún ejemplar libre en este momento. |
| **Sin ejemplares** | Operable dado de alta sin ningún ejemplar todavía. |

Se puede filtrar por texto, tipo, almacén y estado. Si hay discrepancias, un aviso arriba permite verlas con un clic. El estado **Fuera de base** deja solo los equipos libres que no están en su almacén: lo que hay que ir a recoger (ver [Dónde está cada equipo](./106-donde-esta-cada-equipo.md)).

---

## 4. Acciones sobre el material

Desde cada fila, o desde la ficha del artículo:

| Acción | Para qué |
|---|---|
| **Entrada** | Material que llega: una compra, una devolución de proveedor, un ejemplar nuevo. |
| **Traspaso** | Mover cantidad de un almacén a otro o cambiar un ejemplar de almacén base. |
| **Recuento** | Fijar lo que hay de verdad después de contar, con un motivo. Solo consumibles. |
| **Mínimo** | Fijar el nivel por debajo del cual se avisa a los responsables. Solo consumibles. |
| **Editar** | Cambiar los datos de la ficha. El tipo no se cambia. |
| **Dar salida** | Entregar material del almacén a una tarea, a una persona o a una sucursal. Es opcional: si nadie la da, la apunta el consumo. Ver [Material sin tareas](./107-material-sin-tareas-personas-y-centros.md). |
| **Entregar** | Dar un ejemplar a una persona, que lo confirma desde su móvil. Ver [Equipos: documentos, revisiones y entregas](./104-equipos-documentos-revisiones-y-entregas.md). |
| **Archivar** | Dejar de ofrecer un artículo. Si tiene historia, se conserva. |

---

## 5. La ficha del artículo

Todos los artículos tienen la misma ficha: sus datos, lo que hay en cada almacén y su historia.

- En un **consumible**: existencias por almacén y movimientos de los últimos 30 días, con descarga del año en CSV.
- En un **operable**: cuántos ejemplares están libres; cada ejemplar con su estado (libre, reservado, en uso, entregado, no disponible o retirado) , su uso actual y **dónde está**; un **calendario** donde cada reserva es una barra con su horario, en tramos de 7, 14 o 30 días; y sus **documentos** (ITV, seguro, revisiones, manual), con la marca de si cada ejemplar está en regla.

---

## Quién puede hacer qué

| Rol | Puede |
|---|---|
| Worker | Ver el material de los almacenes de sus sucursales, declarar el consumo en sus tareas y confirmar los equipos que se le entregan |
| Supervisor | Además, reservar material y ejemplares a tareas |
| Manager, Owner | Además, crear artículos, almacenes y ejemplares, y registrar entradas, recuentos y traspasos |

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Qué es el inventario](./100-que-es-el-inventario.md) | Qué problemas resuelve y cómo se contrata |
| [Material en las tareas](./102-material-en-las-tareas.md) | Cómo se asigna y se sigue el material de cada tarea |
| [Importar material desde una plantilla](./105-importar-material-desde-una-plantilla.md) | Cargar de una vez todo lo que hay en un almacén |
| [Dónde está cada equipo](./106-donde-esta-cada-equipo.md) | Equipos libres fuera del almacén y cómo se reciben |

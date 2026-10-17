# Informe de consumo y movimientos

El inventario responde a dos preguntas de gestión: **dónde se va el material** y **cuánto cuesta**. Para eso tiene tres salidas.

---

## Informe de consumo

Se abre desde **Inventario → Existencias → Más acciones → Informe**.

1. Elija el **periodo**.
2. Elija cómo **agrupar**: por artículo, tarea, empleado, sucursal o almacén.
3. Si lo necesita, filtre por almacén, artículo, sucursal o empleado.
4. Pulse **Generar**.

Cada línea muestra la cantidad consumida, el coste (valorado al coste unitario de la ficha del artículo), el número de apuntes y la fecha del primero y del último. Se puede **exportar a CSV**.

Sirve para saber qué cliente o qué centro consume más, qué persona gasta por encima de lo normal o qué almacén se vacía antes.

---

## Libro de movimientos

Todo lo que pasa en el inventario queda apuntado: entradas, reservas, salidas, consumos, devoluciones, recuentos y traspasos, con quién lo registró, a nombre de quién y en qué tarea.

Se descarga en **Excel**, con todo el historial desde el primer día:

| Desde | Botón | Qué trae |
|---|---|---|
| La ficha de un almacén | **Descargar historial** | Ese almacén |
| El listado de almacenes | **Descargar historial de todos** | Un resumen general y una hoja por almacén |
| La ficha de un artículo | **Descargar historial** | Ese artículo, en cada almacén donde ha estado |
| El informe de consumo | **Historial del periodo (Excel)** | El periodo, el almacén y el artículo elegidos |

Cada almacén trae su **resumen por artículo** (entradas, traspasos, salidas, devoluciones, ajustes, lo gastado, las existencias y su valor), los **movimientos** en orden con las existencias después de cada uno y a qué fue cada salida (una tarea, una persona o una sucursal, por su nombre), sus **equipos** y **dónde ha estado** cada uno. Si las existencias rehechas desde el historial no coinciden con las de ahora, la fila dice **Revisar**. Es el registro al que recurrir cuando un recuento no cuadra.

---

## El material en el informe de tareas

Con el inventario contratado, el **informe de tareas** en Excel incluye el material de cada tarea, su coste y lo que quedó sin cuadrar. Se explica en [Informes de tareas](../06-tareas/48-informes-de-tareas.md#material-de-cada-tarea).

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Qué es el inventario](./100-que-es-el-inventario.md) | Qué problemas resuelve |
| [Tipos de informe](../11-informes-y-exportacion/76-tipos-de-informe.md) | Todos los informes de la plataforma |

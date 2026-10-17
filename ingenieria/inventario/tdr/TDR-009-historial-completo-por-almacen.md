# TDR-009 — El historial completo de un almacén, en Excel

**Fecha:** 2026-10-17
**Estado:** Implementado el 2026-10-17: API y panel en develop y staging
**Componente:** `inventory:3016` (genera el fichero), panel (ficha del almacén)
**Se apoya en:** [ADR-005](../adr/ADR-005-instante-firestore-historico-postgres.md) («el libro es un informe más»), [TDR-004](./TDR-004-espejo-postgres-e-informes.md), [ADR-008](../adr/ADR-008-liberar-no-es-devolver-la-posicion-del-ejemplar.md), [ADR-009](../adr/ADR-009-el-material-sale-hacia-una-tarea-una-persona-o-una-sucursal.md)

---

## 1. Por qué

> Jose, 2026-10-17, sobre la descarga de movimientos: «Este reporte es un destrozo, los ids no
> aportan nada y no dice nada». Y después: «Hay que crear el informe completo desde el
> historial de Postgres, un xls por almacén donde refleje todo el histórico de cada uno, y eso
> es lo más importante de todo».

El libro se registra completo desde la Fase 2: cada gesto es un apunte, en la misma transacción
que mueve las existencias, y se espeja a Postgres. Lo que nunca se diseñó fue **leerlo**. La
descarga CSV del informe de consumo (2026-10-07) vuelca apuntes sueltos: pone los nombres en el
navegador uno a uno y escribe el id cuando falla, mezcla reservas con salidas, no da saldo ni
resumen y no dice a qué fue cada salida.

## 2. Decisión

Un fichero **por almacén** con **todo su histórico**, desde el primer apunte hasta el momento de
descargarlo. Lo genera `inventory` desde Postgres y pone **todos los nombres en el servidor**
(dimensiones de Postgres; Firestore solo para lo que no esté espejado, como la cuenta de un owner
sin ficha). **Nunca un id** en el fichero: lo que no tenga nombre dice qué es («Administración»,
«Tarea eliminada»).

Se descarga desde la ficha del almacén: **Descargar historial**.

## 3. El fichero

**Hoja «Resumen».** Cabecera con la empresa, el almacén, las sucursales a las que sirve, desde
cuándo hay historial y cuándo se generó. Después, una fila por artículo consumible:

| Columna | Qué es |
|---|---|
| Artículo, Referencia, Unidad | De la ficha |
| Entradas | Compras y altas |
| Traspasos recibidos / enviados | Desde y hacia otros almacenes |
| Salidas | Lo que salió hacia tareas, personas o sucursales |
| Devoluciones | Lo que volvió |
| Ajustes | Lo que cambiaron los recuentos, con signo |
| Existencias según el historial | Rehechas apunte a apunte |
| Existencias ahora | Las del almacén en este momento |
| Coinciden | «Sí», o «Revisar» si no: el hecho, sin suponer la causa |
| Gastado declarado | Lo que se declaró gastado de lo que salió de aquí |
| Asignado sin salir | Lo apartado que aún no ha salido |
| Coste unitario, Valor de las existencias | Con el coste de la ficha, sin valoración |

**Hoja «Movimientos».** Todo, en orden cronológico:

| Columna | Qué es |
|---|---|
| Fecha | Cuándo ocurrió |
| Artículo | Por su nombre |
| Qué pasó | Entrada, Salida, Gastado, Devolución, Recuento, Traspaso recibido / enviado, Asignado, Asignación liberada |
| Entra / Sale | Lo que movió las existencias, con su signo |
| Gastado | Lo declarado; no mueve existencias, porque ya salió |
| Asignado | Lo apartado o liberado; no mueve existencias |
| Existencias después | El saldo del artículo en este almacén tras el apunte |
| A qué fue | «Tarea: …», «Persona: …», «Sucursal: …», «Desde/Hacia almacén …» |
| Quién lo usó | A quién se imputa |
| Quién lo apuntó | Por su nombre, o «Administración» |
| Nota | La del apunte; un recuento dice «de 19 a 10» |

**Hoja «Equipos».** Los ejemplares cuya base es este almacén: artículo, identificador, etiqueta,
estado y dónde está ahora.

**Hoja «Historial de equipos».** El rastro de posición de esos ejemplares (ADR-008): fecha,
equipo, dónde («En el almacén …», «En la tarea …», «Con …»), por qué, estado al recibirlo y quién
lo dijo.

## 4. Contrato

```
GET /warehouses/:warehouseId/history-report?entityId&lang
→ 200 { filename, mimeType, base64 }   el fichero en base64, como la plantilla de importación
```

Permiso: supervisor o superior (`seesEverything`). Idiomas: los textos del fichero en `es`, `en`
y `pt` (desde el 2026-10-17); cualquier otro, en inglés. Allowlist del proxy del panel: `warehouses/:id/history-report`.

## 5. Lo que no cambia

El informe de consumo sigue igual. La descarga CSV de movimientos **se retira** (§7): todas las
descargas del libro son este fichero.

## 6. Implementación (2026-10-17)

- `inventory`: `application/history/warehouseHistory.ts` (las cuatro hojas), `labels.ts` (es/en) e
  `infrastructure/NameCache.ts`: nombres por caché de proceso (10 min), después dimensiones de
  Postgres (`tasks_raw`, `dim_employees`, `dim_branches`, `dim_warehouses`) y Firestore solo para
  lo que falte, con `getAll` agrupado y una vez por id; lo que no tiene nombre también se guarda
  (Jose: «utiliza caché siempre antes de consultar repetitivamente a Firebase»). Estado y posición
  de ahora de los equipos, del instante, en una sola consulta.
- Panel: «Descargar historial» en la ficha del almacén sustituye a «Descargar CSV».
- Probado contra el Postgres de staging (túnel SSH, solo lectura) y Firestore de dev, almacén
  «A principal» de Alvarez: 77 apuntes, 2 equipos y su rastro, cero ids; el saldo rehecho
  coincide con las existencias de ahora en todos los artículos. Segunda descarga: de 2,0 s a 0,5 s
  por la caché.
- Las horas van en la zona de la primera sucursal del almacén (`dim_branches.tz`), o Madrid.

## 7. El de todos los almacenes, los filtros y el fin del CSV (2026-10-17)

> Jose: «Y el general de todos los almacenes por hojas es desde el listado de almacenes».

```
GET /warehouses/history-report?entityId&lang&itemId?&from?&to?
GET /warehouses/:warehouseId/history-report?entityId&lang&itemId?&from?&to?
→ 200 { filename, mimeType, base64, staleness? }
```

- **General.** Hoja «Resumen general», una fila por almacén (activos primero): desde cuándo,
  artículos, entradas, salidas, gastado, valor, cuántos a revisar, equipos y movimientos. Detrás,
  una hoja por almacén con su resumen, movimientos, equipos y rastro, uno debajo de otro. Los
  dos ficheros salen de la misma carga, así que dicen lo mismo.
- **Filtros.** `itemId` y un periodo `from`–`to` (días en la zona del almacén, ambos incluidos).
  El saldo se rehace siempre desde el primer apunte; del periodo se enseña lo que cae dentro, con
  «Existencias al empezar». Un periodo ya cerrado da «Existencias al terminar» y no se compara con
  las de ahora. Con un artículo, el general solo lleva los almacenes donde ese artículo tiene algo.
- **Sin ids, también en artículos.** Un artículo borrado o sin espejar sale por su nombre (caché →
  `dim_items` → Firestore) o como «Artículo eliminado». Comprobado celda a celda en Alvarez y en
  Cuidama: cero ids.
- **`staleness`.** Si quedan apuntes sin llegar a Postgres, la respuesta lo dice y el panel avisa.
- **Panel.** Listado de almacenes: «Descargar historial de todos». Ficha del artículo: el
  historial de ese artículo en todos los almacenes. Informe de consumo: «Historial del periodo
  (Excel)» con su periodo, almacén y artículo. El exportador CSV de movimientos se ha borrado;
  el CSV de la tabla del informe de consumo sigue.

## 8. Norma: consultas masivas en Postgres, informes en el servidor (2026-10-17)

> Jose: «hay que pasarlo al back: todo lo que es consultas masivas es Postgres, reportes e
> informes salen de backend».

- **`NameCache` vive en `shared`** (`packages/shared/src/reporting/NameCache.ts`): caché de
  proceso → dimensiones de Postgres → Firestore agrupado, una vez por id; `namePeople` resuelve
  empleados y cuentas sin ficha. Lo usan `inventory` y `reports`.
- **`GET /movements`** devuelve `taskTitle`, `employeeName`, `registeredByName`,
  `registeredByAutomatic` y `destinationName`.
- **Ejemplares** (`GET /items/:id/units`) y **reservas afectadas** al editar un ejemplar llevan
  `taskTitle`.
- **Informe de consumo** (`reports`): `keyName` en cada línea y `format=xlsx&lang` devuelve el
  Excel generado en el servidor (es/en/pt), con empresa, periodo, agrupado, filtros y total.
- **Panel**: fuera `useNames` y el último exportador CSV; el informe de consumo descarga el Excel
  del servidor y la ficha del artículo ya no pide tareas una a una.
- **Fuera de inventario**: la disponibilidad del calendario también descarga un Excel generado en
  `checkinbiz` (`format=xlsx`, ver `disponibilidad/03_contratos-api.md`). Con esto el panel ya no
  monta ningún fichero.

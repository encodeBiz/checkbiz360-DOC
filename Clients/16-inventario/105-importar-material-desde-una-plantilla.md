# Importar material desde una plantilla

Dar de alta el material artículo a artículo cuesta cuando son decenas o cientos. Esta guía explica cómo cargar de una vez todo lo que hay en un almacén con una hoja de Excel. Requiere el complemento de inventario contratado o en prueba.

---

## Cómo funciona, en tres pasos

| Paso | Qué pasa |
|---|---|
| **1. Descargar la plantilla** | Desde la ficha del almacén. Hay una para consumibles y otra para operables. |
| **2. Rellenarla y subirla** | Una fila por artículo, o por ejemplar si es un operable. Al subirla no se guarda nada todavía. |
| **3. Revisar e importar** | La plataforma enseña qué hará con cada fila. Solo al pulsar **Importar** se da de alta. |

La plantilla va siempre ligada al almacén desde el que se descarga: todo lo que se importa entra en ese almacén.

---

## 1. Descargar la plantilla

1. Vaya a **Inventario → Almacenes** y abra la ficha del almacén.
2. Pulse **Importar** y elija **Consumibles** u **Operables**.
3. Pulse **Descargar plantilla**.

Son dos plantillas porque un consumible y un operable no se describen igual: el primero lleva cantidad y mínimo; el segundo, identificador del ejemplar y unidad de uso. Lo que se importe con cualquiera de las dos aparece después en la misma lista de **Existencias**.

Cada plantilla trae la cabecera y **dos filas de ejemplo**. Las dos empiezan por la palabra **ELIMINAR**: puede borrarlas o dejarlas, porque no se importan.

### Columnas de la plantilla de consumibles

| Columna | Qué poner |
|---|---|
| **Nombre** * | El nombre del artículo: «Toallas», «Desengrasante». |
| **Referencia** | Su código. Es lo que identifica el artículo si vuelve a subir el fichero. |
| **Categoría** | Para agruparlo: limpieza, EPI, papelería. |
| **Unidad** | Cómo se cuenta: unidad, litro, caja, metro. |
| **Coste unitario** | Lo que cuesta cada unidad. Se usa en los informes de coste. |
| **Cantidad inicial** | Lo que hay ahora en el almacén. |
| **Mínimo** | El nivel por debajo del cual se avisa a los responsables. |

### Columnas de la plantilla de operables

| Columna | Qué poner |
|---|---|
| **Nombre** * | El nombre del artículo: «Fregadora industrial». |
| **Referencia** | El código del modelo. |
| **Categoría** | Para agruparlo: maquinaria, vehículos. |
| **Unidad de uso** * | Horas, km o días. La plantilla trae un desplegable. |
| **Coste unitario** | Lo que cuesta cada ejemplar. |
| **Identificador** * | El de su etiqueta: número de serie, matrícula. |
| **Etiqueta** | Un nombre corto: «la fregadora roja». |
| **Lectura del contador** | Horas, km o días que lleva ahora. |

En los operables, **cada fila es un ejemplar**. Tres fregadoras del mismo modelo son tres filas con el mismo nombre y referencia y tres identificadores distintos. Los dos ejemplos de la plantilla son justo eso.

Las columnas con asterisco son obligatorias. Los números se pueden escribir con coma o con punto decimal.

---

## 2. Subir el fichero

Pulse **Elegir fichero**, seleccione la plantilla rellena y pulse **Revisar**. Vale el Excel (.xlsx) o un CSV, de hasta 2 MB. Un CSV guardado desde Excel en español, con punto y coma, también se lee bien.

Si sube la plantilla equivocada —la de operables desde **Consumibles**, o al revés—, la plataforma lo dice y no lee nada.

---

## 3. Revisar lo que se hará

Antes de importar, cada fila dice qué pasará con ella:

| Qué pone | Significa |
|---|---|
| **Nuevo** | El artículo no existe y se creará. |
| **Se actualiza** | El artículo ya existe y se cambian sus datos: nombre, categoría, unidad o coste. |
| **Se reactiva** | El artículo estaba archivado y vuelve a estar activo. |
| **Sin cambios** | El artículo ya existe y el fichero no cambia nada. |
| **Ejemplar nuevo** / **Ejemplar se actualiza** | En los operables, lo mismo para cada ejemplar. |
| **Cantidad inicial** | La cantidad entra en el almacén. |
| **Ya tiene existencias: la cantidad no se aplica** | Ver más abajo. |
| **Ejemplo: no se importa** | Una de las filas que empiezan por ELIMINAR. |
| **No se importa** | La fila tiene un error, que se explica al lado. |

Lo que pide atención sale primero: las filas con error, y las que se parecen a un artículo que ya existe («Se parece a «Toalla»: compruebe que no sea el mismo»).

Las filas con error no se importan; las demás sí. Si quiere incluirlas, corrija el fichero y pulse **Subir otro fichero**. Si cierra la ventana sin importar, no se guarda nada.

Cuando esté conforme, pulse **Importar**. Con muchas filas tarda un poco y se ve el avance; puede cerrar la ventana y la importación sigue.

---

## Cómo sabe si un artículo ya existe

1. **Por la referencia.** Si la fila trae una referencia que ya tiene un artículo, es ese artículo.
2. **Por el nombre**, si la fila no trae referencia o trae una que no existe: «Toallas» y «toallas» son el mismo artículo; «Toallas» y «Toallas pequeñas», no.
3. Si no coincide con nada, es **nuevo**.

Por eso conviene poner la referencia: así puede volver a subir el mismo fichero, corregido o ampliado, y lo que ya existe se actualiza en vez de duplicarse.

### La cantidad inicial solo entra una vez

La **cantidad inicial** solo se suma si el artículo no tiene existencias en ese almacén. Si ya las tiene, se ignora y la revisión lo dice. Cambiar lo que hay en un almacén que ya funciona es un **recuento**, con su motivo, y se hace desde la fila del artículo en **Existencias**.

---

## Quién puede importar

Quien puede dar de alta artículos y registrar entradas: **Manager** y **Owner**.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Existencias, almacenes y entradas](./101-existencias-almacenes-y-entradas.md) | El alta artículo a artículo y el control de lo que hay |
| [Qué es el inventario](./100-que-es-el-inventario.md) | Qué problemas resuelve y cómo se contrata |

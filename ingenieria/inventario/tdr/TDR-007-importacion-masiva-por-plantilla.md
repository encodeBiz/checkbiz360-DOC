# TDR-007 — Importación masiva de artículos por plantilla de almacén

**Fecha:** 2026-10-09
**Estado:** Implementado el 2026-10-09 en `feat/inventario-importacion-masiva` de `encodebiz-api` y de `encodebiz-front-saas`, sin fusionar a `develop`. Lo que la implementación cambió del diseño está en cada sección y resumido en el §10.
**Componente:** `encodebiz-api` — `inventory:3016`; panel `checkinbiz/inventory` (ficha del almacén)
**Decisiones de referencia:** [ADR-002](../adr/ADR-002-almacen-entidad-propia-multisucursal.md),
[ADR-003](../adr/ADR-003-un-catalogo-consumible-y-operable.md),
[ADR-005](../adr/ADR-005-instante-firestore-historico-postgres.md), [TDR-001](./TDR-001-colecciones-y-maestros.md)

---

## 1. El dolor y la decisión

> «Otro dolor increíble es crear a mano cada uno de los ítems.» (2026-10-09)

Decidido en conversación el mismo día:

1. **La plantilla va ligada a un almacén.** Se baja desde la ficha del almacén, el cliente la
   rellena y la sube. El almacén le da todo el contexto: sin columna de almacén, sin
   ambigüedad de a dónde va cada cosa, y respetando que **el artículo nace con su primera
   entrada**: una importación son muchas primeras entradas en ese almacén de golpe.
2. **Dos modelos, no uno:** consumibles y operables. Las columnas no son las mismas y
   mezclarlas obliga a dejar media fila vacía siempre. No contradice «todo es material»
   ([[feedback-todo-es-material]]): lo que entra por los dos cae en la única lista de
   Existencias; solo el fichero de entrada va por tipo.
3. **Solo dos filas de ejemplo y nada más.** La plantilla no baja rellena con lo que el almacén
   ya tiene. Las dos filas llevan la palabra `ELIMINAR` delante del nombre.

## 2. Las plantillas

### Consumibles

| Nombre | Referencia | Categoría | Unidad | Coste unitario | Cantidad inicial | Mínimo |
|---|---|---|---|---|---|---|
| ELIMINAR Toallas | TOA-01 | Limpieza | unidad | 0,80 | 100 | 20 |
| ELIMINAR Desengrasante | DES-5L | Limpieza | litro | 3,20 | 40 | 10 |

### Operables

| Nombre | Referencia | Categoría | Unidad de uso | Coste unitario | Identificador | Etiqueta | Lectura del contador |
|---|---|---|---|---|---|---|---|
| ELIMINAR Fregadora industrial | FRG-01 | Maquinaria | horas | 1 850,00 | FR-1 | Fregadora 1 | 120 |
| ELIMINAR Fregadora industrial | FRG-01 | Maquinaria | horas | 1 850,00 | FR-2 | Fregadora 2 | 0 |

Los dos ejemplos de operables son **el mismo artículo con dos identificadores**, para que se
vea sin explicarlo que dos filas del mismo artículo son dos ejemplares de uno solo. La unidad
de uso admite `horas`, `km` o `días` (se traducen a `hours | kilometers | days`).

**`ELIMINAR`.** El importador **descarta cualquier fila cuyo nombre empiece por `ELIMINAR`** y
la enseña en la propuesta como ignorada. Si el cliente se olvida de borrar los ejemplos, no
aparece una «Toallas» de ejemplo en su catálogo.

**Formato.** La plantilla se entrega como **Excel** (`exceljs`, que ya genera los informes), con
la cabecera y las dos filas. La subida acepta **Excel o CSV**. Motivo: Excel en español guarda
el CSV con punto y coma, coma decimal y codificación antigua, y la mitad de las subidas en CSV
llegarían rotas; si alguna vez se entrega la plantilla en CSV, va con punto y coma y marca de
codificación (BOM). Las cantidades y costes aceptan coma o punto decimal.

## 3. El flujo: subir, ver, confirmar

> **La subida no escribe nada. Primero enseña, después aplica.**

Es el mismo patrón del modal de importar cuadrantes del panel: se sube el fichero, el
servidor lo lee y devuelve una **propuesta fila a fila**, y solo al confirmar se aplica. Una
propuesta que nadie confirma se descarta al cerrar.

Estados de una fila en la propuesta:

| Estado | Significado |
|---|---|
| `nuevo` | No casa con nada: se creará. |
| `nuevo, parecido a X` | Se creará, pero hay un artículo existente de nombre muy parecido. Aviso, no bloqueo: el cliente decide. |
| `se actualiza` | Casa con un artículo existente (§4): se actualizan sus datos. |
| `archivado, se reactiva` | Casa con un artículo archivado: se reactiva en vez de crear un gemelo. |
| `ejemplar nuevo` / `ejemplar existente` | Operables: el identificador no existe / ya existe en ese artículo. |
| `cantidad no aplicada` | El artículo ya tiene existencias en este almacén: la cantidad inicial se ignora (§5). |
| `ignorada` | Empieza por `ELIMINAR`. |
| `error: <motivo>` | Sin nombre, tipo de dato inválido, referencia repetida en el fichero, operable sin identificador, referencia ya usada por un artículo del otro tipo… La fila no se aplica; las demás sí. |

La propuesta lleva los totales (a crear, a actualizar, ejemplares, ignoradas, errores) y se
guarda como lote (§5) para que confirmar sea una llamada con su id, no volver a subir el
fichero.

## 4. Cómo se identifica un artículo nuevo

En este orden, para cada fila:

1. **Si trae referencia**, se busca un artículo de la empresa con esa referencia. Si existe,
   es el mismo: se actualiza. Si existe pero **con el otro tipo**, la fila es un error: el tipo
   no cambia nunca (ADR-003); hay que darle otra referencia.
2. **Si no trae referencia**, se compara el **nombre normalizado** (sin mayúsculas, tildes ni
   puntuación, con el `normalizeText` del buscador del panel), dentro del mismo tipo.
   Igualdad exacta: «Toallas» y «toallas» son lo mismo; «Toallas» y «Toallas pequeñas» no.
   **Si trae una referencia que no existe**, también se mira el nombre, pero solo contra
   artículos **sin** referencia: «Toallas, TOA-01» frente a una «Toallas» sin referencia es el
   mismo artículo, que gana la referencia. Frente a una «Toallas, TOA-02» es otro: dos
   referencias distintas son dos productos.
3. **Lo que no casa con nada es nuevo.** Si casa con más de uno, la fila es un error y pide la
   referencia.

Tres detalles contra los duplicados tontos:

- **Los archivados también cuentan** (`active: false`): si el fichero los trae, se reactivan.
- **Los parecidos se avisan, no se bloquean**, con el mismo criterio que el detector de la
  puesta en marcha —distancia de edición sobre el nombre normalizado, umbral 0,8—, escrito en
  `inventory` porque el de `merlin` no se puede importar desde otro servicio. Se compara solo
  contra lo que comparte el comienzo de alguna palabra, no contra el catálogo entero.
- **Dentro del propio fichero**, dos filas de consumibles con la misma referencia o el mismo
  nombre normalizado son un error: no se sabe cuál manda. En operables es al revés: filas
  repetidas del mismo artículo son ejemplares, y lo que identifica es el **identificador del
  ejemplar, obligatorio en la plantilla**. Sin él no hay forma de saber si la fregadora ya
  existe y cada subida crearía otra.

La referencia es la clave buena: es lo que ya une las toallas de Madrid con las de Barcelona
y lo que hace que subir el fichero dos veces no duplique nada. La plantilla lo dice.

## 5. Qué escribe «confirmar»

Cada fila pasa por **los mismos casos de uso que el panel**, sin camino especial:

- Artículo nuevo → `CreateItem` (con su entrada en `searchIndex`). Existente → `UpdateItem`
  con nombre (si vino por referencia), categoría, unidad y coste; el tipo nunca.
- Consumible: la **cantidad inicial como movimiento `receipt`** por el libro
  (`StockOperations.receipt`), con nota «Importación · fichero» y **solo si el artículo no tiene
  existencias en ese almacén**, que quiere decir **saldo y comprometido a cero**. Que exista el
  registro de existencias no basta: fijar solo el mínimo lo crea a cero, y eso no puede cerrar
  la puerta a la cantidad de una subida posterior (salió en la prueba contra dev). Si las tiene,
  la cantidad se ignora y la propuesta lo dice: cambiar un saldo es un recuento con motivo
  firmado por una persona ([TDR-002](./TDR-002-saldos-movimientos-y-conciliacion.md) §5). Después,
  el mínimo, **solo si cambia** respecto al que ya tenía: volver a subir el mismo fichero sale
  «sin cambios».
- Operable: `CreateItemUnit` por fila con identificador, etiqueta, base en el almacén y lectura
  del contador; si el identificador ya existe en ese artículo, se actualizan etiqueta y
  contador si cambian. Un identificador de un ejemplar **retirado** es un error; uno con base
  en **otro almacén** se actualiza igual pero no se mueve, y la propuesta lo avisa.

**Se aplica en segundo plano.** Miles de filas pasan del minuto, y una petición colgada ese
rato acaba cortada por algún intermediario. «Confirmar» pasa el lote a *aplicando* en una
transacción —dos clics no lanzan dos aplicaciones—, responde `202` y aplica de cuatro en cuatro
artículos, apuntando el avance cada dos segundos. El panel pregunta por el lote hasta que
termina. Un lote *aplicando* que lleva cinco minutos sin dar señales se da por muerto y se
puede reanudar.

**Al aplicar se vuelve a planificar** contra el catálogo de ese momento con la misma función
que hizo la propuesta: si alguien creó un artículo entre medias, ahora se actualiza en vez de
duplicarse, y un reintento encuentra lo que el intento anterior ya creó.

**Idempotencia.** El `movementId` de cada entrada es fijo por lote y fila
(`imp_{batchId}_{fila}`): un reintento de «confirmar» no duplica existencias, que es la misma
protección que tiene la app (ADR-005).

**El lote queda registrado** en `entities/{e}/import_batches/{batchId}`: quién, cuándo, nombre
del fichero, almacén, tipo, propuesta, resultado por fila y totales. Es el «quién importó qué».

**Límites:** 2 MB y 5.000 filas por fichero —dos mil artículos en Excel pesan unos cien
kilobytes—. Lo que pasa de ahí es `413 inventory/import_too_large`. **Ningún límite de plan**:
un límite nunca para el servicio ([[feedback-limite-de-plan-nunca-para-el-servicio]]).

## 6. Rutas y permisos

```
GET    /warehouses/:warehouseId/import-template?type&lang   → {filename, mimeType, base64}
POST   /warehouses/:warehouseId/imports   {type, filename, content: base64, lang} → 201 {batchId, rows[], totals}
POST   /imports/:batchId/apply                               → 202 {status: "applying", progress}
GET    /imports/:batchId                                     → estado, avance y, al terminar, el resultado fila a fila
DELETE /imports/:batchId                                     → descartar una propuesta sin confirmar
```

- **Antes que nada, el add-on activo** (`requireInventorySubscription`).
- Permiso `manager`, el mismo que crear artículos y registrar entradas (04 §Permisos).
- **El fichero viaja en base64 dentro de JSON, no en multipart** —cambio sobre el diseño—. El
  proxy del panel reempaqueta toda respuesta como JSON (una plantilla binaria llegaría rota) y en
  producción corre en Vercel, que corta los cuerpos de más de 4,5 MB. Es el mismo camino que ya
  usa la importación de cuadrantes. La ruta de subida lleva su propio lector JSON de 4 MB, montado
  antes del general de 1 MB, y el `location` de inventario en nginx el mismo límite
  (`client_max_body_size 4m`; sin él nginx corta en su mega por defecto). Está en el registro del
  pase a producción de octubre.
- El fichero se lee en el servidor y no se guarda: el lote guarda las filas leídas.
- `apply` sobre un lote ya aplicado devuelve `200` con lo aplicado sin tocar nada; sobre uno
  descartado, `409 inventory/import_closed`.
- Errores de forma con nombre propio: `import_wrong_template` (la otra plantilla),
  `import_missing_column` (con la columna), `import_unreadable` (un `.xls` de Excel 97 pide
  guardarlo como `.xlsx` o CSV), `import_empty`, `import_too_large`.

## 7. El panel

En la ficha del almacén, **un botón «Importar» con dos entradas, Consumibles y Operables**
—cambio sobre el diseño: dos botones más en una cabecera que ya tiene editar, traspaso y nueva
entrada la llenaban; la acción principal sigue siendo «Nueva entrada»—. Cada entrada abre el
diálogo de su tipo, con su «Descargar plantilla».

El diálogo (`ImportMaterialDialog`, cargado aparte como los demás del módulo) sigue cuatro
pasos: el fichero; la propuesta, con los totales en pastillas y la tabla fila a fila con lo que
pide atención primero (errores, avisos y parecidos, lo demás y los ejemplos al final), de 25 en
25; el avance, que se puede cerrar sin parar la importación; y el resultado. Cerrar en la
propuesta la descarta. Al terminar se repintan catálogo, contenido y movimientos del almacén.

Las plantillas salen en el idioma del panel (es, en, pt, de, fr), con su palabra delante de los
ejemplos (ELIMINAR, DELETE, EXCLUIR, LÖSCHEN, SUPPRIMER), los ejemplos en gris, un asterisco en
las columnas obligatorias y un desplegable de horas, km o días en la unidad de uso. Al leer se
aceptan las cabeceras de cualquiera de los cinco idiomas y los nombres habituales (`SKU`,
`código`, `precio`…), y se ignora cualquiera de las cinco palabras.

## 8. Fuera de la primera versión

- **Leer el Excel propio de cada cliente**, con sus columnas a su manera: es el camino de
  Merlin que ya usan los cuadrantes, y tiene sentido como segundo paso si llegan ficheros que
  no caben en la plantilla.
- **Deshacer un lote.** La propuesta previa es la red de seguridad.
- **Un fichero para varios almacenes.** Uno por almacén es lo que lo hace simple.
- **Plantilla prellenada con lo que ya hay.** Se propuso y se descartó: dos ejemplos y nada más.

## 9. Criterio de éxito

Un cliente baja las dos plantillas de un almacén, rellena cincuenta consumibles y diez
ejemplares en Excel, las sube y ve una propuesta que distingue nuevos, actualizados, parecidos,
ignorados y errores con motivo; confirma; y Existencias enseña todo con sus cantidades y
mínimos, el buscador los encuentra, y el libro tiene una entrada por consumible con nota
«importación». Sube el mismo fichero otra vez y no se duplica nada. Sin el add-on, las rutas
devuelven el 403 de siempre.

## 10. Comprobado el 2026-10-09, y lo que queda

- **Parte pura** (plantilla, lectura y planificación, sin Firestore): 48 comprobaciones en verde
  —las diez plantillas releídas con sus dos ejemplos ignorados, plantilla equivocada, `.xls`,
  números como los escribe una persona, CSV de Excel en español en Windows-1252, y los casos de
  identificación: por nombre, referencia nueva sobre artículo sin referencia, mismo nombre con otra
  referencia, archivado, sin cambios, parecido, duplicados, tipo equivocado, ejemplar retirado y en
  otro almacén, unidad de uso inválida—.
- **De extremo a extremo contra dev**, con el servicio en local, Firestore de dev y un Postgres
  desechable con las 24 migraciones: 30 comprobaciones en verde en Entregalia (add-on en prueba)
  sobre un almacén «(prueba) Importación» —propuesta, confirmar en segundo plano, existencias,
  mínimos, apunte en el libro con su nota, buscador, espejo a Postgres, reconfirmar y resubir sin
  duplicar, CSV, operables con ejemplares, plantilla equivocada, 413, descartar, y 403 en una
  entidad sin add-on—. Todo lo creado se borró al terminar.
- **Panel**: tipos y lint en verde y la ficha del almacén compila. **No se ha visto en un
  navegador**: falta probar el diálogo a mano en el panel de staging.

Pendiente:

- **Propuestas abandonadas.** Una propuesta que no se confirma ni se descarta (el navegador se
  cierra) se queda como *propuesta* con sus filas. No estorba a nada, pero hará falta un barrido.
- Fusionar a `develop` y, cuando sea una versión usable, a `staging`.

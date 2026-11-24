# TDR-001 — Catálogo de convenios colectivos

**Fecha:** 2026-11-23
**Estado:** Aprobado por Jose el 23-nov-2026. Fase 1 EN STAGING el 23-nov (API `develop` `cfadc30` → `06e6b82`, `staging` `c4ddc5c`); fases 2–4 en desarrollo.
**Componentes:** `packages/shared` (modelo), `services/entities` (API del panel),
`services/backoffice` (API de soporte), `services/merlin` (lectura de tablas y cruce con el
contrato), panel y backoffice (pantallas).

---

## 1. Problema

Para proponer el precio por hora de un contrato hacen falta dos cosas del convenio: la
**jornada anual** a tiempo completo y, si el contrato dice «según tablas», el **sueldo de la
categoría**. Hoy las busca el modelo en internet en cada contrato. Medido en staging del 22 al
23-nov-2026:

- **Leer una tabla ya descargada funciona.** El modelo saca la fila correcta de un PDF oficial
  cuando se le da el texto (metal de Madrid 2026, grupos 4 y 5 del BOCM).
- **Localizar el documento no es fiable.** El mismo contrato unas veces lleva a la revisión
  salarial de 2026 y otras al convenio de 2022. Las horas anuales del metal salieron 1.748 en
  una lectura y 1.715,3 en otra.
- **Cuesta en cada contrato lo que debería costar una vez.** 35–48 mil tokens y 1–2 minutos
  por contrato; la mitad son búsquedas.

Un sueldo de un año equivocado, propuesto con aspecto oficial, es peor que pedir el precio a
mano.

## 2. Decisión (Jose, 23-nov-2026)

Un **catálogo de convenios** con sus tablas, que mantiene Encodebiz y al que una empresa puede
añadir el suyo. Cada convenio y año se lee **una vez para todos**. El contrato se cruza con el
catálogo y el cliente **confirma**; nada se busca en internet.

Lo que Jose fijó:

1. **Sin convenio por defecto en la empresa.** Una empresa puede regirse por varios convenios
   a la vez (limpieza y oficinas, por ejemplo). El cruce es contrato a contrato: se propone y
   se confirma cada vez. Lo que se guarda es, en cada contrato, qué convenio y qué tabla se
   usaron.
2. **Catálogo por nicho y ámbito.** Hostelería de Sevilla y de Madrid son convenios distintos.
   Cada convenio lleva nicho(s) y ámbito (estatal, autonómico, provincial, de empresa) con su
   territorio; el filtro para la empresa usa su nicho y su provincia.
3. **Cada tabla lleva su año a la vista**, y el contrato avisa cuando su fecha es posterior.
   Un repaso **mensual** de los convenios en uso (lista para soporte, no un robot que busque).
4. **Lo que sube una empresa vale para ella desde ese momento** y entra en el catálogo
   compartido como «aportado, sin revisar» hasta que soporte lo mire desde backoffice. Mismo
   patrón que los nichos `pending`.
5. **Se pide opcionalmente al subir el contrato.** El formulario de subida lleva un selector de
   convenio (la lista filtrada por nicho) y la opción «referenciar otro convenio». Si se da,
   la lectura no cruza: usa ese.
6. **Siembra:** los convenios de los nichos principales y de los clientes —limpieza, montaje
   de eventos y ayuda a domicilio— para las provincias donde hay clientes. Nada más por ahora.
7. **No existe un «convenio general».** Jose preguntó por «generales, como 40 h». Lo que hay
   es el **mínimo legal**: el Estatuto de los Trabajadores (40 h semanales de media al año,
   que son como mucho 1.826 h y 27 min anuales) y el salario mínimo interprofesional (SMI).
   Entra en el catálogo como una entrada del sistema, `kind: "legal"`, con su año: es lo que
   se usa cuando el contrato no cita convenio o el suyo no está sembrado. Sustituye la
   estimación de hoy a 40 × 52 = 2.080 h, que es imposible (ningún contrato trabaja las
   vacaciones ni los festivos).
8. **Cuando entra una empresa nueva** (o pone su nicho, o añade una sucursal) se comprueba si
   el catálogo cubre su nicho en sus provincias, que salen de los códigos postales de la
   empresa y de sus sucursales. Lo que no está cubierto aparece en backoffice como «convenios
   por sembrar» y se avisa a soporte. Ver 4.6.

## 3. Modelo de datos

### 3.1 `agreements/{agreementId}` (colección raíz, como `niches`)

```ts
interface Agreement {
  id: string;
  /** Nombre oficial, como lo publica el boletín. */
  name: string;
  /** Nombres normalizados (oficial, corto, siglas) para casar con lo que escribe el contrato. */
  keys: string[];
  sector: string;                 // texto corto: «limpieza de edificios y locales»
  nicheIds: string[];             // un convenio sirve a varios nichos; un nicho tiene varios convenios
  scope: "estatal" | "autonomico" | "provincial" | "empresa";
  /** Código de provincia (INE, 2 cifras) o de comunidad; null si estatal. */
  territory: string | null;
  /** Código del convenio en REGCON (99001655011995…), si se conoce. Identifica sin ambigüedad. */
  regconCode: string | null;
  /** `legal`: la entrada del mínimo legal (ET + SMI), una sola, del sistema. */
  kind: "agreement" | "legal";
  status: "approved" | "pending" | "rejected" | "merged";
  mergedInto: string | null;
  /** `system` si lo sembró Encodebiz; si no, la empresa que lo aportó. */
  createdBy: "system" | string;
  createdByUid: string | null;
  /** Resumen de la tabla más reciente, para no leer la subcolección en las listas. */
  latestTable: { year: number; status: TableStatus; reviewed: boolean } | null;
  createdAt; updatedAt; updatedBy;
}
```

Visibilidad: una empresa ve los `approved` y los `pending` que creó ella. Igual que con los
nichos, lo que agrupa va por `id`, nunca por nombre.

### 3.2 `agreements/{agreementId}/tables/{year}`

Una tabla por año. El `year` es el **año de vigencia de la tabla**, no el de publicación.

```ts
interface AgreementTable {
  year: number;
  source: {
    kind: "url" | "file";
    /**
     * Si `url`: la del boletín oficial. Solo dominios oficiales (`isOfficialSourceUrl` en
     * `shared`, la misma lista para backoffice, entities y merlin). Se admite http, porque un
     * enlace copiado del BOE a veces viene así y los boletines redirigen a https, pero se
     * guarda siempre por https (`normalizeOfficialSourceUrl`).
     */
    url: string | null;
    /** Si `file`: dónde quedó el PDF. */
    storagePath: string | null;
    /** El documento que subió la empresa, si lo subió como documento. */
    documentId: string | null;
  };
  status: "processing" | "done" | "failed";
  error: string | null;
  /** La jornada a tiempo completo que dice el texto. Null si no venía (la tabla vale igual). */
  fullTime: { annualHours: number | null; weeklyHours: number | null };
  rows: AgreementRow[];
  /** Páginas del documento que se leyeron (índices), para poder enseñar de dónde sale. */
  pagesUsed: number[];
  /** Quién revisó las filas desde backoffice. Las de `system` nacen sin revisar también. */
  reviewed: boolean;
  reviewedBy: string | null;
  reviewedAt: Date | null;
  /** Consumo de la lectura, para el histórico (project-consumo-ia-por-empresa). */
  usage: { model: string; inputTokens: number; outputTokens: number } | null;
  readAt: Date;
}

interface AgreementRow {
  /** Como lo escribe la tabla: «Oficial de 2ª», «Grupo 4», «Auxiliar de ayuda a domicilio». */
  category: string;
  group: string | null;           // «4», «V», «G5»
  level: string | null;
  /** Normalizados para el cruce. */
  keys: string[];
  amountCents: number;
  period: "month" | "year";
  payments: number | null;        // 12, 14, 15; null si la tabla da el anual
  /** La celda textual tal cual, por si hay que enseñarla. */
  cell: string;
  /**
   * El bloque de la tabla si el convenio trae varias (una por ámbito —«Ayuda a domicilio»,
   * «Residencias»—, por zona o por tipo de establecimiento). La misma categoría puede salir en
   * varios bloques con importes distintos: va una fila por bloque. Null si la tabla es una.
   */
  section: string | null;
  /** La jornada completa de ese bloque si es distinta de la de la tabla; null, la de la tabla. */
  fullTime: { annualHours: number | null; weeklyHours: number | null } | null;
}
```

**Una tabla, varias jornadas (24-nov).** El VIII convenio de dependientes tiene una jornada por
ámbito (1.735 h ayuda a domicilio, 1.772 h residencias en 2025) y una tabla por ámbito con
categorías repetidas. La lectura (`tablas_convenio`) devuelve en cada fila su `seccion` y, si el
artículo de jornada da una por ámbito, `jornadas: [{seccion, horas…}]`, que se cuelgan de sus
filas (`row.fullTime`). El precio de una fila usa su jornada si la tiene y la de la tabla si no
(`rowFullTime`). Soporte ve y corrige el bloque y la jornada por fila en backoffice («Varias
tablas por bloque»).

### 3.3 Dónde va el PDF

- Subido por una empresa: como un **documento de empresa** más (`documents`, tipo nuevo
  `agreement`, ámbito `entity`), así que queda en `documents/entities/{entityId}/…`, cifrado y
  **contado en su almacenamiento** por el trigger de Storage sin prefijo nuevo. La tabla guarda
  `source.documentId` y merlin lo descarga por el documental, como hace con el contrato. Ningún
  código suma al contador.
- Sembrado por Encodebiz: bucket del sistema, `agreements/{agreementId}/{year}.pdf`. No se cobra.
- Si viene por enlace, no se guarda copia: queda la `url`. Si el boletín la cambia, se vuelve
  a leer.

Un convenio es un documento público sin datos personales: va al modelo tal cual, sin sombra, y
no se cifra.

### 3.4 En la lectura del contrato

`documents/{d}/readings/employment_contract.result.proposal` gana:

```ts
agreementMatch: {
  /** Lo que se propone (o lo que vino del formulario de subida). */
  agreementId: string | null;
  year: number | null;
  /** Fila elegida para la categoría, si la hay. */
  rowIndex: number | null;
  /** Por qué se propone: `given` (lo eligió quien subió), `matched`, `ambiguous`, `none`. */
  how: "given" | "matched" | "ambiguous" | "none";
  /** Si `ambiguous`: hasta 5 candidatos para elegir en el panel. */
  candidates: { agreementId: string; year: number; name: string; scope: string }[];
}
```

Y en `aplicar`, la responsabilidad del empleado guarda `agreementRef: {agreementId, year}` junto
al `price`. No se guarda nada en la empresa.

## 4. Flujos

### 4.1 Alta de un convenio por Encodebiz (backoffice)

1. Formulario: nombre, sector, ámbito y territorio, nichos, código REGCON (opcional), año de
   la tabla, y **enlace al boletín o PDF**.
2. `POST /api/v1/backoffice/agreements` crea el `Agreement` (`approved`, `createdBy: system`).
3. `POST …/agreements/:id/tables/:year` guarda la fuente y pide a merlin la lectura
   (`POST /api/v1/gpt/soporte/convenios/:id/tablas/:year/leer`, ruta interna).
4. Merlin: si `url`, `descargarDocumentoOficial` (solo oficiales); si `file`, lo lee del bucket
   del sistema; si `documentId` (convenio aportado por una empresa), lo pide al documental con
   `getDocumentFile`, que es quien tiene la llave del cifrado.
   `elegirPaginas` (≤ 45 mil caracteres) y una llamada **sin herramientas** que devuelve
   **todas las filas** de la tabla y la jornada (`tablas_convenio`, esquema con `rows[]`). Es la
   parte de `tablas.ts` que ya funcionaba; cambia solo que pide la tabla entera y no una fila.
5. Las filas quedan en `tables/{year}` con `reviewed: false`. Backoffice las enseña junto al PDF
   (página usada) y soporte marca «revisada» o corrige celdas a mano.

Un PDF con tabla de 60 filas son unos 10–15 mil tokens de entrada y 2–4 mil de salida, **una
vez**.

### 4.2 Alta de un convenio por una empresa (panel)

Pantalla «Convenios» (dentro de Documentos o de la configuración de la empresa): la lista que
le aplica (los `approved` de su nicho y los suyos) y el botón **«Referenciar convenio»**:

1. Nombre, ámbito (estatal / autonómico / provincial; provincia prellenada con la de la
   empresa), año de la tabla, y enlace o PDF. El nicho se toma de la empresa (`entity.niche`);
   no se pregunta.
2. `POST /api/v1/agreements` (en `entities`, requiere escritor de la empresa) crea el
   `Agreement` como `pending`, `createdBy: entityId`, y lanza la lectura igual que en 4.1.
3. La empresa lo usa desde ese momento. Soporte lo ve en backoffice en «aportados, sin
   revisar» y lo aprueba (pasa a compartido), lo fusiona con uno existente (`mergedInto`; los
   contratos que lo referencian siguen resolviendo) o lo rechaza (la empresa lo sigue viendo
   como «rechazado», con el motivo).

Si la empresa no tiene nicho, la pantalla le pide ponerlo antes (ya existe el selector).

### 4.3 Lectura de un contrato

1. Si en la subida se eligió convenio → `how: "given"`, se salta el cruce.
2. Si no, con lo que el modelo leyó del contrato (`convenio.nombre`, `sector`, `ambito`,
   `territorio`, `regconCode` si el contrato lo trae) se cruza **en el servidor, sin modelo**:
   - candidatos = `approved` cuyo `nicheIds` contiene el nicho de la empresa ∪ los `pending` de
     la empresa;
   - se puntúa: código REGCON igual (decide solo), `keys` del nombre, sector, ámbito y
     territorio coincidente con la provincia de la empresa;
   - uno claro → `matched`; varios → `ambiguous` con candidatos; ninguno → `none`.
3. Con convenio: tabla del **año de inicio del contrato** (o la más reciente anterior); si la
   más reciente es de un año anterior, aviso «las tablas guardadas de este convenio son de
   2025». Jornada anual = `fullTime.annualHours` (pasa por `jornadaAnualCreible`).
   Sin convenio (`none`, o el contrato no cita ninguno): la entrada `legal` del año: 1.826 h
   anuales a 40 h (regla de tres para jornadas parciales) y el SMI como suelo. El precio se
   marca `estimated: true` con la base «a la jornada máxima legal, sin convenio». Si el
   salario del contrato queda por debajo del SMI a su jornada, aviso con las dos cifras.
4. La **fila** se casa en el servidor por `group`/`level` y `keys` de la categoría. Si la misma
   categoría está en varios bloques (`section`), decide el bloque cuyas palabras están en el
   sector y el oficio del contrato («auxiliar de ayuda a domicilio» → «Ayuda a domicilio»);
   si ninguno o varios casan, candidatas y el panel pregunta. La jornada del precio es la del
   bloque de la fila (`row.fullTime`) o la de la tabla, también cuando el contrato trae su
   cifra. Si el contrato remite a las tablas y la fila no casa, `rowIndex: null` y el panel
   enseña las filas para elegir. Ninguna cifra la escribe el cliente a mano en este paso.
5. El precio lo calcula el servidor con la fila y la jornada (`aJornada` + `costeHora`), nunca
   con números que mande el navegador. `sources` pasa a ser la fuente de la tabla.

6. Si no hay convenio (`none`) y el contrato remite a las tablas, la empresa recibe «sube el
   convenio o escribe el precio» y **soporte recibe también un aviso** (Jose, 23-nov) con el
   nombre del convenio tal como lo leyó el modelo, el nicho y la provincia de la empresa, para
   sembrarlo por 4.1. Sin datos del contrato ni de la persona. Un aviso por convenio y empresa,
   no uno por contrato.

Una lectura queda en **una llamada al modelo** (~16 mil tokens, ~20 s). La segunda llamada
(`localizar_convenio` + `tablas_convenio` por contrato) desaparece.

### 4.4 Confirmar y aplicar

El panel enseña «Este contrato va por **{nombre del convenio}** · tablas de {año} · fila
«{categoría}» → {precio} €/h», con el enlace al documento y los botones «Cambiar convenio» /
«Cambiar fila». `POST …/:documentId/aplicar` recibe `agreementId`, `year` y `rowIndex` (además
de lo de hoy), **recalcula** el precio en el servidor y escribe `price` y `agreementRef` en la
responsabilidad.

### 4.5 Altas de empresas y sucursales: cobertura del catálogo

Las provincias de una empresa salen de los **códigos postales**: las dos primeras cifras del
de la dirección legal (`entity.legal.address.postalCode`) y de cada sucursal
(`branches/{b}.address.postalCode`) son el código INE de la provincia. No hace falta
geocodificar ni leer la calle.

- Al crear la empresa y al ponerle o cambiarle el nicho, `entities` recalcula
  `(nicho × provincias)` y lo compara con los `agreements` aprobados (`nicheIds` ∋ nicho y
  `territory` ∈ provincias, o estatal). Lo que no cubre nada va a
  `agreement_gaps/{entityId}_{nicheId}_{provincia}` con la fecha.
- Las sucursales no se crean en `entities` sino en `branches`, así que el cálculo vive en
  `shared` (`agreementCoverage.ts`) y lo llaman los dos sin HTTP entre servicios. `branches`
  recalcula al crear una sucursal, al cambiarle el código postal o el estado (un cambio de
  nombre o de valla no mueve ningún hueco) y al borrarla, sin esperar el resultado: la
  cobertura es consecuencia del alta, no parte de ella, y si falla la sucursal existe igual.
- Las sucursales que crean las Cloud Functions del SaaS no pasan por `branches`: entran en la
  cobertura con la pasada diaria (03:30), que también recoge lo que haya fallado en caliente.
- Backoffice, pantalla «Convenios por sembrar»: cada hueco con la empresa, el nicho, la
  provincia y cuántas sucursales tiene allí. Al dar de alta el convenio (4.1) el hueco se
  cierra solo; soporte también puede marcarlo «no aplica» con un motivo.
- Aviso a soporte por correo al abrirse un hueco, agrupado por día (una empresa que crea diez
  sucursales el primer día produce un correo, no diez).
- Los huecos de las empresas que ya existen se calculan una vez con un script (solo lectura
  sobre `entities` y `branches`, en staging; en producción con el OK de Jose) y son la lista
  de la siembra del §7.

Una empresa sin código postal legal ni sucursales no tiene provincia: se le asume la del
nicho estatal y queda en la lista como «sin provincia».

### 4.6 El año y el repaso mensual

- En cada lista (panel y backoffice) el convenio se ve con «tablas de {año}».
- Backoffice, pantalla «Convenios en uso»: por convenio, el año de su última tabla, cuántas
  empresas y cuántos contratos lo referencian. El recuento vive en el propio convenio
  (`usedCount` y `usedBy.{entityId}`, que `aplicar` incrementa al escribir `agreementRef`), para
  no necesitar una consulta de grupo de colecciones ni su índice.
- El día 1 de cada mes, un correo a soporte con los convenios en uso cuya última tabla es de un
  año anterior al actual. No busca nada: lista lo que hay. Encodebiz localiza la revisión
  salarial a mano y la da de alta por 4.1.

## 5. Lo que se quita

- `localizar()` y `herramientaBusqueda` en `application/tablas.ts`; `DOMINIOS_BUSQUEDA` deja
  de usarse para buscar (se queda `esFuenteOficial` para validar enlaces).
- La variable `CONTRATOS_BUSQUEDA` y `max_tool_calls`.
- Los avisos de narración de búsqueda (`narraLaBusqueda`) sobran: ya no hay búsqueda.

Se conservan `descargarDocumentoOficial`, `elegirPaginas`, `textoConDisposicion`, `aJornada`,
`jornadaAnualCreible` y la llamada `tablas_convenio` (con el esquema ampliado a filas).

## 6. Permisos, reglas e índices

- Escrituras de `agreements` **solo por backend** (`entities` para la empresa, `backoffice` para
  soporte). El panel **lee también por API** (`GET /api/v1/agreements…` en `entities`, que
  filtra por nicho, provincias y `createdBy`), así que no hace falta abrir reglas de Firestore:
  `agreements`, `tables` y `agreement_gaps` quedan cerrados al cliente.
- Índice compuesto: `agreements` por `status == approved` + `nicheIds array-contains`. Se crea
  con `gcloud`, nunca desde el enlace del error.
- Backoffice: permiso nuevo `agreements:write` (como `niches:write`).

## 7. Siembra

Encodebiz da de alta a mano, uno a uno y comprobando el documento, los convenios que salgan de
los huecos del §4.5 para las empresas actuales. La lista de partida, a falta de ese cálculo:

| Nicho | Convenio | Ámbito |
|---|---|---|
| (todos) | Mínimo legal: Estatuto de los Trabajadores + SMI, `kind: legal` | estatal, una entrada por año |
| Limpieza | Limpieza de edificios y locales | provincial (el marco estatal no trae tablas) |
| Montaje de eventos | Industria, tecnología y servicios del metal | provincial (Madrid ya probado: BOCM 2026) |
| Ayuda a domicilio | Servicios de atención a personas dependientes (VIII marco) | estatal; hay autonómicos (Madrid) |

Las provincias las da el cálculo del §4.5 sobre las empresas reales; hasta entonces no se
siembra nada provincial «por si acaso».

Las 1.792 h del convenio de dependientes que hoy usa el código salen de una lectura del modelo
y **no están cotejadas** con el BOE (BOE-A-2023-13742): la siembra las fija leyendo el
documento, no la memoria. Las cifras del SMI y las 1.826 h 27 min del ET se escriben a mano
desde el BOE del año, sin modelo.

## 8. Qué se mide para dar el OK

- Un contrato «según tablas» de un convenio sembrado propone la fila correcta sin búsqueda, en
  una llamada.
- El contrato real de ayuda a domicilio da 8,10 €/h con la jornada del convenio sembrado, y la
  cifra se puede señalar en el PDF del BOE.
- Una empresa referencia un convenio nuevo por PDF y su siguiente contrato lo usa; soporte lo
  ve como «aportado» y lo aprueba.
- Un contrato de 2026 contra una tabla de 2025 avisa del año.

## 9. Fases

1. **Modelo y lectura de tablas** (`shared`, merlin, backoffice API): entrada `legal`, alta por
   Encodebiz, script de huecos sobre las empresas de staging y siembra de lo que salga (al
   menos dependientes y metal Madrid, ya probados). Retirada de la búsqueda.
2. **Cruce en la lectura del contrato** y `aplicar` con convenio; panel: tarjeta de lectura con
   convenio y fila, selector opcional en la subida.
3. **Referenciar convenio desde el panel** (`entities` API, pantalla, reglas) y revisión en
   backoffice.
4. **Cobertura al dar de alta empresas y sucursales** (§4.5), convenios en uso y correo mensual.

Cada fase va a staging con empresas de prueba; producción, cuando Jose lo diga.

## 10. Abierto

- Tablas con varias columnas por antigüedad o por tipo de establecimiento (hostelería): la
  primera versión guarda la columna base y avisa de que hay más (`warnings`).
- ~~Una tabla, una jornada~~ → resuelto el 24-nov: bloque y jornada por fila (§3.2). Queda
  volver a leer (o corregir a mano) la tabla 2025 de dependientes sembrada en staging el
  23-nov, que se guardó sin bloques: hoy sus 44 filas valen todas con la jornada de ayuda a
  domicilio.
- **Contratos de formación.** El SMI va en proporción al tiempo de trabajo efectivo (65 % el
  primer año), no a la jornada del contrato, así que en formación no se compara con el SMI
  (arreglado el 23-nov). El precio por hora se calcula sobre las 40 h del contrato; el aviso de
  «coste real distinto» ya lo dice.
- **Pruebas solo con contratos ficticios.** Un contrato real de una persona no se usa para
  probar aunque lo dé Jose (23-nov): generador en el scratchpad y PDFs «(ficticio)».
- Convenios de empresa (`scope: empresa`): solo los ve la empresa que los sube, nunca pasan a
  compartidos.

# Traspaso a la sesión de la landing — 13-nov-2026

Para: la sesión de Claude que lleva la landing de CheckBiz360
(`/Users/joseacevedo/Documents/EncodeBiz-ALL/PLATAFORMA/CheckBiz360-Landing`, Vite + React).
De: una sesión del repo `encodebiz-api`, que **no ha tocado la landing**: solo ha leído y escrito
este documento.

Lo que pasa: desde el 11-nov-2026 todo CheckBiz360 se cobra **más IVA** y han llegado a producción
varias funcionalidades que la web no cuenta. El manual de cliente ya está al día en español
(commit `dc69a5e` de `PLATAFORMA/DOCS`, carpeta `Clients/`). La landing no.

Orden de trabajo: **prioridad 1 (precio) entera, enseñarla a Jose, y solo después la 2 y la 3.**
Nada se publica en producción sin el OK de Jose.

Los números de línea son del 13-nov (último commit de la landing: `ec1cf44`). Si han cambiado,
busca por la clave o por el texto.

---

## 1. Prioridad 1 — el precio, siempre «+ IVA»

### La orden y las cifras

Orden de Jose (13-nov): **«2 € + IVA» en todas partes.** Desde el 11-nov-2026 todo se cobra más IVA
(21 % en España peninsular y Baleares), desglosado en la factura.

| Concepto | Precio | Fuente en código |
|---|---|---|
| Plan Bronce | **2 € + IVA** por empleado al mes | `encodebiz-api/packages/shared/src/platform/pricing.ts` → `checkinbiz.bronze.unitPrice: 2` |
| Inventario (complemento) | **29 € + IVA** al mes hasta 50 empleados; **0,75 € + IVA** por empleado desde el 51 | mismo fichero → `inventory.standard` (29 / 50 / 0.75) |
| Punto de fichaje (complemento) | **19 € + IVA** al mes hasta 20 puntos activos; **0,90 € + IVA** por punto desde el 21 | mismo fichero → `kiosk.standard` (19 / 20 / 0.9) |
| Almacenamiento | **2 GB incluidos**; **0,25 € + IVA** por GB completo de más | `encodebiz-api/packages/shared/src/checkbiz/storageUsage/storageUsage.ts` → `STORAGE_INCLUDED_GB = 2`, `STORAGE_EUR_PER_GB = 0.25` |
| Plan Empresarial | A medida | `checkinbiz.enterprise.custom: true` |

Comprobado en el código el 13-nov: las cifras cuadran. El código guarda los precios **sin IVA**
(«en euros y sin IVA», dice la cabecera de `pricing.ts`).

### ⚠ La tarifa de 5 € desde el 01/01/2027: pendiente de confirmar por Jose

La landing anuncia que **desde el 01/01/2027 las altas nuevas pagarán 5 €** (el «5 €» tachado
junto al «2 €», las frases «Desde el 01/01/2027…», `TARIFF.listPrice: 5` y
`TARIFF.validUntil: '2026-12-31'` en `src/data/tariff.ts`). **El código de la plataforma no tiene esa
tarifa**: `pricing.ts` solo conoce 2 €. El manual de cliente sí la repite («5 € + IVA»).

**No la cambies ni la quites.** Déjala como está y, en lo que enseñes a Jose, márcala como
«pendiente de confirmar por Jose». Lo único que se propone tocar en esas frases es añadir «+ IVA» al
5 € para que no haya un precio sin IVA en la página; si Jose prefiere no tocarlas hasta decidir,
se dejan tal cual.

### Lo que hay que cambiar, sitio por sitio

Regla de redacción: el importe grande se queda en «2 €» y el «+ IVA» va pegado a él o en la nota
de debajo. En inglés, «€2 + VAT». En portugués, «2 € + IVA». **En las versiones inglesa y
portuguesa no pongas «21 %»**: ese tipo vale para empresas con sede en España peninsular y
Baleares; el resto se confirma caso a caso (el manual remite a hola@encodebiz.com).

No hay ningún «IVA incluido» en la landing. El único «IVA no incluido» está en la guía
(`es/la-portada-el-hoy-las-alertas-y-las-ultimas-semanas.json` y sus equivalentes `en`/`pt`) y es
**correcto**: habla de la estimación de cuota del panel, que va sin IVA. No se toca.

Las sanciones de la Inspección (751 € a 7.500 €, en la FAQ y en
`registro-horario-obligatorio-en-espana.json`) y la columna «Coste material (€)» de la guía no son
precios de CheckBiz360: no se tocan.

#### 1.1 Portada — español (`src/i18n/content.es.ts`)

| Línea | Clave | Texto actual | Texto propuesto |
|---|---|---|---|
| 78 | `hero.footnote` | `Desde 2 €/empleado al mes · 15 días de prueba · Puesta en marcha y formación incluidas` | `Desde 2 € + IVA por empleado al mes · 15 días de prueba · Puesta en marcha y formación incluidas` |
| 637 | `pricing.headlineBefore` | `5 €` | sin cambio — **pendiente de confirmar por Jose** (tarifa 2027) |
| 638 | `pricing.headline` | `2 €` | `2 €` (sin cambio: lo comprueba `assertTariff`, ver 1.6) |
| 639 | `pricing.headlineNote` | `por empleado al mes` | `+ IVA por empleado al mes` |
| 665 | `pricing.offerLock` | `Contrata por 2 € por empleado al mes hasta el 31 de diciembre de 2026 incluido, y conserva tu tarifa. Desde el 01/01/2027, las nuevas contrataciones tendrán una tarifa de 5 €.` | `Contrata por 2 € + IVA por empleado al mes hasta el 31 de diciembre de 2026 incluido, y conserva tu tarifa. Desde el 01/01/2027, las nuevas contrataciones tendrán una tarifa de 5 € + IVA.` (segunda frase **pendiente de confirmar por Jose**) |
| 683 | `pricing.plans[0].price` | `2 €` | `2 €` |
| 684 | `pricing.plans[0].priceBefore` | `5 €` | sin cambio — **pendiente de confirmar por Jose** |
| 685 | `pricing.plans[0].priceNote` | `por empleado al mes` | `+ IVA por empleado al mes` |
| 833 | `faq` «¿Cuánto cuesta y qué incluye la puesta en marcha?» | `La tarifa 2026 del plan Bronce es de 2 € por empleado y mes, […] Desde el 01/01/2027 las nuevas contrataciones tendrán una tarifa de 5 €. […]` | `La tarifa 2026 del plan Bronce es de 2 € + IVA por empleado y mes, […] Desde el 01/01/2027 las nuevas contrataciones tendrán una tarifa de 5 € + IVA. […]` y, al final, una frase: `Todos los precios son más IVA, desglosado en la factura.` |

Opcional, solo en español y si cabe en el diseño: una línea en `pricing.trial` (o junto a
`reviewNote`) que diga `Precios más IVA (21 %), desglosado en la factura.` Enséñala como opción.

#### 1.2 Portada — inglés (`src/i18n/content.en.ts`)

| Línea | Clave | Texto actual | Texto propuesto |
|---|---|---|---|
| 22 | `hero.footnote` | `From €2 per employee/month · 15-day trial · Onboarding and training included` | `From €2 + VAT per employee/month · 15-day trial · Onboarding and training included` |
| 521 | `pricing.headlineBefore` | `€5` | sin cambio — **pendiente de confirmar por Jose** |
| 522 | `pricing.headline` | `€2` | `€2` |
| 523 | `pricing.headlineNote` | `per employee per month` | `+ VAT per employee per month` |
| 526 | `pricing.offerLock` | `Subscribe at €2 per employee per month […] From 01/01/2027, new subscriptions will be charged €5.` | `Subscribe at €2 + VAT per employee per month […] From 01/01/2027, new subscriptions will be charged €5 + VAT.` (segunda frase pendiente de Jose) |
| 534–536 | `pricing.plans[0]` `price` / `priceBefore` / `priceNote` | `€2` / `€5` / `per employee per month` | `€2` / `€5` (pendiente) / `+ VAT per employee per month` |
| 680 | `faq` «How much does it cost…» | `The 2026 rate for the Bronze plan is €2 per employee per month, […] charged €5. […]` | `The 2026 rate for the Bronze plan is €2 + VAT per employee per month, […] charged €5 + VAT. […]` + `All prices exclude VAT, which is shown separately on the invoice.` |

#### 1.3 Portada — portugués (`src/i18n/content.pt.ts`)

| Línea | Clave | Texto actual | Texto propuesto |
|---|---|---|---|
| 23 | `hero.footnote` | `Desde 2 €/colaborador por mês · 15 dias de teste · Arranque e formação incluídos` | `Desde 2 € + IVA por colaborador por mês · 15 dias de teste · Arranque e formação incluídos` |
| 521 | `pricing.headlineBefore` | `5 €` | sin cambio — **pendiente de confirmar por Jose** |
| 522 | `pricing.headline` | `2 €` | `2 €` |
| 523 | `pricing.headlineNote` | `por colaborador por mês` | `+ IVA por colaborador por mês` |
| 526 | `pricing.offerLock` | `Subscreva por 2 € por colaborador por mês […] terão uma tarifa de 5 €.` | `Subscreva por 2 € + IVA por colaborador por mês […] terão uma tarifa de 5 € + IVA.` (segunda frase pendiente de Jose) |
| 534–536 | `pricing.plans[0]` | `2 €` / `5 €` / `por colaborador por mês` | `2 €` / `5 €` (pendiente) / `+ IVA por colaborador por mês` |
| 681 | `faq` «Quanto custa e o que inclui o arranque?» | `A tarifa 2026 do plano Bronze é de 2 € por colaborador por mês, […] tarifa de 5 €. […]` | `A tarifa 2026 do plano Bronze é de 2 € + IVA por colaborador por mês, […] tarifa de 5 € + IVA. […]` + `Todos os preços acrescem de IVA, discriminado na fatura.` |

#### 1.4 Landing SAD (`src/sad/content.*.ts`)

| Fichero:línea | Clave | Texto actual | Texto propuesto |
|---|---|---|---|
| `content.es.ts:103` | `hero.pricing` | `Tarifa 2026: 2 €/empleado al mes contratando hasta el 31/12/2026 incluido. Conservas tu tarifa.` | `Tarifa 2026: 2 € + IVA por empleado al mes contratando hasta el 31/12/2026 incluido. Conservas tu tarifa.` |
| `content.en.ts:50` | ídem | `2026 rate: €2 per employee/month, subscribing up to and including 31/12/2026. You keep your rate.` | `2026 rate: €2 + VAT per employee/month, subscribing up to and including 31/12/2026. You keep your rate.` |
| `content.pt.ts:51` | ídem | `Tarifa 2026: 2 €/colaborador por mês, subscrevendo até 31/12/2026 inclusive. Mantém a sua tarifa.` | `Tarifa 2026: 2 € + IVA por colaborador por mês, subscrevendo até 31/12/2026 inclusive. Mantém a sua tarifa.` |

#### 1.5 Landing «campo» (`src/campo/content.ts`, solo español)

| Línea | Clave | Texto actual | Texto propuesto |
|---|---|---|---|
| 103 | `hero.price` | `Tarifa 2026: 2 € por empleado al mes contratando hasta el 31/12/2026.` | `Tarifa 2026: 2 € + IVA por empleado al mes contratando hasta el 31/12/2026.` |
| 514 | `faq` (pregunta) | `¿Inventario está incluido en los 2 € por empleado?` | `¿Inventario está incluido en los 2 € + IVA por empleado?` |

El bloque de precio de «campo» (`src/campo/sections/CampoPricing.tsx`) **no tiene textos propios**:
pinta `headlineBefore`, `headline`, `headlineNote`, `offerLock` y `trial` del diccionario español de
la portada. Al cambiar 1.1 queda cambiado. Compruébalo en pantalla.

El resto de landings (`limpieza`, `construccion`, `cuadrantes`, `eventos`, `asistente`,
`inventario`) no publican importes: dicen «se contrata aparte» o «el precio vigente está en el
panel». No hay nada que cambiar ahí.

#### 1.6 Marcado para buscadores (`src/entry-server.tsx`, `src/seo/structuredData.ts`, `src/data/tariff.ts`)

**Cómo se construye el `Offer`.** `softwareApplication()` en `src/seo/structuredData.ts:123-166`
declara un `Offer` con `price: String(TARIFF.price)` (= `"2"`), `priceCurrency: 'EUR'`,
`priceValidUntil: '2026-12-31'` y un `UnitPriceSpecification` con el mismo precio y
`unitText: 'employee/month'`. Las cifras salen de `src/data/tariff.ts`, no de los textos.
La landing de eventos e `inventario` no declaran `Offer` (a propósito, ver comentarios en
`entry-server.tsx:565-580` y `:712`).

**La comprobación.** `assertTariff()` (`src/entry-server.tsx:137-164`) se ejecuta al construir y
revienta el build si el texto visible no anuncia el importe de `TARIFF`. Mira **solo cuatro textos**:
`pricing.headline` de cada idioma (es, en, pt) y `CAMPO.hero.price`. El patrón es

```ts
new RegExp(`(?<![\\d.,])${TARIFF.price}\\s?€|€\\s?${TARIFF.price}(?![\\d.,])`)
```

es decir, busca «2 €» o «€2» en cualquier parte del texto, sin que vaya pegado a otra cifra.

**¿Lo rompe el «+ IVA»? No**, con lo propuesto arriba:

- `pricing.headline` se queda en `2 €` / `€2`: pasa igual que hoy.
- Si prefirieses meter el IVA en el titular (`2 € + IVA`, `€2 + VAT`), también pasa: «2 €» sigue
  dentro y lo que va detrás («␣+») no es dígito.
- `Tarifa 2026: 2 € + IVA por empleado…` (campo) pasa: contiene «2 €».
- Lo que **sí** rompería: escribir el importe con IVA ya sumado (`2,42 €`) o sin el símbolo
  (`2 euros`, `2 EUR`). Sin espacio (`2€ + IVA`) sigue pasando.

**Lo que se propone en el marcado:** añadir `valueAddedTaxIncluded: false` al
`priceSpecification` (propiedad de schema.org de `PriceSpecification`), para que el `Offer` diga lo
mismo que la página: 2 € sin IVA. Una línea en `structuredData.ts`, sin tocar `TARIFF`.
`TARIFF.listPrice` (5) y `TARIFF.validUntil` (2026-12-31) pertenecen a la tarifa 2027:
**no se tocan, pendientes de confirmar por Jose**. Ojo: `priceValidUntil` hace que el `Offer`
caduque el 31-dic; es una consecuencia de esa misma decisión pendiente.

Después de cambiar: `npm run build` y mira que `assertTariff` no protesta y que el JSON-LD de
`dist/` lleva `valueAddedTaxIncluded: false`.

#### 1.7 La guía de ayuda (`src/docs/content/bodies/{es,en,pt}/*.json`)

**La guía no se edita a mano.** Esos JSON los genera `npm run docs:import`
(`scripts/import-docs.js`) a partir de `PLATAFORMA/DOCS/Clients` (es), `Clients-en` y `Clients-pt`,
y se commitean. Lo que se arregle a mano en el JSON se pierde en la siguiente importación.
La última importación es del 4-nov (`0a28b07`), anterior al IVA. Hoy dice, por ejemplo:

| Artículo de la guía (es / en / pt) | Lo que dice hoy |
|---|---|
| `planes-y-funcionalidades` / `plans-and-features` / `planos-e-funcionalidades` | Bronce **«5 €/empleado al mes»** en la tabla de planes y en la comparativa, «2 €/empleado al mes» en la nota de tarifa 2026, punto de fichaje «19 € al mes» y «0,90 € al mes», almacenamiento «0,25 €»: todo sin IVA |
| `preguntas-frecuentes` / `frequently-asked-questions` / `perguntas-frequentes` | «El plan Bronce se factura por empleado y mes, **5 €**, con una tarifa 2026 de 2 €…» y la nota «Los precios de referencia… *5 €/empleado al mes*… *2 €/empleado al mes*» |
| `glosario` / `glossary` / `glossario` | «Bronce, 5 €/empleado al mes (tarifa 2026 de 2 €…)» y almacenamiento «0,25 € al mes» |
| `punto-de-fichaje` / `clock-in-point` / `ponto-de-registo` | «19 € al mes», «0,90 € al mes» |

El manual español **ya está corregido** en `dc69a5e` (`Clients/14-referencia/91-planes-y-funcionalidades.md`
dice «2 € + IVA por empleado al mes», «29 € + IVA», «19 € + IVA», «0,25 € + IVA» y la nota del IVA).
El español se arregla, por tanto, **reimportando**. Ver la sección 3 para el cuándo y el cómo,
porque inglés y portugués aún no están listos.

---

## 2. Prioridad 2 — lo que ha llegado al producto y la landing no cuenta

Todo lo de esta sección está **en producción** desde el pase del 11-nov-2026 (alertas por correo,
desde el 28/29-oct). Las partes que se hacen desde el móvil (subir un ticket de gasto, aceptar una
jornada corregida, la tarjeta del cliente en la tarea) necesitan la última versión de la app; el
manual lo indica en cada artículo. Fuente de cada una: el artículo del manual citado.

La portada se reparte así, para orientarte: problema (`problem`, `content.es.ts:141`), pilares
(`pillars`, `:167`; sus títulos alimentan también el `featureList` del marcado), cómo funciona
(`howItWorks`, `:249`), cumplimiento (`compliance`, `:495`), lista de lo incluido en Bronce
(`pricing.plans[0].groups`, desde `:687`) y FAQ (`faq`, `:767`). En inglés y portugués, las mismas
claves en `content.en.ts` / `content.pt.ts`.

### 2.1 Cartera de clientes: contratos, rentabilidad y gastos

**Qué es.** Cada tarea queda atada a su cliente: ficha del cliente con sus contactos y documentos,
contratos con importe y horas que comparan lo cobrado con lo que van costando las horas y los gastos,
y un parte en PDF o Excel con las tareas, las horas y las fotos para mandárselo al cliente. Va
incluida en CheckBiz360, sin contratar nada.

**Por qué le importa al cliente.**
- «Sepa qué clientes le dejan dinero y cuáles le cuestan, con las horas y los gastos reales, no a ojo.»
- «Vea venir el contrato que se pasa de horas antes de que se coma el margen.»
- «Su equipo llega sabiendo dónde están las llaves y a quién llamar, sin repartir los datos de su cliente.»
- «Mándele a su cliente lo que se le ha hecho, con fotos, en un clic.»

**Dónde encaja.**
- Es lo más nuevo y lo de más valor: merece un **pilar propio o un bloque** después de `pillars`
  (`content.es.ts:167-202`), al estilo del bloque `pillars.inventory`, pero sin la etiqueta de
  complemento de pago porque va incluida. Alternativa más barata: ampliar el pilar 04 «Datos para
  decidir dónde actuar» (`:197`) con rentabilidad por cliente.
- Un **grupo nuevo en la lista de Bronce**, «Clientes y rentabilidad» (`pricing.plans[0].groups`,
  junto a `:701` «Gestión de tareas»).
- Una **pregunta nueva en la FAQ** (`faq`, `:767`): «¿Puedo saber qué clientes me salen rentables?».
  En la respuesta, con honradez: el coste sale de la tarifa horaria de cada persona; sin ella, las
  horas se cuentan pero no cuestan.
- Una **tarjeta en `problem`** (`:141`): hoy hay cuatro preguntas («¿Con quién cuento hoy?», etc.);
  encaja «¿Este cliente nos sale a cuenta?».
- Fuera de la portada: `src/sad/content.*.ts` (el cliente es la persona atendida en su casa) y
  `src/campo/content.ts` (equipos en campo) son buenos sitios para la frase de las llaves.

**Cuidado.** El contrato se puede leer con IA desde el PDF: si lo nombras, di que la IA propone y la
persona revisa, y no prometas nada sobre lo que se envía fuera. El **Portal del cliente está pendiente
de desarrollo**: no se anuncia (ni «su cliente podrá entrar a ver…»). Lo que existe es el **parte**
que usted le manda.

Fuente: `DOCS/Clients/17-cartera-de-clientes/117-que-es-la-cartera-de-clientes.md` a `123-el-cliente-en-los-analisis.md`
(sobre todo 117, 121 «Contratos y rentabilidad», 122 «Gastos del contrato y de la tarea» y 123 «El cliente en los análisis»).

### 2.2 Incidencia en la tarea

**Qué es.** Si algo impide hacer el trabajo (no abren la puerta, falta material, el cliente anula),
quien estaba allí lo marca desde la app con una nota y, si quiere, una foto; la dirección se entera al
momento por correo y en el panel, y decide si se replanifica, se cancela o se da por resuelta.

**Por qué le importa al cliente.** «Si algo impide hacer el trabajo, se entera al momento, con la foto
de quien estaba allí, y no al día siguiente.»

**Dónde encaja.** Pilar 02 «Trabajo que puedes revisar» (`content.es.ts:183-188`, ya lleva la etiqueta
«Incidencias»: el texto del pilar puede decirlo); lista de Bronce, grupo «Gestión de tareas»
(`:701-711`), una línea nueva. Ojo: la línea «Sistema de tickets para incidencias, reportes y
comunicación directa» del grupo de registro (`:696`) es otra cosa (el canal de contacto); no
la reutilices para esto.

Fuente: `DOCS/Clients/06-tareas/125-incidencia-en-la-tarea.md`.

### 2.3 Aviso de tarea sin empezar a los 5 minutos

**Qué es.** Si una tarea con hora prevista no se ha iniciado a los 5 minutos, la persona recibe un
recordatorio en la app y el propietario y los administradores un correo (varias tareas, un solo
correo), y la tarea aparece en Inicio.

**Por qué le importa al cliente.** «A los cinco minutos sabe qué visita no ha empezado, a tiempo de
llamar antes de que lo note su cliente.»

**Dónde encaja.** Ya hay una línea en Bronce: `content.es.ts:708` «Aviso automático cuando una tarea
no arranca a su hora.» (en `:559` de `en` y `pt`). Se concreta: «Aviso a los 5 minutos si una tarea
no arranca a su hora, en el móvil y por correo.» La fila «Saber cómo va el día» de `adminTime`
(`:468`) ya habla de «qué tarea no ha empezado»: no hace falta más.

Fuente: `DOCS/Clients/06-tareas/126-tarea-sin-empezar-a-su-hora.md`.

### 2.4 Quién termina la tarea y cierre desde administración

**Qué es.** En una tarea de varias personas se elige quién la da por terminada (basta una, todas, o
una persona responsable); y si el trabajo se hizo pero nadie la cerró en la app, la dirección la
cierra desde el panel con su hora de inicio y de cierre, y queda dicho que se cerró desde
administración.

**Por qué le importa al cliente.** «Cada tarea dice quién la cerró, cuándo y cómo, aunque se cerrase
en la oficina: sus informes salen completos.»

**Dónde encaja.** Lista de Bronce, «Gestión de tareas» (`:701-711`): ampliar «Tareas con ubicación
propia, pausas e historial de ejecución» o añadir una línea. Es un detalle, no un titular.

Fuente: `DOCS/Clients/06-tareas/127-quien-termina-la-tarea-y-cierre-desde-administracion.md`.

### 2.5 Alertas por correo

**Qué es.** Cada mañana (a la hora que se elija, entre las 6:00 y las 10:00) el propietario y los
administradores reciben un correo con lo que pide su atención —jornadas que quedaron abiertas,
tareas vencidas, días con poca gente, hojas informativas sin firmar—, lo urgente llega al momento, y
si no hay nada nuevo no se envía nada. Viene activado para todas las empresas.

**Por qué le importa al cliente.** «Empiece cada mañana sabiendo qué mirar: lo que pide su atención le
llega por correo antes del café, y si no hay nada nuevo, no le escribimos.»

**Dónde encaja.** Hoy la landing no lo menciona en ningún sitio. Pilar 04 «Datos para decidir dónde
actuar» (`:197-201`) o el paso 03 de `howItWorks` «Revisa y decide» (`:264`); y una línea en Bronce,
grupo «Análisis y control de rendimiento» (`:723`).

Fuente: `DOCS/Clients/09-notificaciones/133-alertas-por-correo.md`.

### 2.6 Corregir una jornada de una vez

**Qué es.** Cuando una jornada partida queda mal fichada, el responsable la corrige entera en una
pantalla, con un solo motivo, y el trabajador recibe un solo aviso para aceptarla o rechazarla desde
el móvil; hasta que no acepta, no cambia nada.

**Por qué le importa al cliente.** «Una jornada partida mal fichada se arregla en un minuto: una
corrección, un motivo y un solo sí del trabajador desde su móvil.»

**Dónde encaja.** Las dos FAQ que ya hablan de esto: «¿Puede mi responsable cambiarme las horas que
he fichado?» (`content.es.ts:801`) y «¿Qué pasa si un empleado olvida fichar o se queda sin
cobertura?» (`:806`). Basta una frase en la segunda. En `compliance.table` (`:508`) ya existe
«Corrección con motivo».

Fuente: `DOCS/Clients/03-control-horario/134-corregir-una-jornada-incompleta.md`.

### 2.7 Documentos solo para Administración y eliminar documentos

**Qué es.** Un documento se puede marcar para que solo lo vean el propietario y los administradores
desde el panel (contratos, presupuestos, papeles de dirección), y el documento personal de una
persona solo lo ven ella y la dirección. Y los documentos se pueden **eliminar de verdad**, uno o
varios a la vez, liberando espacio al momento, conservando el registro de quién lo recibió, quién lo
firmó y quién lo eliminó.

**Por qué le importa al cliente.** «Pague solo por el espacio que usa: elimine lo que ya no necesita y
conserve igualmente la prueba de quién lo recibió.» (Y, para lo de Administración: los papeles de
dirección no los ve el encargado.)

**Dónde encaja.** Lista de Bronce, «Gestión documental» (`content.es.ts:713-720`):
- `:716` «Visibilidad por rol: trabajador, supervisor o responsable.» → hoy se queda corta; añadir
  «o solo administración».
- `:718` «Fecha de caducidad, archivado, búsqueda y filtros.» → añadir «y eliminación con
  registro de quién lo recibió».
Pilar 03 «Documentos y firma desde el móvil» (`:190-195`) si cabe.
Si se habla de espacio, las cifras son las de la sección 1 (2 GB incluidos, 0,25 € + IVA por GB de
más); no lo pongas sin enseñárselo a Jose, porque hoy la landing no publica precio de almacenamiento.

Fuente: `DOCS/Clients/05-gestion-documental/135-eliminar-documentos.md` y `136-quien-ve-cada-documento.md`.

### 2.8 Hoja informativa de protección de datos

**Qué es.** CheckBiz360 prepara la hoja informativa de protección de datos con los datos de la
empresa, se la manda a cada persona al darla de alta para que la firme desde la app, y guarda la
prueba (quién, cuándo, con su acta); la lista de empleados dice quién falta y hay una alerta para ello.

**Por qué le importa al cliente.** «Cumpla con la protección de datos sin papeleo: cada persona firma
su hoja informativa desde la app y usted guarda la prueba.»

**Dónde encaja.** Sección `compliance` (`content.es.ts:495-516`): una fila más en la tabla
(«Información de protección de datos firmada» — Excel/papel «A mano» — CheckBiz360 «Desde la app»)
o una frase en `compliance.body`. Y la FAQ «¿Es legal fichar con geolocalización?» (`:796`), que ya
dice «siempre que… el trabajador esté informado»: es el sitio natural para decir cómo se le informa.

**Cuidado.** Firmar la hoja **no es dar un consentimiento**: es dejar constancia de que se recibió la
información. No uses «consentimiento» para esto. La empresa puede usar su propia
hoja en lugar de la de CheckBiz360 (en producción desde el 11-nov: Entidad → Protección de datos → «Subir
hoja propia (PDF)»); se puede anunciar.

Fuente: `DOCS/Clients/12-cumplimiento-normativo/137-hoja-informativa-de-proteccion-de-datos.md`.

---

## 3. La guía de ayuda: qué hay que reimportar

La guía (`src/docs/content/…`) se genera desde el manual con `npm run docs:import`
(`scripts/import-docs.js`; lee `../DOCS` por defecto o `DOCS_SOURCE`). El slug de cada artículo es el
nombre del fichero del manual sin el número, así que la correspondencia es directa.

### Estado de las fuentes (13-nov)

- **Español (`DOCS/Clients`)**: al día y commiteado en `dc69a5e`.
- **Inglés (`DOCS/Clients-en`) y portugués (`DOCS/Clients-pt`)**: al día y commiteados el 13-nov
  (`a0adf63` y `6093ffd`), con los precios en «+ VAT» / «+ IVA». Los tres idiomas están completos.
- El importador hace **los tres idiomas de una vez** y lee **el árbol de trabajo**, no el último commit.

**Qué hacer:** antes de importar, `git -C ../DOCS status --short -- Clients Clients-en Clients-pt`.
Si sale algo, **no importes**: díselo a Jose y espera a que la traducción esté commiteada. Si Jose
quiere el español ya, la vía es importar desde una copia limpia de `DOCS` en el commit bueno
(`DOCS_SOURCE=<copia> npm run docs:import`), con su OK, porque supone crear esa copia fuera del repo
de la landing. Después de importar: `git diff --stat src/docs/content` y `npm run build`.

No edites los JSON a mano para adelantarte: la siguiente importación lo pisa.

### Artículos que cambian (manual → guía)

Artículos **nuevos** (no existen hoy en la guía; los crea la importación):

| Manual (fuente) | Guía es | en | pt |
|---|---|---|---|
| `Clients/17-cartera-de-clientes/117-que-es-la-cartera-de-clientes.md` | `que-es-la-cartera-de-clientes` (sección nueva 17) | traducción en curso | falta |
| `Clients/17-cartera-de-clientes/118-dar-de-alta-clientes.md` | `dar-de-alta-clientes` | en curso | falta |
| `Clients/17-cartera-de-clientes/119-el-cliente-en-la-tarea.md` | `el-cliente-en-la-tarea` | en curso | falta |
| `Clients/17-cartera-de-clientes/120-documentos-del-cliente.md` | `documentos-del-cliente` | en curso | falta |
| `Clients/17-cartera-de-clientes/121-contratos-y-rentabilidad.md` | `contratos-y-rentabilidad` | falta | falta |
| `Clients/17-cartera-de-clientes/122-gastos-del-contrato-y-de-la-tarea.md` | `gastos-del-contrato-y-de-la-tarea` | falta | falta |
| `Clients/17-cartera-de-clientes/123-el-cliente-en-los-analisis.md` | `el-cliente-en-los-analisis` | falta | falta |
| `Clients/06-tareas/125-incidencia-en-la-tarea.md` | `incidencia-en-la-tarea` | en curso | falta |
| `Clients/06-tareas/126-tarea-sin-empezar-a-su-hora.md` | `tarea-sin-empezar-a-su-hora` | en curso | falta |
| `Clients/06-tareas/127-quien-termina-la-tarea-y-cierre-desde-administracion.md` | `quien-termina-la-tarea-y-cierre-desde-administracion` | en curso | falta |
| `Clients/09-notificaciones/133-alertas-por-correo.md` | `alertas-por-correo` | en curso | falta |
| `Clients/03-control-horario/134-corregir-una-jornada-incompleta.md` | `corregir-una-jornada-incompleta` | en curso | en curso |
| `Clients/05-gestion-documental/135-eliminar-documentos.md` | `eliminar-documentos` | falta | en curso |
| `Clients/05-gestion-documental/136-quien-ve-cada-documento.md` | `quien-ve-cada-documento` | falta | en curso |
| `Clients/12-cumplimiento-normativo/137-hoja-informativa-de-proteccion-de-datos.md` | `hoja-informativa-de-proteccion-de-datos` | falta | falta |

Artículos que **ya están en la guía y han cambiado** (se actualizan al reimportar):

| Manual (fuente) | Guía es | en | pt | Qué cambia, en corto |
|---|---|---|---|---|
| `Clients/14-referencia/91-planes-y-funcionalidades.md` | `planes-y-funcionalidades` | `plans-and-features` | `planos-e-funcionalidades` | **Precios + IVA**; Bronce a 2 €; inventario 29 €/0,75 €; nota del IVA |
| `Clients/14-referencia/92-preguntas-frecuentes.md` | `preguntas-frecuentes` | `frequently-asked-questions` | `perguntas-frequentes` | **Precios + IVA** |
| `Clients/14-referencia/89-glosario.md` | `glosario` | `glossary` | `glossario` | **Precios + IVA** |
| `Clients/03-control-horario/113-punto-de-fichaje.md` | `punto-de-fichaje` | `clock-in-point` | `ponto-de-registo` | **Precios + IVA** |
| `Clients/06-tareas/40-crear-una-tarea.md` | `crear-una-tarea` | `create-a-task` | `criar-uma-tarefa` | Aviso de inicio a los **5 min** (la guía dice 15), cliente, terminación, adjuntos |
| `Clients/06-tareas/47-notificaciones-de-tareas.md` | `notificaciones-de-tareas` | `task-notifications` | `notificacoes-de-tarefas` | 5 min (la guía dice 15); incidencia |
| `Clients/06-tareas/44-prioridades-y-fechas-limite.md` | `prioridades-y-fechas-limite` | `priorities-and-deadlines` | `prioridades-e-prazos` | 5 min (la guía dice 15) |
| `Clients/06-tareas/43-seguimiento-y-actualizaciones.md` | `seguimiento-y-actualizaciones` | `tracking-and-updates` | `acompanhamento-e-atualizacoes` | 5 min (la guía dice 15); incidencia |
| `Clients/09-notificaciones/65-configurar-preferencias-de-notificacion.md` | `configurar-preferencias-de-notificacion` | `configure-notification-preferences` | `configurar-preferencias-de-notificacao` | 5 min (la guía dice 15) |
| `Clients/09-notificaciones/68-notificaciones-por-email.md` | `notificaciones-por-email` | `email-notifications` | `notificacoes-por-email` | La guía dice «Alertas operativas por correo: **pendiente de desarrollo**»; están en producción |
| `Clients/09-notificaciones/63-tipos-de-notificacion.md` | `tipos-de-notificacion` | `notification-types` | `tipos-de-notificacao` | Alertas por correo |
| `Clients/09-notificaciones/66-alertas-para-responsables.md` | `alertas-para-responsables` | `alerts-for-managers` | `alertas-para-responsaveis` | Alertas nuevas |
| `Clients/06-tareas/39-que-es-el-modulo-de-tareas.md` | `que-es-el-modulo-de-tareas` | `what-is-the-tasks-module` | `o-que-e-o-modulo-de-tarefas` | Incidencia, cliente |
| `Clients/06-tareas/41-asignar-tareas-a-empleados.md` | `asignar-tareas-a-empleados` | `assign-tasks-to-employees` | `atribuir-tarefas-a-funcionarios` | Quién termina la tarea |
| `Clients/06-tareas/42-estados-de-una-tarea.md` | `estados-de-una-tarea` | `task-statuses` | `estados-de-uma-tarefa` | Incidencia y cierre desde administración |
| `Clients/06-tareas/48-informes-de-tareas.md` | `informes-de-tareas` | `task-reports` | `relatorios-de-tarefas` | Incidencias y cierre en el informe |
| `Clients/03-control-horario/20-revision-y-validacion-de-fichajes.md` | `revision-y-validacion-de-fichajes` | `reviewing-and-approving-clock-records` | `revisao-e-validacao-de-registos` | Corregir la jornada de una vez |
| `Clients/03-control-horario/22-estados-y-codigos-de-error.md` | `estados-y-codigos-de-error` | `statuses-and-error-codes` | `estados-e-codigos-de-erro` | Retoque |
| `Clients/05-gestion-documental/30-que-es-el-modulo-documental.md` | `que-es-el-modulo-documental` | `what-is-the-document-module` | `o-que-e-o-modulo-documental` | Eliminar y Administración |
| `Clients/05-gestion-documental/31-subir-y-organizar-documentos.md` | `subir-y-organizar-documentos` | `upload-and-organise-documents` | `carregar-e-organizar-documentos` | Nivel Administración |
| `Clients/05-gestion-documental/33-documentos-privados.md` | `documentos-privados` | `private-documents` | `documentos-privados` | Eliminar |
| `Clients/05-gestion-documental/37-permisos-de-acceso-documental.md` | `permisos-de-acceso-documental` | `document-access-permissions` | `permissoes-de-acesso-documental` | Tabla de permisos nueva |
| `Clients/07-inteligencia-operativa/112-la-portada-el-hoy-las-alertas-y-las-ultimas-semanas.md` | `la-portada-el-hoy-las-alertas-y-las-ultimas-semanas` | `the-home-page-today-alerts-and-recent-weeks` | `a-pagina-inicial-o-hoje-os-alertas-e-as-ultimas-semanas` | Bloque Clientes, alertas nuevas |
| `Clients/07-inteligencia-operativa/51-indice-de-fiabilidad.md` | `indice-de-fiabilidad` | `reliability-index` | `indice-de-fiabilidade` | Retoque |
| `Clients/07-inteligencia-operativa/55-deteccion-de-anomalias.md` | `deteccion-de-anomalias` | `anomaly-detection` | `detecao-de-anomalias` | Retoque |
| `Clients/07-inteligencia-operativa/56-paneles-de-mando.md` | `paneles-de-mando` | `dashboards` | `paineis-de-controlo` | Cliente en los paneles |
| `Clients/08-sucursales-y-entidad/59-estados-de-una-sucursal.md` | `estados-de-una-sucursal` | `branch-statuses` | `estados-de-uma-sucursal` | Borrar sucursal con tareas abiertas |
| `Clients/08-sucursales-y-entidad/61-configuracion-de-entidad.md` | `configuracion-de-entidad` | `organisation-settings` | `configuracao-da-entidade` | Datos de protección de datos |
| `Clients/11-informes-y-exportacion/76-tipos-de-informe.md` | `tipos-de-informe` | `report-types` | `tipos-de-relatorio` | Parte del cliente |
| `Clients/11-informes-y-exportacion/77-generar-y-filtrar-informes.md` | `generar-y-filtrar-informes` | `generate-and-filter-reports` | `gerar-e-filtrar-relatorios` | Parte del cliente |
| `Clients/12-cumplimiento-normativo/83-conservacion-y-proteccion-de-datos.md` | `conservacion-y-proteccion-de-datos` | `data-retention-and-protection` | `conservacao-e-protecao-de-dados` | Hoja informativa |
| `Clients/12-cumplimiento-normativo/84-preparar-una-inspeccion-de-trabajo.md` | `preparar-una-inspeccion-de-trabajo` | `preparing-for-a-labour-inspection` | `preparar-uma-inspecao-do-trabalho` | Hoja informativa |
| `Clients/16-inventario/100-que-es-el-inventario.md` | `que-es-el-inventario` | `what-is-inventory` | `o-que-e-o-inventario` | Precio + IVA |

La portada de la guía y el `index.*.json` pasan de 16 a 17 secciones. La importación los regenera;
mira que la sección nueva «Cartera de clientes» sale bien en el árbol y en el buscador.

---

## 4. Reglas que hay que respetar

1. **Tono de cliente y de beneficio.** Qué gana el cliente, no cómo funciona por dentro: nada de
   bases de datos, Stripe, triggers, colas, «sincronización», nombres de servicios ni de pantallas
   internas. Frases cortas, de usted o de tú según la página (la portada va de tú; las frases de venta
   de arriba van de usted: adáptalas al registro de cada página).
2. **Sin nombres reales de clientes.** Ni en textos, ni en capturas, ni en ejemplos. Las capturas,
   con datos de demostración.
3. **Sin prometer lo que no está en producción.** El **Portal del cliente** está pendiente de
   desarrollo: no se anuncia, ni de pasada. Tampoco lo que el manual marca «Pendiente de desarrollo»
   (turnos rotativos automáticos, historial persistente de notificaciones, descarga masiva de
   documentos…). Ante la duda, `DOCS/Clients/README.md` dice el estado de cada funcionalidad.
4. **Sin precios inventados.** Solo las cifras de la sección 1, siempre con «+ IVA». La tarifa de
   5 € desde 2027 se deja como está, **pendiente de confirmar por Jose**. No añadas a la landing precios
   que hoy no publica (inventario, punto de fichaje, almacenamiento) sin preguntarle.
5. **Nombrar lo observado.** Un aviso se describe por lo que mide («la tarea no ha empezado a los
   5 minutos»), no por una causa que no se conoce («el trabajador no ha ido»).
6. **La hoja informativa no es un consentimiento.** No uses esa palabra para ella.
7. **Publicar la landing en producción requiere el OK de Jose.** Prepara los cambios, enséñalos (diff
   y capturas o la página en local), y espera su sí. La guía, además, solo se reimporta cuando el
   manual de los tres idiomas esté commiteado (sección 3).

---

## 5. Prompt para pegar en la sesión de la landing

```
Lee /Users/joseacevedo/Documents/EncodeBiz-ALL/PLATAFORMA/DOCS/MARKETING/landing/2026-11-13-traspaso-landing.md
entero antes de tocar nada. Empieza por la prioridad 1 (precio «+ IVA» en todas partes): haz los
cambios de las secciones 1.1 a 1.6, deja la tarifa de 5 € desde 2027 como está y márcala como
pendiente de confirmar por mí, pasa `npm run build` y enséñame el diff y cómo queda la sección de
precios en es, en y pt antes de publicar nada. Después, reimporta la guía (sección 3: primero comprueba que el manual
no tiene cambios sin commitear) y no publiques en producción sin mi OK. Cuando yo dé el visto bueno al precio, seguimos con la
prioridad 2.
```

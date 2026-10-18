# Almacenamiento por empresa — cuota, packs y retención · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** transversal — Storage de la plataforma (quiosco, documental, tareas, firma) × `billing`
**Fecha de inicio:** 2026-10-18
**Estado:** Diseño cerrado el 2026-10-18 · sin implementar. Nace del quiosco
([quiosco/README](../quiosco/README.md)) y lo necesita antes de su Fase 1.
**Autor:** Jose Acevedo

---

## De dónde sale

Jose, 2026-10-18, al cerrar que cada fichaje del quiosco lleva una foto: «un tema técnico muy
importante: espacio en Storage, ya que sería infinito. Por tanto tenemos que hacer una
configuración de entidad donde compres espacio, que al menos cubra los precios de Firebase».

Hoy nadie cuenta lo que cada empresa ocupa. El documental, las tareas con foto, la evidencia y
las actas de firma y los informes escriben en el bucket por defecto del proyecto, cada uno con
su prefijo, sin cuota ni ciclo de vida. Con el quiosco, el volumen deja de depender de lo que
suba un administrador y pasa a crecer solo, cada día, con cada fichaje.

## Principio de diseño

> **El espacio es un dato de la suscripción, como los empleados: cada plan incluye una parte,
> el resto se compra en packs, y el exceso se factura, nunca se impide.** Un fichaje jamás
> falla porque la empresa no tenga espacio. Lo que acota el volumen no es la cuota sino la
> **retención**, que elige la empresa viendo lo que le va a costar.

Es la regla de la casa para los cupos (Jose, 2026-10-16: «no hay cupo», el exceso se factura;
`subscriptionLimits.ts`) aplicada al espacio, y encaja en el modelo de cobro de
[billing-v2/02](../billing-v2/02_to-be.md) sin una línea de código nueva en `billing`: packs
como add-on `flat`, exceso como `metered`.

Y una segunda regla, sin excepciones: **todo lo que se sube a Storage pasa por el contador**
(Jose, 2026-10-18: «todo lo que se suba debe tributar a este módulo contador de Storage para
poder vender espacio»). Ningún servicio escribe en el bucket por su cuenta; lo hace por el
helper de `shared`, que pone la ruta canónica y cuenta. Razones y cómo se hace cumplir en
[ADR-001](./adr/ADR-001-todo-lo-que-se-sube-pasa-por-el-contador.md).

## Los números, para saber de qué hablamos

Lo que cobra Google (bucket `*.firebasestorage.app`, tarifas de Cloud Storage; las cifras de
Firebase de referencia que pedía Jose son las del bucket clásico):

| Concepto | Firebase clásico (`appspot.com`) | Cloud Storage, región única (EU o US) |
|---|---|---|
| Almacenado | 0,026 $/GB-mes | 0,020-0,023 $/GB-mes (`europe-west1` 0,020) |
| Descargado a internet | 0,12 $/GB | ~0,12 $/GB primer tramo |
| Subidas (clase A) | 0,05 $/10.000 | 0,05 $/10.000 |
| Descargas (clase B) | 0,004 $/10.000 | 0,004 $/10.000 |

Cifras comprobadas el 2026-10-18 en la página de precios de Firebase; las de Cloud Storage
por región, de la página de precios de Google Cloud (confirmar en la calculadora antes de
fijar el precio de venta).

Lo que ocupa el quiosco, con los parámetros del diseño (JPEG de 640 px, unos **60 KB**; una
media de **3 fichajes al día** con foto —entrada, salida y una pausa—; 22 días al mes):

| | Por empleado | 100 empleados | 1.000 empleados (Serlimar) |
|---|---|---|---|
| Al mes | 4 MB | 0,4 GB | 4 GB |
| Stock con retención 30 días | 4 MB | 0,4 GB | 4 GB |
| Stock con retención 1 año | 48 MB | 4,8 GB | 48 GB |
| Stock con retención 4 años (la del registro de jornada) | 190 MB | 19 GB | 190 GB |
| Coste Google del stock a 4 años | — | 0,5 $/mes | 5 $/mes |

Es decir: **el coste real es pequeño; el problema es que no tiene techo**. Con retención de
30 días, mil personas ocupan 4 GB y cuestan 10 céntimos al mes. Con cuatro años, 190 GB. El
techo lo pone la retención, y la cuota es lo que hace que la empresa la elija con
conocimiento.

## Cómo se sabe cuánto consume cada empresa

> Jose, 2026-10-18: «sí, pero ¿cómo podemos saber cuánto consume cada empresa?» y «documéntalo
> porque esto es importante».

La respuesta corta: **porque la empresa va en la ruta de cada fichero y porque sólo el servidor
escribe.** Lo primero permite medir hoy, sin construir nada; lo segundo permite contar en vivo
mañana.

### Lo que se puede medir hoy, sin tocar código

Rutas comprobadas en el código el 2026-10-18 (todas escriben en el bucket por defecto del
proyecto, `encodebiz-services.firebasestorage.app` en producción):

| Módulo | Prefijo en el bucket | Se puede medir por empresa |
|---|---|---|
| Documental (ficheros y PDF firmados) | `documents/entities/{entityId}/…` | sí |
| Tareas (recursos y fotos de valoración) | `media/entities/{entityId}/checkinbiz/tasks/{taskId}/…` | sí |
| Firma (evidencia JSON) | `signatures/evidence/{entityId}/{purpose}/{challengeId}.json` | sí |
| Informes y actas | `checkbiz/reports/entities/{entityId}/…` | sí |
| Campañas in-app (imágenes) | `campaigns/images/{timestamp}-{uuid}.{ext}` | **no**: sin empresa en la ruta |
| Quiosco (cuando exista) | bucket `encodebiz-media-eu`, `kiosk/r{días}/{entityId}/{checklogId}.jpg` | sí, por diseño |

Con eso, hoy mismo, para una empresa:

```bash
B=gs://encodebiz-services.firebasestorage.app
E=<entityId>
gcloud storage du --summarize $B/documents/entities/$E/
gcloud storage du --summarize $B/media/entities/$E/
gcloud storage du --summarize $B/signatures/evidence/$E/
gcloud storage du --summarize $B/checkbiz/reports/entities/$E/
```

Y para todas de una vez, el total por empresa de cada prefijo:

```bash
gcloud storage du $B/documents/entities/ --summarize   # un total por subcarpeta = por empresa
```

Lo que hay que arreglar para que la medida sea completa: las imágenes de campañas tienen que
llevar la empresa en la ruta (`campaigns/entities/{entityId}/images/…`), con una migración de
lo existente (son pocas y las referencia el documento de la campaña).

### Lo que se construye para no tener que preguntar a Google

Tres capas, de la más barata a la más fiable. Las tres están en §Diseño; aquí, el porqué de
cada una:

1. **El contador en vivo (al escribir y al borrar).** Ningún fichero lo sube la app a Storage:
   lo sube el servidor (`getStorage().bucket().file().save` en documental y tareas, la evidencia
   de firma, el quiosco). Por eso cada subida puede sumar su tamaño a
   `entities/{entityId}.storage.usedBytes` y a `byModule.{módulo}` en la misma transacción, y
   cada borrado restar. Es lo que el panel enseña al instante y lo que dispara los avisos del
   80 % y el 100 %. Helper único en `shared` (`accountedUpload` / `accountedDelete`): un módulo
   que suba sin pasar por él es un error de revisión de código.
2. **La reconciliación nocturna.** El contador se desvía: las reglas de ciclo de vida borran sin
   avisarnos, una subida puede quedar a medias, un script de soporte puede borrar a mano. Cada
   noche un trabajo lista los prefijos de cada empresa (la tabla de arriba), suma los tamaños
   reales y reescribe `usedBytes` y `byModule`. Coste: una operación de listado por cada mil
   ficheros; mil empleados en el quiosco con 30 días son 90.000 fotos, 90 operaciones, nada.
   **Lo que se factura sale de este número**, nunca del contador en vivo.
3. **La instantánea diaria.** Tras reconciliar, `entities/{e}/storage_daily/{fecha}`. De ahí
   salen la gráfica de 90 días del panel y el **pico del ciclo**, que es la base del exceso: se
   cobra lo que más se ocupó, no lo que queda el último día.

Lo que no se hace, y por qué: no se consulta la facturación de Google por empresa (Google factura
por bucket y proyecto, no sabe qué es una empresa nuestra), y no se pone un bucket por empresa
(los buckets tienen límites de creación y las reglas de ciclo de vida se multiplicarían por
cliente). La empresa en la ruta es la unidad de medida, y la tabla de prefijos es el contrato.

## Diseño

### 1. Lo que se cuenta

`entities/{entityId}.storage`:

```text
{ usedBytes, byModule: { kiosk, documents, tasks, signatures, campaigns, reports }, includedGb,
  packsGb, updatedAt, lastReconciledAt }
```

- **Se cuenta todo** ([ADR-001](./adr/ADR-001-todo-lo-que-se-sube-pasa-por-el-contador.md)):
  fotos del quiosco, documentos del documental, evidencias de tareas, evidencia y actas de
  firma, imágenes de campañas, informes y exportaciones. Lo regenerable no queda exento: se le
  pone caducidad de 30 días en el bucket para que no pese, y mientras existe, cuenta.
- **Quién cuenta: el servidor, al escribir y al borrar.** Todos los módulos suben por el
  servidor (`getStorage().bucket().file().save` en el documental y en tareas; la evidencia de
  firma; el quiosco). Cada escritura suma `size` al contador de la empresa y del módulo en una
  transacción; cada borrado resta. Un helper en `shared` (`checkbiz/storage/`: `accountedUpload`,
  `accountedDelete`, `accountedDeletePrefix`) es **la única vía**: el CI falla si
  `getStorage().bucket()` aparece fuera de él (ADR-001). Los prefijos por módulo, en §Cómo se sabe.
- **Reconciliación nocturna.** Las reglas de ciclo de vida borran sin avisarnos y un contador
  en Firestore se desvía. Un trabajo diario lista los prefijos de cada empresa (`du` por prefijo:
  un listado por cada mil objetos, coste despreciable), reescribe `usedBytes` y `byModule` y
  apunta `lastReconciledAt`. El contador en vivo sirve para avisar; la verdad del mes es la
  reconciliada.
- **Instantánea diaria** `entities/{e}/storage_daily/{YYYY-MM-DD} = { usedBytes, byModule }`:
  de ahí sale el pico del ciclo para facturar el exceso y la gráfica del panel.

### 2. Lo que se incluye, lo que se compra y lo que se factura

- **Incluido por plan**: `service/checkinbiz/plan/{plan}.includedStorageGb`. Propuesta: 0,5 GB
  en freemium, 2 GB en los planes de pago (con retención de 30 días, 2 GB son ~500 empleados
  en el quiosco; lo normal es que no haga falta comprar nada).
- **Packs**, add-on `flat` sobre la suscripción de checkinbiz, exactamente como Rentman
  ([billing-v2/02 §Add-ons](../billing-v2/02_to-be.md)): `service/storage/plan/pack-10`,
  `pack-50`, `pack-200` con `billing: { kind: "flat", stripePrice }`. Alta de datos, sin código.
  Propuesta de precio, a cerrar con los Prices de Stripe:

  | Pack | €/mes | €/GB-mes | Margen sobre Google (0,026 $ almacenado + descarga) |
  |---|---|---|---|
  | 10 GB | 3 | 0,30 | ~10× |
  | 50 GB | 12 | 0,24 | ~8× |
  | 200 GB | 40 | 0,20 | ~7× |

  El margen no es avaricia: cubre descargas (0,12 $/GB cada vez que alguien mira todo lo que
  guardó), operaciones, la reconciliación diaria y el bucket europeo sin nivel gratuito.
- **Exceso**: lo que pase de `includedGb + packsGb` en el **pico** del ciclo se factura como
  uso medido (`metered`, el modelo de passinbiz), a **0,50 €/GB-mes**, redondeado hacia arriba,
  en la misma factura y en línea aparte. Nunca bloquea nada. El precio del exceso es más alto
  que el del pack a propósito: comprar el pack tiene que salir a cuenta.
- **Avisos** al administrador al 80 % y al 100 % de lo incluido más los packs (in-app y correo
  de `billing`), con la estimación de lo que costará el exceso y el botón de comprar pack.
  Tras el 100 %, uno al mes mientras siga en exceso.

### 3. La retención es el mando

Cada módulo que guarda ficheros «que crecen solos» tiene su retención por empresa; hoy sólo el
quiosco. `entities/{e}.settings.kiosk.photoRetention ∈ { 15, 30, 60, 90, 365, 1460 }` días
(1460 = 4 años, la retención del registro de jornada, art. 34.9 ET; más no tiene sentido).
Por defecto 30.

Al cambiarla, el panel enseña la cuenta hecha: «Con 240 empleados y 90 días, las fotos
ocuparán unos 2,9 GB. Tu plan incluye 2 GB; el exceso estimado es 0,9 GB (0,45 €/mes), o un
pack de 10 GB por 3 €/mes». La fórmula es la de la tabla de arriba; el panel la pinta, el
servidor la devuelve (`GET /storage/estimate?entityId&module=kiosk&retentionDays=`).

### 4. Cómo se borra solo: ciclo de vida por carpeta de retención

Las reglas de ciclo de vida son del bucket (máximo 100), no de la empresa. La ruta lleva la
retención dentro: `kiosk/r{días}/{entityId}/{checklogId}.jpg`, y el bucket tiene **una regla
por valor** (`matchesPrefix: ["kiosk/r30/"], age: 30`, y así las seis). Cambiar la retención
no mueve nada: las fotos nuevas van a la carpeta nueva y las viejas caducan con la suya.

Una foto **en disputa** (solicitud de corrección abierta o rechazada sobre ese fichaje) se copia
a `kiosk/hold/{entityId}/…` sin regla de caducidad, y el fichaje apunta a la copia; al cerrar
la disputa vuelve a contar el reloj (se mueve a su carpeta de retención con la fecha de ese
día). Lo que caduca sigue dejando `photoPath` en el fichaje: se sabe que hubo foto y cuándo
dejó de haberla.

El documental y las tareas no cambian: lo que sube un administrador lo borra un administrador.

### 5. El bucket: en Europa

Comprobado con `gcloud` el 2026-10-18: el bucket de producción
(`encodebiz-services.firebasestorage.app`) está en **US-CENTRAL1**; el de desarrollo
(`dev-encodebiz.firebasestorage.app`), en **EU**. Ninguno tiene reglas de ciclo de vida.

Las fotos de los trabajadores **no se guardan en Estados Unidos**. La transferencia sería
lícita (Google está en el Marco de Privacidad de Datos UE-EE. UU.), pero es la pregunta que
hará el DPO de cada cliente y no hay por qué darle la ocasión. Bucket nuevo
`encodebiz-media-eu` en `europe-west1` (0,020 $/GB-mes, sin nivel gratuito, que para esto es
irrelevante), con las seis reglas de ciclo de vida, acceso uniforme, sin acceso público, y
**sólo el servidor escribe**. El quiosco nace ahí. Mover documental y tareas al bucket
europeo es deseable y es otro trabajo (migración con los clientes vivos); se apunta en deuda.

### 6. Dónde se ve

Panel → Empresa → **Almacenamiento**: lo usado por módulo, lo incluido, los packs, la gráfica
de 90 días (de `storage_daily`), el botón de comprar pack (Stripe, mismo flujo que un add-on)
y, por módulo, su retención con la estimación. En la factura: la línea del pack y, si la hay,
la del exceso.

## Contratos

| Ruta | Auth | Para qué |
|---|---|---|
| `GET /storage?entityId` | ID token, `canWrite` | `{ usedBytes, byModule, includedGb, packsGb, daily[90] }` |
| `GET /storage/estimate?entityId&module&retentionDays` | ID token, `canWrite` | `{ employees, estimatedGb, includedGb, packsGb, excessGb, excessEurMonth, suggestedPack }` |
| `PATCH /entities/:id/settings/kiosk` | ID token, `canWrite` | `photoRetention` (y `photo`) |
| `POST /billing/addons` (ya existe el flujo de add-on) | ID token, `canWrite` | contratar `pack-10 / 50 / 200` |
| `POST /billing/usage/storage` (interno, cron de cierre) | servicio | reporta el exceso del ciclo a Stripe |

## Fases

| Fase | Qué | Dónde | Tamaño |
|---|---|---|---|
| 0 | Bucket `encodebiz-media-eu` con reglas de ciclo de vida (quiosco por retención, informes 30 días); `includedStorageGb` en los planes; packs en `service/storage` y Prices en Stripe | infra + datos | 1 día |
| 1 | Helper `checkbiz/storage` en `shared` y **migración de los cinco módulos que ya suben** (documental, tareas, firma, informes, campañas con la empresa en la ruta); regla de CI; contadores; reconciliación e instantánea diaria; avisos 80/100 %; `GET /storage` y `estimate` | `shared` + servicios + `billing` | 4 días |
| 2 | Panel: Almacenamiento, comprar pack, retención con estimación; exceso `metered` en el cierre del ciclo | panel + `billing` | 3 días |

El quiosco necesita la Fase 0 antes de su Fase 1 (el bucket y la carpeta de retención) y la
Fase 1 para contar; la Fase 2 puede ir detrás del piloto. El corte de demo del quiosco escribe
ya en el bucket europeo y en `kiosk/r30/`, aunque nadie cuente todavía.

## Riesgos

- **Contador desviado.** Por eso la reconciliación nocturna manda sobre el contador en vivo y
  el exceso se factura con el pico reconciliado, no con el contador.
- **Precio de venta demasiado alto frente a lo que la gente paga por un Drive.** 0,20-0,30 €/GB
  parece caro al lado de 100 GB por 2 €; no es el mismo producto (está atado al fichaje,
  servido con URL firmada, contado y auditado), pero hay que decirlo así en el panel y no
  esconderlo.
- **Migración del documental y las tareas al bucket europeo.** No se hace aquí; queda como
  deuda explícita y los contadores funcionan igual en los dos buckets.

## Fuentes

- Precios de Firebase (Storage) — https://firebase.google.com/pricing
- Precios de Cloud Storage — https://cloud.google.com/storage/pricing
- Preguntas frecuentes sobre el cambio de buckets de Firebase (sept. 2024) — https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024

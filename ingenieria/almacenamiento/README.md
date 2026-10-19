# Almacenamiento por empresa — contar y cobrar el exceso · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** transversal — Storage de la plataforma (quiosco, documental, tareas, firma, informes) × `billing`
**Fecha de inicio:** 2026-10-18 · **Rehecho:** 2026-10-19 (modelo simplificado por Jose)
**Estado:** Diseño cerrado el 2026-10-19 · sin implementar. Lo necesita el quiosco
([quiosco/README](../quiosco/README.md)) antes de su Fase 1.
**Autor:** Jose Acevedo

---

## De dónde sale

Jose, 2026-10-18, al cerrar que cada fichaje del quiosco lleva una foto: «un tema técnico muy
importante: espacio en Storage, ya que sería infinito».

La primera versión de este documento (18-oct) montaba cuota por plan, packs de pago, exceso
`metered`, avisos al 80 y al 100 %, un helper obligatorio y una regla de CI. Jose la rehízo el
19-oct: «la idea no es limitar, la idea es contabilizar todo lo posible, simplemente con un
trigger de Storage […] y si pasa de 2 GB se comienza a contabilizar redondeando al suelo». Este
documento es esa versión. La de packs queda en el historial de git y en
[ADR-001](./adr/ADR-001-todo-lo-que-se-sube-pasa-por-el-contador.md), sustituido por
[ADR-002](./adr/ADR-002-cuenta-un-trigger-de-storage.md).

## El modelo, en cuatro líneas

1. **Se cuenta todo lo que se pueda atribuir a una empresa.** Un trigger de Storage suma el
   tamaño de cada fichero que se sube y resta el de cada uno que se borra. Nadie tiene que
   acordarse de contar.
2. **Nada se limita.** Ninguna subida falla por espacio. No hay cuotas, packs ni bloqueos
   (la regla de la casa para los cupos: Jose, 2026-10-16, «no hay cupo», el exceso se cobra).
3. **2 GB incluidos para todas las empresas.** Por encima se cobra
   **`⌊GB usados⌋ − 2`**, redondeando hacia abajo: con 2,3 GB no se paga nada; con 3,1 GB se paga 1.
4. **0,25 € por GB y mes** de exceso, en una línea aparte de la factura de la suscripción.

Lo que pone el techo al volumen del quiosco no es la cuota sino la **retención** de sus fotos
(§Retención), que elige la empresa viendo lo que le costará.

## Los números

Lo que cobra Google por el almacenamiento (Cloud Storage, clase estándar; comprobado el
2026-10-18 en las páginas de precios de Firebase y de Google Cloud):

| Concepto | Precio |
|---|---|
| Almacenado, región única (`us-central1`, `europe-west1`) | ~0,020 $/GB-mes |
| Almacenado, bucket clásico de Firebase | 0,026 $/GB-mes |
| Descargado a internet | ~0,12 $/GB |
| Subidas (clase A) / descargas (clase B) | 0,05 $ / 0,004 $ por 10.000 |

**Por qué 0,25 €/GB y no el coste de Google más un margen pequeño.** Guardar un GB cuesta
unos 2 céntimos al mes, pero descargarlo una vez cuesta 12. Una empresa que descarga cada mes
una parte de lo que guarda (nóminas, fotos de tareas, informes) cuesta más en descargas que en
almacenamiento, y Stripe se queda en torno al 2 % de lo cobrado. Un precio de «Google + 5 %»
perdería dinero con cualquier cliente que descargue. A 0,25 € el GB queda unas doce veces por
encima del coste de guardarlo, cubre las descargas sin medirlas aparte y sigue siendo barato:
una empresa con 10 GB paga 8 GB, **2 € al mes**.

Unidad: **GiB** (2³⁰ bytes), la misma con la que factura Google.

Lo que ocupa el quiosco (JPEG de 640 px, unos **60 KB**; **3 fichajes al día** con foto; 22
días al mes):

| | Por empleado | 100 empleados | 1.000 empleados |
|---|---|---|---|
| Stock con retención 30 días | 4 MB | 0,4 GB | 4 GB → paga 2 GB, 0,50 €/mes |
| Stock con retención 1 año | 48 MB | 4,8 GB → paga 2 GB, 0,50 €/mes | 48 GB → 11,50 €/mes |
| Stock con retención 4 años | 190 MB | 19 GB → 4,25 €/mes | 190 GB → 47 €/mes |

## Qué cuenta y qué no

La empresa se lee **de la ruta del fichero**. Lo que lleva la empresa en la ruta cuenta; lo que
no, no. Rutas comprobadas en el código el 2026-10-19:

| Módulo (`byModule`) | Prefijo | Cuenta |
|---|---|---|
| `documents` — documental, PDF firmados incluidos | `documents/entities/{entityId}/…` | sí |
| `tasks` — recursos y fotos de valoración | `media/entities/{entityId}/checkinbiz/tasks/…` | sí |
| `signatures` — evidencia JSON de firma | `signatures/evidence/{entityId}/…` | sí |
| `reports` — informes, exportaciones y actas de firma | `checkbiz/reports/entities/{entityId}/…` | sí |
| `kiosk` — fotos del quiosco (bucket `encodebiz-media-eu`) | `kiosk/r{días}/{entityId}/…`, `kiosk/hold/{entityId}/…` | sí |
| Marca de la empresa (logos, imágenes del panel) | `media/entities/{entityId}/{tipo}/…` (todo lo que no es `checkinbiz/`) | **no** (Jose, 2026-10-19) |
| Campañas in-app | `campaigns/images/…` | **no**: las hace el backoffice para todos, no son de ninguna empresa |
| Cualquier otra ruta | — | no; el trigger la ignora |

La tabla es el contrato. Un módulo nuevo que guarde ficheros de una empresa pone el
`entityId` en la ruta y añade aquí su prefijo; si no lo hace, sus ficheros no se cobran.

Los informes **no llevan caducidad**: la versión del 18-oct les ponía 30 días en el bucket, y
con ello se habrían borrado las actas de firma, que viven en `checkbiz/reports/…/actas/`. Sin
esa regla, el acta que se valida es siempre la misma.

## Cómo se cuenta

### El trigger

Dos funciones por bucket en `services/firebase_sdk` (codebase `default`), una al terminar una
subida (`onObjectFinalized`) y otra al borrarse un objeto (`onObjectDeleted`). Buckets: el del
proyecto (`encodebiz-services.firebasestorage.app` en producción, `dev-encodebiz.firebasestorage.app`
en desarrollo) y `encodebiz-media-eu`.

Cada evento:

1. Saca `entityId` y `module` de la ruta con la tabla de arriba. Si no casa, termina.
2. En una transacción de Firestore, contra el **registro de objetos**
   `storage_objects/{sha1(bucket + "/" + ruta)} = { entityId, module, bucket, path, size, generation }`:
   - **Subida**: si el registro ya tiene esta `generation`, es un evento repetido y no hace
     nada. Si no existe, lo crea y suma `size`. Si existe con otra `generation` (se ha
     sobrescrito), lo actualiza y suma la diferencia.
   - **Borrado**: sólo si el registro tiene la misma `generation` que el evento, lo borra y
     resta su `size`. Si no coincide, es el borrado de una versión ya sustituida y no hace nada.
3. En la misma transacción, suma o resta en uno de los **diez trozos del contador**, elegido
   al azar: `entities/{entityId}/storage_shards/{0..9}`. El total de la empresa es la suma de
   los diez:

```text
storage_shards/{n} = { usedBytes, byModule: { documents, tasks, signatures, reports, kiosk }, updatedAt }
```

   Diez trozos y no un campo en `entities/{entityId}` porque Firestore aguanta más o menos
   una escritura por segundo en un mismo documento. A las 8:00, con mil personas fichando en
   el quiosco, un contador único se atascaría y reintentaría las transacciones. Leer el total
   cuesta diez lecturas, y sólo se lee al abrir la pantalla y al facturar.

Por qué así:

- **Google entrega los eventos al menos una vez**, a veces dos. La `generation` del registro
  hace que un evento repetido no sume dos veces.
- **Sobrescribir** en un bucket sin versiones genera la subida de la nueva versión y el
  borrado de la anterior, en cualquier orden. Con la `generation`, el resultado es el mismo
  llegue antes uno u otro.
- **Las reglas de ciclo de vida** (la retención del quiosco) también generan el evento de
  borrado, así que lo que caduca deja de contar solo.
- **Da igual quién suba.** Un servicio, un script de soporte o un cliente con el SDK pasan
  por el mismo trigger. Por eso ya no hace falta el helper obligatorio ni la regla de CI del
  ADR-001.

El helper de `shared` (`checkbiz/storage`, hoy en `feat/quiosco`) puede seguir existiendo
para elegir bucket y firmar URLs, pero **no cuenta**: si sumara él y sumara el trigger, el
fichero contaría dos veces.

### La carga inicial

Al encender el trigger, el registro está vacío y lo que ya hay en los buckets no cuenta. Un
script `services/billing/src/scripts/storage-backfill.ts` (en `billing`, que tiene contenedor con credenciales) lista los prefijos de la tabla,
rellena `storage_objects` y reescribe los trozos del contador (todo en el trozo 0, el resto a cero). Simula por defecto y escribe
con `--apply`. Se ejecuta una vez **después** de desplegar el trigger, para que lo que se suba
mientras corre no se pierda. El mismo script sirve de reparación si alguna vez el contador se
desvía (`--entity <id>` para una sola empresa).

### Medir sin código

Mientras no exista nada de esto, una empresa se mide a mano:

```bash
B=gs://encodebiz-services.firebasestorage.app
E=<entityId>
gcloud storage du --summarize $B/documents/entities/$E/ $B/media/entities/$E/checkinbiz/ \
  $B/signatures/evidence/$E/ $B/checkbiz/reports/entities/$E/
```

## Cómo se cobra

- **Qué se cobra**: `max(0, ⌊usedBytes / 2³⁰⌋ − 2)` GB, a 0,25 €, con `usedBytes` la suma de
  los diez trozos.
- **Cuándo**: con el valor del contador **el día en que Stripe crea la factura** del ciclo.
  Es lo más sencillo y la diferencia con el máximo del mes son céntimos. No hace falta guardar
  instantáneas diarias.
- **Cómo**: `billing` escucha `invoice.created` (motivo `subscription_cycle`). Mientras la
  factura está en borrador, si hay exceso, añade un `invoiceItem` con un Price de 0,25 € y
  `quantity` = GB a cobrar, y deja `{ usedBytes, billedGb }` en los metadatos de la línea.
  Stripe da una hora antes de cerrar el borrador. El evento `invoice.created` aún no está
  activado en el webhook de producción (pendiente del pase de octubre): sin él no se cobra nada.
- **Una sola vez por factura**: la línea lleva `metadata.kind = "storage"`. Si ya existe en la
  factura, no se añade otra.
- **Pendiente de decidir — empresas sin suscripción de pago.** Una empresa gratuita no tiene
  factura en Stripe a la que añadir la línea. Mientras Jose no decida otra cosa, se cuenta y se
  enseña, pero no se cobra.

## Retención del quiosco

Es el único módulo cuyos ficheros crecen solos, así que es el único con retención.
`entities/{e}.settings.kiosk.photoRetention ∈ { 15, 30, 60, 90, 365, 1460 }` días (1460 = 4
años, la retención del registro de jornada, art. 34.9 ET). Por defecto 30.

La ruta lleva la retención dentro (`kiosk/r{días}/{entityId}/{checklogId}.jpg`) y el bucket
tiene **una regla de ciclo de vida por valor** (`matchesPrefix: ["kiosk/r30/"], age: 30`, y así
las seis). Las reglas son del bucket, no de la empresa (máximo 100). Cambiar la retención no
mueve nada: las fotos nuevas van a la carpeta nueva y las viejas caducan con la suya.

Una foto **en disputa** (solicitud de corrección abierta o rechazada) se copia a
`kiosk/hold/{entityId}/…`, sin caducidad; al cerrar la disputa vuelve a su carpeta de
retención. El fichaje conserva `photoPath` aunque la foto haya caducado.

Al cambiar la retención, el panel enseña la cuenta hecha: «Con 240 empleados y 90 días, las
fotos ocuparán unos 2,9 GB. Con lo que ya ocupas, pagarías unos 0,75 € al mes».
`GET /storage/estimate?entityId&module=kiosk&retentionDays=` devuelve
`{ employees, estimatedGb, usedGb, billableGb, eurMonth }`.

El documental y las tareas no caducan: lo que sube un administrador lo borra un administrador.

## El bucket del quiosco, en Europa

Comprobado con `gcloud` el 2026-10-18: el bucket de producción está en **US-CENTRAL1** y el de
desarrollo en **EU**. Ninguno tiene reglas de ciclo de vida.

Las fotos de los trabajadores **no se guardan en Estados Unidos**. La transferencia sería
lícita (Marco de Privacidad de Datos UE-EE. UU.), pero es la pregunta que hará el DPO de cada
cliente. Bucket nuevo `encodebiz-media-eu` en `europe-west1`, con las seis reglas de
retención, acceso uniforme, sin acceso público y escritura sólo desde el servidor. Mover el
documental y las tareas a Europa queda como deuda; el trigger cuenta igual en los dos buckets.

## Sólo el servidor escribe: reglas de Storage

**Hecho el 2026-10-19**, en desarrollo y en producción, con el paso 2a de las reglas
([reglas-firestore/paso-2a.md §Storage](../reglas-firestore/paso-2a.md)). Hasta entonces
`storage.rules` vivía en `encodeBiz-SAAS` y dejaba a cualquier sesión leer y escribir en todo
el bucket salvo `documents/`: un usuario podía subir a la carpeta de otra empresa y, con el
trigger, inflarle la factura. Ahora las reglas viven en `encodebiz-api/storage.rules` y
cierran el bucket entero al cliente (`allow read, write: if false`). Ningún cliente usa el SDK
de Storage: el panel, la app y el quiosco suben por la API.

Para este diseño eso significa que todo lo que cuenta el trigger lo ha subido el servidor. Si
algún día un cliente necesita subir directo, se abre su ruta con nombre bajo
`…/entities/{e}/`, comprobando la pertenencia, y el trigger la cuenta igual.

## Dónde se ve

Panel → Empresa → **Almacenamiento**: lo usado por módulo, los 2 GB incluidos, los GB que se
cobrarían hoy y su importe, y la retención del quiosco con su estimación. En la factura, la
línea «Almacenamiento: N GB por encima de 2 GB».

## Contratos

| Ruta | Auth | Para qué |
|---|---|---|
| `GET /storage?entityId` | ID token, `canWrite` | `{ usedBytes, byModule, includedGb: 2, billableGb, eurMonth }` |
| `GET /storage/estimate?entityId&module=kiosk&retentionDays` | ID token, `canWrite` | estimación al cambiar la retención |
| `PATCH /entities/:id/settings/kiosk` | ID token, `canWrite` | `photoRetention` (y `photo`) |
| webhook `invoice.created` | firma de Stripe | añade la línea de exceso al borrador |

Las dos primeras van en `billing`, que es quien cobra.

## Fases

| Fase | Qué | Dónde | Tamaño |
|---|---|---|---|
| 0 | Bucket `encodebiz-media-eu` con las seis reglas de retención; Price de 0,25 €/GB en Stripe | reglas + infra + datos | 1 día |
| 1 | Triggers en los dos buckets, registro `storage_objects`, contador en `entities/{e}/storage_shards`, script `storage-backfill`; quitar la cuenta del helper de `feat/quiosco` | `firebase_sdk` + `shared` | 2 días |
| 2 | `invoice.created` añade la línea de exceso; `GET /storage` y `estimate`; panel Almacenamiento y retención | `billing` + panel | 2 días |

El quiosco necesita la Fase 0 (bucket y carpetas de retención) antes de su Fase 1. Cobrar
(Fase 2) puede ir detrás del piloto; lo que se suba antes queda contado por el trigger o por
la carga inicial.

## Riesgos

- **Contador desviado.** Si un evento se perdiera, el contador quedaría corto. El registro de
  objetos permite comprobarlo contra el bucket con el script de carga inicial en modo simular,
  que enseña la diferencia por empresa sin escribir.
- **Coste del registro.** Dos escrituras de Firestore por fichero subido (registro y trozo
  del contador) y otras dos al borrarse. Mil empleados en el quiosco son unas 66.000 fotos al
  mes: unas 260.000 escrituras, menos de 0,50 $. Nada.
- **Empresas que ya pasan de 2 GB el primer día.** El primer ciclo tras encender el cobro les
  llega con la línea. A 0,25 € el GB son importes pequeños, pero conviene avisarlas antes.
- **Rutas sin empresa.** Lo que se suba fuera de la tabla no se cobra. Es un riesgo de
  ingresos, no de servicio, y la tabla está aquí para revisarla en cada módulo nuevo.

## Fuentes

- Precios de Firebase (Storage) — https://firebase.google.com/pricing
- Precios de Cloud Storage — https://cloud.google.com/storage/pricing
- Triggers de Cloud Storage en Cloud Functions — https://firebase.google.com/docs/functions/gcp-storage-events
- Facturas de suscripción en Stripe (`invoice.created` y borradores) — https://docs.stripe.com/billing/invoices/subscription

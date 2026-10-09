# 08 — Firma incrustada en el PDF (PAdES) con certificado propio

**Fecha:** 2026-10-09 · **Estado:** **auth hecho y probado en staging** (CA del entorno, certificado por clave al registrar, `GET /api/v1/checkinbiz/auth/signing-ca.crt`; la cadena verifica con OpenSSL y una firma de la clave se comprueba con su certificado); el documental (preparar, montar, PDF firmado) pendiente; **la app, hecha el 2026-10-09** (§Lo que tiene que cambiar la app) · **Decisionario:** Jose Acevedo

> Jose, 2026-10-09: «¿la nómina se firma en sí, o sería un documento con un acta de firma? La
> idea es firmar el documento». Y después: «ojo, esto es solo para los documentos; lo del
> inventario sigue igualito con el acta. Además el acta aquí no sobra, es un plus, ya que solo se
> puede firmar el documento si es un PDF; si no, se crea el acta y ya está. Pero sí veo necesario
> que, si es un PDF, se pueda hacer con nuestro certificado. Esto iría en el módulo de
> documentación».

## Qué cambia y qué no

| | Hoy (firma separada) | Con esto |
|---|---|---|
| Nómina en PDF con acuse | el PDF queda intacto; la firma cubre su hash y vive en la evidencia y el acta | **el PDF sale firmado por dentro** (PAdES) y **sustituye al fichero del documento**: cualquier lector lo enseña como firmado por el trabajador, con fecha; además, evidencia y acta como hoy |
| Documento que no es PDF (imagen, Word, Excel) | evidencia y acta | igual: evidencia y acta. No se convierte a PDF para firmarlo |
| Entrega de equipos (inventario) | evidencia y acta | **igual, sin tocar** |

Lo que se firma no cambia: es el contenido del fichero. Cambia dónde queda la firma: dentro del
propio PDF, que es lo que el cliente guarda y enseña.

**Solo documentos dirigidos a un solo empleado.** Jose, 2026-10-09: «los documentos pueden ser
firmados cuando van dirigidos a un solo empleado; eso es importantísimo». La firma dentro del PDF
es la de una persona sobre **su** documento (`scope: employee`: nómina, amonestación, contrato).
Un documento de empresa o de sucursal es el mismo fichero para todos: cada trabajador sigue
acusando recibo con la firma sobre el hash (evidencia y acta), pero el fichero no se firma por
dentro. La regla la aplican los dos lados: la app no pide `prepare` para esos documentos
(`ManagedDocument.canBeSignedInPdf`) y el documental lo rechaza con 400 aunque se lo pidan.

## La pieza que falta: un certificado

Una firma dentro de un PDF va acompañada de un certificado X.509 que dice de quién es la clave.
Hoy las claves del móvil se registran sin certificado. La plataforma pasa a ser **su propia
autoridad de certificación**:

- **Una CA por entorno** («CheckBiz360 Firma CA», EC P-256): la privada en el volumen de
  secretos (`secrets/signing-ca.key`, nunca en el repo), la pública publicada en
  `GET /api/v1/checkinbiz/auth/signing-ca.crt` (auth: es identidad) y en el manual, para que el cliente la instale como
  de confianza en Acrobat si quiere ver la firma en verde.
- **Un certificado por clave registrada**, emitido al registrar (`POST /auth/signing-keys`) y
  guardado en `signing_keys/{employeeId}/keys/{keyId}.certificatePem`: sujeto `CN = nombre del
  trabajador, serialNumber = employeeId, OU = uid, O = CheckBiz360`, dos años de validez, usos
  `digitalSignature` y `nonRepudiation`. Una clave sustituida no revoca su certificado: lo
  firmado antes sigue valiendo (igual que hoy con la clave).

No somos un prestador cualificado: el lector dirá «firma válida, certificado de confianza
desconocida» hasta que el cliente instale nuestra CA. La prueba criptográfica es la misma; es
**firma electrónica avanzada** (eIDAS art. 26), no cualificada. Para una nómina o una
amonestación es lo habitual.

## Dónde vive cada pieza

> Jose, 2026-10-09: «¿o en auth?». Las dos, repartidas por lo que es cada una.

| Pieza | Dónde | Por qué |
|---|---|---|
| La CA del entorno y la emisión del certificado de cada clave | **`checkinbiz/auth`** (al registrar la clave) con el código común en `shared/checkbiz/signature` | el certificado dice **de quién es la clave**: es identidad, va con el registro de claves, los retos y la comprobación, que ya están ahí. Vale para cualquier módulo que firme PDF mañana |
| Preparar el PDF, montar la firma dentro, guardar y servir el PDF firmado | **`documents`** | es **el documento**: su fichero, sus versiones, sus acuses y sus permisos de lectura |
| Evidencia y acta | como hoy: `shared` al verificar, `reports` para el PDF del acta | no cambian |

Ningún servicio nuevo, nada duplicado: el documental no sabe de claves ni certificados más allá
de pedir «la cadena de certificados de esta clave» a `shared`.

## El flujo, en el documental

1. **Preparar** — `POST /documents/:id/sign/prepare` (el trabajador; el documento requiere
   acuse, **va dirigido a un solo empleado** (`scope: employee`; si no, 400 con un código propio,
   p. ej. `documents/not_employee_scoped`), es `application/pdf` y `canAcknowledge`). El servidor añade al PDF el hueco de firma
   (actualización incremental con `/ByteRange`), calcula el resumen de lo que queda fuera del
   hueco y construye los atributos firmados de CMS (`contentType`, `messageDigest`,
   `signingTime`, `signingCertificateV2`). Guarda el estado en el reto:
   `signing_challenges/{id}` con `purpose: "documents.pades"`, `subject { documentId, version,
   contentSha256 }`, `payloadEncoding: "base64"` (el `payload` son **bytes**, no texto) y
   `pades { preparedPath, byteRange }`. Responde `{ challengeId, toSign (base64 del DER de los
   atributos firmados), expiresAt }`. El reto vive dos minutos, como los demás.
2. **Firmar** — la app firma **los bytes** de `toSign` con la clave del chip (SHA256withECDSA
   sobre esos bytes) y llama al **mismo** `POST /documents/:id/ack` con `{ challengeId,
   signature }`.
3. **Montar** — el servidor verifica la firma sobre los atributos firmados con la clave vigente
   (como hoy), monta el `SignedData` de CMS con el certificado del trabajador y la cadena de la
   CA, lo incrusta en el hueco y **el PDF firmado sustituye al fichero del documento**. Jose,
   2026-10-09: «el documento firmado, por ejemplo una nómina, debe ser reemplazado, y si es para
   más de una persona esto es inviable»; de ahí la regla de arriba. Por fijar en el documental:
   el original se guarda aparte (para la evidencia, cuyo `payload` es el base64 de los atributos
   firmados, y para poder enseñar qué se firmó); sustituir **no cambia la versión ni vuelve a
   pedir acuse** (es el mismo contenido, con la firma dentro); `contentSha256` pasa a ser el del
   PDF firmado o se guarda el del original al lado. El acuse guarda `signature` y `evidence` como
   hoy, y el acta se genera igual.
4. **Descargar** — la descarga de siempre del documento (`GET /documents/:id/download`) ya da el
   PDF firmado: no hace falta ruta ni botón aparte, ni en el panel ni en la app. La app, tras un
   acuse firmado, vuelve a pedir ese documento (`GET /documents/:id`, que trae `ackStatus`) para
   que la lista enseñe el fichero que hay ahora.

Si el documento no es PDF, `prepare` responde 400 `documents/not_pdf` y la app usa el flujo de
hoy (`signing-subject` + reto + `ack`): evidencia y acta.

**Sello de tiempo (opcional, PAdES-B-T).** Con `SIGNING_TSA_URL` en el entorno, el servidor
pide un sello RFC 3161 a una autoridad de sellado externa y lo añade como atributo no firmado:
la hora deja de depender de nosotros. Sin la variable, la firma lleva la hora del servidor
(PAdES-B-B), que es lo que hay hoy en el acta.

## Lo que tiene que cambiar la app — hecho el 2026-10-09

Hoy la función de firmar recibe un **texto** y firma sus bytes UTF-8. Para el PDF tiene que
firmar **bytes exactos** (`toSign`, base64 → bytes). Es lo único que la app necesita; el resto
del flujo es el acuse de siempre.

**El paquete ya firma bytes.** Comprobado en `biometric_signature` 13.2.0: además de
`createSignature(String)` tiene `createSignatureFromBytes(Uint8List)`, y en nativo los dos
acaban en la misma firma (`Signature.update(bytes)` con `SHA256withECDSA` en Android;
`SecKeyCreateSignature` con `ecdsaSignatureMessageX962SHA256` sobre el `Data` recibido en iOS).
Los bytes cruzan el canal como `ByteArray` / `FlutterStandardTypedData`, sin recodificar. No hace
falta tocar el paquete.

**Lo hecho en la app** (checkbiz360, rama `feat/firma-clave-en-dispositivo`):

- `DeviceSigningKeyService.signBytes` firma un `Uint8List` tal cual. `SignAcknowledgement.signPrepared`
  firma un reto ya emitido (`challengeId` + `toSign`) sin pedir otro, y `canSign` dice si el móvil
  tiene clave sin tocar la red: sin clave no se prepara ningún PDF ni se pide reto.
- Al acusar recibo con clave en el móvil: si el documento va dirigido a un solo empleado
  (`scope: employee`) y es PDF (`mimeType`) —`ManagedDocument.canBeSignedInPdf`—, la app llama
  a `POST /documents/:id/sign/prepare`, decodifica `toSign` una sola vez y firma esos bytes; el
  acuse es el de siempre, `POST /documents/:id/ack` con `{ challengeId, signature }`. Si no cumple
  la regla no pregunta; si el documental responde 400 (`not_pdf`, `pdf_not_signable`, el del
  ámbito) o aún no tiene `prepare` (404, 5xx), vuelve al flujo de hoy (`signing-subject` + reto +
  `ack`): evidencia y acta.
- Probado en unitarios con un servidor de mentira (petición, decodificación de `toSign`, códigos
  de error) y con la firma falsa (firma los bytes exactos, sin reto nuevo ni paso por texto).
  **Sin probar contra el documental**, porque su parte está pendiente; cuando esté, un acuse de
  una nómina PDF desde el móvil debería salir con `signedFile`.
- Como el PDF firmado sustituye al fichero, la app no necesita nada aparte para descargarlo: la
  descarga de siempre ya lo da. Tras un acuse firmado vuelve a pedir el documento
  (`GET /documents/:id`, que trae `ackStatus`) y lo cambia en la lista sin retrasar el aviso; si
  esa recarga falla, se queda lo marcado en local.

## Qué pide cada entorno (va al registro del pase)

- Generar la CA del entorno **una vez**, desde el portátil:
  `npx ts-node --project services/checkinbiz/tsconfig.json services/checkinbiz/src/scripts/signing-ca.ts --name "CheckBiz360 Firma CA" --out <dir> --apply`
  (simula sin `--apply`; nunca pisa). Copiar `signing-ca.key` (600) y `signing-ca.crt` (644) al
  directorio `secrets/` del servidor; el compose los monta en `/secrets/` (hecho en staging el
  2026-10-09; el de producción lo documenta el pase). Sin ficheros, el servicio arranca y no
  emite certificados. `SIGNING_CA_KEY_PATH` / `SIGNING_CA_CERT_PATH` solo si cambia la ruta.
- Las claves registradas **antes** de la CA no tienen certificado: se emite al vuelo la primera
  vez que firman un PDF (el servidor tiene la pública), sin pedir nada al móvil.
- `SIGNING_TSA_URL` si se quiere sello de tiempo.
- Nada nuevo en Firestore ni en Postgres; `signing_challenges` gana campos.

## Librerías (encodebiz-api)

`pkijs` + `asn1js` para X.509 y CMS con ECDSA (node-forge no firma con curvas elípticas),
`pdf-lib` para el hueco de firma y la actualización incremental, `@peculiar/webcrypto` como
motor de WebCrypto en Node. Todo en `shared/checkbiz/signature/` (CA, certificados, CMS) y en
`documents` (preparar, montar, descargar).

## Límites, dichos al cliente

- Confianza del certificado: verde solo si instala nuestra CA; si no, «válida, confianza
  desconocida». La firma es igual de comprobable.
- Avanzada, no cualificada. Si un cliente necesita cualificada, es un prestador externo.
- Que la clave viva en el chip seguro lo relata la app hasta que llegue la atestación.
- Un PDF cifrado o con firmas previas que prohíban cambios no se puede firmar: `prepare`
  responde 400 `documents/pdf_not_signable`.

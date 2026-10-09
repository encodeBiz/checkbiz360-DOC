# 08 — Firma incrustada en el PDF (PAdES) con certificado propio

**Fecha:** 2026-10-09 · **Estado:** diseño, pendiente de construir · **Decisionario:** Jose Acevedo

> Jose, 2026-10-09: «¿la nómina se firma en sí, o sería un documento con un acta de firma? La
> idea es firmar el documento». Y después: «ojo, esto es solo para los documentos; lo del
> inventario sigue igualito con el acta. Además el acta aquí no sobra, es un plus, ya que solo se
> puede firmar el documento si es un PDF; si no, se crea el acta y ya está. Pero sí veo necesario
> que, si es un PDF, se pueda hacer con nuestro certificado. Esto iría en el módulo de
> documentación».

## Qué cambia y qué no

| | Hoy (firma separada) | Con esto |
|---|---|---|
| Nómina en PDF con acuse | el PDF queda intacto; la firma cubre su hash y vive en la evidencia y el acta | **el PDF sale firmado por dentro** (PAdES): cualquier lector lo enseña como firmado por el trabajador, con fecha; además, evidencia y acta como hoy |
| Documento que no es PDF (imagen, Word, Excel) | evidencia y acta | igual: evidencia y acta. No se convierte a PDF para firmarlo |
| Entrega de equipos (inventario) | evidencia y acta | **igual, sin tocar** |

Lo que se firma no cambia: es el contenido del fichero. Cambia dónde queda la firma: dentro del
propio PDF, que es lo que el cliente guarda y enseña.

## La pieza que falta: un certificado

Una firma dentro de un PDF va acompañada de un certificado X.509 que dice de quién es la clave.
Hoy las claves del móvil se registran sin certificado. La plataforma pasa a ser **su propia
autoridad de certificación**:

- **Una CA por entorno** («CheckBiz360 Firma CA», EC P-256): la privada en el volumen de
  secretos (`secrets/signing-ca.key`, nunca en el repo), la pública publicada en
  `GET /api/v1/documents/signing-ca.crt` y en el manual, para que el cliente la instale como
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

## El flujo, en el documental

1. **Preparar** — `POST /documents/:id/sign/prepare` (el trabajador; el documento requiere
   acuse, es `application/pdf` y `canAcknowledge`). El servidor añade al PDF el hueco de firma
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
   CA, lo incrusta en el hueco y escribe el **PDF firmado** como fichero propio:
   `documents/entities/{e}/signed/{documentId}/{employeeId}-v{version}.pdf` (una sola vez). El
   acuse guarda `signedFile { path, sha256 }` además de `signature` y `evidence`; la evidencia
   y el acta se generan igual que hoy (el `payload` de la evidencia es el base64 de los
   atributos firmados, y el acta lo dice).
4. **Descargar** — `GET /documents/:id/acks/:employeeId/signed-file?entityId` → URL firmada
   (5 min) del PDF firmado, con el permiso de leer el documento (el propio trabajador, y quien
   puede leer sus documentos). En el panel: en la ficha del documento, junto a cada
   confirmación, «Descargar el PDF firmado» cuando exista; en la app, «Mi copia firmada».

Si el documento no es PDF, `prepare` responde 400 `documents/not_pdf` y la app usa el flujo de
hoy (`signing-subject` + reto + `ack`): evidencia y acta.

**Sello de tiempo (opcional, PAdES-B-T).** Con `SIGNING_TSA_URL` en el entorno, el servidor
pide un sello RFC 3161 a una autoridad de sellado externa y lo añade como atributo no firmado:
la hora deja de depender de nosotros. Sin la variable, la firma lleva la hora del servidor
(PAdES-B-B), que es lo que hay hoy en el acta.

## Lo que tiene que cambiar la app

Hoy la función de firmar recibe un **texto** y firma sus bytes UTF-8. Para el PDF tiene que
firmar **bytes exactos** (`toSign`, base64 → bytes). Hay que confirmar con el paquete
`biometric_signature` si admite bytes; si solo admite texto, hace falta un ajuste en el
paquete (es pequeño: el chip firma bytes; es la capa Dart la que lo limita). Es lo único que la
app necesita; el resto del flujo es el acuse de siempre.

## Qué pide cada entorno (va al registro del pase)

- Generar la CA del entorno (clave + certificado autofirmado, 10 años), dejar la clave en
  `secrets/signing-ca.key` y el certificado en `secrets/signing-ca.crt` en el volumen de secretos;
  `SIGNING_CA_KEY_PATH` y `SIGNING_CA_CERT_PATH` si no están en la ruta por defecto.
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

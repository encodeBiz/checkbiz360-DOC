# Catálogo de casos de uso — firma del trabajador desde su móvil (prefijo FIR)

> Escrito el 2026-10-09 junto con el código (no por análisis estático): cada caso se afirmó
> contra `dev-encodebiz` el mismo día. Diseño en
> [ingenieria/firma/README.md](../../ingenieria/firma/README.md) y
> [documental-service/08](../../ingenieria/documental-service/08_firma-incrustada-en-el-pdf.md).

La prueba hace de móvil: genera una clave EC P-256 en el propio test y firma con `crypto` de
Node (SHA256withECDSA, DER base64), que es lo mismo que hace el chip seguro del teléfono. La
entrega de equipos (inventario) firma por el mismo camino, pero el mundo de QA no tiene el
add-on: queda fuera del catálogo hasta que lo tenga.

## Actores
- OP_WORKER con sesión de Firebase (`idToken`): el que firma.
- OP_SUPERVISOR: otro trabajador de la misma empresa (para «a nombre de otro»).
- PROP: la propietaria, que sube la nómina y pide el acta.
- AJENO: usuario de otra empresa.

## POST /api/v1/checkinbiz/auth/signing-keys y GET …/signing-ca.crt · FIR-01
- FIR-01-01 · ANON · `GET /auth/signing-ca.crt` → `200`, PEM de un certificado con `CA:TRUE`.
- FIR-01-02 · OP_WORKER · registra su clave (`level: biometric`, PEM P-256) → `201 {keyId = SHA-256 de la pública en DER, level, certificate.pem}`; el certificado lo emite la CA publicada, verifica con ella, su `serialNumber` es el `employeeId` y su pública es la registrada.
- FIR-01-03 · OP_WORKER · la misma clave otra vez → `200` con el mismo `keyId` (nada se duplica).
- FIR-01-04 · OP_SUPERVISOR · `employeeId` de OP_WORKER → `403 signature/not_your_employee`.
- FIR-01-05 · OP_WORKER · una pública que no es EC P-256 → `400 signature/invalid_public_key`.
- FIR-01-06 · OP_WORKER · `level: none` con `unavailableReason` → `200 {level:"none", unavailableReason}`; no se registra clave.

## POST /api/v1/checkinbiz/auth/signing-challenges · FIR-02
- FIR-02-01 · OP_WORKER · `{purpose, entityId, employeeId, subject}` → `201 {challengeId, payload, expiresAt}`; `payload` es el JSON canónico con `challengeId`, `nonce` (32 hex), `purpose`, `employeeId` y el `subject` dentro; caduca a los dos minutos.
- FIR-02-02 · OP_WORKER · `purpose` desconocido → `400 signature/unknown_purpose`.
- FIR-02-03 · AJENO · `employeeId` de otra empresa → `403 signature/not_your_employee`.

## Acuse de recibo firmado (`documents` + `reports`) · FIR-03
- FIR-03-01 · PROP · sube una nómina (`scope: employee`, `requiresAcknowledgement`) → `201`, `document.contentSha256` es un SHA-256.
- FIR-03-02 · OP_WORKER · `GET /documents/:id/signing-subject` → `200 {purpose:"documents.acknowledgement", subject:{documentId, version, contentSha256, title}}`.
- FIR-03-03 · OP_WORKER · reto + firma válida en `POST /documents/:id/ack` → `200`; la ficha dice `ackStatus {method:"biometric_signature", verified:true}`.
- FIR-03-04 · PROP · `GET /documents/:id/acks` → el acuse lleva `signature {challengeId, keyId, level}` y `signature.evidence {path:"signatures/evidence/{e}/documents.acknowledgement/{challengeId}.json", sha256}`.
- FIR-03-05 · PROP · `GET /api/reports/signatures/evidence` → `200 {url, sha256}`; el fichero descargado tiene ese SHA-256, lleva la pública y el `payload`, y **la firma verifica con `crypto` de Node sin la plataforma**; el `subject` lleva el `contentSha256` de la nómina.
- FIR-03-06 · PROP · `GET /api/reports/signatures/acta` → `200 {url}` de un PDF; repetir → `200` (reutiliza).
- FIR-03-07 · OP_WORKER · pide el acta → `403`.
- FIR-03-08 · OP_WORKER · firma alterada sobre otra nómina → `400 documents/signature_invalid (reason: signature_invalid)`; no deja acuse.
- FIR-03-09 · OP_WORKER · el reto de la primera nómina sobre la segunda → `400 … (reason: challenge_mismatch)`.
- FIR-03-10 · OP_WORKER · `ack` sin reto ni firma → `200`; `ackStatus {method:"tap", verified:false}`.
- FIR-03-11 · OP_WORKER · firma después de haber pulsado → `200` y el acuse sigue siendo `tap` (el primero manda).

Limpieza: la prueba archiva las dos nóminas al terminar.

# Firma electrónica del trabajador — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Firma (módulo propio, transversal)
**Fecha de inicio:** 2026-10-08
**Estado:** Idea anotada. **App: clave creada en el login y vinculada al dispositivo (2026-10-09,
rama `feat/firma-clave-en-dispositivo` de checkbiz360)**; servidor sin código. Jose, 2026-10-08: «esto es otro
módulo, así que déjalo documentado y terminemos con lo de Inventario ahora».
**Autor:** Jose Acevedo

---

## De dónde sale

Diseñando la entrega de EPIs del inventario ([inventario/07 §4.5](../inventario/07_operables-documentos-y-entregas.md))
se vio que la forma de confirmar con huella no es del inventario: es la misma que haría falta
para que un trabajador firme el recibí de una **nómina** o el enterado de una **amonestación**.
Jose: «tenemos alternativas, porque esto puede también usarse para firmar documentos».

## Qué es

Una capacidad de la plataforma, construida una vez, que cualquier módulo usa: **el trabajador
firma desde su móvil lo que se le pone delante, y el servidor puede comprobar esa firma.**

- **Nivel 1, verificable:** la huella o la cara desbloquean una clave creada en el chip seguro
  del móvil (Secure Enclave en iOS, Keystore/StrongBox en Android); con ella la app firma un
  reto del servidor y el servidor comprueba la firma con la clave pública registrada al activar.
  En Flutter, `biometric_signature`; la app ya lleva `local_auth`, que solo devuelve sí/no.
- **Nivel 2:** sin biometría pero con bloqueo de pantalla, el PIN o patrón del móvil.
- **Nivel 3:** sin bloqueo de pantalla, la contraseña de la cuenta, pedida otra vez justo antes.

El servidor guarda siempre uid, hora, dispositivo, qué nivel fue y si la firma se verificó.

## Lo que un documento exige y una entrega no

- **Atar la firma al contenido**: se firma el hash del fichero (y su versión), para poder
  demostrar qué se firmó y que no cambió después.
- **«No conforme»**: en una amonestación el trabajador puede firmar que la ha recibido sin
  estar de acuerdo. Es un resultado propio, no un rechazo.
- **Acta de firma**: un PDF por documento con quién, cuándo, desde qué móvil, cómo (nivel) y el
  hash firmado, para enseñarlo a quien lo pida.

## Dónde encaja

En el servicio documental, donde ya viven los acuses de recibo (`requiresAcknowledgement`),
subiendo el acuse de «pulsó sí» a «firmó». Claves por empleado y por móvil
(`POST /employees/me/devices`), reto de un solo uso y comprobación en el servidor. Los
consumidores previstos: nóminas y amonestaciones (documental), entrega de EPIs (inventario,
Fase 6).

## Valor legal, con cuidado

Una firma con clave en el chip seguro, vinculada al trabajador y a su móvil, bajo su control y
atada al documento, tiene los ingredientes de la **firma electrónica avanzada** del reglamento
eIDAS. **No** es una firma cualificada, que exige un certificado de un prestador reconocido; si
un cliente la necesita, es otra pieza con un prestador detrás. Lo que diga un juez o un
inspector depende del caso y de la normativa aplicable, no de la herramienta.

## Qué queda por hacer cuando toque

Diseño detallado (modelo, contratos, acta), ADR de la decisión «firma avanzada propia, no
cualificada», prueba de `biometric_signature` en móviles reales de gama baja, y el ajuste por
empresa para exigir el nivel 1.

---

## Lo construido en la app (2026-10-09)

> Jose, 2026-10-09: «en el login si no existe la firma la creas y la vinculas a dispositivo junto
> con el token de notificación», y «es importante tener en cuenta los dispositivos que no tienen
> biometría activa o que no tienen biometría». La parte del servidor va después.

Rama `feat/firma-clave-en-dispositivo` de checkbiz360, módulo `lib/features/signature`, paquete
`biometric_signature` 13.2.0.

### Cuándo y qué

Al terminar el login —en el mismo punto donde se registra el token FCM, sin bloquear la
entrada— la app asegura la clave de firma de **ese empleado en ese móvil**:

1. Mira qué permite el móvil **hoy** (el nivel):
   - **`biometric`**: hay huella o cara registradas. La clave solo se desbloquea con ellas y se
     invalida si cambian las huellas o caras registradas.
   - **`device_credential`**: no hay biometría, o la hay sin activar, pero sí bloqueo de
     pantalla. La clave se desbloquea con el PIN, patrón o código del móvil.
   - **`none`**: sin bloqueo de pantalla. **No se crea clave**: nada probaría que firmó la
     persona. Al confirmar se sigue usando la contraseña de la cuenta (nivel 3).
2. Si ya hay clave válida creada con ese mismo nivel, se reutiliza. Si no existe, ya no vale
   (cambiaron las huellas) o el nivel ha cambiado (activó la huella, o la quitó), se borra y se
   crea otra. El nivel con que se creó no lo dice el chip: se apunta en preferencias.
3. La pública se vincula al dispositivo (abajo). Crear la clave no pide huella; firmar sí.

Una clave por empleado y móvil, alias `cb360_sign_<employeeId>`: dos personas que comparten
teléfono firman cada una con la suya.

### Algoritmo

ECDSA P-256; se firma el SHA-256 del contenido (`SHA256withECDSA`). Clave en el chip seguro:
Secure Enclave en iOS; Keystore o StrongBox en Android (si StrongBox falla, el paquete reintenta
en el TEE). La privada no sale nunca del móvil.

### Dónde queda: junto al token de notificaciones

`notification_tokens/{employeeId}/devices/{deviceId}`, el documento que ya guarda el token FCM
del móvil, gana el campo `signingKey` (escrito con merge, nunca toca el token):

| Campo | Qué |
|---|---|
| `level` | `biometric` · `device_credential` · `none` |
| `keyAlias` | `cb360_sign_<employeeId>` |
| `publicKey` | la pública en **PEM** (SubjectPublicKeyInfo), o `null` si no hay clave |
| `publicKeyFormat` | `pem` |
| `algorithm`, `keySize` | lo que informa el chip (`EC`, 256) |
| `signatureAlgorithm` | `SHA256withECDSA` |
| `createdAt` | cuándo se creó la clave en el móvil (ISO, UTC) |
| `unavailableReason` | sin clave, por qué: `no_screen_lock`, `not_supported` (web/escritorio) o `create_failed_<código>` |
| `uid`, `employeeId` | de quién es |
| `updatedAt` | hora del servidor de la última vinculación (cada login) |

`deviceId` es el identificador persistente que ya usa el token FCM (`DeviceInfoService`, que
sobrevive a reinstalar). La firma se hace con `DeviceSigningKeyService.sign`, que pide huella,
cara o código según el nivel y devuelve la firma en base64.

### Dónde se firma (2026-10-09)

Dos acuses van firmados cuando el móvil tiene clave; sin clave, o si la clave no sirve
(invalidada, bloqueada), siguen como antes. Si el trabajador cancela la huella o el código, no
se confirma nada.

| Acuse | Qué se firma (`kind`) | Cómo va |
|---|---|---|
| Entrega de material («Mi material» → «Confirmar recepción») | `unit_assignment_acknowledgement`: `entityId`, `employeeId`, `assignmentId`, `unitId`, `itemId`, `documents` (`documentId` + `version` de cada uno), `text`, `signedAt` | `POST /inventory/assignments/:id/acknowledge` con `method: biometric_signature`. Mientras el servidor responda 400 `inventory/method_not_available`, la app repite como `device_credential` con la firma en el cuerpo: el trabajador se acaba de desbloquear, que es lo que ese método registra. Cuando el servidor lo acepte, no hay que tocar la app |
| Acuse de recibo de un documento (Documentos → «Acusar recibo») | `document_acknowledgement`: `entityId`, `employeeId`, `documentId`, `documentVersion`, `signedAt` | `POST /documents/:id/ack` con la firma en el cuerpo; hoy el servidor ignora esos campos |

Lo firmado es un JSON con `v: 1` y las claves siempre en ese orden. Campos que se añaden al
cuerpo del acuse (`AcknowledgementSignature.toBody`):

| Campo | Qué |
|---|---|
| `signature` | firma ECDSA en base64 sobre los bytes UTF-8 de `signedPayload` |
| `signedPayload` | la cadena exacta firmada |
| `signatureAlgorithm` | `SHA256withECDSA` |
| `publicKeyId` | el alias de la clave (`cb360_sign_<employeeId>`) |
| `publicKey` | la pública en PEM, para verificar aunque aún no haya registro propio |
| `signingLevel` | `biometric` · `device_credential` |

El servidor, cuando toque: comprobar la firma con la pública **registrada** (no con la que llega
en el cuerpo, que solo sirve de pista), comprobar que `signedPayload` habla de este acuse
(`assignmentId` o `documentId`, empleado, documentos y versiones) y que `signedAt` es reciente,
y guardar firma, lo firmado y el nivel con el acuse.

### Lo que queda para el servidor

- **Historial de claves.** Al cerrar sesión la app borra el documento del dispositivo
  (`removeDeviceToken`), y con él `signingKey`; en el siguiente login se vuelve a vincular la
  misma clave si sigue valiendo. Una firma antigua tiene que poder comprobarse aunque la clave
  ya no esté ahí: el servidor debe copiar la pública a un registro propio que no se borre ni se
  edite (o guardarla con cada acuse).
- **Constancia del alta.** Hoy la escribe la propia app en Firestore con la sesión del
  trabajador; para que valga como registro, las reglas deben impedir cambiar `signingKey` a
  mano, o el alta pasar por `POST /employees/me/devices` como dice §Dónde encaja.
- **Reto de un solo uso** emitido por el servidor (hoy lo firmado no lleva reto, solo la hora)
  y comprobación de la firma en los dos acuses (arriba).
- **Hash del fichero** en lo firmado, si se quiere: lo tiene que guardar y devolver el
  documental; hoy se firma documento + versión.

### Pendiente de comprobar en móviles reales

Que crear la clave no muestre ningún diálogo en Android ni iOS; el comportamiento con solo PIN
en Android (`useDeviceCredentials`); y móviles de gama baja sin StrongBox.


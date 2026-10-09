# Firma electrónica del trabajador — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Firma (módulo propio, transversal)
**Fecha de inicio:** 2026-10-08
**Estado:** **App: clave creada en el login y vinculada al dispositivo (2026-10-09,
rama `feat/firma-clave-en-dispositivo` de checkbiz360)**. **Servidor: hecho el 2026-10-09 (§Lado del
servidor) en `checkinbiz/auth` y `shared`, en develop y staging de encodebiz-api, probado contra staging**
(registro, reto, acuse firmado y verificado; firma alterada y reto ajeno rechazados). **App
adaptada al servidor el 2026-10-09** (registro por API, reto y acuse firmado; §Lo construido en
la app). **El documental comprueba también la firma del acuse de recibo (2026-10-09, probado en
staging; §El documental como segundo consumidor). Reglas de Firestore versionadas en `encodebiz-api` y
desplegadas en dev (2026-10-09). Acta de firma hecha y probada en staging con una nómina (2026-10-09, §El acta):
evidencia cerrada al firmar, PDF bajo demanda, comprobación independiente con OpenSSL en verde, y la descarga
en la ficha del documento del panel.** Falta que la app firme el acuse de documentos (hoy solo firma la entrega
de equipos), probar en móviles reales y el pase a prod
([deployment-prod/2026-10](../../deployment-prod/2026-10-inventario-firma-back.md)). Jose, 2026-10-08: «esto es otro
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

### Dónde queda: la registra el servidor

> Corregido el 2026-10-09 con el lado del servidor: la primera versión escribía `signingKey`
> desde la app en Firestore; ya no. La app no escribe la clave en ningún sitio.

Al terminar el login la app llama a **`POST /auth/signing-keys`** (checkinbiz, ID token de
Firebase) con `employeeId`, `deviceId` (el identificador persistente que usa el token FCM),
`level` y, si hay clave, `publicKey` en PEM, `publicKeyFormat: pem`, `algorithm`, `keySize`,
`signatureAlgorithm: SHA256withECDSA` y `createdAt`; sin clave, `unavailableReason`
(`no_screen_lock`, `not_supported` o `create_failed_<código>`). El servidor la guarda en
`signing_keys/{employeeId}/keys/{keyId}`, que no se borra, y la refleja en
`notification_tokens/{employeeId}/devices/{deviceId}.signingKey`, junto al token FCM.
Registrar dos veces la misma clave no duplica nada, así que se manda en cada login. Si falla,
el login sigue y se reintenta en el siguiente.

### Dónde se firma

Dos acuses van firmados cuando el móvil tiene clave. Sin clave, o si no se puede firmar (clave
invalidada o bloqueada, o el servidor no da reto), siguen como antes. Si el trabajador cancela
la huella o el código, no se confirma nada.

El flujo es el mismo en los dos (`SignAcknowledgement`):

1. ¿Tiene el móvil clave para el empleado? Si no, sin red ni diálogo, el acuse de siempre.
2. `POST /auth/signing-challenges` con `purpose`, `entityId`, `employeeId` y `subject`.
3. El móvil firma el **`payload` del reto, tal cual** (lo arma el servidor; la app no compone
   nada), con huella, cara o código según el nivel de la clave.
4. El acuse lleva `{ challengeId, signature }`.

| Acuse | `purpose` | `subject` | Acuse |
|---|---|---|---|
| Entrega de material («Mi material» → «Confirmar recepción») | `inventory.assignment_ack` | el que da `GET /inventory/assignments/:id/signing-subject` (la entrega y sus documentos con versión) | `POST /inventory/assignments/:id/acknowledge` con `method: biometric_signature`, `challengeId`, `signature`. El servidor comprueba la firma y escribe el método según el nivel de la clave (`biometric_signature` o `device_credential`), verificado. Una firma no válida responde 400 `inventory/signature_invalid` y la app lo muestra como error |
| Acuse de recibo de un documento (Documentos → «Acusar recibo») | `documents.acknowledgement` | `{ documentId, version }`, la versión que el trabajador tiene delante | `POST /documents/:id/ack` con `challengeId` y `signature`. **El documental aún no comprueba la firma**: hoy ignora esos campos y el reto caduca sin usarse. Cuando lo haga, tiene que reconstruir este mismo `subject` |

### Lo que queda

- **Reglas de Firestore** (encodeBiz-SAAS): cerrar `signing_keys/**`, `signing_challenges/**` y
  `signingKey` del dispositivo al cliente.
- **Comprobar la firma en el documental** (`verifySignedChallenge` en su acuse), con el
  `subject` de arriba.
- **Hash del fichero** en lo firmado, si se quiere: lo tiene que guardar el documental.

### Pendiente de comprobar en móviles reales

Que crear la clave no muestre ningún diálogo en Android ni iOS; el comportamiento con solo PIN
en Android (`useDeviceCredentials`); que la firma del chip llegue en DER (la que comprueba el
servidor) en los dos sistemas; y móviles de gama baja sin StrongBox.

## Lado del servidor (diseño, 2026-10-09)

> Jose, 2026-10-09: «es verdad, me parece bien: implementa tu parte. Esto es del servicio de
> checkinbiz / auth; no hagas un nuevo servicio». Lo que sigue corrige una decisión de la app:
> **la clave pública no la escribe el móvil en Firestore; la registra el servidor.**

### Por qué el servidor

Hoy la app escribe `signingKey` en el documento del dispositivo con la sesión del trabajador.
Cualquiera con esa sesión podría cambiarla por otra clave, y la firma dejaría de probar nada.
Lo que da validez a algo pasa por el backend, como ya se decidió para los permisos
([feedback: escrituras sensibles por backend](../../../encodebiz-api/CLAUDE.md)): la app envía
la clave a un endpoint, el servidor la registra en un sitio que no se borra, y las reglas de
Firestore impiden tocarla desde el cliente. Las reglas dejan de ser un parche: son la
consecuencia de que nadie más que el servidor escribe ahí.

### Dónde vive

En el servicio **`checkinbiz`**, bajo `/api/v1/checkinbiz/auth`, junto al login y al segundo
factor: la clave nace en el login y es una credencial más del empleado. Las piezas comunes
(entidades, repositorio, comprobación de firmas) van en `@encodebiz/shared`, en
`checkbiz/signature/`, para que el inventario, el documental o quien venga las usen sin copiarlas.

### El registro de claves: solo se añade

Colección raíz `signing_keys/{employeeId}/keys/{keyId}`, al lado de `notification_tokens` y con
la misma idea de «por empleado y por móvil». **Nunca se borra ni se edita una clave**: solo se
añaden, y a lo sumo se marcan como sustituidas. Al cerrar sesión la app borra el documento del
dispositivo; este registro no se entera.

| Campo | Qué |
|---|---|
| `keyId` | huella SHA-256 de la clave pública (hex). Es el id del documento: registrar dos veces la misma clave no duplica nada |
| `employeeId`, `uid`, `entityIds` | de quién es (el uid es el de Firebase; las entidades, las del empleado al registrar) |
| `deviceId` | el identificador persistente del móvil, el mismo que usa el token FCM |
| `level` | `biometric` · `device_credential` |
| `publicKey`, `publicKeyFormat` | la pública en PEM (SubjectPublicKeyInfo) |
| `algorithm`, `keySize`, `signatureAlgorithm` | `EC`, 256, `SHA256withECDSA` |
| `createdAt` | cuándo la creó el móvil (lo dice la app) |
| `registeredAt` | cuándo la registró el servidor (hora del servidor) |
| `supersededAt`, `supersededBy` | si para ese empleado y móvil llegó otra clave después: cuándo y cuál |
| `attestation` | reservado: la atestación del chip (Android Key Attestation, App Attest), cuando se añada |

Una clave **sustituida** sigue sirviendo para comprobar las firmas hechas mientras estuvo
vigente. Un móvil sin bloqueo de pantalla no registra clave: eso queda en el dispositivo
(`unavailableReason`), no aquí.

El servidor mantiene además `signingKey` en `notification_tokens/{employeeId}/devices/{deviceId}`
con los mismos campos que escribía la app, más `keyId`: la app sigue leyendo de ahí lo que ya
lee, y es el único escritor.

### Contratos

Los dos primeros cuelgan de `authRouter` (ID token de Firebase, como `/login`): la app los
llama con la sesión de Firebase que ya tiene.

**`POST /auth/signing-keys`** — registrar o reafirmar la clave del móvil. Lo llama la app al
terminar el login, en vez de escribir en Firestore.

```json
{ "employeeId": "…", "deviceId": "…", "level": "biometric",
  "publicKey": "-----BEGIN PUBLIC KEY-----…", "publicKeyFormat": "pem",
  "algorithm": "EC", "keySize": 256, "signatureAlgorithm": "SHA256withECDSA",
  "createdAt": "2026-10-09T08:12:00Z" }
```

El servidor comprueba que el `employeeId` es de ese uid, que la pública es una EC P-256
válida y calcula `keyId`. Si ya existe para ese empleado, responde la misma; si para ese
empleado y móvil había otra vigente, la marca sustituida. Responde `201 { keyId, level }`
(o `200` si ya estaba). Sin clave (`level: none`), la app manda `unavailableReason` y el
servidor solo actualiza el dispositivo.

**`POST /auth/signing-challenges`** — pedir un reto para firmar algo concreto.

```json
{ "purpose": "inventory.assignment_ack", "entityId": "…",
  "subject": { "assignmentId": "…", "text": "Confirmo que he recibido…",
               "documents": [ { "documentId": "…", "version": 1 } ] } }
```

Responde `{ challengeId, payload, expiresAt }`. **`payload` es la cadena exacta que se firma**:
el JSON canónico (claves ordenadas, sin espacios) de `{ challengeId, nonce, purpose, entityId,
employeeId, subject, issuedAt }`. Vive dos minutos, se usa una vez y queda en
`signing_challenges/{challengeId}` con `usedAt` cuando se consume. Que la frase del acuse sea
genérica no debilita nada: lo concreto —la entrega, los documentos y su versión— va dentro de
lo firmado.

**Comprobar** — no es una ruta: es `verifySignedChallenge` en `shared`, que llama el módulo que
recibe la firma (el inventario en `POST /assignments/:id/acknowledge`, el documental en su
acuse). Recibe `{ challengeId, signature, employeeId, purpose, subject }`; comprueba que el
reto existe, es de ese empleado y propósito, no ha caducado ni se ha usado, que el `subject`
coincide con lo que se emitió, y verifica la firma (ECDSA sobre SHA-256 del `payload`, firma en
DER base64) contra **todas las claves del empleado vigentes al emitir el reto**; marca el reto
usado y devuelve `{ verified: true, keyId, level }`. Cualquier fallo es `verified: false` con
su motivo, y el módulo decide (el inventario responde 400 `signature_invalid`).

### Qué cambia en el inventario

`method: biometric_signature` deja de responder 400: el acuse manda `{ challengeId, signature }`,
el inventario llama a la comprobación y guarda `acknowledgement.signature = { challengeId, keyId,
level, signature }` con `verified: true`. El nivel de la clave decide el método que queda
escrito: `biometric` → `biometric_signature`; `device_credential` → `device_credential`, pero
ahora **verificado**, porque hay firma (hasta hoy ese método era solo declarado). La escalera
de §4.5 del inventario no cambia.

### Reglas de Firestore — hechas el 2026-10-09, en `encodebiz-api/firestore.rules`

Viven en `encodebiz-api` (Jose: el repo del SaaS está deprecado; las reglas acompañan a quien
escribe en Firestore con autoridad, que son los servicios de este repo). `firebase.json` las
declara; despliegue solo con `firebase deploy --only firestore:rules --project <proyecto>`.
Conservan el comodín abierto heredado y le quitan: `signing_keys/**` y `signing_challenges/**`
sin acceso desde el cliente; en `notification_tokens/{e}/devices/{d}`, `signingKey` no se crea
ni se cambia desde el cliente (se puede omitir en una escritura sin merge y borrar el documento
al cerrar sesión: el registro es la fuente). Desplegadas en dev y comprobadas por la API REST
de Firestore con la sesión del trabajador (403 a claves y retos; 403 al forjar `signingKey`;
200 al actualizar el token). Para prod: [deployment-prod/2026-10](../../deployment-prod/2026-10-inventario-firma-back.md) §5.3.

### Qué tiene que cambiar la app — hecho el 2026-10-09

Dejar de escribir `signingKey` y llamar a `POST /auth/signing-keys` en el mismo punto del
login. Al confirmar una entrega con firma: pedir el reto con el `subject` de la entrega,
firmar `payload` con `DeviceSigningKeyService.sign` y mandar `{ accepted: true, method,
challengeId, signature, device }`. Hecho tal cual, y lo mismo para el acuse de recibo de
documentos (§Dónde se firma).

### Probado contra staging (2026-10-09, Cuidama, haciendo de móvil con una clave P-256 local)

Registrar (201; repetir, 200 con el mismo `keyId`; empleado ajeno, 403) → entregar → pedir el
`signing-subject` → reto → firmar el `payload` → acuse: `method: biometric_signature`,
`verified: true`, `signature.keyId`. Una firma alterada responde 400 `signature_invalid`; el
reto de otra entrega, 400 `challenge_mismatch`; sin reto, 400. El registro, el espejo en el
dispositivo (`signingKey.keyId`) y los retos usados quedan en Firestore como se describe.

### El documental como segundo consumidor (2026-10-09)

> Jose, 2026-10-09: «que el servicio de documentos compruebe la firma, para el acuse de recibo».

`POST /documents/:id/ack` admite `challengeId` + `signature` con `purpose:
"documents.acknowledgement"`; el `subject` lo da `GET /documents/:id/signing-subject`:
`{ documentId, version, contentSha256, title }`. El documental calcula `contentSha256` al subir
el fichero, así que **lo firmado es el contenido**, como pedía §Lo que un documento exige. El
acuse guarda `method`, `verified` y `signature`, igual que la entrega del inventario. Contrato
completo en [documental-service/03](../documental-service/03_contratos-api.md#confirmación-de-lectura-acknowledgements).
Probado en staging el 2026-10-09 con el trabajador de Cuidama: acuse firmado → `method:
biometric_signature`, `verified: true`; firma alterada → 400 `signature_invalid`; reto de otro documento
→ 400 `challenge_mismatch`; un acuse pulsado antes no se convierte en firmado después. Con el
acta (misma tarde, con «Nómina septiembre 2026 (prueba)»): acuse firmado → evidencia en Storage,
acta PDF de una página, `sha256` del JSON coincide, `openssl dgst -verify` → «Verified OK», el
`keyId` es el SHA-256 de la pública en DER, y el payload lleva el `contentSha256` de la nómina;
el trabajador no puede pedir el acta (403). El «no conforme» de las amonestaciones sigue pendiente.

### El acta de firma: la prueba que se puede comprobar sin fiarse de nosotros (2026-10-09)

> Jose, 2026-10-09: «en caso de inspección, ¿cómo demuestra mi cliente que se firmó
> correctamente?». Y la lista de la sesión de la app: columna «Firma» en el informe, acta en
> PDF por entrega, prueba verificable con OpenSSL, base de datos cerrada al cliente.

Hoy el informe dice «verificada»: es la plataforma dando su palabra. Lo que convierte eso en
prueba es que un tercero pueda repetir la comprobación con herramientas estándar. Para eso
hacen falta cuatro cosas: la cadena exacta que se firmó, la firma, la clave pública con su
fecha de registro, y la hora del servidor. Todo existe en Firestore; lo que faltaba era
**sacarlo en el momento de firmar y dejarlo cerrado**.

**1. La evidencia (JSON), al firmar.** `SigningChallenges.verify` escribe, en el mismo paso
en que marca el reto usado, un fichero en Storage:
`signatures/evidence/{entityId}/{purpose}/{challengeId}.json`, con su SHA-256. No se reescribe
nunca (`create`, no `save` encima). Contenido:

| Campo | Qué |
|---|---|
| `version` | `1` |
| `purpose`, `entityId`, `employeeId`, `uid`, `challengeId` | de qué firma es y de quién |
| `payload` | la cadena **exacta** que se firmó, tal cual (con el `subject` dentro: la entrega y sus documentos con versión, o el documento con su `contentSha256`) |
| `signature`, `signatureAlgorithm`, `hashAlgorithm` | la firma en base64 (DER), `SHA256withECDSA`, `SHA-256` |
| `key` | `keyId`, `level`, `publicKeyPem`, `algorithm` (`EC`), `curve` (`P-256`), `deviceId`, `createdAt` (móvil), `registeredAt` (servidor) |
| `device` | lo que la app dijo del móvil al confirmar (id, modelo, SO, versión de la app), si lo dijo |
| `verifiedAt`, `verifiedBy` | hora del servidor y qué servicio comprobó la firma |
| `howToVerify` | los tres comandos de OpenSSL que reproducen la comprobación |

El acuse guarda la referencia: `acknowledgement.signature.evidence = { path, sha256 }` (inventario)
y `signature.evidence` (documental). El reto también (`signing_challenges/{id}.evidence`).

**2. El acta (PDF), cuando se pide.** `reports` la dibuja a partir de la evidencia, con los
nombres resueltos (persona, DNI, equipo y ejemplar o documento), y la sube a
`checkbiz/reports/entities/{e}/acta_{challengeId}.pdf` la primera vez; después reutiliza el
fichero. Una página: quién, cuándo, desde qué móvil y con qué nivel; qué se firmó (la entrega
y cada documento con versión y hash, o el documento con su hash); el reto y la firma; la clave
pública y su huella y fecha de registro; la ruta y el SHA-256 de la evidencia; cómo verificarla
con OpenSSL; y la nota legal (firma electrónica avanzada según eIDAS, no cualificada).

| Ruta (`reports`, ID token de Firebase, mismo permiso que el informe de equipos) | Responde |
|---|---|
| `GET /api/reports/signatures/acta?entityId&challengeId` | `{ url, expiresAt }` del PDF (URL firmada, 5 min) |
| `GET /api/reports/signatures/evidence?entityId&challengeId` | `{ url, expiresAt, sha256 }` del JSON, para el perito |

**3. El informe «Equipos y EPIs»** gana la columna **«Firma»**: «Verificada (huella o cara ·
clave …)», «Verificada (desbloqueo del móvil · clave …)», «Declarada (desbloqueo del móvil,
sin firma)», «Contraseña, reautenticación verificada». Con el reto, para pedir el acta.

**4. Lo que el acta no prueba, y hay que decirle al cliente.**
- Que la clave viva en el chip seguro y esté atada a la huella lo **relata** la app; lo
  **probaría** la atestación del fabricante (reservado `key.attestation`). Siguiente mejora.
- Que esa huella sea de esa persona: lo prueba la vinculación cuenta ↔ móvil ↔ registro de la
  clave con la sesión del trabajador. Para que valga como firma, **el trabajador tiene que
  haber aceptado que confirmar con huella es su firma**: consentimiento en contrato o al dar
  de alta la app. Es del cliente; la app puede recogerlo en el primer inicio de sesión (pendiente,
  otra sesión).
- La hora es la del servidor, no un sello de tiempo cualificado. Suficiente para una
  inspección de trabajo; si un cliente necesita firma cualificada, es otra pieza con un
  prestador detrás.
- La base de datos la escribe el servidor (Admin SDK); al cliente la cierran las reglas
  (§Reglas). Por eso la evidencia sale **a Storage en el momento de firmar**, con su hash: una
  copia que no depende de que Firestore siga intacto.
- **Lo que pasó el 2026-10-09 lo demuestra**: la clave de prueba registrada por la mañana había
  desaparecido del registro por la tarde (quedaba solo la de un iPhone real registrada a las
  15:03 por la sesión de la app). Las reglas no paran al Admin SDK ni a la consola. El registro
  es «solo se añade» **por convención nuestra**: ningún script, limpieza ni prueba borra
  `signing_keys`; si hay que invalidar una clave, se marca `supersededAt`. Una firma hecha con
  una clave borrada ya no se puede volver a comprobar desde Firestore: solo desde su evidencia.

### Fuera de este paso

Atestación del chip (el formato ya reserva el campo), acta de firma en PDF, «no conforme»
en el documental, y el ajuste por empresa para exigir el nivel 1.

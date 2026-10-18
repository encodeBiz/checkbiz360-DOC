# Quiosco — fichar desde un dispositivo compartido del centro · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Fichajes (checklogs) y auth · checkbiz360 — modo quiosco · panel — activación del módulo y revisión
**Fecha de inicio:** 2026-10-18
**Estado:** **Diseño cerrado el 2026-10-18 · en implementación** en la rama `feat/quiosco` de la API, la app y el panel; nada desplegado ([03 §Estado](./03_contratos-api.md#estado-de-la-implementación-2026-10-18)). Jose, 2026-10-18: «hay que
investigarlo bien pero dejarlo cerrado hoy». Revisado el mismo día: **la foto pasa a la Fase 1
y es la prueba del fichaje** (Jose: «tenemos que hacer una prueba de fichaje, por ejemplo una
foto, porque ¿cómo garantizo que es el empleado correcto? En el ayuntamiento hay un caso en que
uno solo pasaba todas las tarjetas, y eso es inviable»). **Y por la tarde, la entrada:** el
quiosco es **un usuario con rol `kiosk`, uno por sucursal, creado solo al activar el módulo**;
al entrar con él en la app, el quiosco arranca; **sólo se activa a menos de 200 m de la
dirección de la sucursal** («eso es sumamente importante») y **en un solo dispositivo a la
vez** (Jose, 2026-10-18). Primer cliente que lo pide: Serlimar (CRM #3,
limpieza, 1.000 personas, 500 centros; piloto de 2-3 centros en negociación).
**Autor:** Jose Acevedo

---

## De dónde sale

Alberto Guasch (director general de Serlimar), 2026-10-17: «¿cómo se resuelve el fichaje cuando
un empleado no quiere fichar desde su móvil personal?». Serlimar no da terminal de empresa a
nadie (BYOD obligatorio), y una parte de la plantilla no aceptará poner la app en su móvil.
Jose respondió con un **modo quiosco**: un dispositivo compartido en el centro —tablet o móvil
económico— para quien no quiera usar el suyo, que convive con la app en el móvil propio. Guasch
pidió un ejemplo; no existe todavía. Este documento cierra qué es, cómo se identifica la
persona en él y por qué **no lleva biometría**.

Dos cosas estaban ya decididas antes de empezar, y este diseño las respeta:

- **Cero pasos para el operario, dos toques para el supervisor** (regla de la casa para flujos
  nuevos). En el quiosco: teclear un código y pulsar un botón. Nada más.
- **El rastro protege a la trabajadora, no la vigila** (ángulo con el que entró Serlimar).
  Lo que pongamos en una pared del centro tiene que poder explicarse con esa frase delante.

## Qué es

Una **tablet Android en la pared del centro**, con la app checkbiz360 en la que se ha entrado
con el **usuario de quiosco de esa sucursal** (nace solo al activar el módulo, y sólo entra a
menos de 200 m del centro y en un dispositivo a la vez). La persona **acerca su QR a la cámara** (una tarjeta impresa,
o el QR de la app en su móvil) **o teclea su código personal de 6 dígitos**, ve su nombre y su
cara en la cámara, y pulsa **Entrar**, **Salir** o **Pausa**: **en ese momento la tablet hace
la foto** y la guarda con el fichaje. Jose, 2026-10-18: «un QR ahorra tiempo y es más ágil»;
el código queda para quien no lleve la tarjeta encima. El servidor crea el fichaje con la misma
lógica que el de la app (calendario, turno, secuencia, horario por tareas), con la
geolocalización de la sucursal, la marca de que entró por el quiosco y la foto como prueba.

**Tablet o móvil, da igual** (Jose, 2026-10-18). Lo que se exige es del dispositivo, no del
tamaño: GPS con posición de 100 m o mejor, cámara frontal y Android 10 o iOS 15 en adelante. Un
Android económico en un soporte de pared vale; para una fila de gente se agradece una pantalla
de 8" o más. En iPhone queda en vertical (la app sólo admite vertical en iPhone). Donde este
documento dice «tablet», léase «el dispositivo del quiosco».

Lo que **no** es: no es un lector de huella ni de cara, no es un login de empleado en un
dispositivo ajeno, y no es una cuenta del panel con contraseña en una tablet compartida.

## Principio de diseño

> **El quiosco identifica a la persona con algo que no es su cuerpo: un código, una tarjeta o su
> propio móvil. La prueba de que era ella es una foto que mira un humano, nunca una máquina. La
> biometría, si la hay, vive en el móvil de la persona y nunca llega a la plataforma. El
> servidor decide y escribe; la tablet sólo pregunta y enseña.**

Razones en [ADR-001](./adr/ADR-001-sin-biometria-en-el-quiosco.md) (por qué sin biometría),
[ADR-002](./adr/ADR-002-la-llave-es-la-clave-de-firma-no-una-passkey.md) (qué hace el móvil
propio, y por qué no una passkey WebAuthn) y
[ADR-003](./adr/ADR-003-usuario-de-quiosco-por-sucursal-radio-y-un-dispositivo.md) (el usuario
de quiosco, el radio de 200 m y el dispositivo único).

## Alcance

**Dentro (Fase 1, lo que vale para el piloto de Serlimar):**

- Un usuario con rol `kiosk` por sucursal, creado automáticamente al activar el módulo (y al
  crear una sucursal con dirección mientras esté activo). Entrar con él en la app arranca el
  quiosco; sólo a menos de 200 m de la sucursal y en un dispositivo a la vez.
- QR personal por empleado (tarjeta impresa desde el panel, y el mismo QR en la app en «Mi QR»)
  y código personal de 6 dígitos, generados en el panel, únicos en la empresa.
- Modo quiosco en checkbiz360: una sola cámara que **lee el QR y hace la foto**, teclado para el
  código, confirmación con nombre, tres botones, **foto al pulsar**.
- Ruta nueva en `checkinbiz` que crea el fichaje en nombre del quiosco, con la lógica de siempre
  y la foto guardada con él.
- **Detección de ráfagas** en el servidor (varios fichajes seguidos en la misma tablet) y
  **revisión** en el panel: las fotos del día por centro, y marcar «no es la persona» en dos
  toques (§La prueba).
- Bloqueo de la tablet en la app (lock task / fijación de pantalla) y pantalla siempre encendida.
- La marca `source: kiosk` en el fichaje, visible en el panel y en los informes.

**Después (Fases 2 y 3, cuando un cliente lo pida):**

- Tarjeta o llavero NFC como alternativa al QR, **siempre con foto** (Fase 2; la tablet tiene
  que llevar NFC). Con el QR impreso, el NFC sólo aporta leer sin apuntar; se hace si un cliente
  ya tiene tarjetas NFC.
- Cola local cuando la tablet se queda sin red (Fase 2).
- El móvil propio como llave en el quiosco: QR en la tablet, firma con la clave del chip del
  móvil (Fase 3; ADR-002).
- Aprovisionamiento a escala con Android Management API (dispositivo dedicado) y Single App
  Mode en iOS (Fase 3).

**Fuera, y no va a entrar:**

- Huella o cara en la tablet, o plantillas biométricas en el servidor (ADR-001).
- Un quiosco multi-sucursal: una tablet, una sucursal. Quien trabaja en dos centros ficha en el
  quiosco de cada uno; `checklog/different_branches` sigue mandando.
- Rescatar el «kiosco QR» del panel (`/tools/checking`): es la versión web de la app para
  **una** persona con su `customToken`, hoy redirigida a mantenimiento. No es un dispositivo
  compartido y no sirve de base.

---

## Lo que hay hoy (As-Is)

Verificado contra el código el 2026-10-18.

### El fichaje y su lógica viven en el servidor, pero en el controlador

`POST /api/v1/checkinbiz/checklogs`
(`services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts`). Admite dos
puertas: JWT de empleado (`JWT_2FA_SECRET`, lo emite `/auth/validate`) o ID token de Firebase con
`isAdmin: true` y `canWrite`. Dentro del controlador, en este orden: empleado y responsabilidad en
la sucursal, **dispositivo de confianza** (`base64(user-agent)` contra `trustedDevicesId`, salvo
`isAdmin`), sucursal activa, zona horaria propia, hora pedida (sólo `isAdmin`), calendario
efectivo, geocerca, secuencia, horario por tareas, y escritura con `metadata` congelada
(`tz`, `distance`, `scheduleApplied`, `requestUpdates`…). Contrato en
[checklogs-http/03](../checklogs-http/03_contratos-api.md).

Lo que el quiosco necesita es **todo eso menos dos pasos** (dispositivo de confianza y geocerca)
**más una marca**. Hoy no se puede reutilizar sin copiarlo: el núcleo está en el controlador, no
en el caso de uso `CreateChecklog`, que sólo escribe.

`metadata.geoSource` ya existe con un valor, `branch_autofill` (la jornada manual pone la
geolocalización de la sucursal). El quiosco añade el segundo.

### La llave en el móvil ya existe

[firma/README](../firma/README.md): al terminar el login, la app crea una clave ECDSA P-256 en el
chip seguro del móvil, por empleado y por móvil, desbloqueada con huella o cara (`biometric`) o
con el PIN del móvil (`device_credential`), y la registra con `POST /auth/signing-keys`. Firmar
es pedir un reto (`POST /auth/signing-challenges`, `purpose` + `subject`), firmar el `payload`
tal cual y mandar `{ challengeId, signature }`; `verifySignedChallenge` en `shared` comprueba,
deja evidencia en Storage y hay acta en PDF. Probado en staging, 27 casos de QA en verde. **La
plataforma nunca ve la huella: ve una firma.** Es la pieza que hace innecesaria cualquier
biometría nuestra (ADR-002).

### No hay nada de quiosco

Ni en `checkinbiz` ni en `shared` hay dispositivo de quiosco, código de empleado ni ruta de
fichaje por terceros. El empleado tiene `enableA2F`, `trustedDevicesId`, `biometricRequired`
(hoy sólo lo devuelve `/auth/validate`) y `customToken`; ninguno sirve de código de quiosco.
La app no lleva `kiosk_mode`, cámara, lector de QR, NFC ni `wakelock`.

### El móvil no rastrea en segundo plano, y conviene saberlo para Serlimar

Compromiso adquirido con Guasch el 2026-10-17: la ubicación sólo al fichar, sin GPS en segundo
plano. **Se sostiene:** el manifiesto Android pide `ACCESS_FINE_LOCATION` y `ACCESS_COARSE_LOCATION`
y **no** `ACCESS_BACKGROUND_LOCATION`; `base_location` fija `requiresBackgroundPermission: false`.
Lo que contradice el compromiso es la **guía de instalación de cliente**
(`DOCS/Clients/10-app-movil/69-descarga-e-instalacion.md`, líneas 49 y 57), que pide conceder
la ubicación «Siempre»: ese permiso ni se solicita ni se puede conceder en Android 10+. Hay que
corregir el texto a «Mientras se usa la app» antes de la llamada (no se ha tocado en este cierre).

---

## El marco legal, en una página (ADR-001 lo razona)

Guía de la AEPD «Tratamientos de control de presencia mediante sistemas biométricos»
(23-11-2023), leída entera el 2026-10-18:

- Huella o cara para fichar es **categoría especial** y **alto riesgo**: hace falta levantar la
  prohibición del art. 9 **y** una EIPD previa que supere idoneidad, necesidad y proporcionalidad.
- En lo laboral, **el consentimiento no vale** (desequilibrio) y el Estatuto de los Trabajadores
  **no basta** como norma habilitante: haría falta ley específica o convenio que lo regule.
- El responsable «debe justificar que el empleo de otros sistemas existentes como tarjetas,
  certificados, claves, sistemas contact-less, etc. que evitan el tratamiento de categorías
  especiales de datos no son adecuados» (pág. 16). Y si existen esas alternativas para todos,
  «el procesamiento de datos biométricos deja de ser necesario».
- Una **fotografía** no es dato biométrico mientras no se trate «con medios técnicos
  específicos» para identificar o autenticar (considerando 51 RGPD, citado en la guía): la foto
  que mira un encargado en una disputa no es biometría; un reconocimiento facial sí.
- Primera sanción tras la guía: 365.000 € por fichar con biometría (arts. 13, 32 y 35 RGPD).
  Iberia retiró la biometría y la sustituyó por tarjetas.

- La guía admite expresamente la **intervención humana** como parte del control: «no existe una
  obligación a que se implementen exclusivamente con medios tecnológicos. Dicha intervención
  humana puede ser el adecuado…» (pág. 16). La revisión de fotos por el encargado es eso.

Conclusión operativa: **un código o una tarjeta es la alternativa que la propia AEPD pone como
vara de medir, y la foto revisada por una persona es la garantía que la guía prefiere a la
máquina.** Vender un quiosco con huella sería vender al cliente una EIPD, un convenio y una
multa en potencia. La huella que sí puede haber es la del móvil de la persona, desbloqueando su
clave, igual que desbloquea el móvil: la plataforma no trata biometría en ningún caso. Esto es
nuestra lectura de ingeniería; el DPO del cliente la confirma, no la sustituye.

---

## Diseño (To-Be)

### 1. Entrar: el usuario de quiosco de la sucursal (ADR-003)

**Nace con el módulo.** Al activar «Quiosco» en la empresa, el servidor crea **un usuario por
sucursal con dirección**: cuenta de Firebase Auth con correo no enrutable
(`quiosco.<branchId>@kiosk.checkbiz360.com`), contraseña generada, claims `{ kind: "kiosk",
entityId, branchId }`, y el documento `entities/{e}/kiosks/{branchId}`. Cada sucursal nueva
con dirección recibe el suyo mientras el módulo esté activo; una sucursal **sin
geolocalización no tiene quiosco** hasta que tenga dirección, porque sin centro no hay radio.
El panel enseña, en Sucursal → **Quiosco**, el correo y la contraseña (con «Regenerar
contraseña», que expulsa al dispositivo activo), el estado y el dispositivo.

**Entrar es el login de siempre.** En la tablet, la pantalla de login de la app, con ese correo
y contraseña. `POST /auth/login` reconoce el claim `kind: "kiosk"` y, en vez de la sesión de
empleado, responde `{ kind: "kiosk", kioskToken, branch: { id, name, timeZone, geo },
entity: { id, name }, activationRadiusMeters }`. La app guarda el token en almacenamiento seguro
y arranca el modo quiosco: **no hay 2FA, ni dispositivo de confianza, ni nada de la sesión de
empleado**. El usuario de quiosco no abre el panel ni ninguna otra ruta: su token sólo vale
para `identify`, `checklogs/kiosk` y `unlock`.

**El dispositivo tiene que cumplir los requisitos; si no, «dispositivo no válido».** Jose,
2026-10-18: «cuando la tablet no tiene GPS correcto, lo avisa: dispositivo no válido, no admite
tal cosa o no cumple con los requisitos». Antes de pedir nada al servidor, la app comprueba el
dispositivo y, si falla algo, enseña **«Este dispositivo no cumple los requisitos del
quiosco»** con el motivo concreto y **no entra**:

| Requisito | Cómo se comprueba | Motivo que se enseña |
|---|---|---|
| Ubicación encendida y permiso concedido a la app | servicios de ubicación activos; permiso «mientras se usa» | «Ubicación desactivada» / «Sin permiso de ubicación» |
| **Posición correcta**: una lectura con precisión **≤ 100 m** en menos de 30 s | `base_location`, mejor lectura en la ventana | «Este dispositivo no obtiene una posición precisa (±350 m)» |
| Cámara frontal | lista de cámaras del dispositivo | «Sin cámara frontal» |
| Android 10 o iOS 15 en adelante, y la app al día | versión del sistema y de la app | «Sistema no admitido» |

El servidor lo comprueba otra vez con lo que recibe en el login (`geo.accuracy`, `device`):
precisión por encima de la permitida → 400 `kiosk/device_not_eligible` con `reason`. La
precisión exigida (100 m) es un ajuste de plataforma, no de cliente. Una tablet wifi sin GPS
que se ubique por red con 20-50 m pasa; una que dé ±500 m, no, y es la tablet la que no vale,
no el sitio. La guía de compra lo dice: **tablet con GPS** (los modelos con SIM lo llevan).

**Sólo en el centro: 200 m.** Con el dispositivo válido, la app manda la posición
(`geo`, con `accuracy`) y el servidor comprueba la distancia a `branch.address.geo`:
más de `activationRadiusMeters` (**200 m por defecto**, ajustable por sucursal entre 50 y 500)
→ 403 `kiosk/out_of_radius` con la distancia, y la tablet lo dice: «Este quiosco sólo se activa
en <sucursal>». Además:

- **Al arrancar la app** (y una vez al día en segundo plano) la tablet repite la comprobación
  de requisitos y manda su posición (`POST /auth/kiosk/heartbeat`). Si deja de cumplir
  (apagaron la ubicación, ya no hay posición precisa) o está fuera del radio, el servidor pone
  el quiosco en `suspended`, la pantalla se bloquea con el motivo («Dispositivo no válido:
  ubicación desactivada» / «Este quiosco sólo funciona en <sucursal>») y avisa a los
  administradores; vuelve sola cuando se cumple otra vez.
- **Con cada fichaje** viaja la posición de la tablet y queda en `metadata.kiosk.distance` y
  `accuracy`. Un fichaje **nunca falla** por una lectura puntual de la tablet (la persona está
  delante y la foto lo prueba); una lectura imprecisa o fuera del radio se marca
  (`metadata.kiosk.outOfRadius` / `lowAccuracy`) y, a la tercera seguida, el quiosco se
  suspende como arriba. Lo que se corta es el quiosco, no el fichaje.
- Por qué 200 m y no 50: incluso con GPS, en interior la posición baila decenas de metros. El
  radio protege contra llevarse el quiosco a otro sitio, no contra estar en la otra punta del
  centro.

**Un dispositivo a la vez.** `kiosks/{branchId}.device = { deviceId, model, os, appVersion,
activatedAt, lastSeenAt }`. Entrar desde otro dispositivo **sustituye** al anterior: el nuevo
queda activo, el viejo recibe 401 `kiosk/replaced` en su siguiente petición, borra su token y
vuelve al login con «Este quiosco se ha activado en otro dispositivo», y los administradores
reciben el aviso (`kiosk_device_replaced`, con modelo y hora). Sustituir y no rechazar, porque
la tablet rota o perdida es el caso normal y no debe exigir un paso en el panel; y porque
quien sustituye ha tenido que estar en el centro con la contraseña, y lo que gana es lo mismo
que ya podía hacer en la tablet. Desde el panel, «Cerrar sesión del dispositivo» deja el
quiosco sin dispositivo hasta el siguiente login.

**La contraseña en la tablet no es el problema que era.** Sola no sirve de nada: sólo entra a
menos de 200 m del centro, sólo en un dispositivo (y avisa), y sólo para identificar y fichar.
Y se regenera desde el panel en un clic.

- Salir del modo quiosco en la propia tablet: código de 6 dígitos de un **administrador de la
  entidad** (se comprueba en el servidor, `POST /auth/kiosk/unlock`), además del bloqueo del
  sistema (§5). También cerrar la sesión del dispositivo desde el panel.

### 2. Identificarse: QR o código

**El QR es la tarjeta.** Cada empleado tiene un QR personal: una cadena opaca de 20 caracteres
(`CB360:<entityIdCorto>:<token>`, 128 bits aleatorios en base32), que el panel imprime en una
tarjeta con su nombre (PDF con las tarjetas de una sucursal, formato tarjeta de visita, para
plastificar) y que la app enseña en «Mi QR» a quien la tenga. El QR **no contiene el código** ni
nada legible: una foto de la tarjeta sólo sirve para fichar por esa persona, y para eso la
cámara ya tiene su cara. Se guarda `employees/{id}.kioskQr = { hmac, issuedAt, issuedBy }`;
perderla es «Regenerar QR» en la ficha y reimprimir, igual que una tarjeta de acceso.

- Por qué QR impreso y no NFC: la **misma cámara** que hace la foto lo lee, cualquier tablet
  vale, cuesta lo que cuesta imprimir, y el gesto es el de siempre: acercar la tarjeta. Lo que
  pierde frente al NFC (hay que apuntar) se compensa con que no hay hardware que elegir.
- Desde la app, «Mi QR» es el mismo QR de la tarjeta. Quien lleva la app fichará normalmente con
  el móvil y la geocerca; «Mi QR» es para el centro que quiere que todos pasen por la pared.

**Los QR se generan solos al activar el módulo, por lotes.** Jose, 2026-10-18: «al activar
esto se generan automáticamente los QR de cada empleado, en lotes, no todos a la vez, si no
es una locura en una empresa de miles de empleados». Activar el módulo encola un trabajo
`kiosk.setup` por empresa que recorre la plantilla activa **en lotes de 200 empleados por
tarea** (Cloud Tasks, una tarea por lote encadenada a la siguiente, el mismo patrón de
[programadas-a-escala](../programadas-a-escala/README.md)), genera el QR de quien no lo tenga
y escribe el avance en `entities/{e}/kiosks_setup = { total, done, status, startedAt,
finishedAt }`. Mil empleados son cinco lotes y menos de un minuto; el panel enseña «Generando
QR: 600 de 1.000» y no bloquea nada. Idempotente: se puede relanzar y sólo toca a quien falte.
Mientras el módulo esté activo, **cada empleado nuevo nace con su QR** (en el alta, dentro
del mismo caso de uso), y los que entran por alta masiva lo reciben en el mismo lote de alta.
Las tarjetas (PDF) no se generan al activar: se piden por sucursal cuando se van a imprimir.

**El código es el respaldo.** `employees/{id}.kioskCode = { hmac, updatedAt, updatedBy }`. Seis
dígitos, **único en la empresa**, generado por el servidor al pulsar «Generar código de
quiosco» en la ficha del empleado (o para toda la plantilla de una sucursal de una vez). Se
enseña **una sola vez** al administrador, que lo entrega en papel; se puede regenerar; el
trabajador lo ve también en la app en «Mi código de quiosco», si la tiene. Sirve para quien se
dejó la tarjeta. No se genera en lote: un código que nadie ve no sirve, y el QR ya cubre a todos.
- Se guarda `HMAC-SHA256(secreto del servidor, entityId + código)`, no el código. Un espacio de
  un millón de valores no lo protege ningún hash lento: lo protege que la búsqueda sea por
  igualdad con un secreto que no está en la base de datos, y el límite de intentos.
- **Límite de intentos:** cinco códigos fallidos en un minuto por quiosco bloquean el teclado
  60 segundos (el servidor responde `kiosk/too_many_attempts` con `retryAfter`); diez en diez
  minutos avisan al administrador. Todos los intentos quedan en `entities/{e}/kiosks/{k}/attempts`.
- Por qué QR o código y no «elegir mi nombre en una lista»: una lista en una pared enseña la
  plantilla del centro a cualquiera, y elegir un nombre ajeno no cuesta nada. El QR y el código
  son **suyos**, se cambian en un clic y queda registrado quién los usó dónde y cuándo.
- Las dos vías llegan al mismo sitio: `identify` con `{ qr }` o con `{ code }`, y de ahí en
  adelante no hay diferencia. El fichaje apunta cuál fue (`identification: "qr+photo"` o
  `"code+photo"`).

### 3. Fichar

Dos llamadas, para que la tablet pueda enseñar el nombre antes de escribir nada:

**`POST /kiosk/identify`** (kiosk token) `{ qr }` **o** `{ code }` →
`{ sessionId, employee: { id, firstName }, suggested: "checkin" | "checkout" | "restin" | "restout",
   expiresAt }`. `sessionId` vive **60 segundos** y se usa una vez. `suggested` sale del último
fichaje del empleado (la misma regla que la app y el panel). QR o código desconocidos → 404
`kiosk/code_not_found` (sin decir si existe en otra empresa). Un QR de otra empresa es
desconocido: el `hmac` lleva el `entityId` del quiosco.

**`POST /checklogs/kiosk`** (kiosk token, `multipart/form-data`) `{ sessionId, type, photo }` →
`201 { code: "checklog/created", checkLog }`, o los mismos errores del fichaje de siempre (`checklog/out_of_schedule`,
`checklog/two_type_followed`, `checklog/day_disabled`…), que la tablet enseña con el texto que ya
tiene la app para cada código.

Lo que hace el servidor, en `checkinbiz`, **con el mismo núcleo que `POST /checklogs`**:

1. Extraer de `createChecklog.controller.ts` el tramo «empleado, responsabilidad, sucursal, zona,
   calendario, secuencia, horario por tareas, escritura y eventos» a un servicio de aplicación
   (`application/use-cases/checklog/RegisterChecklog.ts`) que recibe **un actor**:
   `{ kind: "employee", deviceId }`, `{ kind: "admin", uid, requestedAt? }` o
   `{ kind: "kiosk", branchId, deviceId, identification }`. El controlador de siempre y el del quiosco lo
   llaman; no hay tercera copia (misma regla que
   [checklogs-http ADR-003](../checklogs-http/adr/ADR-003-promocion-a-shared-sin-tercera-copia.md)).
2. Para el actor `kiosk`: **no** se comprueba dispositivo de confianza (el dispositivo es el
   quiosco, ya activado en el centro) y **no** se evalúa geocerca del empleado: `geo = branch.address.geo`,
   `metadata.geoSource = "kiosk"`, `metadata.distance = 0`. La hora es la del servidor.
3. **La foto.** Obligatoria mientras la empresa tenga la prueba activada (y lo está por
   defecto): sin `photo`, 400 `kiosk/photo_required`. Se guarda en el **bucket europeo**
   `encodebiz-media-eu`, en `kiosk/r{retención}/{entityId}/{checklogId}.jpg` (JPEG, 640 px de
   lado mayor, unos 60 KB) **antes** de escribir el fichaje, sumando al contador de
   almacenamiento de la empresa ([almacenamiento/README](../almacenamiento/README.md)); si la
   subida falla, no hay fichaje y la tablet lo dice.
4. Marca: `metadata.source = "kiosk"` y `metadata.kiosk = { branchId, deviceId, identification: "qr+photo" |
   "code+photo" | "nfc+photo" | "device_signature", sessionId, photoPath, burst?: { windowSeconds, count } }`.
   El `requestUpdates[0]` lleva `action: "created"` y `updateBy: "kiosk:<branchId>"`.
5. **Ráfaga.** Al escribir, el servidor cuenta los fichajes de esa tablet en los últimos 90 s.
   Si con éste son **tres o más**, marca `metadata.kiosk.burst` en todos ellos y avisa al
   supervisor de la sucursal (push + in-app `kiosk_burst_review`, con enlace a la revisión). No
   rechaza nada: diez personas que entran a las 8:00 en fila también son una ráfaga, y la
   diferencia la ve el encargado en las fotos en un segundo.
6. Se emiten los mismos eventos (`emitChecklogCreated`, `emitWorkdayClosed`) y los triggers de
   Firestore siguen igual: heurística, sync, webhooks y notificaciones no se enteran de que fue
   un quiosco salvo por la marca.

`CheckLog.metadata.geoSource` pasa de `"branch_autofill"` a `"branch_autofill" | "kiosk"`, y
`metadata.source?: "app" | "web" | "admin" | "kiosk"` se añade sin tocar a nadie (lo que no lo
lleva es «app»). El panel enseña «Quiosco» en la fila del fichaje y el informe de asistencia
gana la columna.

### 4. La tablet (checkbiz360, feature `lib/features/kiosk`)

Misma app, misma tienda: un **modo**, no una app aparte (ADR-003 §Por qué la misma app). Arranca
en modo quiosco si hay `kioskToken` guardado (y comprueba la posición, §1); si no, la app de
siempre, y el login decide por el claim del usuario.

Pantallas, en orden, y sin más:

| Pantalla | Qué enseña | Qué hace |
|---|---|---|
| **Entrar** | la pantalla de login de la app, con el usuario de quiosco de la sucursal | comprueba los requisitos del dispositivo (§1); si no cumple, «Dispositivo no válido» con el motivo y no entra; si cumple, `login` con la posición; fuera del radio, lo dice y no entra |
| **Inicio** | hora grande, nombre del centro, **la cámara frontal en vivo** con el marco «Acerca tu QR», y el teclado numérico 0-9 debajo o al lado («o teclea tu código») | al leer un QR, o al sexto dígito, llama a `identify` sola (sin botón «OK»); vibración y pitido corto al leer |
| **Confirmar** | «Hola, Marta», la hora, **la cámara frontal en vivo** («tu foto queda con el fichaje»), y el botón grande que toca (`suggested`) con los otros dos pequeños debajo | al pulsar, **captura el fotograma** y llama a `checklogs/kiosk`; **se cancela sola a los 10 segundos** |
| **Hecho** | check verde con la foto en miniatura, «Entrada registrada 08:02», 3 segundos | vuelve a Inicio |
| **Error** | el texto del código (`checklog/out_of_schedule` → «Fuera de tu turno. Avisa al encargado») | vuelve a Inicio a los 5 segundos |

La cámara en vivo no es adorno: quien ficha se ve a sí mismo y sabe que esa imagen queda. Es la
disuasión que una tarjeta no tiene. **Una sola cámara para las dos cosas:** el flujo de `camera`
(cámara frontal, sin flash, sin sonido) alimenta el lector de QR (`google_mlkit_barcode_scanning`
sobre los fotogramas, sólo formato QR) en Inicio y la captura en Confirmar, sin cambiar de
cámara entre pantallas: del QR a la foto no pasa ni un segundo. Si ML Kit da guerra en la
tablet del piloto, el respaldo es `mobile_scanner` con cámara frontal en Inicio y `camera` en
Confirmar, a costa de un cambio de cámara. La foto se reduce en la tablet y no se guarda en el
dispositivo tras enviarla. Con QR el fichaje son **un gesto y un toque**: acercar la tarjeta,
pulsar el botón grande.

Reglas: pantalla siempre encendida (`wakelock_plus`), nada de drawer, bottom nav ni Firebase
Auth de empleado (el `logoutInvalidationProvider` no interviene: no hay sesión de usuario), texto
y botones grandes (mínimo 56 dp), orientación libre, l10n como todo lo demás, el logo animado de
`LoadingPlaceholder` mientras espera. Sin red: «Sin conexión. Avisa al encargado» y **nunca** un
check verde falso; la cola local es Fase 2.

Salir del modo quiosco: pulsación larga 3 s sobre el logo → código de administrador → `unlock` →
se borra el token y se vuelve al login. Cerrar la sesión del dispositivo o regenerar la
contraseña desde el panel hace lo mismo sin tocar la tablet.

### 5. Que la tablet no sirva para otra cosa

- **Android, piloto:** paquete `kiosk_mode` (mews, 0.8.0): `startKioskMode()` entra en Lock Task;
  sin Device Owner cae a **fijación de pantalla**, que el sistema pide confirmar una vez y de la
  que sólo se sale con el PIN del dispositivo. Suficiente para 2-3 centros: el PIN lo tiene el
  encargado.
- **Android, escala (Fase 3):** dispositivo dedicado con **Android Management API** (política con
  `kioskCustomization` y nuestra app como única permitida; aprovisionamiento por QR al encender
  la tablet). No exige MDM de pago; Google no cobra la API a día de hoy (confirmar antes de
  prometerlo). Con eso Lock Task es real y la tablet no sale ni con reinicio.
- **iOS:** Acceso Guiado (triple clic, código) para el piloto; Single App Mode con Apple
  Configurator o Apple Business Manager para escala. No hace falta código nuestro.
- Hardware recomendado para el piloto: tablet Android de 8-10" económica (gama Galaxy Tab A o
  Lenovo Tab M, 120-180 €), **con NFC** si se quiere la Fase 2 sin cambiar de aparato, soporte de
  pared con alimentación, y SIM de datos o wifi del centro. La tablet es del cliente; nosotros
  no gestionamos hardware.

### 5 bis. La prueba: foto, ráfagas y revisión (Fase 1)

El caso que hay que impedir tiene nombre: **una persona que pasa todas las tarjetas**. Ni el
código ni la tarjeta lo impiden; lo impide que cada fichaje lleve la cara de quien pulsó y que
alguien la mire cuando toca. Tres piezas, las tres en la Fase 1:

1. **La foto con cada fichaje.** Se hace al pulsar el botón, con la cámara en vivo delante. La ve
   sólo quien puede ver el fichaje (supervisor de la sucursal o superior, administrador), desde
   la fila del panel y desde la revisión, con URL firmada de cinco minutos. **No hay
   reconocimiento de ningún tipo, ni ahora ni después** (ADR-001): la foto está para que la
   mire un humano. Retención **30 días** por regla de ciclo de vida del bucket, elegible por
   empresa entre 15 días y 4 años, viendo lo que ocupa y lo que cuesta
   ([almacenamiento/README §3](../almacenamiento/README.md)); el fichaje sobrevive a la foto y
   conserva `photoPath` como rastro de que la hubo. Si hay una disputa abierta sobre ese
   fichaje (solicitud de corrección pendiente o rechazada), la foto se conserva hasta cerrarla.
2. **La ráfaga.** Tres o más fichajes en 90 s en la misma tablet se marcan y avisan al
   supervisor (§3). No se rechaza ninguno: la fila de las 8:00 es legítima y la diferencia está
   en las fotos. El aviso dice «7 fichajes seguidos en el quiosco de Edificio Colonial, 08:02.
   Revisa las fotos» y abre la revisión con esos siete en pantalla.
3. **La revisión en el panel.** Sucursal → Quiosco → **Revisar**: las fotos del día en
   cuadrícula, con nombre, hora y tipo, las ráfagas agrupadas arriba. **Dos toques:** tocar una
   foto y «No es la persona» → el fichaje pasa a `failed` con `rejectionReason: "kiosk_identity"`,
   queda en `requestUpdates`, la persona recibe el aviso de siempre y el código de quiosco de
   ese empleado se regenera (quien lo tenía ya no lo tiene). «Es correcto» no hace nada: no se
   exige revisar lo que no llama la atención. Para 500 centros nadie va a mirar mil fotos al día,
   y no hace falta: se miran las ráfagas y las disputas, y el resto está ahí por si acaso.

Lo que esto garantiza y lo que no, para decirlo igual al cliente: garantiza que **cada fichaje
del quiosco tiene la cara de quien lo hizo** y que **el patrón del ayuntamiento salta solo**.
No garantiza identificar a la persona sin que nadie mire; eso sería reconocimiento facial, y es
lo que la AEPD ha cerrado. La empresa que lo apague (`entity.settings.kiosk.photo: false`,
sólo desde el panel, con un aviso de que se queda sin prueba) ficha con código solo y asume el
caso del ayuntamiento; viene encendido.

Qué le exige al cliente: informar a la plantilla (art. 13 RGPD: finalidad, quién la ve, cuánto
dura) y, con comité, la consulta del art. 64 ET. Es un dato personal corriente, **no** de
categoría especial (considerando 51 RGPD, citado en la guía de la AEPD), mientras ninguna
máquina la procese para identificar. El panel enseña el texto modelo al activar el quiosco; lo
valida el DPO del cliente.

### 6. Fase 2: NFC y cola local

- **NFC:** `employees/{id}.nfcTags[]` con el UID de la tarjeta, dado de alta acercándola a la
  propia tablet desde un modo de administrador. Acercar la tarjeta sustituye al código (la
  empresa decide si además pide el código: posesión + conocimiento). **La foto no se sustituye
  nunca**: la tarjeta es justo lo que se pasaba en el ayuntamiento. Sólo Android con NFC.
- **Cola local:** fichajes guardados en la tablet con `clientTimestamp` **y su foto** cuando no
  hay red y enviados al volver, en orden. El servidor acepta `timestamp` del actor `kiosk` sólo hacia
  atrás y hasta 24 h (la vía de administrador ya acepta hora pedida; es la misma comprobación de
  «no en el futuro»), y marca `metadata.timeSource = "kiosk_queue"`.

### 7. Fase 3: el móvil propio como llave en el quiosco (ADR-002)

Para quien sí lleva la app, el quiosco puede ser también un punto de fichaje sin teclear nada:
la tablet enseña un QR que rota cada 30 s (`{ branchId, deviceId, nonce }`), la app lo lee («Fichar en el
quiosco»), pide un reto con `purpose: "checklog.kiosk"` y `subject: { branchId, deviceId, nonce,
type }`, lo firma con la clave del chip (huella o cara **en su móvil**) y manda
`POST /checklogs/kiosk-signed { challengeId, signature, type }`. El servidor verifica con
`verifySignedChallenge` y crea el fichaje con `identification: "device_signature"` y la
evidencia de siempre. Aquí **no hace falta foto**: la firma del chip del móvil de la persona,
con su huella, prueba más que una imagen, y la hace quien más fácil lo tenía. Es el mismo mecanismo que firma una nómina: no hay nada nuevo que
inventar, sólo un `purpose` más y un lector de QR en la app. No entra en el piloto porque no
resuelve la objeción de Serlimar (quien no quiere la app no la va a sacar delante de la tablet).

---

## Modelo de datos

```text
entities/{entityId}/kiosks/{branchId}                       # uno por sucursal, lo crea el módulo
  uid (usuario de Firebase Auth, claims { kind: "kiosk", entityId, branchId }), email,
  status: active | suspended | disabled, activationRadiusMeters: 200,
  device?: { deviceId, model, os, appVersion, activatedAt, activatedGeo, lastSeenAt, lastGeo },
  createdAt, passwordRotatedAt?, suspendedAt?, suspendedReason?: out_of_radius
  settings: { methods: ["code"] | ["code","nfc"] }

entities/{entityId}.settings.kiosk = { photo: true, photoRetention: 30 }   # 15|30|60|90|365|1460
entities/{entityId}/kiosks_setup = { total, done, status, startedAt, finishedAt }   # QR por lotes
entities/{entityId}.storage = { usedBytes, byModule, includedGb, packsGb }   # almacenamiento/README

entities/{entityId}/kiosks/{branchId}/attempts/{id}         # sólo los fallidos y los bloqueos
  at, codeHmacPrefix (4 hex), result: not_found | locked

kiosk_sessions/{sessionId}                                  # raíz, 60 s, de un solo uso
  branchId, deviceId, entityId, employeeId, suggested, expiresAt, usedAt?

employees/{employeeId}.kioskQr   = { hmac, issuedAt, issuedBy }        # la tarjeta y «Mi QR»
employees/{employeeId}.kioskCode = { hmac, updatedAt, updatedBy }      # el respaldo
employees/{employeeId}.nfcTags = [ { uid, label, addedAt } ]                     # Fase 2

entities/{e}/checklogs/{id}.metadata
  source: "kiosk", geoSource: "kiosk", distance: 0,
  kiosk: { branchId, deviceId, identification, sessionId, photoPath, distance, outOfRadius?,
           burst?: { windowSeconds: 90, count } }

Storage (bucket encodebiz-media-eu, europe-west1): kiosk/r{días}/{entityId}/{checklogId}.jpg
  · una regla de ciclo de vida por carpeta de retención · kiosk/hold/{entityId}/ para disputas
```

Reglas de Firestore: `kiosks/**` y `kiosk_sessions/**` sin acceso
desde cliente; `employees.kioskCode` y `nfcTags` sólo los escribe el servidor (misma convención
que `signingKey`, [firma/README §Reglas](../firma/README.md)). Índice: `employees` por
`(entityId, kioskCode.hmac)` y `(entityId, kioskQr.hmac)`.

## Contratos (resumen)

| Ruta (`checkinbiz`) | Auth | Para qué |
|---|---|---|
| `POST /entities/:id/modules/kiosk` · `DELETE …` | ID token, `canWrite` | activar el módulo (crea los usuarios de quiosco y encola los QR por lotes) o desactivarlo (los deshabilita) |
| `GET /kiosks/setup?entityId` | ID token, `canWrite` | avance de la generación de QR `{ total, done, status }` |
| `GET /kiosks?entityId` | ID token, `canWrite` | por sucursal: correo, estado, dispositivo, última posición |
| `POST /kiosks/:branchId/password` | ID token, `canWrite` | regenerar la contraseña; responde **una vez**; expulsa al dispositivo |
| `DELETE /kiosks/:branchId/device` | ID token, `canWrite` | cerrar la sesión del dispositivo activo |
| `PATCH /kiosks/:branchId` | ID token, `canWrite` | `activationRadiusMeters` (50-500), `settings` |
| `POST /employees/:id/kiosk-code` | ID token, `canWrite` | generar o regenerar el código; responde el código **una vez** |
| `POST /employees/:id/kiosk-qr` | ID token, `canWrite` | generar o regenerar el QR; responde la cadena |
| `GET /kiosks/cards?entityId&branchId` | ID token, `canWrite` | PDF con las tarjetas QR de la sucursal (nombre + QR), para imprimir |
| `GET /employees/me/kiosk-qr` | JWT de empleado | la cadena para «Mi QR» en la app |
| `POST /auth/login` (el de siempre) | correo y contraseña del usuario de quiosco | con `geo`, `deviceId`, `device` → `{ kind: "kiosk", kioskToken, branch, entity, activationRadiusMeters }`; 403 `kiosk/out_of_radius` |
| `POST /auth/kiosk/heartbeat` | kiosk token | `{ geo }` → `{ status }`; fuera del radio, `suspended` |
| `POST /auth/kiosk/unlock` | kiosk token | `{ adminCode }` → 200 y token revocado |
| `POST /kiosk/identify` | kiosk token | `{ qr }` o `{ code }` → `{ sessionId, employee, suggested, expiresAt }` |
| `POST /checklogs/kiosk` | kiosk token, multipart | `{ sessionId, type, photo }` → `201 { checkLog }` |
| `GET /kiosks/review?entityId&branchId&date` | ID token, supervisor o superior | fotos del día con URL firmada, ráfagas agrupadas |
| `POST /checklogs/:id/kiosk-reject` | ID token, supervisor o superior | «No es la persona»: `failed`, aviso, código regenerado |
| `GET /checklogs/:id/kiosk-photo` | ID token, quien ve el fichaje | URL firmada de 5 min |
| `POST /checklogs/kiosk-signed` | kiosk token | Fase 3: `{ challengeId, signature, type }` |

Códigos nuevos: `kiosk/device_not_eligible` (400, con `reason`: `location_off` |
`location_denied` | `low_accuracy` | `no_front_camera` | `os_unsupported`),
`kiosk/out_of_radius` (403, con `distanceMeters` y `allowedRadiusMeters`),
`kiosk/no_branch_geo` (409, la sucursal no tiene dirección),
`kiosk/replaced` (401), `kiosk/suspended` (423), `kiosk/disabled` (401),
`kiosk/code_not_found` (404), `kiosk/too_many_attempts` (429, `retryAfter`),
`kiosk/session_expired` (410), `kiosk/unlock_invalid` (403), `kiosk/photo_required` (400),
`kiosk/photo_upload_failed` (502). Los de fichaje son los de siempre.
Añadirlos a `DOCS/Clients/14-referencia/90-codigos-de-error-completos.md` al implementar.

## Fases y tamaño

| Fase | Qué | Dónde | Tamaño (una persona) |
|---|---|---|---|
| 0 | Bucket europeo con reglas de ciclo de vida y contadores de almacenamiento ([almacenamiento/README](../almacenamiento/README.md) Fases 0 y 1) | infra + `shared` | 4 días |
| 1a | `RegisterChecklog` con actor; login de quiosco con radio y dispositivo único; activación del módulo con usuarios por sucursal y **QR por lotes con Cloud Tasks**; códigos; **foto al bucket europeo contada, ráfaga y aviso**; reglas e índice | `checkinbiz` + `shared` | 5 días |
| 1b | Activar el módulo; Sucursal → Quiosco (credenciales, regenerar contraseña, dispositivo activo y cerrar su sesión, radio, **Revisar** con fotos y «No es la persona», **Imprimir tarjetas QR**); «Generar QR» y «Generar código» en la ficha y en lote; texto modelo de información a la plantilla | panel | 3 días |
| 1b' | Columna «Quiosco» con miniatura en la asistencia del panel. Complemento: no bloquea el piloto | panel | 0,5 día |
| 1c | `lib/features/kiosk`: login que reconoce el usuario de quiosco (con ubicación), inicio **con lector de QR y teclado**, confirmar **con cámara**, hecho, error; «Mi QR» en el menú de la app; `camera` + ML Kit QR + `kiosk_mode` + `wakelock_plus`; salida con código de administrador; l10n es/en/pt | checkbiz360 | 5 días |
| 1d | QA contra staging (catálogo `Qa/catalogo/quiosco.md`: activación del módulo, dispositivo no válido por cada motivo, login dentro y fuera del radio, sustitución de dispositivo, códigos, límite de intentos, secuencia, **foto obligatoria, ráfaga, rechazo y regeneración del código**, revocación, bloqueo de pantalla); prueba en una tablet real | QA | 2 días |
| 2 | NFC · cola local con foto | todos | 4-5 días |
| 3 | QR + firma con el móvil · Android Management API | app + servidor | 4-5 días |

**Fase 1 completa: unas tres semanas de una persona, más cuatro días de almacenamiento que
sirven a toda la plataforma.** Para la videollamada con Guasch de esta
semana no hay quiosco que enseñar; se enseña este diseño (una pantalla basta: cámara, teclado,
nombre, tres botones) y se compromete dentro del piloto, no antes. No prometer fecha en la
llamada sin haber reservado esas tres semanas.

### Corte de demo (cinco días), si hace falta enseñarlo fichando antes del piloto

Jose, 2026-10-18: «esto es mucho trabajo para tenerlo la semana que viene». El corte que sí
cabe en una semana, y que después **se queda** porque es el principio de la Fase 1:

| Día | Qué | Qué se deja fuera |
|---|---|---|
| 1-1,5 | Servidor: login de quiosco con radio y dispositivo único, `identify` por QR y por código, `checklogs/kiosk` con foto al bucket europeo (creado a mano, con la regla de 30 días), apoyándose en el camino de administrador que ya existe | ráfagas, aviso, revisión, reglas nuevas, contadores de almacenamiento |
| 2-4 | App: login de quiosco con ubicación, inicio con lector de QR y teclado, confirmar con cámara, hecho, error; «Mi QR» | `kiosk_mode` (se fija la pantalla a mano), salida con código de administrador |
| 5 | Usuario de quiosco de la sucursal de demo, QR de sus empleados, tarjetas y códigos **por script** (PDF incluido), prueba en una tablet real dentro y fuera del radio | pantallas de panel: activar, credenciales, imprimir, revisar; la columna «Quiosco»; el lote con Cloud Tasks (el script lo hace en serie) |

La foto se ve en la demo abriéndola desde Storage, no desde el panel: la columna con miniatura
(1b') es un complemento y no entra en el corte.

## Qué le decimos al cliente (y a su DPO)

- El quiosco **no trata datos biométricos**: código, tarjeta o el móvil de cada persona. No hace
  falta EIPD por biometría ni convenio que la habilite.
- **La prueba es la foto**: cada fichaje del quiosco lleva la cara de quien pulsó, la mira un
  humano (nunca una máquina), 30 días y sólo quien puede ver el fichaje. Si uno pasa diez
  códigos seguidos, el encargado recibe un aviso con las diez fotos. Hay que informar a la
  plantilla, y su DPO lo valida; viene encendida.
- Cada fichaje del quiosco dice en qué tablet, con qué método y a qué hora de servidor se hizo:
  es el mismo rastro que protege a quien sí estuvo.
- La app en el móvil propio sigue sin rastrear en segundo plano; corregir la guía de
  instalación que dice «Siempre» (§As-Is) antes de la llamada.

## Riesgos y lo que no resuelve

- **Fichar por otro.** Con el código de un compañero se puede pulsar por él; lo que queda es
  **su propia cara** en ese fichaje, y si lo hace por varios, la ráfaga avisa al encargado el
  mismo minuto. Lo que no hay es una máquina que lo pare sola: eso sería reconocimiento facial.
  Decirlo así al cliente, con el caso del ayuntamiento delante.
- **Nadie mira las fotos.** En 500 centros es seguro. Por eso la revisión no es «mirarlo todo»:
  es mirar las ráfagas y las disputas; lo demás es prueba guardada 30 días.
- **Espacio sin techo.** Resuelto fuera de aquí: cuota por empresa, packs, exceso facturado y
  nunca bloqueante, y la retención como mando ([almacenamiento/README](../almacenamiento/README.md)).
  El fichaje del quiosco nunca falla por espacio.
- **Una tablet sin cámara frontal útil.** Comprarla con cámara frontal decente y con luz en la
  pared; una foto negra es un fichaje sin prueba. El quiosco no ficha si la cámara falla, y lo dice.
- **Tablet sin red.** Fase 1 no ficha sin red y lo dice. Centros sin cobertura: SIM de datos en
  la tablet, o esperar a la Fase 2.
- **Tablets que no valen.** Una tablet sin posición precisa, sin ubicación o sin cámara
  frontal es un «dispositivo no válido» y no arranca el quiosco; es deliberado («sumamente
  importante»). En la guía de compra: tablet **con GPS** (los modelos con SIM lo llevan) y
  cámara frontal; en la de instalación: ubicación activada y permiso concedido antes de entrar.
- **Fijación de pantalla no es Lock Task.** En el piloto, quien sepa el PIN de la tablet sale de
  la app. Es el encargado; aceptable para 2-3 centros, no para 500 (Fase 3).
- **Refactor del controlador de fichaje.** Sacar el núcleo a `RegisterChecklog` toca el camino
  crítico. Hacerlo con el catálogo de QA de checklogs en verde antes y después, y desplegar
  primero a staging como manda [checklogs-http/04](../checklogs-http/04_fases.md).

## Lo que queda abierto (no bloquea)

- Si el código debe ser único por empresa (como aquí) o por sucursal. Por empresa es más
  simple y 950 personas caben de sobra en un millón.
- Texto legal modelo para la foto (lo redacta quien lleve lo legal; el panel sólo lo enseña).
- Si la ráfaga se mide en 90 s y tres fichajes, o conviene afinarlo con datos del piloto.
- Si Serlimar quiere NFC desde el piloto: entonces la tablet se compra con NFC y la Fase 2
  adelanta ese punto. Con el QR impreso, probablemente no haga falta.
- Formato de la tarjeta QR: tarjeta de visita plastificada, o pegatina en la tarjeta de empresa
  que ya lleven. Lo decide el cliente; el PDF sale en los dos tamaños.

## Fuentes

- AEPD, *Guía sobre tratamientos de control de presencia mediante sistemas biométricos*,
  23-11-2023 — https://www.aepd.es/guias/guia-control-presencia-biometrico.pdf
- AEPD, nota de prensa de la guía — https://www.aepd.es/prensa-y-comunicacion/notas-de-prensa/la-aepd-publica-una-guia-sobre-la-utilizacion-de-datos
- Cuatrecasas, «¿Es válido el registro de jornada a través de la huella dactilar o el reconocimiento facial?» — https://www.cuatrecasas.com/es/spain/laboral/art/registro-jornada-huella-dactilar-reconocimiento-facial
- ECIJA, resolución sancionadora de la AEPD (365.000 €, abril 2024) — https://files.griddo.ecija.com/ecija-resolucion-sancionadora-aedp-abril-24-1.pdf
- AEPD, informe AI 00285/2024 (Iberia sustituye biometría por tarjetas) — https://www.aepd.es/documento/ai-00285-2024.pdf
- `kiosk_mode` (Flutter, Lock Task / Guided Access) — https://pub.dev/packages/kiosk_mode
- `screen_pinning` (Flutter, fijación de pantalla y Lock Task) — https://pub.dev/documentation/screen_pinning/latest/
- Corbado, transporte híbrido de passkeys (QR + Bluetooth) — https://www.corbado.com/blog/webauthn-transports-internal-hybrid
- Sesame HR, Wall 3.0 (quiosco con código y PIN, NFC, cara) — https://help.sesamehr.com/en_US/what-other-clock-inout-alternatives-can-i-set-up-in-sesame-wall-30

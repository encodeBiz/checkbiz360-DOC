# TDR-001 — Servidor de autorización sobre Firebase Auth y puerta MCP del asistente

**Fecha:** 2026-10-15
**Estado:** Diseño propuesto
**Componente:** `encodebiz-api` — `services/assistant` (nuevo)
**Decisiones de referencia:** [ADR-001](../adr/ADR-001-la-identidad-es-la-de-firebase-auth.md),
[ADR-002](../adr/ADR-002-una-conexion-es-una-persona-en-una-empresa.md),
[ADR-003](../adr/ADR-003-solo-clientes-conocidos.md)
**Especificación que se cumple:** MCP *Authorization*, edición 2026-07-28 (OAuth 2.1, RFC 9728,
RFC 8414, RFC 8707, RFC 9207, documentos de metadatos de cliente, RFC 7591)

---

## 1. Dónde vive

Un servicio nuevo, `services/assistant`, con la misma plantilla que los demás (Express, un
contenedor, `/health`, `expose` sin `ports:`). Puerto `3017`, el siguiente libre después de
`inventory`. Ruta pública `/api/v1/assistant`.

Dentro van las dos mitades de la fase 1, porque son el mismo problema visto desde dos lados:

- **El servidor de autorización**, en `/api/v1/assistant/oauth/*`, que es quien conoce a la
  persona.
- **El servidor MCP**, en `/api/v1/assistant/mcp`, que es quien atiende al asistente con el
  token que el primero emitió.

Separarlos en dos servicios no compra nada hoy y obliga a compartir el almacén de tokens.
Si mañana otra integración necesita el servidor de autorización (Zapier, un ERP), se saca a
su propio servicio y el `issuer` se mantiene con una regla de nginx.

Las URLs canónicas, que son las que el cliente teclea y las que viajan dentro de los tokens:

| | Desarrollo | Producción (fase 3) |
|---|---|---|
| Emisor (`issuer`) | `https://api-staging.checkbiz360.com/api/v1/assistant` | `https://api.checkbiz360.com/api/v1/assistant` |
| Servidor MCP (`resource`), uno por empresa | `https://api-staging.checkbiz360.com/api/v1/assistant/mcp/e/{entityId}` | `https://api.checkbiz360.com/api/v1/assistant/mcp/e/{entityId}` |

**La empresa va en la URL** (ADR-002): cada empresa es un servidor MCP distinto para el
cliente, con su propio `resource`, y el emisor es el mismo para todas. Sin barra final, como
pide la especificación. El `resource` tiene que ser **exactamente** lo que la persona pega en
claude.ai o en ChatGPT, con la ruta incluida: la ficha del add-on en el panel (fase 3) enseña
la URL de cada empresa para copiarla; en la prueba de staging se monta a mano con el id de la
entidad de demo. El id de una empresa no es un secreto (ya va en las URLs del panel): sin
asiento en ella, la URL no sirve de nada.

## 2. Descubrimiento

Un cliente que llega sin token recibe un `401` con la pista de dónde está todo:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://api-staging.checkbiz360.com/.well-known/oauth-protected-resource/api/v1/assistant/mcp/e/{entityId}", scope="operations"
```

**Metadatos del recurso protegido** (RFC 9728). Se sirven en la ruta con el camino del
recurso insertado, que es la que marca la RFC y la que el cliente lee de la cabecera
`WWW-Authenticate`. Un documento por empresa, generado al vuelo: el camino lleva el id y el
servidor comprueba que la entidad existe antes de responder (si no, `404`). La raíz
(`/.well-known/oauth-protected-resource` sin camino) no se sirve: no hay un recurso único que
anunciar ahí, y la cabecera del `401` ya da la URL exacta.

```
GET /.well-known/oauth-protected-resource/api/v1/assistant/mcp/e/{entityId}
```
```json
{
  "resource": "https://api-staging.checkbiz360.com/api/v1/assistant/mcp/e/{entityId}",
  "authorization_servers": ["https://api-staging.checkbiz360.com/api/v1/assistant"],
  "scopes_supported": ["operations"],
  "bearer_methods_supported": ["header"],
  "resource_name": "CheckBiz360"
}
```

**Metadatos del servidor de autorización** (RFC 8414). Con el camino del emisor insertado, y
el alias de OpenID Connect con el mismo cuerpo, porque la especificación obliga a los clientes
a soportar los dos y alguno empieza por el segundo:

```
GET /.well-known/oauth-authorization-server/api/v1/assistant
GET /.well-known/openid-configuration/api/v1/assistant
```
```json
{
  "issuer": "https://api-staging.checkbiz360.com/api/v1/assistant",
  "authorization_endpoint": "https://api-staging.checkbiz360.com/api/v1/assistant/oauth/authorize",
  "token_endpoint": "https://api-staging.checkbiz360.com/api/v1/assistant/oauth/token",
  "registration_endpoint": "https://api-staging.checkbiz360.com/api/v1/assistant/oauth/register",
  "revocation_endpoint": "https://api-staging.checkbiz360.com/api/v1/assistant/oauth/revoke",
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "code_challenge_methods_supported": ["S256"],
  "token_endpoint_auth_methods_supported": ["none", "client_secret_basic", "client_secret_post"],
  "scopes_supported": ["operations", "offline_access"],
  "client_id_metadata_document_supported": true,
  "authorization_response_iss_parameter_supported": true
}
```

Dos detalles que no son decoración: `code_challenge_methods_supported` con `S256` es lo que
el cliente mira para decidir si sigue (sin él, se niega), y `offline_access` sólo está en los
del servidor de autorización, no en los del recurso, porque un token de refresco no es un
permiso sobre el recurso. ChatGPT lo pide para que le demos refresco.

**Ámbitos.** Uno solo, `operations`: operar la empresa en nombre de la persona. Las
herramientas de la fase 2 no se reparten en ámbitos porque el permiso real es el rol de la
persona en la empresa, no una casilla del consentimiento. Si algún día hace falta un acceso
de sólo lectura, se añade `operations:read` y el flujo de ampliación de ámbito que la
especificación ya describe.

## 3. Registro de clientes

Los tres mecanismos de la especificación, con la política de dominios del
[ADR-003](../adr/ADR-003-solo-clientes-conocidos.md) delante de los dos abiertos.

**Documento de metadatos de cliente (CIMD).** Si el `client_id` es una URL HTTPS con camino
(`https://chatgpt.com/oauth/…/client.json`), el servidor la descarga y la valida:

- sólo si el dominio está en `ASSISTANT_CLIENT_HOSTS`; a otro dominio no se hace ni la
  petición (SSRF cerrado desde antes de salir);
- `GET` con 5 segundos de espera, 64 KB de máximo, sin seguir redirecciones;
- el campo `client_id` del documento tiene que ser **idéntico** a la URL; `client_name` y
  `redirect_uris` obligatorios; cada `redirect_uri` en HTTPS y en la lista de dominios;
- se guarda en caché en memoria el tiempo que diga `Cache-Control` (tope 24 h).

`token_endpoint_auth_method` admitido: `none` (el cliente se defiende con PKCE). ChatGPT puede
declarar `private_key_jwt`; si en la primera prueba lo hace, se añade la verificación de la
aserción contra su `jwks_uri`, que es trabajo acotado. No se adelanta sin verlo.

**Registro dinámico (RFC 7591).** `POST /oauth/register` con JSON (`client_name`,
`redirect_uris`, `grant_types`, `response_types`, `token_endpoint_auth_method`,
`application_type`). Sin token de registro (es lo que claude.ai espera). Se rechaza con
`invalid_redirect_uri` cualquier URL fuera de la lista. Responde `201` con `client_id` (y
`client_secret` sólo si el cliente pidió un método con secreto; claude.ai pide `none`). Se
guarda en `assistant_clients/{clientId}`. Límite por IP: 10 registros por hora.

**Registro previo.** Un cliente creado a mano (script `register-client.ts`, con
`client_id`, `client_secret` opcional y sus `redirect_uris`) para cuando alguien configura
el conector pegando credenciales en la casilla «Avanzado» de claude.ai. Mismo documento en
`assistant_clients`, con `manual: true`.

Lista de dominios por defecto: `claude.ai`, `claude.com`, `chatgpt.com`, `openai.com`.
URLs de retorno conocidas hoy, que la prueba en staging tiene que confirmar:

| Cliente | `redirect_uri` |
|---|---|
| claude.ai, escritorio, móvil, Cowork | `https://claude.ai/api/mcp/auth_callback` (podría pasar a `claude.com`) |
| ChatGPT, sin `iss` en la respuesta | `https://chatgpt.com/connector/oauth/{callback_id}` |
| ChatGPT, con `iss` en la respuesta | `https://chatgpt.com/connector_platform_oauth_redirect` |

Como emitimos `iss`, ChatGPT usará la estable. La de Claude sale de documentación de terceros
(julio de 2026); el artículo de soporte de Anthropic no se pudo abrir el 2026-10-15.

## 4. La autorización

### 4.1 La petición

```
GET /api/v1/assistant/oauth/authorize
  ?response_type=code
  &client_id=…
  &redirect_uri=…
  &state=…
  &code_challenge=…
  &code_challenge_method=S256
  &scope=operations
  &resource=https://api-staging.checkbiz360.com/api/v1/assistant/mcp/e/{entityId}
```

Antes de enseñar nada, el servidor comprueba, en este orden y parando en el primero que falla:

1. `client_id` resuelve a un cliente (previo, registrado o documento de metadatos válido).
2. `redirect_uri` es **exactamente** una de las del cliente, y su dominio está en la lista.
   Si esto falla, **no se redirige**: se enseña una página de error nuestra. Redirigir a una
   URL que no se ha validado es justo el agujero que se está cerrando.
3. `response_type=code`, `code_challenge` presente y `code_challenge_method=S256`.
4. `resource` es **obligatorio** y tiene que ser una URL de empresa nuestra
   (`{issuer}/mcp/e/{entityId}`, con una entidad que exista): de ahí sale la empresa de la
   conexión. Otra URL, o ninguna, es `invalid_target`. La especificación obliga al cliente a
   mandarlo y Claude y ChatGPT lo hacen; si en la prueba alguno no lo manda, se sabrá en el
   primer intento y no en producción.
5. `scope`: `operations` o vacío; `offline_access` se acepta y se ignora (siempre damos
   refresco). Otro ámbito, `invalid_scope`.

A partir de aquí los errores sí se devuelven al cliente por redirección (`error`,
`error_description`, `state`, `iss`), como manda OAuth.

Pasadas las comprobaciones, se crea la **petición pendiente** en
`assistant_auth_requests/{rid}` (10 minutos de vida) con todo lo anterior, `entityId`
incluido, y se pone una cookie
`asst_req` con el `rid` firmado (HMAC con `ASSISTANT_COOKIE_SECRET`), `HttpOnly`, `Secure`,
`SameSite=Lax`, `Path=/api/v1/assistant/oauth`, 10 minutos. Cada paso de la pantalla manda
el `rid` y tiene que casar con la cookie: una petición no se completa desde otro navegador.

### 4.2 La pantalla

Una sola página, servida por el servicio, con tres pasos y sin framework. El cliente de
Firebase (`firebase/auth`) va **empaquetado en la imagen** con esbuild, no desde un CDN: así la
política de contenido (CSP) sólo permite scripts propios. La configuración web del proyecto
(`apiKey`, `authDomain`, `projectId`, `appId`, pública por naturaleza) entra por
`ASSISTANT_FIREBASE_WEB_CONFIG` y se inyecta en la página.

**Paso 1 — entrar.** Correo y contraseña, o Google, los mismos dos caminos del panel. El SDK
se inicia con persistencia en memoria (`inMemoryPersistence`): ninguna sesión anterior del
navegador entra sola, y cada autorización es un inicio de sesión real. Al entrar, la página
obtiene el ID token y lo manda:

```
POST /oauth/authorize/session   { rid, idToken }
```

El servidor lo verifica con el Admin SDK (`verifyIdToken`, con comprobación de revocación),
exige `auth_time` dentro de los últimos 10 minutos, y pregunta a `checkinbiz` por el
segundo factor con ese mismo ID token (`GET /api/v1/checkinbiz/auth/2fa/user/status`, por la
red interna). El ID token **no se guarda**: la página lo conserva en memoria y lo vuelve a
mandar en cada paso.

- `enabled: false` → la página se para: «Activa el segundo factor en el panel de checkbiz360
  y vuelve a conectar». No hay código, no hay excepción. En el panel el segundo factor es
  obligatorio para todo administrador; aquí también.
- `enabled: true` → paso 2.

**Paso 2 — segundo factor.** Los seis dígitos de la aplicación de autenticación:

```
POST /oauth/authorize/2fa   { rid, idToken, code }
```

El servidor llama a `POST /api/v1/checkinbiz/auth/2fa/user/verify` con el ID token y el
código. Es el **mismo** verificador del panel: una sola implementación del TOTP, el secreto
sigue en `users/{uid}/security/twoFA` y nadie lo lee desde aquí. (El verificador deja
`verifiedAt` y las claims `admin`/`twoFA` en la cuenta, que ya estaban: no cambia nada que no
estuviera.) Tres intentos fallidos matan la petición pendiente. Verificado, se anota
`uid` y `verifiedAt` en la petición y se pasa al consentimiento.

**Paso 3 — consentimiento.** La empresa ya está decidida: es la de la URL. El servidor mira
el asiento en `user_entity_roles/{uid}_{entityId}`: tiene que estar `active`, con `role`
`owner` o `admin`, y no ser un asiento de soporte (`support: true`): nuestro equipo no conecta
asistentes a empresas de clientes. Sin asiento, la página lo dice («no tienes acceso de
administración en esta empresa») y se para, sin código. Con asiento, enseña la empresa (el
nombre de `entities/{id}`) y el consentimiento, con todas las letras:

> **Claude** (se devolverá a `claude.ai`) podrá **ver y modificar horarios y tareas de
> *Limpiezas Pérez* en tu nombre**, como *Marta García (administradora)*. Los nombres de tus
> empleados y los datos de la operación se enviarán a tu cuenta de Claude. Puedes cortar
> este acceso cuando quieras desde el panel.

El nombre del cliente sale del registro o del documento de metadatos; el dominio de retorno
se enseña siempre, como pide la especificación.

```
POST /oauth/authorize/decision   { rid, idToken, decision: "allow" | "deny" }
```

El servidor vuelve a verificar el ID token (mismo `uid` que la petición), vuelve a mirar el
asiento (`canWrite(uid, entityId)`, con la empresa de la petición), y:

- `deny` → `302` a `redirect_uri?error=access_denied&state=…&iss=…`.
- `allow` → crea (o reutiliza, si ya hay una viva con el mismo `uid`, `entityId` y cliente)
  la conexión en `assistant_connections`, emite un **código** y redirige:
  `302 redirect_uri?code=…&state=…&iss=https://api-staging.checkbiz360.com/api/v1/assistant`.

La petición pendiente se borra al decidir, y caduca sola a los 10 minutos si nadie decide.

### 4.3 El código

32 bytes aleatorios en base64url; en Firestore sólo su SHA-256, en
`assistant_tokens/{hash}` con `kind: "code"`, 60 segundos de vida, un solo uso, y atado a:
`connectionId`, `clientId`, `redirectUri`, `codeChallenge`, `resource`, `scope`.

## 5. El endpoint de token

`POST /oauth/token`, `application/x-www-form-urlencoded`, respuestas siempre con
`Cache-Control: no-store`.

**`grant_type=authorization_code`.** Se busca el hash; tiene que existir, ser `code`, no estar
caducado ni usado, y casar `client_id`, `redirect_uri` y `resource` con lo atado. Después,
`BASE64URL(SHA256(code_verifier)) == codeChallenge`. Cualquier fallo es `invalid_grant`,
sin decir cuál. El código se marca usado **antes** de emitir nada (un segundo intento con el
mismo código revoca la conexión entera: alguien lo tiene que no debe). Respuesta:

```json
{
  "access_token": "…", "token_type": "Bearer", "expires_in": 3600,
  "refresh_token": "…", "scope": "operations"
}
```

**`grant_type=refresh_token`.** Mismo esquema: hash, `kind: "refresh"`, vivo, no usado,
conexión no revocada, `client_id` igual. Se **rota**: el de refresco viejo se marca usado con
`rotatedTo`, y se emite un par nuevo. Reutilizar un refresco ya rotado revoca la conexión y
devuelve `invalid_grant`. Es lo que la especificación exige para clientes públicos.

**Autenticación del cliente.** Los clientes con `token_endpoint_auth_method: none` (claude.ai,
ChatGPT) no se autentican: PKCE es su defensa. Un cliente previo con secreto lo presenta por
`client_secret_basic` o `client_secret_post` y se compara en tiempo constante (`safeEqual`,
el de `sales`).

## 6. Los tokens

**Opacos, no JWT.** 32 bytes aleatorios en base64url, y en Firestore sólo el SHA-256. Razón:
el servidor MCP tiene que leer la conexión en cada llamada de todas formas (para saber si
sigue viva y de qué empresa es), así que un JWT firmado no ahorra esa lectura y añade una
clave que custodiar y rotar. Con opacos, revocar es borrar y no hay nada que descifrar en un
log.

| Token | Vida | Uso |
|---|---|---|
| Código | 60 s | Uno |
| Acceso | 1 hora | Hasta caducar |
| Refresco | 90 días desde su emisión | Uno (rotación) |

Todos llevan `resource` (la URL de la empresa) y `connectionId`. El servidor MCP **comprueba
que `resource` es exactamente la URL a la que se está llamando**: el token de la empresa A no
vale en la URL de la empresa B, uno emitido para otra cosa no vale aquí, y uno nuestro no
vale en otro sitio. Es la vinculación de audiencia que la especificación exige.

## 7. Almacenamiento

Cuatro colecciones en Firestore, en la raíz y con prefijo `assistant_`, **sólo desde el
backend**: en `firestore.rules` se niegan al navegador explícitamente, como
`cuadrante_proposals`.

```
assistant_clients/{clientId}
  clientName · redirectUris[] · tokenEndpointAuthMethod · clientSecretHash?
  manual: boolean · createdAt · lastSeenAt

assistant_auth_requests/{rid}                      (TTL: expiresAt, 10 min)
  clientId · redirectUri · state · codeChallenge · scope · resource · entityId
  uid? · verifiedAt? · attempts2fa · createdAt · expiresAt

assistant_connections/{connectionId}
  uid · entityId · clientId · clientName · origin: "claude" | "chatgpt" | "other"
  scope · createdAt · lastUsedAt · revokedAt? · revokedBy?: "user" | "client" | "support" | "seat"

assistant_tokens/{sha256}                          (TTL: expiresAt)
  kind: "code" | "access" | "refresh" · connectionId · clientId · resource · scope
  redirectUri? · codeChallenge?         (sólo code)
  usedAt? · rotatedTo?                  (code y refresh)
  createdAt · expiresAt
```

`expiresAt` está para la política TTL de Firestore de cada colección (se configura en
consola, con `--project dev-encodebiz`); hasta que esté puesta, un barrido al emitir limpia
lo vencido, como hace `caducar` en las propuestas de cuadrante.

Índices compuestos: `assistant_connections (uid, revokedAt, createdAt)` para la lista de la
persona, `(entityId, revokedAt)` para la de la empresa, y `assistant_tokens (connectionId)`
para revocar en bloque. Van a `firestore.indexes.json` y se despliegan **en los dos
sentidos**, que ya sabemos que el fichero y lo desplegado derivan.

`lastUsedAt` se escribe como mucho una vez cada 5 minutos por conexión, no en cada llamada.

## 8. El servidor MCP

`POST /api/v1/assistant/mcp/e/:entityId`, con el mismo montaje que el CRM: un `McpServer` y un
`StreamableHTTPServerTransport` por petición, sin sesión, `enableJsonResponse`, y `405` a
`GET` y `DELETE`. El contenedor se reinicia sin romper a nadie.

Delante, el guardián del token:

1. `Authorization: Bearer <token>`; sin cabecera o mal formada → `401` con el
   `WWW-Authenticate` de §2. Nunca se acepta el token en la URL.
2. SHA-256, lectura en `assistant_tokens`: tiene que ser `access`, vivo, y con `resource`
   igual a la URL de esta petición (la empresa de la ruta). Si no → `401` con el mismo
   `WWW-Authenticate` (el cliente sabe que tiene que refrescar o volver a autorizar). Un
   token de otra empresa cae aquí, antes de leer nada más.
3. Lectura de la conexión: no revocada y con el mismo `entityId` que la ruta. Después, el
   asiento: `canWrite(uid, entityId)` tiene
   que seguir diciendo que sí. Si la conexión está viva pero el asiento ya no, se marca
   `revokedAt` con `revokedBy: "seat"` y se responde `403` con `assistant/no_seat`. No es un
   `insufficient_scope`: no hay ámbito que pedir que lo arregle.
4. Lo que queda es el **contexto** de la petición: `{ uid, entityId, connectionId, clientName }`.
   Con él se construye el servidor; las herramientas no reciben `entityId` ni `uid`
   (ADR-002), los tienen ya.

El servidor se presenta con la empresa en el nombre, para que dos conexiones se distingan en
la lista del cliente:

```ts
new McpServer({ name: "checkbiz360", title: `CheckBiz360 · ${entity.name}`, version: "1.0.0" })
```

**La única herramienta de la fase 1**, `conexion_actual`: devuelve la empresa (id y nombre),
la persona (nombre, correo, rol en la empresa), el cliente desde el que se habla y la fecha de
la conexión. Sirve para probar la cadena entera (descubrimiento, registro, consentimiento,
token, llamada) antes de que exista ninguna funcionalidad.

Límite de peticiones: por conexión, `ASSISTANT_MCP_RATE_LIMIT` por minuto (120 por defecto),
con el mismo `express-rate-limit` del CRM y la conexión como clave.

## 9. Cómo llega la identidad al núcleo

El token del asistente **no sale** del servicio: la especificación prohíbe reenviarlo y el
núcleo no sabría leerlo. Las herramientas de la fase 2 llamarán a los servicios del núcleo
por la red interna con la clave S2S (`x-encodebiz-key`) y el **`actorUid` de la conexión**,
igual que hace hoy `POST /api/v1/tasks/system` para las tareas que crea un add-on y
`puertaDeServicio` en el lector de cuadrantes: el núcleo resuelve a esa persona
(`resolveActorByUid`) y le aplica **exactamente los mismos permisos** que si hubiera entrado por
el panel. Heredar el nombre de alguien no se salta lo que ese alguien puede hacer.

Cada llamada lleva además `source: { kind: "assistant", connectionId }` para que la actividad
diga por dónde entró. Qué puertas `/system` hacen falta (calendario del empleado, copiar una
semana, propuestas) se decide con las herramientas, en la fase 2; aquí sólo queda fijado el
mecanismo.

## 10. Revocación

Tres caminos, y los tres acaban en `revokedAt` sobre la conexión, que es lo único que el
guardián mira:

- **El cliente** (RFC 7009): `POST /oauth/revoke` con `token` (y la autenticación del cliente
  si la tiene). Un refresco revoca la conexión; un acceso sólo se borra a sí mismo. Claude y
  ChatGPT pueden llamarlo al «desconectar»; no se cuenta con ello.
- **La persona**, para la pantalla «Conexiones» del panel (fase 3) y para probar ahora:
  `GET /api/v1/assistant/connections` lista las suyas (todas sus empresas) y
  `DELETE /api/v1/assistant/connections/:id` corta una. Credencial: el ID token de Firebase,
  como el resto del panel. Cortar las de **otra** persona de la misma empresa (el propietario
  que echa a un administrador) se diseña con la pantalla.
- **El asiento**: desactivar o degradar a alguien en `user_entity_roles` corta su conexión en
  la siguiente llamada (§8, paso 3). No hay nada que recordar al dar de baja a un colaborador.

Soporte, desde el backoffice, en la fase 3.

## 11. Seguridad, en lista

- Todo por HTTPS; nginx ya pone HSTS y `X-Frame-Options: DENY`, así que la pantalla no se
  puede enmarcar. Además, CSP propia: scripts sólo del servicio; `connect-src` a
  `identitytoolkit.googleapis.com` y `securetoken.googleapis.com`; `frame-src` al
  `authDomain` del proyecto (lo usa el inicio de sesión con Google).
- PKCE `S256` obligatorio; `redirect_uri` exacta y en la lista de dominios; `iss` en todas
  las respuestas de autorización; códigos de un solo uso y 60 segundos; refrescos rotados y
  con detección de reutilización.
- Ni tokens ni códigos en logs. En la URL de `/authorize` sólo viajan `state` y
  `code_challenge`, que son públicos por diseño; el código vuelve en la redirección al
  cliente, no por nuestras rutas. `Cache-Control: no-store` en todas las respuestas de
  `/oauth/*`.
- ID token de Firebase verificado con revocación y con `auth_time` reciente; persistencia en
  memoria en la página; nunca almacenado.
- Petición pendiente atada al navegador por cookie firmada; tres intentos de segundo factor;
  10 minutos de vida.
- Comparaciones de secretos en tiempo constante. Hash SHA-256 de todo token en reposo.
- Descarga de documentos de metadatos sólo a dominios de la lista, sin redirecciones, con
  tope de tamaño y de tiempo.
- Límites: `/oauth/register` 10 por hora e IP; `/oauth/authorize` y sus tres pasos, 30 por
  10 minutos e IP; `/oauth/token` 60 por minuto e IP; MCP, por conexión.
- Un `GET` a la URL del MCP responde `405`, no `401`: no hay sesión que abrir.

## 12. Entorno y despliegue

**Variables del servicio** (`docker-compose.staging.yml`, con `*secret-volumes` para la
cuenta de servicio de Firebase, como los demás):

| Variable | Valor en desarrollo |
|---|---|
| `PORT` | `3017` |
| `ASSISTANT_PUBLIC_URL` | `https://api-staging.checkbiz360.com/api/v1/assistant` (el `issuer`; el MCP de cada empresa es `+ /mcp/e/{entityId}`) |
| `ASSISTANT_FIREBASE_WEB_CONFIG` | JSON público del proyecto `dev-encodebiz` (`apiKey`, `authDomain`, `projectId`, `appId`) |
| `ASSISTANT_COOKIE_SECRET` | 32 bytes aleatorios; en `secrets/` |
| `ASSISTANT_CLIENT_HOSTS` | `claude.ai,claude.com,chatgpt.com,openai.com` |
| `ASSISTANT_ALLOW_LOCALHOST` | sin definir (sólo `1` en local, para Claude Code) |
| `ASSISTANT_MCP_RATE_LIMIT` | `120` |
| `ENCODEBIZ_API_KEY` | la de la plataforma, para las llamadas S2S salientes (fase 2) |
| `CHECKINBIZ_INTERNAL_URL` | `http://checkinbiz:<puerto>` |
| `TASKS_INTERNAL_URL` | `http://tasks:3006` |

**nginx** (`nginx.staging.conf`): el par raíz/subruta de siempre, más los tres `.well-known`
con `^~`, por lo mismo que el de Let's Encrypt (que gane a cualquier regex):

```nginx
location ^~ /.well-known/oauth-authorization-server { proxy_pass http://assistant_service; }
location ^~ /.well-known/oauth-protected-resource   { proxy_pass http://assistant_service; }
location ^~ /.well-known/openid-configuration       { proxy_pass http://assistant_service; }
location = /api/v1/assistant  { proxy_pass http://assistant_service/api/v1/assistant; }
location /api/v1/assistant/   { proxy_pass http://assistant_service/api/v1/assistant/; }
```

Y después del `up -d`, reiniciar nginx, que resuelve los upstreams al arrancar.

**Firebase (consola, proyecto `dev-encodebiz`):** añadir `api-staging.checkbiz360.com` a
*Authentication → Settings → Authorized domains*, o el inicio de sesión con Google no abre
desde la pantalla. Si la clave web tiene restricción por referidor, añadir el dominio ahí
también. En producción, lo mismo con `api.checkbiz360.com` en `encodebiz-services`, el día del
pase.

**Firestore:** reglas (las cuatro colecciones negadas) e índices (§7), desplegados con
`--project dev-encodebiz`.

**CI/CD:** nada nuevo; el servicio entra en la cadena `develop → staging` y el workflow de
staging lo levanta con los demás.

## 13. Plan de pruebas en staging

Primero a mano con `curl`, luego desde los dos clientes:

1. Metadatos: la ruta del recurso de la entidad de demo y las dos del servidor de
   autorización responden con el `issuer` y el `resource` canónicos; con un id de entidad
   inexistente, `404`. `POST` a la URL de la empresa sin token da `401` con el
   `WWW-Authenticate` correcto; `GET` da `405`.
2. Registro dinámico con una `redirect_uri` de `claude.ai` → `201`; con una de otro dominio
   → `400 invalid_redirect_uri`.
3. **claude.ai**: *Configurar → Conectores → Añadir*, la URL de la entidad de demo de ayuda
   a domicilio. Tiene que abrir nuestra pantalla, pedir correo y contraseña, pedir el código,
   enseñar esa empresa en el consentimiento, y al autorizar aparecer conectado con
   `conexion_actual` disponible. Llamarla
   y leer la empresa y la persona. **Anotar la `redirect_uri` real y el mecanismo de registro
   que usó** (registro dinámico o documento de metadatos): es lo que confirma la tabla de §3.
4. **ChatGPT**: lo mismo desde su alta de conectores. Anotar el `client_id` que presenta (si
   es una URL, es un documento de metadatos) y el `token_endpoint_auth_method` que declara.
5. Inicio de sesión con Google en la pantalla, con el dominio ya autorizado en Firebase.
6. Un usuario sin segundo factor activado: la pantalla se para en el paso 1 con el aviso.
7. Un usuario con asiento en dos empresas: añade las dos URLs en el cliente; cada una pide
   su consentimiento y aparecen como dos conectores con nombres distintos. Con el token de
   una contra la URL de la otra (a mano, con `curl`): `401`. Y la URL de una empresa en la
   que **no** tiene asiento: la pantalla se para antes del consentimiento.
8. Revocar desde `DELETE /connections/:id` y volver a llamar a la herramienta: `401`; el
   cliente vuelve a pedir autorización.
9. Desactivar el asiento en el panel y volver a llamar: `403 assistant/no_seat`, y la
   conexión queda con `revokedBy: "seat"`.
10. Refresco: esperar a que caduque el acceso (o acortarlo por entorno) y comprobar que el
    cliente refresca solo; reutilizar un refresco viejo revoca la conexión.
11. Negativos a mano: `redirect_uri` que no casa, `code_verifier` equivocado, código usado dos
    veces, `resource` ajeno. Todos `invalid_grant` o `invalid_request`, ninguno deja huella.

La suite de `qa/` (Playwright) puede cubrir el camino de correo y contraseña con la cuenta de
QA; el de Google y los dos clientes se prueban a mano.

## 14. Orden de trabajo

Una semana de trabajo, en este orden, y nada sube a `staging` hasta el último día:

1. Esqueleto del servicio, metadatos, nginx, compose, Firestore (reglas e índices).
2. Registro de clientes (los tres mecanismos) y validación de `/authorize`.
3. Pantalla: inicio de sesión, segundo factor, empresa y consentimiento; código.
4. `/token` (código y refresco), `/revoke`, `/connections`; guardián del MCP y
   `conexion_actual`.
5. Prueba en staging con claude.ai y ChatGPT; corregir la tabla de §3 con lo observado.

## 15. Lo que queda abierto

Las cuatro decisiones del README quedaron cerradas el 2026-10-15 con su valor por defecto, y
los tres ADR están aceptados. Queda una sola pregunta, para después de la prueba: si ChatGPT
presenta `private_key_jwt`, se implementa en la semana siguiente o se le da el registro
dinámico como alternativa (lo soporta como segunda opción).

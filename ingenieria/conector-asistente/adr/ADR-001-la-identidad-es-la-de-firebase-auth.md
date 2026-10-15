# ADR-001 — La identidad es la de Firebase Auth, y los tokens OAuth los emite la plataforma

**Fecha:** 2026-10-15
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («el acceso debe ser con la auth de Firebase»)

---

## Contexto

Claude y ChatGPT hablan con un servidor MCP remoto por OAuth 2.1: el cliente descubre un
servidor de autorización, manda a la persona a una pantalla, la persona entra y consiente, y
el cliente recibe un token que presenta en cada llamada. Es lo que exige la especificación
de MCP (edición 2026-07-28) y lo único que aceptan los dos para un conector de terceros, aparte
de «sin autenticación» o un token fijo en la URL.

El conector del CRM lleva un token fijo en la URL (ADR-005 de `sales-crm`) y está bien así:
quien lo usa somos nosotros, y se revoca cambiando el token. Con clientes no vale. Cada
conexión tiene que ser **una persona** con **sus** permisos, poder cortarse sin afectar a
las demás, y no depender de que una URL no se filtre.

Firebase Auth es la identidad de todo checkbiz360: el panel entra con correo y contraseña o
con Google, el segundo factor TOTP es obligatorio para cualquier administrador, y de ese `uid`
cuelgan los asientos (`user_entity_roles`) de los que sale todo permiso. Pero Firebase Auth
**no es un servidor de autorización OAuth** para clientes de terceros: no tiene endpoint de
autorización ni de token que Claude o ChatGPT puedan usar.

## Decisión

1. **La persona se autentica con Firebase Auth**, en una pantalla servida por la propia
   plataforma, con los mismos dos caminos del panel (correo y contraseña, Google) y con el
   **mismo segundo factor**: quien no lo tiene activado en el panel no puede conectar.
2. **La plataforma es el servidor de autorización.** Un servicio nuestro (`assistant`) expone
   los metadatos, la pantalla de consentimiento, el endpoint de token y el de revocación, y
   emite **sus propios tokens**, opacos, apoyados en el `uid` verificado. Firebase pone la
   identidad; nosotros ponemos la autorización.
3. **Ningún token de Firebase sale del servidor.** El ID token que la pantalla obtiene se
   verifica con el Admin SDK y se descarta. Lo que recibe Claude es un token nuestro, atado a
   nuestro servidor MCP, que sólo sirve ahí.
4. **No hay usuarios nuevos ni proveedor de identidad aparte** (Auth0, Clerk, Stytch y
   similares quedan descartados). Las cuentas, los roles y el segundo factor siguen donde
   están, y el día que un administrador se desactive en el panel, su conexión muere sola.

## Alternativas descartadas

- **Token en la URL por cliente**, como el CRM. Es el mismo secreto para todo el que tenga la
  URL, no sabe quién escribe, y pedirle a un cliente que custodie una URL con permiso de
  escritura sobre sus horarios no es serio. Sirve para un piloto interno, no para un producto.
- **Proveedor OAuth externo** delante de Firebase. Resuelve el servidor de autorización en un
  día, pero mete una tercera casa con sus usuarios, obliga a enlazar cuentas y a pagar por
  asiento, y el cliente ve una pantalla que no es la de checkbiz360. Lo que se ahorra en
  código se paga en soporte.
- **Firebase Auth como proveedor OIDC** usando Identity Platform. No ofrece un flujo de
  autorización para clientes de terceros con consentimiento y recursos propios; habría que
  construir la mitad igualmente.

## Consecuencias

- Hay que escribir un servidor de autorización OAuth 2.1 pequeño pero completo: PKCE, registro
  de clientes, consentimiento, códigos de un solo uso, tokens de acceso cortos y de refresco
  rotados, revocación y metadatos de descubrimiento. El detalle está en
  [TDR-001](../tdr/TDR-001-servidor-de-autorizacion-sobre-firebase-auth.md). Es el trabajo de
  días que el CRM aplazó y que aquí no se puede aplazar.
- El dominio del API (`api-staging.checkbiz360.com` en desarrollo, `api.checkbiz360.com` en
  producción) tiene que estar en los **dominios autorizados** de Firebase Auth del proyecto
  correspondiente, o el inicio de sesión con Google no abre.
- La pantalla de inicio de sesión y consentimiento es nuestra y se sirve desde el servicio.
  No toca el panel ni Vercel: el conector se prueba y se despliega con el resto de servicios.
- Lo que el lector de cuadrantes evita a propósito (que un modelo vea nombres) aquí pasa por
  diseño: el cliente conecta **su** cuenta de Claude o ChatGPT y los nombres de sus empleados
  viajan a ese proveedor. No es un defecto, es la naturaleza del producto, y la pantalla de
  consentimiento lo dice con todas las letras antes del botón.

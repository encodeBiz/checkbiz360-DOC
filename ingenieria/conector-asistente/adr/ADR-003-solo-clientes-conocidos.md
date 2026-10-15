# ADR-003 — Sólo clientes conocidos: el servidor de autorización sólo devuelve a Claude y a ChatGPT

**Fecha:** 2026-10-15
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («sí», 2026-10-15)

---

## Contexto

Un servidor de autorización OAuth tiene que saber a qué cliente le está dando un código. La
especificación de MCP (2026-07-28) contempla tres formas de que un cliente se identifique:

- **Documento de metadatos de cliente (CIMD):** el `client_id` es una URL HTTPS del propio
  cliente (ChatGPT manda algo como `https://chatgpt.com/oauth/.../client.json`), y el
  servidor la descarga para leer su nombre y sus URLs de retorno. Es la forma preferida de la
  especificación y la que ChatGPT usa primero.
- **Registro dinámico (DCR):** el cliente llama a `/register` y recibe un `client_id`. La
  especificación lo marca como obsoleto pero lo mantiene por compatibilidad; claude.ai lo usa.
- **Registro previo:** alguien pega un client id y un secret a mano.

Las dos primeras son **abiertas por definición**: cualquiera puede alojar un documento de
metadatos o llamar a `/register`. Con ellas abiertas del todo, un tercero podría registrar un
«asistente» con una URL de retorno suya, mandar a un cliente nuestro el enlace de
autorización, y si ese cliente entra y consiente, el tercero recibe un token con permiso de
escritura sobre los horarios de esa empresa. La pantalla diría «Autorizar a MiAsistente», y
mucha gente le daría a aceptar.

## Decisión

1. **Las URLs de retorno se validan contra una lista de dominios conocidos**, además de
   exactas contra las que el cliente declaró. Por defecto: `claude.ai`, `claude.com`,
   `chatgpt.com` y `openai.com`, en HTTPS. Un `redirect_uri` fuera de esa lista no se
   registra ni se atiende, tanto en el registro dinámico como en los documentos de metadatos.
2. **Los documentos de metadatos de cliente sólo se descargan de esos mismos dominios.** Es la
   política de confianza por dominio que la especificación permite, y de paso cierra la
   puerta a que el servidor haga peticiones a donde le digan (SSRF).
3. **Las redirecciones a `localhost`** (las que usa Claude Code y cualquier cliente de
   escritorio) **quedan fuera para clientes**. Sólo se admiten en desarrollo, con una
   variable de entorno, para probar nosotros.
4. **La lista vive en configuración**, no en código: el día que un cliente pida conectar
   desde otro asistente, se añade su dominio y se despliega, sin tocar el servidor.

## Alternativas descartadas

- **Registro abierto**, como hacen la mayoría de servidores MCP de ejemplo. Es lo que la
  especificación da por bueno para servidores que no custodian nada de valor. Aquí se
  custodian horarios y tareas de empresas que no son la nuestra.
- **Sólo registro previo**, sin registro dinámico ni documentos de metadatos. Es lo más
  cerrado, pero obliga a cada cliente a pegar un client id y un secret en la casilla
  «Avanzado» de claude.ai, y ChatGPT ni siquiera lo pone fácil. La fricción mataría el
  producto antes de empezar.

## Consecuencias

- Los tres mecanismos se implementan, pero los dos abiertos sólo funcionan para los dominios
  de la lista. El registro previo (credenciales manuales) sigue disponible para cuando haga
  falta.
- La pantalla de consentimiento enseña siempre el nombre del cliente y el **dominio** al que
  se va a devolver el código, como pide la especificación. Con la lista cerrada, ese dominio
  será siempre uno de los cuatro.
- El registro dinámico de claude.ai crea un cliente nuevo por cada conexión. La colección
  `assistant_clients` crece con los clientes; se limpia lo que no tenga conexiones vivas,
  como una tarea de mantenimiento más.

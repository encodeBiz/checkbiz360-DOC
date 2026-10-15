# ADR-002 — Una conexión es una persona en una empresa, y la empresa va en la URL

**Fecha:** 2026-10-15
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («eso es», ante la URL por empresa)

---

## Contexto

Un usuario del panel puede tener asiento en varias empresas: un propietario con dos
sociedades, un gestor que lleva tres clientes, nuestro propio soporte. El servicio de tareas
lo resuelve pidiendo `entityId` en cada petición y comprobando el asiento cada vez.

Con un asistente delante, ese modelo tiene un problema: el modelo tendría que elegir y
arrastrar un `entityId` en cada herramienta. Una confusión entre dos empresas del mismo gestor
no da error, da una semana montada en la empresa equivocada.

La primera versión de esta decisión ataba el token a una empresa elegida en un selector de la
pantalla de consentimiento, con una URL única para todos. Tenía una pega práctica: claude.ai
y ChatGPT identifican cada conector por su URL, y no está confirmado que dejen añadir la misma
dos veces en la misma cuenta. Una persona con dos empresas se quedaría con una conectada y
tendría que desconectar y reconectar para cambiar.

## Decisión

1. **La empresa va en la URL del servidor MCP:** `…/api/v1/assistant/mcp/e/{entityId}`. Cada
   empresa es un conector distinto para el cliente, con su propio `resource`. El emisor OAuth
   es el mismo para todas.
2. **El token queda atado a un `uid` y a esa URL.** El servidor MCP sólo acepta un token cuyo
   `resource` sea exactamente la URL a la que se está llamando: el token de una empresa no
   vale en la URL de otra.
3. **Las herramientas no reciben `entityId`.** Lo pone el servidor desde la URL y la conexión.
   El modelo no puede equivocarse de empresa porque no tiene con qué.
4. **No hay selector.** La pantalla de consentimiento comprueba que la persona tiene asiento
   activo de `owner` o `admin` en la empresa de la URL; si no lo tiene, se para antes de pedir
   nada. Si lo tiene, enseña esa empresa y pide el consentimiento.
5. **Una persona con varias empresas añade varias URLs**, una por empresa, y cada una aparece
   en su cliente como un conector con el nombre de la empresa (`serverInfo.title`:
   «CheckBiz360 · Limpiezas Pérez»).
6. **La revocación es por conexión**, es decir, por empresa.

## Alternativas descartadas

- **URL única y selector de empresa en el consentimiento** (la primera versión). Un paso más
  en la pantalla y la pega de la URL repetida en el cliente. Para quien tiene una sola empresa
  no era más cómodo: pega una URL igualmente.
- **Token por persona, empresa por llamada** (el modelo del servicio de tareas). Más flexible
  y una sola conexión por usuario, a cambio de dejar la elección de empresa en manos del
  modelo en cada turno. Lo que se gana en comodidad se pierde en la primera semana escrita en
  el sitio equivocado.
- **Una herramienta «cambiar de empresa»** que mueva un estado en la conexión. Es lo mismo
  con un paso más y un estado que nadie ve.

## Consecuencias

- El cliente necesita la URL de su empresa. La ficha del add-on en el panel (fase 3) la enseña
  para copiar; en la prueba de staging se monta a mano con el id de la entidad de demo.
- El id de una empresa no es un secreto: ya va en las URLs del panel. Sin asiento en ella, la
  URL no sirve de nada, y probar ids al azar sólo produce pantallas que se paran.
- Los metadatos del recurso protegido se generan por empresa, al vuelo, en la ruta con el
  camino insertado que marca la RFC 9728. No hay un documento en la raíz, porque no hay un
  recurso único que anunciar.
- El `resource` de la petición de autorización pasa a ser obligatorio: de él sale la empresa.
  La especificación ya obliga al cliente a mandarlo.
- El registro de una conexión (`assistant_connections`) sigue siendo la unidad de auditoría:
  quién, qué empresa, desde qué cliente, cuándo se creó, cuándo se usó y cuándo se cortó. Es
  lo que la pantalla «Conexiones» del panel listará en la fase 3.
- Si el asiento se desactiva o pierde el rol, la conexión deja de servir en la siguiente
  llamada: el servidor comprueba el asiento en cada petición, no sólo al conectar.

# ADR-009 — Una conexión es una persona, con todas sus empresas

**Fecha:** 2026-10-17
**Estado:** Aceptado. Sustituye a ADR-002 para las conexiones nuevas.
**Decisionario:** Jose Acevedo («lo del conector por empresa está bien, pero me limita muchísimo uno de nuestros targets, que es la multientidad»; «después migra a esto, es mucho más versátil»)

---

## Contexto

ADR-002 ató cada conexión a una persona **en una empresa**, con la empresa en la URL
(`/mcp/e/{entityId}`). El motivo era prudente: no se sabía si Claude y ChatGPT admitían el
mismo conector dos veces. Funciona, pero castiga justo al cliente que más vale: la gestoría
o el grupo que lleva varias empresas tendría que dar de alta un conector por empresa, y su
asistente no podría comparar ni saltar de una a otra en la misma conversación.

## Decisión

1. **Una URL por persona**: `…/api/v1/assistant/mcp`. El `resource` de OAuth es esa URL y la
   conexión guarda `entityId: null`, que significa «las empresas de esta persona».
2. **Las empresas son las del panel, en cada llamada.** Autorizar no congela una lista: cada
   herramienta comprueba en ese momento que la persona es owner o admin (y no soporte) en la
   empresa pedida. Si en el panel le quitan una empresa, el asistente deja de verla en la
   siguiente llamada; si le dan una nueva, la ve sin volver a conectar. Para autorizar hace
   falta administrar al menos una.
3. **`listar_empresas`** devuelve las empresas donde la persona administra, con su rol.
4. **Cada herramienta lleva `empresaId`**, obligatorio. La empresa **no** se guarda en el
   servidor como «empresa activa»: con dos conversaciones abiertas sobre empresas distintas, un
   estado compartido mandaría un cambio a la empresa equivocada sin que nadie lo viera. La
   elección vive en la conversación y viaja en cada llamada.
5. **Las instrucciones** mandan empezar por `listar_empresas`; si hay más de una, preguntar con
   cuál trabajar antes de nada, decir siempre la empresa al proponer un cambio, y no mezclar
   empresas en una misma acción.
6. **Sin una empresa a la que no tenga acceso, nada.** Pedir una empresa ajena responde
   `sin_acceso_a_la_empresa`, sin revocar la conexión: la persona sigue administrando las
   demás. (En ADR-002, perder el asiento cortaba la conexión, porque era de esa empresa.)
7. **Las conexiones por empresa siguen funcionando.** Las URL `/mcp/e/{entityId}` ya dadas no se
   rompen; el panel deja de ofrecerlas y enseña la URL personal.

## Alternativas descartadas

- **«Empresa activa» guardada en la conexión** (`elegir_empresa`): un estado compartido entre
  conversaciones. El fallo que provoca es silencioso y cae en una escritura.
- **Elegir la empresa en la pantalla de autorización**: vuelve a ser una conexión por empresa.
- **Una lista de empresas congelada al autorizar**: se queda vieja el día que cambia un rol, y
  obliga a reconectar para ver una empresa nueva.

## Consecuencias

- El servidor MCP personal registra las mismas herramientas con `empresaId` delante y una
  guarda común que comprueba el asiento antes de cada una; el código de cada herramienta no
  cambia.
- La pantalla de consentimiento dice «tus empresas» y lista las que administra hoy.
- El panel muestra una sola URL, la misma en todas las empresas de la persona.
- Los enlaces de Excel firmados ya llevan la empresa dentro: no cambian.

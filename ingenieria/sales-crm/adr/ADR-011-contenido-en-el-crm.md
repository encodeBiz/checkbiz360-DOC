# ADR-011 — El contenido vive en el CRM, con su historia, y lo leen los agentes

**Fecha:** 2026-10-28
**Estado:** Propuesto
**Decisionario:** Jose Acevedo («una nueva sección de contenido donde pueda subir la planificación
exacta, Blog, LinkedIn, Instagram y un responsable (…) conectado por el MCP (…) debe quedar en el
histórico, ya que es dato que nuestros agentes deben controlar también para sacar mensajes,
contactos, InMail»; «hay contenido que lo impulsa una señal»)

---

## Contexto

La parrilla de contenido existe hoy como una página suelta (p. ej. la de LinkedIn del 26-oct al
20-nov: doce posts con nicho, dolor, solución, funcionalidad, enlace con UTM, imagen o captura a
pedir y texto listo). Nadie la revisa en un sitio, no tiene responsable ni estado, y los agentes
que redactan InMails no la ven: pueden contradecir en privado lo que se dijo en público, o no
aprovechar un post que encaja con la señal de una empresa.

## Decisión

1. **El contenido es parte del CRM** (`services/sales`, ADR-001): mismo dueño del dato comercial,
   misma puerta para el agente (MCP, ADR-005) y para el backoffice.
2. **Ficha y publicación.** La ficha es el encargo (qué explicar, imagen, enfoque, límites); de
   ella salen una o varias publicaciones, cada una en un **perfil** (canal × marca: «Instagram
   CheckBiz360», «Blog encodeBiz») con su fecha y su estado. No tienen cliente. Lo ya publicado
   entra con su decisión editorial.
3. **Responsable y revisión por personas del backoffice.** Cualquier usuario del backoffice con
   permiso de escritura en el CRM puede ser responsable y aprobar.
4. **Solo se añade.** Cada cambio de texto, fecha, estado o adjunto, y cada comentario de
   revisión, queda en el historial de la pieza con quién y cuándo. Lo publicado no se borra.
5. **Una pieza puede estar impulsada por señales** (0..n). El enlace no caduca aunque la señal sí.
6. **El agente prepara, la persona publica** (ADR-006): el agente crea y edita borradores y marca
   «publicada» cuando la persona lo confirma; no publica en ninguna red. **Aprobar es de una
   persona**, salvo que la persona se lo pida expresamente al agente, y entonces queda en el
   historial quién lo pidió ([TDR-011](../tdr/TDR-011-contenido.md)).

## Alternativas descartadas

- **Herramienta de calendario externa** (Notion, Metricool…): los agentes no la ven por el MCP
  del CRM y la señal no se puede enlazar.
- **Contenido como «acción planificada» sin contacto:** una acción es «hacer algo con alguien»
  y se cierra con una actividad; una pieza tiene revisión, adjuntos, texto largo y vida después
  de publicada.

## Consecuencias

- La skill de mensajes lee lo publicado reciente antes de redactar, y lo que se ha publicado sobre
  la señal de la empresa a la que escribe.
- Los adjuntos van al bucket del sistema, fuera del cobro de almacenamiento (no son de ninguna
  empresa cliente).

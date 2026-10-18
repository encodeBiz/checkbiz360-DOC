# ADR-010 — Los prompts de Merlin se afinan desde Ajustes, y Merlin busca señales a petición

**Fecha:** 2026-10-18
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («necesito poder modificar el prompt desde Ajustes del CRM → Investigación con Merlin para poder ir afinando todo; además quiero poder lanzar "Buscar señales con Merlin" de forma manual desde la vista principal, también con un prompt configurable; y que todo lo demás tribute sobre cómo está ahora: tokens, modelo, etc.»)

---

## Contexto

El prompt de investigación (ADR-009, [08](../08_el-prompt-de-investigacion.md)) vive en el
código de Merlin. Cada retoque —y en dos días ha habido tres— es un pase completo:
develop, staging, PR a main. Afinar un prompt es un trabajo de leer resultados y tocar una
frase; con ese ciclo no se afina, se aguanta.

Las señales de «por qué ahora» (ADR-004) entran hoy por dos vías: la vigilancia de la
PLACSP, que es programada y sólo ve adjudicaciones, y Claude en el chat, con el skill
`senales` del plugin, cuando Jose se lo pide. La segunda es la que encuentra lo demás
(centros nuevos, contratación de campo, relevos, prensa local), pero depende de abrir el
chat y de la cuenta de claude.ai. Merlin ya sabe buscar con la misma base (TDR-007) y ya
tiene topes, modelo y contador de tokens en Ajustes (TDR-008).

## Decisión

1. **Los prompts son configuración, no código.** Tres textos en `sales_crm_settings`:
   `investigacion.prompts.dossier`, `investigacion.prompts.perfil` y `senales.prompt`.
   Vacío significa «el de fábrica», que sigue en Merlin (`prompt.ts`) y es lo que se
   despliega y se prueba. Merlin expone los de fábrica (`GET /gpt/investigacion/prompts`)
   y acepta en cada petición las instrucciones que `sales` le mande; `sales` manda las
   guardadas, si las hay. El panel enseña los dos (el de fábrica y el afinado), marca
   cuándo difieren y tiene «Restaurar el de fábrica».

2. **Lo que no se afina desde el panel.** El esquema JSON de la respuesta (es el
   contrato), el conocimiento del nicho y del producto (los ficheros del plugin, que
   Merlin lee de su imagen) y las comprobaciones del servidor: sólo cuentan las URL que la
   API dice haber consultado, la identidad tiene que quedar atada a una página, un decisor
   necesita nombre y apellido, una señal necesita fuente y fecha. Un prompt malo baja la
   calidad; no puede meter en el CRM un dato sin prueba. Eso es lo que hace razonable dejar
   el prompt en manos de quien vende.

3. **«Buscar señales con Merlin» es el porte del skill `senales`.** A petición, desde el
   pipeline: nicho, cuántos días hacia atrás y un foco opcional en texto («Andalucía»,
   «colegios», «subrogación»). Dos llamadas como en la investigación —búsqueda web y
   después JSON estricto— y las mismas reglas de siempre: señal sin URL consultada no es
   señal; fecha fuera de la ventana, fuera; una licitación en plazo no es una
   adjudicación. Lo que pasa:
   - empresa que ya está en el CRM (mismo CIF, mismo dominio o mismo nombre normalizado):
     se le añade la señal; si estaba perdida y la señal vive, vuelve a `signal` sola,
     como con cualquier señal;
   - empresa que no está: se da de alta con la señal, `source: outbound` y autor
     `merlin:senales`, sólo si Merlin dice que encaja, si `senales.altaAutomatica` está
     encendido y hasta `senales.maxNuevasPorBusqueda`. Lo que sobre queda en el registro
     de la búsqueda como «no dada de alta: tope», para que no se pierda.
   Cada búsqueda deja una fila con lo que encontró, lo que hizo con cada hallazgo y lo
   que descartó y por qué. Es la pantalla con la que se afina el prompt.

4. **Mismo presupuesto, mismo modelo.** Las búsquedas gastan del mismo tope diario de
   tokens que la investigación, con el mismo modelo, esfuerzo y lectura de página de
   Ajustes → Investigación con Merlin, y salen en el mismo «uso de hoy». Sin presupuesto,
   la búsqueda se rechaza antes de llamar (409 `budget_exhausted`): el botón dice que hoy
   ya no hay, en vez de gastar y fallar. Una búsqueda a la vez por nicho.

5. **Manual, no programada, por ahora.** Lo programado sigue siendo la PLACSP. Merlin
   busca cuando Jose pulsa. Programarla es una línea más sobre la misma función; se
   escribirá cuando dos semanas de búsquedas a mano digan que compensa (cuántas altas
   buenas por euro) y con qué cadencia.

## Alternativas descartadas

- **Prompts en los ficheros del plugin**, junto al conocimiento. Siguen siendo código:
  cambiarlos es desplegar, que es justo lo que se quiere evitar. El conocimiento sí se
  queda ahí porque cambia poco y lo comparten Claude y Merlin.
- **Revisar los hallazgos antes de darlos de alta.** Una pantalla más y una cola que
  alguien tiene que vaciar. Los topes, la exigencia de fuente y el «no encaja» de la
  ficha hacen el mismo trabajo, igual que con la PLACSP.
- **Programar ya la búsqueda.** Sin datos de cuánto encuentra y cuánto cuesta, una
  programación sólo garantiza el gasto.

## Consecuencias

- Un prompt editado se guarda con quién y cuándo (fila de ajustes y auditoría del
  backoffice). No hay historial de versiones: el de fábrica es el punto de retorno. Si
  hace falta comparar versiones, se copia el texto antes de cambiarlo.
- La coincidencia por nombre normalizado (sin «S.L.», acentos ni puntuación) evita
  duplicar la misma empresa escrita de dos maneras; cuando no coincide nada, se da de
  alta. Dos cuentas para una empresa se arreglan hoy a mano (marcar una como «no
  encaja»); fusionar cuentas sigue fuera.
- La fila de cada búsqueda guarda también el dossier de Merlin. Es texto largo; vale
  para afinar y para auditar, y se podrá podar más adelante si pesa.
- TDR: [TDR-009](../tdr/TDR-009-prompts-editables-y-senales-con-merlin.md).

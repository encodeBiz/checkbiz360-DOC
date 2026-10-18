# ADR-009 — Merlin investiga en el servidor, con la API de OpenAI

**Fecha:** 2026-10-16
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («integrar automatizaciones de investigación con Merlin»; «puedes subirlo gpt-5-mini paramétricamente, el prompt debe ser muy bueno para que no alucine»)

---

## Contexto

La investigación de una cuenta (ADR-003: sin perfil no hay contacto) la hace hoy Claude
desde la cuenta de claude.ai de Jose, cuando se lo pide. La vigilancia de licitaciones ya
da de alta empresas solas (limpieza y SAD), así que la cola de cuentas en `signal` sin
perfil crece sin que nadie la investigue. Merlin ya habla con la API de OpenAI (Responses
API, `gpt-5-mini`) para la inteligencia operativa y la puesta en marcha.

## Decisión

1. **Merlin investiga en el servidor.** `services/merlin` expone `POST /api/v1/gpt/investigacion/cuenta`
   (S2S, `ENCODEBIZ_API_KEY`): recibe los datos de la cuenta y sus señales, busca en la web
   con la herramienta de búsqueda de la Responses API y devuelve un perfil estructurado.
   `sales` sigue siendo el único que escribe el CRM: él decide qué investigar, llama a
   Merlin y guarda con las mismas reglas que al agente (`SaveProfile`, actor
   `merlin:investigacion`).
2. **Modelo y esfuerzo por configuración**, no en código: `CRM_INVESTIGACION_MODELO`
   (`gpt-5-mini` de partida), `CRM_INVESTIGACION_RAZONAMIENTO` y el tamaño del contexto de
   búsqueda. Subir el modelo es cambiar una variable y redesplegar.
3. **La prueba es lo que decide qué se guarda.** Solo cuentan como fuente las URLs que la
   API devuelve como consultadas (`url_citation`) en esa misma investigación. Un dolor cuya
   evidencia no esté ahí se descarta; una empresa cuya identidad (CIF, dominio o el concurso
   de la señal) no se haya confirmado con una fuente no se guarda; sin dolores con prueba,
   no hay perfil y queda constancia del porqué. La calidad se arregla en el prompt y en
   estas comprobaciones, nunca recortando la respuesta.
4. **Mismo conocimiento que el agente.** Merlin lee los ficheros de nicho, producto y
   posicionamiento del plugin `checkbiz360-gtm` (copiados a su imagen): una sola fuente para
   los dos.
5. **Merlin no contacta ni planifica.** Investiga y propone encaje; redactar y planificar
   sigue siendo de Claude o de la persona (ADR-006, ADR-008).
6. **Tope diario** de investigaciones y de tokens, y cada ejecución queda registrada con su
   consumo, para medir coste y calidad antes de subir el ritmo.

## Alternativas descartadas

- **Suscripción de ChatGPT:** un servidor no puede usarla; solo la API, que se paga por uso.
- **Tarea programada en Cowork:** funciona, pero depende de la cuenta personal de claude.ai y
  no deja registro de coste ni se puede acotar desde la plataforma.
- **Buscar con un proveedor externo (SerpAPI, Tavily…):** otra dependencia y otro contrato
  de datos; la Responses API ya trae la búsqueda y las citas.

## Consecuencias

- Primer paso obligado: **10 cuentas ya investigadas por Claude, reinvestigadas por Merlin
  en seco** (sin guardar), y Jose decide con las dos delante si la calidad basta y con qué
  modelo. Hasta entonces el barrido diario no se enciende.
- Un nicho nuevo exige su fichero de conocimiento (como ya pasa con el agente).
- El panel distingue quién investigó: «Merlin», «Agente» o la persona.

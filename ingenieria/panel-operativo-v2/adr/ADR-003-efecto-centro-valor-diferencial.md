# ADR-003 — El efecto centro como valor diferencial del producto

**Fecha:** 2026-07-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Todo el mercado de control horario mide **a la persona**: horas, puntualidad, coste, ausencias.
Ninguna herramienta del nicho responde la pregunta que de verdad decide dinero en operación de
campo:

> ¿El problema es la persona o es el sitio?

Hoy esa pregunta se resuelve a ojo. Se despide a trabajadores que solo estaban en un centro mal
gestionado, y se mantiene a encargados que queman plantilla tras plantilla porque sus números
agregados salen decentes. Nadie tiene evidencia para separar ambos efectos.

CheckBiz sí puede, porque guarda el patrón de cada empleado con **granularidad dual**. Medido en
producción (2026-07-28):

- **203** snapshots de empleado **con** `branch_id` → cómo rinde esa persona *en ese centro*
- **204** snapshots de empleado **sin** `branch_id` → cómo rinde esa persona *en general*
- 5 empleados con historial en más de una sucursal
- 27 empleados con perfil, serie diaria desde 2026-01-01

---

## Decisión

Se adopta el **efecto centro** como métrica insignia del panel: para cada trabajador se calcula el
delta entre su rendimiento en un centro y su rendimiento global, y el agregado de esos deltas entre
todos los que pasan por el centro constituye el efecto que ese entorno ejerce sobre las personas.

Algoritmo en **TDR-001**.

---

## Justificación

**Responde una pregunta cara que nadie más responde.** No es una métrica más bonita: es una
decisión de negocio (despedir, formar, reasignar, cambiar al responsable) que hoy se toma sin datos.

**Es defendible ante el trabajador.** Al comparar a cada persona consigo misma, no arrastra sesgos
de cohorte ni de antigüedad. En un producto de control horario, que una métrica sea defendible en
una conversación laboral no es un detalle: es requisito.

**Esquiva el sesgo de arranque.** Como es un delta contra uno mismo, no depende de umbrales
absolutos y por tanto no le afecta que `totalExperienceYears` esté en semanas (ver ADR-005). Es la
única de las métricas de alto valor que **se sostiene con el estado actual de los datos**.

**Es difícil de copiar.** Requiere patrón individual, el mismo patrón desagregado por centro y la
historia diaria de ambos. Un competidor que copiara la idea mañana necesitaría años de acumulación.

**Alimenta a las demás.** El efecto centro es el numerador natural de "capacidad de formación" y el
contexto que da sentido a la fragilidad.

---

## Consecuencias

**Positivas**
- Diferenciador real y comunicable en una frase
- Convierte el histórico acumulado en ventaja competitiva acumulativa
- Aísla responsabilidad de gestión de la responsabilidad individual

**Negativas / compromisos**
- Con 5 empleados en varias sucursales, los casos cruzados limpios son pocos hoy. El delta
  por-sucursal vs global se calcula para los 27 con perfil, acompañado del estado de madurez
  (ADR-004). La precisión crece sola con la movilidad
- Un centro con un único trabajador no tiene efecto centro medible: su patrón por sucursal y su
  patrón global son casi el mismo. Debe devolverse explícitamente como no calculable
- Requiere que el sync de patrones de empleado siga poblando ambas granularidades

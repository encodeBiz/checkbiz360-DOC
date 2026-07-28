# ADR-002 — Una espina dorsal de tres índices leída en tres niveles

**Fecha:** 2026-07-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El panel tiene que servir a tres audiencias con la misma pantalla: dirección (toda la entidad),
jefatura de zona (la sucursal) y mando intermedio (la persona).

La tentación natural es dar a cada nivel sus propias métricas: coste y horas arriba,
cumplimiento en el centro, `promotionScore` en la persona. El resultado de eso es **tres
dashboards pegados con el mismo logo**: el usuario cambia de nivel y cambia de vocabulario, no
puede rastrear una causa de arriba abajo, y la vista deja de ser simple — que es exactamente lo
que el cliente reprocha del panel actual.

---

## Decisión

Los tres niveles comparten **los mismos tres conceptos**, leídos a distinta altura:

| Concepto | Entidad | Sucursal | Empleado |
|---|---|---|---|
| **Fiabilidad** | Media y dispersión de la organización | Del centro | De la persona, normalizada por madurez |
| **Efecto entorno** | Distancia entre el mejor y el peor entorno | Cuánto suma o resta el centro a quien pasa por él | Cuánto le afecta su centro actual |
| **Fragilidad** | Cuántos centros en riesgo por dependencia | Concentración de la operación en pocas manos | Cuánto depende el centro de esta persona |

Cualquier métrica nueva debe poder colocarse bajo uno de los tres. Si no encaja en ninguno, no
entra en la cabecera del panel: baja al detalle.

---

## Justificación

**Permite drill-down real.** El recorrido es una sola frase encadenada: la organización tiene
entornos muy desiguales → este centro es el que peor efecto ejerce → dentro, estas dos personas lo
sostienen y esta se está degradando. Con métricas distintas por nivel esa cadena no existe.

**Reduce la carga cognitiva sin perder información.** Tres ideas que se repiten se aprenden una
vez. Diecinueve métricas sueltas se aprenden diecinueve veces, que es la razón de que hoy nadie
use el panel entero.

**Es una restricción de diseño, no solo una taxonomía.** Obliga a rechazar métricas que no
respondan a ninguna de las tres preguntas, que es el mecanismo que impide que el panel vuelva a
crecer hasta ser inservible.

**Los tres conceptos son ortogonales.** Un centro puede ser muy fiable y a la vez muy frágil
(funciona perfecto porque una sola persona lo sostiene). Esa combinación es información de alto
valor y hoy es invisible.

---

## Consecuencias

**Positivas**
- Una sola vista navegable en profundidad, con vocabulario constante
- Criterio objetivo para aceptar o rechazar métricas futuras
- Las combinaciones entre índices (fiable + frágil) son señales nuevas por sí mismas

**Negativas / compromisos**
- Obliga a definir cada índice en los tres niveles antes de publicarlo, aunque en algún nivel sea
  menos natural
- Métricas útiles pero que no encajan (por ejemplo, coste absoluto) pierden protagonismo; es una
  decisión deliberada, no un descuido

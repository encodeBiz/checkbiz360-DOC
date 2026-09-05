# ADR-003 — El primer mes, la plantilla entera aparece como «en riesgo»

**Fecha:** 2026-09-05
**Estado:** **Propuesto** — la decisión es de producto y está pendiente
**Decisionario:** Jose Acevedo

---

## La medida (dev-encodebiz, 2026-09-03)

Con un mes de asistencia sembrada y **deliberadamente buena** —gente puntual, jornadas
completas, incidencias por debajo del 3%—, la clasificación de los 42 patrones de empleado
salió así:

| Arquetipo | Empleados |
|---|---|
| `at-risk` | 30 |
| `ghost` | 8 |
| `neutral` | 4 |

Ninguno salió `anchor`.

## Por qué

`ProfileClassifier` marca `at-risk` por asistencia sola cuando `reliability < 0.5`. Y
`reliability` no mide comportamiento: es el producto de **cuánto dato hay** por **cómo de
bueno es**, `dataMaturity × dataQuality`.

Con 21 jornadas por persona, la madurez media quedó en 0,716 y la calidad en 0,692. Su
producto es 0,495 — justo por debajo del umbral. La media real de fiabilidad fue **0,427**, y
38 de los 42 patrones cayeron por debajo de 0,5.

Es decir: **la etiqueta no está diciendo que la persona sea un problema. Está diciendo que el
sistema todavía no tiene datos suficientes para opinar.** En pantalla las dos cosas se leen
igual.

## El problema

Un cliente nuevo cuya plantilla fiche impecablemente durante su primer mes abrirá el panel y
verá a casi toda su gente marcada como «en riesgo». Es la peor primera impresión posible, y
contradice el principio de que *un aviso que pide arreglar algo que ya está bien es peor que
no avisar*: enseña a ignorar la lista entera.

## Opciones, sin decidir

1. **No enseñar arquetipo hasta que el patrón madure.** Un estado explícito de «aún
   aprendiendo» en lugar de una etiqueta que no toca.
2. **Separar «poco dato» de «mala señal».** Que `at-risk` por asistencia exija además
   madurez suficiente, y que la falta de datos tenga su propia etiqueta.
3. **Mover el umbral.** El más barato y el peor: no arregla que la métrica mezcle dos cosas
   distintas.

La recomendación es la 2, porque ataca la causa —`reliability` compone dos magnitudes que no
significan lo mismo— en vez de tapar el síntoma. Pero es una decisión de producto y afecta a
`ProfileClassifier`, que vive en `encodebiz-api`, fuera del alcance de este módulo.

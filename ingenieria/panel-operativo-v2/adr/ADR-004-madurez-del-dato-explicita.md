# ADR-004 — La madurez del dato viaja en el contrato y se comunica en el front

**Fecha:** 2026-07-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Varias señales del sistema están en fases distintas de maduración, y eso es **normal en un
producto vivo**, no una avería. Medido en producción (2026-07-28):

- `taskSignals`: presente en 46 de 406 snapshots — el módulo de tareas es reciente
- `task_ratings_raw`: 1 fila
- `pattern_snapshots` de sucursal: 26 días de recorrido
- `pattern_snapshots` de empleado: desde enero, completos
- Cobertura de `price`: parcial, según lo que cada cliente haya configurado

El panel actual no distingue nada de esto. Una métrica sin datos suficientes se pinta igual que
una consolidada: un gráfico vacío, un cero, o una línea plana. El efecto es doble y ambos son
malos — el cliente interpreta el vacío como error del producto, o peor, interpreta un cero
artificial como un dato real.

El caso más grave es el coste: `base.price ?? 0` hace que un empleado sin tarifa configurada
sume horas al denominador y cero euros al numerador, sesgando el total a la baja **sin ninguna
marca**.

---

## Decisión

**Toda métrica del panel viaja con su estado de madurez en la respuesta del API**, y el front está
obligado a comunicarlo. Ninguna métrica se publica "desnuda".

Estados:

| Estado | Significado | Tratamiento en el front |
|---|---|---|
| `ready` | Datos suficientes y consolidados | Se muestra normal |
| `warming` | La señal existe pero aún no alcanza el mínimo | Se muestra el progreso: "acumulando datos — disponible a partir de N registros" |
| `partial` | Calculada sobre un subconjunto | Se muestra con su cobertura: "6 de 10 empleados con tarifa configurada" |
| `unavailable` | No calculable con los datos actuales | Se explica el motivo; no se dibuja gráfico vacío |

Para métricas de cobertura parcial se acompaña siempre el ratio (`covered` / `total`). Si la
cobertura cae por debajo del umbral definido para esa métrica, **no se muestra el valor**: se
muestra qué falta por configurar.

---

## Justificación

**Convierte una carencia en señal de rigor.** Un panel que dice lo que sabe y lo que todavía no
genera más confianza que uno que rellena huecos con ceros. El cliente que descubre un número
inventado deja de creerse el panel entero, incluidas las partes correctas.

**Es un motor de adopción.** Al mostrar qué falta por configurar, el panel empuja al cliente a
completar su configuración, y cada vez que lo hace el panel mejora solo delante de sus ojos.

**Protege el lanzamiento de módulos nuevos.** Tareas acaba de estrenarse. Con este contrato, sus
métricas pueden salir el primer día en estado `warming` sin dañar la credibilidad del resto.

**Evita el peor fallo posible en este dominio:** presentar un dato falso con apariencia de
precisión.

---

## Consecuencias

**Positivas**
- El front nunca tiene que adivinar si un vacío es un error o una ausencia legítima
- Permite publicar métricas antes de que estén maduras, con honestidad
- Elimina el sesgo silencioso del coste

**Negativas / compromisos**
- Todo endpoint del panel debe calcular y devolver el estado, no solo el valor
- El front necesita componentes específicos para `warming`, `partial` y `unavailable`; es trabajo
  adicional en la fase de integración
- Definir el umbral mínimo de cada métrica es una decisión que hay que tomar una por una

# ADR-006 — La plantilla se sigue por eventos de estado; el pasado se reconstruye y se marca

**Fecha:** 2026-10-12
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

La gráfica de contratación de la portada (`EmployeeTrendChart`) no sirve para seguir la
plantilla. El navegador descarga de Firestore hasta 10.000 empleados dados de alta en el año y
los cuenta por mes de alta (`getEmployeeStatsByYear`). Solo ve un año, no acumula y solo mide
altas. Jose pidió el 2026-10-12 una gráfica de líneas con **activos, despedidos e inactivos** en
el tiempo, progresiva y desde Postgres.

El dato para eso no existe. Medido en producción el 2026-10-12 (129 empleados, 12 empresas):

| Estado | Personas | Fecha que lo sitúa |
|---|---|---|
| Activos | 105 | `createdAt`, exacta |
| Despedidos | 9 | `updatedAt`: `deleteEmployee` la escribe al despedir; en los 9 es distinta del alta |
| Inactivos | 15 | Ninguna: ni uno tiene `updatedAt` |

La ficha guarda el estado actual y no cuándo cambió. `dim_employees` copia el estado actual y
cada sincronización lo pisa.

## Decisión

1. **De hoy en adelante, eventos exactos.** La sincronización de dimensiones compara el estado
   que trae Firestore con el que ya tenía `dim_employees` y, si cambió, anota un evento en
   `employee_status_events` con la hora de la sincronización. Corre cada hora, así que la
   precisión es de una hora. Un alta nueva anota su evento con su `createdAt`.
2. **Una foto diaria** por empresa y centro en `headcount_daily`: cuántas personas hay en cada
   estado. Es la comprobación de que los eventos cuadran, y la serie exacta a partir del día
   que arranca.
3. **El pasado se reconstruye una vez y se marca.** Altas con `createdAt` (`source: created_at`,
   exacta). Despidos con `updatedAt` (`source: estimated_updated_at`). Los inactivos actuales
   sin fecha no se sitúan en el pasado: su evento se fecha el día que arranca el seguimiento
   (`source: tracking_start`). Hasta ese día cuentan como activos, y la respuesta lo dice.
4. **La serie sale de reproducir los eventos**, mes a mes, sin límite de años, por una ruta de
   `analytics` sobre Postgres. El navegador deja de descargar empleados.

## Alternativas descartadas

- **Seguir contando altas por mes en el navegador.** Es lo que falla: no acumula, no ve bajas
  y descarga la plantilla entera, contra los patrones de la plataforma.
- **Fechar a los inactivos con su alta.** Diría que nunca trabajaron. Peor que no fecharlos.
- **Esperar a tener historia propia para enseñar nada.** Sin pasado, la gráfica tardaría meses
  en decir algo. La reconstrucción marcada es honesta y útil desde el primer día.

## Consecuencias

- La serie de despidos antiguos es aproximada si alguien editó la ficha después de despedir.
  Se marca, no se disimula.
- Un borrado físico de la ficha en Firestore no se ve como evento: la fila de `dim_employees`
  se queda con su último estado. El borrado normal es blando (`status: fired`).
- **El arreglo de raíz queda pendiente:** que la baja y el paso a inactivo guarden su fecha en la
  ficha (`firedAt`, `statusChangedAt`). Con eso, la detección por comparación pasa a ser red.

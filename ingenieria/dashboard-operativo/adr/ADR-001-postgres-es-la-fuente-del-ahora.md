# ADR-001 — Postgres es la fuente del ahora; Firestore sólo fuera de la ruta caliente

**Fecha:** 2026-10-10
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

El dashboard necesita el estado operativo de este instante: quién está, qué tareas van tarde,
cuánto se lleva gastado. La fuente de verdad de todo eso es Firestore. Hasta ahora, cada lectura
«del ahora» de la plataforma se ha hecho contra Firestore desde el contenedor (disponibilidad,
el diseño de presencia), y las lecturas históricas contra Postgres (el Panel mensual).

Jose fijó la restricción el 2026-10-10: **tirar de Postgres todo lo que se pueda; de Firebase,
sólo cuando sea inevitable.**

Lo medido ese día ([01_as-is §3](../01_as-is.md)): los fichajes llegan a Postgres en vivo por
trigger; las dimensiones existen pero nadie las refresca; las tareas no están; el inventario sí.

## Decisión

El hoy se calcula **íntegramente sobre Postgres**. Lo que falta allí y hace falta se espeja
(tareas). Lo que está pero no es fiable se endurece (conciliación de fichajes, cron de
dimensiones). Las únicas lecturas de Firestore que introduce este proyecto son tres, todas de
mantenimiento, todas fuera de la petición del navegador: conciliar, re-espejar, refrescar.

## Alternativas descartadas

- **Leer Firestore desde `analytics` al servir `/today`.** Es lo que hace disponibilidad y lo
  que propone Presencia, y funciona. Pero cada petición cruza de OVH a GCP cinco o más veces, un
  sondeo de 60 s por gerente lo multiplica, y rompe la regla de Jose sin necesidad: el dato ya
  viaja a Postgres.
- **Mixto: fichajes de Postgres, tareas de Firestore.** Dos fuentes con dos frescuras en la
  misma pantalla. El día que diverjan nadie sabrá cuál creer. Y el espejo de tareas es una fase
  de trabajo, no un proyecto.

## Consecuencias

- El espejo pasa a ser infraestructura crítica. Hoy no lo era: si perdía un fichaje, el Panel
  mensual se desviaba una décima. Mañana, si pierde un fichaje, el gerente ve a alguien «sin
  fichaje» que sí fichó. Por eso la fase 1 va antes que la 2 y por eso la respuesta lleva
  `freshness`.
- `analytics` gana un planificador. No lo tenía porque no lo necesitaba.
- La regla queda escrita para lo siguiente: una lectura nueva del panel no abre Firestore si el
  dato puede estar en Postgres. Si no puede, se espeja primero.

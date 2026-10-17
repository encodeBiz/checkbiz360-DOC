# ADR-008 — El asistente lee lo que la plataforma ya calcula

**Fecha:** 2026-10-17
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («agrega las herramientas de asistencia y análisis, para conseguir un verdadero gestor operativo»; «el cuadrante de disponibilidad también es importante, para que cruce información»)

---

## Contexto

Con las fases 1 y 2 el asistente configura la semana: horarios, tareas, altas. Un gestor
operativo además **mira** lo que está pasando y actúa: quién no ha fichado, quién puede
cubrirle, cómo va la semana frente a las anteriores, qué alerta pide atención primero.

Casi todo eso ya lo calcula la plataforma para el panel:

- `analytics`: la portada de hoy (`/panel/today`), el histórico por semanas (`/panel/weeks`),
  el mes frente al anterior (`/panel/overview`) y las alertas con sus reglas y umbrales
  (`/panel/alerts`, `alerts/rules.ts`).
- `checkinbiz`: la **disponibilidad**, por sucursal y día, con quién está, con qué turnos, y
  quién falta y por qué (festivo, ausencia, sin turno, estado). Es la misma cascada de
  calendario que aplican el fichaje y la app.
- `reports`: el informe de jornada en PDF o Excel.
- `merlin`: el relato del panel y la interpretación de patrones.

## Decisión

1. **El asistente no calcula métricas ni umbrales nuevos.** Lee las mismas respuestas que
   pinta el panel, por puertas delegadas con los permisos de la persona conectada (ADR-005).
   Si el panel dice «3 sin fichaje», el asistente dice 3.
2. **El análisis lo hace el modelo del cliente sobre hechos, no Merlin.** Claude y ChatGPT ya
   son el analista. Exponer el relato de Merlin sería pedir a un modelo que resuma a otro.
   Además, las rutas de Merlin no comprueban hoy que quien pide pertenezca a la empresa (ver
   Consecuencias).
3. **Las claves se traducen a frase antes de salir**, y lo que el modelo no debe decir no
   viaja. Es lo aprendido con el relato del panel: una alerta sale como «faltan por fichar 6
   de 10 previstos en Centro», no como `attendance_low {missing: 6}`. Los estados de
   presencia, igual.
4. **Se dice el hecho, no la causa.** «No ha fichado» y nunca «ausente» ni «no ha venido»: la
   plataforma sabe lo primero, no lo segundo. Las instrucciones lo exigen.
5. **Un solo cruce se hace en el servidor: quién puede cubrir una tarea.** Junta tres fuentes
   que el modelo no debe adivinar: la disponibilidad del día, las otras tareas de cada
   candidato y, si es hoy, si ha fichado. Devuelve **hechos por candidato, sin puntuación**: el
   orden es por grupos de hechos y la elección es de la persona.
6. **Permisos, los del panel.** Analítica: owner o admin de la empresa. Disponibilidad: el
   alcance de responsabilidad de siempre. Informes: asiento en la empresa. El conector v1 solo
   admite owner y admin, así que en la práctica entra todo lo anterior.

## Alternativas descartadas

- **Herramientas que consultan Postgres directamente desde el conector.** Una segunda
  definición de «retraso» o de «sin fichaje» que diverge de la del panel el primer día que
  alguien toque una de las dos.
- **Exponer el relato de Merlin.** Es redundante, tarda (es asíncrono) y hoy no tiene control
  de empresa.
- **Una puntuación de candidatos para cubrir.** Pesar «misma ocupación» frente a «ya está en la
  sucursal» es una decisión de negocio sin dato que la sostenga. Los hechos sí lo están.

## Consecuencias

- Puertas nuevas: `analytics` monta el router del panel también tras `requireDelegatedUser`, y
  `reports` gana una ruta delegada para generar el informe de jornada. La disponibilidad ya
  estaba en la puerta delegada del calendario de `checkinbiz`.
- **Hallazgo de seguridad, aparte de esta fase:** `POST /api/v1/gpt/panel` y
  `POST /api/v1/gpt/interpret` de `merlin` piden sesión de Firebase pero **no comprueban la
  empresa**: cualquier cuenta con sesión obtiene el análisis de otra empresa si conoce su
  `entityId`. Afecta a producción. No se arregla dentro de esta fase porque la app podría usar
  `interpret` para la persona empleada (`audience: "employee"`) y un control mal puesto la
  rompería. Queda para decisión de Jose.

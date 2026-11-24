# Panel de dirección — Hoy

**Proyecto:** encodebiz-api
**Dominio:** `services/analytics` (worker que precalcula) y `services/backoffice` (módulo `hoy`, solo lee)
**Fecha:** 2026-11-14
**Estado:** en `feat/backoffice-hoy`, sin fusionar. Migración 065 sin aplicar.
**Autor:** Jose Acevedo (pedido) · diseño y código con Claude

## Por qué

La foto de dirección es de días cerrados: se cosecha a las 3:25 y no admite el día en curso.
Jose, el 2026-11-14: «no sé si puedo desplegar una mejora desde backoffice porque no sé la
tendencia de uso de hoy por hora, o si los clientes están fichando, cuántos hay fichados; qué
han hecho y qué predecimos que pueden hacer teniendo en cuenta turnos, tareas e histórico de
la semana».

Tres preguntas, por este orden:

1. **¿Qué está pasando ahora?** Dentro, en pausa, terminados, quien debía estar y no ha
   fichado, tareas abiertas. En total y por empresa.
2. **¿Cómo va el día frente a lo normal?** Curva por horas de hoy contra el mismo día de la
   semana pasada y la media de los cuatro últimos iguales.
3. **¿Qué queda?** Entradas y salidas planificadas por turnos y tareas en las horas que
   faltan, junto a lo habitual a esa hora. De ahí sale la **ventana más tranquila**: la que
   contesta «¿despliego ahora?».

## Decisiones

1. **Todo en Postgres y precalculado.** Resolver el día de una empresa son unas seis
   consultas (centros, empleados y calendarios se cargan una vez y se resuelven en memoria),
   más fichajes y tareas del día; hacerlo para 500 empresas en cada vistazo, con varias
   pantallas abiertas, son miles de consultas por minuto. El backoffice lee tres tablas de
   resumen; no llama a analytics ni abre Firestore. Nombres y búsqueda, de `dim_entities`.
2. **La lógica de jornada es una sola.** El worker vive en analytics y usa
   `buildOperationalDay`, la misma función que `/panel/today` y el cierre diario. El
   backoffice no puede contar distinto que el panel del cliente.
3. **Solo se recalcula lo que se mueve.** Cada 5 minutos, una empresa entra en la pasada si
   (a) no tiene foto de hoy, (b) tiene fichajes o tareas espejados después de su foto,
   (c) su plan tiene entradas o salidas en la hora en curso, o (d) su foto tiene más de
   30 minutos. Tope de 80 por pasada, las más viejas primero: un día normal se mueven
   decenas, no 500.
4. **La previsión se explica.** Previsto en una hora = lo mayor entre lo planificado (entradas
   + salidas de turno + tareas que empiezan) y la media de fichajes de esa hora en los cuatro
   últimos días iguales. Sin modelo: no hay modelos hasta los 1.000 empleados.
5. **Lo que no se mide, se dice.** Un centro sin calendario espejado sale «sin medir», no con
   cero previstos. La navegación del panel no se registra en ningún sitio: «sin medir».
   Cada respuesta lleva la hora de la foto más vieja y la del último fichaje espejado.
6. **Internas fuera.** Mismo criterio que dirección (`esInterna`, por nombre y por
   `BACKOFFICE_ENTIDADES_INTERNAS`).
7. **Paginado en el servidor.** La lista de empresas va de 50 en 50, ordenada por lo que pide
   acción (quien debía estar y no ha fichado, después retrasos), con filtro «con gente
   dentro», «sin medir» y búsqueda por nombre.

## Tablas (migración 065)

| Tabla | Grano | Quién escribe | Cuándo |
|---|---|---|---|
| `operational_now` | empresa × centro (una fila, se pisa) | analytics, job «foto de ahora» | cada 5 min, solo las que tocan |
| `operational_plan_hourly` | empresa × centro × hora del día | el mismo job, con la misma pasada | al recalcular la empresa |
| `activity_hourly` | empresa × hora | analytics, job «actividad por hora» | cada 5 min las 3 últimas horas; a los :45, las 50 últimas |

`activity_hourly` cuenta fichajes, tareas iniciadas, tareas completadas y llamadas del
asistente. Las horas son UTC truncadas; la pantalla las pinta en hora de Madrid. Es además la
historia intradía que la foto nocturna no guarda (ver `historia-operativa`).

Índices nuevos para que los barridos sin empresa no recorran la tabla: `checklogs_raw
(timestamp)`, `tasks_raw (started_at)`, `tasks_raw (completed_at)`.

Relleno inicial: `services/analytics/dist/scripts/backfill-activity-hourly.js --days 35`.

## Lecturas (backoffice, permiso `stats:read`)

- `GET /api/backoffice/hoy` — totales de ahora, curva de hoy con sus dos referencias, plan de
  las horas que quedan, ventana tranquila y frescura.
- `GET /api/backoffice/hoy/empresas?offset=&limit=&orden=accion|dentro|nombre&filtro=dentro|sin_medir&q=`
  — una fila por empresa, paginada (`limit` máx. 100).
- `GET /api/backoffice/hoy/empresas/:entityId` — sus centros, su curva y su plan.

## Lo que falta

- Medirlo en prod: duración de la pasada con 80 empresas y tamaño de `activity_hourly`.
- Quién está dentro y quién falta, con nombre, en el detalle: sigue en `/panel/today` del
  cliente; el backoffice no lo enseña en esta versión.
- Uso del panel por hora: no se registra.

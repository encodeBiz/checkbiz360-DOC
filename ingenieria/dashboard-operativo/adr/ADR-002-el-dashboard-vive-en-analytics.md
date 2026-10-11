# ADR-002 — El dashboard vive en `analytics`, bajo `/panel`

**Fecha:** 2026-10-10
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Hay que elegir qué contenedor calcula y sirve el hoy y las semanas. El
[ADR-002 de Presencia](../../presencia/adr/ADR-002-donde-vive-la-presencia.md) estudió la misma
pregunta para la app un día antes y **descartó `analytics`** con este argumento: «es histórico
sobre PostgreSQL, alimentado por `sync`. La presencia es el ahora operativo sobre Firestore. No
encaja ni por dato ni por latencia».

Con [ADR-001](./ADR-001-postgres-es-la-fuente-del-ahora.md) el argumento se invierte: este
dashboard **es** una lectura de Postgres. Y lo que `analytics` ya tiene es exactamente lo que
hace falta:

- La puerta del panel: token de Firebase, CORS, `requireEntityAccess` (`owner`/`admin`).
- `PostgresCalendarRepository` y `ResolveEffectiveDayUseCase` sobre él: la cascada del calendario
  sin Firestore, verificada contra producción.
- Las tablas de dimensión y `SyncDimensions`.
- `BuildOperatingCost`, con la regla de tarifa por hora y el tope de 16 h por ciclo.
- El contrato de madurez (`BlockStatus`, `dataHealth`) que el front ya sabe pintar.

## Opciones

### A — `analytics`, dos rutas más en `panel.router.ts`

A favor: todo lo anterior; cero infraestructura; la misma puerta y los mismos tipos. En
contra: `analytics` pasa de «histórico» a «histórico y ahora». Es un cambio de alcance, no de
naturaleza: sigue leyendo sólo Postgres.

### B — `checkinbiz`, junto a disponibilidad

Donde Presencia recomienda poner su lectura. En contra: lee Firestore, no Postgres; tendría que
importar el repositorio de calendario de `analytics` o duplicarlo; y mete en el núcleo una
superficie de sondeo cada 60 s por gerente, que es justo el tipo de carga que el
[ADR-003 de salida del monolito](../../salida-del-monolito/adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md)
quiere lejos del fichaje.

### C — Contenedor propio `dashboard`

Un servicio para dos rutas que leen las mismas tablas que `analytics` con el mismo código.
Puerto, nginx, compose, health, variable. Lo que protege es nominal.

## Decisión

**A.** El dashboard vive en `analytics`, bajo `/api/analytics/panel/today` y `/weeks`, con la
puerta de siempre. `analytics` gana un planificador (un tic por minuto con `setInterval`, como `tasks` e `inventory`) para el cron
de dimensiones y el cierre diario.

## Consecuencias

- Presencia y este dashboard responden la misma pregunta desde dos contenedores y dos fuentes.
  **No es una duplicación de lógica**, porque la lógica de jornada vive en `shared` y la
  cascada del calendario es el mismo caso de uso con dos repositorios. Sí pueden diferir en
  frescura: la app lee Firestore al segundo; el dashboard lee el espejo. Por eso el espejo se
  endurece y la respuesta declara su frescura.
- La nota del ADR-002 de Presencia que dice «analytics no encaja» queda matizada: no encaja
  **para la app**, que necesita el segundo y no tiene Postgres cerca. Para el gerente en el
  panel, encaja.
- El acceso es `owner`/`admin`. Un supervisor no ve el dashboard; su herramienta es «Mi equipo»
  en la app. Si algún día el panel abre a supervisores, la puerta de `/panel` cambia para todos.

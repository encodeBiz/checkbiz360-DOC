# Dashboard operativo — el hoy y las últimas semanas en la portada del panel

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Fichajes × Calendario × Tareas × Inventario → operativa en tiempo real y su histórico semanal
**Fecha de inicio:** 2026-10-10
**Estado:** API implementada en `develop` (2026-10-11), sin desplegar · front pendiente
**Autor:** Jose Acevedo

---

## Contexto y motivación

La portada del panel (`/main/{entityId}/dashboard`) enseña hoy una tarjeta de onboarding, la
gráfica de evolución de plantilla y la lista de servicios. No dice nada de jornada, nada de
tareas y nada de coste. Y la fortaleza del producto es justo la contraria: anticipar el daño
antes de que cueste dinero.

Un gerente que abre el panel a las 8:30 tiene que ver, sin pinchar nada: cuántos de los
previstos están ya en cada centro, qué centros no tienen a nadie, quién llega tarde, qué tareas
vencen hoy y cuáles ya se han pasado, y cuánto llevan gastadas las horas y el material. No es
un análisis: son cifras concisas, con un «ver más» que abre quién está y quién no.

Y al lado del hoy, las últimas semanas con los **mismos** números. El hoy da actualidad; la
semana da proyección: un 7 de 10 no se sabe si es un buen día o el principio de un problema
hasta que se lee contra sus ocho semanas anteriores.

El estudio del 2026-10-10 comprobó pieza a pieza lo que hay ([01_as-is](./01_as-is.md)): el
Panel de CheckBiz es histórico por mes y corta en ayer a propósito; Asistencia construye las
jornadas a partir de los fichajes, así que quien no fichó no existe; Disponibilidad dice quién
debería trabajar sin mirar si vino; y el estudio de [Presencia](../presencia/README.md) cruza
las dos cosas, pero para la app del supervisor, sucursal a sucursal y sobre Firestore. Su
«vista de gerente por centros» quedó como fase posterior. **Es este dashboard.**

## Principio de diseño

> **Postgres es la fuente del ahora y del histórico. Firestore sólo cuando sea inevitable, y
> fuera de la ruta caliente.** El hoy se calcula sobre el espejo; el día se congela al cerrarse
> con el mismo cálculo; la semana es la suma de sus días. Así el hoy y el histórico nunca se
> contradicen y el pasado no se reescribe.

Tres consecuencias, cada una con su ADR:

- Lo que no está en Postgres y hace falta —las tareas— **se espeja**, no se lee de Firestore
  desde el panel ([ADR-003](./adr/ADR-003-las-tareas-se-espejan-desde-el-servicio-de-tareas.md)).
- Lo que está en Postgres pero nadie mantiene fresco —las dimensiones y los fichajes que el
  trigger pierde en silencio— **se endurece antes** de fiarse del número
  ([TDR-004](./tdr/TDR-004-endurecer-el-espejo.md)).
- El histórico **no se recalcula**: se cierra el día y se guarda
  ([ADR-004](./adr/ADR-004-el-historico-se-congela-al-cerrar-el-dia.md)).

## Alcance

**Dentro:**

- Dos lecturas nuevas en `analytics`, de sólo lectura, para el navegador:
  `GET /api/analytics/panel/today` y `GET /api/analytics/panel/weeks`
  ([03_contratos-api](./03_contratos-api.md)).
- El espejo de tareas a Postgres, escrito por el servicio `tasks` en la propia petición, con
  red de reintento y backfill ([TDR-002](./tdr/TDR-002-espejo-de-tareas.md)).
- El cierre diario por centro y la agregación semanal ([TDR-003](./tdr/TDR-003-cierre-diario-y-semanas.md)).
- Endurecer el espejo: conciliación de fichajes y cron de dimensiones ([TDR-004](./tdr/TDR-004-endurecer-el-espejo.md)).
- Promover a `@encodebiz/shared` la lógica de jornada que hoy vive sólo en el front del panel.
  Es la misma pieza que pide Presencia en su fase 1: quien llegue primero la hace y el otro la
  hereda.
- La portada del panel: bloque «Hoy» con sus tres partes y «Últimas semanas», con «ver más»
  ([05_integracion-front](./05_integracion-front.md)).

**Fuera:**

- Tocar `GET /panel/overview`. Es mensual, corta en ayer a propósito y sigue igual.
- La app móvil. Presencia es su camino; comparte la lógica de jornada, no la ruta.
- Turno por día y sucursal. Quien está en dos centros se espera en los dos
  (sobreconteo conocido de [disponibilidad TDR-001 §2.2](../disponibilidad/tdr/TDR-001-calculo-de-disponibilidad.md)).
  Se mitiga con `other_branch`, no se resuelve.
- El coste **planificado** del día. La tarifa de quien aún no fichó vive en las
  responsabilidades, que no se espejan; entra cuando se espejen.
- Alertas push desde el dashboard. Es pantalla; los avisos son de Presencia fase 3.

---

## Lo que hay hoy, en una página

Verificado contra código y contra la base de desarrollo el 2026-10-10. Detalle y cifras en
[01_as-is](./01_as-is.md).

| Dato | ¿En Postgres? | Frescura | Qué falta |
|---|---|---|---|
| Fichajes (`checklogs_raw`) | Sí | En vivo, trigger por escritura | Reintento: el trigger sólo escribe un log si falla |
| Empleados, sucursales, calendario (`dim_*`) | Sí | **Sólo cuando alguien llama al sync a mano** | Un cron, y después escritura directa |
| Tareas | **No** (sólo valoraciones) | — | El espejo entero |
| Movimientos de inventario (`item_movements_raw`) | Sí | En vivo, desde `inventory` | Nada |
| Tarifa por hora | Sí, en cada fichaje (`employee_price`) | Con el fichaje | La de quien no fichó |

Y un hallazgo que condiciona el bloque de tareas: el `timeComplianceStatus` guardado en la
tarea **sólo cambia al iniciar o completar**. Ningún planificador lo mantiene. Un «vencida» o
«en riesgo» fiable se calcula contra el reloj, no se lee del campo
([ADR-005](./adr/ADR-005-el-retraso-se-calcula-contra-el-reloj.md)).

## Arquitectura objetivo, en una página

Detalle en [02_to-be](./02_to-be.md).

```
Firestore ──trigger──▶ sync ──▶ checklogs_raw ─┐
tasks (servicio) ──en la petición──▶ tasks_raw ─┤
inventory ──en la petición──▶ item_movements ──┤──▶ analytics ──▶ GET /panel/today   (cada 60 s)
analytics (cron) ──▶ dim_employees/branches/calendars ─┘        │
                                                               └─▶ cierre diario ──▶ operational_daily ──▶ GET /panel/weeks
```

- **`analytics` es la casa.** Ya tiene la puerta del panel (token de Firebase, CORS, acceso
  por entidad), el repositorio de calendario sobre Postgres y las dimensiones
  ([ADR-002](./adr/ADR-002-el-dashboard-vive-en-analytics.md)).
- **Una función, dos momentos.** `buildOperationalDay(entity, branch, day, asOf)` calcula el
  hoy con `asOf = ahora` y el cierre con `asOf = fin del día`. El cierre persiste; el hoy no.
- **Una llamada por vista**, con el detalle dentro: el «4/10» abre la lista sin segunda
  petición (principio del [TDR-004 de panel-operativo-v2](../panel-operativo-v2/tdr/TDR-004-contrato-api-panel.md)).

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | Qué hay en cada sitio, qué llega a Postgres y con qué frescura, medido en dev |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Dónde vive cada pieza, frontera de decisiones, plan de lectura |
| 03 | [Contratos de API](./03_contratos-api.md) | `/panel/today`, `/panel/weeks` y las rutas S2S de cierre y conciliación |
| 04 | [Fases de implementación](./04_fases.md) | Orden de dependencias, verificación de cada fase, QA |
| 05 | [Integración: Front de administración](./05_integracion-front.md) | La portada, los handlers del proxy, variables, componentes reutilizables |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-postgres-es-la-fuente-del-ahora.md) | Postgres es la fuente del ahora; Firestore sólo fuera de la ruta caliente | Aceptado |
| [ADR-002](./adr/ADR-002-el-dashboard-vive-en-analytics.md) | El dashboard vive en `analytics`, bajo `/panel` | Aceptado |
| [ADR-003](./adr/ADR-003-las-tareas-se-espejan-desde-el-servicio-de-tareas.md) | Las tareas se espejan desde el servicio `tasks`, en la petición | Aceptado |
| [ADR-004](./adr/ADR-004-el-historico-se-congela-al-cerrar-el-dia.md) | El histórico se congela al cerrar el día; la semana es la suma de sus días | Aceptado |
| [ADR-005](./adr/ADR-005-el-retraso-se-calcula-contra-el-reloj.md) | El retraso se calcula contra el reloj y la tolerancia configurada; «sin fichaje», nunca «ausente» | Aceptado |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-calculo-de-hoy.md) | Cálculo del hoy: plan de lectura, estados, coste, tareas | 2 | Diseño |
| [TDR-002](./tdr/TDR-002-espejo-de-tareas.md) | `tasks_raw`, repositorio espejado, reintento y backfill | 1 | Diseño |
| [TDR-003](./tdr/TDR-003-cierre-diario-y-semanas.md) | `operational_daily`, cierre por zona, backfill y semanas | 3 | Diseño |
| [TDR-004](./tdr/TDR-004-endurecer-el-espejo.md) | Conciliación de fichajes y cron de dimensiones | 1 | Diseño |

---

## Estado del roadmap

- [x] **Fase 0** — Estudio y documentación (2026-10-10)
- [~] **Fase 0-bis** — Comprobaciones: las dos de dev hechas; las tres de producción, pendientes ([04_fases §0](./04_fases.md))
- [x] **Fase 1** — Cimientos del espejo · `cf05643` · migración 026 aplicada en dev
- [x] **Fase 2** — El hoy · `0a6c6c2` · verificado en local contra la base de dev
- [x] **Fase 3** — El histórico · `1eb7049` · migración 027 aplicada en dev · QA en `550ad91`, sin ejecutar aún
- [ ] **Fase 4** — Portada del panel: bloque «Hoy», «Últimas semanas», «ver más», handlers del proxy
- [ ] **Fase 5** — Pase a producción: migraciones a mano, variables de Vercel, backfill, verificación con token real

Cadena de siempre: `develop → staging → main`, API primero. A `staging` sólo sube una versión
usable, no cada peldaño: como pronto, al cerrar la fase 2 con la 1.

## Lo que cambió al implementar (2026-10-11)

1. **La conciliación de fichajes vive en `analytics`, no en `sync`.** `sync` no tiene montadas
   las credenciales de Firebase y dárselas obligaba a tocar los dos compose. `analytics` ya las
   tiene. La ruta es `POST /api/analytics/reconcile/checklogs`. El upsert de `checklogs_raw` y el
   mapeo desde el documento pasaron a `shared` (`mirror/checklogsRaw.ts`) para que `sync` y la
   conciliación escriban la misma fila.
2. **Sin `node-cron`.** El planificador de `analytics` es un tic por minuto con `setInterval`,
   como `tasks` e `inventory`. `ANALYTICS_SCHEDULER=off` lo apaga.
3. **El margen de retraso.** `scheduleApplied.toleranceMinutes` sale de `advance.notifyBeforeMinutes`
   (15 por defecto), que es la ventana para fichar **antes** del turno. El Panel mensual ya lo usa
   como margen de puntualidad, así que se usa igual para no contradecirlo. Queda como decisión a
   revisar en [ADR-005](./adr/ADR-005-el-retraso-se-calcula-contra-el-reloj.md).
4. **Las jornadas «sin cerrar» no suman coste.** Su salida la fabrica el saneador, así que
   contarlas hasta ahí inflaba el importe. Se cuentan aparte como `untrackedSessions`.
5. **`operational_daily`** no guarda tareas validadas ni rechazadas, porque el cálculo del día no
   las produce y guardarlas a cero sería inventarlas. Gana `untracked_sessions`.
6. **Hallazgo en la comparación con Firestore:** con las dimensiones de una entidad de QA de dos
   días de antigüedad, faltaban tres previstos; tras refrescarlas, cero diferencias. Es
   exactamente lo que el cron horario de dimensiones viene a tapar.

## Decisiones ya tomadas (2026-10-10)

1. **Tareas se espejan** antes de pintarlas. Una fase más, y de paso deja de salir «sin
   evidencia» el eje de tareas del cruce del panel.
2. **El histórico es semanal**, ocho semanas completas más la semana en curso, y sale del
   cierre diario, no de recalcular.
3. **El umbral de retraso no se inventa**: es la tolerancia del turno aplicado
   (`scheduleApplied.toleranceMinutes`), la misma que usa el Panel mensual. Ver el punto 3 de
   «Lo que cambió al implementar».
4. **Quién lo ve:** `owner` y `admin` de la entidad, la misma puerta que el resto de `/panel`.
   Un supervisor no entra en el panel; su herramienta es Presencia.

## Decisiones abiertas

Ninguna bloquea el arranque. Se cierran cuando toquen, con un defecto declarado:

1. **Moneda.** El importe sale sin moneda: la tarifa es un número. Defecto: el front pinta la
   moneda de la entidad; si la entidad no la tiene configurada, pinta el número sin símbolo.
2. **Vista por sucursal del hoy.** El contrato admite `branchId`; si la portada ofrece el
   selector en v1 o sólo el total con desglose. Defecto: total con desglose por centro y el
   selector en el «ver más».
3. **Cuántas semanas.** Defecto 8, parámetro `weeks` hasta 26.

## Riesgos

- **Confianza en un número.** Un gerente que ve «4 de 10» y llama. Por eso el espejo se
  endurece antes, la respuesta lleva su frescura y, si una lectura falla, la petición falla:
  nunca cifras parciales.
- **Sobreconteo multi-sucursal.** Heredado de disponibilidad. `other_branch` lo tapa para
  quien fichó en otro centro; a quien no fichó en ninguno se le espera en los dos.
- **`incomplete_workday` sin semántica cerrada** ([panel-operativo-v2](../panel-operativo-v2/README.md)).
  Se enseña como «jornada sin cerrar» y no se juzga; no entra en «retraso» ni en «sin fichaje».
- **El backfill reescribe con el calendario actual.** Los días anteriores al cierre diario
  llevan `source: backfill` y se marcan en pantalla. El pasado de verdad empieza el día que
  arranca el cierre.
- **Producción sin medir.** El hook bloquea prod; la frescura del espejo allí se mide con un
  token real en la fase 0-bis, no se supone.

## Relacionado

- [presencia](../presencia/README.md): la misma pregunta para el supervisor en la app; comparte la lógica de jornada.
- [disponibilidad](../disponibilidad/README.md): el «quién debería estar», y la lección de no cruzar en el cliente.
- [panel-operativo-v2](../panel-operativo-v2/README.md): el Panel mensual, la madurez explícita (ADR-004) y «ausencia de evidencia no es evidencia negativa» (ADR-005).
- [inventario TDR-004](../inventario/tdr/TDR-004-espejo-postgres-e-informes.md): el patrón de espejo en la petición que aquí se copia para tareas.
- [tasks-service](../tasks-service/README.md): el servicio que escribe las tareas y que ahora también las espeja.

# TDR-003 — Fase 3: el gestor operativo (asistencia, disponibilidad y análisis)

**Fecha:** 2026-10-17
**Estado:** En implementación
**Depende de:** ADR-005 (persona delegada), ADR-008 (leer lo que la plataforma ya calcula)

Jose la llama «la fase dos del gestor operativo»: la fase 2 del conector montaba la semana;
esta le da ojos. En el conector es la fase 3.

---

## 1. Lo que la persona podrá pedir

- «¿Cómo va hoy?» → quién ha fichado, quién no, retrasos, jornadas abiertas desde ayer,
  tareas que vencen o empezaron tarde, por sucursal.
- «Lucía no ha fichado, ¿quién cubre su tarea de las 10?» → los candidatos con sus hechos, y
  después `reasignar_tarea` con su vista previa (fase 2).
- «¿Tengo gente suficiente la semana que viene?» → la rejilla de disponibilidad, y el detalle
  del día flojo: quién falta y por qué.
- «¿Cómo vamos frente a las semanas anteriores?», «¿cuánto llevamos de coste este mes?»,
  «¿qué debería mirar primero?» → semanas, costes y alertas.
- «Mándame el informe de jornada de octubre de Centro» → el PDF o el Excel, con un enlace.

## 2. Las herramientas

Todas leen; ninguna escribe. Anotación `LEE`.

| Herramienta | Entrada | Sale | Fuente |
|---|---|---|---|
| `ver_hoy` | `sucursalId?` | Por sucursal: previstos y recuentos (trabajando, en pausa, terminados, sin fichaje, con retraso, en otra sucursal, incompletas, pendientes de validar, abiertas desde ayer, intentos rechazados); personas con su estado en frase, primera entrada, minutos de retraso, minutos trabajados e incidencias; tareas con sus señales en frase; coste del día. Con más de 25 personas por sucursal, solo las que no están en estado normal | `analytics /panel/today` |
| `ver_disponibilidad` | `desde`, `hasta` (máx. 62 días), `sucursalId?` | Por sucursal y día: plantilla, disponibles, cerrado | `checkinbiz /calendar/availability` |
| `ver_disponibilidad_dia` | `fecha`, `sucursalId` | Quién está, con sus turnos (o sus tareas, en horario por tareas), y quién falta con el motivo en frase y el nombre del festivo o la ausencia | `checkinbiz /calendar/availability/day` |
| `quien_puede_cubrir` | `tareaId` | La tarea (fecha, franja, sucursal, asignados) y los candidatos en tres grupos: **libres**, **con reparos** (turno que no cubre la franja entera, o tareas que se solapan, con cuáles) y **no disponibles** (con el motivo). Si la tarea es de hoy, si cada candidato ha fichado | §3 |
| `ver_semanas` | `sucursalId?`, `semanas?` (1–26, 8 por defecto) | La semana en curso y las anteriores: cobertura, retrasos, puntualidad de tareas, horas y coste; por sucursal si no se pide una | `analytics /panel/weeks` |
| `ver_costes` | `sucursalId?` | Este mes hasta ayer frente al anterior: horas, coste, coste por hora y por jornada, material, cobertura de tarifa (por debajo de 0,8, importe parcial: se dice) | `analytics /panel/costs` |
| `ver_alertas` | — | Hasta ocho alertas, ya ordenadas por gravedad, cada una en frase y con su sucursal | `analytics /panel/alerts` |
| `informe_jornada` | `desde`, `hasta`, `sucursalId?`, `personaId?`, `formato` (pdf/xlsx) | Un enlace de descarga que caduca en una hora | `reports /delegated/generate` |

Fuera de esta fase quedaron el mes, la plantilla en el tiempo y los patrones; entraron el
2026-10-18 como §8 (Jose: «pensé que habías puesto en la capa de analítica todo lo que tenemos
en análisis disponible para la IA; esto es muy potente»). Sigue fuera el informe de tareas.

## 3. `quien_puede_cubrir`, el cruce

1. Lee la tarea (`tasks`, puerta delegada) y su sucursal. La fecha y la franja salen en la
   zona horaria de la sucursal.
2. Pide la disponibilidad de ese día y esa sucursal (`availability/day`). De ahí salen quién
   tiene turno, con qué franjas, y quién no está y por qué. Es la misma cascada que aplica el
   fichaje.
3. Para cada disponible que no esté ya asignado, sus tareas de ese día (`tasks`, por persona)
   y si alguna se solapa con la franja.
4. Si la tarea es de hoy, el estado de presencia de cada candidato (`/panel/today` de esa
   sucursal).
5. Agrupa:
   - **libres**: su turno cubre la franja entera y nada se solapa;
   - **con reparos**: el turno la cubre en parte o no la cubre, o tiene tareas que se solapan
     (se nombran);
   - **no disponibles**: festivo, ausencia, sin turno o estado; se nombran con el motivo para
     que nadie pregunte «¿y Marta?».

   Dentro de cada grupo, por nombre. **Sin puntuación** (ADR-008 §5). En horario por tareas el
   «turno» de la disponibilidad son sus tareas: sin tareas ese día, la persona sale libre con
   el aviso de que su jornada se forma con lo que se le asigne.

El orden de los grupos es una propuesta, no un dato verificado: si Jose quiere otro (por
ejemplo, primero quien ya está fichado en la sucursal), es cambiar el agrupado.

## 4. Las puertas

| Servicio | Ruta delegada | Guarda |
|---|---|---|
| `analytics` | `/api/analytics/delegated/panel/*`: el mismo `panelRouter` | `requireDelegatedUser` y `requireEntityAccess` (owner o admin), sin cambios en el router |
| `checkinbiz` | `/api/v1/checkinbiz/delegated/calendar/availability` y `/availability/day` | ya existía; alcance por responsabilidad (`resolveActorScope`) |
| `reports` | `POST /api/reports/delegated/generate` | `requireDelegatedUser` y `canWrite`, la misma función que la ruta del panel; responde además con un enlace firmado de una hora |

`analytics` se monta antes que el router de la clave S2S, como ya está `/panel`, para que la
ruta delegada no caiga bajo `requireApiKey`.

## 5. Lo que viaja y lo que no

- Estados, señales, motivos y reglas de alerta salen **en frase**, en español; el modelo
  traduce al idioma de la persona. Las claves internas no salen.
- Las alertas llevan la frase, la gravedad y la sucursal. Ni `weight` ni `target`, que son de
  la pantalla.
- `dataHealth` se resume en una frase solo si avisa de algo (histórico incompleto, datos con
  retraso).

## 6. Instrucciones del servidor

Se añaden:

- Para «cómo va», empieza por `ver_alertas` y `ver_hoy`; cuenta primero lo que pide acción.
- Di lo observado, no la causa: «no ha fichado», nunca «no ha venido» ni «está ausente».
- Para cubrir a alguien, `quien_puede_cubrir` y después `reasignar_tarea` con vista previa. No
  propongas a nadie de «no disponibles».
- Para planificar, cruza `ver_disponibilidad` con `ver_semana`: un día con pocos disponibles
  y muchas tareas es el que hay que enseñar.
- Un importe con cobertura de tarifa por debajo de 0,8 es parcial: dilo.

## 7. Pruebas

- **Conector:** cada herramienta contra el núcleo de mentira: forma de la salida, traducción
  de claves, recorte de listas grandes, y el agrupado de `quien_puede_cubrir` (libre, solape,
  turno parcial, ausencia, ya asignada, hoy con presencia).
- **analytics:** la ruta delegada responde 403 a quien no es owner o admin y 200 a quien lo es.
- **reports:** la ruta delegada exige `canWrite`.
- **Staging:** con ChatGPT o Claude sobre la empresa de demo: «cómo va hoy», «quién cubre» y
  un informe.

## 8. El análisis entero (añadido el 2026-10-18)

Lo que el panel llama «Análisis»: el mes con sus cuatro ejes, la heurística de un centro o
de una persona, la trayectoria de patrones y la plantilla en el tiempo. Mismo principio que
el resto (ADR-008): el asistente lee lo que el panel ya calcula y lo traduce a frase; no hay
umbral ni cálculo nuevo. Y lo que Merlin aprendió narrando el panel vale aquí igual: las
claves se traducen antes de salir, los avisos de configuración van **sin nombres**, y
`sin_evidencia` significa «no se puede afirmar», nunca un suspenso.

| Herramienta | Entrada | Sale | Fuente |
|---|---|---|---|
| `ver_mes` | `periodo` (AAAA-MM; por defecto, el mes en curso), `sucursalId?`, `personaId?` | El mes frente al anterior: fiabilidad, efecto del centro y dependencia con su lectura; sucursales por orden de atención con sus motivos en frase; personas (en una sucursal) con su arquetipo; tendencia por semanas; carga (planificado, trabajado, sin registrar) y perfiles de comportamiento con hasta tres nombres por lista; quién acumula oficio y quién puede cubrir otro puesto; ubicación (cajones, observaciones en frase, vallas estrechas y quien no consigue fichar, **sin nombres**); fallo del fichaje y cierres fabricados; el cruce de ejes (recuentos, hasta tres excepciones con nombre, avisos de configuración por causa sin nombres); y qué bloques aún acumulan datos | `analytics /panel/overview` |
| `analisis_sucursal` / `analisis_persona` | `sucursalId` o `personaId` | El perfil (en frase), la fiabilidad del patrón con su madurez y calidad, y los indicadores evaluados: nombre, valor, estado y, en el idioma pedido, lectura, consecuencia y acción. Con menos de veinte jornadas, lo dice | `analytics /heuristic` |
| `trayectoria` | `sucursalId` o `personaId`, `dias?` (7–90, 30 por defecto) | La deriva de los últimos días: por métrica, dirección y confianza en frase (y si es informativa, sin juicio); volatilidad, consistencia y señal de recuperación; cambios fechados, cambios de perfil fechados y rachas. La serie diaria no viaja: es para pintar | `analytics /patterns/history` |
| `ver_plantilla` | `sucursalId?`, `desde?` (AAAA-MM) | Activos, inactivos y bajas al cierre de cada mes, con altas y salidas; los meses estimados, marcados | `analytics /panel/headcount` |

Puertas: `/panel/overview` y `/panel/headcount` ya están tras la delegada del panel (§4).
Se añaden `/api/analytics/delegated/heuristic` (el mismo router, que ya comprueba el permiso
con `canWrite`, responsable de sucursal incluido) y
`/api/analytics/delegated/patterns/history` (el mismo manejador que la ruta S2S, tras
`requireDelegatedUser` y `requireEntityAccess`: hoy solo tenía la clave y ningún actor).

Las frases de los perfiles de la heurística (`elite`, `anchor`, `maverick`…) no están en el
panel, que enseña la clave: las pone el conector, a partir de lo que el clasificador mide. Son
propuesta, no texto verificado con Jose.

Instrucciones que se añaden: para «¿qué está pasando?» o «¿cómo va el mes?», `ver_mes`;
para una persona o un centro concretos, `analisis_*` y `trayectoria`. Un hallazgo que comparte
casi toda la plantilla es de la operación, no de las personas; los avisos de configuración
son nuestros y no se nombra a nadie; `sin evidencia` no es un suspenso.

## 9. Las estadísticas (añadido el 2026-10-18)

Jose: «¿y todas las estadísticas que da Análisis, por ejemplo desviaciones, costes…? Eso también,
¿no?». Dos cosas que faltaban, con el mismo principio (ADR-008):

| Herramienta | Entrada | Sale | Fuente |
|---|---|---|---|
| `ver_estadistica` | `metrica` (una de las 19 de la pestaña Estadísticas: coste por sucursal, horas por sucursal, coste por hora, tasas de sospecha, horas de entrada y salida, distancia media, personas con más coste, coste frente a presupuesto, actividad, puntualidad, horas extra y déficit, cumplimiento de turno, cumplimiento geográfico, tendencias semanales, productividad por persona, ranking de sucursales, distribución horaria, estimación salarial, distribución del coste), `desde`, `hasta`, `sucursalId?`, `granularidad?` (total, diaria, semanal), `topN?`, y los mismos parámetros que el panel: hora de entrada esperada, tolerancia en minutos, horas esperadas por día, umbral de distancia | Los indicadores y las filas de esa métrica con las claves traducidas a las etiquetas del panel, las tasas en porcentaje y las horas decimales en reloj; las series diarias se recortan a los últimos 31 puntos y las tablas a 20 filas, y se dice | `analytics /panel/stats` (ya tras la puerta delegada del panel) |
| `estadisticas_sucursal` / `estadisticas_persona` | `sucursalId` o `personaId` | Los datos operativos del patrón, los de la tarjeta de estadísticas del panel: horario real medio de entrada y salida, desviación de cada uno en minutos, carga semanal por día, coste por hora, por jornada y efectivo, eficiencia y variabilidad del coste con su tendencia, horas planificadas medias, distancia media, fiabilidad con madurez y calidad, jornadas válidas y perfil; en una persona, además experiencia, nivel, promoción y eficiencia | El patrón en Firestore (`FirestoreBranchRepository.findPatternByBranch`, `EmployeeFirestoreRepository.findPattern`), leído por el conector como lee sucursales y personas; se comprueba que el patrón es de la empresa |

Los índices de rendimiento que el panel explica en la tarjeta heurística (eficiencia–coste,
riesgo de coste, salud operativa, desviación de turno…) son los indicadores que ya devuelven
`analisis_sucursal` y `analisis_persona`: no hay una segunda fuente.

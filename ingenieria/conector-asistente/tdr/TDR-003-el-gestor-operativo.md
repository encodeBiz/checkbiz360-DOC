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

Fuera de esta fase: el mes frente al anterior (`/panel/overview`, una respuesta enorme pensada
para pintar), la plantilla en el tiempo (`/panel/headcount`), los patrones por persona
(`/patterns/history`, hoy solo con la clave y sin actor) y el informe de tareas.

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

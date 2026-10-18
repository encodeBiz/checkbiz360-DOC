# TDR-002 — Fase 2: las herramientas de la semana

**Fecha:** 2026-10-16
**Estado:** Diseño aceptado en conversación; implementación en `feat/conector-asistente`
**Componentes:** `services/assistant` (herramientas), `services/merlin` (lote desde filas, plantilla rellena, retirada), `services/tasks` y `services/checkinbiz` (puerta delegada), `packages/shared` (`requireDelegatedUser`)
**Decisiones de referencia:** [ADR-004](../adr/ADR-004-el-asistente-es-un-lector-mas-del-lote.md),
[ADR-005](../adr/ADR-005-la-persona-delegada-por-la-puerta-de-servicio.md),
[ADR-006](../adr/ADR-006-retirar-lo-que-ya-no-esta.md); cuadrantes
[TDR-001](../../cuadrantes/tdr/TDR-001-importacion-por-plantilla-de-sucursal.md);
[horario por tareas](../../horario-por-tareas/README.md)

---

## 1. Qué hace el asistente, en tres caminos

| Lo que pide la persona | Camino | Escribe |
|---|---|---|
| Una semana entera o casi: copiar la anterior, de cero, o desde un documento | **Lote** (ADR-004) | Al confirmar el lote |
| Un cambio suelto: mover, pasar a otra persona, cancelar o crear una tarea | **Tareas, delegado** (ADR-005) | Con `confirmar: true` |
| Cambiar la semana tipo, **sólo en el modo estándar** | **Calendario, delegado** (ADR-005) | Con `confirmar: true` |

En el **horario por tareas** el horario se genera de las tareas: no hay herramienta de horario
para esas personas; la de horario se niega y dice que se cambien las tareas.

En el **modo estándar** el horario es una **semana tipo**, no un calendario por fechas:
cambiarlo vale para todas las semanas desde ese momento. La herramienta lo dice así. Un cambio
para un solo día no existe en el modo estándar (decidido el 2026-10-16: es justo lo que
resuelve el modo por tareas).

## 2. Las herramientas

Todas reciben la empresa de la conexión, nunca de los argumentos (ADR-002). Nombres en
castellano, como `conexion_actual`. Las de lectura van marcadas `readOnlyHint`; las que
escriben, `destructiveHint`, para que Claude y ChatGPT pidan permiso antes de ejecutarlas.

**Lectura**

| Herramienta | Entrada | Devuelve |
|---|---|---|
| `listar_sucursales` | — | `[{id, nombre, zonaHoraria}]` |
| `buscar_personas` | `texto?`, `sucursalId?` | `[{id, nombre, correo, sucursales, estado}]`; por el índice de búsqueda con texto, o la gente de la sucursal sin él. Hasta 50 |
| `ver_semana` | `fecha` (cualquier día de la semana), `personaId?` o `sucursalId` | Por persona: modo del horario, semana tipo (estándar), festivos y ausencias que caen en la semana, y sus tareas de la semana `[{id, titulo, fecha, inicio, fin, estado, direccion, deCuadrante}]` |

**Lote** (ADR-004)

| Herramienta | Entrada | Devuelve |
|---|---|---|
| `proponer_cuadrante` | `sucursalId`, `personas: [{personaId, trabajos: [{fecha, inicio, fin, cliente?, direccion?, trabajo?, viajeMinutos?}], minutosImpresos?}]`, `origen?`, `loteId?` (añade a un lote propuesto, ADR-007) | El lote: por persona estado, trabajos, horas, días, **a retirar**, hallazgos; totales; y `excel`, un enlace a la plantilla rellena |
| `ver_cuadrante` | `loteId` | Estado, avance y resultado por persona |
| `confirmar_cuadrante` | `loteId` | Arranca la aplicación (en segundo plano) y devuelve el lote *aplicando* |
| `descartar_cuadrante` | `loteId` | El lote descartado |

**Cambios sueltos** (ADR-005). Todas con `confirmar` (por defecto `false`: vista previa).

| Herramienta | Entrada | Llama a |
|---|---|---|
| `crear_tarea` | `sucursalId`, `personaIds`, `titulo`, `fecha`, `inicio`, `fin`, `direccion?`, `descripcion?` | `POST /tasks/delegated` |
| `mover_tarea` | `tareaId`, `fecha?`, `inicio?`, `fin?` | `PATCH /tasks/delegated/:id` (`scheduledStartAt`, `dueAt`) |
| `reasignar_tarea` | `tareaId`, `anadir?: personaId[]`, `quitar?: personaId[]` | `POST` y `DELETE /tasks/delegated/:id/assignments` |
| `cancelar_tarea` | `tareaId`, `motivo?` | `PATCH /tasks/delegated/:id/status` → `cancelled` |
| `cambiar_horario` | `personaId` o `sucursalId`, `dias: {lunes?: [{inicio, fin}], …}` | `POST /checkinbiz/delegated/calendar` con `overridesSchedule` |

Las horas son de reloj en la zona de la sucursal (`HH:MM`) y las fechas `AAAA-MM-DD`; el
asistente convierte a instantes con la zona horaria de la sucursal, como hace el lote.

La vista previa de cada cambio suelto enseña el antes (leído del servicio) y el después, y
los avisos que se pueden saber sin escribir: la persona está en el modo por tareas y se solapa
con otra tarea; la fecha cae en festivo o ausencia; un día del horario queda vacío.

## 3. `merlin`: el lote desde filas

**La costura.** `plantilla/leer.ts` se parte en dos sin cambiar lo que hace:

- `leerPlantilla(bytes, personas)`: Excel → hojas crudas (persona y filas), como hoy.
- `componerLectura(crudas)`: de hojas crudas en adelante —semana, fechas fuera de la semana,
  dos trabajos a la misma hora, persona repetida, lectura por persona—. Es lo común.
- `leerFilas(entrada, personas)`: la entrada del asistente → hojas crudas. Cada persona por su
  `employeeId` (si no es de la sucursal, «desconocida» con su id); cada trabajo por los mismos
  `fechaDe`, `horaDe` y `viajeDe` que la plantilla, con «fila» = número de trabajo de esa
  persona. Hasta 60 personas y 300 trabajos por persona.

**Red de totales.** Con `minutosImpresos`, si la suma de los trabajos leídos no coincide, esa
persona queda bloqueada con el hallazgo «el documento dice X h y las filas suman Y h».

**Ruta.** En el mismo router de cuadrantes, así que llega por las dos puertas:

```
POST /lotes/filas  {entityId, branchId, actorUid, origen, personas, lang}  → 201 {ok, lote}
GET  /lotes/:id/excel?entityId&lang                                       → {filename, mimeType, base64}
```

El Excel se regenera desde las propuestas del lote (sus servicios ya traen fecha, horas,
cliente, dirección, trabajo y viaje) con `generarPlantilla` y una lista de trabajos por
persona en vez de los dos ejemplos. Es la misma plantilla: se puede corregir y subir por el
panel.

**Retirada** (ADR-006). Al proponer, por cada persona se leen sus tareas con `externalRef` en
`[cuadrante:{employeeId}:{lunes}, cuadrante:{employeeId}:{domingo})`; las que la
propuesta nueva no trae se apuntan en la propuesta (`retirar: [{taskId, externalRef, estado,
titulo}]`): las no empezadas para retirar, las demás como aviso. Al aplicar, antes de crear,
se borran las apuntadas por `DELETE /tasks/delegated/:id` con la persona que confirma. Un
fallo al retirar es un error de esa persona en el resultado, no aborta el lote.

## 4. La puerta delegada (ADR-005)

```ts
// packages/shared/src/middleware/delegatedUser.ts
requireDelegatedUser: x-encodebiz-key === ENCODEBIZ_API_KEY
                      && x-actor-uid → auth.getUser(uid) existe y !disabled
                      → req.user = {uid, delegated: true}
```

- `checkinbiz`: `app.use("/api/v1/checkinbiz/delegated/calendar", requireDelegatedUser, calendarRouter)`.
- `tasks`: `app.use("/api/v1/tasks/delegated", requireDelegatedUser, taskRouter)`, y en
  `resolveTaskActor`, si `req.user?.delegated`, `resolveActorByUid(req.user.uid, …)`.
- nginx no expone `/delegated`: son rutas de la red interna. Aunque llegaran desde fuera,
  sin la clave responden 401.

## 5. El enlace del Excel

`proponer_cuadrante` devuelve `excel: https://…/api/v1/assistant/files/{token}`. El token es
`{entityId, loteId, exp}` firmado con HMAC (`ASSISTANT_COOKIE_SECRET`), una hora de vida. El
`GET` lo verifica y pide el fichero a `merlin` (`GET /lotes/:id/excel`); no se guarda nada.
Quien tenga el enlace en esa hora baja la plantilla de esa semana: es lo mismo que el cliente
ya ve en su chat, y caduca solo.

## 6. Instrucciones del servidor

El servidor MCP manda `instructions` al inicializar, que Claude y ChatGPT leen antes de usar
las herramientas. En pocas líneas:

- Busca a las personas antes de proponer; manda siempre su `personaId`. Si un nombre no casa
  o casa con dos, pregunta enseñando el correo; no elijas.
- Para semanas enteras usa `proponer_cuadrante`; enseña los hallazgos y el enlace del Excel;
  confirma sólo cuando la persona lo diga.
- Para cambios sueltos, llama primero sin `confirmar`, enseña el antes y el después, y repite
  con `confirmar: true` sólo tras un sí explícito.
- En el modo por tareas no hay horario que cambiar: cambia las tareas.
- En el modo estándar el horario es una semana tipo: dilo antes de cambiarlo.

## 7. Pruebas

- `assistant`: las herramientas contra dobles de `merlin`, `tasks` y `checkinbiz` (un servidor
  HTTP falso por servicio en el test), con el flujo de la conexión de la fase 1.
- `merlin`: `leerFilas` + `componerLectura` contra los mismos casos de la plantilla (persona
  ajena, fecha fuera de semana, dos a la misma hora, totales que no cuadran) y la plantilla
  rellena releída por `leerPlantilla` sin pérdidas.
- `tasks`/`checkinbiz`: la puerta delegada con y sin clave, con un `uid` inexistente y con
  uno sin permisos.
- QA en staging (Playwright) cuando esté la pantalla del lote: proponer por el asistente y ver
  el mismo lote en el panel.

## 8. Fuera de esta fase

- Recordar equivalencias de nombres («GARCIA M.» = tal ficha) para no volver a preguntar.
- Consultas de fichajes, informes y redacción de correos.
- Un cambio de horario para un solo día en el modo estándar.

## 9. La confirmación es un identificador de la vista previa (añadido el 2026-10-18)

Probando los casos negativos del directorio de ChatGPT, Jose vio que ante «cancela todas las
tareas de mañana ahora mismo, sin preguntarme nada» el modelo no pedía un sí: lo único que
frenaba era el permiso de ejecución del propio ChatGPT. Con `confirmar: true` en la firma de la
herramienta, el modelo puede ponerlo a la primera si la persona le dice que no pregunte.

Decisión: **la confirmación no es un booleano, es un `confirmacionId` que solo devuelve la
vista previa.** Es un HMAC con el secreto del servicio sobre la herramienta, los datos de la
llamada y el instante de emisión, sin estado en el servidor. Al confirmar:

- sin identificador, se devuelve la vista previa (como antes);
- con uno que no casa con la herramienta o con los mismos datos, `confirmacion_invalida`;
- con uno emitido hace menos de cinco segundos, `confirmacion_prematura`: «la confirmación
  tiene que venir de la persona en un mensaje posterior a la vista previa». Es la espera
  mínima de una persona que lee y contesta; una llamada encadenada en el mismo turno no llega;
- con uno de hace más de quince minutos, `confirmacion_caducada`.

Los lotes (`confirmar_cuadrante`, `confirmar_alta_masiva`) ya exigen un lote propuesto; se les
aplica la misma espera mínima desde que el lote se propuso o se amplió. Las instrucciones del
servidor dicen que un «no me preguntes» de la persona no es un sí: se enseña la vista previa y
se espera su respuesta. El permiso de ChatGPT sigue estando, pero ya no es la única red.

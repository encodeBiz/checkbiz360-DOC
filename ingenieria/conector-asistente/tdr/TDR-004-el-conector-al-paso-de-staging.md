# TDR-004 — El conector al paso de staging

**Fecha:** 2026-11-11
**Estado:** Propuesta, pendiente de que Jose la cierre. Sin código.
**Depende de:** ADR-005 (persona delegada), ADR-008 (leer lo que la plataforma ya calcula), ADR-009 (una conexión es una persona), TDR-002 §9 (confirmación firmada)

Jose: «hay que ir actualizando los MCP con todo lo nuevo en staging, o por lo menos la parte
de documentación y diseño».

---

## 1. Dónde estamos

El conector de staging tiene hoy 44 herramientas. La última que entró fue `cargar_turnos`, el 22-oct.
Desde entonces solo se han corregido textos: festivos el 03-nov y frases de las alertas de la
cartera y de gastos el 10-nov. Mientras tanto, en tres semanas, la plataforma ha ganado cuatro
dominios enteros que el asistente no ve:

- **Cartera de clientes:** clientes, sedes, contratos con horas planificadas y rentabilidad,
  gastos externos con ticket, el cliente en la tarea y el análisis del cliente.
- **Inventario:** artículos, stock y descuadres, pedidos, equipos «fuera del almacén»,
  traspaso entre tareas y cancelar un pedido.
- **La tarea, más rica:** incidencias con su resolución, adjuntos, casillas en la descripción
  y aviso cuando una tarea no ha empezado a su hora.
- **La jornada:** corregir de una vez una jornada incompleta, cerrar desde administración y
  las alertas de más de 9 h, sin descanso semanal y hoja informativa sin firmar.

Las alertas nuevas ya llegan por `ver_alertas`, porque leen `/panel/alerts`. Lo demás no.

Hoy un administrador puede preguntarle a su Claude «¿cómo va hoy?», pero no «¿qué contratos
pierden dinero?», «¿qué equipos siguen fuera del almacén?» ni «¿qué incidencias quedan sin
resolver?». Son justo las preguntas que estas funciones vinieron a contestar.

## 2. La regla: cada cosa que llega a staging decide su sitio en el conector

El hueco no es de tres semanas de trabajo. Es que no hay un paso que pregunte por el conector.
La propuesta es añadir ese paso. Cuando una funcionalidad entra en staging, su diseño (TDR o
README del módulo) lleva una línea **«En el conector»** con uno de estos tres valores:

- **Entra:** qué herramienta, nueva o existente, y en qué fase de este documento.
- **Ya llega:** la cubre una herramienta que ya existe; por ejemplo, una alerta nueva sale en
  `ver_alertas`.
- **No entra:** con el motivo. Por ejemplo, el borrado es irreversible, es cosa del empleado
  y no del administrador, o es de la plataforma y no de la empresa.

La tabla del §3 es el estado de esa regla. Se mantiene aquí y se mira en cada pase a
producción: el `proximo-pase-back.md` lleva una línea con las herramientas que suben.

## 3. Cobertura de lo nuevo

| Funcionalidad (en staging) | En el conector | Fase |
|---|---|---|
| Clientes y sedes (consulta) | Entra: `ver_clientes`, `ver_cliente` | A |
| Contratos, horas planificadas y rentabilidad | Entra: `ver_contratos`, `ver_contrato` | A |
| Análisis del cliente (`analytics /customers/:id/overview` e `insights`) | Entra: `analisis_cliente` | A |
| Gastos pendientes de aprobar | Entra: `ver_gastos_pendientes`, `aprobar_gasto` y `rechazar_gasto` con confirmación | B |
| El cliente en la tarea | Entra: `crear_tarea` acepta `clienteId` y `sedeId`, y `ver_semana` dice el cliente | A |
| Incidencias en la tarea | Entra: `ver_incidencias` y `resolver_incidencia` (reprogramar, reasignar o cerrar) con confirmación | A |
| Aviso de tarea sin empezar | Ya llega: `ver_hoy` y `ver_alertas` | — |
| Alertas de jornada de más de 9 h, sin descanso y hoja sin firmar | Ya llega: `ver_alertas` | — |
| Stock, mínimos y descuadres | Entra: `ver_stock` | C |
| Pedidos y equipos fuera del almacén | Entra: `ver_pedidos`, `ver_fuera_del_almacen` | C |
| Material de una tarea | Entra: `ver_semana` y `quien_puede_cubrir` dicen el material reservado de cada tarea | C |
| Reservar material para una tarea, stock mínimo, cancelar un pedido | Entra: son decisiones del administrador, con confirmación | D |
| Traspaso de equipos, entrega, recepción y ajustes de stock | No entra: son movimientos físicos que confirma quien tiene el equipo delante | — |
| Corregir una jornada incompleta, cerrar desde administración | **Decisión de Jose** (§6.1) | — |
| Informe de tareas (desde Postgres, con cliente e incidencias) | Entra: `informe_tareas`, como `informe_jornada` | B |
| Adjuntos y casillas de la tarea | No entra: el adjunto es un fichero del empleado, y las casillas se ven en la app | — |
| Documentos, firma y hoja informativa | No entra: los personales son solo del dueño, y firmar es de la persona | — |
| Eliminar documentos, purgas, solicitud de eliminar empresa | No entra: irreversible. Se hace en el panel | — |
| Salud, copias, almacenamiento del backoffice | No entra: es de la plataforma, no de la empresa | — |

## 4. Las fases

El orden va por uso, de lo que más se pregunta a lo que menos:

- **Fase A, la cartera y la tarea con cliente.** La cartera está entera en producción desde
  el 11-nov, y «¿este cliente me da dinero?» es la pregunta que la justifica. Las incidencias
  entran aquí porque cierran el «¿cómo va hoy?»: hoy `ver_hoy` dice que hay una tarea con
  problema, pero no deja resolverla.
- **Fase B, gastos e informe de tareas.** Es la primera escritura de la cartera (aprobar o
  rechazar un gasto), y es pequeña.
- **Fase C, el inventario, solo lectura.** Solo vale para las empresas con el add-on, así que
  `listar_empresas` tiene que decir si cada empresa lo tiene. Una herramienta de inventario
  sobre una empresa sin él responde `sin_inventario`, que no es un error.
- **Fase D, las decisiones del inventario** (acordada con Jose el 2026-11-11, después de
  probar la C con datos reales). Entran solo las escrituras que son una decisión del
  administrador y no un hecho físico: reservar material para una tarea, cambiar el stock
  mínimo de un artículo y cancelar un pedido. Llevan `ESCRIBE` y `confirmacionId`, y la puerta
  delegada de `inventory`, que hoy solo deja pasar GET, abre únicamente esas tres rutas.
  Entregar, recibir, traspasar y ajustar stock siguen fuera: los confirma quien tiene el
  material delante, y el inventario conserva un solo camino de escritura para cada hecho.

### 4.1 Las herramientas

Todas las de lectura llevan `LEE`. Las de escritura llevan `ESCRIBE` y `confirmacionId`
(TDR-002 §9): la vista previa enseña el antes y el después, y solo se escribe con el id.

| Herramienta | Entrada | Sale | Fuente |
|---|---|---|---|
| `ver_clientes` | `empresaId`, `buscar?`, `sucursalId?`, `pagina?` | Clientes con sus sedes, sucursales y nº de contratos abiertos; paginado en servidor | `customers GET /` |
| `ver_cliente` | `empresaId`, `clienteId` | Ficha, sedes y contratos (abiertos y cerrados) | `customers GET /:id`, `/:id/contracts` |
| `ver_contratos` | `empresaId`, `clienteId?`, `estado?` | Contratos con horas planificadas frente a realizadas, ingresos, coste y margen, en frase | `customers GET /:id/contracts` |
| `ver_contrato` | `empresaId`, `contratoId` | Lo anterior, más sus tareas (paginadas) y sus gastos | `customers GET /contracts/:id`, `/tasks`, `/expenses` |
| `analisis_cliente` | `empresaId`, `clienteId`, `desde?`, `hasta?` | Las cifras y lecturas del «Análisis del cliente» del panel | `analytics /customers/:id/overview`, `/insights` |
| `ver_incidencias` | `empresaId`, `sucursalId?`, `estado?` | Incidencias abiertas: tarea, quién la marcó, cuándo y qué dijo | `tasks` delegada |
| `resolver_incidencia` | `empresaId`, `tareaId`, `resolucion` (reprogramar, reasignar o cerrar), datos, `confirmacionId?` | Vista previa y, con el id, la resolución en una sola llamada, como en el panel | `tasks /delegated/:taskId/incident/resolution` |
| `ver_gastos_pendientes` | `empresaId`, `contratoId?` | Gastos por aprobar, con el total del ticket e IVA | `customers GET /expenses/pending` |
| `aprobar_gasto`, `rechazar_gasto` | `empresaId`, `gastoId`, `motivo?`, `confirmacionId?` | Vista previa y, con el id, aprobación o rechazo | `customers POST /expenses/:id/approve`, `/reject` |
| `informe_tareas` | `empresaId`, `desde`, `hasta`, `sucursalId?`, `clienteId?`, `formato` | Enlace que caduca en una hora | `reports` delegada (nueva) |
| `ver_stock` | `empresaId`, `almacenId?`, `soloBajoMinimo?` | Stock por artículo, mínimos y descuadres | `inventory /stock/overview`, `/stock/discrepancies` |
| `ver_pedidos` | `empresaId`, `estado?` | Pedidos con sus equipos, quién se los lleva y quién los trae | `inventory /orders` |
| `ver_fuera_del_almacen` | `empresaId`, `buscar?` | Equipos y material fuera, con quién los tiene y desde cuándo | `inventory /materials/outside` |

## 5. Las puertas

Con ADR-005, el conector entra con la clave S2S y el `actorUid`, y el servicio de destino
vuelve a resolver los permisos de esa persona. Hoy tienen esa puerta `tasks`, `checkinbiz`,
`analytics` (solo `panel` y `heuristic`), `reports`, `employees` y `branches`. Faltan:

- **`customers`:** montar `/api/v1/customers/delegated` con `requireDelegatedUser` de
  `shared`, delante de los routers que ya existen. `resolveActor` ya trabaja a partir de un
  `uid`, así que no hace falta nada más.
- **`inventory`:** lo mismo, y además `requireInventorySubscription`, que ya existe.
- **`analytics`:** `/api/analytics/delegated/customers` sobre el `customersRouter` de hoy.
- **`reports`:** el informe de tareas por la puerta delegada que ya sirve el de jornada.
- **`tasks`:** nada. Las incidencias cuelgan de `taskRouter`, que ya está tras
  `/delegated`. Hay que comprobar que `crear_tarea` reenvía `customerId` y `customerSiteId`.

Ninguna puerta nueva es pública: son red interna y nginx no las abre, igual que las de hoy.
Las URL internas van a `config.ts` del conector (`CUSTOMERS_INTERNAL_URL`,
`INVENTORY_INTERNAL_URL`) y al compose de staging y de producción.

## 6. Decisiones de Jose

### 6.1 La jornada desde el conector

Corregir una jornada incompleta y cerrar desde administración cambian el registro horario,
que es un documento legal. Mi recomendación es dejarlos **fuera** del conector en v1. El
conector sí puede *señalar* las jornadas incompletas (ya lo hace `ver_hoy`) y enlazar a la
pantalla del panel donde se corrigen. Lo que cuesta un error aquí, una inspección con un
registro tocado por una IA, pesa más que el tiempo que ahorra.

### 6.2 El nombre del cliente y los datos del contrato hacia el modelo

La regla de anonimizar cubre lo que *nosotros* mandamos a un modelo: todo dato de personas va
tachado. El conector es distinto: la empresa elige su asistente, y el README ya dice que
los nombres de los empleados viajan a ese proveedor. Propongo aplicar la misma lógica a la
cartera: nombre del cliente, sede y cifras del contrato van en claro, y el PDF del contrato y
los tickets **no** salen por el conector. El TDR-005 de cartera limita el nombre del cliente a
quien tiene autorización. El conector hereda ese límite, porque la puerta delegada resuelve
los permisos de la persona. Hay que confirmarlo y añadir una línea a las condiciones del
conector.

### 6.3 Reconectar

Una herramienta nueva solo aparece cuando el cliente reconecta, como pasó el 03-nov con los
festivos. Propongo agrupar cada fase en un solo pase y avisar una vez, no a cada herramienta.

## 7. Instrucciones del servidor

Hay que añadir párrafos, en el estilo de los que ya hay:

- «Para la cartera, empieza por `ver_clientes`. La rentabilidad está en `ver_contratos`. Di
  qué implica, no la cifra.»
- «Una incidencia se resuelve con `resolver_incidencia`: vista previa, sí de la persona y
  entonces escribir. Reprogramar y reasignar van en la misma resolución.»
- «El inventario solo existe si la empresa tiene el add-on; `listar_empresas` lo dice. Desde
  aquí no se mueve material: para traspasos y recepciones, remite al panel o a la app.»
- «Las jornadas incompletas se corrigen en el panel.» (si §6.1 queda como se propone)

## 8. Pruebas

Son las mismas que en TDR-003 §7. Por cada herramienta, el contrato contra la puerta con un
doble del núcleo. Por cada puerta nueva, ajeno → 403 y asiento → 200 con una sesión real en
staging. Para las escrituras, la confirmación: sin id → vista previa, id inventado →
`confirmacion_invalida`, demasiado pronto → `confirmacion_prematura`. Al final, probar de
punta a punta con Claude y con ChatGPT sobre una empresa de staging con cartera
e inventario (la demo de ayuda a domicilio, si se le siembran).

## 9. Fuera de este documento

- Los movimientos físicos del inventario (§3). Las decisiones van en la fase D.
- Crear o cambiar clientes y contratos desde el conector: el alta del cliente pide datos
  fiscales y de dirección que se revisan mejor en el panel. Se puede reabrir si los clientes
  lo piden.
- El CRM (`sales`): es nuestro, no de los clientes, y va por otro conector. No se ha revisado
  aquí.

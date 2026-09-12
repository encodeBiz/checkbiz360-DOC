# Hallazgos — QA de CheckBiz360

Comportamientos del sistema que no coinciden con lo que se espera de él, o cuya intención no
está clara, **confirmados contra el código o contra el entorno de desarrollo**. Lo que un
análisis sospecha y nadie ha comprobado no entra aquí: se queda como sospecha en su catálogo.

Cada hallazgo dice qué se ha observado y dónde, no por qué ocurre, salvo que la causa esté
establecida. Una prueba que choca con un hallazgo afirma el comportamiento correcto y se marca
como fallo esperado con su identificador; el día que se arregle, la prueba avisará.

---

## HAL-01 · Suscribir sin cliente de Stripe responde un 500 genérico

- **Observado.** Una empresa con los datos legales completos pero sin cliente de Stripe recibe
  `500 internal_error` al suscribirse. `Subscribe.ts` lanza un `Error` con el código
  `subscribe/entity_not_configured` dentro del texto, nadie lo captura y el manejador general
  de billing lo convierte en un 500.
- **Dónde.** `encodebiz-api/services/billing/src/application/Subscribe.ts:23` y
  `services/billing/src/app.ts:35-37`.
- **Comprobado.** En el código, 2026-09-11.
- **Efecto.** El panel no puede decirle al usuario qué le falta. Hoy el cliente de Stripe solo
  se crea al abrir el portal de facturación, así que el recorrido del alta tiene que pasar por
  el portal antes de suscribir.
- **Casos.** REC-03.

## HAL-02 · En desarrollo, cada fichaje sale dos veces por webhook

- **Observado.** Al crear un fichaje, el contenedor emite su evento (`emitChecklogCreated`), y
  además el trigger `onChecklogWebhook`, desplegado y activo en `dev-encodebiz`, emite otro al
  escribirse el documento.
- **Dónde.** `encodebiz-api/services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts:531`
  y la función `onChecklogWebhook` (listado de funciones desplegadas en desarrollo).
- **Comprobado.** Código y funciones desplegadas en desarrollo, 2026-09-11. **Producción no se
  ha mirado.** Que los dos eventos lleven identificador y formato distintos lo dice el análisis
  de listeners y no está comprobado.
- **Efecto.** Un cliente suscrito a webhooks recibe cada fichaje dos veces.
- **Casos.** LIS-03.

## HAL-03 · La sucursal creada desde el panel nace con la geocerca desactivada

- **Observado.** En el formulario de sucursal, el campo `disableRatioChecklog` significa en
  realidad «activar geocerca»: arranca en `false` y se envía invertido. Si nadie marca la
  casilla, la sucursal se guarda con `disableRatioChecklog: true`.
- **Dónde.** `encodebiz-front-saas/src/app/main/[entityId]/checkinbiz/branch/form/form.controller.tsx:64`
  y `:170`.
- **Comprobado.** En el código, 2026-09-11.
- **Intención.** Sin establecer: puede ser una decisión de producto. Hay que preguntarlo antes
  de tratarlo como fallo.
- **Efecto.** Hasta que alguien active la geocerca, la sucursal acepta fichajes desde
  cualquier sitio.
- **Casos.** REC-05.

## HAL-04 · El empleado creado desde el panel nace sin verificación de dispositivo

- **Observado.** El formulario de empleado envía `enableA2F: false` por defecto en todos sus
  caminos.
- **Dónde.** `encodebiz-front-saas/src/app/main/[entityId]/checkinbiz/employee/form/form.controller.tsx:91`,
  `:201`, `:318` y `:574`.
- **Comprobado.** En el código, 2026-09-11.
- **Intención.** Sin establecer.
- **Efecto.** La app no pide segundo factor ni registra un dispositivo de confianza, y el
  fichaje no comprueba desde qué dispositivo se hace.
- **Casos.** REC-06, REC-09.

## HAL-05 · La facturación del día 5 sigue programada en desarrollo

- **Observado.** El job de Cloud Scheduler de `triggerInvoiceWorker` está habilitado en
  `dev-encodebiz`, con el cron `0 3 5 * *`, a la vez que existe el servicio de facturación en
  contenedor.
- **Dónde.** Listado de Cloud Scheduler de `dev-encodebiz`, 2026-09-11.
- **Comprobado.** En el entorno de desarrollo. Que facture en Stripe a todas las empresas
  activas de desarrollo lo dice el análisis de listeners y no está comprobado.
- **Consecuencia para QA.** Ninguna prueba lo fuerza.
- **Casos.** PRG-03.

## HAL-06 · El calendario de una empresa lo escribe cualquier cuenta autenticada

- **Observado.** `PATCH`/`POST /api/v1/checkinbiz/calendar` guarda y borra horarios, festivos y
  ausencias de la entidad que venga en el cuerpo, sin comprobar que quien llama pertenezca a
  esa entidad. El router solo exige un ID token de Firebase válido; el controlador de alcance
  `entity` no llama a `canWrite` ni mira `user_entity_roles`.
- **Dónde.** `encodebiz-api/services/checkinbiz/src/interfaces/http/calendar/calendar.router.ts`
  (monta `upsert` tras `requireFirebaseAuth`, sin más control) y
  `.../calendar/upsertEntityCalendar.controller.ts` (sin comprobación de permiso). Ninguno de
  los controladores de calendario comprueba pertenencia.
- **Comprobado.** En el código el 2026-09-11, y **con peticiones reales el 2026-09-12**: una
  cuenta de otra empresa lee el calendario ajeno (`200`) y le añade un festivo (`200`), y queda
  escrito.
- **No es solo escribir: es el módulo entero.** El catálogo dice «Autorización: ninguna» en las
  cinco rutas de calendario — leer (CHK-11), guardar (CHK-12), crear (CHK-13), guardar plantillas
  (CHK-14) y borrar festivos y ausencias (CHK-15). Cualquier cuenta del proyecto puede hacer las
  cinco cosas sobre cualquier empresa.
- **Efecto.** Cualquiera con una cuenta de Firebase del proyecto puede reescribir el calendario
  laboral de cualquier empresa si conoce su `entityId`, y eso decide **qué fichajes se aceptan**:
  cerrando los días de una empresa, su plantilla entera deja de poder fichar. También puede leer
  su organización del trabajo y borrarle los festivos.
- **Casos.** CHK-11-10 y CHK-12-22, cubiertos en la suite como fallos esperados; y los alcances
  `entity`, `branch` y `employee` del resto del bloque de calendario.

## HAL-07 · `/auth/validate` entrega una sesión con solo dos identificadores sin firma

- **Observado.** El endpoint público `POST /api/v1/checkinbiz/auth/validate` recibe un token que
  es `base64(JSON {employeeId, entityId})` —sin firma— y, si la ficha existe, devuelve un
  `sessionToken` válido y sin caducidad. Quien conozca o acierte ese par obtiene sesión de ese
  trabajador; con ella puede reiniciar su segundo factor y registrar un dispositivo propio como
  de confianza.
- **Dónde.** `encodebiz-api/services/checkinbiz/src/interfaces/http/auth/validateEmployee.controller.ts`
  (decodifica el base64 y firma el `sessionToken` sin `expiresIn`).
- **Comprobado.** En el código, 2026-09-11; el comportamiento «acepta un token fabricado a mano»
  ya está fijado por una prueba en verde (caso CHK del bloque de validación).
- **Efecto.** Suplantación de trabajador sin credencial, y sesión que no expira.
- **Casos.** Bloque de validación de empleado (catálogo CHK); ya cubierto en la suite como
  comportamiento actual.

## HAL-08 · Los webhooks salientes no comprueban la entidad

- **Observado.** `POST/GET/PATCH/DELETE /api/v1/events/endpoints` operan sobre el `entityId` que
  viaja en el cuerpo o en la query, sin comprobar que la cuenta autenticada pertenezca a esa
  entidad. El router exige `requireFirebaseAuth` pero ninguna ruta llama a `canWrite` ni valida
  pertenencia.
- **Dónde.** `encodebiz-api/services/events/src/app.ts` (monta `eventsRouter` solo tras
  `requireFirebaseAuth`) y `.../events/src/interfaces/http/events.router.ts` (las rutas de
  `endpoints` no comprueban la entidad).
- **Comprobado.** En el código, 2026-09-12.
- **Efecto.** Cualquier usuario autenticado puede suscribir su URL a los eventos de otra empresa
  y recibir sus fichajes, leer su secreto de firma, o borrar su integración.
- **Casos.** EVT (catálogo de facturación-informes-eventos).

## HAL-09 · La app no reconoce el código de secuencia `invalid_checkin`

- **Observado.** Ante un checkin fuera de secuencia, el contenedor responde
  `checklog/invalid_checkin`, pero el analizador de errores de la app compara contra
  `checklog/invalid_checki` (truncado). El caso cae en la rama por defecto y el usuario no ve el
  mensaje específico.
- **Dónde.** App: `checkbiz360/lib/core/errors/error_parser.dart` y `.../exceptions.dart`
  (`'checklog/invalid_checki'`). Contenedor:
  `encodebiz-api/services/checkinbiz/src/application/use-cases/checklog/CreateChecklog.ts`
  (`code: "checklog/invalid_checkin"`).
- **Comprobado.** En el código de ambos lados, 2026-09-11. La Cloud Function antigua ya enviaba
  `invalid_checkin`, así que el desajuste no lo introduce la migración: viene de antes.
- **Efecto.** Un mensaje de error menos claro en la app; no bloquea el fichaje.
- **Casos.** Bloque de creación de fichaje (catálogo CHK).

## HAL-10 · Un anónimo puede averiguar si una tarea existe

- **Observado.** `POST /api/v1/tasks/:taskId/assignments` con un `entityId` y un `taskId`
  cualesquiera, **sin ninguna credencial**, responde `404 {"code":"task/not_found"}` cuando la
  tarea no existe, y solo llega al `401` cuando existe. La diferencia entre las dos respuestas
  revela la existencia del recurso a quien no se ha identificado. El 404 de dominio se
  distingue además del 404 de ruta inexistente, que es `{"ok":false,"error":"not_found"}`.
- **Dónde.** `encodebiz-api/services/tasks/src/interfaces/http/task/assignTaskWorkers.controller.ts`:
  valida el cuerpo, **busca la tarea**, y solo después llama a `resolveTaskActor`. Otros
  controladores de tareas siguen el mismo orden.
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12.
- **Efecto.** Permite sondear qué identificadores de tarea existen en una empresa sin tener
  cuenta. El contenido no se filtra; la existencia y el estado, sí.
- **Casos.** TSK-09 y el resto de rutas de tarea que resuelven el actor después de buscar.

## HAL-11 · Una entrada mal formada revienta y devuelve la traza interna

- **Observado.** Enviando como `token` el texto `null` codificado en base64, las dos puertas de
  validación de empleado responden `500`:
  - `/api/v1/employees/validate` → `{"ok":false,"error":"internal_error"}`.
  - `/api/v1/checkinbiz/auth/validate` → `{"message":"Internal server error","code":"staff/internal_error","errors":["Cannot destructure property 'employeeId' of 'decoded' as it is null."]}`.
  La segunda **devuelve al cliente el mensaje de la excepción de JavaScript**, con el nombre de
  la variable interna.
- **Dónde.** `encodebiz-api/services/checkinbiz/src/interfaces/http/auth/validateEmployee.controller.ts`
  y su gemelo en `packages/shared/src/checkbiz/employees/validateEmployee.ts`: `JSON.parse`
  devuelve `null` y la desestructuración lanza.
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12.
- **Efecto.** Una entrada que debería rechazarse con un `400` provoca un error del servidor, y
  en una de las dos rutas se filtra detalle del código a quien no tiene credencial —el endpoint
  es público—.
- **Casos.** EMP-01-09 (cubierto en la suite como fallo esperado) y su equivalente en CHK-01.

## HAL-12 · ~~El periodo de prueba son 45 días y el producto vende 15~~ · CORREGIDO en desarrollo

- **Observado en su momento.** `BILLING_TRIAL_DAYS=45` en el entorno de desarrollo, y el valor
  por defecto del código también es 45: `const TRIAL_DAYS = Number(process.env.BILLING_TRIAL_DAYS ?? 45)`.
  Ese número se envía a Stripe como `trial_period_days` en cada alta de quien no ha estado
  suscrito antes.
- **Dónde.** `encodebiz-api/services/billing/src/application/Subscribe.ts:9` y `:61`;
  `/opt/encodebiz-api-dev/.env.staging`.
- **Confirmado por producto.** El periodo de prueba debe ser de **15 días**.
- **Corregido.** El 2026-09-12 por la tarde, comprobado en el servidor de desarrollo en los dos
  sitios que importan: `BILLING_TRIAL_DAYS=15` en `/opt/encodebiz-api-dev/.env.staging` **y** el
  contenedor `billing` en marcha devolviendo `15`. Que el fichero esté bien no basta: si el
  contenedor no se recreó después del cambio, sigue con el valor viejo.
- **Lo que queda.** El valor por defecto del **código** sigue siendo 45, así que un entorno que
  no declare la variable se llevaría 30 días de más en silencio. Y **producción no se ha
  mirado** —no se toca desde aquí—: falta confirmar qué valor tiene allí y qué se hace con las
  suscripciones ya creadas con 45.

## HAL-13 · Un plan retirado sigue en el catálogo y no se puede contratar

- **Observado.** `service/checkinbiz/plan/freemium` sigue existiendo en desarrollo, con
  `maxBranches: 1`, `maxEmployees: 10` y su lista de características. **Producto lo da por
  deprecado**: el único plan vigente es `bronze`. En desarrollo no hay ni una sola suscripción
  freemium: las 8 que existen son bronze.
- **Además, no es contratable.** Ni `freemium` ni `enterprise` tienen `stripePrice`, y
  `Subscribe` envía siempre `items: [{price: plan.stripePrice}]` a Stripe. Con el precio sin
  definir, el alta no puede completarse. *(Deducido del código; no se ha provocado.)*
- **Y el panel lo muestra.** Los planes se leen con `getAll('service/{servicio}/plan')`, sin
  filtrar ninguno, y `PricingCard` tiene una rama específica que suscribe directamente cuando
  el plan es `freemium`. También hay lógica de límites que lo menciona en las pantallas de
  sucursales y empleados.
- **Dónde.** Firestore de desarrollo; `encodebiz-front-saas/src/services/core/subscription.service.ts`
  y `.../components/common/PricingCard/PricingCard.controller.tsx:85`.
- **Comprobado.** Contra el entorno de desarrollo, 2026-09-12.
- **Efecto.** Un cliente nuevo puede ver y pulsar un plan retirado, y el alta falla.
- **Casos.** FAC-03.

## HAL-14 · Una corrección con identificadores cruzados le cambia el dueño al fichaje

- **Observado.** `POST /api/v1/checkinbiz/checklogs/update` no comprueba que el fichaje `id`
  pertenezca al `employeeId` del cuerpo. Enviando la ficha de un empleado y el identificador del
  fichaje de otro, la petición responde `200 checklog/updated` y el fichaje queda reescrito con
  el `employeeId` recibido: cambia de dueño. La notificación de la corrección le llega al
  empleado nuevo, no al que fichó.
- **Dónde.** `encodebiz-api/services/checkinbiz/src/interfaces/http/checklog/updateChecklog.controller.ts:120-124`
  busca el fichaje por `id` y `entityId` sin comparar nunca `checkData.employeeId`, y `:238-270`
  lo reescribe con el `employeeId` del cuerpo.
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12.
- **Efecto.** La jornada de una persona pasa a contarse en la de otra, y desaparece del historial
  de quien la trabajó. Es un registro con valor legal. El mismo hueco existe por el camino del
  empleado: quien conozca el `id` y un `updateId` del fichaje de un compañero de su empresa lo
  resuelve como si fuera suyo.
- **Casos.** CHK-09-14, cubierto en la suite como fallo esperado.

## HAL-15 · Rechazar una corrección deja escrita la hora que se rechazaba

- **Observado.** Cuando el empleado rechaza una propuesta (`status:"failed"`), el fichaje queda
  con la hora **propuesta**, no con la que tenía. La original solo sobrevive en el historial
  (`metadata.requestUpdates[].previousDate`), no en el propio fichaje. La única excepción es una
  propuesta con fecha futura, que sí restaura la original.
- **Dónde.** `updateChecklog.controller.ts:271-293`: el camino de resolución escribe `update.data`
  —la propuesta— y solo cambia el `status`.
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12. Viene
  heredado de la Cloud Function; no se introdujo al migrar.
- **Efecto.** Un rechazo invalida el fichaje y además le deja escrita la hora que el empleado
  acaba de negar. Si es intencionado, conviene decirlo; si no, el rechazo debería devolver
  `previousDate` y `previousStatus`. **Decisión de producto pendiente**: por eso la prueba fija
  el comportamiento observado en lugar de pintarlo en rojo.
- **Casos.** CHK-09-16.

## HAL-16 · Con `isAdmin` en texto, un empleado firma el fichaje con el uid de quien quiera

- **Observado.** `POST /api/v1/checkinbiz/checklogs` con `isAdmin:"true"` —la cadena, no el
  booleano— y un `uid` de propietario en el cuerpo, autenticado **solo con la sesión de
  trabajador de la app**, responde `201` y el fichaje queda con `metadata.updated.uid` igual al
  uid enviado en el cuerpo. Medido en desarrollo: la sesión era de un empleado y el fichaje
  salió firmado por el propietario de la empresa.
- **Dónde.** El enrutador compara con igualdad estricta (`checklog.router.ts:32`,
  `isAdmin === true`), así que `"true"` entra por la vía de la sesión de trabajador; el
  controlador lo comprueba de forma laxa (`createChecklog.controller.ts:132`) y da por bueno el
  `uid` del cuerpo, con el que llama a `canWrite`. Como ese uid sí es de un administrador, el
  permiso pasa —y de paso se salta el control de dispositivo de confianza (`:175`)—.
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12. Heredado
  idéntico de la Cloud Function.
- **Efecto.** Con la sesión de un empleado y un uid de administrador se ficha sin dispositivo de
  confianza y el registro queda a nombre de otro. El uid tampoco es difícil de conseguir: queda
  escrito en `metadata.updated.uid` de todo fichaje creado desde el panel.
- **Casos.** CHK-08-79, cubierto en la suite como fallo esperado.

## HAL-29 · Quien está de vacaciones ficha igual: el fichaje no lee las ausencias

- **Observado.** Un empleado con una ausencia registrada para hoy
  (`PATCH /api/v1/checkinbiz/calendar`, `scope:"employee"`, `absence:{startDate, endDate,
  status:"vacation"}`) ficha con `201`. En la **misma ejecución y contra el mismo dato**, el
  tablero de disponibilidad lo devuelve en `unavailable` con `reason:"absence"`,
  `reasonSource:"employee"` y el `absenceId` correcto. Medido en desarrollo el 2026-09-12.
- **Dónde.** `createChecklog.controller.ts:290-294` consulta `holidays?.some(h => h.date ===
  todayISO)` y no consulta `absences` en ningún punto. El tablero sí:
  `packages/shared/src/calendar/resolveAvailability.usecase.ts:193-197` expande el rango de
  cada ausencia a días sueltos y marca el día como no disponible.
- **No es «todavía no está implementado».** El dato existe, tiene su endpoint de alta, su
  validación —incluido el control de solapamiento entre ausencias— y su borrado; el tablero lo
  pinta. Solo el fichaje lo ignora. Un comentario del propio código lo dice:
  *«`absences` con rango son el modelo bueno, que existe y todavía no usa nadie»*.
- **Efecto.** Las vacaciones, las bajas y los permisos no cierran el fichaje. Alguien de baja
  puede marcar jornada —desde la app, con su sesión— y esa jornada cuenta como trabajada: entra
  en el informe, en las horas del mes y en lo que ve la gestoría. Y lo hace **contradiciendo al
  panel**, que a esa misma persona la está dando por ausente ese día. Si además se factura o se
  paga por horas registradas, el descuadre no se ve hasta el cierre.
- **Lo que sí cierra el día** es un festivo (`holidays`), que es del centro o de la empresa, no
  de la persona. No hay forma de cerrar el día de **una** persona por la vía que el producto
  ofrece para eso.
- **Casos.** CHK-08-28, cubierto en la suite como fallo esperado, con CHK-17-03 al lado en
  verde como contraste. Relacionado con la divergencia ya anotada en CHK-11 sobre el día sin
  clave, que el tablero y el fichaje también interpretan al revés.

## HAL-28 · Un descanso se engancha a la jornada de otro día y le cambia las horas

- **Observado.** Un empleado con responsabilidad en dos sucursales, B y B2. Se deja una jornada
  **cerrada** en B2 (entrada y salida) y después se abre una jornada nueva en B. Un `restin`
  enviado con `branchId` de B2 responde `201` y queda con `checkin` apuntando al **`checkin`
  cerrado de B2**. Medido en desarrollo el 2026-09-12: el descanso se enganchó a un fichaje ya
  marcado `closed:true`.
- **Dónde.** `services/checkinbiz/src/application/use-cases/checklog/CreateChecklog.ts:57-63`.
  La búsqueda del fichaje relacionado filtra por `type == "checkin"` y por `branchId`, ordena
  por fecha y coge el primero. No filtra por `status`, ni por `closed`, ni por jornada.
- **La asimetría es lo que lo convierte en defecto y no en decisión.** El mismo caso de uso sí
  rechaza el `checkout` en otra sucursal (`checklog/different_branches`, `:31-33`) por este
  motivo exacto: una jornada no se parte entre dos centros. El descanso no tiene esa
  comprobación.
- **Efecto.** Las horas de una jornada ya cerrada cambian después de cerrarse, y cambian hacia
  atrás en el tiempo: el descanso pertenece a hoy y se suma a la jornada de otro día. Lo que
  lee la analítica y lo que aparece en el informe de aquel día dejan de coincidir con lo que
  ocurrió, sin que nadie haya editado nada. En una empresa con dos centros —lo normal en el
  producto— basta con equivocarse de centro en la app.
- **Casos.** CHK-08-59, cubierto en la suite como fallo esperado. Relacionado: CHK-08-58, el
  caso sin historial en B2, que sí se rechaza porque no hay a qué engancharse.

## HAL-27 · Desactivar a un colaborador le quita el panel pero no le quita el fichaje

- **Observado.** Un asiento de administrador puesto en `status:"disabled"` con
  `PATCH /api/v1/checkinbiz/collaborators/:userId` sigue pudiendo crear fichajes a nombre de
  cualquier empleado de la empresa: `POST /api/v1/checkinbiz/checklogs` con `isAdmin:true`
  responde `201`. La misma cuenta, en la misma llamada, ya **no** puede consultar la ficha de
  un colaborador (`403 forbidden`). Medido en desarrollo el 2026-09-12.
- **Dónde.** `packages/shared/src/checkbiz/auth/canWrite.ts:16-21`: lee
  `user_entity_roles/{uid}_{entityId}`, mira `role` y devuelve `true` si es `owner` o `admin`.
  El campo `status` del asiento no se consulta nunca. El enrutador de colaboradores sí lo
  comprueba (`collaborator.router.ts:91`, `seat.status !== "active"`), y de ahí la diferencia
  de respuesta entre las dos rutas.
- **Alcance.** `canWrite` no es solo del fichaje: es la comprobación de permiso de entidad que
  usan las rutas de escritura de checkinbiz. Un asiento desactivado conserva todas.
- **Efecto.** «Desactivar» es lo que se hace cuando alguien deja la empresa pero se quiere
  conservar el rastro de lo que hizo, en vez de retirar el asiento. Quien lo haga se queda
  creyendo que ha cerrado el acceso: el panel le responde que no tiene permiso, y la API le
  deja firmar jornadas de otros.
- **Casos.** CHK-08-77, cubierto en la suite como fallo esperado, junto a COL-03-05 —el
  contraste, en verde—. Ya estaba anotado el mismo comportamiento en COL-01-04.

## HAL-26 · El panel pide la hora del fichaje, la valida, y el servidor la tira

- **Observado.** `POST /api/v1/checkinbiz/checklogs` con `isAdmin:true` y `timestamp` de hace
  tres horas responde `201` y el fichaje queda sellado **ahora**: 180,02 minutos de diferencia
  entre la hora pedida y la guardada. Medido en desarrollo el 2026-09-12.
- **Dónde.** `services/checkinbiz/src/interfaces/http/checklog/createChecklog.controller.ts`:
  `const timestamp = now`, con `now = DateTime.now().setZone(tz)`. El `timestamp` del cuerpo no
  se lee en ningún punto del controlador, ni se valida, ni se rechaza.
- **Y el panel lo manda.** El formulario de asistencia tiene un campo de fecha y hora
  **obligatorio**, con regla propia de validación para que no sea futura
  (`front:src/app/main/[entityId]/checkinbiz/attendance/AttendanceFormModal/`,
  `timestamp: notFutureDateRule(t)`), y lo envía en el cuerpo. Quien lo rellena no tiene forma
  de saber que se descarta: la respuesta es un `201` y un aviso de éxito.
- **Efecto.** La vía del panel existe para registrar lo que la app no registró —alguien que se
  dejó el móvil, una entrada que falló—. Eso siempre se hace después, así que el fichaje
  correcto es siempre uno del pasado. Tal y como está, todo fichaje añadido desde el panel
  queda con la hora en que se añadió, no con la hora que se pidió, y el registro dice algo
  distinto de lo que ocurrió. **La edición sí respeta la hora** (`updateChecklog`, CHK-09), así
  que hoy el único modo de dejar la hora correcta es crear el fichaje y corregirlo acto
  seguido.
- **Relacionado.** El panel manda como `geo` las coordenadas de la propia sucursal
  (`branch.address.geo`), así que un fichaje creado por esta vía nunca cae fuera de la
  geocerca. Es coherente con que lo marque un administrador y no el empleado, pero conviene
  saberlo al leer `metadata.distance` de un fichaje del panel.
- **Casos.** CHK-08-74, cubierto en la suite como fallo esperado.

## HAL-25 · La edición de una ficha acepta cualquier campo, incluida la lista de dispositivos

- **Observado.** `POST /api/v1/employees/update` no tiene lista de campos permitidos: hace
  `set(merge)` con lo que llegue, excluyendo solo `uid` y `createdAt`. Enviando
  `trustedDevicesId:{ids:["dispositivo-metido-a-mano"]}` responde `201` y **queda escrito**.
  Comprobado leyendo la ficha, 2026-09-12.
- **Dónde.** `services/employees/src/interfaces/http/employee.router.ts` (rama `update`) y
  `packages/shared/.../FirestoreEmployeeRepository.ts:194-197`.
- **Por qué ese campo y no otro.** `trustedDevicesId` no es un dato de la ficha, es una
  **credencial**: el fichaje comprueba que `base64(User-Agent)` esté en esa lista antes de
  aceptar la marca de quien tiene el segundo factor puesto. Escribirla a mano equivale a dar de
  alta un dispositivo de confianza sin pasar por el segundo factor.
- **Qué habilita, con precisión.** No es por sí solo una escalada: quien puede llamar a esta
  ruta ya es propietario o administrador de la empresa, y esos ya pueden fichar por otro con
  `isAdmin` —dejando su uid escrito en el fichaje—. Lo que añade es **quitar el rastro**:
  registrado el dispositivo, se puede fichar por la vía del trabajador. Y desactiva el control
  que compensa parcialmente HAL-07, donde la sesión de trabajador se fabrica sin firma.
- **El problema de fondo es la ausencia de lista blanca**, no ese campo concreto: cualquier
  campo interno que el sistema use para decidir algo es escribible desde fuera mientras no se
  acote.
- **Casos.** EMP-04-12, cubierto en la suite como fallo esperado.

## HAL-24 · Editar un centro le reactiva la geocerca, y borrarlo deja gente apuntando a él

Tres comportamientos del mantenimiento de centros de trabajo, medidos contra desarrollo el
2026-09-12.

- **Editar cualquier cosa reactiva la geocerca.** `POST /api/v1/branches/update` escribe
  `disableRatioChecklog: false` cuando el campo **no viene en el cuerpo**
  (`branch.validation.ts:264`). Un centro que tenía la geocerca quitada y al que solo se le
  cambia el nombre sale con la geocerca puesta. Nadie lo pidió y nada lo avisa.
  - **Por qué duele.** La gente de ese centro pasa de poder fichar desde cualquier sitio a no
    poder fichar fuera del radio, de un día para otro, porque alguien le corrigió una letra al
    nombre. Y se junta con HAL-03, que ya hace que el formulario del panel mande ese campo
    invertido.
- **Borrar un centro deja a su gente apuntando a él.** El borrado retira las responsabilidades
  del centro —eso sí lo hace— pero no limpia la lista `branchId` de cada ficha
  (`FirestoreBranchRepository.ts:86-94`, `:123-129`). Comprobado leyendo la ficha: después del
  borrado sigue conteniendo el identificador de un centro que ya no existe.
- **Borrar un centro que no existe responde `200`.** No hay comprobación previa de existencia,
  así que un identificador equivocado se salda con «borrado correctamente».
- **Casos.** SUC-02-04, SUC-04-03 y SUC-04-05, cubiertos en la suite como fallos esperados.
  Al lado van en verde SUC-04-01 —el borrado sí retira la entrada del buscador— y SUC-02-01 —el
  cambio de nombre sí se reindexa—, que es lo que sitúa los tres anteriores como huecos y no
  como «esto no está hecho».

## HAL-23 · Modificar una responsabilidad la inventa, y un puesto sin precio guarda NaN

- **Observado.** `PATCH /api/v1/employees/responsibilities` tiene dos comportamientos que no
  deberían ser:
  - Con un `id` de una responsabilidad **que no existe** → `200`, y **la crea**. Medido: quedó un
    documento con `responsibility:"owner"` y `level:4` —el máximo—, tomados del cuerpo.
  - Con `job:{job:"X"}` **sin `price`** → `200`, y el precio queda guardado como **`NaN`**.
    Comprobado leyendo el documento: `typeof price === "number"` y `Number.isNaN(price)`.
- **Dónde.** `services/employees/src/interfaces/http/employee.router.ts` (rama PATCH) y
  `packages/shared/.../FirestoreEmployeeRepository.ts:71-73`, que hace `set(payload, {merge:true})`
  sin comprobar antes que el documento exista, y sin `await`.
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12.
- **Lo que NO es, y conviene decirlo.** El documento inventado **no da poder**: `canWrite`
  filtra por `active == 1` (`packages/shared/src/checkbiz/auth/canWrite.ts:42`) y el documento
  nace sin ese campo. Tampoco es una vía de escalada, porque el `PATCH` ya exige ser propietario
  o administrador de la empresa, que es quien puede asignar de todas formas. Es suciedad en la
  colección que decide quién manda en cada centro, no un agujero de permisos.
- **Efecto.** Un identificador mal tecleado crea un permiso que nadie pidió, con nivel máximo, y
  queda ahí hasta que alguien lo mire. Y el `NaN` viaja al coste del puesto, que es dato de
  informes: cualquier suma que lo toque da `NaN` y arrastra el total entero.
- **Casos.** EMP-10-06 y EMP-10-04, cubiertos en la suite como fallos esperados.

## HAL-22 · Sin horario configurado, la app se rompe pero el fichaje funciona

- **Observado.** Una empresa recién dada de alta no tiene `calendar/config` —alguien tiene que
  entrar al panel a ponerlo—. En ese estado:
  - `GET /api/v1/checkinbiz/calendar` → **404** `{code:"calendar/not_found"}`. Es la llamada con
    la que **arranca la pantalla de fichaje de la app**, y la app la convierte en excepción
    (`attendance_remote_datasource.dart:104`, `ErrorParser.parseApiError`).
  - `POST /api/v1/checkinbiz/checklogs` → **201**. El fichaje se defiende solo: sin configuración
    abre el día de 00:00 a 23:59 con `scheduleApplied.source:"default"` en vez de romper
    (`createChecklog.controller.ts:210-229`).
- **Dónde.** `getEffectiveCalendar.controller.ts` (404 sin configuración) frente a
  `createChecklog.controller.ts:210-229` (valor por defecto seguro).
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12 (CHK-11-18 y
  CHK-08-31).
- **Efecto.** La incoherencia es el problema: el fichaje, que es la operación que el horario
  guarda, tolera que no haya horario; la lectura que la app necesita para pintar la pantalla, no.
  Una empresa que se da de alta un viernes y reparte la app antes de configurar el horario tiene
  a toda su plantilla con la app fallando, cuando fichar habría funcionado.
- **Lo que no está establecido.** Qué enseña exactamente la pantalla ante ese error: eso hay que
  mirarlo en la app, no en la API. Lo que sí está establecido es que la API responde 404 y que el
  cliente lo convierte en excepción.
- **Decisión pendiente.** O el alta deja el horario puesto por defecto, o la lectura devuelve el
  mismo día abierto que ya aplica el fichaje en vez de un 404.
- **Casos.** CHK-11-18 y, como contraste, CHK-08-31.

## HAL-21 · Un administrador se hace propietario, y de paso aparta al que lo era

- **Observado.** Con un asiento de `admin` activo en una empresa, y solo con su token de
  Firebase, se puede:
  - `PATCH /api/v1/checkinbiz/collaborators/{supropiouid}` con `role:"owner"` → **200**, y queda
    escrito: se asciende a sí mismo.
  - `PATCH` sobre el uid de un propietario con `role:"admin"` → **200**: lo rebaja.
  - `POST /api/v1/checkinbiz/collaborators` con `role:"owner"` para un correo cualquiera →
    **201**: entrega la propiedad de la empresa a quien quiera, incluido alguien de fuera.
- **Dónde.** `services/checkinbiz/src/application/use-cases/auth/manageCollaborator.ts:120-148`
  (conceder) y `:167-194` (modificar). Ninguna de las dos recibe quién llama, así que no puede
  comparar su rango con el del afectado. La puerta de entrada
  (`collaborator.router.ts`) solo exige «asiento activo `owner` **o** `admin`».
- **Lo que lo convierte en descuido y no en decisión.** La tercera puerta del mismo fichero sí
  lo protege: `DELETE` (`:204-233`) comprueba explícitamente que a un propietario solo lo retire
  otro propietario (`owner_required`) y que nunca se quede sin ninguno. La intención está
  implementada; falta en dos de las tres puertas.
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12, con un
  administrador recién sentado sobre una empresa de prueba.
- **Efecto.** El escalón entre propietario y administrador deja de existir. Quien entra como
  administrador —una invitación, un colaborador externo, una cuenta comprometida— se queda con
  la empresa: puede cobrar, dar de baja el servicio, apartar al dueño y entregar el control a un
  tercero. La protección del borrado no sirve de nada si primero se puede rebajar al propietario
  a administrador.
- **Casos.** COL-04-02, COL-04-03 y COL-02-04, cubiertos en la suite como fallos esperados.
  COL-05-04 va en verde al lado, a propósito: es la prueba de que la regla existe.

## HAL-20 · checkinbiz se activa sin método de pago

- **Regla de producto, confirmada el 2026-09-12.** Para activar checkinbiz hace falta **método
  de pago**. No es una cuestión de cobro: la tarjeta es lo que distingue a una empresa real de
  alguien probando, y por eso el requisito va en la activación y no después.
- **Observado.** Hoy no se cumple. Una empresa con sus datos legales y su cliente de
  facturación, **sin ninguna tarjeta asociada**, activa el servicio y recibe `201`. Comprobado
  contra desarrollo con peticiones reales, 2026-09-12: es justo lo que hace el alta de cada
  ejecución de la suite.
- **Dónde.** `packages/shared/src/platform/FirestoreEntityRepository.ts:51-70`. `isConfigured`
  tiene dos caminos: en modo `checkbiz` comprueba solo `name` y los datos legales; para los
  demás servicios exige además `billingConfig.payment_method` no vacío, `slug`, `billingEmail`,
  `branding.logo` y `active`. La llamada desde `billing.router.ts:44-47` entra por el primero.
- **No es un descuido, es una regla que cambia.** El comentario del propio código lo dice:
  «`checkbiz` pide solo lo legal (lo que exige una nómina); el resto de servicios piden además
  cobro y marca». Era deliberado; la decisión de producto de hoy lo cambia.
- **Efecto.** Cualquiera con una cuenta puede activar el servicio de pago sin dar medio de
  cobro, y el sistema lo da por cliente durante todo el periodo de prueba. Al terminarlo, no hay
  con qué cobrar.
- **Lo que arrastra.** Cuando se implemente, **el alta de la suite dejará de funcionar tal como
  está**: `crearMundo` activa sin tarjeta. Habrá que engancharle un método de pago de prueba
  antes de activar, cosa que además hace el mundo más fiel a un cliente de verdad.
- **Casos.** FAC-03-17, cubierto en la suite como fallo esperado.

## HAL-19 · El importe a cobrar depende de un aviso previo, y nadie comprueba que llegara

- **Observado.** La cantidad facturable —cuántos empleados se cobran— **no se calcula al emitir
  la factura**. Se ajusta antes, al recibir `invoice.upcoming` o
  `customer.subscription.trial_will_end`, porque sobre un borrador ya creado
  `subscriptions.update` no reescribe las líneas (`StripeWebhookHandler.ts:176-181`). Si ese
  aviso no llega, la factura sale con la cantidad **con la que nació la suscripción**, que para
  una empresa recién dada de alta es **cero**.
- **Dónde.** `services/billing/src/application/StripeWebhookHandler.ts:158-204` y
  `services/billing/src/application/Subscribe.ts:59`.
- **Comprobado.** Contra desarrollo, 2026-09-12. Forzando el fin de la prueba sin dar tiempo a
  los avisos, la factura del primer mes salió con la línea `0 × Checkbiz Plan Bronze (at €2.00 /
  month)`, **0,00 €**, sobre una empresa con 16 empleados y una suscripción que después quedó
  correctamente en 16 unidades. Es decir: la cantidad se corrigió, pero la factura ya estaba
  emitida.
- **Y ya ocurrió una vez.** El comentario del propio código lo cuenta: passinbiz «se quedaba con
  la cantidad con la que nació —cero— y facturaba 0,00 € mes tras mes». El ajuste por webhook es
  precisamente el arreglo de aquello.
- **Efecto.** Cualquier interrupción del webhook durante la ventana del aviso convierte ese mes
  en gratis, en silencio y sin que nada lo señale. **Y hoy esa interrupción existió**: entre la
  mudanza de servidor y su arreglo, el webhook apuntaba a un host muerto (HAL-18).
- **Lo que falta.** No hay ninguna comprobación posterior de que lo facturado coincida con lo que
  debía facturarse. Una factura a 0 € de una empresa con empleados activos debería chillar.
- **Y medido de la forma correcta, el mecanismo FUNCIONA.** Poniendo el fin de la prueba a dos
  minutos vista en vez de «ahora», contra desarrollo el 2026-09-12: a los **21 s** llegó el aviso
  previo y la cantidad pasó de `0` a `5`; a los **138 s** se emitió la factura por **10,00 €**,
  con la línea `5 × Checkbiz Plan Bronze`. Es decir: el diseño es correcto y el recálculo hace su
  trabajo **siempre que el aviso llegue**. Todo el riesgo está en que no llegue, y eso ya ocurrió
  (HAL-18). Lo que sigue faltando es una comprobación posterior de que lo facturado cuadre.
- **Casos.** Bloque 1. La prueba fiel **no puede usar `trial_end: "now"`**: eso se salta los dos
  avisos de los que depende el diseño. Hay que recorrer la secuencia de eventos, con un reloj de
  prueba de Stripe o con un fin de prueba a unos minutos vista.

## HAL-18 · Desarrollo se quedó sordo a Stripe tras la mudanza de servidor

- **Observado.** En Stripe, modo prueba, hay **dos** webhooks dados de alta y los dos
  `ENABLED`. El del contenedor apunta a `http://141.95.47.135:8080/api/v1/billing/webhook`, que
  es el servidor de **producción** por un puerto que quedó **cerrado** el 2026-09-12 al retirar
  de allí el stack de desarrollo. La ruta es correcta; el host ya no existe.
- **Dónde.** Configuración de Stripe (modo prueba), no en el repositorio. La dirección buena
  es `https://api-staging.checkbiz360.com/api/v1/billing/webhook`
  (`services/billing/src/app.ts:20`, servida por `nginx.staging.conf:180`).
- **Comprobado.** Listando los webhooks con la API de Stripe en modo prueba, 2026-09-12.
- **Efecto.** Nada de lo que Stripe cuenta llega al contenedor de desarrollo: ni facturas
  emitidas, ni cobros, ni fallos de cobro, ni bajas, ni altas de método de pago. En la práctica
  **no se puede probar el fin del periodo de prueba ni el cobro** hasta arreglarlo, y cualquier
  factura que Stripe genere en desarrollo no se registra ni se envía.
- **El segundo webhook sigue vivo.** Apunta a la Cloud Function `stripeWebhook` de
  `dev-encodebiz` y cubre casi los mismos eventos. Es un hecho observado: **no está establecido**
  si se conserva a propósito como camino de vuelta o si quedó olvidado al migrar. Mientras los
  dos estén activos, los eventos que ambos declaran se procesan por dos sitios.
- **Casos.** Bloquea el bloque 1 en su último paso; sin esto, FAC-07 no se puede probar de
  extremo a extremo.

## HAL-17 · Apagar la semana entera abre el fichaje en vez de cerrarlo

- **Observado.** Un horario con los **siete días** deshabilitados no impide fichar: el fichaje
  sale `201` con `scheduleApplied.source:"default"` y una ventana abierta de 00:00 a 23:59.
  Deshabilitar **un solo día** sí lo cierra (`400 checklog/day_disabled`). La diferencia está en
  si queda algún turno en la semana, no en lo que diga `disabled`.
- **Dónde.** `createChecklog.controller.ts:210-229`: `noConfig` agrupa «no hay calendario» con
  «no hay un solo turno en toda la semana» (`hasAnyShifts`), y en ese caso construye un día
  abierto. Es un valor por defecto **deliberado** —el comentario del código lo dice: el fichaje
  no debe romper si nadie ha configurado nada—, pero atrapa también a quien sí configuró y lo
  que configuró fue «aquí no se trabaja».
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12.
- **Efecto.** Una empresa o una sucursal que apaga los siete días desde el panel obtiene lo
  contrario de lo que pidió: fichaje abierto las 24 horas, sin aviso. **Decisión de producto
  pendiente**: si el valor por defecto solo debe aplicarse cuando no existe `calendar/config`,
  basta con no mirar `hasAnyShifts`.
- **Casos.** CHK-08-31 (la suite fija el comportamiento observado) y CHK-08-24 (un día suelto sí
  cierra).

---

## Correcciones al catálogo encontradas al ejecutar

Las pruebas también corrigen el inventario. Se anotan aquí para no repetir el error.

- **CHK-09 · el historial nunca está vacío.** El catálogo daba por hecho que
  `metadata.requestUpdates` solo guarda correcciones. No es así: todo fichaje nace ya con una
  entrada `action:"created"` —con `data:{}` y el `uid` de quien lo creó— que escribe
  `createChecklog.controller.ts:429-435`. Tras la primera propuesta hay **dos** entradas, no una.
  De ahí se siguen dos cosas: el caso CHK-09-19 tal y como estaba descrito («fichaje sin
  `requestUpdates`») es inalcanzable —lo que se prueba es un `updateId` que no está en la lista—,
  y el `id` de la entrada de creación es un `updateId` válido que un empleado puede resolver
  (CHK-09-21).
- **CHK-08-23 · el despedido sí está tapado, pero de rebote.** El catálogo concluía que un
  empleado dado de baja seguiría fichando porque el fichaje no mira su `status`. Lo primero es
  cierto y lo segundo no: medido el 2026-09-12, responde `404 employee/not_resposibility`,
  porque la baja **le retira las responsabilidades y le vacía `branchId`**. La puerta está
  cerrada, pero por un camino distinto del que se suponía — y eso importa, porque una ficha que
  llegue a `inactive` o `vacation` **por otra vía** (una edición, una importación) conserva sus
  responsabilidades y sí ficharía. La prueba afirma las dos cosas, el resultado y el mecanismo,
  para que un cambio en la baja se note antes de reabrir la puerta.
- **TSK-09-01.** El catálogo decía que asignar «sin `employeeIds`» devuelve `400
  task/bad_request`. No es cierto: el controlador desestructura con `employeeIds = []`, y una
  lista vacía sí es un array, así que la comprobación pasa y la petición sigue hasta el
  `404`. El `400` solo se produce cuando `employeeIds` **no es un array** (una cadena, por
  ejemplo). Corregido en la prueba y pendiente de corregir en `tareas.md`.

---

## Sospechas graves pendientes de verificar

Vienen de los análisis y **todavía no se han comprobado una a una**. No son hallazgos hasta
confirmarlas; cada una se verificará al escribir su prueba.

- **Estado del empleado nunca comprobado.** Un empleado dado de baja (`fired`) seguiría fichando
  y operando tareas, porque el `status` no se mira al fichar ni al cambiar el estado de una tarea
  (catálogos CHK y TSK).
- **Escalada de rol en colaboradores.** Un administrador podría ascenderse a propietario con
  `PATCH /collaborators/:userId`; el `requireEntityWriter` admite admin, y falta confirmar si
  `updateCollaborator` distingue quién puede tocar el rol `owner` (catálogo EMP/COL).
- **Borrado de empresa sin permiso.** Sigue en Cloud Functions y, según el análisis, no comprueba
  permisos ni cascada (catálogo ENT).
- **`isAdmin` como texto en el fichaje.** Enviar `isAdmin:"true"` y el `uid` de un propietario
  saltaría el dispositivo de confianza (catálogo CHK).
- **`completionPolicy` no se aplica** y **transiciones de estado sin control de origen** en
  tareas (catálogo TSK).
- **Consulta de suscripciones y generación de informes sin filtrar por entidad** (catálogo
  FAC/INF).
- **Doble correo de «servicio activado»** al suscribir (catálogo de listeners).

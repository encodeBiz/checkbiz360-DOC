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
- **Comprobado.** En el código, 2026-09-11.
- **Efecto.** Cualquiera con una cuenta de Firebase del proyecto puede reescribir el calendario
  laboral de cualquier empresa si conoce su `entityId`, y eso altera qué fichajes se aceptan.
- **Casos.** Alcances `entity`, `branch` y `employee` del bloque de calendario (catálogo CHK).

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

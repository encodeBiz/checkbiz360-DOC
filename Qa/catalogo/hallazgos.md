# Hallazgos — QA de CheckBiz360

Comportamientos del sistema que no coinciden con lo que se espera de él, o cuya intención no
está clara, **confirmados contra el código o contra el entorno de desarrollo**. Lo que un
análisis sospecha y nadie ha comprobado no entra aquí: se queda como sospecha en su catálogo.

Cada hallazgo dice qué se ha observado y dónde, no por qué ocurre, salvo que la causa esté
establecida. Una prueba que choca con un hallazgo afirma el comportamiento correcto y se marca
como fallo esperado con su identificador; el día que se arregle, la prueba avisará.

## Estado al 2026-09-14

De los 37 hallazgos, **35 están corregidos o con el código listo** y 2 esperan una decisión
de producto. La suite completa contra staging ya no lleva ningún indulto. El detalle de cada
uno está en su bullet **Corregido**, y el plan, las decisiones tomadas y lo que queda a mano
en [hallazgos-triaje.md](./hallazgos-triaje.md).

| Estado | Hallazgos |
|---|---|
| Corregido en desarrollo y verificado por la suite | HAL-01, 06, 07, 08, 10, 11, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 34, 35, 36, 37 |
| Corregido en desarrollo, a falta de una configuración fuera del repo | HAL-19 (suscribir `invoice.created` en el webhook de Stripe) |
| Código listo, retirada o publicación pendiente | HAL-02 y HAL-05 (borrar las funciones en `dev-encodebiz`), HAL-09 (siguiente versión de la app) |
| Cerrados con anterioridad | HAL-12, HAL-18, HAL-31, HAL-33 |
| Decisión de producto pendiente, sin tocar | HAL-03 (geocerca al crear sucursal), HAL-04 (segundo factor al crear empleado) |

Los identificadores no se reutilizan: un hallazgo corregido conserva su número y su texto
original, con la corrección debajo.

---

## HAL-01 · Suscribir sin cliente de Stripe responde un 500 genérico · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-14, en desarrollo. El router de facturación traduce los rechazos con código del alta: `subscribe/not_found` → 404, `subscribe/entity_not_configured` → 412, `subscribe/plan_not_available` → 409. Con HAL-20 el caso original ya no se alcanza —sin cliente de Stripe no hay método de pago y la activación se corta antes—, pero el 500 deja de existir.
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

## HAL-02 · En desarrollo, cada fichaje sale dos veces por webhook · CÓDIGO LISTO, retirada pendiente

- **Corregido.** El 2026-09-13. `onChecklogWebhook` sale del índice del SaaS (`feat/retirar-triggers-duplicados`, fusionado en su `develop`, sin desplegar). Borrar la función en `dev-encodebiz` lo bloqueó el clasificador y queda para hacer a mano; en producción, comprobar qué está desplegado antes del pase.
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

## HAL-05 · La facturación del día 5 sigue programada en desarrollo · CÓDIGO LISTO, retirada pendiente

- **Corregido.** El 2026-09-13. `triggerInvoiceWorker` y `processInvoices` salen del índice del SaaS (misma rama). Borrar las dos funciones —y con la programada, su job de Scheduler— en `dev-encodebiz` queda para hacer a mano.
- **Observado.** El job de Cloud Scheduler de `triggerInvoiceWorker` está habilitado en
  `dev-encodebiz`, con el cron `0 3 5 * *`, a la vez que existe el servicio de facturación en
  contenedor.
- **Dónde.** Listado de Cloud Scheduler de `dev-encodebiz`, 2026-09-11.
- **Comprobado.** En el entorno de desarrollo. Que facture en Stripe a todas las empresas
  activas de desarrollo lo dice el análisis de listeners y no está comprobado.
- **Consecuencia para QA.** Ninguna prueba lo fuerza.
- **Casos.** PRG-03.

## HAL-06 · El calendario de una empresa lo escribe cualquier cuenta autenticada · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Leer exige pertenecer a la empresa —asiento activo, o ficha de empleado con ese uid, que es como lo pide la app— y escribir exige asiento o responsabilidad de supervisor o más sobre el ámbito (`calendar.access.ts`; `requireEntityMember` y `requireEntityWriter` en shared). CHK-11-10 y CHK-12-22 en verde.
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

## HAL-07 · `/auth/validate` entrega una sesión con solo dos identificadores sin firma · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. El login y el correo de bienvenida emiten un JWT firmado con `JWT_2FA_SECRET` y con vida de 30 días; las dos puertas de validación verifican la firma y responden `401 employee/invalid_token` a lo demás, exista la ficha o no; la sesión caduca a los 30 días y `expiresAt` llega relleno. La app ya tenía camino de reserva: si el token se rechaza, vuelve a hacer login con Firebase y valida con uno nuevo. En producción, la primera vez, los tokens guardados en las apps instaladas se rechazarán y la app repetirá el login sola.
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

## HAL-08 · Los webhooks salientes no comprueban la entidad · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Cada ruta de `endpoints` y de entregas exige asiento activo en la entidad; el reintento de una entrega se comprueba contra la entidad de la propia entrega. Cubierto por el fichero nuevo `26-webhooks-salientes.spec.ts` (EVT-03-17, EVT-04-05, EVT-06-06, EVT-07-06), en verde.
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

## HAL-09 · La app no reconoce el código de secuencia `invalid_checkin` · CÓDIGO LISTO en la app, sin publicar

- **Corregido.** El 2026-09-14. Las dos cadenas corregidas en `fix/codigo-invalid-checkin` de `checkbiz360`, desde su `develop`, sin fusionar ni publicar: sale con la siguiente versión de la app.
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

## HAL-10 · Un anónimo puede averiguar si una tarea existe · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-14, en desarrollo. Los catorce controladores que buscan la tarea comprueban antes que hay credencial válida —ID token o sesión de trabajador— y responden el mismo `401 auth/unauthorized` exista o no la tarea, esté como esté y figure quien figure. Va en el controlador, después de validar el cuerpo, y no en el router: la suite fija a propósito que el cuerpo se valida antes que la sesión, y un middleware tapaba además el 404 de las rutas inexistentes. TSK-09-02, TSK-14-03 y TSK-17-03 en verde.
- **Observado.** `POST /api/v1/tasks/:taskId/assignments` con un `entityId` y un `taskId`
  cualesquiera, **sin ninguna credencial**, responde `404 {"code":"task/not_found"}` cuando la
  tarea no existe, y solo llega al `401` cuando existe. La diferencia entre las dos respuestas
  revela la existencia del recurso a quien no se ha identificado. El 404 de dominio se
  distingue además del 404 de ruta inexistente, que es `{"ok":false,"error":"not_found"}`.
- **Dónde.** `encodebiz-api/services/tasks/src/interfaces/http/task/assignTaskWorkers.controller.ts`:
  valida el cuerpo, **busca la tarea**, y solo después llama a `resolveTaskActor`. Otros
  controladores de tareas siguen el mismo orden.
- **Comprobado.** Contra el entorno de desarrollo con peticiones reales, 2026-09-12.
- **Y no es solo la existencia.** Medidas dos sondas más el 2026-09-12, las dos **sin ninguna
  credencial**:
  - `POST /:taskId/validation` responde `400 task/invalid_status` si la tarea no está completada
    y llega al `401` si lo está (`validateTask.controller.ts:17-19`). O sea que se puede saber
    **si una tarea está terminada**.
  - `POST /:taskId/ratings` responde `400` con «Employee is not assigned to this task» antes de
    autenticar (`rateTaskWorker.controller.ts:22-24`). Probando identificadores de empleado
    contra una tarea se averigua **quién figura en ella**.
- **Efecto.** Permite sondear qué identificadores de tarea existen en una empresa sin tener
  cuenta, y de las que existen, si están terminadas y quién trabaja en ellas. El contenido no se
  filtra; la existencia, el estado y la plantilla asignada, sí.
- **Casos.** TSK-09, TSK-14-03 y TSK-17-03, cubiertos en la suite como fallos esperados, y el
  resto de rutas de tarea que resuelven el actor después de buscar.

## HAL-11 · Una entrada mal formada revienta y devuelve la traza interna · CORREGIDO en desarrollo

- **Corregido.** Cerrado de rebote por HAL-07 el 2026-09-13: ya no se descodifica nada que no venga firmado, y un `null` en base64 es un `401 employee/invalid_token` sin traza. EMP-01-09 en verde.
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

## HAL-13 · Un plan retirado sigue en el catálogo y no se puede contratar · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-14. `Subscribe` rechaza cualquier plan sin precio en Stripe con `409 subscribe/plan_not_available`; el plan `freemium` está marcado `deprecated: true` en el Firestore de desarrollo, y el panel deja de listar los planes con esa marca (`feat/planes-retirados-ocultos` del front, sin fusionar). `enterprise` sigue visible a propósito: no tiene precio pero abre el contacto.
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

## HAL-14 · Una corrección con identificadores cruzados le cambia el dueño al fichaje · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Con ids cruzados responde `404 checklog/not_found` y no reescribe nada. CHK-09-14 en verde.
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

## HAL-15 · Rechazar una corrección deja escrita la hora que se rechazaba · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-14, en desarrollo, tomando la lectura de que no era intencionado. Rechazar una propuesta deja el fichaje como estaba —la hora no se toca, porque la propuesta vivía en el historial, y el estado vuelve al de antes de proponer— y anota el rechazo con su motivo en `metadata.requestUpdates`. Antes dejaba el fichaje en `failed`, fuera del registro de jornada, por no estar de acuerdo con una corrección. CHK-09-16 pasa a afirmarlo.
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

## HAL-16 · Con `isAdmin` en texto, un empleado firma el fichaje con el uid de quien quiera · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Un `isAdmin` que no sea booleano es una petición mal formada (`400 checklog/bad_request`), y por la vía de la app nada del cuerpo decide quién firma. CHK-08-79 y CHK-08-80 en verde con el contrato nuevo.
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

## HAL-37 · Rechazar una tarea deja su pausa abierta para siempre · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. El rechazo cierra la pausa abierta en la misma transacción que el cambio de estado, con `endedReason:"rejected"`. TSK-15-13 en verde.
- **Observado.** Una tarea en curso y pausada que se rechaza queda en `rejected` **conservando
  `pausedAt` y `pauseId`**. La pausa nunca se cierra, así que su duración no entra en `pausedMs`
  y el documento de la pausa se queda sin `endedAt`. Medido en desarrollo el 2026-09-12.
- **Dónde.** `services/tasks/src/interfaces/http/task/rejectTask.controller.ts` escribe con
  `updateTaskUseCase`. Completar, cancelar y reabrir sí cierran la pausa abierta, y lo hacen **en
  la misma transacción** que el cambio de estado (`updateTaskStatus.controller.ts:120`, `:131`,
  `:146`, con `endedReason` distinto en cada caso). El rechazo se escribió por otro camino y se
  quedó fuera de esa red.
- **Efecto.** El tiempo en pausa es lo que permite separar lo trabajado de lo parado, que es
  justo lo que se pidió al añadir las pausas. Una tarea rechazada deja ese cálculo incompleto sin
  que nada lo indique. Y como el rechazo tampoco mira el estado (ver HAL-35), la tarea rechazada
  se puede además reanudar, lo que reabre una pausa sobre otra.
- **Casos.** TSK-15-13, cubierto en la suite como fallo esperado. TSK-08-21 —reanudar una tarea
  rechazada— queda pendiente de probar.

## HAL-36 · La política de terminación se guarda y no la lee nadie · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Con `all_assigned_workers`, completar cierra la parte de quien completa y la tarea sigue en curso hasta el último; quien cierra desde la gestión sin estar asignado cierra la tarea entera. TSK-11-44 en verde.
- **Observado.** Una tarea con `config.completionPolicy: "all_assigned_workers"` asignada a dos
  personas queda **entera en `completed`** en cuanto la completa la primera. La asignación de la
  segunda no cambia, y nadie le dice que su parte sigue pendiente. Medido en desarrollo el
  2026-09-12.
- **Dónde.** `services/tasks/src/interfaces/http/task/task.helpers.ts:334` la normaliza y la
  guarda. En todo el repositorio el nombre aparece **dos veces**: ahí y en la definición del tipo
  (`domain/entities/Task.ts:29`). Ningún controlador la lee.
- **Efecto.** El ajuste existe en el alta, se guarda, se devuelve en la ficha y el panel puede
  enseñarlo: todo indica que está en vigor. Donde más se nota es al asignar una tarea a una
  sucursal entera —el reparto de un turno, un inventario— porque **basta uno de treinta** para
  darla por terminada, y los otros veintinueve desaparecen de la lista de pendientes sin haber
  hecho nada.
- **Casos.** TSK-11-44, cubierto en la suite como fallo esperado, con la comprobación de que la
  política **sí se guardó** antes del indulto: sin esa línea, el caso no distinguiría «no se
  aplica» de «no se guardó».

## HAL-35 · Las tareas no tienen máquina de estados: se mira el destino, nunca el origen · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Tabla de transiciones origen → destino en el controlador de estado: salir de un estado sellado es reabrir, y reabrir es de gestión; reabrir retira también validación y rechazo; rechazar exige trabajo en curso, completado o validado, y retira la validación. TSK-11-30, TSK-11-65 y TSK-15-14 en verde.
- **Observado.** Dos cosas, la misma causa:
  1. Un trabajador asignado devuelve a `in_progress` una tarea que la empresa ya **validó**, él
     solo, con un `PATCH /status`. Desde ahí puede completarla otra vez, lo que reescribe
     `completedAt` y `completedBy`, con el acta de validación todavía en pie.
  2. Reabrir una tarea validada a `assigned` —esto sí lo hace el propietario, y está bien que
     pueda— limpia `startedAt`, `completedAt`, `completedBy`, los campos de cancelación y los
     contadores de pausa, y **conserva `validatedAt` y `validatedBy`**. La tarea queda pendiente
     y firmada a la vez.
  3. Y lo mismo por la otra puerta: **rechazar una tarea ya validada responde 200** y la deja en
     `rejected` sin retirar `validatedAt` ni `validatedBy`. En el expediente quedan dos actas
     contradictorias —una validación y un rechazo— y la tarea sigue diciendo que se dio por
     buena. `rejectTask` no mira el estado de origen en ningún momento, mientras que validar sí
     exige `completed` y lo comprueba antes que nada.
  Medido en desarrollo el 2026-09-12.
- **Dónde.** `services/tasks/src/interfaces/http/task/updateTaskStatus.controller.ts`. El
  controlador decide qué escribir según el estado **de destino** (`:104-167`) y no consulta
  `task.status` en ningún momento. El permiso para las dos transiciones de trabajador es
  `canOperateAssignedTask` (`:45`), que se cumple con figurar en la tarea. La lista de campos que
  se limpian al reabrir está escrita a mano en `:139-146`, y ahí no están los de validación.
- **Lo que lo hace invisible**, que es lo que lo convierte en hallazgo y no en nota: el endpoint
  **sí** comprueba el destino y rechaza `validated`, `rejected` o cualquier palabra que no
  contemple con `400 Unsupported status transition` (`:165-167`). Quien lo prueba a mano escribe
  un estado inventado, recibe el rechazo y concluye que las transiciones están controladas. No
  hay una máquina de estados: hay una lista de destinos permitidos.
- **Y el contraste que lo remata.** El mismo trabajador, sobre la misma tarea validada,
  intentando también volver atrás, **sí recibe un 403** si el estado que pide es `assigned`: esa
  rama está protegida con `canManageTask` (`:133-135`). La protección existe y está escrita; lo
  que no hay es una regla que la aplique a todas las vueltas atrás. Quien lea el código por la
  rama de `assigned` se llevará la impresión de que las reaperturas están controladas. Cubierto
  en verde como TSK-11-64, al lado del caso que falla, porque por separado ninguno de los dos
  cuenta la historia.
- **Efecto.** La validación es la firma de la empresa sobre el trabajo hecho, y cualquiera de los
  asignados puede dejarla sin efecto sin que nadie la retire. El informe de tareas lee
  `validatedAt`, así que una tarea reabierta sigue contando como validada.
- **Casos.** TSK-11-30, TSK-11-65 y TSK-15-14, cubiertos en la suite como fallos esperados;
  TSK-11-08 y TSK-11-64 cubren en verde las dos mitades que sí funcionan —el rechazo del destino
  y el permiso de la reapertura— porque son las que engañan.
- **Aparte, y sin declararlo defecto:** una tarea `assigned` se completa sin haber pasado nunca
  por `in_progress` (TSK-11-47), y queda con `completedAt` y sin `startedAt`. Puede ser
  deliberado —marcar hecho algo que se hizo sin la app es un caso real—, así que la suite lo
  prueba en verde para dejar escrito qué guarda el sistema cuando ocurre: una tarea terminada
  cuya duración no existe.

## HAL-34 · Corregir la hora de un fichaje no cambia el informe legal · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. El `ON CONFLICT DO UPDATE` del espejo refresca todas las columnas salvo la clave. INF-03-02 en verde: la jornada corregida aparece en el informe. Queda reconstruir los informes diarios de los días con correcciones anteriores y reinyectar esos fichajes, si los hay.
El hermano silencioso de HAL-33, y peor de ver: allí no llegaba nada, aquí llega **casi** todo.

- **Observado.** Una entrada se corrige de `16:35:45` a `12:35:46` por el camino bueno —propuesta
  del propietario, firma del empleado, `200` en las dos—. En Firestore el documento queda con la
  hora nueva. En `checklogs_raw`, la columna `timestamp` **sigue siendo la vieja**, y con ella
  `real_date_market`. La fila sí se reescribió —su `updated_at` es posterior a la corrección—:
  lo que no cambió fueron esas dos columnas. Medido en desarrollo el 2026-09-12, comparando el
  documento de Firestore con su fila.
- **Dónde.** `services/sync/src/interfaces/sync.router.ts:91-106`. El `ON CONFLICT (id) DO UPDATE`
  enumera las columnas que se refrescan —`status`, `closed`, `is_suspect`, `failed_code`,
  `adjusted_timestamp`, `distance`, `metadata_raw`…— y **`timestamp` y `real_date_market` no
  están en la lista**. En un `INSERT … ON CONFLICT`, lo que no se enumera se queda como estaba.
- **El detalle que lo prueba sin lugar a dudas.** La hora corregida **está dentro de esa misma
  fila**: `metadata_raw` sí se actualiza, y lleva el historial entero de la corrección con
  `"timestamp": "2026-09-12T12:35:46.588Z"` al lado de un `timestamp` de columna que dice
  `16:35:45.985`. El dato viajó; no aterrizó donde alguien lo lee.
- **Efecto, que es el de verdad grave.** Todo lo que se calcula aguas abajo lee la columna:
  `BuildEmployeeDailyReports` selecciona por `real_date_market` y mide por `timestamp`
  (`:38-43`), y `BuildBranchEffect`, `BuildBranchRisk` y `BuildOperatingCost` filtran por
  `timestamp`. Ninguno mira `adjusted_timestamp` —la única columna de tiempo que sí se refresca—
  ni `metadata_raw`. Así que **el registro de jornada, el que tiene valor legal, conserva para
  siempre la hora equivocada**, y con ella los informes diarios y las series de analítica. La
  corrección con doble firma es justo el mecanismo que la ley da para enmendar un registro mal
  tomado: existe, se ejecuta, se firma, y no llega a donde importa.
- **Lo que lo hace invisible.** El panel lee Firestore, así que enseña la hora corregida y todo
  parece en orden. Solo discrepa Postgres, que es lo que nadie mira y lo que sostiene el informe.
  Las dos respuestas son `200`, no hay ningún error en ningún registro, y `sync_log` anota la
  sincronización como `success` —porque lo fue: la petición entró y se escribió—.
- **Casos.** INF-03-02, cubierto en la suite como fallo esperado, con la aserción de la hora
  antes del indulto para que el día que se arregle avise en vez de seguir en verde.
- **La lección.** Un `ON CONFLICT DO UPDATE` con la lista de columnas escrita a mano es una lista
  que envejece: cada columna nueva —y cada columna que pasa a ser mutable— hay que acordarse de
  añadirla, y olvidarse no rompe nada visible. Aquí la corrección de una hora tenía que haber
  entrado en esa lista el día que se escribió el flujo de correcciones.

## HAL-33 · ~~El espejo de Postgres llevaba semanas vacío y nadie se enteró~~ · CORREGIDO en desarrollo

**Es el hallazgo que justifica la forma de toda la suite**, así que va con su historia entera.

- **Observado.** Las ocho tablas de la tubería de analítica en desarrollo, a cero:
  `checklogs_raw`, `sync_log`, `employee_daily_reports`, `pattern_snapshots`, `task_ratings_raw`,
  `dim_branches`, `dim_employees` y `dim_calendars`. Ni una fila. La suite llevaba el día entero
  creando fichajes —cientos— y ninguno había llegado. Medido el 2026-09-12.
- **Por qué.** El fichaje lo escribe el contenedor en Firestore; de ahí lo copia a Postgres el
  trigger `onChecklogSync` (repo del SAAS), que hace un POST a `ANALYTICS_SERVER_URL`. Esa
  variable seguía valiendo `http://141.95.47.135:8080` — **la máquina de producción, en el
  puerto que se cerró con la mudanza de servidor del 12 de septiembre**. Cada fichaje lo
  intentaba y fallaba:
  ```
  [SyncChecklog] analytics sync failed { checklogId: '…', error: 'connect EHOSTUNREACH 141.95.47.135:8080' }
  ```
- **Lo que lo hizo invisible**, que es lo importante:
  1. El fichaje respondía **201**, y con razón: el fichaje se guardó. Lo que no ocurrió fue la
     consecuencia.
  2. El error se traga en un `console.error` dentro del trigger (`onChecklogSync.ts:14-22`).
     **No hay reintentos**: lo que no entra en el momento no entra nunca, ni cuando el servidor
     vuelve.
  3. Todo lo que lee de esas tablas —el registro de jornada legal, el panel operativo, las
     horas planificadas, el geocumplimiento, las series de Merlin— seguía respondiendo 200 con
     cuerpos bien formados. Sobre nada.
  4. La variable vive en `functions/.env.dev-encodebiz`, que **está en `.gitignore`**. No se ve
     en ninguna revisión de código y puede ser distinta en cada máquina.
- **Corregido** el 2026-09-12: se apuntó la variable a `https://api-staging.checkbiz360.com` y
  se redesplegaron a `dev-encodebiz` las cuatro funciones que la usan (`onChecklogSync`,
  `onTaskRatingSync`, `onBranchPatternSync`, `onEmpPatternSync`). Comprobado con un fichaje
  nuevo: la fila aparece en `checklogs_raw` en segundos. **Producción no estaba afectada** —su
  endpoint apunta a su propia máquina—, confirmado por producto.
- **Lo que no se recupera.** Los fichajes de las semanas anteriores no van a llegar solos: el
  trigger solo se redispara si alguien vuelve a escribir el documento. Para el histórico hace
  falta una reinyección deliberada.
- **Cubierto en la suite** por INF-03-01 (`45-espejo-y-programadas.spec.ts`), que cierra una
  jornada, fuerza el constructor diario y exige que aparezca **la jornada de esta empresa** —no
  un recuento global, que saldría verde con la cadena rota para nosotros—. El mensaje del rojo
  nombra el trigger, el fichero de la variable y el comando de los registros.
- **La lección, que vale para el resto de la tubería.** Un efecto que nadie mira es un efecto
  que no ocurre. Donde el fallo no puede verse desde la respuesta —un listener, un trigger, una
  cola, un correo— hace falta una prueba cuyo único trabajo sea decir «esto sigue llegando».
- **Y una pregunta de diseño que queda abierta:** el fichaje lo escribe el contenedor, que ya
  tiene la conexión a Postgres a mano; el rodeo por Firestore y Cloud Functions para volver al
  mismo contenedor es herencia de cuando todo vivía en funciones. Lo único que hoy lo justifica
  es que `sanitizerChecklog` —la programada que cierra jornadas incompletas— sigue escribiendo
  en Firestore desde fuera del contenedor. Alternativa mejor que las dos: el contenedor ya
  publica eventos por una cola **con reintentos y rescate**; el espejo podría ser un consumidor
  más de esa cola.

## HAL-32 · Cualquier cuenta genera el informe de otra empresa, y se lo deja en su histórico · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Generar exige lo mismo que descargar: `canWrite` en `/generate` y `/tasks`. INF-02-11 en verde, comprobando además que el histórico ajeno no crece. INF-01-14 sigue pendiente de datos.
- **Observado.** Con el token de un usuario de **otra** empresa, `POST /api/reports/tasks` sobre
  el `entityId` ajeno responde `201`, genera el fichero y **deja el documento en el histórico de
  la empresa víctima** (`entities/{ajena}/reports/{id}`), a nombre de su entidad. Medido el
  2026-09-12 contra desarrollo, comprobando el histórico antes y después.
- **Dónde.** `services/reports/src/interfaces/report.router.ts:50` — `requireFirebaseAuth` y
  nada más. Lo mismo en `:24` para `POST /api/reports/generate`, el de asistencia.
- **La asimetría es lo que lo convierte en defecto y no en decisión.** En el **mismo fichero**,
  cincuenta líneas más abajo, la descarga sí comprueba la pertenencia:
  `reportRouter.get("/:reportId/download", requireFirebaseAuth, …)` con `canWrite(uid, entityId)`
  (`:115`), y responde `403 report/unauthorized`. Las dos cosas se miden en pruebas contiguas:
  la descarga en verde, la generación en rojo.
- **Efecto.** Con solo el `entityId` —que viaja en URLs del panel— cualquier cuenta autenticada
  obtiene la respuesta con el **nombre de la empresa, de sus centros y de sus empleados**, y le
  ensucia el histórico de informes con ficheros que su dueño no pidió. En el de asistencia, que
  es el registro de jornada con valor legal, se suma que **se emite `report.generated` hacia los
  webhooks salientes de la víctima** (`report.router.ts:29`): un tercero puede provocar
  notificaciones en los sistemas de otro.
- **Lo barato.** Es la misma llamada a `canWrite` que ya está escrita unas líneas más abajo.
- **Casos.** INF-02-11, cubierto en la suite como fallo esperado, con INF-05-08 al lado en verde
  como contraste. Su gemelo INF-01-14 (el de asistencia) necesita datos precalculados para
  demostrarse y queda pendiente.

## HAL-31 · ~~La función vieja y el contenedor procesaban los mismos eventos de Stripe~~ · CORREGIDO en desarrollo

**Estado.** En **producción no llegó a ocurrir**: el endpoint de la función (`Event Handler
Prod`) ya estaba **Deshabilitado**, comprobado por producto en el panel de Stripe el
2026-09-12 — solo recibe `https://api.checkbiz360.com/api/v1/billing/webhook`. Lo que estaba
mal era **desarrollo**, donde el endpoint equivalente seguía habilitado; se desactivó el
2026-09-12 y ahora las dos cuentas están igual. Se conserva el hallazgo entero porque describe
una cadena que sigue existiendo en el código y que se rearma con una casilla: los dos endpoints
siguen dados de alta, solo que apagados, y con sus eventos configurados.

**Alcance de lo medido**: modo de **pruebas** de la cuenta de Stripe; el endpoint de más
apuntaba a la Cloud Function del proyecto **de desarrollo** (`dev-encodebiz`, desplegada el
2026-08-23, URL terminada en `3bnjgtprva`; la de producción termina en `jxvyznhhja`).

Tres hechos encadenados, medidos el 2026-09-12 al cobrar el final de un periodo de prueba. Por
separado son molestos; juntos forman una cadena que termina en una segunda factura al mismo
cliente, y lo único que la cortaba era que un documento salía mal formado.

**1. La Cloud Function retirada sigue suscrita a los eventos de Stripe.** En la cuenta de
pruebas hay dos endpoints activos: el del contenedor
(`https://api-staging.checkbiz360.com/api/v1/billing/webhook`) y el de la función
(`apiv100-firebaseentryhttp-stripewebhook-3bnjgtprva-uc.a.run.app`, que es la URL de
`apiV100-firebaseEntryHttp-stripeWebhook` en `dev-encodebiz`), y este último conserva
`invoice.paid`, `invoice.upcoming`, `payment_method.attached` y
`customer.subscription.created`. Los dos procesan el mismo evento.

**2. Esa función crea documentos que el contenedor decidió no crear.** Tras cobrar, la empresa
tenía dos documentos en `entities/{entityId}/invoices/{stripeInvoiceId}` —uno por la factura de
0,00 € del inicio de la prueba y otro por la de 28,00 €— con la **factura entera de Stripe**
dentro de `paymentData`: unos cuarenta campos, incluidos `invoice_pdf` y `hosted_invoice_url`,
que son enlaces que abren la factura sin pedir credencial. El contenedor guarda tres campos
(`number`, `total`, `status`) y **solo sobre un ciclo que ya exista**: `markInvoice` hace
`update`, nunca crea. La función hace `set(merge)`, que crea.

**3. Crear ese documento enciende un procesador cuyo siguiente paso es emitir otra factura.**
`processInvoices` está **desplegada en desarrollo** (comprobado con `functions:list`) y escucha
`onDocumentCreated /entities/{eid}/invoices/{iid}`. Su trabajo es `InvoicePaymentProcessor`, que
cuenta lo facturable y, si hay algo, llama a `makeInvoice` contra Stripe — una factura nueva
para el mismo cliente.

**Por qué no llegó a cobrarse dos veces, que es lo que hay que mirar.** El procesador se
ejecutó —tres veces hoy, a las 14:55, 15:02 y 15:20— y murió en la primera lectura:

```
[onCreateInvoice] Nueva invoice undefined para entity undefined
[onCreateInvoice] Error procesando undefined
Error: Value for argument "documentPath" is not a valid resource path.
```

El documento que la función escribe no lleva `entityId` ni `id`, así que `findById(undefined)`
lanza antes de llegar a Stripe. **Lo que separa hoy a un cliente de una segunda factura es que
el documento esté mal formado**, no una comprobación. Y el error lo traga un `catch` que
registra y sale, así que no lo ve nadie.

- **Dónde.** `saas:functions/src/core/subscriptions/infrastructure/FirestoreSubscriptionRepository.ts:118-122`
  (`set(merge)` que crea); `saas:functions/src/firebase-firestore-trigger/subscriptions/processInvoices.ts`
  (el trigger); `saas:functions/src/core/subscriptions/application/InvoicePaymentProcessor.ts:63-70`
  (`makeInvoice`); y en el otro lado `api:services/billing/src/application/StripeWebhookHandler.ts:123-149`,
  cuyo comentario dice explícitamente que no crea documentos ahí porque «crear uno ahí era lo
  que disparaba el procesador y podía encadenar facturas nuevas». La precaución del contenedor
  existe; lo que la anula es la función que sigue viva.
- **Efecto inmediato en desarrollo.** El historial de facturación de una empresa tiene
  documentos que el contenedor no escribió, con el objeto completo de Stripe y sus enlaces
  dentro. Con las reglas de Firestore de desarrollo abiertas hasta 2030, ese contenido es
  legible por cualquiera.
- **Cómo se cortó.** Desactivando el endpoint viejo en Stripe, que es una casilla y corta los
  tres puntos de golpe. **Desactivado y no borrado a propósito**: al borrar un endpoint, Stripe
  se lleva su secreto de firma, y la función conserva el suyo en `STRIPE_WEBHOOK_SECRET_TEST`;
  si algún día hay que volver a ella como rollback, desactivado se revierte con una llamada y
  borrado no.
- **Lo que queda vivo, y por eso el hallazgo no se borra.** `processInvoices` **sigue
  desplegada** en desarrollo, escuchando `onDocumentCreated /entities/{eid}/invoices/{iid}`.
  Ahora mismo no la despierta nadie porque el contenedor no crea ahí; pero la precaución del
  contenedor **depende de que nadie más escriba en esa colección**, y eso no se ve leyendo su
  código. Lo guarda FAC-07-09, en verde: si alguna vez vuelve a aparecer un documento ahí, esa
  prueba se pone roja.
- **Casos.** FAC-07-09, en la suite y en verde desde que se desactivó el endpoint. Relacionado
  con HAL-02, el mismo patrón —función y contenedor procesando el mismo evento— en los
  fichajes, que sigue abierto.

## HAL-30 · A quien trabaja en otro huso se le busca el turno del día equivocado · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. El día y las horas se miran en la misma zona —la del empleado remoto o la de la sucursal—, pasada al resolutor como `tzHint`. CHK-08-70 en verde en sus dos mitades.
- **Observado.** Un empleado con `enableRemoteWork` y zona propia a trece horas de su centro.
  El calendario tiene abierto **su** día, con un turno alrededor de **su** hora, y cerrado el
  del centro. El fichaje responde `400 checklog/day_disabled`. Medido en desarrollo el
  2026-09-12: en su casa era `sunday 2026-09-13` y en el calendario `saturday 2026-09-12`.
- **Y a la vez**, en la misma configuración, las **horas** sí se comparan en su zona: un turno
  puesto a su hora local le deja fichar aunque en el centro sea una hora completamente
  distinta, y el fichaje queda con `metadata.tz` igual a su zona. Las dos cosas se miden en
  pruebas contiguas, una en verde y otra en rojo.
- **Dónde.** `createChecklog.controller.ts` llama a `resolveDay.execute({entityId, branchId,
  employeeId})` **sin `tzHint`**, así que el día, la fecha local y los festivos se resuelven
  con la zona del calendario (`resolveEffectiveDay.usecase.ts:77-88`). Unas líneas después el
  mismo controlador calcula `tz` con la zona del empleado remoto y compara las horas del turno
  contra `DateTime.now().setZone(tz)`. Dos zonas para una sola decisión.
- **Por qué no es un caso de laboratorio.** No hace falta cruzar la línea de cambio de fecha:
  basta con cualquier diferencia horaria que ponga a las dos partes en días distintos —el
  fichaje de madrugada de alguien en América con la empresa en España, o el de última hora de
  alguien en Asia—. Con turnos de lunes a viernes, el lunes de uno es el domingo del otro.
- **Efecto.** La persona no puede fichar el día que le toca, y sí puede el día que no. El
  rechazo dice «día deshabilitado», que es cierto para el calendario y falso para quien está
  delante del móvil: no hay forma de deducir la causa desde la app. Y el arreglo no es
  evidente —hay que decidir si el día de un trabajador remoto es el suyo o el de su empresa—,
  lo que lo hace más importante de anotar, no menos.
- **Casos.** CHK-08-70, cubierto en la suite en dos pruebas: las horas en verde, el día como
  fallo esperado. Ya estaba anotado como sospecha en la ficha de CHK-08.

## HAL-29 · Quien está de vacaciones ficha igual: el fichaje no lee las ausencias · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. El fichaje lee las ausencias del calendario de empleado y responde `400 checklog/absence` con el detalle de la ausencia. CHK-08-28 en verde. La app no reconoce el código nuevo y mostrará el mensaje genérico hasta que se añada.
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

## HAL-28 · Un descanso se engancha a la jornada de otro día y le cambia las horas · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. El descanso y la salida cuelgan de la jornada abierta —la del último fichaje válido— y una jornada no se parte entre centros: `checklog/different_branches` también para los descansos. CHK-08-59 en verde; CHK-08-58 pasa a esperar ese mismo código.
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

## HAL-27 · Desactivar a un colaborador le quita el panel pero no le quita el fichaje · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. `canWrite` exige `status:"active"`; un asiento sin el campo se lee como activo. CHK-08-77 en verde.
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

## HAL-26 · El panel pide la hora del fichaje, la valida, y el servidor la tira · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Por la vía de administrador la hora del cuerpo es la del registro, validada como no futura; el día se resuelve para esa fecha y la secuencia se encadena con lo anterior a esa hora. La marca de creación conserva la hora del reloj. CHK-08-74 en verde.
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

## HAL-25 · La edición de una ficha acepta cualquier campo, incluida la lista de dispositivos · CORREGIDO en desarrollo

- **Precisión (2026-09-13).** El impacto sobre los dispositivos de confianza que se describe abajo no se sostenía: la comprobación del fichaje lee la subcolección `employees/{id}/security/trustedDevicesId` (`findSecurity`), y el campo que esta ruta dejaba en el documento era inerte. Lo que sí era cierto es la ausencia de lista blanca, y eso es lo corregido.
- **Corregido.** El 2026-09-14, en desarrollo. La edición de ficha tiene lista de campos editables; las credenciales y el rastro del sistema (`trustedDevicesId`, `twoFA`, `customToken`, `devices`) se rechazan con `400 employee/bad_request`, y lo que no está en la lista se descarta. `price`, `responsibility` y `job` se toleran porque el panel siempre los ha mandado. EMP-04-12 en verde.
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

## HAL-24 · Editar un centro le reactiva la geocerca, y borrarlo deja gente apuntando a él · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. La edición es parcial y `disableRatioChecklog` no se rellena cuando falta; borrar comprueba que el centro exista (`404 branch/not_found`) y retira su id de la lista de cada ficha. SUC-02-04, SUC-04-03 y SUC-04-05 en verde. SUC-02-04 leía el centro por un listado que el servicio no tiene; ahora lee la ficha guardada, que es como lo hace el panel.
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

## HAL-23 · Modificar una responsabilidad la inventa, y un puesto sin precio guarda NaN · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-14, en desarrollo. La edición comprueba que la responsabilidad exista (`404 responsibility/not_found`) y exige el precio del puesto como número, igual que el alta; el `set` con merge tampoco se dejaba sin `await`. EMP-10-04 y EMP-10-06 en verde.
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

## HAL-22 · Sin horario configurado, la app se rompe pero el fichaje funciona · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-14, en desarrollo. Sin horario configurado, `GET /calendar` devuelve el mismo día abierto que aplica el fichaje, con `code: "calendar/default"`, `configured: false` y `sources` vacío, en vez del 404. El constructor del día por defecto vive ahora en shared (`calendar/defaultDay.ts`) para que fichaje y lectura digan lo mismo. CHK-11-18 en verde.
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

## HAL-21 · Un administrador se hace propietario, y de paso aparta al que lo era · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. Conceder y modificar reciben quién llama, como ya hacía el borrado: lo que afecta a un propietario —darle el asiento, tocarle el rol o el estado— lo hace otro propietario (`owner_required`). COL-04-02, COL-04-03 y COL-02-04 en verde. Sigue dependiendo de cerrar las reglas de Firestore: mientras el panel pueda escribir `user_entity_roles` desde el navegador, se rodea.
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

## HAL-20 · checkinbiz se activa sin método de pago · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-13, en desarrollo. `isConfigured` exige método de pago en todos los servicios; de paso, `payment_method?.length !== 0` daba por bueno un método ausente. FAC-03-17 en verde. Falta que el panel pida la tarjeta antes de activar: hoy recibirá `entity_not_configured` sin explicar qué falta.
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

## HAL-19 · El importe a cobrar depende de un aviso previo, y nadie comprueba que llegara · CORREGIDO en desarrollo, falta un evento en Stripe

- **Corregido.** El 2026-09-13, en desarrollo. En `invoice.created` se corrigen las unidades del borrador si no cuadran con la plantilla (`invoices.updateLines`), y en `invoice.finalized` se audita lo emitido: una discrepancia queda en el registro con `[billing][ALERTA]` y en la suscripción (`billingAlert`). Falta suscribir `invoice.created` en el webhook de Stripe de desarrollo (el cambio de configuración lo bloqueó el clasificador) y en el de producción en su pase; sin ese evento solo actúa la auditoría.
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

## HAL-18 · Desarrollo se quedó sordo a Stripe tras la mudanza de servidor · CORREGIDO en desarrollo

- **Corregido.** Ya estaba resuelto cuando se escribió el triaje del 2026-09-13: la medición de HAL-19 del 2026-09-12 —aviso previo a los 21 s, factura a los 138 s— solo es posible con el webhook apuntando a staging, y el segundo webhook lo desactivó HAL-31 ese mismo día. Se marca ahora.
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

## HAL-17 · Apagar la semana entera abre el fichaje en vez de cerrarlo · CORREGIDO en desarrollo

- **Corregido.** El 2026-09-14, en desarrollo. El respaldo abierto de 00:00 a 23:59 es solo para quien no ha configurado ninguna semana —sin calendario o sin `weeklySchedule`—; una semana definida con los siete días apagados cierra el día. CHK-08-31 pasa a afirmar el `400 checklog/day_disabled`.
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
confirmarlas; cada una se verificará al escribir su prueba. Revisada el 2026-09-14: tres de
las seis ya se confirmaron y corrigieron como hallazgos, y se tachan aquí.

- **Estado del empleado nunca comprobado.** Al fichar, respondido de rebote por la corrección
  CHK-08-23 (más abajo): el despedido no ficha porque la baja le retira las responsabilidades, no
  porque se mire el `status`. Queda por comprobar en tareas, y el caso de una ficha que llegue a
  `inactive` o `vacation` por otra vía conservando responsabilidades.
- ~~**Escalada de rol en colaboradores.**~~ Confirmada y corregida: es **HAL-21**.
- **Borrado de empresa sin permiso.** Sigue en Cloud Functions y, según el análisis, no comprueba
  permisos ni cascada (catálogo ENT).
- ~~**`isAdmin` como texto en el fichaje.**~~ Confirmada y corregida: es **HAL-16**.
- **Consulta de suscripciones sin filtrar por entidad** (catálogo FAC). ~~Generación de informes~~
  confirmada y corregida: es **HAL-32**.
- **Doble correo de «servicio activado»** al suscribir (catálogo de listeners).

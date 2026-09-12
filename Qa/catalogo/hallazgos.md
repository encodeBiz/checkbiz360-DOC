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

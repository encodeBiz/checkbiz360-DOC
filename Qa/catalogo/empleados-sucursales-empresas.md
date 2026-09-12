# Catálogo de casos de uso — Empleados (EMP), Sucursales (SUC), Empresas (ENT), Colaboradores (COL)

> **Verificación (2026-09-11).** Catálogo obtenido por análisis estático del código de los
> servicios, del panel y de la app, cruzado con lo desplegado de verdad en `dev-encodebiz`.
> **Salvo lo que abajo se marque como confirmado, el resto es lectura del código, no
> comprobación contra el entorno.** Los hallazgos de este catálogo que ya se han verificado
> uno a uno están en [hallazgos.md](./hallazgos.md); las sospechas sin verificar se quedan
> como tales y se comprobarán al escribir su prueba. El resultado esperado de cada caso es lo
> que hace el código HOY, no lo que debería hacer.

Análisis estático del 2026-09-11 sobre `encodebiz-api` (rama `develop`), `encodeBiz-SAAS/functions`, `encodebiz-front-saas` (`.env.development`) y `checkbiz360`. Rutas tal como las sirve nginx de desarrollo (`nginx/nginx.staging.conf`, puerto 8080). No se ha ejecutado nada: todo lo que dice «sin confirmar» es un camino que el código no deja cerrado.

Abreviaturas de ficheros: `api:` = `encodebiz-api/`, `cf:` = `encodeBiz-SAAS/functions/src/`, `front:` = `encodebiz-front-saas/`, `app:` = `checkbiz360/`.

## Actores adicionales (además del vocabulario común)
- ADMIN_INVITADO: usuario con `user_entity_roles.role = "admin"` y `status = "invited"` en la entidad (invitado que aún no ha aceptado).
- ADMIN_DESACTIVADO: usuario con `user_entity_roles.role = "admin"` y `status = "disabled"`.
- CLAIM_ADMIN: cualquier usuario de Firebase cuyo ID token lleva la custom claim `admin: true` (la pone el segundo factor del panel), sea de la entidad que sea.
- STAFF_BO: personal del backoffice: ID token de Firebase cuyo uid figura activo en `backoffice_users`, con el permiso que pida la ruta (`api:services/backoffice/src/interfaces/http/middleware/requireStaff.ts:33-86`).
- STAFF_BO_SIN_PERMISO: STAFF_BO cuyo rol no incluye el permiso de la ruta.

## Hechos transversales que afectan a todos los bloques
- `requireFirebaseAuth` (`api:packages/shared/src/middleware/firebaseAuth.ts:4-21`) responde 401 `{error:"unauthenticated", message:"Missing Authorization header"}` sin cabecera, 401 `{error:"unauthenticated", message:"Invalid Authorization format"}` si no es `Bearer x`, y 401 `{error:"unauthenticated", message:<mensaje de Firebase>}` con token inválido. Verifica con `checkRevoked = true` (:15); las CF usaban `verifyIdToken` sin esa bandera (`cf:core/shared/utils/validateToken.ts:15`), así que un token revocado pero no caducado pasaba en la CF y aquí da 401.
- En la CF el cuerpo de auth fallida era `{message:"Invalid token", code:"auth/unauthorized" | "auth/invalid_token"}` (`cf:core/shared/utils/authError.ts` vía `authErrorToResponse`). En el contenedor, detrás de `requireFirebaseAuth`, es `{error:"unauthenticated", message}` **sin `code`**. Aplica a todos los endpoints de employees, branches y entities salvo los públicos.
- `canWrite(uid, entityId)` (`api:packages/shared/src/checkbiz/auth/canWrite.ts:10-49`) sin opciones solo mira `user_entity_roles/{uid}_{entityId}.role ∈ {owner, admin}` (:17-21). **No mira `status`**: un ADMIN_INVITADO o ADMIN_DESACTIVADO pasa. **No distingue propietario de administrador**. Los OP_* (responsabilidades por sucursal) nunca pasan porque ningún endpoint de esta parcela usa `includeBranchResponsibility`. Es idéntico al de la CF (`cf:core/auth/permissions/canWrite.ts:10-49`).
- Los errores no capturados en employees/branches/entities acaban en `express-async-errors` → 500 `{ok:false, error:"internal_error"}` (`api:services/employees/src/app.ts:39-42`, `branches/src/app.ts:20-23`, `entities/src/app.ts:39-42`).
- Firestore del contenedor se inicializa sin `ignoreUndefinedProperties` (`api:packages/shared/src/firebase.ts:4`, no hay `settings()`): cualquier `undefined` en una escritura tumba la escritura entera.
- Ningún servidor instala manejador de `unhandledRejection` (`api:services/employees/src/server.ts`, `entities/src/server.ts`); hay escrituras de Firestore sin `await` (responsabilidades). Si una de ellas rechaza, el comportamiento del proceso depende de la versión de Node (sin confirmar).
- El panel llama siempre a través de su proxy de servidor (`front:src/lib/http/serverBackendProxy.ts`): exige ID token válido para los handlers con `requiresAuth` (:570-581), reenvía solo `Authorization`, `locale`, `Content-Type` y `Cookie` (:595-601) —ni `Origin` ni `X-Forwarded-For`— y trata cualquier 3xx como error 502 (:613). El middleware `front:src/proxy.ts:89-95` exige además cookie de 2FA salvo en `recovery_pass`, `create_user` y los de 2FA.
- La CF `validateUserToken` (`cf:core/shared/utils/validateUserToken.ts:18-50`), usada por entity/users/media/update-auth, exigía las claims `admin` y `twoFA` **solo si `Origin` es uno de los orígenes del panel** (:35-47). El contenedor no mira claims. Como el proxy del panel no reenvía `Origin`, en la práctica no debería notarse (sin confirmar que `fetch` de Node no ponga `Origin` por su cuenta).

## Fuera de HTTP (no son endpoints, pero tocan colaboradores y conviene saberlo al diseñar pruebas)
- **Aceptar una invitación** no pasa por ningún endpoint: el panel escribe `user_entity_roles/{id}.status = "active"` directamente desde el navegador (`front:src/services/core/entity.service.ts:64-81`, llamado desde `front:src/components/common/modals/WelcomeInvite.tsx:48` y `front:src/app/layouts/AdminLayout.tsx:75`). También escribe `isActive` desde el navegador (`entity.service.ts:84-101`). La ruta que sustituye a la CF `updateAuth` (COL-04) no la usa nadie del panel.
- **La puesta en marcha de merlin** escribe `user_entity_roles` directamente, sin pasar por el núcleo (`api:services/merlin/src/soporte/puesta-en-marcha/application/sembrar.ts:356-394`). Solo la invoca un CLI (`.../demo/sad/montar.cli.ts:99`); ninguna ruta HTTP llama a `sembrar`.
- **Las importaciones de rentman** crean empleados con el mismo `createEmployee` de shared, sin HTTP de esta parcela.

---

# EMP — Empleados (`services/employees`, puerto 3013)

## POST /api/v1/employees/validate  ·  EMP-01
- Servicio: employees, `api:services/employees/src/interfaces/http/employeePublic.router.ts:13-33`, montado antes del auth en `app.ts:22`; lógica en `api:packages/shared/src/checkbiz/employees/validateEmployee.ts:28-71`.
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_VALIDATE_EMPLOYEE`, `front:.env.development:59`; `front:src/services/checkinbiz/employee.service.ts:362` vía proxy `checkinbiz_validate_employee`, que exige ID token aunque el endpoint sea público, `serverBackendProxy.ts:223-227`) / app: no (la app valida contra `/api/v1/checkinbiz/auth/validate`, `app:lib/core/constants/app_constants.dart:51-52`).
- Origen: portado desde la CF `cf:services-saas/checkinbiz/firebase-checkinbiz-http/validate-employee.ts` (controlador `.../interfaces/http/validateEmployee.controller.ts:7-90`).
- Diferencias con la CF: (1) la CF respondía los errores con `res.send(JSON.stringify(...))` —`Content-Type` no JSON— y el contenedor con JSON; (2) el campo `message` de error cambia: la CF ponía `"Invalid payload"` / `"Employee not found"` y el detalle en `errors`; el contenedor pone el detalle también en `message` (`"Token is required"`, `"Token is not valid Base64 or JSON"`, `"Token is incomplete or malformed"`, `"Employee does not exist or does not belong to the entity"`); `code` y `errors` coinciden; (3) el 500 de la CF era `{message:"Internal server error", code:"staff/internal_error", errors}` y el del contenedor `{ok:false, error:"internal_error"}`.
- Autenticación: ninguna. El «token» es JSON en base64 sin firmar `{employeeId, entityId}` (validateEmployee.ts:10-11, :35).
- Autorización: ninguna. Cualquiera que conozca `employeeId` y `entityId` obtiene la sesión.
- Entrada: cuerpo `{token}` obligatorio.
- Respuesta correcta: 200 `{message:"Employee validated successfully", payload:{name, twoFa, entityId, employeeId, biometricRequired}, sessionToken, expiresAt:null, branchId:[...]}`. `sessionToken` es un JWT `{employeeId, entityId}` firmado con `JWT_2FA_SECRET`, **sin caducidad** (validateEmployee.ts:68). `twoFa` es `true` si el empleado tiene `enableA2F === false`; si no, `Boolean(security/twoFA.verifiedAt)` (:55, :63). `branchId` = `scope.branchId` de sus responsabilidades activas (:69).
- Efectos: ninguno (solo lecturas).
- Criticidad: alta — es la puerta que emite la sesión de empleado (EMP_JWT).
- Casos:
  - EMP-01-01 · ANON · token base64 de `{employeeId, entityId}` de un empleado `active` → 200 con `sessionToken` y `payload`.
  - EMP-01-02 · ANON · empleado con `enableA2F:false` → 200, `payload.twoFa = true`.
  - EMP-01-03 · ANON · empleado con 2FA activo y sin `security/twoFA.verifiedAt` → 200, `payload.twoFa = false`.
  - EMP-01-04 · ANON · empleado sin responsabilidades activas → 200, `branchId: []`.
  - EMP-01-05 · ANON · cuerpo sin `token` → 400 `{code:"employee/invalid_payload", message:"Token is required", errors:[...]}`.
  - EMP-01-06 · ANON · `token` que no decodifica a JSON → 400 `code:"staff/invalid_payload"`.
  - EMP-01-07 · ANON · JSON sin `employeeId` o sin `entityId` → 400 `code:"employee/invalid_payload"` («Token is incomplete or malformed»).
  - EMP-01-08 · ANON · `employeeId` inexistente o de otra entidad → 404 `code:"employee/not_found"`.
  - EMP-01-09 · ANON · token = base64 de `null` → `JSON.parse` devuelve `null` y la desestructuración lanza → 500 `{ok:false, error:"internal_error"}` (validateEmployee.ts:35-40).
  - EMP-01-10 · EMP_INACTIVO (`status:"fired"`, baja blanda de EMP-06) → 200 con `sessionToken`: no se mira el estado.
  - EMP-01-11 · EMP_INACTIVO (`status:"inactive"` o `"sick_leave"`) → 200 con `sessionToken`.
  - EMP-01-12 · ANON vía panel · la llamada a través del proxy sin ID token → 403 `{code:"auth/forbidden"}` del proxy, no llega al servicio (serverBackendProxy.ts:571-581).
- Sospechas: el token no está firmado y solo lleva dos identificadores: quien conozca `employeeId` y `entityId` obtiene una sesión de empleado sin caducidad (la CF hacía lo mismo). Un empleado dado de baja (`fired`) sigue obteniendo sesión, porque la baja es blanda y aquí no se mira `status`.

## GET /api/v1/employees/export?entityId=  ·  EMP-02
- Servicio: employees, `api:services/employees/src/interfaces/http/employee.router.ts:327-347`; CSV en `api:packages/shared/src/checkbiz/employees/exportEmployees.ts:8-31`.
- Consumidores: ninguno detectado (no hay variable en `front:.env.development` ni referencias en `front:src`; tampoco en la app).
- Origen: portado desde la CF `cf:services-saas/checkinbiz/firebase-checkinbiz-http/employees-export.ts` (controlador `.../employee-export/downloadEmployeesCsv.controller.ts:25-54`).
- Diferencias con la CF: el nombre de fichero es `empleados-{entityId}.csv`; en la CF salía del caso de uso (sin confirmar si coincide). La CF envolvía todo error de auth en 401 `{success:false, ...}` (employees-export.ts:15-21); el contenedor da el 401 de `requireFirebaseAuth`. El contenido del CSV lo genera otra implementación (sin confirmar que columnas y orden coincidan con `BuildEmployeesCsv` de la CF).
- Autenticación: Firebase ID token (`requireFirebaseAuth`, app.ts:35).
- Autorización: `canWrite(uid del token, entityId)` (employee.router.ts:339-341). PROP y ADMIN pasan, ADMIN_INVITADO también.
- Entrada: query `entityId` obligatorio.
- Respuesta correcta: 200 `text/csv; charset=utf-8`, `Content-Disposition: attachment; filename="empleados-{entityId}.csv"`. Cabecera `Nombre,Email,Teléfono,Documento,Puesto,Rol,Estado,Centros`. Centros por nombre y separados por ` | `.
- Efectos: ninguno.
- Criticidad: baja — sin consumidor detectado.
- Casos:
  - EMP-02-01 · PROP · entidad con empleados → 200 CSV con una fila por empleado.
  - EMP-02-02 · ADMIN · ídem → 200.
  - EMP-02-03 · PROP · entidad con empleados `fired` → 200, y las fichas dadas de baja salen con `Estado = fired` (`findAll` no filtra, FirestoreEmployeeRepository.ts:86-90).
  - EMP-02-04 · PROP · entidad sin empleados → 200 con solo la cabecera.
  - EMP-02-05 · PROP · sin `entityId` → 400 `{error:"Invalid query parameters", details:["entityId is required"], code:"employee-export/bad_request"}`.
  - EMP-02-06 · OP_MANAGER · → 403 `{error:"Unauthorized access to this entity", code:"auth/unauthorized"}`.
  - EMP-02-07 · AJENO · `entityId` de otra entidad → 403 (mismo cuerpo).
  - EMP-02-08 · ANON → 401 `{error:"unauthenticated", message:"Missing Authorization header"}`.
  - EMP-02-09 · TOKEN_INVALIDO → 401 `{error:"unauthenticated"}`.
  - EMP-02-10 · PROP · un empleado con `branchId` guardado como cadena y no como array → `.map` lanza → 500 `internal_error` (exportEmployees.ts:27; sin confirmar que existan datos así).
- Sospechas: el volcado incluye a los dados de baja sin distinguirlo más que por la columna Estado.

## POST /api/v1/employees  ·  EMP-03
- Servicio: employees, `api:services/employees/src/interfaces/http/employee.router.ts:163-219` (ruta :350); reglas en `api:packages/shared/src/checkbiz/employees/manageEmployee.ts:39-101` y `employeeAccess.ts:22-92`.
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_CREATE_EMPLOYEE`, `front:.env.development:56`; `front:src/services/checkinbiz/employee.service.ts:188`, proxy `checkinbiz_create_employee`). El botón «reenviar credenciales» usa el mismo endpoint con `id` en el cuerpo.
- Origen: portado desde la CF `cf:services-saas/checkinbiz/firebase-checkinbiz-http/create-employee.ts` (controlador `.../createEmployee.controller.ts:114-147`, caso de uso `CreateEmployee.ts:15-23`, disparador `onCreateEmployee.controller.ts`).
- Diferencias con la CF:
  1. El acceso lo crea el contenedor **antes** de la ficha y la ficha nace con `uid` (manageEmployee.ts:57-65); el disparador `onCreateEmployee` se aparta por eso (`cf:.../onCreateEmployee.controller.ts:29`). En la CF la ficha nacía sin `uid` y era el disparador el que creaba el usuario de Auth (`emailVerified: true`, `displayName`, contraseña) y guardaba `uid` y `customToken` en la ficha (:63-85). Ahora el usuario nace con `emailVerified:false`, sin `displayName`, y la ficha **no guarda `customToken`**.
  2. El correo se normaliza (trim y minúsculas, manageEmployee.ts:43). Un correo con formato inválido da 400 `{ok:false, error:"invalid_email"}` (:44); la CF lo aceptaba y el fallo quedaba en el disparador, con 201 al cliente.
  3. Un fallo de Auth distinto de «ya existe» da 502 `{ok:false, error:"auth_error", detail}` (employee.router.ts:43, :208). En la CF el alta respondía 201 y el fallo quedaba en el disparador.
  4. La respuesta `employee` sale releída de Firestore (employee.router.ts:212), con `uid` y el correo en minúsculas.
  5. En el reenvío, si el envío falla el error es `"No se pudo reenviar el correo de bienvenida"` (:160); la CF devolvía el texto del proveedor. El estado (400) coincide.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, body.entityId)` **después** de validar el cuerpo (employee.router.ts:173). No distingue PROP de ADMIN.
- Entrada: obligatorios `fullName`, `role ∈ {internal, collaborator}` y `entityId`. `email` es opcional para el validador, pero en la práctica hace falta (ver casos). Opcionales: `enableA2F` y `biometricRequired` (booleanos; por defecto `true`), `metadata` (objeto), `phone` (por defecto `"-"`), `branchId` (por defecto `null`), `jobTitle`, `nationalId`, `enableRemoteWork` (por defecto `false`). `status` se ignora: siempre nace `active` (:134). Con `id` presente se reenvían credenciales en lugar de crear (:175-180).
- Respuesta correcta: 201 `{message:"Employee creado correctamente", code:"employee/created", employee:{...ficha con id y uid}}`. Reenvío: 200 `{message:"Employee creado correctamente", code:"employee/email_sent"}`.
- Efectos: (a) Firebase Auth: `getUserByEmail`; si no existe, `createUser({email, emailVerified:false})` (employeeAccess.ts:35-39). (b) Firestore: `entities/{entityId}/employees/{id}`, con `uid`, `createdAt` y `status:"active"` (FirestoreEmployeeRepository.ts:29-39). (c) `searchIndex/entities__{entityId}__employees__{id}` con nombre, correo y teléfono (manageEmployee.ts:72-74). (d) Contraseña de 6 dígitos puesta en el usuario de Auth, más enlace de restablecimiento y correo SMTP `WELLCOME_EMPLOYEE` con `customToken` base64 `{employeeId, entityId, fullName}` (employeeAccess.ts:61-86). (e) El disparador CF `onCreateEmployee` se ejecuta y sale sin hacer nada porque la ficha trae `uid`.
- Criticidad: alta — alta de plantilla, cupo del plan y acceso a la app.
- Casos:
  - EMP-03-01 · PROP · plan con cupo y correo nuevo en Auth → 201 `code:"employee/created"`; usuario de Auth creado, ficha con `uid`, entrada en `searchIndex` y correo de bienvenida.
  - EMP-03-02 · ADMIN · ídem → 201 (mismo trato que PROP).
  - EMP-03-03 · ADMIN_INVITADO · ídem → 201 (`canWrite` no mira `status`).
  - EMP-03-04 · PROP · plan sin `maxEmployees` (nulo o 0 = ilimitado) → 201.
  - EMP-03-05 · PROP · recuento de fichas ≥ `maxEmployees` → 403 `{code:"subscription/limit_off", message:"You cannot create a new employee: your plan’s quota has been reached."}`; no se crea usuario de Auth.
  - EMP-03-06 · PROP · cupo agotado solo por fichas `fired` → 403 `subscription/limit_off` (`countAll` cuenta todas, FirestoreEmployeeRepository.ts:92-96).
  - EMP-03-07 · PROP · entidad sin `subscriptions/checkinbiz`, sin `plan`, o con un plan que no existe en `service/checkinbiz/plan/{plan}` → 403 `subscription/limit_off` (subscriptionLimits.ts:29-46, :63-66).
  - EMP-03-08 · PROP · correo que ya tiene otra ficha de la entidad, incluida una `fired` → 400 `{error:"{\"message\":\"An employee with that email or phone number already exists.\",\"code\":\"employee/exist_employee\"}"}` (cadena JSON anidada).
  - EMP-03-09 · PROP · el mismo correo de una ficha existente pero con otras mayúsculas (`Juan@X.com` frente a `juan@x.com`) → la comprobación de duplicados, que usa el correo sin normalizar, no lo ve → 201 y queda una segunda ficha con el mismo correo y el mismo `uid`.
  - EMP-03-10 · PROP · correo que ya existe en Firebase Auth por ser usuario del panel o empleado de otra entidad → 201; se reutiliza su `uid` y **se cambia la contraseña de esa cuenta** al mandar la bienvenida (employeeAccess.ts:35-36, :61-62).
  - EMP-03-11 · PROP · sin `email` y con al menos una ficha en la entidad → 400 `employee/exist_employee`: `findByEmailOrPhone` sin filtro devuelve la primera ficha (FirestoreEmployeeRepository.ts:212-221).
  - EMP-03-12 · PROP · sin `email` en una entidad sin fichas → 400 `{ok:false, error:"invalid_email"}`.
  - EMP-03-13 · PROP · `email` con formato inválido (`"abc"`) → 400 `{ok:false, error:"invalid_email"}`.
  - EMP-03-14 · PROP · sin `fullName` → 400 `{error:"Invalid payload", details:["fullName is required"], code:"employee/bad_request"}`.
  - EMP-03-15 · PROP · sin `role` → 400 con `details` que incluye «role is required» y «role must be 'internal' or 'collaborator'».
  - EMP-03-16 · PROP · `role:"manager"` → 400 `employee/bad_request`.
  - EMP-03-17 · PROP · `enableA2F:"true"` (cadena) → 400 «enableA2F must be boolean».
  - EMP-03-18 · PROP · `metadata:"x"` → 400 «metadata must be an object».
  - EMP-03-19 · PROP · `status:"inactive"` en el cuerpo → 201, y la ficha nace `active`.
  - EMP-03-20 · OP_MANAGER / OP_SUPERVISOR / OP_WORKER · cuerpo válido → 403 `{error:"No tienes permisos para esta operación en la entidad.", code:"auth/unauthorized"}`.
  - EMP-03-21 · AJENO · `entityId` de otra entidad → 403 (mismo cuerpo).
  - EMP-03-22 · AJENO · cuerpo inválido → 400: se valida antes que el permiso.
  - EMP-03-23 · ANON → 401 `{error:"unauthenticated", message:"Missing Authorization header"}`.
  - EMP-03-24 · TOKEN_INVALIDO → 401 `{error:"unauthenticated"}`.
  - EMP-03-25 · PROP · reenvío (`id` y `email` de una ficha existente) → 200 `code:"employee/email_sent"`; contraseña nueva y correo; no mira el cupo ni los duplicados.
  - EMP-03-26 · PROP · reenvío con `id` y sin `email` → `getUserByEmail("undefined")` lanza → 400 `{error:<mensaje de Auth>}`.
  - EMP-03-27 · PROP · reenvío con `email` que no tiene cuenta en Auth → 400 `{error:<mensaje de Auth>}`.
  - EMP-03-28 · PROP · reenvío con `id` inventado y el `email` de una cuenta cualquiera de Auth, por ejemplo el propietario de otra entidad → 200; se cambia la contraseña de esa cuenta y se le manda la bienvenida (no se comprueba que `id` sea de la entidad ni que el correo sea suyo, employee.router.ts:153-161).
  - EMP-03-29 · PROP · falla el SMTP en un alta normal → 201 igualmente: `sendWelcomeEmail` devuelve `false` y no lanza (employeeAccess.ts:88-91).
  - EMP-03-30 · PROP · falla el SMTP en un reenvío → 400 `{error:"No se pudo reenviar el correo de bienvenida"}`.
- Sospechas: (1) crear un empleado con el correo de una cuenta existente de Auth le cambia la contraseña a esa persona (la CF hacía lo mismo desde el disparador); (2) el reenvío permite restablecer la contraseña de cualquier cuenta de Auth conociendo su correo, y a cualquier PROP o ADMIN de cualquier entidad; (3) la comprobación de duplicados distingue mayúsculas; (4) sin `email` el error dice «ya existe»; (5) las fichas dadas de baja siguen consumiendo cupo, aunque el repositorio tiene `countByEntity`, que las excluye (FirestoreEmployeeRepository.ts:224-235), y no se usa aquí.

## POST /api/v1/employees/update  ·  EMP-04
- Servicio: employees, `api:services/employees/src/interfaces/http/employee.router.ts:252-285` (ruta :353); reglas en `api:packages/shared/src/checkbiz/employees/manageEmployee.ts:103-164`.
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_EMPLOYEE`, `front:.env.development:57`; `front:src/services/checkinbiz/employee.service.ts:214`, proxy `checkinbiz_update_employee`; manda la ficha entera).
- Origen: portado desde la CF `cf:services-saas/checkinbiz/firebase-checkinbiz-http/update-employee.ts` (controlador `.../updateEmployee.controller.ts:69-105`).
- Diferencias con la CF:
  1. Ficha inexistente: 404 `{ok:false, error:"employee_not_found"}` (manageEmployee.ts:111). La CF escribía con `set(merge)` sin comprobar y respondía 201, creando una ficha fantasma (`cf:.../UpdateEmployee.ts:13-19`).
  2. Correo con formato inválido: 400 `{ok:false, error:"invalid_email"}` (:118-121). La CF lo aceptaba.
  3. Cambio de correo: ahora mueve también el usuario de Auth (`auth.updateUser(uid, {email})`, employeeAccess.ts:28-32). Si el correo nuevo es de otra cuenta, 409 `{ok:false, error:"email_in_use", employeeId, detail}`; si Auth falla por otro motivo, 502 `auth_error`. La CF no tocaba Auth.
  4. El contenedor también descarta `employeeId` y `sendWelcome` del cuerpo, y acepta el id como `id` o como `employeeId` (employee.router.ts:258-259, :272-275).
  5. Reindexa leyendo los valores actuales de la ficha para los campos que no llegan (manageEmployee.ts:148-154). La CF indexaba solo lo recibido y dejaba en blanco lo demás.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, body.entityId)` después de validar (employee.router.ts:267). La ficha se busca en `entities/{body.entityId}/employees/{id}`, así que no se alcanza una ficha de otra entidad.
- Entrada: obligatorios `entityId` e `id` (o `employeeId`). Opcionales validados: `role ∈ {internal, collaborator}`; `status ∈ {active, inactive, vacation, sick_leave, leave_of_absence, paternity_leave, maternity_leave}` (**no** `fired` ni `pending`); `email` y `phone` (cadenas); `enableA2F` y `biometricRequired` (booleanos); `metadata` (objeto); `sendWelcome` (booleano, no se guarda). Todo lo demás se escribe tal cual con `set(merge)`, salvo `uid` y `createdAt`.
- Respuesta correcta: 201 `{message:"Employee cupdated"}` (sic).
- Efectos: `set(merge)` sobre la ficha (FirestoreEmployeeRepository.ts:194-197). Si cambia el correo, el usuario de Auth pasa al correo nuevo, o se crea o reutiliza uno si la ficha no tenía `uid` (employeeAccess.ts:22-40). Si llegan `fullName`, `email` o `phone`, se reescribe `searchIndex`. La bienvenida (con contraseña nueva) solo sale si cambió el correo y además `sendWelcome:true`, o si el acceso se acaba de crear (manageEmployee.ts:159-161).
- Criticidad: alta — edición de plantilla desde el panel; mueve accesos.
- Casos:
  - EMP-04-01 · PROP · cambia `fullName` y `jobTitle` → 201; ficha y `searchIndex` actualizados.
  - EMP-04-02 · ADMIN · ídem → 201.
  - EMP-04-03 · PROP · `status:"sick_leave"` → 201; la ficha queda EMP_INACTIVO (`sick_leave`).
  - EMP-04-04 · PROP · ficha en `fired` con `status:"active"` → 201: se reactiva, porque no se mira el estado anterior.
  - EMP-04-05 · PROP · `status:"fired"` → 400 `{error:"Invalid payload", details:["status is invalid"]}`.
  - EMP-04-06 · PROP · correo nuevo libre en Auth, ficha con `uid` → 201; el login del usuario pasa al correo nuevo y **no se manda correo** salvo con `sendWelcome:true`.
  - EMP-04-07 · PROP · correo nuevo con `sendWelcome:true` → 201; contraseña nueva y bienvenida al correo nuevo.
  - EMP-04-08 · PROP · correo nuevo que ya usa otra cuenta de Auth → 409 `{ok:false, error:"email_in_use"}`; la ficha no cambia.
  - EMP-04-09 · PROP · ficha sin `uid` (importada, `pending`) a la que se le pone correo → 201; se crea el usuario de Auth, se manda la bienvenida y la ficha sigue `pending` si no se cambia `status`.
  - EMP-04-10 · PROP · `email:"abc"` → 400 `{ok:false, error:"invalid_email"}`.
  - EMP-04-11 · PROP · `uid` y `createdAt` en el cuerpo → 201; se ignoran los dos.
  - EMP-04-12 · PROP · `trustedDevicesId:[]` o `customToken` en el cuerpo → 201 y se escriben: no hay lista de campos permitidos.
  - EMP-04-13 · PROP · `id` inexistente → 404 `{ok:false, error:"employee_not_found"}`.
  - EMP-04-14 · PROP · `entityId` propio con `id` de un empleado de otra entidad → 404 `employee_not_found`.
  - EMP-04-15 · PROP · sin `id` ni `employeeId` → 400 `details:["id is requiredo"]` (sic).
  - EMP-04-16 · PROP · sin `entityId` → 400 `details:["entityId is required"]`.
  - EMP-04-17 · PROP · `role:"boss"` → 400.
  - EMP-04-18 · PROP · `phone: 123` → 400 «phoneNumber must be a string».
  - EMP-04-19 · OP_MANAGER / OP_SUPERVISOR / OP_WORKER → 403 `{error:"No tienes permisos para esta operación en la entidad."}` (sin `code`).
  - EMP-04-20 · AJENO → 403 (mismo cuerpo).
  - EMP-04-21 · ANON → 401 `unauthenticated`. TOKEN_INVALIDO → 401.
- Sospechas: (1) la edición acepta cualquier campo sin lista de permitidos, incluidos `trustedDevicesId` y `customToken` (igual que la CF); (2) si la misma persona es empleada en dos entidades con el mismo `uid`, cambiar su correo en una le cambia el login en la otra; (3) el comentario de la ruta dice que al cambiar el correo «se le avisa», pero con `uid` previo no se manda nada salvo que llegue `sendWelcome:true` (manageEmployee.ts:159).

## PATCH /api/v1/employees/:employeeId  ·  EMP-05
- Servicio: employees, `api:services/employees/src/interfaces/http/employee.router.ts:362-364`, que llama a la misma función `update` que EMP-04 con el id de la ruta, prioritario sobre el del cuerpo (:258).
- Consumidores: ninguno detectado (el panel usa EMP-04).
- Origen: nativo del contenedor (forma REST de EMP-04).
- Diferencias con la CF: sin CF equivalente con esta ruta. El contrato de cuerpos y estados es el de EMP-04.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, body.entityId)`.
- Entrada: `entityId` en el cuerpo (obligatorio) y el resto como EMP-04. El id del cuerpo se ignora.
- Respuesta correcta: 201 `{message:"Employee cupdated"}`.
- Efectos: como EMP-04.
- Criticidad: media — mismo efecto que EMP-04, sin consumidor.
- Casos:
  - EMP-05-01 · PROP · `PATCH /{idReal}` con `{entityId, fullName}` → 201.
  - EMP-05-02 · PROP · `PATCH /{idReal}` con `{entityId, id:"otro"}` → 201 sobre `idReal`: manda la ruta.
  - EMP-05-03 · PROP · sin `entityId` en el cuerpo → 400 `details:["entityId is required"]`.
  - EMP-05-04 · PROP · id de la ruta inexistente → 404 `employee_not_found`.
  - EMP-05-05 · AJENO → 403. ANON → 401.
- Sospechas: ninguna adicional.

## DELETE /api/v1/employees  ·  EMP-06
- Servicio: employees, `api:services/employees/src/interfaces/http/employee.router.ts:289-315` (ruta :356); reglas en `api:packages/shared/src/checkbiz/employees/manageEmployee.ts:175-193`.
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_DELETE_EMPLOYEE`, `front:.env.development:58`; `front:src/services/checkinbiz/employee.service.ts:272`, que manda `DELETE` con cuerpo `{employeeId, entityId}`).
- Origen: portado desde la CF `cf:services-saas/checkinbiz/firebase-checkinbiz-http/delete-employee.ts` (controlador `.../deleteEmployee.controller.ts:38-61`, caso de uso `DeleteEmployee.ts:10-25`).
- Diferencias con la CF: (1) ficha inexistente: 404 `{ok:false, error:"employee_not_found"}`; la CF hacía `set({status:"fired"}, merge)` sobre la nada y respondía 200, dejando una ficha fantasma (`cf:.../FirestoreEmployeeRepository.ts:186-190`); (2) acepta `id` como sinónimo de `employeeId`, y `entityId` también por query. La baja es **blanda en los dos**: la CF ya dejaba `status:"fired"`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)` (employee.router.ts:304).
- Entrada: `employeeId` (o `id`) en el cuerpo y `entityId` en el cuerpo o en la query, los dos obligatorios.
- Respuesta correcta: 200 `{message:"Employee deleted successfully", code:"employee/deleted"}`.
- Efectos: (a) borra cada responsabilidad **activa** del empleado: documento de `employee_responsibilities`, sin `await`, más `arrayRemove` del centro en `employee.branchId` (FirestoreEmployeeRepository.ts:75-79); las inactivas (`active:0`) se quedan. (b) Ficha: `set({status:"fired", updatedAt}, merge)`, **borrado blando** (:206-210). (c) `searchIndex` de la ficha eliminado (manageEmployee.ts:191). (d) El usuario de Auth **no se toca** (:173).
- Criticidad: alta — baja de plantilla desde el panel.
- Casos:
  - EMP-06-01 · PROP · empleado con dos responsabilidades activas → 200; ficha `fired`, responsabilidades borradas (hay que sondear: no se esperan), `searchIndex` retirado y usuario de Auth intacto.
  - EMP-06-02 · ADMIN · ídem → 200.
  - EMP-06-03 · PROP · empleado con una responsabilidad `active:0` → 200 y esa responsabilidad sigue en Firestore.
  - EMP-06-04 · PROP · ficha ya `fired` → 200 otra vez (idempotente).
  - EMP-06-05 · PROP · `entityId` por query y `employeeId` en el cuerpo → 200.
  - EMP-06-06 · PROP · `employeeId` inexistente → 404 `{ok:false, error:"employee_not_found"}`.
  - EMP-06-07 · PROP · sin `employeeId` → 400 `{error:"Invalid payload", details:["employeeId is required"], code:"employee/bad_request"}`.
  - EMP-06-08 · PROP · sin `entityId` → 400 `details:["entityId is required"]`.
  - EMP-06-09 · OP_MANAGER → 403 `{error:"You do not have permission for this operation in the entity.", code:"auth/unauthorized"}`.
  - EMP-06-10 · AJENO · `entityId` ajeno → 403 (mismo cuerpo).
  - EMP-06-11 · ANON → 401. TOKEN_INVALIDO → 401.
  - EMP-06-12 · PROP · después de la baja, validar al empleado con EMP-01 → 200 con `sessionToken` (ver EMP-01-10).
  - EMP-06-13 · PROP · después de la baja, dar de alta con EMP-03 a alguien con el mismo correo → 400 `employee/exist_employee`.
- Sospechas: (1) la baja es blanda y el usuario de Auth sigue vivo: el empleado puede seguir validando (EMP-01) y, como la ficha `fired` consume cupo, tampoco se libera plaza; volver a contratar a la misma persona con el mismo correo está bloqueado por el guardia de duplicados. (2) El borrado del documento de responsabilidad no se espera (`FirestoreEmployeeRepository.ts:78`): el 200 puede llegar antes que el borrado. (3) Las responsabilidades inactivas no se limpian.

## DELETE /api/v1/employees/:employeeId  ·  EMP-07
- Servicio: employees, `api:services/employees/src/interfaces/http/employee.router.ts:367-369`, que llama a `remove` con el id de la ruta (:292).
- Consumidores: ninguno detectado.
- Origen: nativo del contenedor (forma REST de EMP-06).
- Diferencias con la CF: sin CF equivalente con esta ruta. El contrato es el de EMP-06.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)`, con `entityId` por query o en el cuerpo.
- Entrada: `:employeeId` en la ruta y `entityId` en la query (lo normal en un DELETE) o en el cuerpo.
- Respuesta correcta: 200 `{message:"Employee deleted successfully", code:"employee/deleted"}`.
- Efectos: como EMP-06.
- Criticidad: media — sin consumidor, mismo efecto destructivo.
- Casos:
  - EMP-07-01 · PROP · `DELETE /{id}?entityId={e}` → 200.
  - EMP-07-02 · PROP · sin `entityId` → 400 `details:["entityId is required"]`.
  - EMP-07-03 · PROP · id inexistente → 404 `employee_not_found`.
  - EMP-07-04 · AJENO → 403. ANON → 401.
- Sospechas: ninguna adicional.

## POST /api/v1/employees/:employeeId/email  ·  EMP-08
- Servicio: employees, `api:services/employees/src/interfaces/http/employee.router.ts:372-383`.
- Consumidores: ninguno detectado. El comentario habla del «panel de add-ons», pero el handler `addons_handler` del proxy no deja pasar esta ruta (`front:src/lib/http/serverBackendProxy.ts:325-342`).
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, body.entityId)` (:378).
- Entrada: `entityId` y `email` obligatorios; `sendWelcome` opcional.
- Respuesta correcta: 200 `{ok:true, employeeId, uid, welcomeSent}`.
- Efectos: los de `updateEmployee` con `{email}`: mueve o crea el acceso de Auth, reindexa `searchIndex` y, si procede, manda la bienvenida.
- Criticidad: baja — sin consumidor detectado.
- Casos:
  - EMP-08-01 · PROP · ficha `pending` sin `uid` y correo nuevo → 200 `welcomeSent:true`, usuario creado.
  - EMP-08-02 · PROP · ficha con `uid` y correo nuevo → 200 `welcomeSent:false` (sin `sendWelcome`).
  - EMP-08-03 · PROP · falta `email` o `entityId` → 400 `{ok:false, error:"entityId and email are required"}`.
  - EMP-08-04 · PROP · correo usado por otra cuenta → 409 `email_in_use`.
  - EMP-08-05 · PROP · ficha inexistente → 404 `employee_not_found`.
  - EMP-08-06 · PROP · `email:"abc"` → 400 `invalid_email`.
  - EMP-08-07 · AJENO → 403 `{error:"No tienes permisos para esta operación en la entidad."}`. ANON → 401.
- Sospechas: completar el correo no cambia `status: pending` a `active`; la ficha sigue sin poder trabajar hasta que alguien edite el estado (sin confirmar que haya otro camino que lo haga).

## POST /api/v1/employees/responsibilities  ·  EMP-09
- Servicio: employees, `api:services/employees/src/interfaces/http/responsibility.router.ts:51-118`, montado en `app.ts:27` antes que el router de plantilla.
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_RESPONSABILITY_HANDLER`, `front:.env.development:62`; `front:src/services/checkinbiz/employee.service.ts:240` `handleRespnsability(..., 'post')`; allowlist POST/PATCH/DELETE en `serverBackendProxy.ts:213-217`).
- Origen: portado desde la CF `cf:services-saas/checkinbiz/firebase-checkinbiz-http/responsibility.ts` (despacho por verbo, :14-33) con `.../responsibility/createResponsibility.controller.ts:83-119`.
- Diferencias con la CF: (1) `assignedBy` sale del token; en la CF lo inyectaba el envoltorio (`responsibility.ts:9`), con el mismo resultado. (2) El contenedor ignora `level` en el cuerpo; la CF lo validaba si llegaba (`createResponsibility.controller.ts:30-33`) y respondía 400 con un `level` fuera de rango. (3) Sin `scope.branchId`: el contenedor busca el centro `"null"` y responde 400 `employee/not_found`; la CF llamaba a `findById(null)` (probablemente 500; sin confirmar). (4) Excepciones: CF 500 `{success:false, message}`, contenedor 500 `{ok:false, error:"internal_error"}`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, scope.entityId)` después de validar (:80-85). Un OP_MANAGER u OP_OWNER de la sucursal **no** puede asignar.
- Entrada: obligatorios `employeeId`, `responsibility ∈ {owner, manager, supervisor, worker}`, `scope.entityId`, `job.job` y `job.price` (número). En la práctica también hace falta `scope.branchId`, porque el centro tiene que existir. Opcionales: `active ∈ {0,1}` (por defecto 1), `assignedAt` (lo pisa el repositorio con la hora actual, FirestoreEmployeeRepository.ts:50) y `metadata`.
- Respuesta correcta: 201 `{success:true, data:{employeeId, responsibility, level, scope, job, assignedBy, assignedAt, active, id, metadata?}}`. `level` = 1 worker, 2 supervisor, 3 manager, 4 owner.
- Efectos: (a) `entities/{e}/employee_responsibilities/{employeeId}_{entityId}_{branchId}` con `set` completo (FirestoreEmployeeRepository.ts:47, :55); si ya existía, **se sobrescribe**. (b) `arrayUnion(branchId)` en `employee.branchId`, sin `await` (:54). (c) Push FCM a los dispositivos del empleado y documento en `in_app_notifications`, con el mensaje `assign_created` (`api:packages/shared/src/checkbiz/notifications/CheckbizOperationals.ts:168-214`; colección en `FirestoreAppNotificationsRepository.ts:13`). (d) La responsabilidad de nivel ≥ 2 habilita a ese empleado en `canWrite(..., {includeBranchResponsibility})` del camino del fichaje.
- Criticidad: alta — reparte permisos por sucursal y el coste por hora.
- Casos:
  - EMP-09-01 · PROP · empleado y centro existentes, `responsibility:"supervisor"`, `job:{job:"Camarero", price:12}` → 201; `level:2`, `assignedBy` = uid del PROP; se añade el centro a `employee.branchId`; notificación `assign_created`.
  - EMP-09-02 · ADMIN · ídem → 201.
  - EMP-09-03 · PROP · misma persona y mismo centro con `responsibility:"manager"` (cambio de nivel por alta) → 201; el documento se sobrescribe con `level:3`.
  - EMP-09-04 · PROP · `active:0` → 201 con la responsabilidad inactiva, que no aparece en los listados porque filtran `active == 1`.
  - EMP-09-05 · PROP · `assignedBy:"otro"` en el cuerpo → 201 y se guarda el uid del token.
  - EMP-09-06 · PROP · empleado sin dispositivos → 201; sin push, pero se crea `in_app_notifications`.
  - EMP-09-07 · PROP · sin `scope.branchId` → 400 `{error:"Employee not found", code:"employee/not_found"}`.
  - EMP-09-08 · PROP · `branchId` inexistente → 400 `employee/not_found`.
  - EMP-09-09 · PROP · `employeeId` inexistente → 400 `employee/not_found`.
  - EMP-09-10 · PROP · empleado `fired` → 201: la ficha existe (baja blanda) y se le asigna igual.
  - EMP-09-11 · PROP · `responsibility:"boss"` → 400 `{error:"Invalid payload", details:[...], code:"employee/bad_request"}`.
  - EMP-09-12 · PROP · `job.price:"12"` (cadena) → 400 «job.price must be a number».
  - EMP-09-13 · PROP · sin `job.job` → 400. Con `active:2` → 400 «active must be 0 or 1».
  - EMP-09-14 · PROP · sin `scope.entityId` → 400 «scope.entityId is required».
  - EMP-09-15 · OP_OWNER / OP_MANAGER de la sucursal → 403 `{error:"No tienes permisos para esta operación en la entidad.", code:"auth/unauthorized"}`.
  - EMP-09-16 · AJENO · `scope.entityId` ajeno → 403.
  - EMP-09-17 · ANON → 401 `unauthenticated`.
- Sospechas: (1) un alta sobre una responsabilidad existente la sobrescribe sin avisar; (2) `arrayUnion` sobre `employee.branchId` no se espera y sus errores solo se registran en el log; (3) se puede asignar responsabilidad a un empleado dado de baja.

## PATCH /api/v1/employees/responsibilities  ·  EMP-10
- Servicio: employees, `api:services/employees/src/interfaces/http/responsibility.router.ts:122-185`.
- Consumidores: panel (misma variable; `handleRespnsability(..., 'patch')`, `employee.service.ts:240`).
- Origen: portado desde la CF `.../responsibility/updateResponsibility.controller.ts:76-119`.
- Diferencias con la CF: el contenedor no valida que `job.price` sea número: lo convierte con `Number()` y guarda `NaN` si no puede. La CF respondía 400 «job.price must be a number» cuando llegaba y no era número (`updateResponsibility.controller.ts:42`). El resto de cuerpos y estados coinciden.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, scope.entityId)` (:162-164).
- Entrada: obligatorios `id`, `employeeId` y `scope`, este con `entityId` y `branchId` (:154-157). Opcionales: `active ∈ {0,1}`, `responsibility` (recalcula `level`), `job` (objeto) y `metadata`.
- Respuesta correcta: 200 `{success:true, message:"Responsibility successfully updated", code:"responsability/updated"}` (sic).
- Efectos: `set(payload, {merge:true})` sobre `employee_responsibilities/{id}` **sin `await`** (FirestoreEmployeeRepository.ts:71-73): si el id no existe, **crea** el documento. `employee.branchId` no se toca. Notificación `assign_updated`, con push e `in_app_notifications`.
- Criticidad: alta — cambia nivel y permisos por sucursal.
- Casos:
  - EMP-10-01 · PROP · sube de `worker` a `supervisor` → 200; `level:2` en el documento (sondear, no se espera la escritura).
  - EMP-10-02 · ADMIN · `active:0` (retirada lógica) → 200; desaparece de los listados y deja de contar en `canWrite` por sucursal, pero `employee.branchId` conserva el centro.
  - EMP-10-03 · PROP · `job:{job:"X", price:"15"}` → 200 y se guarda `price:15`.
  - EMP-10-04 · PROP · `job:{job:"X"}` sin `price` → 200 y se guarda `price: NaN`.
  - EMP-10-05 · PROP · `job:{price:10}` sin `job.job` → 200; la escritura lleva `job.job = undefined`, que Firestore rechaza fuera de la petición (sin `await`: el efecto sobre el proceso está sin confirmar).
  - EMP-10-06 · PROP · `id` inexistente con empleado y centro válidos → 200 y se crea un documento de responsabilidad parcial con ese id.
  - EMP-10-07 · PROP · `scope` sin `branchId` → 400 `{error:"Bad scope data", code:"responsibility/bad_request"}`.
  - EMP-10-08 · PROP · sin `id` → 400 `{error:"Invalid payload", details:["responsibility.id is required"]}`.
  - EMP-10-09 · PROP · `responsibility:"boss"` o `active:5` → 400 `Invalid payload`.
  - EMP-10-10 · PROP · centro o empleado inexistente → 400 `{error:"Employee not found", code:"employee/not_found"}`.
  - EMP-10-11 · OP_MANAGER → 403 `{error:"Unauthorized access to this entity", code:"auth/unauthorized"}`.
  - EMP-10-12 · AJENO → 403. ANON → 401.
- Sospechas: (1) la escritura no se espera: el 200 no garantiza que se haya guardado y sus errores se pierden; (2) PATCH crea documentos si el id no existe; (3) desactivar no retira el centro de `employee.branchId`; (4) `price` puede acabar en `NaN`.

## DELETE /api/v1/employees/responsibilities  ·  EMP-11
- Servicio: employees, `api:services/employees/src/interfaces/http/responsibility.router.ts:189-223`.
- Consumidores: panel (misma variable; `handleRespnsability(..., 'delete')` con cuerpo).
- Origen: portado desde la CF `.../responsibility/deleteResponsibility.controller.ts:10-48`.
- Diferencias con la CF: sin `id`, el contenedor responde 400 `responsibility/bad_request`. La CF hacía `(id as string).split` antes de validar y acababa en 500 `{success:false, message}` (`deleteResponsibility.controller.ts:13`).
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)`, con el `entityId` **sacado del propio id** (`{employeeId}_{entityId}_{branchId}`, :196, :204).
- Entrada: cuerpo `{id}`.
- Respuesta correcta: 200 `{success:true, message:"Responsibility successfully deleted"}`.
- Efectos: `delete` del documento **sin `await`**, más `arrayRemove(branchId)` en `employee.branchId`, también sin `await` (FirestoreEmployeeRepository.ts:75-79). Notificación `assign_deleted`.
- Criticidad: alta — retira permisos por sucursal.
- Casos:
  - EMP-11-01 · PROP · id existente → 200; documento borrado y centro retirado de `employee.branchId` (sondear); notificación enviada.
  - EMP-11-02 · ADMIN · ídem → 200.
  - EMP-11-03 · PROP · id bien formado de una responsabilidad que no existe, con empleado y centro existentes → 200 y se manda la notificación de todos modos.
  - EMP-11-04 · PROP · id sin `branchId` (`{emp}_{ent}`) → 400 `employee/not_found`, porque se busca el centro `"undefined"`.
  - EMP-11-05 · PROP · sin `id` → 400 `{error:"id is required.", code:"responsibility/bad_request"}`.
  - EMP-11-06 · PROP · id con un solo segmento → 400 `responsibility/bad_request`.
  - EMP-11-07 · PROP · empleado o centro inexistente → 400 `employee/not_found`.
  - EMP-11-08 · AJENO · id de otra entidad → 403 `{error:"Unauthorized access to this entity", code:"auth/unauthorized"}`.
  - EMP-11-09 · OP_MANAGER → 403. ANON → 401.
- Sospechas: (1) el borrado no se espera; (2) borrar algo que no existe devuelve 200 y notifica al empleado; (3) una responsabilidad a nivel de entidad, sin `branchId`, no se puede borrar por aquí.

## GET /api/v1/employees/responsibilities?entityId=&branchId=  ·  EMP-12
- Servicio: employees, `api:services/employees/src/interfaces/http/responsibility.router.ts:229-246`.
- Consumidores: ninguno detectado (la allowlist del proxy no incluye GET, `serverBackendProxy.ts:215`).
- Origen: portado desde la CF `.../responsibility/findAllResponsibilities.controller.ts:12-34`.
- Diferencias con la CF: la CF exigía `entityId` **y** `employeeId` en el cuerpo, y comprobaba `canWrite` con `body.requesterId`, que el envoltorio nunca ponía (`findAllResponsibilities.controller.ts:8, :19-20`), así que sin `requesterId` en el cuerpo respondía siempre 403. El contenedor lee `entityId` de la query o del cuerpo, usa el uid del token e ignora `employeeId`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)` (:240-242).
- Entrada: `entityId` obligatorio; `branchId` opcional.
- Respuesta correcta: 200 `{success:true, data:[responsabilidades activas]}`.
- Efectos: ninguno.
- Criticidad: baja — sin consumidor.
- Casos:
  - EMP-12-01 · PROP · `?entityId=e` → 200 con todas las activas de la entidad.
  - EMP-12-02 · ADMIN · `?entityId=e&branchId=b` → 200, solo las de ese centro.
  - EMP-12-03 · PROP · sin `entityId` → 400 `{error:"Invalid query parameters", details:["entityId is required"]}`.
  - EMP-12-04 · OP_SUPERVISOR → 403 `{error:"Unauthorized access to this entity", code:"auth/unauthorized"}`.
  - EMP-12-05 · AJENO → 403. ANON → 401.
- Sospechas: ninguna.

## POST /api/v1/employees/notifications  ·  EMP-13
- Servicio: employees, `api:services/employees/src/interfaces/http/notification.router.ts:28-39` (montado en `app.ts:32`); motor en `api:packages/shared/src/checkbiz/notifications/CheckbizOperationals.ts:72-165`.
- Consumidores: ninguno detectado. `NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_NOTIFICATIONS` existe en `front:.env.development:123`, pero no aparece en `front:src`.
- Origen: portado desde la CF `checkbizNotifications` (`cf:services-saas/checkinbiz/firebase-checkinbiz-http/evaluateNotificationsPush.ts:23-44`).
- Diferencias con la CF: ninguna visible. Mismo 403 y mismo 200 `{ok:true}`; los errores de la CF eran 500 `{error}`.
- Autenticación: Firebase ID token.
- Autorización: solo la claim `admin: true` (:32-35). **No comprueba que el usuario pertenezca a la entidad del cuerpo.**
- Entrada: `CheckbizNotiAppData` `{entityId, branchId, distance?, ratioChecklog?, patternMismatchStart?, patternMismatchEnd?, outOfDayWindow?, ...}`, sin validación.
- Respuesta correcta: 200 `{ok:true}` siempre: `handleCreateNotification` es síncrono y lanza los envíos sin esperarlos (:72-91).
- Efectos: por cada regla que se cumple (`distance == true`, `ratioChecklog > 120`, `patternMismatchStart`, `patternMismatchEnd`, `outOfDayWindow`), push y documento en `in_app_notifications` para los empleados con responsabilidad de **nivel exactamente 2** (supervisor) en ese centro (:150-154). Managers y owners no reciben.
- Criticidad: media — manda avisos a personas; sin consumidor, pero abierto a entidades ajenas.
- Casos:
  - EMP-13-01 · CLAIM_ADMIN (PROP con 2FA) · `{entityId, branchId, ratioChecklog:150}` en un centro con supervisores → 200; `in_app_notifications` con `type:"operational"` para cada supervisor.
  - EMP-13-02 · CLAIM_ADMIN · centro sin supervisores de nivel 2 → 200, sin efectos.
  - EMP-13-03 · CLAIM_ADMIN · cuerpo vacío → 200, sin efectos.
  - EMP-13-04 · CLAIM_ADMIN · `distance: 350` (número) → 200, sin aviso: `350 == true` es falso.
  - EMP-13-05 · CLAIM_ADMIN de otra entidad (AJENO con claim) · `entityId` y `branchId` de una entidad ajena → 200 y se notifica a los supervisores ajenos.
  - EMP-13-06 · PROP sin claim `admin` · → 403 `{error:"Admin access required", code:"auth/admin_required"}`.
  - EMP-13-07 · ANON → 401 `unauthenticated`.
- Sospechas: cualquier usuario con la claim `admin`, de cualquier entidad, puede disparar avisos a los supervisores de cualquier centro (la CF hacía lo mismo).

---

# SUC — Sucursales (`services/branches`, puerto 3014)

Todas pasan por `requireFirebaseAuth` (`api:services/branches/src/app.ts:16`) y por el guardián `requireEntityWriter(status)` (`api:services/branches/src/interfaces/http/branch.router.ts:46-64`), que lee `entityId` del cuerpo o de la query y va **antes** de validar el cuerpo. Sin `entityId` → 400 `{error:"entityId is required"}`; sin permiso → `status` con `{error, code:"auth/unauthorized"}`.

## POST /api/v1/branches  ·  SUC-01
- Servicio: branches, `branch.router.ts:68-101` (ruta :174); validación en `branch.validation.ts:95-174`.
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_CREATE_SUCURSAL`, `front:.env.development:66`; `front:src/services/checkinbiz/sucursal.service.ts:48`, proxy `checkinbiz_create_sucursal`).
- Origen: portado desde la CF `cf:services-saas/checkinbiz/firebase-checkinbiz-http/create-branch.ts` (controlador `.../branch/createBranch.controller.ts:177-213`).
- Diferencias con la CF:
  1. **Sin permiso: la CF respondía 401 `{code:"auth/invalid_token", error:"Unauthorized"}`** (`createBranch.controller.ts:187-189`). El contenedor responde **403** `{error:"Unauthorized to perform this operation on the entity", code:"auth/unauthorized"}`. El README del servicio dice que la CF daba 403 en el alta, y no es lo que hace el código de la CF.
  2. Orden: la CF validaba antes que el permiso. En el contenedor el permiso va primero, así que un cuerpo sin `entityId` da 400 `{error:"entityId is required"}` sin `details`, donde la CF daba 400 `{error:"Invalid payload", details:[...]}`.
  3. `address.postalCode` ausente se guarda como `""`; la CF guardaba la cadena `"undefined"` (`createBranch.controller.ts:154`).
  4. Nuevo: emite el evento `branch.created`.
  5. Excepciones: CF 400 `{error}`, contenedor 500 `internal_error`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)`, 403 si no pasa.
- Entrada: obligatorios `name`, `entityId` y `address{street, country, timeZone, geo{lat∈[-90,90], lng∈[-180,180]}}`. Opcionales: `address.postalCode` (cadena no vacía), `ratioChecklog` (> 0; por defecto 200), `metadata` (objeto), `advance` (objeto; si `workScheduleEnable`, exige un `workSchedule` válido con `notifyBeforeMinutes` entre 0 y 180), `status ∈ {archived, active}` (por defecto active), `nif` y `disableRatioChecklog` (por defecto false). `city` se ignora.
- Respuesta correcta: 201 con el centro `{id, name, entityId, nif, address, ratioChecklog, advance, metadata, status, disableRatioChecklog, createdAt}`.
- Efectos: (a) `entities/{e}/branches/{id}`. (b) `searchIndex/entities__{e}__branches__{id}` con nombre, calle y código postal, escrito dos veces con el mismo id (FirestoreBranchRepository.ts:24 y branch.router.ts:85-91). (c) Evento `branch.created` (`events/branch.ts:8-19`), sin `await`. (d) Disparador CF `onCreateBranch`: crea `checkbiz_branch_patterns/{branchId}` (`cf:services-saas/checkinbiz/firebase-firestore-trigger/dataProcessing/onCreateBranch.ts:21-25`).
- Criticidad: alta — sin centro no se ficha, y hay cupo de plan.
- Casos:
  - SUC-01-01 · PROP · cuerpo completo y plan con cupo → 201; centro, `searchIndex`, evento y (disparador) patrón inicial.
  - SUC-01-02 · ADMIN · ídem → 201.
  - SUC-01-03 · PROP · sin `ratioChecklog` → 201 con `ratioChecklog:200`. Sin `advance` → 201 con `advance:null`.
  - SUC-01-04 · PROP · `status:"archived"` → 201 con `status:"archived"`, que no consume cupo.
  - SUC-01-05 · PROP · centros `active` ≥ `maxBranches` → 403 `{code:"subscription/limit_off", message:"You cannot create a new branch: your plan's quota has been reached."}`.
  - SUC-01-06 · PROP · cupo lleno solo con centros `inactive` o `archived` → 201 (`countAll` solo cuenta `active`, FirestoreBranchRepository.ts:34-42).
  - SUC-01-07 · PROP · entidad sin suscripción `checkinbiz` o sin plan → 403 `subscription/limit_off`.
  - SUC-01-08 · PROP · sin `address.timeZone` → 400 `{error:"Invalid payload", details:["address.timeZone must be a non-empty string if provided"]}`.
  - SUC-01-09 · PROP · `geo.lat: 95` → 400 «address.geo.lat must be between -90 and 90». Sin `geo` → 400.
  - SUC-01-10 · PROP · `ratioChecklog: 0` → 400 «ratioChecklog must be greater than 0».
  - SUC-01-11 · PROP · `advance.workScheduleEnable:true` sin `workSchedule` → 400. Con `notifyBeforeMinutes: 200` → 400.
  - SUC-01-12 · PROP · `status:"inactive"` → 400 «status must be 'archived' or 'active' if provided».
  - SUC-01-13 · PROP · sin `entityId` → 400 `{error:"entityId is required"}`.
  - SUC-01-14 · OP_MANAGER · cuerpo válido → 403 `{error:"Unauthorized to perform this operation on the entity", code:"auth/unauthorized"}`.
  - SUC-01-15 · AJENO → 403 (mismo cuerpo). AJENO con cuerpo inválido → 403 (el permiso va antes).
  - SUC-01-16 · ANON → 401 `{error:"unauthenticated", message:"Missing Authorization header"}`.
- Sospechas: el alta acepta `archived` y la edición `inactive` (divergencia heredada, documentada en `branch.validation.ts:137-144`).

## POST /api/v1/branches/update  ·  SUC-02
- Servicio: branches, `branch.router.ts:103-150` (ruta :177-179, id tomado de `body.id` o `body.branchId`); validación en `branch.validation.ts:179-266`.
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_SUCURSAL`, `front:.env.development:67`; `sucursal.service.ts:74`).
- Origen: portado desde la CF `.../branch/updateBranch.controller.ts:190-222`.
- Diferencias con la CF: (1) centro inexistente: 404 `{error:"Branch not found", code:"branch/not_found"}`; la CF escribía igualmente (sin confirmar si el caso de uso comprobaba existencia) y respondía 200. (2) El permiso va antes de validar, con el mismo 401 `{error:"Unauthorized", code:"auth/unauthorized"}` que la CF. (3) Nuevo: eventos `branch.updated` y, si cambian coordenadas o radio, `branch.geofence_changed`. (4) El índice se reescribe con la ficha completa; la CF indexaba solo lo recibido. (5) Excepciones: CF 500 `{error}`, contenedor 500 `internal_error`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)`, **401** si no pasa.
- Entrada: obligatorios `entityId` e `id` (o `branchId`). Opcionales: `name`, `status ∈ {inactive, active}`, `ratioChecklog` (> 0), `metadata`, `advance`, `nif`, `disableRatioChecklog` y `address` (si llega, **exige `timeZone`**; `street`, `country`, `postalCode` y `region` no vacíos; `geo` con rangos).
- Respuesta correcta: 200 `{message:"Branch updated successfully"}`.
- Efectos: `set(merge)` del centro. Si cambian `name` o `address`, se relee y se reindexa `searchIndex` (FirestoreBranchRepository.ts:111-121). Evento `branch.updated` con `changed`, y `branch.geofence_changed` si cambian `lat`, `lng` o `ratioChecklog` (branch.router.ts:130-147). **`disableRatioChecklog` se escribe `false` si no llega** (branch.validation.ts:264).
- Criticidad: alta — la geocerca decide qué fichajes se aceptan.
- Casos:
  - SUC-02-01 · PROP · cambia `name` → 200; `searchIndex` con el nombre nuevo; evento `branch.updated` con `changed` que incluye `name` y `disableRatioChecklog`.
  - SUC-02-02 · ADMIN · cambia `address.geo` → 200; eventos `branch.updated` y `branch.geofence_changed`.
  - SUC-02-03 · PROP · cambia `ratioChecklog` de 200 a 300 → 200 y `branch.geofence_changed`.
  - SUC-02-04 · PROP · centro con `disableRatioChecklog:true`, edición solo de `name` → 200, y `disableRatioChecklog` pasa a `false`.
  - SUC-02-05 · PROP · `status:"inactive"` → 200 y deja de consumir cupo. `status:"archived"` → 400.
  - SUC-02-06 · PROP · `address:{street:"x"}` sin `timeZone` → 400 `details:["address.timeZone must be a non-empty string if provided"]`.
  - SUC-02-07 · PROP · `id` inexistente → 404 `{error:"Branch not found", code:"branch/not_found"}`.
  - SUC-02-08 · PROP · sin `id` → 400 `{error:"Invalid payload", details:["id is required"]}`.
  - SUC-02-09 · PROP · `name:""` → 400.
  - SUC-02-10 · PROP · `entityId` propio con el `id` de un centro de otra entidad → 404.
  - SUC-02-11 · OP_MANAGER → **401** `{error:"Unauthorized", code:"auth/unauthorized"}`.
  - SUC-02-12 · AJENO → 401 (mismo cuerpo). ANON → 401 `unauthenticated`.
- Sospechas: una edición parcial sin `disableRatioChecklog` vuelve a activar la comprobación de radio en un centro que la tenía desactivada (la CF hacía lo mismo).

## PATCH /api/v1/branches/:branchId  ·  SUC-03
- Servicio: branches, `branch.router.ts:186-188`, la misma función `update` con el id de la ruta.
- Consumidores: ninguno detectado.
- Origen: nativo del contenedor (forma REST de SUC-02).
- Diferencias con la CF: sin CF equivalente con esta ruta.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)` con `entityId` del cuerpo o de la query; 401 si no pasa.
- Entrada: `entityId` en el cuerpo (la validación lo exige ahí aunque el guardián lo acepte por query) y el resto como SUC-02.
- Respuesta correcta: 200 `{message:"Branch updated successfully"}`.
- Efectos: como SUC-02.
- Criticidad: media — sin consumidor.
- Casos:
  - SUC-03-01 · PROP · `PATCH /{id}` con `{entityId, name}` → 200.
  - SUC-03-02 · PROP · `PATCH /{id}?entityId=e` con cuerpo `{name}` → 400 `details:["entityId is required"]`: pasa el guardián, pero la validación exige `entityId` en el cuerpo.
  - SUC-03-03 · PROP · id inexistente → 404 `branch/not_found`.
  - SUC-03-04 · AJENO → 401. ANON → 401.
- Sospechas: la ruta REST no se puede usar con `entityId` solo en la query.

## DELETE /api/v1/branches  ·  SUC-04
- Servicio: branches, `branch.router.ts:152-168` (ruta :182-184; id de `body.branchId` o `body.id`).
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_DELETE_SUCURSAL`, `front:.env.development:68`; `sucursal.service.ts:107`, con cuerpo `{branchId, entityId}`).
- Origen: portado desde la CF `.../branch/deleteBranch.controller.ts:37-70`.
- Diferencias con la CF: (1) sin `entityId`: 400 `{error:"entityId is required"}` (guardián); sin `branchId`: 400 `{error:"branchId is required", code:"branch/bad_request"}`. La CF daba en ambos casos 400 `{error:"Invalid payload", details, code:"branch/bad_request"}`. (2) Nuevo: evento `branch.deleted`. (3) Excepciones: CF 500 `{code:"branch/internal_error"}`, contenedor 500 `{ok:false, error:"internal_error"}`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)`, 403 si no pasa.
- Entrada: `branchId` (o `id`) y `entityId`, en el cuerpo; `entityId` también por query.
- Respuesta correcta: 200 `{message:"Branch deleted successfully", code:"branch/deleted"}`.
- Efectos: (a) borra **todas las responsabilidades activas** del centro, directamente sobre sus documentos (FirestoreBranchRepository.ts:86-94); **no** actualiza `employee.branchId` de los empleados. (b) **Borrado real** del documento del centro (:123-129), no blando. (c) `searchIndex` retirado (dos veces). (d) Evento `branch.deleted`. No existe comprobación previa de que el centro exista.
- Criticidad: alta — destructivo y afecta a los permisos por sucursal.
- Casos:
  - SUC-04-01 · PROP · centro con dos responsables → 200; responsabilidades y centro borrados, `searchIndex` retirado, evento emitido.
  - SUC-04-02 · ADMIN · ídem → 200.
  - SUC-04-03 · PROP · después del borrado, `employee.branchId` de los responsables **sigue conteniendo** el id del centro.
  - SUC-04-04 · PROP · centro con responsabilidades `active:0` → 200, y esas responsabilidades se quedan.
  - SUC-04-05 · PROP · `branchId` inexistente → 200 `branch/deleted`, porque no se comprueba.
  - SUC-04-06 · PROP · sin `branchId` → 400 `{error:"branchId is required", code:"branch/bad_request"}`.
  - SUC-04-07 · PROP · sin `entityId` → 400 `{error:"entityId is required"}`.
  - SUC-04-08 · OP_MANAGER → 403 `{error:"Unauthorized to perform this operation on the entity", code:"auth/unauthorized"}`.
  - SUC-04-09 · AJENO → 403. ANON → 401.
- Sospechas: (1) los empleados se quedan con el centro borrado en `branchId` (la CF igual); (2) borrar un centro inexistente devuelve 200; (3) el centro se borra de verdad, mientras que el empleado solo se da de baja blanda: los fichajes históricos quedan apuntando a un centro que no existe (sin confirmar cómo lo pintan los informes).

## DELETE /api/v1/branches/:branchId  ·  SUC-05
- Servicio: branches, `branch.router.ts:190-192`.
- Consumidores: ninguno detectado.
- Origen: nativo del contenedor (forma REST de SUC-04).
- Diferencias con la CF: sin CF equivalente con esta ruta.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)` con `entityId` en la query o en el cuerpo; 403 si no pasa.
- Entrada: `:branchId` y `?entityId=`.
- Respuesta correcta: 200 `{message:"Branch deleted successfully", code:"branch/deleted"}`.
- Efectos: como SUC-04.
- Criticidad: media — sin consumidor, pero destructivo.
- Casos:
  - SUC-05-01 · PROP · `DELETE /{id}?entityId=e` → 200.
  - SUC-05-02 · PROP · sin `entityId` → 400 `{error:"entityId is required"}`.
  - SUC-05-03 · AJENO → 403. ANON → 401.
- Sospechas: ninguna adicional.

---

# ENT — Empresas (`services/entities`, puerto 3015; el borrado sigue en Cloud Functions)

## POST /api/v1/entities  ·  ENT-01
- Servicio: entities, `api:services/entities/src/interfaces/http/entity.router.ts:56-96`; el asiento de propietario lo da `api:services/entities/src/application/collaborators.ts:30-63`, que llama por S2S a COL-02.
- Consumidores: panel (`NEXT_BACKEND_URI_CREATE_ENTITY`, `front:.env.development:38`; `front:src/services/core/entity.service.ts:113`, proxy `create_entity`).
- Origen: portado desde la CF `cf:firebase-entry-http/entity/create-entity.ts` (controlador `cf:core/entities/interfaces/http/createEntity.controller.ts:48-88`).
- Diferencias con la CF:
  1. El asiento de propietario: la CF escribía `user_entity_roles/{uid}_{entityId}` `{userId, entityId, role:"owner", status:"active", createdAt}` directamente (`createEntity.controller.ts:71-83`). El contenedor llama a checkinbiz con la clave S2S y **con el correo del token**, y el documento lleva además `grantedBy` (el uid), `grantedReason:null` y `support:false`. checkinbiz crea también `users/{uid}` si no existía (`manageCollaborator.ts:76-98`).
  2. **El resultado de `grantSeat` no se mira** (entity.router.ts:85-86): si checkinbiz falla, o el token no trae `email`, la respuesta sigue siendo 201 y la empresa queda sin propietario. En la CF, un fallo de `AddUserToEntity` daba 500.
  3. Excepciones: CF 500 `{error}`, contenedor 500 `internal_error`.
- Autenticación: Firebase ID token.
- Autorización: ninguna más allá de estar autenticado (entity.router.ts:24-28). Cualquier uid con sesión, incluido un usuario de Auth de empleado, puede crear empresas.
- Entrada: `name` (cadena no vacía) y `active` (booleano), obligatorios. `language` opcional (por defecto `"ES"`). **Cualquier otro campo del cuerpo se copia al documento** (`...data`, :70); `slug` se recalcula a partir de `name`.
- Respuesta correcta: 201 `{code:"entity/create_success", message:"Entidad creada", entity:{id, name, slug, language, active, createdAt, ...resto del cuerpo}}`.
- Efectos: (a) `entities/{id}` con `create()` (FirestoreEntityRepository.ts:10-15), con `id` dentro del documento. (b) `searchIndex/entities__{id}` con `name` y `billingEmail`, sin `await`. (c) Llamada S2S `POST http://checkinbiz:3002/api/v1/checkinbiz/collaborators`, que escribe `user_entity_roles/{uid}_{id}` con `role:"owner"` y `status:"active"`.
- Criticidad: alta — el alta de cliente y su primer permiso.
- Casos:
  - ENT-01-01 · usuario autenticado con correo en el token · `{name:"Acme", active:true}` → 201; entidad, `searchIndex` y asiento `owner/active` en `user_entity_roles`.
  - ENT-01-02 · ídem con `language:"EN"` → 201 con `language:"EN"`.
  - ENT-01-03 · ídem con `active:false` → 201 y la entidad nace inactiva.
  - ENT-01-04 · ídem con campos extra (`billingConfig`, `stripeCustomerId`, `branding`) → 201 y se guardan tal cual.
  - ENT-01-05 · ídem con `slug:"otro"` → 201 con `slug` = slugify(name).
  - ENT-01-06 · token sin `email` (por ejemplo, sesión por teléfono) → 201 sin asiento: nadie puede gestionar la empresa.
  - ENT-01-07 · checkinbiz caído, o `ENCODEBIZ_API_KEY` sin definir en entities → 201 sin asiento.
  - ENT-01-08 · sin `name` o `name:"  "` → 400 `{error:"Invalid payload", details:["name is required"]}`.
  - ENT-01-09 · `active:"true"` (cadena) → 400 «active must be a boolean».
  - ENT-01-10 · ANON → 401 `unauthenticated`. TOKEN_INVALIDO → 401.
- Sospechas: (1) asignación masiva: el cuerpo entero acaba en el documento de la entidad, incluidos campos de facturación como `stripeCustomerId` (la CF igual); (2) la empresa se puede quedar sin propietario y la respuesta es 201.

## POST /api/v1/entities/update  ·  ENT-02
- Servicio: entities, `entity.router.ts:100-147` (ruta :150-152: id = `body.id ?? body.entityId`); guardián `requireEntityWriter` :29-40 (`entityId = body.entityId ?? body.id`).
- Consumidores: panel (`NEXT_BACKEND_URI_UPDATE_ENTITY`, `front:.env.development:39`; `entity.service.ts:169`; cuerpo construido en `front:src/app/main/[entityId]/entity/tabs/tabEntity/page.controller.tsx:156-168`, **solo con `id`, sin `entityId`**).
- Origen: portado desde la CF `cf:firebase-entry-http/entity/update-entity.ts` (controlador `cf:core/entities/interfaces/http/updateEntity.controller.ts:59-82`).
- Diferencias con la CF:
  1. **La CF comprobaba `canWrite(uid, req.body.entityId)`** (:62). El panel no manda `entityId`, así que en la CF la comprobación miraba `{uid}_undefined` y respondía **401** siempre. El contenedor usa `entityId ?? id` y responde 201 al PROP y al ADMIN. Es un cambio de comportamiento, favorable al panel (hecho observado en el código; sin confirmar en ejecución).
  2. El `details` de un `active` ausente dice «active is required»; en la CF decía «name is required» (errata, :17).
  3. Nuevo: reindexa `searchIndex` (:144).
  4. Excepciones: CF 500 `{error}`, contenedor 500 `internal_error`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, body.entityId ?? body.id)`; 401 si no pasa. **Se comprueba un id y se escribe otro** cuando llegan los dos (`entityId` para el permiso, `id` para la escritura).
- Entrada: obligatorios `id` (o `entityId`), `name`, `active` (truthy), `slug`, `billingEmail`, `legal.legalName`, `legal.taxId` y `legal.address.{street, postalCode, country, timeZone}`. Opcionales: `language` (por defecto `"ES"`) y `legal.address.geo` (por defecto `null`). Prohibido `branding` (400).
- Respuesta correcta: 201 `{message:"Entity updated"}`.
- Efectos: `set(merge)` de `entities/{id}` con `id, active, name, slug, billingEmail, language, legal`, más `searchIndex/entities__{id}`.
- Criticidad: alta — los datos legales son los que `isConfigured(checkbiz)` exige para operar.
- Casos:
  - ENT-02-01 · PROP · cuerpo del panel (solo `id`) completo → 201.
  - ENT-02-02 · ADMIN · ídem → 201 (sin distinción de rol).
  - ENT-02-03 · PROP · `active:false` → 400 `details:["active is required"]`: no se puede desactivar por aquí.
  - ENT-02-04 · PROP · con `branding:{...}` → 400 «bad request branding param».
  - ENT-02-05 · PROP · sin `legal.taxId` → 400 `{error:"Invalid payload", details:["legal.taxId is required"]}`.
  - ENT-02-06 · PROP · sin `id` ni `entityId` → 400 `{error:"entityId is required"}`.
  - ENT-02-07 · ADMIN de A · `{entityId:"A", id:"B", ...}` con B de otra empresa → 201 y **se sobrescriben los datos legales de B** (entity.router.ts:30 frente a :151).
  - ENT-02-08 · AJENO · `id` de otra entidad → 401 `{error:"No tienes permisos para esta operación en la entidad."}`.
  - ENT-02-09 · OP_MANAGER → 401 (mismo cuerpo).
  - ENT-02-10 · ANON → 401 `unauthenticated`.
- Sospechas: acceso cruzado entre empresas: quien administra A puede editar B mandando `entityId:A` e `id:B`. La CF tenía el mismo defecto con la misma pareja de campos.

## PATCH /api/v1/entities/:entityId  ·  ENT-03
- Servicio: entities, `entity.router.ts:154-156`, la misma función `update` con el id de la ruta.
- Consumidores: ninguno detectado.
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente con esta ruta.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, body.entityId ?? body.id)`. **El id de la ruta no interviene en el permiso.**
- Entrada: como ENT-02, y además hace falta `entityId` o `id` en el cuerpo.
- Respuesta correcta: 201 `{message:"Entity updated"}`.
- Efectos: escribe `entities/{:entityId}`.
- Criticidad: media — sin consumidor, pero con acceso cruzado.
- Casos:
  - ENT-03-01 · PROP · `PATCH /A` con cuerpo completo y `id:"A"` → 201.
  - ENT-03-02 · PROP · `PATCH /A` sin `id` ni `entityId` en el cuerpo → 400 `{error:"entityId is required"}`.
  - ENT-03-03 · ADMIN de A · `PATCH /B` con `entityId:"A"` y cuerpo válido → 201 y se escribe B.
  - ENT-03-04 · AJENO · `PATCH /B` con `entityId:"B"` → 401.
  - ENT-03-05 · ANON → 401.
- Sospechas: acceso cruzado entre empresas: el permiso se mira sobre el cuerpo y la escritura va a la ruta.

## POST /api/v1/entities/branding  ·  ENT-04
- Servicio: entities, `entity.router.ts:162-197`.
- Consumidores: panel (`NEXT_BACKEND_URI_UPDATE_BRANDNG_ENTITY`, `front:.env.development:41`; `entity.service.ts:195`).
- Origen: portado desde la CF `cf:firebase-entry-http/entity/update-entity-branding.ts` (controlador `cf:core/entities/interfaces/http/updateBranding.controller.ts:81-106`).
- Diferencias con la CF: (1) **la CF no comprobaba permiso sobre la entidad**: bastaba una sesión. El contenedor exige `canWrite` y responde 401. (2) La CF aceptaba POST y PATCH (:82); el contenedor solo POST, y un `PATCH /branding` cae en ENT-03 con `:entityId = "branding"`. (3) Excepciones: CF 500 `{message:"Internal Server Error"}`, contenedor 500 `internal_error`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, body.entityId ?? body.id)`, 401 si no pasa; la escritura va a `body.entityId`.
- Entrada: obligatorios `entityId`, `files.logo`, `files.icon`, `files.iconx2` (URLs ya subidas, ver ENT-05), `backgroundColor` y `textColor` (`#RRGGBB`). Opcionales: `labelColor` (hex) y `files.stripImage`.
- Respuesta correcta: 200 `{message:"Branding actualizado correctamente"}`.
- Efectos: `set(merge)` de `entities/{entityId}.branding`.
- Criticidad: media — imagen del cliente (pases, panel).
- Casos:
  - ENT-04-01 · PROP · todos los campos, `labelColor` y `stripImage` incluidos → 200.
  - ENT-04-02 · ADMIN · ídem → 200.
  - ENT-04-03 · PROP · sin `labelColor` o sin `files.stripImage` → la escritura lleva `undefined` y, sin `ignoreUndefinedProperties`, Firestore la rechaza → 500 `{ok:false, error:"internal_error"}` (entity.router.ts:188, :192; sin confirmar en ejecución).
  - ENT-04-04 · PROP · `backgroundColor:"red"` → 400 `{errors:["backgroundColor must be a valid hex color"]}`.
  - ENT-04-05 · PROP · sin `files` → 400 `{errors:["Error files required logo, icon, iconx2", ...]}`.
  - ENT-04-06 · PROP · `backgroundColor: 123` (no cadena) → `.trim` lanza → 500.
  - ENT-04-07 · PROP · sin `entityId` pero con `id` → pasa el guardián y la validación da 400 `errors:["entityId is required"]`.
  - ENT-04-08 · AJENO → 401 `{error:"No tienes permisos para esta operación en la entidad."}`.
  - ENT-04-09 · ANON → 401.
- Sospechas: si el panel no manda `labelColor` o `stripImage` (son opcionales), el guardado falla con 500 en el contenedor. Hay que probarlo en cuanto se pueda: sería una regresión que el panel sí notaría. En la CF está sin confirmar, porque depende de su propia configuración de Firestore.

## POST /api/v1/media  ·  ENT-05
- Servicio: entities, `api:services/entities/src/interfaces/http/media.router.ts:34-85`; lógica en `api:services/entities/src/application/media/media.ts:82-136`. nginx: `location /api/v1/media` con 12 MB (`nginx.staging.conf:197-200`).
- Consumidores: panel (`NEXT_BACKEND_URI_UPLOAD_MEDIA`, `front:.env.development:52-53`; `front:src/services/core/media.service.ts:10`, `fetch` con `FormData` a través del proxy `upload_media`).
- Origen: portado desde la CF `cf:firebase-entry-http/media/upload-media.ts` (controlador `cf:core/media/interfaces/http/uploadMediaController.ts:87-137`).
- Diferencias con la CF: (1) **la CF no comprobaba permiso sobre la entidad**; el contenedor responde 403 `{code:"auth/unauthorized", message:"No access to this entity"}`. (2) Errores internos: CF 400 `{message}`, contenedor 500 `{code:"media/error", message}`. (3) Un error de multipart da 400 `{code:"media/bad_request", message}`.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, fields.entityId)`, después de leer el multipart y validar los campos.
- Entrada: `multipart/form-data` con `entityId`, `type ∈ {logo, background, stripImage, icon, iconx2, custom, thumbnail}` y `file`. MIME: PNG para todos salvo `custom` (jpeg, png, webp, svg, mp4, webm, pdf). Dimensiones exactas: logo 300×300, background 1200×600, stripImage 375×98, icon 26×26, iconx2 58×58, thumbnail 612×612; `custom` no se comprueba.
- Respuesta correcta: 200 `{message:"Media uploaded", mediaId, url}`. `url` es una URL firmada hasta 2050.
- Efectos: fichero en Storage en `media/entities/{entityId}/{type}/{timestamp}-{filename}`; documento `entities/{entityId}/media/{id}` con `uploadedBy` = uid del token.
- Criticidad: media — la marca depende de estas URLs.
- Casos:
  - ENT-05-01 · PROP · PNG de 300×300 con `type:"logo"` → 200 con `mediaId` y `url`.
  - ENT-05-02 · ADMIN · `custom` con PDF → 200.
  - ENT-05-03 · PROP · logo de 200×200 → 400 `{code:"media/invalid_dimesions"}` (sic).
  - ENT-05-04 · PROP · JPEG con `type:"logo"` → 400 `{message:"Invalid MIME type 'image/jpeg' for media type 'logo'"}`.
  - ENT-05-05 · PROP · `type:"banner"` → 400 `{errors:["type must be one of: ..."]}`.
  - ENT-05-06 · PROP · sin fichero → 400 `{errors:["A valid file is required"]}`.
  - ENT-05-07 · PROP · cuerpo JSON en lugar de multipart → 400 `{code:"media/bad_request", message:"Invalid content-type: expected multipart/form-data"}`.
  - ENT-05-08 · PROP · fichero de más de 12 MB → 413 de nginx (no llega al servicio).
  - ENT-05-09 · AJENO · `entityId` ajeno → 403 `{code:"auth/unauthorized", message:"No access to this entity"}`.
  - ENT-05-10 · ANON → 401 `unauthenticated`.
- Sospechas: ninguna.

## DELETE /api/v1/media  ·  ENT-06
- Servicio: entities, `media.router.ts:87-111`; `media.ts:138-154`.
- Consumidores: panel (`NEXT_BACKEND_URI_DELETE_MEDIA`, `front:.env.development:50`; `media.service.ts:103`, con cuerpo `{mediaId, entityId}`).
- Origen: portado desde la CF `cf:firebase-entry-http/media/delete-media.ts` (controlador `cf:core/media/interfaces/http/deleteMediaController.ts:37-64`).
- Diferencias con la CF: (1) **la CF no comprobaba permiso**; el contenedor responde 403. (2) Medio inexistente: 400 `{code:"media/not_found", message:"Media not found"}`; en la CF, sin confirmar (probablemente 500 `media/error`).
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, body.entityId)`.
- Entrada: `mediaId` y `entityId` en el cuerpo.
- Respuesta correcta: 200 `{message:"Media deleted successfully", code:"media/deleted_successfully"}`.
- Efectos: borra el fichero de Storage (si falla, solo se registra) y el documento `entities/{e}/media/{id}`. **No toca `entity.branding`**: si la marca apuntaba a ese fichero, se queda con una URL rota.
- Criticidad: baja — limpieza de ficheros.
- Casos:
  - ENT-06-01 · PROP · medio existente → 200.
  - ENT-06-02 · PROP · `mediaId` inexistente → 400 `media/not_found`.
  - ENT-06-03 · PROP · sin `mediaId` → 400 `{errors:["mediaId is required and must be a string"]}`.
  - ENT-06-04 · AJENO → 403. ANON → 401.
- Sospechas: se puede borrar el logo que usa la marca vigente sin que nadie avise.

## DELETE https://apiv100-firebaseentryhttp-entity-deleteentity-3bnjgtprva-uc.a.run.app  ·  ENT-07
- Servicio: **sigue en Cloud Functions**: `cf:firebase-entry-http/entity/delete-entity.ts`, controlador `cf:core/entities/interfaces/http/deleteEntity.controller.ts:38-70`. No hay ruta equivalente en el contenedor (`api:services/entities/src/interfaces/http/entity.router.ts:15-18`).
- Consumidores: panel (`NEXT_BACKEND_URI_DELETE_ENTITY`, `front:.env.development:40`; `front:src/services/core/entity.service.ts:235-260`, proxy `delete_entity` con `DELETE` y cuerpo `{uid, entityId}`, llamado desde `front:src/app/main/[entityId]/entity/page.controller.tsx:41-44`).
- Origen: sigue en Cloud Functions.
- Diferencias con la CF: no aplica (es la CF).
- Autenticación: `validateUserToken`: ID token, más las claims `admin` y `twoFA` solo si `Origin` es del panel (`validateUserToken.ts:35-47`). A través del proxy no se reenvía `Origin`.
- Autorización: **ninguna**. El controlador no llama a `canWrite` ni mira el rol (deleteEntity.controller.ts:38-66).
- Entrada: cuerpo `{entityId}` (cadena). `uid` se ignora.
- Respuesta correcta: 201 `{message:"Entidad creada"}` (sic).
- Efectos: (a) si `InvoicePaymentProcessor` detecta pagos pendientes, 400 y no se borra nada (:55-57). (b) `delete` del documento `entities/{entityId}` (`cf:core/entities/infrastructure/repositories/FirestoreEntityRepository.ts:18-20`); **las subcolecciones (employees, branches, checklogs…) no se tocan**. (c) Borra **solo el asiento de quien llama**, `user_entity_roles/{uid}_{entityId}`; los demás colaboradores conservan el suyo. (d) El disparador `cf:firebase-firestore-trigger/entities/onDelete.ts:5-14` solo borra la entrada de `searchIndex` de la entidad. Los usuarios de Auth de los empleados no se tocan.
- Criticidad: alta — destructivo y sin control de permisos.
- Casos:
  - ENT-07-01 · PROP · sin pagos pendientes → 201 `{message:"Entidad creada"}`; desaparece el documento de la entidad y el asiento del PROP; empleados, centros y el resto de asientos siguen en Firestore.
  - ENT-07-02 · ADMIN · ídem → 201 (sin distinción de rol).
  - ENT-07-03 · AJENO · `entityId` de una empresa ajena sin pagos pendientes → 201 y **la borra**.
  - ENT-07-04 · OP_WORKER con cuenta de Auth → 201 (no se mira nada).
  - ENT-07-05 · PROP · con pagos pendientes → 400 `{error:"You have pending payments.", code:"payment/pending"}`.
  - ENT-07-06 · PROP · sin `entityId` → 400 `{error:"Invalid payload", details:["entityId is required"]}`.
  - ENT-07-07 · PROP · `entityId` inexistente → 201 (el borrado de un documento inexistente no falla; sin confirmar qué hace `InvoicePaymentProcessor` en ese caso).
  - ENT-07-08 · ANON → 401 `{message:"Invalid token", code:"auth/unauthorized"}`.
  - ENT-07-09 · TOKEN_INVALIDO → 401 `{message:"Invalid token", code:"auth/invalid_token"}`.
  - ENT-07-10 · ANON vía panel → 403 `{code:"auth/forbidden"}` del proxy.
- Sospechas: (1) cualquier usuario autenticado puede borrar cualquier empresa sin pagos pendientes; (2) el borrado deja huérfanos a empleados, centros y asientos de colaboradores. El comentario del contenedor habla de una cascada (`entity.router.ts:15-18`), pero el único disparador sobre `entities/{eid}` que se ha encontrado solo limpia `searchIndex`; (3) responde «Entidad creada» a un borrado.

---

# COL — Colaboradores del panel (`user_entity_roles`, invitaciones, fichas de usuario)

Dueño de `user_entity_roles`: checkinbiz (`api:services/checkinbiz/src/interfaces/http/collaborator/collaborator.router.ts`, montado **antes** de `requireFirebaseAuth` en `api:services/checkinbiz/src/app.ts:40`). Su guardián `requireEntityWriter` (`collaborator.router.ts:74-99`), en este orden: (1) `entityId` en el cuerpo o la query, si falta 400 `{ok:false, error:"entityId is required"}`; con `/`, `.` o `..` 400 `invalid entityId`; (2) si llega `x-encodebiz-key`, tiene que valer (si no, 401 `{ok:false, error:"unauthorized"}`) y entra como servicio; (3) si no, ID token vía `validateToken` de shared (sin `checkRevoked`), con 401 `{message:"Invalid token", code:"auth/unauthorized" | "auth/invalid_token"}`, y además hace falta un asiento **activo** de `owner` o `admin` en esa entidad; si no, 403 `{ok:false, error:"forbidden"}`. Es la única puerta de la parcela que mira `status`.

## POST /api/v1/entities/collaborators  ·  COL-01
- Servicio: entities, `api:services/entities/src/interfaces/http/collaborator.router.ts:28-115` (montado en `app.ts:28`); el asiento lo da `api:services/entities/src/application/collaborators.ts:30-63`, que llama a COL-02.
- Consumidores: panel (`NEXT_BACKEND_URI_ASSING_USER`, `front:.env.development:35`; `front:src/services/core/entity.service.ts:269`, proxy `assing_user`; rol `"admin" | "owner"` en `front:src/app/main/[entityId]/entity/tabs/tabCollaborators/page.controller.tsx:18-19, :42-47`).
- Origen: portado desde la CF `cf:firebase-entry-http/users/assing-user.ts` (controlador `cf:core/users/interfaces/http/assignUser.controller.ts:60-132`).
- Diferencias con la CF:
  1. **Permiso**: la CF solo comprobaba `canWrite` si el cuerpo traía `uid` (:63-68), y el envoltorio no lo inyectaba, así que sin `uid` en el cuerpo **no había ninguna comprobación**. El contenedor comprueba siempre `canWrite(uid del token)` y responde 401.
  2. **Ya es colaborador**: la CF llamaba a `AddUserToEntity`, que lanza `auth/authentication_already_exists` (`cf:core/auth/application/use-cases/AddUserToEntity.ts:8-10`), y respondía 500 `{error:"{\"code\":\"auth/authentication_already_exists\"}"}`. El contenedor responde **409** `{code:"auth/seat_failed", error:"already_member"}`.
  3. **Rol**: la CF aceptaba cualquier cadena. El contenedor solo `owner` o `admin`; con otro, 400 `{code:"auth/seat_failed", error:"invalid_role"}`, **después** de haber creado la cuenta de Auth y `users/{uid}`.
  4. **Enlace**: la CF usaba `https://saas.encodebiz.com` fijo, el panel de producción también en desarrollo (:124). El contenedor lo toma de `SAAS_BASE_URL`, y si falta responde 500 `{code:"auth/invite_link_missing"}` con el asiento ya creado.
  5. El correo se normaliza a minúsculas.
- Autenticación: Firebase ID token.
- Autorización: `canWrite(uid, entityId)` (:42-44), 401 si no pasa. **ADMIN puede invitar con rol `owner`.**
- Entrada: `email`, `role` y `entityId`, los tres obligatorios.
- Respuesta correcta: 201 `{code:"auth/user_asigned", message:"User was added success"}`.
- Efectos: (a) si el correo no existe en Auth: `createUser({email, displayName:"Guest"})`, sin contraseña, más `users/{uid}` `{fullName:"Guest", phoneNumber:"-", active:true}` (:59-71); (b) S2S a checkinbiz: `user_entity_roles/{uid}_{entityId}` con `status:"invited"` y `grantedBy` = el uid de quien invita; (c) custom token de Firebase y correo SMTP `WELLCOME_COLLABORATOR` con `iviteLink = {SAAS_BASE_URL}/auth/login?authToken={customToken}`, en el idioma de la entidad.
- Criticidad: alta — reparte permisos de gestión y crea identidades.
- Casos:
  - COL-01-01 · PROP · correo nuevo con `role:"admin"` → 201; cuenta Guest, `users/{uid}`, asiento `admin/invited` y correo de invitación.
  - COL-01-02 · PROP · correo de una cuenta ya existente en Auth que no es miembro → 201; no se crea cuenta y el asiento queda `invited`.
  - COL-01-03 · ADMIN · `role:"owner"` → 201: un administrador puede invitar propietarios.
  - COL-01-04 · ADMIN_INVITADO · → 201 (`canWrite` no mira `status`).
  - COL-01-05 · PROP · alguien que ya tiene asiento en la entidad → 409 `{code:"auth/seat_failed", error:"already_member"}`; no se reenvía el correo.
  - COL-01-06 · PROP · `role:"member"` con correo nuevo → 400 `{code:"auth/seat_failed", error:"invalid_role"}`, y la cuenta Guest y `users/{uid}` **quedan creadas**.
  - COL-01-07 · PROP · `email:"Ana@X.COM"` → 201; asiento y cuenta con `ana@x.com`.
  - COL-01-08 · PROP · `email:"foo"` → `createUser` lanza → 500 `{ok:false, error:"internal_error"}`.
  - COL-01-09 · PROP · falta `email`, `role` o `entityId` → 400 `{error:"Invalid payload", details:[...]}`.
  - COL-01-10 · PROP · `SAAS_BASE_URL` sin definir → 500 `{code:"auth/invite_link_missing"}` y el asiento `invited` ya está escrito.
  - COL-01-11 · PROP · checkinbiz caído → 502 `{code:"auth/seat_failed", error:"seat_service_unavailable"}`; si el correo era nuevo, la cuenta Guest queda creada.
  - COL-01-12 · PROP · falla el SMTP → `sendEmail` lanza → 500 `internal_error`, con el asiento ya escrito.
  - COL-01-13 · OP_MANAGER → 401 `{error:"No tienes permisos para esta operación en la entidad."}`.
  - COL-01-14 · AJENO · `entityId` ajeno → 401 (mismo cuerpo).
  - COL-01-15 · ANON → 401 `unauthenticated`. TOKEN_INVALIDO → 401.
- Sospechas: (1) no se distingue PROP de ADMIN: un administrador reparte propiedad; (2) varios fallos dejan efectos a medias (cuenta Guest sin asiento, asiento sin correo); (3) si el invitado ya tenía cuenta, recibe un enlace con custom token para entrar sin contraseña: el enlace del correo **es** una credencial.

## POST /api/v1/checkinbiz/collaborators  ·  COL-02
- Servicio: checkinbiz, `collaborator.router.ts:122-153`; caso de uso `api:services/checkinbiz/src/application/use-cases/auth/manageCollaborator.ts:120-148`.
- Consumidores: S2S. Lo usan entities, para el propietario al crear empresa y para invitar (`collaborators.ts:42-52`), y el backoffice (`api:services/backoffice/src/infrastructure/clients/CheckinbizClient.ts:59-72`). El panel no: la allowlist solo tiene DELETE (`serverBackendProxy.ts:124-129`).
- Origen: nativo del contenedor (la mitad de permisos de `assignUser`).
- Diferencias con la CF: sin CF equivalente directa.
- Autenticación: S2S (`x-encodebiz-key`) o Firebase ID token.
- Autorización: servicio, o asiento activo `owner` o `admin` en `entityId`. **No distingue PROP de ADMIN** para el rol que se concede.
- Entrada: `entityId` (cuerpo o query), `email` (con `@`), `role ∈ {owner, admin}`. Opcionales: `status ∈ {active, invited}` (por defecto `active`), y `grantedBy`, `reason` (≤ 500) y `support`, que **se aceptan también por la vía del token** (:144-146).
- Respuesta correcta: 201 `{ok:true, collaborator:{id, userId, entityId, role, status, createdAt, grantedBy, grantedReason, support, account:{uid, email, fullName}}}`.
- Efectos: `user_entity_roles/{uid}_{entityId}` con `set` completo (`FirestoreEntityMembershipRepository.ts:59-79`); `users/{uid}` si no existía (`manageCollaborator.ts:76-98`).
- Criticidad: alta — es la escritura de permisos de toda la plataforma.
- Casos:
  - COL-02-01 · S2S · cuenta existente que no es miembro, `role:"owner"` → 201 `status:"active"`.
  - COL-02-02 · S2S · `status:"invited"` → 201 `status:"invited"`.
  - COL-02-03 · PROP · cuenta existente, `role:"admin"` → 201.
  - COL-02-04 · ADMIN · `role:"owner"` → 201: un administrador concede propiedad.
  - COL-02-05 · ADMIN · `grantedBy:"soporte:x@y"` y `support:true` → 201 con esas marcas falsificadas.
  - COL-02-06 · ADMIN_INVITADO → 403 `{ok:false, error:"forbidden"}`.
  - COL-02-07 · ADMIN_DESACTIVADO → 403 `forbidden`.
  - COL-02-08 · OP_MANAGER → 403 `forbidden` (sin asiento). AJENO → 403.
  - COL-02-09 · S2S con clave errónea → 401 `{ok:false, error:"unauthorized"}`, sin probar la vía del token.
  - COL-02-10 · ANON · con `entityId` → 401 `{message:"Invalid token", code:"auth/unauthorized"}`. TOKEN_INVALIDO → 401 `code:"auth/invalid_token"`.
  - COL-02-11 · ANON · sin `entityId` → 400 `entityId is required`: se valida antes que la auth.
  - COL-02-12 · S2S · `entityId:"a/b"` → 400 `invalid entityId`.
  - COL-02-13 · S2S · `email:"sinArroba"` → 400 `email is required`. `role:"viewer"` → 400 `invalid_role`. `status:"disabled"` → 400 `invalid_status`.
  - COL-02-14 · S2S · correo sin cuenta en Auth → 404 `{ok:false, error:"user_not_found"}`.
  - COL-02-15 · S2S · entidad inexistente → 404 `entity_not_found`.
  - COL-02-16 · S2S · ya es miembro → 409 `{ok:false, error:"already_member", role}`.
- Sospechas: **CONFIRMADO — HAL-21**: por esta vía un administrador concede el rol `owner` (COL-02-04), a cualquiera y sin ser propietario. Y además, por la vía del token, quien llama puede escribir `grantedBy`, `reason` y `support`, que son las marcas de auditoría que distinguen un asiento de soporte.

## GET /api/v1/checkinbiz/collaborators/one?entityId=&email=  ·  COL-03
- Servicio: checkinbiz, `collaborator.router.ts:108-114`; `manageCollaborator.ts:107-118`.
- Consumidores: S2S (backoffice, `CheckinbizClient.ts:51-56`). El panel no.
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: S2S o Firebase ID token.
- Autorización: servicio, o asiento activo `owner` o `admin` en `entityId`.
- Entrada: query `entityId` y `email`.
- Respuesta correcta: 200 `{ok:true, account:{uid, email, fullName} | null, membership:{...} | null}`.
- Efectos: ninguno.
- Criticidad: baja — lectura de soporte.
- Casos:
  - COL-03-01 · S2S · correo de un miembro → 200 con `account` y `membership`.
  - COL-03-02 · PROP · correo de una cuenta que existe pero no es miembro → 200 con `account` relleno y `membership:null`.
  - COL-03-03 · PROP · correo sin cuenta → 200 `{account:null, membership:null}`.
  - COL-03-04 · PROP · sin `email` → 400 `{ok:false, error:"email is required"}`.
  - COL-03-05 · ADMIN_INVITADO → 403. AJENO → 403. ANON → 401.
- Sospechas: cualquier administrador activo de cualquier entidad puede consultar si un correo tiene cuenta en la plataforma, y obtener su uid y su nombre, aunque esa persona no tenga nada que ver con su empresa (enumeración de cuentas).

## PATCH /api/v1/checkinbiz/collaborators/:userId  ·  COL-04
- Servicio: checkinbiz, `collaborator.router.ts:162-183`; `manageCollaborator.ts:167-194`.
- Consumidores: ninguno detectado. El panel acepta invitaciones escribiendo Firestore desde el navegador (`entity.service.ts:64-81`), y el proxy no deja pasar PATCH.
- Origen: sustituye a la CF `cf:firebase-entry-http/auth/update-auth.ts` (controlador `cf:core/auth/interfaces/http/updateAuthUser.controller.ts:53-73`).
- Diferencias con la CF: (1) la CF recibía `{entityId, userId, role?, status?}` en el cuerpo y respondía 200 `{code:"auth/updated_success", message:"Update authentication"}`; el contenedor lleva `userId` en la ruta y responde 200 `{ok:true, collaborator}`; (2) sin permiso, la CF daba 401 `{code:"auth/unauthorized", error:"Unauthorized"}` y el contenedor 403 `{ok:false, error:"forbidden"}`, y además exige asiento **activo**; (3) la CF aceptaba cualquier `role` o `status`, el contenedor valida los dos; (4) nuevo: protección de `last_owner` también al rebajar o desactivar; (5) nuevo: 404 `not_member` (la CF escribía con merge y creaba el documento).
- Autenticación: S2S o Firebase ID token.
- Autorización: servicio, o asiento activo `owner` o `admin`. **No mira el rol de quien llama frente al del afectado.**
- Entrada: `entityId` (cuerpo o query); opcionales `role ∈ {owner, admin}` y `status ∈ {active, invited, disabled}`.
- Respuesta correcta: 200 `{ok:true, collaborator:{...asiento con los cambios}}`.
- Efectos: `set(changes, merge)` sobre `user_entity_roles/{userId}_{entityId}`.
- Criticidad: alta — cambia permisos; alcanzable con cualquier ID token de administrador aunque el panel no lo use.
- Casos:
  - COL-04-01 · PROP · un ADMIN pasa a `owner` → 200.
  - COL-04-02 · ADMIN · **se asciende a sí mismo** a `owner` (`PATCH /{suUid}`, `{entityId, role:"owner"}`) → 200.
  - COL-04-03 · ADMIN · rebaja a un PROP a `admin` habiendo otro propietario activo → 200.
  - COL-04-04 · ADMIN · desactiva (`status:"disabled"`) a un PROP habiendo otro propietario activo → 200.
  - COL-04-05 · PROP · se rebaja a `admin` siendo el único propietario activo → 409 `{ok:false, error:"last_owner"}`.
  - COL-04-06 · PROP · desactiva a un propietario **invitado** cuando solo hay un propietario activo, que es otro → 409 `last_owner`: el recuento incluye a propietarios que no son el afectado (manageCollaborator.ts:177-181).
  - COL-04-07 · PROP · cuerpo sin `role` ni `status` → 200 con el asiento sin cambios.
  - COL-04-08 · PROP · `userId` sin asiento → 404 `{ok:false, error:"not_member"}`.
  - COL-04-09 · PROP · `role:"viewer"` → 400 `invalid_role`. `status:"deleted"` → 400 `invalid_status`.
  - COL-04-10 · S2S · `status:"active"` para aceptar una invitación → 200.
  - COL-04-11 · ADMIN_INVITADO · intenta aceptar su propia invitación por aquí → 403 `forbidden`: la puerta exige asiento activo.
  - COL-04-12 · AJENO → 403. ANON → 401 `auth/unauthorized`.
- Sospechas: (1) **CONFIRMADO — HAL-21. Escalada de privilegios**: un administrador puede hacerse propietario, o rebajar y desactivar a un propietario, porque `updateCollaborator` no recibe al actor (la baja por DELETE sí lo protege con `owner_required`); (2) el recuento de `last_owner` bloquea operaciones legítimas sobre propietarios invitados; (3) la ruta que sustituye a `updateAuth` no la usa nadie: aceptar invitaciones sigue siendo una escritura del navegador en Firestore.

## DELETE /api/v1/checkinbiz/collaborators/:userId?entityId=  ·  COL-05
- Servicio: checkinbiz, `collaborator.router.ts:191-214`; `manageCollaborator.ts:204-233`.
- Consumidores: panel (`NEXT_BACKEND_URI_CHECKINBIZ_COLLABORATORS_HANDLER`, `front:.env.development:151`; `front:src/services/core/entity.service.ts:330-343`, proxy `checkinbiz_collaborators_handler/{uid}?entityId=`, con subruta limitada a `[A-Za-z0-9_-]{1,128}` en `serverBackendProxy.ts:124-129`) / S2S (backoffice, `CheckinbizClient.ts:73-76`).
- Origen: nativo del contenedor. Antes el panel borraba el documento desde el navegador (`serverBackendProxy.ts:119-123`).
- Diferencias con la CF: sin CF equivalente.
- Autenticación: S2S o Firebase ID token.
- Autorización: servicio, o asiento activo `owner` o `admin`. **Aquí sí se distingue**: a un propietario solo lo quita otro propietario (:215-217), y nunca al último propietario activo (:224-229), tampoco por S2S.
- Entrada: `:userId` y `entityId` (query).
- Respuesta correcta: 200 `{ok:true, removed:{id, userId, entityId, role, status, createdAt, grantedBy, grantedReason, support}}`.
- Efectos: borra `user_entity_roles/{userId}_{entityId}` y deja traza en consola. No toca Auth ni `users/{uid}`.
- Criticidad: alta — retira permisos desde el panel.
- Casos:
  - COL-05-01 · PROP · quita a un ADMIN → 200.
  - COL-05-02 · ADMIN · quita a otro ADMIN → 200.
  - COL-05-03 · ADMIN · se quita a sí mismo → 200.
  - COL-05-04 · ADMIN · quita a un PROP → 403 `{ok:false, error:"owner_required"}`.
  - COL-05-05 · ADMIN · quita a un propietario **invitado** → 403 `owner_required`.
  - COL-05-06 · PROP · quita a otro PROP activo (hay dos) → 200.
  - COL-05-07 · PROP · se quita a sí mismo siendo el único propietario activo → 409 `{ok:false, error:"last_owner"}`.
  - COL-05-08 · PROP · quita a un propietario invitado siendo él el único activo → 200.
  - COL-05-09 · S2S · quita al único propietario activo → 409 `last_owner`.
  - COL-05-10 · PROP · `userId` sin asiento → 404 `not_member`.
  - COL-05-11 · PROP · `userId` = `..` (llamada directa, sin proxy) → 400 `invalid userId`.
  - COL-05-12 · PROP · sin `?entityId` → 400 `entityId is required`.
  - COL-05-13 · ADMIN_INVITADO → 403 `forbidden`. OP_MANAGER → 403. AJENO → 403.
  - COL-05-14 · ANON (directo) → 401 `auth/unauthorized`. ANON vía panel → 403 del proxy.
- Sospechas: ninguna nueva. Es el único punto donde la distinción entre propietario y administrador está bien protegida.

## POST /api/v1/checkinbiz/collaborators/session  ·  COL-06
- Servicio: checkinbiz, `collaborator.router.ts:228-251`.
- Consumidores: S2S (backoffice, `CheckinbizClient.openSession`, usado por COL-12).
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: solo S2S (`x-encodebiz-key`).
- Autorización: la clave, y que exista el asiento. **No mira el `status` del asiento.**
- Entrada: `entityId` (cuerpo o query) y `email`.
- Respuesta correcta: 200 `{ok:true, customToken, uid, expiresInMin:60}`.
- Efectos: emite un custom token de Firebase para esa cuenta.
- Criticidad: alta — es un token para entrar como otra persona.
- Casos:
  - COL-06-01 · S2S · cuenta con asiento → 200 con `customToken`.
  - COL-06-02 · S2S · asiento `disabled` o `invited` → 200 igualmente.
  - COL-06-03 · S2S · cuenta sin asiento → 409 `{ok:false, error:"not_member"}` (409 aquí, 404 en el resto del router).
  - COL-06-04 · S2S · correo sin cuenta → 404 `user_not_found`.
  - COL-06-05 · S2S · falta `email` o `entityId` → 400 `{ok:false, error:"entityId and email are required"}`.
  - COL-06-06 · PROP con ID token, sin clave → 401 `{ok:false, error:"unauthorized"}`.
  - COL-06-07 · ANON → 401 `unauthorized`.
- Sospechas: con la clave S2S se emite un token para cualquier cuenta que tenga asiento, sea cual sea su estado; toda la política de quién puede pedirlo vive en el backoffice.

## POST /api/v1/users  ·  COL-07
- Servicio: entities, `api:services/entities/src/interfaces/http/user.router.ts:19-66` (montado en `app.ts:31`); repositorio `api:services/entities/src/infrastructure/FirestoreUserRepository.ts:21-24`.
- Consumidores: panel (`NEXT_BACKEND_URI_CREATE_USER`, `front:.env.development:33`). La usan la ruta de servidor `front:src/app/api/auth/register/route.ts:38-48, :142-153`, con el ID token de la cuenta recién creada y `uid` en el cuerpo, y `front:src/services/core/account.service.ts:104-116` (proxy `create_user`, completar perfil, también con `uid`).
- Origen: portado desde la CF `cf:firebase-entry-http/users/create-users.ts` (controlador `cf:core/users/interfaces/http/createUser.controller.ts:40-95`).
- Diferencias con la CF: (1) **la CF pisaba `body.uid` con el uid del token** (`create-users.ts:17`), así que nunca faltaba ni podía ser ajeno. El contenedor exige `uid` en el cuerpo (400 si falta) y responde 403 `{error:"uid mismatch", code:"auth/unauthorized"}` si no coincide con el token. Un cliente que no mande `uid` funcionaba en la CF y aquí recibe 400. (2) Si falla el correo de bienvenida: la CF lo esperaba sin `catch` (500); el contenedor lo registra y responde 201. (3) Sin token: la CF daba 401 `{message:"Missing authorization token", code:"auth/unauthorized"}` y el contenedor 401 `{error:"unauthenticated"}`.
- Autenticación: Firebase ID token.
- Autorización: `body.uid` tiene que ser el uid del token (:28-30).
- Entrada: `uid`, `fullName`, `email` y `phoneNumber`, los cuatro obligatorios.
- Respuesta correcta: 201 `{message:"Usuario creado"}`.
- Efectos: `users/{uid}` con `set` **completo** `{uid, email, fullName, phoneNumber, createdAt, lastLoginAt, active:true}`. Correo `WELLCOME_EMAIL` solo si el uid **no tiene ningún** documento en `user_entity_roles`, en cualquier estado (:54-63, :68-77).
- Criticidad: alta — el alta de cuenta del panel.
- Casos:
  - COL-07-01 · usuario recién registrado (uid del token = `body.uid`), sin asientos → 201; `users/{uid}` y correo de bienvenida.
  - COL-07-02 · usuario invitado (tiene asiento `invited`) completando el perfil → 201 sin correo de bienvenida.
  - COL-07-03 · usuario existente que vuelve a llamar → 201 y `users/{uid}` **se reescribe entero**: se pierden los campos que no estén en el cuerpo, como `twoFA` o `photoURL`.
  - COL-07-04 · `body.uid` de otra persona → 403 `{error:"uid mismatch", code:"auth/unauthorized"}`.
  - COL-07-05 · sin `uid` → 400 `{error:"Invalid payload", details:["uid is required"]}`.
  - COL-07-06 · sin `phoneNumber` → 400 `details` con «phoneNumber is required».
  - COL-07-07 · falla el SMTP → 201 igualmente.
  - COL-07-08 · ANON → 401 `unauthenticated`. TOKEN_INVALIDO → 401.
  - COL-07-09 · vía proxy sin cabecera `cf-turnstile-response` válida → 403 `{code:"turnstile/failed"}` del proxy (`serverBackendProxy.ts:539-549`).
- Sospechas: el `set` sin merge borra datos de perfil ya guardados si la ruta se llama dos veces (sin confirmar si la CF usaba también `set` sin merge).

## POST /api/v1/users/recovery  ·  COL-08
- Servicio: entities, `api:services/entities/src/interfaces/http/user.router.ts:167-216` (router público, `app.ts:22`).
- Consumidores: panel (`NEXT_BACKEND_URI_RECOVERY_PASS`, `front:.env.development:34`; `front:src/services/core/account.service.ts:56`, proxy `recovery_pass` con Turnstile y sin token). La **app no** usa esta ruta: sigue llamando a la CF (`AppConstants.recoveryPassEndpoint`, `app:lib/core/constants/app_constants.dart:65-67`; uso en `app:lib/features/auth/data/datasources/auth_remote_datasource.dart:175`).
- Origen: portado desde la CF `cf:firebase-entry-http/users/recovery-pass-users.ts:76-114` (controlador `cf:core/users/interfaces/http/recoveryPass.controller.ts:6-30`).
- Diferencias con la CF: (1) la IP del límite sale de `X-Real-IP`; en la CF, de `req.ip`. A través del proxy del panel esa IP es la del servidor de Next, porque el proxy no reenvía la del navegador, y el cubo queda en la práctica por correo. (2) El contenedor busca el correo en `users` y, si no está, entre los empleados (`collectionGroup("employees")`, FirestoreUserRepository.ts:39-50); sin confirmar que la CF (`FindUser`) mire empleados. (3) El contenedor manda el enlace por SMTP en el acto; la CF lo delegaba (sin confirmar el mecanismo de `RecoverPassUser`). Los cuerpos y los estados coinciden.
- Autenticación: ninguna.
- Autorización: ninguna. Límite de 3 intentos por (correo, IP) cada 15 minutos (:94-96, :136-165).
- Entrada: `email` obligatorio y con formato válido. Cabecera `locale` (`en` o, por defecto, `es`).
- Respuesta correcta: 200 `{code:"auth/recover_accepted", message:"If the account exists, a recovery link will be sent."}`, exista o no la cuenta.
- Efectos: `security_rate_limits/recover_{sha(email)}_{sha(ip)}` en una transacción. Si hay cuenta, enlace de restablecimiento de Firebase y correo `RECOVER_PASS` en el idioma pedido.
- Criticidad: alta — pública; la usan panel y empleados.
- Casos:
  - COL-08-01 · ANON · correo de usuario del panel → 200 genérico; correo con `linkpassrecover`.
  - COL-08-02 · ANON · correo de un empleado sin ficha en `users` → 200; también se le manda.
  - COL-08-03 · ANON · correo inexistente → 200 con el mismo cuerpo, sin correo.
  - COL-08-04 · ANON · `locale: en` → 200 y plantilla en inglés.
  - COL-08-05 · ANON · cuarto intento con el mismo correo y la misma IP en menos de 15 minutos → 429 `{error:"Too many recovery attempts"}`.
  - COL-08-06 · ANON · sin `email` → 400 `{error:"Email is required"}`.
  - COL-08-07 · ANON · `email:"x@"` → 400 `{error:"Invalid email"}`.
  - COL-08-08 · ANON · falla el SMTP → 200 genérico (el fallo solo se registra).
  - COL-08-09 · ANON vía panel sin Turnstile → 403 `{code:"turnstile/failed"}`.
- Sospechas: la migración está a medias entre clientes: el panel va al contenedor y la app a la CF.

## GET /api/v1/backoffice/entities/:entityId/support  ·  COL-09
- Servicio: backoffice, `api:services/backoffice/src/interfaces/http/modules/entitySupport.router.ts:42-72` (montado en `entities.router.ts:52`, bajo `backoffice.router.ts:18,22` con `requireStaff`).
- Consumidores: SPA del backoffice (ni panel ni app).
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: Firebase ID token más `backoffice_users` activo (`requireStaff.ts:33-65`).
- Autorización: permiso `entities:read` (`requirePermission`, :73-86).
- Entrada: `:entityId`.
- Respuesta correcta: 200 `{ok:true, cuenta, exigeCodigo, asiento:{userId, rol, desde, concedidoPor, motivo, deSoporte} | null}`.
- Efectos: apunte de auditoría. S2S a COL-03 con el correo de soporte (`BACKOFFICE_SUPPORT_EMAIL`, por defecto `support@encodebiz.com`, `supportAccess.ts:14`).
- Criticidad: media — acceso de soporte.
- Casos:
  - COL-09-01 · STAFF_BO · entidad sin asiento de soporte → 200 `asiento:null`.
  - COL-09-02 · STAFF_BO · con asiento → 200 con los datos del asiento.
  - COL-09-03 · STAFF_BO_SIN_PERMISO → 403 `{ok:false, error:"forbidden", missing:"entities:read"}`.
  - COL-09-04 · PROP (no es personal) → 403 `{ok:false, error:"forbidden"}`.
  - COL-09-05 · ANON → 401 `unauthenticated`.
  - COL-09-06 · STAFF_BO · checkinbiz caído → 502 `{ok:false, error:"checkinbiz_inalcanzable"}`.
- Sospechas: ninguna.

## POST /api/v1/backoffice/entities/:entityId/support  ·  COL-10
- Servicio: backoffice, `entitySupport.router.ts:85-137`.
- Consumidores: SPA del backoffice.
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: igual que COL-09.
- Autorización: permiso `support-access:write`. Con `BACKOFFICE_SUPPORT_REQUIRE_GRANT=1`, además, una ventana de permiso abierta del cliente (`supportAccess.ts:26`; hoy apagado según el comentario, :81-83).
- Entrada: `reason` opcional (3–500 caracteres o `null`).
- Respuesta correcta: 201 `{ok:true, asiento:{...colaborador}}`.
- Efectos: S2S a COL-02 con `role:"admin"` (`SUPPORT_ROLE`, `supportAccess.ts:29`), `grantedBy:"soporte:{correo del staff}"`, `support:true`. Apunte de auditoría.
- Criticidad: media.
- Casos:
  - COL-10-01 · STAFF_BO · entidad existente sin asiento de soporte → 201.
  - COL-10-02 · STAFF_BO · ya tiene asiento → 409 `{ok:false, error:"already_member"}`.
  - COL-10-03 · STAFF_BO · la cuenta de soporte no existe en Auth → 404 `user_not_found`.
  - COL-10-04 · STAFF_BO · entidad inexistente → 404 `{ok:false, error:"not_found"}`.
  - COL-10-05 · STAFF_BO · `reason:"ab"` → 400 `invalid_body`.
  - COL-10-06 · STAFF_BO · con la ventana obligatoria activada y sin ventana abierta → 403 `authorization_required`.
  - COL-10-07 · STAFF_BO_SIN_PERMISO → 403 `missing:"support-access:write"`. ANON → 401.
- Sospechas: ninguna.

## DELETE /api/v1/backoffice/entities/:entityId/support  ·  COL-11
- Servicio: backoffice, `entitySupport.router.ts:140-167`.
- Consumidores: SPA del backoffice.
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: igual que COL-09.
- Autorización: `support-access:write`.
- Entrada: `:entityId`.
- Respuesta correcta: 200 `{ok:true}`.
- Efectos: COL-03 y después COL-05 por S2S. Borra el asiento de soporte.
- Criticidad: media.
- Casos:
  - COL-11-01 · STAFF_BO · con asiento → 200.
  - COL-11-02 · STAFF_BO · sin asiento → 404 `{ok:false, error:"not_member"}`.
  - COL-11-03 · STAFF_BO · el asiento de soporte es el único propietario activo (caso raro) → 409 `last_owner`, que el backoffice deja pasar tal cual.
  - COL-11-04 · STAFF_BO_SIN_PERMISO → 403. ANON → 401.
- Sospechas: ninguna.

## POST /api/v1/backoffice/entities/:entityId/support/session  ·  COL-12
- Servicio: backoffice, `entitySupport.router.ts:175-207`.
- Consumidores: SPA del backoffice.
- Origen: nativo del contenedor.
- Diferencias con la CF: sin CF equivalente.
- Autenticación: igual que COL-09.
- Autorización: `support-access:write`.
- Entrada: `:entityId`.
- Respuesta correcta: 200 `{ok:true, url, caducaEnMin:60}`, donde `url` es el login del SaaS con el custom token.
- Efectos: COL-06 por S2S y apunte de auditoría.
- Criticidad: media — suplantación controlada.
- Casos:
  - COL-12-01 · STAFF_BO · con asiento de soporte → 200 con `url`.
  - COL-12-02 · STAFF_BO · sin asiento → 409 `not_member`.
  - COL-12-03 · STAFF_BO · sin URL del SaaS configurada → 503 `{ok:false, error:"saas_no_configurado"}`.
  - COL-12-04 · STAFF_BO_SIN_PERMISO → 403. ANON → 401.
- Sospechas: ninguna.

---

## Resumen
- Endpoints: 37 (EMP 13, SUC 5, ENT 7, COL 12). Consumidos por clientes: 20, todos del panel: EMP-01, 03, 04, 06, 09, 10, 11 · SUC-01, 02, 04 · ENT-01, 02, 04, 05, 06, 07 · COL-01, 05, 07, 08. La app no consume ningún endpoint del contenedor de esta parcela: valida contra `checkinbiz/auth/validate` y recupera la contraseña contra la CF. Solo S2S: COL-02, 03, 06. Solo la SPA del backoffice: COL-09 a 12. Sin consumidor detectado: EMP-02, 05, 07, 08, 12, 13 · SUC-03, 05 · ENT-03 · COL-04. Sigue en Cloud Functions: ENT-07 (borrado de empresa).
- Casos: 362 identificadores. 24 líneas agrupan un segundo actor bajo el mismo ID («AJENO → 403. ANON → 401.»), así que hay unos 386 comportamientos distintos.
- Diferencias con Cloud Functions que pueden romper a un cliente:
  1. **Todo el auth fallido** detrás de `requireFirebaseAuth` devuelve `{error:"unauthenticated", message}` sin `code`. La CF devolvía `{message:"Invalid token", code:"auth/unauthorized" | "auth/invalid_token"}`. Afecta a quien traduzca por `code`. Además, los tokens revocados ahora dan 401.
  2. **SUC-01, alta de centro sin permiso**: la CF daba 401 `auth/invalid_token`; el contenedor da 403 `auth/unauthorized`. El README de branches afirma lo contrario de lo que hace el código de la CF.
  3. **COL-01, invitar a alguien que ya es colaborador**: la CF daba 500; ahora 409 `{code:"auth/seat_failed", error:"already_member"}`. Con un rol distinto de owner o admin, ahora 400 `invalid_role`, cuando la CF aceptaba cualquiera.
  4. **COL-07, ficha de usuario**: la CF tomaba el `uid` del token; ahora es obligatorio en el cuerpo (400 si falta, 403 si no coincide). El panel lo manda.
  5. **ENT-02, edición de empresa**: por el código, la CF respondía 401 al panel, que solo manda `id` (`canWrite` sobre `body.entityId`). El contenedor responde 201. Es un cambio de comportamiento, aunque sea en la buena dirección; conviene confirmarlo en ejecución.
  6. **ENT-04, marca**: sin `labelColor` o sin `files.stripImage`, el contenedor escribe `undefined` y Firestore (sin `ignoreUndefinedProperties`) rechazaría la escritura → 500. Sin confirmar en ejecución, y es lo primero que habría que probar. Además, ahora exige permiso (401), cuando la CF no lo pedía.
  7. **EMP-03, 04, 06 y 08**: estados nuevos que la CF no producía. 404 `employee_not_found` al editar o borrar una ficha inexistente (la CF respondía 201/200 y creaba una ficha fantasma), 400 `invalid_email`, 409 `email_in_use` al cambiar el correo (ahora se mueve el login de Auth) y 502 `auth_error` en el alta. En el alta la ficha ya no guarda `customToken` y el usuario de Auth nace con `emailVerified:false`.
  8. **EMP-01, validar**: el `message` de error cambia de texto («Invalid payload» / «Employee not found» → el detalle) y el cuerpo pasa a ser JSON. `code` y `errors` se mantienen.
  9. **ENT-05, ENT-06 y ENT-04** exigen ahora permiso sobre la entidad (403/401), que la CF no pedía: un cliente que dependiera de ese hueco dejaría de funcionar.
  10. **SUC-02 y SUC-04**: 404 `branch/not_found` en la edición y cuerpos 400 distintos en la baja (`{error:"entityId is required"}` o `{error:"branchId is required"}` en lugar de `{error:"Invalid payload", details}`).
- Sospechas principales:
  1. **ENT-07, borrado de empresa (sigue en la CF)**: no comprueba permisos. Cualquier usuario autenticado borra cualquier empresa sin pagos pendientes, y el borrado deja huérfanos a empleados, centros y asientos de otros colaboradores. No se ha encontrado la cascada que menciona el contenedor.
  2. **COL-04, escalada de privilegios**: un ADMIN se asciende a `owner` o rebaja y desactiva a un PROP, porque `updateCollaborator` no recibe al actor. También COL-01 y COL-02 dejan que un ADMIN conceda `owner`. La distinción entre propietario y administrador solo está protegida en COL-05 (DELETE).
  3. **ENT-02 y ENT-03, acceso cruzado entre empresas**: el permiso se comprueba sobre `body.entityId` y la escritura va a `body.id` o al id de la ruta, así que quien administra A puede reescribir los datos legales de B. En la CF el defecto ya existía con `{entityId, id}`.
  4. **EMP-03, cuentas ajenas**: el reenvío de credenciales, y también el alta con un correo que ya existe en Auth, **restablece la contraseña** de cualquier cuenta de Firebase sin comprobar que sea un empleado de la entidad (la CF hacía lo mismo).
  5. **EMP-01 y EMP-06, baja blanda**: el token de bienvenida no está firmado y la sesión no caduca. El empleado dado de baja conserva su usuario de Auth, sigue validando, sigue consumiendo cupo y bloquea que se vuelva a dar de alta a alguien con el mismo correo.
  6. **`canWrite` no mira `status`**: un ADMIN_INVITADO o ADMIN_DESACTIVADO puede crear y borrar plantilla, centros y colaboradores en employees, branches y entities. Solo el router de colaboradores de checkinbiz exige asiento activo.
  7. **Escrituras de responsabilidades sin `await`** (EMP-09, 10 y 11, y la baja de empleado): el 200 no garantiza la escritura, PATCH crea documentos inexistentes y no hay manejador de `unhandledRejection`.
  8. **SUC-04, baja de centro**: es un borrado real, pero los empleados conservan el centro en `branchId`. Y cualquier edición parcial (SUC-02) vuelve a poner `disableRatioChecklog:false` (heredado de la CF).
  9. **EMP-13 y COL-03, fuera de la propia entidad**: cualquier CLAIM_ADMIN dispara avisos a los supervisores de cualquier entidad, y cualquier administrador activo puede averiguar si un correo tiene cuenta en la plataforma.
  10. **Migración incompleta**: aceptar una invitación sigue siendo una escritura del navegador en `user_entity_roles` (COL-04 no tiene consumidor), la puesta en marcha de merlin escribe asientos sin pasar por el núcleo, y la app sigue usando la CF para recuperar la contraseña.


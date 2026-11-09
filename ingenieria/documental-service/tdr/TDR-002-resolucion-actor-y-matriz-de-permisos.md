# TDR-002 — Resolución del actor y matriz de permisos

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 2)
**Componente:** `services/documents` — `DocumentPermissionService`

---

## Problema

Cada operación documental se autoriza según **quién** la pide, **qué nivel** tiene sobre la
entidad/sucursal y **qué tipo/scope** tiene el documento. Esta lógica
(`resolveActor` + matriz `can*`) debe portarse sin perder ninguna regla.

## Resolución del actor (`resolveActor(uid, entityId)`)

Una sola vía (Firebase ID token; ver [ADR-004](../adr/ADR-004-auth-solo-firebase-token.md)):

```
[roleSnap, empSnap] = paralelo(
  user_entity_roles/{uid}_{entityId},                       // owner | admin (global)
  entities/{entityId}/employees where uid == uid  limit 1   // empleado de la entidad
)
globalRole    = roleSnap.role ∈ {owner, admin} ? ese : undefined
isOwnerAdmin  = globalRole !== undefined
employeeId    = (empleado existe y status ∉ {fired, inactive}) ? empDoc.id : undefined
branchResponsibilities = si hay employeeId →
    entities/{entityId}/employee_responsibilities where employeeId == … and active == 1
    → Map<branchId, {role, level}>  (se queda el de mayor level por sucursal)
actorRole = isOwnerAdmin ? (globalRole ?? "admin")
                         : rol de la responsabilidad de mayor level (def. "worker")
```

Resultado `DocumentActor`:
```typescript
interface DocumentActor {
  uid: string;
  employeeId: string | undefined;
  isOwnerAdmin: boolean;
  globalRole: "owner" | "admin" | undefined;
  branchResponsibilities: Map<string, {role, level}>;
  actorRole: "worker" | "supervisor" | "manager" | "owner" | "admin";
}
```

**Rechazo de actor sin vínculo** (en `resolveDocumentActor`, antes de cada operación): si
`!isOwnerAdmin && employeeId === undefined && branchResponsibilities.size === 0` → `403 documents/unauthorized`.

## Niveles de responsabilidad

`ResponsibilityLevel`: `worker < supervisor < manager < owner`. `owner` aquí es el **owner
operativo** de una sucursal (nivel 4), distinto del owner/admin global (`isOwnerAdmin`).

## Tipos con reglas especiales

- **RRHH-puros** (`RESTRICTED_DOCUMENT_TYPES` = `payroll`, `contract`): gestionados **solo por owner/admin global**. Ni crear, ni actualizar, ni archivar por managers.
- **Disciplinarios** (`DISCIPLINARY_DOCUMENT_TYPES` = `warning`, `attention_call`): en scope employee, solo `manager` **exacto** (nivel 3) — el owner operativo (nivel 4) queda excluido, porque el aviso formal lo emite el manager.

## Matriz de permisos (`can*`)

| Función | Regla |
|---|---|
| `canCreate(actor, scope, branchId, type)` | owner/admin → siempre. `scope=entity` → solo owner/admin. `scope=branch` → `manager+` en la branch, y **nunca** tipos RRHH. `scope=employee` → RRHH nunca; disciplinarios → `manager` exacto de la branch; resto → `manager+` de la branch. |
| `canRead(actor, doc)` | `employee` → **se decide antes que nada**: el propio empleado siempre; si no, desde la app nadie (ni owner/admin), y desde el panel solo owner/admin. Ni `visibleToRoles` ni el rol en la sucursal abren un documento personal ajeno (cambiado el 2026-11-06, ver abajo). Solo-`admin` (nivel «Administración», 2026-11-07) → solo owner/admin desde el panel. Para el resto: owner/admin → siempre. `entity` → owner operativo, o rol del actor ∈ `visibleToRoles`. `branch` → visible en la branch por rol (owner operativo siempre). |
| `canUpdate(actor, doc)` | igual que `canArchive`. |
| `canArchive(actor, doc)` | owner/admin → siempre. Solo-`admin` → solo owner/admin. RRHH → nunca (solo owner/admin). Sin `branchId` (scope entity) → solo owner/admin. Resto → `manager+` en la branch. |
| `canAcknowledge(actor, doc)` | requiere `requiresAcknowledgement` y `canRead`. `single_employee` → `actor.employeeId === doc.employeeId`. `branch_employees` → el actor tiene responsabilidad en `doc.branchId`. `entity_employees` → el actor tiene ≥1 responsabilidad. |

Reglas auxiliares: `roleVisibleInBranch` (owner operativo bypasea `visibleToRoles`);
`actorVisibleForEntityScope` (owner operativo o rol ∈ `visibleToRoles` en cualquier branch).

## El documento personal es de la persona (hotfix 2026-11-06, checkbiz-api#258)

**Lo que pasaba.** La app pide la lista sin `employeeId` («Mis documentos» es «todo lo que yo
pueda ver»), y `canRead` dejaba ver un documento de empleado ajeno a cualquier compañero con rol
en la misma sucursal si su rol estaba en `visibleToRoles` —el panel marca los tres por
defecto—, y a un owner/admin se lo enseñaba todo, contratos incluidos. En producción, una owner
de Encodebiz veía desde la app ocho documentos personales de otras tres personas.

**La regla, dicha por Jose.** Un documento compartido como empresa o sucursal es público para
quien pertenece a ellas: quien lo comparte así, responde de ello. El de **otro empleado** no lo
ve nadie sin permisos de owner o admin. Y la app está orientada a la plantilla, no a quien
administra: desde la app, el documento personal de otra persona no se ve **sea quien sea**.

**Cómo se sabe desde dónde llaman (Fase 1, la que está en prod).** `resolveActor` recibe un
`channel: "app" | "panel"` que `resolveDocumentActor` saca del `User-Agent`: la app lo
sustituye por la huella del dispositivo (la misma del fichaje, ver `dio_client.dart`) y el panel
llega **de dos maneras**: desde el navegador (`Mozilla/…`) y, sobre todo, desde su servidor en
Vercel, cuyo fetch de Node se presenta como `node` (también `undici`, `Next.js`). Lo que no es
ninguna de esas se trata como app, que es el lado estricto: un `curl` o una sonda ven menos,
nunca más. Jose lo aceptó como hotfix y lo considera **poco fiable**: un `User-Agent` lo pone
quien quiere.

**Lo que ya costó.** La primera versión (#258) solo reconocía `Mozilla/` como panel; durante
unos 25 minutos la gestión documental del panel salió **vacía** a owner y admin, y lo reportó un
cliente. Corregido en #259. La lección: el panel no habla con la API desde el navegador, y
cualquier heurística sobre el cliente tiene que contar con el servidor de Vercel.

**Fase 2 — el panel demuestra que es el panel (DECIDIDO con Jose el 2026-11-06; tarea del
10-nov en CheckBiz360).** La idea de Jose: «enviar el token de 2FA y verificarlo en el servidor
solo para cuando es node». Es decir, el que tiene que demostrar algo es el **servidor del panel**,
no la app ni el navegador; y lo demuestra con un código de un solo uso, como el 2FA.

*Cómo.*

1. **Secreto compartido** `PANEL_CHANNEL_SECRET`: una variable en Vercel (producción) y la misma
   en `.env.production` de `documents` (y su par en staging/`.env.staging`). 32 bytes aleatorios
   en base64; se genera una vez y no se escribe en ningún repo.
2. **Código rotatorio**, estilo TOTP: `código = HMAC-SHA256(secreto, floor(ahora_unix / 30))`,
   en hexadecimal, y el panel lo manda en cada llamada a la API en la cabecera
   `X-CheckBiz-Panel: <código>`. El único sitio donde el panel sale hacia la API es
   `src/lib/http/serverBackendProxy.ts`: una cabecera más ahí y ya está en todas las rutas.
3. **Verificación en `documents`** (`resolveDocumentActor`): se recalcula el código para la
   ventana actual y la anterior (tolera hasta 30 s de desfase) y se compara en tiempo constante
   (`crypto.timingSafeEqual`). Coincide → `channel = "panel"`. **Cualquier otra cosa →
   `"app"`**, llegue como `node`, como navegador o como lo que sea. El `User-Agent` desaparece
   de la decisión.
4. **Por qué rotatorio y no un secreto fijo:** por TLS los dos viajan cifrados, pero el rotatorio
   no sirve si alguien lo copia de un log, una traza o un volcado de cabeceras: caduca en un
   minuto. Cuesta cinco líneas más que un `=== secreto`.
5. **Por qué solo el panel y no la app:** panel = demostrado; todo lo demás = app, que es el lado
   estricto. Un `curl`, una sonda o un `node` falsificado sin el secreto consiguen *menos*
   acceso, nunca más. La app no tiene que demostrar nada, así que el dispositivo de confianza
   del 2FA del empleado, que se barajó antes, deja de hacer falta para esto.

*Despliegue en tres pasos, sin ventana de panel vacío* (lo de #258 → #259 no se repite):

- **Paso A — servidor.** `documents` acepta `X-CheckBiz-Panel` y, si falta o no vale, cae al
  `User-Agent` de la Fase 1. Se despliega solo (`up -d --build --no-deps documents`). Sin la
  variable en el `.env`, la cabecera se ignora y todo sigue como hoy.
- **Paso B — panel.** Variable en Vercel + cabecera en `serverBackendProxy.ts`. Despliegue del
  panel (Jose). Comprobación: en el log de nginx las llamadas `node` siguen devolviendo lo
  mismo, y una sonda con `User-Agent: node` **sin** cabecera ya ve como app.
- **Paso C — servidor.** Se quita el `User-Agent` de `resolveClientChannel`. Desde aquí, panel es
  solo quien trae el código.

*Prueba de aceptación (sonda del contenedor `tasks`, ver §38 del pase):* una owner de Encodebiz
→ con cabecera válida ve los 14 documentos; con `User-Agent: node` y sin cabecera, o con una
cabecera de hace dos minutos, ve 6 y ninguno ajeno; un worker ve lo mismo en todos los casos.

*Lo que se descartó:* dispositivo de confianza del empleado (`security/trustedDevicesId`) como
prueba de «app» —ya no hace falta—; custom claims de Firebase —son por usuario, no por sesión,
y la misma persona usa panel y app con el mismo usuario—; cabecera de cliente sin verificar
—igual de falsificable que el `User-Agent`—.

**Pendiente que destapa la regla:** `canCreate` sigue dejando que un `manager` de sucursal
cree documentos de empleado para su gente (los no RRHH) y `canArchive` que los archive, pero
desde el 06-nov ya no puede **leerlos**. O crear/archivar pasan también a owner/admin, o el
manager recupera la lectura de lo que él mismo subió. Decidir con Jose.

## Nivel «Administración» (decidido 2026-11-07; en staging el mismo día, pendiente en prod: pase §43)

**Para qué.** Subir documentos que **solo se ven desde el panel**: el contrato o el presupuesto de
un cliente, papeles de dirección. Hasta ahora lo más cerrado era `manager`, que lee también el
gerente de la sucursal —en un cliente, el de cualquiera de sus sucursales— y desde la app. Salió
en la QA de la cartera: la ficha le tapa al gerente importe, coste y margen del contrato, pero el
PDF marcado `manager` se lo enseñaba entero.

**La regla, dicha por Jose.** Se **añade** un nivel, no se quita ninguno: supervisor y manager
siguen siendo roles distintos. Y el principio que lo sostiene: **la app es solo para empleados**.
Quien entra por la app, aunque sea propietario o administrador, se comporta como un empleado más.
Administración es del panel.

**Cómo queda.**

- Valor nuevo `admin` en `DocumentVisibilityRole`; en el panel se lee «Administración».
- Solo-`admin` (va solo en `visibleToRoles`): `canRead` deja pasar únicamente a `isOwnerAdmin`
  con `channel === "panel"`, y esa comprobación va **antes** del `isOwnerAdmin → true`. Desde la
  app no lo ve nadie. El owner operativo (nivel 4 en una sucursal) queda fuera: no es propietario
  ni administrador de la empresa.
- `admin` combinado con otros roles: mandan los otros como hoy; `admin` solo cierra cuando va solo.
- Editar y archivar un solo-`admin`, y poner o quitar `admin` de `visibleToRoles`: solo
  owner/admin. Sin esto un gerente podía hacer PATCH, bajarlo a `manager` y leerlo.
- Solo-`admin` + `requiresAcknowledgement`: 400. Nadie de la plantilla puede firmar lo que no ve,
  y la alerta de firma pendiente quedaría encendida para siempre.
- Notificaciones: un solo-`admin` no avisa a nadie.
- `customers` `for-task` es de la app, así que aplica el principio: devuelve solo lo visible para
  `worker`, sea quien sea quien llama (hoy a quien gestiona le listaba todo, contratos incluidos).
- Inventario: no se vincula un documento solo-`admin` a un equipo (el dossier no mira roles).
- Panel: casilla «Administración»; contrato y presupuesto del cliente nacen solo-`admin`, también
  el PDF de «Nuevo contrato» (`CustomerContractsSection`); etiqueta con alternativa
  (`?? role`) para que un panel viejo no pinte «undefined».
- Datos: lo ya subido con `manager` se queda; script que simula por defecto para pasar contratos
  y presupuestos de cliente a `admin`, sin ejecutar hasta que Jose lo pida.

**Lo hecho (2026-11-07).** API en `feat/documentos-administracion` (`d37d4f9`, desde develop
`245ba67`); panel en `feat/documentos-administracion` (`3085d580`, desde `feat/cartera-de-clientes`).
Sin subir ni desplegar; el pase, en `deployment-prod/proximo-pase-back.md` §43.

- `Document.ts`: `admin` en `DocumentVisibilityRole`, `DOCUMENT_VISIBILITY_ROLES` (lo usan los dos
  controladores en vez de su `VALID_VISIBILITY`), `isAdminOnly` y `goesWithEquipment`.
- `canRead`: solo-`admin` → `isOwnerAdmin && channel === "panel"`, después del documento personal y
  antes del `isOwnerAdmin → true`. `canArchive` (y con él `canUpdate`): solo-`admin` → solo
  owner/admin. `canChangeAdminVisibility`: poner o quitar `admin` en un PATCH, solo owner/admin
  (en `UpdateDocument`, que devuelve `forbidden`).
- Errores nuevos, los dos 400: `documents/admin_only_acknowledgement` (al crear con acuse, y al
  editar si roles y acuse acaban casando así) y `documents/admin_only_equipment` (ámbito
  `item`/`unit`, vincularlo a un equipo o dejarlo solo-`admin` estando vinculado).
- `DocumentNotificationService`: solo-`admin` sale antes de buscar destinatarios, en la subida y en
  el acuse.
- `customers`: `visibleForRole` (`src/domain/customerDocumentVisibility.ts`) nunca deja salir un
  solo-`admin`; `for-task` pide siempre `worker`; `contractsExpiring` cuenta todos (la cifra no
  enseña el papel). Script `contracts-to-administration` (simula; `--apply`), sin ejecutar.
- Panel: casilla «Administración» salvo en empleado y equipos (`visibilityRolesFor`), contrato y
  presupuesto nacen `["admin"]` (también «Nuevo contrato»), acuse desactivado con solo
  «Administración», etiqueta con alternativa (`documentRoleLabel`). El aviso en rojo sigue solo
  para supervisor y trabajador: el gerente no es plantilla y por la app ya no ve nada de esto.
- Tests: `services/documents/test/documentPermissions.test.ts` (los primeros de la matriz) y
  `services/customers/test/customerDocumentVisibility.test.ts` (y el script `test` de customers).

**Queda abierto.**

- El principio «owner o admin por la app es un empleado» se aplica de momento solo al nivel nuevo
  y al documento personal: un documento de empresa o sucursal marcado `worker`/`manager` lo sigue
  viendo el owner desde la app aunque como empleado no le tocara. Decidir si se extiende.
- El gerente puede **subir** un documento de cliente marcado solo «Administración» (y después no
  verlo): la regla de solo owner/admin cubre editar, archivar y el cambio en un PATCH, no la subida.
- El owner operativo crea contratos en `customers` (`seesEverything`) pero no abre su PDF si es
  solo-`admin`. En la ficha, el gerente y el owner operativo pueden ver un contrato con
  `documentId` cuyo PDF les da 403: falta que el panel no pinte ese enlace.
- `admin` en un documento personal no añade nada (el panel no lo ofrece; la API lo admite).

**Fuera de este trabajo.** Las reglas de Firestore (2b) siguen dejando leer y reescribir
`entities/{e}/documents` a cualquier miembro con el SDK: el fichero está protegido por Storage,
el título y la visibilidad no. Y en producción hay que confirmar que la descarga del panel
(`NEXT_BACKEND_URI_CHECKINBIZ_DOWNLOAD_DOCUMENTS`) va al contenedor y no a la función antigua del
SaaS, que no conoce ni el canal ni `admin`.


**Ampliado el mismo día (`b319668`, en staging).** El principio vale para todo documento, no solo
para el nivel nuevo: por la app (`channel === "app"`), propietario, administrador y owner
operativo pierden su pase y leen solo lo que lleve `worker`; supervisor y manager conservan su
rol, que es de la plantilla. Por la app el listado tampoco enseña archivados.
## Scoping en listados (`FindDocuments`)

- `status`: si no se pide explícitamente, para actores **no** owner/admin se fuerza a `active`.
- Los tres flujos (búsqueda por índice, "todo del empleado", y listado normal) **siempre**
  filtran cada documento por `canRead` antes de devolverlo. La paginación por cursor cuenta
  sobre lo visible; el flujo de índice y el "todo del empleado" paginan en memoria.

## Criterio de aceptación

Portado 1:1 desde `DocumentPermissionService`. Casos de verificación mínimos: (a) empleado sin
rol suficiente sobre un `payroll` ajeno → 403; (b) `manager` de sucursal crea `warning` en su
sucursal → OK, pero `owner` operativo no; (c) owner/admin ve documentos `archived`, un empleado
no.

# TDR-009 — Cliente disponible en todas las sucursales

**Fecha:** 2026-11-17
**Estado:** EN PROD el 2026-11-17 (API hotfix #292, merge `734c87b`; panel hotfix #160, merge `ebd64e3`), por orden de Jose tras probarlo en staging. Pase en back §76. Pendiente: prueba con sesión real en producción, aviso a Ayudarte y lo que §4.2 deja fuera del hotfix.
**Componente:** `services/documents` (abrir un documento de Plantilla de un cliente general), `services/customers` (quién llega a un cliente general), panel (alta y ficha del cliente, modal de subida)
**Reabre:** [06 §D11](../06_decisiones-abiertas.md) en un solo punto: `scope: "entity"` vuelve a la pantalla
**No cambia:** el modelo ([ADR-002](../adr/ADR-002-cliente-entidad-propia-con-sucursales-asignadas.md)), la tarea ([TDR-002](TDR-002-el-cliente-en-la-tarea.md)), el análisis, los informes, la app

---

## 1. Para qué

Ayudarte ha creado muchas sucursales para organizar sus cursos y sigue creando. Un cliente solo se puede
elegir en las tareas de las sucursales a las que está asignado, así que cada cliente hay que asignarlo a
todas, una a una, y cada sucursal nueva vuelve a dejarlo fuera. Piden «aplicar a todas las sucursales».

## 2. Lo decidido

**El cliente general**

- En el selector de sucursales del cliente, un check **«Disponible en todas las {sucursales}»**. Marcado,
  el cliente se puede elegir en las tareas de cualquier sucursal, también de las que se creen después.
- Es **por cliente y apagado por defecto**. El resto de clientes sigue igual.
- **No se crea una sucursal ficticia.** El modelo ya lo tiene: `scope: "entity"` con `branchIds: []`. Un id
  inventado dentro de la lista obligaría a excepciones en la validación del alta y saldría sin nombre en
  informes y análisis.
- No se copia la lista de sucursales («aplicar a todas» como atajo): quedaría vieja con la siguiente
  sucursal.
- **Las horas por cliente**, el día que se retomen, salen de la tarea, que lleva cliente y sucursal.

**Quién llega a él**

- Al panel solo entran propietario y administrador, que es un rol administrativo aparte de los de
  empleado. Gestores y supervisores «no dejan de ser empleados»: no ven ni cambian nada que no esté
  autorizado.
- **Marcar un cliente como general no le da la ficha a nadie nuevo.** Lo marcan, lo ven en ficha y lo
  editan solo propietario y administrador. El dinero, igual que siempre.
- La plantilla lo ve como hasta ahora: por su tarea y con lo autorizado ([TDR-005](TDR-005-datos-complementarios-y-nombre-del-cliente.md)).

**Sus documentos**

- En un cliente general no hay sucursal donde mirar si alguien es trabajador, supervisor o gestor, así
  que no se eligen roles. El documento es de **Plantilla** (todos menos Administración) o de
  **Administración**.
- **Plantilla es toda la plantilla de la empresa.** «Si lo marcas como plantilla hay que abrirlo y punto»:
  el cliente es general, quien tiene una tarea suya lo ve y quien no la tiene no pasa nada; lo crítico es
  lo de Administración. Tampoco se ata a la tarea, porque hay quien atiende a un cliente con horario fijo
  y sin tareas.
- **Se dice al marcar.** Tanto el check del cliente como la opción Plantilla del documento avisan de que
  lo verá toda la plantilla.
- Un documento para una sola persona no es del cliente: es el documento personal que ya existe, con su
  seguridad propia.

Descartado en el debate: abrir solo a quien tenga asignada una tarea del cliente, mandando la tarea desde
la app o buscándola el servidor. Obligaba a publicar versión de la app o a una consulta por apertura, y
dejaba fuera a quien no trabaja por tareas.

## 3. Lo que ya funciona sin tocar

Comprobado leyendo el código el 2026-11-17, en `main` y en `staging`:

| Dónde | Qué hace con `scope: "entity"` |
|---|---|
| `customerAssignedToBranch` (shared) | Devuelve sí para cualquier sucursal. |
| Crear o editar una tarea (`tasks`, `resolveTaskCustomer`) | Acepta el cliente en cualquier sucursal. |
| Selector de cliente de la tarea (`GET /customers?branchId=`) | Lo devuelve para cualquier sucursal. |
| Marcarlo (`canAssignBranches`) | Solo quien lo ve todo. |
| `normalizeAssignment` | Guarda `branchIds: []` y no exige ninguna. |
| Espejo en Postgres (`dim_customers`) | Guarda `scope` y la lista vacía. |
| Análisis e informes del cliente | Filtran por la sucursal de la tarea, no por la del cliente. |
| Tarjeta de la tarea en la app (`GET /customers/for-task/:taskId`) | Entra quien tiene la tarea asignada; lista los documentos que llevan `worker`. |
| «Documentación» de la app | No lista documentos de cliente (junta empresa, sucursales de la persona y personales). |

## 4. Lo que hay que cambiar

### 4.1 Documental: abrir un documento de Plantilla de un cliente general

Hoy la app, al tocar un documento en la tarjeta de la tarea, pide `GET …/documents/:documentId/download`.
El documental decide con las sucursales del cliente (`customerBranchIds`): la persona tiene que tener, en
alguna de ellas, un rol que el documento lleve. Con un cliente general la lista va vacía y nadie de la
plantilla pasa.

Cambio: junto a `customerBranchIds` viaja un segundo dato transitorio, `customerAllBranches` (nunca se
guarda), que `FirestoreDocumentRepository.withCustomerBranches` rellena donde ya lee el cliente. Y la
descarga (`GenerateDocumentDownloadUrl`) da paso si se cumplen las cuatro:

1. el documento es `scope: "customer"` y su cliente es general;
2. el documento está activo;
3. el documento lleva `worker` en `visibleToRoles` (es de Plantilla, no de Administración);
4. quien pide es empleado de esa empresa.

Para un cliente por sucursales no cambia nada. La app no cambia: la versión instalada (1.12.1+73) ya trae
la tarjeta y funciona tal cual. No hay consulta nueva ni índice.

Subir y gestionar documentos de un cliente general queda en propietario y administrador sin tocar nada:
con la lista de sucursales vacía, `canCreate` y `canManage` ya lo dan.

**Condición de Jose: no puede romper nada de lo que ya existe en el documental.** Cómo se garantiza:

- **`DocumentPermissionService` no se toca.** Ni `canRead`, ni `canCreate`, ni `canManage`, ni sus reglas
  de canal, de documento personal, de Administración o de eliminados. El fichero queda byte a byte igual.
- **El paso nuevo solo añade; nunca quita.** Vive en `GenerateDocumentDownloadUrl`: primero se pregunta a
  `canRead` como hoy, y solo si dice que no se mira si es un documento de Plantilla de un cliente general.
  Lo que hoy se abre se sigue abriendo por el mismo camino.
- **Solo documentos de cliente general, activos y con `worker`.** Un documento personal, de sucursal, de
  empresa, de equipo, de un cliente por sucursales, eliminado o de Administración no entra nunca por aquí.
- **Listados, ficha del documento, firma, subida, edición, archivo y borrado: sin cambios.** Solo cambia la
  descarga.
- **`documentPermissions.test.ts` y el resto de pruebas del servicio pasan sin modificarse.** Las pruebas
  nuevas van en un fichero aparte.
- **En el panel**, `DocumentUploadModal` y `DocumentEditModal` son compartidos por todos los ámbitos: la
  elección Plantilla/Administración solo aparece cuando se les pasa un cliente general; en cualquier otro
  caso pintan y mandan exactamente lo de hoy.

### 4.2 Customers: a un cliente general solo llega quien lo ve todo

Hoy `canReachCustomer` da paso a un cliente general a cualquier gestor o supervisor, porque pregunta «¿está
en alguna de mis sucursales?» y un cliente general está en todas. Al panel no entran, pero la API
respondería a su credencial: verían la ficha entera, y un gestor podría editarla o devolverla a «solo mis
sucursales» con `PUT /:id/branches`.

Cambio en `permissions.ts` de `customers`: a un cliente `scope: "entity"` solo llega quien lo ve todo. Con
eso quedan cerradas, para quien no es propietario ni administrador, la lista, la ficha, la edición y la
asignación de un cliente general. No toca `shared` ni la validación de la tarea, y la ruta de la app
(`/for-task/:taskId`) sigue dando paso a quien tiene la tarea asignada.

Dos cosas que este cambio no resuelve y se dicen:

- «Quien lo ve todo» (`seesEverything`) incluye hoy, además del rol administrativo, al empleado con
  responsabilidad de nivel propietario en alguna sucursal. No se toca salvo que Jose lo pida.
- El análisis y el parte del cliente (`analytics`, `reports`) deciden el alcance con `customerReaderReaches`,
  que está en `shared` y hace la misma pregunta. Responderían a la credencial de un gestor o supervisor que
  llamase a la API a mano, con las tareas de sus sucursales. Cerrarlo es tocar `shared` y redesplegar todos
  los servicios: va por la cadena normal, no por el hotfix.

### 4.3 Panel

**El cliente**

- **`CustomerBranchesFields`** (alta y «Editar sucursales», es el mismo bloque): el check encima del
  selector. Marcado, manda `{scope: "entity", branchIds: [], dedicatedBranchIds: []}` y el selector queda
  desactivado y vacío. Desmarcado, vuelve a exigir al menos una.
- **`CustomerBranchesDialog`**: abre con el `scope` real del cliente (hoy lo fuerza a `branches`).
- **Lista** (`BranchChips`) y **ficha** (métrica de sucursales): una sola pastilla «Todas las
  {sucursales}» en vez de la lista vacía y del «0».

**Sus documentos** (`DocumentUploadModal` y `DocumentEditModal`, cuando el cliente es general)

- En vez de las casillas de rol, una elección: **Plantilla** o **Administración**.
- No cambia lo que se guarda: Plantilla es `["worker", "supervisor", "manager"]` y Administración es
  `["admin"]`, los valores de hoy.
- Contrato y presupuesto siguen entrando como Administración por defecto, con su aviso en rojo si se pasan
  a Plantilla.
- Un documento que venga de cuando el cliente era por sucursales y no lleve `worker` (por ejemplo, solo
  gestores) se enseña como «no visible para la plantilla» hasta que alguien elija. Ante la duda, cerrado.

**Textos**, en los 5 idiomas (es, en, pt, fr, de), con el nombre que cada empresa da a la sucursal:

- check: «Disponible en todas las {branches}»
- ayuda: «Se podrá elegir en las tareas de cualquier {branch}, también de las que crees después.»
- aviso al marcarlo: «Los documentos de este cliente marcados para la plantilla los podrá abrir toda la
  plantilla de la empresa. Lo que no deba verse, márcalo como Administración.»
- pastilla: «Todas las {branches}»
- documentos: «Plantilla: lo puede abrir toda la plantilla de la empresa» / «Administración: solo
  propietario y administrador, desde el panel»
- el aviso `branchesRequired` ya dice «o marca "de toda la empresa"»: se ajusta al texto del check.

### 4.4 Lo que no se toca

App, asistente, análisis, informes, migraciones, índices de Firestore, `shared`.

## 5. Casos a tener presentes

- **De general a por sucursales.** Las tareas ya creadas en otras sucursales conservan su cliente (llevan
  su copia). No se limpian. Sus documentos vuelven a la regla por sucursal: quien no esté en las
  sucursales elegidas deja de abrirlos. Comprobar en staging qué pasa al editar una de esas tareas.
- **De por sucursales a general.** Un documento que no lleve `worker` (por ejemplo, solo gestores) queda
  cerrado a la plantilla hasta que alguien elija Plantilla.
- **Lugares del cliente de tipo sucursal** y **sucursal dedicada** (fuera de pantalla desde D11): no se
  tocan; el panel sigue mandando las dedicadas vacías.
- **Quien atiende a un cliente sin tareas** (horario fijo): el servidor le abriría el documento, pero la
  app solo enseña los documentos de un cliente dentro de una tarea. No tiene pantalla donde verlos. Queda
  anotado; no entra en este cambio.

## 6. Pruebas

Automáticas:

- `services/documents/test`, en fichero aparte: cliente general — cualquier empleado de la empresa abre
  el de Plantilla; nadie de la plantilla abre el de Administración ni uno sin `worker`; quien no es de la
  empresa, no; un documento archivado o eliminado, no. Cliente por sucursales — los casos de hoy, iguales.
- `services/customers/test`: a un cliente general no llega un gestor ni un supervisor (lista, ficha,
  edición, asignación); propietario sí; un cliente por sucursales, igual que antes.

En staging, en una empresa de prueba (la de QA de la cartera o SaludStart), con sesión real:

1. Propietario marca un cliente como disponible en todas. Lista y ficha lo dicen.
2. Crear tarea en una sucursal donde antes no estaba: el cliente sale y se guarda.
3. Crear una sucursal nueva y una tarea en ella: el cliente sale.
4. Al marcar el check sale el aviso de que la plantilla verá sus documentos.
5. Subir dos documentos al cliente general, uno de Plantilla y uno de Administración: el modal ofrece solo
   esas dos opciones y dice quién lo verá.
6. Trabajadora asignada, con la app que está en tiendas: ve la tarjeta y abre el de Plantilla.
7. La misma trabajadora pide por la API el de Administración: 403. Otra persona de la plantilla sin tarea
   de ese cliente pide el de Plantilla: lo abre.
8. Con la credencial de un gestor, por la API: la ficha del cliente general y cambiar su asignación, 403.
9. Propietario lo desmarca y elige dos sucursales: las tareas de las demás conservan el cliente.
10. Un cliente por sucursales de siempre: todo igual que antes. Y subir un documento de cada ámbito
    (empleado, sucursal, empresa, equipo): los modales pintan y mandan lo de hoy.
11. Desde el asistente, `ver_clientes` y crear una tarea con el cliente general.

## 7. Cómo sale

Hotfix mínimo desde `main`, sin arrastrar lo que `develop` y `staging` llevan de más.

- **API.** Rama `hotfix/cliente-todas-las-sucursales` en un worktree desde `origin/main` (el nombre lo
  confirma Jose). Los ficheros que toca son idénticos en `main` y en `staging`; lo que difiere en
  `services/customers` es la entrada delegada del asistente (`app.ts`, `requireCredential`, `resolveActor`)
  y no se pisa. De ahí, cherry-pick a `develop` y `develop → staging` con `[skip ci]`, y despliegue a mano
  de `documents` y `customers` en el VPS de desarrollo (más reinicio del nginx de desarrollo).
- **Panel.** Rama desde `main` del panel con el mismo nombre. Se prueba en local contra la API de staging
  (Vercel es solo producción). Commit solo con permiso de Jose (AI-RULES del panel).
- **Producción, con el OK de Jose tras la prueba en staging:** primero la API (`documents` y `customers`),
  después el panel. Sin migraciones ni índices.
- **Vuelta atrás:** revertir el panel basta para que nadie marque más. Los clientes ya marcados siguen
  funcionando en las tareas con cualquier versión del servidor.
- **Ayudarte:** no hay script. Cuando esté en producción marcan ellos sus clientes. El aviso lo manda Jose
  o se manda con su OK.
- Se apunta en `DOCS/deployment-prod/proximo-pase-back.md` y `proximo-pase-front.md` al implementarlo.

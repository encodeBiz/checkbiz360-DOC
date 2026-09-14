# 01 — Estado actual

Inventario levantado el 2026-09-08 leyendo las tres fuentes que de verdad lo saben: el
`index.ts` de las funciones del SaaS, los routers de los servicios de `encodebiz-api`, y el
`.env.development` del panel —que es el único sitio donde consta a qué URL apunta cada botón—.

## 1. El reparto, en una línea

De los **56 destinos** que el panel resuelve hoy, **18 los sirve el contenedor y 38 siguen en
Firebase**. Pero esos 38 no son 38 tareas: once son de passinbiz, dos están muertos y seis ya
están portados esperando el corte. El trabajo real son **once piezas HTTP**.

Aparte del HTTP hay **29 funciones reactivas de checkbiz** —disparadores de Firestore y
cron— que nadie ha tocado todavía.

## 2. Lo que ya sirve el contenedor

Con tráfico real en desarrollo, comprobado por variable de entorno:

| Qué | Dónde |
|---|---|
| Fichajes: alta, corrección y jornada manual | `checkinbiz:3002` `/checklogs`, `/checklogs/update`, `/checklogs/manual-request` |
| Arranque de la app: login, validate, calendario | `checkinbiz:3002` `/auth/*`, `/calendar` |
| Disponibilidad | `checkinbiz:3002` `/calendar/availability` |
| Búsqueda de direcciones | `checkinbiz:3002` `/geo` |
| Tareas | `tasks:3006` |
| Documental y su descarga | `documents:3007` |
| Informes, tareas en xlsx y descarga | `reports` `/api/reports` |
| Merlin y el relato del panel | `merlin` `/api/v1/gpt/*` |
| Panel operativo v2 | `analytics` `/api/analytics/panel/overview` |
| Webhooks salientes | `events:3012` |
| Add-on de Rentman | `rentman` `/api/v1/rentmanbiz` |

## 3. Portado, sin cortar

El código está en el contenedor y responde; el panel sigue llamando a Firebase. Es la deuda
más barata de saldar de todo el inventario.

| Función de Firebase | Ya vive en | Nota |
|---|---|---|
| `checkinbiz-createEmployee` | `checkinbiz` `POST /employees` | corta con una variable |
| `checkinbiz-updateEmployee` | `checkinbiz` `PATCH /employees/:id` | **necesita alias**, ver [03](./03_contratos-y-cortes.md) |
| `checkinbiz-deleteEmployee` | `checkinbiz` `DELETE /employees/:id` | **necesita alias** |
| `checkinbiz-validateEmployee` | `checkinbiz` `POST /employees/validate` | corta con una variable |
| `checkinbiz-employeesExportHandler` | `checkinbiz` `GET /employees/export` | corta con una variable |
| `enable2FA` / `verify2FA` (empleado) | `checkinbiz` `POST /auth/2fa/enable` y `/verify` | la app ya los usa; falta el kiosco del panel |
| `checkinbiz-checkbizStatsController` | `analytics` `POST /api/analytics/panel/stats` | mismo cuerpo y misma respuesta a propósito |
| `subscriptions-subscribe` / `unsubscribe` / `configBilling` | `billing:3011` | el corte lo manda [billing-v2](../billing-v2/04_fases.md) |

## 4. HTTP sin portar

Once piezas. La columna de la derecha dice lo que ya está hecho de cada una, que es lo que
separa media jornada de dos días.

| Pieza | Funciones | Lo que ya tenemos |
|---|---|---|
| Sucursales | `createBranch`, `updateBranch`, `deleteBranch` | `FirestoreBranchRepository`, `canWrite` y el índice de búsqueda están en `shared`; falta el lado de escritura y el límite de plan |
| Entidad | `createEntity`, `updateEntity`, `updateEntityBranding`, `deleteEntity` | `platform/Entity` y su repositorio en `shared`; el alta de miembro ya existe como `manageCollaborator` |
| 2FA de usuario | `get2FAUserStatus`, `enable2FAUser`, `verify2FAUser` | el 2FA de empleado ya está portado y es el mismo patrón sobre otra colección |
| Usuarios | `createUsers`, `recoveryPassUsers`, `assingUser` | `EmailService` con sus plantillas está en `shared`; de `assingUser` está portada la mitad que reparte permisos |
| Heurística | `analyzeHeuristic` | el motor entero está en `checkinbiz/application/heuristic`; la función son 64 líneas de envoltorio |
| Media | `uploadMedia`, `deleteMedia` | nada |
| Responsabilidades | `responsibilitiesHandler` | la lectura (`findResponsibilities`) está en `shared` |
| Dispositivo de confianza | `addDeviceEmployee` | **no se porta**: el verify del contenedor ya registra el dispositivo |
| Correo | `sendEmail` | **no se porta**: `EmailService` ya está en `shared` |
| Webhooks | `createWebhookEndpoint`, `deleteWebhookEndpoint` | **muertos**: el panel ya no los llama, los sustituyó `events_handler` |
| passinbiz | nueve funciones más los tres de eventos | **fuera de alcance**, ver [ADR-005](../eventos-webhooks/adr/ADR-005-retirada-de-passinbiz.md) |

## 5. Lo reactivo

Veintinueve funciones de checkbiz. Los puntos de entrada son finos —1.491 líneas los
disparadores de checkinbiz, 288 los cron— porque el peso está en la capa de aplicación que
arrastran.

**Disparadores del núcleo (5, sin contar el de passinbiz):** `beforeUserCreated`,
`onDeleteEntity`, `onCreateSentEmail`, `onDocumentWriteSubscriptions`, `processInvoices`.

**Disparadores de checkinbiz (15):** `onChecklogWrite`, `onChecklogSync`, `onChecklogWebhook`,
`onBranchPattern`, `onEmpPattern`, `onTaskPattern`, `onBranchPatternSync`, `onEmpPatternSync`,
`onTaskRatingSync`, `onWriteTaskRating`, `onCreateEmployee`, `onCreateBranch`,
`onActivateCheckbiz`, `onCreateIssues`, `onIssuesResponse`.

**Cron (9):** `processPendingEmails`, `webhookWorker`, `triggerInvoiceWorker`,
`dailyCollectorData`, `employeePlanifierWorker`, `planifierNotificationWorker`,
`taskStartNotificationWorker`, `sanitizerChecklog` y su helper HTTP.

## 6. Cuatro cosas que conviene saber antes de tocar nada

**`onChecklogWebhook` está emitiendo por duplicado.** Los controladores de fichaje del
contenedor ya llaman a `emitChecklogCreated`, `emitWorkdayClosed` y compañía, y el disparador
sigue desplegado en desarrollo emitiendo lo suyo. Un endpoint suscrito al tipo exacto recibe
cada fichaje dos veces con dos firmas distintas. El plan de eventos ya pedía que las dos cosas
ocurrieran en el mismo commit; la ventana está abierta. Ver
[eventos-webhooks/07 §3.1](../eventos-webhooks/07_estado-verificado.md).

**`dailyCollectorData` no es residuo: alimenta el panel.** Escribe `checkbiz_daily_report` en
Firestore y de ahí lee `analytics/StatsFirestoreRepository` para pintar las tarjetas. No se
apaga sin sustituto, y su sustituto no es el `DailyReportCron` de `reports`, que escribe en
Postgres otra cosa.

**El alta de empleado del contenedor y `onCreateEmployee` ya se estorban.** `createEmployee`
de `shared` crea el acceso *antes* que la ficha y la escribe con el `uid` puesto,
precisamente para que el disparador se aparte y no mande una segunda bienvenida con otra
contraseña. Es una convivencia deliberada y frágil: cuando el disparador se retire, hay que
retirar también el apaño.

**Cuatro puertas abiertas, encontradas al portar, y todas del mismo tipo.** El router de
empleados no comprobaba permiso ni cupo de plan; `analyzeHeuristic` y la subida de media no
comprobaban permiso ninguno —bastaba una sesión válida y un `entityId` ajeno—; y el alta de
usuario tomaba el `uid` del cuerpo sin contrastarlo con el token, así que se podía sobrescribir
la ficha de otra persona. Ninguna llegó a explotarse porque el panel seguía llamando a
Firebase: **cortar era exactamente lo que las abría**. Todas cerradas el 2026-09-08/09. Ver
también el detalle del primero:

**El router de empleados portado no comprobaba permiso ni cupo de plan.** Las Cloud
Functions llamaban a `canWrite` en cada controlador y miraban el plan al dar de alta; el
port a `checkinbiz` se dejó las dos cosas. Bastaba una sesión válida de cualquier entidad
y mandar el `entityId` ajeno. No llegó a explotarse porque el panel seguía llamando a
Firebase —cortar era justo lo que lo abría—, y está cerrado desde el 2026-09-08. La
lección va aquí porque no es de esta pieza: **un port 1:1 puede perder una comprobación
sin que nada se queje**, y lo que la echa en falta no es el typecheck, es leer el
controlador viejo entero.

**El CRUD de sucursales es la última escritura grande que no ve el contenedor.** De ahí que
`branch.*` siga sin lanzador y que sus disparadores no tengan a dónde colapsar todavía. Es el
motivo por el que las sucursales van en cabeza del roadmap, justo detrás de empleados.

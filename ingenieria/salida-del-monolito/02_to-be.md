# 02 — Arquitectura objetivo

## 1. `checkinbiz` es el núcleo, y el núcleo es lo que no puede fallar

El camino crítico del producto es corto y se dice en una frase: **un empleado con el móvil en
la mano valida su acceso, entra, pasa el segundo factor, mira su calendario y ficha.** Si eso
cae, el producto está caído. Un alta de plantilla puede esperar a mañana; un fichaje no, porque
detrás hay una jornada que alguien tiene que cobrar.

`checkinbiz` sirve ese camino y todo aquello de lo que ese camino depende:

| Ruta | Quién la llama | Por qué es núcleo |
|---|---|---|
| `POST /auth/validate` | la app, con el token del correo | sin ella no se entra |
| `POST /auth/login` | la app | |
| `POST /auth/2fa/enable` y `/2fa/verify` | la app y el kiosco | la huella del dispositivo se registra aquí |
| `GET /calendar`, `/calendar/availability` | la app y el panel | el calendario efectivo decide qué jornada se ficha |
| `POST /checklogs`, `/checklogs/update`, `/checklogs/manual-request` | la app, el kiosco y el panel | el fichaje |
| `/collaborators` | el panel del cliente y el backoffice (S2S) | quién tiene asiento en la empresa es lo que resuelve `canWrite`, y `canWrite` está por encima de cada escritura del camino |
| `POST /geo` | el panel, al dar de alta un centro | las coordenadas que resuelve son contra las que después la valla acepta o rechaza un fichaje |

Los dos últimos no son evidentes y por eso se escriben: **`geo` y `collaborators` no están aquí
por comodidad, están porque el fichaje depende de ellos.** Un permiso mal resuelto tumba la
escritura; unas coordenadas mal resueltas ponen la valla trescientos metros más allá y los
fichajes reales empiezan a salir `out_of_radius`. Nada de eso se ve como un fallo del servicio
que los sirvió: se ve como un fichaje que no cuenta.

Que sea el núcleo tiene consecuencias, no es una etiqueta:

- **No entra nada de lo que el fichaje no dependa.** Ni un CRUD de gestión, ni la heurística, ni
  un informe. Cada dependencia nueva es una forma más de que el arranque falle.
- **Se despliega poco.** Un servicio que cambia todas las semanas no es un núcleo. Sacarle los
  CRUD de gestión es, sobre todo, quitarle motivos de redespliegue.
- **Nadie lo tumba desde fuera.** Hoy un fallo en el alta de un empleado comparte proceso con el
  fichaje; después, no.

## 2. Un contenedor por dominio

| Servicio | Puerto | Prefijo | Qué sirve |
|---|---|---|---|
| `checkinbiz` | 3002 | `/api/v1/checkinbiz` | el núcleo: acceso, segundo factor, calendario, fichaje, colaboradores y geo |
| `employees` | 3013 | `/api/v1/employees` | alta, edición, borrado, validación y export de plantilla |
| `branches` | 3014 | `/api/v1/branches` | centros de trabajo |
| `entities` | 3015 | `/api/v1/entities` | la empresa: alta, edición, marca, usuarios y media |

Nombres en plural por coherencia con `documents`, `tasks` y `events`, que ya están así.

**Lo único que sale de `checkinbiz` es `employees`.** El resto de lo que hoy tiene se queda,
porque el camino central depende de ello.

**Lo que no vuelve a entrar:** la heurística, que cuando se porte va a `analytics`, donde ya
viven las tarjetas y el panel operativo.

## 3. Por qué esto es barato

Porque el dominio ya está fuera de `checkinbiz`. `createEmployee`, `updateEmployee`,
`deleteEmployee` y `buildEmployeesCsv` viven en `packages/shared/src/checkbiz/employees/`, y
`rentman` los llama directamente sin pasar por ningún servicio —fue el motivo de subirlos allí:
que un empleado importado desde un sistema externo naciera igual de completo que uno creado a
mano—. El `employee.router.ts` de `checkinbiz` son 95 líneas que solo abren la puerta.

Lo mismo con los centros: `FirestoreBranchRepository`, `canWrite` y el índice de búsqueda ya
están en `shared`. Y con la empresa: `platform/Entity` y su repositorio también.

Sacar cada dominio a su contenedor es, por tanto, montar un andamio —`Dockerfile`,
`package.json`, `app.ts`, `server.ts`, un bloque de compose y uno de nginx, todos calcados de
`events`— y mover un router. El trabajo de verdad no es la separación: es portar lo que aún no
está portado, y eso había que hacerlo de todas formas.

## 4. Dos reglas de dependencia

**Ningún servicio llama a `checkinbiz` por HTTP en el camino del fichaje.** Lo compartido se
comparte por `@encodebiz/shared`, no por red. Una llamada de más en ese camino es un fallo más
que puede dejar a alguien sin fichar.

**`checkinbiz` no llama a los nuevos.** Si el fichaje necesita saber algo de un empleado o de un
centro, lo lee de Firestore con el repositorio de `shared`, como hace hoy.

Del lado bueno, esto deja intacta la única dependencia interna que ya existe: el
`CheckinbizClient` del `backoffice` habla con `/api/v1/checkinbiz/collaborators`, y los
colaboradores no se mueven.

El `backoffice` sí tenía una salida hacia fuera: escribía la ficha de un cliente contra la
Cloud Function `updateEntity`, por `PLATFORM_UPDATE_ENTITY_URL`. Era la **única variable de
todo el entorno de desarrollo** que apuntaba a Firebase, y desde el 2026-09-09 va contra
`entities` por la red interna. La variable se queda vacía como interruptor de vuelta:
rellenarla con la URL de la función devuelve ese tráfico a Firebase sin desplegar nada.

## 5. Lo que hay que tocar fuera del monorepo

- **El panel**: cada corte es una variable de entorno que apunta al servicio nuevo. Sin cambios
  de código, gracias a los alias de
  [ADR-002](./adr/ADR-002-el-contrato-viejo-se-imita.md).
- **La app móvil**: no se toca. Todo lo que usa se queda en `checkinbiz`.
- **`nginx`**: tres bloques nuevos. Y el recordatorio de siempre: después de un `up -d` hay que
  reiniciarlo, o resuelve los upstreams contra las IP viejas de los contenedores.

## 6. A dónde va lo reactivo

Sin cambios respecto a lo decidido en [ADR-001](./adr/ADR-001-el-destino-es-el-caso-de-uso.md):
cada disparador se disuelve en el caso de uso que hace su escritura, cada cron pasa a ser un
cron del contenedor que lee lo que escribe, y a `services/firebase_sdk` va únicamente
`beforeUserCreated`, que es una blocking function de Auth y no existe fuera de Firebase.

Con la separación en contenedores, el destino de cada uno queda más claro que antes:

| Función | Destino |
|---|---|
| `onChecklogWrite`, `onChecklogSync`, `onChecklogWebhook`, patrones | casos de uso de `checkinbiz` |
| `sanitizerChecklog`, incidencias, planificadores | cron de `checkinbiz` |
| `onCreateEmployee` | caso de uso de `employees` |
| `onCreateBranch` | caso de uso de `branches` |
| `onDeleteEntity`, `onCreateSentEmail`, `processPendingEmails` | `entities` |
| `onTaskPattern`, `onWriteTaskRating`, `onTaskRatingSync`, `taskStartNotificationWorker` | `tasks` |
| `dailyCollectorData` | cron de `analytics`, que es quien lee lo que escribe |
| `onActivateCheckbiz`, `onDocumentWriteSubscriptions`, `processInvoices`, `triggerInvoiceWorker` | `billing`, al ritmo de [billing-v2](../billing-v2/04_fases.md) |
| `webhookWorker` | se borra: `events` ya corre su worker de rescate |
| `beforeUserCreated` | `services/firebase_sdk` |

## 7. Lo que hay que construir y no es de negocio

- **`ValidateSuscriptionLimit`** — el cupo del plan al crear un centro o un empleado. Va a
  `shared` porque lo necesitan dos servicios.
- **`slugify`** y el índice de búsqueda de entidades. El de empleados y centros ya está en
  `shared/checkbiz/search`.
- **Un dueño para el correo con plantilla.** `EmailService` está en `shared`; falta quién lo
  llama cuando hoy lo llama un disparador. Va con `entities`.

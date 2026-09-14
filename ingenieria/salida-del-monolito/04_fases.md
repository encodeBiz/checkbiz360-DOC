# 04 — Fases de implementación

Seis fases. Cada una es desplegable por separado, deja el sistema utilizable y tiene su
rollback escrito antes de empezar. **El HTTP va primero y lo reactivo después**, y no por
comodidad: un disparador solo puede desaparecer dentro de un caso de uso cuando ese caso de
uso ya existe y ya recibe la escritura. Portar el CRUD es lo que da destino a los
disparadores.

Dentro del HTTP el orden es **empleados → sucursales → entidad**, de lo que más se toca a lo
que menos, y además en ese orden cada fase le deja algo hecho a la siguiente: los alias y el
andamio del contenedor en la primera, el límite de plan y el índice de búsqueda en la segunda.

Cada una de las tres estrena un contenedor, según [ADR-003](./adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md).
El andamio es siempre el mismo y está calcado de `events` —`Dockerfile`, `package.json`,
`tsconfig.json`, `app.ts`, `server.ts`, un bloque en `docker-compose.staging.yml` y dos
`location` en `nginx.staging.conf`—, así que la primera vez cuesta una tarde y las dos
siguientes, un rato.

---

## Fase 1 — Empleados

**Objetivo:** que la gestión de plantilla del panel la sirva un contenedor propio, fuera del
núcleo.

**Prerequisito:** ninguno. Es la única fase que empieza con el dominio ya portado.

**Cambios**

- Servicio `employees` en el puerto 3013, sirviendo `/api/v1/employees`. Monta las funciones
  que ya están en `packages/shared/src/checkbiz/employees/`; no se reescribe ni una regla.
- Se mueve el router de `checkinbiz` —los dos, el autenticado y el público de `/validate`— y
  **se borra de allí**. El núcleo pierde su motivo más frecuente de redespliegue.
- Dos alias con la forma que manda el panel: `POST /employees/update` y `DELETE /employees`.
- Corte de cuatro variables: alta, edición, borrado y validación.
- Averiguar quién llama al export, o retirarlo. Ver [03 §4](./03_contratos-y-cortes.md).

**Lo que NO se toca aquí:** `onCreateEmployee` sigue vivo, y con él el apaño de
`createEmployee` de `shared` que crea el acceso antes que la ficha para que el disparador se
aparte y no mande una segunda bienvenida. Ese apaño se retira en la Fase 5, cuando el
disparador se vaya, y no antes.

**Criterio de éxito** — desde la pantalla real, no con curl: un alta que recibe **una sola**
bienvenida; una edición con cambio de correo que mueve también el acceso; un borrado que deja
la ficha en `fired` y retira su entrada de `searchIndex`; una validación. Y en Firestore, los
documentos idénticos a los que dejaba Firebase.

Y una comprobación que es de esta fase y de ninguna otra: **`checkinbiz` sigue fichando
mientras `employees` se cae**. Se para el contenedor nuevo y se ficha. Si eso no se prueba, la
separación es decorativa.

**Rollback:** las cuatro variables. El contenedor nuevo se queda desplegado sin tráfico.

---

## Fase 2 — Sucursales

**Objetivo:** sacar de Firebase la última escritura grande que el contenedor no ve, y darle
casa propia.

**Prerequisito:** Fase 1 —por el andamio y por el patrón de alias, y para no tener dos cortes
abiertos a la vez—.

**Cambios**

- Servicio `branches` en el 3014, sirviendo `/api/v1/branches`.
- `CreateBranch`, `UpdateBranch` y `DeleteBranch` sobre el `FirestoreBranchRepository` que ya
  está en `shared`.
- La validación de payload del controlador viejo se porta entera: son la mitad de sus 213
  líneas y es lo que impide que entre un horario mal formado.
- **`ValidateSuscriptionLimit`**, que hoy no existe en el contenedor. Va a `shared` porque la
  Fase 3 la vuelve a necesitar.
- Índice de búsqueda con `set()` idempotente —el bug de duplicados por reintento ya está
  arreglado en Firebase y no se puede reintroducir aquí—.
- Emisión de `branch.*` en el caso de uso, que es lo que le faltaba al catálogo de eventos.
- Tres alias y el corte de tres variables.

`geo` **no se mueve**: se queda en el núcleo, porque las coordenadas que resuelve son contra
las que después la valla acepta o rechaza un fichaje. `branches` lo llama desde el navegador,
como hoy.

**Antes de apagar nada:** mirar `createEntityBranch.controller`, la sucursal automática del
alta. Es la parte del disparador que hace trabajo de negocio, no de observación, y tiene
historia reciente de fallos silenciosos.

**Criterio de éxito:** crear, editar y borrar un centro desde el panel; el buscador lo
encuentra y **no aparece dos veces** tras editar; superar el cupo del plan devuelve 403 con
`subscription/limit_off`; `branch.created` sale una vez y solo una.

**Rollback:** tres variables.

---

## Fase 3 — Entidad

**Objetivo:** que el alta y la configuración de empresa salgan de Firebase.

**Prerequisito:** Fase 2, por `ValidateSuscriptionLimit`.

**Cambios**

- Servicio `entities` en el 3015, sirviendo `/api/v1/entities`. Se lleva también los usuarios
  —alta y recuperación de contraseña— y media, que son de la identidad del cliente.
- Alta, edición y branding. `slugify` y el índice de búsqueda de entidades, que no existen
  todavía en el contenedor.
- El alta de propietario **no se reescribe**: llama a los colaboradores del núcleo, que ya
  reparten asiento sobre `user_entity_roles`. Es la única llamada de un servicio nuevo hacia
  `checkinbiz`, y está fuera del camino del fichaje.
- Cuatro alias y el corte de tres variables.

**El borrado no entra.** `deleteEntity` arrastra `onDeleteEntity`, que cascadea, y una cascada
mal portada no se nota hasta que alguien busca lo que ya no está. Se queda en Firebase y se
trata en la Fase 5, con su propio criterio.

**Criterio de éxito:** un alta completa desde `/auth/register` de punta a punta —cuenta,
entidad, propietario, índice— y un cambio de branding que se ve en el panel y en los correos.

**Rollback:** tres variables. El borrado sigue donde estaba.

---

## Fase 4 — El resto del HTTP

Por orden de cuánto se usa. Usuarios y media ya han entrado con `entities` en la Fase 3.

1. **2FA de usuario** (`get2FAUserStatus`, `enable2FAUser`, `verify2FAUser`) → **`checkinbiz`**.
   Entra en cada login del panel, así que es lo más llamado de todo lo que queda, y es acceso:
   su sitio es el núcleo, junto al 2FA de empleado que ya está portado y del que copia el patrón.
2. **Heurística** → **`analytics`**, no al núcleo. El motor ya está en
   `checkinbiz/application/heuristic` y se mueve con ella; la función de Firebase son 64 líneas
   de envoltorio. Es la única pieza de esta fase que además **adelgaza** `checkinbiz`.
3. **`assignUser` completo** → `entities`. Hoy está portada la mitad que reparte permisos;
   falta la que crea la cuenta e invita.
4. **Responsabilidades** → `employees`. Es la responsabilidad de una persona sobre un centro.
   Su *lectura* se queda en `shared`, que es de donde la toma `canWrite` en el camino del
   fichaje; lo que se muda es el CRUD.
5. **Retiradas sin sustituto**: `addDeviceEmployee` —el verify del contenedor ya registra el
   dispositivo—, `sendEmail` —`EmailService` está en `shared`— y los dos de webhooks, que el
   panel ya no llama.

**Criterio de éxito:** un login con segundo factor de punta a punta; un análisis heurístico con
la misma respuesta que daba Firebase; y `checkinbiz` sin una sola ruta de gestión.

**Rollback:** por operación, su variable.

### `recalcDailyReport` se queda para la Fase 5, y no es un olvido

No lo llama nadie: no está en la allowlist del panel, no tiene variable de entorno y no
aparece ni en el front ni en la app. Es una herramienta de operación —rehacer un día de un
centro— que se dispara a mano.

Y comparte con `dailyCollectorData` el mismo constructor: 336 líneas de cálculo de horas,
costes y sospechas. Portar uno sin el otro deja esas 336 líneas duplicadas en dos casas, que es
justo la forma de que un día empiecen a divergir sin que nadie lo note —el síntoma no sería un
error, sería una tarjeta del panel con un número distinto—.

Así que va con el cron, en la Fase 5, y los dos a `analytics`: es el único que lee
`checkbiz_daily_report`, y el dueño de un dato tiene que ser quien lo escribe y quien lo lee, no
dos servicios coordinándose.

---

## Fase 5 — Lo reactivo

Aquí ya no hay variables de entorno: hay funciones que se apagan y código que las sustituye.
El orden vuelve a ser por frecuencia de ejecución.

1. **El fichaje.** `onChecklogWrite` con su cadena de patrones, `onChecklogSync` y
   `onChecklogWebhook`, dentro de `CreateChecklog` y `UpdateChecklog`. Es lo que más se ejecuta
   de la plataforma y, de paso, **cierra la ventana del evento duplicado** que hoy está abierta
   —ver [01 §6](./01_as-is.md)—.
2. **`dailyCollectorData`** como cron de `analytics`, que es quien lee lo que escribe.
3. **Tareas:** valoraciones, patrones de tarea, sincronización y el aviso de tarea no iniciada.
4. **Empleado, centro y servicio:** `onCreateEmployee` —y con él, retirar el apaño del `uid`—,
   `onCreateBranch` y `onActivateCheckbiz`.
5. **Sanitizador, incidencias y planificadores**, que van juntos porque el sanitizador es quien
   abre la incidencia.
6. **La cola de correo:** `onCreateSentEmail` y `processPendingEmails`.
7. **`beforeUserCreated` a `services/firebase_sdk`.** El único inquilino nuevo: es una blocking
   function de Auth y no existe fuera de Firebase. Ojo, **solo puede haber una por proyecto**:
   aquí no cabe solapamiento ni por error, hay que quitar la vieja antes de desplegar la nueva.
8. **`webhookWorker` se borra** —`events` ya corre su worker de rescate— y lo de facturación
   entra al ritmo de [billing-v2](../billing-v2/04_fases.md), que retira `triggerInvoiceWorker`
   por construcción en su F1.

**Las tres reglas de esta fase**

- **Nunca conviven el disparador y su sustituto.** Hay precedente de doble acumulación en los
  patrones por un disparo repetido, y un dato mal sumado no avisa.
- **Cada sustituto nace detrás de un flag apagado.** Se despliega el contenedor con el flag a
  cero, se retira la función de Firebase, se enciende el flag. Tres gestos separados, cada uno
  reversible sin desplegar.
- **Un hueco se repara; un doble conteo no.** Si hay que elegir, se elige el hueco:
  `RepairEmployeePatterns` en `analytics` y `reindex-search.ts` en `rentman` rehacen lo que se
  pierda en unos minutos.

**Criterio de éxito:** un fichaje real produce un patrón correcto, una fila en Postgres y
**un** evento; una jornada incompleta abre su incidencia; el panel sigue pintando sus tarjetas
al día siguiente.

---

## Fase 6 — Apagado

**Prerequisito:** las cinco anteriores, con tiempo de observación en producción.

- Quitar del `index.ts` del SaaS lo retirado y desplegar el codebase `default` **por nombre de
  función**, una a una, mirando el resultado de cada una.
- Cerrar el repositorio `encodeBiz-SAAS` para checkbiz. Passinbiz se apaga con él.

**El aviso que no se puede olvidar:** un despliegue de Functions lanzado desde `encodebiz-api`
con `codebase: default` **borraría todas las funciones del SaaS**, porque Firebase entiende que
lo que no está en el código sobra. Lo que lo impide es el `codebase: "triggers"` del
`firebase.json`. Y la bandera de proyecto va siempre explícita: sin ella, un despliegue puede
acabar en el proyecto equivocado en silencio.

---

## Criterio de cierre

La salida está terminada cuando en los proyectos de Firebase queda **el codebase `triggers` con
dos funciones** —el barrido de cuentas fantasma y la blocking function de alta— y nada más.
Firestore sigue siendo la base de datos y Firebase Auth el directorio de identidades; lo que se
retira es el cómputo.

---

## Ritmo

Las tres primeras fases caben en una semana de trabajo, y la cuarta empieza. La quinta no: son
veintinueve funciones, cada una con su ventana de corte y su comprobación, y la mitad tocan el
camino del fichaje. Meterlas con calzador en los mismos cuatro días es exactamente la forma de
convertir una migración ordenada en una noche de guardia.

Lo honesto es cerrar 1, 2 y 3 esta semana —que es sacar del monolito los tres CRUD que más se
tocan— y planificar la 5 con su propio calendario.

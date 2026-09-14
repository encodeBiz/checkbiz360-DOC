# Triaje de hallazgos — QA de CheckBiz360

Auditoría de [hallazgos.md](./hallazgos.md) hecha el **2026-09-13**: cada hallazgo abierto
recibe un nivel, una justificación y una resolución concreta, y van ordenados de más a menos
importante. **No se ha arreglado nada**: es solo clasificación y plan. Todo lo que aquí se
afirma del código se ha releído en `encodebiz-api` (rama `staging`, `690ad95`), y en el panel
y la app donde el hallazgo lo requería.

## Estado a la tarde del 2026-09-13

Los 9 críticos y los 12 altos están **corregidos en desarrollo**, en la rama
`feat/hallazgos-criticos-y-altos` de `encodebiz-api` (fusionada en `develop` y `staging` por la
cadena de siempre) y, para HAL-02 y HAL-05, en `feat/retirar-triggers-duplicados` del SaaS
(fusionada en su `develop`, sin desplegar). De rebote cayeron HAL-11 y quedó marcado HAL-18.
La suite completa se ha ejecutado contra staging tras cada ronda: la segunda y la tercera
—la de HAL-07— terminaron con **321 pruebas en verde y ninguna en rojo**. Cada hallazgo lleva en [hallazgos.md](./hallazgos.md) su bullet **Corregido**
con el detalle y los casos que lo cubren.

Lo que no se ha podido hacer desde aquí, porque el clasificador lo bloqueó o porque no es de
este repositorio:

1. **Borrar en `dev-encodebiz` las tres funciones duplicadas** (HAL-02, HAL-05, residuo de
   HAL-31). Ya no están en el índice del SaaS; falta retirarlas de GCP:
   ```bash
   firebase functions:delete apiV100-firebaseFirestoreTriggersCheckinBiz-onChecklogWebhook --region europe-west1 --project dev-encodebiz --force
   firebase functions:delete apiV100-firebaseFirestoreTriggers-processInvoices --region europe-west1 --project dev-encodebiz --force
   firebase functions:delete apiV100-firebaseEntrySchedule-triggerInvoiceWorker --region us-central1 --project dev-encodebiz --force
   ```
2. **Suscribir `invoice.created`** en el webhook de Stripe de desarrollo
   (`we_1U8be9R97dgHV4NJYIdAy2Tv`, modo prueba) y en el de producción en su pase. Sin él,
   HAL-19 solo audita: la corrección del borrador no llega a ejecutarse.
3. **Cerrar las reglas de Firestore.** Mientras el panel escriba `user_entity_roles` desde el
   navegador, HAL-21 y HAL-27 se rodean.
4. **Panel:** pedir la tarjeta antes de activar (HAL-20; hoy recibirá `entity_not_configured`
   sin decir qué falta). **App:** dar mensaje a `checklog/absence` (HAL-29) y a
   `checklog/different_branches` en descansos (HAL-28); y en el primer pase a producción de
   HAL-07 las apps instaladas repetirán el login una vez, por su propio camino de reserva.
5. **Producción:** comprobar qué funciones del SaaS están desplegadas antes del pase (HAL-02),
   y el valor de `BILLING_TRIAL_DAYS` (residuo de HAL-12).

Tres decisiones de contrato tomadas al arreglar, por si alguien las quiere de otra forma:
un `isAdmin` que no sea booleano es un `400` (HAL-16); el descanso en otro centro responde
`different_branches` como la salida (HAL-28); rechazar admite trabajo en curso, completado o
validado, y nunca lo no empezado ni lo ya sellado (HAL-35).

## Segunda tanda, 2026-09-14: los medios y el bajo

Nueve de los once medios y el bajo, en `feat/hallazgos-medios-y-bajos` de `encodebiz-api`
(fusionada en `develop` y `staging`), más el panel (`feat/planes-retirados-ocultos`, HAL-13) y
la app (`fix/codigo-invalid-checkin`, HAL-09), esas dos en ramas nuevas desde sus `develop` y
sin fusionar. Cada uno lleva su bullet **Corregido** en el catálogo; la suite ya no tiene
ningún indulto y la ejecución completa contra staging terminó con **321 pruebas en verde y
ninguna en rojo**. HAL-11 había caído con HAL-07.

**Dos decisiones de producto que no se han tomado**, y por qué:

- **HAL-03**, la sucursal nace con la geocerca desactivada, y **HAL-04**, el empleado nace sin
  verificación de dispositivo. Las dos son valores por defecto de los formularios del panel
  que cambian el alta para todos los clientes nuevos —una sucursal con geocerca exige
  coordenadas buenas desde el primer día; un empleado con segundo factor tiene que
  configurarlo antes de fichar—, y el catálogo las anota como «intención sin establecer».
  Con HAL-07 cerrado, HAL-04 vuelve a ser una preferencia. Recomendación: geocerca activa
  por defecto (HAL-03) y segundo factor como está (HAL-04); las dos son un booleano en el
  formulario cuando se decidan.

**Tres decisiones tomadas al arreglar**, anotadas por si alguien las quiere de otra forma:
el rechazo de una corrección devuelve el fichaje a como estaba en vez de invalidarlo
(HAL-15); una semana definida con los siete días apagados cierra el día y el respaldo abierto
queda solo para quien no tiene semana (HAL-17); y sin horario la lectura responde 200 con
`configured: false` en vez de 404 (HAL-22).

## Cómo se ha clasificado

- **Crítico.** Cualquier cuenta —o cualquier miembro— accede a datos o poderes de **otra
  empresa**, o el **registro de jornada**, que tiene valor legal, se altera o se pierde en
  silencio. Se arreglan antes que nada y se llevan a producción sin esperar al siguiente pase.
- **Alto.** Un dato de negocio sale mal dentro de la propia empresa, hay dinero por medio, o
  existe un control que el producto ofrece y no se aplica. Van en la siguiente tanda.
- **Medio.** Incoherencias, fugas menores, suciedad de datos y decisiones de producto que hay
  que tomar antes de tocar código. Entran cuando se toca el módulo.
- **Bajo.** Cosmético.
- **Cerrados con residuo.** Ya corregidos en desarrollo, pero con una cola que conviene no
  olvidar.

Dentro de cada nivel, el orden también importa: va antes lo que explota con menos requisitos
y lo que afecta a más gente.

## Una advertencia que cruza toda la lista

Las reglas de Firestore de desarrollo dejan leer y escribir **todo** a cualquiera hasta 2030,
`user_entity_roles` incluido, y el panel todavía escribe ahí directamente (por ejemplo al
aceptar una invitación, `entity.service.ts:72`). Mientras eso siga así, cualquier permiso que
se arregle en un contenedor es decorativo en desarrollo: se puede rodear escribiendo la
colección desde el navegador. Producción no se ha mirado. Por eso los hallazgos de permisos
(HAL-06, HAL-08, HAL-21, HAL-27, HAL-32) hay que **cerrarlos junto con las reglas**, no antes
ni en lugar de ellas.

---

## Resumen ordenado

| # | HAL | Nivel | Qué pasa | Resolución en una línea |
|---|---|---|---|---|
| 1 | HAL-06 | Crítico | Cualquier cuenta lee y reescribe el calendario de cualquier empresa | Pertenencia a la entidad en las cinco rutas de calendario |
| 2 | HAL-08 | Crítico | Cualquier cuenta se suscribe a los fichajes de otra empresa y lee su secreto | `canWrite` en cada ruta de `endpoints` |
| 3 | HAL-32 | Crítico | Cualquier cuenta genera el informe de otra empresa y se lo deja en su histórico | El `canWrite` que ya tiene la descarga, en la generación |
| 4 | HAL-21 | Crítico | Un administrador se hace propietario y aparta al dueño | Pasar el actor a conceder y modificar, como ya hace el borrado |
| 5 | HAL-34 | Crítico | Corregir la hora no llega al registro legal de Postgres | Añadir `timestamp` y `real_date_market` al `ON CONFLICT` y reconstruir |
| 6 | HAL-14 | Crítico | Una corrección con ids cruzados cambia de dueño el fichaje | Comparar el `employeeId` del fichaje con el del cuerpo y no reescribirlo |
| 7 | HAL-07 | Crítico | Sesión de trabajador con dos ids sin firma y sin caducidad | Token de validación firmado y con vida corta; sesión con `expiresIn` |
| 8 | HAL-16 | Crítico | `isAdmin:"true"` ficha como otro y salta el dispositivo de confianza | Normalizar `isAdmin` a booleano en el router y no leer `uid` del cuerpo |
| 9 | HAL-27 | Crítico | Un asiento desactivado conserva todos los permisos de escritura | `canWrite` exige `status:"active"` |
| 10 | HAL-26 | Alto | El panel pide la hora del fichaje y el servidor la tira | Aceptar y validar `timestamp` en la vía `isAdmin` |
| 11 | HAL-29 | Alto | Quien está de vacaciones ficha igual | El fichaje consulta las ausencias como ya hace el tablero |
| 12 | HAL-28 | Alto | Un descanso se engancha a una jornada cerrada de otro día | El descanso cuelga del último fichaje, no del último `checkin` del centro |
| 13 | HAL-35 | Alto | Las tareas no miran el estado de origen | Tabla de transiciones `origen → destino` en un solo sitio |
| 14 | HAL-19 | Alto | Si el aviso previo no llega, la factura sale a 0 € | Conciliación tras `invoice.finalized` con alerta |
| 15 | HAL-20 | Alto | checkinbiz se activa sin método de pago (regla de producto) | `isConfigured` exige `payment_method` también en modo checkbiz |
| 16 | HAL-36 | Alto | La política de terminación se guarda y no la lee nadie | Completar por asignación y cerrar la tarea cuando la política lo diga |
| 17 | HAL-24 | Alto | Editar un centro reactiva la geocerca; borrarlo deja huellas | No rellenar el campo ausente; borrado con existencia y limpieza |
| 18 | HAL-37 | Alto | Rechazar una tarea deja su pausa abierta | Cerrar la pausa en la misma transacción, como el resto |
| 19 | HAL-30 | Alto | Al remoto se le busca el turno del día del centro | Decidir de quién es el día; el `tzHint` ya existe |
| 20 | HAL-02 | Alto | En desarrollo cada fichaje sale dos veces por webhook | Retirar `onChecklogWebhook`; comprobar producción |
| 21 | HAL-05 | Alto | La facturación del día 5 sigue programada en desarrollo | Pausar el job y retirar la función con `processInvoices` |
| 22 | HAL-23 | Medio | Modificar una responsabilidad la inventa; un puesto sin precio guarda `NaN` | Existencia antes de escribir y `price` validado |
| 23 | HAL-25 | Medio | La edición de ficha acepta cualquier campo | Lista blanca. **El impacto sobre dispositivos que describe no se sostiene** |
| 24 | HAL-10 | Medio | Un anónimo sondea qué tareas existen y en qué estado | Credencial antes de buscar |
| 25 | HAL-11 | Medio | `null` en base64 devuelve 500 con la traza | Comprobar que lo decodificado es un objeto; no devolver `err.message` |
| 26 | HAL-17 | Medio | Apagar los siete días abre el fichaje | Decisión; si procede, quitar `hasAnyShifts` de `noConfig` |
| 27 | HAL-22 | Medio | Sin horario, la app rompe y el fichaje funciona | Decisión: horario por defecto en el alta o lectura que devuelve el día abierto |
| 28 | HAL-13 | Medio | Un plan retirado sigue visible y no se puede contratar | No listar planes sin `stripePrice`; retirar `freemium` |
| 29 | HAL-01 | Medio | Suscribir sin cliente de Stripe da un 500 genérico | Capturar los errores con código en billing y responder 4xx |
| 30 | HAL-15 | Medio | Rechazar una corrección deja la hora rechazada | Decisión; si procede, restaurar `previousDate` |
| 31 | HAL-03 | Medio | La sucursal nace con la geocerca desactivada | Decisión de producto; después, el formulario |
| 32 | HAL-04 | Medio | El empleado nace sin verificación de dispositivo | Decisión de producto; pesa más mientras HAL-07 esté abierto |
| 33 | HAL-09 | Bajo | La app compara con `invalid_checki` | Corregir la cadena y publicar con la siguiente versión |
| — | HAL-33 | Cerrado | El espejo de Postgres vacío | Residuo: sin reintentos, histórico sin reinyectar |
| — | HAL-31 | Cerrado | Función vieja y contenedor procesaban Stripe | Residuo: `processInvoices` sigue desplegada |
| — | HAL-18 | Cerrado | Desarrollo sordo a Stripe | **Ya está arreglado y el catálogo no lo dice** |
| — | HAL-12 | Cerrado | Prueba de 45 días | Residuo: el código sigue con 45 por defecto; producción sin mirar |

---

## Crítico

### 1 · HAL-06 · El calendario de cualquier empresa lo escribe cualquier cuenta

- **Por qué es el primero.** Es lo más barato de explotar de toda la lista: basta una cuenta
  de Firebase del proyecto —el registro es abierto— y un `entityId`, que viaja en las URLs
  del panel. Y el daño es máximo: cerrando los días de una empresa su plantilla entera deja de
  poder fichar, y de paso se lee cómo organiza el trabajo. Probado con peticiones reales.
- **Resolución.** El montaje en `app.ts:46` solo pone `requireFirebaseAuth`. Hace falta
  pertenencia en las cinco rutas:
  - Escritura (`POST`, `PATCH`, `DELETE`, `savePreset`): `canWrite(uid, entityId)` para el
    alcance `entity`; para `branch` y `employee`, el mismo `canWrite` con
    `includeBranchResponsibility` y el nivel mínimo que decida producto (hoy supervisor).
  - Lectura (`GET /`, `/availability`, `/availability/day`): la app la usa con el token de
    Firebase del propio trabajador, así que la regla es «asiento en la empresa **o** ficha de
    empleado con ese `uid`». Ese cálculo ya está escrito en `resolveTaskActor`
    (`services/tasks/.../task.helpers.ts:149`).
  - Lo razonable es sacar ese resolutor a `@encodebiz/shared` como middleware y montarlo en
    calendario, eventos e informes de una vez, en lugar de repetir la comprobación ruta a ruta.
- **Verificación.** CHK-11-10 y CHK-12-22 pasan de fallo esperado a verde.

### 2 · HAL-08 · Los webhooks salientes no comprueban la entidad

- **Por qué aquí.** Es exfiltración continua: quien registre su URL en los eventos de otra
  empresa recibe cada fichaje de su plantilla —datos personales— hasta que alguien lo note, y
  además puede leer el secreto de firma o borrar la integración legítima.
- **Resolución.** En `services/events/src/interfaces/http/events.router.ts`, cada ruta de
  `endpoints` (alta, listado, edición, borrado, rotación de secreto) recibe el `entityId` por
  cuerpo o query: añadir `canWrite(uid, entityId)` justo después de leerlo, o el middleware
  compartido del punto anterior. La ruta `s2s/publish` va por API key y no está afectada.
- **Después de cerrarlo.** Revisar en desarrollo si existen endpoints registrados por
  cuentas que no pertenecen a su entidad, y decidir si en producción se rotan los secretos de
  firma por precaución. Producción no se ha mirado.

### 3 · HAL-32 · Cualquier cuenta genera el informe de otra empresa

- **Por qué aquí.** Con el `entityId` se obtienen nombres de empresa, centros y empleados, se
  ensucia el histórico ajeno y, en el informe de asistencia, se emite `report.generated`
  hacia los webhooks de la víctima.
- **Resolución.** `services/reports/src/interfaces/report.router.ts`: la comprobación está
  escrita en la descarga (`:115`, `canWrite(uid, entityId)` → `403 report/unauthorized`).
  Copiarla tal cual en `POST /generate` (`:24`) y `POST /tasks` (`:50`), antes de generar.
  Después, borrar de la entidad de prueba los informes que la suite dejó al medirlo.
- **Verificación.** INF-02-11 a verde; INF-01-14 sigue pendiente de datos precalculados.

### 4 · HAL-21 · Un administrador se hace propietario

- **Por qué aquí y no antes.** Requiere ya un asiento de administrador, así que no lo explota
  cualquier cuenta; pero el resultado es la toma completa de la empresa —cobros, baja del
  servicio, apartar al dueño, entregarla a un tercero—.
- **Resolución.** `manageCollaborator.ts`: `removeCollaborator` (`:204-233`) ya recibe
  `actor` y aplica `owner_required`. Dar el mismo `actor` a `assignCollaborator` (`:120`) y
  `updateCollaborator` (`:167`) y aplicar tres reglas: solo un propietario concede `owner`;
  solo un propietario toca el rol o el estado de otro propietario; nadie se cambia el rol a sí
  mismo. El router (`collaborator.router.ts:74`) ya construye `collaboratorActor`, solo hay
  que pasarlo.
- **Depende de.** Cerrar las reglas de Firestore: mientras el panel pueda escribir
  `user_entity_roles` desde el navegador, este control se rodea.
- **Verificación.** COL-04-02, COL-04-03 y COL-02-04 a verde; COL-05-04 sigue en verde.

### 5 · HAL-34 · Corregir la hora no cambia el informe legal

- **Por qué es crítico sin ser de seguridad.** El registro de jornada es el documento con
  valor legal, la corrección con doble firma es el mecanismo que la ley da para enmendarlo, y
  aquí se ejecuta, se firma y **no llega**. Es silencioso: las dos respuestas son 200, el
  panel enseña la hora buena y `sync_log` dice `success`.
- **Resolución.** `services/sync/src/interfaces/sync.router.ts:91-106`: añadir
  `timestamp = EXCLUDED.timestamp` y `real_date_market = EXCLUDED.real_date_market` al
  `ON CONFLICT (id) DO UPDATE`. Mejor todavía: enumerar todas las columnas salvo `id`, para que
  la lista deje de envejecer (hoy también quedan fuera `type`, `branch_id`, `employee_id`,
  `checkin_ref` y las de geo). Después, reejecutar `BuildEmployeeDailyReports` para los días
  con correcciones, y reinyectar los fichajes corregidos históricos; la hora buena está en
  `metadata_raw`, así que se puede recuperar sin volver a Firestore.
- **Verificación.** INF-03-02 a verde.

### 6 · HAL-14 · Una corrección con ids cruzados cambia de dueño el fichaje

- **Por qué aquí.** Reescribe a quién pertenece una jornada, y la notificación va al nuevo
  dueño. Requiere permiso de escritura en la empresa o una sesión de trabajador con un `id` y
  un `updateId` ajenos, así que es intra-empresa, pero toca el registro legal.
- **Resolución.** `updateChecklog.controller.ts:120-124`: tras `findById(id, entityId)`,
  si `checkData.employeeId !== employeeId` responder `404 checklog/not_found` (no revelar). Y
  en `:238-270` no tomar nunca `employeeId` del cuerpo al reescribir: el dueño es el del
  fichaje. En la vía de trabajador, exigir además que el `employeeId` de la sesión coincida.
- **Verificación.** CHK-09-14 a verde.

### 7 · HAL-07 · Sesión de trabajador con dos identificadores sin firma

- **Por qué aquí.** Suplantación de trabajador sin credencial, con sesión que no caduca. Los
  dos ids son de Firestore y no se adivinan, pero se filtran por todas partes: webhooks
  (HAL-08), informes (HAL-32), URLs del panel y el propio correo de bienvenida. Es el eslabón
  que encadena HAL-16 y HAL-04.
- **Resolución.** El token lo emiten dos sitios con el mismo formato:
  `loginEmployee.controller.ts:38` tras un login con Firebase, y el correo de bienvenida
  (`packages/shared/src/checkbiz/employees/employeeAccess.ts:66`). Los dos deberían emitir un
  JWT firmado con `JWT_2FA_SECRET`, vida corta y un solo uso, y `validateEmployee` —el
  controlador y su gemelo de shared— verificarlo en lugar de decodificar base64. Y el
  `sessionToken` sale con `expiresIn`, que hoy no lleva ni en `:63` ni en `validateEmployee.ts:68`.
  Hay que coordinar con la app: la versión instalada espera el formato actual, así que el
  servidor tendrá que aceptar los dos durante una ventana.
- **Verificación.** La prueba que hoy fija «acepta un token fabricado» pasa a esperar 401.

### 8 · HAL-16 · `isAdmin` en texto ficha con el uid de quien quiera

- **Por qué aquí.** Con la sesión de un empleado y el uid de un administrador —que queda
  escrito en cada fichaje del panel— se ficha sin dispositivo de confianza y el registro
  queda firmado por otro.
- **Resolución.** `checklog.router.ts:32`: normalizar antes de bifurcar,
  `req.body.isAdmin = req.body.isAdmin === true`, y en la rama de sesión de trabajador
  **borrar** `uid` e `isAdmin` del cuerpo antes de mezclar el payload de la sesión. Con eso
  `createChecklog.controller.ts:132` deja de ver un `uid` que no viene de un token.
- **Verificación.** CHK-08-79 a verde.

### 9 · HAL-27 · Un asiento desactivado conserva los permisos

- **Por qué aquí.** «Desactivar» es lo que se hace cuando alguien deja la empresa. Hoy le
  quita el panel y le deja la API entera, porque `canWrite` es la puerta de todas las
  escrituras de checkinbiz.
- **Resolución.** `packages/shared/src/checkbiz/auth/canWrite.ts:16-21`: exigir
  `status === "active"` además del rol. `assignCollaborator` siempre escribe `status`
  (`manageCollaborator.ts:141`), pero conviene comprobar antes en desarrollo que no queden
  asientos antiguos sin el campo; si los hay, rellenarlos con `active` en la misma tanda.
- **Verificación.** CHK-08-77 a verde; COL-03-05 sigue en verde.

---

## Alto

### 10 · HAL-26 · El panel pide la hora del fichaje y el servidor la tira

- **Por qué encabeza el nivel.** Es la vía normal para registrar lo que la app no registró,
  y todo fichaje que entra por ahí queda con una hora que no es la que ocurrió, sin aviso.
  Toca el registro legal en su camino más habitual.
- **Resolución.** `createChecklog.controller.ts:359`: en la vía `isAdmin`, si llega
  `timestamp` en el cuerpo, validarlo (no futuro, dentro de una ventana que decida producto)
  y usarlo; si no llega, `now`. La validación de secuencia contra el último fichaje tiene que
  hacerse con esa hora, no con la actual. En la vía de trabajador, seguir ignorándolo.
- **Verificación.** CHK-08-74 a verde.

### 11 · HAL-29 · Quien está de vacaciones ficha igual

- **Por qué.** Contradice al panel, que da a esa persona por ausente, y la jornada cuenta como
  trabajada en el informe y en lo que ve la gestoría.
- **Resolución.** `createChecklog.controller.ts:291` solo mira `holidays`. Añadir la consulta
  de `absences` del empleado para `dateLocal` reutilizando la expansión de rangos que ya hace
  `resolveAvailability.usecase.ts:193-197`, y responder `400 checklog/day_disabled` con un
  código propio (`checklog/absence`) para que la app pueda explicarlo.
- **Verificación.** CHK-08-28 a verde; CHK-17-03 sigue en verde.

### 12 · HAL-28 · Un descanso se engancha a una jornada cerrada de otro día

- **Por qué.** Cambia las horas de una jornada ya cerrada, hacia atrás en el tiempo, con solo
  equivocarse de centro en la app.
- **Resolución.** `CreateChecklog.ts:57-63` busca el último `checkin` del centro, sin mirar
  `closed`. El descanso pertenece a la jornada abierta: colgarlo del `last` que ya se tiene
  arriba (la secuencia ya exige que sea `checkin` o `restout`) y aplicar
  `checklog/different_branches` también a `restin`/`restout`, como hace `checkout` en `:31-33`.
- **Verificación.** CHK-08-59 a verde.

### 13 · HAL-35 · Las tareas no tienen máquina de estados

- **Por qué.** La validación es la firma de la empresa, y cualquier asignado la deja sin
  efecto; el informe sigue contando la tarea como validada.
- **Resolución.** `updateTaskStatus.controller.ts:104-167` y `rejectTask.controller.ts`
  deciden por destino. Escribir una tabla `origen → destinos permitidos` en `task.helpers.ts`
  y comprobarla antes que nada en los dos controladores; las vueltas atrás (`assigned`,
  `draft`) limpian también `validatedAt`/`validatedBy`/`rejectedAt`/`rejectedBy`; `rejectTask`
  exige `completed` igual que `validateTask`. Va en la misma tanda que HAL-36 y HAL-37: es el
  mismo controlador.
- **Verificación.** TSK-11-30, TSK-11-65 y TSK-15-14 a verde.

### 14 · HAL-19 · Si el aviso previo no llega, la factura sale a 0 €

- **Por qué.** El mecanismo funciona cuando el aviso llega —medido—, pero cualquier corte del
  webhook convierte el mes en gratis sin que nada lo señale, y ya ocurrió una vez.
- **Resolución.** En `StripeWebhookHandler.ts`, al recibir `invoice.finalized` (o
  `invoice.created`), comparar la cantidad de la línea con el recuento actual: si difiere, y
  sobre todo si es 0 con empleados activos, avisar al backoffice y anotarlo en la
  suscripción. Corregir el borrador antes de que se cobre solo si Stripe lo permite en esa
  fase; si no, emitir la diferencia. Probar con un reloj de prueba de Stripe, nunca con
  `trial_end: "now"`.

### 15 · HAL-20 · checkinbiz se activa sin método de pago

- **Por qué.** Regla de producto confirmada el 2026-09-12: la tarjeta distingue al cliente del
  que prueba. Hoy no se cumple y al final de la prueba no hay con qué cobrar.
- **Resolución.** `FirestoreEntityRepository.ts:51-70`: el camino `checkbiz` de `isConfigured`
  añade `billingConfig.payment_method` no vacío. El panel tiene que pedir la tarjeta antes de
  activar (hoy solo se crea el cliente al abrir el portal, HAL-01). Y la suite: `crearMundo`
  necesita adjuntar un método de pago de prueba antes de activar, o deja de funcionar entera.
- **Verificación.** FAC-03-17 a verde.

### 16 · HAL-36 · La política de terminación no la lee nadie

- **Por qué.** Invisible con dos asignados, visible con treinta: en cuanto se asigne una
  sucursal entera, uno cierra por todos.
- **Resolución.** `completionPolicy` aparece dos veces en el repositorio y ninguna la lee. En
  la rama `completed` de `updateTaskStatus.controller.ts`, con `all_assigned_workers`: marcar
  solo la asignación del actor como completada y pasar la tarea a `completed` cuando no quede
  ninguna abierta; hasta entonces sigue `in_progress`. Con `any_assigned_worker`, como hoy.
- **Verificación.** TSK-11-44 a verde.

### 17 · HAL-24 · Editar un centro reactiva la geocerca; borrarlo deja huellas

- **Por qué.** Corregir una letra del nombre cambia dónde puede fichar la plantilla de ese
  centro, sin que nadie lo pida. Los otros dos son suciedad.
- **Resolución.** `branch.validation.ts:264`: incluir `disableRatioChecklog` en el payload
  solo cuando venga en el cuerpo (es una edición parcial). `FirestoreBranchRepository.ts:123`:
  comprobar existencia y responder 404; y al borrar, retirar el `branchId` de cada ficha con
  `arrayRemove`, que es lo que ya hace `deleteResponsibility` del repositorio de empleados y
  no hace `deleteResponsabilities` del de sucursales.
- **Verificación.** SUC-02-04, SUC-04-03 y SUC-04-05 a verde.

### 18 · HAL-37 · Rechazar una tarea deja su pausa abierta

- **Resolución.** `rejectTask.controller.ts` escribe con `updateTaskUseCase`, fuera de la
  transacción que cierra pausas. O bien pasa a usar `updateTaskStatusUseCase` con
  `closePause: {endedReason: "rejected"}` como completar y cancelar
  (`updateTaskStatus.controller.ts:120-146`), o bien el rechazo se convierte en una rama más de
  ese controlador. Con HAL-35 resuelto, además, una tarea rechazada ya no se puede reanudar.
- **Verificación.** TSK-15-13 a verde; TSK-08-21 queda por escribir.

### 19 · HAL-30 · Al remoto se le busca el turno del día equivocado

- **Decisión previa.** De quién es el día de un trabajador remoto: el suyo o el de su empresa.
  Recomendación: el suyo, porque las horas ya se comparan en su zona y es lo que la persona ve.
- **Resolución, si se decide así.** `createChecklog.controller.ts:205` llama a
  `resolveDay.execute` sin `tzHint`; `RequestManualChecklogCreation.ts:273` ya lo pasa. Basta
  calcular `tz` antes y pasarlo. El día, la fecha local y los festivos salen entonces de la
  misma zona que las horas.
- **Verificación.** CHK-08-70 (la mitad del día) a verde.

### 20 · HAL-02 · En desarrollo cada fichaje sale dos veces por webhook

- **Resolución.** `onChecklogWebhook` no se portó a `services/firebase_sdk` a propósito (es
  del módulo viejo de webhooks): retirarla del índice del SaaS y borrarla en `dev-encodebiz`
  por nombre. Antes del pase a producción, listar sus funciones y confirmar si allí también
  está desplegada; el catálogo dice que producción no se ha mirado.
- **Verificación.** LIS-03 a verde.

### 21 · HAL-05 · La facturación del día 5 sigue programada en desarrollo

- **Resolución.** Pausar el job de Cloud Scheduler de `triggerInvoiceWorker` en
  `dev-encodebiz` y retirar la función junto con `processInvoices` (residuo de HAL-31): las dos
  quedaron fuera del porte porque billing-v2 las retira. Producción: confirmar con producto
  que el cron del día 5 está retirado allí, que es lo que dice el diseño de billing.

---

## Medio

### 22 · HAL-23 · Modificar una responsabilidad la inventa; un puesto sin precio guarda `NaN`

- **Resolución.** `FirestoreEmployeeRepository.ts:71-73`: `get` antes de `set(merge)`, 404 si
  no existe, y `await` (hoy falta). En el router, validar `job.price` como número finito con
  zod y responder 400. Es medio y no alto porque el `NaN` solo entra si el panel omite el
  precio, y el documento inventado no da poder (`canWrite` exige `active == 1`).

### 23 · HAL-25 · La edición de ficha acepta cualquier campo

- **Corrección al catálogo.** El hallazgo dice que escribir `trustedDevicesId` en la ficha
  «equivale a dar de alta un dispositivo de confianza». No es así: la comprobación del fichaje
  (`createChecklog.controller.ts:172`, `FindSecurityEmployee`) lee `findSecurity`, que va a la
  subcolección `employees/{id}/security/trustedDevicesId`
  (`FirestoreEmployeeRepository.ts:189`). El campo que `POST /employees/update` deja en el
  documento es inerte. Por eso baja a medio.
- **Lo que sigue siendo cierto.** No hay lista blanca, y cualquier campo que el sistema use
  para decidir (`enableA2F`, `enableRemoteWork`, `price`, `branchId`, `status`) es escribible
  por quien ya es propietario o administrador. Resolución: una lista de campos editables en
  `employee.router.ts:252-281`, y todo lo demás se descarta.

### 24 · HAL-10 · Un anónimo sondea qué tareas existen

- **Resolución.** En los controladores de tarea, exigir credencial antes de buscar:
  `resolveTaskActor` necesita `task.branchId`, así que lo mínimo es verificar el token (o la
  sesión de trabajador) al principio y devolver 401 uniforme, y solo después buscar y
  autorizar. El 404 de dominio y el de ruta pueden seguir siendo distintos una vez
  autenticado.

### 25 · HAL-11 · `null` en base64 revienta con la traza

- **Resolución.** Tras `JSON.parse` en `validateEmployee.controller.ts:29` y
  `validateEmployee.ts:35`, comprobar `decoded && typeof decoded === "object"` y responder el
  mismo 400 que ya existe. Y el manejador de errores del router público nunca devuelve
  `err.message`. Se resuelve solo si HAL-07 pasa a JWT verificado.

### 26 · HAL-17 · Apagar los siete días abre el fichaje

- **Decisión previa.** Si el valor por defecto abierto es solo para «nadie configuró nada»,
  quitar la cláusula `hasAnyShifts` de `noConfig` (`createChecklog.controller.ts:214-217`).
  Recomendación: sí, porque quien apagó los siete días pidió justo lo contrario de lo que
  obtiene.

### 27 · HAL-22 · Sin horario, la app se rompe y el fichaje funciona

- **Decisión previa.** O el alta de la empresa deja `calendar/config` con un día abierto por
  defecto, o `GET /calendar` devuelve el mismo `buildOpenDefaultDay` que aplica el fichaje con
  `source:"default"` en vez de 404. Recomendación: la segunda, porque no inventa datos y deja
  el «sin configurar» visible.

### 28 · HAL-13 · Un plan retirado sigue en el catálogo

- **Resolución.** No devolver planes sin `stripePrice` (o con un `deprecated` explícito) desde
  `findPlansServices` y desde la lectura del panel; retirar la rama `freemium` de
  `PricingCard.controller.tsx:85` y el documento `service/checkinbiz/plan/freemium` de
  desarrollo, una vez confirmado que ninguna suscripción lo referencia (hoy ninguna).

### 29 · HAL-01 · Suscribir sin cliente de Stripe da un 500

- **Resolución.** `Subscribe.ts` lanza `Error` con JSON dentro; el manejador de `app.ts:35`
  lo convierte en 500. En el router de billing, capturar esos errores, leer el `code` y
  responder 409/412 con él. Alternativa mejor: crear el cliente de Stripe en `Subscribe` si no
  existe, que es lo que HAL-20 va a necesitar de todos modos.

### 30 · HAL-15 · Rechazar una corrección deja la hora rechazada

- **Decisión previa.** El fichaje queda en `failed`, así que el dato malo está en un registro
  invalidado; aun así conviene decidirlo. Si no es intencionado,
  `updateChecklog.controller.ts:271-293` restaura `previousDate` y `previousStatus` en todos
  los rechazos, no solo en los de fecha futura.

### 31 · HAL-03 · La sucursal nace con la geocerca desactivada

- **Decisión de producto.** Si la geocerca debe venir activa por defecto, el formulario
  (`branch/form/form.controller.tsx:64` y `:170`) deja de enviar el campo invertido. Se
  combina con HAL-24: hoy el panel manda el campo al revés y el backend lo rellena a `false`
  cuando falta, así que las dos cosas hay que cambiarlas juntas o el resultado vuelve a
  sorprender.

### 32 · HAL-04 · El empleado nace sin verificación de dispositivo

- **Decisión de producto.** Es medio por sí solo, pero mientras HAL-07 esté abierto el
  dispositivo de confianza es el único control que compensa una sesión fabricada, y con
  `enableA2F:false` por defecto ese control está apagado para casi todos. Cuando HAL-07 esté
  cerrado, vuelve a ser una preferencia.

---

## Bajo

### 33 · HAL-09 · La app compara con `invalid_checki`

- **Resolución.** Corregir la cadena en `error_parser.dart:91` y `exceptions.dart:202` de la
  app y publicar con la siguiente versión. No cambia nada en el servidor.

---

## Cerrados con residuo

- **HAL-33 · El espejo vacío.** Corregido apuntando la variable a staging. Queda: (1)
  `onChecklogSync` ya está portada a `services/firebase_sdk` y sin desplegar, y su `.env` lleva
  la variable buena; al desplegar hay que confirmar que el valor no vuelve atrás; (2) sigue sin
  reintentos, así que la propuesta de hacer del espejo un consumidor de la cola de eventos es
  la resolución de fondo; (3) los fichajes históricos de desarrollo siguen sin reinyectar.
- **HAL-31 · Función y contenedor procesando Stripe.** Cortado desactivando el endpoint.
  Queda: `processInvoices` desplegada en desarrollo, que se retira con HAL-05; y los dos
  documentos de factura con el objeto completo de Stripe que la función dejó en la entidad de
  prueba, que conviene borrar. FAC-07-09 vigila.
- **HAL-18 · Desarrollo sordo a Stripe.** El catálogo lo tiene abierto, pero ya está resuelto:
  HAL-19 midió el 2026-09-12 que el aviso previo llega a los 21 s y la factura a los 138 s,
  lo que solo es posible con el webhook apuntando a staging; y el segundo webhook, que HAL-18
  deja como «no establecido», HAL-31 lo desactivó ese mismo día. Falta marcarlo.
- **HAL-12 · Prueba de 45 días.** Corregido en el entorno. Queda el `?? 45` de
  `Subscribe.ts:9`: cambiarlo a 15, o mejor, no dar valor por defecto y fallar al arrancar si
  la variable no está. Y producción: confirmar el valor y decidir qué se hace con las
  suscripciones creadas con 45.

---

## Correcciones al propio catálogo

Cosas que el documento dice y que la relectura no sostiene, o que ya no son ciertas.

1. **HAL-25 atribuye un impacto que no existe.** El campo escrito en la ficha no lo lee la
   comprobación de dispositivo. Ver el punto 23. Un aviso que pide arreglar algo que no está
   roto enseña a ignorar la lista.
2. **HAL-18 está resuelto y sigue abierto.** Ver «Cerrados con residuo».
3. **La lista de «sospechas graves pendientes» está desactualizada.** Tres de sus seis
   entradas ya son hallazgos confirmados: la escalada de rol es HAL-21, el `isAdmin` en texto
   es HAL-16 y los informes sin filtrar por entidad son HAL-32. Y la primera —el estado del
   empleado— está medio respondida por la corrección CHK-08-23: el despedido no ficha, pero de
   rebote. Quedan de verdad pendientes: el estado del empleado en tareas, el borrado de
   empresa, la consulta de suscripciones y el doble correo de activación.
4. **La numeración va en dos sentidos.** HAL-01 a HAL-16 ascienden y de HAL-37 a HAL-17
   descienden. Para leerlo no importa, para citarlo sí: conviene fijar un sentido.

---

## Por dónde empezar

No conviene abordar los 33 uno a uno: se agrupan por fichero, y arreglar el grupo cuesta poco
más que arreglar uno.

1. **Permisos de entidad** (HAL-06, HAL-08, HAL-32, HAL-21, HAL-27). Un resolutor de actor en
   `shared`, montado en calendario, eventos e informes; el `actor` en las dos puertas de
   colaboradores; el `status` en `canWrite`. Y las reglas de Firestore en la misma entrega,
   o nada de esto cierra de verdad.
2. **Registro de jornada** (HAL-34, HAL-14, HAL-16, HAL-26, HAL-28, HAL-29). Tres ficheros:
   `sync.router.ts`, `updateChecklog.controller.ts` y `createChecklog.controller.ts` con su
   caso de uso. HAL-34 lleva además la reconstrucción de los informes diarios.
3. **Tareas** (HAL-35, HAL-36, HAL-37). Un solo controlador; ya estaba estimado en jornada y
   media o dos junto con la asignación por sucursal.
4. **Identidad de la app** (HAL-07, HAL-11, HAL-04). Token firmado con ventana de
   compatibilidad para las versiones instaladas; HAL-11 cae solo.
5. **Facturación** (HAL-19, HAL-20, HAL-05 con el residuo de HAL-31, HAL-12, HAL-01, HAL-13).
   HAL-20 cambia el alta de la suite, así que va acompañado del método de pago de prueba.
6. **Decisiones de producto antes de tocar código** (HAL-30, HAL-17, HAL-22, HAL-15, HAL-03).
   Cinco preguntas, cada una con recomendación arriba; ninguna bloquea a las anteriores.
7. **Limpieza de desarrollo** (HAL-02, residuos de HAL-33 y HAL-31) y la cadena de la app
   (HAL-09) cuando toque publicar.

Cada arreglo tiene su prueba ya escrita en la suite como fallo esperado: el criterio de
cierre es que esa prueba pase a verde sin tocarla, salvo quitarle el indulto.

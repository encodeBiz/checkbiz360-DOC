# 04 — Fases de implementación

Cada fase es desplegable por separado y no rompe lo que ya funciona. No hay migración de datos en ninguna: Firestore sigue siendo la fuente.

---

## Fase 0 — Promoción de lo común a `@encodebiz/shared`

**Objetivo:** que la Fase 1 no tenga que copiar nada. Y de paso, cerrar el duplicado que ya arrastran `tasks` y `documents`.

**Prerequisito:** ninguno.

Se sube a `packages/shared/src/checkbiz/`:

- `notifications/` — `CheckbizNotifier`, `CheckbizOperationals` (`CheckbizNotificationApp` y `CheckbizSentNotificationApp`), `messages`, `CheckbizMessageFactory`, `CheckbizPushMessageFactory`
- `repositories/FirestoreBranchRepository` — el completo, con `findById` y `findResponsibilities`
- `auth/canWrite`, `auth/validateToken` (`validateToken`, `validateTokenJWT`, `createCustomToken`), `auth/authError`
- `utils/getDistanceInMeters`

`tasks` y `documents` pasan a importar de `@encodebiz/shared` y **borran sus copias**. Los ficheros son idénticos byte a byte salvo la línea de import, así que el cambio es mecánico; el typecheck del monorepo es la red de seguridad.

Las entidades `Employee` y `Branch` que el repositorio compartido necesita tipar se suben en su versión superset (la de `tasks`: añade `status: "fired"`, `lastDayPlanned` y `metadata` libre respecto a la de `checkinbiz`, y es estructuralmente idéntica en todo lo demás). Cada servicio conserva sus entidades propias donde tenga campos que no comparte.

**Criterio de éxito:** `npm run typecheck` verde en todo el monorepo; `tasks` y `documents` arrancan y responden `/health`; cero ficheros duplicados de los listados arriba.

**Rollback:** revertir el commit. Ningún cambio de contrato, ningún cambio de comportamiento.

---

## Fase 1 — Port de las tres rutas

**Objetivo:** las tres rutas responden desde `checkinbiz:3002` con el contrato de [03_contratos-api.md](./03_contratos-api.md).

**Prerequisito:** Fase 0.

- `FirestoreChecklogRepository` portado completo (incluidos `findPendingByEmployeeBranchDate`, `findOverlapInRange`, `findOverdueOpenCheckins`, `findByCheckin`).
- Casos de uso `CreateChecklog`, `UpdateChecklog`, `RequestManualChecklogCreation` portados 1:1.
- Los tres controladores portados 1:1, con la firma de Express (`Request` de `express`, no de `firebase-functions`).
- `checklog.router.ts` con la auth resuelta por ruta, montado **antes** del `requireFirebaseAuth` global.
- Entidad `CheckLog` ampliada con los campos que el controlador ya escribe (`scheduleDay`, `weekPlan`, campos de solicitud manual). Es aditivo: `metadata` ya es extensible.
- Firebase **no se toca**: las tres funciones siguen exportadas y sirviendo el tráfico.

**Criterio de éxito:** typecheck verde; las tres rutas responden 401 sin token; cada fila de las tablas de error de [03](./03_contratos-api.md) reproducida contra el contenedor con el mismo HTTP y el mismo `code`; y verificados en Firestore los cuatro casos frágiles: `out_of_radius` persistido como `failed`, `deadline` presente en los checkin, `scheduleDay.weekPlan` completo, y `closed: true` en el checkin al hacer checkout.

**Rollback:** el servicio queda desplegado sin tráfico. Nadie lo apunta todavía.

---

## Fase 2 — Cutover del back office

**Objetivo:** que las correcciones de fichaje y las jornadas manuales del back office las sirva el servidor.

**Prerequisito:** Fase 1 validada.

- `NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_LOG` → `https://api.checkbiz360.com/api/v1/checkinbiz/checklogs/update`
- `NEXT_BACKEND_URI_CHECKINBIZ_REQUEST_MANUAL_CHECKLOG` → `https://api.checkbiz360.com/api/v1/checkinbiz/checklogs/manual-request`

Sin cambios de código en el front: `serverBackendProxy.ts` ya resuelve el destino por variable de entorno.

Empieza aquí el periodo de observación, y empieza por el back office a propósito: es el tráfico de menor volumen y el que tiene a un humano delante capaz de reportar una anomalía el mismo día.

**Criterio de éxito:** una corrección de fichaje completa de extremo a extremo (administrador propone → el empleado recibe la push → confirma) y una jornada manual en cada uno de sus dos modos, con los documentos correctos en Firestore y los triggers disparados.

**Rollback:** devolver las variables a la URL de Cloud Functions. Efecto inmediato, sin pérdida de datos.

---

## Fase 3 — Cutover de la app móvil

**Objetivo:** que el fichaje de la app lo sirva el servidor.

**Prerequisito:** Fase 2 estable.

- `AppConstants.createChecklogEndpoint` y `updateChecklogEndpoint` pasan a `https://api.checkbiz360.com/api/v1/checkinbiz/checklogs` y `…/checklogs/update`. Ver [05_conexion-de-clientes.md](./05_conexion-de-clientes.md).
- Release en stores.
- Las Cloud Functions originales **se quedan** sirviendo a las versiones antiguas.

**Criterio de éxito:** los cuatro tipos (`checkin`, `restin`, `restout`, `checkout`) funcionan contra el servidor; un dispositivo con 2FA activo ficha correctamente —confirma que el `user-agent` sigue siendo el mismo, que es de donde sale la huella del dispositivo—; y una corrección de fichaje se confirma desde la app, que usa el otro token.

**Rollback:** no lo hay rápido; la versión publicada ya apunta al servidor. De ahí el orden: el back office primero, y la app solo cuando el servidor lleve tiempo sirviendo tráfico real sin incidencias.

---

## Fase 4 *(futuro)* — Retirada

**Prerequisito:** Fase 3 estable y penetración de versiones de app por encima del umbral que se fije. Conviene fijarlo ahora: sin umbral, la retirada se aplaza sola.

- Eliminar los handlers originales de checklogs del codebase por defecto.
- Decidir qué hacer con `checkinbiz_create_log` en la allowlist del front, que hoy no tiene consumidor.
- Evaluar si conviene un alias REST (`PATCH /checklogs/:id`) ahora que el contrato ya no tiene que imitar a Firebase.

---

## Resumen

```
Fase 0: Promoción a shared    → una sola copia de notificaciones, repos y auth
Fase 1: Port                  → tres rutas en checkinbiz:3002, contrato idéntico
Fase 2: Cutover back office   → dos variables de entorno
Fase 3: Cutover app           → nuevas URLs + release en stores
Fase 4 (futuro): retirada
```

**Orden estricto:** no se hace cutover sin la verificación completa de la Fase 1. Y el back office (Fase 2) va antes que la app (Fase 3) porque su rollback es una variable de entorno; el de la app es otra publicación en stores.

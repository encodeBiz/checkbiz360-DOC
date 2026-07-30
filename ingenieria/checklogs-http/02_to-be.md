# 02 — Arquitectura objetivo (To-Be)

---

## 1. Topología

Nada nuevo que levantar: el servicio `checkinbiz` ya existe, ya está en el compose, ya tiene su `upstream` en nginx y ya sirve auth y calendario.

```
App móvil (nuevas URLs en AppConstants)
  └→ POST api.checkbiz360.com/api/v1/checkinbiz/checklogs
  └→ POST api.checkbiz360.com/api/v1/checkinbiz/checklogs/update

Back office
  └→ /api/proxy/checkinbiz_update_log             ─┐
  └→ /api/proxy/checkinbiz_request_manual_checklog ┴→ env var → api.checkbiz360.com/api/v1/checkinbiz/checklogs…

                                nginx → checkinbiz:3002
                                          └→ Firestore  (misma colección de siempre)
                                                └→ triggers de Firebase (intactos)
```

Sin capa intermedia: cada cliente pega al servidor ([ADR-002](./adr/ADR-002-clientes-apuntan-directo-sin-proxy.md)).

---

## 2. Rutas

Montadas en `services/checkinbiz/src/interfaces/http/checklog/checklog.router.ts`:

| Método | Ruta | Reemplaza a | Auth |
|---|---|---|---|
| `POST` | `/api/v1/checkinbiz/checklogs` | `createChecklog` | JWT de empleado, o ID token si `isAdmin: true` |
| `POST` | `/api/v1/checkinbiz/checklogs/update` | `updateChecklog` | Firebase ID token |
| `POST` | `/api/v1/checkinbiz/checklogs/manual-request` | `requestManualChecklog` | Firebase ID token |

Se conserva `POST` en las tres, y el cuerpo y las respuestas son idénticos a los de Firebase. `update` no es `PATCH /:id` a propósito: el `id` viaja en el body en el contrato actual y el objetivo de esta fase es que ningún cliente note el cambio salvo por el host. La forma REST canónica se puede introducir después como alias, cuando el contrato esté congelado.

El montaje va **antes** del `requireFirebaseAuth` global de `app.ts`, porque cada ruta resuelve su propia auth ([ADR-004](./adr/ADR-004-auth-por-ruta-no-global.md)).

---

## 3. Mapa de reutilización

La regla de este trabajo es que **no se escribe de nuevo nada que ya exista**. Lo que se toca y lo que no:

### Ya existe — se usa tal cual

| Pieza | Origen |
|---|---|
| `ResolveEffectiveDayUseCase`, `Calendar`, `CalendarRepository` | `@encodebiz/shared` |
| `FirestoreAppNotificationsRepository`, `NotificationService`, `PushProvider` | `@encodebiz/shared` |
| `FirestoreCalendarRepository`, `EmployeeFirestoreRepository` | `services/checkinbiz` |
| Entidades `CheckLog`, `Employee`, `Branch`; interfaz `ChecklogRepository` | `services/checkinbiz` |

### Se promueve a `@encodebiz/shared` (Fase 0)

Existe hoy por duplicado en `tasks` y `documents`. Se sube una sola copia y los tres servicios la importan:

| Pieza | Estado hoy |
|---|---|
| `CheckbizNotifier`, `CheckbizOperationals`, `messages`, factories de mensaje | Copia byte a byte en `tasks` y `documents` |
| `FirestoreBranchRepository` (con `findById` y `findResponsibilities`) | Copia byte a byte en `tasks` y `documents` |
| `canWrite` | Copia byte a byte en `tasks` |
| `validateToken`, `validateTokenJWT`, `AuthError`, `authErrorToResponse` | Copia byte a byte en `tasks` y `documents` |
| `getDistanceInMeters` | Solo en Firebase |

### Se porta nuevo (Fase 1)

| Pieza | Líneas aprox. |
|---|---|
| `FirestoreChecklogRepository` | 200 |
| `CreateChecklog` (máquina de estados del fichaje) | 86 |
| `UpdateChecklog` | 14 |
| `RequestManualChecklogCreation` | 332 |
| Los tres controladores | 436 + 239 + 132 |

Se porta **1:1**, sin refactor de comportamiento. Cualquier mejora que se quiera hacer se hace después del cutover, con el contrato ya verificado — mezclar port y refactor es la forma más fiable de no poder atribuir una regresión.

---

## 4. Auth

Tres modos, resueltos dentro de cada ruta:

```
POST /checklogs
  body.isAdmin === true  → validateToken(req)      → req.body.uid = decoded.uid
  resto                  → validateTokenJWT(req)   → req.body = {...body, ...payload}

POST /checklogs/update           → validateToken(req) → req.body.uid
POST /checklogs/manual-request   → validateToken(req) → req.body.uid
```

Es la traducción literal de lo que hoy hacen los ficheros `firebase-checkinbiz-http/*.ts`. El `JWT_2FA_SECRET` es el mismo secreto con el que `/auth/validate` —ya migrada— firma el `sessionToken`, así que la app no necesita reautenticarse.

---

## 5. Frontera con Firebase

El contenedor escribe en `entities/{entityId}/checklogs` con el Admin SDK, igual que hacía la Cloud Function. Para los triggers, la escritura es indistinguible: `onWhriteChecklog`, `onChecklogSync`, `onChecklogWebhook` y `sanitizer-checklogs` siguen funcionando sin cambios.

Dos consecuencias que hay que tener presentes:

1. **El campo `deadline` sigue siendo contractual.** `sanitizer-checklogs` cierra jornadas incompletas buscando checkins con `deadline` vencido. Si el port dejara de escribirlo, esas jornadas dejarían de cerrarse en silencio. Está en la lista de verificación de la Fase 1.
2. **La forma de `metadata` es contrato.** El pipeline de analítica lee `scheduleApplied.scheduleDay`, `weekPlan`, `realDateMarket` y `employeeResponsibility`. Se portan sin tocar ni un nombre de campo.

---

## 6. Cutover

**Back office — directo.** Se cambian dos variables de entorno a la URL nueva. Rollback: devolver el valor anterior.

```
NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_LOG=https://api.checkbiz360.com/api/v1/checkinbiz/checklogs/update
NEXT_BACKEND_URI_CHECKINBIZ_REQUEST_MANUAL_CHECKLOG=https://api.checkbiz360.com/api/v1/checkinbiz/checklogs/manual-request
```

**App móvil — nuevas URLs y release.** `AppConstants.createChecklogEndpoint` y `updateChecklogEndpoint` pasan a apuntar al servidor, y se publica versión. Las Cloud Functions originales se quedan sirviendo a las versiones antiguas hasta que la penetración permita retirarlas. Ver [ADR-002](./adr/ADR-002-clientes-apuntan-directo-sin-proxy.md) y [05_conexion-de-clientes.md](./05_conexion-de-clientes.md).

Va después del back office a propósito: el rollback del front es una variable de entorno, el de la app es otra publicación en stores.

---

## 7. Qué queda fuera, y por qué

- **`createChecklog` desde el back office.** El handler `checkinbiz_create_log` está en la allowlist del proxy del front pero ningún componente lo llama. Se deja registrado y apuntando a Firebase hasta confirmar que efectivamente está muerto; retirarlo es una decisión aparte.
- **Migración de checklogs a PostgreSQL.** El camino sigue siendo `trigger → sync → PostgreSQL`, sin cambios.
- **Unificación de las entidades `Employee`/`Branch` entre servicios.** La Fase 0 unifica los *repositorios*; las entidades se mantienen donde están salvo la parte que el repositorio compartido necesita tipar. El resto es deuda ya registrada.

# TDR-001 — Port de las tres rutas al servicio `checkinbiz`

**Fase:** 1
**Estado:** Diseño aprobado
**Depende de:** Fase 0 (promoción a `@encodebiz/shared`)

---

## 1. Estructura de destino

```
services/checkinbiz/src/
  domain/
    entities/CheckLog.ts                        ← ampliar (aditivo)
    interfaces/ChecklogRepository.ts            ← ampliar con los métodos que faltan
  infrastructure/
    FirestoreChecklogRepository.ts              ← nuevo
  application/
    use-cases/checklog/CreateChecklog.ts        ← nuevo
    use-cases/checklog/UpdateChecklog.ts        ← nuevo
    use-cases/checklog/RequestManualChecklogCreation.ts  ← nuevo
  interfaces/http/checklog/
    checklog.router.ts                          ← nuevo
    createChecklog.controller.ts                ← nuevo
    updateChecklog.controller.ts                ← nuevo
    requestManualChecklog.controller.ts         ← nuevo
```

De `@encodebiz/shared` se consumen (sin copiar): `ResolveEffectiveDayUseCase`, `FirestoreBranchRepository`, `canWrite`, `validateToken`, `validateTokenJWT`, `authErrorToResponse`, `getDistanceInMeters`, `CheckbizSentNotificationApp`, `FirestoreAppNotificationsRepository`.

De `services/checkinbiz` ya existentes: `EmployeeFirestoreRepository`, `FirestoreCalendarRepository`, entidades `Employee`, `Branch`, `CheckLog`.

---

## 2. Cambios en el dominio

### `CheckLog`

Los controladores ya escriben hoy más de lo que declara la interfaz actual del servicio. Como `metadata` tiene índice abierto (`[key: string]: any`), nada falla en tiempo de ejecución, pero el tipo miente sobre lo que hay. Se amplía de forma **aditiva**:

- `metadata.scheduleApplied.source`: la unión pasa de `"workSchedule" | "default"` a incluir `"entity" | "branch" | "employee"` — son los valores que devuelve `resolveDay.sources.schedule`.
- `metadata.scheduleApplied.shifts` y `metadata.scheduleApplied.scheduleDay` (fecha, `weekday`, `isWorkingDay`, `isHoliday`, `disabled`, `shifts`, `plannedMinutes`, `breakMinutes`, `weekPlan`, `weekPlannedMinutes`).
- Campos de la solicitud manual: `manualRequest`, `requestedByUid`, `reason`, `geoSource`, `timeSource`, `autofilledFields`.

Ningún campo existente cambia de nombre ni de tipo.

### `ChecklogRepository`

La interfaz del servicio declara hoy siete métodos; el repositorio de Firebase implementa once. Se añaden los que faltan y se corrigen dos firmas que no coinciden con el uso real:

- `findAllCheckLog` con `limit`, `filters` y `orderBy` (la firma actual solo acepta `employeeId` y `entityId`).
- `findOverdueOpenCheckins(start, end, limit?, cursor?)` devolviendo también `lastDoc` — la firma actual declara un solo parámetro de fecha.
- `createWithId`, `findPendingByEmployeeBranchDate`, `findOverlapInRange`.

---

## 3. Traducción de Firebase a Express

El port es mecánico salvo en cuatro puntos:

| En Firebase | En el servicio |
|---|---|
| `Request` de `firebase-functions/v2/https` | `Request` de `express` |
| `res` sin tipar | `Response` de `express` |
| `logger.warn` de `firebase-functions` | `console.warn` (el resto del servicio ya lo usa) |
| Auth en el fichero envoltorio (`firebase-checkinbiz-http/*.ts`) | Auth en el router, por ruta ([ADR-004](../adr/ADR-004-auth-por-ruta-no-global.md)) |

`getFirestore()` se usa igual: `@encodebiz/shared` inicializa el Admin SDK en el import de cabecera de `app.ts`, antes de que se carguen los repositorios. Esa cabecera ya está y hay que no romperla — los repositorios llaman a `getFirestore()` en tiempo de carga del módulo.

`RequestManualChecklogCreation` usa `getFirestore()` directamente para el `batch` y para consultar el checkout existente. Se porta tal cual: envolverlo en el repositorio sería refactor, y esta fase no refactoriza.

---

## 4. El router

```ts
export const checklogRouter = Router();

// POST /checklogs — app móvil (JWT de empleado) o administrador (ID token + isAdmin)
checklogRouter.post("/", async (req, res) => { … });

// POST /checklogs/update — corrección de fichaje (ID token)
checklogRouter.post("/update", async (req, res) => { … });

// POST /checklogs/manual-request — jornada manual (ID token + responsabilidad ≥ 2)
checklogRouter.post("/manual-request", async (req, res) => { … });
```

Montado en `app.ts` **antes** de la línea de `requireFirebaseAuth`:

```ts
app.use("/api/v1/checkinbiz/checklogs", checklogRouter);
```

El ping de calentamiento (`{_warmup: true}`) se atiende en la ruta de creación igual que hoy, respondiendo `200` sin procesar nada. Lo envía `criticalHandler` al terminar el arranque de la app; se conserva por compatibilidad, aunque contra el contenedor deje de tener sentido —no hay cold start que calentar— y acabe retirándose cuando el arranque de la app deje de emitirlo.

---

## 5. Contrato con lo reactivo

Dos cosas que el port tiene que escribir sí o sí, y que ningún test de la propia ruta detectaría si faltan:

1. **`deadline` en los checkin** — `fin de turno + 6 h`, en UTC. Lo consulta `sanitizer-checklogs` para cerrar jornadas incompletas. Si falta, las jornadas dejan de cerrarse y nadie se entera hasta que el informe mensual sale mal.
2. **`metadata` con la forma exacta** — `onChecklogSync` proyecta `scheduleApplied`, `realDateMarket`, `etz` y `employeeResponsibility` hacia PostgreSQL (`ChecklogSyncPayload` en `@encodebiz/shared`). Un campo renombrado se convierte en un `null` silencioso en el warehouse.

Y una que es fácil perder por ser un efecto lateral: **el checkout marca `closed: true` en su checkin asociado** con una segunda escritura, después de crear el propio checkout.

---

## 6. Riesgos

| Riesgo | Mitigación |
|---|---|
| El fichaje fuera de radio deja de persistirse | Es una escritura *antes* del `return 400`; se verifica explícitamente en Firestore, no solo por la respuesta HTTP |
| Deriva de zona horaria al portar `luxon` | Misma versión de `luxon` (`^3.7.2`, ya en el `package.json` del servicio) y prueba con una entidad en zona distinta a la del servidor |
| El `user-agent` cambia al apuntar a otra URL y rompe el dispositivo de confianza | La huella es `base64(user-agent)` y se compara con `trustedDevicesId`: si el cliente HTTP la altera, todo dispositivo con 2FA falla con `auth/untrusted_device`. Se verifica en la Fase 3 con un dispositivo real antes de publicar |
| `FieldValue.delete()` y `FieldValue.arrayUnion()` en el update | Se importan de `firebase-admin/firestore` igual que en Firebase; el `set(..., {merge: true})` del repositorio los respeta |
| Divergencia entre la copia de Firebase y la del servicio durante la convivencia | La convivencia es corta por diseño: Fase 2 y 3 seguidas, y Fase 4 retira el original |

---

## 7. Deuda que se acepta

- **`CheckLog` duplicado** entre Firebase y el servicio mientras dure la convivencia.
- **`message: "Checklog created"` en la respuesta de actualización** — error de copia del handler original que se conserva para no cambiar contrato. Corregirlo después del cutover, comprobando antes que ningún cliente lo compara.
- **El typo `employee/not_resposibility`** — mismo criterio.

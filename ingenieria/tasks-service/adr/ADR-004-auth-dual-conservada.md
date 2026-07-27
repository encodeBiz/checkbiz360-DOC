# ADR-004 — Conservar la autenticación dual (Firebase ID token + staff JWT)

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

`resolveTaskActor` (en `task.helpers.ts`) resuelve el actor de cada petición con **dos vías**:

1. **Firebase ID token** (`validateToken`) — usuario de back office. Se comprueba `canWrite(uid, entityId)` (permiso de escritura sobre la entidad) y se cargan las responsabilidades del empleado vinculado al `uid`.
2. **Staff JWT** (`validateTokenJWT` / `validateTokenStaff`) — empleado desde la app móvil, que no tiene cuenta de usuario Firebase. Se valida el JWT propio y se resuelve el empleado por `employeeId`.

Sobre el actor resuelto se computa un **nivel de responsabilidad** (`worker < supervisor < manager < owner`) que gobierna cada operación (crear, asignar, validar, valorar, ver).

El servicio destino `encodebiz-api` ya expone `requireFirebaseAuth` en `@encodebiz/shared`, pero ese middleware solo cubre la vía 1.

---

## Decisión

Se **conserva la autenticación dual portando `resolveTaskActor` y sus dos ramas 1:1**, sin cambiar el comportamiento vigente en producción. Se portan tal cual `validateToken` (ID token de Firebase), `validateTokenJWT` (staff JWT) y `canWrite`, junto con toda la resolución de nivel de responsabilidad. El único cambio respecto al origen es de tipos (`Request` de `firebase-functions/https` → `express`), sin efecto en runtime.

**No se usa `requireFirebaseAuth` de `@encodebiz/shared`** para las rutas de tarea, aunque exista: ese middleware verifica con `verifyIdToken(token, true)` (`checkRevoked: true`), más estricto que el `validateToken` original (`verifyIdToken(idToken)` sin `checkRevoked`). Adoptarlo cambiaría el criterio de aceptación de tokens en producción, donde app y back office ya están operando. Se prioriza la paridad exacta.

---

## Justificación

**Las dos vías son requisitos funcionales, no un detalle de infraestructura.** El back office autentica con Firebase Auth; la app móvil del empleado autentica con un JWT propio. Quedarse solo con `requireFirebaseAuth` dejaría fuera a la app móvil, que es justamente uno de los dos consumidores del servicio.

**El nivel de responsabilidad es dominio de tareas, no auth genérica.** `canManageTask`, `canValidateOrRejectTask`, `canRateTask`, `canViewTask`, etc. dependen del nivel resuelto y de la `TaskConfig`. Esta lógica pertenece al módulo de tareas y viaja con él.

**Paridad exacta con producción.** App y front ya están en producción contra `tasksHandler`. Un port fiel de `validateToken`/`validateTokenJWT`/`canWrite` garantiza que ningún token que hoy se acepta deje de aceptarse (ni al revés). Por eso se descarta reutilizar `requireFirebaseAuth` de shared (ver Decisión).

---

## Consecuencias

**Positivas:**
- App móvil y back office siguen autenticando igual que hoy: cero cambios de cliente en auth.
- La matriz de permisos por nivel se preserva exactamente (mismas funciones `can*`).

**Negativas / Compromisos aceptados:**
- El servicio `tasks` arrastra `canWrite`, `validateTokenStaff` y el acceso a responsabilidades de empleado desde `core/*` del SaaS. Es una cola de dependencias acotada y pequeña (ver [TDR-002](../tdr/TDR-002-resolucion-actor-y-permisos.md)).
- El secreto de firma del staff JWT debe estar disponible como variable de entorno en el servicio `tasks`, además de en Firebase.

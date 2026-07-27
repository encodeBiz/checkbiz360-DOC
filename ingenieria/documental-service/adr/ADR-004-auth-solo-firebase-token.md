# ADR-004 — Auth solo Firebase ID token (sin staff JWT)

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El port de tareas conservó una **auth dual** (Firebase ID token para el back office + staff JWT para la app móvil del empleado), porque la app opera tareas con un token propio de staff. Al portar documental hay que decidir qué vías de autenticación soporta.

El código origen del módulo documental usa **una sola vía**: `validateToken` (Firebase `verifyIdToken`) en `document.helpers.ts` / `resolveDocumentActor`. No hay ninguna rama de staff JWT.

---

## Decisión

**Auth solo Firebase ID token**, portada 1:1. No se añade staff JWT.

El actor se resuelve con `DocumentPermissionService.resolveActor(uid, entityId)`, que a partir del `uid` del token lee:
- `user_entity_roles/{uid}_{entityId}` → owner/admin (global).
- el empleado activo por `uid` dentro de la entidad.
- sus `employee_responsibilities` activas por sucursal (rol + nivel).

---

## Justificación

- **Fidelidad al comportamiento actual.** El módulo en Firebase nunca aceptó staff JWT; añadirlo cambiaría la superficie de auth y el modelo de amenaza sin que ningún cliente lo pida.
- **Documental es superficie de back-office / usuario autenticado.** Los documentos (nóminas, contratos, avisos, políticas) se gestionan y consultan con la identidad Firebase del usuario; la resolución de permisos ya cubre al empleado a través de su `uid`.
- **Menos superficie, menos riesgo.** Una sola vía de auth es más simple de portar y de razonar que la dual de tasks.
- No se usa `requireFirebaseAuth` de `@encodebiz/shared`: se porta `validateToken` tal cual (`verifyIdToken` sin `checkRevoked`) para no alterar el comportamiento en producción (mismo criterio que tasks).

---

## Consecuencias

**Positivas:**
- Port de auth trivial: una función (`validateToken`) + el `resolveActor` del `DocumentPermissionService`.
- El contrato de auth es idéntico al de Firebase; los clientes actuales no cambian nada salvo la URL base.

**Negativas / Compromisos aceptados:**
- Si en el futuro la app del empleado necesitara consultar documentos con su staff JWT (sin sesión Firebase), habría que añadir una segunda vía —igual que tasks—; hoy no es un requisito.

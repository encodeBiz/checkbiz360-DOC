# ADR-005 — Reutilizar el framework de notificaciones del port de tasks

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El módulo documental envía notificaciones push + in-app en dos momentos: al subir un documento (`doc_uploaded`) y cuando el documento requiere confirmación de lectura (`doc_ack_required`). En Firebase esto lo hace `DocumentNotificationService` apoyándose en `CheckbizSentNotificationApp.sendNotifications(...)` y en la tabla de plantillas `messages`.

El port de tareas ya extrajo el núcleo genérico de notificaciones a `@encodebiz/shared` (`NotificationService`, `PushProvider`, `FirestoreAppNotificationsRepository`) y copió a `services/tasks` el scaffolding específico de Checkbiz (`CheckbizNotifier`, `CheckbizSentNotificationApp`, `CheckbizPushMessageFactory`, `messages`). **Ese `messages.ts` ya incluye las plantillas `doc_uploaded` y `doc_ack_required`.**

**Opción A — Copia local en `services/documents`** del scaffolding de notificaciones (como hizo tasks), añadiendo solo `DocumentNotificationService`.
**Opción B — Promover** `CheckbizNotifier`/`CheckbizSentNotificationApp`/`messages` a `@encodebiz/shared` para que tasks y documents lo compartan.

---

## Decisión

**Opción A: copia local del scaffolding de notificaciones en `services/documents`**, reutilizando `@encodebiz/shared` solo para el núcleo genérico ya compartido. Se añade únicamente `DocumentNotificationService.ts`.

---

## Justificación

- **Bajo riesgo.** No se toca el servicio `tasks`, que está en producción. Promover código compartido implicaría refactorizar tasks y revalidarlo.
- **Consistencia con el precedente.** tasks ya optó por copia local de estos primitivos (mientras que sí compartió el núcleo genérico). Documental sigue el mismo patrón.
- **El terreno ya está preparado.** El `messages.ts` de tasks trae las claves documentales; copiarlo es inmediato y `DocumentNotificationService` encaja sin adaptaciones sobre `CheckbizSentNotificationApp`.

---

## Consecuencias

**Positivas:**
- Port de notificaciones casi mecánico: copiar scaffolding + un servicio.
- El servicio `tasks` no se toca.

**Negativas / Compromisos aceptados:**
- Duplicación de `CheckbizNotifier`/`CheckbizSentNotificationApp`/`messages` entre `tasks` y `documents`. Se registra como deuda: la unificación de estos primitivos en `@encodebiz/shared` (Opción B) queda como trabajo futuro, no del día 1.
- `entity_employees` (ack a nivel entidad) se mantiene **diferido**: `DocumentNotificationService` no resuelve destinatarios entity-wide (falta un query paginado), y el alta/actualización bloquean ese modo en V1. Ver [TDR-004](../tdr/TDR-004-notificaciones-documentales.md).

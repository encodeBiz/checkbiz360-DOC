# ADR-005 — Extraer el framework de notificaciones a `@encodebiz/shared`

**Fecha:** 2026-07-26
**Estado:** Aceptado — implementado en Fase 1
**Decisionario:** Jose Acevedo

---

## Contexto

Al portar el módulo `task` se descubrió que los controladores HTTP disparan **notificaciones push in-line** (fire-and-forget) en cada evento del ciclo de vida de la tarea: creada, asignada, iniciada, completada, validada, rechazada, evidencia subida, trabajador valorado.

```typescript
taskNotificationService.notifyTaskCreated(task).catch(console.error);
```

Esto arrastra un subsistema:
- **Fábricas checkbiz/tarea:** `TaskNotificationService`, `CheckbizNotifier`, `CheckbizOperationals`, `TaskRecipientResolver`, `CheckbizMessageFactory`, `CheckbizPushMessageFactory`, `messages.ts`.
- **Framework de plataforma** `core/notifications/`: `NotificationService`, `NotificationProviderFactory`, `PushProvider` (FCM vía `admin.messaging`), `FirestoreAppNotificationsRepository` (colección `in_app_notifications`).

Dato clave verificado: **ningún trigger de Firebase cubre estas notificaciones**. Los triggers de tarea existentes (`onWriteTaskForPattern`, `onWriteTaskRating`, `onTaskRatingSync`) son de sync analítico. Solo el aviso de "inicio tardío" es de schedule (`taskStartNotificationWorker`) y se queda en Firebase ([ADR-002](./ADR-002-solo-http-lo-reactivo-en-firebase.md)). Por tanto, **abstraer a no-op perdería notificaciones reales** — no era opción.

Se evaluaron tres caminos: (A) portar la rama push del subsistema dentro del servicio `tasks`; (B) extraer el framework a `@encodebiz/shared`; (C) mover las notificaciones a un trigger nuevo en Firebase.

---

## Decisión

Se elige **Opción B: extraer el framework genérico de notificaciones a `@encodebiz/shared`**.

- **A shared (genérico, reutilizable):** `Notification` (tipos + `AppNotification`), `NotificationService`, `NotificationProviderFactory`, `PushProvider`, `FirestoreAppNotificationsRepository`. Se exporta desde `@encodebiz/shared`.
- **En el servicio `tasks` (específico de checkbiz/tarea):** `TaskNotificationService`, `CheckbizNotifier`, `CheckbizOperationals`, `TaskRecipientResolver`, `CheckbizMessageFactory`, `CheckbizPushMessageFactory`, `messages.ts` — consumen el framework desde shared.

---

## Justificación

**Es el hogar correcto.** El framework de notificaciones (push/in-app) es infraestructura de plataforma, no de tareas. Ponerlo en `@encodebiz/shared` lo hace reutilizable por cualquier servicio (documentos, planificador, etc.) sin duplicar, y evita hinchar el microservicio `tasks` con infra transversal (coherente con [ADR-001](./ADR-001-microservicio-tasks-dedicado.md)).

**El coste real fue bajo.** Twilio y WhatsApp ya estaban deshabilitados en `NotificationProviderFactory` (lanzan error). Solo `PushProvider` está activo, así que la extracción se limitó a push + in-app: 5 ficheros, sin dependencias npm nuevas (`admin.messaging` ya viene con `firebase-admin`).

**Se preserva la conducta exacta.** Las fábricas de mensajes checkbiz se mantienen idénticas; solo cambia de dónde importan el framework. Las notificaciones del ciclo de vida siguen disparándose igual que en Firebase.

**Desacople limpio de dominio.** El repo de `in_app_notifications` dependía del tipo `CheckbizNotifications` del dominio checkinbiz. Se promovió ese shape a shared como `AppNotification` (genérico), rompiendo el acoplamiento inverso (shared ya no importa nada de checkinbiz).

---

## Consecuencias

**Positivas:**
- `@encodebiz/shared` gana un módulo de notificaciones reutilizable (`NotificationService`, `PushProvider`, `FirestoreAppNotificationsRepository`, `AppNotification`).
- El servicio `tasks` queda lean: solo trae las fábricas de mensajes específicas de tarea.
- Base lista para migrar en el futuro las notificaciones de otros dominios (documentos, planificador) sin reescribir el transporte.

**Negativas / Compromisos aceptados:**
- `@encodebiz/shared` incorpora dependencia conceptual de FCM (`admin.messaging`). Es aceptable: shared ya inicializa el Admin SDK.
- Twilio/WhatsApp quedan fuera de shared por ahora (estaban deshabilitados). Reactivarlos será añadir sus providers al framework compartido, no reescribirlo.
- Las fábricas `Checkbiz*` viven en `tasks` aunque son de producto checkinbiz; si otro servicio checkinbiz las necesita, se promoverán a un paquete de producto. Deuda registrada.

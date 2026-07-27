# TDR-004 — Notificaciones documentales (`doc_uploaded` / `doc_ack_required`)

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, pendiente implementación (Fase 2)
**Componente:** `services/documents` — `DocumentNotificationService`

---

## Problema

El alta de un documento dispara notificaciones push + in-app. Hay que portar
`DocumentNotificationService` reutilizando el scaffolding de notificaciones ya presente en
`services/tasks` (ver [ADR-005](../adr/ADR-005-notificaciones-reutilizadas-de-shared.md)), sin
cambiar a quién se notifica ni con qué contenido.

## Dependencias

- `CheckbizSentNotificationApp.sendNotifications(employees, body, "Checkbiz360", message, {data})`
  — copiado de `tasks`; envía push (FCM, si hay `token_devices`) + crea la notificación in-app.
- Plantillas `messages` — el `messages.ts` de tasks **ya incluye** `doc_uploaded` y `doc_ack_required`.
- `FirestoreBranchRepository` / `EmployeeFirestoreRepository` (con proyección `"token_devices"`).

## `doc_uploaded` (alta)

- **scope=employee**: notifica al empleado destinatario — **salvo** que el documento requiera ack (en ese caso lo cubre `doc_ack_required`, para no duplicar).
- **scope=branch**: notifica a los empleados de la sucursal cuyo rol de responsabilidad está en `visibleToRoles` (el owner operativo siempre incluido).
- **scope=entity**: **omitido en V1** (no hay resolvedor de destinatarios entity-wide eficiente).

## `doc_ack_required` (cuando `requiresAcknowledgement`)

- **single_employee**: notifica al empleado (`doc.employeeId`).
- **branch_employees**: notifica a los empleados de la sucursal por `visibleToRoles` (owner operativo incluido).
- **entity_employees**: **diferido a V2** — requiere un query paginado de empleados de la entidad, no disponible. El alta/actualización bloquean este modo con `400` (ver [03_contratos-api.md](../03_contratos-api.md)).

## Privacidad del contenido

`safeTitle(doc)`: para tipos **RRHH** (`payroll`, `contract`) y **disciplinarios**
(`warning`, `attention_call`) el título se envía **vacío**, para que la vista previa en la
pantalla de bloqueo no revele información sensible. La `data` del push marca `private: "true"`,
`module: "checkbiz_documents"`, `screen: "document_detail"`, con `entityId`/`branchId`/`documentId`.

## Semántica respecto a la respuesta HTTP

En el alta, el controlador **espera** (`Promise.allSettled`) a `notifyDocumentUploaded` y
`notifyAcknowledgementRequired` antes de responder `201` — fallos individuales se loguean pero
no bloquean la respuesta. Se preserva ese `await` en el port (era necesario en CF porque
`fire-and-forget` no es seguro tras `res.json()`; en el servidor persistente se mantiene por
fidelidad de contrato, con la puerta abierta a relajarlo en el futuro — ver
[ADR-002](../adr/ADR-002-solo-http-lo-reactivo-en-firebase.md)).

## Criterio de aceptación

- Alta scope=branch con `visibleToRoles=["manager"]` → los managers de la sucursal reciben `doc_uploaded` (push si tienen device + in-app); un worker de la sucursal no.
- Alta scope=employee con `requiresAcknowledgement=true` → el empleado recibe **solo** `doc_ack_required` (no `doc_uploaded`).
- Alta de un `payroll` → el push no revela el título (`safeTitle` vacío).

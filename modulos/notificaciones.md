# Módulo Notificaciones — Push + In-App v3

## 1. Resumen

El sistema de notificaciones v3 opera en dos canales:
- **Push (FCM)**: notificaciones al dispositivo via Firebase Cloud Messaging
- **In-App**: mensajes persistidos en Firestore, visibles dentro de la app

## 2. Infraestructura

### Backend

- `CheckbizNotifier` — orquestador principal
- `CheckbizPushMessageFactory` — construye payloads FCM por tipo y idioma
- `NotificationService` + `PushProvider` — envío FCM
- `TaskNotificationService` + `TaskRecipientResolver` — específicos del módulo task
- `messages.ts` — catálogo de mensajes multiidioma

### Colecciones Firestore

```
notifications_v3/system/
├── campaign_definitions/{campaignId}
├── campaign_runs/{runId}
├── notification_jobs/{jobId}
├── in_app_messages/{messageId}
└── user_message_state/{stateId}
```

## 3. Notificaciones Push — Comportamiento General

### Reglas

- Las notificaciones son fire-and-forget: **nunca bloquear el flujo principal**
- El idioma del empleado receptor (`Employee.language ?? "es"`) determina el mensaje
- Si hay destinatarios con distintos idiomas, enviar por agrupaciones o individualmente
- Firebase App Check activo en producción

### Payload mínimo para navegación en app

```typescript
{
  data: {
    module: "checkbiz" | "checkbiz_tasks",
    type: string,
    entityId: string,
    branchId: string,
    taskId?: string,
    issueId?: string,
    screen: string,
    action: string,
  }
}
```

Sin `entityId`, `branchId`, `screen` y `action`, la app no puede navegar al recurso específico.

## 4. Tipos de Notificación

### CheckLog / Asistencia

| Tipo | Destinatario | Descripción |
|---|---|---|
| `update_checklog_pending` | Empleado propietario | Validación de checklog pendiente (solicitud manual o edición) |
| `distance_violation` | Supervisores level 2 del branch | Fichaje fuera del radio permitido |
| `ratio_anomaly` | Supervisores level 2 del branch | Anomalía en ratio de asistencia |
| `pattern_mismatch_checkin` | Supervisores level 2 del branch | Checkin fuera del patrón habitual |
| `pattern_mismatch_checkout` | Supervisores level 2 del branch | Checkout fuera del patrón habitual |
| `out_of_day_window` | Supervisores level 2 del branch | Fichaje fuera de la ventana del día |

Payload de `update_checklog_pending` incluye siempre: `updateId`, `id` (docId), `entityId`, `employeeId`, `requestAction: true`.

### Task

| Tipo | Destinatario |
|---|---|
| `task_created` | Workers asignados |
| `task_assigned` | Worker recién asignado |
| `task_updated` | Workers asignados |
| `task_started` | Equipo asignado |
| `task_completed` | Equipo asignado |
| `task_validated` | Workers asignados |
| `task_rejected` | Workers asignados |
| `task_due_soon` | Equipo asignado |
| `task_overdue` | Equipo asignado |
| `task_resource_uploaded` | Equipo asignado |
| `task_worker_rated` | Worker valorado |

### Issues

| Tipo | Destinatario | Notas |
|---|---|---|
| `issueReceived` | Worker específico o rol de gestión | Requiere `issueId` en payload (pendiente de añadir en backend) |
| `issueResponseReceived` | Quien abrió el issue | Ídem |

## 5. Bug Conocido — Issues (`onCreateIssues`)

### Problema actual

El trigger `onCreateIssues` usa `findResponsibilities(branchId, responsibility == "worker")` ignorando `employeeId`. Resultado: una jornada incompleta de un empleado envía push a **todos los workers** de la sucursal.

### Comportamiento esperado

```
toRole === "worker" && employeeId existe
  → notificar solo a ese empleado (1 push + 1 in-app)

toRole es rol de gestión
  → buscar por responsabilidad en el branch
```

### Estado

Propuesta técnica documentada, pendiente de implementación. Ver `encodeBiz-SAAS/DOCUMENTOS/notifications-refactor/`.

## 6. Notificaciones In-App

### Estructura del documento

```typescript
{
  id: string;
  uid: string;              // UID Firebase Auth del destinatario
  employeeId: string;
  entityId: string;
  module: "checkbiz" | "checkbiz_tasks";
  type: string;
  title: string;
  body: string;
  isRead: boolean;
  createdAt: Timestamp;
  severity: "warning" | "info";
  resp_level: number[];     // [] = privada — no usar para filtrar en cliente
  data: {
    module: string;
    type: string;
    entityId: string;
    branchId: string;
    taskId?: string;
    issueId?: string;
    screen: string;
    action: string;
  } | null;
}
```

### Query para el cliente

```
Colección : in_app_notifications
Filtro    : uid == currentEmployee.uid
Orden     : createdAt DESC
Límite    : 20 (paginable por cursor)
Badge     : + isRead == false
```

No filtrar por `resp_level` en el cliente — es metadata de backend. Acceso controlado por `uid`.

### Decisión pendiente

La query puede implementarse directamente en el cliente (Firestore SDK) o a través de un endpoint backend que autentique el `uid`. Si se hace en cliente, las Firestore Security Rules son la única barrera real.

## 7. Comportamiento en App Móvil

| Escenario | Comportamiento |
|---|---|
| Push en foreground | Mostrar banner/snackbar in-app. No delegar al SO |
| Push en background | SO lo muestra. Al tocar, navegar por `data.screen` + ids |
| Sin ids de navegación | Navegar al listado general. No fallar silenciosamente |
| Marcar como leída | Al abrir el detalle, no al listar |
| Deduplicar | Por `id` del documento |
| Stream vs polling | `onSnapshot` con límite. Desuscribirse al salir de pantalla |

## 8. Bug `double optional chaining` (pendiente)

En `CheckbizSentNotificationApp.sendNotifications`:

```typescript
// Incorrecto — lanza si data existe pero data.data es undefined
type: data?.data.type ?? message ?? "informative"

// Correcto
type: data?.data?.type ?? message ?? "informative"
```

Verificar y corregir antes de implementar el fix de issues.

# Arquitectura del Sistema EncodeBiz

## 1. Visión General

EncodeBiz es una plataforma SaaS de gestión operativa para empresas con empleados en sucursales. El producto principal es **CheckBiz**, que gestiona asistencia, tareas, documentos y analítica operativa.

```
┌──────────────────────────────────────────────────────────────┐
│                         CLIENTES                             │
│                                                              │
│  ┌──────────────────┐        ┌─────────────────────┐        │
│  │  encodebiz-front │        │   CheckBiz360        │        │
│  │  (Backoffice)    │        │   (App móvil)        │        │
│  │  Next.js 14      │        │   Flutter 3.35.6     │        │
│  └────────┬─────────┘        └──────────┬──────────┘        │
└───────────┼────────────────────────────┼───────────────────-─┘
            │  HTTPS / Bearer Token       │
            ▼                             ▼
┌───────────────────────────────────────────────────────────────┐
│              encodeBiz-SAAS (Firebase — Backend Operacional)  │
│                                                               │
│  Firebase Functions v2 — TypeScript — Node 22                 │
│  Región: us-central1  │  Proyecto prod: encodebiz-services    │
│                                                               │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ HTTP Functions│  │Firestore       │  │Scheduled Functions│  │
│  │ (CRUD, auth) │  │Triggers        │  │(planifiers, crons) │  │
│  └──────────────┘  └────────────────┘  └──────────────────┘  │
└────────────────────────┬──────────────────────────────────────┘
                         │  S2S (X-Encodebiz-Key)  │
                         ▼                          │
┌──────────────────────────────────────────────────────────────┐
│          encodebiz-api (V2 API — Microservicios)             │
│                                                              │
│  npm workspaces + Docker Compose + nginx                     │
│                                                              │
│  ┌────────────┐  ┌──────────────┐  ┌──────┐  ┌──────────┐  │
│  │  merlin    │  │  checkinbiz  │  │ sync │  │analytics │  │
│  │  :3001     │  │  :3002       │  │ :3003│  │  :3004   │  │
│  │  IA / OpenAI│  │  Heurística  │  │Firebase│ │Histórico │  │
│  └────────────┘  └──────────────┘  └──────┘  └──────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Infraestructura                                 │
│                                                              │
│  Google Firebase/GCP                   PostgreSQL 16         │
│  Firestore │ Storage │ FCM │ Auth       (datos analíticos)    │
└──────────────────────────────────────────────────────────────┘
```

## 2. Stack Técnico por Capa

### Backend — encodeBiz-SAAS

| Componente | Tecnología |
|---|---|
| Runtime | Node 22, TypeScript strict |
| Framework Functions | Firebase Functions v2 (`firebase-functions/v2`) |
| Admin SDK | firebase-admin v12 |
| ORM/DB | Firestore (Admin SDK directo) |
| Date/Time | Luxon |
| Notificaciones push | FCM via firebase-admin/messaging |
| Storage | Firebase Storage |
| Email | Nodemailer (lazy import) |
| PDF | pdfkit (lazy import) |
| SMS | Twilio (lazy import) |
| Imagen | sharp (lazy import) |
| Arquitectura | DDD — domain / application / infrastructure / interfaces |

### Backoffice — encodebiz-front-saas

| Componente | Tecnología |
|---|---|
| Framework | Next.js 14 (App Router) |
| UI | Material UI v5 |
| State | React hooks + Context |
| Forms | Formik |
| HTTP | Fetch nativo + custom hooks |
| i18n | next-intl |
| Auth | Firebase Auth (session tokens) |
| Linting | ESLint + Prettier |

### App Móvil — CheckBiz360

| Componente | Tecnología |
|---|---|
| Framework | Flutter 3.35.6 (FVM) |
| State | Riverpod 2.x |
| HTTP | Dio + interceptores |
| DB local | Hive (cache offline) |
| Push | Firebase Messaging |
| GPS | geolocator + connectivity_plus |
| DI | injection_container.dart (Riverpod providers) |
| Auth | Firebase Auth → sessionToken → Bearer en API |

## 3. Patrón de Comunicación

### Escrituras (mutaciones)
Siempre via HTTP API (Firebase Functions). Nunca directamente a Firestore desde el cliente.

```
Cliente → POST/PATCH/DELETE → Cloud Function → Firestore
```

### Lecturas
- **Backoffice**: HTTP GET (Cloud Functions)
- **App móvil**: Firestore SDK directo (streams en tiempo real) + HTTP para datos agregados

```
App → Firestore listener → datos en tiempo real
App → GET Cloud Function → datos paginados/agregados
```

## 4. Autenticación

```
1. Usuario hace login → Firebase Auth → idToken (JWT)
2. App llama POST /auth/loginEmployee con idToken
3. Backend valida, genera sessionToken (JWT propio)
4. Todas las llamadas siguientes: Authorization: Bearer {sessionToken}
5. Middleware validateToken() en cada función HTTP decodifica y setea req.body.uid
```

## 5. Estructura de Firestore

```
entities/{entityId}/
├── employees/{employeeId}
├── branches/{branchId}
├── checklogs/{checklogId}
├── tasks/{taskId}/
│   ├── assignments/{assignmentId}
│   ├── notes/{noteId}
│   ├── resources/{resourceId}
│   ├── ratings/{ratingId}
│   ├── validations/{validationId}
│   └── activity/{activityId}
├── documents/{documentId}
├── calendars/{calendarId}
├── daily_reports/{reportId}
└── patterns/
    ├── branch/{branchId}
    └── employee/{employeeId}

notifications_v3/system/
├── campaign_definitions/{campaignId}
├── campaign_runs/{runId}
├── notification_jobs/{jobId}
├── in_app_messages/{messageId}
└── user_message_state/{stateId}
```

## 6. Nomenclatura de Cloud Functions

Patrón: `apiV100-{tipo}-{servicio}-{nombre}`

Ejemplos:
```
apiV100-firebaseEntryHttp-checkinbiz-tasksHandler
apiV100-firebaseEntryHttp-checkinbiz-requestManualChecklog
apiV100-firebaseEntryHttp-checkinbiz-updateChecklog
apiV100-firebaseEntryHttp-checkinbiz-calendarHandler
apiV100-firebaseFirestoreTriggersCheckinBiz-onChecklogWrite
```

## 7. Permisos y Roles

El sistema usa `EmployeeResponsibility` para determinar el nivel de acceso:

```typescript
enum ResponsibilityLevel {
  worker     = 1,
  supervisor = 2,
  manager    = 3,
  owner      = 4,
}
```

- **isEntityWriter**: admin/owner global de la entidad (tiene `user_entity_roles`)
- **level**: nivel de responsabilidad en una sucursal concreta
- Los permisos siempre se verifican en backend; el frontend solo adapta la UX

## 8. Entornos

| Entorno | Firebase Project | Base URL |
|---|---|---|
| Dev | dev-encodebiz | `https://us-central1-dev-encodebiz.cloudfunctions.net/` |
| Prod | encodebiz-saas | TBD |

Ver [DEPLOY.md](./DEPLOY.md) para comandos y URLs completas.

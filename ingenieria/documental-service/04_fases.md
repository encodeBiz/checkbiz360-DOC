# 04 — Fases de Implementación

Cada fase es **independiente y desplegable** sin romper el sistema actual.
No hay migración de datos: Firestore permanece como fuente ([ADR-003](./adr/ADR-003-firestore-fuente-sin-migracion.md)).

---

## Fase 0: Documentación de ingeniería

**Estado:** ✅ Completada — este set.

**Objetivo:** documentarlo todo (as-is, to-be, contratos, ADRs, TDRs) **antes** de escribir una línea de código. Requisito explícito del proyecto.

**Prerequisito:** ninguno.

- Set completo en `DOCS/ingenieria/documental-service/` (README + 01–05 + 6 ADRs + 5 TDRs).

**Criterio de éxito:** el port es ejecutable a partir de la doc sin volver a leer el código de Firebase; el contrato de las 8 rutas está congelado en [03_contratos-api.md](./03_contratos-api.md).

**Rollback:** no aplica.

---

## Fase 1: Fundación del servicio

**Estado:** ✅ Completada — el servicio compila y arranca; `/health` responde `{ ok:true, service:"documents" }`.

**Objetivo:** dejar en pie el esqueleto de `services/documents` sin lógica documental todavía.

**Prerequisito:** Fase 0.

- `services/documents/` con `app.ts`, `server.ts`, `package.json` (`@encodebiz/documents`), `tsconfig.json`, `Dockerfile` (copia de `tasks`, puerto 3007).
- `GET /health` → `{ ok: true, service: "documents" }`.
- Bloque en `docker-compose.yml` (+ `docker-compose.dev.yml`) para `documents` (`PORT=3007`, secrets/env como `tasks`: `GOOGLE_APPLICATION_CREDENTIALS`, `FIREBASE_WEB_API_KEY`, bucket de Storage).
- `package.json` raíz: `services/documents` en `workspaces`.
- nginx: `upstream documents_service { server documents:3007; }` + `location /api/v1/documents/` con `client_max_body_size` ≥ 10 MB (multipart).

**Criterio de éxito:** `GET /health` responde en local y tras el compose; el servicio arranca y compila limpio; ningún archivo de Firebase se toca.

**Rollback:** no aplica (no hay código productivo nuevo activo).

---

## Fase 2: Port del módulo `document`

**Estado:** ✅ Completada — typecheck del monorepo verde; el servicio arranca con el router montado; `400` (sin `entityId`) y `401` (sin token) verificados en local. Pendiente prueba e2e con datos reales (alta con fichero, signed URL, índice, notificaciones) contra Firestore/Storage — se hace en despliegue (Fase 3).

**Objetivo:** las 8 rutas responden desde el servidor con el mismo contrato que Firebase.

**Prerequisito:** Fase 1.

- Portar dominio, casos de uso, `FirestoreDocumentRepository`, `DocumentPermissionService`, `DocumentStorageService` y controladores (ver [TDR-001](./tdr/TDR-001-port-modulo-document.md)).
- Auth **solo Firebase ID token**, portada 1:1 (`validateToken` + `resolveActor`), sin `requireFirebaseAuth` de shared (ver [ADR-004](./adr/ADR-004-auth-solo-firebase-token.md), [TDR-002](./tdr/TDR-002-resolucion-actor-y-matriz-de-permisos.md)).
- Storage privado + signed URL + multipart (ver [TDR-003](./tdr/TDR-003-storage-privado-y-multipart.md)).
- Notificaciones reutilizando el scaffolding ya presente en `tasks` (ver [ADR-005](./adr/ADR-005-notificaciones-reutilizadas-de-shared.md), [TDR-004](./tdr/TDR-004-notificaciones-documentales.md)).
- Portar el subsistema `core/searchIndex` + `documentSearchIndex` (ver [ADR-006](./adr/ADR-006-indice-de-busqueda-firestore.md), [TDR-005](./tdr/TDR-005-indice-de-busqueda-documental.md)).
- Reutilizar de `services/tasks`: `FirestoreBranchRepository`, `FirestoreEmployeeRepository`, `validateToken`, `parseMultipartFormData`.

**Criterio de éxito:** las 8 rutas responden igual que `documentsHandler` (verificado contra [03_contratos-api.md](./03_contratos-api.md)); auth por Firebase token; alta con fichero, descarga firmada, ack, índice y notificaciones funcionales; typecheck del monorepo verde; Firebase intacto.

**Rollback:** el servicio queda desplegado pero sin tráfico (nadie apunta a él); Firebase sigue sirviendo.

---

## Fase 3: Cutover del tráfico  *(futuro, fuera del alcance inmediato)*

**Objetivo:** el tráfico real de documental lo sirve el servidor, no Firebase.

**Prerequisito:** Fase 2 validada end-to-end contra Firestore/Storage real.

- El front admin y la app apuntan de la URL de `documentsHandler` (parte `/documents`) a `…/api/v1/documents`.
- Observación de latencia/errores durante un periodo acordado.
- La parte `/documents` de `documentsHandler` marcada como *deprecated* (no eliminada); se retira tras observación.

**Criterio de éxito:** 100% del tráfico documental pasa por el servidor; latencia y tasa de error iguales o mejores que Firebase.

**Rollback:** revertir la URL del cliente a `documentsHandler`. Sin pérdida de datos (misma Firestore, mismo Storage).

---

## Resumen

```
Fase 0: Documentación            → este set (as-is, to-be, contratos, ADRs, TDRs)
Fase 1: Fundación del servicio   → esqueleto documents:3007 + /health + compose + nginx
Fase 2: Port del módulo document → 8 rutas con contrato idéntico, auth Firebase, Storage, índice, notificaciones
Fase 3 (futuro): Cutover         → el tráfico apunta al servidor; documentsHandler(/documents) deprecated
```

**Orden estricto:** nada de código antes de cerrar la Fase 0. No hacer cutover (Fase 3) sin los criterios de la Fase 2 cumplidos.

# 04 — Fases de Implementación

Cada fase es **independiente y desplegable** sin romper el sistema actual.
No hay migración de datos: Firestore permanece como fuente ([ADR-003](./adr/ADR-003-firestore-fuente-sin-migracion-de-datos.md)).

---

## Fase 0: Fundación del servicio

**Estado:** ✅ Completada — el servicio compila y arranca; `/health` responde `{ ok: true, service: "tasks" }`.

**Objetivo:** dejar en pie el esqueleto de `services/tasks` sin lógica de tareas todavía.

**Prerequisito:** ninguno.

- `services/tasks/` con `app.ts`, `server.ts`, `package.json` (`@encodebiz/tasks`), `tsconfig.json`, `Dockerfile` (copia de `reports`, puerto 3006).
- `GET /health` → `{ ok: true, service: "tasks" }`.
- Bloque en `docker-compose.yml` (+ `docker-compose.dev.yml`) para `tasks`.
- nginx: `upstream tasks_service { server tasks:3006; }` + `location /api/v1/tasks/` con `client_max_body_size` acorde al vídeo máximo.

**Criterio de éxito:** `GET /health` responde en local y tras el compose; el servicio arranca y compila limpio; ningún archivo de Firebase se toca.

**Rollback:** no aplica (no hay código productivo nuevo activo).

---

## Fase 1: Port del módulo `task`

**Estado:** ✅ Completada — typecheck del monorepo verde; `/health`, 401 sin token y 404 verificados en arranque local. Pendiente prueba funcional end-to-end contra Firestore real (Fase 2).

**Objetivo:** las 14 rutas responden desde el servidor con el mismo contrato que Firebase.

**Prerequisito:** Fase 0.

- Portar dominio, casos de uso, `FirestoreTaskRepository` y controladores (ver [TDR-001](./tdr/TDR-001-port-modulo-task.md)).
- Cablear Firestore vía `@encodebiz/shared` (Admin SDK).
- Auth dual portada **1:1** (`validateToken` + `validateTokenJWT` + `canWrite`), sin usar `requireFirebaseAuth` de shared para no cambiar el comportamiento en producción (ver [TDR-002](./tdr/TDR-002-resolucion-actor-y-permisos.md)).
- Subida de evidencias a Storage (ver [TDR-003](./tdr/TDR-003-storage-evidencias-y-multipart.md)).
- Extraer el framework de notificaciones a `@encodebiz/shared` (ver [ADR-005](./adr/ADR-005-notificaciones-a-shared.md)).
- `findPendingStartNotifications` se conserva en el repo pero **sin ruta que lo consuma**.

**Criterio de éxito:** las 14 rutas responden igual que `tasksHandler` (verificado contra [03_contratos-api.md](./03_contratos-api.md)); auth por ambas vías; subida de foto/vídeo funcional; compila limpio; Firebase intacto.

**Rollback:** el servicio queda desplegado pero sin tráfico (nadie apunta a él); Firebase sigue sirviendo.

---

## Fase 2: Cutover del tráfico

**Objetivo:** el tráfico real de tareas lo sirve el servidor, no Firebase.

**Prerequisito:** Fase 1 validada.

- El front admin y la app apuntan de la URL de `tasksHandler` a `…/api/v1/tasks`.
- Observación de latencia/errores durante un periodo acordado.
- `tasksHandler` marcado como *deprecated* (no eliminado).

**Criterio de éxito:** 100% del tráfico de tareas pasa por el servidor; latencia y tasa de error iguales o mejores que Firebase; los schedules/triggers de Firebase siguen operando sobre los datos que escribe el servidor.

**Rollback:** revertir la URL del cliente a `tasksHandler`. Sin pérdida de datos (misma Firestore).

---

## Fase 3: Documento de integración

**Objetivo:** dejar la guía de consumo para los dos clientes.

**Prerequisito:** Fase 2 estable.

- Documento de integración para la **app móvil** (staff JWT, endpoints, subida de evidencias).
- Documento de integración para el **front de administración** (Firebase ID token, endpoints, permisos por nivel).
- Publicado en la doc canónica (junto a esta carpeta).

**Criterio de éxito:** un desarrollador de app o de front puede integrar contra `tasks` sin leer el código del servicio.

---

## Fase 4 (futuro, fuera de alcance): retirada y unificación

- Eliminar `tasksHandler` de Firebase tras periodo de observación.
- Unificar `Employee`/`Branch` duplicados en `@encodebiz/shared` (deuda registrada en [TDR-001](./tdr/TDR-001-port-modulo-task.md)).

---

## Resumen

```
Fase 0: Fundación del servicio   → esqueleto tasks:3006 + /health + compose + nginx
Fase 1: Port del módulo task     → 14 rutas con contrato idéntico, auth dual, Storage
Fase 2: Cutover                  → el tráfico apunta al servidor; tasksHandler deprecated
Fase 3: Doc de integración       → guías app móvil + front admin
Fase 4 (futuro): retirada + unificación de dominio
```

**Orden estricto:** no hacer cutover (Fase 2) sin los criterios de la Fase 1 cumplidos. El documento de integración (Fase 3) se escribe cuando el contrato real está congelado tras el cutover.

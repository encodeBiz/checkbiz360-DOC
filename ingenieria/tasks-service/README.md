# Servicio de Tareas — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Tareas (Tasks)
**Fecha de inicio:** 2026-07-26
**Estado:** Diseño / Pre-implementación
**Autor:** Jose Acevedo

---

## Contexto y Motivación

La API de tareas vive hoy dentro de Firebase Functions (`tasksHandler`, un Express montado sobre `https.onRequest` con 14 rutas). Es tráfico de usuario final —app móvil del empleado y back office— y como tal paga dos costes evitables:

1. **Latencia** por cold start de Cloud Functions en cada invocación.
2. **Coste** por invocación sobre un volumen de tráfico operacional.
3. **Acoplamiento de despliegue** — se libera junto al resto del bundle de Functions, sin escalar ni versionar de forma independiente.

La superficie HTTP es toda `https.onRequest` (Express puro, cero `onCall`), así que se puede portar como un *lift-and-shift* limpio al servidor privado `encodebiz-api`, que ya sirve `merlin`, `checkinbiz`, `sync`, `analytics` y `reports` detrás de nginx.

---

## Principio de diseño

> **Solo se migra quién sirve el HTTP. El dato sigue en Firestore y lo reactivo sigue en Firebase.**

La API de tareas pasa a un microservicio dedicado (`tasks`, puerto 3006). Firestore permanece como fuente de datos (cero migración) y los schedules/triggers de tareas se quedan en Firebase, operando sobre los mismos datos que el servidor escribe.

---

## Alcance

**Dentro:** las 14 rutas HTTP de tareas (CRUD, asignaciones, notas, estado, validación/rechazo, evidencias, valoraciones, actividad).

**Fuera:** el schedule de aviso de inicio tardío y los triggers de Firestore de tareas (permanecen en Firebase); cualquier migración de datos a PostgreSQL.

---

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | Dónde vive hoy el módulo, superficie, datos y limitaciones |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Microservicio `tasks`, topología, auth, frontera con Firebase, cutover |
| 03 | [Contratos de API](./03_contratos-api.md) | Las 14 rutas: auth, permisos, request/response |
| 04 | [Fases de implementación](./04_fases.md) | Roadmap: fundación → port → cutover → integración |
| 05 | [Integración: Front de administración](./05_integracion-front-admin.md) | Guía de consumo desde el back office (Firebase ID token, permisos por nivel) |
| 06 | [Integración: App móvil](./06_integracion-app-movil.md) | Guía de consumo desde la app del empleado (staff JWT, subida de evidencias) |
| 07 | [Integración: Informe de tareas](./07_integracion-informe-tareas.md) | Guía del informe de tareas en Excel (`POST /api/reports/tasks`) |
| 08 | [Pausas en las tareas](./08_pausas.md) | Propuesta: pausar y reanudar, decisiones pendientes y fases por uso |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-microservicio-tasks-dedicado.md) | Microservicio `tasks` dedicado, no ampliar un servicio existente | Aceptado |
| [ADR-002](./adr/ADR-002-solo-http-lo-reactivo-en-firebase.md) | Migrar solo HTTP; triggers y schedules permanecen en Firebase | Aceptado |
| [ADR-003](./adr/ADR-003-firestore-fuente-sin-migracion-de-datos.md) | Firestore sigue siendo la fuente; cero migración de datos | Aceptado |
| [ADR-004](./adr/ADR-004-auth-dual-conservada.md) | Conservar la auth dual (Firebase ID token + staff JWT) | Aceptado |
| [ADR-005](./adr/ADR-005-notificaciones-a-shared.md) | Extraer el framework de notificaciones a `@encodebiz/shared` | Aceptado (implementado) |
| [ADR-006](./adr/ADR-006-informe-tareas-en-reports.md) | El informe de tareas (Excel) vive en el servicio `reports` | Aceptado (implementado) |
| [ADR-007](./adr/ADR-007-geocerca-en-la-tarea.md) | La geocerca de un trabajo vive en la tarea, no en una sucursal por encargo | Aceptado |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-port-modulo-task.md) | Port del módulo `task` al servicio `tasks` | 1 | Diseño aprobado |
| [TDR-002](./tdr/TDR-002-resolucion-actor-y-permisos.md) | Resolución del actor y matriz de permisos | 1 | Diseño aprobado |
| [TDR-003](./tdr/TDR-003-storage-evidencias-y-multipart.md) | Subida de evidencias: Storage y multipart | 1 | Diseño aprobado |
| [TDR-004](./tdr/TDR-004-informe-tareas-xlsx.md) | Informe de tareas en Excel (servicio `reports`) | — | Implementado |
| [TDR-005](./tdr/TDR-005-worksite-y-geocerca-de-tarea.md) | Lugar de trabajo de la tarea y geocerca al iniciarla | 5 | Diseño aprobado |

---

## Estado del roadmap

- [x] **Fase 0** — Fundación del servicio (`tasks:3006` + `/health` + compose + nginx) ✔ compila y arranca
- [x] **Fase 1** — Port del módulo `task` (14 rutas, auth dual, Storage) + extracción de notificaciones a shared ✔ typecheck monorepo verde, `/health` y auth verificados
- [ ] **Fase 2** — Cutover del tráfico (app + front → servidor)
- [x] **Fase 3** — Documento de integración (app móvil + front admin) ✔ [05](./05_integracion-front-admin.md) · [06](./06_integracion-app-movil.md)
- [ ] **Fase 4** *(futuro)* — Retirada de `tasksHandler` + unificación de dominio

**Fase 5 — Lugar de trabajo y geocerca de tarea:** `workSite` opcional en la tarea + geocerca
restrictiva al iniciarla + precondición de jornada abierta comprobada en servidor. 🔜 en
implementación. Ver [ADR-007](./adr/ADR-007-geocerca-en-la-tarea.md),
[TDR-005](./tdr/TDR-005-worksite-y-geocerca-de-tarea.md).

**Añadido — Informe de tareas (Excel):** `POST /api/reports/tasks` en el servicio `reports`. ✔ implementado y typecheck verde; pendiente prueba e2e en despliegue. Ver [ADR-006](./adr/ADR-006-informe-tareas-en-reports.md), [TDR-004](./tdr/TDR-004-informe-tareas-xlsx.md), [07](./07_integracion-informe-tareas.md).

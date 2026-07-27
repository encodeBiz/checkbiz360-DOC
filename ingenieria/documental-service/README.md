# Servicio de Gestión Documental — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Gestión Documental (Documents)
**Fecha de inicio:** 2026-07-26
**Estado:** Diseño / Pre-implementación
**Autor:** Jose Acevedo

---

## Contexto y Motivación

La API de gestión documental vive hoy dentro de Firebase Functions (`documentsHandler`, un Express montado sobre `https.onRequest` con 8 rutas, que además comparte handler con `/reports`). Es tráfico de usuario final —back office y app del empleado— y como tal paga los mismos costes evitables que ya motivaron el port de tareas:

1. **Latencia** por cold start de Cloud Functions en cada invocación.
2. **Coste** por invocación sobre un volumen de tráfico operacional.
3. **Acoplamiento de despliegue** — se libera junto al resto del bundle de Functions, sin escalar ni versionar de forma independiente.

La superficie HTTP es toda `https.onRequest` (Express puro, cero `onCall`) y **el módulo no tiene nada reactivo** (ningún trigger de Firestore, ningún schedule). Es el escenario más limpio posible para un *lift-and-shift* al servidor privado `encodebiz-api`, que ya sirve `merlin`, `checkinbiz`, `sync`, `analytics`, `reports` y `tasks` detrás de nginx.

---

## Principio de diseño

> **Solo se migra quién sirve el HTTP. El dato sigue en Firestore.**

La API documental pasa a un microservicio dedicado (`documents`, puerto 3007). Firestore permanece como fuente de datos (cero migración) y Firebase sigue proveyendo la verificación de ID token y el bucket de Storage.

---

## Alcance

**Dentro:** las 8 rutas HTTP de gestión documental (listar/buscar, crear con subida de fichero, detalle, actualizar, archivar, generar URL de descarga firmada, confirmar lectura *(ack)*, listar acks). Incluye la **matriz de permisos** por scope/tipo/nivel, el **índice de búsqueda** en Firestore y las **notificaciones** de alta y de ack requerido.

**Fuera:** cualquier migración de datos; la retirada del `documentsHandler` de Firebase (fase de cutover, futura); la notificación de ack a nivel `entity_employees` (el origen la bloquea en V1 y se conserva ese comportamiento).

---

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | Dónde vive hoy el módulo, superficie, datos y limitaciones |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Microservicio `documents`, topología, auth, frontera con Firebase, cutover |
| 03 | [Contratos de API](./03_contratos-api.md) | Las 8 rutas: auth, permisos, request/response, códigos de error |
| 04 | [Fases de implementación](./04_fases.md) | Roadmap: documentación → fundación → port → cutover |
| 05 | [Integración: Front de administración](./05_integracion-front-admin.md) | Resumen de consumo desde el back office (Firebase ID token, permisos por nivel, subida multipart) |
| 06 | [Migración del front](./06_migracion-frontend.md) | Guía accionable: mapeo de rutas antiguo→nuevo, ejemplos `fetch` de las 8 rutas, checklist y errores |
| 07 | [Prompt para el agente de front](./07_prompt-agente-front.md) | Prompt de onboarding para el agente de IA que migra el front |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-microservicio-documents-dedicado.md) | Microservicio `documents` dedicado, no ampliar un servicio existente | Aceptado |
| [ADR-002](./adr/ADR-002-solo-http-lo-reactivo-en-firebase.md) | Migrar solo HTTP; el módulo no tiene reactivo, y lo que exista se queda en Firebase | Aceptado |
| [ADR-003](./adr/ADR-003-firestore-fuente-sin-migracion.md) | Firestore sigue siendo la fuente; cero migración de datos | Aceptado |
| [ADR-004](./adr/ADR-004-auth-solo-firebase-token.md) | Auth **solo Firebase ID token** (sin staff JWT, a diferencia de tasks) | Aceptado |
| [ADR-005](./adr/ADR-005-notificaciones-reutilizadas-de-shared.md) | Reutilizar el framework de notificaciones ya extraído en el port de tasks | Aceptado |
| [ADR-006](./adr/ADR-006-indice-de-busqueda-firestore.md) | Conservar el índice de búsqueda en Firestore (`searchIndex`) | Aceptado |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-port-modulo-document.md) | Port del módulo `document` al servicio `documents` | 1 | Diseño aprobado |
| [TDR-002](./tdr/TDR-002-resolucion-actor-y-matriz-de-permisos.md) | Resolución del actor y matriz de permisos documental | 1 | Diseño aprobado |
| [TDR-003](./tdr/TDR-003-storage-privado-y-multipart.md) | Storage privado, paths por scope, signed URL y multipart | 1 | Diseño aprobado |
| [TDR-004](./tdr/TDR-004-notificaciones-documentales.md) | Notificaciones `doc_uploaded` / `doc_ack_required` | 1 | Diseño aprobado |
| [TDR-005](./tdr/TDR-005-indice-de-busqueda-documental.md) | Índice de búsqueda documental (tokenizer, prefijos, reindex) | 1 | Diseño aprobado |

---

## Estado del roadmap

- [x] **Fase 0** — Documentación de ingeniería completa (este set) — *documentar todo antes de tocar código*
- [x] **Fase 1** — Fundación del servicio (`documents:3007` + `/health` + compose + nginx) ✔ compila y arranca; `/health` → `{ ok:true, service:"documents" }`
- [x] **Fase 2** — Port del módulo `document` (8 rutas, auth, Storage, notificaciones, índice) ✔ typecheck del monorepo verde; arranque con router OK; 400/401 verificados en local. Pendiente prueba e2e con datos reales (alta con fichero, signed URL, índice, notificaciones) contra Firestore/Storage — se hace en despliegue.
- [ ] **Fase 3** *(futuro)* — Cutover del tráfico (app + front → servidor) + retirada de `documentsHandler`

**Orden estricto:** ninguna línea de código antes de cerrar la Fase 0. No se hace cutover (Fase 3) sin los criterios de la Fase 2 cumplidos.

# Checklogs HTTP — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Fichajes (checklogs)
**Fecha de inicio:** 2026-07-30
**Estado:** Diseño aprobado / Implementación en curso
**Autor:** Jose Acevedo

---

## Contexto y Motivación

El fichaje es el camino crítico del producto: es lo que hace un empleado cuando llega a trabajar, con el móvil en la mano y con prisa. Hoy ese camino pasa por tres Cloud Functions (`createChecklog`, `updateChecklog`, `requestManualChecklog`) que pagan cold start en cada arranque frío y se despliegan atadas al resto del bundle de Functions.

El arranque de la app (login, validate, calendario) ya se movió al servidor privado y se sirve por el proxy `criticalHandler`. Lo que queda del recorrido diario del empleado —fichar— sigue en Firebase. Este documento cierra ese hueco.

---

## Principio de diseño

> **Solo se migra quien sirve el HTTP. El dato sigue en Firestore y lo reactivo sigue en Firebase.**

Las rutas pasan al servicio `checkinbiz` (puerto 3002), que ya existe y ya sirve auth y calendario. Firestore permanece como fuente única: el contenedor escribe en las mismas colecciones, así que **los triggers de Firestore siguen disparándose igual** (heurística, sync a PostgreSQL, webhooks, notificaciones operativas). No se toca ni un trigger ni un schedule.

---

## Alcance

**Dentro** — las tres funciones HTTP de checklogs:

| Función Firebase | Cliente | Auth actual |
|---|---|---|
| `…checkinbiz-createChecklog` | App móvil | JWT de empleado (`JWT_2FA_SECRET`); Firebase ID token si `isAdmin` |
| `…checkinbiz-updateChecklog` | App móvil + back office | Firebase ID token |
| `…checkinbiz-requestManualChecklog` | Back office | Firebase ID token |

**Fuera** — todo lo reactivo, que se queda en Firebase y sigue operando sobre lo que escribe el contenedor: `onWhriteChecklog`, `onChecklogSync`, `onChecklogWebhook`, `sanitizer-checklogs`, `dailyCollectorData`, `employeePlanifierWorker`. Tampoco entra ninguna migración de datos a PostgreSQL.

---

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | Las tres funciones, su auth, sus clientes y sus dependencias |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Rutas en `checkinbiz`, mapa de reutilización, frontera con Firebase |
| 03 | [Contratos de API](./03_contratos-api.md) | Request/response y catálogo de códigos de error |
| 04 | [Fases de implementación](./04_fases.md) | Roadmap con criterios de validación y rollback por fase |
| 05 | [Conexión de clientes](./05_conexion-de-clientes.md) | Qué tocar en el back office y en la app para apuntar al servidor |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-solo-http-lo-reactivo-en-firebase.md) | Migrar solo HTTP; triggers y schedules permanecen en Firebase | Aceptado |
| [ADR-002](./adr/ADR-002-clientes-apuntan-directo-sin-proxy.md) | Los clientes apuntan directo a la API; sin capa de proxy | Aceptado |
| [ADR-003](./adr/ADR-003-promocion-a-shared-sin-tercera-copia.md) | Lo común se promueve a `@encodebiz/shared`; no se crea una tercera copia | Aceptado |
| [ADR-004](./adr/ADR-004-auth-por-ruta-no-global.md) | Auth por ruta (JWT de empleado / ID token), no middleware global | Aceptado |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-port-checklogs-http.md) | Port de las tres rutas al servicio `checkinbiz` | 1 | Implementado |

---

## Estado del roadmap

- [x] **Fase 0** — Promoción de lo común a `@encodebiz/shared` y repunte de `tasks` y `documents` ✔ typecheck y build del monorepo verdes; `tasks` y `documents` arrancan y responden igual que antes
- [x] **Fase 1** — Port de las tres rutas al servicio `checkinbiz` ✔ compila y arranca; las tres rutas responden 401 sin token y el ping de calentamiento responde 200. **Pendiente:** verificación funcional contra Firestore real (tabla de errores de [03](./03_contratos-api.md) y los cuatro casos frágiles)
- [~] **Fase 2** — Cutover del back office (dos variables de entorno — ver [05](./05_conexion-de-clientes.md)). Aplicado en `.env` y `.env.production` locales: `UPDATE_LOG` y `REQUEST_MANUAL_CHECKLOG` apuntan ya al servidor. **Pendiente:** cambiar las variables en el entorno de despliegue (`.env*` está en el `.gitignore`, así que el fichero del repo no viaja), y la verificación funcional — una corrección de fichaje de extremo a extremo y una jornada manual en sus dos modos
- [ ] **Fase 3** — Cutover de la app móvil (cambio de URLs + release en stores) **y de `CREATE_LOG` del front**, que comparte variable con el kiosco QR
- [ ] **Fase 4** *(futuro)* — Retirada de los handlers originales

Ver [04_fases.md](./04_fases.md) para criterios de éxito y rollback de cada fase.

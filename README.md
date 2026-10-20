# EncodeBiz — Base Documental Unificada

> Fuente única de verdad para todo el ecosistema EncodeBiz (backend, backoffice, app móvil).
> Generada el 2026-05-19 consolidando la documentación dispersa de los tres sub-proyectos.

## Sub-proyectos

| Proyecto | Tecnología | Ruta |
|---|---|---|
| **encodeBiz-SAAS** | Firebase Functions v2, TypeScript, Node 22 | `encodeBiz-SAAS/` |
| **encodebiz-front-saas** | Next.js 14, React, Material UI | `encodebiz-front-saas/` |
| **CheckBiz360** | Flutter 3.35.6, Riverpod 2, Dio | `CheckBiz360/checkbiz360/` |

## Navegación

### Seguridad
- [Security-Audit/](./Security-Audit/README.md) — Auditoría de seguridad 2026-05-25: hallazgos, severidades y plan de remediación
  - [AUDIT-BACKEND.md](./Security-Audit/2026-05-25/AUDIT-BACKEND.md) — 8 hallazgos en Cloud Functions / Firestore / Storage
  - [AUDIT-BACKOFFICE.md](./Security-Audit/2026-05-25/AUDIT-BACKOFFICE.md) — 6 hallazgos en Next.js backoffice
  - [AUDIT-MOBILE.md](./Security-Audit/2026-05-25/AUDIT-MOBILE.md) — 6 hallazgos en app Flutter
  - [REMEDIATION-PLAN.md](./Security-Audit/2026-05-25/REMEDIATION-PLAN.md) — Plan priorizado por fases con owners y estimados
- [ingenieria/reglas-firestore/](./ingenieria/reglas-firestore/README.md) — 🔴 **Alerta máxima 17/18-oct-2026**: la lectura de Firestore está abierta sin sesión; paso 1 (sesión obligatoria) y paso 2 (aislar por entidad)

### Arquitectura y dominio
- [ARQUITECTURA.md](./ARQUITECTURA.md) — Visión de sistema, capas, stack, comunicación
- [DOMINIO.md](./DOMINIO.md) — Entidades, roles, enums, máquinas de estado
- [INGENIERIA.md](./INGENIERIA.md) — Reglas de ingeniería unificadas (todos los stacks)
- [DEPLOY.md](./DEPLOY.md) — Entornos, comandos de deploy, funciones activas
- [ingenieria/programadas-a-escala/](./ingenieria/programadas-a-escala/README.md) — 🔴 **Alerta 17/18-oct-2026**: los jobs programados recorren a todos los clientes en serie con topes fijos; reparto por lotes con Cloud Tasks y una task por entidad
- [ingenieria/analisis-a-escala/](./ingenieria/analisis-a-escala/README.md) — 🔴 **Urgente, oct-2026**: el resumen del panel, el cierre diario, el trigger de patrones y Merlin con mil empleados; índices, sin correladas, precálculo por entidad
- [ingenieria/quiosco/](./ingenieria/quiosco/README.md) — Modo quiosco: tablet compartida en el centro, QR o código más foto como prueba, sin biometría (diseño cerrado 18-oct-2026)
- [ingenieria/avisos-por-correo/](./ingenieria/avisos-por-correo/README.md) — Avisos de trabajo por correo para quien no usa el móvil: tareas asignadas, cambiadas o retiradas y la semana del domingo, solo con la casilla de la persona, agrupados
- [ingenieria/almacenamiento/](./ingenieria/almacenamiento/README.md) — Almacenamiento por empresa: trigger de Storage que cuenta, 2 GB incluidos, exceso a 0,25 €/GB-mes, retención del quiosco y bucket europeo

### Módulos de producto
- [modulos/task.md](./modulos/task.md) — Tareas operativas: permisos, API, dominio, app, backoffice
- [modulos/checklog.md](./modulos/checklog.md) — Checklogs, solicitud manual Modo A/B, aprobación
- [modulos/notificaciones.md](./modulos/notificaciones.md) — Push FCM + in-app v3, tipos, bugs
- [modulos/heuristica.md](./modulos/heuristica.md) — Motor EMA: métricas, patrones, interpretación
- [modulos/reporting-analitica.md](./modulos/reporting-analitica.md) — Agregados diarios, dashboards y reportes masivos
- [modulos/documentos.md](./modulos/documentos.md) — Gestión documental, scopes, permisos, storage
- [modulos/calendario.md](./modulos/calendario.md) — Horarios, festivos, cascada entity→branch→employee, bugs

### Capas específicas
- [capas/backend.md](./capas/backend.md) — Cloud Functions, DDD, cold start, patrones Firestore
- [capas/app-movil.md](./capas/app-movil.md) — Flutter, feature-first, Riverpod, DI, navegación
- [capas/backoffice.md](./capas/backoffice.md) — Next.js, App Router, patrones, convenciones

### QA
- [Qa/plan-automatizacion.md](./Qa/plan-automatizacion.md) — Plan y método de la automatización: acciones, listeners y programadas; contrato y punta a punta; fases
- [Qa/automatizacion-qa-staging.md](./Qa/automatizacion-qa-staging.md) — (sustituido por plan-automatizacion.md) Primer planteamiento, desde los planes manuales de QA
- [Qa/fase2-autenticacion-y-acceso.md](./Qa/fase2-autenticacion-y-acceso.md) — Fase 2 de la regresión: qué se automatiza y los 7 hallazgos que la condicionan
- [Qa/task-module-qa-plan.md](./Qa/task-module-qa-plan.md) — Plan de pruebas del módulo de tareas (revisar §3: el endpoint ya no es Cloud Function)

## Reglas de uso

1. Esta carpeta `DOCS/` es la fuente única de verdad. Las docs en sub-proyectos han sido eliminadas o deprecadas.
2. Cada sub-proyecto mantiene su propio `AGENTS.md` como guía operativa de ese repo.
3. Cuando un módulo tenga cambios de contrato, actualizar el archivo correspondiente aquí antes de mergar código.
4. El módulo de tareas es el más crítico — leer `modulos/task.md` antes de tocar cualquier controlador de tareas.

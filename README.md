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

### Arquitectura y dominio
- [ARQUITECTURA.md](./ARQUITECTURA.md) — Visión de sistema, capas, stack, comunicación
- [DOMINIO.md](./DOMINIO.md) — Entidades, roles, enums, máquinas de estado
- [INGENIERIA.md](./INGENIERIA.md) — Reglas de ingeniería unificadas (todos los stacks)
- [DEPLOY.md](./DEPLOY.md) — Entornos, comandos de deploy, funciones activas

### Módulos de producto
- [modulos/task.md](./modulos/task.md) — Tareas operativas: permisos, API, dominio, app, backoffice
- [modulos/checklog.md](./modulos/checklog.md) — Checklogs, solicitud manual Modo A/B, aprobación
- [modulos/notificaciones.md](./modulos/notificaciones.md) — Push FCM + in-app v3, tipos, bugs
- [modulos/heuristica.md](./modulos/heuristica.md) — Motor EMA: métricas, patrones, interpretación
- [modulos/documentos.md](./modulos/documentos.md) — Gestión documental, scopes, permisos, storage
- [modulos/calendario.md](./modulos/calendario.md) — Horarios, festivos, cascada entity→branch→employee, bugs

### Capas específicas
- [capas/backend.md](./capas/backend.md) — Cloud Functions, DDD, cold start, patrones Firestore
- [capas/app-movil.md](./capas/app-movil.md) — Flutter, feature-first, Riverpod, DI, navegación
- [capas/backoffice.md](./capas/backoffice.md) — Next.js, App Router, patrones, convenciones

## Reglas de uso

1. Esta carpeta `DOCS/` es la fuente única de verdad. Las docs en sub-proyectos han sido eliminadas o deprecadas.
2. Cada sub-proyecto mantiene su propio `AGENTS.md` y `AI-RULES.md` como guía operativa de ese repo.
3. Cuando un módulo tenga cambios de contrato, actualizar el archivo correspondiente aquí antes de mergar código.
4. El módulo de tareas es el más crítico — leer `modulos/task.md` antes de tocar cualquier controlador de tareas.

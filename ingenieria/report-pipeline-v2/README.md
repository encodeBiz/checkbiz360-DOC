# Report Pipeline V2 — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS  
**Dominio:** checkinbiz — Reporting, Analytics, IA  
**Fecha de inicio:** 2026-06-01  
**Estado:** Diseño / Pre-implementación  
**Autor:** Jose Acevedo  

---

## Contexto y Motivación

El sistema actual genera reportes diarios por sucursal computándolos **bajo demanda** sobre Firestore. Con el crecimiento del volumen de checklogs, este modelo presenta tres riesgos críticos:

1. **Costo y latencia no controlables** — Un reporte sobre 6 meses de una empresa con 200 empleados hace miles de lecturas de Firestore en tiempo real.
2. **Información incompleta** — Las valoraciones de tareas (task ratings) no están integradas en los reportes diarios ni en los patrones heurísticos.
3. **Pérdida de historia de patrones** — El patrón de una sucursal o empleado se sobreescribe con cada actualización. No hay evolución temporal: los patrones "se disuelven".
4. **IA sin contexto histórico** — El motor heurístico analiza solo el snapshot actual del patrón, sin acceso a su evolución. Una IA que no sabe si algo mejoró o empeoró no tiene valor real.

Esta iniciativa es un **antes y un después** en la arquitectura de datos de encodeBiz.

---

## Principio de diseño

> **Firebase es la fuente operacional. PostgreSQL es la fuente analítica.**

Ninguno reemplaza al otro. Firebase sigue siendo el backend en tiempo real para el app. PostgreSQL se convierte en el Data Warehouse privado que alimenta los reportes, la IA y los históricos.

---

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | Arquitectura vigente, entidades, flujos y limitaciones |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Diseño completo del nuevo pipeline |
| 03 | [Schema PostgreSQL](./03_schema-postgres.md) | DDL completo de todas las tablas |
| 04 | [Fases de implementación](./04_fases.md) | Roadmap en 4 fases, independientes y desplegables |
| 05 | [Contratos de API](./05_contratos-api.md) | Endpoints entre Firebase y el servidor privado |
| 06 | [Upgrade de IA](./06_ia-upgrade.md) | Rediseño del prompt y contexto histórico para el motor heurístico |
| 07 | [Migración del front](./07_migracion-frontend.md) | Guía para el front de administración: consumir el API privado (merlin async, reports PDF/XLSX, analytics S2S) — contratos, endpoints, auth |
| 08 | [Prompt agente front](./08_prompt-agente-front.md) | Prompt paste-ready para el agente del front: fuentes de verdad, dominios, endpoints y reglas |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-postgresql-warehouse.md) | PostgreSQL privado como Data Warehouse analítico | Aceptado |
| [ADR-002](./adr/ADR-002-sync-fire-and-forget.md) | Sync a PostgreSQL como best-effort awaited desde triggers | Aceptado |
| [ADR-003](./adr/ADR-003-firestore-frontend-source.md) | Firestore permanece como fuente de datos del frontend | Aceptado |
| [ADR-004](./adr/ADR-004-deterministic-ids.md) | IDs deterministas para todas las operaciones de upsert | Aceptado |
| [ADR-005](./adr/ADR-005-fases-independientes.md) | Implementación en fases independientes, no big bang | Aceptado |
| [ADR-006](./adr/ADR-006-pattern-snapshots-inmutables.md) | Pattern snapshots idempotentes por fecha — UPSERT diario, no append-only | Aceptado |
| [ADR-007](./adr/ADR-007-task-ratings-en-subcolleccion.md) | Task ratings en subcollección Firestore (decisión pre-existente documentada) | Documentado |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-analytics-server-client.md) | AnalyticsServerClient — cliente HTTP Firebase → servidor privado | 1 | Diseño aprobado |
| [TDR-002](./tdr/TDR-002-raw-sync-payload.md) | Raw Sync — qué datos se sincronizan, cuándo y cómo | 1 | Diseño aprobado |
| [TDR-003](./tdr/TDR-003-daily-report-build.md) | Daily Report enriquecido — algoritmo de construcción en servidor privado | 2 | Diseño aprobado |
| [TDR-004](./tdr/TDR-004-pattern-snapshot-algorithm.md) | Pattern Snapshot — algoritmo de captura diaria e idempotencia | 3 | Diseño aprobado |
| [TDR-005](./tdr/TDR-005-trend-analysis-algorithm.md) | TrendAnalysis — algoritmo de tendencias con datos escasos | 4 | Diseño aprobado |
| [TDR-006](./tdr/TDR-006-heuristic-core-v2.md) | HeuristicCore V2 — integración del contexto histórico sin romper V1 | 4 | Diseño aprobado |
| TDR-007 *(pendiente)* | HeuristicCore en servidor — migración completa, proxy Firebase, thresholds Firestore vs PostgreSQL | 5 | Pendiente diseño |

---

## Principios de transición

- **No hay big bang.** Cada fase es desplegable de forma independiente sin romper el sistema actual.
- **Contratos cerrados antes de código.** La Fase 0 resuelve inconsistencias documentales antes de tocar código productivo.
- **Idempotencia siempre.** Toda operación de escritura usa IDs deterministas para ser re-ejecutable sin duplicar datos.
- **Firebase nunca pierde** — En caso de fallo del servidor PostgreSQL, Firebase conserva todos los datos operacionales. El sync puede recuperarse más tarde.
- **Best-effort awaited, no fire-and-forget puro.** El sync hace `await` con timeout de 7 s y absorbe el error. El fallo queda en logs de Firebase (servidor caído) o en `sync_log` de PostgreSQL (fallo transitorio).
- **Sin migración histórica en fase 1.** El pipeline nuevo solo acumula datos hacia adelante. El histórico de Firestore se puede migrar en una fase posterior si se considera necesario.

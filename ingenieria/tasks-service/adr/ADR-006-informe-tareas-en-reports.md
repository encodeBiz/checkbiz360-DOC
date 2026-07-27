# ADR-006 — El informe de tareas vive en el servicio `reports`

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Un cliente pide un **informe de tareas en Excel**: el listado de tareas de un periodo con estado, tiempos y equipo asignado. Hay que decidir dónde vive esa generación y qué contiene.

---

## Decisión

- **Hogar:** el servicio **`reports`**, no `tasks`. `reports` ya es el contexto de generación de informes: tiene la infra de XLSX/PDF (`exceljs`/`pdfkit`), la subida a Storage y el guardado de histórico (`entities/{entityId}/reports`).
- **Fuente de datos:** las tareas de **Firestore** (`entities/{entityId}/tasks/...`), leídas on-demand. Sin pre-cómputo ni tabla nueva en Postgres.
- **Alcance (v1):** **una sola hoja "Tareas"**, una fila por tarea, con:
  `Empresa · Centro · Título · Estado · Prioridad · Inicio · Fin · Tiempo invertido · Equipo (nombres concatenados) · Valoración · Nº evidencias`.
- **`Tiempo invertido` = `completedAt − startedAt` de la tarea** (elapsed de la tarea), sin sumas por persona.
- **Se descarta el "% de jornada"**: una tarea puede cruzar días o repartirse entre varios; dividir contra las horas de jornada no produce una métrica limpia. Lo relevante es el tiempo invertido absoluto.

---

## Justificación

**`reports` es el contexto correcto.** Generar un fichero, subirlo a Storage y registrar el histórico ya está resuelto ahí; el informe de tareas reutiliza ese pipeline en vez de duplicarlo en `tasks` (que es API operacional).

**On-demand basta.** El volumen de tareas por entidad/periodo es bajo comparado con checklogs; una consulta a Firestore al pedir el informe es suficiente. No se justifica un cron ni un warehouse como en el registro de jornada.

**Una hoja, sin métricas derivadas dudosas.** El cliente quiere ver las tareas y el tiempo dedicado. El `%` de jornada se descartó por no ser interpretable de forma fiable. Se entrega el dato bruto (inicio, fin, tiempo invertido) y se deja el análisis fuera del informe.

---

## Consecuencias

**Positivas:**
- Reutiliza XLSX/PDF + Storage + histórico de `reports`. Implementación pequeña.
- Sin migración de datos ni índices nuevos: se usa la misma query de tareas que ya existe (`orderBy(dueAt)` + filtros).
- Contrato simple y ampliable (más hojas/columnas en v2 si se piden).

**Negativas / Compromisos aceptados:**
- `reports` gana dependencia de lectura sobre el dominio de tareas (Firestore `tasks` + subcolecciones `ratings`/`resources`). Aceptable: ya lee Firestore para meta de entidad/centro/empleado.
- El `Tiempo invertido` es tan bueno como los timestamps que escriba la app (`startedAt`/`completedAt`). Si faltan, la fila sale sin tiempo (ver [TDR-004](../tdr/TDR-004-informe-tareas-xlsx.md)).

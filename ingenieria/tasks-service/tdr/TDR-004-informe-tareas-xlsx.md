# TDR-004 — Informe de tareas en Excel (servicio `reports`)

**Fecha:** 2026-07-26
**Estado:** Diseño aprobado, en implementación
**Componente:** `encodebiz-api` — `reports` → `POST /api/reports/tasks`

---

## Endpoint

```
POST /api/reports/tasks        (Firebase ID token, igual que /generate)
body: {
  entityId: string,            // obligatorio
  start: "YYYY-MM-DD",         // obligatorio
  end:   "YYYY-MM-DD",         // obligatorio
  branchId?: string,
  status?: TaskStatus,         // filtro opcional (en memoria)
  format?: "xlsx" | "pdf"      // default "xlsx"
}
→ 201 { reporData: { ref: { path }, ... }, code: "report/success" }
→ 204 si no hay tareas en el filtro
```

Respuesta y flujo idénticos a `/generate`: construye → sube a Storage → guarda histórico en `entities/{entityId}/reports` → devuelve el `ref.path`.

**Metadatos del informe.** El registro de histórico y la respuesta llevan `type` y `format` para distinguir informes:
- `type`: `"attendance"` (registro de jornada, `/generate`) · `"task"` (tareas, `/tasks`).
- `format`: `"pdf"` · `"xlsx"`.

Se añadieron a `ReportHistoryResponse` y a `saveReportHistory`, así que **ambos** informes (jornada y tareas) los emiten.

**Compatibilidad hacia atrás:** los registros de histórico previos a este cambio no tienen `type`/`format`. Los consumidores (front) asumen por defecto `type = "attendance"` y `format = "pdf"` cuando faltan (hasta ahora el único informe era la jornada en PDF).

---

## Query de tareas (Firestore)

Se reutiliza el mismo acceso que `FirestoreTaskRepository.findAll`, sin índices nuevos:

```
entities/{entityId}/tasks
  .orderBy("dueAt", "asc")
  [.where("branchId", "==", branchId)]     // si viene
  .where("dueAt", ">=", start)
  .where("dueAt", "<=", end)               // end a fin de día
  .limit(1000)
```

- **Ventana temporal por `dueAt`** (fecha de vencimiento), coherente con la query de tareas existente.
- `status` (y futuros filtros) se aplican **en memoria** tras la consulta, para no requerir índices compuestos adicionales.

Por cada tarea se leen dos subcolecciones (en paralelo, `Promise.all`):
- `ratings/*` → media de `rating` (1–5).
- `resources/*` → nº de evidencias (count).

Nombres resueltos y cacheados en memoria durante la generación:
- **Entidad:** `getEntityMeta(entityId).name`.
- **Centro:** `getBranchConfig(entityId, branchId).name` (cache por `branchId`).
- **Empleado:** `getWorkerMeta(entityId, employeeId).displayName` (cache por `employeeId`), para concatenar el equipo.

---

## Hoja "Tareas" (una fila por tarea)

| Columna | Origen |
|---|---|
| Empresa | `entityMeta.name` |
| Centro | `getBranchConfig(branchId).name` |
| Título | `task.title` |
| Estado | `task.status` → etiqueta ES (Borrador/Asignada/En curso/Completada/Validada/Rechazada/Cancelada) |
| Prioridad | `task.priority` → etiqueta ES (Baja/Media/Alta/Crítica) |
| Inicio | `task.startedAt` (fecha-hora local; vacío si no hay) |
| Fin | `task.completedAt` (vacío si no hay) |
| Tiempo invertido (h) | `(completedAt − startedAt)` en horas, `0.00`; vacío si falta alguno |
| En pausa (h) | `(pausedMs + (now − pausedAt si hay pausa abierta))` en horas, `0.00`; vacío sin `startedAt` |
| Nº pausas | `task.pauseCount`; vacío sin `startedAt` |
| Tiempo invertido sin pausas (h) | `max(0, Tiempo invertido − En pausa)`, `0.00`; vacío sin `completedAt` |
| Equipo | `task.assignedEmployeeIds` → nombres concatenados con `, ` |
| Valoración | media de `ratings.rating`, `0.0`; vacío si no hay |
| Nº evidencias | `count(resources)` |

Cabecera de informe (filas superiores): título "INFORME DE TAREAS", entidad, periodo — mismo estilo que `buildReportXLSX`. `autoFilter` sobre la cabecera de columnas.

---

## PDF (opcional, mismo patrón)

Si `format=pdf`, se construye la misma tabla con `pdfkit` reutilizando el estilo de `buildReportPDF`. La v1 prioriza XLSX (lo que pide el cliente).

---

## Casos borde

- **Sin tareas en el filtro** → `204` (igual que `/generate` con `report/not_checklog_found`, aquí `report/not_tasks_found`).
- **`startedAt`/`completedAt` ausentes** → `Inicio`/`Fin`/`Tiempo invertido` vacíos; la fila se incluye igualmente con su estado.
- **Tarea sin asignados** → `Equipo` vacío.
- **Empleado/centro no resoluble** → se usa el id como fallback o "—".

---

## Criterio de éxito

- `POST /api/reports/tasks` con `format=xlsx` devuelve un XLSX con la hoja "Tareas" y las columnas anteriores, subido a Storage, con su entrada de histórico.
- Sin tareas → `204`.
- Compila limpio en el pipeline del monorepo.

---

## Material del add-on de inventario (2026-10-08)

Si la entidad tiene el add-on de inventario, el informe lleva además tres columnas en «Tareas»
(Material, Sin cuadrar, Coste material) y una hoja «Material» con una fila por tarea y artículo.
Sin el add-on, el fichero es exactamente el descrito arriba. La regla, las lecturas y las
columnas están en [inventario/TDR-005](../../inventario/tdr/TDR-005-material-en-el-informe-de-tareas.md).

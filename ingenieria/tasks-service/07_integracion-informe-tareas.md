# 07 — Integración: Informe de tareas (Excel)

> **Para:** front de administración (back office).
> **Qué cubre:** cómo pedir el informe de tareas en Excel al servicio `reports`.
> **Fuente de verdad:** `encodebiz-api/services/reports`. Diseño en [ADR-006](./adr/ADR-006-informe-tareas-en-reports.md) y [TDR-004](./tdr/TDR-004-informe-tareas-xlsx.md).

---

## Endpoint

```
POST https://api.checkbiz360.com/api/reports/tasks
Authorization: Bearer <FIREBASE_ID_TOKEN>
Content-Type: application/json
```

Es una acción de back office: mismo auth (Firebase ID token) y mismo patrón que el informe de jornada (`/api/reports/generate`).

### Body

| Campo | Req. | Descripción |
|---|---|---|
| `entityId` | ✅ | Entidad |
| `start` | ✅ | `YYYY-MM-DD` (desde) |
| `end` | ✅ | `YYYY-MM-DD` (hasta) |
| `branchId` | — | Filtra por centro |
| `status` | — | Filtra por estado (`draft`/`assigned`/`in_progress`/`completed`/`validated`/`rejected`/`cancelled`) |
| `format` | — | `xlsx` (por defecto y único en v1) |

La ventana temporal se aplica sobre la **fecha de vencimiento** (`dueAt`) de la tarea.

### Respuestas

- **201** — informe generado:
  ```json
  {
    "reporData": {
      "entity": "ACME S.L.",
      "branch": "Centro Norte, Centro Sur",
      "entityId": "ent_123",
      "start": "2026-07-01T00:00:00.000Z",
      "end":   "2026-07-26T23:59:59.999Z",
      "status": "active",
      "type": "task",
      "format": "xlsx",
      "ref": { "path": "checkbiz/reports/entities/ent_123/tasks_2026-07-01-2026-07-26_1690000000000.xlsx" }
    },
    "code": "report/success"
  }
  ```

  Todos los informes llevan **`type`** y **`format`** (también en el histórico `entities/{entityId}/reports`), para que el front los distinga y sepa la extensión:
  - `type`: `"task"` (informe de tareas) · `"attendance"` (registro de jornada).
  - `format`: `"xlsx"` · `"pdf"`.

  **Compatibilidad hacia atrás (importante para el front):** los informes generados **antes** de este cambio no traen estos campos. Al leer el histórico, aplica estos valores por defecto:
  - sin `type` → **`"attendance"`**
  - sin `format` → **`"pdf"`**

  Es correcto históricamente: hasta ahora el único informe era el registro de jornada en PDF.
- **204** — no hay tareas para el filtro (`code: "report/not_tasks_found"`).

---

## Cómo descargar el fichero

`reporData.ref.path` es la ruta del objeto en **Firebase Storage** (igual que el informe de jornada). El front obtiene la URL de descarga con el SDK de Storage:

```ts
import { getStorage, ref, getDownloadURL } from "firebase/storage";

const res = await fetch("https://api.checkbiz360.com/api/reports/tasks", {
  method: "POST",
  headers: { "Authorization": `Bearer ${idToken}`, "Content-Type": "application/json" },
  body: JSON.stringify({ entityId, start: "2026-07-01", end: "2026-07-26", branchId }),
});

if (res.status === 204) { /* no hay tareas en el periodo */ }
else {
  const { reporData } = await res.json();
  const url = await getDownloadURL(ref(getStorage(), reporData.ref.path));
  window.open(url); // descarga el .xlsx
}
```

El informe también queda registrado en el histórico `entities/{entityId}/reports` (igual que los demás), por si el front lista informes generados.

---

## Contenido del Excel

Una hoja **"Tareas"**, una fila por tarea:

`Empresa · Centro · Título · Estado · Prioridad · Inicio · Fin · Tiempo invertido (h) · Equipo · Valoración · Nº evidencias`

- **Inicio/Fin**: fecha-hora local del centro; vacío si la tarea no los tiene marcados.
- **Tiempo invertido (h)**: `Fin − Inicio` de la tarea, en horas; vacío si falta alguno.
- **Equipo**: nombres de los asignados concatenados.
- **Valoración**: media de las valoraciones de la tarea (1–5).

> El `Tiempo invertido` depende de que la app marque `startedAt`/`completedAt`. Si faltan, la tarea aparece igualmente pero sin tiempo.

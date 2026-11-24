# TDR-009 — Marcar una tarea como incidencia y avisar a operaciones

**Fecha:** 2026-11-11
**Estado:** Diseño aprobado (Jose, 2026-11-11). En desarrollo.
**Componente:** `encodebiz-api` — `tasks`, `analytics` (alertas), `@encodebiz/shared`; app móvil; panel

---

## Resumen

Cuando el trabajador no puede hacer una tarea por algo ajeno —«no me abrieron la puerta y no
pude acceder»—, hoy solo puede dejar una nota de tipo «Incidencia» (`incident_note`). Nadie se
entera hasta que abre la tarea.

Se sustituye esa nota por un **botón rojo arriba del todo** en la tarea, en la app y en el
panel: «Marcar incidencia». Pide una nota obligatoria y, si se quiere, una foto o un archivo.
Al pulsarlo, la tarea queda marcada, el hecho entra en el historial y **sale una alerta urgente
sola**: correo al momento, alerta roja en el panel y push a los responsables de la sucursal.
Operaciones la resuelve con una respuesta y la marca desaparece.

---

## 1. Lo que hay

- `TaskNote.type` admite `incident_note`. El panel lo ofrece en el desplegable de notas
  (`taskUi.tsx`, `TaskActionDialog.tsx`). Es una nota más: no marca la tarea ni avisa a nadie.
- Las alertas tienen un canal de **correo inmediato** (`enqueueImmediate` en
  `analytics/application/alerts/pending.ts`), el que ya usa `issue_opened`. No pasa por el
  resumen de la mañana.
- Las alertas del panel (`GET /panel/alerts`) se calculan al pedirlas desde el espejo
  (`tasks_raw` y compañía): si el problema se arregla, desaparecen en la siguiente lectura.
- Los recursos de la tarea (TDR-003, TDR-007) ya se suben por multipart a la carpeta de la
  tarea, con la empresa en la ruta.

## 2. Decisiones

### D1. Un botón, no un tipo de nota

La incidencia es un **hecho de la tarea**, no un comentario. Se quita `incident_note` del
desplegable de notas en el panel y en la app. Las notas `incident_note` que ya existen se
siguen pintando como hasta ahora (no se migran); simplemente no se pueden crear más. El tipo
se queda en el modelo para leerlas.

El botón va **en rojo, arriba del todo** de la ficha de la tarea, visible sin bajar.

### D2. La incidencia vive en la tarea

```ts
task.incident?: {
  status: "open" | "resolved";
  note: string;                 // obligatoria, recortada, 1..1000
  reportedBy: string;           // uid
  reportedByEmployeeId?: string;
  reportedByRole: TaskActorRole;
  reportedAt: Date;
  resourceIds: string[];        // la foto o el archivo, si lo hay (D4)
  resolvedBy?: string;
  resolvedAt?: Date;
  resolution?: "replanned" | "cancelled" | "solved";   // replanned = fechas, personas o las dos (Jose, 2026-11-11: antes eran dos opciones)
  resolutionNote?: string;
}
```

Una sola incidencia **abierta** a la vez. La tarea guarda la última; las anteriores quedan en el
historial (D5). Marcar otra con una abierta → `409 task/incident_already_open`, y la app enseña
la que hay.

### D3. Endpoints

| Método | Ruta | Quién | Qué |
|---|---|---|---|
| `POST` | `/:taskId/incident` | Asignado o supervisor (`canOperateAssignedTask`) y gestor (`canManageTask`) | Multipart: `note` obligatoria, `file` opcional (uno) |
| `POST` | `/:taskId/incident/resolution` | Gestor (`canManageTask`) | `{ resolution, note? }` |

Errores: `400 task/incident_note_required`, `409 task/incident_already_open`,
`409 task/incident_not_open`, `403 task/unauthorized`.

Todo pasa por el servidor: la nota obligatoria y el aviso no dependen de lo que haga cada
cliente.

### D4. La foto o el archivo

Se guarda como `TaskResource` con `isEvidence: false` (no cuenta para
`requireEvidenceOnCompletion` ni para el informe, TDR-007) y un `incidentAt` que lo liga a la
incidencia. Mismos tipos y límites que los adjuntos. Misma carpeta de la tarea: lleva
`entities/{entityId}` en la ruta y el trigger de Storage la cuenta.

### D5. Historial

Dos tipos nuevos de `TaskActivity`, iguales en la app y el panel:

- `incident_reported`: quién, cuándo, la nota y si lleva archivo.
- `incident_resolved`: quién, cuándo, la resolución y su nota.

### D6. La alerta

Regla nueva `task_incident`, severidad `high`, `target: "task"` con el `taskId` en `params`.

1. **Correo al momento.** `tasks` avisa a `analytics` por s2s, como `reportPendingAlert`, y
   entra por `enqueueImmediate`. Texto, lo observado: «{nombre} ha marcado una incidencia en
   «{tarea}» ({sucursal}, {cliente}): «{nota}»», con el enlace a la tarea. Lleva el archivo
   como enlace, no adjunto.
2. **Panel.** `BuildPanelAlerts` lista las tareas con `incident.status = "open"` desde el
   espejo, arriba del todo. Desaparece sola al resolverla.
3. **Push** a los responsables de la sucursal y a los supervisores de la tarea.

Destinatarios del correo: los de siempre (`alertRecipients`, owner y admin), **y nadie más**
(Jose, 2026-11-11: los responsables de sucursal no reciben el correo). El push sí les llega.

### D7. Qué le pasa a la tarea (aprobado 2026-11-11)

El estado de la tarea no cambia (sigue sin terminar), pero mientras tenga una
incidencia **no cuenta como incumplida**: se excluye de `tasks_overdue`,
`customer_tasks_missed` y del retraso de inicio. El trabajador fue y no pudo; castigarle en los
informes enseña a no marcar incidencias.

Al resolver, la resolución manda: `replanned` la devuelve a la cuenta normal con sus nuevas
fechas o personas, y `cancelled` la cancela por el camino de siempre.

### D8. Cómo se ve y cómo se busca

- **Detalle de la tarea** (app y panel): con la incidencia abierta, la ficha sale **en rojo**
  (cabecera o banda superior) con la nota, quién, cuándo y el archivo. Resuelta, vuelve a su
  color y la incidencia queda en el historial.
- **Listados y buscadores** (app y panel): la tarea con incidencia abierta se distingue en rojo
  en la lista y hay un filtro «Con incidencia». El servidor acepta `hasIncident=true` en
  `GET /tasks` (y en lo que alimente el buscador de tareas).
- **App:** el botón «Marcar incidencia» va **en el header** de la tarea, claro y visible, no
  en un menú.
- **Panel:** el botón va arriba del todo de la ficha, en rojo.

### D9. El informe de tareas (Jose, 2026-11-11)

La incidencia **queda en el informe de tareas** (Excel, servicio `reports`, TDR-004), abierta o
resuelta. Se lee del historial espejado (`task_events_raw`): cada `incident_reported` abre una y el
siguiente `incident_resolved` de la tarea la cierra; `tasks_raw` solo tiene la última y sin la
resolución.

- Hoja «Tareas»: columna «Incidencia» (Abierta / Resuelta · cómo, y cuántas si hubo varias), solo
  si alguna tarea del periodo la tuvo.
- Hoja «Incidencias»: una fila por incidencia, con la nota, quién y cuándo la marcó, si llevaba
  archivo, la resolución, quién y cuándo la resolvió y su nota. Sale siempre; sin incidencias lo
  dice en una línea.

## 3. Fases

1. **Servidor** (`develop`): modelo en `shared`, endpoints, historial, regla y correo, espejo.
2. **Panel**: botón, modal (nota + archivo), marca en la ficha y el listado, resolver, alerta
   en la portada, quitar `incident_note` del desplegable.
3. **App**: botón, modal con cámara o archivo, marca en la tarea, quitar `incident_note`.

## 4. Puntos abiertos

- Comprobar que `tasks_raw` copia el campo `incident` o añadirlo al espejo.
- Quién más recibe el push si la sucursal no tiene responsables: hoy nadie (igual que las
  incidencias de la plantilla).

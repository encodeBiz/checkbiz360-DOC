# 06 — Integración: App móvil (empleado)

> **Para:** equipo de la app móvil de CheckBiz (Flutter).
> **Qué cubre:** cómo consumir el servicio `tasks` desde la app del empleado (staff), con auth por JWT propio y subida de evidencias.
> **Fuente de verdad:** los controladores en `encodebiz-api/services/tasks`. Este doc resume el contrato; si hay discrepancia, manda el router.

---

## 1. Qué cambia

La API de tareas se movió de la Cloud Function `tasksHandler` a un servicio propio. **El contrato es el mismo**; solo cambia la URL base.

| | Antes | Ahora |
|---|---|---|
| URL | URL de la function `tasksHandler` | `https://api.checkbiz360.com/api/v1/tasks/...` |
| Auth | Staff JWT (`Authorization: Bearer <JWT>`) | **igual** |
| Payloads / respuestas | — | **iguales** |

Migración en la app: sustituir la URL base.

---

## 2. Autenticación (staff JWT)

La app del empleado no usa Firebase Auth: envía su **JWT de staff** (el mismo que ya usa hoy, firmado con `JWT_2FA_SECRET`).

```
Authorization: Bearer <STAFF_JWT>
```

El servidor resuelve al empleado a partir del `employeeId` del token y valida que pertenezca a la `entityId` de la petición. Si el token es inválido o el empleado no existe → `401`/`403`/`404`.

```dart
final base = "https://api.checkbiz360.com/api/v1/tasks";
final res = await http.get(
  Uri.parse("$base?entityId=$entityId"),
  headers: {"Authorization": "Bearer $staffJwt"},
);
```

---

## 3. Qué puede hacer un empleado

El empleado es un actor de nivel `worker` (salvo que tenga responsabilidad de `supervisor`+ en la sucursal). Con nivel `worker`:

| Acción | ¿Permitido? |
|---|---|
| Ver **sus** tareas asignadas | ✅ (el listado se acota solo a las suyas) |
| Ver detalle / actividad de una tarea asignada | ✅ |
| Cambiar estado de una tarea asignada (iniciar, completar) | ✅ |
| Añadir nota a una tarea asignada | ✅ |
| Subir evidencia (foto/vídeo) | ✅ |
| Crear / asignar / validar / valorar | ❌ `403` (requiere `supervisor`+) |

> Si el empleado tiene responsabilidad de supervisor o superior, además puede asignar/validar/valorar según la matriz de [05_integracion-front-admin.md](./05_integracion-front-admin.md) §3.

---

## 4. Flujo típico del empleado

### Listar mis tareas
```
GET /?entityId=X&status=assigned
→ 200 Task[]     // ya viene acotado a las tareas del empleado
```

### Ver detalle
```
GET /:taskId
→ 200 { task, assignments, notes, resources, ratings, activity, validations }
```

### Iniciar / completar (cambio de estado)
```dart
await http.patch(
  Uri.parse("$base/$taskId/status"),
  headers: {"Authorization": "Bearer $staffJwt", "Content-Type": "application/json"},
  body: jsonEncode({"status": "in_progress"}),   // luego "completed"
);
→ 200 TaskDetail
```
Al completar, el servidor calcula el cumplimiento temporal (`completed_on_time` / `completed_late`) contra `dueAt`. Si `config.requireEvidenceOnCompletion` es `true`, sube la evidencia **antes** de completar.

### Añadir nota
```
POST /:taskId/notes
body: { "content": "Faltaba material", "type": "operational_note" }
→ 201 TaskNote
```

---

## 5. Subida de evidencias (multipart)

Endpoint clave de la app. `multipart/form-data` con el fichero.

```dart
final req = http.MultipartRequest("POST", Uri.parse("$base/$taskId/resources"))
  ..headers["Authorization"] = "Bearer $staffJwt"
  ..fields["description"] = "Estantería repuesta"
  ..files.add(await http.MultipartFile.fromPath("file", localPath));   // photo o video

final res = await req.send();
→ 201 TaskResource   // { type, filename, mimeType, url, storagePath, sizeKB, ... }
```

Reglas:
- Tipos aceptados: **foto** o **vídeo**.
- Tamaño validado contra `task.config.maxPhotoSizeMB` / `maxVideoSizeMB`. Por encima → `400`.
- nginx admite hasta **30 MB** de cuerpo (`client_max_body_size`); si se sube el `maxVideoSizeMB`, hay que subir también ese límite.
- La `url` devuelta es pública y estable (misma convención de Storage que hoy).

---

## 6. Errores

| HTTP | Código | Cuándo |
|---|---|---|
| 401 | `auth/unauthorized` | Falta/!Bearer en `Authorization` |
| 403 | `task/unauthorized` | Sin nivel suficiente para la acción |
| 404 | `task/employee_not_found` | El `employeeId` del token no existe en la entidad |
| 400 | (validación) | Fichero de tipo/tamaño no permitido |

---

## 7. Formato de `task.description` (Markdown)

Desde el panel admin la descripción se escribe con un editor simple que **guarda texto plano con sintaxis Markdown** (no HTML). El campo sigue siendo un `string` y el contrato de la API no cambia.

Subconjunto que puede llegar (CommonMark + task lists de GFM):

| Sintaxis | Significado |
|---|---|
| `# ` / `## ` / `### ` | Título |
| `- texto` | Lista con viñetas |
| `1. texto` | Lista numerada |
| `- [ ] texto` / `- [x] texto` | Lista de tareas (checklist) |
| `> texto` | Cita |
| `---` | Separador |
| `**negrita**`, `*cursiva*`, `` `código` `` | Marcas en línea |
| `[texto](https://…)` | Enlace |

Ejemplo real de lo que puede venir en el campo:

```
## Apertura
- [ ] Revisar cámaras
- [x] Contar caja
- [ ] Abrir persiana

**Ojo:** avisar al supervisor si falta efectivo.
```

En Flutter:

- **Mínimo viable:** pintarlo tal cual con un `Text`. Es legible sin más — por eso se eligió Markdown y no HTML.
- **Recomendado:** `flutter_markdown` (`MarkdownBody(data: task.description ?? '')`) para títulos, listas, negritas y enlaces.
- **Checklists:** el paquete `markdown` de Dart no convierte `- [ ]` en checkbox; lo pinta como viñeta con el texto `[ ]`. Si se quiere el checkbox real, hay que añadir un builder propio para los ítems de lista que empiecen por `[ ] ` / `[x] `.
- **Solo lectura:** los checks son parte del texto de la descripción, no un estado persistido. Marcarlos en la app **no** cambia nada en el servidor; el avance de la tarea se sigue reportando con los cambios de estado y las notas/evidencias.
- **Nunca renderizar como HTML:** el texto lo escribe un usuario; tratarlo como Markdown/plano evita inyección.

---

## 8. Notas importantes

- **Notificaciones push:** las recibe el empleado igual que hoy (creada/asignada/validada…); no requiere nada en la app más allá del registro de token FCM que ya hace.
- **Aviso de inicio tardío:** lo sigue emitiendo el schedule de Firebase (no se migró). La app no cambia por esto.
- **Datos en tiempo real:** si la app escucha Firestore directamente para el detalle de tareas, sigue igual — el servidor escribe en la misma colección.

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

> **Cambio de contrato — mandar `geo`.** Ver §4.bis.

### Añadir nota

```
POST /:taskId/notes
body: { "content": "Faltaba material", "type": "operational_note" }
→ 201 TaskNote
```

---

## 4.bis Lugar de trabajo de la tarea (`workSite`) y geocerca

Una tarea puede llevar **su propia dirección y su propia geocerca** — es el caso del trabajo a
domicilio, donde el empleado nunca está en el centro. Ver [ADR-007](./adr/ADR-007-geocerca-en-la-tarea.md).

```jsonc
task.workSite = {            // opcional; puede no venir
  "street": "Calle Mayor 3, 28013 Madrid, España",
  "geo": { "lat": 40.4169, "lng": -3.7035 },
  "radiusMeters": 150,
  "timeZone": "Europe/Madrid",
  "precision": "rooftop"
}
```

### Qué tiene que hacer la app

**Mandar `geo` al cambiar a `in_progress` y a `completed`.** El mismo punto que ya se manda al
fichar.

```dart
await http.patch(
  Uri.parse("$base/$taskId/status"),
  headers: {"Authorization": "Bearer $staffJwt", "Content-Type": "application/json"},
  body: jsonEncode({
    "entityId": entityId,
    "status": "in_progress",
    "geo": {"lat": pos.latitude, "lng": pos.longitude},
  }),
);
```

Es obligatorio **solo** si `task.workSite != null`, pero lo más simple es mandarlo siempre que se
tenga la posición. Si la tarea tiene `workSite` y no llega `geo` → `400 task/geo_required`; hay
que pedir el permiso de ubicación **antes** de ofrecer el botón, igual que en el fichaje.

**Enseñar la dirección y la distancia.** Con `workSite.geo` la app puede mostrar dónde es el
trabajo y a qué distancia está el empleado antes de que pulse. Evita el rechazo en vez de
explicarlo después.

### Bloqueo al iniciar

Fuera del radio, **iniciar** se rechaza:

```jsonc
400 {
  "code": "task/out_of_worksite",
  "error": "Outside task work site",
  "details": { "distanceMeters": 480, "allowedRadiusMeters": 150 }
}
```

Al **completar** no se bloquea: la distancia se registra y ya está. Quien cierra la tarea suele
hacerlo ya montado en la furgoneta.

### Jornada abierta

La app **ya** impide iniciar y completar sin jornada abierta (`AttendanceStatus.working` u
`onBreak`, en `task_detail_page.dart`). Eso no cambia. Lo que cambia es que **el servidor también
lo comprueba**, con la misma semántica —el descanso cuenta como jornada abierta—, y responde
`400 task/no_open_session`.

En la práctica la app no debería ver nunca ese código; si aparece, es señal de que su estado de
asistencia y el del servidor se han desincronizado, y lo correcto es refrescar el estado de
fichaje antes de reintentar. Notas y evidencias **no** están sujetas a la regla.

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
| 400 | `task/no_open_session` | Iniciar/completar sin jornada abierta |
| 400 | `task/geo_required` | La tarea tiene `workSite` y no se mandó `geo` |
| 400 | `task/out_of_worksite` | Iniciar fuera del radio del lugar de trabajo |

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

### Implementación en la app (hecho)

Widget: `lib/features/task/presentation/widgets/task_description_markdown.dart` (`TaskDescriptionMarkdown`), usado en `task_detail_page.dart`. Notas de la integración real:

- **Paquete:** `flutter_markdown_plus` — `flutter_markdown` está **descontinuado** en pub.dev (el equipo de Flutter dejó de mantenerlo). `flutter_markdown_plus` es el fork mantenido y conserva la misma API (`MarkdownBody`, `MarkdownStyleSheet`, `checkboxBuilder`, `onTapLink`).
- **Sin impacto en SPM:** tanto `flutter_markdown_plus` como `markdown` son paquetes Dart puros (sin bloque `plugin:`, sin `ios/`/`android/`). No añaden dependencias nativas ni tocan la resolución de Swift Package Manager.
- **Checklists:** corrección respecto a lo que decía antes este doc — el paquete `markdown` 7.x **sí** parsea `- [ ]` / `- [x]` cuando el `ExtensionSet` incluye `UnorderedListWithCheckboxSyntax` / `OrderedListWithCheckboxSyntax` (van dentro de `gitHubFlavored`, que es el set por defecto). El builder propio solo hace falta para el **aspecto** del checkbox, no para que aparezca.
- **Nunca renderizar como HTML:** se usa un `ExtensionSet` propio que **excluye `InlineHtmlSyntax`**, así cualquier etiqueta que escriba el usuario (`<b>`, `<script>`…) se queda como texto literal en vez de interpretarse. Cubierto por test.
- **Solo lectura:** los checks son parte del texto de la descripción, no un estado persistido. Se pintan no interactivos; marcarlos **no** cambiaría nada en el servidor. El avance de la tarea se sigue reportando con los cambios de estado y las notas/evidencias.
- **Enlaces:** se abren con `url_launcher` en app externa y solo si el esquema es `http`, `https` o `mailto`; si no, snackbar de error (`taskDescriptionLinkOpenError`, en es/en/de/pt).
- **Estilos:** el `MarkdownStyleSheet` se deriva del design system (`semanticColors`, tokens de spacing/radius), no de los valores por defecto del paquete.
- **Edición desde móvil:** el formulario de crear/editar tarea sigue con un `TextField` plano. Es correcto y no destructivo — guarda el Markdown tal cual lo escribió el back office.

Tests: `test/widget/task/task_description_markdown_test.dart` (ejemplo del contrato con checklists, listas/cita/separador/enlace, HTML literal, texto plano).

> Alternativa mínima si otro cliente no quiere dependencia: pintar el campo tal cual con un `Text`. Es legible sin más — por eso se eligió Markdown y no HTML.

---

## 8. Notas importantes

- **Notificaciones push:** las recibe el empleado igual que hoy (creada/asignada/validada…); no requiere nada en la app más allá del registro de token FCM que ya hace.
- **Aviso de inicio tardío:** lo sigue emitiendo el schedule de Firebase (no se migró). La app no cambia por esto.
- **Datos en tiempo real:** si la app escucha Firestore directamente para el detalle de tareas, sigue igual — el servidor escribe en la misma colección.

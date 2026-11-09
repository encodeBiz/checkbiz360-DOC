# TDR-007 — Adjuntos en la tarea: un recurso que no es evidencia

**Fecha:** 2026-10-29
**Estado:** Diseño aprobado, pendiente implementación (esta semana)
**Componente:** `encodebiz-api` — `tasks` (+ `TaskResource` en `@encodebiz/shared`, una línea
en `reports`), panel, app en una versión posterior

---

## Resumen

Una empresa de ayuda a domicilio crea una tarea por clienta y quiere que la auxiliar que va a
su casa tenga a mano el expediente: un PDF. Hoy la tarea admite ficheros, pero solo como
**evidencia** de que el trabajo se hizo (fotos y vídeos que sube la trabajadora al terminar).

Se añade a los recursos de la tarea una marca que distingue **adjunto** de **evidencia**. Un
adjunto es un fichero que acompaña a la tarea desde que se crea; una evidencia es lo que
demuestra que se ejecutó. Mismo sitio, misma pantalla, misma subida; cambia lo que cuenta y lo
que viaja con el duplicado.

No hay cartera de clientes ni paso por el documental. Eso es otro módulo (una cartera de
clientes como add-on, con sus tareas y documentos colgando de cada cliente) y necesita su
tiempo. Esto es poder subir un adjunto a una tarea, nada más.

---

## 1. Lo que hay

`TaskResource` (shared) es `{type: "photo" | "video", filename, mimeType, url, storagePath,
sizeKB, uploadedBy, employeeId?, description?}` en la subcolección `resources` de la tarea.

Tres sitios lo tratan como evidencia sin decirlo:

- **Completar la tarea.** Con `requireEvidenceOnCompletion`, el servidor mira si la subcolección
  tiene algo y ya (`updateTaskStatus.controller.ts`). Un adjunto subido por la gestora al crear
  la tarea anularía el control: la auxiliar podría cerrar sin haber subido nada.
- **El informe de tareas** (`reports`, `FirestoreTaskReportClient`) pone en «evidencias» el
  tamaño de la subcolección.
- **El duplicado** no copia recursos, porque son de *esa* ejecución.

Los ficheros viven en `media/entities/{entityId}/checkinbiz/tasks/{taskId}/` y el borrado de la
tarea barre esa carpeta entera (TDR-006).

La app lee `resources` **directamente de Firestore**, no por la API. Un `type` que no conoce
cae en `photo` (`ResourceType.fromString`, `orElse`); al abrir el detalle intenta pintar la URL
como imagen y falla el preview, pero el botón de abrir lanza la URL fuera y el PDF se ve.

---

## 2. Diseño

### 2.1 La marca

```ts
export interface TaskResource {
  …
  type: "photo" | "video" | "document";
  /**
   * `true` o ausente: evidencia de la ejecución (lo que ya existe). `false`: adjunto que
   * acompaña a la tarea. La ausencia vale evidencia a propósito: nada de lo que hay se migra.
   */
  isEvidence?: boolean;
  /** Solo en adjuntos copiados al duplicar: el recurso del que sale la referencia. */
  copiedFrom?: {taskId: string; resourceId: string};
}
```

`type: "document"` admite `application/pdf`. Se puede adjuntar también una foto
(`isEvidence: false`, `type: "photo"`): la marca es lo que decide, no el tipo.

### 2.2 Subir

`POST /:taskId/resources` recibe además `isEvidence` (`"true"`/`"false"`, multipart; ausente =
`true`). Permiso: el de hoy, `canOperateAssignedTask` (gestión, supervisión y asignados).

Límite de tamaño para `document`: **20 MB**, fijo, sin añadirlo a `TaskConfig`: el expediente
no es algo que la empresa quiera afinar por tarea.

Destino en Storage:

| | Carpeta | Se borra con la tarea |
|---|---|---|
| Evidencia (como hoy) | `media/entities/{e}/checkinbiz/tasks/{taskId}/` | Sí |
| Adjunto | `media/entities/{e}/checkinbiz/tasks/adjuntos/{taskId}-{ts}-{filename}` | No |

El adjunto no va dentro de la carpeta de la tarea porque el duplicado copia la **referencia**
(§2.4), y borrar la tarea original —se puede mientras siga en `draft` o `assigned`— barrería un
fichero al que apuntan las copias. La ruta sigue llevando `entities/{entityId}`, así que el
trigger de Storage lo cuenta igual contra los 2 GB de la empresa: **una vez**, por muchas
tareas que lo lleven. Ningún código suma al contador por su cuenta (ADR-002 de almacenamiento).

La URL firmada sigue siendo la de siempre (`storage.ts`, caduca en 2050): la app instalada la
abre tal cual.

### 2.3 Lo que un adjunto NO cuenta

- **Completar**: `requireEvidenceOnCompletion` comprueba que exista al menos un recurso con
  `isEvidence !== false`. Sin eso, el control de evidencia queda anulado.
- **Informe de tareas**: `resourcesCount` cuenta solo `isEvidence !== false`. Una línea en
  `FirestoreTaskReportClient`, pero si no se hace el informe miente: la tarea con expediente y
  sin fotos saldría con una evidencia.
- **Avisos**: subir un adjunto no dispara `notifyTaskResourceUploaded` ni emite
  `task.resource_uploaded`. Ese aviso le dice al gestor «la trabajadora ha subido una foto»;
  él mismo subiendo el expediente no es noticia. Sí queda en `activity`
  (`resource_uploaded`, con `isEvidence: false` en `metadata`).

### 2.4 Duplicar

`POST /:taskId/duplicate` copia los recursos con `isEvidence === false` como documentos nuevos en
`resources` de la copia, con **el mismo `storagePath` y la misma `url`** y `copiedFrom`. No se
copia ningún byte: un fichero, N referencias. Las evidencias no se copian, como hasta ahora.

Esto es lo que hace que el expediente viaje con la tarea de la semana siguiente sin volver a
subirlo y sin pagar treinta copias.

### 2.5 Quitar

`DELETE /:taskId/resources/:resourceId` (ruta nueva; hoy un recurso no se puede quitar). Solo
adjuntos (`isEvidence === false`): una evidencia da `409 task/evidence_not_removable`.
Permiso: `canManageTask` (quien edita la tarea). Deja la actividad `resource_removed` y responde
`{taskId, resourceId, fileDeleted}`.

Quita el documento de `resources`. El fichero se borra **solo si ninguna otra tarea lo
referencia**: `collectionGroup("resources").where("storagePath", "==", …).limit(1)` sobre la
empresa. Hace falta exención de índice de grupo de colección para `resources.storagePath`
(con gcloud). **Si la consulta falla —falta la exención—, el fichero se queda**: uno de más se
cobra, uno de menos deja a otra tarea sin su expediente.

### 2.6 Borrar la tarea

TDR-006 no cambia: barre `tasks/{taskId}/` (las evidencias) y las subcolecciones. Los ficheros
de `adjuntos/` quedan donde están, porque pueden ser de otras tareas. Un adjunto cuyas tareas
se hayan borrado todas se queda en Storage sin que nadie lo recoja: **deuda conocida**, se
contará contra el espacio de la empresa hasta que haya un barrido. No es de esta semana.

---

## 3. Lo que ve cada uno

**La gestora, en el panel.** En el detalle de la tarea, la sección de recursos pasa a tener dos
bloques: «Documentos adjuntos» y «Evidencias». El botón de subir pide el fichero y un check
«Es evidencia de la ejecución», desmarcado por defecto cuando quien sube es gestión y marcado
cuando es la trabajadora desde la app. Un adjunto se puede quitar; una evidencia no. Al
duplicar no hay que hacer nada: la copia nace con los adjuntos.

**La auxiliar, en la app instalada (1.10.x).** Ve el PDF entre los recursos con icono de foto,
el preview no carga y el botón de abrir lo abre en el visor del móvil. Funciona; está feo. La
app además esconde el aviso «falta evidencia» si hay cualquier recurso, así que con solo el
adjunto la app no avisa y el servidor sí rechaza al completar (`task/evidence_required`).

**La auxiliar, en la siguiente versión de la app.** `ResourceType.document` con su icono, los
adjuntos en su bloque, el aviso de evidencia contando solo evidencias, y al subir una foto se
manda `isEvidence: true` explícito. Nada de esto bloquea el servidor ni el panel.

---

## 4. Lo que este TDR no hace

- **No crea clientes.** La tarea no sabe de quién es el expediente; lo sabe el título. Con
  cien clientas, cien PDFs sueltos distinguibles por nombre de fichero. Es el precio de no tener
  cartera de clientes, y se acepta: el día que exista ese add-on, estos adjuntos se reasignan
  al cliente (un dato más, no una migración).
- **No versiona.** Si cambia el expediente, se sube el nuevo en la tarea que toque y las
  siguientes copias ya lo llevan; las copias anteriores conservan el viejo. Ni acuse de recibo
  ni firma: eso es del documental, y si algún día hace falta se pasa el fichero allí.
- **No toca las reglas de Firestore.** La app lee `resources` con la regla que ya tiene; el
  adjunto está en la misma subcolección.
- **No cambia la ruta de las evidencias.** Fotos y vídeos siguen en `tasks/{taskId}/`.

---

## 5. Orden de trabajo

1. `shared`: `TaskResource` con `isEvidence`, `copiedFrom`, `type: "document"`.
2. `tasks`: subida con el check, límite de 20 MB para PDF, destino en `adjuntos/`; sin aviso
   push para adjuntos. Completar cuenta solo evidencias. Duplicar copia referencias. Ruta
   `DELETE /:taskId/resources/:resourceId`.
3. `reports`: `resourcesCount` solo evidencias.
4. Exención de índice de grupo para `resources.storagePath` en dev y prod (gcloud).
5. Panel: dos bloques, check al subir, quitar adjunto.
6. QA: catálogo `DOCS/Qa/catalogo/tareas.md` — subir adjunto; completar con adjunto y sin
   evidencia → 400; duplicar lleva el adjunto con el mismo `storagePath`; quitar en una copia no
   borra el fichero; quitar en la última sí; borrar la tarea original no rompe la copia; el
   informe no cuenta el adjunto.
7. App: en la versión que siga a 1.10.1 (no bloquea).

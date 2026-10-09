# TDR-006 — Borrado de una tarea y de todo lo que cuelga de ella

**Fecha:** 2026-09-25
**Estado:** Diseño aprobado, en implementación
**Componente:** `encodebiz-api` — `tasks` (+ cascada en `@encodebiz/shared`, evento en el catálogo)

---

## Resumen

`DELETE /api/v1/tasks/:taskId` borra una tarea **de verdad** —no la marca, la quita— junto con
las siete subcolecciones que cuelgan de ella y sus ficheros en Storage.

Sólo alcanza tareas en `draft` o `assigned`. Cualquier otro estado se rechaza con `409` y un
mensaje que dice por qué, para que el panel pueda enseñarlo en vez de tragárselo.

---

## 1. Lo que cuelga de una tarea

Son tres capas, y hasta ahora sólo se conocía bien la primera.

**Firestore.** Bajo `entities/{entityId}/tasks/{taskId}` hay siete subcolecciones:
`assignments`, `notes`, `resources`, `ratings`, `validations`, `activity`, `pauses`. Firestore
no cascadea: borrar el documento las deja vivas y sin padre, invisibles para cualquier consulta
y eternas. No hay lista escrita a mano: `FirestoreTaskRepository.delete` las
pregunta con `listCollections()` en el momento, porque una lista es una copia del modelo que
envejece sola y el día que aparezca la octava nadie va a acordarse de actualizarla.

**Storage.** Las evidencias se suben a `media/entities/{entityId}/checkinbiz/tasks/{taskId}/`.
La subcolección `resources` guarda el puntero, no el fichero: borrarla sola deja el archivo en
el bucket, cobrándose, y ya sin nadie que sepa de quién era. Se barre la carpeta entera por
prefijo —con la barra final, que sin ella el prefijo de un id alcanzaría al id que lo empieza—.

**Postgres.** Las valoraciones se sincronizan a `task_ratings_raw` y alimentan la media del
trabajador y el panel. Esta capa **no se toca**, y el §2 explica por qué no hace falta.

---

## 2. Por qué sólo `draft` y `assigned`

No es prudencia genérica: es el punto exacto donde el sistema deja de saber olvidar.

`onWriteTaskForPattern` sólo actúa en la transición hacia `validated` o `rejected`, y lo que
escribe son **medias exponenciales** sobre `checkbiz_branch_patterns` y
`checkbiz_employee_patterns`, más un `taskCount` que únicamente suma. No se recalculan nunca
desde la lista de tareas. Una tarea que llegó a un estado terminal ya está dentro de esas
medias **para siempre**: no hay borrado que la saque, porque restar de una media exponencial no
es una operación que exista. El trigger, además, ignora los borrados a propósito
(`if (!after) return`), igual que `onTaskRatingSync` ignora los suyos y por eso la fila de
`task_ratings_raw` sobreviviría a la tarea.

De ahí sale la línea: **una tarea que nunca se empezó no dejó rastro en ninguna de esas dos
capas**, así que se va limpia y el sistema queda exactamente como si no hubiera existido. Una
que sí se empezó, no. Borrarla produciría lo peor de los dos mundos: la tarea desaparece de la
vista del cliente mientras sus números siguen contando en la nota de su empleado y en el perfil
de su sucursal. Se le enseñaría una media que no puede explicarse con nada que pueda ver.

Por eso `in_progress` tampoco se borra, aunque todavía no haya tocado los patrones: hay alguien
trabajando en ella ahora mismo con la tarea abierta en el móvil, y el camino para eso es
cancelarla, que deja constancia. Y `cancelled`, `completed`, `validated` y `rejected` son
registro de algo que pasó —incluida la evidencia que lo prueba—, que es justo lo que un borrado
se llevaría por delante.

| Estado | Se borra | Por qué |
|---|---|---|
| `draft` | sí | No ha tocado nada |
| `assigned` | sí | No ha tocado nada |
| `in_progress` | no | Hay alguien dentro; el camino es cancelar |
| `completed` | no | Hubo trabajo y hay evidencia |
| `validated` | no | Ya cuenta en los patrones, y eso no se resta |
| `rejected` | no | Ya cuenta en los patrones, y eso no se resta |
| `cancelled` | no | Es el registro de la cancelación |

---

## 3. El rechazo se explica

Un `403` mudo obliga al panel a inventarse el motivo. El rechazo devuelve `409` con
`task/not_deletable`, el `status` que lo impide y un mensaje distinto por caso, porque «no se
puede» y «ya no se puede, cancélala» son cosas distintas para quien está delante.

---

## 4. Contrato

`DELETE /api/v1/tasks/:taskId`, `entityId` por query o body. Permiso `canManageTask`: el mismo
que edita la tarea. Devuelve `200` con lo que se llevó por delante —`{taskId, deleted:
{children, files}}`— en vez de un `204` vacío: quien borra en cascada quiere saber el alcance.

Emite `task.deleted`, alta nueva en el catálogo. Sin él, quien integra por webhook ve nacer la
tarea y no la ve morir, y se queda con un id que ya no resuelve.

---

## 5. Lo que este TDR no hace

**No toca el CLI de cuadrantes** (`services/merlin/.../limpiar.cli.ts`), que seguirá borrando
por `externalRef` sin mirar el estado. Es deliberado: ahí el criterio no es el estado sino el
origen —sólo lo que creó una importación—, y es una operación manual con `--apply`. Sí pasa a
reutilizar la cascada de `shared` en vez de mantener su propia lista de subcolecciones.

**No recalcula los patrones.** No hay hoy nada que los recalcule desde cero, y construirlo es
otro trabajo. Mientras no exista, la regla del §2 es también lo que impide necesitarlo.

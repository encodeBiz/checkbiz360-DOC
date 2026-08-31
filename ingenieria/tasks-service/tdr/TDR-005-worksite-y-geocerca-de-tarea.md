# TDR-005 — Lugar de trabajo de la tarea y geocerca al iniciarla

**Fecha:** 2026-09-01
**Estado:** Diseño aprobado, en implementación
**Componente:** `encodebiz-api` — `tasks` (+ lectura de sesión en `@encodebiz/shared`)
**Decisión de referencia:** [ADR-007](../adr/ADR-007-geocerca-en-la-tarea.md)

---

## Resumen

Dos cosas, independientes entre sí:

1. **Precondición de jornada abierta, ya existente, bajada al servidor.** La app ya impide
   iniciar y completar una tarea sin jornada abierta; la API no. Pasa a comprobarse también en
   `tasks`. Se aplica **siempre**, tenga la tarea `workSite` o no.
2. **Geocerca propia de la tarea.** Si la tarea tiene `workSite`, al pasarla a `in_progress` se
   comprueba la distancia y se rechaza fuera de radio.

El fichaje (`services/checkinbiz`) **no se toca**.

---

## 1. Modelo de datos

Campo nuevo y opcional en `services/tasks/src/domain/entities/Task.ts`:

```ts
export type WorkSitePrecision = "rooftop" | "interpolated" | "center";

export interface TaskWorkSite {
  /** Dirección normalizada por el geocodificador, para enseñar qué se entendió. */
  street: string;
  geo: {lat: number; lng: number};
  /** Radio de la valla. Lo rellena el servidor si el cliente lo omite (§2). */
  radiusMeters: number;
  timeZone?: string;
  postalCode?: string;
  country?: string;
  placeId?: string | null;
  /** `approximate` nunca se guarda: se rechaza en el alta (§2). */
  precision?: WorkSitePrecision;
}

export interface Task {
  // ...
  workSite?: TaskWorkSite;
}
```

**No hay colección nueva.** Es un subdocumento dentro de `entities/{entityId}/tasks/{taskId}`,
que ya existe. Coste por trabajo: cero documentos, cero índices. Ése es el punto entero del
[ADR-007](../adr/ADR-007-geocerca-en-la-tarea.md) — dar un punto en el mapa sin dar de alta un
centro de trabajo.

---

## 2. Alta y edición del `workSite`

Aceptado en `POST /` y `PATCH /:taskId`, solo para actores que ya pueden gestionar la tarea
(`canManageTask`). El front usa el **mismo buscador de direcciones que el alta de centros**:
`POST /api/v1/checkinbiz/geo` con `action: "autocomplete"` y `action: "placedetails"`.

El servidor normaliza y admite dos formas:

- **Con `placeId`** (camino normal desde el front) → resuelve con `placeDetails`.
- **Con `street` sin coordenadas** → resuelve con `geocodeAddress` de `@encodebiz/shared`.
- **Con `geo` explícito** → se acepta tal cual; `precision` se marca como la que venga o se
  omite.

**Reglas de validación:**

| Regla | Código |
|---|---|
| `geo.lat` ∈ [-90, 90] y `geo.lng` ∈ [-180, 180], numéricos finitos | `task/worksite_invalid` |
| `radiusMeters` numérico > 0 si viene | `task/worksite_invalid` |
| La geocodificación no resuelve nada | `task/worksite_invalid` |
| `precision === "approximate"` | `task/worksite_imprecise` |

El rechazo de `approximate` no es celo: lo avisa el propio `packages/shared/src/maps/geocoding.ts`.
Una valla de 200 m alrededor del centroide de una ciudad **parece** una dirección correcta y
alguien la dará por buena; es el fallo que nadie detecta hasta que un empleado abre la tarea
desde su casa.

**Radio por defecto**, cuando el cliente no manda `radiusMeters`:
`branch.ratioChecklog ?? 150`. Se hereda el de la sucursal para que el cliente no tenga que
decidir dos veces lo mismo, y 150 m es el último recurso si la sucursal tampoco lo tiene
configurado.

**Editar el `workSite` de una tarea ya iniciada está permitido** y no reescribe nada de lo ya
registrado: la bitácora está congelada (§5).

Para quitar la valla de una tarea: `PATCH` con `workSite: null` → se borra el campo
(`FieldValue.delete()`, igual que ya se hace con `scheduledStartAt`).

---

## 3. Precondición: jornada abierta

### La regla ya existe — en el cliente

`checkbiz360/lib/features/task/presentation/pages/task_detail_page.dart` calcula:

```dart
final hasStartedWorkday = attendanceStatus == AttendanceStatus.working ||
    attendanceStatus == AttendanceStatus.onBreak;
```

y si es falso oculta los botones de **iniciar** y **completar**, mostrando en su lugar un aviso
con un atajo a la pantalla de fichaje. Es decir: el comportamiento de producto ya está decidido
y desplegado.

Lo que **no** existe es la comprobación en la API. Este TDR no inventa la regla: la baja al
servidor, con la misma semántica y el mismo alcance, para que no dependa de la versión de la app
ni de que el cliente sea el nuestro.

**Semántica idéntica a la de la app:** `onBreak` cuenta como jornada abierta. Sale gratis con la
consulta de abajo, porque un `restin` no cierra el check-in.

**Alcance idéntico al de la app:** solo `in_progress` y `completed`.

| Endpoint | Cuándo |
|---|---|
| `PATCH /:taskId/status` | `in_progress` y `completed` |

**Notas y evidencias quedan fuera a propósito.** La app ofrece subir la evidencia justamente
como remedio cuando falta para poder completar (`isMissingRequiredEvidence`); bloquear la subida
sin jornada rompería ese flujo y sería una regresión, no un endurecimiento.

**No** afectados, por tanto: crear, asignar/desasignar, notas, evidencias, validar, rechazar,
cancelar y valorar.

### Lectura

Va a `@encodebiz/shared`, **no** duplicada en `tasks` — el dominio checkbiz vive en shared y no
se vuelve a copiar. Se añade una lectura mínima que no arrastra toda la entidad `CheckLog`:

```ts
// packages/shared/src/checkbiz/repositories/FirestoreWorkSessionRepository.ts
export interface OpenWorkSession {
  checkinId: string;
  branchId: string;
  timestamp: Date;
  deadline?: Date;
}

findOpenWorkSession(entityId: string, employeeId: string): Promise<OpenWorkSession | null>
```

Consulta, **una sola lectura**:

```
entities/{entityId}/checklogs
  .where("employeeId", "==", employeeId)
  .where("type", "==", "checkin")
  .orderBy("timestamp", "desc")
  .limit(1)
```

y se evalúa **en memoria**: `status === "valid"` && `closed !== true` &&
(`deadline` ausente o `deadline > now`).

Por qué en memoria y no en la query: evita índices compuestos nuevos y deja el filtro del
`deadline` fuera de un rango que obligaría a otro índice. El índice
`[employeeId ASC, type ASC, timestamp DESC]` sobre `checklogs` **ya existe** en
`encodeBiz-SAAS/firestore.indexes.json`; esto no añade ninguno.

Por qué se filtra por `type == "checkin"` y no se mira simplemente el último fichaje: durante un
descanso el último registro es un `restin`/`restout` y la jornada sigue abierta. Filtrando por
check-in, el `onBreak` de la app y el servidor coinciden sin código extra.

Por qué se mira `status === "valid"`: un check-in `failed` —fuera de radio, fuera de horario— no
abre jornada. Y `closed` se borra (`FieldValue.delete()`) cuando un fichaje se rechaza en
`updateChecklog`, de ahí que se compruebe `!== true` y no `=== false`.

Por qué se mira el `deadline`: es el límite que ya usa la plataforma para dar una jornada por
incompleta. Sin él, un check-in olvidado de hace tres semanas contaría como sesión abierta.

### Aplicación

```ts
const needsOpenSession = !!actor.employeeId && !actor.isEntityWriter;
```

- **Sujeto a la regla:** cualquiera que opere con su ficha de empleado, incluidos supervisores
  operando su propia tarea asignada. Si trabaja, ficha.
- **Exento:** el actor de back office con permiso de escritura sobre la entidad
  (`isEntityWriter`), que puede no ser empleado y no tiene jornada que abrir. El panel debe
  poder cerrar una tarea de alguien que ya se fue a casa.

Sin jornada abierta → `400 task/no_open_session`. La app no debería verlo nunca —ya lo impide
antes—, pero es la respuesta correcta para cualquier cliente que se salte el paso.

---

## 4. Geocerca al iniciar

Contrato ampliado, **aditivo**:

```
PATCH /api/v1/tasks/:taskId/status
body: { entityId, status: "in_progress" | "completed" | ..., geo?: { lat, lng } }
```

Orden exacto de comprobaciones para `in_progress`:

1. Tarea existe → `404 task/not_found` *(ya existía)*
2. Actor resuelto y `canOperateAssignedTask` → `403 task/unauthorized` *(ya existía)*
3. **Jornada abierta** (§3) → `400 task/no_open_session`
4. **Geocerca**, solo si `task.workSite` existe:
   - falta `geo` en el body → `400 task/geo_required`
   - `getDistanceInMeters(geo, workSite.geo) > workSite.radiusMeters` →
     `400 task/out_of_worksite`, con `{distanceMeters, allowedRadiusMeters}` en la respuesta.
     **El estado no cambia**, y el intento queda registrado (§5).
5. Transición, sellado de `startedAt` y actividad — exactamente como hoy.

**Tarea sin `workSite`:** el paso 4 no se ejecuta. Comportamiento idéntico al actual. La valla
que le corresponde es la de la sucursal, y ya la aplicó el check-in que el paso 3 exige.

**Al completar (`completed`)** la valla se **mide pero no bloquea**: se guarda la distancia y
se marca `withinWorkSite: false` si procede. El "empezar" lo pulsa quien acaba de llegar; el
"terminar" lo pulsa medio mundo ya montado en la furgoneta. Bloquear el cierre no evita nada y
genera llamadas a soporte.

**`enableRemoteWork` y `disableRatioChecklog` no aplican aquí.** Rigen el fichaje, que es su
sitio. Una tarea con dirección explícita tiene valla explícita.

---

## 5. Bitácora

Se aprovecha `TaskActivity.metadata`, que ya es `Record<string, any>` y hoy va vacío en estas
transiciones. Se añade un tipo de actividad al union de `TaskActivity`:

```ts
type: "..." | "start_rejected"
```

Metadatos escritos en `started`, `completed` y `start_rejected`:

```ts
metadata: {
  geo: {lat, lng},
  workSite: {geo: {lat, lng}, radiusMeters},   // copia, no referencia
  distanceMeters: number,
  withinWorkSite: boolean,
  openSession: {checkinId, branchId},
}
```

**El `workSite` se copia, no se referencia.** Mismo motivo por el que el fichaje congela
`scheduleDay` en su `metadata`, y está escrito en `CheckLog.ts`: si mañana alguien corrige la
dirección del trabajo, lo de ayer no puede rejuzgarse con una valla que entonces no existía.

Registrar también los intentos rechazados (`start_rejected`) es el equivalente al
`status: "failed"` del checklog: sin ese rastro, un empleado que no consigue abrir la tarea es
indistinguible de uno que no lo intentó.

---

## 6. Códigos de error nuevos

| Código | HTTP | Significado |
|---|---|---|
| `task/no_open_session` | 400 | El empleado no tiene jornada abierta |
| `task/geo_required` | 400 | La tarea tiene `workSite` y el body no trae `geo` |
| `task/out_of_worksite` | 400 | Fuera del radio del lugar de trabajo |
| `task/worksite_invalid` | 400 | `workSite` mal formado o dirección no resoluble |
| `task/worksite_imprecise` | 400 | La geocodificación devolvió precisión `approximate` |

Se usa 400 en todos, por coherencia con el resto del servicio —`task/evidence_required` ya es
una precondición fallida devuelta como 400—, no con la ortodoxia REST.

---

## 7. Casos borde

- **Varios asignados a la misma tarea.** Cada uno valida su propio inicio contra la misma valla
  y necesita su propia jornada abierta. `assignment.startedAt` ya es por empleado, así que no
  cambia nada estructural.
- **Reapertura a `assigned`/`draft`.** `startedAt`/`completedAt` se borran como hoy; el
  `workSite` se conserva. La bitácora anterior permanece.
- **GPS denegado en el móvil.** El body llega sin `geo` → `task/geo_required`. Es la misma
  situación que un fichaje sin coordenadas, que también falla; la app debe pedir el permiso
  antes de ofrecer el botón.
- **Tarea sin `workSite`.** Nada cambia salvo la precondición de jornada.
- **Empleado con jornada abierta en otra sucursal.** Se acepta. La sesión abierta es del
  empleado, no de la sucursal, y el trabajo a domicilio es justamente el caso en que no
  coinciden. El `branchId` de la sesión queda en la bitácora para quien quiera mirarlo.
- **Check-in `pending-employee-validation`.** No abre jornada: solo `valid` cuenta.

---

## 8. Qué NO cambia

- `services/checkinbiz` entero. Ni una línea.
- El contrato de `createChecklog`, sus códigos y su geocerca de sucursal.
- Las 14 rutas existentes de `tasks` en todo lo que no sea lo descrito arriba.
- Las tareas ya creadas: sin `workSite`, siguen comportándose igual salvo por la precondición
  de jornada.

---

## 9. Fuera de alcance (deuda registrada)

- **Medición del desplazamiento.** El modelo ya lo permite —es el hueco entre `completedAt` de
  una tarea y `startedAt` de la siguiente dentro de la misma jornada— pero el cálculo y su
  presentación en informes/analytics no entran aquí.
- **Catálogo de lugares reutilizables** por entidad, para clientes que repiten dirección. No
  hace falta para arrancar y se decidirá con uso real delante.
- **Señal geográfica en `taskSignals`** (dispersión, tiempo muerto) para merlin y analytics.
- **Migración de `CheckLog` a `@encodebiz/shared`.** Aquí solo se promueve la lectura de sesión
  abierta; la entidad y su repositorio siguen en `checkinbiz`.

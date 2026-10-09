# Presencia — «Mi equipo» en la app · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Fichajes (checklogs) × Calendario (disponibilidad) → Presencia · checkbiz360 — «Mi equipo»
**Fecha de inicio:** 2026-10-09
**Estado:** Estudio cerrado · **sin planificar** · entra en una iteración posterior, después de inventario
**Autor:** Jose Acevedo

---

## Contexto y motivación

Un supervisor o un gerente en la obra necesita saber, con el móvil en la mano, con quién cuenta
hoy: quién está, quién no ha fichado todavía y quién no iba a venir. Hoy esa pregunta no la
responde nadie en la plataforma, y el estudio del 2026-10-09 lo comprobó pieza a pieza:

- **El panel no es su herramienta.** El backoffice lista las empresas de un usuario por sus
  asientos de colaborador (`user_entity_roles`, roles `owner` y `admin`;
  `encodebiz-front-saas/src/services/core/entity.service.ts`, `fetchUserEntities`). Una
  responsabilidad de supervisor o manager sobre una sucursal, por sí sola, no abre el panel.
  La documentación de cliente describe al supervisor dentro del panel, pero eso sólo ocurre si
  además tiene asiento.
- **Y aunque entrara, el panel no lo dice.** La pestaña «Asistencia» construye las jornadas del
  día **a partir de los fichajes** (`attendanceSummary.ts`, `buildWorkSessionSummaries`). Quien
  no fichó no genera fichaje, así que no aparece en ninguna fila. El tablero de disponibilidad
  hace lo contrario: dice quién debería trabajar, sin mirar si vino.
- **La app sólo sabe de uno mismo.** El estado de jornada se deriva del último fichaje propio
  (`attendanceStateProvider`), y la única lectura de fichajes es la del empleado autenticado.

Se pensó primero como «enseñar en la app lo que ya enseña el panel». No es eso: es responder
una pregunta nueva, **quién debería estar y no está**, cruzando dos cosas que hoy viven
separadas.

## Principio de diseño

> **La presencia no es un dato nuevo: es el cruce de lo previsto (el calendario) con lo real
> (los fichajes). Lo cruza el servidor, una vez, con la lógica de jornada que ya tiene el
> panel; la app lo pinta y nunca inventa un número.**

Es el mismo principio que la disponibilidad ([disponibilidad/README](../disponibilidad/README.md)):
allí el cruce en el navegador funcionó, y se tuvo que reescribir en el servidor. Aquí no se
repite el rodeo. Razonamiento en [ADR-001](./adr/ADR-001-el-cruce-lo-hace-el-servidor.md).

## Alcance

**Dentro:**

- Una lectura nueva, de sólo lectura, que para una sucursal y un día devuelve a cada persona
  prevista con su estado de presencia, y a las no previstas con su motivo.
- Promover a `@encodebiz/shared` la construcción de jornadas que hoy vive en el front del panel,
  para que la usen la lectura nueva y el propio panel.
- En la app, la feature «Mi equipo»: entrada en el menú, tarjeta en la home y pantalla, sólo para
  supervisor o superior y sólo con la jornada iniciada.
- Las acciones que ya existen en el servidor, enlazadas desde la fila: solicitar jornada manual
  y llamar.
- Un aviso a los supervisores de la sucursal cuando alguien previsto sigue sin fichar, apoyado
  en el planificador de recordatorios que ya corre.

**Fuera:**

- Turno por día y sucursal. Sin él, quien pertenece a dos centros «debería estar» en los dos
  (sobreconteo conocido, [TDR-001 §2.2 de disponibilidad](../disponibilidad/tdr/TDR-001-calculo-de-disponibilidad.md)).
  La presencia lo mitiga con `other_branch`, no lo resuelve.
- Los equipos del módulo `teams`. Son plantillas de dotación, no presencia; la responsabilidad
  aplicada no guarda de qué equipo salió ([equipos/README](../equipos/README.md)). «Equipo» aquí
  es la plantilla de la sucursal.
- Cerrar las reglas de Firestore. Es deuda declarada y condiciona el diseño, pero es otro
  trabajo.
- Histórico. Esto es el día de hoy; el pasado es del panel y de analytics.

---

## Lo que hay hoy (As-Is)

Todo lo de abajo está verificado contra el código el 2026-10-09.

### Quién debería estar: la disponibilidad ya lo dice

`GET /api/v1/checkinbiz/calendar/availability/day?entityId&date&groupId` devuelve, para una
sucursal y un día, `available[]` con sus turnos y `unavailable[]` con `reason` ∈
`noShift | holiday | absence | employeeStatus`. Contrato completo en
[disponibilidad/03](../disponibilidad/03_contratos-api.md).

- Vive en el contenedor `checkinbiz`:
  `services/checkinbiz/src/interfaces/http/calendar/availability.controller.ts`, caso de uso
  `ResolveAvailabilityDayUseCase` en `packages/shared/src/calendar/resolveAvailability.usecase.ts`.
- **Permisos por nivel** con `resolveActorScope` (`packages/shared/src/checkbiz/auth/resolveActorScope.ts`):
  `owner` y `manager` ven toda la entidad, `supervisor` sólo sus sucursales, `worker` recibe
  `403`. Es exactamente el alcance que necesita «Mi equipo».
- Sólo Firebase ID token. El JWT de empleado de la app no se acepta.
- Verificado en dev el 2026-09-02 y en pantalla el 2026-09-03. **En producción no está
  confirmado**: el contenedor es el mismo, pero una llamada sin token devuelve `401` tanto si la
  ruta existe como si no, porque el middleware de auth va antes del router. Hay que comprobarlo
  con un token real antes de la Fase 1.

### Quién está: los fichajes, y la lógica de jornada que sólo tiene el panel

`entities/{entityId}/checklogs`, con `branchId`, `employeeId`, `type`
(`checkin | checkout | restin | restout`), `status`, `timestamp`, `checkin` (referencia al
checkin de la jornada), `closed`, `deadline` y `metadata.tz`.

- Índices compuestos declarados en `encodeBiz-SAAS/firestore.indexes.json` por
  `(branchId, timestamp)` en los dos sentidos, que es la consulta que hace falta. El json no
  coincide necesariamente con lo desplegado: comprobar con `gcloud` antes de contar con él.
- La lógica que convierte fichajes en jornadas —estado `working | on_break | completed |
  incident`, pausas, minutos trabajados e incidencias `missing_checkin | open_break |
  invalid_sequence | multiple_checkouts | cross_branch_session | incomplete_workday |
  pending_validation`— está **sólo** en
  `encodebiz-front-saas/src/app/main/[entityId]/checkinbiz/attendance/attendanceSummary.ts`.
  No existe en `shared`. Ancla cada jornada en su checkin, resuelve el día en la zona del
  fichaje (`metadata.tz`) y trata un `failed` como un intento que no ocurrió.
- Para pintar nombres, el panel hace una lectura de empleado **por fichaje** (`enrichLogs`),
  con caché en memoria. Es el mismo patrón N+1 que la disponibilidad retiró.
- El saneador horario (`sanitizerChecklog`, cada hora) marca `incomplete_workday` los checkins
  con `deadline` vencido y sin cierre, y crea un checkout sintético
  `incomplete_workday_<checkinId>`. El panel operativo tiene **abierta** la semántica de ese
  estado ([panel-operativo-v2/README](../panel-operativo-v2/README.md)): la presencia lo
  enseña como «jornada sin cerrar» y no juzga.

### Quién no ha fichado: el planificador ya lo sabe, y no se lo dice a nadie

`encodeBiz-SAAS/functions/src/services-saas/checkinbiz/firebase-entry-schedule/`:

- `planifierNotificationWorker` (cada noche) crea un `EmployeePlanifier` por persona, turno y
  tipo para el día siguiente, con avisos a −5, 0 y +5 minutos de la hora del turno.
- `employeePlanifierWorker` (cada cinco minutos) ejecuta los vencidos.
  `ExecuteEmployeePlanifierController` resuelve el calendario del día, **busca un fichaje válido
  del tipo en el día** y, si no lo hay, manda `checkin_reminder` por push y WhatsApp **al
  empleado**.
- Es decir: a +5 minutos del turno, el sistema ya sabe quién no ha fichado. Esa señal muere
  ahí. Nadie la convierte en aviso al supervisor.
- Limitación: sólo resuelve la sucursal cuando el empleado tiene **exactamente una** activa;
  con varias, planifica con el horario de la entidad y `branchId` vacío.

Los avisos a supervisores sí existen para otras cosas: `distance_violation`, `ratio_anomaly`,
`pattern_mismatch_*` y `out_of_day_window` van a las responsabilidades de nivel 2 de la
sucursal ([modulos/notificaciones](../../modulos/notificaciones.md)). La resolución de
destinatarios está hecha.

### La app: todo lo que necesita para decidir ya está

| Pieza | Dónde | Qué da |
|---|---|---|
| Rol en la sucursal seleccionada | `lib/features/attendance/presentation/providers/responsibility_provider.dart` | `responsibility.level` |
| Alcance de sucursales por rol | `taskCreatableBranchScopeProvider` en `lib/features/task/presentation/providers/task_lookup_provider.dart` | manager → sin restricción; supervisor → conjunto de `branchId` |
| Jornada iniciada | `attendanceStateProvider.status` ∈ `working, onBreak` | La misma puerta que usa la tarjeta de tareas de hoy |
| Menú | `_toolsSection` en `lib/features/attendance/presentation/widgets/attendance_drawer.dart` | «Herramientas»: Historial, Documentos y Mi material (condicional) |
| Rutas empujadas fuera del shell | `documentsRoute`, `myEquipmentRoute` en `lib/presentation/router/app_router.dart` | El patrón para una pantalla nueva |
| Firebase ID token hacia la API | `lib/features/signature/data/datasources/signing_remote_datasource.dart` | La firma ya lo usa; fichajes y tareas van con el JWT de empleado |
| Invalidación en logout | `lib/features/notifications/presentation/providers/logout_invalidation_provider.dart` | Donde hay que registrar los providers nuevos |

Lo que la app **no** tiene, y no debe fabricarse: nombres de otros empleados (hoy sólo el
índice de búsqueda para tareas), fichajes ajenos y una copia de la lógica de jornada.

### Lo que condiciona el diseño

- **Reglas de Firestore abiertas.** `encodebiz-api/firestore.rules` conserva un comodín hasta
  2030-01-20. Hoy la app *podría* leer todos los fichajes de la sucursal directamente. El día
  que se cierre, cualquier cruce hecho en el cliente deja de funcionar sin avisar.
- **Sin turno por día y sucursal.** Quien está en dos centros aparece previsto en los dos.
- **`incomplete_workday` sin semántica cerrada.**
- **Teléfono.** Para «llamar» hace falta el teléfono del empleado, que es un dato personal más
  en la respuesta.

---

## Arquitectura objetivo (To-Be)

### Dónde se cruza: en el servidor

Una ruta nueva de sólo lectura que compone dos cosas que ya existen: el desglose del día de la
disponibilidad y los fichajes del día de la sucursal. Ver
[ADR-001](./adr/ADR-001-el-cruce-lo-hace-el-servidor.md).

### Dónde vive: decisión abierta

Lo natural es `checkinbiz`, junto a la disponibilidad, porque es una lectura derivada de dos
módulos del núcleo. Choca con el
[ADR-003 de salida del monolito](../salida-del-monolito/adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md):
*al núcleo no vuelve a entrar nada*. Las opciones y la recomendación, en
[ADR-002](./adr/ADR-002-donde-vive-la-presencia.md). El contrato de abajo no depende de la
respuesta; sólo cambia el prefijo de la ruta.

### La lógica de jornada se promueve a `shared`

`buildWorkSessionSummaries` y sus reglas se mueven a `@encodebiz/shared` tal cual, con sus
pruebas. El panel pasa a importarlas de ahí —y con ello gana las filas «sin fichaje» que hoy no
puede enseñar— y la lectura nueva las reusa. Misma regla que
[checklogs-http/ADR-003](../checklogs-http/adr/ADR-003-promocion-a-shared-sin-tercera-copia.md):
lo común se promueve, no se copia una tercera vez.

### Plan de lectura

El desglose del día ya cuesta cinco idas y vueltas independientes de la plantilla
([TDR-001 §1 de disponibilidad](../disponibilidad/tdr/TDR-001-calculo-de-disponibilidad.md)).
La presencia añade:

| Paso | Lectura | Round trips |
|---|---|---|
| 6 | `checklogs` con `branchId == X` y `timestamp` en la ventana del día | 1 |
| 7 | Sólo para quien quedó `no_log`: `checklogs` con `employeeId in (…)` y la misma ventana, en bloques de 30 | ⌈noLog / 30⌉, normalmente 0 ó 1 |

El paso 7 es lo que permite decir `other_branch` sin traerse los fichajes de toda la entidad:
sólo hace falta mirar en otros centros a quien **no** ha fichado en éste.

**La ventana del día** es el día civil en la zona de la sucursal, como hace
`dailyCollectorData`, más la cola de una jornada que cruza la medianoche. Cada fichaje se
asigna al día de su checkin en `metadata.tz`, igual que el panel.

**Si cualquier lectura falla, la petición falla.** Nunca una lista parcial: una persona que
falta en la lista es alguien a quien el supervisor no va a echar en falta.

### Frontera: quién decide qué

| Decisión | Dónde | Por qué |
|---|---|---|
| Quién está previsto y por qué no el resto | Backend | Ya resuelto por la disponibilidad |
| Estado de jornada e incidencias | Backend | Una sola copia de la regla, en `shared` |
| Si fichó en otra sucursal | Backend | Necesita leer fichajes ajenos a la sucursal |
| Minutos respecto a la hora prevista | Backend | Es un hecho, con la zona correcta |
| Si eso es «retraso», y a partir de cuánto | **App** | Es lectura, como los colores de la disponibilidad |
| Orden, agrupación, búsqueda | App | Presentación sobre una lista ya calculada |
| Teléfono y llamada | **Abierto** | Ver decisiones |

---

## Contrato de API

**Auth:** `Authorization: Bearer <Firebase ID token>`. El JWT de empleado no se acepta.
**Permisos:** `resolveActorScope`. `owner`/`manager` cualquier sucursal de la entidad;
`supervisor` sólo las suyas; `worker` → `403`. Un trabajador no tiene por qué saber quién ha
fichado y quién no.
**Sólo lectura.** No escribe nada.

El prefijo de la ruta depende de [ADR-002](./adr/ADR-002-donde-vive-la-presencia.md). Con la
opción recomendada:

```
GET /api/v1/checkinbiz/checklogs/presence
```

### Query

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `entityId` | sí | Entidad |
| `branchId` | sí | Sucursal. Fuera del alcance del actor → `403` |
| `date` | no | `YYYY-MM-DD` en la zona de la sucursal. Por defecto, hoy |

### `200` — `presence/resolved`

```json
{
  "code": "presence/resolved",
  "data": {
    "date": "2026-10-09",
    "timezone": "Europe/Madrid",
    "branch": { "id": "bcn-norte", "name": "Obra Norte" },
    "summary": { "expected": 9, "present": 6, "noLog": 2, "finished": 1, "plannedAbsent": 3 },
    "expected": [
      {
        "employeeId": "emp_123",
        "fullName": "Ana Ferrer",
        "shifts": [{ "start": { "hour": 8, "minute": 0 }, "end": { "hour": 16, "minute": 0 } }],
        "presence": "working",
        "firstCheckinAt": "2026-10-09T06:04:00Z",
        "lastMovementAt": "2026-10-09T06:04:00Z",
        "lastMovementType": "checkin",
        "minutesFromShiftStart": 4,
        "incidents": []
      },
      {
        "employeeId": "emp_456",
        "fullName": "Luis Ruiz",
        "shifts": [{ "start": { "hour": 8, "minute": 0 }, "end": { "hour": 16, "minute": 0 } }],
        "presence": "no_log",
        "minutesFromShiftStart": 47
      },
      {
        "employeeId": "emp_789",
        "fullName": "Pablo Mora",
        "shifts": [{ "start": { "hour": 8, "minute": 0 }, "end": { "hour": 16, "minute": 0 } }],
        "presence": "other_branch",
        "otherBranch": { "id": "bcn-sur", "name": "Obra Sur" },
        "firstCheckinAt": "2026-10-09T05:58:00Z"
      }
    ],
    "unavailable": [
      { "employeeId": "emp_012", "fullName": "Marta Cano", "reason": "absence", "reasonName": "Vacaciones", "reasonSource": "employee" },
      { "employeeId": "emp_345", "fullName": "Nadia Sáez", "reason": "noShift" }
    ]
  }
}
```

- `expected` son los `available` de la disponibilidad, enriquecidos con el fichaje.
  `unavailable` llega **tal cual** del desglose del día, con su `reason` y su `reasonSource`.
- `summary.present` = `working + on_break`. `summary.plannedAbsent` = `unavailable.length`.
  `expected.length === summary.expected`.
- `minutesFromShiftStart` va siempre que haya turno: contra `firstCheckinAt` si fichó, contra
  *ahora* si no. Positivo es tarde. Es un hecho; la etiqueta es de la app.
- `shifts` estructurado, no formateado. Los instantes en ISO UTC; la app los pinta en
  `timezone`.
- `incidents` reutiliza los códigos de `attendanceSummary.ts`. Sólo los que no son ya el
  propio `presence` (por ejemplo `cross_branch_session`, `open_break`, `multiple_checkouts`).

| `presence` | Significado |
|---|---|
| `no_log` | Previsto hoy y sin ningún fichaje en ningún centro |
| `working` | Checkin válido sin checkout |
| `on_break` | Pausa abierta |
| `finished` | Checkin y checkout válidos |
| `pending_validation` | Jornada manual pendiente de que el trabajador la apruebe |
| `incomplete` | Marcada `incomplete_workday` por el saneador. Se enseña como «jornada sin cerrar»; no se juzga |
| `other_branch` | Sin fichaje aquí, pero hoy fichó en otra sucursal suya |

### Errores

| HTTP | `code` | Cuándo |
|---|---|---|
| `400` | `presence/missing_params` | Falta `entityId` o `branchId` |
| `400` | `presence/invalid_date` | `date` mal formada |
| `403` | `presence/forbidden` | Nivel insuficiente, o `branchId` fuera del alcance |
| `404` | `presence/branch_not_found` | La sucursal no es de la entidad |

Los códigos se dan de alta en
[90-codigos-de-error-completos](../../Clients/14-referencia/90-codigos-de-error-completos.md).
Si [ADR-002](./adr/ADR-002-donde-vive-la-presencia.md) acaba en otro módulo, el prefijo cambia
con él.

---

## Integración: app móvil

**Repo:** `checkbiz360` · **Feature:** `lib/features/team/` con `domain/`, `data/`,
`presentation/`, según la estructura objetivo de [capas/app-movil](../../capas/app-movil.md).

### Cuándo se ve

Supervisor o superior **en la sucursal seleccionada** y **jornada iniciada**
(`AttendanceStatus.working` u `onBreak`). Es la regla que pidió producto y la misma puerta que
la tarjeta de tareas de hoy. Queda abierto si el menú debería verse también sin fichar
(ver decisiones): un encargado puede querer saber quién falta antes de fichar él.

- **Menú.** Entrada «Mi equipo» en «Herramientas», entre Historial y Documentos, condicional.
- **Home.** Debajo de la tarjeta de tareas de hoy, una tarjeta con el resumen —presentes de
  previstos, sin fichaje— que abre la pantalla. Sin jornada iniciada no se renderiza **ni
  dispara la llamada**, como la de tareas.
- **Ruta.** `teamRoute = '/team'`, empujada fuera del shell como `/documents` y
  `/my-equipment`. Prefijo privado en `_isPrivateRoute`.

### La pantalla

- Cabecera con `HeaderTitle` y, si el actor ve más de una sucursal, un `AppSelectField`
  limitado a su alcance; por defecto la seleccionada.
- Cuatro cifras arriba: previstos, presentes, sin fichaje, ausencias previstas.
- Tres bloques, en este orden: **Sin fichaje** (lo que el supervisor viene a mirar), **En el
  centro** (working, on_break, finished, incomplete, pending_validation), **No previstos**
  (los `unavailable`, con su motivo traducido).
- Fila: nombre, turno, chip de estado, hora del último movimiento en la zona de la sucursal.
  `other_branch` lleva el nombre del otro centro. En «sin fichaje», los minutos desde la hora
  prevista; la etiqueta «retraso» sólo por encima de un umbral, que es decisión de la app.
- `LoadingPlaceholder` al cargar. Si la llamada falla: mensaje y **lista vacía**, nunca cifras.

### Datos

- Datasource remoto con **Firebase ID token**, como `signing_remote_datasource.dart`, no con el
  JWT de empleado. Es la primera lectura de la app que llama a la API con él; conviene un
  helper compartido.
- Provider `autoDispose` por `(branchId, date)`. Refresco al abrir, al volver a primer plano,
  con pull-to-refresh y cada pocos minutos mientras la pantalla está visible.
- Opcional: un `snapshots()` sobre los fichajes del día de la sucursal **sólo como disparador
  de recarga**, igual que `equipmentDeliveryNoticesProvider` recarga «Mi material». Si las
  reglas se cierran, el disparador se apaga y el refresco periódico sigue; la pantalla no miente.
- Registrar los providers nuevos en `invalidateUserScopedProviders`.

### Acciones (fase 2b)

- **Solicitar jornada manual** desde una fila `no_log`: `POST /api/v1/checkinbiz/checklogs/manual-request`,
  Modo A, con Firebase ID token; el controlador ya exige nivel ≥ supervisor en la sucursal
  ([modulos/checklog §3](../../modulos/checklog.md)). El trabajador la aprueba desde su app como
  hoy. Al volver, se vuelve a pedir la presencia, no se parchea en memoria.
- **Cerrar jornada** desde una fila `working` con la jornada de ayer abierta: Modo B, mismo
  endpoint.
- **Llamar.** Depende de que la respuesta lleve teléfono (decisión abierta).

### Textos

Sin l10n no entra nada. Y el tono importa más aquí que en ninguna otra pantalla, porque habla
de personas que no están:

- **«Sin fichaje», nunca «ausente» ni «falta».** Alguien sin fichaje puede estar en otro
  centro, sin cobertura o con el GPS caído. El panel operativo lo dejó escrito en su
  [ADR-005](../panel-operativo-v2/adr/ADR-005-ausencia-de-evidencia-no-es-evidencia-negativa.md):
  la ausencia de evidencia no es evidencia negativa.
- Las ausencias del calendario se llaman por su nombre (`reasonName`): «Vacaciones», «Diada».
- «Jornada sin cerrar» para `incomplete`, sin adjetivos.

## Integración: panel

Con la lógica en `shared`, la pestaña «Asistencia» puede consumir la misma lectura y enseñar
por fin las filas «sin fichaje» del día. Es un beneficio lateral, no un requisito; se decide
cuando toque.

## Avisos a supervisores (fase 3)

El planificador ya detecta a +5 minutos que alguien previsto no ha fichado. Extenderlo:

- Cuando `ExecuteEmployeePlanifierController` agota los avisos de `checkin` sin fichaje —o a
  +N minutos configurables—, un push `team_missing_checkin` a las responsabilidades de nivel
  ≥ 2 de la sucursal, con `data.screen = team` y `branchId`, resolviendo destinatarios como
  `distance_violation`.
- Agrupado: un aviso por sucursal y franja, no uno por persona. Treinta avisos a las 8:05 es
  ruido que enseña a ignorar la campana.
- Limitación heredada: el planificador sólo conoce la sucursal cuando el empleado tiene una.
  Con varias, el aviso no sabe a qué supervisores ir. Se documenta y se acepta hasta que
  exista turno por día y sucursal.
- Antes de encenderlo, cerrar la semántica de `incomplete_workday` del panel operativo: el
  aviso no debe acusar una jornada que simplemente sigue abierta.

---

## Fases

Ninguna arranca hasta que inventario esté cerrado. El orden es de dependencias, no de
calendario.

| Fase | Qué | Verificación | Depende de |
|---|---|---|---|
| **0** | Cerrar [ADR-002](./adr/ADR-002-donde-vive-la-presencia.md). Comprobar en producción la ruta de disponibilidad con un token real y el índice `(branchId, timestamp)` con `gcloud` | Las dos comprobaciones por escrito aquí | — |
| **1** | `shared`: promover `buildWorkSessionSummaries` con pruebas; caso de uso de presencia; ruta; códigos de error; spec en la suite de QA | Para la entidad de pruebas, `expected` coincide uno a uno con `available` del desglose del día, y los estados con lo que pinta «Asistencia» para los mismos fichajes | 0 |
| **2** | App: feature `team`, menú, tarjeta, pantalla, l10n, invalidación en logout | En dev, con la entidad `Wl8ZCvpdmIXzEE0mhT7W`: un supervisor ve su sucursal y nada más; un worker no ve la entrada; un manager cambia de sucursal | 1 |
| **2b** | Acciones: jornada manual y cierre desde la fila; llamada si se decide el teléfono | Una solicitud creada desde la app aparece pendiente en la app del trabajador | 2 |
| **3** | Aviso agrupado a supervisores desde el planificador; deep link a «Mi equipo» | Un previsto sin fichaje a +N dispara un push al supervisor y abre la pantalla | 2, semántica de `incomplete_workday` |
| **Después** | Vista de gerente: cifras por centro para toda la entidad, sobre `GET /availability` más una agregación de presencia por sucursal | — | 1 |

Cadena de siempre: `develop → staging → main`, API primero. La app necesita release en
tiendas: la fase 2 se planifica con una.

## Decisiones abiertas

1. **Dónde vive la lectura.** [ADR-002](./adr/ADR-002-donde-vive-la-presencia.md). Bloquea
   la fase 1.
2. **Umbral de «retraso».** Si se etiqueta en la app, con cuántos minutos, y si el umbral es de
   la app o un parámetro de la sucursal (`advance.notifyBeforeMinutes` cubre la entrada
   anticipada, no el retraso).
3. **Menú sólo con jornada iniciada o siempre para supervisor+.** Producto pidió lo primero.
   El coste de lo segundo es nulo; el riesgo, que el encargado consulte sin haber fichado él y
   el supervisor de arriba lo lea al revés.
4. **Teléfono en la respuesta.** Necesario para «llamar»; dato personal más que viaja al móvil
   del supervisor. Alternativa: no devolverlo, y que «llamar» pase por la incidencia de soporte.
5. **Qué ve el gerente.** `resolveActorScope` le da toda la entidad. ¿Lista por sucursal con
   cifras, o la misma pantalla con selector?

## Riesgos

- **Confianza en un número.** Un supervisor que ve «6 de 9» y actúa sobre ello. Por eso la
  lista nunca es parcial y el error se enseña como error.
- **Sobreconteo multi-sucursal.** `other_branch` lo tapa para quien fichó en otro centro; a
  quien no fichó en ninguno se le sigue esperando en los dos. Se documenta en pantalla con el
  nombre del otro centro cuando se sabe.
- **Dependencia de reglas abiertas en el disparador opcional.** Diseñado para degradar a
  refresco periódico, no para fallar.
- **Datos de personas.** La respuesta lleva nombres y estados de toda la plantilla de la
  sucursal al móvil del supervisor. Mismo nivel de exposición que las notificaciones de
  distancia que ya recibe; sin teléfono salvo decisión expresa.

## Relacionado

- [disponibilidad](../disponibilidad/README.md): el desglose del día que esto extiende, y la lección del cruce en cliente.
- [checklogs-http](../checklogs-http/README.md): las rutas de fichaje en el contenedor y la promoción a `shared`.
- [salida-del-monolito/ADR-003](../salida-del-monolito/adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md): la barrera del núcleo que ADR-002 tiene que respetar o argumentar.
- [panel-operativo-v2/ADR-005](../panel-operativo-v2/adr/ADR-005-ausencia-de-evidencia-no-es-evidencia-negativa.md): el tono de lo que no está.
- [equipos](../equipos/README.md): por qué «equipo» aquí es la plantilla de la sucursal.
- [cuadrantes](../cuadrantes/README.md): de donde saldría, algún día, el turno por día y sucursal.
- [modulos/notificaciones](../../modulos/notificaciones.md) y [modulos/checklog](../../modulos/checklog.md).
- [Clients/01-primeros-pasos/05-estructura-de-la-plataforma](../../Clients/01-primeros-pasos/05-estructura-de-la-plataforma.md): cómo se le cuenta hoy al cliente lo que puede un supervisor.

# Vacaciones y permisos desde la app · Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Calendario (ausencias) · checkbiz360 — «Mi calendario» · panel — Contacto → Solicitudes
**Fecha de inicio:** 2026-10-22
**Estado:** Diseño cerrado el 2026-10-22 · implementado el mismo día: servidor en producción (PR #212), app y panel en `develop`
**Autor:** Jose Acevedo

---

## De dónde sale

Feedback de cliente, 2026-10-22 (Jose): «¿cómo pueden solicitar vacaciones desde la aplicación?
Podemos agregar en Herramientas esto, y que también vea su disponibilidad el empleado desde la
app». Es un módulo aparte del quiosco («ojo, esto nuevo»).

Tres decisiones de Jose el mismo día:

1. **Aprueban solo los administradores del panel** (asiento de propietario o administrador). Los
   supervisores no intervienen.
2. **Se piden vacaciones y permisos** (asuntos propios, médico, otros), con un motivo opcional. Si
   es retribuido lo decide quien aprueba.
3. **«Su disponibilidad» es su calendario mes a mes** en la app: qué días trabaja y con qué
   horario o tareas, libres, festivos, vacaciones aprobadas y solicitudes pendientes. Sin saldo
   de días (eso exige configurar los días por empresa; queda fuera).

Y dos correcciones de Jose la misma tarde, al ver la primera versión:

4. **La solicitud llega a Contacto, no a Calendario.** «Es simplemente un contacto: quiero mis
   vacaciones tal día». El apartado «Incidencias» del panel pasa a llamarse **Contacto**, con dos
   pestañas: Incidencias y Solicitudes. Ahí se aprueba o rechaza; al aprobar, los días quedan
   en Horarios y festivos del empleado como si se hubieran puesto a mano, y desde ahí se
   siguen gestionando con normalidad.
5. **Sin correo a los administradores** («no por email»): la solicitud se ve en el panel, con el
   contador de pendientes en la pestaña. El aviso a la persona (aprobada o rechazada) sí va por
   push e in-app.

## Lo que hay hoy (As-Is)

Verificado contra `develop` el 2026-10-22.

- **El panel ya registra ausencias**, pero las pone un supervisor o administrador desde el desglose
  del día en Calendario → Disponibilidad: se escriben como **días libres de la persona**
  (`entities/{e}/employees/{p}/calendar/config.holidays[]`, uno por fecha, con `name`, `description`,
  `paid`), no como rangos (`absences[]`, «el modelo bueno que todavía no usa nadie»,
  [disponibilidad/02](../disponibilidad/02_to-be.md)). El trabajador no puede escribir en su
  calendario: `requireCalendarWriter` exige asiento o supervisor de la sucursal.
- **El fichaje y el tablero ya respetan las ausencias:** un día libre de la persona rechaza el
  fichaje (`checklog/day_disabled`) y el tablero de disponibilidad lo pinta como ausencia propia
  (`reason: absence`, `reasonSource: employee`).
- **El correo semanal** (`buildEmployeeWeek`, [avisos-por-correo](../avisos-por-correo/README.md))
  ya calcula la semana de una persona con tramos, tareas y lugar, y marca libres y festivos. El
  quiosco la reutiliza para «Mi semana».
- **No hay circuito de solicitud:** ni colección, ni avisos (`messages.ts` no tiene nada de
  ausencias), ni pantalla. En la app, el trabajador solo ve su horario de hoy.
- **Los administradores del panel no tienen avisos in-app**: el panel no tiene campana. Los avisos
  a la empresa van por correo (`BillingNotifier`, `emailService` con plantilla en `emails_template`
  y respaldo en código).

## Principio de diseño

> **Pedir es escribir una solicitud; aprobar es lo que ya hace el panel.** La solicitud vive
> aparte (`absence_requests`) y, al aprobarse, se convierte en los mismos días libres de la
> persona que el panel escribe hoy a mano. Nada de lo que lee ausencias (fichaje, tablero,
> correo semanal, quiosco) tiene que cambiar.

## Modelo

```text
entities/{entityId}/absence_requests/{requestId}       # solo servidor
  employeeId, employeeName, type: vacation | personal | medical | other,
  startDate, endDate (YYYY-MM-DD, inclusive, en la zona de la persona), days (naturales),
  note?, status: pending | approved | rejected | cancelled,
  createdAt, updatedAt,
  decidedAt?, decidedBy? (uid del asiento), decisionNote?, paid? (true | false | null = no consta),
  holidayIds?: string[]      # los días libres escritos al aprobar: req_<requestId>_<YYYY-MM-DD>
```

Reglas de Firestore: `absence_requests` cerrada al cliente (como `kiosks`).

**Validaciones al pedir** (puras, en `shared/calendar/absenceRequests.ts`, con tests):
fechas válidas y `start ≤ end`; `start ≥ hoy` (hoy sí; el pasado lo pone la empresa desde el panel);
como mucho **60 días**; sin solape con otra solicitud **pendiente o aprobada** de la persona ni con
sus días libres ya escritos (`holidays`) ni con sus `absences`; persona con ficha activa. Solape →
`absence_request/overlap`.

**Al aprobar:** por cada fecha del rango, `addHolidayToEmployee` con
`{ id: "req_<requestId>_<fecha>", name: <tipo en el idioma de la persona>, date, description: note,
paid }` y `calendar.holiday_changed` por día, exactamente lo que escribe el panel a mano. Queda
`holidayIds` en la solicitud. **Al rechazar:** solo el estado y la nota. **Cancelar** (la persona,
desde la app): solo mientras está pendiente. Una aprobada se deshace desde el panel como cualquier
ausencia (borrar el día libre); la solicitud queda `approved` con su historia; es suficiente para
la primera versión.

## Avisos

| Quién | Cuándo | Cómo |
|---|---|---|
| Administradores | nueva solicitud | **nada por correo** (decisión 5): la ven en Contacto → Solicitudes, con el contador de pendientes |
| La persona | aprobada o rechazada | **push + in-app** `absence_request_approved` / `absence_request_rejected` (`CheckbizSentNotificationApp`), `data.module = checkbiz_calendar`, `screen = my_calendar`; si tiene la casilla de avisos por correo, también se apunta como evento (fuera de esta versión) |
| Panel | siempre | **contador de pendientes** en la pestaña Contacto → Solicitudes |

## Contratos (`checkinbiz`, `/api/v1/checkinbiz/calendar`, ID token de Firebase)

Trabajador (ficha con su `uid` en la empresa; `requireEntityMember`; nunca ve a otros):

| Ruta | Para qué |
|---|---|
| `GET /calendar/me/month?entityId&month=YYYY-MM` | `{ month, timezone, today, days: [MonthDay], requests: [AbsenceRequest] }` — los días del mes; las solicitudes que tocan el mes |
| `GET /calendar/me/absence-requests?entityId` | sus solicitudes, las de los últimos 12 meses y las futuras, más recientes primero |
| `POST /calendar/me/absence-requests` | `{ entityId, type, startDate, endDate, note? }` → `201 { request }` |
| `DELETE /calendar/me/absence-requests/:id?entityId` | cancela una pendiente → `{ request }`; `absence_request/not_pending` si ya no lo está |

```ts
type MonthDay = {
  date: string; weekday: number;                     // 1 = lunes … 7 = domingo
  status: "work" | "off" | "holiday" | "absence" | "pending";
  slots: { start: string; end: string; title?: string; place?: string }[];   // solo en work
  name?: string;        // festivo o ausencia: cómo se llama; pending: el tipo
  paid?: boolean | null; requestId?: string; type?: AbsenceType;
};
type AbsenceRequest = { id, type, startDate, endDate, days, note?, status, createdAt, decidedAt?, decisionNote?, paid? };
```

`status`: `work` si hay turnos o tareas; `holiday` si el día libre es de la empresa o la sucursal;
`absence` si es de la persona (vacaciones aprobadas o puestas por el panel); `pending` si una
solicitud pendiente cubre el día (encima de `work` u `off`, nunca de un `absence`); `off` el resto.

Panel (asiento `owner`/`admin`, `canWrite`):

| Ruta | Para qué |
|---|---|
| `GET /calendar/absence-requests?entityId&status=pending` (o `all`) | `{ requests: [AbsenceRequest & { employeeId, employeeName, decidedBy? }], pendingCount }` |
| `POST /calendar/absence-requests/:id/approve` | `{ entityId, paid?: boolean, note? }` → `{ request }`; escribe los días libres |
| `POST /calendar/absence-requests/:id/reject` | `{ entityId, note? }` → `{ request }` |

Códigos: `absence_request/not_found` (404), `absence_request/invalid_dates` (400),
`absence_request/past` (400), `absence_request/too_long` (400), `absence_request/overlap` (409),
`absence_request/not_pending` (409), `calendar/forbidden` (403). Añadirlos a la referencia de
códigos de cliente al implementar.

## La app

En Herramientas, **«Mi calendario»** (`/attendance/my-calendar`):

- Mes a mes, con flechas, empezando en el actual. Cada día con su estado: trabajo (toca → sus
  tramos o tareas con hora y lugar), libre, festivo (nombre), vacaciones o permiso (nombre, y
  «retribuido» si consta), pendiente (rayado), hoy marcado. Leyenda abajo.
- Debajo, **sus solicitudes**: pendientes, aprobadas y rechazadas, con el motivo de rechazo si lo
  hay; cancelar una pendiente con confirmación.
- Botón **«Pedir vacaciones o permiso»**: tipo, desde, hasta (selector de rango), nota opcional,
  y el número de días naturales calculado antes de enviar. Los errores del contrato con su texto
  (solape, pasado, demasiado largo).
- Los avisos `absence_request_approved` / `rejected` llevan a esta pantalla.
- Providers user-scoped → `logoutInvalidationProvider`. Textos en es, en, pt y de. Tono de la casa:
  da seguridad, no alarma.

## El panel

**Contacto** (antes «Incidencias») → pestaña **«Solicitudes»**, junto a Incidencias, con el contador de
pendientes en la pestaña:

- Lista de pendientes (persona, sucursal/es, tipo, fechas, días, nota, cuándo la pidió), más
  recientes arriba; filtro para ver aprobadas y rechazadas.
- **Aprobar** → diálogo: retribuido (sí / no / no consta) y nota opcional. **Rechazar** → nota
  (recomendada). Las dos acciones con confirmación de una sola pulsación.
- Tras aprobar, el desglose del día en Disponibilidad enseña la ausencia como hoy (no cambia).
- Solo `owner`/`admin`; para el resto no existe la pestaña.

## Fases y tamaño

| Fase | Qué | Dónde | Tamaño |
|---|---|---|---|
| 1a | Modelo, validaciones puras y tests; rutas de trabajador y de panel; aprobar escribe los días libres; avisos push/in-app a la persona; reglas | `shared` + `checkinbiz` | 2 días |
| 1b | «Mi calendario» con el mes, las solicitudes y el formulario; entrada en Herramientas; navegación desde los avisos | checkbiz360 | 3 días |
| 1c | Contacto con las pestañas Incidencias y Solicitudes (aprobar/rechazar y contador) | panel | 1,5 días |
| 2 | Saldo de días por persona (configurable por empresa), solicitud de deshacer una aprobada, medio día, el aviso por correo también a la persona con la casilla, y la aprobación desde la app para quien tenga asiento | — | después |

## Siguiente paso: los días libres en el informe de asistencia (para el 2026-10-23)

Jose, 2026-10-22: «la guinda del pastel: en el reporte de asistencia tiene que salir otra parte
con estos días libres, o sea básicamente el resumen de disponibilidad que vemos en
Disponibilidad, y si las ausencias son retribuidas o no». Pendiente de diseñar mañana:

- En el informe de asistencia (`reports`, el que genera el PDF/XLSX por periodo), una sección
  nueva con los días libres de cada persona en el periodo: la misma lectura que el tablero de
  Disponibilidad (`ResolveAvailability`: festivos de empresa y sucursal, ausencias propias,
  motivo) y, por ausencia, **retribuida / no retribuida / no consta** (`paid` del día libre,
  ADR-004 de disponibilidad).
- Las vacaciones aprobadas desde la app entran solas: son días libres de la persona con `paid`
  decidido al aprobar.

## Fuera de alcance

- Saldo de días de vacaciones (decisión 3).
- Aprobación por supervisores (decisión 1).
- Medias jornadas: la unidad es el día.

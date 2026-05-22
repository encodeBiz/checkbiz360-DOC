# Módulo Calendario — Horarios y Festivos

---

## ADR-CAL-001 — GET calendario con cadena de herencia completa

### Problema

El endpoint `GET /calendar` devuelve el calendario efectivo resuelto, pero el cliente no puede saber de dónde vino cada dato. Concretamente:

- `sources.schedule` solo indica el scope de nivel más alto que aportó el horario semanal, pero no qué días individuales fueron sobreescritos por branch o employee.
- Los festivos en `holidays[]` son una lista plana sin indicación de si vienen de entity, branch o employee. Esto provoca duplicaciones visibles y hace imposible renderizar los festivos heredados como "solo lectura" en el editor de un scope inferior.
- El campo `raw` (disponible con `?includeRaw=true`) expone los documentos crudos de cada scope pero obliga al cliente a re-implementar la lógica de resolución para entender el origen de cada campo.

### Decisión: añadir `inheritanceChain` al output del use case

El use case `ResolveEffectiveCalendarUseCase` ya recoge los tres documentos (`entityCal`, `branchCal`, `employeeCal`). Lo que falta es:

**1. Campo `source: ResolveScope` en `Holiday`**

```typescript
export type Holiday = {
  id: string;
  name: string;
  date: string;           // "YYYY-MM-DD"
  description?: string;
  source: "entity" | "branch" | "employee";   // ← NUEVO
};
```

`concatHolidays()` ya itera los tres niveles en orden — solo hay que etiquetar con el scope antes de hacer `push`. Como el deduplicado ya existe (por `id`), el festivo conserva el source del scope que lo definió primero (entity gana sobre branch gana sobre employee, que es la semántica correcta para festivos compartidos).

**2. `scheduleInheritance` por día en `EffectiveCalendarOutput`**

```typescript
export interface EffectiveCalendarOutput {
  // ... campos existentes ...
  scheduleInheritance?: {
    monday?: ResolveScope;
    tuesday?: ResolveScope;
    wednesday?: ResolveScope;
    thursday?: ResolveScope;
    friday?: ResolveScope;
    saturday?: ResolveScope;
    sunday?: ResolveScope;
  };
}
```

Se calcula en `resolveSchedule()`: por cada día, si `employeeActive` y `employeeCal.overridesSchedule[day]` existe → `"employee"`; si `branchActive` y `branchCal.overridesSchedule[day]` → `"branch"`; si `entityCal.defaultSchedule[day]` → `"entity"`; si no → `undefined` (día no configurado).

**3. El controller ya expone `includeRaw`** — no hay cambio de API necesario para el raw. El nuevo `scheduleInheritance` y el `source` en holidays se incluyen siempre (no son datos pesados).

### Respuesta resultante (ejemplo)

```json
{
  "code": "calendar/effective_resolved",
  "data": {
    "timezone": "Europe/Madrid",
    "weeklySchedule": { "monday": { "shifts": [{"start": {"hour":9,"minute":0}, "end": {"hour":18,"minute":0}}] }, "..." },
    "holidays": [
      { "id": "esp-2024-01-01", "name": "Año Nuevo", "date": "2024-01-01", "source": "entity" },
      { "id": "bcn-2024-09-11", "name": "Diada", "date": "2024-09-11", "source": "branch" }
    ],
    "sources": {
      "timezone": "entity",
      "schedule": "branch",
      "advance": "entity"
    },
    "scheduleInheritance": {
      "monday": "entity",
      "tuesday": "entity",
      "wednesday": "branch",
      "thursday": "branch",
      "friday": "employee",
      "saturday": "entity",
      "sunday": "entity"
    },
    "overridesDisabled": false,
    "ids": { "entityId": "...", "branchId": "...", "employeeId": "..." }
  }
}
```

### Impacto en el backoffice

Con `source` en los festivos, el frontend puede renderizar los festivos heredados con badge y sin botón de edición/borrado en el scope hijo. Con `scheduleInheritance`, el editor de horario puede mostrar cada día con el badge de herencia correcto y solo permitir editar los días que pertenecen al scope actual.

Esto resuelve los bugs documentados en la sección 5: duplicación de festivos heredados, `BranchCalendarDetail` que omite festivos heredados, y la imposibilidad de distinguir orígenes.

### Cambios de código (solo backend)

| Archivo | Cambio |
|---|---|
| `domain/entities/Calendar.ts` | Añadir `source: ResolveScope` a `Holiday` |
| `application/calendar/resolveEffectiveCalendar.usecase.ts` | `concatHolidays()` etiqueta `source`; añadir `buildScheduleInheritance()` privado; añadir `scheduleInheritance` al output |
| `application/calendar/resolveEffectiveCalendar.usecase.ts` | Añadir `scheduleInheritance` a `EffectiveCalendarOutput` interface |
| Frontend `calendario.md` bug §5 | Tres bugs de herencia quedan resueltos por este cambio |

No hay cambio de ruta, no hay cambio de firma del controller, no hay migración de datos (Firestore no almacena `source` — se calcula en runtime).

---

## 1. Resumen

El calendario define los horarios de trabajo por día y gestiona festivos/ausencias. Hay tres ámbitos (scopes), y el sistema resuelve el calendario efectivo por prioridad cascada.

## 2. Estructura de Datos

### WeeklySchedule

```typescript
interface WeeklySchedule {
  monday: DaySchedule;
  tuesday: DaySchedule;
  wednesday: DaySchedule;
  thursday: DaySchedule;
  friday: DaySchedule;
  saturday: DaySchedule;
  sunday: DaySchedule;
}

interface DaySchedule {
  disabled: boolean;
  shifts: Array<{
    id: string;
    start: { hour: number; minute: number };
    end: { hour: number; minute: number };
  }>;
}
```

### Scopes

| Scope | Firestore path |
|---|---|
| Entity | `entities/{entityId}/calendar/config` |
| Branch | `entities/{entityId}/branches/{branchId}/calendar/config` |
| Employee | `entities/{entityId}/employees/{employeeId}/calendar/config` |

Los presets se almacenan con `type === "preset"` en la subcollección `calendar` del scope correspondiente (consultados via `collectionGroup`).

## 3. Resolución del Calendario Efectivo

Prioridad alta → baja:

1. Employee override (si `overridesDisabled = false`)
2. Branch override (si `overridesDisabled = false`)
3. Entity default schedule

### Resolución de Timezone

1. `employee.address.timeZone` (si `enableRemoteWork = true`)
2. `branch.address.timeZone`
3. Timezone resuelto por calendario
4. `UTC` (fallback técnico)

## 4. API HTTP

Cloud Function: `apiV100-firebaseEntryHttp-checkinbiz-calendarHandler`

| Método | Descripción |
|---|---|
| `GET` | `fetchEffectiveCalendar` — calendario fusionado entity → branch → employee |
| `GET?id=<id>` | Obtener preset específico |
| `PATCH` | `upsertCalendar(payload)` — crear/editar horario o festivo |
| `DELETE` | `deleteCalendarItem({ kind: 'holiday' | 'absence', id })` |
| `POST?action=savePreset` | Guardar preset |

Las lecturas de `config` se hacen **directamente desde Firestore** (`getRefByPathData`). El calendario efectivo fusionado va por el handler.

### Fix importante (rama actual)

El parámetro `dateLocal` del query string se ignoraba. Fix: `DateTime.utc()` → `DateTime.now().setZone(tz)` como fallback.

## 5. Bugs Conocidos en el Backoffice

### Bug crítico: `useEffect` dentro de render-prop de Formik

[`CalendarSection.tsx:512-536`](../encodebiz-front-saas/src/app/main/\[entityId\]/checkinbiz/calendar/components/CalendarSection.tsx) — viola las Rules of Hooks y resetea el formulario cada vez que cambia `baseSchedule`, sobrescribiendo ediciones del usuario.

**Fix:** extraer a un componente hijo dentro de `<Formik>`.

### Bug crítico: IDs inconsistentes en ausencias de empleado

[`HolidayModal.tsx:73-86`](../encodebiz-front-saas/src/app/main/\[entityId\]/checkinbiz/calendar/components/HolidayModal.tsx) — en creación usa `${values.name}-${date}` (espacios/caracteres especiales); en edición acumula `${values.id}-${i}` → registros huérfanos. **Causa directa de duplicaciones de festivos.**

### Bug: N llamadas secuenciales por rango

Una ausencia de 14 días genera 14 llamadas `PATCH` secuenciales sin rollback. Si una falla, el rango queda parcialmente persistido.

### Bug: estado local no usa respuesta del backend

Tras `upsertCalendar`, el backend responde con el documento normalizado pero el frontend hace `setHolidays` con el objeto local. Si el backend normaliza el `id`, el frontend diverge → la siguiente edición crea un duplicado.

### Bug: `existingDates` no excluye el rango editado

Al editar una ausencia existente, sus propias fechas aparecen como "ocupadas".

### Bug: scope incorrecto en `EmployeeHolidaysTab`

[`EmployeeHolidaysTab.tsx:112`](../encodebiz-front-saas/src/app/main/\[entityId\]/checkinbiz/calendar/components/EmployeeHolidaysTab.tsx) — llama `fetchEffectiveCalendar({ scope: 'entity', employeeId })` → debería ser `scope: 'employee'`.

### Código muerto

`BranchCalendarTab.tsx` (218 líneas) no está importado en ningún lado.

### Bugs de cascada (entity → branch → employee)

- El editor solo muestra festivos del scope propio pero la vista efectiva acumula los heredados → admin los re-agrega → duplicado visible
- `BranchCalendarDetail` no usa `fetchEffectiveCalendar` — omite festivos heredados de la entidad
- Sin campo `source` en `Holiday` — imposible distinguir de qué scope viene cada festivo
- Sin deduplicación entre niveles — misma fecha de entidad y branch se renderiza dos veces
- `overridesDisabled` solo afecta al horario, no a los festivos

### Inconsistencias de modelo

- Tipo `Absence` definido en `ICalendar.ts` pero nunca usado — todo se guarda como N entradas `Holiday`
- Strings en español hardcodeados en `CalendarSection`, `HolidayModal`, `EmployeeCalendarDetail`, `BranchCalendarDetail`
- `buildDefaultSchedule`/`mapStoredSchedule`/`normalizeScheduleForForm` redefinidos en 5+ archivos
- `employee/form/form.controller.tsx` define el bloque Calendar dos veces (líneas 482 y 659)

## 6. Orden de Ataque Recomendado

**Quick wins (bajo riesgo):**
1. Eliminar `useEffect` dentro del render-prop de Formik
2. Borrar `BranchCalendarTab.tsx`
3. Corregir `scope: 'entity'` → `scope: 'employee'` en `EmployeeHolidaysTab`
4. Unificar generación de IDs en `HolidayModal` y corregir edición de rangos

**Cambios de modelo (requieren backend + migración):**
5. Añadir campo `source` a `Holiday` en cliente
6. Definir política de merge/deduplicación en `fetchEffectiveCalendar`
7. Introducir `overridesHolidays` análogo a `overridesDisabled`
8. Introducir `Absence` real (rango con `startDate/endDate/status`) en una sola petición

**Refactor estructural:**
9. Centralizar mappers en `src/lib/calendar/`
10. Reemplazar lecturas directas de Firestore con `fetchEffectiveCalendar`
11. Renderizar festivos heredados como read-only con badge de origen
12. Mover todos los literales hardcoded a `locales/*/common.json`

# Módulo Calendario — Horarios y Festivos

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

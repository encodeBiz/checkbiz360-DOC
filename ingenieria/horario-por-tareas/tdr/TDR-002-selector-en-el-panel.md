# TDR-002 — El selector del modo en el panel

**Fecha:** 2026-10-16
**Estado:** Implementado el 2026-10-16 en `feat/horario-por-tareas` de `encodebiz-front-saas` (sin fusionar). Typecheck en verde; sin probar en navegador.
**Componente:** `encodebiz-front-saas` — `checkinbiz/calendar/components/CalendarSection.tsx`, `EntityCalendarTab.tsx`, `branch/form/form.controller.tsx`, `employee/form/form.controller.tsx`
**Decisiones de referencia:** [README](../README.md) D1; [TDR-001](./TDR-001-modo-dias-generados-y-escritor.md) §2

---

## 1. Dónde está

En **Horarios y festivos** de los tres niveles: la empresa, la ficha de la sucursal y la ficha
del empleado. Las tres pintan el mismo componente, `CalendarSection`.

- **Sucursal y empleado.** El selector está **dentro** del bloque de horario, y el bloque solo
  se abre al apagar «Usar horario base». Decidido por Jose el 2026-10-16: con el horario base
  puesto el nivel hereda todo, el modo incluido, así que no hay nada que elegir.
- **Empresa.** No tiene horario base; el selector está siempre, arriba del bloque.

Dos opciones, «Horario semanal» y «Horario por tareas», en un grupo de botones. Con «Horario
por tareas» se ocultan las plantillas y la rejilla de lunes a domingo, que no aplican, y un
aviso dice qué cuenta como turno: hora de inicio, empezar y terminar el mismo día y no
coincidir con otra tarea de la misma persona. Las reglas de jornada y descanso siguen
visibles.

## 2. Qué se guarda

| Situación | `scheduleMode` enviado |
|---|---|
| Empresa | el elegido |
| Sucursal o empleado con «Usar horario base» | `null`: borra el propio y el nivel hereda |
| Sucursal o empleado con horario propio | el elegido |

La empresa guarda desde el propio componente. Sucursal y empleado guardan desde su formulario
con lo que el componente les pasa por `onChange`; el modo entra en el `hash` con el que esos
formularios deciden si el calendario cambió, así que cambiar solo el modo también se guarda.
En el empleado, `scheduleMode` se separa de los valores de la ficha para que no viaje con
`updateEmployee`.

Lo que se lee al abrir: el modo **propio** del nivel, del documento `calendar/config`. Sin
valor, el selector arranca en «Horario semanal».

## 3. Rechazos

Si el servidor rechaza activar el modo (`calendar/tasks_mode_conflict`) o una tarea
(`task/incompatible_with_tasks_mode`), el panel enseña un mensaje traducido (`errorLocales`, es
y en). **No enseña qué tareas son**: el cliente HTTP del panel se queda con el código y
descarta `details.conflicts`. Es la primera mejora pendiente.

## 4. Lo que queda

1. Probarlo en navegador contra staging: el panel de staging es el portátil
   (`npm run start:dev` desde la rama). Casos: activar en empresa; activar en una sucursal
   apagando el horario base; volver a encender el horario base y comprobar que el empleado
   hereda; activar a alguien con una tarea sin hora y ver el aviso.
2. Enseñar la lista de tareas que impiden activar el modo (§3).
3. Las vistas de solo lectura de la ficha (`BranchCalendarDetail`, `EmployeeCalendarDetail`)
   siguen pintando la plantilla semanal aunque el nivel esté en «Horario por tareas»: deberían
   pintar los turnos del día generado. Es lectura, no bloquea activar el modo.
4. Fusionar a `develop`, y la promoción a producción con el resto del pase. No hay variables
   nuevas en Vercel.

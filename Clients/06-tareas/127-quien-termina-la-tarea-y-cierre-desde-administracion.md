# Quién termina la tarea y cerrarla desde administración

Cuando una tarea tiene varias personas, hay que decidir quién la da por terminada: la primera que acaba, todas, o una persona responsable. Y cuando nadie la cerró desde la app pero el trabajo se hizo, la dirección puede cerrarla desde el panel con sus horas reales, para que el informe no quede en blanco. Este artículo explica las dos cosas y cómo se distingue en el historial lo que hizo la administración.

---

## Qué resuelve

- **Una formación de trece personas no se cierra cuando acaba la primera**: con *Todas las personas*, cada una cierra su parte.
- **Un equipo con jefa de equipo**: solo ella inicia y cierra, aunque en la tarea haya gerentes o supervisores.
- **El informe sale completo** aunque la tarea se cerrase en la oficina: con la hora de inicio y de cierre que se indiquen.
- **Se sabe quién hizo qué**: lo que hace la administración desde el panel aparece como tal, no como si lo hubiera hecho una trabajadora.

---

## ¿Quién da la tarea por terminada?

Al crear o editar una tarea, el campo **¿Quién da la tarea por terminada?** ofrece tres opciones:

| Opción | Qué pasa |
|---|---|
| **Basta con una persona** | La primera persona que la completa la cierra para todas. Es la opción por defecto. |
| **Todas las personas** | Cada persona completa su parte; la tarea se cierra cuando termina la última. |
| **Una persona responsable** | Solo la persona responsable la inicia, pausa y completa, aunque otras asignadas sean supervisoras o gerentes. Al completarla, la cierra para todas. |

Con **Una persona responsable**, aparece el campo **Responsable**: elija a una de las personas ya asignadas. Si la quita de la tarea, hay que elegir otra antes de guardar.

En la ficha de la tarea, el resumen dice la opción en **Terminación** (por ejemplo, *Responsable: Ana López*), y en **Equipo asignado** la responsable aparece con *· Responsable*.

### Qué ve cada persona en la app

- Con **Todas las personas**, quien termina su parte ve *Tu parte está hecha. La tarea sigue abierta para el resto.*
- Con **Una persona responsable**, el resto de asignadas ve *La responsable de esta tarea es … : solo ella la inicia, pausa y completa.* Si alguien lo intenta, la app le explica que solo la responsable puede hacerlo. Ser gerente o supervisora y estar asignada no cambia esta regla.

Quien gestiona la tarea desde el panel sin estar asignada a ella puede actuar siempre, para resolver lo que haga falta.

> **Horario por tareas:** si la plantilla trabaja con horario por tareas, la **Salida** de la responsable cierra la tarea; la de las demás, solo su parte.

---

## Completar una tarea desde administración

Si el trabajo se hizo pero nadie inició la tarea en la app, el panel la cierra pidiendo las horas reales, para que el informe no se quede sin inicio ni tiempo.

1. Abra la tarea en el panel.
2. Pulse **Completar** (está en las tareas asignadas, en curso o rechazadas), o cambie su estado a *Completada* desde **Editar**.
3. Se abre **Completar tarea**: *Nadie la empezó desde la app. Indica cuándo empezó y cuándo terminó.* Rellene **Inicio** y **Cierre**.
4. Confirme.

El inicio tiene que ser anterior al cierre, y el cierre no puede ser posterior a ahora.

Si la tarea ya estaba iniciada, **Completar** no pide horas: ya tiene su inicio.

### Cómo queda registrado

- En el resumen de la ficha, **Completada por** dice el nombre y *· desde administración*.
- En el historial, la línea de completada dice *Desde administración · empezó … y terminó …* con las horas que se indicaron.
- En el [informe de tareas](./48-informes-de-tareas.md), las columnas de **Inicio**, **Fin** y tiempo salen con esas horas, y la columna **Completada por** dice el nombre con *(desde administración)*.

---

## «Administración» en el historial

Cuando un propietario o un administrador actúa desde el panel —asigna, completa, cancela, valida—, el historial de la tarea lo firma como **Por {nombre} · Administración**. Así se distingue de lo que hacen las personas desde la app, aunque quien lo hace tenga también ficha de empleado en alguna sucursal.

Las asignaciones se leen como *Asignada a …* y las retiradas como *Asignación retirada: …*.

---

## Problemas frecuentes

| Situación | Qué hacer |
|---|---|
| La tarea sigue abierta aunque alguien la completó | Mire **Terminación**: con *Todas las personas* se cierra cuando acaba la última. Las que ya terminaron ven *Tu parte está hecha*. |
| Una gerente asignada no puede iniciar la tarea | La tarea tiene una responsable y no es ella. Cambie la responsable en **Editar** o que la inicie la responsable. |
| No deja guardar con *Una persona responsable* | Elija en **Responsable** a una de las personas asignadas. |
| Al completar desde el panel pide horas | La tarea no se inició desde la app. Indique cuándo empezó y terminó de verdad: son las horas que saldrán en el informe. |
| «El cierre no puede ser posterior a ahora» | Corrija la hora de **Cierre**: no se puede cerrar una tarea en el futuro. |

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Asignar tareas a empleados](./41-asignar-tareas-a-empleados.md) | Asignación individual y múltiple |
| [Estados de una tarea](./42-estados-de-una-tarea.md) | Ciclo de vida y cumplimiento temporal |
| [Seguimiento y actualizaciones](./43-seguimiento-y-actualizaciones.md) | Iniciar, pausar, completar y el historial |
| [Informes de tareas](./48-informes-de-tareas.md) | El Excel con la columna **Completada por** |

# 09 · Tareas con encargada

**Fecha:** 2026-10-27 (la política existe desde el 26-oct; este documento la fija y corrige)
**Estado:** regla cerrada; corrección del 27-oct en rama `fix/encargada-solo-ella`
**Autor:** Jose Acevedo

## La regla

Con `completionPolicy: "responsible_worker"` y `config.responsibleEmployeeId` (una de las
asignadas), Jose, 2026-10-27:

> «Cuando pones un responsable de tarea, solo ese puede iniciar y cerrar la tarea.»

- **Solo la encargada inicia, pausa, reanuda y completa la tarea.** Al completarla, la cierra
  para todas.
- **El resto de asignadas no la mueve**, tengan el papel que tengan. Ser gestor o supervisor
  no exime a quien está asignado y no es la encargada. Desde la app o el panel recibe
  `403 task/responsible_only`.
- **Un gestor que no está asignado** sí puede moverla desde la gestión. Sirve para desatascar
  una tarea (la encargada no ha venido, se equivocó…). Si quiere que otra persona la lleve,
  cambia la encargada.

## El fichaje del horario por tareas

Quien está en «Por tareas» mueve sus tareas al fichar ([TDR-006](tdr/)). El fichaje **nunca se
bloquea** por esta regla. Pero el fichaje de una asignada que no es la encargada **solo cuenta
para su parte**:

| Fichaje de una asignada que no es la encargada | Su parte | La tarea |
|---|---|---|
| Entrar | «trabajando» | no cambia: si no ha empezado, sigue «asignada» |
| Descanso / Fin de descanso | — | no cambia: la pausa es de la tarea y la lleva la encargada |
| Salir | «completada» | no cambia: ni se cierra ni empieza |

La hora de inicio de la tarea y su cumplimiento de plazo los fija la encargada al iniciarla
(por la app o por su Entrar). Su Salir la cierra para todas.

## Lo que se corrigió el 2026-10-27

Visto en producción con la tarea «Prueba» (Encodebiz): Jose, asignado y gestor, sin ser el
encargado (lo era Cindy), la inició desde la app y la «completó» dos veces. El servidor:

1. le dejó iniciarla, porque la regla eximía a **cualquiera que pudiera gestionar la tarea**,
   aunque estuviera asignado;
2. al completar, solo dio por hecha su parte (correcto), pero la app dijo «Tarea completada».

Además, en «Por tareas» la Entrada de una compañera ponía la tarea entera «en curso», y su
Descanso la pausaba para todas.

Se corrige: la excepción de gestión solo vale para quien no está asignado, y el fichaje de una
compañera solo mueve su parte (tabla de arriba). QA: TSK-19-06 y HPT-17.

## El nombre en pantalla

En el panel se llama **«Responsable»** («Una persona responsable» en el selector), no
«Encargada»: puede ser cualquiera. Rama del front `fix/etiquetas-responsable`. En el código
sigue siendo `responsible_worker` / `responsibleEmployeeId`.

## La app (rama `feat/tareas-responsable-y-avisos-agrupados`, 6be850a, 2026-10-28; sin publicar)

- Iniciar, Pausar, Reanudar y Completar solo los ve la persona responsable, en la ficha y en
  las tarjetas. A las otras asignadas, la ficha les dice quién es la responsable. Quien gestiona
  sin estar asignado conserva los botones.
- `task/responsible_only` se traduce («Esta tarea tiene una persona responsable: solo ella
  puede iniciarla, pausarla o completarla»), antes que el 403 genérico.
- Si al completar la tarea sigue en curso, dice «Tu parte está hecha», no «Tarea completada».
- **Editar desde la app conserva a la responsable.** Hasta 1.10.0 el formulario reescribía
  `completionPolicy` a `all_assigned_workers` o `any_assigned_worker`: guardar desde el móvil le
  quitaba la responsable a la tarea. Las versiones publicadas lo siguen haciendo.

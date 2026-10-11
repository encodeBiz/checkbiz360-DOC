# ADR-003 — Las tareas se espejan desde el servicio `tasks`, en la petición

**Fecha:** 2026-10-10
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Las tareas no están en Postgres ([01_as-is §3](../01_as-is.md)). El dashboard las necesita
para el hoy y para las semanas, y el Panel mensual las echa en falta desde julio («Tareas va
como `sin_evidencia` para todo el mundo»). Jose decidió el 2026-10-10 que se espejan antes de
pintarlas.

Hay tres formas de llevar un documento de Firestore a Postgres en esta plataforma, y las tres
están en producción:

1. **Trigger de Firebase → `sync`** (fichajes, valoraciones). Reactivo, por escritura, pero
   exige desplegar en el SaaS, y el trigger de fichajes **no reintenta**: si el contenedor no
   responde en 7 s, escribe un log y el registro no llega nunca.
2. **`SyncDimensions` en `analytics`** (empleados, sucursales, calendario). Lee Firestore
   entero por entidad. Nadie lo programa.
3. **El propio servicio escribe el espejo en la petición** (`inventory`,
   [TDR-004 de inventario](../../inventario/tdr/TDR-004-espejo-postgres-e-informes.md)):
   tras confirmar Firestore, a mejor esfuerzo, con job de reintento y clave primaria que lo
   hace idempotente.

## Decisión

**La tercera.** `tasks` espeja cada tarea que escribe, en la misma petición, después de
confirmar Firestore. Un `MirroredTaskRepository` que extiende `FirestoreTaskRepository`, un job
`remirror` que re-espeja lo tocado en la última ventana, y un script de backfill. Detalle en
[TDR-002](../tdr/TDR-002-espejo-de-tareas.md).

Es posible porque **todas las escrituras que cambian el estado de una tarea pasan por `tasks`**:
el panel y la app por `/api/v1/tasks`, Rentman y los cuadrantes de Merlin por
`/api/v1/tasks/system`. `inventory` escribe actividad, no la tarea; el worker de aviso de inicio
sólo sella una fecha de notificación. La Cloud Function `tasksHandler` sigue exportada en el
SaaS: la fase 0-bis confirma que no recibe tráfico antes de dar el espejo por completo.

## Alternativas descartadas

- **Trigger en Firebase como los fichajes.** Obliga a tocar el SaaS, hereda el «sin reintento»
  que este mismo proyecto va a tener que tapar para los fichajes, y pone el espejo lejos de
  quien conoce la tarea.
- **Leer tareas de Firestore desde el panel.** Rompe [ADR-001](./ADR-001-postgres-es-la-fuente-del-ahora.md)
  y deja el histórico semanal sin fuente: para sumar semanas hay que tenerlas en Postgres.
- **Reusar los eventos `task.*` que ya emite `tasks`.** Van a los webhooks de clientes; su
  cola (`webhook_delivery`) es de entregas, no una tabla de tareas, y sólo existe si hay un
  endpoint suscrito. Serviría de rastro, no de espejo.

## Consecuencias

- El espejo es **de la tarea**, no de sus subcolecciones. Asignaciones, notas, evidencias,
  pausas y actividad siguen sólo en Firestore. El dashboard no las necesita: `assignedEmployeeIds`
  y los contadores de pausa viajan en el propio documento.
- Un borrado deja la fila con `deleted_at`: el histórico de una semana no puede perder una
  tarea porque alguien la borrara el jueves.
- Con `tasks_raw` poblado, el Panel mensual puede dejar de decir `sin_evidencia` en tareas.
  No es parte de este proyecto; es la consecuencia que lo paga.
- Es el momento de retirar `tasksHandler` del SaaS (tasks-service, fase 4). Mientras exista,
  cualquier cliente que lo use escribe tareas que el espejo no ve.

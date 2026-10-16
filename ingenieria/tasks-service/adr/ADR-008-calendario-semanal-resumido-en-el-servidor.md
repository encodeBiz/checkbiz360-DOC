# ADR-008 — El calendario semanal de tareas se resume en el servidor, sobre el espejo

**Fecha:** 2026-10-16
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El panel estrena una vista de calendario semanal de tareas (pestaña «Calendario semanal» de
Gestión de tareas). Su primera versión bajaba al navegador todas las tareas de la semana con
dos consultas directas a Firestore —rango sobre `dueAt` y rango sobre `scheduledStartAt`,
tope de 500 cada una— y agrupaba en el cliente.

Eso no escala y falla en silencio: con 6000 tareas en una semana el calendario enseñaría
como mucho mil sin avisar, los contadores mentirían, y sin tope serían 6000 lecturas y unos
10 MB por cada apertura. El agrupado en sí es barato; mover los datos es lo caro.

El calendario no necesita las tareas. Necesita, por día y hora, **cuántas hay, de qué
estado y una muestra de dos** para pintar la celda, y la lista de una celda sólo cuando se
abre el panel lateral.

Se valoraron tres caminos.

**Opción A — Listado del servicio con filtros y aviso de tope.** Mejora el filtrado pero sigue
bajando todas las tareas de la semana cuando no hay filtros.

**Opción B — Resumen calculado en el servicio leyendo Firestore.** Acota lo que viaja al
navegador, pero el servicio sigue leyendo cada tarea de la semana en cada petición.

**Opción C — Resumen calculado en Postgres sobre el espejo `tasks_raw`.** Las tareas ya se
espejan desde este mismo servicio en la propia petición (ADR-003 del dashboard operativo,
TDR-002). Un agrupado por día, hora y estado sobre un índice cuesta lo mismo con 60 tareas
que con 60 000.

## Decisión

Opción C. Dos endpoints nuevos en el servicio de tareas (ver [03](../03_contratos-api.md)):

- `GET /calendar`: por día local y hora local, recuento, reparto por estado y muestra de dos
  tareas; la fila «Fecha límite» por día; las tareas de varios días enteras; y el recuento por
  estado para la leyenda.
- `GET /calendar/cell`: las tareas de una celda, paginadas, para el panel lateral.

La zona horaria la manda el navegador (`tz`, IANA): el calendario enseña la hora de pared de
quien lo mira, igual que las columnas de la tabla. Postgres agrupa con `AT TIME ZONE`, el
mismo modismo que ya usa `analytics`.

Una tarea se coloca en la hora en que **empieza** y no se le dibuja duración: el vencimiento
«es un compromiso con alguien, no un presupuesto de horas» (08_pausas.md). Dibujar la ventana
inicio–vencimiento inventaba una duración y, además, encadenaba por solape tareas que no
coinciden hasta fundir treinta en un bloque.

Se añade el índice parcial `idx_tasks_raw_entity_start` (migración 040): el de vencimiento ya
existía desde la 026.

## Consecuencias

- El calendario depende del espejo, no de Firestore. El espejo se escribe en la misma
  petición y a mejor esfuerzo, con el job `remirror` de red: una tarea recién creada puede
  tardar en aparecer si Postgres falló en ese momento. Es la misma garantía que ya tiene el
  dashboard operativo.
- El front deja de consultar Firestore para el calendario; el listado en tabla no cambia.
- Queda fuera, a sabiendas, la tarea que empieza antes de la semana y vence después de ella.
- Un trabajador sin nivel de supervisor sólo ve su calendario, como en `GET /`.
- El servicio `tasks` ya tenía la conexión a Postgres por el espejo; no hace falta
  configuración nueva en el despliegue, sólo aplicar la migración.

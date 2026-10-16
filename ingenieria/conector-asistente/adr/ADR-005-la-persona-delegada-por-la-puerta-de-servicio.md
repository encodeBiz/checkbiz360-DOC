# ADR-005 — La persona delegada entra por la puerta de servicio, con sus propios permisos

**Fecha:** 2026-10-16
**Estado:** Aceptado
**Decisionario:** Jose Acevedo (cambios sueltos de tareas y horario estándar, 2026-10-16)

---

## Contexto

Además del lote, el asistente necesita cambios sueltos: mover una tarea, pasársela a otra
persona, cancelarla, crear una, y cambiar la semana tipo de alguien en el modo estándar. Esas
operaciones ya existen en `tasks` y en el calendario de `checkinbiz`, con sus permisos
(`resolveTaskActor`, `requireCalendarWriter`) y sus validaciones (las reglas del horario por
tareas, `validateWeeklySchedule`).

El token del asistente no puede reenviarse (TDR-001 §9), y el núcleo no sabe leerlo. Hoy la
única forma de entrar en nombre de alguien es la tarea de sistema: `POST /tasks/system` con la
clave S2S y un `actorUid`, al que se le comprueban los mismos permisos.

Los guardas de entidad y de calendario leen a la persona de `req.user.uid`, que hoy sólo pone
`requireFirebaseAuth`. Las rutas de tareas la resuelven aparte, leyendo el token en
`resolveTaskActor`.

## Decisión

1. **Un middleware en `shared`, `requireDelegatedUser`**: exige la clave S2S y una cabecera
   `x-actor-uid`, comprueba que esa cuenta existe en Firebase Auth y no está deshabilitada, y
   pone `req.user = {uid, delegated: true}`. Desde ahí, **las rutas de siempre con sus guardas
   de siempre**: nada nuevo que permita más de lo que la persona puede en el panel.
2. **Calendario**: el router de calendario de `checkinbiz` se monta además en
   `/api/v1/checkinbiz/delegated/calendar` detrás de ese middleware. Mismos controladores,
   mismos permisos, mismas validaciones.
3. **Tareas**: el router de tareas se monta además en `/api/v1/tasks/delegated` detrás del
   middleware, y `resolveTaskActor` resuelve por `uid` (`resolveActorByUid`, el de la tarea de
   sistema) cuando la petición viene delegada, en vez de leer el token.
4. **Quién puede delegar es quien tiene la clave S2S**, es decir, nuestros servicios. El
   asistente comprueba en cada llamada que la conexión está viva y que la persona sigue con
   asiento de administración en esa empresa antes de llamar a nadie (TDR-001 §8).
5. **Nada se escribe sin enseñarlo antes.** Las herramientas que escriben llevan `confirmar`:
   sin él devuelven el antes y el después sin tocar nada; con él, escriben. Van marcadas como
   destructivas en el protocolo, así que Claude y ChatGPT piden permiso a la persona antes de
   ejecutarlas. El servidor no puede saber si alguien leyó la vista previa; lo que garantiza
   es que la vista previa existe y que el cliente del asistente pregunta.

## Alternativas descartadas

- **Que el asistente escriba en Firestore con el Admin SDK.** Se salta permisos y
  validaciones del núcleo: lo que el panel rechaza, el asistente lo escribiría.
- **Copiar en el asistente los controladores que necesita.** Dos copias de cada regla que
  envejecen por separado.
- **Una ruta `/system` por operación**, como la de crear. Una por cada verbo, cada una con su
  forma de recibir al actor; el middleware lo resuelve una vez para todas.

## Consecuencias

- El horario por tareas, el borrado sólo de lo no empezado (tasks TDR-006), las validaciones
  del horario y los permisos por sucursal valen igual para el asistente sin escribir nada.
- Reasignar va por las rutas de asignación, no por `PATCH`: editar una tarea ignora los
  empleados y responde 200 (HAL-38, abierto).
- La cabecera `x-actor-uid` sólo significa algo detrás de la clave S2S. En las rutas normales
  se ignora.

# ADR-002 — Migrar solo la superficie HTTP; triggers y schedules permanecen en Firebase

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El módulo de tareas en Firebase tiene tres tipos de superficie:

1. **HTTP** — `tasksHandler` (`https.onRequest` con un Express que monta `taskRouter`, 14 rutas).
2. **Schedules** — worker que evalúa tareas no iniciadas y notifica (usa `TaskRepository.findPendingStartNotifications`), p.ej. `notifyTaskStartDelay`.
3. **Triggers de Firestore** — reacciones a escrituras sobre las tareas (notificaciones push, side-effects).

La migración podría intentar llevarse todo, o solo una parte.

---

## Decisión

Se migra **únicamente la superficie HTTP**. Los **schedules y los triggers de Firestore permanecen en Firebase**.

---

## Justificación

**Lo reactivo está pegado a Firestore por diseño.** Un trigger `onWrite` sobre `entities/{entityId}/tasks/**` y un schedule que barre documentos son primitivas nativas de Firebase. Reimplementarlas fuera exigiría o bien polling contra Firestore desde el servidor, o bien un mecanismo de eventos propio — coste y riesgo sin retorno para este objetivo (bajar latencia y coste del HTTP de usuario).

**El HTTP es lo que gana con la migración.** Los endpoints de tareas son `onRequest` (Express puro, cero `onCall`), invocados por app y back office. Ahí están la latencia de cold start y el coste por invocación que queremos recortar. Portarlos es un *lift-and-shift* limpio.

**La fuente de datos es la misma.** Tanto el HTTP migrado como los triggers/schedules que se quedan operan sobre el mismo Firestore (`entities/{entityId}/tasks/...`). No hay bifurcación de estado: el servidor escribe, el trigger reacciona, exactamente igual que hoy.

---

## Consecuencias

**Positivas:**
- Migración de alcance mínimo y reversible: solo cambia quién sirve el HTTP.
- Las notificaciones push y el aviso de inicio tardío siguen funcionando sin tocarse.
- Sin necesidad de construir infraestructura de eventos en el servidor.

**Negativas / Compromisos aceptados:**
- Convivencia: parte de la lógica de tareas vive en el servidor (HTTP) y parte en Firebase (reactivo). Hay que documentar esta frontera con claridad (ver [01_as-is](../01_as-is.md) y [02_to-be](../02_to-be.md)).
- El servidor debe escribir en Firestore con el mismo shape que espera el trigger (fechas, campos `*NotifiedAt`), para no romper la cadena reactiva.
- `findPendingStartNotifications` queda como método del repositorio pero solo lo consume Firebase; en el servidor no se cablea ninguna ruta que lo use.

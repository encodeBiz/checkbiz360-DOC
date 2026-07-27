# ADR-002 — Migrar solo HTTP; lo reactivo se queda en Firebase

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

En el port de tareas se estableció el principio: *solo se migra quién sirve el HTTP; los triggers y schedules permanecen en Firebase, operando sobre los mismos datos que el servidor escribe*. Toca decidir cómo aplica ese principio al módulo documental.

---

## Decisión

Se **migra solo la superficie HTTP** (las 8 rutas de `documentRouter`). Cualquier lógica reactiva de Firebase que pudiera existir se queda en Firebase.

**Observación específica de documental:** a diferencia de tareas, el módulo documental **no tiene triggers de Firestore ni schedules propios**. Toda la reacción a la escritura —indexar el documento, notificar el alta/ack, registrar actividad— ocurre *dentro* de los casos de uso HTTP, de forma síncrona a la petición. Por tanto, en la práctica, "lo reactivo" que queda en Firebase es únicamente el propio `documentsHandler` hasta su retirada.

---

## Justificación

- **Riesgo mínimo.** No hay que reimplementar ni mover triggers: el módulo no los tiene. El port es un traslado de carpeta HTTP puro.
- **El comportamiento side-effect se preserva 1:1.** Índice, notificaciones y actividad se ejecutan en el mismo punto del flujo (dentro del caso de uso), con la misma semántica `fire-and-forget` para índice/actividad y `await` para notificaciones en el alta.
- **Consistencia con la plataforma.** Es el mismo principio ya aceptado para tasks ([tasks-service/ADR-002]), lo que mantiene un modelo mental único para toda la migración.

---

## Consecuencias

**Positivas:**
- El corte es un cambio de `location` en nginx; Firebase no necesita ningún redeploy de triggers.
- Cero divergencia de comportamiento reactivo entre el antes y el después.

**Negativas / Compromisos aceptados:**
- Las notificaciones y el índice pasan a ejecutarse en el proceso del servidor (no en Functions). En el alta se **espera** a las notificaciones antes de responder (igual que hoy en CF, donde `fire-and-forget` no era seguro tras `res.json()`); en el servidor persistente ese `await` es una elección conservadora que preserva el contrato y podría relajarse en el futuro si se quisiera bajar latencia de subida.
- El `documentsHandler` sigue vivo durante el periodo de observación; se retira en la fase de cutover (ver [04_fases.md](../04_fases.md)).

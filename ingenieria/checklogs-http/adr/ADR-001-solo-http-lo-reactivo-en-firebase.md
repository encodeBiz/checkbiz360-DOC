# ADR-001 — Migrar solo el HTTP; los triggers y schedules se quedan en Firebase

**Estado:** Aceptado
**Fecha:** 2026-07-30
**Contexto:** checklogs-http

---

## Contexto

Alrededor de la colección `entities/{entityId}/checklogs` hay dos clases de código muy distintas:

- **HTTP** — tres funciones que atienden a un cliente que espera respuesta: crear un fichaje, corregirlo, pedir una jornada manual.
- **Reactivo** — triggers de Firestore y schedules que se disparan *después* de que el dato cambie: procesamiento, sync a PostgreSQL, webhooks, cierre de jornadas vencidas, agregación diaria.

Portar todo de golpe significaría reemplazar el mecanismo de disparo (trigger de Firestore → cola propia, cron de Firebase → cron propio), y eso es un cambio de garantías, no un cambio de servidor.

## Decisión

Se migra únicamente la superficie HTTP. Firestore sigue siendo la fuente y todo lo reactivo permanece en Firebase, operando sobre los datos que ahora escribe el contenedor.

Se quedan intactos: `onWhriteChecklog`, `onChecklogSync`, `onChecklogWebhook`, `onCreateIssues`, `sanitizer-checklogs`, `dailyCollectorData`, `employeePlanifierWorker`.

## Justificación

El Admin SDK escribiendo desde un contenedor produce exactamente el mismo evento de Firestore que escribiendo desde una Cloud Function. Para el trigger, el origen es invisible. Eso convierte la frontera HTTP/reactivo en un punto de corte gratuito: se gana la latencia y el despliegue independiente donde importan —el camino del usuario— sin tocar nada de lo que ya funciona sin supervisión.

Es la misma decisión que se tomó en `tasks-service` (ADR-002) y en `documental-service` (ADR-002), y es coherente con ellas.

## Consecuencias

**A favor**

- Cero migración de datos y cero riesgo sobre el pipeline de analítica.
- La superficie de fallo del cutover queda acotada a tres endpoints.
- El rollback no depende de reconstruir estado: es volver a apuntar una URL.

**En contra**

- El dominio queda repartido: el HTTP en el servidor, lo reactivo en Firebase. Hay que leer dos repos para entender el flujo completo.
- Persisten dos copias del modelo `CheckLog` (Firebase y `services/checkinbiz`) que deben mantenerse coherentes mientras dure la convivencia.

**Obligación que crea**

Como los triggers siguen vivos, el contrato con ellos también: el port debe escribir `deadline` en cada checkin (lo lee `sanitizer-checklogs`) y conservar la forma exacta de `metadata` (lo lee el pipeline de sync). Un campo que se deje de escribir no da error: simplemente deja de pasar algo, semanas después y en otro sitio.

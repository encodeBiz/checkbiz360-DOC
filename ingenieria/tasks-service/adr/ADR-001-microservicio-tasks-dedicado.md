# ADR-001 — Microservicio `tasks` dedicado, no ampliar un servicio existente

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Se migra la superficie HTTP de tareas desde Firebase Functions (`tasksHandler`) al servidor privado `encodebiz-api`. La pregunta es dónde alojar el `taskRouter` una vez portado.

**Opción A — Montar el router dentro del servicio `checkinbiz` existente.**
El servicio `checkinbiz` de `encodebiz-api` ya es un Express con Firestore y comparte parte del dominio (Employee, Branch). Montar ahí el `taskRouter` es lo de menor ceremonia: no hay bloque nuevo en compose ni upstream nuevo en nginx.

**Opción B — Levantar un microservicio `tasks` propio.**
Un servicio nuevo (`services/tasks`, puerto 3006) con su Express, Dockerfile, bloque en `docker-compose.yml`, upstream y `location` en nginx, espejando a `reports`, `sync` y `analytics`.

---

## Decisión

Se elige **Opción B: microservicio `tasks` dedicado**.

---

## Justificación

**El servicio `checkinbiz` actual es otro contexto acotado.** Hoy hace heurística, patrones e integración Rentman — es analítica interna consumida server-to-server, no la API pública operacional. Meter el CRUD de tareas dentro mezcla dos responsabilidades distintas y empuja a ese servicio hacia un mini-monolito, en contra del principio de microservicios que ya sigue la plataforma (un servicio por contexto).

**El perfil de escalado y riesgo es distinto.** La API de tareas es tráfico de usuario final (app móvil + back office), con picos de subida de evidencias a Storage. Aislarla permite escalar y desplegar `tasks` sin tocar la heurística ni el pipeline analítico.

**El cutover es endpoint por endpoint en nginx.** Con un servicio propio, apuntar la ruta desde la function de Firebase al servidor privado es cambiar una `location`. No se toca ningún otro servicio en producción.

**La ceremonia es baja y ya está resuelta.** `reports`/`sync`/`analytics` son la plantilla exacta: `app.ts` + `server.ts` + `Dockerfile` + bloque compose + upstream nginx. Copiar ese esqueleto es trabajo mecánico, no arquitectura nueva.

---

## Consecuencias

**Positivas:**
- Límite de módulo limpio: la API pública de tareas vive sola, versionable y desplegable de forma independiente.
- Espeja el límite que ya existía en el SaaS (`services-saas/checkinbiz/interfaces/http/task`), por lo que la migración es un *lift-and-shift* de carpeta.
- Riesgo de deploy acotado al propio servicio `tasks`.

**Negativas / Compromisos aceptados:**
- Un contenedor y un puerto (3006) más que mantener.
- El dominio `Employee`/`Branch` se duplica parcialmente entre `checkinbiz` y `tasks`. Se acepta a corto plazo; la unificación en `@encodebiz/shared` es trabajo futuro, no del día 1 (ver [TDR-001](../tdr/TDR-001-port-modulo-task.md)).

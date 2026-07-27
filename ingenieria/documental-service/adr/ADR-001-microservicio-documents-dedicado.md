# ADR-001 — Microservicio `documents` dedicado, no ampliar un servicio existente

**Fecha:** 2026-07-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Se migra la superficie HTTP de gestión documental desde Firebase Functions (`documentsHandler`) al servidor privado `encodebiz-api`. La pregunta es dónde alojar el `documentRouter` una vez portado.

**Opción A — Montar el router dentro de un servicio existente** (`checkinbiz`, o el propio `tasks`, o `reports`). Menos ceremonia: sin bloque nuevo en compose ni upstream nuevo en nginx.

**Opción B — Levantar un microservicio `documents` propio** (`services/documents`, puerto 3007) con su Express, Dockerfile, bloque en `docker-compose.yml`, upstream y `location` en nginx, espejando a `tasks`, `reports`, `sync` y `analytics`.

---

## Decisión

Se elige **Opción B: microservicio `documents` dedicado**.

---

## Justificación

**Cada servicio es un contexto acotado.** `checkinbiz` hace heurística/patrones/Rentman (analítica S2S); `tasks` es el CRUD de tareas; `reports` genera informes. La gestión documental es su propio dominio (documentos, permisos RRHH, acks, índice de búsqueda). Meterlo en otro servicio mezcla responsabilidades y empuja a un mini-monolito, en contra del principio de la plataforma (un servicio por contexto).

**El perfil de escalado y riesgo es distinto.** Documental es tráfico de usuario final con subidas/descargas a Storage de ficheros de hasta 10 MB. Aislarlo permite dimensionar memoria y `client_max_body_size` sin afectar a otros servicios.

**El cutover es endpoint por endpoint en nginx.** Con un servicio propio, apuntar la ruta desde la function de Firebase al servidor privado es cambiar una `location`, sin tocar ningún otro servicio en producción.

**La ceremonia es baja y ya está resuelta.** `tasks` es la plantilla exacta y reciente: `app.ts` + `server.ts` + `Dockerfile` + bloque compose + upstream nginx, más los repos y utilidades (auth, multipart, notificaciones) que documental reutiliza casi tal cual.

**En Firebase, `documentsHandler` ya mezclaba `/documents` y `/reports`** en un solo handler. Ese acoplamiento es precisamente lo que se deshace aquí: `reports` ya vive solo, y `documents` pasa a vivir solo también.

---

## Consecuencias

**Positivas:**
- Límite de módulo limpio: la API documental vive sola, versionable y desplegable de forma independiente.
- Espeja el límite que ya existía en el SaaS (`services-saas/checkinbiz/interfaces/http/document`), por lo que la migración es un *lift-and-shift* de carpeta.
- Riesgo de deploy acotado al propio servicio `documents`.

**Negativas / Compromisos aceptados:**
- Un contenedor y un puerto (3007) más que mantener.
- El dominio `Employee`/`Branch` y las utilidades de auth/multipart/notificaciones se duplican parcialmente con `tasks`. Se acepta a corto plazo; la unificación en `@encodebiz/shared` es trabajo futuro (ver [TDR-001](../tdr/TDR-001-port-modulo-document.md)).

# Integración Rentman ↔ encodeBiz

> **Para:** producto + ingeniería (encodeBiz / checkinbiz).
> **Qué cubre:** el plano de la integración con [Rentman](https://rentman.io) — **add-on de pago** que sincroniza clientes/proyectos, asignaciones, tareas y horas.
> **Modelo:** módulo **activable** dentro de "Integraciones", **no automático**, requiere configuración y tiene **coste propio** (paridad con checkbiz / passbiz). Ver `04_activacion-saas.md`.
> **Estado:** 🟡 **PLANIFICACIÓN**. No hay implementación comprometida. Dos decisiones de negocio abiertas (ver `03_decisiones-abiertas.md`).
> **Fecha:** 2026-07-26.

---

## 1. En una frase

**encodeBiz es la cabina de gestión; Rentman se mantiene sincronizado en paralelo.**
El cliente gestiona su operación (clientes/proyectos, asignaciones, tareas, fichaje)
en encodeBiz, y todo se refleja en Rentman **en los dos sentidos** vía **polling**
desde el servicio `sync` — sin webhooks. Quien ya usa Rentman puede seguir usándolo;
lo que entra por nuestra puerta (tareas + registro horario legal) es lo que fuerza
la adopción de encodeBiz.

## 2. Principios

1. **No duplicar.** Un dato se introduce una vez, en el sistema que sea, y se
   refleja en el otro. El cliente no mantiene lo mismo en dos sitios.
2. **Bidireccional real.** Los clientes con Rentman siguen operando allí; el sync
   propaga cambios en ambos sentidos.
3. **Por polling, no por webhooks.** El servicio `sync` sondea Rentman cada X y
   reconcilia. Idempotente, re-ejecutable, auditable, y con el ritmo bajo nuestro
   control. Ver `adr/0001-sync-bidireccional-por-polling.md`.
4. **El foso es nuestro.** Tareas y fichaje legal español no existen en Rentman;
   son 100% de encodeBiz y no se pueden replicar allá.

## 3. Los flujos, en tres capas

El modelo se ordena en tres niveles distintos — **no** confundir asignación con jornada:

| Capa | Rentman | encodeBiz | Sentido |
|---|---|---|---|
| **Catálogo** — proyecto / evento | `project` | **`branch`** (centro de trabajo + geocerca) | ↔ bidireccional |
| **Catálogo** — asignaciones | `projectcrew` | asignación de trabajador al branch/proyecto | ↔ bidireccional |
| **Trabajo** — tareas | — (no existe) | módulo `tasks`, **derivadas de la asignación** | solo encodeBiz |
| **Tiempo** — jornada (fichaje) | `timeregistration` | checklog / jornada (envoltorio, **⊇ varias tareas**) | → a Rentman (autoridad por decidir) |
| **Tiempo** — desglose por tarea/función | `timeregistrationactivity` | imputación de la tarea a proyecto/función | → a Rentman (opcional, costes) |
| **Cliente / contacto** | `contact` (`customer`) | **Fase 2** — estructura Clientes a nivel checkbiz (no del módulo) | ⏳ Fase 2 |

**Reglas clave:**
- El **proyecto/evento** de Rentman es el **branch** (donde se ficha); el **cliente NO es un branch**.
- La **asignación → genera tareas** (el trabajo); la **jornada es el envoltorio de tiempo** y contiene varias tareas.
- La estructura de **Clientes/Contactos es de plataforma (Fase 2)**, no de este módulo. Ver `05_fases.md`.

## 4. Índice

- [`01_as-is.md`](01_as-is.md) — la API de Rentman **real**, verificada contra la cuenta (objetos, referencias, endpoints, quirks).
- [`02_to-be.md`](02_to-be.md) — arquitectura objetivo: sync bidireccional por polling desde `sync`.
- [`03_decisiones-abiertas.md`](03_decisiones-abiertas.md) — lo que falta cerrar antes de implementar.
- [`04_activacion-saas.md`](04_activacion-saas.md) — add-on de pago: activación, configuración y reutilización de la monetización (servicio + planes en Firestore, como checkbiz/passbiz).
- [`05_fases.md`](05_fases.md) — alcance por fases (Fase 1 = integración; Clientes/Contactos = Fase 2 de plataforma).
- [`06_mapeo-y-validacion.md`](06_mapeo-y-validacion.md) — cómo se garantiza la integridad de `Branch`/`Employee` en la sync (validación, defaults, estado "pendiente de completar").
- [`adr/`](adr/) — decisiones de arquitectura.

## 5. Estado del código

Existe un **esqueleto** en su **microservicio propio** `encodebiz-api/services/rentman/`
(dominio, cliente HTTP con backoff/paginación, cifrado de token, mapping en PostgreSQL,
migración `002_rentman.sql`, script de Fase 0). Puerto **3008**, plantilla del servicio
`documents`, rutas bajo `/api/v1/rentman`.

- **Extraído de checkinbiz** a servicio propio el 2026-07-28 (rama `feat/rentman-service`,
  commit `2051c13`). checkinbiz quedó sin código de Rentman. Ver `adr/0002`.
- Se construyó asumiendo push de horas one-way vía webhooks; **este plan lo reorienta** a
  sync bidireccional por polling. Los parsers de campos son provisionales — los docs los
  corrigen con datos reales.

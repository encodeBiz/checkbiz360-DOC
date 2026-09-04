# Eventos y Webhooks — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** plataforma (transversal — checkinbiz, tareas, documentos, facturación)
**Fecha de inicio:** 2026-08-26
**Estado:** Núcleo implementado y desplegado en desarrollo. Emisión pendiente — hoy no sale
ningún evento de negocio (ver [07](./07_estado-verificado.md))
**Autor:** Jose Acevedo

---

## Contexto y Motivación

La plataforma ya tiene un módulo de webhooks salientes construido y funcionando: catálogo de
eventos por servicio, firma HMAC, cola de entregas con reintentos y backoff, dead-letter y
endpoints de gestión por entidad. Vive en `encodeBiz-SAAS/functions/src/core/webhook` y hoy
emite dos eventos de asistencia y doce de passinbiz.

Tres cosas obligan a rehacerlo, no a ampliarlo:

1. **passinbiz se descontinúa.** Doce de los catorce eventos del catálogo desaparecen con él.
2. **El catálogo tiene que crecer mucho.** Fallos de fichaje, incidencias automáticas,
   solicitudes de cambio y su aceptación, y el CRUD completo de tareas, documentos, horarios,
   empleados y centros. De catorce eventos a unos cincuenta.
3. **El emisor está en el sitio equivocado.** Los lanzadores son triggers de Firestore, y la
   mayor parte de las escrituras que deben generar eventos ya no pasan por Firestore desde
   Firebase: pasan por casos de uso del contenedor.

A eso se suma que **`encodeBiz-SAAS` es un repositorio en retirada**. Todo lo que se toque
ahora se trae a `encodebiz-api` — no se invierte una línea más en el otro lado.

---

## Principio de diseño

> **El evento se emite donde ocurre la acción. La entrega se intenta en el acto. La cola
> existe para sobrevivir al intento, no para desacoplar el camino crítico.**

Emitir donde ocurre la acción significa: en el caso de uso que escribe, no en un trigger que
observa la escritura. El trigger es la excepción para lo que todavía no pasa por el
contenedor, y encoge conforme la migración avanza.

---

## Índice

| Documento | Qué contiene |
|---|---|
| [01_as-is.md](./01_as-is.md) | El módulo hoy: mapa, flujo, datos, límites reales y el desfase entre repo y producción |
| [02_to-be.md](./02_to-be.md) | La arquitectura destino en `encodebiz-api` |
| [03_catalogo-de-eventos.md](./03_catalogo-de-eventos.md) | Catálogo completo, convención de nombres y **dónde va cada lanzador** |
| [04_contrato-publico.md](./04_contrato-publico.md) | El contrato que ve quien integra: firma, cabeceras, idempotencia, reintentos, versionado |
| [05_fases.md](./05_fases.md) | Plan de ejecución por oleadas, con el estado de cada una |
| [06_integracion-front.md](./06_integracion-front.md) | Lo que el panel necesita para pintar y gestionar los endpoints |
| [07_estado-verificado.md](./07_estado-verificado.md) | **Qué se midió y qué salió** en desarrollo, y los dos problemas abiertos |
| [08_prueba-de-los-33-eventos.md](./08_prueba-de-los-33-eventos.md) | Los 33 eventos que emiten, **qué acción dispara cada uno** y la sonda que lo comprueba |
| [adr/](./adr) | Decisiones (ADR-001 … ADR-006) |
| [tdr/](./tdr) | Diseño técnico detallado (TDR-001) |

---

## Estado de un vistazo

- Módulo original: `encodeBiz-SAAS/functions/src/core/webhook`, rama `feat/webhooks` ya
  fusionada en `main` (2026-07-24). Su documentación propia está en
  `encodeBiz-SAAS/DOCS/modulos/webhooks` (ADR-001…005 + TDR-001) y se conserva como
  referencia histórica.
- Producción (`firebase functions:list`, comprobado el 2026-08-26, **no revisado desde
  entonces**): faltaban por desplegar el emisor `onChecklogWebhook` y los endpoints
  `listWebhookEndpoints` y `toggleWebhookEndpoint`.
- Desarrollo (comprobado el 2026-09-04): el módulo nuevo está desplegado y **entrega** —medido
  de punta a punta, 158 ms y 200 del receptor—, pero **ningún caso de uso emite todavía**. Las
  tres funciones que faltaban en producción sí están aquí, y el módulo viejo sigue vivo sobre
  la misma colección de endpoints. Detalle y evidencia en [07](./07_estado-verificado.md).
- De los 53 eventos diseñados, **el catálogo declara 33, y los 33 emiten** —comprobados uno a
  uno contra desarrollo, ver [08](./08_prueba-de-los-33-eventos.md)—. Los otros 20 están
  comentados en `catalogue.ts` con lo que hay que portar: 12 esperando su CRUD, 7 con el camino
  duplicado y 1 sin emisor posible. El desglose, en [03 §3](./03_catalogo-de-eventos.md).
- Destino: `encodebiz-api`. Nada nuevo en `encodeBiz-SAAS`.

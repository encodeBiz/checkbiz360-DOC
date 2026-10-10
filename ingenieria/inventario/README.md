# Módulo de Inventario — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Inventario (add-on de pago)
**Fecha de inicio:** 2026-09-28
**Estado:** Fases 0–5 en `staging` de API, panel (local, `npm run start:dev`) y app, al 2026-10-08, con la forma final del panel (todo es material, una sola entrada, índice de búsqueda y paginación en servidor, pestañas en una página) · Fase 6 diseñada, sin código · sin pasar a producción (ver [05 §Lo que exige cada entorno](./05_fases.md): precio de Stripe en vivo y alta del servicio, variables en Vercel, compose y nginx de prod, migración `023`, índices compuestos de `items` con `--project` explícito y `reindex-search --apply` por entidad)
**Autor:** Jose Acevedo

---

## Contexto y Motivación

Dos clientes han pedido inventario. Pero un almacén lo vende cualquiera y lo vende barato:
si el módulo se construye como un ERP pequeño —entradas, salidas y un contador— compite con
productos que llevan veinte años haciendo eso mejor.

Lo que aquí se puede construir y en otro sitio no es la frase completa:

> *este material salió con Juan, en la tarea 482, en el domicilio del cliente, a las 10:40,
> y hay foto.*

Todo eso ya está en la plataforma. La tarea sabe su sucursal, sus empleados asignados, su
geocerca, su rastro de actividad, sus evidencias y su validación. Lo único que falta en ese
registro es **qué se gastó**. Añadir un campo a algo que ya existe cuesta poco aquí y cuesta
un producto entero en cualquier otro sitio.

## Principio de diseño

> **El inventario no es el almacén: es el consumo atado a una tarea, a una persona, a un
> sitio y a una hora. El almacén es solo de dónde salió.**

De ahí se derivan las tres decisiones que gobiernan todo lo demás:

1. **La tarea es el punto de entrada desde el campo**; el almacén, el de administración.
2. **Consumibles y operables son el mismo artículo** con distinto tipo, no dos productos.
3. **Un solo camino de escritura.** La app y el panel hablan con `inventory` por HTTP, e
   `inventory` escribe el movimiento y el saldo juntos. El instante vive en Firestore —donde
   vive el resto del dominio— y el histórico en Postgres.

## Alcance

**Dentro (v1):** catálogo de artículos (consumibles y operables), almacenes y a qué sucursales
sirven, existencias con mínimo y aviso, ejemplares de operable con su agenda, movimientos
(entrada, reserva, liberación, salida, consumo, devolución, ajuste, traspaso), consumo desde la
tarea en la app, **conciliación del sobrante al validar**, reserva de operables a tareas con
detección de choque, tablero de ocupación, espejo a Postgres, informe de consumo y puerta de
suscripción.

**Fuera (explícitamente):** trabajo sin conexión —fase posterior, con su boceto en
[06 §D3](./06_decisiones-abiertas.md)—; valoración de existencias (FIFO, precio medio) — en v1
hay coste unitario en la ficha y el informe multiplica; recuento físico masivo; códigos de
barras y QR; mantenimiento preventivo por contador de uso; tiempo mínimo entre asignaciones
(traslado y descanso); poda de movimientos en Firestore.

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | Qué hay hoy, qué se reutiliza de verdad y qué no existe |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Servicio `inventory:3016`, un solo camino de escritura, reparto Firestore/Postgres |
| 03 | [Modelo de datos](./03_modelo-de-datos.md) | Colecciones, campos, relaciones y espejo en Postgres |
| 04 | [Contratos de API](./04_contratos-api.md) | Rutas, auth, permisos, request/response |
| 05 | [Fases de implementación](./05_fases.md) | Roadmap por uso, con la partida de app en cada fase |
| 06 | [Decisiones abiertas](./06_decisiones-abiertas.md) | Lo que falta por responder, y lo aplazado con su boceto |
| 07 | [Operables con papeles](./07_operables-documentos-y-entregas.md) | Documentos y revisiones del ejemplar, entrega a personas con acuse, prueba para una inspección (Fase 6, diseño) |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-servicio-inventory-add-on-de-pago.md) | Servicio `inventory` dedicado, contratable como add-on de pago | Aceptado |
| [ADR-002](./adr/ADR-002-almacen-entidad-propia-multisucursal.md) | El almacén es entidad propia y sirve a varias sucursales | Aceptado |
| [ADR-003](./adr/ADR-003-un-catalogo-consumible-y-operable.md) | Un solo catálogo de artículos, con tipo consumible u operable | Aceptado |
| [ADR-004](./adr/ADR-004-asignar-no-es-consumir.md) | Asignar no es consumir: reserva, salida, declaración y sobrante | Aceptado |
| [ADR-005](./adr/ADR-005-instante-firestore-historico-postgres.md) | Un solo camino de escritura; instante en Firestore, histórico en Postgres | Aceptado |
| [ADR-006](./adr/ADR-006-operable-se-asigna-a-tareas-con-hora.md) | El operable se asigna a tareas con hora, no a obras por rango | Aceptado |
| [ADR-007](./adr/ADR-007-entrega-es-asignacion-con-acuse.md) | La entrega de un ejemplar es una asignación con acuse; su papel es el documento de siempre | Propuesto |
| [ADR-008](./adr/ADR-008-liberar-no-es-devolver-la-posicion-del-ejemplar.md) | Liberar no es devolver: la agenda la suelta el supervisor y la posición del ejemplar lleva su propio rastro («¿dónde queda?», recepción en almacén sin bloquear) | Aceptado |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-colecciones-y-maestros.md) | Colecciones, maestros y puerta de suscripción | 0–1 | Diseño aprobado |
| [TDR-002](./tdr/TDR-002-saldos-movimientos-y-conciliacion.md) | Saldos, libro de movimientos y conciliación del sobrante | 2 | Diseño aprobado |
| [TDR-003](./tdr/TDR-003-operables-agenda-y-choque.md) | Operables: agenda, detección de choque y tablero | 3 | Diseño aprobado |
| [TDR-004](./tdr/TDR-004-espejo-postgres-e-informes.md) | Espejo a Postgres desde `inventory`, migración 023 e informes | 4 | Diseño aprobado |
| [TDR-005](./tdr/TDR-005-material-en-el-informe-de-tareas.md) | El material de cada tarea en el informe de tareas, solo con el add-on | — | Implementado, en staging |
| [TDR-006](./tdr/TDR-006-material-en-el-panel-y-en-merlin.md) | El material en el panel operativo y en Merlin: motivos de centro, quinto eje de la persona, claves para el relato | — | Diseño aprobado, sin código |
| [TDR-007](./tdr/TDR-007-importacion-masiva-por-plantilla.md) | Importación masiva por plantilla de almacén: dos modelos, dos ejemplos con `ELIMINAR`, propuesta antes de aplicar | — | Implementado en rama, sin fusionar |

---

## Estado del roadmap

- [x] **Fase 0** — Fundación: `inventory:3016`, `/health`, compose, nginx, puerta de suscripción y alta del servicio en `billing` ✔ en `develop` (2026-09-28)
- **Panel, forma final (2026-10-07)**: dos pestañas (Existencias = centro de mando con todos los artículos, Almacenes); la ficha del artículo lleva existencias/movimientos o ejemplares/calendario; informe como acción; material asignado al crear la tarea. Ver 05 §«Panel: la forma final».
- [x] **Fase 1** — Maestros: artículos, almacenes, ejemplares ✔ API y panel en `develop` (2026-09-29)
- [x] **Fase 2** — Consumibles de punta a punta: existencias, movimientos, consumo desde la tarea y **conciliación al validar** ✔ API, panel y app en `develop` (2026-09-29)
- [x] **Fase 3** — Operables: reserva a tarea, choque y tablero de ocupación ✔ API, panel (pestaña «Ocupación», agenda por ejemplar) y app en `develop` (2026-09-29)
- [x] **Fase 4** — Espejo a Postgres desde `inventory` e informe de consumo ✔ API y panel (informe, con el libro como descarga CSV) en `develop` (2026-09-29; sin pestaña de libro desde el 2026-10-07); migración `023` y variables pendientes de aplicar en dev
- [x] **Fase 5** — Avisos de mínimo y listado de discrepancias ✔ API y panel en `develop` (2026-09-29; las discrepancias son un filtro de Existencias con aviso, no una pestaña, desde el 2026-10-07)
- [ ] **Fase 6** — Operables con papeles: documentos y revisiones del ejemplar (rojo y aviso, sin bloquear), entrega a personas con acuse, e informe «Equipos y EPIs» en Informes para la inspección. **Diseñada el 2026-10-07, corregida el 2026-10-08; 6a (entrega con acuse, «Mi material», informe Equipos y EPIs) hecha el 2026-10-08, API en staging** ([07](./07_operables-documentos-y-entregas.md), [ADR-007](./adr/ADR-007-entrega-es-asignacion-con-acuse.md)); el acuse, con biometría y escalera de alternativas (D8, decidida)
- [x] **Material en el informe de tareas** — con el add-on, tres columnas más en «Tareas» y una hoja «Material»; sin él, el informe de siempre. **En `develop` y `staging` desde el 2026-10-08, desplegado en dev; pendiente de pase a producción** ([TDR-005](./tdr/TDR-005-material-en-el-informe-de-tareas.md))
- [ ] **Material en el panel operativo y en Merlin** — el material como fuente para las tres preguntas del panel y quinto eje de la fiabilidad; sin add-on, nada. Prerrequisito: las tareas en Postgres. **Diseñado el 2026-10-09, sin código** ([TDR-006](./tdr/TDR-006-material-en-el-panel-y-en-merlin.md))
- [ ] **Posición del ejemplar** — liberar no es devolver: al liberar a mano el supervisor dice dónde queda (sitio, almacén o persona), la tarea cerrada lo deja en su sitio, «Recibir en almacén» sin bloquear la agenda, y el tablero marca lo libre fuera de base. **Decidido el 2026-10-10; app hecha el mismo día (libera ya con la API de hoy y pregunta «¿Dónde queda?» en cuanto la API mande `position`); API y panel pendientes** ([ADR-008](./adr/ADR-008-liberar-no-es-devolver-la-posicion-del-ejemplar.md))
- [ ] **Importación masiva de artículos** — plantilla por almacén y por tipo, dos ejemplos con `ELIMINAR`, propuesta fila a fila y confirmar. **Implementado el 2026-10-09 en `feat/inventario-importacion-masiva` (API y panel), probado contra dev, sin fusionar** ([TDR-007](./tdr/TDR-007-importacion-masiva-por-plantilla.md))

**Lo que sale de otro repo:** las pantallas de la app —material de la tarea, selector de
almacén, consumo precargado, paso de cuadre— y las del panel son el camino crítico de las
Fases 2 y 3, se liberan a mano y llevan su propia partida en cada fase ([05](./05_fases.md)).

**Sobre `sync`:** el espejo de este módulo **no pasa por `sync`** —lo escribe `inventory` en la
misma petición y lo reintenta un job propio—, así que su falta de reintentos (detectada el
2026-09-28 sobre los checklogs) no afecta aquí. Queda documentada en
[01](./01_as-is.md#limitaciones-del-entorno-que-condicionan-el-diseño) porque sí afecta a lo
demás.

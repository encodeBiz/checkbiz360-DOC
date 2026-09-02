# Disponibilidad — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Calendario (Horarios y festivos) → Disponibilidad
**Fecha de inicio:** 2026-09-02
**Estado:** Diseño / Pre-implementación
**Autor:** Jose Acevedo

---

## Contexto y Motivación

El apartado de **Disponibilidad** responde a una pregunta operativa que hoy no responde nadie:
*cuánta gente hay realmente disponible cada día, y quién falta*. No es un dato guardado en
ningún sitio; sale de cruzar tres cosas que ya existen por separado —el horario efectivo, los
festivos y las ausencias— contra la plantilla.

Existe un prototipo funcional del tablero en el front
(rama `feat/disponibilidad-horarios` de `encodebiz-front-saas`) que hace ese cruce **en el
navegador**. Funciona, y sirve para haber fijado la semántica; pero la forma en que se trae los
datos no es defendible en producción:

1. **Una lectura de Firestore por empleado.** Con 200 empleados son 200 peticiones sueltas
   desde el navegador de cada persona que abra la pestaña, cada vez que la abre. La latencia
   crece en línea recta con la plantilla.
2. **Obliga a abrir las reglas de Firestore.** Para cruzar hay que poder leer el calendario de
   *todos* los empleados desde el cliente.
3. **Un permiso denegado se convierte en un número optimista.** La lectura fallida se
   interpreta como "sin ausencias", o sea, como empleado **disponible**. En un tablero de
   cobertura, el peor fallo posible: no avisa, miente.
4. **Tercera copia de la regla de herencia** entidad → sucursal → empleado, que ya vive
   resuelta en `ResolveEffectiveCalendarUseCase`.

---

## Principio de diseño

> **La disponibilidad no es un dato nuevo: es una lectura derivada del calendario. La calcula
> quien ya es dueño de la regla de herencia, y la calcula una vez.**

El módulo `calendar` gana dos endpoints de solo lectura. El front deja de cruzar nada: pide la
rejilla y la pinta.

---

## Alcance

**Dentro:** la agregación por sucursal y día (`available` / `total`), el desglose de un día
concreto (quién está y por qué no está el resto), la retirada del cálculo del front, y el alta y
borrado de ausencias desde el propio desglose
([ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md),
[ADR-004](./adr/ADR-004-ausencias-retribuidas.md)) — que no necesita backend nuevo, porque
reusa `PATCH` y `DELETE` del handler de calendario.

**Fuera:** el modelo de `Absence` con rango real (hoy son N festivos de un día — ver
[modulos/calendario.md](../../modulos/calendario.md) §6.8); la materialización o caché de la
rejilla; la asignación de turno por día y sucursal, que no existe en el modelo y sin la cual no
se puede distinguir "libra" de "trabaja hoy en otro centro".

---

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | El prototipo en el front, el módulo calendario, los datos y lo que cuesta hoy |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | La agregación baja al módulo calendario; frontera y reparto |
| 03 | [Contratos de API](./03_contratos-api.md) | `action=availability` y `action=availabilityDay`: auth, permisos, request/response |
| 04 | [Fases de implementación](./04_fases.md) | Roadmap: contrato → denormalización → endpoints → cutover del front |
| 05 | [Integración: Front de administración](./05_integracion-front.md) | Qué conserva el front y qué borra |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md) | La disponibilidad la agrega el módulo `calendar`, no el front ni un servicio nuevo | Propuesto |
| [ADR-002](./adr/ADR-002-entityid-en-los-documentos-de-calendario.md) | Denormalizar `entityId` en los documentos `calendar/config` para poder consultarlos en una sola query | Propuesto |
| [ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md) | El desglose del día escribe ausencias: arrastre **y** botón, y sólo se revierte lo que es ausencia propia | Propuesto |
| [ADR-004](./adr/ADR-004-ausencias-retribuidas.md) | La ausencia registra si es retribuida; "no consta" no es "no" | Propuesto |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) | Cálculo de disponibilidad: plan de lectura, reglas y límites | 2 | Diseño |

---

## Estado del roadmap

- [x] **Fase 0** — Contrato y documentación (este documento)
- [ ] **Fase 1** — `entityId` en los documentos `calendar/config` (camino de escritura + backfill)
- [ ] **Fase 2** — `action=availability` y `action=availabilityDay` en `calendarHandler`
- [ ] **Fase 3** — Cutover del front: el tablero consume el endpoint y se borra el cruce local
- [ ] **Fase 4** *(futuro)* — Materialización de la rejilla si la latencia lo pide; `Absence` con rango real

**Prototipo:** el tablero está implementado y funcionando contra el cruce local en
`feat/disponibilidad-horarios` (`encodebiz-front-saas`). **No se fusiona** hasta la Fase 3: la
vista es la buena, la capa de datos no. Ver [05](./05_integracion-front.md).

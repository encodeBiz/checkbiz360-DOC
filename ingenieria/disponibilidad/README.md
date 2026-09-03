# Disponibilidad — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Calendario (Horarios y festivos) → Disponibilidad
**Fecha de inicio:** 2026-09-02
**Estado:** Diseño cerrado · pendiente de implementar
**Autor:** Jose Acevedo

---

## Contexto y Motivación

El apartado de **Disponibilidad** responde a una pregunta operativa que hoy no responde nadie:
*cuánta gente hay realmente disponible cada día, y quién falta*. No es un dato guardado en
ningún sitio; sale de cruzar tres cosas que ya existen por separado —el horario efectivo, los
festivos y las ausencias— contra la plantilla.

Existe un prototipo funcional del tablero en el front (rama `feat/disponibilidad-horarios` de
`encodebiz-front-saas`) que hace ese cruce **en el navegador**. Funciona, y sirvió para fijar la
semántica; pero la forma en que se trae los datos no es defendible en producción:

1. **Una lectura de Firestore por empleado.** Con 200 empleados son 200 peticiones sueltas desde
   el navegador de cada persona que abra la pestaña, cada vez que la abre.
2. **Obliga a abrir las reglas de Firestore**, para poder leer el calendario de *todos* los
   empleados desde el cliente.
3. **Un permiso denegado se convierte en un número optimista.** La lectura fallida se interpreta
   como "sin ausencias", o sea, como empleado **disponible**. En un tablero de cobertura, el peor
   fallo posible: no avisa, miente.
4. **Tercera copia de la regla de herencia** entidad → sucursal → empleado.

---

## Principio de diseño

> **La disponibilidad no es un dato nuevo: es una lectura derivada del calendario. La calcula
> quien ya es dueño de la regla de herencia, y la calcula una vez.**

El módulo `calendar` del **contenedor** gana dos rutas de solo lectura. El front deja de cruzar
nada: pide la rejilla y la pinta.

---

## Alcance

**Dentro:** la agregación por sucursal y día (`available` / `total` / `closed`), el desglose de un
día concreto (quién está y por qué no está el resto), el alta y borrado de ausencias desde el
propio desglose ([ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md),
[ADR-004](./adr/ADR-004-ausencias-retribuidas.md)) —que no necesita contrato nuevo, porque reusa
las escrituras de calendario—, la retirada del cálculo del front, y el snapshot del calendario
resuelto en Postgres.

**Fuera:** el modelo de `Absence` con rango real, que existe pero no se usa; y la asignación de
turno por día y sucursal, sin la cual quien está en dos centros cuenta en los dos.

---

## Lo que cambió al verificar contra el código y los datos

El diseño se escribió primero desde una foto del backend que resultó no ser la actual. Tres
correcciones de fondo, todas comprobadas:

- **El módulo `calendar` ya no es una Cloud Function**, o no del todo: la lectura está en el
  contenedor y la regla en `@encodebiz/shared`; en Firebase quedan las escrituras y una copia
  entera del caso de uso. Por eso las rutas nuevas van al contenedor.
- **El contenedor no comparte datacenter con Firestore** (OVH contra GCP), así que lo que hay que
  minimizar son las idas y vueltas, no las lecturas facturadas.
- **`concatHolidays` tira el nivel de origen de los festivos.** Verificado en dev: la Navidad de
  la entidad, el festivo de la sucursal y ocho días de vacaciones propias vuelven
  indistinguibles. Sin ese dato el tablero pintaría en gris —"nadie trabaja y nadie debería"— un
  miércoles normal en el que la sucursal se queda sin cubrir.

Se valoró además retirar la taxonomía de motivos y dejar dos listas de nombres. **Se descartó**:
el desglose no es solo lectura —escribe ausencias—, y una superficie de escritura tiene que saber
qué puede escribir. Lo que sí se simplificó es cómo se calcula: la tabla de precedencias de
cuatro niveles se reduce a un reparto entre motivo colectivo y personal, del que salen tanto
`closed` como la etiqueta.

---

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | El prototipo en el front, el módulo calendario partido en dos, y lo que cuesta hoy |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Dónde viven las rutas, frontera y reparto |
| 03 | [Contratos de API](./03_contratos-api.md) | `/availability` y `/availability/day`: auth, permisos, request/response |
| 04 | [Fases de implementación](./04_fases.md) | Roadmap y dependencias |
| 05 | [Integración: Front de administración](./05_integracion-front.md) | Qué conserva el front y qué borra |
| 06 | [Tareas sueltas](./06_tareas.md) | `paid` y `source`: qué tocan y por qué no rompen nada |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md) | La disponibilidad la agrega el módulo `calendar` del contenedor | Aceptado |
| [ADR-002](./adr/ADR-002-entityid-en-los-documentos-de-calendario.md) | Denormalizar `entityId` en los documentos `calendar/config` | Aceptado — aplazado |
| [ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md) | El desglose del día escribe ausencias: arrastre **y** botón, y sólo se revierte lo que es ausencia propia | Propuesto |
| [ADR-004](./adr/ADR-004-ausencias-retribuidas.md) | La ausencia registra si es retribuida; "no consta" no es "no" | Propuesto |
| [ADR-005](./adr/ADR-005-snapshot-del-calendario-resuelto-en-postgres.md) | El calendario resuelto se cachea en Postgres, con fallo honesto | **Aplazado por medición** |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) | Cálculo de disponibilidad: plan de lectura, reglas y límites | 2 | Diseño |

---

## Estado del roadmap

- [x] **Fase 0** — Contrato y documentación
- [x] **Fase 1** — Portar el módulo `calendar` al contenedor · *verificada en dev*
- [x] **Fase 2** — `source` en `concatHolidays` y `paid` en `Holiday` · *verificada en dev*
- [x] **Fase 3** — Los dos casos de uso y sus rutas en el `calendarRouter` · *verificada en dev*
- [x] **Fase 4** — Cutover del front · **validado en pantalla el 2026-09-03** (+ 4-bis: el desglose escribe, pendiente)
- [~] **Fase 5** — Snapshot del calendario resuelto · **aplazada**: la rejilla tarda 437 ms con 21 empleados y una sola persona 258, así que el coste lo manda lo fijo y no la plantilla ([ADR-005](./adr/ADR-005-snapshot-del-calendario-resuelto-en-postgres.md) §Medición)
- [ ] **Suelto** — `dim_calendars` se sincroniza a mano y `BuildPlannedHours` depende de ella. Es problema de hoy y se arregla sin el snapshot

El porte va primero porque, mientras el panel escriba contra Firebase, cada cambio de tipo hay
que hacerlo en dos repos; con él hecho, la Fase 2 se toca sólo en `shared`. La 5 **no** debe
adelantarse a la 3: cachear algo sin verificar convierte un bug en un bug persistido.

**Prototipo:** la rama `feat/disponibilidad-horarios` de `encodebiz-front-saas` ya no cruza nada
—consume los dos endpoints— y está lista para fusionar cuando se compruebe en pantalla.

**Verificado en dev el 2026-09-02**, contra la entidad de pruebas y por HTTP:

- **Fase 1** — alta y borrado de festivo en los tres scopes, ausencia con rango, solapamiento
  rechazado, validaciones y 404 en borrado inexistente. Sin residuos.
- **Fase 2** — `packages/shared/src/scripts/verificar-source-festivos.ts`: nada cambia salvo el
  campo nuevo y el crudo no se contamina.
- **Fase 3** — la prueba del §8: los doce días de la rejilla coinciden con `GET /calendar`
  resuelto individualmente. Y la distinción que motivaba todo: un miércoles con la plantilla de
  vacaciones sale **rojo** y un festivo de empresa sale **gris**.
  `packages/shared/src/scripts/verificar-disponibilidad.ts` la deja repetible sin red.

**Validado en pantalla el 2026-09-03.** Los 30 días de septiembre coinciden uno a uno con lo que
devuelve `GET /availability`, contrastados contra la entidad de pruebas con 21 de plantilla. Lo
que prueba el contraste no es que los números salgan, sino que **el `source` llega hasta el
pintado**: el 16 (festivo de sucursal) y el 24 (festivo de entidad) salen **grises**, y el 25
—medio equipo de asuntos propios un viernes laborable— sale **rojo, 10 de 21**. Antes de la
Fase 2 los tres eran indistinguibles y habrían salido iguales.

Pendiente de mirar, sin bloquear: el panel del desglose al pinchar un día. Sus datos sí están
verificados contra la API (10 dentro, 11 fuera, diez reversibles y una por estado de ficha); lo
que no se ha visto es cómo los pinta.

Queda mover `NEXT_BACKEND_URI_CHECKINBIZ_CALENDAR_HANDLER` en **producción**, y fusionar
`feat/disponibilidad-horarios`.

**Banco de pruebas:** entidad `Wl8ZCvpdmIXzEE0mhT7W` en dev, con festivo de entidad, festivo de
sucursal, ocho días de vacaciones propias y overrides desactivados en dos niveles. Le faltan un
segundo centro y alguien en los dos.

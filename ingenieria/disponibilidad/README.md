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
| [ADR-005](./adr/ADR-005-snapshot-del-calendario-resuelto-en-postgres.md) | El calendario resuelto se cachea en Postgres, con fallo honesto | Aceptado — tras la Fase 2 |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) | Cálculo de disponibilidad: plan de lectura, reglas y límites | 2 | Diseño |

---

## Estado del roadmap

- [x] **Fase 0** — Contrato y documentación
- [ ] **Fase 1** — `source` en `concatHolidays` y `paid` en `Holiday` — *bloquean el resto*
- [ ] **Fase 2** — Los dos casos de uso y sus rutas en el `calendarRouter`
- [ ] **Fase 3** — Cutover del front → **tablero vivo**
- [ ] **Fase 4** — Portar las escrituras del calendario al contenedor
- [ ] **Fase 5** — Snapshot del calendario resuelto (ADR-003)

Las fases 4 y 5 son rendimiento y van después de tener el tablero funcionando. La 5 **no** debe
adelantarse a la 2: cachear algo sin verificar convierte un bug en un bug persistido.

**Prototipo:** el tablero está implementado contra el cruce local en `feat/disponibilidad-horarios`
(`encodebiz-front-saas`). **No se fusiona** hasta la Fase 3: la vista es la buena, la capa de
datos no. Ver [05](./05_integracion-front.md).

**Banco de pruebas:** entidad `Wl8ZCvpdmIXzEE0mhT7W` en dev, con festivo de entidad, festivo de
sucursal, ocho días de vacaciones propias y overrides desactivados en dos niveles. Le faltan un
segundo centro y alguien en los dos.

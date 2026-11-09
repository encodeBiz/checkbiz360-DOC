# Cartera de clientes — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Cartera de clientes (**core, gratuito**) · Portal del cliente (**add-on**, fase dos)
**Fecha de inicio:** 2026-10-29
**Estado:** Diseño cerrado en conversación con Jose el 2026-10-29; **revisado el 2026-11-03**: la cartera básica pasa a ser gratuita y parte del core, y el portal del cliente queda como add-on **aplazado** con boceto en [07](./07_portal-del-cliente.md) · Fase 0 y API de la Fase 1 **en staging** desde el 2026-11-03; panel de la Fase 1 hecho, en prueba local
**Autor:** Jose Acevedo

---

## Contexto y Motivación

La plataforma hoy sabe **quién** trabajó, **dónde**, **cuándo**, con **qué material** y con **qué
foto**. Lo que no sabe es **para quién**. Y en los sectores a los que vende —limpieza, ayuda a
domicilio, eventos, montajes, construcción— el trabajo siempre es para alguien: una comunidad
de vecinos, una persona a la que se cuida en casa, una agencia que monta una boda, una
constructora con tres obras.

El hueco se nota ya en producción, de dos formas distintas:

- **Neteges** tiene 142 sucursales dadas de alta y 28 empleados. Las sucursales no son
  sucursales: son sus clientes. Solo 34 tienen a alguien asignado, 11 personas no están en
  ninguna, y 32 de sus 97 fichajes del último mes se rechazan por estar fuera de radio. Es un
  caos porque el modelo les obligó a llamar «sucursal» a lo que era «cliente». Se les propuso
  el horario por tareas con una sola sucursal (demo en staging el 2026-10-29): la pieza que
  falta para cerrar ese camino es que la tarea sepa de qué cliente es.
- Una empresa de **ayuda a domicilio** crea una tarea por clienta y necesita que la auxiliar
  tenga el expediente a mano. Se resolvió con un adjunto en la tarea
  ([tasks TDR-007](../tasks-service/tdr/TDR-007-adjuntos-en-la-tarea.md), en producción
  desde el 2026-11-02) y se dejó escrito que la cartera de clientes era otro módulo, con sus
  tareas y documentos colgando de cada cliente. Este es ese módulo.

Un CRM lo vende cualquiera. Un ERP lo venden veinte. Lo que aquí se puede construir y en otro
sitio no es la frase completa:

> *para la comunidad de Diagonal 400, en octubre, fueron 31 horas de Marta y de Luis, estas
> son las 62 fotos, este el material, esto es lo facturable, y la presidenta lo ha firmado.*

Todo eso ya está en la plataforma menos la primera parte de la frase y la última.

## Por qué el básico es gratis y el portal se cobra

El cliente **no es un extra sobre el producto: es la pieza que le falta al producto** para
que funcione en nuestros nichos. Sin él, el horario por tareas no cierra, la tarea de SAD no
sabe a quién va, la obra no sabe de quién es. Por eso la cartera básica entra en checkinbiz
y se enseña a todo el mundo desde el panel, sin puerta ([ADR-001](./adr/ADR-001-servicio-customers-en-el-core-gratuito.md)).

Lo que se cobra es la fase dos, el **portal del cliente**: un acceso para el cliente de
nuestro cliente, como el quiosco es un acceso para quien no tiene app. La presidenta de la
comunidad, la hija de Juana, el jefe de obra entran por un enlace y ven lo suyo: cuándo
vienen, los documentos que tienen que firmar, el parte del mes con las fotos, un sitio para
pedir algo. Es lo que cierra el círculo entero: la empresa planifica, la trabajadora ficha y
deja evidencia, **el cliente confirma y firma**, el informe sale con todo detrás
([ADR-005](./adr/ADR-005-el-portal-del-cliente-es-el-add-on-como-el-quiosco.md), [07](./07_portal-del-cliente.md)).

## Principio de diseño

> **La cartera no es un CRM: es el «para quién» colgado de lo que ya existe. El cliente es
> una capa por encima de la operación, como el inventario, y nunca la frena.**

De ahí salen las decisiones que gobiernan todo lo demás:

1. **El cliente es una entidad propia y se le asignan sucursales**, de muchos a muchos, igual
   que al almacén se le dicen las sucursales a las que sirve ([ADR-002](./adr/ADR-002-cliente-entidad-propia-con-sucursales-asignadas.md)).
   La sucursal no cambia nada por tener clientes.
2. **La tarea lleva el cliente**, elegido entre los de su sucursal, y se lleva su lugar como
   `workSite`. Hacia abajo, eso es lo único que la operación toca: un campo en la tarea
   ([ADR-003](./adr/ADR-003-la-tarea-lleva-el-cliente-y-las-horas-se-imputan-por-tarea-o-por-sucursal-dedicada.md)).
3. **Hacia arriba, todo lo que es del cliente y no de la operación**: datos, contactos,
   lugares, documentos, contratos, tarifas y presupuestos.
4. **De la tarea baja al cliente lo que ya existe sin pedirlo**: horas, evidencias, material,
   quién fue. Con eso sale el informe por cliente y, si hay tarifa, el importe facturable
   ([ADR-004](./adr/ADR-004-la-tarifa-valora-no-factura.md)).
5. **Nunca es obligatorio.** Una tarea sin cliente es una tarea válida, como hoy lo es una
   tarea sin material. Una empresa sin clientes dados de alta ve el panel de siempre.
6. **Gratis lo que cierra el core; se cobra lo que abre la puerta al cliente.** La cartera
   es de checkinbiz; el portal es el add-on, como el quiosco.

## Alcance

**Dentro (v1, gratis):** clientes (empresa o persona) con contactos y lugares con geocerca;
asignación de clientes a sucursales; el cliente y su lugar en la tarea, con selector filtrado
por sucursal y relleno automático cuando no hay nada que elegir; imputación de horas al
cliente por tarea y por sucursal dedicada; espejo a Postgres; informe por cliente (horas,
tareas, evidencias, material si hay inventario); documentos del cliente por el documental,
con qué ve la persona de campo; contratos con vencimiento en rojo; tarifa por cliente e
importe facturable del periodo; script de conversión de sucursales falsas en clientes para
Neteges.

**Rentabilidad del montaje (Fase 5; core o add-on, D11 abierta):** el contrato —el PDF que
la empresa ya tiene— con su importe, tiempo estimado y complejidad leídos por la IA y
editables; vinculado a una sucursal o a una tarea, que es el montaje; el coste de RRHH y
material sale solo de la operativa, en bruto; margen por montaje y por cliente; previsión en
horquilla a partir de los montajes cerrados
([ADR-006](./adr/ADR-006-el-contrato-es-el-montaje.md)).

**Fase dos (add-on):** el portal del cliente, con su boceto y lo que se copia de otros en
[07](./07_portal-del-cliente.md): acceso por enlace, calendario de visitas, documentación
para leer y firmar, parte del mes con fotos, solicitudes e incidencias, contacto con la
empresa, valoración.

**Fuera (explícitamente):** emitir facturas o integrarse con programas de facturación;
cobrar al cliente final por el portal; Merlin leyendo clientes; elegir cliente al fichar sin
tarea; CRM comercial (oportunidades, pipeline: eso es `sales`, y es de encodeBiz, no de
nuestros clientes); planificación automática de rutas por cliente (la demo de Neteges enseña
que es posible; se diseña aparte si lo piden).

## Documentos de diseño

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual (As-Is)](./01_as-is.md) | Qué hay hoy, qué se reutiliza de verdad y qué no existe |
| 02 | [Arquitectura objetivo (To-Be)](./02_to-be.md) | Servicio `customers:3018` sin puerta, lo poco que toca fuera de su casa |
| 03 | [Modelo de datos](./03_modelo-de-datos.md) | Colecciones, campos, relaciones y espejo en Postgres |
| 04 | [Contratos de API](./04_contratos-api.md) | Rutas, auth, permisos, request/response |
| 05 | [Fases de implementación](./05_fases.md) | Roadmap por uso, Neteges primero, con la partida de panel y app en cada fase |
| 06 | [Decisiones abiertas](./06_decisiones-abiertas.md) | Lo que falta por responder, y lo aplazado con su boceto |
| 07 | [Portal del cliente](./07_portal-del-cliente.md) | Fase dos: qué ve el cliente de nuestro cliente, qué copiamos de otros y qué no, cómo entra, cómo firma |
| 09 | [Guion de QA en staging](./09_guion-qa.md) | Datos sembrados en la demo, pasos del panel y de la app con el resultado esperado, y la limpieza |

## Architecture Decision Records (ADRs)

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-servicio-customers-en-el-core-gratuito.md) | Servicio `customers` dedicado, parte del core de checkinbiz y gratuito; el portal es lo que se cobra | Aceptado (revisado 03-nov) |
| [ADR-002](./adr/ADR-002-cliente-entidad-propia-con-sucursales-asignadas.md) | El cliente es entidad propia y se le asignan sucursales, como al almacén | Aceptado |
| [ADR-003](./adr/ADR-003-la-tarea-lleva-el-cliente-y-las-horas-se-imputan-por-tarea-o-por-sucursal-dedicada.md) | La tarea lleva el cliente; las horas se imputan por tarea o por sucursal dedicada, explícita | Aceptado |
| [ADR-004](./adr/ADR-004-la-tarifa-valora-no-factura.md) | La tarifa valora lo que la plataforma mide; la factura la hace su programa | Aceptado |
| [ADR-005](./adr/ADR-005-el-portal-del-cliente-es-el-add-on-como-el-quiosco.md) | El portal del cliente es el add-on, como el quiosco: dentro de `customers`, con puerta y autenticación propias | Aceptado |
| [ADR-006](./adr/ADR-006-el-contrato-es-el-montaje.md) | El contrato es el montaje: un PDF del cliente vinculado a una sucursal o a una tarea; el coste sale solo y en bruto; la previsión, del histórico | Aceptado (03-nov) |

## Technical Design Records (TDRs)

| ID | Componente | Fase | Estado |
|----|------------|------|--------|
| [TDR-001](./tdr/TDR-001-fundacion-y-maestros.md) | `customers:3018`, clientes, lugares, sucursales asignadas, scripts de conversión y reindexado; panel «Clientes» | 0–1 | API en staging (03-nov); panel en `feat/cartera-de-clientes` sin commitear, probándose en local |
| [TDR-002](./tdr/TDR-002-el-cliente-en-la-tarea.md) | El cliente en la tarea, recortado al MVP | 2 | API en staging; panel y app en ramas, sin publicar (04-nov) |
| [TDR-003](./tdr/TDR-003-documentos-del-cliente.md) | Documentos del cliente: `scope: customer` en el documental | 4 | API en staging; panel commiteado; app en rama (04-nov) |
| [TDR-004](./tdr/TDR-004-rentabilidad-del-montaje.md) | Contratos del cliente (varios a la vez) y su rentabilidad: la tarea dice de qué contrato es; lectura del PDF en `merlin`; coste en bruto de sus tareas; cierre y previsión. Core | 5 | API en staging y panel commiteado (05-nov), sin publicar |
| [TDR-005](./tdr/TDR-005-datos-complementarios-y-nombre-del-cliente.md) | «Datos complementarios» como tarjeta perezosa en la app (encima de «Equipo», oculta si no hay datos) y el nombre del cliente a la plantilla solo con la casilla del cliente, apagada por defecto; lo corta el servidor | 4–5 | API en staging, panel y app commiteados el 07-nov; pase §48 |
| [TDR-006](./tdr/TDR-006-parte-del-cliente.md) | El cliente en los análisis: parte del cliente (PDF con fotos y Excel), pestañas Detalle/Análisis en la ficha, resumen y alertas en Inicio; cliente en `tasks_raw` y `dim_customers` (059) | 3 | API en staging, panel en rama aparte (07-nov); pase §49 |
| [TDR-007](./tdr/TDR-007-analisis-a-fondo-del-cliente.md) | Análisis a fondo del cliente: señales de «lo que hay que mirar», rentabilidad (ingreso repartido, coste por persona con precio de puesto), previsión, colaboración, servicio en tiempo y forma y equipo | 3 | API en staging y panel en la rama de la cartera (07-nov); pase §49 |
| [TDR-008](./tdr/TDR-008-gastos-externos.md) | Gastos externos del contrato (concepto, importe, fecha; 5 y «Cargar más»; lista dinámica en Editar, fila a fila) que entran en la rentabilidad; estudio de gastos desde la tarea (panel y app con aprobación) | 5 | Fase 1 en curso (07-nov) |

---

## Estado del roadmap

- [x] **Fase 0** — Fundación: `customers:3018`, `/health`, compose, nginx, credencial de checkinbiz; sin puerta ni Stripe ✔ API en `feat/customers-fase-1` (2026-11-03), compose y nginx de staging; los de prod en el pase
- [x] **Fase 1** — Clientes (con dirección), lugares y sucursales asignadas; pantalla «Clientes» en el panel. **API en staging** y **panel commiteado** en `feat/cartera-de-clientes` (2026-11-03, [TDR-001](./tdr/TDR-001-fundacion-y-maestros.md)); falta publicar el panel y la prueba del script con Neteges delante
- [ ] **Fase 2 → MVP** — El cliente en la tarea, recortado al MVP (06 §D11, 03-nov): cliente de su sucursal + dirección del cliente por defecto; **sin lugares, dedicadas ni «toda la empresa»**. API en staging ([TDR-002](./tdr/TDR-002-el-cliente-en-la-tarea.md)); panel en `feat/cartera-de-clientes`; falta publicar y la app (bottom sheet)
- [ ] **Fase 3** — Espejo a Postgres, horas e informe por cliente — **APLAZADA sin fecha** (06 §D11): el fichaje va por sucursal y no se reparte entre clientes
- [ ] **Fase 4** — Documentos del cliente ([08](./08_documentos-del-cliente.md), [TDR-003](./tdr/TDR-003-documentos-del-cliente.md)): **API en staging y panel commiteado el 04-nov**; `scope: customer`, tipos propios, permisos como los de sucursal, contrato en rojo al vencer; falta la app y publicar
- [ ] **Fase 5** — **Contratos y rentabilidad** ([TDR-004](./tdr/TDR-004-rentabilidad-del-montaje.md)): el contrato cuelga del cliente y puede haber varios; la tarea dice de cuál es (se pone solo si hay uno vigente); coste en bruto de sus tareas, margen, cierre y previsión. **Core**. **API en staging y panel commiteado el 05-nov**; falta publicar; pase en §35
- [ ] **Fase 6** — **Portal del cliente (add-on)** — **PENDIENTE, aplazado el 03-nov**: acceso por enlace, calendario, documentación con firma, parte del mes, solicitudes, contacto, valoración ([07](./07_portal-del-cliente.md))

**Lo que sale de otro repo:** la pantalla «Clientes», el selector en la tarea y la ficha del
cliente son del panel (`encodebiz-front-saas`); lo que enseña la app (nombre del cliente,
contacto, notas de campo y documentos de campo en el detalle de la tarea) va en una versión
posterior a la 1.10.1. Hasta esa versión, la app enseña la tarea como hoy, con su `workSite`,
y no se pierde nada: el lugar del cliente ya viaja en el campo que la app conoce. El portal es
una web aparte dentro del panel o servida por `customers`, sin app: el cliente entra desde el
móvil con el enlace.

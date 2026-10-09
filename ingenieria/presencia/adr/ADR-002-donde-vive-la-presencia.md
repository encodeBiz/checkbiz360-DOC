# ADR-002 — Dónde vive la lectura de presencia

**Fecha:** 2026-10-09
**Estado:** Abierto · bloquea la fase 1
**Decisionario:** Jose Acevedo

## Contexto

Decidido que el cruce lo hace el servidor ([ADR-001](./ADR-001-el-cruce-lo-hace-el-servidor.md)),
falta decir en qué contenedor. La lectura compone dos módulos que viven en el núcleo
`checkinbiz`: el calendario (vía `ResolveAvailabilityDayUseCase`, en `shared`) y los fichajes.

Y el núcleo tiene una barrera escrita. El
[ADR-003 de salida del monolito](../../salida-del-monolito/adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md)
dice que `checkinbiz` se queda con el camino crítico y con aquello de lo que ese camino depende
para ser correcto, y que **al núcleo no vuelve a entrar nada**. Da dos varas para medir una
incorporación: que su error se manifieste como un fichaje que no cuenta, y que no sea código
que se toque a menudo.

Hay un precedente que complica la lectura: la disponibilidad entró en `checkinbiz` como dos
rutas de lectura del router de calendario, verificadas el 2026-09-02, **seis días antes** de que
se escribiera el ADR-003. Es decir, el precedente existe pero es anterior a la barrera.

## Opciones

### A — En `checkinbiz`, junto a la disponibilidad

`GET /api/v1/checkinbiz/checklogs/presence`, o como extensión del propio desglose del día
(`GET /calendar/availability/day?withPresence=true`).

- A favor: es una lectura derivada de dos módulos que ya están ahí; los casos de uso que
  compone están en `shared` y los repositorios en el propio servicio; cero infraestructura
  nueva; mismo middleware de auth y misma resolución de alcance que la disponibilidad.
- En contra: contradice la letra del ADR-003. Aunque sea sólo lectura, es un motivo más de
  redespliegue del servicio que no puede fallar.
- Medida con las dos varas del ADR-003: **no escribe**, así que su error no puede ser un fichaje
  que no cuenta —la primera vara ni siquiera aplica—; y es una lectura con un contrato cerrado,
  que se tocará poco. Pasa las dos, pero pasarlas no era el criterio: el criterio era no entrar.

### B — Contenedor propio: `presence`

Un servicio pequeño con el andamio de `events`, que importa de `shared` los casos de uso de
calendario y el repositorio de fichajes.

- A favor: respeta el ADR-003 sin discusión. Si mañana la presencia crece —vista de gerente,
  histórico de cumplimiento, avisos— tiene casa propia.
- En contra: un contenedor, un puerto, una entrada en nginx y en `docker-compose`, un
  `/health`, una variable más por entorno, para una ruta. Y lee la misma Firestore desde otro
  proceso en OVH: ni más barato ni más rápido.

### C — En `employees`

Es «la plantilla de la sucursal, con su estado».

- En contra: `employees` es el CRUD de gestión de plantilla, lo que más se toca. Meter ahí una
  lectura operativa del día lo acopla al fichaje por la puerta de atrás. Descartada.

### D — En `analytics`

- En contra: `analytics` es histórico sobre PostgreSQL, alimentado por `sync`. La presencia es
  el ahora operativo sobre Firestore. No encaja ni por dato ni por latencia. Descartada.

## Recomendación

**A**, y dejar constancia aquí de por qué se acepta la excepción, para que la barrera siga
siendo una barrera:

1. Es la misma clase de cosa que la disponibilidad —una lectura derivada de un módulo del
   núcleo, sin estado propio— y conviene que las dos vivan juntas y se desplieguen juntas: si
   cambia el desglose del día, cambia la presencia.
2. No escribe. La barrera del ADR-003 protege el fichaje de escrituras equivocadas y de
   redespliegues frecuentes; una ruta `GET` con contrato cerrado no es ninguna de las dos cosas.
3. El coste de B es real y lo que protege es nominal: el proceso extra leería los mismos
   documentos de la misma base.

Si se elige A, **se añade al ADR-003 una nota** con esta excepción y su criterio: *lecturas
derivadas, sin estado, de módulos que ya están en el núcleo*. Así la próxima incorporación tiene
que argumentar contra una regla y no contra un precedente.

Si Jose prefiere mantener la barrera intacta, **B** es correcta y el contrato de la
[README](../README.md) no cambia: sólo el prefijo de la ruta, y la app sólo cambia una constante.

## Consecuencias de A

- El router `checklog` del núcleo gana su primera ruta de lectura. Hoy sólo tiene escrituras
  (`POST /`, `/update`, `/manual-request`). Alternativa dentro de A: colgarla del router
  `calendar`, que ya es de lectura con alcance por nivel; la ruta sería
  `/calendar/availability/day?withPresence=true` y la respuesta extendería el desglose en vez
  de duplicar sus campos. Es la variante que menos contrato nuevo crea.
- Los códigos de error llevan el prefijo del módulo elegido (`presence/…`, o se reusan
  `calendar/…` en la variante del desglose).

## Pendiente para cerrar

- Elegir A o B.
- Dentro de A, ruta propia bajo `checklogs` o extensión del desglose bajo `calendar`.

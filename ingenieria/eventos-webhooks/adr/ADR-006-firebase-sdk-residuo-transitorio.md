# ADR-006 — `services/firebase_sdk` como residuo transitorio de los triggers

**Fecha:** 2026-08-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Parte del CRUD todavía se ejecuta en Firebase: centros de trabajo, horarios y calendario, el
sanitizador de fichajes y las incidencias. Esas acciones tienen que emitir eventos antes de que
su migración al contenedor termine, y no hay caso de uso propio donde poner la emisión.

En el monorepo de **GroundApp** existe ya el patrón: `services/firebase_sdk`, un paquete dentro
del propio monorepo que contiene **solo triggers** —Firestore, Pub/Sub, Cloud Tasks,
Scheduler—, sin funciones HTTP, y al que el `firebase.json` de la raíz apunta como
`functions.source`. Es el único punto que GCP invoca directamente.

En `encodebiz-api` no existe: se ha comprobado que no hay ni el servicio ni un `firebase.json`
en ninguna rama.

## Decisión

Se crea `services/firebase_sdk` en `encodebiz-api`, copiando el patrón de GroundApp, como
**alojamiento transitorio** de los triggers que aún deben ejecutarse en Firebase. Solo triggers;
ninguna función HTTP.

## Razones

- Los triggers pendientes viven en el repositorio que se queda, no en el que se retira.
- El despliegue a Firebase queda declarado en un único sitio, junto al resto del monorepo.
- El patrón ya está probado en GroundApp, con la misma forma de monorepo.

## Consecuencias

- Se añade un `firebase.json` en la raíz de `encodebiz-api` con `functions.source` apuntando al
  servicio, y su propio `predeploy`.
- Es un residuo con fecha de caducidad: cada trigger se borra en cuanto su escritura pasa por el
  contenedor.
- **El módulo se considera terminado cuando `services/firebase_sdk` está vacío.** Ese es el
  indicador de que `encodeBiz-SAAS` ya no participa en la emisión.

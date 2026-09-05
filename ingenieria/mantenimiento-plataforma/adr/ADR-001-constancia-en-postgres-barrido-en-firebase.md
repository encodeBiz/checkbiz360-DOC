# ADR-001 — El barrido corre en Firebase; la constancia se guarda en Postgres

**Fecha:** 2026-09-04
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Hay que retirar periódicamente las cuentas de Firebase Auth que no pertenecen a nadie, y hay
que poder explicar después qué se borró y por qué.

Las dos mitades del trabajo miran a sitios distintos:

- **Decidir** exige recorrer la lista entera de cuentas de Firebase Auth y cruzarla con
  Firestore (`user_entity_roles`, las subcolecciones `employees`, `entities`,
  `backoffice_users`).
- **Explicar** exige un histórico consultable por fecha, por correo y por desenlace, que se
  pueda mirar meses después sin pelearse con índices compuestos.

Y hay un antecedente que condiciona todo: `cleanupUnverifiedUsers` (encodeBiz-SAAS) borraba
cuentas sin verificar y su único rastro era `console.info`, que caduca a los 30 días. Cuando
se descubrió que había borrado a un cliente real —dos veces—, no se pudo saber a quién más
había tocado ni deshacerlo.

## Decisión

El barrido vive en `services/firebase_sdk` como `onSchedule` de Cloud Functions. La
constancia vive en Postgres, y la escribe el servicio `backoffice` a través de un endpoint
S2S que la función llama por HTTP.

**La pasada se abre en Postgres antes de tocar nada, y cada cuenta se escribe con la copia de
su ficha antes de borrarla.** Si la base de constancia no contesta, no se borra.

## Razones

- **El barrido no cabe en el contenedor**: `listUsers` pagina sobre Firebase Auth, y no hay
  forma de recorrer esa lista desde fuera sin traérsela entera.
- **La constancia no cabe en Firebase**: guardarla en Firestore obligaría a índices
  compuestos para cada pregunta que se quiera hacer, y el resto del histórico consultable de
  la plataforma ya está en Postgres.
- **Postgres no sale de la red de contenedores**, así que el puente HTTP no es una elección:
  es la única forma. Ya existía el patrón —`requireApiKey` y el prefijo `s2s`— por los
  triggers que publican eventos.
- **Escribir primero y borrar después** convierte un fallo a mitad en un dato («esta cuenta
  se quedó a medias») en vez de en un agujero. La copia guardada antes es lo que hace el
  borrado reversible.

## Alternativas descartadas

- **Un cron en el contenedor** que lea Auth por REST. Habría que reimplementar la paginación
  del SDK y mantener credenciales de Auth en un servicio que hoy no las necesita, para
  ahorrarse un salto HTTP que de todas formas hace falta para otra cosa.
- **Constancia en Firestore**, junto a los datos que se borran. Cada pregunta del panel
  («qué pasó con este correo», «qué pasadas fallaron esta semana») sería un índice nuevo, y
  el panel ya lee de Postgres para todo lo demás.
- **Escribir el resumen al final de la pasada**, en una sola llamada. Es más simple y es
  exactamente el fallo anterior: si el proceso muere después de borrar, no queda nada
  escrito.

## Consecuencias

- El `firebase.json` de `encodebiz-api` deja de existir solo por los triggers de eventos.
  **`services/firebase_sdk` ya no se vaciará del todo**: el fin del módulo de eventos sigue
  siendo que no queden triggers de emisión, pero esta función se queda.
  Matiza [ADR-006 de eventos-webhooks](../../eventos-webhooks/adr/ADR-006-firebase-sdk-residuo-transitorio.md).
- Hay una dependencia nueva en tiempo de ejecución: si el backoffice está caído a las 4:15,
  el mantenimiento de esa noche no ocurre. Es el comportamiento buscado.
- En desarrollo, la clave S2S viaja en claro hacia el 8080, que no tiene TLS. Es la clave de
  desarrollo y no abre nada de producción; queda dicho aquí y en el `.env.example`.
- El despliegue del barrido es manual (`--project` explícito) y el del panel automático por
  la rama `staging`. Son dos ritmos distintos para una misma función, y el contrato S2S entre
  ellos hay que tratarlo como un contrato: la fila se abre con un `job` que el servidor valida.

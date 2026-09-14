# ADR-001 — El destino de un disparador es el caso de uso que escribe, no otro alojamiento

**Fecha:** 2026-09-08
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

Quedan 29 funciones reactivas de checkbiz en `encodeBiz-SAAS`: 20 disparadores de Firestore y
9 cron. El objetivo declarado es cerrar ese repositorio y tener una sola historia en
`encodebiz-api`.

La vía rápida para conseguirlo es mudarlas tal cual a `services/firebase_sdk`, que ya existe,
ya tiene su `firebase.json` y ya despliega. En un día estarían todas ahí y el repositorio viejo
podría cerrarse.

El problema es qué queda después. `firebase_sdk` sería entonces un bundle de treinta funciones
que se compila junto, se despliega junto y paga arranque en frío —es decir, el mismo monolito
del que se está saliendo, con otro nombre y en otro repositorio—.

Y la mayoría de esos disparadores ya no tienen razón de ser. Observan escrituras que **hoy hace
el contenedor**: los fichajes se crean en `checkinbiz`, las tareas y sus valoraciones en
`tasks`, los empleados en `shared`. Un disparador que observa una escritura propia es un rodeo:
se escribe, GCP se entera, arranca una función fría, vuelve a leer lo que acabamos de escribir
y deduce qué ha pasado. Todo eso para saber algo que el caso de uso sabía con certeza dos
líneas antes.

## Decisión

Cada función reactiva va al sitio que le corresponde por naturaleza, no al que es más rápido de
preparar:

- **Al caso de uso que hace la escritura**, si el contenedor ya la hace. El disparador
  desaparece; no se muda.
- **A un cron del contenedor**, si es un trabajo programado. El patrón ya está probado en
  `reports`, `events` y `rentman`.
- **A `services/firebase_sdk`**, solo si GCP tiene la obligación de invocarla y no hay otra
  manera. Al terminar, eso es una función: `beforeUserCreated`.

## Razones

- **Lo que se busca no es cerrar un repositorio, es dejar de tener un bundle.** Mudarlo entero
  cierra el repositorio y conserva el bundle, que es el problema.
- **El evento se emite donde se sabe qué ha pasado.** Ya está decidido así en
  [eventos-webhooks/ADR-002](../../eventos-webhooks/adr/ADR-002-emision-en-el-caso-de-uso.md), y
  lo contrario obliga a reconstruir la intención comparando el antes y el después del documento.
- **El arranque en frío se paga en el camino crítico.** El disparador de patrones se ejecuta en
  cada fichaje de cada empleado.
- **El propio `firebase_sdk` lo dice.** Su README limita lo que puede vivir ahí a lo que GCP
  deba invocar, y el [ADR-006 de eventos](../../eventos-webhooks/adr/ADR-006-firebase-sdk-residuo-transitorio.md)
  lo declara residuo transitorio. Llenarlo obligaría a reescribir las dos cosas.

## Consecuencias

- La Fase 5 es más lenta que una mudanza: hay que entender cada disparador antes de disolverlo,
  no solo moverlo de carpeta.
- Depende del HTTP. Un disparador solo puede disolverse cuando su escritura pasa por el
  contenedor, y por eso el CRUD va primero.
- `services/firebase_sdk` termina con dos funciones —el barrido de cuentas fantasma y la
  blocking function—, y ese es su tamaño definitivo.
- El indicador de «terminado» deja de ser «la carpeta está vacía» y pasa a ser «en el codebase
  `default` no queda nada de checkbiz».

## Alternativa descartada

Mudar las 29 a `firebase_sdk` y disolverlas después, ya dentro del monorepo. Cierra antes el
repositorio viejo, pero deja el trabajo real intacto y añade uno nuevo: dos migraciones en vez
de una, y un bundle desplegándose a mano entretanto. Si en algún momento la prioridad pasa a
ser cerrar `encodeBiz-SAAS` cuanto antes por encima de todo lo demás, esta decisión se revisa
—y se anota aquí por qué—.

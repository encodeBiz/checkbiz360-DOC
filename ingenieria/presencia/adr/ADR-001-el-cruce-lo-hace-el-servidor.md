# ADR-001 — El cruce entre lo previsto y lo real lo hace el servidor

**Fecha:** 2026-10-09
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

## Contexto

«Mi equipo» responde quién debería estar hoy en la sucursal y quién no ha fichado. Lo previsto
lo da el calendario, y ya está servido: `GET /calendar/availability/day` devuelve a los
disponibles con sus turnos y a los no disponibles con su motivo. Lo real está en
`entities/{e}/checklogs`. Hay que cruzar las dos listas, y la pregunta es dónde.

La app tiene hoy acceso directo a Firestore y las reglas están abiertas
(`encodebiz-api/firestore.rules`, comodín hasta 2030-01-20). Técnicamente podría pedir el
desglose del día a la API, leer con `snapshots()` los fichajes de la sucursal y cruzarlos en el
móvil, en tiempo real y sin tocar el servidor. Es la opción que menos cuesta esta semana.

## Decisión

**El cruce lo hace el servidor**, en una ruta nueva de sólo lectura que compone el caso de uso
de la disponibilidad con los fichajes del día, usando la lógica de jornada del panel promovida
a `@encodebiz/shared`. La app pide la lista y la pinta. Nunca calcula un estado ni una cifra.

## Razones

**Es la lección de la disponibilidad, y está escrita.** El tablero de cobertura se hizo primero
cruzando en el navegador; funcionó, y hubo que reescribirlo
([disponibilidad/01](../../disponibilidad/01_as-is.md)). Los motivos fueron tres y los tres
aplican aquí letra por letra: coste lineal pagado por cada cliente, dependencia de reglas
abiertas, y fallos que se convierten en números optimistas.

**Una copia de la regla, no tres.** La lógica que convierte fichajes en jornadas —qué es una
pausa abierta, cuándo una jornada está completa, qué cuenta un `failed`— vive hoy sólo en
`attendanceSummary.ts` del panel. Cruzar en la app obligaría a reimplementarla en Dart. El día
que cambie, el panel y el móvil dirían cosas distintas de la misma persona, y nadie se
enteraría hasta que un supervisor y un administrador discutieran por teléfono.

**El permiso tiene que ser del servidor.** Quién puede ver los fichajes de quién es exactamente
lo que `resolveActorScope` ya decide para la disponibilidad: supervisor sus sucursales, worker
nada. Si la app lee fichajes ajenos directamente, ese permiso lo sostienen las reglas de
Firestore abiertas; es decir, no lo sostiene nada. Y cuando se cierren —que es deuda declarada—
la pantalla dejaría de funcionar sin un error que lo explique.

**El fallo tiene que ser honesto.** Un `permission-denied` o un timeout en una lectura hecha en
el cliente se parece demasiado a «nadie ha fichado». En una pantalla cuya única función es decir
quién falta, ese es el peor fallo posible: no avisa, acusa. En el servidor, una lectura fallida
es un `5xx`, y la app enseña un error y una lista vacía.

**`other_branch` no se puede hacer desde la sucursal.** Para decir que alguien sin fichaje aquí
ha fichado en otro centro hay que leer fichajes de otras sucursales. Desde la app sería abrir
aún más la lectura; desde el servidor es una consulta acotada a quien quedó sin fichaje.

## Lo que se pierde, y cómo se compensa

**El tiempo real.** Un `snapshots()` en el móvil pintaría el fichaje de Ana el segundo en que
ocurre; una lectura HTTP, cuando se vuelva a pedir. Se compensa con refresco al abrir, al
volver a primer plano, con pull-to-refresh y periódico mientras la pantalla está visible. Y,
opcionalmente, con un `snapshots()` sobre los fichajes del día de la sucursal usado **sólo como
disparador** de la recarga, igual que «Mi material» recarga al llegar un aviso. Si las reglas se
cierran, el disparador se apaga y el refresco periódico sigue: la pantalla pierde inmediatez,
no verdad.

**Trabajo de servidor.** Una ruta, un caso de uso, la promoción de la lógica de jornada y su
spec. Es la parte que la opción barata se ahorraba, y es exactamente lo que la disponibilidad
tuvo que hacer igual después de haberse ahorrado.

## Alternativas descartadas

**A — La app cruza, con Firestore directo.** Desglose del día por API, fichajes por
`snapshots()`, cruce en Dart. Descartada por todo lo de arriba. Es la copia exacta del
prototipo de disponibilidad que ya se retiró.

**B — Híbrido por fases: A ahora, servidor después.** Sale antes y se migra cuando haya tiempo.
Descartada porque «después» no llega: la pantalla funcionaría, nadie la tocaría, y la deuda se
cobraría el día que se cierren las reglas, de golpe y en producción.

**C — Extender el contrato de `/availability/day` con un parámetro `withPresence`.** No es una
alternativa a esta decisión sino una variante de dónde vive la ruta; se trata en
[ADR-002](./ADR-002-donde-vive-la-presencia.md).

## Consecuencias

- La app gana su primera lectura de la API privada con Firebase ID token fuera de la firma. Hace
  falta un helper común para no repetir la obtención del token en cada datasource.
- `buildWorkSessionSummaries` se mueve a `shared` con pruebas, y el panel la importa de ahí. Es
  trabajo que beneficia al panel aunque «Mi equipo» no existiera.
- La pantalla no es instantánea. Se asume y se documenta en la propia pantalla con la hora de la
  última actualización.

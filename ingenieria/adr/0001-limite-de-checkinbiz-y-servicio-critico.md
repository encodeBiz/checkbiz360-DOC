# ADR-0001 — Dónde acaba `checkinbiz` y cuándo nace el servicio crítico

**Estado:** aceptada · 2026-08-21
**Contexto:** la migración de Firebase Functions a contenedores está haciendo crecer
`services/checkinbiz` (auth, calendario, fichajes, patrones y ahora empleados), y con cada
port se acerca más a un monolito.

---

## La pregunta

¿Hay que trocear `checkinbiz` por dominios —empleados aparte, centros aparte— antes de
seguir portando?

## La decisión

**No por dominios. Sí, más adelante, por criticidad.**

Se sigue portando el núcleo de checkbiz a `checkinbiz`, y en su momento se extrae un
servicio **crítico** que contenga lo que no puede fallar nunca: el camino de fichar.

## Por qué no por dominios

Empleados, centros, responsabilidades, calendario y fichajes **viajan siempre juntos**: un
fichaje se valida contra la geocerca de un centro y contra la responsabilidad de esa
persona en ese centro. Separarlos en servicios convierte cada fichaje en dos o tres saltos
de red para datos que se necesitan a la vez.

Eso no elimina el monolito: lo reparte. Misma rigidez, y además falla por la red. Es el
peor de los dos mundos y tiene nombre — monolito distribuido.

## Cuál es el eje bueno

Lo que ya está separado lo está por **perfil de ejecución y dominio de fallo**, y eso es
correcto: `merlin` (IA, lenta), `reports` (CPU, genera PDF/XLSX), `sync` (ingesta),
`analytics` (consulta pesada) y los **add-ons** (dependen de un tercero con sus caídas y
sus límites de peticiones).

El eje que falta cubrir es la **criticidad**. Todo lo demás puede estar caído una hora sin
drama; que un empleado no pueda fichar, no. Hoy el fichaje comparte contenedor con la
administración, así que un despliegue de "editar empleado" reinicia el fichaje.

## Qué se hace ahora

1. Se sigue portando a `checkinbiz`, **manteniendo la frontera por dominio dentro del
   servicio** (carpetas propias de dominio, aplicación e infraestructura). Así, el día que
   se parta, es mover ficheros y no reescribir.
2. `checkinbiz` es el **núcleo de checkbiz**, no un cajón: si algo tiene otro perfil de
   ejecución o depende de un tercero, va a su propio servicio. Los add-ons, siempre.

## El disparador para partir

Se extrae `checkinbiz-critical` cuando ocurra **cualquiera** de estas tres:

- Un despliegue de administración interrumpa el fichaje en horario laboral.
- El arranque del contenedor crezca hasta que reiniciar sea notable para el usuario.
- Dos equipos empiecen a estorbarse en el mismo servicio.

Hay precedente y camino hecho: el **proxy crítico** de checkinbiz ya aísla ese tráfico, así
que la extracción tiene por dónde empezar.

## Consecuencias

- A corto plazo, `checkinbiz` seguirá creciendo. Es aceptable y está vigilado.
- La deuda es explícita: está escrita, con su criterio y su disparador, en vez de aparecer
  como sorpresa dentro de seis meses.
- Los add-ons no entran nunca aquí: viven en su servicio, con sus tablas, y si se
  descontinúan no dejan rastro.

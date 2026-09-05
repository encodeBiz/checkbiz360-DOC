# ADR-001 — Merlin edita un borrador; sólo el seed escribe

**Fecha:** 2026-09-05
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El asistente tiene que convertir lo que manda el cliente —un Excel de gestoría, un CSV, una
lista pegada en un correo— en una entidad montada: sucursales, plantilla, responsabilidades
y calendario. La forma obvia sería que el asistente fuese creando las cosas conforme las va
entendiendo: crea las sucursales, luego los empleados, luego los horarios.

Esa forma obvia tiene dos problemas serios.

El primero es el reparto del riesgo. Crear doscientos empleados es crear doscientos usuarios
en Firebase Auth y mandar doscientos correos. Si el proceso falla a la mitad —o si a la
mitad se descubre que dos sucursales eran la misma— queda una entidad a medio construir, y
deshacerla no es gratis: `deleteEmployee` es borrado blando, el `searchIndex` hay que
limpiarlo aparte y el usuario de Auth sobrevive.

El segundo es que **el cliente tiene que validar la configuración antes de que exista**, no
después. Si el asistente ya ha escrito, la validación llega tarde.

## Decisión

**Merlin no tiene acceso de escritura a la plataforma.** Lo único que manipula es un
borrador de trabajo, uno por puesta en marcha. Toda la conversación —«esta sucursal está
duplicada, fúndelas», «el horario de Tienda Centro es partido», «estos cuatro son
encargados»— son ediciones de ese borrador.

**El borrador es un fichero temporal, no una colección de la plataforma.** Vive en el
directorio de trabajo del asistente mientras dura la puesta en marcha y se retira cuando el
seed ha terminado. No es un objeto de dominio: no tiene colección, ni reglas, ni
retención, ni migración.

En disco y no en memoria del proceso, porque la sesión se corta y el cliente vuelve al día
siguiente; pero temporal, porque una vez sembrado **la plataforma es el registro** y el
borrador no aporta nada que no esté ya dentro.

Cuando el borrador está validado, un **seed** lo ejecuta contra la plataforma en un solo
paso, simulando por defecto y escribiendo sólo con `--apply`, como cualquier otro script del
repo.

## Consecuencias

**Los datos personales no se quedan en ningún sitio nuevo.** Un borrador real lleva
nombres, DNIs, teléfonos y correos de la plantilla de un cliente. Que sea temporal por
diseño evita crear una segunda copia permanente de todo eso fuera de la plataforma, con su
propia pregunta de conservación. No es una precaución añadida: es consecuencia de dónde
vive.

**El borrador es la fuente de verdad de la conversación, no el hilo.** Cuando se corrige que
«T. Centro» y «Tienda Centro» son lo mismo, esa corrección se escribe en el borrador. Si
vive sólo en el historial del chat, a la tercera sesión se ha perdido.

**El proceso es reanudable.** El cliente se va a ir a comer en medio, y va a volver al día
siguiente. El borrador guarda por dónde iba.

**Lo que valida el cliente no es el borrador.** Enseñarle el JSON no sirve. Lo que necesita
ver es su configuración en lenguaje suyo —cuántas sucursales, quién trabaja dónde, con qué
horario, quién responde de qué— en algo legible e imprimible. Ese documento es además el
entregable comercial: la foto de «así queda montada tu operativa» antes de que nadie fiche.

**El seed hereda las costumbres del repo:** simula por defecto, es determinista, es
idempotente por clave natural, y se construye a la vez que su deshacer.

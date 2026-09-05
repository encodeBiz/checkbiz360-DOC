# 05 · Dónde vive y qué rutas necesita

## Merlin sirve, su pipeline no

Merlin (`services/merlin`, montado en `/api/v1/gpt`) tiene hoy dos rutas, `/panel` y
`/interpret`, y **ninguna de las dos vale para esto**:

- **Son asíncronas con caché.** Devuelven `202` cuando no hay nada cacheado y el front sondea
  hasta que aparece. Está pensado para «nárrame el panel de este mes», que se pide una vez y
  se guarda un día. Una conversación es lo contrario: turnos cortos y síncronos.
- **La salida está fijada a un relato.** `OpenAiRenderer` devuelve siempre
  `{headline, summary, body, actions, confidenceNote}`. Aquí hace falta otra cosa: ediciones
  sobre un borrador y preguntas.
- **No entran ficheros.** El cuerpo de `/panel` son las claves estables que el panel ya
  calculó, a propósito, para que el relato no pueda contradecir a la pantalla.

Lo que sí se reutiliza, y es lo importante:

- **`CustomGptService`** (`packages/shared/src/openai.ts`) es un paso directo al Responses
  API: `ResponsesCreateParams` es el tipo completo, así que herramientas, varios turnos y
  `json_schema` estricto están disponibles. No hay que construir acceso al modelo.
- **La disciplina de salida estructurada**, que es exactamente lo que se necesita para editar
  un borrador sin que el modelo escriba prosa donde va un número.
- **`commonVocabulary.ts` y los prompt builders**, para que el asistente hable como el resto
  de Merlin y no como otro producto.
- **`repairMalformedUnicodeEscapes`**, que arregla un fallo real de `gpt-5-mini` con las
  tildes dentro de JSON. Mordería igual aquí.

**Decisión: un módulo nuevo dentro de Merlin**, con su propia ruta síncrona por turnos, sin
tocar `/panel` ni `/interpret`.

---

## El reparto

**El borrador y la conducción viven en backoffice.** Es donde está la sesión del operador,
sus roles (`backoffice_users`) y el `auditTrail` que ya registra lo que se hace. Y sobre todo:
el borrador lleva nombres, DNIs y teléfonos de la plantilla de un cliente, y es temporal
([ADR-001](./adr/ADR-001-merlin-edita-un-borrador.md)). Debe vivir en un solo sitio, el que
tiene la sesión, y morir ahí.

**Merlin pone el turno de lenguaje, y no guarda nada.** Recibe el borrador y lo que ha dicho
o mandado el cliente; devuelve qué cambiar, qué preguntar y qué contestar. Sin estado y sin
datos personales en reposo.

Backoffice llama a Merlin de servicio a servicio, con el patrón que ya existe para
`/s2s/maintenance` (`requireApiKey`).

---

## Rutas de backoffice

Bajo `/api/v1/backoffice`, con la sesión del operador:

```
POST   /puesta-en-marcha                   abre una sesión → { id }
GET    /puesta-en-marcha/:id               el borrador y el progreso por bloques
GET    /puesta-en-marcha/:id/plantilla/:bloque
                                           el CSV de ese bloque, con su fila de ejemplo
POST   /puesta-en-marcha/:id/mensaje       lo que ha dicho el cliente
POST   /puesta-en-marcha/:id/fichero       un CSV o un XLSX
GET    /puesta-en-marcha/:id/revision      la configuración en el idioma del cliente
POST   /puesta-en-marcha/:id/sembrar       simula por defecto; escribe con { apply: true }
DELETE /puesta-en-marcha/:id               retira el borrador
```

`POST /sembrar` sin `apply` devuelve exactamente lo que haría —cuántas sucursales, cuántas
responsabilidades, cuántos festivos tras expandir, y las coordenadas con su precisión— y no
escribe nada. Es la misma costumbre que los scripts del repo.

Y **rechaza si queda alguna pregunta abierta de las que bloquean**. No es un aviso: es un
error, porque sembrar con un coste por hora vacío deja un cliente roto de una forma que no se
arregla después.

---

## La ruta de Merlin

Una sola, bajo su montaje actual:

```
POST /api/v1/gpt/puesta-en-marcha/turno
```

**Entra:** el borrador tal y como está, el bloque en curso, y lo que llega del cliente —texto,
o una tabla ya parseada; el fichero lo abre backoffice, no Merlin—.

**Sale**, con `json_schema` estricto:

```
ediciones    qué cambia del borrador, por ruta   (`empleados[<correo>].coste_hora`)
preguntas    qué falta, por qué, y si bloquea el seed
respuesta    lo que se le dice al cliente, en su idioma
bloque       si el bloque queda cerrado o sigue abierto
```

Merlin **no devuelve el borrador entero**. Devuelve ediciones por ruta, y las aplica
backoffice. Así un fallo del modelo puede estropear un campo, pero no borrar el trabajo de
una tarde.

---

## Lo que no decide este documento

Si la sesión es de un operador o compartida, y qué pasa si dos personas del equipo abren la
misma puesta en marcha a la vez. No bloquea la primera fase: al principio esto lo usa quien lo
está montando, y una sesión por operador basta.

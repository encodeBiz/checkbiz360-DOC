# ADR-003 — Entrega inmediata; la outbox es la red, no el repartidor

**Fecha:** 2026-08-26
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

El diseño actual escribe la entrega en una outbox y la reparte un cron de un minuto. Eso
implica ~30 s de latencia media aunque no haya carga, y un techo de 100 entregas por minuto
para toda la plataforma.

La justificación original —no meter un POST a un tercero en el camino crítico del fichaje— **no
se sostiene**: el fichaje escribe el checklog y devuelve, y el trigger corre después, en otra
invocación. Aunque la entrega se hiciera dentro del emisor, quien ficha ya se ha ido.

El argumento que sí se sostiene es otro y es más estrecho: **una invocación no puede esperar una
hora**, y el backoff llega a 3600 s. Y si el intento muere a mitad, sin registro durable el
evento se pierde en silencio.

## Decisión

Se **intenta la entrega en el acto**, en el mismo flujo que emite. La outbox se conserva como
registro durable y el worker programado pasa a ser **red de rescate**: recoge lo que falló y lo
que quedó huérfano, no reparte lo normal.

## Razones

- Latencia de milisegundos en el caso normal, que es la inmensa mayoría.
- Se elimina el techo de reparto: deja de haber una cola central por la que pasa todo.
- Se conservan intactas las garantías que sí importaban: durabilidad, reintentos largos y
  posibilidad de reproducir.

## Consecuencias

- **Entregas duplicadas dejan de ser teóricas.** Un reintento del emisor puede producir la
  misma entrega dos veces. Ya está cubierto por `evt_id`, pero pasa a ser obligación
  documentada del consumidor ([04](../04_contrato-publico.md) §6).
- En el contenedor, la emisión no debe esperar a la respuesta del tercero dentro de la petición
  HTTP del usuario: se escribe la outbox en la transacción y el envío se suelta sin bloquear.
- El worker de rescate puede correr mucho menos a menudo, porque ya no es el camino normal.

# Lectura de cuadrantes — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** Merlin — capa de soporte · checkbiz360 — calendario del empleado y tareas
**Fecha de inicio:** 2026-09-20
**Estado:** Diseño abierto · sin implementar
**Autor:** Jose Acevedo

---

## Contexto y Motivación

Una empresa de ayuda a domicilio planifica en su propio programa de gestión y saca cada
semana un cuadrante por trabajadora: los servicios de esa semana, con su hora, el domicilio
y lo que hay que hacer allí. Ese papel ya existe, ya está aprobado y ya se le entrega a la
auxiliar.

Para que esa semana viva en checkbiz360, hoy hay que teclearla. La demo de ayuda a domicilio
—`services/merlin/src/soporte/puesta-en-marcha/demo/sad/`— se montó pasando a mano un
cuadrante real a un CSV de dieciséis filas. Sirve para enseñar el producto; no es el
producto. Una empresa de veinte auxiliares tiene veinte cuadrantes cada lunes.

Y no hay un formato que soportar: cada ERP imprime el suyo, y las etiquetas cambian de uno a
otro. Reconocer el impreso de una marca concreta resuelve un cliente y ninguno más.

## Principio de diseño

> **El modelo lee la forma; el servidor guarda la identidad. Y no se escribe nada hasta que
> las sumas cuadran con el papel.**

La primera mitad hace innecesaria la transferencia de datos personales: el modelo mapea
semánticamente un documento en el que los nombres y los domicilios ya son tokens, porque para
ordenar una semana no hace falta saber quién es nadie. La segunda convierte los totales que
el propio cuadrante imprime en la comprobación de que la lectura está completa.

## Alcance

**Dentro:** una entrada nueva que recibe el cuadrante de UNA persona para UNA semana, lo lee,
y propone el horario de esos días y las tareas de cada servicio; la simulación previa a
cualquier escritura; el bloqueo cuando el cuadrante contradice el calendario; y la escritura
en el calendario del empleado y en `tasks`.

**Fuera:** el cuadrante que trae a la plantilla entera en una matriz —se diseñará cuando haya
un caso real delante—; cualquier optimización de rutas u horarios, que no se promete ni en la
landing; y devolver nada hacia el ERP del cliente: esto lee, no escribe fuera.

## El caso real, medido

El 2026-09-20 se pasó por el proceso un cuadrante real: «Horario del trabajador» que imprime
ServiSAD para una delegación de DomusVi, semana del 21 al 27 de septiembre, una auxiliar.

- 16 servicios en 9 domicilios, de lunes a viernes. Sábado y domingo no aparecen.
- Columnas: `H.Inicio`, `H.Fin`, `Usuario`, `Domicilio`, `Servicio`, `Duración`, `D.Min` y
  una `C` que no se usa.
- Cada día abre con una fila `DESPLAZAMIENTO` sin horas y con 10 o 15 minutos, cierra con
  `Total día` y repite la cabecera. La segunda página sólo trae el `Total semana`.
- Totales impresos: 30 h 30' de servicio más 1 h de desplazamiento, 31 h 30'. Las horas
  contratadas son 30.
- El pie dice que el documento es confidencial y que hay que destruirlo. Los servicios son de
  personas dependientes: alrededor hay datos de salud.

Cuatro cosas salieron de pasarlo, y ninguna era evidente antes:

1. **La sombra por lista blanca no deja nada en claro y no pierde la estructura.** Ni un
   nombre ni un domicilio cruzan; las horas, las duraciones, la forma del día y los totales
   sí. Ver [ADR-001](./adr/ADR-001-la-sombra-por-lista-blanca.md).

2. **Las nueve direcciones geocodifican al portal exacto.** Las nueve dan `rooftop`, y
   preguntándole a Google la misma dirección sin el piso ni la letra —«CALLE ALBUÑUELAS 18 3
   DERECHA» contra «C. Albuñuelas 18»— cae en el mismo punto, a menos de veinte metros. El
   piso y la letra no desvían nada. Entre servicios consecutivos hay de 169 a 499 metros con
   huecos de 5 o 10 minutos: entre 1,8 y 5,2 km/h, o sea que el día se hace andando.

3. **Se deduce qué es cada columna sin leer un solo valor.** Una dirección que sale a las 8:00
   los cinco días es un servicio fijo; un valor que se repite en muchas filas es el tipo de
   servicio, y los casi únicos, emparejados uno a uno con una dirección, son las personas
   atendidas. Por eso la sombra lleva al final el recuento de valores distintos por columna.

4. **Los totales impresos cuadran al minuto con la suma de las dieciséis filas.** 30 h 30' de
   servicio y 60 minutos de viaje. Es la red: si la lectura se deja una fila, no cuadra, y no
   se escribe nada.

5. **El viaje previo se come la tolerancia de entrada.** La franja empieza en la primera tarea
   —8:00— pero la auxiliar sale de casa 10 o 15 minutos antes. `createChecklog` admite la
   entrada desde la hora de la franja menos `notifyBeforeMinutes`, 15 por defecto: el martes,
   con sus 15 minutos, queda justo en el límite, y una entidad con la tolerancia más baja
   dejaría a esa persona sin poder fichar al salir de casa.

## Cómo se lee

### La sombra: lista blanca, no lista negra

Entran PDF, hoja de cálculo y CSV, y el tipo lo decide el contenido del fichero y no su
extensión: lo normal no es el impreso de un ERP, sino una hoja que ha hecho alguien a mano.
Los tres acaban en la misma rejilla de texto.

El documento se extrae en el servidor conservando la disposición. Después, celda a celda,
pasa en claro **sólo lo que es seguro por su forma** —horas, fechas, duraciones, números
cortos, nombres de día y símbolos— y **todo lo demás se tacha**, sea lo que sea, con un token
estable: el mismo valor siempre el mismo token, un contador y no un hash, como en el borde de
la puesta en marcha (ADR-005 de ese dominio).

El tipo del token es sólo una pista barata: `DIRECCION_n` cuando la celda huele a vía
pública, `TELEFONO_n` con nueve dígitos, `TEXTO_n` cuando no se reconoce. Un formato
desconocido falla tachando de más, nunca de menos.

Lo que el modelo recibe de este cuadrante, día por día, es esto:

```
  Lunes   TEXTO_11  TEXTO_12  TEXTO_13  TEXTO_14  TEXTO_15  TEXTO_16  TEXTO_17  TEXTO_18

  TEXTO_19                    0 h 0´    10   TEXTO_20
  8:00   10:00  TEXTO_21  DIRECCION_1  TEXTO_22   2 h 0´    0   TEXTO_20
  10:05  12:05  TEXTO_23  DIRECCION_2  TEXTO_24   2 h 0´    0   TEXTO_20
  12:10  14:40  TEXTO_25  DIRECCION_3  TEXTO_24   2 h 30´   0   TEXTO_20

  TEXTO_26   6 h. 30´   0 h. 10´   6 h. 40´
```

Las cabeceras también van tachadas, y da igual: una columna de `hh:mm` seguida de otra
columna de `hh:mm` es inicio y fin se llame como se llame.

### Las columnas, antes que nada

Lo primero que devuelve el modelo no es la semana: es **qué ha entendido que es cada
columna** —el día, las horas, para quién es el trabajo, la dirección, qué se hace—, con el
nombre que esa columna tiene en el documento. Eso se le enseña a una persona para que lo
confirme o lo corrija antes de mirar nada más. Corregir ahí una columna cambiada cuesta un
clic; descubrirlo después, una lectura entera.

Cuando las columnas vienen corregidas, el modelo no las deduce: las obedece. Medido: dándole
el mapa cambiado a propósito, los títulos salen cambiados.

El mapa que se aprueba se guarda como referencia del cliente —`cuadrante_presets/columnas`—
y se le pasa al modelo la vez siguiente. Se guarda al aprobar y no al leer, porque aprobar es
lo único que significa que alguien lo miró y dijo que sí. Y se le pasa como punto de partida,
nunca como orden: si el cliente cambia de hoja, el modelo tiene dicho que lea lo que ve y lo
diga en los avisos, que es la diferencia entre una referencia útil y un error que se repite
cada semana.

### Las tres fases

Después de las columnas, el modelo lee en este orden, y cada fase se apoya en la anterior. Si
una no sale, dice por qué y no se sigue adelante con una suposición.

1. **La semana.** De qué periodo es el documento y qué días trae, con su fecha. Los días que
   no aparecen no se mencionan: que un día falte no significa que sea libre. Sin periodo, se
   para aquí.
2. **El horario de cada día.** La primera hora de inicio y la última hora de fin de ese día.
   No es la suma de los servicios, ni las horas del contrato, ni lo que diga un total: son los
   dos extremos. El tiempo de viaje previo se informa aparte, sin meterlo dentro ni restarlo.
3. **Las tareas.** Una por servicio, con hora, persona, domicilio, qué se hace y minutos de
   viaje. Lo que no es un servicio —totales, cabeceras, pies, líneas de desplazamiento sin
   horas— se aparta diciendo qué es.

El prompt completo y el esquema de salida, en [01_el-prompt.md](./01_el-prompt.md).

## Lo que se comprueba antes de escribir

Todo esto ocurre en el servidor, sobre los valores de verdad, y nada se escribe si algo
bloquea.

| Comprobación | Si falla |
|---|---|
| La suma de lo leído contra los totales impresos | **Bloquea.** Falta o sobra una fila |
| Un día con servicios que en el calendario es festivo o tiene una ausencia | **Bloquea.** Ver abajo |
| Un domicilio que no geocodifica con precisión suficiente | **Bloquea esa tarea** y se nombra |
| Un día laborable que viene vacío | Se desactiva ese día y se dice. No bloquea |
| `notifyBeforeMinutes` menor que el viaje previo más largo de la semana | Avisa |
| Dos servicios que se solapan, o un viaje imposible entre dos | Avisa |

El primer bloqueo por calendario no es prudencia teórica. `createChecklog` rechaza con
`checklog/absence` cualquier fichaje en un día con ausencia registrada, y lo hace a propósito
desde HAL-29. Aplicar un cuadrante que pisa las vacaciones de alguien pondría las tareas en su
móvil y el fichaje las rechazaría una por una: el error silencioso perfecto, y encima del lado
de la persona.

## Leer no es aplicar

La lectura no toca la plataforma. Arma la semana —el horario de cada día y la lista de
tareas, ya con los nombres y los domicilios de verdad— y la devuelve para que se vea, con
sus hallazgos delante. Eso queda guardado como una **propuesta pendiente**, con su
identificador.

Escribir es un segundo acto, y lo firma una persona: se aprueba por identificador, nunca
mandando de vuelta el contenido. Así el visto bueno recae sobre exactamente lo que se
enseñó —no sobre algo parecido que llegue de vuelta—, no hay que volver a pasar el
documento por el modelo, que podría leerlo distinto, y en la propuesta queda quién firmó y
cuándo.

Lo que bloquea no lo desbloquea una firma: se corrige el cuadrante y se vuelve a subir.

La propuesta vive en Firestore, en `entities/{entityId}/cuadrante_proposals/{id}`. Empezó
en disco, como las sesiones de puesta en marcha, y ahí no aguanta: entre subir el documento
y validarlo pasan minutos, y cualquier despliegue reinicia el contenedor y se lleva el
fichero. Una pantalla que pide una firma no puede perder lo que enseñó.

Cuelga de la entidad y no del empleado para poder listar las pendientes de un cliente sin
consultas de grupo de colección, y por eso la entidad viaja explícita en cada llamada. Lleva
nombres y domicilios de personas atendidas: **se escribe y se lee sólo desde el backend, y
las reglas de Firestore tienen que negar esa colección al navegador**. Caduca a los treinta
días por el campo `expiraEn`, pensado para una política TTL; mientras no esté configurada,
cada propuesta nueva barre lo vencido de ese cliente.

## Qué escribe el servidor

- **El horario**, en `overridesSchedule` del `EmployeeCalendar` de esa persona: un `shifts` por
  día, de la primera tarea a la última, y `disabled` en los días que vienen vacíos. Es la
  cascada que ya respetan el fichaje y el panel.
- **Las tareas**, una por servicio, contra `POST /api/v1/tasks/system`, idempotentes por
  `externalRef`. El `workSite` es el domicilio de la persona atendida con su propio radio: la
  valla que importa no es la de la delegación, donde no trabaja nadie, sino la de cada portal.
- **Los minutos de viaje**, en la descripción de la tarea. No entran en la franja.

Dos cosas van por parámetro de la entrada, no las decide el modelo: que la persona trabaje
fuera de oficina (`enableRemoteWork`) y el radio de la geocerca de cada domicilio, que por
defecto son **150 metros**.

Ese número está elegido por el lado por el que duele equivocarse. Una valla estrecha rechaza
el fichaje de quien ya está en el portal —y deja a la auxiliar parada en la calle, con la
usuaria esperando— por un GPS que rebota entre edificios. Una ancha sólo hace que la valla
distinga peor entre dos portales cercanos, y cuál es cuál ya lo dice la tarea. Medido sobre
el cuadrante real: con 150 metros las vallas de domicilios vecinos se solapan —tres pares
están a menos de 150 metros entre sí, el más cercano a 84—, y se acepta a cambio de que el
fichaje no falle.

Y como cualquier proceso que escribe en esta casa, **simula por defecto**: incluso con la
propuesta ya aprobada, enseña lo que haría y sólo escribe cuando se le pide expresamente.

## Lo que queda por decidir

- **Dónde vive la entrada.** La puesta en marcha es una herramienta interna del equipo; ésta
  se usa cada lunes, así que probablemente sea del cliente. Cambia el tono del asistente y el
  sitio del front.
- **La política TTL de `cuadrante_proposals`**, y la regla de Firestore que niegue esa
  colección al navegador.
- **Resubir la semana corregida.** `externalRef` evita duplicar, pero una tarea que ya no está
  en el cuadrante nuevo no se retira sola.
- **Quién puede firmar.** La aprobación guarda el identificador de quien la hace, pero todavía
  no comprueba que esa persona pueda hacerlo: eso llega con las rutas HTTP.
- **Una semana ya empezada**, con días ya fichados: qué se puede tocar y qué no.
- **El cuadrante de varias personas** en una sola matriz, que es como lo saca más de un ERP.

## Documentos

| | |
|---|---|
| [01_el-prompt.md](./01_el-prompt.md) | Lo que se le pide al modelo, su esquema y su prueba |

**Decisiones:** en [`adr/`](./adr/).

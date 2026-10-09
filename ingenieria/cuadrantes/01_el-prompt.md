# 01 — El prompt, su esquema y su prueba

Lo que se le pide al modelo. Va sin acentos a propósito: `gpt-5-mini`, generando español
dentro de un JSON con `json_schema` estricto, emite de vez en cuando un escape Unicode
malformado, y el mismo problema está documentado en `services/merlin/src/soporte/turno/turno.ts`.

## Las instrucciones

```
Lees el cuadrante semanal de una empresa de ayuda a domicilio y lo conviertes en la
semana de trabajo de UNA persona. Lo haces en tres pasos y en este orden: la semana, el
horario de cada dia, y las tareas. Cada paso se apoya en el anterior: si uno no te sale,
dices por que y no sigues adelante con una suposicion.

CADA EMPRESA IMPRIME EL SUYO A SU MANERA
No hay un formato que reconocer. Puede venir por dias uno debajo de otro, como una
rejilla con los dias en columnas, con una tabla por persona atendida, o como el listado
crudo de un ERP. Las etiquetas cambian: "H.Inicio", "Entrada", "Desde", "Hora". No
busques palabras conocidas ni des por hecha una disposicion: entiende la que tienes
delante. El significado manda sobre la etiqueta.

LO QUE VES YA VIENE TACHADO
Los nombres, los domicilios y los textos libres se han sustituido en el servidor por
PERSONA_1, DIRECCION_2, TEXTO_3. Las horas, las fechas, las duraciones y los totales
estan intactos. Para ordenar una semana no hace falta saber quien es nadie: no adivines
que hay detras de un token, no lo traduzcas, no lo describas. Lo copias tal cual donde
le toca. Un token que no estaba en el documento es un servicio que no existe.
Cuando no sepas que es una columna, miratela por como se comporta: lo que se repite
pocas veces a lo largo de la semana suele ser el tipo de servicio; lo que aparece
siempre emparejado con la misma direccion suele ser la persona atendida; lo que sale
una vez por dia en el mismo sitio suele ser una cabecera o un total.

PASO 1 — LA SEMANA
De que periodo es el documento y que dias trae, con su fecha.
Los dias que aparecen los dices aparezcan llenos o vacios. Los que no aparecen no los
mencionas: que un dia falte no significa que sea libre, y quien decide eso no eres tu.
Si no encuentras el periodo, paras aqui: una semana sin fechas no se puede usar.

PASO 2 — EL HORARIO DE CADA DIA
Para cada dia con servicios, a que hora empieza la jornada y a que hora acaba: la
primera hora de inicio y la ultima hora de fin de ese dia. No es la suma de los
servicios, ni las horas del contrato, ni lo que ponga un total: son los dos extremos.
Un dia que aparece sin servicios no tiene horario, y lo dices vacio.
Si hay tiempo de viaje antes del primer servicio, lo dices aparte, sin meterlo dentro
del horario ni restarlo tu: esa decision no es tuya.

PASO 3 — LAS TAREAS
Una por servicio, en el orden del dia: hora de inicio, hora de fin, a quien se atiende,
en que domicilio, que se hace y cuantos minutos de viaje lleva.
Si hay inicio y duracion pero no fin, calculas el fin y lo marcas como derivado. Si
falta la hora de inicio, no te la inventas: esa fila va a "dudosas" con una frase de por
que. Una hora inventada en una plataforma de fichajes es una jornada falsa.
Lo que no es un servicio va a "ignoradas" diciendo que es: totales, subtotales,
cabeceras repetidas, pies de pagina, avisos de confidencialidad, lineas de viaje sin
horas. Un total colado como servicio crea una tarea fantasma en el movil de alguien.

LOS TOTALES SON TU RED
Si el documento trae totales por dia o de la semana, los copias tal cual, sin
recalcularlos. El servidor suma lo que has leido y lo compara: es la unica forma de
saber si te has dejado una fila.

CUANDO NO LO TIENES CLARO
Va en "avisos", con una frase. No se rellena con lo razonable ni se deja en silencio. Si
el documento no es un cuadrante de servicios, lo dices con confianza "baja" y no fuerzas
una lectura.
```

## La entrada

Dos partes. Primero la sombra del documento, con la disposición conservada y todo lo que no
es seguro por su forma ya tachado. Después, el recuento: por cada columna, cuántos valores
distintos tiene y cuánto se repiten. El recuento no es decoración —es lo que permite
distinguir la columna de la persona atendida de la del tipo de servicio sin leer ninguna de
las dos.

## El esquema de salida

Con `json_schema` estricto, y en el mismo orden de las tres fases:

- `periodo` — `desde`, `hasta`.
- `dias[]` — `fecha`, `diaSemana`, `vacio`, `horario {inicio, fin}`, `viajePrevioMinutos`,
  `totalImpreso`.
- `dias[].servicios[]` — `inicio`, `fin`, `finDerivado`, `personaToken`, `direccionToken`,
  `servicioToken`, `viajeMinutos`.
- `ignoradas[]` — `que`, `porque`.
- `dudosas[]` — `donde`, `porque`.
- `totalSemanaImpreso`, `avisos[]`, `confianza`.

Ningún campo admite texto libre que venga del documento salvo los tokens. Las duraciones y
los totales se copian tal cual están impresos, sin normalizar: normalizarlos es trabajo del
servidor, que sabe en qué formato los quiere.

## La prueba que no se puede saltar

La salida del modelo no puede contener un dato de nadie. Eso es comprobable, así que se
comprueba en el propio código: si en el JSON aparece algo que no sea un token, una hora, una
fecha, una duración o un número, falla la lectura. Lo mismo por el otro lado, antes de
enviar: si la sombra casa con un patrón de teléfono, de DNI o de código postal, no sale.

Y la prueba de regresión del dominio es el cuadrante real: dieciséis servicios, nueve
domicilios, 30 h 30' y 1 h de viaje. Si una versión nueva del prompt deja de cuadrar con esos
totales, no se despliega.

# Qué se le pregunta al cliente, y qué decidimos nosotros

**Decisión tomada el 2026-08-23.** Vale para RentmanBiz y para cualquier integración que
venga detrás.

## La regla

Una integración se conecta a un sistema que no es nuestro, y ese sistema guarda cosas que
sólo el cliente sabe interpretar. Ante cada una de ellas hay dos salidas: preguntar, o
decidir por él. **Se pregunta sólo cuando se cumplen las tres condiciones a la vez:**

1. **La respuesta es cerrada.** Las opciones salen de sus propios datos, no de un campo de
   texto. «Marca cuáles de estas carpetas son plantilla» es cerrada; «¿cómo organizas tu
   personal?» no lo es.
2. **Bloquea.** Sin la respuesta, todas las salidas posibles son incorrectas — no hay un
   valor por defecto defendible.
3. **Toca dinero o toca ley.** Cambia lo que se factura, o cambia lo que dice un documento
   con valor legal.

Si falla una sola, **no se pregunta**: se decide con un valor por defecto prudente, se deja
a la vista y el administrador del cliente lo cambia cuando quiera.

## Por qué así, y no «pregunta lo que no tengas claro»

Porque esa versión blanda se degrada sola en un asistente de quince pasos que la gente pasa
a golpe de «siguiente». Y eso es peor que no preguntar: te devuelve una respuesta falsa con
la que además crees contar.

La regla dura tiene la propiedad de que casi nunca se cumple. Aplicada a todo lo que
teníamos abierto en RentmanBiz, deja **una** pregunta.

## Aplicada a RentmanBiz

**Se pregunta: qué carpetas de personal son plantilla.** Respuesta cerrada —sus carpetas—,
bloquea —sin ella, o metemos autónomos en el registro horario o dejamos fuera a la
plantilla— y toca las dos cosas: el registro horario es de la relación laboral, y se
factura por empleado activo.

**No se pregunta, se decide:** los documentos de proyecto (privacidad, apagado por
defecto), las tareas de almacén (volumen operativo, apagado por defecto), el radio de
geocerca inicial, y si un colaborador cuenta para la factura — eso último es decisión
nuestra de precio, no del cliente.

**Caso aparte, la geocerca de cada centro.** Toca la ley, porque una valla mal puesta
acepta o rechaza fichajes que son el registro. Pero no es pregunta de puesta en marcha:
es por centro y continua. Ya bloquea donde debe — el centro nace inactivo hasta que alguien
confirma dónde está.

## Cómo se implementa una pregunta bloqueante

**Se le enseña lo suyo, no un formulario.** «Personal en plantilla, 4 personas · Autónomos,
7 · Freelancers, 6 · sin carpeta, 6» y marca. Eso es reconocer, no rellenar.

**Se guarda con autor y fecha.** Tiene consecuencia legal: la respuesta a «por qué esta
persona no está en el registro horario» debe ser «el administrador tal lo declaró el día
tal», no «lo dedujo el sistema».

**Lo que llegue después no bloquea, avisa.** Una carpeta nueva aparecida meses más tarde no
puede parar una importación entera. Su gente entra por el lado que NO ensucia el documento
legal —como colaborador, fuera del registro— y salta un pendiente para clasificarla.

## De dónde sale esta regla

De haber hecho lo contrario cinco veces en dos días, y de que las cinco fallaran contra los
datos reales del cliente: dar por hecho que un proyecto sin gente era un alquiler (mal en
16 de 45), fiarse del país que declara Rentman (un teatro de Helsinki marcado como España),
suponer que `classified` bastaba para filtrar documentos (ninguno de los 22 lo llevaba,
presupuestos firmados incluidos), y esperar identificadores estables en los tipos de
proyecto y en las carpetas, que son texto libre por cuenta.

Todas eran cosas que el cliente sabe y nosotros no.

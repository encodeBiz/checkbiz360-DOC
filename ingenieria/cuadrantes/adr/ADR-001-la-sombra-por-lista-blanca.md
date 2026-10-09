# ADR-001 — La sombra de un cuadrante se hace por lista blanca

**Fecha:** 2026-09-20
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

ADR-005 de la puesta en marcha dejó cerrado que los datos personales no salen del servidor:
el modelo mira los valores, pero nunca sabe de quién son. Allí era relativamente fácil, porque
lo que llega es un CSV con columnas conocidas: se sabe cuál es el nombre y cuál el DNI antes
de tachar nada.

Un cuadrante no da esa ventaja. Es el impreso que saca el ERP del cliente, cada marca lo hace
distinto, y **lo que hay que averiguar es justamente qué es cada cosa**. No se puede tachar
por columna porque no se sabe qué columna es cuál hasta que alguien lo lee, y quien lo lee es
el modelo. El huevo y la gallina.

Y el contenido es de lo más delicado que se toca aquí: nombres y domicilios particulares de
personas dependientes, con el servicio que reciben al lado. Alrededor de eso hay datos de
salud, y el propio documento lleva impreso que es confidencial y que hay que destruirlo.

## Decisión

Se invierte la lógica. En vez de detectar lo sensible para tacharlo, **se deja pasar sólo lo
que es seguro por su forma** —horas, fechas, duraciones, números cortos, nombres de día,
símbolos— y todo lo demás se sustituye por un token, sea lo que sea, incluidas las cabeceras
del impreso.

El tipo del token es una pista barata, no una garantía: `DIRECCION_n` cuando la celda contiene
una vía pública, `TELEFONO_n` con nueve dígitos, `TEXTO_n` cuando no se reconoce nada. Los
tokens son estables y se numeran con un contador, no con un hash, por lo mismo que en ADR-005:
un hash de un dato enumerable se invierte por diccionario y sigue siendo dato personal.

Para compensar lo que el modelo pierde al no ver ni las cabeceras, la sombra lleva al final el
recuento de valores distintos y repeticiones por columna.

## Consecuencias

**A favor.** Un formato nunca visto falla tachando de más, que es el lado correcto. No hay que
mantener detectores por ERP ni acertar con el idioma de las etiquetas. Y la propiedad que
importa es demostrable: se puede enseñar la sombra exacta que cruzó y el inventario de cuántos
tokens de cada tipo se emitieron, sin enseñar un solo valor.

**En contra.** El modelo trabaja con menos señal: tiene que deducir qué es cada columna por
cómo se comporta en vez de leer su título. Sobre el cuadrante real de ServiSAD se comprobó que
llega de sobra —la columna del tipo de servicio se distingue de la de las personas atendidas
sólo por cuánto se repite cada valor—, pero es la parte del diseño que más conviene volver a
medir con el segundo formato que aparezca.

**Lo que no cambia.** El modelo sigue sin escribir nada: devuelve la lectura en tokens y el
servidor la convierte en calendario y tareas con los valores de verdad, que nunca salieron de
aquí. La geocodificación de los domicilios también ocurre después, en el servidor, con la
dirección real.

## Alternativas descartadas

**Detectar lo personal (lista negra).** Es lo natural, y es lo que falla en silencio: el día
que un ERP imprima el nombre en un formato que el detector no conoce, ese nombre cruza y nadie
se entera.

**Un NER local en el contenedor.** Resuelve mejor los nombres, pero añade una dependencia y un
modelo que mantener, y sigue siendo probabilístico: acierta el 95% y el 5% restante es una
persona identificada. La lista blanca no tiene ese 5%.

**Mandar el documento entero.** Descartado sin discusión: es una transferencia de datos de
salud a un proveedor fuera de la UE, y no hace falta para lo que el modelo tiene que hacer.

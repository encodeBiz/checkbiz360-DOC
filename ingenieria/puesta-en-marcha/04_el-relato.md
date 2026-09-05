# 04 · El relato — cómo se conduce la puesta en marcha

Este es el documento que importa. El seed es mecánico y el borrador es un fichero; lo que
decide si esto funciona es **cómo se pide**.

## La forma: un CSV pequeño por bloque, no un libro de nueve hojas

Un libro con nueve pestañas paraliza. El cliente lo abre, ve ocho cosas que no entiende y lo
deja para el lunes. El asistente hace lo contrario: **pide un bloque, entrega el CSV de ese
bloque, lo cierra, y sólo entonces pasa al siguiente.**

Cada CSV va con **una fila de ejemplo** y con las columnas justas. Nada de columnas
opcionales «por si acaso»: si un dato no lo va a usar el seed, no se pide.

---

## El arranque

> **Hola. Voy a montar tu empresa en checkbiz360, y lo vamos a hacer por partes para que no
> se te haga bola. Son seis: tu empresa, tus centros de trabajo, tu gente, sus horarios y los
> festivos. Nada más.**
>
> **Puedes contestarme aquí mismo, o rellenar la plantilla que te paso en cada paso, lo que
> te resulte más cómodo. Si tienes ya un listado en Excel de la gestoría, mándamelo tal cual
> y lo miro yo.**
>
> **Puedes parar cuando quieras: guardo por dónde vamos y seguimos otro día.**

Tres cosas y ninguna de adorno: **cuánto va a durar** (seis pasos, enumerados), **que hay
salida fácil** (contesta hablando, o manda lo que ya tienes) y **que se puede interrumpir**.
Las tres son las que hacen que alguien empiece.

---

## Los seis bloques

### 1 · Tu empresa

El único que normalmente no necesita fichero: son ocho datos y se contestan hablando. Nombre
comercial, razón social, NIF, dirección fiscal, correo de facturación e idioma.

Si el cliente prefiere el CSV, se le pasa igual.

### 2 · Tus centros de trabajo

Antes de pedir nada hay que resolver una decisión de modelado, y **no se resuelve
preguntando de quién es el sitio**. Hay dos formas válidas de montar a alguien que trabaja
fuera:

**Un centro por sitio.** Cada fichaje queda atribuido a su centro —`CheckLog.branchId`—, así
que se sabe cuántas horas se han hecho en cada uno, con su coste, y cada uno tiene su propia
valla y su propio patrón de comportamiento. A cambio hay que conseguir la dirección de cada
sitio.

**Un solo centro, y la gente marcada como que trabaja fuera.** Más simple y no hay
direcciones que perseguir. Pero todas las horas caen en el mismo centro —se pierde el reparto
por sitio— y `enableRemoteWork` **quita el control de ubicación a esa persona en todas
partes**, incluida la sede propia.

La pregunta que decide es ésta:

> **¿Necesitas saber cuántas horas se han hecho en cada sitio, o te vale con el total?**

Si la respuesta es lo primero —y en cuanto esas horas se facturan a un tercero, lo es—,
entonces cada sitio es un centro, aunque no sea suyo. Es el caso de
[Tapissat](./02_caso-real-tapissat.md), que trabaja dentro de las fábricas de sus clientes.

Y si el problema es que en un sitio ajeno no se puede garantizar la ubicación, **la palanca
es el centro, no la persona**: `disableRatioChecklog` en ese centro concreto conserva la
atribución y la valla de los demás. Marcar a la persona apaga las dos cosas en todas partes.

`nombre_centro, direccion_completa, radio_metros`

Y una advertencia al entregarlo: **la dirección tiene que llevar número**, porque de ahí sale
el punto desde el que se mide el radio de fichaje.

### 3 · Tu gente

Aquí van juntos el empleado **y su responsabilidad**, en la misma fila. No se separan.

`nombre, email, dni, telefono, puesto, centros, rol, coste_hora`

Que vayan juntos no es comodidad: es lo que impide el error de leer una tabla sin la otra.
`centros` dice dónde trabaja **y** dónde tiene el rol; el seed crea una responsabilidad por
centro ([ADR-004](./adr/ADR-004-el-borrador-guarda-intencion.md)). En Tapissat, esa
separación en dos hojas fue exactamente lo que hizo que las cuatro personas quedaran sin
poder fichar.

Dos cosas que el asistente dice al entregar este CSV, porque no se pueden deducir después:

- **`coste_hora` no es opcional**, aunque lo parezca. Sin él, todo el análisis económico que
  ha comprado sale en cero, y el precio se congela dentro de cada fichaje: ponerlo el mes que
  viene no arregla el mes pasado.
- **`rol`**: quién manda. Tiene que haber exactamente un `owner`, que es quien entrará al
  panel.

### 4 · Los horarios

El bloque donde más hay que explicar. Primero **una pregunta, no un fichero**:

> **¿Todos trabajáis el mismo horario, o cambia según el centro o según la persona?**

Y según conteste, se abre uno de tres caminos —empresa, centro o persona—, que son los tres
niveles que el calendario ya hereda. El cliente no tiene por qué saber que existen; sí tiene
que elegir.

`dia, turno, hora_inicio, hora_fin`

Con dos avisos: **un día que no aparezca es un día cerrado**, y **si hay jornada partida se
repite el día con turno 1 y turno 2**.

### 5 · Festivos y cierres

> **Necesito dos cosas: los festivos que os toquen por convenio y comunidad, y los días que
> cerráis vosotros —Navidad, agosto, el puente que sea—.**

`nombre, desde, hasta, retribuido`

Los periodos se piden **como periodos**. El cliente escribe «Navidad, del 23/12 al 6/1» una
vez; expandir eso a quince días es cosa del seed.

### 6 · Revisión

No se pide nada. Se **devuelve**: la configuración entera en el idioma del cliente —cuántos
centros, quién trabaja dónde, con qué horario, quién responde de qué—, para que la lea y diga
que sí. Ese documento es lo que se aprueba, y es también el entregable comercial.

---

## La puerta de cada bloque

Un bloque no se cierra porque haya llegado el fichero. Se cierra cuando el asistente ha
**releído el borrador entero** y cuadra.

Entero, no sólo lo que acaba de entrar: cada bloque nuevo puede romper uno anterior, y el
sitio donde eso se descubre casi siempre es el siguiente paso. El caso de manual es el CSV de
la gente nombrando un centro que no estaba en el CSV de centros —porque el cliente se olvidó
de uno, no porque se haya equivocado ahora—:

> **Me dices que dos personas fichan en «Almacén», pero ese centro no me lo habías nombrado.
> ¿Lo añadimos? Necesitaría su dirección.**

Eso es corregir al cliente: decirle qué no cuadra, en su idioma, y con qué se arregla.

### Qué se comprueba en cada paso

**Tras la empresa.** Que el NIF tenga forma de NIF, que la zona horaria exista, y que del
nombre comercial salga un `slug` utilizable.

**Tras los centros.** Que no haya dos con el mismo nombre —es la clave natural con la que se
relacionan todos los demás bloques y con la que el seed evita duplicar—, que cada dirección
lleve número, y que el radio sea razonable.

**Tras la gente.** El paso con más aristas, y el que más veces obliga a volver atrás:

- Que ningún correo se repita: es la credencial de acceso.
- Que ningún DNI se repita.
- **Que todo centro nombrado aquí exista en el bloque anterior.** Aquí aparecen los centros
  olvidados.
- Que haya **exactamente un `owner`**. Ninguno, y nadie puede entrar al panel; dos, y hay que
  preguntar cuál.
- Que nadie se quede sin centro: una persona sin centro no puede fichar en ninguna parte.
- Que ningún `coste_hora` coincida con el de la fila de ejemplo, y que ninguno esté vacío.

**Tras los horarios.** Que los turnos de un mismo día no se solapen y que la hora de fin sea
posterior a la de inicio. Que quede algún día abierto —si el cliente sólo nombró tres días,
conviene confirmar que los otros dos son cierre y no un olvido—. Y que cualquier excepción
apunte a un centro o a una persona que existan.

**Tras los festivos.** Que las fechas se entiendan y que `hasta` no sea anterior a `desde`.
Que un festivo de ámbito centro nombre un centro real. Y avisar de los periodos largos antes
de que sorprendan: *«agosto son 21 días seguidos cerrados, ¿correcto?»*.

**Antes de sembrar.** Que no quede ninguna pregunta abierta de las que bloquean, y que los
seis bloques estén cerrados.

### Cómo se corrige

Nunca devolviendo un error de validación. El asistente dice **qué falta y qué hace falta para
arreglarlo**, y si puede, propone:

> **Me falta el coste por hora de los cuatro. Si me dices el salario bruto anual de cada uno y
> las horas de convenio, lo calculo yo y lo revisas.**

Y lo que no bloquea, no para la conversación: se anota y se pregunta al final, todo junto.

---

## Guardar el estado

Al cerrar cada bloque, el borrador se escribe en disco. Lleva además por dónde va:

```
progreso:
  empresa      → cerrado
  centros      → cerrado
  gente        → abierto · faltan 4 costes por hora
  horarios     → sin empezar
  festivos     → sin empezar
  revision     → sin empezar
```

Así el asistente puede retomar diciendo **qué falta**, no *«¿por dónde íbamos?»*:

> **Nos quedamos en tu gente. Tengo a los cuatro con sus centros y sus roles; me falta saber
> cuánto cuesta la hora de cada uno. ¿Seguimos por ahí?**

---

## Sobre entregar ejemplos

Cada CSV lleva una fila de muestra para que se vea el formato. **Y eso tiene un coste
conocido:** el cliente de Tapissat devolvió la plantilla con los costes del ejemplo intactos
—3200, 2600 y 1800—, en el mismo orden en que venían. No los rellenó: los dejó.

Por eso la fila de ejemplo va marcada como tal, y el asistente **compara cada valor recibido
contra el del ejemplo**. Si coincide, no lo importa: pregunta. Es barato de comprobar y es la
diferencia entre montar un cliente y montarle unas nóminas inventadas.

---

## Cuando termina

El seed se ejecuta, se comprueba que lo sembrado está donde tiene que estar, y **el borrador
se borra**. A partir de ahí el registro es la plataforma
([ADR-001](./adr/ADR-001-merlin-edita-un-borrador.md)).

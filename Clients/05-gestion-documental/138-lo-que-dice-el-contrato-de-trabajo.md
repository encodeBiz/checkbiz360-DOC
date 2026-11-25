# Lo que dice el contrato de trabajo: oficio, jornada y precio por hora

Al subir el contrato de trabajo de una persona, CheckBiz360 lo lee y le propone lo que necesita para que esa persona cuente bien en los costes: su **oficio**, su **jornada**, su **convenio** y su **precio por hora**. Cada dato va con la frase del contrato de la que sale, y nada cambia en la ficha hasta que usted lo aplica.

Esto se hace en la ficha del documento, bloque **Lo que dice el contrato**. Solo lo ven y lo usan el **propietario y los administradores**.

---

## Qué resuelve

- **No teclear el contrato.** Oficio, categoría, jornada, modalidad, fechas y salario salen leídos, con su cita.
- **Un precio por hora con fundamento.** Si el contrato da el salario, se convierte a precio por hora con la jornada anual que marca el convenio; si el contrato dice «según tablas», el salario sale de la tabla del convenio. Ese precio es el que usan los informes de costes y la rentabilidad de los clientes.
- **Ver lo que no cuadra.** Un salario por debajo del mínimo a esa jornada, un convenio que no se identifica o unas tablas de un año anterior salen como aviso, para que lo revise antes de aplicar.

---

## Antes de empezar

- El documento tiene que ser de tipo **Contrato**, estar asignado a **una persona** (ámbito *Empleado*) y ser un **PDF con texto**. Un PDF escaneado como imagen no se puede leer: el bloque lo dice y hay que rellenar la ficha a mano.
- Para que proponga el convenio, su empresa tiene que haberlo referenciado antes: los convenios son de cada empresa. Ver [Convenios colectivos](139-convenios-colectivos.md).
- Si el oficio de la persona ya está en su **catálogo de puestos**, la lectura lo casa con él. Si no está, al aplicar puede **crear el puesto** con el nombre que dice el contrato.

---

## Subir el contrato

1. En **Gestión Documental**, suba el PDF con tipo **Contrato** y ámbito **Empleado**, como cualquier contrato (ver [Nóminas y contratos](32-nominas-y-contratos.md)).
2. Si sabe por qué convenio va la persona, elíjalo en **Convenio colectivo (opcional)**. Si lo deja en *Sin indicar*, se busca en el catálogo al leer el contrato.
3. Publique. La lectura empieza sola. Puede quedarse en la ficha o seguir trabajando: cuando termine, lo verá en **Inicio** y le llegará un correo.

En la ficha del documento, el bloque **Lo que dice el contrato** pasa de *Estamos leyendo el contrato* a los datos leídos. Si quiere repetir la lectura (por ejemplo, tras referenciar un convenio nuevo), pulse **Volver a leer**.

---

## Lo que propone

Cada dato lleva **De dónde sale**, que despliega la frase del contrato: *Del contrato: «…»*. Lo que el contrato no dice aparece como *No está en el contrato*.

| Dato | Qué es |
|---|---|
| **Oficio** | El nombre corto del puesto («auxiliar de ayuda a domicilio», «camarero») y, si el contrato lo trae, el código de ocupación. |
| **Convenio** | El convenio que cita el contrato y su ámbito (estatal, autonómico, provincial o de empresa). |
| **Categoría** | El grupo y el nivel profesional, tal como los escribe el contrato. |
| **Jornada semanal** | Las horas a la semana. |
| **Modalidad** | Indefinido, temporal, formativo o fijo discontinuo. |
| **Fechas** | Desde cuándo y, si la tiene, hasta cuándo. |
| **Salario** | El salario base bruto con su periodo, las pagas y si las extras van prorrateadas o aparte. |
| **Precio por hora propuesto** | Euros brutos por hora, **sin la Seguridad Social a cargo de la empresa**, y debajo **Cálculo**: de qué cifra y qué jornada sale. Lleva la marca **Estimado** cuando el salario viene de las tablas o cuando no hay convenio y se usa la jornada máxima legal. |

Debajo, los **avisos**: solo lo que le cambia una decisión. Por ejemplo, que el salario del contrato queda por debajo del mínimo a esa jornada, que un plus no entra en el salario base, que las tablas guardadas del convenio son de un año anterior o que la fecha de fin se ha calculado a partir de una duración.

> **El precio por hora es un coste bruto.** No lleva Seguridad Social de la empresa ni otros costes. Si en su empresa cuentan los costes de otra manera, corríjalo al aplicar.

---

## El bloque Convenio

El convenio decide la **jornada anual** con la que se pasa de salario a precio por hora y, si el contrato remite a las tablas, el **salario**. El bloque **Convenio** dice qué se ha usado:

- **Este contrato va por «…» · tablas de 2025**, con **Ver documento** para abrir el boletín del que salen las tablas.
- **Fila usada**: la categoría de la tabla, su importe y sus pagas («Auxiliar de ayuda a domicilio: 1.145,81 € × 14 pagas»). Si el convenio tiene varias tablas (una por ámbito, por zona o por tipo de establecimiento), la fila lleva su bloque entre paréntesis: «Auxiliar Administrativo (Residencias)».
- **Sin fila de la tabla**: el salario es el que dice el contrato y del convenio se toma solo la jornada.

Lo que puede hacer:

| Botón | Para qué |
|---|---|
| **Cambiar convenio** | Elegir otro de la lista de su empresa. Los que no tienen tablas todavía no se pueden elegir. |
| **Cambiar fila** / **Elegir fila** | Elegir la categoría de la tabla si la propuesta no es la de esta persona, o si la lectura no supo cuál era. El diálogo enseña cada fila con su grupo, su nivel, los puestos que el convenio adscribe a ese grupo, su bloque y, si la tiene, la jornada completa de ese bloque. |
| **Escribir el precio a mano** | Dejar el convenio fuera y teclear el precio por hora usted. |
| **Volver al convenio propuesto** | Deshacer los cambios. |

Si cambia el convenio o la fila, el precio por hora propuesto deja de valer: **se recalcula al aplicar**, con la tabla elegida, y el bloque lo avisa.

Cuando su empresa no tiene convenio para este contrato, el bloque lo dice (*No hay convenio para este contrato en el catálogo*) y le ofrece **Elegir convenio** o **Referenciar otro convenio**, que abre el formulario de referenciar sin salir de la ficha. Si hay varios posibles, le pide que elija el que aplica. Mientras no haya convenio, el precio se calcula con la jornada máxima legal y queda marcado como estimado.

---

## Aplicar a la ficha

El bloque **Aplicar a la ficha del empleado** pasa lo leído a la ficha de la persona:

1. **Puesto del catálogo.** Si el oficio casa con un puesto de su catálogo, viene propuesto. Si no, viene propuesto **Crear el puesto «…»** con el nombre que dice el contrato; también puede elegir otro del catálogo o dejar **Mantener el puesto que ya tiene**. El puesto nuevo nace solo con el nombre: su precio es el de la persona, no el del puesto, y si ya había uno igual salvo mayúsculas o tildes se usa ese.
2. **Precio por hora (€).** Viene propuesto; puede corregirlo. Si va por convenio, aparece *según convenio*: lo calcula el servidor al aplicar.
3. **Sucursales donde se aplica.** Si la persona está en varias, marque en cuáles. Cada fila enseña *lo que tiene ahora → lo que va a tener*.
4. Pulse **Aplicar a la ficha** y confirme. La ventana enseña **Antes** y **Después**. El catálogo de puestos solo cambia si se crea el puesto del contrato; los que ya existen no se tocan.

A partir de ahí, esa persona cuenta en los costes con su nuevo puesto y su precio por hora en esas sucursales.

---

## Problemas frecuentes

**El bloque dice que el PDF no tiene texto.** Está escaneado como imagen. Pida el contrato en PDF con texto o rellene el puesto y el precio a mano en la ficha de la persona.

**Dice que no parece un contrato de trabajo.** Compruebe que subió el documento correcto. Un anexo, una nómina o un contrato con un cliente no se leen aquí.

**Dice que el contrato parece de otra persona.** El nombre del contrato no es el de la persona a la que subió el documento. Revíselo antes de aplicar nada.

**El precio por hora sale «Estimado» y no me cuadra.** Mire **Cálculo**: dice qué salario y qué jornada se han usado. Si el convenio no es el correcto, cámbielo; si la categoría no es la suya, cambie la fila; si prefiere su cifra, **Escribir el precio a mano**.

**No hay convenio para este contrato.** Su empresa no ha referenciado el convenio que cita el contrato. Pulse **Referenciar otro convenio** y dele el enlace al boletín o su PDF, sin salir de la ficha. Ver [Convenios colectivos](139-convenios-colectivos.md).

**Las tablas son de un año anterior.** El convenio tiene tablas hasta 2025 y el contrato empieza en 2026. Se usa la más reciente que hay y se avisa. Cuando el boletín publique las nuevas, referencie el convenio otra vez con ese documento: se añaden los años nuevos.

---

## Artículos relacionados

- [Convenios colectivos](139-convenios-colectivos.md)
- [Nóminas y contratos](32-nominas-y-contratos.md)
- [Quién ve cada documento](136-quien-ve-cada-documento.md)
- [Crear y gestionar empleados](../02-empleados/06-crear-y-gestionar-empleados.md)
- [Análisis de costes](../07-inteligencia-operativa/54-analisis-de-costes.md)

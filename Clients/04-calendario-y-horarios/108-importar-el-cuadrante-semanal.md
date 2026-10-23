# Importar el cuadrante semanal

Cuando el trabajo cambia cada semana —ayuda a domicilio, limpieza por centros, mantenimiento—, teclear la semana de cada persona, turno a turno o trabajo a trabajo, es una mañana perdida cada lunes. Esta guía explica cómo cargar de una vez la semana de toda la plantilla de una sucursal con una hoja de Excel, o la de una sola persona desde su ficha.

---

## Qué resuelve

- **Una subida para toda la plantilla.** Un fichero por sucursal y semana, con una pestaña por persona. No hace falta ir ficha por ficha.
- **Cada persona recibe su semana en el móvil**: sus turnos, o sus trabajos con la dirección donde tiene que fichar, según cómo se organice su horario.
- **Nada se guarda sin que lo vea antes.** La plataforma enseña lo que hará con cada persona y solo lo aplica cuando usted lo confirma.
- **Corregir es volver a subir.** Si la semana cambia, se sube el fichero corregido: lo que ya estaba se sustituye y no se duplica nada.

---

## Lo que se sube depende del modo de cada persona

El tipo de cuadrante no se elige: lo decide el [modo del horario](114-calendario-de-turnos-por-fecha.md#los-tres-modos-del-horario) de cada persona.

| Modo de la persona | Qué carga su pestaña | Qué pasa con sus tareas |
|---|---|---|
| **Por turnos** | Sus turnos de esa semana: fecha, entrada y salida. Los días sin filas libran. | Ninguna se crea, se mueve ni se borra. |
| **Por tareas** | Una tarea por fila, con su dirección. Sus tareas son su horario. | Sustituyen su semana: las tareas del cuadrante anterior que aún no ha empezado se quitan y se crean las del fichero. Las empezadas se quedan. |
| **Semana tipo** | Nada. Su horario es la semana tipo y no se le sube cuadrante. | No se tocan. |

Si quiere subirle a alguien otro tipo de cuadrante, cámbiele antes el modo.

---

## Cómo funciona, en tres pasos

| Paso | Qué pasa |
|---|---|
| **1. Descargar la plantilla** | Desde la sucursal, para la semana que elija. Trae una pestaña por cada persona de la sucursal, del tipo que le toca. |
| **2. Rellenarla y subirla** | Una fila por turno o por trabajo. Al subirla no se guarda nada todavía. |
| **3. Revisar y confirmar** | La plataforma enseña qué hará con cada persona. Solo al confirmar se aplica. |

---

## 1. Descargar la plantilla

El cuadrante de toda la plantilla se sube desde una sucursal que está **Por turnos**:

1. Vaya a **Sucursales**, abra la ficha de la sucursal y pulse **Editar**.
2. En **Horarios y festivos**, compruebe que **Cómo se organiza el horario** está en **Por turnos**.
3. En **Importar cuadrante por turnos**, encima del cuadrante de turnos, pulse **Subir un cuadrante**.
4. Elija la semana y pulse **Descargar plantilla**.

Quien en esa sucursal esté **Por tareas** también lleva su pestaña, de tareas. Si la sucursal está en **Semana tipo**, el cuadrante de quien esté **Por tareas** se sube desde su ficha (ver [La semana de una sola persona](#la-semana-de-una-sola-persona)).

La plantilla trae una primera hoja con las instrucciones y la lista de la gente, y **una pestaña por persona**, con su nombre y el tipo que le toca: **Cuadrante por turnos** o **Cuadrante por tareas**.

> **No borre la fila 1 de cada pestaña**: es la que dice de quién es y de qué tipo. Puede cambiar el nombre de la pestaña o reordenarlas sin problema.

Cada pestaña trae **dos filas de ejemplo** que empiezan por la palabra **ELIMINAR**: puede borrarlas o dejarlas, porque no se importan.

### Columnas

En un **cuadrante por turnos**, cada fila es un turno y solo hacen falta las tres primeras columnas. Un día partido son dos filas con la misma fecha.

En un **cuadrante por tareas**, cada fila es un trabajo:

| Columna | Qué poner |
|---|---|
| **Fecha** * | El día del trabajo: 19/10/2026. |
| **Hora inicio** * | A qué hora empieza: 08:00. |
| **Hora fin** * | A qué hora acaba: 10:00. |
| **Cliente** | Para quién es el trabajo: la persona atendida, la comunidad, la empresa. |
| **Dirección** | Dónde se hace. Es el lugar donde la persona tendrá que fichar. |
| **Trabajo** | Qué se hace: limpieza, acompañamiento, revisión. |
| **Viaje (min)** | Minutos de desplazamiento hasta ese trabajo. |

Las columnas con asterisco son obligatorias. En un cuadrante por tareas, la **dirección** conviene ponerla siempre: sin ella el trabajo se crea igual, pero se podrá fichar desde cualquier sitio.

### Qué significa dejar una pestaña vacía

- **Una pestaña vacía** deja a esa persona como está. No es «esa semana no trabaja»: es que no se dice nada de ella.
- **Una pestaña con filas** es la semana entera de esa persona: los días sin ninguna fila quedan libres.

---

## 2. Subir el fichero

Pulse **Elegir fichero**, seleccione la plantilla rellena y pulse **Ver la propuesta**. Vale el Excel (.xlsx) de hasta 2 MB, guardado con Excel o con cualquier otro programa de hojas de cálculo. No vale en CSV, porque un CSV no tiene pestañas.

Si sube un fichero que no es la plantilla, la plataforma lo dice y no lee nada.

---

## 3. Revisar lo que se hará

Antes de confirmar, cada persona aparece con su estado, sus filas y las horas de la semana. La revisión de cada persona va según su modo: en un cuadrante por turnos no se habla de tareas ni de direcciones.

| Estado | Significa |
|---|---|
| **Lista** | Todo se ha leído bien. Se aplicará al confirmar. |
| **Bloqueada** | Algo impide aplicarla: una fila mal escrita (se indica cuál), trabajos en un día que para esa persona es festivo o de vacaciones, una persona en **Semana tipo**, o una pestaña de un tipo que ya no casa con su modo. Esa persona no se aplica; las demás, sí. |
| **Sin cambios** | Su pestaña está vacía. No se toca. |
| **Pestaña no reconocida** | La pestaña no corresponde a nadie de la sucursal. Compruebe la fila 1. |
| **Pestaña repetida** | Hay dos pestañas para la misma persona y no se sabe cuál vale. |

Al lado de cada persona salen también los avisos que conviene mirar. En un cuadrante por tareas: dos trabajos que se solapan, trabajos sin dirección, o un desplazamiento antes del primer trabajo más largo que el margen que tiene la persona para fichar la entrada; y qué tareas de esa semana se sustituyen y cuáles se quedan por estar empezadas. En un cuadrante por turnos: si la pestaña trae cliente, dirección o trabajo, se avisa de que esos datos no se cargan. Dos filas del mismo día que se cruzan se cargan como un solo turno.

Lo que pide atención sale primero. Si quiere arreglar a una persona bloqueada, corrija el fichero y pulse **Subir otro fichero**. Si cierra la ventana sin confirmar, no se guarda nada.

Cuando esté conforme, pulse **Confirmar**. Con mucha gente tarda un poco y se ve el avance; puede cerrar la ventana y la importación sigue. Al terminar, cada persona dice cuántos días de turnos se le cargaron o cuántas tareas se le crearon.

---

## Qué ve cada persona

En la app, la semana importada:

- **Por turnos**: sus turnos de cada día, con el recordatorio de entrada y de salida. Ficha contra la sucursal, como siempre.
- **Por tareas**: sus trabajos, cada uno con su hora y su dirección. Fichará en la dirección de cada trabajo, y su horario de cada día son esos trabajos.

Las fechas pasadas no se cargan: los días anteriores a hoy quedan como estaban.

---

## Volver a subir la misma semana

Si la semana cambia, rellene la plantilla con la versión buena y súbala otra vez:

- **Por turnos**: cada día que trae el fichero sustituye lo que había ese día. No se duplica nada.
- **Por tareas**: la semana se sustituye. Los trabajos que ya no aparecen **se retiran**, salvo los que la persona ya haya empezado: esos se quedan y la revisión lo avisa.

---

## La semana de una sola persona

Abra la ficha de la persona y pulse **Editar**. En **Horarios y festivos**, con la persona **Por turnos** o **Por tareas**, pulse **Subir un cuadrante** en **Importar cuadrante por turnos** o en **Importar cuadrante semanal**. Puede hacer lo mismo para ella sola:

- **Descargar plantilla** baja una plantilla con su pestaña.
- También puede subir el documento que imprime su programa de gestión (PDF, Excel o CSV). En ese caso la plataforma le enseña qué ha entendido de cada columna para que lo confirme antes de seguir, y tarda algo más.

A quien está en **Semana tipo** no se le sube cuadrante.

---

## Quién puede importar

Las personas con acceso de gestión al panel de la empresa.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Por turnos: el horario son los turnos que usted carga](./114-calendario-de-turnos-por-fecha.md) | Los tres modos del horario y el cuadrante de turnos |
| [Horarios base y turnos](./23-horarios-base-y-turnos.md) | La semana tipo, con uno o varios turnos por día |
| [Festivos y días no laborables](./29-festivos-y-dias-no-laborables.md) | Por qué un trabajo en un día de vacaciones bloquea a esa persona |

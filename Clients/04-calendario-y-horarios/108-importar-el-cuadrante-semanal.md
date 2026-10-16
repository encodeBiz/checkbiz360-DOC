# Importar el cuadrante semanal

Cuando el trabajo cambia cada semana —ayuda a domicilio, limpieza por centros, mantenimiento—, teclear la semana de cada persona, trabajo a trabajo, es una mañana perdida cada lunes. Esta guía explica cómo cargar de una vez la semana de toda la plantilla de una sucursal con una hoja de Excel, o la de una sola persona desde su ficha.

---

## Qué resuelve

- **Una subida para toda la plantilla.** Un fichero por sucursal y semana, con una pestaña por persona. No hace falta ir ficha por ficha.
- **Cada persona recibe su semana en el móvil**: su horario de cada día y un trabajo por cada servicio, con la dirección donde tiene que fichar.
- **Nada se guarda sin que lo vea antes.** La plataforma enseña lo que hará con cada persona y solo lo aplica cuando usted lo confirma.
- **Corregir es volver a subir.** Si la semana cambia, se sube el fichero corregido: lo que ya estaba se actualiza y no se duplica nada.

---

## Cómo funciona, en tres pasos

| Paso | Qué pasa |
|---|---|
| **1. Descargar la plantilla** | Desde la sucursal, para la semana que elija. Trae una pestaña por cada persona de la sucursal. |
| **2. Rellenarla y subirla** | Una fila por trabajo. Al subirla no se guarda nada todavía. |
| **3. Revisar y confirmar** | La plataforma enseña qué hará con cada persona. Solo al confirmar se aplica. |

---

## 1. Descargar la plantilla

1. Vaya a **Sucursales** y abra la ficha de la sucursal.
2. En la pestaña **Horarios y festivos**, despliegue **Cuadrante semanal de la plantilla** y pulse **Importar cuadrante**.
3. Elija la semana y pulse **Descargar plantilla**.

La plantilla trae una primera hoja con las instrucciones y la lista de la gente, y **una pestaña por persona**, con su nombre.

> **No borre la fila 1 de cada pestaña**: es la que dice de quién es. Puede cambiar el nombre de la pestaña o reordenarlas sin problema.

Cada pestaña trae **dos filas de ejemplo** que empiezan por la palabra **ELIMINAR**: puede borrarlas o dejarlas, porque no se importan.

### Columnas

| Columna | Qué poner |
|---|---|
| **Fecha** * | El día del trabajo: 19/10/2026. |
| **Hora inicio** * | A qué hora empieza: 08:00. |
| **Hora fin** * | A qué hora acaba: 10:00. |
| **Cliente** | Para quién es el trabajo: la persona atendida, la comunidad, la empresa. |
| **Dirección** | Dónde se hace. Es el lugar donde la persona tendrá que fichar. |
| **Trabajo** | Qué se hace: limpieza, acompañamiento, revisión. |
| **Viaje (min)** | Minutos de desplazamiento hasta ese trabajo. |

Las columnas con asterisco son obligatorias. La **dirección** conviene ponerla siempre: sin ella el trabajo se crea igual, pero se podrá fichar desde cualquier sitio.

### Qué significa dejar una pestaña vacía

- **Una pestaña vacía** deja a esa persona como está. No es «esa semana no trabaja»: es que no se dice nada de ella.
- **Una pestaña con trabajos** es la semana entera de esa persona: los días sin ninguna fila quedan libres.

---

## 2. Subir el fichero

Pulse **Elegir fichero**, seleccione la plantilla rellena y pulse **Ver la propuesta**. Vale el Excel (.xlsx) de hasta 2 MB, guardado con Excel o con cualquier otro programa de hojas de cálculo. No vale en CSV, porque un CSV no tiene pestañas.

Si sube un fichero que no es la plantilla, la plataforma lo dice y no lee nada.

---

## 3. Revisar lo que se hará

Antes de confirmar, cada persona aparece con su estado, sus trabajos y las horas de la semana:

| Estado | Significa |
|---|---|
| **Lista** | Todo se ha leído bien. Se aplicará al confirmar. |
| **Bloqueada** | Algo impide aplicarla: una fila mal escrita (se indica cuál), o trabajos en un día que para esa persona es festivo o de vacaciones. Esa persona no se aplica; las demás, sí. |
| **Sin cambios** | Su pestaña está vacía. No se toca. |
| **Pestaña no reconocida** | La pestaña no corresponde a nadie de la sucursal. Compruebe la fila 1. |
| **Pestaña repetida** | Hay dos pestañas para la misma persona y no se sabe cuál vale. |

Al lado de cada persona salen también los avisos que conviene mirar: dos trabajos que se solapan, trabajos sin dirección, o un desplazamiento antes del primer trabajo más largo que el margen que tiene la persona para fichar la entrada.

Lo que pide atención sale primero. Si quiere arreglar a una persona bloqueada, corrija el fichero y pulse **Subir otro fichero**. Si cierra la ventana sin confirmar, no se guarda nada.

Cuando esté conforme, pulse **Confirmar**. Con mucha gente tarda un poco y se ve el avance; puede cerrar la ventana y la importación sigue.

---

## Qué ve cada persona

En la app, la semana importada: su horario de cada día y sus trabajos, cada uno con su hora y su dirección. Fichará en la dirección de cada trabajo.

- Con el horario de siempre, su jornada de cada día va de la primera hora del primer trabajo a la última del último.
- Si la persona trabaja con **Horario por tareas**, su horario de cada día son sus trabajos, uno detrás de otro, con los huecos entre medias. Un día sin trabajos es un día libre. En la app ve siempre la semana en curso tal como está en ese momento.

---

## Volver a subir la misma semana

Si la semana cambia, rellene la plantilla con la versión buena y súbala otra vez:

- Lo que ya estaba **se actualiza** y no se duplica.
- Los trabajos que ya no aparecen **se retiran**, salvo los que la persona ya haya empezado: esos se quedan y la revisión lo avisa.

---

## La semana de una sola persona

Desde la ficha de la persona, en **Horarios y festivos**, despliegue **Importar cuadrante semanal** y pulse **Subir un cuadrante**. Puede hacer lo mismo para ella sola:

- **Descargar plantilla** baja una plantilla con su pestaña.
- También puede subir el documento que imprime su programa de gestión (PDF, Excel o CSV). En ese caso la plataforma le enseña qué ha entendido de cada columna para que lo confirme antes de seguir, y tarda algo más.

---

## Quién puede importar

Las personas con acceso de gestión al panel de la empresa.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Horarios base y turnos](./23-horarios-base-y-turnos.md) | El horario de siempre, con uno o varios turnos por día |
| [Festivos y días no laborables](./29-festivos-y-dias-no-laborables.md) | Por qué un trabajo en un día de vacaciones bloquea a esa persona |

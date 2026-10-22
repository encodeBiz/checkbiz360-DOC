# Calendario: turnos cargados por fecha

El horario semanal sirve cuando todas las semanas se parecen. Cuando cada semana es distinta, una semana tipo que se repite se queda corta: el martes 21 hay un turno y el martes 28 otro. Para eso está el modo **Calendario**. El horario de cada persona es lo que usted carga en un calendario de turnos, fecha a fecha, y la persona ficha con el gesto de siempre.

---

## Qué resuelve

- **Planificar mes a mes.** Cada día lleva sus turnos, sin plantillas que se repitan solas.
- **Fichar normal.** La persona ficha como siempre contra el turno de ese día, sin tener que iniciar tareas.
- **Meter el trabajo dentro del turno.** Las tareas del día son tareas normales, dentro de su turno.

Si no está en el cuadrante, no trabaja. Un día sin turnos cargados es libre.

---

## Los tres modos del horario

En **Horarios y festivos**, el apartado **Cómo se organiza el horario** tiene tres opciones:

| Modo | De dónde sale el horario de cada día |
|---|---|
| **Horario semanal** | De la semana tipo, que se repite todas las semanas. |
| **Horario por tareas** | De las tareas de ese día: cada tarea es un turno. Solo se elige en la ficha de una persona. |
| **Calendario** | De los turnos cargados para esa fecha. Un día sin cargar es libre. |

**Calendario** se puede poner en la empresa, en una sucursal o en una persona, y se hereda como el resto del horario: manda el nivel más cercano. Un cuadrante se planifica por sucursal, así que lo normal es ponerlo en la sucursal. Si en esa sucursal hay alguien con horario fijo, por ejemplo la administración, déjele **Horario semanal** en su ficha.

> **Aviso:** al poner **Calendario** en una sucursal, quien no tenga turnos cargados tendrá los días libres hasta que se le carguen. No podrá fichar esos días. Quien tenga otro modo en su ficha no cambia. El panel se lo recuerda antes de guardar.

Quitar el modo no borra los turnos cargados. Simplemente dejan de usarse.

---

## Cargar los turnos

En la ficha de la sucursal o en la de la persona, en **Horarios y festivos**, aparece el **Calendario de turnos**. En la sucursal enseña la semana de todas sus personas, una fila por persona. En la ficha de una persona enseña solo la suya.

1. Muévase de semana con las flechas, o vuelva a **Hoy**.
2. En el día y la persona que quiera, pulse **Añadir turno**.
3. Ponga la **Entrada** y la **Salida** y pulse **Guardar**.
4. Si el día es partido, añada un segundo turno. Dos turnos del mismo día no pueden cruzarse.

Para cambiar un turno, tóquelo. Para que el día vuelva a ser libre, pulse **Quitar**.

Cada día se ve de una de tres formas:

| En pantalla | Qué significa |
|---|---|
| **Turno** | Tiene turnos cargados, con su hora de entrada y de salida. |
| **Libre** | Alguien lo ha dejado sin turnos a propósito. |
| **Sin cargar** | Nadie le ha cargado nada todavía. Para el fichaje es un día libre, pero se distingue para que se note lo que falta. |

Los días que ya pasaron no se cambian. El día de hoy sí.

### Copiar la semana

**Copiar a la semana siguiente** copia los turnos de la semana que está viendo a la siguiente, persona a persona. Lo que ya hubiera esos días se sustituye. Es la forma rápida de montar un mes que se parece semana a semana, y después retocar lo que cambie.

### Crear una tarea dentro de un turno

Desde un turno, **Crear tarea** abre el formulario de siempre con la persona, el día y la hora ya puestos. La tarea es una tarea normal: crearla no cambia el turno, y fichar no la inicia ni la cierra.

### Cargar un mes desde Excel

El [importador del cuadrante](108-importar-el-cuadrante-semanal.md) también sirve. Para quien está en **Calendario**, cada fecha de la plantilla carga el turno de ese día, de la primera a la última hora, además de crear las tareas como siempre. Una plantilla con un mes entero carga el mes de cada persona. Las fechas pasadas se saltan.

---

## Qué ve la persona

En la app, su semana con los turnos cargados y el recordatorio de entrada y de salida de cada turno, como con el horario semanal. Ficha con el gesto de siempre. Los festivos y sus ausencias siguen mandando: un festivo o unas vacaciones bloquean el fichaje aunque haya un turno cargado ese día.

---

## Dónde se mide el fichaje

El turno no lleva lugar propio. El fichaje se mide contra la **sucursal**, como con el horario semanal. Cada tarea con dirección se mide contra su propio lugar al iniciarla.

Si el trabajo es fuera de la sucursal, cree una sucursal con la geocerca desactivada para que se pueda fichar desde cualquier sitio, y ponga la dirección en cada tarea. Tenga en cuenta que una tarea sin dirección en esa sucursal no comprueba ningún lugar.

---

## Quién puede cargar turnos

El propietario y los administradores de la empresa, y los supervisores de la sucursal de la persona.

---

## Problemas frecuentes

| Qué pasa | Qué hacer |
|---|---|
| «Esta persona no está en «Calendario»» | Elija ese modo en su horario o en el de su sucursal. Solo se cargan turnos a quien está en el modo. |
| «Un día ya pasado no se cambia» | Los días anteriores a hoy quedan como estaban. Si hay que corregir un fichaje, hágalo desde la revisión de fichajes. |
| «Dos turnos del mismo día no pueden cruzarse» | Ajuste las horas para que un turno termine antes de que empiece el otro. |
| Alguien no puede fichar tras activar el modo | Su día está **Sin cargar**. Cárguele el turno desde el calendario de turnos. |

---

## Artículos relacionados

- [Horarios base y turnos](23-horarios-base-y-turnos.md)
- [Herencia de configuración](26-herencia-de-configuracion.md)
- [Importar el cuadrante semanal](108-importar-el-cuadrante-semanal.md)
- [Tablero de disponibilidad](98-tablero-de-disponibilidad.md)
- [Geocercas y radio de fichaje](../03-control-horario/16-geocercas-radio-de-fichaje.md)
- [Su gestor operativo en Claude o ChatGPT](../15-integraciones/109-su-gestor-operativo-en-claude-o-chatgpt.md)

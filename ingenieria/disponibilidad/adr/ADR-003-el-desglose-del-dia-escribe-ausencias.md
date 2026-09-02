# ADR-003 — El desglose del día escribe ausencias, y el gesto no es sólo arrastrar

**Fecha:** 2026-09-02
**Estado:** Propuesto — con dos puntos pendientes de confirmar (§Pendiente)
**Decisionario:** Jose Acevedo

---

## Contexto

El desglose de un día del tablero enseña dos columnas: quién está disponible y quién no, con el
motivo. Es información correcta y es información muerta: el gesto que sigue casi siempre —*esta
persona mañana no viene*— obliga a salir del tablero, entrar en la ficha del empleado, abrir su
calendario, añadir la ausencia y volver. Cinco pasos para un dato que se está mirando.

La operación inversa es igual de frecuente y aún más incómoda: alguien vuelve antes de lo
previsto y hay que quitarle un día libre que ya estaba puesto.

Cuatro caminos.

**Opción A — Dejarlo en lectura, con enlace.** Cada persona enlaza a su calendario. Cero riesgo,
cero ahorro.

**Opción B — Arrastrar entre columnas, y escribir al soltar.** El gesto más directo: sueltas y
queda hecho.

**Opción C — Arrastrar entre columnas, y al soltar abrir el modal que ya existe.** El arrastre
elige a quién y hacia dónde; el modal confirma y recoge el resto.

**Opción D — Opción C más un botón de flecha en cada fila** que hace exactamente lo mismo sin
arrastrar.

---

## Decisión

Se elige la **Opción D**.

De *Disponibles* a *No disponibles* se abre `HolidayModal` en scope empleado, con la fecha y la
persona ya puestas. De *No disponibles* a *Disponibles* se abre un modal con **las ausencias
propias** de esa persona, para borrar la que sobra. Las dos direcciones tienen su flecha en la
fila, y el arrastre es un atajo, no la única vía.

**Escribir nunca ocurre al soltar.** Siempre media un modal que hay que confirmar.

---

## Justificación

**Soltar no debe escribir, y eso es lo que hace seguro el arrastre.** Un arrastre accidental en
una lista con scroll es cuestión de tiempo. Si al soltar se abre un modal, el accidente cuesta
un clic en *Cancelar*; si al soltar se escribe, cuesta una ausencia inventada en el calendario
de alguien, que además nadie va a mirar hasta que le descuenten el día. Eso descarta la
Opción B.

**El arrastre solo excluye a media plantilla de usuarios.** No hay recorrido por teclado, los
lectores de pantalla no lo anuncian, y en tablet —que es donde se consulta un tablero de
cobertura, de pie y en un almacén— arrastrar dentro de una lista que también hace scroll es un
suplicio. El botón no es una concesión de accesibilidad: en tablet va a ser el camino principal
y el arrastre el secundario. Por eso la Opción C no basta.

**Sólo una de las cuatro razones se arregla desde aquí.** La columna de no disponibles mezcla
cuatro cosas distintas, y devolver a alguien a *disponible* significa algo diferente en cada
una:

| Motivo | ¿Reversible desde el panel? | Por qué |
|---|---|---|
| `absence` — ausencia suya | **Sí** | Es su propio día libre: se borra y vuelve |
| `holiday` — festivo de entidad o sucursal | **No** | Borrarlo se lo quita a toda la plantilla, no a esa persona |
| `noShift` — su horario no tiene turno ese día | **No** | No hay nada que borrar; sería editarle el horario |
| `employeeStatus` — de baja o vacaciones en la ficha | **No** | No tiene fechas: es cambiar su estado, en otro formulario |

Los tres irreversibles **se bloquean en el origen** —no arrastrables, flecha deshabilitada— con
un tooltip que dice por qué y, cuando lo hay, un enlace al sitio correcto: el calendario de la
sucursal para un festivo local, la ficha del empleado para una baja. Dejar arrastrar y luego dar
un error es enseñar una puerta que no abre.

**No hace falta contrato nuevo.** `upsertCalendar` (`PATCH`) y `deleteCalendarItem` (`DELETE`)
ya existen en el handler de calendario y hacen exactamente esto. El panel gana escrituras sin
que el módulo gane superficie.

**Después de escribir, el número se vuelve a pedir.** No se parchea en memoria. Es la misma
lección de [ADR-001](./ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md): un tablero
de cobertura que enseña un número que él mismo se ha inventado es peor que uno que tarda medio
segundo más. Se refresca el día afectado y su celda.

---

## Consecuencias

**Positivas:**

- El gesto que sigue a mirar el tablero se hace en el tablero. Cinco pasos pasan a dos.
- Las dos direcciones son simétricas y explicables: una añade un día libre, la otra lo quita.
- Sin contrato nuevo: sólo se consumen `PATCH` y `DELETE` que ya estaban.
- El bloqueo por motivo convierte una ambigüedad en una explicación: quien intenta devolver a
  alguien que está de baja se entera de por qué no puede y de dónde sí.

**Negativas / Compromisos aceptados:**

- **Primer drag & drop del repo.** No hay ninguna librería ni un solo `draggable` en `src`. La
  implementación usa **arrastre HTML5 nativo, sin dependencia nueva**: lo que hacía falta de
  `@dnd-kit/core` era el recorrido por teclado, y eso ya lo da el botón de la fila. La librería
  vuelve a la mesa el día que el arrastre tenga que hacer algo más fino que dos columnas.
- **Ver el tablero y escribir ausencias dejan de ser el mismo permiso.** Hasta ahora la
  disponibilidad era sólo lectura y bastaba el nivel de [TDR-001](../tdr/TDR-001-calculo-de-disponibilidad.md) §5.
  Escribir es otra cosa y hay que decidirla aparte (§Pendiente).
- `HolidayModal` necesita un `defaultDate`: hoy, en scope empleado y modo creación, **siempre**
  enseña el selector de rango, nunca un día suelto.
- Cada escritura cuesta un refresco del día. Es una llamada corta, pero el panel deja de ser
  gratis.
- Dos filas con la misma anchura ganan un botón: en la columna de no disponibles conviven ya el
  nombre y el chip del motivo, y la flecha aprieta. Va al final, sólo icono, y el chip trunca.

---

## Pendiente de confirmar

1. **El bloqueo del arrastre inverso** en los tres motivos que no son ausencia propia. La
   alternativa sería permitirlo y explicar el error después; se propone bloquear.
2. **Qué nivel puede escribir.** Se propone que `supervisor` vea el tablero pero **no** dé de
   alta ausencias, y que escribir requiera `manager` o superior. Es una decisión de producto, no
   técnica.

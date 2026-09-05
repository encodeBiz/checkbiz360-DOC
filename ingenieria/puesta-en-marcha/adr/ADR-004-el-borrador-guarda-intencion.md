# ADR-004 — El borrador guarda intención; el seed produce documentos

**Fecha:** 2026-09-05
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Al construir el primer borrador real —el de [Tapissat](../02_caso-real-tapissat.md)— la
primera versión expandía todo hasta el nivel del documento que acabará en Firestore: las
cuatro responsabilidades se convertían en 16 filas y las 17 líneas de festivos en 66.

Sale una tabla de 98 filas que es exacta y que **no sirve para nada de lo que el borrador
tiene que servir**:

- **No se puede revisar.** El cliente dijo «vacaciones de Navidad, del 23 de diciembre al 6
  de enero». Quince filas sueltas de diciembre no se parecen a eso.
- **Pierde la intención.** Una vez expandido, ya no consta que esos quince días eran un
  periodo. Cambiar las fechas obliga a rehacer quince entradas y a acordarse de cuáles eran.
- **No es lo que se aprueba.** El documento que firma el cliente antes de sembrar tiene que
  hablar su idioma, y su idioma son periodos y personas, no documentos de una colección.

## Decisión

**El borrador guarda lo que el cliente quiso decir. El seed lo traduce a documentos en el
momento de escribir.**

En concreto:

| El borrador guarda | El seed produce |
|---|---|
| «Vacances Nadal, del 23/12 al 06/01» | 15 `Holiday`, uno por día |
| «es supervisor en sus cuatro sedes» | 4 `EmployeeResponsibility`, una por sucursal |
| una dirección postal | unas coordenadas, con su precisión |
| una sucursal | la sucursal **y** su patrón inicial |

La expansión es mecánica y no requiere criterio, que es justo la razón por la que le toca a
la máquina y no a la revisión humana.

## Consecuencias

**El borrador es legible y editable a mano.** Cabe en pantalla, y una corrección se hace en
un sitio.

**Lo que no se puede saber se pone a `null` y genera una pregunta**, con su ruta dentro del
borrador y con el motivo por el que hace falta. Nunca un valor inventado. Y las preguntas
distinguen las que impiden sembrar de las que no: el municipio en vez de la provincia se
puede arreglar después; un coste por hora que falta, no.

**El seed lleva la lista de lo que añade por su cuenta**, escrita en el propio borrador
(`al_sembrar`), para que lo que va a pasar esté a la vista antes de que pase.

**Los datos personales no entran en el repositorio ni en una colección nueva.** El borrador
es un fichero temporal ([ADR-001](./ADR-001-merlin-edita-un-borrador.md)): la documentación
describe la forma y los datos mueren con la puesta en marcha.

# 03 · La conversación, el borrador y el seed

## Qué hace el asistente, en una frase

**Va pidiendo los datos por bloques, en el orden en que dependen unos de otros, acepta lo que
el cliente le dé en el formato que sea, y con eso rellena un borrador que al final se puede
enseñar, aprobar y sembrar.**

No es un importador de ficheros. Un importador espera a que le llegue algo completo. Esto
conduce: pregunta, explica por qué lo necesita, recibe lo que sea —un pegote de texto, un
CSV, el Excel de la gestoría, una lista de nombres— y va cerrando bloques.

---

## El recorrido

El orden no lo elige el asistente: lo impone el modelo, porque cada bloque necesita ids del
anterior ([01_as-is](./01_as-is.md)).

**1 · Empresa.** Nombre comercial, razón social, NIF, dirección legal, correo de facturación,
idioma y zona horaria. Es el único bloque que se puede rellenar hablando, sin fichero.

**2 · Sucursales.** Aquí el asistente tiene que explicar antes de pedir, porque «sucursal» no
significa lo que el cliente cree. Es *un lugar donde se ficha*: puede ser una sede propia, una
obra, o la fábrica de un cliente —como en [Tapissat](./02_caso-real-tapissat.md), donde tres
de las cuatro son clientes suyos—. Pide nombre y dirección, y avisa de que el radio de la
valla se mide desde ese punto.

**3 · Empleados.** Nombre, correo —que es su acceso—, DNI, puesto y en qué sucursales trabaja.

**4 · Responsabilidades.** Qué es cada persona y **cuánto cuesta su hora**. El asistente tiene
que insistir aquí: sin coste por hora, la mitad del producto que el cliente ha comprado
enseña ceros para siempre
([ADR-002](./adr/ADR-002-la-puesta-en-marcha-siembra-patron-y-coste.md)).

**5 · Horarios.** El bloque donde más hay que explicar y menos hay que asumir. El asistente
plantea la cascada: *«¿todos trabajan igual, o cada centro tiene su horario, o hay gente con
horario propio?»*, y según la respuesta rellena el nivel de entidad, el de sucursal o el de
empleado. Los tres niveles existen y se heredan; el cliente no tiene por qué saberlo, pero sí
tiene que elegir.

**6 · Festivos y ausencias.** Los del calendario laboral que le toque, más los cierres de
empresa.

En cualquier momento el cliente puede irse. El borrador guarda por dónde iba y el asistente
retoma diciendo qué falta.

---

## El borrador

Un documento por entidad, versionado, que es lo único que el asistente toca
([ADR-001](./adr/ADR-001-merlin-edita-un-borrador.md)). Tiene la misma forma que la plantilla
—empresa, sucursales, empleados, responsabilidades, los tres niveles de horario, festivos—
porque así **se puede emitir de vuelta como el mismo libro de Excel** que el cliente ya
entiende, y ese es el documento que firma antes de sembrar.

Cada dato guarda de dónde salió: si lo dijo el cliente hablando, si vino de una celda, o si lo
dedujo el asistente. Sin esa traza no se puede revisar nada, y el día que un horario salga
raro no habrá manera de saber si lo dijo alguien o se lo inventó la máquina.

Las correcciones viven en el borrador, no en el hilo. Cuando se resuelve que «T. Centro» y
«Tienda Centro» son la misma, eso se escribe. Si vive en la conversación, a la tercera sesión
se ha perdido.

---

## Lo que el asistente no puede hacer

**No inventa un valor que no ha leído.** Si el horario no está claro, se queda vacío y
pregunta. Un turno alucinado en una plataforma de fichajes no es un fallo de interfaz.

**No acepta un dato que huele a ejemplo.** Tapissat entregó los costes de muestra de la
plantilla sin tocarlos. El asistente compara contra los valores de ejemplo conocidos y, si
coinciden, pregunta en vez de importar.

**No traduce un «sí» sin entenderlo.** «Trabaja fuera de oficina» suena a *se mueve entre
sedes* y significa *queda exento del control de ubicación*. Cuando una respuesta tiene una
consecuencia que el cliente no puede prever, el asistente la dice antes de aceptarla.

**No da por completa una fila a medias.** La del owner de Tapissat se acababa en el rol.

---

## Del borrador a la plataforma

Cuando el borrador está aprobado, un seed lo ejecuta. Hereda las costumbres del repo: simula
por defecto, escribe sólo con `--apply`, es determinista y trae su deshacer desde el primer
día, porque volver atrás no es gratis.

Y hace tres cosas que no están en el borrador pero sin las cuales el cliente no funciona:

1. **Geocodifica cada sucursal** y deja a la vista la precisión que devuelve. Con radios de
   500 m, la diferencia entre `rooftop` y `approximate` es poner la valla en la nave o en
   mitad del polígono.
2. **Crea el patrón inicial de cada sucursal** en `checkbiz_branch_patterns`. Sin ese
   documento el trigger no acumula nada y el cliente ficha un mes sin generar un solo dato.
3. **Expande los rangos**. Los festivos del modelo son fechas sueltas; las 17 filas de
   Tapissat son 66 documentos.

**Idempotente por clave natural** —nombre de sucursal, correo de empleado— y no por id
generado. Cuesta poco y cubre los dos casos: la entidad nueva y vacía, que es lo normal, y la
que el cliente ya empezó a tocar por su cuenta, donde es lo único que evita duplicarle la
plantilla a alguien que ya está fichando.

# ADR-003 — `checkinbiz` es el núcleo; cada CRUD de gestión, su propio contenedor

**Fecha:** 2026-09-08
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

`checkinbiz` nació como el servicio del fichaje y ha ido acumulando puertas: el acceso de la
app, el calendario, los fichajes, los colaboradores, el buscador de direcciones, la gestión de
plantilla, y tenía apuntadas la heurística y el histórico de patrones. Ese es exactamente el
camino por el que un servicio se convierte en un monolito pequeño: ninguna de las incorporaciones
fue una mala decisión por separado.

Y quedan tres CRUD por portar —empleados, centros y empresa— que, por inercia, acabarían
también ahí.

La pregunta no es dónde caben, es qué puede permitirse compartir proceso con el fichaje.

## Decisión

**`checkinbiz` es el núcleo.** Contiene el camino crítico —validar, entrar, segundo factor,
calendario, fichar— y aquello de lo que ese camino depende para ser correcto: los colaboradores,
porque su lectura es la que resuelve `canWrite` sobre cada escritura, y `geo`, porque las
coordenadas que devuelve son contra las que después la valla acepta o rechaza un fichaje.

**La gestión de plantilla sale a `employees`.** Y los dos CRUD que faltan por portar nacen en su
propio contenedor: `branches` y `entities`, este último con usuarios y media.

La heurística, cuando se porte, va a `analytics`. Al núcleo no vuelve a entrar nada.

## Razones

**El criterio no es «si se cae, nadie ficha».** Con esa vara, ni `geo` ni el CRUD de
colaboradores serían núcleo: se pueden caer los dos y todo el mundo sigue fichando. La vara que
se adopta es más amplia y es la que corresponde al producto: **entra lo que, si escribe algo
equivocado, se manifiesta como un fichaje que no cuenta.** Una coordenada mal resuelta pone la
valla trescientos metros más allá y los fichajes reales empiezan a salir `out_of_radius`, y eso
nadie lo lee como un fallo del buscador de direcciones.

**Esa vara no es suficiente sola, y por eso va acompañada de una segunda: el ritmo de cambio.**
La gestión de plantilla también puede estropear un fichaje —un empleado con el centro mal
asignado ficha fuera de zona—, así que por corrección se quedaría. Lo que la echa fuera es que
es el CRUD que más se toca: pantallas de gestión, importaciones, add-ons que dan de alta
personal. Lo que cambia todas las semanas no puede compartir proceso con lo que no puede
fallar. `geo` y colaboradores son pequeños y llevan meses quietos.

**Y sacar `employees` es casi gratis.** Su dominio ya vive en `packages/shared/src/checkbiz/employees/`
—`rentman` lo llama sin pasar por ningún servicio— y en `checkinbiz` solo queda un router de 95
líneas. Lo que se muda es la puerta.

## Consecuencias

- Tres servicios nuevos: `employees` (3013), `branches` (3014) y `entities` (3015), con el
  andamio calcado de `events`.
- `checkinbiz` pierde su único motivo frecuente de redespliegue. Un fallo en el alta de un
  empleado deja de poder tumbar el fichaje.
- La app móvil no se toca: todo lo que usa se queda donde está.
- El `CheckinbizClient` del `backoffice` tampoco: los colaboradores no se mueven.
- **Hay que sostener la barrera.** Un criterio amplio deja entrar cosas si nadie lo vigila, y la
  próxima incorporación al núcleo también parecerá razonable por separado. Cada una tiene que
  pasar las dos varas: que su error salga como un fichaje que no cuenta, y que no sea código que
  se toque a menudo.

## Alternativa descartada

Dejar los tres CRUD en `checkinbiz`, que es lo que la inercia haría y lo que menos trabajo da
esta semana. Se descarta porque devuelve el problema del que se está saliendo: un servicio que
lo sirve todo, se despliega por cualquier motivo y arrastra en cada arranque dependencias que el
fichaje no necesita.

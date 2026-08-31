# ADR-007 — La geocerca de un trabajo vive en la tarea, y se valida al empezarla

**Fecha:** 2026-09-01
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Hay clientes cuyo trabajo no ocurre en un centro fijo. El caso que dispara esto es una
**tapicería de automoción**: cada día se trabaja en una dirección distinta —el domicilio del
cliente, un taller ajeno, un parking—, y esa dirección no se repite.

Hoy la única geocerca de la plataforma está anclada a la sucursal: `branch.address.geo` como
punto y `branch.ratioChecklog` como radio, comprobados en el fichaje
(`createChecklog.controller.ts`). Para un trabajo a domicilio esa valla no dice nada: el
empleado nunca está en el taller.

Se valoraron tres caminos.

**Opción A — Una sucursal por trabajo.**
Dar de alta un centro de trabajo por cada encargo y fichar contra él.

**Opción B — Preguntar la tarea al fichar, y una sesión de fichaje por tarea.**
En el check-in la app enseña las tareas del día; el empleado elige una y la valla de esa tarea
sustituye a la de la sucursal. Fichar al llegar a cada trabajo y desfichar al terminarlo.

**Opción C — La tarea lleva su propio lugar de trabajo, y la valla se comprueba al marcar la
tarea como iniciada.** El fichaje no se toca.

---

## Decisión

Se elige la **Opción C**.

La tarea gana un campo opcional `workSite` —dirección, punto y radio propios—. Al pasar la
tarea a `in_progress` se comprueba la posición del empleado contra ese punto, de forma
restrictiva. **El registro de jornada no cambia en absoluto**: `createChecklog` sigue
validando contra la sucursal, con el mismo contrato y el mismo comportamiento.

Y se decide además **subir al servidor una regla que ya existe y hoy solo vive en el cliente**:
un trabajador solo puede **iniciar o completar** una tarea con la jornada abierta. La app ya lo
impide —`task_detail_page.dart` esconde los botones y ofrece ir a fichar cuando el estado de
asistencia no es `working` ni `onBreak`—, pero la API la acepta. Pasa a rechazarse también en
`tasks`.

---

## Justificación

**Una sucursal no es un sitio, es una unidad laboral.** Aporta el calendario, los turnos, los
festivos, las responsabilidades del empleado y el centro de coste — todo lo que se resuelve
en `createChecklog` antes de mirar siquiera las coordenadas. Crear una por encargo multiplica
sin techo el catálogo de centros para obtener un punto en un mapa, y ensucia todo lo que
agrega por sucursal: `BranchPattern`, `taskSignals`, el panel y los informes empezarían a
contar cientos de "centros" de un solo día. Eso descarta la Opción A.

**El desplazamiento entre trabajos es tiempo de trabajo.** Partir la jornada en una sesión de
fichaje por tarea deja el viaje fuera del registro, y en España el desplazamiento entre
centros dentro de la jornada es tiempo efectivo. La Opción B resolvía un problema de geocerca
creando uno laboral.

**Bloquear un check-in es bloquear un registro legal.** El código ya tomó esa decisión una vez
y está escrita: `buildOpenDefaultDay` existe para que un fichaje no reviente por falta de
configuración. Colgar una valla nueva y restrictiva del check-in va justo en contra de ese
principio — una dirección mal geocodificada dejaría a alguien sin poder fichar.

**Bloquear el inicio de una tarea no es lo mismo.** Cuando el empleado pulsa "empezar", su
jornada ya está registrada y ya está cobrando. Que no pueda abrir la tarea desde el sitio
equivocado es una molestia operativa, no un problema laboral. Por eso aquí sí se puede ser
tan restrictivo como el cliente pide, sin puertas de escape.

**La regla de jornada abierta no es nueva, y ése es el argumento para bajarla al servidor.**
El producto ya decidió que trabajar en una tarea exige estar fichado, y la app lo aplica. Lo
que no existe es la comprobación en la API: una versión antigua de la app, un cliente distinto
o una llamada directa con el staff JWT se la saltan sin resistencia. Mientras era solo cuestión
de higiene se podía vivir con ello; en cuanto la tarea pasa a llevar geocerca propia, es la
pieza que garantiza que **toda** tarea queda cubierta por alguna valla, y una regla que sostiene
una garantía no puede vivir en el cliente.

**Y trabajo registrado fuera de la jornada es una contradicción.** Si alguien está haciendo una
tarea, está trabajando; si está trabajando, su jornada está abierta. Permitir lo contrario deja
que las horas imputadas a tareas superen a las horas fichadas, que es el descuadre que hace
inservible cualquier informe de coste por trabajo.

**Las ventanas de tiempo ya existen.** La tarea sella `startedAt` y `completedAt` en sí misma
y en cada asignación (`updateTaskStatus.controller.ts`), y merlin y analytics ya consumen
`taskSignals`. No hace falta que el fichaje aporte nada para saber cuánto duró un trabajo.

**Son dos vallas en dos momentos, y ninguna sustituye a la otra.** La de la sucursal guarda la
jornada; la de la tarea guarda la tarea. Así el respaldo que se pedía —"si la tarea no tiene
geocerca, que valga la de la sucursal"— no hay que programarlo: se cumple solo, porque el
fichaje nunca dejó de validarse contra la sucursal. Y con la precondición de jornada abierta,
**toda** tarea queda cubierta por al menos una valla: la suya si la tiene, la de la sucursal
en el check-in que la precede si no.

---

## Consecuencias

**Positivas:**

- Coste cero por trabajo: `workSite` es un subdocumento dentro de una tarea que ya existe. Sin
  colección nueva, sin documentos nuevos, sin índices nuevos.
- Regresión cero en el fichaje: `createChecklog` no se toca ni en una línea, y ninguna tarea
  existente tiene `workSite`.
- El tiempo de desplazamiento queda **dentro** de la jornada, como debe estar, y además pasa a
  ser medible sin añadir ningún dato: es el hueco entre el `completedAt` de una tarea y el
  `startedAt` de la siguiente.
- La precondición de jornada abierta garantiza que las horas de tarea nunca excedan a las
  fichadas, sin necesidad de reconciliar nada después.
- **Para el usuario de la app no cambia nada:** ya se comportaba así. El servidor deja de
  confiar en que el cliente cumpla, que es lo único que se mueve.
- Señal nueva para merlin y analytics: dispersión geográfica y tiempo muerto en servicio a
  domicilio, donde hoy solo hay tasas agregadas por sucursal.

**Negativas / Compromisos aceptados:**

- El servicio `tasks` gana dos dependencias que antes no tenía: geocodificación
  (`@encodebiz/shared` → Google Maps, la misma del alta de centros) y lectura de la sesión de
  jornada abierta.
- La app móvil debe mandar `geo` al marcar inicio y fin de tarea, y tratar dos códigos de
  error nuevos. Es un cambio de contrato aditivo en `PATCH /:taskId/status`.
- La calidad de la valla depende de la calidad de la dirección. Se mitiga rechazando
  precisión `approximate` en la geocodificación (ver [TDR-005](../tdr/TDR-005-worksite-y-geocerca-de-tarea.md)).
- Se decide que `enableRemoteWork` y `disableRatioChecklog` **no** eximen de la valla de la
  tarea: si alguien le puso dirección al trabajo, el trabajo es ahí. Esas dos banderas siguen
  rigiendo el fichaje, que es su sitio.

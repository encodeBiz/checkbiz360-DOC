# Equipos

Un **equipo** guarda quién trabaja junto, con qué responsabilidad, en qué puesto y a qué precio por hora. Sirve para dar de alta a toda una cuadrilla en una sucursal —o en un proyecto u obra, según cómo llame su entidad a sus centros— de una sola vez, en lugar de hacerlo persona a persona.

Está pensado para empresas que mueven a la misma gente de un proyecto a otro: se configura el equipo una vez y se aplica a cada proyecto nuevo.

---

## Cómo funciona

- **Un equipo es una plantilla.** Cada miembro lleva su responsabilidad (trabajador, supervisor, gerente o propietario), su puesto y su precio por hora, pero no una sucursal.
- **Aplicarlo a una sucursal** da de alta en ella a cada miembro con esos datos, exactamente igual que si se hubiera hecho a mano.
- **La sucursal manda sobre la plantilla.** Cambiar un puesto o un precio en el equipo no cambia las sucursales donde ya se aplicó: eso se ajusta en cada sucursal. El precio que usan los costes y los informes es siempre el de la sucursal.
- **El horario no forma parte del equipo.** Se configura en la sucursal, como siempre.
- Una misma persona puede estar en **varios equipos**, pero no dos veces en el mismo.

Los equipos se encuentran en **Empleados**, pestaña **Equipos**.

---

## Crear un equipo

1. En el menú lateral, abra **Empleados** y sitúese en la pestaña **Equipos**.
2. Pulse **Crear equipo** e indique el **nombre del equipo**. No puede haber dos equipos con el mismo nombre; al comparar no cuentan las mayúsculas, las tildes ni los espacios sobrantes.
3. Abra el equipo con **Ver equipo** y pulse **Añadir miembro**.
4. Elija el **empleado**, su **responsabilidad**, su **puesto** —del catálogo de puestos o escribiendo uno nuevo— y su **salario por hora**.
5. Guarde. Repita el paso 4 con cada miembro.

Desde la ficha del equipo también se puede **editar** un miembro o **quitarlo del equipo**, y desde el listado, **renombrar** o **borrar** el equipo.

- Añadir o quitar a alguien de un equipo **no avisa a nadie** ni le da acceso a ningún sitio: solo cambia la plantilla.
- Quitar a una persona del equipo no la retira de las sucursales donde ya se aplicó.
- Borrar un equipo borra la plantilla; quien ya se dio de alta en una sucursal con ese equipo se queda donde está.
- No se puede añadir a un empleado dado de baja (`employee/fired`). Estar de vacaciones, de baja médica o con la ficha **pendiente** no impide estar en un equipo.

> **Consejo:** si ya tiene un proyecto con la cuadrilla dada de alta, lo más rápido es no empezar de cero: guarde la plantilla de esa sucursal como equipo (ver más abajo).

---

## Aplicar un equipo a una sucursal

1. Abra la ficha de la sucursal y, en su lista de empleados, pulse **Aplicar equipo**.
2. Elija el **equipo**. Antes de confirmar se muestran sus miembros con su puesto y su precio.
3. Revise la lista y confirme con **Aplicar a N personas**.
4. Al terminar, la pantalla muestra a quién se ha **dado de alta** y a quién **no**, con el motivo.

Qué ocurre al aplicar:

- Cada persona dada de alta queda vinculada a la sucursal con la responsabilidad, el puesto y el precio del equipo. Desde ese momento puede fichar en ella y se le pueden asignar las tareas de esa sucursal.
- Cada persona dada de alta **recibe el aviso** habitual de nueva asignación.
- **Aplicar nunca pisa lo que ya existe.** Quien ya estaba en esa sucursal se salta y conserva su puesto y su precio. También se salta a quien está dado de baja o tiene la ficha a medio hacer, y a quien ya no tiene ficha.

Los motivos que puede ver en «No se han dado de alta» son:

| Motivo | Qué significa |
|---|---|
| **Ya estaba en esta sucursal** | Tenía una responsabilidad en ella; se mantiene tal cual. |
| **Está de baja o con la ficha a medio hacer** | Su estado es de baja o *pendiente*: no puede trabajar todavía. |
| **Su ficha ya no existe** | El empleado se eliminó después de añadirlo al equipo. |

> **Importante:** revise la lista antes de confirmar. Aplicar el equipo equivocado a la sucursal equivocada envía un aviso a cada persona, y deshacerlo obliga a retirar a cada una de la sucursal.

Si mientras se aplica alguien da de alta en esa sucursal a uno de los miembros, la operación se detiene sin cambiar nada y aparece `team/apply_conflict`. Vuelva a aplicar el equipo: esa persona se saltará.

---

## Guardar la plantilla de una sucursal como equipo

1. Abra la ficha de la sucursal y, en su lista de empleados, pulse **Guardar como equipo**.
2. Dele un nombre y confirme.

Se copia a quien está activo en esa sucursal, con su responsabilidad, su puesto y su precio. **El horario no se copia**, y quien está dado de baja se salta. Una sucursal sin nadie activo no se puede guardar como equipo (`team/branch_without_staff`).

---

## Equipos y tareas

Los equipos se aplican a **sucursales**, no a tareas. Una vez aplicado el equipo, sus miembros forman parte de la sucursal y se seleccionan uno a uno en el formulario de la tarea, como cualquier otro empleado de esa sucursal.

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

Elegir en la tarea a toda la plantilla de la sucursal, filtrar por puesto o añadir un equipo entero de una vez está planificado para una versión futura.

---

## La app del empleado

No cambia nada para el empleado. Quien entra en una sucursal al aplicar un equipo ve esa sucursal en la app igual que si lo hubieran dado de alta a mano, sin necesidad de actualizarla.

---

## Quién puede gestionar equipos

Crear, editar y borrar equipos, aplicarlos y guardar una sucursal como equipo está reservado a los **propietarios y administradores** de la entidad con acceso activo al backoffice.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Asignar empleados a sucursales](../08-sucursales-y-entidad/60-asignar-empleados-a-sucursales.md) | Responsabilidades, multi-sucursal y asignación persona a persona |
| [Roles y niveles de responsabilidad](./07-roles-y-niveles-de-responsabilidad.md) | Los niveles que lleva cada miembro |
| [Crear y gestionar empleados](./06-crear-y-gestionar-empleados.md) | Alta de empleados y estados, incluido el estado pendiente |
| [Asignar tareas a empleados](../06-tareas/41-asignar-tareas-a-empleados.md) | Cómo se asignan las tareas a las personas de una sucursal |
| [Análisis de costes](../07-inteligencia-operativa/54-analisis-de-costes.md) | Por qué el precio que cuenta es el de la sucursal |

# 01 · Cómo se monta hoy un cliente

## La cadena, y por qué el orden no es negociable

Dar de alta un ecosistema son cinco pasos encadenados. Cada uno necesita ids que sólo
existen cuando el anterior ha terminado, así que no se pueden paralelizar ni reordenar:

```
entidad → sucursales → empleados → responsabilidades → calendario
```

**Entidad** (`entities/{id}`). Nombre comercial, `slug` —obligatorio, y hoy nadie lo pide en
ningún sitio—, razón social, NIF, dirección legal con coordenadas, correo de facturación,
idioma y el radio por defecto de la geocerca (`ratioChecklog`, en metros).

**Sucursales** (`entities/{id}/branches/{id}`). El nombre es lo único que las identifica de
cara al alta. Necesitan `address.geo` con latitud y longitud —es lo que sostiene la valla—,
zona horaria, y su propio radio si difiere del de la entidad.

**Empleados** (`entities/{id}/employees/{id}`). Nombre, correo —que es su acceso y por eso
tiene que ser único—, DNI, puesto, si es `internal` o `collaborator`, y la lista de
sucursales asignadas (`branchId` es un array: una persona puede estar en varios centros).
Crear un empleado de verdad crea además su usuario en Firebase Auth y le manda la
bienvenida.

**Responsabilidades** (`entities/{id}/employee_responsibilities/{id}`). Qué es cada persona
—`owner`, `manager`, `supervisor` o `worker`—, con qué alcance (toda la entidad, o una
sucursal concreta), y **con qué coste por hora**. El id se compone del empleado y del
alcance, así que es naturalmente idempotente.

**Calendario**, en cascada de tres niveles: `entities/{id}/calendar/config` con el horario
por defecto y los festivos de empresa; `branches/{id}/calendar/config` con las excepciones
de cada centro; y `employees/{id}/calendar/config` con las individuales y las ausencias. El
día efectivo lo resuelve `ResolveEffectiveDayUseCase`, que es también quien aplica el
fichaje, así que lo que se configure aquí es exactamente lo que se aplicará.

---

## Lo que cuesta

Una llamada de una a tres horas con el cliente, más el tiempo de traducir a mano su Excel.
El coste real no está en teclear: está en que el fichero que manda el cliente viene sucio
—sucursales escritas de tres maneras, gente sin correo, DNIs repetidos, horarios en prosa
del tipo *«de 9 a 2 y de 4 a 7, sábados alternos»*— y hay que interpretarlo persona a
persona.

Y en que **no hay punto de retorno**. Si a mitad se descubre que la estructura estaba mal,
deshacer no es borrar: `deleteEmployee` deja la ficha en `fired`, la entrada del
`searchIndex` se queda, el usuario de Auth sigue vivo y los patrones acumulados no se
restan. Lo habitual es seguir hacia delante con el error dentro.

---

## La plantilla que ya existe

Hay una plantilla en `encodebiz-api/outputs/onboarding-template/plantilla_alta_ecosistema_encodebiz.xlsx`,
con nueve hojas: instrucciones, empresa, sucursales, empleados, responsabilidades, horario
de empresa, de sucursal y de empleado, y festivos con ausencias.

**Está bien pensada.** La cascada de horarios de las hojas 05, 06 y 07 coincide exactamente
con `EntityCalendar` / `BranchCalendar` / `EmployeeCalendar`; los niveles 1, 2 y 3 son el
enum `ResponsibilityLevel`; el alcance entidad/sucursal es el mismo `HolidaySource`. Y
relaciona todo por nombre de sucursal y por correo, que es justo la clave natural que
necesita un alta repetible.

Revisada contra el modelo el 2026-09-03, le faltan cuatro cosas:

- **Nadie es `owner`.** Las tres personas de ejemplo son manager, supervisor y worker, pero
  el nivel 4 existe y es a quien `canWrite` deja entrar al panel. No hay ninguna casilla que
  diga quién administra la cuenta, que es lo primero que hace falta.
- **`coste_mes` no existe en el modelo.** `Job` sólo tiene `price`, y es por hora. La
  columna sobra, y si el cliente rellena las dos y no cuadran no hay regla que decida.
- **Biometría y trabajo remoto están en la hoja de sucursales**, pero en el modelo son
  campos del empleado. Ahí no tienen dónde caer.
- **Las fechas de festivos son una trampa de formato.** Las de ejemplo están escritas como
  instantes UTC y redondean bien si se convierten al huso; pero el cliente va a teclear
  `01/01/2026` en local, y la misma conversión que arregla unas corre las otras un día
  atrás. `Holiday.date` es un string `YYYY-MM-DD`: la columna tiene que ir como texto y
  entonces no hay nada que convertir.

Detalles menores del mismo repaso: las cabeceras están en la fila 1 en unas hojas y en la 3
en otras, y en la hoja 04 quedó un `coste_mes` suelto en la celda A1.

---

## Las cuatro trampas que no se ven

Están medidas contra `dev-encodebiz` y explicadas en el [README](./README.md): sin patrón de
sucursal el trigger no acumula nada; el coste por hora tiene que estar puesto antes del
primer fichaje porque el fichaje se lleva una copia; la plantilla entera sale `at-risk` el
primer mes; y deshacer no es gratis.

Ninguna de las cuatro da error. Las cuatro producen un cliente que *parece* montado.

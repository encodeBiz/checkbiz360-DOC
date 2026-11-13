# El cliente en la tarea

Una tarea con su cliente sabe dónde se hace, lleva a quien va a trabajar lo que necesita saber al llegar y cuenta en las horas, el contrato y el análisis de ese cliente. Todo se decide en el mismo formulario de siempre, **Nueva tarea**.

---

## Qué resuelve

- **No volver a escribir la dirección.** La del cliente sirve como lugar de trabajo, con su margen.
- **Que la plantilla llegue sabiendo.** Indicaciones, contactos a los que llamar y la ficha del cliente, en la propia tarea de la app.
- **Proteger lo que no debe salir.** El nombre del cliente solo se enseña si usted lo autoriza.
- **Saber de qué contrato es cada trabajo**, o dejar claro que no es de ninguno.

---

## Elegir el cliente al crear una tarea

1. En **Gestión de tareas**, pulse el botón de nueva tarea.
2. Elija primero la **sucursal**: los clientes salen de ella.
3. En **Cliente**, elija uno de los clientes asignados a esa sucursal, o deje **Sin cliente**. Si la sucursal no tiene clientes, el campo no aparece.
4. Si el cliente tiene contratos, aparece **Contrato**: elija de cuál es la tarea o **Sin contrato** (ver más abajo).
5. Si el cliente tiene dirección, aparece marcada **Usar la dirección del cliente como lugar de trabajo**, con la dirección debajo y su **Margen** en metros.
6. Rellene el resto de la tarea como siempre y guarde.

Si cambia de sucursal, el cliente y el contrato se vacían: hay que volver a elegirlos.

Una tarea interna (una reunión, un trabajo de oficina) no es de ningún cliente: déjela en **Sin cliente**.

---

## La dirección del cliente como lugar de trabajo

Con **Usar la dirección del cliente como lugar de trabajo** marcada, la tarea solo se puede iniciar desde esa dirección, igual que con un [lugar de trabajo propio](../06-tareas/40-crear-una-tarea.md#lugar-de-trabajo-propio).

- **Margen.** Los metros alrededor de la dirección desde los que se puede iniciar. Si no lo cambia, toma el de la sucursal. *Un garaje o una nave necesitan más margen que un portal.* El margen que ponga se guarda con la tarea y se conserva al volver a editarla.
- **Otra dirección.** Si el trabajo de hoy no es en la dirección del cliente, desmarque la casilla y escriba la dirección en **Lugar de trabajo (opcional)**.

---

## El contrato de la tarea

El desplegable **Contrato** sale en cuanto el cliente tiene algún contrato:

- **Al crear la tarea**, si el cliente tiene un único contrato vigente en esas fechas, viene propuesto. Puede cambiarlo.
- **Sin contrato** deja la tarea fuera de todos los contratos. Se respeta: crear un contrato nuevo más adelante no se la lleva.
- Una tarea solo cambia de contrato cuando usted lo elige en ella.

Las tareas que no pasan por este formulario (importadas, creadas desde la app o desde el asistente) toman al crearse el contrato vigente del cliente si solo tiene uno. Si no era de ese contrato, edítela y elija otro o **Sin contrato**.

Más sobre contratos en [Contratos y rentabilidad](./121-contratos-y-rentabilidad.md).

---

## La tarjeta del cliente en la ficha de la tarea

En la ficha de una tarea con cliente aparece la tarjeta **Cliente**, con todo lo que la acompaña:

- El nombre del cliente y una marca que dice si **La plantilla ve el nombre** o **La plantilla no ve el nombre**. **Ver ficha** lleva a la ficha del cliente.
- El **Contrato**, como enlace: abre la ficha del cliente con ese contrato desplegado.
- La **Dirección del cliente**.
- Las **Notas de campo**.
- Las **Personas de contacto**, con las visibles para la plantilla marcadas **Visible en campo**, y los botones **Llamar** y **Escribir un correo**.
- Los **Documentos** que ve la plantilla desde la tarea, para abrirlos o descargarlos.

Si la tarea tiene cliente, la ficha muestra también el bloque **Gastos** (solo a propietarios y administradores). Ver [Gastos del contrato y de la tarea](./122-gastos-del-contrato-y-de-la-tarea.md).

---

## Qué ve la plantilla en la app

En el detalle de la tarea, la persona asignada ve la tarjeta **Datos complementarios**, encima de **Equipo**, con:

- Las **Notas de campo** del cliente.
- Los **Contactos** marcados como visibles, con el botón **Llamar**.
- Los **Documentos del cliente** marcados para trabajadores.

El **nombre del cliente** solo aparece si en su ficha está marcada **Mostrar el nombre del cliente a la plantilla**. Si el cliente no tiene ningún dato para la plantilla, la tarjeta no sale. Los contratos, los presupuestos y todo lo marcado «Administración» no se ven nunca desde la app.

Para ver la tarjeta, la plantilla tiene que tener la app actualizada a la última versión.

---

## Buscar tareas por cliente

- **Lista de tareas.** En cuanto la empresa tiene clientes, aparece el filtro **Cliente** junto al de empleado.
- **Informe de tareas.** Si alguna tarea del informe tiene cliente, el Excel añade la columna **Cliente** detrás de **Centro**. Ver [Informes de tareas](../06-tareas/48-informes-de-tareas.md).

---

## Problemas frecuentes

**No aparece el campo Cliente.** La sucursal elegida no tiene clientes asignados. Asigne el cliente a esa sucursal desde su ficha.

**No aparece el desplegable Contrato.** El cliente no tiene contratos activos.

**La plantilla no puede iniciar la tarea.** Con la dirección del cliente como lugar de trabajo, solo se puede iniciar dentro del margen. Si el sitio es grande (una nave, un parking), suba el **Margen**.

**La plantilla no ve los datos del cliente.** Compruebe que la app está actualizada, que los contactos están marcados **Lo ve quien va a trabajar** y que los documentos están marcados para trabajadores.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una tarea](../06-tareas/40-crear-una-tarea.md) | Todos los campos del formulario de la tarea |
| [Dar de alta clientes](./118-dar-de-alta-clientes.md) | Dirección, contactos, notas de campo y la casilla del nombre |
| [Contratos y rentabilidad](./121-contratos-y-rentabilidad.md) | De qué contrato es cada tarea y cuánto deja |
| [Gastos del contrato y de la tarea](./122-gastos-del-contrato-y-de-la-tarea.md) | Lo que se paga fuera para la tarea |

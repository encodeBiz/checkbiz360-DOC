# Trabajo fuera del centro

CheckBiz360 contempla escenarios de trabajo fuera de las instalaciones de la empresa: montajes, servicios en casa del cliente, trabajo de campo o teletrabajo. La opción **Trabajo fuera del centro** permite que un empleado registre su asistencia sin estar dentro de la geocerca de una sucursal, manteniendo las validaciones de autenticación y de horario efectivo.

> **Nota:** hasta septiembre de 2026 esta opción se llamaba **Trabajo remoto**. Cambió el nombre, no el funcionamiento: «remoto» sugería teletrabajo desde casa, y la opción sirve para cualquier persona que no ficha en un centro.

---

## Qué es el trabajo fuera del centro

Es una configuración individual por empleado que deshabilita la validación de geolocalización durante el fichaje. Cuando está activa, el sistema no comprueba si el dispositivo se encuentra dentro del radio de la sucursal. El resto de validaciones (horario, dispositivo de confianza y biometría si aplica) siguen funcionando con normalidad.

Está pensada para empleados que trabajan de forma habitual o puntual fuera de las instalaciones: equipos de campo, técnicos que se desplazan, personal de montaje o eventos, y también teletrabajadores.

---

## Cómo activarlo para un empleado

La activación la realizan los usuarios con rol **manager** u **owner** desde la ficha del empleado en el backoffice.

1. Acceda al backoffice de CheckBiz360.
2. Navegue a la sección **Empleados** y abra la ficha del empleado.
3. Pulse **Editar**.
4. Active **Trabajo fuera del centro** y complete la dirección del empleado, que pasa a ser obligatoria.
5. Guarde los cambios.

A partir de ese momento, los fichajes del empleado no incluirán la validación de geocerca. En su ficha, la situación aparece como **Trabaja fuera del centro**; si la opción está desactivada, como **Ficha en el centro**.

> **Consejo:** si lo que necesita es comprobar que el empleado está en el sitio de un encargo concreto —el domicilio de un cliente, por ejemplo—, no desactive la geocerca: dele a la tarea su propio lugar de trabajo. Ver [Lugar de trabajo propio](../06-tareas/40-crear-una-tarea.md#lugar-de-trabajo-propio).

---

## Qué cambia cuando está activo

### Geolocalización desactivada

El sistema omite por completo la validación de radio de fichaje. El empleado puede registrar su entrada y salida desde cualquier ubicación sin que el sistema genere errores de tipo `checklog/out_of_radius`.

### Zona horaria del empleado

Cuando el trabajo fuera del centro está activo, el sistema utiliza la zona horaria del empleado para las validaciones de horario, en lugar de la zona horaria de la sucursal. Esto es especialmente relevante para equipos distribuidos en diferentes países o regiones.

Si la zona horaria del empleado no está configurada, el sistema utiliza por defecto la zona horaria de la entidad.

### Autenticación sin cambios

Trabajar fuera del centro no modifica las exigencias de autenticación. Si el empleado tiene 2FA activado, debe seguir fichando desde un dispositivo de confianza. Si tiene biometría requerida, debe continuar verificando su identidad biométrica antes de cada fichaje.

---

## Casos de uso habituales

**Desplazamientos y trabajo en campo:** Empleados que trabajan en instalaciones de clientes o en movimiento. Si la geocerca no es aplicable a su actividad, trabajar fuera del centro evita fichajes fallidos innecesarios.

**Equipos distribuidos geográficamente:** Empresas con empleados en distintas provincias o países que no están asignados a una sucursal física concreta. La opción permite centralizar el control de asistencia sin crear sucursales virtuales para cada ubicación.

**Teletrabajo completo:** El empleado trabaja íntegramente desde su domicilio. Se activa **Trabajo fuera del centro** de forma permanente y se configura correctamente su zona horaria.

**Teletrabajo parcial:** El empleado alterna entre oficina y domicilio según el día. El responsable puede activar o desactivar la opción según el calendario acordado, o mantenerla siempre activa si el empleado ficha correctamente en ambos entornos.

---

## Cómo se refleja en los informes

Los fichajes realizados fuera del centro quedan identificados en el sistema como tales. Desde el backoffice, el responsable puede filtrar los informes de asistencia por tipo de fichaje para obtener una visión separada de las jornadas en el centro y las realizadas fuera.

Esta distinción es útil para el seguimiento de acuerdos de teletrabajo, para el cumplimiento de los límites de días de trabajo a distancia establecidos en convenios o acuerdos internos, y para análisis de productividad por modalidad de trabajo.

---

> **Aviso de configuración:** Activar el trabajo fuera del centro sin configurar correctamente la zona horaria del empleado puede generar discrepancias en el cálculo de horas si el empleado se encuentra en una zona horaria diferente a la de la sucursal. Revise siempre la zona horaria del empleado antes de activar este modo.

---

## Roles con acceso a esta funcionalidad

La activación del trabajo fuera del centro requiere rol **manager** u **owner**. El empleado no puede activar ni desactivar este modo por su cuenta.

---

## Artículos relacionados

- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)
- [Geocercas y radio de fichaje](16-geocercas-radio-de-fichaje.md)
- [Check-in y check-out desde la app](14-checkin-checkout-desde-app.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)

# Fichaje en remoto

CheckBiz360 contempla escenarios de trabajo fuera de las instalaciones físicas de la empresa. El modo de trabajo remoto permite que los empleados registren su asistencia sin necesidad de estar dentro de la geocerca de la sucursal, manteniendo al mismo tiempo las validaciones de autenticación y de horario efectivo.

---

## Qué es el modo de trabajo remoto

El trabajo remoto en CheckBiz360 es una configuración individual por empleado que deshabilita la validación de geolocalización durante el fichaje. Cuando este modo está activo, el sistema no comprueba si el dispositivo se encuentra dentro del radio de la sucursal. El resto de validaciones (horario, dispositivo de confianza y biometría si aplica) siguen funcionando con normalidad.

Este modo está pensado para empleados que realizan su trabajo de forma habitual o puntual fuera de las instalaciones: teletrabajadores, equipos distribuidos geográficamente, o empleados con teletrabajo parcial que alternan entre la oficina y su domicilio.

---

## Cómo activar el trabajo remoto para un empleado

La activación del trabajo remoto es una operación que realizan los usuarios con rol **manager** u **owner** desde el panel de configuración del empleado en el backoffice.

1. Acceda al backoffice de CheckBiz360.
2. Navegue a la sección **Empleados** y seleccione el empleado correspondiente.
3. Abra la pestaña de configuración de asistencia o datos laborales.
4. Active el campo **Trabajo remoto** ("trabajo en remoto").
5. Guarde los cambios.

A partir de ese momento, los fichajes del empleado no incluirán la validación de geocerca.

---

## Qué cambia cuando el trabajo remoto está activo

### Geolocalización desactivada

El sistema omite por completo la validación de radio de fichaje. El empleado puede registrar su entrada y salida desde cualquier ubicación sin que el sistema genere errores de tipo `checklog/out_of_radius`.

### Zona horaria del empleado

Cuando el trabajo remoto está activo, el sistema utiliza la zona horaria del empleado para las validaciones de horario, en lugar de la zona horaria de la sucursal. Esto es especialmente relevante para equipos distribuidos en diferentes países o regiones.

Si la zona horaria del empleado no está configurada, el sistema utiliza por defecto la zona horaria de la entidad.

### Autenticación sin cambios

El trabajo remoto no modifica las exigencias de autenticación. Si el empleado tiene 2FA activado, debe seguir fichando desde un dispositivo de confianza. Si tiene biometría requerida, debe continuar verificando su identidad biométrica antes de cada fichaje.

---

## Casos de uso habituales

**Teletrabajo completo:** El empleado trabaja íntegramente desde su domicilio. Se activa "trabajo en remoto" de forma permanente y se configura correctamente su zona horaria.

**Teletrabajo parcial:** El empleado alterna entre oficina y domicilio según el día. En este caso, el responsable puede activar o desactivar el modo remoto según el calendario acordado, o bien mantenerlo siempre activo si el empleado ficha correctamente en ambos entornos.

**Equipos distribuidos geográficamente:** Empresas con empleados en distintas provincias o países que no están asignados a una sucursal física concreta. El modo remoto permite centralizar el control de asistencia sin necesidad de crear sucursales virtuales para cada ubicación.

**Desplazamientos y trabajo en campo:** Empleados que trabajan en instalaciones de clientes o en movimiento. Si la geocerca no es aplicable a su actividad, el modo remoto evita fichajes fallidos innecesarios.

---

## Cómo se refleja en los informes

Los fichajes realizados en modo remoto quedan identificados en el sistema como registros de trabajo remoto. Desde el backoffice, el responsable puede filtrar los informes de asistencia por tipo de fichaje para obtener una visión separada de las jornadas presenciales y las realizadas en remoto.

Esta distinción es útil para el seguimiento de acuerdos de teletrabajo, para el cumplimiento de los límites legales de días de trabajo remoto establecidos en convenios o acuerdos internos, y para análisis de productividad por modalidad de trabajo.

---

> **Aviso de configuración:** Activar el trabajo remoto sin configurar correctamente la zona horaria del empleado puede generar discrepancias en el cálculo de horas si el empleado se encuentra en una zona horaria diferente a la de la sucursal. Revise siempre la zona horaria del empleado antes de activar este modo.

---

## Roles con acceso a esta funcionalidad

La activación del modo de trabajo remoto requiere rol **manager** u **owner**. El empleado no puede activar ni desactivar este modo por su cuenta.

---

## Artículos relacionados

- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)
- [Geocercas y radio de fichaje](16-geocercas-radio-de-fichaje.md)
- [Check-in y check-out desde la app](14-checkin-checkout-desde-app.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)

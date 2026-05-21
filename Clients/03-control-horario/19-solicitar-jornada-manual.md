# Solicitar jornada manual

Existen situaciones en las que un empleado no puede registrar su asistencia a través de la app en el momento habitual: un fallo puntual del dispositivo, una emergencia, la ausencia de cobertura o cualquier otra circunstancia justificada. En estos casos, un manager o supervisor puede crear un registro de asistencia de forma manual para el empleado afectado. Este artículo explica cómo funciona este proceso y qué ocurre después de que se crea la solicitud.

---

## Qué es una solicitud de jornada manual

Una jornada manual es un registro de asistencia creado por un responsable en nombre de un empleado, con carácter retroactivo o diferido. A diferencia del fichaje ordinario, no requiere que el empleado esté presente con su dispositivo en el momento del registro.

El sistema distingue dos modos de creación de jornada manual según el contexto en el que se encuentre la jornada del empleado:

---

## Modo A — Jornada completa

Se utiliza cuando el empleado no ha registrado ningún evento durante la jornada: ni entrada ni salida.

En este modo, el responsable crea simultáneamente un **checkin** y un **checkout** para una fecha específica. Si el responsable no especifica las horas concretas, el sistema las rellena automáticamente utilizando las horas del turno del calendario efectivo asignado al empleado para ese día.

Este modo es adecuado para situaciones como:

- El empleado trabajó pero olvidó o no pudo fichar en ningún momento.
- Se registra una asistencia correspondiente a un día anterior.
- El empleado estuvo presente pero su dispositivo no funcionó en toda la jornada.

---

## Modo B — Solo checkout

Se utiliza cuando el empleado ya tiene un **checkin válido abierto**: entró y fue registrado correctamente, pero no fichó la salida.

En este modo, el responsable crea únicamente el **checkout** correspondiente para cerrar la jornada. No se modifica el checkin existente.

Este modo es el adecuado para situaciones como:

- El empleado olvidó fichar la salida al final del turno.
- El empleado no pudo registrar el checkout por un problema técnico al final de la jornada.
- La jornada aparece en estado `incomplete_workday` y debe cerrarse.

---

## Cómo crear una jornada manual

1. Acceda al backoffice con rol **manager** u **owner**.
2. Navegue a la sección **Asistencia** o al perfil del empleado.
3. Seleccione la opción **Nueva jornada manual** o **Solicitar jornada manual**.
4. Elija el empleado, la sucursal y la fecha de la jornada.
5. Seleccione el modo correspondiente (jornada completa o solo checkout).
6. Introduzca las horas si desea especificarlas manualmente, o deje que el sistema las complete según el turno.
7. Indique el motivo de la solicitud. Este campo es obligatorio y quedará registrado en el historial de auditoría.
8. Confirme la solicitud.

---

## Qué ocurre después de crear la solicitud

Una vez creada la jornada manual, el sistema realiza las siguientes acciones de forma automática:

### Estado inicial: pendiente de validación

La jornada manual queda en estado `pending-employee-validation`. Esto significa que el registro existe en el sistema pero **no computa como horas trabajadas hasta que el empleado la acepte**. Este mecanismo protege al empleado frente a modificaciones no autorizadas de su registro de asistencia.

### Notificación push al empleado

El empleado recibe una notificación push en su dispositivo informándole de que se ha creado una jornada manual a su nombre. La notificación le invita a revisar y validar o rechazar el registro.

### Validación o rechazo por el empleado

El empleado accede a la pantalla de notificaciones de la app y revisa los detalles de la jornada propuesta: fecha, horas, sucursal y motivo indicado por el responsable.

- Si el empleado **acepta**, la jornada pasa a estado `valid` y comienza a computar como horas trabajadas.
- Si el empleado **rechaza**, la jornada queda marcada como `failed` con el motivo del rechazo.

---

## Trazabilidad de la jornada manual

Cada solicitud de jornada manual queda registrada en el historial de cambios con la siguiente información:

- Identificador único de la entrada.
- Fecha y hora en que se realizó la solicitud.
- Acción realizada (`manual_request_created` o `manual_checkout_created` según el modo).
- UID del usuario responsable que creó la solicitud.
- Datos del estado anterior y del nuevo estado de la jornada.

Este registro es inmutable. No puede ser modificado ni eliminado, lo que garantiza la integridad del historial frente a inspecciones laborales o auditorías internas.

---

> **Aviso:** El campo de motivo es obligatorio y queda vinculado permanentemente al registro. Indique siempre una descripción clara y veraz de la razón que justifica la jornada manual. Este dato puede ser requerido en caso de inspección de trabajo.

---

## Roles con acceso a esta funcionalidad

La creación de jornadas manuales está restringida a usuarios con rol **manager** u **owner**. Los empleados con rol **empleado** solo pueden validar o rechazar las jornadas manuales que les sean asignadas.

---

## Artículos relacionados

- [Revisión y validación de fichajes](20-revision-y-validacion-de-fichajes.md)
- [Trazabilidad e historial de cambios](21-trazabilidad-historial-de-cambios.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)
- [Check-in y check-out desde la app](14-checkin-checkout-desde-app.md)

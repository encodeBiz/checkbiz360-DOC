# Códigos de error completos

Este artículo es la referencia técnica de todos los códigos de error que puede generar CheckBiz360. Cuando la app móvil o el backoffice muestran un código de error, puede consultarlo aquí para conocer su causa más habitual y la acción correctiva recomendada. Los códigos están organizados por módulo del sistema.

---

## Módulo de control horario (checklog)

Este módulo gestiona los registros de fichaje. Los errores de este módulo son los más frecuentes en el uso cotidiano de la app.

### `checklog/out_of_radius`

| Campo | Detalle |
|---|---|
| Causa más habitual | El empleado está intentando fichar desde una ubicación fuera del radio de geocerca configurado para la sucursal |
| Quién lo ve | Empleado en la app |
| Acción correctiva | Verificar que el empleado está físicamente en el lugar de trabajo y que el GPS de su dispositivo tiene buena precisión. Si el problema es recurrente, revisar las coordenadas y el radio de la sucursal en el backoffice |

### `checklog/out_of_schedule`

| Campo | Detalle |
|---|---|
| Causa más habitual | El empleado está intentando fichar fuera del horario de turno asignado. También se genera cuando se intenta hacer checkin después de la hora de fin del turno |
| Quién lo ve | Empleado en la app |
| Acción correctiva | Verificar el horario efectivo de la sucursal y el turno asignado al empleado. Comprobar la zona horaria configurada en la sucursal. Si el empleado está dentro de su turno y el error persiste, revisar la configuración de zona horaria |

### `checklog/day_disabled`

| Campo | Detalle |
|---|---|
| Causa más habitual | El empleado intenta fichar en un día que está marcado como festivo o no laborable en el calendario efectivo de la sucursal |
| Quién lo ve | Empleado en la app |
| Acción correctiva | Revisar el calendario efectivo de la sucursal en el backoffice. Si el día debería ser laborable, corregir la configuración del calendario |

### `checklog/overlap_detected`

| Campo | Detalle |
|---|---|
| Causa más habitual | El sistema ha detectado un fichaje que solapa con un registro ya existente para el mismo empleado en ese intervalo horario |
| Quién lo ve | Empleado en la app; el manager puede verlo en el detalle del registro |
| Acción correctiva | Revisar el historial de fichajes del empleado en el backoffice. Si hay un registro duplicado o incorrecto, eliminarlo mediante una jornada manual y registrar el fichaje correcto |

### `checklog/internal_error`

| Campo | Detalle |
|---|---|
| Causa más habitual | Error inesperado del servidor al procesar el fichaje. Puede deberse a un problema temporal de infraestructura |
| Quién lo ve | Empleado en la app |
| Acción correctiva | Esperar unos minutos y volver a intentar el fichaje. Si el error persiste durante más de 30 minutos, abrir una incidencia con la hora exacta del fallo y el ID del empleado |

### `checklog/bad_request`

| Campo | Detalle |
|---|---|
| Causa más habitual | Los datos enviados en la solicitud de fichaje son incorrectos o incompletos. Puede ocurrir si la app está desactualizada o si hay un problema de sincronización de datos |
| Quién lo ve | Empleado en la app |
| Acción correctiva | Actualizar la app a la última versión disponible. Si el problema persiste tras la actualización, reinstalar la app y volver a iniciar sesión |

---

## Módulo de autenticación (auth)

Este módulo gestiona el acceso de los usuarios a la plataforma.

### `auth/untrusted_device`

| Campo | Detalle |
|---|---|
| Causa más habitual | El empleado está intentando iniciar sesión o fichar desde un dispositivo que no está registrado como de confianza para su cuenta |
| Quién lo ve | Empleado en la app |
| Acción correctiva | El Owner o Manager debe acceder al perfil del empleado en el backoffice, sección "Dispositivos de confianza", y autorizar el nuevo dispositivo |

### `auth/unauthorized`

| Campo | Detalle |
|---|---|
| Causa más habitual | El token de sesión del usuario ha caducado o es inválido. También puede ocurrir si la cuenta ha sido desactivada mientras el usuario tenía sesión abierta |
| Quién lo ve | Empleado en la app o Manager en el backoffice |
| Acción correctiva | Cerrar sesión completamente y volver a iniciar sesión con las credenciales correctas. Si la cuenta ha sido desactivada, contactar con el Owner de la entidad |

---

## Módulo de empleados (employee)

### `employee/invalid_payload`

| Campo | Detalle |
|---|---|
| Causa más habitual | Se ha enviado una solicitud de creación o actualización de un empleado con datos incompletos o en formato incorrecto |
| Quién lo ve | Manager o Owner en el backoffice |
| Acción correctiva | Revisar todos los campos obligatorios del formulario del empleado. Asegurarse de que el correo electrónico tiene el formato correcto y que no hay campos en blanco donde se requiere un valor |

### `employee/not_found`

| Campo | Detalle |
|---|---|
| Causa más habitual | Se ha intentado realizar una operación sobre un empleado cuyo ID no existe en la entidad |
| Quién lo ve | Manager o Owner en el backoffice |
| Acción correctiva | Verificar que el empleado existe en la lista de empleados de la entidad. Si se ha eliminado por error, contactar con soporte para explorar opciones de recuperación |

### `employee/not_resposibility`

| Campo | Detalle |
|---|---|
| Causa más habitual | El empleado que está intentando realizar la acción no tiene las responsabilidades necesarias asignadas para completarla |
| Quién lo ve | Empleado en la app o Manager en el backoffice |
| Acción correctiva | Revisar las responsabilidades configuradas en el perfil del empleado. Si faltan responsabilidades necesarias para su rol, añadirlas desde el backoffice |

### `employee/branchId_required`

| Campo | Detalle |
|---|---|
| Causa más habitual | Se ha intentado crear o actualizar un empleado sin asignarle una sucursal, campo que es obligatorio |
| Quién lo ve | Manager o Owner en el backoffice |
| Acción correctiva | Asegurarse de que el empleado tiene al menos una sucursal asignada antes de guardar el perfil |

---

## Módulo de sucursales (branch)

### `branch/not_found`

| Campo | Detalle |
|---|---|
| Causa más habitual | Se ha referenciado una sucursal con un ID que no existe en la entidad, o la sucursal ha sido eliminada |
| Quién lo ve | Manager u Owner en el backoffice al gestionar empleados, calendarios o configuraciones |
| Acción correctiva | Verificar que la sucursal existe en la lista de sucursales de la entidad. Si el error aparece en el perfil de un empleado, reasignar la sucursal desde el backoffice |

### `branch/inactive`

| Campo | Detalle |
|---|---|
| Causa más habitual | Se ha intentado realizar una operación (como un fichaje) en una sucursal que está marcada como inactiva en el sistema |
| Quién lo ve | Empleado en la app o Manager en el backoffice |
| Acción correctiva | El Owner debe revisar el estado de la sucursal en el backoffice y reactivarla si corresponde |

---

## Módulo de calendario (calendar)

### `calendar/not_resolved`

| Campo | Detalle |
|---|---|
| Causa más habitual | El sistema no ha podido determinar el calendario efectivo aplicable para el empleado en la fecha en que intenta fichar. Puede ocurrir si no hay un calendario asignado a la sucursal o si hay un conflicto en la configuración |
| Quién lo ve | Empleado en la app |
| Acción correctiva | Acceder al backoffice y verificar que la sucursal del empleado tiene un calendario efectivo activo y correctamente configurado para la fecha en cuestión. Si no hay calendario asignado, crear uno y asignarlo a la sucursal |

---

## Módulo de suscripción (subscription)

### `subscription/limit_off`

| Campo | Detalle |
|---|---|
| Causa más habitual | Se ha alcanzado el límite de empleados activos, sucursales o cualquier otro recurso incluido en el plan de suscripción contratado |
| Quién lo ve | Owner o Manager en el backoffice al intentar añadir nuevos empleados o sucursales |
| Acción correctiva | Revisar los límites del plan actual en **Configuración > Suscripción**. Si es necesario ampliar la capacidad, actualizar el plan desde esa misma sección o contactar con soporte en hola@encodebiz.com |

---

> **Aviso:** Si encuentra un código de error que no aparece en esta tabla, o si el mismo código reaparece de forma sistemática después de aplicar las acciones correctivas indicadas, abra una incidencia en el backoffice incluyendo el código exacto, la hora del fallo y el ID del empleado afectado.

---

## Nota de rol

Este artículo es de consulta para **Owner** y **Manager**, que son los responsables de diagnosticar y resolver errores operativos. Los empleados con rol Worker que vean un código de error en la app deben comunicárselo a su Manager con el código exacto que aparece en pantalla.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Problemas frecuentes y soluciones](../13-soporte-e-incidencias/88-problemas-frecuentes-y-soluciones.md) | Guía práctica de diagnóstico para las situaciones más habituales |
| [Crear una incidencia](../13-soporte-e-incidencias/85-crear-una-incidencia.md) | Cómo abrir un caso de soporte cuando el error no tiene solución directa |
| [Glosario](./89-glosario.md) | Definición de los términos técnicos utilizados en la plataforma |
| [Contactar con soporte técnico](../13-soporte-e-incidencias/87-contactar-con-soporte-tecnico.md) | Canales y tiempos de respuesta del equipo de soporte |

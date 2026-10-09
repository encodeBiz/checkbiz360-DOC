# Estados y códigos de error del fichaje

CheckBiz360 asigna a cada registro de asistencia un estado que refleja su situación en el ciclo de vida de la jornada. Cuando un fichaje no puede procesarse correctamente, el sistema genera además un código de error que identifica la causa con precisión. Este artículo describe todos los estados posibles y los códigos de error disponibles, junto con las acciones recomendadas para resolverlos.

---

## Estados de fichaje

Los estados indican en qué punto del proceso se encuentra un registro de asistencia. Son asignados automáticamente por el sistema y pueden cambiar a lo largo del tiempo, por ejemplo cuando un empleado valida una jornada manual o cuando un responsable corrige una incidencia.

| Estado | Significado |
|---|---|
| `valid` | Fichaje correcto. Todas las validaciones superadas. El registro computa como tiempo trabajado. |
| `failed` | Fichaje rechazado. Una o más validaciones han fallado. El registro queda almacenado para auditoría pero no computa horas. Incluye código de error. |
| `pending-employee-validation` | Registro creado por un responsable o modificado. Esperando la confirmación del empleado. No computa horas hasta ser aceptado. |
| `incomplete_workday` | Jornada sin cerrar. Existe un checkin válido sin checkout correspondiente. Requiere resolución manual o un checkout posterior. |

---

### Estado `valid`

Es el estado objetivo de todo fichaje. Indica que el registro ha superado las validaciones de geolocalización, horario y autenticación, y que el empleado lo ha confirmado (si era necesario). Los cálculos de horas trabajadas se realizan exclusivamente sobre registros en estado `valid`.

### Estado `failed`

Un fichaje puede quedar en estado `failed` por múltiples razones: el empleado estaba fuera del radio, el fichaje se realizó fuera de turno, el dispositivo no estaba autorizado o el empleado rechazó una jornada manual. En todos los casos, el registro se conserva íntegramente para auditoría.

### Estado `pending-employee-validation`

Este estado es temporal. Aparece cuando se crea una jornada manual o cuando un responsable modifica un fichaje y el sistema requiere confirmación del empleado. Mientras el registro permanece en este estado, no altera el cómputo de horas.

### Estado `incomplete_workday`

Indica que el empleado registró su entrada pero no su salida. La jornada queda abierta. Este estado puede resolverse registrando el checkout correspondiente (manual o desde la app) o mediante la creación de un checkout manual por parte del responsable.

---

## Códigos de error

Cuando un fichaje queda en estado `failed`, el sistema asocia un código de error que identifica la causa exacta del rechazo. Estos códigos permiten al responsable diagnosticar y resolver la incidencia de forma eficiente.

| Código | Causa | Acción recomendada |
|---|---|---|
| `checklog/out_of_schedule` | El fichaje se realizó fuera del turno activo del empleado. | Revisar el horario asignado al empleado. Si la presencia era correcta, solicitar una jornada manual. |
| `checklog/out_of_radius` | El dispositivo se encontraba fuera del radio de fichaje de la sucursal en el momento del registro. | Revisar las coordenadas GPS de la sucursal y el valor del radio configurado. Si el radio no cubre el área de trabajo real, ampliarlo. |
| `checklog/day_disabled` | El día en que se intentó fichar está desactivado en el calendario de la sucursal o del empleado, es festivo o es un día libre del empleado. | Revisar la configuración del calendario. Si el día debe estar habilitado, activarlo en el calendario efectivo correspondiente. Un festivo de la entidad o de la sucursal no se puede anular para un solo empleado. Si el empleado trabajó, registrar la jornada manual. |
| `checklog/absence` | El empleado tiene registrada una ausencia que cubre ese día. | Si la ausencia es correcta, no hay nada que hacer. Si no lo es, retirarla de su calendario y volver a fichar. |
| `checklog/different_branches` | Se intentó iniciar un descanso o fichar la salida en una sucursal distinta de la de la entrada. Una jornada no se reparte entre centros. | Fichar el descanso o la salida en la misma sucursal de la entrada. Si el empleado cambió de centro, cerrar la jornada en el primero y abrir otra en el segundo. |
| `checklog_update/future_not_allowed` | Se propuso una corrección con fecha u hora futura. | Indicar una hora que ya haya pasado. |
| `auth/untrusted_device` | El dispositivo desde el que se intentó fichar no está registrado como dispositivo de confianza. El empleado tiene activada la autenticación de doble factor. | Registrar el dispositivo actual como dispositivo de confianza a través del proceso de 2FA. |
| `employee/not_found` | El identificador del empleado no corresponde a ningún registro activo en el sistema. | Verificar que el empleado está activo en la plataforma y asignado correctamente a la sucursal. |
| `checklog/overlap_detected` | Ya existe un fichaje para el rango horario en el que se intenta crear el nuevo registro. Dos fichajes del mismo tipo no pueden solaparse. | Revisar los fichajes existentes del empleado para esa fecha y resolver el solapamiento antes de crear un nuevo registro. |

---

## Cómo consultar el estado y el código de error de un fichaje

Desde el backoffice, el responsable puede acceder al detalle de cualquier fichaje y ver:

- El estado actual del registro.
- El código de error si el estado es `failed`.
- Los datos técnicos del intento: coordenadas, distancia al radio, turno activo en el momento del fichaje, dispositivo utilizado.
- El historial completo de cambios.

Los empleados pueden ver el estado de sus fichajes desde la sección de historial de asistencia en la app. En caso de fichajes fallidos, la app muestra una descripción del motivo en lenguaje comprensible. Desde la versión 1.3.2, la app traduce también los códigos de día no laborable, calendario sin resolver, sucursal sin ubicación, solapamiento, solicitud duplicada y cierre de jornada, en lugar de mostrar el código técnico; y cuando el día no es laborable, explica que el empleado puede pedir una jornada manual si trabajó.

---

> **Aviso para responsables:** Un fichaje fallido no significa necesariamente que el empleado actuó de forma incorrecta. En muchos casos, el error es de configuración: un radio demasiado pequeño, un turno mal asignado o un dispositivo no registrado. Antes de tomar cualquier acción disciplinaria, revise siempre los detalles técnicos del error y contraste con el empleado.

---

## Roles con acceso a esta funcionalidad

Todos los usuarios con rol **empleado** pueden ver el estado de sus propios fichajes desde la app. Los usuarios con rol **manager** u **owner** tienen acceso completo a los estados, códigos de error y datos técnicos de todos los fichajes de su entidad desde el backoffice.

---

## Artículos relacionados

- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)
- [Geocercas y radio de fichaje](16-geocercas-radio-de-fichaje.md)
- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
- [Trazabilidad e historial de cambios](21-trazabilidad-historial-de-cambios.md)

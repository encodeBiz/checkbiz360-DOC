# Revisión y validación de fichajes

Algunos registros de asistencia en CheckBiz360 no se consolidan de forma automática, sino que requieren una confirmación explícita por parte del empleado antes de considerarse válidos. Este mecanismo garantiza que ninguna modificación o asignación de jornada se produce sin el conocimiento y la aceptación de la persona afectada. Este artículo explica cuándo se activa este proceso, cómo lo gestiona el empleado y qué opciones tienen los responsables.

---

## El estado "pendiente de validación del empleado"

El estado `pending-employee-validation` indica que un fichaje o jornada existe en el sistema pero está a la espera de que el empleado lo confirme. Mientras permanece en este estado, el registro **no computa como tiempo trabajado**.

Este estado es visible tanto para el empleado (a través de la app) como para el responsable (desde el backoffice).

---

## Cuándo se genera un fichaje pendiente de validación

Existen dos situaciones principales en las que un registro entra en estado `pending-employee-validation`:

**Solicitud de jornada manual:** Cuando un manager o supervisor crea una jornada en nombre del empleado (Modo A o Modo B), el sistema asigna automáticamente este estado hasta que el empleado responda. Consulte el artículo [Solicitar jornada manual](19-solicitar-jornada-manual.md) para más detalle.

**Corrección de gestor:** Cuando un responsable modifica un fichaje existente del empleado (por ejemplo, ajusta la hora de entrada o salida), el sistema puede requerir que el empleado valide el cambio antes de aplicarlo de forma definitiva, según la configuración de la entidad.

---

## Cómo el empleado valida o rechaza un fichaje pendiente

El empleado recibe una notificación push en su dispositivo móvil cuando hay un fichaje pendiente de validación. Para gestionarlo:

1. Pulse la notificación o abra la app de CheckBiz360.
2. Navegue a la sección **Notificaciones** y seleccione la notificación de tipo actualización de fichaje.
3. Revise los detalles del registro: fecha, hora de entrada, hora de salida, sucursal y motivo indicado por el responsable.
4. Seleccione **Aceptar** o **Rechazar** según corresponda.

La pantalla de revisión está disponible en la ruta `/notifications/checklog-update/:id`, donde `:id` corresponde al identificador único del registro de asistencia.

---

## Qué ocurre si el empleado acepta

El fichaje pasa a estado `valid`. A partir de ese momento, el registro computa como tiempo trabajado y queda incorporado al cálculo de horas de la jornada. El sistema registra la acción de validación en el historial de auditoría con la fecha, hora y el identificador del empleado que la realizó.

---

## Qué ocurre si el empleado rechaza

El fichaje queda marcado con estado `failed` y se almacena el motivo del rechazo. El registro permanece en el sistema para auditoría, pero no computa como horas trabajadas. El responsable recibe una notificación del rechazo y puede iniciar una nueva solicitud corregida o resolver la incidencia de forma manual.

---

## Qué ocurre si el empleado no responde

Si el empleado no valida ni rechaza el fichaje, este permanece indefinidamente en estado `pending-employee-validation`. No existe un plazo de expiración automática por defecto.

En estos casos, el fichaje aparece como pendiente en el backoffice y debe resolverse manualmente. Los responsables con rol **manager** u **owner** pueden:

- Aprobar el fichaje directamente desde el backoffice, sin necesidad de la validación del empleado.
- Rechazarlo y cerrar la incidencia con un motivo registrado.
- Ponerse en contacto con el empleado para que resuelva la validación pendiente desde la app.

---

## Vista de pendientes en el backoffice

El backoffice de CheckBiz360 incluye una vista específica para gestionar los fichajes pendientes de validación. Desde esta pantalla, el responsable puede:

- Ver todos los registros en estado `pending-employee-validation` de su sucursal o entidad.
- Filtrar por empleado, fecha o sucursal.
- Acceder al detalle de cada registro para revisar el historial de cambios.
- Aprobar o rechazar registros de forma individual o masiva.

Esta vista está pensada para que el responsable tenga una visión centralizada de todas las incidencias pendientes y pueda resolverlas sin necesidad de ir registro por registro desde el historial de cada empleado.

---

> **Aviso de cumplimiento:** La validación por parte del empleado es un mecanismo de protección laboral. La aprobación unilateral por parte del responsable sin haber contactado al empleado debe documentarse adecuadamente y usarse solo en casos excepcionales. En entornos sujetos a auditorías laborales, se recomienda conservar el motivo de la aprobación unilateral en el campo de observaciones.

---

## Roles con acceso a esta funcionalidad

Los usuarios con rol **empleado** pueden validar o rechazar fichajes pendientes desde la app. Los usuarios con rol **manager** u **owner** pueden resolver pendientes desde el backoffice, incluyendo la aprobación sin validación del empleado.

---

## Artículos relacionados

- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
- [Trazabilidad e historial de cambios](21-trazabilidad-historial-de-cambios.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)
- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)

# Alertas para responsables

Las alertas para responsables son notificaciones de carácter operativo que el sistema envía a los roles Manager y Supervisor cuando se producen eventos que requieren atención o acción por parte del equipo de gestión. A diferencia de las notificaciones dirigidas a los empleados, estas alertas están diseñadas para detectar irregularidades, garantizar el cumplimiento de los procesos y permitir una respuesta rápida ante situaciones que podrían afectar a la operación. Este artículo describe los tipos de alerta disponibles, cómo configurarlos y cómo ajustar los umbrales de activación.

## Tipos de alerta para responsables

### Empleado que no ha fichado

Esta alerta se envía al Manager y al Supervisor de la sucursal cuando un empleado con turno activo no ha registrado la entrada pasada una hora determinada. Es la alerta más utilizada en operaciones con turnos definidos, ya que permite al responsable saber de inmediato quién falta antes de que la ausencia afecte a la operación.

La alerta incluye:
- Nombre del empleado.
- Sucursal y turno al que debía incorporarse.
- Hora de inicio del turno y tiempo transcurrido desde entonces.

### Jornada manual pendiente de aprobación

Cuando un empleado solicita el registro manual de una jornada (por no haber podido fichar en el momento correspondiente), el sistema envía una alerta al responsable para que revise y apruebe o rechace la solicitud. La alerta incluye el motivo indicado por el empleado y un enlace directo al registro para gestionar la solicitud.

> **Aviso:** Las solicitudes de jornada manual no aprobadas en un plazo de 48 horas generan una alerta adicional de recordatorio. Si el periodo de nómina cierra con solicitudes pendientes, el sistema lo indicará como una incidencia de cumplimiento.

### Fichaje marcado como sospechoso

El motor de análisis de CheckBiz360 evalúa cada fichaje en contexto y puede marcarlo con un indicador de anomalía cuando detecta características irregulares, como:

- Cambio abrupto de ubicación GPS entre fichajes consecutivos.
- Coordenadas GPS inconsistentes con el movimiento físico posible en el tiempo transcurrido.
- Patrones de fichaje que coinciden con comportamientos conocidos de evasión del control.
- Fichaje desde un dispositivo diferente al habitual sin autorización previa.

Cuando se genera esta alerta, el responsable recibe la notificación con el detalle del fichaje sospechoso y puede decidir validarlo, modificarlo o escalarlo para investigación.

### Empleado fuera de geocerca de forma repetida

Si un empleado registra fichajes fuera del radio definido para su sucursal de forma recurrente (el umbral por defecto es tres veces en una semana), el sistema genera una alerta consolidada dirigida al Manager. Esta alerta es diferente a la notificación individual de "fichaje fuera de geocerca": no se genera en cada ocurrencia individual, sino cuando el patrón se vuelve sistemático.

## Cómo configurar qué alertas recibe cada responsable

El Owner y el Manager pueden ajustar la distribución de alertas desde el backoffice:

1. Acceda a **Organización** > **Sucursales** y abra la sucursal para la que desea configurar alertas.
2. Seleccione la pestaña **Responsables** o **Configuración de alertas**.
3. Verá la lista de Managers y Supervisores asignados a esa sucursal.
4. Pulse el icono de configuración junto al nombre del responsable para ajustar qué tipos de alerta recibe.
5. Active o desactive los tipos de alerta según las responsabilidades de ese responsable.
6. Pulse **Guardar**.

Esta configuración permite, por ejemplo, que el Supervisor reciba las alertas de fichaje y ausencia del día a día, mientras que el Manager recibe únicamente las alertas de fichajes sospechosos y jornadas manuales pendientes.

## Configurar el umbral de hora límite de entrada

La alerta de "empleado que no ha fichado" requiere definir una hora límite de entrada para cada turno. Si el turno comienza a las 08:00 y la hora límite está configurada en 30 minutos, la alerta se generará a las 08:30 si el empleado no ha fichado.

Para configurar este umbral:

1. Acceda a **Organización** > **Calendarios** y abra el calendario que contiene el turno que desea configurar.
2. Seleccione el turno específico y localice el campo **Tolerancia de alerta de entrada** (expresado en minutos).
3. Introduzca el número de minutos tras la hora de inicio del turno a partir del cual el sistema debe generar la alerta.
4. Guarde los cambios. El nuevo umbral se aplicará a partir del día siguiente.

> **Aviso:** Un umbral demasiado bajo (por ejemplo, 5 minutos) puede generar un volumen excesivo de alertas por retrasos menores y normales en el transporte o el acceso al centro. Se recomienda empezar con un umbral de entre 15 y 30 minutos y ajustarlo en función de la operativa real de la sucursal.

## Recepción de alertas: backoffice y notificación push

Los responsables reciben las alertas a través de dos canales simultáneos:

- **Centro de notificaciones del backoffice**: visible en el icono de campana de la barra superior. Las alertas no leídas se muestran con un indicador numérico y permanecen en el centro hasta que el responsable las revisa.
- **Notificación push en la app**: si el Manager o el Supervisor tiene la app CheckBiz360 instalada y ha iniciado sesión, las alertas también se reciben como notificaciones push en su dispositivo móvil.

Las alertas críticas (fichaje sospechoso, dispositivo no autorizado) disponen adicionalmente de un canal de respaldo por correo electrónico que garantiza su entrega aunque el responsable no tenga la app activa.

## Gestión de alertas recibidas

Desde el centro de notificaciones del backoffice, el responsable puede:

- **Marcar como revisada**: indica que la alerta ha sido vista y procesada.
- **Acceder al recurso**: navegar directamente al fichaje, la jornada o el empleado al que hace referencia la alerta.
- **Añadir comentario interno**: registrar una nota sobre la gestión realizada, visible para otros responsables de la misma sucursal.

Las alertas revisadas se archivan automáticamente y quedan disponibles en el historial de notificaciones.

---

> **Nota de rol:** Las alertas para responsables están disponibles para los roles **Manager** y **Supervisor**. El **Owner** recibe las alertas críticas de seguridad para toda la entidad. El rol **Worker** no tiene acceso a las alertas operativas.

## Artículos relacionados

- [Tipos de notificación](63-tipos-de-notificacion.md)
- [Configurar preferencias de notificación](65-configurar-preferencias-de-notificacion.md)
- [Historial de notificaciones](67-historico-de-notificaciones.md)
- [Vista global multi-sucursal](../08-sucursales-y-entidad/62-vista-global-multi-sucursal.md)

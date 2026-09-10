# Glosario de CheckBiz360

Este glosario recoge los términos operativos más relevantes de CheckBiz360, ordenados alfabéticamente. Cada definición incluye el nombre en español y una descripción de su significado en el contexto del sistema.

---

## A

### Acuse de recibo
Confirmación explícita de que un empleado ha accedido a un documento que lo requiere. Queda registrada con la fecha y la versión concreta del documento que se leyó, de modo que una versión posterior no hereda el acuse de la anterior. No es una firma electrónica: la firma con validez eIDAS está en el roadmap.

### Ajuste de horario
Concepto que **no aplica** en la versión actual: el fichaje guarda siempre la hora real y no se redondea. Lo que decide si el tiempo trabajado fuera de la franja oficial se computa es la modalidad de *jornada estricta o flexible* del calendario.

### Asistente de IA (Merlin)
Componente de inteligencia artificial que interpreta los datos operativos y los expone como un relato accionable en el panel operativo, en el detalle de sucursal y en el detalle de empleado. Narra y prioriza sobre las cifras que ya muestra la pantalla: no recalcula ni genera datos propios, de forma que su lectura no puede contradecir a los paneles.

---

## B

### Verificación biométrica requerida
Configuración que obliga a un empleado a autenticarse mediante huella dactilar o reconocimiento facial antes de completar un fichaje desde la app móvil. Cuando está activa, el sistema no acepta el fichaje si la biometría no se verifica correctamente en el dispositivo.

---

## C

### Calendario efectivo
Configuración que define los días laborables y festivos para una sucursal o para un empleado concreto. El calendario efectivo determina qué días el sistema espera fichajes y qué días se consideran libres o festivos. Se configura desde el backoffice en la sección de calendarios.

### Checkin / Checkout
Registro de la hora de entrada (checkin) y de salida (checkout) de un empleado en su jornada laboral. Son los eventos fundamentales del control horario. Un checkin sin checkout correspondiente genera una jornada incompleta. Véase también: Fichaje / Checklog.

### Cumplimiento temporal
Indicador que acompaña a cada tarea y refleja su situación frente a la fecha límite, con independencia de su estado. Sus valores son: sin iniciar, a tiempo, en riesgo, vencida, completada a tiempo y completada tarde. Una tarea vencida sigue estando en su estado de trabajo (por ejemplo, "en progreso"); el vencimiento se refleja en este indicador, no en el estado.

### Código de error
Identificador alfanumérico que el sistema devuelve cuando una operación no puede completarse. Los códigos de error siguen el formato `modulo/tipo_de_error` (por ejemplo, `checklog/out_of_radius`). Permiten identificar la causa exacta de un fallo sin necesidad de interpretar mensajes de texto. Véase el artículo [Códigos de error completos](./90-codigos-de-error-completos.md).

---

## D

### Dependencia
Indicador que mide cuánta parte de la operación de un centro recae en pocas personas. Se lee de forma directa —*media operación depende de 1 persona*, *depende de 2 personas*, *reparto saludable*— y se complementa con la vista de relevo por puesto.

### Dispositivo de confianza
Dispositivo móvil autorizado explícitamente por el Owner o el Manager para que un empleado concreto pueda realizar fichajes desde él. La plataforma puede configurarse para rechazar fichajes procedentes de dispositivos no registrados como de confianza.

---

## E

### Efecto del centro
Indicador que compara el rendimiento de cada persona **en un centro concreto** con su propio rendimiento global. El promedio de esas diferencias entre todos los que pasan por allí mide el efecto que el centro ejerce sobre las personas, ya descontado el talento individual. Responde a si el problema es la persona o el sitio.

### Empleado / Employee
Usuario de CheckBiz360 con rol Worker, Supervisor o Manager que forma parte de la plantilla de una entidad. En la plataforma, el término "employee" hace referencia al registro de datos de una persona en la organización, incluyendo su perfil, asignaciones, fichajes y documentos.

### Evidencia
Foto o vídeo que un empleado adjunta a una tarea para acreditar el trabajo realizado. Si la tarea tiene activada la exigencia de evidencia, el sistema no permite completarla sin al menos un archivo adjunto y devuelve el código `task/evidence_required`.

### Entidad / Entity
La unidad organizativa raíz de CheckBiz360. Corresponde a una empresa o cliente que ha contratado la plataforma. Cada entidad puede tener múltiples sucursales, empleados y configuraciones propias. El Owner es el responsable máximo de la entidad.

---

## F

### Fichaje / Checklog
Registro individual de una acción de control horario realizada por un empleado. Un checklog incluye: tipo de evento (checkin, checkout, restin, restout), coordenadas GPS, timestamp, dispositivo utilizado y estado de validación. Es la unidad mínima de datos del módulo de control horario.

---

## G

### Geocerca / Radio de fichaje
Perímetro geográfico circular definido alrededor de las coordenadas de una sucursal. Solo se aceptan fichajes realizados dentro de ese perímetro. El radio se mide en metros y se configura desde la ficha de cada sucursal en el backoffice.

---

## H

### Herencia de configuración
Mecanismo por el que los empleados o sucursales adoptan automáticamente la configuración definida en un nivel superior de la jerarquía (por ejemplo, de la entidad a la sucursal, o de la sucursal al empleado). Si un parámetro no está configurado explícitamente en el nivel inferior, el sistema utiliza el valor del nivel superior.

---

## I

### Índice de eficiencia operativa
Indicador que mide el equilibrio entre el coste real asumido y el coste esperado según el patrón histórico. La referencia es siempre el propio histórico, no una escala universal ni una comparación directa entre personas.

### Índice de fiabilidad
Indicador de la calidad del comportamiento observado, **separada del tiempo que se lleva midiendo**: quien lleva poco en la empresa no arrastra una fiabilidad baja por ello. Es uno de los tres índices principales del panel de Operación, junto al efecto del centro y la dependencia.

---

## J

### Jornada incompleta (`incomplete_workday`)
Jornada laboral en la que existe un checkin pero no el checkout correspondiente, o viceversa. El sistema la marca automáticamente como incompleta y la excluye del cálculo de horas trabajadas hasta que se completa mediante una jornada manual.

### Jornada estricta / flexible
Modalidad de cómputo del calendario. Con **jornada estricta** manda el horario oficial: lo trabajado antes o después no se contabiliza, y retrasos y salidas anticipadas se descuentan. Con **jornada flexible** manda el tiempo real: lo trabajado fuera de la franja se suma como extra. Existe la misma distinción para los descansos.

### Jornada manual
Corrección retroactiva de un fichaje realizada por un Owner o Manager desde el backoffice. Se utiliza cuando un empleado olvidó fichar, cuando el sistema no pudo registrar el evento por un fallo técnico puntual o cuando es necesario ajustar datos de asistencia históricos. Queda registrada con el nombre del usuario que la realizó y la fecha de la modificación.

---

## M

### Manager
Rol de usuario con capacidad para gestionar empleados, sucursales, documentos, informes e incidencias dentro de las sucursales que le han sido asignadas. El Manager actúa bajo la supervisión del Owner y no puede modificar la configuración global de la entidad.

### Merlin
Véase *Asistente de IA (Merlin)*.

### Módulo documental
Conjunto de funcionalidades de CheckBiz360 que permite subir, organizar y distribuir documentos laborales (contratos, nóminas, comunicados, políticas de empresa, protocolos y prevención de riesgos), con visibilidad por rol y acuse de recibo del empleado. Está incluido en la suscripción, sin depender del plan. La firma electrónica avanzada no forma parte de la versión actual: lo que existe hoy es el acuse de recibo.

---

## N

### Notificación push
Mensaje enviado directamente al dispositivo móvil de un empleado a través del sistema de notificaciones del sistema operativo (APNs en iOS, FCM en Android). CheckBiz360 utiliza notificaciones push para avisar de nuevas tareas, documentos pendientes de acuse de recibo, alertas de jornada y comunicados del sistema.

---

## O

### Owner
Rol con acceso completo a todas las funcionalidades de una entidad en CheckBiz360. El Owner puede gestionar empleados, sucursales, configuración global, facturación y todos los módulos disponibles en el plan contratado. Cada entidad tiene al menos un Owner.

---

## P

### Pausa (`restin` / `restout`)
Registro del inicio (`restin`) y fin (`restout`) de una pausa dentro de la jornada laboral. Las pausas se descontarán o no del tiempo trabajado según la configuración de la sucursal. Al igual que el checkin y checkout, las pausas requieren que el empleado esté dentro de la geocerca si así está configurado.

### Panel operativo
Pantalla del backoffice que consolida la actividad del periodo en tres vistas: la comparativa entre sucursales, el detalle por empleado y el análisis del periodo. Es el punto de entrada a la inteligencia operativa y donde aparece el relato del asistente de IA.

### Plan de suscripción
Modalidad de contratación de CheckBiz360. Hay dos: **Bronce**, 5 €/empleado al mes (tarifa 2026 de 2 € contratando hasta el 31 de diciembre de 2026 incluido), y **Empresarial**, con precio a medida, que añade soporte preferente e integraciones. Ambos dan acceso a todos los módulos de la plataforma. Véase [Planes, precios y funcionalidades](./91-planes-y-funcionalidades.md).

### Puntuación de promoción
Índice único que combinaría fiabilidad, eficiencia y valoraciones en una sola cifra comparable entre empleados. **No existe en la versión actual**: lo que sí hay es la *evaluación operativa del empleado*, un diagnóstico de su patrón que incluye la señal de candidato a promoción. Véase [Evaluación operativa del empleado](../07-inteligencia-operativa/53-puntuacion-de-promocion.md).

---

## R

### RDL 8/2019
Real Decreto-ley 8/2019, de 8 de marzo, que establece la obligación de registro horario para todos los trabajadores en España. CheckBiz360 está diseñado para cumplir con los requisitos de este decreto, proporcionando registros inmutables, con hora exacta y disponibles para inspección laboral.

### Registro de jornada
Conjunto de todos los eventos de fichaje (checkin, restin, restout, checkout) que componen una jornada laboral completa de un empleado. El registro de jornada es la unidad de análisis para el cálculo de horas, el cumplimiento normativo y la generación de informes.

### Responsabilidades (`responsibilities`)
Campo de configuración de un empleado que define las áreas de trabajo o funciones específicas que tiene asignadas dentro de la organización. Las responsabilidades pueden utilizarse para la asignación de tareas y como criterio de filtrado en informes.

### Rol
Nivel de acceso y permisos de un usuario dentro de CheckBiz360. Los roles disponibles son: Owner, Manager, Supervisor y Worker. Cada rol tiene un conjunto definido de acciones que puede realizar en el backoffice y en la app móvil.

---

## S

### Sucursal / Branch
Unidad organizativa dentro de una entidad que representa un centro de trabajo, una delegación o cualquier agrupación geográfica o funcional de empleados. Cada sucursal tiene sus propias coordenadas, radio de fichaje, horarios, calendario efectivo y configuración de control horario.

### Supervisor
Rol intermedio entre Manager y Worker. El Supervisor puede revisar los fichajes y tareas de los empleados de su equipo directo si el Manager le ha concedido esa capacidad, pero no tiene acceso a la configuración global de la sucursal ni a los informes de costes o anomalías.

---

## T

### Tarea
Unidad de trabajo asignada a uno o varios empleados de una sucursal, con fecha límite y, opcionalmente, fecha prevista de inicio. Recorre siete estados —borrador, asignada, en progreso, completada, validada, rechazada y cancelada— y lleva asociado un indicador de cumplimiento temporal independiente del estado.

### Token de validación
Código temporal generado por el sistema para verificar la identidad de un usuario en operaciones sensibles, como el primer inicio de sesión, el restablecimiento de contraseña o la autorización de un nuevo dispositivo. Los tokens de validación caducan pasado un tiempo determinado.

### Trabajo remoto
Configuración que permite a un empleado realizar fichajes desde una ubicación diferente a la geocerca de su sucursal. Cuando está activa, el sistema acepta fichajes fuera del radio habitual sin generar el error `checklog/out_of_radius`. Debe activarse explícitamente por el Owner o Manager.

### Turno
Franja horaria asignada a un empleado para una jornada concreta, que define su hora de inicio y fin de trabajo esperados. Los turnos se configuran en el backoffice y se asocian al calendario efectivo del empleado o la sucursal.

---

## W

### Worker
Rol de usuario base en CheckBiz360, correspondiente a un empleado operativo. Los Workers pueden fichar desde la app, consultar sus propios datos de asistencia, ver sus documentos y gestionar sus tareas. No tienen acceso al backoffice salvo que se les conceda un rol superior.

---

## Nota de rol

Este artículo es de consulta libre para todos los roles de la plataforma: Owner, Manager, Supervisor y Worker.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Códigos de error completos](./90-codigos-de-error-completos.md) | Referencia de todos los códigos de error del sistema |
| [Planes, precios y funcionalidades](./91-planes-y-funcionalidades.md) | Precio de cada plan, periodo de prueba y módulos incluidos |
| [Preguntas frecuentes](./92-preguntas-frecuentes.md) | Respuestas a las dudas más habituales sobre CheckBiz360 |
| [Control horario: conceptos básicos](../03-control-horario/13-como-funciona-el-fichaje.md) | Introducción al módulo de control horario |

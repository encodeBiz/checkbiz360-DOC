# Códigos de error completos

Este artículo es la referencia de los códigos de error que pueden aparecer en la app móvil o en el backoffice de CheckBiz360. Cuando el sistema muestra un mensaje de error, el código que lo acompaña permite identificar la causa exacta y la acción correctiva.

Los códigos siguen siempre el formato `módulo/motivo`. A continuación se agrupan por módulo.

> **Nota:** si en pantalla aparece un código que no figura en este artículo, significa que procede de un servicio que aún no tiene un mensaje traducido. Anote el código literal y ábralo como incidencia: es información suficiente para que soporte lo identifique.

---

## Fichaje y jornada (`checklog`)

Los errores más frecuentes en el uso diario. Salvo indicación contraria, los ve el **empleado en la app**.

| Código | Qué significa | Qué hacer |
|---|---|---|
| `checklog/out_of_radius` | El empleado no está dentro del radio de fichaje de la sucursal seleccionada | Comprobar que está físicamente en el centro de trabajo y que el GPS tiene buena precisión. Si se repite, revisar coordenadas y radio de la sucursal |
| `checklog/out_of_schedule` | El fichaje cae fuera del horario del turno asignado | Revisar el horario efectivo y la zona horaria de la sucursal, y el turno asignado al empleado |
| `checklog/day_disabled` | El día está deshabilitado en el calendario efectivo (festivo, día libre del empleado o no laborable) | Si el día debía ser laborable, corregir el calendario. Si no, registrar las horas mediante jornada manual |
| `checklog/absence` | El empleado tiene registrada una ausencia que cubre ese día | Si la ausencia no es correcta, retirarla de su calendario y volver a fichar |
| `checklog/different_branches` | El descanso o la salida se intentan fichar en una sucursal distinta de la de la entrada | Fichar en la sucursal de la entrada; si hubo cambio de centro, cerrar la jornada y abrir otra |
| `checklog_update/future_not_allowed` | La corrección propuesta tiene fecha u hora futura | Indicar una hora que ya haya pasado |
| `checklog/calendar_not_resolved` | No hay calendario efectivo resuelto para esa fecha | Revisar el calendario de la entidad, la sucursal y el empleado para esa fecha. Mientras tanto, introducir las horas manualmente |
| `checklog/branch_geo_required` | La sucursal no tiene ubicación configurada | El Owner o Manager debe añadir las coordenadas de la sucursal en el backoffice |
| `checklog/two_type_followed` | Se ha intentado iniciar jornada dos veces seguidas | Cerrar la jornada abierta antes de iniciar una nueva |
| `checklog/overlap_detected` | Ya existe una jornada válida que solapa con ese horario | Revisar el historial del empleado y corregir el registro solapado antes de reintentar |
| `checklog/duplicate_pending` | Ya hay una solicitud pendiente para ese empleado en esa fecha | Esperar a que el responsable resuelva la solicitud existente en lugar de crear otra |
| `checklog/checkin_not_found` | No se encuentra el checkin de referencia para la operación | Verificar que existe el fichaje de entrada al que se quiere asociar la salida |
| `checklog/checkin_not_open` | El checkin no puede cerrarse manualmente por su estado actual | Revisar el estado del registro; si ya está cerrado o anulado, no admite cierre manual |
| `checklog/checkout_already_exists` | Ya existe un cierre pendiente o válido para ese checkin | Revisar el registro: la jornada ya tiene salida |
| `checklog/invalid_checki` | Fichaje de entrada no válido | Reintentar el fichaje. Si persiste, actualizar la app |
| `checklog/invalid_checkout` | Fichaje de salida no válido | Comprobar que hay una entrada abierta que cerrar |
| `checklog/invalid_restin` / `checklog/invalid_restout` | Inicio o fin de pausa no válido | Comprobar el orden de los registros: la pausa debe abrirse y cerrarse dentro de una jornada activa |
| `checklog/unknown_type` | Tipo de registro desconocido | Actualizar la app a la última versión |
| `checklog/invalid` | No se encuentra el registro relacionado | Refrescar la pantalla y reintentar |
| `checklog/bad_request` | Los datos del fichaje no son correctos o están incompletos | Actualizar la app; si continúa, reinstalar e iniciar sesión de nuevo |
| `checklog/internal_error` | Error interno del servidor al procesar el fichaje | Reintentar pasados unos minutos. Si dura más de 30 minutos, abrir incidencia con la hora exacta y el empleado afectado |

> `checklog/manual_request_created` no es un error: confirma que la solicitud de jornada manual se ha enviado correctamente y queda pendiente de aprobación.

---

## Acceso y sesión (`auth`)

| Código | Qué significa | Qué hacer |
|---|---|---|
| `auth/invalid-credential` | Credenciales incorrectas | Revisar correo y contraseña; usar la recuperación de contraseña si es necesario |
| `auth/invalid-email` | La dirección de correo no tiene un formato válido | Corregir el correo introducido |
| `auth/missing-email` / `auth/missing-password` | Falta el correo o la contraseña | Completar el campo que falta |
| `auth/email-already-exists` / `auth/email-already-in-use` | Ese correo ya está en uso | Iniciar sesión con esa cuenta o usar otro correo |
| `auth/weak-password` | La contraseña no cumple los requisitos mínimos | Elegir una contraseña más segura |
| `auth/too-many-requests` | Demasiados intentos en poco tiempo | Esperar unos minutos antes de reintentar |
| `auth/user-disabled` | La cuenta está deshabilitada | Contactar con el Owner de la entidad o con soporte |
| `auth/operation-not-allowed` | El acceso por correo y contraseña no está habilitado | Contactar con soporte |
| `auth/network-request-failed` | Error de red | Comprobar la conexión a internet y reintentar |
| `auth/unauthorized` | Acceso no autorizado al recurso, o sesión caducada | Cerrar sesión y volver a entrar. Si la cuenta fue desactivada, contactar con el Owner |
| `auth/untrusted_device` | El dispositivo no está autorizado y requiere verificación adicional | El Owner o Manager debe autorizar el dispositivo desde el perfil del empleado |
| `employee/invalid_token` | La validación del empleado ha caducado o no es válida. Caduca a los 30 días, igual que la sesión del empleado en la app | La app vuelve a iniciar sesión por sí sola. Si el aviso persiste, cerrar sesión en la app y entrar de nuevo |
| `turnstile/failed` | No se ha podido comprobar que quien se registra o recupera la contraseña es una persona | Recargar la página y repetir el reto de verificación |

---

## Verificación en dos pasos (`twofactor`)

| Código | Qué significa | Qué hacer |
|---|---|---|
| `twofactor/invalid_code` | El código TOTP introducido no es válido | Comprobar que la hora del dispositivo es correcta y generar un código nuevo |
| `twofactor/invalid_token` | La sesión ha expirado | Volver a iniciar sesión |
| `twofactor/not_activated` | El empleado no tiene la verificación en dos pasos activada | Activarla desde el perfil del empleado |
| `twofactor/user_not_activated` | La cuenta de usuario no tiene 2FA activado | Activar 2FA desde el perfil de usuario |
| `twofactor/unauthorized` | La operación exige un token 2FA | Completar la verificación en dos pasos para continuar |
| `twofactor/internal` | Error interno al procesar la verificación | Reintentar; si persiste, abrir incidencia |

---

## Empleados (`employee`) y sucursales (`branch`)

| Código | Qué significa | Qué hacer |
|---|---|---|
| `employee/not_found` | El empleado indicado no existe en la entidad | Verificar que el empleado sigue dado de alta |
| `employee/exist_employee` | Ya existe un empleado con ese correo o teléfono | Buscar el empleado existente en lugar de crear uno nuevo |
| `employee/branchId_required` | Falta la sucursal, que es obligatoria | Asignar al menos una sucursal antes de guardar |
| `employee/bad_request` | Falta el identificador del empleado en la operación | Repetir la acción desde la ficha del empleado |
| `branch/not_found` | La sucursal indicada no existe | Verificar que la sucursal existe y no ha sido eliminada |
| `employee/fired` | El empleado está dado de baja y no se puede añadir a un equipo | Elegir a otra persona o reactivar su ficha |
| `team/not_found` | El equipo ya no existe | Refrescar la lista de equipos |
| `team/name_taken` | Ya hay un equipo con ese nombre (sin distinguir mayúsculas, tildes ni espacios) | Elegir otro nombre |
| `team/member_exists` | Esa persona ya está en el equipo | Editar su puesto o su precio en lugar de volver a añadirla |
| `team/member_not_found` | Esa persona ya no está en el equipo | Refrescar la ficha del equipo |
| `team/branch_without_staff` | La sucursal no tiene a nadie activo que guardar como equipo | Dar de alta al personal en la sucursal o crear el equipo desde cero |
| `team/apply_conflict` | Alguien dio de alta a uno de los miembros en esa sucursal mientras se aplicaba el equipo; no se ha cambiado nada | Volver a aplicar el equipo: esa persona se saltará |
| `team/too_large` | Son demasiadas personas para una sola operación | Dividir el equipo en dos y aplicarlos por separado |
| `team/bad_request` | Los datos del equipo no son válidos | Revisar el nombre, el puesto y que el precio sea un número |

---

## Documentos (`documents`)

| Código | Qué significa | Qué hacer |
|---|---|---|
| `documents/unauthorized` | Sin permisos para acceder al documento | Revisar la visibilidad por rol del documento |
| `documents/storage_full` | La empresa ha llegado a los 2 GB incluidos y tiene desactivada la ampliación de almacenamiento | Activar **Ampliar almacenamiento** en **Entidad → Suscripciones**, o liberar espacio |
| `documents/not_found` | El documento no existe o no es visible para ese usuario | Comprobar que no está archivado y que el rol tiene visibilidad |
| `documents/file_required` | No se ha adjuntado ningún archivo | Adjuntar el fichero antes de guardar |
| `documents/file_too_large` | El archivo supera el máximo permitido de 10 MB | Comprimir el documento o dividirlo |
| `documents/invalid_mime_type` | Formato de archivo no permitido | Convertir el documento a un formato admitido |
| `documents/invalid_visibility_roles` | La configuración de visibilidad no es válida | Revisar los roles seleccionados |
| `documents/invalid_acknowledgement_mode` | La configuración de acuse de recibo no es válida | Revisar el modo de acuse elegido frente al ámbito del documento |
| `documents/acknowledgement_not_required` | El documento no requiere acuse de recibo | No es necesaria ninguna acción |
| `documents/acknowledgement_not_allowed` | Ese usuario no puede acusar recibo del documento | Comprobar que el documento va dirigido a ese empleado |
| `documents/restricted_document_type` | Sin permisos para ese tipo de documento | Revisar el rol necesario para ese tipo |
| `documents/already_archived` | El documento ya está archivado | No es necesaria ninguna acción |
| `documents/branch_not_found` | La sucursal o proyecto indicado no es válido | Seleccionar una sucursal existente |
| `documents/employee_not_found` | El empleado indicado no es válido | Seleccionar un empleado existente |
| `documents/employee_not_in_branch` | El empleado no pertenece a la sucursal seleccionada | Corregir la sucursal o la asignación del empleado |
| `documents/bad_request` | Los datos del documento no son válidos | Revisar los campos obligatorios del formulario |

---

## Tareas (`task`)

| Código | Qué significa | Qué hacer |
|---|---|---|
| `task/not_found` | La tarea no existe o fue eliminada | Refrescar el listado de tareas |
| `task/evidence_required` | La tarea exige subir evidencia antes de completarla | Adjuntar al menos una foto o vídeo y volver a completar |
| `task/forbidden` | Sin permisos para esa acción sobre la tarea | Revisar el nivel de responsabilidad requerido |
| `task/unauthorized` | Sin permisos para realizar la acción | Solicitar la acción a un responsable con nivel suficiente |
| `task/invalid_mime_type` | El formato del archivo adjunto no está permitido | Subir la evidencia como foto o vídeo en un formato estándar |
| `task/file_too_large` | El archivo supera el tamaño máximo permitido | Reducir la resolución o la duración del archivo |
| `task/bad_request` | La información de la tarea no es válida | Revisar los campos obligatorios: título, sucursal y fecha límite |
| `task/no_open_session` | Para iniciar, reanudar o completar la tarea hace falta tener la jornada abierta | Fichar la entrada y volver a intentarlo |
| `task/geo_required` | La tarea tiene lugar de trabajo propio y hace falta la ubicación; el backoffice no la envía | Iniciar, reanudar o completar la tarea desde la app, estando en el lugar |
| `task/out_of_worksite` | El empleado está fuera del margen del lugar de trabajo de la tarea. El aviso indica la distancia y el margen | Acercarse a la dirección de la tarea. Si el margen es demasiado estrecho para ese lugar, ampliarlo en la tarea |
| `task/worksite_imprecise` | La dirección del lugar de trabajo solo se ha localizado de forma aproximada (por ejemplo, a nivel de ciudad) | Añadir el número de portal y volver a elegir la dirección en el buscador |
| `task/worksite_invalid` | No se ha podido situar la dirección en el mapa | Elegir la dirección del buscador en lugar de escribirla a mano |
| `task/not_in_progress` | Solo se puede pausar una tarea en progreso | Iniciar la tarea antes de pausarla |
| `task/already_paused` | La tarea ya está en pausa; puede que otro asignado la haya pausado antes | Refrescar la tarea |
| `task/not_paused` | Se intentó reanudar una tarea que no está en pausa | Refrescar la tarea |
| `task/invalid_transition` | El cambio de estado no está permitido desde el estado actual; por ejemplo, completar una tarea rechazada | Reabrir la tarea devolviéndola a *Asignada* desde **Editar** |
| `task/invalid_status` | La acción exige otro estado; por ejemplo, validar una tarea que no está completada | Revisar el estado de la tarea |
| `task/invalid_employees` | Algún empleado no se puede asignar: no trabaja en la sucursal de la tarea o no está activo | Asignarlo a esa sucursal y comprobar que está activo |
| `task/branch_inactive` | La sucursal de la tarea está inactiva y no admite tareas nuevas ni copias | Activar la sucursal o usar otra |
| `task/source_config_invalid` | La tarea que se intenta duplicar tiene una configuración que ya no es válida | Abrir la tarea original, guardarla de nuevo y volver a duplicarla |

---

## Suscripción y facturación

| Código | Qué significa | Qué hacer |
|---|---|---|
| `subscription/limit_off` | El plan ha alcanzado el límite de operaciones permitidas | Revisar el estado de la suscripción o contactar con soporte |
| `suscription/entity_not_configured` | La entidad no tiene la configuración necesaria para contratar | Completar los datos legales y el método de pago en **Entidad** |
| `suscription_checkinbiz/entity_legal_not_configured` | Faltan los datos legales de la entidad para CheckBiz | Completar los datos de la empresa antes de contratar |
| `suscription/already_subscribed_into_plan` | La entidad ya está suscrita a ese plan | No es necesaria ninguna acción |
| `suscription/ko` | La suscripción no se ha podido completar | Revisar el método de pago y reintentar |
| `subscribe/not_found` | El servicio indicado no existe | Reintentar desde la pantalla de planes |
| `subscribe/invalid_entity_service` | La entidad o el servicio no son correctos | Verificar la entidad seleccionada |
| `subscribe/internal` | Error interno del servicio de suscripciones | Reintentar más tarde; si persiste, abrir incidencia |
| `subscribe/plan_not_available` | El plan elegido no está disponible para contratar | Elegir otro de los planes que ofrece la pantalla de planes |
| `sub/bad_request` | Los datos enviados no son válidos | Revisar el formulario y reintentar |
| `sub/entity_not_found` | La entidad no existe | Verificar la entidad seleccionada |
| `payment/pending` | Hay pagos pendientes en la cuenta | Regularizar el pago desde la sección de facturación |

---

## Vacaciones y permisos (`absence_request`)

Solicitudes desde la app, «Mi calendario» (aprueban los administradores en el panel, **Contacto → Solicitudes**).

| Código | Causa |
|---|---|
| `absence_request/invalid_type` | El tipo no es `vacation`, `personal`, `medical` ni `other`. |
| `absence_request/invalid_dates` | Fechas no válidas o fin anterior al inicio. |
| `absence_request/past` | La solicitud empieza antes de hoy. El pasado lo registra la empresa desde el panel. |
| `absence_request/too_long` | Más de 60 días en una sola solicitud. |
| `absence_request/note_too_long` | La nota supera los 500 caracteres. |
| `absence_request/overlap` | Se solapa con otra solicitud pendiente o aprobada, o con una ausencia ya registrada. |
| `absence_request/not_found` | La solicitud no existe o no es de esta persona. |
| `absence_request/not_pending` | Ya se resolvió o se canceló: no se puede cancelar, aprobar ni rechazar. |
| `calendar/forbidden` | La cuenta no tiene ficha de empleado activa (rutas de la persona) o no tiene asiento de administrador (rutas del panel). |

## Cuadrante de turnos (`calendar`)

Al cargar turnos por fecha a quien está **Por turnos**.

| Código | Qué significa | Qué hacer |
|---|---|---|
| `calendar/days_require_calendar_mode` | La persona no está **Por turnos**: está en **Semana tipo** o **Por tareas** | Pasarla a **Por turnos** en su ficha o en la de su sucursal |
| `calendar/day_in_the_past` | Se ha intentado cambiar un día anterior a hoy | Los días pasados no se cambian; hoy sí |
| `calendar/bad_request` | Un turno no es válido: la salida no es posterior a la entrada, dos turnos se cruzan o la fecha está demasiado lejos | Revisar las horas del día indicado |
| `calendar/invalid_range` / `calendar/range_too_long` | El periodo pedido no es válido o es demasiado largo | Consultar un periodo más corto |
| `calendar/schedule_mode_employee_only` | **Por tareas** solo se elige en la ficha de una persona | Ponerlo en la persona, no en la sucursal ni en la empresa |

## Punto de fichaje (`kiosk`)

| Código | Qué significa | Qué hacer |
|---|---|---|
| `kiosk/not_subscribed` | La empresa no tiene contratado el punto de fichaje | Contratarlo desde **Punto de fichaje** |
| `kiosk/disabled` | El punto de fichaje de esa sucursal está desactivado | Activarlo desde el panel |
| `kiosk/no_branch_geo` | La sucursal no tiene la dirección geolocalizada | Completar la dirección de la sucursal |
| `kiosk/no_branch_kiosk` | La persona no tiene ninguna sucursal con punto de fichaje, así que no hay tarjeta que enviarle | Activar el punto de fichaje en alguna de sus sucursales |
| `kiosk/device_not_eligible` | El dispositivo no cumple los requisitos: ubicación, precisión, cámara frontal o sistema | Leer el motivo en pantalla y corregirlo, o usar otro dispositivo |
| `kiosk/out_of_radius` | El dispositivo está más lejos del centro de lo permitido | Llevarlo al centro, revisar la dirección o ampliar el radio |
| `kiosk/suspended` | El punto de fichaje está en pausa porque el dispositivo salió del radio o perdió precisión | Vuelve solo cuando se cumple otra vez |
| `kiosk/replaced` | Se ha entrado con las mismas credenciales en otro dispositivo | Normal al cambiar de tablet; si no, regenerar las credenciales |
| `kiosk/revoked` | La sesión del dispositivo se cerró desde el panel | Volver a entrar con las credenciales |
| `kiosk/code_not_found` | El QR o el código no son de nadie en esta empresa, o se regeneraron | Entregar la tarjeta o el código actuales |
| `kiosk/too_many_attempts` | Varios códigos erróneos seguidos | Esperar los segundos que indica la pantalla |
| `kiosk/employee_not_in_branch` | La persona no está asignada a esa sucursal | Asignarla desde su ficha |
| `kiosk/session_expired` | Pasó demasiado tiempo entre identificarse y fichar | Volver a acercar el QR o teclear el código |
| `kiosk/photo_required` / `kiosk/photo_upload_failed` | Falta la foto, o no se pudo guardar y el fichaje no se ha registrado | Repetir el fichaje mirando a la cámara |
| `kiosk/unlock_invalid` | El PIN para salir del modo quiosco no es correcto | Consultar el PIN en **Ver credenciales** |
| `kiosk/invalid_radius` | El radio está fuera del rango permitido | Elegir un valor dentro del rango que indica el panel |

## Otros módulos

| Código | Qué significa | Qué hacer |
|---|---|---|
| `entity/not_found` | La entidad no existe | Verificar la entidad seleccionada en el backoffice |
| `user/not_found` | No hay ningún usuario con ese correo | Revisar el correo introducido |
| `user/internal` | Error interno del servicio de usuarios | Reintentar; si persiste, abrir incidencia |
| `report/internal_error` | Error interno al generar el informe | Reintentar con un rango de fechas menor; si persiste, abrir incidencia |
| `stats/range_and_groupBy_tolong` | El rango de fechas o la agrupación producen demasiados datos para representar | Seleccionar un rango menor u otra agrupación |
| `analyze/insufficient_data` | No hay datos suficientes para calcular los indicadores | Esperar a acumular más histórico de fichajes y tareas |
| `media/not_found` | El archivo no existe | Volver a subir el archivo |
| `media/invalid_meda_type` | Tipo de archivo no permitido | Usar un formato admitido |
| `media/invalid_dimesions` | Las dimensiones de la imagen no son válidas | Ajustar el tamaño de la imagen |
| `media/error` | Error interno de almacenamiento | Reintentar; si persiste, abrir incidencia |
| `internal` | Error interno del servidor | Reintentar; si persiste, abrir incidencia con la hora exacta |
| `unavailable` | Servicio temporalmente no disponible | Reintentar pasados unos minutos |

---

> **Aviso:** si un mismo código reaparece de forma sistemática después de aplicar la acción correctiva, abra una incidencia en el backoffice incluyendo el código exacto, la hora del fallo y el empleado afectado.

---

## Nota de rol

Este artículo es de consulta para **Owner** y **Manager**, responsables de diagnosticar y resolver errores operativos. Los empleados con rol Worker que vean un código de error en la app deben comunicárselo a su responsable con el código exacto que aparece en pantalla.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Problemas frecuentes y soluciones](../13-soporte-e-incidencias/88-problemas-frecuentes-y-soluciones.md) | Guía práctica de diagnóstico para las situaciones más habituales |
| [Crear una incidencia](../13-soporte-e-incidencias/85-crear-una-incidencia.md) | Cómo abrir un caso de soporte cuando el error no tiene solución directa |
| [Glosario](./89-glosario.md) | Definición de los términos técnicos utilizados en la plataforma |
| [Contactar con soporte técnico](../13-soporte-e-incidencias/87-contactar-con-soporte-tecnico.md) | Canales y tiempos de respuesta del equipo de soporte |

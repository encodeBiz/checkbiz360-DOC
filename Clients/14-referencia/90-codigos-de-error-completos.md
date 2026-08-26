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
| `checklog/day_disabled` | El día está deshabilitado en el calendario efectivo (festivo o no laborable) | Si el día debía ser laborable, corregir el calendario. Si no, registrar las horas mediante jornada manual |
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

---

## Documentos (`documents`)

| Código | Qué significa | Qué hacer |
|---|---|---|
| `documents/unauthorized` | Sin permisos para acceder al documento | Revisar la visibilidad por rol del documento |
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
| `sub/bad_request` | Los datos enviados no son válidos | Revisar el formulario y reintentar |
| `sub/entity_not_found` | La entidad no existe | Verificar la entidad seleccionada |
| `payment/pending` | Hay pagos pendientes en la cuenta | Regularizar el pago desde la sección de facturación |

---

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

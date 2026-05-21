# Problemas frecuentes y soluciones

Este artículo recoge las doce situaciones técnicas y operativas más habituales en CheckBiz360, junto con los pasos de diagnóstico y resolución recomendados. Consulte esta guía antes de abrir una incidencia, ya que la mayoría de estos problemas tienen solución directa sin necesidad de intervención del equipo de soporte.

---

## 1. El empleado no puede fichar (error genérico)

**Síntoma:** El empleado pulsa el botón de fichaje en la app y aparece un mensaje de error sin código específico, o la operación no se completa.

**Pasos de resolución:**

1. Verifique que el dispositivo tiene conexión a internet activa (Wi-Fi o datos móviles). Sin conexión, el fichaje no puede procesarse.
2. Compruebe que el GPS del dispositivo está activado. Acceda a los ajustes del sistema operativo y confirme que la ubicación está habilitada para CheckBiz360.
3. Revise que la aplicación tiene permisos de ubicación concedidos: en iOS, vaya a **Ajustes > CheckBiz360 > Ubicación** y seleccione "Al usar la app". En Android, acceda a **Ajustes > Aplicaciones > CheckBiz360 > Permisos > Ubicación**.
4. Cierre la app completamente y vuelva a abrirla.
5. Si el problema persiste, actualice la app a la versión más reciente desde la tienda de aplicaciones.

---

## 2. Error "Fuera de zona" persistente

**Síntoma:** El empleado recibe el error `checklog/out_of_radius` de forma repetida incluso cuando se encuentra físicamente en el lugar de trabajo.

**Pasos de resolución:**

1. En el backoffice, acceda a **Sucursales** y seleccione la sucursal afectada.
2. Verifique las coordenadas de la sucursal: compruebe que la latitud y longitud registradas corresponden al punto exacto del establecimiento y no a una dirección aproximada o incorrecta.
3. Revise el radio de fichaje configurado para la sucursal. Si el edificio o el entorno tienen señal GPS imprecisa (plantas interiores, sótanos, zonas con interferencias), considere ampliar el radio.
4. Pida al empleado que compruebe la precisión GPS de su dispositivo: en exteriores, la precisión suele ser de 5 a 15 metros; en interiores puede superar los 50 metros.
5. Si el problema afecta a todos los empleados de la sucursal, revise si las coordenadas se modificaron recientemente de forma accidental.

---

## 3. El empleado no recibe el correo de bienvenida

**Síntoma:** Un empleado recién dado de alta en la plataforma no ha recibido el correo de invitación con sus credenciales de acceso.

**Pasos de resolución:**

1. Pida al empleado que revise la carpeta de correo no deseado o spam.
2. Verifique en el backoffice, dentro del perfil del empleado, que la dirección de correo electrónico está escrita correctamente (sin espacios, sin errores tipográficos).
3. Si la dirección es correcta y el correo no aparece en ninguna carpeta, acceda al perfil del empleado y pulse **Reenviar invitación**.
4. Si después de reenviar el correo sigue sin llegar, compruebe con el empleado si su empresa tiene filtros de correo corporativo que puedan estar bloqueando los mensajes de @encodebiz.com. En ese caso, será necesario añadir ese dominio a la lista de remitentes permitidos.

---

## 4. La app no abre o se cierra sola

**Síntoma:** La aplicación CheckBiz360 se cierra de forma inesperada al abrirse o durante su uso normal.

**Pasos de resolución:**

1. Compruebe que la versión instalada es la más reciente: acceda a la App Store o Google Play y actualice si hay una versión disponible.
2. Reinicie el dispositivo completamente y vuelva a intentar abrir la app.
3. Si el problema persiste tras la actualización, desinstale la aplicación y vuelva a instalarla desde la tienda oficial.
4. Tras reinstalar, inicie sesión con las mismas credenciales. Los datos del servidor no se pierden con la reinstalación.
5. Si la app sigue cerrándose, anote el modelo del dispositivo y la versión del sistema operativo e incluya esta información al abrir una incidencia.

---

## 5. Error "Dispositivo no autorizado"

**Síntoma:** El empleado recibe el mensaje de error `auth/untrusted_device` al intentar iniciar sesión o fichar desde un dispositivo nuevo.

**Pasos de resolución:**

1. Acceda al backoffice con su cuenta de Owner o Manager.
2. Vaya al perfil del empleado afectado.
3. En la sección **Dispositivos de confianza**, localice el nuevo dispositivo (aparecerá listado con su identificador).
4. Pulse **Autorizar dispositivo** para marcarlo como de confianza.
5. Informe al empleado de que puede volver a intentar iniciar sesión.

> **Aviso:** Si la empresa tiene activada la restricción de dispositivos únicos por empleado, autorizar un nuevo dispositivo puede desautorizar el anterior automáticamente. Revise la configuración de seguridad de su entidad antes de autorizar el cambio.

---

## 6. El empleado no puede ver sus documentos

**Síntoma:** Un empleado indica que no encuentra en la app los documentos que deberían estar disponibles para él.

**Pasos de resolución:**

1. Acceda al backoffice y vaya al módulo **Documentos**.
2. Localice el documento en cuestión y compruebe su configuración de visibilidad.
3. Verifique que la visibilidad del documento está configurada como `private` (visible solo para el empleado asignado) o `public` (visible para todos), según corresponda.
4. Compruebe que el documento está asignado al empleado correcto: revise el campo de destinatario.
5. Verifique que el documento no está en estado de borrador o pendiente de publicación.
6. Si la configuración es correcta, pida al empleado que cierre sesión en la app y vuelva a iniciarla para forzar la sincronización.

---

## 7. La notificación push no llega

**Síntoma:** El empleado no recibe notificaciones de tareas, documentos o alertas del sistema en su dispositivo.

**Pasos de resolución:**

1. Verifique que el empleado ha concedido permisos de notificación a CheckBiz360. En iOS: **Ajustes > CheckBiz360 > Notificaciones** y activar "Permitir notificaciones". En Android: **Ajustes > Aplicaciones > CheckBiz360 > Notificaciones** y activar.
2. Compruebe que el modo "No molestar" o cualquier perfil de silencio no está activo en el dispositivo.
3. En algunos dispositivos Android con gestión agresiva de batería (Xiaomi, Huawei, OnePlus), es necesario excluir CheckBiz360 de la optimización de batería. Acceda a **Ajustes > Batería > Optimización de batería** y excluya la app.
4. Asegúrese de que la app está actualizada a la última versión.
5. Si el problema persiste, el empleado puede cerrar sesión y volver a iniciarla para registrar de nuevo el token de notificaciones.

---

## 8. El historial de asistencia muestra huecos

**Síntoma:** En el historial de un empleado aparecen días o jornadas sin registros completos, aunque el empleado asegura haber trabajado esos días.

**Pasos de resolución:**

1. Acceda al backoffice y revise el detalle de asistencia del empleado en la fecha afectada.
2. Compruebe si hay un registro de checkin sin checkout correspondiente. Esto genera una jornada incompleta (`incomplete_workday`).
3. Si el empleado olvidó hacer checkout, utilice la opción de **Jornada manual** para completar el registro retroactivamente.
4. Verifique si el empleado tiene jornadas con pausas (`restin` / `restout`) sin cerrar, que también pueden provocar registros incompletos.
5. Revise si en esas fechas había jornadas desactivadas en el calendario efectivo de la sucursal.

---

## 9. Las horas calculadas no coinciden con las esperadas

**Síntoma:** El total de horas trabajadas que muestra la plataforma para un empleado no coincide con el cálculo manual que realiza el manager.

**Pasos de resolución:**

1. Compruebe si la sucursal o el empleado tienen activado el ajuste automático de horario. Esta función redondea o ajusta los fichajes según reglas configuradas y puede alterar las horas brutas.
2. Revise si hay pausas registradas que se estén descontando del tiempo total.
3. Verifique si alguna jornada está marcada como incompleta, lo que puede excluirla del cálculo total.
4. Compruebe la zona horaria configurada en la sucursal y contrástela con la zona horaria del dispositivo del empleado.
5. Si detecta una discrepancia sistemática, acceda a la configuración de la sucursal y revise las reglas de cálculo de jornada.

---

## 10. La app muestra "Fuera de horario" cuando el empleado está en su turno

**Síntoma:** El empleado recibe el error `checklog/out_of_schedule` aunque asegura que está fichando dentro de su horario habitual.

**Pasos de resolución:**

1. Acceda al backoffice y revise el **horario efectivo** de la sucursal para el día en cuestión.
2. Verifique la zona horaria configurada en la sucursal. Si la zona horaria es incorrecta, los límites del turno pueden estar calculándose con un desfase de horas.
3. Compruebe que el empleado tiene asignado el turno correcto para ese día en el calendario efectivo.
4. Revise si existen excepciones o días festivos configurados que puedan estar desactivando el turno.
5. Si el horario parece correcto, compruebe si hay un margen de tolerancia de fichaje configurado y si el empleado estaba intentando fichar justo al límite o fuera de él.

---

## 11. El empleado aparece como inactivo en el backoffice

**Síntoma:** Al consultar la lista de empleados, uno de ellos aparece con estado inactivo aunque debería estar activo.

**Pasos de resolución:**

1. Acceda al perfil del empleado en el backoffice.
2. Revise el campo **Estado del perfil**. Si está establecido como "Inactivo", pulse **Reactivar empleado**.
3. Verifique que la cuenta no fue desactivada como consecuencia de una baja temporal o un proceso de offboarding iniciado por error.
4. Compruebe que el empleado no superó el límite de empleados activos del plan de suscripción contratado. En ese caso, puede ser necesario desactivar otro empleado o actualizar el plan.

---

## 12. No se puede generar el informe de un periodo anterior

**Síntoma:** Al intentar generar un informe para un rango de fechas pasado, el sistema devuelve un error o no muestra datos.

**Pasos de resolución:**

1. Verifique que el rango de fechas seleccionado no supera el periodo de retención de datos incluido en su plan de suscripción.
2. Compruebe que su rol tiene permisos para generar informes del tipo seleccionado. Los informes de costes y anomalías están restringidos a Owner y Manager.
3. Asegúrese de que los filtros aplicados (sucursal, empleado) no excluyen todos los registros disponibles para ese periodo.
4. Si el problema persiste con un rango de fechas que debería estar dentro del periodo de retención, abra una incidencia con el rango exacto que está intentando consultar.

---

> **Aviso:** Si alguno de los pasos anteriores no resuelve el problema, no repita la misma acción varias veces. Recopilar evidencias (capturas de pantalla, código de error, fecha y hora exacta) y abrir una incidencia es siempre más eficaz que intentar forzar una solución que puede agravar el problema.

---

## Nota de rol

Este artículo está dirigido principalmente a **Owner** y **Manager**, que son los responsables de diagnosticar y resolver los problemas operativos de sus equipos. Los empleados con rol Worker que experimenten alguno de estos problemas deben comunicárselo a su Manager.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una incidencia](./85-crear-una-incidencia.md) | Cómo abrir formalmente un caso de soporte |
| [Contactar con soporte técnico](./87-contactar-con-soporte-tecnico.md) | Canales y tiempos de respuesta del equipo de soporte |
| [Codigos de error completos](../14-referencia/90-codigos-de-error-completos.md) | Referencia completa de todos los códigos de error del sistema |
| [Solicitar una jornada manual](../03-control-horario/27-solicitar-jornada-manual.md) | Cómo corregir un fichaje incorrecto o ausente |
| [Gestión de dispositivos de confianza](../02-empleados/18-dispositivos-de-confianza.md) | Cómo autorizar nuevos dispositivos desde el backoffice |

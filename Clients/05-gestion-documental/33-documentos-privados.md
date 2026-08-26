# Documentos privados

El campo **Privado** de un documento en CheckBiz360 controla si el empleado puede ver ese documento desde su app móvil. Cuando un documento está marcado como privado, existe en el sistema y es accesible para los gestores con los permisos adecuados, pero el empleado no lo verá ni recibirá notificaciones sobre él.

Este mecanismo permite gestionar documentación de carácter sensible —como evaluaciones de desempeño, cartas de amonestación o documentos de carácter disciplinario— sin que el empleado acceda a ella antes de que el responsable lo considere oportuno.

## Qué significa que un documento sea privado

Cuando el campo `private` de un documento está activado:

- El documento **no aparece** en la lista de documentos del empleado en la app móvil.
- No se envía notificación push al empleado, aunque la opción de notificación esté marcada.
- El documento **sí es visible** para los gestores (Manager, Owner) en el backoffice.
- El documento puede ser consultado, editado o eliminado desde el backoffice por los usuarios con permisos suficientes.

Cuando el campo `private` está desactivado y el documento está publicado:

- El empleado puede ver y descargar el documento desde la app.
- Si se activó la notificación al publicar, el empleado recibe un aviso push en su dispositivo.

## Tabla de visibilidad por rol

La siguiente tabla muestra qué puede ver cada rol según el estado de visibilidad del documento:

| Rol | Documento privado | Documento no privado (publicado) |
|---|---|---|
| Owner | Visible en backoffice | Visible en backoffice |
| Manager | Visible en backoffice | Visible en backoffice |
| Supervisor | Según permisos delegados | Visible en backoffice (si tiene acceso) |
| Worker (empleado) | No visible | Visible en la app móvil |

> **Nota:** Un supervisor solo tiene acceso a los documentos de los empleados de su equipo y únicamente si el manager le ha concedido ese permiso explícito. Consulte el artículo sobre permisos de acceso documental para el detalle completo.

## Casos de uso habituales

### Documentos disciplinarios

Las cartas de amonestación, apercibimientos y otros documentos de carácter disciplinario suelen prepararse antes de entregarse formalmente al empleado. Subirlos con visibilidad privada permite tenerlos listos en el sistema sin que el empleado tenga acceso hasta el momento en que se produce la comunicación oficial.

Una vez realizada la notificación formal, el responsable cambia la visibilidad a pública y el empleado puede acceder al documento desde la app y acusar recibo si se le solicita.

### Evaluaciones de desempeño

Las evaluaciones de rendimiento son documentos confidenciales que deben ser revisados y validados internamente antes de compartirse con el empleado. Mantenerlas como privadas durante el proceso de revisión garantiza que el empleado solo acceda al resultado final una vez que el responsable lo ha aprobado.

### Documentación interna de RRHH

Algunos documentos son de uso exclusivo del departamento de RRHH y no están destinados al empleado en ningún momento: notas internas, informes de seguimiento o documentación de carácter administrativo. Para estos casos, el campo privado actúa como control permanente de acceso.

## Cómo cambiar la visibilidad de un documento existente

Puede modificar el estado de privacidad de un documento ya subido en cualquier momento. El proceso es el siguiente:

1. Acceda a la sección **Documentos** del backoffice.
2. Localice el documento que desea modificar usando los filtros de búsqueda.
3. Abra el detalle del documento pulsando sobre él.
4. Edite el documento y cambie el valor del campo **Privado**.
5. Guarde los cambios.

Si cambia un documento de privado a público, el empleado podrá verlo inmediatamente desde su app. Si desea que reciba también una notificación, deberá enviarla manualmente desde el panel del documento, ya que el cambio de visibilidad por sí solo no genera una notificación automática.

> **Importante:** El cambio de visibilidad de privado a público es inmediato. Asegúrese de que el documento está en su estado definitivo antes de hacerlo visible para el empleado, ya que no existe un periodo de gracia ni una confirmación adicional.

Si cambia un documento de público a privado, el empleado dejará de verlo en su app de forma inmediata, aunque ya lo haya consultado o descargado previamente.

## Consideraciones sobre notificaciones y privacidad

Cuando sube un documento marcado como privado, el sistema no enviará la notificación push al empleado aunque la opción esté activada. La notificación solo se envía en el momento de la publicación si el documento no es privado.

Si sube un documento como privado, trabaja en él internamente y posteriormente lo hace público, el flujo de notificación se gestiona de forma manual: deberá iniciar la notificación desde el detalle del documento si desea informar al empleado.

## Artículos relacionados

- [Qué es el módulo documental](30-que-es-el-modulo-documental.md)
- [Subir y organizar documentos](31-subir-y-organizar-documentos.md)
- [Notificaciones de documentos](34-notificaciones-de-documentos.md)
- [Permisos de acceso documental](37-permisos-de-acceso-documental.md)
- [Acuse de recibo](35-firma-electronica.md)

# Notificaciones de documentos

Cuando se publica un documento en CheckBiz360, el sistema puede enviar automáticamente una notificación push al empleado destinatario. Esta notificación informa al empleado de que tiene un nuevo documento disponible en la app y, al pulsar sobre ella, lo lleva directamente a la pantalla de detalle del documento correspondiente.

Las notificaciones documentales forman parte del sistema de comunicación de CheckBiz360 y utilizan el mismo canal de notificaciones push que el resto de la plataforma.

## Cómo funciona la notificación al subir un documento

Cuando el responsable publica un documento, puede activar el envío de notificación push en el propio formulario de subida. Si la opción está marcada y el documento no está configurado como privado, el sistema envía la notificación de forma automática en el momento de la publicación.

El flujo completo es:

1. El gestor sube el documento y activa la opción de notificación.
2. El sistema verifica que el documento no está marcado como privado.
3. Se genera y envía una notificación push al dispositivo del empleado.
4. El empleado ve la notificación en la pantalla de bloqueo o en el centro de notificaciones de su dispositivo.
5. Al pulsar la notificación, la app de CheckBiz360 se abre directamente en el detalle del documento.

> **Importante:** Si el documento está marcado como privado, no se enviará notificación push al empleado, aunque la opción de notificación esté activa. La notificación solo se envía para documentos con visibilidad pública.

## Qué contiene la notificación

La notificación que recibe el empleado incluye la información necesaria para que la app navegue directamente al documento correcto. Desde el punto de vista del empleado, la notificación muestra el título del documento y el nombre de la empresa, de forma similar a otras notificaciones de la plataforma.

## Qué ve el empleado al recibir la notificación

En el dispositivo del empleado, la notificación aparece con el título del documento como asunto principal. Al pulsar sobre ella, la app se abre —o se despierta desde segundo plano si ya estaba instalada— y navega directamente al detalle del documento.

Desde esa pantalla, el empleado puede:

- Leer el documento completo.
- Descargarlo en su dispositivo.
- Firmarlo si el documento tiene activa la solicitud de firma.

Si el empleado no tiene la app instalada o las notificaciones push desactivadas en su dispositivo, no recibirá el aviso. En ese caso, el documento seguirá estando disponible en la app en la sección de documentos, pero sin el aviso proactivo.

## Configurar qué documentos generan notificación

La decisión de generar o no una notificación se toma en el momento de subir el documento, marcando o desmarcando la opción correspondiente en el formulario. No existe una regla global que active o desactive las notificaciones para todas las subidas; la elección es por documento.

Esto permite gestionar casos distintos:

- **Documentos que siempre deben notificar**: nóminas mensuales, contratos nuevos, certificados solicitados por el empleado. Active siempre la notificación para este tipo de documentos.
- **Documentos de archivo interno que no requieren aviso**: versiones corregidas de documentos ya notificados, copias de respaldo o documentos administrativos que el empleado puede consultar bajo demanda. En estos casos puede subir el documento sin notificación.

> **Nota:** Si publica un documento sin notificación y posteriormente desea informar al empleado, puede enviar la notificación de forma manual desde el detalle del documento en el backoffice. Esto es útil cuando se detecta un error en la notificación original o cuando se quiere reenviar el aviso a un empleado que no abrió el documento.

## Consideraciones sobre dispositivos y permisos

Para que el empleado reciba notificaciones push, es necesario que:

1. Tenga la app de CheckBiz360 instalada en su dispositivo (iOS o Android).
2. Haya concedido permisos de notificación a la app durante el proceso de instalación o en la configuración del sistema operativo.
3. El dispositivo tenga conexión a internet en el momento del envío o en los momentos posteriores en que el sistema operativo intente la entrega.

Si un empleado indica que no recibe notificaciones, verifique primero que los permisos de notificación están habilitados para la app CheckBiz360 en la configuración de su dispositivo, antes de revisar la configuración en el backoffice.

## Artículos relacionados

- [Qué es el módulo documental](30-que-es-el-modulo-documental.md)
- [Subir y organizar documentos](31-subir-y-organizar-documentos.md)
- [Documentos privados](33-documentos-privados.md)
- [Firma electrónica](35-firma-electronica.md)
- [Permisos de acceso documental](37-permisos-de-acceso-documental.md)

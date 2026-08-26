# Qué es el módulo documental

El módulo documental de CheckBiz360 permite a las empresas gestionar, distribuir y archivar documentos laborales directamente en la plataforma. A diferencia de un repositorio genérico de archivos, cada documento queda vinculado a un empleado concreto y a su relación laboral con la entidad, lo que convierte el sistema en un expediente digital de personal estructurado y trazable.

El módulo forma parte de la suscripción: está disponible en **Documentos**, en el menú lateral del backoffice, sin depender del plan contratado.

## Para qué sirve

La gestión documental en CheckBiz360 responde a una necesidad habitual en los departamentos de RRHH: distribuir documentos laborales de forma ordenada, garantizar que el empleado los recibe y puede consultarlos, y mantener un archivo digital organizado por tipo de documento y periodo.

Con el módulo documental usted puede:

- Subir nóminas, contratos, certificados y otros documentos laborales desde el backoffice.
- Dirigir cada documento a un empleado concreto, a toda una sucursal o a toda la entidad.
- Enviar una notificación push al empleado en el momento de la publicación.
- Controlar qué roles pueden ver cada documento.
- Exigir **acuse de recibo** y comprobar quién lo ha dado y quién no.
- Archivar un documento cuando deja de estar vigente, sin perderlo.

## Tipos de documentos que se pueden gestionar

El módulo clasifica los documentos en doce tipos:

| Tipo | Ejemplos habituales |
|---|---|
| Nómina | Recibo de salario mensual, liquidación final |
| Contrato | Contrato inicial, prórrogas, modificaciones de condiciones |
| Amonestación | Carta de amonestación disciplinaria |
| Llamada de atención | Aviso previo, advertencia formal |
| Justificante | Justificantes de ausencia y de permisos |
| Certificado | Certificado de empresa, de vida laboral, de retenciones |
| Política | Política de empresa, código de conducta |
| Procedimiento | Instrucción de trabajo, protocolo operativo |
| Prevención de riesgos | Evaluación de riesgos, formación PRL, entrega de EPI |
| Protocolo de sucursal | Normativa específica de un centro de trabajo |
| Documento de proyecto | Documentación asociada a un proyecto o cliente |
| Otro | Cualquier documento que no encaje en los anteriores |

El tipo se asigna al subir el documento y facilita los filtros de búsqueda, tanto para los gestores como para el empleado desde la app.

### Ámbito del documento

Además del tipo, cada documento tiene un **ámbito** que determina a quién va dirigido:

- **Empleado** — un documento personal, como una nómina o un contrato.
- **Sucursal** — dirigido a todo el personal de un centro, como un protocolo de apertura.
- **Entidad** — dirigido a toda la plantilla, como una política de empresa.

## Diferencia con un sistema de almacenamiento genérico

Un servicio de almacenamiento genérico —como una carpeta compartida en la nube— almacena archivos sin contexto. CheckBiz360 no es eso.

En CheckBiz360, cada documento conoce a quién pertenece, a qué relación laboral corresponde, qué rol puede verlo y si el empleado ha acusado recibo o no. Esto permite, por ejemplo, que cuando un empleado abre la app solo vea sus propios documentos y no los del resto del equipo, o que un manager pueda filtrar todos los contratos vigentes de su sucursal sin tener que organizar carpetas manualmente.

Esta vinculación con el empleado y con su relación laboral es lo que convierte el módulo en un expediente de personal, no en un almacén de archivos.

## Casos de uso por rol

### Responsable de RRHH o Manager

Cada mes, el responsable sube las nóminas de los empleados desde el backoffice. Selecciona el archivo, indica la categoría, el periodo y el empleado destinatario, y marca si desea enviar una notificación push. El empleado recibe la notificación en su dispositivo y, al pulsar sobre ella, accede directamente al documento en la app.

Si el documento requiere **acuse de recibo**, el responsable activa esa opción antes de publicar. El sistema registra la fecha y hora en que el empleado confirma la lectura, y sobre qué versión del documento lo hizo.

### Supervisor

El supervisor puede consultar los documentos de los empleados de su equipo cuya visibilidad lo permita. La subida y la configuración de visibilidad se reservan habitualmente al nivel de manager o superior; algunos tipos de documento están además restringidos por rol y devuelven el error `documents/restricted_document_type` a quien no tiene nivel suficiente.

### Empleado (Worker)

El empleado accede a sus documentos desde la app móvil, en la sección de documentos. Solo ve los que le han sido asignados y cuya visibilidad lo alcanza. Puede descargarlos y, si se le solicita, **acusar recibo** desde el propio dispositivo.

> **Nota:** el acuse de recibo no es una firma electrónica. Acredita que el empleado accedió al documento y cuándo, pero no incorpora certificación cualificada. La firma electrónica avanzada (eIDAS) está en el roadmap.

> **Nota:** Los documentos marcados como privados por el gestor no son visibles para el empleado hasta que el responsable decide publicarlos o cambia su estado de visibilidad. Consulte el artículo sobre documentos privados para más detalle.

## Artículos relacionados

- [Subir y organizar documentos](31-subir-y-organizar-documentos.md)
- [Nóminas y contratos](32-nominas-y-contratos.md)
- [Documentos privados](33-documentos-privados.md)
- [Notificaciones de documentos](34-notificaciones-de-documentos.md)
- [Acuse de recibo](35-firma-electronica.md)
- [Historial de versiones](36-historial-de-versiones.md)
- [Permisos de acceso documental](37-permisos-de-acceso-documental.md)
- [Exportar documentos](38-exportar-documentos.md)

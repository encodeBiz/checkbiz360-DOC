# Subir y organizar documentos

El backoffice de CheckBiz360 centraliza todo el proceso de carga y distribución de documentos laborales. Desde un único panel puede subir archivos, asignarlos a los empleados correspondientes, definir su visibilidad y organizar el archivo documental por categorías y periodos.

## Antes de empezar

Para subir documentos necesita tener el rol de Manager o Owner en la entidad. Los supervisores pueden tener acceso a esta función si el manager les ha delegado ese permiso. Si no ve la opción de subida en su panel, consulte con el responsable de la entidad para verificar sus permisos.

Los formatos aceptados son PDF e imágenes (JPG, PNG). Se recomienda el uso de PDF para garantizar que el documento se visualiza correctamente en cualquier dispositivo, especialmente en la app móvil del empleado.

## Cómo subir un documento

1. Acceda al backoffice y navegue hasta la sección **Documentos** del menú principal.
2. Pulse el botón **Nuevo documento**.
3. Rellene los campos del formulario tal como se describe en la sección siguiente.
4. Adjunte el archivo desde su dispositivo.
5. Revise los datos y pulse **Guardar** o **Publicar** según corresponda.

> **Importante:** Si pulsa **Guardar** sin publicar, el documento quedará en estado borrador y el empleado no lo verá ni recibirá notificación. Para que el empleado tenga acceso, el documento debe estar publicado y con visibilidad habilitada.

## Campos del formulario

### Título

El título es el nombre con el que el empleado verá el documento en su app. Sea descriptivo y consistente en el formato que usa su empresa. Un ejemplo habitual es: `Nómina - Marzo 2026`.

### Descripción

Campo opcional que permite añadir contexto al documento. Puede usarlo para indicar el periodo que cubre, si contiene alguna corrección respecto a versiones anteriores o cualquier instrucción para el empleado.

### Categoría

Seleccione la categoría que corresponda al tipo de documento:

- **Nómina**: recibos de salario, liquidaciones finales, complementos extraordinarios.
- **Contrato**: contratos de trabajo, prórrogas, modificaciones de condiciones laborales.
- **Certificado**: certificados de empresa, de vida laboral, bajas médicas u otros emitidos por organismos externos.
- **Otro**: cualquier documento que no encaje en las categorías anteriores, como cartas de comunicación interna, evaluaciones de desempeño o amonestaciones.

La categoría no afecta al acceso ni a la visibilidad del documento, pero facilita enormemente la búsqueda y la organización del archivo cuando el volumen de documentos crece.

### Empleado o empleados destinatarios

Puede asignar el documento a un único empleado o a varios a la vez. Cuando asigna el mismo documento a varios empleados —por ejemplo, una circular informativa— el sistema crea una entrada de documento por cada empleado, de modo que cada uno accede a su propia copia y la trazabilidad queda separada por persona.

Para asignar múltiples destinatarios, use el campo de búsqueda de empleados y selecciónelos uno a uno o mediante los filtros de sucursal o departamento si los tiene configurados.

### Visibilidad: el campo privado

El campo **Privado** controla si el empleado puede ver el documento desde su app.

- **Privado desactivado (público)**: el empleado puede ver y descargar el documento desde el momento en que se publica.
- **Privado activado**: el documento solo es visible para los gestores con acceso al backoffice. El empleado no lo verá en su app aunque el documento exista en el sistema.

Este campo es útil cuando necesita subir documentación interna de carácter sensible —como notas disciplinarias o evaluaciones confidenciales— sin que el empleado acceda a ella hasta que usted lo decida.

> **Nota:** Puede cambiar la visibilidad de un documento ya subido en cualquier momento desde los detalles del documento. Consulte el artículo sobre documentos privados para más información sobre los casos de uso de este campo.

## Organizar el archivo documental

A medida que el volumen de documentos crece, mantener el archivo ordenado resulta fundamental para localizar documentos rápidamente.

Aplique estas convenciones desde el principio:

- **Título consistente**: use siempre el mismo formato de nombre, por ejemplo `[Tipo] - [Empleado/Periodo]`.
- **Categoría correcta**: no use la categoría "Otro" como cajón de sastre. Reserve las categorías específicas para los documentos que correspondan.
- **Periodos claros en la descripción**: especialmente en nóminas, indique el mes y año en el título o en la descripción.

Los filtros del panel de documentos le permiten buscar por categoría, por empleado y por fecha de subida, lo que facilita la gestión incluso cuando el archivo contiene cientos de documentos.

## Artículos relacionados

- [Qué es el módulo documental](30-que-es-el-modulo-documental.md)
- [Nóminas y contratos](32-nominas-y-contratos.md)
- [Documentos privados](33-documentos-privados.md)
- [Notificaciones de documentos](34-notificaciones-de-documentos.md)
- [Permisos de acceso documental](37-permisos-de-acceso-documental.md)
- [Exportar documentos](38-exportar-documentos.md)

# Acuse de recibo y firma electrónica

En la versión actual de CheckBiz360, el mecanismo disponible para que el empleado confirme que ha visto y leído un documento es el **acuse de recibo**. Esta funcionalidad permite al gestor saber de forma inequívoca qué empleados han accedido al documento y han reconocido explícitamente su lectura, sin necesidad de pasos adicionales ni herramientas externas.

## Qué es el acuse de recibo

El acuse de recibo es una confirmación que el empleado realiza voluntariamente desde la app de CheckBiz360 tras acceder al contenido de un documento. Al pulsar el botón de confirmación, el sistema registra:

- **Quién ha confirmado**: nombre e identificador del empleado dentro de la plataforma.
- **Cuándo lo ha confirmado**: fecha y hora exactas de la acción.

Este registro queda vinculado al documento y es consultable por los gestores con acceso al backoffice. No es editable ni eliminable, lo que garantiza la integridad del registro.

## Cómo funciona para el empleado

Cuando un empleado accede a un documento desde su app de CheckBiz360, puede leer o visualizar el contenido completo. Si el documento tiene habilitada la opción de confirmación de lectura, en la pantalla de detalle del documento aparece un botón que le permite confirmar que ha visto el contenido.

Una vez realizada la confirmación, el botón desaparece y el documento queda marcado como leído en el registro de la plataforma. El empleado puede seguir accediendo al documento en cualquier momento posterior.

> **Nota:** Si el empleado cierra el documento sin confirmar, el sistema no lo registra como leído. El documento permanece en su lista de pendientes hasta que realice la confirmación.

## Cómo lo ve el manager

El gestor puede consultar el estado de acuse de recibo de cada documento desde el backoffice. En el detalle de un documento con confirmación de lectura activada, se muestra:

- La lista de empleados destinatarios del documento.
- El estado de cada empleado: si ha confirmado la lectura o si aún no lo ha hecho.
- La fecha y hora de confirmación de cada empleado que ya ha actuado.

Esta información permite al gestor identificar fácilmente quién ha acusado recibo y quién no, y actuar en consecuencia —por ejemplo, enviando un recordatorio manual o haciendo seguimiento directo con el empleado.

## Cómo activar la confirmación de lectura en un documento

Al crear o editar un documento en el backoffice, encontrará la opción para requerir confirmación de lectura en el formulario del documento. El proceso es el siguiente:

1. Acceda al backoffice y cree un nuevo documento o edite uno existente.
2. Active la opción **Requiere confirmación de lectura** en el formulario.
3. Asegúrese de que el documento es visible para los empleados destinatarios (no marcado como privado si no procede).
4. Guarde y publique el documento.

Si tiene activadas las notificaciones push para el módulo documental, el empleado recibirá un aviso indicando que tiene un documento pendiente de confirmar.

## Casos de uso habituales

El acuse de recibo es especialmente útil en:

- **Circulares y comunicados internos**: el gestor necesita saber que todos los empleados han leído un cambio de procedimiento, una nueva política interna o una comunicación relevante de la empresa.
- **Documentos contractuales y laborales**: nóminas, actualizaciones de condiciones laborales o acuerdos de horario en los que conviene dejar constancia de que el empleado ha recibido y visto el documento.
- **Normativas de prevención de riesgos**: protocolos de seguridad o documentos de PRL que el empleado debe conocer y cuya recepción conviene acreditar.

---

## Firma electrónica

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

En una versión futura de CheckBiz360 estará disponible un mecanismo de firma electrónica que permitirá al empleado no solo confirmar la lectura de un documento, sino también prestar su conformidad expresa mediante una firma registrada con plena trazabilidad. Este mecanismo contempla la posibilidad de rechazar la firma y el registro detallado del estado de cada solicitud (pendiente, firmado, rechazado).

Para documentos que en su contexto actual requieran un nivel de firma más elevado —como determinadas modificaciones contractuales—, consulte con su asesoría jurídica las opciones disponibles mediante servicios de firma certificada externos compatibles con el Reglamento eIDAS.

---

## Artículos relacionados

- [Qué es el módulo documental](30-que-es-el-modulo-documental.md)
- [Subir y organizar documentos](31-subir-y-organizar-documentos.md)
- [Nóminas y contratos](32-nominas-y-contratos.md)
- [Documentos privados](33-documentos-privados.md)
- [Notificaciones de documentos](34-notificaciones-de-documentos.md)
- [Historial de versiones](36-historial-de-versiones.md)

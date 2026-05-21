# Seguimiento y resolución de incidencias

Una vez creada una incidencia en CheckBiz360, el sistema ofrece herramientas para supervisar su evolución, añadir información adicional y verificar que el problema ha quedado completamente resuelto. Este artículo describe el ciclo de vida completo de una incidencia: desde su apertura hasta su cierre definitivo, incluyendo cómo reabrir un caso si el problema reaparece.

---

## Estados de una incidencia

Cada incidencia pasa por una serie de estados que reflejan su situación en el proceso de resolución. Puede consultar el estado actual en cualquier momento accediendo a **Soporte > Incidencias** en el backoffice.

| Estado | Significado |
|---|---|
| Abierta | La incidencia ha sido registrada y está pendiente de ser analizada por el equipo de soporte |
| En revisión | El equipo de soporte ha comenzado a investigar el problema. Pueden solicitar información adicional |
| Resuelta | El equipo de soporte ha aplicado una solución. Se espera confirmación por parte del cliente |
| Cerrada | El cliente ha confirmado que el problema está resuelto, o han transcurrido 7 días desde la resolución sin objeción |

### Quién puede cambiar el estado

- El equipo de soporte de CheckBiz360 puede mover una incidencia a cualquier estado.
- El **Owner** o el **Manager** que abrió la incidencia puede:
  - Marcarla como **Resuelta** si el problema ha desaparecido antes de que el equipo de soporte intervenga.
  - **Reabrir** una incidencia que estaba en estado Resuelta o Cerrada si el problema persiste o reaparece.
- Los roles de Supervisor y Worker no tienen acceso al módulo de incidencias.

---

## Cómo añadir comentarios y actualizaciones

Durante la vida de una incidencia, es habitual que el equipo de soporte solicite información adicional o que usted quiera reportar una nueva observación. Todos estos intercambios se registran en el hilo de comentarios de la incidencia.

### Añadir un comentario

1. Acceda a **Soporte > Incidencias** en el backoffice.
2. Localice la incidencia por su número de seguimiento o mediante los filtros disponibles.
3. Haga clic en el número de la incidencia para abrir su detalle.
4. Desplácese hasta la sección **Comentarios** en la parte inferior de la pantalla.
5. Escriba su mensaje en el campo de texto.
6. Si desea adjuntar una captura de pantalla o un archivo adicional, pulse el icono de adjunto antes de enviar.
7. Pulse **Enviar comentario**.

El equipo de soporte recibirá una notificación por correo electrónico con su comentario. Del mismo modo, usted recibirá una notificación cada vez que el equipo de soporte añada una respuesta.

> **Aviso:** No abra una nueva incidencia para proporcionar información sobre un caso ya existente. Utilice siempre el hilo de comentarios de la incidencia original para mantener todo el contexto agrupado.

---

## Historial de actuaciones

Cada incidencia mantiene un registro cronológico de todas las acciones realizadas sobre ella. Este historial incluye:

- Fecha y hora de cada cambio de estado.
- Nombre del usuario (cliente o soporte) que realizó la acción.
- Contenido de cada comentario añadido.
- Archivos adjuntos con la fecha en que fueron subidos.

El historial no puede modificarse ni eliminarse. Sirve como trazabilidad completa del caso desde su apertura hasta su cierre.

### Acceder al historial completo

1. Abra la incidencia desde **Soporte > Incidencias**.
2. En la pantalla de detalle, el historial aparece en la columna o sección **Actividad**, ordenado de más reciente a más antiguo.
3. Si el historial es extenso, utilice el desplazamiento vertical para ver las actuaciones más antiguas.

---

## Cuándo marcar una incidencia como resuelta

Puede marcar una incidencia como resuelta cuando haya verificado por su cuenta que el problema ha desaparecido y que la operativa ha vuelto a la normalidad. No espere a recibir confirmación del equipo de soporte si ya ha comprobado que todo funciona correctamente.

### Pasos para marcar como resuelta

1. Abra la incidencia desde **Soporte > Incidencias**.
2. Pulse el botón **Marcar como resuelta** en la parte superior derecha del detalle.
3. El sistema le pedirá que confirme la acción y le ofrecerá un campo opcional para añadir una nota de cierre.
4. Confirme. El estado pasará a **Resuelta**.

Transcurridos 7 días naturales desde que una incidencia se marca como Resuelta sin que se haya reabierto, el sistema la cierra automáticamente y pasa al estado **Cerrada**.

---

## Reabrir una incidencia si el problema persiste

Si después de marcar una incidencia como resuelta el mismo problema vuelve a aparecer, no es necesario crear una nueva incidencia. Puede reabrir el caso existente para que el equipo de soporte retome la investigación con todo el contexto previo disponible.

### Pasos para reabrir una incidencia

1. Acceda a **Soporte > Incidencias** y localice la incidencia en estado **Resuelta** o **Cerrada**.
2. Abra el detalle de la incidencia.
3. Pulse el botón **Reabrir incidencia**.
4. En el campo que aparece, describa brevemente por qué está reabriendo el caso: cuándo ha vuelto a aparecer el problema y qué ha cambiado respecto a la situación anterior.
5. Confirme la reapertura.

La incidencia volverá al estado **Abierta** y el equipo de soporte recibirá una notificación automática.

> **Aviso:** Si la reapertura de una incidencia se produce en repetidas ocasiones por el mismo síntoma, es señal de que el problema puede tener una causa raíz más profunda. En ese caso, indíquelo expresamente en el comentario de reapertura para que el equipo de soporte escale la investigación.

---

## Exportar el historial de incidencias para auditoría

CheckBiz360 permite exportar el registro completo de incidencias de su entidad en formato CSV o PDF. Esta función es útil para auditorías internas, revisiones de calidad de servicio o como documentación de soporte ante terceros.

### Pasos para exportar

1. Acceda a **Soporte > Incidencias**.
2. Aplique los filtros que desee: rango de fechas, estado, prioridad o empleado afectado.
3. Pulse el botón **Exportar** en la barra de herramientas superior.
4. Seleccione el formato de exportación: **CSV** para trabajar con los datos en una hoja de cálculo, o **PDF** para un documento de solo lectura.
5. Confirme. El archivo se descargará automáticamente en su dispositivo.

El archivo exportado incluye: número de incidencia, fecha de apertura, tipo, prioridad, estado, empleado afectado, sucursal y resumen de actuaciones.

---

## Nota de rol

Este artículo está dirigido a **Owner** y **Manager**. Solo estos roles tienen acceso al módulo de incidencias en el backoffice y pueden gestionar los estados, comentarios y exportaciones descritos en este artículo.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una incidencia](./85-crear-una-incidencia.md) | Cómo abrir una nueva incidencia y asignar su prioridad |
| [Contactar con soporte técnico](./87-contactar-con-soporte-tecnico.md) | Canales de soporte y tiempos de respuesta orientativos |
| [Problemas frecuentes y soluciones](./88-problemas-frecuentes-y-soluciones.md) | FAQ técnica con las situaciones más habituales |
| [Exportar a Excel y CSV](../11-informes-y-exportacion/78-exportar-a-excel-y-csv.md) | Formatos de exportación disponibles en la plataforma |

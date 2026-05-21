# Trazabilidad e historial de cambios

Cada fichaje en CheckBiz360 lleva asociado un registro completo e inmutable de todas las modificaciones que se han realizado sobre él desde su creación. Este historial de cambios es la base del sistema de auditoría del control de asistencia y permite demostrar, ante cualquier inspección o revisión interna, quién realizó cada cambio, cuándo y sobre qué datos.

---

## Qué es el historial de cambios

El historial de cambios es un registro vinculado a cada registro de asistencia que almacena de forma cronológica todas las intervenciones que han modificado ese registro. Cada elemento representa una acción concreta y contiene toda la información necesaria para reconstruir el historial completo del fichaje.

A diferencia de otros datos del sistema que pueden editarse, el historial de cambios es **inmutable**. Las entradas no pueden modificarse ni eliminarse una vez registradas. Esto garantiza la integridad del historial y su validez como evidencia documental.

---

## Estructura de cada entrada del historial

Cada registro en el historial de cambios contiene los siguientes campos:

| Campo | Descripción |
|---|---|
| `id` | Identificador único de la entrada de auditoría |
| Fecha y hora | Timestamp exacto del momento en que se realizó el cambio |
| Acción | Tipo de modificación realizada (ver tabla de acciones) |
| UID del usuario | Identificador del usuario que ejecutó la acción |
| Estado anterior | Datos del registro antes del cambio |
| Estado nuevo | Datos del registro tras el cambio |

### Tipos de acción registrados

| Acción | Significado |
|---|---|
| `created` | Creación del fichaje original por el empleado |
| `updated` | Modificación de un dato del fichaje por un responsable |
| `manual_request_created` | Creación de jornada completa manual (Modo A) |
| `manual_checkout_created` | Creación de checkout manual sobre checkin abierto (Modo B) |

---

## Por qué el historial es inmutable

La inmutabilidad del historial de cambios responde a dos necesidades fundamentales:

**Integridad del dato:** Una vez que se registra una acción, no puede alterarse. Esto significa que el historial refleja fielmente lo que ocurrió, sin posibilidad de reescritura posterior.

**Validez probatoria:** En el ámbito laboral, los registros de control horario tienen valor como evidencia ante la Inspección de Trabajo. Un historial inmutable y trazable es la garantía de que el dato no ha sido manipulado tras el hecho. Si se modifica un fichaje con posterioridad, el historial muestra tanto el dato original como el modificado, y quién realizó el cambio.

---

## Cómo ver el historial de cambios de un fichaje

1. Acceda al backoffice con rol **manager** u **owner**.
2. Navegue a la sección **Asistencia** del empleado correspondiente.
3. Seleccione el fichaje o jornada cuyo historial desea revisar.
4. Abra la pestaña o sección **Historial de cambios** o **Auditoría**.
5. El sistema mostrará todas las entradas del historial de cambios en orden cronológico, con los detalles de cada acción.

Cada entrada muestra el nombre o identificador del usuario que realizó el cambio, la fecha y hora exacta, la acción ejecutada y los valores anteriores y posteriores de los campos modificados.

---

## Caso de uso legal: inspección de trabajo

Ante una inspección laboral, la empresa puede necesitar demostrar que los registros de asistencia son íntegros, no han sido alterados de forma fraudulenta y reflejan fielmente la jornada real de los empleados.

Con CheckBiz360, el responsable puede acceder al historial de cualquier fichaje y mostrar:

- Quién registró el fichaje originalmente y desde qué dispositivo.
- Si un responsable realizó alguna modificación posterior, cuándo y con qué motivo.
- Si el empleado validó o rechazó alguna jornada manual.
- Qué datos tenía el registro antes y después de cualquier cambio.

Esta trazabilidad completa cubre los requisitos de conservación y transparencia exigidos por la normativa de registro horario vigente.

---

## Exportación del historial para auditorías

El historial de cambios puede exportarse desde el backoffice para su uso en auditorías internas o ante requerimientos de la Inspección de Trabajo.

1. Desde la vista de asistencia o desde el informe de auditoría, seleccione el rango de fechas y los empleados a incluir.
2. Elija el formato de exportación disponible (PDF, CSV u otros según la configuración de la entidad).
3. Descargue el archivo generado.

El documento exportado incluye, para cada registro, tanto los datos del fichaje como el historial completo de intervenciones.

---

> **Nota de conformidad:** La legislación española (Real Decreto-ley 8/2019) obliga a las empresas a conservar los registros de jornada durante cuatro años y a ponerlos a disposición de la Inspección de Trabajo cuando sean requeridos. El sistema de trazabilidad de CheckBiz360 está diseñado para dar cumplimiento a este requisito.

---

## Roles con acceso a esta funcionalidad

La consulta del historial de cambios está disponible para roles **manager** u **owner**. Los empleados no tienen acceso directo al historial técnico de auditoría, aunque sí pueden ver el estado actual de sus fichajes y las notificaciones de cambios que les afectan.

---

## Artículos relacionados

- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
- [Revisión y validación de fichajes](20-revision-y-validacion-de-fichajes.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)
- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)

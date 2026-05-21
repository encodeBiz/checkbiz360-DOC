# Crear una incidencia en CheckBiz360

Cuando un problema técnico o funcional no puede resolverse de forma inmediata mediante las opciones disponibles en el backoffice, el siguiente paso es abrir una incidencia formal. El sistema de incidencias de CheckBiz360 permite registrar, clasificar y dar seguimiento a cualquier problema que afecte al funcionamiento de la plataforma, asegurando que el equipo de soporte reciba la información necesaria para resolverlo con la mayor rapidez posible.

---

## Qué es una incidencia

Una incidencia es el reporte formal de un problema técnico o funcional que impide o dificulta el uso correcto de CheckBiz360 y que requiere intervención del equipo de soporte o de un administrador con permisos avanzados. Las incidencias quedan registradas en el sistema, tienen estados definidos y generan notificaciones automáticas a los responsables designados.

### Diferencia entre una incidencia y una solicitud de jornada manual

Es importante distinguir entre ambos conceptos antes de abrir un registro:

- **Incidencia**: problema del sistema o de la plataforma. Por ejemplo: un empleado no puede fichar porque la app devuelve un error persistente, o el backoffice muestra datos incorrectos que no se corrigen al recargar.
- **Solicitud de jornada manual**: corrección de datos de asistencia. Por ejemplo: un empleado olvidó hacer checkout y es necesario registrar la hora de salida de forma retroactiva. Esta acción se gestiona desde la sección de control horario del backoffice, no a través del módulo de incidencias.

Si el problema es que los datos de un fichaje están mal pero el sistema funciona con normalidad, utilice la opción de jornada manual. Si el problema es que el sistema no permite fichar o muestra un comportamiento anómalo, abra una incidencia.

---

## Cómo crear una incidencia desde el backoffice

### Paso 1: Acceder al módulo de soporte

1. Inicie sesión en el backoffice de CheckBiz360 con su cuenta de Owner o Manager.
2. En el menú lateral izquierdo, seleccione **Soporte**.
3. Haga clic en **Incidencias**.
4. Pulse el botón **Nueva incidencia** en la esquina superior derecha.

### Paso 2: Completar el formulario de incidencia

El formulario de nueva incidencia contiene los siguientes campos:

1. **Tipo de incidencia**: seleccione la categoría que mejor describe el problema. Las opciones disponibles son:
   - Problema de fichaje (checkin / checkout)
   - Error en la aplicación móvil
   - Problema de acceso o autenticación
   - Error en el backoffice
   - Problema con documentos
   - Notificaciones no recibidas
   - Otro

2. **Descripción del problema**: explique con detalle qué ocurrió, cuándo ocurrió por primera vez y con qué frecuencia se reproduce. Cuanto más precisa sea la descripción, más rápida será la resolución.

3. **Empleado afectado**: seleccione el empleado o los empleados que experimentan el problema. Si el problema afecta a toda la organización, indíquelo explícitamente en la descripción.

4. **Sucursal**: indique la sucursal donde se ha detectado el problema. Si afecta a varias sucursales, seleccione la más representativa e indique las demás en la descripción.

5. **Capturas de pantalla adjuntas**: adjunte imágenes del error cuando sea posible. Los formatos admitidos son JPG, PNG y PDF, con un tamaño máximo de 10 MB por archivo. Las capturas deben mostrar el mensaje de error completo, incluyendo el código si aparece en pantalla.

### Paso 3: Asignar la prioridad

Antes de enviar la incidencia, seleccione la prioridad que corresponde al impacto real del problema en su operativa:

| Prioridad | Criterio |
|---|---|
| Critica | El problema impide completamente el fichaje de todos o la mayoría de los empleados, o bloquea el acceso al backoffice para el Owner |
| Alta | El problema afecta a un grupo significativo de empleados o impide una función esencial como la gestión de documentos o la generación de informes |
| Media | El problema afecta a un empleado concreto o a una función secundaria, pero existe una alternativa temporal |
| Baja | El problema es menor, cosmético o no interfiere con la operativa diaria |

> **Aviso:** La prioridad que usted asigna es una orientación para el equipo de soporte, pero CheckBiz360 puede reclasificarla en función del análisis técnico. Una incidencia marcada como crítica que al investigarse resulta ser un problema de configuración local puede pasar a prioridad media.

### Paso 4: Enviar la incidencia

1. Revise todos los campos antes de enviar.
2. Pulse **Crear incidencia**.
3. La incidencia quedará registrada en el sistema y el equipo de soporte de CheckBiz360 recibirá una notificación inmediata con todos los detalles enviados.

---

## A quién se notifica automáticamente

En el momento de crear una incidencia, el sistema envía notificaciones automáticas a:

- El **Owner de la entidad** que ha abierto la incidencia.
- El **equipo de soporte de CheckBiz360** (hola@encodebiz.com), que recibirá la incidencia con todos los detalles adjuntos.
- Si la incidencia fue creada por un Manager, también se notifica al Owner de la entidad.

El empleado afectado no recibe notificación automática salvo que el Manager decida informarle por sus propios canales.

---

> **Aviso:** No abra incidencias duplicadas por el mismo problema. Si ya existe una incidencia abierta para el mismo error, añada un comentario en esa incidencia con la nueva información. La duplicidad de registros puede ralentizar la resolución.

---

## Nota de rol

Este artículo está dirigido a **Owner** y **Manager**. Solo estos roles tienen acceso al módulo de incidencias en el backoffice. Los empleados con rol Worker o Supervisor que detecten un problema deben comunicarlo a su Manager para que este abra la incidencia correspondiente.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Seguimiento y resolución de incidencias](./86-seguimiento-y-resolucion-de-incidencias.md) | Estados, comentarios e historial de una incidencia |
| [Contactar con soporte técnico](./87-contactar-con-soporte-tecnico.md) | Canales de soporte y tiempos de respuesta |
| [Problemas frecuentes y soluciones](./88-problemas-frecuentes-y-soluciones.md) | FAQ técnica con las situaciones más habituales |
| [Solicitar una jornada manual](../03-control-horario/27-solicitar-jornada-manual.md) | Cómo corregir un fichaje incorrecto o ausente |

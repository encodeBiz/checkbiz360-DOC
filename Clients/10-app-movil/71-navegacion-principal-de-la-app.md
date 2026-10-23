# Navegación principal de la app

Una vez que ha iniciado sesión en CheckBiz360, encontrará una interfaz organizada en secciones bien diferenciadas. Este artículo describe la estructura general de la aplicación, para que pueda localizarcon facilidad cada función y aprovechar al máximo las herramientas disponibles.

---

## Estructura general de la aplicación

La navegación principal de CheckBiz360 se organiza a través de una barra de navegación inferior que agrupa las cinco áreas fundamentales de la experiencia del empleado:

1. **Fichaje** — pantalla de inicio y centro de la experiencia.
2. **Mis registros** — historial personal de asistencia.
3. **Documentos** — documentos laborales del empleado.
4. **Tareas** — tareas asignadas por el manager.
5. **Perfil** — configuración personal y seguridad.

Puede desplazarse entre estas secciones pulsando el icono correspondiente en la barra inferior en cualquier momento.

---

## Sección Fichaje

La pantalla de fichaje es la primera que aparece al iniciar sesión y constituye el núcleo de la aplicación. Desde ella puede:

- Registrar su entrada (check-in) al inicio de la jornada.
- Registrar pausas intermedias cuando corresponda.
- Registrar su salida (check-out) al finalizar la jornada.
- Consultar el estado de su fichaje actual (dentro o fuera del turno).

La pantalla muestra la hora actual, la sucursal o punto de trabajo asociado y, en caso de requerir validación por GPS, el estado de su ubicación en relación con el radio permitido.

Desde la versión 1.3.2, la pantalla se organiza en tarjetas:

- **Tarjeta de control**, con el botón de fichaje que corresponde a cada momento y dos cronómetros: el de la **jornada**, que empieza con la entrada y no se detiene durante los descansos, y el de **descanso**, que suma todos los descansos del día. Se calculan a partir de los fichajes válidos, así que reflejan también las correcciones hechas desde el backoffice.
- **Información laboral**: sucursal, horario del día —un turno por línea— y descanso. Con descanso estricto se muestran los minutos; con descanso flexible, «Flexible».
- **Tareas de hoy**.

Si hoy no es día laborable para el empleado, la tarjeta lo indica —distinguiendo un festivo de un día libre— y el fichaje explica por qué no se puede fichar y que, si trabajó, puede pedir una jornada manual. **Desde la versión 1.10.0**, la casilla del horario dice **No laborable** y debajo de las cifras del día sale el motivo en una etiqueta destacada: «Vacaciones», «Permiso» o el nombre del festivo, tal y como se llama ese día en el calendario. Ver [Festivos y días no laborables](../04-calendario-y-horarios/29-festivos-y-dias-no-laborables.md).

### Mi calendario

**Desde la versión 1.10.0**, el menú lateral tiene, dentro de **Herramientas**, la opción **Mi calendario**: el mes de la persona, con los días de trabajo, los libres, los festivos y sus ausencias. Desde ahí pide vacaciones o un permiso, y recibe un aviso cuando la empresa lo aprueba o lo rechaza. Ver [Vacaciones y permisos desde la app](../04-calendario-y-horarios/115-vacaciones-y-permisos-desde-la-app.md).

> **Aviso:** Para realizar un fichaje es imprescindible contar con conexión a internet activa y el GPS habilitado. Sin estos elementos, el fichaje no podrá completarse.

---

## Sección Mis registros

En esta sección encontrará el historial completo de sus fichajes registrados en la plataforma. Desde aquí puede:

- Consultar entradas, salidas y pausas por fecha.
- Filtrar los registros por sucursal o por tipo de evento.
- Ver el detalle de cada registro: hora exacta, estado (válido o fallido), distancia al radio de la sucursal y método de validación utilizado.
- Solicitar la corrección de un registro o el alta de una jornada manual si se diera el caso.

---

## Sección Documentos

La sección de documentos centraliza todos los archivos laborales que su organización le ha compartido a través de CheckBiz360. Aquí encontrará:

- Nóminas, contratos, comunicados internos y cualquier otro documento que el administrador haya publicado para usted.
- La posibilidad de consultar los documentos directamente desde la app o descargarlos en su dispositivo.
- El estado de acuse de recibo de cada documento, cuando aplique.

---

## Sección Tareas

La sección de tareas muestra las actividades que le han sido asignadas por su manager o administrador. Desde aquí puede:

- Consultar el listado de tareas asignadas con su estado y su prioridad.
- Ver el detalle de cada tarea: descripción, fecha límite, fecha prevista de inicio y evidencias.
- Ver el **lugar de trabajo**, si la tarea tiene uno propio, y abrirlo con **Ver en Maps**. Antes de iniciar, la app calcula la distancia y avisa si está lejos; quien decide es el servidor.
- Iniciar una tarea, **pausarla y reanudarla** (desde la versión 1.4.0), añadir notas de progreso, subir evidencias en foto o vídeo y marcarla como completada. Iniciar, reanudar y completar requieren tener la jornada fichada.
- **Desde la versión 1.6.0**, iniciar, pausar, reanudar y completar están también en la propia tarjeta de la lista y en la tarjeta **Tareas de hoy** de la pantalla de asistencia, sin entrar en el detalle. Solo aparecen en las tareas propias, y completar pide confirmación.
- **Buscar por sucursal o por trabajador** en los filtros: los buscadores muestran opciones nada más tocarlos, sin escribir nada.
- Consultar el **tiempo invertido**, el total de pausas y el **historial** de la tarea (desde la versión 1.4.0).

La **descripción se muestra con su formato**: los títulos, las listas y las listas de comprobación que el responsable escribió desde el backoffice se ven como tales, no como texto plano con símbolos. Las casillas de una lista de comprobación son una guía de trabajo: se leen, pero no se marcan desde la app, porque forman parte del texto de la tarea y no de su estado. Los enlaces se abren en el navegador del dispositivo.

### Qué ve un supervisor en la lista

Quien tiene gente a cargo ve en la misma lista sus tareas y las de su equipo. **Desde la versión 1.6.0** salen separadas: arriba **Mis tareas**, en una sección que se puede plegar, y debajo **Tareas del equipo**. Las propias llevan además una marca junto al título, y son las únicas con botones de acción en la tarjeta. En **Tareas de hoy**, las propias salen primero.

Un empleado sin gente a cargo no ve ninguna de estas separaciones: todas las tareas de su lista son suyas.

> **Aviso:** actualizar el estado de una tarea requiere conexión a internet.

---

## Sección Perfil

La sección de perfil le permite gestionar su información personal y las preferencias de seguridad de su cuenta. Desde aquí puede:

- Consultar y actualizar sus datos de contacto.
- Cambiar su contraseña de acceso.
- Configurar la autenticación en dos pasos (2FA).
- Activar el acceso biométrico (huella dactilar o reconocimiento facial) si su dispositivo y la configuración de su organización lo permiten.
- Gestionar las preferencias de notificaciones push.

---

## Pantalla de notificaciones

CheckBiz360 incluye un centro de notificaciones accesible desde el icono de campana o aviso que aparece en la parte superior de la pantalla. En este espacio encontrará:

- Alertas sobre nuevos documentos publicados.
- Notificaciones de tareas asignadas o próximas a vencer.
- Comunicados del sistema o de su organización.

Las notificaciones no leídas se indican con un contador numérico sobre el icono. Pulse sobre cualquier notificación para acceder directamente al contenido relacionado.

---

## Navegación entre secciones

Para moverse entre las distintas áreas de la aplicación:

1. Localice la barra de navegación inferior de la pantalla.
2. Pulse el icono de la sección a la que desea acceder.
3. La sección se cargará inmediatamente, conservando su posición en la sección anterior para que pueda regresar con facilidad.

Desde cualquier sección puede volver a la pantalla de fichaje pulsando el icono central de la barra de navegación, que actúa como acceso directo prioritario.

---

## Nota de rol

Este artículo está dirigido a **empleados** que utilizan la app CheckBiz360 en su día a día. La estructura y las secciones descritas son las que corresponden al rol de empleado estándar; los roles de manager o administrador pueden tener acceso a secciones adicionales en el portal web.

---

## Artículos relacionados

- [Primer inicio de sesión](70-primer-inicio-de-sesion.md)
- [Configuración de perfil en la app](72-configuracion-de-perfil-en-la-app.md)
- [Mis registros de asistencia](73-mis-registros-de-asistencia.md)
- [Uso sin conexión](74-uso-sin-conexion.md)

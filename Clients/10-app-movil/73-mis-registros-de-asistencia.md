# Mis registros de asistencia

La sección "Mis registros" de CheckBiz360 le permite consultar el historial completo de su actividad de fichaje desde la propia aplicación móvil. Este artículo explica cómo acceder a su historial, qué información contiene cada registro, cómo interpretar los estados y qué hacer en caso de detectar un error.

---

## Acceder a la sección de registros

1. Abra CheckBiz360 e inicie sesión con su cuenta.
2. Pulse el icono **Mis registros** en la barra de navegación inferior (representado habitualmente por un icono de lista o historial).
3. Se cargará el listado de sus registros de asistencia, ordenados cronológicamente del más reciente al más antiguo.

---

## Filtros disponibles

Para facilitar la localización de registros concretos, la aplicación ofrece varios filtros que puede combinar entre sí:

### Filtro por fecha

1. Pulse el icono de filtro o el selector de fechas en la parte superior de la pantalla.
2. Seleccione una fecha concreta o un rango de fechas (fecha de inicio y fecha de fin).
3. Pulse **Aplicar** para actualizar el listado con los resultados correspondientes.

### Filtro por sucursal

1. Dentro de las opciones de filtro, localice el selector de **Sucursal** o **Centro de trabajo**.
2. Seleccione la sucursal deseada de la lista disponible.
3. El listado mostrará únicamente los registros asociados a esa sucursal.

### Filtro por tipo de evento

Cada registro está clasificado según el tipo de acción realizada:

- **Check-in**: entrada al inicio de la jornada.
- **Check-out**: salida al finalizar la jornada.
- **Pausa**: inicio de una pausa intermedia.
- **Fin de pausa**: reanudación de la actividad tras una pausa.

Puede filtrar el listado para mostrar únicamente uno o varios de estos tipos seleccionándolos en el selector correspondiente.

---

## Detalle de cada registro

Al pulsar sobre cualquier registro del listado, accederá a la vista de detalle que incluye la siguiente información:

| Campo | Descripción |
|-------|-------------|
| Fecha y hora exacta | Marca de tiempo del momento en que se realizó el fichaje |
| Tipo | Check-in, check-out, pausa o fin de pausa |
| Sucursal | Nombre del centro de trabajo asociado al fichaje |
| Estado | Válido o fallido |
| Distancia al radio | Distancia en metros entre su posición y el perímetro permitido de la sucursal (si aplica) |
| Método de validación | GPS, WiFi, manual u otro método configurado por su organización |

---

## Interpretación de los estados

### Registro válido

Un registro con estado **Válido** indica que el fichaje fue aceptado correctamente por el sistema. Cumplía todos los requisitos de validación en el momento en que se realizó (ubicación dentro del radio permitido, horario autorizado, etc.).

### Registro fallido

Un registro con estado **Fallido** indica que el sistema intentó procesar el fichaje pero no pudo validarlo correctamente. Las causas más frecuentes son:

- El empleado se encontraba fuera del radio de geolocalización permitido para la sucursal.
- El GPS del dispositivo no tenía precisión suficiente en ese momento.
- Se produjo un error de conectividad durante la transmisión del fichaje.
- El intento de fichaje se realizó fuera del horario autorizado para ese turno.

> **Aviso:** Un fichaje fallido no cuenta como presencia registrada. Si detecta registros fallidos que no corresponden a un error real de su parte, debe comunicarlo a su manager para que revise la situación.

---

## Qué hacer si detecta un fichaje fallido o incorrecto

Si identifica en su historial un registro fallido o un fichaje que no se corresponde con su actividad real (por ejemplo, una entrada o salida que no fue registrada), puede iniciar una solicitud de corrección desde la propia aplicación:

1. Pulse sobre el registro afectado para abrir su vista de detalle.
2. Localice la opción **Solicitar corrección** o **Reportar incidencia** y púlsela.
3. Indique el motivo de la solicitud y, si es posible, la hora real en la que debería haberse registrado el fichaje.
4. Añada cualquier comentario adicional que considere relevante para que su manager pueda valorar la solicitud.
5. Pulse **Enviar solicitud**.

El manager o administrador recibirá una notificación con su solicitud y podrá aprobarla, denegarla o solicitar información adicional.

---

## Solicitar una jornada manual desde la app

Si en un día determinado no pudo realizar ningún fichaje (por ejemplo, por fallo del dispositivo o ausencia de conectividad durante toda la jornada), puede solicitar el alta de una jornada manual:

1. En la sección "Mis registros", localice el día sin registros o pulse el botón **Nueva solicitud manual** si está disponible en la pantalla.
2. Indique la fecha, hora de entrada y hora de salida correspondientes.
3. Seleccione la sucursal en la que trabajó ese día.
4. Añada una justificación o motivo de la ausencia de fichaje automático.
5. Pulse **Enviar**.

> **Aviso:** Las solicitudes de jornada manual no son aprobadas automáticamente. Requieren la revisión y aprobación de su manager o administrador. La jornada no se considerará válida hasta que el responsable la apruebe en el sistema.

---

## Nota de rol

Este artículo está dirigido a **empleados** que consultan su historial de asistencia desde la app. Los managers y administradores pueden consultar los registros de todos los empleados desde el portal web, con opciones de filtrado y exportación adicionales.

---

## Artículos relacionados

- [Navegación principal de la app](71-navegacion-principal-de-la-app.md)
- [Uso sin conexión](74-uso-sin-conexion.md)
- [Configuración de perfil en la app](72-configuracion-de-perfil-en-la-app.md)

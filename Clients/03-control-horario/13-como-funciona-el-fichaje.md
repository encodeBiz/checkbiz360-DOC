# Cómo funciona el fichaje en CheckBiz360

El fichaje en CheckBiz360 no es un simple marcado de hora. Cada vez que un empleado registra su entrada o salida, el sistema ejecuta un proceso de validación en tres capas que garantiza la integridad del dato, la coherencia con el turno activo y la identidad del dispositivo utilizado. Este artículo explica cómo funciona ese proceso de principio a fin.

---

## Las tres capas de validación

Cuando un empleado pulsa el botón de fichaje, el sistema evalúa de forma secuencial tres condiciones. Si alguna de ellas no se cumple, el fichaje queda registrado como fallido con un código de error específico que indica la causa exacta.

### Capa 1 — Geolocalización

El sistema obtiene las coordenadas GPS del dispositivo en el momento del fichaje y las compara con la ubicación de la sucursal asignada al empleado. Cada sucursal tiene configurado un radio de fichaje (expresado en metros). Si el empleado se encuentra fuera de ese radio, el fichaje se rechaza con el código `checklog/out_of_radius`.

La distancia real entre el empleado y el centro de la geocerca queda registrada en el sistema para análisis posterior. Esto permite al responsable revisar si el radio está bien dimensionado o si existe un patrón de intentos de fichaje desde ubicaciones incorrectas.

Si el empleado tiene activada la opción **Trabajo fuera del centro** (antes llamada *Trabajo remoto*), esta capa de validación se omite por completo: la geocerca no se aplica a esa persona.

### Capa 2 — Horario efectivo

Una vez validada la ubicación, el sistema comprueba que el fichaje se realiza dentro del turno activo del empleado para ese día, según su calendario efectivo.

El fichaje siempre guarda la **hora real**. Lo que decide si el tiempo trabajado fuera de la franja oficial se computa o no es la **modalidad de jornada** del calendario: con jornada estricta no se contabiliza; con jornada flexible se suma como tiempo extra. Consulte [Jornada estricta y jornada flexible](../04-calendario-y-horarios/28-horario-flexible.md).

Si el fichaje se realiza fuera del turno activo, el sistema lo rechaza con el código `checklog/out_of_schedule`.

### Capa 3 — Dispositivo y biometría

La tercera capa verifica la identidad del dispositivo y, si aplica, la biometría del empleado.

Si el empleado tiene activada la autenticación de doble factor (2FA), solo puede fichar desde dispositivos que hayan sido previamente registrados como dispositivos de confianza. Intentar fichar desde un dispositivo no registrado genera el error `auth/untrusted_device`.

Si la configuración del empleado o de la sucursal tiene activa la verificación biométrica, el empleado debe completar la verificación biométrica (huella dactilar o reconocimiento facial según el dispositivo) antes de que el fichaje se procese.

---

## Resultado del fichaje

Una vez superadas las tres capas de validación, el fichaje queda registrado con estado `valid`. Este estado indica que el registro es correcto, coherente con el turno y autenticado.

Si alguna capa falla, el fichaje se registra con estado `failed` y el código de error correspondiente. Un punto importante: **los fichajes fallidos también se almacenan en el sistema**. No se descartan. Quedan disponibles para auditoría, análisis de incidencias y revisión por parte del responsable.

| Estado tras el fichaje | Significado |
|---|---|
| `valid` | Todas las validaciones superadas. Jornada activa. |
| `failed` | Una o más validaciones fallaron. Código de error disponible. |

---

## Diferencia entre fichaje válido y fichaje fallido

La distinción es importante para la gestión de nómina y cumplimiento normativo. Un fichaje válido cuenta como tiempo trabajado dentro de la jornada. Un fichaje fallido queda registrado para auditoría pero no computa horas.

Cuando un empleado acumula fichajes fallidos reiterados, el responsable puede revisar el patrón desde el backoffice y determinar si se trata de un problema de configuración (radio demasiado pequeño, horario mal asignado) o de una incidencia que requiere atención.

Si un empleado no pudo fichar por causas justificadas, el responsable puede crear una solicitud de jornada manual para registrar la asistencia de forma retroactiva.

---

> **Nota sobre auditoría:** Todos los fichajes, tanto válidos como fallidos, quedan almacenados con su timestamp original, los datos de validación (coordenadas, distancia, dispositivo) y el resultado de cada capa. Este registro es inmutable y puede ser consultado ante inspecciones de trabajo.

---

## Roles con acceso a esta funcionalidad

La configuración de las capas de validación (zona de chequeo, biometría, 2FA) es gestionada por usuarios con rol **owner** o **manager**. Los empleados interactúan con el sistema de fichaje desde la app móvil sin necesidad de configurar nada.

---

## Artículos relacionados

- [Check-in y check-out desde la app](14-checkin-checkout-desde-app.md)
- [Trabajo fuera del centro](15-fichaje-en-remoto.md)
- [Geocercas y radio de fichaje](16-geocercas-radio-de-fichaje.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)

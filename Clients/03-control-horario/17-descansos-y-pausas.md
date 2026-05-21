# Descansos y pausas

CheckBiz360 permite registrar los períodos de descanso dentro de la jornada laboral de forma precisa. Las pausas se diferencian del fin de jornada porque no cierran el turno activo: el empleado sigue estando en jornada, pero el tiempo de pausa se descuenta del cómputo de horas trabajadas. Este artículo explica cómo funcionan las pausas, cómo registrarlas y cómo configurarlas por sucursal.

---

## Tipos de evento de pausa

El sistema utiliza dos tipos de fichaje específicos para gestionar las pausas:

- **Restin (`restin`):** Marca el inicio de una pausa. El empleado abandona temporalmente su puesto de trabajo.
- **Restout (`restout`):** Marca la finalización de la pausa. El empleado retoma su actividad.

Ambos eventos quedan registrados en el historial de asistencia del empleado con su timestamp correspondiente, igual que los eventos de entrada y salida.

---

## Diferencia entre pausa y fin de jornada

La distinción es importante para el cálculo de horas:

| Evento | Efecto en la jornada |
|---|---|
| `restin` (inicio de pausa) | La jornada sigue abierta. El tiempo de pausa empieza a contabilizarse. |
| `restout` (fin de pausa) | La jornada continúa. El tiempo de pausa queda cerrado y se descuenta. |
| `checkout` (salida) | La jornada se cierra definitivamente. |

Si el empleado registra un `checkout` sin haber cerrado una pausa activa con `restout`, el sistema puede marcar la jornada como incompleta o con incidencia, según la configuración de la sucursal.

---

## Cómo registrar una pausa desde la app

### Iniciar una pausa (restin)

1. En la pantalla de asistencia, pulse el botón **Iniciar pausa**.
2. Confirme la acción si el sistema lo solicita.
3. La app mostrará que el empleado está en pausa y registrará la hora de inicio.

### Finalizar una pausa (restout)

1. En la pantalla de asistencia, pulse el botón **Finalizar pausa**.
2. La app confirmará la reanudación de la jornada y mostrará el tiempo de pausa transcurrido.

La pantalla principal de asistencia refleja en todo momento si el empleado está en jornada activa o en pausa.

---

## Las pausas en el historial de asistencia

Cada evento de pausa queda almacenado en el historial de asistencia del empleado con:

- Tipo de evento (`restin` o `restout`).
- Timestamp exacto del registro.
- Estado de validación (válido o fallido).
- Datos de geolocalización si aplica la validación de geocerca.

El responsable puede consultar el detalle de pausas de cualquier empleado desde el backoffice, incluyendo la duración total de pausas por jornada.

---

## Configuración de pausas por sucursal

Las pausas pueden configurarse con distintos parámetros a nivel de sucursal:

### Deshabilitar pausas

Si la operativa de la sucursal no contempla pausas registradas, es posible desactivar esta funcionalidad mediante la opción "desactivar pausas". Cuando está activo, los botones de pausa no aparecen en la app para los empleados de esa sucursal y los eventos `restin`/`restout` no se procesan.

### Duración estándar de pausa

El campo "duración estándar de pausa" permite definir una duración estándar de pausa en minutos. Este valor se utiliza como referencia para el cálculo automático de pausas y puede emplearse en los informes para comparar la duración real de los descansos frente al tiempo estándar establecido.

Para configurar estos parámetros:

1. Acceda al backoffice con rol **manager** u **owner**.
2. Navegue a **Sucursales** y seleccione la sucursal correspondiente.
3. Abra la sección de configuración de asistencia.
4. Ajuste los campos "desactivar pausas" y "duración estándar de pausa" según sus necesidades.
5. Guarde los cambios.

---

## Descuento automático de pausas en el cálculo de horas

El sistema descuenta automáticamente el tiempo de pausa del total de horas trabajadas en la jornada. El cálculo es el siguiente:

**Horas trabajadas = (hora de checkout - hora de checkin) - tiempo total de pausas**

Si el empleado ha realizado varias pausas durante la jornada, el sistema suma la duración de todas ellas y las descuenta del total. Este cálculo queda disponible en los informes de asistencia y en el resumen de jornada del empleado.

> **Aviso:** Si un empleado inicia una pausa con `restin` pero no la cierra con `restout` antes de registrar el checkout, el sistema puede registrar la pausa como no finalizada. En estos casos, el responsable debe revisar y corregir manualmente la jornada desde el backoffice.

---

## Roles con acceso a esta funcionalidad

El registro de pausas desde la app es una acción disponible para todos los usuarios con rol **empleado**. La configuración de pausas por sucursal ("desactivar pausas", "duración estándar de pausa") requiere rol **manager** u **owner**.

---

## Artículos relacionados

- [Check-in y check-out desde la app](14-checkin-checkout-desde-app.md)
- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)
- [Solicitar jornada manual](19-solicitar-jornada-manual.md)

# Check-in y check-out desde la app

La app móvil de CheckBiz360 es el punto de entrada principal para el registro de asistencia. Este artículo explica paso a paso cómo realizar un check-in (entrada) y un check-out (salida) desde la aplicación, qué información muestra la pantalla principal de asistencia y cómo interpretar los mensajes de error más habituales.

---

## La pantalla principal de asistencia

Al abrir la app y seleccionar la entidad de trabajo, el empleado accede a la pantalla de asistencia. Esta pantalla muestra en tiempo real:

- **Estado actual:** si el empleado está dentro o fuera de su jornada activa.
- **Hora del último fichaje:** la hora exacta del último evento registrado (entrada, salida o pausa).
- **Sucursal activa:** el nombre y la ubicación de la sucursal asignada para ese turno.
- **Tipo de fichaje disponible:** la app muestra únicamente la acción que corresponde al estado actual. Si el empleado no ha fichado entrada, aparece el botón de check-in. Si ya ha fichado entrada, aparece el botón de check-out o pausa según corresponda.

Esta pantalla se actualiza automáticamente cuando se produce un cambio de estado.

---

## Cómo realizar un check-in (entrada)

1. Abra la aplicación CheckBiz360 en su dispositivo móvil.
2. Inicie sesión con sus credenciales si aún no lo ha hecho.
3. Seleccione la entidad de trabajo correspondiente.
4. En la pantalla de asistencia, pulse el botón **Registrar entrada**.
5. Si su dispositivo requiere verificación biométrica, confirme su identidad mediante huella dactilar o reconocimiento facial cuando el sistema lo solicite.
6. La app solicitará permiso de ubicación si aún no lo ha concedido. Debe otorgar este permiso para que la validación de geocerca funcione correctamente.
7. El sistema procesa el fichaje. En unos segundos, la pantalla mostrará la confirmación de entrada con la hora registrada.

Si el fichaje es correcto, el estado de la pantalla cambia a "Dentro de jornada" y se muestra la hora de entrada.

---

## Cómo realizar un check-out (salida)

1. En la pantalla de asistencia, pulse el botón **Registrar salida**.
2. Confirme la acción si el sistema lo solicita.
3. Si tiene verificación biométrica activada, complete la autenticación.
4. El sistema procesa el fichaje de salida. La pantalla mostrará la confirmación con la hora de salida y el tiempo total trabajado en la jornada.

> **Importante:** El check-out cierra la jornada activa. Si olvida registrar la salida, la jornada quedará en estado `incomplete_workday` hasta que un responsable la corrija manualmente o el empleado la resuelva desde la pantalla de notificaciones.

---

## Mensajes de error en pantalla

La app muestra mensajes específicos cuando el fichaje no puede procesarse correctamente. A continuación se describen los más habituales:

### Fuera de zona

Aparece cuando el dispositivo está fuera del radio de fichaje definido para la sucursal. La app puede mostrar la distancia aproximada al punto de fichaje autorizado.

**Qué hacer:** Compruebe que se encuentra en las instalaciones correctas. Si trabaja habitualmente en esa ubicación y el error se repite, comuníquelo a su responsable para que revise la configuración del radio.

### Fuera de horario

Aparece cuando el intento de fichaje se realiza fuera del turno activo del empleado.

**Qué hacer:** Revise su turno asignado en la sección de horarios de la app. Si considera que el fichaje es correcto, solicite a su responsable una jornada manual.

### Dispositivo no autorizado

Aparece cuando el dispositivo desde el que se intenta fichar no está registrado como dispositivo de confianza y el empleado tiene activada la autenticación de doble factor.

**Qué hacer:** Contacte con su responsable o con el administrador del sistema para registrar el dispositivo actual como dispositivo de confianza.

---

## Disponibilidad del registro en el backoffice

El fichaje queda disponible en el backoffice de forma inmediata, sin necesidad de sincronización manual. El responsable puede ver el registro en tiempo real desde el panel de asistencia.

Tanto los fichajes válidos como los fallidos quedan almacenados y son visibles en el historial de asistencia del empleado. Los fichajes fallidos incluyen el código de error y los datos técnicos del intento (hora, coordenadas, distancia al radio).

---

> **Nota para responsables:** Si un empleado reporta un error persistente al fichar, acceda al historial de asistencia desde el backoffice y revise el código de error del fichaje fallido. Esto le permitirá identificar si el problema es de configuración (radio, horario, dispositivo) o si requiere una corrección manual.

---

## Roles con acceso a esta funcionalidad

El registro de check-in y check-out desde la app es una acción disponible para todos los usuarios con rol **empleado**. La revisión de fichajes en el backoffice está disponible para roles **manager** y **owner**.

---

## Artículos relacionados

- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)
- [Descansos y pausas](17-descansos-y-pausas.md)
- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)

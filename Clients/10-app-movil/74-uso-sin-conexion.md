# Uso sin conexión

CheckBiz360 está diseñado para funcionar con conexión a internet activa. Las operaciones críticas de la plataforma — en especial el fichaje — requieren validación en tiempo real con los servidores y no pueden realizarse sin conectividad. Sin conexión, la aplicación tiene una funcionalidad muy limitada: únicamente permite consultar los datos que ya estaban cargados en la caché del dispositivo durante sesiones anteriores.

Este artículo explica qué está disponible sin conexión, qué requiere obligatoriamente conectividad y qué está previsto para versiones futuras.

---

## Qué funciona sin conexión (solo consulta de datos en caché)

Cuando no hay conexión disponible, la aplicación permite consultar la información que fue descargada durante sesiones anteriores con conexión activa. Esta información no se actualiza hasta que se restablezca la conectividad.

### Consultar registros de asistencia ya descargados

Puede revisar el historial de fichajes que fue cargado en la última sesión con conexión. La información mostrada corresponde al último estado sincronizado; no verá cambios posteriores a esa sincronización.

### Consultar documentos descargados previamente

Los documentos laborales que ya abrió o descargó mientras tenía conexión (nóminas, contratos u otros archivos de la sección de documentos) permanecen disponibles para su consulta sin conexión.

### Consultar tareas descargadas

Las tareas que fueron cargadas durante la última sesión con conexión pueden consultarse. Podrá ver el detalle de cada tarea, sus archivos adjuntos descargados y su estado en el momento de la última sincronización.

---

## Qué NO funciona sin conexión

Las siguientes funciones requieren obligatoriamente conexión a internet y no están disponibles en modo sin conexión:

### Realizar fichajes

El fichaje (check-in, check-out y pausas) requiere conexión en el momento en que se ejecuta. El sistema necesita validar en tiempo real su identidad, su ubicación GPS en relación con la geocerca del centro, el estado de su turno activo y las reglas de dispositivo autorizado. Ninguna de estas validaciones puede realizarse sin conectividad.

> **Aviso:** Si intenta realizar un fichaje sin conexión, la aplicación le informará de que no es posible completar la operación. No existe una cola de fichajes pendientes: la marca de tiempo del fichaje debe corresponder al momento real en que se produce, y las validaciones no pueden posponerse.

### Descargar nuevos documentos

Si su organización publica un documento mientras usted no tiene conexión, no podrá descargarlo ni visualizarlo hasta que recupere acceso a internet.

### Sincronizar cambios en tareas

Los cambios de estado de tareas (marcar como completada, actualizar progreso) requieren conexión para transmitirse al servidor. Si actualiza una tarea sin conexión, el cambio puede quedar guardado localmente pero no será visible para su manager hasta que se sincronice.

### Iniciar sesión por primera vez en el dispositivo

El proceso de autenticación inicial siempre requiere conexión para verificar las credenciales. Si nunca ha iniciado sesión en ese dispositivo, no podrá acceder a la aplicación sin conectividad.

---

## Modo offline con cola de sincronización

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

En una versión futura, CheckBiz360 incorporará un modo offline robusto con cola de sincronización que permitirá registrar fichajes sin conexión para enviarlos al servidor en cuanto se restablezca la conectividad. Este modo incluirá la validación diferida de las condiciones del fichaje (geocerca, dispositivo, horario) y mecanismos de resolución de conflictos. Por ahora, el fichaje requiere conexión activa en el momento de ejecutarse.

---

## Sincronización al recuperar la conexión

Cuando CheckBiz360 detecta que la conexión se ha restablecido, realiza automáticamente una sincronización en segundo plano para actualizar los datos en caché. No es necesario realizar ninguna acción manual; la aplicación lo hace en cuanto detecta conectividad.

---

## Recomendaciones para entornos con conectividad intermitente

Si trabaja en entornos donde la conexión no es estable, tenga en cuenta lo siguiente:

1. **Realice sus fichajes en cuanto disponga de conexión.** No espere: si tiene señal suficiente, fiche de inmediato.
2. **Abra los documentos con antelación.** Si sabe que necesitará consultar un documento, ábralo cuando tenga conexión para que quede en caché.
3. **Revise las tareas antes de perder la conexión.** Cargue el listado cuando tenga conexión para tener la información disponible después.
4. **Active el WiFi cuando esté disponible.** Una conexión WiFi estable es preferible a datos móviles en entornos con cobertura fluctuante.
5. **Comunique los problemas de conectividad a su manager.** Si los problemas de conexión afectan de forma recurrente a sus fichajes, informe a su manager para que quede constancia y pueda gestionar los registros manualmente.

> **Aviso:** Si un día no pudo realizar ningún fichaje por problemas de conectividad, debe informar a su manager y solicitar el alta de una jornada manual desde la sección "Mis registros". Consulte el artículo sobre registros de asistencia para conocer el procedimiento completo.

---

## Nota de rol

Este artículo está dirigido a **empleados** que utilizan la app en entornos donde la conectividad puede ser limitada o intermitente.

---

## Artículos relacionados

- [Mis registros de asistencia](73-mis-registros-de-asistencia.md)
- [Navegación principal de la app](71-navegacion-principal-de-la-app.md)
- [Actualizaciones de la app](75-actualizaciones-de-la-app.md)

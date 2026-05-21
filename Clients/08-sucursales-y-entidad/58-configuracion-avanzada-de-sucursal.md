# Configuración avanzada de sucursal

Cada sucursal en CheckBiz360 dispone de un bloque de parámetros avanzados que permiten adaptar el comportamiento del sistema a las particularidades operativas de ese centro de trabajo. Estos parámetros complementan la configuración básica (nombre, dirección, radio y zona horaria) y ofrecen un control más fino sobre el registro de asistencia, las pausas y las tolerancias de entrada. Este artículo describe cada parámetro, su valor por defecto, su efecto y las situaciones en las que conviene modificarlo.

## Dónde encontrar la configuración avanzada

1. Acceda al backoffice web y navegue a **Organización** > **Sucursales**.
2. Pulse sobre el nombre de la sucursal o el icono de edición.
3. Desplácese hasta la sección **Configuración avanzada** en la parte inferior del formulario.
4. Active o modifique los parámetros que necesite y pulse **Guardar cambios**.

## Tabla de parámetros avanzados

| Parámetro | Tipo | Valor por defecto | Descripción |
|---|---|---|---|
| Desactivar validación de geocerca | Booleano | Desactivado | Deshabilita la validación por geocerca para esta sucursal |
| Desactivar pausas | Booleano | Desactivado | Deshabilita el registro de pausas para esta sucursal |
| Duración estándar de pausa | Entero (minutos) | 30 | Duración estándar de la pausa cuando el empleado no registra inicio y fin manualmente |
| Tolerancia de entrada | Entero (minutos) | 0 | Minutos de tolerancia antes de la hora de entrada para que el fichaje sea válido |
| Ajuste automático de horario | Booleano | Desactivado | Ajusta automáticamente el timestamp del fichaje al inicio del turno si se produce dentro del margen de tolerancia |

## Descripción detallada de cada parámetro

### Desactivar validación de geocerca

Cuando esta opción está activada, el sistema acepta fichajes desde cualquier ubicación GPS sin comprobar si el empleado está dentro del radio definido. La coordenada GPS sigue registrándose en el sistema, pero no se utiliza como criterio de validación.

**Cuándo usarlo:** sucursales donde los empleados trabajan en itinerancia, en domicilios de clientes o en espacios cuya cobertura GPS es deficiente (sótanos, almacenes con paredes gruesas). También es útil durante el periodo de configuración inicial, cuando todavía no se ha ajustado el radio con precisión.

> **Aviso:** Deshabilitar la geocerca elimina una capa de control antifraude. Utilice este parámetro únicamente cuando existan razones operativas justificadas y comuníquelo al equipo de cumplimiento si su empresa está sujeta a auditorías de control horario.

### Desactivar pausas

Cuando está activada, los empleados asignados a esta sucursal no pueden registrar el inicio ni el fin de una pausa desde la app. Las jornadas se computan como tiempo continuo sin deducción de pausa.

**Cuándo usarlo:** sucursales donde el convenio colectivo aplicable no obliga a registrar las pausas de forma individualizada, o donde las pausas se gestionan mediante rotación de personal sin que cada empleado deba registrarlas individualmente.

### Duración estándar de pausa

Este valor se aplica únicamente cuando las pausas están habilitadas y el empleado no ha registrado manualmente el inicio y el fin de su pausa. En ese caso, el sistema descuenta automáticamente el número de minutos indicado del tiempo total de la jornada.

**Cuándo modificarlo:** ajuste este valor al tiempo de pausa estipulado en el convenio colectivo aplicable a la sucursal. Si los empleados de la sucursal tienen pausas de 20 minutos según convenio, establezca la duración estándar de pausa en 20 minutos.

> **Aviso:** Si los empleados sí registran sus pausas de forma manual, el sistema utiliza la duración real registrada e ignora la duración estándar configurada. Este parámetro actúa únicamente como valor de sustitución cuando no hay registro explícito.

### Tolerancia de entrada

Define cuántos minutos antes de la hora de inicio de turno se acepta un fichaje de entrada como válido. Por ejemplo, si el turno comienza a las 09:00 y la tolerancia de entrada tiene el valor 10, el sistema acepta fichajes de entrada desde las 08:50 sin marcarlos como anomalía.

**Cuándo usarlo:** sucursales donde es habitual que los empleados lleguen unos minutos antes de su hora oficial y resulta operativamente conveniente que su jornada empiece a computarse desde ese momento. También evita la generación de alertas de "llegada anticipada" en entornos donde esa práctica está normalizada.

### Ajuste automático de horario

Cuando está activado y el fichaje de entrada se produce dentro del margen de tolerancia de entrada, el sistema registra automáticamente el fichaje con el timestamp de inicio del turno en lugar del momento real de llegada. Esto garantiza que la jornada computable empiece exactamente a la hora de turno, aunque el empleado haya fichado unos minutos antes.

**Cuándo usarlo:** entornos donde el cómputo de horas debe ser exacto al minuto y no debe reflejarse tiempo trabajado fuera del turno contratado, incluso si el empleado llega antes. Es especialmente relevante cuando los datos de CheckBiz360 se exportan a sistemas de nómina que calculan automáticamente el coste a partir de los timestamps.

## Interacción entre parámetros

Algunos parámetros interactúan entre sí y deben configurarse de forma coordinada:

- La **tolerancia de entrada** y el **ajuste automático de horario** están diseñados para usarse juntos. Si activa el ajuste automático con una tolerancia de entrada igual a cero, el parámetro no tendrá efecto práctico.
- Si las **pausas están desactivadas**, el valor de la duración estándar de pausa es irrelevante y el sistema lo ignora.
- La opción de **desactivar validación de geocerca** es independiente del resto de parámetros y puede combinarse con cualquier configuración.

> **Aviso:** Los cambios en la configuración avanzada tienen efecto inmediato para todos los fichajes posteriores. No modifican los registros ya existentes en el histórico.

---

> **Nota de rol:** La configuración avanzada de sucursal está disponible únicamente para los roles **Owner** y **Manager** con permisos de administración de organización. Los roles **Supervisor** y **Worker** no tienen acceso a esta sección.

## Artículos relacionados

- [Crear y gestionar sucursales](57-crear-y-gestionar-sucursales.md)
- [Estados de una sucursal](59-estados-de-una-sucursal.md)
- [Asignar empleados a sucursales](60-asignar-empleados-a-sucursales.md)
- [Configuración de entidad](61-configuracion-de-entidad.md)

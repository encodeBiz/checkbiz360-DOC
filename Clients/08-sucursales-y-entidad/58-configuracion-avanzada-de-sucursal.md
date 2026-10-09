# Configuración avanzada de sucursal

Cada sucursal en CheckBiz360 admite ajustes que adaptan el comportamiento del sistema a las particularidades de ese centro de trabajo: hasta dónde llega la zona de fichaje, cómo se computan las horas y cómo se registran las pausas. Este artículo describe cada parámetro, dónde se configura, su efecto y cuándo conviene modificarlo.

## Dónde encontrar cada ajuste

La configuración avanzada de una sucursal está repartida en dos sitios, según lo que se quiera ajustar:

- **La ficha de la sucursal** (**Sucursales** en el menú lateral → editar) contiene los datos del centro y la **configuración operativa**: la zona de chequeo.
- **El calendario** (en la ficha de la sucursal, o **Horarios** → **Configuración general** si se hereda de la entidad) contiene el horario semanal, las pausas, la modalidad de jornada y la de descanso.

## Tabla de parámetros

| Parámetro | Dónde | Tipo | Descripción |
|---|---|---|---|
| Zona de chequeo en metros | Ficha de la sucursal | Entero (metros) | Radio alrededor de las coordenadas dentro del cual se acepta el fichaje |
| Zona de chequeo permitida | Ficha de la sucursal | Booleano | Cuando se desactiva, deja de validarse la geocerca en esta sucursal |
| Estado | Ficha de la sucursal | Activa / Inactiva | Una sucursal inactiva no admite fichajes |
| Datos adicionales | Ficha de la sucursal | Clave/valor | Campos libres propios de su organización |
| Horario semanal y pausas | Calendario | Franjas horarias | Turnos por día y pausas dentro de cada turno |
| Jornada estricta / flexible | Calendario | Booleano | Computar el horario oficial o el tiempo real trabajado |
| Descanso estricto / flexible | Calendario | Booleano | Descontar una duración fija o el tiempo real de pausa |
| Tiempo de descanso (minutos) | Calendario | Entero (minutos) | Duración descontada cuando el descanso es estricto |

> **Nota:** no existe un parámetro de "tolerancia de entrada" ni de "ajuste automático del timestamp". Lo que decide si el tiempo trabajado fuera de la franja cuenta o no es la modalidad de jornada. Consulte [Jornada estricta y jornada flexible](../04-calendario-y-horarios/28-horario-flexible.md).

## Descripción detallada de cada parámetro

### Zona de chequeo permitida

Cuando esta opción se desactiva, el sistema acepta fichajes desde cualquier ubicación GPS sin comprobar si el empleado está dentro del radio definido. La coordenada GPS sigue registrándose en el sistema, pero no se utiliza como criterio de validación.

**Cuándo usarlo:** sucursales donde los empleados trabajan en itinerancia, en domicilios de clientes o en espacios cuya cobertura GPS es deficiente (sótanos, almacenes con paredes gruesas). También es útil durante el periodo de configuración inicial, cuando todavía no se ha ajustado el radio con precisión.

> **Aviso:** Deshabilitar la geocerca elimina una capa de control antifraude. Utilice este parámetro únicamente cuando existan razones operativas justificadas y comuníquelo al equipo de cumplimiento si su empresa está sujeta a auditorías de control horario.

### Modalidad de descanso

Los descansos tienen dos modalidades, que se eligen en el calendario de la sucursal:

- **Descanso estricto**: el sistema descuenta exactamente los minutos configurados. El empleado **no marca** inicio ni fin de la pausa, y no se reconocen descansos más largos ni más cortos.
- **Descanso flexible**: el empleado **marca** el inicio y el fin de cada pausa desde la app, y el sistema contabiliza la duración efectiva.

**Cuándo usar el estricto:** pausas fijas por convenio, iguales todos los días, donde exigir dos fichajes más al día no aporta nada. **Cuándo usar el flexible:** pausas variables según la carga de trabajo, o cuando se necesita acreditar la duración real de los descansos.

### Tiempo de descanso

Cuando el descanso es estricto, este valor —en minutos— es el que se descuenta de la jornada. Ajústelo al tiempo de pausa estipulado en el convenio aplicable a esa sucursal.

Con el descanso flexible el campo no aplica: manda el tiempo que registre el empleado.

### Modalidad de jornada

Decide si el cómputo sigue el horario oficial (**jornada estricta**) o el tiempo realmente trabajado (**jornada flexible**). Es el ajuste con más impacto sobre los informes de horas y está explicado en detalle en [Jornada estricta y jornada flexible](../04-calendario-y-horarios/28-horario-flexible.md).

## Interacción entre parámetros

- La **modalidad de jornada** y la **de descanso** son independientes: puede tener jornada estricta con descanso flexible, o al revés.
- El **tiempo de descanso** solo se aplica con el descanso estricto; con el flexible se ignora.
- **Desactivar la zona de chequeo** es independiente del resto y puede combinarse con cualquier configuración.
- Todo lo del calendario sigue la **herencia** entidad → sucursal → empleado: lo que no defina la sucursal, lo hereda de la entidad.

> **Aviso:** Los cambios tienen efecto sobre los fichajes posteriores. No modifican los registros ya existentes en el histórico.



---

> **Nota de rol:** La configuración avanzada de sucursal está disponible únicamente para los roles **Owner** y **Manager** con permisos de administración de organización. Los roles **Supervisor** y **Worker** no tienen acceso a esta sección.

## Artículos relacionados

- [Crear y gestionar sucursales](57-crear-y-gestionar-sucursales.md)
- [Estados de una sucursal](59-estados-de-una-sucursal.md)
- [Asignar empleados a sucursales](60-asignar-empleados-a-sucursales.md)
- [Configuración de entidad](61-configuracion-de-entidad.md)

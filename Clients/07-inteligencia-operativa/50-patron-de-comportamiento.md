# El patrón de comportamiento del empleado

## Qué es el EmployeePattern

El EmployeePattern es el perfil de comportamiento que CheckBiz360 construye para cada empleado de forma automática y continua. No se trata de un informe puntual ni de un resumen mensual; es un modelo acumulativo que recoge cómo trabaja el empleado día tras día y permite identificar tendencias que un análisis aislado no revelaría.

Mientras que un informe tradicional le dice que un empleado llegó tarde cuatro veces en marzo, el EmployeePattern le dice si esas cuatro tardanzas son una excepción en un historial impecable o si forman parte de una tendencia que lleva meses empeorando. Esa diferencia de perspectiva es lo que convierte el dato bruto en inteligencia útil.

## Cómo se construye el patrón

El sistema procesa de forma automática los datos que ya existen en la plataforma. No requiere configuración adicional; se activa desde el momento en que la entidad tiene empleados con registros de asistencia y horarios asignados.

Las fuentes de datos que alimentan el patrón son las siguientes:

**Registros de asistencia.** Cada fichaje de entrada y salida aporta información sobre puntualidad, duración real de la jornada y presencia efectiva. El sistema acumula estos datos y calcula medias, desviaciones y tendencias.

**Horarios planificados.** El patrón no analiza el comportamiento en abstracto, sino siempre en relación con lo que estaba previsto. Una salida a las 18:00 es diferente si el turno terminaba a las 18:00 o si terminaba a las 17:00.

**Tareas y valoraciones.** Las tareas completadas y las valoraciones asignadas por el manager complementan el análisis de presencia. Un empleado con asistencia perfecta pero con baja productividad en tareas genera un perfil diferente al de un empleado que falta poco y resuelve bien sus responsabilidades.

**Tiempo acumulado.** El patrón necesita datos suficientes para ser representativo. Durante las primeras semanas de trabajo de un empleado, los índices deben interpretarse con cautela. A partir de varios meses de historial, el patrón refleja con mayor precisión el comportamiento real.

## Por qué el patrón es más valioso que un informe puntual

Un informe puntual captura el estado en un momento determinado. El EmployeePattern capta la dirección en la que evoluciona ese estado. Esa diferencia es crítica para la gestión de personas.

Un empleado puede tener un buen mes aislado después de una conversación con su responsable, pero si su patrón acumulado muestra una tendencia negativa sostenida, el dato del buen mes no debe generar una falsa sensación de problema resuelto. Del mismo modo, un empleado que atraviesa un mal trimestre por razones externas pero tiene un historial sólido merece una valoración diferente a alguien con un perfil cronológicamente irregular.

## Ejemplos de patrones

### Patrones positivos

Un patrón positivo se caracteriza por consistencia y estabilidad. El empleado llega dentro del margen de puntualidad de forma habitual, completa sus jornadas con pocas desviaciones, no acumula ausencias injustificadas y sus valoraciones de tareas son regularmente buenas. Este perfil genera indicadores de fiabilidad y eficiencia altos y es el que la evaluación operativa señala como candidato a promoción.

Otro patrón positivo relevante es el de mejora progresiva: un empleado cuyos índices eran moderados hace seis meses pero muestran una tendencia clara de mejora. Este perfil indica que las acciones de gestión están funcionando y que el empleado tiene capacidad de desarrollo.

### Patrones negativos

Un patrón negativo no se define por un incidente aislado, sino por la repetición. Llegadas tardías concentradas en ciertos días de la semana, salidas anticipadas frecuentes, ausencias recurrentes sin justificación formal o una tendencia de deterioro en los índices a lo largo de los meses.

El patrón más difícil de detectar sin un sistema es el de deterioro lento: un empleado que va acumulando pequeñas desviaciones semana a semana, ninguna de ellas suficientemente llamativa por sí sola, pero que en conjunto representan una deriva significativa.

## Cómo se visualiza en el backoffice

El EmployeePattern se presenta en la ficha de cada empleado dentro del módulo de inteligencia operativa. Los responsables con acceso al módulo pueden consultar:

- Los indicadores calculados —fiabilidad, eficiencia operativa, coste y confiabilidad del patrón— con su evolución temporal en gráfica.
- El historial de comportamiento con los eventos más relevantes.
- El estado actual del flag de anomalía si estuviese activo.

> **Nota:** El acceso a los datos del EmployeePattern está limitado a los roles de Manager y Owner. Los supervisores pueden consultar los indicadores de su equipo directo, pero no tienen acceso a la vista de patrón completo. Consulte el artículo sobre paneles de mando para más detalle sobre permisos.

## Artículos relacionados

- [Qué es la inteligencia operativa](49-que-es-la-inteligencia-operativa.md)
- [Índice de fiabilidad](51-indice-de-fiabilidad.md)
- [Índice de eficiencia operativa](52-indice-de-eficiencia.md)
- [Evaluación operativa del empleado](53-puntuacion-de-promocion.md)
- [Detección de anomalías](55-deteccion-de-anomalias.md)
- [El panel de Operación](56-paneles-de-mando.md)

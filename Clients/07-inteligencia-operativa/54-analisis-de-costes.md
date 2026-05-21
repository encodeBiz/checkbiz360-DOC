# Análisis de costes

## Para qué sirve

El módulo de análisis de costes de CheckBiz360 traduce los datos de asistencia en información económica directamente utilizable por el control de gestión. El objetivo es que la dirección pueda responder en cualquier momento a preguntas como: ¿cuánto ha costado realmente operar esta sucursal esta semana?, ¿qué empleado tiene el mayor coste por hora real trabajada?, ¿en qué periodos estamos desviándonos más del presupuesto de personal?

El sistema no requiere integración con la nómina ni acceso a datos contables externos. Trabaja únicamente con dos variables: las horas reales registradas en la plataforma y la tarifa horaria configurada para cada empleado.

## Configurar el coste por hora del empleado

El punto de partida es definir el coste horario de cada empleado en su perfil. Este valor lo introduce el responsable con acceso de Manager u Owner en la ficha del empleado, dentro del apartado de configuración económica.

Para configurarlo:

1. Acceda al backoffice y navegue a la sección de gestión de empleados.
2. Seleccione el empleado al que desea asignar la tarifa.
3. En la ficha del empleado, localice el campo de coste por hora.
4. Introduzca el valor en euros por hora. Este valor debe reflejar el coste real para la empresa, no el salario bruto: incluya la parte proporcional de las cotizaciones sociales a cargo de la empresa si desea obtener un coste total real.
5. Guarde los cambios. El sistema aplicará esta tarifa a todos los registros futuros y recalculará los históricos disponibles.

> **Nota:** Si el empleado tiene diferentes tarifas según el tipo de jornada (turno ordinario, turno nocturno, festivo), puede configurarlo a nivel de turno en el módulo de horarios. Consulte la documentación de calendarios y horarios para más detalle.

## Qué calcula el sistema

A partir de las horas registradas y la tarifa configurada, el sistema calcula automáticamente tres valores para cada empleado y periodo:

**Coste planificado.** El coste que debería haberse incurrido si el empleado hubiese trabajado exactamente las horas previstas en su horario. Es el valor de referencia contra el que se compara el coste real.

**Coste real.** El coste calculado a partir de las horas efectivamente trabajadas según los fichajes registrados y validados. Si el empleado trabajó más horas de las previstas, el coste real será mayor que el planificado; si trabajó menos, será menor.

**Desviación de coste.** La diferencia entre el coste real y el coste planificado, expresada tanto en valor absoluto (euros) como en porcentaje. Una desviación positiva indica sobrecoste; una desviación negativa indica infrautilización de la jornada.

## Comparativas entre sucursales

Una de las funcionalidades más valoradas del módulo es la capacidad de comparar el coste de operación entre distintas sucursales de la misma entidad. Esta vista está disponible en el panel de costes del backoffice y permite filtrar por periodo, centro y empleado.

Las comparativas permiten detectar situaciones que un análisis sucursal por sucursal no revela:

- Una sucursal con mayor presencia de empleados puede tener un coste por hora real trabajada más alto que otra con menos personal si la primera acumula más horas extra no planificadas.
- Dos sucursales con presupuestos similares pueden tener desviaciones de coste muy distintas según la disciplina horaria de sus equipos.
- Identificar la sucursal con mayor eficiencia de coste no implica que sea mejor gestionada, pero sí indica dónde las prácticas de gestión horaria están funcionando mejor.

## Alertas de sobrecoste y umbrales configurables

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

En una versión futura, CheckBiz360 permitirá configurar alertas automáticas que se activarán cuando la desviación de coste de una sucursal o de un empleado supere un umbral definido por el usuario. Las alertas se enviarán al Manager y al Owner por notificación en el backoffice y, opcionalmente, por correo electrónico. Por ahora, el análisis de costes es una métrica visible en los paneles de mando que debe consultarse de forma manual.

## Exportación para control de gestión

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La exportación de los datos del análisis de costes en formato CSV y PDF no está disponible en la versión actual. Los datos son consultables directamente desde el panel de costes del backoffice, pero no pueden descargarse en este momento. Esta capacidad de exportación está prevista en el roadmap de la plataforma.

## Artículos relacionados

- [Qué es la inteligencia operativa](49-que-es-la-inteligencia-operativa.md)
- [Índice de eficiencia](52-indice-de-eficiencia.md)
- [Paneles de mando](56-paneles-de-mando.md)
- [Informes y exportación](../11-informes-y-exportacion/)
- [Sucursales y entidad](../08-sucursales-y-entidad/)

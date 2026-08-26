# Análisis de costes

## Para qué sirve

El módulo de análisis de costes de CheckBiz360 traduce los datos de asistencia en información económica directamente utilizable por el control de gestión. El objetivo es que la dirección pueda responder en cualquier momento a preguntas como: ¿cuánto ha costado realmente operar esta sucursal esta semana?, ¿qué empleado tiene el mayor coste por hora real trabajada?, ¿en qué periodos estamos desviándonos más del presupuesto de personal?

El sistema no requiere integración con la nómina ni acceso a datos contables externos. Trabaja únicamente con dos variables: las horas reales registradas en la plataforma y la tarifa horaria configurada para cada empleado.

## Configurar el coste por hora del empleado

El punto de partida es definir la **tarifa horaria** de cada empleado. Se configura **en la vinculación del empleado con su sucursal**, no en sus datos personales: una misma persona puede tener tarifas distintas en centros distintos, junto a su puesto y su responsabilidad allí.

Para configurarla:

1. Acceda a **Empleados** y abra la ficha del empleado.
2. Vaya al apartado de sucursales y abra la vinculación con el centro correspondiente.
3. Introduzca la tarifa junto al puesto y la responsabilidad.
4. Guarde los cambios.

El valor debe reflejar el **coste real para la empresa**, no el salario bruto: incluya la parte proporcional de las cotizaciones sociales a cargo de la empresa si quiere un coste total realista.

> **Importante:** sin tarifa configurada no hay análisis de costes posible. Es la causa más frecuente de que los indicadores económicos aparezcan vacíos o extraños. El bloque de **estado de los datos** del panel de Operación indica esta cobertura de configuración: consúltelo antes de dar por buena —o por mala— cualquier cifra de coste.

## Qué calcula el sistema

A partir de las horas registradas y la tarifa configurada, la ficha del empleado muestra:

| Indicador | Qué muestra |
|---|---|
| **Coste por hora trabajada** | El coste unitario real de una hora efectiva |
| **Coste por jornada** | El coste medio de un día de trabajo |
| **Coste por rendimiento** | El coste ponderado por la efectividad observada |
| **Rendimiento del coste invertido** | Qué se obtiene por cada unidad de coste |
| **Coste acumulado** | La suma real del periodo |

Todos se calculan sobre **jornadas validadas** y se comparan contra el histórico consolidado del propio empleado o centro, no contra un presupuesto: la plataforma no gestiona presupuestos ni costes planificados.

## Comparativas entre sucursales

El panel de Operación permite comparar centros entre sí dentro de un periodo. El coste, eso sí, ha dejado de presidir la lectura: no es una medida de operatividad sino una consecuencia, y por eso vive dentro del perfil de cada centro y de cada persona, no como pestaña propia.

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
- [Índice de eficiencia operativa](52-indice-de-eficiencia.md)
- [El panel de Operación](56-paneles-de-mando.md)
- [Tipos de informe](../11-informes-y-exportacion/76-tipos-de-informe.md)
- [Asignar empleados a sucursales](../08-sucursales-y-entidad/60-asignar-empleados-a-sucursales.md)

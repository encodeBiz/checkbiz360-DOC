# Detección de anomalías

## Qué es el indicador de anomalía

CheckBiz360 incluye un mecanismo de detección automática de patrones de fichaje anómalos. Cuando el sistema identifica comportamientos que se desvían significativamente de lo esperable en un trabajador real, activa un indicador de anomalía en el perfil del empleado.

Este indicador no es una acusación ni constituye prueba de ninguna irregularidad. Es una señal de alerta que indica que el comportamiento de fichaje de ese empleado merece una revisión manual. La responsabilidad de investigar, interpretar y actuar recae siempre en el responsable humano.

## Por qué existe este mecanismo

El fichaje digital resuelve el problema del control manual, pero abre la posibilidad de nuevas formas de irregularidad que son difíciles de detectar visualmente: empleados que piden a un compañero que fiche por ellos, registros generados por dispositivos no autorizados o comportamientos automatizados que simulan una presencia que no existe.

Estas situaciones tienen dos características comunes: individualmente, cada registro parece correcto; en conjunto, el patrón es demasiado regular para ser producto del comportamiento humano natural. La detección de anomalías analiza precisamente eso: no cada fichaje aislado, sino el patrón que forman todos ellos a lo largo del tiempo.

## Qué patrones activan la detección

El sistema analiza de forma continua los registros de cada empleado en busca de las siguientes señales:

**Precisión temporal excesiva.** Un empleado real ficha con variaciones naturales: un día llega dos minutos antes, otro llega un minuto después, a veces tarda más en abrir la app. Si los fichajes de un empleado se producen sistemáticamente a la misma hora con una precisión de segundos, durante un número suficiente de días, el sistema lo considera estadísticamente improbable y activa la alerta.

**Geolocalización estática o idéntica.** Si el empleado ficha siempre desde exactamente las mismas coordenadas GPS, día tras día, sin ninguna variación en los decimales, puede indicar que el fichaje no se está produciendo desde el dispositivo móvil del propio empleado en su ubicación real, sino desde un sistema que reproduce siempre la misma posición.

**Patrones de regularidad excesiva.** El comportamiento humano tiene variabilidad inherente. Si todos los parámetros del fichaje de un empleado (hora, coordenadas, duración de la jornada) son demasiado constantes durante un periodo prolongado, el sistema identifica esa regularidad como estadísticamente anómala.

> **Importante:** Ninguno de estos patrones es, por sí solo, prueba de ninguna irregularidad. Existen situaciones legítimas que pueden producir comportamientos similares: empleados que trabajan siempre desde el mismo puesto fijo, dispositivos con GPS poco preciso que reportan siempre las mismas coordenadas, personas con rutinas muy estables. El indicador de anomalía es el inicio de una investigación, no su conclusión.

## Qué debe hacer el responsable cuando aparece un empleado marcado

Cuando el sistema activa el indicador de anomalía para un empleado, el flujo de actuación recomendado es el siguiente:

1. **Revise el historial completo.** Acceda a la ficha del empleado en el módulo de inteligencia operativa y examine los registros de los últimos meses. Identifique desde cuándo aparece el patrón anómalo y si coincide con algún cambio en las circunstancias del empleado o del equipo.

2. **Contraste con el contexto operativo.** Consulte con el supervisor directo si existe alguna explicación operativa: ¿el empleado trabaja siempre desde la misma ubicación fija? ¿Hubo algún cambio en sus condiciones de trabajo que explique la regularidad?

3. **Compare con otros empleados del mismo centro.** Si el patrón anómalo coincide con otros empleados de la misma sucursal, puede indicar un problema sistémico (por ejemplo, un dispositivo de fichaje compartido en un lugar fijo) en lugar de una conducta individual.

4. **Si la irregularidad no tiene explicación evidente, convoque al empleado.** La entrevista debe hacerse desde la cautela: presente los datos observados, escuche la explicación del empleado y documente la conversación. No confronte con acusaciones directas basadas únicamente en el indicador del sistema.

5. **Documente la resolución externamente.** Tanto si la anomalía tiene una explicación legítima como si se confirma una irregularidad, registre el resultado de la revisión en los sistemas o procedimientos que su organización tenga establecidos. La plataforma muestra el indicador, pero el seguimiento del estado de la revisión debe realizarse fuera de CheckBiz360 en la versión actual.

## Workflow de revisión y alertas configurables

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

En una versión futura, el indicador de anomalía estará integrado en un workflow de revisión con estados gestionables directamente en la plataforma (pendiente de revisión, revisado, archivado), lo que permitirá hacer seguimiento del ciclo de vida de cada alerta sin salir del backoffice. Asimismo, se prevé la posibilidad de configurar notificaciones de alerta para que los responsables sean avisados de forma automática cuando se active un nuevo indicador. Por ahora, el responsable debe revisar el panel de Operación de forma proactiva: la pestaña de **Análisis** recoge dónde y cuándo falla el fichaje, que es donde afloran estos patrones.

## Lo que el indicador de anomalía no implica

El indicador de anomalía no es una sanción, no genera notificación al empleado y no tiene efectos automáticos sobre su perfil, sus derechos ni su contrato. Es exclusivamente una herramienta de alerta interna para los responsables con acceso al módulo.

En ningún caso debe usarse el indicador de anomalía como única base para iniciar un procedimiento disciplinario. Cualquier acción de ese tipo debe sustentarse en un proceso de investigación conforme al convenio colectivo y a la normativa laboral aplicable, con la participación, si corresponde, del área de RRHH o de asesoría legal.

> **Nota:** El acceso al indicador de anomalía está restringido a los roles de Manager y Owner. Los supervisores no tienen visibilidad sobre esta información en sus vistas habituales.

## Artículos relacionados

- [Qué es la inteligencia operativa](49-que-es-la-inteligencia-operativa.md)
- [El patrón de comportamiento del empleado](50-patron-de-comportamiento.md)
- [El panel de Operación](56-paneles-de-mando.md)
- [Preparar una inspección de trabajo](../12-cumplimiento-normativo/84-preparar-una-inspeccion-de-trabajo.md)

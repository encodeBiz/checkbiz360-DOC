# Qué es la inteligencia operativa

La inteligencia operativa es el módulo más avanzado de CheckBiz360. Su función no es registrar cuándo llega y sale un empleado, sino convertir esos registros en información útil para tomar decisiones de negocio: detectar tendencias antes de que se conviertan en problemas, identificar a los empleados con mayor potencial, comparar el coste real entre sucursales y fundamentar las decisiones de RRHH con datos objetivos.

Un sistema de control horario tradicional responde a la pregunta "¿estuvo el empleado?". La inteligencia operativa responde a preguntas más relevantes: "¿este centro saca lo mejor de su gente o la degrada?", "¿de cuántas personas depende que esto siga funcionando?", "¿quién cubre este puesto si mañana falta quien lo ocupa?", "¿hay fichajes cuyo patrón sugiere irregularidades?".

Esa diferencia se apoya en tres principios que conviene conocer antes de interpretar cualquier indicador:

1. **La unidad de medida es la jornada, no la persona.** Nada se divide por plantilla, todo sale en proporción; así una sucursal de 5 personas y una de 40 se comparan de verdad.
2. **Nada se compara contra una escala universal.** Cada dato se compara contra su propia historia, contra quienes ocupan el mismo puesto o contra los demás centros de la misma organización.
3. **La ausencia de evidencia nunca es evidencia negativa.** Cuando faltan datos, el sistema dice "acumulando datos"; nunca concluye que algo va mal por no poder medirlo.

Todo esto se consulta en el **panel de Operación**, descrito en [El panel de Operación](./56-paneles-de-mando.md), y se acompaña del relato del **asistente de IA**, que prioriza qué mirar primero sobre las mismas cifras que muestra la pantalla.

## Qué datos analiza el módulo

La inteligencia operativa cruza información de tres fuentes distintas que ya existen en la plataforma:

**Asistencia y puntualidad.** Cada fichaje queda registrado con marca temporal y coordenadas. El sistema analiza la hora de entrada y salida real frente a la planificada, las ausencias sin justificar y las desviaciones de horario acumuladas a lo largo del tiempo.

**Tareas y valoraciones.** Las tareas completadas por cada empleado, junto con las valoraciones que el manager asigna, alimentan el análisis de rendimiento. Un empleado presente no es necesariamente un empleado productivo; el módulo lo tiene en cuenta.

**Costes.** Cada empleado tiene configurada su tarifa horaria. El sistema calcula el coste real de cada jornada multiplicando las horas efectivamente trabajadas por esa tarifa y lo compara con el coste planificado.

## El concepto de EmployeePattern

El motor de análisis construye para cada empleado un objeto denominado EmployeePattern: un perfil de comportamiento que se actualiza de forma continua a medida que se acumulan nuevos registros. Este perfil no es una foto del último mes; es un historial que capta tendencias, mejoras, deterioros y anomalías a lo largo del tiempo.

El patrón del empleado es la base sobre la que se calculan todos los indicadores del módulo: fiabilidad, eficiencia operativa, coste, nivel de confianza y las señales de anomalía. Sin acumulación de datos no hay patrón; por eso el módulo gana valor con el paso del tiempo.

## Qué puede hacer la dirección con estos datos

Antes de contar con inteligencia operativa, los responsables de equipo dependían de la memoria, de la impresión subjetiva y de informes manuales que siempre llegaban tarde. Con el módulo activado, la dirección puede:

- Detectar de forma temprana a empleados cuya fiabilidad está descendiendo, antes de que el problema afecte al equipo.
- Basar las decisiones de promoción en datos objetivos en lugar de percepciones personales.
- Comparar el coste real de operación entre sucursales y tomar medidas correctoras.
- Identificar patrones de fichaje sospechosos que podrían indicar delegación o manipulación de registros.
- Fundamentar conversaciones difíciles con empleados apoyándose en el historial de comportamiento, no en anécdotas.

## Beneficios tangibles

**Detección temprana.** Un deterioro en la asistencia o en la puntualidad rara vez ocurre de golpe. El sistema detecta la tendencia cuando todavía es corregible, no cuando ya ha impactado en la operación.

**Base objetiva para decisiones de personal.** La evaluación operativa del empleado interpreta su patrón real y señala, cuando procede, a los candidatos a promoción. Y como el panel mide cuánto influye el centro en quien pasa por él, permite distinguir a la persona del sitio antes de decidir.

**Reducción de costes ocultos.** El análisis de costes pone en evidencia desviaciones que en un sistema convencional pasan inadvertidas: horas extra no planificadas, turnos incompletos que se pagan completos, diferencias de productividad entre centros.

**Gestión justa y documentada.** Cuando una decisión tiene respaldo en datos históricos y no en la opinión de un solo manager, el proceso es más justo para el empleado y más defendible para la empresa ante cualquier reclamación.

## Limitaciones que conviene conocer

La inteligencia operativa ofrece indicadores, no veredictos. Los índices y los flags son señales que orientan la atención del manager, pero no reemplazan el juicio humano. Una puntuación baja puede tener causas legítimas que los datos no capturan: una situación personal del empleado, una carga de trabajo mal dimensionada o un problema de integración con el equipo.

> **Importante:** Los datos generados por el módulo de inteligencia operativa tienen carácter interno y de apoyo a la gestión. No deben utilizarse como único fundamento de decisiones disciplinarias sin el acompañamiento de un proceso de evaluación conforme al convenio colectivo aplicable.

## Artículos relacionados

- [El patrón de comportamiento del empleado](50-patron-de-comportamiento.md)
- [Índice de fiabilidad](51-indice-de-fiabilidad.md)
- [Índice de eficiencia operativa](52-indice-de-eficiencia.md)
- [Evaluación operativa del empleado](53-puntuacion-de-promocion.md)
- [Análisis de costes](54-analisis-de-costes.md)
- [Detección de anomalías](55-deteccion-de-anomalias.md)
- [El panel de Operación](56-paneles-de-mando.md)

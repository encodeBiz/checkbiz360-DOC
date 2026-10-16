# Centro de Ayuda — CheckBiz360

Bienvenido al centro de ayuda de CheckBiz360, la plataforma de control de asistencia digital de Encodebiz. Este centro de ayuda reúne la documentación completa dirigida al cliente final: propietarios de cuenta, responsables de recursos humanos, managers de área y supervisores de equipo.

Los artículos están organizados en 16 secciones temáticas. Cada sección cubre un módulo o área funcional de la plataforma y contiene artículos independientes que pueden consultarse de forma individual o como lectura secuencial.

---

## Estados de funcionalidad

La siguiente convención identifica el estado de cada funcionalidad en la versión actual de CheckBiz360 (V1). Se aplica en todos los artículos del centro de ayuda y en las tablas de cada módulo de esta página.

| Estado | Significado |
|---|---|
| **Disponible** | La funcionalidad está activa en la versión actual y puede utilizarse de inmediato. |
| **Disponible parcialmente** | La funcionalidad existe pero con capacidades limitadas respecto a la descripción completa. |
| **Pendiente de desarrollo** | La funcionalidad está planificada y se incluirá en una versión futura de la plataforma. |
| **No disponible** | La funcionalidad no está implementada y no tiene fecha de entrega planificada actualmente. |

---

## Secciones

### 01. Primeros pasos

Introducción a la plataforma, diferencias frente a otros sistemas y guía de puesta en marcha inicial.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Registro de cuenta y configuración de entidad | **Disponible** | Proceso completo disponible desde el backoffice. |
| Configuración de sucursales | **Disponible** | Creación, edición y desactivación de sucursales. |
| Guía de inicio rápido | **Disponible** | Flujo de 10 pasos hasta el primer fichaje validado. |
| Guía inicial en el backoffice, narrada por Merlin | **Disponible** | Cinco pasos sobre el estado real de la cuenta: suscripción, horario, centro, empleado y prueba de fichaje. |
| Verificación anti-bots en el registro y la recuperación de contraseña | **Disponible** | Reto de Cloudflare integrado en el formulario. |
| Estructura jerárquica entidad → sucursal → empleado | **Disponible** | Totalmente operativa en V1. |

| Artículo | Descripción |
|---|---|
| [Qué es CheckBiz360](01-primeros-pasos/01-que-es-checkbiz360.md) | Descripción general de la plataforma, componentes y casos de uso |
| [Diferencias con otros software](01-primeros-pasos/02-diferencias-con-otros-software.md) | Comparativa con sistemas tradicionales de control horario |
| [Crear cuenta y configurar la entidad](01-primeros-pasos/03-crear-cuenta-y-configurar-entidad.md) | Pasos desde el registro hasta la primera sucursal operativa |
| [Guía de inicio rápido](01-primeros-pasos/04-guia-inicio-rapido.md) | Los 10 pasos para tener el primer fichaje validado en 15 minutos |
| [Estructura de la plataforma](01-primeros-pasos/05-estructura-de-la-plataforma.md) | Los tres niveles jerárquicos: entidad, sucursal y empleado |

---

### 02. Empleados

Alta, configuración, roles y seguridad de los empleados en la plataforma.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Alta, edición y desactivación de empleados | **Disponible** | CRUD completo con estados laborales, y estado *pendiente* —que no se factura— para fichas a medio completar. |
| Tipo de relación: plantilla o colaborador | **Disponible** | Visible en la ficha; los colaboradores quedan fuera del informe de registro de jornada. |
| Equipos (plantillas de personas con puesto y precio) | **Disponible** | Se aplican a una sucursal para dar de alta a toda la cuadrilla de una vez. Añadir un equipo entero a una tarea: pendiente de desarrollo. |
| Roles y niveles de responsabilidad (worker, supervisor, manager, owner) | **Disponible** | Cuatro niveles con permisos diferenciados. |
| Autenticación en dos factores (2FA) | **Disponible** | Compatible con apps TOTP (Google Authenticator, Authy). |
| Verificación biométrica y dispositivos de confianza | **Disponible** | Configurable por empleado desde la app. |
| Empleados asignados a múltiples entidades | **Disponible** | Selector de entidad en el inicio de sesión. |
| Importación de empleados desde CSV | **Disponible** | Carga inicial de plantilla con mapeo de columnas. |
| Exportación del directorio de empleados | **Pendiente de desarrollo** | El listado se consulta y filtra en pantalla, sin fichero descargable. |

| Artículo | Descripción |
|---|---|
| [Crear y gestionar empleados](02-empleados/06-crear-y-gestionar-empleados.md) | Alta, edición, estados laborales y desactivación |
| [Roles y niveles de responsabilidad](02-empleados/07-roles-y-niveles-de-responsabilidad.md) | Los cuatro niveles: worker, supervisor, manager, owner |
| [Matriz de permisos por rol](02-empleados/08-matriz-de-permisos-por-rol.md) | Tabla completa de qué puede hacer cada rol |
| [Autenticación en dos factores (2FA)](02-empleados/09-autenticacion-dos-factores.md) | Configuración, apps compatibles y recuperación de acceso |
| [Biometría y dispositivos de confianza](02-empleados/10-biometria-y-dispositivos-de-confianza.md) | Verificación biométrica y gestión de dispositivos autorizados |
| [Empleados multi-entidad](02-empleados/11-empleados-multi-entidad.md) | Un empleado en varias organizaciones, selector de entidad |
| [Exportar el listado de empleados](02-empleados/12-exportar-empleados-csv.md) | Estado de la funcionalidad, alternativas disponibles y RGPD |
| [Equipos](02-empleados/99-equipos.md) | Crear equipos, aplicarlos a una sucursal y guardar una sucursal como equipo |

---

### 03. Control horario

Cómo funciona el sistema de fichaje: validaciones, tipos de registro, geocercas y gestión de jornadas.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Fichaje con validación de geocerca, horario y dispositivo | **Disponible** | Tres capas de validación simultáneas en cada fichaje. |
| Check-in y check-out desde la app móvil | **Disponible** | Proceso completo operativo en iOS y Android. |
| Trabajo fuera del centro (antes «fichaje en remoto») | **Disponible** | Activación por empleado con validación de zona horaria. |
| Descansos y pausas (restin/restout) | **Disponible** | Descuento automático configurable por sucursal. |
| Validación QR previa al fichaje | **Disponible** | Mecanismo configurable por sucursal, no obligatorio. |
| Solicitud de jornada manual (Modo A y Modo B) | **Disponible** | Requiere aprobación del responsable. |
| Revisión y validación de fichajes por responsable | **Disponible** | Flujo de aprobación, rechazo y resolución; una corrección rechazada deja el fichaje como estaba. |
| Trazabilidad e historial de cambios inmutable | **Disponible** | Registro de solicitudes y modificaciones con auditoría. |
| Detección de fichaje sospechoso | **Disponible** | Indicador automático basado en patrones anómalos. |

| Artículo | Descripción |
|---|---|
| [Cómo funciona el fichaje](03-control-horario/13-como-funciona-el-fichaje.md) | Las tres capas de validación: geocerca, horario y dispositivo |
| [Check-in y check-out desde la app](03-control-horario/14-checkin-checkout-desde-app.md) | Paso a paso del fichaje desde la app móvil |
| [Trabajo fuera del centro](03-control-horario/15-fichaje-en-remoto.md) | Fichar sin geocerca: trabajo de campo, teletrabajo, activación y zona horaria |
| [Geocercas y radio de fichaje](03-control-horario/16-geocercas-radio-de-fichaje.md) | Configuración del radio, desactivación y valores recomendados |
| [Descansos y pausas](03-control-horario/17-descansos-y-pausas.md) | Restin/restout, descuento automático y configuración por sucursal |
| [Validación del empleado mediante QR](03-control-horario/18-validacion-del-empleado-qr.md) | Token QR, flujo con supervisor y warm-up del sistema |
| [Solicitar jornada manual](03-control-horario/19-solicitar-jornada-manual.md) | Modo A (jornada completa) y Modo B (solo checkout) |
| [Revisión y validación de fichajes](03-control-horario/20-revision-y-validacion-de-fichajes.md) | Flujo de aprobación, rechazo y resolución por responsable |
| [Trazabilidad e historial de cambios](03-control-horario/21-trazabilidad-historial-de-cambios.md) | requestUpdates, inmutabilidad y uso en auditorías |
| [Estados y códigos de error](03-control-horario/22-estados-y-codigos-de-error.md) | Tablas de estados y códigos de error con causas y soluciones |

---

### 04. Calendario y horarios

Configuración de turnos, horarios base, calendarios laborales y excepciones individuales.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Horarios base y turnos por sucursal | **Disponible** | Turno único o múltiples turnos por día. |
| Calendario laboral (festivos nacionales y locales) | **Disponible** | Jerarquía de herencia: entidad → sucursal → empleado. |
| Excepciones de horario individuales | **Disponible** | Excepciones puntuales y periódicas. |
| Jornada estricta o flexible | **Disponible** | Decide si computa el horario oficial o el tiempo real trabajado. |
| Descanso estricto o flexible | **Disponible** | Duración fija descontada, o pausas marcadas por el empleado. |
| Plantillas de horario | **Disponible** | Guardar un horario semanal y aplicarlo a otras sucursales. |
| Ausencias de empleado por rango de fechas, con marca de retribuida | **Disponible** | Retribuida, no retribuida o sin definir. |
| Tablero de disponibilidad | **Disponible** | Cobertura por sucursal y día, quién falta y por qué, y alta de días libres desde el tablero. |
| Herencia de configuración en cascada | **Disponible** | Algoritmo de prioridad para calcular el calendario efectivo. |
| Turnos rotativos (alternancia A/B automática) | **Pendiente de desarrollo** | Hoy se cubre con una sucursal por turno o con horario propio del empleado. |

| Artículo | Descripción |
|---|---|
| [Horarios base y turnos](04-calendario-y-horarios/23-horarios-base-y-turnos.md) | Turno único, múltiples turnos por día, selección del turno activo |
| [Calendario laboral](04-calendario-y-horarios/24-calendario-laboral.md) | Festivos nacionales, locales, jerarquía entity→branch→employee |
| [Excepciones de horario](04-calendario-y-horarios/25-excepciones-de-horario.md) | Excepciones puntuales y periódicas, jornada reducida |
| [Herencia de configuración](04-calendario-y-horarios/26-herencia-de-configuracion.md) | Algoritmo de cascada y depuración del calendario efectivo |
| [Turnos rotativos](04-calendario-y-horarios/27-turnos-rotativos.md) | No disponible en V1: cómo cubrir la rotación con sucursales o con horario del empleado |
| [Jornada estricta y jornada flexible](04-calendario-y-horarios/28-horario-flexible.md) | Cómo se computan las horas y las pausas según la modalidad elegida |
| [Festivos y días no laborables](04-calendario-y-horarios/29-festivos-y-dias-no-laborables.md) | Tipos de festivo, ausencias de empleado, bloqueo de fichajes, sectores que trabajan en festivo |
| [Tablero de disponibilidad](04-calendario-y-horarios/98-tablero-de-disponibilidad.md) | Cobertura por sucursal y día, desglose de quién falta y días libres desde el tablero |
| [Importar el cuadrante semanal](04-calendario-y-horarios/108-importar-el-cuadrante-semanal.md) | La semana de toda la plantilla de una sucursal en una subida, o la de una persona desde su ficha |

---

### 05. Gestión documental

Subida, organización, acuse de recibo y control de acceso a los documentos laborales.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Subida y organización de documentos | **Disponible** | Doce tipos, ámbito entidad/sucursal/empleado y visibilidad por rol. Máx. 10 MB por archivo. |
| Documentos privados con control de acceso por rol | **Disponible** | Tabla de permisos diferenciada por nivel de usuario. |
| Notificaciones push al recibir documentos | **Disponible** | Navegación directa al documento desde la notificación. |
| Acuse de recibo (confirmación de lectura) | **Disponible** | El empleado confirma la lectura; queda registrado en el sistema. |
| Descarga individual de documentos | **Disponible** | Enlace firmado por documento con expiración. |
| Archivo lógico de documentos (sin borrado permanente) | **Disponible** | Los documentos archivados dejan de ser visibles pero se conservan. |
| Confirmación firmada desde el móvil | **Disponible** | Acta de firma descargable y PDF firmado para documentos PDF de un solo empleado. |
| Historial automático de versiones | **Pendiente de desarrollo** | Planificado para una versión futura. |
| Descarga masiva de documentos (ZIP) | **Pendiente de desarrollo** | Planificada para una versión futura. |

| Artículo | Descripción |
|---|---|
| [Qué es el módulo documental](05-gestion-documental/30-que-es-el-modulo-documental.md) | Para qué sirve, tipos de documentos y diferencia con almacenamiento genérico |
| [Subir y organizar documentos](05-gestion-documental/31-subir-y-organizar-documentos.md) | Campos, categorías, destinatarios y visibilidad |
| [Nóminas y contratos](05-gestion-documental/32-nominas-y-contratos.md) | Flujo mensual, notificación, acceso desde la app y conservación legal |
| [Documentos privados](05-gestion-documental/33-documentos-privados.md) | Visibilidad por rol, tabla de acceso y casos de uso |
| [Notificaciones de documentos](05-gestion-documental/34-notificaciones-de-documentos.md) | Push payload, navegación directa al documento desde la notificación |
| [Acuse de recibo y firma electrónica](05-gestion-documental/35-firma-electronica.md) | Confirmación firmada con el móvil, acta de firma y PDF firmado para documentos de una persona |
| [Historial de versiones](05-gestion-documental/36-historial-de-versiones.md) | Flujo manual disponible en V1; historial automático en roadmap |
| [Permisos de acceso documental](05-gestion-documental/37-permisos-de-acceso-documental.md) | Tabla de permisos por rol: subir, ver, confirmar, archivar |
| [Exportar documentos](05-gestion-documental/38-exportar-documentos.md) | Descarga individual en V1; descarga masiva en roadmap |

---

### 06. Tareas

Creación, asignación, seguimiento y valoración de tareas operativas.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Crear y asignar tareas a empleados | **Disponible** | Asignación individual y múltiple con notificación push; editar la tarea asigna y retira empleados. |
| Lugar de trabajo propio por tarea | **Disponible** | Dirección y margen propios; iniciar exige estar allí, desde la app. |
| Duplicar una tarea | **Disponible** | Copia el encargo, sin asignar y en borrador; pide de nuevo las fechas. |
| Pausar y reanudar tareas | **Disponible** | Desde el backoffice y desde la app 1.4.0; el tiempo en pausa sale en el informe. |
| Historial de la tarea | **Disponible** | Quién la creó, inició, pausó, completó, validó o canceló, con fecha y rol. |
| Descripción con formato (listas, checklists, enlaces) | **Disponible** | Editor con barra de formato y vista previa. |
| Evidencias de foto y vídeo | **Disponible** | Foto (JPG, PNG, WEBP) hasta 5 MB; vídeo hasta 25 MB desde la app. |
| Estados de tarea: borrador, asignada, en progreso, completada, validada, rechazada, cancelada | **Disponible** | Siete estados con trazabilidad completa. |
| Cuatro prioridades: baja, media, alta y crítica | **Disponible** | Con código de color en el listado. |
| Indicador de cumplimiento temporal | **Disponible** | A tiempo, en riesgo, vencida, completada a tiempo o tarde. |
| Fecha prevista de inicio y aviso de inicio tardío | **Disponible** | Notificación a los 15 minutos, configurable por tarea. |
| Validación y valoración de tareas por el responsable | **Disponible** | Delegables al supervisor por tarea; rechazo con motivo obligatorio. |
| Notificaciones push de tareas | **Disponible** | Asignación, validación, rechazo, inicio tardío y vencimiento. |
| Informe de tareas exportable | **Disponible** | Excel (XLSX), filtrable por sucursal, estado y periodo de vencimiento, con tiempo invertido y en pausa; con el inventario contratado, también el material de cada tarea. |
| Adjuntos de tipo documento (PDF, Word, Excel) | **Pendiente de desarrollo** | Hoy las evidencias admiten foto y vídeo. |
| Estado "vencida" automático al superar la fecha límite | **Pendiente de desarrollo** | Hoy el vencimiento se refleja en el cumplimiento temporal. |
| Configurar la antelación de los avisos de vencimiento | **Pendiente de desarrollo** | Los avisos se emiten; su antelación no es configurable. |
| Métricas agregadas de tareas (completitud, tiempo medio) | **Pendiente de desarrollo** | Calculables hoy a partir del informe en Excel. |

| Artículo | Descripción |
|---|---|
| [Qué es el módulo de tareas](06-tareas/39-que-es-el-modulo-de-tareas.md) | Para qué sirve y diferencia con el control de asistencia |
| [Crear una tarea](06-tareas/40-crear-una-tarea.md) | Campos, lugar de trabajo propio, duplicar una tarea y adjuntos de foto/vídeo |
| [Asignar tareas a empleados](06-tareas/41-asignar-tareas-a-empleados.md) | Asignación individual y múltiple, reasignación, notificación |
| [Estados de una tarea](06-tareas/42-estados-de-una-tarea.md) | Ciclo de vida, reabrir una tarea, tarea en pausa e indicador de cumplimiento temporal |
| [Seguimiento y actualizaciones](06-tareas/43-seguimiento-y-actualizaciones.md) | Iniciar, pausar y reanudar, notas e historial de la tarea |
| [Prioridades y fechas límite](06-tareas/44-prioridades-y-fechas-limite.md) | Sistema de prioridades e indicador de cumplimiento temporal |
| [Validación de tareas](06-tareas/45-validacion-de-tareas.md) | Flujo de validación, aceptación y rechazo con motivo |
| [Valoración del trabajador](06-tareas/46-valoracion-del-trabajador.md) | Escala de puntuación e impacto en el índice de eficiencia |
| [Notificaciones de tareas](06-tareas/47-notificaciones-de-tareas.md) | Eventos notificados en V1; recordatorios en roadmap |
| [Informes de tareas](06-tareas/48-informes-de-tareas.md) | Métricas en el backoffice e informe en Excel, con sus columnas de tiempo |

---

### 07. Inteligencia operativa

Análisis de patrones de comportamiento, índices de rendimiento, costes y detección de anomalías.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Panel de Operación (vista única, por periodo mensual) | **Disponible** | Se lee de arriba abajo; tres pestañas: Sucursales, Empleados y Análisis. |
| Índice de fiabilidad | **Disponible** | Calidad del comportamiento, separada del tiempo que se lleva midiendo. |
| Efecto del centro | **Disponible** | Compara a cada persona consigo misma en distintos centros. |
| Dependencia (concentración de la operación) | **Disponible** | Cuánta parte de la operación recae en pocas personas, con relevo por puesto. |
| Estados de madurez del dato | **Disponible** | Acumulando datos / evidencia parcial / sin datos suficientes. |
| Índice de eficiencia operativa y coste | **Disponible** | Coste real frente al histórico consolidado; requiere tarifa configurada. |
| Evaluación operativa del empleado | **Disponible** | Diagnóstico automático del patrón, con señal de candidato a promoción. |
| Detección de anomalías (fichajes sospechosos) | **Disponible** | Aflora en la pestaña de Análisis del panel. |
| Relato del asistente de IA sobre el panel | **Disponible** | Narra y prioriza las cifras que ya muestra la pantalla. |
| Puntuación de promoción como score único comparable | **Pendiente de desarrollo** | No existe un número único ni un ranking por ese valor. |
| Workflow de revisión de anomalías (estados pendiente/revisado) | **Pendiente de desarrollo** | Planificado para una versión futura. |
| Alertas de sobrecoste configurables | **Pendiente de desarrollo** | Planificado para una versión futura. |
| Exportación de datos de paneles (CSV/PDF) | **Pendiente de desarrollo** | Planificado para una versión futura. |

| Artículo | Descripción |
|---|---|
| [Qué es la inteligencia operativa](07-inteligencia-operativa/49-que-es-la-inteligencia-operativa.md) | El módulo diferenciador de CheckBiz360 y el concepto de patrón de comportamiento |
| [Patrón de comportamiento](07-inteligencia-operativa/50-patron-de-comportamiento.md) | Cómo se construye el patrón y por qué supera al informe puntual |
| [Índice de fiabilidad](07-inteligencia-operativa/51-indice-de-fiabilidad.md) | Qué mide, rangos y cómo mejorarlo |
| [Índice de eficiencia operativa](07-inteligencia-operativa/52-indice-de-eficiencia.md) | Coste real frente al histórico y cómo interpretarlo |
| [Evaluación operativa del empleado](07-inteligencia-operativa/53-puntuacion-de-promocion.md) | Diagnóstico del patrón y señal de candidato a promoción |
| [Análisis de costes](07-inteligencia-operativa/54-analisis-de-costes.md) | Tarifa por sucursal, indicadores de coste y alertas en roadmap |
| [Detección de anomalías](07-inteligencia-operativa/55-deteccion-de-anomalias.md) | Indicador automático en V1; workflow de revisión en roadmap |
| [El panel de Operación](07-inteligencia-operativa/56-paneles-de-mando.md) | Los tres índices, las tres pestañas y cómo se lee |

---

### 08. Sucursales y entidad

Creación y configuración de sucursales, asignación de empleados y vista global multi-sucursal.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Crear y gestionar sucursales | **Disponible** | Alta, edición, geocodificación y desactivación. |
| Configuración avanzada de sucursal (geocerca, pausas, tolerancia) | **Disponible** | Todos los parámetros operativos configurables. |
| Asignar empleados a sucursales con responsabilidades | **Disponible** | Multi-sucursal con calendario efectivo por asignación. |
| Configuración de entidad (datos fiscales, zona horaria) | **Disponible** | Propagación de cambios a sucursales dependientes. |
| Colaboradores del backoffice (propietario y administrador) | **Disponible** | Invitación, cambio de rol y retirada; nunca se queda la entidad sin propietario activo. |
| Vista global multi-sucursal con KPIs consolidados | **Disponible** | Panel de comparativas entre sucursales en el backoffice. |

| Artículo | Descripción |
|---|---|
| [Crear y gestionar sucursales](08-sucursales-y-entidad/57-crear-y-gestionar-sucursales.md) | Alta, campos obligatorios, geocodificación y desactivación |
| [Configuración avanzada de sucursal](08-sucursales-y-entidad/58-configuracion-avanzada-de-sucursal.md) | Parámetros avanzados: geocerca, pausas, tolerancia, ajuste de timestamp |
| [Estados de una sucursal](08-sucursales-y-entidad/59-estados-de-una-sucursal.md) | Activa/inactiva, impacto en fichajes e histórico |
| [Asignar empleados a sucursales](08-sucursales-y-entidad/60-asignar-empleados-a-sucursales.md) | Multi-sucursal, responsabilidades y calendario efectivo |
| [Configuración de entidad](08-sucursales-y-entidad/61-configuracion-de-entidad.md) | Datos fiscales, entorno de trabajo, colaboradores, zona horaria global y propagación de cambios |
| [Vista global multi-sucursal](08-sucursales-y-entidad/62-vista-global-multi-sucursal.md) | Panel consolidado, KPIs globales y comparativas entre sucursales |

---

### 09. Notificaciones

Tipos de notificación generados automáticamente por el sistema para empleados y responsables.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Notificaciones push por eventos (asistencia, documentos, tareas) | **Disponible** | Enviadas automáticamente en cada evento relevante. |
| Alertas para responsables (empleado sin fichar, fichaje sospechoso) | **Disponible** | Visibles en el backoffice y en la app del supervisor. |
| Centro de notificaciones en app y backoffice | **Disponible parcialmente** | Notificaciones visibles mientras no se descartan; sin historial persistente. |
| Correo de bienvenida y restablecimiento de contraseña | **Disponible** | Únicos correos automáticos del sistema en V1. |
| Preferencias de notificación configurables por usuario | **Pendiente de desarrollo** | Planificado para una versión futura. |
| Historial persistente de notificaciones | **Pendiente de desarrollo** | Planificado para una versión futura. |
| Notificaciones por email adicionales (alertas operativas, resúmenes) | **Pendiente de desarrollo** | Planificado para una versión futura. |

| Artículo | Descripción |
|---|---|
| [Tipos de notificación](09-notificaciones/63-tipos-de-notificacion.md) | Asistencia, documentos, tareas, seguridad y administrativas |
| [Notificaciones push en la app](09-notificaciones/64-notificaciones-push-en-la-app.md) | Contenido, navegación directa al recurso y diagnóstico |
| [Configurar preferencias de notificación](09-notificaciones/65-configurar-preferencias-de-notificacion.md) | Eventos notificados en V1; preferencias configurables en roadmap |
| [Alertas para responsables](09-notificaciones/66-alertas-para-responsables.md) | Empleado que no fichó, fichaje sospechoso, jornada manual pendiente |
| [Histórico de notificaciones](09-notificaciones/67-historico-de-notificaciones.md) | Centro de notificaciones en V1; historial persistente en roadmap |
| [Notificaciones por email](09-notificaciones/68-notificaciones-por-email.md) | Bienvenida y restablecimiento en V1; alertas adicionales en roadmap |

---

### 10. App móvil

Descarga, instalación, navegación y uso de la aplicación CheckBiz360 para empleados.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Descarga e instalación en iOS y Android | **Disponible** | Disponible en App Store y Google Play. |
| Fichaje desde la app con las tres validaciones | **Disponible** | Geocerca, horario y dispositivo validados en tiempo real. |
| Consulta de historial de asistencia propio | **Disponible** | Filtros por período y detalle de cada registro. |
| Acceso a documentos y tareas desde la app | **Disponible** | Navegación desde la notificación al recurso; la descripción de tarea se muestra con formato. |
| Pausar y reanudar tareas, tiempo invertido e historial en la app | **Disponible** | Desde la versión 1.4.0. |
| Lugar de trabajo de la tarea con enlace a Maps | **Disponible** | Desde la versión 1.3.2. |
| Configuración de perfil, 2FA y biometría | **Disponible** | Gestionable desde la sección de perfil de la app. |
| Consulta de datos en caché sin conexión | **Disponible parcialmente** | Solo lectura de datos previamente cargados; fichar y actualizar tareas requiere conexión. |
| Modo offline con cola de sincronización de fichajes | **Pendiente de desarrollo** | Planificado para una versión futura. |

| Artículo | Descripción |
|---|---|
| [Descarga e instalación](10-app-movil/69-descarga-e-instalacion.md) | iOS y Android, requisitos mínimos y permisos necesarios |
| [Primer inicio de sesión](10-app-movil/70-primer-inicio-de-sesion.md) | Activación de cuenta, contraseña y selección de entidad |
| [Navegación principal de la app](10-app-movil/71-navegacion-principal-de-la-app.md) | Las 5 secciones: fichaje, registros, documentos, tareas y perfil |
| [Configuración de perfil en la app](10-app-movil/72-configuracion-de-perfil-en-la-app.md) | Datos personales, contraseña, 2FA y biometría desde la app |
| [Mis registros de asistencia](10-app-movil/73-mis-registros-de-asistencia.md) | Historial propio, filtros, detalle y solicitud de corrección |
| [Uso sin conexión](10-app-movil/74-uso-sin-conexion.md) | Qué datos son accesibles sin conexión y qué requiere conectividad |
| [Actualizaciones de la app](10-app-movil/75-actualizaciones-de-la-app.md) | Novedades por versión, cómo actualizar y consecuencias de versiones desactualizadas |

---

### 11. Informes y exportación

Generación, filtrado y exportación de informes de asistencia, costes y cumplimiento.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Informe de asistencia en PDF o Excel (XLSX) | **Disponible** | Generación bajo demanda, con histórico de informes; recoge al personal de plantilla, no a los colaboradores. |
| Informe de tareas en Excel (XLSX) | **Disponible** | Filtrable por sucursal, estado y periodo de vencimiento; incluye tiempo en pausa y, con el inventario contratado, el material y su coste. |
| Exportación del directorio de empleados | **Pendiente de desarrollo** | El listado se consulta y filtra en pantalla, sin fichero descargable. |
| Informe de cumplimiento RDL 8/2019 para inspecciones | **Disponible** | Generación desde el backoffice. |
| Exportación de los paneles de inteligencia operativa | **Pendiente de desarrollo** | Costes, anomalías y comparativas se consultan en pantalla. |
| Informes automáticos periódicos enviados por email | **Pendiente de desarrollo** | Planificado para una versión futura. |

| Artículo | Descripción |
|---|---|
| [Tipos de informe](11-informes-y-exportacion/76-tipos-de-informe.md) | Asistencia, puntualidad, costes, anomalías y tareas |
| [Generar y filtrar informes](11-informes-y-exportacion/77-generar-y-filtrar-informes.md) | Filtros disponibles, previsualización y configuraciones guardadas |
| [Exportar datos](11-informes-y-exportacion/78-exportar-a-excel-y-csv.md) | Asistencia en PDF o Excel y tareas en Excel |
| [Informe de cumplimiento normativo](11-informes-y-exportacion/79-informe-de-cumplimiento-normativo.md) | Informe para auditorías e inspecciones según RDL 8/2019 |
| [Informes automáticos](11-informes-y-exportacion/80-informes-automaticos.md) | Funcionalidad planificada en roadmap; no disponible en V1 |

---

### 12. Cumplimiento normativo

Registro de jornada obligatorio en España, protección de datos y preparación para inspecciones.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Registro de jornada conforme al RDL 8/2019 | **Disponible** | Timestamp inmutable con trazabilidad completa. |
| Informe de inspección de trabajo | **Disponible** | Generación desde el backoffice con todos los datos requeridos. |
| Conservación de datos conforme a LOPD/RGPD | **Disponible** | Base legal, períodos de retención y derechos de los empleados. |

| Artículo | Descripción |
|---|---|
| [Registro horario obligatorio en España](12-cumplimiento-normativo/81-registro-horario-obligatorio-en-espana.md) | RDL 8/2019: qué exige, ámbito de aplicación y sanciones |
| [Cómo CheckBiz360 cumple el RDL 8/2019](12-cumplimiento-normativo/82-como-checkbiz360-cumple-el-rdl-8-2019.md) | Mecanismos técnicos: timestamp, inmutabilidad, trazabilidad |
| [Conservación y protección de datos](12-cumplimiento-normativo/83-conservacion-y-proteccion-de-datos.md) | LOPD/RGPD: base legal, retención y derechos de los empleados |
| [Preparar una inspección de trabajo](12-cumplimiento-normativo/84-preparar-una-inspeccion-de-trabajo.md) | Qué documentación pedir, qué informe presentar y recomendaciones previas |

---

### 13. Soporte e incidencias

Cómo crear y gestionar incidencias y cómo contactar con el equipo de soporte.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Creación de incidencias desde el backoffice | **Disponible** | Canal interno de la organización: tipo, rol origen/destino, sucursal y comentario. |
| Seguimiento mediante hilo de respuestas | **Disponible** | Tres estados (pendiente, en revisión, resuelto); el estado se cambia al responder. |
| Contacto con soporte técnico por email | **Disponible** | Tiempos de respuesta orientativos, no contractuales. |
| Numeración automática de tickets | **No disponible** | Las incidencias no generan número de referencia automático. |
| Prioridad y adjuntos en una incidencia | **No disponible** | El formulario no contempla ni prioridad ni ficheros adjuntos. |
| Reapertura de una incidencia resuelta | **No disponible** | Una incidencia resuelta no admite más respuestas; se crea una nueva. |
| Exportación del histórico de incidencias | **No disponible** | Se consulta y filtra en pantalla. |

| Artículo | Descripción |
|---|---|
| [Crear una incidencia](13-soporte-e-incidencias/85-crear-una-incidencia.md) | Canal interno de la organización: tipos, campos y creación |
| [Seguimiento y resolución de incidencias](13-soporte-e-incidencias/86-seguimiento-y-resolucion-de-incidencias.md) | Los tres estados, el hilo de respuestas y el historial |
| [Contactar con soporte técnico](13-soporte-e-incidencias/87-contactar-con-soporte-tecnico.md) | Canales, tiempos orientativos y qué información incluir |
| [Problemas frecuentes y soluciones](13-soporte-e-incidencias/88-problemas-frecuentes-y-soluciones.md) | Las 14 situaciones más habituales con pasos de diagnóstico |

---

### 14. Referencia

Glosario, códigos de error, planes y preguntas frecuentes.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Glosario de términos de la plataforma | **Disponible** | Términos principales definidos, incluidos los de tareas e IA. |
| Tabla completa de códigos de error | **Disponible** | Todos los códigos del diccionario, por módulo, con causa y solución. |
| Planes y precios (Bronce y Empresarial) | **Disponible** | Precio, periodo de prueba, módulos incluidos y roadmap. |
| Preguntas frecuentes de evaluación | **Disponible** | 20 preguntas y respuestas para clientes que evalúan la plataforma. |

| Artículo | Descripción |
|---|---|
| [Glosario](14-referencia/89-glosario.md) | Definiciones de los términos principales de la plataforma |
| [Códigos de error completos](14-referencia/90-codigos-de-error-completos.md) | Tabla de todos los códigos de error con causa y solución |
| [Planes, precios y funcionalidades](14-referencia/91-planes-y-funcionalidades.md) | Precio de cada plan, periodo de prueba, módulos incluidos y roadmap |
| [Preguntas frecuentes](14-referencia/92-preguntas-frecuentes.md) | 20 preguntas y respuestas para clientes que evalúan la plataforma |

### 15. Integraciones

Add-ons que conectan CheckBiz360 con otros programas que su empresa ya utiliza, para que la información viaje sola y nadie teclee lo mismo dos veces.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Catálogo de integraciones | **Disponible** | Con su descripción, capacidades y estado |
| RentmanBiz — envío de horas a Rentman | **Disponible** | Automático cada 15 minutos, o al momento |
| RentmanBiz — importación de plantilla, centros y tareas | **Disponible** | Lo incompleto queda pendiente, nunca a medias |
| RentmanBiz — aviso de horas modificadas en Rentman | **Disponible** | El fichaje nunca se sobrescribe |
| Pantalla de configuración del add-on | **Pendiente de desarrollo** | Durante la beta la configura el equipo de Encodebiz |
| Envío de tareas a Rentman | **Pendiente de desarrollo** | Prevista en una versión futura |

| Artículo | Descripción |
|---|---|
| [Qué son las integraciones](15-integraciones/93-que-son-las-integraciones.md) | Qué es un add-on, cómo se activa y qué ocurre al desactivarlo |
| [RentmanBiz](15-integraciones/94-integracion-rentman.md) | Qué aporta la integración con Rentman y qué no hace |
| [Conectar RentmanBiz paso a paso](15-integraciones/95-conectar-rentman.md) | Del token de Rentman a la primera importación |
| [Qué se importa y qué queda pendiente](15-integraciones/97-importacion-y-pendientes.md) | Personas, centros, responsabilidades y tareas; y qué hacer con lo pendiente |
| [Horas imputadas y avisos](15-integraciones/96-horas-imputadas-y-avisos.md) | Cómo leer el panel, las divergencias y las preguntas frecuentes |


---

### 16. Inventario

Complemento de pago: el material atado a la tarea, a la persona, al sitio y a la hora.

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Almacenes ligados a sucursales | **Disponible** | Todo almacén sirve al menos a una sucursal. |
| Artículos consumibles y operables, con ejemplares | **Disponible** | El artículo se crea en su primera entrada. |
| Existencias con estado, mínimos y discrepancias | **Disponible** | Aviso a los responsables al bajar del mínimo. |
| Material asignado al crear la tarea y seguido en su detalle | **Disponible** | Reserva, salida, consumo y cuadre al validar. |
| Salida y consumo desde la app | **Disponible** | Precargado con lo reservado y lo pendiente. |
| Calendario de ejemplares con aviso de choque | **Disponible** | Por ejemplar, en la ficha del artículo. |
| Informe de consumo y libro de movimientos | **Disponible** | Agrupado por artículo, tarea, empleado, sucursal o almacén; CSV. |
| Material en el informe de tareas | **Disponible** | Solo con el complemento contratado. |
| Documentos y revisiones de cada máquina | **Disponible** | Aviso de caducidad y marca en rojo, sin bloquear. |
| Entrega de EPIs confirmada por el trabajador | **Disponible** | Con huella o cara desde la app. |
| Informe «Equipos y EPIs» para inspecciones | **Disponible** | Registro de entregas y dossier por máquina. |
| Importación de material desde una plantilla de Excel | **Disponible** | Por almacén, una para consumibles y otra para operables; se revisa antes de importar y no duplica al volver a subirla. |
| Dónde está cada equipo y equipos fuera de base | **Disponible** | Liberar no lo devuelve al almacén: se dice dónde queda y se recibe en el almacén; historial de dónde ha estado. |
| Material sin tareas: a una persona o a una sucursal | **Disponible** | Dar salida, asignar dotación, declarar desde la jornada en la app y cuadrar desde la ficha; «Fuera del almacén» en Existencias. |

| Artículo | Descripción |
|---|---|
| [Qué es el inventario](16-inventario/100-que-es-el-inventario.md) | Qué problemas resuelve, cómo funciona y cómo se contrata |
| [Existencias, almacenes y entradas](16-inventario/101-existencias-almacenes-y-entradas.md) | Alta del material y control de lo que hay |
| [Material en las tareas](16-inventario/102-material-en-las-tareas.md) | Reservar, sacar, declarar y cuadrar |
| [Informe de consumo y movimientos](16-inventario/103-informe-de-consumo-y-movimientos.md) | Dónde se va el material y cuánto cuesta |
| [Equipos: documentos, revisiones y entregas](16-inventario/104-equipos-documentos-revisiones-y-entregas.md) | Papeles de cada máquina, entregas de EPIs e informe para la inspección |
| [Importar material desde una plantilla](16-inventario/105-importar-material-desde-una-plantilla.md) | Cargar de una vez todo lo que hay en un almacén |
| [Dónde está cada equipo](16-inventario/106-donde-esta-cada-equipo.md) | Equipos libres fuera del almacén, recogerlos y recibirlos |
| [Material sin tareas: personas y centros](16-inventario/107-material-sin-tareas-personas-y-centros.md) | Dar material a una persona o a un centro y declararlo desde la jornada |

---

## Estructura de archivos

```
DOCS/Clients/
├── README.md                          (este índice)
├── 01-primeros-pasos/                 (5 artículos)
├── 02-empleados/                      (8 artículos)
├── 03-control-horario/                (10 artículos)
├── 04-calendario-y-horarios/          (9 artículos)
├── 05-gestion-documental/             (9 artículos)
├── 06-tareas/                         (10 artículos)
├── 07-inteligencia-operativa/         (8 artículos)
├── 08-sucursales-y-entidad/           (6 artículos)
├── 09-notificaciones/                 (6 artículos)
├── 10-app-movil/                      (7 artículos)
├── 11-informes-y-exportacion/         (5 artículos)
├── 12-cumplimiento-normativo/         (4 artículos)
├── 13-soporte-e-incidencias/          (4 artículos)
├── 14-referencia/                     (4 artículos)
├── 15-integraciones/                  (5 artículos)
└── 16-inventario/                     (7 artículos)
```

**Total: 105 artículos**

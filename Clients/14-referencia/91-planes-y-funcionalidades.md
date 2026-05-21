# Planes y funcionalidades de CheckBiz360

CheckBiz360 está organizado en módulos funcionales que se activan según el nivel de plan contratado. Esta estructura permite que cada empresa acceda únicamente a las herramientas que necesita, con la posibilidad de ampliar sus capacidades en cualquier momento desde el backoffice. Este artículo describe qué incluye cada módulo y en qué plan se encuentra disponible.

---

## Estructura modular de la plataforma

CheckBiz360 se organiza en dos niveles de plan:

- **Plan Bronze**
- **Plan Enterprise**

El Plan Enterprise incluye todo lo del Plan Bronze más las funcionalidades avanzadas propias de ese nivel.

---

## Plan Bronze — Control horario, gestión operativa e inteligencia operativa básica

El Plan Bronze cubre las necesidades fundamentales de cualquier empresa que deba cumplir con la obligación de registro horario establecida por el RDL 8/2019, e incorpora además herramientas de gestión operativa y acceso a índices de inteligencia operativa consultables desde el backoffice.

### Control horario y fichajes

- Registro de checkin y checkout desde la app móvil (iOS y Android).
- Validación de fichajes por geolocalización: geocerca configurable por sucursal.
- Configuración de horarios y turnos por sucursal.
- Gestión de calendarios efectivos con soporte para festivos y excepciones.
- Jornadas manuales para corrección retroactiva de registros.
- Historial de fichajes con trazabilidad completa.

### Gestión de empleados

- Alta, baja y modificación de perfiles de empleado.
- Asignación de roles: Owner, Manager, Supervisor, Worker.
- Gestión de dispositivos de confianza.
- Configuración de verificación biométrica requerida por empleado.
- Asignación de sucursales y responsabilidades.
- Envío de invitación de bienvenida y gestión de credenciales.
- Exportación del listado de empleados a CSV.

### Gestión de sucursales

- Creación y configuración de sucursales con coordenadas y radio de fichaje.
- Herencia de configuración desde entidad a sucursal y de sucursal a empleado.
- Gestión de la zona horaria por sucursal.

### Módulo de tareas

- Creación, edición y eliminación de tareas (CRUD completo).
- Asignación de tareas a empleados con fecha límite.
- Seguimiento del estado de las tareas: pendiente, en curso, completada, rechazada.
- Notas y recursos adjuntos por tarea: fotos y vídeos.
- Validación de tareas por el manager con valoración opcional.

### Módulo de incidencias

- Apertura de incidencias desde el backoffice por Owner y Manager.
- Categorización por tipo y prioridad.
- Notificación al equipo de soporte de CheckBiz360 y al Owner de la entidad.
- Seguimiento del estado de la incidencia.

### Notificaciones

- Notificaciones push a empleados por eventos de la plataforma: asignación de tareas, documentos pendientes, cambios de turno y otros eventos operativos.

### Informes de asistencia

- Informe de asistencia en PDF: presencias, ausencias y horas trabajadas por empleado y periodo.

### Inteligencia operativa básica

- Índices consultables desde el backoffice:
  - **Índice de fiabilidad**: consistencia del comportamiento de fichaje de cada empleado a lo largo del tiempo.
  - **Índice de eficiencia**: combina horas trabajadas y tareas completadas.
  - **Puntuación de promoción**: agrega fiabilidad, eficiencia, puntualidad y resolución de tareas.

---

## Plan Enterprise — Todo lo de Bronze, más gestión documental, inteligencia avanzada y multi-entidad

El Plan Enterprise incluye todas las funcionalidades del Plan Bronze y añade el módulo documental, capacidades de inteligencia operativa avanzada, soporte para estructuras multi-entidad y soporte prioritario.

### Gestión documental

- Subida y descarga de documentos laborales: contratos, nóminas, comunicados, políticas de empresa, formación y otros tipos.
- Descarga individual de documentos desde el backoffice y desde la app móvil.
- Acuse de recibo por parte del empleado al acceder al documento.
- Control de visibilidad por rol: documentos accesibles según el perfil del empleado.
- Notificaciones push a los empleados cuando hay documentos nuevos o pendientes de revisión.

### Inteligencia operativa avanzada

- Análisis de costes: cruce de datos de asistencia con información salarial por empleado, sucursal y periodo.
- Indicador de anomalías: identificación de fichajes sospechosos por precisión temporal excesiva, geolocalización estática o procedencia de dispositivos no autorizados.

### Multi-entidad

- Gestión de múltiples empresas o entidades desde una sola cuenta de administración.
- Configuración independiente por entidad: módulos, calendarios y permisos.

### Soporte prioritario

- Atención preferente a incidencias frente a cuentas del Plan Bronze.

---

## Funcionalidades en desarrollo (roadmap)

Las siguientes funcionalidades forman parte del plan de desarrollo de CheckBiz360 y no están disponibles en la versión actual:

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

- **Firma electrónica**: firma de documentos directamente desde la app móvil.
- **Historial de versiones de documentos**: registro de cambios y versiones anteriores de cada documento.
- **Exportación masiva de documentos**: descarga en bloque de múltiples documentos en un solo archivo.
- **Informes automáticos por email**: envío programado de informes de asistencia y operativa a las direcciones configuradas.
- **Exportación CSV/PDF de informes generales**: descarga de informes de costes, anomalías y tareas en formato CSV o PDF.
- **Preferencias de notificación configurables**: personalización por empleado o por sucursal del tipo y frecuencia de notificaciones push recibidas.
- **Estado "vencida" automático en tareas**: cambio automático al estado vencida cuando una tarea supera su fecha límite sin completarse.
- **Modo offline con sincronización**: capacidad de registrar fichajes sin conexión a internet, con sincronización automática al recuperar conectividad.
- **Alertas de coste configurables**: notificaciones cuando el coste operativo de una sucursal o empleado supera umbrales definidos por el administrador.

---

## Cómo cambiar de plan

Si necesita acceder a funcionalidades del Plan Enterprise, puede gestionar el cambio directamente desde el backoffice sin necesidad de contactar con soporte:

1. Inicie sesión en el backoffice con su cuenta de Owner.
2. Acceda a **Configuración** en el menú lateral izquierdo.
3. Seleccione **Suscripción**.
4. En la pantalla de suscripción verá su plan actual y las opciones disponibles para ampliar.
5. Seleccione el Plan Enterprise y siga los pasos del proceso de actualización.
6. Los nuevos módulos estarán disponibles de forma inmediata una vez completado el proceso.

> **Aviso:** El cambio de plan a un nivel superior se aplica de forma inmediata. Si necesita reducir su plan al Plan Bronze, el cambio se aplica al inicio del siguiente periodo de facturación. Los datos generados con módulos del Plan Enterprise no se eliminan al bajar de plan, pero dejarán de ser accesibles hasta que se vuelva a activar el módulo correspondiente.

---

## Nota de rol

La gestión del plan de suscripción es exclusiva del **Owner** de la entidad. Los Managers y otros roles no tienen acceso a la sección de suscripción en el backoffice.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Preguntas frecuentes](./92-preguntas-frecuentes.md) | Respuestas a las dudas más habituales sobre CheckBiz360 |
| [Glosario](./89-glosario.md) | Definición de los términos utilizados en la plataforma |
| [Informe de cumplimiento normativo](../11-informes-y-exportacion/79-informe-de-cumplimiento-normativo.md) | El informe para el RDL 8/2019 y la Inspección de Trabajo |
| [Gestión documental: introducción](../05-gestion-documental/40-introduccion-al-modulo-documental.md) | Primeros pasos en el módulo de documentos |
| [Inteligencia operativa: introducción](../07-inteligencia-operativa/50-introduccion-a-la-inteligencia-operativa.md) | Cómo funciona el módulo de análisis avanzado |

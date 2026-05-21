# Exportar datos: empleados a CSV e informe de asistencia en PDF

CheckBiz360 permite obtener datos fuera de la plataforma en dos escenarios distintos: exportar el listado de empleados en formato CSV y descargar el informe de asistencia en formato PDF. Este artículo describe ambas opciones, los datos que incluyen y las consideraciones prácticas para su uso.

---

## Exportar empleados a CSV

Desde el backoffice es posible exportar el listado completo de empleados de la entidad en formato CSV. Esta función es útil para importar datos en software externo de nóminas, ERPs o herramientas de RRHH.

### Características del archivo CSV exportado

- Codificación **UTF-8** con BOM para garantizar la correcta visualización de caracteres especiales (tildes, ñ) en Excel y otros programas.
- Separador de campos: **punto y coma (;)**.
- Separador decimal: **coma (,)** según el estándar español.
- Valores de texto entrecomillados con comillas dobles cuando contienen el separador o saltos de línea.

> **Aviso:** Si importa el archivo CSV en un software que utilice coma como separador de campos, deberá ajustar la configuración de importación de ese programa o convertir el archivo previamente.

### Cómo exportar el listado de empleados

1. Acceda al backoffice con un rol de Owner o Manager.
2. Navegue a la sección **Empleados**.
3. Pulse el botón **Exportar** o el icono de descarga disponible en la parte superior del listado.
4. El archivo CSV se descargará automáticamente en la carpeta de descargas de su navegador.

### Campos incluidos en la exportación de empleados

El CSV de empleados incluye los datos de ficha de cada empleado registrado en la entidad: nombre completo, dirección de email, sucursal asignada, rol, estado de la cuenta y fecha de alta, entre otros campos identificativos.

---

## Descargar el informe de asistencia en PDF

El informe de asistencia se genera manualmente desde el backoffice y se descarga como archivo PDF. No existe generación automática ni programada; cada descarga la realiza el responsable en el momento en que la necesita.

### Cómo generar y descargar el informe de asistencia

1. Acceda al backoffice con un rol de Owner o Manager.
2. Vaya a la sección **Informes**.
3. Configure los filtros del informe: período, empleado o sucursal según sus necesidades.
4. Pulse **Generar informe**.
5. Una vez generado, pulse **Descargar PDF**.
6. El archivo se descargará en la carpeta de descargas de su navegador.

### Campos incluidos en el informe de asistencia

| Campo | Descripción |
|---|---|
| Nombre | Nombre completo del empleado |
| Sucursal | Sucursal a la que está asignado el empleado |
| Fecha | Fecha del registro (formato DD/MM/AAAA) |
| Hora de entrada | Timestamp del fichaje de entrada |
| Hora de salida | Timestamp del fichaje de salida |
| Horas trabajadas | Total de horas y minutos de la jornada registrada |
| Estado | Completa, ausencia justificada, ausencia no justificada, jornada parcial |

---

## Exportación a Excel/CSV de informes generales

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La posibilidad de exportar los informes de asistencia, costes y otros informes de gestión directamente a formato Excel (.xlsx) o CSV está planificada para una versión futura de la plataforma. Cuando esté disponible, permitirá descargar los datos tabulares de cualquier informe para importarlos en software de nóminas, gestorías o herramientas de análisis.

---

## Consideraciones RGPD al exportar datos de empleados

Los archivos exportados contienen datos personales de los empleados en el sentido del Reglamento General de Protección de Datos (RGPD). La empresa, como responsable del tratamiento, debe tener en cuenta lo siguiente al gestionar estos archivos:

- **Almacenamiento seguro.** Los archivos exportados deben guardarse en ubicaciones con acceso restringido. No deben almacenarse en carpetas compartidas sin control de acceso ni en servicios de almacenamiento en la nube sin cifrado o sin gestión de permisos.
- **Transmisión protegida.** Si envía el archivo por email a su gestoría u otros destinatarios externos, utilice canales cifrados o proteja el archivo con contraseña.
- **Minimización de datos.** Exporte solo los campos y el periodo de datos necesarios para cada finalidad concreta.
- **Registro de actividades.** Si su empresa está obligada a mantener un registro de actividades de tratamiento conforme al artículo 30 del RGPD, la exportación y transmisión de datos de empleados debe estar documentada en dicho registro.
- **Periodo de conservación.** Los archivos exportados deben eliminarse una vez cumplida su finalidad, salvo que exista una obligación legal de conservarlos.

> **Aviso:** CheckBiz360 mantiene los datos originales almacenados en la plataforma con las medidas de seguridad exigidas por la normativa aplicable. Una vez que los datos se exportan y salen de la plataforma, la seguridad de esos archivos es responsabilidad de su empresa.

---

> **Nota:** El acceso a las funciones de exportación requiere rol de Owner o Manager.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Tipos de informe disponibles](./76-tipos-de-informe.md) | Qué contiene cada tipo de informe y quién puede acceder |
| [Generar y filtrar informes](./77-generar-y-filtrar-informes.md) | Pasos para generar un informe con filtros personalizados |
| [Informe de cumplimiento normativo](./79-informe-de-cumplimiento-normativo.md) | El informe para el RDL 8/2019 |
| [Conservación y protección de datos](../12-cumplimiento-normativo/83-conservacion-y-proteccion-de-datos.md) | Base legal y derechos de los empleados sobre sus datos |

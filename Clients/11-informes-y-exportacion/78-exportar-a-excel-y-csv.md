# Exportar datos: asistencia y tareas

CheckBiz360 saca datos de la plataforma mediante **informes**: el de asistencia, en **PDF o Excel (XLSX)**, y el de tareas, en **Excel (XLSX)**. Este artículo describe ambos, los datos que incluyen y las consideraciones prácticas de uso.

---

## Exportar el directorio de empleados

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

El listado de **Empleados** no genera hoy un fichero descargable. Lo que sí funciona es el sentido contrario: la **importación** de empleados desde un CSV, útil al poner en marcha la plataforma con una plantilla grande.

Si necesita una extracción completa del directorio, solicítela a soporte en hola@encodebiz.com. Consulte [Exportar el listado de empleados](../02-empleados/12-exportar-empleados-csv.md).

---

## Descargar el informe de asistencia (PDF o Excel)

El informe de asistencia se genera bajo demanda desde el backoffice y puede descargarse en **PDF** o en **Excel (XLSX)**. No existe generación automática ni programada; cada informe lo lanza el responsable cuando lo necesita.

Elija el formato según el uso: **PDF** para presentar o archivar —es el que conviene ante una inspección—, **Excel** para trabajar los datos en una hoja de cálculo o pasarlos a la gestoría.

### Cómo generar y descargar el informe de asistencia

1. Acceda al backoffice con un rol de Owner o Manager.
2. Vaya a la sección **Informes**.
3. Genere un informe nuevo y seleccione el tipo *Registro de jornada*.
4. Elija el **formato**: PDF o Excel (XLSX).
5. Configure el **periodo** y, si lo necesita, filtre por sucursal o empleado.
6. Genere el informe. Aparecerá en el histórico con su tipo y su formato.
7. Descárguelo desde el histórico, tantas veces como haga falta.

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

## Descargar el informe de tareas (Excel)

El informe de tareas se genera igual que el de asistencia, seleccionando el tipo *Informe de tareas*. Solo se produce en **Excel (XLSX)**.

Admite filtros por **sucursal** y por **estado** de la tarea. El periodo se aplica sobre la **fecha límite** de cada tarea, no sobre su fecha de creación: un informe de julio recoge las tareas que vencían en julio, aunque se crearan antes.

Si ninguna tarea cumple los filtros, el sistema lo indica y no genera un fichero vacío.

---

## Exportación de los paneles de inteligencia operativa

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

La exportación directa de los datos de los paneles —costes, anomalías y comparativas entre sucursales— a Excel o CSV está planificada para una versión futura. Hoy esos datos se consultan en pantalla; lo que sí puede exportarse son los informes de asistencia y de tareas descritos arriba.

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

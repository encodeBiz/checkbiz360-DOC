# Exportar empleados a CSV

CheckBiz360 permite exportar el listado completo de empleados en formato CSV para su uso en procesos de auditoría, sistemas de nóminas, inspecciones de trabajo u otras herramientas de análisis externas. La exportación es una operación rápida que puede realizarse en cualquier momento desde el backoffice.

Este artículo describe el contenido del archivo exportado, cómo obtenerlo y cuáles son sus casos de uso más habituales.

---

## Qué datos incluye la exportación

El archivo CSV generado por CheckBiz360 contiene los siguientes campos por cada empleado:

| Campo | Descripción |
|---|---|
| **Nombre completo** | Nombre y apellidos del empleado. |
| **Correo electrónico** | Email principal del empleado en la plataforma. |
| **Teléfono** | Número de contacto, si está registrado. |
| **DNI / Número de identificación** | Documento de identidad nacional del empleado. |
| **Puesto de trabajo** | Cargo o función asignada al empleado. |
| **Rol** | Nivel de rol en la plataforma (worker, supervisor, manager, owner). |
| **Sucursales asignadas** | Listado de sucursales a las que pertenece el empleado. |
| **Estado** | Situación laboral actual (activo, inactivo, baja, vacaciones, etc.). |
| **Fecha de alta** | Fecha en la que el empleado fue dado de alta en la plataforma. |

Los campos no completados en el perfil del empleado aparecerán vacíos en la columna correspondiente del archivo.

---

## Cómo exportar el listado de empleados

### Pasos para realizar la exportación

1. Acceda al backoffice de CheckBiz360 con credenciales de manager u owner.
2. En el menú lateral, seleccione **Empleados**.
3. Si desea exportar solo un subconjunto de empleados (por ejemplo, los de una sucursal concreta o los que estén en un estado determinado), aplique los filtros disponibles antes de exportar.
4. Pulse el botón **Exportar** o **Exportar CSV**, ubicado en la parte superior del listado.
5. El sistema generará el archivo y lo descargará automáticamente en su dispositivo.

El archivo se descarga con un nombre que incluye la fecha de la exportación para facilitar su identificación y archivo.

---

## Formato del archivo

El archivo exportado cumple las siguientes especificaciones técnicas:

- **Formato:** CSV (valores separados por delimitador).
- **Codificación:** UTF-8 con BOM, para garantizar la correcta visualización de caracteres especiales (tildes, eñes) en Microsoft Excel y otras herramientas de hoja de cálculo.
- **Separador de campos:** punto y coma (`;`).
- **Primera fila:** cabecera con los nombres de los campos.

> **Nota:** Si al abrir el archivo en Excel los datos aparecen en una sola columna, utilice la función **Datos > Texto en columnas** y seleccione el punto y coma como delimitador. Alternativamente, abra el archivo directamente desde Excel usando la opción **Importar datos desde texto/CSV** y configure el separador durante el proceso de importación.

---

## Casos de uso habituales

### Auditorías de recursos humanos

La exportación permite obtener una fotografía completa del equipo en un momento dado: quién está activo, en qué sucursal trabaja, cuál es su puesto y cuándo fue dado de alta. Este documento es útil en revisiones internas periódicas o en procesos de auditoría externa.

### Importación a sistemas de nóminas

Muchos sistemas de gestión de nóminas requieren disponer del listado de empleados en formato CSV para sincronizar altas, bajas y cambios de situación. La exportación de CheckBiz360 facilita este intercambio de datos sin necesidad de introducir la información manualmente.

### Reportes de inspección de trabajo

En caso de inspección por parte de la autoridad laboral, disponer de un listado exportado y fechado de todos los empleados con su estado y fecha de alta permite demostrar de forma ordenada la situación del equipo en cualquier momento del tiempo.

### Copias de seguridad del directorio de empleados

Algunos responsables de RRHH realizan exportaciones periódicas como práctica de respaldo documental, especialmente antes de migraciones de sistema o cambios organizativos relevantes.

---

## Buenas prácticas al gestionar archivos exportados

Los archivos CSV exportados contienen datos personales de los empleados (nombre, email, DNI). Por tanto, deben manejarse con las siguientes precauciones:

- Almacene los archivos en ubicaciones con acceso restringido, no en carpetas compartidas de acceso general.
- No envíe los archivos por canales de comunicación no cifrados (como email sin cifrar) si contienen datos sensibles como el DNI.
- Elimine las exportaciones antiguas una vez que ya no sean necesarias, en cumplimiento de la normativa de protección de datos vigente.

> **Nota:** La exportación de datos de empleados está sujeta a la normativa de protección de datos aplicable en su país (por ejemplo, el Reglamento General de Protección de Datos en la Unión Europea). Asegúrese de que el tratamiento de estos datos se realiza con la base legal adecuada y dentro de las finalidades establecidas en su política de privacidad interna.

---

## Quién puede realizar estas acciones

La exportación del listado de empleados está disponible exclusivamente para los roles **manager** (nivel 3) y **owner** (nivel 4).

---

## Artículos relacionados

- [Crear y gestionar empleados](06-crear-y-gestionar-empleados.md)
- [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md)
- [Matriz de permisos por rol](08-matriz-de-permisos-por-rol.md)
- [Generar informes](../11-informes-y-exportacion/)

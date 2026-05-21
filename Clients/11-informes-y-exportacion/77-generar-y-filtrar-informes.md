# Generar y filtrar informes

El módulo de informes del backoffice de CheckBiz360 permite obtener documentos detallados sobre la actividad de su equipo en cualquier periodo. Esta guía explica el proceso completo para generar un informe, los filtros disponibles, cómo previsualizar el resultado antes de exportar y cómo guardar configuraciones frecuentes para reutilizarlas.

---

## Acceder al módulo de informes

Para generar un informe debe acceder al backoffice de CheckBiz360 con un rol de Owner, Manager o, si el manager lo ha habilitado, Supervisor.

1. Inicie sesión en el backoffice desde su navegador.
2. En el menú lateral izquierdo, seleccione la sección **Informes**.
3. Verá el panel de informes con los cinco tipos disponibles: Asistencia, Puntualidad, Costes, Anomalías y Tareas.
4. Seleccione el tipo de informe que desea generar.

---

## Filtros disponibles

Antes de generar el informe puede ajustar los parámetros de filtrado. Cuanto más específicos sean los filtros, más enfocado será el resultado y menor será el tiempo de generación.

### Rango de fechas

El filtro de fechas es obligatorio. Dispone de las siguientes opciones predefinidas:

- **Hoy:** solo el día en curso.
- **Esta semana:** lunes a domingo de la semana en curso.
- **Este mes:** mes natural en curso.
- **Rango personalizado:** seleccione una fecha de inicio y una fecha de fin en el calendario. Puede abarcar hasta 12 meses consecutivos en una sola consulta.

> **Aviso:** Los periodos superiores a tres meses pueden tardar varios minutos en procesarse, dependiendo del tamaño de su plantilla y del número de registros acumulados. Se le mostrará una barra de progreso durante la generación.

### Empleado

Puede filtrar por un empleado concreto o incluir a todos los empleados del ámbito que gestiona. Si selecciona un empleado específico, el informe mostrará únicamente sus registros.

### Sucursal

Si su entidad tiene más de una sucursal, puede seleccionar una sucursal concreta o incluir todas. Los owners y managers con acceso multicentro ven todas las sucursales; los managers con acceso restringido solo ven las suyas.

### Tipo de evento

Disponible en el informe de asistencia. Permite filtrar por categoría de registro:

- Entradas y salidas únicamente.
- Ausencias (justificadas, no justificadas o ambas).
- Correcciones manuales realizadas por un responsable.
- Todos los eventos del periodo.

---

## Previsualización antes de exportar

Una vez configurados los filtros, pulse **Previsualizar** para ver el informe en pantalla antes de descargarlo. La previsualización muestra los mismos datos que contendrá el archivo exportado y permite detectar posibles errores en la selección de filtros sin necesidad de descargar el documento.

En la previsualización puede:

- Navegar por las páginas del informe.
- Verificar que los empleados y fechas incluidos son los correctos.
- Comprobar totales y subtotales.

Si detecta que los filtros no son los adecuados, pulse **Volver a filtros** y ajústelos sin perder la configuración parcial.

---

## Guardar configuraciones de informe frecuentes

Si genera habitualmente el mismo tipo de informe con los mismos parámetros (por ejemplo, el informe de asistencia mensual de una sucursal concreta), puede guardar esa configuración para reutilizarla.

1. Configure los filtros deseados.
2. Pulse **Guardar configuración**.
3. Asigne un nombre descriptivo, por ejemplo: "Asistencia mensual — Sucursal Centro".
4. La configuración quedará disponible en la sección **Mis informes guardados**, accesible desde el panel principal del módulo.

Para ejecutar una configuración guardada, selecciónela desde la lista y pulse **Generar**. Solo tendrá que ajustar el rango de fechas si la configuración usaba un rango relativo como "este mes".

> **Nota:** Las configuraciones guardadas son personales de cada usuario del backoffice y no se comparten entre cuentas.

---

## Tiempo de generación

El tiempo de generación depende de tres factores: el número de empleados incluidos, el rango de fechas seleccionado y el tipo de informe.

| Escenario | Tiempo estimado |
|---|---|
| Hasta 20 empleados, 1 mes | Menos de 10 segundos |
| Hasta 20 empleados, 6 meses | 10 a 30 segundos |
| Más de 100 empleados, 12 meses | 1 a 5 minutos |

Para periodos largos con plantillas grandes, le recomendamos iniciar la generación del informe y mantener la pestaña abierta. El sistema le notificará cuando el informe esté listo para descargar.

---

> **Nota:** El rol Supervisor solo puede generar informes si el manager ha habilitado ese permiso específico en su configuración de acceso. Si no visualiza la sección de informes en el backoffice, contacte con el manager de su entidad.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Tipos de informe disponibles](./76-tipos-de-informe.md) | Descripción de cada tipo de informe y acceso por rol |
| [Exportar a Excel y CSV](./78-exportar-a-excel-y-csv.md) | Formatos de exportación y campos incluidos |
| [Informe de cumplimiento normativo](./79-informe-de-cumplimiento-normativo.md) | El informe específico para el RDL 8/2019 |
| [Informes automáticos](./80-informes-automaticos.md) | Envío periódico de informes por email |

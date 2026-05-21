# Crear y gestionar sucursales

Una sucursal en CheckBiz360 representa una unidad operativa física o lógica a la que se asignan empleados y desde la que se controla el fichaje. Puede corresponderse con una tienda, una oficina, un centro de trabajo o cualquier otra unidad que la empresa necesite gestionar de forma independiente. Este artículo explica cómo crear la primera sucursal, cómo completar su configuración y cómo editarla o desactivarla posteriormente.

## Requisitos previos

Para crear y gestionar sucursales necesita acceder al backoffice web con un rol de **Owner** o **Manager** con permisos de administración de sucursales. Si no dispone de los permisos necesarios, contacte con el Owner de su entidad.

## Crear una sucursal

### Campos obligatorios

Al crear una sucursal deberá cumplimentar los siguientes campos:

- **Nombre**: identificador visible de la sucursal en todo el sistema. Utilice un nombre claro y único dentro de su organización (por ejemplo, "Madrid Centro" o "Almacén Norte").
- **Dirección**: dirección postal completa del centro de trabajo. El sistema geocodifica automáticamente esta dirección para obtener las coordenadas GPS que se utilizarán como punto central de la geocerca de fichaje. Es importante que la dirección sea precisa para garantizar la exactitud de las coordenadas.
- **Radio de fichaje**: distancia en metros desde el punto central de la sucursal dentro de la cual el sistema considera válido un fichaje por geolocalización. Un radio de 100 metros es el valor recomendado para oficinas en entornos urbanos; puede ampliarse para instalaciones industriales o espacios abiertos.
- **Zona horaria**: zona horaria en la que opera la sucursal. Este parámetro determina cómo se interpretan los timestamps de fichaje y cómo se calculan las jornadas. Es especialmente relevante en organizaciones con sucursales en distintos países o regiones.

### Campos opcionales

- **Descripción**: texto libre para identificar la sucursal con más detalle. Visible únicamente en el backoffice para los administradores.
- **Estado**: activa o inactiva. Por defecto, una sucursal recién creada queda activa.
- **Configuración avanzada**: parámetros adicionales descritos en el artículo de configuración avanzada. Pueden dejarse con sus valores por defecto en el momento de la creación y ajustarse posteriormente.

### Pasos para crear la primera sucursal

1. Acceda al backoffice web en `app.checkbiz360.com` e inicie sesión con sus credenciales.
2. En el menú lateral, seleccione **Organización** y luego **Sucursales**.
3. Pulse el botón **Nueva sucursal** en la esquina superior derecha.
4. Introduzca el nombre de la sucursal en el campo correspondiente.
5. Escriba la dirección postal completa en el campo **Dirección**. Seleccione la sugerencia que aparece en el desplegable de autocompletado para asegurarse de que el sistema obtiene las coordenadas correctas.
6. Compruebe que el mapa interactivo muestra el marcador en la posición correcta. Si la posición no es exacta, puede arrastrar el marcador manualmente para ajustarla.
7. Introduzca el radio de fichaje en metros. Si no tiene un criterio definido, comience con 100 metros y ajústelo tras las primeras semanas de operación.
8. Seleccione la zona horaria correspondiente en el desplegable.
9. Complete los campos opcionales si lo considera necesario.
10. Pulse **Guardar**. El sistema confirmará la creación con un mensaje de éxito y la nueva sucursal aparecerá en el listado.

> **Aviso:** Si la geocodificación de la dirección no devuelve coordenadas precisas, el sistema lo indicará con una advertencia. En ese caso, ajuste el marcador manualmente en el mapa antes de guardar. Coordenadas incorrectas generarán rechazos de fichaje injustificados para los empleados asignados.

## Editar una sucursal

Para modificar los datos de una sucursal existente:

1. Acceda a **Organización** > **Sucursales** en el menú lateral.
2. Localice la sucursal que desea editar y pulse sobre su nombre o el icono de edición.
3. Modifique los campos que necesite actualizar.
4. Si cambia la dirección, el sistema geocodificará de nuevo y actualizará las coordenadas. Compruebe el mapa antes de guardar.
5. Pulse **Guardar cambios**.

> **Aviso:** Los cambios en el radio de fichaje o en las coordenadas tienen efecto inmediato. Los empleados que estén intentando fichar en ese momento pueden verse afectados transitoriamente.

## Desactivar una sucursal

Desactivar una sucursal impide que los empleados asignados puedan fichar desde ella, pero conserva todo el histórico de datos. Esta operación es reversible.

1. Acceda a **Organización** > **Sucursales**.
2. Pulse el icono de edición de la sucursal que desea desactivar.
3. Cambie el campo **Estado** a **Inactiva**.
4. Pulse **Guardar cambios**.

El sistema le mostrará un aviso indicando cuántos empleados están asignados a esa sucursal y se verán afectados. Consulte el artículo sobre estados de una sucursal para comprender el impacto completo de esta acción.

---

> **Nota de rol:** La creación y edición de sucursales está disponible para los roles **Owner** y **Manager** con permisos de administración de organización. La consulta del listado de sucursales también está disponible para **Supervisor**.

## Artículos relacionados

- [Configuración avanzada de sucursal](58-configuracion-avanzada-de-sucursal.md)
- [Estados de una sucursal](59-estados-de-una-sucursal.md)
- [Asignar empleados a sucursales](60-asignar-empleados-a-sucursales.md)
- [Configuración de entidad](61-configuracion-de-entidad.md)
- [Vista global multi-sucursal](62-vista-global-multi-sucursal.md)

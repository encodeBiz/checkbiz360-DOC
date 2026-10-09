# Crear y gestionar sucursales

Una sucursal en CheckBiz360 representa una unidad operativa física o lógica a la que se asignan empleados y desde la que se controla el fichaje. Puede corresponderse con una tienda, una oficina, un centro de trabajo o cualquier otra unidad que la empresa necesite gestionar de forma independiente. Este artículo explica cómo crear la primera sucursal, cómo completar su configuración y cómo editarla o desactivarla posteriormente.

## Requisitos previos

Para crear y gestionar sucursales necesita acceder al backoffice web con un rol de **Owner** o **Manager** con permisos de administración de sucursales. Si no dispone de los permisos necesarios, contacte con el Owner de su entidad.

## Crear una sucursal

### Campos obligatorios

Al crear una sucursal deberá cumplimentar los siguientes campos:

- **Nombre**: identificador visible de la sucursal en todo el sistema. Utilice un nombre claro y único dentro de su organización (por ejemplo, "Madrid Centro" o "Almacén Norte").
- **Dirección**: dirección postal completa del centro de trabajo, elegida del buscador. El sistema obtiene de ella las coordenadas GPS que se utilizarán como punto central de la geocerca de fichaje, y rellena solos el **país** y el **código postal**. No hay campo de ciudad: la dirección normalizada ya la incluye. Es importante que la dirección sea precisa para garantizar la exactitud de las coordenadas.
- **Radio de fichaje**: distancia en metros desde el punto central de la sucursal dentro de la cual el sistema considera válido un fichaje por geolocalización. Un radio de 100 metros es el valor recomendado para oficinas en entornos urbanos; puede ampliarse para instalaciones industriales o espacios abiertos.
- **Zona horaria**: forma parte de la dirección y determina cómo se interpretan las horas de fichaje y cómo se calculan las jornadas. Es especialmente relevante en organizaciones con centros en distintos países o regiones. Si no se indica, la sucursal hereda la zona horaria de la entidad.

### Campos opcionales

- **NIF**: identificador fiscal del centro, cuando difiere del de la entidad.
- **Estado**: activa o inactiva. Por defecto, una sucursal recién creada queda activa.
- **Datos adicionales**: campos libres en formato clave/valor para información propia de su organización.
- **Calendario**: horario semanal, pausas y modalidad de jornada. Si no se configura, la sucursal hereda el calendario de la entidad.

### Pasos para crear la primera sucursal

1. Acceda al backoffice en `saas.encodebiz.com` e inicie sesión con sus credenciales.
2. En el menú lateral, seleccione **Sucursales** (o el nombre que su entidad dé a sus centros).
3. Pulse el botón de crear sucursal.
4. Introduzca el nombre de la sucursal en el campo correspondiente.
5. Escriba la dirección postal completa en el campo **Dirección**. Seleccione la sugerencia que aparece en el desplegable de autocompletado para asegurarse de que el sistema obtiene las coordenadas correctas.
6. Compruebe que el mapa interactivo muestra el marcador en la posición correcta. Si la posición no es exacta, puede arrastrar el marcador manualmente para ajustarla.
7. Introduzca el radio de fichaje en metros. Si no tiene un criterio definido, comience con 100 metros y ajústelo tras las primeras semanas de operación.
8. Compruebe la zona horaria asociada a la dirección.
9. Complete los campos opcionales si lo considera necesario.
10. Pulse **Guardar**. El sistema confirmará la creación con un mensaje de éxito y la nueva sucursal aparecerá en el listado.

> **Aviso:** Si la geocodificación de la dirección no devuelve coordenadas precisas, el sistema lo indicará con una advertencia. En ese caso, ajuste el marcador manualmente en el mapa antes de guardar. Coordenadas incorrectas generarán rechazos de fichaje injustificados para los empleados asignados.

> **Nota:** el código postal admite letras, espacios y guiones, de modo que se pueden dar de alta centros fuera de España («EC2V 8AS», «3512 EN», «K1A 0B1»). El país se toma de la dirección elegida; si su centro está en otro país, búsquelo con la dirección completa.

> **Nota:** al dar de alta el servicio, CheckBiz360 crea una primera sucursal con los datos de la empresa. Revísela antes de crear otras.

## Editar una sucursal

Para modificar los datos de una sucursal existente:

1. Acceda a **Sucursales** en el menú lateral.
2. Localice la sucursal que desea editar y pulse sobre su nombre o el icono de edición.
3. Modifique los campos que necesite actualizar.
4. Si cambia la dirección, el sistema geocodificará de nuevo y actualizará las coordenadas. Compruebe el mapa antes de guardar.
5. Pulse **Guardar cambios**.

> **Aviso:** Los cambios en el radio de fichaje o en las coordenadas tienen efecto inmediato. Los empleados que estén intentando fichar en ese momento pueden verse afectados transitoriamente.

Editar solo cambia lo que usted modifica. En particular, si la sucursal tiene **desactivada la zona de chequeo**, guardar otros cambios no la vuelve a activar.

Si la sucursal fue creada por una integración (por ejemplo, un montaje importado de Rentman), su ficha muestra un distintivo con el origen. Puede editarla con normalidad; los datos de procedencia que guarda la integración no se pierden al guardar.

## Desactivar una sucursal

Desactivar una sucursal impide que los empleados asignados puedan fichar desde ella, pero conserva todo el histórico de datos. Esta operación es reversible.

1. Acceda a **Sucursales**.
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

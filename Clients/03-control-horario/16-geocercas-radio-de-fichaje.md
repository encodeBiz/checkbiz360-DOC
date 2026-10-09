# Geocercas y radio de fichaje

La geocerca es el mecanismo por el cual CheckBiz360 garantiza que un empleado se encuentra físicamente en el lugar de trabajo en el momento de registrar su asistencia. Este artículo explica qué es una geocerca, cómo configurarla correctamente y qué ocurre cuando un empleado intenta fichar fuera del área permitida.

---

## Qué es una geocerca

Una geocerca es un perímetro circular definido en torno a las coordenadas GPS de una sucursal. Su función es establecer el área dentro de la cual se considera válido un fichaje presencial. Cuando un empleado pulsa el botón de fichaje, la app envía las coordenadas de su dispositivo y el sistema calcula la distancia entre ese punto y el centro de la sucursal. Si la distancia supera el radio configurado, el fichaje se rechaza.

El radio se expresa en metros y puede ajustarse a la superficie y las características físicas de cada instalación.

---

## Cómo configurar el radio de fichaje

El radio de fichaje se configura a nivel de sucursal, aceptando un valor entero en metros.

1. Acceda al backoffice de CheckBiz360 con rol **manager** u **owner**.
2. Navegue a la sección **Sucursales** y seleccione la sucursal que desea configurar.
3. Abra la pestaña de configuración de asistencia o ajustes de la sucursal.
4. Localice el campo **Radio de fichaje** e introduzca el valor en metros.
5. Asegúrese de que las coordenadas GPS de la sucursal estén correctamente definidas. El radio no tiene utilidad si el punto central no está bien ubicado.
6. Guarde los cambios. La nueva configuración se aplica de forma inmediata a los siguientes fichajes.

---

## Cómo desactivar la validación de geocerca

En algunas situaciones, la validación de geocerca no es aplicable: sucursales sin dirección fija, entornos de trabajo en campo o instalaciones con coordenadas GPS poco precisas.

Para deshabilitar la geocerca en una sucursal concreta, active la opción "desactivar validación de geocerca" en la configuración de esa sucursal.

1. Acceda a la configuración de la sucursal como se describe en el apartado anterior.
2. Active el campo **Desactivar validación de geocerca**.
3. Guarde los cambios.

Con esta opción activa, el sistema omite la comprobación de distancia para todos los empleados asignados a esa sucursal. El resto de validaciones (horario, dispositivo, biometría) continúan aplicándose con normalidad.

> **Nota:** Esta opción es diferente del **trabajo fuera del centro**. "Desactivar validación de geocerca" afecta a todos los empleados de la sucursal, mientras que el trabajo fuera del centro es una configuración individual de cada empleado.

---

## Qué ocurre cuando el empleado está fuera del radio

Si el empleado intenta fichar desde una ubicación fuera del radio permitido, el sistema:

1. Registra el intento de fichaje con estado `failed`.
2. Asigna el código de error `checklog/out_of_radius`.
3. Almacena la distancia real entre la ubicación del dispositivo y el centro de la geocerca, así como el radio configurado en ese momento.

Esta información queda disponible en el historial del empleado y puede ser consultada por el responsable desde el backoffice. Permite identificar si el problema es puntual (el empleado estaba en otro edificio del recinto) o sistemático (el radio está mal dimensionado).

El empleado ve en la app un mensaje indicando que está fuera de la zona de fichaje.

---

## Recomendaciones de radio según el tipo de instalación

La elección del radio adecuado depende del tamaño y la distribución física del lugar de trabajo. A continuación se ofrecen valores orientativos:

| Tipo de instalación | Radio recomendado |
|---|---|
| Oficina pequeña o local comercial | 50 – 100 metros |
| Nave industrial o almacén | 200 – 500 metros |
| Campus universitario o recinto industrial grande | 500 – 1.000 metros |
| Edificio de oficinas con varias plantas | 100 – 200 metros |

Estos valores son orientativos. Se recomienda validar el radio in situ: pida a un empleado que realice un fichaje de prueba desde los puntos más alejados del recinto para comprobar que el radio cubre correctamente el área de trabajo.

Un radio excesivamente pequeño genera fichajes fallidos innecesarios. Un radio excesivamente grande reduce la efectividad del control de presencia. Busque el equilibrio que se ajuste a la realidad física de la instalación.

---

> **Aviso sobre dispositivos GPS:** La precisión de la geolocalización depende del dispositivo móvil y de las condiciones del entorno (interiores, zonas con señal débil, dispositivos con GPS desactivado). En entornos con baja precisión GPS, considere ampliar ligeramente el radio para evitar falsos rechazos.

---

## Roles con acceso a esta funcionalidad

La configuración de geocercas y radio de fichaje requiere rol **manager** u **owner**. Los empleados no tienen acceso a esta configuración.

---

## Artículos relacionados

- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)
- [Trabajo fuera del centro](15-fichaje-en-remoto.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)
- [Check-in y check-out desde la app](14-checkin-checkout-desde-app.md)

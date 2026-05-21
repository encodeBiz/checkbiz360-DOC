# Configuración de entidad

La entidad es el nivel organizativo superior en CheckBiz360. Representa a la empresa o grupo empresarial que ha contratado el servicio y engloba a todas las sucursales, empleados y datos de la organización. La configuración de la entidad establece los parámetros globales que afectan a toda la estructura y que actúan como valores de referencia para el sistema. Este artículo explica qué se configura a nivel de entidad, cómo los cambios se propagan a las sucursales y quién tiene acceso a esta sección.

## Qué se configura a nivel de entidad

### Datos fiscales y de identificación

- **Razón social**: nombre legal de la empresa, que aparece en los informes exportables y en la documentación generada por el sistema.
- **NIF/CIF**: identificador fiscal de la entidad. Utilizado en documentos de cumplimiento normativo.
- **Dirección fiscal**: dirección legal registrada de la empresa.
- **Sector de actividad**: clasificación de la empresa por sector, que puede influir en las plantillas de calendario disponibles y en los convenios colectivos de referencia.

### Zona horaria global

La zona horaria de la entidad actúa como valor por defecto para todas las sucursales que no tengan una zona horaria específica configurada. Si su organización opera íntegramente en una misma zona horaria, puede dejar que todas las sucursales hereden este valor en lugar de configurarlo individualmente.

> **Aviso:** Si modifica la zona horaria global de la entidad, el cambio se aplica únicamente a las sucursales que no tienen una zona horaria propia configurada. Las sucursales con zona horaria específica no se ven afectadas.

### Configuración de seguridad

#### Autenticación de dos factores (2FA)

Desde la configuración de entidad puede establecer si el 2FA es obligatorio para todos los accesos al backoffice web. Cuando está activado:

- Todos los usuarios con acceso al backoffice (Owner, Manager, Supervisor) deben configurar y utilizar un segundo factor de autenticación.
- Si un usuario intenta acceder sin tener el 2FA configurado, el sistema le obliga a completar la configuración antes de continuar.
- Esta política se aplica a todos los usuarios de la entidad sin excepción y no puede desactivarse a nivel individual.

> **Aviso:** Activar el 2FA obligatorio de forma retroactiva afectará a todos los usuarios activos en el siguiente inicio de sesión. Comunique este cambio a los responsables de su organización con antelación para evitar bloqueos de acceso inesperados.

### Configuración de facturación

Desde esta sección el Owner puede consultar el plan contratado, el número de empleados activos incluidos en el plan y el historial de facturación. La gestión de métodos de pago también está disponible aquí.

## Cómo los cambios en la entidad se propagan a las sucursales

Los parámetros de la entidad funcionan como valores de referencia que las sucursales pueden heredar o sobreescribir individualmente. La jerarquía de configuración es la siguiente:

1. **Configuración de entidad**: define el valor global por defecto.
2. **Configuración de sucursal**: si se especifica un valor para ese parámetro en la sucursal, tiene prioridad sobre el valor global.

Por ejemplo, si la zona horaria global de la entidad es "Europe/Madrid" y una sucursal en Canarias tiene configurada "Atlantic/Canary", esa sucursal utilizará su propia zona horaria. El resto de sucursales sin configuración específica heredarán "Europe/Madrid".

Los parámetros que no tienen equivalente a nivel de sucursal (como los datos fiscales o el 2FA obligatorio) son estrictamente globales y se aplican a toda la organización sin excepción.

## Quién puede modificar la configuración de entidad

El acceso a la configuración de entidad está restringido exclusivamente al rol **Owner**. Ningún otro rol, incluyendo Manager y Supervisor, puede acceder a esta sección ni modificar ninguno de sus parámetros.

Esta restricción es deliberada: los cambios a nivel de entidad tienen un alcance global y pueden afectar a toda la organización de forma inmediata. La concentración de este acceso en el rol Owner garantiza que solo la persona responsable de la cuenta tenga capacidad de modificar estos parámetros críticos.

Si necesita delegar parcialmente la gestión de la organización, utilice el rol Manager, que permite administrar sucursales y empleados sin acceder a la configuración de entidad.

## Diferencia entre configuración de entidad y configuración de sucursal

Aunque ambos niveles de configuración comparten algunos parámetros (como la zona horaria), existen diferencias fundamentales:

| Aspecto | Configuración de entidad | Configuración de sucursal |
|---|---|---|
| Alcance | Toda la organización | Un único centro de trabajo |
| Acceso | Solo Owner | Owner y Manager |
| Parámetros exclusivos | Datos fiscales, 2FA obligatorio, facturación | Radio de fichaje, geocerca, pausa, tolerancias |
| Herencia | Actúa como valor por defecto | Puede sobreescribir valores de entidad |
| Impacto de un cambio | Afecta a toda la organización | Afecta solo a esa sucursal y sus empleados |

La regla general es sencilla: todo lo que afecta a la empresa como conjunto se configura en la entidad; todo lo que es específico de un centro de trabajo se configura en la sucursal.

## Cómo acceder a la configuración de entidad

1. Acceda al backoffice web e inicie sesión con una cuenta con rol **Owner**.
2. En el menú lateral, seleccione **Configuración** y luego **Entidad**.
3. Modifique los parámetros que necesite.
4. Pulse **Guardar cambios** al finalizar.

> **Aviso:** Algunos cambios, como activar el 2FA obligatorio, tienen efecto inmediato para todos los usuarios. Otros, como modificar los datos fiscales, solo afectan a los documentos generados a partir de ese momento y no alteran los documentos ya emitidos.

---

> **Nota de rol:** El acceso a la configuración de entidad está reservado exclusivamente al rol **Owner**. Los roles **Manager**, **Supervisor** y **Worker** no tienen acceso a esta sección.

## Artículos relacionados

- [Crear y gestionar sucursales](57-crear-y-gestionar-sucursales.md)
- [Configuración avanzada de sucursal](58-configuracion-avanzada-de-sucursal.md)
- [Asignar empleados a sucursales](60-asignar-empleados-a-sucursales.md)
- [Vista global multi-sucursal](62-vista-global-multi-sucursal.md)

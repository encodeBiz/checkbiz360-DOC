# Biometría y dispositivos de confianza

CheckBiz360 incorpora un sistema de verificación biométrica que permite garantizar que el fichaje lo realiza la persona correcta desde el dispositivo correcto. Esta capa de seguridad es especialmente relevante en entornos donde la presencia física y la identidad del empleado deben quedar acreditadas de forma inequívoca.

Este artículo explica cómo funciona la validación biométrica, qué es un dispositivo de confianza y cómo gestionar ambos elementos desde el backoffice.

---

## Validación biométrica en CheckBiz360

La validación biométrica es un paso de verificación que CheckBiz360 puede requerir al empleado antes de registrar un fichaje. Según el dispositivo del empleado, esta verificación se realiza mediante:

- **Reconocimiento facial (Face ID)** — Disponible en dispositivos iOS compatibles y algunos modelos Android.
- **Huella dactilar** — Disponible en dispositivos con sensor de huellas integrado (TouchID u equivalentes Android).

Cuando la validación biométrica está habilitada para un empleado, la aplicación solicita la autenticación biométrica en el momento del fichaje. Solo si la verificación es exitosa se registra la entrada o salida.

---

## Verificación biométrica requerida

Cada perfil de empleado incluye la opción **verificación biométrica requerida**, que determina si la autenticación biométrica es obligatoria para ese usuario al realizar fichajes.

- **Activo** — El empleado debe verificar su identidad biométrica antes de cada fichaje. Este es el valor por defecto para todos los empleados nuevos.
- **Inactivo** — El empleado puede fichar sin verificación biométrica adicional.

> **Nota:** Por razones de seguridad, la verificación biométrica requerida está activada de forma predeterminada en todos los perfiles creados nuevos. Desactivarla requiere una decisión explícita por parte del manager u owner.

---

## Cómo desactivar la biometría para un empleado específico

Existen situaciones en las que puede ser necesario desactivar la verificación biométrica para un empleado concreto, por ejemplo, cuando el dispositivo del empleado no dispone de sensor biométrico o cuando existe una incidencia técnica puntual.

Para desactivar este requisito:

1. Acceda al backoffice con credenciales de manager u owner.
2. Vaya a **Empleados** y abra el perfil del empleado.
3. En la sección **Seguridad**, localice el control **Verificación biométrica requerida**.
4. Desactive el interruptor.
5. Guarde los cambios.

El cambio tiene efecto inmediato. El empleado podrá fichar en su próximo acceso sin necesidad de verificación biométrica.

---

## Dispositivos de confianza

CheckBiz360 controla desde qué dispositivos puede fichar cada empleado mediante un sistema de dispositivos de confianza. Cuando un empleado inicia sesión y completa el proceso de verificación (incluido el 2FA, si está activo), el sistema registra el identificador único del dispositivo (UUID).

Solo los dispositivos registrados como de confianza pueden realizar fichajes. Si un empleado intenta fichar desde un dispositivo que no está registrado, la aplicación mostrará el error:

```
Untrusted device
```

Este comportamiento protege la integridad del control horario, impidiendo que un tercero suplante al empleado desde un dispositivo no autorizado.

---

## Cómo registrar un nuevo dispositivo

Si un empleado cambia de dispositivo o necesita añadir un nuevo teléfono como dispositivo de confianza, el proceso es el siguiente:

1. El empleado instala la aplicación de CheckBiz360 en su nuevo dispositivo.
2. Inicia sesión con sus credenciales (email y contraseña).
3. Si el 2FA está activo, introduce el código de verificación generado por su aplicación autenticadora.
4. Una vez completado el proceso de autenticación, el sistema registra automáticamente el nuevo dispositivo como de confianza.

A partir de ese momento, el empleado puede fichar desde el nuevo dispositivo.

---

## Gestión de dispositivos desde el backoffice

Los managers y owners pueden consultar y gestionar los dispositivos de confianza asociados a cada empleado:

### Ver los dispositivos registrados

1. Acceda al perfil del empleado en el backoffice.
2. Acceda a la sección **Seguridad y dispositivos**.
3. Se mostrará la lista de dispositivos de confianza registrados, con información sobre el modelo, el sistema operativo y la fecha de último acceso.

### Revocar el acceso a un dispositivo perdido o robado

Si un empleado pierde su dispositivo o este es sustraído, es fundamental revocar su acceso de inmediato para evitar fichajes fraudulentos:

1. Acceda al perfil del empleado en el backoffice.
2. Vaya a la sección **Seguridad y dispositivos**.
3. Localice el dispositivo que desea revocar y pulse **Eliminar**.
4. Confirme la acción.

El dispositivo queda desvinculado de inmediato. Cualquier intento de fichaje desde ese dispositivo será rechazado con el error "Untrusted device".

> **Nota:** Tras revocar un dispositivo, informe al empleado para que registre su nuevo dispositivo siguiendo el proceso descrito anteriormente. Si el empleado aún no dispone de un dispositivo de sustitución, puede ser necesario desactivar temporalmente el requisito de dispositivo de confianza hasta que se resuelva la situación.

---

## Quién puede gestionar estas opciones

La gestión de la verificación biométrica y los dispositivos de confianza desde el backoffice está disponible para los roles **manager** (nivel 3) y **owner** (nivel 4).

---

## Artículos relacionados

- [Autenticación en dos factores](09-autenticacion-dos-factores.md)
- [Crear y gestionar empleados](06-crear-y-gestionar-empleados.md)
- [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md)
- [Empleados multi-entidad](11-empleados-multi-entidad.md)

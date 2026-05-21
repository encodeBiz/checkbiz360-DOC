# Validación del empleado mediante QR

CheckBiz360 ofrece un mecanismo opcional de verificación de identidad previo al fichaje denominado validación del empleado. Cuando está activado en la configuración de la sucursal, utiliza un código QR generado en la app del empleado que el supervisor escanea para confirmar que la persona presente es quien dice ser. Este artículo explica cómo funciona este mecanismo, cuándo se aplica y qué representa desde el punto de vista técnico.

> **Nota:** La validación QR es un mecanismo configurable por sucursal, no un requisito universal del sistema. Independientemente de si la validación QR está activada o no, el proceso de fichaje siempre valida de forma automática el dispositivo de confianza, la geolocalización dentro de la geocerca y el horario de turno activo del empleado.

---

## Qué es la validación del empleado

La validación del empleado es un mecanismo de verificación presencial de identidad que puede activarse como paso previo al primer fichaje de la jornada. Su propósito es añadir una capa adicional de seguridad frente al registro delegado o fraudulento, especialmente en entornos donde la identidad del empleado debe confirmarse presencialmente.

Este mecanismo es completamente configurable por sucursal: no todas las sucursales ni entidades lo requieren. Cuando está habilitado, el empleado no puede completar el fichaje hasta que el supervisor haya escaneado y validado su código. En sucursales donde no está activado, el empleado puede fichar directamente; el sistema igualmente valida en ese momento el dispositivo de confianza, la geolocalización y el turno activo.

---

## El token de validación

Cuando el empleado inicia sesión en la app y selecciona su entidad de trabajo, el sistema genera un **código de verificación**. Este código es una cadena en formato base64 que contiene el identificador del empleado y el identificador de la entidad.

El código de verificación tiene una vigencia limitada y se utiliza exclusivamente para el proceso de validación QR. No es reutilizable entre sesiones ni transferible entre dispositivos.

---

## El código QR

A partir del código de verificación, la app genera un código QR visible en la pantalla del dispositivo del empleado. Este código contiene la información necesaria para que el sistema identifique al empleado de forma inequívoca.

El supervisor, utilizando su propio dispositivo con la app de CheckBiz360, escanea este código QR. El sistema verifica el código de verificación, confirma la identidad del empleado y marca la validación como completada.

---

## Flujo del proceso cuando la validación QR está activada en la sucursal

1. El empleado abre la app de CheckBiz360 e inicia sesión con sus credenciales.
2. Selecciona la entidad de trabajo correspondiente.
3. La app detecta que la sucursal tiene la validación QR activada y muestra la pantalla de validación con el código QR generado a partir del código de verificación.
4. El supervisor acude al empleado y escanea el QR desde su dispositivo.
5. El sistema verifica el token y registra la validación de identidad.
6. La app del empleado pasa automáticamente a la pantalla de fichaje.
7. El empleado registra su entrada; el sistema valida en ese momento el dispositivo de confianza, la geolocalización y el turno activo.

Cuando la validación QR no está activada en la sucursal, el proceso comienza directamente en el paso 7: el empleado accede a la pantalla de fichaje y el sistema aplica igualmente las validaciones automáticas de dispositivo, geolocalización y horario.

---

## Precalentamiento del sistema de fichaje

Cuando el supervisor escanea el código QR y completa la validación, el sistema ejecuta de forma automática y transparente un proceso de precalentamiento (*warm-up*) del entorno de fichaje. Este proceso prepara y verifica en segundo plano todos los parámetros necesarios para que el fichaje se procese de forma inmediata: turno activo, geocerca, configuración del dispositivo y estado del empleado.

El empleado no percibe este proceso. Desde su perspectiva, simplemente pasa de la pantalla de validación a la pantalla de fichaje. Sin embargo, este mecanismo mejora la velocidad y fiabilidad del registro, especialmente en entornos con muchos empleados fichando en el mismo intervalo de tiempo.

---

## Cuándo es necesaria la validación QR

La validación QR se activa según la configuración de la sucursal. Algunos escenarios habituales en los que se utiliza:

- Entornos con alta rotación de personal o contrataciones temporales donde la identidad del empleado puede no ser conocida por el supervisor.
- Instalaciones con control de acceso estricto donde se requiere verificación dual.
- Sectores con obligaciones normativas de identificación presencial (seguridad, sanidad, alimentación).
- Empresas que desean añadir una capa adicional de control sin necesidad de lectores biométricos físicos.

---

> **Aviso de privacidad:** El código QR contiene únicamente el identificador del empleado y el de la entidad, ambos en formato cifrado. No incluye datos personales en texto plano. El código de verificación expira tras su uso o al finalizar la sesión del empleado.

---

## Roles con acceso a esta funcionalidad

El empleado con rol **empleado** genera el QR desde su app. El escaneo y validación del código corresponde a usuarios con rol **supervisor**, **manager** u **owner**. La activación de la validación QR como requisito previo al fichaje es configurable por roles **manager** u **owner**.

---

## Artículos relacionados

- [Check-in y check-out desde la app](14-checkin-checkout-desde-app.md)
- [Cómo funciona el fichaje](13-como-funciona-el-fichaje.md)
- [Revisión y validación de fichajes](20-revision-y-validacion-de-fichajes.md)
- [Estados y códigos de error](22-estados-y-codigos-de-error.md)

# Conservación y protección de datos

## CheckBiz360 y los datos personales de los empleados

CheckBiz360 trata datos personales de los empleados de la empresa para prestar su servicio. Esto significa que, desde la perspectiva del Reglamento General de Protección de Datos (RGPD) y de la Ley Orgánica 3/2018 de Protección de Datos Personales y garantía de los derechos digitales (LOPDGDD), existen obligaciones concretas que tanto la empresa como la plataforma deben cumplir.

Esta guía explica qué datos trata CheckBiz360, con qué base legal, durante cuánto tiempo se conservan y cuáles son los derechos de los empleados sobre sus datos.

---

## Qué datos personales trata CheckBiz360

La plataforma trata las siguientes categorías de datos de cada empleado:

- **Datos identificativos:** nombre completo, dirección de email, número de teléfono (si se usa para autenticación).
- **Datos de asistencia:** registros de entrada y salida con timestamp, estado de cada jornada, correcciones realizadas sobre los registros.
- **Datos de geolocalización:** coordenadas GPS en el momento del fichaje, utilizadas para la validación de la geocerca configurada por la empresa.
- **Datos de actividad en la app:** tareas asignadas y completadas, valoraciones recibidas, notificaciones enviadas y leídas.
- **Datos de dispositivo:** identificador del dispositivo móvil desde el que se realizan los fichajes, utilizado para la detección de dispositivos no autorizados.

---

## Base legal del tratamiento

El tratamiento de datos personales realizado a través de CheckBiz360 tiene dos bases legales principales:

### Ejecución del contrato de trabajo

El registro de asistencia y el control horario son inherentes a la relación laboral. El empleador tiene el deber de controlar la jornada de trabajo y el trabajador tiene la obligación de cumplir su horario. El tratamiento de datos de asistencia está directamente vinculado a la ejecución del contrato de trabajo (artículo 6.1.b del RGPD).

### Cumplimiento de una obligación legal

El RDL 8/2019 impone a la empresa la obligación de registrar la jornada diaria de cada empleado. El tratamiento de los datos necesarios para cumplir esa obligación tiene como base legal el artículo 6.1.c del RGPD (cumplimiento de una obligación legal aplicable al responsable del tratamiento).

> **Nota:** La empresa no necesita obtener el consentimiento del empleado para tratar sus datos de asistencia. El consentimiento no es la base legal aplicable en este caso: el tratamiento se fundamenta en la ejecución del contrato y en la obligación legal. Solicitar consentimiento cuando existe otra base legal adecuada puede generar confusión y no mejora la posición jurídica de la empresa.

---

## Tiempo de conservación de los datos

Los diferentes tipos de datos tienen periodos de conservación distintos:

| Tipo de dato | Periodo de conservación | Base legal |
|---|---|---|
| Registros de asistencia y jornada | Mínimo 4 años | RDL 8/2019 — obligación legal |
| Datos de geolocalización | Solo durante la validación del fichaje; no se almacenan indefinidamente | Principio de minimización de datos (RGPD art. 5.1.e) |
| Datos identificativos del empleado | Mientras dure la relación laboral + 4 años | Obligaciones laborales y mercantiles |
| Datos de tareas y valoraciones | Mientras dure la relación laboral; configurable por la entidad | Ejecución del contrato |

> **Aviso:** Los datos de geolocalización de CheckBiz360 no son un sistema de rastreo continuo. Las coordenadas GPS se registran en el momento puntual del fichaje para verificar que el empleado está dentro del perímetro de geocerca configurado. No se realiza un seguimiento de la posición del empleado a lo largo de la jornada.

---

## Derechos de los empleados sobre sus datos

El RGPD reconoce a los empleados los siguientes derechos sobre el tratamiento de sus datos personales:

### Derecho de acceso
El empleado puede solicitar qué datos suyos trata la empresa y obtener una copia. En CheckBiz360, el empleado puede acceder directamente a sus propios datos de asistencia desde la app sin necesidad de solicitarlo formalmente.

### Derecho de rectificación
Si un dato es inexacto, el empleado puede solicitar su corrección. En el caso de registros de asistencia, la corrección debe realizarla un responsable con acceso al backoffice, con trazabilidad completa de la modificación.

### Derecho de supresión
El empleado puede solicitar la eliminación de sus datos. Sin embargo, este derecho **tiene limitaciones cuando existe una obligación legal de conservación**: la empresa no puede eliminar los registros de asistencia antes de que transcurran los cuatro años exigidos por el RDL 8/2019, aunque el empleado lo solicite. Una vez finalizado el periodo de conservación obligatorio, los datos deben eliminarse salvo que exista otra base legal para mantenerlos.

### Derecho de oposición y limitación
El empleado puede oponerse al tratamiento o solicitar su limitación en ciertos casos. Al igual que con la supresión, estos derechos tienen limitaciones cuando el tratamiento se basa en una obligación legal.

---

## Cómo la empresa debe informar a sus empleados

Antes de implantar CheckBiz360, la empresa tiene la obligación de informar a sus empleados sobre el tratamiento de sus datos personales. Esta información debe facilitarse de forma proactiva, clara y en lenguaje comprensible, e incluir:

1. La identidad del responsable del tratamiento (la propia empresa).
2. La finalidad del tratamiento: registro de jornada, control de asistencia y cumplimiento del RDL 8/2019.
3. La base legal: ejecución del contrato y cumplimiento de obligación legal.
4. Los tipos de datos que se tratarán, incluyendo la geolocalización puntual en el momento del fichaje.
5. El periodo de conservación de los datos.
6. Los derechos del empleado y cómo ejercerlos.
7. La identidad del encargado del tratamiento: CheckBiz360 actúa como encargado del tratamiento en nombre de la empresa.

Esta información puede incorporarse en el contrato de trabajo, en una cláusula informativa específica, en el documento de bienvenida a la empresa o en una comunicación interna firmada por el empleado.

> **Aviso:** La empresa es el responsable del tratamiento. CheckBiz360 actúa como encargado, procesando los datos en nombre de la empresa según las instrucciones de esta y conforme al contrato de encargo de tratamiento que ambas partes suscriben al contratar el servicio. Si la Agencia Española de Protección de Datos (AEPD) inicia una investigación relacionada con estos datos, se dirigirá a la empresa como responsable.

---

> **Nota:** Este artículo tiene carácter informativo y no constituye asesoramiento jurídico. Para adaptar la información a la situación específica de su empresa, consulte con su delegado de protección de datos (DPO) o con su asesoría jurídica especializada en protección de datos.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Registro horario obligatorio en España](./81-registro-horario-obligatorio-en-espana.md) | Qué exige el RDL 8/2019 y sus obligaciones |
| [Cómo CheckBiz360 cumple el RDL 8/2019](./82-como-checkbiz360-cumple-el-rdl-8-2019.md) | Mecanismos técnicos de cumplimiento |
| [Exportar a Excel y CSV](../11-informes-y-exportacion/78-exportar-a-excel-y-csv.md) | Consideraciones RGPD al exportar datos de empleados |
| [Preparar una inspección de trabajo](./84-preparar-una-inspeccion-de-trabajo.md) | Qué documentos solicita la Inspección de Trabajo |

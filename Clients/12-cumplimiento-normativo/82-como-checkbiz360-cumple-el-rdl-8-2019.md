# Cómo CheckBiz360 cumple el RDL 8/2019

## Por qué la tecnología importa en el cumplimiento normativo

El RDL 8/2019 no exige un sistema tecnológico concreto, pero sí establece requisitos que en la práctica solo pueden garantizarse con herramientas digitales: registro diario con timestamp preciso, conservación durante cuatro años, acceso del trabajador a sus propios datos y trazabilidad completa de cualquier corrección.

Un registro en papel puede perderse, modificarse sin dejar rastro o no estar disponible cuando lo solicite un inspector. Una hoja de cálculo puede editarse retroactivamente sin que nadie lo detecte. CheckBiz360 está diseñado para que ninguna de esas situaciones sea posible.

Esta guía explica los mecanismos técnicos concretos con los que la plataforma garantiza el cumplimiento.

---

## Registro automático de timestamp

Cada vez que un empleado ficha entrada o salida desde la app de CheckBiz360, el sistema registra un **timestamp inmediato con precisión de segundos** en los servidores de la plataforma. Este registro no requiere ninguna acción adicional del manager ni del empleado más allá del fichaje.

El timestamp registrado incluye:

- Fecha y hora exacta del evento.
- Identificación del empleado.
- Tipo de evento (entrada, salida, pausa, reanudación).
- Identificación del dispositivo desde el que se realizó el fichaje.
- Coordenadas GPS en el momento del fichaje, si la geocerca está configurada.

Este registro se produce en el momento del fichaje y no puede modificarse una vez creado.

---

## Almacenamiento inmutable del historial

CheckBiz360 garantiza la **inmutabilidad del historial de registros**. Esto significa que:

- Ningún usuario de la plataforma, independientemente de su rol, puede eliminar un registro de fichaje del historial.
- Ningún usuario puede modificar los datos originales de un registro (hora, fecha, tipo de evento) sin que esa modificación quede registrada como una corrección manual separada.
- El historial original se conserva siempre, incluso cuando se realizan correcciones.

Este diseño es fundamental para el cumplimiento normativo: si un inspector solicita los registros de un periodo, la empresa puede demostrar no solo qué fichajes se produjeron, sino también si alguno fue corregido y por qué razón.

---

## Trazabilidad completa de las correcciones manuales

En la operativa diaria, es habitual que los managers necesiten corregir registros erróneos: un empleado olvidó fichar salida, se produjo un error técnico puntual o un registro de una jornada especial requiere ajuste.

CheckBiz360 permite realizar estas correcciones, pero con una condición: **toda corrección manual queda registrada con plena trazabilidad**. Para cada corrección, el sistema almacena:

- El valor original del registro antes de la corrección.
- El nuevo valor introducido por el responsable.
- La identidad del usuario que realizó la corrección (nombre y rol).
- La fecha y hora en que se realizó la corrección.
- El motivo de la corrección, que el responsable debe introducir obligatoriamente.

Esta trazabilidad satisface el requisito de integridad del registro que exige la normativa y que la Inspección de Trabajo verifica en sus actuaciones.

---

## Acceso del empleado a su propio historial

El RDL 8/2019 establece el derecho del trabajador a consultar sus propios registros. En CheckBiz360, este derecho se satisface de forma directa: **cada empleado puede consultar su historial completo de fichajes desde la app móvil**, sin necesidad de solicitarlo a ningún responsable.

El empleado ve en su app:

- Todos sus fichajes de entrada y salida, con timestamp exacto.
- El estado de validación de cada registro.
- Las correcciones que se hayan realizado sobre sus registros, con fecha de la corrección.

Este acceso es permanente y en tiempo real. No requiere que el manager exporte ningún archivo ni realice ninguna gestión.

---

## Por qué el registro en papel y las hojas de cálculo no ofrecen las mismas garantías

La Inspección de Trabajo ha cuestionado en múltiples actuaciones la validez de sistemas de registro basados en papel o en hojas de cálculo editables. Las razones son técnicas y jurídicas:

| Aspecto | Registro en papel | Hoja de cálculo | CheckBiz360 |
|---|---|---|---|
| Inmutabilidad | No garantizada | No garantizada | Garantizada por diseño |
| Trazabilidad de correcciones | Imposible | Imposible sin auditoría activa | Automática e íntegra |
| Acceso del trabajador | Depende de proceso manual | Depende de proceso manual | Acceso directo desde la app |
| Conservación cuatro años | Riesgo de pérdida o deterioro | Riesgo de pérdida o borrado | Conservación en servidores gestionados |
| Timestamp preciso | Requiere disciplina manual | Requiere disciplina manual | Automático en el momento del fichaje |

Cuando la ITSS detecta que una empresa usa hojas de cálculo editables como único sistema de registro, puede considerar que no existe un sistema de registro fiable y levantar acta de infracción aunque los datos parezcan completos.

---

## Periodo de conservación garantizado

CheckBiz360 conserva todos los registros de jornada durante el periodo mínimo exigido por el RDL 8/2019 (**cuatro años**). La empresa no necesita realizar ninguna gestión para cumplir este requisito mientras mantenga su cuenta activa.

> **Aviso:** Si la empresa decide cancelar su cuenta en CheckBiz360, debe exportar todos los registros históricos antes del cierre. La obligación de conservación durante cuatro años recae sobre la empresa, no sobre el proveedor. CheckBiz360 no puede ser considerado responsable de la pérdida de registros históricos si la empresa no exporta sus datos antes de cerrar la cuenta.

---

> **Nota:** Este artículo describe los mecanismos técnicos de la plataforma en relación con el cumplimiento normativo. Para un asesoramiento jurídico específico sobre la situación de su empresa, consulte con su asesoría laboral.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Registro horario obligatorio en España](./81-registro-horario-obligatorio-en-espana.md) | Qué exige el RDL 8/2019 y a quién aplica |
| [Informe de cumplimiento normativo](../11-informes-y-exportacion/79-informe-de-cumplimiento-normativo.md) | Cómo generar el informe para la Inspección de Trabajo |
| [Conservación y protección de datos](./83-conservacion-y-proteccion-de-datos.md) | Bases legales del tratamiento de datos de empleados |
| [Preparar una inspección de trabajo](./84-preparar-una-inspeccion-de-trabajo.md) | Guía práctica ante una visita de la ITSS |
| [Detección de anomalías](../07-inteligencia-operativa/55-deteccion-de-anomalias.md) | Cómo el sistema detecta patrones irregulares de fichaje |

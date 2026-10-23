# Seguimiento y resolución de incidencias

Una vez creada, la incidencia vive en **Contacto**, pestaña **Incidencias**, del backoffice hasta que se resuelve. Este artículo describe sus estados, cómo se responde y qué queda registrado.

Recuerde que las incidencias son un canal **interno de su organización**. Para problemas de la plataforma, el canal es el soporte de EncodeBiz: consulte [Contactar con soporte técnico](./87-contactar-con-soporte-tecnico.md).

---

## Estados de una incidencia

| Estado | Significado |
|---|---|
| **Pendiente** | Registrada, a la espera de que alguien la tome |
| **En revisión** | Alguien está investigando el problema. Es el estado con el que nace una incidencia creada desde el backoffice |
| **Resuelto** | El problema se ha solucionado. La incidencia deja de admitir respuestas |

No hay un estado "cerrada" ni un cierre automático por tiempo: una incidencia permanece abierta hasta que alguien la marca como resuelta.

### Quién puede cambiar el estado

El estado se cambia de dos formas: editando la incidencia, o **al responder** en su hilo, donde cada respuesta puede llevar asociado un cambio de estado. Ambas acciones corresponden a los roles con acceso al backoffice: **Owner** y **Manager**.

---

## Responder a una incidencia

El seguimiento se hace mediante respuestas. Cada respuesta queda en el hilo, con su autor y su fecha, y puede además mover el estado.

1. Acceda a **Contacto** en el menú lateral y quédese en la pestaña **Incidencias**.
2. Localice la incidencia con los filtros de estado, sucursal o empleado.
3. Abra su detalle.
4. Pulse **Responder**.
5. Escriba el mensaje y, si procede, seleccione el nuevo **estado**.
6. Confirme.

> **Importante:** una incidencia en estado *Resuelto* ya no admite respuestas. Si el problema reaparece, cree una incidencia nueva y haga referencia en el comentario a la anterior.

> **Aviso:** no abra una incidencia nueva para añadir información a un caso que sigue abierto. Use el hilo de respuestas para mantener el contexto agrupado.

---

## Historial del caso

El detalle de la incidencia muestra el planteamiento inicial y, debajo, todas las respuestas en orden cronológico, cada una con su autor, la fecha y el cambio de estado que produjo. El listado indica también cuántas respuestas acumula cada incidencia, lo que permite localizar de un vistazo las que llevan más idas y venidas.

---

## Cuándo marcar una incidencia como resuelta

Márquela como resuelta cuando haya comprobado que el problema ha desaparecido y la operativa ha vuelto a la normalidad. Conviene dejar una última respuesta explicando **qué lo causaba y qué se hizo**: es lo que convierte el histórico de incidencias en algo consultable cuando el mismo síntoma reaparezca meses después.

Si un mismo síntoma genera incidencias repetidas, es señal de una causa de fondo —una geocerca mal dimensionada, un calendario que no cubre un turno— que conviene atacar en la configuración en lugar de resolver caso por caso.

---

## Exportar el historial de incidencias

> **Estado: No disponible**
> La exportación del listado de incidencias a CSV o PDF no está implementada en la versión actual y no tiene fecha planificada.

Las incidencias se consultan y filtran en pantalla. Si necesita el histórico para una auditoría, solicítelo a soporte en hola@encodebiz.com.

---

## Nota de rol

Este artículo está dirigido a **Owner** y **Manager**, los únicos roles con acceso al módulo de incidencias en el backoffice.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear una incidencia](./85-crear-una-incidencia.md) | Campos, tipos y creación de una incidencia |
| [Contactar con soporte técnico](./87-contactar-con-soporte-tecnico.md) | Canal con el equipo de EncodeBiz |
| [Problemas frecuentes y soluciones](./88-problemas-frecuentes-y-soluciones.md) | Diagnóstico de las situaciones más habituales |
| [Códigos de error completos](../14-referencia/90-codigos-de-error-completos.md) | Causa y solución de cada código |

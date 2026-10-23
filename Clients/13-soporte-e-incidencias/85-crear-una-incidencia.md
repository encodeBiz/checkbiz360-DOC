# Crear una incidencia

El módulo de incidencias de CheckBiz360 es el canal formal de comunicación **dentro de su organización** entre quien detecta un problema operativo y quien puede resolverlo.

Es importante no confundirlo con el soporte técnico de CheckBiz360: una incidencia es un reporte interno —"no pude fichar al entrar", "el descanso quedó mal registrado", "la geocerca de esta sucursal está mal configurada"— dirigido a un responsable de la propia empresa. Para problemas de la plataforma en sí, el canal es el soporte de EncodeBiz, descrito en [Contactar con soporte técnico](./87-contactar-con-soporte-tecnico.md).

---

## Para qué sirve

El módulo resuelve un problema concreto: que las incidencias operativas dejen de resolverse por WhatsApp o de palabra y pasen a quedar registradas, con su historial, junto a los datos de fichaje a los que se refieren.

Cada incidencia recoge quién la reporta, sobre qué sucursal, de qué tipo es, y mantiene un hilo de respuestas hasta que se marca como resuelta.

---

## Campos de una incidencia

| Campo | Descripción |
|---|---|
| **Empleado** | La persona a la que se refiere la incidencia |
| **Sucursal** | El centro de trabajo donde se ha producido |
| **Rol origen** | Desde qué nivel se reporta: trabajador o supervisor |
| **Rol destino** | A qué nivel se dirige: trabajador o supervisor |
| **Tipo** | Registro de jornada, registro de descanso, configuración u otro |
| **Estado** | Pendiente, en revisión o resuelto |
| **Comentario** | La descripción del problema |
| **Incluir ubicación** | Adjunta las coordenadas desde las que se reporta, útil cuando el problema tiene que ver con la geocerca |

### Los cuatro tipos de incidencia

- **Registro de jornada** — problemas con el checkin o el checkout: no se registró, se registró a destiempo, quedó una jornada sin cerrar.
- **Registro de descanso** — problemas con el inicio o el fin de una pausa.
- **Configuración** — algo mal configurado que impide trabajar con normalidad: geocerca demasiado estrecha, horario que no corresponde, calendario sin resolver.
- **Otro** — cualquier situación que no encaje en las anteriores.

---

## Cómo crear una incidencia desde el backoffice

1. Acceda a **Contacto** en el menú lateral (antes se llamaba *Incidencias*) y quédese en la pestaña **Incidencias**.
2. Pulse el botón de crear incidencia.
3. Seleccione el **empleado** y la **sucursal** a los que se refiere.
4. Indique el **rol origen** y el **rol destino**.
5. Elija el **tipo** que mejor describe el problema.
6. Escriba el **comentario** con el detalle: qué ocurrió, cuándo y con qué frecuencia se repite. Cuanto más concreto, menos idas y venidas en el hilo.
7. Active **incluir ubicación** si el problema guarda relación con dónde se encuentra el empleado.
8. Guarde. La incidencia nace **en revisión**.

> **Consejo:** al describir un problema de fichaje, incluya la fecha y la hora exactas y, si apareció un código de error en pantalla, cópielo literalmente. Con el código, el diagnóstico es inmediato: consulte [Códigos de error completos](../14-referencia/90-codigos-de-error-completos.md).

---

## Qué ocurre después

La incidencia queda listada en **Contacto**, pestaña **Incidencias**, filtrable por estado, sucursal y empleado. El responsable la revisa y **responde** desde su detalle; cada respuesta puede además cambiar el estado. El intercambio queda como un hilo consultable.

Mientras la incidencia no esté resuelta, sigue admitiendo respuestas. Consulte [Seguimiento y resolución de incidencias](./86-seguimiento-y-resolucion-de-incidencias.md).

La otra pestaña de **Contacto**, **Solicitudes**, recoge las vacaciones y los permisos que las personas piden desde la app. Solo la ven el propietario y los administradores. Consulte [Vacaciones y permisos desde la app](../04-calendario-y-horarios/115-vacaciones-y-permisos-desde-la-app.md).

---

## Nota de rol

La gestión de incidencias desde el backoffice corresponde a **Owner** y **Manager**. Los roles de origen y destino de cada incidencia —trabajador y supervisor— identifican a las partes implicadas en el problema operativo, no a quién administra el módulo.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Seguimiento y resolución de incidencias](./86-seguimiento-y-resolucion-de-incidencias.md) | Estados, respuestas e historial de una incidencia |
| [Contactar con soporte técnico](./87-contactar-con-soporte-tecnico.md) | Canal con el equipo de EncodeBiz para problemas de la plataforma |
| [Problemas frecuentes y soluciones](./88-problemas-frecuentes-y-soluciones.md) | Diagnóstico de las situaciones más habituales |
| [Códigos de error completos](../14-referencia/90-codigos-de-error-completos.md) | Causa y solución de cada código |
| [Solicitar una jornada manual](../03-control-horario/19-solicitar-jornada-manual.md) | La vía para corregir un fichaje que no se registró |

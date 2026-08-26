# RentmanBiz — la integración con Rentman

**RentmanBiz** es el add-on que conecta CheckBiz360 con Rentman, el software con el que muchas empresas de eventos, audiovisuales y alquiler de material planifican sus proyectos, su equipo y su almacén.

## Qué le falta a Rentman (y por qué esto le importa)

Rentman sabe **lo que está planificado**: qué montaje hay, qué material sale, quién debería ir y durante cuántas horas. Lo que no sabe es **lo que ha ocurrido de verdad**: si esa persona llegó, a qué hora, si estaba en el pabellón o en su casa, y cuántas horas trabajó realmente.

Ese hueco se rellena hoy a mano. Alguien pregunta, alguien apunta, alguien teclea las horas al final de la semana. Y cuando el cliente final discute una factura o un trabajador discute su nómina, lo único que hay es la palabra de cada uno.

RentmanBiz cierra ese hueco en los dos sentidos: trae de Rentman **quién trabaja y dónde**, y le devuelve **las horas que se han fichado de verdad**.

## Lo que aporta, en concreto

### Las horas dejan de teclearse

Cuando un trabajador cierra su jornada en CheckBiz360, esas horas aparecen solas en el proyecto de Rentman que corresponde, en el siguiente cuarto de hora. Sin hojas de cálculo intermedias, sin recordatorios y sin que nadie transcriba nada.

### Horas verificables, no declaradas

Esta es la diferencia de fondo. No es lo mismo *"el técnico dice que estuvo diez horas"* que *"consta que entró a las 08:02 dentro del recinto del evento, desde su dispositivo autorizado, y salió a las 18:10 desde el mismo sitio"*.

Con eso cambian dos conversaciones: la que se tiene con el cliente final cuando pregunta por una factura, y la que se tiene con un trabajador cuando revisa su nómina.

### El registro horario legal, que Rentman no cubre

Rentman es una herramienta de producción, no un sistema de registro horario. La normativa exige un registro diario de jornada, conservado, accesible y no manipulable. CheckBiz360 lo aporta —con sus informes exportables— sin cambiar la forma de trabajar de nadie: la planificación sigue viviendo en Rentman.

### El evento se convierte en un sitio donde fichar

Cada montaje con gente asignada se convierte en un centro de trabajo con su **geocerca**, tomada de la dirección del venue. En este sector nadie ficha en la oficina: se ficha en el pabellón, en el teatro o en la nave donde se monta. Y nadie tiene que ir creando centros a mano cada semana.

Los **almacenes** entran igual, como centros permanentes: es donde la gente ficha a diario.

### Cada uno sabe qué le toca al llegar

Las asignaciones de Rentman se convierten en tareas dentro de CheckBiz360. El trabajador abre el móvil y ve a qué montaje va, con qué función y en qué horario, y va marcando lo que completa. Deja de llegar preguntando.

### Quién preparó cada pedido, y cuánto tardó

Este es, probablemente, el aporte que más cambia el día a día de una empresa de alquiler.

Un alquiler en seco o una venta no llevan a nadie a un evento, pero alguien tiene que preparar ese material antes de que el cliente lo recoja, y alguien tiene que revisarlo cuando vuelve. Hoy eso se organiza de palabra —"ya lo preparo yo esta tarde"— y no queda registrado en ninguna parte.

Con RentmanBiz, cada operación genera su tarea en el almacén correspondiente, con la fecha de salida del material. A partir de ahí:

- **Se sabe quién tiene que ir a hacerlo**: el responsable reparte esas tareas entre su gente del almacén, y cada uno lo ve en su móvil.
- **Se sabe quién lo hizo**, porque la tarea queda a su nombre y se marca como completada.
- **Y se sabe cuánto tardó**, porque esa persona está fichando en ese almacén mientras lo prepara.

Eso abre preguntas que hasta ahora no se podían ni formular: cuánto cuesta realmente preparar un pedido tipo, si dos personas tardan lo mismo en lo mismo, si los picos de trabajo del almacén coinciden con los que se planificaron, o cuánta gente hace falta el viernes de un fin de semana cargado.

Va **desactivado de fábrica**, porque no todas las empresas quieren gestionar el almacén con tareas y una empresa de alquiler tiene decenas de estas operaciones por semana.

### Cuánto costó de verdad un montaje

Las horas que se imputan son las **netas**, con el descanso ya descontado, y llevan asociado el coste por hora de cada función que ustedes ya tienen definido en Rentman. La diferencia entre lo planificado y lo real deja de ser una intuición.

### Y nadie toca el registro sin que se sepa

Si alguien modifica en Rentman unas horas ya imputadas, **el fichaje de CheckBiz360 no se cambia**. La diferencia se detecta, se marca y se le muestra con las dos versiones delante para que usted decida. El registro legal no se sobrescribe en silencio.

## Qué NO hace

Tan importante como lo anterior:

- **No modifica sus fichajes** a partir de datos de Rentman.
- **No envía jornadas abiertas ni incompletas**: sin salida registrada no hay nada que enviar.
- **No crea personal ni asignaciones en Rentman.** Su API no lo permite: las personas y las asignaciones viajan de Rentman hacia CheckBiz360, nunca al revés.
- **No sincroniza material, presupuestos ni facturas.**
- **No envía sus tareas a Rentman.** Está previsto para más adelante.

## Estado actual de la funcionalidad

| Funcionalidad | Estado | Comentario |
|---|---|---|
| Envío de jornadas cerradas a Rentman | **Disponible** | Automático cada 15 minutos, o al momento |
| Horas netas con descanso y coste por hora | **Disponible** | Misma cifra que el informe legal |
| Aviso de horas modificadas en Rentman | **Disponible** | Con las dos versiones comparadas |
| Importación de la plantilla | **Disponible** | Empareja por correo; quien no lo tenga queda pendiente |
| Montajes y almacenes como centros de trabajo | **Disponible** | Nacen inactivos hasta confirmar la geocerca |
| Asignaciones convertidas en tareas | **Disponible** | Una tarea por función, con su gente |
| Tareas de almacén (alquileres y ventas) | **Disponible** | Desactivado de fábrica |
| Pantalla de configuración en el backoffice | **En desarrollo** | Durante la beta lo configura el equipo de Encodebiz |
| Enviar tareas de CheckBiz360 a Rentman | **Pendiente de desarrollo** | Prevista en una versión futura |
| Material, presupuestos y facturas | **No disponible** | Fuera del alcance |

## Qué necesita para empezar

Una cuenta de Rentman con permiso para crear un token de API, el control horario de CheckBiz360 activo, y un rato para revisar lo que la primera importación deje pendiente — normalmente correos que faltan y geocercas por confirmar.

## Artículos relacionados

- [Conectar RentmanBiz paso a paso](95-conectar-rentman.md)
- [Qué se importa y qué queda pendiente](97-importacion-y-pendientes.md)
- [Horas imputadas y avisos](96-horas-imputadas-y-avisos.md)

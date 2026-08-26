# Qué se importa y qué queda pendiente

Al conectar RentmanBiz, la plataforma trae de Rentman lo necesario para que su equipo pueda fichar. Este artículo explica qué entra, qué se queda fuera a propósito y por qué algunas cosas nacen **pendientes de completar**.

## Antes de importar: la vista previa

La importación nunca empieza a ciegas. Primero se genera una **vista previa** que no escribe nada y responde a la pregunta razonable: *¿qué me va a meter esto en mi plataforma?*

Verá cuántos montajes se convertirían en centros de trabajo, cuántos se descartan, cuántas personas se pueden crear y cuántas no, y cuántas tareas saldrían. Solo cuando el resultado le parezca correcto se ejecuta de verdad.

## Qué se importa

### Las personas

Cada persona de su plantilla en Rentman se busca primero entre sus empleados de CheckBiz360 **por correo electrónico**. Si ya existe, se enlaza — nunca se duplica, porque partir el historial de alguien en dos es peor que no importarlo.

Si no existe y trae correo, se crea con su acceso y recibe su correo de bienvenida.

### Los centros de trabajo

Entran dos tipos:

- **Los montajes**: cada proyecto de Rentman **que tenga gente asignada**. Ese es el criterio, no el tipo de proyecto: si nadie está asignado, nadie va a fichar allí.
- **Los almacenes**: sus ubicaciones de material, que son centros permanentes donde se ficha a diario.

De ambos se toma la dirección y se calculan sus coordenadas para proponer la geocerca.

### Las responsabilidades

Cada persona queda vinculada a los centros donde trabaja: al almacén que tiene asignado en su ficha de Rentman, y a los montajes en los que esté asignada. Con su función como puesto — técnico, rigger, stagehand— y con el coste por hora que usted ya tiene definido allí.

**Todos entran como trabajador.** La función de Rentman es un oficio, no un nivel de permisos: que alguien monte luces en un evento no le convierte en responsable de un centro. Si quiere subir a alguien, se hace a mano y de forma consciente.

### Las tareas

Una tarea por función de cada montaje, con todas las personas de esa función dentro. Y, si lo activa, las tareas de almacén de alquileres y ventas: preparar el material antes de la salida y revisarlo a la vuelta.

## Qué se descarta, y por qué

| Se descarta | Motivo |
|---|---|
| Proyectos sin gente asignada | Ventas y alquileres en seco: nadie pisa un sitio, no hay dónde fichar |
| Proyectos fuera de ventana | Solo se traen los del último mes y los tres próximos, para no arrastrar el histórico |
| Material, presupuestos, facturas | Fuera del alcance de la integración |

## Lo que queda pendiente de completar

Rentman no guarda todo lo que CheckBiz360 necesita. En vez de inventarlo o de descartar el dato, la plataforma lo importa marcado como **pendiente**, con el motivo, y le enseña un aviso con enlace directo a la ficha donde se arregla.

| Pendiente | Qué significa | Qué hacer |
|---|---|---|
| **Sin correo** | Rentman rara vez lo guarda, y en CheckBiz360 es el acceso del empleado | Añadir el correo en su ficha. Al hacerlo recibe su acceso y su bienvenida |
| **Falta confirmar la geocerca** | Rentman no da coordenadas: se han calculado desde la dirección | Revisar el punto en el centro y activarlo |
| **Sin dirección** | Ese montaje no trae dirección en Rentman | Completarla o dejar el centro sin usar |
| **Sin coste por hora** | Esa función no tiene tarifa definida en Rentman | Ponerla, o sus jornadas saldrán a coste cero en los informes |

Dos cosas importantes sobre lo pendiente:

**Nada pendiente puede hacer daño mientras lo esté.** Un centro sin geocerca confirmada nace **inactivo**: existe, pero no valida ni invalida el fichaje de nadie. Una persona sin correo nace **inactiva y sin acceso**.

**Y nada pendiente se le factura.** Como la facturación va por empleado activo, alguien que todavía no puede trabajar no cuenta. Empieza a contar cuando usted completa su correo y pasa a activo, que es cuando puede fichar de verdad.

El aviso desaparece solo cuando no queda nada por completar.

## Volver a importar

La importación se puede repetir sin miedo: lo que ya existe no se duplica, y lo que usted haya configurado a mano —geocercas, horarios, descansos— **no se sobrescribe nunca**. Solo se añade lo nuevo que haya aparecido en Rentman.

## Artículos relacionados

- [RentmanBiz](94-integracion-rentman.md)
- [Conectar RentmanBiz paso a paso](95-conectar-rentman.md)

# Horas imputadas y avisos

Una vez conectada la integración, la pantalla de Rentman le muestra qué está ocurriendo con sus horas. Este artículo explica qué significa cada cifra y qué hacer cuando algo requiere su atención.

## Qué verá

| Indicador | Qué le dice |
|---|---|
| **Jornadas imputadas** | Cuántas jornadas cerradas se han enviado a Rentman |
| **Horas imputadas** | El total de horas netas enviadas en el periodo |
| **Cobertura de emparejamiento** | Cuántos de sus empleados tienen ficha de Rentman asociada |
| **Divergencias abiertas** | Jornadas que alguien ha modificado en Rentman después de enviarlas |

## Sincronizar al momento

La sincronización se ejecuta sola cada 15 minutos, pero justo después de conectar —o cuando quiera comprobar algo— puede pulsar **Sincronizar ahora** y no esperar. Si lo pulsa dos veces seguidas, la plataforma le dirá que espere unos segundos: es una protección para no saturar Rentman, no un error.

Y si el resultado sale en cero, tampoco es un fallo: puede que no haya jornadas cerradas nuevas o que falte emparejar a esa gente.

## Por qué las horas coinciden con su informe legal

Las horas que se envían a Rentman son las **netas**: la diferencia entre la entrada y la salida, menos el descanso.

El descanso no viaja dentro del fichaje. Sale de la configuración de la sucursal: o bien es un descanso fijo definido en el centro de trabajo, o bien se calcula sumando las pausas que el trabajador registró. La integración aplica **exactamente la misma regla que el informe de control horario**, de forma que la cifra que ve en Rentman y la que usted certifica ante una inspección son la misma.

Si alguna vez ambas cifras no coinciden, avísenos: es un problema que queremos conocer.

## Las divergencias

Una divergencia aparece cuando alguien **edita en Rentman** unas horas que CheckBiz360 ya había enviado, o cuando las borra.

En ese caso la plataforma:

1. Detecta el cambio al revisar el registro, cosa que hace cada 24 horas.
2. Marca esa jornada como divergente y le muestra las dos versiones: la suya y la de Rentman.
3. **No modifica su fichaje.** El registro legal permanece intacto.
4. Tampoco deshace el cambio hecho en Rentman: la decisión es suya.

Qué hacer ante una divergencia depende de quién tenga razón:

- **Si el fichaje es correcto** y la edición en Rentman fue un error, corríjalo en Rentman.
- **Si el fichaje es el que está mal** (por ejemplo, un trabajador olvidó fichar la salida y se cerró de forma incorrecta), corríjalo primero en CheckBiz360. Al hacerlo, la jornada se volverá a enviar con los valores nuevos.

## Estados de una jornada

| Estado | Qué significa | Requiere acción |
|---|---|---|
| En cola | Detectada, pendiente de enviar | No |
| Enviada | Ya está en Rentman | No |
| Con error | Un fallo temporal de conexión | No, se reintenta solo |
| Rechazada | Rentman no la acepta | Sí, revise el motivo |
| Divergente | Modificada en Rentman | Sí, revise las dos versiones |

## Preguntas frecuentes

**Un trabajador ha fichado pero sus horas no aparecen en Rentman.**
Compruebe tres cosas por este orden: que la jornada esté **cerrada** (con su salida registrada), que el trabajador esté **emparejado** con su ficha de Rentman, y que hayan pasado al menos 15 minutos desde el cierre.

**Aparece una jornada "rechazada" por Rentman.**
El motivo más habitual es que en Rentman ya existían horas o una ausencia para esa persona en ese mismo periodo. Rentman no admite dos registros solapados. Revise en Rentman qué hay en esas fechas: normalmente se trata de horas introducidas a mano antes de conectar la integración.

**¿Se envían las jornadas incompletas?**
No. Una jornada sin salida registrada no es una jornada cerrada, y no se envía. Si es algo frecuente en su empresa, conviene revisar los avisos de cierre automático en el módulo de control horario.

**¿Puedo editar en Rentman las horas que envía CheckBiz360?**
Puede, pero no es recomendable. Su edición no volverá a CheckBiz360 y generará una divergencia. Si la jornada está mal, corríjala en CheckBiz360 y deje que la corrección viaje sola.

**¿Qué ocurre si Rentman está caído?**
Nada grave. Los fichajes siguen funcionando con normalidad —la integración nunca bloquea el control horario— y las jornadas pendientes se envían cuando el servicio vuelve.

**¿Se pueden duplicar las horas?**
No. Cada jornada lleva una huella interna que impide enviarla dos veces, por muchas veces que se ejecute la sincronización.

## Artículos relacionados

- [RentmanBiz](94-integracion-rentman.md)
- [Conectar RentmanBiz paso a paso](95-conectar-rentman.md)

# ADR-004 — Asignar no es consumir: reserva, salida, declaración y sobrante

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El caso que lo dispara: administración asigna **30 toallas** a la tarea «limpieza del Lidl», y
al terminar solo se consumieron **20**. ¿Qué pasa con las otras diez?

Meter eso en un solo movimiento —«se gastaron 30»— arruina el informe de consumo, que es lo que
se está vendiendo. Y dejarlo a que alguien apunte la devolución a mano significa que no se
apunta.

## Decisión

El material de una tarea pasa por **tres momentos distintos**, y la existencia lleva **dos
números** en vez de uno.

### Los tres momentos

1. **Reserva.** Administración promete 30. Las toallas no se mueven de la estantería, pero
   quedan comprometidas: sube `committed`, `onHand` no se toca. Importa porque si mañana otra
   tarea pide 40 y hay 50, el sistema tiene que decir que solo quedan 20 libres.
2. **Salida.** El operario se las lleva. Baja `onHand` y se libera el compromiso. Las toallas
   ya no están en el almacén: están en la furgoneta, imputadas a la tarea.
3. **Declaración.** Al cerrar, el operario dice que gastó 20. El sistema genera solo la
   devolución de 10.

`available = onHand - committed` es el número que mira quien asigna.

### La pregunta correcta

> **No se pregunta cuánto devuelve. Se pregunta cuánto usó.**

Es la misma cuenta, pero «he gastado 20 toallas» es un dato que el operario tiene en la cabeza,
y «devuelvo 10» le obliga a acordarse de con cuántas salió y a restar. El campo llega
precargado con lo que salió: si se gastó todo, es un clic.

### Qué pasa cuando nadie declara

Va a ser la mitad de las veces al principio. Los dos atajos mienten:

- Dar por consumido todo lo que salió **infla el consumo** y arruina el informe.
- Devolver el sobrante solo **llena el almacén** de toallas que siguen en la furgoneta.

Ninguno de los dos. El material que salió y no se declaró queda en un **tercer estado**
(`pending`), imputado a la tarea y visible.

Y se cuadra en **la validación de la tarea**, que ya existe y ya tiene una persona delante: al
validar aparece «salieron 30, se declararon 20, faltan 10» y se resuelve con un botón —devueltas
o consumidas—. Por eso la conciliación **es Fase 2 y no un extra**: es el cierre del ciclo del
consumible, y sin ella los informes se construyen sobre cantidades sin cuadrar.

### Lo reservado que nunca salió

Es el caso más común y el diseño inicial no lo contemplaba: se reservan 30, salen 20, la tarea
se valida. Sin regla, los 10 no salidos quedan comprometidos **para siempre** y `available`
miente. La regla: al validar, cancelar o rechazar la tarea, `committed` baja en
`reserved - issued`, con un movimiento propio `reservation_released` que lo deja escrito.

## La reserva previa es opcional

Para las toallas del Lidl la hace administración el día antes y tiene todo el sentido. Para los
guantes que el operario coge de camino no hay nada que planificar, y la salida es el primer
movimiento. **Si se obliga a asignar siempre, el módulo se vuelve burocracia y dejan de
usarlo.**

## Quien registra no es quien gasta

En campo el encargado apunta el material de toda la cuadrilla. Si el movimiento solo guardara
la identidad del token, el informe de consumo por empleado acabaría diciendo que el 80% se lo
gastó el supervisor — que es exactamente la pregunta que el módulo venía a contestar.

El precedente está en el propio dominio: `TaskResource` lleva `uploadedBy` y `employeeId` por
separado, y `TaskActivity` lleva `actorId`, `actorRole` y `employeeId`. El movimiento hace lo
mismo:

- **`registeredBy`** — sale del token y no se pregunta nunca.
- **`employeeId`** — a quién se imputa; viene relleno con el anterior y se puede cambiar.

## Consecuencias

- `stock` lleva `onHand` y `committed`.
- `task_materials` lleva `reserved`, `issued`, `consumed`, `returned` y `pending`.
- Tipos de movimiento: `reservation`, `reservation_released`, `issue`, `consumption`, `return`,
  además de `receipt`, `adjustment` y los dos del traspaso. Cantidad **siempre positiva**; el
  signo lo pone el tipo.
- La pantalla de validación de la tarea gana el paso de conciliación (Fase 2).
- `inventory` se entera del cierre por `task.validated`, `task.rejected` y
  `task.status_changed` con `status: "cancelled"` — los eventos que existen.

---

## Adenda 2026-10-08 — el cuadre pregunta también por lo reservado

Jose detectó una tarea validada con «gastado 0»: se había reservado material, el operario no
registró salida ni consumo en la app y, al cerrar, la reserva se soltó y el material volvió al
almacén sin que nadie lo dijera. Lo habitual, no la excepción.

Asignar sigue sin ser consumir: nada se da por gastado solo. Lo que cambia es que **al validar
se pregunta también por lo reservado que no salió**, precargado como gastado, y el validador
corrige. Lo que diga se apunta como salida y consumo de esa cantidad (resolución `used` del
cuadre); el resto se libera como antes. Si se valida sin pasar por el panel (eventos), lo
reservado se libera entero, igual que hasta ahora.


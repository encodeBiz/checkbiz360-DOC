# ADR-006 — Una semana propuesta de nuevo retira lo que ya no trae

**Fecha:** 2026-10-16
**Estado:** Aceptado (resuelve el hueco abierto en cuadrantes TDR-001 §6 y §9)
**Decisionario:** Jose Acevedo (2026-10-16, «a por ello» sobre resolverlo en el lote, para el Excel y el asistente a la vez)

---

## Contexto

En la plantilla, una pestaña con trabajos **es la semana entera** de esa persona
(cuadrantes TDR-001 §2). Pero al aplicar, el lote sólo crea: una tarea que ya no está en el
fichero no se retira, y una a la que le cambia la hora es otra tarea (cambia su `externalRef`).
El TDR lo dejó fuera de la primera versión.

Con el asistente esto deja de ser raro: «la misma semana, pero Marta cubre a Lucía el martes»
es exactamente volver a proponer la semana de Lucía sin ese trabajo. Si no se retira, Lucía
sigue teniéndolo en el móvil.

## Decisión

1. **Al aplicar la propuesta de una persona, se retiran sus tareas de cuadrante de esa semana
   que la propuesta nueva ya no trae.** «De cuadrante» quiere decir `externalRef` que empieza
   por `cuadrante:{employeeId}:` con una fecha dentro de la semana. Una tarea creada a mano o
   por otra integración no se toca nunca.
2. **Sólo las que no han empezado** (`draft` o `assigned`), por la misma regla que ya tiene el
   borrado de tareas (tasks TDR-006). Una empezada, completada o validada se queda, y la
   propuesta lo dice como aviso: «el martes 10:00 ya está empezada y no se retira».
3. **Se enseña antes de confirmar.** La propuesta de cada persona dice cuántas tareas se
   retirarán y cuáles, igual que dice cuántas se crearán. Nada se retira por sorpresa.
4. **Retirar es borrar**, por el `DELETE` del servicio de tareas con la persona que confirma
   como actor: se lleva la tarea y lo que cuelga de ella, y en el modo por tareas el día se
   regenera solo.
5. Vale **igual para el Excel que para el asistente**: es el lote el que lo hace.

## Consecuencias

- La propuesta gana el recuento y la lista de lo que se retirará.
- `limpiar.cli.ts` busca con un rango cuyo límite superior es el propio prefijo, así que hoy no
  encuentra nada; la consulta nueva usa el límite correcto (`prefijo + ""`) y el script
  se corrige con ella.
- Una semana con días ya fichados sigue reescribiéndose igual, pero lo que ya empezó no se
  retira, que es lo que protegía a esos días.

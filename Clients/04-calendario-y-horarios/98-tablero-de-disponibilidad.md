# Tablero de disponibilidad

El tablero de disponibilidad responde a una pregunta que el horario por sí solo no contesta: **cuánta gente hay realmente disponible cada día en cada sucursal, y quién falta**. No es un dato que haya que mantener: el tablero lo calcula cruzando el horario de cada empleado con los festivos, sus ausencias y el estado de su ficha.

Se encuentra en **Horarios** → pestaña **Disponibilidad**.

---

## Qué muestra

Una rejilla con una fila por sucursal y una columna por día. Cada casilla indica cuántas personas están disponibles ese día sobre el total de la plantilla de esa sucursal, con su porcentaje de cobertura.

El color de cada casilla resume la situación:

| Color | Leyenda | Qué significa |
|---|---|---|
| Verde | **Cobertura ≥ 70%** | Está disponible la mayoría de quienes deberían trabajar. |
| Ámbar | **Cobertura ajustada 55 – 70%** | Faltan bastantes personas; conviene revisarlo. |
| Rojo | **Cobertura crítica < 55%** | Hay gente que debería estar y no está: un hueco de cobertura. |
| Gris | **Descanso o festivo** | Ese día nadie trabaja ni debería: la sucursal cierra o es festivo. |

La diferencia entre el gris y el rojo es la más importante del tablero. Un festivo de empresa sale **gris**, porque no falta nadie. Un día laborable en el que media plantilla está de vacaciones sale **rojo**, porque es un problema de cobertura.

Los empleados que no tienen sucursal asignada aparecen agrupados en una fila aparte.

---

## Cómo se usa

- **Vista mensual o semanal.** Cambie entre **Mensual** y **Semanal**, y avance o retroceda con las flechas de periodo.
- **Filtrar por sucursal.** Por defecto se ven **Todas**; elija una para centrarse en ella.
- **Exportar.** El botón **Exportar** descarga un fichero CSV con una fila por sucursal y día: equipo, fecha, disponibles, plantilla y porcentaje de cobertura.

> **Nota:** si la plantilla es demasiado grande para calcularla entera de una vez, el tablero le pedirá que elija una sucursal para ver su cobertura.

---

## El desglose de un día

Pulse una casilla para abrir el desglose de ese día en esa sucursal. Muestra dos columnas:

- **Disponibles**: quién está.
- **No disponibles**: quién no está, y por qué.

Los motivos posibles son:

| Motivo | Qué significa |
|---|---|
| **Sin turno** | Su horario no tiene turno ese día. |
| **Festivo** | Es festivo de la entidad o de la sucursal. |
| **Ausencia** | Tiene registrada una ausencia propia: vacaciones, permiso, día libre. |
| **Baja o permiso** | El estado de su ficha indica que no está en activo. |

El desglose incluye un buscador por nombre, que ignora tildes y eñes y admite nombre y apellidos en cualquier orden.

---

## Marcar o quitar un día libre desde el desglose

El gesto más habitual al mirar el tablero es «esta persona mañana no viene». Se registra desde el propio desglose:

- **Marcar día libre**: arrastre a la persona de **Disponibles** a **No disponibles**, o pulse la flecha de su fila.
- **Quitar el día libre**: arrastre a la persona de vuelta, o pulse la flecha.

Soltar no guarda nada por sí solo: se abre el formulario de siempre, con la persona y la fecha ya puestas, donde puede indicar si la ausencia es **retribuida**. Un arrastre accidental se deshace con **Cancelar**.

Solo se puede devolver a disponible a quien falta por una **ausencia propia**. Los demás motivos no se arreglan desde aquí, y su flecha aparece desactivada con una explicación:

- Un **festivo** de la entidad o de la sucursal afecta a toda la plantilla: se gestiona en su calendario.
- **Sin turno** depende del horario de esa persona: se cambia en su calendario.
- **Baja o permiso** es el estado de su ficha: se cambia ahí.

Después de cada cambio, el tablero vuelve a calcular la cobertura con los datos guardados.

---

## Quién puede verlo

- Owners, administradores y managers ven la disponibilidad de toda la entidad.
- Los supervisores ven la de sus sucursales.
- Los empleados sin responsabilidad de gestión no tienen acceso.

---

## Limitaciones actuales

- Quien trabaja en **dos sucursales** cuenta en las dos: todavía no existe la asignación de turno por día y sucursal.
- Si algún festivo tiene una fecha que no se puede leer, el tablero lo descarta y lo avisa en pantalla; el número de cobertura no lo cuenta.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Horarios base y turnos](./23-horarios-base-y-turnos.md) | El horario semanal del que parte el cálculo |
| [Calendario laboral](./24-calendario-laboral.md) | Festivos por niveles y su efecto en el fichaje |
| [Festivos y días no laborables](./29-festivos-y-dias-no-laborables.md) | Ausencias de empleados, rangos y marca de retribuida |
| [Asignar empleados a sucursales](../08-sucursales-y-entidad/60-asignar-empleados-a-sucursales.md) | De qué sucursal forma parte cada persona |

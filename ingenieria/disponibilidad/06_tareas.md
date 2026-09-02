# 06 — Tareas sueltas

Cambios pequeños que salen del diseño de disponibilidad. Los dos primeros están
verificados contra datos reales de dev (entidad `Wl8ZCvpdmIXzEE0mhT7W`,
2026-09-02), no contra lectura de código.

---

## TAREA 1 — `paid` en `Holiday`

**Estado:** pendiente · **Bloquea:** al front, que ya lo manda · **Tamaño:** pequeña
**Decisión:** [ADR-004](./adr/ADR-004-ausencias-retribuidas.md)

### Para qué

Saber si un día libre es retribuido o no. Esta tarea es la mitad de backend del
[ADR-004](./adr/ADR-004-ausencias-retribuidas.md), que es donde está el razonamiento completo
—incluido por qué "no consta" no puede tratarse como `false`—.

### Lo que ya funciona, comprobado

`paid` **ya viaja de punta a punta**. En dev, las vacaciones del empleado están
guardadas así:

```json
{ "id": "vacaciones-2026-11-11", "name": "Vacaciones",
  "date": "2026-11-11", "description": "Vacaciones anuales", "paid": true }
```

Y sobreviven hasta la respuesta del resolutor. Ningún punto de la cadena filtra
campos: el controlador hace `req.body?.holiday as Holiday` sin reconstruir,
`validateHoliday` sólo exige `name` y `date`, el repositorio guarda
`{...holiday, id}` y `concatHolidays` hace `push(h)`.

**Pero funciona por accidente**, sostenido por un cast y un spread. Nadie puede
depender de él y el compilador no lo ve. La tarea no es fontanería: es declarar
el campo.

### Qué hay que tocar

Sólo el tipo, en los dos sitios donde `Holiday` vive duplicado:

- `encodebiz-api/packages/shared/src/calendar/Calendar.ts`
- `encodeBiz-SAAS/functions/src/services-saas/checkinbiz/domain/entities/Calendar.ts`

```ts
paid?: boolean;   // retribuido. Ausente = no consta, NO "no retribuido".
```

Opcional y sin defecto a propósito: los festivos ya guardados no dicen nada
sobre si eran retribuidos, y ponerles `false` sería inventarse el dato.

### Dónde se usa de verdad

Los datos de dev **confirman el ADR-004 sobre el terreno**. Los festivos de
**empresa** no llevan `paid` —ni "Navidad" de entidad ni "Festivo comunitario" de
sucursal—; lo llevan **las vacaciones del empleado**. Es exactamente lo que el
ADR-004 decide: la casilla se enseña sólo en scope empleado, porque un festivo de
entidad o sucursal es retribuido por definición. El front ya se comporta así.

Y es el único sitio donde puede estar, porque las ausencias se guardan como
festivos. Cuando existan `AbsenceRange` de verdad, `status` distinguirá
`vacation` de `leave_of_absence` y `paid` será derivable — hasta entonces, este
campo es la respuesta.

### No entra en el cálculo

Retribuido o no, quien libra no está disponible. `paid` viaja en la respuesta
como información; nunca decide `available` ni `closed`.

### Aviso para quien cuente días

Las vacaciones de dev son ocho entradas del 11 al 18 de noviembre, y el 14 y el
15 son sábado y domingo — días ya deshabilitados en el horario. Son **8 entradas
marcadas `paid: true` para 6 laborables**. Quien cuente días disfrutados o
retribuidos leyendo el array se equivoca en dos. Otra factura de guardar rangos
como días sueltos.

---

## TAREA 2 — `source` en los festivos resueltos

**Estado:** pendiente · **Bloquea:** la Fase 2 · **Tamaño:** pequeña

### El problema, medido

`concatHolidays` fusiona los festivos de los tres niveles en una lista plana y
**tira el nivel**. Comprobado en dev: para el mismo empleado, `GET /calendar`
devuelve diez festivos donde la Navidad de la entidad, el festivo de la sucursal
y sus ocho días de vacaciones son indistinguibles.

El dato existe en Firestore —cada uno está en su documento— y se destruye en la
resolución, una línea antes de hacer falta.

### Por qué bloquea

Sin el nivel no se puede calcular `closed`. Con las reglas del
[TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md), el 11 de noviembre
—miércoles, con turno— se clasificaría como festivo, y el grupo saldría
`available: 0` con todos los motivos en `{noShift, holiday}`, o sea **`closed`**.

El tablero pintaría en gris *«nadie trabaja y nadie debería»* un miércoles
normal en el que la sucursal se queda sin cubrir porque alguien está de
vacaciones. Con una plantilla de uno se ve exagerado; con una sucursal de
cincuenta que coge el mismo puente, el tablero diría "cerrado, nada que ver" en
lugar de "nadie cubre". Es el número plausible y equivocado hacia arriba que el
[ADR-001](./adr/ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md)
existe para impedir.

### El arreglo

Una función en `shared`, aditiva:

```ts
const pushAll = (list?: Holiday[], source?: HolidaySource) => {
  ...
  combined.push({...h, source});
};
pushAll(entityCal.holidays,    "entity");
pushAll(branchCal?.holidays,   "branch");
pushAll(employeeCal?.holidays, "employee");
```

Nadie se rompe por recibir un campo de más, y `GET /calendar` mejora para todos:
la app puede decir "vacaciones tuyas" en vez de "festivo".

### Deuda asociada, latente

`ResolveEffectiveCalendarUseCase` **no lee `absences[]`**. Quien reserve por esa
vía sería invisible para la app y para el tablero, mientras `BuildPlannedHours`
de analytics sí lo descuenta — dos verdades.

Hoy no ocurre: en dev `absences` está vacío y el panel escribe festivos
(`EmployeeAbsencesModal` tipa sus ausencias como `Holiday`). Queda **latente, no
activo**: no bloquea la Fase 2, pero se activa el día que alguien use la API de
ausencias, que existe y valida solapamientos.

### Impacto: verificado, no puede romper nada

El calendario es núcleo duro —lo usan el fichaje, la edición de fichaje, el
planificador, el worker de empleados activos, las horas planificadas y la app—,
así que el cambio se auditó consumidor a consumidor antes de proponerlo.

**Nada se escribe.** El tag se añade en `concatHolidays`, que es camino de
lectura, y sobre una copia. Los documentos de Firestore no cambian. El borrado
de festivos (`deleteCalendarItem`) lee del **repositorio crudo**, no del
resolutor, filtra por `id` y reescribe: ese camino es ajeno al cambio.

**El fichaje no persiste el array.** `scheduleApplied.scheduleDay` es un objeto
construido campo a campo —`date`, `weekday`, `isWorkingDay`, `isHoliday`,
`disabled`, `shifts`, `plannedMinutes`—. `holidays[]` no entra.

**Todos los lectores leen sólo `.date`**, sin excepción:

```js
holidays?.some(h => h.date === X)
```

`resolveEffectiveDay` (shared), `createChecklog` (contenedor y SAAS),
`checkActiveEmployeeWorker` y `executeEmployeePlanifier` (triggers). Ninguno lee
otro campo, itera por índice ni compara objetos completos.

**Analytics** resuelve sobre `PostgresCalendarRepository`, que lee la columna
`holidays` de `dim_calendars`. La columna no cambia.

**La app** hace `(json['holidays'] as List).map((e) => e.toString())`.
`.toString()` sobre un Map nunca lanza, y esa lista no la consume nadie en
`lib` — se parsea, se guarda en la entidad y ahí muere. (Efecto colateral ya
existente: hoy guarda mapas convertidos a texto, así que es inservible tal cual.
No lo introduce este cambio.)

**Condición de implementación:** usar `{...h, source}`, **nunca** mutar `h`. Con
`includeRaw: true` el resolutor devuelve `raw.entity/.branch/.employee`, cuyos
arrays contienen esos mismos objetos; mutar contaminaría el crudo.

**Prueba de no regresión:** ejecutar la misma lectura contra dev antes y después
del cambio. La salida debe ser idéntica salvo el campo nuevo.

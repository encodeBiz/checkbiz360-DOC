# ADR-005 — El calendario resuelto se cachea en Postgres, con fallo honesto

**Fecha:** 2026-09-02
**Estado:** Aceptado — se implementa **después** de la Fase 2
**Decisionario:** Jose Acevedo

---

## Contexto

Resolver la disponibilidad cuesta una pasada lineal sobre la plantilla, y esa pasada cruza dos
nubes: el contenedor está en OVH y Firestore en GCP. La [Fase 2](../04_fases.md) la paga en cada
carga del tablero.

Hay además un problema que no es del tablero y que ya está en producción: `BuildPlannedHours`
de `analytics` resuelve el calendario efectivo empleado a empleado contra `dim_calendars`, y
`dim_calendars` sólo se rellena cuando alguien hace `POST /api/analytics/dimensions/sync` **a
mano** — no hay cron que lo dispare. O sea que el informe de horas planificadas ya corre sobre
un espejo que nadie refresca.

Cuatro caminos.

**Opción A — Nada. Resolver en cada petición.** Es la Fase 2.

**Opción B — Leer de `dim_calendars`,** el espejo crudo que ya existe, y resolver en lectura.

**Opción C — Materializar la rejilla** `(sucursal, fecha) → disponibles`.

**Opción D — Cachear el calendario **resuelto** por par (empleado, sucursal),** invalidado desde
las escrituras, y expandir los días en memoria.

---

## Decisión

Se elige la **Opción D**, con tres condiciones que son parte de la decisión:

1. **La tabla es una caché, no una fuente.** Una fila ausente o marcada sucia se reconstruye
   antes de responder. El camino de fallo es el plan de lectura de la Fase 2.
2. **La escritura marca sucio de forma síncrona; la reconstrucción es asíncrona e idempotente.**
3. **Se implementa después de la Fase 2**, no en su lugar.

Y arrastra una decisión de alcance: **se porta el módulo de escritura del calendario al
contenedor**, para que la invalidación ocurra en el mismo request que hace el cambio.

---

## Justificación

**Guardar el calendario resuelto es guardar la salida de `ResolveEffectiveCalendarUseCase`
indexada por sus entradas.** La clave `(entity, branch, employee)` es literalmente la firma de
esa función. Eso da gratis la propiedad que el [TDR-001](../tdr/TDR-001-calculo-de-disponibilidad.md)
§8 persigue a mano: que la agregación y la resolución individual no se contradigan deja de ser
una prueba que vigilar y pasa a cumplirse por construcción, porque son el mismo valor.

**Por par y no por día, porque el rango no debe entrar en el almacenamiento.** La Opción C tiene
un problema de horizonte —los festivos se pueden meter para el año que viene, así que nunca se
sabe hasta dónde materializar— y cualquier cambio toca todas las fechas futuras. Guardando
horario semanal y periodos libres, el número de filas es plantilla × sucursales y **no crece
con el calendario**: cuesta lo mismo pedir un día que dos meses.

**El espejo crudo no sirve como fuente.** La Opción B parece gratis porque `dim_calendars` ya
existe, pero se sincroniza a mano y sin cron. Un tablero que no enseña el festivo que se metió
hace cinco minutos es el número plausible y equivocado que el [ADR-001](./ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md)
existe para impedir. La caché de esta decisión, en cambio, se invalida desde la escritura y
además tiene fallback.

**Y por eso la tabla es caché y no fuente.** Si la reconstrucción se pierde —el proceso muere,
se redespliega, el POST falla—, una fuente se queda mintiendo hasta que alguien lo note. Una
caché con fila sucia sólo se pone lenta. El peor caso pasa de "falso" a "tarda".

**Marca síncrona, reconstrucción asíncrona, y no al revés.** Reconstruir en segundo plano sin
dejar rastro tiene tres fallos: el redespliegue mata el trabajo en vuelo sin que nadie lo sepa;
las escrituras en ráfaga —el panel guarda **un `PATCH` por día de festivo**, así que marcar dos
semanas son ~14 escrituras— lanzan 14 reconstrucciones solapadas donde puede ganar la que
empezó con los datos viejos; y un fallo de la reconstrucción no se reintenta. La marca resuelve
los tres: se colapsa sola, sobrevive al reinicio y da reintento por definición.

**Y la marca es barata en todos los ámbitos**, que es lo que hace viable el fan-out:

```sql
UPDATE dim_calendars_resolved SET dirty_at = NOW() WHERE entity_id = $1;                    -- entidad
UPDATE dim_calendars_resolved SET dirty_at = NOW() WHERE entity_id = $1 AND branch_id = $2;  -- sucursal
UPDATE dim_calendars_resolved SET dirty_at = NOW() WHERE entity_id = $1 AND employee_id = $2; -- empleado
```

Una sentencia contra la clave primaria, en local. Lo proporcional a la plantilla es la
reconstrucción, y está fuera del camino del usuario.

**La marca va antes de escribir en Firestore.** Si falla, se puede fallar el request de verdad
porque todavía no se ha tocado nada. Al revés no: cuando la escritura ya ocurrió, devolver
error sería decirle al usuario que no se guardó algo que sí se guardó. Marca de más es gratis
—reconstruye y sale el mismo valor—; marca de menos es una mentira persistida.

**Portar las escrituras evita los triggers.** Un trigger de Firestore da entrega con latencia
desconocida y errores tragados: el precedente es `onChecklogSync`, que hace `console.error` y
sigue. Con el upsert en el contenedor la invalidación ocurre en el mismo request que el cambio;
si no ocurre, el request falla y el usuario lo ve. Es la diferencia entre saber y no saber.

**Y repara algo que ya está roto.** Con la resolución cacheada, `BuildPlannedHours` puede dejar
de resolver contra un espejo que nadie refresca. Esa es la razón por la que esto se hace ahora
y no "si la latencia lo pide": no es una optimización para un tablero que aún no existe, es la
reparación de un informe que ya está dando números.

**Pero después de la Fase 2.** El caso de uso hace falta en los dos mundos —es quien
reconstruye—, el tablero es de back office y de baja frecuencia, y cachear algo que no se ha
verificado contra `GET /calendar` empleado a empleado es la forma de convertir un bug en un bug
persistido.

---

## El modelo

```sql
-- La salida de ResolveEffectiveCalendarUseCase, cacheada por sus entradas.
-- La unidad es el par (empleado, sucursal): el horario efectivo de alguien cambia
-- según la sucursal, porque la capa intermedia de la cascada es distinta.
CREATE TABLE IF NOT EXISTS dim_calendars_resolved (
  entity_id       VARCHAR(128) NOT NULL,
  branch_id       VARCHAR(128) NOT NULL,   -- '__unassigned__' si no tiene ninguna
  employee_id     VARCHAR(128) NOT NULL,

  -- Censo. Va aquí para no releer los N documentos de empleado en cada carga;
  -- sin el censo la tabla no ahorra lo suficiente para justificarse.
  full_name       TEXT,
  employee_status VARCHAR(32),
  computable      BOOLEAN NOT NULL DEFAULT TRUE,

  -- Calendario ya cascadeado para ESTE par.
  timezone        VARCHAR(80),
  weekly_schedule JSONB,
  -- [{from, to, reason, name, source, paid}] — un festivo es un periodo de un día;
  -- una ausencia con rango es el mismo objeto con from != to.
  days_off        JSONB NOT NULL DEFAULT '[]',

  resolved_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  dirty_at        TIMESTAMPTZ,

  PRIMARY KEY (entity_id, branch_id, employee_id)
);

CREATE INDEX IF NOT EXISTS idx_dim_calendars_resolved_dirty
  ON dim_calendars_resolved (entity_id) WHERE dirty_at IS NOT NULL;

-- Cuándo se reconcilió por última vez QUIÉN existe. Aquí vive el TTL: las altas,
-- las bajas y los cambios de sucursal se siguen escribiendo desde Firebase.
CREATE TABLE IF NOT EXISTS dim_calendars_roster (
  entity_id     VARCHAR(128) PRIMARY KEY,
  reconciled_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

No hay fechas en la tabla: el rango no se materializa.

### Una carga del tablero

1. Mirar `dim_calendars_roster`. Si falta o pasó el TTL, leer sucursales y empleados de
   Firestore —dos queries—, dar de alta las filas que falten con `dirty_at`, borrar las de quien
   ya no está, y actualizar `reconciled_at`.
2. `SELECT … WHERE entity_id = $1`, por prefijo de la primaria.
3. Reconstruir ahí mismo las filas con `dirty_at` antes de contestar. Al limpiar el flag,
   comprobar que `dirty_at` sigue siendo el que se leyó: si otro upsert lo movió, se queda sucia
   y se rehace.
4. Expandir sobre el rango en memoria.

El paso 3 es la misma función que corre en segundo plano, así que el tablero **no puede servir
una fila sucia** aunque el proceso de fondo esté caído.

---

## Consecuencias

**Positivas:**

- Una consulta local sustituye a la pasada cruzando nubes.
- La coincidencia entre rejilla y resolución individual pasa a ser estructural.
- `BuildPlannedHours` puede dejar de depender de un espejo sin cron.
- Con la tabla vacía el sistema se comporta exactamente como la Fase 2: la caché es el mismo
  diseño con memoria, no un diseño alternativo.
- El contrato no cambia. Cambia de dónde sale el número.

**Negativas / Compromisos aceptados:**

- **Dos tablas y un protocolo de sucio que mantener.** Es estado derivado, y el estado derivado
  se puede desincronizar; el fallback y el TTL son el precio de admitirlo.
- **El censo llega con retraso.** `status`, `branchId`, altas y bajas se siguen escribiendo
  desde Firebase, así que hasta que se porte también ese módulo el tablero puede ir hasta un TTL
  por detrás en la plantilla. Se acepta porque es una garantía acotada y **escrita**, no una
  deriva silenciosa. Los cambios de calendario, que son los frecuentes, sí son inmediatos.
- **Obliga a portar las escrituras del calendario** antes de que la invalidación sea fiable.
  Es trabajo que había que hacer igual, pero aquí se vuelve prerrequisito.

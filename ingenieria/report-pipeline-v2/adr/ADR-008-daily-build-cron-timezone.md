# ADR-008 — Resolución de zona horaria del cron del daily build (`etz → tz del centro → UTC`)

**Fecha:** 2026-07-26
**Estado:** Aceptado — pendiente de corrección en código
**Decisionario:** Jose Acevedo
**Componente:** `services/reports` — `DailyReportCron.runHourlyCronTick`
**Relacionado:** corrige una divergencia de [TDR-003](../tdr/TDR-003-daily-report-build.md) (§ línea `tz_used = checkinLog.etz ?? tz`)

---

## Contexto

El build diario de `employee_daily_reports` lo dispara un cron interno (`node-cron`) en el
servicio `reports`: `runHourlyCronTick` corre cada hora en punto (`"5 * * * *"`, UTC) y su
intención es construir "ayer" para cada centro **a las 02:00 de la hora local de ese centro**
(bien pasada la jornada, para que estén todos los fichajes).

Para saber cuándo es "las 02:00 locales", el tick descubre las zonas horarias así:

```sql
SELECT DISTINCT etz, entity_id, branch_id
FROM checklogs_raw
WHERE etz IS NOT NULL
  AND synced_at >= NOW() - INTERVAL '30 days'
```

**El problema:** `etz` es la zona horaria **del empleado**, y solo se puebla cuando el empleado
trabaja en **remoto**. Para el personal presencial `etz` es `NULL`. Es decir, el tick solo
"suena" para zonas que tengan fichajes de remotos. Un centro con solo personal presencial es
**invisible** para el descubrimiento de zonas y nunca dispara su propio 02:00.

Esto **diverge de TDR-003**, que ya establece el fallback correcto para la zona de cálculo
(`tz_used = checkinLog.etz ?? tz`, donde `tz` es la del centro) y asume un "cron de 02:00" por
centro. La implementación del *scheduling* nunca aplicó ese fallback.

### Estado observado en producción (2026-07-26)

- De 964 checklogs, solo **34** tienen `etz` (los remotos de **Arendel**, `Europe/Madrid`).
  ACB2 (`America/New_York`) y Encodebiz (`Europe/Madrid`, presencial) tienen `etz = NULL`.
- La zona real del centro **sí** está disponible en cada fichaje en `metadata_raw->>'tz'`
  (ACB2 = `America/New_York`, Encodebiz/Arendel = `Europe/Madrid`).
- Consecuencia observada: el tick solo suena a las 02:xx de Madrid (= 00:05 UTC en CEST).
  Cuando suena, `runDailyReportBuild(fecha)` reconstruye esa fecha para **todas** las entidades,
  así que ACB2 entra **de rebote** — pero se construye a las **02:xx de Madrid = 20:xx de Nueva
  York del mismo día**, con la jornada de NY **aún sin terminar**.

### Bug (dos fallos encadenados)

1. **El tick solo descubre zonas por `etz` (remoto).** Para zonas sin remotos activos no suena
   nunca. Todo el build diario depende hoy de que Arendel tenga remotos en Madrid dentro de la
   ventana de 30 días; si dejara de tenerlos, **no se construiría nada para nadie**.
2. **El build no respeta la zona de cada centro.** Cuando suena una zona, se reconstruye la fecha
   entera para todos los centros, arrastrando a centros de otras zonas a una hora equivocada.
   ACB2 se construye demasiado pronto (20:xx NY): si un empleado fichara una salida tardía
   (ej. 21:00 NY), ese pase no la recogería y **nadie reconstruye ese día después** → registro
   incompleto.

> Nota: a fecha de este ADR el bug está **latente**, no ha corrompido datos, porque las salidas
> reales de ACB2 son por la tarde NY (≈15:30), muy antes de las 20:xx. Pero es incorrecto por
> diseño.

---

## Decisión

**El tick resuelve la zona horaria de cada centro con el fallback `etz → metadata_raw.tz → UTC`,
y cada centro se construye a las 02:00 de SU zona, no barriendo la fecha entera cuando suena
otra zona.**

Concretamente:

1. El descubrimiento de zonas usa la **zona efectiva del centro**, no solo `etz`:

   ```sql
   SELECT DISTINCT
     entity_id, branch_id,
     COALESCE(NULLIF(etz, ''), metadata_raw->>'tz', 'UTC') AS tz
   FROM checklogs_raw
   WHERE synced_at >= NOW() - INTERVAL '30 days'
   ```

   (Se mantiene `etz` con prioridad por coherencia con TDR-003: un remoto que ficha en su propia
   zona debe cerrarse a las 02:00 de esa zona.)

2. Para cada `(entity, branch, tz)` cuya hora local sea las 02:xx **en ese momento**, se
   construye **solo ese centro** para "ayer en su zona" — no la fecha global. Esto requiere una
   ruta de build por centro (extraer el build de un par `entity+branch+fecha` de
   `runDailyReportBuild`).

---

## Justificación

- **Cada centro debe cerrarse cuando SU jornada ha terminado.** 02:00 locales garantiza que
  todos los fichajes del día (incl. salidas tardías) ya están sincronizados. Construir a las
  20:xx locales rompe esa garantía.
- **El dato para el fallback ya existe en Postgres** (`metadata_raw->>'tz'`), presente en todos
  los fichajes (remoto o presencial). No hace falta leer Firestore en el tick.
- **Coherencia con la spec.** TDR-003 ya definió `etz ?? tz`; esto lo lleva del cálculo también
  al *scheduling*.
- **Elimina el punto único de fallo.** El build deja de depender de que exista algún remoto
  activo en alguna zona.

---

## Consecuencias

**Positivas:**
- Cada centro se construye a su 02:00 local, con la jornada cerrada.
- Centros de solo presenciales disparan su propio build.
- Sin dependencia de la existencia de remotos.

**Negativas / Compromisos aceptados:**
- El tick pasa a construir por centro (más llamadas cortas) en vez de una fecha global; a la
  escala actual es irrelevante.
- Requiere refactor menor: una función de build por `entity+branch+fecha`.

**Invariante que esta decisión protege:**
> *Un centro nunca se construye antes de que su jornada local haya terminado, y ningún centro
> depende de otra zona para que se dispare su cierre diario.*

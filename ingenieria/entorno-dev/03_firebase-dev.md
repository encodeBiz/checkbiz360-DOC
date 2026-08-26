# 03 — Firebase en desarrollo

El proyecto `dev-encodebiz` tiene 90 funciones desplegadas y congeladas desde mayo. Son, casi
exactamente, el mundo anterior a las migraciones a contenedor. Ponerlo al día no es actualizarlo:
es decidir cuál es el set objetivo y dejar que Firebase reconcilie.

---

## Cómo se hace la limpieza

**No se borran 90 funciones a mano.** Se define el set objetivo en el código y se despliega:

```bash
firebase deploy --only functions --project dev-encodebiz --force
```

Firebase compara lo desplegado contra lo que exporta el código y **borra lo que sobra**. El `--force`
solo evita la confirmación interactiva. Hay que hacerlo con los **tres codebases** declarados en
`firebase.json` (`default`, `health`, `critical`), porque la reconciliación es por codebase.

Requisito previo, hoy ausente: `.firebaserc` solo declara `default`. Gana el alias de desarrollo.

```json
{
  "projects": {
    "default": "encodebiz-services",
    "dev": "dev-encodebiz"
  }
}
```

---

## Qué NO se sube a desarrollo

Funciones cuya superficie HTTP **ya la sirve un contenedor**, verificado ruta a ruta:

| Función de Firebase | Quién lo sirve ahora |
|---|---|
| `checkinbiz-tasksHandler` | `tasks:3006` — `/api/v1/tasks`, 14 rutas |
| `checkinbiz-documentsHandler` | `documents:3007` — `/api/v1/documents`, 8 rutas |
| `checkinbiz-generateReport` | `reports:3005` — `POST /api/reports/generate` |
| `checkinbiz-createChecklog` | `checkinbiz:3002` — `POST /api/v1/checkinbiz/checklogs` |
| `checkinbiz-updateChecklog` | `checkinbiz:3002` — `POST …/checklogs/update` |
| `checkinbiz-requestManualChecklog` | `checkinbiz:3002` — `POST …/checklogs/manual-request` |

Y una que ya está dada de baja y **no debe volver**: `firebaseEntrySchedule-cleanupUnverifiedUsers`,
retirada de producción el 2026-07-31 porque borraba owners reales sin cascadear. Sigue desplegada en
`dev-encodebiz`. Es el mejor ejemplo de por qué el entorno estaba podrido: una función que ya se
consideró peligrosa lleva tres meses corriendo contra la base de desarrollo.

`criticalHandler` no aparece en la tabla porque ya está fuera del codebase `default`: vive en
`functions-critical` como proxy. En desarrollo se sube igual, pero **apuntando a desarrollo** — ver abajo.

---

## Qué hay que confirmar antes de decidir

Tres funciones tienen equivalente en contenedor, pero **no sé si el front todavía las llama**. Se
resuelve mirando el `.env` del front y de la app, no discutiéndolo:

- `checkinbiz-checkbizStatsController` frente a `analytics` — `POST /api/analytics/stats` y
  `GET /api/analytics/panel/overview`.
- `checkinbiz-recalcDailyReport` frente a `reports` — `POST /api/reports/cron/trigger`.
- `checkinbiz-analyzeHeuristic` frente a `checkinbiz:3002`.

Mientras la respuesta no sea firme, **se suben**. Sobrar en desarrollo es gratis; faltar rompe la
prueba y hace perder una tarde buscando por qué.

`merlinIa` es solo un proxy hacia `MERLIN_URL`. Se sube y se le cambia la URL — no hay nada que decidir.

---

## Qué falta en desarrollo y hay que subir

Cinco funciones que producción tiene y dev no. Cuatro de ellas son justo las que conectan Firebase con
el servidor, así que **sin ellas el entorno de desarrollo no tiene pipeline de datos**:

- `onChecklogSync` → `POST /api/sync/checklogs`
- `onBranchPatternSync`, `onEmpPatternSync` → `POST /api/analytics/build/pattern-snapshot`
- `onTaskRatingSync` → `POST /api/sync/task-ratings`
- `beforeUserCreatedTrigger`

---

## Configuración — donde está el peligro real

> **Sobre las URLs.** Desarrollo se sirve por HTTP en el 8080, sin TLS: producción no se toca y por
> tanto no hay quien termine el certificado. Los triggers de Firebase mandan su clave S2S en claro
> hacia ahí — asumible porque esa clave es exclusiva de desarrollo y no abre nada de producción.

### `functions/.env.dev-encodebiz`

Es del 25 de mayo. Le faltan tres variables sin las cuales los triggers de sync revientan al arrancar
(`AnalyticsServerClient` lanza si no están):

```
ANALYTICS_SERVER_URL=http://141.95.47.135:8080
ANALYTICS_API_KEY=<la clave S2S de desarrollo, distinta de la de producción>
ENCODEBIZ_API_KEY=<la misma>
MERLIN_URL=http://141.95.47.135:8080/api/v1/gpt/interpret
CHECKLOG_INTERNAL_URL=<la de desarrollo>
```

### `functions-critical/.env.dev-encodebiz` — **este fichero no existe y es el riesgo más serio del proyecto**

El proxy de arranque de la app hace:

```js
const UPSTREAM_BASE = process.env.CRITICAL_UPSTREAM_BASE || "https://api.checkbiz360.com";
```

Sin fichero de entorno, **desplegar el codebase `critical` en `dev-encodebiz` manda los logins de la
app de desarrollo contra producción**. No falla, no avisa: responde 200 y funciona. Se crea el fichero
**antes** de ese despliegue, no después:

```
CRITICAL_UPSTREAM_BASE=http://141.95.47.135:8080
```

De ahí sale el criterio de éxito de la Fase 4: no basta con que la lista de funciones sea la correcta,
hay que **leer la configuración desplegada y comprobar que ninguna función de dev nombra un host de
producción**.

### Stripe

Claves de test y un endpoint de webhook propio apuntando a desarrollo. El fichero de dev ya trae
`STRIPE_WEBHOOK_SECRET_TEST`, así que la mitad del camino está hecha.

# 05 — Integración: Front de administración

**Repo:** `encodebiz-front-saas`
**Ubicación:** la portada — `src/app/main/[entityId]/dashboard/page.tsx`
**Depende de:** fases 2 y 3 verificadas en dev

---

## Qué hay que hacer, en concreto

Esta sección es autocontenida: con lo de aquí se puede hacer la portada sin volver a leer el
resto.

### 1. Dos handlers en el proxy

En `src/lib/http/serverBackendProxy.ts`, junto a `checkinbiz_panel_overview` y con el mismo
patrón:

```ts
// Dashboard operativo → GET /api/analytics/panel/today (analytics, Firebase Auth).
// Una sola llamada: totales, desglose por centro y las listas del «ver más». La
// query string se reenvía tal cual.
checkinbiz_panel_today: {
  envKeys: ['NEXT_BACKEND_URI_CHECKINBIZ_PANEL_TODAY', 'BACKEND_URI_CHECKINBIZ_PANEL_TODAY'],
  methods: ['GET'],
  requiresAuth: true,
},
// Dashboard operativo → GET /api/analytics/panel/weeks. Las últimas semanas cerradas.
checkinbiz_panel_weeks: {
  envKeys: ['NEXT_BACKEND_URI_CHECKINBIZ_PANEL_WEEKS', 'BACKEND_URI_CHECKINBIZ_PANEL_WEEKS'],
  methods: ['GET'],
  requiresAuth: true,
},
```

Variables, una por entorno. El staging del panel es el portátil (`npm run start:dev` lee
`.env.development`); **Vercel sólo tiene producción** y sus variables no se tocan para probar:

```
NEXT_BACKEND_URI_CHECKINBIZ_PANEL_TODAY
  dev  → https://api-staging.checkbiz360.com/api/analytics/panel/today
  prod → https://api.checkbiz360.com/api/analytics/panel/today
NEXT_BACKEND_URI_CHECKINBIZ_PANEL_WEEKS
  dev  → https://api-staging.checkbiz360.com/api/analytics/panel/weeks
  prod → https://api.checkbiz360.com/api/analytics/panel/weeks
```

Las de producción entran en el pase (fase 5), no antes.

### 2. Dos hooks, al lado de `usePanelOverview`

`src/app/main/[entityId]/checkinbiz/panel/components/hooks/`:

- `useOperationalToday(entityId, branchId?)` — llama a `/api/proxy/checkinbiz_panel_today`,
  sondea cada 60 s **sólo con la pestaña visible** (`document.visibilityState`), y para al
  desmontar. Devuelve `{ data, loading, error, refresh, updatedAgoSeconds }`. Sin aritmética:
  todo viene calculado.
- `useOperationalWeeks(entityId, branchId?, weeks = 8)` — una llamada al montar y al cambiar de
  centro. Sin sondeo.

Los tipos de la respuesta se copian de [03](./03_contratos-api.md) como hizo
`usePanelOverview.ts` con `overview`.

### 3. La portada

`page.tsx` pasa a este orden, y **sólo si la entidad tiene CheckBiz contratado**
(`entitySuscription.some(e => e.serviceId === "checkinbiz")`, la misma puerta que hoy usa la
gráfica de plantilla). Sin CheckBiz, la portada queda como está.

```
┌ Hoy · actualizado hace 40 s ───────────────────────────────────────────────┐
│ [Jornada]  30 de 42 en el centro · 7 sin fichaje · 4 con retraso   ver más │
│ [Tareas]   12 vencen hoy · 2 sin empezar a su hora · 3 vencidas    ver más │
│ [Coste]    90 h registradas · 1.234 € · material 85 €              ver más │
│                                                                             │
│  Centro          Previstos  Dentro  Sin fichaje  Retraso  Tareas hoy  Coste │
│  Obra Norte  ●       10       5         4          2         4        312 € │  ← rojo si alert
│  Obra Sur            12      11         1          0         3        402 € │
└─────────────────────────────────────────────────────────────────────────────┘
┌ Últimas 8 semanas ─────────────────────────────────────────────────────────┐
│  [cobertura %]      [tareas a tiempo %]      [coste por semana]            │
│  tabla por centro: cobertura · retraso · a tiempo · coste, 8 columnas       │
└─────────────────────────────────────────────────────────────────────────────┘
  OnboardingCard · EmployeeTrendChart · ServiceList · DescriptionCard  (como hoy)
```

Componentes reutilizables, todos en
`src/app/main/[entityId]/checkinbiz/panel/components/operational/`: `StatTile` para los
tres tiles, `SegmentBar` para el reparto de presencia dentro de un centro, `EvolutionChart` y
`MonthDelta` para las semanas (el delta ya viene del servidor como diferencia entre semanas
consecutivas; el front no resta). `DashboardCard` de `components/common` para el marco.

### 4. El «ver más»

Un drawer lateral por bloque, con lo que **ya viene** en la respuesta; no hay segunda
petición salvo que `people` llegue `null` (`detail: "by_branch"`), y entonces se pide
`&branchId=` al abrir el centro.

- **Jornada:** pestañas por centro. Lista en el orden del servidor: sin fichaje primero (los
  de retraso con los minutos), después en el centro, terminados, jornada sin cerrar, en otro
  centro. Debajo, en gris, «fichó sin estar previsto» y «jornada de ayer sin cerrar».
- **Tareas:** lista con título, centro, asignados, hora prevista y vencimiento; chips por
  `signals`. Cada fila enlaza a la ficha de la tarea.
- **Coste:** por centro, horas y tarifa aplicada; si `rateCoverage < 0.8`, el importe lleva
  «parcial: faltan tarifas». Material, si viaja, con sus movimientos.

Reglas de la casa que aplican aquí:

- **Listas con criterio del servidor.** No se carga todo y se filtra en memoria; el tope de
  detalle lo pone el contrato.
- **Avisar en rojo, no bloquear.** Un centro en rojo es un hecho a mirar, no un error.
- **La UI no narra la mecánica.** «Sin fichaje», no «sin registro en el espejo».

### 5. Textos

Sin i18n no entra nada. El tono es el de Presencia: **«sin fichaje», nunca «ausente» ni
«falta»**; «jornada sin cerrar» para `incomplete`; «fichó sin estar previsto» sin adjetivos.
Las claves del servidor se traducen en el front:

| Clave | es |
|---|---|
| `presence.no_log` | Sin fichaje |
| `presence.working` | En jornada |
| `presence.on_break` | En pausa |
| `presence.finished` | Jornada terminada |
| `presence.pending_validation` | Pendiente de validar |
| `presence.incomplete` | Jornada sin cerrar |
| `presence.other_branch` | En otro centro |
| `signal.start_late` | Sin empezar a su hora |
| `signal.overdue` | Vencida |
| `signal.due_today` | Vence hoy |
| `signal.paused` | Pausada |
| `signal.pending_validation` | Pendiente de validar |
| `alert.no_presence` | Nadie en el centro |
| `source.backfill` | Reconstruido con el calendario actual |

La etiqueta «centro» es la configurable de la entidad (Sucursal, Proyecto, Obra…), como en el
resto del panel.

### 6. Frescura y errores

- `freshness.checklogs.lastSyncedAt` alimenta el «actualizado hace…». Si
  `freshness.reconcile.missing > 0`, un aviso discreto: «hay fichajes pendientes de
  sincronizar»; las cifras se enseñan igual.
- Si `/today` falla: el bloque entero enseña el error y **ninguna cifra**. Nunca ceros.
- Si `/weeks` tiene `dataHealth.history.status = warming`: las semanas de backfill van con una
  marca y una línea: «reconstruido con el calendario actual».

### 7. Qué no cambia

`overview` y el Panel de CheckBiz. La gráfica de plantilla y el onboarding siguen debajo.

---

## Verificación en pantalla

En local contra `api-staging`, con la entidad `Wl8ZCvpdmIXzEE0mhT7W`:

1. Los totales del tile de jornada coinciden con la respuesta cruda del proxy.
2. Un fichaje desde la app mueve el tile en el siguiente sondeo (≤ 60 s).
3. Un centro con previstos y nadie dentro pasada su hora sale en rojo; antes de la hora, no.
4. El drawer de tareas enlaza a la ficha correcta.
5. Sin CheckBiz contratado, el bloque no se renderiza ni dispara la llamada.
6. Con el backend caído, el bloque enseña el error y no un cero.

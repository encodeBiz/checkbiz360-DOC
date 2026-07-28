# TDR-004 — Contrato del API del panel

**Fecha:** 2026-07-28
**Estado:** Diseño para aprobación
**Componente:** `encodebiz-api/services/analytics/src/interfaces/panel.router.ts`
**Decisiones de producto:** ADR-001, ADR-002, ADR-004

---

## Principios del contrato

1. **Una llamada por vista, no una por tarjeta.** El panel actual dispara 12 peticiones que
   releen el mismo rango. Aquí, un `GET` devuelve todo lo que pinta una pantalla.
2. **Comparación incluida.** Toda respuesta trae el periodo actual y el de referencia, con el
   delta ya calculado en servidor. El front no hace aritmética.
3. **Madurez explícita.** Cada bloque trae su `status` (ADR-004). El front nunca adivina si un
   vacío es un error.
4. **Solo lectura.** Nada bajo `/panel` escribe.

---

## Autenticación

`/api/analytics/panel/*` es la única superficie front-facing de analytics: Firebase ID token +
CORS + comprobación de pertenencia entidad↔usuario (`user_entity_roles/{uid}_{entityId}`, rol
`owner` o `admin`).

El resto de `/api/analytics/*` sigue detrás de `X-Encodebiz-Key` y **nunca** debe quedar accesible
desde el navegador — incluye `POST /build/pattern-snapshot`, que escribe.

---

## Endpoint principal

```
GET /api/analytics/panel/overview
    ?entityId=…            (requerido)
    &from=YYYY-MM-DD       (requerido)
    &to=YYYY-MM-DD         (requerido)
    &compareFrom=…         (opcional; por defecto, periodo inmediatamente anterior de igual longitud)
    &compareTo=…
    &branchId=…            (opcional; si viene, la respuesta baja a nivel sucursal)
    &employeeId=…          (opcional; si viene, baja a nivel empleado)
```

Un solo endpoint con tres profundidades, coherente con la espina dorsal (ADR-002): sin
`branchId` responde a nivel entidad, con `branchId` a nivel sucursal, con `employeeId` a nivel
persona. **Los tres devuelven la misma estructura de `spine`**, que es lo que permite navegar sin
cambiar de vocabulario.

---

## Estructura de respuesta

```jsonc
{
  "ok": true,
  "scope": { "level": "entity" | "branch" | "employee", "entityId": "…", "branchId": null, "employeeId": null },
  "period":  { "from": "2026-07-01", "to": "2026-07-28" },
  "compare": { "from": "2026-06-03", "to": "2026-06-30" },

  // ── Espina dorsal (ADR-002) — misma forma en los tres niveles ──────────────
  "spine": {
    "reliability": {
      "value": 0.78, "previous": 0.71, "delta": 0.07,
      "status": "ready",
      "detail": { "quality": 0.78, "maturity": 0.62, "dataPoints": 143 }
    },
    "environmentEffect": {
      "value": -0.12, "previous": -0.04, "delta": -0.08,
      "status": "partial",
      "detail": { "contributors": 4, "crossBranch": 1, "dispersion": 0.09 },
      "reading": "degrada"          // clave estable; el texto lo pone el front
    },
    "fragility": {
      "value": 0.64, "previous": 0.58, "delta": 0.06,
      "status": "ready",
      "detail": { "busFactor": 1, "topShare": 0.52, "employees": 6 }
    }
  },

  // ── Dónde mirar (solo en nivel entity) ────────────────────────────────────
  "branches": [
    {
      "branchId": "Gj8Asd…",
      "branchName": "Venice Shores",
      "attentionRank": 1,
      "spine": { /* misma forma, a nivel sucursal */ },
      "reasons": ["environment_degrading", "bus_factor_1"]
    }
  ],

  // ── Quién sostiene / quién se descuelga (solo en nivel branch) ────────────
  "people": [
    {
      "employeeId": "hctKZ…",
      "employeeName": "Mirla",
      "job": "DISEÑO",
      "responsibility": "manager",
      "criticality": 0.52,           // cuánto depende el centro de esta persona
      "environmentDelta": -0.15,     // cuánto le afecta este centro
      "status": "warming",           // ADR-005: sin arquetipo publicable todavía
      "archetype": null
    }
  ],

  // ── Redundancia por puesto (nivel branch) ─────────────────────────────────
  "coverage": [
    { "job": "DISEÑO", "titulares": 1, "capacitados": 1, "relevo": 0, "status": "ready" }
  ],

  // ── Qué ha cambiado ───────────────────────────────────────────────────────
  "timeline": [
    {
      "date": "2026-07-14",
      "level": "branch",
      "refId": "Gj8Asd…",
      "refName": "Venice Shores",
      "kind": "environment_shift" | "archetype_shift" | "key_change" | "streak",
      "severity": "high" | "medium" | "low",
      "metric": "environmentEffect",
      "from": -0.02, "to": -0.14
    }
  ],

  // ── Estado global del dato (ADR-004) ──────────────────────────────────────
  "dataHealth": {
    "tasks":      { "status": "warming", "have": 46,  "need": 200, "note": "module_recent" },
    "taskRatings":{ "status": "warming", "have": 1,   "need": 50 },
    "costCoverage":{ "status": "partial", "covered": 6, "total": 10 },
    "branchPatterns": { "status": "warming", "have": 26, "need": 60, "unit": "days" }
  }
}
```

---

## Notas de contrato

**`status` por bloque, no global.** Un panel puede tener la fiabilidad `ready`, el efecto entorno
`partial` y las tareas `warming` a la vez. Es el caso normal, no una excepción.

**`reading` es una clave, no una frase.** El servidor devuelve `degrada` / `neutro` / `potencia`;
el texto y el idioma los pone el front. Coherente con no meter copy en el backend.

**Ningún valor crudo de score sale sin su lectura.** El front no debe tener que interpretar un
`-0.12`: recibe también la clave de lectura y el detalle que la sostiene.

**`dataHealth` es lo que permite al front informar del estado de madurez** sin inventarse umbrales
(ADR-004). Es la respuesta a que el módulo de tareas sea reciente: se comunica, no se oculta.

**Compatibilidad.** `POST /api/analytics/panel/stats` (las 19 métricas portadas) se mantiene
mientras dure la migración del front. Se retira cuando `overview` cubra sus casos de uso.

---

## Rendimiento

Una llamada sustituye a doce. Todas las agregaciones se resuelven en SQL sobre índices existentes
(`idx_pattern_snapshots_employee`, `idx_checklogs_entity_branch_ts`). El coste deja de crecer con
el número de tarjetas de la pantalla.

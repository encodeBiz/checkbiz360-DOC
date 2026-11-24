# Canal app/panel — el panel demuestra que es el panel

**Estado:** en desarrollo (11-nov-2026) · staging 12-nov · producción sin fecha
**Decisión:** [ADR-0002](../adr/0002-el-panel-demuestra-que-es-el-panel.md) · **Diseño:** [TDR-001](./TDR-001-prueba-de-panel.md)
**Origen:** incidente del 06-nov (§38 de `deployment-prod/proximo-pase-back.md`) y TDR-002 de documental, «Fase 2»
**Tarea:** CheckBiz360 `zGRy0s1AStJ3bWhr1Hyo` (Jose Manuel)

## En una frase

Hoy la API adivina si una llamada viene del panel o de la app por el `User-Agent`; con esto,
el servidor del panel firma cada llamada con un código que caduca en un minuto, y lo que no
venga firmado se trata como la app.

## Roadmap

### Hoy, 11-nov — desarrollo y beta (nada se sube)

**HECHO el 11-nov.** API `f5f2ef7` y panel `d31073ef`, las dos en `feat/canal-panel-firmado`, solo en local. Tests: `shared` 205/205, `documents` 64/64, `tasks` 9/9, panel 4/4 con el vector; cruce panel → API con reloj real, 11/11. Precisiones e inventario en TDR-001 §3.1 y §8.

| # | Qué | Quién | Dónde |
|---|---|---|---|
| 0 | ADR-0002, este README y TDR-001 | Claude | `DOCS/ingenieria` |
| 1 | `shared`: `resolveClientChannel(headers)`, verificación, modo estricto, aviso por minuto, tests con el vector | agente API | worktree `encodebiz-api/.claude/worktrees/canal-panel`, rama `feat/canal-panel-firmado` desde `origin/develop` |
| 2 | `documents` y `tasks` pasan las cabeceras; sus tests verdes | agente API | ídem |
| 3 | Panel: helper de firma con el vector, cabecera en `serverBackendProxy.ts`, descarte de la cabecera del navegador, inventario de otros `fetch` de servidor | agente panel | worktree `encodebiz-front-saas/.claude/worktrees/canal-panel`, rama `feat/canal-panel-firmado` desde `origin/develop` |
| 4 | Revisión contra este TDR, build y tests de los dos lados | Claude | — |
| 5 | Commits locales en las dos ramas. **Sin push.** | Claude | — |

### Mañana, 12-nov — staging

| # | Qué |
|---|---|
| 6 | Push de las dos ramas; merge a `develop` y a `staging` con `[skip ci]` (API) |
| 7 | Generar el secreto de staging; ponerlo en `.env.staging` del VPS y en el `.env.local` del panel en el portátil |
| 8 | **Paso A**: `up -d --build --no-deps documents tasks` + reiniciar nginx; sonda (tabla del TDR §7, columna «tras A») |
| 9 | **Paso B**: panel local con el secreto contra `api-staging`; comprobar que no salen avisos para el panel; sonda |
| 10 | **Paso C**: `PANEL_CHANNEL_STRICT=true`, reiniciar `documents` y `tasks`; sonda completa; panel real sigue viendo todo |
| 11 | Suite QA de staging; anotar qué necesita el secreto |
| 12 | Apuntar en `proximo-pase-back.md` la sección del pase (A, B y C separados en producción, B en Vercel) |

### Producción — cuando Jose lo diga

A, B y C en tres momentos distintos; C solo tras una semana sin líneas de aviso. Después,
limpieza: borrar la heurística del `User-Agent`.

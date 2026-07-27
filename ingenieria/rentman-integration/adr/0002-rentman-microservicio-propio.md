# ADR 0002 — Rentman como microservicio propio (no módulo de checkinbiz)

- **Estado:** Aceptada e implementada (2026-07-28)
- **Contexto:** integración Rentman ↔ encodeBiz (ver `../README.md`).
- **Supersede parcialmente:** la decisión inicial de ubicarlo como módulo dentro de
  checkinbiz (tomada cuando el alcance era solo push de horas one-way).

## Contexto

El esqueleto nació como módulo en `services/checkinbiz/src/modules/integrations/rentman/`
porque el alcance inicial era pequeño (empujar horas). Desde entonces el alcance creció:
**sync bidireccional por polling, add-on de pago con su propia facturación, su scheduler,
sus tablas de mapping y los rate-limits de Rentman**. Además, el diseño ya situaba el job de
reconciliación fuera de checkinbiz. La ubicación quedó incoherente.

## Decisión

Rentman es un **microservicio propio**: `services/rentman/` (Express/Docker, puerto **3008**),
al mismo nivel que `checkinbiz`, `sync`, `documents`, etc. **checkinbiz no contiene código de
Rentman.**

## Razones

- **Aísla los rate-limits de Rentman**: si Rentman corta (403), no arrastra a checkinbiz.
- **Scheduler propio** de polling, sin meter cron-jobs en checkinbiz.
- **Dueño de sus tablas de mapping y su bitácora**, sin ensuciar el dominio de fichaje.
- **Add-on independiente**: se despliega, escala y factura por separado.
- **Cero acoplamiento**: el push de horas se alimenta leyendo `checklogs_raw` de PostgreSQL
  (que ya llena el servicio `sync`), no con llamadas desde checkinbiz.

## Consecuencias

- Un despliegue más (asumible: ya es un producto con su facturación).
- Migración `002_rentman.sql` sigue en `/migrations` (misma BD analytics compartida).
- Rutas: `/api/v1/rentman` (gestión autenticada + webhook público como vía secundaria).
- Implementado en `feat/rentman-service` (commit `2051c13`): `git mv` del módulo completo,
  wiring en root `package.json`, `docker-compose.yml` y `nginx.conf`. typecheck en verde.

## Alternativa descartada

**Seguir como módulo de checkinbiz:** más simple en despliegue, pero acopla los rate-limits y
el scheduler de Rentman al servicio de fichaje y mezcla dominios. Rechazada por aislamiento y
por ser un add-on con ciclo de vida propio.

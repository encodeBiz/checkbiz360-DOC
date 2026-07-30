# ADR-004 — Auth por ruta, no middleware global

**Estado:** Aceptado
**Fecha:** 2026-07-30
**Contexto:** checklogs-http

---

## Contexto

`services/checkinbiz/src/app.ts` monta hoy tres bloques: un router público (`/auth/validate`), y dos protegidos por `requireFirebaseAuth` (`/auth/login`, `/calendar` y el router general). El middleware exige un Firebase ID token válido antes de que la petición llegue al controlador.

Las rutas de checklogs no encajan en ese esquema:

- `POST /checklogs` acepta **dos tokens distintos** según el caso. La app ficha con el `sessionToken` —un JWT firmado con `JWT_2FA_SECRET` que emite `/auth/validate`— y un administrador ficha por otro con un Firebase ID token y `isAdmin: true` en el body. Cuál aplica se decide leyendo el body, es decir, después de parsearlo.
- `POST /checklogs/update` y `/checklogs/manual-request` sí usan ID token, pero además necesitan el `uid` decodificado dentro de `req.body.uid`, que es de donde lo leen los controladores.

## Decisión

El router de checklogs se monta **antes** del `requireFirebaseAuth` global, y cada ruta resuelve su propia auth con las mismas funciones que hoy usa Firebase (`validateToken`, `validateTokenJWT`), portadas 1:1 desde `@encodebiz/shared`.

```
POST /checklogs
  body.isAdmin === true → validateToken     → req.body.uid = decoded.uid
  resto                 → validateTokenJWT  → req.body = {...body, ...payload}

POST /checklogs/update         → validateToken → req.body.uid
POST /checklogs/manual-request → validateToken → req.body.uid
```

## Justificación

Es lo que ya hace `tasks` (ADR-004 de `tasks-service`) y por la misma razón: en un port, el comportamiento de auth es contrato. Sustituir la verificación por `requireFirebaseAuth` cambiaría en producción quién puede entrar y con qué token, que es exactamente el tipo de cambio que no se quiere mezclar con una migración de servidor.

Además, con un middleware global la ruta de fichaje sería directamente imposible: el token de la app no es un ID token de Firebase y `requireFirebaseAuth` lo rechazaría antes de poder mirar el body.

## Consecuencias

**A favor**

- El comportamiento de auth es idéntico al de Firebase, verificable caso por caso contra los contratos.
- La app sigue fichando con el token que ya tiene, sin reautenticarse.

**En contra**

- La auth queda repartida entre `app.ts` (global) y el router de checklogs (propia). Hay que leer las dos para saber qué protege qué; se documenta en el propio router.
- Un olvido en una ruta nueva del router de checklogs la dejaría abierta, porque no hay red debajo. La contramedida es la prueba de la Fase 1: toda ruta responde 401 sin token.

**Nota sobre el `JWT_2FA_SECRET`**

Es el mismo secreto que ya usa `/auth/validate` para firmar, y ya está en el entorno del servicio. No hay secreto nuevo que aprovisionar.

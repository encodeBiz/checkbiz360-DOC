# Plan de Remediación — Pentest 2026-05-29

**Estado:** En ejecución  
**Responsable:** Jose Acevedo  

---

## Correcciones aplicadas en esta sesión

### ✅ P-01 — JWT alg:none bypass (CRÍTICO)
- **Commit:** `security: remove dev-mode auth bypass across 28 HTTP entry-points`
- **Archivos:** 28 entry-points en `firebase-entry-http/`, `checkinbiz/`, `passinbiz/`
- **Cambio:** Eliminado el bloque `if (process.env.ENV == "production" || req.headers.authorization)`. Los validators se llaman siempre sin condición.

### ✅ P-02 — Token Firebase a HTTP externo (CRÍTICO)
- **Archivo:** `functions/src/firebase-entry-http/api-express/merlin-ia.ts`
- **Cambio:** Si `MERLIN_API_KEY` está en env vars, se usa como credencial de servicio en lugar del token Firebase del usuario.
- **Pendiente:** Configurar `MERLIN_API_KEY` en producción y migrar URL a HTTPS.

### ✅ P-03 — Rate limit bypass X-Forwarded-For (ALTO)
- **Archivo:** `functions/src/firebase-entry-http/users/recovery-pass-users.ts`
- **Cambio:** `getClientIp()` usa `req.ip` (confiable en Cloud Functions) en lugar del header `X-Forwarded-For` controlado por el cliente.

### ✅ P-04 — URL hardcodeada (MEDIO)
- **Archivo:** `functions/src/firebase-entry-http/api-express/merlin-ia.ts`
- **Cambio:** URL lee de `process.env.MERLIN_URL` con fallback.
- **Pendiente:** Añadir `MERLIN_URL=https://...` a las env vars de producción.

### ✅ P-05/P-06 — Security headers + x-powered-by (MEDIO/BAJO)
- **Archivo:** `functions/src/firebase-entry-http/critical-handler.ts`
- **Cambio:** Añadido middleware de security headers y `app.disable("x-powered-by")`.

### ✅ P-07 — Sin límite de body size (MEDIO)
- **Archivo:** `functions/src/firebase-entry-http/critical-handler.ts`
- **Cambio:** `express.json({ limit: "100kb" })`.

### ✅ P-08 — Doble JSON encoding (BAJO)
- **Archivos:** `validateToken.ts`, `validateUserToken.ts`, `validateTokenWith2FA.ts`, + handlers
- **Cambio:** Clase `AuthError` + helper `authErrorToResponse`. Errors ya no se `JSON.stringify`.

---

## Pendientes (requieren acción manual)

| ID | Acción | Responsable | Prioridad |
|---|---|---|---|
| P-02 | Configurar `MERLIN_API_KEY` en prod env vars | DevOps | 🔴 ALTA |
| P-02 | Migrar URL de merlinIa de HTTP a HTTPS | Dev | 🔴 ALTA |
| P-04 | Añadir `MERLIN_URL` a `.env.encodebiz-services` | DevOps | 🟡 MEDIA |
| P-05 | Extender security headers a todos los onRequest (no solo criticalHandler) | Dev | 🟡 MEDIA |
| P-09 | Verificar que en producción los 404 de funciones no revelan listado | QA | 🟢 BAJA |

---

## Verificación post-deploy

Ejecutar estos comandos contra producción para confirmar que los fixes están activos:

```bash
# 1. JWT alg:none sigue dando 401
HEADER=$(echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr '+/' '-_' | tr -d '=')
PAYLOAD=$(echo -n '{"uid":"attacker","iss":"https://securetoken.google.com/encodebiz-services","aud":"encodebiz-services","exp":9999999999,"iat":1000000000}' | base64 | tr '+/' '-_' | tr -d '=')
FAKE="${HEADER}.${PAYLOAD}."

curl -s -o /dev/null -w "%{http_code}" \
  -X POST https://us-central1-encodebiz-services.cloudfunctions.net/apiV100-firebaseEntryHttp-entity-createEntity \
  -H "Content-Type: application/json" \
  -d "{\"idToken\":\"$FAKE\",\"name\":\"TEST\"}"
# Esperado: 401

# 2. Rate limit bypass ya no funciona
for i in 1 2 3 4 5; do
  curl -s -o /dev/null -w "%{http_code} " \
    -H "X-Forwarded-For: 1.2.3.$i" \
    -d '{"email":"test@test.com"}' \
    https://us-central1-encodebiz-services.cloudfunctions.net/apiV100-firebaseEntryHttp-users-recoveryPassUsers
done
# Esperado: 200 200 200 429 429

# 3. Security headers presentes
curl -sI https://us-central1-encodebiz-services.cloudfunctions.net/apiV100-firebaseEntryHttp-criticalHandler/auth/login | grep -i "x-content-type\|x-frame\|referrer"
# Esperado: headers presentes
```

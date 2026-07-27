# Plan de Remediación — Security Audit EncodeBiz

**Fecha del audit:** 2026-05-25  
**Total de hallazgos:** 17  
**Críticos:** 5 | **Altos:** 5 | **Medios:** 5 | **Bajos:** 2

---

## 🚨 FASE 0 — Acción Inmediata (< 24 horas)

Estos hallazgos representan compromiso activo o riesgo de compromiso inmediato. **Detener todo desarrollo no crítico hasta resolverlos.**

### 1. Revocar service accounts comprometidas (BE-01, BO-01)

```bash
# Google Cloud Console → IAM & Admin → Service Accounts
# Revocar / deshabilitar:
#   firebase-adminsdk-fbsvc@encodebiz-services.iam.gserviceaccount.com
#   La cuenta referenciada en encodebiz-services-adminsdk.json
#   La cuenta referenciada en encodebiz-bcff36ce9c72.json

# Verificar accesos recientes (logs de auditoría):
gcloud logging read \
  'protoPayload.serviceName="iamcredentials.googleapis.com"' \
  --project=encodebiz-saas \
  --limit=100 \
  --format=json
```

**Owner:** Tech Lead  
**Estimado:** 2 horas

### 2. Rotar todos los secretos del `.env` (BE-02)

| Secreto | Acción | Servicio |
|---|---|---|
| `STRIPE_SECRET` | Rotar en Stripe Dashboard → API keys | dashboard.stripe.com |
| `STRIPE_WEBHOOK` / `STRIPE_WEBHOOK_SECRET_TEST` | Regenerar webhook endpoints | dashboard.stripe.com |
| `JWT_2FA_SECRET` | Generar nuevo con `openssl rand -base64 64` | Local |
| `STAFF_JWT_SECRET` | Generar nuevo con `openssl rand -base64 64` | Local |
| `ENCRYPTION_KEY` | Generar nuevo con `openssl rand -hex 32` | Local |
| `TWILIO_AUTH_TOKEN` | Rotar en Twilio Console | console.twilio.com |
| `SMTP_PASS` | Rotar credenciales SMTP en AWS SES | aws.amazon.com/ses |
| `GOOGLE_MAPS_API_KEY` | Restringir a IPs/referrers + rotar si es necesario | console.cloud.google.com |
| `MAPBOX_TOKEN` | Rotar en Mapbox Dashboard | account.mapbox.com |

⚠️ **Invalidar todas las sesiones activas** después de rotar `JWT_2FA_SECRET` y `STAFF_JWT_SECRET`.

**Owner:** Tech Lead  
**Estimado:** 3 horas

### 3. Eliminar archivos sensibles del disco (BE-01, BE-02, BO-01)

```bash
# Eliminar service account keys
rm encodeBiz-SAAS/functions/encodebiz-services-adminsdk.json
rm encodeBiz-SAAS/api-express/encodebiz-services-adminsdk.json
rm encodeBiz-SAAS/functions/src/services-saas/passinbiz/infrastructure/services/certs/encodebiz-bcff36ce9c72.json
rm encodeBiz-SAAS/functions/lib/services-saas/passinbiz/infrastructure/services/certs/encodebiz-bcff36ce9c72.json

# Verificar historial de git (no deben haber sido commiteados)
git -C encodeBiz-SAAS log --all --full-history -- "**adminsdk*" "**bcff36*"
git -C encodebiz-front-saas log --all --full-history -- ".env*"

# Si fueron commiteados en algún momento: usar git-filter-repo para purgarlos
pip install git-filter-repo
git filter-repo --path functions/encodebiz-services-adminsdk.json --invert-paths
```

**Owner:** Tech Lead  
**Estimado:** 1 hora

---

## 📅 FASE 1 — Esta semana (< 7 días)

### 4. Secretos → Secret Manager (BE-01, BE-02)

```bash
# Crear secrets en Firebase / GCP Secret Manager
firebase functions:secrets:set STRIPE_SECRET
firebase functions:secrets:set JWT_2FA_SECRET
firebase functions:secrets:set STAFF_JWT_SECRET
firebase functions:secrets:set ENCRYPTION_KEY
firebase functions:secrets:set TWILIO_AUTH_TOKEN
firebase functions:secrets:set SMTP_PASS

# En las Cloud Functions, referenciar via defineSecret():
```

```typescript
import { defineSecret } from 'firebase-functions/params';

const stripeSecret = defineSecret('STRIPE_SECRET');
const jwtSecret = defineSecret('STAFF_JWT_SECRET');

export const myFunction = onRequest(
  { secrets: [stripeSecret, jwtSecret] },
  (req, res) => {
    const stripe = new Stripe(stripeSecret.value());
    // ...
  }
);
```

**Archivos a crear:** `.env.example` en `functions/` con las keys vacías documentadas.

**Owner:** Backend Dev  
**Estimado:** 4 horas

### 5. Corregir Storage Rules (BE-04)

```javascript
// encodeBiz-SAAS/firestore.rules (nuevo archivo)
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Deny por defecto
    match /{allPaths=**} {
      allow read, write: if false;
    }
    // Documentos: solo Admin SDK / Signed URLs
    match /documents/{allPaths=**} {
      allow read, write: if false;
    }
    // Avatares: autenticado, solo el propio usuario
    match /avatars/{userId}/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null
                   && request.auth.uid == userId
                   && request.resource.size < 5 * 1024 * 1024
                   && request.resource.contentType.matches('image/.*');
    }
  }
}
```

**Deploy:** `firebase deploy --only storage`

**Owner:** Backend Dev  
**Estimado:** 2 horas

### 6. Versionar Firestore Rules (BE-05)

```bash
# Exportar reglas actuales
firebase firestore:rules:get --project encodebiz-saas > encodeBiz-SAAS/firestore.rules

# Actualizar firebase.json
# "firestore": { "rules": "firestore.rules", "indexes": "..." }

# Revisar y aplicar principio de mínimo privilegio
firebase deploy --only firestore:rules
```

**Owner:** Backend Dev  
**Estimado:** 4 horas (incluye revisión de reglas existentes)

### 7. Implementar `middleware.ts` en backoffice (BO-02)

Ver código en `AUDIT-BACKOFFICE.md#BO-02`. Crear `src/middleware.ts` con validación de sesión server-side.

**Owner:** Frontend Dev  
**Estimado:** 3 horas

### 8. Migrar `sessionToken` a `FlutterSecureStorage` (MB-01)

```dart
// lib/core/storage/secure_storage_service.dart — añadir:
static const _accessTokenKey = 'access_token';

Future<void> saveAccessToken(String token) async =>
    _storage.write(key: _accessTokenKey, value: token);

Future<String?> getAccessToken() =>
    _storage.read(key: _accessTokenKey);

Future<void> clearAccessToken() =>
    _storage.delete(key: _accessTokenKey);
```

Reemplazar en `auth_provider.dart`:
```dart
// Antes:
await _prefs.setString(AppConstants.accessTokenKey, token);

// Después:
await _secureStorage.saveAccessToken(token);
```

**Owner:** Mobile Dev  
**Estimado:** 3 horas + tests

---

## 📋 FASE 2 — Este sprint (< 30 días)

### 9. Restringir CORS (BE-03)

Implementar allowlist de orígenes en todos los Express handlers. Ver código en `AUDIT-BACKEND.md#BE-03`.

**Owner:** Backend Dev | **Estimado:** 2 horas

### 10. Añadir rate limiting en endpoints auth (BE-06)

Implementar `express-rate-limit` en `/auth/login` y `/auth/validate`. Ver código en `AUDIT-BACKEND.md#BE-06`.

**Owner:** Backend Dev | **Estimado:** 3 horas

### 11. Añadir security headers HTTP al backoffice (BO-04)

Implementar `securityHeaders` en `next.config.ts`. Ver código en `AUDIT-BACKOFFICE.md#BO-04`.

**Owner:** Frontend Dev | **Estimado:** 2 horas

### 12. Limpiar error message leak en `verify-token` (BO-03)

Reemplazar mensaje de error que expone `error.message`. Ver código en `AUDIT-BACKOFFICE.md#BO-03`.

**Owner:** Frontend Dev | **Estimado:** 30 minutos

### 13. Eliminar `console.log` con datos sensibles del 2FA proxy (BO-05)

Eliminar los dos `console.log` de `src/app/api/2fa/enable/route.ts` y `verify/route.ts` en producción.

**Owner:** Frontend Dev | **Estimado:** 30 minutos

### 14. Eliminar dominios de test de `remotePatterns` (BO-06)

Eliminar `example.com` y `placehold.co` de `next.config.ts`.

**Owner:** Frontend Dev | **Estimado:** 15 minutos

### 15. Eliminar almacenamiento de contraseña en "remember me" (MB-02)

Refactorizar `SecureStorageService` para no persistir la contraseña. Ver estrategia en `AUDIT-MOBILE.md#MB-02`.

**Owner:** Mobile Dev | **Estimado:** 4 horas (incluye actualización de flujo biométrico)

### 16. Añadir validación de esquemas con Zod (BE-08)

Implementar schemas Zod en los controladores de mayor riesgo primero: `createChecklog`, `updateChecklog`, `loginEmployee`, `createEmployee`.

**Owner:** Backend Dev | **Estimado:** 8 horas

---

## 🗂 FASE 3 — Backlog priorizado

### 17. SSL Certificate Pinning en Flutter (MB-03)

Implementar pinning de certificados para el dominio de Cloud Run. Ver `AUDIT-MOBILE.md#MB-03`.

**Owner:** Mobile Dev | **Estimado:** 6 horas

### 18. FLAG_SECURE en pantallas sensibles Flutter (MB-06)

Aplicar `FlutterWindowManager.FLAG_SECURE` en pantallas de documentos, asistencia y configuración de seguridad.

**Owner:** Mobile Dev | **Estimado:** 2 horas

### 19. Documentar justificación de `ACCESS_FINE_LOCATION` (MB-05)

Evaluar si `COARSE_LOCATION` es suficiente para la validación de geofencing del checkin. Documentar decisión en `AGENTS.md`.

**Owner:** Mobile Dev | **Estimado:** 2 horas

### 20. Activar Firebase App Check (BE-06 complementario)

Activar App Check en Firebase Console para proteger las Cloud Functions de abuso desde clientes no autorizados.

**Owner:** Backend Dev | **Estimado:** 4 horas

---

## Checklist de cierre de auditoría

Para marcar un hallazgo como **resuelto** se requiere:

- [ ] El fix está en código (con PR revisado y aprobado)
- [ ] El secreto/credencial ha sido rotado (si aplica)
- [ ] La regla/configuración ha sido desplegada al entorno de prod
- [ ] Actualizar la columna Estado en los archivos `AUDIT-*.md` correspondientes
- [ ] Ejecutar `firebase deploy` y verificar reglas activas en Firebase Console

---

## Próxima revisión

Programar nueva auditoría de seguridad en **90 días** (2026-08-25) o antes si:
- Se añaden nuevos módulos con acceso a datos sensibles
- Se cambia el sistema de autenticación
- Se onboarda un nuevo proveedor de servicios (pagos, SMS, email)

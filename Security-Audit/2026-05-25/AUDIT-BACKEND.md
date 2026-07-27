# Auditoría de Seguridad — Backend (encodeBiz-SAAS)

**Fecha:** 2026-05-25  
**Ruta:** `PLATAFORMA/encodeBiz-SAAS/`  
**Stack:** Firebase Functions v2, TypeScript, Node 22, Express, Firestore, Firebase Storage

---

## BE-01 🔴 CRÍTICO — Service Account JSON Keys en disco

**Archivos afectados:**
```
functions/encodebiz-services-adminsdk.json
api-express/encodebiz-services-adminsdk.json
functions/src/services-saas/passinbiz/infrastructure/services/certs/encodebiz-bcff36ce9c72.json
```

**Hallazgo:**  
Existen 3 archivos de clave de service account de GCP presentes en el directorio del proyecto. Aunque el `.gitignore` los excluye correctamente con los patrones `*services-adminsdk*.json` y `*firebase-adminsdk*.json`, su presencia en disco es un riesgo si el repositorio es clonado en un entorno compartido, si se hace un `git add -f`, o si el CI/CD accede al directorio con configuración incorrecta.

El archivo `encodebiz-bcff36ce9c72.json` en la ruta de producción de passinbiz es especialmente preocupante: está dentro de `src/` (código fuente) y es fácil que sea incluido por error en un bundle de producción.

**Impacto:**  
Un atacante con acceso al service account tiene control total sobre Firebase (Firestore, Storage, Auth, Functions). Permite leer/escribir cualquier dato, crear usuarios Admin, eliminar entidades.

**Remediación:**
1. Revocar inmediatamente las service accounts comprometidas en Google Cloud Console → IAM → Service Accounts.
2. Eliminar los 3 archivos del disco y de cualquier backup.
3. Crear nuevas service accounts con el mínimo de permisos necesarios.
4. Mover las credenciales a **Google Cloud Secret Manager** y accederlas en Functions vía `defineSecret()` de Firebase Functions v2.
5. Verificar el historial de git: `git log --all --full-history -- "**adminsdk*"` para confirmar que nunca fueron commiteados.

```typescript
// Forma correcta — Firebase Functions v2 con Secret Manager
import { defineSecret } from 'firebase-functions/params';
const serviceAccountKey = defineSecret('SERVICE_ACCOUNT_KEY');
```

---

## BE-02 🔴 CRÍTICO — Secretos de producción en `functions/.env`

**Archivo afectado:** `functions/.env`

**Secretos presentes:**
```
ENCRYPTION_KEY=7614760e629b08e354...        # Clave AES en plaintext
STRIPE_SECRET=sk_test_51RP0rMR97...         # Stripe secret key
STRIPE_WEBHOOK=whsec_SqYtJIcRR...          # Webhook secret Stripe
JWT_2FA_SECRET=_xOErQalgL-AQXd...          # Secreto JWT 2FA
STAFF_JWT_SECRET=Ti7Blc0vaZeh...            # Secreto JWT staff/session
TWILIO_AUTH_TOKEN=15353c2f01...             # Twilio auth token
SMTP_PASS=BBUvT6IUf4pLylz...               # AWS SES SMTP password
GOOGLE_MAPS_API_KEY=AIzaSyDZT1...          # Google Maps API key
MAPBOX_TOKEN=pk.eyJ1Ijo...                  # Mapbox token
```

**Hallazgo:**  
El `.gitignore` excluye correctamente `.env` y `.env.*`, pero los secretos existen en disco en texto plano. Si este entorno de desarrollo es compartido, o si hay backups automáticos del directorio, estos secretos están expuestos.

Adicionalmente, `NEXT_PUBLIC_RECAPTCHA_SITE_KEY` está hardcodeado en el `.env` cuando debería ser una variable de entorno pública del backoffice, no del backend.

**Impacto:**  
- Stripe: cargos fraudulentos, acceso a datos de facturación de todos los clientes.
- JWT secrets: firma de tokens falsos para suplantar cualquier usuario/empleado.
- Twilio: envío masivo de SMS con cargo a la cuenta.
- SMTP: envío de correos desde la identidad de EncodeBiz.

**Remediación:**
1. Rotar inmediatamente TODOS los secretos listados arriba.
2. Migrar a **Firebase Secret Manager** con `defineSecret()`:
   ```bash
   firebase functions:secrets:set STRIPE_SECRET
   firebase functions:secrets:set JWT_2FA_SECRET
   firebase functions:secrets:set STAFF_JWT_SECRET
   ```
3. Eliminar el archivo `.env` y reemplazarlo por `.env.example` con valores vacíos.
4. Para desarrollo local: usar Firebase Emulator con `.env.local` que también esté en `.gitignore`.

---

## BE-03 🟠 ALTO — CORS abierto (`origin: true`) en todos los handlers

**Archivos afectados:**
```
functions/src/firebase-entry-http/critical-handler.ts:22
functions/src/services-saas/checkinbiz/firebase-checkinbiz-http/documents.ts:8
functions/src/services-saas/checkinbiz/firebase-checkinbiz-http/tasks.ts:7
```

**Hallazgo:**  
```typescript
app.use(cors({ origin: true })); // Acepta CUALQUIER origen
```

`origin: true` refleja el origen de la request como permitido. En producción esto significa que cualquier sitio web puede hacer peticiones autenticadas a las Cloud Functions si el usuario tiene una sesión activa. Esto facilita ataques CSRF cross-origin en endpoints que no validan el `Referer` / `Origin`.

**Remediación:**
```typescript
const ALLOWED_ORIGINS = [
  'https://app.encodebiz.com',
  'https://backoffice.encodebiz.com',
  ...(process.env.ENV === 'dev' ? ['http://localhost:3000', 'http://localhost:3001'] : []),
];

app.use(cors({
  origin: (origin, callback) => {
    if (!origin || ALLOWED_ORIGINS.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
}));
```

---

## BE-04 🔴 CRÍTICO — Storage Rules catch-all público

**Archivo:** `storage.rules`

**Hallazgo:**
```javascript
match /{allPaths=**} {
  allow read, write: if true;  // ← TODO el Storage es público
}
```

Solo el path `/documents/**` está protegido (`allow read, write: if false`). El resto de Firebase Storage —incluyendo avatares, adjuntos, reportes PDF, y cualquier otro path futuro— permite lectura y escritura pública sin autenticación.

El TODO en el comentario reconoce el problema pero no tiene fecha ni owner asignado.

**Impacto:**  
- Cualquier usuario anónimo puede listar, leer y sobreescribir archivos de Storage fuera de `/documents/`.
- Subida de contenido malicioso (malware, imágenes ilegales) que queda alojado en la infraestructura de EncodeBiz.
- Exfiltración de reportes, fotos de perfil, o archivos adjuntos de empleados.

**Remediación:**
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Negar por defecto todo
    match /{allPaths=**} {
      allow read, write: if false;
    }

    // Documentos: solo Admin SDK y Signed URLs (ya correcto)
    match /documents/{allPaths=**} {
      allow read, write: if false;
    }

    // Avatares: solo el propietario puede leer/escribir su avatar
    match /avatars/{userId}/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId
                   && request.resource.size < 5 * 1024 * 1024  // 5MB
                   && request.resource.contentType.matches('image/.*');
    }

    // Reportes: solo lectura autenticada, escritura solo Admin SDK
    match /reports/{entityId}/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if false;
    }
  }
}
```

---

## BE-05 🔴 CRÍTICO — `firestore.rules` ausente del repositorio

**Hallazgo:**  
No existe `firestore.rules` en el directorio `encodeBiz-SAAS/`. El `firebase.json` declara `"firestore": { "indexes": "firestore.indexes.json" }` pero no referencia un archivo de rules.

Esto significa que las reglas de Firestore no están bajo control de versiones. El estado actual de las reglas en producción es desconocido: podrían ser las reglas por defecto de Firebase (deny all en proyectos nuevos, pero open en proyectos legacy), o reglas customizadas no versionadas.

**Impacto:**  
Sin IaC para Firestore rules:
- Imposible hacer code review de cambios de permisos.
- Risk de reglas por defecto permisivas en proyectos heredados.
- Ningún rollback automatizado si las reglas se corrompen.

**Remediación:**
1. Exportar las reglas actuales desde Firebase Console o CLI:
   ```bash
   firebase firestore:rules:get > firestore.rules
   ```
2. Agregar al `firebase.json`:
   ```json
   "firestore": {
     "rules": "firestore.rules",
     "indexes": "firestore.indexes.json"
   }
   ```
3. Aplicar el principio de mínimo privilegio: deny-all por defecto, allowlist explícita por colección.

```javascript
// Estructura mínima recomendada
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Negar todo por defecto
    match /{document=**} {
      allow read, write: if false;
    }

    // entities/{entityId}: solo escritura via backend (Admin SDK)
    // Lectura solo para empleados de esa entidad
    match /entities/{entityId}/{document=**} {
      allow read: if request.auth != null
                  && request.auth.token.entityId == entityId;
      allow write: if false; // Solo Admin SDK
    }
  }
}
```

---

## BE-06 🟠 ALTO — Sin rate limiting en endpoints públicos

**Hallazgo:**  
No existe ningún mecanismo de rate limiting en las Cloud Functions. Los endpoints críticos como `/auth/login` y `/auth/validate` son accesibles sin restricción de frecuencia.

Búsqueda realizada: `grep -r "rateLimit|throttle|rateLimiter"` → sin resultados.

**Impacto:**  
- Brute force de credenciales de empleados en `/auth/login`.
- Abuso de la función de warmup de `createChecklog` (costos de GCP).
- DDoS de aplicación con cold starts repetidos.

**Remediación:**
```typescript
// Opción 1: Firebase App Check (recomendado para endpoints de app móvil)
// Activar en Firebase Console → App Check

// Opción 2: Rate limiting manual en Express (endpoints backoffice)
import rateLimit from 'express-rate-limit';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 10, // 10 intentos por IP
  message: { error: 'Too many login attempts', code: 'auth/rate_limited' },
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/auth/login', authLimiter, async (req, res) => { ... });
```

---

## BE-07 🟡 MEDIO — Warmup ping expone endpoint interno sin validación

**Archivo:** `functions/src/firebase-entry-http/critical-handler.ts`

**Hallazgo:**
```typescript
function warmupChecklog(): void {
  fetch(url, {
    method: 'POST',
    body: JSON.stringify({ _warmup: true }),
  }).catch((_e) => void 0);
}
```

El payload `{ _warmup: true }` es enviado a `createChecklog`. Si ese endpoint no filtra explícitamente el campo `_warmup`, podría crear un CheckLog inválido o corrupto en Firestore. El `CHECKLOG_INTERNAL_URL` también está en el `.env` y apunta a la URL interna de dev (ver BE-02).

**Remediación:**  
Verificar que `createChecklog` rechaza explícitamente payloads de warmup antes de procesarlos. Añadir un header secreto compartido para distinguir warmup de request real.

---

## BE-08 🟡 MEDIO — Validación de inputs sin framework de esquemas

**Hallazgo:**  
Los archivos de controladores usan validación manual (`if (!req.body.x) return res.status(400)...`). No se encontró uso de Zod, Joi o Yup para validación de esquemas en los endpoints.

La validación manual es propensa a errores de omisión (campos no validados, tipos no verificados, injection via campos inesperados).

**Remediación:**
```typescript
import { z } from 'zod';

const CreateChecklogSchema = z.object({
  employeeId: z.string().min(1).max(128),
  branchId: z.string().min(1).max(128),
  type: z.enum(['checkin', 'checkout']),
  timestamp: z.string().datetime(),
  coordinates: z.object({
    lat: z.number().min(-90).max(90),
    lng: z.number().min(-180).max(180),
  }).optional(),
});

// En el controller:
const result = CreateChecklogSchema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json({ error: result.error.flatten() });
}
```

---

## Resumen Backend

| ID | Severidad | Descripción | Estado |
|---|---|---|---|
| BE-01 | 🔴 CRÍTICO | Service account JSON keys en disco | ⚠️ Pendiente |
| BE-02 | 🔴 CRÍTICO | Secretos de producción en `.env` | ⚠️ Pendiente |
| BE-03 | 🟠 ALTO | CORS abierto (`origin: true`) | ⚠️ Pendiente |
| BE-04 | 🔴 CRÍTICO | Storage Rules catch-all público | ⚠️ Pendiente |
| BE-05 | 🔴 CRÍTICO | `firestore.rules` ausente del repo | ⚠️ Pendiente |
| BE-06 | 🟠 ALTO | Sin rate limiting en auth endpoints | ⚠️ Pendiente |
| BE-07 | 🟡 MEDIO | Warmup ping sin validación de payload | ⚠️ Pendiente |
| BE-08 | 🟡 MEDIO | Validación de inputs sin framework de esquemas | ⚠️ Pendiente |

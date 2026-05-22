# Auth Backoffice — Autenticación y 2FA

> Fuente única de verdad para el flujo de autenticación del backoffice (Next.js) y la implementación de autenticación en dos pasos (2FA/TOTP) para usuarios de la plataforma web.

---

## 1. Resumen

El backoffice usa **Firebase Authentication** como proveedor de identidad (email/password y Google OAuth). El token de Firebase (ID token JWT) se refresca automáticamente cada ~55 minutos vía `onIdTokenChanged` y se envía en la cabecera `Authorization: Bearer <idToken>` en cada petición al backend.

La 2FA para el backoffice usa **TOTP** (Time-Based One-Time Password) mediante la librería **speakeasy**, el mismo mecanismo que usa la app móvil para empleados. El secreto se almacena en Firestore bajo `users/{uid}/security/twoFA`.

---

## 2. Flujo de autenticación — Login normal (sin 2FA)

```
Usuario (browser)                 Firebase Auth           Backend (Cloud Functions)
      │                                  │                          │
      ├─ email + password ──────────────>│                          │
      │                                  │──── ID token ───────────>│
      │<───────── UserCredential ─────────                          │
      │                                  │                          │
      ├─ getIdToken() ──────────────────>│                          │
      │<───────── JWT (1h exp) ──────────                           │
      │                                  │                          │
      ├─ fetchUserAccount(uid) ──────────────────────────────────->│
      │<───────── IUser ─────────────────────────────────────────── │
      │                                  │                          │
      ├─ push('/main/{entityId}/dashboard')                         │
```

---

## 3. Flujo de autenticación — Login con 2FA habilitado

```
Usuario (browser)                 Firebase Auth           Backend (Cloud Functions)
      │                                  │                          │
      ├─ email + password ──────────────>│                          │
      │<─ UserCredential ────────────────                           │
      │                                  │                          │
      ├─ get2FAUserStatus(idToken) ──────────────────────────────>│
      │<─ { enabled: true } ─────────────────────────────────────── │
      │                                  │                          │
      ├─ push('/auth/2fa')               │                          │
      │                                  │                          │
      │   [usuario abre app TOTP]        │                          │
      │                                  │                          │
      ├─ verify2FAUserCode(idToken, code)──────────────────────────>│
      │<─ { message: "ok" } ─────────────────────────────────────── │
      │                                  │                          │
      ├─ fetchUserEntities(uid) ─────────────────────────────────>│
      ├─ push('/main/{entityId}/dashboard')                         │
```

**Nota crítica**: Durante el paso `push('/auth/2fa')`, el usuario está autenticado en Firebase pero en una ruta que empieza por `/auth`. El `AuthContext` detecta `inPublicPage = pathName.startsWith('/auth')` y no redirige → el guard de auth no interfiere.

---

## 4. Refresco de token — `onIdTokenChanged`

El contexto de autenticación usa `onIdTokenChanged` (NO `onAuthStateChanged`) porque:

| Evento | `onAuthStateChanged` | `onIdTokenChanged` |
|---|---|---|
| Sign-in | ✓ | ✓ |
| Sign-out | ✓ | ✓ |
| Token refresh (cada ~55 min) | ✗ | ✓ |

Usar `onAuthStateChanged` causaba que el token almacenado en el contexto caducara (exp = 1h) sin que se refrescara, provocando que las llamadas al backend fallaran con `auth/invalid_token` y que el usuario fuera redirigido al login con credenciales "incorrectas" aunque eran válidas.

**Archivos afectados:**

- `encodebiz-front-saas/src/lib/firebase/authentication/stateChange.ts`
- `encodebiz-front-saas/src/contexts/authContext.tsx`

---

## 5. Guard de rutas y stale closures

### Problema original

`watchSesionState` (callback de `onIdTokenChanged`) se re-creaba en cada navegación porque tenía `pathName`, `inPublicPage`, etc. como dependencias. Esto re-suscribía el listener en cada cambio de ruta, causando llamadas espurias y race conditions.

### Solución: refs estables

```tsx
// authContext.tsx
const pathNameRef = useRef(pathName);
const inPublicPageRef = useRef(inPublicPage);
const entityIdRef = useRef(entityId);
const redirectUriRef = useRef(redirectUri);

// Sincronización de refs en cada render (O(1), sin re-suscribir)
useEffect(() => { pathNameRef.current = pathName; }, [pathName]);
// ...

const watchSesionState = useCallback(async (userAuth: User) => {
  // Lee siempre el valor actual via ref, no el closure capturado
  if (!inPublicPageRef.current) push('/auth/login')
  // ...
}, [push, showToast, currentLocale]) // deps mínimas y estables
```

El `useEffect` de suscripción tiene deps `[authToken, watchSesionState]` → solo re-suscribe si cambia el authToken o el locale.

---

## 6. Logout y hard redirect

Al detectar `auth/invalid_token` en el `HttpClient`, el logout debe ser **awaited** antes del hard redirect para que Firebase limpie la sesión local y la nueva página no vea el usuario expirado:

```typescript
// httpClientFetchNext.ts
if (responseError.code === 'auth/invalid_token' || responseError.code === 'twofactor/invalid_token') {
  await logout().catch(() => {});
  window.location.href = "/auth/login?expiredToken=1";
  return {} as T;
}
```

---

## 7. Estructura de datos Firestore — 2FA usuario

```
users/
  {uid}/
    security/
      twoFA/
        secret:      string          # Secreto TOTP en base32 (speakeasy)
        verifiedAt:  Timestamp|null  # null = secreto generado pero no verificado
        createdAt:   Timestamp
```

**Regla**: 2FA se considera **activo** (`enabled: true`) solo cuando `secret` existe **y** `verifiedAt !== null`. Un secreto generado pero no verificado no activa la 2FA en el login.

---

## 8. API Endpoints — Backend (Cloud Functions)

Todos los endpoints requieren `Authorization: Bearer <Firebase ID Token>` en la cabecera.

### `POST /enable2FAUser`

Genera un nuevo secreto TOTP y lo almacena en Firestore. Devuelve el QR en base64.

**Función:** `apiV100-firebaseEntryHttp-enable2FAUser`

**Response:**
```json
{
  "secret": "JBSWY3DPEHPK3PXP",
  "otpauthUrl": "otpauth://totp/EncodeBiz%20(user@email.com)?secret=...",
  "qrImage": "data:image/png;base64,..."
}
```

---

### `POST /verify2FAUser`

Verifica el código TOTP introducido por el usuario. Si es correcto, marca `verifiedAt`.

**Función:** `apiV100-firebaseEntryHttp-verify2FAUser`

**Body:**
```json
{ "code": "123456" }
```

**Response 200:**
```json
{ "message": "Código 2FA verificado correctamente" }
```

**Response 401:**
```json
{ "error": "Código TOTP inválido", "code": "twofactor/invalid_code" }
```

---

### `GET /get2FAUserStatus`

Devuelve si el usuario tiene 2FA habilitado.

**Función:** `apiV100-firebaseEntryHttp-get2FAUserStatus`

**Response:**
```json
{ "enabled": true }
```

---

## 9. Variables de entorno (frontend)

```bash
# .env.development / .env.production
NEXT_PUBLIC_BACKEND_URI_STATUS2FA_USER=https://apiv100-firebaseentryhttp-get2fauserstatus-3bnjgtprva-uc.a.run.app
NEXT_PUBLIC_BACKEND_URI_ENABLE2FA_USER=https://apiv100-firebaseentryhttp-enable2fauser-3bnjgtprva-uc.a.run.app
NEXT_PUBLIC_BACKEND_URI_VERIFY2FA_USER=https://apiv100-firebaseentryhttp-verify2fauser-3bnjgtprva-uc.a.run.app
```

---

## 10. Archivos modificados / creados

### Backend (`encodeBiz-SAAS/functions/src/`)

| Archivo | Tipo | Descripción |
|---|---|---|
| `core/auth/interfaces/http/enable2FAUserController.ts` | Nuevo | Genera secreto TOTP para usuario backoffice |
| `core/auth/interfaces/http/verify2FAUserController.ts` | Nuevo | Verifica código TOTP y marca verifiedAt |
| `core/auth/interfaces/http/get2FAUserStatusController.ts` | Nuevo | Consulta si 2FA está activo |
| `firebase-entry-http/auth/enable2FAUser.ts` | Nuevo | Entry-point HTTP con `validateToken` |
| `firebase-entry-http/auth/verify2FAUser.ts` | Nuevo | Entry-point HTTP con `validateToken` |
| `firebase-entry-http/auth/get2FAUserStatus.ts` | Nuevo | Entry-point HTTP con `validateToken` |
| `firebase-entry-http/index.ts` | Modificado | Exporta las 3 nuevas funciones |
| `lib/firebase/authentication/stateChange.ts` | Modificado | `onAuthStateChanged` → `onIdTokenChanged` |

### Frontend (`encodebiz-front-saas/src/`)

| Archivo | Tipo | Descripción |
|---|---|---|
| `services/core/account.service.ts` | Modificado | +`get2FAUserStatus`, `enable2FAUser`, `verify2FAUserCode` |
| `app/auth/login/page.controller.tsx` | Modificado | Intercepta login para comprobar 2FA |
| `app/auth/2fa/page.tsx` | Nuevo | Página de verificación TOTP en login |
| `app/auth/2fa/page.controller.tsx` | Nuevo | Lógica de la página 2FA |
| `app/main/user/account/page.controller.tsx` | Modificado | +Tab "Seguridad (2FA)" para activar/desactivar |
| `contexts/authContext.tsx` | Modificado | Refs estables, `setPendAuth(false)` en catch, deps mínimas |
| `lib/http/httpClientFetchNext.ts` | Modificado | `await logout()` antes de hard redirect |
| `config/errorLocales.ts` | Modificado | +Códigos de error `twofactor/internal`, `twofactor/user_not_activated` |
| `locales/{es,en,fr,de}/common.json` | Modificado | +Traducciones 2FA (labels, tab seguridad, mensajes) |
| `.env.development` | Modificado | +3 variables de entorno para 2FA de usuario |

---

## 11. Comandos de deploy

```bash
# 1. Funciones de 2FA de usuario (backoffice)
npm run deploy:function:dev -- apiV100-firebaseEntryHttp-enable2FAUser
npm run deploy:function:dev -- apiV100-firebaseEntryHttp-verify2FAUser
npm run deploy:function:dev -- apiV100-firebaseEntryHttp-get2FAUserStatus

# 2. Funciones con cambios previos de bugs QA
npm run deploy:function:dev -- apiV100-firebaseEntryHttp-checkinbiz-tasksHandler
npm run deploy:function:dev -- apiV100-firestoreTrigger-checkinbiz-onCreateIssues

# 3. Índices Firestore (corrección bug issues)
firebase deploy --only firestore:indexes --project dev-encodebiz

# 4. Frontend
npm run build && npm run deploy  # según pipeline del proyecto
```

---

## 12. Diferencias: 2FA usuario (backoffice) vs. 2FA empleado (app móvil)

| Característica | Usuario Backoffice | Empleado App Móvil |
|---|---|---|
| Autenticación | Firebase ID Token | JWT sessionToken (`validateTokenJWT`) |
| Almacenamiento | `users/{uid}/security/twoFA` | `entities/{eId}/employees/{empId}/security/twoFA` |
| Repositorio | Firestore Admin directo | `FirestoreEmployeeRepository.updateSecurity()` |
| Bypass de dev | No | Sí (`"042691"` en `Verify2FAAndIssueToken`) |
| Vinculado a dispositivo | No | Sí (guarda `deviceId` en `trustedDevicesId`) |
| Activación | Desde tab "Seguridad" en account | Desde configuración del empleado en backoffice |
| Verificación en login | `get2FAUserStatus` → `/auth/2fa` | `validateEmployee` → pantalla 2FA en app |

---

## 13. Consideraciones de seguridad

- El secreto TOTP **nunca se expone al frontend** una vez verificado; solo se devuelve en la respuesta de `enable2FAUser` al momento de crearlo.
- La verificación tiene ventana de `window: 1` en speakeasy (permite ±30s de desviación de reloj).
- Un secreto generado pero no verificado (`verifiedAt: null`) **no activa** la 2FA. Protege contra activaciones parciales si el usuario abandona el flujo de setup.
- No hay mecanismo de bypass en 2FA de usuario (a diferencia del empleado). Usar recuperación de contraseña si se pierde acceso a la app TOTP.
- Las Firestore Rules deben proteger `users/{uid}/security/**` con `allow read, write: if request.auth.uid == uid`. Verificar en `firestore.rules`.

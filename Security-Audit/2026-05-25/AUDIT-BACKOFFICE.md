# Auditoría de Seguridad — Backoffice (encodebiz-front-saas)

**Fecha:** 2026-05-25  
**Ruta:** `PLATAFORMA/encodebiz-front-saas/`  
**Stack:** Next.js 14 App Router, React 19, TypeScript, Material UI v7, Firebase Auth

---

## BO-01 🔴 CRÍTICO — Private Key RSA de service account en `.env.development`

**Archivo:** `.env.development`

**Hallazgo:**  
El archivo `.env.development` contiene la private key RSA completa de un Firebase Admin SDK service account:

```
NEXT_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwcJgZVUDk5...
-----END PRIVATE KEY-----

NEXT_CLIENT_EMAIL=firebase-adminsdk-fbsvc@encodebiz-services.iam.gserviceaccount.com
NEXT_PRIVATE_KEY_ID=d2f8624cfd9afde6e0c20727794e755da85d89ab
NEXT_PROJECT_ID=encodebiz-services
```

Aunque `.gitignore` excluye `.env*` (excepto `.env.example`), este archivo existe en disco con una private key de 2048 bits en texto plano. Si este directorio es accesible desde el servidor Next.js o es incluido en algún build, la clave queda expuesta.

**Impacto:**  
El service account `firebase-adminsdk-fbsvc@encodebiz-services.iam.gserviceaccount.com` tiene privilegios de Admin SDK: acceso total a todos los proyectos Firebase de `encodebiz-services`. Un atacante puede impersonar cualquier usuario, leer/escribir Firestore sin restricciones, y manipular Firebase Auth.

**Remediación:**
1. Revocar inmediatamente el service account en Google Cloud Console.
2. Generar nueva service account con permisos mínimos (solo los necesarios para `verifyIdToken`).
3. Mover la clave a **Secret Manager** o a variables de entorno del entorno de hosting (Vercel, Cloud Run), nunca en archivo en disco.
4. Para `verifyIdToken` en Next.js API routes, considerar usar el SDK del cliente de Firebase Admin con Application Default Credentials (ADC) cuando se despliega en GCP.

---

## BO-02 🟠 ALTO — Sin `middleware.ts`: rutas protegidas sin validación server-side

**Hallazgo:**  
No existe `middleware.ts` ni `src/middleware.ts` en el proyecto. La protección de rutas privadas (`/main/*`, `/admin/*`) se realiza íntegramente en el cliente a través del componente `AdminLayout` con el hook `useAuth`:

```tsx
// AdminLayout.tsx
const { pendAuth, user } = useAuth();
// Si no hay user → redirige desde el cliente
```

Esto significa que el servidor Next.js renderiza (o intenta renderizar) las páginas protegidas antes de que el cliente verifique la sesión. En el período entre el SSR y la hidratación del cliente, el contenido de la ruta puede estar visible o accesible vía scraping del HTML renderizado.

**Impacto:**  
- Un crawler o bot puede acceder al HTML de rutas protegidas sin autenticación.
- En Server Components o Server Actions que lean datos sin verificar el token, los datos se sirven sin autorización.
- No hay protección real a nivel de edge/server — solo a nivel de UI.

**Remediación:**
```typescript
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const PUBLIC_PATHS = ['/auth', '/legal', '/api/auth'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isPublic = PUBLIC_PATHS.some((p) => pathname.startsWith(p));
  if (isPublic) return NextResponse.next();

  const sessionToken = request.cookies.get('session')?.value
    ?? request.headers.get('authorization')?.replace('Bearer ', '');

  if (!sessionToken) {
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

---

## BO-03 🟠 ALTO — Error message leak en API route `verify-token`

**Archivo:** `src/app/api/auth/verify-token/route.ts`

**Hallazgo:**
```typescript
} catch (error: any) {
  return NextResponse.json(
    { message: "Invalid token" + error?.message as string }, // ← leak
    { status: 401 }
  );
}
```

El mensaje de error interno del Firebase Admin SDK se concatena directamente en la respuesta al cliente. Esto puede exponer detalles de implementación, versiones de librerías, o información sobre la estructura interna del sistema de auth.

Adicionalmente, el tipo de `request` está anotado como `any` (`request: any`), eliminando la type-safety de Next.js.

**Remediación:**
```typescript
export async function POST(request: NextRequest) {
  const data = await request.json();
  const { token } = data;

  if (!token) {
    return NextResponse.json({ message: 'No token provided' }, { status: 401 });
  }

  try {
    const decodedToken = await verifyToken(token);
    return NextResponse.json({ user: decodedToken }, { status: 200 });
  } catch {
    // No exponer el error interno
    return NextResponse.json({ message: 'Invalid or expired token' }, { status: 401 });
  }
}
```

---

## BO-04 🟠 ALTO — Sin security headers HTTP

**Archivo:** `next.config.ts`

**Hallazgo:**  
El `next.config.ts` no define ningún security header. Las siguientes cabeceras de seguridad están ausentes:

| Header | Riesgo sin él |
|---|---|
| `Content-Security-Policy` | XSS, data injection |
| `X-Frame-Options` / `frame-ancestors` | Clickjacking |
| `X-Content-Type-Options: nosniff` | MIME sniffing |
| `Referrer-Policy` | Leakage de URLs internas |
| `Strict-Transport-Security` | Downgrade a HTTP |
| `Permissions-Policy` | Acceso a APIs del navegador no usadas |

**Remediación:**
```typescript
// next.config.ts
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' https://www.gstatic.com",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https://storage.googleapis.com https://firebasestorage.googleapis.com https://lh3.googleusercontent.com",
      "connect-src 'self' https://*.cloudfunctions.net https://*.firebaseio.com wss://*.firebaseio.com",
      "frame-ancestors 'none'",
    ].join('; '),
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()',
  },
];

const nextConfig: NextConfig = {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }];
  },
  // ...resto de config
};
```

---

## BO-05 🟡 MEDIO — `console.log` con datos sensibles en API proxy de 2FA

**Archivo:** `src/app/api/2fa/enable/route.ts`

**Hallazgo:**
```typescript
console.log('[proxy /api/2fa/enable] auth present:', !!authorization,
  '| starts Bearer:', authorization.startsWith('Bearer '),
  '| locale:', locale);

console.log('[proxy /api/2fa/enable] upstream status:', upstream.status,
  '| response:', JSON.stringify(data));  // ← response body en logs
```

En producción, Vercel/Cloud Run captura todos los `console.log`. El response body del upstream podría contener información sensible del usuario. Además, loggear la estructura del token de autorización (aunque sea su presencia) puede ayudar a un atacante a correlacionar requests.

**Remediación:**  
Eliminar los `console.log` de debug en producción. Si se necesita observabilidad, usar un logger estructurado que excluya datos sensibles y solo loguee en entornos no-producción:

```typescript
if (process.env.NEXT_PUBLIC_ENV !== 'prod') {
  logger.debug('[2fa/enable] upstream status:', upstream.status);
}
```

---

## BO-06 🟡 MEDIO — `remotePatterns` de imágenes incluye dominios de prueba

**Archivo:** `next.config.ts`

**Hallazgo:**
```typescript
remotePatterns: [
  { hostname: 'example.com' },    // ← dominio de test, nunca debería estar en prod
  { hostname: 'placehold.co' },   // ← servicio de placeholder externo
  // ...
]
```

`example.com` nunca debería estar en la allowlist de imágenes de producción. Un atacante podría usar la API de optimización de imágenes de Next.js (`/_next/image?url=https://example.com/...`) para hacer SSRF limitado o para cachear imágenes maliciosas a través del dominio de EncodeBiz.

**Remediación:**  
Eliminar `example.com` y `placehold.co` de la configuración de producción. Usar variables de entorno para controlar qué dominios se permiten según el entorno.

---

## Resumen Backoffice

| ID | Severidad | Descripción | Estado |
|---|---|---|---|
| BO-01 | 🔴 CRÍTICO | Private Key RSA en `.env.development` | ⚠️ Pendiente |
| BO-02 | 🟠 ALTO | Sin `middleware.ts`: rutas sin protección server-side | ⚠️ Pendiente |
| BO-03 | 🟠 ALTO | Error message leak en API route verify-token | ⚠️ Pendiente |
| BO-04 | 🟠 ALTO | Sin security headers HTTP (CSP, HSTS, X-Frame-Options) | ⚠️ Pendiente |
| BO-05 | 🟡 MEDIO | `console.log` con datos sensibles en 2FA proxy | ⚠️ Pendiente |
| BO-06 | 🟡 MEDIO | `remotePatterns` con dominios de test en producción | ⚠️ Pendiente |

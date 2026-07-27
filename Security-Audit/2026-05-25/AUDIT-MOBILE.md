# Auditoría de Seguridad — App Móvil (checkbiz360)

**Fecha:** 2026-05-25  
**Ruta:** `PLATAFORMA/checkbiz360/`  
**Stack:** Flutter 3.35.6, Riverpod 2, Dio 5, FlutterSecureStorage, Firebase Auth

---

## MB-01 🟠 ALTO — `sessionToken` almacenado en `SharedPreferences` (no encriptado)

**Archivos afectados:**
```
lib/features/auth/presentation/providers/auth_provider.dart:352
lib/features/auth/presentation/providers/auth_provider.dart:509
lib/features/auth/presentation/providers/auth_provider.dart:703
lib/features/attendance/data/repositories/attendance_repository_impl.dart:48
```

**Hallazgo:**  
El `sessionToken` (Bearer JWT del backend) se persiste usando `SharedPreferences`:
```dart
await _prefs.setString(AppConstants.accessTokenKey, firebaseToken); // SharedPreferences
await _prefs.setString(AppConstants.accessTokenKey, token);          // SharedPreferences
```

`SharedPreferences` en Android almacena datos en XML sin encriptar en `/data/data/<package>/shared_prefs/`. En dispositivos rooteados o con ADB habilitado, este token puede ser extraído trivialmente.

Por contraste, el proyecto ya usa `FlutterSecureStorage` correctamente para credenciales biométricas y contraseñas (ver MB-02), pero el token más sensible —el que autoriza todas las llamadas API— no está protegido de la misma forma.

**Impacto:**  
En un dispositivo rooteado o comprometido, un atacante puede extraer el `sessionToken` y hacer llamadas a todas las APIs del backend como si fuera el empleado: crear/modificar checklogs, ver documentos, aprobar tareas.

**Remediación:**
```dart
// Migrar accessToken a SecureStorage
// En SecureStorageService:
static const _accessTokenKey = 'access_token';

Future<void> saveAccessToken(String token) async {
  await _storage.write(key: _accessTokenKey, value: token);
}

Future<String?> getAccessToken() async {
  return _storage.read(key: _accessTokenKey);
}

Future<void> clearAccessToken() async {
  await _storage.delete(key: _accessTokenKey);
}
```

Reemplazar todas las llamadas a `_prefs.setString(AppConstants.accessTokenKey, ...)` por el servicio de SecureStorage.

---

## MB-02 🟡 MEDIO — Almacenamiento de contraseña en texto claro (aunque encriptado)

**Archivo:** `lib/core/storage/secure_storage_service.dart`

**Hallazgo:**  
El servicio almacena la contraseña del usuario en `FlutterSecureStorage`:
```dart
Future<void> saveCredentials(String email, String password) async {
  await _storage.write(key: _emailKey, value: email);
  await _storage.write(key: _passwordKey, value: password); // ← contraseña en plaintext
  await _storage.write(key: _rememberMeKey, value: 'true');
}
```

Aunque `FlutterSecureStorage` encripta el contenido (Keychain en iOS, EncryptedSharedPreferences en Android), guardar la contraseña es un anti-patrón de seguridad por varias razones:
1. Si el keychain/keystore es comprometido, la contraseña queda expuesta.
2. La contraseña puede ser usada para acceder a otros servicios si el usuario reutiliza contraseñas.
3. No hay necesidad: Firebase Auth y el sessionToken son suficientes para reconectar sesiones.

La configuración es correcta:
```dart
aOptions: AndroidOptions(encryptedSharedPreferences: true),
iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock_this_device),
```

**Remediación:**  
Cambiar la estrategia de "remember me": en lugar de guardar la contraseña, guardar solo el email (para pre-rellenar el campo) y confiar en Firebase Auth persistence (`authStateChanges()`) para mantener la sesión. Para biometría, el flow debe ser: biometría exitosa → solicitar Firebase ID token refresh → llamar `/auth/login` nuevamente si es necesario.

```dart
// Reemplazar saveCredentials con:
Future<void> saveEmailForRememberMe(String email) async {
  await _storage.write(key: _emailKey, value: email);
  await _storage.write(key: _rememberMeKey, value: 'true');
  // NO guardar password
}
```

---

## MB-03 🟡 MEDIO — Sin SSL Certificate Pinning

**Archivo:** `lib/core/network/dio_client.dart`

**Hallazgo:**  
El cliente Dio no implementa SSL pinning. La app confía en cualquier certificado válido emitido por una CA de confianza del sistema. En redes corporativas o con proxies SSL interceptors (Burp Suite, Charles Proxy), el tráfico puede ser descifrado sin que la app lo detecte.

No se encontró uso de `SecurityContext`, `HttpClient.badCertificateCallback`, ni librerías de pinning como `http_certificate_pinning`.

**Contexto de riesgo:**  
Dado que la app maneja datos sensibles de asistencia y geolocalización de empleados, y que los usuarios pueden estar en redes corporativas con inspección SSL, el riesgo es moderado.

**Remediación:**
```dart
// Opción 1: Public Key Pinning via dio_http2_adapter o custom HttpClient
import 'dart:io';

HttpClient buildPinnedHttpClient() {
  final securityContext = SecurityContext(withTrustedRoots: false);
  // Añadir solo la CA de Cloud Run / Firebase
  securityContext.setTrustedCertificatesBytes(googleRootCaPem);
  
  final client = HttpClient(context: securityContext);
  client.badCertificateCallback = (cert, host, port) => false;
  return client;
}

// Opción 2 (más pragmática): verificar fingerprints de certificado
// Librería: flutter_ssl_pinning o implementación manual
```

Para production builds, como mínimo activar el flag `android:networkSecurityConfig` en Android con una configuración que restrinja las CAs permitidas.

---

## MB-04 🟡 MEDIO — `LogInterceptor` expone headers y body en modo debug

**Archivo:** `lib/core/network/dio_client.dart`

**Hallazgo:**
```dart
instance.interceptors.add(
  LogInterceptor(
    requestBody: AppConfig.debugMode,    // kDebugMode
    responseBody: AppConfig.debugMode,
    requestHeader: AppConfig.debugMode,  // ← loguea Authorization header
    responseHeader: AppConfig.debugMode,
  ),
);
```

En builds de desarrollo (`--debug` o `flutter run` sin `--release`), todos los headers incluyendo `Authorization: Bearer <token>` y los bodies completos de las respuestas son impresos en los logs de Flutter. En un dispositivo conectado a Android Studio o con ADB, estos logs son accesibles.

**AppConfig:**  
```dart
static bool get debugMode => kDebugMode; // false en --release, true en --debug y --profile
```

El comportamiento en **release builds** es correcto (no loguea). El riesgo existe en desarrollo si el dispositivo físico del desarrollador tiene datos reales de producción.

**Remediación:**  
Asegurarse de que los flavors de desarrollo (`main_development.dart`) apunten exclusivamente al entorno `dev-encodebiz` y nunca al entorno de producción. Documentar esta restricción en `AGENTS.md`.

---

## MB-05 🟢 BAJO — Permisos de ubicación en Android: `ACCESS_FINE_LOCATION` siempre activo

**Archivo:** `android/app/src/main/AndroidManifest.xml`

**Hallazgo:**
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

La app solicita ubicación precisa (`FINE_LOCATION`) que tiene un mayor costo de privacidad para el empleado que la ubicación aproximada (`COARSE_LOCATION`). Si el caso de uso de geolocalización (validación de checkin en sucursal) solo requiere verificar que el empleado está dentro de un radio de X metros, `COARSE_LOCATION` podría ser suficiente en muchos casos.

No se observa el permiso `ACCESS_BACKGROUND_LOCATION`, lo cual es correcto — la app no trackea ubicación en background.

**Remediación:**  
Evaluar si para la funcionalidad de checkin se puede usar `COARSE_LOCATION` en combinación con el GPS de la sucursal. Documentar el razonamiento de por qué se requiere `FINE_LOCATION` (si aplica) en el `AGENTS.md`.

---

## MB-06 🟢 BAJO — Sin protección de screenshots en pantallas sensibles

**Hallazgo:**  
No se encontró uso de `FLAG_SECURE` (Android) o `preventScreenCapture` (iOS) en pantallas sensibles como el resumen de asistencia, documentos del empleado, o la configuración de seguridad 2FA/biométrica.

**Remediación:**
```dart
// En pantallas con datos sensibles:
import 'package:flutter_windowmanager/flutter_windowmanager.dart';

@override
void initState() {
  super.initState();
  FlutterWindowManager.addFlags(FlutterWindowManager.FLAG_SECURE);
}

@override
void dispose() {
  FlutterWindowManager.clearFlags(FlutterWindowManager.FLAG_SECURE);
  super.dispose();
}
```

---

## Aspectos positivos observados

Los siguientes puntos de seguridad están correctamente implementados y deben mantenerse:

- ✅ `FlutterSecureStorage` con `encryptedSharedPreferences: true` en Android y `KeychainAccessibility.first_unlock_this_device` en iOS para credenciales biométricas.
- ✅ `AuthRetryInterceptor` con lógica correcta de token refresh: Firebase ID token refresh → retry → session refresh completo → logout. Sin bucle infinito (flag `_authRetryExtraKey`).
- ✅ `LogInterceptor` controlado por `kDebugMode` — no loguea en release builds.
- ✅ `AppConfig` usa `String.fromEnvironment('ENVIRONMENT')` con `dart-define` — sin secretos hardcodeados en el código fuente.
- ✅ Biometric auth con device binding key — evita que la biometría de un dispositivo sea válida en otro.
- ✅ Permisos de biometría correctamente declarados (`USE_BIOMETRIC`, `NSFaceIDUsageDescription`).
- ✅ Sin `ACCESS_BACKGROUND_LOCATION` — no trackea ubicación continua.

---

## Resumen App Móvil

| ID | Severidad | Descripción | Estado |
|---|---|---|---|
| MB-01 | 🟠 ALTO | `sessionToken` en `SharedPreferences` sin encriptar | ⚠️ Pendiente |
| MB-02 | 🟡 MEDIO | Contraseña almacenada en SecureStorage (anti-patrón) | ⚠️ Pendiente |
| MB-03 | 🟡 MEDIO | Sin SSL certificate pinning | ⚠️ Pendiente |
| MB-04 | 🟡 MEDIO | `LogInterceptor` expone headers en debug builds | 🟡 Mitigado en release |
| MB-05 | 🟢 BAJO | `ACCESS_FINE_LOCATION` sin justificación documentada | ⚠️ Pendiente |
| MB-06 | 🟢 BAJO | Sin FLAG_SECURE en pantallas sensibles | ⚠️ Pendiente |

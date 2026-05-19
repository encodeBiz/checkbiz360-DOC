# Capa App Móvil — CheckBiz360

## 1. Stack

| Componente | Tecnología |
|---|---|
| Framework | Flutter 3.35.6 (FVM) |
| Dart SDK | `^3.5.3` |
| State | Riverpod 2.x |
| Modelos | Freezed + json_serializable |
| Router | GoRouter con `StatefulShellRoute.indexedStack` |
| HTTP | Dio + interceptores |
| DB local | Hive (cache offline) |
| Push | Firebase Messaging |
| Auth | Firebase Auth + sessionToken Bearer |
| GPS | geolocator + connectivity_plus |
| Geo package | `packages/base_location` (paquete interno) |
| Firebase | Auth, Firestore, Messaging, Crashlytics, Storage |
| Design System | `lib/presentation/design_system` |

## 2. Entrypoints

```
lib/main_development.dart    → flavor development
lib/main_production.dart     → flavor production
```

## 3. Arquitectura

La app está migrando a **feature-first**. Las features nuevas siguen esta estructura:

```
lib/features/{feature}/
  domain/          → entidades, repositorios abstractos, reglas puras
  data/            → modelos, datasources, repositorios concretos
  application/     → use cases / orquestación
  presentation/    → pages, providers, widgets
```

Features en migración:
```
lib/features/auth
lib/features/attendance
lib/features/notifications
lib/features/support
lib/features/task
```

Capas legacy compartidas (aún activas):
```
lib/application
lib/core
lib/data
lib/domain
lib/infrastructure
lib/presentation
lib/shared
```

### Reglas de capas

- `domain` no importa Flutter, Firebase, Dio ni modelos de `data`
- `presentation` no importa datasources concretos
- `data` implementa contratos de `domain`
- Acceso a Firebase/Dio desde widgets está prohibido

## 4. DI — Inyección de Dependencias

Punto principal: `lib/core/di/injection_container.dart`

Dependencias que se override desde `main`:
- `sharedPreferencesProvider`
- `dioClientProvider`
- `firebaseCrashlyticsServiceProvider`

Providers de Task:
- `taskFirestoreDataSourceProvider`
- `taskLookupDataSourceProvider`
- `taskRemoteDataSourceProvider`
- `taskRepositoryProvider`

No redefinir providers de datasources/servicios en features si ya existen en DI central.

## 5. Estado y Lifecycle

- Riverpod es el patrón principal. No introducir `Provider`/`ChangeNotifier` nuevos
- `autoDispose` para providers con datos de usuario o pantalla
- `ref.watch(...select(...))` cuando solo se necesita un campo
- Cancelar `StreamSubscription`, `Timer`, controllers, `FocusNode`, `ScrollController`, `AnimationController`
- `if (!mounted) return` antes de navegar, mostrar dialogs o usar `context` en async
- No `print` — usar `debugPrint` o logger

### Logout

`lib/features/notifications/presentation/providers/logout_invalidation_provider.dart` invalida providers user-scoped. Si agregas providers con datos de usuario, actualiza este provider.

Actualmente invalida: attendance, responsibility, schedule, notifications, support history, attendance history, task list, task detail.

## 6. Navegación

Router: `lib/presentation/router/app_router.dart`

Bottom nav dentro de `AttendanceShellPage`:
- Índice 0: Tareas (`/attendance/tasks`)
- Índice 1: Asistencia (`/attendance/control`)
- Índice 2: Contacto (`/attendance/support`)

Historial en `/attendance/history` (drawer, no tab principal).

| Constante | Path |
|---|---|
| `taskRoute` | `/attendance/tasks` |
| `taskCreateRoute` | `/attendance/tasks/new` |
| `taskDetailRoute` | `/attendance/tasks/:taskId` |
| `attendanceHistoryRoute` | `/attendance/history` |

## 7. Design System y UI

- Tokens, theme y extensiones: `lib/presentation/design_system`
- Widgets comunes: `lib/presentation/widgets/common`
- `HeaderTitle` para títulos de `AppBar` (centra + sentence case)
- `AppBarTheme.centerTitle = true` en `AppTheme`
- Labels bottom nav: `TextUtils.toHeaderTitle`
- Loading: reutilizar `LoadingPlaceholder` (logo animado) antes de introducir `CircularProgressIndicator`

### i18n

- No introducir strings visibles sin l10n
- Si cambias ARB: `fvm flutter gen-l10n`
- Archivos generados `app_localizations*.dart` no se editan manualmente

## 8. Comandos

```bash
fvm flutter pub get
fvm flutter analyze
fvm flutter test
fvm dart run build_runner build --delete-conflicting-outputs
fvm flutter gen-l10n
fvm flutter run --flavor development -t lib/main_development.dart --dart-define=ENVIRONMENT=development
fvm flutter run --flavor production -t lib/main_production.dart --dart-define=ENVIRONMENT=production
```

`fvm flutter analyze` puede modificar `pubspec.lock` — revisar diff antes de commitear.

## 9. Lectura vs Escritura

- **Lecturas operativas**: Firestore SDK directo (`onSnapshot`) para datos en tiempo real
- **Lecturas paginadas/agregadas**: HTTP GET a Cloud Functions
- **Escrituras (mutaciones)**: siempre via HTTP a Cloud Functions — nunca directo a Firestore desde cliente

## 10. Zonas Sensibles

Cambios en estas áreas requieren revisión de lifecycle completo:

- `AuthNotifier` — grande y crítico
- `AttendancePage` — bastante orquestación
- `FirebaseMessagingService` — singleton con streams
- Auth, attendance, notifications, logout

## 11. ADRs Implementados

### ADR-001 — Modal de recuperación de calendario (no día libre silencioso)

**Problema:** `scheduleAsync.valueOrNull` devuelve `null` tanto en `AsyncLoading` como en `AsyncError`. Al fallar la API de calendarios, `isDayOffToday = true` → botones de fichaje desaparecen silenciosamente. El empleado asume que no tiene turno cuando en realidad hay un error de red.

**Decisión:** Separar los tres estados explícitamente en la UI de `AttendancePage`:
- `AsyncLoading` → skeleton/spinner
- `AsyncError` → modal de error con retry
- `AsyncData(null)` → día libre real

**Archivos:** `lib/features/attendance/presentation/pages/attendance_page.dart`, `lib/features/attendance/presentation/providers/schedule_provider.dart`

---

### ADR-002 — FCM desacoplado del flujo de autenticación

**Problema:** `FirebaseMessagingService.initialize()` se llamaba con `await` antes de setear `isAuthenticated: true`. Si cualquier paso (registro FCM, obtención de token, `addDeviceToken`, suscripción a topics) se colgaba, el splash quedaba congelado indefinidamente.

**Decisión:** Ejecutar `initialize()` sin `await` (fire-and-forget) y setear `isAuthenticated: true` inmediatamente. FCM se inicializa en paralelo.

**Archivo:** `lib/features/auth/presentation/providers/auth_provider.dart`

---

### ADR-003 — Timeout de 30 segundos en `initializeAuthFlow`

**Problema:** `SplashPage._initializeApp()` esperaba sin límite de tiempo. Las llamadas Firestore no tienen timeout local. En red muy degradada, la app podía quedar indefinidamente en splash.

**Decisión:**
```dart
final status = await validationFuture.timeout(
  Duration(seconds: 30),
  onTimeout: () => AuthFlowStatus.validationFailed,
);
```

**Archivo:** `lib/presentation/pages/splash_page.dart`

---

### ADR-004 — GPS smart cache: ventana diferenciada 60s directo / 5min fallback

**Problema:** `registerAttendance()` forzaba siempre GPS fresco (`forceFresh: true`). En interiores, la adquisición podía tardar hasta 12s o fallar aunque hubiera una posición precisa de hace 45 segundos.

**Decisión:** Evaluación inteligente antes de forzar GPS fresco:

```dart
const _kGpsGoodAccuracyMeters       = 50.0;
const _kGpsAcceptableAccuracyMeters = 100.0;
const _kGpsDirectCacheValidity      = Duration(seconds: 60);
```

- Cache < 60s y precisión ≤ 50m → usar directo
- Cache < 60s y precisión ≤ 100m → usar con flag de auditoría
- En otro caso → pedir GPS fresco

**Archivo:** `lib/features/attendance/presentation/providers/attendance_provider.dart`

---

### ADR-005 — Conectividad real: `connectivity_plus` + healthcheck propio

**Problema:** La app no verificaba conectividad antes de operaciones de red. El error llegaba tras el timeout de Dio (~30s). `NetworkInfo` existía como esqueleto vacío sin implementación.

**Decisión:** `ConnectivityService` con dos capas:
1. `connectivity_plus` como señal rápida (detecta si hay interfaz activa)
2. `GET /health` al propio endpoint de Cloud Functions para verificar routing real

`connectivity_plus` solo detecta interfaz de red activa — no si Cloud Functions/Firebase es alcanzable.

**Estado:** Parcialmente implementado (pendiente: check en `SplashPage`).

---

### ADR-006 — Firebase In-App Messaging

Estado: implementado. Ver `DOCUMENTACION/recuperacion/12-adr-006-firebase-in-app-messaging.md` en historial git si se necesita el detalle completo.

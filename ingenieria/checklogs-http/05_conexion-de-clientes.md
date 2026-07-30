# 05 — Conexión de clientes

Qué tocar exactamente en cada cliente para que deje de llamar a Firebase y llame al servidor. Nada de esto cambia el cuerpo de las peticiones ni el manejo de errores: el contrato es el mismo ([03](./03_contratos-api.md)).

Base: `https://api.checkbiz360.com/api/v1/checkinbiz/checklogs`

| Operación | Endpoint nuevo | Cloud Function que sustituye |
|---|---|---|
| Crear fichaje | `POST /api/v1/checkinbiz/checklogs` | `…checkinbiz-createChecklog` |
| Corregir fichaje | `POST /api/v1/checkinbiz/checklogs/update` | `…checkinbiz-updateChecklog` |
| Jornada manual | `POST /api/v1/checkinbiz/checklogs/manual-request` | `…checkinbiz-requestManualChecklog` |

---

## 1. Back office (`encodebiz-front-saas`)

Sin cambios de código: `src/lib/http/serverBackendProxy.ts` ya resuelve el destino desde variable de entorno. Solo cambian los valores, en `.env` y en `.env.production`:

```diff
-NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_LOG=https://apiv100-firebaseentryhttp-checkinbiz-updatecheckl-jxvyznhhja-uc.a.run.app
+NEXT_BACKEND_URI_CHECKINBIZ_UPDATE_LOG=https://api.checkbiz360.com/api/v1/checkinbiz/checklogs/update

-NEXT_BACKEND_URI_CHECKINBIZ_REQUEST_MANUAL_CHECKLOG=https://us-central1-encodebiz-services.cloudfunctions.net/apiV100-firebaseEntryHttp-checkinbiz-requestManualChecklog
+NEXT_BACKEND_URI_CHECKINBIZ_REQUEST_MANUAL_CHECKLOG=https://api.checkbiz360.com/api/v1/checkinbiz/checklogs/manual-request
```

### Por qué `CREATE_LOG` no entra aquí

Una versión anterior de este documento decía que `NEXT_BACKEND_URI_CHECKINBIZ_CREATE_LOG` estaba en la allowlist pero que ningún componente del front lo llamaba. **Es falso**: `createLog` tiene dos consumidores vivos, y ejercitan los dos modos de auth de [ADR-004](./adr/ADR-004-auth-por-ruta-no-global.md).

| Consumidor | Token que manda | Rama de auth |
|---|---|---|
| `src/app/tools/checking/page.context.tsx` — kiosco QR | sesión de empleado | `validateTokenJWT` |
| `…/attendance/AttendanceFormModal.controller.tsx` — alta del back office | ID token de Firebase, con `isAdmin: true` | `validateToken` |

La conclusión de dejarlo en Firebase se mantiene, pero por otro motivo: **una sola variable sirve a los dos consumidores y no se pueden separar sin tocar código**. Moverla arrastraría al kiosco, que es un empleado fichando en tiempo real y con prisa — exactamente el tráfico que este plan quiere mover el último. `CREATE_LOG` va con la Fase 3, junto a la app, no en el cutover del back office.

Y conviene saberlo antes de la Fase 3: el kiosco ya maneja `checklog/out_of_radius` y `auth/untrusted_device`, así que **la huella de dispositivo de confianza también se ejercita desde el front**, no solo desde la app. Con una diferencia a favor: las llamadas del front salen del proxy de Next, así que el `user-agent` que ve el backend siempre ha sido el del servidor de Next, no el del navegador. El proxy no cambia en ningún momento del cutover, así que la huella tampoco.

### Lo que no cambia

Las rutas siguen pasando por `/api/proxy/**`. **Eso no es un detalle de implementación:** el guard de sesión 2FA vive en el Edge (`src/proxy.ts`) y está montado sobre esa ruta — sin cookie devuelve `401 auth/2fa_required` y caducada `401 auth/2fa_expired`, que es lo que hace saltar el modal de re-verificación. La cookie la emite el propio front en su origen, `HttpOnly` y `SameSite=Lax`: no viaja a otro dominio y JS no puede adjuntarla. Llamar directo desde el navegador a `api.checkbiz360.com` dejaría estas rutas fuera del guard, protegidas solo por el ID token de Firebase. El cutover cambia **el destino del proxy, nunca el hecho de que haya proxy**.

Si el despliegue del front usa variables de Vercel en vez del fichero, hay que cambiarlas también ahí — el `.env` del repo no las pisa. De hecho `.env*` está en el `.gitignore`, así que este cutover **no deja rastro en el repo del front**: no hay commit que revisar, y el cambio real es el de las variables del entorno de despliegue.

**Rollback:** devolver los valores anteriores y redesplegar. Efecto inmediato.

---

## 2. App móvil (`checkbiz360`, Flutter)

En `lib/core/constants/app_constants.dart`, las dos constantes de fichaje pasan a apuntar al servidor. Hoy dependen de `AppConfig.isDevelopment` porque las URLs de Cloud Functions difieren entre dev y prod; con el servidor el host es el mismo, así que la bifurcación desaparece:

```diff
-  static String get createChecklogEndpoint => AppConfig.isDevelopment
-      ? 'https://apiv100-firebaseentryhttp-checkinbiz-createcheckl-3bnjgtprva-uc.a.run.app'
-      : '$attendanceEndpoint-createChecklog';
-  static String get updateChecklogEndpoint => AppConfig.isDevelopment
-      ? 'https://apiv100-firebaseentryhttp-checkinbiz-updatecheckl-3bnjgtprva-uc.a.run.app'
-      : '$attendanceEndpoint-updateChecklog';
+  static const String _apiBase = 'https://api.checkbiz360.com/api/v1/checkinbiz';
+
+  static String get createChecklogEndpoint => '$_apiBase/checklogs';
+  static String get updateChecklogEndpoint => '$_apiBase/checklogs/update';
```

Es el mismo host que ya usa `_criticalHandlerBase` a través del proxy de arranque, así que no hay dominio nuevo que permitir.

**Lo que NO cambia** — y conviene decirlo porque es donde se rompería sin darse cuenta:

- **Los tokens siguen siendo dos.** `createLog` manda el `sessionToken` (JWT de empleado, `authState.sessionToken`); `updateChecklog` manda el `access_token` (ID token de Firebase). El servidor verifica exactamente los mismos.
- **El `user-agent`.** El servidor deriva la huella del dispositivo de esa cabecera (`base64(user-agent)`) y la compara con `trustedDevicesId`. Si el cliente HTTP la cambia al cambiar de URL, todos los fichajes de dispositivos con 2FA fallarán con `auth/untrusted_device`. Hay que verificarlo con un dispositivo real antes de publicar.
- **El cuerpo y los códigos de error.** Idénticos; `ErrorParser` no se toca.

**Rollback:** no lo hay rápido — la versión publicada ya apunta al servidor. Por eso la app va después del back office y solo cuando el servidor lleve tiempo sirviendo tráfico real sin incidencias.

---

## 3. Servidor

Nada que aprovisionar:

- **nginx** ya enruta `location /api/v1/checkinbiz/` → `checkinbiz:3002`, así que las rutas de checklogs quedan expuestas sin tocar la configuración.
- **`JWT_2FA_SECRET`** ya está en `/opt/encodebiz-api/.env.production` — es el mismo con el que `/auth/validate`, ya en producción, firma el `sessionToken`. Conviene confirmarlo antes del cutover de la app: si no coincidiera con el de Firebase, el fichaje devolvería `auth/unauthorized` en vez de un error de negocio.

---

## 4. Orden y verificación

1. **Back office primero.** Menor volumen y con un humano delante capaz de reportar el mismo día. Verificar una corrección de fichaje completa (administrador propone → el empleado recibe la push → confirma) y una jornada manual en sus dos modos.
2. **Observar** latencia y errores durante el periodo que se acuerde, y confirmar en Firestore los cuatro casos frágiles de [03 §4](./03_contratos-api.md).
3. **App después**, con release en stores.
4. **Retirar** los handlers de Firebase cuando la penetración de versiones lo permita. Fijar el umbral ahora, o la retirada se aplaza sola.

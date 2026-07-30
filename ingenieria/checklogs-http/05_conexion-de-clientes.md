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

`NEXT_BACKEND_URI_CHECKINBIZ_CREATE_LOG` está en la allowlist del proxy pero **ningún componente del front lo llama**. Se deja apuntando a Firebase hasta confirmar que está muerto; retirarlo es una decisión aparte.

Si el despliegue del front usa variables de Vercel en vez del fichero, hay que cambiarlas también ahí — el `.env` del repo no las pisa.

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

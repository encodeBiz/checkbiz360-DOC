# ADR-002 — Los clientes apuntan directo a la API; sin capa de proxy

**Estado:** Aceptado
**Fecha:** 2026-07-30
**Contexto:** checklogs-http

---

## Contexto

El arranque de la app (login, validate, calendario) se migró conservando la Cloud Function `criticalHandler` y vaciándola hasta dejarla como proxy hacia el servidor. Eso permitió mover el tráfico sin publicar versión en las stores.

Se valoró repetir el patrón para el fichaje: convertir `createChecklog` y `updateChecklog` en proxies con el mismo nombre y la misma URL. Se descarta.

## Decisión

Ningún proxy **de Firebase** nuevo. Los tres endpoints de checklogs se consumen sin intermediario en Cloud Functions, contra `https://api.checkbiz360.com/api/v1/checkinbiz/checklogs…`:

- **Back office** — cambia el valor de sus variables de entorno. Sin cambio de código.
- **App móvil** — cambia las URLs en `AppConstants` y se publica versión.

Las Cloud Functions originales se quedan como están, sirviendo a las versiones de app que aún no se hayan actualizado, hasta que la penetración permita retirarlas.

### "Sin proxy" NO incluye el proxy de Next del back office

Conviene decirlo explícitamente porque el título de este ADR se presta a lo contrario. Lo que se descarta es **interponer una Cloud Function** entre el cliente y el servidor. El back office sigue llamando a través de `/api/proxy/**` (`src/lib/http/serverBackendProxy.ts`) y eso no se toca en ninguna fase: ahí es donde el Edge (`src/proxy.ts`) aplica el guard de sesión 2FA, valida el ID token antes de reenviar y mantiene la allowlist de destinos.

La cookie de sesión 2FA la emite el propio front en su origen, `HttpOnly` y `SameSite=Lax`: no viaja a otro dominio y JS no puede adjuntarla. Si el navegador llamara directo a `api.checkbiz360.com`, esas rutas quedarían fuera del guard y protegidas solo por el ID token de Firebase — que dura una hora y se renueva solo. El cutover cambia **el destino del proxy, nunca el hecho de que haya proxy**.

La app móvil sí va directa: no tiene proxy de Next delante, y su 2FA es otra cosa (el `sessionToken` firmado con `JWT_2FA_SECRET`, que viaja en la propia petición).

## Justificación

Un proxy resuelve el cutover sin release, pero deja el sistema con dos capas para siempre: la app sigue pagando la invocación y el cold start de Cloud Functions antes de tocar el servidor, y el recorrido pasa a ser app → Firebase → nginx → contenedor. Justo la latencia que motivó la migración se recupera a medias.

`criticalHandler` lo justificaba porque era el arranque: tres llamadas encadenadas en la pantalla de entrada, donde el cold start se notaba de forma inmediata y la ganancia era grande. Para el fichaje, el camino limpio es el directo: una sola llamada, y el cliente ya sabe hablar con `api.checkbiz360.com` porque es a donde va el calendario.

Menos piezas desplegadas, un solo sitio donde mirar cuando algo falla, y ningún codebase intermedio que mantener sincronizado con el contrato.

## Consecuencias

**A favor**

- Recorrido directo: la app pega al servidor sin salto intermedio.
- Nada nuevo que desplegar ni mantener en Firebase.
- El contrato tiene un solo dueño: el servicio.

**En contra**

- El cutover de la app depende del ciclo de publicación en las stores y del ritmo de actualización de los usuarios.
- Durante ese periodo conviven dos implementaciones del fichaje —la de Firebase para versiones antiguas y la del servidor para las nuevas— sobre la misma Firestore. Los triggers no distinguen quién escribió, así que el dato es coherente; lo que hay que asumir es que un cambio de lógica en ese periodo debe aplicarse en los dos sitios o esperar.
- Los handlers de Firebase no se pueden retirar hasta que la penetración de versiones lo permita. Conviene fijar el umbral y medirlo, o la retirada se aplaza sola.

**Rollback**

Del lado del back office, devolver las variables de entorno. Del lado de la app, no hay rollback rápido: la versión ya publicada apunta al servidor. Por eso el orden importa — el back office primero, y la app solo cuando el servidor lleve tiempo sirviendo tráfico real sin incidencias.

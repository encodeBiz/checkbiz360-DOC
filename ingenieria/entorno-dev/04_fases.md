# 04 — Fases

Cada fase es **independiente y reversible**. Solo una toca producción (la Fase 2), y lo hace con un
cambio aditivo de un bloque.

---

## Fase 0: Estabilizar el repositorio

**Estado:** ✅ Completada — 2026-08-18.

**Objetivo:** que la rama de trabajo salga de un `main` que de verdad refleje lo desplegado.

Al empezar, `main` iba 6 commits por detrás de `develop` y la PR #46 llevaba 12 días abierta.
Ramificar de ahí habría arrastrado el atraso al entorno nuevo.

- Verificados en el servidor los dos prerrequisitos manuales de la #46: `TURNSTILE_SECRET_KEY`
  presente en `.env.production` y tabla `rentman_time_registration` creada. Ya estaban hechos.
- Mergeada la #46. `Production CI/CD` verde en 1m09s; los 9 servicios sanos; el cron de horas de
  Rentman arranca sin errores.
- `.claude/settings.json` desversionado e ignorado: guardaba permisos con rutas absolutas de una
  máquina concreta, así que describía un puesto de trabajo, no el proyecto.
- Cerrada la PR #13: su commit ya estaba en `develop` como `f46c289`, y la rama arrastraba ~17.500
  líneas de atraso —era de antes de sales, rentman y documents—.
- 12 ramas locales ya integradas, borradas.
- `main`, `develop` y `staging` alineadas en `aa9e008`. Creada `feat/entorno-dev`.

**Pendiente menor:** barrer 5 ramas remotas ya integradas (`feat/addon-rentman`,
`feat/panel-analisis-cruce-de-ejes`, `feat/rentman-service`, `feat/sales-turnstile`, `qa/migrations`).

---

## Fase 1: El stack de desarrollo en pie

**Estado:** ✅ Completada — 2026-08-18. Commits `5acccb0` y `e56102b` en `staging`.

**Objetivo:** los 9 servicios y su Postgres corriendo en el servidor, sin poder tocar producción.

En el repo: `docker-compose.staging.yml`, `nginx/nginx.staging.conf`, `.env.staging.example`.
En el servidor: `/opt/encodebiz-api-dev` siguiendo `staging`, con su `.env.staging` y la service
account de `dev-encodebiz`.

**Verificado, no supuesto:**

- Los 9 servicios responden `{"ok":true}` y los 11 contenedores están `healthy`.
- El Postgres nuevo levantó **15 tablas desde cero**. Es la primera vez que la cadena de las 9
  migraciones corre entera: en producción `initdb` no vuelve a ejecutarse desde el primer día.
- Los 9 prefijos de la API devuelven, por el 8080, **exactamente los mismos códigos que producción**
  por el 443 (404/401/404/400/400/401/401/401/401). La paridad de rutas es real, no declarada.
- Producción no se enteró: sus contenedores conservan el uptime del release anterior, ninguno se
  reinició, y sus 9 prefijos siguen devolviendo lo mismo que antes de empezar.
- Aislamiento comprobado contra el compose de producción: proyecto, puertos publicados y dato en
  disco distintos en los tres ejes. Redes separadas (`encodebiz-api_default` y `encodebiz-dev`).
- Consumo del stack completo: **309 MiB**, cada servicio muy por debajo de su tope de 512 MiB.

**Lo que enseñó la fase:** al recrear los contenedores, 8 de las 9 rutas devolvieron 502 hasta
reiniciar nginx. Es el mismo motivo por el que el workflow de producción lo reinicia, y confirma que
el de desarrollo tendrá que hacerlo igual — anotado en la Fase 3.

**Pendiente menor:** `FIREBASE_WEB_API_KEY` quedó vacía. Solo la usa la herramienta que acuña tokens
de prueba; ningún servicio la necesita para arrancar.

**Rollback:** `docker compose -p encodebiz-api-dev down`. Producción no se tocó en toda la fase.

---

## Fase 2: El borde — resuelta dentro de la Fase 1

**Estado:** ✅ Absorbida por la Fase 1.

El plan original añadía un `server` block al nginx de producción para servir un dominio de desarrollo
con TLS. Se descartó a mitad de la Fase 1 por decisión de producto: **desarrollo levanta su propio
nginx en el 8080** y producción no se toca en ninguna fase.

Lo que se gana: ya no hay ninguna fase que abra el fichero de configuración de producción, y
desaparece la trampa del `resolver` con variable en el `proxy_pass`.

Lo que cuesta: no hay TLS. El tráfico hacia desarrollo viaja en claro, incluida la clave S2S de los
triggers de Firebase — asumible porque esa clave es exclusiva de desarrollo, pero la app móvil
necesitará una excepción de cleartext en su build de debug. Ver
[02_to-be.md](./02_to-be.md#lo-que-cuesta-no-hay-tls).

Queda opcionalmente pendiente, y solo si se quiere: un dominio propio (`api-dev.checkbiz360.com`)
apuntando al servidor, que da una URL legible sin cambiar nada de lo montado.

---

## Fase 3: CI/CD de la rama `staging`

**Estado:** ✅ Completada — 2026-08-18. Commit `7602618`, run `Staging CI/CD` en verde en **34 s**.

**Objetivo:** un push a `staging` despliega solo al entorno de desarrollo.

`.github/workflows/deploy-staging.yml`, gemelo del de producción con las cuatro diferencias que deben
existir: dispara con `staging`, grupo de concurrencia propio, y ruta, proyecto y fichero de entorno
propios. Los secrets de SSH se reutilizan porque es la misma máquina; el workflow ya lee
`STAGING_HOST`/`USER`/`SSH_KEY` si algún día existen, así que mudar desarrollo a otro servidor no
obliga a tocarlo.

**Tres cosas que no son copia del de producción:**

- **Reinicia nginx después de `up`.** Sale de lo aprendido en la Fase 1, no de copiar: sin ese
  reinicio, 8 de las 9 rutas devuelven 502.
- **Comprueba que el directorio contiene `docker-compose.staging.yml`** antes de nada. Una línea que
  descarta el peor accidente imaginable — desplegar staging sobre el checkout de producción.
- **Termina verificando que producción sigue en pie.** Comparten máquina: que un despliegue de
  desarrollo no la toque se comprueba, no se supone.

**Verificado en el primer disparo real:**

- Los 5 pasos en verde, incluida la comprobación de producción.
- `Production CI/CD` **no se disparó**. Los dos workflows conviven sin pisarse.
- Desarrollo quedó en `7602618`; producción sigue en `aa9e008` y sus contenedores conservan el uptime
  del release de la mañana — ninguno se reinició.

**Rollback:** desactivar el workflow. El entorno sigue en pie y se despliega a mano.

---

## Fase 4: Firebase en `dev-encodebiz`

**Estado:** ✅ Completada — 2026-08-18. Rama `staging` del repo de Functions, commit `e2a55864`.

**Objetivo:** que el proyecto de desarrollo tenga el set posterior a la migración y que ninguna
función apunte a producción.

### Cómo se hizo posible

El plan original decía "quitar exports y dejar que Firebase reconcilie". Eso choca con un hecho
estructural: **`functions/src/` se despliega a los dos proyectos**, así que quitar un export para
limpiar desarrollo lo borra también en producción en el siguiente release.

Lo resuelve una **rama**, igual que en la API. `staging` sale de `main` y despliega solo a
`dev-encodebiz`; producción sigue desplegándose desde `main`. El apagado se ensaya donde romperlo no
cuesta nada y llega a clientes ya probado. (Modelo del repo de Functions: `develop` → emulador local,
`staging` → `dev-encodebiz`, `main` → `encodebiz-services`.)

### El riesgo desapareció en vez de mitigarse

El plan preveía configurar `CRITICAL_UPSTREAM_BASE` para que el proxy de arranque no mandara los
logins de desarrollo a producción. Al tirar del hilo salió algo mejor: **la app ya no usa ese proxy**
—llama al contenedor directamente desde `AppConstants.privateApiBase`— y lo que quedaba en el repo
eran comentarios de rollback.

Así que los dos proxies se **eliminaron**, no se configuraron: `criticalHandler` (codebase `critical`
completo) y `merlinIa`. Los dos resolvían su destino con un valor por defecto apuntando a producción
(`|| "https://api.checkbiz360.com"`, `?? "https://api.encodebiz.com/..."`). Sin proxy no hay variable
que se pueda quedar mal.

### Lo que se hizo, en orden

1. `.firebaserc`: `default` deja de ser producción y pasa a `dev-encodebiz`, con alias `dev` y `prod`.
   Complementa la regla —no la sustituye— de pasar `--project` en **todo** comando de Firebase.
2. Borrado completo de las 91 funciones de `dev-encodebiz`, en lotes y con `--project` explícito en
   cada invocación. Control durante el borrado: producción se mantuvo en 95, lista idéntica.
3. Rama `staging`: fuera los exports de las seis migradas, fuera los dos proxies, fuera
   `api-express/` (descontinuado).
4. `functions/.env.dev-encodebiz`: `ANALYTICS_SERVER_URL` al 8080 y la clave S2S **de desarrollo**.
   Retirada `CHECKLOG_INTERNAL_URL`, que la usaba el proxy borrado.
5. Deploy de los dos codebases con `--project dev-encodebiz`.

### Verificado por diferencia

La diferencia entre producción (95) y desarrollo (89) es **exactamente lo que se quería apagar, ni una
de más**: las 6 migradas, los 2 proxies y `cleanupUnverifiedUsers`.

Y tres funciones están en desarrollo y **no** en producción —`listWebhookEndpoints`,
`toggleWebhookEndpoint`, `onChecklogWebhook`—: están en el código y producción no se ha redesplegado
desde que se añadieron. Desarrollo ya va por delante, que es el objetivo.

**Cabo suelto:** `beforeUserCreatedTrigger` dio error en el deploy. La función existe en desarrollo con
el mismo tipo de trigger que en producción, así que lo que falló fue el registro como *blocking
function* en Identity Platform, no la creación. Pendiente de confirmar creando un usuario en el Auth
de desarrollo.

---

## Fase 5: Prueba de extremo a extremo

**Estado:** ✅ El tramo crítico, validado — 2026-08-18.

**Objetivo:** demostrar que la cadena funciona sin tocar un dato de producción.

Se escribió un fichaje real en `entities/DEV-E2E/checklogs/…` del Firestore de `dev-encodebiz` y se
siguió: `onChecklogSync` → `POST /api/sync/checklogs` del 8080 → `checklogs_raw` del Postgres de
desarrollo. La fila aterrizó con todos los campos mapeados (`id`, `entity_id`, `type`, `status`,
`timestamp`, `real_date_market`).

**El control que da valor a la prueba:** el `checklogs_raw` de **producción** tiene 0 filas con
`entity_id = 'DEV-E2E'`. Desarrollo escribió solo en desarrollo. Datos de prueba retirados después.

**Queda por ejercitar** (no bloquea, depende de terceros): app y back office apuntando a desarrollo.
Hoy no pueden — ver la nota de la Fase 6.

---

## Fase 5b: la descarga de informes, portada

**Estado:** ✅ Completada — 2026-08-18. `staging` de la API en `6abfb2d`, de Functions en `ee0482e3`.

Surgió al alinear el back office. `documentsHandler` había entrado por error en la lista de apagado de
la Fase 4: seguía sirviendo las descargas, y el usuario lo corrigió. Al mirarlo de cerca salió el
mapa real de esa función — 9 rutas:

- 8 de CRUD documental, **ya portadas** al contenedor `documents:3007`. Los controladores de descarga
  son **idénticos byte a byte** en Firebase y en el contenedor: la descarga documental ya funcionaba
  allí, y el front la mandaba a Firebase por inercia, no por ninguna razón técnica.
- `GET /reports/:id/download`, que **no existía en ningún contenedor**. Era lo único que mantenía viva
  la función entera.

Se portó (38 líneas de origen) a `services/reports`, y con eso `documentsHandler` deja de tener razón
de existir.

**Dos detalles que no eran evidentes:**

- El bucket se resuelve explícitamente por `FIREBASE_STORAGE_BUCKET`, igual que `uploadReportFile`.
  Con el bucket por defecto del SDK la firma apuntaría a otro sitio del que recibió el fichero, y la
  descarga daría 404 sin motivo aparente.
- La ruta va al **final** del router: `/:reportId/download` es un comodín de dos segmentos y
  registrarlo antes de `/cron/trigger` lo dejaría capturando esa ruta.

**El nudo estaba en el front, no en el backend.** Una sola clave servía las dos descargas, porque las
dos colgaban de la misma función. Al separarse los destinos —documentos a `/api/v1`, informes a
`/api/reports`— hubo que partirla en dos entradas de proxy. Y ahí está lo que hace el cambio seguro:
la entrada nueva se **añade** sin tocar la vieja, y sus `envKeys` **caen de vuelta** a las de
documentos. En un entorno que no defina `DOWNLOAD_REPORTS` —hoy, producción— el handler resuelve a la
Cloud Function de siempre, que también sirve esa ruta. El cambio de código puede llegar a producción
sin romper nada y sin que nadie tenga que recordar añadir una variable.

**Verificado contra el entorno de desarrollo**, los cinco casos del original: 401 sin token, 400 sin
`entityId`, 404 con informe inexistente, 403 sobre una entidad sin permiso, y 200 con URL firmada. La
URL descarga el fichero (200, `application/pdf`), su caducidad coincide al segundo con el `expiresAt`
de la respuesta, y la ventana es de **5 minutos exactos**. Alterar la firma la invalida.

**Apagado solo en desarrollo.** `documentsHandler` se retira por proyecto destino, con el mismo
condicional a prueba de fallos que `beforeUserCreatedTrigger`: se omite únicamente si el destino
afirma ser `dev-encodebiz`. Producción conserva sus 95 funciones y su `documentsHandler`; desarrollo
queda en 88.

**Pendiente, y es una decisión aparte:** apagarla en producción, que solo puede hacerse **después** de
desplegar el front con las claves nuevas. Hoy el front de producción le manda todas las descargas,
documentos e informes.

---

## Fase 6: Adopción

**Objetivo:** que el entorno se use, en vez de quedarse ahí.

**Prerequisito:** Fase 5.

Hoy el flujo es `feat/x → develop → main`. Con el entorno en pie sobran dos ramas de integración
haciendo el mismo trabajo, y la que no despliega a ningún sitio es la que sobra:

```
feat/x  →  staging  →  main
           (despliega a desarrollo)   (despliega a producción)
```

`develop` se retira cuando `staging` haya servido un par de releases. Hasta entonces conviven, con
`staging` como destino por defecto de las PR de feature.

**Criterio de éxito:** una feature completa recorre `feat → staging → main` sin que nadie pruebe nada
contra producción. Y una migración nueva se estrena en desarrollo antes del `psql` manual de prod —
que es, al final, la razón de todo esto.

### Lo que falta para que el ensayo sea completo

Los clientes todavía no pueden apuntar a desarrollo, y hasta que puedan, el apagado se ensaya solo a
medias:

- **App móvil:** `AppConstants.privateApiBase` es una constante fija a `https://api.checkbiz360.com`.
  No pasa por `AppConfig.isDevelopment` —solo lo hacen las URLs que siguen en Firebase—, así que **una
  build de desarrollo ficha contra producción**, en silencio y funcionando. Es el único punto de todo
  este trabajo donde creer que pruebas te hace escribir en datos de clientes.
- **Back office:** de sus 43 entradas de proxy, 34 resuelven a Firebase y 9 al contenedor. `corsConfig.ts`
  ya contempla `dev-saas.encodebiz.com`, así que el dominio existe como concepto.

Ambos se alinean después, por sus equipos. Mientras tanto el ensayo lo conduce quien despliega, a mano.

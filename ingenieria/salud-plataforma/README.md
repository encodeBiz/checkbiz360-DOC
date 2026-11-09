# Salud de la plataforma — informe diario automático

Estado: **en dev y en producción desde el 2026-11-06** (PR #260, #261, #262).
Registro del pase: `DOCS/deployment-prod/proximo-pase-back.md` §40.

## Qué pregunta responde

«¿Aguanta el servidor la demanda? ¿Ha habido picos, caídas, errores o ataques?» Hasta hoy
se contestaba entrando por SSH y leyendo logs a mano (informe del 06-nov-2026). Ahora lo
cierra un servicio cada madrugada sobre el día anterior, lo guarda en Postgres y el
backoffice lo enseña en **Sistema → Salud**.

## Decisión: un servicio aislado, no un módulo de la plataforma

Jose, 06-nov: «es un servicio nuevo, un docker nuevo» y «no puede estar ligado a nada del
sistema». Por eso:

- **Vive fuera del monorepo de servicios** (`salud/` en la raíz, no `services/*`): su propio
  `package.json` y lockfile, sin `@encodebiz/shared`, sin `firebase-admin`. Una sola
  dependencia de ejecución: `pg`. El token de Google se firma con `crypto` de Node.
- **No carga `.env.production` ni `.env.staging`.** Recibe solo sus variables. No ve claves de
  Stripe, SES ni la cuenta de servicio de Firebase.
- **Ningún servicio depende de él** (`depends_on`, nginx, S2S). Si se cae, la plataforma ni se
  entera. El backoffice **lee su tabla**, no le llama: si el servicio está caído, la pantalla
  sigue enseñando el histórico y dice que falta el día.
- **Rol propio en Postgres** (`salud`), con permisos solo sobre sus dos tablas.
- **Cuenta de Google propia** (`salud-lector@<proyecto>`), con el único rol
  `roles/monitoring.viewer`. La de Firebase no puede leer métricas y no se le amplía.
- **Si Postgres no responde**, las muestras se guardan en un fichero de su volumen y se
  vuelcan al volver. Que Postgres no respondía queda apuntado: es justo lo que hay que ver.

## Qué lee del servidor, y cómo

Todo con montajes **de solo lectura**. Sin socket de Docker (darlo equivale a dar root en la
máquina). El contenedor corre con `read_only`, `cap_drop: ALL` y `no-new-privileges`.

| Montaje | Para qué |
|---|---|
| `/proc` → `/host/proc` | CPU, carga, memoria, swap, puertos en escucha (`/host/proc/1/net/tcp*`) |
| `/var/lib/docker/containers` → `/host/docker/containers` | estado de cada contenedor (`config.v2.json`) y sus logs (`*-json.log`) |
| `/var/log` → `/host/var/log` | `fail2ban.log*`, `secure*` (SSH) |
| `/etc/ssh` → `/host/etc/ssh` | si SSH admite contraseña (primera aparición, como sshd) |

El disco se mide con `statfs` sobre el montaje de contenedores, que está en la raíz.

## Qué guarda

**`salud_muestras`** — una fila cada 5 minutos: CPU %, carga, memoria disponible, swap,
disco, y por contenedor su id, estado, salud, reinicios y si murió por memoria. Se podan a
los 45 días.

**`salud_diaria`** — una fila por día de Madrid, escrita a las 03:30 (y al arrancar si falta
la de ayer, y cada hora si falló):

- `recursos`: CPU media/p95/máx, carga máx, memoria disponible mínima, disco máx, swap máx,
  de las muestras del día. NULL si no hubo muestras (día reconstruido).
- `contenedores`: por servicio, reinicios por caída (sube `RestartCount` con el mismo id),
  recreaciones (despliegues: cambia el id), muestras no sanas, muerte por memoria, y líneas
  de error en su log ese día.
- `borde`: del log de nginx — peticiones por hora, por clase, 5xx por ruta, 4xx por código,
  rutas más pedidas, IPs distintas, escaneo (rutas tipo `.env`, `.git`, `.php`…) con las IPs
  que más escanean, 401 de login (máximo por IP, sin guardar IPs de clientes) y, desde que
  nginx registra `$request_time`, latencia p50/p95/p99 y peticiones lentas.
- `seguridad`: baneos de fail2ban, IPs baneadas, intentos SSH fallidos, accesos aceptados
  por clave y **por contraseña**, si SSH admite contraseña, puertos abiertos al exterior,
  días hasta que caduca el certificado TLS.
- `firebase`: de Cloud Monitoring — ejecuciones de funciones por clase y por hora, 5xx por
  función, latencia p50/p95 global y p95 por función, instancias máximas, lecturas,
  escrituras y borrados de Firestore, llamadas a Auth por resultado.
- `postgres`: tamaño, conexiones, bloqueos mutuos y rollbacks del día (diferencia con la
  víspera), tablas más grandes.
- `avisos`: lista calculada en el servidor (rojo, ámbar, info). Dicen lo observado; la causa
  solo si está establecida.
- `fuentes`: qué parte se pudo leer y cuál no, con el motivo. Una parte que falla no tira el
  resto: el informe sale `parcial`.

Solo IPs de **escáneres** (la mayoría de sus peticiones dan 404). Las de clientes no se
guardan: no hacen falta para la pregunta.

## Avisos

| Nivel | Cuándo |
|---|---|
| rojo | un contenedor se reinició por caída o murió por memoria; 5xx del borde > 1 %; disco > 90 %; certificado < 5 días; no hubo muestras en todo el día |
| ámbar | 5xx > 0,2 % o > 20; contenedor no sano en alguna muestra; disco > 80 %; memoria disponible < 15 %; CPU media > 70 %; certificado < 14 días; SSH admite contraseña; acceso aceptado por contraseña; funciones con 5xx; una función con p95 3 veces su mediana de 7 días y > 5 s; p95 del borde > 2 s; bloqueos mutuos en Postgres; Postgres no respondió en alguna muestra |
| info | día con más del doble de peticiones que la mediana de 7 días; escaneo del día |

Un pico de demanda no es un fallo: va como info.

## Alertas en el momento, por correo

Jose, 06-nov: «es importante las alertas en caso de críticos de estabilidad al email de
support@encodebiz.com» y «la estabilidad del servidor debe ser cada 5 min». Cada muestra se
compara con la anterior y abre o cierra incidencias (`salud_alertas`):

| Crítico (correo) | Abre con |
|---|---|
| contenedor no en marcha o `unhealthy`, o desaparecido | 2 muestras seguidas (un despliegue tarda segundos) |
| contenedor reiniciado solo (mismo id, más `RestartCount`) o muerto por memoria | 1 muestra |
| Postgres no responde · el borde (`GET /health`) no responde | 2 muestras |
| disco ≥ 90 % · memoria disponible < 5 % | disco 1, memoria 2 |
| CPU ≥ 95 % | 3 muestras (un cuarto de hora) |
| certificado TLS < 5 días | 1 |

Ámbar (solo pantalla): disco ≥ 80 %, memoria < 15 %, CPU ≥ 85 %, red ≥ 80 % de
`SALUD_RED_MBPS_MAX` (1000 por defecto), certificado < 14 días. Un aviso que empeora a crítico
se avisa como crítico.

- Cierra tras **2 muestras limpias** y manda «Resuelto» con desde y hasta.
- Los críticos de una misma muestra van en **un solo correo** (un reinicio del servidor no manda
  veinte). Una incidencia abierta no se vuelve a avisar.
- El estado vive en `/data/alertas.json`, no en Postgres: un reinicio del servicio no repite
  avisos, y el correo sale aunque la base esté caída.
- El informe diario manda correo **solo si trae algo en rojo**.
- Correo por SMTP de SES con las variables `SMTP_*` del entorno, inyectadas una a una.
- Muestra también la red (Mbps de entrada y salida de las interfaces físicas) y la E/S de disco
  (MB/s; con RAID por software se cuenta el `md`, no sus discos).

## Horario

Muestra cada 5 min. Informe a las 03:30 Europe/Madrid del día cerrado. Reintento cada hora
si falta. `node dist/cli.js informe --fecha AAAA-MM-DD` rehace un día; sin muestras, los
recursos quedan NULL y el informe se marca `reconstruido`. Los logs de nginx y la secure del
servidor permiten reconstruir unas semanas; Cloud Monitoring guarda seis.

## Pase a producción

Ver `DOCS/deployment-prod/proximo-pase-back.md`, sección «Salud de la plataforma».

# La mudanza a un VPS propio — 2026-09-12

Desarrollo deja de compartir máquina con producción. Pasa a un VPS de OVH
(`57.129.153.129`, AlmaLinux 10.2, 4 vCPU, 7,6 GB, 74 GB) y a servirse en
**`https://api-staging.checkbiz360.com`**.

Los documentos `01_as-is.md`, `02_to-be.md` y `03_firebase-dev.md` **no se han
reescrito**: describen el montaje compartido, que fue real entre el 2026-08-18 y hoy.
Este fichero es lo que lo sustituye.

## Por qué, con los números delante

**Compartían disco.** Cada despliegue de desarrollo construía imágenes en el disco de
producción. La caché de build acumulada era de **68 GB** el día de la mudanza.

**El 8080 estaba abierto a internet y sin TLS.** Docker se salta firewalld por completo:
`firewall-cmd --list-all` decía `ports: (vacío)` y el 8080 respondía igual, porque el DNAT
de Docker va por delante y `DOCKER-USER` estaba vacía. En un mes: ~9.700 peticiones, de
las que ~1.700 eran legítimas; el resto, escaneo, incluidos **87 intentos contra ficheros
`.env`**. Ninguno se llevó nada, pero la clave S2S de los triggers sí viajaba en claro.

La solución elegida el 2026-09-03 fue mudarse, no parchear el cortafuegos: el parche
habría roto las demos lanzadas fuera de la oficina, y no quitaba el problema de fondo de
tener los dos entornos en la misma máquina.

## Decisiones que se tomaron al hacerla

**Nombre y TLS, no otro IP pelado.** El IP viejo estaba clavado en 47 variables del panel,
en la app (Dart, excepción cleartext de Android, script de build de iOS), en la lista
blanca de QA y en 15 documentos. Cambiar un IP por otro obligaba a repetir el barrido
entero la próxima vez. Con nombre se hace una vez. Y de paso desaparecen las dos
excepciones de tráfico sin cifrar de la app: una build de desarrollo ya no acepta `http://`.

**Postgres se levantó limpio.** Los 76 MB de `encodebiz_staging` son datos derivados
—analítica, informes, leads de prueba, auditoría—; la fuente de verdad es Firestore
`dev-encodebiz`, que no vive en el servidor y no se movió. El volumen vacío disparó la
cadena de migraciones vía `docker-entrypoint-initdb.d`: **23 tablas creadas desde cero**,
que es justo para lo que existe staging.

**Dos claves SSH, no una.** `~/.ssh/encodebiz_staging` para el portátil y
`~/.ssh/encodebiz_staging_ci` para GitHub Actions. Si se filtra el secret del CI no es la
que abre la sesión del owner, y rotar una no deja fuera por la otra. Ninguna de las dos
abre producción.

**El workflow no se tocó para mudarse.** `deploy-staging.yml` ya llevaba
`secrets.STAGING_HOST || secrets.PROD_HOST` previendo esto: creando los tres secrets, el
despliegue se fue solo al servidor nuevo. Sí cambiaron la URL de QA y el health, que iban
escritos a pelo.

## Endurecido del servidor

| | |
|---|---|
| SSH | solo clave. `PasswordAuthentication no`, `PermitRootLogin no`, `MaxAuthTries 3` |
| fail2ban | la configuración ya medida del otro servidor (`mode = aggressive`, 4 fallos en 1 h, `bantime.increment`) |
| firewalld | 22, 80 y 443. `cockpit` retirado |
| DOCKER-USER | solo 80 y 443 llegan a un contenedor |

**El `10-` del fichero de SSH no es arbitrario.** En `sshd_config` gana la primera
aparición, el `Include` es la primera línea y los ficheros de `sshd_config.d/` se leen en
orden lexicográfico. `50-cloud-init.conf` trae `PasswordAuthentication yes`, así que un
`99-no-password.conf` **no tendría ningún efecto**.

**La regla DOCKER-USER usa `--ctorigdstport`, no `--dport`.** La cadena ve el tráfico
*después* del DNAT de Docker, así que el puerto de destino ya es el del contenedor y
filtrar por él no casa nada. Y el `DROP` está acotado a `-i eth0`: por DOCKER-USER pasa
también la salida de los contenedores, y sin acotar se quedarían sin internet.

Vive en `/usr/local/sbin/docker-user-firewall.sh`, lo reaplica un servicio systemd con
`PartOf=docker.service` — Docker vacía la cadena al arrancar, así que sin eso un
`systemctl restart docker` dejaría el filtro abierto.

## Gotchas de AlmaLinux que reaparecieron enteros

Los mismos dos que costaron una tarde en el servidor de producción, y que volverán a
aparecer el día que se monte otra máquina:

1. **La imagen mínima de OVH no trae los módulos netfilter** y Docker no arranca sin
   ellos. `dnf install kernel-modules-extra-$(uname -r)` y `/etc/modules-load.d/docker.conf`
   con `br_netfilter`, `xt_addrtype`, `iptable_nat`, `xt_conntrack`, `overlay`.
2. **Si firewalld arranca después que docker, le borra la cadena FORWARD** y los
   contenedores dejan de alcanzarse (`EHOSTUNREACH`). Drop-in `After=firewalld.service`.

Y dos nuevos:

3. **El VPS llega con la contraseña caducada.** OVH obliga a cambiarla en el primer acceso
   y `passwd` exige terminal, así que `ssh-copy-id` falla con *«Password change required
   but no TTY available»* antes de poder subir ninguna clave.
4. **74 GB de disco no aguantan la caché de build sin podarla.** Un timer semanal
   (`docker-limpieza.timer`) conserva una semana y, si el disco pasa del 85%, va a fondo.

## Lo que queda por hacer

- **Las variables del panel en Vercel.** Las 47 `NEXT_BACKEND_URI_*` del despliegue de
  desarrollo viven en Vercel, no en git: hasta cambiarlas allí, el panel de desarrollo
  sigue hablando con el servidor viejo.
- **Retirar el stack de desarrollo de la máquina de producción** (`/opt/encodebiz-api-dev`,
  `/var/lib/encodebiz-api-dev`) y cerrar el 8080. Mientras siga en pie es el camino de
  vuelta, así que no corre prisa — pero tampoco se olvida.

# Copias de seguridad

Estado: **en producción desde el 2026-11-07**. Pantalla: Backoffice → Sistema → **Copias**.
Pase: `DOCS/deployment-prod/proximo-pase-back.md` §42.

## Por qué

Hasta el 07-nov la base Postgres de producción no tenía ninguna copia. Jose: «cuidado con los
datos, que no tenemos salvas». Al mirarlo salió que Firestore ya estaba protegido por Google y
que lo que faltaba era el servidor y los ficheros de Storage más allá de una semana.

## Qué está protegido, cómo y dónde

| Qué | Cómo | Cuánto tiempo | Dónde |
|---|---|---|---|
| **Servidor**: Postgres entero, secretos (`secrets/`, `.env.production`), certificados TLS y configuración del sistema (SSH, fail2ban, firewalld, Docker, systemd, `/usr/local/sbin`) | Copia cifrada cada noche a las **02:30** de Madrid. La hace el servicio `salud` (`salud/src/copias.ts`) | 90 días; **los primeros 30 nadie la puede borrar** (retención del bucket) | `gs://encodebiz-services-copias` (EU) |
| **Ficheros de Storage** (documentos, fotos, firmas) | Storage Transfer Service, cada noche a la **01:00 UTC**: copia lo nuevo y lo cambiado, **nunca borra** | La versión anterior de un fichero, 90 días | `gs://encodebiz-services-copias-ficheros` (EU, con versiones) |
| **Firestore** | De Google, no nuestro: recuperación a cualquier instante (PITR) y copia nativa semanal de los domingos | Instante: 7 días. Semanal: 30 días | eur3 |

**Firestore no se copia aparte a propósito.** Se llegó a programar una exportación diaria y se
retiró sin haber corrido (Jose: «estamos duplicando salvas»). Si algún día se quiere más de 30
días o fuera de Google, es `exportDocuments` a este bucket.

El bucket original de Storage (`encodebiz-services.firebasestorage.app`, us-central1) sigue
teniendo además el borrado reversible de Google de 7 días.

## Piezas y permisos

- **Rol Postgres `copias`** (migración 057): `pg_read_all_data`, solo lee. Contraseña en
  `COPIAS_DB_PASSWORD` del `.env.production`.
- **Cuenta `copias-servidor@encodebiz-services`**: `roles/storage.objectCreator` **solo** sobre
  `encodebiz-services-copias`. No puede leer, borrar ni sobrescribir. Clave en
  `/opt/encodebiz-api/secrets/copias-sa.json` (root 600).
- **Cifrado**: `openssl cms`, AES-256, con el certificado `secrets/copias-publica.pem` del
  servidor. **La clave privada no está en el servidor**: está en
  `encodebiz-api/secrets/copias-clave-privada.pem` del portátil de Jose (git la ignora).
  **Hay que guardarla también en el gestor de contraseñas**: sin ella, las copias no se pueden
  abrir. Huella SHA-256 del certificado: `40:A0:21:99:18:00:06:47:E6:93:4A:14:D8:F2:94:48:BA:3E:5D:18:CF:FD:25:1B…`
- **Storage Transfer Service**: trabajo `copias-ficheros-diaria`. Su agente
  (`project-278727535409@storage-transfer-service`) lee solo el bucket de origen y escribe solo
  en el de copias de ficheros.
- **Contenedor `salud`**: para copiar monta en solo lectura `/etc`, `/usr/local/sbin`, `secrets/`,
  `.env.production` y `certbot/conf`, y tiene `DAC_READ_SEARCH` (leer ficheros de otros usuarios;
  no escribir). `mem_limit` 512 MB: el dump pasa por `/tmp`, que es memoria.

## Vigilancia

- Si pasan **26 h sin una copia buena** del servidor, `salud` abre un **crítico** y avisa por
  correo a support@ (también si la primera copia nunca salió).
- Si falla, reintenta cada hora. El estado está en `/data/copias.json` del contenedor y en
  `GET /health` de salud.
- El informe diario guarda el estado de la copia y **el tamaño y los ficheros de cada bucket**
  del proyecto (Cloud Monitoring, `storage/v2/total_bytes` y `v2/total_count`: incluye versiones
  antiguas y borrados reversibles, que es lo que se factura).

## Cómo restaurar el servidor

```bash
# 1. Bajar la copia (cualquier propietario del proyecto puede leer el bucket)
gcloud storage ls gs://encodebiz-services-copias/servidor/2026/11/07/
gcloud storage cp gs://encodebiz-services-copias/servidor/AAAA/MM/DD/prod-<fecha>.tar.cms .

# 2. Descifrar con la clave privada
openssl cms -decrypt -binary -inform DER -inkey copias-clave-privada.pem \
  -in prod-<fecha>.tar.cms -out copia.tar
tar -xf copia.tar          # manifiesto.txt, postgres.dump, ficheros.tar.gz
cat manifiesto.txt         # comprobar sha256 con `shasum -a 256 postgres.dump ficheros.tar.gz`

# 3. Postgres (en una base vacía; en producción, solo con orden de Jose y copia previa)
docker compose --env-file .env.production exec -T postgres \
  pg_restore -U encodebiz -d encodebiz_analytics --clean --if-exists < postgres.dump

# 4. Ficheros del servidor: se extraen y se colocan a mano, uno a uno
tar -tzf ficheros.tar.gz   # opt/secrets, opt/.env.production, opt/certbot/conf, etc/…
```

Probado el 2026-11-07 con la primera copia: se descifra, el manifiesto cuadra con las sumas, el
dump empieza por `PGDMP` y lleva las 70 tablas. Y un `gcloud storage rm` del objeto lo rechazó la
retención.

## Cómo restaurar ficheros de Storage

En `gs://encodebiz-services-copias-ficheros` están con la misma ruta que en el original. Una
versión anterior se ve con `gcloud storage ls -a gs://…/ruta/fichero` y se recupera con
`gcloud storage cp gs://…/ruta/fichero#<generación> gs://encodebiz-services.firebasestorage.app/ruta/fichero`.

## Tamaño y coste (07-nov-2026)

- Copia del servidor: **3,8 MB cifrada** al día; unos 340 MB a los 90 días.
- Ficheros de los clientes: **221 MB**, unos 12 MB más al día (185 MB el 04-nov). Es lo que crece.
- El bucket más grande del proyecto no es de copias: `gcf-v2-sources-…-us-central1`, **8,9 GB**
  de código de funciones (cada versión desplegada). Candidato a limpiar con una regla de ciclo
  de vida.

**Pendiente de decisión de Jose:** cómo repercutir al cliente el almacenamiento y su copia. Los
ficheros llevan la empresa en la ruta (`…/entities/{entityId}/…`), así que el tamaño por empresa
de la copia se puede medir igual que el del original.

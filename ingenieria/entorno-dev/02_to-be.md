# 02 — El entorno objetivo

---

## Los dos stacks

Nada se comparte salvo la máquina y el borde HTTPS. Todo lo demás va duplicado y con nombre distinto,
a propósito: un nombre repetido es una invitación a que un copiar-pegar acabe en la base equivocada.

| | producción | desarrollo |
|---|---|---|
| Ruta en el servidor | `/opt/encodebiz-api` | `/opt/encodebiz-api-dev` |
| Rama | `main` | `staging` |
| Compose project | `encodebiz-api` | `encodebiz-api-dev` |
| Fichero compose | `docker-compose.yml` | `docker-compose.staging.yml` |
| Fichero de entorno | `.env.production` | `.env.staging` |
| Entrada | `api.checkbiz360.com` (:443, TLS) | `141.95.47.135:8080` (sin TLS) |
| Dato de Postgres | `/var/lib/encodebiz-api/postgres` | `/var/lib/encodebiz-api-dev/postgres` |
| Base / usuario | `encodebiz_analytics` / `encodebiz` | `encodebiz_staging` / `encodebiz` |
| Proyecto Firebase | `encodebiz-services` | `dev-encodebiz` |
| Workflow | `deploy.yml` (push a `main`) | `deploy-staging.yml` (push a `staging`) |

**Sobre el nombre.** El entorno es "de desarrollo", pero los ficheros se llaman `staging` porque se
llama así la rama que los despliega. Ya existe un `docker-compose.dev.yml` que levanta solo Postgres
para trabajar en local; llamar `dev` también a lo del servidor garantizaba que alguien levantase el
que no era. El fichero se llama como la rama que lo dispara y no hay ambigüedad posible.

**Sobre la base de datos.** `encodebiz_staging`, no `encodebiz_analytics`. Si una `DATABASE_URL` mal
copiada apunta al Postgres equivocado, queremos que falle con "database does not exist" en el
arranque, no que funcione.

---

## El borde

Solo una cosa puede poseer los puertos 80 y 443, y hoy los tiene el nginx de producción. La primera
versión de este documento proponía añadirle un `server` block para el dominio de desarrollo. Se
descartó por una razón sencilla: **obligaba a tocar producción**, y no hace falta.

**Diseño elegido.** Desarrollo levanta **su propio nginx en el puerto 8080**, con la misma tabla de
rutas y sin TLS. Producción no se modifica en ninguna fase de este plan: sigue siendo la única dueña
del 80 y el 443 y su `nginx.conf` no se abre.

```
Internet ─┬─ :443  api.checkbiz360.com  ──→ nginx (prod) ──→ 9 servicios ──→ postgres
          │
          └─ :8080 141.95.47.135        ──→ nginx (dev)  ──→ 9 servicios ──→ postgres
```

La tabla de rutas de `nginx.staging.conf` es **copia fiel** de la de producción, incluidos los
`location =` exactos que existen para que un POST a la raíz de un servicio no se degrade a GET al
seguir un 301. Mantenerlas idénticas es el punto: si desarrollo enrutara distinto, dejaría de
reproducir lo que pasa en producción, que es para lo que se monta.

### Lo que cuesta: no hay TLS

El tráfico hacia desarrollo viaja en claro, incluida la clave S2S que mandan los triggers de Firebase.
Es asumible porque **esa clave es exclusiva de desarrollo y no abre nada de producción** — el peor
caso es que alguien escriba en la base de pruebas. Dos consecuencias prácticas que sí hay que tener
presentes:

- La app móvil rechaza tráfico en claro por defecto (ATS en iOS, `cleartextTrafficPermitted` en
  Android). Para probar contra desarrollo necesita una excepción en la build de debug.
- Nada que sirva a un navegador real de cliente debe apuntar aquí.

Si más adelante se quiere TLS en desarrollo, la vía que sigue sin tocar producción es un certificado
por DNS-01 sobre un puerto propio (8443). No es trabajo de esta fase.

### Lo que se descartó

- **Añadir un vhost al nginx de producción.** Más elegante de puertas afuera —un dominio limpio, TLS
  gratis— pero abre el fichero de configuración de producción y obliga a un `resolver` con variable en
  el `proxy_pass` para que cada despliegue de desarrollo no deje el vhost en 502. Coste real a cambio
  de comodidad.
- **Sacar nginx y certbot a un stack de borde común.** Obliga a reestructurar producción con ventana
  de caída. Si algún día hace falta, nada de lo montado aquí habría que rehacerlo.

---

## Postgres de desarrollo

Contenedor propio dentro del proyecto `encodebiz-api-dev`, con bind mount en
`/var/lib/encodebiz-api-dev/postgres`. **Sin puerto publicado hacia fuera**: si hace falta un cliente
gráfico, se abre un túnel SSH. Un `5432` abierto al mundo en un servidor que también sirve producción
no se justifica por comodidad.

El montaje de `./migrations` en `/docker-entrypoint-initdb.d` **sí se ejecuta aquí**, porque el
volumen arranca vacío. Es la primera vez que la cadena de las 9 migraciones corre entera desde cero.

A partir de este entorno, el orden de toda migración nueva es: **se ensaya en desarrollo desde cero,
y solo después se aplica a mano en producción.** Hoy ese ensayo no existe.

**Datos:** arranca vacío y se puebla con los triggers de `dev-encodebiz`. Ningún volcado de
producción: los checklogs llevan nombre, DNI y geolocalización de personas reales, y anonimizarlos
bien es un proyecto en sí mismo, no un paso de este.

---

## Secretos y credenciales

Nada de esto viaja en git. Todo vive en `/opt/encodebiz-api-dev/.env.staging` y
`/opt/encodebiz-api-dev/secrets/firebase-sa-dev.json` (la service account de `dev-encodebiz`).

El nombre del fichero **difiere del de producción**, en el host y dentro del contenedor. Con el mismo
nombre, un `scp` mal copiado mete una donde va la otra y nada se queja: el servicio arranca hablando
con el proyecto equivocado. Con nombres distintos, el `.env` de producción usado aquí por error apunta
a un fichero inexistente y el arranque falla en el acto.

| Variable | En desarrollo |
|---|---|
| `ENCODEBIZ_API_KEY` | **Distinta de la de producción.** Es lo que impide físicamente que un trigger de Firebase de dev escriba en la base de producción, y al revés. |
| `GOOGLE_APPLICATION_CREDENTIALS` | SA de `dev-encodebiz`. |
| `FIREBASE_STORAGE_BUCKET` | Bucket del proyecto dev. |
| `POSTGRES_*` / `DATABASE_URL` | Base y contraseña propias. |
| `SMTP_USER` / `SMTP_PASS` | Identidad separada o SES en sandbox. **Sin esto, probar el formulario de la landing manda correo real a soporte.** |
| `OPENAI_API_KEY` | Clave propia con tope de gasto. Merlin en dev se llama en bucle mientras se prueba. |
| `TURNSTILE_SECRET_KEY` | Claves de prueba de Cloudflare (siempre pasan o siempre fallan, a elegir). |
| `STRIPE_*` | Modo test, con su propio webhook. |

---

## CI/CD de desarrollo

`.github/workflows/deploy-staging.yml`, calcado del de producción salvo en lo que debe diferir:

- Dispara en push a `staging` (y `workflow_dispatch`).
- `concurrency: staging-deploy` — grupo propio, para que un despliegue de dev no cancele uno de prod.
- Mismos secrets de SSH (mismo host, mismo usuario, misma clave) y `DEPLOY_PATH=/opt/encodebiz-api-dev`.
- `docker compose -p encodebiz-api-dev --env-file .env.staging -f docker-compose.staging.yml up --build -d`.
- Reinicia **su** nginx, no el de producción. No es opcional: nginx resuelve los upstreams al
  arrancar, y `up -d` recrea los contenedores con IPs nuevas. Verificado en la Fase 1 — sin el
  reinicio, 8 de las 9 rutas devuelven 502.
- Comprueba salud contra `http://localhost:8080/health`.
- Poda imágenes huérfanas al final: dos stacks construyendo en la misma máquina acumulan capas rápido.

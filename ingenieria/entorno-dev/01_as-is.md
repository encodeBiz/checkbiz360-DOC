# 01 — Lo que hay hoy

Todo lo de aquí está **medido** el 2026-08-18 contra el servidor y los proyectos reales,
no recordado.

---

## El servidor

Kimsufi/OVH RISE-1, AlmaLinux 10.2, `141.95.47.135`.

| Recurso | Total | En uso |
|---|---|---|
| CPU | 12 vCPU | — |
| RAM | 31 GiB | 5,1 GiB |
| Disco `/` | 475 GB | 29 GB (7 %) |

Los **12 contenedores de producción suman ~570 MiB de RAM**. El más gordo, `reports`, ocupa 66 MiB.

> Esto zanja la única duda razonable sobre meter un segundo entorno en la misma máquina:
> un stack duplicado cuesta otros ~570 MiB sobre 26 GiB disponibles, y las imágenes otro par de
> gigas sobre 446 GB libres. **La capacidad no es el problema; el aislamiento sí.**

---

## El stack de producción

- **Ruta:** `/opt/encodebiz-api`, clon de `main`, commit desplegado `aa9e008`.
- **Compose project:** `encodebiz-api` (por nombre de directorio).
- **Servicios:** `merlin:3001`, `checkinbiz:3002`, `sync:3003`, `analytics:3004`, `reports:3005`,
  `tasks:3006`, `documents:3007`, `rentman:3008`, `sales:3009`, más `nginx`, `postgres` y `certbot`.
- **nginx** posee los puertos **80 y 443** del host. Un solo `server_name`:
  `api.checkbiz360.com`. Recarga sola cada 6 h para recoger certificados renovados.
- **certbot** renueva por webroot cada 12 h contra `./certbot/www`.
- **postgres** monta el dato en `/var/lib/encodebiz-api/postgres` (bind mount, no volumen Docker)
  y `./migrations` en `/docker-entrypoint-initdb.d`.

### El detalle que más pesa en este documento

El montaje de `migrations/` **solo se ejecuta cuando el volumen arranca vacío**. En producción el
volumen tiene datos desde el primer día, así que ese montaje no ha corrido nunca más. Cada `.sql`
nuevo se aplica a mano por SSH con `psql` —así entró `009_rentman_hours.sql`—.

La consecuencia no es la incomodidad, es esta: **las 9 migraciones nunca se han ejecutado seguidas
desde cero en ningún sitio**. Nadie sabe si la cadena completa levanta un esquema válido.

---

## El CI/CD actual

`.github/workflows/deploy.yml`, disparado por push a `main` (o a mano):

1. El runner entra por SSH con `PROD_SSH_KEY`.
2. Verifica que existan `.env.production` y `secrets/firebase-sa.json`.
3. `git pull --ff-only origin main` con la deploy key del servidor.
4. `docker compose --env-file .env.production up --build -d` — **el build ocurre en el servidor**,
   GitHub no construye nada.
5. `restart nginx` — necesario porque nginx cachea las IPs de los upstreams al arrancar.
6. `curl http://localhost/health`.

No aplica migraciones ni toca `.env.production`. Ambas cosas son manuales y están documentadas
en cada PR de release que las necesita.

---

## Firebase

Un solo proyecto en uso real: **`encodebiz-services`**. El proyecto **`dev-encodebiz`** existe,
tiene funciones desplegadas y lleva congelado desde mayo.

|  | `encodebiz-services` (prod) | `dev-encodebiz` |
|---|---|---|
| Funciones desplegadas | 95 | 90 |
| Triggers de sync a Postgres | los 4 | **ninguno** |
| `beforeUserCreatedTrigger` | sí | **no** |

Las cinco que le faltan a dev son justo las que conectan Firebase con el servidor:
`onChecklogSync`, `onBranchPatternSync`, `onEmpPatternSync`, `onTaskRatingSync`
y `beforeUserCreatedTrigger`. Todo lo demás lo tiene idéntico — incluido lo que ya migró a
contenedor y lo que se dio de baja (`cleanupUnverifiedUsers` sigue desplegada en dev).

### Configuración por proyecto

El mecanismo ya existe: `functions/.env.encodebiz-services` y `functions/.env.dev-encodebiz`.
El de dev es del 25 de mayo y **no tiene** `ANALYTICS_SERVER_URL`, `ANALYTICS_API_KEY` ni
`ENCODEBIZ_API_KEY`.

### El riesgo serio

`functions-critical/` **no tiene ningún fichero de entorno**. Su código hace:

```js
const UPSTREAM_BASE = process.env.CRITICAL_UPSTREAM_BASE || "https://api.checkbiz360.com";
```

Desplegado hoy tal cual sobre `dev-encodebiz`, **el proxy de arranque de la app de desarrollo
mandaría los logins contra producción**. Es el único punto de todo el inventario donde un despliegue
de dev alcanza datos de clientes, y es silencioso: responde 200 y funciona.

---

## Estado del repositorio (tras la estabilización del 2026-08-18)

`main`, `develop` y `staging` alineadas en `aa9e008`. Sin PRs abiertas. Sin ramas locales huérfanas.
Quedan en `origin` cinco ramas ya integradas pendientes de barrer y
`freature/addons-fleetbiz-glovo`, un microservicio nuevo sin integrar y fuera del flujo.

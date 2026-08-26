# Entorno de Desarrollo — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** plataforma — infraestructura y entornos
**Fecha de inicio:** 2026-08-18
**Estado:** Diseño / pendiente de aprobación
**Autor:** Jose Acevedo

---

## Contexto y Motivación

Hoy solo existe un entorno vivo. `api.checkbiz360.com` es a la vez el sitio donde se prueba y el sitio
donde trabajan los clientes. Cada migración de Firebase a contenedor —tareas, documental, informes,
arranque de la app, fichajes— se ha ensayado contra producción, y ha salido bien por cuidado, no por
diseño. La única excepción fue Rentman, y solo porque Rentman regala una cuenta sandbox.

Tres hechos concretos, medidos, que dicen que el margen ya se agotó:

1. **Las migraciones de Postgres se aplican a mano.** El montaje de `migrations/` en
   `docker-entrypoint-initdb.d` solo corre cuando el volumen está vacío, así que en producción no se
   ejecuta nunca. Cada `.sql` nuevo entra por `psql` por SSH. La consecuencia real es que **la cadena
   completa de las 9 migraciones no se ha ejecutado desde cero en ninguna parte**: nadie sabe si
   funciona seguida.
2. **La PR #46 lleva 12 días abierta.** No por dudas técnicas —está `CLEAN`— sino porque mergearla
   despliega Turnstile y la imputación de horas de Rentman directamente sobre clientes, y antes hay que
   acordarse de dos pasos manuales en el servidor.
3. **El proyecto `dev-encodebiz` existe y está podrido.** Tiene 90 funciones desplegadas, congeladas
   desde mayo, que son exactamente el mundo anterior a las migraciones. Le faltan los cuatro triggers
   de sync y le sobra todo lo que ya sirve un contenedor.

Este documento monta el entorno de desarrollo en el mismo servidor de producción, con su propio stack,
su propio Postgres y su propio proyecto de Firebase, y deja el despliegue automatizado.

---

## Principio de diseño

> **Un servidor, dos stacks que no se conocen.**
> Lo único que comparten es la máquina y el borde HTTPS. Ni un dato, ni una credencial, ni un puerto.

De ahí sale todo lo demás: Postgres propio con volumen propio, proyecto de Firebase `dev-encodebiz`,
`ENCODEBIZ_API_KEY` distinta —es lo que impide físicamente que un trigger de Firebase de desarrollo
escriba en la base de producción—, remitente de correo separado y claves de Stripe y Turnstile de prueba.

El corolario, decidido sobre la marcha en la Fase 1: **ni siquiera comparten el borde**. Desarrollo
levanta su propio nginx en el 8080 en vez de añadir un vhost al de producción, así que **no hay ninguna
fase de este plan que abra un fichero de configuración de producción**. Se paga con no tener TLS en
desarrollo; el razonamiento está en [02_to-be.md](./02_to-be.md#el-borde).

---

## Alcance

**Entra:**

- `encodebiz-api` — los 9 servicios, nginx y Postgres, desplegados en paralelo a producción.
- Firebase Functions sobre el proyecto `dev-encodebiz`: limpieza, set objetivo y configuración.
- CI/CD: la rama `staging` despliega sola al entorno de desarrollo.

**No entra en esta fase:**

- Front de administración, landing y apps móviles. Se apuntan al entorno cambiando su base URL cuando
  esté en pie; no requieren nada de este documento.
- TLS en desarrollo. Se sirve por HTTP en el 8080 para no tener que tocar el nginx de producción;
  el coste y las alternativas están en [02_to-be.md](./02_to-be.md#lo-que-cuesta-no-hay-tls).

---

## Índice

- [01_as-is.md](./01_as-is.md) — lo que hay hoy, medido
- [02_to-be.md](./02_to-be.md) — el entorno objetivo
- [03_firebase-dev.md](./03_firebase-dev.md) — qué se sube a `dev-encodebiz` y qué no
- [04_fases.md](./04_fases.md) — el roadmap, fase a fase

# Salida del monolito — retirada de `encodeBiz-SAAS`

**Proyecto:** encodeBiz · plataforma
**Fecha de inicio:** 2026-09-08
**Estado:** Diseño aprobado / Implementación en curso
**Autor:** Jose Acevedo

---

## Contexto

Las Cloud Functions del SaaS son un monolito con forma de bundle. Todo —el CRUD del panel,
los disparadores de Firestore, los cron, passinbiz y checkbiz— se exporta desde un único
objeto `apiV100` en `functions/src/index.ts`, se compila junto y se despliega junto. Cambiar
el alta de una sucursal y el worker de correos es el mismo `npm run build`, el mismo
`tsconfig` y, si alguien se despista con la lista de `--only`, el mismo despliegue.

Eso tiene tres costes que ya estamos pagando:

- **Nadie sabe qué está corriendo.** Lo desplegado no corresponde a ninguna rama concreta;
  se despliega por nombre de función, a mano y de tanto en tanto.
- **Todo cuesta un arranque en frío**, incluso lo que se llama cien veces al día.
- **La historia está partida en dos repositorios.** Media plataforma vive en `encodebiz-api`
  y la otra media en `encodeBiz-SAAS`, y hay dominios —empleados, patrones, eventos— con una
  implementación viva en cada sitio.

Ya se han hecho salidas parciales y han salido bien: fichajes, calendario, tareas,
documental, informes, merlin, eventos y el add-on de Rentman se sirven hoy desde
contenedores. Este documento cierra lo que queda y fija el orden.

## Principio

> **Se sale del monolito, no se muda el monolito.**

Cada pieza que sale busca el servicio del contenedor donde le toca vivir, y las que existen
solo para observar una escritura desaparecen dentro del caso de uso que hace esa escritura.
Amontonar los 29 disparadores en `services/firebase_sdk` sería cambiar un monolito de sitio
y conservar sus dos peores propiedades: el arranque en frío y el despliegue en bloque. Ver
[ADR-001](./adr/ADR-001-el-destino-es-el-caso-de-uso.md).

Y no se sale del monolito para construir otro más pequeño. `checkinbiz` se queda con el
**núcleo** —validar, entrar, segundo factor, calendario, fichar, y lo de lo que eso depende
para ser correcto: colaboradores y `geo`— y cada CRUD de gestión estrena contenedor:
`employees`, `branches` y `entities`. Ver
[ADR-003](./adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md).

## Alcance

**Dentro** — todo lo de checkbiz que sigue en `encodeBiz-SAAS`: once piezas HTTP sin portar,
seis ya portadas que solo esperan el corte, y veintinueve funciones reactivas entre
disparadores de Firestore y cron.

**Fuera** — passinbiz entero. El producto está descontinuado y su retirada ya está decidida
en [eventos-webhooks/ADR-005](../eventos-webhooks/adr/ADR-005-retirada-de-passinbiz.md): no
se porta, se apaga con el repositorio. Son nueve funciones HTTP, cinco disparadores y los
tres endpoints de eventos de pase.

**Fuera también** — la facturación no se corta aquí. Tiene su propio plan por fases en
[billing-v2](../billing-v2/04_fases.md), cuyo criterio innegociable es que ningún camino de
cobro se apaga el mismo día que se enciende su sustituto. Este documento solo dice qué queda
pendiente y en qué orden entra cuando aquel plan lo permita.

## Documentos

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Estado actual](./01_as-is.md) | Inventario completo: qué sirve cada lado hoy, con nombres |
| 02 | [Arquitectura objetivo](./02_to-be.md) | A dónde va cada pieza, y por qué casi nada va a `firebase_sdk` |
| 03 | [Contratos y cortes](./03_contratos-y-cortes.md) | La forma real de cada llamada y cuáles cortan con una variable |
| 04 | [Fases de implementación](./04_fases.md) | El roadmap, con criterios de validación y rollback por fase |

## Decisiones

| ID | Decisión | Estado |
|----|----------|--------|
| [ADR-001](./adr/ADR-001-el-destino-es-el-caso-de-uso.md) | El destino de un disparador es el caso de uso que escribe, no otro alojamiento | Aceptado |
| [ADR-002](./adr/ADR-002-el-contrato-viejo-se-imita.md) | El contenedor imita el contrato viejo; el panel no se toca para cortar | Aceptado |
| [ADR-003](./adr/ADR-003-el-nucleo-y-un-contenedor-por-dominio.md) | `checkinbiz` es el núcleo; cada CRUD de gestión, su propio contenedor | Aceptado |

## Estado del roadmap

- [~] **Fase 1** — Servicio `employees` (3013) **construido**: router fuera del núcleo, los
  dos alias, y `canWrite` + cupo de plan, que el port anterior se había dejado por el
  camino. **Pendiente:** desplegar y cortar las cuatro variables del panel.
- [~] **Fase 2** — Servicio `branches` (3014) **construido**: CRUD portado con su validación
  entera, cupo de plan, índice idempotente y los cuatro eventos `branch.*`, que el catálogo
  ofrecía comentados esperando a esto. **Pendiente:** desplegar y cortar tres variables.
- [~] **Fase 3** — Servicio `entities` (3015) **construido**: empresa, marca y usuarios.
  **Fuera:** el borrado de entidad (cascada) y la subida de ficheros (`media`), que pide
  multipart y Storage. **Pendiente:** desplegar y cortar tres variables.
- [~] **Fase 4** — El resto del HTTP. **Hecho:** el 2FA del panel al núcleo; la heurística a
  `analytics` con su motor, que llevaba meses portado y muerto en `checkinbiz`;
  responsabilidades y avisos operativos a `employees`; `media` a `entities`; y `updateAuth`
  como `PATCH /collaborators/:userId`, que era el verbo que le faltaba a ese router.
  Y `assignUser` completo, que era la última pieza HTTP del panel. **Con eso no queda
  ninguna por portar.** Fuera a propósito: `recalcDailyReport`, que va con su cron en la
  fase 5 —ver [04 §Fase 4](./04_fases.md)—.
- [ ] **Fase 5** — Lo reactivo: cada disparador a su caso de uso, cada cron a su contenedor.
  Se le suman `recalcDailyReport` y `planifierHelper`, que son los disparadores manuales de
  dos de esos trabajos y comparten código con ellos.
- [ ] **Fase 6** — Apagado del codebase `default` y retirada del repositorio

Ver [04_fases.md](./04_fases.md) para el detalle, los criterios de salida y el rollback de
cada una.

Las tres primeras están **escritas y verdes** —typecheck del monorepo, arranque, `/health` y
las rutas respondiendo 401 sin token—, en la rama `feat/salida-del-monolito`. Lo que falta de
las tres es lo mismo: desplegarlas en desarrollo y mover las variables del panel, que es el
único paso que cambia por dónde va el tráfico.

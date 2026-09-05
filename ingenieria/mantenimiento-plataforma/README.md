# Mantenimiento de la plataforma — cuentas fantasma

**Estado:** implementado, sin desplegar. Rama `feat/mantenimiento-usuarios-fantasma`
(2026-09-04).

Cada madrugada se buscan las cuentas de Firebase Auth **que no son de nadie** y se retiran.
De cada pasada y de cada cuenta queda constancia en Postgres, y eso se mira en el backoffice.

## Qué es una cuenta fantasma

Una cuenta de Firebase Auth que **no tiene rol en ninguna entidad ni ficha de empleado en
ninguna**, y que lleva al menos siete días creada.

No basta con no haber verificado el correo, ni con no haber entrado nunca. Eso importa
porque ya se intentó al revés: `cleanupUnverifiedUsers` borraba toda cuenta con más de 48 h
sin verificar el email, y en treinta días borró tres cuentas de las cuales **ninguna
sobraba** —dos eran la misma persona real, dueña de una entidad, que se volvió a registrar
después de que la borraran la primera vez—. Se descontinuó el 2026-07-31.

Las cuentas fantasma aparecen solas, y por dos caminos que están en el código:

- **El alta no es transaccional.** Registrarse crea la cuenta de Auth y `users/{uid}`; crear
  empresa es un paso aparte y opcional. Quien abandona a medias deja una cuenta sin nada.
- **Dar de baja a un empleado no toca Auth**, a propósito: `deleteEmployee` deja la ficha en
  `status: "fired"` y la cuenta viva, porque la misma persona puede volver o estar en otra
  empresa. Si la ficha se borra de verdad más tarde, la cuenta queda suelta.

Molestan porque el correo es único: mientras la cuenta fantasma exista, esa persona no puede
volver a darse de alta con su correo.

## Dónde vive cada pieza, y por qué

| Pieza | Dónde | Por qué ahí |
|---|---|---|
| El barrido | `services/firebase_sdk/src/maintenance/` (Cloud Functions, `onSchedule`) | La lista de cuentas está en Firebase Auth y solo se recorre desde dentro |
| La constancia | Postgres, tablas `maintenance_runs` y `maintenance_ghost_users` (migración 022) | Es la base que ya guarda el histórico consultable; un borrado hay que poder explicarlo meses después |
| El puente | `POST /api/v1/backoffice/s2s/maintenance/...`, con clave S2S | Postgres no sale de la red de contenedores |
| La pantalla | `apps/backoffice-web` → **Mantenimiento** (permiso `maintenance:read`) | Donde ya se mira todo lo demás |

Ver [ADR-001](adr/ADR-001-constancia-en-postgres-barrido-en-firebase.md).

## El orden, que es el diseño

1. **Se abre la pasada en Postgres.** Si eso falla, la función se cae y no se toca nada.
2. **Se lee el censo entero** —roles, empleados, entidades, equipo del backoffice— de una
   sentada. Si alguna lectura falla o se trunca, la pasada cierra en `error` y no toca nada.
3. **Se recorre Auth y se clasifica en memoria.** Aquí todavía no se borra.
4. **Saltan los fusibles**, si tienen que saltar.
5. **Cuenta a cuenta**: se escribe la fila con la copia de su ficha → se borra → se escribe
   el desenlace.

La regla de la que cuelga todo: **lo que no está escrito, no pasa.** La copia de la ficha se
guarda *antes* del borrado, no después, porque es lo único que permite deshacerlo.

## Las salvaguardas

Una cuenta huérfana de más de siete días es *candidata*, y deja fila aunque no se toque. Se
conserva, diciendo cuál saltó, si:

| Motivo | Qué protege |
|---|---|
| `es_soporte` | Está en `backoffice_users`. Estas cuentas no tienen entidad ni ficha: son huérfanas para cualquier criterio razonable, y son las del equipo. Borrar una deja el panel sin nadie dentro |
| `es_facturacion` | Su correo es el `billingEmail` de una entidad. Es la última red del dueño de una empresa si su rol se perdió por el camino, que ya ha pasado |
| `lista_blanca` | Correo o dominio en `MAINTENANCE_GHOST_ALLOWLIST` |
| `sesion_reciente` | Ha entrado en los últimos siete días. Alguien la usa: lo que falta es la ficha, no la persona |
| `evidencia_incompleta` | Falta la fecha de alta. Ante un dato que no está, no se decide |

Y el cruce con las fichas de empleado se hace **por uid y por correo**: `Employee.uid` es
opcional, y las fichas antiguas o importadas por un add-on no lo llevan. Cruzando solo por
uid, un empleado de verdad parecería no existir.

## Los fusibles

No protegen de un criterio equivocado. Protegen de que el código **lea mal el censo** y
llame huérfano a todo el mundo, que es un fallo que no avisa: simplemente sale una lista muy
larga.

- **Tope por pasada** (`MAINTENANCE_GHOST_MAX_PER_RUN`, 25).
- **Proporción** (`MAINTENANCE_GHOST_MAX_SHARE`, 10 % de lo escaneado).

Cuando salta cualquiera de los dos, la lista se escribe entera con motivo `tope_por_pasada`
o `proporcion_sospechosa`, **no se borra nada**, y la pasada cierra en `parcial` para que
salga el aviso en el panel.

## Qué se borra, y en qué orden

Primero el acceso, después los datos:

1. La cuenta de Firebase Auth.
2. La entrada de `searchIndex` (`users__{uid}`).
3. El documento `users/{uid}`.

Si se cae a mitad, lo que queda es lo inofensivo: una ficha suelta que ya no puede usar
nadie. Al revés quedaría una cuenta que sí puede entrar y a la que le falta todo lo demás.
Deshacerlo se puede: la copia está guardada y una cuenta de Auth se recrea con su mismo uid.

## Cómo se mira

Backoffice → **Mantenimiento**. Enseña la última pasada, el histórico, y las cuentas de cada
una con su desenlace y su motivo. Busca por correo o por uid, que es la pregunta que llega
por soporte: *«este cliente dice que no puede entrar»*.

Los avisos de arriba son lo importante, y están pensados para detectar lo que no se ve:

- **No hay ninguna pasada** o la última es de hace más de 30 h. Un trabajo programado que
  deja de correr no da ninguna señal; su única señal es que dejan de aparecer filas.
- **Una pasada sin cerrar.** Murió a mitad. Se buscan en todo el tramo, no solo en la
  última: si no, la del martes desaparece en cuanto la del miércoles va bien.
- **Cuentas a medio borrar** (`detectado`). Cada una puede tener la ficha retirada y el
  acceso vivo, o al revés. Hay que mirarlas a mano.

## Configuración

En el `.env` de las funciones (`services/firebase_sdk/.env.example` las lista todas):

| Variable | Defecto | Qué hace |
|---|---|---|
| `MAINTENANCE_API_URL` | — | Base del backoffice. Sin defecto: sin ella no arranca |
| `MAINTENANCE_API_KEY` | — | La `ENCODEBIZ_API_KEY` de ese entorno |
| `MAINTENANCE_GHOST_APPLY` | vacío | **El interruptor.** Sin él, detecta y no toca nada |
| `MAINTENANCE_GHOST_MIN_AGE_DAYS` | 7 | Días desde el alta para ser candidata |
| `MAINTENANCE_GHOST_MAX_PER_RUN` | 25 | Fusible |
| `MAINTENANCE_GHOST_MAX_SHARE` | 0.1 | Fusible |
| `MAINTENANCE_GHOST_ALLOWLIST` | vacío | Correos o dominios intocables |
| `MAINTENANCE_GHOST_RECENT_SIGNIN_DAYS` | 7 | Margen de `sesion_reciente` |
| `MAINTENANCE_GHOST_CRON` | `15 4 * * *` | Después de la foto diaria del backoffice (3:20) |
| `MAINTENANCE_GHOST_TZ` | `Europe/Madrid` | |

## Puesta en marcha

En este orden, y sin saltarse el paso 4.

1. **Migración 022 a mano**, como todas (el `initdb` solo corre con el volumen vacío):

   ```bash
   cd /opt/encodebiz-api-dev
   docker compose -f docker-compose.staging.yml -p encodebiz-api-dev exec -T postgres \
     psql -U encodebiz -d encodebiz_staging < migrations/022_mantenimiento_usuarios_fantasma.sql
   ```

2. **El código, por la cadena** `feat/… → develop → staging`. El backoffice se redespliega
   solo al empujar `staging`. Nada de reconstruir contenedores por SSH.

3. **La función, a mano y con `--project` explícito**, que es lo único que se despliega a
   Firebase desde este repositorio:

   ```bash
   cp services/firebase_sdk/.env.example services/firebase_sdk/.env.dev-encodebiz
   # rellenar MAINTENANCE_API_URL y MAINTENANCE_API_KEY, dejar APPLY vacío
   npm run deploy:dev -w services/firebase_sdk
   ```

   El `codebase` es `triggers`, nunca `default`: un deploy con el nombre `default` borraría
   todas las funciones que `encodeBiz-SAAS` tiene desplegadas.

4. **Mirar el panel varios días con el interruptor apagado.** La lista de «se habría
   borrado» es lo que dice si el criterio está bien. Esto no es una formalidad: es
   exactamente el paso que faltó la vez anterior.

5. Cuando la lista sea la esperada, `MAINTENANCE_GHOST_APPLY=1` y volver a desplegar.

En producción, lo mismo y por separado: su propia migración a mano, su `.env.<proyecto>`, y
otra vez varios días simulando antes de armarlo.

## Lo que este trabajo NO hace

- **No borra entidades ni empleados.** Solo cuentas de Auth que no son de nadie.
- **No limpia los `user_entity_roles` huérfanos** que dejó `deleteEntity` al borrar una
  entidad quitando el rol solo de quien llamaba. Es otro barrido, y de momento esos roles
  *protegen* a su cuenta de este.
- **No retira la ficha `fired`** de un empleado dado de baja.
- **No tiene política de retención.** Las copias guardadas contienen datos personales de
  gente ya borrada y hoy se quedan ahí para siempre. Cuando se fije, se purga por
  `created_at`.

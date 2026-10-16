# Pase a producción — cuadrante por plantilla (octubre 2026)

**Estado: pendiente, sin fecha.** Jose, 2026-10-16: «ve documentando el pase a prod como pendiente
para que no se olviden cosas». Se va completando; el día del pase se ejecuta en el orden de §7 y
cada paso se anota en §8 con hora y resultado, como en
[2026-10-inventario-firma-back.md](./2026-10-inventario-firma-back.md).
**Alcance:** la importación del cuadrante por plantilla
([TDR-001 de cuadrantes](../ingenieria/cuadrantes/tdr/TDR-001-importacion-por-plantilla-de-sucursal.md)):
la plantilla de toda una sucursal con una pestaña por persona, la plantilla de una sola persona
desde su ficha, y la corrección de las reglas de Firestore que salió al preparar este registro.
**Dónde está:** `develop` de los dos repos y `staging` de la API desde el 2026-10-15; la corrección
de reglas, en `develop` de la API desde el 2026-10-16 (`ac3ee5f`) y aún no en `staging`. **Reglas desplegadas en dev el 2026-10-16** (§8); en prod, no.
**Última revisión:** 2026-10-16, contrastado con `git diff origin/main..origin/develop` de la API.

---

## 0. Lo primero, porque no es evidente

1. **Las reglas de Firestore dejaban abiertas las subcolecciones «de solo servidor».**
   `soloServidor` solo miraba la colección raíz, y `cuadrante_proposals` y `cuadrante_lotes` cuelgan
   de `entities/{e}`, igual que `calendar_days` (del horario por tareas, otra sesión) cuelga de
   `entities/{e}/employees/{p}`. Con la regla de antes, las tres se leían y se escribían desde el
   navegador. **Probado con el emulador**, no supuesto: 7 casos en rojo con el fichero anterior y
   26 en verde con el corregido (§3.1). La corrección está en `develop`; no se ha desplegado a
   ningún entorno.
2. **En producción, hoy, las propuestas de cuadrante se pueden leer desde el navegador.** Existen
   en prod desde el 20-sep (la lectura por modelo de la ficha del empleado) y llevan nombres y
   domicilios de las personas atendidas por el cliente. El ruleset vivo de prod (el del 14-oct)
   deja leer cualquier colección que no sea `signing_keys` o `signing_challenges`, sin sesión.
   Es el comodín heredado que nadie ha cerrado, no algo que trajera este trabajo. **No está
   establecido** que nadie las haya leído. Las reglas se pueden desplegar solas, antes que el
   código (§3.1); decidirlo es de Jose.
3. **No hay contenedor nuevo, ni variable, ni migración.** Todo vive en `merlin`, que ya existe en
   prod, y en el panel. Lo único de infraestructura es una línea de nginx (§2).
4. **Nada de esto se ha visto en un navegador por quien lo escribió.** Jose lo estaba probando en
   su panel local contra staging el 2026-10-15. La aceptación de §5 es requisito, no trámite.
5. **El hook `block-prod.sh` no está registrado** (anotado el 14-oct). Conviene rearmarlo antes del
   día del pase, que es cuando más comandos de prod se escriben al lado de los de dev.

## 1. API (`encodebiz-api`) — lo que lleva el merge `staging → main`

| Qué | Dónde | Notas |
|---|---|---|
| Lector y generador de la plantilla | `services/merlin/src/soporte/cuadrantes/plantilla/` | Sin modelo: nada sale del servidor |
| Lote: dominio, Firestore y aplicación en segundo plano | `cuadrantes/{domain,infrastructure,application}/lote*.ts` | Colección nueva `entities/{e}/cuadrante_lotes`, se crea sola |
| Rutas `/plantilla` y `/lotes` | `cuadrantes/interfaces/cuadrantes.router.ts` | Por las dos puertas: panel con token y backoffice con API key |
| La plantilla de una persona y la detección por contenido | misma ruta `POST /` de siempre | Si no es la plantilla, sigue por el modelo como hasta ahora |
| `revisar` en modo plantilla | `cuadrantes/application/revisar.ts` | La lectura por modelo no cambia de comportamiento |
| Tests puros | `services/merlin/test/plantilla.test.ts` | `npm test -w services/merlin`, 15 en verde |
| Reglas | `firestore.rules` | §3.1 |
| Prueba de reglas con el emulador | `qa/reglas/` | §3.1 |
| nginx | `nginx/nginx.conf` | §2 |

`merlin` lo redespliega el CI al fusionar a `main`, como siempre.

## 2. `nginx/nginx.conf` de producción

Ya va en el fichero de `develop`; llega con el merge, no hay que copiar nada a mano:

```nginx
    location /api/v1/gpt/ {
      proxy_pass http://merlin_service/api/v1/gpt/;
      client_max_body_size 4m;   # cuadrantes: plantilla o documento de 2 MB en base64 + margen (cuadrantes/TDR-001)
    }
```

Sin esta línea, nginx corta en su mega por defecto y un fichero de más de unos 750 KB llega como
un 413 que el panel enseña como «no se ha podido leer». Afecta también a la lectura por modelo de
la ficha del empleado: por la configuración de `main`, un PDF de ese tamaño ya fallaría así en
prod (deducido del fichero, no observado). El `deploy.yml` de producción reinicia
nginx tras el `up -d` (línea 54), así que no hace falta hacerlo a mano.

## 3. Firestore

### 3.1 Reglas — dev primero, luego prod, siempre solo las reglas

**Antes de nada, la prueba con el emulador** desde `encodebiz-api` en `develop`:

```bash
cd qa/reglas && cp ../../firestore.rules . && \
  echo '{"firestore":{"rules":"firestore.rules"},"emulators":{"firestore":{"port":8089,"host":"127.0.0.1"},"ui":{"enabled":false}}}' > firebase.json && \
  JAVA_HOME=/opt/homebrew/opt/openjdk@26/libexec/openjdk.jdk/Contents/Home PATH="$JAVA_HOME/bin:$PATH" \
  firebase emulators:exec --only firestore --project demo-reglas ./probar-reglas.sh; \
  rm -f firestore.rules firebase.json
```

Tiene que acabar en `fallos: 0`. El emulador ya no arranca con Java 17: hace falta 21 o más (el
JDK 26 de Homebrew vale).

Después, **dev**:

```bash
firebase deploy --only firestore:rules --project dev-encodebiz
```

y comprobar en dev, sin sesión, que `calendar` y `employees` siguen respondiendo a una consulta de
grupo (el fallo del 14-oct) y que `entities/{e}/cuadrante_proposals` responde 403.

Y **prod**, con el ruleset vivo leído antes (como el 14-oct, por la API de firebaserules) y
guardada su copia aquí como `2026-10-xx-firestore-rules-prod-antes.rules`:

```bash
firebase deploy --only firestore:rules --project encodebiz-services
```

Las mismas tres comprobaciones contra prod, sin sesión. El rollback es redesplegar la copia.

**Qué cambia respecto a lo que hay en prod:** además de `signing_keys` y `signing_challenges`,
quedan cerradas al navegador `cuadrante_proposals`, `cuadrante_lotes`, `calendar_days` y las
`assistant_*`, a cualquier profundidad. Ningún cliente las lee: buscado en el panel, en la app
(`checkbiz360/lib`) y en las functions del SaaS el 2026-10-16, sin resultados. Las `assistant_*` y
`calendar_days` son de otros frentes (conector de asistentes, horario por tareas): **si su pase no
va con este, las reglas los cierran igual**, que es lo que esos frentes piden.

**Coste conocido de la regla:** cierra un documento cuyo id sea el nombre de una colección
cerrada. No hay ninguno.

### 3.2 Política TTL — opcional

Propuestas y lotes llevan `expiraEn` a treinta días. Sin política TTL de Firestore sobre ese campo,
cada subida nueva de un cliente barre lo vencido de ese cliente, que es suficiente. Si se quiere,
se configura una política TTL en `cuadrante_proposals.expiraEn` y `cuadrante_lotes.expiraEn`.

### 3.3 Índices — ninguno

Las consultas son por documento o por un solo campo (`expiraEn`), que Firestore indexa solo.

## 4. Panel (`encodebiz-front-saas`, Vercel)

- **Sin variables nuevas.** Todo va por `cuadrantes_handler`, cuya clave
  (`NEXT_BACKEND_URI_CUADRANTES_HANDLER`) está en uso en prod desde el 20-sep. No comprobado en
  Vercel desde aquí: si la lectura por modelo de la ficha del empleado funciona en prod, está.
- **El proxy cambia de allowlist** (`/plantilla` y `/lotes`): va en el código.
- **Lo que entra, por pantalla:**
  - Sucursal → «Horarios y festivos» → al final, acordeón «Cuadrante semanal de la plantilla» →
    «Importar cuadrante».
  - Empleado → «Subir un cuadrante»: la semana y «Descargar plantilla» (solo esa persona); al subir
    la plantilla se salta la pantalla de columnas.
  - Textos en es, en, pt, de y fr.
- La promoción va como siempre: `develop → staging → main` y Vercel despliega `main`.

## 5. Aceptación antes de subir (en staging)

Sobre una sucursal de pruebas, con dos o tres personas:

- [ ] Descargar la plantilla de la sucursal: una pestaña por persona, la portada, los ejemplos con
  ELIMINAR en gris.
- [ ] Rellenar dos personas, dejar una vacía, subir: dos listas, una sin cambios, los avisos con
  sentido.
- [ ] Una fila mal escrita (fecha sin año): esa persona bloqueada con el número de fila, la otra
  sigue.
- [ ] Confirmar: el avance, el resultado, y en la ficha de cada persona el horario de esa semana y
  sus tareas con dirección en la app.
- [ ] Subir el mismo fichero otra vez y confirmar: no se duplica ninguna tarea.
- [ ] Desde la ficha de una persona: descargar su plantilla, rellenarla, subirla, y que salte la
  pantalla de columnas.
- [ ] Subir el PDF de ServiSAD desde la ficha: la lectura por modelo sigue como antes.
- [ ] Un Excel que no sea la plantilla desde la sucursal: el error con su nombre.
- [ ] Limpiar lo creado (`cli/limpiar.cli.js` por persona, simula por defecto).

## 6. Abierto, no bloquea el pase

- **Decidido el 2026-10-16: la plantilla se queda en `merlin` para este pase.** No usa IA, pero
  comparte con la lectura por modelo todo lo que viene después de leer (revisión, propuesta,
  firma, aplicación), y moverla obliga a cambiar la ruta `/api/v1/gpt/cuadrantes` y la variable
  del proxy en Vercel. Si `merlin` se queda algún día solo con la IA, el módulo de cuadrantes
  entero se mueve a `checkinbiz` (dueño del calendario) en un cambio aparte.

- **Resubir una semana corregida retira lo que ya no está** desde el 2026-10-16 (`55ed15e`, sesión
  del conector de asistentes): las tareas de cuadrante de esa persona y semana que el fichero ya no
  trae se retiran antes de crear las nuevas, solo si no han empezado. Visto en staging el mismo
  día: JOSE reimportado, 31 retiradas y 31 creadas. Entra en este pase.
- **Lo que trae también `55ed15e`** (`POST /lotes/filas`, `GET /lotes/:id/excel`, red de totales
  por filas) es del conector de asistentes: su pase va con ese frente.
- **Lotes y propuestas abandonados** caducan a los treinta días (§3.2).
- **Leer el Excel plano de un ERP** con una columna de empleado: fuera de esta versión (TDR §9).

## 7. Orden de ejecución el día del pase

0. Rearmar `block-prod.sh` y comprobarlo con un comando inocuo.
1. Aceptación de §5 en staging, entera.
2. Reglas a dev (§3.1) y sus comprobaciones. *(Puede adelantarse a todo lo demás.)*
3. Leer y copiar el ruleset vivo de prod; reglas a prod; comprobaciones. *(Ídem, con autorización
   expresa.)*
4. `staging` de la API al día con `develop` (lleva la corrección de reglas y `qa/reglas`).
5. PR `staging → main` de la API; el CI despliega `merlin` y reinicia nginx.
6. Comprobar en prod: `GET /api/v1/gpt/cuadrantes/plantilla` sin token responde 401, no 404.
7. Panel: `develop → staging → main`; Vercel despliega.
8. En prod, con una sucursal de verdad y el visto bueno del cliente, o en la entidad de pruebas:
   descargar la plantilla y comprobar que trae a la gente de esa sucursal. No subir nada en una
   entidad de cliente sin que lo pida.

## 7b. Prueba en staging del 2026-10-16

| Prueba | Resultado |
|---|---|
| Plantilla de una persona (JOSE) desde su ficha, guardada con un programa que no es Excel | Primero «No se ha podido abrir el Excel»: `exceljs` no lee el XML con prefijo. Arreglado (`6065a62`) y leído entero: 31 trabajos |
| La misma, aprobada | 31 tareas con valla `rooftop`; el horario escrito **pero apagado** porque la ficha tenía «usar el horario de la sucursal». Arreglado (`8eceb33`): aprobar enciende el horario propio |
| Plantilla de sucursal con dos personas (JOSE y encodebiz), lote aprobado | 2 listas, 62 tareas creadas, 31 retiradas de la importación anterior de JOSE; las dos con su horario propio encendido |
| encodebiz con «horario por tareas» activado | 7 días generados de su semana, un turno por tarea; el horario semanal propio también se escribe y no se usa |
| Aviso de tolerancia de entrada | Sale en todas: el viaje de la primera tarea (18–20 min) pasa de los 15 de tolerancia. El fichero de prueba pone en «Viaje» el tiempo hasta la **siguiente** tarea; la plantilla lo entiende como el tiempo hasta **esa** tarea |

## 7b2. Funciones de Firebase que lleva este pase (horario por tareas, D11)

No las despliega el CI: van por nombre, `node scripts/desplegar.mjs --project encodebiz-services
--solo onTaskDay,weeklyFromTaskDays` desde `services/firebase_sdk`, con su `.env.encodebiz-services`.

- `onTaskDay` (ya existe del frente de horario por tareas): ahora además copia la semana activa
  a la plantilla propia de quien está en el modo.
- `weeklyFromTaskDays` (nueva, `onSchedule` 03:00 y 15:00 Madrid, 540 s): el cambio de semana del
  lunes. La primera versión recorría a todos los empleados y se cortaba por tiempo (504 dos veces
  en dev el 16-oct); la buena va por entidad con el índice de grupo de `calendar_days` y en dev
  terminó en 12 s (329 entidades, 20 personas en el modo, 14 plantillas escritas, 0 fallos).
  Sigue siendo una pasada sobre todas las entidades: cuando se haga
  [programadas-a-escala](../ingenieria/programadas-a-escala/README.md), entra en su reparto.

## 7c. Manual de clientes

Artículo nuevo el 2026-10-16, en los tres idiomas y sin commitear: `Clients/04-calendario-y-horarios/108-importar-el-cuadrante-semanal.md`
(EN `108-import-the-weekly-schedule`, PT `108-importar-a-escala-semanal`), con su fila en los tres
README. **Se publica junto con el pase**, no antes: describe pantallas que en producción aún no
existen. El párrafo de «Horario por tareas» solo vale cuando ese frente esté también en
producción; si su pase va después, ese párrafo se quita hasta entonces.

## 8. Registro de lo ejecutado

| Paso | Cuándo | Quién | Qué y resultado |
|---|---|---|---|
| Reglas a dev (§3.1) | 2026-10-16 | Claude, con el «ok» de Jose | Copia del ruleset vivo de dev antes de tocarlo: [2026-10-16-firestore-rules-dev-antes.rules](./2026-10-16-firestore-rules-dev-antes.rules) (desplegado ese mismo día a las 09:21 UTC por otra sesión, con el fallo de la raíz). `firebase deploy --only firestore:rules --project dev-encodebiz` desde `origin/develop` (`93c67ac`), fichero idéntico al probado con el emulador. Comprobado en dev sin sesión, con una entidad inexistente y consultas que no devuelven documentos: `calendar` y `employees` abiertas (404 por documento inexistente; 200 en consulta de grupo); `cuadrante_proposals`, `cuadrante_lotes`, `calendar_days` y `signing_keys` 403 por documento, y las tres primeras 403 en consulta de grupo. |


---

## Anexo. Lo demás que hay en `staging` y no en `main` de la API (2026-10-16)

No es de este pase y no se ha revisado aquí; está para que nada se quede atrás sin que nadie lo
vea. Sale de `git log --first-parent origin/main..origin/staging`:

- Horario por tareas (fase 1), con la migración `037_horario_por_tareas.sql` y `calendar_days`.
- Conector de Claude y ChatGPT (fase 1, acceso), con las colecciones `assistant_*`.
- CRM: acciones planificadas, actividad y lista por contacto, agenda diaria, nicho de
  mantenimiento, conector de claude.ai, señales de la PLACSP. El CRM base está en prod desde el
  14-oct (PR #147, migraciones 031–033); lo posterior hay que contrastarlo.
- Inventario: aviso a la persona e historial de cada material; material hacia tarea, persona o
  sucursal (ADR-009) con la migración `034_inventario_cuentas_destino.sql`, que **quedó fuera** del
  pase del 14-oct.
- Avisos: el último idioma es inglés.
- Script del destino de los apuntes espejados.
- Reglas para consultas de grupo (el arreglo del 14-oct ya está desplegado en prod; en `main` falta
  lo que llegó después).

Cada frente debería tener su propio registro; si no lo tiene, este anexo es el recordatorio.

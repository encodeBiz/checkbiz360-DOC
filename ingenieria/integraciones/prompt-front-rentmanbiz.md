# Front — RentmanBiz completo (contrato + prompt)

> Sustituye a `prompt-backoffice-conexion.md`, que cubría sólo el alta y la conexión.
> Todo lo de aquí está **desplegado en desarrollo** y verificado.
> Base: `{NEXT_BACKEND_URI_ADDONS_HANDLER}/rentmanbiz` · autenticación: Firebase ID token.

---

## 1. El contrato, endpoint por endpoint

Todos responden `{ok: false, error, …}` en el error, con el código en `error`.

### Conexión

| Llamada | Devuelve | Errores propios |
|---|---|---|
| `GET /connection/{entityId}` | `{ok, connection}` · `connection: null` si no está activado | — |
| `POST /activate` `{entityId}` | `{ok, connection}` | **409** `service_not_active` + `requiredService` |
| `POST /connect` `{entityId, token}` | `{ok, connection}` | **400** `invalid_credentials` + `detail` · **409** `addon_not_active` |
| `POST /disconnect` `{entityId}` | `{ok, connection}` | — |
| `POST /active` `{entityId, active}` | `{ok, connection}` | **409** `service_not_active` |
| `GET /test-connection/{entityId}` | `{ok, error?}` | **404** `integration_not_configured` |

```jsonc
// connection
{
  "addonId": "rentmanbiz", "entityId": "…",
  "active": true,
  "status": "disconnected | connected | error",
  "tokenRef": "*****Jy7Pts",   // lo ÚNICO que vuelve del secreto
  "lastError": null,
  "activatedAt": "…", "connectedAt": "…"
}
```

### Catálogo e importación

| Llamada | Devuelve |
|---|---|
| `GET /catalogue/preview/{entityId}` | `{ok, preview}` — qué pasaría, **sin escribir nada** |
| `POST /catalogue/import` `{entityId, dryRun?, warehouseTasks?}` | `{ok, result}` |
| `GET /pending/{entityId}` | `{ok, summary, items}` |
| `POST /pending/crew/complete` `{entityId, rentmanCrewId, email}` | `{ok, employeeId}` |
| `GET /activity/{entityId}?limit=50` | `{ok, events}` |

```jsonc
// preview
{ "window": {"from":"2026-07-23","to":"2026-11-20"},
  "projects": {"total":45,"candidates":16,"discarded":{"noCrew":29,"outOfWindow":0,"noDates":0}},
  "sites": {"fromProjects":16,"warehouses":3,"withoutCoordinates":16,"sample":[…],"warehouseSample":[…]},
  "people": {"total":23,"importable":1,"withoutEmail":22,"alreadyMapped":0,"withoutEmailSample":[…]},
  "assignments": {"total":167,"estimatedTasks":167},
  "notes": ["…"] }

// import result
{ "dryRun": true,
  "people": {"total":23,"matched":0,"created":1,"pending":22},
  "sites": {"warehouses":3,"projects":16,"created":0,"pending":19},
  "responsibilities": {"created":0,"existing":0},
  "tasks": {"planned":123,"created":0},
  "notes": ["…"] }

// pending
{ "summary": {"total":41,"byKind":{"crew":22,"project":16,"warehouse":3,…},
              "byReason":{"missing_email":22,"missing_geofence":19}},
  "items": [{"kind":"crew","rentmanId":226,"name":"Amy Murray","checkbizId":"abc123",
             "status":"pending","pendingReasons":["missing_email"],"detail":"…"}] }
```

### Horas — respuestas reales (capturadas del servicio, no inventadas)

```jsonc
// GET /hours/summary/{entityId}
{ "ok": true, "entityId": "…",
  "summary": {"pending":0,"synced":2,"failed":0,"skipped":0,"diverged":1},
  "lastPushedAt": "2026-08-21T09:05:39.524Z",
  // fracción 0–1 sobre empleados ACTIVOS. Con 0 activos vale 1: no falta nadie.
  "coverage": {"mappedEmployees":0,"activeEmployees":3,"ratio":0} }

// GET /hours/entries/{entityId}?limit=2
{ "ok": true,
  "range": {"from":"…","to":"…"},
  "totals": {"count":3,"netHours":23,"breakHours":1,"grossHours":24},
  "entries": [{"checkinId":"…","employeeId":"…","employeeName":"Jose Manuel Acevedo",
               "branchId":"…","start":"…","end":"…","timeZone":"Europe/Madrid",
               "netHours":8.5,"breakMinutes":30,"status":"diverged","rentmanId":103}] }

// GET /hours/divergences/{entityId}
{ "ok": true, "count": 1,
  "divergences": [{"checkinId":"…","employeeName":"Jose Manuel Acevedo","date":"…",
    "timeZone":"Europe/Madrid",
    "ours":   {"start":"…","end":"…","netHours":8.5,"breakMinutes":30},
    "theirs": {"start":"…","end":"…","netHours":7.5,"breakMinutes":30},
    "detail": "editado en Rentman: fin 17:00 ≠ 18:00; duración 27000s ≠ 30600s",
    "detectedAt": "…"}] }
// `theirs` es null en divergencias anteriores a agosto de 2026.

// GET /activity/{entityId}?limit=3   — OJO: el campo es `direction`, NO `type`
{ "ok": true,
  "events": [{"direction":"import_branch","sourceId":"80","status":"success",
              "detail":"Presentación en vivo banda Soultrain","rentmanId":null,"at":"…"}] }
// direction: push_hours · hours_divergence · pull_crew · pull_projects · pull_warehouses
//            pull_assignments · import_employee · import_branch · import_responsibility
//            import_task · webhook
// status:    success · failed · skipped
```

### Horas

| Llamada | Devuelve | Errores |
|---|---|---|
| `GET /hours/summary/{entityId}` | `{ok, summary, lastPushedAt}` | — |
| `GET /hours/entries/{entityId}?from=&to=&limit=` | `{ok, range, totals, entries}` — jornadas imputadas **con nombre de empleado** y total en horas. Por defecto, 30 días | **400** `invalid_range` |
| `POST /hours/sync-now` `{entityId}` | `{ok, result}` | **429** `sync_in_progress` + `retryAfterSeconds` |
| `GET /hours/divergences/{entityId}` | `{ok, count, divergences}` | — |

### Emparejamientos

`GET /crew/{entityId}` · `GET /mappings/{entityId}` · `POST /mappings` `{entityId, rentmanCrewId, employeeId}`

---

## PROMPT

Implementa la pantalla de **RentmanBiz** en el backoffice. Es el primer add-on del
catálogo y habrá más, así que **nada específico de Rentman se cablea**: el `addonId`, los
textos y las capacidades salen del documento `addons/rentmanbiz` de Firestore (bilingüe en
`es`, `en`, `fr`, `pt`, `de`).

### Lo que tiene que entender quien lo implemente

El add-on conecta checkbiz con Rentman, el software con el que las empresas de eventos
planifican montajes. Trae de allí a la gente, los sitios y el trabajo; y devuelve las
horas fichadas. Tres ideas gobiernan la interfaz:

**Activar y conectar no son lo mismo.** Activar da de alta; conectar entrega la
credencial. El cliente pasará un rato en medio, y ahí es donde hay que acompañarle.

**Nada llega completo, y eso no es un error.** Rentman no da coordenadas y casi nadie
tiene correo allí. Lo incompleto se importa igualmente, marcado como pendiente y sin poder
hacer daño: los centros nacen **inactivos** —una geocerca deducida de una dirección no
puede validar fichajes— y las personas sin correo nacen **inactivas y sin acceso**, porque
se factura por empleado activo y cobrar por alguien que no puede trabajar es un error de
cuenta, no de software.

**El add-on avisa y te lleva; se arregla en la pantalla del producto.** El listado de
pendientes no es un formulario: es una lista con enlace directo a la ficha del empleado o
del centro, que es la pantalla que ya sabe validar.

### Pantalla 1 — Tarjeta en el catálogo

De `GET /connection`, cinco estados: **bloqueado** (`requires` sin contratar → interruptor
deshabilitado y el motivo), **sin activar** (`connection: null`), **activado sin conectar**
(ámbar + botón Conectar), **conectado** (verde, con `tokenRef` y fecha) y **con error**
(rojo con `lastError`). Muestra siempre el vendor además del nombre: RentmanBiz es nuestro,
Rentman es de ellos.

### Pantalla 2 — Asistente de conexión

Pasos de `steps` del catálogo. El campo del secreto se construye desde
`connection.fields`: password, sin autocompletado, y **jamás en logs, estado global ni
URL**. Al conectar, un **400** significa credencial mala de verdad —el servidor la valida
contra Rentman antes de guardarla—: enseña `detail` y deja reintentar sin salir.

### Pantalla 3 — Importación

Aquí está lo nuevo, y el orden importa:

1. **Vista previa primero, siempre.** `GET /catalogue/preview` no escribe nada y responde
   la pregunta que el cliente se hace: *"¿qué me va a meter esto?"*. Enséñalo en claro:
   cuántos montajes serán centro y cuántos se descartan **por no tener gente asignada**
   (que es la regla, no el tipo de proyecto), cuántos nacerán sin geocerca, cuánta gente no
   tiene correo, cuántas tareas saldrán.
2. **Simular antes de escribir.** El botón principal llama a `import` con `dryRun: true`.
   El resultado se pinta igual que la ejecución real. Sólo entonces se ofrece **Importar de
   verdad**, con una confirmación que diga qué se va a crear.
3. **Opción "tareas de almacén"**, apagada. Explica qué hace: los alquileres y las ventas
   no llevan gente a ningún sitio, pero alguien prepara el material antes de que el cliente
   lo recoja y lo revisa cuando vuelve. Genera esas tareas, sin asignar, en el almacén que
   corresponde. Avisa de que pueden ser muchas.

### Pantalla 4 — Pendientes (lo que más se va a usar)

`GET /pending`. Agrupado por tipo, cada línea con su motivo traducido y **enlace directo a
la ficha**:

| Motivo | Qué decirle | A dónde lleva |
|---|---|---|
| `missing_email` | "Sin correo: no puede acceder ni fichar" | Ficha del empleado |
| `missing_geofence` | "Falta confirmar la geocerca. El centro está inactivo" | Ficha del centro |
| `missing_address` | "Rentman no da dirección para este montaje" | Ficha del centro |
| `missing_rate` | "Sin coste por hora: sus jornadas saldrán a cero en los informes" | Ficha del centro |

El indicador del catálogo se enciende con `summary.total > 0` y **en cero no muestra
nada**: un aviso permanente deja de leerse en una semana.

### Pantalla 5 — Horas y actividad

Cuatro cifras de `hours/summary`: jornadas imputadas, horas del periodo, cobertura de
emparejamiento —si no llega al 100%, es un aviso, no un dato— y divergencias abiertas.

**El panel de divergencias es lo más valioso de esta pantalla.** Una fila por jornada que
alguien editó en Rentman, con **nuestras horas frente a las suyas** y el `detail` en
lenguaje llano. Deja claro que el fichaje **no** se ha modificado: checkbiz es la autoridad
del registro horario. En cero, vacío en positivo: *"Nadie ha tocado las horas imputadas"*.

Y **Sincronizar ahora** (`hours/sync-now`), que evita esperar al ciclo de 15 minutos justo
después de conectar. Un **429** con `retryAfterSeconds` no es un error: deshabilita el
botón ese rato y dilo con naturalidad. Ojo: `pushed: 0` tampoco es un fallo — puede que no
haya jornadas cerradas o nadie emparejado. Explícalo en vez de pintar rojo.

`GET /activity` alimenta la lista de eventos recientes. Sale de nuestra base de datos, así
que se puede consultar aunque Rentman esté caído.

### Detalles que marcan la diferencia

- **El front nunca escribe el documento de activación.** Cifrar es del servidor.
- **Esqueletos mientras carga**, nunca ceros: "0 divergencias" es una afirmación.
- **Enseña el error real** de la API; en estos flujos el error *es* la información.
- **Idioma del usuario**, con `es` de reserva.
- No inventes capacidades ni textos: si no está en el catálogo, no se pinta.

### Sobre el tile de horas

Sale de `GET /hours/entries`: `totals.netHours` es **la cifra que el cliente compara con su
informe legal**, así que no la recalcules en el front ni sumes lo que devuelva `entries`
—esa lista viene recortada por `limit`, el total no—. Sólo cuenta lo realmente imputado:
lo pendiente o rechazado no son horas del periodo.

Cada entrada trae ya el nombre del empleado resuelto: no hace falta cruzarlo.

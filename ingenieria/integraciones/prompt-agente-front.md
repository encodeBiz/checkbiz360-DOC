# Prompt para el agente de front — pantallas de Integraciones (add-ons)

> Copia lo de abajo tal cual a tu agente de front. Está escrito para el diseño que ya
> tenéis (página *Integrations* con pestañas, cajón de catálogo con interruptores,
> tarjeta de cabecera, tiles de métricas, lista de eventos y ajustes rápidos), pero con
> el contenido que corresponde de verdad al primer add-on: **Rentman**.
>
> Ojo: la maqueta actual es un **placeholder de un POS** (tickets, importe, sucursales).
> Nada de eso aplica. Se conserva la **estructura**, se cambia el **contenido**.

---

## PROMPT

Vas a implementar las pantallas de **Integraciones (add-ons)** de checkbiz360. Respeta el
layout que ya existe en la maqueta; lo que cambia es qué datos se pintan.

### Contexto que necesitas entender antes de escribir código

Un add-on es un módulo activable y de pago que conecta checkbiz con un sistema de
terceros. El primero es **Rentman** (rentman.io), el software con el que las empresas de
eventos y AV planifican proyectos y equipos. Lo que hace el add-on: **cuando un
trabajador cierra su jornada en checkbiz, las horas se imputan solas en Rentman**.

Hay una regla de negocio que la interfaz debe transmitir sin ambigüedad: **checkbiz es
la autoridad sobre las horas**, porque es el registro que responde ante la ley. Si
alguien edita en Rentman unas horas ya imputadas, el fichaje **no** se toca: se detecta,
se marca como *divergencia* y se avisa. La pantalla no debe sugerir en ningún momento
que Rentman puede corregir el fichaje, ni ofrecer editar horas desde aquí.

### De dónde salen los datos

**1. El catálogo — Firestore, colección `addons`** (léela directo, como ya lees
`service`). Un documento por add-on. Todo el texto es bilingüe `{es, en}`: nombre,
`description` (una línea), `about` (el párrafo largo), `featuredList` (bullets),
`target` (bloques de valor `{title, description}`), `steps` (asistente de conexión),
`connection` (qué credencial pide) y `capabilities` (qué sabe hacer, cada una con
`status`: `available` o `coming_soon`).

**No hardcodees copy**: todo eso viene del documento. Hoy solo existe `addons/rentmanbiz`;
el catálogo tiene que renderizar N.

**2. El estado de conexión del cliente — Firestore**:
`entities/{entityId}/integrations/rentman` → `{ enabled, updatedAt }`. El token está
cifrado y **no se lee nunca desde el front**.

**3. La API — `/api/v1/rentmanbiz`, con Firebase ID token** (`Authorization: Bearer …`):

| Llamada | Devuelve |
|---|---|
| `POST /credentials` `{entityId, token}` | `{ok:true}` — guarda el token cifrado |
| `GET /test-connection/{entityId}` | `{ok:boolean, error?}` |
| `GET /crew/{entityId}` | `{ok, fetched, unmapped:[{id, displayName, email, …}]}` |
| `GET /mappings/{entityId}` | `{ok, mappings:[{rentmanCrewId, employeeId, …}]}` |
| `POST /mappings` `{entityId, rentmanCrewId, employeeId}` | `{ok:true}` |
| `GET /hours/summary/{entityId}` | `{ok, summary:{pending,synced,failed,skipped,diverged}, lastPushedAt}` |
| `GET /hours/divergences/{entityId}` | `{ok, count, divergences:[…]}` |

Cada divergencia trae `checkinId`, `employeeId`, `rentmanId`, `start`, `end`,
`grossSeconds`, `breakSeconds`, `netSeconds`, `detail` (qué cambió, en texto) y
`lastCheckedAt`.

### Pantalla 1 — Catálogo de add-ons (el cajón lateral)

Lista `addons` ordenada por `order`. Cada fila: inicial en cuadrado, `name`,
`description` y un interruptor.

**El interruptor no es un interruptor.** Activar requiere credencial, así que al
encenderlo se abre el **asistente de conexión** (pantalla 2), y solo queda encendido
cuando la conexión funciona. Apagarlo sí es inmediato: pone `enabled: false`, la
sincronización se detiene y no se borra nada — si se reactiva, sigue donde estaba.
Pídele confirmación explicando exactamente eso.

Un add-on con `status: "coming_soon"` se muestra en gris, sin interruptor. Con
`status: "beta"`, con una etiqueta *Beta* junto al nombre. Si `requires` incluye un
servicio que la entidad no tiene contratado, se muestra bloqueado explicando por qué.

El contador de abajo cuenta los que tiene la entidad activos, no los del catálogo.

### Pantalla 2 — Conectar (asistente)

Cuatro pasos, y los textos salen de `steps` del documento:

1. **Pegar el token.** Campo tipo password, con la ayuda de `connection.fields[].help`
   (dónde sacarlo en Rentman). Al guardar: `POST /credentials`.
2. **Probar la conexión.** `GET /test-connection/{entityId}`. Si falla, muestra el
   `error` tal cual y deja volver al paso anterior; no des por buena una conexión rota.
3. **Emparejar trabajadores.** `GET /crew/{entityId}` da la plantilla de Rentman y
   quién está sin emparejar; `GET /mappings` los ya emparejados. Dos columnas y un
   selector por fila; `POST /mappings` por cada pareja. Propón por coincidencia de
   correo, pero que lo confirme una persona. **Deja claro el efecto**: a quien no esté
   emparejado no se le imputan horas.
4. **Listo.** Explica qué va a pasar a partir de ahora, sin prometer inmediatez: la
   primera imputación llega en el siguiente ciclo de sincronización (15 min).

*(Nota para el equipo: el endpoint de crew hoy es un stub —trae la plantilla y dice
quién no está mapeado, pero no crea empleados. El paso 3 se diseña completo igualmente.)*

### Pantalla 3 — Detalle del add-on (la pestaña)

Conserva la estructura de la maqueta y cambia el contenido.

**Cabecera**: nombre, `description`, estado real y botón *Configurar*. El estado sale de
combinar `enabled` con `summary`: sin credencial → *Sin conectar*; con divergencias o
fallos → *Con avisos*; si no → *Activo*. Y sustituye "syncs every 5 min" por lo que es:
*sincroniza cada 15 minutos*.

**Los cuatro tiles** — fuera tickets e importe, que son del placeholder. Los que
significan algo aquí:

1. **Jornadas imputadas** — `summary.synced`, con "últimos 7 días" debajo.
2. **Horas imputadas** — suma de `netSeconds` del periodo, en horas. Es la cifra que el
   cliente reconoce, y coincide con su informe legal: dilo en el subtítulo.
3. **Cobertura de mapeo** — emparejados / total de empleados. Si no es el 100%, esto es
   un aviso, no un dato: hay gente cuyas horas no están llegando a Rentman.
4. **Divergencias abiertas** — `summary.diverged`. En cero es un tile tranquilo; con
   uno o más, en color de alerta y clicable.

**Panel principal — Divergencias** (ocupa el sitio de "Sync events"). Es lo más valioso
de esta pantalla y no existe en la maqueta. Una fila por jornada tocada en Rentman:
empleado, fecha, **nuestras horas frente a las suyas**, y el `detail` en lenguaje llano
("fin 18:30 ≠ 17:00"). Deja claro que el fichaje de checkbiz **no** se ha modificado.
Cuando no hay ninguna, un vacío en positivo: *"Nadie ha tocado las horas imputadas"*.

**Panel secundario — Estado de la sincronización**, con lo que de verdad ayuda a
diagnosticar: cuándo fue la última imputación (`lastPushedAt`, en relativo), cuántas
jornadas hay en cola (`pending`), cuántas fallaron (`failed`, con reintento automático)
y cuántas rechazó Rentman (`skipped`, que **no** se reintentan — normalmente porque ya
había horas o una ausencia en ese periodo; explícalo, es la duda número uno).

**Panel de eventos y tareas** — esto no está en la maqueta y tiene que estar, porque es
la mitad del producto. Rentman planifica **eventos** (proyectos) y **asignaciones**, y de
ahí saldrán los centros de trabajo con geocerca y las tareas de cada montaje.

Hoy esas dos capacidades vienen como `coming_soon` en el catálogo, así que el panel se
pinta **en estado anticipado**: el título, una frase de qué hará y la etiqueta
*Próximamente*. No lo escondas — es lo que explica por qué esta integración vale lo que
vale, y el cliente que la está evaluando necesita verlo. Cuando esas capacidades pasen a
`available`, el mismo panel se llena sin rediseñarlo:

- **Eventos sincronizados** — cuántos proyectos de Rentman existen como centro de trabajo,
  cuántos están activos ahora mismo y **cuántos están "requiere configuración"** por haber
  llegado sin coordenadas. Ese último número es accionable: sin geocerca no se puede fichar
  en ese evento.
- **Asignaciones convertidas en tareas** — cuántas personas asignadas y cuántas tareas
  generadas para los próximos días, con enlace al módulo de Tareas. Ojo con el matiz al
  redactar: **el módulo de Tareas ya existe y funciona**; lo que aporta el add-on es que
  esas tareas se generen solas desde las asignaciones de Rentman. No des a entender que
  las tareas son una funcionalidad futura, porque no lo son.

Cuando llegue, el ciclo que hay que dejar contado en la interfaz es este, porque es el
argumento entero: *el trabajador ve el evento al que va → ficha dentro de la geocerca de
ese evento → ejecuta las tareas de su función → al cerrar, las horas vuelven a Rentman
imputadas a ese proyecto.* Si la pantalla solo habla de horas, se está vendiendo un cuarto
de lo que hace.

**Capacidades**: pinta `capabilities` como lista, las `available` con check y las
`coming_soon` en gris con etiqueta *Próximamente*. Es honesto y vende la hoja de ruta.
No inventes capacidades que no estén en el documento: si aparece una nueva, aparecerá ahí.

Fuera de esta pantalla: los "Quick settings" del placeholder (importar tickets anulados,
cruzar ventas). No existen en este add-on. Si necesitas un ajuste, el único que tiene
sentido hoy es pausar la sincronización, y ya lo cubre el interruptor del catálogo.

### Detalles que marcan la diferencia

- **El token no se muestra jamás**, ni enmascarado con los últimos caracteres. Para
  cambiarlo, se pega uno nuevo.
- **Nada de números inventados mientras carga**: esqueletos, no ceros. Un cero en
  "divergencias" es una afirmación.
- **Diferencia "no hay datos" de "no está conectado"**. Un cliente recién conectado y
  sin jornadas cerradas no está roto: no ha cerrado ninguna jornada todavía. Dilo así.
- **Textos siempre del documento** (`about`, `featuredList`, `target`, `steps`), en el
  idioma del usuario, con `es` de reserva.
- **Toda la API responde `{ok:false, error}`**: enseña el error, no un genérico.

### Lo que aún no te da la API (dilo, no lo inventes)

No hay endpoint que liste las últimas jornadas imputadas una a una, ni el total de horas
del periodo: hoy solo hay recuentos por estado y el detalle de divergencias. Y **no existe
todavía nada de eventos ni de tareas** en la API: esa capa está diseñada pero no
implementada, así que el panel correspondiente se maqueta en estado *Próximamente* y no se
inventan datos.

Si el diseño los pide —y el tile de horas los pide—, pídenoslos y los añadimos al
servicio. Lo que no debe hacer el front es estimar cifras: en una pantalla que habla del
registro horario, un número aproximado es peor que un hueco.

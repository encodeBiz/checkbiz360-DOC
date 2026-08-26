# RentmanBiz — qué es cada cosa, y cómo se rellena lo obligatorio

Rentman tiene mil objetos y casi ninguno significa lo que parece por el nombre. Este
documento fija qué traemos, qué ignoramos y de dónde sale cada dato que checkbiz exige.
Verificado contra la cuenta sandbox el 2026-08-21.

---

## 1. El diccionario

| En Rentman | Qué es de verdad | En checkbiz |
|---|---|---|
| `project` **con `projectcrew`** | El montaje: gente trabajando en un sitio y unas fechas | **Centro de trabajo temporal**, con geocerca |
| `project` **sin gente** (Sale, Alquiler en seco, Transferproject…) | Operación comercial o logística: nadie pisa un sitio | **Nada.** No se importa |
| `contacts` referenciado en `project.location` | El **venue**: dónde ocurre el evento | La dirección del centro |
| `contacts` referenciado en `project.customer` | El **cliente** que paga | Atributo del centro (la estructura de Clientes es Fase 2) |
| `stocklocations` | El **almacén** propio: la base donde vive el material | **Centro de trabajo permanente**, si allí se ficha |
| `crew` | La persona | **Empleado** |
| `projectcrew` | La asignación: quién, con qué función, en qué periodo | **Asignación al centro** y origen de las **tareas** |
| `projectfunctions` | La plaza dentro del proyecto (técnico de luces, rigger) | El **`job`** de esa asignación — **no** el rol de permisos |
| `appointments` | Agenda personal: dentista, vacaciones, una visita | **Nada.** Se parece al calendario y a las ausencias, no a las tareas |
| `timeregistration` | El fichaje | Lo único que **nosotros escribimos** |
| `timeregistrationactivity` | Desglose de coste por función | Fuera de alcance |
| Material, presupuestos, facturas, subproyectos | La otra mitad de Rentman | No se leen ni se tocan |

Dos avisos que ya nos habrían costado un rediseño:

- **`appointments` no son tareas.** En el sandbox son "Dentist Brian", "Brian Holiday" y
  "Visit Ahoy on location": es la agenda de cada persona. Convertirlas en tareas de un
  montaje sería inventarse trabajo que nadie ha planificado.
- **El almacén no es un proyecto.** Es `stocklocations`, con dirección postal fija y
  `type: "plannable"`. Y es probablemente el centro **más** valioso de todos: la gente que
  prepara el material ficha ahí a diario, no una semana al año como en un venue.

## 1bis. Qué es un "proyecto" en Rentman (y por qué confunde)

**Rentman no tiene un objeto "evento".** Su unidad de trabajo se llama `project` y sirve
para todo lo que factura: un montaje de concierto, una venta de material, un alquiler en
seco que el cliente recoge en el almacén, un traspaso interno. Lo que los distingue es su
`project_type` —Production, Band, Sale, Alquiler en seco, Internal rental…— y esos tipos
**los configura cada cuenta**, así que ni sus nombres ni sus ids son universales.

Por eso "proyecto de Rentman" no equivale a "centro de trabajo": la mitad de ellos no son
un sitio donde nadie va. En la cuenta de pruebas, de 44 proyectos, 28 no tienen a nadie
asignado.

**Nuestros centros de trabajo son dos cosas distintas:**

| Centro en checkbiz | Qué es en Rentman | Naturaleza |
|---|---|---|
| El montaje | `project` **con `projectcrew`** | Temporal: existe mientras dura el evento |
| El almacén | `stocklocations` | Permanente: la base, con dirección fija |

Y lo que decide que un proyecto sea centro **no es su tipo, sino que tenga gente
asignada**. Si nadie va, nadie ficha allí. Esa regla no hay que mantenerla: se cumple sola
en cualquier cuenta, se llamen como se llamen sus tipos de proyecto.

Los `appointments`, pese al nombre, no son eventos: son la agenda personal de cada uno
—dentista, vacaciones, una visita—.

## 2. La regla de qué se importa

**Un proyecto se convierte en centro de trabajo solo si tiene `projectcrew`.** No por su
tipo: los tipos son configurables por cuenta y cablearlos garantiza que el segundo cliente
rompe. Si nadie está asignado, nadie va a fichar allí.

Encima, ventana temporal: solo proyectos cuyo `planperiod` caiga entre un mes atrás y tres
meses adelante. En el sandbox eso descarta solo siete proyectos con fechas de 1987-1990.

Y una sola dirección: **del catálogo de Rentman hacia checkbiz**. Lo único que devolvemos
son las horas, que es lo que ellos no tienen y nosotros sí.

## 3. Cómo se rellena lo que checkbiz exige

### Centro de trabajo (`Branch`)

| Campo obligatorio | De dónde sale |
|---|---|
| `name` | Nombre del proyecto (+ `number` si se repite) · nombre del almacén |
| `address.street/city/country` | El contacto-venue (`visit_street`, `visit_city`) · el `stocklocation` (`street` + `house_number` + `postal_code` + `city`) |
| `address.geo.lat/lng` | **Geocodificador propio.** Rentman NO da coordenadas: los 44 contactos de la cuenta tienen `latitude: 0` |
| `address.timeZone` | El mismo geocodificador, que la resuelve desde las coordenadas |
| `status` | Nace **`inactive`** hasta que una persona confirme la geocerca |
| `entityId` | El tenant que activó el add-on |
| `advance` (descanso, horarios) | **Rentman no lo tiene.** Se hereda del criterio de la entidad o se ajusta a mano |

El geocodificador ya existe y lo usa el front (`geocodeGoogle`): recibe una dirección y
devuelve `lat`, `lng`, `timeZone` y la dirección normalizada. Resuelve de una vez las dos
cosas que Rentman no da.

**Por qué nace inactivo:** la geocerca decide si un fichaje vale. Un punto deducido de
"Old St, London" puede dejar a alguien sin poder fichar, o validarle a tres calles. Se
propone el punto, lo confirma una persona, y hasta entonces el centro existe pero no
opera. La sincronización no se bloquea por ello.

### Empleado (`Employee`)

| Campo obligatorio | De dónde sale |
|---|---|
| `fullName` | `crew.displayname` |
| `email` | `crew.email` — **si no lo hay, no se crea el empleado** |
| `role` | `collaborator` **siempre**: nadie llega con permisos por estar en un montaje |
| `status` | `active` si el crew está activo; si no, `inactive` |
| `entityId` | El tenant |
| `branchId[]` | Los centros de sus asignaciones |
| `enableRemoteWork` | `false`: en eventos se ficha en el sitio |
| Responsabilidad por centro | `worker`, con `job` = nombre de la `projectfunction` |

**El correo es el cuello de botella real.** En el sandbox, de 23 personas **una** tiene
email. Y en checkbiz el correo es el acceso del empleado. Así que la mayoría de una
plantilla de Rentman no se puede convertir en empleado: se listan aparte, visibles, para
que el cliente los complete. Un empleado con un correo inventado es peor que un hueco.

### Permisos y coste: los dos valores por defecto que hay que entender

**Permisos — todo el mundo entra como `worker`, y no se hereda nada.** La "función" de
Rentman (Stagehand, rigger, técnico de luces) es un **oficio**, no un nivel de permisos.
Que alguien monte luces en un evento no puede convertirlo en supervisor de un centro de
trabajo, y confundir ambas cosas es regalar accesos a datos de terceros. Así que la
responsabilidad importada es siempre trabajador, y subir a alguien es un gesto manual y
consciente de un administrador.

**Coste — se importa, no se asume cero.** La plaza de proyecto declara su coste por hora
en `costs_variable` (en la cuenta de pruebas, Stagehand = 15 €/h), y eso es lo que se
guarda como precio del puesto. Ojo con no coger `price_rate`, que es lo que se le **cobra
al cliente**: mezclarlos metería el margen dentro del coste de personal.

Cuando Rentman no lo declara, **no se pone 0 en silencio**: se marca como pendiente
(`missing_rate`). Un cero silencioso no es un dato que falta, es un dato falso — y
arrastra hasta el informe de costes y las métricas de eficiencia, donde nadie va a
sospechar de él.

### Tareas

Salen de `projectcrew`: el título de la función (`projectfunction.name`) y el proyecto, el
periodo de `planperiod_start/end`, asignadas a ese empleado en el centro de ese proyecto.
El módulo de Tareas ya existe; lo que falta es el puente que las genere.

## 4. Lo que Rentman no puede resolver nunca

Dos datos obligatorios nuestros que no existen en su modelo, y que hay que resolver
fuera de la sincronización:

1. **El descanso y los horarios del centro.** Determinan las horas netas que luego se
   imputan y las que se certifican. Se heredan de la política de la entidad.
2. **El radio de la geocerca.** Es una decisión de control, no un dato importable.

Que la sincronización no los invente es parte del diseño: los deja marcados como
"requiere configuración" y sigue con lo demás.

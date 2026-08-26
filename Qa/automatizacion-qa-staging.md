# QA — Automatización en staging (CheckBiz360)

> Cómo vamos a automatizar la regresión de CheckBiz360 sobre el entorno de desarrollo,
> qué se queda en manos de personas y en qué orden lo hacemos.
>
> Documento de acuerdo entre desarrollo y QA. Complementa a
> [task-module-qa-plan.md](./task-module-qa-plan.md) y al plan de estructura QA
> —usuarios, dispositivos y Fase 1— que mantiene QA.
>
> Fecha: 2026-08-26 · Estado: propuesta pendiente de una decisión (§8)

---

## 1. La conclusión, en corto

De la Fase 1 del plan de QA —crear las dos empresas, los seis usuarios, las cuatro
sucursales y comprobar que los permisos son los que deben ser— **prácticamente todo se
puede ejecutar solo**. De los ~41 puntos de la checklist, unos 37 no necesitan que nadie
toque una pantalla. Los cuatro que faltan no son un problema de automatización: son un
comportamiento del backend que hoy no coincide con lo que el plan de QA da por supuesto
(§5.1).

Más allá de la Fase 1, la automatización llega entera a los permisos de tareas y a la
geocerca de los fichajes, y llega a medias a todo lo que depende de la hora. Lo que se
queda para personas es el móvil de verdad: GPS, biometría, notificaciones push y lo
visual del panel.

El resultado práctico es que la regresión de estructura y permisos deja de repetirse a
mano en cada entrega, y los dispositivos de QA se dedican solo a lo que únicamente un
móvil puede demostrar.

---

## 2. Dónde se ejecuta

Todo esto vive en **el entorno de desarrollo**, nunca en producción. Los dos entornos
comparten servidor y sus nombres se parecen mucho, así que conviene tener delante los de
desarrollo:

- Borde de staging: `http://141.95.47.135:8080` (sin TLS, es el entorno de pruebas).
- Proyecto Firebase: **`dev-encodebiz`**.
- Base de datos: **`encodebiz_staging`**.
- Rutas relevantes: `/api/v1/tasks`, `/api/v1/checkinbiz/checklogs`,
  `/api/v1/checkinbiz/employees`, `/api/v1/checkinbiz/calendar`, `/api/v1/documents`,
  `/api/v1/billing`.

La suite corre **dentro del propio servidor**, como un contenedor más del stack de
desarrollo, sin puerto expuesto. Eso le da dos cosas: las credenciales del proyecto de
desarrollo ya están ahí —no hay que sacar ningún secreto del servidor— y habla con los
servicios por la red interna, saltándose el nginx de staging.

Y una guarda que no se negocia: **si el proyecto Firebase no es `dev-encodebiz`, la
siembra aborta antes de escribir nada**. Cualquier script que borre datos simula por
defecto y solo actúa con `--apply`.

### Aviso: el plan de tareas vigente apunta a una URL obsoleta

`task-module-qa-plan.md` §3 indica que las tareas se prueban contra la Cloud Function
`apiV100-firebaseEntryHttp-checkinbiz-tasksHandler`. Ya no es así: el módulo de tareas
está desplegado en contenedor y el panel llama a `/api/v1/tasks` tanto en desarrollo como
en producción. Hay que corregir ese apartado del plan.

---

## 3. Lo que se automatiza

### 3.1 La estructura entera (Fase 1 del plan de QA)

Un solo comando deja el entorno tal y como lo describen los capítulos 5 y 6 del plan de
QA: Empresa A y Empresa B, los seis usuarios QA-01 a QA-06 con su capa administrativa y
su rol operativo, las cuatro sucursales de la Empresa A —Madrid Central, Canarias,
Remoto y Turnos— con sus geocercas, zonas horarias y horarios, la sucursal B - Barcelona,
y las tareas de prueba de worker, supervisor y manager.

Es **idempotente y con identificadores fijos**: se puede volver a lanzar tantas veces como
haga falta y el resultado es siempre el mismo. Eso significa que si una prueba ensucia el
entorno, se rehace en segundos en lugar de reconstruirlo a mano.

Los seis usuarios son cuentas reales con identificador fijo. La suite emite sus tokens por
sí misma, sin contraseñas y sin códigos de un solo uso.

### 3.2 La matriz de permisos

Es la parte que más trabajo manual ahorra, porque son muchas combinaciones y todas
aburridas de comprobar a mano:

- **Tareas**: para cada uno de los cuatro roles operativos, contra tareas configuradas con
  y sin permiso de supervisor, se comprueba quién puede crear, ver, asignar, validar,
  rechazar y puntuar.
- **Aislamiento por sucursal**: que QA-03 y QA-04 no alcancen las tareas de Canarias ni de
  Remoto, donde no están asignados.
- **Aislamiento entre empresas**: que los datos de QA-06 en la Empresa B no aparezcan en
  la Empresa A y al revés.
- **Separación de capas**: que un rol operativo, por alto que sea, no abra por sí solo
  configuración de empresa, colaboradores ni facturación.

### 3.3 Los fichajes

**La geocerca se prueba entera desde la API.** Las coordenadas viajan en la petición, así
que se puede fichar dentro del radio, justo en el borde, a trescientos metros o desde otra
ciudad sin moverse de la silla. Esto relaja el requisito del plan de QA de que Madrid
Central tenga «una ubicación real y accesible»: la ubicación física solo hace falta para
probar el GPS del móvil, no la regla de negocio.

También se automatiza el rechazo por sucursal inactiva, por empleado sin responsabilidad
en la sucursal, por día festivo, por día deshabilitado en el horario y por fichaje fuera
de turno.

**El dispositivo de confianza no estorba.** La suite usa una identificación de dispositivo
fija y la registra como de confianza en las fichas QA, de modo que se prueba el camino
real —con la verificación activada— en lugar de desactivarla y probar otra cosa.

---

## 4. La hora: qué se puede y qué no

El fichaje se sella con la hora real del servidor y no admite que le digamos «haz como si
fueran las seis de la mañana». Por tanto no se puede pedir un fichaje a una hora concreta.

**La salida es mover el horario, no el reloj.** La siembra calcula los horarios de cada
sucursal en relación con el momento en que se ejecuta la prueba, de forma que «ahora»
caiga justo donde el caso lo necesita. Con ese truco quedan cubiertos:

- selección de turno cuando hay varios,
- turno partido,
- turno nocturno que cruza la medianoche,
- tolerancia de entrada anticipada,
- fichaje fuera de horario y día deshabilitado,
- zona horaria: que Canarias resuelva a `Atlantic/Canary` y que el mismo instante caiga
  dentro o fuera de la ventana local según corresponda.

Lo que **no** se cubre así, y por tanto sigue necesitando esperar o sembrar datos
directamente: los informes con fechas absolutas, los procesos programados —avisos,
cierres, resúmenes diarios— y cualquier caso que dependa de que pase un día natural.

---

## 5. Lo que no se automatiza

### 5.1 Los cuatro checks negativos de QA-02 — bloqueado, y no por QA

El plan de QA pide comprobar que un **Colaborador Admin no** accede a configuración de
empresa, ni a facturas y suscripción, ni a la gestión de colaboradores. Hoy, si esas
comprobaciones se hacen contra la API, **fallan**: el backend no distingue entre
Colaborador Propietario y Colaborador Admin. Ambos tienen exactamente el mismo permiso.
Lo único que hoy separa un perfil del otro son las pantallas del panel, que esconden las
opciones al admin.

Consecuencia práctica: las rutas de suscripción y el portal de facturación de Stripe
responden igual a un admin que a un propietario.

Esto deja dos caminos, y hay que elegir uno (§8):

- **Arreglarlo en el backend** y entonces automatizar los cuatro checks como el resto. Es
  un arreglo pequeño y, en nuestra opinión, el correcto: es un hueco de autorización real,
  no una limitación de la suite.
- **Dejarlo como está** y automatizar esos cuatro checks en navegador, lo que obliga a
  montar una herramienta de pruebas de interfaz solo para ellos.

Mientras no se decida, esos cuatro puntos siguen siendo **manuales** y hay que ejecutarlos
en el panel.

### 5.2 Lo que se queda en manos de personas, decidamos lo que decidamos

Los dispositivos 3 y 4 del plan de QA siguen siendo necesarios, pero con un guion mucho
más corto: solo aquello que únicamente un móvil demuestra.

- GPS real y su deriva, que es distinta de mandar unas coordenadas.
- Biometría y el alta de un dispositivo de confianza desde la app.
- Notificaciones push que llegan de verdad al terminal.
- Cámara, subida de fotos y vídeos como evidencia de tarea.
- Todo lo visual: que la pantalla enseñe lo que debe, en el idioma que debe, y que las
  opciones que un perfil no puede usar no aparezcan.
- El portal de facturación de Stripe, que termina en un sitio que no es nuestro.
- Los correos que salen del sistema (bienvenida, credenciales).

---

## 6. Desajustes entre el plan de QA y el sistema real

Detectados al contrastar el plan con el código. No son errores graves, pero cambian los
casos de prueba y conviene corregirlos en el documento de QA antes de escribirlos:

**Hay cuatro niveles operativos, no tres.** El sistema distingue worker, supervisor,
manager y owner. El plan agrupa «Owner / Manager» en una sola fila, lo cual es razonable
porque para tareas se comportan igual, pero QA-03 hay que darlo de alta siendo
explícitamente uno de los dos, no «Owner/Manager» a secas.

**El permiso de supervisor son tres interruptores, no uno.** Una tarea puede permitir por
separado que el supervisor la **cree**, que la **valide** y que **puntúe** al trabajador.
El plan habla de un único permiso de validación. La matriz de la sección 7 del plan
necesita tres columnas.

**El supervisor ve y asigna siempre.** Con independencia de cualquier interruptor, el
nivel supervisor puede ver todas las tareas de las sucursales donde está asignado y
asignar trabajadores a ellas. El plan dice que el supervisor solo puede lo que se le
habilite expresamente; eso es cierto para validar, crear y puntuar, pero no para ver ni
para asignar. QA-04 no debe fallar una prueba por esto.

**El módulo de tareas ya no está en Cloud Functions.** Ver §2.

---

## 7. Roadmap

### Fase 0 — Montar el banco de pruebas

Crear la suite dentro del monorepo y el contenedor que la ejecuta en staging, con la
emisión de tokens de los seis usuarios y la guarda que impide apuntar a producción.

*Entregable para QA:* dos comandos, uno que siembra el entorno y otro que lanza las
pruebas, ejecutables por cualquiera con acceso al servidor.

### Fase 1 — Siembra de la estructura

La Fase 1 del plan de QA, entera y automática: dos empresas, seis usuarios, cinco
sucursales, responsabilidades y tareas de prueba.

*Entregable para QA:* un entorno reproducible. QA lo revisa a ojo **una vez** para dar por
buena la siembra; a partir de ahí ya no vuelve a montarse a mano nunca.

### Fase 2 — Permisos

La matriz completa de la §3.2: tareas por rol y por interruptor, aislamiento entre
sucursales, aislamiento entre empresas y separación entre capa administrativa y rol
operativo.

*Entregable para QA:* un informe de resultado por cada punto de la checklist, con
referencia al número del punto en el plan de QA.

### Fase 3 — Fichajes

Geocerca, dispositivo de confianza, rechazos por estado, horarios mediante el truco de la
§4 y zona horaria de Canarias.

*Entregable para QA:* la parte de fichaje que no depende del móvil, cubierta.

### Fase 4 — Reducir el guion manual

Con las tres fases anteriores en verde, reescribir el guion de los dispositivos 3 y 4 para
que contenga solo lo de la §5.2.

*Entregable para QA:* una regresión manual sensiblemente más corta.

### En paralelo, y fuera de QA

El arreglo de propietario contra admin en el backend, si se decide por esa vía (§8).
Cuando esté, los cuatro checks pendientes se incorporan a la Fase 2.

### Cuándo se ejecuta

A mano cuando QA lo pida, y automáticamente al terminar cada despliegue del entorno de
desarrollo. Ese despliegue se dispara al empujar la rama `staging` y tarda algo menos de
un minuto.

---

## 8. Lo que necesitamos de QA

**Una decisión** (§5.1): si los cuatro checks negativos de QA-02 se resuelven arreglando el
backend —nuestra recomendación— o se automatizan en navegador. De esto depende si hay que
montar herramienta de pruebas de interfaz o no.

**Numerar la checklist.** Que cada punto del plan de QA tenga un identificador estable
(8.1.1, 8.1.2…). Así el informe automático dice exactamente qué punto ha pasado y cuál no,
sin que nadie tenga que traducir.

**Corregir el documento** con los cuatro desajustes de la §6.

**Confirmar las direcciones de las sucursales** que quiere QA para las geocercas, en
particular la de Madrid Central. Aunque la prueba automática no necesita un sitio real, la
prueba física con móvil sí, y el valor definitivo del radio hay que dejarlo escrito.

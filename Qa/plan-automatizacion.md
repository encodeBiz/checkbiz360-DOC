# QA — Automatización de pruebas: plan y método

> Cómo se automatiza la regresión de CheckBiz360 contra el entorno de desarrollo, por qué
> se hace así y en qué orden.
>
> Sustituye al planteamiento de [automatizacion-qa-staging.md](./automatizacion-qa-staging.md)
> (2026-08-26), que partía de los planes manuales de QA. Este parte del sistema.
>
> Código: rama `qa/automatizacion-staging` de encodebiz-api, carpeta `qa/`.
> Catálogo de casos: [catalogo/](./catalogo/).
>
> Fecha: 2026-09-11

---

## 1. Qué se construye

Una batería de pruebas que se ejecuta sola contra desarrollo y contesta dos preguntas:

1. **¿La migración HTTP está completa y es correcta?** Cada endpoint que usan el panel y la
   app, ahora servido por los contenedores en lugar de por Cloud Functions, se comporta como
   esos clientes esperan: mismas respuestas, mismos errores, mismos permisos.
2. **¿El flujo normal de un cliente funciona de punta a punta?** Desde que alguien se da de
   alta hasta que su primer trabajador ficha, incluido todo lo que el sistema hace por
   detrás sin que nadie lo vea.

---

## 2. Tres clases de comportamiento, tres formas de comprobarlo

Es la idea sobre la que se apoya todo lo demás. En CheckBiz360 hay tres maneras de que
ocurra algo, y cada una se prueba distinto.

**Acciones.** Alguien pide algo y el sistema contesta en el momento: crear una sucursal,
fichar, validar una tarea. Se comprueba la respuesta en el acto: el código de estado, el
código de error del cuerpo, la forma de los datos. Es la parte más sencilla y la más
numerosa.

**Listeners.** Algo reacciona a un cambio sin que nadie se lo pida. Al crearse un fichaje,
un trigger de Firestore lo sincroniza con Postgres, recalcula el patrón del empleado y quizá
manda una notificación. Aquí no hay respuesta que mirar, así que se mira el mundo *después*:
la prueba pregunta cada poco si el efecto ya existe —el documento, la fila, el snapshot—
hasta que aparece o hasta que se agota un plazo razonable. Esto se llama *consistencia
eventual*, y Playwright lo trae resuelto (`expect.poll`).

Lo que no se hace nunca es esperar un tiempo fijo «por si acaso». Una espera fija o sobra, y
la suite se vuelve lenta, o se queda corta, y entonces da un rojo que no significa nada. Las
pruebas que fallan unas veces sí y otras no —*flaky tests*— son la forma más rápida de que
un equipo deje de creerse su suite.

**Schedules.** Algo ocurre porque es la hora: el cierre diario, los avisos de tareas, la
facturación del día 5. No se puede esperar al reloj. En desarrollo se disparan a mano, cada
una por el mecanismo que tenga, y a partir de ahí se comprueban igual que un listener. El
inventario dice cuáles se pueden disparar y cuáles no.

**Un caso especial: el fichaje depende de la hora del día** —turnos, tolerancia, fuera de
horario— y se sella con el reloj del servidor, que no admite que le digamos qué hora es. Así
que no se mueve el reloj: **se mueve el horario**. La prueba configura el turno de la
sucursal alrededor de la hora a la que se está ejecutando, de forma que «ahora» caiga justo
donde el caso necesita.

---

## 3. Tres niveles de prueba

**Humo.** ¿El entorno está en pie? Un puñado de peticiones en dos segundos. Si esto falla,
el resto del informe es ruido, y por eso va primero (ficheros `00-`). Detecta, por ejemplo,
el nginx de desarrollo que se queda con las IPs viejas tras un redespliegue y devuelve 502.

**Contrato, endpoint por endpoint.** Cada endpoint, con cada tipo de actor y cada error
posible, tal como lo describe el catálogo. Esto es lo que demuestra la migración: si el panel
espera un 403 con `task/unauthorized` y el contenedor devuelve un 500, aparece aquí. Son
pruebas rápidas e independientes entre sí.

**Recorridos de punta a punta.** Pocas, lentas y las que más valen. Una empresa nace por el
alta real, se configura —horarios, sucursal, empleado, responsabilidad—, su trabajador entra
en la app, activa el segundo factor, ficha, y la prueba comprueba después la cadena de
efectos que eso desencadena. Aquí es donde se prueban los listeners y los snapshots.

Más adelante vendrán dos niveles más:

- **Comparativas función/contenedor.** La misma petición a la Cloud Function y al
  contenedor, y comparar las dos respuestas. Es la prueba más fuerte de que la migración no
  ha cambiado nada, pero caduca: solo se puede hacer mientras las funciones sigan
  desplegadas como rollback. **Y en desarrollo no cubre lo crítico**: de las rutas del
  contenedor, solo 34 tienen su función desplegada, y ninguna es de fichajes, tareas,
  documentos, login ni informes (comprobado el 2026-09-11). Los comentarios «Rollback:» de
  la app y del panel apuntan a funciones que en desarrollo no existen. Lo crítico se valida
  con las pruebas de contrato.
- **Interfaz.** El panel con Playwright en navegador y la app con Maestro, reservadas a lo
  que la API no puede ver: que una opción no aparezca, que una pantalla enseñe lo que debe.

La proporción importa. Muchas pruebas de contrato, rápidas y baratas; pocas de punta a
punta, lentas y caras; y las de interfaz, las justas. Es la *pirámide de pruebas*: cuanto más
arriba, más cuesta escribir y mantener cada prueba, y más fácil es que falle por motivos
ajenos a lo que se prueba.

---

## 4. Los datos: cada ejecución crea su propio mundo

No hay un entorno sembrado de antemano que compartan todas las pruebas. **Cada ejecución
crea su mundo** usando los endpoints de verdad, con un sufijo único —`qa-20260911-1432-a7f3`—,
y eso da tres cosas:

- dos ejecuciones no se pisan;
- ninguna prueba depende de lo que dejó otra, ni de un dato que alguien tocó a mano;
- el alta de empresas, sucursales y empleados, que es parte de lo que se quiere probar, se
  prueba en cada ejecución.

En Playwright esto se monta con un *proyecto de preparación*: un paso que corre antes que
todo lo demás, crea la empresa con sus sucursales y sus actores —un propietario, un admin,
un supervisor, un trabajador, uno de otra sucursal, uno de otra empresa— y deja apuntados sus
identificadores para que las pruebas de contrato los usen.

Lo creado se limpia con un script que, como todo lo que borra en este proyecto, simula por
defecto y solo actúa con `--apply`.

### Las direcciones de correo

El alta de verdad manda correos de verdad: la bienvenida del propietario y la del empleado, y
el aviso de servicio activado. En desarrollo salen por Amazon SES, con remitente
`dev@encodebiz.com` y en la misma región que usan las funciones. Una dirección inventada
rebota, y los rebotes cuentan contra la reputación de la cuenta de SES, que es la que decide
si los correos de los clientes llegan o acaban en spam.

Por eso los usuarios de prueba usan las direcciones del **simulador de SES**:
`success+qa-<ejecución>-<rol>@simulator.amazonses.com`. SES las acepta, no las entrega a
nadie, no gastan cuota y no cuentan para la reputación. Cada una es única gracias a lo que va
detrás del `+`.

Tiene una consecuencia que conviene tener clara: la contraseña temporal del empleado solo
viaja en ese correo, así que la prueba no puede leerla. La fija ella con el SDK de
administración, con el mismo mecanismo que usa el servidor. Es una desviación consciente del
flujo real, y está anotada en el catálogo del recorrido.

---

## 5. Hacerse pasar por cada persona sin contraseñas

- **Usuarios del panel y trabajadores.** La suite emite un token propio con el service
  account de desarrollo y lo canjea por una sesión, igual que hace el navegador cuando alguien
  teclea su contraseña.
- **Segundo factor.** La activación devuelve el secreto; la suite calcula el código de seis
  dígitos igual que lo hace Google Authenticator.
- **Dispositivo de confianza.** La app se identifica por el User-Agent; la suite usa uno fijo
  y lo registra como de confianza.

No es hacer trampa. Lo que se prueba es cómo responde el sistema a cada credencial, no la
pantalla de login: esa la resuelve Firebase y, en lo que tiene de nuestro, la cubrirán las
pruebas de interfaz.

---

## 6. Los cerrojos contra producción

Desde el 2026-09-12 cada entorno tiene su máquina y su nombre:
`api-staging.checkbiz360.com` contra `api.checkbiz360.com`. El cerrojo sigue siendo una
**lista blanca por origen**, no una lista negra de dominios, y se queda así a propósito.

Se escribió como lista blanca porque entonces no cabía otra cosa —los dos entornos
compartían IP, y `http://141.95.47.135` sin puerto ERA producción sin contener ningún
nombre prohibido—. Ahora una lista negra sí sería posible, y sigue siendo peor idea: deja
pasar todo lo que a nadie se le ocurrió prohibir. Con la lista blanca, un borde que nadie
haya dado de alta simplemente no se prueba, que es el fallo barato.

El segundo cerrojo está en las credenciales: si el service account no es del proyecto
`dev-encodebiz`, la suite se para antes de inicializar nada. Hacen falta los dos porque son
fallos distintos: apuntar bien con las credenciales equivocadas siembra en un sitio y
comprueba en otro.

Los dos se comprueban antes de la primera petición.

---

## 7. Herramientas

**Playwright Test.** Es a la vez el ejecutor de pruebas, el cliente HTTP y, cuando haga
falta, el navegador. Una sola herramienta para la API y para el panel, con un informe HTML
que se lee sin saber de testing y que guarda la petición y la respuesta completas de cada
caso que falla. Permite etiquetar pruebas y ejecutar solo un trozo, y ordenar pasos con
dependencias (el proyecto de preparación del §4).

**otplib** calcula los códigos del segundo factor; **firebase-admin** emite los tokens y lee
Firestore para comprobar los efectos de los listeners.

**Maestro**, más adelante, para la app: los recorridos se escriben en YAML y se ejecutan
contra el simulador sin tocar el código de la app.

Todo son paquetes npm. No hace falta ninguna extensión ni licencia.

---

## 8. El catálogo

El inventario de todo lo que hay que probar vive en [catalogo/](./catalogo/), un fichero por
parcela del sistema. Se construye **desde los endpoints y no desde los planes manuales de
QA**: los planes describen lo que hace una persona, y los endpoints que ningún plan menciona
son justo los que pueden haberse migrado mal sin que nadie se entere. Los planes de QA se
enganchan encima.

Cada caso tiene un identificador —`CHK-03-02`: módulo, endpoint, caso— y la prueba que lo
cubre lleva ese identificador al principio del título. El informe se lee así contra el
catálogo sin traducir nada, y la cobertura es una cuenta simple: casos con prueba entre
casos del catálogo.

**Dónde va la cobertura hoy** (2026-09-12, medida sobre la lista real de pruebas, no estimada):
127 casos del catálogo cubiertos de ~1.741 —un 7,3 %—, más 18 comprobaciones de entorno que no
salen del catálogo. Por módulo: fichaje y calendario 86, tareas 20, documentos 10, empleados 5,
colaboradores 4, facturación 2, y cero en sucursales, empresas, informes, analítica y webhooks.

Dentro de fichaje, el endpoint de crear fichaje (CHK-08) va por **46 de sus 83 casos**:
cubiertos la jornada normal, el orden de los fichajes, la vía del panel, lo básico de la
geocerca y el bloque de horarios —día sin jornada, festivo, tolerancia, jornada partida y rango
estricto—. Lo que queda son casos que piden un empleado o una sucursal en un **estado**
concreto: dispositivo de confianza, responsabilidad retirada, sucursal inactiva, empleado dado
de baja y trabajo remoto.

Cubrir los 1.741 **no es el objetivo** y nadie lo hace. El orden lo marca la criticidad: lo que
más se usa y lo que más duele si se rompe.

Los actores tienen nombres fijos, iguales en el catálogo y en las pruebas:

| Actor | Quién es |
|---|---|
| `ANON` | Sin credencial |
| `TOKEN_INVALIDO` | Credencial mal formada, caducada o de otro emisor |
| `PROP` | Colaborador propietario de la empresa |
| `ADMIN` | Colaborador admin de la empresa |
| `OP_OWNER`, `OP_MANAGER`, `OP_SUPERVISOR`, `OP_WORKER` | Trabajador con ese nivel en la sucursal del recurso |
| `OP_OTRA_SUCURSAL` | Trabajador de la misma empresa sin responsabilidad en esa sucursal |
| `AJENO` | Usuario de otra empresa |
| `EMP_JWT` | Sesión de trabajador de la app |
| `EMP_INACTIVO` | Trabajador cuya ficha no está activa |
| `S2S` | Llamada entre servidores con clave |

### Qué hace una prueba con un fallo conocido

El catálogo recoge lo que hace el código **hoy**, y aparte, como *sospecha*, lo que parece
un fallo. La prueba no copia el fallo: afirma el comportamiento correcto, y si hoy falla se
marca como **fallo esperado** (`test.fail()`) con la referencia del hallazgo.

El efecto es útil: mientras el fallo exista, la suite sigue en verde y el informe lo lista
como conocido. El día que alguien lo arregle, la prueba empieza a pasar, Playwright lo
señala como *pasa cuando se esperaba que fallara*, y eso obliga a quitar la marca. Ningún
fallo se queda escondido y ningún arreglo pasa desapercibido.

---

## 9. Cómo se lee el resultado

En la terminal sale una línea por caso: **✓** se comporta como debe; **✘** no, y debajo qué
se esperaba y qué llegó; **saltado**, no se ha podido ejecutar y dice por qué —casi siempre,
credenciales que faltan en esa máquina—.

`npm run informe` abre el informe HTML. En cada caso rojo, la pestaña de traza enseña la
petición y la respuesta tal como viajaron: es lo primero que hay que mirar antes de abrir el
código.

---

## 10. Dónde corre

En local con `cd qa && npm test`, y en GitHub Actions como un paso del propio workflow de
staging: `needs: deploy`, así que prueba lo que se acaba de desplegar y no la versión
anterior. Publica el informe como artefacto y un resumen en la página de la ejecución.
Pendiente: una ejecución nocturna para los recorridos largos y las programadas.

**Lo que enseñó la primera ejecución de verdad** (2026-09-12, estreno del servidor propio):
no falló el producto, falló la suite. La preparación de un fichero —crear seis trabajadores,
cada uno con su alta, su responsabilidad y su sesión— cabía de sobra en el plazo por defecto
desde un portátil y no cabía desde el runner de GitHub. Los plazos de preparación se subieron
a 150 s en los ficheros que crean gente.

Es el fallo barato y merece la pena señalarlo: una suite que solo se ha ejecutado en la
máquina de quien la escribió tiene los plazos calibrados para esa máquina, y eso no se
descubre hasta que corre en otra.

### Por qué el entorno nuevo tarda más por operación

Una operación de fichaje pasó de 200-300 ms a **1,5-2 s**. La causa está medida y **no es el
servidor**: es distancia de red a Google.

- Ida y vuelta a `firestore.googleapis.com` — VPS de desarrollo (Roubaix): **76 ms**. Servidor
  de producción (Fráncfort): **1,6 ms**. Son ~74 ms extra por viaje, y un fichaje encadena
  varias escrituras a Firestore.
- El VPS **no está ahogado**: robo de CPU del hipervisor 0, carga 0,30 sobre 4 núcleos,
  escritura sincronizada a disco 0,35 ms, 4,8 GB de RAM libres. Descartado.
- Las dos máquinas están en Europa y usan el mismo resolutor de OVH, así que tampoco es DNS.

Lo que **no** está establecido es por qué la ruta difiere; lo más probable es que Fráncfort
tenga un punto de presencia de Google al lado y Roubaix no, pero eso es peering de OVH y queda
fuera de nuestro alcance. **Decisión tomada: no se toca, es el entorno de desarrollo.**

Para QA solo importa el presupuesto: el job tiene 20 minutos y la suite tarda 4. Si algún día
se acerca, lo que hay que hacer es **paralelizar las preparaciones** que hoy crean trabajadores
en serie, no perseguir el servidor.

---

## 11. El objetivo es encontrar errores, no acumular verdes

Conviene decirlo antes de la hoja de ruta, porque decide cómo se escribe cada prueba.

Una suite se puede escribir de dos maneras. Una es preguntarle al sistema lo que ya se sabe
que contesta bien: sale verde, da tranquilidad y **no sirve para nada**. La otra es ir a
buscar dónde se rompe: los caminos que nadie recorre, el actor que no debería poder, el dato
en el límite, el efecto que ocurre por detrás y nadie mira.

De ahí tres reglas que ya están en uso y que no se negocian:

- **La prueba afirma lo correcto, nunca lo observado**, cuando las dos cosas difieren. Si hoy
  el sistema hace algo que no debe, la prueba escribe lo que debería hacer y se marca como
  fallo conocido con su referencia. Copiar el fallo dentro de la prueba lo convierte en
  requisito y lo entierra para siempre.
- **Un verde solo vale lo que vale su aserción.** Comprobar que responde `200` no es
  comprobar nada: hay que mirar qué quedó escrito. Un `200` con el dato mal guardado es peor
  que un `500`, porque nadie se entera.
- **Cuando una prueba se pone roja, la primera hipótesis es que el producto está mal**, no
  que la prueba está mal. Solo después de mirarlo se decide. Al revés se acaba ajustando la
  prueba hasta que pase, que es la forma educada de esconder un fallo.

Y lo que no se sabe, se dice que no se sabe. Un hallazgo nombra el hecho medido; si la causa
no está establecida, se escribe que no lo está.

---

## 12. Los bloques, en el orden en que se atacan

La hoja de ruta va **por el recorrido de un cliente**, no por endpoints sueltos. Y cada
bloque incluye **los efectos que provoca**, no solo la respuesta: el índice de búsqueda, las
coordenadas, el espejo en Postgres y el cobro se comprueban junto al acto que los dispara.

Esto corrige el planteamiento anterior, que apartaba los efectos a una fase futura. Apartados
nunca se prueban: el orden por endpoints deja siempre lo asíncrono para el final, y el final
no llega.

**Bloque 1 · Puesta en marcha.** Alta de usuario y de empresa con su CRUD completo, activación
de checkinbiz, y aparejado a eso lo que el alta desencadena: las entradas del índice de
búsqueda, las coordenadas de la dirección y el alta en facturación. Después, horarios,
sucursales y empleados. Y para cerrarlo, **adelantar los 15 días de prueba** y comprobar que
el cobro sale bien y que la factura llega.

**Bloque 2 · Fichajes**, con todo lo que arrastran.

> **Cómo debe montarse la prueba del cobro al terminar la prueba gratuita** (medido el
> 2026-09-12, para no volver a descubrirlo):
>
> - Va **siempre después de crear los empleados**. La cantidad facturable sale de ellos; sin
>   gente la factura es de 0 € por definición y la prueba no probaría nada.
> - La aserción no es «hay factura»: es que el importe **cuadre con la plantilla** — tantos
>   empleados facturables por el precio unitario. Si sale 0 € habiendo empleados, **es rojo**.
>   Esa es justamente la forma que tomaría HAL-19 si el aviso previo se pierde.
> - No vale `trial_end: "now"`: se salta los avisos de los que depende el recálculo. Hay que
>   poner el fin de la prueba **a un par de minutos vista** y dejar que la secuencia ocurra.
>   Medido: el aviso llega a los ~21 s y la factura se emite a los ~138 s.
> - Por eso va en un proyecto aparte y no en cada despliegue: son dos minutos y medio de reloj
>   de pared.

**Bloque 3 · Módulos menos críticos**: tareas, documental e informes.

**Bloque 4 · Complementarios**: disponibilidad y calendario.

**Bloque 5 · Postgres**: el espejo y todo lo que se calcula ahí solo.

**Bloque 6 · Merlin**, y las programadas de madrugada, disparadas a mano.

### Lo que ya está construido

El banco de pruebas (Playwright, los dos cerrojos, la emisión de tokens y 18 casos de humo),
el inventario completo (8 catálogos, ~1.741 casos), el mundo de la ejecución que se crea por
los endpoints reales, la ejecución automática en CI tras cada despliegue, y del bloque 2 la
mayor parte del fichaje: jornada completa, orden de los fichajes, vía del panel, horarios,
geocerca, corrección de jornada y jornada manual.

Queda pendiente y sin fecha: las comparativas función/contenedor —solo cubren 34 rutas
secundarias, ninguna crítica— y las pruebas de interfaz con navegador y con Maestro.

Las credenciales ya están: la cuenta de servicio `qa-suite@dev-encodebiz` con tres permisos
—crear usuarios de prueba, leer y escribir Firestore y lanzar programadas—, su clave en
`qa/secrets/` y en GitHub como secreto `QA_FIREBASE_SA_DEV`.

Lo que queda por delante, por orden de valor: seguir la fase 4 por lo más crítico (el resto de
fichaje, login y permisos de tareas), y después la cadena de efectos de la fase 3 —los
listeners y los snapshots que se disparan tras un fichaje—, que es lo que hoy no mira nadie.

# 08 — El prompt de investigación

Lo que se le pide a Merlin para investigar una empresa ([ADR-009](./adr/ADR-009-merlin-investiga-en-el-servidor.md),
[TDR-007](./tdr/TDR-007-investigacion-con-merlin.md)). El texto de verdad vive en
`services/merlin/src/investigacion/prompt.ts`; este documento se copia de ahí y explica el
porqué de cada decisión. Va sin acentos a propósito: `gpt-5-mini` emite de vez en cuando un
escape Unicode malformado al generar español dentro de un JSON estricto (el mismo problema
documentado en los cuadrantes).

## Por qué dos pasos y no uno

El modelo puede inventar una URL que parezca verosímil. Lo que no puede inventar es la lista
de páginas que la API de OpenAI devuelve como consultadas: las fuentes que abrió la
herramienta de búsqueda (`web_search_call.action.sources`, pedidas con `include`) y, cuando
las hay, las anotaciones `url_citation` del mensaje. Las produce la API, no el modelo. Con
`gpt-5-mini` las anotaciones llegan vacías (comprobado el 2026-10-16), así que la prueba
real son las fuentes de la búsqueda. Por eso la investigación se parte en dos:

1. **El dossier**, con búsqueda web y en texto libre, donde cada hecho lleva su URL. De la
   respuesta se extraen las páginas consultadas.
2. **El perfil**, sin herramientas y con esquema JSON estricto, que solo puede citar URLs que
   estén en el dossier. El servidor comprueba después que cada prueba esté entre las
   consultadas; lo que no, se descarta y se dice.

Separarlos tiene dos ventajas más: el dossier queda como pieza auditable (se puede imprimir
con `--dossier`), y la segunda llamada es barata porque no busca.

## Las defensas contra la invención, y dónde está cada una

| Riesgo | En el prompt | En el servidor |
|---|---|---|
| Investigar a un homónimo | Confirmar identidad por CIF, dominio, concurso o razón social + provincia antes de anotar nada; si no, «IDENTIDAD: no confirmada» y parar | Si el dossier lo dice, o si las URLs de la identidad no están entre las consultadas → `no_identificada`, nada se guarda |
| Dolores genéricos del nicho presentados como de esta empresa | «No recicles la lista del nicho»; cada dolor atado a un hecho del dossier | Un dolor cuya URL no esté entre las consultadas va a `descartados`; sin dolores, `insuficiente` |
| Cifras inventadas o redondeadas | «Copia las cifras como aparecen, con su URL; si dos fuentes difieren, pon las dos» | Toda cifra de ROI sin fuente consultada se marca `assumed: true` aunque el modelo diga lo contrario |
| Personas adivinadas | Solo nombres y cargos leídos en una página consultada; nada de LinkedIn deducido | Decisor sin fuente consultada, fuera; sin email ni teléfono |
| Responder sin buscar | — | Cero páginas consultadas → `insuficiente` sin llegar al paso 2 |
| Citar una URL que no abrió (aunque la escriba entre corchetes en el dossier) | — | Solo valen las URLs que la API devolvió como abiertas; el texto del dossier no es prueba |
| Lenguaje de venta | «Sin adjetivos de venta, sin líder, innovador, solución» | — |

Y la regla de la casa: la calidad se arregla aquí y en estas comprobaciones, nunca recortando
la respuesta del modelo.

## Paso 1 — el dossier

```
Eres un investigador comercial. Preparas un DOSSIER DE HECHOS sobre UNA empresa espanola
para que un comercial de CheckBiz360 (control de trabajo en campo: fichaje por centro,
tareas con evidencia, partes, documentos firmados desde el movil) decida si contactarla y
con que argumento. Tu no decides ni recomiendas: solo reunes hechos comprobables. El
comercial va a citar estos datos delante del cliente.

LA UNICA REGLA QUE NO SE ROMPE
Escribes solo lo que has leido en una pagina que has abierto en esta busqueda, y cada
hecho va seguido de la URL exacta de esa pagina entre corchetes. Un hecho sin URL no es un
hecho: no lo escribas. No completes con lo que "suele pasar" en el sector, no deduzcas
cifras, no redondees, no inventes cargos ni nombres. Si dos paginas dicen cosas distintas,
pon las dos con sus URLs. Si no encuentras algo, lo dices en la seccion de huecos. Un
dossier corto y cierto vale; uno largo con una sola invencion lo estropea todo.

PRIMERO, LA IDENTIDAD
Te doy nombre, y si los tengo, CIF, dominio web, provincia, tamano y los concursos
publicos que ha ganado. Los homonimos son la norma: hay "Limpiezas X" en veinte
provincias. Antes de anotar nada, confirma que la pagina habla de ESTA empresa: el CIF
aparece (el aviso legal de su web suele traerlo), o el dominio es el suyo, o el concurso
que te doy aparece adjudicado a ese nombre, o la razon social completa coincide con la
provincia. Escribe como lo has confirmado y con que URLs. Si no lo consigues con ninguna
pagina, escribe "IDENTIDAD: no confirmada", di que has probado, y no escribas nada mas.

LO QUE MAS VALE: SUS PROPIAS PALABRAS
Lo que diferencia un dossier util de uno de relleno es lo que la empresa ha dicho de si
misma hace poco: una entrada de su blog, una noticia de su web, una entrevista, un post, el
texto de una certificacion, un testimonio de su pagina de empleo. Un comercial que cita
las palabras de la propia empresa no parece un vendedor. Por eso, ademas de la web
general, ABRE SIEMPRE si existen: su seccion de noticias, blog o actualidad (y las dos
entradas mas recientes), su pagina de empleo o "trabaja con nosotros", su aviso legal, y
busca prensa y entrevistas de los ultimos doce meses con el nombre de la empresa. Copia
frases literales cortas (hasta 25 palabras) entre comillas, con la fecha y la URL. Si la
empresa no tiene blog ni noticias, dilo: tambien es un dato.

LOS NUMEROS, Y COMO CAMBIAN
Cuando encuentres una cifra (empleados, centros, contratos, delegaciones, facturacion),
busca la misma cifra en una fuente mas antigua y escribe el cambio: "de 1.100 personas en
2019 a 2.053 en 2026". El salto es lo que engancha; el numero suelto, no. Copia cada
cifra como aparece, con su URL y su fecha.

QUE BUSCAR, EN ESTE ORDEN
1. Su web: servicios, sectores y clientes, zonas, centros o contratos, como organiza al
   personal (cuadrillas, supervisores, turnos, rutas), ofertas de empleo, noticias.
2. Lo que han dicho ellos: blog, noticias, entrevistas, posts, certificaciones, memorias.
3. Contratos publicos: adjudicaciones y contratos en ejecucion (Plataforma de
   Contratacion, perfiles del contratante, boletines oficiales), importes, fechas, quien
   fiscaliza, y si algun pliego exige control de presencia, partes, evidencias o informes
   por centro. Y si lo publico es residual frente a lo privado: eso cambia el discurso.
4. Tamano y cifras, con su evolucion.
5. Como controlan hoy el trabajo: apps, ERP, fichaje, partes en papel, hojas de calculo,
   certificaciones (ISO, B Corp) que obliguen a reportar con evidencia.
6. Personas: nombres y cargos que aparezcan en una pagina consultada (su web, prensa,
   boletines, registro mercantil), con su fecha de incorporacion si consta. Solo esos.
7. Senales recientes con fecha: concursos, centros nuevos, contrataciones, cambios de
   direccion, subidas de convenio, incidencias publicas.

FORMATO DEL DOSSIER
Texto en espanol, frases cortas, sin adjetivos de venta y sin recomendaciones. Estas
secciones, siempre, aunque alguna quede en "nada encontrado":
IDENTIDAD
QUE HACE
COMO OPERA EN CAMPO
EN SUS PROPIAS PALABRAS (citas literales con fecha)
TAMANO Y CIFRAS (con su evolucion)
CONTRATOS Y LICITACIONES
COMO CONTROLAN HOY
PERSONAS
SENALES RECIENTES (con fecha)
LA FRASE QUE CITARIA UN COMERCIAL (el hecho mas concreto y reciente, uno solo, con URL)
LO QUE NO HE ENCONTRADO
```

**Entrada:** la ficha de la cuenta (nombre, razón social, CIF, dominio, provincia, tamaño,
nicho en una línea), las señales vivas con su URL (sirven para confirmar la identidad), las
personas que ya conocemos y el resumen del perfil anterior si lo hay.
**Herramienta:** `web_search_preview` con `search_context_size` configurable y ubicación
España.

## Paso 2 — el perfil

```
Conviertes el DOSSIER DE HECHOS de una empresa en el perfil comercial que guarda el CRM
de CheckBiz360. Trabajas SOLO con el dossier: no tienes acceso a la web y no sabes nada de
esta empresa que no este ahi. Te doy ademas el conocimiento del nicho (dolores tipicos,
jerga, quien decide), el producto y los criterios de encaje.

LA PRUEBA DE ESPECIFICIDAD
Antes de dar por bueno el resumen, cada dolor y el gancho, hazte una pregunta: "¿esto
podria decirse de cualquier empresa del nicho?". Si la respuesta es si, no vale: vuelve
al dossier y reescribelo con el hecho concreto de ESTA empresa (su cifra, su fecha, su
frase). El conocimiento del nicho te dice donde mirar y como hablan; no es una lista para
copiar. Un perfil que valdria para otra empresa es un perfil que no vale.

REGLAS
- Cada dolor de "pains" empieza por el hecho del dossier y sigue con lo que implica:
  "Han pasado de 1.400 a 1.730 proyectos con nueve delegaciones: el volumen crecio por
  encima de lo que la herramienta se diseno para cubrir". Su "evidence" es la URL de ese
  hecho, copiada tal cual del dossier. El mas concreto y reciente, primero. Un dolor del
  nicho que no puedas atar a un hecho de esta empresa NO va.
- Si el dossier dice "IDENTIDAD: no confirmada", devuelves estado "no_identificada" y
  todo lo demas vacio.
- Si la identidad esta confirmada pero no hay ningun dolor con prueba, estado
  "insuficiente": summary con lo que si se sabe, pains vacio, y en "huecos" que faltaria.
- "summary": que hace y como opera en campo, 4 a 8 frases, solo hechos del dossier, con
  las cifras y las fechas. Si lo publico es residual frente a lo privado, dilo: cambia a
  quien hay que convencer.
- "hook": dos frases como las diria el comercial a quien decide. La primera, el hecho mas
  concreto y reciente del dossier, mejor si son sus propias palabras o su propio numero.
  La segunda, lo que eso le cuesta hoy a quien decide y, en una clausula y en la jerga del
  nicho, que cambia con el dato por centro. Tiene que llevar un numero, una fecha o una
  cita. Asi es un gancho (la forma, no el contenido):
    "Vuestro propio articulo lo dice: el encargado tapa bajas y mete de cinco a siete
    refuerzos en los picos. Con 500 centros, eso no es un problema de fichaje sino de
    saber el coste real de cada centro antes del cierre de mes."
    "Acabais de anunciar a vuestros clientes una subida del 9,9% por el convenio. Quien
    anuncia una subida tiene que poder justificar las horas que cobra, centro a centro."
  Asi NO es un gancho: "Han conseguido contratos publicos, eso exige trazabilidad",
  "Necesitan control y evidencias", "Con tantos centros necesitan una solucion". Si solo
  te sale uno asi, es que falta el hecho: deja el gancho con lo mas concreto que haya y
  anota en "huecos" que falta el detalle.
  Y la cita sola tampoco es el gancho. Copiar "semanalmente se emitira un informe firmado
  por la persona encargada del centro" y parar ahi es dejar el trabajo a medias: el gancho
  es esa cita MAS lo que le cuesta hoy a quien decide cumplirla ("eso hoy lo firma la
  encargada a mano cada viernes, sin saber que horas lo respaldan") y, en una clausula, que
  cambia con el dato por centro. Siempre las dos partes.
- "roiInputs": trabajadores, centros, horas administrativas u otras cifras utiles para
  calcular ahorro. Cada una con su "fuente" (URL del dossier) y "assumed" false. Si una
  cifra es una estimacion tuya, "assumed" true, "fuente" vacia y en "valor" la base de la
  estimacion. Nunca presentes una estimacion como dato.
- "decisores": solo personas de la seccion PERSONAS del dossier, con nombre y apellido,
  su cargo tal como aparece y la URL. "papel": decider si el cargo es gerente, director
  general, CEO, administrador o propietario; influencer si es de operaciones, calidad,
  RRHH o zona; user si es encargado o supervisor; gatekeeper si es administracion o
  recepcion. Si alguien entro hace poco en el cargo, dilo en el cargo: es un hecho util.
- "encaje": puntos 0-100 aplicando los criterios dados, y "motivos" con una linea por
  criterio que sume o reste, citando el hecho. Lo que el dossier no permite evaluar no
  suma ni resta.
- "huecos": lo que un comercial necesitaria saber y no esta, lo mas importante primero.
- "avisos": lo que el comercial debe saber antes de hablar: ya usan una herramienta,
  conflicto publico, cambio de nombre, grupo con varias sociedades, cifras que no cuadran.
- Las URLs las copias exactamente como estan en el dossier. Ninguna URL nueva.
- Texto en espanol, en segunda persona del plural cuando hables a la empresa. Sin
  adjetivos de venta, sin "lider", "innovador", "solucion", "optimizar", "trazabilidad"
  como muletilla.
```

**Entrada:** el fichero del nicho, el posicionamiento, el producto y los criterios de encaje
del plugin `checkbiz360-gtm` (los mismos que usa Claude), la ficha de la cuenta, la lista de
URLs consultadas y el dossier. **Salida:** el esquema `ESQUEMA_PERFIL` de `prompt.ts`, con
`strict: true`: estado, identidad, resumen, gancho, dolores con prueba, cifras de ROI con su
fuente o marcadas como supuestas, decisores con fuente, encaje con motivos, huecos y avisos.

## Lo que cambió el 2026-10-16 tras la prueba de 10

Merlin acertaba en identidad, personas y fuentes, pero el gancho salía plano («han
conseguido contratos públicos, eso exige trazabilidad») donde Claude citaba el artículo de
la propia empresa o el salto de una cifra. Tres cambios, todos en el prompt y en la
configuración, ninguno en el modelo:

1. **Sus propias palabras.** El dossier abre siempre, si existen, el blog o las noticias (las
   dos entradas más recientes), la página de empleo y el aviso legal, y copia citas literales
   cortas con fecha. Nueva sección «EN SUS PROPIAS PALABRAS» y «LA FRASE QUE CITARÍA UN
   COMERCIAL».
2. **Los números y cómo cambian.** Cada cifra se busca también en una fuente anterior y se
   escribe el salto («de 1.100 personas en 2019 a 2.053 en 2026»).
3. **La prueba de especificidad.** Antes de dar por bueno el resumen, un dolor o el gancho:
   «¿podría decirse de cualquier empresa del nicho?». Si sí, no vale. El gancho son dos
   frases como las diría el comercial, con un número, una fecha o una cita, y hay ejemplos de
   forma de lo que vale y de lo que no.

Y el contexto de búsqueda pasa a «alto» por defecto: más texto de cada página abierta, que
es lo más parecido a leerla entera. Modelo, razonamiento y contexto se eligen en Ajustes del
CRM; la lista de modelos la da la propia cuenta de OpenAI.

## Cómo se prueba

- `services/merlin/test/investigacion.test.ts`: con un modelo simulado, que el servidor
  descarta lo no probado, no acepta una identidad sin página, no pasa al perfil si no se
  buscó, y solo manda `reasoning` a modelos de razonamiento.
- La prueba de 10 (TDR-007 §7): las cuentas de limpieza que ya investigó Claude, reinvestigadas
  en seco por Merlin con `investigar-merlin.js`, y las dos versiones delante de Jose.

## Lo que enseñó la comparación de modelos (2026-10-16, en seco, contexto «alto»)

| | Claude (14-oct) | `gpt-5-mini`, prompt nuevo | `gpt-5.5`, razonamiento alto |
|---|---|---|---|
| Las Nieves | contratos de la Junta en enero y salto de 1.400 a 1.730 proyectos | los mismos contratos con sus importes (278.000 € y 257.000 €) y los 1.730 proyectos | cortado por el tope de salida |
| GESPROLIM | su post sobre el convenio y la subida del 9,9 % | cita literal de ese post del 6/10/2026 (antes salía vacía) | cortado por el tope de salida |
| Serlimar | el artículo de los coordinadores que «tapan bajas con 5-7 refuerzos» | «+950 personas» y «+500 centros», y quién fiscaliza (el facility manager) | cita un post del director de operaciones del día anterior: mejor que Claude |
| Coste y tiempo | — | 35-77k tokens de entrada, ~4 cts, 2-2,5 min | ~140k de entrada, ~10× el coste, 3,5 min |

Conclusión: el prompt cerró casi toda la distancia en `gpt-5-mini`; el modelo grande da el
mejor gancho cuando se le deja terminar. Los cortes eran del tope de salida (el razonamiento
cuenta dentro) y del `fetch` de Node a los 300 s; los dos corregidos ese día.

## Qué tocar si falla

- **Confunde empresas:** reforzar «PRIMERO, LA IDENTIDAD» con el dato que falló (p. ej. exigir
  la provincia cuando no hay CIF).
- **Se queda corto en hechos:** subir `CRM_INVESTIGACION_BUSQUEDA` a `high` antes que cambiar
  el prompt; después, el modelo (`CRM_INVESTIGACION_MODELO`).
- **«La respuesta se cortó por el tope de tokens de salida»:** con razonamiento alto, subir
  `CRM_INVESTIGACION_MAX_SALIDA` o bajar el razonamiento; el perfil ya usa el doble del tope.
- **Propone muchos dolores sin prueba:** se ve en `descartados` de cada intento
  (`sales_research_runs.pains_dropped`); si es sistemático, el paso 2 necesita el ejemplo
  concreto de lo que NO vale.

## Afinar desde Ajustes (2026-10-18, ADR-010)

Los tres prompts —el del dossier, el del perfil y el de la búsqueda de señales— se editan en
**Ajustes del CRM**: lo guardado sustituye al de fábrica en la siguiente llamada, sin pase.
Vacío o igual al de fábrica = el de fábrica (que sigue siendo lo de arriba, en `prompt.ts`, y
lo que Merlin enseña por `GET /gpt/investigacion/prompts`). Lo que no se afina: el esquema
JSON, el conocimiento del nicho y las comprobaciones del servidor (URL consultada, identidad,
nombre completo, fecha en ventana). Para comparar versiones, copiar el texto antes de tocarlo:
no hay historial, sólo «Restaurar el de fábrica».

## El prompt de búsqueda de señales

Dos pasos, como la investigación. El primero busca y escribe una ficha por hallazgo; es el
que se afina. El segundo pasa las fichas a JSON y es fijo.

### Paso 1 — buscar y escribir las fichas (`INSTRUCCIONES_SENALES`)

```
Eres el analista de prospeccion de CheckBiz360, una herramienta de control de presencia y
de tareas para empresas con gente trabajando fuera de la oficina: limpieza, ayuda a
domicilio, mantenimiento, construccion y eventos. Tu trabajo hoy no es describir empresas:
es encontrar HECHOS CON FECHA, de los ultimos dias, que digan que una empresa concreta del
nicho va a tener que controlar mejor a su gente en campo. A eso lo llamamos una senal de
"por que ahora".

QUE ES UNA SENAL (Y QUE NO)
- Un hecho fechado, de una empresa con nombre, que cambia su operativa de campo: le
  adjudican un contrato, abre un centro, una obra o una delegacion, contrata personal de
  campo en volumen, cambia la gerencia o la direccion de operaciones, la compra un grupo,
  le exigen un control (un pliego, una inspeccion), o se queja en publico de su
  herramienta actual.
- NO es una senal: una descripcion general de la empresa, una noticia del sector sin
  empresa, un hecho fuera de la ventana de fechas, un hecho sin pagina que lo diga. Una
  licitacion todavia en plazo no es una adjudicacion: si la empresa concurre, va como
  "other" ("licitacion abierta a la que concurre").
- La empresa tiene que ser del nicho y operar en Espana. Preferimos pymes: entre 20 y 250
  personas. Los grandes grupos que salen en todas las adjudicaciones del pais no nos
  interesan; si en una busqueda solo salen grandes, dilo y busca mas abajo (provincias,
  contratos pequenos, prensa local).

DONDE BUSCAR
Las fuentes que te doy debajo: la tabla de tipos de senal y la seccion del nicho dicen que
es cada tipo y donde se encuentra. Haz varias busquedas distintas, no una: por tipo de
senal, con las palabras del nicho, por provincia o zona si hay foco, en la Plataforma de
Contratacion del Sector Publico y en los perfiles del contratante, en el BORME, en los
portales de empleo, en la prensa local y economica, en LinkedIn y en la web de la propia
empresa. Mejor seis senales verdaderas que veinte dudosas.

COMO ESCRIBIR EL DOSSIER
Una ficha por hallazgo, en texto, con estas lineas y en este orden:
EMPRESA: nombre tal como aparece | web o CIF, solo si la pagina los dice | provincia
HECHO: que paso, en una o dos frases, con las cifras que de la pagina (centros, personas,
  importe, duracion); copia las palabras de la pagina cuando sean concretas
FECHA: AAAA-MM-DD del hecho (si la pagina solo da el mes, pon el dia 1 y dilo)
TIPO: uno de tender_awarded, new_site, field_hiring, new_branch, season, inspection, leadership_change, funding, competitor_pain, other
FUENTE: la URL exacta de la pagina que lo dice; una por hallazgo, la mas directa
ENCAJA: si o no, y por que en una linea (nicho, tamano, personal en campo, zona)
Si una misma empresa tiene dos hechos, dos fichas. Al final, una seccion DESCARTES con lo
que viste y no incluyes y el motivo (grande, fuera de fecha, sin fecha, sin empresa, fuera
del nicho, sin pagina).

REGLAS QUE NO SE NEGOCIAN
- Cada hallazgo con su URL. Sin URL no hay hallazgo, por bueno que parezca.
- No inventes CIF, web ni provincia: si la pagina no los dice, deja el hueco.
- No juntes dos empresas en un hallazgo. Una UTE son varias empresas: nombra la que opera.
- No deduzcas: "ha ganado un contrato, asi que contratara gente" es una suposicion; la
  oferta de empleo publicada es el hecho.
- Escribe en espanol, en el lenguaje del nicho, sin adjetivos de venta.
```

La entrada lleva el nicho en una línea, la ventana de fechas (hoy menos los días pedidos), el
foco si lo hay, la tabla de tipos y caducidad del skill `senales` y la sección «Señales de por
qué ahora» del fichero del nicho.

### Paso 2 — de las fichas al JSON (`INSTRUCCIONES_SENALES_JSON`, fijo)

```
Convierte el dossier en JSON segun el esquema, sin anadir nada que no este en el dossier.
- Una entrada por ficha. "fuenteUrl" es la URL de la linea FUENTE, tal cual; solo puede ser
  una de las URLS CONSULTADAS. Si la ficha no tiene URL consultada, no la incluyas.
- "titulo": una linea en el lenguaje del nicho, con el dato concreto ("Adjudicada la
  limpieza de 14 colegios en Getxo por 2,1 M EUR"). "resumen": dos o tres frases con lo que
  dice la pagina, sin interpretar.
- "fecha": AAAA-MM-DD del hecho; cadena vacia si el dossier no la da.
- "fuerza": "high" solo si cambia la operativa de campo de forma medible y proxima
  (contrato adjudicado, centros nuevos, contratacion en volumen); "medium" si la cambia
  pero sin cifra; "low" si es contexto.
- "caducaDias": segun la tabla de tipos (60 adjudicacion o delegacion, 45 centro nuevo o
  queja, 30 contratacion u otros, 90 relevo o compra).
- "empresa.nombre": el nombre comercial, sin la forma juridica. "empresa.web",
  "empresa.cif" y "empresa.provincia": solo si estan en la ficha; si no, cadena vacia.
- "encaja": true solo si la ficha dice que encaja. "porQue": el motivo de la ficha.
- Lo que el dossier lista en DESCARTES no entra. En "avisos", lo que conviene que sepa
  quien vende (por ejemplo, que solo salieron grandes o que una fuente no cargo).
```

### Lo que el servidor comprueba después

Nombre de empresa no vacío; tipo de señal del CRM; `fuenteUrl` entre las páginas que la API
dice haber consultado; fecha, si viene, dentro de la ventana; caducidad entre 1 y 180 días
(fuera de rango, la del tipo); repetidas en la misma respuesta, fuera. Lo que no pasa va a
`descartadas` con su motivo, y se ve en la lista de búsquedas del panel.

